# The Law of Evidence: Expected vs. Observed

## Tier 2/3 Supplier Traceability

> **Assessment Date:** 2026-02-12 [SAMPLE — replace with your assessment date]
> **Environment:** Stella Maris Lab — Tier 2 Register + Supply Chain Maps [SAMPLE]
> **Assessor:** Robert Myers, MBA | SailPoint ISL, Security+, CCSK, CC
> **Pack Version:** 1.0.0
> **Status:** 7/10 controls confirmed | 2 partial | 1 fail

---

## Summary

| Status | Count | Percentage |
|--------|-------|------------|
| Pass | 7 | 70% |
| Partial | 2 | 20% |
| Fail | 1 | 10% |

---

## Assessment Detail

### 1 — Tier 2 Data Collected from Available Sources

| Field | Detail |
|-------|--------|
| **Expected State** | Tier 2 subprocessor data collected from every available source: SOC 2 carve-outs (Pack 02), DPA subprocessor lists, GDPR Article 28 disclosures, vendor public documentation, and subprocessor questionnaire responses. |
| **Observed State** | **4 data sources** harvested across 5 Critical/High vendors. **SOC 2 carve-outs (Pack 02):** BackupVault Pro SOC 2 carves out encryption key management subservice — Tier 2 entity identified: KeyVault Solutions (US). HR-Cloud SaaS SOC 2: no carve-outs but "inclusive" method — subservice organizations included in scope but not individually named. CloudPlatform Corp: no carve-outs, all infrastructure self-managed. SecureDefend Tools: no carve-outs. **DPA/GDPR Article 28 lists:** HR-Cloud SaaS DPA names 3 subprocessors: PayrollEngine (US), DataStore Plus (Ireland), AnalyticsHub (US). IdentityFirst Inc DPA names 2 subprocessors: CloudHost Alpha (US-EAST), CertAuth Global (Netherlands). **Public documentation:** CloudPlatform Corp trust page lists infrastructure regions (self-operated). SecureDefend Tools trust page lists "no third-party data processing." **Subprocessor questionnaire:** Sent to all 5 vendors. 2 responses received (CloudPlatform Corp, SecureDefend Tools). 3 outstanding (IdentityFirst, HR-Cloud, BackupVault). |
| **Evidence** | SOC 2 reports, DPA attachments, vendor trust pages, questionnaire log |
| **NIST 800-161** | SR-3 |
| **Status** | **Pass** |

---

### 2 — Tier 2 Register Built and Populated

| Field | Detail |
|-------|--------|
| **Expected State** | Centralized register of all known Tier 2 entities. Each entry includes: Tier 1 vendor relationship, service provided, jurisdiction, attestation status (if known), and data flow type. |
| **Observed State** | `tier2-register.json` **populated** with **8 known Tier 2 entities** across 5 Tier 1 vendors: |
| | **CloudPlatform Corp:** Self-operated infrastructure. No Tier 2 entities identified. Questionnaire confirmed. |
| | **IdentityFirst Inc:** (1) CloudHost Alpha — hosting, US-EAST, no independent attestation visible. (2) CertAuth Global — certificate services, Netherlands, WebTrust accredited. |
| | **HR-Cloud SaaS:** (3) PayrollEngine — payroll calculation, US, SOC 2 Type II (per HR-Cloud DPA). (4) DataStore Plus — database hosting, Ireland, ISO 27001 (per HR-Cloud DPA). (5) AnalyticsHub — usage analytics, US, no attestation listed. |
| | **SecureDefend Tools:** No Tier 2 entities. Questionnaire confirmed self-operated. |
| | **BackupVault Pro:** (6) KeyVault Solutions — encryption key management, US, carved out of SOC 2. No independent attestation visible. (7) StorageGrid Inc — object storage infrastructure, US-WEST, no attestation listed. (8) TransitNet — network transit, US, no attestation listed. Entities 7 and 8 identified through public documentation review only — not confirmed by vendor. |
| **Evidence** | `tier2-register.json`, Screenshot #01 |
| **NIST 800-53** | SA-9(2) |
| **Status** | **Pass** |

---

### 3 — Jurisdiction Tracking Complete for All Known Tier 2 Entities

