# The Law of Evidence: Expected vs. Observed

## Vendor Offboarding & Access Revocation

> **Assessment Date:** 2026-02-12 [SAMPLE — replace with your assessment date]
> **Environment:** Stella Maris Lab — Entra ID + Sentinel + Offboarding Automation [SAMPLE]
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

### 1 — Offboarding Checklist Documented with All Access Paths

| Field | Detail |
|-------|--------|
| **Expected State** | Structured offboarding checklist covering all 5 phases: access revocation (10 items), secret rotation (5 items), software removal (5 items), data disposition (5 items), verification audit (5 items). Checklist sources data from Packs 01, 05, 06, and Identity Packs 06/08 to ensure every access path is captured. |
| **Observed State** | `offboarding-checklist.json` **documented** with 30 items across 5 phases. Checklist compiled from 4 cross-pillar sources: **Pack 01 vendor intake form:** integration type, data classification, access requirements — provides base access profile for each vendor. **Pack 05 blast radius inventory:** service principals, guest accounts, API keys, VPN tunnels, agent installations — comprehensive access enumeration. **Identity Pack 06 guest register:** all guest accounts with lifecycle status, group memberships, and application assignments. **Identity Pack 08 CIEM:** permission scope and PCI score per vendor service principal. All 5 Critical/High vendors have vendor-specific offboarding checklists generated from these sources. Each checklist customized to vendor's actual access footprint — no generic templates. |
| **Evidence** | `offboarding-checklist.json`, vendor-specific checklists |
| **NIST 800-53** | PS-4 |
| **Status** | **Pass** |

---

### 2 — Automated Access Revocation Deployed and Tested

| Field | Detail |
|-------|--------|
| **Expected State** | Automated script disables all vendor accounts, revokes sessions, and removes group memberships via Graph API. Tested with tabletop. Execution time under 5 minutes for any vendor. |
| **Observed State** | `revoke-vendor-access.py` **deployed and tested.** Script actions: (1) Query Entra ID for all guest accounts matching vendor domain, (2) Query for all service principals tagged to vendor, (3) Disable all accounts, (4) Revoke all sessions, (5) Remove from all groups, (6) Revoke OAuth consents, (7) Log all actions with timestamps. **Tabletop test (Feb 10) — Planned offboarding scenario:** Simulated end-of-contract offboarding for test vendor "DemoVendor-Alpha." Vendor had: 2 guest accounts, 1 service principal, 3 group memberships, 1 OAuth consent. Script execution: **38 seconds.** All accounts disabled, sessions revoked, groups cleared, consent revoked. **Tabletop test (Feb 11) — Termination-for-cause scenario:** Simulated immediate termination using Pack 05 containment playbook as first action, followed by full offboarding script. Combined time: containment in 52 seconds (Pack 05 validated), full offboarding in 41 seconds. **Total time to complete access revocation: 93 seconds.** |
| **Evidence** | Screenshot #02, tabletop log, `revoke-vendor-access.py` execution log |
| **NIST 800-53** | AC-2 |
| **Status** | **Pass** |

---

### 3 — Secret Rotation Checklist Executed Post-Offboarding

| Field | Detail |
|-------|--------|
| **Expected State** | All shared secrets, API keys, certificates, and SAS tokens associated with the offboarded vendor are rotated. Old credentials confirmed non-functional. |
| **Observed State** | Secret rotation checklist **tested** in planned offboarding tabletop. DemoVendor-Alpha had: 1 API key (application integration), 1 shared certificate (mutual TLS), 1 SAS token (blob storage access). Rotation results: API key rotated — new key functional, old key returns **401 Unauthorized** (verified). Certificate rotated — new thumbprint in configuration, old cert rejected on handshake (verified). SAS token regenerated — old token returns **403 Forbidden** (verified). **Time to complete rotation: 22 minutes** (manual process, 3 secrets). **Finding:** Rotation is manual. For vendors with 10+ shared secrets, this could take over an hour. Pre-staging a secret inventory per vendor (from Pack 05 blast radius) would accelerate. Recommendation documented. |
| **Evidence** | Screenshot #05, rotation verification log |
| **NIST 800-53** | AC-2 |
| **Status** | **Pass** |

