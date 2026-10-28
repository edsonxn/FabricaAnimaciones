# -*- coding: utf-8 -*-
"""Hojas de prueba de los MG nuevos de este video (previews/mg_<nombre>.jpg): cuadros a varios dt sobre fondo gris.
    python _prueba_mg.py"""
import os
import sys

import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))
sys.path.insert(0, AQUI)
import efectos as E   # noqa: E402  (los MG con los datos del guion)


def hoja(nombre, fn, marcas, tiempos, dur=20.0):
    cuadros = []
    for t in tiempos:
        a = fn(t, dur, marcas)
        im = Image.fromarray(a[..., [2, 1, 0, 3]])
        lien = Image.new("RGBA", (1920, 1080), (95, 105, 100, 255))
        lien.alpha_composite(im, ((1920 - im.width) // 2, (1080 - im.height) // 2))
        lien = lien.convert("RGB").resize((640, 360))
        cuadros.append(lien)
    col = 3
    filas = (len(cuadros) + col - 1) // col
    h = Image.new("RGB", (640 * col, 360 * filas), (0, 0, 0))
    for i, c in enumerate(cuadros):
        h.paste(c, ((i % col) * 640, (i // col) * 360))
    h.save(os.path.join(AQUI, "previews", f"mg_{nombre}.jpg"), quality=85)
    print("previews/mg_%s.jpg" % nombre)


if __name__ == "__main__":
    for nombre, fn, marcas, tiempos in E.PRUEBAS:
        hoja(nombre, fn, marcas, tiempos)
