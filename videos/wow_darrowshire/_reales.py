# -*- coding: utf-8 -*-
"""Pegatinas REALES de World of Warcraft (Wowpedia, `pegatinas/_orig/`) para el estilo pegatina Flow:
  piezas/reales/<slug>.png   foto del juego en un marco de papel crema (borde y sombra los pone pegaflow.actor)
  piezas/medallon/<slug>.png retrato oval con filete de tinta (árbol de la familia Rutagrana)
Uso (desde la carpeta del video): python _reales.py"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SRC = "pegatinas/_orig"
PAPEL = (240, 232, 214)
TINTA = (40, 30, 24)

# slug: (recorte x0, y0, x1, y1 en fracciones, alto de salida)
FOTOS = {
    "pamela": ((0, 0, 1, 1), 620), "pamela_muneca": ((0.45, 0.0, 1.0, 1.0), 620), "muneca": ((0.1, 0.05, 0.9, 0.95), 520),
    "joseph": ((0, 0, 1, 1), 680), "joseph_cos": ((0.0, 0.0, 1.0, 1.0), 520), "marlene_cos": ((0, 0, 1, 0.75), 620),
    "marlene": ((0, 0, 1, 1), 680), "carlin": ((0, 0, 1, 0.8), 620), "jessica": ((0, 0, 1, 1), 600),
    "davil": ((0, 0, 1, 1), 680), "horgus": ((0, 0, 1, 1), 680), "marduk": ((0, 0, 1, 1), 640),
    "rutagrana_corrompido": ((0, 0, 1, 1), 680), "villa_darrow": ((0, 0, 1, 1), 520), "ghoul": ((0.1, 0, 0.95, 1), 600),
    "skeleton": ((0, 0, 1, 1), 620), "mano_plata": ((0, 0, 1, 1), 360), "andorhal": ((0, 0, 1, 1), 520),
    "batalla": ((0, 0, 1, 1), 680), "escudo": ((0, 0, 1, 1), 480), "espiritu": ((0, 0, 1, 1), 620),
    "cromi": ((0.0, 0.0, 1.0, 1.0), 620), "cromi_dragon": ((0.0, 0.05, 1.0, 1.0), 620),
}
# iconos REALES de objetos de misión (Wowhead, 56 px) → piezas/iconos/<slug>.png con marco de icono de WoW
ICONOS = {"muneca": "inv_misc_idol_02", "muneca_cabeza": "inv_misc_head_gnome_01", "muneca_lado": "inv_misc_idol_01",
          "anillo": "inv_jewelry_ring_03", "anales": "inv_misc_book_07"}
# medallones: recorte de la CARA (fracciones) → óvalo
MEDALLON = {
    "joseph": (0.22, 0.03, 0.80, 0.30), "pamela": (0.18, 0.10, 0.82, 0.42), "jessica": (0.12, 0.05, 0.88, 0.32),
    "marlene_cos": (0.18, 0.04, 0.82, 0.30), "carlin": (0.22, 0.02, 0.78, 0.30),
    "davil": (0.30, 0.03, 0.66, 0.22), "horgus": (0.30, 0.20, 0.72, 0.48),
}


def tono_papel(im, k=0.16):
    """Un poco hacia el guache frío del video sin perder la foto del juego."""
    a = np.asarray(im.convert("RGB")).astype(np.float32) / 255.0
    g = a.mean(2, keepdims=True)
    a = (1 - k) * a + k * g * np.float32((0.92, 0.98, 1.0))
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))


def recorte(slug, caja):
    im = Image.open(os.path.join(SRC, slug + ".jpg")).convert("RGB")
    w, h = im.size
    x0, y0, x1, y1 = caja
    return im.crop((int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h)))


GAMMA = {"ghoul": 0.7, "horgus": 0.8, "villa_darrow": 0.55, "muneca": 0.7, "escudo": 0.75, "skeleton": 0.8}   # capturas muy oscuras del juego


def foto(slug, caja, alto):
    im = recorte(slug, caja)
    if slug in GAMMA:
        a = np.asarray(im).astype(np.float32) / 255.0
        im = Image.fromarray((np.clip(a ** GAMMA[slug] * 1.05, 0, 1) * 255).astype(np.uint8))
    im = tono_papel(im)
    k = alto / im.height
    im = im.resize((max(2, int(im.width * k)), alto), Image.LANCZOS)
    b = max(14, alto // 28)
    out = Image.new("RGBA", (im.width + 2 * b, im.height + 2 * b), PAPEL + (255,))
    out.paste(im, (b, b))
    d = ImageDraw.Draw(out)
    d.rectangle([b - 1, b - 1, b + im.width, b + im.height], outline=TINTA + (255,), width=3)
    d.rectangle([0, 0, out.width - 1, out.height - 1], outline=(150, 138, 118, 255), width=2)
    os.makedirs("piezas/reales", exist_ok=True)
    out.save(f"piezas/reales/{slug}.png")


def medallon(slug, caja, lado=360):
    im = tono_papel(recorte(slug, caja), 0.1)
    s = lado / min(im.size)
    im = im.resize((max(lado, int(im.width * s)), max(lado, int(im.height * s))), Image.LANCZOS)
    im = im.crop(((im.width - lado) // 2, 0, (im.width - lado) // 2 + lado, lado))
    m = Image.new("L", (lado, lado), 0)
    ImageDraw.Draw(m).ellipse([6, 6, lado - 7, lado - 7], fill=255)
    out = Image.new("RGBA", (lado, lado), (0, 0, 0, 0))
    out.paste(im, (0, 0), m)
    d = ImageDraw.Draw(out)
    d.ellipse([4, 4, lado - 5, lado - 5], outline=(196, 156, 84, 255), width=9)
    d.ellipse([2, 2, lado - 3, lado - 3], outline=TINTA + (255,), width=3)
    d.ellipse([14, 14, lado - 15, lado - 15], outline=TINTA + (255,), width=2)
    os.makedirs("piezas/medallon", exist_ok=True)
    out.save(f"piezas/medallon/{slug}.png")


def icono(slug, archivo, lado=240):
    im = Image.open(os.path.join(SRC, f"icono_{archivo}.jpg")).convert("RGB").resize((lado, lado), Image.LANCZOS)
    b = lado // 14
    out = Image.new("RGBA", (lado + 2 * b, lado + 2 * b), (12, 10, 8, 255))
    out.paste(im, (b, b))
    d = ImageDraw.Draw(out)
    d.rectangle([b // 2, b // 2, out.width - 1 - b // 2, out.height - 1 - b // 2], outline=(196, 156, 84, 255), width=max(3, b // 2))
    d.rectangle([b - 2, b - 2, b + lado + 1, b + lado + 1], outline=(10, 8, 6, 255), width=3)
    os.makedirs("piezas/iconos", exist_ok=True)
    out.save(f"piezas/iconos/{slug}.png")


if __name__ == "__main__":
    for s, (c, a) in FOTOS.items():
        foto(s, c, a)
    for s, c in MEDALLON.items():
        medallon(s, c)
    for s, a in ICONOS.items():
        icono(s, a)
    print(len(FOTOS), "fotos,", len(MEDALLON), "medallones,", len(ICONOS), "iconos")
