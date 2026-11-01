# -*- coding: utf-8 -*-
"""Voz completa con reintentos y, si pasa el control, tiempo + beats. Log en _ronda.log (sin barras de progreso).
Espera antes a que la GPU quede libre (otra sesión puede estar con voz/seleccionar/render): < 4 GB usados y sin
procesos `tts_select`/`seleccionar`/`voz` de otro video, comprobado dos veces seguidas."""
import json
import os
import subprocess
import sys
import time

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
V = "doce_animales"
LOG = open(os.path.join(os.path.dirname(__file__), "_ronda.log"), "w", encoding="utf-8")


def _gpu_mb():
    try:
        r = subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
                           capture_output=True, text=True)
        return int(r.stdout.split()[0])
    except Exception:
        return 0


def _ocupada():
    r = subprocess.run(["powershell", "-NoProfile", "-Command",
                        "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | ForEach-Object { $_.CommandLine }"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    otros = [l for l in r.stdout.splitlines() if V not in l and
             any(k in l for k in (" seleccionar", " voz", "tts_select", " video", " todo"))]
    return _gpu_mb() > 4000 or bool(otros), otros


libres = 0
while libres < 2:
    oc, otros = _ocupada()
    libres = 0 if oc else libres + 1
    if oc:
        LOG.write(f"{time.strftime('%H:%M')} GPU ocupada ({_gpu_mb()} MB) {otros[:2]}\n")
        LOG.flush()
    time.sleep(60)
LOG.write(f"{time.strftime('%H:%M')} GPU libre: empiezo\n")
LOG.flush()


def fab(*a):
    r = subprocess.run([sys.executable, "fab.py", V, *a], cwd=RAIZ, capture_output=True, text=True, encoding="utf-8", errors="replace")
    lineas = [l for l in (r.stdout + r.stderr).splitlines() if "Sampling" not in l and l.strip()]
    LOG.write(f"\n=== {' '.join(a)} (código {r.returncode})\n" + "\n".join(lineas[-60:]) + "\n")
    LOG.flush()
    return r.returncode


fab("voz")
for seeds in (["5", "6", "7", "8"], ["9", "10", "11", "12"], None):
    fab("seleccionar")
    reg = json.load(open(os.path.join(os.path.dirname(__file__), "voz", "regenerar.json"), encoding="utf-8"))
    if not reg:
        break
    if seeds is None:
        LOG.write(f"\nNO PASAN tras 12 tomas: {reg}\n")
        LOG.close()
        sys.exit(2)
    fab("voz", "--seeds", *seeds, "--solo", *reg)
fab("tiempo")
fab("beats")
LOG.write("\nRONDA COMPLETA\n")
LOG.close()
