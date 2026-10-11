# -*- coding: utf-8 -*-
"""Mundos 2D de la escena 6 (el hartazgo): costales de tributo, templo que se derrumba, olla tapada que hierve con termómetro de tensión,
y el peñol del Mixtón visto de lado (paredes casi verticales, gente que sube, fogatas arriba)."""
import math

import numpy as np

import plano as P
import kz_pers2d as K2
from motor import circulo, elipse, rect_red, catmull, h01, prog, smooth, e_out, e_in, e_back, e_inout, ruido1, W, H
from util import llama, humo

BARRO = (196, 104, 70)
BARRO_S = (138, 62, 56)
BARRO_L = (226, 146, 96)
PIEDRA = ((214, 190, 160), (176, 146, 124), (132, 104, 104))      # luz, base, sombra


# ------------------------------------------------------------------------------------------------ costal de tributo
def costal_mano(D, m, ang, t, seed):
    """Objeto para K2.cuerpo(obj_d=...): costal de maíz sostenido delante del pecho."""
    cx, cy = m[0] + 0.25, m[1] - 0.15
    pts = [(cx - 0.95, cy + 0.85), (cx - 1.05, cy - 0.15), (cx - 0.6, cy - 0.9), (cx - 0.15, cy - 1.15), (cx + 0.25, cy - 0.95), (cx + 0.8, cy - 0.55),
           (cx + 1.0, cy + 0.35), (cx + 0.7, cy + 0.95), (cx - 0.2, cy + 1.05)]
    D.cat(pts, (176, 140, 92))
    D.cat([(x - 0.12, y - 0.1) for x, y in pts[:6]] + [(cx + 0.3, cy + 0.2), (cx - 0.5, cy + 0.4)], (206, 172, 116), a=0.9)
    D.ell(cx - 0.1, cy - 1.0, 0.32, 0.16, (150, 112, 72))
    for k in range(3):
        D.ell(cx - 0.35 + 0.3 * k, cy + 0.1 + 0.12 * (k % 2), 0.09, 0.06, (250, 210, 90))


def costal(lz, x, y, s, seed=0, alfa=1.0, capa=1):
    """Costal en el suelo (origen en la base)."""
    b = (176, 140, 92) if seed % 3 else (190, 150, 100)
    q = np.array([(-1.0, 0.0), (-1.1, -0.9), (-0.7, -1.6), (-0.2, -1.85), (0.3, -1.7), (0.9, -1.2), (1.05, -0.4), (0.9, 0.0)])
    lz.relleno(catmull(q * s + (x, y), 6, True), P.oscurecer(b, 0.25), alfa=alfa, capa=capa)
    lz.relleno(catmull(q[:6] * s * 0.92 + (x - 0.1 * s, y - 0.1 * s), 6, True), b, alfa=alfa, capa=capa)
    lz.relleno(elipse(x - 0.15 * s, y - 1.8 * s, 0.35 * s, 0.16 * s, 0, 12), P.oscurecer(b, 0.35), alfa=alfa, capa=capa)


def pila_costales(lz, x, y, s, n, alfa=1.0, capa=1):
    """Pila que crece con n (0..15): filas de 5, 4, 3, 2, 1."""
    k = 0
    for fila, m in enumerate((5, 4, 3, 2, 1)):
        for j in range(m):
            if k >= n:
                return
            costal(lz, x + (j - (m - 1) / 2) * 1.9 * s, y - fila * 1.45 * s, s, seed=k, alfa=alfa, capa=capa)
            k += 1


