# -*- coding: utf-8 -*-
"""Ventana (s) de cada FX de efectos.py, para ver qué se encima en un tramo.  python _ventanas.py 300 420"""
import sys
exec(open("_anclas.py", encoding="utf-8").read().split("prev = 0.0")[0])
def t(x):
    off = 0.0
    if isinstance(x, (tuple, list)):
        x, off = x[0], x[1]
    if not isinstance(x, str) or x.startswith("scene-"):
        return None
    occ, fij = veces(x)
    if not occ:
        return None
    return (occ[fij - 1] if fij else occ[0]) + off, len(occ)
a0, a1 = float(sys.argv[1]), float(sys.argv[2])
for n, d in enumerate(efectos.FX):
    if "en" in d:
        r = t(d["en"]); 
        if not r: continue
        s, e = r[0], r[0] + d.get("dur", 3)
    elif "de" in d:
        r = t(d["de"]); r2 = t(d.get("a"))
        if not r: continue
        s = r[0]; e = r2[0] if r2 else s + 5
    else:
        continue
    if e >= a0 and s <= a1:
        print(f"FX{n:3d} {s:7.1f}-{e:7.1f} {'*' if r[1]>1 else ' '} {d.get('tipo',''):9s} {d.get('nombre','')[:50]}  x={d.get('x','')} y={d.get('y','')}")
