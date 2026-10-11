# -*- coding: utf-8 -*-
"""Mundos 2D de la escena 1 (gancho) y motivos de agua que se repiten en el video: gota, espuma, vapor, poza termal, hacienda 2D,
peñol en llamas y la lupa con el tramo Juchipila–Apozol–Jalpa de la carretera."""
import math

import numpy as np

import kz_ui as U
import plano as P
from motor import circulo, elipse, rect_red, catmull, h01, prog, smooth, e_out, e_back, e_inout, W, H

AZUL = (66, 156, 236)
CIAN = (112, 224, 236)
ESPUMA = (244, 252, 255)
CALIDO = (255, 150, 70)


def gota(lz, x, y, r, t, k=1.0, alfa=1.0, capa=2, col=AZUL, seed=0, brillo=True):
    """Gota de agua con la punta arriba (2 tonos y brillo). (x, y) = centro del cuerpo; r = radio del cuerpo."""
    if k <= 0.01 or alfa <= 0.01:
        return
    r = r * k
    y = y + math.sin(t * 1.8 + seed) * 0.05 * r
    d = 2.1 * r
    arc = [(x + r * math.cos(a), y + r * math.sin(a)) for a in np.linspace(math.radians(-28.4), math.radians(208.4), 28)]
    pts = np.array([(x, y - d)] + arc)
    lz.halo(x, y, r * 2.2, col, alfa=0.25 * alfa, dureza=1.3, capa=capa)
    lz.degradado(pts, P.aclarar(col, 0.28), P.oscurecer(col, 0.30), (x - r * 0.9, y - d * 0.6), (x + r * 0.8, y + r), capa=capa, alfa=alfa)
    if brillo:
        lz.relleno(elipse(x - 0.40 * r, y - 0.15 * r, 0.15 * r, 0.34 * r, -0.5, 14), (255, 255, 255), alfa=0.85 * alfa, capa=capa)


def espuma(lz, x, y, w, t, k=1.0, n=24, seed=0, alfa=1.0, capa=2, col=ESPUMA):
    """Racimo de burbujas de espuma sobre una línea (x = centro, y = base); más alto al centro."""
    if k <= 0.01:
        return
    orden = sorted(range(n), key=lambda i: -h01(seed, i, 3))
    for i in orden:
        u = h01(seed, i, 1)
        env = 1 - abs(u - 0.5) * 2
        r = (7 + 20 * h01(seed, i, 2)) * k * (0.55 + 0.7 * env)
        bx = x + (u - 0.5) * w
        by = y - r * 0.5 - 34 * env * h01(seed, i, 3) * k + 3 * math.sin(t * 2.2 + i)
        lz.relleno(circulo(bx, by, r, 14), P.oscurecer(col, 0.10) if i % 3 == 0 else col, alfa=0.96 * alfa, capa=capa)
        lz.relleno(circulo(bx - r * 0.30, by - r * 0.32, r * 0.34, 10), (255, 255, 255), alfa=0.9 * alfa, capa=capa)


def agua_con_espuma(lz, x0, x1, y0, t, k=1.0, seed=0, capa=1, n_burb=52):
    """Masa de agua con la cresta cubierta de espuma (burbujas blancas que se desplazan). y0 = cresta; llena hasta el borde inferior."""
    if k <= 0.01:
        return
    cresta = lambda x: y0 + 9 * math.sin(x * 0.011 + t * 1.3) + 5 * math.sin(x * 0.027 - t * 1.9)
    xs = np.linspace(x0, x1, 26)
    poli = np.array([(x, cresta(x)) for x in xs] + [(x1, H + 10), (x0, H + 10)])
    lz.degradado(poli, (96, 188, 246), (14, 58, 160), (0, y0 - 10), (0, H), capa=capa)
    for j in range(3):                                                  # estelas claras que avanzan
        yy = y0 + 70 + 60 * j
        pts = [(x, yy + 7 * math.sin(x * 0.013 + t * (0.9 + 0.2 * j) + j)) for x in np.linspace(x0, x1, 26)]
        lz.trazo(np.array(pts), (214, 244, 255, 150), 4.0, afinar=False, temblor=0.0, capa=capa)
    for i in range(n_burb):
        u = (h01(seed, i, 1) + t * 0.015) % 1.0
        x = x0 + (x1 - x0) * u
        r = (7 + 19 * h01(seed, i, 2)) * k
        by = cresta(x) - r * 0.30 + 5 * math.sin(t * 2.3 + i)
        lz.relleno(circulo(x, by, r, 14), ESPUMA if i % 3 else (214, 238, 252), alfa=0.97, capa=capa + 1)
        lz.relleno(circulo(x - r * 0.3, by - r * 0.3, r * 0.32, 10), (255, 255, 255), alfa=0.9, capa=capa + 1)


