# -*- coding: utf-8 -*-
"""Kit del estilo Vox: papel recortado, rotulación gruesa, marcador amarillo, anotaciones a mano y
PERSONAJES DIBUJADOS CUADRO A CUADRO (tablas de poses escritas a mano, no interpolaciones).

Todo se dibuja sobre el Lienzo (coordenadas locales; usar con lz.grupo). Los objetos de "papel" van en la capa 1
(sticker: borde crema + sombra); la rotulación y las anotaciones en la capa 2 (sin borde).

Personajes: `figura(lz, x, y, s, pose, traje, dir=1, obj=..., carga=...)` con `pose` = tupla de 11 valores
(bob, torso, cabeza, muslo_i, rodilla_i, muslo_d, rodilla_d, brazo_i, codo_i, brazo_d, codo_d); ángulos en grados
medidos desde la vertical hacia abajo, positivo = hacia adelante. Un brazo puede darse como ("ik", x, y): mano en
(x, y) relativo al hombro. El pie más bajo siempre se apoya en el suelo (y = 0). Ciclos ya escritos: CAMINAR (8
cuadros), PICAR (6), SUBIR (8), ARCO (7), IDLE (2), SEÑALAR (2). `cuadro(ciclo, t, fps=15)` elige el cuadro (baile
"en dos": 15 dibujos por segundo).
"""
import math

import numpy as np

from motor import (BLANCO, NEGRO, ancho_texto, clamp01, e_back, e_out, h01, lerp, prog, r1, rect_red, smooth)

# ------------------------------------------------------------------ paleta
PAPEL = (240, 231, 210)
TINTA = (38, 30, 27)
ROJO = (206, 66, 52)
NARANJA = (233, 140, 52)
AMARILLO = (250, 206, 66)
TEAL = (48, 138, 140)
AZUL = (54, 92, 150)
VERDE = (96, 140, 78)
VERDE_OSC = (62, 102, 66)
OCRE = (204, 152, 82)
TIERRA = (148, 102, 70)
TIERRA_OSC = (104, 70, 52)
ROCA = (150, 140, 132)
ROCA_OSC = (92, 84, 84)
PLATA = (216, 222, 228)
PLATA_OSC = (160, 170, 182)
MAR = (176, 205, 208)
ARENA = (232, 214, 170)
CREMA = (247, 241, 228)
ROSA = (226, 120, 110)
MORADO = (120, 84, 140)
PIELES = [(191, 128, 86), (163, 104, 70), (122, 80, 56), (212, 158, 112)]


def oscurecer(c, u):
    return tuple(int(v * (1 - u)) for v in c)


def aclarar(c, u):
    return tuple(int(v + (255 - v) * u) for v in c)


def mezcla(a, b, u):
    return tuple(int(x + (y - x) * u) for x, y in zip(a, b))


def _v(a):
    return np.asarray(a, float)


# ------------------------------------------------------------------ geometría de papel
def corte(pts, seed=0, amp=2.0, sub=2, cerrado=True):
    """Polígono 'cortado con tijera': cada arista se parte y se desvía un poco (determinista)."""
    P = _v(pts)
    n = len(P)
    out = []
    for i in range(n if cerrado else n - 1):
        a, b = P[i], P[(i + 1) % n]
        out.append(a)
        for k in range(1, sub):
            u = k / sub
            out.append(a + (b - a) * u + np.array([(h01(seed, i, k) - .5) * 2 * amp, (h01(seed, i, k + 7) - .5) * 2 * amp]))
    if not cerrado:
        out.append(P[-1])
    return np.array(out)


def capsula(p0, p1, w0, w1=None, n=7):
    """Polígono de una cápsula ahusada entre dos puntos (ancho w0 en p0, w1 en p1)."""
    p0, p1 = _v(p0), _v(p1)
    w1 = w0 if w1 is None else w1
    d = p1 - p0
    u = d / (np.hypot(*d) + 1e-9)
    nr = np.array([-u[1], u[0]])
    a = math.atan2(nr[1], nr[0])
    pts = [p0 + nr * w0 / 2]
    for k in range(n + 1):
        ang = a - k * math.pi / n
        pts.append(p1 + (w1 / 2) * np.array([math.cos(ang), math.sin(ang)]))
    for k in range(1, n):
        ang = a - math.pi - k * math.pi / n
        pts.append(p0 + (w0 / 2) * np.array([math.cos(ang), math.sin(ang)]))
    return np.array(pts)


def elipse_pts(cx, cy, rx, ry, rot=0.0, n=40):
    a = np.linspace(0, 2 * math.pi, n, endpoint=False)
    x, y = rx * np.cos(a), ry * np.sin(a)
    c, s = math.cos(rot), math.sin(rot)
    return np.stack([cx + x * c - y * s, cy + x * s + y * c], 1)


def poligono_reg(cx, cy, r, n, rot=0.0):
    a = rot + np.linspace(0, 2 * math.pi, n, endpoint=False)
    return np.stack([cx + r * np.cos(a), cy + r * np.sin(a)], 1)


