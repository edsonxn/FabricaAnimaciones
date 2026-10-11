param([Parameter(ValueFromRemainingArguments=$true)]$a)
$env:PYTHONPATH='C:\FabricaAnimaciones\videos\primer_foton;C:\FabricaAnimaciones\nucleo'
$env:PYTHONIOENCODING='utf-8'
Set-Location C:\FabricaAnimaciones\videos\primer_foton
python @a
