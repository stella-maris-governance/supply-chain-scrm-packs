# The Law of Evidence: Expected vs. Observed

## Supply Chain Incident Response

> **Assessment Date:** 2026-02-11 [SAMPLE — replace with your assessment date]
> **Environment:** Stella Maris Lab — Sentinel + Playbooks + Tabletop [SAMPLE]
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

### 1 — Third-Party Incident Response Plan Documented and Approved

| Field | Detail |
|-------|--------|
| **Expected State** | Written plan covering: third-party incident classification (4 tiers), containment playbooks (4 types), blast radius assessment procedures, communication framework, vendor accountability scoring, and post-incident review process. Approved by organizational leadership. |
| **Observed State** | Plan **approved** by tenant owner. Covers all 4 severity tiers with defined SLAs. 4 containment playbooks documented: credential compromise, data breach, supply chain software attack, and vendor service outage. Communication templates for 6 audiences: CISO, executive, legal, vendor, regulator, customer. Vendor accountability framework with 5 scoring factors. Post-incident review process with scorecard update and re-assessment triggers. Plan version 1.0.0, effective Feb 2026. |
| **Evidence** | Plan document v1.0 |
| **NIST 800-53** | IR-8 |
| **Status** | **Pass** |

---

### 2 — Vendor Access Inventory Complete for Blast Radius

| Field | Detail |
|-------|--------|
| **Expected State** | All vendor access paths documented: user accounts, service principals, API keys, VPN connections, network access, data shares. Inventory enables rapid blast radius scoping when a vendor is compromised. |
| **Observed State** | Vendor access inventory **completed** for all 5 Critical/High vendors. **CloudPlatform Corp:** 1 service principal (Contributor on 2 subscriptions), 0 user accounts, API integration via managed identity. **IdentityFirst Inc:** 1 service principal (Directory.ReadWrite.All), 2 vendor user accounts (guest), SSO integration. **HR-Cloud SaaS:** 1 service principal (User.Read.All, Mail.Send), 1 vendor admin account (guest), SFTP data transfer for employee sync. **SecureDefend Tools:** 1 service principal (SecurityEvents.Read.All), agent installed on 47 endpoints. **BackupVault Pro:** 1 service principal (Storage.Blob.Contributor on backup vault), VPN tunnel for on-prem backup agent. Total: 5 service principals, 3 guest user accounts, 1 VPN tunnel, 1 SFTP channel, 47 agent installations. Cross-referenced with Pack 08 (CIEM) PCI scores and Pack 06 (Guest vIAM) lifecycle status. |
| **Evidence** | Vendor access register, Pack 08/06 cross-reference |
| **NIST 800-161** | SR-6 |
| **Status** | **Pass** |

---

### 3 — Credential Containment Playbook Deployed and Tested

| Field | Detail |
|-------|--------|
| **Expected State** | Automated playbook: on third-party credential compromise, disable vendor accounts, revoke sessions, rotate shared secrets. Playbook tested via tabletop. |
| **Observed State** | `playbook-credential-compromise` **deployed** as Sentinel-triggered Logic App. Actions: (1) Identify all accounts associated with vendor (query by domain/tag), (2) Disable accounts via Graph API, (3) Revoke sessions via Graph API, (4) Flag API keys/secrets for manual rotation, (5) Notify SOC + Risk Owner. **Tabletop exercise (Feb 8):** Scenario — IdentityFirst Inc reports credential compromise. Playbook manually triggered. Results: 2 guest accounts disabled in 42 seconds, 1 service principal disabled in 44 seconds, sessions revoked in 48 seconds, SOC notified in 52 seconds. Total containment: **52 seconds.** API key rotation completed manually in 14 minutes (not automated — see finding). |
| **Evidence** | Screenshot #02, tabletop log |
| **NIST 800-53** | IR-4 |
| **Status** | **Pass** |

---

### 4 — Tabletop Exercise: Vendor Credential Compromise

