# The Law of Evidence: Expected vs. Observed

## Third-Party Attestation Validation

> **Assessment Date:** 2026-02-11 [SAMPLE — replace with your assessment date]
> **Environment:** Stella Maris Lab — Attestation Register [SAMPLE]
> **Assessor:** Robert Myers, MBA | SailPoint ISL, Security+, CCSK, CC
> **Pack Version:** 1.0.0
> **Status:** 8/10 controls confirmed | 2 partial | 0 failed

---

## Summary

| Status | Count | Percentage |
|--------|-------|------------|
| Pass | 8 | 80% |
| Partial | 2 | 20% |
| Fail | 0 | 0% |

---

## Assessment Detail

### 1 — Attestation Requirements Defined by Vendor Tier

| Field | Detail |
|-------|--------|
| **Expected State** | Minimum attestation requirements documented for each vendor tier. Critical and High vendors require independent attestation. Medium vendors require at least one independent report. Low vendors accept self-assessment with spot verification. |
| **Observed State** | Requirements **documented and approved** in vendor risk policy. Critical: SOC 2 Type II (validated) + annual pen test (full report) + financial attestation. High: SOC 2 Type II or ISO 27001 (validated) + pen test summary. Medium: one independent attestation or supplemented self-assessment. Low: self-assessment accepted. **All 5 Critical/High vendors** have attestation requirements assigned. 5 Medium vendors have requirements assigned. 2 Low vendors documented as self-assessment only. |
| **Evidence** | Policy document, attestation tracker |
| **NIST 800-161** | SR-6 |
| **Status** | **Pass** |

---

### 2 — Attestation Tracker Deployed and Populated

| Field | Detail |
|-------|--------|
| **Expected State** | Centralized tracker logs every attestation received: vendor, report type, issue date, expiry date, validation status, findings, CUEC status, and auditor identity. Tracker validated for completeness weekly. |
| **Observed State** | Tracker **deployed** with 9 attestation records across 5 Critical/High vendors. Records include: CloudPlatform Corp (SOC 2 Type II + pen test), IdentityFirst Inc (ISO 27001 + pen test), HR-Cloud SaaS (SOC 2 Type II), SecureDefend Tools (SOC 2 Type II + ISO 27001), BackupVault Pro (SOC 2 Type II). `validate-attestation-completeness.py` confirms all Critical/High vendors meet minimum attestation requirements. **0 gaps** for Critical/High vendors. |
| **Evidence** | `attestation-tracker.json`, Screenshot #01 |
| **NIST 800-53** | SA-9 |
| **Status** | **Pass** |

---

### 3 — SOC 2 Type II Reports Validated (15-Point Checklist)

| Field | Detail |
|-------|--------|
| **Expected State** | Every SOC 2 Type II report received undergoes 15-point structured validation. Results documented with findings per checkpoint. |
| **Observed State** | **4 SOC 2 Type II reports** validated using `soc2-validation-checklist.json`. Results: **CloudPlatform Corp (PASS, 15/15):** Report dated Jun 2025, 12-month observation period, Big 4 auditor, scope covers exact services used (US-EAST-1, US-WEST-2), all 5 trust criteria included, no subservice carve-outs, 0 exceptions, no qualified opinions, 3 CUECs identified (MFA, log review, encryption), bridging letter on file. **HR-Cloud SaaS (CONDITIONAL, 12/15):** Report dated Mar 2025, scope covers HR module but NOT the payroll integration added in Q3 2025 (scope mismatch finding), 2 exceptions noted (backup recovery test failed once, access review delayed), management response documented, no bridging letter — report is 11 months old, approaching stale threshold. **SecureDefend Tools (PASS, 14/15):** Report dated Sep 2025, scope covers all modules, 1 minor exception (terminated user access removal exceeded 24-hour SLA by 3 hours), management response adequate, 2 CUECs identified. **BackupVault Pro (CONDITIONAL, 11/15):** Report dated Jan 2025, 13 months old (STALE), scope covers backup service but carves out the encryption key management subservice organization, 3 exceptions noted, management response addresses 2 of 3. |
| **Evidence** | Completed checklists, Screenshot #02 |
| **NIST 800-53** | SA-9, SA-4 |
| **Status** | **Pass** |

---

### 4 — ISO 27001 Certificates Validated (10-Point Checklist)

