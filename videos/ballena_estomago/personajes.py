# -*- coding: utf-8 -*-
"""Personajes y utilería del Short de la ballena, pintados con el kit acuarela.py (todo en coordenadas locales → tr()).
    buzo(...)        buzo chibi de frente (tanque amarillo, aletas, visor); poses por parámetros, caras por nombre
    kuri(...)        Kuri, la mascota de Kuriox: robot redondo turquesa con pantalla-cara y antena con foco (brilla)
    cachalote(...)   de perfil (cabeza de bloque, mandíbula estrecha que se abre, arrugas, bulto que baja por la garganta)
    calamar, pez, alga, burbuja · iconos: exclama, pregunta, nube_lluvia, destello, corazon, gota, mareo
"""
import math

import cv2
import numpy as np

from acuarela import (TINTA, brillo, brillo_forma, cinta, curva, elipse, forma, hervir, lavado, linea, lerp, mancha_pts,
                      rgb, rotulo, rrect, tr)

PIEL = rgb("f4cfae")
PELO = rgb("4a3226")
TRAJE = rgb("2f4f86")
TRAJE_OSC = rgb("1d2f55")
FRANJA = rgb("3fb8b0")
TANQUE = rgb("f2bf35")
ALETA = rgb("ef7b3c")
VISOR = rgb("2b6f7e")
CRISTAL = rgb("bfe7f3")
KURI = np.array([64, 196, 190], np.float32) / 255
KURI_OSC = KURI * 0.62
PANTALLA = rgb("10232b")
OJO_K = np.array([150, 255, 236], np.float32) / 255
AMARILLO = rgb("ffd65a")
BLANCO = rgb("fbf7ee")
ROSA = rgb("f08a9a")


# ------------------------------------------------------------ buzo
def _ojos(im, cara, ex, ey, s, t, seed, sx=1.0):
    """Ojos dentro del visor. ex = separación, (centro en coords de pantalla ya transformadas: lista de 2 puntos)."""
    for i, (x, y) in enumerate(ex):
        sd = seed + 11 * i
        if cara in ("normal", "parpadeo"):
            if cara == "parpadeo":
                linea(im, [(x - 8 * s, y), (x + 8 * s, y + 1 * s)], 3.4 * s, seed=sd, t=t)
            else:
                forma(im, elipse(x, y, 7.5 * s, 10 * s), TINTA, t, sd, tinta=0, amp=0.5)
                brillo(im, x + 2.5 * s, y - 3.5 * s, 2.2 * s, BLANCO, 1.3)
        elif cara in ("susto", "abiertos"):
            forma(im, elipse(x, y, 13 * s, 14.5 * s), BLANCO, t, sd, tinta=2.6 * s, amp=0.6)
            forma(im, elipse(x + 1.5 * s * sx, y + 1 * s, 5.5 * s, 6.5 * s), TINTA, t, sd + 3, tinta=0, amp=0.4)
        elif cara == "feliz":
            linea(im, curva([(x - 9 * s, y + 4 * s), (x, y - 6 * s), (x + 9 * s, y + 4 * s)], 6), 3.6 * s, seed=sd, t=t)
        elif cara == "apretados":
            d = -1 if i == 0 else 1
            linea(im, [(x - 9 * s * d, y - 7 * s), (x + 7 * s * d, y), (x - 9 * s * d, y + 7 * s)], 3.4 * s, seed=sd, t=t)
        elif cara == "mareo":
            a = np.linspace(0, 4 * math.pi, 40)
            r = np.linspace(1, 11, 40) * s
            ang = a + t * 6 * (1 if i == 0 else -1)
            linea(im, np.stack([x + r * np.cos(ang), y + r * np.sin(ang)], 1), 2.6 * s, seed=sd, t=t, punta=False)
        elif cara == "triste":
            forma(im, elipse(x, y + 2 * s, 7 * s, 8 * s), TINTA, t, sd, tinta=0, amp=0.5)
            d = 1 if i == 0 else -1
            linea(im, [(x - 11 * s * d, y - 10 * s), (x + 9 * s * d, y - 15 * s)], 2.8 * s, seed=sd + 5, t=t)


