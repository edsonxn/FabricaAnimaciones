# -*- coding: utf-8 -*-
"""Regenera solo las frases corregidas (modernidad_1, siglo20_0) y selecciona tomas; reintenta hasta 2 rondas más."""
import json
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
FAB = [sys.executable, os.path.join(RAIZ, "fab.py"), "historia_egipto"]


def correr(*a):
    print(">>", " ".join(a), flush=True)
    r = subprocess.run(FAB + list(a), cwd=RAIZ)
    if r.returncode:
        sys.exit(f"falló {a}")


claves = ["modernidad_1", "siglo20_0"]
correr("voz", "--seeds", "1", "2", "3", "4", "--solo", *claves)
for seeds in (["5", "6", "7", "8"], ["9", "10", "11", "12"], None):
    correr("seleccionar")
    reg = json.load(open(os.path.join(AQUI, "voz", "regenerar.json"), encoding="utf-8"))
    print("regenerar:", reg, flush=True)
    if not reg or seeds is None:
        break
    correr("voz", "--seeds", *seeds, "--solo", *reg)
correr("tiempo")
print("VOZ_FIX_OK", flush=True)
