param([string[]]$vs, [string]$espera = "")
Set-Location C:\FabricaAnimaciones
if ($espera) { while (Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match [regex]::Escape($espera) }) { Start-Sleep -Seconds 20 } }
foreach ($v in $vs) {
    python fab.py $v limpiar *> $null
    powershell -NoProfile -ExecutionPolicy Bypass -File C:\FabricaAnimaciones\videos\_pipe_short.ps1 -v $v -procs 8
}
