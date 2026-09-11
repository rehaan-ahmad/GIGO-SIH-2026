# Getting Started with Railway Block Planning

Welcome to the AI-Powered Block Planner. In this tutorial, you will go from a blank state to your first optimized maintenance schedule.

## What you'll build
You will deploy the system, load a demo scenario, and use the AI solver to resolve a complex set of maintenance conflicts.

## What you'll need
- **Docker & Docker Compose** installed.
- A web browser.

---

## Step 1: Launch the Environment
First, let's get the system online. Open your terminal and run:

```bash
git clone git@github.com:rehaan-ahmad/GIGO-SIH-2026.git
cd GIGO
docker-compose up --build -d
```

**What happened?** Docker just started four containers: the PostgreSQL database (with PostGIS), a Redis cache, the FastAPI backend, and the React frontend.

## Step 2: Load the Demo Scenario
The system starts with a clean state. Let's load a set of pre-defined maintenance tasks including Engineering, TRD, and S&T work.

Open your browser and visit:
`http://localhost:8000/api/demo/load`

**Expected Result:** You should see a success message: `"Demo scenario loaded: Integrated blocks for Engineering+TRD+S&T"`.

## Step 3: Run Your First Optimization
Now, let's let the AI solve the puzzle. 

1. Open the Dashboard at `http://localhost`.
2. Click the **"Optimize Blocks"** button.
3. Wait a few seconds for the CP-SAT solver to process the spatio-temporal constraints.

**What happened?** The `SolverAgent` analyzed every task, checked for 500m safety buffers, and packed the tasks into the available time windows to maximize criticality.

## Step 4: Analyze the String Diagram
Look at the **String Diagram** (the time-distance graph).
- **Blocks**: Notice how the colored rectangles are spread out.
- **Safety**: Check two blocks at the same time; they are either in different locations or separated by at least 500m.
- **Priorities**: Notice that the "Critical" tasks (highlighted in the task list) were assigned windows first.

---

## What you built
You now have a fully functioning, AI-driven block planning system. You've successfully:
1. Orchestrated a multi-container environment.
2. Injected complex railway maintenance data.
3. Resolved spatial conflicts using constraint programming.

### Next Steps
- **Try dragging a block**: Move a block in the String Diagram to see the real-time heuristic re-optimizer in action.
- **Explore Hermes**: Visit `/api/agent/status` to see the autonomous health metrics.
- **Deep Dive**: Read [`docs/explanation-spatio-temporal.md`](docs/explanation-spatio-temporal.md) to understand the math behind the safety buffers.
