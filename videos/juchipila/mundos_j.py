# -*- coding: utf-8 -*-
"""Mundos 2D de la escena 9 (el castigo), en paleta sobria gris-violeta y sin mostrar violencia: iconos duotono (cañón, perro, espada),
la mina en corte con cautivos que trabajan, el pueblo en ruinas, la ciudad del cerro que se desvanece sobre un refugio escondido,
la sala del Consejo de Indias con la lupa sobre el virrey, y la encrucijada sierra/valle."""
import math

import numpy as np

import plano as P
import kz_pers2d as K2
from motor import circulo, elipse, rect_red, catmull, h01, prog, smooth, e_out, e_in, e_back, e_inout, ruido1, W, H
from util import llama, humo, degradado_v

DUO = ((236, 228, 246), (150, 136, 186))      # luz, sombra de los iconos duotono
ROJO_G = (214, 80, 96)


# ------------------------------------------------------------------------------------------------ iconos duotono
def icono_canon(lz, x, y, s, alfa=1.0, capa=2):
    luz, som = DUO
    with lz.grupo(x, y, 1.0, -0.25):
        lz.relleno(rect_red(-2.6 * s, -0.55 * s, 4.6 * s, 1.1 * s, 0.5 * s), som, alfa=alfa, capa=capa)
        lz.relleno(rect_red(-2.6 * s, -0.55 * s, 4.6 * s, 0.45 * s, 0.4 * s), luz, alfa=alfa, capa=capa)
        lz.relleno(circulo(2.1 * s, 0, 0.62 * s, 18), som, alfa=alfa, capa=capa)
        lz.relleno(circulo(2.1 * s, 0, 0.32 * s, 14), (40, 30, 56), alfa=alfa, capa=capa)
    lz.relleno(circulo(x - 0.6 * s, y + 0.9 * s, 1.0 * s, 24), som, alfa=alfa, capa=capa)
    lz.relleno(circulo(x - 0.6 * s, y + 0.9 * s, 0.55 * s, 18), luz, alfa=alfa, capa=capa)
    for k in range(6):
        a = k * math.pi / 3
        lz.trazo(np.array([(x - 0.6 * s, y + 0.9 * s), (x - 0.6 * s + math.cos(a) * 0.95 * s, y + 0.9 * s + math.sin(a) * 0.95 * s)]), som, 0.14 * s, afinar=False, temblor=0.0, capa=capa)


def icono_perro(lz, x, y, s, t=0.0, alfa=1.0, capa=2):
    """Mastín de perfil en silueta duotono (mirando a la izquierda)."""
    luz, som = DUO
    resp = 0.05 * s * math.sin(t * 3)
    cuerpo = [(1.9, -0.2), (1.2, -1.2), (-0.8, -1.3), (-1.6, -1.0), (-1.9, -0.2), (-1.4, 0.4), (1.4, 0.4)]
    lz.relleno(np.array(catmull(np.array([(x + a * s, y + b * s + resp) for a, b in cuerpo]), 6, True)), som, alfa=alfa, capa=capa)
    cab = [(-1.4, -1.0), (-1.8, -2.0), (-2.6, -2.0), (-3.2, -1.5), (-3.0, -1.1), (-2.2, -0.9)]
    lz.relleno(np.array(catmull(np.array([(x + a * s, y + b * s) for a, b in cab]), 6, True)), som, alfa=alfa, capa=capa)
    lz.relleno(np.array([(x - 1.9 * s, y - 2.0 * s), (x - 1.6 * s, y - 2.5 * s), (x - 1.5 * s, y - 1.9 * s)]), som, alfa=alfa, capa=capa)
    for dx in (-1.4, -0.9, 1.0, 1.5):
        lz.relleno(rect_red(x + dx * s - 0.17 * s, y, 0.34 * s, 1.5 * s, 0.12 * s), som, alfa=alfa, capa=capa)
    lz.relleno(np.array([(x + 1.8 * s, y - 0.6 * s), (x + 2.8 * s, y - 1.5 * s + 0.2 * s * math.sin(t * 6)), (x + 2.9 * s, y - 1.3 * s), (x + 1.9 * s, y - 0.3 * s)]), som, alfa=alfa, capa=capa)
    lz.relleno(np.array(catmull(np.array([(x + a * s, y + b * s + resp) for a, b in [(1.6, -0.9), (-0.6, -1.15), (-1.4, -0.8), (0.4, -0.6)]]), 6, True)), luz, alfa=alfa * 0.7, capa=capa)
    lz.relleno(circulo(x - 2.5 * s, y - 1.65 * s, 0.12 * s, 8), (40, 30, 56), alfa=alfa, capa=capa)


