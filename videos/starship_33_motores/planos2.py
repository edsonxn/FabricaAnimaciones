# -*- coding: utf-8 -*-
"""Planos 2: el N1 soviético, el Falcon 9 y el Falcon Heavy, la primera razón (fallas), la segunda (fábrica)."""
import math

import numpy as np

from comun import (H, W, L3, Cam, S, IDX, ap, bloque, cabecera, clamp, contador, e_inout, e_out, F0, F1, foto, lerp, panel33,
                   pr, real, smooth, T0, T1, vacio, vent, ww, a_img, _Img)
from planos1 import rp, con_foto, barras

SEG = dict(n1b_desp=90.0, n1_expl=168.0, n1_ruina=178.0, crs1_flash=7.0, fh=0.0, fab=88.0, r3_banco=133.0,
           b7_amplia=20.0, b7_tuit=40.0, crs1_desp=0.0)


# ------------------------------------------------------------------ piezas 2D
def base_n1(lz, cx, cy, e, op=1.0, apagados=(), cruz=(), on_all=True, onda=None):
    """Base del N1: 24 motores en el anillo exterior + 6 en el centro. onda = (índice, k) = un fallo que se propaga."""
    if op <= 0.01:
        return []
    lz.c2(cx, cy, 7.6 * e, op * 0.55, w=1.2)
    pos = []
    for i in range(24):
        a = 2 * math.pi * i / 24
        pos.append((cx + 6.6 * e * math.cos(a), cy + 6.6 * e * math.sin(a)))
    for i in range(6):
        a = 2 * math.pi * i / 6 + math.pi / 6
        pos.append((cx + 2.4 * e * math.cos(a), cy + 2.4 * e * math.sin(a)))
    for i, (x, y) in enumerate(pos):
        r = 0.78 * e
        prender = on_all and i not in apagados
        if onda is not None:
            j, k = onda
            d = math.dist(pos[j], (x, y)) / e
            if d < k * 9:
                prender = False
        lz.c2(x, y, r, op * (1.0 if prender else 0.4), w=1.3, lleno=prender)
        if i in cruz:
            dd = r * 1.1
            lz.l2([(x - dd, y - dd), (x + dd, y + dd)], op, 1.8)
            lz.l2([(x - dd, y + dd), (x + dd, y - dd)], op, 1.8)
    return pos


def base_f9(lz, cx, cy, e, op=1.0, cruz=(), etiqueta=True):
    """Octaweb del Falcon 9: 8 alrededor + 1 en el centro."""
    if op <= 0.01:
        return
    lz.c2(cx, cy, 1.85 * e, op * 0.55, w=1.2)
    pos = [(cx, cy)] + [(cx + 1.25 * e * math.cos(2 * math.pi * i / 8), cy + 1.25 * e * math.sin(2 * math.pi * i / 8)) for i in range(8)]
    for i, (x, y) in enumerate(pos):
        on = i not in cruz
        lz.c2(x, y, 0.42 * e, op * (1.0 if on else 0.4), w=1.3, lleno=on)
        if i in cruz:
            d = 0.46 * e
            lz.l2([(x - d, y - d), (x + d, y + d)], op, 2.0)
            lz.l2([(x - d, y + d), (x + d, y - d)], op, 2.0)


def tobera2d(lz, x, y, s, op=1.0):
    """Icono de motor visto de lado (cámara arriba, campana abajo)."""
    lz.l2([(x - 0.18 * s, y - 0.5 * s), (x + 0.18 * s, y - 0.5 * s), (x + 0.18 * s, y - 0.18 * s), (x - 0.18 * s, y - 0.18 * s)], op, 1.4, cerrada=True)
    lz.l2([(x - 0.12 * s, y - 0.18 * s), (x - 0.34 * s, y + 0.5 * s)], op, 1.4)
    lz.l2([(x + 0.12 * s, y - 0.18 * s), (x + 0.34 * s, y + 0.5 * s)], op, 1.4)
    lz.l2([(x - 0.34 * s, y + 0.5 * s), (x + 0.34 * s, y + 0.5 * s)], op * 0.7, 1.2)


