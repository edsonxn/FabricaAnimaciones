# -*- coding: utf-8 -*-
"""Utilidades comunes de «¿Quién envenenó al rey?» (noir feudal): rótulos, cartela de pergamino, reflejos y transformaciones."""
import math

import numpy as np

import noir as N
import noir_feudal as NF
from motor import H, W, clamp01


def rect(x, y, w, h):
    return np.array([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], float)


def rot(P, a, c=(0.0, 0.0)):
    P = np.asarray(P, float).reshape(-1, 2)
    c = np.asarray(c, float)
    ca, sa = math.cos(a), math.sin(a)
    Q = P - c
    return np.stack([Q[:, 0] * ca - Q[:, 1] * sa, Q[:, 0] * sa + Q[:, 1] * ca], 1) + c


def T_obj(cx, cy, ang=0.0, s=1.0, sx=1.0):
    """Transformación local -> mundo de un objeto (escala, espejo sx=-1 y giro alrededor de su origen)."""
    c = np.array([cx, cy], float)

    def f(P):
        P = np.asarray(P, float).reshape(-1, 2) * (s * sx, s)
        return rot(P, ang) + c
    return f


def a_pantalla(h, P, prof):
    M = h.matriz_capa(prof)
    return np.asarray(P, float) @ M[:2, :2].T + M[:2, 2]


def fijo(h):
    return h.capa(0.0)


def banda(h, s, cx, cy, px, t, t0, claro=False, sem=0, fuente=None, mundo=False, sale=None):
    """Rótulo de énfasis sólido (negro con letra crema, o crema con letra negra) que entra con un golpe; en pantalla."""
    if t < t0 or (sale is not None and t > sale):
        return
    u = clamp01((t - t0) / 0.14)
    k = 1.0 + 0.25 * (1 - u) ** 2
    im, _ = N._txt_img(s, px, fuente or N.FUENTE_SELLO, 3.0)
    an, al = (im.shape[1] + px * 0.9) * k, (px * 1.5) * k

    def pintar(cx, cy):
        h.pieza(rect(cx - an / 2, cy - al / 2, an, al), 228 if claro else 10, sem + 770, w=5, luz=(0, -1), d=4, sombra=0, trama=0,
                jit=0.6, rampa="pergamino" if claro else "personaje")
        h.luz_fija(rect(cx - an / 2 - 4, cy - al / 2 - 4, an + 8, al + 8), 0.95)
        N.texto_maquina(h, s, cx, cy, px * k, t, -99, cps=1e9, tono=0.04 if claro else 0.94, centro=True,
                        fuente=fuente or N.FUENTE_SELLO, track=3.0, encuadrar=False)
    if mundo:
        pintar(cx, cy)
    else:
        with h.capa(0.0):
            pintar(min(max(cx, an / 2 + 36), W - an / 2 - 36), min(max(cy, al / 2 + 36), H - al / 2 - 36))


def cartela(h, titulo, sub, cx, cy, t, t0, px=64, sem=0, sale=None):
    """Cartela de pergamino con el nombre en letra gótica y una línea a pluma debajo (presentación de personajes y lugares).
    Se desenrolla desde el centro en 0,35 s; siempre en pantalla."""
    if t < t0 or (sale is not None and t > sale + 0.3):
        return
    u = clamp01((t - t0) / 0.35)
    if sale is not None and t > sale:
        u = min(u, 1 - clamp01((t - sale) / 0.3))
    im, _ = N._txt_img(titulo, px, NF.FUENTE_GOTICA, 3.0)
    an = max(im.shape[1] + px * 1.6, len(sub or "") * px * 0.33 + px * 1.2)
    al = px * (2.25 if sub else 1.5)
    an_u = an * (0.08 + 0.92 * (1 - (1 - u) ** 3))
    with h.capa(0.0):
        cx = min(max(cx, an / 2 + 50), W - an / 2 - 50)
        cy = min(max(cy, al / 2 + 40), H - al / 2 - 40)
        h.pieza(rect(cx - an_u / 2, cy - al / 2, an_u, al), 205, sem + 780, w=4, luz=(0.2, -1), d=8, sombra=0.3, trama=0,
                jit=0.8, rampa="pergamino")
        for sx in (-1, 1):
            x = cx + sx * an_u / 2
            h.pieza(rect(x - 14, cy - al / 2 - 10, 28, al + 20), 170, sem + 781 + sx, w=4, luz=(0.2, -1), d=8, sombra=0.4, trama=0.3,
                    rim=0.6, rampa="pergamino")
        h.luz_fija(rect(cx - an_u / 2 - 20, cy - al / 2 - 14, an_u + 40, al + 28), 0.92)
        if u > 0.85:
            ty = cy - (px * 0.38 if sub else 0)
            N.texto_maquina(h, titulo, cx, ty, px, t, -99, cps=1e9, tono=np.array(h.pal["tinta"]) * 2.0, centro=True,
                            fuente=NF.FUENTE_GOTICA, track=1.0, encuadrar=False)
            if sub:
                N.texto_maquina(h, sub, cx, cy + px * 0.62, px * 0.42, t, t0 + 0.4, cps=40, tono=np.array(h.pal["tinta"]) * 2.4,
                                centro=True, fuente=NF.FUENTE_PLUMA_R, track=1.0, encuadrar=False)


def reflejar(h, t, y_mundo, k=0.32):
    """Suelo mojado: refleja lo que hay sobre y_mundo (también la emisión con su color)."""
    ys = h.tf(np.array([[0, y_mundo]]))[0][1]
    if not (40 < ys < H - 20):
        return
    N.reflejo(h.img, ys, k=k, t=t, onda=4.0, desv=3.0)
    if h._E is not None:
        N.reflejo(h._E, ys, k=k * 0.9, t=t, onda=4.0, desv=3.0)
        Ec = h._color_emision()
        y = int(ys)
        alto = min(H - y, y)
        Ec[y:y + alto] = Ec[y - alto:y][::-1]


def ambiente(h, k, col="luna"):
    h.ambiente[:] = np.array(h.pal[col], np.float32) * k