| Field | Detail |
|-------|--------|
| **Expected State** | Every ISO 27001 certificate undergoes 10-point validation. Statement of Applicability (SoA) reviewed for excluded controls. Certification body accreditation verified. |
| **Observed State** | **2 ISO 27001 certificates** validated. **IdentityFirst Inc (CONDITIONAL, 8/10):** Certificate current (issued Nov 2024, expires Nov 2027), BSI accredited by UKAS, scope covers identity platform services, SoA reviewed — excludes A.11 (physical security, acceptable for cloud-native) and A.8.1 (mobile device management, finding — relevant to endpoint access). Surveillance audit completed Oct 2025, 1 minor nonconformity (incident response notification SLA documentation gap). Transitioned to ISO 27001:2022. **SecureDefend Tools (PASS, 10/10):** Certificate current, ANAB-accredited body, scope covers all security products, SoA complete with no relevant exclusions, surveillance audit clean, transitioned to 2022 version. |
| **Evidence** | Completed checklists, certificates on file |
| **NIST 800-161** | SR-6 |
| **Status** | **Pass** |

---

### 5 — Penetration Test Reports Validated (12-Point Checklist)

| Field | Detail |
|-------|--------|
| **Expected State** | Pen test reports for Critical/High vendors validated using 12-point checklist. Methodology, scope, findings severity, and remediation status assessed. |
| **Observed State** | **3 pen test reports** validated. **CloudPlatform Corp (PASS, 12/12):** CREST-certified tester, OWASP methodology, external + internal + API in scope, 0 critical, 2 high (both remediated + re-tested), 4 medium (3 remediated, 1 accepted with compensating control), full technical report provided, social engineering not in scope (documented). **IdentityFirst Inc (CONDITIONAL, 9/12):** OSCP-certified tester, external + web app in scope but API not tested (scope gap), 0 critical, 1 high (remediated), 3 medium (2 remediated, 1 open with timeline), executive summary only — full report requested, not yet received. **HR-Cloud SaaS: No pen test report provided.** Vendor states annual test completed but report is "confidential." Finding logged — High-tier vendor must provide at minimum a summary. |
| **Evidence** | Completed checklists, Screenshot #02 |
| **NIST 800-53** | SA-4 |
| **Status** | **Pass** |

---

### 6 — Stale and Expired Attestations Identified

| Field | Detail |
|-------|--------|
| **Expected State** | All attestations tracked by expiry. Reports 12-14 months old flagged as stale. Reports 14+ months flagged as expired. KQL scan runs weekly to catch approaching expirations. |
| **Observed State** | `attestation-expiry-scan.kql` **active** since Jan 20, runs weekly. Current state: 7 of 9 attestations current (< 12 months), 1 stale (BackupVault Pro SOC 2: 13 months — renewal requested, vendor confirms new report due Mar 2026), 1 approaching stale (HR-Cloud SaaS SOC 2: 11 months — 60-day warning triggered). **0 expired attestations.** 60-day advance warning notifications configured via Power Automate to vendor relationship owner. |
| **Evidence** | Screenshot #04, KQL output |
| **NIST 800-161** | SR-3 |
| **Status** | **Pass** |

---

### 7 — Scope Mismatch Findings Documented

| Field | Detail |
|-------|--------|
| **Expected State** | Every attestation validated for scope alignment: does the report cover the specific services, locations, and infrastructure your organization uses? Mismatches documented as findings. |
| **Observed State** | **2 scope mismatch findings** identified: (1) HR-Cloud SaaS SOC 2 does not cover payroll integration added Q3 2025 — vendor notified, updated report requested for next cycle. (2) BackupVault Pro SOC 2 carves out encryption key management subservice organization — compensating control: SMG manages encryption keys directly, documented in Pack 01 risk register. Both findings fed back to Pack 01 Compliance Status domain scores. HR-Cloud dropped from 75 to 72. BackupVault dropped from 74 to 69. |
| **Evidence** | Validation checklists, Pack 01 score adjustments |
| **NIST 800-53** | SA-9(2) |
| **Status** | **Pass** |

---

### 8 — CUEC Gap Analysis Completed

| Field | Detail |
|-------|--------|
| **Expected State** | Every SOC 2 report's Complementary User Entity Controls (CUECs) mapped to our internal control environment. Gaps between vendor expectations and our actual controls identified and remediated or risk-accepted. |
| **Observed State** | **7 CUECs** identified across 4 SOC 2 reports. CUEC mapping to SMG identity packs: **MFA enforcement (3 vendors expect it):** Mapped to Pack 03 — Conditional Access Baseline. CA001 enforces MFA for all users. CUEC satisfied. **Access review completion (2 vendors expect it):** Mapped to Pack 02 — Access Reviews Automation. Quarterly reviews with auto-revoke. CUEC satisfied. **Encryption of data at rest (2 vendors expect it):** Mapped to cloud-security-packs (planned). Currently client-managed via Azure Storage encryption. CUEC satisfied. **Timely user deprovisioning (1 vendor expects it):** Mapped to Pack 01 — Zero-Touch JML. Leaver event triggers within 4 hours. CUEC satisfied. **Log review and monitoring (2 vendors expects it):** Mapped to Pack 09 — ITDR. Continuous identity monitoring via Sentinel. CUEC satisfied. **0 CUEC gaps.** All vendor expectations mapped to operational controls with evidence from identity pillar. |
| **Finding** | CUEC analysis depends on identity packs being operational. If any referenced pack control degrades, the CUEC mapping becomes stale. Quarterly re-validation of CUEC mappings added to review cadence. |
| **Evidence** | `cuec-gap-analysis.md`, identity pack E-v-O cross-references |
| **NIST 800-53** | SA-9 |
| **Status** | **Partial** — all CUECs currently satisfied but cross-pillar dependency creates re-validation requirement |

