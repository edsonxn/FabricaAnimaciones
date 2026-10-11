# -*- coding: utf-8 -*-
"""Escenas 5-8: durero (el cargamento cruza el Atlántico y Durero lo ve en Bruselas), fundicion (horno, molde y reparto en quintos),
matanza (Cortés sale, fiesta de Tóxcatl y ataque, cerco al palacio) y muerte (Moctezuma en la azotea: dos versiones)."""
import json
import math
import os

import numpy as np

from motor import W, H, prog, lerp, smooth, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, blob, catmull, bezier, h01, corazon
import plano as P
import mapa as MP
import mapa_local as ML
import figuras as F
from mundo import degradado_v, llama, humo
from reg import shot, snd
from util import *

PANT = np.array([[0, 0], [W, 0], [W, H], [0, H]], float)

# ======================================================================== 5. DURERO
E5 = "durero"
KA = 17.0
_TIERRA = []


def _cargar_tierra():
    if not _TIERRA:
        d = json.load(open("datos/tierra_atlantico.json"))
        for r in d:
            a = np.array(r, float)
            if len(a) < 8:
                continue
            xy = np.stack([a[:, 0] * KA, -a[:, 1] * KA], 1)
            _TIERRA.append(((xy[:, 0].min(), xy[:, 1].min(), xy[:, 0].max(), xy[:, 1].max()), xy))
    return _TIERRA


def ax(lon, lat):
    return lon * KA, -lat * KA


def w2s(c, lon, lat):
    x, y = ax(lon, lat)
    cx, cy = ax(c[0], c[1])
    return W / 2 + (x - cx) * c[2], H / 2 + (y - cy) * c[2]


def tierra_atl(lz, c):
    cx, cy = ax(c[0], c[1])
    z = c[2]
    x0, x1 = cx - W / 2 / z - 60, cx + W / 2 / z + 60
    y0, y1 = cy - H / 2 / z - 60, cy + H / 2 / z + 60
    with lz.grupo(W / 2 - cx * z, H / 2 - cy * z, z):
        for (bb, xy) in _cargar_tierra():
            if bb[2] < x0 or bb[0] > x1 or bb[3] < y0 or bb[1] > y1:
                continue
            if (bb[2] - bb[0]) * z < 3 and (bb[3] - bb[1]) * z < 3:
                continue
            lz.relleno(xy + np.array([0, 5.0 / z]), (150, 104, 88))
            lz.relleno(xy, (226, 178, 112))


RUTA_MAR = [(-96.1, 19.2), (-90.0, 22.2), (-84.5, 23.6), (-80.4, 26.0), (-70.0, 31.0), (-45.0, 36.0), (-26.0, 38.3), (-12.0, 37.0), (-6.2, 37.0)]
RUTA_TIERRA = [(-6.0, 37.3), (-4.7, 41.6), (-1.5, 44.0), (2.3, 48.8), (4.35, 50.85)]


def _poli_ax(pts, n=14):
    return catmull(np.array([ax(a, b) for a, b in pts]), n)


def _en_ruta(pts, u):
    d = np.hypot(*np.diff(pts, axis=0).T)
    cum = np.concatenate([[0], np.cumsum(d)])
    s = u * cum[-1]
    i = int(np.clip(np.searchsorted(cum, s) - 1, 0, len(pts) - 2))
    f = (s - cum[i]) / max(d[i], 1e-6)
    p = pts[i] + (pts[i + 1] - pts[i]) * f
    ang = math.atan2(*(pts[i + 1] - pts[i])[::-1])
    return p, ang


@shot(T0(E5), bg=lambda t: bg_grad((22, 70, 150), (8, 30, 96)), ent=("tinta", 0.8))
def d_atlantico(lz, t):
    c = Klog(t, [(T0(E5), (-50.0, 30.0, 1.0)), (76.6, (-32.0, 36.5, 1.3)), (78.3, (-2.0, 43.0, 3.0)), (81.6, (2.5, 46.5, 3.6))])
    tierra_atl(lz, c)
    z = c[2]
    mar = _poli_ax(RUTA_MAR)
    cx, cy = ax(c[0], c[1])
    u1 = K(t, [(INI(E5, 0) - 0.2, 0.0), (77.6, 1.0)], e_inout)
    u2 = K(t, [(77.6, 0.0), (81.4, 1.0)], e_inout)
    with lz.grupo(W / 2 - cx * z, H / 2 - cy * z, z):
        P.discontinua(lz, mar, (255, 226, 130), ancho=7.0 / z ** 0.8, largo=26 / z ** 0.8, hueco=18 / z ** 0.8, fase=-t * 30 / z ** 0.8, frac=u1)
        tie = _poli_ax(RUTA_TIERRA)
        P.discontinua(lz, tie, (255, 150, 110), ancho=7.0 / z ** 0.8, largo=26 / z ** 0.8, hueco=18 / z ** 0.8, fase=-t * 30 / z ** 0.8, frac=u2)
        if u1 < 1.0:
            p, ang = _en_ruta(mar, u1)
            F.bergantin(lz, p[0], p[1], 0.62 / z ** 0.8, t, lado=1 if math.cos(ang) >= 0 else -1, seed=3)
            for k in range(7):
                q, _ = _en_ruta(mar, max(0.0, u1 - 0.008 * (k + 1)))
                lz.relleno(circulo(q[0], q[1] + 4 / z, (5.0 - 0.5 * k) / z ** 0.8, 8), (255, 255, 255), alfa=0.5 - 0.06 * k)
        if u2 > 0.0:
            p, ang = _en_ruta(_poli_ax(RUTA_TIERRA), u2)
            F.caballo(lz, p[0], p[1], 0.62 / z ** 0.8, t, paso=1.5 if u2 < 1 else 0.0, lado=1, carga=1, seed=2)
    for txt, (lo, la), tt, dy in (("Veracruz", RUTA_MAR[0], T0(E5), -46), ("Sevilla", RUTA_MAR[-1], 77.3, 44), ("Bruselas", RUTA_TIERRA[-1], 81.0, -50)):
        x, y = w2s(c, lo, la)
        a = smooth(prog(t, tt, tt + 0.4))
        if a > 0.01 and -100 < x < W + 100 and -100 < y < H + 100:
            with lz.capa(2):
                lz.halo(x, y, 26, (255, 214, 96), alfa=0.7 * a)
                lz.relleno(circulo(x, y, 8, 16), BLANCO, alfa=a)
                P.pastilla(lz, x, y + dy, txt, px=34, alfa=a)
    cifra(lz, t, T0(E5) + 0.4, "julio de 1519", W / 2, 120, px=70, col=BLANCO, t1=w_(E5, 1, 2))
    cifra(lz, t, w_(E5, 1, 3), "agosto de 1520", W / 2, 120, px=70, col=ORO, t1=81.6)
    a = vent(t, w_(E5, 1, 7) - 0.2, w_(E5, 1, 12) + 1.2, 0.4, 0.4)
    if a > 0.01:
        tarjeta(lz, "durero", 250 - 60 * (1 - a), 400, 300, aspecto=1.36, foco=(0.5, 0.3), rot=-0.05, alfa=a, pie="Alberto Durero")


