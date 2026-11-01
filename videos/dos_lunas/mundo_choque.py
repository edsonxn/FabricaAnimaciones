# -*- coding: utf-8 -*-
"""Tomas 9 «choque» (281,5-331,6 s) y 10 «cierre» (331,6-350,2 s).
9: dos lunas chocan entre ellas (sobre la Tierra con el anillo que se apaga); un reloj que retrocede y la cámara baja a la Luna real:
cara visible lisa con mares oscuros -> giro -> cara oculta con montañas y cráteres, corteza más gruesa (corte); la hipótesis de 2011
(luna de 1 200 km con regla frente a la Luna); la cámara sube al punto de equilibrio L4 (nace, se queda, la órbita cambia y el equilibrio
se rompe); vuelve a la Luna y un recuadro lateral enseña el choque lento («panqueque») mientras la cara oculta gira y aparece la
meseta; «hipótesis», «encaja»; 1 + 1 pegadas.
10: la cámara sube al espacio y cae a la misma playa nocturna de la toma 5, ahora con UNA luna (mar en calma, estrellas), tres tarjetas
de «con dos…» y Kuri que se sienta a mirar la Luna; fundido final."""
import math

import numpy as np

import fondos as F
import plano as P
import kz_espacio as K
from plano import mezcla, aclarar, oscurecer
from motor import W, H, prog, clamp01, lerp, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, smooth, h01
from mundo_comun import Cam, Sup, kf, pop, ventana, campana, mezclar_cam
from anclas import A, TOTAL, E_CHOQUE, E_CIERRE
import mundo_espacio as ME
import mundo_tierra as MT
import mundo_mareas as MM
import mundo_caida as MD
from mundo_espacio import ER, MR, RL, LUZ, AZUL, ORO, TINTA, MENTA, ROSA, LIN, chip, fantasma, marca_x, kuri_ui
from mundo_mareas import kuri6, fondo_gas
from mundo_caida import ROJO, C8, KURI8, flecha_arco

C8B = Cam((0, 0), (640, 540), 1.9)           # fin de la toma 8 / inicio de la 9
CL4 = Cam((0, 0), (820, 570), 0.85)          # encuadre de L4 (como en la toma 4)
ZM = 6.3                                     # zoom del primer plano de la Luna (radio ≈ 328 px)
PM = (700.0, 540.0)
T_X = A.choquen + 0.40                       # choque de las dos lunas
T_ZIN = (A.ya_paso - 0.25, A.caras + 0.35)  # zoom a la Luna
T_OUT = (A.mil_x + 1.2, A.nacio_x + 1.6)     # sube a L4
T_IN = (A.cambio + 2.4, A.cambio + 4.6)      # vuelve a la Luna
T_FLIP = (A.oculta - 0.45, A.oculta + 0.9)   # giro a la cara oculta
T_FLIP2 = (A.crater_x - 2.4, A.crater_x - 0.4)   # segundo giro (antes del choque lento)
NEB9 = [(500, 300, 760, (150, 70, 190), 51, 0.50), (1500, 780, 660, (230, 150, 70), 52, 0.35),
        (1250, 250, 600, (80, 90, 220), 53, 0.30)]
R_C = 250.0                                  # órbita de las dos lunas que chocan (mundo)
R_LC = 18.0                                  # radio de la luna compañera (1 200 km frente a 3 474 km -> 18 / 52)


# ======================================================================== la Luna real en la toma 9
def ang_m9(t):
    a0 = MD.ang1_8(288.0)
    return float(kf(t, [(288.0, a0), (303.0, -0.60), (E_CIERRE, -0.45)]))


def r_m9(t):
    return MD.r1_8(t) + float(kf(t, [(A.orbita_x + 0.0, 0.0), (A.cambio + 0.6, 150.0)]))


def pm9(t):
    r = r_m9(t)
    return np.array(K.pos_orbita(0, 0, r, r, 0, ang_m9(t)))


def rel_c(t):
    """Ángulo de la compañera respecto de la Luna: 60° (L4) hasta que se rompe el equilibrio; luego se va acercando."""
    return float(kf(t, [(A.cambio, math.pi / 3), (A.equilibrio_x2 + 0.2, math.pi / 3), (T_IN[0], 0.30)]))


def pc9(t):
    r = r_m9(t)
    return np.array(K.pos_orbita(0, 0, r, r, 0, ang_m9(t) + rel_c(t)))


def cam9(t):
    if t < T_ZIN[0]:
        return C8B
    pm = pm9(t)
    if t < T_ZIN[1]:
        u = e_inout(prog(t, *T_ZIN))
        return Cam(pm * u, (640 + 60 * u, 540), math.exp(lerp(math.log(1.9), math.log(ZM), u)))
    if t < T_OUT[0]:
        return Cam(pm, PM, ZM)
    if t < T_OUT[1]:
        u = e_inout(prog(t, *T_OUT))
        return Cam(pm * (1 - u), (lerp(PM[0], 820, u), lerp(PM[1], 570, u)), math.exp(lerp(math.log(ZM), math.log(0.85), u)))
    if t < T_IN[0]:
        return CL4
    if t < T_IN[1]:
        u = e_inout(prog(t, *T_IN))
        return Cam(pm * u, (lerp(820, PM[0], u), lerp(570, PM[1], u)), math.exp(lerp(math.log(0.85), math.log(ZM), u)))
    return Cam(pm, PM, ZM)


def rot_luna(t):
    """Giro de la Luna: visible (0) -> oculta (pi) en `T_FLIP`; vuelve a la visible antes de 2011 y otra vez a la oculta en el choque lento."""
    a = e_inout(prog(t, *T_FLIP))
    b = e_inout(prog(t, A.y2011 - 0.9, A.y2011 + 0.3))
    c = e_inout(prog(t, *T_FLIP2))
    return math.pi * (a - b + c) + 0.012 * (t - 287.0)


