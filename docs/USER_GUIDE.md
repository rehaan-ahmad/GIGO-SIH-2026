# User Guide: Railway Block Planner

Welcome to the **Railway Block Planner**. This tool is designed for Railway Controllers to automate the scheduling of maintenance blocks while ensuring safety and efficiency.

## 🧭 Navigating the Dashboard

### 1. The Task Queue (Left Sidebar)
The sidebar displays all pending maintenance tasks.
- **Ranking**: Tasks are automatically sorted by their **Criticality Score**.
- **Urgency Badges**:
  - <span style="color:red">**Red**</span>: High Urgency (Score $\ge 80$). Action required immediately.
  - <span style="color:orange">**Amber**</span>: Medium Urgency (Score $50-80$).
  - <span style="color:green">**Green**</span>: Low Urgency (Score $< 50$).
- **Metadata**: Each card shows the department (Engineering, TRD, S&T) and the track chainage (km).

### 2. The String Diagram (Main View)
The center of the screen is a **Time-Distance Graph**.
- **X-Axis (Time)**: Represents the 24-hour window.
- **Y-Axis (Chainage)**: Represents the physical location on the track in kilometers.
- **Blocks**: Colored rectangles represent scheduled maintenance.
  - 🟥 **Red**: Engineering
  - 🟦 **Blue**: TRD (Traction Distribution)
  - 🟩 **Green**: S&T (Signaling & Telecomm)
- **Interpreting the Graph**: If two blocks overlap vertically at the same time, they are in the same location. The system prevents this for heavy machinery to ensure safety.

---

## 🛠 How to Generate a Plan

1. **Select Horizon**: Use the dropdown in the header to choose between a **Weekly Plan** (operational) or a **Monthly Strategic** plan.
2. **Trigger Optimization**: Click the **"Generate Plan"** button.
3. **Review the Results**:
   - The String Diagram will populate with optimized blocks.
   - The system will report the **Solver Status** (e.g., "OPTIMAL" means the best possible plan was found).
   - Any tasks that could not be scheduled will be flagged with a reason (e.g., `SPATIAL_CONFLICT`).

## ⚡ Advanced Features

### Manual Overrides (Drag-and-Drop)
If you need to move a block manually:
1. Drag a block to a new time window.
2. The system will trigger a **Real-time Heuristic Re-optimization**.
3. Other tasks will shift automatically to accommodate your change while maintaining safety buffers.

### Hermes Agent Automation
The system includes an autonomous agent named **Hermes**.
- **Automatic Retrieval**: Hermes continuously monitors the laod on the corridor.
- **Auto-Fix**: If the unscheduled task rate becomes too high, Hermes can be triggered via the API to perform an autonomous re-optimization.