snd(T0(E5) + 0.2, "whoosh", 0.4, dur=0.7)
snd(T0(E5) + 0.6, "viento", 0.3, dur=4.5)
snd(w_(E5, 1, 7), "pop", 0.4)
snd(77.6, "pasos", 0.25, dur=3.6)
snd(81.0, "campana", 0.3)


def _sala(lz, t, zoom, cxx):
    """Sala del palacio de Bruselas: arcos góticos, pedestales, mesas con telas y piezas del tesoro."""
    with cam(lz, cxx, 540, zoom):
        lz.relleno(rect_red(-200, 100, 2320, 760, 0), (92, 70, 100))
        for i in range(7):
            x = 40 + i * 300
            lz.relleno(np.array([[x - 90, 760], [x - 90, 330], [x - 60, 200], [x, 150], [x + 60, 200], [x + 90, 330], [x + 90, 760]]), (110, 86, 118))
            lz.relleno(np.array([[x - 62, 760], [x - 62, 340], [x - 38, 236], [x, 196], [x + 38, 236], [x + 62, 340], [x + 62, 760]]), (72, 90, 150) if i % 2 else (150, 100, 90))
            lz.relleno(rect_red(x - 96, 748, 192, 16, 2), (150, 120, 130))
        lz.relleno(rect_red(-200, 760, 2320, 200, 0), (64, 48, 72))
        for i in range(-10, 30):
            lz.relleno(np.array([[i * 110, 760], [i * 110 + 6, 760], [i * 110 - 60, 960], [i * 110 - 66, 960]]), (86, 66, 96))
        # luz de las ventanas
        lz.halo(560, 470, 420, (255, 214, 120), alfa=0.5)
        lz.halo(1360, 470, 400, (200, 226, 255), alfa=0.35)
        # pedestales y discos
        for x in (560, 1360):
            lz.relleno(rect_red(x - 90, 690, 180, 90, 6), (140, 60, 70))
            lz.relleno(rect_red(x - 110, 776, 220, 20, 4), (176, 130, 92))
            lz.relleno(rect_red(x - 14, 600, 28, 100, 3), (176, 130, 92))
        ts, tl_ = w_(E5, 2, 2), w_(E5, 2, 7)
        if t > ts - 0.3:
            k = e_back(prog(t, ts - 0.3, ts + 0.5))
            F.disco(lz, 560, 470 - 30 * (1 - k), 175 * max(k, 0.01), t, "oro", rot=t * 0.35)
        if t > tl_ - 0.3:
            k = e_back(prog(t, tl_ - 0.3, tl_ + 0.5))
            F.disco(lz, 1360, 470 - 30 * (1 - k), 175 * max(k, 0.01), t, "plata", rot=-t * 0.2)
        # mesa central con piezas
        lz.relleno(rect_red(760, 700, 400, 24, 4), (150, 40, 60))
        lz.relleno(np.array([[780, 724], [1140, 724], [1120, 790], [800, 790]]), (110, 30, 50))
        F.cofre(lz, 840, 700, 1.0, 1.0)
        F.barra_oro(lz, 960, 688, 0.7, 0.0, 0.3)
        F.jade(lz, 1050, 690, 1.1, t)
        F.pluma(lz, 1120, 700, 0.9, 0.2, (60, 200, 130), t)
        # cortesanos que pasean
        for k, (x0, col) in enumerate(((100, 1), (700, 3), (1500, 5), (1800, 2))):
            x = (x0 + t * 30 * (1 if k % 2 else -1)) % 2100 - 100
            P.humano(lz, x, 800, 1.05, t, ropa=[(198, 80, 90), (90, 120, 200), (230, 190, 90), (120, 90, 170), (84, 170, 140), (220, 120, 70)][col], paso=0.45, voltear=(k % 2 == 0))


