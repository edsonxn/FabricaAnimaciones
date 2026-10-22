# -*- coding: utf-8 -*-
"""Recorta piezas de interfaz pintadas en Flow sobre fondo BLANCO (marcos, medallones, botones) a PNG con transparencia.
Creado el 22-oct-2026 (zelda_oot: «esos cuadros de texto se ven muy poco trabajados… apóyate de Flow», el usuario).
Quita solo el blanco CONECTADO al borde (el interior claro de un pergamino o una etiqueta se conserva), suaviza el borde
y recorta al contenido. Con --partes N separa las N piezas más grandes (p. ej. una fila de botones) de izquierda a derecha.

  python nucleo/recortar_ui.py <entrada.jpg> <salida.png> [--partes N]   (con N: salida_1.png … salida_N.png)
"""
import sys

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage


def mascara(im, umbral=232):
    a = np.asarray(im.convert("RGB")).astype(np.int16)
    blanco = (a.min(axis=2) >= umbral) & ((a.max(axis=2) - a.min(axis=2)) <= 18)
    lab, _ = ndimage.label(blanco)
    borde = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    fondo = np.isin(lab, list(borde))
    m = Image.fromarray(((~fondo) * 255).astype(np.uint8))
    return m.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))


def recortar(src, dst, partes=0):
    im = Image.open(src).convert("RGB")
    m = mascara(im)
    rgba = im.convert("RGBA")
    rgba.putalpha(m)
    if not partes:
        rgba.crop(m.point(lambda v: 255 if v > 20 else 0).getbbox()).save(dst)
        print(dst, rgba.size)
        return
    lab, n = ndimage.label(np.asarray(m) > 20)
    tam = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
    mayores = sorted(np.argsort(tam)[::-1][:partes] + 1,
                     key=lambda k: ndimage.find_objects(lab == k)[0][1].start)
    for i, k in enumerate(mayores, 1):
        sl = ndimage.find_objects((lab == k).astype(int))[0]
        p = rgba.crop((sl[1].start, sl[0].start, sl[1].stop, sl[0].stop))
        out = dst.replace(".png", f"_{i}.png")
        p.save(out)
        print(out, p.size)


if __name__ == "__main__":
    args = sys.argv[1:]
    n = 0
    if "--partes" in args:
        n = int(args[args.index("--partes") + 1])
        args = args[:args.index("--partes")]
    recortar(args[0], args[1], n)
