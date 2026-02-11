#!/usr/bin/env python3
"""
Vendor Security Scorecard Engine — Stella Maris Governance
Composite scoring across 5 signal categories with trend analysis.
The photograph is the assessment. The scorecard is the surveillance camera.
"""

import json
import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path

CATEGORY_WEIGHTS = {
    "external_security": 0.30,
    "financial_health": 0.15,
    "compliance_currency": 0.20,
    "internal_behavior": 0.20,
    "relationship_health": 0.15
}

THRESHOLDS = {
    "healthy": 80,
    "watch": 60,
    "concern": 40,
    "critical": 0
}


def calculate_composite(category_scores: dict) -> dict:
    """Calculate weighted composite score from category scores."""
    composite = 0.0
    breakdown = {}

    for category, weight in CATEGORY_WEIGHTS.items():
        score = category_scores.get(category, 0)
        weighted = round(score * weight, 2)
        composite += weighted
        breakdown[category] = {
            "raw_score": score,
            "weight": weight,
            "weighted": weighted
        }

    return {
        "composite": round(composite, 2),
        "breakdown": breakdown
    }


def get_status(composite: float) -> str:
    """Determine vendor status from composite score."""
    if composite >= THRESHOLDS["healthy"]:
        return "HEALTHY"
    elif composite >= THRESHOLDS["watch"]:
        return "WATCH"
    elif composite >= THRESHOLDS["concern"]:
        return "CONCERN"
    else:
        return "CRITICAL"


def calculate_trend(history: list) -> dict:
    """Calculate trend from score history. Expects list of {date, composite}."""
    if len(history) < 2:
        return {"trend": "INSUFFICIENT DATA", "change": 0}

    # Sort by date
    sorted_hist = sorted(history, key=lambda x: x["date"])
    oldest = sorted_hist[0]["composite"]
    newest = sorted_hist[-1]["composite"]
    change = round(newest - oldest, 2)
    days = (datetime.fromisoformat(sorted_hist[-1]["date"]) -
            datetime.fromisoformat(sorted_hist[0]["date"])).days

    if abs(change) <= 5:
        trend = "STABLE"
    elif change > 5:
        trend = "IMPROVING"
    elif change < -15 and days <= 90:
        trend = "RAPID DECLINE"
    else:
        trend = "DECLINING"

    return {
        "trend": trend,
        "change": change,
        "period_days": days,
        "oldest_score": oldest,
        "newest_score": newest
    }


def check_category_alerts(category_scores: dict) -> list:
    """Check for category-level threshold breaches."""
    alerts = []
    for category, score in category_scores.items():
        if score < 40:
            alerts.append({
                "type": "CATEGORY_BREACH",
                "category": category,
                "score": score,
                "message": f"{category} below 40 threshold ({score})"
            })
    return alerts


def main():
    parser = argparse.ArgumentParser(description="Stella Maris Vendor Scorecard Engine")
    parser.add_argument("--signals", required=True, help="Path to signal data JSON")
    parser.add_argument("--register", default="scorecard-register.json", help="Path to scorecard register")
    args = parser.parse_args()

    with open(args.signals) as f:
        signals = json.load(f)
    
    register_path = Path(args.register)
    register = json.load(open(register_path)) if register_path.exists() else {"vendors": []}

    print(f"{'='*65}")
    print(f"  VENDOR SECURITY SCORECARD")
    print(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"{'='*65}")
    print()

    for vendor in signals.get("vendors", []):
        name = vendor["vendor_name"]
        categories = vendor.get("category_scores", {})
        history = vendor.get("score_history", [])

        result = calculate_composite(categories)
        status = get_status(result["composite"])
        trend = calculate_trend(history)
        alerts = check_category_alerts(categories)

        # Status indicator
        status_icon = {"HEALTHY": "●", "WATCH": "◐", "CONCERN": "○", "CRITICAL": "✗"}

        print(f"  {status_icon.get(status, '?')} {name}")
        print(f"    Composite: {result['composite']:.1f} [{status}]")
        print(f"    Trend: {trend['trend']} ({trend['change']:+.1f} over {trend.get('period_days', 0)} days)")
        print()

        for cat, detail in result["breakdown"].items():
            flag = " ⚠" if detail["raw_score"] < 40 else ""
            print(f"    {cat:.<40} {detail['raw_score']:>5.1f} × {detail['weight']:.0%} = {detail['weighted']:>5.2f}{flag}")

        if alerts:
            print()
            for alert in alerts:
                print(f"    🚨 ALERT: {alert['message']}")

        print(f"    {'─'*50}")
        print()

    print(f"{'='*65}")
    print(f"  Stella Maris Governance — The camera doesn't blink.")
    print(f"{'='*65}")


if __name__ == "__main__":
    main()
