# The Law of Evidence: Expected vs. Observed

## Vendor Security Scorecard

> **Assessment Date:** 2026-02-11 [SAMPLE — replace with your assessment date]
> **Environment:** Stella Maris Lab — Scorecard Dashboard + Signal Feeds [SAMPLE]
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

### 1 — External Security Signal Monitoring Active

| Field | Detail |
|-------|--------|
| **Expected State** | All Critical and High vendor domains monitored for SSL/TLS health, DNS configuration, exposed services, breach database presence, and dark web mentions. Checks run on defined cadence. |
| **Observed State** | `external-signal-check.py` **operational** across 5 Critical/High vendor primary domains. **SSL/TLS:** Daily checks. All 5 vendors current. CloudPlatform Corp: TLS 1.3, cert expires Aug 2026. BackupVault Pro: TLS 1.2 (flagged — 1.3 recommended but not required). **DNS:** Daily checks. 4 of 5 vendors have SPF + DKIM + DMARC. HR-Cloud SaaS: DMARC policy set to "none" (monitoring only, not enforcing) — scored as partial. **Exposed services:** Weekly Shodan check. CloudPlatform Corp: expected ports only (443, 80 redirect). IdentityFirst Inc: port 8443 exposed (admin panel) — flagged, vendor notified. **Breach database:** Daily HaveIBeenPwned check. 0 new vendor domain appearances in 30 days. **Dark web:** Weekly scan. 0 vendor mentions. |
| **Evidence** | `external-signal-check.py` output, Screenshot #02 |
| **NIST 800-53** | CA-7 |
| **Status** | **Pass** |

---

### 2 — Financial Health Signal Monitoring Active

| Field | Detail |
|-------|--------|
| **Expected State** | Public company vendors monitored via SEC filings. Private vendor financial signals tracked through news monitoring and Pack 01 burn rate flags. Financial distress indicators trigger scorecard impact. |
| **Observed State** | **2 public vendors** (CloudPlatform Corp, SecureDefend Tools): SEC filings monitored quarterly. CloudPlatform Corp Q4 2025 earnings: revenue up 12% YoY, no going concern, no material weakness. SecureDefend Tools Q4 2025: revenue flat, R&D expense up 22% — no immediate concern but trend noted. **3 private vendors:** News monitoring active. IdentityFirst Inc: burn rate flag from Pack 01 (40% YoY) confirmed by 2 news articles citing "aggressive expansion." HR-Cloud SaaS: no distress signals. BackupVault Pro: 1 article noting "seeking Series C" — neutral signal, monitored. No financial score drops triggered in 30 days. IdentityFirst burn rate flag carries forward from Pack 01 (already scored). |
| **Evidence** | News monitoring log, SEC filing review notes |
| **NIST 800-161** | SR-6 |
| **Status** | **Pass** |

---

### 3 — Compliance Currency Signal Active

| Field | Detail |
|-------|--------|
| **Expected State** | Attestation expiry status from Pack 02, SBOM CVE feed from Pack 03, and regulatory action monitoring integrated into scorecard. Lapsed compliance triggers automatic score reduction. |
| **Observed State** | **Pack 02 feed active:** BackupVault Pro SOC 2 flagged as stale (13 months). Score impact: Compliance Currency category reduced from 80 to 55. HR-Cloud SaaS SOC 2 approaching stale (11 months, 60-day warning). No score impact yet — warning logged. **Pack 03 CVE feed active:** jackson-databind critical CVE affecting SecureDefend Tools SBOM. Score impact: Compliance Currency reduced from 90 to 75 until vendor confirms patch. Vendor confirmed patch Feb 8 — score restored to 85 (5-point residual for 7-day exposure window). **Regulatory monitoring:** Weekly check across FTC, GDPR enforcement, state AG actions. 0 actions against monitored vendors in 30 days. |
| **Evidence** | Screenshot #05, Pack 02/03 cross-reference logs |
| **NIST 800-53** | CA-7 |
| **Status** | **Pass** |

---

### 4 — Internal Behavior Telemetry Active

| Field | Detail |
|-------|--------|
| **Expected State** | Vendor account sign-in patterns, API call volumes, data transfer activity, and permission usage monitored. Anomalies flagged and scored. |
| **Observed State** | **Sign-in monitoring (via ITDR Pack 09):** 7 vendor service accounts and 4 vendor user accounts monitored. Baselines established (30+ days). 1 anomaly detected: BackupVault Pro service account signed in from a new IP range (Feb 5) — investigated, confirmed legitimate (vendor infrastructure migration). Acknowledged in 22 minutes. **API monitoring:** CloudPlatform Corp and HR-Cloud SaaS API activity tracked. CloudPlatform Corp: stable, within baseline. HR-Cloud SaaS: API call volume increased 2.1x baseline week of Feb 3 — investigated, correlated with vendor-side feature rollout (confirmed via vendor changelog). No malicious indicator. **Data transfer:** No anomalous bulk transfers detected. **CIEM (Pack 08):** Vendor identity PCI scores checked weekly. All vendor identities below PCI 40 (within threshold). |
| **Evidence** | Sentinel logs, CIEM output, Screenshot #02 |
| **NIST 800-53** | SA-9 |
| **Status** | **Pass** |

