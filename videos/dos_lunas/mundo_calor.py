# -*- coding: utf-8 -*-
"""Toma 7 «calor» (202,9-229,1 s): la Tierra grande (cámara `C7`) con la 2.ª luna cerca a la derecha; se abre una cuña que
enseña el interior (corteza, manto, núcleos); la roca sube y baja con la luna (cada vez más fuerte), el manto se frota y se
calienta (termómetro), recuadro de Ío con volcanes y, al final, volcanes y terremotos en la Tierra. `tierra_corte` también la
usa la toma 8 para cerrar la cuña."""
import math

import numpy as np

import plano as P
import kz_espacio as K
from plano import mezcla, aclarar, oscurecer
from motor import W, H, prog, clamp01, lerp, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, smooth, h01
from mundo_comun import Cam, kf, pop, ventana, campana
from anclas import A, E_CALOR, E_CAIDA
import mundo_espacio as ME
import mundo_mareas as MM
from mundo_espacio import ER, MR, RL, LUZ, AZUL, ORO, TINTA, MENTA, ROSA, kuri_ui
from mundo_mareas import C7, R2, p_luna1, kuri6, fondo_gas

NEB7 = [(500, 300, 760, (232, 92, 60), 31, 0.50), (1450, 780, 640, (206, 60, 140), 32, 0.42),
        (1250, 250, 600, (240, 150, 60), 33, 0.30)]
E7 = np.array([700.0, 540.0])
R7 = 300.0
KURI7 = (1760.0, 960.0)
AW = 0.95                                   # dirección (pantalla) de la cuña: abajo a la derecha
CRUST, MANTO, NUC1, NUC2 = (96, 66, 74), (240, 126, 64), (255, 186, 72), (255, 238, 156)


def ang2_7(t):
    return -0.12 + 0.012 * (t - E_CALOR)


def p2_7(t):
    return C7.a_pant(np.array(K.pos_orbita(0, 0, R2, R2, 0, ang2_7(t))))


# ---------------------------------------------------------------- vaivén de la roca: fase acumulada (la frecuencia sube)
_TT = np.arange(E_CALOR - 0.5, E_CAIDA + 4.0, 0.02)
_U = np.array([e_inout(prog(t, A.vaiven - 0.4, A.frotaria + 0.8)) for t in _TT])
_PH = np.cumsum(2 * math.pi / (2.8 - 1.5 * _U)) * 0.02


def flex(t):
    """0..1: cuánto está estirada la roca hacia la luna; la amplitud y la rapidez crecen con «una luna mucho más cercana»."""
    u = e_inout(prog(t, A.vaiven - 0.4, A.frotaria + 0.8))
    ampl = 0.30 * e_out(prog(t, A.sube - 0.5, A.sube + 0.8)) + 0.70 * u
    ampl *= 1 - e_inout(prog(t, A.volcanes2 + 0.6, E_CAIDA + 1.5))
    return ampl * (0.5 + 0.5 * math.sin(float(np.interp(t, _TT, _PH))))


def calor_t(t):
    return e_inout(prog(t, A.frotaria, A.calor_w + 1.6)) * (1 - 0.35 * e_inout(prog(t, A.tierra_c, A.tierra_c + 2.0)))


def abre_t(t):
    return e_out(prog(t, A.roca_c - 0.55, A.roca_c + 0.6))


# ---------------------------------------------------------------- la Tierra con cuña
def _globo(lz, t, r, lunas, amp, rot, ang_luz):
    """Agua abultada hacia las lunas + la Tierra (como `K.tierra_marea`, pero SIN los halos, que no se recortan)."""
    th = np.linspace(0, 2 * np.pi, 180, endpoint=False)
    f = np.zeros_like(th)
    for ang, fz in lunas:
        f += fz * np.cos(2 * (th - ang))
    R = r * (1.0 + amp * f)
    pts = np.stack([R * np.cos(th), R * np.sin(th)], 1)
    col = (76, 164, 246)
    lz.relleno(pts, col, alfa=0.95)
    lz.relleno(pts * 0.985, mezcla(col, (40, 122, 226), 0.55), alfa=0.95)
    P.tierra(lz, 0, 0, r * 0.985, t, rot=rot, ang_luz=ang_luz, luz=1.0, atmosfera=0.0)


