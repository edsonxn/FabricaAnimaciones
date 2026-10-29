# -*- coding: utf-8 -*-
"""Pegatinas REALES de World of Warcraft (warcraft.wiki.gg / Wowhead, `pegatinas/_orig/`, ver `_bajar_reales.py`)
para el estilo pegatina Flow (copiado de videos/wow_darrowshire/_reales.py):
  piezas/reales/<slug>.png   foto del juego en un marco de papel crema (borde y sombra los pone pegaflow.actor)
  piezas/medallon/<slug>.png retrato oval con filete de tinta
  piezas/iconos/<slug>.png   icono real del objeto con marco de icono de WoW
  previews/_reales_contacto.jpg  hoja de contacto de todo
Uso (desde la carpeta del video): python _reales.py"""
import glob
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

SRC = "pegatinas/_orig"
PAPEL = (240, 232, 214)
TINTA = (40, 30, 24)
FONDO_ARMA = (34, 30, 36)   # las armas con transparencia van sobre pizarra oscura

# slug: (recorte x0, y0, x1, y1 en fracciones, alto de salida)
FOTOS = {
    # personajes
    "alexandros": ((0, 0, 1, 1), 680), "alexandros_vivo": ((0.08, 0, 1, 1), 680),
    "alexandros_espiritu": ((0, 0, 0.86, 0.80), 640), "renault": ((0, 0.08, 1, 0.92), 620),
    "darion": ((0, 0, 1, 1), 680), "tirion": ((0, 0, 1, 1), 600), "tirion_highlord": ((0, 0, 1, 1), 680),
    "taelan": ((0, 0, 0.80, 1), 680), "isillien": ((0, 0, 1, 1), 620), "kelthuzad": ((0, 0, 1, 0.97), 680),
    "rey_exanime": ((0.05, 0.04, 0.95, 1), 680), "eitrigg": ((0, 0, 1, 1), 640), "balnazzar": ((0.27, 0.04, 0.76, 1), 640),
    "dathrohan": ((0.05, 0, 0.95, 1), 640), "ribalimpia": ((0, 0.04, 0.82, 1), 640), "magni": ((0, 0, 1, 1), 620),
    "zeliek": ((0, 0, 1, 1), 640), "korthazz": ((0, 0, 1, 1), 640), "blaumeux": ((0, 0, 1, 1), 640),
    "myranda": ((0, 0, 1, 1), 600), "renfray": ((0, 0, 1, 1), 640), "koltira": ((0, 0, 1, 1), 680),
    "thassarian": ((0, 0, 1, 1), 680), "orbaz": ((0, 0, 1, 1), 680), "maxwell": ((0, 0, 1, 1), 680),
    "barthilas": ((0, 0, 1, 1), 640), "uther": ((0, 0, 1, 1), 680), "zabra": ((0, 0, 1, 1), 640),
    # lugares
    "naxxramas": ((0.08, 0, 0.92, 0.78), 520), "capilla": ((0, 0, 1, 1), 520), "monasterio": ((0, 0, 1, 1), 520),
    "stratholme": ((0, 0, 1, 1), 520), "acherus": ((0, 0, 1, 0.92), 520), "torre_taelan": ((0, 0, 1, 1), 520),
    # armas (modelos del juego)
    "crematoria": ((0, 0, 1, 1), 300), "crematoria_corrupta": ((0, 0, 1, 1), 320), "agonia_escarcha": ((0, 0, 1, 1), 640),
}
# iconos REALES de objetos (Wowhead, 56 px) → piezas/iconos/<slug>.png con marco de icono de WoW
ICONOS = {"crematoria": "inv_sword_48", "crematoria_corrupta": "inv_sword_2h_ashbringercorrupt",
          "martillo_taelan": "inv_hammer_01", "simbolo_honor": "inv_banner_02", "cuadro": "inv_scroll_06",
          "obsequio": "inv_box_01", "fragmento_alma": "inv_jewelcrafting_gem_05", "marca_fordring": "inv_jewelry_talisman_07"}
