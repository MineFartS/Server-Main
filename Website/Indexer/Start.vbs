
' Create a new Shell Object
Set Shell = WScript.CreateObject("WScript.Shell")

' CD to the script directory
Shell.CurrentDirectory = "E:\Website\"

' Run the command
Shell.run "python -m Indexer", 0, 0