def pancake_k(t):
    return e_inout(prog(t, A.aplasto - 0.2, A.panqueque + 1.4))


def luna1(lz, t, cam, alfa=1.0):
    p = cam.a_pant(pm9(t))
    z = cam.z
    r = MR * z
    if not cam.visible(pm9(t), MR, margen=40):
        return p, r
    big = e_inout(prog(z, 2.0, 3.4))
    if big < 0.99:
        K.cuerpo_rocoso(lz, p[0], p[1], r, "luna", seed=1, ang_luz=LUZ, rot=0.07 * t, alfa=alfa * (1 - big))
    if big > 0.01:
        K.luna_dos_caras(lz, p[0], p[1], r, rot=rot_luna(t), ang_luz=LUZ, alfa=alfa * big, panqueque=pancake_k(t))
    return p, r


# ======================================================================== choque de las dos lunas (con la Tierra y el anillo)
def choque_lunas(lz, t, cam):
    z = cam.z
    E = cam.a_pant((0, 0))
    rs = ER * z
    th_x = -0.75
    r_c = MR * z * 0.9
    if t < T_X:
        s = (T_X - t)
        a_a = th_x - (0.55 * s + 0.19)
        a_b = th_x + (0.55 * s + 0.19)
        k = pop(t, A.otro_final - 0.3, 0.4)
        pa = E + R_C * z * np.array([math.cos(a_a), math.sin(a_a)])
        pb = E + R_C * z * np.array([math.cos(a_b), math.sin(a_b)])
        K.cuerpo_rocoso(lz, pa[0], pa[1], r_c * k, "ceniza", seed=5, ang_luz=LUZ, rot=0.07 * t + 5)
        K.cuerpo_rocoso(lz, pb[0], pb[1], r_c * k, "luna", seed=3, ang_luz=LUZ, rot=-0.06 * t)
        kt = ventana(t, A.dos_x, T_X - 0.1, 0.3, 0.1)
        if kt > 0.02:
            d = pb - pa
            u = d / max(1.0, float(np.hypot(*d)))
            K.flecha(lz, pa + u * (r_c + 12), pa + u * (r_c + 12 + 60 * kt), ORO, ancho=9, alfa=kt, capa=2)
            K.flecha(lz, pb - u * (r_c + 12), pb - u * (r_c + 12 + 60 * kt), ORO, ancho=9, alfa=kt, capa=2)
    else:
        pc = E + R_C * z * np.array([math.cos(th_x), math.sin(th_x)])
        dt = t - T_X
        kk = campana(t, T_X - 0.05, T_X + 1.1)
        if kk > 0.01:
            lz.halo(pc[0], pc[1], 300 * kk, (255, 230, 170), alfa=0.85 * kk, r0=0.0, capa=2)
            K.destello(lz, pc[0], pc[1], 100 * kk, t, alfa=min(1.0, kk * 1.4))
        for j in range(2):
            uu = prog(t, T_X + 0.1 * j, T_X + 1.4 + 0.1 * j)
            if 0 < uu < 1:
                P.onda(lz, pc[0], pc[1], 40 + 420 * e_out(uu), 8.0, (255, 214, 150), alfa=0.7 * (1 - uu))
        for i in range(30):
            a = h01(i, 1, 5) * 6.2832
            v = 150 + 380 * h01(i, 2, 5)
            r = v * (1 - math.exp(-dt * 1.7)) / 1.7
            q = pc + np.array([math.cos(a), math.sin(a)]) * r
            rad = (6 + 9 * h01(i, 3, 5)) * (1 - 0.6 * prog(dt, 0.0, 2.2))
            if rad > 1:
                lz.relleno(circulo(q[0], q[1], rad, 8), mezcla((255, 190, 120), (170, 160, 186), prog(dt, 0, 1.2)),
                           alfa=1 - 0.7 * prog(dt, 1.2, 2.4))


def reloj(lz, t):
    k = pop(t, A.ya_paso - 0.1, 0.4) * (1 - e_in(prog(t, T_ZIN[1] - 0.3, T_ZIN[1] + 0.3)))
    if k < 0.02:
        return
    cx, cy = 1520.0, 260.0
    with lz.capa(2):
        with lz.grupo(cx, cy, k):
            lz.relleno(circulo(0, 0, 96, 60), (255, 255, 255))
            lz.relleno(circulo(0, 0, 84, 60), (34, 28, 80))
            for i in range(12):
                a = i * math.pi / 6
                lz.trazo(np.array([[70 * math.cos(a), 70 * math.sin(a)], [80 * math.cos(a), 80 * math.sin(a)]]), (255, 255, 255), 4,
                         afinar=False, temblor=0.0)
            am = -(t - A.ya_paso) * 9.0
            lz.trazo(np.array([[0, 0], [62 * math.sin(am), -62 * math.cos(am)]]), ORO, 7, afinar=False, temblor=0.0)
            ah = am / 12
            lz.trazo(np.array([[0, 0], [38 * math.sin(ah), -38 * math.cos(ah)]]), (255, 255, 255), 9, afinar=False, temblor=0.0)
            lz.relleno(circulo(0, 0, 9, 14), ORO)
        P.rotulo(lz, cx + 150, cy - 10, "?", px=110, color=ORO, alfa=k)


# ======================================================================== primer plano de la Luna: rótulos
def pos_mar(rot):
    px, py, z = K._proy_esfera(0.25, 0.32, rot)
    return np.array([PM[0] + px * MR * ZM, PM[1] + py * MR * ZM]), z


