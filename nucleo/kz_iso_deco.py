# -*- coding: utf-8 -*-
"""Densidad automática para dioramas isométricos (estilo Kurzgesagt): que ningún suelo quede liso.
  parches(...)   manchas orgánicas de tono variado sobre el terreno       campos(...)   mosaico de campos de cultivo con setos y surcos
  hierba(...)    motas de pasto y florecitas que se mecen                 esparcir(...) coloca N objetos al azar evitando zonas (árboles, rocas, arbustos…)
  bosque(...)    arboleda densa con claros                                 aves(...), mariposas(...), polvo_luz(...)  vida en el aire
  borde_cerca(...) cercas y setos en el borde de campos                    acequia(...)  canal de agua con corriente
Todo es función del tiempo y de la semilla (cada cuadro es independiente)."""
import math

import numpy as np

import kz_iso as I
import kz_iso_obj as O
import plano as P
from kz_iso import tint, sombra_elipse
from motor import circulo, elipse, rect_red, h01, catmull

FLORES = [(250, 214, 80), (240, 100, 140), (250, 250, 244), (150, 120, 240), (250, 150, 70)]


def parches(lz, iso, x0, y0, x1, y1, base, n=14, var=22, seed=0, alfa=0.5, tam=(40, 90)):
    """Manchas orgánicas más claras u oscuras que el suelo (variación de tono)."""
    for i in range(n):
        cx, cy = x0 + (x1 - x0) * h01(seed, i, 1), y0 + (y1 - y0) * h01(seed, i, 2)
        r = tam[0] + (tam[1] - tam[0]) * h01(seed, i, 3)
        a = h01(seed, i, 4) * 6.28
        pts = [(cx + math.cos(a + k * 1.047) * r * (0.7 + 0.5 * h01(seed, i, 10 + k)), cy + math.sin(a + k * 1.047) * r * (0.7 + 0.5 * h01(seed, i, 20 + k))) for k in range(6)]
        d = int(var * (h01(seed, i, 5) - 0.5) * 2)
        col = tuple(int(np.clip(c + d, 0, 255)) for c in base)
        I.suelo_curvo(lz, iso, pts, col, alfa=alfa)


def campos(lz, iso, x0, y0, x1, y1, nx=3, ny=3, seed=0, t=0.0, colores=None, setos=True, margen=4.0):
    """Mosaico de campos (cada celda con otro cultivo: maíz, trigo, hortaliza, barbecho, maguey) separados por setos."""
    colores = colores or [(176, 200, 96), (226, 196, 100), (140, 186, 100), (190, 150, 100), (214, 178, 112), (120, 176, 96)]
    w, d = (x1 - x0) / nx, (y1 - y0) / ny
    for j in range(ny):
        for i in range(nx):
            c = colores[int(h01(seed, i, j) * len(colores)) % len(colores)]
            xa, ya = x0 + i * w + margen, y0 + j * d + margen
            ww, dd = w - 2 * margen, d - 2 * margen
            I.suelo_rect(lz, iso, xa, ya, ww, dd, c)
            # surcos
            ang_x = h01(seed, i, j + 9) > 0.5
            n = max(2, int((dd if ang_x else ww) / 9))
            for k in range(n):
                f = (k + 0.5) / n
                if ang_x:
                    I.suelo_rect(lz, iso, xa + 2, ya + f * dd - 0.9, ww - 4, 1.8, P.oscurecer(c, 0.14), alfa=0.7)
                else:
                    I.suelo_rect(lz, iso, xa + f * ww - 0.9, ya + 2, 1.8, dd - 4, P.oscurecer(c, 0.14), alfa=0.7)
            if setos:
                for (a, b, cx_, dy_) in ((xa, ya, ww, 1.6), (xa, ya + dd - 1.6, ww, 1.6)):
                    I.suelo_rect(lz, iso, a, b, cx_, dy_, (86, 150, 84))