@shot(81.7, bg=lambda t: bg_grad((60, 44, 80), (30, 22, 52)), ent=("tinta", 0.8))
def d_sala(lz, t):
    zoom = K(t, [(81.7, 1.0), (89.5, 1.18)], e_inout)
    cxx = K(t, [(81.7, 960.0), (85.0, 760.0), (88.0, 1080.0)], e_inout)
    _sala(lz, t, zoom, cxx)
    esc = smooth(prog(t, w_(E5, 2, 14), w_(E5, 2, 15)))
    with cam(lz, cxx, 540, zoom):
        F.durero(lz, 960, 858, 2.5, t, lado=-1 if t < w_(E5, 2, 14) else 1, escribe=esc, sorpresa=smooth(prog(t, w_(E5, 2, 2), w_(E5, 2, 3))))
        if t > w_(E5, 2, 23):
            for i in range(9):
                u = (t - w_(E5, 2, 23)) * 0.6 - i * 0.07
                if 0 < u < 1.3:
                    px = 960 + 40 * math.sin(i * 2.1 + t * 2) + (h01(3, i) - 0.5) * 240 * u
                    py = 520 - 300 * u
                    lz.relleno(corazon(px, py, 16 + 8 * h01(4, i)), (255, 96, 120), alfa=1 - u / 1.3, capa=2)
    etq(lz, t, w_(E5, 1, 7) + 0.3, w_(E5, 1, 12) + 0.5, "Alberto Durero", W / 2, 250, px=40)
    a = vent(t, w_(E5, 2, 14), T1(E5) - 0.3, 0.4, 0.4)
    if a > 0.01:
        with lz.capa(2):
            x, y = 1700, 300
            lz.relleno(rect_red(x - 200, y - 150, 400, 330, 10), (250, 240, 214), alfa=0.96 * a)
            lz.relleno(rect_red(x - 200, y - 150, 400, 26, 8), (196, 150, 90), alfa=a)
            P.rotulo(lz, x, y - 137, "Diario de Durero · 1520", px=26, color=(60, 40, 40), sombra=0.0, alfa=a)
            for i in range(9):
                u = smooth(prog(t, w_(E5, 2, 15) + i * 0.32, w_(E5, 2, 15) + i * 0.32 + 0.5))
                if u > 0:
                    lz.relleno(rect_red(x - 170, y - 96 + i * 32, 340 * u * (0.5 + 0.5 * h01(6, i)), 5, 2), (80, 60, 64), alfa=a)


snd(81.9, "revelar", 0.4)
snd(w_(E5, 2, 2), "brillo", 0.5)
snd(w_(E5, 2, 7), "brillo", 0.4)
snd(w_(E5, 2, 15), "escribir", 0.4, dur=4.5)
snd(w_(E5, 2, 23), "pop", 0.4)
snd(w_(E5, 2, 24), "bling", 0.35)

# ======================================================================== 6. FUNDICIÓN
E6 = "fundicion"
T_MELT = w_(E6, 1, 2)
T_BARRAS = w_(E6, 1, 4)
T_REPARTO = w_(E6, 1, 5) - 0.1
T_NADA = INI(E6, 2) - 0.1
PIEZAS = [("disco", 250, 700), ("mascara", 330, 780), ("collar", 190, 790), ("idolo", 300, 640), ("plumas", 230, 660)]


def _mascara(lz, x, y, s):
    with lz.grupo(x, y, s):
        lz.relleno(elipse(0, -30, 30, 40, 0.0, 24), F.ORO_S)
        lz.relleno(elipse(-2, -32, 26, 36, 0.0, 24), F.ORO)
        lz.relleno(circulo(-11, -40, 8, 12), (60, 200, 200))
        lz.relleno(circulo(11, -40, 8, 12), (60, 200, 200))
        lz.relleno(circulo(-11, -40, 3, 8), (30, 40, 60))
        lz.relleno(circulo(11, -40, 3, 8), (30, 40, 60))
        lz.relleno(rect_red(-9, -22, 18, 8, 3), F.ORO_S)


def _idolo(lz, x, y, s):
    with lz.grupo(x, y, s):
        lz.relleno(rect_red(-16, -52, 32, 46, 8), F.ORO)
        lz.relleno(circulo(0, -68, 16, 16), F.ORO)
        lz.relleno(np.array([[-18, -78], [-9, -96], [0, -80], [9, -96], [18, -78]]), F.ORO_S)
        lz.relleno(circulo(-5, -70, 3, 6), (60, 60, 80))
        lz.relleno(circulo(5, -70, 3, 6), (60, 60, 80))
        lz.relleno(rect_red(-16, -12, 32, 10, 3), F.ORO_S)


def _pieza(lz, kind, x, y, s, t):
    if kind == "disco":
        F.disco(lz, x, y - 30 * s, 34 * s, t, "oro")
    elif kind == "mascara":
        _mascara(lz, x, y, 1.1 * s)
    elif kind == "collar":
        F.joya(lz, x, y - 10, 1.4 * s, "collar", t)
    elif kind == "idolo":
        _idolo(lz, x, y, 1.0 * s)
    else:
        F.pluma(lz, x, y, 0.55 * s, 0.1, (60, 200, 130), t)