---

### 9 — Attestation Validation Results Feed Pack 01 Scoring

| Field | Detail |
|-------|--------|
| **Expected State** | Attestation validation results directly influence Pack 01 Compliance Status domain score (20% weight). Validated = full credit. Conditional = reduced credit. Missing/expired = zero credit. |
| **Observed State** | **All 5 Critical/High vendor** Compliance Status scores updated based on validation results. CloudPlatform Corp: SOC 2 validated (full credit) + ISO not applicable + pen test validated (full credit) = 95/100. IdentityFirst Inc: ISO validated conditional (reduced) + pen test conditional (reduced) = 70/100. HR-Cloud SaaS: SOC 2 conditional (scope gap) + no pen test (zero credit) = 55/100. SecureDefend Tools: SOC 2 validated + ISO validated = 92/100. BackupVault Pro: SOC 2 stale (reduced) + carve-out finding = 50/100. All score changes reflected in Pack 01 vendor risk register. |
| **Evidence** | Pack 01 register, `calculate_risk.py` re-run output |
| **NIST 800-161** | SR-6 |
| **Status** | **Pass** |

---

### 10 — Attestation Renewal Calendar Active

| Field | Detail |
|-------|--------|
| **Expected State** | Every attestation has a tracked expiry date with 60-day advance notification. Vendor relationship owner responsible for requesting updated reports before expiry. |
| **Observed State** | Calendar **configured** for all 9 attestation records. 60-day and 30-day notifications active via Power Automate. Current status: 1 renewal in progress (BackupVault Pro SOC 2, due Mar 2026, requested Feb 3), 1 approaching 60-day window (HR-Cloud SaaS, expires Mar 2026, notification sent). **0 renewals missed.** |
| **Finding** | Calendar depends on vendor providing updated report on time. If vendor delays beyond expiry, attestation auto-flags as expired in tracker and Compliance Status score drops to zero for that report. The math handles the consequence — but the follow-up requires manual effort. |
| **Status** | **Partial** — calendar active but vendor-side delivery is outside our control |

---

## Remediation Tracker

| # | Control | Finding | Owner | Remediation | Target Date | Status |
|---|---------|---------|-------|-------------|-------------|--------|
| 8 | CUEC gap analysis | Cross-pillar dependency requires quarterly re-validation | R. Myers | Add CUEC re-validation to quarterly review cadence | 2026-Q2 | Open |
| 10 | Renewal calendar | Vendor-side delivery outside our control | R. Myers | Escalation procedure: if vendor misses renewal by 30 days, trigger re-assessment | 2026-Q1 | Open |

---

## Watchstander Notes

1. **We read the report.** That's the entire differentiator of this pack. Most organizations collect attestation reports and file them. We open them, validate 15 points, identify scope mismatches, find carve-outs, map CUECs, and feed findings back into the scoring engine. The report is not the evidence. The validation of the report is the evidence.

2. **Scope mismatch is the most common and most dangerous finding.** A vendor provides a SOC 2 that covers "Product A" but you're using "Product B" which runs on different infrastructure. The report is technically valid. It just doesn't cover you. This is the supply chain equivalent of a Certificate of Conformance for the wrong part number. You wouldn't install it. Don't accept it.

3. **CUECs are the bridge between pillars.** When a vendor says "we're secure as long as the client enforces MFA," they're creating a dependency on your identity controls. The CUEC gap analysis in this pack maps those dependencies directly to the identity pillar. This is why SMG isn't three separate practices — it's one operating picture. The chain of command is intact because the evidence chain is intact.

4. **A vendor who won't share their pen test report is telling you something.** HR-Cloud SaaS called their pen test "confidential." In a physical supply chain, a manufacturer who won't show you their quality inspection is a manufacturer you don't use. The digital supply chain deserves the same standard. The finding is documented. The score reflects it. The conversation with the vendor is now data-driven, not opinion-driven.

---

*Assessment conducted by Robert Myers, MBA | SailPoint ISL, Security+, CCSK, CC*
*Stella Maris Governance — 2026*
