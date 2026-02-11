# Screenshot Capture Guide — Tier 2/3 Supplier Traceability

---

### 01 — Tier 2 Register
**Path:** Register view
**Show:** All 8 Tier 2 entities with vendor, service, jurisdiction, attestation, confidence

### 02 — Supply Chain Map
**Path:** `build-supply-chain-map.py` output or Mermaid render
**Show:** Dependency visualization for Critical vendor with Tier 2 and Tier 3 nodes

### 03 — Concentration Risk
**Path:** `concentration-risk-scan.py` output
**Show:** Shared dependencies or Tier 3 concentration findings

### 04 — Jurisdiction Tracker
**Path:** `jurisdiction-tracker.json` or dashboard
**Show:** Tier 2 entities with jurisdiction flags (GDPR, ITAR)

### 05 — Traceability Gap
**Path:** KQL output or register view
**Show:** Critical vendor with incomplete Tier 2 data highlighted
