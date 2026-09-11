"""
Scoring Agent Module
====================

This module implements the criticality scoring logic for railway maintenance tasks.
It uses an Analytic Hierarchy Process (AHP) weighted formula to prioritize tasks
based on severity, urgency (overdue days), and estimated train delay costs.
"""
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def score_tasks(tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Ranks maintenance tasks using an Analytic Hierarchy Process (AHP) weighted formula.

    The criticality score C_i is calculated as:
    C_i = (w1 * Severity) + (w2 * OverdueDays) + (w3 * TrainDelayCost)
    """
    W1 = 0.50
    W2 = 0.30
    W3 = 0.20

    scored_tasks = []

    for task in tasks:
        train_delay_cost = (task.get("duration_mins", 0) / 60) * (task.get("severity", 1) / 2)

        score = (W1 * task.get("severity", 0)) + \
                (W2 * task.get("days_overdue", 0)) + \
                (W3 * train_delay_cost)

        if task.get("dept") == "S&T":
            score *= 1.5

        if task.get("needs_power_block"):
            score += 5.0

        normalized_score = min(100.0, score * 4.0)

        scored_tasks.append({
            **task,
            "criticality_score": round(normalized_score, 2),
            "shadow_block_candidate": task.get("needs_power_block", False)
        })

    scored_tasks.sort(key=lambda x: x["criticality_score"], reverse=True)

    logger.info("Top 5 Critical Tasks:")
    for i, t in enumerate(scored_tasks[:5]):
        logger.info(f"{i+1}. {t['task_id']} - Score: {t['criticality_score']}")

    return scored_tasks