| Field | Detail |
|-------|--------|
| **Expected State** | Tabletop exercise simulating vendor credential compromise. Full incident timeline documented with timestamps at every stage. Containment within SLA. |
| **Observed State** | **Tabletop executed Feb 8, 2026.** Scenario: IdentityFirst Inc notifies SMG at 10:00 UTC that a phishing attack compromised credentials of their support team member who has access to client environments. |
| | **10:00:00 UTC** — Vendor notification received (simulated phone call) |
| | **10:02:15 UTC** — Incident classified as Tier 2 (probable exposure, vendor has directory access) |
| | **10:03:30 UTC** — Containment playbook triggered manually |
| | **10:04:12 UTC** — 2 guest accounts disabled |
| | **10:04:14 UTC** — 1 service principal disabled |
| | **10:04:18 UTC** — All sessions revoked |
| | **10:04:22 UTC** — SOC + Risk Owner notified |
| | **10:18:00 UTC** — API key rotation completed (manual) |
| | **10:22:00 UTC** — Blast radius assessment initiated |
| | **10:45:00 UTC** — Blast radius assessment complete: vendor SP accessed directory read operations only in last 30 days, no write operations, no lateral movement indicators |
| | **11:00:00 UTC** — CISO briefed (within 2-hour SLA for Tier 2) |
| | **11:30:00 UTC** — Vendor demand for information sent |
| | **14:00:00 UTC** — Vendor responds: compromised employee had MFA bypassed via AiTM, vendor has revoked employee access, no evidence of client data access |
| | |
| | **Time to contain: 4 minutes 22 seconds** (notification → all accounts disabled + sessions revoked) |
| | **Time to blast radius: 45 minutes** (notification → exposure assessment complete) |
| | **Time to CISO brief: 1 hour** (within 2-hour Tier 2 SLA) |
| | Both containment and communication within SLA. |
| **Evidence** | Screenshot #04, tabletop timeline document |
| **NIST 800-53** | IR-4, IR-5 |
| **Status** | **Pass** |

---

### 5 — Tabletop Exercise: Vendor Data Breach Notification

| Field | Detail |
|-------|--------|
| **Expected State** | Second tabletop simulating a vendor reporting a data breach where your organization's data may be affected. Full Playbook B executed including regulatory assessment. |
| **Observed State** | **Tabletop executed Feb 9, 2026.** Scenario: HR-Cloud SaaS emails at 14:00 UTC that their database was accessed by an unauthorized party. Your employee PII (names, SSNs, dates of birth) was stored in the affected database. |
| | **14:00:00 UTC** — Vendor email received |
| | **14:08:00 UTC** — Classified as Tier 1 (confirmed data exposure, PII in blast radius) |
| | **14:12:00 UTC** — Data flows to/from HR-Cloud restricted (SFTP disabled, API throttled) |
| | **14:15:00 UTC** — Vendor demand for information sent: scope, timeline, affected records, remediation plan |
| | **14:30:00 UTC** — Data inventory completed: 214 employee records (name, SSN, DOB, salary) shared via SFTP monthly sync |
| | **14:45:00 UTC** — Legal engaged: GDPR 72-hour notification assessed (not applicable — US employees only). State breach notification laws assessed: Texas, Virginia, California employees identified. |
| | **15:00:00 UTC** — CISO briefed (within 2-hour Tier 1 SLA) |
| | **15:30:00 UTC** — Executive briefed with business impact and regulatory exposure |
| | **16:00:00 UTC** — Vendor responds: 847 client records in affected database, breach window Jan 28 – Feb 2, attacker accessed via SQL injection, vendor has engaged forensic firm |
| | **18:00:00 UTC** — Customer notification draft prepared (pending legal review) |
| | |
| | **Time to classify: 8 minutes** |
| | **Time to contain (data flow restriction): 12 minutes** |
| | **Time to data inventory: 30 minutes** |
| | **Time to CISO brief: 1 hour** (within 2-hour Tier 1 SLA) |
| | **Time to executive brief: 1.5 hours** |
| | All within SLA. Regulatory assessment initiated within 1 hour. |
| **Evidence** | Tabletop timeline document |
| **NIST 800-53** | IR-4, IR-6 |
| **Status** | **Pass** |

---

### 6 — Blast Radius Assessment Tool Operational

