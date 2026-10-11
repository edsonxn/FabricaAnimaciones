# -*- coding: utf-8 -*-
"""Hoja de contacto de tiempos globales: python hoja.py salida.jpg t1 t2 ...  (o rangos a:b:n)"""
import sys, os
import cv2, numpy as np
import estilos
estilos.activar("kurzgesagt")
from motor import Lienzo, a_uint8
import escenas as S

out = sys.argv[1]
ts = []
for a in sys.argv[2:]:
    if ":" in a:
        x, y, n = a.split(":")
        ts += list(np.linspace(float(x), float(y), int(n)))
    else:
        ts.append(float(a))
lz = Lienzo()
tiles = []
for t in ts:
    img = S.render_mundo(lz, t)
    im = cv2.resize(a_uint8(img), (640, 360), interpolation=cv2.INTER_AREA)
    cv2.putText(im, f"t={t:.1f}", (8, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
    tiles.append(im)
while len(tiles) % 3:
    tiles.append(np.zeros_like(tiles[0]))
rows = [np.hstack(tiles[i:i + 3]) for i in range(0, len(tiles), 3)]
cv2.imwrite(os.path.join("previews", out), cv2.cvtColor(np.vstack(rows), cv2.COLOR_RGB2BGR))
print("ok", len(ts))
