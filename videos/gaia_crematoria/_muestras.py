# -*- coding: utf-8 -*-
"""Hoja de muestras del render: python _muestras.py <salida.jpg> t1 t2 ... | <salida.jpg> --rango t0 t1 paso
Cada cuadro a 640x360 con su tiempo (desde la carpeta del video)."""
import os
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
sys.path[:0] = [AQUI, os.path.join(AQUI, "..", "..", "nucleo")]
import numpy as np  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

import escenas  # noqa: E402

sal = sys.argv[1]
if sys.argv[2] == "--rango":
    a, b, p = map(float, sys.argv[3:6])
    ts = [float(x) for x in np.arange(a, b, p)]
else:
    ts = [float(x) for x in sys.argv[2:]]
cols = 4
w, h = 640, 360
hoja = Image.new("RGB", (w * cols, (h + 20) * ((len(ts) + cols - 1) // cols)), (0, 0, 0))
d = ImageDraw.Draw(hoja)
t_ini = time.time()
for i, t in enumerate(ts):
    img = escenas.render_mundo(t)
    im = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8)).resize((w, h))
    x, y = (i % cols) * w, (i // cols) * (h + 20)
    hoja.paste(im, (x, y + 20))
    d.text((x + 4, y + 3), f"{t:.1f}s", fill=(255, 220, 0))
hoja.save(sal, quality=82)
print(sal, len(ts), "cuadros", f"{(time.time() - t_ini) / max(1, len(ts)):.2f} s/cuadro")
