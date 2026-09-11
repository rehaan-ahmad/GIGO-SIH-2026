# Understanding Spatio-Temporal Packing

Railway maintenance planning is not just a scheduling problem—it is a **packing problem in 4D space**.

## The Problem: Spatial Blindness

Traditional railway scheduling tools often treat blocks as simple "time slots." They assume that if Window A is open from 02:00 to 06:00, any number of tasks can be placed there as long as the total duration fits.

**The failure mode:** If two heavy machinery teams are working on the same stretch of track at the same time, they risk physical collision or operational deadlock. This is "Spatial Blindness."

## The Approach: 1D Coordinate Mapping

To solve this, we treat the railway track as a **1D coordinate system (Chainage)** and time as a **linear axis**.

### The Safety Buffer
We implement a **500m Physical Clearance**. For any two blocks that overlap in time, the solver checks their chainage intervals:
- Block 1: $[S_1, E_1]$
- Block 2: $[S_2, E_2]$

If the distance between these intervals is $< 0.5\text{km}$, the assignment is forbidden. This ensures that no two teams are working in the same "safety zone" simultaneously.

### Stochastic Freight Guard
Railway corridors are not static. There is always a probability that a freight train will be delayed or diverted.

We introduce a **Stochastic Guard**: If a window has a high `freight_probability` ($> 0.4$), we forbid any block longer than 120 minutes. This prevents a single long maintenance block from causing a cascading failure across the entire network if a freight train arrives unexpectedly.

## Trade-offs

| Choice | Benefit | Trade-off |
| :--- | :--- | :--- |
| **Linear Approximation** | Extremely fast computation; fits into CP-SAT. | Ignores track curvature (negligible for 500m buffers). |
| **Hard Safety Buffer** | Zero risk of physical conflict. | May lead to "under-utilization" of track in very large corridors. |
| **Freight Probability** | Increases network resilience. | May push some critical work to less-optimal windows. |

## Alternatives Considered
We considered using full 2D GIS polygons for safety checks. However, given that railway tracks are essentially linear, the overhead of polygon intersection was $10\text{x}$ higher than linear interval checks for negligible gain in accuracy.

## Related
- See [`docs/reference-solver.md`](docs/reference-solver.md) for the implementation details.
- See [`docs/explanation-string-diagram.md`](docs/explanation-string-diagram.md) for how this is visualized.
