# -*- coding: utf-8 -*-
"""Mosaico de pegatinas para revisarlas con la vista: previews/peg_NN.jpg (8 x 6 por hoja, con el slug).
    python _mosaico_peg.py [slug ...]     (sin slugs: las de Rasganorte, desde «saurfang» en _pegatinas_bajar.TITULOS)"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import _pegatinas_bajar as PB  # noqa: E402

C, COL, FIL = 220, 8, 6
F = ImageFont.truetype("arialbd.ttf", 15)


def main(slugs):
    if not slugs:
        k = list(PB.TITULOS)
        slugs = k[k.index("saurfang"):]
    os.makedirs(os.path.join(AQUI, "previews"), exist_ok=True)
    por = COL * FIL
    for h in range(0, len(slugs), por):
        hoja = Image.new("RGB", (COL * C, FIL * (C + 20)), (40, 40, 48))
        d = ImageDraw.Draw(hoja)
        for i, s in enumerate(slugs[h:h + por]):
            x, y = (i % COL) * C, (i // COL) * (C + 20)
            r = os.path.join(AQUI, "pegatinas", s + ".png")
            if os.path.exists(r):
                im = Image.open(r).convert("RGBA")
                im.thumbnail((C - 8, C - 8))
                hoja.paste(im, (x + (C - im.width) // 2, y + (C - im.height) // 2), im)
            d.text((x + 4, y + C), s, font=F, fill=(255, 220, 80))
        ruta = os.path.join(AQUI, "previews", f"peg_{h // por + 1:02d}.jpg")
        hoja.save(ruta, quality=85)
        print(ruta)


if __name__ == "__main__":
    main(sys.argv[1:])