| Field | Detail |
|-------|--------|
| **Expected State** | Every Tier 2 entity tagged with: incorporation jurisdiction, data processing jurisdiction, data storage jurisdiction. Jurisdictions flagged for GDPR adequacy, ITAR restrictions, and data sovereignty requirements. |
| **Observed State** | **8 Tier 2 entities** jurisdiction-tagged. Summary: 6 entities US-based (no jurisdiction flags for current data types). 1 entity Ireland-based (DataStore Plus) — EU jurisdiction, GDPR adequate, no concern for US employee data processing. 1 entity Netherlands-based (CertAuth Global) — EU jurisdiction, GDPR adequate, certificate services only (no PII). **No ITAR-restricted jurisdictions identified.** **No data sovereignty conflicts detected** for current data classification. **Flag:** BackupVault Pro's Tier 2 entities (StorageGrid, TransitNet) identified through public docs only — jurisdictions are inferred, not confirmed by vendor. Confidence: medium. |
| **Evidence** | `jurisdiction-tracker.json` |
| **NIST 800-161** | SR-3 |
| **Status** | **Pass** |

---

### 4 — Concentration Risk Analysis Completed

| Field | Detail |
|-------|--------|
| **Expected State** | Analysis identifies Tier 2 entities shared by multiple Tier 1 vendors. Shared dependencies flagged as concentration risk with impact assessment. |
| **Observed State** | `concentration-risk-scan.py` **executed.** Results: **No shared Tier 2 entities detected across current vendor set.** Each Tier 2 entity maps to a single Tier 1 vendor. However, analysis revealed a **Tier 3 concentration risk:** CloudHost Alpha (IdentityFirst's hosting) and StorageGrid Inc (BackupVault's storage) both operate on AWS US-EAST infrastructure — confirmed through public routing data. If AWS US-EAST experiences a major outage, both IdentityFirst (Critical) and BackupVault (High) could be simultaneously affected. **Tier 3 concentration documented.** Not directly governable, but awareness enables contingency planning. Additionally, **software-layer concentration** from Pack 03: jackson-databind present in 2 vendor SBOMs (App-2 and SecureDefend Tools). A single library CVE affected multiple points in the supply chain. This is concentration risk at the code level — already governed by Pack 03 but cross-referenced here. |
| **Evidence** | `concentration-risk-scan.py` output, Screenshot #03 |
| **NIST 800-161** | SR-3 |
| **Status** | **Pass** |

---

### 5 — Supply Chain Maps Generated for Critical Vendors

| Field | Detail |
|-------|--------|
| **Expected State** | Visual dependency chain maps generated for all Critical vendors showing Tier 1 → Tier 2 → Tier 3 relationships. Maps show data flow direction, jurisdiction, and attestation status. |
| **Observed State** | `build-supply-chain-map.py` **generated** maps for 2 Critical vendors: **CloudPlatform Corp:** Clean map. Self-operated infrastructure. No Tier 2 dependencies. Data stays within vendor-owned regions. Map depth: 1 tier. **IdentityFirst Inc:** Map shows: IdentityFirst → CloudHost Alpha (hosting, US-EAST, no attestation) → AWS US-EAST (Tier 3, inferred). IdentityFirst → CertAuth Global (certificates, Netherlands, WebTrust accredited). Map depth: 3 tiers. CloudHost Alpha's lack of independent attestation is visible as a gap on the map. Maps for 3 High vendors generated with available data. BackupVault Pro map includes 3 Tier 2 entities with 2 unconfirmed (dotted lines on map indicating low-confidence data). |
| **Evidence** | Screenshot #02, generated map files |
| **NIST 800-161** | SR-4(2) |
| **Status** | **Pass** |

---

### 6 — Right-to-Audit Clauses Tracked

| Field | Detail |
|-------|--------|
| **Expected State** | All Critical and High vendor contracts reviewed for right-to-audit clauses. Clause presence documented. Flow-down to Tier 2 assessed. |
| **Observed State** | **Contract review completed** for 5 Critical/High vendors: **CloudPlatform Corp:** Right-to-audit clause present. Flow-down: CloudPlatform self-operates, no Tier 2 to flow to. **IdentityFirst Inc:** Right-to-audit clause present but limited — "upon reasonable notice and no more than annually." Flow-down: clause does not explicitly extend to subprocessors (CloudHost Alpha, CertAuth Global). Gap documented. **HR-Cloud SaaS:** Right-to-audit clause present. Flow-down: DPA states subprocessors are subject to "equivalent security requirements" but does not grant client audit rights over subprocessors. Gap documented. **SecureDefend Tools:** Right-to-audit clause present. Flow-down: not applicable (no Tier 2). **BackupVault Pro:** No explicit right-to-audit clause in contract. Finding: Pack 01 already flagged this gap. Right-to-audit is negotiation item for contract renewal. |
| **Evidence** | Contract review log |
| **NIST 800-53** | SA-9(2) |
| **Status** | **Pass** |

