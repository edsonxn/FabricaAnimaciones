# -*- coding: utf-8 -*-
"""Tiempos de muestra (62 % de cada toma) entre t0 y t1 + comprobación AST de nombres de módulo repetidos (docs §8).
Uso (con PYTHONPATH del video y nucleo): python _muestras.py t0 t1"""
import ast
import collections
import sys

import escenas as S

a, b = float(sys.argv[1]), float(sys.argv[2])
ts = [d["t0"] for d in S.TOMAS] + [S.TOTAL]
m = [round(x + 0.62 * (y - x), 2) for x, y in zip(ts, ts[1:]) if a <= x < b]
c = collections.Counter()
for n in ast.parse(open("escenas.py", encoding="utf-8").read()).body:
    if isinstance(n, ast.FunctionDef):
        c[n.name] += 1
    if isinstance(n, ast.Assign):
        for tg in n.targets:
            if isinstance(tg, ast.Name):
                c[tg.id] += 1
print("repetidos:", [k for k, v in c.items() if v > 1], "· tomas:", len(S.TOMAS))
print(" ".join(map(str, m)))
