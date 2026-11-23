# -*- coding: utf-8 -*-
"""Hoja previews/pegatinas_check.jpg (regla del 6-nov-2026): CADA imagen que usa efectos.py (pegatinas, iconos de fichas, fotos de
mapa, pantallas) con la frase de la voz que la llama debajo, para mirarla a mano antes del render.
    python _peg_check.py
"""
import os
import re

from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(AQUI, "efectos.py"), encoding="utf-8").read()
cuerpo = src[src.index("FX = ["):]
entradas = re.split(r"\n    (?=[a-z*#])", cuerpo)
filas = []
for e in entradas:
    if e.lstrip().startswith("#"):
        continue
    strs = re.findall(r'"([^"]*)"', e)
    if not strs:
        continue
    ancla = strs[0]
    for s in strs:
        for carpeta, ext in (("pegatinas", ".png"), ("pantallas", ".jpg")):
            for cand in (s, s.replace("com_", "com_")):
                r = os.path.join(AQUI, carpeta, cand + ext)
                if os.path.exists(r) and not cand.startswith("com_") and (r, ancla) not in filas:
                    filas.append((r, ancla))
    for cid in re.findall(r"C_[A-Z]+", e):
        pass
W, H, COLS = 300, 230, 8
f = ImageFont.truetype("arial.ttf", 15)
hoja = Image.new("RGB", (W * COLS, H * ((len(filas) + COLS - 1) // COLS)), (30, 30, 30))
for i, (r, a) in enumerate(filas):
    im = Image.open(r).convert("RGBA")
    im.thumbnail((W - 10, H - 60))
    bg = Image.new("RGBA", im.size, (70, 70, 70, 255))
    bg.alpha_composite(im)
    x, y = (i % COLS) * W, (i // COLS) * H
    hoja.paste(bg.convert("RGB"), (x + 5, y + 4))
    d = ImageDraw.Draw(hoja)
    d.text((x + 5, y + H - 54), os.path.basename(r), font=f, fill=(255, 220, 0))
    txt = a[:76]
    d.text((x + 5, y + H - 36), txt[:38], font=f, fill=(230, 230, 230))
    d.text((x + 5, y + H - 18), txt[38:], font=f, fill=(230, 230, 230))
hoja.save(os.path.join(AQUI, "previews", "pegatinas_check.jpg"), quality=80)
print(len(filas), "imágenes en previews/pegatinas_check.jpg")
