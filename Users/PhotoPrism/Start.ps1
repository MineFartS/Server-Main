
Clear-Host

Set-Location $PSScriptRoot

# 1. Find the container ID or name dynamically
#$containerName = (docker ps --filter "name=photoprism" --format "{{.Names}}") | Select-Object -First 1

#if (-not $containerName) {
#    Write-Error "No running PhotoPrism container found. Please run 'docker compose up -d' first."
#    exit
#}

#Write-Host "Found container: $containerName"

# 2. Get the Gateway IP from that container
#$WslIp = (docker inspect $containerName --format='{{range .NetworkSettings.Networks}}{{.Gateway}}{{end}}')


#if (-not $WslIp) {
#    Write-Error "Could not find the container network gateway. Is the container named 'photoprism' running?"
#    exit
#}

#Write-Host "Detected WSL Gateway IP via Docker: $WslIp"
#Write-Host "Setting up port proxy for PhotoPrism (Port 2342)..."

# 2. Clear old proxy rules
#netsh interface portproxy delete v4tov4 listenport=2342 listenaddress=0.0.0.0 *>$null

#netsh interface portproxy `
#    add v4tov4 `
#    listenport=2342 `
#    listenaddress=0.0.0.0 `
#    connectport=2342 `
#    connectaddress=$WslIp

docker.exe compose up -d