def icono_espada(lz, x, y, s, alfa=1.0, capa=2):
    luz, som = DUO
    with lz.grupo(x, y, 1.0, 0.6):
        lz.relleno(np.array([(-0.22 * s, -0.6 * s), (0.22 * s, -0.6 * s), (0.12 * s, -4.4 * s), (0, -4.8 * s), (-0.12 * s, -4.4 * s)]), luz, alfa=alfa, capa=capa)
        lz.relleno(np.array([(0, -0.6 * s), (0.22 * s, -0.6 * s), (0.12 * s, -4.4 * s), (0, -4.8 * s)]), som, alfa=alfa * 0.6, capa=capa)
        lz.relleno(rect_red(-1.2 * s, -0.7 * s, 2.4 * s, 0.32 * s, 0.15 * s), som, alfa=alfa, capa=capa)
        lz.relleno(rect_red(-0.16 * s, -0.4 * s, 0.32 * s, 1.4 * s, 0.1 * s), (110, 90, 130), alfa=alfa, capa=capa)
        lz.relleno(circulo(0, 1.1 * s, 0.3 * s, 12), som, alfa=alfa, capa=capa)


# ------------------------------------------------------------------------------------------------ la mina en corte
def mina_corte(lz, t, cx=0.0, y_sup=520):
    """Montaña cortada con galerías: entrada con marco de madera arriba a la izquierda, túneles con lámparas y cautivos que cargan mineral."""
    pts = [(-60, y_sup + 40), (300, y_sup - 160), (700, y_sup - 260), (1080, y_sup - 120), (1500, y_sup - 230), (1980, y_sup - 60), (1980, H + 40), (-60, H + 40)]
    lz.relleno(np.array(pts), (92, 76, 104), capa=1)
    for k, col in enumerate(((104, 86, 116), (84, 68, 98), (98, 80, 110))):
        yy = y_sup + 120 + 150 * k
        lz.relleno(np.array([(-60, yy), *[(x, yy + 18 * math.sin(x * 0.006 + k)) for x in range(0, 2000, 100)], (1980, yy + 120), (-60, yy + 120)]), col, alfa=0.7, capa=1)
    # galerías (túneles) en zigzag
    gal = [((220, 610), (900, 640)), ((900, 640), (1000, 800)), ((420, 810), (1500, 800)), ((1500, 800), (1560, 960)), ((300, 980), (1700, 970))]
    for (a, b) in gal:
        lz.trazo(np.array([a, b]), (36, 26, 44), 96.0, afinar=False, temblor=0.0, capa=1)
        lz.trazo(np.array([(a[0], a[1] + 30), (b[0], b[1] + 30)]), (54, 42, 60), 30.0, afinar=False, temblor=0.0, capa=1)
    # vigas
    for (a, b) in gal:
        for u in np.linspace(0.08, 0.92, 6):
            x, y = a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u
            lz.relleno(rect_red(x - 7, y - 46, 14, 92, 2), (130, 92, 70), capa=1)
            lz.relleno(rect_red(x - 30, y - 50, 60, 12, 2), (150, 106, 80), capa=1)
    # entrada
    lz.relleno(rect_red(150, 520, 150, 150, 8), (30, 20, 40), capa=1)
    for xx in (150, 286):
        lz.relleno(rect_red(xx, 510, 16, 170, 2), (150, 106, 80), capa=1)
    lz.relleno(rect_red(136, 500, 180, 22, 4), (170, 120, 88), capa=1)
    # lámparas que titilan
    for k, (x, y) in enumerate(((560, 600), (980, 720), (800, 790), (1300, 800), (700, 960), (1300, 960))):
        f = 0.8 + 0.2 * math.sin(t * 9 + k * 2)
        lz.halo(x, y, 170 * f, (255, 190, 110), alfa=0.5, capa=1)
        lz.relleno(circulo(x, y, 8, 10), (255, 220, 150), capa=1)
    # mineros cautivos: cargan mineral por las galerías (cabeza baja, sin cara)
    for i, (a, b) in enumerate(gal):
        if a[1] == b[1] or abs(b[1] - a[1]) < 40:
            for j in range(3):
                u = ((t * 0.05 + j / 3 + 0.17 * i) % 1.0)
                x = a[0] + (b[0] - a[0]) * u
                y = a[1] + (b[1] - a[1]) * u + 44
                spec = dict(K2.variar("caxcan", 1100 + i * 3 + j), ropa=(120, 112, 150), ropa2=(150, 140, 170), tocado=None)
                K2.cuerpo(lz, x, y, 15, spec, t, piernas="camina", brazos="carga", mirar=1 if b[0] > a[0] else -1, vista="perfil", seed=1100 + i * 3 + j, cara="ninguna",
                          sombra=False, ph=t * 4 + j, lean=0.2)