def rot_pts(P, a, c=(0, 0)):
    P = _v(P) - _v(c)
    co, si = math.cos(a), math.sin(a)
    return np.stack([P[:, 0] * co - P[:, 1] * si, P[:, 0] * si + P[:, 1] * co], 1) + _v(c)


def sit(P, dx=0, dy=0, s=1.0):
    return _v(P) * s + np.array([dx, dy])


# ------------------------------------------------------------------ texturas de papel
def semitono(lz, poligono, color, esp=16.0, r=3.0, ang=0.6, alfa=1.0, capa=None):
    """Trama de puntos (medio tono) recortada al polígono."""
    P = _v(poligono)
    x0, y0 = P.min(0)
    x1, y1 = P.max(0)
    c, s = math.cos(ang), math.sin(ang)
    R = math.hypot(x1 - x0, y1 - y0) / 2
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    n = int(R / esp) + 1
    ii, jj = np.meshgrid(np.arange(-n, n + 1), np.arange(-n, n + 1))
    gx, gy = ii * esp + (jj % 2) * esp / 2, jj * esp * 0.87
    px, py = cx + gx * c - gy * s, cy + gx * s + gy * c
    ok = (px > x0 - r) & (px < x1 + r) & (py > y0 - r) & (py < y1 + r)
    pts = np.stack([px[ok], py[ok]], 1)
    if len(pts) == 0 or len(pts) > 1600:
        return
    with lz.recorte(poligono):
        lz.puntos(pts, r, color if alfa >= 1 else color, capa=capa)


def rayado(lz, poligono, color, esp=14.0, ancho=2.0, ang=0.8, capa=None):
    """Líneas paralelas (sombreado de grabado) recortadas al polígono."""
    P = _v(poligono)
    x0, y0 = P.min(0)
    x1, y1 = P.max(0)
    R = math.hypot(x1 - x0, y1 - y0) / 2
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    n = int(R / esp) + 1
    d = np.array([math.cos(ang), math.sin(ang)])
    nr = np.array([-d[1], d[0]])
    if n > 90:
        return
    with lz.recorte(poligono):
        for k in range(-n, n + 1):
            c = np.array([cx, cy]) + nr * k * esp
            lz.trazo(np.array([c - d * R, c + d * R]), color, ancho, afinar=False, temblor=0.0, capa=capa, paso=60.0)


# ------------------------------------------------------------------ rotulación
def rotulo(lz, txt, x, y, px, color=BLANCO, fuente="vox_x", k=1.0, rot=0.0, ancla=(0.5, 0.5), alfa=1.0,
           sombra=0.35, capa=2):
    """Texto grueso sin contorno, con sombra suave (rotulación tipo documental)."""
    if k <= 0.01 or alfa <= 0.01:
        return
    if sombra > 0:
        lz.texto(txt, x + px * 0.035, y + px * 0.05, px, fuente, color=(20, 14, 10), borde=None, k=k, ancla=ancla,
                 alfa=alfa * sombra, capa=capa, temblor=0.0, rot=rot)
    lz.texto(txt, x, y, px, fuente, color=color, borde=None, k=k, ancla=ancla, alfa=alfa, capa=capa, temblor=0.0,
             rot=rot)


def marcador(lz, x, y, w, h, frac, color=AMARILLO, seed=0, alfa=0.92, capa=2):
    """Barrido de marcador amarillo (x, y = centro izquierdo; w ancho total; frac 0..1 = avance)."""
    if frac <= 0.01:
        return
    L = w * clamp01(frac)
    n = max(3, int(L / 40))
    xs = np.linspace(0, L, n + 1)
    top = [(xs[i] + (h * 0.22 if i == 0 else 0), -h / 2 + (h01(seed, i) - .5) * h * 0.14) for i in range(n + 1)]
    bot = [(xs[i] - (h * 0.18 if i == n else 0) - (h * 0.18 if i == 0 else 0), h / 2 + (h01(seed, i + 40) - .5) * h * 0.14)
           for i in range(n, -1, -1)]
    with lz.capa(capa):
        with lz.grupo(x, y):
            lz.relleno(np.array(top + bot), color, seed=seed, temblor=0.4, alfa=alfa)


def pastilla(lz, x, y, txt, px=40, k=1.0, fondo=CREMA, color=TINTA, fuente="vox_b", alfa=1.0, rot=0.0, capa=2,
             sombra=True):
    """Etiqueta en cápsula (fondo claro, texto oscuro)."""
    if k <= 0.01 or alfa <= 0.01:
        return
    w = ancho_texto(txt, fuente, px) + px * 1.2
    h = px * 1.6
    with lz.capa(capa):
        with lz.grupo(x, y, k, rot):
            if sombra:
                lz.relleno(rect_red(-w / 2 + 3, -h / 2 + 5, w, h, h / 2), (30, 20, 14), alfa=0.28 * alfa)
            lz.relleno(rect_red(-w / 2, -h / 2, w, h, h / 2), fondo, alfa=alfa)
            lz.texto(txt, 0, px * 0.04, px, fuente, color=color, borde=None, alfa=alfa, temblor=0.0)