def tierra_corte(lz, t, E, r, a_m2, a_m1, f_m1, f_m2, abre, fl, calor, jit=(0.0, 0.0)):
    """Tierra con el agua abultada hacia las lunas y una cuña abierta (`abre` 0..1) con las capas. `fl` = estiramiento de la
    roca (0..1), `calor` = temperatura del manto (0..1), `a_m2`/`a_m1` = ángulos (pantalla) hacia las dos lunas."""
    cx, cy = E[0] + jit[0], E[1] + jit[1]
    if calor > 0.02:
        lz.halo(cx, cy, r * 1.6, (255, 110, 50), alfa=0.36 * calor, r0=0.5)
    sx, sy = 1 + 0.10 * fl, 1 - 0.06 * fl
    hw = 0.62 * abre
    aw_l = AW - a_m2                                  # dirección de la cuña en el marco girado
    a0, a1 = aw_l - hw, aw_l + hw
    with lz.grupo(cx, cy, sx, a_m2, sy):
        lz.halo(0, 0, r * 1.45, (110, 190, 255), alfa=0.32, r0=0.7)
        lz.halo(0, 0, r * 1.6, (76, 164, 246), alfa=0.24, r0=0.62)
        if hw > 0.02:
            gr = 3.0 * r
            grande = [(gr * math.cos(a0 - (2 * math.pi - 2 * hw) * k / 90), gr * math.sin(a0 - (2 * math.pi - 2 * hw) * k / 90))
                      for k in range(91)]
            chico = [(1.04 * r * math.cos(a1 - 2 * hw * k / 40), 1.04 * r * math.sin(a1 - 2 * hw * k / 40)) for k in range(41)]
            resto = np.array([(1.04 * r * math.cos(a0), 1.04 * r * math.sin(a0))] + grande + chico)
            ctx = lz.recorte(resto)
        else:
            ctx = lz.recorte(circulo(0, 0, 3.0 * r, 8))
        with ctx:
            _globo(lz, t, r, [(a_m1 - a_m2, f_m1), (0.0, f_m2)], 0.12, 0.45 * t, LUZ - a_m2)
        if hw > 0.02:
            sector = np.array([[0.0, 0.0]] + [[1.02 * r * math.cos(a0 + 2 * hw * k / 40),
                                                 1.02 * r * math.sin(a0 + 2 * hw * k / 40)] for k in range(41)])
            manto = mezcla(MANTO, (255, 70, 48), calor)
            with lz.recorte(sector):
                lz.relleno(circulo(0, 0, r, 96), CRUST)
                lz.relleno(circulo(0, 0, 0.955 * r, 96), manto)
                lz.relleno(circulo(0, 0, 0.80 * r, 96), oscurecer(manto, 0.07), alfa=0.8)
                lz.relleno(circulo(0, 0, 0.56 * r, 96), mezcla(NUC1, (255, 150, 60), calor))
                lz.relleno(circulo(0, 0, 0.30 * r, 96), NUC2)
                # corrientes del manto: puntos que giran más rápido con el calor
                for i in range(16):
                    rho = r * (0.62 + 0.30 * h01(i, 1, 4))
                    th = a0 + (2 * hw) * ((h01(i, 2, 4) + (0.05 + 0.10 * calor) * t * (1 if i % 2 else -1)) % 1.0)
                    lz.relleno(circulo(rho * math.cos(th), rho * math.sin(th), 7 + 4 * h01(i, 3, 4), 12),
                               aclarar(manto, 0.28), alfa=0.8)
                for rr in (0.955, 0.56, 0.30):
                    lz.trazo(np.array([[rr * r * math.cos(a0 + 2 * hw * k / 40), rr * r * math.sin(a0 + 2 * hw * k / 40)]
                                       for k in range(41)]), (255, 255, 255), 2.5, afinar=False, temblor=0.0)
            for a in (a0, a1):
                lz.trazo(np.array([[0.0, 0.0], [1.02 * r * math.cos(a), 1.02 * r * math.sin(a)]]), (255, 240, 220), 4.0,
                         afinar=False, temblor=0.0)
    return (cx, cy)


