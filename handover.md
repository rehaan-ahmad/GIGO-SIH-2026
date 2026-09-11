# Project Handover: AI-Powered Automatic Block Planning (GIGO-SIH 2026)

## 📋 Project Overview
The **AI-Powered Automatic Block Planning** system is a spatio-temporal optimizer for railway maintenance. It ensures that maintenance tasks are scheduled optimally across time and space, preventing hazardous machinery overlap and minimizing train delays.

## 🏗️ Technical Implementation Details

### 1. Spatio-Temporal Logic
The system treats the track as a 1D linear coordinate (Chainage in km).
- **Spatial Clearance**: A safety buffer of 500m (0.5km) is enforced between any two tasks requiring heavy machinery in the same time window.
- **Temporal Packing**: Tasks are packed into availability windows. The solver ensures the sum of durations $\le$ window length.

### 2. The AI Pipeline
- **Ingestion**: Uses Pydantic for strict schema enforcement. Handles heterogeneous data from TMS, SMMS, and TDMS.
- **Scoring**: Implements a weighted AHP formula.
  - $C = (0.5 \cdot Sev) + (0.3 \cdot Overdue) + (0.2 \cdot DelayCost)$
  - Safety-critical signal tasks are boosted by $1.5\times$.
- **Solving**: Leverages **Google OR-Tools CP-SAT**. 
  - Uses `BoolVar` for task-window assignments.
  - Implements `AddImplication` for spatial conflicts.
  - Objective function maximizes $\sum (Score \cdot Assignment)$.

### 3. Frontend Visualization
- **The String Diagram**: Implemented using D3.js. 
  - **X-Axis**: Time (0-24h).
  - **Y-Axis**: Chainage (Km).
  - **Blocks**: Rendered as rectangles where `height = (end_km - start_km)`.
- **Re-optimization**: The `heuristic_agent.py` implements a greedy descent algorithm to ensure UI fluidity during manual overrides.

## 🛠 Tech Stack Summary
- **Backend**: FastAPI (Async), OR-Tools (CP-SAT), SQLAlchemy, PostgreSQL/PostGIS.
- **Frontend**: React 19, D3.js, Tailwind CSS 4.
- **Infra**: Docker, Docker Compose, Redis.

## 🏁 Final Milestone Status
- [x] **Phase 0: Repo Setup** $\rightarrow$ Completed
- [x] **Phase 1: Mock Data Layer** $\rightarrow$ Completed
- [x] **Phase 2: Scoring Engine** $\rightarrow$ Completed
- [x] **Phase 3: Constraint Solver** $\rightarrow$ Completed
- [x] **Phase 4: FastAPI Backend** $\rightarrow$ Completed
- [x] **Phase 5: React Frontend** $\rightarrow$ Completed
- [x] **Phase 6: Integration & Docker** $\rightarrow$ Completed
- [x] **Phase 7: PostGIS Spatial Integration** $\rightarrow$ Completed
- [x] **Phase 8: Demo Polish** $\rightarrow$ Completed

## 🚀 Deployment Instructions
1. Run `docker-compose up --build`.
2. Access UI at `http://localhost:5173`.
3. Use `/api/demo/load` to load the judge's scenario.
