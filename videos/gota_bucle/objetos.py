# -*- coding: utf-8 -*-
"""Objetos del video 'El viaje de una gota' (estilo boceto). Todos son `Dib` en coordenadas locales."""
import math
from functools import lru_cache

import numpy as np

import boceto as B
from boceto import (AMARILLO, AZUL, AZUL_CL, AZUL_OSC, GRIS, GRIS_CL, HIELO, MARRON, NARANJA, PIEL, R, ROJO, ROSA, T,
                    VERDE, VERDE_OSC, Dib, arco_, circ, curva, elip, linea, mano_poli, ondas, union_circulos)


# ------------------------------------------------------------------ la gota (mascota)
def _cuerpo_gota():
    C, r, tip = (0.0, 30.0), 64.0, (0.0, -108.0)
    d = C[1] - tip[1]
    phi = math.degrees(math.acos(r / d))
    a0, a1 = -90 + phi, 270 - phi
    arc = arco_(C[0], C[1], r, a0, a1, 40)
    return np.vstack([[tip], arc, [tip]]), arc


CUERPO, _ARC = _cuerpo_gota()
CUERPO_CERR = np.vstack([CUERPO, CUERPO[:1]])


@lru_cache(maxsize=None)
def gota(ojos="abiertos", boca="sonrisa", mejillas=True, brazos=False, mira=0):
    ops = [T(np.vstack([CUERPO, curva([CUERPO[-2], (2, -100), (0, -108)], 4)[1:]]), 6.5, peso=0.5),
           R(CUERPO, (112, 176, 232), peso=0.35, sp=10)]
    ex = 23
    ox = 7 * mira            # la gota mira a un lado (-1, 0, 1)
    if ojos == "abiertos":
        ops += [T(linea((-ex + ox, 14), (-ex + ox, 27)), 10, peso=0.03), T(linea((ex + ox, 14), (ex + ox, 27)), 10, peso=0.03)]
    elif ojos == "feliz":
        ops += [T(arco_(-ex + ox, 26, 10, 200, 340, 8), 5, peso=0.04), T(arco_(ex + ox, 26, 10, 200, 340, 8), 5, peso=0.04)]
    elif ojos == "cerrados":
        ops += [T(arco_(-ex + ox, 22, 10, 20, 160, 8), 4.5, peso=0.04), T(arco_(ex + ox, 22, 10, 20, 160, 8), 4.5, peso=0.04)]
    elif ojos == "miedo":
        ops += [T(circ(-ex + ox, 22, 9, n=14), 4.5, peso=0.05), T(circ(ex + ox, 22, 9, n=14), 4.5, peso=0.05),
                T(linea((-ex + ox, 21), (-ex + ox, 24)), 6, peso=0.02), T(linea((ex + ox, 21), (ex + ox, 24)), 6, peso=0.02)]
    if boca == "sonrisa":
        ops.append(T(arco_(0, 42, 17, 28, 152, 10), 5, peso=0.06))
    elif boca == "o":
        ops.append(T(circ(0, 52, 8, n=14), 4.5, peso=0.05))
    elif boca == "zigzag":
        ops.append(T(linea((-18, 52), (-11, 46), (-4, 54), (4, 46), (11, 54), (18, 47)), 4.5, peso=0.06))
    elif boca == "abierta":
        ops += [T(arco_(0, 40, 17, 5, 175, 12), 4.5, peso=0.06), R(arco_(0, 40, 17, 5, 175, 12), ROSA, peso=0.05, sp=5)]
    elif boca == "ronca":
        ops.append(T(elip(0, 52, 8, 6, n=14), 4.5, peso=0.05))
    if mejillas:
        ops += [R(elip(-42, 44, 11, 7, n=16), ROSA, peso=0.04, sp=5, off=(2, -2)),
                R(elip(42, 44, 11, 7, n=16), ROSA, peso=0.04, sp=5, off=(2, -2))]
    return Dib(ops)


