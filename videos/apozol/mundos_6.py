# -*- coding: utf-8 -*-
"""Mundos de la escena 6 (haciendas): el valle que se llena de haciendas con cañaverales, la casa grande que se levanta (1775), el hotel al
atardecer y el proceso del piloncillo en 2D (caña → prensa → olla → conos)."""
import math

import numpy as np

import kz_iso as I
import kz_iso_obj as O
import kz_iso_obj2 as O2
import kz_iso_arq as A
import kz_iso_deco as DC
import kz_gente_iso as G
import kz_pers2d as K2
import kz_ui as U
import plano as P
from motor import circulo, elipse, rect_red, catmull, h01, prog, smooth, e_out, e_back, e_inout, W, H
import mundos_2 as M2

CANA = (150, 200, 74)
SITIOS = [(10, -170), (330, -150), (-130, 170), (300, 170), (120, 360)]


class Valle:
    """Valle de haciendas: cada hacienda con su cañaveral; `n` = cuántas están levantadas (float, la última crece); carretas y gente en el camino."""

    def suelo(self, lz, iso, t):
        I.isla(lz, iso, -240, -260, 660, 560, color_top=(150, 190, 108), t=t, seed=141, esp=42)
        DC.parches(lz, iso, -240, -260, 660, 560, (150, 190, 108), n=26, var=20, seed=142, alfa=0.5, tam=(50, 110))
        O.agua(lz, iso, M2.cinta([(640, -280), (580, -80), (620, 120), (570, 300), (610, 540)], 50), t, z=-1.0, seed=3)
        I.camino(lz, iso, [(-240, 80), (30, 90), (260, 110), (540, 70)], 24, (232, 214, 170), borde=(208, 188, 144))
        DC.hierba(lz, iso, -240, -260, 660, 560, n=160, seed=143, t=t, color=(112, 170, 88), flores=0.08)

    def objetos(self, t, n=5.0, gente=1.0, noche=0.0):
        m = I.Mundo()
        m.topo = False
        for i, (x, y) in enumerate(SITIOS):
            u = float(np.clip(n - i, 0.0, 1.0))
            if u <= 0.01:
                continue
            if u < 0.999:
                m.add(x, y, x + 150, y + 110, 60, (lambda x, y, u: (lambda lz, iso: obra(lz, iso, x, y, 150, 110, 38 * smooth(u))))(x, y, u), fijo=False, clave=x + y * 3)
            else:
                A.hacienda(m, x, y, w=150, d=110, muro=[A.OCRE, A.CAL, A.ROSA, A.OCRE, A.CAL][i], techo=A.TEJA2 if i % 2 else A.TEJA, capilla=(i % 2 == 0))
                cx, cy = x + (-120 if i % 2 else 170), y + 10
                m.add(cx, cy, cx + 110, cy + 100, 26, (lambda cx, cy, i: (lambda lz, iso: O.milpa(lz, iso, cx, cy, 110, 100, t=t, seed=i + 40, color=CANA)))(cx, cy, i), clave=cx + cy)
        for i, (x, y) in enumerate(((-200, -200), (480, -20), (-200, 380), (440, 360), (90, 10), (220, 300))):
            m.add(x - 8, y - 8, x + 8, y + 8, 50, (lambda x, y, i: (lambda lz, iso: O.arbol(lz, iso, x, y, h=48, seed=i + 5, t=t)))(x, y, i), clave=x + y * 7)
        # carretas de caña por el camino
        for i in range(2):
            u = ((t * 0.04) + 0.5 * i) % 1.0
            x = -240 + 780 * u
            y = 80 + 30 * (u) + 4 * i
            m.add(x - 12, y - 8, x + 12, y + 8, 30, (lambda x, y, i: (lambda lz, iso: O.carreta(lz, iso, x, y, t=t, mov=1.0, carga=CANA, s=1.2)))(x, y, i), fijo=False, clave=x + y * 3 + 7)
        if gente > 0.01:
            mu = G.Multitud()
            for i in range(6):
                mu.ronda((60 + 70 * i, 40 + 20 * (i % 3)), 40, "campesino" if i % 2 else "campesina", n=1, vel=3, seed=3500 + i, h=44, accion="trabaja" if i % 2 else None)
            mu.camina([(-200, 82), (260, 108), (540, 74)], "arriero", vel=10, seed=3520, h=44)
            mu.dibujar(m, t)
        return m


