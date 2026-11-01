# -*- coding: utf-8 -*-
"""Cámaras del plano secuencia «gravedad 5 s»: claves del paisaje (Xc, Hc, k), claves del espacio (ex, ey, r) y
transición continua paisaje <-> planeta (`zoom_global`, curvatura 1/rs)."""
import math

import numpy as np

from motor import W, H, prog, lerp, e_in, e_out, e_inout
from mundo_comun import Sup, cam_kf, kf
from anclas import A, Z1, Z2, Z3, Z4, TOTAL
from estado import T_IMPACTO

RW = 1.0e5          # radio del planeta en unidades del paisaje


def _claves():
    return [
        # ---- intro en el parque
        (0.0, -550, 210, 1.36),
        (A.suelo + 0.1, -545, 205, 1.38),
        (Z1[0], -540, 225, 1.30),
        # ---- versión A: casa en corte y parque
        (Z2[1], -1220, 165, 1.24),
        (A.quieto, -1230, 160, 1.32),
        (A.piso_a + 0.35, -1210, 175, 1.28),
        (A.caminando - 0.1, -560, 185, 1.16),
        (A.arriba_a + 0.3, -520, 265, 1.02),
        (A.arbol + 0.2, -460, 320, 0.90),
        (A.perros, -365, 295, 1.04),
        (A.lenta + 0.3, -345, 330, 0.98),
        (A.aire_a + 0.4, -330, 360, 0.90),
        # ---- viento y mar
        (A.dos_v + 0.3, -290, 420, 0.72),
        (A.golpe_v + 0.2, -250, 440, 0.75),
        (A.oidos + 0.25, -455, 425, 1.42),
        (A.viento + 0.1, 380, 285, 0.74),
        (A.olas - 0.1, 1480, 255, 0.68),
        (A.burbujas + 0.35, 1620, 270, 0.66),
        (A.gira + 0.2, 820, 320, 0.62),
        (A.recta_v + 0.4, 920, 320, 0.64),
        # ---- caída en Segundo 5
        (A.cinco_ca + 0.15, 560, 300, 0.68),
        (A.golpean + 0.2, 510, 200, 0.74),
        (A.humanidad - 0.1, -180, 225, 0.80),
        (Z3[0], -160, 240, 0.74),
        # ---- cierre en el parque
        (Z4[1], -430, 180, 1.28),
        (A.piso_c + 0.25, -415, 155, 1.36),
        (A.tiron + 0.2, -370, 225, 1.06),
        (A.fin, -330, 255, 0.92),
        (TOTAL, -320, 265, 0.88),
    ]


_CL = _claves()


def cam_paisaje(t):
    Xc, Hc, k = cam_kf(t, _CL)
    # Sacudida de cámara al golpear el suelo en Segundo 5 de la versión A
    sh = 0.0
    if T_IMPACTO - 0.08 < t < T_IMPACTO + 1.1:
        u = prog(t, T_IMPACTO - 0.08, T_IMPACTO + 1.1)
        sh = 11.0 * math.sin(t * 42.0) * (1.0 - u)
    return Sup.centrada(Xc + sh / k, Hc + sh * 0.65 / k, k)


def _cl_espacio():
    return [
        # ---- intro en el espacio
        (Z1[1], (920, 560), 285),
        (A.cohetes + 0.2, (800, 560), 265),
        (A.depende - 0.1, (610, 560), 245),
        (Z2[0], (940, 580), 275),
        # ---- versión B y principio del cierre
        (Z3[1], (900, 560), 290),
        (A.brutal, (810, 560), 305),
        (A.lava + 0.35, (830, 560), 295),
        (A.tres_b + 0.25, (690, 580), 215),
        (A.espacio_b + 0.3, (650, 585), 205),
        (A.sol_b + 0.2, (520, 580), 175),
        (A.nuclear + 0.85, (500, 580), 170),
        (A.cinco_b + 0.2, (860, 560), 295),
        (A.funde + 0.35, (880, 560), 305),
        (A.suerte + 0.2, (740, 515), 250),
        (A.materia + 0.3, (750, 510), 245),
        (Z4[0], (960, 560), 275),
    ]


_CE = _cl_espacio()


def cam_espacio(t):
    c = kf(t, [(a, b) for a, b, _ in _CE])
    r = math.exp(kf(t, [(a, math.log(rr)) for a, _, rr in _CE]))
    return float(c[0]), float(c[1]), r


def zoom_global(t, Z, salida):
    """Durante Z: (Sup del paisaje doblado, centro y radio de la Tierra en pantalla, s = cuánto es cielo azul)."""
    u = prog(t, Z[0], Z[1])
    tl = Z[0] if salida else Z[1]
    S0 = cam_paisaje(tl)
    Xc0, k0 = S0.X0, S0.k
    top0 = np.array([S0.hx, S0.hy])
    ex, ey, R = cam_espacio(Z[1] if salida else Z[0])
    top1 = np.array([ex, ey - R])
    v = u if salida else 1 - u
    w = e_in(v) * 0.45 + e_inout(v) * 0.55 if salida else e_out(v) * 0.45 + e_inout(v) * 0.55
    rs0 = RW * k0
    rs = math.exp(lerp(math.log(rs0), math.log(R), w))
    top = top0 + (top1 - top0) * e_inout(v)
    k = rs / RW
    S = Sup(float(top[0]), float(top[1]), k, 1.0 / rs, Xc0)
    s = prog(math.log(rs), math.log(1300), math.log(14000))
    return S, (float(top[0]), float(top[1] + rs), rs), s


def modo(t):
    if t < Z1[0]:
        return "paisaje"
    if t < Z1[1]:
        return "z_salida", Z1
    if t < Z2[0]:
        return "espacio"
    if t < Z2[1]:
        return "z_entrada", Z2
    if t < Z3[0]:
        return "paisaje"
    if t < Z3[1]:
        return "z_salida", Z3
    if t < Z4[0]:
        return "espacio"
    if t < Z4[1]:
        return "z_entrada", Z4
    return "paisaje"
