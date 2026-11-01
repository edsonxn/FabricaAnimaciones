# -*- coding: utf-8 -*-
"""Toma 4 «orbita» (82:9-133:1 s): ¿dónde la ponemos? Zoom-out a la esfera de Hill (1,5 millones de km) con el Sol que
tira desde la izquierda, la mitad estable, dos lunas en órbitas parecidas que se estorban (choque / eyección), recuadro de
Saturno con Jano y Epimeteo que se intercambian la órbita, y el punto de equilibrio L4 con la segunda luna persiguiendo a la
primera (este encuadre se reutiliza en la toma 9, «choque»: `escena_L4`)."""
import math

import numpy as np

import plano as P
import kz_espacio as K
from plano import mezcla, aclarar, oscurecer
from motor import W, H, prog, clamp01, lerp, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, smooth, h01
from mundo_comun import Cam, kf, pop, ventana, campana
from anclas import A
import mundo_espacio as ME
import mundo_origen as MO
from mundo_espacio import (ER, RL, MR, HILL, LUZ, AZUL, ORO, TINTA, MENTA, ROSA, ang_luna, luna_mundo, radio_luna1, chip,
                           fantasma, marca_x, bez2, trail, kuri_ui, T_LUNA1, PHI_A)

ROJO = (255, 96, 120)

# ---------------------------------------------------------------- helpers de dibujo con tamaño mínimo
def tierra_r(lz, t, E, r, lunas=(), amp=0.0):
    K.tierra_marea(lz, E[0], E[1], r, t, list(lunas), rot=0.45 * t, ang_luz=LUZ, amp=amp)


def luna_r(lz, p, r, t, tipo="luna", seed=1, alfa=1.0, rot=None):
    K.cuerpo_rocoso(lz, p[0], p[1], r, tipo, seed=seed, ang_luz=LUZ, rot=0.07 * t + seed if rot is None else rot, alfa=alfa)


def anillo_poly(x, y, r0, r1, n=120):
    th = np.linspace(0, 2 * np.pi, n)
    o = np.stack([x + r1 * np.cos(th), y + r1 * np.sin(th)], 1)
    i = np.stack([x + r0 * np.cos(th), y + r0 * np.sin(th)], 1)
    return np.vstack([o, o[:1], i[::-1], i[-1:]])


# ---------------------------------------------------------------- la segunda luna en cada tramo
T_COL = A.chocan + 0.05                       # choque de las dos lunas
T_REPLAY = A.disparada - 0.55                 # «o una sale disparada»
HOPS = [(A.donde_o - 0.1, A.donde_o + 0.5, np.array([1000.0, -650.0])),
        (A.donde_o + 1.0, A.donde_o + 1.5, np.array([-1100.0, 420.0])),
        (A.sitio - 0.2, A.sitio + 0.3, np.array([520.0, 620.0]))]


def luna2_ghost(t):
    """Posición de la 2.ª luna como fantasma que salta de sitio en sitio (mundo)."""
    p_prev = MO.luna_joven_2(HOPS[0][0])
    for (a, b, q) in HOPS:
        if t < a:
            return p_prev
        if t <= b:
            return p_prev + (q - p_prev) * e_inout(prog(t, a, b))
        p_prev = q
    return p_prev


def pos_gemela(t):
    """La 2.ª luna de la escena de choque: órbita 780 -> 740, se acerca (por detrás de la Luna)."""
    d = float(kf(t, [(A.lunas_o, 1.35), (T_COL, 0.05)], ease=lambda x: x ** 1.2))
    r2 = float(kf(t, [(A.lunas_o, 790.0), (A.tira_o, 770.0), (T_COL, 718.0)]))
    th = ang_luna(t) + d
    return np.array(K.pos_orbita(0, 0, r2, r2, 0, th))


def pos_luna_choque(t):
    r1 = float(kf(t, [(A.lunas_o, 700.0), (A.tira_o, 708.0), (T_COL, 716.0)]))
    return np.array(K.pos_orbita(0, 0, r1, r1, 0, ang_luna(t)))


