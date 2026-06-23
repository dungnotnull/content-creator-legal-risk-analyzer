#Requires -RunAsAdministrator
# Register a weekly Monday 03:00 Task Scheduler job for the knowledge updater.
param(
    [string]$RepoPath = (Resolve-Path (Join-Path $PSScriptRoot ..)),
    [string]$TaskName = "ContentCreatorLegalRiskAnalyzer-KnowledgeUpdate",
    [string]$Python = "python"
)

$action = New-ScheduledTaskAction -Execute $Python -Argument "tools/knowledge_updater.py" -WorkingDirectory $RepoPath
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At "03:00"
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable
Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings -Force
Write-Host "Scheduled task '$TaskName' created. Check Task Scheduler for status."
