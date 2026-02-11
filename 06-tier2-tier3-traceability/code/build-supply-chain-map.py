#!/usr/bin/env python3
"""
Supply Chain Map Builder — Stella Maris Governance
Generates dependency chain visualization from Tier 2 register.
"""

import json
import argparse
from datetime import datetime


def build_mermaid_map(vendor_name: str, entities: list) -> str:
    """Generate Mermaid diagram for vendor's supply chain."""
    vendor_entities = [e for e in entities if e["tier1_vendor"] == vendor_name]

    if not vendor_entities:
        return f"graph TD\n    V1[\"{vendor_name}\"] --> NONE[\"No Tier 2 entities identified\"]"

    lines = ["graph TD"]
    lines.append(f'    V1["{vendor_name}"]')

    for i, entity in enumerate(vendor_entities):
        node_id = f"T2_{i}"
        name = entity["entity_name"]
        service = entity["service"]
        jurisdiction = entity.get("jurisdiction_processing", "Unknown")
        attestation = entity.get("attestation", "NONE")
        confidence = entity.get("confidence", "Unknown")

        # Style based on attestation
        if "NONE" in attestation.upper():
            style = f"style {node_id} fill:#fff3e0,stroke:#e65100"
        else:
            style = f"style {node_id} fill:#e3fcef,stroke:#36b37e"

        # Line style based on confidence
        arrow = "-->" if confidence != "Low" else "-.->"

        lines.append(f'    V1 {arrow} {node_id}["{name}<br/>{service}<br/>{jurisdiction}"]')
        lines.append(f"    {style}")

        # Tier 3 if present
        tier3 = entity.get("tier3_dependency", "")
        if tier3:
            t3_id = f"T3_{i}"
            lines.append(f'    {node_id} -.-> {t3_id}["{tier3}"]')
            lines.append(f"    style {t3_id} fill:#f5f6f8,stroke:#999")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Stella Maris Supply Chain Map Builder")
    parser.add_argument("--vendor", required=True, help="Tier 1 vendor name")
    parser.add_argument("--register", required=True, help="Path to tier2-register.json")
    parser.add_argument("--output", default=None, help="Output .mmd file")
    args = parser.parse_args()

    with open(args.register) as f:
        register = json.load(f)

    entities = register.get("tier2_entities", [])
    mermaid = build_mermaid_map(args.vendor, entities)

    print(f"{'='*60}")
    print(f"  SUPPLY CHAIN MAP: {args.vendor}")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"{'='*60}")
    print()
    print(mermaid)
    print()

    if args.output:
        with open(args.output, 'w') as f:
            f.write(mermaid)
        print(f"  Map written to {args.output}")

    print(f"{'='*60}")


if __name__ == "__main__":
    main()
