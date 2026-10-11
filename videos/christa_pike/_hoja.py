# -*- coding: utf-8 -*-
"""Hoja de contacto de cuadros reales de Mundo.  python _hoja.py t1 t2 ...  ->  previews/hoja.jpg (y cuadros sueltos previews/q_<t>.jpg con --solos)"""
import sys, time
import cv2, numpy as np
import escenas as S
from escena_base import TL
ts = [float(x) for x in sys.argv[1:] if not x.startswith("--")]
solos = "--solos" in sys.argv
m = S.CLASES[TL["escenas"][0]["id"]](TL["escenas"][0], 0)
im = []
for t in ts:
    t0 = time.time()
    f = m.render(None, t)
    print(f"t={t:6.2f}  {time.time() - t0:.2f}s", flush=True)
    f8 = cv2.cvtColor((np.clip(f, 0, 1) * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
    if solos:
        cv2.imwrite(f"previews/q_{t:.1f}.jpg", f8, [cv2.IMWRITE_JPEG_QUALITY, 92])
    cv2.putText(f8, f"{t:.2f}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)
    im.append(cv2.resize(f8, (640, 360), interpolation=cv2.INTER_AREA))
cols = 3
while len(im) % cols: im.append(np.zeros_like(im[0]))
hoja = np.vstack([np.hstack(im[i:i + cols]) for i in range(0, len(im), cols)])
cv2.imwrite("previews/hoja.jpg", hoja, [cv2.IMWRITE_JPEG_QUALITY, 88])
print("ok", hoja.shape)
