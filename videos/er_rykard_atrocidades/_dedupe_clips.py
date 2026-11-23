# -*- coding: utf-8 -*-
"""Clips REPETIDOS entre beats de er_rykard_atrocidades: dos beats que enseñan el mismo tramo del mismo video
(solape real = desde + duración del beat). Por defecto solo INFORMA; los arreglos se hacen a mano con
`python fab.py er_rykard_atrocidades bajar scene-NNN --rehacer --url <url> --desde <s>` (y `_mano` en busquedas.json).
    python _dedupe_clips.py [--min 1.0]      (solapes de menos de --min segundos se ignoran)
Revisión previa al render, 22-nov-2026: 020↔021, 077↔078, 135↔183, 160↔165 arreglados; quedan 032/033↔034 y 164↔165
(0,6 s, invisibles).
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
MIN = float(sys.argv[sys.argv.index("--min") + 1]) if "--min" in sys.argv else 1.0
bus = json.load(open(os.path.join(AQUI, "busquedas.json"), encoding="utf-8"))
beats = {b["id"]: b for b in json.load(open(os.path.join(AQUI, "beats.json"), encoding="utf-8"))}


def vid(u):
    return u.rstrip("/")[-11:]


it = sorted(bus.items())
n = 0
for i, (a, x) in enumerate(it):
    for c, y in it[i + 1:]:
        if vid(x["url"]) != vid(y["url"]):
            continue
        a0 = float(x["desde"])
        a1 = a0 + beats[a]["t1"] - beats[a]["t0"]
        c0 = float(y["desde"])
        c1 = c0 + beats[c]["t1"] - beats[c]["t0"]
        ov = min(a1, c1) - max(a0, c0)
        if ov >= MIN:
            n += 1
            print(f"{a} <-> {c}  {vid(x['url'])}  {a0:.0f}-{a1:.0f} / {c0:.0f}-{c1:.0f}  solape {ov:.1f} s")
print(n, "solapes >=", MIN, "s")
