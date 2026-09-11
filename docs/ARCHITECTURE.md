# Technical Architecture: Spatio-Temporal Block Optimizer

## 1. Conceptual Model
Unlike traditional scheduling (which only considers *when* a task happens), this system treats railway maintenance as a **Spatio-Temporal Packing Problem**. 

We define a block as a tuple: $B = (S, E, T_{start}, T_{end}, D)$
- $S, E$: Start and End Chainage (km)
- $T_{start}, T_{end}$: Start and End Time
- $D$: Department (Engineering, TRD, S&T)

## 2. The Solver Logic (OR-Tools CP-SAT)
The heart of the system is a Constraint Programming (CP) model. The solver searches for an assignment of tasks to windows that maximizes the total criticality score while satisfying hard safety constraints.

### Hard Constraints
| Constraint | Logic | Purpose |
| :--- | :--- | :--- |
| **C1: Uniqueness** | $\sum_{w \in W} assign_{t,w} = 1$ | Every task must be scheduled exactly once. |
| **C2: Capacity** | $\sum_{t \in T} duration_t \cdot assign_{t,w} \le WindowDuration_w$ | Total work cannot exceed the window length. |
| **C3: Spatial Safety** | $Overlap(t1, t2) \implies assign_{t1,w} + assign_{t2,w} \le 1$ | Two heavy machines cannot be within 500m in the same window. |
| **C4: Freight Guard** | $Prob(Freight)_w > 0.4 \implies duration_t \le 120\text{min}$ | Prevent long blocks in high-risk freight windows. |

### The Objective Function
The solver maximizes the weighted sum of scheduled tasks:
$$\text{Maximize } \sum_{t \in T} \sum_{w \in W} (CriticalityScore_t \cdot assign_{t,w})$$

## 3. Criticality Scoring (AHP)
To reduce the search space, we pre-rank tasks. The score is calculated as:
$$C = (w_1 \cdot Severity) + (w_2 \cdot OverdueDays) + (w_3 \cdot DelayCost)$$
- **Weights**: $w_1=0.5, w_2=0.3, w_3=0.2$.
- **Boosts**: S&T signal failures receive a $1.5\times$ multiplier due to safety urgency.

## 4. Data Flow Pipeline
The system operates as a pipeline of specialized agents:
`IngestionAgent` $\rightarrow$ `ScoringAgent` $\rightarrow$ `SolverAgent` $\rightarrow$ `API` $\rightarrow$ `UI`

**The Agentic Layer (Hermes)**: 
Wrapped around this pipeline is the `HermesAgent`. Hermes acts as the autonomous brain that can:
- **Retrieve**: Poll the state of the pipeline to generate high-level summaries.
- **Monitor**: Continuously check for "bottlenecks" (e.g., excessive unscheduled tasks).
- **Act**: Trigger the `SolverAgent` autonomously when schedule health degrades.

1. **Ingestion**: `IngestionAgent` polls mock systems $\rightarrow$ validates via Pydantic $\rightarrow$ normalizes to unified `Task` schema.
2. **Scoring**: `ScoringAgent` computes $C$ for all tasks $\rightarrow$ sorts descending.
3. **Solving**: `SolverAgent` constructs the CP-SAT model $\rightarrow$ returns optimal `Schedule`.
4. **UI Rendering**: The React frontend consumes the `Schedule` and maps it to a D3.js Time-Distance coordinate system.

## 5. Real-time Heuristic
To maintain a responsive UI during "drag-and-drop," we bypass the CP-SAT solver (which takes seconds) and use a **Greedy Heuristic**:
1. Lock the dragged task into the new window.
2. Lock all "Approved" blocks.
3. Iteratively fill remaining space with highest-scored tasks that satisfy spatial/capacity checks.
4. Execution time: $\approx 10\text{ms} - 100\text{ms}$.
