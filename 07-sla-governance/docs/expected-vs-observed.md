# The Law of Evidence: Expected vs. Observed

## SLA Governance & Monitoring

> **Assessment Date:** 2026-02-12 [SAMPLE — replace with your assessment date]
> **Environment:** Stella Maris Lab — SLA Registry + Monitoring Dashboard [SAMPLE]
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

### 1 — SLA Terms Extracted from All Vendor Contracts

| Field | Detail |
|-------|--------|
| **Expected State** | Every Critical and High vendor contract reviewed. SLA terms extracted into structured registry with: metric name, category, target value, measurement method, penalty clause (if any), and escalation path. |
| **Observed State** | **5 vendor contracts** reviewed. SLA extraction results: **CloudPlatform Corp:** 8 measurable SLAs extracted. Uptime: 99.95%. Sev-1 response: 15 min. Incident notification: 24 hours. RTO: 2 hours. RPO: 15 min. Vulnerability remediation (critical): 48 hours. Data export: 14 days. Service credit clause: yes (10% monthly fee per 0.1% below uptime SLA). **IdentityFirst Inc:** 5 measurable SLAs extracted. Uptime: 99.9%. Sev-1 response: 30 min. Incident notification: 48 hours. Attestation renewal: before expiry. Service credit clause: yes (5% monthly fee). **HR-Cloud SaaS:** 4 measurable SLAs extracted. Uptime: 99.9%. Sev-1 response: 1 hour. Breach notification: 48 hours. Data deletion: 90 days post-termination. Service credit clause: no — "best effort remediation" only. **SecureDefend Tools:** 6 measurable SLAs extracted. Uptime: 99.95%. Sev-1 response: 15 min. Incident notification: 24 hours. Vulnerability patch (critical): 24 hours. SBOM refresh: per major release. Service credit clause: yes. **BackupVault Pro:** 2 measurable SLAs extracted. Uptime: 99.9%. Sev-1 response: 4 hours. All other terms are "reasonable effort" or "commercially reasonable timeframe." No service credit clause. No incident notification SLA. **Total: 25 measurable SLA metrics** across 5 vendors. HR-Cloud SaaS and BackupVault Pro have significant gaps in measurable commitments — flagged for contract amendment. |
| **Evidence** | `sla-registry.json`, contract review notes |
| **NIST 800-53** | SA-4 |
| **Status** | **Pass** |

---

### 2 — SLA Registry Built and Classified

| Field | Detail |
|-------|--------|
| **Expected State** | Centralized registry with all SLA metrics organized by vendor and category. Each entry includes target, measurement method, current monitoring status, and penalty clause. |
| **Observed State** | `sla-registry.json` **populated** with 25 SLA metrics across 5 categories: Availability (7 metrics), Incident Response (5 metrics), Support (5 metrics), Security & Compliance (5 metrics), Data & Operations (3 metrics). Each metric tagged with: vendor, category, target value, measurement method (automated/manual/vendor-reported), monitoring status (active/planned/not monitored), and penalty clause (credit/escalation/none). **20 of 25 metrics** have defined measurement methods. **5 metrics** rely on vendor self-reporting with no independent verification capability (vendor-side RTO, RPO, internal incident detection time). |
| **Evidence** | `sla-registry.json`, Screenshot #01 |
| **NIST 800-161** | SR-3 |
| **Status** | **Pass** |

---

### 3 — Availability Monitoring Active for Critical/High Vendors

| Field | Detail |
|-------|--------|
| **Expected State** | Uptime monitoring configured for all Critical and High vendor services. Synthetic health checks or status page monitoring running. Downtime events logged with timestamps. |
| **Observed State** | **5 vendor services** monitored: CloudPlatform Corp: synthetic health check every 5 minutes. 30-day uptime: **99.97%** (target: 99.95%). 1 incident: 12-minute degradation Feb 3 (API latency, not full outage). SLA met. IdentityFirst Inc: status page monitoring + synthetic auth check every 10 minutes. 30-day uptime: **99.88%** (target: 99.9%). 2 incidents: 45-minute outage Jan 28 (planned maintenance without advance notice — SLA breach, Category: Availability + Process), 18-minute degradation Feb 6 (auth service slow). **Below SLA target.** HR-Cloud SaaS: status page monitoring. 30-day uptime: **99.94%** (target: 99.9%). SLA met. No incidents. SecureDefend Tools: agent heartbeat monitoring. 30-day uptime: **99.99%** (target: 99.95%). SLA met. BackupVault Pro: synthetic backup verification every hour. 30-day uptime: **99.72%** (target: 99.9%). 3 incidents: 2-hour outage Jan 22, 45-minute outage Feb 1, 30-minute degradation Feb 9. **Below SLA target.** |
| **Evidence** | Monitoring dashboard, Screenshot #02 |
| **NIST 800-53** | SA-9 |
| **Status** | **Pass** |