def rotulos_caras(lz, t):
    kv = ventana(t, A.caras, T_FLIP[0] + 0.2, 0.3, 0.3)
    if kv > 0.02:
        P.pastilla(lz, 1330, 150, "dos caras muy distintas", px=40, k=pop(t, A.caras - 0.1, 0.4) * kv, fondo=(255, 255, 255), color=TINTA)
    kl = ventana(t, A.lisa - 0.2, T_FLIP[0] + 0.2, 0.3, 0.3)
    if kl > 0.02:
        P.pastilla(lz, 1380, 300, "cara visible: lisa", px=40, k=pop(t, A.lisa - 0.2, 0.4) * kl, fondo=MENTA, color=TINTA)
    km = ventana(t, A.mares_x - 0.1, T_FLIP[0] + 0.1, 0.3, 0.3)
    if km > 0.02:
        q, zq = pos_mar(rot_luna(t))
        P.linea_llamada(lz, (q[0], q[1]), (1280.0, 430.0), frac=km)
        P.pastilla(lz, 1380, 430, "mares oscuros", px=40, k=pop(t, A.mares_x - 0.1, 0.4) * km, fondo=(190, 200, 235), color=TINTA)
    ko = ventana(t, A.oculta - 0.1, A.corteza + 2.4, 0.3, 0.4)
    if ko > 0.02:
        P.pastilla(lz, 1380, 150, "cara oculta", px=40, k=pop(t, A.oculta - 0.1, 0.4) * ko, fondo=ROSA, color=TINTA)
    kc = ventana(t, A.montanas - 0.2, A.corteza + 0.2, 0.3, 0.4)
    if kc > 0.02:
        P.linea_llamada(lz, (PM[0] - 130, PM[1] + 170), (1160.0, 300.0), frac=kc)
        P.pastilla(lz, 1380, 300, "montañas y cráteres", px=40, k=pop(t, A.montanas - 0.2, 0.4) * kc, fondo=(255, 236, 170), color=TINTA)


def cara_espejo(lz, t):
    """Ventana redonda a la derecha con la OTRA cara de la Luna (la contraria a la grande: antes del giro enseña la oculta, después la
    visible). Rellena la mitad vacía del cuadro entre «dos caras» y la sección; cede su sitio al corte (mismo centro y radio)."""
    k = pop(t, A.caras + 0.5, 0.45) * (1 - e_in(prog(t, A.corteza - 0.75, A.corteza - 0.3)))
    if k < 0.02:
        return
    cx, cy, R = 1500.0, 700.0, 190.0
    with lz.capa(2):
        with lz.grupo(cx, cy, k):
            lz.relleno(circulo(0, 0, R + 22, 60), (16, 14, 52), alfa=0.9)
            lz.trazo(np.stack([(R + 22) * np.cos(np.linspace(0, 2 * np.pi, 120)), (R + 22) * np.sin(np.linspace(0, 2 * np.pi, 120))], 1),
                     (255, 255, 255), 4.0, afinar=False, temblor=0.0)
            K.luna_dos_caras(lz, 0.0, 0.0, R, rot=rot_luna(t) + math.pi, ang_luz=LUZ, alfa=1.0)
        P.pastilla(lz, cx, cy + R + 56, "la otra cara", px=38, k=k, fondo=(255, 255, 255), color=TINTA)


def corte_luna(lz, t):
    """Sección de la Luna: corteza fina por la cara visible y gruesa por la oculta."""
    k = pop(t, A.corteza - 0.5, 0.45) * (1 - e_in(prog(t, A.y2011 - 0.9, A.y2011 - 0.4)))
    if k < 0.02:
        return
    cx, cy, R = 1500.0, 700.0, 190.0
    esp = e_inout(prog(t, A.corteza - 0.2, A.gruesa + 0.5))
    with lz.capa(2):
        with lz.grupo(cx, cy, k):
            lz.relleno(circulo(0, 0, R + 22, 60), (16, 14, 52), alfa=0.9)
            lz.relleno(circulo(0, 0, R, 90), (120, 82, 96))                     # manto
            lz.relleno(circulo(0, 0, R * 0.42, 60), (255, 200, 120))            # núcleo
            n = 60
            # corteza: ancho 20 px del lado visible (izquierda) y hasta 78 px del lado oculto (derecha)
            for i in range(n):
                a0 = 2 * math.pi * i / n
                a1 = 2 * math.pi * (i + 1) / n
                am = (a0 + a1) / 2
                w = 18 + 62 * esp * (0.5 - 0.5 * math.cos(am))
                pts = np.array([[R * math.cos(a0), R * math.sin(a0)], [R * math.cos(a1), R * math.sin(a1)],
                                [(R - w) * math.cos(a1), (R - w) * math.sin(a1)], [(R - w) * math.cos(a0), (R - w) * math.sin(a0)]])
                lz.relleno(pts, (214, 212, 230))
            th = np.linspace(0, 2 * np.pi, 120)
            lz.trazo(np.stack([R * np.cos(th), R * np.sin(th)], 1), (255, 255, 255), 4.0, afinar=False, temblor=0.0)
        P.pastilla(lz, cx - 150, cy + R + 52, "fina", px=36, k=k * e_out(prog(t, A.corteza, A.corteza + 0.5)), fondo=MENTA, color=TINTA)
        P.pastilla(lz, cx + 150, cy + R + 52, "gruesa", px=36, k=k * e_out(prog(t, A.gruesa - 0.2, A.gruesa + 0.4)), fondo=ROSA, color=TINTA)
        P.pastilla(lz, cx, cy - R - 54, "corteza más gruesa", px=38, k=k * e_out(prog(t, A.corteza - 0.1, A.corteza + 0.4)), fondo=ORO,
                   color=TINTA)


