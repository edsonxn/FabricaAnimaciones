# -*- coding: utf-8 -*-
"""Utilería animada (por cuadro) de «¿Quién envenenó al rey?» (noir feudal a color: cada pieza con su rampa de material).

    candelabro(h, t, x, y, r)            corona de hierro con velas colgada de cadenas (luz cálida)
    caliz(h, x, y, s, ang, vino)         el gran cáliz de boda, de oro con gemas (origen = pie)
    empanada(h, t, x, y, s, corte)       la empanada gigante con celosía de masa;  palomas(h, t, t0, x, y, n)  salen volando
    espada(h, x, y, ang, s)              espada larga del rey (origen = pomo)
    jarra(h, x, y, s, ang)               jarra de vino (origen = base)
    musico(h, t, x, y, s, tipo)          laúd o tambor, de perfil, tocando
    cristales(h, t, x, y, s, n)          los cristales morados del veneno (emiten el acento púrpura)
    frasco(h, t, x, y, s)                frasco de vidrio con tapón de cera y cristales dentro
    puno(h, x, y, s, cierra)             mano de perfil que se cierra en un puño
    collar_grande(h, t, x, y, s, falta)  el collar de Sansa en primer plano (cadena, engastes, piedras)
    cofre(h, t, x, y, s, abre)           cofre de joyas que se abre
    ballesta(h, x, y, s, ang) · saeta(h, x, y, ang, s)
    barca(h, t, x, y, s)                 bote de remos con dos figuras (Dontos rema, Sansa encapuchada)
    rosa(h, t, x, y, s)                  rosa roja abierta
    monedas(h, t, x, y, n, s)            pila de monedas de oro
    rollo(h, t, x0, y, largo, s)         rollo de pergamino desenrollado (devuelve T local->mundo)
    gotas_vino(h, t, t0, x, y)           salpicadura de vino al caer la copa
"""
import math

import numpy as np

import noir as N
import noir_feudal as NF
from comun import T_obj, rect, rot
from motor import clamp01, smooth
from toon import blob, elipse_, suave, tubo

TINTA = (14, 12, 16)


# ------------------------------------------------------------------ luces
def candelabro(h, t, x, y, r=160.0, s=1.0, sem=0, cadena=900.0, luz=1.0, alcance=900.0, k=1.0):
    """Corona de hierro (vista algo desde abajo) con velas encendidas, colgada de tres cadenas; se mece un poco."""
    sw = 0.025 * math.sin(t * 0.7 + sem)
    cx = x + math.sin(sw) * cadena * 0.05
    with h.con_rampa("hierro"):
        for a in (-0.6, 0.0, 0.6):
            x0 = cx + r * math.sin(a) * s
            h.trazo([(x + 0, y - cadena * s), (x0, y)], 2.6 * s, sem + 1, color=(26, 26, 30), alfa=0.9)
        P = elipse_(cx, y, r * s, r * 0.28 * s, n=40)
        Q = elipse_(cx, y, (r - 14) * s, (r * 0.28 - 6) * s, n=40)
        h.pieza(np.vstack([P, Q[::-1]]), 60, sem + 2, w=3 * s, d=4 * s, trama=0, rim=0.9)
        h.pieza(elipse_(cx, y + 6 * s, r * s, r * 0.28 * s + 6 * s, n=40), 40, sem + 3, w=3 * s, d=3 * s, trama=0, rim=0.6, alfa=0.0)
    tot = 0.0
    n = 9
    for i in range(n):
        a = 2 * math.pi * i / n + 0.3
        vx = cx + r * s * math.cos(a)
        vy = y + r * 0.28 * s * math.sin(a)
        with h.con_rampa("cera"):
            h.pieza(rect(vx - 7 * s, vy - 34 * s, 14 * s, 34 * s), 200, sem + 10 + i, w=2 * s, d=3 * s, trama=0, rim=0.6)
        tot += NF.llama(h, t, vx, vy - 36 * s, s=0.42 * s, sem=sem + 20 + i, k=k)
    h.luz_radial(cx, y, alcance * s, h.pal["vela"], k=luz * tot / n)
    return cx, y


