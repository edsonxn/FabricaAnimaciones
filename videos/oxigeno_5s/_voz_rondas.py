# -*- coding: utf-8 -*-
"""Voz -> seleccionar con rondas de reintento -> tiempo (copia de videos/voynich/_ronda2.py). Escribe ronda_ok.txt al terminar."""
import json
import os
import subprocess
import sys

os.chdir(r"C:\FabricaAnimaciones")
env = dict(os.environ, PYTHONIOENCODING="utf-8")
V = "oxigeno_5s"
D = f"videos/{V}"


def fab(*a, log):
    with open(log, "w", encoding="utf-8") as f:
        return subprocess.run([sys.executable, "fab.py", V, *a], stdout=f, stderr=subprocess.STDOUT, env=env).returncode


if os.path.exists(f"{D}/ronda_ok.txt"):
    os.remove(f"{D}/ronda_ok.txt")
fab("voz", log=f"{D}/r_voz.txt")
for ronda, seeds in enumerate((["5", "6", "7", "8"], ["9", "10", "11", "12"], ["13", "14", "15", "16"])):
    fab("seleccionar", log=f"{D}/r_sel{ronda}.txt")
    reg = json.load(open(f"{D}/voz/regenerar.json", encoding="utf-8"))
    if not reg:
        break
    fab("voz", "--seeds", *seeds, "--solo", *reg, log=f"{D}/r_voz{ronda}.txt")
else:
    fab("seleccionar", log=f"{D}/r_sel_final.txt")
fab("tiempo", log=f"{D}/r_tiempo.txt")
reg = json.load(open(f"{D}/voz/regenerar.json", encoding="utf-8"))
open(f"{D}/ronda_ok.txt", "w", encoding="utf-8").write("ok\npendientes: " + " ".join(reg))
