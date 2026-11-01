# -*- coding: utf-8 -*-
"""Toma 8 «caída» (229,1-281,5 s): la cámara se aleja de la Tierra con corte (empalme con la toma 7) hasta `C8`. La Luna se
aleja (marea adelantada que la empuja), una luna que gira al revés / más rápido cae (marea atrasada), recuadro de Fobos, el
límite de Roche (9 500 y 18 400 km) con un recuadro donde la luna se estira, se parte y forma un anillo que se inclina hasta
verse como el de Saturno (recuadro de referencia) y las rocas que llueven sobre la Tierra. Mundo: Tierra en el origen,
`ER`=100 px (≈ 63,7 km/px solo para las cotas de Roche; las órbitas de las lunas no van a escala)."""
import math

import numpy as np

import plano as P
import kz_espacio as K
from plano import mezcla, aclarar, oscurecer
from motor import W, H, prog, clamp01, lerp, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, smooth, h01
from mundo_comun import Cam, kf, pop, ventana, campana, mezclar_cam
from anclas import A, E_CALOR, E_CAIDA, E_CHOQUE
import mundo_espacio as ME
import mundo_mareas as MM
import mundo_calor as MC
from mundo_espacio import ER, MR, RL, LUZ, AZUL, ORO, TINTA, MENTA, ROSA, LIN, chip, fantasma, trail
from mundo_mareas import C7, kuri6, fondo_gas

ROJO = (255, 96, 120)
C8 = Cam((0, 0), (640, 540), 1.3)
R_IN = 9500.0 / 6371.0 * ER                  # límite rígido (≈ 149 px)
R_OUT = 18400.0 / 6371.0 * ER                # límite fluido (≈ 289 px)
NEB8 = [(500, 300, 760, (70, 60, 210), 41, 0.50), (1500, 780, 660, (190, 70, 140), 42, 0.40),
        (1250, 250, 600, (60, 120, 220), 43, 0.30)]
KURI8 = (170.0, 965.0)


# ======================================================================== lunas del mundo en la toma 8
C8B = Cam((0, 0), (640, 540), 1.9)          # acercamiento al anillo y a las rocas (empalma con la toma 9)


def cam8(t):
    c = mezclar_cam(C7, C8, e_inout(prog(t, E_CAIDA + 0.2, E_CAIDA + 2.7)))
    return mezclar_cam(c, C8B, e_inout(prog(t, A.anillos + 0.4, A.preciosos + 1.1)))


def r1_8(t):
    return RL + 40.0 * e_inout(prog(t, A.aleja - 0.5, A.delante_c + 6.0))


def ang1_8(t):
    return 0.006 * (t - E_CAIDA)


def r2_8(t):
    return float(kf(t, [(E_CAIDA, 350.0), (A.reves - 1.1, 350.0), (A.acerca_c + 0.8, 328.0), (A.cerca_c + 0.4, 312.0),
                        (A.frontera, 297.0), (A.roche + 0.0, 289.0), (A.estira_c + 0.5, 264.0), (A.mantiene, 226.0),
                        (A.nueve + 0.4, 196.0), (A.cruzarlo - 0.1, 152.0), (A.parte, 140.0)], ease=LIN))


_TT = np.arange(E_CAIDA - 0.5, E_CHOQUE + 4.0, 0.02)
_W2 = np.array([0.30 * (350.0 / r2_8(t)) ** 1.5 * float(kf(t, [(A.reves - 1.1, 1.0), (A.reves + 0.9, -1.0)])) for t in _TT])
_A2 = 0.194 + np.cumsum(_W2) * 0.02


def ang2_8(t):
    return float(np.interp(t, _TT, _A2))


def p1_8(t):
    return np.array(K.pos_orbita(0, 0, r1_8(t), r1_8(t), 0, ang1_8(t)))


def p2_8(t):
    r = r2_8(t)
    return np.array(K.pos_orbita(0, 0, r, r, 0, ang2_8(t)))


def estira_t(t):
    return clamp01((R_OUT - r2_8(t)) / (R_OUT - R_IN))


def rompe_t(t):
    return e_out(prog(t, A.parte - 0.2, A.parte + 2.4))