@shot(T0(E6), bg=lambda t: bg_grad((30, 18, 34), (74, 34, 30)), ent=("tinta", 0.7))
def f_horno(lz, t):
    nivel = K(t, [(T_MELT, 0.12), (T_MELT + 1.6, 0.86)], e_inout)
    incl = K(t, [(T_BARRAS - 0.4, 0.0), (T_BARRAS + 0.4, 0.55), (T_BARRAS + 2.0, 0.55), (T_BARRAS + 2.6, 0.0)], e_inout)
    _cm = cam(lz, 940, 640, 1.16)
    _cm.__enter__()
    # horno de piedra
    lz.halo(900, 800, 520, (255, 140, 50), alfa=0.35 + 0.1 * math.sin(t * 8))
    lz.relleno(rect_red(660, 660, 480, 240, 12), (120, 86, 100))
    lz.relleno(rect_red(660, 660, 480, 22, 6), (170, 132, 140))
    lz.relleno(np.array([[760, 900], [760, 780], [800, 730], [900, 710], [1000, 730], [1040, 780], [1040, 900]]), (36, 20, 30))
    for k in range(4):
        llama(lz, 830 + k * 46, 900, 1.0, t, seed=k)
    lz.halo(900, 830, 200, (255, 190, 80), alfa=0.6)
    # crisol
    with lz.grupo(900, 660, 1.0, incl * 0.9):
        lz.relleno(np.array([[-120, 0], [120, 0], [96, -170], [-96, -170]]), (70, 60, 84))
        lz.relleno(np.array([[-120, 0], [-84, 0], [-70, -170], [-96, -170]]), (110, 96, 130))
        lz.relleno(rect_red(-110, -184, 220, 22, 8), (140, 124, 158))
        yl = -170 + (1 - nivel) * 150
        lz.relleno(np.array([[-100 + (yl + 170) * 0.15, yl], [100 - (yl + 170) * 0.15, yl], [96, -170 + 0], [-96, -170 + 0]]), (255, 190, 60), alfa=0.0)
        lz.relleno(elipse(0, yl - 4, 96 - (yl + 170) * 0.13, 16, 0.0, 30), (255, 236, 150))
        lz.relleno(elipse(0, yl + 2, 90 - (yl + 170) * 0.13, 12, 0.0, 30), (255, 190, 60))
        for b in range(5):
            ph = (t * 1.3 + b * 0.37) % 1.0
            lz.relleno(circulo(-60 + 30 * b, yl - 8 - 10 * ph, 5 + 5 * ph, 10), (255, 246, 190), alfa=1 - ph)
    lz.halo(900, 500, 240 * (nivel - 0.1) + 50, (255, 200, 80), alfa=0.6 * min(1.0, nivel * 2))
    # mesa con las piezas de arte (antes de fundirlas)
    lz.relleno(rect_red(80, 790, 420, 26, 5), (140, 90, 66))
    lz.relleno(rect_red(110, 816, 24, 100, 2), (110, 70, 56))
    lz.relleno(rect_red(446, 816, 24, 100, 2), (110, 70, 56))
    for i, (kind, px, py) in enumerate(PIEZAS):
        tt = T_MELT + i * 0.42
        u = prog(t, tt, tt + 0.9)
        if u >= 1.0:
            continue
        bx, by = 140 + i * 78, 790
        x = lerp(bx, 900, e_inout(u))
        y = lerp(by, 470, u) - 240 * math.sin(math.pi * u)
        _pieza(lz, kind, x, y, 1.05 - 0.4 * u, t)
        if u > 0.85:
            lz.halo(900, 500, 120, (255, 240, 170), alfa=0.6 * (u - 0.85) / 0.15)
    # personajes
    F.soldado(lz, 640, 900, 2.0, t, lado=1, brazos=(-0.3, 2.3 * smooth(prog(t, w_(E6, 1, 1), w_(E6, 1, 1) + 0.4)) if t < T_MELT + 2 else 0.0), seed=8,
              tunica=(150, 40, 60), arma=None)
    F.guerrero(lz, 1240, 900, 2.0, t, lado=-1, arma=None, escudo=False, plumas=0, seed=3, brazos=(-0.8 + 0.5 * math.sin(t * 5), 0.6))
    # arte: brilla y se conserva (frase 0)
    a = vent(t, INI(E6, 0), T_MELT - 0.3, 0.3, 0.3)
    if a > 0.01:
        P.pastilla(lz, 290, 610, "arte mexica en oro", px=36, alfa=a)
    # verter: chorro hasta los moldes
    if t >= T_BARRAS - 0.2:
        u = smooth(prog(t, T_BARRAS - 0.2, T_BARRAS + 0.6)) * (1 - smooth(prog(t, T_BARRAS + 2.0, T_BARRAS + 2.5)))
        if u > 0.02:
            x0, y0 = 1040, 620
            with lz.capa(1):
                lz.relleno(np.array([[x0, y0], [x0 + 22, y0], [1500 + 20, 800], [1500 - 6, 800]]), (255, 214, 96), alfa=u)
            lz.halo(1500, 800, 90, (255, 214, 96), alfa=0.5 * u)
    # moldes y barras que se forman
    for k in range(5):
        x = 1310 + k * 118
        lz.relleno(rect_red(x - 48, 800, 96, 60, 6), (74, 60, 84))
        f = smooth(prog(t, T_BARRAS + 0.5 + k * 0.28, T_BARRAS + 0.9 + k * 0.28))
        if f > 0.01:
            lz.relleno(rect_red(x - 42, 812 + (1 - f) * 34, 84, 34 * f, 4), (255, 200, 70))
    _cm.__exit__(None, None, None)
    etq(lz, t, T_BARRAS - 0.6, T_BARRAS + 1.6, "moldes de barras", 1560, 740, px=34)
    gran(lz, t, T_MELT - 0.2, T_MELT + 1.6, "FUNDIR", 900, 250, px=110, col=(255, 190, 80))


snd(T0(E6) + 0.2, "fuego", 0.4, dur=5.5)
for _i in range(5):
    snd(T_MELT + _i * 0.42 + 0.7, "clink", 0.35, tono=0.9 + 0.05 * _i)
snd(T_MELT + 1.2, "siseo", 0.4)
snd(T_BARRAS - 0.2, "chorro", 0.45, dur=2.4)


def _cofre_zona(lz, x, y, titulo, sub, icono, t, t0):
    a = smooth(prog(t, t0 - 0.6, t0))
    with lz.capa(1):
        lz.relleno(rect_red(x - 240, 330, 480, 560, 24), (60, 40, 80), alfa=0.9 * a)
    P.rotulo(lz, x, 380, titulo, px=54, color=(255, 255, 255), alfa=a)
    P.pastilla(lz, x, 450, sub, px=34, alfa=a)
    icono(x, 540, a)


@shot(T_REPARTO, bg=lambda t: bg_grad((44, 26, 76), (24, 14, 46)), ent=("zoom", 0.5))
def f_reparto(lz, t):
    tr, tc, ts = w_(E6, 1, 9), w_(E6, 1, 12), w_(E6, 1, 18)
    def corona(x, y, a):
        lz.relleno(np.array([[x - 40, y + 20], [x - 40, y - 20], [x - 20, y], [x, y - 30], [x + 20, y], [x + 40, y - 20], [x + 40, y + 20]]), F.ORO, alfa=a)
    def sello(x, y, a):
        F.soldado(lz, x, y + 80, 1.3, t, lado=1, seed=1, tunica=(150, 40, 60))
    def tropa(x, y, a):
        for i in range(3):
            F.soldado(lz, x - 90 + i * 90, y + 90, 1.05, t, lado=1 if i != 1 else -1, seed=i + 12, carga=0.6 * smooth(prog(t, ts, ts + 1)))
    _cofre_zona(lz, 380, 0, "El rey", "un quinto", corona, t, tr)
    _cofre_zona(lz, 960, 0, "Cortés", "un quinto", sello, t, tc)
    _cofre_zona(lz, 1540, 0, "Soldados", "el resto", tropa, t, ts)
    # barras que vuelan desde arriba a cada zona
    for (tt, tx, ty, n) in ((tr, 380, 760, 1), (tc, 960, 760, 1), (ts, 1540, 760, 3)):
        for k in range(n):
            u = prog(t, tt + 0.05 + 0.18 * k, tt + 0.75 + 0.18 * k)
            if u <= 0:
                continue
            x = lerp(960, tx + (k - 1) * 90 * (n > 1), e_inout(u))
            y = lerp(90, ty - 30 * k * (n > 1), e_in(u)) - 240 * math.sin(math.pi * u) * (1 - 0.2 * k)
            F.barra_oro(lz, x, y, 0.9, 0.3 * (1 - u), 0.5 if u < 1 else 0.0)
            if u >= 1:
                pass
    # una barra que queda en cada montón
    for (tt, tx, n) in ((tr, 380, 1), (tc, 960, 1), (ts, 1540, 3)):
        if t > tt + 0.9:
            for k in range(n):
                F.barra_oro(lz, tx + (k - 1) * 90 * (n > 1), 770 - 30 * k * (n > 1), 0.9, 0.0, 0.0)
    fr = smooth(prog(t, T_REPARTO, T_REPARTO + 0.5))
    P.rotulo(lz, 960, 180, "Reparto del oro fundido", px=64, alfa=fr)


