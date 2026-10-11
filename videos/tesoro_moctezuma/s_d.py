# -*- coding: utf-8 -*-
"""Escenas 13-16: cuauhtemoc (caída de la ciudad, interrogatorio, oro al lago, sospechas), lago (el lago se seca y la ciudad crece),
subsuelo (corte de sección del centro, el monolito y el Templo Mayor) y barra (mapa del centro, hallazgo de 1981, análisis, ruta y hueco)."""
import math

import numpy as np

from motor import W, H, prog, lerp, smooth, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, blob, catmull, bezier, h01
import plano as P
import mapa_local as ML
import figuras as F
from mundo import degradado_v, llama, humo
from reg import shot, snd
from util import *

PANT = np.array([[0, 0], [W, 0], [W, H], [0, H]], float)


def burbuja(lz, x, y, txt, a, px=36, cola=1, w=None):
    """Globo de diálogo blanco con texto oscuro."""
    if a <= 0.01:
        return
    from motor import ancho_texto
    ww = (w or (len(txt) * px * 0.55 + 60))
    with lz.capa(2):
        lz.relleno(rect_red(x - ww / 2, y - px * 0.9, ww, px * 1.8, px * 0.6), (255, 255, 255), alfa=0.96 * a)
        lz.relleno(np.array([[x - 12 * cola - 4, y + px * 0.85], [x + 22 * cola, y + px * 0.85], [x + 30 * cola, y + px * 1.6]]), (255, 255, 255), alfa=0.96 * a)
        P.rotulo(lz, x, y, txt, px=px, color=(34, 28, 80), sombra=0.0, alfa=a)


# ======================================================================== 13. CUAUHTÉMOC
E13 = "cuauhtemoc"
GY13 = 830.0


def _cofre_vacio(lz, x, y, s, abre, t):
    with lz.grupo(x, y, s):
        lz.relleno(rect_red(-52, -44, 104, 44, 6), (140, 92, 58))
        lz.relleno(rect_red(-52, -26, 104, 7, 1), (94, 60, 44))
        if abre > 0.05:
            lz.relleno(elipse(0, -44, 46, 10, 0.0, 20), (24, 14, 30))
        lz.relleno(np.array([[-52, -44], [52, -44], [46, -44 - 34 * (1 - abre)], [-46, -44 - 34 * (1 - abre)]]) + np.array([0, -52 * abre]) * np.array([0, 1]) * 0, (172, 122, 78), alfa=0.0)
        with lz.grupo(-52, -44, 1.0, -1.55 * abre):
            lz.relleno(np.array([[0, 0], [104, 0], [98, -34], [6, -34]]), (172, 122, 78))
            lz.relleno(rect_red(0, -8, 104, 8, 2), F.ORO_S)
        lz.relleno(rect_red(-6, -30, 12, 14, 2), F.ORO_S)


@shot(T0(E13), bg=lambda t: bg_grad((120, 40, 64), (28, 18, 48)), ent=("tinta", 0.7))
def c_cae(lz, t):
    tc = w_(E13, 0, 3)
    for i in range(-2, 12):
        x = i * 200 + 40 * h01(2, i)
        h = 110 + 90 * h01(3, i)
        w = 150 + 40 * h01(4, i)
        lz.relleno(rect_red(x - w / 2, GY13 - h, w, h, 3), (56, 34, 70))
    F.templo_mayor(lz, 960, GY13, 1.55)
    lz.relleno(rect_red(-20, GY13, W + 40, 260, 0), (42, 28, 56))
    for i in range(14):
        x = 60 + i * 140 + 30 * h01(5, i)
        s = 0.8 + 0.8 * h01(6, i)
        u = smooth(prog(t, tc + 0.2 * h01(7, i), tc + 1.5))
        llama(lz, x, GY13 - 20 - 40 * (i % 3), s * u, t, seed=i, alfa=u)
        humo(lz, x, GY13 - 90 - 40 * (i % 3), t, tc + 0.5, n=4, s=1.0 * s, alfa=0.4, seed=i, col=(50, 34, 60))
    lz.halo(960, 560, 520, (255, 120, 60), alfa=0.35 * smooth(prog(t, tc, tc + 1.5)))
    # bandera española que se iza
    izar = smooth(prog(t, tc + 0.4, tc + 2.2))
    px, top = 1560.0, 300.0
    py = lerp(GY13 - 30, top, izar)
    lz.relleno(rect_red(px - 5, top, 10, GY13 - top, 3), (200, 190, 180))
    bx = px + 8
    pts_t = [(bx + k * 20, py + 6 * math.sin(t * 5 + k * 0.7) * (k / 9)) for k in range(10)]
    pts_b = [(bx + k * 20, py + 110 + 6 * math.sin(t * 5 + k * 0.7) * (k / 9)) for k in range(9, -1, -1)]
    lz.relleno(np.array(pts_t + pts_b), (206, 44, 56))
    lz.relleno(np.array([(bx + 70, py + 20), (bx + 110, py + 20), (bx + 110, py + 92), (bx + 70, py + 92)]) * 0 + np.array([(bx + 84, py + 12), (bx + 100, py + 12), (bx + 100, py + 98), (bx + 84, py + 98)]), (255, 240, 200))
    lz.relleno(np.array([(bx + 50, py + 46), (bx + 134, py + 46), (bx + 134, py + 62), (bx + 50, py + 62)]), (255, 240, 200))
    # calendario
    a = vent(t, w_(E13, 0, 5), w_(E13, 0, 13), 0.4, 0.4)
    if a > 0.01:
        with lz.capa(2):
            lz.relleno(rect_red(140, 180, 300, 300, 26), (255, 255, 255), alfa=0.96 * a)
            lz.relleno(rect_red(140, 180, 300, 84, 26), (226, 70, 70), alfa=a)
            lz.relleno(rect_red(140, 236, 300, 28, 0), (226, 70, 70), alfa=a)
            P.rotulo(lz, 290, 224, "AGOSTO 1521", px=38, color=(255, 255, 255), sombra=0.0, alfa=a)
            P.rotulo(lz, 290, 372, "13", px=170, color=(34, 28, 80), sombra=0.0, alfa=a)
    # el cofre está vacío
    tv = w_(E13, 0, 13)
    k = e_back(prog(t, tv - 0.4, tv + 0.3))
    if k > 0.02:
        _cofre_vacio(lz, 1240, GY13 + 10, 2.4 * k, smooth(prog(t, tv + 0.2, tv + 1.0)), t)
        if t > tv + 0.6:
            for i in range(6):
                u = ((t - tv - 0.6) * 0.8 + i / 6) % 1.0
                lz.relleno(circulo(1240 + 50 * math.sin(i * 2.4 + t), GY13 - 170 - u * 120, 9 + 10 * u, 10), (200, 190, 200), alfa=0.35 * (1 - u))
    gran(lz, t, tv + 0.5, T1(E13) - 0.1, "VACÍO", 1240, 500, px=110, col=(255, 210, 120)) if False else None
    etq(lz, t, tv + 0.9, INI(E13, 1) - 0.2, "el cofre estaba vacío", 1240, 560, px=38)