# ------------------------------------------------------------------ el cáliz y el vino
def caliz(h, x, y, s=1.0, ang=0.0, vino=0.7, sem=0, rampa="oro", luz=(0.4, -1.0)):
    """El gran cáliz de boda (alto ~260 px con s=1): pie ancho, nudo con gemas, copa honda con el vino. ang gira sobre el pie."""
    T = T_obj(x, y, ang, s)
    with h.con_rampa(rampa):
        h.pieza(T(suave([(-80, 0), (80, 0), (60, -18), (20, -30), (-20, -30), (-60, -18)], 3)), 150, sem, w=4 * s, luz=luz, d=8 * s,
                trama=0.3, rim=1.0)
        h.pieza(T(rect(-12, -110, 24, 82)), 160, sem + 1, w=3.5 * s, luz=luz, d=6 * s, trama=0.2, rim=1.0)
        h.pieza(T(elipse_(0, -80, 30, 22, n=20)), 170, sem + 2, w=3.5 * s, luz=luz, d=6 * s, trama=0.2, rim=1.0)
        copa = [(-96, -260), (96, -260), (90, -200), (60, -140), (20, -112), (-20, -112), (-60, -140), (-90, -200)]
        h.pieza(T(suave(copa, 4)), 158, sem + 3, w=4.5 * s, luz=luz, d=12 * s, trama=0.3, rim=1.0)
        h.pieza(T(rect(-96, -262, 192, 14)), 190, sem + 4, w=3 * s, luz=luz, d=3 * s, trama=0, rim=1.0)
        for k, gx in enumerate((-50, 0, 50)):
            h.pieza(T(elipse_(gx, -200, 12, 14, n=12)), 110, sem + 5 + k, w=2.5 * s, d=2, trama=0, rim=0.9,
                    rampa="estandarte" if k != 1 else "purpura")
            h.disco(*T([[gx + 4, -205]])[0], 2.6 * s, (255, 240, 220))
        for k in range(5):                                                         # cincelado
            h.trazo(T([(-80 + k * 40, -248), (-70 + k * 36, -170)]), 1.6 * s, sem + 9 + k, color=(60, 40, 10), alfa=0.6)
    if vino > 0:
        with h.con_rampa("vino"):
            h.pieza(T(elipse_(0, -260, 92, 14, n=24)), 80, sem + 15, w=2 * s, d=2, sombra=0, trama=0, rim=0.6)
    return T


def gotas_vino(h, t, t0, x, y, n=26, sem=0, s=1.0):
    """Salpicadura: gotas en parábola desde (x, y) y un charco que se extiende."""
    if t < t0:
        return
    u = t - t0
    rng = np.random.default_rng(sem)
    with h.con_rampa("vino"):
        r = 260 * s * (1 - math.exp(-u * 2.2))
        h.pieza(suave([(x - r, y), (x - r * 0.5, y - r * 0.12), (x + r * 0.3, y - r * 0.14), (x + r, y + r * 0.02),
                       (x + r * 0.4, y + r * 0.16), (x - r * 0.6, y + r * 0.12)], 4), 70, sem, w=2.5 * s, d=0, sombra=0, trama=0,
                rim=0.7, alfa=0.9)
        for i in range(n):
            vx, vy = rng.uniform(-600, 600) * s, -rng.uniform(300, 900) * s
            px, py = x + vx * u, y + vy * u + 1800 * s * u * u
            if py > y + 40 * s or u > 1.4:
                continue
            rr = rng.uniform(4, 11) * s
            h.pieza(elipse_(px, py, rr, rr * 1.3, n=10), 80, sem + 1 + i, w=1.5 * s, d=1, sombra=0, trama=0, rim=0.9)


def jarra(h, x, y, s=1.0, ang=0.0, sem=0):
    T = T_obj(x, y, ang, s)
    with h.con_rampa("laton"):
        P = suave([(-50, 0), (50, 0), (62, -60), (54, -140), (30, -170), (36, -200), (-30, -200), (-26, -170), (-54, -140), (-62, -60)], 4)
        h.pieza(T(P), 130, sem, w=4 * s, d=10 * s, trama=0.4, rim=0.9)
        h.pieza(T(tubo(np.array([[54.0, -150], [92, -120], [86, -50], [58, -40]]), 12, 12)), 110, sem + 1, w=3 * s, d=4 * s, trama=0,
                rim=0.8)
        h.pieza(T([(-30, -200), (-60, -214), (-26, -186)]), 130, sem + 2, w=3 * s, d=2, trama=0, rim=0.8)
        h.trazo(T([(-56, -80), (56, -80)]), 3 * s, sem + 3, color=(50, 30, 10), alfa=0.7)
    return T(np.array([[-60.0, -212.0]]))[0]