---

### 4 — Tabletop: Planned Vendor Offboarding

| Field | Detail |
|-------|--------|
| **Expected State** | Tabletop simulating end-of-contract vendor offboarding. All 5 phases executed. Cooperative vendor scenario. |
| **Observed State** | **Tabletop executed Feb 10, 2026.** Scenario: DemoVendor-Alpha contract expires Feb 28. Offboarding initiated Feb 10 (18 days before expiry). |
| | **Phase 1 — Access Revocation:** All accounts disabled, sessions revoked, groups cleared. 38 seconds. |
| | **Phase 2 — Secret Rotation:** 3 secrets rotated and verified. 22 minutes. |
| | **Phase 3 — Software Removal:** DemoVendor-Alpha had no installed agents (SaaS-only). DNS CNAME record removed. Webhook URL removed from application config. 15 minutes. |
| | **Phase 4 — Data Disposition:** Data return request sent (simulated). Deletion request sent with attestation template. Tier 2 deletion request sent (DemoVendor-Alpha had 1 known Tier 2 entity). Response deadline: 90 days. |
| | **Phase 5 — Verification Audit:** Scheduled for 30 days post-offboarding (Mar 12). KQL query pre-staged. |
| | **Total active offboarding time: 76 minutes** (excluding Phase 4 waiting period and Phase 5 scheduled audit). |
| | All items in Phase 1-3 completed within SLA. Phase 4 and 5 are time-dependent and cannot be completed same-day by design. |
| **Evidence** | Tabletop timeline document |
| **NIST 800-53** | PS-4 |
| **Status** | **Pass** |

---

### 5 — Tabletop: Termination for Cause

| Field | Detail |
|-------|--------|
| **Expected State** | Tabletop simulating immediate vendor termination after a security incident. Pack 05 containment first, then full offboarding. Non-cooperative vendor scenario. |
| **Observed State** | **Tabletop executed Feb 11, 2026.** Scenario: DemoVendor-Beta terminated immediately after Pack 05 Tabletop 2 findings (simulating HR-Cloud SaaS breach + 7-day disclosure delay). Vendor is non-cooperative. |
| | **Immediate (T+0):** Pack 05 containment playbook triggered. All accounts disabled, sessions revoked. **52 seconds.** |
| | **T+2 minutes:** Full offboarding script executed. Groups cleared, OAuth consents revoked. **41 seconds additional.** |
| | **T+25 minutes:** Secret rotation completed (4 secrets: API key, SFTP credentials, shared password, SAS token). All verified non-functional. |
| | **T+45 minutes:** Software removal — SFTP channel disabled, webhook removed, DNS record removed. |
| | **T+1 hour:** Legal notified to send formal termination letter with data return demand and right-to-audit activation. |
| | **Data disposition challenge:** Vendor non-cooperative. Data return request sent but no expectation of timely response. Right-to-audit clause activated (contractual leverage). Deletion attestation unlikely without legal enforcement. **This is the realistic outcome for termination-for-cause.** |
| | **Phase 5 verification audit:** Scheduled for 30 days post-termination. Critical for this scenario — need to verify vendor doesn't attempt access after termination. |
| **Evidence** | Tabletop timeline document |
| **NIST 800-53** | PS-4 |
| **Status** | **Pass** |

---

### 6 — Post-Offboarding Verification Audit Configured

| Field | Detail |
|-------|--------|
| **Expected State** | KQL query scans Sentinel logs for 30 days post-offboarding. Detects any vendor account activity, vendor IP access attempts, vendor domain sign-in attempts. Zero activity expected. Any activity is a finding. |
| **Observed State** | `post-offboarding-audit.kql` **configured and tested.** Query searches: (1) Sign-in attempts from disabled vendor accounts (expected: 0 or all failed), (2) Sign-in attempts from vendor IP ranges, (3) API calls using old vendor credentials, (4) Any Entra audit events referencing vendor entities. **Tested against DemoVendor-Alpha (tabletop):** Query returned 0 events for vendor accounts post-disabling. 2 events flagged: automated system health check from monitoring tool attempted to reach vendor's webhook endpoint (expected — webhook was removed, call failed). Both classified as false positives (internal system, not vendor-initiated). **True positives: 0. False positives: 2.** Both explainable and documented. Query tuning note added to exclude known internal health check sources. |
| **Evidence** | `post-offboarding-audit.kql`, Screenshot #03 |
| **NIST 800-53** | SA-9 |
| **Status** | **Pass** |

