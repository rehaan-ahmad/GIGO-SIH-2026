from typing import List, Dict, Any, Optional
import logging
from agents.ingestion_agent import ingest
from agents.scoring_agent import score_tasks
from agents.solver_agent import solve

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HermesAgent:
    """
    The Hermes Agent serves as the autonomous orchestrator for the Block Planner.
    It is responsible for 'Automatic Retrieval' of system state and 'Automated Actions'
    to maintain schedule health without human intervention.
    """

    def __init__(self):
        self.name = "Hermes"
        self.version = "1.0.0"

    def retrieve_system_summary(self) -> Dict[str, Any]:
        """
        Automatic Retrieval: Gathers a high-level summary of the current
        system state, including task criticality and corridor utilization.
        """
        logger.info("Hermes: Performing automatic system retrieval...")
        data = ingest()
        scored_tasks = score_tasks(data["tasks"])

        total_tasks = len(scored_tasks)
        critical_tasks = len([t for t in scored_tasks if t["criticality_score"] >= 80])

        # Calculate approximate corridor utilization
        windows = data["corridor_windows"]
        total_capacity = sum(
            (int(w["end_time"].split(":")[0])*60 + int(w["end_time"].split(":")[1])) -
            (int(w["start_time"].split(":")[0])*60 + int(w["start_time"].split(":")[1]))
            for w in windows
        )

        return {
            "agent": self.name,
            "status": "ONLINE",
            "metrics": {
                "total_tasks": total_tasks,
                "critical_tasks": critical_tasks,
                "total_capacity_mins": total_capacity,
                "criticality_ratio": round(critical_tasks / total_tasks, 2) if total_tasks > 0 else 0
            },
            "summary": f"System is monitoring {total_tasks} tasks with {critical_tasks} high-priority items."
        }

    def analyze_and_auto_optimize(self, horizon: str = "weekly") -> Dict[str, Any]:
        """
        Automated Action: Analyzes current schedule and triggers re-optimization
        if the ratio of unscheduled tasks exceeds a threshold.
        """
        logger.info("Hermes: Analyzing schedule for automated optimization...")

        data = ingest()
        scored_tasks = score_tasks(data["tasks"])
        result = solve(scored_tasks, data["corridor_windows"], mode="exact", horizon=horizon)

        unscheduled_count = len(result["unscheduled_tasks"])
        total_tasks = len(scored_tasks)
        failure_rate = unscheduled_count / total_tasks if total_tasks > 0 else 0

        # Trigger: If > 20% of tasks are unscheduled, Hermes considers this a 'bottleneck'
        if failure_rate > 0.20:
            logger.info(f"Hermes: Bottleneck detected ({failure_rate:.2%}). Triggering autonomous re-optimization...")
            # In a real system, this would involve adjusting weights or expanding windows.
            # Here, it returns the result and flags the autonomous action.
            return {
                "action": "AUTO_OPTIMIZE",
                "reason": f"Unscheduled task rate {failure_rate:.2%} exceeded threshold 20%",
                "result": result
            }

        return {
            "action": "MONITOR",
            "reason": "Schedule health within acceptable parameters.",
            "result": result
        }

# Singleton instance for the API
hermes = HermesAgent()
