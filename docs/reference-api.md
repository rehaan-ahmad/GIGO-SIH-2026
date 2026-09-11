# API Reference

The Railway Block Planner provides a RESTful API built with FastAPI. All endpoints are prefixed with `/api`.

## Base Configuration
- **Base URL**: `http://localhost:8000` (Docker)
- **Content-Type**: `application/json`
- **CORS**: Enabled for all origins (`*`).

---

## System & Agent Endpoints

### `GET /api/health`
Returns the current health status of the API.

**Response:**
```json
{ "status": "healthy", "message": "Railway Block Planner API is online" }
```

### `GET /api/agent/status`
Triggers the **Hermes Agent** to perform an automatic retrieval of system health metrics.

**Response:**
```json
{
  "agent": "Hermes",
  "status": "ONLINE",
  "metrics": {
    "total_tasks": 50,
    "critical_tasks": 10,
    "total_capacity_mins": 1440,
    "criticality_ratio": 0.2
  },
  "summary": "..."
}
```

### `POST /api/agent/auto-fix`
Triggers the **Hermes Agent** to autonomously analyze the schedule and re-optimize if a bottleneck is detected.

**Request Body:**
```json
{ "horizon": "weekly" }
```

**Response:**
Returns the action taken (`AUTO_OPTIMIZE` or `MONITOR`) and the resulting schedule.

---

## Block Planning Endpoints

### `GET /api/tasks`
Retrieves all maintenance tasks, including their calculated AHP criticality scores.

**Response:**
A list of `TaskResponse` objects:
- `task_id` (`str`)
- `dept` (`str`)
- `type` (`str`)
- `criticality_score` (`float`)
- `duration_mins` (`int`)
- `chainage_start_km` (`float`)
- `chainage_end_km` (`float`)

### `GET /api/windows`
Retrieves the available corridor windows for the current period.

**Response:**
A list of window objects containing `window_id`, `start_time`, `end_time`, and `freight_probability`.

### `POST /api/optimize-blocks`
Invokes the **Solver Agent** to generate an optimal block plan.

**Request Body:**
```json
{
  "horizon": "weekly",
  "solver_mode": "exact"
}
```

**Response:**
- `status`: `"success"`
- `schedule`: List of assigned blocks.
- `unscheduled_tasks`: List of tasks that failed constraints.
- `solver_status`: `"OPTIMAL"`, `"FEASIBLE"`, or `"INFEASIBLE"`.

### `POST /api/reoptimize`
Invokes the **Heuristic Agent** for real-time re-optimization during UI interactions.

**Request Body:**
```json
{
  "locked_tasks": ["T1", "T2"],
  "forced_window": { "window_id": "W1", "start_time": "02:00" },
  "dragged_task_id": "T3"
}
```

**Response:**
A refined schedule based on the greedy heuristic.

## Related
- For deployment details, see [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md).
- For an explanation of the solver logic, see [`docs/reference-solver.md`](docs/reference-solver.md).
