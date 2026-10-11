# -*- coding: utf-8 -*-
"""Hoja de contacto de cuadros del mundo: python _prueba.py t1 t2 ... (desde la carpeta del video, PYTHONPATH con nucleo)."""
import sys
import time

import cv2
import numpy as np

import escenas as S

m = S.CLASES["nube"](S._ESC["nube"], 0)
ts = [float(x) for x in sys.argv[1:]]
tiles = []
for t in ts:
    t0 = time.time()
    im = m.render(None, t)
    print(t, round(time.time() - t0, 2), flush=True)
    im = (im * 255).astype(np.uint8)
    tiles.append(cv2.resize(im, (360, 640), interpolation=cv2.INTER_AREA))
    cv2.putText(tiles[-1], f"{t:.1f}", (6, 630), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
while len(tiles) % 6:
    tiles.append(np.zeros_like(tiles[0]))
hoja = np.vstack([np.hstack(tiles[i:i + 6]) for i in range(0, len(tiles), 6)])
cv2.imwrite('previews/hoja.jpg', cv2.cvtColor(hoja, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 88])
