# -*- coding: utf-8 -*-
"""Escenas 9-12: antes_huida (reparto y carga del oro en el patio), noche (huida por la calzada, canoas, caída al agua y hundimiento),
bajas (gráfica de muertos, pérdidas y el árbol del amanecer) y regreso (Tlaxcala, viruela, trece bergantines y cerco)."""
import math

import numpy as np

from motor import W, H, prog, lerp, smooth, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, blob, catmull, bezier, h01
import plano as P
import mapa as MP
import mapa_local as ML
import figuras as F
from mundo import degradado_v, llama, humo
from reg import shot, snd
from util import *

PANT = np.array([[0, 0], [W, 0], [W, H], [0, H]], float)

# ======================================================================== 9. ANTES DE LA HUIDA
E9 = "antes_huida"
GY9 = 860.0
PILA = None


def _posiciones_monton():
    pos = []
    for r, n in enumerate((6, 5, 4, 3, 2, 1)):
        for k in range(n):
            pos.append(((k - (n - 1) / 2) * 84, -r * 34 - 14))
    return pos


PILA = _posiciones_monton()


def _monton(lz, x, y, n, t, brillo=0.3):
    for i in range(min(n, len(PILA))):
        dx, dy = PILA[i]
        F.barra_oro(lz, x + dx, y + dy, 0.9, 0.0, brillo if i == len(PILA) - 1 else 0.0)
    if n > 0:
        lz.halo(x, y - 60, 260, ORO, alfa=0.35 + 0.1 * math.sin(t * 3))


def _balanza(lz, x, y, s, incl, t):
    with lz.grupo(x, y, s):
        lz.relleno(np.array([[0, -60], [40, 120], [-40, 120]]), (210, 210, 230))
        lz.relleno(rect_red(-60, 118, 120, 14, 4), (150, 150, 180))
        a = incl * 0.32
        ex, ey = math.cos(a) * 190, math.sin(a) * 190
        lz.trazo(np.array([[-ex, -60 - ey], [ex, -60 + ey]]), (226, 228, 246), 12.0, temblor=0.0, capa=2)
        for sg, (px, py) in ((-1, (-ex, -60 - ey)), (1, (ex, -60 + ey))):
            lz.trazo(np.array([[px, py], [px - 34, py + 100]]), (226, 228, 246), 3.0, temblor=0.0, capa=2)
            lz.trazo(np.array([[px, py], [px + 34, py + 100]]), (226, 228, 246), 3.0, temblor=0.0, capa=2)
            lz.relleno(np.array([[px - 46, py + 100], [px + 46, py + 100], [px + 30, py + 116], [px - 30, py + 116]]), (226, 228, 246))
            if sg < 0:
                for k in range(3):
                    F.barra_oro(lz, px - 20 + 16 * k, py + 82 - 20 * (k % 2), 0.55, 0.0, 0.0)
            else:
                lz.relleno(circulo(px, py + 76, 14, 14), F.PIELES[0])
                lz.relleno(rect_red(px - 12, py + 88, 24, 12, 4), (206, 70, 62))


