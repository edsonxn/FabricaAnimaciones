# -*- coding: utf-8 -*-
"""Toma 3 «origen» (41:45-82:9 s): ¿de dónde sacamos otra Luna? (a) captura (asteroide que se queda, Tritón, casi todo
sigue de largo), (b) mini-luna 2024 PT5 (un lazo y se va), (c) choque gigante: escombros -> anillo -> dos lunas.
Cámara: Tierra a la izquierda (0,0) del mundo; las trayectorias están en coordenadas del mundo."""
import math

import numpy as np

import plano as P
import kz_espacio as K
from plano import mezcla, aclarar, oscurecer
from motor import W, H, prog, clamp01, lerp, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, smooth, h01
from mundo_comun import Cam, kf, pop, ventana, campana
from anclas import A
import mundo_espacio as ME
from mundo_espacio import (ER, RL, MR, LUZ, AZUL, ORO, TINTA, MENTA, ROSA, LIN, ang_luna, luna_mundo, radio_luna1,
                           chip, fantasma, marca_x, bez2, kepler, trail, kuri_ui, T_LUNA1, PHI_A)

# ---------------------------------------------------------------- (a) captura
MU = 3.88e7                        # «gravedad» del dibujo (px³/s²)
Q_CAP, E_CAP = 190.0, 0.30
A_CAP = Q_CAP / (1 - E_CAP)
N_CAP = math.sqrt(MU / A_CAP ** 3)
T_CAP = A.atrapa - 0.9             # el asteroide pasa por el periapsis y se queda
D_ENT = 2.1                        # duración del acercamiento
S_CAP = np.array([1050.0, -720.0])
C_CAP = np.array([Q_CAP, -700.0])
P2_CAP = np.array([Q_CAP, 0.0])


def roca_cap(t):
    if t < T_CAP:
        return bez2(S_CAP, C_CAP, P2_CAP, prog(t, T_CAP - D_ENT, T_CAP))
    return kepler(A_CAP, E_CAP, 0.0, N_CAP * (t - T_CAP))


# pasos «sigue de largo»: (ángulo de entrada, desvío del ángulo de salida, distancia mínima, tiempo de inicio, duración, radio)
PASOS = [(0.35, 0.30, 330, 0.00, 2.0, 15), (-1.00, -0.25, 270, 0.40, 2.0, 11), (2.70, 0.40, 400, 0.80, 2.2, 18),
         (1.35, 0.20, 300, 1.15, 1.9, 12), (-2.30, 0.35, 360, 1.55, 2.1, 14), (0.75, -0.30, 430, 1.95, 2.0, 10),
         (3.05, 0.10, 280, 2.30, 2.0, 13)]
T_PASOS = A.dificilisimo - 0.9


def roca_paso(i, t):
    a_in, d_out, dmin, ti, dur, r = PASOS[i]
    u = prog(t, T_PASOS + ti, T_PASOS + ti + dur)
    S = 1500.0 * np.array([math.cos(a_in), math.sin(a_in)])
    a_out = a_in + math.pi + d_out
    F = 1500.0 * np.array([math.cos(a_out), math.sin(a_out)])
    side = 1.0 if i % 2 == 0 else -1.0
    C = dmin * 1.7 * np.array([math.cos(a_in + math.pi / 2 * side), math.sin(a_in + math.pi / 2 * side)])
    return bez2(S, C, F, u)


# ---------------------------------------------------------------- (b) 2024 PT5
T_PT0, T_PT1 = A.y2024 - 0.1, A.se_fue + 0.5
_UU = np.linspace(0, 1, 301)
_RR = 360 + 1000 * np.abs(2 * _UU - 1) ** 1.4
_CUM = np.cumsum(1 / _RR ** 2)
_CUM = (_CUM - _CUM[0]) / (_CUM[-1] - _CUM[0])
TH0_PT = -0.9


def pt5_mundo(t):
    u = prog(t, T_PT0, T_PT1)
    r = 360 + 1000 * abs(2 * u - 1) ** 1.4
    th = TH0_PT + 2 * math.pi * 1.15 * float(np.interp(u, _UU, _CUM))
    return np.array([r * math.cos(th), r * math.sin(th)])


# ---------------------------------------------------------------- (c) choque gigante
T_IMP = A.choque1 + 0.35            # el impacto
S_TH = np.array([1500.0, -420.0])
A_TH = np.array([40.0, -14.0])
R_TH = 66.0
_D = float(np.hypot(*(A_TH - S_TH)))
S_END = (_D - (ER + R_TH) * 1.0) / _D
P_IMP = S_TH + (A_TH - S_TH) * S_END
PHI_IMP = math.atan2(P_IMP[1], P_IMP[0])
T_MOON2 = A.dos_o + 0.1
PHI_B = PHI_A + 2.35
W_M = 0.95                          # velocidad angular de las lunas jóvenes (rad/s)

