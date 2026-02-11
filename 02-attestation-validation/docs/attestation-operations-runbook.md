# Attestation Validation — Operations Runbook

> **Version:** 1.0.0 | **Author:** Robert Myers, MBA | Stella Maris Governance

---

## 1. Purpose and Scope

Operational procedures for validating third-party attestation reports. Every report a vendor provides is inspected, not filed. We read the report.

**Scope:** SOC 2 Type II, ISO 27001, penetration test reports, FedRAMP/StateRAMP authorizations, and vendor self-assessments.

**Out of Scope:** Vendor intake and risk scoring (Pack 01), continuous monitoring (Pack 04), software component analysis (Pack 03).

---

## 2. Prerequisites

| Requirement | Detail |
|-------------|--------|
| Pack 01 operational | Vendors classified by tier with attestation requirements assigned |
| Attestation tracker | Deployed and populated with vendor records |
| Validation checklists | SOC 2 (15-point), ISO (10-point), pen test (12-point) loaded |
| CUEC mapping template | `cuec-gap-analysis.json` linked to identity pillar packs |
| Expiry scanner | `attestation-expiry-scan.kql` running weekly |

---

## 3. Receiving an Attestation Report

When a vendor provides an attestation:

1. Log it in the attestation tracker: vendor name, report type, issue date, expiry date, auditor name
2. Determine validation depth by vendor tier:
   - Critical/High: full checklist validation
   - Medium: abbreviated validation (scope + currency + findings)
   - Low: log receipt, spot-check one item
3. Assign validation to assessor
4. Target: complete validation within 5 business days of receipt

> **Watchstander Note:** A report that sits in an inbox for 30 days is not governance. It's a backlog. The 5-day SLA exists because attestation data feeds Pack 01 scoring. A stale validation delays risk-informed decisions.

---

## 4. SOC 2 Type II Validation (Critical/High Vendors)

Work through all 15 points in `soc2-validation-checklist.json`. For each point:

1. **Read the relevant section of the report** — not the vendor's summary, the actual report
2. **Document the finding** — what you found, not what you expected
3. **Mark pass/conditional/fail** for each checkpoint
4. **Flag any finding that impacts your risk** — scope mismatch, carve-out, exception, stale date

### Key Sections to Read First

- **Section I (Auditor's Opinion):** Qualified or unqualified? Any reservations?
- **Section III (Description of the System):** Does this match the service you use?
- **Section IV (Trust Service Criteria):** Which criteria are covered?
- **Section V (Tests and Results):** Where are the exceptions?
- **Complementary User Entity Controls:** What does the vendor expect you to do?

### Common Findings

| Finding | Frequency | Impact |
|---------|-----------|--------|
| Scope doesn't cover your specific product/service | Very common | Report is irrelevant to your risk |
| Subservice organization carved out | Common | Gap in the assurance chain |
| Exceptions in access management or change management | Common | Indicates control weakness |
| Report > 12 months old with no bridging letter | Common | Assurance gap between report and today |
| CUECs not mapped to your controls | Very common | Hidden dependency |

---

## 5. ISO 27001 Validation (Critical/High Vendors)

Work through all 10 points in `iso27001-validation-checklist.json`.

### Key Actions

1. **Verify the certificate** on the certification body's public registry — do not accept a PDF alone
2. **Request the Statement of Applicability (SoA)** — vendors may resist; the SoA shows what's excluded
3. **Check surveillance audit status** — a certificate without recent surveillance is weakening
4. **Verify transition to 2022 version** — the 2013 version deadline passed October 2025

### Common Findings

| Finding | Frequency | Impact |
|---------|-----------|--------|
| Scope covers parent company, not subsidiary you contract with | Common | Certificate doesn't apply to your vendor relationship |
| SoA excludes relevant controls (e.g., mobile, physical) | Common | Control gaps in areas that matter to you |
| Surveillance audit overdue | Uncommon | Certificate validity in question |
| Still on 2013 version | Declining | Indicates slow governance maturity |

---

## 6. Penetration Test Validation (Critical/High Vendors)

Work through all 12 points in `pentest-validation-checklist.json`.

### Key Actions

1. **Request the full technical report** for Critical vendors — executive summaries hide detail
2. **Verify tester independence** — internal pen tests are not independent attestation
3. **Check remediation status** — findings without remediation evidence are open risks
4. **Compare to prior year** — same finding categories in consecutive years indicate systemic weakness

### When a Vendor Refuses to Share

Document the refusal. Score the pen test component of Compliance Status at zero. Feed the zero back to Pack 01. The math handles the consequence. The conversation becomes data-driven.

> **Watchstander Note:** A vendor who calls their pen test "confidential" is protecting themselves, not you. In a physical supply chain, a manufacturer who won't show the quality inspection doesn't ship parts to your assembly line. Same standard.

---

## 7. CUEC Gap Analysis

After every SOC 2 validation:

1. Extract all CUECs from the report
2. For each CUEC, identify the corresponding internal control:
   - Map to specific identity pack and control number
   - Verify the mapped control is operational (check E-v-O status)
3. Document in `cuec-gap-analysis.json`:
   - Vendor, CUEC requirement, internal control mapping, last verification date, status
4. If a CUEC has no corresponding internal control: **that is a gap**
   - Escalate to risk owner
   - Either implement the control or document risk acceptance

### CUEC Re-Validation

Quarterly: re-verify all CUEC mappings. If a referenced identity pack control degrades (e.g., access reviews paused, CA policy disabled), the CUEC mapping becomes invalid. Update status from VALIDATED to GAP and trigger remediation.

---

## 8. Feeding Results to Pack 01

After validation is complete:

1. Update attestation tracker with validation status and findings
2. Re-run `calculate_risk.py` for the vendor with updated Compliance Status inputs:
   - Validated report = full credit
   - Conditional report = reduced credit (pro-rate by checklist pass rate)
   - Missing/expired report = zero credit
3. Update Pack 01 vendor risk register with new score
4. If score change crosses a threshold (e.g., Accept → Conditional), trigger re-approval workflow

---

## 9. Review Cadence

| Review | Frequency | Owner |
|--------|-----------|-------|
| Expiry scan (KQL) | Weekly | Risk Owner |
| New attestation validation | Within 5 days of receipt | Assessor |
| CUEC re-validation | Quarterly | Risk Owner |
| Full attestation program review | Semi-annual | Risk Owner + Leadership |
| Checklist calibration | Annual | Risk Owner |

---

## 10. Troubleshooting

**Vendor provides wrong report type:** Vendor sends SOC 2 Type I instead of Type II. Type I describes controls at a point in time but doesn't test them. Request Type II. If unavailable, document the limitation and score accordingly.

**Report scope is ambiguous:** Contact the vendor's GRC team directly. Request clarification in writing. If scope remains unclear, assume it doesn't cover your services and score conservatively.

**Vendor claims "in progress" for expired report:** Document the gap. Set a 30-day deadline for receipt. If not received, Compliance Status score drops to zero for that attestation. The math handles the escalation.

**CUEC maps to a control you don't have:** This is a finding, not a failure. Options: implement the control, accept the risk with documentation, or add a compensating control. All three are valid if documented.

---

*Stella Maris Governance — 2026*
