# -*- coding: utf-8 -*-
"""Miniatura 1280x720 (receta de wow_darrowshire/_miniatura.py): escenario de Flow (la Capilla con la espada clavada), el padre
caballero de la muerte (pieza de Flow) con su fantasma detrás, el hijo que lo apuñala y la Crematoria REAL del juego en foto de
papel. Texto corto que complementa al título. Uso (desde la carpeta del video): python _miniatura.py → salida/miniatura.jpg"""
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


def pieza(ruta, alto, tono=None, op=1.0):
    p = Image.open(ruta).convert("RGBA")
    p = p.resize((int(p.width * alto / p.height), alto), Image.LANCZOS)
    if tono is not None or op < 1:
        a = np.asarray(p).astype(np.float32) / 255
        if tono is not None:
            g = a[..., :3].mean(2, keepdims=True)
            a[..., :3] = np.clip((0.45 * a[..., :3] + 0.55 * g) * np.float32(tono) + 0.06, 0, 1)
        a[..., 3] *= op
        p = Image.fromarray((a * 255).astype(np.uint8))
    return p


def halo(img, p, xy, color, r=26, k=0.9):
    h = Image.new("RGBA", p.size, (0, 0, 0, 0))
    h.putalpha(p.getchannel("A").filter(ImageFilter.GaussianBlur(r)).point(lambda v: int(v * k)))
    h = Image.composite(Image.new("RGBA", p.size, color + (255,)), h, h.getchannel("A"))
    img.alpha_composite(h, xy)


fondo = Image.open("imagenes/e02_capilla_espada_b.jpg").convert("RGB")
fondo = fondo.resize((int(fondo.width * H / fondo.height * 1.12), int(H * 1.12)), Image.LANCZOS)
fondo = fondo.crop((40, 30, 40 + W, 30 + H))
a = np.asarray(fondo).astype(np.float32) / 255
Y, X = np.mgrid[0:H, 0:W].astype(np.float32)
vin = 1 - 0.6 * np.clip(np.hypot((X - W * 0.4) / W, (Y - H * 0.55) / H) * 1.5, 0, 1) ** 1.6
a = a * vin[..., None] * np.float32((0.80, 0.92, 1.0))
img = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).convert("RGBA")

# el espíritu del padre (fantasma) detrás, enorme
fant = pieza("piezas/h02_alexandros_dk/03.png", 640, tono=(0.62, 1.05, 1.15), op=0.75)
halo(img, fant, (-30, 40), (110, 230, 255))
img.alpha_composite(fant, (-30, 40))
# el padre caído de rodillas y el hijo con la espada alzada
padre = pieza("piezas/h01_alexandros_hoja/03.png", 380)
img.alpha_composite(padre, (200, H - padre.height - 10))
hijo = pieza("piezas/h03_renault_hoja/03.png", 470)
halo(img, hijo, (430, H - hijo.height - 10), (90, 255, 120), r=20, k=0.7)
img.alpha_composite(hijo, (430, H - hijo.height - 10))

# la Crematoria corrupta REAL del juego, como foto de papel
r = Image.open("piezas/reales/crematoria_corrupta.png").convert("RGBA")
r = r.resize((420, int(r.height * 420 / r.width)), Image.LANCZOS).rotate(-8, expand=True, resample=Image.BICUBIC)
sombra = Image.new("RGBA", r.size, (0, 0, 0, 0))
sombra.putalpha(r.getchannel("A").filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.6)))
img.alpha_composite(sombra, (W - r.width - 40, H - r.height - 20))
img.alpha_composite(r, (W - r.width - 50, H - r.height - 30))

# texto: corto, grande, blanco con contorno y halo verde
f2 = fuente("Baskervville-Bold.ttf", 108)
txt = ["SU PROPIO", "HIJO"]
capa = Image.new("RGBA", img.size, (0, 0, 0, 0))
dc = ImageDraw.Draw(capa)
for k, t in enumerate(txt):
    dc.text((640, 36 + 106 * k), t, font=f2, fill=(110, 255, 140, 255))
img.alpha_composite(capa.filter(ImageFilter.GaussianBlur(16)))
d = ImageDraw.Draw(img)
for k, t in enumerate(txt):
    d.text((640, 36 + 106 * k), t, font=f2, fill=(245, 250, 255, 255), stroke_width=9, stroke_fill=(8, 6, 4, 255))
os.makedirs("salida", exist_ok=True)
img.convert("RGB").save("salida/miniatura.jpg", quality=92)
print("salida/miniatura.jpg")
