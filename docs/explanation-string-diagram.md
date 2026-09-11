# Understanding the String Diagram

The **String Diagram** (also known as a Time-Distance Graph) is the gold standard for railway operational visualization. Unlike a Gantt chart, it preserves the physical location of the work.

## The Problem: The "Where" is Missing

In a standard Gantt chart, you see that "Task A" happens from 02:00 to 04:00. But you don't know if Task A is at KM 10 or KM 500. If you have another task at the same time, you have to check a separate list to see if they conflict.

**The result:** High cognitive load for the controller and a high risk of spatial conflicts.

## The Approach: Spatio-Temporal Mapping

The String Diagram maps the maintenance schedule onto a 2D plane:
- **X-Axis**: Time (00:00 $\rightarrow$ 24:00).
- **Y-Axis**: Track Chainage (KM).

### How to Read the Diagram
- **A Horizontal Line/Rectangle**: Represents a maintenance block. Its length is the duration, and its vertical position is its location on the track.
- **Vertical Overlap**: If two blocks are at the same vertical position (same KM) and overlap horizontally (same time), they are in conflict.
- **Slope/Angle**: While not used for blocks, a diagonal line in a string diagram typically represents a train's movement (speed = slope).

### Color Coding
To allow controllers to see departmental distribution at a glance, blocks are color-coded:
- **Red**: Engineering
- **Blue**: TRD (Traction & Distribution)
- **Green**: S&T (Signals & Telecommunications)

## Design Decisions: Performance vs. Fidelity

To ensure the UI remains responsive ($<500\text{ms}$), we use a **Hybrid Rendering Strategy**:
1. **D3.js SVG**: Used for the primary diagram because it allows for high-precision coordinate mapping and easy interaction (dragging/clicking).
2. **Heuristic Re-optimization**: When a block is dragged, the system doesn't re-run the full CP-SAT solver (which takes seconds). Instead, it uses a greedy heuristic to shift other blocks, providing immediate visual feedback.

## Related
- See [`docs/reference-solver.md`](docs/reference-solver.md) for how the spatial constraints are enforced.
- See [`docs/explanation-spatio-temporal.md`](docs/explanation-spatio-temporal.md) for the underlying geometry.
