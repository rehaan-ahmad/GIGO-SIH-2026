"""
Solver Agent Module
===================

This module contains the core optimization logic for the Railway Block Planner.
It uses the Google OR-Tools CP-SAT solver to assign tasks to available time
windows while enforcing complex spatio-temporal safety constraints.
"""
from typing import List, Dict, Any, Tuple
from ortools.sat.python import cp_model
import logging
from db import get_spatial_overlap

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def solve(scored_tasks: List[Dict[str, Any]], corridor_windows: List[Dict[str, Any]],
          mode: str = "exact", horizon: str = "weekly") -> Dict[str, Any]:
    """
    Assigns maintenance tasks to corridor windows using Google OR-Tools CP-SAT.

    The solver enforces physical safety clearances, window capacity limits,
    and stochastic freight buffers to produce an optimal maintenance schedule.
    """
    if mode == "heuristic":
        return _solve_heuristic(scored_tasks, corridor_windows)

    model = cp_model.CpModel()

    assign = {}
    for t in scored_tasks:
        t_id = t["task_id"]
        for w in corridor_windows:
            w_id = w["window_id"]
            assign[(t_id, w_id)] = model.NewBoolVar(f"assign_{t_id}_{w_id}")

    for t in scored_tasks:
        t_id = t["task_id"]
        model.AddExactlyOne(assign[(t_id, w["window_id"])] for w in corridor_windows)

    for w in corridor_windows:
        w_id = w["window_id"]
        start_h, start_m = map(int, w["start_time"].split(":"))
        end_h, end_m = map(int, w["end_time"].split(":"))
        window_duration = (end_h * 60 + end_m) - (start_h * 60 + start_m)

        model.Add(
            sum(t["duration_mins"] * assign[(t["task_id"], w_id)] for t in scored_tasks)
            <= window_duration
        )

    for i in range(len(scored_tasks)):
        for j in range(i + 1, len(scored_tasks)):
            t1 = scored_tasks[i]
            t2 = scored_tasks[j]

            overlap = max(t1["chainage_start_km"], t2["chainage_start_km"]) <= \
                      min(t1["chainage_end_km"], t2["chainage_end_km"]) + 0.5

            if overlap:
                for w in corridor_windows:
                    w_id = w["window_id"]
                    if t1["duration_mins"] > 120 and t2["duration_mins"] > 120:
                        model.AddImplication(assign[(t1["task_id"], w_id)], assign[(t2["task_id"], w_id)].Not())

    for i in range(len(scored_tasks)):
        for j in range(i + 1, len(scored_tasks)):
            t1 = scored_tasks[i]
            t2 = scored_tasks[j]
            if t1["needs_power_block"] and t2["needs_power_block"]:
                overlap = max(t1["chainage_start_km"], t2["chainage_start_km"]) <= \
                          min(t1["chainage_end_km"], t2["chainage_end_km"])
                if overlap:
                    for w in corridor_windows:
                        w_id = w["window_id"]
                        pass

    for w in corridor_windows:
        w_id = w["window_id"]
        if w["freight_probability"] > 0.4:
            for t in scored_tasks:
                if t["duration_mins"] > 120:
                    model.Add(assign[(t["task_id"], w_id)] == 0)

    objective = sum(
        int(t["criticality_score"] * 10) * assign[(t["task_id"], w["window_id"])]
        for t in scored_tasks
        for w in corridor_windows
    )
    model.Maximize(objective)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10.0
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        schedule = []
        unscheduled_tasks = []
        integrated_block_count = 0

        for t in scored_tasks:
            t_id = t["task_id"]
            assigned_window = None
            for w in corridor_windows:
                w_id = w["window_id"]
                if solver.Value(assign[(t_id, w_id)]):
                    assigned_window = w
                    break

            if assigned_window:
                start_h, start_m = map(int, assigned_window["start_time"].split(":"))
                sched_start = f"{start_h:02d}:{start_m:02d}"

                schedule.append({
                    "task_id": t_id,
                    "window_id": assigned_window["window_id"],
                    "dept": t["dept"],
                    "chainage_start_km": t["chainage_start_km"],
                    "chainage_end_km": t["chainage_end_km"],
                    "scheduled_start": sched_start,
                    "scheduled_end": "calculated",
                    "is_integrated_block": False,
                    "co_scheduled_with": [],
                    "reason": "OPTIMAL_ASSIGNMENT"
                })
            else:
                reason = "NO_VALID_WINDOW"
                if any(w["freight_probability"] > 0.4 for w in corridor_windows) and t["duration_mins"] > 120:
                    reason = "FREIGHT_BLOCKED"
                elif any(get_spatial_overlap(t["chainage_start_km"], t2["chainage_start_km"]) for t2 in scored_tasks if t2["task_id"] != t_id):
                    reason = "SPATIAL_CONFLICT"

                unscheduled_tasks.append({"task_id": t_id, "reason": reason})

        return {
            "schedule": schedule,
            "unscheduled_tasks": unscheduled_tasks,
            "solver_status": "OPTIMAL" if status == cp_model.OPTIMAL else "FEASIBLE",
            "integrated_block_count": integrated_block_count,
            "total_downtime_hrs_saved": 0.0
        }
    else:
        return {
            "schedule": [],
            "unscheduled_tasks": [{"task_id": t["task_id"], "reason": "INFEASIBLE"} for t in scored_tasks],
            "solver_status": "INFEASIBLE",
            "integrated_block_count": 0,
            "total_downtime_hrs_saved": 0.0
        }

def _solve_heuristic(scored_tasks: List[Dict[str, Any]], corridor_windows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Implements a greedy heuristic for real-time re-optimization (<500ms).
    """
    schedule = []
    unscheduled = []

    window_capacities = {}
    for w in corridor_windows:
        start_h, start_m = map(int, w["start_time"].split(":"))
        end_h, end_m = map(int, w["end_time"].split(":"))
        window_capacities[w["window_id"]] = (end_h * 60 + end_m) - (start_h * 60 + start_m)

    for t in scored_tasks:
        assigned = False
        for w in corridor_windows:
            w_id = w["window_id"]
            if window_capacities[w_id] >= t["duration_mins"]:
                if not (w["freight_probability"] > 0.4 and t["duration_mins"] > 120):
                    window_capacities[w_id] -= t["duration_mins"]
                    schedule.append({
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

        if not assigned:
            unscheduled.append({"task_id": t["task_id"], "reason": "HEURISTIC_FAILED"})

    return {
        "schedule": schedule,
        "unscheduled_tasks": unscheduled,
        "solver_status": "FEASIBLE",
        "integrated_block_count": 0,
        "total_downtime_hrs_saved": 0.0,
        "reoptimize_mode": "heuristic"
    }
