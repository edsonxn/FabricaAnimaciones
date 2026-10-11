# -*- coding: utf-8 -*-
"""Panorama de Teotihuacán (vista lateral a lo largo de la Calzada de los Muertos), estilo Kurzgesagt.
Coordenadas del mundo: x a lo largo de la calzada (px), y hacia abajo, suelo en y = 0.
Estado `est` (todo continuo): hora (0 noche, 1 amanecer, 2 día, 3 ocaso, 4 noche), fuego, ruina, gente, luces.
Cámara: (cx, cy, z): el punto del mundo (cx, cy) cae en (960, 720) de la pantalla con zoom z."""
import math

import numpy as np

from motor import (W, H, prog, lerp, smooth, e_inout, e_out, circulo, elipse, rect_red, blob, ruido1, h01)
import plano as P

# ---- posiciones de los edificios (mundo)
X_CIUDADELA = -1500.0
X_SOL = 1300.0
X_LUNA = 3600.0
SUELO_Y = 0.0
GX, GY = 960.0, 720.0

# ---- paleta
PIEDRA = (226, 150, 104)        # cara iluminada
PIEDRA_S = (168, 100, 104)      # cara en sombra
PIEDRA_C = (255, 196, 132)      # luz
TABLERO = (150, 86, 100)
ESTUCO = (250, 232, 206)
ESTUCO_S = (206, 176, 170)
ROJO = (214, 72, 78)
TIERRA_A = (200, 128, 92)
TIERRA_B = (96, 56, 92)
VERDE = (84, 150, 96)
VERDE_S = (52, 108, 90)
PIELES = [(240, 184, 140), (212, 146, 102), (168, 108, 74), (132, 84, 60)]
ROPAS = [(250, 240, 220), (222, 74, 84), (66, 190, 190), (255, 206, 80), (146, 96, 226), (255, 140, 90)]

PAL_CIELO = [((10, 12, 42), (60, 40, 104)),        # noche
             ((48, 58, 150), (255, 152, 112)),     # amanecer
             ((62, 146, 234), (255, 228, 184)),    # día
             ((58, 42, 138), (255, 118, 92))]      # ocaso


def _c(c, a=1.0):
    return c


def _poly(*pts):
    return np.array(pts, float)


def cielo_cols(h, fuego=0.0, ruina=0.0):
    h = h % 4.0
    i = int(h)
    u = smooth(h - i)
    a = PAL_CIELO[i]
    b = PAL_CIELO[(i + 1) % 4]
    top = P.mezcla(a[0], b[0], u)
    bot = P.mezcla(a[1], b[1], u)
    if fuego > 0:
        top = P.mezcla(top, (70, 12, 44), fuego * 0.85)
        bot = P.mezcla(bot, (255, 96, 40), fuego * 0.9)
    if ruina > 0:
        top = P.mezcla(top, (96, 108, 124), ruina * 0.35)
        bot = P.mezcla(bot, (176, 168, 170), ruina * 0.35)
    return top, bot


def tinte(col, bot, k=0.35):
    """Perspectiva atmosférica: acerca un color al del horizonte."""
    return P.mezcla(col, bot, k)


def pantalla_rect():
    return np.array([[-10, -10], [W + 10, -10], [W + 10, H + 10], [-10, H + 10]], float)


# ======================================================================== degradado rápido
def degradado_v(lz, x0, x1, y0, y1, c0, c1, ya, yb, paso=10.0):
    """Degradado vertical por bandas: color c0 en y=ya y c1 en y=yb (fuera, constante). Mucho más rápido que
    lz.degradado (que calcula cada píxel) y visualmente igual con bandas de ~10 px."""
    if y1 <= y0:
        return
    n = max(1, int(math.ceil((y1 - y0) / paso)))
    ys = np.linspace(y0, y1, n + 1)
    for i in range(n):
        u = min(1.0, max(0.0, ((ys[i] + ys[i + 1]) / 2 - ya) / (yb - ya)))
        lz.relleno(np.array([[x0, ys[i] - 0.7], [x1, ys[i] - 0.7], [x1, ys[i + 1] + 0.7], [x0, ys[i + 1] + 0.7]]),
                   P.mezcla(c0, c1, u))


# ======================================================================== cielo
def estrellas(lz, alfa, t, semilla=5):
    if alfa <= 0.01:
        return
    rng = np.random.RandomState(semilla)
    n = 130
    xs = rng.rand(n) * W
    ys = rng.rand(n) * 620
    rs = 0.9 + rng.rand(n) * 1.9
    ph = rng.rand(n) * 6.28
    br = 0.55 + 0.45 * np.sin(t * 1.6 + ph)
    pts = np.stack([xs, ys], 1)
    for lvl, col in ((0, (255, 255, 255)), (1, (200, 210, 255))):
        m = (np.arange(n) % 2) == lvl
        c = P.mezcla((20, 20, 50), col, alfa * float(br[m].mean()))
        lz.puntos(pts[m], rs[m], c)


