# -*- coding: utf-8 -*-
"""Miniatura PROVISIONAL por código con el estilo del canal (pergamino, título blanco con contorno, píldoras), hasta tener la de Flow.
Paarthurnax real (UESP) a la derecha. -> salida/miniatura.jpg (1280x720)"""
import os

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
W, H = 1280, 720
fondo = Image.open(os.path.join(AQUI, "mapas", "skyrim.jpg")).convert("RGB")
fondo = fondo.crop((0, 0, fondo.width, int(fondo.width * 9 / 16))).resize((W, H), Image.LANCZOS)
fondo = ImageEnhance.Brightness(fondo).enhance(.62)
drag = Image.open(os.path.join(AQUI, "pegatinas", "paarthurnax.png")).convert("RGB")
h = H
d_w = int(drag.width * h / drag.height)
drag = drag.resize((d_w, h), Image.LANCZOS).crop((d_w - 760, 0, d_w, h)) if d_w > 760 else drag.resize((d_w, h))
mask = Image.new("L", drag.size, 0)
dm = ImageDraw.Draw(mask)
for x in range(drag.width):
    dm.line([(x, 0), (x, h)], fill=int(255 * min(1, x / 240)))
fondo.paste(drag, (W - drag.width, 0), mask)
d = ImageDraw.Draw(fondo)
FN = "C:/Windows/Fonts/bahnschrift.ttf"
try:
    F = ImageFont.truetype(FN, 150)
    F2 = ImageFont.truetype(FN, 64)
    F3 = ImageFont.truetype(FN, 40)
    for f in (F, F2, F3):
        f.set_variation_by_name("Bold Condensed")
except OSError:
    F, F2, F3 = [ImageFont.truetype("arialbd.ttf", s) for s in (130, 58, 38)]
d.text((44, 120), "40", font=F, fill="white", stroke_width=9, stroke_fill="black")
d.text((44, 262), "SECRETOS", font=F, fill="white", stroke_width=9, stroke_fill="black")
d.rounded_rectangle((44, 440, 44 + d.textlength("QUE NADIE TE CONTÓ", font=F2) + 56, 540), 26, fill=(250, 208, 40))
d.text((72, 454), "QUE NADIE TE CONTÓ", font=F2, fill="black")
d.rounded_rectangle((44, 562, 44 + d.textlength("SKYRIM", font=F3) + 44, 628), 20, fill="black")
d.text((66, 572), "SKYRIM", font=F3, fill="white")
os.makedirs(os.path.join(AQUI, "salida"), exist_ok=True)
fondo.save(os.path.join(AQUI, "salida", "miniatura.jpg"), quality=92)
fondo.resize((640, 360)).save(os.path.join(AQUI, "previews", "miniatura_prov.jpg"), quality=85)
print("ok")
