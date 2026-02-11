# Vendor Risk Assessment — Operations Runbook

> **Version:** 1.0.0 | **Author:** Robert Myers, MBA | Stella Maris Governance

---

## 1. Purpose and Scope

Operational procedures for vendor risk assessment, classification, scoring, approval, and ongoing governance. Treats every vendor relationship as a supply chain node that must be inventoried, inspected, and continuously monitored.

**Scope:** All third-party vendors, SaaS providers, cloud service providers, contractors, and subprocessors that access organizational data, systems, or infrastructure.

**Out of Scope:** Internal departments, employee contractors managed through identity lifecycle (see Pack 06 — Vendor/Guest vIAM for identity governance of vendor personnel).

---

## 2. Prerequisites

| Requirement | Detail |
|-------------|--------|
| Vendor risk policy | Approved by leadership with defined risk appetite |
| Intake form | Deployed in SharePoint or GRC platform |
| Scoring model | `risk-scoring-model.json` configured with organizational weights |
| Approval workflow | Power Automate or GRC tool with tiered routing |
| Log Analytics | Workspace connected for audit trail |
| Schema validator | `schema_validation.py` tested and scheduled weekly |

---

## 3. New Vendor Intake

### When a Business Unit Requests a New Vendor

1. Business unit submits intake form (SharePoint or GRC tool)
2. Mandatory fields enforced: vendor name, sponsor, data classification, integration type, business criticality
3. System auto-calculates preliminary tier:

| Data Classification | Mission Critical | Important | Standard | Convenience |
|-------------------|-----------------|-----------|----------|-------------|
| Restricted | Critical | Critical | High | High |
| Confidential | Critical | High | High | Medium |
| Internal | High | Medium | Medium | Low |
| Public | Medium | Low | Low | Low |

4. Preliminary tier triggers assessment depth:
   - Critical/High → Full 6-domain assessment
   - Medium → Abbreviated 3-domain assessment
   - Low → Self-attestation with spot verification

> **Watchstander Note:** Business units will push for "Low" classification to skip assessment. The matrix is the arbiter, not the requester. If the vendor touches Confidential data, the tier is at minimum High regardless of what the business unit writes on the form.

---

## 4. Conducting a Full Assessment (Critical/High)

### 4.1 Security Posture (30%)

- Request: current penetration test summary, vulnerability management cadence, MFA status, encryption standards
- Verify: SOC 2 Type II or ISO 27001 (forward to Pack 02 for attestation validation)
- Score each sub-metric 0-100, average for domain score

### 4.2 Compliance Status (20%)

- Request: SOC 2 Type II report, ISO 27001 certificate, FedRAMP authorization (if federal), CMMC certification (if defense)
- Verify: is the report current? Does the scope cover the services you're using? Are there qualified opinions or exceptions?
- Do not accept a vendor's claim of compliance. Verify the artifact. (Pack 02)

### 4.3 Data Handling (20%)

- What data will they access? Where is it stored? Is it encrypted at rest and in transit?
- What is their retention policy? How do they dispose of data at contract end?
- Do they process data in jurisdictions that create regulatory exposure?

### 4.4 Financial Stability (10%)

- Publicly traded: review latest 10-K or annual report
- Private: request financial summary or reference from financial institution
- Calculate burn rate if data is available: monthly operating expense / cash on hand
- **Burn rate flag:** if burn rate exceeds 30% annually, flag for elevated monitoring

> **Watchstander Note:** A financially unstable vendor is a supply chain single point of failure. If they go under, your data goes with them unless you have a tested exit plan. Financial stability isn't just a nice-to-have — it's operational continuity.

### 4.5 Incident History (10%)

- Has the vendor experienced a breach in the past 3 years?
- How did they respond? Was disclosure timely and transparent?
- Are there repeat patterns? A single incident with a strong response is forgivable. A pattern is a finding.

### 4.6 Subcontractor Risk (10%)

- Who processes data on the vendor's behalf?
- Where are Tier 2 subcontractors located?
- Does the vendor's contract with their subcontractors include security requirements?
- If the vendor cannot or will not provide Tier 2 data: score this domain low and document the gap