| Field | Detail |
|-------|--------|
| **Expected State** | Cross-pillar blast radius assessment: given a vendor name, rapidly determine all access paths, data exposure, software components, and network connections. All five assessment pillars (identity, data, software, network, financial) queryable. |
| **Observed State** | `blast-radius-assessment.py` **operational.** Takes vendor name as input, queries: (1) Pack 06 vendor access register for accounts and permissions, (2) Pack 08 CIEM for vendor PCI scores and permission scope, (3) Pack 01 intake form for data classification and integration type, (4) Pack 03 SBOM register for vendor software components, (5) Contract database for financial exposure and SLA terms. **Tested during both tabletop exercises.** Tabletop 1 (IdentityFirst): full blast radius in 23 minutes. Tabletop 2 (HR-Cloud): full blast radius in 30 minutes. |
| **Finding** | Network assessment (pillar 4) is partially manual — VPN and firewall rules are not yet queryable via API. Network team provided data manually during tabletop in 15 minutes. Automating this feed would reduce blast radius time. |
| **Evidence** | Screenshot #03, `blast-radius-assessment.py` output |
| **NIST 800-53** | IR-4 |
| **Status** | **Partial** — 4 of 5 pillars automated, network assessment partially manual |

---

### 7 — Communication Templates Prepared and Tested

| Field | Detail |
|-------|--------|
| **Expected State** | Communication templates for all 6 audiences prepared, reviewed by legal, and tested during tabletop. Distribution lists current. |
| **Observed State** | **5 of 6 templates** prepared and tested: CISO brief (tested in both tabletops), executive brief (tested in Tabletop 2), legal brief (tested in Tabletop 2), vendor demand for information (tested in both tabletops), customer notification (drafted in Tabletop 2). **Regulator notification template:** drafted but not tested — Tabletop 2 determined GDPR did not apply (US employees only). State breach notification templates not yet customized for Texas, Virginia, and California. Distribution lists: CISO (current), legal (current), executive (current), vendor security contacts (3 of 5 vendors confirmed — HR-Cloud and BackupVault contacts unverified). |
| **Evidence** | Template documents, tabletop usage log |
| **NIST 800-53** | IR-6 |
| **Status** | **Partial** — 5 of 6 templates tested; regulator template and 2 vendor contacts need completion |

---

### 8 — Vendor Accountability Scored Post-Tabletop

| Field | Detail |
|-------|--------|
| **Expected State** | After each incident (real or tabletop), vendor scored on 5 accountability factors: disclosure timeliness, transparency, cooperation, remediation quality, and contractual compliance. Scores feed Pack 04 Relationship Health. |
| **Observed State** | Vendor accountability scoring **applied** to both tabletop scenarios (simulated vendor responses). **Tabletop 1 (IdentityFirst):** Disclosure timeliness: 8/10 (prompt notification). Transparency: 7/10 (provided scope but not full timeline initially). Cooperation: 9/10 (responded to demand within 4 hours). Remediation: 8/10 (revoked compromised employee access immediately). Contractual: 8/10 (met notification SLA). **Composite accountability: 80%.** **Tabletop 2 (HR-Cloud):** Disclosure timeliness: 5/10 (breach window Jan 28 – Feb 2, notified Feb 9 — 7 days late). Transparency: 6/10 (provided record count but not full forensic scope initially). Cooperation: 7/10 (responded to demand but did not grant audit access). Remediation: pending (forensic investigation ongoing). Contractual: 4/10 (notification SLA was 48 hours, actual was 7 days). **Composite accountability: 55%.** Both scores documented. HR-Cloud accountability score of 55% would trigger Relationship Health category drop in Pack 04 scorecard — moved from 65 to estimated 52. |
| **Evidence** | Accountability scoring worksheets |
| **NIST 800-161** | SR-6 |
| **Status** | **Pass** |

---

### 9 — Post-Incident Review Process Documented and Tested