# ------------------------------------------------------------------------------------------------ templo que se derrumba
def templo_derribado(lz, x, y, s, t, caida, amb=0.0, capa=1):
    """Basamento escalonado con un templo arriba; con caida 0..1 los bloques del templo se sueltan, giran y caen con polvo. Origen = centro de la base."""
    luz, base, sombra = PIEDRA
    for i in range(4):                                                  # cuerpos del basamento
        w, h = (3.6 - 0.7 * i) * s, 0.75 * s
        yb = y - i * h
        lz.relleno(np.array([(x - w, yb), (x + w, yb), (x + w - 0.25 * s, yb - h), (x - w + 0.25 * s, yb - h)]), base, capa=capa)
        lz.relleno(np.array([(x + w * 0.35, yb), (x + w, yb), (x + w - 0.25 * s, yb - h), (x + w * 0.35, yb - h)]), sombra, alfa=0.7, capa=capa)
        lz.relleno(rect_red(x - w + 0.25 * s, yb - h, 2 * w - 0.5 * s, 0.12 * s, 0), luz, alfa=0.8, capa=capa)
    # escalinata
    lz.relleno(np.array([(x - 0.55 * s, y), (x + 0.55 * s, y), (x + 0.4 * s, y - 3.0 * s), (x - 0.4 * s, y - 3.0 * s)]), P.aclarar(base, 0.1), capa=capa)
    for k in range(10):
        yy = y - k * 0.3 * s
        lz.relleno(rect_red(x - 0.52 * s, yy - 0.05 * s, 1.04 * s, 0.05 * s, 0), sombra, alfa=0.6, capa=capa)
    top = y - 3.0 * s
    # bloques del templo: (x rel, y rel, w, h, color)
    bloques = [(-1.1, 0.0, 0.7, 0.55, base), (-0.4, 0.0, 0.8, 0.55, base), (0.4, 0.0, 0.7, 0.55, sombra), (-1.1, -0.55, 0.7, 0.55, base),
               (0.4, -0.55, 0.7, 0.55, sombra), (-0.4, -0.55, 0.8, 0.3, (60, 36, 50)), (-1.25, -1.1, 2.5, 0.35, (184, 74, 64)), (-0.9, -1.45, 1.8, 0.35, (214, 96, 76)),
               (-0.5, -1.8, 1.0, 0.35, (184, 74, 64))]
    for i, (bx, by, bw, bh, col) in enumerate(bloques):
        d = max(0.0, caida * 1.25 - 0.05 * (len(bloques) - 1 - i))          # los de arriba caen primero
        d = min(1.0, d)
        sd = 1 if h01(5, i) > 0.5 else -1
        dx = sd * (0.6 + 1.6 * h01(6, i)) * s * e_out(d)
        dy = 3.0 * s * e_in(d) * (0.8 + 0.4 * h01(7, i))
        rot = sd * 2.2 * d * (0.5 + h01(8, i))
        cx, cy = x + (bx + bw / 2) * s + dx, top + (by - bh / 2) * s + dy
        with lz.grupo(cx, cy, 1.0, rot):
            lz.relleno(rect_red(-bw / 2 * s, -bh / 2 * s, bw * s, bh * s, 0.05 * s), col, capa=capa)
            lz.relleno(rect_red(-bw / 2 * s, -bh / 2 * s, bw * s, 0.1 * s, 0), P.aclarar(col, 0.2), alfa=0.6, capa=capa)
    if 0.05 < caida < 1.6:                                                # polvo
        for k in range(14):
            u = (caida - 0.05) / 1.2
            a = (1 - min(1, u)) * 0.6
            px = x + (h01(9, k) - 0.5) * 6 * s * (0.3 + u)
            py = top - 0.2 * s + 1.4 * s * h01(10, k) - u * 1.5 * s
            lz.relleno(circulo(px, py, (0.5 + 1.2 * u) * s * (0.6 + 0.6 * h01(11, k)), 18), (226, 206, 190), alfa=a, capa=capa)


