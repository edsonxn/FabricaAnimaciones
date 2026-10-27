# -*- coding: utf-8 -*-
"""Hoja de prueba de los MG nuevos de Rasganorte (previews/mg_<nombre>.jpg, 3x2 cuadros sobre gris)."""
import os
import sys

import numpy as np
from PIL import Image

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [os.getcwd(), r"C:\FabricaAnimaciones\nucleo"]
import mg_wow as M  # noqa: E402
from efectos import P  # noqa: E402

PRUEBAS = {
    "altares": (M.altares("LOS DIOSES QUE SE COMIERON", [
        (P("rhunok"), "Rhunok", "el oso", False), (P("quetzlun"), "Quetz'lun", "la serpiente alada", False),
        (P("sseratus"), "Sseratus", None, False), (P("akali"), "Akali", "el rinoceronte", False),
        (P("harkoa"), "Har'koa", "la leopardo de las nieves", True)], sello=("SE COMIERON A SUS DIOSES", 5)),
        [0, 1.5, 3.0, 3.8, 7.0, 12.0], [.3, 1.2, 2.6, 4.6, 8.0, 13.0]),
    "apariciones": (M.apariciones(P("harrison"), "LAS APARICIONES DE HARRISON JONES", [
        ("Zul'Aman", "Burning Crusade"), ("Colinas Pardas", "Wrath of the Lich King"), ("Uldum", "Cataclysm"), ("Draenor", None)],
        actual=1, sello=("EN CADA EXPANSIÓN", 4)), [.1, 1.0, 4.0, 7.5, 9.0], [.5, 1.4, 3.0, 4.5, 8.0, 10.0]),
}

for nom, (fn, marcas, ts) in PRUEBAS.items():
    cuadros = []
    for t in ts:
        a = fn(t, 14.0, marcas)
        im = Image.new("RGB", (1920, 1080), (70, 80, 70))
        if a.shape[0] > 2:
            rgba = Image.fromarray(a[..., [2, 1, 0, 3]])
            im.paste(rgba, ((1920 - rgba.width) // 2, (1080 - rgba.height) // 2), rgba)
        cuadros.append(im.resize((640, 360)))
    hoja = Image.new("RGB", (1920, 720))
    for k, c in enumerate(cuadros):
        hoja.paste(c, ((k % 3) * 640, (k // 3) * 360))
    hoja.save(f"previews/mg_{nom}.jpg", quality=85)
    print(f"previews/mg_{nom}.jpg")