| Field | Detail |
|-------|--------|
| **Expected State** | After every third-party incident, post-incident review conducted within 14 days. Review covers: timeline accuracy, containment effectiveness, communication quality, vendor cooperation, lessons learned, and governance improvements. |
| **Observed State** | Post-incident review template **documented.** Applied to both tabletop exercises. **Tabletop 1 review findings:** Containment fast (52 seconds). API key rotation was manual and slow (14 minutes) — recommendation: pre-stage rotation procedures. Blast radius assessment effective. Lesson: document vendor API key inventory separately from account inventory for faster rotation. **Tabletop 2 review findings:** Classification fast (8 minutes). Data flow restriction effective (12 minutes). Regulatory assessment identified state-specific requirements quickly. Lesson: pre-build state-specific notification templates for Texas, Virginia, California. Lesson: HR-Cloud SaaS 7-day disclosure delay is a contractual breach — recommend amending contract with penalty clause and shorter notification SLA. Both reviews archived. Recommendations logged in remediation tracker. |
| **Evidence** | Post-incident review documents |
| **NIST 800-53** | IR-4 |
| **Status** | **Pass** |

---

### 10 — Incident Register Configured and Logging

| Field | Detail |
|-------|--------|
| **Expected State** | Centralized incident register tracks all third-party incidents (real and tabletop): incident ID, vendor, severity, detection source, timeline, containment time, blast radius, vendor accountability score, lessons learned, status. |
| **Observed State** | Register **configured** with 2 entries (both tabletop exercises). Fields tracked: incident ID (SCRM-IR-001, SCRM-IR-002), vendor name, severity tier, detection source, classification time, containment time, blast radius summary, vendor accountability composite, communication log, lessons learned, remediation items, status (both closed — tabletop). Register stored with 90-day retention for tabletop entries, indefinite for real incidents. |
| **Evidence** | `incident-register.json`, Screenshot #01 |
| **NIST 800-53** | IR-5 |
| **Status** | **Pass** |

---

## Remediation Tracker

| # | Control | Finding | Owner | Remediation | Target Date | Status |
|---|---------|---------|-------|-------------|-------------|--------|
| 6 | Blast radius | Network assessment partially manual — VPN/firewall rules not API-queryable | R. Myers | Evaluate network automation API or pre-stage network inventory export | 2026-Q2 | Open |
| 7 | Communication | Regulator notification template not tested; state-specific templates needed for TX, VA, CA; 2 vendor security contacts unverified | R. Myers | Build state templates, verify vendor contacts, test regulator template in next tabletop | 2026-03-15 | Open |

---

## Watchstander Notes

1. **Two tabletop exercises tell two different stories.** Tabletop 1 (credential compromise) was clean: fast containment, cooperative vendor, limited blast radius. Tabletop 2 (data breach) was messy: PII in the blast radius, 7-day vendor disclosure delay, regulatory exposure, incomplete vendor cooperation. Both were realistic. Real incidents will be somewhere between them. You need to be ready for both ends of the spectrum, not just the clean scenario.

2. **52 seconds to contain vendor credentials.** That number matters. When a vendor tells you their credentials may be compromised, every minute their accounts are active in your environment is a minute the attacker could be using them. The automated playbook removes the human from the critical path. The human investigates after containment, not before. Same principle as ITDR Pack 09 — contain first, investigate second.

3. **The 7-day disclosure gap is the real finding.** HR-Cloud SaaS's breach window was Jan 28 – Feb 2. They notified on Feb 9. That's 7 days where your employee PII was potentially exposed and you didn't know. The contractual SLA was 48 hours. This isn't just a scorecard finding — it's a contract amendment conversation. The post-incident review turned a tabletop exercise into an actionable contract negotiation point. That's what post-incident reviews are for.

4. **Blast radius is a pillar exercise, not a silo exercise.** The blast radius assessment pulls from identity (who has access), data (what's at risk), software (is the code compromised), network (what paths exist), and financial (what's the exposure). No single pack can answer the question alone. This is the operating picture your mentor described — and it only works because the pillars are built and connected. Without the identity pillar sealed, the blast radius assessment would have a blind spot on the most critical vector.

---

*Assessment conducted by Robert Myers, MBA | SailPoint ISL, Security+, CCSK, CC*
*Stella Maris Governance — 2026*