# medallones: recorte de la CARA (fracciones) → óvalo; (fuente, caja) si la cara sale de otra imagen
MEDALLON = {
    "alexandros": ("alexandros_vivo", (0.58, 0.0, 0.80, 0.18)),   # el Alexandros vivo (el de Naxxramas va con casco)
    "renault": (0.28, 0.20, 0.52, 0.36), "darion": (0.42, 0.07, 0.70, 0.22), "tirion": (0.25, 0.07, 0.65, 0.24),
    "taelan": (0.50, 0.0, 0.73, 0.19), "isillien": (0.32, 0.03, 0.68, 0.24), "kelthuzad": (0.24, 0.30, 0.64, 0.60),
    "rey_exanime": (0.38, 0.02, 0.64, 0.21),
}
# capturas muy oscuras del juego
GAMMA = {"magni": 0.75, "renfray": 0.7, "rey_exanime": 0.75, "balnazzar": 0.8, "alexandros_espiritu": 0.8, "orbaz": 0.8,
         "zabra": 0.8, "koltira": 0.85, "thassarian": 0.85, "renault": 0.85, "darion": 0.9, "alexandros": 0.85}


def abrir(slug):
    f = [p for p in glob.glob(os.path.join(SRC, slug + ".*"))][0]
    im = Image.open(f)
    if im.mode in ("RGBA", "LA", "P") or "transparency" in im.info:
        im = im.convert("RGBA")
        fondo = Image.new("RGBA", im.size, FONDO_ARMA + (255,))
        fondo.alpha_composite(im)
        im = fondo
    return im.convert("RGB")


def tono_papel(im, k=0.16):
    """Un poco hacia el guache frío del video sin perder la foto del juego."""
    a = np.asarray(im.convert("RGB")).astype(np.float32) / 255.0
    g = a.mean(2, keepdims=True)
    a = (1 - k) * a + k * g * np.float32((0.92, 0.98, 1.0))
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))


def recorte(slug, caja):
    im = abrir(slug)
    w, h = im.size
    x0, y0, x1, y1 = caja
    im = im.crop((int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h)))
    if slug in GAMMA:
        a = np.asarray(im).astype(np.float32) / 255.0
        im = Image.fromarray((np.clip(a ** GAMMA[slug] * 1.05, 0, 1) * 255).astype(np.uint8))
    return im


def foto(slug, caja, alto):
    im = tono_papel(recorte(slug, caja))
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
    fuente = slug
    if isinstance(caja[0], str):
        fuente, caja = caja
    im = tono_papel(recorte(fuente, caja), 0.1)
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


def contacto(S=200, cols=10):
    """previews/_reales_contacto.jpg: todas las piezas en rejilla con su slug."""
    piezas = [(f"reales/{s}", f"piezas/reales/{s}.png") for s in FOTOS] + \
             [(f"iconos/{s}", f"piezas/iconos/{s}.png") for s in ICONOS] + \
             [(f"medallon/{s}", f"piezas/medallon/{s}.png") for s in MEDALLON]
    filas = (len(piezas) + cols - 1) // cols
    hoja = Image.new("RGB", (cols * S, filas * (S + 18)), (70, 66, 62))
    d = ImageDraw.Draw(hoja)
    try:
        fnt = ImageFont.truetype("arial.ttf", 13)
    except OSError:
        fnt = ImageFont.load_default()
    for i, (nom, p) in enumerate(piezas):
        im = Image.open(p).convert("RGBA")
        im.thumbnail((S - 8, S - 8))
        x, y = (i % cols) * S, (i // cols) * (S + 18)
        hoja.paste(im, (x + (S - im.width) // 2, y + (S - im.height) // 2), im)
        d.text((x + 4, y + S + 1), nom, fill=(255, 236, 160), font=fnt)
    os.makedirs("previews", exist_ok=True)
    hoja.save("previews/_reales_contacto.jpg", quality=88)


if __name__ == "__main__":
    for s, (c, a) in FOTOS.items():
        foto(s, c, a)
    for s, c in MEDALLON.items():
        medallon(s, c)
    for s, a in ICONOS.items():
        icono(s, a)
    contacto()
    print(len(FOTOS), "fotos,", len(MEDALLON), "medallones,", len(ICONOS), "iconos")