NP = 280
_rng = np.random.default_rng(21)
PR_FIN = 200 + 330 * _rng.random(NP)
PR_ANG = _rng.normal(0, 0.30, NP)
PR_TAM = 3.0 + 4.5 * _rng.random(NP)
PR_JIT = _rng.normal(0, 1, (NP, 2))
GRUPO = np.arange(NP) % 4          # 0 -> Luna 1, 1 -> Luna 2, 2/3 -> anillo que queda


def part_pos(i, t):
    dt = t - T_IMP
    R = lerp(ER * 1.04, PR_FIN[i], e_out(prog(dt, 0.0, 1.7)))
    w = 1.15 * (330.0 / R) ** 1.5
    phi = PHI_IMP + PR_ANG[i] + w * dt
    return np.array([R * math.cos(phi), R * math.sin(phi)])


def luna_joven_1(t):
    return np.array(K.pos_orbita(0, 0, 330.0, 330.0, 0, PHI_A + W_M * (t - T_LUNA1)))


def luna_joven_2(t):
    return np.array(K.pos_orbita(0, 0, 345.0, 345.0, 0, PHI_B + W_M * (t - T_LUNA1)))


def joven(t):
    """0..1: la Tierra recién chocada brilla al rojo y se enfría."""
    k = 0.5 * e_out(prog(t, A.fabricarla, A.fabricarla + 1.2)) + 0.5 * e_out(prog(t, T_IMP, T_IMP + 0.5))
    return k * (1 - e_inout(prog(t, A.nacio + 0.2, A.anos + 0.4)))


def escombros(lz, cam, t):
    if t < T_IMP:
        return
    z = cam.z
    fade = 1 - e_in(prog(t, T_MOON2 + 0.3, 83.2))
    for i in range(NP):
        g = GRUPO[i]
        if g in (2, 3) and fade < 0.02:
            continue
        p = part_pos(i, t)
        rad = PR_TAM[i]
        if g == 0:
            c = e_inout(prog(t, A.junta - 0.8, T_LUNA1))
            tgt = luna_joven_1(t) + PR_JIT[i] * 14 * (1 - c)
            p = p + (tgt - p) * c
            if c > 0.985:
                continue
            rad *= 1 - 0.5 * c
        elif g == 1:
            c = e_inout(prog(t, A.distinto - 0.3, T_MOON2))
            tgt = luna_joven_2(t) + PR_JIT[i] * 14 * (1 - c)
            p = p + (tgt - p) * c
            if c > 0.985:
                continue
            rad *= 1 - 0.5 * c
        else:
            rad *= fade
        q = cam.a_pant(p)
        if not (-30 < q[0] < W + 30 and -30 < q[1] < H + 30):
            continue
        calor = 1 - prog(t - T_IMP, 0.0, 4.0)
        col = mezcla((176, 168, 190), (255, 170, 90), calor)
        lz.relleno(circulo(q[0], q[1], max(2.0, rad * z * 1.3), 8), col)
        if calor > 0.3 and i % 3 == 0:
            lz.halo(q[0], q[1], rad * z * 3.2, (255, 160, 80), alfa=0.35 * calor, r0=0.1)


# ---------------------------------------------------------------- recuadro de Tritón (Neptuno)
PAN = dict(cx=1480.0, cy=335.0, w=800.0, h=500.0)


