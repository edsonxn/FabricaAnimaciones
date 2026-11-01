# -*- coding: utf-8 -*-
"""medios/scene-NNN.jpg (orden de envío del lote de Flow del 21-oct) → imagenes/<clave>_a|b.jpg (escenarios) y hojas/<clave>_a|b.jpg.
El paquete `_bundle.js` envía los prompts en orden ALFABÉTICO de clave: N = k+1, prompt k//2, variante k%2."""
import json
import os
import shutil

d = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(d, "prompts.json"), encoding="utf-8"))
claves = sorted(P)
for sub in ("imagenes", "hojas"):
    os.makedirs(os.path.join(d, sub), exist_ok=True)
n = 0
for k in range(2 * len(claves)):
    src = os.path.join(d, "medios", f"scene-{k + 1:03d}.jpg")
    clave = claves[k // 2]
    sub = "imagenes" if clave.startswith("e") else "hojas"
    dst = os.path.join(d, sub, f"{clave}_{'ab'[k % 2]}.jpg")
    if os.path.exists(src):
        shutil.copy2(src, dst)
        n += 1
print("repartidas", n, "de", 2 * len(claves))