def buzo(im, x, y, s, t, rot=0.0, cara="normal", brazos=(0.35, -0.35), codos=(0.4, -0.4), patada=1.0, vel=6.0, sx=1.0,
         lampara=False, seed=100, rubor=True, apretado=0.0, traje=None, traje_osc=None, franja=None, pelo=None, guante_roto=0.0):
    """Buzo chibi de frente. (x, y) = centro del torso. brazos: ángulo de cada hombro (0 = colgando, + hacia fuera);
    patada: amplitud del aleteo; apretado 0..1 lo achata de lado (paredes que aprietan); traje/franja/pelo = otro buzo;
    guante_roto 0..1 = un dedo asoma por el guante y se enrojece (el ácido)."""
    g = globals()
    TRAJE = g["TRAJE"] if traje is None else traje
    TRAJE_OSC = g["TRAJE_OSC"] if traje_osc is None else traje_osc
    FRANJA = g["FRANJA"] if franja is None else franja
    PELO = g["PELO"] if pelo is None else pelo
    sq = 1 - 0.28 * apretado

    def T(p):
        q = np.asarray(p, np.float32).copy()
        q[:, 0] *= sq
        q[:, 1] *= 1 + 0.12 * apretado
        return tr(q, x, y, s, rot, sx)

    a_ = s * 1.0
    # tanque detrás (asoma a la izquierda) y manguera
    tq = T(rrect(-58, -6, 50, 128, 22))
    forma(im, tq, TANQUE, t, seed + 1, tinta=4.2 * a_, sombra=(rgb("b5781c"), 10, 0, 0.6), luz=(BLANCO, -10, 8, 0.22))
    forma(im, T(rrect(-58, -78, 22, 16, 5)), rgb("5b5f66"), t, seed + 2, tinta=3.4 * a_)
    # piernas con aletas
    for i, d in enumerate((-1, 1)):
        ang = d * 0.12 + patada * 0.42 * math.sin(t * vel + i * math.pi)
        hip = np.array([d * 20, 44], np.float32)
        rodilla = hip + 34 * np.array([math.sin(ang), math.cos(ang)])
        pie = rodilla + 32 * np.array([math.sin(ang * 1.4), math.cos(ang * 1.4)])
        forma(im, T(cinta([hip, rodilla, pie], 30, 26)), TRAJE_OSC, t, seed + 10 + i, tinta=4 * a_)
        aleta = tr(np.array([(-17, 0), (17, 0), (30, 74), (0, 64), (-30, 74)], np.float32), 0, 0, 1, -ang * 1.6)
        aleta = aleta + pie
        forma(im, T(aleta), ALETA, t, seed + 12 + i, tinta=4 * a_, sombra=(rgb("a8461d"), 6 * d, -4, 0.5))
    # torso
    torso = curva([(-44, -52), (44, -52), (50, 8), (40, 56), (-40, 56), (-50, 8)], 8, True)
    forma(im, T(torso), TRAJE, t, seed + 20, tinta=4.6 * a_, sombra=(TRAJE_OSC, 14, 0, 0.55), luz=(BLANCO, -12, 10, 0.12))
    forma(im, T(np.array([(-47, -14), (47, -14), (48, 2), (-48, 2)], np.float32)), FRANJA, t, seed + 21, tinta=2.6 * a_)
    forma(im, T(rrect(0, 40, 92, 12, 5)), rgb("23262c"), t, seed + 22, tinta=2.6 * a_)
    forma(im, T(rrect(0, 40, 18, 16, 4)), rgb("c9cdd3"), t, seed + 23, tinta=2.4 * a_)
    # brazos
    for i, d in enumerate((-1, 1)):
        hom = np.array([d * 40, -38], np.float32)
        a1 = brazos[i] * d
        codo = hom + 40 * np.array([math.sin(a1), math.cos(a1)])
        a2 = a1 + codos[i] * d
        mano = codo + 36 * np.array([math.sin(a2), math.cos(a2)])
        forma(im, T(cinta([hom, codo, mano], 25, 22)), TRAJE, t, seed + 30 + i, tinta=4 * a_)
        forma(im, T(elipse(mano[0], mano[1], 14, 14)), rgb("234e5c"), t, seed + 32 + i, tinta=3.6 * a_)
        if guante_roto > 0 and i == 1:
            dd = mano + 14 * np.array([math.sin(a2), math.cos(a2)])
            forma(im, T(elipse(dd[0], dd[1], 7, 9)), PIEL * (1 - guante_roto) + rgb("e0574a") * guante_roto, t, seed + 34,
                  tinta=2.6 * a_)
    # cabeza
    hc = np.array([0, -122], np.float32)
    cab = elipse(hc[0], hc[1], 72, 68)
    forma(im, T(cab), PIEL, t, seed + 40, tinta=4.8 * a_, sombra=(rgb("d9967a"), 12, -2, 0.45))
    pelo = curva([(-74, -118), (-62, -168), (-20, -194), (28, -192), (66, -164), (76, -116), (52, -146), (14, -150),
                  (-20, -142), (-48, -150)], 7, True)
    forma(im, T(pelo), PELO, t, seed + 41, tinta=4.2 * a_, luz=(BLANCO, -6, 10, 0.12))
    linea(im, T(curva([(4, -190), (10, -214), (26, -222)], 6)), 4.4 * a_, seed=seed + 42, t=t)          # mechón
    # correa del visor y lámpara
    linea(im, T(curva([(-74, -132), (-40, -158), (0, -164), (40, -158), (74, -132)], 6)), 7 * a_, col=rgb("23262c"),
          seed=seed + 43, t=t, punta=False, seco=0.1)
    if lampara:
        forma(im, T(rrect(0, -170, 30, 20, 6)), rgb("d8dbe0"), t, seed + 44, tinta=3 * a_)
        forma(im, T(elipse(0, -170, 9, 7)), AMARILLO, t, seed + 45, tinta=2 * a_)
    # visor
    forma(im, T(rrect(0, -124, 132, 66, 28)), VISOR, t, seed + 46, tinta=4.6 * a_)
    forma(im, T(rrect(0, -124, 114, 50, 21)), CRISTAL, t, seed + 47, tinta=2.6 * a_, alfa=0.92, luz=(BLANCO, 8, 10, 0.25))
    oc = T(np.array([(-26, -122), (26, -122)], np.float32))
    _ojos(im, cara, list(oc), 0, s, t, seed + 50, sx)
    linea(im, T(curva([(-46, -138), (-34, -144), (-18, -146)], 5)), 3.4 * a_, col=BLANCO, seed=seed + 48, t=t, alfa=0.8, seco=0)
    if rubor:
        for d in (-1, 1):
            lavado(im, T(elipse(d * 44, -88, 13, 8)), ROSA, 0.45, seed + 49 + d)
    # regulador en la boca
    forma(im, T(rrect(4, -76, 30, 18, 7)), TANQUE, t, seed + 52, tinta=3.2 * a_)
    forma(im, T(elipse(4, -76, 6, 5)), rgb("23262c"), t, seed + 53, tinta=0)
    linea(im, T(curva([(-58, -82), (-44, -64), (-20, -62), (-8, -72)], 6)), 8 * a_, col=rgb("3a3d44"), seed=seed + 54, t=t,
          punta=False, seco=0.05)
    return T(np.array([(4, -84)], np.float32))[0]           # boca (de ahí salen las burbujas)