def cinta(lz, x, y, w, h, color=AMARILLO, rot=0.0, seed=0, alfa=0.85, capa=2):
    """Cinta adhesiva semitransparente con bordes dentados."""
    with lz.capa(capa):
        with lz.grupo(x, y, 1.0, rot):
            n = 5
            arriba = [(-w / 2 + (h01(seed, 1, i) - .5) * 4, -h / 2 + (0 if i % 2 else 3)) for i in range(n)]
            abajo = [(w / 2 + (h01(seed, 2, i) - .5) * 4, -h / 2 + i * h / (n - 1)) for i in range(n)]
            P = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2 + 5, 0), (w / 2, h / 2), (-w / 2, h / 2), (-w / 2 - 5, 0)]
            lz.relleno(np.array(P), color, seed=seed, temblor=0.2, alfa=alfa)


# ------------------------------------------------------------------ anotaciones a mano (se dibujan con el tiempo)
def _parcial(pts, frac):
    pts = _v(pts)
    seg = np.hypot(*np.diff(pts, axis=0).T)
    d = np.concatenate([[0.0], np.cumsum(seg)])
    L = d[-1] * clamp01(frac)
    k = int(np.searchsorted(d, L))
    sub = list(pts[:k])
    if 0 < k < len(pts):
        u = (L - d[k - 1]) / max(1e-9, d[k] - d[k - 1])
        sub.append(pts[k - 1] + (pts[k] - pts[k - 1]) * u)
    return np.array(sub)


def trazo_mano(lz, pts, frac, color=ROJO, ancho=7.0, seed=0, capa=2):
    """Trazo dibujado progresivamente (como a marcador); re-tiembla a 10 fps."""
    if frac <= 0.005:
        return
    s = _parcial(pts, frac)
    if len(s) >= 2:
        lz.trazo(s, color, ancho, seed=seed, temblor=1.6, capa=capa, afinar=False)


def circulo_mano(lz, x, y, rx, ry, frac, color=ROJO, ancho=7.0, seed=0, capa=2):
    a = np.linspace(-1.2, -1.2 + 2 * math.pi * 1.1, 70)
    r = 1 + 0.06 * (a + 1.2) / (2 * math.pi)
    pts = np.stack([x + rx * r * np.cos(a), y + ry * r * np.sin(a)], 1)
    trazo_mano(lz, pts, frac, color, ancho, seed, capa)


def subrayado(lz, x0, x1, y, frac, color=ROJO, ancho=7.0, seed=0, capa=2):
    n = 6
    xs = np.linspace(x0, x1, n)
    pts = np.stack([xs, y + np.array([math.sin(i * 1.9 + seed) * 3 - i * 0.6 for i in range(n)])], 1)
    trazo_mano(lz, pts, frac, color, ancho, seed, capa)


def flecha_mano(lz, p0, p1, frac, color=ROJO, ancho=7.0, curva=0.25, seed=0, capa=2):
    p0, p1 = _v(p0), _v(p1)
    d = p1 - p0
    nr = np.array([-d[1], d[0]])
    m = (p0 + p1) / 2 + nr * curva
    u = np.linspace(0, 1, 30)[:, None]
    pts = (1 - u) ** 2 * p0 + 2 * (1 - u) * u * m + u ** 2 * p1
    trazo_mano(lz, pts, min(1.0, frac / 0.85), color, ancho, seed, capa)
    if frac > 0.85:
        t = pts[-1] - pts[-4]
        a = math.atan2(t[1], t[0])
        L = ancho * 3.4
        for s in (-0.5, 0.5):
            lz.trazo(np.array([pts[-1], pts[-1] - L * np.array([math.cos(a + s), math.sin(a + s)])]), color, ancho,
                     seed=seed + 5, temblor=1.0, capa=capa, afinar=False)


# ------------------------------------------------------------------ figuras cuadro a cuadro
MUSLO, PANT, TORSO, BRAZO, ANTEB, CAB, CUELLO = 68.0, 66.0, 92.0, 52.0, 50.0, 27.0, 10.0

# --- tablas de poses (una por cuadro; escritas a mano) -------------------------------------------------------
# pierna (muslo, rodilla) por fase: contacto, bajada, apoyo, impulso, despegue, elevación, paso, adelanto
_CAM = [(28, -6), (20, -14), (6, -12), (-8, -10), (-22, -26), (-14, -58), (6, -74), (24, -40)]
_ARM_CAM = [(-22, 14), (-14, 16), (-2, 18), (10, 20), (22, 22), (14, 20), (2, 18), (-12, 16)]   # (brazo, codo) lado de la pierna


def _pose_caminar(f, torso=5.0):
    r, l = _CAM[f % 8], _CAM[(f + 4) % 8]
    ar, al = _ARM_CAM[f % 8], _ARM_CAM[(f + 4) % 8]
    # el brazo del mismo lado que la pierna adelantada va hacia atrás
    return (0, torso, 2, l[0], l[1], r[0], r[1], ar[0], ar[1], al[0], al[1])


CAMINAR = [_pose_caminar(f) for f in range(8)]

# recolectar mineral con pico / barreta: (torso, brazos i/d, codos)
_PICAR_T = [(-8, 150, 20, 160, 12), (-12, 168, 10, 176, 6), (10, 112, 30, 120, 24), (32, 40, 20, 46, 14),
            (24, 62, 10, 68, 6), (8, 104, 20, 110, 20)]