for _t_, _v in ((w_(E6, 1, 9), 0.4), (w_(E6, 1, 12), 0.4), (w_(E6, 1, 18), 0.5)):
    snd(_t_ + 0.7, "clink", _v)
snd(T_REPARTO, "zoom_whoosh", 0.4, dur=0.8)


@shot(T_NADA, bg=lambda t: bg_grad((30, 20, 44), (16, 10, 30)), ent=("tinta", 0.7))
def f_nada(lz, t):
    tt = INI(E6, 2)
    for i, (kind, x, y) in enumerate((("disco", 330, 430), ("plata", 960, 400), ("mascara", 1560, 460))):
        u = smooth(prog(t, tt + 0.8 + i * 0.3, tt + 1.6 + i * 0.3))
        k = max(1.0 - u, 0.0)
        with lz.grupo(x, y, 1.0):
            if k > 0.02:
                if kind == "disco":
                    F.disco(lz, 0, 0, 150 * k, t, "oro")
                elif kind == "plata":
                    F.disco(lz, 0, 0, 150 * k, t, "plata")
                else:
                    _mascara(lz, 0, 60 * k, 4.0 * k)
            ring = circulo(0, 0, 160, 60)
            P.discontinua(lz, np.vstack([ring, ring[:1]]), (255, 214, 96), ancho=6.0, largo=22, hueco=16, fase=-t * 20, frac=u)
            if u > 0.5:
                lz.trazo(np.array([[-110, -110], [110, 110]]), (240, 70, 70), 16.0, temblor=0.0, capa=2)
                lz.trazo(np.array([[110, -110], [-110, 110]]), (240, 70, 70), 16.0, temblor=0.0, capa=2)
    gran(lz, t, tt + 1.4, T1(E6) - 0.2, "Ninguna se conserva", 960, 190, px=90, col=(255, 200, 100))
    etq(lz, t, tt + 0.2, tt + 2.0, "Las piezas que vio Durero", 960, 700, px=38)


snd(T_NADA + 0.6, "borrar", 0.5, dur=0.6)
for _i in range(3):
    snd(INI(E6, 2) + 1.6 + _i * 0.3, "sello", 0.5)

# ======================================================================== 7. MATANZA (fiesta de Tóxcatl)
E7 = "matanza"
T_ATAQUE = w_(E7, 1, 10)


@shot(T0(E7), bg=lambda t: bg_grad((10, 20, 60), (24, 60, 120)), ent=("tinta", 0.7))
def m_sale(lz, t):
    c = Klog(t, [(T0(E7), (-98.0, 19.25, 1.35)), (108.4, (-97.8, 19.3, 1.5))])
    MP.mapa(lz, t, c, dict(ciudad_alfa=0.0, cdmx=0.0))
    u = K(t, [(INI(E7, 0) + 0.4, 0.0), (w_(E7, 0, 9), 1.0)], e_inout)
    ruta = np.array([MP.XY(-99.13, 19.43), MP.XY(-98.4, 19.2), MP.XY(-97.4, 19.35), MP.XY(-96.42, 19.43)])
    pts = catmull(ruta, 14)
    cx, cy = MP.XY(c[0], c[1])
    z = c[2]
    with lz.grupo(960 - cx * z, 540 - cy * z, z):
        P.discontinua(lz, pts, (255, 214, 96), ancho=9.0 / z ** 0.5, largo=36 / z ** 0.5, hueco=24 / z ** 0.5, fase=-t * 40 / z ** 0.5, frac=u)
        hx, hy = pts[min(len(pts) - 1, int(u * (len(pts) - 1)))]
        with lz.grupo(hx, hy, 0.5 / z):
            F.caballo(lz, 0, 0, 0.9, t, paso=1.6, lado=1, carga=0, seed=4)
    MP.marcador(lz, c, MP.CDMX, "Tenochtitlan", alfa=smooth(prog(t, T0(E7), T0(E7) + 0.5)), dy=-56, px=34)
    MP.marcador(lz, c, (-96.42, 19.43), "Cempoala · otro capitán", alfa=smooth(prog(t, w_(E7, 0, 8), w_(E7, 0, 9) + 0.3)), dy=-56, px=34)
    a = vent(t, w_(E7, 0, 12) - 0.4, T_ATAQUE - 0.4, 0.4, 0.3)
    if a > 0.01:
        px, py = MP.scr(c, *MP.CDMX)
        with lz.capa(2):
            F.soldado(lz, px + 70, py + 40, 1.0, t, lado=1, seed=9, tunica=(206, 110, 60), brazos=(-2.6, 0.4))
            lz.relleno(rect_red(px + 96, py - 100, 5, 128, 2), (120, 90, 60), alfa=a)
            lz.relleno(np.array([[px + 100, py - 100], [px + 168, py - 82], [px + 100, py - 62]]), (230, 60, 70), alfa=a)
            P.pastilla(lz, px + 90, py - 130, "Pedro de Alvarado al mando", px=32, alfa=a)