# ------------------------------------------------------------------ N1
def n_base(t):
    t0 = F0("n1", 1) - 0.3
    lz = vacio()
    tk = F0("n1", 2) - 0.2
    # KORD: falla el 3, se apaga el opuesto (15); luego más parejas
    cruz, apag = [], []
    if t > ww("n1", 2, "fallaba"):
        cruz.append(3)
    if t > ww("n1", 2, "opuesto"):
        apag.append(15)
    if t > F0("n1", 3) + 0.4:
        cruz.append(8); apag.append(20)
    if t > F0("n1", 3) + 1.4:
        cruz.append(26); apag.append(29)
    pos = base_n1(lz, 1260, 540, 52, op=ap(t, t0), apagados=apag, cruz=cruz)
    if t > ww("n1", 2, "opuesto") and pos:
        o = ap(t, ww("n1", 2, "opuesto")) * (1 - ap(t, F0("n1", 3)))
        lz.l2([pos[3], pos[15]], o * 0.8, 1.4)
        lz.texto("KORD", (pos[3][0] + pos[15][0]) / 2 + 20, (pos[3][1] + pos[15][1]) / 2 - 20, 30, "Bold Condensed", o, "lm", esp=0.1)
    bloque(lz, 120, 380, "30 MOTORES", "24 EN LA ORILLA + 6 EN EL CENTRO", ap(t, ww("n1", 1, "treinta")) * (1 - ap(t, tk)), 90)
    bloque(lz, 120, 380, "SI UNO FALLA,", "SE APAGA TAMBIÉN EL DE ENFRENTE", vent(t, tk, F0("n1", 3) - 0.1), 70)
    bloque(lz, 120, 380, "EN TEORÍA:", "PUEDE PERDER VARIOS Y SEGUIR", ap(t, F0("n1", 3) - 0.1), 70)
    cabecera(lz, "N1 · PRIMERA ETAPA (BLOQUE A)", ap(t, t0))
    return lz


def n_cuatro(t):
    t0 = F0("n1", 4) - 0.3
    lz = vacio()
    fechas = [("21 FEB 1969", "INCENDIO · APAGADO A T+68 s"), ("3 JUL 1969", "EXPLOTA AL DESPEGAR"),
              ("26 JUN 1971", "GIRA Y SE DESINTEGRA"), ("23 NOV 1972", "EXPLOTA UN MOTOR · T+110 s")]
    lz.l2([(200, 540), (1720, 540)], ap(t, t0) * 0.6, 1.2)
    for i, (f, d) in enumerate(fechas):
        x = 300 + i * 440
        o = ap(t, t0 + 0.5 + i * 0.55)
        lz.c2(x, 540, 10, o, w=1.6, lleno=True)
        lz.texto(f, x, 470, 36, "Bold Condensed", o, "mm", esp=0.06)
        lz.texto(d, x, 600, 20, "SemiBold Condensed", o * 0.85, "mm", esp=0.12)
        oc = ap(t, ww("n1", 4, "falló") + i * 0.2)
        lz.l2([(x - 28, 680), (x + 28, 736)], oc, 3.0)
        lz.l2([(x - 28, 736), (x + 28, 680)], oc, 3.0)
    lz.texto("4 VUELOS · 4 FALLAS", W / 2, 880, 70, "Bold Condensed", ap(t, ww("n1", 4, "falló")), "mm", esp=0.05)
    cabecera(lz, "N1 · TODOS SUS LANZAMIENTOS", ap(t, t0))
    return lz


