# Understanding AHP Prioritization

Prioritizing railway maintenance is a multi-objective problem. You cannot simply look at "which fault is oldest" because a new, high-severity signal failure is far more dangerous than a month-old fence repair.

## The Problem: Subjective Prioritization

Manual prioritization often suffers from "Recency Bias" (fixing the last thing reported) or "Squeaky Wheel Bias" (fixing what the loudest department complains about). This leads to inefficient use of maintenance windows and increased safety risks.

## The Approach: Analytic Hierarchy Process (AHP)

We use a simplified **Analytic Hierarchy Process (AHP)** to turn subjective urgency into a mathematical criticality score.

### The Three Pillars of Criticality
1. **Technical Severity**: How bad is the fault? (e.g., a broken rail is 10, a missing sign is 1).
2. **Temporal Urgency**: How long has it been overdue? (The longer it waits, the higher the risk).
3. **Economic Impact**: What is the estimated cost of train delays if this isn't fixed?

By applying weights ($0.5$ for severity, $0.3$ for overdue, $0.2$ for cost), we ensure that safety-critical items always rise to the top, regardless of how recently they were reported.

### The "S&T Boost"
In railway operations, **Signals & Telecommunications (S&T)** failures can paralyze an entire section of the network. To account for this systemic risk, all S&T tasks receive a **1.5x multiplier**. This ensures that a "Medium" severity signal fault is treated as "High" because its impact is multiplied across all trains using that line.

## Trade-offs

| Choice | Benefit | Trade-off |
| :--- | :--- | :--- |
| **Fixed Weights** | Predictable and transparent ranking. | Does not adapt to changing seasonal priorities (e.g., winter prep). |
| **Normalized Scores** | Easy to communicate to controllers (0-100). | Loses the raw magnitude of the difference between tasks. |

## Related
- See [`docs/reference-scoring.md`](docs/reference-scoring.md) for the exact formula.
- See [`docs/reference-solver.md`](docs/reference-solver.md) for how scores are maximized in the objective function.