def inset_triton(lz, t):
    k = pop(t, A.neptuno - 0.5, 0.45) * (1 - e_in(prog(t, A.fuera + 1.0, A.fuera + 1.35)))
    if k < 0.02:
        return
    cx, cy, w, h = PAN["cx"], PAN["cy"], PAN["w"], PAN["h"]
    gx, gy = -150.0, 25.0            # Neptuno (coordenadas locales del recuadro)
    R_O = 212.0
    q = rect_red(-w / 2, -h / 2, w, h, 40)
    with lz.capa(2):
        with lz.grupo(cx, cy, k):
            lz.relleno(q, (18, 18, 56), alfa=0.96)
            with lz.recorte(q):
                for i in range(18):      # estrellas del recuadro
                    lz.relleno(circulo(-w / 2 + w * h01(i, 1, 9), -h / 2 + h * h01(i, 2, 9), 2.2 + 2 * h01(i, 3, 9), 8),
                               (230, 235, 255), alfa=0.7)
                K.planeta_gas(lz, gx, gy, 118, t, "hielo", seed=8, tormenta=False)
                th_ = np.linspace(0, 2 * np.pi, 120)
                P.discontinua(lz, np.stack([gx + R_O * np.cos(th_), gy + R_O * np.sin(th_)], 1), AZUL, 3.5, 14, 10, fase=-t * 28)
                t_ant = A.fuera - 1.5          # se va «hacia atrás» por donde vino
                a_ant = 2.3 - 1.15 * (t_ant - A.triton)
                q0 = np.array([gx + R_O * math.cos(a_ant), gy + R_O * math.sin(a_ant)])
                tang = np.array([math.sin(a_ant), -math.cos(a_ant)])
                Cc = q0 + tang * 260
                Ff = np.array([-560.0, -340.0])
                u = e_in(prog(t, t_ant, A.fuera + 0.9))
                if u > 0:
                    pos = bez2(q0, Cc, Ff, u)
                    ruta = np.array([bez2(q0, Cc, Ff, v) for v in np.linspace(0, 1, 40)])
                    P.discontinua(lz, ruta, ORO, 5.0, 16, 12, fase=-t * 30)
                else:
                    ang = 2.3 - 1.15 * (t - A.triton)
                    pos = np.array([gx + R_O * math.cos(ang), gy + R_O * math.sin(ang)])
                kt = pop(t, A.triton - 0.1, 0.3)
                K.cuerpo_rocoso(lz, pos[0], pos[1], 32 * kt, "hielo", seed=2, ang_luz=LUZ, rot=t * 0.8)
                ln = e_out(prog(t, A.neptuno + 0.1, A.neptuno + 0.7))
                K.etiqueta(lz, gx + 60, gy - 90, "Neptuno", dx=120, dy=-80, px=38, frac=ln)
                lt = e_out(prog(t, A.triton, A.triton + 0.6)) * (1 - e_in(prog(t, A.viajera - 0.1, A.viajera + 0.3)))
                if lt > 0.01:
                    K.etiqueta(lz, pos[0], pos[1] - 36, "Tritón", dx=120, dy=-80, px=38, frac=lt)
                lv = e_out(prog(t, A.viajera, A.viajera + 0.5))
                if lv > 0.01:
                    P.pastilla(lz, 205, -185, "viajera de fuera", px=38, k=lv, fondo=ORO, color=TINTA)
            lz.trazo(np.vstack([q, q[:1]]), (255, 255, 255), 5.0, afinar=False, temblor=0.0)


