# Screenshot Capture Guide — Supply Chain Incident Response

---

### 01 — Incident Register
**Path:** Incident register view
**Show:** Both tabletop incidents with severity, containment time, vendor accountability score

### 02 — Containment Playbook Execution
**Path:** Logic App run history
**Show:** Vendor accounts disabled, sessions revoked, SOC notified with timestamps

### 03 — Blast Radius Assessment
**Path:** `blast-radius-assessment.py` output
**Show:** 5-pillar assessment for a vendor with exposure summary

### 04 — Vendor Activity Timeline
**Path:** KQL output from Sentinel
**Show:** Reconstructed vendor account activity during incident window

### 05 — Post-Incident Review
**Path:** Review document
**Show:** Lessons learned, scorecard update, contract recommendations
