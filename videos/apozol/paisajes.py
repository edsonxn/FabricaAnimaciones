# -*- coding: utf-8 -*-
"""Paisajes 2D de Juchipila (estilo Kurzgesagt): cielo, sol, sierras con paralaje, paredes del cañón, río, flores y aves.
`amb` va de 0 (amanecer cálido y tranquilo) a 1 (tormenta roja); entre medias se mezcla. Todo es función de t."""
import math

import numpy as np

import plano as P
from motor import W, H, elipse, circulo, catmull, h01, prog, smooth, ruido1, rect_red
from kz_abstracto import _petalo_pts

ALBA = dict(cielo=((92, 56, 160), (236, 112, 150), (255, 206, 128)), sol=(255, 236, 176), sierras=((196, 124, 176), (166, 98, 160), (134, 74, 140), (100, 52, 112), (72, 38, 90)),
            pared=((98, 54, 104), (74, 40, 88)), luz=(255, 170, 96), rio=((110, 190, 232), (62, 130, 206)), pasto=((84, 168, 110), (52, 130, 96)))
TORMENTA = dict(cielo=((24, 8, 46), (112, 28, 70), (236, 84, 70)), sol=(255, 110, 80), sierras=((120, 44, 96), (92, 34, 82), (66, 26, 68), (46, 20, 56), (30, 12, 40)),
                pared=((56, 22, 60), (38, 14, 46)), luz=(255, 90, 80), rio=((170, 70, 110), (110, 36, 84)), pasto=((70, 80, 80), (44, 52, 62)))


def _m(a, b, u):
    return tuple(int(round(a[i] + (b[i] - a[i]) * u)) for i in range(3))


def pal(amb):
    u = float(np.clip(amb, 0, 1))
    return dict(cielo=tuple(_m(ALBA["cielo"][i], TORMENTA["cielo"][i], u) for i in range(3)), sol=_m(ALBA["sol"], TORMENTA["sol"], u),
                sierras=tuple(_m(ALBA["sierras"][i], TORMENTA["sierras"][i], u) for i in range(5)),
                pared=tuple(_m(ALBA["pared"][i], TORMENTA["pared"][i], u) for i in range(2)), luz=_m(ALBA["luz"], TORMENTA["luz"], u),
                rio=tuple(_m(ALBA["rio"][i], TORMENTA["rio"][i], u) for i in range(2)), pasto=tuple(_m(ALBA["pasto"][i], TORMENTA["pasto"][i], u) for i in range(2)))


_BG = {}


def cielo(amb):
    """Fondo (H, W, 3) float32 con degradado de tres tonos."""
    c = pal(round(float(amb), 2))["cielo"]
    if c not in _BG:
        ys = np.linspace(0, 1, H, dtype=np.float32)[:, None]
        a, b, d = (np.float32(x) / 255 for x in c)
        u1 = np.clip(ys / 0.55, 0, 1)
        u2 = np.clip((ys - 0.55) / 0.45, 0, 1)
        col = np.where(ys[..., None] < 0.55, a * (1 - u1[..., None]) + b * u1[..., None], b * (1 - u2[..., None]) + d * u2[..., None])
        _BG[c] = np.repeat(col, W, axis=1).astype(np.float32)
    return _BG[c]


def sol(lz, x, y, r, t, amb=0.0, alfa=1.0):
    p = pal(amb)
    lz.halo(x, y, r * 5.0, p["sol"], alfa=0.30 * alfa, dureza=1.1, capa=0)
    lz.halo(x, y, r * 2.6, p["sol"], alfa=0.45 * alfa, dureza=1.4, capa=0)
    for k in range(12):                                            # rayos suaves que giran
        a = k * math.pi / 6 + t * 0.05
        lz.relleno(np.array([[x + math.cos(a - 0.05) * r * 1.2, y + math.sin(a - 0.05) * r * 1.2], [x + math.cos(a) * r * 3.2, y + math.sin(a) * r * 3.2],
                             [x + math.cos(a + 0.05) * r * 1.2, y + math.sin(a + 0.05) * r * 1.2]]), p["sol"], alfa=0.10 * alfa, capa=0)
    lz.relleno(circulo(x, y, r, 40), P.aclarar(p["sol"], 0.2), alfa=alfa, capa=0)


def _linea_sierra(x0, x1, y_base, amp, paso, seed, fase=0.0, escala=1.0):
    xs = np.arange(x0, x1 + paso, paso)
    ys = [y_base - amp * (0.55 * ruido1(x * 0.0042 * escala + seed * 7 + fase, seed, 1) + 0.30 * ruido1(x * 0.011 * escala + seed * 3 + fase, seed, 2) + 0.15 * ruido1(x * 0.027 * escala + fase, seed, 3)) for x in xs]
    return list(zip(xs, ys))


