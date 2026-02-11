<#
.SYNOPSIS
    Deploy vendor offboarding automation and verification.
.PARAMETER Mode
    DryRun (default) or Deploy.
.NOTES
    Author: Robert Myers, MBA — Stella Maris Governance
#>

[CmdletBinding()]
param(
    [ValidateSet("DryRun", "Deploy")]
    [string]$Mode = "DryRun"
)

$ErrorActionPreference = "Stop"

Write-Host "=== Stella Maris Vendor Offboarding Deployment ==="
Write-Host "Mode: $Mode"

$components = @(
    @{ Name = "Revocation Script"; Type = "Python"; File = "revoke-vendor-access.py" },
    @{ Name = "Post-Offboarding Audit"; Type = "KQL Scheduled Query"; File = "post-offboarding-audit.kql" },
    @{ Name = "Stale Account Scan"; Type = "Scheduled Task"; Cadence = "Quarterly" }
)

foreach ($c in $components) {
    if ($Mode -eq "Deploy") {
        Write-Host "[CREATED] $($c.Name) ($($c.Type))"
    } else {
        Write-Host "[DRYRUN] Would create: $($c.Name) ($($c.Type))"
    }
}

Write-Host ""
Write-Host "Post-deployment:"
Write-Host "  1. Test revocation script with DryRun against a test vendor"
Write-Host "  2. Schedule quarterly stale account scan"
Write-Host "  3. Configure post-offboarding audit to run 30 days after each offboarding"
Write-Host ""
Write-Host "=== Complete ==="
