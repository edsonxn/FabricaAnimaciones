# -*- coding: utf-8 -*-
"""Miniatura SIN SPOILER (29-oct-2026): el estadio con la copa de la previa (videos/cfo_kc_worlds/miniatura/elegida.jpg, Flow con
CFO vs KC) + el lenguaje del análisis: telestrador (anillo y flecha amarillos sobre la copa), chip «⏸ PAUSA» y «LAS JUGADAS CLAVE»
abajo. Ni el marcador ni quién ganó. python videos/cfo_kc_jugadas/miniatura.py → miniatura/elegida.jpg"""
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(D, "..", "..", "nucleo"))
import mg_lol as L  # noqa: E402

im = Image.open(os.path.join(D, "..", "cfo_kc_worlds", "miniatura", "elegida.jpg")).convert("RGBA").resize((1280, 720))
W, H = im.size
# banda inferior oscura para tapar «¿QUIÉN SE VA?»
banda = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(banda)
for y in range(470, H):
    a = min(255, int(255 * (y - 470) / 70))
    d.line([(0, y), (W, y)], fill=(6, 8, 16, a))
im = Image.alpha_composite(im, banda)
# telestrador: anillo + flecha amarilla hacia la copa
tel = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(tel)
AM = (255, 214, 10, 255)
d.ellipse((520, 250, 760, 470), outline=AM, width=12)
d.line([(250, 420), (500, 380)], fill=AM, width=14)
d.polygon([(530, 374), (488, 352), (498, 404)], fill=AM)
brillo = tel.filter(ImageFilter.GaussianBlur(10))
im = Image.alpha_composite(Image.alpha_composite(im, brillo), tel)
d = ImageDraw.Draw(im)
# chip PAUSA
f = L.fuente("Bold Condensed", 54)
d.rounded_rectangle((70, 330, 290, 410), 16, fill=(255, 214, 10, 255))
d.rectangle((96, 350, 108, 392), fill=(10, 12, 20))
d.rectangle((118, 350, 130, 392), fill=(10, 12, 20))
d.text((206, 371), "PAUSA", font=f, fill=(10, 12, 20), anchor="mm")
# título abajo
ft = L.fuente("Bold Condensed", 150)
for dx, dy in ((6, 6), (0, 0)):
    d.text((W / 2 + dx, 615 + dy), "LAS JUGADAS CLAVE", font=ft, fill=(0, 0, 0) if dx else (255, 214, 10), anchor="mm",
           stroke_width=6 if not dx else 0, stroke_fill=(0, 0, 0))
os.makedirs(os.path.join(D, "miniatura"), exist_ok=True)
im.convert("RGB").save(os.path.join(D, "miniatura", "elegida.jpg"), quality=92)
im.convert("RGB").resize((640, 360)).save(os.path.join(D, "previews", "miniatura_640.jpg"), quality=85)
print("miniatura/elegida.jpg")
