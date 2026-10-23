# -*- coding: utf-8 -*-
"""Hoja de contacto: python _prueba.py t1 t2 ... [--full] -> previews/hoja.jpg (cuadros 360x640, vertical) y, con --full, previews/full_<t>.jpg a 1080x1920."""
import sys
import time

import cv2
import numpy as np

import escenas as E

full = "--full" in sys.argv
OUT = next((a[6:] for a in sys.argv if a.startswith("--out=")), "hoja")
ts = [float(a) for a in sys.argv[1:] if not a.startswith("--")]
cols = 6 if len(ts) > 6 else max(1, len(ts))
m = E.Mundo(E.TL["escenas"][0], 0)
tiles = []
for t in ts:
    t0 = time.time()
    im = m.render(None, t)
    dt = time.time() - t0
    print(f"t={t:6.2f}  {dt * 1000:5.0f} ms", flush=True)
    big = (np.clip(im, 0, 1)[..., ::-1] * 255).astype(np.uint8)
    if full:
        cv2.imwrite(f"previews/full_{OUT}_{t:06.2f}.jpg", big, [cv2.IMWRITE_JPEG_QUALITY, 92])
    small = cv2.resize(big, (360, 640), interpolation=cv2.INTER_AREA)
    cv2.putText(small, f"{t:.2f}", (10, 630), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    tiles.append(small)
while len(tiles) % cols:
    tiles.append(np.zeros_like(tiles[0]))
rows = [np.hstack(tiles[i:i + cols]) for i in range(0, len(tiles), cols)]
cv2.imwrite(f"previews/{OUT}.jpg", np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 88])
