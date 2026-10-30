# -*- coding: utf-8 -*-
"""Vuelta 4 (30-oct): 5 clips junto a tramos ya limpios del mismo longplay."""
import json

U = "https://youtu.be/JV3tKszygTU"
D = {32: 325, 37: 725, 52: 2325, 80: 3930, 107: 4330}
p = "videos/tes_secretos_40/busquedas.json"
d = json.load(open(p, encoding="utf-8"))
for k, t in D.items():
    d[f"scene-{k:03d}"] = {"url": U, "desde": t}
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(",".join(str(k) for k in D))
