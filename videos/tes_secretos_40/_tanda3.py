# -*- coding: utf-8 -*-
"""Vuelta 3 (30-oct): los 11 que quedaban salen de un longplay limpio ya visto (Loopy Longplays), cada uno en otro minuto."""
import json

U = "https://youtu.be/JV3tKszygTU"
D = {18: 300, 27: 700, 32: 1100, 37: 1500, 52: 1900, 58: 2300, 73: 3100, 80: 3500, 89: 3900, 94: 4300, 107: 4700}
p = "videos/tes_secretos_40/busquedas.json"
d = json.load(open(p, encoding="utf-8"))
for k, t in D.items():
    d[f"scene-{k:03d}"] = {"url": U, "desde": t}
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(",".join(str(k) for k in D))
