from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import evaluate, validate
from .render import html_dashboard, markdown


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate real-time predictive and prescriptive business decisions")
    parser.add_argument("scenario", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    scenario = json.loads(args.scenario.read_text())
    validate(scenario)
    report = evaluate(scenario)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "decision-intelligence.json").write_text(json.dumps(report, indent=2) + "\n")
    (args.output / "executive-scorecard.md").write_text(markdown(report))
    (args.output / "executive-dashboard.html").write_text(html_dashboard(report))
    print(json.dumps({"receipt_sha256": report["receipt_sha256"], "promotion": report["promotion"]["status"]}, indent=2))


if __name__ == "__main__":
    main()
