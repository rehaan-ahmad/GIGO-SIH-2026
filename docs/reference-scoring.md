# AHP Scoring Engine Reference

The **AHP Scoring Engine** ranks maintenance tasks to ensure that the most critical work is prioritized by the solver. It uses a weighted formula based on the Analytic Hierarchy Process (AHP).

## Scoring Formula

The criticality score $C$ for a task is calculated as a weighted sum of three primary dimensions:

$$C = (W_1 \cdot \text{Severity}) + (W_2 \cdot \text{OverdueDays}) + (W_3 \cdot \text{TrainDelayCost})$$

### Weight Configuration

| Weight | Variable | Value | Description |
| :--- | :--- | :--- | :--- |
| $W_1$ | **Severity** | $0.50$ | The technical severity of the fault (1-10 scale). |
| $W_2$ | **OverdueDays** | $0.30$ | Days elapsed since the task became overdue. |
| $W_3$ | **TrainDelayCost** | $0.20$ | Estimated cost of delays caused by not fixing the task. |

### Special Multipliers & Boosts

To account for operational realities, the engine applies the following modifiers:

- **S&T Boost**: Tasks from the **Signals & Telecommunications (S&T)** department receive a **1.5x multiplier** due to the high safety risk of signal failures.
- **Power Block Premium**: Tasks requiring a full power block receive a flat **+5.0 point boost** to ensure they are prioritized for the limited windows where power can be cut.

## Normalization

The raw score is normalized to a $0-100$ scale to provide a consistent priority metric for the Solver Agent:
$$\text{Normalized Score} = \min(100.0, \text{Raw Score} \times 4.0)$$

## API Interface

The scoring logic is implemented in `backend/agents/scoring_agent.py`.

### `score_tasks(tasks)`

**Parameters:**
- `tasks` (`List[Dict]`): Raw task data containing `severity`, `days_overdue`, `dept`, and `duration_mins`.

**Returns:**
A list of tasks sorted by `criticality_score` in descending order. Each task is augmented with:
- `criticality_score` (`float`): The normalized priority value.
- `shadow_block_candidate` (`bool`): True if the task is a candidate for an integrated block.

## Related
- For the design rationale, see [`docs/explanation-ahp-prioritization.md`](docs/explanation-ahp-prioritization.md).
- See [`docs/reference-solver.md`](docs/reference-solver.md) for how these scores are used in the objective function.
