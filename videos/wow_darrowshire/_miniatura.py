# -*- coding: utf-8 -*-
"""Miniatura 1280x720 con ingredientes REALES: escenario de Flow (casa con la vela), Pamela fantasma (pieza de Flow teñida),
su modelo REAL del juego (piezas/reales/pamela) y el «!» amarillo de misión. Texto corto que complementa al título.
Uso (desde la carpeta del video): python _miniatura.py → salida/miniatura.jpg"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1280, 720
FD = os.path.expanduser("~/AppData/Local/Microsoft/Windows/Fonts") + "/"


def fuente(n, px):
    for r in (FD + n, "C:/Windows/Fonts/georgiab.ttf"):
        try:
            return ImageFont.truetype(r, px)
        except OSError:
            pass


fondo = Image.open("imagenes/casa_pamela_vela_a.jpg").convert("RGB")
fondo = fondo.resize((int(fondo.width * H / fondo.height * 1.18), int(H * 1.18)), Image.LANCZOS)
fondo = fondo.crop((fondo.width - W - 40, 60, fondo.width - 40, 60 + H))
a = np.asarray(fondo).astype(np.float32) / 255
Y, X = np.mgrid[0:H, 0:W].astype(np.float32)
vin = 1 - 0.55 * np.clip(np.hypot((X - W * 0.45) / W, (Y - H * 0.55) / H) * 1.5, 0, 1) ** 1.6
a = a * vin[..., None] * np.float32((0.85, 0.95, 1.05))
img = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).convert("RGBA")

# Pamela fantasma: la pieza de Flow teñida azul-verde, translúcida, con halo
p = Image.open("piezas/pamela_hoja/02.png").convert("RGBA")
p = p.resize((int(p.width * 560 / p.height), 560), Image.LANCZOS)
pa = np.asarray(p).astype(np.float32) / 255
g = pa[..., :3].mean(2, keepdims=True)
pa[..., :3] = np.clip((0.45 * pa[..., :3] + 0.55 * g) * np.float32((0.62, 1.05, 1.15)) + 0.08, 0, 1)
pa[..., 3] *= 0.86
fant = Image.fromarray((pa * 255).astype(np.uint8))
halo = Image.new("RGBA", fant.size, (0, 0, 0, 0))
halo.putalpha(fant.getchannel("A").filter(ImageFilter.GaussianBlur(26)).point(lambda v: int(v * 0.9)))
halo = Image.composite(Image.new("RGBA", fant.size, (110, 230, 255, 255)), halo, halo.getchannel("A"))
img.alpha_composite(halo, (90, H - 560 - 10))
img.alpha_composite(fant, (90, H - 560 - 10))

# el «!» amarillo de misión sobre su cabeza
d = ImageDraw.Draw(img)
f = fuente("Baskervville-Bold.ttf", 150)
for dx in (-5, 0, 5):
    for dy in (-5, 0, 5):
        d.text((250 + dx, 30 + dy), "!", font=f, fill=(10, 6, 2, 255))
d.text((250, 30), "!", font=f, fill=(255, 209, 0, 255))

# su modelo REAL del juego, como foto de papel
r = Image.open("piezas/reales/pamela.png").convert("RGBA")
r = r.resize((int(r.width * 330 / r.height), 330), Image.LANCZOS).rotate(6, expand=True, resample=Image.BICUBIC)
sombra = Image.new("RGBA", r.size, (0, 0, 0, 0))
sombra.putalpha(r.getchannel("A").filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.6)))
img.alpha_composite(sombra, (W - r.width - 50, H - r.height - 20))
img.alpha_composite(r, (W - r.width - 60, H - r.height - 30))

# texto: 2 palabras grandes, blanco frío con contorno negro y halo
f2 = fuente("Baskervville-Bold.ttf", 138)
txt = ["NUNCA", "VOLVIÓ"]
capa = Image.new("RGBA", img.size, (0, 0, 0, 0))
dc = ImageDraw.Draw(capa)
for k, t in enumerate(txt):
    dc.text((560, 40 + 130 * k), t, font=f2, fill=(120, 230, 255, 255))
img.alpha_composite(capa.filter(ImageFilter.GaussianBlur(14)))
d = ImageDraw.Draw(img)
for k, t in enumerate(txt):
    d.text((560, 40 + 130 * k), t, font=f2, fill=(245, 250, 255, 255), stroke_width=9, stroke_fill=(8, 6, 4, 255))
img.convert("RGB").save("salida/miniatura.jpg", quality=92)
print("salida/miniatura.jpg")