snd(T0(E13) + 0.2, "fuego", 0.4, dur=6.0)
snd(w_(E13, 0, 3), "impacto", 0.6)
snd(w_(E13, 0, 5), "pop", 0.4)
snd(w_(E13, 0, 13), "campana", 0.4)
snd(w_(E13, 0, 14), "hmm", 0.45)


@shot(INI(E13, 1) - 0.1, bg=lambda t: bg_grad((54, 34, 44), (22, 14, 30)), ent=("fuga", 0.7))
def c_interroga(lz, t):
    zoom = K(t, [(INI(E13, 1) - 0.1, 1.0), (INI(E13, 3), 1.14)], e_inout)
    with lz.grupo(640, 500, zoom):
        tarjeta(lz, "suplicio", 0, 0, 1000, alfa=smooth(prog(t, INI(E13, 1), INI(E13, 1) + 0.5)), capa=1)
    P.pastilla(lz, 640, 900, "«El suplicio de Cuauhtémoc» · Leandro Izaguirre, 1893", px=28, alfa=smooth(prog(t, INI(E13, 1) + 0.4, INI(E13, 1) + 1.0)))
    # figuras que representan la escena, con globos
    F.soldado(lz, 1400, 840, 2.1, t, lado=-1, arma=None, seed=1, tunica=(150, 40, 60), brazos=(-0.3, 1.4 + 0.2 * math.sin(t * 3)))
    F.tlatoani(lz, 1700, 840, 2.1, t, lado=-1, seed=9, manto=(230, 120, 70))
    burbuja(lz, 1400, 420, "¿Dónde está el oro?", smooth(prog(t, w_(E13, 1, 1), w_(E13, 1, 1) + 0.4)) * (1 - smooth(prog(t, INI(E13, 2) - 0.3, INI(E13, 2)))), px=34)
    burbuja(lz, 1700, 430, "Se perdió…", smooth(prog(t, w_(E13, 1, 5), w_(E13, 1, 5) + 0.4)) * (1 - smooth(prog(t, INI(E13, 2) - 0.3, INI(E13, 2)))), px=34, cola=-1)
    # aceite hirviendo sobre el brasero
    a = smooth(prog(t, INI(E13, 2), INI(E13, 2) + 0.5))
    if a > 0.01:
        with lz.capa(2):
            F.brasero(lz, 1560, 690, 1.4, t)
            lz.relleno(np.array([[1500, 560], [1620, 560], [1600, 640], [1520, 640]]), (52, 46, 62), alfa=a)
            lz.relleno(elipse(1560, 560, 60, 12, 0.0, 20), (240, 190, 60), alfa=a)
            for i in range(5):
                ph = (t * 1.6 + i * 0.25) % 1.0
                lz.relleno(circulo(1530 + i * 16, 556 - 14 * ph, 4 + 3 * ph, 8), (255, 236, 150), alfa=(1 - ph) * a)
        P.pastilla(lz, 1560, 780, "aceite hirviendo", px=34, alfa=a)


snd(INI(E13, 1), "whoosh", 0.4, dur=0.7)
snd(INI(E13, 2), "fuego", 0.4, dur=2.5)
snd(INI(E13, 2) + 0.2, "siseo", 0.3)


@shot(INI(E13, 3) - 0.1, bg=lambda t: bg_grad((255, 150, 110), (255, 220, 170), ym=0.6), ent=("tinta", 0.7))
def c_lago(lz, t):
    ys = 760.0
    for i in range(6):
        x = 200 + i * 340
        lz.relleno(circulo(x, 220 + 60 * h01(3, i), 60, 20), (255, 236, 220), alfa=0.6)
        lz.relleno(circulo(x + 60, 236 + 60 * h01(3, i), 44, 20), (255, 236, 220), alfa=0.6)
    lz.relleno(np.array([[0, 700], [300, 640], [700, 690], [1100, 630], [1500, 680], [1920, 650], [1920, 800], [0, 800]]), (210, 120, 120))
    agua(lz, -50, W + 50, ys, H + 50, t, (60, 130, 200), (20, 50, 120), amp=6, luna=None)
    lz.relleno(rect_red(-50, ys - 34, 1200, 44, 0), (206, 176, 140))
    lz.relleno(rect_red(-50, ys - 34, 1200, 8, 0), (240, 214, 176))
    for i in range(4):
        F.guerrero(lz, 300 + 210 * i, ys - 34, 1.9, t, paso=0.0, lado=1, arma=None, escudo=False, plumas=i, seed=i + 60,
                   brazos=(-0.4, 2.2 - 1.2 * math.sin(t * 5 + i) ** 2))
    tt0 = w_(E13, 3, 9)
    for i in range(4):
        for k in range(3):
            ts = tt0 + 0.42 * i + 1.0 * k
            u = prog(t, ts, ts + 0.9)
            if 0 < u < 1:
                x = lerp(340 + 210 * i, 1500 + 90 * i + 40 * k, e_inout(u))
                y = lerp(ys - 200, ys + 24, e_in(u)) - 300 * math.sin(math.pi * u)
                F.barra_oro(lz, x, y, 0.8, 0.9 * u, 0.6)
            if u >= 1.0 and t < ts + 2.2:
                chapoteo(lz, 1500 + 90 * i + 40 * k, ys + 30, t, ts + 0.9, 1.0)
    # calendario: cuatro días antes de la captura
    tt = w_(E13, 3, 5)
    for i, txt in enumerate(("4", "3", "2", "1", "Captura")):
        a = e_back(prog(t, tt + 0.3 * i, tt + 0.3 * i + 0.4))
        if a <= 0.02:
            continue
        x = 560 + i * 200
        with lz.capa(2):
            fin = i == 4
            lz.relleno(rect_red(x - 84 * a, 120 - 0 * a, 168 * a, 170 * a, 20), (226, 70, 70) if fin else (255, 255, 255), alfa=0.96)
            P.rotulo(lz, x, 205, txt, px=92 if not fin else 44, color=(255, 255, 255) if fin else (34, 28, 80), sombra=0.0, alfa=a)
            if not fin:
                P.rotulo(lz, x, 150, "días antes" if i == 0 else "", px=22, color=(120, 110, 150), sombra=0.0, alfa=a)
    etq(lz, t, w_(E13, 3, 0), w_(E13, 3, 3) + 0.8, "Según las crónicas", 500, 330, px=38)


