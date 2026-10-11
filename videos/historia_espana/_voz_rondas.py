# -*- coding: utf-8 -*-
"""Voz -> seleccionar con rondas de reintento (como `fab.py todo`, pero solo la parte de voz). Escribe voz_ok.txt al terminar."""
import json
import os
import subprocess
import sys

os.chdir(r"C:\FabricaAnimaciones")
env = dict(os.environ, PYTHONIOENCODING="utf-8")
V = "historia_espana"
D = f"videos/{V}"


def fab(*a, log):
    with open(log, "w", encoding="utf-8") as f:
        return subprocess.run([sys.executable, "fab.py", V, *a], stdout=f, stderr=subprocess.STDOUT, env=env).returncode


if os.path.exists(f"{D}/voz_ok.txt"):
    os.remove(f"{D}/voz_ok.txt")
fab("voz", log=f"{D}/voz_log.txt")
for ronda, seeds in enumerate((["5", "6", "7", "8"], ["9", "10", "11", "12"], ["13", "14", "15", "16"])):
    fab("seleccionar", log=f"{D}/sel_log{ronda}.txt")
    reg = json.load(open(f"{D}/voz/regenerar.json", encoding="utf-8"))
    if not reg:
        break
    fab("voz", "--seeds", *seeds, "--solo", *reg, log=f"{D}/voz_log{ronda + 1}.txt")
else:
    fab("seleccionar", log=f"{D}/sel_log_final.txt")
open(f"{D}/voz_ok.txt", "w").write("ok")
