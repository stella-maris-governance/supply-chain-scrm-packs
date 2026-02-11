# SBOM Governance — Operations Runbook

> **Version:** 1.0.0 | **Author:** Robert Myers, MBA | Stella Maris Governance

---

## 1. Purpose and Scope

Operational procedures for generating, collecting, validating, and governing Software Bills of Materials. The SBOM is the parts manifest for your software supply chain.

**Scope:** All internally developed applications and all vendor-provided software classified as Critical or High in Pack 01.

**Out of Scope:** Hardware BOMs, firmware (unless software-defined), Low-tier vendor commodity tools.

---

## 2. Prerequisites

| Requirement | Detail |
|-------------|--------|
| CI/CD pipeline | GitHub Actions, Azure DevOps, or equivalent with plugin support |
| CycloneDX plugin | Installed for project language (npm, Maven, pip, dotnet, etc.) |
| SBOM register | `sbom-register.json` initialized |
| NTIA validator | `validate-ntia-elements.py` tested |
| Vulnerability feed | OSV API access configured |
| Pack 01 operational | Vendor tiers defined — drives SBOM requirement level |

---

## 3. Internal SBOM Generation

### 3.1 CI/CD Integration

Every merge to main triggers SBOM generation:
```yaml
# GitHub Actions example
- name: Generate SBOM
  uses: CycloneDX/gh-dotnet-generate-sbom@v1
  with:
    output: ./sbom/cyclonedx.json
    format: json
```

Adapt plugin for your stack: `@cyclonedx/npm` for Node, `cyclonedx-maven-plugin` for Java, `cyclonedx-bom` for Python.

### 3.2 Post-Build Validation

After SBOM generation, run NTIA validation as a pipeline step:
```bash
python3 validate-ntia-elements.py --sbom ./sbom/cyclonedx.json
```

If validation fails, the build should warn (not block) in non-production branches. In release branches, NTIA failure blocks the release.

### 3.3 Storage

- Store SBOMs in artifact repository alongside build artifacts
- Tag with build ID, commit hash, and timestamp
- Retain for minimum 3 years (matches most compliance requirements)

> **Watchstander Note:** An SBOM generated at build time is accurate. An SBOM generated after deployment is a reconstruction. Integrate at build. Always.

---

## 4. Vendor SBOM Collection

### 4.1 Request Process

1. During Pack 01 vendor intake or re-assessment, include SBOM request:
   - Critical vendors: SBOM required in CycloneDX or SPDX format
   - High vendors: SBOM requested
2. Provide vendor with format specification and NTIA minimum element list
3. Set 30-day response window
4. Log request date and response in SBOM register

### 4.2 Handling Non-Compliance

| Vendor Response | Action |
|----------------|--------|
| Valid SBOM provided | Validate, ingest, correlate |
| Non-standard format (Excel, PDF list) | Reject. Explain requirement. Re-request with format spec. |
| "On our roadmap" | Log. Score Subcontractor Risk at reduced credit. Re-request at next assessment. |
| No response | Log after 2 attempts. Score Subcontractor Risk at minimum. Escalate at contract renewal. |
| "Proprietary/confidential" | Document refusal. Score accordingly. Discuss NDA-protected disclosure. |

---

## 5. NTIA Validation

Run `validate-ntia-elements.py` on every SBOM before ingestion:
```bash
python3 validate-ntia-elements.py --sbom vendor-sbom.json
```

### Required Elements

| Element | Validation Rule |
|---------|----------------|
| Supplier name | Non-empty string. "Unknown" flagged as finding. |
| Component name | Non-empty string for every component. |
| Version | Non-empty. "latest" or "N/A" rejected. |
| Unique identifier | CPE, PURL, or SWID present. Required for CVE correlation. |
| Dependency relationship | Parent-child relationships mapped. Flat lists flagged. |
| SBOM author | Identified. Tool-generated acceptable. |
| Timestamp | ISO 8601. SBOMs without timestamps rejected. |

---

## 6. Vulnerability Correlation

### 6.1 Daily Scan
```bash
python3 correlate-vulnerabilities.py --register sbom-register.json
```

Checks all components against OSV database. Cross-references NVD for CVSS scoring.

### 6.2 Response by Severity

| Severity | SLA | Action |
|----------|-----|--------|
| Critical (9.0+) | 48 hours | Patch or mitigate. Escalate to CISO. Notify affected vendor relationship owners. |
| High (7.0-8.9) | 7 days | Patch in next maintenance window. Track in remediation register. |
| Medium (4.0-6.9) | 30 days | Patch in next release. Track. |
| Low (0.1-3.9) | 90 days | Track. Patch at convenience. |

### 6.3 Context Matters

Severity alone doesn't determine urgency:
- A critical CVE in a component your app doesn't invoke = lower urgency
- A medium CVE in a component that handles authentication = higher urgency
- A critical CVE in a vendor's SBOM = vendor notification + verification

> **Watchstander Note:** The CVE database tells you the severity. The SBOM tells you the exposure. You need both. A fire alarm without a floor plan doesn't help the firefighter find the fire.

---

## 7. License Compliance

### 7.1 Classification
```bash
python3 license-classifier.py --register sbom-register.json
```

### 7.2 Action by License Type

| License Type | Action |
|-------------|--------|
| Permissive (MIT, Apache 2.0, BSD) | No action. Compliant for all use. |
| Copyleft (GPL, LGPL) | Legal review if distributed. LGPL: verify dynamic linking. GPL: verify no distribution. |
| AGPL | Legal review required. AGPL triggers if service is network-accessible. |
| Commercial | Verify license terms on file. Confirm seat/usage compliance. |
| Unknown | Investigate. Contact author. If unresolved in 30 days, flag for component replacement. |

---

## 8. Review Cadence

| Review | Frequency | Owner |
|--------|-----------|-------|
| Vulnerability correlation | Daily (automated) | Security Lead |
| Critical CVE response | Within 48 hours of alert | Security Lead |
| SBOM register completeness | Monthly | Risk Owner |
| Vendor SBOM refresh check | Quarterly | Risk Owner |
| License compliance review | Quarterly | Risk Owner + Legal |
| Dependency depth review | Semi-annual | Engineering Lead |
| Full SBOM program review | Annual | Risk Owner + Leadership |

---

## 9. Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Internal SBOM coverage | 100% of production apps | 100% (3/3) |
| Vendor SBOM coverage (Critical/High) | 100% | 40% (2/5) |
| NTIA compliance rate | 100% of ingested SBOMs | 100% (5/5 validated) |
| Critical CVE response time | < 48 hours | 36 hours avg |
| Components with unknown license | < 5% | 2% (12/587) |

---

## 10. Troubleshooting

**CI/CD plugin doesn't capture all dependencies:** Ensure plugin is configured for the full dependency tree, not just direct dependencies. For npm: use `--include-dev`. For Maven: ensure transitive resolution is enabled.

**Vendor SBOM in wrong format:** Provide vendor with CycloneDX spec link and NTIA element list. Offer to accept SPDX as alternative. If vendor can only produce CSV/Excel, explain why structured format is required (dependency relationships, unique identifiers for CVE correlation).

**CVE correlation returns false positives:** Component is listed but not actually invoked by the application. Document as "present but not exploitable in this context." Track but deprioritize. Do not suppress — the component is still in the assembly.

**License classifier returns "Unknown":** Check SPDX license identifier in SBOM. If missing, check component repository (GitHub/npm/PyPI) for LICENSE file. If truly unlicensed open-source, contact maintainer or plan replacement.

---

*Stella Maris Governance — 2026*
