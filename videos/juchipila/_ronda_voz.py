# -*- coding: utf-8 -*-
"""Espera a que no haya ningún render en marcha (la voz y el render a la vez agotan la memoria virtual: docs/voz.md)
y entonces corre voz -> seleccionar con rondas de reintento. Escribe ronda_ok.txt al terminar.
Cancelar: matar este proceso (no toca nada más) o borrar `_ronda_voz_espera.txt`."""
import json
import os
import re
import subprocess
import sys
import time

os.chdir(r"C:\FabricaAnimaciones")
V = "juchipila"
CARPETA = f"videos/{V}"
env = dict(os.environ, PYTHONIOENCODING="utf-8")
ESPERA = f"{CARPETA}/_ronda_voz_espera.txt"
PATRON_RENDER = re.compile(r"-m render|_render|render_|fab\.py \S+ (video|final)", re.I)


def renders_en_marcha():
    ps = ("Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='ffmpeg.exe'\" | "
          "ForEach-Object { $_.CommandLine }")
    out = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, errors="replace").stdout
    return [l.strip()[:120] for l in out.splitlines() if PATRON_RENDER.search(l) and "_ronda_voz" not in l and "ffmpeg" not in l.lower()]


def gpu_usada_mb():
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"], capture_output=True, text=True).stdout
        return int(out.split()[0])
    except Exception:
        return 0


def fab(*a, log):
    with open(log, "w", encoding="utf-8") as f:
        return subprocess.run([sys.executable, "fab.py", V, *a], stdout=f, stderr=subprocess.STDOUT, env=env).returncode


open(ESPERA, "w").write("esperando a que termine el render (borra este archivo para cancelar)\n")
if os.path.exists(f"{CARPETA}/ronda_ok.txt"):
    os.remove(f"{CARPETA}/ronda_ok.txt")
calmas = 0
while True:
    if not os.path.exists(ESPERA):
        sys.exit("cancelado")
    r = renders_en_marcha()
    g = gpu_usada_mb()
    if not r and g < 4500:
        calmas += 1          # 3 comprobaciones seguidas (1,5 min) sin render antes de empezar
        if calmas >= 3:
            break
    else:
        calmas = 0
    open(ESPERA, "w").write(f"{time.strftime('%d-%b %H:%M')} esperando: {len(r)} render(s) {r[:2]}, GPU {g} MB (borra este archivo para cancelar)\n")
    time.sleep(30)

os.remove(ESPERA)
fab("voz", log=f"{CARPETA}/r_voz.txt")
for ronda, seeds in enumerate((["5", "6", "7", "8"], ["9", "10", "11", "12"], ["13", "14", "15", "16"])):
    fab("seleccionar", log=f"{CARPETA}/r_sel{ronda}.txt")
    reg = json.load(open(f"{CARPETA}/voz/regenerar.json", encoding="utf-8"))
    if not reg:
        break
    fab("voz", "--seeds", *seeds, "--solo", *reg, log=f"{CARPETA}/r_voz{ronda}.txt")
else:
    fab("seleccionar", log=f"{CARPETA}/r_sel_final.txt")
open(f"{CARPETA}/ronda_ok.txt", "w").write("ok")