def friccion(lz, t, E, r, k):
    """Pares de flechas que se frotan en sentidos contrarios dentro del manto + chispas."""
    if k < 0.02:
        return
    a_m2 = math.atan2(p2_7(t)[1] - E[1], p2_7(t)[0] - E[0])
    for i, da in enumerate((-0.38, 0.0, 0.38)):
        a = AW + da
        rho = 0.78 * r
        p = E + rho * np.array([math.cos(a), math.sin(a)])
        tg = np.array([-math.sin(a), math.cos(a)])
        nr = np.array([math.cos(a), math.sin(a)])
        s = math.sin(t * 7 + i * 2.1)
        K.flecha(lz, p - tg * 34 * s + nr * 16, p + tg * 34 * s + nr * 16, (255, 255, 255), ancho=6, alfa=k, capa=2)
        K.flecha(lz, p + tg * 34 * s - nr * 16, p - tg * 34 * s - nr * 16, (255, 255, 255), ancho=6, alfa=k, capa=2)
        if (int(t * 6) + i) % 2 == 0:
            K.destello(lz, p[0] + 30 * math.cos(t * 3 + i), p[1] - 26, 20 * k, t + i, color=(255, 220, 140), alfa=k)


def termo(lz, t, k):
    if k < 0.02:
        return
    nivel = calor_t(t)
    with lz.capa(2):
        P.termometro(lz, 150, 940, 0.9, nivel, col=(255, 96, 70))
        P.pastilla(lz, 150, 520, "calor", px=40, k=k, fondo=(255, 186, 120), color=TINTA)


# ---------------------------------------------------------------- Ío
def pluma(lz, t, x, y, ang, seed, k):
    """Chorro de azufre que sale del borde de Ío (origen en (x, y), sale hacia `ang`)."""
    with lz.grupo(x, y, 1.0, ang + math.pi / 2):
        lz.halo(0, -10, 56 * k, (255, 150, 70), alfa=0.7 * k, r0=0.1)
        for i in range(14):
            ph = ((t * 0.75 + i / 14 + seed * 0.37) % 1.0)
            yy = -ph * (150 + 60 * h01(i, 1, seed)) * k
            xx = (h01(i, 2, seed) - 0.5) * 70 * ph + 10 * math.sin(ph * 6 + i)
            rr = (5 + 9 * ph) * k
            lz.relleno(circulo(xx, yy, rr, 12), mezcla((255, 232, 150), (190, 150, 200), ph), alfa=0.95 - 0.55 * ph)


def inset_io(lz, t):
    k = pop(t, A.io - 0.4, 0.45) * (1 - e_in(prog(t, A.activos + 1.0, A.activos + 1.4)))
    if k < 0.02:
        return
    cx, cy, w, h = 1290.0, 420.0, 820.0, 540.0
    q = rect_red(-w / 2, -h / 2, w, h, 40)
    with lz.capa(2):
        lz.relleno(rect_red(-10, -10, W + 20, H + 20, 0), (10, 8, 34), alfa=0.55 * min(1.0, k))
        with lz.grupo(cx, cy, k):
            lz.relleno(q, (22, 14, 50), alfa=0.97)
            with lz.recorte(q):
                for i in range(22):
                    lz.relleno(circulo(-w / 2 + w * h01(i, 1, 9), -h / 2 + h * h01(i, 2, 9), 2.0 + 2 * h01(i, 3, 9), 8),
                               (230, 235, 255), alfa=0.7)
                K.nebulosa(lz, 200, 150, 460, (210, 90, 60), seed=6, alfa=0.35, capa=2)
                K.planeta_gas(lz, -300, 60, 230, t, "jupiter", seed=4)
                est = 0.25 + 0.15 * math.sin(t * 5.5)
                K.luna_rota(lz, 120, -20, 124, est, math.pi, t, seed=3, tipo="volcanica", ang_luz=LUZ)
                for j, (aa, sd) in enumerate(((-1.25, 1), (-0.35, 2), (0.75, 3), (-2.0, 4), (0.2, 5))):
                    kp = pop(t, A.estirada - 0.1 + 0.26 * j, 0.4) * 1.5
                    bx, by = 120 + 124 * 1.15 * math.cos(aa), -20 + 124 * 1.0 * math.sin(aa)
                    pluma(lz, bx, by, aa, t, sd, kp)
                lio = e_out(prog(t, A.io, A.io + 0.5))
                K.etiqueta(lz, 190, -100, "Ío", dx=120, dy=-90, px=40, frac=lio)
                lju = e_out(prog(t, A.jupiter, A.jupiter + 0.5))
                P.pastilla(lz, -300, -175, "Júpiter", px=38, k=lju, fondo=(255, 236, 170), color=TINTA)
                ke = e_out(prog(t, A.estirada - 0.1, A.estirada + 0.5))
                if ke > 0.02:
                    P.pastilla(lz, 40, -225, "estirada y frotada", px=36, k=ke, fondo=ORO, color=TINTA)
                kc = pop(t, A.cuatrocientos - 0.3, 0.4)
                if kc > 0.02:
                    n = int(400 * e_out(prog(t, A.cuatrocientos - 0.2, A.volcanes + 0.5)))
                    P.pastilla(lz, 60, 220, f"más de {n} volcanes", px=44, k=kc, fondo=(255, 186, 120), color=TINTA)
            lz.trazo(np.vstack([q, q[:1]]), (255, 255, 255), 5.0, afinar=False, temblor=0.0)


