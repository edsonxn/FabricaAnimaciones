# -*- coding: utf-8 -*-
"""Capítulos `cerro` (1546-1548) y `campamento` (1549-1550): actores y escenografía sobre el plano llano."""
import math

import numpy as np

import locales as L
import subsuelo as S
import vox as V
from cap_local import A, FIG, MUL, SUR, CASAS, CAMP_DX, casa_en, bocamina
from ctx import INI, FIN
from motor import prog, e_back, e_inout, smooth, clamp01, h01, lerp, rect_red


def _y(x, prof=70.0):
    return float(L.h(x)) + prof


def piedra(lz, x, y, s=1.0, t=0.0, brillo=1.0):
    with lz.grupo(x, y, s):
        lz.relleno(V.poligono_reg(0, 0, 22, 6, 0.4), (110, 104, 108), temblor=0.0, capa=1)
        lz.relleno(np.array([[-8, -12], [12, -16], [18, -2], [0, 4]]), V.PLATA, temblor=0.0, capa=1)
        if brillo > 0:
            L.chispa(lz, 12, -22, 20 * brillo, t, capa=2)
            L.chispa(lz, -16, -10, 12 * brillo, t + 1.3, seed=2, capa=2)


def odre(lz, x, y, s=1.0, alfa=1.0):
    """Odre (bota de vino): bolsa de cuero abultada con patitas (piel de cabra) y cuello con tapón."""
    with lz.grupo(x, y, s):
        cuero, claro, osc = (160, 104, 66), (196, 140, 92), (112, 70, 46)
        for dx, dy, ang in ((-46, 34, 0.25), (-12, 40, 0.05), (26, 40, -0.05), (58, 30, -0.3)):
            lz.relleno(V.capsula([dx, dy - 20], [dx + 14 * ang * 4, dy + 20], 22, 15), osc, temblor=0.0, capa=1, alfa=alfa)
        lz.relleno(V.elipse_pts(0, -4, 84, 52, -0.15), cuero, temblor=0.0, capa=1, alfa=alfa)
        lz.relleno(V.elipse_pts(-16, -18, 46, 22, -0.2), claro, temblor=0.0, capa=1, alfa=alfa)
        lz.relleno(V.capsula([54, -30], [86, -76], 30, 20), cuero, temblor=0.0, capa=1, alfa=alfa)
        lz.relleno(V.capsula([84, -74], [96, -92], 24, 20), osc, temblor=0.0, capa=1, alfa=alfa)
        lz.trazo(np.array([[-50, -6], [-10, 2], [40, -4]]), osc, 5, afinar=False, temblor=0.0, capa=1)


X_ENCUENTRO = (-300.0, -190.0)         # indígena, Tolosa
X_CAMPAM = 470.0                        # donde Tolosa arma el campamento (al pie de la Bufa)
VETA_PTS = np.array([[640, -60], [690, -170], [738, -260], [790, -340], [846, -430]], float)


def veta_bufa(lz, t, frac, alfa=1.0):
    """La veta de San Bernabé aflorando en la ladera de la Bufa: cinta de plata que se dibuja sola."""
    if frac <= 0.005:
        return
    P = V._parcial(VETA_PTS, frac)
    if len(P) < 2:
        return
    lz.trazo(P, (232, 208, 170), 26, afinar=False, temblor=0.0, capa=1)
    lz.trazo(P, V.PLATA, 12, afinar=False, temblor=0.0, capa=1)
    for i, p in enumerate(P[1:]):
        L.chispa(lz, p[0] + 22, p[1] - 12, 16 + 8 * (i % 2), t + i, seed=i, capa=2, alfa=alfa)


