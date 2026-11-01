# -*- coding: utf-8 -*-
"""Cámaras del plano secuencia: claves del paisaje (Xc, Hc, k) por tramo, claves del espacio (Tierra: centro y radio en
pantalla) y la transición continua paisaje <-> planeta (el horizonte se curva hasta ser la Tierra vista desde el espacio)."""
import math

import numpy as np

from motor import W, H, prog, lerp, e_in, e_out, e_inout
from mundo_comun import Sup, cam_kf, kf
from anclas import A, Z1, Z2, Z3, Z4, PORTAL_IN, PORTAL_OUT, TOTAL
import gente as G

RW = 1.0e5          # radio del planeta en unidades del paisaje (la curvatura sale de aquí)


def _jumbo(t, dx=0.0, dh=0.0, k=0.85):
    X, Hh = G.pos_jumbo(t)
    return (t, X + dx, Hh + dh, k)


def _claves():
    return [
        (0.0, -770, 250, 1.36), (Z1[0], -765, 262, 1.30),
        # ---- vuelta al paisaje (versión A)
        (Z2[1], -760, 300, 1.0), (A.esfuma - 0.6, -745, 320, 1.0), (A.quinta + 0.6, -700, 330, 1.05),
        (A.montana - 1.2, -3000, 760, 0.52), (A.oidos - 0.6, -3050, 770, 0.52),
        (A.oidos + 0.5, -792, 205, 2.5), (A.timpanos, -792, 205, 2.6), (A.cielo - 0.2, -792, 212, 2.5),
        (A.azul + 0.2, -700, 1000, 0.85), (A.uno_f - 0.8, -660, 1050, 0.85),
        # ---- fuego
        (A.uno_f + 0.3, -150, 330, 0.82), (A.velas - 0.3, -120, 330, 0.84), (A.velas + 1.2, 0, 330, 0.9),
        (A.coches - 0.4, 40, 360, 0.9), (A.coches + 0.6, 600, 160, 1.05), (A.aviones - 1.2, 820, 170, 1.05),
        _jumbo(A.aviones - 0.1, 60, -40), _jumbo(A.piedra - 0.6, 60, -60), _jumbo(A.planea + 0.6, 250, -150, 0.6),
        _jumbo(A.centrales - 1.6, 260, -150, 0.6),
        (A.centrales + 0.6, 1760, 420, 0.72), (A.llama - 0.6, 1760, 430, 0.75), (A.llama + 0.8, 1000, 380, 0.52),
        (A.sol_f - 0.4, 900, 380, 0.52), (A.brillando + 0.4, 900, 960, 2.6), (A.necesita + 1.0, 900, 960, 2.8),
        # ---- cuerpo (entrada por el pecho)
        (A.dos_c + 1.2, -800, 165, 2.1), (PORTAL_IN[0], -800, 150, 2.3), (PORTAL_IN[1], -800, 150, 4.5),
        # ---- salida por la cabeza
        (PORTAL_OUT[0], -797, 196, 4.0), (PORTAL_OUT[1], -795, 205, 2.6), (A.tunel, -790, 235, 1.5),
        (A.desmayarse + 0.6, -820, 250, 1.25),
        # ---- regreso A
        (A.cinco_ra + 0.2, -760, 300, 1.05), (A.vuelve_ra + 0.6, -760, 300, 1.05), (A.sube + 0.4, -795, 205, 2.0),
        (A.contrario + 0.6, -795, 205, 2.0), (A.brasas, -560, 230, 1.5), (A.pilotos - 0.6, -560, 230, 1.5),
        (A.pilotos + 0.5, -1420, 760, 0.8), (A.motores_ra + 0.8, -1260, 800, 0.8),
        (A.choques + 0.5, 600, 330, 0.72), (A.sobreviviriamos + 1.2, 650, 330, 0.72),
        (A.version_facil + 0.8, 0, 450, 0.42), (A.dificil - 0.6, 0, 450, 0.42),
        # ---- versión B: átomos
        (A.dificil + 1.0, 600, -150, 0.38), (A.sorpresa + 1.0, 420, -260, 0.44),
        (A.mitad_at - 0.2, -100, -420, 0.75), (A.agua_at - 0.6, -100, -420, 0.75),
        (A.agua_at + 0.4, 3100, -550, 0.62), (A.cuerpo_at - 0.5, 3100, -550, 0.62),
        (A.cuerpo_at + 0.3, -790, 170, 1.5), (A.pegamento - 0.4, -790, 170, 1.5),
        (A.pegamento + 0.6, 300, 150, 0.45), (A.cero_s - 0.2, 300, 150, 0.45),
        # ---- suelo
        (A.cero_s + 0.5, 300, 120, 0.72), (A.edificios - 0.8, 330, 120, 0.72), (A.edificios + 0.4, 350, 200, 0.62),
        (A.metales - 0.6, 380, 180, 0.62), (A.metales + 0.6, 600, 230, 0.95), (A.piezas - 0.4, 620, 230, 0.95),
        (A.piezas + 0.5, 540, 130, 2.0), (A.invento - 0.3, 540, 130, 2.1), (A.invento + 0.8, 520, 200, 1.2),
        (A.uno_ag - 0.6, 500, 200, 1.1),
        # ---- agua
        (A.uno_ag + 0.5, 2900, 120, 0.7), (A.molecula - 0.8, 2900, 120, 0.7), (A.molecula + 0.2, 2950, 50, 0.85),
        (A.oceanos - 0.4, 2950, 50, 0.85), (A.oceanos + 0.6, 2600, 350, 0.48), (A.fondo_ag - 0.4, 2600, 350, 0.48),
        (A.fondo_ag + 0.9, 3600, -1050, 0.75), (A.brutal + 0.4, 3600, -1000, 0.75), (A.treinta - 1.3, 3100, 600, 0.42),
        (A.nosotros - 0.3, 3100, 650, 0.42),
        # ---- nosotros
        (A.nosotros + 0.5, 1200, 700, 0.3), (A.terceras_n - 0.1, -790, 230, 1.15), (A.sobrevivir + 0.8, -790, 220, 1.25),
        (A.agua_n + 0.2, -700, 230, 1.0), (A.llevan + 1.6, -700, 230, 1.0), (A.version_n + 0.4, -1100, 300, 0.62),
        (A.cinco_rb - 1.0, -1000, 300, 0.62),
        # ---- regreso B
        (A.cinco_rb + 0.2, -900, 500, 0.5), (A.vuelve_rb + 0.6, -900, 500, 0.5), (A.revuelto + 0.8, 1600, 1000, 0.3),
        (A.combustible, 1700, 1000, 0.3), (Z3[0], 1700, 1000, 0.3),
        # ---- cierre
        (Z4[1], -760, 280, 1.15), (A.fin, -770, 262, 1.3), (TOTAL, -772, 258, 1.34),
    ]