# ------------------------------------------------------------------ la empanada y las palomas
def empanada(h, t, x, y, s=1.0, corte=0.0, sem=0):
    """Empanada gigante (ancho ~520 px) sobre bandeja de plata, con celosía de masa; corte 0..1 abre una raja central."""
    T = T_obj(x, y, 0.0, s)
    with h.con_rampa("hierro"):
        h.pieza(T(elipse_(0, 0, 330, 54, n=48)), 170, sem, w=4 * s, d=8 * s, trama=0.2, rim=1.0)
    with h.con_rampa("cuero"):
        cuerpo = [(-270, -10), (-276, -120), (-230, -190), (-110, -230), (0, -236), (110, -230), (230, -190), (276, -120), (270, -10)]
        h.pieza(T(suave(cuerpo, 4)), 150, sem + 1, w=4.5 * s, d=16 * s, trama=0.4, rim=0.9)
        for k in range(-5, 6):                                                     # celosía
            h.trazo(T([(k * 46 - 60, -220 + abs(k) * 4), (k * 46 + 60, -40)]), 9 * s, sem + 2 + k, color=h.c(185, "cuero"), alfa=0.9)
            h.trazo(T([(k * 46 + 60, -220 + abs(k) * 4), (k * 46 - 60, -40)]), 9 * s, sem + 20 + k, color=h.c(175, "cuero"), alfa=0.9)
        for k in range(14):                                                        # borde trenzado
            a = math.pi * k / 13
            h.pieza(T(elipse_(-270 * math.cos(a), -16 - 8 * math.sin(a), 22, 12, n=10)), 170, sem + 40 + k, w=2 * s, d=3 * s,
                    trama=0, rim=0.8)
    if corte > 0:
        ab = 60 * corte
        with h.con_rampa("personaje"):
            h.pieza(T(suave([(-ab * 0.35, -232), (ab * 0.35, -232), (ab * 0.15, -70), (-ab * 0.15, -70)], 3)), 60, sem + 60, w=2.5 * s,
                    d=0, sombra=0, rim=0)
            h.pieza(T(suave([(-ab * 0.25, -226), (ab * 0.25, -226), (ab * 0.1, -90), (-ab * 0.1, -90)], 3)), 120, sem + 61, w=0,
                    d=0, sombra=0, rim=0, rampa="vino", linea=False)


def paloma(h, t, x, y, s=1.0, d=1, fase=0.0, sem=0):
    """Paloma blanca de perfil batiendo las alas."""
    a = math.sin(t * 22.0 + fase)
    T = T_obj(x, y, 0.0, s, sx=d)
    with h.con_rampa("neutro"):
        h.pieza(T(suave([(-40, 0), (-10, -14), (24, -12), (40, -4), (24, 8), (-10, 10)], 3)), 220, sem, w=2.5 * s, d=4 * s, trama=0,
                rim=0.8)
        h.pieza(T(elipse_(38, -10, 10, 9, n=10)), 225, sem + 1, w=2 * s, d=2, trama=0, rim=0.8)
        h.pieza(T([(46, -10), (56, -7), (46, -5)]), 120, sem + 2, w=1.5 * s, d=1, trama=0, rim=0, rampa="cuero")
        h.pieza(T([(-40, 0), (-66, -10), (-64, 8)]), 205, sem + 3, w=2 * s, d=2, trama=0, rim=0.6)
        h.pieza(T(suave([(-6, -8), (20, -8), (10 - 30 * a, -50 * a - 8), (-30 - 20 * a, -60 * a - 4)], 3)), 235, sem + 4, w=2 * s, d=3 * s,
                trama=0, rim=0.9)
    h.disco(*T([[40, -12]])[0], 1.8 * s, TINTA)


