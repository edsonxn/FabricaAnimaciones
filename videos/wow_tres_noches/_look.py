# -*- coding: utf-8 -*-
"""Hoja de prueba del look:  python _look.py cementerio:1.0 danza:2.5 recuerdo:0.5 ... [--out nombre] [-f]
Dibuja cada lámina de look.py en ese segundo y las junta en previews/<nombre>.jpg (640x360 c/u). -f guarda además cada una
a tamaño completo en previews/look_<lamina>_<t>.jpg."""
import os
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))
sys.path.insert(0, AQUI)

import cv2  # noqa: E402
import numpy as np  # noqa: E402

import look  # noqa: E402

args = [a for a in sys.argv[1:] if not a.startswith("-")]
full = "-f" in sys.argv
out = "look"
if "--out" in sys.argv:
    out = sys.argv[sys.argv.index("--out") + 1]
    args.remove(out)
cel = []
for a in args:
    nombre, t = a.split(":")
    t0 = time.time()
    im = (np.clip(look.LAMINAS[nombre](float(t)), 0, 1) * 255).astype(np.uint8)[..., ::-1]
    print(f"{nombre} t={t}: {time.time() - t0:.2f} s")
    if full:
        cv2.imwrite(f"previews/look_{nombre}_{float(t):05.2f}.jpg", im, [cv2.IMWRITE_JPEG_QUALITY, 92])
    ch = cv2.resize(im, (640, 360), interpolation=cv2.INTER_AREA)
    cv2.putText(ch, a, (8, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 4)
    cv2.putText(ch, a, (8, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    cel.append(ch)
cols = min(2, len(cel))
while len(cel) % cols:
    cel.append(np.zeros_like(cel[0]))
hoja = np.vstack([np.hstack(cel[i:i + cols]) for i in range(0, len(cel), cols)])
cv2.imwrite(f"previews/{out}.jpg", hoja, [cv2.IMWRITE_JPEG_QUALITY, 88])
print(f"previews/{out}.jpg")
