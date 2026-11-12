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
    ("voto", E.votacion(), [0.3, 2.0, 3.5, 7.0], 9, [1.0, 2.6, 4.6, 6.2, 8.0]),
    ("injerto", E.injerto(miembros=[("Hombres de Roderika", "brazos, piernas, cabezas"), ("Halcones de guerra", "sin garras"),
                                    ("Un dragón muerto", "su propio brazo"), ("Tú", "la siguiente rama")],
                          remate="Todo lo que pierde, lo cose de otro"),
     [0.3, 1.2, 2.1, 3.0, 4.2], 5.5, [0.8, 1.6, 2.6, 3.6, 5.0]),
    ("linaje", E.linaje(), [0.2, .8, 2.0, 3.0, 4.2], 5.5, [0.6, 1.5, 2.6, 3.6, 5.0]),
]
for nom, f, mk, dur, ts in PRUEBAS:
    ims = []
    for t in ts:
        a = f(t, dur, mk)
        im = Image.fromarray(a[..., [2, 1, 0, 3]])
        bg = Image.new("RGBA", im.size, (60, 40, 40, 255))
        bg.alpha_composite(im)
        ims.append(bg.convert("RGB").resize((im.width // 3, im.height // 3)))
    out = Image.new("RGB", (sum(i.width for i in ims), ims[0].height))
    x = 0
    for i in ims:
        out.paste(i, (x, 0))
        x += i.width
    out.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "previews", f"mg_{nom}.jpg"), quality=80)
print("ok")