def palomas(h, t, t0, x, y, n=9, s=1.0, sem=0):
    """Bandada que sale de (x, y) en abanico y sube aleteando; plumas que caen."""
    if t < t0:
        return
    u = t - t0
    rng = np.random.default_rng(sem)
    for i in range(n):
        retardo = rng.uniform(0, 0.35)
        v = max(0.0, u - retardo)
        if v <= 0:
            continue
        ang = rng.uniform(-2.5, -0.6)
        vel = rng.uniform(230, 380) * s
        px = x + math.cos(ang) * vel * v + rng.uniform(-30, 30)
        py = y + math.sin(ang) * vel * v - 40 * v * v * s
        ss = 1.7 * s * rng.uniform(0.75, 1.1) * (1 + 0.25 * v)
        paloma(h, t, px, py, ss, d=1 if math.cos(ang) > 0 else -1, fase=rng.uniform(0, 6), sem=sem + i * 7)
    for i in range(14):
        v = u - rng.uniform(0.1, 0.6)
        if v <= 0:
            continue
        px = x + rng.uniform(-200, 200) * s + 30 * math.sin(v * 3 + i)
        py = y - rng.uniform(100, 400) * s + 90 * v * s
        with h.con_rampa("neutro"):
            h.pieza(rot(elipse_(px, py, 9 * s, 3 * s, n=8), math.sin(v * 4 + i), (px, py)), 230, sem + 100 + i, w=1.2 * s, d=1,
                    trama=0, rim=0.6)


def espada(h, x, y, ang=0.0, s=1.0, sem=0, brillo=0.0):
    """Espada larga (~720 px): pomo en el origen, empuñadura de cuero, gavilanes dorados y hoja con acanaladura."""
    T = T_obj(x, y, ang, s)
    with h.con_rampa("oro"):
        h.pieza(T(elipse_(0, 0, 18, 18, n=14)), 160, sem, w=3 * s, d=4 * s, trama=0, rim=1.0)
        h.pieza(T(rect(130, -60, 22, 120)), 165, sem + 1, w=3 * s, d=4 * s, trama=0, rim=1.0)
    with h.con_rampa("cuero"):
        h.pieza(T(rect(14, -14, 118, 28)), 70, sem + 2, w=3 * s, d=4 * s, trama=0.3, rim=0.6)
        for k in range(6):
            h.trazo(T([(24 + k * 18, -14), (34 + k * 18, 14)]), 2 * s, sem + 3 + k, color=TINTA, alfa=0.7)
    with h.con_rampa("hierro"):
        h.pieza(T([(152, -18), (690, -10), (730, 0), (690, 10), (152, 18)]), 190, sem + 10, w=3 * s, d=4 * s, trama=0, rim=1.0)
        h.trazo(T([(160, 0), (640, 0)]), 3 * s, sem + 11, color=(60, 66, 74), alfa=0.8)
    if brillo > 0:
        q = T([[400 + 300 * brillo, -6]])[0]
        h.emitir(elipse_(q[0], q[1], 26 * s, 5 * s, n=12), 0.9 * math.sin(math.pi * brillo), col=h.pal["relampago"], blur=2)


# ------------------------------------------------------------------ músicos
def musico(h, t, x, y, s=1.0, tipo="laud", sem=0, d=1):
    """Silueta de músico sentado tocando (laúd o tambor), con gorro y calzas; la mano rasguea o golpea a tempo."""
    T = T_obj(x, y, 0.0, s, sx=d)
    b = math.sin(t * 2 * math.pi * 1.4 + sem)
    with h.con_rampa("lana"):
        h.pieza(T(suave([(-40, -60), (-36, -200), (-10, -230), (30, -224), (44, -190), (40, -60)], 4)), 80, sem, w=4 * s, d=10 * s,
                trama=0.5, rim=0.8)
        h.pieza(T(tubo(np.array([[-20.0, -60], [40, -60], [60, 0]]), 26, 22)), 60, sem + 1, w=4 * s, d=6 * s, trama=0.4, rim=0.7)
    with h.con_rampa("piel"):
        h.pieza(T(elipse_(6, -262, 30, 34, n=20)), 120, sem + 2, w=3.5 * s, d=8 * s, trama=0.3, rim=0.8)
    with h.con_rampa("estandarte"):
        h.pieza(T(suave([(-30, -276), (-10, -310), (30, -306), (44, -280), (36, -262), (-26, -262)], 3)), 110, sem + 3, w=3 * s, d=4 * s,
                trama=0.2, rim=0.7)
    h.disco(*T([[26, -266]])[0], 2.4 * s, TINTA)
    if tipo == "laud":
        with h.con_rampa("madera"):
            h.pieza(T(elipse_(40, -120, 50, 38, rot=-0.5, n=24)), 140, sem + 4, w=3 * s, d=6 * s, trama=0.3, rim=0.9)
            h.pieza(T(rot(rect(80, -128, 120, 16), -0.5, (40, -120))), 120, sem + 5, w=2.5 * s, d=3 * s, trama=0, rim=0.8)
        h.disco(*T([[40, -120]])[0], 9 * s, TINTA)
        mano = (40 + 8 * b, -110 + 6 * b)
    else:
        with h.con_rampa("cuero"):
            h.pieza(T(rect(10, -140, 90, 80)), 140, sem + 4, w=3 * s, d=6 * s, trama=0.3, rim=0.9)
            h.pieza(T(elipse_(55, -140, 45, 10, n=20)), 200, sem + 5, w=2.5 * s, d=2, trama=0, rim=0.8)
        mano = (40 + 20 * b, -150 - 40 * max(0.0, b))
    with h.con_rampa("lana"):
        h.pieza(T(tubo(np.array([[20.0, -200], [(20 + mano[0]) / 2 + 10, -150], mano]), 18, 14)), 76, sem + 6, w=3 * s, d=4 * s,
                trama=0, rim=0.7)
    with h.con_rampa("piel"):
        h.pieza(T(elipse_(mano[0], mano[1], 11, 9, n=10)), 120, sem + 7, w=2 * s, d=2, trama=0, rim=0.6)