---

### 4 — Support Ticket SLA Tracking Operational

| Field | Detail |
|-------|--------|
| **Expected State** | Support ticket response and resolution times tracked against SLA targets. Sev-1 through Sev-3 response time SLAs measured. Breaches flagged automatically. |
| **Observed State** | ITSM integration **configured** for ticket tracking. 30-day results across 5 vendors: **CloudPlatform Corp:** 2 Sev-1 tickets. Response: 8 min, 12 min (SLA: 15 min). Both met. 5 Sev-2 tickets: all within 1-hour SLA. **IdentityFirst Inc:** 1 Sev-1 ticket (Jan 28 outage). Response: 22 min (SLA: 30 min). Met. 3 Sev-2 tickets: all met. **HR-Cloud SaaS:** 0 Sev-1 tickets. 4 Sev-2 tickets: 3 met, 1 responded in 2.5 hours (SLA: 1 hour). **SLA breach.** **SecureDefend Tools:** 1 Sev-1 ticket. Response: 6 min (SLA: 15 min). 2 Sev-2 tickets: both met. **BackupVault Pro:** 3 Sev-1 tickets (during outages). Response: 45 min, 1 hr 12 min, 2 hr 30 min (SLA: 4 hours). All technically met — but 4-hour SLA for Sev-1 is weak compared to industry standard. Flagged for contract amendment. |
| **Evidence** | ITSM ticket export, Screenshot #02 |
| **NIST 800-53** | SA-9 |
| **Status** | **Pass** |

---

### 5 — Incident Notification Timeliness Measured

| Field | Detail |
|-------|--------|
| **Expected State** | Vendor incident notification measured against contractual SLA. Timestamp comparison: vendor-detected → vendor-notified-client. Late notifications documented as SLA breach. Cross-referenced with Pack 05 incident timeline. |
| **Observed State** | **3 incident notifications** measured in 30 days: **IdentityFirst Inc (Jan 28 maintenance outage):** No advance notification. SLA requires 48-hour advance notice for planned maintenance. **SLA breach — notification.** Vendor acknowledged error, attributed to "internal communication gap." **BackupVault Pro (Jan 22 outage):** Vendor notified 6 hours post-detection. No contractual notification SLA exists. Documented but cannot score as breach — no SLA to breach. **Flagged for contract amendment.** **BackupVault Pro (Feb 1 outage):** Vendor notified 4 hours post-detection. Same issue — no contractual SLA. No Pack 05 tabletop incidents involved real notification SLA measurement. Tabletop 2 (HR-Cloud) simulated a 7-day disclosure delay — this informed the finding that HR-Cloud's 48-hour breach notification SLA needs enforcement mechanism. |
| **Evidence** | Vendor notification log, Pack 05 cross-reference |
| **NIST 800-53** | SA-4 |
| **Status** | **Pass** |

---

### 6 — SLA Breach Register Active and Logging

| Field | Detail |
|-------|--------|
| **Expected State** | Every SLA breach logged: vendor, metric, target, actual, severity, disposition (credit requested, escalated, accepted, remediated). Breach register enables pattern analysis. |
| **Observed State** | `sla-breach-tracker.json` **active** with **6 breaches** logged in 30 days: |
| | (1) **IdentityFirst — Uptime:** 99.88% vs 99.9% target. Severity: Moderate. Disposition: vendor notified, monitoring elevated. |
| | (2) **IdentityFirst — Maintenance notification:** No advance notice for planned maintenance. Severity: Moderate. Disposition: vendor acknowledged, process correction committed. |
| | (3) **HR-Cloud SaaS — Sev-2 response:** 2.5 hours vs 1-hour SLA. Severity: Minor. Disposition: logged, first occurrence. |
| | (4) **BackupVault Pro — Uptime:** 99.72% vs 99.9% target. Severity: Major (3 outages in 30 days). Disposition: vendor escalation initiated. |
| | (5) **BackupVault Pro — Uptime (pattern):** Recurring outages (Jan 22, Feb 1, Feb 9). Severity: Major. Disposition: pattern flag, corrective action requested. |
| | (6) **BackupVault Pro — Service credits:** Contract has no service credit clause. Severity: governance gap. Disposition: flagged for contract amendment. |
| | **Breach distribution:** BackupVault Pro: 3 breaches (50%). IdentityFirst Inc: 2 breaches (33%). HR-Cloud SaaS: 1 breach (17%). CloudPlatform Corp: 0. SecureDefend Tools: 0. |
| **Evidence** | `sla-breach-tracker.json`, Screenshot #03 |
| **NIST 800-161** | SR-3 |
| **Status** | **Pass** |

