"""Hoja de prueba de escenas.py (desde la carpeta del video): python _hoja.py <salida.jpg> t1 t2 ...  (cuadros 640x360, 4 por fila)
Sin argumentos de tiempo: un cuadro a mitad de cada toma."""
import os
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))
sys.path.insert(0, AQUI)

import cv2  # noqa: E402
import numpy as np  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

import escenas as S  # noqa: E402

sal = sys.argv[1]
ts = [float(x) for x in sys.argv[2:]]
if not ts:
    TT = S.TOMAS
    ts = [round((TT[i]["t0"] + (TT[i + 1]["t0"] if i + 1 < len(TT) else S.TOTAL)) / 2 + 0.25, 2) for i in range(len(TT))]
cols = 4
w, h = 640, 360
filas = (len(ts) + cols - 1) // cols
hoja = Image.new("RGB", (cols * w, filas * (h + 20)), "white")
d = ImageDraw.Draw(hoja)
t_ini = time.time()
for i, t in enumerate(ts):
    img = S.render_mundo(t)
    im = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8)).resize((w, h), Image.LANCZOS)
    x, y = (i % cols) * w, (i // cols) * (h + 20)
    hoja.paste(im, (x, y + 20))
    d.text((x + 4, y + 4), f"t={t:.2f}", fill="black")
hoja.save(sal, quality=86)
print(len(ts), "cuadros en", round(time.time() - t_ini, 1), "s ->", sal)
