Set-Location C:\FabricaAnimaciones
$log = "C:\FabricaAnimaciones\videos\_voz_shorts_log.txt"
"" | Out-File $log
foreach ($v in "platano_radiactivo","luna_se_aleja","peso_nube","dedos_arrugados","cielo_azul") {
    "=== $v voz ===" | Out-File $log -Append
    python fab.py $v voz *>> $log
    "=== $v seleccionar ===" | Out-File $log -Append
    python fab.py $v seleccionar *>> $log
    "=== $v tiempo ===" | Out-File $log -Append
    python fab.py $v tiempo *>> $log
}
"=== FIN ===" | Out-File $log -Append
