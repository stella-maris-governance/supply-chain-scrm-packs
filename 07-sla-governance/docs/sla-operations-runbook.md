# SLA Governance & Monitoring — Operations Runbook

> **Version:** 1.0.0 | **Author:** Robert Myers, MBA | Stella Maris Governance

---

## 1. Purpose and Scope

Operational procedures for extracting, monitoring, scoring, and enforcing vendor SLA commitments. A promise without measurement is a suggestion. This runbook turns SLAs into measured obligations.

**Scope:** All Critical and High vendor SLAs. Medium vendors monitored for availability only.

**Out of Scope:** Internal SLAs, customer-facing SLAs. This pack governs what vendors owe you, not what you owe others.

---

## 2. Prerequisites

| Requirement | Detail |
|-------------|--------|
| Vendor contracts accessible | All Critical/High vendor contracts with SLA terms |
| Monitoring tools | Uptime monitoring, ITSM ticket tracking, status page monitoring |
| Pack 02 operational | Attestation expiry data feeds Security & Compliance SLA category |
| Pack 04 operational | SLA scores feed Relationship Health category |
| Pack 05 operational | Incident notification timeliness cross-referenced |

---

## 3. SLA Extraction Process

When a new vendor is onboarded or a contract is renewed:

1. **Obtain the full contract** including all appendices and service schedules
2. **Search for measurable commitments** — look for: percentages, time windows, response times, delivery dates
3. **For each SLA found, record:**
   - Metric name (e.g., "Monthly uptime percentage")
   - Category (Availability / Incident Response / Support / Security / Data)
   - Target value (e.g., 99.9%)
   - Measurement method (how you will verify — automated check, vendor report, ticket timestamp)
   - Penalty clause (service credit, termination right, escalation, or none)
   - Escalation path (who at the vendor to contact when breached)
4. **Flag unmeasurable terms:** "Best effort," "commercially reasonable," "reasonable timeframe" — these are not SLAs. Document and add to contract amendment list.
5. **Enter all metrics into `sla-registry.json`**

### Minimum SLA Expectations by Tier

| Tier | Minimum SLAs Expected |
|------|----------------------|
| **Critical** | Uptime (%), Sev-1 response, incident notification, breach notification, RTO, RPO, vulnerability remediation, service credit clause |
| **High** | Uptime (%), Sev-1 response, incident notification, breach notification, service credit clause |
| **Medium** | Uptime (%), Sev-1 response |

If a vendor's contract falls below the minimum for their tier, document the gap and add to contract amendment list.

> **Watchstander Note:** SLA extraction is a one-time effort per contract that pays dividends for the entire contract term. Invest the 30 minutes per contract. The alternative is discovering the SLA gap during an incident when you need leverage and don't have it.

---

## 4. Monitoring Configuration

### 4.1 Availability Monitoring

| Method | Vendor Type | Cadence |
|--------|------------|---------|
| Synthetic health check | SaaS platforms, APIs | Every 5 minutes |
| Status page monitoring | All vendors with public status pages | Continuous (webhook or poll) |
| Agent heartbeat | Security tools with installed agents | Continuous |
| Backup verification | Backup and storage vendors | Hourly |

Configure all monitors to log: timestamp, status (up/degraded/down), response time.

### 4.2 Support Ticket Tracking

Ensure ITSM tool captures:
- Ticket creation timestamp
- Severity level
- First vendor response timestamp
- Resolution timestamp
- Vendor name tag

Calculate: response time = first response - creation. Resolution time = resolution - creation.

### 4.3 Incident Notification Tracking