---

## 5. Running the Scoring Engine
```bash
cd 01-vendor-risk-assessment/code
python3 calculate_risk.py --input assessment-data.json --config risk-scoring-model.json
```

Output: vendor name, domain scores, weighted total, risk status (Accept/Conditional/Elevated/Reject), burn rate flag if applicable.

**The engine is deterministic.** Same inputs, same score, every time. No assessor discretion in the math. Assessor discretion belongs in the recommendation, not the score.

---

## 6. Approval Process

| Tier | Approver | SLA |
|------|----------|-----|
| Critical | CISO + Legal (both required) | 5 business days |
| High | Security Lead | 3 business days |
| Medium | IT Manager | 2 business days |
| Low | Auto-approved | Immediate (logged) |

### Conditional Acceptance

When score falls between 60-79:
1. Document specific compensating controls required
2. Set elevated monitoring schedule (next tier up re-assessment cadence)
3. Document risk accepted and by whom
4. Set review trigger: if compensating control is not in place by target date, escalate

### Rejection

When score falls below 40:
1. Notify business unit sponsor with scoring breakdown
2. If business-critical: escalate to executive leadership
3. Executive may accept risk with documented justification
4. Executive risk acceptance logged in register with expiration date (max 90 days before re-review)

---

## 7. Ongoing Governance

### Re-Assessment Cadence

| Tier | Cadence | Lead Time Reminder |
|------|---------|-------------------|
| Critical | Quarterly | 30 days |
| High | Semi-annual | 30 days |
| Medium | Annual | 30 days |
| Low | Biennial | 60 days |

### Between Re-Assessments

- Monitor vendor security scorecard (Pack 04) for real-time signals
- Watch for vendor breach notifications
- Track financial news for Critical vendors
- Review vendor changelog for material changes to service

### Trigger-Based Re-Assessment (Outside Cadence)

Immediate re-assessment required when:
- Vendor experiences a publicly disclosed breach
- Vendor undergoes acquisition or material leadership change
- Vendor's financial stability degrades (earnings miss, layoffs, funding concerns)
- Material change to data handling or integration scope
- Regulatory action against vendor

---

## 8. Schema Validation
```bash
python3 schema_validation.py --register vendor-risk-register.json
```

Run weekly. Validates every register entry has:
- Vendor name (string, non-empty)
- Tier (Critical/High/Medium/Low)
- Risk score (0-100)
- Approval status (Approved/Conditional/Rejected/Pending)
- Approval date (ISO 8601)
- Approver (string, non-empty)
- Next re-assessment date (ISO 8601, future date)
- Compensating controls (required if Conditional)
- Burn rate flag (boolean)

> **Watchstander Note:** Schema validation is the packing slip inspection for your vendor register. In a physical supply chain, you wouldn't accept a shipment with a missing lot number. Your digital register deserves the same rigor.

---

## 9. Review Cadence

| Review | Frequency | Owner |
|--------|-----------|-------|
| Schema validation | Weekly | Automated |
| Re-assessment scan (KQL) | Weekly | Risk Owner |
| New vendor intake review | As submitted | Risk Owner |
| Full register review | Monthly | Risk Owner |
| Scoring model calibration | Semi-annual | Risk Owner + Leadership |
| Policy review | Annual | Risk Owner + Leadership |

---

## 10. Troubleshooting

**Business unit bypasses intake:** Vendor found operating without intake form. Immediate: conduct retroactive assessment. Root cause: process communication gap. Remediate: reinforce with business unit leadership that no vendor activates without intake.

**Vendor refuses to provide assessment data:** Score "Security Posture" domain conservatively (assume worst case). Escalate to vendor relationship owner. If Critical/High vendor refuses basic transparency, that is itself a finding — document and factor into score.

**Score disputed by business unit:** Re-run `calculate_risk.py` with the same inputs. Show domain breakdown. The engine is deterministic. If the dispute is about the inputs, review the assessment evidence together. If the dispute is about the thresholds, escalate to leadership for risk appetite recalibration.

---

*Stella Maris Governance — 2026*
