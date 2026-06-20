Import-Module WebAdministration

Set-ItemProperty "IIS:\Sites\Website" serverAutoStart False

Stop-IISSite -Name 'Website' -Confirm:$false
