# -*- coding: utf-8 -*-
"""Quita el marco de papel que Flow pinta a veces alrededor de un escenario (e02_canon_amanecer_a, 21-oct-2026) y deja 16:9.
Receta de videos/secreto_ia/_ordenar_flow.py. El original queda en imagenes/_conmarco/."""
import glob
import os
import shutil

import numpy as np
from PIL import Image

d = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(d, "imagenes", "_conmarco"), exist_ok=True)


def borde(lineas):
    n = 0
    for v in lineas:
        if v.std() < 9 and (v.mean() > 175 or v.mean() < 18):
            n += 1
        else:
            break
    return n


for p in sorted(glob.glob(os.path.join(d, "imagenes", "e*.jpg"))):
    im = Image.open(p).convert("RGB")
    a = np.asarray(im.convert("L"), np.float32)
    h, w = a.shape
    t = borde(a[i] for i in range(h // 6))
    b = borde(a[h - 1 - i] for i in range(h // 6))
    l = borde(a[:, i] for i in range(w // 6))
    r = borde(a[:, w - 1 - i] for i in range(w // 6))
    if max(t, b, l, r) < 3:
        continue
    m = 6
    x0, y0, x1, y1 = l + m * (l > 0), t + m * (t > 0), w - r - m * (r > 0), h - b - m * (b > 0)
    cw, ch = x1 - x0, y1 - y0
    if cw / ch > 16 / 9:
        nw = int(ch * 16 / 9); x0 += (cw - nw) // 2; x1 = x0 + nw
    else:
        nh = int(cw * 9 / 16); y0 += (ch - nh) // 2; y1 = y0 + nh
    shutil.copy2(p, os.path.join(d, "imagenes", "_conmarco", os.path.basename(p)))
    im.crop((x0, y0, x1, y1)).resize((w, h), Image.LANCZOS).save(p, quality=95)
    print(f"{os.path.basename(p):34s} marco t/b/l/r = {t},{b},{l},{r}")