---

### 7 — SLA Compliance Scores Calculated (90-Day Rolling)

| Field | Detail |
|-------|--------|
| **Expected State** | Every vendor receives a weighted SLA compliance score on a rolling 90-day window. Scores feed Pack 04 Relationship Health category. |
| **Observed State** | `calculate-sla-compliance.py` **operational.** 30-day scores (90-day baseline accumulating): **CloudPlatform Corp:** 100% — all 8 SLAs met. Status: Exemplary. **SecureDefend Tools:** 100% — all 6 SLAs met. Status: Exemplary. **IdentityFirst Inc:** 82% — 2 breaches (uptime, maintenance notification). Status: Underperforming. Weighted impact: Availability breach (30% weight) + Incident Response breach (25% weight) = significant score impact despite only 2 of 5 SLAs missed. **HR-Cloud SaaS:** 91% — 1 breach (Sev-2 support response). Status: Compliant. Minor breach, first occurrence, low-weight category (15%). **BackupVault Pro:** 58% — 3 breaches (uptime pattern, no credits, no notification SLA). Status: Non-Compliant. Availability breach is 30% weight and recurring. Scores fed to Pack 04 Relationship Health category. |
| **Evidence** | `calculate-sla-compliance.py` output, Screenshot #02 |
| **NIST 800-53** | SA-9 |
| **Status** | **Pass** |

---

### 8 — Pattern Analysis Identifies Recurring Failures

| Field | Detail |
|-------|--------|
| **Expected State** | `sla-pattern-analysis.py` detects recurring SLA breaches by vendor, category, and timeframe. Three or more breaches in the same category within 90 days triggers a pattern flag. |
| **Observed State** | Pattern analysis **executed.** **1 pattern identified:** BackupVault Pro — Availability. 3 outages in 30 days (Jan 22, Feb 1, Feb 9). Pattern classification: **Systemic.** Not random incidents but recurring infrastructure instability. Cross-reference with Pack 04 scorecard: BackupVault declining trend (-8 points / 30 days) correlates with SLA pattern. Cross-reference with Pack 02: stale SOC 2 report — vendor's control environment may be degrading. Cross-reference with Pack 06: Tier 2 entities unconfirmed, infrastructure supply chain opaque. **BackupVault Pro is now flagged across 7 packs.** Pattern finding escalated to vendor relationship owner with recommendation: initiate formal corrective action request. |
| **Evidence** | `sla-pattern-analysis.py` output, Screenshot #04 |
| **NIST 800-161** | SR-3 |
| **Status** | **Pass** |

---

### 9 — Service Credit and Penalty Enforcement Tracked

| Field | Detail |
|-------|--------|
| **Expected State** | When SLA breaches trigger contractual service credits or penalties, enforcement is tracked: credit amount, request date, vendor acknowledgment, credit applied. |
| **Observed State** | **Service credit review** conducted for all breaches: **IdentityFirst Inc:** Uptime breach (99.88% vs 99.9%). Contract clause: 5% monthly fee per 0.1% below target. Breach: 0.02% below. Credit: calculated at $XX. Credit request **not yet submitted** — first occurrence, under review whether to enforce or use as leverage for improved maintenance notification process. **BackupVault Pro:** Uptime breach (99.72% vs 99.9%). **No service credit clause in contract.** Cannot enforce financially. Finding: governance gap. Recommendation: add service credit clause at contract renewal. **HR-Cloud SaaS:** Sev-2 response breach. **No service credit clause for support SLA.** "Best effort remediation" language only. Cannot enforce. |
| **Finding** | Only 3 of 5 vendor contracts have service credit clauses. 2 vendors (HR-Cloud SaaS, BackupVault Pro) have no financial enforcement mechanism. SLA breaches for these vendors can only be addressed through escalation and contract amendment — not financial consequence. |
| **Status** | **Fail** — service credit enforcement not possible for 40% of vendors due to contract gaps |

