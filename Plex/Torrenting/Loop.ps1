
$loc = Get-Location
Set-Location $PSScriptRoot\..

foreach ($x in 0..$args[0]) {
    python.exe `
        -m Torrenting `
        --limit $args[1]
}

Set-Location $loc