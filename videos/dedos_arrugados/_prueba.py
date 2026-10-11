# -*- coding: utf-8 -*-
"""Hoja de contacto: python _prueba.py t1 t2 ...   (-f: guarda cada cuadro a tamaño completo en previews/c_<t>.png)
Desde la carpeta del video con PYTHONPATH = video + nucleo (ver run.ps1)."""
import sys
import time

import cv2
import numpy as np

import escenas as S

args = [a for a in sys.argv[1:] if not a.startswith("-")]
full = "-f" in sys.argv
ts = [float(x) for x in args]
tiles = []
for t in ts:
    k = max(i for i, e in enumerate(S._ORD) if S.INI(e) <= t + 1e-6)
    t0 = time.time()
    im = S.cuadro(S._ORD[k], t)
    if im.dtype != np.uint8:
        im = (np.clip(im, 0, 1) * 255).astype(np.uint8)
    im = (im.astype(np.float32) * S.vineta()).astype(np.uint8)
    print(t, S._ORD[k], round(time.time() - t0, 2), flush=True)
    if full:
        cv2.imwrite(f"previews/c_{t:05.2f}.png", cv2.cvtColor(im, cv2.COLOR_RGB2BGR))
    tiles.append(cv2.resize(im, (360, 640), interpolation=cv2.INTER_AREA))
    cv2.putText(tiles[-1], f"{t:.2f}", (6, 630), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
while len(tiles) % 6:
    tiles.append(np.zeros_like(tiles[0]))
hoja = np.vstack([np.hstack(tiles[i:i + 6]) for i in range(0, len(tiles), 6)])
cv2.imwrite("previews/hoja.jpg", cv2.cvtColor(hoja, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
