# Render en cola de secreto_ia (21-oct-2026): espera a que termine el render de frio_extremo y la voz de nervio_vago
# (render y voz NO a la vez), y luego video → final → verificar → aviso por voz. Log en previews/_render_en_cola.log
$Esperar = @($env:FAB_ESPERAR -split ',' | Where-Object { $_ } | ForEach-Object { [int]$_ })
Set-Location C:\FabricaAnimaciones
$log = "videos\secreto_ia\previews\_render_en_cola.log"
"$(Get-Date -Format s) esperando a: $($Esperar -join ',')" | Out-File -Encoding utf8 $log
if ($Esperar.Count) { Wait-Process -Id $Esperar -ErrorAction SilentlyContinue }
"$(Get-Date -Format s) render" | Out-File -Encoding utf8 -Append $log
python fab.py secreto_ia video *>> $log
"$(Get-Date -Format s) final" | Out-File -Encoding utf8 -Append $log
python fab.py secreto_ia final *>> $log
python fab.py secreto_ia verificar *>> $log
"$(Get-Date -Format s) LISTO" | Out-File -Encoding utf8 -Append $log
python fab.py avisar "Terminó el render de La IA que guarda secretos." *>> $log