# ======================================================================== 2011: la segunda luna frente a la Luna
def luz_idea(lz, t, x, y, k):
    if k < 0.02:
        return
    lz.halo(x, y - 8, 90 * k, (255, 230, 120), alfa=0.8 * k, r0=0.2, capa=2)
    with lz.capa(2):
        lz.relleno(circulo(x, y - 8, 30 * k, 24), (255, 232, 130))
        lz.relleno(rect_red(x - 14 * k, y + 20 * k, 28 * k, 18 * k, 4), (200, 200, 220))


def dos_mil_once(lz, t):
    if t < A.y2011 - 0.4 or t > A.pasaron + 0.3:
        return
    kf_ = 1 - e_in(prog(t, A.nacio_x - 0.3, A.nacio_x + 0.3))
    ky = pop(t, A.y2011 - 0.1, 0.45) * kf_
    P.pastilla(lz, 1300, 130, "2011", px=64, k=ky, fondo=ORO, color=TINTA)
    kc = pop(t, A.cientificos - 0.1, 0.4) * kf_
    if kc > 0.02:
        for i, (x, sc, col) in enumerate(((1480, 0.95, (240, 240, 250)), (1610, 1.0, (250, 232, 240)))):
            with lz.capa(2):
                P.humano(lz, x, 985, sc * kc, t + i, ropa=col, pelo=(70, 54, 50) if i else (190, 150, 90), brazo=0.4 + 0.3 * math.sin(t * 2 + i))
        luz_idea(lz, t, 1545, 790, pop(t, A.cientificos + 1.4, 0.4) * kf_)
    kg = pop(t, A.segunda_x - 0.2, 0.5) * kf_
    if kg > 0.02:
        c = np.array([1380.0, 470.0])
        rc = MR * ZM * (R_LC / MR) * kg
        K.cuerpo_rocoso(lz, c[0], c[1], rc, "ceniza", seed=9, ang_luz=LUZ, rot=0.05 * t, alfa=0.5)
        fantasma(lz, c[0], c[1], rc * 1.1, t, alfa=kg)
        K.destello(lz, c[0] + rc * 0.8, c[1] - rc * 0.9, 50 * campana(t, A.segunda_x, A.segunda_x + 1.0), t)
        P.rotulo(lz, c[0] + rc + 56, c[1] - rc * 0.8, "?", px=100, color=ORO, alfa=kg * (0.7 + 0.3 * math.sin(t * 5)))
        kr = e_inout(prog(t, A.mil_x - 0.2, A.km_x + 0.5)) * kf_
        if kr > 0.02:
            K.regla(lz, np.array([c[0] - rc, c[1] + rc + 64]), np.array([c[0] + rc, c[1] + rc + 64]), "≈ 1 200 km", px=38, frac=kr, lado=1)
            kk = e_inout(prog(t, A.km_x, A.km_x + 0.8)) * kf_
            if kk > 0.02:
                p = np.array(PM)
                K.regla(lz, np.array([p[0] - MR * ZM, p[1] - MR * ZM - 62]), np.array([p[0] + MR * ZM, p[1] - MR * ZM - 62]), "3 474 km",
                        px=38, frac=kk, lado=-1)


