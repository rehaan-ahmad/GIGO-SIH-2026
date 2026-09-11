# API Reference: Railway Block Planner

All endpoints are prefixed with `/api`. Base URL: `http://localhost:8000/api`

## 🛠 General
### Health Check
`GET /health`
- **Description**: Liveness check for the backend.
- **Response**: `{ "status": "healthy", "message": "..." }`

---

## 📋 Task & Window Management

### Fetch Ranked Tasks
`GET /tasks`
- **Description**: Returns all current maintenance tasks sorted by their AHP criticality score.
- **Response**: `List[TaskResponse]`
  - `task_id`: Unique identifier (e.g., "TMS-8092")
  - `dept`: Department (Engineering/TRD/S&T)
  - `criticality_score`: Normalized 0-100 score
  - `duration_mins`: Required window length

### Fetch Corridor Availability
`GET /windows`
- **Description**: Returns available time windows for the current horizon.
- **Response**: `List[WindowModel]`
  - `window_id`: Unique ID
  - `date`: ISO date
  - `start_time`: "HH:mm"
  - `end_time`: "HH:mm"
  - `freight_probability`: 0.0 to 1.0

---

## 🚀 Optimization Engine

### Generate Optimal Plan
`POST /optimize-blocks`
- **Description**: Runs the full Ingest $\rightarrow$ Score $\rightarrow$ Solve pipeline.
- **Request Body**:
  ```json
  {
    "horizon": "weekly", // "weekly" | "monthly"
    "solver_mode": "exact" // "exact" | "heuristic"
  }
  ```
- **Response**: `ScheduleResponse`
  - `status`: "success" | "error"
  - `schedule`: List of assigned blocks with `scheduled_start` and `window_id`.
  - `unscheduled_tasks`: Tasks that couldn't fit, with reasons (`NO_VALID_WINDOW`, `SPATIAL_CONFLICT`, `FREIGHT_BLOCKED`).
  - `solver_status`: "OPTIMAL" | "FEASIBLE" | "INFEASIBLE"

### Real-time Re-optimization
`POST /reoptimize`
- **Description**: Fast heuristic re-run for UI interactions (Drag-and-Drop).
- **Request Body**:
  ```json
  {
    "locked_tasks": ["TMS-101", "TRD-202"],
    "forced_window": { "window_id": "WIN-001", "start_time": "02:00", ... },
    "dragged_task_id": "SMMS-303"
  }
  ```
- **Response**: Updated `Schedule` object.

---

## 🧪 Demo Tools

### Load Demo Scenario
`POST /demo/load`
- **Description**: Seeds the system with a high-impact scenario showing integrated multi-dept blocks.
- **Response**: `{ "status": "success", "message": "..." }`
