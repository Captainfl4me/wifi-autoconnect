Set objShell = WScript.CreateObject("WScript.Shell")
scriptDir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
runCmd = "cmd /c " & """" & scriptDir & "\connect.exe"""
objShell.Run runCmd, 0, True
