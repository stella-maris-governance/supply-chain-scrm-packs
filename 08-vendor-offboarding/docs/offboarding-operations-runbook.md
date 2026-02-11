# Vendor Offboarding & Access Revocation — Operations Runbook

> **Version:** 1.0.0 | **Author:** Robert Myers, MBA | Stella Maris Governance

---

## 1. Purpose and Scope

Operational procedures for terminating vendor relationships with complete access revocation, data disposition, and verification. The door you opened must close completely.

**Scope:** All vendor offboardings — planned (contract expiry, replacement, mutual termination) and unplanned (termination for cause, acquisition-triggered).

---

## 2. Prerequisites

| Requirement | Detail |
|-------------|--------|
| Vendor access inventory | Pack 05 blast radius inventory or Pack 01 intake + Identity Pack 06 guest register |
| Offboarding checklist | Vendor-specific 30-item checklist generated from access inventory |
| Revocation script | `revoke-vendor-access.py` deployed and tested |
| Data disposition template | `data-deletion-attestation-template.md` approved by legal |
| Post-offboarding audit query | `post-offboarding-audit.kql` configured |
| Tier 2 register | Pack 06 register identifying subprocessors holding your data |

---

## 3. Offboarding Triggers and Timelines

### 3.1 Planned Offboarding (Contract Expiry / Replacement / Mutual)

| Milestone | Timing | Action |
|-----------|--------|--------|
| Decision to offboard | T-60 days | Notify vendor. Initiate data return request. |
| Migration complete (if replacing) | T-30 days | Confirm new vendor operational. Begin Phase 1. |
| Phase 1: Access revocation | T-7 days | Disable accounts, revoke sessions, clear groups |
| Phase 2: Secret rotation | T-7 to T-3 days | Rotate all shared credentials |
| Phase 3: Software removal | T-7 to T-0 | Remove agents, webhooks, DNS records |
| Contract expiry | T-0 | All access revoked. Data return SLA begins. |
| Phase 4: Data disposition | T+0 to T+90 | Deletion request sent. Attestation due within 90 days. |
| Phase 5: Verification audit | T+30 | Sentinel scan. Access scan. Close record. |

### 3.2 Termination for Cause (Immediate)

| Milestone | Timing | Action |
|-----------|--------|--------|
| Decision to terminate | T+0 | Activate Pack 05 containment playbook immediately. |
| Containment | T+0 (< 2 min) | All accounts disabled, sessions revoked. |
| Full offboarding | T+0 (< 5 min) | Groups cleared, OAuth revoked, network disconnected. |
| Secret rotation | T+0 to T+30 min | All shared secrets rotated and verified. |
| Software removal | T+0 to T+1 hour | Agents, webhooks, DNS removed. |
| Legal engagement | T+1 hour | Formal termination letter. Data return demand. Right-to-audit activation. |
| Data disposition | T+0 to T+90 | Per legal guidance. Vendor may not cooperate. |
| Verification audit | T+30 days | Critical — must verify vendor doesn't attempt access. |

> **Watchstander Note:** In termination for cause, the access revocation IS the first action, not the termination letter. Disable first. Notify second. The containment playbook from Pack 05 gives you 52-second revocation. Use it. The legal conversation happens after the environment is secure.

---

## 4. Phase 1: Access Revocation

### Automated Revocation
```bash
python3 revoke-vendor-access.py --vendor "VendorName" --domain "vendor.com" --mode execute
```

Script performs:
1. Query all guest accounts matching vendor domain
2. Query all service principals tagged to vendor
3. Disable all accounts
4. Revoke all active sessions
5. Remove from all Entra ID groups
6. Revoke OAuth application consents
7. Log all actions with timestamps

### Manual Follow-Up

After automated revocation:
1. **SSO integration:** Remove vendor from SAML/OIDC federation configuration
2. **VPN tunnel:** Submit change request to network team for tunnel termination
3. **Firewall rules:** Submit change request to remove vendor IP range permissions
4. **SFTP/file transfer:** Disable vendor SFTP account and transfer channel
5. **Conditional access:** Remove vendor from any CA policy exclusions

### Verification

For each action, record:
- Action taken
- Timestamp
- Verification method (Entra audit log event ID, firewall rule audit, etc.)
- Verified by (name)

---

## 5. Phase 2: Secret Rotation

For each shared secret associated with the vendor:

| Secret Type | Rotation Method | Verification |
|-------------|----------------|-------------|
| API key | Regenerate in application settings | Old key returns 401 |
| Shared password | Reset in credential store | Old password rejected |
| Certificate (mTLS) | Generate new cert, update config | Old cert rejected on handshake |
| SAS token | Regenerate access key (invalidates all SAS) | Old token returns 403 |
| Storage access key | Rotate key in storage account | Old key returns 403 |
| SSH key | Remove vendor public key from authorized_keys | Old key rejected |
| Webhook secret | Regenerate in application | Old signature validation fails |

### Secret Inventory Source

Pull from:
- Pack 05 blast radius assessment (secret inventory per vendor)
- Application configuration files referencing vendor
- Key vault entries tagged to vendor
- Certificate store entries issued for vendor integration

> **Watchstander Note:** The secrets you know about are the easy part. The dangerous ones are the secrets you don't know about — the API key someone shared in a Teams chat, the certificate someone generated outside the standard process, the test credential that was never rotated from onboarding. The 30-day verification audit (Phase 5) is your safety net for what you missed.

---

## 6. Phase 3: Software Removal

