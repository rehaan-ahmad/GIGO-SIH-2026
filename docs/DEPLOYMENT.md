# Deployment Guide: Railway Block Planner

This guide provides detailed instructions for deploying the AI-Powered Automatic Block Planning system.

## 🐳 Docker Deployment (Recommended)

The system is designed to be deployed as a containerized stack using Docker Compose.

### 1. Environment Configuration
Create a `.env` file in the root directory:
```env
DB_URL=postgresql://postgres:postgres@db:5432/postgres
REDIS_URL=redis://redis:6379/0
CORS_ORIGIN=http://localhost:5173
```

### 2. Launching the Stack
Run the following command to build and start all services:
```bash
docker-compose up --build -d
```

### 3. Service Architecture
- **`backend`**: FastAPI application. Exposes port `8000`.
- **`frontend`**: Vite + React app served via Nginx. Exposes port `5173`.
- **`db`**: PostGIS enabled PostgreSQL database for spatial queries.
- **`redis`**: In-memory store for Celery task queuing and state caching.

### 4. Verifying Installation
Check the health of the API:
```bash
curl http://localhost:8000/api/health
```
Expected response: `{"status":"healthy","message":"..."}`

## 💻 Local Development Setup

If you prefer running the services natively:

### Backend
1. Create a virtual environment: `python -m venv venv && source venv/bin/activate`
2. Install dependencies: `pip install -r backend/requirements.txt`
3. Run the server: `export PYTHONPATH=. && uvicorn backend.main:app --reload --port 8000`

### Frontend
1. Navigate to the frontend folder: `cd frontend`
2. Install dependencies: `npm install`
3. Start the dev server: `npm run dev`

## 🛠 Troubleshooting

### Database Connection Issues
If the backend cannot connect to the DB, ensure the `db` container is fully healthy. PostGIS initialization can take a few seconds on the first boot.

### CORS Errors
If the frontend cannot reach the API, verify that `CORS_ORIGIN` in the `.env` file matches the URL in your browser.

### Solver Timeouts
For very large task sets, the CP-SAT solver might hit the 10s timeout. You can increase this in `backend/agents/solver_agent.py` by modifying `solver.parameters.max_time_in_seconds`.
