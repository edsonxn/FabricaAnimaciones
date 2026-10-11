param([Parameter(ValueFromRemainingArguments=$true)]$a)
$env:PYTHONPATH='C:\FabricaAnimaciones\videos\luna_se_aleja;C:\FabricaAnimaciones\nucleo'
$env:PYTHONIOENCODING='utf-8'
Set-Location C:\FabricaAnimaciones\videos\luna_se_aleja
python @a