PICAR = [(0, t, 0, -6, -8, 14, -12, a1, e1, a2, e2) for (t, a1, e1, a2, e2) in _PICAR_T]

# subir por escala con carga (cuerpo encorvado, rodillas altas)
_SUB = [(20, -20), (38, -55), (58, -92), (42, -70), (16, -30), (4, -14), (-4, -8), (6, -10)]
_ARM_SUB = [(100, 20), (120, 25), (140, 25), (120, 20), (90, 15), (70, 10), (60, 10), (80, 15)]
SUBIR = [(0, 24, 8, _SUB[(f + 4) % 8][0], _SUB[(f + 4) % 8][1], _SUB[f][0], _SUB[f][1],
          _ARM_SUB[(f + 4) % 8][0], _ARM_SUB[(f + 4) % 8][1], _ARM_SUB[f][0], _ARM_SUB[f][1]) for f in range(8)]

# arquero: brazo izquierdo estirado (ik), derecho jala la cuerda
ARCO = [(0, 4, 0, -14, -6, 12, -8, ("ik", 62, -6), None, ("ik", 30, -8), None),
        (0, 2, 0, -14, -6, 12, -8, ("ik", 66, -8), None, ("ik", 12, -6), None),
        (0, 0, 0, -14, -6, 12, -8, ("ik", 70, -8), None, ("ik", -6, -6), None),
        (0, -2, 0, -14, -6, 12, -8, ("ik", 72, -8), None, ("ik", -26, -4), None),
        (0, -2, 0, -14, -6, 12, -8, ("ik", 72, -8), None, ("ik", -34, -4), None),
        (0, 0, 0, -14, -6, 12, -8, ("ik", 70, -6), None, ("ik", 30, 4), None),
        (0, 3, 0, -14, -6, 12, -8, ("ik", 64, 0), None, ("ik", 36, 14), None)]

IDLE = [(0, 2, 0, -4, -4, 6, -4, 8, 14, -6, 14), (1, 2, 1, -4, -4, 6, -4, 10, 16, -4, 16)]
SEÑALAR = [(0, 2, 0, -6, -4, 8, -4, ("ik", 40, -8), None, -6, 14), (0, 2, 0, -6, -4, 8, -4, ("ik", 44, -10), None, -4, 16)]


def cuadro(ciclo, t, fps=15.0, t0=0.0):
    """Índice del dibujo en el ciclo: 15 dibujos por segundo (animación 'en dos')."""
    return int(math.floor((t - t0) * fps + 1e-6)) % len(ciclo)


def pose_de(ciclo, t, fps=15.0, t0=0.0):
    return ciclo[cuadro(ciclo, t, fps, t0)]


def _ik(S, T, l1, l2, signo=1):
    """Codo de una cadena de 2 huesos de S a T (mano). signo elige hacia dónde dobla."""
    d = T - S
    L = float(np.hypot(*d))
    L = min(max(L, 1e-3), l1 + l2 - 0.5)
    a = math.atan2(d[1], d[0])
    cosb = (l1 * l1 + L * L - l2 * l2) / (2 * l1 * L)
    b = math.acos(max(-1, min(1, cosb)))
    codo = S + l1 * np.array([math.cos(a + signo * b), math.sin(a + signo * b)])
    mano = S + (T - S) / (np.hypot(*(T - S)) + 1e-9) * L
    return codo, mano


def _vec(ang_deg, d):
    a = math.radians(ang_deg)
    return np.array([math.sin(a) * d, math.cos(a)  * d])


