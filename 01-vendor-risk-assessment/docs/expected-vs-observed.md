# The Law of Evidence: Expected vs. Observed

## Vendor Risk Assessment Framework

> **Assessment Date:** 2026-02-11 [SAMPLE — replace with your assessment date]
> **Environment:** Stella Maris Lab — SharePoint + Log Analytics [SAMPLE]
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

### 1 — Vendor Risk Assessment Policy Defined and Approved

| Field | Detail |
|-------|--------|
| **Expected State** | Written policy defining vendor risk assessment requirements, risk appetite, scoring thresholds, tier definitions, and approval authorities. Approved by organizational leadership. |
| **Observed State** | Policy document **approved** by tenant owner. Defines 4-tier classification model (Critical, High, Medium, Low), 6-domain weighted scoring (Security 30%, Compliance 20%, Data Handling 20%, Financial 10%, Incident History 10%, Subcontractor Risk 10%), approval authorities by tier, and re-assessment cadence. Risk appetite statement: "No vendor with score below 40 proceeds without executive risk acceptance and documented compensating controls." |
| **Evidence** | Policy document v1.0 |
| **NIST 800-161** | SR-1 |
| **Status** | **Pass** |

---

### 2 — Vendor Intake Form Deployed with Mandatory Fields

| Field | Detail |
|-------|--------|
| **Expected State** | Structured intake form captures: vendor name, business unit sponsor, data classification of data accessed, integration type, business criticality, and preliminary tier assignment. No vendor proceeds without completed intake. |
| **Observed State** | Intake form **deployed** as SharePoint list with mandatory fields. **12 vendors** processed through intake in 30 days. Fields enforced: vendor name, sponsor, data classification (Public/Internal/Confidential/Restricted), integration type (API/SSO/File Transfer/VPN/None), business criticality (Mission Critical/Important/Standard/Convenience), preliminary tier (auto-calculated from data classification × business criticality). 2 submissions rejected for incomplete fields — system enforced mandatory completion. |
| **Evidence** | Screenshot #02 |
| **NIST 800-161** | SR-5 |
| **Status** | **Pass** |

---

### 3 — All Vendors Classified by Risk Tier

| Field | Detail |
|-------|--------|
| **Expected State** | Every vendor with access to organizational data or systems classified into a risk tier. Classification based on data access level, integration depth, and business dependency. No unclassified vendors. |
| **Observed State** | **12 vendors** classified: 2 Critical (cloud IaaS provider, identity platform), 3 High (HR SaaS, security tooling, backup provider), 5 Medium (project management, CRM, communication platform, CI/CD tooling, analytics), 2 Low (office supplies, facilities). Classification documented in vendor risk register with justification for each tier assignment. |
| **Evidence** | Screenshot #01 |
| **NIST 800-161** | SR-6 |
| **Status** | **Pass** |

---

### 4 — Risk Scoring Model Operational with Schema Validation

| Field | Detail |
|-------|--------|
| **Expected State** | 6-domain weighted scoring model deployed. Every assessment produces a quantified score (0-100). Scoring is repeatable — same inputs produce same score regardless of assessor. Schema validation ensures data integrity of every register entry. |
| **Observed State** | Scoring model **operational.** `calculate_risk.py` produces deterministic scores from assessment JSON input. `schema_validation.py` validates every register entry against required schema: tier, score, date, approval status, next re-assessment. **5 full assessments** completed (2 Critical, 3 High). Scores: Cloud IaaS 84 (Accept), Identity Platform 77 (Conditional — subcontractor visibility limited), HR SaaS 72 (Conditional), Security Tooling 88 (Accept), Backup Provider 69 (Conditional). Schema validation: 0 malformed entries across 12 records. Financial Stability domain includes burn rate flag — Identity Platform flagged: 18 months cash but 40% YoY burn rate increase. |
| **Evidence** | `calculate_risk.py` output, `schema_validation.py` output, Screenshot #03 |
| **NIST 800-53** | SA-4 |
| **Status** | **Pass** |

---

