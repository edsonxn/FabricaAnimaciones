# -*- coding: utf-8 -*-
"""Personajes y utilería de «¿Cómo VE una IA?» (kit acuarela.py; Kuri e iconos vienen de personajes.py).
    nina(...)          chibi de frente con coletas, suéter mostaza y falda; sostiene cosas con las manos
    gato(...)          gato naranja atigrado acostado/dormido (o despierto, o de espaldas) · teclado(...)
    lienzo(...)        pinta una «foto» o tarjeta UNA VEZ en un lienzo propio (cacheado) → pegar(...) la pone en pantalla
                       con escala, giro y marco de papel (polaroid); fotos: foto_gato, dibujo_nino, radiografia, meme_gato
    globo(...)         globo de diálogo pintado con texto (Kuri «escribe» letra a letra)
    celda(...)         un píxel gigante con su color y sus tres números (R, V, A)
"""
import math

import cv2
import numpy as np

import acuarela as A
from acuarela import (TINTA, H, W, brillo, cinta, clamp, curva, elipse, forma, lavado, linea, lerp, mancha_pts, rgb, rotulo,
                      rrect, tr)
from comun import cache
from personajes import AMARILLO, BLANCO, PIEL, ROSA, _ojos

PELO_N = rgb("4b2c22")
SUETER = rgb("e8b53e")
SUETER_OSC = rgb("b98a24")
FALDA = rgb("5b6fb5")
MEDIA = rgb("f3efe6")
ZAPATO = rgb("b8443a")
NARANJA = rgb("ee9a45")
NARANJA_OSC = rgb("c56a26")
NARANJA_CLARO = rgb("f8cf96")
MADERA = rgb("b98352")
MADERA_OSC = rgb("8a5a34")
TECLA = rgb("e9e4da")
GRIS = rgb("8d8f96")


# ------------------------------------------------------------ niña chibi
def _boca(im, T, tipo, t, seed, a_):
    if tipo == "sonrisa":
        linea(im, T(curva([(-14, -84), (0, -75), (14, -84)], 6)), 3.6 * a_, seed=seed, t=t)
    elif tipo == "o":
        forma(im, T(elipse(0, -78, 8, 10)), rgb("6a2b2b"), t, seed, tinta=3 * a_)
    elif tipo == "abierta":
        forma(im, T(curva([(-15, -86), (15, -86), (10, -70), (0, -66), (-10, -70)], 6, True)), rgb("6a2b2b"), t, seed,
              tinta=3.2 * a_)
        forma(im, T(elipse(0, -70, 7, 3.5)), ROSA, t, seed + 1, tinta=0)
    elif tipo == "duda":
        linea(im, T(curva([(-12, -80), (0, -82), (12, -77)], 6)), 3.4 * a_, seed=seed, t=t)
    else:
        linea(im, T([(-10, -80), (10, -80)]), 3.4 * a_, seed=seed, t=t)