_CL = _claves()


def cam_paisaje(t):
    Xc, Hc, k = cam_kf(t, _CL)
    # temblor de cámara cuando el suelo se hunde y cuando el gas estalla
    sh = 0.0
    if A.edificios - 0.2 < t < A.hunde + 2.0:
        sh = 6 * math.sin(t * 37) * (1 if t < A.hunde + 1.2 else 1 - prog(t, A.hunde + 1.2, A.hunde + 2.0))
    if A.brutal - 0.4 < t < A.brutal + 1.4:
        sh += 9 * math.sin(t * 41) * (1 - prog(t, A.brutal, A.brutal + 1.4))
    return Sup.centrada(Xc + sh / k, Hc + sh * 0.6 / k, k)


# ======================================================================== espacio
def _cl_espacio():
    return [
        (Z1[1], (960, 560), 300), (A.siempre - 0.2, (960, 560), 300), (A.cinco_i + 0.4, (700, 560), 280),
        (A.parece + 0.4, (620, 560), 270), (A.sitios - 0.4, (620, 560), 270), (A.sitios + 0.4, (960, 610), 250),
        (A.mundo_i - 0.6, (960, 610), 250), (A.mundo_i + 0.4, (960, 680), 240), (A.reglas - 0.6, (960, 680), 240),
        (A.reglas + 0.4, (430, 580), 230), (A.facil - 1.0, (430, 580), 230), (Z2[0], (960, 600), 260),
        # final de la versión B y realidad
        (Z3[1], (960, 560), 300), (A.suerte, (960, 560), 300), (A.interruptor + 0.6, (760, 560), 290),
        (A.millones_r, (760, 560), 290), (A.fabricaron + 0.3, (700, 600), 330), (A.hoy + 0.4, (700, 600), 330),
        (Z4[0], (960, 600), 280),
    ]


_CE = _cl_espacio()


def cam_espacio(t):
    c = kf(t, [(a, b) for a, b, _ in _CE])
    r = math.exp(kf(t, [(a, math.log(rr)) for a, _, rr in _CE]))
    return float(c[0]), float(c[1]), r


# ======================================================================== transición paisaje <-> planeta
def zoom_global(t, Z, salida):
    """Durante Z: (Sup del paisaje doblado, centro y radio de la Tierra en pantalla, s = cuánto es cielo azul).
    salida=True: del paisaje al espacio; False: del espacio al paisaje."""
    u = prog(t, Z[0], Z[1])
    tl = Z[0] if salida else Z[1]
    S0 = cam_paisaje(tl)
    Xc0, k0 = S0.X0, S0.k
    top0 = np.array([S0.hx, S0.hy])
    ex, ey, R = cam_espacio(Z[1] if salida else Z[0])
    top1 = np.array([ex, ey - R])
    v = u if salida else 1 - u                   # 0 = paisaje, 1 = espacio
    w = e_in(v) * 0.45 + e_inout(v) * 0.55 if salida else e_out(v) * 0.45 + e_inout(v) * 0.55
    rs0 = RW * k0
    rs = math.exp(lerp(math.log(rs0), math.log(R), w))
    top = top0 + (top1 - top0) * e_inout(v)
    k = rs / RW
    S = Sup(float(top[0]), float(top[1]), k, 1.0 / rs, Xc0)
    s = prog(math.log(rs), math.log(1300), math.log(14000))
    return S, (float(top[0]), float(top[1] + rs), rs), s


def modo(t):
    """'paisaje' | 'z1'... qué mundo se ve en t."""
    if t < Z1[0]:
        return "paisaje"
    if t < Z1[1]:
        return "z_salida", Z1
    if t < Z2[0]:
        return "espacio"
    if t < Z2[1]:
        return "z_entrada", Z2
    if t < PORTAL_IN[0]:
        return "paisaje"
    if t < PORTAL_IN[1]:
        return "portal_in"
    if t < PORTAL_OUT[0]:
        return "cuerpo"
    if t < PORTAL_OUT[1]:
        return "portal_out"
    if t < Z3[0]:
        return "paisaje"
    if t < Z3[1]:
        return "z_salida", Z3
    if t < Z4[0]:
        return "espacio"
    if t < Z4[1]:
        return "z_entrada", Z4
    return "paisaje"
