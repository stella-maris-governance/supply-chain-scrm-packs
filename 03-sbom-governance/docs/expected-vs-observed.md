# The Law of Evidence: Expected vs. Observed

## Software Bill of Materials (SBOM) Governance

> **Assessment Date:** 2026-02-11 [SAMPLE — replace with your assessment date]
> **Environment:** Stella Maris Lab — CI/CD Pipeline + SBOM Register [SAMPLE]
> **Assessor:** Robert Myers, MBA | SailPoint ISL, Security+, CCSK, CC
> **Pack Version:** 1.0.0
> **Status:** 8/10 controls confirmed | 1 partial | 1 fail

---

## Summary

| Status | Count | Percentage |
|--------|-------|------------|
| Pass | 8 | 80% |
| Partial | 1 | 10% |
| Fail | 1 | 10% |

---

## Assessment Detail

### 1 — SBOM Generation Integrated into CI/CD Pipeline

| Field | Detail |
|-------|--------|
| **Expected State** | CycloneDX SBOM generation integrated into CI/CD pipeline. Every build produces a current SBOM automatically. No manual generation. |
| **Observed State** | CycloneDX plugin **integrated** into GitHub Actions pipeline for 3 internal applications. SBOM generated automatically on every merge to main. Format: CycloneDX 1.5 JSON. SBOMs stored in artifact repository with build correlation ID. **47 SBOMs generated** in 30 days across 3 applications. Average component count: App-1 (142 components), App-2 (89 components), App-3 (211 components). All SBOMs include NTIA minimum elements by default (validated by `validate-ntia-elements.py` as post-build check). |
| **Evidence** | CI/CD pipeline logs, Screenshot #01 |
| **NIST 800-161** | SR-4 |
| **Status** | **Pass** |

---

### 2 — NTIA Minimum Element Validation Operational

| Field | Detail |
|-------|--------|
| **Expected State** | Every SBOM — internal or vendor-provided — validated against NTIA minimum elements before ingestion. Incomplete SBOMs rejected with specific findings. |
| **Observed State** | `validate-ntia-elements.py` **operational** as automated gate. Validates 7 NTIA elements: supplier name, component name, version, unique identifier (CPE/PURL), dependency relationship, SBOM author, timestamp. **Internal SBOMs:** All 47 pass (CI/CD plugin generates compliant output by default). **Vendor SBOMs:** 3 received, 2 pass, 1 fail. CloudPlatform Corp (CycloneDX, PASS): all elements present, 312 components, full dependency tree. SecureDefend Tools (SPDX, PASS): all elements present, 178 components, converted to CycloneDX for internal consistency. IdentityFirst Inc (FAIL): provided a "component list" in Excel — not a valid SBOM format. Missing: unique identifiers, dependency relationships, SBOM author, timestamp. Rejected. Finding logged. |
| **Evidence** | `validate-ntia-elements.py` output, Screenshot #02 |
| **EO 14028** | Sec 4(e) |
| **Status** | **Pass** |

---

### 3 — Vendor SBOM Collection by Tier

| Field | Detail |
|-------|--------|
| **Expected State** | SBOMs requested from all Critical and High vendors per tier requirements. Collection status tracked. Non-provision documented and scored. |
| **Observed State** | **Critical vendors (2):** CloudPlatform Corp — SBOM received and validated (PASS). IdentityFirst Inc — "component list" received, rejected as non-compliant, formal SBOM re-requested with CycloneDX/SPDX format requirement. **High vendors (3):** SecureDefend Tools — SBOM received and validated (PASS). HR-Cloud SaaS — vendor responded "SBOM generation is on our 2026 roadmap." No SBOM. BackupVault Pro — no response after 2 requests. **Collection rate:** 2 of 5 Critical/High vendors provided valid SBOMs (40%). 1 provided non-compliant format. 2 have not provided. Non-provision findings fed to Pack 01 Subcontractor Risk domain. |
| **Evidence** | SBOM register, vendor correspondence log |
| **NIST 800-161** | SR-4 |
| **Status** | **Pass** |

---

### 4 — Component Inventory Centralized

| Field | Detail |
|-------|--------|
| **Expected State** | All SBOM components aggregated into a centralized inventory. Inventory queryable by component name, version, license, and presence across applications/vendors. |
| **Observed State** | Component inventory **built** from 5 validated SBOMs (3 internal + 2 vendor). **Total unique components: 587.** Breakdown: 312 from CloudPlatform Corp, 178 from SecureDefend Tools, 142/89/211 from internal apps (with significant overlap). **Top shared components:** lodash (present in 4 of 5 SBOMs), axios (3 of 5), OpenSSL (3 of 5), jackson-databind (2 of 5). Inventory stored in JSON register, queryable by component, version, source, license. |
| **Evidence** | `sbom-register.json`, Screenshot #01 |
| **NIST 800-53** | CM-8 |
| **Status** | **Pass** |