def nina(im, x, y, s, t, rot=0.0, cara="normal", boca="sonrisa", brazos=(0.3, 0.3), codos=(0.4, 0.4), anda=0.0, vel=7.0,
         sx=1.0, seed=100, mira=0.0, delante=None):
    """Niña chibi de frente. (x, y) = centro del torso. brazos/codos en rad desde la vertical (+ hacia fuera; ~2,4 = arriba).
    mira = desplazamiento de las pupilas (−1..1, izquierda/derecha). delante = función(im, manos) que pinta lo que sostiene
    ENTRE el cuerpo y las manos (una foto, una tableta). Devuelve dict con 'manos', 'pies' y 'cabeza'."""
    def T(p):
        return tr(np.asarray(p, np.float32), x, y, s, rot, sx)

    a_ = s
    # coletas detrás
    for d in (-1, 1):
        sw = 0.12 * math.sin(t * 2.2 + d)
        pts = [(d * 66, -150), (d * (104 + 8 * sw), -128), (d * (112 + 14 * sw), -96), (d * (100 + 18 * sw), -66)]
        forma(im, T(cinta(pts, 30, 14)), PELO_N, t, seed + 2 + d, tinta=3.8 * a_)
    # piernas
    pies = []
    for i, d in enumerate((-1, 1)):
        ang = d * 0.08 + anda * 0.45 * math.sin(t * vel + i * math.pi)
        hip = np.array([d * 20, 46], np.float32)
        rod = hip + 34 * np.array([math.sin(ang), math.cos(ang)])
        pie = rod + 32 * np.array([math.sin(ang), math.cos(ang)])
        forma(im, T(cinta([hip, rod, pie], 22, 20)), MEDIA, t, seed + 10 + i, tinta=3.8 * a_, sombra=(rgb("d8d0c0"), 6 * d, 0, 0.4))
        zap = np.array([(-15, -8), (15, -8), (22, 6), (22, 16), (-16, 16)], np.float32)
        zap[:, 0] *= d
        forma(im, T(zap + pie), ZAPATO, t, seed + 12 + i, tinta=3.8 * a_, luz=(BLANCO, -4, 6, 0.18))
        pies.append(T([pie])[0])
    # falda
    forma(im, T(curva([(-44, 16), (44, 16), (62, 66), (0, 72), (-62, 66)], 6, True)), FALDA, t, seed + 18, tinta=4.2 * a_,
          sombra=(FALDA * 0.7, 14, 0, 0.5))
    # torso (suéter)
    torso = curva([(-44, -54), (44, -54), (50, 6), (46, 30), (-46, 30), (-50, 6)], 8, True)
    forma(im, T(torso), SUETER, t, seed + 20, tinta=4.6 * a_, sombra=(SUETER_OSC, 14, 0, 0.55), luz=(BLANCO, -12, 10, 0.14))
    forma(im, T(curva([(-18, -54), (0, -38), (18, -54)], 4, True)), BLANCO, t, seed + 21, tinta=2.8 * a_)       # cuello
    forma(im, T(elipse(0, -14, 13, 13)), rgb("e35d4a"), t, seed + 22, tinta=2.6 * a_)                           # corazón-parche
    # lo que sostiene va entre el cuerpo y las manos
    manos = []
    geo = []
    for i, d in enumerate((-1, 1)):
        hom = np.array([d * 40, -40], np.float32)
        a1 = brazos[i] * d
        codo = hom + 36 * np.array([math.sin(a1), math.cos(a1)])
        a2 = a1 + codos[i] * d
        mano = codo + 32 * np.array([math.sin(a2), math.cos(a2)])
        geo.append((hom, codo, mano))
        manos.append(T([mano])[0])
    if delante is not None:
        delante(im, manos)
    for i, (hom, codo, mano) in enumerate(geo):
        forma(im, T(cinta([hom, codo], 24, 20)), SUETER, t, seed + 30 + i, tinta=4 * a_)
        forma(im, T(cinta([codo, mano], 18, 16)), PIEL, t, seed + 32 + i, tinta=3.8 * a_)
        forma(im, T(elipse(mano[0], mano[1], 13, 13)), PIEL, t, seed + 34 + i, tinta=3.6 * a_)
    # cabeza
    forma(im, T(elipse(0, -118, 72, 66)), PIEL, t, seed + 40, tinta=4.8 * a_, sombra=(rgb("d9967a"), 12, -2, 0.45))
    for d in (-1, 1):
        forma(im, T(elipse(d * 72, -112, 11, 15)), PIEL, t, seed + 41 + d, tinta=3.6 * a_)
    # fleco
    forma(im, T(curva([(-74, -118), (-70, -160), (-30, -186), (20, -188), (62, -166), (76, -122), (58, -140), (30, -146),
                       (10, -136), (-14, -148), (-44, -138)], 7, True)), PELO_N, t, seed + 44, tinta=3.8 * a_,
          luz=(BLANCO, -10, 10, 0.12))
    for d in (-1, 1):                                                                                           # moños
        forma(im, T(elipse(d * 66, -152, 14, 12)), rgb("e35d4a"), t, seed + 46 + d, tinta=3 * a_)
    ojos = list(T([(-27 + 5 * mira, -110), (27 + 5 * mira, -110)]))
    _ojos(im, cara, ojos, 0, s * 1.15, t, seed + 50, sx)
    for d in (-1, 1):
        lev = 10 if cara in ("susto", "abiertos") else (6 * d if cara == "duda" else 0)
        linea(im, T(curva([(d * 40, -134 - lev), (d * 27, -140 - lev), (d * 14, -136 - lev)], 4)), 3.4 * a_, seed=seed + 55 + d, t=t)
    lavado(im, T(elipse(-46, -88, 13, 8)), ROSA, 0.55, seed + 58)
    lavado(im, T(elipse(46, -88, 13, 8)), ROSA, 0.55, seed + 59)
    _boca(im, T, boca, t, seed + 60, a_)
    return dict(manos=manos, pies=pies, cabeza=T([(0, -120)])[0])


