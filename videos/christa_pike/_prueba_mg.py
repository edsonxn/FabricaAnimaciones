# -*- coding: utf-8 -*-
"""Prueba de escenas dibujadas: python _prueba_mg.py <escena> tl1 tl2 ...   (tl = segundos desde el inicio de la escena)
-> previews/mg_<escena>.jpg (hoja 2 columnas a 960x540). Sin argumentos de tiempo, usa 5 puntos repartidos."""
import sys
import time
import cv2
import numpy as np
import mg_esc as E
import importlib
for _m in ('mg_esc2', 'mg_esc3', 'mg_esc4'):
    try:
        importlib.import_module(_m)
    except ModuleNotFoundError:
        pass
from motor import H, W

nombre = sys.argv[1]
fn, ini, fin = E.ESC[nombre]
t0, t1 = ini(), fin()
dur = t1 - t0 + 0.5
tls = [float(x) for x in sys.argv[2:]] or list(np.linspace(0.2, max(0.5, t1 - t0 - 0.2), 6))
ims = []
for tl in tls:
    t = time.time()
    lz = np.zeros((H, W, 3), np.float32)
    fn(lz, tl, t0 + tl, dur, 1.0)
    print(f"{nombre} tl={tl:5.2f} {1000 * (time.time() - t):.0f} ms", flush=True)
    f8 = cv2.cvtColor((np.clip(lz, 0, 1) * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
    cv2.putText(f8, f"{tl:.2f}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)
    ims.append(cv2.resize(f8, (960, 540), interpolation=cv2.INTER_AREA))
while len(ims) % 2:
    ims.append(np.zeros_like(ims[0]))
cv2.imwrite(f"previews/mg_{nombre}.jpg", np.vstack([np.hstack(ims[i:i + 2]) for i in range(0, len(ims), 2)]), [cv2.IMWRITE_JPEG_QUALITY, 90])
print("ok")