---

### 7 — Tier 2 Attestation Visibility Assessed

| Field | Detail |
|-------|--------|
| **Expected State** | For every Tier 2 entity serving a Critical vendor, determine whether an independent attestation (SOC 2, ISO 27001, etc.) exists. If visible, note type and currency. If not, document as a gap. |
| **Observed State** | **8 Tier 2 entities** assessed for attestation visibility: (1) CloudHost Alpha: **No attestation visible.** Hosts IdentityFirst (Critical vendor). Gap. (2) CertAuth Global: **WebTrust accredited.** Adequate for certificate services. (3) PayrollEngine: **SOC 2 Type II per DPA.** Not independently verified — accepting HR-Cloud's representation. (4) DataStore Plus: **ISO 27001 per DPA.** Not independently verified. (5) AnalyticsHub: **No attestation listed.** HR-Cloud DPA silent on analytics subprocessor attestation. (6) KeyVault Solutions: **No attestation visible.** Carved out of BackupVault SOC 2. Handles encryption key management. Gap. (7) StorageGrid Inc: **No attestation visible.** Unconfirmed Tier 2. (8) TransitNet: **No attestation visible.** Unconfirmed Tier 2. **Summary:** 1 independently verified (CertAuth), 2 vendor-represented (PayrollEngine, DataStore Plus), 5 with no attestation visibility. **5 of 8 Tier 2 entities have no independent attestation.** Two of these (CloudHost Alpha, KeyVault Solutions) serve Critical or High vendors in sensitive roles. |
| **Evidence** | Tier 2 register attestation column |
| **NIST 800-161** | SR-6 |
| **Status** | **Partial** — attestation visibility exists for 3 of 8 entities; 5 gaps documented |

---

### 8 — Tier 2 Findings Fed to Pack 01 Scoring

| Field | Detail |
|-------|--------|
| **Expected State** | Tier 2 visibility and attestation gaps directly impact Pack 01 Subcontractor Risk domain (10% of vendor score). Full visibility = full credit. Gaps reduce score proportionally. |
| **Observed State** | **All 5 vendor** Subcontractor Risk domain scores updated: **CloudPlatform Corp:** No Tier 2 dependencies, self-operated. Full credit: 95/100. **IdentityFirst Inc:** 2 Tier 2 entities known, 1 with attestation (CertAuth), 1 without (CloudHost Alpha). Right-to-audit doesn't flow down. Score: 45/100 (was 40 before Pack 06 provided structured data — slight increase because entities are now identified even if not fully visible). **HR-Cloud SaaS:** 3 Tier 2 entities via DPA, 2 with vendor-represented attestation, 1 with no attestation. No client audit rights over subprocessors. Score: 50/100. **SecureDefend Tools:** No Tier 2, confirmed via questionnaire. Full credit: 90/100. **BackupVault Pro:** 3 Tier 2 entities, 2 unconfirmed, 0 attestation visibility, no right-to-audit clause. Score: 15/100 (lowest in portfolio). Pack 01 `calculate_risk.py` re-run confirmed all score changes. |
| **Evidence** | Pack 01 register, scoring output |
| **NIST 800-161** | SR-6 |
| **Status** | **Pass** |

---

### 9 — Subprocessor Questionnaire Deployed

| Field | Detail |
|-------|--------|
| **Expected State** | Structured subprocessor questionnaire sent to all Critical and High vendors. Questionnaire requests: Tier 2 entity names, services provided, jurisdictions, attestation status, data flow types, and whether the vendor has right-to-audit over their subprocessors. |
| **Observed State** | `subprocessor-questionnaire.json` **deployed** to all 5 Critical/High vendors on Feb 5. **Responses received (2):** CloudPlatform Corp (Feb 7): confirmed no Tier 2 subprocessors, all infrastructure self-managed. SecureDefend Tools (Feb 8): confirmed no Tier 2 subprocessors for data processing, internal tooling only. **Responses outstanding (3):** IdentityFirst Inc: follow-up sent Feb 10. HR-Cloud SaaS: no response. BackupVault Pro: no response. **Response rate: 40% (2 of 5).** Both responses confirmed self-operation. The 3 non-responders are the vendors where Tier 2 visibility is most needed — and most lacking. Non-response documented and scored. |
| **Finding** | 60% non-response rate on the primary data collection mechanism. DPA and SOC 2 analysis provided partial data for non-responders, but the questionnaire would provide the most comprehensive picture. |
| **Status** | **Fail** — questionnaire deployed but 60% non-response rate means primary data collection is not yet effective |

