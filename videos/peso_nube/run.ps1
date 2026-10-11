param([Parameter(ValueFromRemainingArguments=$true)]$a)
$env:PYTHONPATH='C:\FabricaAnimaciones\videos\peso_nube;C:\FabricaAnimaciones\nucleo'
$env:PYTHONIOENCODING='utf-8'
Set-Location C:\FabricaAnimaciones\videos\peso_nube
python @a