# ---------------------------------------------------------------- volcanes y terremotos de la Tierra
def volcan(lz, t, x, y, ang, s, k, seed):
    with lz.grupo(x, y, s, ang + math.pi / 2):
        lz.relleno(np.array([[-46, 8], [-12, -56], [12, -56], [46, 8]]), (122, 82, 84))
        lz.relleno(np.array([[-46, 8], [-12, -56], [-2, -56], [-14, 8]]), oscurecer((122, 82, 84), 0.2), alfa=0.8)
        lz.relleno(elipse(0, -56, 14, 6, 0, 16), (255, 150, 60))
        if k > 0.02:
            lz.halo(0, -60, 110 * k, (255, 140, 60), alfa=0.75 * k, r0=0.1)
            lz.trazo(np.array([[0, -56], [6, -30], [-4, -4]]), (255, 160, 70), 7, afinar=True, temblor=0.0)
            for i in range(18):
                ph = ((t * 1.1 + i / 18 + seed * 0.31) % 1.0)
                yy = -60 - (170 * math.sin(ph * math.pi * 0.5)) * k
                xx = (h01(i, 1, seed) - 0.5) * 150 * ph * k
                if ph < 0.55:
                    lz.relleno(circulo(xx, yy, (4 + 5 * h01(i, 2, seed)) * k, 10), (255, 190, 90))
                else:
                    lz.relleno(circulo(xx * 0.8, yy - 24 * ph, (10 + 22 * ph) * k, 16), mezcla((200, 120, 90), (110, 90, 120), ph),
                               alfa=0.75 * (1 - 0.5 * ph))


def final_volcanes(lz, t, E, r):
    kt = ventana(t, A.terremotos - 0.15, A.volcanes2 + 1.6, 0.25, 0.7)
    kv = pop(t, A.volcanes2 - 0.2, 0.45) * ventana(t, A.volcanes2 - 0.2, E_CAIDA + 0.6, 0.2, 0.6)
    for j, (aa, s, sd) in enumerate(((-2.15, 0.9, 1), (-1.55, 1.1, 2), (-0.95, 0.85, 3))):
        kc = pop(t, A.volcanes2 - 0.3 + 0.18 * j, 0.4) * (1 - e_in(prog(t, E_CAIDA + 0.2, E_CAIDA + 0.8)))
        if kc > 0.02:
            px_, py_ = E[0] + r * 0.985 * math.cos(aa), E[1] + r * 0.985 * math.sin(aa)
            volcan(lz, t, px_, py_, aa, s * kc, kv, sd)
    if kt > 0.02:
        for j in range(3):
            u = ((t - A.terremotos) * 0.9 + j / 3.0) % 1.0
            for aa in (-1.9, -1.2):
                px_, py_ = E[0] + r * math.cos(aa), E[1] + r * math.sin(aa)
                P.onda(lz, px_, py_, 30 + 220 * u, 7.0, (255, 214, 150), alfa=0.7 * kt * (1 - u))
    fo = 1 - e_in(prog(t, E_CAIDA - 0.3, E_CAIDA + 0.4))
    ktp = pop(t, A.terremotos - 0.1, 0.4) * (1 - e_in(prog(t, A.volcanes2 - 0.2, A.volcanes2 + 0.1))) * fo
    P.pastilla(lz, E[0] - 230, 150, "terremotos", px=42, k=ktp, fondo=(255, 236, 170), color=TINTA)
    kvp = pop(t, A.volcanes2, 0.4) * fo
    P.pastilla(lz, E[0] + 90, 150, "volcanes", px=42, k=kvp, fondo=(255, 186, 120), color=TINTA)


