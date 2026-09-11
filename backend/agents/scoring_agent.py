from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def score_tasks(tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Assigns criticality scores to tasks based on AHP-weighted formula.
    C_i = (w1 * Severity) + (w2 * OverdueDays) + (w3 * TrainDelayCost)
    """
    # Weights
    W1 = 0.50  # Severity
    W2 = 0.30  # Overdue Days
    W3 = 0.20  # Train Delay Cost (Simplified as a function of duration/severity)

    scored_tasks = []

    for task in tasks:
        # Simplified TrainDelayCost: assume 10 points per hour of duration, scaled by severity
        # In production, this would be predicted by XGBoost
        train_delay_cost = (task.get("duration_mins", 0) / 60) * (task.get("severity", 1) / 2)

        # Basic score
        score = (W1 * task.get("severity", 0)) + \
                (W2 * task.get("days_overdue", 0)) + \
                (W3 * train_delay_cost)

        # Multipliers
        # S&T signal failure tasks: x1.5 (safety-critical)
        if task.get("dept") == "S&T":
            score *= 1.5

        # Power block required: +5 points (clustering bonus)
        if task.get("needs_power_block"):
            score += 5.0

        # Normalize score 0-100 (approximate normalization)
        # Max possible score is roughly (0.5*10) + (0.3*30) + (0.2*30) + 5 * 1.5 = ~25
        # We multiply by 4 to bring it closer to a 0-100 scale for the solver
        normalized_score = min(100.0, score * 4.0)

        # Priority rank will be determined by sorting
        scored_tasks.append({
            **task,
            "criticality_score": round(normalized_score, 2),
            "shadow_block_candidate": task.get("needs_power_block", False)
        })

    # Sort descending by criticality_score
    scored_tasks.sort(key=lambda x: x["criticality_score"], reverse=True)

    # Log top 5
    logger.info("Top 5 Critical Tasks:")
    for i, t in enumerate(scored_tasks[:5]):
        logger.info(f"{i+1}. {t['task_id']} - Score: {t['criticality_score']}")

    return scored_tasks