---

### 7 — Data Disposition Tracker Operational

| Field | Detail |
|-------|--------|
| **Expected State** | Centralized tracker for data return and deletion: vendor, data types, return status, deletion request date, attestation received, Tier 2 deletion status. |
| **Observed State** | `data-disposition-tracker.json` **configured** with schema. No real offboardings completed yet (tabletop data used). Tracker fields: vendor name, data types held by vendor, data classification, return requested (date), return received (date/status), deletion requested (date), deletion attestation received (date/status), Tier 2 entities requiring deletion, Tier 2 deletion confirmed (date/status). **Tabletop entries logged:** DemoVendor-Alpha: data return requested (simulated), deletion requested, Tier 2 deletion requested for 1 entity. All pending (90-day SLA). DemoVendor-Beta (termination for cause): data return demanded, deletion demanded, right-to-audit activated. Status: non-cooperative — escalated to legal. |
| **Evidence** | `data-disposition-tracker.json` |
| **NIST 800-53** | MP-6 |
| **Status** | **Pass** |

---

### 8 — Data Deletion Attestation Template Prepared

| Field | Detail |
|-------|--------|
| **Expected State** | Formal data deletion attestation template prepared for vendor signature. Template includes: scope of data deleted, systems affected, method of destruction, date of destruction, confirmation that no copies retained, Tier 2 subprocessor deletion confirmation, authorized signer. |
| **Observed State** | `data-deletion-attestation-template.md` **prepared.** Template includes all required fields: organization name, vendor name, data description (types, classifications, record counts), systems from which data was deleted, method of destruction (cryptographic erasure, secure overwrite, physical destruction), confirmation that backup copies and replicas were also deleted, Tier 2 subprocessor deletion confirmation section, authorized signer with title and date. Template **reviewed against GDPR Article 17 and Article 28(3)(g) requirements.** Template covers both cooperative (planned offboarding) and non-cooperative (termination for cause with legal enforcement) scenarios. Legal team approved template. |
| **Evidence** | `data-deletion-attestation-template.md` |
| **GDPR** | Art. 17, Art. 28(3)(g) |
| **Status** | **Pass** |

---

### 9 — Tier 2 Data Deletion Confirmation Process

| Field | Detail |
|-------|--------|
| **Expected State** | For Critical vendors, data deletion extends to Tier 2 subprocessors identified in Pack 06. Deletion confirmation requested from Tier 1 vendor, who confirms deletion by their subprocessors. |
| **Observed State** | Process **designed** and included in data disposition tracker. For each Critical vendor offboarding, Pack 06 Tier 2 register is queried for entities handling your data. Deletion request flows: You → Tier 1 vendor → Tier 2 subprocessor. Tier 1 vendor is contractually responsible for confirming Tier 2 deletion. **Challenge documented:** Pack 06 found that 3 of 5 Tier 1 vendors do not have right-to-audit clauses extending to Tier 2 subprocessors. This means the Tier 1 vendor may not be able to compel Tier 2 deletion confirmation. The process works when the vendor has Tier 2 governance. When they don't, the process is request-only with no enforcement mechanism. |
| **Finding** | Tier 2 deletion confirmation depends on Tier 1 vendor having governance over their subprocessors. Pack 06 already documented that 3 of 5 vendors lack this. The offboarding process cannot overcome an upstream governance gap. |
| **Status** | **Partial** — process designed and operational, but effectiveness limited by Tier 1-Tier 2 governance gaps (Pack 06 finding) |

---

### 10 — Offboarding Register Tracking All Vendor Lifecycle Closures

