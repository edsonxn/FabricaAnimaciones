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
    ("versiones", E._versiones(), 12.0, [0.5, 3.0, 6.0, 8.0], [0.3, 2.0, 4.5, 7.5, 9.0, 11.5]),
    ("inversion", E._inversion(), 22.0, [1.0, 4.0, 7.0, 10.0, 13.0, 16.0, 19.0], [0.6, 4.5, 8.0, 11.0, 14.0, 17.0, 21.0]),
    ("fragmentos A", E._fragmentos(), 9.0, [1.0, 2.0, 2.5, 3.0, 99, 99, 99], [0.3, 1.6, 2.6, 4.0, 6.0, 8.5]),
    ("fragmentos B", E._fragmentos(), 9.0, [-4, -4, -4, -4, .1, 1.5, 4.0], [0.2, 0.6, 1.2, 2.2, 4.5, 8.0]),
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
cols = 3
filas = (len(celdas) + cols - 1) // cols
hoja = Image.new("RGB", (cols * 640, filas * 360))
for k, c in enumerate(celdas):
    hoja.paste(c, ((k % cols) * 640, (k // cols) * 360))
hoja.save(os.path.join(AQUI, "previews", "prueba_mg.jpg"), quality=85)
print("ok", len(celdas))