# ------------------------------------------------------------ Kuri
def kuri(im, x, y, s, t, cara="normal", rot=0.0, brazos=(0.5, 0.5), luz=1.0, seed=300, sx=1.0, aura=True):
    """Kuri flotando. (x, y) = centro del cuerpo. luz 0..1 = cuánto brilla la pantalla y la antena."""
    def T(p):
        return tr(p, x, y, s, rot, sx)

    a_ = s
    if aura and luz > 0:
        brillo(im, x, y, 120 * s, OJO_K * 0.55, 0.22 * luz)
    for i, d in enumerate((-1, 1)):
        ang = brazos[i]
        p0 = np.array([d * 50, 6], np.float32)
        p1 = p0 + np.array([d * 26 * math.cos(ang), -26 * math.sin(ang)])
        forma(im, T(cinta([p0, p1], 15, 13)), KURI_OSC, t, seed + i, tinta=3.4 * a_)
    cuerpo = elipse(0, 0, 58, 54)
    forma(im, T(cuerpo), KURI, t, seed + 5, tinta=4.6 * a_, sombra=(KURI_OSC, 0, -12, 0.65), luz=(BLANCO, -10, 12, 0.22))
    linea(im, T(curva([(0, -54), (4, -74), (10, -88)], 5)), 4 * a_, seed=seed + 6, t=t)
    fx, fy = T(np.array([(10, -92)], np.float32))[0]
    forma(im, T(elipse(10, -92, 9, 9)), AMARILLO, t, seed + 7, tinta=3 * a_)
    if luz > 0:
        brillo(im, fx, fy, 26 * s, AMARILLO, 0.55 * luz)
    pan = rrect(0, -4, 80, 52, 17)
    forma(im, T(pan), PANTALLA, t, seed + 8, tinta=3.6 * a_)
    if luz > 0:
        brillo_forma(im, T(pan), OJO_K, 10 * s, 0.10 * luz)
    oc = T(np.array([(-17, -6), (17, -6)], np.float32))
    col = OJO_K * (0.45 + 0.55 * luz)
    for i, (ox, oy) in enumerate(oc):
        sd = seed + 20 + i
        if cara == "normal":
            parp = (t * 0.7 + i * 0.0) % 3.1 < 0.12
            h = 3 if parp else 13
            forma(im, rrect(ox, oy, 9 * s, h * s, 4 * s), col, t, sd, tinta=0, amp=0.3)
        elif cara == "feliz":
            linea(im, curva([(ox - 8 * s, oy + 4 * s), (ox, oy - 5 * s), (ox + 8 * s, oy + 4 * s)], 5), 3.6 * s, col=col, seed=sd, t=t, seco=0)
        elif cara == "susto":
            forma(im, elipse(ox, oy, 9 * s, 10 * s), col, t, sd, tinta=0, amp=0.3)
            forma(im, elipse(ox, oy, 4 * s, 4.5 * s), PANTALLA, t, sd + 2, tinta=0, amp=0.2)
        elif cara == "apretados":
            d = -1 if i == 0 else 1
            linea(im, [(ox - 7 * s * d, oy - 6 * s), (ox + 6 * s * d, oy), (ox - 7 * s * d, oy + 6 * s)], 3.4 * s, col=col, seed=sd, t=t, seco=0)
        elif cara == "triste":
            forma(im, rrect(ox, oy + 2 * s, 9 * s, 9 * s, 4 * s), col, t, sd, tinta=0, amp=0.3)
            d = 1 if i == 0 else -1
            linea(im, [(ox - 9 * s * d, oy - 8 * s), (ox + 7 * s * d, oy - 12 * s)], 2.6 * s, col=col, seed=sd + 4, t=t, seco=0)
        elif cara == "corazon":
            corazon(im, ox, oy, 0.55 * s, t, sd, col=col, tinta=0)
        if luz > 0:
            brillo(im, ox, oy, 12 * s, OJO_K, 0.35 * luz)


