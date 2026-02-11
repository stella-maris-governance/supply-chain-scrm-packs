#!/usr/bin/env python3
"""
Concentration Risk Scanner — Stella Maris Governance
Detects shared Tier 2 dependencies across Tier 1 vendors.
A shared dependency is a single point of failure that multiplies blast radius.
"""

import json
import sys
import argparse
from collections import defaultdict
from datetime import datetime


def scan_shared_dependencies(entities: list) -> list:
    """Find Tier 2 entities serving multiple Tier 1 vendors."""
    entity_vendors = defaultdict(list)
    for entity in entities:
        entity_vendors[entity["entity_name"]].append(entity["tier1_vendor"])

    findings = []
    for entity_name, vendors in entity_vendors.items():
        if len(vendors) >= 2:
            findings.append({
                "type": "SHARED_DEPENDENCY",
                "entity": entity_name,
                "serves_vendors": vendors,
                "vendor_count": len(vendors),
                "severity": "HIGH" if len(vendors) >= 3 else "MEDIUM"
            })
    return findings


def scan_attestation_gaps(entities: list) -> list:
    """Find Tier 2 entities with no attestation serving Critical vendors."""
    findings = []
    for entity in entities:
        attestation = entity.get("attestation", "")
        if "NONE" in attestation.upper():
            findings.append({
                "type": "ATTESTATION_GAP",
                "entity": entity["entity_name"],
                "tier1_vendor": entity["tier1_vendor"],
                "service": entity["service"],
                "severity": "HIGH"
            })
    return findings


def scan_jurisdiction_risk(entities: list) -> list:
    """Flag Tier 2 entities in restricted or high-risk jurisdictions."""
    restricted = ["CN", "RU", "IR", "KP", "SY", "CU"]
    findings = []
    for entity in entities:
        for field in ["jurisdiction_incorporation", "jurisdiction_processing", "jurisdiction_storage"]:
            jurisdiction = entity.get(field, "")
            for code in restricted:
                if code.lower() in jurisdiction.lower():
                    findings.append({
                        "type": "JURISDICTION_RISK",
                        "entity": entity["entity_name"],
                        "tier1_vendor": entity["tier1_vendor"],
                        "jurisdiction_field": field,
                        "jurisdiction_value": jurisdiction,
                        "severity": "CRITICAL"
                    })
    return findings


def scan_low_confidence(entities: list) -> list:
    """Flag Tier 2 entities identified from low-confidence sources."""
    findings = []
    for entity in entities:
        if entity.get("confidence", "").lower() == "low":
            findings.append({
                "type": "LOW_CONFIDENCE",
                "entity": entity["entity_name"],
                "tier1_vendor": entity["tier1_vendor"],
                "source": entity.get("source", "Unknown"),
                "severity": "MEDIUM"
            })
    return findings


def scan_tier3_concentration(entities: list) -> list:
    """Detect shared Tier 3 infrastructure patterns."""
    tier3_vendors = defaultdict(list)
    for entity in entities:
        tier3 = entity.get("tier3_dependency", "")
        if tier3:
            tier3_vendors[tier3].append({
                "tier2": entity["entity_name"],
                "tier1": entity["tier1_vendor"]
            })

    findings = []
    for tier3, dependents in tier3_vendors.items():
        if len(dependents) >= 2:
            findings.append({
                "type": "TIER3_CONCENTRATION",
                "tier3_entity": tier3,
                "affected_chain": dependents,
                "severity": "MEDIUM"
            })
    return findings


def main():
    parser = argparse.ArgumentParser(description="Stella Maris Concentration Risk Scanner")
    parser.add_argument("--register", required=True, help="Path to tier2-register.json")
    args = parser.parse_args()

    with open(args.register) as f:
        register = json.load(f)

    entities = register.get("tier2_entities", [])

    print(f"{'='*65}")
    print(f"  CONCENTRATION RISK SCAN")
    print(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"  Tier 2 Entities: {len(entities)}")
    print(f"{'='*65}")
    print()

    all_findings = []

    # Run all scans
    scans = [
        ("Shared Dependencies", scan_shared_dependencies(entities)),
        ("Attestation Gaps", scan_attestation_gaps(entities)),
        ("Jurisdiction Risk", scan_jurisdiction_risk(entities)),
        ("Low Confidence Entries", scan_low_confidence(entities)),
        ("Tier 3 Concentration", scan_tier3_concentration(entities))
    ]

    for scan_name, findings in scans:
        print(f"  ─── {scan_name} ───")
        if findings:
            for f in findings:
                icon = "🔴" if f["severity"] == "CRITICAL" else "🟡" if f["severity"] == "HIGH" else "🟠"
                print(f"  {icon} [{f['severity']}] {f['type']}: {f.get('entity', f.get('tier3_entity', 'N/A'))}")
                for k, v in f.items():
                    if k not in ("type", "severity", "entity", "tier3_entity"):
                        print(f"      {k}: {v}")
            all_findings.extend(findings)
        else:
            print(f"  ✓ No findings")
        print()

    print(f"{'─'*65}")
    print(f"  TOTAL FINDINGS: {len(all_findings)}")
    critical = sum(1 for f in all_findings if f["severity"] == "CRITICAL")
    high = sum(1 for f in all_findings if f["severity"] == "HIGH")
    medium = sum(1 for f in all_findings if f["severity"] == "MEDIUM")
    print(f"  Critical: {critical} | High: {high} | Medium: {medium}")
    print(f"{'='*65}")

    sys.exit(1 if critical > 0 else 0)


if __name__ == "__main__":
    main()
