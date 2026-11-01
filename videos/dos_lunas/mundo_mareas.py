# -*- coding: utf-8 -*-
"""Toma 6 «mareas» (163,6-202,9 s): la cámara sube de la playa nocturna al espacio con la 2.ª luna a 192 000 km (cotas, curva
1/d³, «×8», la Tierra con el agua abultada), vuelve a caer hasta una costa al atardecer (medidor de marea en metros: dos
vaivenes al día, récord de 16 m en Fundy, «normal» con esta luna, dos lunas que se alinean y se suman, ola gigante) y sube otra
vez al espacio para empalmar con la toma 7 (`C7`). Aquí viven también los ayudantes que usan las tomas 7-10: `cam_inm`
(caída/subida entre el espacio y una superficie), `espacio_cuerpos`, `fondo_gas`."""
import math

import numpy as np

import fondos as F
import plano as P
import kz_espacio as K
from plano import mezcla, aclarar, oscurecer
from motor import W, H, prog, clamp01, lerp, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, smooth, h01
from mundo_comun import Cam, Sup, kf, pop, ventana, campana, smooth_arr
from anclas import A, E_MAREAS, E_CALOR
import mundo_espacio as ME
import mundo_tierra as MT
from mundo_espacio import ER, MR, RL, LUZ, AZUL, ORO, TINTA, MENTA, ROSA, LIN, kuri_ui, chip

R2 = 350.0                                  # radio de la órbita de la 2.ª luna a 192 000 km (la mitad de la órbita lunar)
C6 = Cam((0, 0), (640, 545), 1.45)          # vista de las cotas y de la curva
C7 = Cam((0, 0), (700, 540), 3.0)           # vista con la que empieza la toma 7 (Tierra grande, 2.ª luna a la derecha)
HX = MT.HX
H_COSTA = 860.0                             # y de pantalla de H = 0 en la costa
T_SAL = (E_MAREAS, E_MAREAS + 3.6)          # playa nocturna -> espacio
T_INM = (A.oceanos_m - 0.8, A.oceanos_m + 2.2)   # espacio -> costa
T_SAL2 = (E_CALOR - 2.4, E_CALOR)           # costa -> espacio (empalme con la toma 7)
KURI_ESP = (1760.0, 940.0)
KURI_COSTA = (1000.0, 340.0)
NEB6 = [(500, 300, 760, (30, 140, 210), 21, 0.55), (1500, 780, 660, (80, 70, 220), 22, 0.45),
        (1250, 280, 600, (30, 190, 170), 23, 0.35)]


# ======================================================================== lunas (mundo)
def ang1(t):
    return float(kf(t, [(E_MAREAS, -0.30), (E_CALOR, 0.0)], ease=LIN))


def ang2(t):
    return float(kf(t, [(E_MAREAS, -0.55), (E_CALOR, -0.12)], ease=LIN))


def p_luna1(t):
    return np.array(K.pos_orbita(0, 0, RL, RL, 0, ang1(t)))


def p_luna2(t):
    return np.array(K.pos_orbita(0, 0, R2, R2, 0, ang2(t)))


# ======================================================================== cámara espacio <-> superficie
def cam_inm(c0, u, dest=(HX, H_COSTA)):
    """Cámara que cae hacia el punto más alto de la Tierra: u=0 es la vista espacial `c0`, u=1 es la superficie plana.
    Devuelve (cam, radio de la Tierra en pantalla). Misma fórmula que `mundo_tierra.cam_inmersion`."""
    u = clamp01(u)
    L0 = np.array([0.0, -ER])
    ue = e_inout(u)
    p0 = c0.a_pant(L0)
    z = math.exp(lerp(math.log(c0.z), math.log(520.0), e_in(u) * 0.35 + ue * 0.65))
    p = p0 + (np.array(dest, float) - p0) * ue
    return Cam(L0, p, z), ER * z


def fondo_gas(lz, t, cam, neb, k=1.0, sol=True):
    """Nubes de gas de color propio + Sol y rocas lejanas (con la opacidad `k`)."""
    if k < 0.02:
        return
    ME.nebulas(lz, cam, [(x, y, r, c, sd, al * k) for (x, y, r, c, sd, al) in neb])
    if sol and k > 0.4:
        ME.fondo_vivo(lz, t, cam)


def lunas_marea(t, E, p1, p2):
    """Fuerzas de las dos lunas sobre el agua; la 2.ª crece al decir «ocho veces más fuerte»."""
    k8 = e_inout(prog(t, A.mitad_m2 - 0.3, A.ocho + 1.1))
    a1 = math.atan2(p1[1] - E[1], p1[0] - E[0])
    a2 = math.atan2(p2[1] - E[1], p2[0] - E[0])
    return [(a1, 0.8), (a2, 0.8 + 3.6 * k8)], k8