# ------------------------------------------------------------------------------------------------ olla tapada que hierve
def olla(lz, x, y, s, t, presion, fuego=1.0, capa=1):
    """Olla de barro sobre tres piedras y fuego; la tapa vibra y suelta vapor según `presion` 0..1. Origen = base de la olla. s ≈ px por unidad (olla ~5 u)."""
    # fuego y piedras (detrás de la olla)
    for k, dx in enumerate((-1.9, 0.0, 1.9)):
        lz.relleno(elipse(x + dx * s, y + 0.5 * s, 0.9 * s, 0.55 * s, 0, 18), (96, 70, 84), capa=capa)
        lz.relleno(elipse(x + dx * s - 0.15 * s, y + 0.35 * s, 0.6 * s, 0.3 * s, 0, 16), (130, 100, 110), capa=capa)
    if fuego > 0:
        for k in range(5):
            llama(lz, x + (k - 2) * 0.75 * s, y + 0.7 * s, 0.024 * s * (0.8 + 0.5 * presion) * (1.0 - 0.25 * abs(k - 2)), t, seed=k, alfa=fuego)
    # cuerpo de la olla
    temb = presion ** 2 * 0.06 * s
    ox = x + ruido1(t * 30, 1, 2) * temb
    q = np.array([(-1.6, 0.0), (-2.6, -0.8), (-3.0, -2.2), (-2.7, -3.5), (-2.0, -4.2), (-1.5, -4.5), (1.5, -4.5), (2.0, -4.2), (2.7, -3.5), (3.0, -2.2), (2.6, -0.8), (1.6, 0.0)])
    cuerpo = catmull(q * s + (ox, y), 8, True)
    lz.relleno(cuerpo, BARRO_S, capa=capa)
    with lz.recorte(cuerpo):
        lz.relleno(catmull(q * s * 0.95 + (ox - 0.35 * s, y - 0.15 * s), 8, True), BARRO, capa=capa)
        lz.relleno(elipse(ox - 1.4 * s, y - 2.9 * s, 0.7 * s, 1.1 * s, -0.4, 20), BARRO_L, alfa=0.7, capa=capa)
        # banda decorativa con grecas
        lz.relleno(rect_red(ox - 3.2 * s, y - 2.6 * s, 6.4 * s, 0.55 * s, 0), (120, 50, 50), capa=capa)
        for k in range(9):
            xx = ox - 2.8 * s + k * 0.7 * s
            lz.relleno(np.array([(xx, y - 2.1 * s), (xx + 0.35 * s, y - 2.5 * s), (xx + 0.7 * s, y - 2.1 * s)]), (240, 200, 120), alfa=0.85, capa=capa)
        # el barro se enrojece con la presión
        lz.relleno(cuerpo, (255, 80, 40), alfa=0.28 * presion ** 1.5, capa=capa)
    # boca y asas
    lz.relleno(elipse(ox, y - 4.5 * s, 1.7 * s, 0.38 * s, 0, 24), BARRO_S, capa=capa)
    for sd in (-1, 1):
        lz.trazo(np.array([(ox + sd * 2.55 * s, y - 3.4 * s), (ox + sd * 3.35 * s, y - 3.3 * s), (ox + sd * 3.3 * s, y - 2.6 * s), (ox + sd * 2.8 * s, y - 2.4 * s)]),
                 BARRO_S, 0.35 * s, afinar=False, temblor=0.0, capa=capa)
    # tapa que brinca
    salto = presion ** 2 * 0.45 * s * max(0.0, math.sin(t * (9 + 10 * presion))) ** 6
    rot = presion ** 2 * 0.12 * math.sin(t * 23)
    with lz.grupo(ox, y - 4.6 * s - salto, 1.0, rot):
        lz.relleno(elipse(0, 0, 1.95 * s, 0.42 * s, 0, 24), (110, 60, 60), capa=capa)
        lz.relleno(elipse(0, -0.2 * s, 1.8 * s, 0.38 * s, 0, 24), (170, 84, 64), capa=capa)
        lz.relleno(elipse(0, -0.55 * s, 0.38 * s, 0.25 * s, 0, 14), (110, 60, 60), capa=capa)
    # vapor que escapa por los lados de la tapa
    n = int(4 + 10 * presion)
    for k in range(n):
        ph = (t * (0.7 + 0.6 * presion) + h01(3, k)) % 1.0
        sd = -1 if k % 2 else 1
        px = ox + sd * (1.7 + 2.2 * ph) * s + 0.4 * s * math.sin(t * 2 + k)
        py = y - 4.7 * s - ph * (2.0 + 2.0 * presion) * s
        lz.relleno(circulo(px, py, (0.25 + 0.6 * ph) * s, 16), (244, 236, 255), alfa=(0.25 + 0.5 * presion) * (1 - ph) * min(1, ph * 5), capa=capa)
    # líneas de vibración
    if presion > 0.5:
        a = (presion - 0.5) * 2
        for sd in (-1, 1):
            for j in range(3):
                xx = ox + sd * (3.6 + 0.45 * j) * s
                lz.trazo(np.array([(xx, y - (3.4 - 0.3 * j) * s), (xx + sd * 0.3 * s, y - (2.6 - 0.3 * j) * s)]), (255, 236, 200), 0.14 * s, temblor=0.0, capa=capa, afinar=False)