# ---------------------------------------------------------------- la toma
def toma_7(lz, t):
    cam = C7
    bg = ME.fondo(t, cam, tono=1)
    fondo_gas(lz, t, cam, NEB7)
    E = E7
    p2 = p2_7(t)
    p1 = cam.a_pant(p_luna1(t))
    a2 = math.atan2(p2[1] - E[1], p2[0] - E[0])
    a1 = math.atan2(p1[1] - E[1], p1[0] - E[0])
    K.orbita(lz, E[0], E[1], R2 * cam.z, R2 * cam.z, 0, ORO, 3.0, alfa=0.35, fase=t * 26)
    fl = flex(t)
    cal = calor_t(t)
    ab = abre_t(t)
    quake = ventana(t, A.terremotos - 0.15, A.volcanes2 + 1.6, 0.25, 0.7)
    jit = (5 * quake * math.sin(t * 43), 4 * quake * math.cos(t * 37))
    tierra_corte(lz, t, E, R7, a2, a1, 0.8, 4.4, ab, fl, cal, jit)
    # la 2.ª luna (grande, cerca) con el tirón hacia la Tierra
    K.cuerpo_rocoso(lz, p2[0], p2[1], MR * cam.z, "ceniza", seed=5, ang_luz=LUZ, rot=0.07 * t + 5)
    kt = ventana(t, A.vaiven - 0.2, A.parar + 0.6, 0.3, 0.5)
    if kt > 0.02:
        d = p2 - E
        u = d / max(1.0, float(np.hypot(*d)))
        pul = 0.85 + 0.15 * math.sin(t * 5)
        K.flecha(lz, p2 - u * (MR * cam.z + 18), p2 - u * (MR * cam.z + 18 + 170 * pul), ORO, ancho=11, alfa=kt, capa=2)
    friccion(lz, t, E, R7, ventana(t, A.frotaria - 0.1, A.calor_w + 3.5, 0.3, 0.6))
    # rótulos de las capas y de «decenas de centímetros»
    kcm = ventana(t, A.decenas - 0.1, A.cm_c + 0.9, 0.3, 0.4)
    if kcm > 0.02:
        P.pastilla(lz, E[0] - 40, E[1] - R7 - 60, "unas decenas de cm", px=40, k=kcm, fondo=(255, 255, 255), color=TINTA)
        K.flecha(lz, np.array([E[0] - 40, E[1] - R7 - 30]), np.array([E[0] - 40, E[1] - R7 + 4 + 14 * fl]), ORO, ancho=7,
                 alfa=kcm, capa=2)
    kcr = ventana(t, A.roca_c + 0.4, A.sube + 0.9, 0.3, 0.4)
    if kcr > 0.02:
        for txt, rho, dy, col in (("núcleo", 0.30, 70, NUC2), ("manto", 0.78, 165, (255, 186, 120)),
                                  ("corteza", 0.985, 260, (210, 180, 170))):
            a = AW + (0.30 if rho > 0.9 else (-0.10 if rho < 0.5 else 0.12))
            q0 = E + rho * R7 * np.array([math.cos(a), math.sin(a)])
            K.etiqueta(lz, q0[0], q0[1], txt, dx=1230.0 - q0[0], dy=E[1] + dy - q0[1], px=36, fondo=col, frac=kcr)
    termo(lz, t, ventana(t, A.frotaria - 0.2, E_CAIDA + 1.0, 0.4, 0.8))
    final_volcanes(lz, t, E, R7)
    inset_io(lz, t)
    kuri6(lz, t, KURI7, 1.0, E, boca=0.6 * ventana(t, A.terremotos, A.volcanes2 + 1.4, 0.2, 0.5))
    return bg
