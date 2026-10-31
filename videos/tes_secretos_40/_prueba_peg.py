# -*- coding: utf-8 -*-
"""Hoja de prueba de los estilos de nucleo/peg_estilos.py sobre un cuadro real del video -> previews/prueba_peg.jpg
    python _prueba_peg.py [fondo.jpg]"""
import os
import sys

from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))
import peg_estilos as PE  # noqa: E402

P = lambda s: os.path.join(AQUI, "pegatinas", s + ".png")
J = lambda s: os.path.join(AQUI, "pegatinas", s + ".jpg")
fondo = Image.open(sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, "previews", "_fondo.jpg")).convert("RGBA").resize((1920, 1080))
s1 = PE.silueta(P("runil_b"), "Runil", "Sacerdote de Arkay", encuadre=(0, .62), lado="izq")
s2 = PE.silueta(P("runil_b"), "Runil", "Sacerdote de Arkay", encuadre=(0, .62), lado="der")
CASOS = [
    ("silueta izq", s1, PE.pos_silueta(s1, "izq"), [2.5]),
    ("silueta der", s2, PE.pos_silueta(s2, "der"), [.25, 2.5]),
    ("reliquia", PE.reliquia(P("estrella_azura"), "Estrella de Azura"), (.74, .50), [2.0]),
    ("banda", PE.banda(J("f_delphine"), "Delphine", "Tres atentados", foco=(.3, .22, 2.4)), (.5, .50), [2.0]),
    ("camafeo", PE.camafeo(P("bolund"), "Bolund"), (.20, .68), [2.0]),
    ("legajo", PE.legajo(P("sybille"), "Sybille Stentor", ["Maga de la corte", "Detectar vida no la marca"], sello=("Vampira", 0)), (.24, .50), [2.0]),
    ("abanico", PE.abanico([(P("riekling"), "Rieklings"), (P("arvak"), "Arvak"), (P("senor_vampiro"), "Vampiros")]), (.5, .62), [2.0]),
]
celdas = []
for nombre, fn, (x, y), dts in CASOS:
    for dt in dts:
        a = fn(dt, 6.0, [1.0])
        im = Image.fromarray(a[..., [2, 1, 0, 3]], "RGBA")
        c = fondo.copy()
        px, py = int(x * 1920 - im.width / 2), int(y * 1080 - im.height / 2)
        PE._pegar(c, im, px, py)
        ImageDraw.Draw(c).text((20, 20), f"{nombre} dt={dt}", fill=(255, 255, 0, 255))
        celdas.append(c.convert("RGB").resize((640, 360)))
cols = 3
filas = (len(celdas) + cols - 1) // cols
hoja = Image.new("RGB", (cols * 640, filas * 360))
for k, c in enumerate(celdas):
    hoja.paste(c, ((k % cols) * 640, (k // cols) * 360))
hoja.save(os.path.join(AQUI, "previews", "prueba_peg.jpg"), quality=85)
print("ok", len(celdas))
