# -*- coding: utf-8 -*-
"""Prueba del arreglo de fundido entre rejillas con la copia _escenas_fix.py (no toca escenas.py): python _prueba_fix.py [--viejo] t1 t2 ..."""
import sys
import cv2
import numpy as np

viejo = "--viejo" in sys.argv
E = __import__("escenas" if viejo else "_escenas_fix")
ts = [float(a) for a in sys.argv[1:] if not a.startswith("--")]
m = E.Mundo(E.TL["escenas"][0], 0)
tiles = []
for t in ts:
    im = m.render(None, t)
    big = (np.clip(im, 0, 1)[..., ::-1] * 255).astype(np.uint8)
    if len(ts) == 1:
        cv2.imwrite(f"previews/_dbg/full_{'viejo' if viejo else 'nuevo'}_{t:.2f}.jpg", big, [cv2.IMWRITE_JPEG_QUALITY, 92])
    small = cv2.resize(big, (640, 360), interpolation=cv2.INTER_AREA)
    cv2.putText(small, f"{t:.2f} w={E.R.peso_am(t):.2f}", (8, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    tiles.append(small)
while len(tiles) % 3:
    tiles.append(np.zeros_like(tiles[0]))
cv2.imwrite(f"previews/_dbg/hoja_{'viejo' if viejo else 'nuevo'}.jpg", np.vstack([np.hstack(tiles[i:i + 3]) for i in range(0, len(tiles), 3)]), [cv2.IMWRITE_JPEG_QUALITY, 90])
print("listo")
