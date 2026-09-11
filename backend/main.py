from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging
from agents.ingestion_agent import ingest
from agents.scoring_agent import score_tasks
from agents.solver_agent import solve
from agents.heuristic_agent import solve_heuristic as heuristic_reoptimize

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Railway Block Planner API", version="1.0.0")

# CORS setup for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models ---

class OptimizeRequest(BaseModel):
    horizon: str = "weekly"  # "weekly" | "monthly"
    solver_mode: str = "exact" # "exact" | "heuristic"

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

# --- Endpoints ---

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "Railway Block Planner API is online"}

@app.get("/api/tasks", response_model=List[TaskResponse])
async def get_tasks():
    """Returns all tasks with their calculated criticality scores."""
    data = ingest()
    scored_tasks = score_tasks(data["tasks"])
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
    """Returns corridor availability windows."""
    data = ingest()
    return data["corridor_windows"]

@app.post("/api/optimize-blocks", response_model=ScheduleResponse)
async def optimize_blocks(req: OptimizeRequest):
    """
    Full pipeline: Ingest -> Score -> Solve.
    """
    logger.info(f"Optimizing blocks: horizon={req.horizon}, mode={req.solver_mode}")

    # 1. Ingest
    data = ingest()

    # 2. Score
    scored_tasks = score_tasks(data["tasks"])

    # 3. Solve
    result = solve(scored_tasks, data["corridor_windows"], mode=req.solver_mode, horizon=req.horizon)

    return ScheduleResponse(
        status="success",
        schedule=result["schedule"],
        unscheduled_tasks=result["unscheduled_tasks"],
        solver_status=result["solver_status"]
    )

@app.post("/api/reoptimize")
async def reoptimize(req: ReoptimizeRequest):
    """
    Real-time heuristic re-optimization triggered by UI drag-and-drop.
    """
    logger.info(f"Real-time re-optimization for task {req.dragged_task_id}")

    # In a real app, we'd fetch the current state from DB
    data = ingest()
    scored_tasks = score_tasks(data["tasks"])

    # We need the current full schedule to identify what is locked
    # For now, we'll run a quick solve to get a base schedule
    base_result = solve(scored_tasks, data["corridor_windows"], mode="heuristic")

    result = heuristic_reoptimize(
        full_schedule=base_result["schedule"],
        locked_tasks=req.locked_tasks,
        forced_window=req.forced_window,
        dragged_task_id=req.dragged_task_id,
        scored_tasks=scored_tasks,
        corridor_windows=data["corridor_windows"]
    )

    return result

@app.get("/api/schedule/{date}")
async def get_schedule_by_date(date: str):
    """Fetch stored daily block plan. (Mocked for now)"""
    return {"date": date, "schedule": [], "message": "Stored schedules coming soon with DB integration"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
