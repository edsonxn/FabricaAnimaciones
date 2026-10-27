# -*- coding: utf-8 -*-
"""mapas/<zona>_rejilla.jpg: cuadrícula cada 5 % (rótulos cada 10 %) + los puntos de PUNTOS en rojo, para leer coordenadas
de zona (las de Wowpedia = fracción del mapa de Wowhead). python _rejilla.py [zona ...]"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
F = ImageFont.truetype("arial.ttf", 13)
FB = ImageFont.truetype("arialbd.ttf", 14)

# zona -> [(x%, y%, rótulo)]  (Wowpedia {{coords}}; los «?» son estimados a ojo)
PUNTOS = {
    "boreal": [(42, 53, "Grito de Guerra"), (57, 44, "DEHTA"), (57, 18, "Palanqueta"), (65, 23.5, "Bombeo Palanqueta"),
               (33, 35, "Escudo Transito"), (45, 33, "Saliente Ambar"), (77, 35, "Taunka'le")],
    "fiordo": [(67, 53, "Nafsavar")],
    "dragones": [(87, 51, "Naxxramas"), (78, 46, "Hibergarde"), (87.2, 57.4, "Orik"), (73, 23, "Caverna Agonia"),
                 (71, 75, "Nueva Vega"), (38, 31, "Sant. Obsidiana")],
    "pardas": [(51.3, 42.5, "Fauceparda"), (38.5, 52.5, "Corazon Vordrassil"), (52.1, 23.4, "Guarida Ursoc"),
               (59, 27, "Brigada"), (26.3, 37.6, "Arroyoplata"), (82.6, 30, "Isla Luna Sangre"), (72.6, 24.6, "Drakil'jin")],
    "zuldrak": [(63.6, 70, "Har'koa"), (53.4, 36.8, "Rhunok"), (40.3, 39.8, "Sseratus"), (74.7, 43, "Mam'toth"),
                (47.3, 57.1, "Anfiteatro"), (31.9, 75.1, "Brecha de Luz")],
    "sholazar": [(65, 49, "Avatar Freya"), (28, 39, "Pedestal Creadores"), (53.6, 56.6, "Dosel Oraculos")],
    "cumbres": [(40.6, 85.6, "K3"), (48.2, 69.2, "Brunnhildar"), (29, 73, "Fuerte Escarcha"), (42.2, 24.8, "Ulduar"),
                (31, 69, "PPT"), (51, 70, "PPT"), (35, 76, "PPT"), (52, 34, "PPT")],
    "canto_cristal": [(74, 79, "Mirador Brisaveloz"), (78, 49, "Atalaya Atracasol")],
    "invierno": [(50.5, 20.5, "Fortaleza")],
    "corona": [(9, 41, "Puerto Embate"), (79.7, 72.3, "Pinaculo"), (79, 30, "Bridenbrad")],
    "rasganorte": [],
}


def hacer(zona):
    im = Image.open(os.path.join(AQUI, "mapas", zona + ".jpg")).convert("RGB")
    W, H = im.size
    d = ImageDraw.Draw(im)
    for k in range(1, 20):
        a = (255, 255, 255) if k % 2 == 0 else (150, 150, 150)
        x, y = W * k / 20, H * k / 20
        d.line([(x, 0), (x, H)], fill=a, width=1)
        d.line([(0, y), (W, y)], fill=a, width=1)
        if k % 2 == 0:
            d.text((x + 2, 2), str(k * 5), font=F, fill=(255, 255, 0))
            d.text((2, y + 1), str(k * 5), font=F, fill=(255, 255, 0))
    for x, y, r in PUNTOS.get(zona, []):
        px, py = W * x / 100, H * y / 100
        d.ellipse((px - 5, py - 5, px + 5, py + 5), fill=(255, 30, 30), outline=(0, 0, 0))
        d.text((px + 7, py - 8), r, font=FB, fill=(255, 60, 60), stroke_width=2, stroke_fill=(0, 0, 0))
    im.save(os.path.join(AQUI, "mapas", zona + "_rejilla.jpg"), quality=88)


if __name__ == "__main__":
    for z in sys.argv[1:] or PUNTOS:
        hacer(z)
        print("ok", z)