def espacio_cuerpos(lz, t, cam, rs, orbitas=True):
    """Tierra con sus mareas, órbitas y las dos lunas del mundo (se muestran al alejarse la cámara)."""
    z = cam.z
    E = cam.a_pant((0, 0))
    p1, p2 = cam.a_pant(p_luna1(t)), cam.a_pant(p_luna2(t))
    lunas, k8 = lunas_marea(t, E, p1, p2)
    ao = (1 - prog(math.log(z), math.log(2.4), math.log(6.0))) if orbitas else 0.0
    if ao > 0.02:
        K.orbita(lz, E[0], E[1], R2 * z, R2 * z, 0, ORO, 3.0, alfa=0.5 * ao, fase=t * 26)
        K.orbita(lz, E[0], E[1], RL * z, RL * z, 0, AZUL, 3.0, alfa=0.45 * ao, fase=t * 22)
    if rs < 24000:
        K.tierra_marea(lz, E[0], E[1], rs, t, lunas, rot=0.45 * t, ang_luz=LUZ, amp=0.1)
    aw = 1 - prog(math.log(z), math.log(3.2), math.log(4.4))
    r_m = MR * z
    if aw > 0.02:
        for p, tipo, seed, rot in ((p1, "luna", 1, 0.07 * t), (p2, "ceniza", 5, 0.07 * t + 5)):
            if -r_m - 60 < p[0] < W + r_m + 60 and -r_m - 60 < p[1] < H + r_m + 60:
                K.cuerpo_rocoso(lz, p[0], p[1], r_m, tipo, seed=seed, ang_luz=LUZ, rot=rot, alfa=aw)
    return E, p1, p2, k8


# ======================================================================== la costa al atardecer
def terr(X):
    """Altura del terreno H(X): meseta con casas a la izquierda, acantilado, repisa del muelle y fondo marino que se hunde."""
    X = np.asarray(X, float)
    h = np.full_like(X, 330.0)
    a = smooth_arr((X + 560) / 70)
    h = h * (1 - a) + 62.0 * a
    b = smooth_arr((X + 330) / 300)
    h = h * (1 - b) + (-95.0) * b
    c = smooth_arr((X + 30) / 600)
    h = h * (1 - c) + (-230.0 + 14 * np.sin(X / 90)) * c
    return h


PX_M = 20.0                 # píxeles por metro de marea
H0_MAR = -30.0              # H del nivel de la pleamar... del cero del medidor (bajamar)

CLAVES_M = [(T_INM[1] - 0.6, 1.0), (180.5, 7.0), (181.8, 1.5), (183.0, 7.5), (183.7, 2.0), (184.9, 16.0), (186.4, 3.5),
            (188.0, 16.0), (189.2, 3.0), (190.5, 16.0), (191.9, 5.0), (193.0, 14.0), (194.2, 4.0), (195.9, 24.0),
            (197.4, 7.0), (199.4, 9.0), (200.6, 26.0), (T_SAL2[1], 26.0)]


def nivel_m(t):
    return float(kf(t, CLAVES_M))


def nivel_H(t):
    return H0_MAR + PX_M * nivel_m(t)


def superficie(X, t):
    X = np.asarray(X, float)
    s = nivel_H(t) + 3.2 * np.sin(X / 58 + t * 1.5) + 1.8 * np.sin(X / 23 - t * 2.2)
    # ola gigante: frente empinado hacia la tierra y cola larga
    u = prog(t, A.ola_m - 1.3, A.ola_m + 1.5)
    if 0 < u < 1:
        xw = lerp(1100.0, -430.0, e_inout(u))
        amp = 250.0 * math.sin(math.pi * min(1.0, u * 1.15)) ** 0.8
        d = X - xw
        s = s + amp * np.where(d < 0, np.exp(-(d / 75.0) ** 2), np.exp(-(d / 340.0) ** 2))
    return s


def cielo_costa(t):
    img = F.degradado(t, (0.10, 0.13, 0.40), (1.0, 0.62, 0.50))
    return F.estrellas(img, t, 0.30)


def gaviota(lz, x, y, s, t, ph):
    f = math.sin(t * 5.5 + ph)
    with lz.grupo(x, y, s):
        for lado in (-1, 1):
            lz.trazo(np.array([[0, 0], [lado * 18, -10 - 9 * f], [lado * 36, 2 + 4 * f]]), (250, 244, 240), 5.5, afinar=True,
                     temblor=0.0)
        lz.relleno(elipse(0, 2, 7, 5, 0, 12), (250, 244, 240))