def obra(lz, iso, x, y, w, d, h):
    """Muros de la casa grande que suben con andamios."""
    I.caja(lz, iso, x, y, w, d, max(2.0, h), (214, 180, 134))
    for k in range(int(max(0, h) // 6)):
        z = 6 * k + 3
        a, b = iso.P(x, y + d, z), iso.P(x + w, y + d, z)
        lz.trazo(np.array([a, b]), (176, 140, 102), 1.4, afinar=False, temblor=0.0, capa=1)
    for px in (x - 6, x + w + 6, x + w / 2):
        a, b = iso.P(px, y + d + 6, 0), iso.P(px, y + d + 6, h + 16)
        lz.trazo(np.array([a, b]), (150, 106, 70), 3.2, afinar=False, temblor=0.0, capa=1)


# ------------------------------------------------------------------------------------------------ 2D: del jugo de la caña al piloncillo
def trapiche(lz, t, u_prensa, u_olla, u_conos, t0=0.0):
    """Cadena de trabajo en 2D, de izquierda a derecha: haces de caña → molino de rodillos → olla de cobre hirviendo → conos de piloncillo."""
    # suelo de piedra y muro de fondo con arcos
    lz.relleno(np.array([(-40, 760), (W + 40, 740), (W + 40, H + 20), (-40, H + 20)]), (150, 112, 88), capa=0)
    lz.relleno(rect_red(0, 360, W, 400, 0), (236, 206, 160), capa=0)
    for i in range(7):
        lz.relleno(rect_red(100 + 270 * i, 430, 170, 330, 80), (190, 150, 110), capa=0)
    lz.relleno(rect_red(0, 340, W, 40, 0), (190, 90, 76), capa=0)
    # haces de caña
    for j in range(3):
        for i in range(7):
            x0 = 130 + 26 * i + 40 * j
            lz.trazo(np.array([(x0, 900 - 30 * j), (x0 + 60 + 6 * i, 640 - 18 * j)]), (122, 170, 70), 12.0, afinar=False, temblor=0.0, capa=1)
            lz.trazo(np.array([(x0 + 3, 880 - 30 * j), (x0 + 63 + 6 * i, 650 - 18 * j)]), (170, 214, 96), 4.0, afinar=False, temblor=0.0, capa=1)
        lz.relleno(rect_red(130 + 40 * j - 6, 820 - 30 * j, 190, 10, 4), (176, 130, 80), capa=1)
    # molino de rodillos (con engranajes que giran)
    px, py = 600, 800
    lz.relleno(rect_red(px - 120, py - 220, 240, 240, 14), (120, 84, 62), capa=1)
    for sg, cy in ((-1, py - 150), (1, py - 70)):
        ang = t * 2.0 * sg * u_prensa
        lz.relleno(circulo(px, cy, 60, 28), (96, 70, 58), capa=1)
        lz.relleno(circulo(px, cy, 50, 28), (170, 150, 128), capa=1)
        for k in range(8):
            a = ang + k * math.pi / 4
            lz.relleno(circulo(px + 44 * math.cos(a), cy + 44 * math.sin(a), 6, 8), (110, 90, 76), capa=1)
    # jugo que cae por un canal hacia la olla
    pts = [(px + 90, py - 20), (px + 190, py - 6), (820, py + 24)]
    lz.trazo(np.array(pts), (255, 214, 120), 14.0 * min(1.0, u_prensa * 1.5), afinar=False, temblor=0.0, capa=1)
    # olla grande de cobre sobre fuego
    ox, oy = 1040, 800
    lz.relleno(elipse(ox, oy + 30, 190, 36, 0, 30), (40, 24, 40), alfa=0.4, capa=1)
    for j, (col, sc) in enumerate((((236, 60, 48), 1.0), ((255, 138, 40), 0.72), ((255, 224, 96), 0.42))):
        for q in (-100, -40, 30, 90):
            a = 80 * sc * u_olla * (1 + 0.18 * math.sin(t * 9 + q + j))
            lz.relleno(np.array([(ox + q - 24 * sc, oy + 24), (ox + q + 24 * sc, oy + 24), (ox + q + 4 * math.sin(t * 7 + q), oy + 24 - a)]), col, capa=1)
    lz.relleno(np.array([(ox - 170, oy - 140), (ox + 170, oy - 140), (ox + 140, oy - 20), (ox + 80, oy + 8), (ox - 80, oy + 8), (ox - 140, oy - 20)]), (196, 106, 60), capa=1)
    lz.relleno(np.array([(ox + 40, oy - 140), (ox + 170, oy - 140), (ox + 140, oy - 20), (ox + 80, oy + 8), (ox + 30, oy + 8)]), (150, 76, 50), capa=1)
    lz.relleno(elipse(ox, oy - 140, 170, 28, 0, 30), (255, 190, 90), capa=1)
    lz.relleno(elipse(ox, oy - 140, 150, 22, 0, 30), (176, 96, 44), capa=1)
    for q in range(10):                                                      # burbujas del jugo hirviendo
        u = ((t * 0.9 + q / 10.0) % 1.0)
        bx = ox - 120 + 240 * h01(5, q, 1)
        lz.relleno(circulo(bx, oy - 140 - 10 * u, 5 + 12 * (1 - u) * u * 4, 12), (255, 226, 150), alfa=0.9 * (1 - u) * u_olla, capa=1)
    for i in range(8):                                                       # vapor
        u = ((t * 0.25 + i / 8.0) % 1.0)
        lz.relleno(circulo(ox - 80 + 160 * h01(6, i, 1) + 24 * math.sin(u * 6 + i), oy - 170 - u * 300, 20 + 46 * u, 18), (252, 248, 240), alfa=0.55 * (1 - u) * u_olla, capa=1)
    # el trabajador revuelve con la pala
    K2.cuerpo(lz, 1300, 900, 40, "caxcan", t, piernas="idle", brazos="balanceo", mirar=-1, vista="perfil", seed=9)
    # conos de piloncillo (moldes) sobre una mesa
    lz.relleno(rect_red(1440, 800, 450, 26, 6), (120, 84, 62), capa=1)
    for i in range(7):
        k = float(np.clip(u_conos * 8 - i, 0, 1))
        if k <= 0.01:
            continue
        cx = 1480 + 62 * i
        lz.relleno(np.array([(cx - 24 * k, 800), (cx + 24 * k, 800), (cx + 5 * k, 800 - 92 * k), (cx - 5 * k, 800 - 92 * k)]), (156, 92, 48), capa=1)
        lz.relleno(np.array([(cx + 4 * k, 800), (cx + 24 * k, 800), (cx + 5 * k, 800 - 92 * k)]), (118, 66, 36), capa=1)
        lz.relleno(elipse(cx - 6 * k, 800 - 60 * k, 3 * k, 14 * k, 0.1, 10), (214, 150, 90), alfa=0.8, capa=1)
