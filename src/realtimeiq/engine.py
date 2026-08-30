from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class Decision:
    order_id: str
    customer_id: str
    predicted_delay_probability: float
    risk_band: str
    recommended_action: str
    expected_loss_without_action_usd: float
    intervention_cost_usd: float
    expected_value_usd: float
    actual_delayed: bool


ACTION_EFFECTS = {
    "observe": {"risk_reduction": 0.0, "cost_usd": 0.0},
    "priority-support": {"risk_reduction": 0.08, "cost_usd": 35.0},
    "expedite-shipment": {"risk_reduction": 0.28, "cost_usd": 240.0},
    "reroute-inventory": {"risk_reduction": 0.42, "cost_usd": 410.0},
}


def sigmoid(value: float) -> float:
    return 1.0 / (1.0 + math.exp(-value))


def predict_delay(order: dict[str, Any]) -> float:
    """Transparent synthetic risk model; coefficients are scenario assumptions."""
    score = -3.2
    score += 0.055 * order["supplier_delay_hours"]
    score += 0.62 * order["open_incidents"]
    score += 1.35 * (1.0 - order["inventory_coverage_ratio"])
    score += 0.75 if order["sentiment"] == "negative" else 0.0
    score += 0.35 if order["customer_tier"] == "strategic" else 0.0
    return round(sigmoid(score), 6)


def choose_action(order: dict[str, Any], probability: float, intervention_threshold: float = 0.25) -> tuple[str, float, float, float]:
    penalty = order["contract_penalty_usd"]
    contribution = order["order_value_usd"] * order["gross_margin_pct"]
    exposure = penalty + contribution
    expected_loss = probability * exposure
    if probability < intervention_threshold:
        return "observe", expected_loss, 0.0, 0.0
    candidates = []
    for action, effect in ACTION_EFFECTS.items():
        avoided = min(probability, effect["risk_reduction"]) * exposure
        net_value = avoided - effect["cost_usd"]
        candidates.append((net_value, action, effect["cost_usd"]))
    net_value, action, cost = max(candidates)
    if net_value <= 0:
        return "observe", expected_loss, 0.0, 0.0
    return action, expected_loss, cost, net_value


def evaluate(scenario: dict[str, Any]) -> dict[str, Any]:
    decisions: list[Decision] = []
    for order in scenario["orders"]:
        probability = predict_delay(order)
        action, loss, cost, value = choose_action(order, probability, scenario["model_policy"]["intervention_threshold"])
        band = "critical" if probability >= 0.75 else "high" if probability >= 0.5 else "medium" if probability >= 0.25 else "low"
        decisions.append(
            Decision(
                order_id=order["order_id"],
                customer_id=order["customer_id"],
                predicted_delay_probability=probability,
                risk_band=band,
                recommended_action=action,
                expected_loss_without_action_usd=round(loss, 2),
                intervention_cost_usd=round(cost, 2),
                expected_value_usd=round(value, 2),
                actual_delayed=order["actual_delayed"],
            )
        )

    threshold = scenario["model_policy"]["decision_threshold"]
    tp = sum(item.predicted_delay_probability >= threshold and item.actual_delayed for item in decisions)
    fp = sum(item.predicted_delay_probability >= threshold and not item.actual_delayed for item in decisions)
    fn = sum(item.predicted_delay_probability < threshold and item.actual_delayed for item in decisions)
    tn = len(decisions) - tp - fp - fn
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    brier = sum((item.predicted_delay_probability - int(item.actual_delayed)) ** 2 for item in decisions) / len(decisions)

    processing_cost = scenario["unit_economics"]["events_processed"] / 1_000_000 * scenario["unit_economics"]["cost_per_million_events_usd"]
    total_action_cost = sum(item.intervention_cost_usd for item in decisions)
    gross_expected_value = sum(item.expected_value_usd for item in decisions)
    net_expected_value = gross_expected_value - processing_cost
    acted = sum(item.recommended_action != "observe" for item in decisions)
    report: dict[str, Any] = {
        "schema_version": "realtimeiq/v1",
        "scenario": scenario["scenario"],
        "evidence_level": "deterministic-synthetic-case-study",
        "freshness_slo_seconds": scenario["freshness_slo_seconds"],
        "decisions": [asdict(item) for item in decisions],
        "predictive_analytics": {
            "model": "transparent-logistic-risk-score",
            "decision_threshold": threshold,
            "intervention_threshold": scenario["model_policy"]["intervention_threshold"],
            "confusion_matrix": {"true_positive": tp, "false_positive": fp, "false_negative": fn, "true_negative": tn},
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "brier_score": round(brier, 4),
        },
        "prescriptive_analytics": {
            "orders_evaluated": len(decisions),
            "interventions_recommended": acted,
            "modeled_gross_expected_value_usd": round(gross_expected_value, 2),
            "modeled_intervention_cost_usd": round(total_action_cost, 2),
        },
        "unit_economics": {
            "events_processed": scenario["unit_economics"]["events_processed"],
            "modeled_data_platform_cost_usd": round(processing_cost, 2),
            "modeled_net_expected_value_usd": round(net_expected_value, 2),
            "modeled_return_per_platform_dollar": round(net_expected_value / processing_cost, 2),
            "modeled_cost_per_evaluated_order_usd": round(processing_cost / len(decisions), 2),
            "modeled_cost_per_recommended_intervention_usd": round(processing_cost / acted, 2) if acted else None,
        },
        "promotion": {
            "status": "evaluation-only",
            "auto_execute": False,
            "required_gates": ["live data contract validation", "prospective model validation", "bias review", "operator approval", "bounded canary", "rollback"],
        },
        "claim_boundary": [
            "All customers, orders, outcomes, prices and costs are synthetic scenario inputs",
            "Predictive performance on this small deterministic fixture is not evidence of production accuracy",
            "Expected value is modeled opportunity, not realized revenue or guaranteed savings",
            "No Microsoft Fabric, Databricks, Kafka cloud service or customer data was accessed",
        ],
    }
    canonical = json.dumps(report, sort_keys=True, separators=(",", ":"))
    report["receipt_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    return report


def validate(scenario: dict[str, Any]) -> None:
    required = {"scenario", "freshness_slo_seconds", "model_policy", "unit_economics", "orders"}
    missing = sorted(required - scenario.keys())
    if missing:
        raise ValueError(f"missing keys: {', '.join(missing)}")
    if not scenario["orders"]:
        raise ValueError("orders must not be empty")
    for key in ("decision_threshold", "intervention_threshold"):
        if not 0 < scenario["model_policy"].get(key, 0) < 1:
            raise ValueError(f"{key} must be between zero and one")
    ids = [item["order_id"] for item in scenario["orders"]]
    if len(ids) != len(set(ids)):
        raise ValueError("order_id must be unique")
    for order in scenario["orders"]:
        if not 0 <= order["inventory_coverage_ratio"] <= 1:
            raise ValueError("inventory_coverage_ratio must be between zero and one")
        if not 0 < order["gross_margin_pct"] <= 1:
            raise ValueError("gross_margin_pct must be between zero and one")
