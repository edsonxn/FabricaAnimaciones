# -*- coding: utf-8 -*-
"""Hoja de contacto de una escena con tiempos LOCALES (s desde el inicio de la escena):
    python videos/ia_noir/_prueba.py sala 0.2 1.2 2.4        -> previews/p_sala.jpg (3 columnas, 360x640) + previews/p_sala_<u>.png (completo)
    python videos/ia_noir/_prueba.py sala 2.9..3.4:0.1       -> rango u0..u1 con paso (cuadros consecutivos a 1/3 de tamaño)
    opciones: --solo-hoja (no guarda los PNG completos)  --cols 6"""
import json
import os
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [AQUI, os.path.join(AQUI, "..", "..", "nucleo")]
os.chdir(AQUI)

import cv2
import numpy as np

import escenas as S

TL = json.load(open("timeline.json", encoding="utf-8"))
args = [a for a in sys.argv[1:] if not a.startswith("--")]
solo_hoja = "--solo-hoja" in sys.argv
cols = int(sys.argv[sys.argv.index("--cols") + 1]) if "--cols" in sys.argv else 3
if "--cols" in sys.argv:
    args = [a for a in args if a != str(cols)]
eid = args[0]
tiempos = []
for a in args[1:]:
    if ".." in a:
        r, _, paso = a.partition(":")
        u0, u1 = (float(x) for x in r.split(".."))
        paso = float(paso) if paso else 0.1
        tiempos += list(np.arange(u0, u1 + 1e-6, paso))
    else:
        tiempos.append(float(a))
d = [e for e in TL["escenas"] if e["id"] == eid][0]
esc = S.CLASES[eid](d, [e["id"] for e in TL["escenas"]].index(eid))
os.makedirs("previews", exist_ok=True)
tiles = []
for u in tiempos:
    t = d["t0"] + u
    t0 = time.time()
    img = esc.render(None, t)
    dt = time.time() - t0
    im = (np.clip(img, 0, 1) * 255).astype(np.uint8)
    if not solo_hoja and len(tiempos) <= 12:
        cv2.imwrite(f"previews/p_{eid}_{u:05.2f}.png", cv2.cvtColor(im, cv2.COLOR_RGB2BGR))
    esc_ = 640 if cols <= 3 else 480
    sm = cv2.resize(im, (esc_, esc_ * 9 // 16), interpolation=cv2.INTER_AREA)
    for col, gr in (((0, 0, 0), 3), ((255, 255, 255), 1)):
        cv2.putText(sm, f"u={u:.2f} {dt * 1000:.0f}ms", (6, sm.shape[0] - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, col, gr, cv2.LINE_AA)
    tiles.append(sm)
while len(tiles) % cols:
    tiles.append(np.zeros_like(tiles[0]))
hoja = np.vstack([np.hstack(tiles[i:i + cols]) for i in range(0, len(tiles), cols)])
cv2.imwrite(f"previews/p_{eid}.jpg", cv2.cvtColor(hoja, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
print(f"{len(tiempos)} cuadros -> previews/p_{eid}.jpg")
