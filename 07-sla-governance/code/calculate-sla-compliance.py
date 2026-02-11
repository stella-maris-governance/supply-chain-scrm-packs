#!/usr/bin/env python3
"""
SLA Compliance Calculator — Stella Maris Governance
90-day rolling SLA compliance score per vendor with category weighting.
"""

import json
import sys
import argparse
from datetime import datetime
from collections import defaultdict

CATEGORY_WEIGHTS = {
    "Availability": 0.30,
    "Incident Response": 0.25,
    "Support": 0.15,
    "Security": 0.20,
    "Data": 0.10
}

STATUS_THRESHOLDS = {
    "Exemplary": 95,
    "Compliant": 85,
    "Underperforming": 70,
    "Non-Compliant": 50,
    "Critical Breach": 0
}


def get_status(score: float) -> str:
    for status, threshold in STATUS_THRESHOLDS.items():
        if score >= threshold:
            return status
    return "Critical Breach"


def calculate_vendor_compliance(vendor_name: str, metrics: list, breaches: list) -> dict:
    """Calculate weighted SLA compliance for a vendor."""
    vendor_metrics = [m for m in metrics if m["vendor"] == vendor_name]
    vendor_breaches = [b for b in breaches if b["vendor"] == vendor_name]

    if not vendor_metrics:
        return {"vendor": vendor_name, "score": 0, "status": "NO DATA"}

    # Group by category
    category_metrics = defaultdict(list)
    for m in vendor_metrics:
        category_metrics[m["category"]].append(m)

    breached_metrics = set()
    for b in vendor_breaches:
        breached_metrics.add((b["vendor"], b["metric"]))

    # Calculate per-category compliance
    category_scores = {}
    for category, cat_metrics in category_metrics.items():
        total = len(cat_metrics)
        met = sum(1 for m in cat_metrics if (m["vendor"], m["metric"]) not in breached_metrics)
        category_scores[category] = (met / total * 100) if total > 0 else 100

    # Weighted composite
    composite = 0.0
    for category, weight in CATEGORY_WEIGHTS.items():
        cat_score = category_scores.get(category, 100)
        composite += cat_score * weight

    return {
        "vendor": vendor_name,
        "score": round(composite, 1),
        "status": get_status(composite),
        "category_scores": {k: round(v, 1) for k, v in category_scores.items()},
        "total_metrics": len(vendor_metrics),
        "total_breaches": len(vendor_breaches)
    }


def main():
    parser = argparse.ArgumentParser(description="Stella Maris SLA Compliance Calculator")
    parser.add_argument("--registry", required=True, help="Path to sla-registry.json")
    parser.add_argument("--breaches", required=True, help="Path to sla-breach-tracker.json")
    args = parser.parse_args()

    with open(args.registry) as f:
        registry = json.load(f)
    with open(args.breaches) as f:
        breach_data = json.load(f)

    metrics = registry.get("sla_metrics", [])
    breaches = breach_data.get("breaches", [])
    vendors = sorted(set(m["vendor"] for m in metrics))

    print(f"{'='*65}")
    print(f"  SLA COMPLIANCE REPORT")
    print(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"  Vendors: {len(vendors)} | Metrics: {len(metrics)} | Breaches: {len(breaches)}")
    print(f"{'='*65}")
    print()

    for vendor in vendors:
        result = calculate_vendor_compliance(vendor, metrics, breaches)
        icon = {"Exemplary": "●", "Compliant": "◐", "Underperforming": "◑",
                "Non-Compliant": "○", "Critical Breach": "✗"}.get(result["status"], "?")

        print(f"  {icon} {result['vendor']}")
        print(f"    Score: {result['score']}% [{result['status']}]")
        print(f"    Metrics: {result['total_metrics']} | Breaches: {result['total_breaches']}")
        for cat, score in result.get("category_scores", {}).items():
            flag = " ⚠" if score < 70 else ""
            print(f"    {cat:.<35} {score:>6.1f}%{flag}")
        print()

    print(f"{'='*65}")
    print(f"  A promise without measurement is a suggestion.")
    print(f"{'='*65}")


if __name__ == "__main__":
    main()
