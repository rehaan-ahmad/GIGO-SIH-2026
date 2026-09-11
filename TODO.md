# TODO.md — Aarush: Spatio-Temporal Rolling Block System

## Project: AI-Powered Automatic Block Planning (SIH 2026)
**Stack:** FastAPI · OR-Tools CP-SAT · XGBoost · PostgreSQL+PostGIS · Redis · React+D3.js · Docker  
**Differentiator:** Spatio-temporal optimizer, not a scheduler. Enforces 500m physical clearance + stochastic freight buffering.

---

## PHASE 0 — REPO SETUP
- [ ] `mkdir backend frontend data scripts docs`
- [ ] Init git: `git init && touch .gitignore`
- [ ] `.gitignore`: add `__pycache__/`, `node_modules/`, `.env`, `*.pyc`, `venv/`
- [ ] Root `docker-compose.yml` stub (fill in Phase 6)
- [ ] Root `README.md` with project summary + run instructions
- [ ] Create `backend/requirements.txt`:
  ```
  fastapi uvicorn[standard] ortools xgboost pandas pydantic
  psycopg2-binary sqlalchemy redis celery python-dotenv
  ```
- [ ] Create Python venv: `python -m venv venv && source venv/bin/activate`
- [ ] `pip install -r backend/requirements.txt`
- [ ] Init Vite frontend: `cd frontend && npm create vite@latest . -- --template react`
- [ ] Install frontend deps: `npm install axios d3 tailwindcss @tailwindcss/vite`
- [ ] Init Tailwind: `npx tailwindcss init -p`

---

## PHASE 1 — MOCK DATA LAYER
**Goal:** Realistic multi-source JSON simulating TMS, SMMS, TDMS, COA. No live CRIS access.

- [ ] Create `data/mocks.json` with all four data sources:
  - [ ] `tasks[]` — 15+ entries across Engineering/TRD/S&T depts
    - Fields: `task_id, dept, type, chainage_start_km, chainage_end_km, duration_mins, severity (1-10), days_overdue, needs_power_block (bool), machinery_type`
  - [ ] `corridor_availability[]` — 7-day rolling windows (weekly plan)
    - Fields: `window_id, date, start_time, end_time, freight_probability (0-1), passenger_train_slots[]`
  - [ ] `train_timetable[]` — fixed passenger trains with chainage, times
  - [ ] `freight_forecast[]` — stochastic entries with `±120min` buffer field
- [ ] Create `scripts/generate_mocks.py` — script to regenerate realistic mock data programmatically (50+ tasks, 30-day horizon)
- [ ] Validate mock schema matches all backend Pydantic models before proceeding

**Dept distribution in mocks:**
| Dept | System | Task Examples |
|------|--------|---------------|
| Engineering | TMS | Track tamping, rail renewal, deep screening |
| TRD | TDMS | OHE mast repair, feeder cable, booster transformer |
| S&T | SMMS | Point machine testing, signal post, track circuit |

---

## PHASE 2 — SCORING ENGINE (`backend/scoring.py`)
**Goal:** Rank tasks by criticality before solver sees them. Reduces solver search space.

- [ ] Implement AHP-weighted criticality formula:
  ```
  C_i = (w1 * Severity) + (w2 * OverdueDays) + (w3 * TrainDelayCost)
  ```
  Weights: `w1=0.5, w2=0.3, w3=0.2` (tune after testing)
- [ ] Add `TrainDelayCost` field — estimate delay impact per chainage segment
- [ ] Normalize scores 0–100 for solver integer encoding
- [ ] Add `dept_flag` urgency multiplier: S&T signal failures = 1.5x boost
- [ ] Add `power_block_flag` grouping: tasks needing power block cluster together
- [ ] Unit test `scoring.py` with 5 mock tasks — verify rank order makes sense
- [ ] Export: `score_tasks(tasks: list) -> list[dict]` sorted descending by `criticality_score`

**Optional (XGBoost upgrade):**
- [ ] Train XGBoost model on synthetic historical data (defect → actual_delay_hrs)
- [ ] Replace static w3 with XGBoost predicted delay cost
- [ ] Save model: `models/criticality_model.pkl`
- [ ] Load in `scoring.py` at startup

---

## PHASE 3 — CONSTRAINT SOLVER (`backend/solver.py`)
**Goal:** OR-Tools CP-SAT assigns tasks to corridor windows. Must enforce spatial + temporal constraints.

### 3.1 Core CP-SAT Model
- [ ] Import `from ortools.sat.python import cp_model`
- [ ] Create `CpModel()` instance
- [ ] Create `BoolVar` for each `(task, window)` pair: `assign_{task_id}_{window_id}`