def sol_luna(lz, hora, t, fuego=0.0):
    """Sol y luna que recorren el cielo con la hora (pantalla)."""
    h = hora % 4.0
    s = (h - 0.7) / 2.6                 # sol visible de 0.7 a 3.3
    if 0.0 <= s <= 1.0:
        x = 200 + s * 1520
        y = 640 - math.sin(math.pi * s) * 470
        col = P.mezcla((255, 170, 100), (255, 244, 190), math.sin(math.pi * s))
        lz.halo(x, y, 210, col, alfa=0.45)
        lz.relleno(circulo(x, y, 58, 40), col)
    m = ((h - 3.3) % 4.0) / 1.4          # luna de 3.3 a 4.7
    if 0.0 <= m <= 1.0:
        x = 260 + m * 1400
        y = 600 - math.sin(math.pi * m) * 430
        lz.halo(x, y, 130, (150, 170, 255), alfa=0.35)
        lz.relleno(circulo(x, y, 44, 36), (236, 240, 255))
        lz.relleno(circulo(x - 14, y - 8, 9, 16), (206, 212, 240))
        lz.relleno(circulo(x + 14, y + 14, 6, 14), (206, 212, 240))


def fondo_cielo(lz, est, t):
    top, bot = cielo_cols(est["hora"], est.get("fuego", 0.0), est.get("ruina", 0.0))
    degradado_v(lz, -10, W + 10, -10, H + 10, top, bot, 0, 780, paso=12.0)
    h = est["hora"] % 4.0
    noche = 1.0 - prog(min(h, 4.0 - h), 0.2, 0.95)
    estrellas(lz, noche * (1 - est.get("fuego", 0.0)), t)
    sol_luna(lz, est["hora"], t)
    return top, bot


# ======================================================================== capas con paralaje
def capa_mundo(lz, cam, f):
    """Grupo con paralaje f (1 = mundo; <1 = lejos)."""
    cx, cy, z = cam
    zl = z ** f
    return lz.grupo(GX - cx * f * zl, GY - cy * f * zl, zl)


def cordillera(lz, x0, x1, base, alt, semilla, col, col_luz, paso=60.0, pico=1.0):
    xs = np.arange(x0, x1 + paso, paso)
    hs = (0.55 + 0.45 * ruido1(xs / 380.0, semilla)) * alt * (0.75 + 0.25 * ruido1(xs / 110.0, semilla + 7))
    top = np.stack([xs, base - hs], 1)
    poly = np.vstack([top, [[xs[-1], base + 900], [xs[0], base + 900]]])
    lz.relleno(poly, col)
    # cara iluminada (mitad de cada ladera)
    for i in range(len(xs) - 1):
        if hs[i + 1] > hs[i] and (i % 2 == 0):
            q = np.array([[xs[i], base - hs[i]], [xs[i + 1], base - hs[i + 1]], [xs[i + 1], base], [xs[i], base]])
            lz.relleno(q, col_luz, alfa=0.5)


# ======================================================================== llamas y humo
def llama(lz, x, y, s, t, seed=0, alfa=1.0):
    """Llama de tres capas (rojo, naranja, amarillo). Origen en la base."""
    ph = h01(seed) * 6.28
    for k, (col, sc) in enumerate((((236, 60, 48), 1.0), ((255, 138, 40), 0.72), ((255, 224, 96), 0.42))):
        n = 14
        u = np.linspace(0, 1, n)
        alt = 90 * s * sc * (1 + 0.16 * math.sin(t * 9 + ph + k))
        ancho = 34 * s * sc
        izq = [(x - ancho * math.sin(math.pi * v) ** 0.8 + 9 * s * math.sin(t * 7 + ph + v * 5),
                y - alt * v) for v in u]
        der = [(x + ancho * math.sin(math.pi * v) ** 0.8 + 9 * s * math.sin(t * 7 + ph + v * 5 + 1),
                y - alt * v) for v in u[::-1]]
        lz.relleno(np.array(izq + der), col, alfa=alfa)


def humo(lz, x, y, t, t0, n=7, s=1.0, alfa=0.55, seed=0, col=(70, 52, 84)):
    if t < t0:
        return
    for i in range(n):
        ti = ((t - t0) * 0.35 + i / n) % 1.0
        px = x + 40 * s * math.sin(ti * 5 + i * 1.7 + seed) + ti * 60 * s
        py = y - ti * 420 * s
        r = (26 + ti * 70) * s
        lz.relleno(circulo(px, py, r, 24), col, alfa=alfa * (1 - ti) * min(1.0, ti * 6))


# ======================================================================== personas
def _capsula(lz, x0, y0, ang, L, w, col):
    x1, y1 = x0 + L * math.sin(ang), y0 + L * math.cos(ang)
    dx, dy = math.cos(ang) * w / 2, -math.sin(ang) * w / 2
    lz.relleno(np.array([[x0 - dx, y0 - dy], [x0 + dx, y0 + dy], [x1 + dx, y1 + dy], [x1 - dx, y1 - dy]]), col)
    lz.relleno(circulo(x1, y1, w / 2, 10), col)
    return x1, y1