# ------------------------------------------------------------ cachalote
def cachalote(im, x, y, s, t, sx=1.0, rot=0.0, boca=0.0, bulto=None, cola=1.0, seed=500, col=None, ojo="abierto", arrugas=True):
    """Cachalote de perfil mirando a la derecha (sx=-1: a la izquierda). (x, y) = centro; largo ≈ 1100·s.
    boca 0..1 abre la mandíbula; bulto = (u 0..1 de la cabeza a la cola, tamaño) dibuja algo tragado bajando."""
    col = rgb("5f6e88") if col is None else col
    osc = col * 0.62
    claro = np.minimum(col * 1.35, 1)

    def T(p):
        return tr(p, x, y, s, rot, sx)

    ang_c = 0.22 * math.sin(t * 1.6) * cola
    # aleta caudal
    fl = np.array([(-470, 0), (-560, -40), (-640, -96), (-606, -18), (-640, 96), (-560, 40)], np.float32)
    fl = tr(fl + (470, 0), -470, 0, 1, ang_c)
    forma(im, T(curva(fl, 5, True)), osc * 1.15, t, seed + 1, tinta=5 * s)
    # interior de la boca (detrás de la mandíbula)
    if boca > 0.02:
        boc = np.array([(230, 70), (480, 50), (470, 70 + 140 * boca), (230, 100)], np.float32)
        forma(im, T(boc), rgb("5a1f2c"), t, seed + 2, tinta=0, sombra=(rgb("2a0d14"), 0, 30, 0.8))
        forma(im, T(np.array([(300, 82), (460, 66), (452, 60 + 90 * boca), (300, 96)], np.float32)), rgb("b5525e"), t, seed + 3,
              tinta=0, modo="lavado", alfa=0.5)
    # cuerpo
    cuerpo = curva([(500, -110), (512, -20), (488, 62), (380, 92), (160, 128), (-100, 112), (-320, 46), (-470, 14),
                    (-472, -12), (-330, -48), (-150, -104), (-60, -122), (-10, -108), (60, -132), (300, -150), (460, -142)], 7, True)
    forma(im, T(cuerpo), col, t, seed + 3, tinta=6 * s, sombra=(osc, 0, -34, 0.7), luz=(claro, 0, 30, 0.18), humedo=8)
    # vientre más claro
    lavado(im, T(curva([(420, 80), (150, 124), (-120, 104), (-200, 80), (60, 92), (300, 70)], 6, True)), claro, 0.25, seed + 4)
    # bulto tragado
    if bulto is not None:
        u, tam = bulto
        bx = lerp(380, -200, u)
        by = lerp(96, 100, u)
        b = elipse(bx, by, 70 * tam, 46 * tam)
        forma(im, T(b), col, t, seed + 5, tinta=0, sombra=(osc, 0, -16, 0.6))
        linea(im, T(curva([(bx - 74 * tam, by - 6), (bx - 30 * tam, by + 44 * tam), (bx + 30 * tam, by + 44 * tam),
                           (bx + 74 * tam, by - 6)], 6)), 5 * s, seed=seed + 6, t=t)
    # aleta pectoral
    forma(im, T(curva([(300, 82), (250, 150), (196, 168), (226, 96)], 5, True)), osc * 1.1, t, seed + 7, tinta=4.4 * s)
    # mandíbula estrecha
    ang = -0.55 * boca
    mand = np.array([(230, 84), (472, 68), (478, 84), (230, 104)], np.float32)
    mand = tr(mand - (230, 92), 230, 92, 1, -ang)
    forma(im, T(mand), claro * 0.95, t, seed + 8, tinta=4 * s)
    if boca > 0.15:
        for k in range(7):
            p = tr(np.array([(270 + 30 * k, 76), (282 + 30 * k, 76), (276 + 30 * k, 60)], np.float32) - (230, 92), 230, 92, 1, -ang)
            forma(im, T(p), BLANCO, t, seed + 9 + k, tinta=1.6 * s, amp=0.3)
    linea(im, T(curva([(240, 86), (360, 80), (470, 70)], 5)), 3.4 * s, seed=seed + 20, t=t)
    # ojo
    if ojo == "abierto":
        forma(im, T(elipse(330, 40, 13, 10)), TINTA, t, seed + 21, tinta=0)
        bx_, by_ = T(np.array([(334, 36)], np.float32))[0]
        brillo(im, bx_, by_, 3.5 * s, BLANCO, 1.0)
    else:
        linea(im, T(curva([(316, 40), (330, 46), (344, 40)], 4)), 4 * s, seed=seed + 21, t=t)
    linea(im, T(curva([(306, 26), (330, 20), (352, 28)], 4)), 3 * s, seed=seed + 22, t=t)
    # arrugas
    if arrugas:
        rg = np.random.default_rng(seed)
        for k in range(14):
            ax = rg.uniform(-380, 120)
            ay = rg.uniform(-70, 60) * (1 - abs(ax) / 700)
            linea(im, T(curva([(ax, ay), (ax + 24, ay - 6 + rg.normal(0, 4)), (ax + 48, ay + rg.normal(0, 4))], 4)),
                  2.6 * s, seed=seed + 30 + k, t=t, alfa=0.55)
    return T


