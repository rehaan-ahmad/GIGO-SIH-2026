import unittest
from agents.scoring_agent import score_tasks

class TestScoringAgent(unittest.TestCase):
    def test_score_ranking(self):
        tasks = [
            {
                "task_id": "T1", "dept": "Engineering", "severity": 5, "days_overdue": 2,
                "duration_mins": 120, "needs_power_block": False
            },
            {
                "task_id": "T2", "dept": "S&T", "severity": 10, "days_overdue": 10,
                "duration_mins": 120, "needs_power_block": True
            },
            {
                "task_id": "T3", "dept": "TRD", "severity": 2, "days_overdue": 1,
                "duration_mins": 60, "needs_power_block": False
            }
        ]

        scored = score_tasks(tasks)

        # T2 should be the most critical (S&T, High severity, High overdue, Power block)
        self.assertEqual(scored[0]["task_id"], "T2")
        # T3 should be the least critical
        self.assertEqual(scored[-1]["task_id"], "T3")
        # T2 score should be significantly higher than T3
        self.assertGreater(scored[0]["criticality_score"], scored[-1]["criticality_score"])

if __name__ == "__main__":
    unittest.main()