---

### 10 — Tier 2 Traceability Review Cadence Established

| Field | Detail |
|-------|--------|
| **Expected State** | Tier 2 register reviewed semi-annually. Vendor subprocessor changes tracked. New Tier 2 entities assessed upon disclosure. GDPR Article 28 change notifications monitored. |
| **Observed State** | Review cadence **established:** semi-annual full review (next: Aug 2026), plus event-driven review when vendor discloses subprocessor change. GDPR Article 28 change notification monitoring configured for HR-Cloud SaaS (only vendor with GDPR-covered data flowing to EU subprocessor). **Not yet tested** — no subprocessor changes have occurred since register was built. Process is designed but unexercised. |
| **Finding** | Semi-annual cadence is designed. First review not due until Aug 2026. Process will be validated at first review or first subprocessor change event, whichever comes first. |
| **Status** | **Partial** — cadence established but not yet exercised |

---

## Remediation Tracker

| # | Control | Finding | Owner | Remediation | Target Date | Status |
|---|---------|---------|-------|-------------|-------------|--------|
| 7 | Tier 2 attestation | 5 of 8 Tier 2 entities have no attestation visibility, including 2 in sensitive roles | R. Myers | Request attestation data through Tier 1 vendors. Include Tier 2 attestation requirement in contract renewals. | 2026-Q2 | Open |
| 9 | Questionnaire response | 60% non-response rate on subprocessor questionnaire | R. Myers | Escalate through vendor relationship owners. Tie questionnaire response to re-assessment cooperation score. | 2026-03-15 | Open |
| 10 | Review cadence | Semi-annual review not yet exercised | R. Myers | Time-based — first review Aug 2026 | 2026-08-15 | Open |

---

## Watchstander Notes

1. **This is the hardest data to get. It's also the most important.** Vendors don't want to tell you who their subprocessors are. They call it commercially sensitive. They say it changes frequently. They say their contracts don't allow it. Document every excuse. Then point to the right-to-audit clause — or the absence of one. The resistance itself is a data point about the vendor's supply chain maturity.

2. **The honest fail on Control 9 is strategic.** A 60% non-response rate on the questionnaire means the primary data collection mechanism isn't working yet. But we didn't just wait for questionnaires. We harvested SOC 2 carve-outs, DPA subprocessor lists, and public documentation to build partial visibility. The fail drives the next action: tie questionnaire response to re-assessment cooperation scoring. Make the silence cost something in the math.

3. **Concentration risk at Tier 3 is real and ungovernable.** Both IdentityFirst and BackupVault ultimately depend on AWS US-EAST. We can't change that. We can't audit AWS. But we can know it, plan for it, and ensure our incident response (Pack 05) accounts for a simultaneous failure of both vendors. Awareness is the governance tool when control is not available.

4. **BackupVault Pro's Subcontractor Risk score of 15/100 tells the full story.** No right-to-audit clause. No questionnaire response. 3 Tier 2 entities identified through public docs only — 2 unconfirmed. Zero attestation visibility at Tier 2. Combined with their stale SOC 2 (Pack 02), declining scorecard (Pack 04), and missing SBOM (Pack 03), the picture is clear. This isn't one finding. It's a trajectory. The data across 6 packs builds the case that no single pack could make alone. That is the operating picture.

5. **Transitive software dependencies (Pack 03) and organizational subprocessors (this pack) are the same principle in different domains.** A library 6 levels deep in your dependency tree is a Tier 3 software supplier. A hosting provider 2 levels behind your vendor is a Tier 2 infrastructure supplier. Both are invisible without deliberate traceability. Both can be the source of your next incident. The SBOM maps the code chain. This pack maps the organizational chain. Together, they map the full supply chain.

---

*Assessment conducted by Robert Myers, MBA | SailPoint ISL, Security+, CCSK, CC*
*Stella Maris Governance — 2026*