VERDES = ((140, 200, 104), (112, 184, 100), (88, 164, 96), (64, 140, 88), (48, 112, 80))


def sierras(lz, t, cx, amb=0.0, y0=620, capas=5, semilla=1, deriva=2.0, verde=0.0):
    """5 capas de sierra con paralaje (cx = desplazamiento de cámara en px; las lejanas se mueven menos). El relieve es función de la coordenada
    del mundo, así que al mover la cámara la sierra no «hierve»."""
    p = pal(amb)
    xs = np.arange(-80, W + 81, 40)
    for i in range(capas):
        prof = (i + 1) / capas
        par = 0.12 + 0.55 * prof
        off = -cx * par - t * deriva * (0.3 + prof)
        y_base = y0 - (1 - prof) * 120 + prof * 10
        amp = 130 + 90 * prof
        pts = [(float(x), y_base - amp * (0.55 * ruido1((x - off) * 0.0042 + semilla * 7, semilla + i, 1) + 0.30 * ruido1((x - off) * 0.011 + semilla * 3, semilla + i, 2)
                                       + 0.15 * ruido1((x - off) * 0.027, semilla + i, 3))) for x in xs]
        col = _m(p["sierras"][i], VERDES[i], 0.92 * verde) if verde > 0 else p["sierras"][i]
        lz.relleno(np.array(pts + [(W + 80.0, H + 20.0), (-80.0, H + 20.0)]), col, capa=0)
        borde = np.array(pts + [(x, y + 16) for x, y in pts[::-1]])                 # filo de luz en la cresta
        lz.relleno(borde, _m(col, p["luz"], 0.30 + 0.1 * (1 - prof)), alfa=0.55, capa=0)
        lz.halo(W / 2, y_base + 60, 900, _m(col, p["cielo"][2], 0.5), alfa=0.18, dureza=0.9, capa=0)     # bruma entre capas


def pared_canon(lz, t, lado, amb=0.0, y_top=140, ancho=520, seed=1, capa=1, verde=0.0):
    """Pared del cañón en primer plano (lado = -1 izquierda, +1 derecha) con cara iluminada, estratos y filo de luz."""
    p = pal(amb)
    x_out = -120 if lado < 0 else W + 120
    sal = -1 if lado < 0 else 1                                       # hacia fuera de la pantalla
    n = 14
    cont = []
    for i in range(n + 1):
        v = i / n
        y = y_top + (H - y_top + 80) * v
        d = ancho * (0.50 + 0.50 * smooth(v)) + 45 * ruido1(v * 8 + seed * 5, seed, 4) + 18 * math.sin(t * 0.3 + v * 3)
        cont.append((d if lado < 0 else W - d, y))
    arriba, abajo = (x_out, y_top - 60.0), (x_out, H + 80.0)
    c1 = _m(p["pared"][1], (52, 110, 84), 0.55 * verde) if verde > 0 else p["pared"][1]
    c0 = _m(p["pared"][0], (76, 140, 98), 0.55 * verde) if verde > 0 else p["pared"][0]
    lz.relleno(np.array([arriba] + cont + [abajo]), c1, capa=capa)
    cont2 = [(x + sal * 34, y) for x, y in cont]
    lz.relleno(np.array([arriba] + cont2 + [abajo]), c0, capa=capa)
    for k in range(6):                                                # estratos
        v = 0.10 + 0.15 * k
        yk = y_top + (H - y_top) * v
        x_in = cont[min(n, int(v * n))][0] + sal * 34
        lz.relleno(np.array([(x_out, yk), (x_in, yk + 6), (x_in, yk + 18), (x_out, yk + 12)]), _m(p["pared"][1], (0, 0, 0), 0.3), alfa=0.35, capa=capa)
    borde = np.array(cont + [(x + sal * 12, y) for x, y in cont[::-1]])
    lz.relleno(borde, p["luz"], alfa=0.5, capa=capa)


def rio_borde(y, y_h=640, x_h=960, ancho_fondo=60, ancho_frente=900):
    """(x izq, x der) del cauce de `rio` a la altura y de pantalla (None arriba del horizonte)."""
    if y < y_h:
        return None
    v = (y - y_h) / (H + 40 - y_h)
    w = ancho_fondo + (ancho_frente - ancho_fondo) * v
    m = x_h + 90 * math.sin(v * 3.1 + 0.6) * (1 - v * 0.55)
    return m - w / 2, m + w / 2


