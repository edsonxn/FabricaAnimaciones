# -*- coding: utf-8 -*-
"""Hoja de prueba de los MG nuevos de este video (previews/mg_<nombre>.jpg): cuadros en varios tiempos sobre fondo rojizo.
    python _prueba_mg.py
"""
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "nucleo"))
import mg_er as E

PRUEBAS = [
    ("cuenta", E.cuenta_atras(), [0.3, 1.0, 1.7, 2.4, 4.6], 5.5, [0.6, 1.2, 1.9, 2.9, 5.2]),
    ("recl", E.reclutamiento([("Varré", "el Rostro Alabastrado"), ("Dedo infestado", "invade tres veces"),
                              ("El paño", "sangre de doncella"), ("La medalla", "sangre pura")]),
     [0.3, 1, 1.7, 2.4, 3.2], 4.5, [0.8, 1.5, 2.9, 4.2]),
    ("dina", E.dinastia(filas=[("Dedos Sangrientos", "cazan Sinluz"), ("Caballeros", "de sangre pura"), ("Nobles sanguinos", None),
                               ("Cirujanos", "raptados"), ("Albináuricos", "con cuernos")]),
     [0.2, .8, 1.3, 1.8, 2.3, 2.8, 3.6, 4.6], 6, [1.0, 3.0, 5.5]),
]
for nom, f, mk, dur, ts in PRUEBAS:
    ims = []
    for t in ts:
        a = f(t, dur, mk)
        im = Image.fromarray(a[..., [2, 1, 0, 3]])
        bg = Image.new("RGBA", im.size, (60, 40, 40, 255))
        bg.alpha_composite(im)
        ims.append(bg.convert("RGB").resize((im.width // 2, im.height // 2)))
    out = Image.new("RGB", (sum(i.width for i in ims), ims[0].height))
    x = 0
    for i in ims:
        out.paste(i, (x, 0))
        x += i.width
    out.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "previews", f"mg_{nom}.jpg"), quality=80)
print("ok")
