# Hermes Agent Reference

**Hermes** is the autonomous orchestrator for the Railway Block Planner. It monitors system health, retrieves state, and triggers re-optimization when bottlenecks are detected.

## Core Capabilities

Hermes operates on two primary modes: **Automatic Retrieval** and **Automated Action**.

### 1. Automatic Retrieval
Hermes gathers a high-level summary of the current system state to provide a "health check" for the railway corridor.

**Metrics Tracked:**
- **Total Tasks**: Number of tasks in the pipeline.
- **Criticality Ratio**: Percentage of tasks with a score $\ge 80$.
- **Total Capacity**: Total available minutes across all configured corridor windows.

### 2. Automated Action (Auto-Fix)
Hermes analyzes the schedule and triggers a re-optimization if the "failure rate" (unscheduled tasks / total tasks) exceeds a predefined threshold.

**Trigger Threshold:**
- **Failure Rate > 20%**: If more than 20% of tasks remain unscheduled, Hermes triggers the `solve` agent autonomously.

## API Interface

The Hermes agent is implemented in `backend/agents/hermes_agent.py`.

### `retrieve_system_summary()`

**Returns:**
A dictionary containing system status and health metrics:
```json
{
  "agent": "Hermes",
  "status": "ONLINE",
  "metrics": {
    "total_tasks": 45,
    "critical_tasks": 12,
    "total_capacity_mins": 1440,
    "criticality_ratio": 0.27
  },
  "summary": "System is monitoring 45 tasks with 12 high-priority items."
}
```

### `analyze_and_auto_optimize(horizon="weekly")`

**Parameters:**
- `horizon` (`str`): The scheduling horizon (`"weekly"`, `"monthly"`).

**Returns:**
A dictionary indicating the action taken:
- **`AUTO_OPTIMIZE`**: Triggered when the failure rate is too high.
- **`MONITOR`**: No action taken as health is within parameters.

## Related
- For the orchestration design, see [`docs/explanation-agentic-pipeline.md`](docs/explanation-agentic-pipeline.md).
- For API endpoint usage, see [`docs/reference-api.md`](docs/reference-api.md).
