#!/usr/bin/env python3
"""
SBOM Vulnerability Correlator — Stella Maris Governance
Checks SBOM components against OSV database for known CVEs.
The CVE database tells you the severity. The SBOM tells you the exposure.
"""

import json
import sys
import argparse
from pathlib import Path

# In production, this would call the OSV API: https://api.osv.dev/v1/query
# This implementation reads from a local vulnerability feed for lab/demo

SEVERITY_THRESHOLDS = {
    "CRITICAL": {"min": 9.0, "sla_hours": 48},
    "HIGH": {"min": 7.0, "sla_hours": 168},
    "MEDIUM": {"min": 4.0, "sla_hours": 720},
    "LOW": {"min": 0.1, "sla_hours": 2160}
}


def classify_severity(cvss: float) -> str:
    """Classify CVSS score into severity."""
    for level, config in SEVERITY_THRESHOLDS.items():
        if cvss >= config["min"]:
            return level
    return "NONE"


def correlate(components: list, vuln_feed: list) -> list:
    """Match components against vulnerability feed."""
    findings = []
    for vuln in vuln_feed:
        affected_package = vuln.get("package", "")
        affected_versions = vuln.get("affected_versions", [])

        for comp in components:
            comp_name = comp.get("name", "").lower()
            comp_version = comp.get("version", "")

            if comp_name == affected_package.lower():
                if comp_version in affected_versions or "*" in affected_versions:
                    findings.append({
                        "component": comp_name,
                        "version": comp_version,
                        "cve": vuln.get("cve", "Unknown"),
                        "cvss": vuln.get("cvss", 0),
                        "severity": classify_severity(vuln.get("cvss", 0)),
                        "description": vuln.get("description", ""),
                        "sources": comp.get("sources", [])
                    })
    return findings


def main():
    parser = argparse.ArgumentParser(description="SBOM Vulnerability Correlator")
    parser.add_argument("--register", required=True, help="Path to SBOM register")
    parser.add_argument("--feed", default="vuln-feed.json", help="Path to vulnerability feed")
    args = parser.parse_args()

    register_path = Path(args.register)
    if not register_path.exists():
        print(f"ERROR: Register not found: {register_path}")
        sys.exit(1)

    with open(register_path) as f:
        register = json.load(f)

    components = register.get("components", [])

    # Load vulnerability feed (in production: call OSV API)
    feed_path = Path(args.feed)
    vuln_feed = []
    if feed_path.exists():
        with open(feed_path) as f:
            vuln_feed = json.load(f).get("vulnerabilities", [])

    findings = correlate(components, vuln_feed)

    print(f"{'='*60}")
    print(f"  SBOM VULNERABILITY CORRELATION")
    print(f"  Components scanned: {len(components)}")
    print(f"  Vulnerabilities in feed: {len(vuln_feed)}")
    print(f"{'='*60}")
    print()

    if findings:
        critical = [f for f in findings if f["severity"] == "CRITICAL"]
        high = [f for f in findings if f["severity"] == "HIGH"]
        medium = [f for f in findings if f["severity"] == "MEDIUM"]
        low = [f for f in findings if f["severity"] == "LOW"]

        if critical:
            print(f"  🔴 CRITICAL ({len(critical)}):")
            for f_item in critical:
                print(f"     {f_item['component']}@{f_item['version']} — {f_item['cve']} (CVSS {f_item['cvss']})")
        if high:
            print(f"  🟠 HIGH ({len(high)}):")
            for f_item in high:
                print(f"     {f_item['component']}@{f_item['version']} — {f_item['cve']} (CVSS {f_item['cvss']})")
        if medium:
            print(f"  🟡 MEDIUM ({len(medium)})")
        if low:
            print(f"  🟢 LOW ({len(low)})")
    else:
        print(f"  ✓ No known vulnerabilities found")

    print()
    print(f"{'─'*60}")
    total = len(findings)
    print(f"  TOTAL: {total} finding(s)")
    print(f"{'='*60}")

    sys.exit(1 if critical else 0)


if __name__ == "__main__":
    main()