TRAJES = {
    "tolosa": dict(piel=PIELES[3], ropa=(150, 40, 44), ropa2=(60, 40, 40), pant=(52, 44, 52), bota=(64, 40, 30),
                   sombrero="ala", sombrero_col=(36, 32, 40), pluma=ROJO, pelo=(70, 44, 30), falda=34, barba=True),
    "soldado": dict(piel=PIELES[3], ropa=(120, 100, 70), ropa2=(80, 70, 60), pant=(70, 62, 52), bota=(64, 44, 34),
                    sombrero="morrion", sombrero_col=(150, 150, 156), pelo=(60, 40, 30), falda=26),
    "indigena": dict(piel=PIELES[1], ropa=(242, 236, 220), ropa2=(200, 60, 50), pant=(242, 236, 220), bota=None,
                     sombrero="banda", sombrero_col=ROJO, pelo=(28, 24, 26), falda=30),
    "minero": dict(piel=PIELES[1], ropa=(226, 214, 186), ropa2=(180, 70, 50), pant=(150, 120, 90), bota=None,
                   sombrero="paño", sombrero_col=(190, 66, 50), pelo=(28, 24, 26), falda=22),
    "cargador": dict(piel=PIELES[2], ropa=(214, 196, 160), ropa2=(150, 110, 70), pant=(214, 196, 160), bota=None,
                     sombrero="paño", sombrero_col=(160, 120, 80), pelo=(26, 22, 24), falda=20),
    "africano": dict(piel=PIELES[2], ropa=(196, 180, 150), ropa2=(120, 90, 60), pant=(120, 100, 82), bota=None,
                     sombrero=None, sombrero_col=None, pelo=(22, 18, 20), falda=0),
    "guachichil": dict(piel=PIELES[1], ropa=(186, 74, 58), ropa2=(240, 230, 200), pant=PIELES[1], bota=None,
                       sombrero="pintura", sombrero_col=ROJO, pelo=(24, 20, 22), falda=22, pintura=True),
    "fraile": dict(piel=PIELES[3], ropa=(126, 88, 60), ropa2=(230, 224, 210), pant=(126, 88, 60), bota=None,
                   sombrero="capucha", sombrero_col=(126, 88, 60), pelo=(60, 40, 30), falda=66),
    "caldera": dict(piel=PIELES[0], ropa=(70, 100, 120), ropa2=(200, 170, 90), pant=(60, 60, 70), bota=(70, 50, 36),
                    sombrero="ala", sombrero_col=(170, 130, 70), pluma=None, pelo=(40, 28, 24), falda=30),
    "arriero": dict(piel=PIELES[0], ropa=(190, 170, 130), ropa2=(70, 100, 130), pant=(90, 80, 70), bota=None,
                    sombrero="ala", sombrero_col=(214, 190, 130), pluma=None, pelo=(40, 28, 24), falda=22),
    "mujer": dict(piel=PIELES[1], ropa=(70, 110, 130), ropa2=(230, 200, 90), pant=(70, 110, 130), bota=None,
                  sombrero="trenza", sombrero_col=(24, 20, 22), pelo=(24, 20, 22), falda=76),
    "hoy": dict(piel=PIELES[0], ropa=(226, 90, 90), ropa2=(60, 60, 80), pant=(60, 70, 110), bota=(230, 230, 230),
                sombrero=None, sombrero_col=None, pelo=(50, 36, 30), falda=0),
}


def figura(lz, x, y, s, pose, traje, dir=1, obj=(), carga=None, seed=0, alfa=1.0, capa=None):
    """Dibuja un personaje (origen en los pies, altura ~ 330 * s). Mira a la derecha (dir=1) o a la izquierda (-1)."""
    if isinstance(traje, str):
        traje = TRAJES[traje]
    bob, tor, cab, tl, kl, tr, kr, al, el, ar, er = pose
    piel, ropa, ropa2, pant = traje["piel"], traje["ropa"], traje["ropa2"], traje["pant"]
    lejos = 0.2
    with lz.grupo(x, y, s * dir, 0.0, sy=s):
        def L(pts, col, sd, tem=0.5):
            lz.relleno(pts, col, seed=seed + sd, temblor=tem, capa=capa, alfa=alfa)

        # cadera: apoya el pie más bajo en el suelo
        def cadena(t1, k):
            r1_ = _vec(t1, MUSLO)
            r2_ = _vec(t1 + k, PANT)
            return r1_, r1_ + r2_

        rl, fl = cadena(tl, kl)
        rr, fr = cadena(tr, kr)
        cad = np.array([0.0, -max(fl[1], fr[1]) + bob])
        ta = math.radians(tor)
        hom = cad + np.array([math.sin(ta) * TORSO, -math.cos(ta) * TORSO])
        cen = hom + np.array([math.sin(ta + math.radians(cab)) * (CUELLO + CAB), -math.cos(ta + math.radians(cab)) * (CUELLO + CAB)])

        def pierna(t1, k, col, cbota, sd, osc):
            a = cad + _vec(t1, MUSLO)
            b = a + _vec(t1 + k, PANT)
            c = mezcla(col, (0, 0, 0), osc)
            L(capsula(cad, a, 30, 24), c, sd)
            L(capsula(a, b, 24, 17), c, sd + 1)
            if cbota is not None:
                L(elipse_pts(b[0] + 9, b[1] - 6, 22, 11), mezcla(cbota, (0, 0, 0), osc), sd + 2)
            else:
                L(elipse_pts(b[0] + 8, b[1] - 5, 17, 8), mezcla(piel, (0, 0, 0), osc), sd + 2)
            return b

        def brazo(a1, e1, col, sd, osc, mano_col=None):
            if isinstance(a1, tuple):
                T = hom + np.array([a1[1], a1[2]])
                codo, mano = _ik(hom, T, BRAZO, ANTEB, -1 if a1[1] > 0 else 1)
                v = mano - codo
                fa = math.degrees(math.atan2(v[0], v[1]))
            else:
                codo = hom + _vec(a1, BRAZO)
                mano = codo + _vec(a1 + e1, ANTEB)
                fa = a1 + e1
            c = mezcla(col, (0, 0, 0), osc)
            L(capsula(hom, codo, 22, 17), c, sd)
            L(capsula(codo, mano, 17, 14), mezcla(piel, (0, 0, 0), osc), sd + 1)
            L(elipse_pts(mano[0], mano[1], 9, 9), mezcla(piel, (0, 0, 0), osc), sd + 2)
            return mano, fa

        # capa lejana: brazo izquierdo y pierna izquierda
        mano_i, fa_i = brazo(al, el, ropa, 10, lejos)
        pierna(tl, kl, pant, traje["bota"], 20, lejos)
        # carga a la espalda (detrás del torso)
        if carga:
            _carga(lz, carga, hom, ta, s, seed, capa, L)
        # torso + prenda
        L(capsula(cad, hom, 44, 40), ropa, 30)
        fl_ = traje.get("falda", 0)
        if fl_ > 0:
            base = cad + np.array([0, fl_])
            L(np.array([cad + [-27, -6], cad + [27, -6], base + [31 + fl_ * 0.12, 0], base + [-31 - fl_ * 0.12, 0]]), ropa, 33)
        if traje.get("ropa2") and fl_ > 0:
            L(capsula(cad + [-26, -10], cad + [26, -10], 9), ropa2, 34)
        pierna(tr, kr, pant, traje["bota"], 40, 0.0)
        mano_d, fa_d = brazo(ar, er, ropa, 50, 0.0)
        # cabeza
        with lz.grupo(cen[0], cen[1], 1.0, math.radians(tor + cab) * 0.6):
            L(capsula([0, CAB * 0.7], [0, CUELLO + 8], 15, 13), piel, 60)
            L(elipse_pts(0, 0, CAB, CAB * 1.05), piel, 61)
            L(elipse_pts(CAB * 0.42, -CAB * 0.05, 3.2, 3.6), TINTA, 62, 0.0)
            _sombrero(lz, traje, seed, capa, L)
        for o in obj:
            if o[0] == "arco":       # ("arco", escala): arco en la mano izquierda, cuerda hasta la derecha
                arco(lz, mano_i, mano_d, o[1] if len(o) > 1 else 1.0, seed, True, capa)
                continue
            m, fa = (mano_d, fa_d) if o[0] == "d" else (mano_i, fa_i)
            _objeto(lz, o, m, fa, seed, capa, L)
    return None


