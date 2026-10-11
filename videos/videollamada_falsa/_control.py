# -*- coding: utf-8 -*-
"""Hoja de control con cuadros sueltos de varias escenas (tiempos LOCALES):
    python _control.py regla:15.4 llamada:17 truco:6,29.5      -> previews/control.jpg (3 columnas, 640x360)"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [AQUI, os.path.join(AQUI, "..", "..", "nucleo")]
os.chdir(AQUI)

import cv2
import numpy as np

import escenas as S

TL = json.load(open("timeline.json", encoding="utf-8"))
IDS = [e["id"] for e in TL["escenas"]]
tiles = []
for a in sys.argv[1:]:
    eid, _, us = a.partition(":")
    d = TL["escenas"][IDS.index(eid)]
    esc = S.CLASES[eid](d, IDS.index(eid))
    for u in us.split(","):
        im = (np.clip(esc.render(None, d["t0"] + float(u)), 0, 1) * 255).astype(np.uint8)
        sm = cv2.resize(im, (640, 360), interpolation=cv2.INTER_AREA)
        cv2.putText(sm, f"{eid} u={u}", (6, 352), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        tiles.append(sm)
while len(tiles) % 3:
    tiles.append(np.zeros_like(tiles[0]))
hoja = np.vstack([np.hstack(tiles[i:i + 3]) for i in range(0, len(tiles), 3)])
cv2.imwrite("previews/control.jpg", cv2.cvtColor(hoja, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
print(len(tiles), "cuadros -> previews/control.jpg")
