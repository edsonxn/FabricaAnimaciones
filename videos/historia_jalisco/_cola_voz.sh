#!/bin/bash
# Espera a que termine la voz de otra sesión (Chatterbox en la GPU) y lanza la de historia_jalisco.
cd /c/FabricaAnimaciones
while powershell -NoProfile -Command "if (Get-CimInstance Win32_Process -Filter \"name='python.exe'\" | Where-Object { \$_.CommandLine -match 'tts_gen|fab.py \w+ voz' }) { exit 0 } else { exit 1 }"; do sleep 30; done
date
python fab.py historia_jalisco voz
date
