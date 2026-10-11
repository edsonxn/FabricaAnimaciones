# -*- coding: utf-8 -*-
"""Cadena (4-oct-2026): espera la cola de escenas -> «conservar» las escenas 2-5 (no cambian) -> render completo de España -> final -> verificar
-> marca _espana_listo.txt -> reanuda el render de Satoshi (videos/satoshi_nakamoto/_render_despierto.py). Un solo render a la vez (memoria virtual).
Log: _cierre_render_log.txt"""
import json
import os
import subprocess
import sys
import time
import urllib.request

RAIZ = r"C:\FabricaAnimaciones"
V = "historia_espana"
CARPETA = os.path.join(RAIZ, "videos", V)
LOG = os.path.join(CARPETA, "_cierre_render_log.txt")
COLA = os.path.join(CARPETA, "_cola_escenas_log.txt")
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")


def log(*a):
    with open(LOG, "a", encoding="utf-8") as f:
        print(time.strftime("%H:%M:%S"), *a, file=f, flush=True)


def fab(*args, salida=None):
    with open(salida or os.path.join(CARPETA, "_cierre_render_fab.txt"), "a", encoding="utf-8") as f:
        f.write(f"\n=== {time.strftime('%H:%M:%S')} fab.py {' '.join(args)} ===\n")
        f.flush()
        return subprocess.run([sys.executable, "fab.py", *args], cwd=RAIZ, stdout=f, stderr=subprocess.STDOUT, env=ENV).returncode


# 1) cola de escenas
log("esperando la cola de escenas…")
while True:
    txt = open(COLA, encoding="utf-8").read() if os.path.exists(COLA) else ""
    if "COLA TERMINADA" in txt:
        break
    if "ERROR" in txt or " error" in txt:
        log("la cola de escenas falló; me detengo:", txt[-300:])
        sys.exit(1)
    time.sleep(10)
log("cola terminada")

# 2) conservar las escenas cuyo código cambió pero no su imagen (todas con w = 0: ningún fundido de rejilla)
try:
    d = json.loads(urllib.request.urlopen(f"http://127.0.0.1:8765/api/preview?video={V}", timeout=30).read().decode("utf-8"))
    req = urllib.request.Request(f"http://127.0.0.1:{d['puerto']}/escenas/conservar?ids=origenes,roma,visigodos,alandalus&token={d['token']}", method="POST")
    log("conservar:", urllib.request.urlopen(req, timeout=30).read().decode("utf-8"))
except Exception as e:                                  # noqa: BLE001
    log("no pude conservar (el render rehará esas escenas):", e)

# 3) render completo + final + verificar
for etapa in (("video", "--procs", "12"), ("final",), ("verificar",)):
    t0 = time.time()
    rc = fab(V, *etapa)
    log(f"{etapa[0]} -> código {rc} ({time.time() - t0:.0f} s)")
    if rc != 0 and etapa[0] != "verificar":             # verificar solo informa: no frena el render de Satoshi
        log("falló; me detengo (revisar _cierre_render_fab.txt)")
        sys.exit(1)
open(os.path.join(CARPETA, "_espana_listo.txt"), "w").write(time.strftime("%H:%M:%S"))
log("ESPAÑA LISTA (MASTER hecho); sigo con Satoshi")

# 4) Satoshi: reanuda los segmentos hechos (el 1.er intento murió por MemoryError con 7-8 procesos; con 5 va)
rc = subprocess.run([sys.executable, os.path.join(RAIZ, "videos", "satoshi_nakamoto", "_render_despierto.py"), "5"], cwd=RAIZ, env=ENV).returncode
log("SATOSHI render terminó con código", rc)
