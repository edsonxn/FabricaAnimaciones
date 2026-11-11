# -*- coding: utf-8 -*-
"""Pausa pedida por el usuario (11-nov-2026): espera a que no quede render de Warcraft (fab.py wow_* video/final, o ffmpeg
escribiendo en videos/wow_*) durante 2 comprobaciones seguidas (cada 120 s) y relanza `bash _render_tramos.sh`."""
import json
import os
import re
import subprocess
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
PS = ("Get-CimInstance Win32_Process | Select-Object ProcessId,Name,CommandLine | ConvertTo-Json -Compress")
PAT = re.compile(r"fab\.py\s+wow_\S+\s+(video|final)|videos[/\\]wow_\S+[/\\]salida")


def hay():
    out = subprocess.run(["powershell", "-NoProfile", "-Command", PS], capture_output=True, text=True, encoding="utf-8",
                         errors="replace").stdout
    try:
        ps = json.loads(out or "[]")
    except ValueError:
        return True
    yo = os.getpid()
    return any(p.get("CommandLine") and PAT.search(p["CommandLine"]) and p.get("ProcessId") != yo
               and "_espera_wow" not in p["CommandLine"] for p in ps)


ceros = 0
while ceros < 2:
    ceros = 0 if hay() else ceros + 1
    print(time.strftime("%H:%M"), "render wow:", "no" if ceros else "sí", flush=True)
    if ceros < 2:
        time.sleep(120)
print("Warcraft terminó:", time.strftime("%Y-%m-%d %H:%M"), flush=True)
subprocess.run([r"C:\Program Files\Git\bin\bash.exe", "_render_tramos.sh"], cwd=AQUI)   # «bash» a secas abre el de WSL
print("render por tramos terminado", flush=True)