### 5 — Critical and High Vendors Fully Assessed (6 Domains)

| Field | Detail |
|-------|--------|
| **Expected State** | All Critical and High vendors receive full 6-domain assessment: security posture, compliance status, data handling, financial stability (with trend analysis), incident history, and subcontractor risk. |
| **Observed State** | **5 vendors** (2 Critical, 3 High) fully assessed across all 6 domains. Assessment details: **Cloud IaaS (Critical, score 84):** SOC 2 Type II verified (Pack 02), ISO 27001 current, FedRAMP Moderate authorized, data encrypted at rest and in transit, 3 years profitable, no material breaches, Tier 2 subcontractors documented. **Identity Platform (Critical, score 77):** SOC 2 Type II verified, strong security controls, data handling compliant, financial stable but burn rate elevated (flagged), no breaches, subcontractor visibility limited to Tier 1 only — compensating control: quarterly attestation refresh required. **HR SaaS (High, score 72):** SOC 2 Type II verified, encryption in transit only (at-rest encryption planned Q2), PII handling documented, financially stable, 1 minor incident 2024 (handled well), no subcontractor data provided — finding logged. |
| **Evidence** | Assessment reports, Screenshot #03 |
| **NIST 800-161** | SR-3, SR-6 |
| **Status** | **Pass** |

---

### 6 — Approval Workflow Enforced by Tier

| Field | Detail |
|-------|--------|
| **Expected State** | Vendor approval follows tiered authority: Critical → CISO + Legal, High → Security Lead, Medium → IT Manager, Low → auto-approve with documentation. No vendor activates access before approval is recorded. |
| **Observed State** | Power Automate workflow **active.** Approval chain enforced by tier — tested with all 4 tiers. Critical: routed to CISO + Legal, both approvals required (2 vendors processed, average approval time 3 business days). High: routed to Security Lead (3 vendors, average 1.5 business days). Medium: routed to IT Manager (5 vendors, average 1 business day). Low: auto-approved with intake form logged (2 vendors). **1 rejection:** Medium vendor denied by IT Manager — justification: "Duplicate capability with existing approved vendor. Unnecessary expansion of vendor surface." |
| **Evidence** | Screenshot #04, Power Automate run history |
| **NIST 800-161** | SR-5 |
| **Status** | **Pass** |

---

### 7 — Vendor Risk Register Complete with Schema Integrity

| Field | Detail |
|-------|--------|
| **Expected State** | Centralized register of all vendors with: tier, risk score, approval status, approval date, approver, next re-assessment date, and compensating controls (if conditional). Register entries validated against schema. |
| **Observed State** | Register **maintained** in SharePoint with 12 vendor records. All fields populated. `schema_validation.py` runs weekly — **0 schema violations** in 3 weeks. Register includes: vendor name, business unit sponsor, tier, risk score, score breakdown by domain, approval status (approved/conditional/rejected), approver name + date, compensating controls (for conditional), next re-assessment date, burn rate flag (for financial trend monitoring). **3 conditional vendors** have documented compensating controls and elevated monitoring schedules. |
| **Evidence** | Screenshot #01, `schema_validation.py` weekly output |
| **NIST 800-53** | SA-9 |
| **Status** | **Pass** |

---

### 8 — Re-Assessment Calendar Active

| Field | Detail |
|-------|--------|
| **Expected State** | Re-assessment dates set by tier: Critical (quarterly), High (semi-annual), Medium (annual), Low (biennial). Automated reminders 30 days before due date. KQL scan identifies overdue re-assessments. |
| **Observed State** | Calendar **configured.** All 12 vendors have re-assessment dates assigned. `vendor-reassessment-scan.kql` runs weekly — identifies vendors within 30 days of due date and vendors past due. Current state: 0 overdue, 2 Critical vendors due for first quarterly re-assessment in April 2026. Reminder notifications configured via Power Automate — 30-day and 14-day advance notice to assessment owner. |
| **Evidence** | Screenshot #05, KQL output |
| **NIST 800-161** | SR-3 |
| **Status** | **Pass** |