snd(INI(E13, 3), "whoosh", 0.4, dur=0.7)
for _i in range(5):
    snd(w_(E13, 3, 5) + 0.3 * _i, "tick", 0.35)
for _i in range(4):
    for _k in range(3):
        snd(w_(E13, 3, 9) + 0.42 * _i + 1.0 * _k + 0.9, "chapuzon", 0.3)


@shot(INI(E13, 4) - 0.1, bg=lambda t: bg_grad((255, 226, 176), (255, 244, 220), ym=0.6), ent=("aberracion", 0.6))
def c_sospecha(lz, t):
    gy = 850.0
    lz.relleno(rect_red(-20, gy, W + 40, 260, 0), (214, 180, 140))
    for i in range(7):
        x = 100 + i * 300
        lz.relleno(rect_red(x - 100, 520 - 60 * h01(3, i), 200, 340, 3), (236, 222, 204) if i % 2 else (222, 204, 186))
    # bergantín y monedas que se van (la expedición)
    F.bergantin(lz, 230, 660, 1.5, t, lado=1, seed=2)
    tg = w_(E13, 4, 8)
    F.soldado(lz, 640, gy, 3.0, t, lado=1, arma=None, seed=1, tunica=(150, 40, 60), brazos=(-0.3, 1.2))
    bolsa = 1.0 - 0.85 * smooth(prog(t, tg + 0.6, tg + 4.0))
    with lz.capa(2):
        lz.relleno(blob(790, 640, 38 * bolsa + 8, 3, 0.1, 20, 4), F.ORO_S)
        lz.relleno(blob(768, 638, 32 * bolsa + 6, 3, 0.1, 20, 4), F.ORO)
    for k in range(14):
        u = prog(t, tg + 0.8 + 0.22 * k, tg + 1.9 + 0.22 * k)
        if 0 < u < 1:
            x = lerp(770, 260, e_inout(u))
            y = lerp(640, 660, u) - 240 * math.sin(math.pi * u)
            F.moneda(lz, x, y, 12)
    etq(lz, t, tg + 0.4, tg + 4.2, "gastó su fortuna en la expedición", 450, 300, px=36)
    # soldados que esperan su parte
    for i in range(6):
        vuelta = smooth(prog(t, INI(E13, 5), INI(E13, 5) + 0.6))
        F.soldado(lz, 1000 + 150 * i, gy + 6 * (i % 2), 2.5, t, lado=-1, arma=None, seed=i + 40,
                  brazos=(-1.6, 1.6) if t < INI(E13, 5) else (-0.3, 0.3))
    burbuja(lz, 1300, 420, "¿Y mi parte?", smooth(prog(t, w_(E13, 4, 3), w_(E13, 4, 3) + 0.4)) * (1 - smooth(prog(t, INI(E13, 5) - 0.2, INI(E13, 5)))), px=34)
    # sospechas
    for i in range(6):
        burbuja(lz, 1000 + 150 * i, 480 - 40 * (i % 2), "?", smooth(prog(t, w_(E13, 5, 3) + 0.15 * i, w_(E13, 5, 3) + 0.5 + 0.15 * i)), px=44, w=90)
    # el saco escondido
    b = smooth(prog(t, w_(E13, 5, 5), w_(E13, 5, 6)))
    if b > 0.01:
        with lz.capa(2):
            F.saco(lz, 500, gy - 8, 2.0, brillo=1.0)
    etq(lz, t, INI(E13, 5), T1(E13) - 0.2, "¿se quedó con parte del oro?", 900, 260, px=40)


snd(INI(E13, 4) - 0.1, "whoosh", 0.4, dur=0.6)
for _k in range(6):
    snd(w_(E13, 4, 8) + 0.9 + 0.5 * _k, "clink", 0.3, tono=1.0 - 0.03 * _k)
snd(w_(E13, 4, 3), "pop", 0.4)
snd(w_(E13, 5, 3), "hmm", 0.45)

# ======================================================================== 14. EL LAGO SE SECA
E14 = "lago"
TESO = [(-1.6, 0.06), (-2.2, 0.02), (-3.0, 0.08), (-3.8, 0.1), (-0.6, -0.15), (0.4, 0.3), (-1.0, 0.5), (1.1, -0.4), (-2.5, -0.1), (0.0, 0.0)]


