
Get-Process -Name "ollama" | ForEach-Object {
    $_
    Stop-Process $_ -Force
}

