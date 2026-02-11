#!/usr/bin/env python3
"""
Vendor Risk Scoring Engine — Stella Maris Governance
Deterministic scoring: same inputs, same score, every time.
The engine doesn't have opinions.
"""

import json
import sys
import argparse
from pathlib import Path


def calculate_vendor_score(assessment: dict, scoring_logic: dict) -> dict:
    """Calculate weighted risk score across 6 domains."""
    domain_results = {}
    final_score = 0.0

    for domain, config in scoring_logic.items():
        weight = config["weight"]
        domain_data = assessment.get(domain, {})

        if not domain_data:
            domain_results[domain] = {
                "score": 0,
                "weight": weight,
                "weighted": 0,
                "status": "NOT ASSESSED"
            }
            continue

        # Average all metric scores in the domain (each 0-100)
        metric_scores = [v for v in domain_data.values() if isinstance(v, (int, float))]
        avg = sum(metric_scores) / len(metric_scores) if metric_scores else 0
        weighted = round(avg * weight, 2)
        final_score += weighted

        domain_results[domain] = {
            "score": round(avg, 1),
            "weight": weight,
            "weighted": weighted,
            "metrics_counted": len(metric_scores)
        }

    return {
        "domain_scores": domain_results,
        "total_score": round(final_score, 2)
    }


def get_risk_status(score: float, thresholds: dict) -> str:
    """Determine risk status from score thresholds."""
    if score >= thresholds["accept"]["min"]:
        return "ACCEPT"
    elif score >= thresholds["conditional"]["min"]:
        return "CONDITIONAL"
    elif score >= thresholds["elevated_review"]["min"]:
        return "ELEVATED REVIEW"
    else:
        return "REJECT"


def check_burn_rate(financial_data: dict, threshold: float) -> dict:
    """Check vendor financial burn rate against threshold."""
    cash_months = financial_data.get("Solvency_Months", 0)
    burn_rate = financial_data.get("Annual_Burn_Rate", 0)

    flagged = burn_rate > (threshold * 100) if burn_rate else False
    runway = round(cash_months / (burn_rate / 12), 1) if burn_rate > 0 else cash_months

    return {
        "burn_rate_flagged": flagged,
        "stated_cash_months": cash_months,
        "annual_burn_rate_pct": burn_rate,
        "effective_runway_months": runway
    }


def main():
    parser = argparse.ArgumentParser(description="Stella Maris Vendor Risk Scoring Engine")
    parser.add_argument("--input", required=True, help="Path to vendor assessment JSON")
    parser.add_argument("--config", default="risk-scoring-model.json", help="Path to scoring model config")
    args = parser.parse_args()

    config_path = Path(args.config)
    input_path = Path(args.input)

    if not config_path.exists():
        print(f"ERROR: Config not found: {config_path}")
        sys.exit(1)
    if not input_path.exists():
        print(f"ERROR: Assessment not found: {input_path}")
        sys.exit(1)

    with open(config_path) as f:
        config = json.load(f)
    with open(input_path) as f:
        assessment = json.load(f)

    scoring_logic = config["scoring_logic"]
    thresholds = config["thresholds"]

    # Calculate score
    result = calculate_vendor_score(assessment.get("domains", {}), scoring_logic)
    status = get_risk_status(result["total_score"], thresholds)

    # Check burn rate
    financial_data = assessment.get("domains", {}).get("Financial Stability", {})
    burn_check = check_burn_rate(
        financial_data,
        scoring_logic.get("Financial Stability", {}).get("burn_rate_threshold", 0.30)
    )

    # Output
    vendor_name = assessment.get("vendor_name", "Unknown")
    print(f"{'='*60}")
    print(f"  VENDOR RISK SCORE: {vendor_name}")
    print(f"{'='*60}")
    print()

    for domain, detail in result["domain_scores"].items():
        flag = ""
        if domain == "Financial Stability" and burn_check["burn_rate_flagged"]:
            flag = " ⚠ BURN RATE FLAG"
        print(f"  {domain:.<35} {detail['score']:>5.1f} × {detail['weight']:.0%} = {detail['weighted']:>5.2f}{flag}")

    print(f"  {'─'*55}")
    print(f"  {'TOTAL SCORE':.<35} {result['total_score']:>5.2f}")
    print(f"  {'STATUS':.<35} {status}")
    print()

    if burn_check["burn_rate_flagged"]:
        print(f"  ⚠ FINANCIAL WARNING: Annual burn rate {burn_check['annual_burn_rate_pct']}%")
        print(f"    Stated cash: {burn_check['stated_cash_months']} months")
        print(f"    Effective runway: {burn_check['effective_runway_months']} months")
        print()

    print(f"{'='*60}")
    print(f"  Stella Maris Governance — The engine doesn't have opinions.")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
