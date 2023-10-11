$taskname = "WIFI_AUTOCONNECT"
$exePath = $PSScriptRoot+"\runConnect.ps1"
$arg = '-File "'+ $exePath + '"'
$action = New-ScheduledTaskAction -Execute "Powershell.exe" -Argument $arg -WorkingDirectory $PSScriptRoot

$CIMTriggerClass = Get-CimClass -ClassName MSFT_TaskEventTrigger -Namespace Root/Microsoft/Windows/TaskScheduler:MSFT_TaskEventTrigger
$trigger = New-CimInstance -CimClass $CIMTriggerClass -ClientOnly
$trigger.Subscription = 
@"
<QueryList><Query Id="0" Path="Microsoft-Windows-NetworkProfile/Operational"><Select Path="Microsoft-Windows-NetworkProfile/Operational">*[System[(EventID=10000)]]</Select></Query></QueryList>
"@
$trigger.Enabled = $True

$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries

Register-ScheduledTask -TaskName $taskname -Trigger $trigger -Action $action -Settings $settings