| Field | Detail |
|-------|--------|
| **Expected State** | Centralized offboarding register tracks all vendor offboardings: vendor, trigger, start date, phase completion status, data disposition status, verification audit status, closure date. No vendor offboarding is complete until all 5 phases are verified. |
| **Observed State** | `offboarding-register.json` **configured** with 2 tabletop entries. **No real vendor offboardings have occurred** since the supply chain pillar was built. Both entries are tabletop exercises (DemoVendor-Alpha planned, DemoVendor-Beta termination-for-cause). Register is operational but untested with a real vendor offboarding. |
| **Finding** | Process is built, tested via tabletop, and ready for execution. But tabletop is not the real thing. A real offboarding will surface issues the tabletop couldn't — vendor delays, incomplete data inventories, secrets we didn't know about, applications configured by people who have since left. The first real offboarding will be the true test. |
| **Status** | **Fail** — register operational but no real offboarding completed to validate end-to-end process |

---

## Remediation Tracker

| # | Control | Finding | Owner | Remediation | Target Date | Status |
|---|---------|---------|-------|-------------|-------------|--------|
| 3 | Secret rotation | Manual process for 3+ secrets takes 22+ min. Pre-stage secret inventory. | R. Myers | Build per-vendor secret inventory linked to Pack 05 blast radius | 2026-Q2 | Open |
| 9 | Tier 2 deletion | 3 of 5 vendors lack Tier 2 governance — deletion confirmation is request-only | R. Myers | Include Tier 2 audit rights in contract renewals (Pack 06 remediation) | Next renewal | Open |
| 10 | Register | No real offboarding completed. Tabletop validated but not production-tested. | R. Myers | Time-based — first real offboarding will validate | When triggered | Open |

---

## Watchstander Notes

1. **93 seconds to fully revoke a terminated vendor's access.** Containment (52 seconds) + full offboarding script (41 seconds). That's the time between "terminate this vendor" and "every account disabled, every session revoked, every group membership cleared." In a termination-for-cause after a security incident, those 93 seconds are the most important 93 seconds in your supply chain risk program. The automation removes the human from the critical path. The human handles the investigation, legal engagement, and data disposition — the parts that require judgment.

2. **The honest fail on Control 10 is the right call.** We've tested the offboarding with tabletops. The process works in simulation. But a tabletop doesn't discover the API key that was shared in a Slack DM and never documented. It doesn't discover the service account someone created outside the standard process. It doesn't discover the data the vendor copied to a personal environment. The first real offboarding will surface what the tabletop couldn't. Marking it as a fail is honest. Marking it as a pass would be overconfident.

3. **Tier 2 data deletion is the unsolvable problem at the end of the supply chain.** You ask the vendor to delete your data. You even get an attestation. But the vendor's subprocessor in Ireland has a backup copy in a system the vendor can't audit. You know this because Pack 06 told you the vendor doesn't have right-to-audit over their Tier 2. The offboarding process can't fix an upstream governance gap. But it can document it, which turns an invisible risk into a visible one. And the next contract you negotiate will include Tier 2 audit rights because this finding exists.

4. **The door you opened must close completely.** That's the principle. But in practice, "completely" means "to the extent you can verify." You can verify that your accounts are disabled. You can verify that your secrets are rotated. You can verify that your network paths are closed. You cannot verify that the vendor actually deleted your data. You can require it. You can demand attestation. You can activate your audit clause. But ultimately, data deletion depends on the vendor's integrity. That's why everything that came before this pack — the assessment (Pack 01), the attestation validation (Pack 02), the scorecard (Pack 04), the SLA governance (Pack 07) — matters. You spent the relationship measuring who this vendor is. Now, at offboarding, you're relying on that character assessment for the one thing you can't independently verify.

5. **This pack closes the vendor lifecycle.** Pack 01 opened it (assessment and onboarding). Packs 02-07 governed it (attestation, SBOM, scorecard, incident response, traceability, SLA). Pack 08 closes it. Every vendor has an entry and an exit. The exit is as governed as the entry. That is the supply chain pillar.

---

*Assessment conducted by Robert Myers, MBA | SailPoint ISL, Security+, CCSK, CC*
*Stella Maris Governance — 2026*