| Item | Removal Method | Verification |
|------|---------------|-------------|
| Endpoint agents | Uninstall via MDM/SCCM or manual removal | Endpoint scan: agent absent |
| Server software | Uninstall from server | Server inventory scan |
| Browser extensions | Remove via endpoint policy | Extension audit |
| DNS CNAME/A records | Remove from DNS zone | DNS resolution check |
| Webhook/callback URLs | Remove from application config | Application config audit |
| Mail connectors | Remove from Exchange Online | Connector list audit |
| Power Platform connectors | Remove from Power Platform admin | Connector audit |

---

## 7. Phase 4: Data Disposition

### 7.1 Data Return

1. Send formal data return request (citing contract clause and Pack 07 SLA)
2. Specify format: original format or agreed export format
3. Set deadline per contract (typically 14-30 days)
4. Receive and validate returned data: completeness, integrity, correct format
5. Acknowledge receipt to vendor

### 7.2 Data Deletion

1. Send formal deletion request with `data-deletion-attestation-template.md`
2. Request covers: production systems, backup systems, replicas, test environments
3. Set deadline: 90 days from request (per contract or GDPR Art. 17)
4. Receive signed deletion attestation
5. Validate attestation: scope covers all known data locations, method specified, authorized signer

### 7.3 Tier 2 Deletion (Critical Vendors)

1. Query Pack 06 Tier 2 register for entities handling your data
2. Include Tier 2 deletion requirement in deletion request to Tier 1 vendor
3. Request Tier 1 vendor provide Tier 2 deletion confirmation
4. If Tier 1 vendor cannot confirm Tier 2 deletion: document as residual risk
5. Escalate via right-to-audit clause if available

### 7.4 Non-Cooperative Vendor

When vendor doesn't respond to deletion request:
1. Day 14: Send follow-up with contract clause reference
2. Day 30: Escalate through vendor executive contact
3. Day 45: Legal engagement — formal demand letter
4. Day 60: Activate right-to-audit clause if available
5. Day 90: Document non-compliance. Assess regulatory notification requirements. Archive as unresolved finding.

---

## 8. Phase 5: Verification Audit

30 days after access revocation:

### 8.1 Sentinel Log Review

Run `post-offboarding-audit.kql`:
- Sign-in attempts from vendor accounts (all should be blocked/failed)
- Sign-in attempts from vendor IP ranges
- API calls using vendor credentials
- Entra audit events referencing vendor entities

**Expected result:** Zero successful vendor-attributed events.

### 8.2 Environment Scan

| Check | Method | Expected Result |
|-------|--------|----------------|
| Vendor accounts | Entra ID query | All disabled or deleted |
| Vendor service principals | Entra ID query | All disabled or deleted |
| Vendor group memberships | Group audit | Zero memberships |
| Vendor OAuth consents | Enterprise app audit | Zero active consents |
| Vendor DNS records | DNS zone scan | Zero vendor-related records |
| Vendor firewall rules | Firewall audit | Zero vendor IP rules |
| Vendor software | Endpoint scan | Zero vendor agents/software |

### 8.3 Closure

When all Phase 5 checks pass:
1. Mark offboarding record as **CLOSED**
2. Archive all evidence (audit logs, attestations, checklists)
3. Update Pack 01 vendor register: status = "Offboarded"
4. Update Pack 04 scorecard: status = "Archived"
5. Remove vendor from active monitoring

---

## 9. Cross-Pack Updates on Offboarding

| Pack | Action |
|------|--------|
| Pack 01 | Vendor status → "Offboarded." Risk score archived. |
| Pack 02 | Attestation records archived. No further tracking. |
| Pack 03 | Vendor SBOM entries archived. Components may remain in other vendor SBOMs. |
| Pack 04 | Scorecard archived. Vendor removed from active monitoring. |
| Pack 05 | Vendor removed from active blast radius inventory. |
| Pack 06 | Tier 2 entities marked "inactive" for this vendor relationship. |
| Pack 07 | SLA tracking archived. Final compliance score recorded. |
| Identity Pack 06 | Guest accounts removed from lifecycle management. |
| Identity Pack 08 | CIEM permissions archived. |

---

## 10. Review Cadence

| Review | Frequency | Owner |
|--------|-----------|-------|
| Offboarding register review | Monthly | Risk Owner |
| Data disposition follow-up (pending attestations) | Monthly | Risk Owner |
| Post-offboarding verification audit | 30 days post-revocation | SOC + Risk Owner |
| Stale vendor account scan (accounts disabled but not deleted) | Quarterly | IAM Lead |
| Full offboarding process review | Annual | Risk Owner |

---

## 11. Troubleshooting

**Discovered vendor access path not in checklist:** Add to checklist immediately. Revoke. Document how it was missed. Update Pack 05 blast radius inventory and onboarding intake process to capture in future.

**Vendor account shows activity after offboarding:** Investigate immediately. Determine if activity is automated (cached token, scheduled task) or human-initiated. If human-initiated, escalate to CISO — potential unauthorized access. Ensure session revocation was effective and account is truly disabled.

**Vendor refuses data deletion:** Escalate to legal. Activate right-to-audit if available. Document non-compliance for regulatory purposes. Assess whether regulatory notification is required.

**Can't identify all secrets shared with vendor:** Expand search: key vault audit logs, application configuration repositories, deployment scripts, Teams/Slack messages mentioning vendor name + "key" or "secret" or "credential." Accept that some may be missed. The 30-day verification audit is the safety net.

**Vendor was acquired — new entity wants continued access:** This is not a continuation. This is a new vendor. Trigger Pack 01 assessment for the new entity. If they pass, onboard fresh with new credentials. If they fail, offboard per this pack.

---

*Stella Maris Governance — 2026*
