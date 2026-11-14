param([string]$ruta)
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$img = [System.Drawing.Image]::FromFile($ruta)
[System.Windows.Forms.Clipboard]::SetImage($img)
$img.Dispose()
"ok $ruta"
