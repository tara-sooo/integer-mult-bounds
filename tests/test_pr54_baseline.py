import unittest
from pathlib import Path

from scripts.replay_pr54_baseline import PINNED_COMMIT, research_summary


class Pr54BaselineTests(unittest.TestCase):
    def test_receipt_summary_matches_the_pinned_witness(self):
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(PINNED_COMMIT, "7210de7d0f9ccaeb64c3f60f188419e02be08d95")
        self.assertEqual(
            research_summary(root),
            {
                "R23": 32693,
                "R25": 43056,
                "W": 159592676,
                "kappa": "141532521/3125000000000",
            },
        )
