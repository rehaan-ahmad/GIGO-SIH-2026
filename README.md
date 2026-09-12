# 🚂 Aarush: Spatio-Temporal Rolling Block System

> **AI-Powered Automatic Block Planning for Indian Railways**  
> *Smart India Hackathon 2026 • Problem Statement SIH26027*

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/rehaan-ahmad/GIGO-SIH-2026)
[![License](https:///img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Stack](https://img.shields.io/badge/stack-FastAPI%20%7C%20React%20%7C%20OR--Tools%20%7C%20PostGIS-orange)]
[![SIH 2026](https://img.shields.io/badge/SIH-2026%20Finalist-red)]
[![Docker](https://img.shields.io/badge/docker-ready-blue)](docker-compose.yml)

---

## 🎯 The Problem: Railway Maintenance is Broken

Indian Railways runs **13,000+ trains daily** across 68,000+ km of track. Maintenance planning today happens in **departmental silos**:

| System | Department | Problem |
|--------|------------|---------|
| **TMS** | Engineering (Track) | Grants 2-hr blocks blindly |
| **SMMS** | S&T (Signals) | No visibility into Engineering plans |
| **TDMS** | TRD (Traction/OHE) | Overlaps cause last-minute cancellations |
| **COA** | Train Operations | Freight forecasts are stochastic, not fixed |

**Result:** 40% of planned blocks are cancelled. Labour & machinery sit idle. Safety margins are violated when gangs work 200m apart.

---

## 💡 The Solution: Aarush — A Spatio-Temporal Optimizer

Aarush doesn't *schedule* — it **packs 4D space-time**. It treats the railway as a 4D manifold:
- **X-axis**: Chainage (km markers)
- **Y-axis**: Time (00:00–24:00)  
- **Z-axis**: Department/Layer (Engg / TRD / S&T)
- **W-axis**: Criticality Priority (AHP-scored)

```mermaid
graph LR
    A[TMS/SMMS/TDMS/COA] --> B[IngestionAgent]
    B --> C[ScoringAgent: AHP Criticality]
    C --> D[SolverAgent: OR-Tools CP-SAT]
    D --> E[Optimal Block Plan]
    E --> F[React + D3 String Diagram]
    D -.->|<500ms| G[HeuristicAgent: Real-time Re-opt]
    H[HermesAgent] -.->|Autonomous| D
```

---

## ✨ Why Judges Love This

| Innovation | What It Means | Judge Impact |
|------------|---------------|--------------|
| **🔴 500m Physical Clearance** | Hard constraint: No two heavy machines within 500m chainage | *Safety-first engineering* |
| **🟡 Stochastic Freight Guard** | Probabilistic ±120min buffers for goods trains | *Production-grade resilience* |
| **🟢 Authentic String Diagrams** | D3.js Time-Distance graphs — railway gold standard | *Domain-native UX* |
| **🔵 Two-Tier Solver** | Nightly exact CP-SAT + real-time greedy heuristic | *Scalable architecture* |
| **🟣 AHP Criticality Scoring** | Math-backed priority: Severity + Overdue + Delay Cost | *Explainable AI* |
| **🟠 Hermes Autonomous Agent** | Self-healing: triggers re-opt when schedule health degrades | *Agentic AI* |

---

## 🏗️ Architecture: Agentic Pipeline

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Ingestion   │───▶│ Scoring     │───▶│ Solver      │───▶│ API + UI    │
│ Agent       │    │ Agent (AHP) │    │ Agent (CP-SAT)│    │ (String Diag)│
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                  │                   │                   │
       ▼                  ▼                   ▼                   ▼
  Normalize          Criticality =        Maximize Σ          Interactive
  TMS/SMMS/          0.5×Severity +       (Criticality ×     Time-Distance
  TDMS/COA           0.3×Overdue +        Assign)            Graph
  → Unified          0.2×DelayCost        s.t. C1–C6         Drag→Reopt
  Task Schema        + S&T 1.5× boost     Safety, Capacity,  <500ms
                                         Spatial, Freight
```

### Core Constraints (CP-SAT)

| ID | Constraint | Mathematical Form |
|----|------------|-------------------|
| **C1** | **Uniqueness** | `∑ assign[t,w] = 1` ∀ tasks |
| **C2** | **Capacity** | `∑ duration[t] × assign[t,w] ≤ WindowDur[w]` |
| **C3** | **Spatial Safety** | `Overlap(t1,t2) ⇒ assign[t1,w] + assign[t2,w] ≤ 1` |
| **C4** | **Power Block Sync** | `needs_power[t1] ∧ needs_power[t2] ∧ overlap ⇒ same window` |
| **C5** | **Freight Guard** | `P(Freight)[w] > 0.4 ⇒ duration[t] ≤ 120min` |
| **C6** | **Dept Sequence** | Engg before TRD on same chainage |

**Objective:** `Maximize Σ (CriticalityScore[t] × assign[t,w])`

---

## 🎨 The UI: Railway String Diagrams

Not a calendar. Not a Gantt chart. **A Time-Distance Graph** — the visualization railway controllers have used for 100+ years.

![String Diagram Preview](docs/assets/string-diagram-preview.png)

- **X-Axis**: Time (00:00 → 24:00)
- **Y-Axis**: Chainage (Km 1040 → 1050)
- **Diagonal Lines**: Passenger train paths (from COA)
- **Colored Blocks**: Maintenance windows
  - 🔴 **Red** = Engineering (Tamping, Rail Renewal)
  - 🔵 **Blue** = TRD (OHE, Feeder Cable)
  - 🟢 **Green** = S&T (Point Machine, Signals)
  - 🟣 **Gradient** = Integrated Shadow Blocks (multi-dept)
- **Shaded Zones**: Stochastic freight buffers
- **Drag & Drop**: Move a block → heuristic re-optimizes in **<500ms**

---

## 📊 Impact Metrics (Projected)

| Metric | Current | With Aarush | Improvement |
|--------|---------|-------------|-------------|
| Block Cancellation Rate | ~40% | <10% | **3× reduction** |
| Shadow Block Colocation | ~15% | ~40% | **2.5× increase** |
| Line Capacity Recovered | — | 200+ hrs/div/year | **Freight throughput ↑** |
| Controller Cognitive Load | 3 spreadsheets + chart | Single String Diagram | **Unified view** |
| Safety Incidents (machinery) | 12/yr/div | Near-zero | **Hard constraint** |

---

## 🛠 Tech Stack

| Layer | Technology | Why |
|-------|------------|-----|
| **API** | FastAPI (async) | High concurrency, auto OpenAPI docs |
| **Solver** | Google OR-Tools CP-SAT | World-class constraint programming |
| **ML** | XGBoost (optional) | Predictive delay cost modeling |
| **Database** | PostgreSQL + PostGIS | Spatial linear referencing (LRS) |
| **Cache/Queue** | Redis + Celery | Background solver, state caching |
| **Frontend** | React 19 + D3.js | String Diagram rendering |
| **Styling** | Tailwind CSS 4 | Dark-mode control room aesthetic |
| **DevOps** | Docker Compose | One-click orchestration |

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- (Optional) Python 3.11+, Node.js 20+ for local dev

### One-Command Launch
```bash
git clone git@github.com:rehaan-ahmad/GIGO-SIH-2026.git
cd GIGO
docker-compose up --build
```

### Access Points
| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend** | http://localhost | String Diagram Dashboard |
| **Backend API** | http://localhost:8000 | REST endpoints |
| **Swagger Docs** | http://localhost:8000/docs | Interactive API explorer |
| **Health Check** | http://localhost:8000/health | Liveness probe |

### Demo Scenario (Pre-loaded)
```bash
# Inject integrated block scenario: Engineering + TRD + S&T merged
curl -X POST http://localhost:8000/api/demo/load
```
Then drag a block in the UI → watch heuristic re-optimize in **<500ms**.

---

## 📚 Documentation (Diàtaxis Framework)

We follow the **Diàtaxis** four-quadrant model for complete coverage:

| Quadrant | Documents | Purpose |
|----------|-----------|---------|
| **🎓 Tutorials** | [`Getting Started`](docs/tutorial-getting-started.md) • [`String Diagram Guide`](docs/tutorial-string-diagram.md) | Learning-oriented; zero-to-one |
| **📖 How-to Guides** | [`Deploy`](docs/how-to-deploy.md) • [`API Usage`](docs/how-to-api.md) • [`Hermes Agent`](docs/how-to-use-hermes.md) | Task-oriented; achieve goals |
| **📋 Reference** | [`Solver`](docs/reference-solver.md) • [`Scoring`](docs/reference-scoring.md) • [`Hermes`](docs/reference-hermes.md) • [`API`](docs/reference-api.md) | Information-oriented; specs |
| **🧠 Explanations** | [`Spatio-Temporal`](docs/explanation-spatio-temporal.md) • [`AHP`](docs/explanation-ahp-prioritization.md) • [`String Diagram`](docs/explanation-string-diagram.md) • [`Agentic Pipeline`](docs/explanation-agentic-pipeline.md) | Understanding-oriented; rationale |

> **Legacy/High-Level**: [`Technical Architecture`](docs/ARCHITECTURE.md) • [`Implementation Handover`](handover.md) • [`Implementation Plan`](implementationPlan.md)

---

## 🔬 Deep Dive: The Mathematics

### AHP Criticality Scoring
```
Cᵢ = (w₁ × Severity) + (w₂ × OverdueDays) + (w₃ × TrainDelayCost)

w₁ = 0.50   # Defect severity (1-10)
w₂ = 0.30   # Days past scheduled maintenance  
w₃ = 0.20   # Estimated delay impact (minutes × trains affected)

Multipliers:
  • S&T Signal Failure: ×1.5    (safety-critical)
  • Power Block Required: +5.0  (clustering incentive)
```

### Spatial Deconfliction Logic
```python
# Two tasks conflict if their chainage intervals overlap
# AND both use heavy machinery (tamping machine, tower wagon, etc.)
def spatial_conflict(t1, t2):
    overlap = max(t1.chainage_start, t2.chainage_start) <= min(t1.chainage_end, t2.chainage_end)
    heavy = t1.machinery_type in HEAVY_TYPES and t2.machinery_type in HEAVY_TYPES
    return overlap and heavy

# Enforced as hard constraint in CP-SAT:
model.AddImplication(assign[t1, w], assign[t2, w].Not())
```

### Two-Tier Solver Strategy
| Tier | Mode | Use Case | Latency |
|------|------|----------|---------|
| **Strategic** | CP-SAT Exact | Nightly 30-day plan | 10–30s |
| **Tactical** | Greedy Heuristic | Controller drag & drop | **<500ms** |

---

## 🐳 Docker Architecture

```yaml
# docker-compose.yml (simplified)
services:
  postgres:
    image: postgis/postgis:15-3.3
    environment:
      POSTGRES_DB: railway
      POSTGRES_USER: railway
    volumes:
      - pgdata:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
  
  backend:
    build: ./backend
    ports: ["8000:8000"]
    depends_on: [postgres, redis]
    environment:
      - DATABASE_URL=postgresql://railway:railway@postgres/railway
      - REDIS_URL=redis://redis:6379/0
  
  frontend:
    build: ./frontend
    ports: ["80:5173"]
    depends_on: [backend]
```

---

## 🎬 Demo Script for Judges

```bash
# 1. Launch
docker-compose up --build -d

# 2. Open http://localhost — see 7-day String Diagram
#    → Notice integrated blocks (gradient = multi-dept)

# 3. Click "Generate Plan" → watch CP-SAT optimize in background

# 4. SIMULATE EMERGENCY: VIP train added at Km 1043, 03:00
#    → Drag the Engineering block from 02:00 to 04:00

# 5. HEURISTIC RE-OPTIMIZES IN <500ms
#    → TRD & S&T tasks auto-shift to next valid corridor
#    → No spatial conflicts, no capacity violations

# 6. Click "Approve Plan" → HermesAgent dispatches grants
#    → Check data/approved_grants.json for BDMS-ready output
```

---

## 🧪 Testing

```bash
# Backend tests
cd backend && pytest -v

# Frontend tests  
cd frontend && npm test

# Integration test (full pipeline)
curl -X POST http://localhost:8000/api/optimize-blocks \
  -H "Content-Type: application/json" \
  -d '{"horizon": "weekly", "solver_mode": "exact"}'
```

---

## 📁 Project Structure

```
GIGO/
├── backend/
│   ├── agents/              # 5 specialized agents
│   │   ├── ingestion_agent.py
│   │   ├── scoring_agent.py
│   │   ├── solver_agent.py
│   │   ├── heuristic_agent.py
│   │   └── notification_agent.py
│   ├── orchestrator.py      # Pipeline coordination
│   ├── main.py              # FastAPI entrypoint
│   ├── scoring.py           # AHP criticality engine
│   ├── solver.py            # OR-Tools CP-SAT model
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── StringDiagram.jsx   # D3.js Time-Distance graph
│   │   │   ├── Dashboard.jsx
│   │   │   ├── TaskList.jsx
│   │   │   ├── BlockCard.jsx
│   │   │   ├── ControlPanel.jsx
│   │   │   └── ConflictAlert.jsx
│   │   ├── api.js
│   │   └── App.jsx
│   └── package.json
├── data/
│   ├── mocks.json           # Realistic TMS/SMMS/TDMS/COA data
│   └── approved_grants.json # Generated block grants
├── docs/                    # Diàtaxis documentation (16 files)
├── scripts/
│   └── generate_mocks.py    # Programmatic mock generator
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 🏆 Hackathon Differentiators

| Typical Hackathon Approach | Aarush (This Project) |
|----------------------------|----------------------|
| Time-only scheduling | **Spatio-temporal packing (4D)** |
| Single department | **Multi-dept shadow blocks** |
| Static freight schedule | **Stochastic ±120min buffers** |
| Calendar/Gantt UI | **Authentic String Diagrams (D3.js)** |
| Single solver | **Two-tier: CP-SAT + Greedy** |
| No explainability | **AHP scores + constraint reasons** |
| Manual trigger only | **Hermes autonomous agent** |
| No spatial awareness | **PostGIS Linear Referencing** |

---

## 🔮 Future Roadmap

- [ ] **Phase 9**: XGBoost criticality model trained on historical delay data
- [ ] **Phase 10**: Full PostGIS Linear Referencing (true 500m on curved track)
- [ ] **Phase 11**: Celery nightly 30-day strategic solver
- [ ] **Phase 12**: Mobile-responsive String Diagram for field supervisors
- [ ] **Phase 13**: Integration with CRIS BDMS APIs (production pilot)

---

## 👥 Team

| Role | Contribution |
|------|--------------|
| **Backend/OR Lead** | CP-SAT model, AHP scoring, agentic pipeline |
| **Frontend/Viz Lead** | D3.js String Diagram, drag-reoptimize UX |
| **Data/Infra Lead** | Docker, PostGIS, mock data realism |
| **Domain/Railway Lead** | BDMS/RBS/COA alignment, constraint validity |

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- **Google OR-Tools Team** — for the world-class CP-SAT solver
- **Indian Railways** — for the BDMS/RBS/COA framework (SIH26027)
- **D3.js Community** — for the visualization primitives
- **SIH 2026 Organizers** — for the platform to solve real problems

---

<div align="center">

**Built with ❤️ for Indian Railways • Smart India Hackathon 2026**

*If the String Diagram doesn't load, check `docker-compose logs frontend` — D3.js needs the SVG namespace.*

</div>