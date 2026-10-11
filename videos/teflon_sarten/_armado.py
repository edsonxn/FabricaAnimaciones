# -*- coding: utf-8 -*-
"""Armado completo: video -> sfx -> mezcla -> final -> verificar. Log en _armado.log (sin barras de progreso)."""
import os
import subprocess
import sys

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
V = "teflon_sarten"
LOG = open(os.path.join(os.path.dirname(__file__), "_armado.log"), "w", encoding="utf-8")
for paso in ("video", "sfx", "mezcla", "final", "verificar"):
    r = subprocess.run([sys.executable, "fab.py", V, paso], cwd=RAIZ, capture_output=True, text=True, encoding="utf-8", errors="replace")
    lineas = [l for l in (r.stdout + r.stderr).splitlines() if l.strip() and "it/s" not in l and "frame=" not in l]
    LOG.write(f"\n=== {paso} (código {r.returncode})\n" + "\n".join(lineas[-25:]) + "\n")
    LOG.flush()
    if r.returncode:
        LOG.write("\nARMADO DETENIDO\n")
        LOG.close()
        sys.exit(r.returncode)
LOG.write("\nARMADO COMPLETO\n")
LOG.close()
