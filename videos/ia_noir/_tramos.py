# -*- coding: utf-8 -*-
"""Tramos (s) afectados por las transiciones entre escenas y las de tinta internas -> _rehacer.txt"""
import json, math, sys
sys.path[:0] = [".", "../../nucleo"]
import escenas as S
tl = json.load(open("timeline.json", encoding="utf-8"))
ids = [e["id"] for e in tl["escenas"]]
v = []
for k, e in enumerate(tl["escenas"]):
    esc = S.CLASES[e["id"]](e, k)
    d = esc.TR_SALIDA[1]
    if k < len(ids) - 1:
        v.append((e["t1"] - d - 0.1, e["t1"] + 0.1))
    for p in esc.planos:
        if p.tr == "tinta":
            v.append((p.t0 - 0.1, p.t0 + p.dur + 0.1))
v.append((tl["escenas"][1]["t0"], tl["escenas"][1]["t0"] + 2.6))
v.sort()
m = []
for a, b in v:
    a, b = math.floor(a), math.ceil(b)
    if m and a <= m[-1][1]:
        m[-1][1] = max(m[-1][1], b)
    else:
        m.append([a, b])
txt = " ".join(f"{a}-{b}" for a, b in m)
print(txt, sum(b - a for a, b in m), "s")
open("_rehacer.txt", "w").write(txt)