---

### 5 — Composite Scorecards Built for All Critical/High Vendors

| Field | Detail |
|-------|--------|
| **Expected State** | Every Critical and High vendor has a composite scorecard with scores across all 5 categories. Scorecard updated at minimum weekly. |
| **Observed State** | **5 composite scorecards** active, updated weekly. Current scores: |
| | **CloudPlatform Corp (Critical):** External 92, Financial 88, Compliance 90, Internal 95, Relationship 90. **Composite: 91 — Healthy.** |
| | **IdentityFirst Inc (Critical):** External 70 (exposed port), Financial 62 (burn rate), Compliance 68 (ISO conditional), Internal 85, Relationship 72 (slow SBOM response). **Composite: 71 — Watch.** |
| | **HR-Cloud SaaS (High):** External 78 (DMARC not enforcing), Financial 82, Compliance 60 (SOC 2 approaching stale, no pen test), Internal 80, Relationship 65 (non-responsive on pen test). **Composite: 72 — Watch.** |
| | **SecureDefend Tools (High):** External 90, Financial 80, Compliance 85 (CVE residual), Internal 92, Relationship 88. **Composite: 87 — Healthy.** |
| | **BackupVault Pro (High):** External 82, Financial 70 (seeking funding), Compliance 55 (stale SOC 2, carve-out), Internal 78, Relationship 58 (non-responsive to SBOM + re-assessment). **Composite: 68 — Watch.** |
| **Evidence** | Screenshot #01, `scorecard-register.json` |
| **NIST 800-161** | SR-6(1) |
| **Status** | **Pass** |

---

### 6 — Trend Analysis Producing 90-Day Rolling View

| Field | Detail |
|-------|--------|
| **Expected State** | 90-day rolling trend tracked for every vendor. Trend classified as Improving, Stable, Declining, or Rapid Decline. Declining trends trigger investigation. |
| **Observed State** | Trend analysis **operational** for 5 vendors. Current trends (30-day data available, 90-day accumulating): CloudPlatform Corp: **Stable** (+1 point over 30 days). SecureDefend Tools: **Stable** (-2 points over 30 days, within ±5 threshold). IdentityFirst Inc: **Declining** (-6 points over 30 days, driven by exposed port finding and SBOM non-compliance). Investigation initiated — vendor engagement meeting scheduled Feb 15. HR-Cloud SaaS: **Stable** (-3 points). BackupVault Pro: **Declining** (-8 points, driven by stale SOC 2 + non-responsiveness). Out-of-cycle re-assessment recommended. |
| **Finding** | Only 30 days of trend data available. 90-day rolling view requires 60 more days to reach full confidence. Current trends are directional but not yet statistically reliable. |
| **Evidence** | Screenshot #03, `scorecard-trend-scan.kql` output |
| **NIST 800-53** | RA-3 |
| **Status** | **Partial** — trend operational but only 30 of 90 days accumulated |

---

### 7 — Threshold Alerting Configured and Tested

| Field | Detail |
|-------|--------|
| **Expected State** | Alerts fire when: composite drops below 60 (Concern), composite drops below 40 (Critical), any single category drops below 40, rapid decline detected (>15 points in 90 days), or vendor appears in breach database. |
| **Observed State** | Alert rules **deployed** in `scorecard-alert-rules.json`. **2 alerts fired** in 30 days: (1) BackupVault Pro Compliance Currency dropped below category threshold (55) — alerted risk owner within 1 hour, investigated, root cause: stale SOC 2 + carve-out compounding. Action: renewal escalated. (2) IdentityFirst Inc exposed port flagged by external check — alerted within 6 hours of detection, vendor notified same day, port closed within 48 hours. No composite score breached "Concern" threshold (all vendors > 60). No breach database alerts. Both alerts acknowledged within SLA. |
| **Evidence** | Screenshot #04, alert logs |
| **NIST 800-53** | CA-7 |
| **Status** | **Pass** |

---

### 8 — Scorecard Triggers Out-of-Cycle Re-Assessment

| Field | Detail |
|-------|--------|
| **Expected State** | When a vendor's composite score drops to "Concern" (40-59) or trend shows "Rapid Decline" (>15 points in 90 days), an out-of-cycle re-assessment is triggered in Pack 01. The scorecard drives the assessment calendar, not just the calendar itself. |
| **Observed State** | Trigger logic **configured.** No composite score has yet reached "Concern" threshold (lowest is BackupVault Pro at 68). However, BackupVault Pro's declining trend (-8 in 30 days) is on pace for Rapid Decline if it continues. **Proactive recommendation** issued to risk owner: initiate re-assessment at next quarterly cycle (Apr 2026) rather than waiting for automated trigger. Trigger mechanism validated via controlled test: manually set test vendor composite to 55 → Pack 01 re-assessment ticket auto-generated in 4 minutes. |
| **Evidence** | Test trigger log, proactive recommendation |
| **NIST 800-161** | SR-6 |
| **Status** | **Pass** |

