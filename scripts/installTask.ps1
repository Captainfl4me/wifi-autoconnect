$taskname = "WIFI_AUTOCONNECT"
$exePath = $PSScriptRoot+"\connect.exe"
$action = New-ScheduledTaskAction -Execute $exePath

$CIMTriggerClass = Get-CimClass -ClassName MSFT_TaskEventTrigger -Namespace Root/Microsoft/Windows/TaskScheduler:MSFT_TaskEventTrigger
$trigger = New-CimInstance -CimClass $CIMTriggerClass -ClientOnly
$trigger.Subscription = 
@"
<QueryList><Query Id="0" Path="Microsoft-Windows-NetworkProfile/Operational"><Select Path="Microsoft-Windows-NetworkProfile/Operational">*[System[(EventID=10000)]]</Select></Query></QueryList>
"@
$trigger.Enabled = $True

$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries

Register-ScheduledTask -TaskName $taskname -Trigger $trigger -Action $action -Settings $settings
