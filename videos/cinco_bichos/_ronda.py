# -*- coding: utf-8 -*-
"""Voz completa con reintentos y, si pasa el control, tiempo + beats. Log en _ronda.log (sin barras de progreso)."""
import json
import os
import subprocess
import sys

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
V = "cinco_bichos"
LOG = open(os.path.join(os.path.dirname(__file__), "_ronda.log"), "w", encoding="utf-8")


def fab(*a):
    r = subprocess.run([sys.executable, "fab.py", V, *a], cwd=RAIZ, capture_output=True, text=True, encoding="utf-8", errors="replace")
    lineas = [l for l in (r.stdout + r.stderr).splitlines() if "Sampling" not in l and l.strip()]
    LOG.write(f"\n=== {' '.join(a)} (código {r.returncode})\n" + "\n".join(lineas[-60:]) + "\n")
    LOG.flush()
    return r.returncode


fab("voz")
for seeds in (["5", "6", "7", "8"], ["9", "10", "11", "12"], None):
    fab("seleccionar")
    reg = json.load(open(os.path.join(os.path.dirname(__file__), "voz", "regenerar.json"), encoding="utf-8"))
    if not reg:
        break
    if seeds is None:
        LOG.write(f"\nNO PASAN tras 12 tomas: {reg}\n")
        LOG.close()
        sys.exit(2)
    fab("voz", "--seeds", *seeds, "--solo", *reg)
fab("tiempo")
fab("beats")
LOG.write("\nRONDA COMPLETA\n")
LOG.close()