def rio(lz, t, amb=0.0, y_h=640, x_h=960, ancho_fondo=60, ancho_frente=900, frac=1.0, capa=1):
    """Río en perspectiva desde el horizonte (x_h, y_h) hasta el borde inferior, con brillos que avanzan hacia la cámara."""
    p = pal(amb)
    top, bot = p["rio"]
    n = 18
    izq, der = [], []
    for i in range(n + 1):
        v = (i / n) ** 1.7
        y = y_h + (H + 40 - y_h) * v
        w = ancho_fondo + (ancho_frente - ancho_fondo) * v
        meandro = 90 * math.sin(v * 3.1 + 0.6) * (1 - v * 0.55)
        izq.append((x_h + meandro - w / 2, y))
        der.append((x_h + meandro + w / 2, y))
    poli = np.array(izq + der[::-1])
    lz.degradado(poli, top, bot, (0, y_h), (0, H), capa=capa)
    for k in range(14):                                             # destellos que avanzan
        u = (t * 0.10 + h01(7, k, 1)) % 1.0
        v = u ** 1.7
        y = y_h + (H - y_h) * v
        w = ancho_fondo + (ancho_frente - ancho_fondo) * v
        meandro = 90 * math.sin(v * 3.1 + 0.6) * (1 - v * 0.55)
        xx = x_h + meandro + (h01(7, k, 2) - 0.5) * w * 0.7
        lz.relleno(elipse(xx, y, 8 + 70 * v, 2 + 7 * v, 0, 16), (255, 255, 255), alfa=0.35 * min(1, u * 8) * (1 - u), capa=capa)


def flores_frente(lz, t, cx=0.0, n=26, amb=0.0, y0=900, seed=5, escala=1.0):
    """Hierba y cempasúchiles en primer plano (se mecen). cx desplaza la capa (paralaje fuerte)."""
    p = pal(amb)
    for i in range(n):
        zona = h01(seed, i, 1)                                      # solo en las orillas: izquierda o derecha del río
        x = (-150 + 700 * zona if i % 2 == 0 else 1440 + 700 * zona) - cx * 0.35
        y = y0 + 150 * h01(seed, i, 2)
        s = (0.8 + 0.9 * h01(seed, i, 3)) * escala * (0.7 + 0.5 * (y - y0) / 150)
        bal = math.sin(t * 1.4 + i * 1.7) * 7 * s
        col = p["pasto"][i % 2]
        lz.relleno(np.array([[x - 7 * s, y + 40 * s], [x + bal, y - 110 * s], [x + 7 * s, y + 40 * s]]), col, capa=2)
        lz.relleno(np.array([[x + 4 * s, y + 40 * s], [x + bal + 10 * s, y - 70 * s], [x + 14 * s, y + 40 * s]]), P.oscurecer(col, 0.2), capa=2)
        if i % 3 == 0:                                              # cempasúchil
            fx, fy = x + bal, y - 118 * s
            for k, (R_, c) in enumerate(((20, (255, 140, 30)), (14, (255, 176, 44)), (8, (255, 214, 90)))):
                for j in range(8):
                    a = j * math.pi / 4 + k * 0.4 + t * 0.2
                    lz.relleno(_petalo_pts(fx, fy, R_ * s * 1.1, R_ * s * 0.5, a), c, alfa=1.0 - 0.0 * k, capa=2)
            lz.relleno(circulo(fx, fy, 4 * s, 8), (120, 60, 20), capa=2)


def aves(lz, t, n=7, seed=1, y0=130, y1=380, alfa=0.9, color=(60, 30, 80), vel=1.0, sentido=1):
    for i in range(n):
        u = (t * 0.035 * vel + h01(seed, i, 1)) % 1.0
        x = (u if sentido > 0 else 1 - u) * (W + 200) - 100
        y = y0 + (y1 - y0) * h01(seed, i, 2) + 14 * math.sin(t * 0.9 + i)
        al = math.sin(t * 7 + i * 1.7) * 9
        s = 0.8 + 0.6 * h01(seed, i, 3)
        lz.relleno(np.array([[x - 14 * s, y - al * s], [x, y + 2 * s], [x + 14 * s, y - al * s], [x, y - 2 * s]]), color, alfa=alfa, capa=1)