def termometro(lz, x, y, h, nivel, t, capa=2, alfa=1.0):
    """Termómetro vertical (x, y = centro del bulbo); nivel 0..1 del amarillo al rojo, con marcas."""
    r = h * 0.11
    w = h * 0.07
    lz.relleno(rect_red(x - w - 6, y - h - 6, 2 * w + 12, h + 12, w + 6), (250, 244, 255), alfa=alfa, capa=capa)
    lz.relleno(circulo(x, y, r + 8, 28), (250, 244, 255), alfa=alfa, capa=capa)
    col = P.mezcla((255, 206, 70), (236, 50, 50), float(np.clip(nivel, 0, 1)))
    lz.relleno(circulo(x, y, r, 28), col, alfa=alfa, capa=capa)
    hh = (h - r) * float(np.clip(nivel, 0, 1)) + r * 0.6
    lz.relleno(rect_red(x - w * 0.55, y - hh, w * 1.1, hh, w * 0.55), col, alfa=alfa, capa=capa)
    for k in range(1, 6):
        yy = y - r - (h - r - 10) * k / 5.4
        lz.relleno(rect_red(x + w + 10, yy - 2, 20 if k % 2 else 32, 4, 2), (250, 244, 255), alfa=alfa * 0.8, capa=capa)
    lz.relleno(circulo(x - r * 0.35, y - r * 0.35, r * 0.25, 14), (255, 255, 255), alfa=alfa * 0.5, capa=capa)


