# -*- coding: utf-8 -*-
"""Hoja de prueba de los MG nuevos de este video (cuadros a varios dt sobre fondo gris) -> previews/prueba_mg.jpg"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))
sys.path.insert(0, AQUI)
import efectos as E  # noqa: E402

CASOS = [
    ("aguante", E._aguante(), 10.0, [.5, 8.5], [0.3, 1.6, 2.2, 9.2]),
    ("esbern", E._informe_esbern(), 12.0, [1.0, 4.0, 8.0], [0.5, 2.0, 6.0, 11.0]),
    ("ulfric", E._informe_ulfric(), 14.0, [1.0, 4.0, 8.0, 11.0], [0.5, 5.0, 9.0, 13.0]),
    ("cordura", E._cordura(), 22.0, [.5, 2.5, 5.0, 8.0, 10.0, 12.0, 17.0], [1.0, 6.0, 13.0, 19.0]),
    ("nombre", E._nombre(), 9.0, [.8, 2.6, 4.0], [0.5, 1.6, 3.4, 6.0]),
]
celdas = []
for nombre, fn, dur, marcas, dts in CASOS:
    for dt in dts:
        a = fn(dt, dur, marcas)
        im = Image.fromarray(a[..., [2, 1, 0, 3]])
        fondo = Image.new("RGBA", (1920, 1080), (95, 105, 100, 255))
        if im.width > 4:
            fondo.alpha_composite(im, ((1920 - im.width) // 2, (1080 - im.height) // 2))
        ImageDraw.Draw(fondo).text((20, 20), f"{nombre} dt={dt}", fill=(255, 255, 0, 255))
        celdas.append(fondo.convert("RGB").resize((640, 360)))
cols = 4
filas = (len(celdas) + cols - 1) // cols
hoja = Image.new("RGB", (cols * 640, filas * 360))
for k, c in enumerate(celdas):
    hoja.paste(c, ((k % cols) * 640, (k // cols) * 360))
hoja.save(os.path.join(AQUI, "previews", "prueba_mg.jpg"), quality=85)
print("ok", len(celdas))
