# -*- coding: utf-8 -*-
"""Miniaturas de los dibujos del catálogo para el selector del Estudio -> estudio/iconos/<nombre>.png (fondo transparente).
Se corre desde una carpeta de proyecto (necesita guion.py); el servidor la lanza la primera vez."""
import json
import os
import sys

import cv2
import numpy as np

SAL = sys.argv[1]
os.makedirs(SAL, exist_ok=True)
if not os.path.exists("timeline.json"):
    import muestra_estilo
    _tl = muestra_estilo.timeline_provisional()
    with open("timeline.json", "w", encoding="utf-8") as f:
        json.dump(_tl, f, ensure_ascii=False)
import escena_base as B  # noqa: E402
from motor import Lienzo, a_uint8, componer  # noqa: E402

lz = Lienzo()
for n in sorted(B.ICONOS):
    ruta = os.path.join(SAL, f"{n}.png")
    if os.path.exists(ruta):
        continue
    lz.nuevo(1.0)
    B.dibujar_icono(lz, n, 960, 540, 1.5, 1.0)
    capa = lz.resolver()
    negro = componer(np.zeros((1080, 1920, 3), np.float32), capa, boil=0)
    blanco = componer(np.ones((1080, 1920, 3), np.float32), capa, boil=0)
    alfa = np.clip(1 - (blanco - negro).mean(-1), 0, 1)
    rgb = np.where(alfa[..., None] > 1e-3, negro / np.maximum(alfa[..., None], 1e-3), 0)
    img = np.dstack([a_uint8(np.clip(rgb, 0, 1)), (alfa * 255).astype(np.uint8)])[:, 420:1500]
    ys, xs = np.nonzero(img[..., 3] > 8)
    if len(xs):
        x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
        lado = max(x1 - x0, y1 - y0) + 40
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
        pad = np.zeros((img.shape[0] + 2 * lado, img.shape[1] + 2 * lado, 4), np.uint8)
        pad[lado:lado + img.shape[0], lado:lado + img.shape[1]] = img
        img = pad[cy + lado - lado // 2: cy + lado + lado // 2, cx + lado - lado // 2: cx + lado + lado // 2]
    img = cv2.resize(img, (160, 160), interpolation=cv2.INTER_AREA)
    cv2.imwrite(ruta, cv2.cvtColor(img, cv2.COLOR_RGBA2BGRA))
print("ok", len(B.ICONOS))