def hierba(lz, iso, x0, y0, x1, y1, n=160, seed=0, t=0.0, color=(96, 170, 84), flores=0.12, alto=5.0):
    """Briznas de pasto (triangulitos) y flores diminutas que se mecen con el viento. Se dibujan solo las visibles."""
    k = iso.z
    if k < 0.5:
        n = int(n * 0.5)
    for i in range(n):
        x = x0 + (x1 - x0) * h01(seed, i, 1)
        y = y0 + (y1 - y0) * h01(seed, i, 2)
        sx, sy = iso.P(x, y, 0)
        if sx < -20 or sx > 1940 or sy < -20 or sy > 1100:
            continue
        sw = math.sin(t * 2.2 + x * 0.05 + y * 0.03) * 1.4 * k
        if h01(seed, i, 3) < flores:
            c = FLORES[int(h01(seed, i, 4) * len(FLORES)) % len(FLORES)]
            lz.relleno(rect_red(sx - 0.5 * k + sw * 0.5, sy - 4.2 * k, 1.0 * k, 4.2 * k, 0.3), tint((96, 160, 80)))
            lz.relleno(circulo(sx + sw, sy - 5 * k, 1.9 * k, 6), tint(c))
        else:
            a = alto * (0.7 + 0.6 * h01(seed, i, 5)) * k
            lz.relleno(np.array([[sx - 1.1 * k, sy], [sx + 1.1 * k, sy], [sx + sw, sy - a]]), tint(color if h01(seed, i, 6) > 0.4 else P.aclarar(color, 0.2)))


def esparcir(m, x0, y0, x1, y1, n, fn, seed=0, evitar=(), min_d=0.0, clave_extra=0.0):
    """Registra n objetos en posiciones al azar dentro del rectángulo, evitando las cajas `evitar` [(x0,y0,x1,y1), ...] y manteniendo distancia mínima.
    fn(lz, iso, x, y, i). Devuelve las posiciones."""
    pos = []
    k = 0
    intentos = 0
    while len(pos) < n and intentos < n * 30:
        intentos += 1
        x = x0 + (x1 - x0) * h01(seed, intentos, 1)
        y = y0 + (y1 - y0) * h01(seed, intentos, 2)
        if any(a <= x <= c and b <= y <= d for (a, b, c, d) in evitar):
            continue
        if min_d and any((x - p[0]) ** 2 + (y - p[1]) ** 2 < min_d * min_d for p in pos):
            continue
        pos.append((x, y))
        i = len(pos) - 1
        m.add(x - 8, y - 8, x + 8, y + 8, 60, (lambda x, y, i: (lambda lz, iso: fn(lz, iso, x, y, i)))(x, y, i), clave=x + y + clave_extra)
    return pos


def bosque(m, x0, y0, x1, y1, n=30, seed=0, evitar=(), t_fn=None, tipos=("arbol",), h=(46, 70), colores=None, min_d=22):
    """Arboleda: mezcla de árboles de varios tamaños y colores (+ arbustos al pie)."""
    colores = colores or O.VERDES

    def f(lz, iso, x, y, i):
        tp = tipos[int(h01(seed, i, 7) * len(tipos)) % len(tipos)]
        hh = h[0] + (h[1] - h[0]) * h01(seed, i, 8)
        t = t_fn() if t_fn else 0.0
        if tp == "arbol":
            O.arbol(lz, iso, x, y, h=hh, color=colores[i % len(colores)], seed=seed + i, t=t)
        elif tp == "pino":
            O.pino(lz, iso, x, y, h=hh * 1.1, seed=seed + i)
        elif tp == "palma":
            O.palmera(lz, iso, x, y, h=hh, seed=seed + i, t=t)
        elif tp == "cipres":
            O.cipres(lz, iso, x, y, h=hh, seed=seed + i)
        elif tp == "nopal":
            O.nopal(lz, iso, x, y, s=0.8 + 0.5 * h01(seed, i, 9))
        elif tp == "maguey":
            O.maguey(lz, iso, x, y, s=0.8 + 0.4 * h01(seed, i, 9), seed=i)
        elif tp == "organo":
            O.organo(lz, iso, x, y, h=hh * 0.8, seed=i)
        elif tp == "arbusto":
            O.arbusto(lz, iso, x, y, r=8 + 5 * h01(seed, i, 9), seed=i, flores=(236, 92, 140) if i % 3 == 0 else None)
        elif tp == "roca":
            O.roca(lz, iso, x, y, s=0.8 + 0.7 * h01(seed, i, 9), seed=i)
    return esparcir(m, x0, y0, x1, y1, n, f, seed=seed, evitar=evitar, min_d=min_d)


def aves(lz, t, n=7, seed=1, y0=140, y1=420, alfa=0.9, color=(70, 44, 90), vel=1.0, sentido=1):
    """Bandada lejana de pájaros (V de dos alas) cruzando la pantalla en bucle."""
    for i in range(n):
        u = ((t * 0.035 * vel * (0.8 + 0.4 * h01(seed, i, 1))) + h01(seed, i, 2)) % 1.0
        x = (u * 2300 - 200) if sentido > 0 else (2100 - u * 2300)
        y = y0 + (y1 - y0) * h01(seed, i, 3) + 18 * math.sin(t * 0.9 + i)
        al = math.sin(t * 9 + i * 1.7) * 6
        s = 0.8 + 0.6 * h01(seed, i, 4)
        lz.relleno(np.array([[x - 10 * s, y - al * s], [x, y + 1.2 * s], [x + 10 * s, y - al * s], [x, y - 1.6 * s]]), color, alfa=alfa, capa=2)


