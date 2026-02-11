#!/usr/bin/env python3
"""
Blast Radius Assessment — Stella Maris Governance
Cross-pillar exposure assessment for vendor incidents.
Given a vendor name, determine all access paths, data exposure,
software components, and network connections.
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime


def assess_identity(vendor_name: str, access_register: dict) -> dict:
    """Assess vendor identity exposure from access register."""
    vendor_entries = [v for v in access_register.get("vendors", [])
                      if v.get("vendor_name") == vendor_name]
    if not vendor_entries:
        return {"status": "NOT FOUND", "exposure": "Unknown"}

    entry = vendor_entries[0]
    return {
        "status": "ASSESSED",
        "service_principals": entry.get("service_principals", 0),
        "guest_accounts": entry.get("guest_accounts", 0),
        "permissions_summary": entry.get("permissions", []),
        "pci_score": entry.get("pci_score", "N/A"),
        "last_activity": entry.get("last_activity", "Unknown")
    }


def assess_data(vendor_name: str, vendor_register: dict) -> dict:
    """Assess data exposure from Pack 01 vendor register."""
    vendor_entries = [v for v in vendor_register.get("vendors", [])
                      if v.get("vendor_name") == vendor_name]
    if not vendor_entries:
        return {"status": "NOT FOUND"}

    entry = vendor_entries[0]
    return {
        "status": "ASSESSED",
        "data_classification": entry.get("data_classification", "Unknown"),
        "data_types": entry.get("data_types", []),
        "integration_type": entry.get("integration_type", "Unknown"),
        "tier": entry.get("tier", "Unknown")
    }


def assess_software(vendor_name: str, sbom_register: dict) -> dict:
    """Assess software exposure from Pack 03 SBOM register."""
    vendor_sboms = [s for s in sbom_register.get("sboms", [])
                    if s.get("vendor") == vendor_name]
    if not vendor_sboms:
        return {"status": "NO SBOM", "exposure": "Unknown — SBOM not on file"}

    sbom = vendor_sboms[0]
    return {
        "status": "ASSESSED",
        "component_count": sbom.get("component_count", 0),
        "critical_cves": sbom.get("critical_cves", 0),
        "high_cves": sbom.get("high_cves", 0),
        "sbom_date": sbom.get("date", "Unknown")
    }


def assess_network(vendor_name: str, network_register: dict) -> dict:
    """Assess network exposure. Partially manual — see finding."""
    vendor_entries = [v for v in network_register.get("vendors", [])
                      if v.get("vendor_name") == vendor_name]
    if not vendor_entries:
        return {"status": "MANUAL ASSESSMENT REQUIRED"}

    entry = vendor_entries[0]
    return {
        "status": "ASSESSED",
        "vpn_tunnel": entry.get("vpn", False),
        "network_segments": entry.get("segments", []),
        "firewall_rules": entry.get("firewall_rules", 0)
    }


def assess_financial(vendor_name: str, vendor_register: dict) -> dict:
    """Assess financial exposure from contract data."""
    vendor_entries = [v for v in vendor_register.get("vendors", [])
                      if v.get("vendor_name") == vendor_name]
    if not vendor_entries:
        return {"status": "NOT FOUND"}

    entry = vendor_entries[0]
    return {
        "status": "ASSESSED",
        "contract_value": entry.get("contract_value", "Unknown"),
        "liability_cap": entry.get("liability_cap", "Unknown"),
        "cyber_insurance": entry.get("cyber_insurance", "Unknown")
    }


def main():
    parser = argparse.ArgumentParser(description="Stella Maris Blast Radius Assessment")
    parser.add_argument("--vendor", required=True, help="Vendor name to assess")
    parser.add_argument("--data-dir", default=".", help="Directory containing register files")
    args = parser.parse_args()

    data_dir = Path(args.data_dir)

    print(f"{'='*65}")
    print(f"  BLAST RADIUS ASSESSMENT: {args.vendor}")
    print(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"{'='*65}")
    print()

    # Load available registers
    def load_json(filename):
        path = data_dir / filename
        if path.exists():
            return json.load(open(path))
        return {}

    access_reg = load_json("vendor-access-register.json")
    vendor_reg = load_json("vendor-risk-register.json")
    sbom_reg = load_json("sbom-register.json")
    network_reg = load_json("network-register.json")

    pillars = {
        "1. Identity": assess_identity(args.vendor, access_reg),
        "2. Data": assess_data(args.vendor, vendor_reg),
        "3. Software": assess_software(args.vendor, sbom_reg),
        "4. Network": assess_network(args.vendor, network_reg),
        "5. Financial": assess_financial(args.vendor, vendor_reg)
    }

    for pillar_name, result in pillars.items():
        status = result.get("status", "UNKNOWN")
        icon = "✓" if status == "ASSESSED" else "⚠" if "MANUAL" in status else "✗"
        print(f"  {icon} {pillar_name}: {status}")
        for key, value in result.items():
            if key != "status":
                print(f"      {key}: {value}")
        print()

    print(f"{'='*65}")
    print(f"  Contain first. Investigate second. Document everything.")
    print(f"{'='*65}")


if __name__ == "__main__":
    main()
