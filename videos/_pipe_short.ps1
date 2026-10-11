param([string]$v, [int]$procs = 8)
Set-Location C:\FabricaAnimaciones
$log = "C:\FabricaAnimaciones\videos\$v\_pipe_log.txt"
"" | Out-File $log
function paso($n, $cmd) { "=== $n ===" | Out-File $log -Append; & $cmd *>> $log }
"=== sfx ===" | Out-File $log -Append
python fab.py $v sfx *>> $log
"=== lyria ===" | Out-File $log -Append
$env:PYTHONPATH = "C:\FabricaAnimaciones\videos\$v;C:\FabricaAnimaciones\nucleo"
$env:PYTHONIOENCODING = "utf-8"
Set-Location "C:\FabricaAnimaciones\videos\$v"
python ..\..\nucleo\lyria.py --n 2 *>> $log
python ..\..\nucleo\lyria.py --usar 2 *>> $log
Set-Location C:\FabricaAnimaciones
"=== mezcla ===" | Out-File $log -Append
python fab.py $v mezcla *>> $log
"=== video ===" | Out-File $log -Append
python fab.py $v video --procs $procs *>> $log
"=== final ===" | Out-File $log -Append
python fab.py $v final *>> $log
"=== verificar ===" | Out-File $log -Append
python fab.py $v verificar *>> $log
"=== FIN ===" | Out-File $log -Append