def persona(lz, x, y, s=1.0, t=0.0, ropa=0, piel=0, paso=0.0, lado=1, brazos=0.0, sentado=False,
            tocado=None, seed=0, alfa=1.0, carga=None, cara=None):
    """Personita plana (origen en los pies, ~110 de alto). paso: velocidad del andar (0 = quieto).
    brazos 0..1: levanta los brazos. tocado: None | 'plumas' | 'oro'. carga: None | 'bulto' | 'vasija'."""
    rc = ROPAS[ropa % len(ROPAS)]
    pc = PIELES[piel % len(PIELES)]
    sombra_r = P.oscurecer(rc, 0.22)
    ph = t * paso * 6.0 + h01(seed) * 6.28
    sw = math.sin(ph) * 0.5 if paso > 0 else 0.0
    bob = abs(math.sin(ph)) * 3 if paso > 0 else 0.0
    with lz.grupo(x, y - bob * s, s * lado, 0.0, s):
        if sentado:
            _capsula(lz, -6, -18, 1.35, 28, 10, P.oscurecer(rc, 0.3))
            lz.relleno(rect_red(-14, -62, 28, 46, 10), rc)
            _capsula(lz, 0, -58, 0.3, 26, 8, pc)
            lz.relleno(circulo(0, -76, 12, 20), pc)
            lz.relleno(np.array([[-13, -78], [0, -94], [13, -78], [11, -84], [0, -88], [-11, -84]]), (44, 30, 56))
            return
        _capsula(lz, -5, -42, -sw, 42, 10, P.oscurecer(rc, 0.35))
        _capsula(lz, 5, -42, sw, 42, 10, P.oscurecer(rc, 0.35))
        lz.relleno(rect_red(-13, -84, 26, 46, 10), rc)
        lz.relleno(np.array([[-13, -50], [13, -50], [12, -40], [-12, -40]]), sombra_r)
        a1 = -0.3 + (-2.6 * brazos) - sw * 0.8 if brazos > 0 else -0.25 - sw
        a2 = 0.3 + (2.6 * brazos) + sw * 0.8 if brazos > 0 else 0.25 + sw
        _capsula(lz, -13, -78, a1, 32, 9, pc)
        _capsula(lz, 13, -78, a2, 32, 9, pc)
        if carga == "bulto":
            lz.relleno(rect_red(-22, -84, 16, 30, 6), (176, 120, 80))
        elif carga == "vasija":
            lz.relleno(elipse(0, -112, 15, 12, 0, 20), (206, 108, 78))
        lz.relleno(circulo(0, -98, 13, 22), pc)
        lz.relleno(np.array([[-13, -100], [0, -118], [13, -100], [11, -108], [0, -112], [-11, -108]]), (44, 30, 56))
        if cara == "sorpresa":
            for ex in (-5, 5):
                lz.relleno(circulo(ex, -97, 3.6, 12), (255, 255, 255))
                lz.relleno(circulo(ex + 0.4, -97, 1.8, 10), (34, 24, 52))
            lz.relleno(elipse(0, -89, 3.2, 4.4, 0, 14), (70, 30, 50))
        if tocado == "plumas":
            for i, c in enumerate(((60, 200, 130), (255, 210, 80), (230, 80, 90), (60, 200, 130), (90, 160, 240))):
                a = -0.9 + i * 0.45
                lz.relleno(elipse(math.sin(a) * 22, -118 - math.cos(a) * 20, 6, 18, -a, 12), c)
        elif tocado == "oro":
            lz.relleno(rect_red(-14, -117, 28, 8, 3), (255, 210, 90))


def grupo_gente(lz, x0, x1, y, n, t, semilla, s=0.5, paso=0.35, alfa=1.0, vis=None):
    """n personas repartidas entre x0 y x1 (mundo, absoluto) caminando en distintos sentidos; vis = (a, b) recorta."""
    for i in range(n):
        u = h01(semilla, i)
        v = h01(semilla, i, 3)
        dirn = 1 if h01(semilla, i, 5) > 0.5 else -1
        vel = 30 + 25 * h01(semilla, i, 7)
        L = x1 - x0
        px = x0 + ((u * L + dirn * vel * t * paso) % L)
        if vis and not (vis[0] <= px <= vis[1]):
            continue
        persona(lz, px, y + 10 * v, s * (0.9 + 0.2 * v), t, ropa=i, piel=int(3 * h01(semilla, i, 9)),
                paso=1.0 if paso > 0 else 0.0, lado=dirn, seed=i + semilla)


# ======================================================================== vegetación y casas
def nopal(lz, x, y, s=1.0, col=VERDE):
    for (dx, dy, rx, ry, a) in ((0, -40, 20, 34, 0.0), (-26, -74, 16, 26, -0.6), (24, -80, 16, 26, 0.5),
                                (-36, -110, 11, 19, -0.3)):
        lz.relleno(elipse(x + dx * s, y + dy * s, rx * s, ry * s, a, 20), col)
    lz.relleno(elipse(x - 6 * s, y - 46 * s, 8 * s, 20 * s, 0, 16), P.aclarar(col, 0.12))