snd(T0(E7) + 0.4, "pasos", 0.3, dur=4.5)
snd(w_(E7, 0, 12), "pop", 0.4)

DANZ = 30


def _plaza(lz, t):
    cx, cy, R = W / 2, 500.0, 400.0
    lz.relleno(rect_red(cx - R - 40, cy - R - 40, 2 * R + 80, 2 * R + 80, 14), (176, 140, 126))
    lz.relleno(rect_red(cx - R, cy - R, 2 * R, 2 * R, 8), (238, 222, 192))
    for k in range(-6, 7):
        lz.relleno(rect_red(cx - R, cy + k * 66 - 1, 2 * R, 2, 0), (214, 194, 164), alfa=0.6)
        lz.relleno(rect_red(cx + k * 66 - 1, cy - R, 2, 2 * R, 0), (214, 194, 164), alfa=0.6)
    for i in range(5):
        h = 120 - i * 22
        lz.relleno(rect_red(cx - h, cy - h, 2 * h, 2 * h, 0), (250, 236, 210) if i % 2 == 0 else (206, 176, 150))
    lz.relleno(rect_red(cx - 12, cy - 12, 24, 24, 0), (222, 70, 78))
    for (gx, gy, w, h) in ((cx - 40, cy - R - 6, 80, 12), (cx - 40, cy + R - 6, 80, 12), (cx - R - 6, cy - 40, 12, 80), (cx + R - 6, cy - 40, 12, 80)):
        lz.relleno(rect_red(gx, gy, w, h, 2), (110, 84, 96))


def _bailarin(lz, x, y, s, t, k, viva=1.0):
    col = [(250, 240, 220), (222, 74, 84), (66, 190, 190), (255, 206, 80)][k % 4]
    if viva < 1.0:
        col = P.mezcla(col, (130, 130, 140), 1 - viva)
    lz.relleno(circulo(x, y, 15 * s, 14), col, alfa=0.4 + 0.6 * viva)
    lz.relleno(circulo(x, y - 3 * s, 8 * s, 10), (176, 116, 80), alfa=0.4 + 0.6 * viva)
    if viva > 0.5:
        for j in range(6):
            a = j / 6 * 6.283 + t * 2
            lz.relleno(elipse(x + math.cos(a) * 15 * s, y + math.sin(a) * 15 * s, 3.2 * s, 7 * s, a + 1.57, 6), [(60, 200, 130), (255, 210, 80), (230, 80, 90)][j % 3])


@shot(w_(E7, 0, 15) + 0.8, bg=lambda t: bg_grad((58, 40, 84), (34, 24, 60)), ent=("aberracion", 0.6))
def m_plaza(lz, t):
    _plaza(lz, t)
    cx, cy = W / 2, 500.0
    muertos = 0
    for anillo, (r, n, w) in enumerate(((300, 20, 0.42), (215, 14, -0.55))):
        for k in range(n):
            a = k / n * 6.283 + t * w
            x, y = cx + math.cos(a) * r * 1.0, cy + math.sin(a) * r * 1.0
            td = T_ATAQUE + 0.9 + 2.6 * h01(7, anillo * 40 + k)
            viva = 1.0 - smooth(prog(t, td, td + 0.4))
            if viva < 0.5 and t > td + 0.4:
                muertos += 1
            _bailarin(lz, x, y + 4 * math.sin(t * 6 + k), 1.4, t, k, viva)
    # atacantes: cuatro pelotones que entran por las puertas hacia el centro
    u = smooth(prog(t, T_ATAQUE, T_ATAQUE + 2.6))
    for g, (ang, gx, gy) in enumerate(((math.pi, 560, 500), (0, 1360, 500), (-math.pi / 2, 960, 100), (math.pi / 2, 960, 900))):
        for k in range(6):
            off = (k - 2.5) * 22
            sx = gx + (cx - gx) * u * 0.62 + (off if g >= 2 else 0)
            sy = gy + (cy - gy) * u * 0.62 + (off if g < 2 else 0)
            if u > 0.001:
                lz.relleno(circulo(sx, sy, 21, 14), (172, 180, 200))
                lz.relleno(circulo(sx, sy, 11, 10), (206, 70, 62))
                lz.trazo(np.array([[sx, sy], [sx + math.cos(ang + 3.14) * -48, sy + math.sin(ang + 3.14) * -48]]), (230, 236, 250), 6.0, temblor=0.0, capa=2)
    if u > 0.02:
        lz.relleno(PANT, (230, 40, 50), alfa=0.16 * u, capa=2)
    cifra(lz, t, w_(E7, 1, 1), "mayo de 1520", W / 2, 110, px=70, col=BLANCO, t1=T_ATAQUE + 0.2)
    etq(lz, t, w_(E7, 1, 6), T_ATAQUE + 0.4, "Fiesta de Tóxcatl · Templo Mayor", 300, 200, px=34)
    cifra(lz, t, w_(E7, 1, 13), "cientos de nobles", W / 2, 110, px=70, col=(255, 110, 110), t1=INI(E7, 2) - 0.2)


snd(w_(E7, 0, 15) + 0.8, "whoosh", 0.4, dur=0.7)
snd(w_(E7, 1, 6), "campana", 0.35)
snd(T_ATAQUE, "impacto", 0.6)
for _k in range(10):
    snd(T_ATAQUE + 0.9 + 2.6 * h01(7, _k * 4), "golpe_suave", 0.25)


def _cerco(lz, t, c, t_ini, t_fin, radio0=1.3, radio1=0.28, n=44, col=(60, 200, 210)):
    """Anillo de guerreros (puntos) que se cierra sobre el palacio (en km), dibujado dentro de la cámara del mapa."""
    px, py = ML.km(-0.35, 0.05)
    u = smooth(prog(t, t_ini, t_fin))
    r = lerp(radio0, radio1, u) * ML.PXKM
    for k in range(n):
        a = k / n * 6.283 + 0.4 * math.sin(t * 0.7)
        rr = r * (1 + 0.06 * math.sin(k * 3.1 + t * 4))
        x, y = px + math.cos(a) * rr, py + math.sin(a) * rr
        lz.relleno(circulo(x, y, 6.5, 10), col)
        lz.relleno(circulo(x, y - 2, 3.0, 8), (255, 214, 96))
    for k in range(8):
        a = k / 8 * 6.283 + t
        lz.relleno(circulo(px + math.cos(a) * 16, py + math.sin(a) * 12, 5.5, 10), (206, 70, 62))
    lz.halo(px, py, 50, (255, 120, 90), alfa=0.5 * u)