# ------------------------------------------------------------------ el veneno
def cristales(h, t, x, y, s=1.0, n=7, sem=0, brillo=1.0):
    """Racimo de cristales morados (el Estrangulador): prismas facetados que emiten un púrpura tenue."""
    rng = np.random.default_rng(sem)
    for i in range(n):
        a = rng.uniform(-0.9, 0.9)
        L = rng.uniform(40, 100) * s
        w = rng.uniform(12, 24) * s
        c = np.array([x + rng.uniform(-50, 50) * s, y])
        P = np.array([(-w, 0), (-w, -L), (0, -L - w * 1.4), (w, -L), (w, 0)])
        Q = rot(P + c, a, c)
        h.pieza(Q, 120 + rng.uniform(-20, 30), sem + i, w=2.5 * s, d=4 * s, trama=0, rim=1.0, rampa="purpura")
        h.trazo(rot(np.array([(0, 0), (0, -L - w * 1.2)]) + c, a, c), 1.6 * s, sem + 20 + i, color=(230, 200, 240), alfa=0.6)
        if brillo > 0:
            pul = 0.6 + 0.4 * math.sin(t * 2.0 + i)
            h.emitir(Q, 0.35 * brillo * pul, col=(0.7, 0.25, 0.9), blur=2)
    h.luz_radial(x, y - 40 * s, 300 * s, (0.75, 0.35, 0.95), k=0.6 * brillo)


def frasco(h, t, x, y, s=1.0, sem=0, brillo=1.0):
    """Frasco de vidrio con tapón de cera roja y los cristales dentro."""
    T = T_obj(x, y, 0.0, s)
    cristales(h, t, x, y - 20 * s, 0.55 * s, n=6, sem=sem + 50, brillo=brillo)
    P = suave([(-70, 0), (70, 0), (80, -70), (70, -150), (30, -180), (30, -230), (-30, -230), (-30, -180), (-70, -150), (-80, -70)], 4)
    h.pieza(T(P), 160, sem, w=3.5 * s, d=6 * s, sombra=0.2, trama=0, rim=1.0, alfa=0.35, rampa="vidrio_verde")
    h.trazo(T([(-52, -150), (-60, -60), (-50, -20)]), 4 * s, sem + 1, color=(230, 240, 235), alfa=0.6)
    h.pieza(T(rect(-36, -262, 72, 36)), 120, sem + 2, w=3 * s, d=4 * s, trama=0, rim=0.8, rampa="lacre")
    h.pieza(T(suave([(-40, -232), (40, -232), (36, -216), (-10, -206), (-38, -214)], 3)), 110, sem + 3, w=2.5 * s, d=2, trama=0,
            rim=0.7, rampa="lacre")


