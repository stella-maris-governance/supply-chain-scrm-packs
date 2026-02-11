#!/usr/bin/env python3
"""
NTIA Minimum Element Validator — Stella Maris Governance
Validates SBOMs against EO 14028 / NTIA minimum element requirements.
An incomplete manifest grounds the aircraft.
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime

NTIA_ELEMENTS = [
    "supplier_name",
    "component_name",
    "version",
    "unique_identifier",
    "dependency_relationship",
    "sbom_author",
    "timestamp"
]


def validate_cyclonedx(sbom: dict) -> list:
    """Validate CycloneDX SBOM against NTIA elements."""
    findings = []

    # SBOM-level checks
    metadata = sbom.get("metadata", {})
    if not metadata.get("authors") and not metadata.get("manufacture"):
        findings.append("SBOM author: MISSING — no authors or manufacture in metadata")

    timestamp = metadata.get("timestamp", "")
    if not timestamp:
        findings.append("Timestamp: MISSING — no timestamp in metadata")
    else:
        try:
            datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except ValueError:
            findings.append(f"Timestamp: INVALID format — '{timestamp}'")

    # Component-level checks
    components = sbom.get("components", [])
    if not components:
        findings.append("Components: NONE — SBOM contains no components")
        return findings

    no_supplier = 0
    no_version = 0
    no_identifier = 0
    no_name = 0

    for comp in components:
        if not comp.get("name"):
            no_name += 1
        if not comp.get("version") or comp.get("version") in ("latest", "N/A", "unknown"):
            no_version += 1
        if not comp.get("supplier") and not comp.get("publisher") and not comp.get("author"):
            no_supplier += 1
        if not comp.get("purl") and not comp.get("cpe") and not comp.get("swid"):
            no_identifier += 1

    total = len(components)
    if no_name > 0:
        findings.append(f"Component name: {no_name}/{total} components missing name")
    if no_supplier > 0:
        findings.append(f"Supplier name: {no_supplier}/{total} components missing supplier/publisher/author")
    if no_version > 0:
        findings.append(f"Version: {no_version}/{total} components missing valid version")
    if no_identifier > 0:
        findings.append(f"Unique identifier: {no_identifier}/{total} components missing CPE/PURL/SWID")

    # Dependency relationship check
    dependencies = sbom.get("dependencies", [])
    if not dependencies:
        findings.append("Dependency relationships: MISSING — no dependency tree (flat list only)")

    return findings


def main():
    parser = argparse.ArgumentParser(description="NTIA Minimum Element Validator")
    parser.add_argument("--sbom", required=True, help="Path to SBOM file (CycloneDX JSON)")
    args = parser.parse_args()

    sbom_path = Path(args.sbom)
    if not sbom_path.exists():
        print(f"ERROR: SBOM not found: {sbom_path}")
        sys.exit(1)

    with open(sbom_path) as f:
        sbom = json.load(f)

    # Detect format
    if "bomFormat" in sbom and sbom["bomFormat"] == "CycloneDX":
        findings = validate_cyclonedx(sbom)
    else:
        print("WARNING: Non-CycloneDX format detected. Limited validation.")
        findings = ["Format: Not CycloneDX — convert to CycloneDX for full validation"]

    components = sbom.get("components", [])
    vendor = sbom.get("metadata", {}).get("component", {}).get("name", "Unknown")

    print(f"{'='*60}")
    print(f"  NTIA MINIMUM ELEMENT VALIDATION")
    print(f"  SBOM: {sbom_path.name}")
    print(f"  Source: {vendor}")
    print(f"  Components: {len(components)}")
    print(f"{'='*60}")
    print()

    if findings:
        for f_item in findings:
            print(f"  ✗ {f_item}")
        print()
        print(f"  RESULT: {len(findings)} finding(s)")
        print(f"  STATUS: FAIL — SBOM does not meet NTIA minimum elements")
    else:
        for elem in NTIA_ELEMENTS:
            print(f"  ✓ {elem.replace('_', ' ').title()}")
        print()
        print(f"  RESULT: All 7 NTIA elements validated")
        print(f"  STATUS: PASS")

    print(f"{'='*60}")
    sys.exit(1 if findings else 0)


if __name__ == "__main__":
    main()
