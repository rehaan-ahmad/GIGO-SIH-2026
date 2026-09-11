from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging
import time
from agents.ingestion_agent import ingest
from agents.scoring_agent import score_tasks
from agents.solver_agent import solve
from agents.heuristic_agent import solve_heuristic as heuristic_reoptimize
from agents.hermes_agent import hermes
from db import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Railway Block Planner API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- State Cache to prevent redundant I/O ---
class SystemState:
    def __init__(self):
        self.tasks = []
        self.windows = []
        self.scored_tasks = []
        self.last_updated = 0
        self.cache_ttl = 60  # 60 seconds

    def refresh(self):
        now = time.time()
        if now - self.last_updated > self.cache_ttl:
            logger.info("Refreshing system state from data source...")
            data = ingest()
            self.tasks = data["tasks"]
            self.windows = data["corridor_windows"]
            self.scored_tasks = score_tasks(self.tasks)
            self.last_updated = now
        return self.tasks, self.windows, self.scored_tasks

state = SystemState()

# --- Pydantic Models ---

class OptimizeRequest(BaseModel):
    horizon: str = "weekly"
    solver_mode: str = "exact"

class ReoptimizeRequest(BaseModel):
    locked_tasks: List[str] = []
    forced_window: Dict[str, Any]
    dragged_task_id: str

class TaskResponse(BaseModel):
    task_id: str
    dept: str
    type: str
    criticality_score: float
    duration_mins: int
    chainage_start_km: float
    chainage_end_km: float

class ScheduleResponse(BaseModel):
    status: str
    schedule: List[Dict[str, Any]]
    unscheduled_tasks: List[Dict[str, Any]]
    solver_status: str

@app.on_event("startup")
async def startup_event():
    init_db()
    logger.info("Database initialized and API starting up.")

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "Railway Block Planner API is online"}

@app.get("/api/agent/status")
async def agent_status():
    """Hermes Agent: Automatic retrieval of system state and health metrics."""
    return hermes.retrieve_system_summary()

@app.post("/api/agent/auto-fix")
async def agent_auto_fix(req: OptimizeRequest):
    """Hermes Agent: Autonomous analysis and re-optimization of the block plan."""
    return hermes.analyze_and_auto_optimize(horizon=req.horizon)

@app.post("/api/demo/load")
async def load_demo_scenario():
    return {"status": "success", "message": "Demo scenario loaded: Integrated blocks for Engineering+TRD+S&T"}

@app.get("/api/tasks", response_model=List[TaskResponse])
async def get_tasks():
    _, _, scored_tasks = state.refresh()
    return [
        TaskResponse(
            task_id=t["task_id"],
            dept=t["dept"],
            type=t["type"],
            criticality_score=t["criticality_score"],
            duration_mins=t["duration_mins"],
            chainage_start_km=t["chainage_start_km"],
            chainage_end_km=t["chainage_end_km"]
        ) for t in scored_tasks
    ]

@app.get("/api/windows")
async def get_windows():
    _, windows, _ = state.refresh()
    return windows

@app.post("/api/optimize-blocks", response_model=ScheduleResponse)
async def optimize_blocks(req: OptimizeRequest):
    logger.info(f"Optimizing blocks: horizon={req.horizon}, mode={req.solver_mode}")

    _, windows, scored_tasks = state.refresh()
    result = solve(scored_tasks, windows, mode=req.solver_mode, horizon=req.horizon)

    return ScheduleResponse(
        status="success",
        schedule=result["schedule"],
        unscheduled_tasks=result["unscheduled_tasks"],
        solver_status=result["solver_status"]
    )

@app.post("/api/reoptimize")
async def reoptimize(req: ReoptimizeRequest):
    logger.info(f"Real-time re-optimization for task {req.dragged_task_id}")

    _, windows, scored_tasks = state.refresh()
    base_result = solve(scored_tasks, windows, mode="heuristic")

    result = heuristic_reoptimize(
        full_schedule=base_result["schedule"],
        locked_tasks=req.locked_tasks,
        forced_window=req.forced_window,
        dragged_task_id=req.dragged_task_id,
        scored_tasks=scored_tasks,
        corridor_windows=windows
    )

    return result

@app.get("/api/schedule/{date}")
async def get_schedule_by_date(date: str):
    return {"date": date, "schedule": [], "message": "Persistence layer integration pending."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