def agave(lz, x, y, s=1.0, col=(96, 170, 150)):
    for a in np.linspace(-1.2, 1.2, 7):
        tip = (x + math.sin(a) * 70 * s, y - math.cos(a) * 62 * s)
        lz.relleno(np.array([[x - 7 * s, y], [tip[0], tip[1]], [x + 7 * s, y]]), P.mezcla(col, (60, 110, 120), abs(a) / 1.6))


def arbolito(lz, x, y, s=1.0, col=VERDE, seco=0.0):
    c = P.mezcla(col, (150, 130, 80), seco)
    lz.relleno(rect_red(x - 5 * s, y - 60 * s, 10 * s, 60 * s, 4), (110, 72, 84))
    for dx, dy, r in ((0, -84, 34), (-26, -66, 24), (26, -68, 24)):
        lz.relleno(circulo(x + dx * s, y + dy * s, r * s, 24), c)
    lz.relleno(circulo(x + 8 * s, y - 92 * s, 18 * s, 20), P.aclarar(c, 0.14))


def casa(lz, x, y, w, h, est, seed=0, escala=1.0):
    """Bloque de vivienda de techo plano con puerta y luz. Origen en la esquina izquierda de la base."""
    ruina = est.get("ruina", 0.0)
    h = h * (1 - 0.55 * ruina * h01(seed, 3))
    cuerpo = P.mezcla(ESTUCO, (150, 140, 130), ruina * 0.6)
    sombra = P.mezcla(ESTUCO_S, (110, 100, 100), ruina * 0.6)
    lz.relleno(rect_red(x, y - h, w, h, 3, 4), cuerpo)
    lz.relleno(rect_red(x + w * 0.72, y - h, w * 0.28, h, 3, 4), sombra)
    lz.relleno(np.array([[x - 3, y - h], [x + w + 3, y - h], [x + w + 3, y - h - 7], [x - 3, y - h - 7]]),
               P.mezcla(ROJO, (110, 90, 90), ruina * 0.7))
    lz.relleno(rect_red(x + w * 0.16, y - h * 0.55, w * 0.2, h * 0.55, 3, 4), (86, 52, 84))
    lu = est.get("luces", 0.0)
    if lu > 0.02:
        lz.relleno(rect_red(x + w * 0.5, y - h * 0.7, w * 0.16, h * 0.2, 2, 4), (255, 212, 110), alfa=lu)
        lz.halo(x + w * 0.58, y - h * 0.6, w * 0.55, (255, 190, 90), alfa=0.35 * lu)


_LAYOUT = {}


def _casas_layout(semilla, escala):
    k = (semilla, escala)
    if k not in _LAYOUT:
        L, x, i = [], -9000.0, 0
        while x < 12000:
            w = (54 + 46 * h01(semilla, i)) * escala
            h = (44 + 40 * h01(semilla, i, 2)) * escala
            L.append((x, w, h, i))
            x += w + (10 + 16 * h01(semilla, i, 4)) * escala
            i += 1
        _LAYOUT[k] = L
    return _LAYOUT[k]


def barrio(lz, x0, x1, y, est, semilla, escala=1.0, filas=1):
    """Casas en posiciones absolutas del mundo; solo se dibujan las que caen entre x0 y x1."""
    for (x, w, h, i) in _casas_layout(semilla, escala):
        if x + w < x0:
            continue
        if x > x1:
            break
        casa(lz, x, y, w, h, est, seed=semilla * 31 + i)


# ======================================================================== pirámides
def _tiers(x, w, h, n):
    th = h / n
    out = []
    for i in range(n):
        wb = w * (1 - 0.66 * i / n)
        wt = wb * 0.86
        out.append((x, wb, wt, -i * th, -(i + 1) * th))
    return out


