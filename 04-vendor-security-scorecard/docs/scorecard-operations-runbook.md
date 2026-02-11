# Vendor Security Scorecard — Operations Runbook

> **Version:** 1.0.0 | **Author:** Robert Myers, MBA | Stella Maris Governance

---

## 1. Purpose and Scope

Operational procedures for continuous vendor security monitoring between assessment cycles. The scorecard is the surveillance camera. The assessment is the photograph. This runbook operates the camera.

**Scope:** All Critical and High vendors. Medium vendors monitored at reduced signal depth. Low vendors not scored.

**Out of Scope:** Vendor intake and assessment (Pack 01), attestation validation (Pack 02), SBOM governance (Pack 03). These packs are data sources — this pack consumes their output.

---

## 2. Prerequisites

| Requirement | Detail |
|-------------|--------|
| Pack 01 operational | Vendor register with tier classification and risk scores |
| Pack 02 operational | Attestation tracker with expiry dates |
| Pack 03 operational | SBOM register with CVE correlation feed |
| Vendor domains enumerated | Primary domains for all Critical/High vendors |
| Sentinel connected | Vendor account sign-in and activity logs flowing |
| 30-day baseline | Minimum data collection before trusting trends |

---

## 3. Standing Watch: Daily Operations

### Signal Collection Schedule

| Cadence | Signal | Action |
|---------|--------|--------|
| **Continuous** | Vendor sign-in anomalies (via ITDR) | Auto-alerted. Verify acknowledgment. |
| **Daily** | SSL/TLS validity, breach database, SBOM CVE feed | Automated. Review alerts only. |
| **Weekly** | Exposed services (Shodan), dark web, DNS health, CIEM PCI, regulatory actions | Run `external-signal-check.py`. Review output. |
| **Monthly** | Financial signals, SLA compliance, responsiveness, full scorecard review | Manual review + scorecard refresh. |
| **Quarterly** | Burn rate recalculation, SEC filing review (public vendors) | Update financial scores. |

### Morning Check (5 minutes)

1. Any scorecard alerts fired overnight? If yes — investigate per Section 5.
2. Any breach database hits? If yes — immediate escalation per Section 6.
3. Any Pack 02/03 feed updates? If yes — verify scorecard auto-updated.

> **Watchstander Note:** Most mornings are quiet. The discipline is checking anyway. The one morning you skip is the morning the signal was there.

---

## 4. Running the Scorecard

### Weekly Scorecard Refresh
```bash
# Run external signal checks
python3 external-signal-check.py --vendors vendor-domains.json --output signals.json

# Calculate composite scores
python3 calculate-scorecard.py --signals signals.json --register scorecard-register.json

# Run trend analysis
# KQL: scorecard-trend-scan.kql in Sentinel
```

### Interpreting Results

- **Score change > 5 points from last week:** Investigate which category drove the change
- **Category score below 40:** Alert fires automatically. Investigate immediately.
- **Trend flipped from Stable to Declining:** Schedule vendor engagement within 14 days

---

## 5. Alert Response

When a scorecard alert fires:

### Composite Below 60 (Concern)

1. Acknowledge alert within 4 hours
2. Identify which category or categories drove the drop
3. Cross-reference with Pack 01/02/03 for contributing findings
4. Notify vendor relationship owner
5. Trigger out-of-cycle Pack 01 re-assessment
6. Document in monthly review

### Composite Below 40 (Critical)

1. Acknowledge immediately
2. Escalate to CISO
3. Activate contingency planning:
   - Is there an alternative vendor?
   - What is the migration timeline?
   - What compensating controls can be applied immediately?
4. Schedule vendor executive-level engagement within 48 hours
5. Document as incident in Pack 05

### Category Below 40

1. Acknowledge within 4 hours
2. Investigate root cause in that specific category
3. Determine if root cause is transient (e.g., certificate renewal in progress) or systemic
4. If systemic: notify vendor and set remediation deadline
5. If transient: monitor for resolution within defined timeframe

