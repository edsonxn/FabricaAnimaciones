# -*- coding: utf-8 -*-
"""Regenera solo las frases cambiadas (voz --solo) y vuelve a seleccionar, con reintentos. Escribe voz_ok.txt al terminar."""
import json
import os
import subprocess
import sys

os.chdir(r"C:\FabricaAnimaciones")
env = dict(os.environ, PYTHONIOENCODING="utf-8")
V = "historia_espana"
D = f"videos/{V}"
SOLO = sys.argv[1:] or ["ochocientos_5"]


def fab(*a, log):
    with open(log, "w", encoding="utf-8") as f:
        return subprocess.run([sys.executable, "fab.py", V, *a], stdout=f, stderr=subprocess.STDOUT, env=env).returncode


if os.path.exists(f"{D}/voz_ok.txt"):
    os.remove(f"{D}/voz_ok.txt")
fab("voz", "--solo", *SOLO, log=f"{D}/voz_una_log.txt")
for ronda, seeds in enumerate((None, ["5", "6", "7", "8"], ["9", "10", "11", "12"])):
    if seeds:
        reg = json.load(open(f"{D}/voz/regenerar.json", encoding="utf-8"))
        if not reg:
            break
        fab("voz", "--seeds", *seeds, "--solo", *reg, log=f"{D}/voz_una_log{ronda}.txt")
    rc = fab("seleccionar", log=f"{D}/sel_una_log{ronda}.txt")
    if rc != 0:                                       # fallo de GPU (cuBLAS): un reintento
        rc = fab("seleccionar", log=f"{D}/sel_una_log{ronda}b.txt")
    reg = json.load(open(f"{D}/voz/regenerar.json", encoding="utf-8"))
    if not reg and rc == 0:
        break
open(f"{D}/voz_ok.txt", "w").write("ok")
