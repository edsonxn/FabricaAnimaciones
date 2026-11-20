# -*- coding: utf-8 -*-
"""Planos 3: la tercera razón (volver a casa), los vuelos, la nave, las desventajas y el cierre."""
import math

import numpy as np

from comun import (H, W, L3, Cam, S, IDX, ap, bloque, cabecera, chorro, clamp, contador, e_inout, e_out, F0, F1, foto, lerp,
                   panel33, pr, real, rejilla_suelo, smooth, T0, T1, vacio, vent, ww, a_img, _Img)
from planos1 import rp, con_foto, barras, cam_orb
from planos2 import base_n1, tobera2d

X, Y, Z = np.array([1.0, 0, 0]), np.array([0, 1.0, 0]), np.array([0, 0, 1.0])
O = np.zeros(3)
SEG = dict(f5_regreso=88.0, f5_captura=131.0, f15_desp=0.0, f15ap=41.0, f1_desp=52.0, f1_gira=100.0, f1_expl=119.5,
           f2sep=0.0, r3b_comp=30.0, fab_b=196.0, b7_lenta=114.0, f1b_desp=40.0, f2b_lenta=54.0)
CAPT_X = 35.5
ZB_SH = 100.0


def torre(lz, apertura=0.0, z=ZB_SH, op=0.8):
    return S.torre_captura(lz, O, Z, X, 1.0, alto=146.0, z_brazos=z, apertura=apertura, op=op, w=1.0)


# ------------------------------------------------------------------ ATERRIZAJE (3.ª razón)
def at_vacio(t):
    """La etapa casi vacía con los 33 encendidos saldría disparada hacia arriba."""
    t0 = F0("aterrizaje", 2) - 0.3
    tdisp = ww("aterrizaje", 2, "disparada") - 0.8
    k = pr(t, tdisp, tdisp + 2.5)
    h = 10 + 160 * k * k
    lz = L3(cam_orb(Z * lerp(40, 110, k), lerp(150, 230, k), 210, 8, centro=(W * 0.35, H * 0.5)))
    rejilla_suelo(lz, O, X, Y, 140, 10, op=0.16)
    base = Z * h
    S.super_heavy(lz, base, Z, 1.0, 1.0, op=1.0, ref=Y)
    if t > ww("aterrizaje", 2, "encendiera") - 0.2:
        for i, p in enumerate(S.salidas_sh(base, Z, 1.0, Y)):
            if i % 3 == 0:
                chorro(lz, p, -Z, 20, 1.4, t, n=20, op=0.8, semilla=i)
    lz.texto("CASI VACÍA", 1150, 330, 80, "Bold Condensed", ap(t, ww("aterrizaje", 2, "vacía") - 0.2), "lm", esp=0.04)
    lz.texto("33 ENCENDIDOS =", 1150, 470, 56, "Bold Condensed", ap(t, ww("aterrizaje", 2, "encendiera") - 0.1), "lm", esp=0.05)
    lz.texto("SALDRÍA HACIA ARRIBA", 1150, 540, 56, "Bold Condensed", ap(t, tdisp + 0.4), "lm", esp=0.05)
    cabecera(lz, "RAZÓN 3 · VOLVER A CASA", ap(t, t0))
    return lz


def at_gigante(t):
    t0 = F0("aterrizaje", 3) - 0.3
    lz = vacio()
    o1 = ap(t, t0) * (1 - ap(t, F0("aterrizaje", 4) - 0.3))
    if o1 > 0:
        tobera2d(lz, 620, 540, 460, o1)
        lz.texto("UN SOLO MOTOR GIGANTE", 1100, 440, 60, "Bold Condensed", o1, "lm", esp=0.05)
        lz.texto("TODO O CASI NADA", 1104, 510, 30, "SemiBold Condensed", o1, "lm", esp=0.14)
        lz.texto("NO HAY FRENADO SUAVE", 1100, 620, 50, "Bold Condensed", o1 * ap(t, ww("aterrizaje", 3, "frenar") - 0.3), "lm", esp=0.05)
    o2 = ap(t, F0("aterrizaje", 4) - 0.3)
    if o2 > 0:
        t13 = F0("aterrizaje", 5) - 0.2
        on = set(IDX[0] + IDX[1]) if t > t13 else set(IDX[0][:2] + IDX[1][::3])
        panel33(lz, 760, 540, 72, op=o2, on=on, resalta={0, 1} if t > t13 else None)
        n = len(on)
        lz.texto(str(n), 1360, 470, 170, "Bold Condensed", o2, "lm", esp=0.02)
        lz.texto("ENCENDIDOS PARA FRENAR" if t > t13 else "BASTAN UNOS CUANTOS", 1366, 580, 28, "SemiBold Condensed", o2, "lm", esp=0.14)
    cabecera(lz, "RAZÓN 3 · VOLVER A CASA", ap(t, t0))
    return lz