# ------------------------------------------------------------------------------------------------ pueblo en ruinas
def casa_ruina(lz, x, y, s, seed=0, humo_t=None, t=0.0):
    """Casita de adobe sin techo, con muros rotos y vigas caídas."""
    w, h = 90 * s, 60 * s
    perfil = [(x - w / 2, y), (x - w / 2, y - h * 0.7), (x - w / 4, y - h * (0.9 + 0.2 * h01(seed, 1))), (x, y - h * 0.5), (x + w / 5, y - h * (0.8 + 0.2 * h01(seed, 2))),
              (x + w / 2, y - h * 0.4), (x + w / 2, y)]
    lz.relleno(np.array(perfil), (150, 132, 150), capa=1)
    lz.relleno(np.array([(x + w / 6, y), (x + w / 2, y), (x + w / 2, y - h * 0.4), (x + w / 5, y - h * 0.75)]), (120, 104, 126), capa=1)
    lz.relleno(rect_red(x - 12 * s, y - 34 * s, 24 * s, 34 * s, 3 * s), (54, 40, 60), capa=1)
    lz.relleno(rect_red(x - w / 2 - 10 * s, y - 8 * s, w * 0.8, 6 * s, 2), (110, 84, 76), capa=1)
    with lz.grupo(x + w * 0.3, y - h * 0.2, 1.0, -0.6):
        lz.relleno(rect_red(-30 * s, -3 * s, 60 * s, 6 * s, 2), (110, 84, 76), capa=1)
    for k in range(4):
        lz.relleno(elipse(x - w / 2 + 20 * s * k, y + 2, 10 * s, 5 * s, 0, 10), (130, 116, 134), capa=1)
    if humo_t is not None:
        humo(lz, x, y - h * 0.6, t, humo_t, n=6, s=0.6 * s, alfa=0.45, seed=seed, col=(90, 80, 100))


