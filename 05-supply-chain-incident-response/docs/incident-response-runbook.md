# Supply Chain Incident Response — Operations Runbook

> **Version:** 1.0.0 | **Author:** Robert Myers, MBA | Stella Maris Governance

---

## 1. Purpose and Scope

Operational procedures for responding to third-party security incidents. When a vendor is compromised, this runbook governs your response — containment, investigation, communication, and recovery.

**Scope:** All incidents originating from or involving third-party vendors, suppliers, or subprocessors.

**Out of Scope:** Internal-only incidents (covered by organizational IR plan), identity-layer threats detected by ITDR Pack 09 (unless vendor account is involved).

---

## 2. Prerequisites

| Requirement | Detail |
|-------------|--------|
| Vendor access inventory | All vendor accounts, service principals, API keys, VPN, network paths documented |
| Containment playbook deployed | `playbook-credential-compromise` Logic App active |
| Communication distribution lists | CISO, legal, executive, vendor security contacts current |
| Blast radius tool | `blast-radius-assessment.py` tested and operational |
| Pack 04 scorecard active | Breach database and signal monitoring feeding detection |
| Tabletop completed | At least 2 scenarios tested within last 6 months |

---

## 3. Detection: How You Learn About It

| Source | What It Looks Like | First Action |
|--------|-------------------|--------------|
| **Vendor self-disclosure** | Phone call, email, or portal notification from vendor | Classify severity immediately |
| **Pack 04 breach database hit** | Automated alert: vendor domain in new breach dataset | Verify breach is current and relevant |
| **Pack 09 ITDR** | Vendor account anomaly: impossible travel, privilege escalation, unusual activity | Correlate with vendor status — is this compromise or authorized? |
| **Public disclosure / news** | Media report or security researcher disclosure | Verify against your vendor register — are you affected? |
| **Threat intelligence** | Industry-specific threat feed identifies vendor compromise | Assess proximity and classify |

> **Watchstander Note:** Do not wait for the vendor to tell you. If you see it in the news, in the breach database, or in your own logs — act. The vendor's disclosure timeline is their problem. Your containment timeline is yours.

---

## 4. Classification: First 15 Minutes

Upon learning of a potential third-party incident:

1. **Identify the vendor** — confirm they are in your vendor register
2. **Determine data proximity** — does this vendor have access to your data? What classification?
3. **Classify severity:**

| Question | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|----------|--------|--------|--------|--------|
| Is the breach confirmed? | Yes | Yes | Yes | Yes |
| Does the vendor access your data? | Yes | Yes | No (indirect) | No |
| Is your data in the blast radius? | Confirmed | Probable | Unlikely | No |
| Evidence of exfiltration? | Yes | Not yet | No | No |

4. **Log in incident register** with timestamp and initial classification
5. **Notify appropriate parties** per severity:
   - Tier 1: CISO within 2 hours, executive within 24 hours
   - Tier 2: CISO within 8 hours
   - Tier 3: Risk owner within 24 hours
   - Tier 4: Log and monitor

---

## 5. Containment: Playbook Execution

### 5.1 Credential Compromise (Playbook A)

**Automated (via Logic App):**
1. Identify all accounts tagged to the vendor
2. Disable all accounts
3. Revoke all sessions
4. Notify SOC + Risk Owner

**Manual follow-up:**
1. Rotate all API keys and shared secrets associated with vendor
2. Rotate any certificates used for vendor integration
3. Review vendor account activity for last 30 days
4. Check for persistence mechanisms

### 5.2 Data Breach (Playbook B)

1. Restrict data flows: disable SFTP, throttle API, block file shares
2. Send demand for information to vendor (use template)
3. Inventory all data shared with or accessible by vendor
4. Engage legal for regulatory notification assessment
5. Prepare CISO and executive briefs

### 5.3 Supply Chain Software Attack (Playbook C)

1. Query Pack 03 SBOM for affected component
2. Identify all systems running affected version
3. Isolate affected systems
4. Block vendor update mechanism
5. Roll back to last known-good version
6. Scan for IOCs from threat intelligence

### 5.4 Vendor Service Outage (Playbook D)

1. Confirm scope and estimated recovery
2. Activate business continuity for affected services
3. Determine if outage is security-related
4. If security-related: escalate to Playbook A or B

---

## 6. Investigation

After containment:

### 6.1 Timeline Construction

