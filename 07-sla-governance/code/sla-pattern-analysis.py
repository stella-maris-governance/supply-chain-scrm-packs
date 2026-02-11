#!/usr/bin/env python3
"""
SLA Pattern Analysis — Stella Maris Governance
Detects recurring SLA failures indicating systemic vendor issues.
"""

import json
import argparse
from collections import defaultdict
from datetime import datetime


def analyze_patterns(breaches: list, window_days: int = 90) -> list:
    """Detect patterns: 3+ breaches in same category within window."""
    vendor_category = defaultdict(list)
    for breach in breaches:
        key = (breach["vendor"], breach["category"])
        vendor_category[key].append(breach)

    patterns = []
    for (vendor, category), cat_breaches in vendor_category.items():
        if len(cat_breaches) >= 3:
            patterns.append({
                "type": "SYSTEMIC",
                "vendor": vendor,
                "category": category,
                "breach_count": len(cat_breaches),
                "dates": [b["breach_date"] for b in cat_breaches],
                "severity": "HIGH"
            })
        elif len(cat_breaches) >= 2:
            # Check for escalating severity
            severities = [b["severity"] for b in cat_breaches]
            if severities[-1] in ("Major", "Critical") and severities[0] in ("Minor", "Moderate"):
                patterns.append({
                    "type": "ESCALATING",
                    "vendor": vendor,
                    "category": category,
                    "breach_count": len(cat_breaches),
                    "severity_progression": severities,
                    "severity": "MEDIUM"
                })

    # Check for same root cause across breaches
    root_causes = defaultdict(list)
    for breach in breaches:
        root = breach.get("root_cause", "Unknown")
        root_causes[root].append(breach)
    for root, root_breaches in root_causes.items():
        if len(root_breaches) >= 2 and root != "Unknown":
            patterns.append({
                "type": "UNRESOLVED_ROOT_CAUSE",
                "root_cause": root,
                "affected_vendors": list(set(b["vendor"] for b in root_breaches)),
                "breach_count": len(root_breaches),
                "severity": "HIGH"
            })

    return patterns


def main():
    parser = argparse.ArgumentParser(description="Stella Maris SLA Pattern Analysis")
    parser.add_argument("--breaches", required=True, help="Path to sla-breach-tracker.json")
    parser.add_argument("--window", type=int, default=90, help="Analysis window in days")
    args = parser.parse_args()

    with open(args.breaches) as f:
        data = json.load(f)

    breaches = data.get("breaches", [])
    patterns = analyze_patterns(breaches, args.window)

    print(f"{'='*60}")
    print(f"  SLA PATTERN ANALYSIS")
    print(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"  Window: {args.window} days | Breaches: {len(breaches)}")
    print(f"{'='*60}")
    print()

    if patterns:
        for p in patterns:
            icon = "🔴" if p["severity"] == "HIGH" else "🟡"
            print(f"  {icon} [{p['type']}] {p.get('vendor', 'Multi-vendor')}")
            for k, v in p.items():
                if k not in ("type", "severity"):
                    print(f"      {k}: {v}")
            print()
    else:
        print(f"  ✓ No patterns detected")
        print()

    print(f"{'='*60}")
    print(f"  Patterns found: {len(patterns)}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
