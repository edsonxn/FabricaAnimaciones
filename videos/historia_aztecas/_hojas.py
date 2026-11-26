# -*- coding: utf-8 -*-
"""Hojas de revisión de todo el video: python _hojas.py paso [t0 t1] -> previews/rev_NN.jpg (12 cuadros de 640x360 por hoja)."""
import sys
import cv2
import numpy as np
import escenas as E
paso = float(sys.argv[1]) if len(sys.argv) > 1 else 3.0
t0 = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
t1 = float(sys.argv[3]) if len(sys.argv) > 3 else E.TOTAL
m = E.Mundo(E.TL["escenas"][0], 0)
ts = list(np.arange(t0, t1, paso))
for h in range(0, len(ts), 12):
    tiles = []
    for t in ts[h:h + 12]:
        im = (np.clip(m.render(None, float(t)), 0, 1)[..., ::-1] * 255).astype(np.uint8)
        s = cv2.resize(im, (640, 360), interpolation=cv2.INTER_AREA)
        cv2.putText(s, f"{t:.1f}", (8, 352), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        tiles.append(s)
    while len(tiles) % 3:
        tiles.append(np.zeros_like(tiles[0]))
    rows = [np.hstack(tiles[i:i + 3]) for i in range(0, len(tiles), 3)]
    cv2.imwrite(f"previews/rev_{h // 12:02d}.jpg", np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 85])
    print("hoja", h // 12, flush=True)