M1C = np.array([1180.0, 150.0])
M2C = np.array([1580.0, 255.0])


def pos_m1c(t):
    u = e_inout(prog(t, A.dos_lunas_m + 0.2, A.sumarian + 0.4))
    return M1C + (np.array([1395.0, 140.0]) - M1C) * u


def cielo_costa_obj(lz, t, a):
    """Sol que se pone detrás del acantilado, nubes, dos lunas y gaviotas (todo en pantalla)."""
    if a < 0.01:
        return
    lz.halo(130, 540, 560, (255, 186, 120), alfa=0.38 * a, r0=0.1)
    lz.relleno(circulo(130, 540, 72, 40), (255, 226, 170), alfa=0.95 * a)
    for i, (x0, y0, s, v) in enumerate(((300, 130, 1.0, 9), (1000, 60, 1.3, 6), (1650, 130, 0.9, 12))):
        x = (x0 + v * t) % (W + 500) - 250
        MT.nube(lz, x, y0, s, (236, 168, 160), 0.45 * a)
    MT.luna_cielo(lz, t, pos_m1c(t), 70.0, "luna", 1, 0.6, math.pi, a, 0.5)
    MT.luna_cielo(lz, t, M2C, 140.0, "ceniza", 5, 0.5, math.pi, a, 0.5)
    for i in range(5):
        gx = (150 + 330 * i + 40 * t * (0.7 + 0.1 * i)) % (W + 200) - 100
        gaviota(lz, gx, 250 + 55 * (i % 3) + 8 * math.sin(t * 1.3 + i), 1.0 - 0.1 * (i % 3), t, i * 1.7)


def torre(lz, t, S, X):
    """Faro de rayas rojas con haz de luz que barre."""
    with S.en(lz, X, float(terr(X)) + 2):
        lz.relleno(np.array([[-30, 0], [30, 0], [19, -190], [-19, -190]]), (244, 240, 236))
        for y0, y1 in ((-30, -64), (-98, -132), (-162, -190)):
            f0, f1 = 30 - 11 * (-y0 / 190), 30 - 11 * (-y1 / 190)
            lz.relleno(np.array([[-f0, y0], [f0, y0], [f1, y1], [-f1, y1]]), (212, 84, 84))
        lz.relleno(rect_red(-28, -204, 56, 14, 3), (70, 60, 100))
        lz.relleno(rect_red(-20, -236, 40, 34, 4), (255, 226, 140))
        lz.relleno(np.array([[-26, -236], [0, -262], [26, -236]]), (212, 84, 84))
        lz.halo(0, -219, 120, (255, 226, 150), alfa=0.55, r0=0.2)
        c = abs(math.cos(t * 1.15))
        for lado in (-1, 1):
            lz.relleno(np.array([[0, -222], [lado * 900 * c, -300], [lado * 900 * c, -150]]), (255, 240, 180), alfa=0.16)


def muelle(lz, t, S, alfa=1.0):
    X0, X1 = -345.0, -40.0
    deck = np.array([[X0, 80], [X1, 80], [X1, 66], [X0, 66]])
    for X in np.arange(X0 + 20, X1, 52.0):
        base = float(terr(X))
        lz.relleno(S.poly(np.array([[X - 6, 70], [X + 6, 70], [X + 6, base - 4], [X - 6, base - 4]])), (112, 80, 70), alfa=alfa)
    lz.relleno(S.poly(deck), (160, 118, 90), alfa=alfa)
    lz.relleno(S.poly(np.array([[X0, 66], [X1, 66], [X1, 58], [X0, 58]])), (116, 82, 72), alfa=alfa)
    for X in np.arange(X0 + 10, X1, 38.0):
        lz.trazo(np.array([S.pt(X, 80), S.pt(X, 112)]), (230, 224, 214), max(2.0, 5 * S.k), afinar=False, temblor=0.0)
    lz.trazo(np.array([S.pt(X0 + 10, 112), S.pt(X1 - 6, 112)]), (230, 224, 214), max(2.0, 5 * S.k), afinar=False, temblor=0.0)


def barca(lz, t, S, X, s):
    Hs = float(superficie(X, t)) + 2
    x, y = S.pt(X, Hs)
    ang = 0.07 * math.sin(t * 1.4 + X)
    ME.barquito(lz, x, y, -math.pi / 2 + ang, s * S.k)