def dibujar_cerro(lz, t, tc, cam_l):
    fase = prog(t, A["llega"] - 0.2, A["llega"] + 5.6)
    x_t = lerp(X_ENCUENTRO[1], X_CAMPAM, e_inout(fase))
    llega = fase > 0
    caminando = 0 < fase < 1
    señala = V.SEÑALAR[V.cuadro(V.SEÑALAR, t, 2.5)]
    if not llega:
        V.figura(lz, X_ENCUENTRO[0], _y(0), FIG, señala, "indigena", 1, seed=5)
        kp = e_back(prog(t, A["piedras"], A["piedras"] + 0.35), 1.8)
        if kp > 0.01:
            piedra(lz, X_ENCUENTRO[0] + 46, _y(0) - 74, 1.1 * kp, t, brillo=kp)
        V.figura(lz, X_ENCUENTRO[1], _y(0), FIG, V.pose_de(V.IDLE, t, 2.5), "tolosa", -1, seed=1)
        V.mula(lz, -110, _y(0) + 12, MUL, 0, 1, "costales", seed=2)
    else:
        f = V.cuadro(V.CAMINAR, t, 15.0)
        V.figura(lz, x_t, _y(0), FIG, V.CAMINAR[f] if caminando else V.pose_de(V.IDLE, t, 2.5), "tolosa", 1, seed=1)
        V.mula(lz, x_t + 130, _y(0) + 12, MUL, f if caminando else 0, 1, "costales", seed=2)
        V.figura(lz, X_ENCUENTRO[0], _y(0), FIG, señala, "indigena", 1, seed=5)
    # odre + rótulo de la Bufa
    ko = e_back(prog(t, A["odre"], A["odre"] + 0.5), 1.7) * (1 - smooth(prog(t, A["arma"] + 1.0, A["arma"] + 1.6)))
    if ko > 0.01:
        odre(lz, 590, -560, 1.7 * ko)
        V.pastilla(lz, 590, -430, "ODRE DE VINO", 30, k=ko, fondo=V.CREMA)
        V.trazo_mano(lz, np.array([[700, -600], [780, -640], [850, -700]]), prog(t, A["odre"] + 0.3, A["odre"] + 1.0), V.CREMA, 10, seed=3)
    # campamento de Tolosa: tiendas + fogata
    for i, (tx, fila) in enumerate([(X_CAMPAM - 110, 0), (X_CAMPAM + 90, 1), (X_CAMPAM + 200, 0)]):
        k = prog(t, A["arma"] + 0.15 * i, A["arma"] + 0.6 + 0.15 * i)
        if k > 0:
            L.tienda(lz, tx, _y(tx, 26 + 44 * fila), 1.6, k, 40 + i)
    if t > A["arma"] + 0.6:
        L.fogata(lz, X_CAMPAM + 20, _y(0, 96), 1.3, t)
    # la veta de San Bernabé y la fiebre
    fv = smooth(prog(t, A["veta"] - 0.2, A["veta"] + 2.6))
    veta_bufa(lz, t, fv)
    if fv > 0:
        k = e_back(prog(t, A["bernabe"], A["bernabe"] + 0.4), 1.7)
        if k > 0.01:
            V.pastilla(lz, 880, -250, "SAN BERNABÉ", 40, k=k, fondo=V.AMARILLO)
    if t > A["fiebre"] - 0.2:
        u0 = A["fiebre"] - 0.2
        trajes = ("arriero", "indigena", "minero", "africano", "soldado", "mujer", "tolosa", "cargador")
        for i in range(10):
            x0 = -260 + 160 * i if i % 2 == 0 else 1400 - 110 * i
            u = e_inout(prog(t, u0 + 0.10 * i, u0 + 2.7 + 0.10 * i))
            x = lerp(x0, 640 + 30 * (i % 4), u)
            f = V.cuadro(V.CAMINAR, t, 15.0, 0.07 * i)
            V.figura(lz, x, _y(0, 36 + 8 * (i % 4)), FIG * (0.9 + 0.1 * (i % 3)),
                     V.CAMINAR[f] if u < 1 else V.IDLE[int(t * 2.2 + i) % 2],
                     trajes[i % len(trajes)], 1 if x0 < 640 else -1, seed=300 + i)