---

### 9 — Cross-Pillar Data Integration Verified

| Field | Detail |
|-------|--------|
| **Expected State** | Scorecard ingests data from: Pack 01 (risk score), Pack 02 (attestation status), Pack 03 (SBOM CVE feed), Identity Pack 06 (guest identity health), Identity Pack 08 (vendor PCI), Identity Pack 09 (vendor sign-in anomalies). All feeds validated as operational. |
| **Observed State** | **6 cross-pillar feeds** configured. Status: Pack 01 risk score: **Active.** All 5 vendor scores reflected in Relationship Health. Pack 02 attestation status: **Active.** Expiry alerts feeding Compliance Currency. Pack 03 SBOM CVE feed: **Active.** jackson-databind CVE reflected in SecureDefend Tools scorecard within 6 hours of correlation. Identity Pack 08 (CIEM): **Active.** Vendor PCI scores checked weekly. Identity Pack 09 (ITDR): **Active.** BackupVault Pro sign-in anomaly detected and scored. **Identity Pack 06 (Guest vIAM): Feed designed but not yet connected.** Guest lifecycle events not yet flowing to scorecard due to integration gap between SharePoint-based scorecard and Entra guest audit logs. |
| **Evidence** | Feed validation log, Screenshot #05 |
| **NIST 800-53** | CA-7 |
| **Status** | **Partial** — 5 of 6 feeds active, Pack 06 integration pending |

---

### 10 — Monthly Scorecard Review Cadence Established

| Field | Detail |
|-------|--------|
| **Expected State** | Monthly review of all vendor scorecards by risk owner. Review documents: score changes, trend directions, alerts fired, actions taken, and recommendations for next period. |
| **Observed State** | First monthly review **completed** Feb 10. Review covered: all 5 vendor scorecards, 2 alerts (both resolved), 2 declining trends (IdentityFirst and BackupVault), 0 threshold breaches. Recommendations issued: (1) Schedule IdentityFirst vendor engagement meeting re: exposed port and SBOM. (2) Escalate BackupVault SOC 2 renewal through procurement. (3) Monitor HR-Cloud SaaS SOC 2 expiry — 60-day window approaching. Review documented and archived. Next review: Mar 10. |
| **Evidence** | Monthly review document |
| **NIST 800-161** | SR-6 |
| **Status** | **Pass** |

---

## Remediation Tracker

| # | Control | Finding | Owner | Remediation | Target Date | Status |
|---|---------|---------|-------|-------------|-------------|--------|
| 6 | Trend analysis | Only 30 of 90 days accumulated — trends directional but not statistically reliable | R. Myers | Time-based — continue collecting. 90-day confidence by May 2026. | 2026-05-11 | Open |
| 9 | Cross-pillar feeds | Identity Pack 06 (Guest vIAM) feed not yet connected to scorecard | R. Myers | Build Entra guest audit log → scorecard pipeline | 2026-Q2 | Open |

---

## Watchstander Notes

1. **The scorecard is not a replacement for the assessment. It's the watch between assessments.** Pack 01 takes the photograph. The scorecard runs the surveillance camera. Both are necessary. The photograph gives you depth — the 6-domain assessment, the scoring engine, the approval workflow. The camera gives you continuity — what changed since the last photograph. Without both, you're either deep but blind, or aware but shallow.

2. **BackupVault Pro tells the whole story across 4 packs.** Pack 01: risk score 69, conditional. Pack 02: SOC 2 stale, carve-out finding. Pack 03: no SBOM provided. Pack 04: declining trend, approaching re-assessment trigger. That's not 4 separate findings. That's one vendor on a trajectory. The scorecard makes the trajectory visible. Without it, each pack sees its own finding. With it, the pattern is undeniable. This is the operating picture.

3. **The exposed port on IdentityFirst proves external monitoring works.** We found it through automated Shodan checks, not through the vendor telling us. The vendor didn't know — or didn't disclose. Either way, the external signal caught what the vendor's own attestation didn't. Port closed within 48 hours of notification. That's the value of continuous monitoring: you see what the vendor's self-reporting misses.

4. **Trend requires patience.** 30 days of data gives you direction. 90 days gives you confidence. We are transparent that the trend analysis is accumulating, not yet statistically reliable. Marking this as partial is honest. An auditor reading this in May will see 90 days of data and a trend that either confirmed or corrected our early signal. That's the discipline — document what you know and what you don't.

---

*Assessment conducted by Robert Myers, MBA | SailPoint ISL, Security+, CCSK, CC*
*Stella Maris Governance — 2026*
