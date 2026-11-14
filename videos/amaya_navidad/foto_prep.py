# -*- coding: utf-8 -*-
"""Fotos reales (Commons, licencia libre) → presentaciones coquette en stickers/foto_<n>.png + fuentes.json (créditos).
Estilos: polaroid (marco blanco, pie ancho, cinta washi), recorte (esquinas redondas y borde blanco grueso de sticker),
revista (borde de papel rasgado crema con sombra de recorte). python foto_prep.py"""
import json
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
ELEGIDAS = {   # nombre → (candidata, estilo, recorte cuadrado opcional (x0,y0,x1,y1 en fracción))
    "camara": ("camara_0", "polaroid", None), "termo": ("termo_0", "recorte", None), "oso": ("oso_0", "polaroid", None),
    "squishy": ("squishy_0", "revista", None), "maquillaje": ("maquillaje_1", "polaroid", None),
    "pirata": ("pirata_0", "recorte", None), "original": ("pirata_2", "recorte", None), "audifonos": ("audif_1", "revista", None),
    "juego": ("juegob_2", "polaroid", None),
}
WASHI = [(248, 207, 220, 215), (200, 226, 246, 215), (255, 236, 170, 215)]


def cuadrar(im, ratio=1.0):
    w, h = im.size
    if w / h > ratio:
        nw = int(h * ratio)
        return im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    nh = int(w / ratio)
    return im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))


def polaroid(foto, k):
    f = cuadrar(foto, 1.0).resize((700, 700), Image.LANCZOS)
    im = Image.new("RGBA", (800, 960), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 40, 790, 950), radius=10, fill=(255, 253, 250, 255))
    im.paste(f, (50, 80))
    d.polygon([(300, 10), (500, 0), (510, 80), (290, 90)], fill=WASHI[k % 3])
    return im


def recorte(foto, k):
    f = cuadrar(foto, 1.0).resize((700, 700), Image.LANCZOS)
    m = Image.new("L", f.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, 700, 700), radius=90, fill=255)
    im = Image.new("RGBA", (780, 780), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, 780, 780), radius=120, fill=(255, 255, 255, 255))
    im.paste(f, (40, 40), m)
    return im


def revista(foto, k):
    f = cuadrar(foto, 1.25).resize((750, 600), Image.LANCZOS)
    rg = np.random.default_rng(k + 3)
    W, H = 830, 680
    pts = []
    for i in range(40):
        pts.append((i * W / 39, rg.uniform(0, 14)))
    for i in range(30):
        pts.append((W - rg.uniform(0, 14), i * H / 29))
    for i in range(40):
        pts.append((W - i * W / 39, H - rg.uniform(0, 14)))
    for i in range(30):
        pts.append((rg.uniform(0, 14), H - i * H / 29))
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(im).polygon(pts, fill=(252, 246, 234, 255))
    im.paste(f, (40, 40))
    d = ImageDraw.Draw(im)
    d.polygon([(W - 160, -4), (W + 4, -4), (W + 4, 110), (W - 60, 120)], fill=WASHI[(k + 1) % 3])
    return im


def main():
    meta = {}
    for f in ("cand_1.json", "cand_2.json", "cand_3.json", "cand.json"):
        p = os.path.join(AQUI, "fotos", f)
        if os.path.exists(p):
            meta.update(json.load(open(p, encoding="utf-8")))
    fuentes = {}
    for k, (nom, (cand, estilo, _)) in enumerate(ELEGIDAS.items()):
        foto = Image.open(os.path.join(AQUI, "fotos", "cand", cand + ".jpg")).convert("RGB")
        im = {"polaroid": polaroid, "recorte": recorte, "revista": revista}[estilo](foto, k)
        im.save(os.path.join(AQUI, "stickers", f"foto_{nom}.png"))
        m = meta[cand]
        fuentes[f"foto_{nom}"] = dict(estilo=estilo, titulo=m["titulo"], pagina=m["pagina"], autor=m["autor"], licencia=m["licencia"])
        print(nom, estilo, m["licencia"], m["autor"][:40])
    json.dump({"fotos": fuentes, "nota": "Fotos de Wikimedia Commons con licencia libre; crédito en la descripción del video."},
              open(os.path.join(AQUI, "fuentes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
