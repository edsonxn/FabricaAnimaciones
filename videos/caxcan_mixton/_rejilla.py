# -*- coding: utf-8 -*-
"""Rejilla 10x10 sobre escenarios para colocar piezas: python _rejilla.py salida.jpg fondo1 fondo2 ... (2 columnas)."""
import sys
from PIL import Image, ImageDraw
out, fs = sys.argv[1], sys.argv[2:]
w, h = 760, 424
im = Image.new("RGB", (2 * w, ((len(fs) + 1) // 2) * (h + 18)), "black")
d = ImageDraw.Draw(im)
for k, f in enumerate(fs):
    x0, y0 = (k % 2) * w, (k // 2) * (h + 18)
    t = Image.open(f"imagenes/{f}.jpg").convert("RGB").resize((w, h))
    dt = ImageDraw.Draw(t)
    for i in range(1, 10):
        dt.line([(i * w / 10, 0), (i * w / 10, h)], fill=(255, 0, 0), width=1)
        dt.line([(0, i * h / 10), (w, i * h / 10)], fill=(255, 0, 0), width=1)
        dt.text((i * w / 10 + 2, 2), str(i), fill="yellow"); dt.text((2, i * h / 10 + 1), str(i), fill="yellow")
    im.paste(t, (x0, y0 + 18)); d.text((x0 + 4, y0 + 3), f, fill="white")
im.save(out, quality=80)