# ---------------------------------------------------------------- la toma
def toma_3(lz, t, cam0):
    shake = np.zeros(2)
    if t > T_IMP:
        dt = t - T_IMP
        shake = 16 * math.exp(-dt * 4.2) * np.array([math.sin(dt * 71), math.cos(dt * 83)])
    cam = Cam(cam0.ancla, cam0.pant + shake, cam0.z)
    z = cam.z
    E = cam.a_pant((0, 0))
    th = ang_luna(t)
    moon_v = (1 - e_in(prog(t, A.fabricarla - 0.1, A.fabricarla + 0.5))) if t < T_LUNA1 else 1.0
    mw = luna_mundo(t)
    mp = cam.a_pant(mw)
    # órbita de la Luna
    if t < A.fabricarla + 0.4 or t > T_LUNA1:
        r_o = radio_luna1(t) if t > T_LUNA1 else RL
        K.orbita(lz, E[0], E[1], r_o * z, r_o * z, 0, AZUL, 3.0, alfa=0.45 * (moon_v if t < T_LUNA1 else e_out(prog(t, T_LUNA1, T_LUNA1 + 0.6))),
                 fase=t * 26)
    # Tierra
    y = joven(t)
    if y > 0.01:
        lz.halo(E[0], E[1], ER * z * 2.0, (255, 120, 50), alfa=0.5 * y, r0=0.35)
    amp = 0.0
    if t < A.fabricarla:
        amp = 0.1
    ang_m = math.atan2(mp[1] - E[1], mp[0] - E[0])
    Ec = ME._tierra(lz, t, cam, [(ang_m, 1.0)] if (moon_v > 0.5 and t < A.fabricarla) else [], amp, 0.0)
    if y > 0.01:
        lz.relleno(circulo(Ec[0], Ec[1], ER * z * 0.985, 70), (255, 96, 36), alfa=0.38 * y)
        # manchas de lava
        for i in range(7):
            a = h01(i, 1, 4) * 6.28 + t * 0.35
            d = ER * z * (0.2 + 0.6 * h01(i, 2, 4))
            lz.relleno(elipse(Ec[0] + math.cos(a) * d, Ec[1] + math.sin(a) * d * 0.9, ER * z * 0.14, ER * z * 0.08, a, 16),
                       (255, 200, 90), alfa=0.65 * y)
    # ---- La Luna de hoy (hasta que se «borra» para fabricarla)
    if t < A.fabricarla + 0.7 and moon_v > 0.01:
        K.cuerpo_rocoso(lz, mp[0], mp[1], MR * z * moon_v, "luna", seed=1, ang_luz=LUZ, rot=0.07 * t)

    # ---- (a) la pregunta y la captura
    if t < A.uno:
        qa = ventana(t, A.primera, A.uno - 0.2, 0.3, 0.3)
        if qa > 0.02:
            gp = cam.a_pant(np.array(K.pos_orbita(0, 0, RL * 0.8, RL * 0.8, 0, ang_luna(t) - 0.9)))
            fantasma(lz, gp[0], gp[1], MR * z * 1.0, t, alfa=qa)
            P.rotulo(lz, gp[0], gp[1] - MR * z - 52 - 5 * math.sin(t * 3), "?", px=110, color=ORO, alfa=qa)
    # cartas de opciones
    chip(lz, t, 250, 90, "1 · Capturarla", A.uno - 0.15, 82.3, 42, ORO, alfa=1.0 - 0.6 * e_out(prog(t, A.fabricarla - 0.1, A.fabricarla + 0.3)))
    chip(lz, t, 262, 170, "2 · Fabricarla", A.fabricarla - 0.15, 82.3, 42, ROSA)

    # rocas que pasan de largo (primero la que se queda)
    T_SALE = A.dificilisimo - 0.9
    if A.asteroide - 0.7 < t < T_SALE + 0.6:
        vis = 1.0 if t < T_SALE else 1 - e_in(prog(t, T_SALE, T_SALE + 0.5))
        if vis > 0.02:
            f = lambda tt: cam.a_pant(roca_cap(tt))  # noqa: E731
            trail(lz, f, t, dur=0.55, n=12, color=(255, 255, 255), ancho=9 * vis)
            pr = f(t)
            if t > T_CAP:
                nu = np.linspace(0, 2 * np.pi, 160)
                rr = A_CAP * (1 - E_CAP ** 2) / (1 + E_CAP * np.cos(nu))
                pts = np.stack([E[0] + z * rr * np.cos(nu), E[1] + z * rr * np.sin(nu)], 1)
                P.discontinua(lz, pts, MENTA, 3.0, 14, 10, fase=-t * 30, frac=e_out(prog(t, T_CAP, T_CAP + 0.9)))
            K.roca(lz, pr[0], pr[1], 24 * z * vis, seed=5, rot=t * 1.4, tipo="ceniza", ang_luz=LUZ)
    if A.dificilisimo - 0.9 < t < T_PASOS + 2.5 + 2.4:
        for i, (a_in, d_out, dmin, ti, dur, r) in enumerate(PASOS):
            if T_PASOS + ti - 0.05 < t < T_PASOS + ti + dur + 0.05:
                f = lambda tt, i=i: cam.a_pant(roca_paso(i, tt))  # noqa: E731
                pr = f(t)
                trail(lz, f, t, dur=0.5, n=10, color=(210, 220, 255), ancho=5.0)
                K.roca(lz, pr[0], pr[1], r * z, seed=i + 20, rot=t * (1 + 0.3 * i), tipo="ceniza" if i % 2 else "mercurio",
                       ang_luz=LUZ)
        cs = ventana(t, A.casi, A.largo + 0.9, 0.3, 0.4)
        if cs > 0.02:
            P.pastilla(lz, 1500, 110, "casi todo sigue de largo", px=40, k=cs, fondo=(255, 255, 255), color=TINTA)

    # ---- (b) 2024 PT5
    if T_PT0 - 0.2 < t < T_PT1 + 0.4:
        vis = ventana(t, T_PT0 + 0.2, T_PT1 - 0.1, 0.3, 0.3)
        if vis > 0.01:
            f = lambda tt: cam.a_pant(pt5_mundo(tt))  # noqa: E731
            trail(lz, f, t, dur=1.2, n=24, color=(255, 214, 90), ancho=6.0)
            pr = f(t)
            K.roca(lz, pr[0], pr[1], 11 * z * 1.0, seed=7, rot=t * 3, tipo="mercurio", ang_luz=LUZ)
            pul = 0.65 + 0.35 * math.sin(t * 7)
            lz.halo(pr[0], pr[1], 46 * z + 12, ORO, alfa=0.55 * pul * vis, r0=0.45)
            if pr[0] < W - 360 and pr[1] > 190:
                lt = e_out(prog(t, A.y2024 + 0.3, A.y2024 + 0.9))
                K.etiqueta(lz, pr[0], pr[1], "2024 PT5", dx=-170, dy=-90, px=36, frac=lt * vis)
                lo = e_out(prog(t, A.once, A.once + 0.5))
                if lo > 0.01:
                    P.pastilla(lz, pr[0] - 170, pr[1] - 90 + 70, "11 m", px=36, k=lo * vis, fondo=ORO, color=TINTA)
        fe = ventana(t, A.dos_meses - 0.3, T_PT1, 0.3, 0.3)
        if fe > 0.02:
            P.pastilla(lz, 330, 960, "29 sep – 25 nov 2024", px=40, k=fe, fondo=(255, 255, 255), color=TINTA)
            P.rotulo(lz, 330, 1030, "mini Luna" if t > A.mini - 0.1 else "dos meses", px=34, alfa=fe * 0.9)

    # ---- (c) choque gigante
    if A.fabricarla < t < T_IMP + 0.05:
        u = prog(t, T_IMP - 1.45, T_IMP)
        s_ = S_END * (u ** 1.7)
        pos = S_TH + (A_TH - S_TH) * s_
        q = cam.a_pant(pos)
        K.cuerpo_rocoso(lz, q[0], q[1], R_TH * z, "rojiza", seed=9, ang_luz=LUZ, rot=-0.5 * t)
        trail(lz, lambda tt: cam.a_pant(S_TH + (A_TH - S_TH) * (S_END * (prog(tt, T_IMP - 1.45, T_IMP) ** 1.7))), t, dur=0.4,
              n=12, color=(255, 170, 110), ancho=9)
    if T_IMP - 0.05 < t < T_IMP + 2.6:
        qi = cam.a_pant(P_IMP)
        k = campana(t, T_IMP - 0.05, T_IMP + 1.0)
        lz.halo(qi[0], qi[1], 360 * z * k, (255, 230, 170), alfa=0.8 * k, r0=0.0)
        K.destello(lz, qi[0], qi[1], 140 * z * k, t, alfa=min(1.0, k * 1.3))
        for j in range(3):
            uu = prog(t, T_IMP + 0.12 * j, T_IMP + 1.5 + 0.12 * j)
            if 0 < uu < 1:
                P.onda(lz, E[0], E[1], ER * z * (1.1 + 3.4 * e_out(uu)), 9.0, (255, 214, 150), alfa=0.65 * (1 - uu))
    escombros(lz, cam, t)
    # ---- Lunas jóvenes (nacen de los escombros)
    for tn_, fn, tp_, sd in ((T_LUNA1, luna_joven_1, "luna", 1), (T_MOON2, luna_joven_2, "ceniza", 5)):
        if t > tn_ - 0.05:
            m = cam.a_pant(luna_mundo(t) if sd == 1 else luna_joven_2(t))
            k = pop(t, tn_ - 0.05, 0.5)
            K.cuerpo_rocoso(lz, m[0], m[1], MR * z * k, tp_, seed=sd, ang_luz=LUZ, rot=0.07 * t + sd)
            kd = campana(t, tn_ - 0.1, tn_ + 0.9)
            if kd > 0.01:
                K.destello(lz, m[0], m[1], 120 * z * kd, t, alfa=min(1.0, kd * 1.4))
    # texto «hace 4 500 millones de años»
    ka = ventana(t, A.nacio + 0.2, A.anos + 0.8, 0.3, 0.4)
    if ka > 0.02:
        P.pastilla(lz, 1380, 130, "hace 4 500 millones de años", px=44, k=ka, fondo=ORO, color=TINTA)
    # --- Kuri
    pos_k = tuple(kf(t, [(41.4, (1640.0, 420.0)), (43.4, (1760.0, 930.0)), (1000.0, (1760.0, 930.0))]))
    if A.asteroide - 0.5 < t < T_SALE + 0.8:
        tgt = cam.a_pant(roca_cap(t))
    elif T_PT0 - 0.2 < t < T_PT1:
        tgt = cam.a_pant(pt5_mundo(t))
    elif t > A.fabricarla:
        tgt = E
    else:
        tgt = E
    head = np.array([pos_k[0], pos_k[1] - 90])
    d = np.asarray(tgt, float) - head
    mirar = tuple(d / max(1.0, float(np.hypot(*d))) * 0.9)
    kuri_ui(lz, t, pos_k[0], pos_k[1], 1.0, mirar, boca=campana(t, T_IMP - 0.3, T_IMP + 1.6),
            feliz=1.0 if (A.dos_o - 0.2 < t < 83.0) else 0.0)
    inset_triton(lz, t)
