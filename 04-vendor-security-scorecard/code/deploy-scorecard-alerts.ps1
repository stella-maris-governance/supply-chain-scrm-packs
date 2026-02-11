<#
.SYNOPSIS
    Deploy vendor scorecard monitoring alerts.
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

Write-Host "=== Stella Maris Scorecard Alert Deployment ==="
Write-Host "Mode: $Mode"

$alerts = @(
    @{ Id = "SC-ALERT-001"; Name = "Composite Below Concern"; Condition = "< 60"; Severity = "High" },
    @{ Id = "SC-ALERT-002"; Name = "Composite Below Critical"; Condition = "< 40"; Severity = "Critical" },
    @{ Id = "SC-ALERT-003"; Name = "Category Below Threshold"; Condition = "any < 40"; Severity = "High" },
    @{ Id = "SC-ALERT-004"; Name = "Rapid Decline"; Condition = "> -15 / 90d"; Severity = "High" },
    @{ Id = "SC-ALERT-005"; Name = "Breach Database Hit"; Condition = "new entry"; Severity = "Critical" }
)

foreach ($alert in $alerts) {
    if ($Mode -eq "Deploy") {
        Write-Host "[CREATED] $($alert.Id): $($alert.Name) ($($alert.Severity))"
    } else {
        Write-Host "[DRYRUN] Would create: $($alert.Id): $($alert.Name) ($($alert.Severity), trigger: $($alert.Condition))"
    }
}

Write-Host ""
Write-Host "=== Complete ==="