def piramide(lz, x, w, h, n=5, est=None, luz_izq=True, templo=True, escalera=True, seed=0):
    est = est or {}
    ruina = est.get("ruina", 0.0)
    piedra = P.mezcla(PIEDRA, (120, 130, 110), ruina * 0.7)
    sombra = P.mezcla(PIEDRA_S, (86, 96, 96), ruina * 0.7)
    for (cx, wb, wt, yb, yt) in _tiers(x, w, h, n):
        lz.relleno(np.array([[cx - wb / 2, yb], [cx + wb / 2, yb], [cx + wt / 2, yt], [cx - wt / 2, yt]]), piedra)
        lz.relleno(np.array([[cx, yb], [cx + wb / 2, yb], [cx + wt / 2, yt], [cx, yt]]), sombra)
        # banda de tablero
        bh = (yb - yt) * 0.34
        lz.relleno(np.array([[cx - wt / 2 * 1.02, yt], [cx + wt / 2 * 1.02, yt],
                             [cx + wt / 2 * 1.02, yt + bh], [cx - wt / 2 * 1.02, yt + bh]]),
                   P.mezcla(TABLERO, (76, 88, 88), ruina * 0.6))
        lz.relleno(np.array([[cx - wt / 2, yt], [cx - wt / 2 + wt * 0.22, yt], [cx - wt / 2 + wt * 0.22, yt + bh],
                             [cx - wt / 2, yt + bh]]), PIEDRA_C, alfa=0.25 * (1 - ruina))
    top = -h
    wtop = w * (1 - 0.66) * 0.86
    if escalera:
        e0, e1 = w * 0.17, w * 0.08
        lz.relleno(np.array([[x - e0 / 2, 0], [x + e0 / 2, 0], [x + e1 / 2, top], [x - e1 / 2, top]]),
                   P.mezcla((250, 214, 160), (130, 140, 130), ruina * 0.6))
        for k in range(1, 18):
            yy = -h * k / 18
            ww = lerp(e0, e1, k / 18)
            lz.relleno(np.array([[x - ww / 2, yy], [x + ww / 2, yy], [x + ww / 2, yy + 2.2], [x - ww / 2, yy + 2.2]]),
                       (210, 150, 130), alfa=0.6)
    if templo:
        tw = wtop * 0.72
        th = h * 0.13
        lz.relleno(rect_red(x - tw / 2, top - th, tw, th, 4, 4), P.mezcla(ESTUCO, (140, 150, 140), ruina * 0.7))
        lz.relleno(rect_red(x, top - th, tw / 2, th, 4, 4), P.mezcla(ESTUCO_S, (110, 116, 116), ruina * 0.7))
        lz.relleno(np.array([[x - tw / 2 - 8, top - th], [x + tw / 2 + 8, top - th],
                             [x + tw / 2 + 8, top - th - 12], [x - tw / 2 - 8, top - th - 12]]), ROJO)
        lz.relleno(rect_red(x - tw * 0.12, top - th * 0.75, tw * 0.24, th * 0.75, 3, 4), (86, 52, 84))
    if ruina > 0.02:                     # tierra y vegetación que la cubren
        sil = []
        for (cx, wb, wt, yb, yt) in _tiers(x, w, h, n):
            sil.append((cx - wb / 2, yb))
        pts = [(x - w / 2 - 20, 4)]
        for k in range(0, 21):
            u = k / 20.0
            pts.append((x - w / 2 + u * (w / 2 - wtop / 2 * 0.9) - 10, -h * (u ** 0.85) * (1 - 0.0) + 8 * math.sin(u * 20 + seed)))
        pts.append((x - wtop / 2, top - 18))
        pts.append((x + wtop / 2, top - 18))
        for k in range(20, -1, -1):
            u = k / 20.0
            pts.append((x + w / 2 - u * (w / 2 - wtop / 2 * 0.9) + 10, -h * (u ** 0.85) + 8 * math.sin(u * 22 + seed + 2)))
        pts.append((x + w / 2 + 20, 4))
        lz.relleno(np.array(pts), (92, 132, 92), alfa=0.78 * ruina)
        lz.relleno(np.array(pts), (60, 96, 80), alfa=0.25 * ruina)
        for i in range(7):
            px = x + (h01(seed, i) - 0.5) * w * 0.6
            py = -h * (1 - abs(px - x) / (w / 2) * 0.9) * 0.85
            if ruina > 0.4:
                arbolito(lz, px, py + 10, 0.5 * ruina, VERDE_S, seco=0.1)


def plataforma(lz, x, w, h, est, tapa=True):
    ruina = est.get("ruina", 0.0)
    lz.relleno(np.array([[x - w / 2, 0], [x + w / 2, 0], [x + w * 0.44, -h], [x - w * 0.44, -h]]),
               P.mezcla(PIEDRA, (120, 130, 110), ruina * 0.7))
    lz.relleno(np.array([[x, 0], [x + w / 2, 0], [x + w * 0.44, -h], [x, -h]]),
               P.mezcla(PIEDRA_S, (86, 96, 96), ruina * 0.7))
    lz.relleno(np.array([[x - w * 0.45, -h], [x + w * 0.45, -h], [x + w * 0.45, -h + h * 0.24], [x - w * 0.45, -h + h * 0.24]]),
               P.mezcla(TABLERO, (76, 88, 88), ruina * 0.6))
    if tapa:
        lz.relleno(rect_red(x - w * 0.2, -h - h * 0.55, w * 0.4, h * 0.55, 3, 4), P.mezcla(ESTUCO, (140, 150, 140), ruina * 0.7))
        lz.relleno(np.array([[x - w * 0.22, -h - h * 0.55], [x + w * 0.22, -h - h * 0.55],
                             [x + w * 0.22, -h - h * 0.65], [x - w * 0.22, -h - h * 0.65]]), ROJO)