---

### 10 — SLA Compliance Feeds Pack 04 Scorecard

| Field | Detail |
|-------|--------|
| **Expected State** | SLA compliance scores feed Pack 04 Vendor Security Scorecard Relationship Health category (15% of composite). SLA pattern findings trigger scorecard alerts. |
| **Observed State** | **Feed active.** SLA compliance scores reflected in Pack 04 Relationship Health: CloudPlatform Corp: SLA 100% → Relationship Health: 90 (SLA is one input among several). SecureDefend Tools: SLA 100% → Relationship Health: 88. IdentityFirst Inc: SLA 82% → Relationship Health dropped from 72 to 68 (SLA underperformance + questionnaire non-response compounding). HR-Cloud SaaS: SLA 91% → Relationship Health: 65 (minor SLA impact, but existing non-responsiveness on pen test and SBOM weighs more). BackupVault Pro: SLA 58% → Relationship Health dropped from 58 to 48. **Category threshold breach (< 40 proximity).** Approaching alert trigger. |
| **Finding** | BackupVault Pro Relationship Health now at 48 — approaching the category threshold of 40 that would trigger a scorecard alert. If the next 30 days include another SLA breach, the alert fires. |
| **Status** | **Partial** — feed active and scoring correctly, but 30-day data only; 90-day rolling confidence requires 60 more days |

---

## Remediation Tracker

| # | Control | Finding | Owner | Remediation | Target Date | Status |
|---|---------|---------|-------|-------------|-------------|--------|
| 1 | SLA extraction | HR-Cloud and BackupVault have significant gaps in measurable SLA terms | R. Myers | Contract amendment: add measurable SLAs for incident notification, vulnerability remediation, SBOM refresh | Next renewal | Open |
| 9 | Service credits | 2 of 5 vendors have no service credit clause — cannot enforce financially | R. Myers | Add service credit clauses at contract renewal for HR-Cloud and BackupVault | Next renewal | Open |
| 10 | Scorecard feed | 30-day data only; 90-day baseline required for statistical confidence | R. Myers | Time-based — continue accumulating | 2026-05-12 | Open |

---

## Watchstander Notes

1. **BackupVault Pro is now flagged across 7 packs. The data is undeniable.** Pack 01: conditional risk score (69). Pack 02: stale SOC 2 with carve-out. Pack 03: no SBOM provided. Pack 04: declining scorecard (68, Watch). Pack 05: no incident notification SLA to measure. Pack 06: Tier 2 opaque, questionnaire non-response, Subcontractor Risk 15/100. Pack 07: SLA non-compliant (58%), recurring outage pattern, no service credits. No single pack made this case. All seven together make it irrefutable. This is the operating picture. This is why you build all the packs, not just the ones that are easy.

2. **"Best effort" is not an SLA.** HR-Cloud SaaS and BackupVault Pro have contracts with language like "commercially reasonable timeframe" and "best effort remediation." These are unenforceable commitments. You cannot measure "best effort." You cannot score it. You cannot trigger a service credit against it. If the SLA doesn't have a number, it isn't an SLA — it's a suggestion. The contract amendment list writes itself from this pack.

3. **The IdentityFirst maintenance notification failure reveals process, not malice.** They had an outage because they did planned maintenance without telling you. They acknowledged the error. They committed to process correction. That's the response of a vendor who made a mistake, not a vendor with systemic problems. The SLA breach is documented and scored, but the vendor's response quality matters in the assessment. Context always matters.

4. **SLA governance is the Duty of Fiscal Stewardship applied to vendor performance.** You're paying for 99.9% uptime. If you're getting 99.72%, you're paying for something you're not receiving. In FinOps terms, that's waste — you're paying premium price for sub-premium service. SLA governance isn't just a compliance exercise. It's a financial accountability exercise. The service credit clause is the mechanism. The measurement is the evidence. The pack is the discipline.

---

*Assessment conducted by Robert Myers, MBA | SailPoint ISL, Security+, CCSK, CC*
*Stella Maris Governance — 2026*