@lru_cache(maxsize=None)
def barba():
    """Barba blanca de anciano (para la gota que duerme tres mil años)."""
    borde = curva([(-52, 60), (-64, 96), (-40, 132), (-10, 168), (0, 190), (12, 166), (42, 130), (66, 94), (54, 60)], 8)
    zig = [linea((-30 + 12 * k, 78 + 8 * (k % 2)), (-28 + 12 * k, 118 + 12 * (k % 3) - 10 * abs(k - 2))) for k in range(6)]
    return Dib([T(borde, 5.5, peso=0.5), R(np.vstack([borde, borde[:1]]), (240, 240, 244), peso=0.3, sp=9)]
               + [T(z, 3.2, peso=0.06) for z in zig])


# ------------------------------------------------------------------ nube y sol
def _contorno_nube(circulos, base, x0, x1, centro):
    """Contorno cerrado de una nube: arcos superiores (ordenados de derecha a izquierda por encima) + base ondulada."""
    pts, _ = union_circulos(circulos, base, centro)
    th = np.arctan2(-(pts[:, 1] - centro[1]), pts[:, 0] - centro[0])
    th = np.where(th < -math.pi / 2, th + 2 * math.pi, th)
    pts = pts[np.argsort(th)]
    xs = np.linspace(pts[-1, 0], pts[0, 0], 26)              # de donde termina el arco izquierdo hasta donde empieza el derecho
    bl = np.stack([xs, base + 4 * np.sin(xs / 60)], 1)
    return np.vstack([pts, bl, pts[:1]])


@lru_cache(maxsize=None)
def nube():
    circulos = [(-190, 30, 85, 84), (-85, -35, 105, -8), (45, -55, 120, -8), (175, -5, 95, 50), (250, 55, 55, 80)]
    P = _contorno_nube(circulos, 108, -258, 294, (20, 20))
    det = [arco_(-130, 20, 40, 200, 290, 10), arco_(30, -10, 52, 210, 300, 10), arco_(190, 30, 34, 200, 290, 10)]
    return Dib([T(P, 6.0, peso=1.0), R(P, AZUL_CL, peso=0.9, sp=12)] + [T(d, 3.6, peso=0.08) for d in det])


@lru_cache(maxsize=None)
def sol(r=76):
    ops = [T(circ(0, 0, r, a0=-1.2), 6.0, peso=0.4), R(circ(0, 0, r, vuelta=1.0, n=40), AMARILLO, peso=0.5, sp=10)]
    for i in range(12):
        a = i * math.pi / 6 + 0.1
        r0, r1 = r * 1.28, r * (1.62 if i % 2 == 0 else 1.5)
        ops.append(T(linea((r0 * math.cos(a), r0 * math.sin(a)), (r1 * math.cos(a), r1 * math.sin(a))), 5.5, peso=0.05))
    return Dib(ops)


# ------------------------------------------------------------------ montaña
@lru_cache(maxsize=None)
def montana():
    izq = [(-470, 0), (-330, -190), (-250, -150), (-90, -390), (40, -300), (150, -410), (330, -190), (400, -230), (500, 0)]
    contorno = mano_poli(np.array(izq), 3.5, seed=3)
    suelo = ondas(-540, 540, 0, 4, 200)
    nieve1 = mano_poli(np.array([(-90, -390), (-160, -262), (-118, -282), (-88, -240), (-40, -285), (0, -250), (40, -300),
                                 (-20, -335), (-90, -390)]), 2.5, seed=8)
    nieve2 = mano_poli(np.array([(150, -410), (85, -290), (128, -305), (160, -262), (205, -300), (240, -262), (330, -190),
                                 (250, -290), (150, -410)]), 2.5, seed=9)
    ops = [T(np.vstack([[(-540, 0)], contorno, [(540, 0)]]), 6.0, peso=1.1),
           R(np.vstack([contorno, contorno[:1]]), (168, 176, 200), peso=0.9, sp=13),
           R(nieve1, HIELO, peso=0.25, sp=8), R(nieve2, HIELO, peso=0.25, sp=8),
           T(nieve1, 4.0, peso=0.3), T(nieve2, 4.0, peso=0.3),
           T(suelo, 5.0, peso=0.4)]
    # pinos
    for (px, py, ps) in [(-390, 0, 0.9), (-330, 0, 1.15), (330, 0, 1.0), (410, 0, 0.8)]:
        ops += _pino(px, py, ps)
    return Dib(ops)