# ------------------------------------------------------------ calamar, pez, alga, burbuja
def calamar(im, x, y, s, t, rot=0.0, seed=700, ojo=True, ondas=1.0):
    def T(p):
        return tr(p, x, y, s, rot)

    rojo = rgb("c9553e")
    osc = rojo * 0.65
    rg = np.random.default_rng(seed)
    for k in range(10):
        largo = 300 if k in (4, 5) else 150 + 20 * rg.random()
        x0 = -30 + 60 * k / 9
        pts = []
        for j in range(9):
            v = j / 8
            pts.append((x0 * (1 + v * 0.8) + 24 * math.sin(t * 3 + k * 0.9 + v * 4) * v * ondas, 60 + largo * v))
        forma(im, T(cinta(pts, 15, 4)), rojo * (0.85 + 0.15 * (k % 2)), t, seed + k, tinta=3 * s)
        if k in (4, 5):
            forma(im, T(elipse(pts[-1][0], pts[-1][1], 12, 22)), rojo, t, seed + 20 + k, tinta=3 * s)
    forma(im, T(curva([(0, -170), (52, -50), (44, 50), (-44, 50), (-52, -50)], 6, True)), rojo, t, seed + 30, tinta=4.4 * s,
          sombra=(osc, 12, 0, 0.6))
    forma(im, T(curva([(0, -175), (60, -130), (0, -110), (-60, -130)], 5, True)), rojo * 0.9, t, seed + 31, tinta=3.6 * s)
    if ojo:
        forma(im, T(elipse(14, 24, 16, 16)), BLANCO, t, seed + 32, tinta=2.6 * s)
        forma(im, T(elipse(17, 26, 8, 8)), TINTA, t, seed + 33, tinta=0)


