# Screenshot Capture Guide — Vendor Offboarding

---

### 01 — Offboarding Register
**Path:** Register view
**Show:** Tabletop entries with phase completion status

### 02 — Access Revocation
**Path:** Entra audit log
**Show:** Vendor accounts disabled, sessions revoked with timestamps

### 03 — Post-Offboarding Audit
**Path:** KQL output from Sentinel
**Show:** 30-day scan showing zero vendor activity post-offboarding

### 04 — Data Disposition Tracker
**Path:** Tracker view
**Show:** Deletion request status, attestation tracking

### 05 — Secret Rotation Verification
**Path:** API test or credential test output
**Show:** Old credentials returning 401/403 after rotation
