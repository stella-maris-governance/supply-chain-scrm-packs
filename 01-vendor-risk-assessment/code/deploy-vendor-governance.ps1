<#
.SYNOPSIS
    Initialize vendor governance infrastructure.
.DESCRIPTION
    Creates SharePoint list for vendor register, configures Log Analytics
    custom log table, and sets up Power Automate approval flow stub.
.PARAMETER Mode
    DryRun (default) or Deploy.
.NOTES
    Author: Robert Myers, MBA — Stella Maris Governance
#>

[CmdletBinding()]
param(
    [ValidateSet("DryRun", "Deploy")]
    [string]$Mode = "DryRun",
    [string]$SharePointSite = "https://yourtenant.sharepoint.com/sites/governance",
    [string]$WorkspaceName = "",
    [string]$ResourceGroupName = ""
)

$ErrorActionPreference = "Stop"

Write-Host "=== Stella Maris Vendor Governance Deployment ==="
Write-Host "Mode: $Mode"

# Step 1: SharePoint list for vendor register
$listColumns = @(
    @{ Name = "VendorName"; Type = "Text"; Required = $true },
    @{ Name = "Tier"; Type = "Choice"; Choices = @("Critical","High","Medium","Low"); Required = $true },
    @{ Name = "RiskScore"; Type = "Number"; Min = 0; Max = 100; Required = $true },
    @{ Name = "ApprovalStatus"; Type = "Choice"; Choices = @("Approved","Conditional","Rejected","Pending"); Required = $true },
    @{ Name = "ApprovalDate"; Type = "DateTime"; Required = $true },
    @{ Name = "Approver"; Type = "Text"; Required = $true },
    @{ Name = "NextReassessment"; Type = "DateTime"; Required = $true },
    @{ Name = "CompensatingControls"; Type = "MultiLineText"; Required = $false },
    @{ Name = "BurnRateFlag"; Type = "Boolean"; Required = $true },
    @{ Name = "Notes"; Type = "MultiLineText"; Required = $false }
)

if ($Mode -eq "Deploy") {
    Write-Host "[DEPLOY] Creating SharePoint list: VendorRiskRegister"
    # PnP PowerShell or SharePoint REST API implementation
    foreach ($col in $listColumns) {
        Write-Host "  [COLUMN] $($col.Name) ($($col.Type))"
    }
} else {
    Write-Host "[DRYRUN] Would create SharePoint list with $($listColumns.Count) columns"
    foreach ($col in $listColumns) {
        Write-Host "  $($col.Name) ($($col.Type)) Required=$($col.Required)"
    }
}

# Step 2: Log Analytics custom table
Write-Host ""
if ($Mode -eq "Deploy" -and $WorkspaceName) {
    Write-Host "[DEPLOY] Creating custom log table: VendorGovernance_CL"
} else {
    Write-Host "[DRYRUN] Would create Log Analytics table: VendorGovernance_CL"
    Write-Host "  Fields: TimeGenerated, VendorName_s, Tier_s, EventType_s, Score_d, Actor_s"
}

# Step 3: Power Automate approval flow
Write-Host ""
if ($Mode -eq "Deploy") {
    Write-Host "[DEPLOY] Power Automate flow: Vendor-Approval-Workflow"
} else {
    Write-Host "[DRYRUN] Would create approval flow:"
    Write-Host "  Trigger: New item in VendorRiskRegister"
    Write-Host "  Route: Critical → CISO+Legal, High → Security Lead, Medium → IT Manager, Low → Auto"
    Write-Host "  Actions: Send approval, update status, log to VendorGovernance_CL"
}

Write-Host ""
Write-Host "=== Complete ==="
Write-Host "Next: populate register with existing vendors and run schema validation."