def puno(h, x, y, s=1.0, cierra=0.0, sem=0, d=1, rampa_manga="cuero"):
    """Mano de perfil que se cierra en un puño (cierra 0..1): cuatro dedos que se enroscan y el pulgar encima."""
    T = T_obj(x, y, 0.0, s, sx=d)
    with h.con_rampa(rampa_manga):
        h.pieza(T(rect(-420, -70, 300, 140)), 70, sem, w=4 * s, d=10 * s, trama=0.5, rim=0.8)
    with h.con_rampa("piel"):
        h.pieza(T(suave([(-140, -66), (40, -70), (70, -30), (60, 50), (-140, 64)], 4)), 120, sem + 1, w=4 * s, d=12 * s, trama=0.4,
                rim=0.9)
        c = clamp01(cierra)
        for k in range(4):
            y0 = -50 + k * 30
            L1, L2 = 70 - k * 4, 56 - k * 4
            a1 = c * 1.6
            a2 = a1 + c * 1.5
            p0 = np.array([50.0, y0])
            p1 = p0 + (L1 * math.cos(a1), L1 * math.sin(a1) * 0.3)
            p2 = p1 + (L2 * math.cos(a2), L2 * math.sin(a2) * 0.45)
            h.pieza(T(tubo(np.array([p0, p1, p2]), 26, 22)), 125 - k * 3, sem + 2 + k, w=3 * s, d=6 * s, trama=0.3, rim=0.8)
        pul = np.array([[0.0, -60], [50 + 30 * c, -84 + 50 * c], [80 + 20 * c, -70 + 70 * c]])
        h.pieza(T(tubo(pul, 26, 22)), 128, sem + 9, w=3 * s, d=6 * s, trama=0.3, rim=0.9)


# ------------------------------------------------------------------ el collar
def collar_grande(h, t, x, y, s=1.0, falta=3, n=7, sem=0, brillo=0.0, ang=0.0):
    """El collar de Sansa en primer plano (ancho ~900 px): cadena de eslabones, engastes de oro y piedras oscuras; el engaste
    vacío (falta) tiene las garras abiertas. Devuelve las posiciones de las piedras."""
    T = T_obj(x, y, ang, s)
    pts = [(-450 + 900 * u, 300 * math.sin(math.pi * u)) for u in np.linspace(0, 1, 60)]
    for i in range(len(pts) - 1):                                                  # eslabones alternos
        a, b = np.array(pts[i]), np.array(pts[i + 1])
        c = (a + b) / 2
        ang_k = math.atan2(*(b - a)[::-1])
        h.pieza(T(rot(elipse_(c[0], c[1], 10, 5 if i % 2 else 2.5, n=12), ang_k, c)), 165, sem + i % 7, w=2 * s, d=2, trama=0, rim=1.0,
                rampa="oro")
    out = []
    for i, u in enumerate(np.linspace(0.12, 0.88, n)):
        cx, cy = -450 + 900 * u, 300 * math.sin(math.pi * u) + 40
        h.pieza(T(elipse_(cx, cy, 44, 52, n=24)), 160, sem + 20 + i, w=3 * s, d=6 * s, trama=0.2, rim=1.0, rampa="oro")
        for ga in np.linspace(0, 2 * math.pi, 6, endpoint=False):                  # garras
            q = (cx + 44 * math.cos(ga), cy + 52 * math.sin(ga))
            dq = 1.0 if i != falta else 1.3
            h.pieza(T(elipse_(q[0] * 1 + (q[0] - cx) * (dq - 1), q[1] + (q[1] - cy) * (dq - 1), 8, 8, n=8)), 180, sem + 40 + i,
                    w=1.5 * s, d=2, trama=0, rim=1.0, rampa="oro")
        if i == falta:
            h.pieza(T(elipse_(cx, cy, 30, 36, n=20)), 14, sem + 60 + i, w=2.5 * s, d=0, sombra=0, rim=0, rampa="oro")
            out.append(T([[cx, cy]])[0])
            continue
        h.pieza(T(elipse_(cx, cy, 32, 38, n=20)), 70, sem + 80 + i, w=2.5 * s, d=4 * s, trama=0, rim=1.0, rampa="purpura")
        h.pieza(T([(cx - 16, cy - 20), (cx + 4, cy - 30), (cx + 14, cy - 10), (cx - 6, cy)]), 140, sem + 90 + i, w=1 * s, d=1, sombra=0,
                trama=0, rim=0, alfa=0.6, rampa="purpura")
        h.disco(*T([[cx + 10, cy - 16]])[0], 4 * s, (240, 220, 245))
        if brillo > 0:
            h.emitir(T(elipse_(cx, cy, 30, 36, n=16)), 0.25 * brillo, col=(0.7, 0.25, 0.9), blur=2)
        out.append(T([[cx, cy]])[0])
    return out