Build the timeline from your logs, not the vendor's narrative:
```
T0  — First malicious activity (from your logs or vendor disclosure)
T1  — Breach confirmed / notification received
T2  — Incident classified
T3  — Containment actions completed
T4  — Blast radius assessment completed
T5  — CISO briefed
T6  — Vendor demand for information sent
T7  — Vendor response received
T8  — Investigation complete
T9  — Recovery initiated
T10 — Incident closed
```

Every timestamp goes in the incident register.

### 6.2 Blast Radius Assessment

Run `blast-radius-assessment.py --vendor [vendor_name]`:

1. **Identity:** What accounts exist? What permissions? Activity during incident window?
2. **Data:** What data classification? Where stored? Was it accessed?
3. **Software:** Is vendor software in our SBOM? Is the compromised component present?
4. **Network:** VPN tunnels? Firewall rules? Network segments accessible?
5. **Financial:** Contract value? Liability terms? Insurance coverage?

### 6.3 Vendor Engagement

Send demand for information (template: `comms-vendor-demand.md`):
- What happened? (timeline)
- What systems were affected? (scope)
- Was our data accessed or exfiltrated? (exposure)
- What remediation has been taken? (containment)
- What is the root cause? (analysis)
- When will a full forensic report be available? (accountability)

Set response deadline: 24 hours for Tier 1, 48 hours for Tier 2.

> **Watchstander Note:** The vendor's incident response quality tells you more about them than their SOC 2 report. A vendor who responds within 4 hours with scope, timeline, and remediation steps is a vendor who has a real IR plan. A vendor who takes 7 days and sends a vague statement is a vendor who has a PR plan.

---

## 7. Recovery

### 7.1 Access Restoration

Vendor access is restored only when:
- Vendor provides root cause analysis
- Vendor confirms remediation is complete
- Blast radius assessment confirms no residual exposure
- Risk Owner approves restoration
- Credentials are freshly issued (never re-enable old credentials)

### 7.2 Controlled Restoration Process

1. Issue new credentials (new service principal, new API key, new guest accounts)
2. Apply principle of least privilege — re-assess whether vendor needs same access level
3. Enable enhanced monitoring for 30 days post-restoration
4. Set 30-day review checkpoint

---

## 8. Post-Incident Review

Within 14 days of incident closure:

1. **Timeline review:** Was the timeline accurate? Where were the gaps?
2. **Containment assessment:** Did containment execute within SLA? What was slow?
3. **Communication review:** Were the right people notified at the right time?
4. **Vendor accountability scoring:** Score the vendor on 5 factors
5. **Governance improvements:** What changes to policy, procedure, or technology?
6. **Scorecard update:** Update Pack 04 scorecard with incident data
7. **Re-assessment trigger:** Schedule Pack 01 out-of-cycle re-assessment
8. **Contract recommendations:** Amend contract terms based on findings

### Post-Incident Review Document
```markdown
## Post-Incident Review: [Incident ID]

### Incident Summary
### Timeline (with all timestamps)
### Containment Effectiveness
### Blast Radius Findings
### Communication Log
### Vendor Accountability Score
### Lessons Learned
### Governance Improvements
### Contract Recommendations
### Follow-Up Items
```

---

## 9. Review Cadence

| Review | Frequency | Owner |
|--------|-----------|-------|
| Vendor access inventory refresh | Quarterly | IAM Lead |
| Communication distribution lists | Quarterly | Risk Owner |
| Playbook test (tabletop) | Semi-annual | Risk Owner + SOC |
| Vendor security contact verification | Semi-annual | Risk Owner |
| Full IR plan review | Annual | Risk Owner + CISO + Legal |
| Post-incident review | Within 14 days of every incident | Risk Owner |

---

## 10. Troubleshooting

**Vendor is unresponsive during incident:** Escalate through vendor executive contact. If still unresponsive after 24 hours, activate right-to-audit clause. Document non-cooperation — this scores in accountability and may trigger vendor replacement discussion.

**Blast radius tool missing data source:** If a pillar query fails, gather data manually and note the gap. Don't delay the assessment waiting for automation. The manual data feeds the same decision.

**Regulatory notification deadline approaching:** When in doubt, notify. Under-notification has legal consequences. Over-notification has minor reputational cost. Legal makes the final call, but bias toward notification.

**Vendor claims "your data not affected" without evidence:** Do not accept vendor's claim at face value. Request specific evidence: log excerpts, forensic scope, network segmentation proof. Until you verify independently, maintain containment.

---

*Stella Maris Governance — 2026*
