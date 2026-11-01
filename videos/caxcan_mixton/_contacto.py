# -*- coding: utf-8 -*-
"""Hojas de contacto de Flow: previews/_contacto_<carpeta>_N.jpg, 6 claves por hoja (a | b lado a lado), 380 px por imagen.
Uso: python _contacto.py imagenes|hojas [prefijo]"""
import glob
import os
import sys

from PIL import Image, ImageDraw, ImageFont

d = os.path.dirname(os.path.abspath(__file__))
sub = sys.argv[1]
pref = sys.argv[2] if len(sys.argv) > 2 else ""
claves = sorted({os.path.basename(p)[:-6] for p in glob.glob(os.path.join(d, sub, f"{pref}*_a.jpg"))})
W, H, POR = 380, 214, 6
fnt = ImageFont.truetype("arial.ttf", 15)
for h in range(0, len(claves), POR):
    grupo = claves[h:h + POR]
    lam = Image.new("RGB", (4 * W + 50, 3 * (H + 22) + 10), (40, 40, 40))
    dr = ImageDraw.Draw(lam)
    for i, c in enumerate(grupo):
        for v, var in enumerate("ab"):
            p = os.path.join(d, sub, f"{c}_{var}.jpg")
            if not os.path.exists(p):
                continue
            im = Image.open(p).convert("RGB")
            im.thumbnail((W, H))
            x = (i % 2) * (2 * W + 30) + v * (W + 4) + 8
            y = (i // 2) * (H + 22) + 22
            lam.paste(im, (x, y))
            dr.text((x + 2, y - 18), f"{c} {var}", fill=(255, 220, 120), font=fnt)
    out = os.path.join(d, "previews", f"_contacto_{sub}{('_' + pref) if pref else ''}_{h // POR + 1}.jpg")
    lam.save(out, quality=85)
    print(out)
