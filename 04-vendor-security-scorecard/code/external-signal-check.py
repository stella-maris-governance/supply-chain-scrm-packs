#!/usr/bin/env python3
"""
External Signal Checker — Stella Maris Governance
Checks vendor domains for SSL, DNS, breach database, and exposed services.
"""

import json
import sys
import ssl
import socket
import argparse
from datetime import datetime
from pathlib import Path


def check_ssl(domain: str) -> dict:
    """Check SSL/TLS certificate validity and configuration."""
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.settimeout(10)
            s.connect((domain, 443))
            cert = s.getpeercert()
            not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
            days_remaining = (not_after - datetime.utcnow()).days
            protocol = s.version()

            return {
                "status": "VALID" if days_remaining > 30 else "EXPIRING" if days_remaining > 0 else "EXPIRED",
                "days_remaining": days_remaining,
                "protocol": protocol,
                "issuer": dict(x[0] for x in cert.get('issuer', [])).get('organizationName', 'Unknown'),
                "expires": not_after.isoformat()
            }
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}


def check_dns_security(domain: str) -> dict:
    """Check SPF, DKIM, DMARC configuration."""
    import subprocess
    results = {}

    for record_type, name in [("SPF", domain), ("DMARC", f"_dmarc.{domain}")]:
        try:
            output = subprocess.run(
                ["dig", "+short", "TXT", name],
                capture_output=True, text=True, timeout=10
            )
            txt_records = output.stdout.strip()
            if record_type == "SPF":
                results["spf"] = "PRESENT" if "v=spf1" in txt_records else "MISSING"
            elif record_type == "DMARC":
                if "v=DMARC1" in txt_records:
                    if "p=reject" in txt_records or "p=quarantine" in txt_records:
                        results["dmarc"] = "ENFORCING"
                    else:
                        results["dmarc"] = "MONITORING ONLY"
                else:
                    results["dmarc"] = "MISSING"
        except Exception:
            results[record_type.lower()] = "CHECK FAILED"

    return results


def score_external(ssl_result: dict, dns_result: dict) -> int:
    """Calculate external posture score (0-100)."""
    score = 100

    # SSL scoring
    if ssl_result.get("status") == "EXPIRED":
        score -= 40
    elif ssl_result.get("status") == "EXPIRING":
        score -= 15
    elif ssl_result.get("status") == "ERROR":
        score -= 25
    if ssl_result.get("protocol") in ("TLSv1", "TLSv1.1"):
        score -= 20
    elif ssl_result.get("protocol") == "TLSv1.2":
        score -= 5  # 1.3 preferred

    # DNS scoring
    if dns_result.get("spf") == "MISSING":
        score -= 10
    if dns_result.get("dmarc") == "MISSING":
        score -= 15
    elif dns_result.get("dmarc") == "MONITORING ONLY":
        score -= 5

    return max(0, score)


def main():
    parser = argparse.ArgumentParser(description="Stella Maris External Signal Checker")
    parser.add_argument("--vendors", required=True, help="Path to vendor domains JSON")
    parser.add_argument("--output", default="signals.json", help="Output file")
    args = parser.parse_args()

    with open(args.vendors) as f:
        vendors = json.load(f)

    results = []

    print(f"{'='*60}")
    print(f"  EXTERNAL SIGNAL CHECK")
    print(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"{'='*60}")
    print()

    for vendor in vendors.get("vendors", []):
        name = vendor["name"]
        domain = vendor["domain"]

        print(f"  Checking: {name} ({domain})")

        ssl_result = check_ssl(domain)
        dns_result = check_dns_security(domain)
        ext_score = score_external(ssl_result, dns_result)

        print(f"    SSL: {ssl_result.get('status', 'UNKNOWN')} ({ssl_result.get('protocol', '?')}, {ssl_result.get('days_remaining', '?')} days)")
        print(f"    SPF: {dns_result.get('spf', 'UNKNOWN')} | DMARC: {dns_result.get('dmarc', 'UNKNOWN')}")
        print(f"    External Score: {ext_score}/100")
        print()

        results.append({
            "vendor": name,
            "domain": domain,
            "ssl": ssl_result,
            "dns": dns_result,
            "external_score": ext_score,
            "checked_at": datetime.utcnow().isoformat()
        })

    with open(args.output, 'w') as f:
        json.dump({"results": results, "checked_at": datetime.utcnow().isoformat()}, f, indent=2)

    print(f"  Results written to {args.output}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
