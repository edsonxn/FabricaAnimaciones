# -*- coding: utf-8 -*-
"""Quita clips repetidos entre beats (misma url a < 12 s) y evita las opciones con tramos negros (medir_brillo).
Reescribe busquedas.json y borra medios/scene-NNN.mp4 de los beats que cambian (luego `fab.py <v> bajar`).
    python _dedupe_clips.py
"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
plan = json.load(open("plan_frases.json", encoding="utf-8"))
bus = json.load(open("busquedas.json", encoding="utf-8"))
VETADAS = {("7BnZhJg91RQ", 46), ("U-hb0vL5sgg", 92), ("c5mltemiLdA", 60), ("dEwcTvkOnNw", 102)}
NEGRO = {"scene-001", "scene-078", "scene-101", "scene-112", "scene-180", "scene-190"}
usados = []          # (vid, desde)


def vid(u):
    return u.rstrip("/")[-11:]


def libre(v, d):
    return (v, d) not in VETADAS and all(not (v == v2 and abs(d - d2) < 12) for v2, d2 in usados)


cambios = []
for sid in sorted(bus):
    b = bus[sid]
    v0, d0 = vid(b["url"]), int(b["desde"])
    if sid not in NEGRO and libre(v0, d0):
        usados.append((v0, d0))
        continue
    ops = plan.get(b.get("_frase", ""), [])
    elegido = next(((o["url"], int(o["desde"])) for o in ops if libre(vid(o["url"]), int(o["desde"]))), None)
    if elegido is None:                                   # sin opción libre: misma fuente, más adelante
        base = ops[0] if ops else b
        for k in range(1, 20):
            d = int(base["desde"]) + 14 * k
            if libre(vid(base["url"]), d):
                elegido = (base["url"], d)
                break
    b["url"], b["desde"] = elegido
    usados.append((vid(elegido[0]), elegido[1]))
    cambios.append(sid)
    f = os.path.join("medios", sid + ".mp4")
    if os.path.exists(f):
        os.remove(f)
json.dump(bus, open("busquedas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(cambios), "beats cambiados:", " ".join(cambios))