# ======================================================================== encuadre de L4
def escena_L4(lz, t, cam):
    z = cam.z
    E = cam.a_pant((0, 0))
    rs = ER * z
    th = ang_m9(t)
    r_o = r_m9(t)
    K.orbita(lz, E[0], E[1], r_o * z, r_o * z, 0, AZUL, 3.0, alfa=0.5, fase=t * 24)
    K.tierra_marea(lz, E[0], E[1], rs, t, [(th, 0.6)], rot=0.45 * t, ang_luz=LUZ, amp=0.08)
    pm = cam.a_pant(pm9(t))
    p4 = cam.a_pant(np.array(K.pos_orbita(0, 0, r_o, r_o, 0, th + math.pi / 3)))
    pc = cam.a_pant(pc9(t))
    rm = max(MR * z, 24.0)
    rc = max(R_LC * z, 22.0)
    ke_ = 1 - e_in(prog(t, T_IN[0] - 0.4, T_IN[0] + 0.3))
    # triángulo y marca L4
    ktri = e_inout(prog(t, A.puntos, A.equilibrio_x + 0.8)) * ke_ * (1 - e_inout(prog(t, A.equilibrio_x2 + 0.4, A.rompio + 0.3)))
    if ktri > 0.01:
        K.triangulo_equilibrio(lz, E, pm, p4, t, frac=ktri)
    k4 = pop(t, A.puntos - 0.1, 0.4) * ke_
    if k4 > 0.01:
        K.punto_lagrange(lz, p4[0], p4[1], "L4", t, s=k4 * (1 - 0.5 * e_inout(prog(t, A.rompio, A.rompio + 0.5))))
    kx = pop(t, A.rompio - 0.1, 0.3) * ke_
    if kx > 0.02:
        marca_x(lz, p4[0], p4[1], 1.3, kx)
    # la Luna
    K.cuerpo_rocoso(lz, pm[0], pm[1], rm, "luna", seed=1, ang_luz=LUZ, rot=0.07 * t)
    # la compañera: nace con destello, se queda en L4, luego se va acercando
    kn = pop(t, A.choque_g - 0.2, 0.5)
    if kn > 0.01:
        dn = campana(t, A.choque_g - 0.1, A.choque_g + 1.0)
        K.cuerpo_rocoso(lz, pc[0], pc[1], rc * kn, "ceniza", seed=9, ang_luz=LUZ, rot=0.2 * t)
        if dn > 0.01:
            K.destello(lz, pc[0], pc[1], 66 * dn, t, alfa=min(1.0, dn * 1.4))
            lz.halo(pc[0], pc[1], 150 * dn, (255, 230, 170), alfa=0.7 * dn, r0=0.0, capa=2)
        P.pastilla(lz, pc[0] + 120, pc[1] + 54, "segunda luna", px=38, k=kn * ke_ * e_out(prog(t, A.nacio_x + 0.6, A.nacio_x + 1.1)),
                   fondo=(255, 255, 255), color=TINTA)
    # el tiempo pasa y la órbita cambia
    kp = ventana(t, A.pasaron - 0.1, A.cambio + 2.0, 0.3, 0.5)
    if kp > 0.02:
        P.pastilla(lz, 1100, 120, "millones de años", px=44, k=kp, fondo=ORO, color=TINTA)
        P.rotulo(lz, 1300, 120, "", px=10)
        cx, cy = 1090.0 - 340, 120.0
        lz.relleno(circulo(cx, cy, 34, 40), (255, 255, 255), alfa=kp, capa=2)
        lz.relleno(circulo(cx, cy, 29, 40), (34, 28, 80), alfa=kp, capa=2)
        a_ = (t - A.pasaron) * 7.0
        lz.trazo(np.array([[cx, cy], [cx + 24 * math.sin(a_), cy - 24 * math.cos(a_)]]), ORO, 5, afinar=False, temblor=0.0, capa=2)
        lz.trazo(np.array([[cx, cy], [cx + 15 * math.sin(a_ / 12), cy - 15 * math.cos(a_ / 12)]]), (255, 255, 255), 6, afinar=False, temblor=0.0, capa=2)
    ko = ventana(t, A.orbita_x - 0.1, A.cambio + 1.4, 0.3, 0.5)
    if ko > 0.02:
        P.pastilla(lz, E[0] - 40, E[1] + r_o * z + 62, "la órbita cambia", px=40, k=ko, fondo=MENTA, color=TINTA)
        u_ = np.array([math.cos(th + 0.25), math.sin(th + 0.25)])
        K.flecha(lz, E + u_ * (r_o * z + 12), E + u_ * (r_o * z + 12 + 70 * ko), MENTA, ancho=9, alfa=ko, capa=2)
    kq = ventana(t, A.equilibrio_x2 - 0.2, A.rompio + 1.2, 0.3, 0.5)
    if kq > 0.02:
        P.pastilla(lz, p4[0] - 260, p4[1] - 60, "el equilibrio se rompe", px=38, k=kq, fondo=ROSA, color=TINTA)


# ======================================================================== recuadro lateral del choque lento
def inset_lateral(lz, t):
    k = pop(t, A.chocaron - 0.4, 0.45) * (1 - e_in(prog(t, A.hipotesis + 2.4, A.hipotesis + 2.8)))
    if k < 0.02:
        return
    cx, cy, w, h = 1450.0, 640.0, 820.0, 560.0
    q = rect_red(-w / 2, -h / 2, w, h, 40)
    t_c = A.crater_x + 0.9                          # contacto
    suelo = 150.0
    rc = 92.0
    with lz.capa(2):
        with lz.grupo(cx, cy, k):
            lz.relleno(q, (20, 16, 52), alfa=0.97)
            with lz.recorte(q):
                for i in range(20):
                    lz.relleno(circulo(-w / 2 + w * h01(i, 1, 9), -h / 2 + h * h01(i, 2, 9), 2.0 + 2 * h01(i, 3, 9), 8), (230, 235, 255),
                               alfa=0.7)
                # superficie de la Luna (arco enorme) con cráteres
                lz.relleno(circulo(0, suelo + 1700, 1700, 140), (150, 150, 182))
                lz.relleno(circulo(0, suelo + 1702, 1690, 140), (176, 176, 204))
                for i in range(7):
                    xx = -330 + 110 * i + 14 * math.sin(i * 3.1)
                    yy = suelo + 1700 - math.sqrt(max(1.0, 1700 ** 2 - xx ** 2)) + 22 + 16 * (i % 2)
                    lz.relleno(elipse(xx, yy, 34 + 10 * (i % 3), 9, 0, 20), (120, 120, 156))
                # la compañera baja despacio
                d = e_inout(prog(t, A.chocaron - 0.2, t_c))
                yc = lerp(-150.0, suelo - rc, d ** 1.2)
                ap = e_inout(prog(t, t_c, t_c + 1.5))
                sx, sy = 1 + 1.35 * ap, 1 - 0.66 * ap
                yb = suelo - rc * sy
                yb = yb if ap > 0 else yc
                lz.relleno(elipse(0, yb + (0 if ap > 0 else 0), rc * sx, rc * sy, 0, 48), (150, 140, 160))
                lz.relleno(elipse(-rc * 0.12 * sx, yb - rc * sy * 0.18, rc * sx * 0.88, rc * sy * 0.8, 0, 48), mezcla((150, 140, 160), (255, 244, 224), 0.65 * ap))
                for i in range(4):
                    lz.relleno(elipse((-0.5 + i * 0.33) * rc * sx, yb + 10 * math.sin(i), rc * 0.22 * sx, rc * 0.2 * sy, 0, 20), (120, 112, 130),
                               alfa=0.8 * (1 - ap))
                # polvo muy suave tras el contacto
                dp = prog(t, t_c, t_c + 2.4)
                if 0 < dp < 1:
                    for i in range(10):
                        a = -math.pi + math.pi * (i + 0.5) / 10
                        rr = (30 + 120 * dp) * (0.6 + 0.4 * h01(i, 1, 4))
                        lz.relleno(circulo(rr * math.cos(a) * 1.8, suelo + rr * math.sin(a) * 0.5 - 6, 8 + 12 * dp, 12), (210, 206, 222),
                                   alfa=0.5 * (1 - dp))
                # velocidad: flecha corta que casi no avanza + «muy despacio»
                kv = ventana(t, A.despacio - 0.2, t_c - 0.2, 0.3, 0.3)
                if kv > 0.02:
                    K.flecha(lz, np.array([0.0, yc - rc - 80]), np.array([0.0, yc - rc - 80 + 34 * kv]), ORO, ancho=8, alfa=kv)
                    P.pastilla(lz, 0, -215, "muy despacio", px=42, k=kv, fondo=ORO, color=TINTA)
                # sin cráter
                kcx = pop(t, A.crater_x - 0.1, 0.4) * (1 - e_in(prog(t, A.aplasto, A.aplasto + 0.4)))
                if kcx > 0.02:
                    lz.relleno(elipse(-250, suelo + 60, 70, 20, 0, 24), (100, 100, 140), alfa=0.9 * kcx)
                    marca_x(lz, -250, suelo + 60, 1.2, kcx)
                    P.pastilla(lz, -250, -30, "sin cráter", px=40, k=kcx, fondo=ROSA, color=TINTA)
                # panqueque
                kp = pop(t, A.panqueque - 0.1, 0.5)
                if kp > 0.02:
                    pan = (-250.0, -160.0)
                    with lz.grupo(pan[0], pan[1], 1.05 * kp):
                        for j, (yy, c) in enumerate(((16, (214, 150, 80)), (0, (230, 170, 96)), (-16, (240, 186, 110)))):
                            lz.relleno(elipse(0, yy, 74, 20, 0, 28), c)
                        lz.relleno(rect_red(-14, -42, 28, 14, 4), (255, 240, 150))
                        lz.relleno(elipse(18, -12, 40, 9, 0.1, 20), (170, 90, 40), alfa=0.9)
                    P.pastilla(lz, pan[0] + 220, pan[1] - 6, "panqueque", px=40, k=kp, fondo=(255, 244, 224), color=TINTA)
            lz.trazo(np.vstack([q, q[:1]]), (255, 255, 255), 5.0, afinar=False, temblor=0.0)