@shot(T0(E9), bg=lambda t: bg_grad((10, 12, 44), (40, 26, 76)), ent=("tinta", 0.7))
def a_patio(lz, t):
    ZP = 1.5
    cxx = K(t, [(T0(E9), 760.0), (w_(E9, 1, 3), 900.0), (w_(E9, 1, 8), 1420.0), (T1(E9), 1700.0)], e_inout)
    with cam(lz, cxx, 690, ZP):
        # patio: muro del fondo con arcos y suelo de piedra
        lz.relleno(rect_red(-400, 300, 3200, 560, 0), (58, 44, 92))
        for i in range(-2, 12):
            x = i * 250
            lz.relleno(np.array([[x - 80, 860], [x - 80, 560], [x - 50, 470], [x, 440], [x + 50, 470], [x + 80, 560], [x + 80, 860]]), (34, 24, 64))
        lz.relleno(rect_red(-400, 860, 3200, 300, 0), (86, 66, 110))
        lz.relleno(rect_red(-400, 852, 3200, 12, 0), (150, 124, 150))
        for x in (100, 1120, 2100):
            F.brasero(lz, x, GY9, 1.5, t)
        # montón grande del botín
        n_pila = 21
        taken = 0
        tiempos = []
        for i in range(6):
            x0 = 430 + i * 70
            xt = 1500 + i * 46
            ts = w_(E9, 1, 3) + 0.15 * i
            tl = ts + (xt - x0) / 380.0
            tiempos.append((ts, tl))
            if t >= tl + 0.3:
                taken += 3
        _monton(lz, 1640, GY9, n_pila - taken, t)
        # reservas: quinto del rey y quinto de Cortés (se cargan a caballo)
        t_rey, t_suyo, t_carga = w_(E9, 0, 5), w_(E9, 0, 9), w_(E9, 0, 13)
        for (tt, x, txt) in ((t_rey, 1060, "Quinto del rey"), (t_suyo, 1200, "Quinto de Cortés")):
            u = e_back(prog(t, tt, tt + 0.5))
            if u > 0.02:
                for k in range(3):
                    ti = t_carga + 0.35 * k + (0.0 if x == 1060 else 1.2)
                    if t < ti + 0.9:
                        yy = GY9 - 20 - 30 * k
                        F.barra_oro(lz, x, yy - 60 * (1 - u), 0.85 * u, 0.0, 0.0)
                lz.halo(x, GY9 - 60, 90, ORO, alfa=0.3 * u)
        # caballos que reciben la carga
        for j, hx in enumerate((170, 400)):
            recibido = smooth(prog(t, t_carga + 0.9 + 1.2 * j, t_carga + 1.4 + 1.2 * j))
            sale = smooth(prog(t, w_(E9, 1, 0), w_(E9, 1, 0) + 2.4)) * 900
            F.caballo(lz, hx - sale * 0.0 - 0, GY9 + 10, 1.35, t, paso=1.0 if sale > 5 else 0.0, lado=1, carga=1 if recibido > 0.5 else 0, col=(150, 98, 68) if j == 0 else (96, 70, 60), seed=j)
        # las barras vuelan del montón a los caballos
        for (x, jj) in ((1060, 0), (1200, 1)):
            for k in range(3):
                ti = t_carga + 0.35 * k + 1.2 * jj
                u = prog(t, ti, ti + 0.9)
                if 0 < u < 1:
                    px = lerp(x, 170 + 230 * jj, e_inout(u))
                    py = lerp(GY9 - 40, GY9 - 210, u) - 130 * math.sin(math.pi * u)
                    F.barra_oro(lz, px, py, 0.75, 0.3 * (1 - u), 0.5)
        # Cortés dirige
        F.soldado(lz, 930, GY9, 2.0, t, lado=1, arma="espada", seed=1, tunica=(150, 40, 60),
                  brazos=(-0.3, 1.6 + 0.3 * math.sin(t * 3)) if t < w_(E9, 1, 3) else (-0.3, 2.4))
        # soldados que corren al montón y vuelven cargados
        for i, (ts, tl) in enumerate(tiempos):
            x0 = 430 + i * 70
            xt = 1500 + i * 46
            if t < ts:
                xx, paso, lado, carga = x0, 0.0, 1, 0.0
            elif t < tl:
                xx, paso, lado, carga = lerp(x0, xt, (t - ts) / max(tl - ts, 1e-3)), 2.0, 1, 0.0
            elif t < tl + 0.6:
                xx, paso, lado, carga = xt, 0.0, 1, 1.4 * smooth(prog(t, tl + 0.2, tl + 0.6))
            else:
                v = 60 + 40 * h01(2, i)
                xx = xt + v * (t - tl - 0.6) * (1 if t < w_(E9, 2, 6) else 0.6)
                paso, lado, carga = 0.7, 1, 1.4
            F.soldado(lz, xx, GY9 + 6 * (i % 2), 1.6, t, paso=paso, lado=lado, carga=carga, seed=i + 20)
    # etiquetas
    etq(lz, t, t_rey, t_rey + 2.2, "Quinto del rey", 960, 220, px=40) if False else None
    for (tt, txt, sx) in ((t_rey, "Quinto del rey", 1060), (t_suyo, "Quinto de Cortés", 1200)):
        a = vent(t, tt, t_carga + 1.0)
        if a > 0.01:
            P.pastilla(lz, W / 2 + (sx - cxx) * ZP, H / 2 + (GY9 - 190 - 690) * ZP, txt, px=34, alfa=a)
    a = vent(t, w_(E9, 1, 6), w_(E9, 1, 10) + 1.2)
    if a > 0.01:
        P.pastilla(lz, W / 2 + (1640 - cxx) * ZP, H / 2 + (GY9 - 330 - 690) * ZP, "«el oro que quisieran»", px=38, alfa=a)
    # balanza: el peso contra la vida
    b = vent(t, w_(E9, 2, 5), T1(E9), 0.4, 0.3)
    if b > 0.01:
        with lz.capa(2):
            _balanza(lz, 960, 300, 0.9 * b, K(t, [(w_(E9, 2, 5), 0.0), (w_(E9, 2, 8), 1.0)]), t)
    gran(lz, t, w_(E9, 2, 8), T1(E9) - 0.1, "COSTARÍA LA VIDA", W / 2, 150, px=90, col=(255, 130, 110))


snd(T0(E9) + 0.2, "fuego", 0.3, dur=6.0)
for _i in range(3):
    snd(w_(E9, 0, 13) + 0.9 + 0.35 * _i, "clink", 0.35)
    snd(w_(E9, 0, 13) + 2.1 + 0.35 * _i, "clink", 0.35)
snd(w_(E9, 0, 5), "pop", 0.4)
snd(w_(E9, 0, 9), "pop", 0.4)
snd(w_(E9, 1, 3), "pasos", 0.4, dur=2.4)
for _i in range(6):
    snd(w_(E9, 1, 3) + 1.9 + 0.15 * _i, "bling", 0.25)
snd(w_(E9, 2, 8), "hmm", 0.4)

# ======================================================================== 10. NOCHE TRISTE
E10 = "noche"
GY10 = 760.0
T_LLUVIA0 = T0(E10)
GAP0, GAP1 = 1560.0, 1900.0
T_ATQ = w_(E10, 1, 3)
T_PARA = T_ATQ + 1.0
T_J0 = INI(E10, 2)                 # empiezan los saltos
T_HUND = INI(E10, 3)
_Q = [(i, 300 + 0) for i in range(9)]


def _xcol(t):
    """x de la cabeza de la columna (mundo)."""
    if t < T_PARA:
        return 300.0 + 150.0 * (t - T0(E10))
    return 300.0 + 150.0 * (T_PARA - T0(E10)) + 0.0


def _ciudad_noche(lz, camx, t):
    with lz.grupo(W / 2 - camx * 0.35, 0, 1.0):
        for i in range(-6, 12):
            x = 200 + i * 200 + 40 * h01(2, i)
            h = 90 + 60 * h01(3, i)
            w = 150 + 40 * h01(4, i)
            lz.relleno(rect_red(x - w / 2, 690 - h, w, h, 3), (52, 44, 96))
            for j in range(3):
                if h01(5, i, j) > 0.4:
                    lz.relleno(rect_red(x - w / 2 + 18 + j * 40, 690 - h + 24, 14, 20, 3), (255, 214, 120), alfa=0.9)
        F.templo_mayor(lz, 200, 694, 0.75)
        lz.halo(200, 500, 340, (255, 140, 60), alfa=0.35)
        for k in range(3):
            llama(lz, 60 + k * 300, 690, 0.9, t, seed=k)