### Rapid Decline (>15 Points in 90 Days)

1. Review full 90-day signal history
2. Identify inflection point — when did the decline start and what changed?
3. Cross-reference all 5 categories for compounding signals
4. Trigger out-of-cycle re-assessment
5. Present full trajectory to risk owner with recommendation

---

## 6. Breach Database Hit Response

When a vendor domain appears in a breach database:

1. **Immediate** (within 1 hour):
   - Verify the breach database entry is current and relevant
   - Determine scope: what type of data was exposed?
   - Cross-reference with vendor's own disclosure (if any)

2. **Within 4 hours:**
   - Contact vendor security team directly
   - Request: incident scope, timeline, impact to your data, remediation status
   - Activate Pack 05 (Supply Chain Incident Response) if your data may be affected

3. **Within 24 hours:**
   - Update scorecard (External Posture category drops)
   - Assess whether vendor accounts in your environment should be restricted
   - Brief CISO if Critical vendor

4. **Ongoing:**
   - Monitor vendor's incident response quality
   - Score cooperation in Relationship Health category
   - Document everything — timestamps, vendor responses, your actions

---

## 7. Monthly Scorecard Review

First Monday of each month:

1. Generate scorecard summary for all monitored vendors
2. Review each vendor:
   - Current composite score and category breakdown
   - 30-day score change (and 90-day trend once available)
   - Alerts fired and disposition
   - Cross-pillar updates (new Pack 01/02/03 findings)
3. Identify:
   - Vendors requiring engagement
   - Vendors approaching threshold boundaries
   - Trends that need watching
4. Recommendations for next period
5. Archive review document

### Review Template
```markdown
## Monthly Scorecard Review — [Month Year]

### Vendor Summary
| Vendor | Composite | Trend | Alerts | Action Required |
|--------|-----------|-------|--------|-----------------|

### Key Findings

### Recommendations

### Next Review: [Date]
```

---

## 8. Vendor Engagement Triggers

| Trigger | Engagement Level | Timeline |
|---------|-----------------|----------|
| Category < 40 | Security team email | 48 hours |
| Composite entering "Watch" (70-79) | Relationship owner notified | 7 days |
| Composite entering "Concern" (< 60) | Vendor executive meeting | 14 days |
| Composite entering "Critical" (< 40) | CISO-to-CISO call | 48 hours |
| Breach database hit | Security team direct contact | 1 hour |
| Declining trend confirmed (90 days) | Relationship owner meeting | 14 days |

> **Watchstander Note:** Vendor engagement is not confrontational. It's collaborative. You're showing them their own data and asking how they plan to address it. The scorecard removes emotion and replaces it with evidence. You're not accusing them of being insecure. You're showing them a declining trend and asking what changed.

---

## 9. Review Cadence

| Review | Frequency | Owner |
|--------|-----------|-------|
| Signal collection | Daily/weekly per schedule | Automated + Risk Owner |
| Scorecard refresh | Weekly | Risk Owner |
| Monthly review | Monthly | Risk Owner |
| Trend confidence assessment | Quarterly (until 90-day baseline) | Risk Owner |
| Scorecard model calibration | Semi-annual | Risk Owner + Leadership |
| Cross-pillar feed validation | Quarterly | Risk Owner |

---

## 10. Troubleshooting

**External signal check failing for a vendor:** Verify domain is correct. Some vendors use CDN/proxy that masks direct checks. Document limitation and note reduced external visibility.

**Cross-pillar feed stale:** Check Pack 02 attestation tracker and Pack 03 SBOM register update dates. If stale > 14 days, investigate feed pipeline. Scorecard is only as current as its inputs.

**False positive on breach database:** HaveIBeenPwned may include historical breaches. Verify the breach date. If > 12 months old and already known/addressed, note in scorecard but don't score again.

**Vendor disputes scorecard findings:** Share the specific signal data. The scorecard is evidence-based. If the vendor has remediated and you can verify, update the score. If they dispute without evidence, the score stands.

---

*Stella Maris Governance — 2026*