def at_final(t):
    t0 = F0("aterrizaje", 7) - 0.3
    lz = vacio()
    panel33(lz, 760, 540, 72, op=ap(t, t0), on=set(IDX[0]), resalta={0})
    lz.texto("3", 1360, 430, 170, "Bold Condensed", ap(t, t0), "lm", esp=0.02)
    lz.texto("DEL CENTRO AL FINAL", 1366, 540, 28, "SemiBold Condensed", ap(t, t0), "lm", esp=0.14)
    lz.texto("LOS 20 DE AFUERA: TRABAJO HECHO", 1366, 640, 30, "SemiBold Condensed", ap(t, ww("aterrizaje", 7, "trabajo") - 0.2), "lm", esp=0.1)
    lz.texto("PRECISIÓN", 1360, 760, 80, "Bold Condensed", ap(t, ww("aterrizaje", 7, "precisión") - 0.2), "lm", esp=0.04)
    return lz


def at_captura(t):
    """Overlay sobre el video de la captura: los 3 del centro encendidos."""
    def ex(lz, tt):
        panel33(lz, W - 220, 300, 22, op=ap(tt, F0("aterrizaje", 6) + 0.5), on=set(IDX[0]), resalta={0})
        lz.texto("SOLO LOS 3 DEL CENTRO", W - 220, 450, 24, "SemiBold Condensed", ap(tt, F0("aterrizaje", 6) + 0.5), "mm", esp=0.14)
    return rp("f5", SEG["f5_captura"], F0("aterrizaje", 6) - 0.3, "VUELO 5 · 13 OCT 2024", "LA TORRE LO ATRAPA", extra=ex, vel=0.9)(t)


# ------------------------------------------------------------------ VUELOS
def v_riesgo(t):
    t0 = T0("vuelos")
    lz = vacio()
    k = pr(t, ww("vuelos", 0, "oportunidades") - 0.5, F1("vuelos", 0))
    cruz = tuple(i for i in range(33) if (i * 7) % 33 < 33 * k)
    panel33(lz, 760, 540, 72, op=ap(t, t0), cruz=cruz)
    lz.texto("33 MOTORES", 1300, 440, 80, "Bold Condensed", ap(t, t0 + 0.2), "lm", esp=0.04)
    lz.texto("33 FORMAS DE FALLAR", 1300, 530, 56, "Bold Condensed", ap(t, ww("vuelos", 0, "oportunidades") - 0.2), "lm", esp=0.05)
    return lz


def v_ocho(t):
    t0 = F0("vuelos", 3) - 0.3
    lz = vacio()
    cr = (5, 9) if t > ww("vuelos", 3, "dos", 1) else ()
    panel33(lz, 760, 540, 72, op=ap(t, t0), on=set(IDX[0] + IDX[1]), apagados=cr, cruz=cr, resalta={0, 1})
    lz.texto("11 DE 13", 1300, 440, 120, "Bold Condensed", ap(t, ww("vuelos", 3, "dos", 1) - 0.1), "lm", esp=0.02)
    lz.texto("REENCENDIERON PARA EL REGRESO", 1304, 520, 24, "SemiBold Condensed", ap(t, ww("vuelos", 3, "dos", 1)), "lm", esp=0.14)
    cabecera(lz, "VUELO 8 · 6 MAR 2025", ap(t, t0))
    return lz