def _calzada_noche(lz, camx, t, con_hueco=True):
    with lz.grupo(W / 2 - camx, 0, 1.0):
        agua(lz, camx - 1200, camx + 1200, GY10 + 40, 1900, t, (40, 76, 140), (10, 20, 60), amp=5, luna=None)
        # tramos de calzada (con el hueco del puente)
        x0 = camx - 1200
        lz.relleno(rect_red(x0, GY10, GAP0 - x0, 46, 0), (150, 126, 130))
        lz.relleno(rect_red(x0, GY10, GAP0 - x0, 8, 0), (196, 170, 170))
        lz.relleno(rect_red(GAP1, GY10, camx + 1200 - GAP1, 46, 0), (150, 126, 130))
        lz.relleno(rect_red(GAP1, GY10, camx + 1200 - GAP1, 8, 0), (196, 170, 170))
        t_rompe = w_(E10, 1, 1)
        if t < t_rompe + 0.1:
            lz.relleno(rect_red(GAP0, GY10, GAP1 - GAP0, 46, 0), (110, 80, 60))
            for k in range(8):
                lz.relleno(rect_red(GAP0 + 10 + k * 42, GY10 - 4, 34, 50, 2), (150, 106, 72))
        else:
            u = t - t_rompe
            for k in range(8):
                v = u - 0.06 * k
                if v > 0 and v < 1.6:
                    with lz.grupo(GAP0 + 27 + k * 42, GY10 + 20 + 620 * v * v, 1.0, 0.8 * v * (1 if k % 2 else -1)):
                        lz.relleno(rect_red(-17, -25, 34, 50, 2), (150, 106, 72), alfa=1 - v / 1.6)
        for k in range(-40, 41):
            xx = (camx // 130) * 130 + k * 130
            if xx < GAP0 - 20 or xx > GAP1 + 20:
                lz.relleno(rect_red(xx, GY10 + 46, 12, 70, 0), (86, 66, 96))


def _canoa_atq(lz, t, k, camx):
    """Canoa que sube desde abajo y arroja lanzas a la columna."""
    ts = T_ATQ - 0.4 + 0.25 * k
    u = e_out(prog(t, ts, ts + 1.6))
    if u <= 0.01:
        return
    xs = (900, 1250, 1520, 1700, 1050)[k]
    ys = lerp(GY10 + 520, GY10 + 150 + 30 * (k % 2), u)
    F.canoa(lz, xs + 30 * math.sin(t * 0.8 + k), ys, 1.2, t, lado=1 if k % 2 else -1, guerreros=2, seed=k, plumas=k)
    for j in range(3):
        tt = ts + 1.6 + 0.9 * j + 0.3 * k
        uu = prog(t, tt, tt + 0.7)
        if 0 < uu < 1:
            tx = 1200 + 40 * k
            px = lerp(xs, tx, uu)
            py = lerp(ys - 60, GY10 - 110, uu) - 260 * math.sin(math.pi * uu)
            ang = math.atan2(-(GY10 - 110 - ys + 60) * 0 - 1, 1)
            lz.trazo(np.array([[px, py], [px + 34 * (1 if tx > xs else -1), py - 12]]), (226, 220, 210), 4.0, temblor=0.0, capa=2)


@shot(T0(E10), bg=lambda t: bg_grad((6, 8, 30), (24, 22, 70)), post=[lambda i, t: post_lluvia(i, t, 1.0, 0.32, 44, 0.42), lambda i, t: post_viñeta(i, 0.4)], ent=("negro", 0.5))
def n_calzada(lz, t):
    camx = K(t, [(T0(E10), 620.0), (T_ATQ, 1080.0), (T_J0 - 0.4, 1200.0), (T_J0 + 1.0, 1620.0), (T_HUND - 0.3, 1660.0)], e_inout)
    zoom = K(t, [(T0(E10), 1.3), (T_J0 - 0.4, 1.3), (T_J0 + 1.2, 1.65), (T_HUND - 0.3, 1.7)], e_inout)
    lz.relleno(PANT, (8, 10, 40), alfa=0.0)
    _ciudad_noche(lz, camx, t)
    with cam(lz, W / 2 + (camx - W / 2), 540, 1.0) if False else lz.grupo(0, 0, 1.0):
        pass
    with lz.grupo(W / 2, 560, zoom):
        with lz.grupo(-W / 2, -690, 1.0):
            _calzada_noche(lz, camx, t)
            with lz.grupo(W / 2 - camx, 0, 1.0):
                xh = _xcol(t)
                estatica = t >= T_PARA
                for i in range(9):
                    x = xh - 96 * i
                    if i in (3, 6):
                        F.caballo(lz, x - 20, GY10, 1.5, t, paso=0.0 if estatica else 1.0, lado=1, carga=1, col=(96, 70, 60) if i == 3 else (150, 98, 68), seed=i)
                        continue
                    lado = 1
                    br = None
                    if t >= T_PARA and t < T_J0 + 0.5:
                        lado = 1 if (t * 0 + i) % 2 else -1
                        br = (-0.3, 1.9 + 1.4 * math.sin(t * 9 + i)) if t > T_ATQ + 1.5 else None
                    if t >= T_J0 + 0.3 and i >= 5:
                        continue                                    # los que saltan se dibujan aparte
                    F.soldado(lz, x, GY10 + 4 * (i % 2), 1.55, t, paso=0.0 if estatica else 1.4, lado=lado, carga=1.4 if i % 3 else 0.7,
                              arma="lanza" if i % 2 else "espada", seed=i + 3, brazos=br)
                F.canon(lz, xh - 96 * 9.4, GY10, 1.3)
                # canoas que atacan
                for k in range(5):
                    _canoa_atq(lz, t, k, camx)
                # los que saltan el hueco con demasiado oro
                for j, i in enumerate(range(5, 9)):
                    tj = T_J0 + 0.3 + 0.75 * j
                    x0 = xh - 96 * i
                    if t < tj:
                        continue
                    u = prog(t, tj, tj + 1.1)
                    if u < 1.0:
                        x = lerp(GAP0 - 60, GAP0 + 170 + 20 * j, u)
                        y = GY10 - 150 * math.sin(math.pi * min(u * 1.1, 1.0)) + (u ** 3) * (110 + 20 * j)
                        F.soldado(lz, x, y, 1.55, t, paso=0.0, lado=1, carga=1.5, seed=i + 3, brazos=(-2.8, 2.8), inc=-0.3 * u)
                    else:
                        agua_y = GY10 + 60
                        xw = GAP0 + 170 + 20 * j
                        v = t - tj - 1.1
                        chapoteo(lz, xw, agua_y, t, tj + 1.1, 1.1)
                        if v < 1.6:
                            F.soldado(lz, xw + 10 * math.sin(v * 4), agua_y + 20 + v * 6, 1.55 * (1 - 0.15 * v), t, paso=0.0, lado=1, carga=1.5, seed=i + 3,
                                      brazos=(-2.9 + 0.4 * math.sin(v * 8), 2.9 - 0.4 * math.sin(v * 8)))
    # títulos
    gran(lz, t, T0(E10) + 0.4, T0(E10) + 2.6, "30 de junio de 1520", W / 2, 130, px=84)
    etq(lz, t, w_(E10, 0, 14), w_(E10, 0, 16) + 1.6, "Calzada de Tacuba", W / 2, 250, px=40)
    gran(lz, t, w_(E10, 0, 11), w_(E10, 0, 12) + 1.2, "EN SILENCIO", W / 2, 400, px=96, col=(190, 210, 255))
    gran(lz, t, w_(E10, 1, 2), w_(E10, 1, 3) + 1.2, "¡LOS DESCUBRIERON!", W / 2, 180, px=90, col=(255, 110, 110))
    gran(lz, t, w_(E10, 2, 5), w_(E10, 2, 10) + 0.4, "NO PODÍAN PELEAR NI NADAR", W / 2, 180, px=72, col=(255, 200, 100))


snd(T0(E10), "lluvia", 0.5, dur=3.0)
for _k in range(6):
    snd(T0(E10) + 3.0 * _k, "lluvia", 0.45, dur=3.0)
snd(T0(E10) + 0.4, "pasos", 0.3, dur=6.0)
snd(w_(E10, 1, 1), "impacto", 0.6)
snd(w_(E10, 1, 1) + 0.1, "golpe_suave", 0.5)
snd(T_ATQ, "whoosh", 0.4, dur=0.7)
for _k in range(6):
    snd(T_ATQ + 1.4 + 0.7 * _k, "golpe_suave", 0.3)
for _j in range(4):
    snd(T_J0 + 0.3 + 0.75 * _j + 1.1, "chapuzon", 0.5)


def _submarino(lz, camx, t, ys):
    """Corte bajo la superficie: agua profunda, rayos, burbujas y el fondo de lodo."""
    with lz.grupo(W / 2 - camx, 0, 1.0):
        degradado_v(lz, camx - 1400, camx + 1400, ys, ys + 1300, (28, 96, 150), (4, 14, 40), ys, ys + 1000, paso=16.0)
        for i in range(9):
            x = camx - 1200 + i * 300 + 40 * math.sin(t * 0.5 + i)
            lz.relleno(np.array([[x, ys], [x + 90, ys], [x + 260, ys + 900], [x + 100, ys + 900]]), (120, 190, 220), alfa=0.05 + 0.03 * math.sin(t + i))
        lz.relleno(blob(camx, ys + 1010, 1400, 4, 0.05, 40, 3) * np.array([1, 0.13]) + np.array([0, ys + 1010]) * 0 + np.array([0, 0]), (58, 46, 66), alfa=0.0)
        lz.relleno(np.array([[camx - 1500, ys + 1000], [camx + 1500, ys + 1000], [camx + 1500, ys + 1300], [camx - 1500, ys + 1300]]), (52, 42, 66))
        lz.relleno(rect_red(camx - 1500, ys + 992, 3000, 12, 0), (86, 70, 90))
        for i in range(20):
            ph = (t * (0.15 + 0.05 * (i % 4)) + i * 0.137) % 1.0
            x = camx - 1000 + 100 * i + 20 * math.sin(t + i)
            lz.relleno(circulo(x, ys + 1000 - ph * 1000, 4 + 3 * (i % 3), 8), (200, 240, 255), alfa=0.35 * (1 - ph))


@shot(T_HUND, bg=lambda t: bg_grad((28, 96, 150), (4, 14, 40)), ent=("zoom", 0.7))
def n_hundir(lz, t):
    ys = GY10 + 50
    camx = 1750.0
    cy = K(t, [(T_HUND, 640.0), (T_HUND + 1.8, 1100.0)], e_inout)
    with lz.grupo(0, 540 - cy, 1.0):
        # superficie con lluvia y canoas
        lz.relleno(rect_red(-200, ys - 700, W + 400, 700, 0), (14, 16, 56))
        with lz.grupo(W / 2 - camx, 0, 1.0):
            lz.relleno(rect_red(camx - 1200, ys - 8, 2400, 12, 0), (170, 226, 250), alfa=0.9)
            for k in range(3):
                F.canoa(lz, 1500 + 260 * k, ys - 6, 1.1, t, lado=1 if k % 2 else -1, guerreros=2, seed=k + 10, plumas=k)
        _submarino(lz, camx, t, ys)
        with lz.grupo(W / 2 - camx, 0, 1.0):
            for i in range(6):
                x = 1520 + 60 * i + 20 * math.sin(t * 2 + i)
                v = (t - T_HUND) * 150 + 40 * i - 100
                y = ys + 20 + max(0.0, v) * (1.0 + 0.3 * h01(9, i)) * 0.9
                y = min(y, ys + 940)
                if i % 2 == 0:
                    F.soldado(lz, x, y, 1.4, t, paso=0.0, lado=1, carga=1.5, seed=i + 40, brazos=(-2.6, 2.6), inc=0.3 * math.sin(t + i))
                    F.barra_oro(lz, x - 10, y - 20, 0.6, 0.2, 0.0)
            for i in range(14):
                x = 1480 + 46 * i
                v = (t - T_HUND - 0.3) * 200 * (0.8 + 0.4 * h01(11, i)) - 30 * i
                y = min(ys + 40 + max(0.0, v), ys + 970 - 0.0)
                F.barra_oro(lz, x + 10 * math.sin(t * 1.2 + i), y, 0.7, 0.4 * math.sin(t + i), 0.5 if y < ys + 960 else 0.0)
            if t > T_HUND + 2.0:
                lz.halo(1800, ys + 960, 380, ORO, alfa=0.35 * smooth(prog(t, T_HUND + 2.0, T_HUND + 3.0)))
    gran(lz, t, w_(E10, 3, 4), T1(E10) - 0.1, "SE HUNDIERON CON SU BOTÍN", W / 2, 150, px=76, col=(255, 210, 110))
    etq(lz, t, w_(E10, 3, 0), w_(E10, 3, 4), "Lago de Texcoco", W / 2, 250, px=38)


snd(T_HUND, "chapuzon", 0.6)
snd(T_HUND + 0.3, "burbujas", 0.5, dur=1.0)
snd(T_HUND + 1.6, "clink", 0.4, tono=0.8)
snd(T_HUND + 2.0, "brillo", 0.4)

# ======================================================================== 11. BAJAS
E11 = "bajas"


def _barra_datos(lz, x0, y, largo, col, alto=70, borde=(255, 255, 255)):
    if largo > 4:
        lz.relleno(rect_red(x0, y - alto / 2, largo, alto, 14), P.oscurecer(col, 0.25))
        lz.relleno(rect_red(x0, y - alto / 2, largo, alto - 8, 14), col)


@shot(T0(E11), bg=lambda t: bg_grad((22, 26, 78), (10, 12, 44)), ent=("tinta", 0.7))
def b_grafica(lz, t):
    k = 0.28
    x0 = 470
    P.rotulo(lz, W / 2, 110, "Muertos en la Noche Triste", px=64, alfa=smooth(prog(t, T0(E11), T0(E11) + 0.6)))
    filas = (
        (300, (226, 80, 80), "Españoles", "según Cortés", 154, w_(E11, 0, 2), w_(E11, 0, 5) + 0.3, "154"),
        (500, (255, 170, 60), "Españoles", "según otros cronistas", 450, w_(E11, 0, 12), w_(E11, 0, 13) + 0.4, "450 o más"),
    )
    for (y, col, tit, sub, val, ta, tb, txt) in filas:
        u = e_out(prog(t, ta, tb + 0.6))
        largo = val * k * u
        _barra_datos(lz, x0, y, largo, col)
        P.rotulo(lz, 250, y - 14, tit, px=40, color=BLANCO)
        P.pastilla(lz, 250, y + 30, sub, px=28, alfa=smooth(prog(t, ta - 0.3, ta)))
        if u > 0.05:
            cifra(lz, t, ta, txt, x0 + largo + 190, y, px=64, col=(255, 255, 255))
    # aliados: rango de 1 000 a 4 000
    ta, tb = w_(E11, 0, 19), w_(E11, 0, 22)
    u = e_out(prog(t, ta, tb + 0.4))
    y = 700
    P.rotulo(lz, 250, y - 14, "Aliados", px=40, color=BLANCO)
    P.pastilla(lz, 250, y + 30, "tlaxcaltecas", px=28, alfa=smooth(prog(t, ta - 0.3, ta)))
    _barra_datos(lz, x0, y, 1000 * k * min(u * 1.2, 1.0), (70, 200, 200))
    if u > 0.4:
        ext = (u - 0.4) / 0.6
        lz.relleno(rect_red(x0 + 1000 * k, y - 35, 3000 * k * ext, 62, 14), (70, 200, 200), alfa=0.35)
        P.discontinua(lz, np.array([[x0 + 1000 * k, y - 52], [x0 + 1000 * k + 3000 * k * ext, y - 52]]), (170, 240, 240), ancho=4.0, largo=14, hueco=10, capa=2)
    if u > 0.05:
        cifra(lz, t, ta, "1 000 a 4 000", x0 + (1000 * k + 3000 * k * max(0, (u - 0.4) / 0.6)) / 2, y - 78, px=58, col=BLANCO)
    # multitud de fondo (los aliados) y unos cuantos soldados caídos
    for i in range(9):
        F.guerrero(lz, 250 + 195 * i, 950, 0.8, t, paso=0.0, lado=1 if i % 2 else -1, arma="lanza", escudo=False, plumas=i, seed=i + 70) if False else None


snd(T0(E11) + 0.2, "whoosh", 0.35, dur=0.6)
snd(w_(E11, 0, 2), "ding", 0.3)
snd(w_(E11, 0, 12), "ding", 0.3, tono=0.9)
snd(w_(E11, 0, 19), "ding", 0.3, tono=0.8)


@shot(INI(E11, 1) - 0.1, bg=lambda t: bg_grad((14, 16, 60), (6, 10, 40)), ent=("glitch", 0.5))
def b_perdidas(lz, t):
    ys = 760.0
    agua(lz, -50, W + 50, ys, H + 50, t, (40, 96, 170), (10, 26, 84), amp=6)
    items = ((4, 480, "Cañones", "canon"), (7, 960, "Caballos", "caballo"), (12, 1440, "Oro", "oro"))
    for (i, x, txt, kind) in items:
        tt = w_(E11, 1, i)
        u = prog(t, tt, tt + 1.2)
        if u <= 0:
            continue
        y = lerp(100, ys - 10, e_in(u)) if u < 1 else ys - 10 + 30 * smooth(prog(t, tt + 1.2, tt + 2.2))
        a = 1 - smooth(prog(t, tt + 1.2, tt + 2.4))
        with lz.grupo(x, y, 1.0):
            if kind == "canon":
                F.canon(lz, 0, 0, 1.9)
            elif kind == "caballo":
                F.caballo(lz, 0, 0, 1.5, t, paso=0.0, lado=1, carga=1)
            else:
                for j in range(4):
                    F.barra_oro(lz, (j % 2) * 60 - 30, -20 - 34 * (j // 2), 1.2, 0.0, 0.4)
        chapoteo(lz, x, ys, t, tt + 1.1, 1.6)
        P.pastilla(lz, x, 220, txt, px=44, alfa=smooth(prog(t, tt, tt + 0.3)))
        if u >= 1:
            with lz.capa(2):
                lz.trazo(np.array([[x - 90, 300], [x + 90, 420]]), (240, 70, 70), 14.0, temblor=0.0, alfa=1.0) if False else None
    gran(lz, t, w_(E11, 1, 0), INI(E11, 2) - 0.2, "SE PERDIERON", W / 2, 130, px=88, col=(255, 130, 110))


snd(INI(E11, 1), "whoosh", 0.4, dur=0.7)
for _i in (4, 7, 12):
    snd(w_(E11, 1, _i) + 1.1, "chapuzon", 0.5)


@shot(INI(E11, 2) - 0.1, bg=lambda t: bg_grad((255, 200, 140), (255, 236, 196), ym=0.7), ent=("fuga", 0.7))
def b_arbol(lz, t):
    sol = K(t, [(INI(E11, 2) - 0.1, 0.0), (T1(E11), 1.0)])
    # sol naciente
    lz.halo(W / 2 + 200, 700 - 220 * sol, 520, (255, 236, 170), alfa=0.6)
    lz.relleno(circulo(W / 2 + 200, 700 - 220 * sol, 110, 40), (255, 244, 206))
    # colinas
    lz.relleno(np.array([[0, 760], [300, 690], [700, 730], [1200, 680], [1700, 740], [1920, 700], [1920, 1080], [0, 1080]]), (150, 170, 120))
    lz.relleno(np.array([[0, 830], [400, 780], [900, 820], [1500, 770], [1920, 820], [1920, 1080], [0, 1080]]), (120, 150, 96))
    lz.relleno(rect_red(-20, 880, W + 40, 220, 0), (96, 124, 84))
    P.arbol(lz, 1380, 900, 3.4, t, hojas=(70, 150, 90))
    # Cortés sentado bajo el árbol y algunos supervivientes
    F.soldado_triste(lz, 1150, 900, 2.6, t, lado=-1, seed=1)
    for i, (x, l) in enumerate(((560, 1), (760, 1), (300, 1))):
        F.soldado_triste(lz, x, 900 + 6 * i, 1.7, t + i, lado=l, seed=i + 5, tunica=(120, 60, 60))
    for i in range(2):
        F.soldado(lz, 100 + 900 * i, 900, 1.6, t, paso=0.5, lado=1, brazos=(-0.2, 0.2), seed=i + 30)
    etq(lz, t, INI(E11, 2), INI(E11, 2) + 3.0, "Según la tradición", 960, 220, px=42)
    gran(lz, t, w_(E11, 2, 6), T1(E11) - 0.1, "LLORÓ LA PÉRDIDA DE SUS HOMBRES", W / 2, 130, px=64, col=(120, 60, 100))


snd(INI(E11, 2), "amanecer", 0.4, dur=3.0)
snd(w_(E11, 2, 6), "suspiro", 0.4, dur=1.2)

# ======================================================================== 12. REGRESO (Tlaxcala, viruela, bergantines, cerco)
E12 = "regreso"


@shot(T0(E12), bg=lambda t: bg_grad((10, 20, 60), (24, 60, 120)), ent=("tinta", 0.7))
def r_tlaxcala(lz, t):
    c = Klog(t, [(T0(E12), (-98.65, 19.3, 3.0)), (T1(E12) if False else 203.2, (-98.55, 19.3, 3.4))])
    MP.mapa(lz, t, c, dict(ciudad_alfa=0.0, cdmx=0.0))
    ruta = np.array([MP.XY(-99.13, 19.43), MP.XY(-98.8, 19.30), MP.XY(-98.55, 19.36), MP.XY(-98.2, 19.32)])
    pts = catmull(ruta, 14)
    u = K(t, [(INI(E12, 0) + 0.2, 0.0), (w_(E12, 0, 5), 1.0)], e_inout)
    cx, cy = MP.XY(c[0], c[1])
    z = c[2]
    with lz.grupo(960 - cx * z, 540 - cy * z, z):
        P.discontinua(lz, pts, (255, 214, 96), ancho=9.0 / z ** 0.5, largo=36 / z ** 0.5, hueco=24 / z ** 0.5, fase=-t * 40 / z ** 0.5, frac=u)
        hx, hy = pts[min(len(pts) - 1, int(u * (len(pts) - 1)))]
        with lz.grupo(hx, hy, 0.34 / z):
            for k in range(4):
                F.soldado(lz, -80 + k * 44, 0, 1.0, t, paso=0.9, lado=1, carga=0.0, brazos=(-0.1, 0.1), seed=k + 6, inc=0.18)
    tx, ty = MP.scr(c, -98.2, 19.32)
    a = smooth(prog(t, w_(E12, 0, 5) - 0.3, w_(E12, 0, 5) + 0.5))
    if a > 0.01:
        with lz.capa(2):
            for k in range(5):
                P.casa(lz, tx + 60 + k * 62, ty + 46 + 12 * (k % 2), 0.9 * a, calor=1.0)
            for k in range(3):
                F.guerrero(lz, tx - 40 - k * 46 + 60 * (1 - a), ty + 60, 0.6, t, paso=1.0, lado=1, arma="lanza", plumas=k, seed=k + 2)
            llama(lz, tx + 20, ty + 100, 0.7, t, seed=3, alfa=a)
    MP.marcador(lz, c, (-99.13, 19.43), "Tenochtitlan", alfa=smooth(prog(t, T0(E12), T0(E12) + 0.4)), dy=-52, px=34)
    MP.marcador(lz, c, (-98.2, 19.32), "Tlaxcala", alfa=smooth(prog(t, w_(E12, 0, 5) - 0.3, w_(E12, 0, 5) + 0.3)), dy=-56, px=36)
    etq(lz, t, w_(E12, 0, 6), w_(E12, 0, 9) + 0.8, "ciudad aliada", W / 2, 240, px=40)
    gran(lz, t, w_(E12, 0, 10), T1(E12) - 14.4 if False else 203.1, "SE RECUPERARON", W / 2, 150, px=86, col=(255, 240, 200))


snd(T0(E12) + 0.2, "pasos", 0.3, dur=4.0)
snd(w_(E12, 0, 5), "pop", 0.4)
snd(w_(E12, 0, 8), "fuego", 0.3, dur=2.0)


@shot(INI(E12, 1) - 0.1, bg=lambda t: bg_plano((30, 30, 70)), ent=("glitch", 0.5))
def r_viruela(lz, t):
    c = (0.0, 0.0, 3.0)
    ML.dibujar_valle(lz, t, c, noche=0.35, luces=0.4, detalle=1.0)
    tv = w_(E12, 1, 3)
    with cam(lz, 0, 0, c[2]):
        u = smooth(prog(t, tv, tv + 3.0))
        with lz.recorte(ML.isla_pts()):
            lz.relleno(circulo(-40, 30, 40 + 700 * u, 40), (216, 50, 70), alfa=0.36)
        for i in range(120):
            ta = tv + 3.0 * h01(1, i)
            if t < ta:
                continue
            a = (h01(2, i) * 6.283)
            r = (h01(3, i) ** 0.7) * 150
            x = -40 + math.cos(a) * r * 2.2 + 9 * math.sin(t * 3 + i)
            y = 30 + math.sin(a) * r * 1.6 + 9 * math.cos(t * 2.5 + i)
            rr = 5 + 3 * math.sin(t * 4 + i)
            lz.relleno(circulo(x, y, rr, 10), (230, 60, 80), alfa=0.9)
            for j in range(6):
                b = j / 6 * 6.283 + t
                lz.relleno(circulo(x + math.cos(b) * (rr + 3), y + math.sin(b) * (rr + 3), 1.8, 5), (255, 140, 150), alfa=0.9)
    # tarjetas: el emperador muere y sube otro
    a1 = vent(t, w_(E12, 1, 7) - 0.5, T1(E12), 0.4, 0.4)
    a2 = smooth(prog(t, w_(E12, 1, 9), w_(E12, 1, 10)))
    if a1 > 0.01:
        with lz.capa(2):
            lz.relleno(rect_red(300, 130, 340, 420, 26), (255, 255, 255), alfa=0.92 * a1)
            gris = P.mezcla((70, 190, 200), (150, 150, 160), smooth(prog(t, w_(E12, 1, 7), w_(E12, 1, 8))))
            F.tlatoani(lz, 470, 470, 1.9, t, lado=1, seed=2, manto=gris)
            P.rotulo(lz, 470, 176, "Cuitláhuac", px=40, color=(34, 28, 80), sombra=0.0, alfa=a1)
            P.pastilla(lz, 470, 590, "muere de viruela", px=30, alfa=a1)
    if a2 > 0.01:
        with lz.capa(2):
            lz.relleno(rect_red(1280, 130, 340, 420, 26), (255, 255, 255), alfa=0.92 * a2)
            F.tlatoani(lz, 1450 + 40 * (1 - a2), 470, 1.9, t, lado=-1, seed=5, manto=(230, 120, 70))
            P.rotulo(lz, 1450, 176, "Cuauhtémoc", px=40, color=(34, 28, 80), sombra=0.0, alfa=a2)
            P.pastilla(lz, 1450, 590, "nuevo emperador", px=30, alfa=a2)
    gran(lz, t, tv, tv + 2.2, "VIRUELA", W / 2, 130, px=104, col=(255, 110, 130))


snd(w_(E12, 1, 3), "glitch", 0.35)
snd(w_(E12, 1, 3) + 0.4, "hmm", 0.45)
snd(w_(E12, 1, 9), "pop", 0.4)


def _flota(lz, t, c, n_vis, t0, t1_, cerrar=0.0, destruida=0.0):
    """Trece bergantines que entran al lago desde el este y rodean la isla; canoas aliadas en enjambre."""
    for i in range(13):
        ti = t0 + (t1_ - t0) * i / 13.0
        if t < ti:
            continue
        u = e_out(prog(t, ti, ti + 1.6))
        ang = i / 13 * 6.283 + 0.25
        rad = lerp(2.5, 1.95, cerrar)
        xf, yf = math.cos(ang) * rad * 1.15, -0.05 + math.sin(ang) * rad * 0.85
        xs, ys = lerp(9.0, xf, u), lerp(-1.0, yf, u)
        X, Y = ML.km(xs, ys)
        lado = 1 if xs < 0 else -1
        F.bergantin(lz, X, Y, 0.34, t + i, lado=lado, seed=i)
        lz.relleno(circulo(X - lado * 40, Y + 4, 4, 8), (255, 255, 255), alfa=0.4 * (1 - u))
    for j in range(70):
        tj = t0 + 0.4 + (t1_ - t0) * h01(4, j)
        if t < tj:
            continue
        u = e_out(prog(t, tj, tj + 2.0))
        ang = h01(5, j) * 6.283
        rad = lerp(2.9, 2.55, cerrar) + 0.15 * h01(6, j)
        xf, yf = math.cos(ang) * rad * 1.15, -0.05 + math.sin(ang) * rad * 0.85
        xs, ys = lerp(12.0 + 4 * h01(7, j), xf, u), lerp(-2.0 + 4 * h01(8, j), yf, u)
        X, Y = ML.km(xs, ys)
        lz.relleno(elipse(X, Y, 8, 3.4, 0.0, 10), (60, 200, 210))
        lz.relleno(circulo(X, Y - 3, 2.6, 6), (255, 214, 96))


@shot(INI(E12, 2) - 0.1, bg=lambda t: bg_plano((20, 44, 100)), ent=("tinta", 0.7))
def r_flota(lz, t):
    c = Klog(t, [(INI(E12, 2) - 0.1, (2.0, -1.5, 0.9)), (w_(E12, 2, 15), (0.0, 0.0, 1.05))])
    ML.dibujar_valle(lz, t, c, noche=0.15, luces=0.0, detalle=smooth(prog(c[2], 0.85, 1.0)) * 0.6, lago=1.0)
    with cam(lz, c[0] * ML.PXKM, -c[1] * ML.PXKM, c[2]):
        _flota(lz, t, c, 13, w_(E12, 2, 7), w_(E12, 2, 14))
    n = min(13, int(13 * prog(t, w_(E12, 2, 7), w_(E12, 2, 14))) + (1 if t > w_(E12, 2, 7) else 0))
    if t > w_(E12, 2, 7):
        P.rotulo(lz, 260, 200, str(n), px=200, color=ORO, alfa=1.0)
        P.pastilla(lz, 260, 320, "bergantines", px=36)
    cifra(lz, t, w_(E12, 2, 1), "mayo de 1521", W / 2, 110, px=70, col=BLANCO, t1=w_(E12, 2, 6))
    etq(lz, t, w_(E12, 2, 9), w_(E12, 2, 12) + 1.0, "miles de aliados indígenas", 1500, 240, px=38)


snd(w_(E12, 2, 7), "whoosh", 0.4, dur=0.7)
for _i in range(13):
    snd(w_(E12, 2, 7) + (w_(E12, 2, 14) - w_(E12, 2, 7)) * _i / 13.0, "pop", 0.25, tono=0.8 + 0.03 * _i)
snd(w_(E12, 2, 13), "ding", 0.4)


@shot(INI(E12, 3) - 0.1, bg=lambda t: bg_plano((20, 44, 100)), ent=("fundido", 0.5))
def r_asedio(lz, t):
    c = Klog(t, [(INI(E12, 3) - 0.1, (0.0, 0.0, 1.05)), (T1(E12), (0.0, 0.0, 2.0))])
    ruina = smooth(prog(t, w_(E12, 3, 6), w_(E12, 3, 12)))
    ML.dibujar_valle(lz, t, c, noche=0.2 + 0.4 * ruina, luces=0.0, detalle=1.0 - 0.3 * ruina, lago=1.0)
    with cam(lz, c[0] * ML.PXKM, -c[1] * ML.PXKM, c[2]):
        cerr = smooth(prog(t, INI(E12, 3), w_(E12, 3, 5)))
        _flota(lz, t, c, 13, -100.0, -99.0, cerrar=cerr)
        with lz.recorte(ML.isla_pts()):
            lz.relleno(circulo(0, 0, 500, 40), (70, 60, 70), alfa=0.5 * ruina)
        for i in range(9):
            a = h01(3, i) * 6.283
            r = (0.2 + 0.8 * h01(4, i)) * 100
            X, Y = math.cos(a) * r * 1.6, math.sin(a) * r * 1.1
            if ruina > 0.05:
                llama(lz, X, Y, 0.5 * ruina, t, seed=i, alfa=ruina)
                humo(lz, X, Y - 20, t, 0.0, n=4, s=0.4, alfa=0.35 * ruina, seed=i)
        ring = circulo(0, 0, 2.3 * ML.PXKM * (1 - 0.2 * cerr), 60)
        P.discontinua(lz, np.vstack([ring, ring[:1]]), (255, 226, 130), ancho=5.0, largo=22, hueco=16, fase=-t * 30, frac=cerr)
    # calendario: mayo -> agosto
    pr = prog(t, INI(E12, 3), T1(E12) - 0.5)
    with lz.capa(2):
        lz.relleno(rect_red(460, 92, 1000, 84, 24), (255, 255, 255), alfa=0.92)
        lz.relleno(rect_red(476, 118, 968, 22, 11), (200, 205, 230))
        lz.relleno(rect_red(476, 118, 968 * pr, 22, 11), (226, 80, 80))
        for k, m in enumerate(("mayo", "junio", "julio", "agosto")):
            P.rotulo(lz, 476 + 968 * (k + 0.5) / 4, 160, m, px=26, color=(34, 28, 80), sombra=0.0)
    cifra(lz, t, w_(E12, 3, 2), "3 meses", W / 2, 260, px=100, col=(255, 130, 110), t1=w_(E12, 3, 6))
    gran(lz, t, w_(E12, 3, 10), T1(E12) - 0.1, "LA CIUDAD ESTABA DESTRUIDA", W / 2, 260, px=72, col=(255, 240, 220))


snd(INI(E12, 3), "fuego", 0.35, dur=4.0)
snd(w_(E12, 3, 7), "hmm", 0.4)
snd(w_(E12, 3, 12), "suspiro", 0.4, dur=1.4)
