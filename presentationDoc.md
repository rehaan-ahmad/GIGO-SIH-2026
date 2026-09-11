# AI-Powered Automatic Block Planning System: Spatio-Temporal Maintenance Optimizer

## Page 1: Idea Title & Proposed Solution

**Idea Title:** 
Aarush: Spatio-Temporal Rolling Block System (RBS) for Integrated Railway Maintenance

**Detailed Proposed Solution:**
Current block planning via the Block Demand Management System (BDMS) operates in silos across Engineering (TMS), Signalling (SMMS), and Traction (TDMS). "Aarush" is a centralized, AI-driven optimization engine that ingests cross-departmental defect logs and COA (Control Office Application) train forecasts. It uses a Multi-Criteria Decision Analysis (AHP) pipeline to rank task criticality, followed by a Constraint Programming (CP-SAT) solver to generate conflict-free, multi-departmental "Shadow Blocks." 

**How It Addresses the Problem:**
Instead of granting isolated 2-hour blocks to different departments on the same day, Aarush identifies spatial and temporal overlaps. If the Engineering department requires a 3-hour power block for track tamping, the system automatically pulls pending TDMS (OHE repair) and SMMS (point machine testing) tasks within that specific track chainage (Km marker) and schedules them concurrently, minimizing overall line downtime.

**Innovation and Uniqueness:**
1. **Chainage-Aware Spatial Deconfliction:** Unlike standard schedulers, Aarush understands physical track layout. It prevents heavy machinery collisions by enforcing a strict 500m minimum spatial buffer between different departmental gangs operating in the same time block.
2. **Stochastic Freight Buffering:** Recognizes that COA goods train forecasts are dynamic. The system injects a probabilistic ±120-minute buffer for freight movements, ensuring maintenance blocks are not shattered by delayed goods trains.
3. **Time-Distance String Diagram UI:** Abandons standard bar charts for authentic railway String Diagrams, allowing Traffic Controllers to visualize train paths intersecting with maintenance block polygons in real-time.

---

## Page 2: Technical Approach

**Tech Stack:**
*   **Backend:** Python (FastAPI) for high-concurrency API endpoints, Celery for asynchronous solver task queues.
*   **Optimization Engine:** Google OR-Tools (CP-SAT Solver) for combinatorial optimization, XGBoost for defect criticality scoring.
*   **Database:** PostgreSQL with PostGIS extension (crucial for spatial linear referencing of track chainages), Redis for caching COA live forecasts.
*   **Frontend:** React.js + D3.js (for rendering complex, interactive Time-Distance String Diagrams) and TailwindCSS.

**System Architecture:**
1.  **Ingestion Layer:** Kafka/REST endpoints poll mock JSON schemas representing TMS, SMMS, TDMS, and COA.
2.  **Scoring Engine:** Normalizes task urgency. Calculates $C_i$ (Criticality Score) utilizing the mathematical model: 
    $$C_i = (w_1 \cdot \text{Severity}) + (w_2 \cdot \text{OverdueDays}) + (w_3 \cdot \Delta \text{TrainDelayCost})$$
3.  **Solver Core (OR-Tools):** Solves a Mixed-Integer constrained problem. Maximizes total $C_i$ resolved while strictly adhering to train timetables and spatial track capacity.
4.  **Presentation Layer:** Pushes the 7-day Rolling Block plan to the React frontend.

**User Flow:**
1.  **Section Controller** logs into the dashboard and views the system-generated 7-day block proposal overlaid on the String Diagram.
2.  The Controller visually inspects "Integrated Blocks" (e.g., Track maintenance + OHE maintenance bundled together).
3.  If a sudden VIP train is scheduled, the Controller drags a block window on the UI to adjust it.
4.  The system runs a **sub-second heuristic re-optimization**, shifting conflicting maintenance tasks to the next optimal corridor without breaking constraints.
5.  Controller approves the plan, and automated disconnection grants are issued to departmental supervisors via BDMS.

---

## Page 3: Feasibility and Viability

**Analysis of Feasibility:**
The architecture relies on proven, open-source operations research tools (OR-Tools) used heavily in global supply chain logistics. By enforcing standard JSON data contracts, the solution can act as an overlay on top of existing CRIS infrastructure without requiring a massive database migration. 

**Potential Challenges and Strategies:**
*   **Challenge 1: Solver Combinatorial Explosion (Latency):** Running an exact mathematical optimization on 1,000+ tasks across a 500km railway division can take hours, freezing the UI.
    *   **Strategy:** Implement a "Two-Tier" solver strategy. A background CP-SAT job runs nightly for the 30-day strategic plan. For real-time UI interaction, a greedy heuristic algorithm executes in <500ms to provide immediate "what-if" feedback to the controller.
*   **Challenge 2: Incomplete Legacy Data:** TMS/TDMS entries might lack precise GPS coordinates, relying only on abstract chainage (e.g., Km 1042/15).
    *   **Strategy:** Use PostGIS Linear Referencing Systems (LRS). The system maps abstract chainage markers to a 1D spatial model, allowing the algorithm to compute physical distances between tasks without needing exact lat/long coordinates.

---

## Page 4: Impacts and Benefits

**Potential Impact on Target Audience:**
*   **Traffic Controllers:** Eliminates the cognitive overload of manually cross-referencing three different departmental spreadsheets against live train charts.
*   **Maintenance Supervisors:** Provides deterministic, guaranteed working windows, eliminating situations where labor and machinery are deployed but denied a traffic block at the last minute.

**Social, Economic, and Environmental Benefits:**
*   **Economic:** Indian Railways loses millions annually to asset downtime and train delay penalties. By increasing "Shadow Block" colocation by an estimated 25%, Aarush recovers hundreds of hours of line capacity per division annually, allowing for increased freight throughput.
*   **Safety (Social):** Reduces the pressure on trackmen working under tight, poorly planned margins. Guaranteed, digitally locked spatial clearances prevent accidents between heavy track machinery and manual labor gangs.
*   **Environmental:** Optimizing the dispatch of diesel-heavy Track Tamping machines and Tower Wagons reduces unnecessary idling and travel, cutting down Division-level locomotive emissions.

---

## Page 5: Research and References

1.  **Block Demand Management System (BDMS) / Rolling Block System (RBS):** Official Ministry of Railways framework for integrating divisional block demands across Engineering, S&T, and TRD [1].
2.  **Control Office Application (COA):** CRIS architecture for tracking real-time passenger and unscheduled freight operations on the Indian Railways network [2].
3.  **Google OR-Tools CP-SAT:** State-of-the-art constraint programming solver utilized for job-shop and spatial scheduling (Google Developers, 2024).
4.  **Track Management System (TMS) & PostGIS Linear Referencing:** Research methodologies for translating railway chainage (Km posts) into computable 1D spatial distances for algorithmic processing.