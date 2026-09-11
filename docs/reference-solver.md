# Spatio-Temporal Block Solver Reference

The **Spatio-Temporal Block Solver** is the core optimization engine of the Railway Block Planner. It assigns maintenance tasks to available time windows while ensuring physical safety and operational efficiency.

## Core Logic

The solver uses the **Google OR-Tools CP-SAT** (Constraint Programming - Satisfiability) solver to find an optimal assignment of tasks to windows.

### Constraints

The solver enforces the following hard constraints:

| Constraint | Logic | Purpose |
| :--- | :--- | :--- |
| **Temporal Capacity** | $\sum \text{TaskDuration} \le \text{WindowDuration}$ | Prevents over-scheduling a time window. |
| **Spatial Safety** | $\max(S_1, S_2) \le \min(E_1, E_2) + 0.5\text{km}$ | Ensures a 500m safety buffer between overlapping blocks. |
| **Freight Guard** | $\text{Duration} > 120\text{min} \implies \text{Prob(Freight)} \le 0.4$ | Prevents long blocks in windows with high freight probability. |
| **Exact Assignment** | Each task is assigned to exactly one window. | Ensures all requested work is attempted. |

### Objective Function

The solver maximizes the total criticality score of all assigned tasks:

$$\text{Maximize} \sum_{i \in \text{Tasks}} \sum_{j \in \text{Windows}} (\text{Criticality}_i \times \text{Assign}_{i,j})$$

## API Interface

The solver is invoked via the `solve` function in `backend/agents/solver_agent.py`.

### `solve(scored_tasks, corridor_windows, mode="exact", horizon="weekly")`

**Parameters:**
- `scored_tasks` (`List[Dict]`): A list of tasks containing `task_id`, `duration_mins`, `chainage_start_km`, `chainage_end_km`, and `criticality_score`.
- `corridor_windows` (`List[Dict]`): A list of available windows containing `window_id`, `start_time`, `end_time`, and `freight_probability`.
- `mode` (`str`): 
  - `"exact"`: Uses CP-SAT for global optimality.
  - `"heuristic"`: Uses a greedy approach for real-time response.
- `horizon` (`str`): The scheduling timeframe (e.g., `"weekly"`, `"monthly"`).

**Returns:**
A dictionary containing:
- `schedule`: List of assigned tasks with `scheduled_start` and `window_id`.
- `unscheduled_tasks`: List of tasks that could not be placed, including the `reason` (e.g., `"SPATIAL_CONFLICT"`, `"FREIGHT_BLOCKED"`).
- `solver_status`: Status of the solve (`"OPTIMAL"`, `"FEASIBLE"`, or `"INFEASIBLE"`).

## Performance Characteristics

| Mode | Algorithm | Typical Latency | Optimality |
| :--- | :--- | :--- | :--- |
| **Exact** | CP-SAT | $1\text{s} - 10\text{s}$ | Global Optimum |
| **Heuristic** | Greedy Descent | $< 500\text{ms}$ | Local Optimum |

## Related
- For a deep dive into the mathematical reasoning, see [`docs/explanation-spatio-temporal.md`](docs/explanation-spatio-temporal.md).
- For usage in the API, see [`docs/reference-api.md`](docs/reference-api.md).