### 3.2 Constraints (implement in order)
- [ ] **C1 — Single Assignment:** Each task assigned to exactly one window
  ```python
  model.AddExactlyOne(task_vars[(t['task_id'], w['window_id'])] for w in windows)
  ```
- [ ] **C2 — Window Capacity:** Each window has max duration. Sum of assigned task durations ≤ window duration
- [ ] **C3 — Spatial Deconfliction (CRITICAL):** Two tasks with machinery overlap within 500m chainage cannot share same window
  ```python
  # Spatial overlap check
  overlap = max(t1['chainage_start_km'], t2['chainage_start_km']) <= min(t1['chainage_end_km'], t2['chainage_end_km'])
  if overlap and both_heavy_machinery:
      model.AddImplication(assign[t1,w], assign[t2,w].Not())
  ```
- [ ] **C4 — Power Block Grouping:** Tasks with `needs_power_block=True` on overlapping chainage MUST share same window (co-scheduling incentive)
- [ ] **C5 — Freight Buffer:** Windows with `freight_probability > 0.4` cannot hold tasks with `duration_mins > 120` (stochastic guard)
- [ ] **C6 — Department Sequence:** Engineering (track) must complete before TRD (OHE) on same chainage if safety dependency exists

### 3.3 Objective
- [ ] Maximize sum of `criticality_score * assigned_var` across all (task, window) pairs
- [ ] Set solver time limit: `solver.parameters.max_time_in_seconds = 10.0`
- [ ] Return `OPTIMAL` or `FEASIBLE` results; log if only `FEASIBLE`

### 3.4 Two-Tier Strategy
- [ ] **Tier 1 (background):** Full CP-SAT run nightly → 30-day strategic plan, stored in DB
- [ ] **Tier 2 (real-time):** Greedy heuristic re-optimizer < 500ms for Controller UI drag interactions
  - Greedy: sort by `criticality_score`, assign to first valid window via simple constraint check
- [ ] Expose flag: `solver_mode: "exact" | "heuristic"` in API request

---

## PHASE 4 — FASTAPI BACKEND (`backend/main.py`)
**Goal:** REST API exposing scoring + solver. Async-ready for Celery background jobs.

### 4.1 Endpoints
- [ ] `POST /api/optimize-blocks` — run scorer + solver, return schedule
  - Body: `{ "horizon": "weekly" | "monthly", "solver_mode": "exact" | "heuristic" }`
  - Response: `{ status, schedule[], unscheduled_tasks[], solver_status }`
- [ ] `GET /api/tasks` — return all tasks with criticality scores
- [ ] `GET /api/windows` — return corridor availability for date range
- [ ] `GET /api/schedule/{date}` — fetch stored daily block plan
- [ ] `POST /api/reoptimize` — Tier 2 heuristic re-run (< 500ms, triggered by Controller drag)
  - Body: `{ "locked_tasks": [], "forced_window": {...} }`
- [ ] `GET /api/health` — liveness check

### 4.2 Pydantic Models
- [ ] `Task` model with all fields + validators
- [ ] `CorridorWindow` model
- [ ] `ScheduleResponse` model
- [ ] `ReoptimizeRequest` model

### 4.3 CORS + Middleware
- [ ] Add `CORSMiddleware` for React dev server (`localhost:5173`)
- [ ] Add request logging middleware

### 4.4 Startup
- [ ] On startup: load `data/mocks.json` into memory (or seed DB)
- [ ] Run: `uvicorn main:app --reload --port 8000`

### 4.5 Celery (optional for hackathon, implement if time)
- [ ] `backend/tasks.py` — Celery task: `run_nightly_solver()`
- [ ] Redis as broker: `CELERY_BROKER_URL=redis://localhost:6379/0`
- [ ] Cron: nightly 00:00 → run 30-day exact solver

---

## PHASE 5 — REACT FRONTEND
**Goal:** String Diagram UI. Railway judges expect time-distance graphs, NOT calendar widgets.

### 5.1 Component Tree
```
App.jsx
├── Dashboard.jsx          ← main layout, date range selector
├── StringDiagram.jsx      ← D3.js time-distance graph (CRITICAL)
├── TaskList.jsx           ← sidebar: ranked tasks with criticality scores
├── BlockCard.jsx          ← info card on block click
├── ControlPanel.jsx       ← horizon selector, trigger optimize button
└── ConflictAlert.jsx      ← shows unscheduled tasks + reason
```

### 5.2 StringDiagram.jsx (D3.js) — PRIORITY
- [ ] X-axis: Time (00:00–24:00 or multi-day)
- [ ] Y-axis: Chainage Km (dynamic domain from data)
- [ ] Render maintenance blocks as colored rectangles:
  - Engineering = red, TRD = blue, S&T = green
  - Integrated (multi-dept) blocks = gradient/hatched fill