---

### 5 — Vulnerability Correlation Operational

| Field | Detail |
|-------|--------|
| **Expected State** | All components in inventory correlated against OSV and NVD databases. Known CVEs mapped to affected components with severity classification. Critical CVEs trigger immediate notification. |
| **Observed State** | `correlate-vulnerabilities.py` **operational.** Runs daily against OSV database (primary) with NVD cross-reference. **Current findings across 587 components:** 3 critical CVEs (CVSS 9.0+): 1 in jackson-databind (CVE-2025-XXXXX, deserialization RCE, present in App-2 and SecureDefend Tools), 1 in OpenSSL (CVE-2025-XXXXX, buffer overflow, present in App-1 and CloudPlatform Corp), 1 in log4j-core (CVE-2021-44228 residual, present in App-3 legacy dependency). 7 high CVEs (CVSS 7.0-8.9): distributed across 5 components. 14 medium CVEs. 22 low CVEs. **Critical CVE response:** jackson-databind patched in App-2 within 36 hours (within 48-hour SLA). OpenSSL — CloudPlatform Corp confirmed patched in their infrastructure (verified via vendor advisory). log4j-core — App-3 legacy dependency identified, migration to log4j 2.21+ initiated, ETA 2 weeks. |
| **Evidence** | `correlate-vulnerabilities.py` output, Screenshot #03 |
| **NIST 800-53** | RA-5 |
| **Status** | **Pass** |

---

### 6 — License Compliance Classification Complete

| Field | Detail |
|-------|--------|
| **Expected State** | All components classified by license type. Copyleft licenses flagged for legal review. Unknown licenses escalated. License conflicts identified. |
| **Observed State** | `license-classifier.py` **operational.** Classification across 587 components: **Permissive (MIT, Apache 2.0, BSD):** 412 components (70%). No action required. **Copyleft (GPL, LGPL, AGPL):** 38 components (6.5%). 2 AGPL components flagged for legal review — both in internal App-3, confirmed as development-only dependencies not distributed to customers. LGPL components confirmed as dynamically linked (compliant). **Commercial:** 84 components (14.3%). License terms on file. **Unknown/No License:** 53 components (9%). 41 are internal/proprietary (acceptable). **12 open-source components with no identifiable license** — finding logged, traced to 3 vendor SBOMs. Authors contacted for clarification. |
| **Evidence** | `license-classifier.py` output, Screenshot #05 |
| **EO 14028** | Sec 4(e) |
| **Status** | **Pass** |

---

### 7 — Dependency Depth Analysis Completed

| Field | Detail |
|-------|--------|
| **Expected State** | Transitive dependencies mapped for all internal applications. Maximum dependency depth tracked. Deep dependency chains (> 5 levels) flagged for review — these are the Tier 3 and Tier 4 suppliers of your software supply chain. |
| **Observed State** | Dependency tree analysis **completed** for 3 internal applications. **App-1:** Max depth 4. No concern. **App-2:** Max depth 7. One chain: app → spring-boot → spring-core → commons-logging → log4j-api → log4j-core → jackson-databind. The jackson-databind critical CVE was 6 levels deep — invisible without dependency depth analysis. **App-3:** Max depth 9. Legacy application with deep transitive chains. 3 chains exceed depth 5. Flagged for dependency cleanup in next refactoring cycle. **Key finding:** The most critical vulnerability in the assessment (jackson-databind RCE) was a transitive dependency 6 levels deep. Without SBOM dependency mapping, it would not have been discovered until exploitation. |
| **Evidence** | Screenshot #04 |
| **NIST 800-161** | SR-4(2) |
| **Status** | **Pass** |

---

### 8 — Critical CVE Alerting Configured

| Field | Detail |
|-------|--------|
| **Expected State** | When a new critical CVE is published that affects any component in the inventory, immediate notification to security lead. Impact assessment within 4 hours. |
| **Observed State** | Alert pipeline **configured:** OSV API polled every 6 hours → new CVEs matched against component inventory → critical/high matches trigger email + Teams notification to security lead. **2 critical alerts fired** in 30 days: (1) jackson-databind — alerted within 6 hours of OSV publication, impact assessment completed in 2 hours, patch deployed in 36 hours. (2) OpenSSL — alerted within 6 hours, impact assessment in 3 hours, vendor confirmation of patch received within 24 hours. Both within SLA. |
| **Evidence** | Alert logs, Screenshot #03 |
| **NIST 800-53** | RA-5 |
| **Status** | **Pass** |