def hipotesis(lz, t):
    fin = min(A.dos_lunas_x, A.quizas_x - 0.15)        # se va antes de que entre la tarjeta «1 + 1» (misma esquina)
    k = pop(t, A.hipotesis - 0.2, 0.5) * (1 - e_in(prog(t, fin - 0.4, fin)))
    if k > 0.02:
        with lz.capa(2):
            with lz.grupo(1330, 200, k, -0.12):
                lz.relleno(rect_red(-190, -52, 380, 104, 22), ROSA, alfa=0.95)
                lz.relleno(rect_red(-178, -40, 356, 80, 16), (34, 28, 80), alfa=0.9)
                lz.texto("HIPÓTESIS", 0, 4, 56, "geo", color=(255, 255, 255), borde=None, temblor=0.0)
    ke = pop(t, A.encaja - 0.1, 0.4) * (1 - e_in(prog(t, fin - 0.4, fin)))
    if ke > 0.02:
        with lz.capa(2):
            with lz.grupo(1640, 196, ke):
                lz.relleno(circulo(0, 0, 54, 40), (110, 220, 150))
                lz.trazo(np.array([[-24, 2], [-6, 22], [28, -20]]), (255, 255, 255), 13, afinar=False, temblor=0.0)
            P.pastilla(lz, 1640, 296, "encaja", px=42, k=ke, fondo=(190, 240, 210), color=TINTA)


def uno_mas_uno(lz, t):
    kq = pop(t, A.quizas_x - 0.1, 0.4) * (1 - e_in(prog(t, E_CIERRE - 0.6, E_CIERRE)))
    if kq < 0.02 or t < A.quizas_x - 0.2:
        return
    ks = e_inout(prog(t, A.pegada - 0.8, A.pegada + 0.6))
    ka = pop(t, A.dos_lunas_x - 0.2, 0.45)
    with lz.capa(2):
        with lz.grupo(1500, 190, kq, 0.0):
            lz.relleno(rect_red(-250, -90, 500, 180, 40), (255, 255, 255), alfa=0.92)
            xa = lerp(-130.0, -40.0, ks)
            xb = lerp(120.0, 36.0, ks)
            lz.relleno(circulo(xa, 0, 58 * ka, 40), (204, 204, 222))
            lz.relleno(elipse(xa - 8, -10, 14 * ka, 10 * ka, 0, 16), (150, 150, 182))
            lz.relleno(circulo(xb, 8, 38 * ka, 40), (152, 142, 166))
            if ks < 0.3:
                P.rotulo(lz, -4, 0, "+", px=64, color=(34, 28, 80), alfa=ka * (1 - ks / 0.3), sombra=0.0)