def costa(lz, t, S, alfa=1.0):
    """La costa al atardecer vista de lado: meseta con casas y faro, muelle, mar con el nivel de la marea y colinas lejanas."""
    X = np.arange(-4200, 4201, 40.0)
    top = superficie(X, t)
    ter = terr(X)
    lev = nivel_H(t)
    # colinas lejanas detrás del mar (las tapa el agua cuando sube)
    Hh = (170 + 70 * np.sin(X / 260 + 1) + 34 * np.sin(X / 110 + 2.3)) * np.clip((1250 - np.abs(X - 650)) / 500, 0, 1)
    lz.relleno(S.poly(np.concatenate([np.stack([X, Hh], 1), [[X[-1], -20], [X[0], -20]]])), (118, 96, 160), alfa=alfa)
    Hn = (110 + 46 * np.sin(X / 190 + 0.4) + 20 * np.sin(X / 80)) * np.clip((1100 - np.abs(X - 380)) / 450, 0, 1)
    lz.relleno(S.poly(np.concatenate([np.stack([X, Hn], 1), [[X[-1], -20], [X[0], -20]]])), (92, 108, 172), alfa=alfa)
    # agua de fondo (opaca) y tierra encima
    agua = np.concatenate([np.stack([X, top], 1), [[X[-1], -2500], [X[0], -2500]]])
    x0, y0 = S.pt(600, lev)
    x1, y1 = S.pt(600, lev - 520)
    lz.degradado(S.poly(agua), (92, 190, 226), (18, 52, 120), (x0, y0), (x1, y1), alfa=alfa)
    # roca del acantilado + fondo de arena
    Xr = X[X <= -330]
    roca = np.concatenate([np.stack([Xr, terr(Xr)], 1), [[Xr[-1], -2500], [Xr[0], -2500]]])
    Pr = S.poly(roca)
    lz.relleno(Pr, (148, 104, 92), alfa=alfa)
    with lz.recorte(Pr):
        for d0, d1, c in ((40, 130, (128, 90, 86)), (130, 260, (108, 78, 84)), (260, 2600, (84, 62, 82))):
            capa_ = np.concatenate([np.stack([Xr, terr(Xr) - d0], 1), np.stack([Xr[::-1], terr(Xr[::-1]) - d1], 1)])
            lz.relleno(S.poly(capa_), c, alfa=alfa)
        for i in range(9):
            px_ = -1150 + i * 120 + 30 * math.sin(i * 5.3)
            ph = float(terr(px_)) - 80 - 55 * (i % 3)
            with S.en(lz, px_, ph):
                lz.relleno(elipse(0, 0, 26 + 8 * (i % 3), 14, 0.3 * i, 20), (168, 126, 108), alfa=alfa)
    Xa = X[X >= -340]
    arena = np.concatenate([np.stack([Xa, terr(Xa)], 1), [[Xa[-1], -2500], [Xa[0], -2500]]])
    lz.relleno(S.poly(arena), (206, 172, 132), alfa=alfa)
    # pasto de la meseta
    Xp = X[X <= -560]
    pasto = np.concatenate([np.stack([Xp, terr(Xp) + 4], 1), np.stack([Xp[::-1], terr(Xp[::-1]) - 22], 1)])
    lz.relleno(S.poly(pasto), (96, 156, 108), alfa=alfa)
    if S.k > 0.2:
        for Xs_, s in ((-905, 0.92), (-790, 1.0), (-660, 0.86)):
            x, y = S.pt(Xs_, 332)
            P.casa(lz, x, y, s * S.k, calor=0.75, oscuro=0.1)
        torre(lz, t, S, -590)
        muelle(lz, t, S, alfa)
        for Xb, sb in ((130, 2.1), (470, 1.8), (810, 2.3)):
            barca(lz, t, S, Xb, sb)
        # rocas y algas del fondo
        for i, Xf in enumerate((-20, 90, 240, 400, 560, 720, 880)):
            hb = float(terr(Xf))
            x, y = S.pt(Xf, hb - 3)
            with lz.grupo(x, y, S.k):
                lz.relleno(elipse(0, -6, 34 + 6 * (i % 3), 16, 0, 20), (150, 120, 112), alfa=alfa)
                for j in range(3):
                    sw = 10 * math.sin(t * 1.2 + i + j)
                    lz.trazo(np.array([[(j - 1) * 12, -8], [(j - 1) * 12 + sw * 0.5, -40], [(j - 1) * 12 + sw, -78 - 10 * j]]),
                             (70, 168, 120), 8, afinar=True, temblor=0.0)
        for i in range(10):
            fx = -250 + ((t * (24 + 4 * (i % 3)) * (1 if i % 2 else -1) + i * 197) % 1500)
            fh = lev - 60 - 36 * (i % 5)
            if fh > float(terr(fx)) + 20:
                x, y = S.pt(fx, fh)
                sent = 1 if i % 2 else -1
                with lz.grupo(x, y, S.k * (0.8 + 0.1 * (i % 3))):
                    c = [(255, 160, 90), (120, 200, 255), (255, 120, 170), (160, 230, 150)][i % 4]
                    lz.relleno(elipse(0, 0, 22, 11, 0, 20), c)
                    lz.relleno(np.array([[-20 * sent, 0], [-35 * sent, -10], [-35 * sent, 10]]), oscurecer(c, 0.2))
                    lz.relleno(circulo(11 * sent, -2, 2.4, 8), (255, 255, 255))
    # velo de agua por delante (todo lo que queda bajo la superficie se ve sumergido)
    mk = np.where(top > ter)[0]
    if len(mk):
        i0 = int(mk[0])
        Xw, tw, rw = X[i0:], top[i0:], np.minimum(ter[i0:], top[i0:])
        over = np.concatenate([np.stack([Xw, tw], 1), np.stack([Xw[::-1], rw[::-1] - 2], 1)])
        lz.relleno(S.poly(over), (30, 112, 196), alfa=0.34 * alfa)
        xs_, ys_ = S.p(Xw, tw)
        lz.trazo(np.stack([xs_, ys_], 1), (196, 230, 255), max(2.0, 5 * S.k), afinar=False, temblor=0.0)
    # espuma de la ola gigante
    u = prog(t, A.ola_m - 1.3, A.ola_m + 1.5)
    if 0 < u < 1 and S.k > 0.2:
        xw = lerp(1100.0, -430.0, e_inout(u))
        for i in range(34):
            fx = xw + (h01(i, 1, 3) - 0.62) * 260
            fy = float(superficie(fx, t)) + 8 * h01(i, 2, 3)
            x, y = S.pt(fx, fy)
            lz.relleno(circulo(x, y, (5 + 9 * h01(i, 3, 3)) * S.k, 10), (244, 250, 255), alfa=0.9 * alfa)


