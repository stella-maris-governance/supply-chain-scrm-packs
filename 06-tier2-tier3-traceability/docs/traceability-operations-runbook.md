# Tier 2/3 Supplier Traceability — Operations Runbook

> **Version:** 1.0.0 | **Author:** Robert Myers, MBA | Stella Maris Governance

---

## 1. Purpose and Scope

Operational procedures for identifying, mapping, and monitoring Tier 2 and Tier 3 supplier dependencies. You vetted the vendor. This runbook governs the visibility behind the vendor.

**Scope:** All subprocessors, subservice organizations, infrastructure providers, and key dependencies of Critical and High Tier 1 vendors.

**Out of Scope:** Tier 1 vendor assessment (Pack 01), software-layer transitive dependencies (Pack 03 — cross-referenced but governed separately).

---

## 2. Prerequisites

| Requirement | Detail |
|-------------|--------|
| Pack 01 operational | Vendor register with tier classification |
| Pack 02 operational | SOC 2 carve-out data available for extraction |
| Vendor contracts accessible | DPAs, service agreements, right-to-audit clauses |
| Subprocessor questionnaire | `subprocessor-questionnaire.json` ready for distribution |
| Tier 2 register | `tier2-register.json` initialized |

---

## 3. Data Collection: Building the Map

### 3.1 SOC 2 Carve-Out Extraction

For every SOC 2 report validated in Pack 02:

1. Open Section III (Description of the System)
2. Search for "subservice organization" or "carved out"
3. For each carved-out entity:
   - Record: entity name, service description, relationship to your data
   - Add to Tier 2 register
   - Flag: this entity's controls are NOT covered by the vendor's SOC 2

> **Watchstander Note:** A "carved-out" subservice organization in a SOC 2 is the vendor telling you, in writing, that a piece of their control environment is someone else's responsibility — and the auditor didn't test it. It is the most explicit Tier 2 signal you'll get. Don't miss it.

### 3.2 DPA and GDPR Article 28 Review

For every vendor DPA and data processing agreement:

1. Locate the subprocessor annex or attachment
2. For each listed subprocessor:
   - Record: entity name, service, jurisdiction, data types processed
   - Add to Tier 2 register
3. Note whether the DPA grants you:
   - Notification of subprocessor changes
   - Right to object to new subprocessors
   - Audit rights extending to subprocessors

### 3.3 Subprocessor Questionnaire

Send `subprocessor-questionnaire.json` to all Critical and High vendors:

1. Request: all subprocessors who handle, store, process, or transit your data
2. For each subprocessor: name, service, jurisdiction, attestation status, right-to-audit
3. Ask: does the vendor audit their subprocessors? How? Frequency?
4. Set response deadline: 14 business days
5. Follow up at 7 days if no response
6. Document non-response as finding

### 3.4 Public Documentation Review

For each Critical/High vendor:

1. Review trust page, security page, status page
2. Identify named infrastructure providers, hosting partners, CDN
3. Cross-reference with SOC 2 and DPA data
4. Mark entries sourced from public docs as "low confidence" until vendor-confirmed

---

## 4. Building the Tier 2 Register

For each identified Tier 2 entity, record:

| Field | Description |
|-------|-------------|
| Tier 2 entity name | Legal or operating name |
| Tier 1 vendor | Which of your vendors uses them |
| Service provided | What they do (hosting, database, encryption, etc.) |
| Data flow | Does your data touch this entity? Type? |
| Incorporation jurisdiction | Where entity is legally based |
| Data processing jurisdiction | Where data is processed |
| Data storage jurisdiction | Where data is stored |
| Attestation status | SOC 2, ISO, FedRAMP — or none visible |
| Source | How you learned about this entity (SOC 2, DPA, questionnaire, public) |
| Confidence | High (vendor-confirmed), Medium (DPA/SOC 2), Low (public docs) |
| Last updated | Date of most recent data |

---

## 5. Concentration Risk Analysis

After building the register, run `concentration-risk-scan.py`:
```bash
python3 concentration-risk-scan.py --register tier2-register.json
```

The scan identifies:
- Any Tier 2 entity serving 3+ Tier 1 vendors (shared dependency)
- Any Tier 2 entity in a high-risk or restricted jurisdiction serving Critical vendors
- Any Tier 2 entity with no attestation visibility serving Critical vendors
- Tier 3 infrastructure patterns (e.g., multiple Tier 2 entities on same cloud provider)