def v_atrapado(t):
    """Vuelo 8: el propulsor llega a la torre y lo atrapan (3D)."""
    t0 = F0("vuelos", 4) - 0.3
    k = e_inout(pr(t, t0, t0 + 2.6))
    lz = L3(cam_orb(X * 30 + Z * 92, 140, 230, 12, centro=(W * 0.42, H * 0.5)))
    rejilla_suelo(lz, O, X, Y, 200, 10, op=0.15)
    ap_ = 1.0 - smooth(pr(t, t0 + 2.0, t0 + 2.8))
    torre(lz, apertura=ap_)
    base = X * CAPT_X + Z * (ZB_SH - S.Z_PERNOS_SH + 40 * (1 - k))
    S.super_heavy(lz, base, Z, 1.0, 1.0, op=1.0, ref=Y)
    if k < 0.98:
        for i, p in enumerate(S.salidas_sh(base, Z, 1.0, Y, cuales=IDX[0])):
            chorro(lz, p, -Z, 14, 1.2, t, n=24, op=0.9, semilla=i)
    lz.texto("ATRAPADO", 1250, 430, 90, "Bold Condensed", ap(t, t0 + 2.4), "lm", esp=0.04)
    lz.texto("AUN CON 2 MOTORES MENOS", 1254, 510, 28, "SemiBold Condensed", ap(t, t0 + 2.6), "lm", esp=0.14)
    cabecera(lz, "VUELO 8 · RECREACIÓN 3D", ap(t, t0))
    return lz


def v_s42(t):
    """Vuelo 15: la nave S42 entre los brazos de la torre (3D)."""
    t0 = ww("vuelos", 6, "nave") - 0.4
    k = e_inout(pr(t, t0, t0 + 2.4))
    lz = L3(cam_orb(X * 32 + Z * 90, 130, 220, 10, centro=(W * 0.42, H * 0.5)))
    rejilla_suelo(lz, O, X, Y, 200, 10, op=0.15)
    torre(lz, apertura=1.0 - smooth(pr(t, t0 + 1.8, t0 + 2.6)))
    base = X * CAPT_X + Z * (ZB_SH - S.Z_PERNOS_NAVE + 30 * (1 - k))
    S.nave(lz, base, Z, 1.0, op=1.0, ref=Y, flaps=0.0)
    lz.texto("LA NAVE S42", 1250, 430, 80, "Bold Condensed", ap(t, t0 + 0.3), "lm", esp=0.04)
    lz.texto("ATRAPADA POR LA TORRE", 1254, 500, 28, "SemiBold Condensed", ap(t, t0 + 2.3), "lm", esp=0.14)
    cabecera(lz, "VUELO 15 · RECREACIÓN 3D", ap(t, t0))
    return lz


# ------------------------------------------------------------------ NAVE
def n_39(t):
    t0 = T0("nave")
    k = pr(t, t0, F1("nave", 1))
    lz = L3(cam_orb(Z * 60, lerp(200, 170, k), 200 + 30 * k, 6, centro=(W * 0.3, H * 0.5)))
    S.pila(lz, O, Z, 1.0, op=1.0, ref=Y)
    o6 = ap(t, ww("nave", 1, "seis") - 0.2)
    lz.texto("6", 1080, 380, 140, "Bold Condensed", o6, "lm", esp=0.02)
    lz.texto("EN LA NAVE", 1180, 380, 30, "SemiBold Condensed", o6, "lm", esp=0.14)
    lz.texto("+ 33", 1080, 540, 140, "Bold Condensed", o6, "lm", esp=0.02)
    lz.texto("EN EL PROPULSOR", 1250, 540, 30, "SemiBold Condensed", o6, "lm", esp=0.14)
    o39 = ap(t, ww("nave", 1, "treinta") - 0.2)
    lz.l2([(1080, 640), (1600, 640)], o39, 1.6)
    lz.texto("39 MOTORES", 1080, 730, 110, "Bold Condensed", o39, "lm", esp=0.03)
    cabecera(lz, "STARSHIP COMPLETA", ap(t, t0))
    return lz