def n_vecinos(t):
    t0 = F0("n1", 7) - 0.3
    lz = vacio()
    tv = ww("n1", 7, "vecinos") - 0.6
    k = pr(t, ww("n1", 7, "cuando") - 0.2, tv + 0.8)
    base_n1(lz, 960, 520, 48, op=ap(t, t0), onda=(5, k), cruz=(5,))
    lz.texto("UN MOTOR FALLA… Y SE LLEVA A SUS VECINOS", W / 2, 960, 40, "Bold Condensed", ap(t, ww("n1", 7, "cuando")), "mm", esp=0.05)
    cabecera(lz, "EL VERDADERO PROBLEMA DEL N1", ap(t, t0))
    return lz


# ------------------------------------------------------------------ FALCON
def f_nueve(t):
    t0 = F0("falcon", 1) - 0.3
    lz = vacio()
    base_f9(lz, 960, 500, 150, op=ap(t, t0))
    lz.texto("FALCON 9 · 9 MOTORES MERLIN", W / 2, 900, 50, "Bold Condensed", ap(t, t0 + 0.2), "mm", esp=0.05)
    cabecera(lz, "VISTA DESDE ABAJO", ap(t, t0))
    return lz


def f_ocho(t):
    t0 = F0("falcon", 3) - 0.3
    lz = vacio()
    base_f9(lz, 620, 520, 140, op=ap(t, t0), cruz=(1,))
    o = ap(t, ww("falcon", 3, "ocho") - 0.1)
    lz.texto("8 DE 9", 1180, 380, 130, "Bold Condensed", o, "lm", esp=0.02)
    lz.texto("ARDEN MÁS TIEMPO", 1184, 460, 26, "SemiBold Condensed", o, "lm", esp=0.16)
    od = ap(t, ww("falcon", 3, "dragon") - 0.1)
    lz.texto("DRAGON LLEGA A LA ESTACIÓN", 1180, 600, 44, "Bold Condensed", od, "lm", esp=0.05)
    os_ = ap(t, F0("falcon", 4) - 0.1)
    lz.texto("SATÉLITE SECUNDARIO: PERDIDO", 1180, 690, 34, "Bold Condensed", os_, "lm", esp=0.05)
    lz.texto("ORBCOMM-OG2 · ÓRBITA INÚTIL", 1184, 734, 20, "SemiBold Condensed", os_ * 0.85, "lm", esp=0.16)
    lz.texto("MISIÓN PRINCIPAL: A SALVO", 1180, 840, 44, "Bold Condensed", ap(t, ww("falcon", 4, "misión") - 0.1), "lm", esp=0.05)
    cabecera(lz, "CRS-1 · 8 OCT 2012", ap(t, t0))
    return lz


def f_heavy(t):
    t0 = F0("falcon", 5) - 0.3
    def ex(lz, tt):
        o = ap(tt, ww("falcon", 5, "veintisiete") - 0.2)
        for j in range(3):
            base_f9(lz, 1340 + (j - 1) * 210, 470, 52, op=o)
        lz.texto("27", 1340, 690, 110, "Bold Condensed", o, "mm", esp=0.02)
        lz.texto("MOTORES A LA VEZ", 1340, 760, 24, "SemiBold Condensed", o, "mm", esp=0.18)
    return rp("fh", SEG["fh"], t0, "FALCON HEAVY · 6 FEB 2018", "TRES PRIMERAS ETAPAS", extra=ex)(t)


# ------------------------------------------------------------------ FALLAS (1.ª razón)
def r1(t):
    t0 = T0("fallas")
    lz = vacio()
    cr = (20,) if t > ww("fallas", 0, "perder") else ()
    panel33(lz, 620, 540, 66, op=ap(t, t0), cruz=cr, apagados=cr)
    lz.texto("RAZÓN 1", 1180, 360, 40, "SemiBold Condensed", ap(t, t0 + 0.2), "lm", esp=0.3)
    lz.texto("PERDER UNO", 1180, 450, 96, "Bold Condensed", ap(t, ww("fallas", 0, "perder") - 0.1), "lm", esp=0.03)
    lz.texto("NO ES EL FIN", 1180, 550, 96, "Bold Condensed", ap(t, ww("fallas", 0, "fin") - 0.2), "lm", esp=0.03)
    return lz