### Responding to Concentration Risk

| Finding | Action |
|---------|--------|
| Shared Tier 2 serves 3+ vendors | Document in risk register. Ensure Pack 05 incident response accounts for simultaneous failure. |
| Restricted jurisdiction | Assess against ITAR, GDPR adequacy, data sovereignty. Escalate to legal if applicable. |
| No Tier 2 attestation for Critical vendor | Flag in Pack 01 Subcontractor Risk. Request vendor obtain or share Tier 2 attestation. |
| Tier 3 concentration (shared cloud) | Document for awareness. Include in Pack 05 contingency planning. Cannot govern directly. |

---

## 6. Supply Chain Map Generation

For Critical vendors, generate visual dependency maps:
```bash
python3 build-supply-chain-map.py --vendor "IdentityFirst Inc" --register tier2-register.json
```

Maps show:
- Tier 1 → Tier 2 → Tier 3 relationships
- Data flow direction
- Jurisdiction tags
- Attestation status (green = attested, yellow = vendor-represented, red = none)
- Confidence level (solid line = confirmed, dotted = inferred)

Generate maps for all Critical vendors. Update semi-annually or when Tier 2 changes are disclosed.

---

## 7. Feeding Results to Pack 01

Tier 2 findings directly impact Pack 01 Subcontractor Risk domain (10% weight):

| Tier 2 Visibility Level | Score Impact |
|--------------------------|-------------|
| All Tier 2 identified, attestations verified, right-to-audit flows down | 80-100 |
| Tier 2 partially identified, some attestations, right-to-audit present | 50-79 |
| Tier 2 partially identified, minimal attestation, limited audit rights | 25-49 |
| Tier 2 unknown, no attestation visibility, no audit rights | 0-24 |

After updating Tier 2 register:
1. Re-calculate each vendor's Subcontractor Risk domain score
2. Re-run `calculate_risk.py` for affected vendors
3. Update Pack 01 register
4. If score crosses a threshold, trigger re-assessment workflow

---

## 8. Vendor Non-Response Handling

When a vendor doesn't respond to the subprocessor questionnaire:

| Day | Action |
|-----|--------|
| Day 7 | Send follow-up reminder |
| Day 14 | Escalate to vendor relationship owner |
| Day 21 | Document non-response as finding |
| Day 30 | Non-response scored in Pack 01 (Subcontractor Risk reduced) and Pack 04 (Relationship Health reduced) |
| Contract renewal | Include questionnaire response as contractual obligation |

> **Watchstander Note:** Non-response is data. A vendor who won't tell you about their supply chain is a vendor who either doesn't know their own supply chain or doesn't want you to know. Both are findings. The silence costs them in the math.

---

## 9. Review Cadence

| Review | Frequency | Owner |
|--------|-----------|-------|
| Tier 2 register review | Semi-annual | Risk Owner |
| Concentration risk scan | Semi-annual (with register review) | Risk Owner |
| Supply chain map update (Critical vendors) | Semi-annual | Risk Owner |
| GDPR Article 28 change monitoring | Continuous (for applicable vendors) | Risk Owner |
| Subprocessor questionnaire re-send | Annual (or at contract renewal) | Risk Owner |
| Right-to-audit clause review | At contract renewal | Legal + Risk Owner |

---

## 10. Troubleshooting

**Vendor refuses to disclose subprocessors:** Cite right-to-audit clause. If no clause exists, document gap and include in contract renewal. Use DPA, SOC 2, and public documentation to build partial visibility. Score the refusal.

**Tier 2 entity changes after register was built:** If vendor notifies you (GDPR Article 28 requirement), update register immediately. If you discover the change independently, update register and flag that vendor notification process may be inadequate.

**Cannot determine Tier 2 attestation status:** Request through Tier 1 vendor. If Tier 1 vendor cannot or will not provide, document as gap. You cannot audit Tier 2 directly without contractual right flowing through Tier 1.

**Concentration risk identified but not actionable:** Document it. Include in Pack 05 contingency planning. Some concentration risks (e.g., AWS dependency) are industry-systemic and not vendor-specific. Awareness is the governance tool when control is not available.

---

*Stella Maris Governance — 2026*