@shot(T0(E14), bg=lambda t: bg_plano((20, 44, 100)), ent=("tinta", 0.7))
def l_seca(lz, t):
    tS, tE = w_(E14, 0, 6), w_(E14, 0, 10)
    lago = K(t, [(tS, 1.0), (tE, 0.05)], e_inout)
    mod = K(t, [(w_(E14, 0, 10), 0.0), (w_(E14, 0, 17), 1.0)], e_inout)
    noche = K(t, [(T0(E14), 0.1), (w_(E14, 0, 15), 0.2), (w_(E14, 0, 19), 0.85)])
    c = Klog(t, [(T0(E14), (2.5, -1.5, 0.82)), (T1(E14), (1.2, -0.6, 0.95))])
    ML.dibujar_valle(lz, t, c, noche=noche, luces=noche, detalle=1.0, lago=lago, moderna=mod, ciudad=1.0)
    with cam(lz, c[0] * ML.PXKM, -c[1] * ML.PXKM, c[2]):
        for k, (x, y) in enumerate(TESO):
            X, Y = ML.km(x, y)
            a = smooth(prog(t, INI(E14, 1) + 0.2 + 0.12 * k, INI(E14, 1) + 0.8 + 0.12 * k))
            if a > 0.01:
                lz.halo(X, Y, 26 + 6 * math.sin(t * 4 + k), ORO, alfa=0.7 * a)
                lz.relleno(circulo(X, Y, 3.5, 8), (255, 250, 210), alfa=a)
    # contador de años
    anio = int(K(t, [(T0(E14) + 0.5, 1521), (tS, 1521), (w_(E14, 0, 8), 1607), (tE, 1900), (w_(E14, 0, 17), 2025)]))
    with lz.capa(2):
        lz.relleno(rect_red(90, 90, 360, 140, 28), (255, 255, 255), alfa=0.92)
        P.rotulo(lz, 270, 160, str(anio), px=110, color=(34, 28, 80), sombra=0.0)
    etq(lz, t, w_(E14, 0, 8), w_(E14, 0, 10), "Desagüe del valle", 270, 260, px=34)
    gran(lz, t, w_(E14, 0, 17), w_(E14, 0, 19) + 2.0, "CIUDAD DE MÉXICO", W / 2, 130, px=88)
    gran(lz, t, w_(E14, 0, 1), w_(E14, 0, 3) + 1.4, "NUNCA APARECIÓ", W / 2, 130, px=88, col=(255, 210, 120))


snd(T0(E14) + 0.3, "viento", 0.3, dur=3.0)
snd(w_(E14, 0, 6), "ola", 0.4, dur=1.4)
snd(w_(E14, 0, 10), "zoom_whoosh", 0.4, dur=1.4)
snd(w_(E14, 0, 17), "pop", 0.35)


@shot(INI(E14, 1) - 0.1, bg=lambda t: bg_plano((20, 24, 60)), ent=("fuga", 0.6))
def l_asfalto(lz, t):
    c = Klog(t, [(INI(E14, 1) - 0.1, (1.2, -0.6, 0.95)), (w_(E14, 1, 5), (-2.0, 0.0, 2.4)), (T1(E14), (-2.4, 0.0, 2.6))])
    ML.dibujar_valle(lz, t, c, noche=0.9, luces=1.0, detalle=1.0, lago=0.05, moderna=1.0)
    # escáner que baja revelando los destellos de oro
    yscan = K(t, [(w_(E14, 1, 4), -100.0), (w_(E14, 1, 9) + 0.8, H + 100.0)], e_inout)
    with lz.capa(2):
        lz.relleno(rect_red(0, yscan - 6, W, 12, 3), (110, 240, 220), alfa=0.8)
        lz.relleno(rect_red(0, yscan - 60, W, 54, 0), (110, 240, 220), alfa=0.10)
    for k, (x, y) in enumerate(TESO):
        sx, sy = W / 2 + (x - c[0]) * ML.PXKM * c[2], H / 2 - (y - c[1]) * ML.PXKM * c[2]
        a = smooth(prog(yscan - sy, 0, 80))
        if a > 0.01:
            with lz.capa(2):
                lz.halo(sx, sy, 60 + 14 * math.sin(t * 4 + k), ORO, alfa=0.85 * a)
                F.barra_oro(lz, sx, sy, 0.5 * a, 0.3 * (k - 4) * 0.2, 0.0)
    gran(lz, t, w_(E14, 1, 7), T1(E14) - 0.1, "BAJO EL ASFALTO", W / 2, 130, px=92, col=(255, 226, 130))


snd(INI(E14, 1), "whoosh", 0.4, dur=0.7)
snd(w_(E14, 1, 4), "zoom_whoosh", 0.35, dur=2.0)
for _k in range(6):
    snd(w_(E14, 1, 5) + 0.25 * _k, "bling", 0.25, tono=0.8 + 0.06 * _k)

# ======================================================================== 15. SUBSUELO (corte de sección)
E15 = "subsuelo"
SY = 430.0