def casita(lz, x, y, s, amb=0.0, muro=(236, 200, 150), techo=(190, 84, 70), chimenea=True, t=0.0, seed=0, capa=1):
    """Casita de adobe 2D (origen en la base, centro). Se tiñe con la luz del ambiente; con humo si tiene chimenea."""
    p = pal(amb)
    c = _m(muro, p["cielo"][1], 0.20 + 0.2 * amb)
    cs = P.oscurecer(c, 0.25)
    tc = _m(techo, p["cielo"][1], 0.15 + 0.2 * amb)
    k = s
    lz.relleno(np.array([(x - 46 * k, y), (x + 46 * k, y), (x + 46 * k, y - 38 * k), (x - 46 * k, y - 38 * k)]), cs, capa=capa)
    lz.relleno(np.array([(x - 46 * k, y), (x + 30 * k, y), (x + 30 * k, y - 38 * k), (x - 46 * k, y - 38 * k)]), c, capa=capa)
    lz.relleno(np.array([(x - 54 * k, y - 36 * k), (x + 54 * k, y - 36 * k), (x + 34 * k, y - 66 * k), (x - 34 * k, y - 66 * k)]), P.oscurecer(tc, 0.18), capa=capa)
    lz.relleno(np.array([(x - 54 * k, y - 36 * k), (x + 30 * k, y - 36 * k), (x + 20 * k, y - 66 * k), (x - 34 * k, y - 66 * k)]), tc, capa=capa)
    lz.relleno(np.array([(x - 8 * k, y), (x + 8 * k, y), (x + 8 * k, y - 22 * k), (x - 8 * k, y - 22 * k)]), (90, 50, 60), capa=capa)
    lz.relleno(np.array([(x + 14 * k, y - 18 * k), (x + 26 * k, y - 18 * k), (x + 26 * k, y - 28 * k), (x + 14 * k, y - 28 * k)]), _m((255, 214, 120), p["luz"], 0.4 * (1 - amb)), capa=capa)
    if chimenea:
        lz.relleno(np.array([(x + 22 * k, y - 60 * k), (x + 32 * k, y - 60 * k), (x + 32 * k, y - 82 * k), (x + 22 * k, y - 82 * k)]), cs, capa=capa)
        for i in range(5):
            u = ((t * 0.28 + i / 5 + h01(seed, i, 1)) % 1.0)
            lz.relleno(circulo(x + 28 * k + 22 * k * math.sin(u * 5 + i) + u * 16 * k, y - 86 * k - u * 90 * k, (5 + 14 * u) * k, 12), (236, 228, 240), alfa=0.55 * (1 - u), capa=capa)


def arbol(lz, x, y, s, amb=0.0, seed=0, t=0.0, capa=1):
    """Árbol 2D de copa en racimos (mezquite): tronco, 3 tonos de hoja, se mece apenas."""
    p = pal(amb)
    g0, g1 = p["pasto"]
    bal = math.sin(t * 1.1 + seed) * 3 * s
    lz.relleno(np.array([(x - 6 * s, y), (x + 6 * s, y), (x + 3 * s + bal * 0.3, y - 48 * s), (x - 3 * s + bal * 0.3, y - 48 * s)]), _m((120, 80, 70), p["pared"][1], 0.4), capa=capa)
    for dx, dy, r, c in ((-16, -62, 24, g1), (16, -64, 26, g1), (0, -80, 28, g1), (-12, -66, 22, g0), (12, -70, 24, g0), (-4, -86, 20, _m(g0, (255, 255, 255), 0.15))):
        lz.relleno(circulo(x + dx * s + bal, y + dy * s, r * s, 16), c, capa=capa)


def aldea(lz, t, amb=0.0, x0=620, x1=1320, y=706, n=5, seed=4, rio_h=640):
    """Casitas y árboles en las dos ORILLAS (plano medio). Se dibujan DESPUÉS del río: las que caerían en el cauce se apartan a la orilla
    más cercana (rio_h = horizonte del río que se dibuja con `rio`; None si no hay río)."""
    b = rio_borde(y + 10, rio_h) if rio_h is not None else None
    if b is None:
        xs = [x0 + (x1 - x0) * i / max(1, n - 1) for i in range(n)]
    else:                                                           # mitad en cada orilla, repartidas parejo (casa ~70 px + árbol a la derecha)
        paso = (x1 - x0) / max(1, n - 1)
        nl = n // 2
        nr = n - nl
        xl1 = b[0] - 40 - 110
        xr0 = b[1] + 40 + 50
        xs = [xl1 - paso * (nl - 1 - i) for i in range(nl)] + [xr0 + paso * i for i in range(nr)]
    for i in range(n):
        xx = xs[i] + 24 * (h01(seed, i, 1) - 0.5)
        yy = y + 22 * (h01(seed, i, 2) - 0.5) + (14 if i % 2 else 0)
        s = 0.8 + 0.3 * h01(seed, i, 3)
        arbol(lz, xx + 70, yy + 6, s * 0.9, amb, seed + i, t)
        casita(lz, xx, yy, s, amb, muro=[(236, 200, 150), (240, 214, 170), (226, 176, 140)][i % 3], techo=[(190, 84, 70), (170, 92, 96), (200, 110, 70)][i % 3], chimenea=(i % 2 == 0), t=t, seed=seed + i)