# ======================================================================== medidor de marea (diagrama en pantalla)
GX = 1790.0
GY0 = 890.0


def y_nivel(m):
    return GY0 - PX_M * m


def medidor(lz, t, k):
    if k < 0.02:
        return
    q = rect_red(GX - 40, y_nivel(26.5), 80, PX_M * 26.5 + 34, 26)
    with lz.capa(2):
        lz.relleno(q, (14, 18, 56), alfa=0.62 * k)
        for i in range(0, 25, 2):
            yy = y_nivel(i)
            lz.relleno(rect_red(GX - 30, yy - 2, 26 if i % 4 == 0 else 14, 4, 2), (230, 236, 255), alfa=0.9 * k)
            if i % 4 == 0:
                P.rotulo(lz, GX + 12, yy, str(i), px=32, alfa=k, ancla=(0.0, 0.5))
        P.rotulo(lz, GX, y_nivel(26.5) - 28, "metros", px=30, alfa=k * 0.85)
        m = nivel_m(t)
        ym = y_nivel(m)
        lz.relleno(np.array([[GX - 46, ym], [GX - 80, ym - 17], [GX - 80, ym + 17]]), ORO, alfa=k)
        P.pastilla(lz, GX - 168, ym, f"{m:.0f} m".replace(".", ","), px=40, k=k, fondo=ORO, color=TINTA)


def linea_nivel(lz, t, m, texto, k, fondo=(255, 255, 255)):
    if k < 0.02:
        return
    y = y_nivel(m)
    with lz.capa(2):
        P.discontinua(lz, np.array([[0.0, y], [GX - 50, y]]), (255, 255, 255), 3.0, 20, 14, fase=-t * 40, frac=min(1.0, k * 2))
        P.pastilla(lz, 960, y - 38, texto, px=38, k=k, fondo=fondo, color=TINTA)


