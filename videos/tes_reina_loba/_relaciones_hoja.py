# -*- coding: utf-8 -*-
"""Hoja de prueba de las redes de relaciones (_relaciones.py): por cada red, su CUADRO FINAL (todos los pasos aplicados)
grande y 2 cuadros intermedios (a media animación: un nexo que se dibuja, un quiebre o un cambio de intención).
    python _relaciones_hoja.py            → previews/relaciones_hoja.jpg
    python _relaciones_hoja.py cap3 [dir] → además el cuadro final de esa red a tamaño completo (dir, por defecto previews/)"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from _relaciones import REDES, T  # noqa: E402

PASO = 2.6


def cuadro(fn, pasos, dt):
    mk = [1.0 + PASO * k for k in range(len(pasos))]
    a = np.asarray(fn(dt, mk[-1] + 4.0, mk))
    im = Image.fromarray(a[..., [2, 1, 0, 3]].copy())
    bg = Image.new("RGBA", (1920, 1080), (60, 80, 60, 255))
    bg.alpha_composite(im, ((1920 - im.width) // 2, (1080 - im.height) // 2))
    return bg.convert("RGB")


def momentos(pasos):
    """(dt, etiqueta) de los dos intermedios: el primer quiebre/cambio a media animación y un nexo dibujándose."""
    mk = [1.0 + PASO * k for k in range(len(pasos))]
    ev = [k for k, p in enumerate(pasos) if p.get("rompe") or p.get("cambia")]
    k1 = ev[0] if ev else len(pasos) // 2
    k0 = 1 if len(pasos) > 1 and k1 != 1 else 0
    return [(mk[k0] + .45, f"paso {k0} +0,45 s"), (mk[k1] + .35, f"paso {k1} +0,35 s")], mk[-1] + 3.0


if __name__ == "__main__":
    solo = sys.argv[1] if len(sys.argv) > 1 else None
    filas = []
    for nombre, f, pasos in REDES:
        fn = f()
        inter, fin = momentos(pasos)
        final = cuadro(fn, pasos, fin)
        if solo == nombre:
            dst = sys.argv[2] if len(sys.argv) > 2 else os.path.join(AQUI, "previews")
            final.save(os.path.join(dst, f"relaciones_{nombre}.jpg"), quality=92)
            for i, (dt, _) in enumerate(inter):
                cuadro(fn, pasos, dt).save(os.path.join(dst, f"relaciones_{nombre}_i{i}.jpg"), quality=90)
        fila = Image.new("RGB", (1920, 720), (0, 0, 0))
        fila.paste(final.resize((1280, 720), Image.LANCZOS), (0, 0))
        d = ImageDraw.Draw(fila)
        for i, (dt, et) in enumerate(inter):
            fila.paste(cuadro(fn, pasos, dt).resize((640, 360), Image.LANCZOS), (1280, 360 * i))
            d.text((1290, 360 * i + 8), et, fill=(255, 255, 0), font=T.fuente("SemiBold Condensed", 24))
        d.text((12, 8), f"{nombre} · FINAL" + ("" if not fn.avisos else "  AVISOS: " + "; ".join(fn.avisos))[:160],
               fill=(255, 255, 0), font=T.fuente("SemiBold Condensed", 26))
        filas.append(fila)
        print(nombre, fn.avisos or "OK")
    hoja = Image.new("RGB", (1920, 720 * len(filas)), (0, 0, 0))
    for i, f in enumerate(filas):
        hoja.paste(f, (0, 720 * i))
    hoja.save(os.path.join(AQUI, "previews", "relaciones_hoja.jpg"), quality=85)
    print("previews/relaciones_hoja.jpg")
