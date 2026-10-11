# -*- coding: utf-8 -*-
"""Barrido de control: un cuadro cada `paso` s de todo el video (detecta errores y arma hojas de revisión).
python _barrido.py [paso] [t_ini] [t_fin] -> previews/barrido_XX.jpg (30 cuadros por hoja, 480x270) y lista de fallas"""
import sys
import time
import traceback

import cv2
import numpy as np

import escenas as S
from kit import TL, TOTAL

paso = float(sys.argv[1]) if len(sys.argv) > 1 else 3.0
t_ini = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
t_fin = float(sys.argv[3]) if len(sys.argv) > 3 else TOTAL
m = S.CLASES[TL["escenas"][0]["id"]](TL["escenas"][0], 0)
ims, fallas, hoja = [], [], 0
t = t_ini
t0 = time.time()
while t < t_fin:
    try:
        f = m.render(None, t)
        f8 = cv2.cvtColor((np.clip(f, 0, 1) * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
    except Exception as e:
        fallas.append((t, repr(e)))
        traceback.print_exc()
        f8 = np.zeros((1080, 1920, 3), np.uint8)
    s = cv2.resize(f8, (480, 270), interpolation=cv2.INTER_AREA)
    cv2.putText(s, f"{int(t // 60)}:{t % 60:04.1f}", (6, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2, cv2.LINE_AA)
    ims.append(s)
    if len(ims) == 30:
        cv2.imwrite(f"previews/barrido_{hoja:02d}.jpg", np.vstack([np.hstack(ims[i:i + 5]) for i in range(0, 30, 5)]), [cv2.IMWRITE_JPEG_QUALITY, 85])
        hoja += 1
        ims = []
    t += paso
if ims:
    while len(ims) % 5:
        ims.append(np.zeros_like(ims[0]))
    cv2.imwrite(f"previews/barrido_{hoja:02d}.jpg", np.vstack([np.hstack(ims[i:i + 5]) for i in range(0, len(ims), 5)]), [cv2.IMWRITE_JPEG_QUALITY, 85])
print(f"{time.time() - t0:.0f}s; fallas: {len(fallas)}", fallas[:10])