def pez(im, x, y, s, t, col, sx=1.0, seed=800):
    def T(p):
        return tr(p, x, y, s, 0.08 * math.sin(t * 9 + seed), sx)

    cola = 0.35 * math.sin(t * 12 + seed)
    forma(im, T(tr(np.array([(0, 0), (-30, -20), (-26, 0), (-30, 20)], np.float32), -26, 0, 1, cola)), col * 0.8, t, seed, tinta=2.6 * s)
    forma(im, T(elipse(0, 0, 32, 18)), col, t, seed + 1, tinta=3 * s, sombra=(col * 0.6, 0, -6, 0.5))
    forma(im, T(elipse(16, -4, 4, 4)), TINTA, t, seed + 2, tinta=0)


def alga(im, x0, y0, largo, t, seed=900, col=None, grosor=26):
    col = rgb("6f8f3f") if col is None else col
    pts = []
    for j in range(10):
        v = j / 9
        pts.append((x0 + 30 * math.sin(t * 1.3 + v * 3 + seed) * v + 12 * math.sin(v * 7 + seed), y0 - largo * v))
    forma(im, cinta(pts, grosor, grosor * 0.35), col, t, seed, tinta=3.6, sombra=(col * 0.6, 8, 0, 0.5))
    for j in (3, 5, 7):
        px, py = pts[j]
        d = 1 if j % 2 else -1
        hoja = curva([(px, py), (px + d * 46, py - 30), (px + d * 70, py - 10), (px + d * 30, py + 6)], 5, True)
        forma(im, hoja, col * 1.08, t, seed + j, tinta=3)