def vapor(lz, x, y, t, n=7, s=1.0, alfa=0.6, ancho=70.0, alto=240.0, seed=0, col=(252, 248, 242), capa=2):
    """Columna de vapor: bocanadas que suben, crecen y se desvanecen."""
    for i in range(n):
        u = (t * 0.22 + i / n + h01(seed, i, 1) * 0.3) % 1.0
        px = x + (h01(seed, i, 2) - 0.5) * ancho * s + 26 * s * math.sin(u * 6 + i)
        py = y - u * alto * s
        r = (14 + 38 * u) * s
        lz.relleno(circulo(px, py, r, 18), col, alfa=alfa * (1 - u) * min(1.0, u * 6), capa=capa)


def poza(lz, x, y, rx, ry, t, k=1.0, capa=1, seed=0, vapor_=True, alfa=1.0):
    """Poza de aguas termales vista en 3/4: borde de piedras, agua turquesa con destellos, ondas y vapor. (x, y) = centro del agua."""
    if k <= 0.01:
        return
    rx, ry = rx * k, ry * k
    lz.relleno(elipse(x, y + ry * 0.22, rx * 1.18, ry * 1.24, 0, 40), (70, 52, 70), alfa=0.30 * alfa, capa=capa)               # sombra
    lz.relleno(elipse(x, y + 0.10 * ry, rx * 1.12, ry * 1.18, 0, 40), (168, 150, 150), alfa=alfa, capa=capa)                    # borde de roca
    lz.relleno(elipse(x, y, rx * 1.06, ry * 1.08, 0, 40), (206, 190, 186), alfa=alfa, capa=capa)
    lz.degradado(elipse(x, y, rx, ry, 0, 40), (126, 236, 232), (28, 150, 214), (x, y - ry), (x, y + ry), capa=capa, alfa=alfa)
    for j in range(3):                                                                                                         # ondas
        u = (t * 0.35 + j / 3.0 + 0.2 * seed) % 1.0
        lz.relleno(elipse(x + 0.15 * rx * math.sin(j * 2.1 + seed), y + 0.1 * ry, rx * (0.2 + 0.7 * u), ry * (0.2 + 0.7 * u), 0, 32), (255, 255, 255),
                   alfa=0.16 * (1 - u) * alfa, capa=capa)
    for i in range(9):                                                                                                         # destellos
        a = h01(seed, i, 1) * 6.28
        rr = 0.75 * math.sqrt(h01(seed, i, 2))
        c = 0.5 + 0.5 * math.sin(t * 3 + i * 1.7)
        lz.relleno(elipse(x + math.cos(a) * rr * rx, y + math.sin(a) * rr * ry, 14 + 12 * c, 3 + 2 * c, 0, 12), (255, 255, 255), alfa=0.55 * c * alfa, capa=capa)
    for i in range(14):                                                                                                        # piedras del borde (delante)
        a = i * 2 * math.pi / 14 + 0.2 * h01(seed, i, 4)
        sx, sy = x + math.cos(a) * rx * 1.08, y + math.sin(a) * ry * 1.10
        r = (16 + 12 * h01(seed, i, 5)) * min(rx, ry * 2) / 120
        c = [(176, 160, 160), (150, 134, 140), (196, 182, 178)][i % 3]
        lz.relleno(elipse(sx, sy, r * 1.25, r * 0.95, 0, 14), P.oscurecer(c, 0.25), alfa=alfa, capa=capa)
        lz.relleno(elipse(sx - r * 0.1, sy - r * 0.18, r * 1.15, r * 0.82, 0, 14), c, alfa=alfa, capa=capa)
    if vapor_:
        vapor(lz, x, y - 0.2 * ry, t, n=10, s=rx / 130.0, ancho=rx * 1.1, alto=rx * 1.9, alfa=0.85 * alfa, seed=seed, capa=capa + 1)


