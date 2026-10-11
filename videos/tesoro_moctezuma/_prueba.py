# -*- coding: utf-8 -*-
"""Hoja de cuadros: python _prueba.py nombre t1 t2 ...  (o a:b:n)  ->  previews/<nombre>.jpg"""
import sys, os, time
import cv2, numpy as np
import estilos
estilos.activar("kurzgesagt")
from motor import Lienzo, a_uint8
import escenas as S
out = sys.argv[1]
ts = []
for a in sys.argv[2:]:
    if ":" in a:
        x, y, n = a.split(":"); ts += list(np.linspace(float(x), float(y), int(n)))
    else:
        ts.append(float(a))
lz = Lienzo()
tiles = []
for t in ts:
    t0 = time.time()
    img = S.render_mundo(lz, t)
    print(f"t={t:6.2f} {time.time() - t0:.2f}s", flush=True)
    im = cv2.resize(a_uint8(img), (640, 360), interpolation=cv2.INTER_AREA)
    cv2.putText(im, f"{t:.1f}", (8, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2, cv2.LINE_AA)
    tiles.append(im)
while len(tiles) % 3: tiles.append(np.zeros_like(tiles[0]))
cv2.imwrite(f"previews/{out}.jpg", cv2.cvtColor(np.vstack([np.hstack(tiles[i:i + 3]) for i in range(0, len(tiles), 3)]), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