# ======================================================================== suelo
def suelo(lz, x0, x1, est, cam, profundo=False):
    ruina = est.get("ruina", 0.0)
    a = P.mezcla(TIERRA_A, (150, 150, 100), ruina * 0.6)
    b = P.mezcla(TIERRA_B, (60, 70, 70), ruina * 0.4)
    cx, cy, z = cam
    ytop, ybot = cy - GY / z - 30, cy + (H - GY) / z + 30       # solo la franja visible
    vx0, vx1 = cx - 1000 / z - 50, cx + 1000 / z + 50
    lz.relleno(np.array([[vx0, max(0.0, ytop)], [vx1, max(0.0, ytop)], [vx1, ybot], [vx0, ybot]], float), b)
    if ytop < 900:
        degradado_v(lz, vx0, vx1, max(0.0, ytop), min(900.0, ybot), a, b, 0, 900, paso=max(6.0, 10.0 / z))
    # calzada (banda más clara) y bandas de profundidad
    lz.relleno(np.array([[x0, 0], [x1, 0], [x1, 30], [x0, 30]], float),
               P.mezcla((240, 186, 140), (150, 160, 110), ruina * 0.8), alfa=0.85)
    for k, (yy, hh, al) in enumerate(((60, 18, 0.14), (120, 28, 0.12), (210, 44, 0.10))):
        lz.relleno(np.array([[x0, yy], [x1, yy], [x1, yy + hh], [x0, yy + hh]], float), (255, 236, 200), alfa=al)


# ======================================================================== extras del panorama
X_HUECO = -1850.0
Y_TUNEL = 92.0
CAMARAS = [(-1590.0, Y_TUNEL, 46, 36), (-1500.0, Y_TUNEL, 62, 46), (-1410.0, Y_TUNEL, 46, 36)]


def _rc(x, y, w, h, r=3):
    return rect_red(x, y, w, h, r, 6)


def subsuelo(lz, t, est):
    """Hueco tras la tormenta y túnel sellado bajo el Templo de la Serpiente Emplumada."""
    hueco = est.get("hueco", 0.0)
    tun = est.get("tunel", 0.0)
    if hueco > 0.01:
        w = 30 * e_out(hueco)
        lz.relleno(elipse(X_HUECO, 2, w * 1.25, 9 * e_out(hueco) + 1, 0, 24), (120, 70, 88), alfa=0.6)
        lz.relleno(elipse(X_HUECO, 2, w, 7 * e_out(hueco) + 1, 0, 24), (26, 14, 44))
        if hueco < 1:
            for i in range(6):
                lz.relleno(circulo(X_HUECO + (h01(2, i) - 0.5) * 60, -12 - 24 * (1 - hueco) * h01(3, i), 3, 8),
                           (150, 96, 90))
    if tun <= 0.01:
        return
    marco = (236, 156, 128)
    hueco_col = (34, 18, 58)
    p = e_out(prog(tun, 0.0, 0.22))                       # pozo
    if p > 0:
        lz.relleno(_rc(X_HUECO - 9.5, 0, 19, 96 * p + 6), marco, alfa=0.7)
        lz.relleno(_rc(X_HUECO - 7, 0, 14, 96 * p + 3), hueco_col)
    q = e_inout(prog(tun, 0.2, 0.7))                      # túnel horizontal
    if q > 0:
        x1 = lerp(X_HUECO, CAMARAS[0][0], q)
        lz.relleno(_rc(X_HUECO - 9.5, Y_TUNEL - 10, x1 - X_HUECO + 19, 20), marco, alfa=0.7)
        lz.relleno(_rc(X_HUECO - 7, Y_TUNEL - 7.5, x1 - X_HUECO + 14, 15), hueco_col)
    c = prog(tun, 0.66, 1.0)                              # cámaras y su tesoro
    if c > 0:
        lz.relleno(_rc(CAMARAS[0][0], Y_TUNEL - 8, CAMARAS[2][0] - CAMARAS[0][0], 16), marco, alfa=0.7)
        lz.relleno(_rc(CAMARAS[0][0], Y_TUNEL - 5.5, CAMARAS[2][0] - CAMARAS[0][0], 11), hueco_col)
        for i, (cx, cy, w, h) in enumerate(CAMARAS):
            a = e_out(prog(c, i * 0.18, i * 0.18 + 0.5))
            if a <= 0.01:
                continue
            lz.relleno(_rc(cx - w / 2 - 2.5, cy - h / 2 - 2.5, w + 5, h + 5, 8), marco, alfa=0.7 * a)
            lz.relleno(_rc(cx - w / 2, cy - h / 2, w, h, 6), hueco_col, alfa=a)
            lz.halo(cx, cy, w * 0.9, (255, 200, 110), alfa=0.28 * a)
            rng = [h01(20 + i, k) for k in range(40)]
            for k in range(9):        # esferas de pirita: brillan como oro
                px = cx + (rng[k] - 0.5) * (w - 12)
                py = cy + (rng[k + 9] - 0.5) * (h - 10)
                lz.relleno(circulo(px, py, 2.6 + 1.2 * rng[k + 18], 12), (255, 214, 104), alfa=a)
                lz.relleno(circulo(px - 0.8, py - 0.8, 0.9, 8), (255, 250, 214), alfa=a)
            for k in range(6):        # conchas y jade
                px = cx + (rng[k + 24] - 0.5) * (w - 10)
                py = cy + (rng[k + 30] - 0.5) * (h - 8)
                if k % 2:
                    lz.relleno(elipse(px, py, 2.6, 1.8, rng[k] * 3, 10), (250, 240, 226), alfa=a)
                else:
                    lz.relleno(np.array([[px, py - 3], [px + 2.4, py], [px, py + 3], [px - 2.4, py]]),
                               (90, 214, 150), alfa=a)
        cx, cy, w, h = CAMARAS[1]           # paisaje en miniatura con pozas de mercurio
        a = e_out(prog(c, 0.5, 1.0))
        for dx in (-19, -3, 14):
            lz.relleno(np.array([[cx + dx - 6, cy + 2], [cx + dx, cy - 9], [cx + dx + 6, cy + 2]]),
                       (176, 112, 118), alfa=a)
        for dx, dy in ((-16, 10), (0, 12), (15, 9)):
            lz.relleno(elipse(cx + dx, cy + dy, 7, 2.6, 0, 16), (196, 208, 230), alfa=a)
            lz.relleno(elipse(cx + dx - 2, cy + dy - 0.8, 2.6, 0.9, 0, 10), (250, 252, 255), alfa=a)


