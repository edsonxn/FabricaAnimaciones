# -*- coding: utf-8 -*-
"""Hoja con el CUADRO FINAL de cada árbol genealógico de efectos.py → previews/arboles_final.jpg"""
exec(open("_ventanas.py", encoding="utf-8").read().split("a0, a1")[0])
import numpy as np
from PIL import Image
ims = []
for d in efectos.FX:
    if d.get("nombre", "").startswith("MG árbol"):
        s = t(d["de"])[0]; e = t(d["a"])[0]
        mk = [t(m)[0] - s for m in d["marcas"]]
        a = np.asarray(d["fn"](e - s - 0.2, e - s, mk))
        im = Image.fromarray(a[..., [2, 1, 0, 3]])
        bg = Image.new("RGBA", (1920, 1080), (60, 80, 60, 255)); bg.alpha_composite(im, ((1920 - im.width) // 2, (1080 - im.height) // 2))
        ims.append(bg.convert("RGB").resize((960, 540)))
hoja = Image.new("RGB", (1920, 540 * 3), (0, 0, 0))
for i, im in enumerate(ims):
    hoja.paste(im, ((i % 2) * 960, (i // 2) * 540))
hoja.save("previews/arboles_final.jpg", quality=85)
