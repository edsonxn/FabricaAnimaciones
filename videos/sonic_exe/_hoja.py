# -*- coding: utf-8 -*-
"""Hoja de prueba:  python _hoja.py 0.8 2.0 3.4 ... [-f] [--out nombre]
Dibuja esos segundos con `escenas.cuadro` y los junta en previews/<nombre>.jpg (cada cuadro a 360x640).
-f guarda además cada cuadro a tamaño completo en previews/c_<t>.jpg. `a:b:paso` = rango de segundos."""
import os
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))
sys.path.insert(0, AQUI)

import cv2  # noqa: E402
import numpy as np  # noqa: E402

import escenas  # noqa: E402

args = [a for a in sys.argv[1:] if not a.startswith("-")]
full = "-f" in sys.argv
out = "hoja"
if "--out" in sys.argv:
    out = sys.argv[sys.argv.index("--out") + 1]
    args.remove(out)
ts = []
for a in args:
    if ":" in a:
        x, y, s = (float(v) for v in a.split(":"))
        ts += list(np.arange(x, y + 1e-6, s))
    else:
        ts.append(float(a))
cel = []
t0 = time.time()
for t in ts:
    im = (np.clip(escenas.cuadro(t), 0, 1) * 255).astype(np.uint8)[..., ::-1]
    if full:
        cv2.imwrite(f"previews/c_{t:07.2f}.jpg", im, [cv2.IMWRITE_JPEG_QUALITY, 92])
    ch = cv2.resize(im, (640, 360), interpolation=cv2.INTER_AREA)
    cv2.putText(ch, f"{t:.2f}", (8, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 5)
    cv2.putText(ch, f"{t:.2f}", (8, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
    cel.append(ch)
cols = min(3, len(cel))
while len(cel) % cols:
    cel.append(np.zeros_like(cel[0]))
hoja = np.vstack([np.hstack(cel[i:i + cols]) for i in range(0, len(cel), cols)])
cv2.imwrite(f"previews/{out}.jpg", hoja, [cv2.IMWRITE_JPEG_QUALITY, 88])
print(f"previews/{out}.jpg  {len(ts)} cuadros  {(time.time() - t0) / max(1, len(ts)):.2f} s/cuadro")
