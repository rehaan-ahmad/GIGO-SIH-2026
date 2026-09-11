# agents.md — Aarush System Agent Definitions

## Architecture Overview

Aarush runs five functional agents. In hackathon build: agents = Python modules/functions, not separate processes. In production: each agent = microservice or Celery worker.

```
[Data Sources]          [Agents]                    [Output]
TMS/SMMS/TDMS  →  IngestionAgent
COA Forecast   →  IngestionAgent  →  ScoringAgent  →  SolverAgent  →  Block Plan API
                                                    ↘  HeuristicAgent  →  Real-time re-optimize
                                  SolverAgent  →  NotificationAgent  →  BDMS grants
```

---

## Agent 1: IngestionAgent
**File:** `backend/agents/ingestion_agent.py`  
**Role:** Polls and normalizes data from all four source systems. Outputs unified task schema.

### Inputs
| Source | System | Format | Polling |
|--------|--------|--------|---------|
| Track defects | TMS | JSON / REST mock | Every 6h |
| Signal defects | SMMS | JSON / REST mock | Every 6h |
| OHE defects | TDMS | JSON / REST mock | Every 6h |
| Corridor windows | COA | JSON / REST mock | Every 1h |

### Responsibilities
- Pull from `data/mocks.json` (hackathon) or live REST endpoints (production)
- Normalize heterogeneous schemas into unified `Task` Pydantic model
- Attach `source_system` field: `"TMS" | "SMMS" | "TDMS"`
- Validate required fields: `chainage_start_km`, `severity`, `duration_mins`
- Flag incomplete records (missing chainage → reject, log warning)
- Inject `freight_probability` from COA forecast into `CorridorWindow` objects
- Apply stochastic freight buffer: windows with `freight_probability > 0.4` → set `buffer_mins = 120`

### Outputs
```python
{
  "tasks": [Task],             # unified task list
  "corridor_windows": [Window], # availability windows with freight buffers
  "ingestion_timestamp": str,
  "rejected_records": int
}
```

### Hackathon implementation
```python
# agents/ingestion_agent.py
import json

def ingest() -> dict:
    with open('../data/mocks.json') as f:
        raw = json.load(f)
    tasks = [normalize_task(t) for t in raw['tasks']]
    windows = [normalize_window(w) for w in raw['corridor_availability']]
    return {"tasks": tasks, "corridor_windows": windows}
```

---

## Agent 2: ScoringAgent
**File:** `backend/agents/scoring_agent.py`  
**Role:** Assigns criticality scores to tasks. Determines solver priority ordering.

### Inputs
- `tasks: list[Task]` from IngestionAgent

### Scoring Formula
```
C_i = (w1 * Severity) + (w2 * OverdueDays) + (w3 * TrainDelayCost)

w1 = 0.50  ← defect severity (1-10 scale)
w2 = 0.30  ← days past scheduled maintenance
w3 = 0.20  ← estimated train delay impact cost

Multipliers:
  S&T signal failure tasks: × 1.5  (safety-critical)
  power_block required: + 5 points  (clustering bonus)
```

### Responsibilities
- Compute `criticality_score` for each task
- Normalize scores 0–100 (for CP-SAT integer encoding: multiply × 10)
- Group tasks by `needs_power_block=True` AND chainage overlap → tag as `shadow_block_candidate`
- Sort output descending by `criticality_score`
- Log top 5 critical tasks at each scoring run

### Optional XGBoost upgrade
- Model: `models/criticality_model.pkl`
- Input features: `[severity, days_overdue, dept, machinery_type, chainage_zone]`
- Output: predicted `train_delay_hrs` → used as `TrainDelayCost` in formula
- Train on synthetic data in `scripts/train_criticality_model.py`

### Outputs
```python
[
  {
    ...task_fields,
    "criticality_score": float,  # 0-100
    "shadow_block_candidate": bool,
    "priority_rank": int
  }
]
```

---

## Agent 3: SolverAgent
**File:** `backend/agents/solver_agent.py`  
**Role:** Core optimization brain. Runs OR-Tools CP-SAT to assign tasks to corridor windows.

### Inputs
- `scored_tasks: list` from ScoringAgent
- `corridor_windows: list` from IngestionAgent
- `solver_mode: "exact" | "heuristic"`

### CP-SAT Model
**Decision variables:** `assign[task_id][window_id]` ∈ {0, 1}

**Constraints (in priority order):**

| ID | Constraint | Description |
|----|-----------|-------------|
| C1 | Single assignment | Each task → exactly one window |
| C2 | Window capacity | Sum(task durations in window) ≤ window duration |
| C3 | Spatial deconfliction | Tasks with machinery overlap within 500m → different windows |
| C4 | Power block grouping | `needs_power_block=True` tasks on same chainage → same window |
| C5 | Freight buffer | High freight probability windows → no long-duration tasks |
| C6 | Dept sequence | Engineering tasks before TRD tasks on same chainage (safety) |

**Objective:** Maximize `Σ (assign[t][w] × criticality_score[t] × 10)`