# ======================================================================== toma 9
def toma_9(lz, t):
    cam = cam9(t)
    z = cam.z
    E = cam.a_pant((0, 0))
    rs = ER * z
    bg = ME.fondo(t, cam)
    fondo_gas(lz, t, cam, NEB9, sol=(z < 1.5 or t > T_IN[0]))
    ver_tierra = cam.visible((0, 0), ER, margen=300) and z < 3.0
    if t < A.pasado + 0.6:
        # anillo y rocas de la toma 8 se apagan; el plano del anillo vuelve a verse de arriba
        kf_ = 1 - e_inout(prog(t, E_CHOQUE, E_CHOQUE + 1.2))
        incl = lerp(1.0, 0.30, kf_)
        tilt = -0.25 * kf_
        if kf_ > 0.01:
            MD.anillo_roto(lz, t, E, z, 0, incl, tilt, k=kf_)
        K.tierra_marea(lz, E[0], E[1], rs, t, [], rot=0.45 * t, ang_luz=LUZ, amp=0.0)
        if kf_ > 0.01:
            MD.anillo_roto(lz, t, E, z, 1, incl, tilt, k=kf_)
        if t < E_CHOQUE + 1.4:
            MD.lluvia_gorda(lz, t, E, rs, z, incl, tilt, kf_)
        choque_lunas(lz, t, cam)
    elif ver_tierra:
        escena_L4(lz, t, cam)
    # luna real (primer plano) y rótulos
    if t >= T_ZIN[0] - 0.2 and not (T_OUT[1] - 0.2 < t < T_IN[0] + 0.1):
        luna1(lz, t, cam)
    elif T_OUT[0] < t < T_OUT[1]:
        luna1(lz, t, cam)
    reloj(lz, t)
    if T_ZIN[1] - 0.6 < t < A.y2011 - 0.3:
        rotulos_caras(lz, t)
        cara_espejo(lz, t)
        corte_luna(lz, t)
    dos_mil_once(lz, t)
    if t > T_IN[1] - 0.6:
        inset_lateral(lz, t)
    hipotesis(lz, t)
    uno_mas_uno(lz, t)
    pos = MD.KURI8
    kuri6(lz, t, pos, 1.0, (1000, 400), boca=campana(t, T_X, T_X + 1.4) + 0.5 * campana(t, A.aplasto, A.panqueque + 0.8),
          feliz=1.0 if t > A.encaja else 0.0)
    return bg


# ======================================================================== toma 10: cierre
C10 = Cam((0, 0), (640, 540), 1.0)
T_PULL = (E_CIERRE, E_CIERRE + 2.4)
T_CAE = (E_CIERRE + 2.4, E_CIERRE + 5.3)
M_C = np.array([1180.0, 300.0])
R_MC = 118.0
KURI_PLAYA_X = -790.0


def luna_c(t):
    """Luna del cielo final: sube y crece despacio tras la caída para que los 13 s de playa no queden quietos
    (x fija: así sigue libre entre la 2.ª y la 3.ª tarjeta)."""
    u = e_inout(prog(t, T_CAE[1], TOTAL))
    return np.array([M_C[0], lerp(M_C[1], 252.0, u)]), lerp(R_MC, 124.0, u)


def t_eq(t):
    """Tiempo «de noche normal» para reutilizar el paisaje de la toma 5 (sin noches claras ni corales que desovan)."""
    return 100.0 + (t - E_CIERRE)


def cam10_pull(t):
    u = e_inout(prog(t, *T_PULL))
    pm = pm9(t)
    return Cam(pm * (1 - u), (lerp(PM[0], 640, u), lerp(PM[1], 540, u)), math.exp(lerp(math.log(ZM), math.log(1.0), u)))


def espacio_luna_sola(lz, t, cam, rs):
    z = cam.z
    E = cam.a_pant((0, 0))
    pm = cam.a_pant(pm9(t))
    r_o = r_m9(t)
    ao = (1 - prog(math.log(z), math.log(2.4), math.log(6.0)))
    if ao > 0.02:
        K.orbita(lz, E[0], E[1], r_o * z, r_o * z, 0, AZUL, 3.0, alfa=0.45 * ao, fase=t * 22)
    a1 = math.atan2(pm[1] - E[1], pm[0] - E[0])
    if rs < 24000:
        K.tierra_marea(lz, E[0], E[1], rs, t, [(a1, 0.5)], rot=0.45 * t, ang_luz=LUZ, amp=0.05)
    r_m = MR * z
    if cam.visible(pm9(t), MR, margen=40) and z < 3.4:
        big = e_inout(prog(z, 2.0, 3.4))
        K.cuerpo_rocoso(lz, pm[0], pm[1], r_m, "luna", seed=1, ang_luz=LUZ, rot=0.07 * t, alfa=1.0 - big)
    if cam.visible(pm9(t), MR, margen=40) and z > 2.0:
        K.luna_dos_caras(lz, pm[0], pm[1], r_m, rot=rot_luna(t), ang_luz=LUZ, alfa=e_inout(prog(z, 2.0, 3.4)), panqueque=pancake_k(t))
    return E, pm


