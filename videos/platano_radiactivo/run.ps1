param([Parameter(ValueFromRemainingArguments=$true)]$a)
$env:PYTHONPATH='C:\FabricaAnimaciones\videos\platano_radiactivo;C:\FabricaAnimaciones\nucleo'
$env:PYTHONIOENCODING='utf-8'
Set-Location C:\FabricaAnimaciones\videos\platano_radiactivo
python @a
