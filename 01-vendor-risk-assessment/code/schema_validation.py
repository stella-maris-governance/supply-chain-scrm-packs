#!/usr/bin/env python3
"""
Vendor Risk Register — Schema Validator
Ensures every entry in the register follows the required format.
Data integrity is as important as the data itself.

Stella Maris Governance — 2026
"""

import json
import sys
import argparse
from datetime import datetime, date
from pathlib import Path

REQUIRED_FIELDS = {
    "vendor_name": str,
    "tier": ["Critical", "High", "Medium", "Low"],
    "risk_score": (int, float),
    "approval_status": ["Approved", "Conditional", "Rejected", "Pending"],
    "approval_date": str,  # ISO 8601
    "approver": str,
    "next_reassessment_date": str,  # ISO 8601
    "burn_rate_flagged": bool
}

CONDITIONAL_FIELDS = {
    "compensating_controls": str  # Required when approval_status == "Conditional"
}


def validate_date(date_str: str) -> bool:
    """Validate ISO 8601 date format."""
    try:
        datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return True
    except (ValueError, AttributeError):
        return False


def validate_entry(entry: dict, index: int) -> list:
    """Validate a single register entry. Returns list of findings."""
    findings = []
    vendor = entry.get("vendor_name", f"Entry #{index}")

    # Required fields
    for field, expected_type in REQUIRED_FIELDS.items():
        value = entry.get(field)
        if value is None:
            findings.append(f"[{vendor}] MISSING: {field}")
            continue

        if isinstance(expected_type, list):
            if value not in expected_type:
                findings.append(f"[{vendor}] INVALID: {field}='{value}' — must be one of {expected_type}")
        elif isinstance(expected_type, tuple):
            if not isinstance(value, expected_type):
                findings.append(f"[{vendor}] TYPE ERROR: {field} must be {expected_type}, got {type(value).__name__}")
        elif expected_type == str:
            if not isinstance(value, str) or not value.strip():
                findings.append(f"[{vendor}] EMPTY: {field} cannot be blank")

    # Date validation
    for date_field in ["approval_date", "next_reassessment_date"]:
        value = entry.get(date_field, "")
        if value and not validate_date(value):
            findings.append(f"[{vendor}] DATE FORMAT: {date_field}='{value}' — must be ISO 8601")

    # Future date check for re-assessment
    reassess = entry.get("next_reassessment_date", "")
    if reassess and validate_date(reassess):
        reassess_date = datetime.fromisoformat(reassess.replace("Z", "+00:00")).date()
        if reassess_date < date.today():
            findings.append(f"[{vendor}] OVERDUE: next_reassessment_date is in the past ({reassess})")

    # Score range
    score = entry.get("risk_score", 0)
    if isinstance(score, (int, float)) and not (0 <= score <= 100):
        findings.append(f"[{vendor}] RANGE: risk_score={score} — must be 0-100")

    # Conditional field requirement
    if entry.get("approval_status") == "Conditional":
        controls = entry.get("compensating_controls", "")
        if not controls or not controls.strip():
            findings.append(f"[{vendor}] MISSING: compensating_controls required when status is Conditional")

    return findings


def main():
    parser = argparse.ArgumentParser(description="Stella Maris Vendor Register Schema Validator")
    parser.add_argument("--register", required=True, help="Path to vendor risk register JSON")
    args = parser.parse_args()

    register_path = Path(args.register)
    if not register_path.exists():
        print(f"ERROR: Register not found: {register_path}")
        sys.exit(1)

    with open(register_path) as f:
        data = json.load(f)

    vendors = data.get("vendors", [])
    total_findings = []

    print(f"{'='*60}")
    print(f"  VENDOR REGISTER SCHEMA VALIDATION")
    print(f"  Records: {len(vendors)}")
    print(f"  Date: {date.today().isoformat()}")
    print(f"{'='*60}")
    print()

    for i, vendor in enumerate(vendors):
        findings = validate_entry(vendor, i)
        total_findings.extend(findings)
        name = vendor.get("vendor_name", f"Entry #{i}")
        if findings:
            print(f"  ✗ {name}")
            for f_item in findings:
                print(f"    → {f_item}")
        else:
            print(f"  ✓ {name}")

    print()
    print(f"{'─'*60}")
    if total_findings:
        print(f"  RESULT: {len(total_findings)} finding(s) across {len(vendors)} vendors")
        print(f"  STATUS: FAIL — correct findings before next audit cycle")
    else:
        print(f"  RESULT: 0 findings across {len(vendors)} vendors")
        print(f"  STATUS: PASS — schema integrity verified")
    print(f"{'='*60}")

    sys.exit(1 if total_findings else 0)


if __name__ == "__main__":
    main()