def _pino(x, y, s):
    tri = [linea((x - 38 * s, y - 40 * s), (x, y - 120 * s), (x + 38 * s, y - 40 * s), (x - 38 * s, y - 40 * s)),
           linea((x - 30 * s, y - 90 * s), (x, y - 165 * s), (x + 30 * s, y - 90 * s), (x - 30 * s, y - 90 * s))]
    return [T(linea((x, y), (x, y - 42 * s)), 5, peso=0.05),
            T(tri[0], 4.5, peso=0.1), R(tri[0], VERDE, peso=0.08, sp=7),
            T(tri[1], 4.5, peso=0.1), R(tri[1], VERDE_OSC, peso=0.08, sp=7)]


# ------------------------------------------------------------------ glaciar, copo, marcas
@lru_cache(maxsize=None)
def bloque_hielo(w=300, h=330):
    """Bloque de hielo redondeado donde queda atrapada la gota (centrado)."""
    a, b = w / 2, h / 2
    P = mano_poli(np.array([(-a, -b + 30), (-a + 22, -b + 4), (a - 26, -b), (a, -b + 34), (a + 4, b - 30), (a - 24, b),
                            (-a + 30, b + 2), (-a, b - 26), (-a, -b + 30)]), 3.0, seed=12)
    br = [arco_(-a + 42, -b + 60, 34, 200, 260, 8), linea((a - 70, -b + 24), (a - 34, -b + 18))]
    grietas = [linea((a - 90, b), (a - 70, b - 70), (a - 100, b - 110)), linea((-a + 60, -b + 30), (-a + 40, -b + 90))]
    return Dib([T(P, 6.0, peso=0.8), R(P, HIELO, peso=0.5, sp=10, off=(4, -4)), R(P, AZUL_CL, peso=0.4, sp=22, ang=35)]
               + [T(x, 3.4, peso=0.08) for x in br + grietas])


@lru_cache(maxsize=None)
def copo(r=70):
    ops = []
    for i in range(6):
        a = i * math.pi / 3
        c, s = math.cos(a), math.sin(a)
        ops.append(T(linea((0, 0), (r * c, r * s)), 4.5, peso=0.1))
        for f, l in ((0.55, 0.32), (0.8, 0.22)):
            bx, by = r * f * c, r * f * s
            for sg in (-1, 1):
                aa = a + sg * 0.75
                ops.append(T(linea((bx, by), (bx + r * l * math.cos(aa), by + r * l * math.sin(aa))), 3.6, peso=0.05))
    return Dib(ops)