---

### 9 — Vendor SBOM Gaps Scored in Pack 01

| Field | Detail |
|-------|--------|
| **Expected State** | Vendors who cannot provide valid SBOMs receive reduced Subcontractor Risk domain scores in Pack 01. The math handles the consequence. |
| **Observed State** | **3 vendor SBOM gaps** identified and scored: IdentityFirst Inc — non-compliant SBOM (Excel, not CycloneDX/SPDX). Subcontractor Risk domain: reduced from 60 to 40. Overall score impact: 77 → 75. HR-Cloud SaaS — no SBOM, "on roadmap." Subcontractor Risk domain: reduced from 50 to 25. Overall score impact: 72 → 69.5. BackupVault Pro — no response. Subcontractor Risk domain: reduced from 40 to 15. Overall score impact: 69 → 66.5. All score changes reflected in Pack 01 vendor risk register. `calculate_risk.py` re-run confirmed. |
| **Evidence** | Pack 01 register, scoring output |
| **NIST 800-161** | SR-6 |
| **Status** | **Pass** |

---

### 10 — Vendor-Provided SBOM Freshness Governance

| Field | Detail |
|-------|--------|
| **Expected State** | Vendor SBOMs refreshed with every major release or quarterly (whichever is more frequent) for Critical vendors. Stale SBOMs (> 6 months without update) flagged. SBOM register tracks last received date and next expected date. |
| **Observed State** | SBOM register **tracks** refresh dates for 2 validated vendor SBOMs. CloudPlatform Corp: last SBOM dated Jan 2026, next expected Apr 2026 (quarterly). SecureDefend Tools: last SBOM dated Dec 2025, next expected at next major release (no release schedule provided). |
| **Finding** | Only 2 of 5 Critical/High vendors have validated SBOMs in the register. Freshness governance cannot be fully enforced when 60% of vendors have not provided initial SBOMs. The process is designed and operational for the SBOMs we have, but the coverage gap is the constraint. Additionally, SecureDefend Tools has no defined refresh trigger — their SBOM ages until they release. Compensating control: re-request at 6-month mark if no release. |
| **Status** | **Fail** — process operational but vendor coverage too low to claim effective governance |

---

## Remediation Tracker

| # | Control | Finding | Owner | Remediation | Target Date | Status |
|---|---------|---------|-------|-------------|-------------|--------|
| 3 | Vendor SBOM collection | 3 of 5 Critical/High vendors have not provided valid SBOMs | R. Myers | Escalate SBOM requirement in next vendor re-assessment. Include SBOM clause in contract renewals. | 2026-Q2 | Open |
| 6 | License compliance | 12 open-source components with no identifiable license | R. Myers | Contact component authors. If unresolved, flag for replacement. | 2026-03-15 | Open |
| 10 | SBOM freshness | 60% vendor SBOM coverage gap prevents effective freshness governance | R. Myers | Tie SBOM provision to contract renewal gate for Critical vendors | 2026-Q2 | Open |

---

## Watchstander Notes

1. **The jackson-databind finding proves the model.** A critical RCE vulnerability was hiding 6 dependency levels deep. Without SBOM dependency mapping, it would have been invisible until an attacker found it first. This is the digital equivalent of a counterfeit bolt buried in a sub-assembly — undetectable by surface inspection. The SBOM is the X-ray.

2. **Vendors will resist.** 3 of 5 Critical/High vendors didn't provide valid SBOMs. One gave us an Excel spreadsheet. One said "it's on our roadmap." One didn't respond. This is the current reality of software supply chain governance in 2026. The discipline isn't universal yet. But the scoring model handles it: no SBOM means a lower score, which means a harder conversation at re-assessment. The math creates the incentive.

3. **The honest fail on Control 10 matters.** I could have marked it partial. The process is built, tested, and operational for the SBOMs we have. But claiming "freshness governance" when only 40% of Critical/High vendors are in the register is not honest. The control is operational. The coverage is not. That distinction matters. An auditor trusts the assessor who marks a fail and explains why more than the assessor who marks a pass and hides the gap.

4. **Transitive dependencies are Tier 2/3 suppliers.** When your application depends on library A, which depends on library B, which depends on library C — library C is your Tier 3 software supplier. You didn't choose it. You didn't vet it. You didn't even know it existed. The SBOM makes it visible. Pack 06 (Tier 2/3 Traceability) governs the organizational equivalent. This pack governs the code equivalent. Same principle, different domain.

---

*Assessment conducted by Robert Myers, MBA | SailPoint ISL, Security+, CCSK, CC*
*Stella Maris Governance — 2026*
