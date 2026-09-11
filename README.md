# AI-Powered Automatic Block Planning (GIGO-SIH 2026)

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/rehaan-ahmad/GIGO-SIH-2026)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Stack](https://img.shields.io/badge/stack-FastAPI%20%7C%20React%20%7C%20OR--Tools-orange)]()

## 🚂 Project Overview
The **AI-Powered Automatic Block Planning** system is a professional-grade spatio-temporal optimizer designed for railway maintenance. It replaces manual, error-prone block scheduling with an automated engine that ensures safety, maximizes corridor utilization, and prioritizes critical repairs.

### The Core Problem
Railway maintenance requires "blocks" (portions of the track closed to traffic). Traditional scheduling often ignores the **spatial dimension**, leading to conflicts where multiple heavy machines are too close for safety. This system treats the railway as a 4D space (X-axis: Chainage, Y-axis: Time, Z-axis: Dept/Layer).

## ✨ Key Features
- **Spatio-Temporal Solver**: Uses Google OR-Tools CP-SAT to enforce a strict **500m physical clearance** between machinery.
- **AHP Criticality Scoring**: Implements an Analytic Hierarchy Process to rank tasks based on severity, overdue status, and train delay impact.
- **Railway String Diagrams**: A custom D3.js visualization providing a high-fidelity time-distance graph, the gold standard for railway controllers.
- **Real-time Heuristic**: A greedy re-optimizer that provides $<500\text{ms}$ feedback when blocks are dragged in the UI.
- **Stochastic Freight Guard**: Automatically buffers windows with high freight probability to prevent cascading delays.

## 🛠 Tech Stack
| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **API** | `FastAPI` | High-performance async REST interface |
| **Solver** | `OR-Tools CP-SAT` | Constraint programming for optimal block assignment |
| **Intelligence** | `XGBoost` | (Optional) Predictive delay cost modeling |
| **Database** | `PostgreSQL` + `PostGIS` | Spatial storage and proximity queries |
| **Cache/Queue** | `Redis` + `Celery` | Background solver execution and state caching |
| **Frontend** | `React 19` + `D3.js` | Professional String Diagram UI |
| **Styling** | `Tailwind CSS 4` | Dark-mode control room aesthetic |
| **DevOps** | `Docker` + `Compose` | One-click environment orchestration |

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local dev)
- Node.js 20+ (for local dev)

### Installation
1. **Clone the Repo**
   ```bash
   git clone git@github.com:rehaan-ahmad/GIGO-SIH-2026.git
   cd GIGO
   ```

2. **Run via Docker (Recommended)**
   ```bash
   docker-compose up --build
   ```

3. **Access the App**
   - 🌐 **Frontend**: `http://localhost` (Docker) or `http://localhost:5173` (Local Dev)
   - 🔌 **Backend API**: `http://localhost:8000`
   - 📖 **API Docs**: `http://localhost:8000/docs` (Swagger UI)

## 📐 System Architecture
The system operates as a pipeline of specialized agents:
`IngestionAgent` $\rightarrow$ `ScoringAgent` $\rightarrow$ `SolverAgent` $\rightarrow$ `API` $\rightarrow$ `UI`

For a deep dive into the mathematical constraints and data flow, see [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## 📄 Documentation

The project follows the **Diataxis framework** for comprehensive coverage:

### 🎓 Learning & Guidance
- **Getting Started**: [`docs/tutorial-getting-started.md`](docs/tutorial-getting-started.md) — First steps to a working plan.
- **String Diagram Guide**: [`docs/tutorial-string-diagram.md`](docs/tutorial-string-diagram.md) — Mastering the visualization.
- **Deployment Guide**: [`docs/how-to-deploy.md`](docs/how-to-deploy.md) — Setup and infrastructure.
- **API Usage**: [`docs/how-to-api.md`](docs/how-to-api.md) — Programmatic interaction.
- **Hermes Orchestrator**: [`docs/how-to-use-hermes.md`](docs/how-to-use-hermes.md) — Autonomous health management.

### 📚 Technical Reference
- **Spatio-Temporal Solver**: [`docs/reference-solver.md`](docs/reference-solver.md) — Logic and constraints.
- **AHP Scoring**: [`docs/reference-scoring.md`](docs/reference-scoring.md) — Priority calculations.
- **Hermes Agent**: [`docs/reference-hermes.md`](docs/reference-hermes.md) — System metrics.
- **REST API**: [`docs/reference-api.md`](docs/reference-api.md) — Endpoint specifications.

### 🧠 Deep Dives & Explanations
- **Spatio-Temporal Packing**: [`docs/explanation-spatio-temporal.md`](docs/explanation-spatio-temporal.md) — Why we use 4D space.
- **Prioritization Logic**: [`docs/explanation-ahp-prioritization.md`](docs/explanation-ahp-prioritization.md) — Design of the scoring engine.
- **String Diagram Design**: [`docs/explanation-string-diagram.md`](docs/explanation-string-diagram.md) — Rendering and UX.
- **Agentic Architecture**: [`docs/explanation-agentic-pipeline.md`](docs/explanation-agentic-pipeline.md) — The pipeline philosophy.

### 🛠 Legacy & High-Level
- **Technical Architecture**: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- **Implementation Handover**: [`handover.md`](handover.md)

