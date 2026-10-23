# -*- coding: utf-8 -*-
"""Numera líneas «uuid expires firma» desde N y las pasa a flow_integrado bajar.
Acepta el texto tal cual lo devuelve __ver() (entre comillas y con \\n literales).
Uso: python videos/_lote.py <v> <N> < lineas"""
import subprocess
import sys

v, n = sys.argv[1], int(sys.argv[2])
crudo = sys.stdin.read().replace(chr(92) + "n", chr(10)).replace('"', "")
lineas = [l.strip() for l in crudo.splitlines() if l.strip()]
txt = "\n".join(str(n + k) + " " + l for k, l in enumerate(lineas))
r = subprocess.run([sys.executable, "nucleo/flow_integrado.py", "bajar", v], input=txt, text=True, capture_output=True)
print(r.stdout.strip(), r.stderr.strip()[-300:])
