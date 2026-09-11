"""
Heuristic Agent Module
======================

This module implements the real-time re-optimization logic.
Unlike the solver agent, which uses CP-SAT for global optimality,
the Heuristic Agent uses a greedy descent algorithm to provide
sub-500ms responses for interactive UI changes.
"""
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def solve_heuristic(full_schedule: List[Dict[str, Any]],
                    locked_tasks: List[str],
                    forced_window: Dict[str, Any],
                    dragged_task_id: str,
                    scored_tasks: List[Dict[str, Any]],
                    corridor_windows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Performs a real-time greedy re-optimization of the block plan.

    This heuristic is triggered during UI interactions (e.g., dragging a block)
    to provide immediate feedback (<500ms) without invoking the full CP-SAT solver.
    """
    # Section 1: Reinitialize window capacities based on availability
    window_capacities = {}
    for w in corridor_windows:
        start_h, start_m = map(int, w["start_time"].split(":"))
        end_h, end_m = map(int, w["end_time"].split(":"))
        window_capacities[w["window_id"]] = (end_h * 60 + end_m) - (start_h * 60 + start_m)

    # Section 2: Account for locked tasks that cannot be moved
    for task in full_schedule:
        if task["task_id"] in locked_tasks:
            task_detail = next((t for t in scored_tasks if t["task_id"] == task["task_id"]), None)
            if task_detail:
                window_capacities[task["window_id"]] -= task_detail["duration_mins"]

    # Section 3: Prioritize the dragged task in its new forced window
    new_schedule = []
    dragged_task_detail = next((t for t in scored_tasks if t["task_id"] == dragged_task_id), None)
    if dragged_task_detail:
        w_id = forced_window["window_id"]
        if window_capacities[w_id] >= dragged_task_detail["duration_mins"]:
            window_capacities[w_id] -= dragged_task_detail["duration_mins"]
            new_schedule.append({
                "task_id": dragged_task_id,
                "window_id": w_id,
                "dept": dragged_task_detail["dept"],
                "chainage_start_km": dragged_task_detail["chainage_start_km"],
                "chainage_end_km": dragged_task_detail["chainage_end_km"],
                "scheduled_start": forced_window["start_time"],
                "scheduled_end": "calculated",
                "is_integrated_block": False,
                "co_scheduled_with": []
            })
        else:
            logger.warning(f"Forced window {w_id} has no capacity for {dragged_task_id}")

    # Section 4: Greedy assignment for all remaining tasks sorted by criticality
    for t in scored_tasks:
        if t["task_id"] == dragged_task_id or t["task_id"] in locked_tasks:
            continue

        assigned = False
        for w in corridor_windows:
            w_id = w["window_id"]
            if window_capacities[w_id] >= t["duration_mins"]:
                if not (w["freight_probability"] > 0.4 and t["duration_mins"] > 120):
                    window_capacities[w_id] -= t["duration_mins"]
                    new_schedule.append({
                        "task_id": t["task_id"],
                        "window_id": w_id,
                        "dept": t["dept"],
                        "chainage_start_km": t["chainage_start_km"],
                        "chainage_end_km": t["chainage_end_km"],
                        "scheduled_start": w["start_time"],
                        "scheduled_end": "calculated",
                        "is_integrated_block": False,
                        "co_scheduled_with": []
                    })
                    assigned = True
                    break

    return {
        "schedule": new_schedule,
        "solver_status": "FEASIBLE",
        "reoptimize_mode": "heuristic"
    }
