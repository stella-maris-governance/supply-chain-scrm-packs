# Screenshot Capture Guide — SBOM Governance

---

### 01 — SBOM Register
**Path:** Register view or dashboard
**Show:** All SBOMs (internal + vendor) with format, component count, NTIA status, CVE summary

### 02 — NTIA Validation
**Path:** `validate-ntia-elements.py` output
**Show:** Pass for valid SBOM, Fail for non-compliant vendor submission with specific findings

### 03 — Vulnerability Correlation
**Path:** `correlate-vulnerabilities.py` output or dashboard
**Show:** Components with active CVEs by severity, response status

### 04 — Dependency Tree
**Path:** Dependency analysis output
**Show:** Transitive dependency chain for App-2 showing jackson-databind at depth 6

### 05 — License Classification
**Path:** `license-classifier.py` output
**Show:** Component breakdown by license type with flags
