# Render completo del Mixton: video -> final -> verificar -> aviso por voz (21-oct-2026). Log: previews/_render_todo.log
# (sin acentos: PowerShell 5.1 lee los .ps1 sin BOM como ANSI)
Set-Location C:\FabricaAnimaciones
$log = "videos\caxcan_mixton\previews\_render_todo.log"
"== inicio $(Get-Date -Format 'HH:mm:ss')" | Out-File -Encoding utf8 $log
python fab.py caxcan_mixton video *>> $log
if ($LASTEXITCODE -ne 0) { "== video FALLO $LASTEXITCODE" | Out-File -Append -Encoding utf8 $log; python fab.py avisar "El render del Mixton fallo. Revisa el log."; exit 1 }
python fab.py caxcan_mixton final *>> $log
if ($LASTEXITCODE -ne 0) { "== final FALLO $LASTEXITCODE" | Out-File -Append -Encoding utf8 $log; python fab.py avisar "El final del Mixton fallo."; exit 1 }
python fab.py caxcan_mixton verificar *>> $log
"== fin $(Get-Date -Format 'HH:mm:ss') verificar $LASTEXITCODE" | Out-File -Append -Encoding utf8 $log
python fab.py avisar "Ya termino el render completo del Mixton."