def _carga(lz, carga, hom, ta, s, seed, capa, L):
    tipo = carga[0]
    if tipo == "tenate":       # cesto de mineral a la espalda, con mecapal
        esc = carga[1] if len(carga) > 1 else 1.0
        c = hom + np.array([-38 * esc, 30 * esc])
        with lz.grupo(c[0], c[1], esc, ta * 0.9):
            cesto = np.array([[-34, -44], [34, -44], [42, 40], [-42, 40]])
            L(cesto, (170, 120, 70), 70, 0.4)
            L(np.array([[-34, -44], [34, -44], [36, -30], [-36, -30]]), (120, 80, 50), 71)
            for i in range(6):
                px, py = -26 + (i % 3) * 24, -58 + (i // 3) * -14 - (i % 2) * 6
                L(poligono_reg(px, py, 16 + (i * 5) % 7, 5, i), ROCA if i % 2 else ROCA_OSC, 72 + i)
            L(poligono_reg(-6, -64, 7, 5, 0.3), PLATA, 90)
            L(capsula([26, -30], [70, -110], 6, 6), (110, 80, 50), 91)
    elif tipo == "bulto":
        c = hom + np.array([-30, 24])
        L(elipse_pts(c[0], c[1], 44, 36), (200, 170, 120), 70)
        L(capsula(c + [-30, 0], c + [30, 4], 6), (120, 90, 60), 71)


def _sombrero(lz, tr, seed, capa, L):
    k = tr.get("sombrero")
    col = tr.get("sombrero_col")
    pelo = tr.get("pelo", (30, 24, 24))
    if k in (None, "ala", "morrion", "trenza", "paño", "banda", "pintura"):
        if k != "pintura":
            L(np.array([[-CAB, -CAB * 0.1], [-CAB * 0.9, -CAB * 0.9], [0, -CAB * 1.12], [CAB * 0.8, -CAB * 0.85],
                        [CAB * 0.95, -CAB * 0.3], [CAB * 0.3, -CAB * 0.55], [-CAB * 0.4, -CAB * 0.4]]), pelo, 63, 0.3)
    if tr.get("barba"):
        L(np.array([[CAB * 0.3, CAB * 0.4], [CAB * 0.95, CAB * 0.2], [CAB * 0.85, CAB * 0.95], [0, CAB * 0.9]]), (70, 44, 30), 64)
    if k == "ala":
        L(elipse_pts(0, -CAB * 0.72, CAB * 1.75, CAB * 0.3, -0.05), col, 65)
        L(np.array([[-CAB * 0.85, -CAB * 0.75], [CAB * 0.85, -CAB * 0.75], [CAB * 0.6, -CAB * 1.7], [-CAB * 0.6, -CAB * 1.7]]), col, 66)
        if tr.get("pluma"):
            L(capsula([-CAB * 0.6, -CAB * 1.5], [-CAB * 1.8, -CAB * 2.3], 8, 3), tr["pluma"], 67)
    elif k == "morrion":
        L(np.array([[-CAB * 1.05, -CAB * 0.45], [-CAB * 0.9, -CAB * 1.2], [0, -CAB * 1.55], [CAB * 0.9, -CAB * 1.2], [CAB * 1.05, -CAB * 0.5],
                    [CAB * 1.6, -CAB * 0.35], [-CAB * 1.6, -CAB * 0.35]]), col, 65)
        L(capsula([0, -CAB * 1.5], [0, -CAB * 1.9], 8, 4), (170, 60, 50), 66)
    elif k == "banda":
        L(capsula([-CAB, -CAB * 0.42], [CAB, -CAB * 0.42], 9), col, 65)
    elif k == "pintura":
        L(np.array([[-CAB * 0.98, -CAB * 0.2], [-CAB * 0.9, -CAB * 0.85], [0, -CAB * 1.06], [CAB * 0.9, -CAB * 0.85],
                    [CAB * 0.98, -CAB * 0.25], [0, -CAB * 0.2]]), col, 65)
        L(capsula([-CAB * 0.3, -CAB * 1.0], [-CAB * 0.9, -CAB * 1.8], 6, 3), (90, 60, 40), 66)
        L(capsula([0.2 * CAB, -CAB * 1.05], [0.2 * CAB, -CAB * 1.9], 6, 3), (90, 60, 40), 67)
    elif k == "paño":
        L(capsula([-CAB * 0.98, -CAB * 0.5], [CAB * 0.98, -CAB * 0.55], 13), col, 65)
        L(np.array([[-CAB, -CAB * 0.5], [-CAB * 1.6, -CAB * 0.1], [-CAB * 1.5, CAB * 0.3], [-CAB * 0.9, -CAB * 0.1]]), col, 66)
    elif k == "capucha":
        L(np.array([[-CAB * 1.35, CAB * 0.8], [-CAB * 1.2, -CAB * 0.8], [0, -CAB * 1.5], [CAB * 0.4, -CAB * 1.0], [CAB * 0.2, -CAB * 0.2],
                    [-CAB * 0.5, CAB * 0.1], [-CAB * 0.6, CAB * 1.0]]), col, 65)
    elif k == "trenza":
        L(capsula([-CAB * 0.9, -CAB * 0.2], [-CAB * 1.5, CAB * 1.7], 12, 8), col, 65)


def _objeto(lz, o, mano, fa, seed, capa, L):
    """o = (lado, tipo, desvío_grados, escala). El objeto sigue la dirección del antebrazo (fa)."""
    _, tipo, ang, esc = o[:4]
    with lz.grupo(mano[0], mano[1], esc, math.radians(-fa + ang)):
        if tipo == "barreta":        # barra de hierro con punta
            L(capsula([0, -70], [0, 100], 8, 8), ROCA_OSC, 100)
            L(np.array([[-9, 100], [9, 100], [0, 130]]), (70, 64, 66), 101)
            L(capsula([0, -70], [0, -90], 12, 10), TIERRA_OSC, 102)
        elif tipo == "pico":
            L(capsula([0, -60], [0, 60], 9, 9), (130, 96, 64), 100)
            L(np.array([[-52, -60], [52, -66], [46, -48], [0, -54], [-46, -46]]), ROCA_OSC, 101)
        elif tipo == "vela":
            L(rect_red(-6, -6, 12, 34, 3), (250, 244, 224), 100)
            L(np.array([[0, -34], [9, -14], [0, -8], [-9, -14]]), NARANJA, 101, 0.0)
            L(np.array([[0, -26], [4, -14], [0, -10], [-4, -14]]), AMARILLO, 102, 0.0)
        elif tipo == "bolsa":
            L(elipse_pts(0, 30, 30, 34), (206, 180, 130), 100)
            L(np.array([[-10, 4], [10, 4], [14, -6], [-14, -6]]), (150, 110, 70), 101)
        elif tipo == "lanza":
            L(capsula([0, -190], [0, 90], 6, 6), (130, 96, 64), 100)
            L(np.array([[-8, -190], [8, -190], [0, -230]]), PLATA, 101)
        elif tipo == "cruz":
            L(capsula([0, -70], [0, 30], 8, 8), (120, 84, 56), 100)
            L(capsula([-26, -48], [26, -48], 8, 8), (120, 84, 56), 101)
        elif tipo == "rollo":
            L(rect_red(-8, -34, 16, 68, 6), (236, 226, 196), 100)
            L(capsula([-8, -30], [8, -30], 5), ROJO, 101)
        elif tipo == "maiz":
            L(elipse_pts(0, 0, 10, 32), AMARILLO, 100)
            L(np.array([[-2, -28], [-16, 10], [0, 34]]), VERDE, 101)
        elif tipo == "arco":         # extra: cuerda tensión hacia la otra mano (posición mano_d en local)
            pass
    return None


def arco(lz, mano_i, mano_d, s, seed=0, flecha=True, capa=None):
    """Arco con cuerda estirada hasta mano_d (coordenadas locales de la figura)."""
    top, bot = mano_i + np.array([-6, -95]) * s, mano_i + np.array([-6, 95]) * s
    curva = np.array([top, mano_i + np.array([8, -50]) * s, mano_i + np.array([16, 0]) * s,
                      mano_i + np.array([8, 50]) * s, bot])
    lz.trazo(curva, (110, 76, 50), 9, seed=seed, temblor=0.0, afinar=False, capa=capa)
    lz.trazo(np.array([top, mano_d, bot]), (60, 46, 36), 3.0, seed=seed, temblor=0.0, afinar=False, capa=capa)
    if flecha:
        lz.trazo(np.array([mano_d, mano_i + np.array([64, 0]) * s]), (120, 90, 60), 5, seed=seed, temblor=0.0,
                 afinar=False, capa=capa)
        p = mano_i + np.array([64, 0]) * s
        lz.relleno(np.array([p + [0, -7], p + [24, 0], p + [0, 7]]), PLATA_OSC, temblor=0.0, capa=capa)


def bailar_idle(t):
    return IDLE[int(t * 2.5) % 2]


# ------------------------------------------------------------------ mula (cuatro patas, ciclo de 8 cuadros)
_PATA = [(18, -4), (10, -8), (0, -6), (-10, -6), (-16, -18), (-6, -50), (8, -46), (20, -22)]
_DESF = dict(tras_cerca=0, del_cerca=2, tras_lejos=4, del_lejos=6)


def mula(lz, x, y, s, f, dir=1, carga="barras", seed=0, alfa=1.0, cuello=0.0, capa=None, color=(150, 118, 92)):
    """Mula con carga. f = índice del cuadro (0..7). Origen: bajo el centro del cuerpo. Altura ~ 210 * s."""
    oscuro = mezcla(color, (0, 0, 0), 0.22)
    with lz.grupo(x, y, s * dir, 0.0, sy=s):
        def L(pts, col, sd):
            lz.relleno(pts, col, seed=seed + sd, temblor=0.4, capa=capa, alfa=alfa)

        def pata(base, key, col, sd, adelante):
            a1, k = _PATA[(f + _DESF[key]) % 8]
            m = base + _vec(a1 * 0.9, 74)
            p = m + _vec(a1 * 0.9 + k * (0.8 if adelante else -0.5), 78)
            L(capsula(base, m, 26, 17), col, sd)
            L(capsula(m, p, 17, 12), col, sd + 1)
            L(np.array([[p[0] - 8, p[1] - 3], [p[0] + 12, p[1] - 3], [p[0] + 12, p[1] + 7], [p[0] - 8, p[1] + 7]]), (50, 40, 36), sd + 2)

        bal = [0, 2, 3, 2, 0, -1, -2, -1][f % 8]
        cu = np.array([0.0, -150.0 + bal])
        pata(np.array([-70.0, -122 + bal]), "tras_lejos", oscuro, 10, False)
        pata(np.array([66.0, -126 + bal]), "del_lejos", oscuro, 20, True)
        # cuerpo
        L(elipse_pts(0, -142 + bal, 108, 56), color, 30)
        L(elipse_pts(0, -128 + bal, 86, 34), aclarar(color, 0.28), 31)
        # cuello y cabeza
        L(capsula([70, -168 + bal], [124, -222 + bal + cuello], 44, 30), color, 40)
        L(capsula([120, -226 + bal + cuello], [176, -204 + bal + cuello], 30, 22), color, 41)
        L(elipse_pts(178, -204 + bal + cuello, 12, 13), (90, 72, 66), 42)
        L(capsula([116, -240 + bal + cuello], [104, -290 + bal + cuello], 14, 6), color, 43)
        L(capsula([128, -240 + bal + cuello], [128, -292 + bal + cuello], 13, 6), oscuro, 44)
        L(elipse_pts(146, -222 + bal + cuello, 3.5, 3.5), TINTA, 45)
        L(np.array([[70, -186 + bal], [104, -230 + bal + cuello], [86, -178 + bal]]), (70, 52, 44), 46)   # crin
        # cola
        L(capsula([-104, -156 + bal], [-128, -104 + bal + [0, 6, 10, 6, 0, -4, -6, -4][f % 8]], 12, 6), (70, 52, 44), 47)
        pata(np.array([-68.0, -118 + bal]), "tras_cerca", color, 50, False)
        pata(np.array([70.0, -124 + bal]), "del_cerca", color, 60, True)
        # albarda + carga
        L(np.array([[-72, -190 + bal], [72, -190 + bal], [80, -152 + bal], [-80, -152 + bal]]), (176, 60, 60), 70)
        L(np.array([[-72, -178 + bal], [72, -178 + bal], [76, -166 + bal], [-76, -166 + bal]]), (232, 190, 80), 71)
        if carga == "barras":
            for i, dx in enumerate((-40, 40)):
                L(np.array([[dx - 34, -256 + bal], [dx + 34, -256 + bal], [dx + 40, -190 + bal], [dx - 40, -190 + bal]]), PLATA, 72 + i)
                L(np.array([[dx - 34, -256 + bal], [dx + 34, -256 + bal], [dx + 30, -246 + bal], [dx - 30, -246 + bal]]), aclarar(PLATA, 0.5), 74 + i)
        elif carga == "costales":
            for i, dx in enumerate((-40, 40)):
                L(elipse_pts(dx, -222 + bal, 42, 36), (206, 180, 130), 72 + i)
                L(capsula([dx - 26, -252 + bal], [dx + 26, -252 + bal], 8), (140, 100, 64), 74 + i)
        elif carga == "agua":
            L(elipse_pts(0, -218 + bal, 56, 34), (110, 84, 60), 72)
    return None


def catmull(P, n=8, cerrado=False):
    from motor import catmull as _c
    return _c(P, n, cerrado)
