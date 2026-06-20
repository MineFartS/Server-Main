Import-Module WebAdministration

$Website = Get-Website -Name 'Website'

($Website.State -eq 'Started') | ConvertTo-JSON
