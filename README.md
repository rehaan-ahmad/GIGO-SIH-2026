# AI-Powered Automatic Block Planning (GIGO-SIH 2026)

## Overview
The AI-Powered Automatic Block Planning system is a spatio-temporal optimizer designed to automate the allocation of railway maintenance blocks. Unlike simple schedulers, this system enforces physical safety clearances and optimizes for criticality and corridor availability.

## Key Features
- **Spatio-Temporal Optimization**: Ensures maintenance tasks do not overlap in time AND space (500m clearance).
- **Criticality Scoring**: Uses an AHP-weighted formula (and optional XGBoost) to prioritize urgent repairs.
- **String Diagram UI**: High-fidelity time-distance graphs for railway controllers.
- **Real-time Re-optimization**: Greedy heuristic for immediate feedback during UI drag-and-drop.

## Tech Stack
- **Backend**: FastAPI, OR-Tools CP-SAT, XGBoost, PostgreSQL+PostGIS, Redis.
- **Frontend**: React, D3.js, Tailwind CSS.
- **Infrastructure**: Docker, Docker Compose.

## Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 20+

### Installation & Run
1. Clone the repository:
   ```bash
   git clone git@github.com:rehaan-ahmad/GIGO-SIH-2026.git
   cd GIGO
   ```
2. Start the system using Docker:
   ```bash
   docker-compose up --build
   ```
3. Access the frontend at `http://localhost:5173` and backend at `http://localhost:8000`.
