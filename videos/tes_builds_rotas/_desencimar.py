# -*- coding: utf-8 -*-
"""Lee previews/bordes.txt (de `_bordes.py`) y escribe _ajustes.json: para cada par ENCIMA, acorta el gráfico chico que entró antes
o retrasa/quita el que entró después (s3, 4-nov-2026). efectos.py aplica _ajustes.json al final (por índice en FX)."""
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
sys.path[:0] = [AQUI, os.path.join(AQUI, "..", "..", "nucleo")]
os.environ["FAB_SIN_AJUSTES"] = "1"
import secuencia_fx as SF  # noqa: E402
import efectos as E  # noqa: E402

capa = SF.cargar()
idx = {id(d["fn"]): i for i, d in enumerate(E.FX) if "fn" in d}
aj = json.load(open("_ajustes.json", encoding="utf-8")) if os.path.exists("_ajustes.json") else {}


def hallar(nombre, t):
    c = [d for d in capa.fx if d.get("nombre") == nombre and d["de"] - .5 <= t <= d["a"] + .5]
    return min(c, key=lambda d: abs(d["de"] - t)) if c else None


def chico(d):
    i = idx.get(id(d.get("fn")))
    return i is not None and "en" in E.FX[i] and "dur" in E.FX[i], i


for ln in open("previews/bordes.txt", encoding="utf-8"):
    m = re.match(r"ENCIMA (\d+):([\d.]+) \(([\d.]+) s\)\s+(.+?)\s+×\s+(.+?)\s+\(\d+%\)", ln.strip())
    if not m:
        continue
    t = int(m.group(1)) * 60 + float(m.group(2))
    a, b = hallar(m.group(4), t), hallar(m.group(5), t)
    if not a or not b:
        print("no hallo", ln.strip())
        continue
    if a["de"] > b["de"]:
        a, b = b, a
    ca, ia = chico(a)
    cb, ib = chico(b)
    if ca and str(ia) not in aj and b["de"] - a["de"] - .15 >= 1.5:
        aj[str(ia)] = {"dur": round(b["de"] - a["de"] - .15, 2)}
    elif cb and str(ib) not in aj and b["a"] - (a["a"] + .15) >= 1.5:
        aj[str(ib)] = {"retraso": round(a["a"] + .15 - b["de"], 2), "dur": round(b["a"] - a["a"] - .15, 2)}
    elif cb and str(ib) not in aj:
        aj[str(ib)] = {"quitar": True}
    elif ca and str(ia) not in aj:
        aj[str(ia)] = {"quitar": True}
    else:
        print("sin arreglo automático:", ln.strip())
json.dump(aj, open("_ajustes.json", "w", encoding="utf-8"), indent=1)
print(len(aj), "ajustes")