def estatua(lz, x, y, rotura=0.0, seed=0, s=1.0):
    col = (176, 146, 158)
    sh = (132, 106, 128)
    r = e_out(rotura)
    sg = 1 if seed % 2 else -1
    with lz.grupo(x, y, s):
        lz.relleno(rect_red(-18, -80, 36, 80, 6, 5), col)
        lz.relleno(rect_red(0, -80, 18, 80, 6, 5), sh)
        lz.relleno(rect_red(-22, -18, 44, 18, 3, 4), sh)
        with lz.grupo(34 * r * sg, -94 + 60 * r * r, 1.0, 1.4 * r * sg):     # la cabeza cae al romperse
            lz.relleno(circulo(0, 0, 15, 20), col)
            lz.relleno(rect_red(-20, -26, 40, 14, 4, 4), (214, 168, 110))
            lz.relleno(rect_red(0, -26, 20, 14, 4, 4), (176, 128, 100))
        if r > 0.02:
            lz.relleno(np.array([[-4, -78], [2, -60], [-2, -44], [4, -20]]), (60, 40, 70), alfa=0.8)
            for k in range(4):
                fx = (h01(seed, k) - 0.5) * 90 * r
                fy = -10 - 30 * h01(seed, k, 2) * (1 - r) + 8 * r
                lz.relleno(np.array([[fx - 7, fy], [fx + 6, fy - 5], [fx + 8, fy + 5]]), col if k % 2 else sh)


def incendio(lz, t, est):
    f = est.get("fuego", 0.0)
    if f <= 0.02:
        return
    fuegos = []
    for (x, w, h, n) in ((X_SOL, 780, 470, 5), (X_LUNA, 400, 270, 4), (X_CIUDADELA, 620, 150, 3)):
        for (cx, wb, wt, yb, yt) in _tiers(x, w, h, n):
            fuegos.append((cx - wt / 2 + 8, yt, 0.8))
            fuegos.append((cx + wt / 2 - 8, yt, 0.8))
        fuegos.append((x, -h - 30, 1.5))
        fuegos.append((x - 30, -h - 20, 1.1))
    for i, px in enumerate(np.arange(X_CIUDADELA + 600, X_LUNA - 300, 380.0)):
        if abs(px - X_SOL) > 500:
            fuegos.append((px, -70, 1.0))
    for i, (fx, fy, fs) in enumerate(fuegos):
        u = e_out(prog(f, (i % 9) * 0.05, (i % 9) * 0.05 + 0.5))
        if u > 0.02:
            llama(lz, fx, fy, fs * u, t, seed=i)
    lz.halo(X_SOL, -200, 1400, (255, 120, 40), alfa=0.28 * f)
    for i, (fx, fy, fs) in enumerate(fuegos[::4]):
        humo(lz, fx, fy - 60, t, 0.0, n=5, s=fs, alfa=0.42 * f, seed=i)


