# Screenshot Capture Guide — Vendor Security Scorecard

---

### 01 — Vendor Scorecard Dashboard
**Path:** Scorecard register or dashboard view
**Show:** All vendors with composite score, status, trend, last updated

### 02 — Signal Detail
**Path:** `external-signal-check.py` output or monitoring tool
**Show:** SSL, DNS, breach, and exposed service checks for a Critical vendor

### 03 — Trend Analysis
**Path:** KQL output or dashboard
**Show:** 90-day rolling trend with score history for declining vendor

### 04 — Alert Firing
**Path:** Alert log or notification
**Show:** Category threshold breach alert with acknowledgment timestamp

### 05 — Cross-Pillar Feed
**Path:** Scorecard showing Pack 02/03 data integration
**Show:** Attestation expiry and CVE data reflected in Compliance Currency category
