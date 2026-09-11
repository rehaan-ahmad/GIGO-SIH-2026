# Understanding the Agentic Pipeline

The Railway Block Planner is not a single monolithic program, but a **pipeline of specialized agents**. This architecture decouples data ingestion, prioritization, optimization, and orchestration.

## The Problem: Coupling and Rigidity

In traditional software, changing the scoring logic usually requires touching the solver logic, which in turn requires touching the data ingestion layer. This makes the system rigid and difficult to test.

## The Approach: Agentic Decoupling

We implement an "Agentic Pipeline" where each agent has a single responsibility and a strictly defined input/output schema.

### The Pipeline Flow
`IngestionAgent` $\rightarrow$ `ScoringAgent` $\rightarrow$ `SolverAgent` $\rightarrow$ `API/UI`

1. **IngestionAgent**: The "Translator." It polls heterogeneous sources (TMS, SMMS) and normalizes them into a unified Pydantic model. It handles the "messy" data.
2. **ScoringAgent**: The "Judge." It doesn't care where the data came from; it only cares about the AHP formula. It ranks tasks by criticality.
3. **SolverAgent**: The "Optimizer." It takes the ranked list and fits them into windows using CP-SAT. It enforces the physical safety laws.
4. **HermesAgent**: The "Overseer." Hermes sits above the pipeline. It monitors the output and, if it sees too many unscheduled tasks, it triggers the pipeline to run again with different parameters.

## Why this Architecture?

| Benefit | Impact |
| :--- | :--- |
| **Testability** | You can test the `ScoringAgent` with mock data without ever running the `SolverAgent`. |
| **Interchangeability** | You can replace the CP-SAT solver with a Genetic Algorithm without changing a single line of code in the `IngestionAgent`. |
| **Autonomous Recovery** | Hermes allows the system to "self-heal" by detecting bottlenecks and re-optimizing without human intervention. |

## Trade-offs

- **Latency**: Passing data between agents adds a small amount of overhead compared to a single function call.
- **Complexity**: Requires more boilerplate (Pydantic models) to ensure agents communicate correctly.

## Related
- See [`docs/reference-hermes.md`](docs/reference-hermes.md) for the overseer's logic.
- See [`docs/reference-solver.md`](docs/reference-solver.md) for the optimization logic.