def tarjetas(lz, t):
    """Tres tarjetas de «con dos…»: se estorban, se estrellan, destrozan las costas."""
    # la Luna (M_C = 1180, 300; r 118) queda libre entre la 2.ª y la 3.ª tarjeta
    items = ((A.estorban_f, 560.0, "estorban"), (A.estrellan, 900.0, "estrellan"), (A.destrozan, 1620.0, "costas"))
    kout = 1 - e_in(prog(t, A.mira - 0.5, A.mira - 0.1))
    for j, (t0, x, tipo) in enumerate(items):
        k = pop(t, t0 - 0.15, 0.4) * kout
        if k < 0.02:
            continue
        y = 215.0
        with lz.capa(2):
            with lz.grupo(x, y, k):
                q = rect_red(-150, -120, 300, 240, 34)
                lz.relleno(q, (18, 16, 56), alfa=0.9)
                with lz.recorte(q):
                    if tipo == "estorban":
                        lz.relleno(circulo(-70, 0, 46, 40), (204, 204, 222))
                        lz.relleno(circulo(70, 4, 40, 40), (152, 142, 166))
                        K.flecha(lz, np.array([-16.0, 0.0]), np.array([-2.0 + 10 * math.sin(t * 6), 0.0]), ORO, ancho=8)
                        K.flecha(lz, np.array([16.0, 4.0]), np.array([2.0 - 10 * math.sin(t * 6), 4.0]), ORO, ancho=8)
                    elif tipo == "estrellan":
                        lz.halo(0, 0, 170, (255, 214, 140), alfa=0.8, r0=0.1, capa=2)
                        K.destello(lz, 0, 0, 80, t + j, alfa=1.0)
                        for i in range(14):
                            a = h01(i, 1, 5) * 6.2832
                            rr = 60 + 50 * ((t * 1.2 + h01(i, 2, 5)) % 1.0)
                            lz.relleno(circulo(rr * math.cos(a), rr * math.sin(a), 6, 8), (255, 190, 120))
                    else:
                        lz.relleno(rect_red(-150, 40, 300, 100, 0), (60, 130, 220))
                        pts = np.array([[x_, 40 - 70 * math.exp(-((x_ + 60 - 40 * math.sin(t * 3)) / 55.0) ** 2)] for x_ in range(-150, 151, 10)])
                        lz.relleno(np.vstack([pts, [[150, 140], [-150, 140]]]), (96, 170, 240))
                        P.casa(lz, 90, 40, 0.55, calor=0.0)
                lz.trazo(np.vstack([q, q[:1]]), (255, 255, 255), 4.0, afinar=False, temblor=0.0)


def toma_10(lz, t):
    te = t_eq(t)
    if t < T_CAE[0]:
        cam = cam10_pull(t)
        rs = ER * cam.z
        bg = ME.fondo(t, cam)
        fondo_gas(lz, t, cam, NEB9, k=1.0)
        E, pm = espacio_luna_sola(lz, t, cam, rs)
        kuri6(lz, t, MD.KURI8, 1.0, pm, boca=0.0, feliz=1.0)
        return bg
    u = prog(t, *T_CAE)
    c0 = mezclar_cam(C10, C10, 0.0)
    cam, rs = MM.cam_inm(c0, u, (MM.HX, MT.H_ORIZ))
    s = MT.mezcla_cielo(rs)
    bg = ME.fondo(t, cam) * (1 - s) + MT.cielo(te) * s
    fondo_gas(lz, t, cam, NEB9, k=1 - s)
    if s < 0.999:
        E, pm = espacio_luna_sola(lz, t, cam, rs)
    S = Sup(cam.pant[0], cam.pant[1], min(1.0, rs / 9000), (1 / rs) * clamp01((1 - u) / 0.04))
    al = prog(rs, 360, 900)
    luz_m = 0.55
    if al > 0.003:
        MT.paisaje(lz, te, S, alfa=al, corte=1.0)
        a_cielo = prog(rs, 4000, 20000)
        if a_cielo > 0.01:
            mc, r_mc = luna_c(t)
            lz.halo(mc[0], mc[1], r_mc * 3.2, (196, 210, 255), alfa=0.2 * a_cielo, r0=0.2)
            MT.luna_cielo(lz, te, mc, r_mc, "luna", 1, 0.92, math.pi, a_cielo, luz_m)
            MT.luz_mar(lz, S, te, mc[0] - MT.HX, 0.55 * a_cielo)
        if S.k > 0.25:
            MT.corales_y_vida(lz, te, S, alfa=al)
        if S.k > 0.05:
            MT.arboles(lz, te, S, alfa=al)
            for X, tipo, sc in ((-585, "conejo", 1.7), (-455, "zorro", 1.35)):
                x, y = S.pt(X, float(MT.h_tierra(X)) + 3)
                if tipo == "conejo":
                    P.conejo(lz, x, y, sc * S.k, t)
                else:
                    P.zorro(lz, x, y, sc * S.k, t)
    # estrellas: más vivas al hablar de ellas, y una fugaz
    ke = ventana(t, A.estrellas_f - 0.4, A.estrellas_f + 1.4, 0.4, 0.8)
    if ke > 0.02 and u >= 1.0:
        uu = prog(t, A.estrellas_f + 0.2, A.estrellas_f + 1.0)
        if 0 < uu < 1:
            p0 = np.array([1600.0, 120.0])
            p1 = p0 + np.array([-420.0, 170.0]) * uu
            lz.trazo(np.array([p1 + np.array([260.0, -105.0]) * (1 - uu) * 0.0, p1 + np.array([120.0, -48.0])]), (255, 255, 255), 5, afinar=True,
                     temblor=0.0, capa=2)
            lz.halo(p1[0], p1[1], 30, (255, 255, 255), alfa=0.9, r0=0.2, capa=2)
    # Kuri llega a la playa y se queda mirando la Luna
    xk, yk = S.pt(KURI_PLAYA_X, float(MT.h_tierra(KURI_PLAYA_X)) + 3)
    uk = e_inout(prog(t, T_CAE[0] + 0.6, T_CAE[1] - 0.2))
    pk = (lerp(MD.KURI8[0], xk, uk), lerp(MD.KURI8[1], yk, uk) - 90 * math.sin(math.pi * uk))
    sk = lerp(1.0, 1.55, uk)
    mirar_a = luna_c(t)[0] if u >= 1.0 else (1180, 300)
    kuri6(lz, t, pk, sk, mirar_a, boca=0.0, feliz=1.0 if t > A.hoy_f else 0.0)
    tarjetas(lz, t)
    return bg


# ======================================================================== despachador
def toma_9_10(lz, t):
    if t < E_CIERRE:
        return toma_9(lz, t), 1.0
    bg = toma_10(lz, t)
    fade = 1.0 - e_inout(prog(t, TOTAL - 1.3, TOTAL - 0.1))
    return bg, fade