# ---------------------------------------------------------------- Jano y Epimeteo (Saturno)
PAN2 = dict(cx=960.0, cy=520.0, w=1500.0, h=860.0)
T_J0, T_J1 = A.excepcion - 0.8, A.cuatro_anos + 1.3
SAT = (-210.0, -10.0)          # Saturno (local del recuadro)
R_IN, R_OUT = 335.0, 390.0
_DT = 0.01
_TS = np.arange(T_J0, T_J1 + 0.5, _DT)


def _integra():
    n = len(_TS)
    ra = np.zeros(n)
    rb = np.zeros(n)
    th_a = np.zeros(n)
    th_b = np.zeros(n)
    th_a[0], th_b[0] = 0.0, 1.55
    for i in range(n):
        t = _TS[i]
        s = e_inout(prog(t, A.intercambian - 0.9, A.intercambian + 0.5))
        ra[i] = lerp(R_IN, R_OUT, s)
        rb[i] = lerp(R_OUT, R_IN, s)
        if i + 1 < n:
            th_a[i + 1] = th_a[i] + _DT * 1.15 * (R_IN / ra[i]) ** 1.5
            th_b[i + 1] = th_b[i] + _DT * 1.15 * (R_IN / rb[i]) ** 1.5
    return ra, rb, th_a, th_b


_RA, _RB, _THA, _THB = _integra()


def jano_pos(t):
    return (float(np.interp(t, _TS, _RA)), float(np.interp(t, _TS, _THA))), (float(np.interp(t, _TS, _RB)), float(np.interp(t, _TS, _THB)))


def inset_saturno(lz, t):
    k = pop(t, T_J0 + 0.2, 0.5) * (1 - e_in(prog(t, A.cuatro_anos + 0.9, A.cuatro_anos + 1.3)))
    if k < 0.02:
        return 0.0
    cx, cy, w, h = PAN2["cx"], PAN2["cy"], PAN2["w"], PAN2["h"]
    q = rect_red(-w / 2, -h / 2, w, h, 46)
    with lz.capa(2):
        with lz.grupo(cx, cy, k):
            lz.relleno(q, (16, 16, 54), alfa=0.97)
            with lz.recorte(q):
                for i in range(26):
                    lz.relleno(circulo(-w / 2 + w * h01(i, 1, 9), -h / 2 + h * h01(i, 2, 9), 2.2 + 2 * h01(i, 3, 9), 8),
                               (230, 235, 255), alfa=0.7)
                K.nebulosa(lz, 300, 100, 480, (110, 80, 210), seed=4, alfa=0.35, capa=2)
                sx, sy = SAT
                K.anillo(lz, sx, sy, 190, 285, tilt=-0.22, incl=0.28, mitad=0, col=(226, 204, 150))
                K.planeta_gas(lz, sx, sy, 150, t, "saturno", seed=2)
                K.anillo(lz, sx, sy, 190, 285, tilt=-0.22, incl=0.28, mitad=1, col=(226, 204, 150))
                th_ = np.linspace(0, 2 * np.pi, 150)
                for rr, col in ((R_IN, (255, 214, 90)), (R_OUT, MENTA)):
                    P.discontinua(lz, np.stack([sx + rr * np.cos(th_), sy + rr * np.sin(th_)], 1), col, 3.0, 12, 10, fase=-t * 24)
                (ra, tha), (rb, thb) = jano_pos(t)
                pa = np.array([sx + ra * math.cos(tha), sy + ra * math.sin(tha)])
                pb = np.array([sx + rb * math.cos(thb), sy + rb * math.sin(thb)])
                kj = pop(t, A.jano - 0.1, 0.35)
                ke = pop(t, A.epimeteo - 0.1, 0.35)
                K.roca(lz, pa[0], pa[1], 28 * kj, seed=3, rot=t * 1.2, tipo="ceniza", ang_luz=LUZ, alargada=1.2)
                K.roca(lz, pb[0], pb[1], 20 * ke, seed=8, rot=-t * 1.4, tipo="mercurio", ang_luz=LUZ, alargada=1.2)
                # etiquetas (siguen a cada luna mientras la narración las nombra)
                lj = e_out(prog(t, A.jano, A.jano + 0.5)) * (1 - e_in(prog(t, A.alcanza - 0.2, A.alcanza + 0.2)))
                le = e_out(prog(t, A.epimeteo, A.epimeteo + 0.5)) * (1 - e_in(prog(t, A.alcanza - 0.2, A.alcanza + 0.2)))
                if lj > 0.01:
                    K.etiqueta(lz, pa[0], pa[1], "Jano", dx=(120 if pa[0] < 200 else -120), dy=(90 if pa[1] < 0 else -90), px=38, frac=lj)
                if le > 0.01:
                    K.etiqueta(lz, pb[0], pb[1], "Epimeteo", dx=(130 if pb[0] < 200 else -130), dy=(-95 if pb[1] > 0 else 95), px=38, frac=le)
                ls = e_out(prog(t, A.saturno, A.saturno + 0.5))
                if ls > 0.01:
                    P.pastilla(lz, sx, sy - 215, "Saturno", px=36, k=ls * (1 - e_in(prog(t, A.comparten, A.comparten + 0.3))),
                               fondo=(255, 236, 170), color=TINTA)
                # el intercambio: flechas ⇄ entre las dos órbitas
                ki = ventana(t, A.intercambian - 0.2, A.intercambian + 1.6, 0.25, 0.3)
                if ki > 0.02:
                    mid = (R_IN + R_OUT) / 2
                    a_c = (tha + thb) / 2
                    cxp, cyp = sx + mid * math.cos(a_c), sy + mid * math.sin(a_c)
                    nrm = np.array([math.cos(a_c), math.sin(a_c)])
                    K.flecha(lz, np.array([cxp, cyp]) - nrm * 6, np.array([cxp, cyp]) + nrm * 70, ORO, ancho=7, alfa=ki, frac=ki)
                    K.flecha(lz, np.array([cxp, cyp]) + nrm * 6, np.array([cxp, cyp]) - nrm * 70, ORO, ancho=7, alfa=ki, frac=ki)
                    P.pastilla(lz, 430, -200, "se intercambian la órbita", px=36, k=ki, fondo=ORO, color=TINTA)
                # años
                for i, an in enumerate(("2006", "2010", "2014", "2018", "2022")):
                    ka = pop(t, A.cuatro_anos - 0.2 + 0.18 * i, 0.3)
                    if ka > 0.01:
                        P.pastilla(lz, -300 + 170 * i, 385, an, px=34, k=ka, fondo=(255, 255, 255), color=TINTA)
                kc = e_out(prog(t, A.cuatro_anos - 0.3, A.cuatro_anos + 0.3))
                if kc > 0.01:
                    P.pastilla(lz, 430, 290, "cada 4 años", px=44, k=kc, fondo=MENTA, color=TINTA)
            lz.trazo(np.vstack([q, q[:1]]), (255, 255, 255), 5.0, afinar=False, temblor=0.0)
    return k


