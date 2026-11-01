# -*- coding: utf-8 -*-
"""Miniatura SIN SPOILER (31-oct-2026): resumen de la semana decisiva de la fase suiza. Fondo = splash de Orianna (el cuádruple de
Knight) oscurecido + los 16 escudos en dos filas, todos iguales (ni quién pasó ni quién se fue) + «SOLO 8 SIGUEN» y chip
«WORLDS 2026 · FASE SUIZA». python videos/lol_semana2/miniatura.py → miniatura/elegida.jpg"""
import os
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(D, "..", "..", "nucleo"))
import mg_lol as L  # noqa: E402

W, H = 1280, 720
AM = (255, 214, 10)
fondo = Image.open(os.path.join(D, "splash", "Orianna.jpg")).convert("RGB")
fondo = fondo.resize((W, int(fondo.height * W / fondo.width))).crop((0, 0, W, H)) if fondo.width / fondo.height < W / H else \
    fondo.resize((int(fondo.width * H / fondo.height), H))
fondo = fondo.crop(((fondo.width - W) // 2, 0, (fondo.width - W) // 2 + W, H))
fondo = ImageEnhance.Brightness(ImageEnhance.Color(fondo).enhance(.85)).enhance(.7).convert("RGBA")
# oscuro arriba (título) y abajo (escudos), la cara de Orianna al centro-derecha queda viva
capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(capa)
for y in range(H):
    a = 200 if y < 60 else max(0, int(200 - (y - 60) * 1.4)) if y < 300 else 0
    if y > 430:
        a = min(235, int((y - 430) * 1.6))
    d.line([(0, y), (W, y)], fill=(6, 8, 16, a))
im = Image.alpha_composite(fondo, capa)
d = ImageDraw.Draw(im)

# título
ft = L.fuente("Bold Condensed", 176)
for txt, y, col in (("SOLO 8", 128, (255, 255, 255)), ("SIGUEN", 290, AM)):
    d.text((60 + 7, y + 7), txt, font=ft, fill=(0, 0, 0), anchor="lm")
    d.text((60, y), txt, font=ft, fill=col, anchor="lm", stroke_width=5, stroke_fill=(0, 0, 0))
# chip
fc = L.fuente("Bold Condensed", 42)
d.rounded_rectangle((64, 392, 470, 448), 14, fill=(18, 22, 36, 235), outline=AM, width=3)
d.text((267, 420), "WORLDS 2026 · FASE SUIZA", font=fc, fill=(255, 255, 255), anchor="mm")

# 16 escudos en dos filas de 8, todos iguales
EQ = ["T1", "HLE", "GEN", "G2", "BLG", "LOS", "TES", "AL", "KC", "MKOI", "DK", "CFO", "LYON", "TSW", "IG", "TLAW"]    # mezclados: 4 y 4 por fila
lado, gap = 100, 40
x0 = (W - (8 * lado + 7 * gap)) // 2
for i, e in enumerate(EQ):
    x, y = x0 + (i % 8) * (lado + gap), 478 + (i // 8) * (lado + 16)
    d.rounded_rectangle((x - 6, y - 6, x + lado + 6, y + lado + 6), 18, fill=(14, 18, 30, 230), outline=(70, 80, 110), width=2)
    lg = Image.open(os.path.join(D, "iconos", "equipos", e + ".png")).convert("RGBA")
    lg.thumbnail((lado - 14, lado - 14))
    im.alpha_composite(lg, (x + (lado - lg.width) // 2, y + (lado - lg.height) // 2))

os.makedirs(os.path.join(D, "miniatura"), exist_ok=True)
im.convert("RGB").save(os.path.join(D, "miniatura", "elegida.jpg"), quality=92)
im.convert("RGB").resize((640, 360)).save(os.path.join(D, "previews", "miniatura_640.jpg"), quality=85)
print("miniatura/elegida.jpg")
