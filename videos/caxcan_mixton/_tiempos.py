# -*- coding: utf-8 -*-
"""Tiempos de cada frase (inicio-fin) por escena, para planear tomas. Uso: python _tiempos.py esc1 esc2 ..."""
import json
import os
import sys

d = os.path.dirname(os.path.abspath(__file__))
TL = json.load(open(os.path.join(d, "timeline.json"), encoding="utf-8"))
for e in TL["escenas"]:
    if len(sys.argv) > 1 and e["id"] not in sys.argv[1:]:
        continue
    print(f"== {e['id']}  {e['t0']:.2f}-{e['t1']:.2f}")
    for i, f in enumerate(e["frases"]):
        w = f["words"]
        txt = f["texto"]
        print(f"  {i} {f['t0']:.2f}-{f['t1']:.2f}  {txt[:150]}")

