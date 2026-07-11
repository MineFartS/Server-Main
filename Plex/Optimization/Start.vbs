
' Create a new Shell Object
Set Shell = WScript.CreateObject("WScript.Shell")

' CD to the script directory
Shell.CurrentDirectory = "E:\Plex\"

' Run the command
Shell.run "python -m Optimization", 0, 0