def _superficie(lz, t, x0=-300, x1=2500):
    for i in range(0, 12):
        x = x0 + 40 + i * 220
        h = 190 + 100 * h01(8, i)
        w = 190
        col = [(236, 190, 150), (214, 150, 120), (250, 226, 176), (190, 160, 200), (170, 210, 190)][i % 5]
        lz.relleno(rect_red(x - w / 2, SY - h, w, h, 4), col)
        lz.relleno(rect_red(x - w / 2, SY - h, w, 14, 0), P.oscurecer(col, 0.2))
        for j in range(2):
            for k in range(int(h // 90)):
                lz.relleno(rect_red(x - 60 + j * 70, SY - h + 40 + k * 80, 40, 52, 4), (100, 150, 200) if (i + j + k) % 3 else (255, 226, 130))
    lz.relleno(rect_red(x0, SY - 24, x1 - x0, 24, 0), (120, 118, 134))
    for i in range(6):
        cxx = ((t * (60 + 15 * i) + i * 500) % (x1 - x0 + 400)) + x0 - 200
        lz.relleno(rect_red(cxx, SY - 44, 90, 20, 6), [(226, 80, 80), (80, 140, 226), (240, 200, 80), (90, 190, 130), (250, 250, 250), (140, 90, 190)][i])
        lz.relleno(circulo(cxx + 20, SY - 22, 8, 10), (30, 30, 40))
        lz.relleno(circulo(cxx + 70, SY - 22, 8, 10), (30, 30, 40))
    for i in range(5):
        px = ((t * 26 * (1 if i % 2 else -1) + i * 480) % (x1 - x0)) + x0
        P.humano(lz, px, SY, 0.6, t, ropa=[(198, 80, 90), (90, 120, 200), (230, 190, 90), (120, 90, 170), (84, 170, 140)][i], paso=0.5, voltear=(i % 2 == 0))


def _capas_terreno(lz, alfa=1.0):
    """Capas del subsuelo: asfalto y cimientos, relleno colonial y lodo del antiguo lago (bandas con alfa)."""
    for (y0, y1, c0, c1, paso) in ((SY, SY + 120, (120, 116, 132), (176, 132, 96), 12.0), (SY + 120, SY + 340, (176, 132, 96), (140, 108, 100), 16.0),
                                   (SY + 340, SY + 1300, (120, 104, 118), (46, 40, 70), 30.0)):
        n = max(1, int((y1 - y0) / paso))
        for i in range(n):
            ya, yb = y0 + (y1 - y0) * i / n, y0 + (y1 - y0) * (i + 1) / n + 1.0
            u = (i + 0.5) / n
            lz.relleno(np.array([[-400, ya], [2600, ya], [2600, yb], [-400, yb]]), P.mezcla(c0, c1, u), alfa=alfa)


def _detalles_subsuelo(lz, t):
    """Cables (los electricistas), tubería, cascotes y raíces para que el terreno no quede vacío; etiquetas de capas."""
    for k in range(60):
        x = -300 + 50 * k
        lz.relleno(rect_red(x, SY + 58, 26, 9, 2), (255, 214, 60) if k % 2 == 0 else (40, 40, 52))
    lz.relleno(rect_red(-400, SY + 92, 3000, 14, 6), (70, 140, 210))
    lz.relleno(rect_red(-400, SY + 96, 3000, 4, 2), (150, 200, 250))
    for i in range(46):
        x = -300 + 2600 * h01(31, i)
        y = SY + 150 + 700 * h01(32, i) ** 1.3
        c = [(210, 160, 110), (150, 130, 150), (226, 190, 140), (120, 100, 120)][i % 4]
        lz.relleno(np.array([[x, y], [x + 22, y - 6], [x + 30, y + 10], [x + 6, y + 18]]) * 1.0, c, alfa=0.8)
    for i in range(14):
        x = -200 + 180 * i
        lz.trazo(np.array([[x, SY + 120], [x + 20 * math.sin(i), SY + 190], [x - 12, SY + 250]]), (110, 76, 60), 5.0, temblor=0.0, capa=1)
    for (yy, txt) in ((SY + 50, "cables y asfalto"), (SY + 215, "relleno colonial"), (SY + 560, "lodo del antiguo lago")):
        P.pastilla(lz, 230, yy, txt, px=26)


def _piedra_luna(lz, x, y, r, t, brillo=0.0):
    with lz.grupo(x, y, 1.0):
        if brillo > 0.01:
            lz.halo(0, 0, r * 2.4, (255, 226, 160), alfa=0.6 * brillo)
        lz.relleno(circulo(0, 0, r, 50), (150, 140, 150))
        lz.relleno(circulo(-r * 0.05, -r * 0.05, r * 0.94, 50), (186, 176, 184))
        lz.relleno(circulo(0, 0, r * 0.7, 40), (166, 156, 166))
        for k in range(6):
            a = k / 6 * 6.283 + 0.4
            lz.relleno(elipse(math.cos(a) * r * 0.5, math.sin(a) * r * 0.5, r * 0.16, r * 0.34, a + 1.57, 14), (130, 120, 132))
        lz.relleno(circulo(0, 0, r * 0.2, 20), (120, 110, 124))
        lz.trazo(np.array(circulo(0, 0, r * 0.86, 60)), (120, 110, 124), 3.0, cerrado=True, temblor=0.0, capa=2)


@shot(T0(E15), bg=lambda t: bg_grad((120, 190, 250), (255, 236, 200), ym=0.4), ent=("tinta", 0.7))
def s_corte(lz, t):
    T_CAVA0, T_CAVA1 = w_(E15, 1, 8), w_(E15, 1, 13)
    T_ROCA = w_(E15, 1, 15)
    T_DESC = w_(E15, 2, 2)
    cy = K(t, [(T0(E15), 560.0), (INI(E15, 1) + 0.6, 560.0), (T_CAVA1, 720.0), (T_ROCA + 0.5, 820.0), (T_DESC, 900.0), (T1(E15), 900.0)], e_inout)
    zoom = K(t, [(T0(E15), 1.12), (T_ROCA, 1.3), (T_DESC + 0.5, 1.05)], e_inout)
    cx = K(t, [(T0(E15), 900.0), (T_ROCA, 760.0), (T_DESC, 1050.0)], e_inout)
    with cam(lz, cx, cy, zoom):
        _superficie(lz, t)
        # capas del terreno
        _capas_terreno(lz, 1.0)
        _detalles_subsuelo(lz, t)
        for (yy, txt) in ((SY + 60, "asfalto y cimientos"), (SY + 230, "relleno colonial"), (SY + 520, "lodo del antiguo lago")):
            pass
        # el Templo Mayor enterrado
        F.templo_mayor(lz, 1350, SY + 720, 1.7)
        cubre = 1.0 - smooth(prog(t, T_DESC + 0.4, T_DESC + 3.2))
        if cubre > 0.01:
            with lz.recorte(np.array([[880, SY + 20], [1820, SY + 20], [1820, SY + 760], [880, SY + 760]])):
                _capas_terreno(lz, cubre)
        if cubre > 0.01 and t > T_ROCA + 1.2:
            u_ = smooth(prog(t, T_ROCA + 1.2, T_ROCA + 2.6)) * cubre
            base = np.array([[1080, SY + 720], [1620, SY + 720], [1560, SY + 500], [1500, SY + 500], [1440, SY + 500], [1380, SY + 500], [1320, SY + 500], [1260, SY + 500], [1200, SY + 500], [1140, SY + 500], [1080, SY + 720]])
            P.discontinua(lz, np.array([[1080, SY + 720], [1620, SY + 720], [1540, SY + 500], [1160, SY + 500], [1080, SY + 720]]), (255, 230, 150), ancho=5.0, largo=20, hueco=14, fase=-t * 20, frac=u_, capa=2)
            P.pastilla(lz, 1350, SY + 440, "el Templo Mayor, dos metros más abajo", px=30, alfa=u_) if False else P.pastilla(lz, 1350, SY + 440, "el Templo Mayor sigue enterrado", px=30, alfa=u_)
        # zanja
        prof = K(t, [(T_CAVA0, 0.0), (T_CAVA1, 300.0)], e_inout)
        if prof > 1:
            lz.relleno(rect_red(640, SY, 170, prof, 0), (34, 26, 44))
        # monolito
        mk = smooth(prog(t, T_ROCA, T_ROCA + 0.6))
        if mk > 0.01:
            _piedra_luna(lz, 725, SY + 300 - 60, 78 * mk, t, brillo=mk)
        # obreros
        F.obrero(lz, 570, SY, 1.5, t, lado=1, pico=1.0 if T_CAVA0 - 0.3 < t < T_CAVA1 else 0.0, seed=1)
        vuelta = smooth(prog(t, T_ROCA, T_ROCA + 0.5))
        F.obrero(lz, 900 + 30 * vuelta, SY, 1.5, t, lado=-1, pico=1.0 if T_CAVA0 - 0.3 < t < T_ROCA else 0.0, seed=2)
        if t > T_ROCA + 0.1:
            for xx in (570, 900):
                pass
    # rótulos
    etq(lz, t, T0(E15) + 0.3, INI(E15, 1) - 0.3, "Centro Histórico, hoy", W / 2, 240, px=40)
    cifra(lz, t, w_(E15, 1, 1), "1978", W / 2, 130, px=110, col=(34, 28, 80), t1=T_ROCA - 0.2) if False else None
    a = vent(t, w_(E15, 1, 1), T_ROCA + 0.2, 0.3, 0.3)
    if a > 0.01:
        with lz.capa(2):
            lz.relleno(rect_red(760, 80, 400, 140, 26), (255, 255, 255), alfa=0.92 * a)
            P.rotulo(lz, 960, 150, "1978", px=110, color=(34, 28, 80), sombra=0.0, alfa=a)
    b = vent(t, T_ROCA + 0.2, T_DESC - 0.2, 0.3, 0.3)
    if b > 0.01:
        P.pastilla(lz, W / 2, 250, "Coyolxauhqui: una enorme piedra tallada", px=38, alfa=b)
    c_ = vent(t, T_DESC + 1.0, T1(E15) - 0.1, 0.4, 0.3)
    if c_ > 0.01:
        P.pastilla(lz, W / 2, 190, "Templo Mayor · enterrado durante siglos", px=44, alfa=c_)


snd(T0(E15) + 0.3, "viento", 0.25, dur=2.0)
for _k in range(9):
    snd(w_(E15, 1, 8) + 0.55 * _k, "golpe_suave", 0.3)
snd(w_(E15, 1, 15), "impacto", 0.6)
snd(w_(E15, 1, 15) + 0.2, "revelar", 0.5)
snd(w_(E15, 2, 2) + 0.4, "zoom_whoosh", 0.4, dur=2.0)
snd(w_(E15, 2, 3), "brillo", 0.4)

# ======================================================================== 16. BARRA DE ORO
E16 = "barra"


def _mapa_centro(lz, t, ruta=0.0, ping=None, excav=None):
    """Plano esquemático del Centro Histórico (vista cenital): manzanas, Zócalo, Templo Mayor, Alameda y la ruta de la huida (esquemática)."""
    rng = np.random.RandomState(11)
    for r in range(6):
        for c in range(11):
            x0 = -60 + c * 200 + 8 * rng.rand()
            y0 = 60 + r * 190 + 8 * rng.rand()
            if (4 <= c <= 6 and 1 <= r <= 3) or (1 <= c <= 2 and r == 2):
                continue
            lz.relleno(rect_red(x0, y0, 178 + 10 * rng.rand(), 162 + 8 * rng.rand(), 12), (224, 212, 190) if (r + c) % 2 else (216, 202, 178))
    lz.relleno(rect_red(1000, 250, 420, 300, 8), (250, 240, 214))
    lz.relleno(rect_red(1000, 250, 420, 80, 4), (204, 180, 146))
    lz.relleno(rect_red(1440, 256, 120, 200, 6), (236, 214, 178))
    for i in range(4):
        h = 30 - i * 6
        lz.relleno(rect_red(1500 - h, 356 - h, 2 * h, 2 * h, 0), (250, 236, 210) if i % 2 == 0 else (206, 176, 150))
    lz.relleno(rect_red(1495, 351, 10, 10, 0), (222, 70, 78))
    lz.relleno(rect_red(260, 370, 400, 200, 12), (170, 206, 140))
    for i in range(40):
        lz.relleno(circulo(280 + 380 * h01(3, i), 385 + 170 * h01(4, i), 9 + 5 * h01(5, i), 8), (110, 170, 100))
    P.pastilla(lz, 1210, 300, "Zócalo", px=30)
    P.pastilla(lz, 460, 335, "Alameda Central", px=30)
    P.pastilla(lz, 1500, 480, "Templo Mayor", px=26)
    if ruta > 0.001:
        pts = catmull(np.array([[1000, 470], [820, 610], [600, 632], [380, 620], [140, 660], [-60, 690]]), 12)
        P.discontinua(lz, pts, (226, 70, 70), ancho=9.0, largo=30, hueco=20, fase=-t * 40, frac=ruta)
        P.pastilla(lz, 640, 700, "ruta de la huida (esquema)", px=28, alfa=smooth(ruta * 2))
    if ping is not None:
        u, x, y = ping
        for k in range(3):
            v = (t * 0.7 + k / 3) % 1.0
            lz.trazo(circulo(x, y, 20 + 110 * v, 40), (255, 190, 60), 5.0, cerrado=True, temblor=0.0, capa=2)
        lz.halo(x, y, 60, ORO, alfa=0.7 * u)
        lz.relleno(circulo(x, y, 10, 14), (255, 250, 210), alfa=u)


def _excavadora(lz, x, y, s, t, activa=1.0):
    with lz.grupo(x, y, s):
        lz.relleno(rect_red(-90, -34, 180, 34, 10), (60, 60, 76))
        for k in range(5):
            lz.relleno(circulo(-70 + k * 35, -17, 15, 12), (110, 110, 130))
        lz.relleno(rect_red(-70, -100, 130, 66, 8), (250, 190, 50))
        lz.relleno(rect_red(-30, -150, 74, 56, 8), (250, 200, 70))
        lz.relleno(rect_red(-20, -140, 54, 34, 4), (150, 200, 240))
        a = math.sin(t * 2.2) * 0.5 * activa
        x1, y1 = 66 + 100 * math.cos(-0.9 + a), -90 + 100 * math.sin(-0.9 + a)
        lz.trazo(np.array([[60, -84], [x1, y1]]), (250, 190, 50), 16.0, temblor=0.0, capa=1)
        x2, y2 = x1 + 84 * math.cos(0.7 + a * 1.4), y1 + 84 * math.sin(0.7 + a * 1.4)
        lz.trazo(np.array([[x1, y1], [x2, y2]]), (250, 190, 50), 13.0, temblor=0.0, capa=1)
        lz.relleno(np.array([[x2 - 18, y2 - 8], [x2 + 22, y2 - 8], [x2 + 30, y2 + 24], [x2 - 24, y2 + 24]]), (90, 90, 110))


@shot(T0(E16), bg=lambda t: bg_plano((236, 226, 204)), ent=("tinta", 0.7))
def bar_mapa(lz, t):
    ap = (smooth(prog(t, w_(E16, 0, 10), w_(E16, 0, 11))), 460.0, 470.0)
    _mapa_centro(lz, t, ruta=0.0, ping=ap if t > w_(E16, 0, 10) else None)
    ex = smooth(prog(t, w_(E16, 0, 6), w_(E16, 0, 7)))
    if ex > 0.01:
        _excavadora(lz, 520 - 240 * (1 - ex), 660, 1.0 * ex, t)
    cifra(lz, t, w_(E16, 0, 1), "1981", 300, 140, px=130, col=(34, 28, 80), t1=w_(E16, 0, 15))
    etq(lz, t, w_(E16, 0, 6), w_(E16, 0, 10), "obreros excavando", 700, 250, px=34)


snd(T0(E16) + 0.3, "pasos", 0.2, dur=1.0)
snd(w_(E16, 0, 6), "brr", 0.35)
snd(w_(E16, 0, 10), "pop", 0.4)


@shot(w_(E16, 0, 15) - 0.1, bg=lambda t: bg_grad((120, 190, 250), (255, 236, 200), ym=0.4), ent=("zoom", 0.5))
def bar_hallazgo(lz, t):
    tb = w_(E16, 0, 17)
    with lz.grupo(0, 0, 1.0):
        lz.relleno(rect_red(-20, 620, W + 40, 60, 0), (120, 118, 134))
        degradado_v(lz, -20, W + 20, 680, 1100, (176, 132, 96), (100, 84, 100), 680, 1000, paso=16.0)
        lz.relleno(rect_red(760, 680, 400, 230, 0), (36, 26, 44))
        for k, x in enumerate((-30, 1900)):
            pass
    F.obrero(lz, 520, 620, 2.4, t, lado=1, pico=1.0 if t < tb + 0.4 else 0.0, seed=3)
    F.obrero(lz, 1390, 620, 2.4, t, lado=-1, pico=1.0 if t < tb + 0.4 else 0.0, seed=4)
    u = smooth(prog(t, tb + 0.4, tb + 2.0))
    yb = lerp(870, 470, u)
    lz.halo(960, yb, 160 + 80 * u, ORO, alfa=0.7)
    if u > 0.02:
        for i in range(10):
            a = i / 10 * 6.283 + t * 0.5
            lz.trazo(np.array([[960 + math.cos(a) * 110, yb + math.sin(a) * 70], [960 + math.cos(a) * 180, yb + math.sin(a) * 120]]), (255, 236, 150), 6.0, temblor=0.0, capa=1)
    F.barra_oro(lz, 960, yb, 2.6, 0.05 * math.sin(t), 0.9)
    etq(lz, t, tb, tb + 2.0, "Alameda Central, 1981", 960, 200, px=40)
    cifra(lz, t, w_(E16, 0, 21), "1,93 kg", 960, 330, px=120, col=ORO, t1=w_(E16, 1, 0))


snd(w_(E16, 0, 15), "whoosh", 0.3, dur=0.6)
for _k in range(5):
    snd(w_(E16, 0, 15) + 0.4 * _k, "golpe_suave", 0.3)
snd(w_(E16, 0, 17) + 0.5, "revelar", 0.5)
snd(w_(E16, 0, 17) + 1.4, "bling", 0.5)
snd(w_(E16, 0, 21), "ding", 0.4)


@shot(INI(E16, 1) - 0.1, bg=lambda t: bg_grad((200, 224, 240), (240, 244, 250), ym=0.6), ent=("tinta", 0.7))
def bar_lab(lz, t):
    gy = 840.0
    lz.relleno(rect_red(-20, gy, W + 40, 300, 0), (206, 214, 226))
    lz.relleno(rect_red(-20, gy, W + 40, 10, 0), (170, 180, 200))
    lz.relleno(rect_red(560, 640, 800, 30, 8), (150, 110, 84))
    lz.relleno(rect_red(600, 670, 30, 170, 2), (120, 88, 66))
    lz.relleno(rect_red(1290, 670, 30, 170, 2), (120, 88, 66))
    F.barra_oro(lz, 960, 618, 2.0, 0.0, 0.5)
    # cañón de rayos X que barre la barra
    u = (t * 0.45) % 1.0
    x = lerp(800, 1120, 0.5 - 0.5 * math.cos(u * 6.283))
    lz.relleno(rect_red(x - 40, 300, 80, 150, 10), (90, 100, 130))
    lz.relleno(rect_red(x - 12, 450, 24, 46, 4), (60, 70, 96))
    lz.relleno(np.array([[x - 8, 496], [x + 8, 496], [x + 70, 600], [x - 70, 600]]), (120, 240, 220), alfa=0.35 + 0.15 * math.sin(t * 20))
    lz.relleno(rect_red(x - 4, 120, 8, 190, 2), (90, 100, 130))
    # monitor con espectro (ilustrativo)
    lz.relleno(rect_red(1440, 300, 380, 280, 16), (36, 40, 60))
    lz.relleno(rect_red(1454, 314, 352, 252, 10), (14, 22, 40))
    pts = []
    for i in range(60):
        xx = 1470 + i * 5.6
        v = 24 + 20 * math.sin(i * 0.5 + t * 3) * 0.3 + 90 * math.exp(-((i - 22) / 2.2) ** 2) + 130 * math.exp(-((i - 38) / 2.6) ** 2) + 60 * math.exp(-((i - 49) / 2.0) ** 2)
        pts.append((xx, 546 - v))
    lz.trazo(np.array(pts), (110, 240, 200), 4.0, temblor=0.0, capa=2)
    P.pastilla(lz, 1630, 610, "espectro (ilustrativo)", px=26)
    # científica
    P.humano(lz, 420, gy, 2.2, t, ropa=(250, 250, 255), paso=0.0, brazo=0.3)
    # resultado
    tv = w_(E16, 1, 9)
    k = e_back(prog(t, tv, tv + 0.5))
    if k > 0.02:
        with lz.capa(2):
            lz.relleno(circulo(960, 300, 92 * k, 40), (60, 200, 130))
            lz.trazo(np.array([[915, 300], [950, 340], [1010, 262]]) * k + np.array([960, 300]) * (1 - k), (255, 255, 255), 18.0 * k, temblor=0.0)
    etq(lz, t, INI(E16, 1), w_(E16, 1, 8), "Instituto Nacional de Antropología e Historia", W / 2, 200, px=34)
    etq(lz, t, w_(E16, 1, 5), w_(E16, 1, 9) + 0.5, "análisis químico · fluorescencia de rayos X", 960, 760 + 40, px=32)
    gran(lz, t, w_(E16, 1, 11), T1(E16) if False else w_(E16, 2, 0) - 0.1, "ORO DE LA ÉPOCA DE MOCTEZUMA", W / 2, 150, px=64, col=(30, 110, 80))


snd(INI(E16, 1), "whoosh", 0.35, dur=0.6)
snd(INI(E16, 1) + 0.6, "escribir", 0.3, dur=3.5)
snd(w_(E16, 1, 9), "ding", 0.5)
snd(w_(E16, 1, 9) + 0.15, "brillo", 0.4)


@shot(INI(E16, 2) - 0.1, bg=lambda t: bg_plano((236, 226, 204)), ent=("fuga", 0.6))
def bar_ruta(lz, t):
    r = smooth(prog(t, INI(E16, 2), w_(E16, 2, 8)))
    _mapa_centro(lz, t, ruta=r, ping=(1.0, 460.0, 470.0))
    F.barra_oro(lz, 460, 400, 1.0, 0.0, 0.9)
    # fila de barras perdidas (contornos) con una sola real
    tu = w_(E16, 2, 12)
    for i in range(14):
        x = 210 + i * 110
        a = smooth(prog(t, tu - 0.5 + 0.05 * i, tu + 0.1 + 0.05 * i))
        if a <= 0.01:
            continue
        real = i == 6
        with lz.capa(2):
            if real:
                F.barra_oro(lz, x, 870, 0.95 * a, 0.0, 0.9)
            else:
                pts = np.array([[x - 46, 878], [x + 46, 878], [x + 32, 852], [x - 32, 852], [x - 46, 878]])
                P.discontinua(lz, pts, (170, 140, 90), ancho=4.0, largo=12, hueco=9, capa=2)
    etq(lz, t, tu, T1(E16) if False else w_(E16, 3, 0) - 0.2, "la única pieza identificada", 810, 780, px=34)
    gran(lz, t, w_(E16, 2, 3), w_(E16, 2, 8), "EN LA RUTA DE LA HUIDA", W / 2, 130, px=76, col=(180, 40, 50))


snd(INI(E16, 2), "whoosh", 0.35, dur=0.6)
snd(w_(E16, 2, 4), "pasos", 0.25, dur=2.5)
snd(w_(E16, 2, 12), "bling", 0.4)


@shot(INI(E16, 3) - 0.1, bg=lambda t: bg_grad((22, 26, 70), (8, 10, 34)), ent=("aberracion", 0.6))
def bar_sonar(lz, t):
    lz.relleno(rect_red(-20, 420, W + 40, 700, 0), (60, 48, 76))
    degradado_v(lz, -20, W + 20, 420, H + 20, (100, 80, 100), (36, 30, 56), 420, H, paso=16.0)
    lz.relleno(rect_red(-20, 380, W + 40, 44, 0), (120, 118, 134))
    for i in range(9):
        P.humano(lz, 140 + 220 * i, 380, 0.6, t, ropa=[(198, 80, 90), (90, 120, 200), (230, 190, 90)][i % 3], paso=0.4, voltear=(i % 2 == 0))
    # pulsos de sonar y destellos bajo tierra
    for k in range(3):
        v = ((t - INI(E16, 3)) * 0.35 + k / 3) % 1.0
        lz.trazo(circulo(960, 430, 60 + 900 * v, 70), (110, 240, 220), 4.0, cerrado=True, temblor=0.0, capa=2)
    for i in range(16):
        x = 140 + 1640 * h01(4, i)
        y = 560 + 420 * h01(5, i)
        a = smooth(prog(t, w_(E16, 3, 8) + 0.12 * i, w_(E16, 3, 8) + 0.6 + 0.12 * i))
        if a > 0.01:
            lz.halo(x, y, 60, ORO, alfa=0.7 * a * (0.6 + 0.4 * math.sin(t * 4 + i)))
            F.barra_oro(lz, x, y, 0.45 * a, 0.5 * (h01(6, i) - 0.5), 0.0)
    gran(lz, t, w_(E16, 3, 9), T1(E16) - 0.1, "¿CUÁNTAS MÁS?", W / 2, 240, px=104, col=(255, 226, 130))
    etq(lz, t, w_(E16, 3, 12), T1(E16) - 0.2, "seguir bajo tierra", W / 2, 320, px=38)


snd(INI(E16, 3), "zoom_whoosh", 0.35, dur=1.0)
for _k in range(8):
    snd(w_(E16, 3, 8) + 0.25 * _k, "bling", 0.25, tono=0.8 + 0.05 * _k)
snd(w_(E16, 3, 9), "latido", 0.5, dur=1.2)
