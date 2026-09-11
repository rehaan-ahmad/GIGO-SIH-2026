# Mastering the String Diagram

The String Diagram is the heart of the Railway Block Planner. This tutorial teaches you how to interpret and manipulate the time-distance graph to manage corridor health.

## What you'll learn
You'll learn how to identify conflicts, use the "Drag-and-Drop" re-optimizer, and interpret the departmental color-coding.

## What you'll need
- The application running at `http://localhost`.
- A loaded demo scenario (`/api/demo/load`).

---

## Step 1: Reading the Axes
The String Diagram is not a map; it's a **Spatio-Temporal Graph**.

- **Horizontal (X-Axis)**: Time. Moving left to right is moving forward through the day (00:00 $\rightarrow$ 24:00).
- **Vertical (Y-Axis)**: Chainage. Moving top to bottom is moving along the track (e.g., KM 0 $\rightarrow$ KM 1000).

**Exercise**: Find a block. If it's at the top of the graph at 02:00, it's a task at the start of the track early in the morning.

## Step 2: Identifying Departmental Blocks
Different departments have different priorities and risks. We use a color-coded system:

- **Red Blocks**: Engineering (Heavy machinery, track work).
- **Blue Blocks**: TRD (Traction and Distribution - Power lines).
- **Green Blocks**: S&T (Signals and Telecommunications).

**Exercise**: Look for "Integrated Blocks"—areas where multiple colors are stacked vertically. This means multiple departments are working in the same window at different locations.

## Step 3: Resolving Conflicts with Manual Overrides
Sometimes the AI's "Optimal" plan doesn't fit a real-world constraint (e.g., a specific team is unavailable at 04:00).

1. Select a block on the diagram.
2. **Drag** the block to a different time or location.
3. Release the mouse.

**What happened?** The `HeuristicAgent` instantly recalculated the rest of the schedule. It "locked" your dragged block and shifted other tasks to ensure no 500m safety buffers were violated.

## Step 4: Verifying the "Unscheduled" List
When you move a block, you might "push" another task out of its window.

1. Look at the **Unscheduled Tasks** panel on the right.
2. If a task appears there, it means the manual move created an infeasible state.
3. Click **"Auto-Fix"** to let the Hermes Agent find a new global equilibrium.

---

## What you learned
You can now use the String Diagram as a professional control tool. You've learned to:
1. Map time and space to a 2D plane.
2. Distinguish departmental work by color.
3. Perform real-time "what-if" analysis using the heuristic re-optimizer.

### Next Steps
- **Deep Dive**: Read [`docs/explanation-string-diagram.md`](docs/explanation-string-diagram.md) for the D3.js implementation details.
- **Logic**: Read [`docs/explanation-spatio-temporal.md`](docs/explanation-spatio-temporal.md) to understand why blocks can't overlap.
