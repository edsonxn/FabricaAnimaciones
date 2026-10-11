# -*- coding: utf-8 -*-
"""Cadena 2 (4-oct-2026): rehace SOLO los tramos de España corregidos tras la revisión del MASTER -> final -> verificar
-> marca _espana_fix_listo.txt -> relanza Satoshi (3 procesos; sus segmentos ya viven en E:). Un render a la vez (memoria virtual)."""
import os
import subprocess
import sys
import time

RAIZ = r"C:\FabricaAnimaciones"
V = "historia_espana"
CARPETA = os.path.join(RAIZ, "videos", V)
LOG = os.path.join(CARPETA, "_cierre2_log.txt")
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")
TRAMOS = ["45-51", "57-63", "67-73.5", "77-83", "145-162", "163-171", "190-196", "216.5-222.5", "224-228", "270-277"]


def log(*a):
    with open(LOG, "a", encoding="utf-8") as f:
        print(time.strftime("%H:%M:%S"), *a, file=f, flush=True)


def fab(*args):
    with open(os.path.join(CARPETA, "_cierre2_fab.txt"), "a", encoding="utf-8") as f:
        f.write(f"\n=== {time.strftime('%H:%M:%S')} fab.py {' '.join(args)} ===\n")
        f.flush()
        return subprocess.run([sys.executable, "fab.py", *args], cwd=RAIZ, stdout=f, stderr=subprocess.STDOUT, env=ENV).returncode


for etapa in (("video", "--rehacer", *TRAMOS, "--procs", "12"), ("final",), ("verificar",)):
    t0 = time.time()
    rc = fab(V, *etapa)
    log(f"{etapa[0]} -> código {rc} ({time.time() - t0:.0f} s)")
    if rc != 0 and etapa[0] != "verificar":
        log("falló; me detengo")
        sys.exit(1)
open(os.path.join(CARPETA, "_espana_fix_listo.txt"), "w").write(time.strftime("%H:%M:%S"))
log("ESPAÑA (tramos corregidos) LISTA; relanzo Satoshi con 3 procesos")

rc = subprocess.run([sys.executable, os.path.join(RAIZ, "videos", "satoshi_nakamoto", "_render_despierto.py"), "3"], cwd=RAIZ, env=ENV).returncode
txt = open(os.path.join(RAIZ, "videos", "satoshi_nakamoto", "render_log.txt"), encoding="utf-8", errors="replace").read()
ok = txt.rstrip().endswith("código 0 ===")
log("SATOSHI render:", "TERMINÓ BIEN" if ok else "FALLÓ (ver render_log.txt)", f"(lanzador rc={rc})")
