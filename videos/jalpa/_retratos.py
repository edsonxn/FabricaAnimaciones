# -*- coding: utf-8 -*-
"""Retratos REALES (Commons, dominio público; créditos en nucleo/datos/retratos/CREDITOS.md) como pegatinas: el cuadro dentro de un
marco de madera pintado con filete dorado → piezas/retratos/<quien>.png (el borde de papel y la sombra los pone pegaflow.actor).
Uso (desde la carpeta del video): python _retratos.py hidalgo alvarado mendoza"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "nucleo", "datos", "retratos")
M = 30                      # grosor del marco
TINTA = (48, 30, 22)


def marco(quien):
    im = Image.open(os.path.join(SRC, quien + ".jpg")).convert("RGB")
    a = np.asarray(im).astype(np.float32) / 255.0
    g = a.mean(axis=2, keepdims=True)                       # un poco hacia el guache cálido del estilo (sin perder el cuadro)
    a = 0.82 * a + 0.18 * g * np.float32((1.08, 0.97, 0.82))
    im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
    w, h = im.size
    W, H = w + 2 * M, h + 2 * M
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(out)
    d.rounded_rectangle([0, 0, W - 1, H - 1], 10, fill=(92, 58, 34, 255), outline=TINTA + (255,), width=5)
    for k in range(6):                                      # vetas de la madera pintada
        y = int(H * (0.1 + 0.16 * k))
        d.line([(6, y), (M - 6, y + 14)], fill=(70, 42, 24, 255), width=2)
        d.line([(W - M + 6, y + 8), (W - 6, y - 6)], fill=(70, 42, 24, 255), width=2)
    d.rectangle([M - 7, M - 7, W - M + 6, H - M + 6], fill=(214, 168, 82, 255), outline=TINTA + (255,), width=2)
    out.paste(im, (M, M))
    d.rectangle([M, M, W - M - 1, H - M - 1], outline=TINTA + (255,), width=3)
    sombra = Image.new("L", (W, H), 0)                      # sombra interior del marco sobre el lienzo
    ImageDraw.Draw(sombra).rectangle([M, M, W - M - 1, H - M - 1], outline=110, width=10)
    sombra = sombra.filter(ImageFilter.GaussianBlur(6))
    rgb = np.asarray(out).astype(np.float32)
    k = np.asarray(sombra).astype(np.float32)[..., None] / 255.0
    inner = np.zeros((H, W, 1), np.float32)
    inner[M:H - M, M:W - M] = 1
    rgb[..., :3] *= 1 - 0.45 * k * inner
    dst = os.path.join("piezas", "retratos")
    os.makedirs(dst, exist_ok=True)
    Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGBA").save(os.path.join(dst, quien + ".png"))
    print("ok", quien, (W, H))


if __name__ == "__main__":
    for q in sys.argv[1:] or ["hidalgo", "alvarado", "mendoza"]:
        marco(q)
