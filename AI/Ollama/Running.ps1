
if (Get-Process -Name "ollama") {
    Write-Host "true"
} else {
    Write-Host "false"
}
