
' Create a new Shell Object
Set Shell = WScript.CreateObject("WScript.Shell")

' CD to the script directory
Shell.CurrentDirectory = "E:\AI\Ollama\"

' Run (and wait for) CreateLink.ps1
Shell.run "Powershell -File Configure.ps1", 0, 1

Shell.CurrentDirectory = "E:\AI\Ollama\.app\"

' Start Ollama Service
Shell.run "OllamaPortable serve", 0, 0
