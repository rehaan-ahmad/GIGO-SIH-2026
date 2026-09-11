# How to Interact with the Block Planner API

This guide provides practical examples for using the REST API to programmatically manage railway blocks.

## Prerequisites
- The backend server must be running (`http://localhost:8000`).
- A tool like `curl`, Postman, or Insomnia is recommended.

## Steps

### 1. Fetch the Current Task List
Before optimizing, retrieve the tasks and their current priority scores.

```bash
curl http://localhost:8000/api/tasks
```
**Expected Result:** A JSON list of tasks with their `criticality_score`.

### 2. Generate an Optimal Schedule
Run the CP-SAT solver to assign tasks to the best possible windows.

```bash
curl -X POST http://localhost:8000/api/optimize-blocks \
     -H "Content-Type: application/json" \
     -d '{"horizon": "weekly", "solver_mode": "exact"}'
```
**Expected Result:** A JSON response containing the `schedule` (assigned tasks) and `unscheduled_tasks` (those that failed constraints).

### 3. Perform a Real-time Re-optimization
Simulate a "block drag" by forcing a specific task into a new window and seeing how it affects the rest of the plan.

```bash
curl -X POST http://localhost:8000/api/reoptimize \
     -H "Content-Type: application/json" \
     -d '{
       "locked_tasks": ["T1", "T2"],
       "forced_window": { "window_id": "W1", "start_time": "04:00" },
       "dragged_task_id": "T3"
     }'
```
**Expected Result:** A new schedule where T3 is moved to W1, and other tasks are greedily shifted to accommodate the change.

## Verification
To verify that your API calls are working:
1. Call `/api/tasks` $\rightarrow$ Note a high-priority task ID.
2. Call `/api/optimize-blocks` $\rightarrow$ Check if that ID is in the `schedule`.
3. Check the **String Diagram** UI to see the blocks visually rendered.

## Troubleshooting

| Error | Cause | Fix |
| :--- | :--- | :--- |
| `422 Unprocessable Entity` | Incorrect JSON body format. | Verify your request matches the Pydantic models in `main.py`. |
| `Empty schedule` | Solver returned `INFEASIBLE`. | Reduce the number of tasks or increase the available windows. |
| `Connection Refused` | Backend is not running. | Run `docker-compose up` or start the FastAPI server. |
