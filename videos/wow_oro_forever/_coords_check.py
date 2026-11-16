# -*- coding: utf-8 -*-
"""Hoja de comprobación de _coords.md: cada punto dibujado sobre su mapa (1 % = coordenada del juego). python _coords_check.py → previews/_coords_check.jpg"""
import os
from PIL import Image, ImageDraw
D = os.path.dirname(os.path.abspath(__file__))
PTS = {  # mapa: [(x, y, rótulo)]  — mismos valores que _coords.md
    "elwynn": [(84.2, 65.0, "Randal Hunter"), (41.5, 68.9, "Gelvas (Villadorada)")],
    "orgrimmar": [(69.2, 13.2, "Kildar")],
    "baldios": [(62.6, 35.5, "Strahad (Trinquete)"), (57.5, 27.2, "Chol'aruk"), (50.0, 29.2, "Dokimi")],
    "mulgore": [(37.2, 37.8, "Gelvas (Mulgore)")],
    "desolace": [(20.0, 80.7, "Trampas de marisco"), (40.5, 79.2, "Supervendedor 680")],
    "arathi": [(25.2, 30.6, "Exiliado ardiente"), (51.4, 50.6, "Exiliado del trueno"), (66.6, 29.8, "Exiliado blasonado")],
    "tuercespina": [(25.9, 26.6, "Almejas (Arrecife Vil)"), (27.4, 77.0, "Viejo Heming"), (32.5, 29.0, "Grom'gol (ref)")],
    "tanaris_eses": [(52.6, 28.0, "Dirge"), (50.1, 30.6, "Rocs"), (46.6, 41.4, "Rocs de fuego"), (54.1, 93.1, "Planeadores (sur)"), (68.5, 57.2, "Planeadores (este)")],
    "feralas_eses": [(55.3, 68.0, "Frayfeather")],
    "crestagrana": [(9.5, 71.0, "Marcy Baker")],
    "marjal_eses": [(58.5, 60.0, "Nat Pagle")],
    "frondavil_eses": [(41.7, 85.0, "Jadefire (Claro)"), (35.8, 66.6, "Jadefire (Bastión)"), (42.4, 17.4, "Jadefire (Paso)")],
    "azshara": [(56.4, 20.6, "Legashi"), (66.0, 17.5, "Legashi (este)")],
    "estepas": [(47.3, 33.4, "torio"), (30.3, 58.6, "torio"), (54.4, 60.1, "torio"), (61.0, 38.5, "torio"), (72.4, 29.8, "torio")],
}
minis = []
for m, pts in PTS.items():
    im = Image.open(os.path.join(D, "mapas", m + ".jpg")).convert("RGB")
    W, H = im.size
    d = ImageDraw.Draw(im)
    for x, y, r in pts:
        px, py = x / 100 * W, y / 100 * H
        d.ellipse((px - 7, py - 7, px + 7, py + 7), outline=(255, 0, 0), width=3)
        d.text((px + 9, py - 6), r, fill=(255, 255, 0), stroke_width=2, stroke_fill=(0, 0, 0))
    d.text((8, H - 20), m, fill=(0, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))
    minis.append(im.resize((640, 427)))
col = 3
h = Image.new("RGB", (col * 640, ((len(minis) + col - 1) // col) * 427))
for i, mi in enumerate(minis):
    h.paste(mi, ((i % col) * 640, (i // col) * 427))
os.makedirs(os.path.join(D, "previews"), exist_ok=True)
h.save(os.path.join(D, "previews", "_coords_check.jpg"), quality=85)
for k in range(0, len(minis), 6):  # trozos para mirarlos grandes
    g = Image.new("RGB", (2 * 640, 3 * 427))
    for i, mi in enumerate(minis[k:k + 6]):
        g.paste(mi, ((i % 2) * 640, (i // 2) * 427))
    g.save(os.path.join(D, "previews", f"_coords_check_{k // 6 + 1}.jpg"), quality=85)
print(len(minis))