---

### 9 — Vendor Assessment Data Flows to Log Analytics

| Field | Detail |
|-------|--------|
| **Expected State** | Vendor risk events (intake, assessment, approval, re-assessment) logged to Log Analytics workspace for centralized audit trail and cross-pillar correlation. Register changes are not just stored — they are observable. |
| **Observed State** | SharePoint list changes **export** to Log Analytics via Logic App connector. **42 vendor governance events** in 30 days: 12 intakes, 5 full assessments, 12 approvals, 10 re-assessment calendar entries, 3 schema validation runs. All events include timestamp, actor, vendor name, action, and result. Retention: 90 days. |
| **Finding** | Pipeline is functional but relies on Logic App connector. Direct API integration with a GRC platform would be more resilient for production scale. |
| **Status** | **Partial** — functional but not production-hardened for scale |

---

### 10 — Subcontractor Risk Visibility for Critical Vendors

| Field | Detail |
|-------|--------|
| **Expected State** | Critical vendors provide Tier 2 subcontractor information: who processes data on their behalf, where, and under what controls. Tier 2 visibility is a scored domain in the assessment. |
| **Observed State** | **Cloud IaaS (Critical):** Tier 2 subcontractors documented — 3 data center operators, 2 support outsourcers. Subcontractor data processing agreements on file. Score: 85/100 for subcontractor domain. **Identity Platform (Critical):** Tier 1 subcontractors documented. Tier 2 **not provided** — vendor stated "commercially sensitive." Compensating control: quarterly attestation refresh + right to audit clause in contract. Subcontractor domain score reduced to 40/100, pulling overall score from 82 to 77. |
| **Finding** | 1 of 2 Critical vendors unable to provide Tier 2 subcontractor visibility. This is common in the industry but it is still a gap. The compensating control (quarterly refresh + right to audit) is documented but the audit clause has not been exercised. |
| **Status** | **Partial** — compensating controls in place but Tier 2 gap exists for 1 Critical vendor |

---

## Remediation Tracker

| # | Control | Finding | Owner | Remediation | Target Date | Status |
|---|---------|---------|-------|-------------|-------------|--------|
| 9 | Log Analytics pipeline | Logic App connector functional but not production-hardened | R. Myers | Evaluate direct GRC platform integration for scale | 2026-Q2 | Open |
| 10 | Tier 2 subcontractor gap | Identity Platform vendor unable to provide Tier 2 data | R. Myers | Exercise right-to-audit clause OR require Tier 2 data at next quarterly re-assessment | 2026-04-15 | Open |

---

## Watchstander Notes

1. **The scoring engine eliminates bias.** `calculate_risk.py` takes the same JSON input and produces the same score every time. No "gut feel." No "they seemed fine on the call." The math is the math. If two assessors disagree, run the inputs through the engine. The engine doesn't have opinions.

2. **Financial stability is not a snapshot.** The auditor was right to flag this. A vendor with 12 months of cash and a 50% burn rate is on a clock. The burn rate flag in the scoring model catches what a point-in-time solvency check would miss. This is MBA-level fiscal analysis applied to vendor risk — and it's the kind of thing most cybersecurity consultants don't think to look at.

3. **Subcontractor visibility is the hardest data to get and the most important.** Vendors will push back. They'll say "commercially sensitive." They'll say "we handle it." That's not evidence. The right-to-audit clause in the contract is your leverage. If they refuse at re-assessment, the subcontractor domain score drops, the overall score drops, and the conditional acceptance may flip to elevated review. The math handles the consequence. You just have to ask the question.

4. **Schema validation is data integrity.** In a physical supply chain, you wouldn't accept a packing slip with missing fields. The digital supply chain register deserves the same discipline. `schema_validation.py` runs weekly because entropy is constant. Data decays. Fields get skipped. Dates get missed. The validator catches it before the auditor does.

---

*Assessment conducted by Robert Myers, MBA | SailPoint ISL, Security+, CCSK, CC*
*Stella Maris Governance — 2026*
