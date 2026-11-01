# -*- coding: utf-8 -*-
"""Lista de las hojas ELEGIDAS para bajar en 2K desde Flow (proyecto «oct 21 - 17:09»): clave, variante original y uuid de la imagen
(el src de cada mosaico es https://flow-content.google/image/<uuid>?…). Escribe _2k_pendientes.txt.
Orden del lote: claves en orden ALFABÉTICO, scene N = k+1, prompt k//2, variante k%2 (0 = a original, 1 = b original)."""
import json
import os

d = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(d, "prompts.json"), encoding="utf-8"))
claves = sorted(P)
B = set(open(os.path.join(d, "hojas", "_elegidas.txt"), encoding="utf-8").read().split())
SCR = r"C:\Users\jaire\AppData\Local\Temp\claude\C--FabricaAnimaciones\50a18967-a3ef-4340-b078-47f0736edf29\scratchpad"
uu = {}
for f in ("lineas1.txt", "lineas2.txt"):
    for ln in open(os.path.join(SCR, f), encoding="utf-8"):
        p = ln.split()
        if len(p) >= 2:
            uu[int(p[0])] = p[1]
out = []
for i, c in enumerate(claves):
    if c.startswith("e"):
        continue
    v = 1 if c in B else 0
    out.append(f"{c}\t{'ab'[v]}\t{uu[2 * i + v + 1]}")
open(os.path.join(d, "_2k_pendientes.txt"), "w", encoding="utf-8").write("\n".join(out) + "\n")
print(len(out), "hojas →", os.path.join(d, "_2k_pendientes.txt"))
