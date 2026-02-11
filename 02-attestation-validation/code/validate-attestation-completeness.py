#!/usr/bin/env python3
"""
Attestation Completeness Validator — Stella Maris Governance
Ensures all vendors have required attestations based on their tier.
"""

import json
import sys
import argparse
from pathlib import Path

TIER_REQUIREMENTS = {
    "Critical": {
        "required": ["SOC 2 Type II", "Penetration Test"],
        "recommended": ["ISO 27001", "FedRAMP"],
        "self_assessment_acceptable": False
    },
    "High": {
        "required": ["SOC 2 Type II"],
        "alternative": ["ISO 27001"],
        "recommended": ["Penetration Test"],
        "self_assessment_acceptable": False
    },
    "Medium": {
        "required": [],
        "one_of": ["SOC 2 Type II", "ISO 27001", "Penetration Test"],
        "self_assessment_acceptable": True,
        "self_assessment_note": "Acceptable if supplemented by one independent attestation"
    },
    "Low": {
        "required": [],
        "self_assessment_acceptable": True
    }
}


def check_vendor(vendor: dict, attestations: list) -> list:
    """Check a vendor's attestations against tier requirements."""
    findings = []
    tier = vendor.get("tier", "Unknown")
    name = vendor.get("vendor_name", "Unknown")
    reqs = TIER_REQUIREMENTS.get(tier, {})

    # Get this vendor's attestation types
    vendor_attestations = [a["report_type"] for a in attestations if a["vendor"] == name]

    # Check required
    for req in reqs.get("required", []):
        if req not in vendor_attestations:
            findings.append(f"[{name}] MISSING REQUIRED: {req} (Tier: {tier})")

    # Check one-of for Medium
    one_of = reqs.get("one_of", [])
    if one_of and not any(r in vendor_attestations for r in one_of):
        findings.append(f"[{name}] MISSING: Need at least one of {one_of} (Tier: {tier})")

    # Check for expired/stale
    for att in attestations:
        if att["vendor"] == name and att.get("validation_status") == "CONDITIONAL":
            findings.append(f"[{name}] CONDITIONAL: {att['report_type']} — review findings")

    return findings


def main():
    parser = argparse.ArgumentParser(description="Attestation Completeness Check")
    parser.add_argument("--register", required=True, help="Path to vendor risk register")
    parser.add_argument("--tracker", required=True, help="Path to attestation tracker")
    args = parser.parse_args()

    with open(args.register) as f:
        register = json.load(f)
    with open(args.tracker) as f:
        tracker = json.load(f)

    vendors = register.get("vendors", [])
    attestations = tracker.get("attestations", [])
    all_findings = []

    print(f"{'='*60}")
    print(f"  ATTESTATION COMPLETENESS CHECK")
    print(f"  Vendors: {len(vendors)} | Attestations: {len(attestations)}")
    print(f"{'='*60}")
    print()

    for vendor in vendors:
        findings = check_vendor(vendor, attestations)
        all_findings.extend(findings)
        name = vendor.get("vendor_name")
        tier = vendor.get("tier")
        if findings:
            print(f"  ✗ {name} ({tier})")
            for f_item in findings:
                print(f"    → {f_item}")
        else:
            print(f"  ✓ {name} ({tier})")

    print()
    print(f"{'─'*60}")
    if all_findings:
        print(f"  RESULT: {len(all_findings)} finding(s)")
        print(f"  STATUS: GAPS IDENTIFIED — review and remediate")
    else:
        print(f"  RESULT: All vendors meet attestation requirements")
        print(f"  STATUS: PASS")
    print(f"{'='*60}")

    sys.exit(1 if all_findings else 0)


if __name__ == "__main__":
    main()