MINAS34_X = [(-1300 + (i // 2) * 160 + (i % 2) * 80 + 10 * h01(77, i)) for i in range(34)]


def hospital(lz, x, y, s, k):
    kk = e_back(clamp01(k), 1.7) if k < 1 else 1
    if kk <= 0.01:
        return
    with lz.grupo(x, y, s, sy=s * kk):
        lz.relleno(rect_red(-80, -100, 160, 100, 3), (238, 230, 214), temblor=0.0, capa=1)
        lz.relleno(np.array([[-90, -100], [90, -100], [64, -130], [-64, -130]]), L.TEJA, temblor=0.0, capa=1)
        lz.relleno(rect_red(-16, -60, 32, 60, 14), (60, 44, 40), temblor=0.0, capa=1)
        lz.relleno(rect_red(-6, -128, 12, 34, 0), V.ROJO, temblor=0.0, capa=1)
        lz.relleno(rect_red(-17, -117, 34, 12, 0), V.ROJO, temblor=0.0, capa=1)


def dibujar_campamento(lz, t, tc, cam_l):
    ti = INI("campamento")
    L.arroyo(lz, x0=-260, x1=-190, y0=2, y1=SUR - 8)
    bocamina(lz, -40, SUR * 0.42, 1.5, 1.0, t)
    for i, (x, tipo, fila, seed) in enumerate(CASAS):
        t0 = A["casas"] - 0.4 + 0.30 * i if i > 2 else ti - 5
        casa_en(lz, t, x, tipo, fila, seed, t0)
    for i, (tx, fila) in enumerate([(X_CAMPAM - 110, 0), (X_CAMPAM + 90, 1), (X_CAMPAM + 200, 0)]):
        L.tienda(lz, tx, _y(tx, 26 + 44 * fila), 1.6, 1.0, 40 + i)
    L.fogata(lz, X_CAMPAM + 20, _y(0, 96), 1.3, t)
    if t > A["casas"]:
        for i in range(6):
            ph = t * (0.25 + 0.03 * i) + i * 1.7
            x = -170 + 340 * (0.5 + 0.5 * math.sin(ph)) + 70 * i
            dr = 1 if math.cos(ph) > 0 else -1
            V.figura(lz, x, _y(0, 60 + 12 * (i % 4)), FIG * (0.92 + 0.04 * (i % 3)),
                     V.CAMINAR[V.cuadro(V.CAMINAR, t, 15.0, 0.11 * i)],
                     ("indigena", "arriero", "africano", "mujer", "minero", "soldado")[i], dr, seed=320 + i)
    # abasto: mulas con costales + vaca (maíz y carne llegan de rancherías lejanas)
    ua = e_inout(prog(t, A["maiz"] - 0.6, A["ranch"] + 2.4))
    if t >= A["maiz"] - 0.6:
        for i in range(2):
            x = lerp(1250 + 170 * i, 240 + 170 * i, ua)
            V.mula(lz, x, _y(0, 120), MUL, V.cuadro(V.CAMINAR, t, 15.0, 0.1 * i) if ua < 1 else 0, -1, "costales", seed=340 + i)
        S.vaca(lz, lerp(1760, 760, ua), _y(0, 128), 0.6, -1)
    # 34 minas en las lomas del fondo
    n = int(34 * prog(t, A["t34"] - 0.2, A["t34"] + 3.2))
    for i in range(n):
        bocamina(lz, MINAS34_X[i], 4 - 44 * (i % 2), 1.7, prog(t, A["t34"] - 0.2 + i * 0.094, A["t34"] + 0.15 + i * 0.094), t)
    # hospitales y hospicios
    for i, hx in enumerate((560, -420)):
        hospital(lz, hx, _y(hx, 110), 1.35, prog(t, A["hosp"] + 0.3 * i, A["hosp"] + 0.7 + 0.3 * i))