# ------------------------------------------------------------------------------------------------ el peñol del Mixtón, de perfil
def penol(lz, t, cx=960, y_base=1000, ancho=760, alto=560, sube=0.0, fogatas=0.0, capa=1, gente=True):
    """Mesa rocosa de paredes casi verticales con estratos, vegetación en la cumbre, sendero en zigzag, gente que sube (sube 0..1) y fogatas."""
    x0, x1 = cx - ancho / 2, cx + ancho / 2
    top = y_base - alto
    # silueta con paredes casi verticales e irregulares
    izq = [(x0 - 60 + 22 * h01(1, i) + 30 * (i / 9) ** 3, y_base - alto * i / 9) for i in range(10)]
    der = [(x1 + 60 - 22 * h01(2, i) - 30 * (i / 9) ** 3, y_base - alto * i / 9) for i in range(10)][::-1]
    cima = [(x0 + (x1 - x0) * k / 8, top - 10 - 14 * h01(3, k)) for k in range(1, 8)]
    sil = np.array(izq + cima + der)
    lz.relleno(sil, (132, 82, 96), capa=capa)
    with lz.recorte(sil):
        cols = [(176, 110, 104), (158, 96, 98), (190, 124, 110), (146, 88, 96), (170, 104, 100)]
        for k in range(9):                                              # estratos horizontales con ondulación
            yy = top + alto * k / 9
            pts = [(x0 - 100 + 60 * j, yy + 8 * math.sin(j * 1.3 + k)) for j in range(16)]
            lz.relleno(np.array(pts + [(x1 + 100, yy + alto / 9 + 4), (x0 - 100, yy + alto / 9 + 4)]), cols[k % 5], alfa=0.9, capa=capa)
        lz.relleno(np.array([(cx + ancho * 0.12, top - 40), (x1 + 100, top - 40), (x1 + 100, y_base), (cx + ancho * 0.28, y_base)]), (90, 50, 80), alfa=0.35, capa=capa)
        for k in range(14):                                             # grietas verticales
            xx = x0 + ancho * h01(4, k)
            yy = top + alto * 0.1 + alto * 0.7 * h01(5, k)
            lz.trazo(np.array([(xx, yy), (xx + 6, yy + 40), (xx - 4, yy + 90)]), (100, 60, 80), 3.0, temblor=0.0, capa=capa)
    # vegetación en la cumbre: árboles, magueyes y nopales de alturas distintas
    for k in range(14):
        xx = x0 + 20 + (ancho - 40) * k / 13 + 14 * (h01(6, k) - 0.5)
        yy = top - 8 - 10 * h01(3, k % 8)
        tipo = k % 3
        if tipo == 0:
            r = 26 + 18 * h01(6, k)
            lz.relleno(rect_red(xx - 4, yy - r * 1.2, 8, r * 1.2, 3), (110, 70, 60), capa=capa)
            lz.relleno(circulo(xx, yy - r * 1.5, r, 18), (64, 128, 92), capa=capa)
            lz.relleno(circulo(xx - r * 0.3, yy - r * 1.8, r * 0.55, 14), (104, 176, 110), alfa=0.85, capa=capa)
        elif tipo == 1:
            for a_ in range(7):
                ang = -1.3 + 0.43 * a_
                L = 34 + 10 * h01(7, k, a_)
                lz.relleno(np.array([(xx - 5, yy), (xx + math.sin(ang) * L, yy - math.cos(ang) * L), (xx + 5, yy)]), (80, 150, 120) if a_ % 2 else (60, 126, 104), capa=capa)
        else:
            for (dx, dy, rx, ry) in ((0, -22, 14, 22), (-16, -48, 11, 17), (14, -50, 11, 17)):
                lz.relleno(elipse(xx + dx, yy + dy, rx, ry, 0.2 * dx / 16, 16), (90, 160, 100), capa=capa)
    # sendero en zigzag por la pared izquierda
    ruta = [(x0 - 130, y_base + 10), (x0 + 30, y_base - alto * 0.2), (x0 - 20, y_base - alto * 0.38), (x0 + 60, y_base - alto * 0.58), (x0 + 10, y_base - alto * 0.78), (x0 + 90, top - 6)]
    q = np.array(catmull(np.array(ruta, float), 10, False))
    lz.trazo(q, (226, 190, 150), 9.0, afinar=False, temblor=0.0, capa=capa)
    # fogatas y humo en la cima
    if fogatas > 0.01:
        for k, fx in enumerate((cx - 220, cx - 40, cx + 170, cx + 300)):
            fy = top - 4
            llama(lz, fx, fy, 0.32 * fogatas, t, seed=k + 3)
            humo(lz, fx, fy - 30, t, 0.0, n=5, s=0.5, alfa=0.35 * fogatas, seed=k)
    # gente que sube (siluetas pequeñas de 2 tonos) — posición sobre el sendero
    if gente and sube > 0.0:
        seg = np.hypot(*np.diff(q, axis=0).T)
        d = np.r_[0, np.cumsum(seg)]
        for i in range(16):
            f = sube * 1.1 - i * 0.05 + 0.04 * math.sin(t * 0.7 + i)
            if f <= 0 or f >= 1.02:
                continue
            f = min(f, 1.0)
            s_ = d[-1] * f
            j = int(np.clip(np.searchsorted(d, s_) - 1, 0, len(q) - 2))
            u = (s_ - d[j]) / max(1e-6, d[j + 1] - d[j])
            px, py = q[j] + (q[j + 1] - q[j]) * u
            dirx = 1 if q[j + 1][0] >= q[j][0] else -1
            K2.cuerpo(lz, px, py, 8.0, K2.variar("caxcana" if i % 3 == 1 else "caxcan", 60 + i), t, piernas="camina", brazos="balanceo", mirar=dirx, vista="perfil",
                      seed=i + 70, cara="ninguna", sombra=False, ph=t * 6 + i)
        # los que ya llegaron, de pie en la cima
        nn = int(np.clip((sube - 0.4) * 22, 0, 12))
        for i in range(nn):
            px = x0 + 140 + (ancho - 260) * h01(12, i)
            K2.cuerpo(lz, px, top - 6, 7.5, K2.variar("caxcan", 90 + i), t, piernas="idle", brazos="idle" if i % 3 else "arriba", mirar=1 if i % 2 else -1, vista="perfil",
                      seed=i + 90, cara="ninguna", sombra=False)