# ---------------------------------------------------------------- la toma
def toma_4(lz, t, cam):
    z = cam.z
    E = cam.a_pant((0, 0))
    r_e = max(ER * z, 22.0)
    r_m = max(MR * z, 13.0)
    pm_w = luna_mundo(t)
    # ------------------------------------------------ fondo: el Sol (de ahí viene el tirón)
    ks = e_out(prog(t, A.mas_alla - 0.4, A.mas_alla + 0.6)) * (1 - e_in(prog(t, 98.7, 99.9)))
    if ks > 0.01:
        x_s = lerp(-700, -60, ks)
        P.sol(lz, x_s, 560, 330, t, brillo=1.0)
        ksl = e_out(prog(t, A.sol_o, A.sol_o + 0.4)) * ks
        P.pastilla(lz, 330, 330, "Sol", px=44, k=ksl, fondo=(255, 226, 150), color=TINTA)
    R = HILL * z
    # ------------------------------------------------ esfera de Hill
    if A.hasta - 0.5 < t < A.lunas_o + 0.4:
        kh = e_out(prog(t, A.hasta - 0.5, A.hasta + 1.0)) * (1 - e_in(prog(t, A.lunas_o - 0.2, A.lunas_o + 0.5)))
        if kh > 0.01:
            K.esfera_hill(lz, E[0], E[1], R * kh, t, alfa=kh)
            lh = e_out(prog(t, A.gravedad, A.gravedad + 0.6)) * (1 - e_in(prog(t, A.seguras - 0.2, A.seguras + 0.3)))
            if lh > 0.01:
                P.pastilla(lz, E[0], E[1] - R - 56, "hasta aquí manda la Tierra", px=38, k=lh, fondo=(190, 210, 255), color=TINTA)
            # regla de 1,5 millones de km
            fr = e_inout(prog(t, A.millon - 0.3, A.millon + 1.4)) * (1 - e_in(prog(t, A.seguras - 0.3, A.seguras + 0.2)))
            if fr > 0.01:
                p0 = np.array([E[0], E[1] + R * 0.42])
                p1 = np.array([E[0] + R, E[1] + R * 0.42])
                for p in (p0, p1):
                    pass
                K.regla(lz, p0, p1, "1,5 millones de km", px=38, frac=fr, lado=-1)
    # ------------------------------------------------ mitad segura
    if A.seguras - 0.3 < t < A.lunas_o + 0.3:
        km = e_out(prog(t, A.seguras, A.seguras + 0.9)) * (1 - e_in(prog(t, A.lunas_o - 0.2, A.lunas_o + 0.3)))
        if km > 0.01:
            lz.relleno(anillo_poly(E[0], E[1], R * 0.5, R * 0.98), ROJO, alfa=0.13 * km)
            lz.relleno(circulo(E[0], E[1], R * 0.5, 120), MENTA, alfa=0.10 * km)
            th_ = np.linspace(0, 2 * np.pi, 160)
            P.discontinua(lz, np.stack([E[0] + R * 0.5 * np.cos(th_), E[1] + R * 0.5 * np.sin(th_)], 1), MENTA, 4.0, 18, 12,
                          fase=t * 28, frac=km)
            P.pastilla(lz, E[0], E[1] - R * 0.5 - 50, "órbitas estables", px=38, k=km, fondo=MENTA, color=TINTA)
            P.pastilla(lz, E[0] + R * 0.74, E[1] - R * 0.6, "inestable", px=36, k=km, fondo=ROSA, color=TINTA)
            kmi = e_out(prog(t, A.mitad, A.mitad + 0.4)) * km
            P.pastilla(lz, E[0] + R * 0.5 * 0.71, E[1] - R * 0.5 * 0.71 - 46, "½", px=44, k=kmi, fondo=(255, 255, 255), color=TINTA)
    # ------------------------------------------------ restos del anillo de escombros (se desvanecen al abrir la cámara)
    if t < 83.4:
        MO.escombros(lz, cam, t)
    # ------------------------------------------------ órbita de la Luna
    r_o = radio_luna1(t) if t < 100 else 700.0
    K.orbita(lz, E[0], E[1], r_o * z, r_o * z, 0, AZUL, 3.0, alfa=0.5, fase=t * 26)
    # ------------------------------------------------ Tierra
    tierra_r(lz, t, E, r_e, [], 0.0)
    # ------------------------------------------------ cuerpos según el tramo
    mp = cam.a_pant(pm_w)
    if A.lunas_o - 0.4 < t < T_COL + 0.05:
        pm_w = pos_luna_choque(t)
        mp = cam.a_pant(pm_w)
    # --- (1) 2.ª luna joven -> fantasma que salta de sitio
    if t < A.segunda + 3.6:
        t_g = HOPS[0][0]
        if t < t_g:
            p2 = cam.a_pant(MO.luna_joven_2(t))
            k2 = 1.0
            luna_r(lz, p2, r_m * 1.0, t, "ceniza", 5, rot=0.07 * t + 5)
        else:
            p2 = cam.a_pant(luna2_ghost(t))
            kg = 1 - e_in(prog(t, A.sitio + 0.6, A.sitio + 1.2))
            if kg > 0.01:
                luna_r(lz, p2, max(MR * z, 13.0), t, "ceniza", 5, alfa=0.45 * kg)
                fantasma(lz, p2[0], p2[1], max(MR * z, 13.0) * 1.15, t, alfa=kg)
                P.rotulo(lz, p2[0], p2[1] - max(MR * z, 13.0) - 54, "?", px=100, color=ORO, alfa=kg)
        # ✗ en los sitios descartados
        for i, (a_, b_, q) in enumerate(HOPS):
            t_x = a_ if i < len(HOPS) - 1 else b_
            t_x = HOPS[i + 1][0] if i + 1 < len(HOPS) else b_ + 0.3
            if t > t_x:
                kx = pop(t, t_x, 0.3) * (1 - e_in(prog(t, A.sitio + 0.6, A.sitio + 1.1)))
                qx = cam.a_pant(q)
                marca_x(lz, qx[0], qx[1], 1.0, kx)
        chip(lz, t, 340, 90, "¿Dónde la ponemos?", A.segunda - 0.15, A.sitio + 1.3, 42, MENTA)
    # --- (2) caída del Sol: cuerpo fuera de Hill que se va
    if A.mas_alla - 0.2 < t < A.mitad:
        u = prog(t, A.mas_alla - 0.2, A.lleva + 0.7)
        ang = lerp(-0.35, -2.6, e_in(u))
        rr = R * lerp(1.22, 1.55, u)
        pb = np.array([E[0] + rr * math.cos(ang), E[1] + rr * math.sin(ang)])
        kb = (1 - e_in(prog(t, A.lleva + 0.5, A.lleva + 1.0))) * e_out(prog(t, A.mas_alla - 0.2, A.mas_alla + 0.1))
        if kb > 0.01 and -60 < pb[0] < W + 60 and -60 < pb[1] < H + 60:
            fb = lambda tt: np.array([E[0] + R * lerp(1.22, 1.55, prog(tt, A.mas_alla - 0.2, A.lleva + 0.7)) *  # noqa: E731
                                      math.cos(lerp(-0.35, -2.6, e_in(prog(tt, A.mas_alla - 0.2, A.lleva + 0.7)))),
                                      E[1] + R * lerp(1.22, 1.55, prog(tt, A.mas_alla - 0.2, A.lleva + 0.7)) *
                                      math.sin(lerp(-0.35, -2.6, e_in(prog(tt, A.mas_alla - 0.2, A.lleva + 0.7))))])
            trail(lz, fb, t, dur=0.7, n=16, color=(255, 214, 90), ancho=8 * kb)
            luna_r(lz, pb, 24 * kb, t, "ceniza", 5)
            K.flecha(lz, pb + np.array([-30.0, 40.0]), pb + np.array([-190.0, 80.0]), (255, 226, 150), ancho=8, alfa=0.9 * kb)
    # --- (3) la Luna de hoy
    luna_r(lz, mp, r_m, t, "luna", 1)
    # --- (4) dos lunas: tirón, choque, eyección
    if A.lunas_o - 0.3 < t < A.disparada + 2.0:
        toma_estorban(lz, t, cam, E, r_m)
    # --- Jano y Epimeteo (recuadro)
    if T_J0 - 0.3 < t < A.cuatro_anos + 1.6:
        dim = e_inout(prog(t, T_J0, T_J0 + 0.5)) * (1 - e_inout(prog(t, A.cuatro_anos + 0.8, A.cuatro_anos + 1.4)))
        if dim > 0.01:
            lz.relleno(rect_red(-10, -10, W + 20, H + 20, 0), (10, 10, 40), alfa=0.55 * dim, capa=2)
        inset_saturno(lz, t)
    # --- L4
    if t > A.escondite - 0.6:
        toma_L4(lz, t, cam, E, r_m)
    # --- Kuri
    pos_k = (1760, 935)
    if t < 100:
        tgt = E
    else:
        tgt = E
    head = np.array([pos_k[0], pos_k[1] - 90])
    d = np.asarray(tgt, float) - head
    mirar = tuple(d / max(1.0, float(np.hypot(*d))) * 0.9)
    kuri_ui(lz, t, pos_k[0], pos_k[1], 1.0, mirar, boca=campana(t, T_COL - 0.2, T_COL + 1.0),
            feliz=1.0 if (A.excepcion < t < A.alcanza - 1.0) else 0.0)