def hacienda2d(lz, x, y, s, capa=1, alfa=1.0, ocre=(236, 190, 120)):
    """Casa grande de hacienda en 2D: muro largo con arcos, techo de teja, torre con campana y cruz. (x, y) = centro de la base."""
    k = s
    cs = P.oscurecer(ocre, 0.22)
    lz.relleno(rect_red(x - 150 * k, y - 84 * k, 300 * k, 84 * k, 0), ocre, alfa=alfa, capa=capa)
    lz.relleno(np.array([(x + 100 * k, y - 84 * k), (x + 150 * k, y - 84 * k), (x + 150 * k, y), (x + 100 * k, y)]), cs, alfa=alfa, capa=capa)
    lz.relleno(np.array([(x - 164 * k, y - 80 * k), (x + 164 * k, y - 80 * k), (x + 140 * k, y - 112 * k), (x - 140 * k, y - 112 * k)]), (196, 84, 70), alfa=alfa, capa=capa)
    lz.relleno(np.array([(x - 164 * k, y - 80 * k), (x + 164 * k, y - 80 * k), (x + 164 * k, y - 74 * k), (x - 164 * k, y - 74 * k)]), (150, 56, 56), alfa=alfa, capa=capa)
    for i in range(7):                                                      # portal con arcos
        ax = x - 120 * k + 40 * k * i
        lz.relleno(rect_red(ax - 13 * k, y - 56 * k, 26 * k, 56 * k, 12 * k), (94, 52, 60), alfa=alfa, capa=capa)
    for i in range(3):                                                      # ventanas altas
        ax = x - 80 * k + 80 * k * i
        lz.relleno(rect_red(ax - 7 * k, y - 76 * k, 14 * k, 14 * k, 2 * k), (255, 214, 120), alfa=0.9 * alfa, capa=capa)
    # torre-campanario
    tx = x + 120 * k
    lz.relleno(rect_red(tx - 20 * k, y - 190 * k, 40 * k, 110 * k, 0), ocre, alfa=alfa, capa=capa)
    lz.relleno(np.array([(tx + 8 * k, y - 190 * k), (tx + 20 * k, y - 190 * k), (tx + 20 * k, y - 80 * k), (tx + 8 * k, y - 80 * k)]), cs, alfa=alfa, capa=capa)
    lz.relleno(rect_red(tx - 9 * k, y - 172 * k, 18 * k, 26 * k, 8 * k), (70, 40, 60), alfa=alfa, capa=capa)
    lz.relleno(circulo(tx, y - 160 * k, 5 * k, 10), (255, 206, 72), alfa=alfa, capa=capa)
    lz.relleno(np.array([(tx - 24 * k, y - 190 * k), (tx + 24 * k, y - 190 * k), (tx, y - 224 * k)]), (196, 84, 70), alfa=alfa, capa=capa)
    lz.relleno(rect_red(tx - 1.5 * k, y - 252 * k, 3 * k, 30 * k, 0), (250, 244, 230), alfa=alfa, capa=capa)
    lz.relleno(rect_red(tx - 8 * k, y - 244 * k, 16 * k, 3 * k, 0), (250, 244, 230), alfa=alfa, capa=capa)