def panel_tierra_sum(lz, t, k):
    """Recuadro: la Tierra con las dos lunas que se alinean y su agua que se suma."""
    if k < 0.02:
        return
    cx, cy, w, h = 300.0, 190.0, 540.0, 290.0
    q = rect_red(-w / 2, -h / 2, w, h, 34)
    ali = e_inout(prog(t, A.alinearan - 0.3, A.sumarian - 0.1))
    a_m1 = lerp(math.pi / 2, 0.0, ali)
    a_m2 = 0.0
    lunas = [(a_m1, 1.0), (a_m2, 1.0)]
    with lz.capa(2):
        with lz.grupo(cx, cy, k):
            lz.relleno(q, (16, 16, 56), alfa=0.94)
            with lz.recorte(q):
                for i in range(16):
                    lz.relleno(circulo(-w / 2 + w * h01(i, 1, 9), -h / 2 + h * h01(i, 2, 9), 2 + 2 * h01(i, 3, 9), 8),
                               (230, 235, 255), alfa=0.7)
                K.tierra_marea(lz, -170, 10, 74, t, lunas, rot=0.45 * t, ang_luz=LUZ, amp=0.16)
                p1 = np.array([-170 + 160 * math.cos(a_m1), 10 + 160 * math.sin(a_m1)])
                K.cuerpo_rocoso(lz, p1[0], p1[1], 28, "luna", seed=1, ang_luz=LUZ, rot=0.07 * t)
                K.cuerpo_rocoso(lz, -170 + 118 * math.cos(a_m2), 10 + 118 * math.sin(a_m2), 22, "ceniza", seed=5, ang_luz=LUZ,
                                rot=0.07 * t + 5)
                ks = e_out(prog(t, A.sumarian - 0.1, A.sumarian + 0.5))
                if ks > 0.01:
                    P.pastilla(lz, 125, 10, "se suman", px=40, k=ks, fondo=ORO, color=TINTA)
            lz.trazo(np.vstack([q, q[:1]]), (255, 255, 255), 5.0, afinar=False, temblor=0.0)


# ======================================================================== curva 1/d³ y cotas (vista espacial)
def panel_curva(lz, t):
    k = pop(t, A.tiron_m - 0.5, 0.45) * (1 - e_in(prog(t, A.fuerte + 0.6, A.fuerte + 1.0)))
    if k < 0.02:
        return
    cx, cy, w, h = 330.0, 168.0, 560.0, 290.0
    q = rect_red(-w / 2, -h / 2, w, h, 34)
    OX, OY = -230.0, 105.0
    with lz.capa(2):
        with lz.grupo(cx, cy, k):
            lz.relleno(q, (16, 16, 56), alfa=0.94)
            lz.trazo(np.array([[OX, OY], [OX + 500, OY]]), (255, 255, 255), 4.0, afinar=False, temblor=0.0)
            lz.trazo(np.array([[OX, OY], [OX, OY - 218]]), (255, 255, 255), 4.0, afinar=False, temblor=0.0)
            P.rotulo(lz, OX + 400, OY + 26, "distancia", px=34, ancla=(1.0, 0.5))
            P.rotulo(lz, OX + 10, OY - 228, "tirón", px=34, ancla=(0.0, 0.5))
            d = np.linspace(0.45, 1.6, 90)
            val = np.minimum(1.0 / d ** 3, 10.0)
            pts = np.stack([OX + (d - 0.45) / 1.15 * 470, OY - val * 20.0], 1)
            fr = e_inout(prog(t, A.tiron_m, A.cercania + 0.2))
            n = max(2, int(len(pts) * fr))
            lz.trazo(pts[:n], ORO, 7.0, afinar=False, temblor=0.0)
            x1 = OX + (1.0 - 0.45) / 1.15 * 470
            x2 = OX + (0.5 - 0.45) / 1.15 * 470
            k1 = pop(t, A.cercania + 0.1, 0.35)
            k2 = pop(t, A.ocho - 0.3, 0.35)
            if k1 > 0.02:
                lz.relleno(circulo(x1, OY - 20, 12 * k1, 16), (255, 255, 255))
                P.rotulo(lz, x1 + 14, OY - 56, "Luna hoy", px=34, alfa=k1, ancla=(0.0, 0.5))
            if k2 > 0.02:
                lz.relleno(circulo(x2, OY - 160, 13 * k2, 16), ROSA)
                P.pastilla(lz, x2 + 120, OY - 160, "×8", px=44, k=k2, fondo=ROSA, color=TINTA)
            kc = e_out(prog(t, A.cubo - 0.2, A.cubo + 0.4))
            if kc > 0.02:
                P.pastilla(lz, 130, -100, "1 / distancia³", px=36, k=kc, fondo=(255, 255, 255), color=TINTA)
            lz.trazo(np.vstack([q, q[:1]]), (255, 255, 255), 5.0, afinar=False, temblor=0.0)