# ------------------------------------------------------------------------------------------------ la ciudad del cerro que se desvanece / refugio escondido
def ciudad_fantasma(lz, x, y, s, alfa, t=0.0):
    """Contorno luminoso de la antigua ciudad de la montaña (muros con ventanas, pirámide, chozas) — un recuerdo."""
    if alfa <= 0.01:
        return
    col = (255, 214, 140)
    q = []
    for i in range(5):
        w, h = (3.4 - 0.6 * i) * s, 0.55 * s
        yb = y - i * h
        q.append(np.array([(x - w, yb), (x + w, yb), (x + w - 0.2 * s, yb - h), (x - w + 0.2 * s, yb - h)]))
    for p in q:
        lz.trazo(p, col, 4.0, cerrado=True, temblor=0.0, capa=1, afinar=False)
        lz.relleno(p, col, alfa=0.10 * alfa, capa=1)
    for k in range(6):
        xx = x - 6 * s + 1.0 * s * k
        lz.trazo(np.array([(xx, y - 1.6 * s), (xx, y - 2.3 * s), (xx + 0.5 * s, y - 2.3 * s), (xx + 0.5 * s, y - 1.6 * s)]), col, 3.0, temblor=0.0, capa=1, afinar=False)
    lz.halo(x, y - 1.5 * s, 4 * s, col, alfa=0.25 * alfa, capa=1)
    for k in range(18):                                                 # se deshace en motas que suben
        ph = (t * 0.3 + h01(4, k)) % 1.0
        lz.relleno(circulo(x + (h01(5, k) - 0.5) * 8 * s, y - 2 * s - ph * 3 * s, 4 * (1 - ph), 8), col, alfa=alfa * (1 - ph), capa=1)


def refugio(lz, x, y, s, t, alfa=1.0):
    """Abrigo rocoso con una fogata pequeña y una familia sentada (escondidos)."""
    roca = [(x - 260 * s, y), (x - 240 * s, y - 120 * s), (x - 120 * s, y - 210 * s), (x + 80 * s, y - 220 * s), (x + 240 * s, y - 140 * s), (x + 300 * s, y)]
    lz.relleno(np.vstack([np.array(catmull(np.array(roca, float), 6, False)), [(x + 300 * s, y + 20), (x - 260 * s, y + 20)]]), (70, 58, 90), alfa=alfa, capa=1)
    lz.relleno(elipse(x + 10 * s, y - 40 * s, 200 * s, 90 * s, 0, 30), (30, 22, 44), alfa=alfa, capa=1)
    lz.halo(x, y - 30 * s, 220 * s, (255, 160, 80), alfa=0.35 * alfa, capa=1)
    llama(lz, x, y - 6 * s, 0.35 * s, t, seed=3, alfa=alfa)
    for i, (dx, tipo, mirar) in enumerate(((-130, "anciano_caxcan", 1), (-70, "caxcana", 1), (90, "caxcan", -1), (140, "nino", -1))):
        K2.cuerpo(lz, x + dx * s, y - 4 * s, 15 * s, tipo, t, piernas="sentado", brazos="idle", mirar=mirar, vista="perfil", seed=1200 + i, emocion="triste", alfa=alfa,
                  sombra=False)


# ------------------------------------------------------------------------------------------------ el Consejo de Indias
def sala_consejo(lz, t, cx=0.0):
    """Sala con arcos, cortinas rojas y mesa larga con tapete verde (vista frontal)."""
    lz.relleno(rect_red(0, 0, W, H, 0), (64, 46, 70), capa=0)
    for i in range(5):
        x = 200 + 380 * i - cx * 0.3
        lz.relleno(rect_red(x - 140, 120, 280, 640, 140), (90, 66, 92), capa=0)
        lz.relleno(rect_red(x - 110, 160, 220, 600, 110), (46, 32, 60), capa=0)
        lz.relleno(rect_red(x - 160, 110, 26, 680, 4), (120, 92, 110), capa=0)
    for sd in (-1, 1):                                                   # cortinas
        xx = 0 if sd < 0 else W
        pts = [(xx, 0), (xx - sd * 260, 0), *[(xx - sd * (240 - 30 * math.sin(y * 0.02 + t)), y) for y in range(0, 900, 60)], (xx - sd * 120, 900), (xx, 900)]
        lz.relleno(np.array(pts), (150, 40, 60), capa=0)