# ------------------------------------------------------------ gato y teclado
def teclado(im, x, y, s, t, seed=4000, rot=0.0, filas=4, cols=12):
    def T(p):
        return tr(np.asarray(p, np.float32), x, y, s, rot)
    w, h = 40 * cols + 30, 40 * filas + 30
    forma(im, T(rrect(0, 0, w, h, 16)), GRIS, t, seed, tinta=4 * s, sombra=(GRIS * 0.7, 0, -10, 0.5))
    for f in range(filas):
        for c in range(cols - (1 if f == filas - 1 else 0)):
            ww_ = 34 if not (f == filas - 1 and c == 4) else 34 * 5
            if f == filas - 1 and 4 < c < 9:
                continue
            cx = -w / 2 + 35 + c * 40 + (ww_ - 34) / 2
            forma(im, T(rrect(cx, -h / 2 + 35 + f * 40, ww_, 32, 7)), TECLA, t, seed + 1 + f * 20 + c, tinta=2.2 * s, amp=0.6)


def gato(im, x, y, s, t, seed=4100, pose="dormido", rot=0.0, sx=1.0, respira=True):
    """Gato naranja atigrado acostado de lado, cabeza a la derecha (sx=-1: a la izquierda). (x, y) = centro del cuerpo.
    pose: 'dormido' (ojos cerrados), 'despierto', 'espalda' (enroscado de espaldas: sin cara)."""
    def T(p):
        return tr(np.asarray(p, np.float32), x, y, s, rot, sx)
    a_ = s
    r = 1 + (0.025 * math.sin(t * 2.4) if respira else 0)
    # cola enroscada por delante
    cola = [(-150, 30), (-180, 0), (-160, -40), (-110, -30)] if pose != "espalda" else [(-170, 10), (-140, 70), (-40, 92), (80, 78)]
    forma(im, T(cinta(cola, 30, 18)), NARANJA, t, seed + 1, tinta=4 * a_)
    for k in range(3):
        u = 0.25 + 0.25 * k
        i = int(u * (len(cola) - 1))
        p = np.array(cola[i]) * (1 - (u * 3 % 1)) + np.array(cola[min(i + 1, 3)]) * (u * 3 % 1)
        linea(im, T([p + (-10, -12), p + (10, 12)]), 5 * a_, col=NARANJA_OSC, seed=seed + 2 + k, t=t)
    # cuerpo
    cuerpo = elipse(0, 0, 160, 78 * r)
    forma(im, T(cuerpo), NARANJA, t, seed + 5, tinta=4.8 * a_, sombra=(NARANJA_OSC, 0, -16, 0.6), luz=(BLANCO, -12, 14, 0.18))
    lavado(im, T(elipse(10, 34, 110, 30)), NARANJA_CLARO, 0.55, seed + 6)
    for k in range(5):                                                                                   # rayas
        bx = -100 + k * 44
        linea(im, T(curva([(bx, -72 * r), (bx + 10, -40), (bx + 2, -14)], 4)), 9 * a_, col=NARANJA_OSC, seed=seed + 7 + k, t=t)
    # patas delanteras
    for k in range(2):
        forma(im, T(elipse(90 + 40 * k, 62, 34, 17)), NARANJA_CLARO, t, seed + 14 + k, tinta=3.6 * a_)
    if pose == "espalda":
        for d in (-1, 1):                                                                                # orejas de espaldas
            forma(im, T(curva([(110 + d * 34, -62), (118 + d * 44, -122), (140 + d * 20, -70)], 3, True)), NARANJA, t,
                  seed + 20 + d, tinta=3.8 * a_)
        return dict(cabeza=T([(130, -40)])[0])
    # cabeza
    cx, cy = 150, -30
    for d in (-1, 1):
        o = [(cx + d * 40, cy - 40), (cx + d * 56, cy - 104), (cx + d * 6, cy - 62)]
        forma(im, T(curva(o, 3, True)), NARANJA, t, seed + 20 + d, tinta=4 * a_)
        forma(im, T(curva([(cx + d * 38, cy - 50), (cx + d * 48, cy - 88), (cx + d * 16, cy - 62)], 3, True)), ROSA, t,
              seed + 22 + d, tinta=0)
    forma(im, T(elipse(cx, cy, 72, 62)), NARANJA, t, seed + 25, tinta=4.6 * a_, sombra=(NARANJA_OSC, 10, -4, 0.5))
    lavado(im, T(elipse(cx, cy + 22, 40, 26)), NARANJA_CLARO, 0.7, seed + 26)
    for k in range(3):
        linea(im, T(curva([(cx - 18 + k * 18, cy - 60), (cx - 16 + k * 16, cy - 40)], 3)), 6 * a_, col=NARANJA_OSC, seed=seed + 27 + k, t=t)
    for d in (-1, 1):
        ex, ey = cx + d * 26, cy - 4
        if pose == "dormido":
            linea(im, T(curva([(ex - 12, ey), (ex, ey + 7), (ex + 12, ey)], 5)), 3.6 * a_, seed=seed + 30 + d, t=t)
        else:
            forma(im, T(elipse(ex, ey, 11, 13)), rgb("b7d36a"), t, seed + 30 + d, tinta=2.8 * a_)
            forma(im, T(elipse(ex, ey, 3.5, 10)), TINTA, t, seed + 32 + d, tinta=0)
        for k in range(2):                                                                               # bigotes
            linea(im, T([(cx + d * 30, cy + 22 + k * 8), (cx + d * 92, cy + 12 + k * 18)]), 2.2 * a_, seed=seed + 34 + d * 3 + k, t=t)
    forma(im, T(curva([(cx - 8, cy + 14), (cx + 8, cy + 14), (cx, cy + 24)], 3, True)), ROSA, t, seed + 40, tinta=2.6 * a_)
    linea(im, T(curva([(cx - 10, cy + 32), (cx, cy + 28), (cx + 10, cy + 32)], 4)), 2.8 * a_, seed=seed + 41, t=t)
    return dict(cabeza=T([(cx, cy)])[0], oreja=T([(cx + 50, cy - 96)])[0], ojo=T([(cx + 26, cy - 4)])[0])


