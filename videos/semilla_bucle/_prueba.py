# -*- coding: utf-8 -*-
"""Hoja de contacto de cuadros del mundo: python _prueba.py t1 t2 ..."""
import os
import sys
import time

sys.path.insert(0, os.path.abspath("../../nucleo"))
sys.path.insert(0, os.path.abspath("."))

import cv2
import numpy as np

import escenas as S

m = S.CLASES["vuelo"](S._ESC["vuelo"], 0)
ts = [float(x) for x in sys.argv[1:]]
if not ts:
    # Muestreo por defecto a lo largo del video
    ts = [0.0, 3.0, 8.0, 13.0, 18.0, 23.0, 29.0, 34.0, 39.0, 44.0, 48.0, float(S.TOTAL) - 0.04]

tiles = []
for t in ts:
    t0 = time.time()
    im = m.render(None, t)
    dt = time.time() - t0
    print(f"t={t:.2f} s ({dt:.2f}s)", flush=True)
    im = (im * 255).astype(np.uint8)
    tile = cv2.resize(im, (360, 640), interpolation=cv2.INTER_AREA)
    cv2.putText(tile, f"t={t:.1f}s", (10, 620), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    tiles.append(tile)

n_cols = 4
while len(tiles) % n_cols:
    tiles.append(np.zeros_like(tiles[0]))

hoja = np.vstack([np.hstack(tiles[i:i + n_cols]) for i in range(0, len(tiles), n_cols)])
cv2.imwrite('previews/hoja_semilla.jpg', cv2.cvtColor(hoja, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
print("Guardado en previews/hoja_semilla.jpg")