def penol_fuego(lz, x, y, s, t, capa=1, alfa=1.0, fuego=1.0):
    """Peñol de paredes casi verticales (silueta violeta en 3 tonos) con fogatas y humo. (x, y) = centro de la base."""
    k = s
    cuerpo = [(-230, 0), (-200, -120), (-150, -250), (-110, -330), (-60, -360), (60, -362), (116, -330), (156, -240), (206, -118), (240, 0)]
    pts = np.array([(x + px * k, y + py * k) for px, py in cuerpo])
    lz.relleno(pts, (92, 56, 118), alfa=alfa, capa=capa)
    sh = np.array([(x + px * k, y + py * k) for px, py in [(40, -362), (116, -330), (156, -240), (206, -118), (240, 0), (60, 0), (70, -150)]])
    lz.relleno(sh, (62, 36, 88), alfa=alfa, capa=capa)
    for yy in (-70, -150, -240):                                                 # estratos
        lz.relleno(np.array([(x - 230 * k, y + (yy - 6) * k), (x + 240 * k, y + (yy - 10) * k), (x + 240 * k, y + (yy + 6) * k), (x - 230 * k, y + (yy + 2) * k)]),
                   (50, 30, 74), alfa=0.22 * alfa, capa=capa)
    lz.relleno(np.array([(x - 60 * k, y - 362 * k), (x + 60 * k, y - 364 * k), (x + 70 * k, y - 352 * k), (x - 70 * k, y - 350 * k)]), (124, 150, 96), alfa=alfa, capa=capa)   # tope verde
    for i, fx in enumerate((-40, 10, 50)):                                       # fogatas arriba
        if fuego > 0.01:
            fy = y - 362 * k
            for j, (col, sc) in enumerate((((236, 60, 48), 1.0), ((255, 138, 40), 0.7), ((255, 224, 96), 0.4))):
                a = 26 * k * sc * fuego * (1 + 0.2 * math.sin(t * 9 + i * 2 + j))
                px = x + fx * k
                lz.relleno(np.array([(px - 8 * k * sc, fy), (px + 8 * k * sc, fy), (px + 2 * k * math.sin(t * 7 + i), fy - a * 1.6)]), col, alfa=alfa, capa=capa)
            for q in range(4):
                u = ((t * 0.3 + q / 4 + i * 0.2) % 1.0)
                lz.relleno(circulo(x + fx * k + 14 * k * math.sin(u * 5 + i), fy - 30 * k - u * 150 * k, (8 + 22 * u) * k, 14), (70, 52, 84), alfa=0.5 * (1 - u) * alfa, capa=capa)