# ------------------------------------------------------------ «fotos» y tarjetas: se pintan una vez y se pegan
def lienzo(nombre, w, h, pintar, t=0.0):
    """Pinta `pintar(im, w, h, t)` en el centro del cuadro y devuelve el recorte (h, w, 3), cacheado por nombre y boil(t)."""
    def f():
        im = np.ones((H, W, 3), np.float32)
        x0, y0 = (W - w) // 2, (H - h) // 2
        pintar(im, x0, y0, w, h, t)
        return im[y0:y0 + h, x0:x0 + w].copy()
    return cache(("lienzo", nombre, A.boil(t) % 2), f)


def pegar(im, img, cx, cy, esc=1.0, rot=0.0, alfa=1.0, marco=24, sombra=True, t=0.0, seed=4500, marco_col=None):
    """Pone `img` centrada en (cx, cy) con escala y giro, con marco de papel tipo polaroid y contorno de tinta."""
    if esc <= 0.01 or alfa <= 0.01:
        return None
    h, w = img.shape[:2]
    mw, mh = (w + 2 * marco) * esc, (h + 2 * marco + (marco * 2 if marco else 0)) * esc
    caja = rrect(cx, cy + (marco * esc if marco else 0) * 0.5, mw, mh, 6 * esc, rot)
    if sombra:
        lavado(im, caja + np.array([10 * esc, 14 * esc]), rgb("6a5a4a"), 0.35 * alfa, seed + 1, humedo=6)
    if marco:
        forma(im, caja, marco_col if marco_col is not None else BLANCO, t, seed, tinta=3.4 * min(esc, 1.4), alfa=alfa)
    M = cv2.getRotationMatrix2D((w / 2, h / 2), -math.degrees(rot), esc)
    M[0, 2] += cx - w / 2
    M[1, 2] += cy - h / 2
    src = np.concatenate([img, np.ones((h, w, 1), np.float32)], -1)
    out = cv2.warpAffine(src, M, (W, H), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
    a = out[..., 3:4] * alfa
    im *= 1 - a
    im += out[..., :3] * a
    linea(im, rrect(cx, cy, w * esc, h * esc, 2, rot), 2.4, seed=seed + 2, t=t, cerrado=True, punta=False, alfa=0.8 * alfa)
    return caja


def _fondo_escritorio(im, x0, y0, w, h, t):
    sub = im[y0:y0 + h, x0:x0 + w]
    u = np.linspace(0, 1, h, dtype=np.float32)[:, None, None]
    sub[:] = rgb("e9d6b4") * (1 - u) + rgb("c99a68") * u
    lavado(im, np.array([(x0, y0 + h * 0.55), (x0 + w, y0 + h * 0.5), (x0 + w, y0 + h), (x0, y0 + h)], np.float32), MADERA,
           0.75, 4600, humedo=10)
    for k in range(4):
        linea(im, curva([(x0, y0 + h * (0.62 + 0.09 * k)), (x0 + w * 0.5, y0 + h * (0.6 + 0.09 * k)),
                         (x0 + w, y0 + h * (0.58 + 0.09 * k))], 6), 2, col=MADERA_OSC, seed=4610 + k, t=0, alfa=0.45, punta=False)
    lavado(im, mancha_pts(x0 + w * 0.82, y0 + h * 0.2, 90, 4620, 0.3), rgb("f6e08a"), 0.5, 4620, humedo=12)    # lámpara


def foto_gato(t=0.0, pose="dormido"):
    """La foto del gancho: gato naranja dormido sobre un teclado, 560x420."""
    def p(im, x0, y0, w, h, t_):
        _fondo_escritorio(im, x0, y0, w, h, t_)
        teclado(im, x0 + w * 0.5, y0 + h * 0.72, 0.85, t_)
        gato(im, x0 + w * 0.45, y0 + h * 0.6, 1.05, t_, pose=pose, respira=False)
    return lienzo(("gato", pose), 560, 420, p, t)


def dibujo_nino(t=0.0):
    """Dibujo infantil con crayones: casa, sol y un perro."""
    def p(im, x0, y0, w, h, t_):
        im[y0:y0 + h, x0:x0 + w] = rgb("fbf8f0")
        cr = lambda pts, c, sd, a=7: linea(im, curva(pts, 8), a, col=c, seed=sd, t=t_, amp=2.6, seco=0.5)
        cr([(x0 + 30, y0 + h - 60), (x0 + w - 30, y0 + h - 64)], rgb("4caf50"), 4700, 10)
        cr([(x0 + 110, y0 + 300), (x0 + 110, y0 + 190), (x0 + 190, y0 + 130), (x0 + 270, y0 + 190), (x0 + 270, y0 + 300),
            (x0 + 110, y0 + 300)], rgb("e04a3c"), 4701)
        cr([(x0 + 175, y0 + 300), (x0 + 175, y0 + 250), (x0 + 205, y0 + 250), (x0 + 205, y0 + 300)], rgb("7a4a2a"), 4702)
        cr(elipse(x0 + w - 90, y0 + 80, 44, 44), rgb("f2b81d"), 4703, 8)
        for k in range(8):
            a = k / 8 * 2 * math.pi
            cr([(x0 + w - 90 + 55 * math.cos(a), y0 + 80 + 55 * math.sin(a)),
                (x0 + w - 90 + 80 * math.cos(a), y0 + 80 + 80 * math.sin(a))], rgb("f2b81d"), 4704 + k, 6)
        cr(elipse(x0 + 400, y0 + 290, 60, 34), rgb("8a5a34"), 4720)
        cr(elipse(x0 + 460, y0 + 250, 30, 28), rgb("8a5a34"), 4721)
        for k in range(4):
            cr([(x0 + 360 + k * 26, y0 + 316), (x0 + 360 + k * 26, y0 + 350)], rgb("8a5a34"), 4722 + k, 6)
    return lienzo("dibujo", 560, 420, p, t)


def radiografia(t=0.0):
    """Radiografía de una mano: huesos blanco-azulados sobre negro."""
    def p(im, x0, y0, w, h, t_):
        im[y0:y0 + h, x0:x0 + w] = rgb("0e1620")
        brillo(im, x0 + w / 2, y0 + h / 2, 210, rgb("3d5a70"), 0.5)
        hueso = rgb("dbe7f0")
        cx, cy = x0 + w / 2, y0 + h * 0.78
        forma(im, rrect(cx, cy, 120, 90, 30), hueso * 0.8, t_, 4801, tinta=0, alfa=0.85)
        for k, (ang, lg) in enumerate([(-1.05, 120), (-0.4, 190), (-0.12, 210), (0.14, 200), (0.4, 170)]):
            px, py = cx + 50 * math.sin(ang) * (2 if k == 0 else 1), cy - 40
            for j in range(3):
                l = lg / 3
                a0 = (px + l * j * math.sin(ang), py - l * j * math.cos(ang))
                a1 = (px + l * (j + 0.85) * math.sin(ang), py - l * (j + 0.85) * math.cos(ang))
                forma(im, cinta([a0, a1], 20 - 3 * j, 17 - 3 * j), hueso, t_, 4810 + k * 5 + j, tinta=0, alfa=0.9)
        brillo(im, cx, cy - 80, 220, rgb("7fa6c4"), 0.12)
    return lienzo("rayosx", 560, 420, p, t)


def meme_gato(t=0.0):
    """Meme inventado: gato aplastado en una caja con «LUNES» arriba en letras blancas con borde negro."""
    def p(im, x0, y0, w, h, t_):
        im[y0:y0 + h, x0:x0 + w] = rgb("dfe9ef")
        forma(im, np.array([(x0 + 140, y0 + 230), (x0 + 420, y0 + 230), (x0 + 440, y0 + 400), (x0 + 120, y0 + 400)], np.float32),
              rgb("c8955a"), t_, 4900, tinta=4)
        gato(im, x0 + 270, y0 + 220, 0.85, t_, pose="despierto", respira=False, seed=4910)
        forma(im, np.array([(x0 + 120, y0 + 260), (x0 + 440, y0 + 260), (x0 + 440, y0 + 400), (x0 + 120, y0 + 400)], np.float32),
              rgb("d8a466"), t_, 4920, tinta=4)
        rotulo(im, "LUNES", x0 + w / 2, y0 + 70, 92, BLANCO, t_, seed=4930, fuente="impact.ttf")
    return lienzo("meme", 560, 420, p, t)


# ------------------------------------------------------------ globos, píxeles
def globo(im, x, y, w, h, texto, t, px=40, n=None, seed=5000, cola=(-1, 1), col=BLANCO, alfa=1.0, lineas=None):
    """Globo de diálogo centrado en (x, y); `n` letras visibles (máquina de escribir); `lineas` = lista de renglones."""
    if alfa <= 0.01:
        return
    forma(im, rrect(x, y, w, h, 34), col, t, seed, tinta=4, alfa=alfa)
    cx, cy = x + cola[0] * w * 0.28, y + cola[1] * h / 2
    forma(im, np.array([(cx - 24, cy - 8 * cola[1]), (cx + 24, cy - 8 * cola[1]), (cx + cola[0] * 46, cy + 50 * cola[1])],
                       np.float32), col, t, seed + 1, tinta=4, alfa=alfa)
    forma(im, rrect(x, y, w - 8, h - 8, 30), col, t, seed + 2, tinta=0, alfa=alfa)
    renglones = lineas if lineas is not None else [texto]
    total = sum(len(r) for r in renglones)
    k = total if n is None else int(n)
    y0 = y - (len(renglones) - 1) * px * 0.6
    for i, r in enumerate(renglones):
        vis = r[:max(0, k)]
        k -= len(r)
        if vis:
            m, _ = A._txt_mask(r, px, "LuckiestGuy-Regular.ttf")
            ancho = m.shape[1]
            mv, _ = A._txt_mask(vis, px, "LuckiestGuy-Regular.ttf")
            rotulo(im, vis, x - ancho / 2 + mv.shape[1] / 2, y0 + i * px * 1.2, px, TINTA, t, seed=seed + 5 + i, tinta=False,
                   alfa=alfa)


def celda(im, x, y, lado, col, t, seed=5100, numeros=True, alfa=1.0, px=None):
    """Un píxel gigante (cuadro de color con contorno de tinta) y, debajo, sus tres números R V A en barras."""
    col = np.asarray(col, np.float32)
    forma(im, rrect(x, y, lado, lado, lado * 0.06), col, t, seed, tinta=4, alfa=alfa, mota=0.25)
    if not numeros:
        return
    px = px or int(lado * 0.2)
    for i, (nom, c) in enumerate((("R", rgb("e0483c")), ("V", rgb("45a85a")), ("A", rgb("3f78c8")))):
        v = int(round(col[i] * 255))
        bx = x - lado * 0.36 + i * lado * 0.36
        by = y + lado * 0.5 + px * 1.6
        rotulo(im, str(v), bx, by, px, c, t, seed=seed + 3 + i, alfa=alfa)


# ------------------------------------------------------------ retratos REALES pasados a acuarela (fotos_reales/, CREDITOS.txt)
RECORTES = {"hubel": (0.02, 0.0, 0.92, 0.80), "wiesel": (0.18, 0.08, 0.92, 0.75), "feifei_li": (0.33, 0.0, 0.80, 0.36),
            "lecun": (0.10, 0.0, 0.90, 0.58), "hubel_wiesel_registro": (0.0, 0.0, 1.0, 1.0)}


def retrato(nombre, w, h, sepia=False):
    """Foto real recortada → acuarela (stylization + tinta en los bordes + tono de papel). Devuelve (h, w, 3) float."""
    def f():
        img = cv2.imread(f"fotos_reales/{nombre}.jpg")
        H0, W0 = img.shape[:2]
        x0, y0, x1, y1 = RECORTES[nombre]
        img = img[int(y0 * H0):int(y1 * H0), int(x0 * W0):int(x1 * W0)]
        ih, iw = img.shape[:2]                                   # recorte al aspecto pedido, centrado arriba
        if iw / ih > w / h:
            nw = int(ih * w / h)
            img = img[:, (iw - nw) // 2:(iw - nw) // 2 + nw]
        else:
            img = img[:int(iw * h / w)]
        img = cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA)
        st = cv2.stylization(img, sigma_s=40, sigma_r=0.35)
        g = cv2.cvtColor(cv2.GaussianBlur(img, (0, 0), 1.2), cv2.COLOR_BGR2GRAY)
        bordes = cv2.Canny(g, 40, 110)
        bordes = cv2.GaussianBlur(cv2.dilate(bordes, np.ones((2, 2), np.uint8)), (0, 0), 0.8).astype(np.float32) / 255
        im = st[..., ::-1].astype(np.float32) / 255
        if sepia:
            gg = im.mean(2, keepdims=True)
            im = np.concatenate([gg * 1.06 + 0.05, gg * 0.92 + 0.03, gg * 0.72], 2)
        im = im * 0.88 + np.array([0.98, 0.93, 0.84], np.float32) * 0.12              # se aclara hacia el papel
        im *= 1 - 0.55 * bordes[..., None] * (1 - TINTA)
        return np.clip(im, 0, 1)
    return cache(("retrato", nombre, w, h, sepia), f)


def camafeo(im, img, cx, cy, esc, t, nombre="", seed=5200, col=None, alfa=1.0, rot=0.0):
    """Retrato en marco ovalado pintado (pegatina «camafeo») con cartela del nombre debajo."""
    if esc <= 0.02 or alfa <= 0.01:
        return
    h, w = img.shape[:2]
    rx, ry = w / 2 * esc, h / 2 * esc
    col = col if col is not None else rgb("c9a45a")
    lavado(im, elipse(cx + 12 * esc, cy + 16 * esc, rx + 26 * esc, ry + 26 * esc), rgb("5a4a3a"), 0.35 * alfa, seed + 1)
    forma(im, elipse(cx, cy, rx + 22 * esc, ry + 22 * esc, rot), col, t, seed, tinta=4.5, alfa=alfa, luz=(BLANCO, -10, 12, 0.3))
    M = cv2.getRotationMatrix2D((w / 2, h / 2), -math.degrees(rot), esc)
    M[0, 2] += cx - w / 2
    M[1, 2] += cy - h / 2
    out = cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR)
    m = np.zeros((H, W), np.float32)
    cv2.ellipse(m, (int(cx), int(cy)), (int(rx), int(ry)), math.degrees(rot), 0, 360, 1.0, -1, cv2.LINE_AA)
    m = cv2.GaussianBlur(m, (0, 0), 1.2)[..., None] * alfa
    im *= 1 - m
    im += out * m
    linea(im, elipse(cx, cy, rx, ry, rot), 3.2, seed=seed + 2, t=t, cerrado=True, punta=False, alfa=alfa)
    if nombre:
        forma(im, rrect(cx, cy + ry + 46 * esc, max(240, len(nombre) * 26) * esc, 64 * esc, 14 * esc), rgb("fbf3df"), t,
              seed + 3, tinta=3.6, alfa=alfa)
        rotulo(im, nombre, cx, cy + ry + 46 * esc, int(38 * esc) + 2, TINTA, t, seed=seed + 4, tinta=False, alfa=alfa)