def toma_estorban(lz, t, cam, E, r_m):
    z = cam.z
    if t < T_COL + 0.05:
        k2 = pop(t, A.lunas_o - 0.1, 0.4)
        p2 = cam.a_pant(pos_gemela(t))
        pm = cam.a_pant(pos_luna_choque(t))
        luna_r(lz, p2, r_m * k2, t, "ceniza", 5)
        kd = campana(t, A.lunas_o - 0.15, A.lunas_o + 0.8)
        if kd > 0.01:
            K.destello(lz, p2[0], p2[1], 80 * kd, t, alfa=min(1.0, kd * 1.5))
        # tirón: flechas de la una hacia la otra
        kt = ventana(t, A.tira_o, T_COL - 0.1, 0.25, 0.1)
        if kt > 0.02:
            d = p2 - pm
            n = max(1.0, float(np.hypot(*d)))
            u = d / n
            K.flecha(lz, pm + u * r_m * 1.2, pm + u * (r_m * 1.2 + 60 * kt), ORO, ancho=8, alfa=kt)
            K.flecha(lz, p2 - u * r_m * 1.2, p2 - u * (r_m * 1.2 + 60 * kt), ORO, ancho=8, alfa=kt)
        # estorban: aviso
        ke = ventana(t, A.estorban, A.tira_o - 0.2, 0.3, 0.3)
        if ke > 0.02:
            P.pastilla(lz, E[0], E[1] - 410 * z / 0.62 * 0.62 - 90, "se estorban", px=42, k=ke, fondo=ROSA, color=TINTA)
    # choque
    if T_COL - 0.05 < t < T_COL + 1.9:
        pc = cam.a_pant(pos_luna_choque(T_COL))
        k = campana(t, T_COL - 0.05, T_COL + 1.0)
        lz.halo(pc[0], pc[1], 260 * k, (255, 230, 170), alfa=0.85 * k, r0=0.0)
        K.destello(lz, pc[0], pc[1], 80 * k, t, alfa=min(1.0, k * 1.4))
        for j in range(2):
            uu = prog(t, T_COL + 0.1 * j, T_COL + 1.3 + 0.1 * j)
            if 0 < uu < 1:
                P.onda(lz, pc[0], pc[1], 40 + 380 * e_out(uu), 8.0, (255, 214, 150), alfa=0.7 * (1 - uu))
        for i in range(22):
            a = h01(i, 1, 5) * 6.2832
            v = 150 + 330 * h01(i, 2, 5)
            dt = t - T_COL
            if dt < 0:
                continue
            r = v * (1 - math.exp(-dt * 1.8)) / 1.8
            q = pc + np.array([math.cos(a), math.sin(a)]) * r
            rad = (5 + 7 * h01(i, 3, 5)) * (1 - 0.5 * prog(dt, 0.0, 1.8))
            if rad > 1:
                lz.relleno(circulo(q[0], q[1], rad, 8), mezcla((255, 190, 120), (170, 160, 186), prog(dt, 0, 1.2)),
                           alfa=1 - 0.6 * prog(dt, 1.0, 1.9))
        # chip «o»
    ko = pop(t, A.disparada - 1.35, 0.35) * (1 - e_in(prog(t, A.disparada + 0.8, A.disparada + 1.1)))
    if ko > 0.01:
        P.pastilla(lz, E[0], E[1] - 500 * z, "o…", px=60, k=ko, fondo=(255, 255, 255), color=TINTA)
    # la que sale disparada: sale tangente a la órbita y se va
    if A.disparada - 0.6 < t < A.disparada + 2.0:
        t0 = A.disparada - 0.55
        kk = pop(t, t0, 0.35)
        th_d = ang_luna(A.disparada) + 0.14

        def f(tt):
            if tt <= A.disparada:
                return cam.a_pant(np.array(K.pos_orbita(0, 0, 700.0, 700.0, 0, ang_luna(tt) + 0.14)))
            d_ = tt - A.disparada
            return cam.a_pant(np.array(K.pos_orbita(0, 0, 700.0, 700.0, 0, th_d))
                              + np.array([-math.sin(th_d), math.cos(th_d)]) * 760 * d_
                              + np.array([math.cos(th_d), math.sin(th_d)]) * 520 * d_ * d_)
        q = f(t)
        if t > A.disparada:
            trail(lz, f, t, dur=0.6, n=14, color=(255, 214, 90), ancho=11)
        if -80 < q[0] < W + 80 and -80 < q[1] < H + 80:
            luna_r(lz, q, r_m * kk, t, "ceniza", 5)


