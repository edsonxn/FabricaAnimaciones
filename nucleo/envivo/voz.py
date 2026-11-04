# -*- coding: utf-8 -*-
"""Voz del EN VIVO: voz de Windows (gratis, sin GPU ni créditos de ElevenLabs).

Usa las voces OneCore (las «nuevas» de Windows, mejores que las de System.Speech) a través de SAPI:
por defecto Raúl (es-MX). Un solo PowerShell por bloque genera un .wav por frase; la duración real de
cada .wav marca cuándo cambia la imagen, así lo que dice la voz se ve en ese momento.
"""
import json
import os
import re
import subprocess
import wave

PS = r"""
$ErrorActionPreference = 'Stop'
$trabajo = Get-Content -Raw -Encoding UTF8 $args[0] | ConvertFrom-Json
$cat = New-Object -ComObject SAPI.SpObjectTokenCategory
$cat.SetId('HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices', $false)
$tok = $null
foreach ($t in $cat.EnumerateTokens()) { if ($t.GetDescription() -like ('*' + $trabajo.voz + '*')) { $tok = $t } }
$v = New-Object -ComObject SAPI.SpVoice
if ($tok) { $v.Voice = $tok }
$v.Rate = [int]$trabajo.velocidad
foreach ($f in $trabajo.frases) {
  $fs = New-Object -ComObject SAPI.SpFileStream
  $fs.Format.Type = 22
  $fs.Open($f.wav, 3, $false)
  $v.AudioOutputStream = $fs
  [void]$v.Speak($f.texto)
  $fs.Close()
}
'ok'
"""


def limpiar(t):
    t = re.sub(r"\[[^\]]*\]", "", t)            # corchetes de actuación de ElevenLabs, por si el director los pone
    t = t.replace("«", "").replace("»", "").replace("*", "")
    return re.sub(r"\s+", " ", t).strip()


def duracion(ruta):
    with wave.open(ruta) as w:
        return w.getnframes() / float(w.getframerate())


def sintetizar(textos, carpeta, base, voz="Raul", velocidad=1):
    """textos -> [(ruta_wav, segundos)]. velocidad: -10..10 (SAPI)."""
    os.makedirs(carpeta, exist_ok=True)
    frases = [{"texto": limpiar(t), "wav": os.path.join(carpeta, f"{base}_{i:02d}.wav")} for i, t in enumerate(textos)]
    trabajo = os.path.join(carpeta, f"{base}_voz.json")
    script = os.path.join(carpeta, "_voz.ps1")
    if not os.path.exists(script):
        with open(script, "w", encoding="utf-8-sig") as f:
            f.write(PS)
    with open(trabajo, "w", encoding="utf-8") as f:
        json.dump({"voz": voz, "velocidad": velocidad, "frases": frases}, f, ensure_ascii=False)
    subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", script, trabajo],
                   capture_output=True, timeout=120, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    salida = []
    for f in frases:
        try:
            salida.append((f["wav"], duracion(f["wav"])))
        except Exception:
            salida.append((None, max(1.5, len(f["texto"]) / 15.0)))
    return salida