def r1_musk(t):
    t0 = F0("fallas", 1) - 0.3
    lz = vacio()
    lineas = [("SI LA FALLA DE UN MOTOR", "falla"), ("QUEDA AISLADA DE LOS DEMÁS", "aislada"), ("Y DEL CUERPO DEL COHETE,", "cuerpo"),
              ("MÁS MOTORES = MÁS CONFIABLE", "confiable")]
    for i, (txt, pal) in enumerate(lineas):
        o = ap(t, ww("fallas", 1, pal) - 0.25)
        lz.texto(txt, 1000, 330 + i * 92, 60 if i < 3 else 66, "Bold Condensed", o, "lm", esp=0.04)
    lz.texto("— ELON MUSK", 1004, 330 + 4 * 92, 28, "SemiBold Condensed", ap(t, ww("fallas", 1, "confiable")), "lm", esp=0.2)
    ol = ap(t, F0("fallas", 2) - 0.2)
    if ol > 0:
        lz.texto("LA LECCIÓN DEL N1", 1000, 900, 50, "Bold Condensed", ol, "lm", esp=0.05)
    return con_foto(lambda tt: lz, dict(nombre="musk", cx=520, cy=520, ancho=520, t0=t0 + 0.1, t1=T1("fallas") + 9,
                                       rotulo="ELON MUSK", sub="FOTO: COMMONS", estilo=1, asp=0.8, ancla=(520, 520)))(t)


def r1_31(t):
    t0 = F0("fallas", 4) - 0.3
    lz = vacio()
    k = ap(t, ww("fallas", 4, "arrancaron") - 0.1)
    apag = (17, 30) if t > ww("fallas", 4, "apagó") - 0.2 else ((17,) if t > ww("fallas", 4, "uno") else ())
    panel33(lz, 620, 540, 66, op=ap(t, t0), apagados=apag, cruz=apag)
    lz.texto("31 DE 33", 1180, 440, 130, "Bold Condensed", k, "lm", esp=0.02)
    lz.texto("9 FEB 2023 · BOOSTER 7", 1184, 520, 26, "SemiBold Condensed", k, "lm", esp=0.16)
    lz.texto("1 APAGADO A PROPÓSITO", 1184, 620, 30, "SemiBold Condensed", ap(t, ww("fallas", 4, "apagó") - 0.1), "lm", esp=0.12)
    lz.texto("1 SE DETUVO SOLO", 1184, 670, 30, "SemiBold Condensed", ap(t, ww("fallas", 4, "solo") - 0.2), "lm", esp=0.12)
    cabecera(lz, "PRIMER ENCENDIDO DE LOS 33", ap(t, t0))
    return lz


