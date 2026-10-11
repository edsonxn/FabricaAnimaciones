# -*- coding: utf-8 -*-
"""Voz -> seleccionar con rondas de reintento (plantilla de voynich/_ronda2.py). Escribe ronda_ok.txt al terminar."""
import json
import os
import subprocess
import sys

V = "satoshi_nakamoto"
os.chdir(r"C:\FabricaAnimaciones")
env = dict(os.environ, PYTHONIOENCODING="utf-8")


def fab(*a, log):
    with open(log, "w", encoding="utf-8") as f:
        return subprocess.run([sys.executable, "fab.py", V, *a], stdout=f, stderr=subprocess.STDOUT, env=env).returncode


ok = f"videos/{V}/ronda_ok.txt"
if os.path.exists(ok):
    os.remove(ok)
fab("voz", log=f"videos/{V}/r_voz.txt")
for ronda, seeds in enumerate((["5", "6", "7", "8"], ["9", "10", "11", "12"], ["13", "14", "15", "16"])):
    fab("seleccionar", log=f"videos/{V}/r_sel{ronda}.txt")
    reg = json.load(open(f"videos/{V}/voz/regenerar.json", encoding="utf-8"))
    if not reg:
        break
    fab("voz", "--seeds", *seeds, "--solo", *reg, log=f"videos/{V}/r_voz{ronda}.txt")
else:
    fab("seleccionar", log=f"videos/{V}/r_sel_final.txt")
open(ok, "w").write("ok")