- [ ] Render train paths as diagonal lines (time-distance strings)
- [ ] Render freight buffer zones as semi-transparent shading
- [ ] Click on block → show `BlockCard` with task details
- [ ] Drag block to new window → call `POST /api/reoptimize` → re-render
- [ ] 500ms debounce on drag before firing API call

### 5.3 Dashboard.jsx
- [ ] Date range picker (7-day default, 30-day option)
- [ ] "Generate Plan" button → `POST /api/optimize-blocks`
- [ ] Loading spinner during solver run
- [ ] Summary stats bar: total tasks, scheduled %, integrated blocks count, estimated downtime saved

### 5.4 TaskList.jsx
- [ ] Sorted by `criticality_score` descending
- [ ] Color-coded urgency badges (red > 8, amber 5-8, green < 5)
- [ ] Mark unscheduled tasks with warning icon + reason

### 5.5 API Integration (`src/api.js`)
- [ ] `optimizeBlocks(horizon, mode)` → axios POST
- [ ] `reoptimize(lockedTasks, forcedWindow)` → axios POST
- [ ] `fetchTasks()` → axios GET
- [ ] Handle loading/error states globally

### 5.6 Styling
- [ ] Tailwind dark theme (railway control room aesthetic — dark bg, bright accent lines)
- [ ] Responsive layout: sidebar + main diagram
- [ ] Department color legend

---

## PHASE 6 — INTEGRATION & DOCKER
- [ ] `docker-compose.yml` with services:
  - `backend` (FastAPI, port 8000)
  - `frontend` (Vite, port 5173)
  - `redis` (port 6379)
  - `postgres` (port 5432, with PostGIS image: `postgis/postgis:15-3.3`)
- [ ] `backend/Dockerfile`:
  ```dockerfile
  FROM python:3.11-slim
  WORKDIR /app
  COPY requirements.txt .
  RUN pip install -r requirements.txt
  COPY . .
  CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
  ```
- [ ] `frontend/Dockerfile`:
  ```dockerfile
  FROM node:20-alpine
  WORKDIR /app
  COPY package*.json .
  RUN npm install
  COPY . .
  CMD ["npm", "run", "dev", "--", "--host"]
  ```
- [ ] Environment vars via `.env`: `DB_URL, REDIS_URL, CORS_ORIGIN`
- [ ] `docker-compose up --build` → all services boot
- [ ] End-to-end test: generate plan via UI → verify String Diagram renders blocks

---

## PHASE 7 — POSTGI S SPATIAL (optional, HIGH IMPACT for judges)
- [ ] Init PostGIS in DB: `CREATE EXTENSION postgis;`
- [ ] Create `track_segments` table with Linear Reference System:
  ```sql
  CREATE TABLE track_segments (
    id SERIAL PRIMARY KEY,
    segment_id TEXT,
    geom GEOMETRY(LINESTRING, 4326),
    chainage_start FLOAT,
    chainage_end FLOAT
  );
  ```
- [ ] Map abstract chainage (e.g., Km 1042/15) to 1D spatial model
- [ ] Compute task spatial proximity in solver via PostGIS `ST_DWithin` instead of raw km arithmetic
- [ ] This unlocks real "500m buffer" computation on actual track geometry

---

## PHASE 8 — DEMO POLISH
- [ ] Pre-load demo scenario: 3 integrated blocks showing Engineering+TRD+S&T merged
- [ ] Demo script: Controller logs in → sees 7-day plan → VIP train added → drag block → re-optimize → new plan in <500ms
- [ ] Add "Why this schedule?" explainability panel — show top 3 constraint reasons per block
- [ ] Export plan as PDF/CSV button
- [ ] Mobile-responsive StringDiagram (judges may demo on tablet)

---

## CRITICAL PATH (Hackathon Minimum Viable Demo)

```
Phase 0 setup (1h)
  ↓
Phase 1 mock data (2h)
  ↓
Phase 2 scoring.py (1h)
  ↓
Phase 3 solver.py — constraints C1-C3 only (3h)
  ↓
Phase 4 /api/optimize-blocks endpoint (1h)
  ↓
Phase 5 StringDiagram + Dashboard (4h)
  ↓
Phase 6 docker-compose (1h)
  ↓
Phase 8 demo scenario (1h)
```

**Total minimum:** ~14h. PostGIS, XGBoost, Celery = bonus if time allows.

---

## KNOWN RISKS

| Risk | Mitigation |
|------|-----------|
| CP-SAT too slow for 50+ tasks | 10s timeout + fallback heuristic always ready |
| D3.js String Diagram complexity | Build static version first, add drag last |
| PostGIS setup time | Skip if < 8h remaining; use pure km arithmetic in solver |
| Docker networking issues | Test backend alone first, add compose layer last |
| Mock data not realistic enough | Use `scripts/generate_mocks.py` for 50-task diversity |
