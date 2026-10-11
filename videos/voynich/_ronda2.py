# -*- coding: utf-8 -*-
"""Voz -> seleccionar con rondas de reintento (como `fab.py todo`, pero solo la parte de voz). Escribe ronda_ok.txt al terminar."""
import json
import os
import subprocess
import sys

os.chdir(r"C:\FabricaAnimaciones")
env = dict(os.environ, PYTHONIOENCODING="utf-8")


def fab(*a, log):
    with open(log, "w", encoding="utf-8") as f:
        return subprocess.run([sys.executable, "fab.py", "voynich", *a], stdout=f, stderr=subprocess.STDOUT, env=env).returncode


if os.path.exists("videos/voynich/ronda_ok.txt"):
    os.remove("videos/voynich/ronda_ok.txt")
fab("voz", log="videos/voynich/r2_voz.txt")
for ronda, seeds in enumerate((["5", "6", "7", "8"], ["9", "10", "11", "12"], ["13", "14", "15", "16"])):
    fab("seleccionar", log=f"videos/voynich/r2_sel{ronda}.txt")
    reg = json.load(open("videos/voynich/voz/regenerar.json", encoding="utf-8"))
    if not reg:
        break
    fab("voz", "--seeds", *seeds, "--solo", *reg, log=f"videos/voynich/r2_voz{ronda}.txt")
else:
    fab("seleccionar", log="videos/voynich/r2_sel_final.txt")
open("videos/voynich/ronda_ok.txt", "w").write("ok")