def off_marea(t):
    """Desfase del abultamiento respecto de la luna: adelantado (+) para la Luna que se aleja, atrasado para la que cae."""
    return 0.35


def flecha_arco(lz, cx, cy, R, a0, a1, color, ancho=7.0, alfa=1.0, frac=1.0):
    n = 32
    aa = a0 + (a1 - a0) * clamp01(frac)
    pts = np.array([[cx + R * math.cos(a0 + (aa - a0) * k / n), cy + R * math.sin(a0 + (aa - a0) * k / n)] for k in range(n + 1)])
    if len(pts) < 3 or abs(a1 - a0) * clamp01(frac) < 0.08:
        return
    lz.trazo(pts, color, ancho, afinar=False, temblor=0.0, capa=2)
    d = pts[-1] - pts[-2]
    u = d / max(1e-6, float(np.hypot(*d)))
    nv = np.array([-u[1], u[0]])
    lz.relleno(np.array([pts[-1] + u * ancho * 1.4, pts[-1] + nv * ancho * 1.9, pts[-1] - nv * ancho * 1.9]), color, alfa=alfa, capa=2)


# ======================================================================== recuadros
def panel(lz, t, k, cx, cy, w, h, dim=True):
    """Marco de recuadro (devuelve el contexto de dibujo); el contenido se pinta dentro de `lz.recorte(q)`."""
    return rect_red(-w / 2, -h / 2, w, h, 40)


def inset_fobos(lz, t):
    k = pop(t, A.fobos - 0.5, 0.45) * (1 - e_in(prog(t, A.siglo + 1.2, A.siglo + 1.6)))
    if k < 0.02:
        return
    cx, cy, w, h = 1300.0, 410.0, 820.0, 540.0
    q = rect_red(-w / 2, -h / 2, w, h, 40)
    mx, my = -200.0, 25.0
    with lz.capa(2):
        lz.relleno(rect_red(-10, -10, W + 20, H + 20, 0), (10, 8, 34), alfa=0.5 * min(1.0, k))
        with lz.grupo(cx, cy, k):
            lz.relleno(q, (22, 14, 44), alfa=0.97)
            with lz.recorte(q):
                for i in range(22):
                    lz.relleno(circulo(-w / 2 + w * h01(i, 1, 9), -h / 2 + h * h01(i, 2, 9), 2.0 + 2 * h01(i, 3, 9), 8),
                               (230, 235, 255), alfa=0.7)
                K.nebulosa(lz, 220, -120, 440, (200, 80, 60), seed=8, alfa=0.35, capa=2)
                K.cuerpo_rocoso(lz, mx, my, 138, "rojiza", seed=7, ang_luz=LUZ, rot=0.1 * t)
                R = 214.0 - 20.0 * e_inout(prog(t, A.baja_f, A.siglo + 1.0))
                th_ = np.linspace(0, 2 * np.pi, 140)
                P.discontinua(lz, np.stack([mx + R * np.cos(th_), my + R * np.sin(th_)], 1), AZUL, 3.5, 14, 10, fase=-t * 26)
                ang = 1.5 + 1.9 * (t - A.fobos)
                K.estela(lz, mx, my, R, R, 0, ang, color=(255, 214, 90), largo=0.9, ancho=9.0)
                kp = pop(t, A.fobos - 0.1, 0.4)
                fx, fy = mx + R * math.cos(ang), my + R * math.sin(ang)
                K.roca(lz, fx, fy, 30 * kp, seed=4, rot=t * 1.3, tipo="ceniza", ang_luz=LUZ, alargada=1.3)
                lm = e_out(prog(t, A.marte, A.marte + 0.5))
                P.pastilla(lz, mx, my - 172, "Marte", px=38, k=lm, fondo=(255, 190, 160), color=TINTA)
                lf = e_out(prog(t, A.fobos, A.fobos + 0.5))
                P.linea_llamada(lz, (fx, fy), (200.0, -150.0), frac=lf)
                P.pastilla(lz, 200, -150, "Fobos", px=38, k=lf, fondo=(255, 255, 255), color=TINTA)
                kc = pop(t, A.dos_m - 0.3, 0.45)
                if kc > 0.02:
                    P.pastilla(lz, 160, 150, "1,8 m cada siglo", px=44, k=kc, fondo=ORO, color=TINTA)
                    K.flecha(lz, np.array([160.0, 60.0]), np.array([160.0, 60.0 + 54 * kc]), ORO, ancho=8, alfa=kc)
            lz.trazo(np.vstack([q, q[:1]]), (255, 255, 255), 5.0, afinar=False, temblor=0.0)


