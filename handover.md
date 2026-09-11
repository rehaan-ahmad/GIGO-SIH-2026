# Project Handover: AI-Powered Automatic Block Planning (GIGO-SIH 2026)

## 📋 Project Overview
The **AI-Powered Automatic Block Planning** system is a professional spatio-temporal optimizer for railway maintenance. It replaces manual scheduling with a constraint-based engine that ensures physical safety clearances (500m) and optimizes for criticality and corridor availability.

## 🏗️ Technical Architecture

### 1. The Agentic Pipeline
The system is built as a pipeline of specialized agents:
- **IngestionAgent**: Normalizes data from TMS, SMMS, TDMS, and COA. Validates via Pydantic.
- **ScoringAgent**: Implements an AHP-weighted formula to rank tasks.
- **SolverAgent**: Uses Google OR-Tools CP-SAT for optimal assignment.
- **HeuristicAgent**: Provides $<500\text{ms}$ real-time re-optimization for UI interactions.
- **HermesAgent**: The autonomous orchestrator for system retrieval and health monitoring.

### 2. Key Mathematical Logic
- **Spatio-Temporal Packing**: Treats the track as a 1D coordinate and the window as a 1D time-axis.
- **Constraint Logic**: 
  - **Spatial Safety**: $\max(\text{start}_1, \text{start}_2) \le \min(\text{end}_1, \text{end}_2) + 0.5\text{km}$ is forbidden for heavy machinery.
  - **Temporal Capacity**: $\sum \text{durations} \le \text{WindowLength}$.
  - **Stochastic Guard**: Blocks duration $> 120\text{min}$ are forbidden in windows where $Prob(\text{Freight}) > 0.4$.
- **Criticality Formula**: $C = (0.5 \cdot \text{Sev}) + (0.3 \cdot \text{Overdue}) + (0.2 \cdot \text{DelayCost}) \times (\text{S\&T Boost})$.

### 3. Tech Stack
- **Backend**: FastAPI, OR-Tools CP-SAT, PostgreSQL+PostGIS, Redis.
- **Frontend**: React 19, D3.js (String Diagram), Tailwind CSS 4.
- **Infra**: Docker, Docker Compose.

## 📖 Documentation Suite
The project is fully documented in the `/docs` directory:
- **`README.md`**: Entry point and quick-start.
- **`ARCHITECTURE.md`**: Mathematical and logic specifications.
- **`API.md`**: REST interface and Agentic endpoints.
- **`DEPLOYMENT.md`**: Docker and local environment setup.
- **`USER_GUIDE.md`**: Operational guide for Railway Controllers.

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
- [x] **Hermes Agent Integration** $\rightarrow$ Completed
- [x] **Professional Documentation** $\rightarrow$ Completed

## 🚀 Deployment & Operation
1. Run `docker-compose up --build`.
2. Access Dashboard at `http://localhost:5173`.
3. Use `POST /api/demo/load` to showcase integrated block scenarios.
