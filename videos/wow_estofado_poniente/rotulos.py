# -*- coding: utf-8 -*-
"""Rótulos de pergamino con serif amarilla («película de fantasía 1983») → rotulos/rot_N.png (RGBA, para efectos.py).
Pergamino oscuro y gastado por código (ruido + bordes quemados) para que el dorado se lea; texto Palatino negrita con
sombra y filo oscuro. Uso (desde la carpeta del video):  python rotulos.py
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import guion

FUENTE = "C:/Windows/Fonts/palab.ttf"
ORO = (247, 205, 74)
os.makedirs("rotulos", exist_ok=True)


def ruido(w, h, escala, sem):
    r = np.random.default_rng(sem)
    peq = r.random((max(2, h // escala), max(2, w // escala))).astype(np.float32)
    return np.asarray(Image.fromarray((peq * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32) / 255


def pergamino(w, h, sem):
    n = 0.55 * ruido(w, h, 40, sem) + 0.3 * ruido(w, h, 9, sem + 1) + 0.15 * ruido(w, h, 2, sem + 2)
    base = np.array([92, 64, 34], np.float32)                      # sepia oscuro
    rgb = base[None, None] * (0.7 + 0.6 * n[..., None])
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    dx = np.minimum(xx, w - 1 - xx) / (w * 0.5)
    dy = np.minimum(yy, h - 1 - yy) / (h * 0.5)
    borde = np.minimum(dx * w / h, dy)                             # 0 en el filo
    rgb *= np.clip(0.35 + borde * 2.2, 0, 1)[..., None]            # bordes tostados
    irregular = borde * 6 - 0.25 * ruido(w, h, 14, sem + 3)        # filo roto
    alfa = np.clip(irregular * 4, 0, 1) * 235
    return Image.fromarray(np.dstack([np.clip(rgb, 0, 255), alfa]).astype(np.uint8), "RGBA")


def rotulo(texto, k):
    lineas = texto.split("\n")
    tams = [96 if i == 0 else 64 for i in range(len(lineas))] if len(lineas) > 1 else [120]
    if len(lineas) > 2:
        tams = [74] + [54] * (len(lineas) - 1)
    fnts = [ImageFont.truetype(FUENTE, t) for t in tams]
    cajas = [f.getbbox(l) for f, l in zip(fnts, lineas)]
    w = max(b[2] - b[0] for b in cajas) + 220
    h = sum(b[3] - b[1] for b in cajas) + 34 * (len(lineas) - 1) + 170
    im = pergamino(w, h, 10 + k)
    capa = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    y = 85
    for f, l, b in zip(fnts, lineas, cajas):
        x = (w - (b[2] - b[0])) / 2 - b[0]
        d.text((x + 5, y - b[1] + 6), l, font=f, fill=(20, 10, 2, 220))
        d.text((x, y - b[1]), l, font=f, fill=ORO + (255,), stroke_width=2, stroke_fill=(60, 30, 6, 255))
        y += b[3] - b[1] + 34
    sombra = capa.filter(ImageFilter.GaussianBlur(1))
    im = Image.alpha_composite(im, sombra)
    im = Image.alpha_composite(im, capa)
    im.save(f"rotulos/rot_{k}.png")
    return im.size


if __name__ == "__main__":
    for k, r in enumerate(guion.ROTULOS):
        print(f"rotulos/rot_{k}.png", rotulo(r["texto"], k))
