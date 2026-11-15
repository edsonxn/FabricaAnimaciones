# -*- coding: utf-8 -*-
"""Busca candidatos en Wikimedia Commons (UA genérico, sin datos personales) y baja miniaturas para elegir por identidad."""
import json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))
import imagenes_web as iw
GEN = {"User-Agent": "FabricaAnimaciones/1.0 python-urllib"}
iw.UA = GEN
iw._get.__defaults__ = (GEN, 40)
iw.guardar_commons.__globals__["UA"] = GEN
cons = sys.argv[1:]
out = os.path.join(AQUI, "imagenes", "_cand")
res = {}
import time
for q in cons:
    time.sleep(8)
    try:
        r = iw.commons(q, 6)
    except Exception as e:
        print("ERR", q, e); continue
    for i, info in enumerate(r):
        print(f"[{q}] {i} {info['w']}x{info['h']} {info['licencia']} | {info['titulo'][:90]} | {info['autor'][:40]}")
        res[f"{q}#{i}"] = info
old = os.path.join(out, "_cand.json")
d = json.load(open(old, encoding="utf-8")) if os.path.exists(old) else {}
d.update(res); json.dump(d, open(old, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
