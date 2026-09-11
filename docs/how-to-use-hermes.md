# How to Use the Hermes Agent

The **Hermes Agent** allows you to monitor the health of your block plan and trigger autonomous fixes without manually running the solver.

## Prerequisites
- The backend API must be running.
- You should have some tasks and windows loaded in the system.

## Steps

### 1. Check System Health
To see how the corridor is performing, request a system summary from Hermes.

**Request:**
```bash
curl http://localhost:8000/api/agent/status
```

**What to look for:**
- **`criticality_ratio`**: If this is high ($> 0.4$), you have many urgent tasks that need windows.
- **`total_capacity_mins`**: Ensure you have enough total window time to accommodate your tasks.

### 2. Trigger an Autonomous Fix
If you notice that many tasks are unscheduled or the schedule is inefficient, you can ask Hermes to "auto-fix" the plan.

**Request:**
```bash
curl -X POST http://localhost:8000/api/agent/auto-fix \
     -H "Content-Type: application/json" \
     -d '{"horizon": "weekly"}'
```

### 3. Verify the Result
Hermes will return one of two actions:
- **`MONITOR`**: The system is healthy; no change was made.
- **`AUTO_OPTIMIZE`**: A bottleneck was detected, and Hermes has triggered the solver to create a new, more efficient plan.

## Verification
After an `AUTO_OPTIMIZE` action, refresh your **String Diagram** in the UI. You should see more tasks assigned to windows and a reduction in the "Unscheduled Tasks" list.

## Troubleshooting
If Hermes returns `MONITOR` but you still see many unscheduled tasks, it means the "Failure Rate" is below 20%. You can manually trigger the solver via `POST /api/optimize-blocks` to force a global optimum.
