# -*- coding: utf-8 -*-
"""Base común de los portales (escenas dibujadas dentro de las polaroids): registro PORTAL, decorador, colores y utilidades."""
import functools  # noqa: F401
import math

import cv2  # noqa: F401
import numpy as np

from kit import INI, FIN, ww, we, TL  # noqa: F401  (anclas de la voz)
from arcade import *  # noqa: F401,F403
from mg_obj import *  # noqa: F401,F403

PORTAL = {}
FIG = (0.018, 0.020, 0.034)
FIG2 = (0.045, 0.045, 0.075)


def portal(nombre, vin=0.45):
    def deco(fn):
        def f(t):
            p = P()
            fn(p, t)
            vineta_p(p, vin)
            return np.clip(p.im * 1.22 + 0.006, 0, 1.5)        # el filtro de película oscurece: se compensa aquí
        PORTAL[nombre] = f
        return fn
    return deco


def parpadeo(t, t0, dur=0.9):
    """0..1: un tubo que se enciende a tirones desde t0."""
    e = t - t0
    if e < 0:
        return 0.0
    if e > dur:
        return 1.0
    return 1.0 if int(e * 23) % 3 == 0 or e > dur * 0.8 else 0.15


def rotulo_rec(p, txt="RECREACIÓN · NO ES UNA IMAGEN REAL", x=1890, y=1050, op=0.75):
    p.texto(txt, x, y, 26, (0.85, 0.85, 0.9), "mono", op, "rb")


def coche(p, x, y, esc, color=SIL, dir=1, luces=True, t=0.0, op=1.0):
    """Coche de perfil (silueta) con ruedas que giran; (x, y) = suelo bajo el centro."""
    E = esc
    f = dir
    p.poly([(x - f * E * 0.95, y - E * 0.18), (x - f * E * 0.95, y - E * 0.42), (x - f * E * 0.55, y - E * 0.48), (x - f * E * 0.32, y - E * 0.78),
            (x + f * E * 0.35, y - E * 0.78), (x + f * E * 0.62, y - E * 0.48), (x + f * E * 0.95, y - E * 0.42), (x + f * E * 0.98, y - E * 0.18)], color, op)
    p.poly([(x - f * E * 0.26, y - E * 0.72), (x + f * E * 0.02, y - E * 0.72), (x + f * E * 0.02, y - E * 0.50), (x - f * E * 0.48, y - E * 0.50)],
           (0.35, 0.45, 0.55), 0.35 * op)
    p.poly([(x + f * E * 0.08, y - E * 0.72), (x + f * E * 0.32, y - E * 0.72), (x + f * E * 0.55, y - E * 0.50), (x + f * E * 0.08, y - E * 0.50)],
           (0.35, 0.45, 0.55), 0.35 * op)
    for wx in (-0.58, 0.60):
        cxw = x + f * E * wx
        p.circ(cxw, y - E * 0.16, E * 0.18, (0.02, 0.02, 0.03), op)
        p.circ(cxw, y - E * 0.16, E * 0.09, (0.30, 0.30, 0.32), op)
        a = t * 12 * f
        p.linea((cxw - E * 0.08 * math.cos(a), y - E * 0.16 - E * 0.08 * math.sin(a)), (cxw + E * 0.08 * math.cos(a), y - E * 0.16 + E * 0.08 * math.sin(a)),
                E * 0.025, (0.1, 0.1, 0.1), op)
    if luces:
        p.haz(x + f * E * 0.97, y - E * 0.34, 0 if f > 0 else 180, E * 3.2, 18, (1.0, 0.95, 0.75), 0.35 * op)
        p.glow(x + f * E * 0.97, y - E * 0.34, E * 0.25, (1.0, 0.95, 0.8), 0.9 * op)
        p.glow(x - f * E * 0.95, y - E * 0.34, E * 0.18, (1.0, 0.15, 0.1), 0.8 * op)


def ventana_web(p, x0, y0, x1, y1, titulo, url, t, t0, barra=(0.10, 0.20, 0.55)):
    """Ventana de navegador de finales de los 90 (barra azul, botones grises, barra de dirección). Devuelve el área útil."""
    p.rect(x0 + 16, y0 + 20, x1 + 16, y1 + 20, (0, 0, 0), 0.45)
    p.rect(x0, y0, x1, y1, (0.76, 0.76, 0.76))
    p.rect(x0 + 6, y0 + 6, x1 - 6, y0 + 52, barra, grad=(mix(barra, (1, 1, 1), 0.15), barra))
    p.texto(titulo, x0 + 22, y0 + 29, 30, (1, 1, 1), "sans_b", 1, "lm")
    for k in range(3):
        p.rect(x1 - 52 - k * 44, y0 + 12, x1 - 14 - k * 44, y0 + 46, (0.76, 0.76, 0.76))
    p.rect(x0 + 6, y0 + 58, x1 - 6, y0 + 112, (0.70, 0.70, 0.70))
    p.rect(x0 + 150, y0 + 66, x1 - 20, y0 + 104, (1, 1, 1))
    p.texto("Dirección", x0 + 22, y0 + 85, 26, (0.1, 0.1, 0.1), "sans", 1, "lm")
    n = int(clamp((t - t0) / 1.4) * len(url))
    p.texto(url[:n] + ("|" if n < len(url) and int(t * 4) % 2 == 0 else ""), x0 + 162, y0 + 85, 26, (0.05, 0.05, 0.3), "mono", 1, "lm")
    p.rect(x0 + 6, y0 + 118, x1 - 6, y1 - 6, (0.96, 0.96, 0.93))
    return x0 + 6, y0 + 118, x1 - 6, y1 - 6