def lupa(lz, x, y, r, alfa=1.0, capa=2):
    lz.trazo(circulo(x, y, r, 48), (230, 220, 240), r * 0.12, cerrado=True, temblor=0.0, capa=capa)
    lz.relleno(circulo(x, y, r * 0.94, 48), (200, 220, 255), alfa=0.18 * alfa, capa=capa)
    lz.relleno(circulo(x - r * 0.35, y - r * 0.35, r * 0.18, 16), (255, 255, 255), alfa=0.6 * alfa, capa=capa)
    a = math.pi / 4
    p0 = (x + math.cos(a) * r * 1.05, y + math.sin(a) * r * 1.05)
    p1 = (x + math.cos(a) * r * 2.0, y + math.sin(a) * r * 2.0)
    lz.trazo(np.array([p0, p1]), (120, 80, 60), r * 0.22, afinar=False, temblor=0.0, capa=capa)


def sello_secreto(lz, x, y, s, k, rot=-0.2, capa=2):
    if k <= 0.01:
        return
    with lz.grupo(x, y, 1.0, rot):
        lz.trazo(rect_red(-150 * s * k, -46 * s * k, 300 * s * k, 92 * s * k, 10 * s), (214, 50, 60), 8 * s, cerrado=True, temblor=0.0, capa=capa)
        P.rotulo(lz, 0, 0, "SECRETO", px=int(60 * s * k) + 1, color=(214, 50, 60), alfa=1.0, sombra=0.0)


# ------------------------------------------------------------------------------------------------ la encrucijada
def encrucijada(lz, t, lado, cx=960, y=860):
    """Camino que se parte en dos: a la izquierda sube a la sierra (frío, oscuro), a la derecha baja al valle (cálido, con el pueblo).
    lado = -1..1 hacia dónde «se inclina» la luz."""
    # valle cálido a la derecha
    degradado_v(lz, cx, W, 0, H, (255, 196, 140), (230, 140, 120), 0, H)
    lz.relleno(np.array([(cx, 640), (W, 600), (W, H), (cx, H)]), (150, 190, 110), capa=0)
    for k in range(4):
        xx = cx + 260 + 170 * k
        lz.relleno(rect_red(xx, 610 - 8 * k, 70, 46, 4), (240, 214, 180), capa=0)
        lz.relleno(np.array([(xx - 8, 612 - 8 * k), (xx + 35, 586 - 8 * k), (xx + 78, 612 - 8 * k)]), (200, 110, 80), capa=0)
    # sierra fría a la izquierda
    lz.relleno(np.array([(0, 0), (cx, 0), (cx, H), (0, H)]), (40, 44, 86), capa=0)
    for k, col in enumerate(((60, 64, 112), (48, 50, 96), (36, 38, 76))):
        lz.relleno(np.array([(0, 380 + 120 * k), (200, 220 + 120 * k), (420, 330 + 120 * k), (640, 200 + 120 * k), (cx, 420 + 120 * k), (cx, H), (0, H)]), col, capa=0)
    # caminos
    lz.trazo(np.array(catmull(np.array([(cx, H + 20), (cx - 40, 900), (cx - 260, 720), (cx - 520, 520)], float), 8, False)), (120, 120, 170), 60.0, afinar=False, temblor=0.0, capa=1)
    lz.trazo(np.array(catmull(np.array([(cx, H + 20), (cx + 40, 900), (cx + 300, 760), (cx + 640, 700)], float), 8, False)), (236, 210, 160), 60.0, afinar=False, temblor=0.0, capa=1)
    # poste con dos letreros
    lz.relleno(rect_red(cx - 8, y - 260, 16, 260, 3), (120, 84, 60), capa=1)
    for sd, txt, col in ((-1, "SIERRA", (90, 100, 170)), (1, "VALLE", (220, 140, 70))):
        yy = y - 230 + (0 if sd < 0 else 70)
        tip = cx + sd * 230
        lz.relleno(np.array([(cx, yy - 34), (tip - sd * 40, yy - 34), (tip, yy), (tip - sd * 40, yy + 34), (cx, yy + 34)]), col, capa=1)
        P.rotulo(lz, cx + sd * 105, yy, txt, px=36, color=(255, 255, 255), alfa=1.0, sombra=0.0)