@shot(INI(E7, 2) - 0.1, bg=lambda t: bg_plano((30, 30, 70)), ent=("glitch", 0.5))
def m_ciudad(lz, t):
    c = Klog(t, [(INI(E7, 2) - 0.1, (0.0, 0.0, 1.5)), (120.5, (-0.35, 0.05, 3.6)), (T1(E7), (-0.35, 0.05, 4.0))])
    ML.dibujar_valle(lz, t, c, noche=0.45, luces=0.5, detalle=1.0)
    tw = w_(E7, 2, 2)
    with cam(lz, c[0] * ML.PXKM, -c[1] * ML.PXKM, c[2]):
        I = ML.isla_pts()
        with lz.recorte(I):
            for k in range(3):
                u = prog(t, tw + 0.35 * k, tw + 0.35 * k + 2.2)
                if 0 < u < 1:
                    lz.relleno(circulo(0, 0, 40 + 210 * u, 40), (230, 50, 60), alfa=0.32 * (1 - u))
            u = smooth(prog(t, tw, tw + 2.5))
            lz.relleno(circulo(0, 0, 400, 40), (230, 50, 60), alfa=0.22 * u)
        _cerco(lz, t, c, w_(E7, 2, 8), T1(E7) - 0.2)
        px, py = ML.km(-0.35, 0.05)
        F.palacio(lz, px, py + 24, 0.14)
    a = smooth(prog(t, w_(E7, 2, 12), w_(E7, 2, 13)))
    if a > 0.01:
        sx, sy = km2s_(c, -0.35, 0.05)
        with lz.capa(2):
            P.pastilla(lz, sx, sy - 150, "españoles sitiados en el palacio", px=36, alfa=a)
    gran(lz, t, tw, tw + 2.5, "LA CIUDAD ESTALLÓ", W / 2, 130, px=96, col=(255, 110, 110))


def km2s_(c, x, y):
    return W / 2 + (x - c[0]) * ML.PXKM * c[2], H / 2 - (y - c[1]) * ML.PXKM * c[2]


snd(w_(E7, 2, 2), "impacto", 0.6)
snd(w_(E7, 2, 2) + 0.2, "zoom_whoosh", 0.4, dur=1.5)
snd(w_(E7, 2, 8), "pasos", 0.3, dur=3.0)

# ======================================================================== 8. MUERTE DE MOCTEZUMA (dos versiones)
E8 = "muerte"
GY8 = 850.0


def _fachada(lz, x, y, s, t, luz=0.0):
    F.palacio(lz, x, y, s, luz=luz)


def _multitud(lz, t, xs, y, s, mirar_a, k0, agita=1.0, lanzan=None):
    for i, x in enumerate(xs):
        lado = 1 if x < mirar_a else -1
        br = (-2.3 + 0.4 * math.sin(t * 6 + i), 2.3 - 0.4 * math.sin(t * 5 + i)) if agita else None
        F.guerrero(lz, x, y + 8 * (i % 2), s, t, paso=0.0, lado=lado, arma=None, escudo=False, plumas=i + k0, seed=i + k0, brazos=br)


@shot(T0(E8), bg=lambda t: bg_grad((90, 170, 240), (255, 226, 190), ym=0.5), ent=("tinta", 0.7))
def mu_azotea(lz, t):
    with lz.grupo(0, 0, 1.0):
        for i in range(7):
            x = 200 + i * 260
            lz.relleno(rect_red(x - 90, 600 - 60 * h01(3, i), 180, 400, 3), (236, 222, 204) if i % 2 else (222, 204, 186))
    lz.relleno(rect_red(-20, GY8, W + 40, 260, 0), (214, 180, 140))
    _fachada(lz, 900, GY8, 2.3, t)
    # escalera lateral y azotea
    lz.relleno(np.array([[1470, GY8], [1600, GY8], [1600, 458], [1440, 458]]), (206, 178, 150))
    for k in range(9):
        lz.relleno(rect_red(1470 + k * 4, GY8 - 40 * k - 14, 130 - k * 4, 8, 0), (176, 148, 130))
    # Moctezuma sube y levanta los brazos
    u = smooth(prog(t, T0(E8) + 0.3, 127.6))
    x = lerp(1560, 1130, smooth(prog(t, 127.0, 127.9)))
    y = lerp(GY8 - 6, 462, u) if t < 127.0 else 462
    F.tlatoani(lz, x if t >= 127.0 else 1560 - (1 - 1) * 0, y, 1.9, t, lado=-1, brazos=smooth(prog(t, 127.9, 128.5)) * 0.9, paso=1.0 if 0.02 < u < 0.99 else 0.0, seed=3)
    for k, dx in enumerate((-90, -30)):
        F.soldado(lz, 1230 + dx * 0 + k * 70 + 0, 462, 1.9, t, lado=-1, arma="lanza", seed=k + 60)
    _multitud(lz, t, [180 + 120 * i for i in range(14)], GY8, 1.7, 1130, 40, agita=1.0)
    etq(lz, t, T0(E8) + 0.5, 128.6, "Moctezuma intenta calmar a su pueblo", W / 2, 240, px=38)


snd(T0(E8) + 0.3, "pasos", 0.3, dur=2.4)
snd(127.9, "hmm", 0.35)


