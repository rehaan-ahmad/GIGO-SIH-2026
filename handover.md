# Project Handover: AI-Powered Automatic Block Planning (GIGO-SIH 2026)

## 📋 Project Overview
The **AI-Powered Automatic Block Planning** system is a professional-grade spatio-temporal optimizer for railway maintenance. It replaces manual, error-prone block scheduling with an automated engine that ensures physical safety clearances (500m) and optimizes for criticality and corridor availability.

## 🏗️ Complete Technical Scope

### 1. The Agentic Pipeline (Intelligence Layer)
The system is architected as a decoupled pipeline of specialized agents:

| Agent | Primary Responsibility | Key Implementation Detail |
| :--- | :--- | :--- |
| **IngestionAgent** | Data Normalization | Validates heterogeneous source data (TMS, SMMS, TDMS, COA) via Pydantic models. |
| **ScoringAgent** | Criticality Ranking | Implements AHP weighted formula: $(0.5 \cdot \text{Sev}) + (0.3 \cdot \text{Overdue}) + (0.2 \cdot \text{DelayCost})$. |
| **SolverAgent** | Global Optimization | Uses Google OR-Tools CP-SAT to maximize criticality while enforcing spatial safety. |
| **HeuristicAgent** | Real-time Feedback | Greedy descent algorithm providing $<500\text{ms}$ updates for UI block-drags. |
| **HermesAgent** | Autonomous Oversight | Monitors system health; triggers re-optimization if unscheduled task rate $> 20\%$. |

### 2. Core Mathematical & Spatial Logic
- **Spatio-Temporal Packing**: Maps tracks as 1D coordinates (Chainage) and time as a linear axis.
- **Physical Safety Buffer**: Enforces a strict $\text{distance} \ge 0.5\text{km}$ between overlapping maintenance blocks to prevent machinery conflicts.
- **Stochastic Freight Guard**: Forbids blocks $> 120\text{min}$ in windows where $Prob(\text{Freight}) > 0.4$ to maintain network resilience.
- **Priority Boosts**:
  - **S&T Boost**: $1.5\text{x}$ multiplier for Signals & Telecommunications tasks.
  - **Power Block Premium**: Flat $+5.0$ point boost for tasks requiring power shutdowns.

### 3. User Interface & Visualization
- **Railway String Diagram**: A high-fidelity D3.js time-distance graph.
  - **X-Axis**: Time (00:00 to 24:00).
  - **Y-Axis**: Track Chainage (KM).
  - **Color Coding**: Red (Engineering), Blue (TRD), Green (S&T).
- **Control Dashboard**: Integrated task list, window management, and real-time "Auto-Fix" triggers.

### 4. Infrastructure & API
- **Backend**: FastAPI (Async) with a cached `SystemState` for performance.
- **Persistence**: PostgreSQL with **PostGIS** for spatial indexing.
- **Caching**: Redis for solver state and session management.
- **Containerization**: Docker Compose orchestration for one-click deployment.

## 📖 Documentation Suite (Diataxis Framework)
The project is fully documented in the `/docs` directory, categorized by user intent:

| Quadrant | Documents | Purpose |
| :--- | :--- | :--- |
| **Tutorials** | `tutorial-getting-started.md`, `tutorial-string-diagram.md` | Learning-oriented; zero-to-one guides. |
| **How-to Guides** | `how-to-deploy.md`, `how-to-api.md`, `how-to-use-hermes.md` | Task-oriented; achieving specific goals. |
| **Reference** | `reference-solver.md`, `reference-scoring.md`, `reference-hermes.md`, `reference-api.md` | Information-oriented; technical specifications. |
| **Explanations** | `explanation-spatio-temporal.md`, `explanation-ahp-prioritization.md`, `explanation-string-diagram.md`, `explanation-agentic-pipeline.md` | Understanding-oriented; design rationale. |

## 🏁 Final Milestone Status
- [x] **Phase 0: Repo Setup** $\rightarrow$ Complete
- [x] **Phase 1: Mock Data Layer** $\rightarrow$ Complete
- [x] **Phase 2: Scoring Engine** $\rightarrow$ Complete
- [x] **Phase 3: Constraint Solver** $\rightarrow$ Complete
- [x] **Phase 4: FastAPI Backend** $\rightarrow$ Complete
- [x] **Phase 5: React Frontend** $\rightarrow$ Complete
- [x] **Phase 6: Integration & Docker** $\rightarrow$ Complete
- [x] **Phase 7: PostGIS Spatial Integration** $\rightarrow$ Complete
- [x] **Phase 8: Demo Polish** $\rightarrow$ Complete
- [x] **Hermes Agent Integration** $\rightarrow$ Complete
- [x] **Diataxis Documentation Suite** $\rightarrow$ Complete

## 🚀 Deployment & Operation
1. **Launch**: `docker-compose up --build -d`.
2. **Access**: Dashboard at `http://localhost`.
3. **Demo**: Use `POST /api/demo/load` to inject integrated block scenarios.