@lru_cache(maxsize=None)
def marcas(n=20):
    """Palitos de conteo agrupados de cinco en cinco (los años pasan)."""
    ops = []
    for g in range(n // 5):
        gx = (g % 2) * 150
        gy = (g // 2) * 80
        for k in range(4):
            ops.append(T(linea((gx + k * 22, gy), (gx + k * 22 + 3, gy + 54)), 5, peso=0.07))
        ops.append(T(linea((gx - 12, gy + 40), (gx + 84, gy + 10)), 5, peso=0.1))
    return Dib(ops)


# ------------------------------------------------------------------ río
def curva_rio():
    return curva([(-30, -560), (125, -300), (-125, -20), (120, 260), (-30, 640)], 20)


@lru_cache(maxsize=None)
def rio():
    C = curva_rio()
    d = np.gradient(C, axis=0)
    d /= np.linalg.norm(d, axis=1, keepdims=True)
    nrm = np.stack([-d[:, 1], d[:, 0]], 1)
    ancho = 64 + 10 * np.sin(np.linspace(0, 7, len(C)))
    izq = C + nrm * ancho[:, None]
    der = C - nrm * ancho[:, None]
    poly = np.vstack([izq, der[::-1]])
    ops = [T(izq, 5.5, peso=1.0), T(der, 5.5, peso=1.0), R(poly, AZUL, peso=1.6, sp=13, ang=70)]
    for k in range(1, len(C) - 20, 12):        # ondas de agua
        o = 0.32 * ancho[k] * (1 if (k // 12) % 2 else -1)
        p = C[k] + nrm[k] * o
        ops.append(T(ondas(p[0] - 26, p[0] + 26, p[1], 5, 26), 3.6, peso=0.06))
    for k in range(6, len(C) - 8, 18):          # pasto en las orillas
        for lado, pts in ((1, izq), (-1, der)):
            p = pts[k] + nrm[k] * lado * 26
            ops.append(T(linea((p[0] - 10, p[1] - 12), (p[0] - 2, p[1] + 8), (p[0] + 2, p[1] - 14), (p[0] + 4, p[1] + 8), (p[0] + 14, p[1] - 10)),
                         3.8, peso=0.05))
    return Dib(ops)


def punto_rio(u):
    C = curva_rio()
    seg = np.hypot(*np.diff(C, axis=0).T)
    d = np.concatenate([[0.0], np.cumsum(seg)])
    s = u * d[-1]
    return np.array([np.interp(s, d, C[:, 0]), np.interp(s, d, C[:, 1])])


@lru_cache(maxsize=None)
def hoja_barca():
    P = curva([(-80, 0), (-40, -34), (10, -46), (80, -8), (60, 22), (-20, 28), (-80, 0)], 8)
    return Dib([T(P, 5.5, peso=0.35), R(P, VERDE, peso=0.25, sp=8), T(linea((-60, 2), (70, -6)), 3.5, peso=0.08)])


# ------------------------------------------------------------------ grifo, vaso, persona
@lru_cache(maxsize=None)
def grifo():
    tubo = [(-560, -40), (-60, -40), (-8, -34), (34, -6), (40, 30), (40, 60), (-14, 60), (-14, 30), (-30, 8), (-60, 6),
            (-560, 6)]
    P = np.array(tubo)
    manija = [linea((-150, -40), (-150, -84)), linea((-190, -90), (-110, -90))]
    return Dib([T(P, 6.0, peso=0.8), R(np.vstack([P, P[:1]]), GRIS_CL, peso=0.5, sp=9)]
               + [T(m, 6.0, peso=0.1) for m in manija]
               + [T(linea((-14, 66), (40, 66)), 5, peso=0.04)])


def vaso_poli():
    return np.array([(-100, -130), (100, -130), (76, 130), (-76, 130)], float)


@lru_cache(maxsize=None)
def vaso():
    P = vaso_poli()
    return Dib([T(np.vstack([P, P[:1]]), 6.0, peso=0.8), T(arco_(0, -130, 100, 0, 0, 2), 4, peso=0.01),
                T(linea((-78, -100), (-64, 60)), 3.4, peso=0.12, v=170)])


def agua_poli(nivel):
    """Agua dentro del vaso (nivel 0..1)."""
    P = vaso_poli()
    yt = 130 - 250 * nivel
    if nivel <= 0.001:
        return None
    f = (yt + 130) / 260
    xl = -100 + (-76 + 100) * f
    xr = 100 + (76 - 100) * f
    return np.array([(xl, yt), (xr, yt), (76, 130), (-76, 130)], float)


@lru_cache(maxsize=None)
def persona(boca="sonrisa"):
    """Cabeza grande de 'tú', de perfil suave, con hombros."""
    cab = circ(0, 0, 170, a0=-2.0, vuelta=1.03, n=60)
    hombros = curva([(-230, 330), (-180, 230), (-90, 190), (0, 176), (90, 190), (180, 230), (230, 330)], 8)
    ext = arco_(0, 0, 180, 190, 350, 22)
    inte = arco_(0, -14, 138, 350, 190, 22)
    pelo = ext
    pelo_pol = np.vstack([ext, inte])
    ops = [T(cab, 6.5, peso=0.9), R(circ(0, 0, 170, vuelta=1.0, n=44), PIEL, peso=0.8, sp=11),
           T(hombros, 6.0, peso=0.5), R(np.vstack([hombros, [(230, 420), (-230, 420)], hombros[:1]]), NARANJA, peso=0.6, sp=12),
           T(pelo, 6, peso=0.3), R(pelo_pol, (110, 78, 58), peso=0.3, sp=8),
           T(linea((-62, -18), (-62, 6)), 11, peso=0.03), T(linea((62, -18), (62, 6)), 11, peso=0.03),
           T(arco_(-62, -46, 26, 215, 325, 8), 4.5, peso=0.05), T(arco_(62, -46, 26, 215, 325, 8), 4.5, peso=0.05),
           R(elip(-104, 60, 18, 11, n=16), ROSA, peso=0.05, sp=6, off=(2, -2)),
           R(elip(104, 60, 18, 11, n=16), ROSA, peso=0.05, sp=6, off=(2, -2))]
    if boca == "sonrisa":
        ops.append(T(arco_(0, 62, 34, 30, 150, 10), 5, peso=0.06))
    elif boca == "o":
        ops.append(T(circ(0, 84, 16, n=16), 5, peso=0.06))
    return Dib(ops)


# ------------------------------------------------------------------ mar, pez, sol grande, vapor
@lru_cache(maxsize=None)
def mar_capa(y, alt, col, semilla=0, ph=0.0, hilos=True):
    """Banda de mar (coordenadas de pantalla): ondas arriba y relleno hasta y + alt."""
    top = ondas(-30, 1110, y, 15, 210, ph, 60)
    poly = np.vstack([top, [(1110, y + alt), (-30, y + alt)]])
    ops = [T(top, 5.5, peso=0.9), R(poly, col, peso=1.2, sp=13, ang=15)]
    return Dib(ops)


@lru_cache(maxsize=None)
def pez():
    cuerpo = curva([(-90, 0), (-40, -46), (30, -40), (90, 0), (30, 40), (-40, 44), (-90, 0)], 8)
    cola = np.array([(-84, 0), (-140, -42), (-124, 0), (-140, 42), (-84, 0)], float)
    return Dib([T(cuerpo, 5.5, peso=0.4), R(cuerpo, NARANJA, peso=0.3, sp=8), T(cola, 5, peso=0.15),
                R(cola, ROJO, peso=0.1, sp=7), T(linea((44, -8), (44, 0)), 9, peso=0.03),
                T(arco_(70, 6, 12, 20, 110, 6), 3.6, peso=0.05), T(arco_(-8, 0, 30, 250, 110, 8), 3.4, peso=0.08)])


@lru_cache(maxsize=None)
def alga():
    return Dib([T(curva([(0, 0), (-16, -60), (14, -120), (-10, -190)], 8), 5.5, peso=0.25),
                T(curva([(30, 0), (44, -50), (20, -100)], 8), 5, peso=0.15)])


@lru_cache(maxsize=None)
def vapor(n=3, sep=120):
    """Líneas onduladas de calor que suben."""
    ops = []
    for i in range(n):
        x = (i - (n - 1) / 2) * sep
        P = ondas(0, 1, 0, 1, 1)
        ys = np.linspace(0, -520, 40)
        xs = x + 26 * np.sin(ys / 60 + i * 1.7)
        ops.append(T(np.stack([xs, ys], 1), 5, peso=0.7))
        ops.append(T(linea((xs[-1] - 20, ys[-1] + 26), (xs[-1], ys[-1]), (xs[-1] + 20, ys[-1] + 26)), 5, peso=0.08))
    return Dib(ops)


@lru_cache(maxsize=None)
def soplo():
    """Nubecita de aliento (la gota se va en él)."""
    circulos = [(-70, 10, 50, 30), (0, -30, 62, -8), (72, 0, 52, 30)]
    P = _contorno_nube(circulos, 54, -118, 120, (0, 10))
    return Dib([T(P, 5.0, peso=0.6), R(P, (222, 236, 248), peso=0.4, sp=10)])



# ------------------------------------------------------------------ objetos de la versión dinámica
@lru_cache(maxsize=None)
def planeta():
    r = 110
    ops = [T(circ(0, 0, r, a0=-0.7, vuelta=1.04, n=56), 6.0, peso=0.5),
           R(circ(0, 0, r, vuelta=1.0, n=48), AZUL, peso=0.5, sp=11)]
    conts = [[(-62, -48), (-22, -80), (12, -42), (-8, -6), (-48, 12), (-76, -22)],
             [(24, 18), (72, 8), (86, 48), (52, 84), (16, 58)], [(-52, 46), (-26, 40), (-14, 74), (-44, 88)]]
    for c in conts:
        P = curva(c, 6, True)
        ops += [R(P, VERDE, peso=0.15, sp=7, off=(2, -2)), T(np.vstack([P, P[:1]]), 4.0, peso=0.12)]
    return Dib(ops)


def _barra(p, q, w):
    p, q = np.array(p, float), np.array(q, float)
    d = q - p
    n = np.array([-d[1], d[0]])
    n = n / np.linalg.norm(n) * w
    return np.array([p + n, q + n, q - n, p - n, p + n])


@lru_cache(maxsize=None)
def tache():
    a, b = _barra((-58, -58), (58, 58), 12), _barra((58, -58), (-58, 58), 12)
    return Dib([T(a, 4.5, peso=0.25), R(a, ROJO, peso=0.15, sp=6), T(b, 4.5, peso=0.25), R(b, ROJO, peso=0.15, sp=6)])


@lru_cache(maxsize=None)
def flecha_ida():
    """Flecha roja hacia arriba (salir del planeta)."""
    cuerpo = _barra((0, 130), (0, -60), 11)
    punta = np.array([(-46, -50), (0, -130), (46, -50), (-46, -50)], float)
    return Dib([T(cuerpo, 4.5, peso=0.3), R(cuerpo, ROJO, peso=0.15, sp=6), T(punta, 4.5, peso=0.2),
                R(punta, ROJO, peso=0.15, sp=6)])


@lru_cache(maxsize=None)
def flecha_circ(r=120):
    """Flecha circular (dar vueltas / volver a empezar)."""
    arc = arco_(0, 0, r, -50, 225, 44)
    a = math.radians(225)
    tip = np.array([r * math.cos(a), r * math.sin(a)])
    tg = np.array([-math.sin(a), math.cos(a)])
    nr = np.array([math.cos(a), math.sin(a)])
    return Dib([T(arc, 6.5, peso=0.6),
                T(np.array([tip - tg * 30 + nr * 22, tip + tg * 8, tip - tg * 30 - nr * 22]), 6.5, peso=0.15)])


@lru_cache(maxsize=None)
def hoja_cal():
    P = np.array([(-50, -62), (50, -62), (50, 62), (-50, 62), (-50, -62)], float)
    banda = np.array([(-50, -62), (50, -62), (50, -30), (-50, -30)], float)
    return Dib([T(mano_poli(P, 2.0, 5), 5.0, peso=0.3), R(banda, ROJO, peso=0.15, sp=7, off=(1, 1)),
                T(linea((-30, 0), (30, 0)), 3.5, peso=0.05), T(linea((-30, 22), (30, 22)), 3.5, peso=0.05),
                T(linea((-30, 44), (10, 44)), 3.5, peso=0.05)])


@lru_cache(maxsize=None)
def reloj():
    ops = [T(circ(0, 0, 95, a0=-1.0, vuelta=1.04, n=44), 6.0, peso=0.5),
           R(circ(0, 0, 95, vuelta=1.0, n=40), HIELO, peso=0.4, sp=10)]
    for i in range(12):
        a = i * math.pi / 6
        ops.append(T(linea((78 * math.cos(a), 78 * math.sin(a)), (88 * math.cos(a), 88 * math.sin(a))), 4.0, peso=0.03))
    return Dib(ops)


@lru_cache(maxsize=None)
def charco():
    P = elip(0, 0, 150, 30, vuelta=1.03, n=36)
    return Dib([T(P, 5.0, peso=0.4), R(elip(0, 0, 150, 30, vuelta=1.0, n=32), AZUL_CL, peso=0.3, sp=9, ang=10)])


@lru_cache(maxsize=None)
def luna():
    fi = np.radians(np.linspace(100, 260, 20))
    ext = np.stack([60 * np.cos(fi), 60 * np.sin(fi)], 1)
    th = np.radians(np.linspace(237, 123, 20))
    inte = np.stack([28 + 70.5 * np.cos(th), 70.5 * np.sin(th)], 1)
    P = np.vstack([ext, inte, ext[:1]])
    return Dib([T(P, 5.5, peso=0.4), R(P, (238, 226, 160), peso=0.3, sp=8)])


@lru_cache(maxsize=None)
def chispa():
    ops = []
    for a, l in ((0, 34), (math.pi / 2, 34), (math.pi / 4, 20), (3 * math.pi / 4, 20)):
        ops.append(T(linea((-l * math.cos(a), -l * math.sin(a)), (l * math.cos(a), l * math.sin(a))), 4.5, peso=0.05))
    return Dib(ops)


# ------------------------------------------------------------------ formas que cambian de forma todo el tiempo
def nube_din(t):
    """Nube cuyos globos crecen y se encogen (su forma nunca se repite dentro de cada ciclo)."""
    w = B.OMEGA
    base = [(-190, 30, 85, 84), (-85, -35, 105, -8), (45, -55, 120, -8), (175, -5, 95, 50), (250, 55, 55, 80)]
    cs = []
    for i, (cx, cy, r, ym) in enumerate(base):
        k = 1 + 0.07 * math.sin(w * t * (1 + i % 2) + i * 1.3)
        cs.append((cx + 6 * math.sin(w * t * 2 + i), cy - (k - 1) * r * 0.5, r * k, ym))
    P = _contorno_nube(cs, 108, -258, 294, (20, 20))
    det = [arco_(-130 + 8 * math.sin(w * t), 20, 40, 200, 290, 10), arco_(30, -10 + 6 * math.sin(w * t * 2 + 1), 52, 210, 300, 10),
           arco_(190, 30 + 5 * math.sin(w * t + 2), 34, 200, 290, 10)]
    return Dib([T(P, 6.0, peso=1.0), R(P, AZUL_CL, peso=0.9, sp=12)] + [T(d, 3.6, peso=0.08) for d in det])


def sol_din(r, t):
    """Sol que gira y late: los rayos se alargan y se acortan, y el disco respira."""
    w = B.OMEGA
    rr = r * (1 + 0.035 * math.sin(2 * w * t))
    ops = [T(circ(0, 0, rr, a0=-1.2), 6.0, peso=0.4), R(circ(0, 0, rr, vuelta=1.0, n=40), AMARILLO, peso=0.5, sp=10)]
    for i in range(12):
        a = i * math.pi / 6 + 0.1 + B.GIRO_SOL * t
        r0 = rr * 1.28
        r1 = rr * (1.62 if i % 2 == 0 else 1.5) * (1 + 0.13 * math.sin(2 * w * t + i * 0.9))
        ops.append(T(linea((r0 * math.cos(a), r0 * math.sin(a)), (r1 * math.cos(a), r1 * math.sin(a))), 5.5, peso=0.05))
    return Dib(ops)