def cotas(lz, t, E, p1, p2):
    k1 = e_inout(prog(t, A.mitad_m - 0.2, A.ciento + 0.1)) * (1 - e_in(prog(t, T_INM[0] - 0.3, T_INM[0] + 0.3)))
    k2 = e_inout(prog(t, A.ciento - 0.1, A.km_m + 0.6)) * (1 - e_in(prog(t, T_INM[0] - 0.3, T_INM[0] + 0.3)))
    if k1 > 0.01:
        yr = 985.0
        for p in (E, p1):
            P.discontinua(lz, np.array([[p[0], p[1]], [p[0], yr]]), (255, 255, 255), 2.5, 10, 9, fase=t * 20, frac=k1)
        K.regla(lz, np.array([E[0], yr]), np.array([p1[0], yr]), "384 400 km", px=38, frac=k1, lado=-1)
    if k2 > 0.01:
        yr = 885.0
        for p in (E, p2):
            P.discontinua(lz, np.array([[p[0], p[1]], [p[0], yr]]), (255, 214, 90), 2.5, 10, 9, fase=t * 20, frac=k2)
        K.regla(lz, np.array([E[0], yr]), np.array([p2[0], yr]), "192 000 km", color=ORO, px=38, frac=k2, lado=-1)
    if k1 > 0.9:
        P.rotulo(lz, 1700, 1046, "(sin escala)", px=26, alfa=0.6, color=(210, 215, 245))


# ======================================================================== Kuri
def kuri6(lz, t, pos, s, mirar_a, **kw):
    head = np.array([pos[0], pos[1] - 90 * s])
    d = np.asarray(mirar_a, float) - head
    mirar = tuple(d / max(1.0, float(np.hypot(*d))) * 0.9)
    kuri_ui(lz, t, pos[0], pos[1], s, mirar, **kw)


# ======================================================================== caída / subida (cuerpo de la toma)
def caida(lz, t, u, c0, escena):
    """Cámara entre la vista espacial `c0` (u=0) y la superficie (u=1) de la playa nocturna ('playa') o de la costa ('costa')."""
    h_dest = MT.H_ORIZ if escena == "playa" else H_COSTA
    cam, rs = cam_inm(c0, u, (HX, h_dest))
    s = MT.mezcla_cielo(rs)
    cielo = MT.cielo(t) if escena == "playa" else cielo_costa(t)
    bg = ME.fondo(t, cam) * (1 - s) + cielo * s
    fondo_gas(lz, t, cam, NEB6, k=1 - s)
    E, p1, p2, k8 = espacio_cuerpos(lz, t, cam, rs)
    S = Sup(cam.pant[0], cam.pant[1], min(1.0, rs / 9000), (1 / rs) * clamp01((1 - u) / 0.04))
    al = prog(rs, 360, 900)
    if al > 0.003:
        if escena == "playa":
            MT.paisaje(lz, t, S, alfa=al, corte=1.0)
            a_cielo = 1 - prog(t, E_MAREAS + 0.0, E_MAREAS + 1.0)
            if a_cielo > 0.01:
                MT.cielo_dos_lunas(lz, t, S, a_cielo)
            if S.k > 0.25:
                MT.corales_y_vida(lz, t, S, alfa=al)
            if S.k > 0.05:
                MT.arboles(lz, t, S, alfa=al)
                for X, tipo, sc in ((-585, "conejo", 1.7), (-455, "zorro", 1.35)):
                    x, y = S.pt(X, float(MT.h_tierra(X)) + 3)
                    if tipo == "conejo":
                        P.conejo(lz, x, y, sc * S.k, t)
                    else:
                        P.zorro(lz, x, y, sc * S.k, t)
        else:
            a_cielo = prog(rs, 4000, 20000)
            cielo_costa_obj(lz, t, a_cielo)
            costa(lz, t, S, alfa=al)
    return bg, E, p1, p2, S, rs


# ======================================================================== fases de la toma
def fase_salida(lz, t):
    u = 1 - prog(t, *T_SAL)
    bg, E, p1, p2, S, rs = caida(lz, t, u, C6, "playa")
    # Kuri deja la playa y vuelve a su rincón
    x, y = S.pt(-790.0, float(MT.h_tierra(-790.0)) + 3)
    uk = e_inout(prog(t, E_MAREAS + 0.3, E_MAREAS + 3.1))
    pos = (lerp(x, KURI_ESP[0], uk), lerp(y, KURI_ESP[1], uk) - 90 * math.sin(math.pi * uk))
    kuri6(lz, t, pos, lerp(1.55, 1.0, uk), p2 if uk > 0.5 else (1440, 440), boca=0.0)
    return bg


