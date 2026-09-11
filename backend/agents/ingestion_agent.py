import json
import logging
from typing import List, Dict, Any
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskModel(BaseModel):
    task_id: str
    dept: str
    type: str
    chainage_start_km: float
    chainage_end_km: float
    duration_mins: int
    severity: int
    days_overdue: int
    needs_power_block: bool
    machinery_type: str

class WindowModel(BaseModel):
    window_id: str
    date: str
    start_time: str
    end_time: str
    freight_probability: float
    passenger_train_slots: List[str]

def ingest() -> Dict[str, Any]:
    """
    Polls and normalizes data from mock JSON.
    """
    try:
        with open('data/mocks.json', 'r') as f:
            raw = json.load(f)

        tasks = []
        rejected_records = 0

        for t in raw.get("tasks", []):
            try:
                # Validation via Pydantic
                task_obj = TaskModel(**t)
                tasks.append(task_obj.model_dump())
            except Exception as e:
                logger.warning(f"Rejecting record {t.get('task_id', 'unknown')}: {e}")
                rejected_records += 1

        windows = []
        for w in raw.get("corridor_availability", []):
            try:
                window_obj = WindowModel(**w)
                # Apply stochastic freight buffer: probability > 0.4 -> buffer_mins = 120
                window_data = window_obj.model_dump()
                if window_data["freight_probability"] > 0.4:
                    window_data["buffer_mins"] = 120
                else:
                    window_data["buffer_mins"] = 0
                windows.append(window_data)
            except Exception as e:
                logger.warning(f"Rejecting window {w.get('window_id', 'unknown')}: {e}")

        return {
            "tasks": tasks,
            "corridor_windows": windows,
            "ingestion_timestamp": "2026-09-11T12:00:00Z", # Mock timestamp
            "rejected_records": rejected_records
        }
    except FileNotFoundError:
        logger.error("mocks.json not found!")
        return {"tasks": [], "corridor_windows": [], "rejected_records": 0}