def toma_L4(lz, t, cam, E, r_m, fade=1.0):
    z = cam.z
    th = ang_luna(t)
    pm = cam.a_pant(luna_mundo(t))
    p4 = cam.a_pant(np.array(K.pos_orbita(0, 0, 700.0, 700.0, 0, th + math.pi / 3)))
    p5 = cam.a_pant(np.array(K.pos_orbita(0, 0, 700.0, 700.0, 0, th - math.pi / 3)))
    # marcas L4 y L5
    k4 = pop(t, A.equilibrio, 0.4) * fade
    k5 = pop(t, A.detras - 0.1, 0.4) * fade
    # triángulo y 60°
    u_tri = e_inout(prog(t, A.sesenta - 0.1, A.sesenta + 0.9)) * fade
    if u_tri > 0.01:
        K.triangulo_equilibrio(lz, E, pm, p4, t, frac=u_tri)
        if u_tri > 0.95:
            arc = P.arco_pts(E[0], E[1], 95, th, th + math.pi / 3, 24)
            lz.trazo(np.asarray(arc), ORO, 5.0, afinar=False, temblor=0.0)
            am = th + math.pi / 6
            P.pastilla(lz, E[0] + 150 * math.cos(am), E[1] + 150 * math.sin(am), "60°", px=38, k=min(1.0, (u_tri - 0.95) * 20),
                       fondo=ORO, color=TINTA)
    if k4 > 0.01:
        K.punto_lagrange(lz, p4[0], p4[1], "L4", t, s=k4)
    if k5 > 0.01:
        K.punto_lagrange(lz, p5[0], p5[1], "L5", t, s=k5)
    # fuerzas que se compensan
    kf_ = ventana(t, A.ahi - 0.1, A.segunda_luna - 0.2, 0.3, 0.4) * fade
    if kf_ > 0.02:
        dE = E - p4
        dM = pm - p4
        uE = dE / max(1.0, float(np.hypot(*dE)))
        uM = dM / max(1.0, float(np.hypot(*dM)))
        K.flecha(lz, p4, p4 + uE * 150 * kf_, (110, 190, 255), ancho=8, alfa=kf_)
        K.flecha(lz, p4, p4 + uM * 75 * kf_, (255, 255, 255), ancho=8, alfa=kf_)
        res = uE * 150 + uM * 75
        K.flecha(lz, p4, p4 + res * 0.75 * kf_, ORO, ancho=10, alfa=kf_)
        P.pastilla(lz, p4[0] + 140, p4[1] - 100, "se compensan", px=38, k=e_out(prog(t, A.compensan, A.compensan + 0.4)) * kf_,
                   fondo=ORO, color=TINTA)
    # la segunda luna se queda en L4
    k2 = pop(t, A.segunda_luna - 0.1, 0.45)
    if k2 > 0.01:
        f2 = lambda tt: cam.a_pant(np.array(K.pos_orbita(0, 0, 700.0, 700.0, 0, ang_luna(tt) + math.pi / 3)))  # noqa: E731
        if t > A.persiguiendo - 0.2:
            trail(lz, f2, t, dur=0.9, n=18, color=(190, 205, 255), ancho=10)
        luna_r(lz, p4, r_m * k2, t, "ceniza", 5)
        kd = campana(t, A.segunda_luna - 0.15, A.segunda_luna + 0.9)
        if kd > 0.01:
            K.destello(lz, p4[0], p4[1], 90 * kd, t, alfa=min(1.0, kd * 1.5))
    # cadena: persiguiendo sin alcanzarla
    kc = ventana(t, A.persiguiendo, A.jamas + 1.2, 0.3, 0.4) * fade
    if kc > 0.02:
        a_mid = th + math.pi / 6
        rr = 700.0 * z * 1.07
        arc = P.arco_pts(E[0], E[1], rr, th + 0.12, th + math.pi / 3 - 0.12, 22)
        lz.trazo(np.asarray(arc), (255, 255, 255), 4.0, afinar=False, temblor=0.0)
        P.pastilla(lz, E[0] + (rr + 56) * math.cos(a_mid), E[1] + (rr + 56) * math.sin(a_mid), "siempre 60°", px=36, k=kc,
                   fondo=(255, 255, 255), color=TINTA)
