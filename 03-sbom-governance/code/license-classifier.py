#!/usr/bin/env python3
"""
License Classifier — Stella Maris Governance
Classifies SBOM component licenses and flags compliance risks.
"""

import json
import sys
import argparse
from pathlib import Path

LICENSE_CATEGORIES = {
    "permissive": [
        "MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC",
        "Unlicense", "CC0-1.0", "0BSD", "Zlib", "PSF-2.0"
    ],
    "copyleft": [
        "GPL-2.0-only", "GPL-2.0-or-later", "GPL-3.0-only", "GPL-3.0-or-later",
        "LGPL-2.1-only", "LGPL-2.1-or-later", "LGPL-3.0-only", "LGPL-3.0-or-later",
        "AGPL-3.0-only", "AGPL-3.0-or-later", "MPL-2.0", "EPL-2.0"
    ],
    "commercial": ["Commercial", "Proprietary", "EULA"],
    "public_domain": ["CC0-1.0", "Unlicense"]
}

AGPL_LICENSES = ["AGPL-3.0-only", "AGPL-3.0-or-later"]


def classify(license_id: str) -> dict:
    """Classify a license identifier."""
    if not license_id or license_id.lower() in ("unknown", "none", "noassertion", ""):
        return {"category": "unknown", "action": "INVESTIGATE", "risk": "high"}

    for category, licenses in LICENSE_CATEGORIES.items():
        if license_id in licenses:
            risk = "none" if category == "permissive" else "medium" if category == "copyleft" else "low"
            action = "OK" if category == "permissive" else "LEGAL REVIEW" if license_id in AGPL_LICENSES else "REVIEW"
            return {"category": category, "action": action, "risk": risk}

    # Check partial matches
    upper = license_id.upper()
    if "MIT" in upper or "APACHE" in upper or "BSD" in upper:
        return {"category": "permissive", "action": "OK", "risk": "none"}
    if "GPL" in upper:
        return {"category": "copyleft", "action": "REVIEW", "risk": "medium"}

    return {"category": "unknown", "action": "INVESTIGATE", "risk": "high"}


def main():
    parser = argparse.ArgumentParser(description="License Classifier")
    parser.add_argument("--register", required=True, help="Path to SBOM register")
    args = parser.parse_args()

    with open(args.register) as f:
        register = json.load(f)

    components = register.get("components", [])
    results = {"permissive": 0, "copyleft": 0, "commercial": 0, "unknown": 0, "public_domain": 0}
    flags = []

    for comp in components:
        license_id = comp.get("license", "")
        classification = classify(license_id)
        results[classification["category"]] = results.get(classification["category"], 0) + 1

        if classification["action"] in ("LEGAL REVIEW", "INVESTIGATE"):
            flags.append({
                "component": comp.get("name", "Unknown"),
                "version": comp.get("version", ""),
                "license": license_id,
                "action": classification["action"],
                "risk": classification["risk"]
            })

    total = len(components)
    print(f"{'='*60}")
    print(f"  LICENSE COMPLIANCE CLASSIFICATION")
    print(f"  Components: {total}")
    print(f"{'='*60}")
    print()
    print(f"  Permissive .... {results['permissive']:>4} ({results['permissive']/total*100:.0f}%)")
    print(f"  Copyleft ...... {results['copyleft']:>4} ({results['copyleft']/total*100:.0f}%)")
    print(f"  Commercial .... {results['commercial']:>4} ({results['commercial']/total*100:.0f}%)")
    print(f"  Unknown ....... {results['unknown']:>4} ({results['unknown']/total*100:.0f}%)")
    print()

    if flags:
        print(f"  ⚠ FLAGS ({len(flags)}):")
        for flag in flags:
            print(f"    {flag['component']}@{flag['version']} — {flag['license']} → {flag['action']}")

    print(f"{'='*60}")
    sys.exit(1 if results["unknown"] > total * 0.05 else 0)


if __name__ == "__main__":
    main()
