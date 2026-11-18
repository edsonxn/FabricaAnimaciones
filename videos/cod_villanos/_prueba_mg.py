# -*- coding: utf-8 -*-
"""Hoja de prueba de los MG nuevos (C.acta, C.bajas): previews/mg_prueba.jpg."""
import os, sys
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.join("..", "..", "nucleo"))
import mg_cod as C
P = lambda s: next(os.path.join("pegatinas", s + e) for e in (".png", ".jpg", ".webp") if os.path.exists(os.path.join("pegatinas", s + e)))
fondo = Image.open(P("c_mw3")).convert("RGB").resize((1920, 1080))
acta = C.acta("Vladimir Makarov", P("makarov"), [("CAUSA", "Ahorcado con un cable"), ("AUTOR", "John Price"),
              ("LUGAR", "Hotel Oasis, Dubái · 2017"), ("MISIÓN", "Polvo al polvo · MW3")], "confirmado", "Price enciende un puro")
acta2 = C.acta("Gabriel Rorke", P("rorke"), [("DISPARO", "Magnum .44, una sola bala"), ("AUTOR", "Logan Walker")], "sobrevivio", "Nunca hubo Ghosts 2")
sag = [("MODERN WARFARE", [(P(s), n) for s, n in [("zakhaev", "Zakhaev"), ("alasad", "Al-Asad"), ("victor", "Victor"), ("shepherd", "Shepherd"), ("makarov", "Makarov")]]),
       ("BLACK OPS", [(P(s), n) for s, n in [("dragovich", "Dragovich"), ("kravchenko", "Kravchenko"), ("steiner", "Steiner"), ("menendez", "Menéndez"), ("harrow", "Harrow"), ("perseus", "Perseus")]]),
       ("REINICIO MW", [(P(s), n) for s, n in [("wolf", "El Lobo"), ("barkov", "Barkov"), ("hassan", "Hassan"), ("graves", "Graves"), ("makarov_r", "Makarov")]]),
       ("OTROS", [(P(s), n) for s, n in [("amsel", "Amsel"), ("rorke", "Rorke"), ("irons", "Irons"), ("kotch", "Kotch"), ("richtofen", "Richtofen")]])]
baj = C.bajas(sag, tachados=("Amsel", "Al-Asad"), foco="Victor", titulo="20 villanos · 20 expedientes")
cuadros = [(acta, 1.0, [.5, 1.1, 1.7, 2.3, 3.0]), (acta, 4.0, [.5, 1.1, 1.7, 2.3, 3.0]), (acta2, 3.5, [.5, 1.2, 2.0]),
           (baj, .4, [1.2]), (baj, 1.3, [1.2]), (baj, 2.5, [1.2])]
hoja = Image.new("RGB", (1920, 1080 * 3 // 2), (0, 0, 0))
for i, (fn, t, mk) in enumerate(cuadros):
    a = fn(t, 6.0, mk)
    im = Image.fromarray(a[..., [2, 1, 0, 3]], "RGBA")
    c = fondo.copy()
    if im.width > 1920 or im.height > 1080:
        im.thumbnail((1900, 1060))
    c.paste(im, ((1920 - im.width) // 2, (1080 - im.height) // 2), im)
    hoja.paste(c.resize((960, 540)), ((i % 2) * 960, (i // 2) * 540))
hoja.save("previews/mg_prueba.jpg", quality=85)
print("ok")
