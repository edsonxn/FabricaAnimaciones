# -*- coding: utf-8 -*-
"""Hoja de identidad de pegatinas: previews/pegatinas_check.jpg (cada imagen con su slug y, si se pasa, la frase de la voz)."""
import os, sys, math
from PIL import Image, ImageDraw, ImageFont
P = "pegatinas"
fs = sorted(f for f in os.listdir(P) if not f.startswith("_") and f.lower().endswith((".png", ".jpg", ".webp")))
if len(sys.argv) > 1:
    fs = [f for f in fs if os.path.splitext(f)[0] in sys.argv[1:]]
C, T = 8, 200
filas = math.ceil(len(fs) / C)
hoja = Image.new("RGB", (C * T, filas * (T + 40)), (30, 30, 30))
d = ImageDraw.Draw(hoja)
f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 15)
for i, n in enumerate(fs):
    im = Image.open(os.path.join(P, n)).convert("RGBA")
    w, h = im.size
    im.thumbnail((T - 8, T - 8))
    x, y = (i % C) * T, (i // C) * (T + 40)
    hoja.paste(im, (x + 4, y + 4), im)
    d.text((x + 4, y + T + 2), f"{os.path.splitext(n)[0]} {w}x{h}", fill=(255, 220, 80), font=f)
os.makedirs("previews", exist_ok=True)
hoja.save("previews/pegatinas_check.jpg", quality=85)
print(len(fs), "imagenes")