def burbuja(im, x, y, r, t, seed=0):
    p = elipse(x, y, r, r, n=28)
    lavado(im, p, rgb("e8f7fb"), 0.35, seed, humedo=max(1.5, r * 0.2))
    linea(im, p, max(1.6, r * 0.12), seed=seed, t=t, cerrado=True, amp=0.5, alfa=0.85)
    brillo(im, x - r * 0.35, y - r * 0.35, r * 0.28, BLANCO, 0.9)


# ------------------------------------------------------------ iconos (como la referencia)
def exclama(im, x, y, s, t, seed=1000, col=None):
    col = AMARILLO if col is None else col
    forma(im, tr(np.array([(-10, -46), (10, -46), (5, 10), (-5, 10)], np.float32), x, y, s), col, t, seed, tinta=3.4 * s)
    forma(im, elipse(x, y + 26 * s, 8 * s, 8 * s), col, t, seed + 1, tinta=3 * s)
    brillo(im, x, y, 40 * s, col, 0.2)


def pregunta(im, x, y, s, t, seed=1010):
    rotulo(im, "?", x, y, int(80 * s), rgb("9dd0f0"), t, seed)


_NUBE = None


def _nube_local():
    global _NUBE
    if _NUBE is None:
        m = np.zeros((200, 300), np.uint8)
        for (cx, cy, r) in ((90, 120, 50), (150, 90, 62), (215, 118, 48), (150, 135, 50)):
            cv2.circle(m, (cx, cy), r, 255, -1)
        c, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        p = max(c, key=len)[:, 0, :].astype(np.float32)[::4]
        _NUBE = (p - (150, 115)) / 100
    return _NUBE


def nube_lluvia(im, x, y, s, t, seed=1020, lluvia=True):
    forma(im, tr(_nube_local(), x, y, 100 * s), rgb("e9eef4"), t, seed, tinta=3.6 * s, sombra=(rgb("a9b4c4"), 0, -14 * s, 0.6))
    if lluvia:
        for k in range(4):
            u = (t * 1.6 + k * 0.27) % 1
            gx = x + (-60 + 40 * k) * s
            gy = y + (60 + 70 * u) * s
            gota(im, gx, gy, 0.35 * s, t, seed + 5 + k, alfa=1 - u)


def destello(im, x, y, s, t, seed=1030, col=None, f=1.0):
    col = rgb("f5f0b0") if col is None else col
    r = 40 * s * (0.85 + 0.15 * math.sin(t * 7 + seed))
    a = np.linspace(0, 2 * math.pi, 9)[:-1]
    rr = np.where(np.arange(8) % 2 == 0, r, r * 0.26)
    pts = np.stack([x + rr * np.sin(a), y - rr * np.cos(a)], 1)
    pts = curva(pts, 4, True)
    brillo(im, x, y, r * 1.4, col, 0.45 * f)
    forma(im, pts, col, t, seed, tinta=2.8 * s, amp=0.4)


def corazon(im, x, y, s, t, seed=1040, col=None, tinta=3.0):
    col = ROSA if col is None else col
    a = np.linspace(0, 2 * math.pi, 40, endpoint=False)
    hx = 16 * np.sin(a) ** 3
    hy = -(13 * np.cos(a) - 5 * np.cos(2 * a) - 2 * np.cos(3 * a) - np.cos(4 * a))
    forma(im, np.stack([x + hx * 1.4 * s, y + hy * 1.4 * s], 1), col, t, seed, tinta=tinta * s, amp=0.5)


def gota(im, x, y, s, t, seed=1050, alfa=1.0):
    p = curva([(0, -40), (22, 6), (0, 26), (-22, 6)], 6, True)
    forma(im, tr(p, x, y, s), rgb("8fd0f2"), t, seed, tinta=3 * s, alfa=alfa, amp=0.4)


def mareo(im, x, y, s, t, seed=1060):
    for k in range(3):
        a = t * 4 + k * 2.09
        destello(im, x + 70 * s * math.cos(a), y + 22 * s * math.sin(a), 0.4 * s, t, seed + k, col=AMARILLO, f=0.6)