def inset_estira(lz, t):
    k = pop(t, A.dentro - 0.3, 0.45) * (1 - e_in(prog(t, A.unida + 1.1, A.unida + 1.5)))
    if k < 0.02:
        return
    cx, cy, w, h = 1400.0, 300.0, 700.0, 440.0
    q = rect_red(-w / 2, -h / 2, w, h, 40)
    est = e_inout(prog(t, A.dentro + 0.4, A.mantiene + 0.4))
    with lz.capa(2):
        with lz.grupo(cx, cy, k):
            lz.relleno(q, (16, 14, 52), alfa=0.97)
            with lz.recorte(q):
                for i in range(18):
                    lz.relleno(circulo(-w / 2 + w * h01(i, 1, 9), -h / 2 + h * h01(i, 2, 9), 2.0 + 2 * h01(i, 3, 9), 8),
                               (230, 235, 255), alfa=0.7)
                lz.relleno(circulo(-470, 20, 270, 80), (60, 130, 230))
                lz.relleno(circulo(-470, 20, 262, 80), (86, 168, 246), alfa=0.6)
                K.luna_rota(lz, 90, 20, 92, est, math.pi, t, seed=5, tipo="ceniza", ang_luz=LUZ)
                kg = pop(t, A.estira_c - 0.1, 0.4)
                if kg > 0.02:
                    for dx_, sgn in ((-1, -1), (1, 1)):
                        x0 = 90 + dx_ * (92 * (1 + 0.9 * est) + 22)
                        K.flecha(lz, np.array([x0, 20.0]), np.array([x0 + sgn * 70 * (0.5 + 0.8 * est) * kg, 20.0]), ORO, ancho=11,
                                 alfa=kg)
                kp = pop(t, A.propia - 0.1, 0.4)
                if kp > 0.02:
                    hy = 92 / (1 + 0.45 * est) + 18
                    for sgn in (-1, 1):
                        y0 = 20 + sgn * (hy + 62)
                        K.flecha(lz, np.array([90.0, y0]), np.array([90.0, y0 - sgn * 50 * kp]), MENTA, ancho=10, alfa=kp)
                P.pastilla(lz, 90, -178, "tirón de la Tierra", px=36, k=kg, fondo=ORO, color=TINTA)
                P.pastilla(lz, 90, 178, "su propia gravedad", px=36, k=kp, fondo=MENTA, color=TINTA)
                kw = pop(t, A.unida - 0.3, 0.4)
                P.pastilla(lz, -200, -110, "gana la Tierra", px=36, k=kw, fondo=ROSA, color=TINTA)
            lz.trazo(np.vstack([q, q[:1]]), (255, 255, 255), 5.0, afinar=False, temblor=0.0)


def inset_saturno(lz, t):
    k = pop(t, A.saturno_c - 0.4, 0.45) * (1 - e_in(prog(t, A.brillantes + 0.8, A.brillantes + 1.2)))
    if k < 0.02:
        return
    cx, cy, w, h = 1500.0, 270.0, 640.0, 400.0
    q = rect_red(-w / 2, -h / 2, w, h, 40)
    with lz.capa(2):
        with lz.grupo(cx, cy, k):
            lz.relleno(q, (16, 16, 54), alfa=0.97)
            with lz.recorte(q):
                for i in range(16):
                    lz.relleno(circulo(-w / 2 + w * h01(i, 1, 9), -h / 2 + h * h01(i, 2, 9), 2.0 + 2 * h01(i, 3, 9), 8),
                               (230, 235, 255), alfa=0.7)
                K.anillo(lz, 0, 20, 118, 205, tilt=-0.22, incl=0.28, mitad=0)
                K.planeta_gas(lz, 0, 20, 100, t, "saturno", seed=2)
                K.anillo(lz, 0, 20, 118, 205, tilt=-0.22, incl=0.28, mitad=1)
                P.pastilla(lz, 0, -150, "Saturno", px=40, k=e_out(prog(t, A.saturno_c, A.saturno_c + 0.4)), fondo=(255, 236, 170),
                           color=TINTA)
            lz.trazo(np.vstack([q, q[:1]]), (255, 255, 255), 5.0, afinar=False, temblor=0.0)


