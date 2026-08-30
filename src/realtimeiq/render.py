from __future__ import annotations

from typing import Any


def markdown(report: dict[str, Any]) -> str:
    predictive = report["predictive_analytics"]
    economics = report["unit_economics"]
    lines = [
        f"# {report['scenario']}",
        "",
        f"**Evidence:** `{report['evidence_level']}`  ",
        f"**Receipt:** `{report['receipt_sha256']}`  ",
        f"**Automation:** `disabled`",
        "",
        "## Executive decision scorecard",
        "",
        f"- Modeled net expected value: `${economics['modeled_net_expected_value_usd']:,.2f}`",
        f"- Modeled return per platform dollar: `{economics['modeled_return_per_platform_dollar']:,.2f}x`",
        f"- Recommended interventions: `{report['prescriptive_analytics']['interventions_recommended']}`",
        f"- Predictive precision: `{predictive['precision']:.2%}`",
        f"- Predictive recall: `{predictive['recall']:.2%}`",
        f"- Brier score: `{predictive['brier_score']}`",
        "",
        "## Prescriptive decisions",
        "",
        "| Order | Customer | Risk | Band | Recommendation | Expected value |",
        "|---|---|---:|---|---|---:|",
    ]
    for item in report["decisions"]:
        lines.append(f"| {item['order_id']} | {item['customer_id']} | {item['predicted_delay_probability']:.1%} | {item['risk_band']} | {item['recommended_action']} | ${item['expected_value_usd']:,.2f} |")
    lines.extend(["", "## Claim boundary", ""])
    lines.extend(f"- {item}" for item in report["claim_boundary"])
    return "\n".join(lines) + "\n"


def html_dashboard(report: dict[str, Any]) -> str:
    economics = report["unit_economics"]
    predictive = report["predictive_analytics"]
    rows = "".join(
        f"<tr><td>{item['order_id']}</td><td>{item['customer_id']}</td><td>{item['predicted_delay_probability']:.1%}</td><td><span class='band {item['risk_band']}'>{item['risk_band']}</span></td><td>{item['recommended_action']}</td><td>${item['expected_value_usd']:,.0f}</td></tr>"
        for item in sorted(report["decisions"], key=lambda value: value["expected_value_usd"], reverse=True)
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Real-Time Revenue Intelligence</title><style>
:root{{--ink:#e8edf7;--muted:#97a3b8;--panel:#121a2b;--line:#26324a;--cyan:#4de2c5;--amber:#ffbf69;--red:#ff6b7a}}
*{{box-sizing:border-box}} body{{margin:0;background:#08101f;color:var(--ink);font:15px Inter,system-ui,sans-serif}} main{{max-width:1240px;margin:auto;padding:38px}}
h1{{font-size:34px;margin:0 0 6px}} .sub{{color:var(--muted);margin-bottom:28px}} .grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}}
.card{{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:18px}} .label{{color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.08em}} .value{{font-size:28px;font-weight:750;margin-top:8px}}
.wide{{margin-top:16px}} table{{width:100%;border-collapse:collapse}} th,td{{text-align:left;padding:12px;border-bottom:1px solid var(--line)}} th{{color:var(--muted);font-size:12px;text-transform:uppercase}} .band{{padding:4px 8px;border-radius:99px;background:#24314a}} .critical{{background:#5c2130}} .high{{background:#5b3f1d}} .medium{{background:#293e55}} .low{{background:#17443d}} .boundary{{color:var(--muted);font-size:12px;line-height:1.6}}
@media(max-width:850px){{.grid{{grid-template-columns:1fr 1fr}}main{{padding:20px}}}} </style></head>
<body><main><h1>Real-Time Revenue Intelligence</h1><div class="sub">Predictive risk · Prescriptive action · Business intelligence · Unit economics</div>
<section class="grid"><div class="card"><div class="label">Modeled net expected value</div><div class="value">${economics['modeled_net_expected_value_usd']:,.0f}</div></div>
<div class="card"><div class="label">Return / platform dollar</div><div class="value">{economics['modeled_return_per_platform_dollar']:,.1f}×</div></div>
<div class="card"><div class="label">Predictive precision</div><div class="value">{predictive['precision']:.0%}</div></div>
<div class="card"><div class="label">Predictive recall</div><div class="value">{predictive['recall']:.0%}</div></div></section>
<section class="card wide"><div class="label">Prescriptive decision queue</div><table><thead><tr><th>Order</th><th>Customer</th><th>Risk</th><th>Band</th><th>Recommended action</th><th>Expected value</th></tr></thead><tbody>{rows}</tbody></table></section>
<section class="card wide boundary"><strong>Evidence boundary.</strong> Synthetic deterministic case study. Expected value is modeled opportunity, not realized revenue. No action auto-executes. Receipt: {report['receipt_sha256']}</section>
</main></body></html>"""
