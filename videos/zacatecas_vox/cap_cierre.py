# -*- coding: utf-8 -*-
"""Capítulo `cierre`: el costo humano (mina a oscuras), la ciudad de hoy y la mina como origen de cada calle."""
import math

import numpy as np

import locales as L
import subsuelo as S
import ui_vox as U
import vox as V
from cap_local import FIG, SUR
from ctx import T, INI, FIN
from motor import W, H, prog, e_out, e_back, e_inout, smooth, clamp01, h01, lerp, rect_red

A = dict(
    ini=INI("cierre"), fin=FIN("cierre"),
    costo=T("cierre", "costo"), pagaron=T("cierre", "pagaron"), cavaron=T("cierre", "cavaron"), oscuridad=T("cierre", "oscuridad"),
    hoy=T("cierre", "Hoy"), centro=T("cierre", "centro"), patrimonio=T("cierre", "Patrimonio"), humanidad=T("cierre", "Humanidad"),
    calle=T("cierre", "calle"), empinada=T("cierre", "empinada"), bajo=T("cierre", "bajó"), mina=T("cierre", "mina"),
)
PASTEL = [(232, 130, 96), (240, 190, 90), (98, 160, 160), (226, 120, 140), (150, 190, 110), (120, 140, 200), (240, 214, 150)]


def casas_hoy(lz, k):
    """Casas de colores trepando por los cerros (la ciudad de hoy)."""
    if k <= 0.01:
        return
    n = 0
    for fila in range(4):
        for i in range(30):
            x = -820 + i * 60 + 22 * h01(50, i, fila) + fila * 20
            if abs(x - 560) < 0 or x > 1000:
                continue
            hh = float(L.h(x))
            y = hh + 6 + fila * 34
            if fila > 0 and hh < -320:
                continue
            u = clamp01(k * 1.6 - h01(51, i, fila) * 0.6)
            if u <= 0:
                continue
            w = 22 + 10 * h01(52, i, fila)
            alto = 40 + 28 * h01(53, i, fila)
            col = PASTEL[int(h01(54, i, fila) * len(PASTEL))]
            with lz.grupo(x, y, 1.0, sy=e_back(u, 1.3)):
                lz.relleno(rect_red(-w, -alto, 2 * w, alto, 2), col, temblor=0.0, capa=1)
                lz.relleno(rect_red(w - 8, -alto, 8, alto, 0), V.oscurecer(col, 0.16), temblor=0.0, capa=1)
                lz.relleno(np.array([[-w - 3, -alto], [w + 3, -alto], [w + 3, -alto - 6], [-w - 3, -alto - 6]]), V.oscurecer(col, 0.32), temblor=0.0, capa=1)
                lz.relleno(rect_red(-7, -alto * 0.6, 14, alto * 0.6, 6), (60, 44, 44), temblor=0.0, capa=1)
                n += 1


def catedral(lz, x, y, s, k):
    kk = e_back(clamp01(k), 1.5) if k < 1 else 1.0
    if kk <= 0.01:
        return
    with lz.grupo(x, y, s, sy=s * kk):
        piedra = (226, 168, 128)
        osc = (196, 134, 100)
        lz.relleno(rect_red(-150, -260, 300, 260, 2), piedra, temblor=0.0, capa=1)
        for sx in (-1, 1):
            lz.relleno(rect_red(sx * 150 - 44, -420, 88, 420, 2), piedra, temblor=0.0, capa=1)
            lz.relleno(rect_red(sx * 150 - 44 + (44 if sx < 0 else 0), -420, 44, 420, 0), osc, temblor=0.0, capa=1)
            lz.relleno(np.array([[sx * 150 - 52, -420], [sx * 150 + 52, -420], [sx * 150, -500]]), (206, 110, 90), temblor=0.0, capa=1)
            lz.relleno(rect_red(sx * 150 - 14, -380, 28, 60, 12), (70, 50, 48), temblor=0.0, capa=1)
            lz.trazo(np.array([[sx * 150, -500], [sx * 150, -540]]), L.MADERA, 6, afinar=False, temblor=0.0, capa=1)
        lz.relleno(rect_red(-62, -260, 124, 260, 30), osc, temblor=0.0, capa=1)
        lz.relleno(rect_red(-42, -200, 84, 200, 24), (70, 50, 48), temblor=0.0, capa=1)
        for i in range(3):
            lz.relleno(V.elipse_pts(-82 + i * 82, -300, 14, 22), (70, 50, 48), temblor=0.0, capa=1)


def teleferico(lz, t, k):
    """Cables y góndola entre el cerro del Grillo y la Bufa."""
    if k <= 0.01:
        return
    a, b = np.array([-560.0, -450.0]), np.array([520.0, -760.0])
    lz.trazo(np.array([a, b]), (70, 60, 60), 4, afinar=False, temblor=0.0, capa=1, alfa=1.0) if False else lz.trazo(np.array([a, b]), (70, 60, 60), 4, afinar=False, temblor=0.0, capa=1)
    u = (0.5 + 0.5 * math.sin(t * 0.35))
    p = a + (b - a) * u
    with lz.grupo(p[0], p[1] + 46, k):
        lz.trazo(np.array([[0, -46], [0, -10]]), (70, 60, 60), 3, afinar=False, temblor=0.0, capa=1)
        lz.relleno(rect_red(-30, -10, 60, 40, 8), V.ROJO, temblor=0.0, capa=1)
        lz.relleno(rect_red(-22, -2, 44, 16, 4), (196, 226, 236), temblor=0.0, capa=1)


def mina_oscura(lz, t, tc, ka):
    """El minero picando en la oscuridad, solo con su vela (todo lo demás se apaga)."""
    with lz.grupo(0, SUR):
        lz.relleno(np.array([[-1500, 1500], [1500, 1500], [1500, 2900], [-1500, 2900]]), (6, 5, 10), temblor=0.0, capa=2, alfa=0.5 * ka)
        f = V.cuadro(V.PICAR, t, 7.5)
        S.luz_vela(lz, -170, 2060, 360, t, alfa=ka)
        V.figura(lz, -170, 2203, 0.5, V.PICAR[f], "africano" if int(t / 4) % 2 else "minero", 1,
                 obj=[("d", "barreta", 0, 1.0)], seed=200)
