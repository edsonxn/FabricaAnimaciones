# -*- coding: utf-8 -*-
"""Miniatura PROVISIONAL por código (30-oct-2026): la de Flow quedó pendiente porque Flow pide aceptar su política de privacidad en el
navegador integrado y esa aceptación es del usuario. Cuadros reales del juego + pegatinas reales; misma familia del canal
(texto blanco con contorno negro + píldora roja). Sale salida/miniatura.jpg (1280x720).
    python miniatura_provisional.py
"""
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
W, H = 1280, 720


def cuadro(n, s):
    cap = cv2.VideoCapture(os.path.join(AQUI, "medios", f"scene-{n:03d}.mp4"))
    cap.set(cv2.CAP_PROP_POS_MSEC, s * 1000)
    ok, fr = cap.read()
    return Image.fromarray(cv2.cvtColor(fr, cv2.COLOR_BGR2RGB)).resize((W, H), Image.LANCZOS)


def peg(slug, alto):
    im = Image.open(os.path.join(AQUI, "pegatinas", slug + ".png")).convert("RGBA")
    im = im.crop(im.getbbox())
    e = alto / im.height
    return im.resize((int(im.width * e), alto), Image.LANCZOS)


lava, hielo = cuadro(143, 3.0), cuadro(162, 2.0)
# mitad fuego, mitad hielo: el número 1 del ranking, con corte diagonal
m = Image.new("L", (W, H), 0)
ImageDraw.Draw(m).polygon([(760, 0), (W, 0), (W, H), (480, H)], fill=255)
base = Image.composite(hielo, lava, m.filter(ImageFilter.GaussianBlur(3)))
base = Image.eval(base, lambda v: min(255, int(v * 1.08)))
sombra = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(sombra).rectangle((0, 0, 720, H), fill=(0, 0, 0, 110))
sombra = sombra.filter(ImageFilter.GaussianBlur(70))
im = base.convert("RGBA")
im.alpha_composite(sombra)

for slug, alto, x, y in (("banjo", 500, 760, 210), ("kazooie", 300, 1020, 60)):
    p = peg(slug, alto)
    s = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    s.paste((0, 0, 0, 170), (x + 10, y + 12), p)
    im.alpha_composite(s.filter(ImageFilter.GaussianBlur(10)))
    im.alpha_composite(p, (x, y))
j = peg("jiggy", 190)
im.alpha_composite(j, (60, 500))

d = ImageDraw.Draw(im)
f1 = ImageFont.truetype("C:/Windows/Fonts/COOPBL.TTF", 150)
f2 = ImageFont.truetype("C:/Windows/Fonts/COOPBL.TTF", 76)
f3 = ImageFont.truetype("C:/Windows/Fonts/COOPBL.TTF", 96)
for i, t in enumerate(("8", "MUNDOS")):
    d.text((46, 28 + 150 * i), t, font=f1, fill="white", stroke_width=11, stroke_fill="black")
d.rounded_rectangle((42, 352, 700, 470), 26, fill=(214, 28, 28), outline="black", width=6)
d.text((371, 411), "PEOR A MEJOR", font=f2, fill="white", anchor="mm", stroke_width=4, stroke_fill="black")
d.text((155, 590), "1", font=f3, fill=(214, 28, 28), anchor="mm", stroke_width=6, stroke_fill="white")
os.makedirs(os.path.join(AQUI, "salida"), exist_ok=True)
im.convert("RGB").save(os.path.join(AQUI, "salida", "miniatura.jpg"), quality=92)
im.convert("RGB").resize((320, 180), Image.LANCZOS).save(os.path.join(AQUI, "previews", "miniatura_chica.jpg"), quality=88)