def estatuas(lz, t, est):
    a = est.get("estatuas", 0.0)
    if a <= 0.02:
        return
    for k in range(6):
        estatua(lz, X_SOL - 900 + k * 460 + (k // 3) * 300, 16, est.get("rotura", 0.0), seed=k, s=1.0)


def obreros(lz, t, est):
    a = est.get("obreros", 0.0)
    if a <= 0.02:
        return
    x0 = X_SOL - 1500
    avance = (t * 34) % 900
    bx = x0 + avance + 380
    for k in range(5):
        lz.relleno(circulo(bx - 60 + k * 30 + (avance % 30), 12, 8, 14), (150, 96, 88))
    lz.relleno(rect_red(bx - 70, -60, 140, 62, 6, 5), (188, 156, 170))
    lz.relleno(rect_red(bx, -60, 70, 62, 6, 5), (146, 118, 140))
    for k in range(9):
        persona(lz, bx + 120 + k * 46, 22 + (k % 2) * 8, 0.6, t, ropa=k, piel=k % 4, paso=1.0, lado=-1, seed=k)
    lz.trazo(np.array([[bx + 70, -22], [bx + 470, -30]]), (176, 128, 90), 3)


def turistas(lz, t, est):
    a = est.get("turistas", 0.0)
    if a <= 0.02:
        return
    n = int(6 + 34 * a)
    for i in range(n):
        u = ((h01(31, i) + t * (0.010 + 0.006 * h01(32, i))) % 1.0)
        yy = -470 * u
        xx = X_SOL + (h01(33, i) - 0.5) * (133 - 71 * u) * 0.9
        persona(lz, xx, yy, 0.30, t, ropa=i, piel=int(4 * h01(34, i)), paso=0.6, lado=1, seed=i,
                brazos=est.get("brazos", 0.0))
    for i in range(int(4 + 24 * a)):
        persona(lz, X_SOL - 300 + i * 40 + 20 * h01(35, i), 24 + 14 * h01(36, i), 0.45, t, ropa=i + 2,
                piel=int(4 * h01(37, i)), paso=0.0, lado=1 if i % 2 else -1, brazos=est.get("brazos", 0.0), seed=i)


def lluvia(lz, t, est):
    a = est.get("lluvia", 0.0)
    if a <= 0.02:
        return
    for i in range(9):
        x = 100 + i * 230
        y = 60 + 24 * math.sin(i * 1.7 + t * 0.4)
        for dx, dy, r in ((0, 0, 120), (-90, 20, 90), (90, 24, 96), (30, -34, 90)):
            lz.relleno(circulo(x + dx, y + dy, r, 28), (66, 58, 104), alfa=0.9 * a)
    with lz.capa(2):
        for i in range(46):
            x = (h01(50, i) * (W + 300) + t * 130) % (W + 300) - 100
            y = ((h01(51, i) + t * (0.9 + 0.3 * h01(52, i))) % 1.0) * (H + 60) - 30
            lz.trazo(np.array([[x, y], [x - 14, y + 34]]), (176, 200, 255), 3)


# ======================================================================== panorama completo
def panorama(lz, t, est, cam):
    """Dibuja el panorama con el estado `est` y la cámara `cam` = (cx, cy, z)."""
    top, bot = fondo_cielo(lz, est, t)
    cx, cy, z = cam
    ruina = est.get("ruina", 0.0)
    fuego = est.get("fuego", 0.0)
    dia = est["hora"] % 4.0
    tono = P.mezcla(bot, (255, 255, 255), 0.0)
    xa, xb = cx - 1400 / max(z, 0.2) - 2400, cx + 1400 / max(z, 0.2) + 2400
    v0, v1 = cx - 1100 / z - 250, cx + 1100 / z + 250     # franja visible del mundo (con margen)

    with capa_mundo(lz, cam, 0.10):                 # cordillera lejana
        cordillera(lz, xa * 0.2 - 3000, xb * 0.2 + 3000, 0, 300, 2, tinte((92, 82, 150), bot, 0.55),
                   tinte((150, 120, 190), bot, 0.4), 80)
    with capa_mundo(lz, cam, 0.28):                 # cerros medios (Cerro Gordo)
        cordillera(lz, xa * 0.4 - 3000, xb * 0.4 + 3000, 30, 230, 9, tinte((112, 96, 142), bot, 0.4),
                   tinte((170, 130, 160), bot, 0.3), 70)
    with capa_mundo(lz, cam, 1.0):
        x0, x1 = xa - 2000, xb + 2000
        # casas del fondo (más pequeñas), con perspectiva
        with lz.grupo(0, -34, 0.62):
            barrio(lz, v0 / 0.62, v1 / 0.62, 0, est, 1)
        suelo(lz, x0, x1, est, cam)
        subsuelo(lz, t, est)
        # plataformas y templos de la calzada
        for i, px in enumerate(np.arange(X_CIUDADELA + 600, X_LUNA - 300, 380.0)):
            if abs(px - X_SOL) > 500:
                plataforma(lz, px, 210, 46 + 16 * h01(3, i), est, tapa=(i % 2 == 0))
        piramide(lz, X_CIUDADELA, 620, 150, 3, est, seed=1, templo=True, escalera=True)
        piramide(lz, X_SOL, 780, 470, 5, est, seed=2)
        piramide(lz, X_LUNA, 400, 270, 4, est, seed=3)
        # casas en primer plano a los lados de la calzada
        barrio(lz, v0, min(v1, X_CIUDADELA - 420), 0, est, 4)
        # plantas del primer plano
        for i in range(int(v0 // 220), int(v1 // 220) + 2):
            px = i * 220 + 90 * h01(7, i)
            k = h01(8, i)
            if k < 0.34:
                nopal(lz, px, 40 + 26 * h01(9, i), 0.9, P.mezcla(VERDE, (150, 150, 100), ruina * 0.4))
            elif k < 0.6:
                agave(lz, px, 44 + 30 * h01(9, i), 0.9)
            elif k < 0.75 and ruina > 0:
                arbolito(lz, px, 34, 0.8 + ruina * 0.9, VERDE_S, seco=0.2)
        incendio(lz, t, est)
        estatuas(lz, t, est)
        obreros(lz, t, est)
        turistas(lz, t, est)
        # gente
        g = est.get("gente", 0.0)
        if g > 0.02:
            n = int((3 + 26 * g) * 2.6)
            grupo_gente(lz, -3000.0, 6000.0, 14, n, t, 11, s=0.55, alfa=g, vis=(v0, v1))
    lluvia(lz, t, est)
    return top, bot
