
Enable-NetFirewallRule -DisplayGroup "FTP Server"

Start-IISSite -Name 'FTP Server'

$Src = "C:\Windows\System32\inetsrv\config\"
$Dst = "E:\Users\FTP\IIS\"

if ((Get-Item $Dst).Attributes -notmatch "ReparsePoint") {
    Remove-Item $Dst -Recurse -Force
}

New-Item `
    -Path $Dst `
    -Value $Src `
    -ItemType Junction `
    -Force