def n_muchos(t):
    t0 = F0("nave", 3) - 0.3
    lz = vacio()
    o1 = ap(t, t0) * (1 - ap(t, ww("nave", 3, "muchos") - 0.3))
    tobera2d(lz, 960, 520, 420, o1)
    lz.texto("UN MOTOR PERFECTO", 960, 160, 60, "Bold Condensed", o1, "mm", esp=0.05)
    o2 = ap(t, ww("nave", 3, "muchos") - 0.3)
    if o2 > 0:
        for j in range(33):
            x, y = 330 + (j % 11) * 126, 330 + (j // 11) * 170
            tobera2d(lz, x, y, 110, o2 * ap(t, ww("nave", 3, "muchos") - 0.3 + j * 0.03))
        for i, (txt, pal) in enumerate((("BUENOS", "buenos"), ("BARATOS", "baratos"), ("REPETIBLES", "repetibles"))):
            lz.texto(txt, 560 + i * 400, 900, 60, "Bold Condensed", ap(t, ww("nave", 3, pal) - 0.2), "mm", esp=0.05)
    return lz


# ------------------------------------------------------------------ CONTRAS
def c_tuberias(t):
    t0 = F0("contras", 1) - 0.3
    lz = vacio()
    cx, cy, e = 760, 540, 72
    panel33(lz, cx, cy, e, op=ap(t, t0) * 0.6)
    mot = S.motores_sh()
    k = pr(t, t0 + 0.3, F1("contras", 1))
    n = int(80 * k)
    for j in range(n):
        a, b = (j * 7) % 33, (j * 13 + 5) % 33
        xa, ya = cx + mot[a][1] * e, cy + mot[a][2] * e
        xb, yb = cx + mot[b][1] * e, cy + mot[b][2] * e
        mx, my = (xa + xb) / 2 + 40 * math.sin(j), (ya + yb) / 2 + 40 * math.cos(j)
        lz.l2([(xa, ya), (mx, my), (xb, yb)], 0.55, 1.0)
    for i, (txt, pal) in enumerate((("+ TUBERÍAS", "tuberías"), ("+ VÁLVULAS", "válvulas"), ("+ CABLES", "cables"),
                                    ("+ FORMAS DE FALLAR", "formas"))):
        lz.texto(txt, 1300, 330 + i * 110, 64, "Bold Condensed", ap(t, ww("contras", 1, pal) - 0.2), "lm", esp=0.05)
    cabecera(lz, "LAS DESVENTAJAS", ap(t, t0))
    return lz


def c_escudo(t):
    t0 = F0("contras", 2) - 0.3
    lz = vacio()
    cx, cy, e = 760, 540, 72
    mot = S.motores_sh()
    tx = ww("contras", 2, "explota") - 0.1
    k = pr(t, tx, tx + 1.2)
    vecinos = [i for i in range(33) if 0 < math.dist(mot[i][1:3], mot[17][1:3]) < 2.4]
    dañados = tuple(vecinos) if k > 0.6 else ()
    panel33(lz, cx, cy, e, op=ap(t, t0), apagados=(17,) + dañados, cruz=(17,))
    if 0 < k < 1:
        x, y = cx + mot[17][1] * e, cy + mot[17][2] * e
        for a in range(14):
            ang = a * math.pi / 7
            lz.l2([(x + 20 * k * math.cos(ang), y + 20 * k * math.sin(ang)), (x + 140 * k * math.cos(ang), y + 140 * k * math.sin(ang))], 1 - k, 2.0)
    op_ = ap(t, ww("contras", 2, "protección") - 0.3)
    if op_ > 0:
        for (_, mx, my, rt) in mot:
            lz.c2(cx + mx * e, cy + my * e, rt * e * 1.18 + 9, op_ * 0.8, w=1.2)
    lz.texto("DAÑA A SUS VECINOS", 1300, 430, 60, "Bold Condensed", ap(t, ww("contras", 2, "dañar") - 0.2), "lm", esp=0.05)
    lz.texto("CADA UNO, SU PROTECCIÓN", 1300, 560, 50, "Bold Condensed", op_, "lm", esp=0.05)
    return lz


def c_sincro(t):
    t0 = F0("contras", 3) - 0.3
    lz = vacio()
    k = pr(t, ww("contras", 3, "encender") - 0.1, ww("contras", 3, "sincronizados") + 0.3)
    on = set(i for i in range(33) if i / 33 < k)
    panel33(lz, 760, 540, 72, op=ap(t, t0), on=on)
    for i in range(33):
        y = 160 + i * 23
        x0 = 1250 + (i * 37 % 33) / 33 * 60
        lz.l2([(x0, y), (x0 + 400 * clamp(k * 1.6 - i / 33 * 0.6), y)], ap(t, t0), 2.0)
    lz.texto("TODOS SINCRONIZADOS", 1250, 960, 50, "Bold Condensed", ap(t, ww("contras", 3, "sincronizados") - 0.2), "lm", esp=0.05)
    cabecera(lz, "SECUENCIA DE ENCENDIDO · ESQUEMA", ap(t, t0))
    return lz


def c_r3(t):
    t0 = F0("contras", 4) - 0.3
    def ex(lz, tt):
        barras(lz, tt, 1000, 640, [("RAPTOR 2", 1630, "1 630 KG", ww("contras", 4, "ligero") - 0.6),
                                   ("RAPTOR 3", 1525, "1 525 KG", ww("contras", 4, "ligero") - 0.2)], 0, 1630, ancho=560, sep=110)
    return rp("r3b", SEG["r3b_comp"], t0, "RAPTOR 3", "MÁS SIMPLE, MÁS LIGERO", extra=ex)(t)


# ------------------------------------------------------------------ CIERRE
def ci_razones(t):
    t0 = T0("cierre")
    lz = vacio()
    panel33(lz, 480, 540, 56, op=ap(t, t0))
    lz.texto("¿POR QUÉ 33?", 480, 140, 70, "Bold Condensed", ap(t, t0), "mm", esp=0.05)
    for i, (txt, pal) in enumerate((("1 · UNA FALLA NO DETIENE LA MISIÓN", "falla"), ("2 · SE FABRICAN EN SERIE", "serie"),
                                    ("3 · FRENAR CON PRECISIÓN Y VOLVER", "frenar"))):
        lz.texto(txt, 940, 380 + i * 130, 50, "Bold Condensed", ap(t, ww("cierre", 1, pal) - 0.3), "lm", esp=0.04)
    return lz


def ci_trampa(t):
    t0 = F0("cierre", 2) - 0.3
    lz = vacio()
    base_n1(lz, 560, 520, 34, op=ap(t, t0), onda=(5, 0.6), cruz=(5,))
    panel33(lz, 1360, 520, 52, op=ap(t, ww("cierre", 2, "starship") - 0.2))
    lz.texto("N1 · UNA TRAMPA", 560, 880, 50, "Bold Condensed", ap(t, ww("cierre", 2, "trampa") - 0.2), "mm", esp=0.05)
    lz.texto("STARSHIP · LA SALIDA", 1360, 880, 50, "Bold Condensed", ap(t, ww("cierre", 2, "salida") - 0.2), "mm", esp=0.05)
    return lz


def ci_suscribe(t):
    t0 = F0("cierre", 3) - 0.3
    def ex(lz, tt):
        o = ap(tt, ww("cierre", 4, "suscríbete") - 0.2)
        lz.texto("T MENOS CERO", W / 2, 470, 120, "Bold Condensed", o, "mm", esp=0.06)
        lz.texto("CADA LANZAMIENTO, EXPLICADO EN 3D", W / 2, 560, 28, "SemiBold Condensed", o, "mm", esp=0.2)
        lz.l2([(W / 2 - 160, 640), (W / 2 + 160, 640), (W / 2 + 160, 710), (W / 2 - 160, 710)], o, 1.8, cerrada=True)
        lz.texto("SUSCRÍBETE", W / 2, 675, 40, "Bold Condensed", o, "mm", esp=0.12)
    return rp("f2b", SEG["f2b_lenta"], t0, "EL PRÓXIMO VUELO", "EXPLICADO EN 3D", extra=ex, vel=1.0)(t)


# ------------------------------------------------------------------ montaje 3
PLANOS = [
    (T0("aterrizaje"), rp("f5", SEG["f5_regreso"], T0("aterrizaje"), "RAZÓN 3", "VOLVER A CASA")),
    (F0("aterrizaje", 1) - 0.3, rp("f1b", SEG["f1b_desp"], F0("aterrizaje", 1) - 0.3, "AL DESPEGAR", "MILES DE TONELADAS · TODA LA FUERZA")),
    (F0("aterrizaje", 2) - 0.3, at_vacio),
    (F0("aterrizaje", 3) - 0.3, at_gigante),
    (F0("aterrizaje", 6) - 0.3, at_captura),
    (F0("aterrizaje", 7) - 0.3, at_final),
    (T0("vuelos"), v_riesgo),
    (F0("vuelos", 1) - 0.3, rp("f1", SEG["f1_desp"], F0("vuelos", 1) - 0.3, "VUELO 1 · 20 ABR 2023", "VARIOS MOTORES SE APAGAN")),
    (ww("vuelos", 1, "perdió") - 0.3, rp("f1", SEG["f1_gira"], ww("vuelos", 1, "perdió") - 0.3, "PIERDE EL CONTROL", "GIRA SIN SEPARARSE")),
    (ww("vuelos", 1, "explosión") - 0.6, rp("f1", SEG["f1_expl"], ww("vuelos", 1, "explosión") - 0.6, "VUELO 1", "TERMINA EN UNA EXPLOSIÓN")),
    (F0("vuelos", 2) - 0.3, rp("f2sep", SEG["f2sep"], F0("vuelos", 2) - 0.3, "VUELO 2 · 18 NOV 2023", "LOS 33 HASTA LA SEPARACIÓN")),
    (F0("vuelos", 3) - 0.3, v_ocho),
    (F0("vuelos", 4) - 0.3, v_atrapado),
    (F0("vuelos", 5) - 0.3, rp("f15ap", SEG["f15_desp"], F0("vuelos", 5) - 0.3, "VUELO 15 · 13 NOV 2026", "33 RAPTOR 3 AL DESPEGAR", zoom=1.4, cy=0.5)),
    (F0("vuelos", 6) - 0.3, rp("f15ap", SEG["f15ap"], F0("vuelos", 6) - 0.3, "SIN COMBUSTIBLE PARA VOLVER", "CAPTURA CANCELADA · CAE AL GOLFO", zoom=1.4, cy=0.5)),
    (ww("vuelos", 6, "nave") - 0.4, v_s42),
    (T0("nave"), n_39),
    (F0("nave", 2) - 0.3, rp("fabrica", SEG["fab_b"], F0("nave", 2) - 0.3, "CADA MOTOR", "SE CAMBIA, SE REVISA, SE REEMPLAZA")),
    (F0("nave", 3) - 0.3, n_muchos),
    (T0("contras"), rp("b7", SEG["b7_lenta"], T0("contras"), "¿DESVENTAJAS?", "CLARO", vel=0.5)),
    (F0("contras", 1) - 0.3, c_tuberias),
    (F0("contras", 2) - 0.3, c_escudo),
    (F0("contras", 3) - 0.3, c_sincro),
    (F0("contras", 4) - 0.3, c_r3),
    (T0("cierre"), ci_razones),
    (F0("cierre", 2) - 0.3, ci_trampa),
    (F0("cierre", 3) - 0.3, ci_suscribe),
]


def sfx():
    return [(T0("aterrizaje"), "pulso", 0.7, 0.0, None), (F0("aterrizaje", 1), "rugido", 0.7, 0.0, None),
            (ww("aterrizaje", 2, "disparada") - 0.6, "whoosh", 0.7, 0.0, None), (F0("aterrizaje", 5), "ignicion", 0.6, 0.0, None),
            (F0("aterrizaje", 6) + 2.0, "brazos", 0.6, 0.0, None), (T0("vuelos"), "alarma", 0.5, 0.0, None),
            (ww("vuelos", 1, "explosión"), "explosion", 0.8, 0.0, None), (F0("vuelos", 2), "rugido", 0.6, 0.0, None),
            (ww("vuelos", 3, "dos", 1), "apagado", 0.6, 0.0, None), (F0("vuelos", 4) + 2.2, "brazos", 0.6, 0.0, None),
            (F0("vuelos", 5), "rugido", 0.6, 0.0, None), (F0("vuelos", 6), "alarma", 0.5, 0.0, None),
            (T0("nave"), "whoosh", 0.6, 0.0, None), (ww("nave", 1, "treinta"), "sello", 0.7, 0.0, None),
            (F0("contras", 1), "tic", 0.5, 0.0, None), (ww("contras", 2, "explota"), "explosion", 0.5, 0.0, None),
            (F0("contras", 3), "ignicion", 0.5, 0.0, None), (T0("cierre"), "pulso", 0.8, 0.0, None),
            (ww("cierre", 4, "suscríbete"), "campana", 0.7, 0.0, None)]
