Set-Location C:\FabricaAnimaciones
$log = "C:\FabricaAnimaciones\videos\polybius\voz_log.txt"
"espera a independencia_mx (pid 29008)..." | Out-File $log -Encoding utf8
Wait-Process -Id 29008 -ErrorAction SilentlyContinue
Start-Sleep 8
"inicio voz $(Get-Date)" | Out-File $log -Append -Encoding utf8
python fab.py polybius voz *>> $log
"inicio seleccionar $(Get-Date)" | Out-File $log -Append -Encoding utf8
python fab.py polybius seleccionar *>> $log
"FIN $(Get-Date)" | Out-File $log -Append -Encoding utf8
