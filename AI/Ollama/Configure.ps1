
git.exe submodule update --init --recursive --remote

$rule = Get-NetFirewallRule `
    -DisplayName 'Ollama' `
    -ErrorAction SilentlyContinue

if ($null -eq $rule) {

    New-NetFirewallRule `
        -DisplayName 'Ollama' `
        -Direction Inbound `
        -LocalPort 11434 `
        -Protocol TCP `
        -Action Allow `
        -Verbose

}