def flecha_altura(lz, x, y0, y1, texto=None, color=(255, 255, 255), alfa=1.0, capa=2):
    """Cota vertical con puntas de flecha (para «paredes casi verticales»)."""
    lz.trazo(np.array([(x, y0), (x, y1)]), color, 5.0, afinar=False, temblor=0.0, capa=capa)
    for yy, sd in ((y0, 1), (y1, -1)):
        lz.relleno(np.array([(x, yy), (x - 16, yy + sd * 26), (x + 16, yy + sd * 26)]), color, alfa=alfa, capa=capa)


# ------------------------------------------------------------------------------------------------ noche: emisarios con antorcha de pueblo en pueblo
NOCHE = ((58, 62, 128), (40, 42, 100), (28, 28, 72), (18, 16, 48))


def colinas_noche(lz, t, cx, y0=640, semilla=3):
    """Capas de lomas nocturnas con paralaje (cx = desplazamiento de cámara en px del plano cercano)."""
    for k, col in enumerate(NOCHE[:3]):
        par = 0.18 + 0.3 * k
        yb = y0 + 90 * k
        xs = np.linspace(-40, W + 40, 48)
        ys = [yb - 70 * (1 - 0.2 * k) * (0.5 + 0.5 * math.sin((x + cx * par) * 0.004 + k * 1.7 + semilla)) - 30 * math.sin((x + cx * par) * 0.011 + k) for x in xs]
        lz.relleno(np.array(list(zip(xs, ys)) + [(W + 40, H), (-40, H)]), col, capa=0)


def aldea_noche(lz, x, y, s, t, encendida, seed=0):
    """Cuatro chozas de adobe en silueta con puertas que brillan y una fogata que se enciende (encendida 0..1). Origen = suelo."""
    for i in range(4):
        xx = x + (i - 1.5) * 90 * s + 18 * s * (h01(seed, i) - 0.5)
        yy = y + 10 * s * (i % 2)
        w, h = (56 + 14 * h01(seed, i, 2)) * s, (44 + 10 * h01(seed, i, 3)) * s
        lz.relleno(rect_red(xx - w / 2, yy - h, w, h, 3 * s), (44, 40, 86), capa=1)
        lz.relleno(np.array([(xx - w / 2 - 8 * s, yy - h), (xx, yy - h - 34 * s), (xx + w / 2 + 8 * s, yy - h)]), (70, 56, 96), capa=1)
        luz = 0.35 + 0.65 * encendida
        lz.relleno(rect_red(xx - 9 * s, yy - 26 * s, 18 * s, 26 * s, 3 * s), (255, 200, 110), alfa=luz, capa=1)
        lz.halo(xx, yy - 14 * s, 50 * s, (255, 190, 100), alfa=0.25 * luz, capa=1)
    if encendida > 0.01:
        lz.halo(x, y - 30 * s, 260 * s * encendida, (255, 160, 70), alfa=0.35 * encendida, capa=1)
        llama(lz, x, y + 4 * s, 0.55 * s * encendida, t, seed=seed)
        for k in range(10):                                              # chispas que suben
            ph = (t * 0.8 + h01(seed, k, 5)) % 1.0
            lz.relleno(circulo(x + 30 * s * math.sin(t * 2 + k), y - 40 * s - ph * 200 * s, 3.5 * s * (1 - ph), 8), (255, 220, 140), alfa=encendida * (1 - ph), capa=1)


