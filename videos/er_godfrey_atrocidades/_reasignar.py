# -*- coding: utf-8 -*-
"""Reasigna beats concretos a otra opción libre del plan (misma frase o vecinas), vetando la que tenían; borra su clip.
    python _reasignar.py scene-043 scene-102 ...      (sin argumentos: los que no tienen clip o pesan < 5 KB)
"""
import json
import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
plan = json.load(open("plan_frases.json", encoding="utf-8"))
bus = json.load(open("busquedas.json", encoding="utf-8"))
vid = lambda u: u.rstrip("/")[-11:]
vetos = json.load(open("_vetos.json", encoding="utf-8")) if os.path.exists("_vetos.json") else []
ids = sys.argv[1:] or [s for s in bus if not os.path.exists(f"medios/{s}.mp4") or os.path.getsize(f"medios/{s}.mp4") < 5000]
claves = list(plan)
for s in ids:
    vetos.append([vid(bus[s]["url"]), int(bus[s]["desde"])])
usados = [(vid(v["url"]), int(v["desde"])) for k, v in bus.items() if k not in ids]
libre = lambda v, d: [v, d] not in vetos and all(not (v == v2 and abs(d - d2) < 12) for v2, d2 in usados)
for s in ids:
    fr = bus[s].get("_frase", "")
    i = claves.index(fr) if fr in claves else 0
    cand = [o for k in [fr] + claves[max(0, i - 1):i + 2] for o in plan.get(k, [])]
    elegido = None
    for off in (0, 15, -10, 30):
        for o in cand:
            v, d = vid(o["url"]), max(0, int(o["desde"]) + off)
            if libre(v, d):
                elegido = (o["url"], d)
                break
        if elegido:
            break
    bus[s]["url"], bus[s]["desde"] = elegido
    usados.append((vid(elegido[0]), elegido[1]))
    if os.path.exists(f"medios/{s}.mp4"):
        os.remove(f"medios/{s}.mp4")
    print(s, fr, elegido)
json.dump(bus, open("busquedas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(vetos, open("_vetos.json", "w", encoding="utf-8"))