# ------------------------------------------------------------------ FÁBRICA (2.ª razón)
def fb_serie(t):
    """Uno gigante, a mano, contra muchos pequeños en una línea."""
    t0 = F0("fabrica", 1) - 0.3
    lz = vacio()
    o1 = ap(t, t0) * (1 - ap(t, F0("fabrica", 2) - 0.3))
    if o1 > 0:
        tobera2d(lz, 960, 520, 520, o1)
        lz.texto("UN MOTOR GIGANTE", 960, 140, 60, "Bold Condensed", o1, "mm", esp=0.05)
        lz.texto("UNO POR UNO · CADA ERROR CUESTA AÑOS", 960, 900, 30, "SemiBold Condensed", o1 * ap(t, ww("fabrica", 1, "error") - 0.2), "mm", esp=0.14)
    o2 = ap(t, F0("fabrica", 2) - 0.3)
    if o2 > 0:
        lz.l2([(80, 700), (1840, 700)], o2 * 0.7, 1.6)
        for j in range(12):
            x = (j * 170 + (t - F0("fabrica", 2)) * 160) % 2040 - 100
            tobera2d(lz, x, 600, 150, o2)
        for j in range(24):
            x = (j * 80 + (t * 160) % 80)
            lz.c2(x, 712, 6, o2 * 0.5, w=1.0)
        lz.texto("EN SERIE", 960, 260, 96, "Bold Condensed", o2, "mm", esp=0.04)
        lz.texto("COMO UNA LÍNEA DE AUTOS", 960, 330, 28, "SemiBold Condensed", ap(t, ww("fabrica", 2, "autos") - 0.3), "mm", esp=0.18)
        od = ap(t, F0("fabrica", 3) - 0.2)
        lz.texto("MÁS DE 1 RAPTOR AL DÍA", 960, 870, 64, "Bold Condensed", od, "mm", esp=0.05)
        lz.texto("FINALES DE 2022", 960, 930, 24, "SemiBold Condensed", od, "mm", esp=0.2)
    cabecera(lz, "RAZÓN 2 · LA FÁBRICA", ap(t, t0))
    return lz


def fb_curva(t):
    t0 = F0("fabrica", 5) - 0.3
    lz = vacio()
    gx, gy, gw, gh = 260, 820, 900, 520
    o = ap(t, t0)
    lz.l2([(gx, gy - gh), (gx, gy), (gx + gw, gy)], o * 0.8, 1.2)
    lz.texto("MOTORES FABRICADOS", gx + gw, gy + 40, 20, "SemiBold Condensed", o, "rm", esp=0.16)
    lz.texto("COSTO POR MOTOR", gx, gy - gh - 30, 20, "SemiBold Condensed", o, "lm", esp=0.16)
    k = pr(t, t0 + 0.3, ww("fabrica", 5, "barato") + 0.6)
    pts = [(gx + gw * u, gy - gh * (0.12 + 0.85 / (1 + 7 * u))) for u in np.linspace(0, k, int(160 * k) + 2)]
    lz.l2(pts, o, 2.0)
    lz.texto("ESQUEMA", gx + gw, gy - gh, 18, "Light Condensed", o * 0.7, "rm", esp=0.2)
    o1 = ap(t, ww("fabrica", 5, "tierra") - 0.2)
    o2 = ap(t, ww("fabrica", 5, "aire") - 0.2)
    lz.texto("FALLA EN TIERRA", 1300, 420, 50, "Bold Condensed", o1, "lm", esp=0.05)
    lz.texto("= UNA LECCIÓN", 1300, 480, 36, "SemiBold Condensed", o1, "lm", esp=0.1)
    lz.texto("FALLA EN EL AIRE", 1300, 620, 50, "Bold Condensed", o2, "lm", esp=0.05)
    lz.texto("= UNA CATÁSTROFE", 1300, 680, 36, "SemiBold Condensed", o2, "lm", esp=0.1)
    return lz


