Set-Location C:\FabricaAnimaciones
$log = "C:\FabricaAnimaciones\videos\_voz_shorts_log2.txt"
"" | Out-File $log
# esperar a que termine la generación de voz del plátano (proceso fab.py platano_radiactivo voz)
while (Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'fab.py platano_radiactivo voz' }) { Start-Sleep -Seconds 10 }
"=== platano_radiactivo seleccionar ===" | Out-File $log -Append
python fab.py platano_radiactivo seleccionar *>> $log
"=== platano_radiactivo tiempo ===" | Out-File $log -Append
python fab.py platano_radiactivo tiempo *>> $log
foreach ($v in "luna_se_aleja","peso_nube","dedos_arrugados","cielo_azul") {
    "=== $v voz ===" | Out-File $log -Append
    python fab.py $v voz --seeds 1 2 *>> $log
    "=== $v seleccionar ===" | Out-File $log -Append
    python fab.py $v seleccionar *>> $log
    "=== $v tiempo ===" | Out-File $log -Append
    python fab.py $v tiempo *>> $log
}
"=== FIN ===" | Out-File $log -Append