### Time Limits
- Exact mode: `max_time_in_seconds = 10.0`
- Returns `OPTIMAL` or `FEASIBLE`; logs solver status

### Responsibilities
- Build CP-SAT model fresh each run
- Detect and log infeasible assignments (task with no valid window)
- Return `unscheduled_tasks[]` with reason codes:
  - `NO_VALID_WINDOW` — no window fits duration
  - `SPATIAL_CONFLICT` — all windows have heavy machinery overlap
  - `FREIGHT_BLOCKED` — all windows have high freight probability
- Produce 7-day rolling plan (weekly) or 30-day strategic plan (monthly)

### Outputs
```python
{
  "schedule": [
    {
      "task_id": str,
      "window_id": str,
      "dept": str,
      "chainage_start_km": float,
      "chainage_end_km": float,
      "scheduled_start": str,  # ISO datetime
      "scheduled_end": str,
      "is_integrated_block": bool,  # multi-dept co-scheduled
      "co_scheduled_with": [str]    # task_ids in same block
    }
  ],
  "unscheduled_tasks": [{"task_id": str, "reason": str}],
  "solver_status": "OPTIMAL" | "FEASIBLE" | "INFEASIBLE",
  "integrated_block_count": int,
  "total_downtime_hrs_saved": float
}
```

---

## Agent 4: HeuristicAgent
**File:** `backend/agents/heuristic_agent.py` 
**Role:** Real-time re-optimizer. Fires when Controller drags a block in UI. Must complete < 500ms.

### When triggered
- Controller drags maintenance block to new time window in StringDiagram
- VIP train inserted → some blocks need shifting
- Manual override of any scheduled task

### Algorithm
Greedy descent (not CP-SAT — too slow for real-time):
1. Accept `locked_tasks[]` (blocks Controller has approved — cannot move)
2. Accept `forced_window` (where Controller dropped the dragged task)
3. For each remaining unscheduled/displaced task, sorted by `criticality_score`:
   - Try `forced_window` first
   - Check C1 (capacity), C3 (spatial), C5 (freight) constraints only
   - If valid → assign
   - Else → try next available window
4. Return updated schedule in < 500ms

### Inputs
```python
{
  "full_schedule": [...],     # current full schedule
  "locked_tasks": [str],      # task_ids Controller locked
  "forced_window": {...},     # new window for dragged task
  "dragged_task_id": str
}
```

### Outputs
Same schema as SolverAgent output, plus `"reoptimize_mode": "heuristic"`.

---

## Agent 5: NotificationAgent
**File:** `backend/agents/notification_agent.py` 
**Role:** Dispatches approved block plans to departmental supervisors. Simulates BDMS grant issuance.

### Triggers
- Controller clicks "Approve Plan" in UI
- Nightly solver run completes (auto-dispatch for next 24h blocks)

### Responsibilities
- Format approved schedule into dept-specific block grants
- In hackathon: write to `data/approved_grants.json` + log to console
- In production: POST to BDMS API endpoint per department
- Group grants by department, sort by scheduled time
- Generate plain-language grant text:
  ```
  BLOCK GRANT — Engineering Dept
  Date: 2026-10-15 | Window: 02:00–06:00
  Section: Km 1042.0 to 1045.5
  Tasks: Track Tamping (CSM) [TMS-8092]
  Co-scheduled with: TRD OHE Mast Repair [TDMS-441]
  Power disconnection required: YES
  ```

### Outputs
```python
[
  {
    "grant_id": str,
    "dept": str,
    "date": str,
    "window_start": str,
    "window_end": str,
    "chainage_start_km": float,
    "chainage_end_km": float,
    "tasks": [str],
    "power_off_required": bool,
    "grant_text": str
  }
]
```

---

## Agent Orchestration (`backend/orchestrator.py`)

Called by `/api/optimize-blocks` endpoint:

```python
# backend/orchestrator.py

from agents.ingestion_agent import ingest
from agents.scoring_agent import score_tasks
from agents.solver_agent import solve
from agents.notification_agent import dispatch_grants

def run_optimization_pipeline(horizon: str, solver_mode: str) -> dict:
    # 1. Ingest
    data = ingest()
    
    # 2. Score
    scored_tasks = score_tasks(data["tasks"])
    
    # 3. Solve
    result = solve(scored_tasks, data["corridor_windows"], 
                   mode=solver_mode, horizon=horizon)
    
    # 4. Notify (only if mode=exact and plan approved)
    # dispatch_grants(result["schedule"])  ← call after Controller approval
    
    return result
```

---

## Agent Data Flow Summary

```
mocks.json
    │
    ▼
IngestionAgent ──────────────────────────────────────┐
    │ tasks[]                   corridor_windows[]    │
    ▼                                                 │
ScoringAgent                                          │
    │ scored_tasks[] (with criticality_score)         │
    ▼                                                 │
SolverAgent ←────────────────────────────────────────┘
    │ schedule[], unscheduled[]
    │
    ├──→ API Response → Frontend StringDiagram
    │
    └──→ Controller approves
              │
              ▼
        NotificationAgent → dept block grants
              ↑
        HeuristicAgent ← Controller drags block in UI
```