# ------------------------------------------------------------------ montaje 2
PLANOS = [
    (T0("n1"), con_foto(rp("n1b", SEG["n1b_desp"], T0("n1"), "URSS · EL CAMINO CONTRARIO", "COHETE LUNAR N1", zoom=1.45, cy=0.38),
                        dict(nombre="n1_pad", cx=1500, cy=470, ancho=380, t0=ww("n1", 0, "soviéticos"), t1=F0("n1", 1) - 0.2,
                             rotulo="N1 EN BAIKONUR, 1967", sub="FOTO: DOMINIO PÚBLICO", estilo=0, asp=0.62))),
    (F0("n1", 1) - 0.3, n_base),
    (F0("n1", 4) - 0.3, n_cuatro),
    (F0("n1", 5) - 0.3, rp("n1b", SEG["n1_expl"], F0("n1", 5) - 0.3, "3 JUL 1969", "LA BOMBA DE OXÍGENO DE UN MOTOR EXPLOTA", zoom=1.45, cy=0.38)),
    (F0("n1", 6) - 0.3, rp("n1b", SEG["n1_ruina"], F0("n1", 6) - 0.3, "CAE SOBRE SU PLATAFORMA", "RECONSTRUIRLA: 18 MESES", zoom=1.45, cy=0.38)),
    (F0("n1", 7) - 0.3, n_vecinos),
    (T0("falcon"), rp("crs1", SEG["crs1_desp"], T0("falcon"), "FALCON 9", "SPACEX · 2012")),
    (F0("falcon", 1) - 0.3, f_nueve),
    (F0("falcon", 2) - 0.3, rp("crs1", SEG["crs1_flash"] - (ww("falcon", 2, "setenta") - F0("falcon", 2) + 0.3), F0("falcon", 2) - 0.3,
                               "CRS-1 · 8 OCT 2012", "UN MOTOR SE APAGA A LOS 79 s")),
    (F0("falcon", 3) - 0.3, f_ocho),
    (F0("falcon", 5) - 0.3, con_foto(f_heavy, dict(nombre="fh", cx=440, cy=470, ancho=560, t0=F0("falcon", 5) + 0.5, t1=T1("falcon") + 0.3,
                                                    rotulo="FALCON HEAVY", sub="FOTO: SPACEX · CC0", estilo=2, asp=1.5))),
    (T0("fallas"), r1),
    (F0("fallas", 1) - 0.3, r1_musk),
    (F0("fallas", 3) - 0.3, rp("b7", SEG["b7_amplia"], F0("fallas", 3) - 0.3, "9 FEB 2023 · BOOSTER 7", "PRUEBA ESTÁTICA · LOS 33 A LA VEZ")),
    (F0("fallas", 4) - 0.3, r1_31),
    (F0("fallas", 5) - 0.3, rp("b7", SEG["b7_tuit"], F0("fallas", 5) - 0.3, "«AÚN BASTAN PARA LLEGAR A ÓRBITA»", "ELON MUSK", cy=0.4)),
    (T0("fabrica"), rp("fabrica", SEG["fab"], T0("fabrica"), "RAZÓN 2", "LA FÁBRICA")),
    (F0("fabrica", 1) - 0.3, fb_serie),
    (F0("fabrica", 4) - 0.3, rp("r3", SEG["r3_banco"], F0("fabrica", 4) - 0.3, "McGREGOR, TEXAS", "BANCO DE PRUEBAS · RAPTOR 3")),
    (F0("fabrica", 5) - 0.3, fb_curva),
]


def sfx():
    return [(T0("n1"), "whoosh", 0.6, 0.0, None), (ww("n1", 2, "fallaba"), "alarma", 0.5, -0.3, None),
            (ww("n1", 2, "opuesto"), "apagado", 0.5, 0.3, None), (ww("n1", 4, "falló"), "sello", 0.7, 0.0, None),
            (F0("n1", 5), "explosion", 0.9, 0.0, None), (F0("n1", 7), "explosion", 0.4, 0.0, None),
            (F0("falcon", 1), "hud", 0.6, 0.0, None), (ww("falcon", 2, "setenta"), "alarma", 0.6, 0.0, None),
            (F0("falcon", 5), "rugido", 0.7, 0.0, None), (T0("fallas"), "pulso", 0.8, 0.0, None),
            (F0("fallas", 3), "rugido", 0.7, 0.0, None), (ww("fallas", 4, "arrancaron"), "tic", 0.6, 0.0, None),
            (T0("fabrica"), "pulso", 0.7, 0.0, None), (F0("fabrica", 2), "fabrica", 0.6, 0.0, None),
            (F0("fabrica", 4), "ignicion", 0.6, 0.0, None), (ww("fabrica", 5, "catástrofe"), "explosion", 0.4, 0.0, None)]