def cofre(h, t, x, y, s=1.0, abre=0.0, sem=0):
    """Cofre de joyas de frente: caja con herrajes y tapa abombada que se abre hacia atrás; dentro, terciopelo y destellos."""
    T = T_obj(x, y, 0.0, s)
    with h.con_rampa("madera"):
        h.pieza(T(rect(-260, -200, 520, 200)), 90, sem, w=4 * s, d=12 * s, trama=0.5, rim=0.8)
    if abre > 0.05:
        with h.con_rampa("purpura"):
            h.pieza(T(rect(-240, -210, 480, 30)), 60, sem + 1, w=3 * s, d=2, trama=0, rim=0)
        rng = np.random.default_rng(sem)
        for k in range(9):
            gx = rng.uniform(-200, 200)
            h.pieza(T(elipse_(gx, -206, 16, 10, n=12)), 140, sem + 10 + k, w=2 * s, d=2, trama=0, rim=1.0,
                    rampa=["oro", "purpura", "estandarte"][k % 3])
            q = T([[gx + 5, -210]])[0]
            h.emitir(elipse_(q[0], q[1], 5 * s, 5 * s, n=8), 0.5 * abre * (0.5 + 0.5 * math.sin(t * 5 + k)), col=h.pal["vela"])
    alto = 150 * math.cos(abre * 1.9)
    with h.con_rampa("madera"):
        tapa = suave([(-268, -200), (268, -200), (260, -200 - alto * 0.7), (0, -200 - alto), (-260, -200 - alto * 0.7)], 4)
        h.pieza(T(tapa), 100 if abre < 0.5 else 60, sem + 2, w=4 * s, d=10 * s, trama=0.5, rim=0.8)
    with h.con_rampa("oro"):
        for xx in (-200, 200):
            h.pieza(T(rect(xx - 14, -200, 28, 200)), 150, sem + 3, w=2.5 * s, d=3 * s, trama=0, rim=0.9)
        h.pieza(T(rect(-30, -120, 60, 70)), 160, sem + 4, w=2.5 * s, d=3 * s, trama=0, rim=1.0)
        h.disco(*T([[0, -86]])[0], 7 * s, TINTA)


# ------------------------------------------------------------------ la huida
def ballesta(h, x, y, s=1.0, ang=0.0, sem=0, tensa=1.0):
    T = T_obj(x, y, ang, s)
    with h.con_rampa("madera"):
        h.pieza(T(rect(-200, -14, 300, 28)), 110, sem, w=3 * s, d=4 * s, trama=0.3, rim=0.8)
        h.pieza(T([(-200, -14), (-260, 20), (-250, 40), (-190, 14)]), 100, sem + 1, w=3 * s, d=4 * s, trama=0.3, rim=0.8)
    with h.con_rampa("hierro"):
        arco = suave([(90, -150), (120, -60), (124, 0), (120, 60), (90, 150), (100, 150), (134, 60), (138, 0), (134, -60), (100, -150)], 3)
        h.pieza(T(arco), 150, sem + 2, w=3 * s, d=3 * s, trama=0, rim=1.0)
    cuerda_x = 90 - 140 * tensa
    h.trazo(T([(92, -146), (cuerda_x, 0), (92, 146)]), 2.2 * s, sem + 3, color=(200, 190, 170), alfa=0.9)


def saeta(h, x, y, ang=0.0, s=1.0, sem=0):
    T = T_obj(x, y, ang, s)
    with h.con_rampa("madera"):
        h.pieza(T(rect(-160, -5, 170, 10)), 130, sem, w=2 * s, d=2, trama=0, rim=0.9)
    with h.con_rampa("hierro"):
        h.pieza(T([(10, -10), (44, 0), (10, 10)]), 170, sem + 1, w=2 * s, d=2, trama=0, rim=1.0)
    with h.con_rampa("lana"):
        for sg in (-1, 1):
            h.pieza(T([(-160, 0), (-120, 0), (-150, sg * 22), (-176, sg * 20)]), 200, sem + 2, w=1.5 * s, d=1, trama=0, rim=0.6)