For every vendor-reported incident:
- Record: vendor detection timestamp (from vendor's disclosure)
- Record: client notification timestamp (when you received it)
- Calculate: notification delay = notification - detection
- Compare against contractual SLA

---

## 5. SLA Compliance Scoring

### Weekly Score Calculation
```bash
python3 calculate-sla-compliance.py --registry sla-registry.json --breaches sla-breach-tracker.json
```

### Scoring Logic

For each vendor:
1. Count total SLA commitments measured in the 90-day window
2. Count SLA commitments met
3. Calculate raw compliance: met / total × 100
4. Apply category weights:
   - Availability: 30%
   - Incident Response: 25%
   - Support: 15%
   - Security & Compliance: 20%
   - Data & Operations: 10%
5. Weighted score = Σ (category compliance × category weight)

### Score Interpretation

- 95-100%: Exemplary. Vendor exceeding commitments.
- 85-94%: Compliant. Minor issues, vendor self-correcting.
- 70-84%: Underperforming. Engagement required.
- 50-69%: Non-Compliant. Escalation + credit enforcement.
- 0-49%: Critical Breach. Contract review.

---

## 6. SLA Breach Response

When a breach is detected:

### Minor (First Occurrence, Non-Critical)

1. Log in breach tracker
2. Monitor for recurrence
3. No vendor notification required for first minor breach

### Moderate (Second Occurrence or First Critical)

1. Log in breach tracker
2. Notify vendor relationship owner
3. Send vendor notification requesting corrective action
4. Set 30-day follow-up

### Major (Third Occurrence or Operational Impact)

1. Log in breach tracker
2. Escalate to vendor executive contact
3. Request formal corrective action plan with timeline
4. Calculate and request service credits (if clause exists)
5. Feed breach to Pack 04 scorecard
6. Set 14-day follow-up

### Critical (Data Exposure, Regulatory, Business Interruption)

1. Log in breach tracker
2. Activate Pack 05 incident response if applicable
3. Notify CISO
4. Formal vendor engagement at executive level
5. Legal review of contract enforcement options
6. Evaluate vendor replacement timeline

---

## 7. Service Credit Enforcement

When a breach triggers a service credit:

1. Calculate credit amount per contractual formula
2. Document: breach date, metric, target, actual, credit calculation
3. Submit credit request to vendor billing contact
4. Track: request date, vendor acknowledgment, credit applied date
5. If vendor disputes, escalate with evidence (monitoring logs, timestamps)

> **Watchstander Note:** Service credits are not about the money. A $200 credit on a $4,000 monthly contract isn't the point. The credit is the mechanism that proves you're measuring and enforcing. It changes the vendor's behavior because it proves you're paying attention. The conversation shifts from "please do better" to "here's the data, here's the clause, here's the invoice."

---

## 8. Pattern Analysis

Monthly, run `sla-pattern-analysis.py`:
```bash
python3 sla-pattern-analysis.py --breaches sla-breach-tracker.json --window 90
```

Pattern triggers:
- 3+ breaches in same category within 90 days = **systemic pattern**
- Breaches increasing in severity = **escalating pattern**
- Same root cause cited in multiple breaches = **unresolved root cause**

When pattern identified:
1. Compile full breach history with timeline
2. Cross-reference with Pack 04 scorecard trend
3. Present to vendor with formal corrective action request
4. Set improvement targets with measurement dates
5. If no improvement within 60 days, escalate to contract review

---

## 9. Review Cadence

| Review | Frequency | Owner |
|--------|-----------|-------|
| Monitoring check | Daily (automated) | Automated |
| Breach logging | As they occur | Risk Owner |
| SLA compliance score | Weekly | Risk Owner |
| Pattern analysis | Monthly | Risk Owner |
| Full SLA review (all vendors) | Quarterly | Risk Owner + Procurement |
| Contract amendment review | At renewal | Legal + Risk Owner + Procurement |
| Service credit reconciliation | Monthly | Finance + Risk Owner |

---

## 10. Troubleshooting

**Vendor disputes uptime measurement:** Share your monitoring data. If vendor has different data, compare methodologies. Your synthetic checks measure from your perspective — which is the perspective that matters to your operations.

**Contract has no measurable SLAs:** Document the gap. Add to contract amendment list. In the interim, establish internal expectations and measure against them — the data builds the case for contract improvement.

**Vendor meets SLA technically but service is poor:** SLAs are minimums, not targets. A vendor who consistently delivers 99.91% against a 99.9% SLA is technically compliant but barely. Track trend. If declining toward threshold, engage proactively.

**Multiple vendors breach simultaneously:** Investigate whether shared Tier 2 dependency caused cascading failure (Pack 06 concentration risk). This isn't multiple independent breaches — it's one root cause. Document as systemic supply chain risk.

---

*Stella Maris Governance — 2026*
