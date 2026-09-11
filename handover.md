# Project Handover: AI-Powered Automatic Block Planning (GIGO-SIH 2026)

## Project Overview
This system is a Spatio-Temporal Rolling Block Optimizer designed for railway maintenance planning. It replaces traditional scheduling with a constraint-based optimization engine that ensures physical clearance (500m) and accounts for stochastic freight patterns.

## System Architecture
The system follows an agent-based pipeline:
1. **IngestionAgent**: Normalizes data from TMS, SMMS, TDMS, and COA sources.
2. **ScoringAgent**: Ranks tasks based on criticality (Severity, Overdue Days, Train Delay Cost).
3. **SolverAgent**: Uses OR-Tools CP-SAT for optimal spatio-temporal assignment.
4. **HeuristicAgent**: Provides <500ms real-time re-optimization for UI interactions.
5. **NotificationAgent**: Dispatches approved grants to departmental supervisors.

## Tech Stack
- **Backend**: FastAPI, OR-Tools CP-SAT, XGBoost, PostgreSQL+PostGIS, Redis, Celery.
- **Frontend**: React, D3.js, Tailwind CSS.
- **Deployment**: Docker, Docker Compose.

## Implementation Progress
*Initial setup complete. Implementation following the phased approach in `TODO.md`.*

---
## Completed Milestones
- [x] Repository Connection & Initial Setup
- [ ] Phase 0: Repo Setup & Environment
- [ ] Phase 1: Mock Data Layer
- [ ] Phase 2: Scoring Engine
- [ ] Phase 3: Constraint Solver
- [ ] Phase 4: FastAPI Backend
- [ ] Phase 5: React Frontend
- [ ] Phase 6: Integration & Docker
- [ ] Phase 7: PostGIS Spatial (Optional)
- [ ] Phase 8: Demo Polish
