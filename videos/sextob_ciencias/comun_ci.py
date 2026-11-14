# -*- coding: utf-8 -*-
"""Ayudas comunes a los planos de Ciencias: título que entra, letrero con palomita, pantalla de PAUSA Y CONTESTA, opciones."""
import math

import numpy as np

from acuarela import TINTA, e_out, pr, rgb, rotulo
from iconos_ia import marca_x, palomita
from kit_amaya import CREMA, MORADO, ROJO, VERDE, cuenta, entra, letrero, pausa, tarjeta

GRIS_C = np.array([0.85, 0.85, 0.85], np.float32)


def titulo(im, texto, t, t0, seed, col=ROJO, x=740, y=110, px=78, rot=-0.02):
    if t > t0 - 0.3:
        rotulo(im, texto, x, y, px, col, t, seed=seed, esc=entra(t, t0 - 0.3), rot=rot)


def cartel(im, texto, x, y, px, t, t0, seed, col=CREMA, txt=TINTA, rot=0.0, ok=None, t_ok=1e9):
    """Letrero que entra en t0; ok=True/False pone palomita o tache desde t_ok."""
    if t <= t0 - 0.3:
        return
    letrero(im, texto, x, y, px, t, col=col, txt=txt, seed=seed, esc=entra(t, t0 - 0.3), rot=rot)
    if ok is not None and t > t_ok - 0.2:
        w = len(texto) * px * 0.56 + px * 1.4
        (palomita if ok else marca_x)(im, x + w / 2 + 40, y, 0.7 * entra(t, t_ok - 0.2), t, seed=seed + 50,
                                      col=VERDE if ok else ROJO)


def pantalla_pregunta(im, t, t_pausa, t_fin, t_resp, seed, lineas, t_lineas, y0=420, px=66, col=MORADO):
    """Botón de PAUSA + rótulo + la pregunta en renglones (cada uno cuando la voz llega) + cuenta 3-2-1 en el silencio."""
    pausa(im, 230, 200, 0.7 * entra(t, t_pausa - 0.3), t, seed=seed, texto=False)
    rotulo(im, "PAUSA Y CONTESTA", 800, 200, 72, ROJO, t, seed=seed + 5, esc=entra(t, t_pausa - 0.1))
    for k, (ln, tk) in enumerate(zip(lineas, t_lineas)):
        if t > tk - 0.3:
            e = entra(t, tk - 0.3)
            w = len(ln) * px * 0.56 + px * 1.6
            tarjeta(im, 760, y0 + 150 * k, w * e, px * 1.9 * e, t, CREMA, seed + 10 + k * 5, rot=(k % 2 - 0.5) * 0.03)
            rotulo(im, ln, 760, y0 + 4 + 150 * k, px * e + 1, col, t, seed=seed + 11 + k * 5, tinta=False, rot=(k % 2 - 0.5) * 0.03)
    cuenta(im, 1640, 250, t, t_fin + 0.15, t_resp + 0.1, s=0.75, seed=seed + 30)


def opciones(im, t, y, ops, t_aps, ok=-1, t_ok=1e9, seed=0, xs=(380, 760, 1140), px=40):
    """Botones de opción [(texto, color)]; desde t_ok el correcto se pone verde y brinca, los otros se apagan."""
    for k, ((txt, col), x) in enumerate(zip(ops, xs)):
        e = entra(t, t_aps[k] - 0.2)
        if e <= 0.01:
            continue
        r = pr(t, t_ok - 0.1, t_ok + 0.3)
        if k == ok:
            c, b = (VERDE if r > 0.5 else col), 1 + 0.15 * r
        else:
            c, b = col * (1 - 0.5 * r) + GRIS_C * 0.5 * r, 1 - 0.1 * r
        tarjeta(im, x, y, 330 * e * b, 110 * e * b, t, c, seed + k * 5, rot=(k - 1) * 0.02)
        rotulo(im, txt, x, y + 4, px * e * b + 1, CREMA if (k == ok and r > 0.5) else TINTA, t, seed=seed + 1 + k * 5, tinta=False)