def mariposas(lz, iso, x0, y0, x1, y1, n=5, t=0.0, seed=1):
    k = iso.z
    for i in range(n):
        x = x0 + (x1 - x0) * (0.5 + 0.5 * math.sin(t * 0.3 * (0.6 + h01(seed, i, 1)) + h01(seed, i, 2) * 6.28))
        y = y0 + (y1 - y0) * (0.5 + 0.5 * math.sin(t * 0.37 * (0.6 + h01(seed, i, 3)) + h01(seed, i, 4) * 6.28))
        z = 14 + 10 * math.sin(t * 1.3 + i)
        sx, sy = iso.P(x, y, z)
        al = abs(math.sin(t * 14 + i * 2.1))
        c = FLORES[i % len(FLORES)]
        for sg in (-1, 1):
            lz.relleno(elipse(sx + sg * 2.2 * k * al, sy, 2.6 * k * (0.3 + 0.7 * al), 3.2 * k, sg * 0.5, 8), tint(c), capa=2)


def polvo_luz(lz, t, n=26, seed=1, color=(255, 240, 200), alfa=0.5, area=(0, 0, 1920, 1080)):
    """Motas de polvo/pólenes que flotan a distintas profundidades (alfa que titila)."""
    x0, y0, x1, y1 = area
    for i in range(n):
        x = x0 + (x1 - x0) * ((h01(seed, i, 1) + t * 0.006 * (0.3 + h01(seed, i, 2))) % 1.0)
        y = y0 + (y1 - y0) * ((h01(seed, i, 3) + t * 0.004 * (h01(seed, i, 4) - 0.2)) % 1.0)
        r = 1.6 + 3.2 * h01(seed, i, 5)
        a = alfa * (0.4 + 0.6 * (0.5 + 0.5 * math.sin(t * 1.4 + i)))
        lz.relleno(circulo(x, y, r, 8), color, alfa=a, capa=2)


def acequia(lz, iso, pts_xy, t, ancho=10.0, c1=(70, 168, 226), c2=(40, 120, 200)):
    """Canal de agua con corriente (rayitas que avanzan) a lo largo de una polilínea del suelo."""
    p = np.array(catmull(np.asarray(pts_xy, float), 8, False), float)
    d = np.gradient(p, axis=0)
    d /= np.maximum(np.hypot(d[:, 0], d[:, 1]), 1e-6)[:, None]
    nrm = np.stack([-d[:, 1], d[:, 0]], 1)
    a_, b_ = p + nrm * (ancho / 2 + 2), p - nrm * (ancho / 2 + 2)
    I.suelo(lz, iso, np.vstack([a_, b_[::-1]]), (176, 150, 110))
    a_, b_ = p + nrm * ancho / 2, p - nrm * ancho / 2
    I.suelo(lz, iso, np.vstack([a_, b_[::-1]]), c1)
    seg = np.hypot(*np.diff(p, axis=0).T)
    s_ = np.r_[0, np.cumsum(seg)]
    for i in range(int(s_[-1] / 24)):
        u = ((i * 24 + t * 18) % s_[-1])
        j = int(np.clip(np.searchsorted(s_, u, side="right") - 1, 0, len(p) - 2))
        q0 = p[j] + nrm[j] * ancho * 0.18 * (1 if i % 2 else -1)
        q1 = q0 + d[j] * 8
        I.suelo(lz, iso, [q0 + nrm[j] * 0.8, q1 + nrm[j] * 0.8, q1 - nrm[j] * 0.8, q0 - nrm[j] * 0.8], c2, alfa=0.8)


def muro_bajo(m, pts_xy, h=10, color=(214, 196, 178)):
    """Muro bajo de piedra a lo largo de una polilínea (tramos rectos alineados a los ejes)."""
    p = np.asarray(pts_xy, float)
    for a, b in zip(p[:-1], p[1:]):
        x0, x1 = sorted((a[0], b[0]))
        y0, y1 = sorted((a[1], b[1]))
        w, d = max(x1 - x0, 3.5), max(y1 - y0, 3.5)
        m.add(x0, y0, x0 + w, y0 + d, h, (lambda x0, y0, w, d: (lambda lz, iso: I.caja(lz, iso, x0, y0, w, d, h, color)))(x0, y0, w, d))
