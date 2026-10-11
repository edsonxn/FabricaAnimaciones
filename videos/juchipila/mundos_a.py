# -*- coding: utf-8 -*-
"""Mundos 2D de la escena 1 (gancho): la flor de xúchitl (cempasúchil) que brota, y la multitud sin cara que se disuelve en pétalos."""
import math

import numpy as np

import plano as P
from motor import circulo, elipse, h01, prog, smooth, e_back, e_out, e_inout
from kz_abstracto import _petalo_pts

ANILLOS = [  # (n, radio inicial, largo, ancho, color, momento en que abre)
    (16, 0.20, 0.82, 0.21, (255, 126, 24), 0.00),
    (14, 0.15, 0.66, 0.20, (255, 158, 36), 0.10),
    (12, 0.10, 0.50, 0.18, (255, 190, 56), 0.22),
    (10, 0.06, 0.35, 0.16, (255, 218, 96), 0.36),
    (8, 0.00, 0.20, 0.13, (255, 238, 156), 0.50),
]


def flor_xuchitl(lz, x, y, r, t, u=1.0, seed=0, alfa=1.0, capa=2, giro=0.0, sombra=True):
    """Flor de xúchitl/cempasúchil de pétalos en anillos (2 tonos por pétalo). u 0..1 = brotar: abre de fuera hacia dentro con rebote. Gira y respira."""
    if u <= 0.003 or alfa <= 0.003:
        return
    resp = 1 + 0.02 * math.sin(t * 1.7 + seed)
    r = r * resp
    if sombra:
        lz.halo(x, y, r * 1.5, (255, 150, 50), alfa=0.22 * alfa * min(1, u * 2), dureza=1.3, capa=capa)
    for k, (n, r0, L, Wd, col, t_ab) in enumerate(ANILLOS):
        s = e_back(prog(u, t_ab, t_ab + 0.5), 1.6)
        if s <= 0.001:
            continue
        rot = giro + t * (0.10 + 0.03 * k) * (1 if k % 2 == 0 else -1) + k * 0.31 + seed
        for j in range(n):
            a = rot + j * 2 * math.pi / n
            ox, oy = x + math.cos(a) * r0 * r * s, y + math.sin(a) * r0 * r * s
            Lp, Wp = L * r * s, Wd * r * s
            lz.relleno(_petalo_pts(ox, oy, Lp, Wp, a), P.oscurecer(col, 0.20), alfa=alfa, capa=capa)               # base en sombra
            lz.relleno(_petalo_pts(ox - 0.03 * r, oy - 0.03 * r, Lp * 0.96, Wp * 0.78, a), col, alfa=alfa, capa=capa)   # cara iluminada
            lz.relleno(_petalo_pts(ox - 0.03 * r, oy - 0.045 * r, Lp * 0.78, Wp * 0.18, a + 0.03), P.aclarar(col, 0.30), alfa=alfa * 0.7, capa=capa)
    s = e_out(prog(u, 0.5, 0.9))
    lz.relleno(circulo(x, y, 0.07 * r * s, 14), (160, 80, 20), alfa=alfa, capa=capa)
    lz.relleno(circulo(x - 0.012 * r, y - 0.012 * r, 0.04 * r * s, 12), (212, 130, 40), alfa=alfa, capa=capa)


def silueta_guerrero(lz, x, y, s, color, t, seed=0, alfa=1.0, escala=1.0, capa=1, lanza=True):
    """Guerrero de un solo tono (silueta de lanza en alto y penacho) para crestas y fondos lejanos. Origen en los pies; s = px por unidad (~8 u de alto)."""
    k = s * escala
    if k <= 0.2:
        return
    bal = math.sin(t * 3.0 + seed) * 0.10
    pts = lambda L: np.array([(x + px * k, y + py * k) for px, py in L])
    lz.relleno(pts([(-0.62, -3.1), (0.62, -3.1), (0.78, -5.1), (-0.78, -5.1)]), color, alfa=alfa, capa=capa)                      # tronco
    for sd in (-1, 1):                                                                                                            # piernas
        lz.relleno(pts([(sd * 0.60 - 0.30, -3.2), (sd * 0.60 + 0.30, -3.2), (sd * 0.72 + 0.26, 0.0), (sd * 0.72 - 0.26, 0.0)]), color, alfa=alfa, capa=capa)
    lz.relleno(circulo(x, y - 5.95 * k, 0.66 * k, 14), color, alfa=alfa, capa=capa)                                              # cabeza
    for j in range(5):                                                                                                            # penacho
        a = -0.8 + 0.4 * j + bal
        lz.relleno(pts([(-0.2 + 0.1 * j - 0.15, -6.5), (math.sin(a) * 1.9, -6.5 - math.cos(a) * 1.9), (0.2 + 0.1 * j - 0.1, -6.5)]), color, alfa=alfa, capa=capa)
    # brazo en alto con lanza
    lz.relleno(pts([(0.5, -4.9), (1.5, -6.8 + bal * 2), (1.9, -6.6 + bal * 2), (0.9, -4.5)]), color, alfa=alfa, capa=capa)
    if lanza:
        lz.relleno(pts([(1.55, -3.2 + bal * 2), (1.7, -3.2 + bal * 2), (1.78 + bal, -10.4), (1.62 + bal, -10.4)]), color, alfa=alfa, capa=capa)
        lz.relleno(pts([(1.45 + bal, -10.4), (1.7 + bal, -11.7), (1.95 + bal, -10.4)]), color, alfa=alfa, capa=capa)