# ======================================================================== cuerpos (Tierra, anillo, lunas)
def anillo_roto(lz, t, E, z, mitad, incl, tilt, k=1.0):
    u = e_inout(prog(t, A.parte + 0.4, A.reparten + 1.2))
    if u < 0.01 or k < 0.01:
        return
    n = int((30 + 200 * u) * k)
    K.anillo(lz, E[0], E[1], 150 * z, 192 * z, tilt=tilt, incl=incl, mitad=mitad, col=(190, 176, 200), alfa=0.35 * u * k)
    K.anillo_escombros(lz, E[0], E[1], 148 * z, 196 * z, t, n=n, seed=3, incl=incl, tilt=tilt, mitad=mitad, tam=7.0 * z / 1.45,
                       brillo=0.6 * (1 - e_inout(prog(t, A.anillo_c, A.anillos + 1.5))))


def lluvia_gorda(lz, t, E, rs, z, incl, tilt, k):
    """Rocas del anillo que caen sobre la Tierra: estela incandescente, destello al chocar."""
    n = int(6 + 10 * k)
    for i in range(n):
        ph = (t * 0.62 + h01(i, 1, 6) * 3.0) % 1.0
        a = h01(i, 2, 6) * 6.2832
        rr = 178 * z
        p0 = E + np.array([rr * math.cos(a), rr * math.sin(a) * max(incl, 0.45)])
        p1_ = E + np.array([math.cos(a), math.sin(a)]) * rs * 0.92
        u = ph ** 1.4
        p = p0 + (p1_ - p0) * u
        cola = (p - p0) * 0.0
        for j in range(1, 6):
            uu = max(0.0, u - 0.06 * j)
            q = p0 + (p1_ - p0) * uu
            lz.relleno(circulo(q[0], q[1], (11 - 1.6 * j) * (0.7 + 0.5 * h01(i, 3, 6)), 12), mezcla((255, 190, 90), (255, 90, 50), j / 6),
                       alfa=0.75 - 0.11 * j)
        if u < 0.97:
            K.roca(lz, p[0], p[1], (9 + 8 * h01(i, 4, 6)) * k, seed=i, rot=t * 2 + i, tipo="ceniza", ang_luz=LUZ, alargada=1.2)
        else:
            f = (u - 0.97) / 0.03
            lz.halo(p1_[0], p1_[1], 70 * (0.5 + f), (255, 170, 80), alfa=0.8, r0=0.1, capa=2)


