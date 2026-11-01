# -*- coding: utf-8 -*-
"""Genera voz + seleccionar (con hasta 2 rondas de reintento por semillas) + tiempo."""
import json
import os
import subprocess
import sys

RAIZ = r"C:\FabricaAnimaciones"
V = "historia_mexico"
CARP = os.path.join(RAIZ, "videos", V)


def run(*args):
    r = subprocess.run([sys.executable, os.path.join(RAIZ, "fab.py"), V, *args], cwd=RAIZ)
    if r.returncode != 0:
        sys.exit(r.returncode)


run("voz")
for ronda, seeds in enumerate((["5", "6", "7", "8"], ["9", "10", "11", "12"])):
    run("seleccionar")
    reg = json.load(open(os.path.join(CARP, "voz", "regenerar.json"), encoding="utf-8"))
    if not reg:
        break
    print(f"Reintentando ronda {ronda + 1}: {reg}", flush=True)
    run("voz", "--seeds", *seeds, "--solo", *reg)
else:
    run("seleccionar")
    reg = json.load(open(os.path.join(CARP, "voz", "regenerar.json"), encoding="utf-8"))
    if reg:
        print(f"ATENCIÓN: quedan por regenerar: {reg}", flush=True)
        sys.exit(2)

run("tiempo")
print("VOZ + TIEMPO COMPLETADO CON ÉXITO", flush=True)