def antorcha_mano(D, m, ang, t, seed):
    """Objeto para K2.cuerpo(obj_d=...): antorcha de ocote encendida."""
    x, y = m
    D.poly([(x - 0.12, y + 0.6), (x + 0.12, y + 0.6), (x + 0.2, y - 1.6), (x - 0.04, y - 1.6)], (120, 76, 50))
    for k, (col, sc) in enumerate((((236, 70, 40), 1.0), ((255, 150, 40), 0.7), ((255, 230, 120), 0.4))):
        fl = 0.15 * math.sin(t * 13 + k + seed)
        D.cat([(x - 0.45 * sc + 0.08, y - 1.6), (x - 0.2 * sc + fl, y - 2.3 - 0.6 * sc), (x + 0.1 + fl * 1.5, y - 2.8 - 0.9 * sc), (x + 0.35 * sc + fl, y - 2.2 - 0.5 * sc),
               (x + 0.45 * sc, y - 1.6)], col, n=5)


_INS = {}


def inset_mapa(img, t, cam, luces, x=1440, y=46, w=430, h=250, titulo=None):
    """Recuadro con el mapa de relieve REAL (cam) en la esquina, con pueblos que se encienden. luces = [(lon, lat, brillo 0..1)]. Post-proceso numpy."""
    import cv2
    import kz_mapa as KM
    clave = (cam, w, h)
    if clave not in _INS:
        m = KM.MAPA.base(cam, 0.0, exag=12.0, rios_umbral=0.7)
        _INS[clave] = cv2.resize(np.ascontiguousarray(m), (w, h), interpolation=cv2.INTER_AREA) * np.float32((0.62, 0.68, 1.0)) * 0.85
    sub = _INS[clave].copy()
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    for lon, lat, b in luces:
        px, py = KM.MAPA.proy(cam, lon, lat)
        px, py = float(px) * w / W, float(py) * h / H
        r2 = (xx - px) ** 2 + (yy - py) ** 2
        sub += (np.exp(-r2 / (2 * (10 + 8 * b) ** 2)) * (0.15 + 0.85 * b))[..., None] * np.float32((1.0, 0.75, 0.35))
        sub[r2 < 20] = np.float32((1.0, 0.95, 0.8)) if b > 0.3 else np.float32((0.55, 0.55, 0.75))
    out = img.copy()
    b_ = 6
    out[y - b_:y + h + b_, x - b_:x + w + b_] = np.float32((0.96, 0.93, 1.0))
    out[y:y + h, x:x + w] = np.clip(sub, 0, 1)
    return out


def matorral_noche(lz, cx, y=H, n=9, seed=7):
    """Primer plano nocturno en silueta (magueyes, nopales, hierba) con paralaje fuerte (cx en px)."""
    col = (10, 8, 30)
    for i in range(n):
        x = ((i * 330 + 140 * h01(seed, i) - cx) % (W + 600)) - 300
        if i % 3 == 0:
            for a in range(9):
                ang = -1.35 + 0.34 * a
                L = 120 + 60 * h01(seed, i, a)
                lz.relleno(np.array([(x - 10, y), (x + math.sin(ang) * L, y - math.cos(ang) * L), (x + 10, y)]), col, capa=2)
        elif i % 3 == 1:
            for dx, dy, rx, ry in ((0, -60, 38, 62), (-44, -140, 30, 46), (40, -150, 30, 46), (0, -200, 26, 40)):
                lz.relleno(elipse(x + dx, y + dy, rx, ry, 0.15 * dx / 40, 18), col, capa=2)
        else:
            for k in range(12):
                xx = x + (k - 6) * 14
                lz.relleno(np.array([(xx - 5, y), (xx + 8 * math.sin(k), y - 70 - 40 * h01(seed, i, k)), (xx + 5, y)]), col, capa=2)