def _panel(lz, x0, x1, titulo, t, izq=True):
    lz.relleno(rect_red(x0 - 8, 92, x1 - x0 + 16, 770, 22), (255, 255, 255), alfa=0.9)
    with lz.recorte(rect_red(x0, 100, x1 - x0, 754, 16)):
        degradado_v(lz, x0, x1, 100, 854, (110, 180, 244), (255, 226, 190), 100, 854, paso=14.0)
        lz.relleno(rect_red(x0, 780, x1 - x0, 90, 0), (214, 180, 140))
        F.palacio(lz, (x0 + x1) / 2, 780, 1.7)


@shot(w_(E8, 1, 0) - 0.3, bg=lambda t: bg_plano((44, 30, 100)), ent=("fuga", 0.7))
def mu_versiones(lz, t):
    xa0, xa1, xb0, xb1 = 40.0, 940.0, 980.0, 1880.0
    _panel(lz, xa0, xa1, "", t)
    _panel(lz, xb0, xb1, "", t)
    tA = w_(E8, 1, 12)
    tB = w_(E8, 1, 21)
    ts = w_(E8, 1, 2)
    with lz.recorte(rect_red(xa0, 100, xa1 - xa0, 754, 16)):
        xm = 700.0
        caida = smooth(prog(t, tA + 1.4, tA + 2.2))
        with lz.grupo(xm, 500, 1.0, 1.35 * caida):
            F.tlatoani(lz, 0, 0, 1.5, t, lado=-1, brazos=0.5 * (1 - caida), seed=3)
        for i in range(10):
            xi = 120 + 60 * i
            F.guerrero(lz, xi, 778, 1.05, t, paso=0.0, lado=1, arma=None, escudo=False, plumas=i, seed=i + 90, brazos=(-2.2, 2.0 * math.sin(t * 6 + i)))
            # piedras en parábola desde la multitud hasta la azotea
            for j in range(2):
                uu = ((t - tA - 0.15 * i - 0.5 * j) * 0.9) % 1.6 if t > tA else 9
                if 0 < uu < 1.0:
                    px = lerp(xi + 20, xm, uu)
                    py = lerp(690, 500, uu) - 300 * math.sin(math.pi * uu)
                    lz.relleno(circulo(px, py, 13, 10), (150, 150, 160))
    with lz.recorte(rect_red(xb0, 100, xb1 - xb0, 754, 16)):
        xm = 1640.0
        caida = smooth(prog(t, tB + 0.6, tB + 1.4))
        with lz.grupo(xm, 500, 1.0, -1.35 * caida):
            F.tlatoani(lz, 0, 0, 1.5, t, lado=-1, brazos=0.3 * (1 - caida), seed=3)
        F.soldado(lz, xm - 150 + 60 * smooth(prog(t, tB - 0.3, tB + 0.3)), 500, 1.5, t, lado=1, arma="espada", seed=61,
                  brazos=(-0.3, 1.0 + 1.6 * math.sin(t * 9) * smooth(prog(t, tB + 0.3, tB + 0.9)) * (1 - caida)))
        for i in range(7):
            F.guerrero(lz, 1050 + 60 * i, 778, 1.05, t, paso=0.0, lado=1, arma=None, escudo=False, plumas=i, seed=i + 95, brazos=None)
    with lz.capa(2):
        lz.relleno(circulo(960, 470, 70, 30), (255, 255, 255), alfa=0.95)
    P.rotulo(lz, 960, 472, "?", px=130, color=(226, 70, 70), sombra=0.0, capa=2)
    a = smooth(prog(t, w_(E8, 1, 0), w_(E8, 1, 1)))
    P.rotulo(lz, 490, 130 - 0, "Versión española", px=44, color=(34, 28, 80), sombra=0.0, alfa=a)
    P.rotulo(lz, 1430, 130, "Fuentes indígenas", px=44, color=(34, 28, 80), sombra=0.0, alfa=a)
    etq(lz, t, tA, tA + 3.0, "«Lo apedrearon los mexicas»", 490, 200, px=34)
    etq(lz, t, tB, tB + 2.6, "«Lo mataron los españoles»", 1430, 200, px=34)
    cifra(lz, t, w_(E8, 1, 1), "junio de 1520", W / 2, 60, px=44, col=(255, 255, 255), t1=T1(E8) - 3.5)


snd(w_(E8, 1, 0), "whoosh", 0.4, dur=0.8)
for _k in range(6):
    snd(w_(E8, 1, 12) + 0.6 + _k * 0.35, "pop", 0.25)
snd(w_(E8, 1, 21) + 0.6, "golpe_suave", 0.4)


@shot(INI(E8, 2) - 0.1, bg=lambda t: bg_plano((30, 30, 70)), ent=("tinta", 0.7))
def mu_escapa(lz, t):
    c = Klog(t, [(INI(E8, 2) - 0.1, (-0.6, 0.05, 2.0)), (140.0, (-1.6, 0.05, 2.6)), (T1(E8), (-2.0, 0.05, 2.6))])
    ML.dibujar_valle(lz, t, c, noche=0.55, luces=0.7, detalle=1.0)
    with cam(lz, c[0] * ML.PXKM, -c[1] * ML.PXKM, c[2]):
        _cerco(lz, t, c, INI(E8, 2), w_(E8, 2, 7), radio0=1.2, radio1=0.5)
        pts = np.array([ML.km(-0.35, 0.05), ML.km(-1.35, 0.05), ML.km(-2.9, 0.05), ML.km(-4.6, 0.1)])
        u = smooth(prog(t, w_(E8, 2, 7), T1(E8) - 0.2))
        P.discontinua(lz, pts, (255, 226, 130), ancho=7.0, largo=26, hueco=18, fase=-t * 40, frac=u)
        px, py = ML.km(-0.35, 0.05)
        F.palacio(lz, px, py + 24, 0.14)
    gran(lz, t, w_(E8, 2, 3), w_(E8, 2, 7), "LA CIUDAD SE LEVANTÓ EN ARMAS", W / 2, 130, px=76, col=(255, 130, 110))
    gran(lz, t, w_(E8, 2, 8), T1(E8) - 0.1, "Cortés decide escapar", W / 2, 130, px=86, col=(255, 226, 130))


snd(INI(E8, 2), "impacto", 0.5)
snd(w_(E8, 2, 8), "whoosh", 0.45, dur=0.8)