def barca(h, t, x, y, s=1.0, sem=0, remo=None):
    """Bote de remos de perfil (proa a la derecha) con Dontos remando y Sansa encapuchada a popa; deja estela."""
    T = T_obj(x, y + 4 * math.sin(t * 1.3), 0.02 * math.sin(t * 1.1), s)
    r = (t * 1.1) if remo is None else remo
    ph = math.sin(r * 2 * math.pi)
    with h.con_rampa("lana"):                                                      # Sansa, encapuchada, a popa
        h.pieza(T(suave([(-170, -10), (-176, -90), (-150, -130), (-120, -126), (-104, -90), (-100, -10)], 4)), 150, sem + 1, w=3 * s,
                d=6 * s, trama=0.4, rim=0.9)
    with h.con_rampa("piel"):
        h.pieza(T(elipse_(-126, -112, 13, 16, n=12)), 130, sem + 2, w=2 * s, d=2, trama=0, rim=0.6)
    with h.con_rampa("estandarte"):                                                # Dontos, de remiendos, rema
        bx = -10 - 20 * ph
        h.pieza(T(suave([(bx - 34, -10), (bx - 30, -110), (bx, -130), (bx + 26, -112), (bx + 30, -10)], 4)), 120, sem + 3, w=3 * s,
                d=6 * s, trama=0.4, rim=0.9)
    with h.con_rampa("piel"):
        h.pieza(T(elipse_(bx + 4, -152, 18, 20, n=14)), 130, sem + 4, w=2.5 * s, d=3 * s, trama=0, rim=0.7)
    with h.con_rampa("madera"):
        h.trazo(T([(bx + 20, -80), (60 + 50 * ph, 40)]), 7 * s, sem + 5, color=h.c(120, "madera"))
        casco = suave([(-220, -20), (200, -26), (250, -50), (210, 30), (-190, 30)], 4)
        h.pieza(T(casco), 100, sem, w=4 * s, d=8 * s, trama=0.5, rim=0.9)
        h.trazo(T([(-210, -6), (220, -14)]), 2.4 * s, sem + 6, color=TINTA, alfa=0.7)
    for k in range(5):                                                             # estela
        q = T([[-240 - k * 60, 34]])[0]
        h.trazo([(q[0] - 30, q[1] + k * 3), (q[0] + 30, q[1] + k * 3)], 2.0 * s, sem + 7 + k, color=(200, 210, 220), alfa=0.4 - 0.06 * k)


# ------------------------------------------------------------------ rosas, monedas, pergamino
def rosa(h, t, x, y, s=1.0, sem=0, abre=1.0):
    rng = np.random.default_rng(sem)
    with h.con_rampa("estandarte"):
        for k in range(6):
            a = k * 2.3 + 0.2 * math.sin(t * 0.6 + sem)
            r = (30 - k * 4) * s * (0.5 + 0.5 * abre)
            P = elipse_(x + 6 * s * math.cos(a), y + 4 * s * math.sin(a), r, r * 0.8, rot=a, n=14)
            h.pieza(P, 100 + k * 12, sem + k, w=2 * s, d=3 * s, trama=0.2, rim=0.8)
        h.trazo(suave([(x - 10 * s, y - 2 * s), (x, y - 10 * s), (x + 8 * s, y)], 4, cerrado=False), 2 * s, sem + 9, color=TINTA, alfa=0.7)


def monedas(h, t, x, y, n=8, s=1.0, sem=0):
    with h.con_rampa("oro"):
        for j in range(n):
            h.pieza(elipse_(x + 2 * math.sin(j * 1.7) * s, y - j * 9 * s, 34 * s, 11 * s, n=20), 150 + 12 * (j % 2), sem + j, w=2 * s,
                    d=2, trama=0, rim=0.9)


def rollo(h, t, x0, y, largo, s=1.0, sem=0, ancho=440.0):
    """Pergamino desenrollado en vertical desde y hacia abajo (largo px) con el rollo al final. Devuelve T(local)->mundo
    (x local = -ancho/2..ancho/2 desde el centro, y local = 0..largo)."""
    with h.con_rampa("pergamino"):
        h.pieza(rect(x0 - ancho / 2 * s, y, ancho * s, largo), 205, sem, w=4 * s, d=6 * s, trama=0.1, rim=0.3)
        h.pieza(rect(x0 - (ancho / 2 + 20) * s, y + largo - 26 * s, (ancho + 40) * s, 52 * s), 170, sem + 1, w=4 * s, d=10 * s,
                trama=0.4, rim=0.8)
        h.pieza(rect(x0 - (ancho / 2 + 20) * s, y - 26 * s, (ancho + 40) * s, 40 * s), 165, sem + 2, w=4 * s, d=10 * s, trama=0.4,
                rim=0.8)
    N.soporte(h, x0, y + largo / 2, ancho * s, largo, 0.0, 1.0)
    return lambda P: np.asarray(P, float).reshape(-1, 2) * (s, 1.0) + (x0, y)