def toma_8(lz, t):
    cam = cam8(t)
    z = cam.z
    E = cam.a_pant((0, 0))
    rs = ER * z
    bg = ME.fondo(t, cam)
    fondo_gas(lz, t, cam, NEB8)
    p1 = cam.a_pant(p1_8(t))
    p2 = cam.a_pant(p2_8(t))
    r1, r2 = r1_8(t), r2_8(t)
    a1 = math.atan2(p1[1] - E[1], p1[0] - E[0])
    a2 = math.atan2(p2[1] - E[1], p2[0] - E[0])
    r_m = MR * z
    # --- órbitas
    ko1 = 1.0
    K.orbita(lz, E[0], E[1], r1 * z, r1 * z, 0, AZUL, 3.0, alfa=0.42, fase=t * 22)
    if t < A.parte + 0.5:
        K.orbita(lz, E[0], E[1], r2 * z, r2 * z, 0, ROSA if t > A.reves - 1.0 else ORO, 3.0, alfa=0.55, fase=-t * 26)
    # --- Roche
    fr_ = 1 - e_in(prog(t, A.anillo_c + 0.3, A.anillos + 0.9))
    kr = e_inout(prog(t, A.frontera - 0.3, A.roche + 0.2)) * fr_
    kz = e_out(prog(t, A.nueve - 0.6, A.nueve + 0.4)) * fr_
    ka = e_inout(prog(t, A.limite - 0.1, A.limite + 0.6)) * (1 - 0.0 * kz)
    if kr > 0.01:
        if kz > 0.01:
            lz.relleno(MB_anillo(E[0], E[1], R_IN * z, R_OUT * z), ROJO, alfa=0.13 * kz)
        th_ = np.linspace(0, 2 * np.pi, 160)
        P.discontinua(lz, np.stack([E[0] + R_OUT * z * np.cos(th_), E[1] + R_OUT * z * np.sin(th_)], 1), ROJO, 4.5, 20, 12,
                      fase=t * 24, frac=kr)
        if kz > 0.01:
            P.discontinua(lz, np.stack([E[0] + R_IN * z * np.cos(th_), E[1] + R_IN * z * np.sin(th_)], 1), (255, 150, 90), 4.5, 20,
                          12, fase=-t * 24, frac=kz)
    # --- Tierra (con marea adelantada / atrasada y, al empezar, la cuña que se cierra)
    ab = 1 - e_inout(prog(t, E_CAIDA + 0.05, E_CAIDA + 1.1))
    cal = MC.calor_t(t) * (1 - prog(t, E_CAIDA, E_CAIDA + 1.6))
    kdir = float(kf(t, [(A.reves - 1.1, 1.0), (A.reves + 0.9, -1.0)]))
    f2 = min(4.4, 0.8 * (350.0 / r2) ** 3) * (1 - rompe_t(t))
    off1 = 0.5 * e_inout(prog(t, A.marea_c - 0.5, A.marea_c + 0.6)) * (1 - e_inout(prog(t, A.reves - 1.0, A.reves)))
    off2 = 0.5 * e_inout(prog(t, A.reves - 0.2, A.reves + 0.8))
    lunas = [(a1 + off1, 0.8), (a2 + off2, f2)]
    ring_mitad0 = ring_mitad1 = False
    tilt_k = e_inout(prog(t, A.anillos - 0.4, A.anillos + 1.8))
    incl = lerp(1.0, 0.30, tilt_k)
    tilt = -0.25 * tilt_k
    if t > A.parte + 0.4:
        anillo_roto(lz, t, E, z, 0, incl, tilt)
    if ab > 0.02:
        MC.tierra_corte(lz, t, E, rs, a2, a1, 0.8, 4.4, ab, 0.0, cal)
    else:
        K.tierra_marea(lz, E[0], E[1], rs, t, lunas, rot=0.45 * t, ang_luz=LUZ, amp=0.2)
    if t > A.parte + 0.4:
        anillo_roto(lz, t, E, z, 1, incl, tilt)
    # --- lluvia de rocas sobre la Tierra
    kl = e_inout(prog(t, A.peligrosos - 0.3, A.lloverian + 0.6))
    if kl > 0.02:
        lluvia_gorda(lz, t, E, rs, z, incl, tilt, kl)
    kbr = ventana(t, A.preciosos - 0.1, A.brillantes + 1.2, 0.2, 0.6)
    if kbr > 0.02:
        for j in range(5):
            th = 1.1 * j + 0.5
            q_ = E + np.array([178 * z * math.cos(th), 178 * z * math.sin(th) * incl])
            kd_ = campana(t, A.preciosos + 0.35 * j, A.preciosos + 0.35 * j + 1.0)
            if kd_ > 0.02:
                K.destello(lz, q_[0], q_[1], 36 * kd_, t + j, alfa=min(1.0, kd_ * 1.4))
    # --- Luna 1 y luna 2
    K.cuerpo_rocoso(lz, p1[0], p1[1], r_m, "luna", seed=1, ang_luz=LUZ, rot=0.07 * t)
    if t < A.parte + 2.6:
        ang_t = math.atan2(E[1] - p2[1], E[0] - p2[0])
        esti = estira_t(t)
        rmp = rompe_t(t)
        K.luna_rota(lz, p2[0], p2[1], r_m, esti, ang_t, t, seed=5, tipo="ceniza", rompe=rmp, ang_luz=LUZ)
    # ---------------------------------------------------------------- anotaciones
    kg = ventana(t, A.no_quedan - 0.1, A.aleja + 1.0, 0.3, 0.5)
    if kg > 0.02:
        tg = A.no_quedan
        for pw, col in ((p1_8(tg), (255, 255, 255)), (p2_8(tg), (255, 255, 255))):
            pg = cam.a_pant(pw)
            fantasma(lz, pg[0], pg[1], r_m * 1.1, t, alfa=kg)
        u1 = (p1 - E) / max(1.0, float(np.hypot(*(p1 - E))))
        u2 = (p2 - E) / max(1.0, float(np.hypot(*(p2 - E))))
        K.flecha(lz, p1 + u1 * (r_m + 14), p1 + u1 * (r_m + 14 + 70 * kg), MENTA, ancho=9, alfa=kg, capa=2)
        K.flecha(lz, p2 - u2 * (r_m + 14), p2 - u2 * (r_m + 14 + 70 * kg), ROSA, ancho=9, alfa=kg, capa=2)
    # fase B: la Luna se aleja
    kb = ventana(t, A.aleja - 0.1, A.delante_c + 0.8, 0.3, 0.6)
    if kb > 0.02:
        chip(lz, t, float(np.clip(p1[0], 220, 1700)), float(np.clip(p1[1] - r_m - 56, 70, 1000)), "3,8 cm al año", A.cuatro_c - 0.2,
             A.delante_c + 1.0, px=40, fondo=MENTA)
        u1 = (p1 - E) / max(1.0, float(np.hypot(*(p1 - E))))
        K.flecha(lz, p1 + u1 * (r_m + 16), p1 + u1 * (r_m + 16 + 80 * kb), MENTA, ancho=9, alfa=kb, capa=2)
    kd = ventana(t, A.marea_c - 0.2, A.delante_c + 1.2, 0.3, 0.6)
    if kd > 0.02:
        ab_ = a1 + off1
        u_1 = np.array([math.cos(a1), math.sin(a1)])
        u_b = np.array([math.cos(ab_), math.sin(ab_)])
        P.discontinua(lz, np.array([E + u_1 * rs * 1.25, p1 - u_1 * (r_m + 8)]), (255, 255, 255), 3.0, 12, 10, fase=t * 20, frac=kd)
        P.discontinua(lz, np.array([E + u_b * rs * 1.3, E + u_b * rs * 2.4]), ORO, 4.0, 12, 10, fase=t * 20, frac=kd)
        kp = pop(t, A.empuja - 0.2, 0.4)
        tg = np.array([-math.sin(a1), math.cos(a1)])
        if kp > 0.02:
            K.flecha(lz, p1 + tg * (r_m + 14), p1 + tg * (r_m + 14 + 120 * kp), ORO, ancho=11, alfa=kp, capa=2)
            P.pastilla(lz, float(np.clip(p1[0] + tg[0] * 170, 150, 1770)), float(np.clip(p1[1] + tg[1] * 170, 70, 1000)), "empuja", px=38,
                       k=kp, fondo=ORO, color=TINTA)
    # fase C: gira al revés / más rápido
    kc = ventana(t, A.reves - 0.4, A.acerca_c + 1.3, 0.3, 0.6)
    if kc > 0.02:
        flecha_arco(lz, E[0], E[1], rs * 1.5, 0.55, 2.55, MENTA, 8, kc, frac=kc)
        P.pastilla(lz, E[0], E[1] + rs * 1.5 + 56, "la Tierra gira así", px=36, k=pop(t, A.reves - 0.3, 0.4) * kc, fondo=MENTA,
                   color=TINTA)
        flecha_arco(lz, E[0], E[1], r2 * z * 1.0, a2 + 0.55, a2 - 0.35, ROSA, 9, kc, frac=kc)
        cx_ = float(np.clip(p2[0], 220, 1700))
        cy_ = float(np.clip(p2[1] - r_m - 56, 70, 1000))
        chip(lz, t, cx_, cy_, "al revés", A.reves - 0.2, A.rapido - 0.3, px=40, fondo=ROSA)
        chip(lz, t, cx_, cy_, "o más rápido", A.rapido - 0.2, A.acerca_c - 0.25, px=40, fondo=ROSA)
    kac = ventana(t, A.acerca_c - 0.1, A.acerca_c + 1.0, 0.3, 0.5)
    if kac > 0.02:
        u2 = (p2 - E) / max(1.0, float(np.hypot(*(p2 - E))))
        K.flecha(lz, p2 + u2 * (r_m + 14), p2 + u2 * (r_m + 14) - u2 * 90 * kac, ROSA, ancho=11, alfa=kac, capa=2)
        chip(lz, t, float(np.clip(p2[0], 220, 1700)), float(np.clip(p2[1] - r_m - 56, 70, 1000)), "se acerca", A.acerca_c - 0.1,
             A.acerca_c + 1.0, px=40, fondo=ROSA)
    # fase E/F: tirón creciente y Roche
    kt = ventana(t, A.cerca_c - 0.2, A.mantiene + 0.8, 0.3, 0.6)
    if kt > 0.02:
        K.flechas_marea(lz, E[0], E[1], rs, a2, fuerza=0.9 + 0.8 * clamp01((350 - r2) / 150), t=t)
    kp_ = pop(t, A.limite - 0.1, 0.4) * (1 - e_in(prog(t, A.estira_c, A.estira_c + 0.4)))
    if kp_ > 0.02:
        P.pastilla(lz, E[0], E[1] + R_OUT * z + 58, "límite de Roche", px=42, k=kp_, fondo=ROSA, color=TINTA)
    # cotas de 9 500 y 18 400 km
    for ang_c, rr, txt, t0, col in ((-0.80, R_IN, "9 500 km", A.nueve - 0.2, (255, 190, 140)),
                                    (2.75, R_OUT, "18 400 km", A.dieciocho - 0.2, (255, 160, 170))):
        kk = e_inout(prog(t, t0, t0 + 0.9)) * (1 - e_in(prog(t, A.cruzarlo + 0.4, A.cruzarlo + 1.0)))
        if kk > 0.02:
            u_c = np.array([math.cos(ang_c), math.sin(ang_c)])
            q = E + rr * z * u_c
            P.discontinua(lz, np.array([E, q]), col, 4.0, 12, 9, fase=-t * 20, frac=kk)
            lz.relleno(circulo(q[0], q[1], 9 * kk, 14), col)
            lz.relleno(circulo(E[0], E[1], 7 * kk, 14), (255, 255, 255))
            P.pastilla(lz, q[0] + u_c[0] * 108, q[1] + u_c[1] * 70, txt, px=38, k=pop(t, t0 + 0.4, 0.4), fondo=col, color=TINTA)
    kcen = ventana(t, A.centro - 0.2, A.centro + 1.4, 0.2, 0.4)
    if kcen > 0.02:
        P.pastilla(lz, E[0], E[1] + R_OUT * z + 62, "desde el centro de la Tierra", px=36, k=kcen, fondo=(255, 255, 255), color=TINTA)
    # fase H: se cruza el límite
    kx = campana(t, A.cruzarlo - 0.1, A.cruzarlo + 0.9)
    if kx > 0.01:
        P.onda(lz, p2[0], p2[1], r_m * (1.2 + 1.5 * kx), 7.0, ROJO, alfa=0.7 * kx)
    # recuadros
    inset_fobos(lz, t)
    inset_estira(lz, t)
    inset_saturno(lz, t)
    # restos de la toma 7
    if t < E_CAIDA + 0.9:
        MC.final_volcanes(lz, t, E, rs)
    if t < E_CAIDA + 2.0:
        MC.termo(lz, t, MC_termo_k(t))
    uk = e_inout(prog(t, E_CAIDA + 0.3, E_CAIDA + 2.6))
    pk = (lerp(MC.KURI7[0], KURI8[0], uk), lerp(MC.KURI7[1], KURI8[1], uk) - 80 * math.sin(math.pi * uk))
    kuri6(lz, t, pk, 1.0, E if t < A.fobos - 2 else p2, boca=campana(t, A.peligrosos - 0.2, A.rocas + 1.5), feliz=0.0)
    return bg


def MC_termo_k(t):
    return ventana(t, A.frotaria - 0.2, E_CAIDA + 1.0, 0.4, 0.8)


def MB_anillo(x, y, r0, r1, n=120):
    th = np.linspace(0, 2 * np.pi, n)
    o = np.stack([x + r1 * np.cos(th), y + r1 * np.sin(th)], 1)
    i = np.stack([x + r0 * np.cos(th), y + r0 * np.sin(th)], 1)
    return np.vstack([o, o[:1], i[::-1], i[-1:]])
