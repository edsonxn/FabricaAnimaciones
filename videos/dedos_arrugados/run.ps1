param([Parameter(ValueFromRemainingArguments=$true)]$a)
$env:PYTHONPATH='C:\FabricaAnimaciones\videos\dedos_arrugados;C:\FabricaAnimaciones\nucleo'
$env:PYTHONIOENCODING='utf-8'
Set-Location C:\FabricaAnimaciones\videos\dedos_arrugados
python @a