def vista_espacio(lz, t, cam, rs):
    """Elementos del espacio de la toma 6 (cotas, curva, flechas, ×8) con la cámara `cam` (la vista C6)."""
    E = cam.a_pant((0, 0))
    p1, p2 = cam.a_pant(p_luna1(t)), cam.a_pant(p_luna2(t))
    cotas(lz, t, E, p1, p2)
    E, p1, p2, k8 = espacio_cuerpos(lz, t, cam, rs)
    kt = ventana(t, A.tiron_m - 0.2, A.fuerte + 1.0, 0.4, 0.5)
    if kt > 0.02:
        a2 = math.atan2(p2[1] - E[1], p2[0] - E[0])
        K.flechas_marea(lz, E[0], E[1], rs, a2, fuerza=0.9 + 1.3 * k8, t=t)
    panel_curva(lz, t)
    r_m = MR * cam.z
    chip(lz, t, p2[0], p2[1] - r_m - 62, "×8", A.ocho - 0.1, T_INM[0] + 0.3, px=76, fondo=ROSA)
    return E, p1, p2


def fase_espacio(lz, t):
    cam, rs = C6, ER * C6.z
    bg = ME.fondo(t, cam)
    fondo_gas(lz, t, cam, NEB6)
    E, p1, p2 = vista_espacio(lz, t, cam, rs)
    kuri6(lz, t, KURI_ESP, 1.0, E if t < A.dos_veces_m - 6 else p2)
    return bg


def fase_inmersion(lz, t):
    u = prog(t, *T_INM)
    bg, E, p1, p2, S, rs = caida(lz, t, u, C6, "costa")
    # lo que queda del espacio se desvanece al caer
    fa = 1 - prog(u, 0.0, 0.25)
    if fa > 0.02:
        cotas(lz, t, E, p1, p2)
    ukk = e_inout(prog(u, 0.15, 0.95))
    pos = (lerp(KURI_ESP[0], KURI_COSTA[0], ukk), lerp(KURI_ESP[1], KURI_COSTA[1], ukk) - 70 * math.sin(math.pi * ukk))
    kuri6(lz, t, pos, lerp(1.0, 0.95, ukk), p2, boca=0.0)
    return bg


def fase_costa(lz, t):
    S = Sup(HX, H_COSTA, 1.0, 0.0)
    cielo_costa_obj(lz, t, 1.0)
    costa(lz, t, S, 1.0)
    k = e_out(prog(t, T_INM[1] - 0.4, T_INM[1] + 0.2))
    medidor(lz, t, k)
    # récord de Fundy y «normal»
    kr = pop(t, A.diecis - 0.15, 0.4) * (1 - e_in(prog(t, A.esa_luna - 0.3, A.esa_luna)))
    linea_nivel(lz, t, 16.0, "récord: 16 m", kr, fondo=(255, 255, 255))
    kf_ = pop(t, A.fundy - 0.1, 0.4) * (1 - e_in(prog(t, A.esa_luna - 0.3, A.esa_luna)))
    if kf_ > 0.02:
        P.pastilla(lz, 560, y_nivel(16.0) + 44, "bahía de Fundy, Canadá", px=36, k=kf_, fondo=(190, 226, 255), color=TINTA)
    kn = pop(t, A.esa_luna - 0.1, 0.4) * (1 - e_in(prog(t, A.dos_lunas_m - 0.5, A.dos_lunas_m)))
    linea_nivel(lz, t, 16.0, "con esta luna: normal", kn, fondo=ROSA)
    kk = e_out(prog(t, A.dos_lunas_m - 0.2, A.dos_lunas_m + 0.5)) * (1 - e_in(prog(t, A.costa_m - 0.2, A.costa_m + 0.3)))
    panel_tierra_sum(lz, t, kk)
    kuri6(lz, t, KURI_COSTA, 0.95, (1580, 255), boca=campana(t, A.ola_m - 0.2, A.termina + 0.6), aleteo=0.0)
    return cielo_costa(t)


def fase_salida2(lz, t):
    u = 1 - prog(t, *T_SAL2)
    bg, E, p1, p2, S, rs = caida(lz, t, u, C7, "costa")
    uk = e_inout(prog(t, T_SAL2[0] + 0.2, T_SAL2[1] - 0.1))
    pos = (lerp(KURI_COSTA[0], KURI_ESP[0], uk), lerp(KURI_COSTA[1], KURI_ESP[1], uk) - 80 * math.sin(math.pi * uk))
    kuri6(lz, t, pos, lerp(0.95, 1.0, uk), E, boca=0.0)
    if u > 0.9:
        medidor(lz, t, (u - 0.9) * 10)
    return bg


def toma_6(lz, t):
    """Dibuja la toma 6 y devuelve el fondo."""
    if t < T_SAL[1]:
        return fase_salida(lz, t)
    if t < T_INM[0]:
        return fase_espacio(lz, t)
    if t < T_INM[1]:
        return fase_inmersion(lz, t)
    if t < T_SAL2[0]:
        return fase_costa(lz, t)
    return fase_salida2(lz, t)