def lupa_carretera(lz, cx, cy, R, t, k=1.0, t_juch=1e9, t_jalpa=1e9, t_carr=1e9, t_apozol=1e9, t_nombres=1e9, alfa=1.0, nombres=True):
    """Lupa con el tramo Juchipila (S) – Apozol – Jalpa (N) de la carretera federal 54 junto al río, en vector plano."""
    if k <= 0.01:
        return
    R = R * k
    ring = circulo(cx, cy, R, 56)
    lz.relleno(circulo(cx + 10, cy + 14, R + 10, 56), (20, 10, 50), alfa=0.35 * alfa, capa=1)
    with lz.recorte(ring):
        lz.degradado(ring, (196, 226, 150), (110, 184, 118), (cx, cy - R), (cx, cy + R), capa=1, alfa=alfa)
        for i in range(10):                                                         # manchones de campo
            bx, by = cx - R + 2 * R * h01(81, i, 1), cy - R + 2 * R * h01(81, i, 2)
            lz.relleno(elipse(bx, by, 60 + 60 * h01(81, i, 3), 26 + 22 * h01(81, i, 4), 0.3, 18), P.oscurecer((150, 200, 120), 0.12 * (i % 3)), alfa=0.55 * alfa, capa=1)
        for sgn, ax in ((-1, cx - R), (1, cx + R)):                                  # sierras a los lados
            pts = [(ax + sgn * 0, cy - R - 10)] + [(ax - sgn * (110 + 50 * math.sin(v * 3.2 + (1 if sgn > 0 else 0)) + 40 * h01(82, int(v * 10))), cy - R + v * 2 * R) for v in np.linspace(0, 1, 12)] + [(ax, cy + R + 10)]
            lz.relleno(np.array(pts), (150, 110, 150) if sgn < 0 else (132, 96, 140), alfa=0.85 * alfa, capa=1)
        rio = [(cx - 40, cy + 340), (cx - 10, cy + 200), (cx + 50, cy + 70), (cx + 70, cy - 60), (cx + 130, cy - 180), (cx + 190, cy - 340)]
        q = np.array(catmull(np.array(rio, float), 10, False))
        lz.trazo(q, (60, 150, 226), 26.0, afinar=False, temblor=0.0, capa=1)
        lz.trazo(q, (140, 214, 246), 10.0, afinar=False, temblor=0.0, capa=1)
        via = [(cx - 190, cy + 330), (cx - 110, cy + 200), (cx - 40, cy + 100), (cx + 6, cy + 4), (cx - 24, cy - 110), (cx + 36, cy - 210), (cx + 84, cy - 340)]
        v = np.array(catmull(np.array(via, float), 10, False))
        f = smooth(prog(t, t_carr - 0.1, t_carr + 1.5))
        n = max(2, int(len(v) * f))
        if f > 0.01:
            lz.trazo(v[:n], (48, 40, 70), 22.0, afinar=False, temblor=0.0, capa=1)
            lz.trazo(v[:n], (232, 226, 214), 16.0, afinar=False, temblor=0.0, capa=1)
            P.discontinua(lz, v[:n], (252, 200, 60), ancho=3.0, largo=18.0, hueco=14.0, fase=-t * 40.0, capa=1)
        # los tres pueblos
        for nombre, (px, py), t0, col in (("Juchipila", (cx - 112, cy + 202), t_juch, U.COL["morado"]), ("Apozol", (cx + 4, cy + 8), t_apozol, U.COL["naranja"]),
                                          ("Jalpa", (cx + 28, cy - 196), t_jalpa, U.COL["teal"])):
            kk = e_back(prog(t, t0, t0 + 0.4)) if t >= t0 else 0.0
            if kk <= 0.01:
                continue
            grande = nombre == "Apozol"
            for j, (ox, oy, sc) in enumerate(((-34, 6, 0.9), (30, 10, 0.8), (0, -14, 1.0), (60, -6, 0.7), (-64, -8, 0.7))):
                P.casa(lz, px + ox * kk, py + oy * kk, (0.62 if grande else 0.46) * sc * kk, calor=0.4, oscuro=0.0)
            if grande:
                u = ((t - t0) * 0.9) % 1.6
                lz.trazo(elipse(px, py - 6, 40 + 120 * u, 26 + 80 * u, 0, 36), (255, 214, 90, int(230 * (1 - u / 1.6) * alfa)), 4.0, cerrado=True, afinar=False, temblor=0.0, capa=2)
    lz.trazo(ring, (255, 206, 72), 12.0, cerrado=True, afinar=False, temblor=0.0, capa=2)
    lz.trazo(ring, (255, 244, 200), 3.0, cerrado=True, afinar=False, temblor=0.0, capa=2)
    if nombres:
        for nombre, (px, py), t0, col in (("Juchipila", (cx - 112, cy + 270), t_juch, U.COL["morado"]), ("Apozol", (cx + 4, cy - 70), t_apozol, U.COL["naranja"]),
                                          ("Jalpa", (cx + 28, cy - 250), t_jalpa, U.COL["teal"])):
            kk = U.pop(t, t0 + 0.1)
            if kk > 0.01:
                U.llamada(lz, px, py, nombre, color=col, px=46 if nombre == "Apozol" else 40, k=kk * alfa, cola=None)
