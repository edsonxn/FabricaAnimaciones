# -*- coding: utf-8 -*-
"""Piezas compartidas por las escenas del anuncio de 60 s: cámara del «mundo», entradas, utilería grande y nombres de la pareja.
La pareja es la de la demo de la app (capturas de E:/CalendarioPareja/guia): Ana (coral, voz Lina) y Beto (violeta, voz Eric)."""
import math

from duo import (AV_A, AV_L, BG, H, TEL_H, TEL_W, W, e_in, e_out, lerp, pop, pr, smooth)

ANA_C, BETO_C = AV_A, AV_L
K = 1.92                                   # escala de la pantalla del teléfono a cámara 1 (px CSS -> px)


class Cam:
    """Cámara del mundo: zoom z alrededor de (cx, cy), que queda al centro de la pantalla."""

    def __init__(self, z=1.0, cx=W / 2, cy=H / 2):
        self.z, self.cx, self.cy = z, cx, cy

    def a(self, x, y):
        return W / 2 - self.cx * self.z + x * self.z, H / 2 - self.cy * self.z + y * self.z

    def aplicar(self, p):
        return p.cam(self.z, self.cx, self.cy)


def css(cam, tel_c, xc, yc, k=K):
    """Px CSS de la pantalla de un teléfono con centro `tel_c` (en el mundo) -> px de pantalla."""
    return cam.a(tel_c[0] - TEL_W * k / 2 + xc * k, tel_c[1] - TEL_H * k / 2 + yc * k)


def subir(t, t0, dur=0.5, d=18):
    """La entrada `rise` de la app: (opacidad, desplazamiento en y)."""
    u = e_out(pr(t, t0, t0 + dur))
    return smooth(pr(t, t0, t0 + dur * 0.8)), d * (1 - u)


def ventana(t, t0, t1, ent=0.3, sal=0.3):
    """Opacidad 0..1 de algo que vive entre t0 y t1 con fundidos."""
    return smooth(pr(t, t0, t0 + ent)) * (1 - smooth(pr(t, t1 - sal, t1)))


def utileria(p, emo, x, y, px, t, t0, t1, fase=0.0, sombra=True):
    """Emoji grande del plano delantero: entra con rebote, flota y se va (encoge) en t1."""
    if t < t0 or t > t1 + 0.3:
        return
    s = pop(t, t0, 0.38) * (1 - e_in(pr(t, t1, t1 + 0.3)))
    if s <= 0.01:
        return
    yy = y + 12 * math.sin(t * 3.0 + fase)
    with p.pivote(x, yy, s):
        if sombra:
            p.sombra(x - px * 0.35, yy - px * 0.2, x + px * 0.35, yy + px * 0.5, px * 0.3, blur=24, op=0.45, dy=18)
        p.emoji(emo, x, yy, px)


def velo_bajo(p, y, alto=140, op=0.78):
    """Apaga lo que queda debajo de `y` (foco en lo de arriba)."""
    import numpy as np
    ys = np.arange(H, dtype=np.float32)
    a = (np.clip((ys - y) / alto, 0, 1) * op)[:, None, None]
    p.im *= 1 - a
    p.im += a * np.float32(BG)


def mezcla_t(t, t0, dur):
    return e_out(pr(t, t0, t0 + dur))


def ir(a, b, u):
    return (lerp(a[0], b[0], u), lerp(a[1], b[1], u))
