import copy
import json
import unittest
from pathlib import Path

from realtimeiq.engine import evaluate, predict_delay, validate
from realtimeiq.render import html_dashboard


ROOT = Path(__file__).parents[1]


class DecisionIntelligenceTests(unittest.TestCase):
    def setUp(self):
        self.scenario = json.loads((ROOT / "examples/revenue-at-risk/scenario.json").read_text())

    def test_high_risk_order_scores_above_low_risk_order(self):
        high, low = self.scenario["orders"][0], self.scenario["orders"][1]
        self.assertGreater(predict_delay(high), predict_delay(low))

    def test_prescriptive_action_is_economically_positive(self):
        report = evaluate(self.scenario)
        acted = [item for item in report["decisions"] if item["recommended_action"] != "observe"]
        self.assertTrue(acted)
        self.assertTrue(all(item["expected_value_usd"] > 0 for item in acted))

    def test_low_risk_orders_remain_observation_only(self):
        report = evaluate(self.scenario)
        low_risk = [item for item in report["decisions"] if item["predicted_delay_probability"] < 0.25]
        self.assertTrue(low_risk)
        self.assertTrue(all(item["recommended_action"] == "observe" for item in low_risk))

    def test_model_performance_is_reported(self):
        metrics = evaluate(self.scenario)["predictive_analytics"]
        self.assertGreaterEqual(metrics["precision"], 0.8)
        self.assertGreaterEqual(metrics["recall"], 0.8)
        self.assertIn("brier_score", metrics)

    def test_unit_economics_are_traceable(self):
        economics = evaluate(self.scenario)["unit_economics"]
        self.assertEqual(economics["modeled_data_platform_cost_usd"], 8000.0)
        self.assertGreater(economics["modeled_net_expected_value_usd"], 0)
        self.assertGreater(economics["modeled_return_per_platform_dollar"], 1)

    def test_decisions_never_auto_execute(self):
        self.assertFalse(evaluate(self.scenario)["promotion"]["auto_execute"])

    def test_receipt_is_deterministic(self):
        self.assertEqual(evaluate(self.scenario)["receipt_sha256"], evaluate(self.scenario)["receipt_sha256"])

    def test_duplicate_order_is_rejected(self):
        invalid = copy.deepcopy(self.scenario)
        invalid["orders"].append(copy.deepcopy(invalid["orders"][0]))
        with self.assertRaises(ValueError):
            validate(invalid)

    def test_invalid_inventory_ratio_is_rejected(self):
        invalid = copy.deepcopy(self.scenario)
        invalid["orders"][0]["inventory_coverage_ratio"] = 1.2
        with self.assertRaises(ValueError):
            validate(invalid)

    def test_executive_dashboard_preserves_claim_boundary(self):
        dashboard = html_dashboard(evaluate(self.scenario))
        self.assertIn("Real-Time Revenue Intelligence", dashboard)
        self.assertIn("Expected value is modeled opportunity", dashboard)


if __name__ == "__main__":
    unittest.main()
