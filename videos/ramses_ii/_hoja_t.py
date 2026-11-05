# -*- coding: utf-8 -*-
"""Hoja de cuadros en tiempos dados: python _hoja_t.py salida.jpg t1 t2 ... (3 columnas, 640x360)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "nucleo"))
import cv2, numpy as np
import escenas as E
out, ts = sys.argv[1], [float(x) for x in sys.argv[2:]]
cs = []
for t in ts:
    c = cv2.resize((np.clip(E.render_mundo(t), 0, 1) * 255).astype(np.uint8), (640, 360), interpolation=cv2.INTER_AREA)
    cv2.putText(c, f"{t:.1f}", (6, 18), 0, 0.55, (255, 255, 0), 1)
    cs.append(c)
while len(cs) % 3:
    cs.append(np.zeros_like(cs[0]))
cv2.imwrite(out, cv2.cvtColor(np.vstack([np.hstack(cs[i:i + 3]) for i in range(0, len(cs), 3)]), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 82])
