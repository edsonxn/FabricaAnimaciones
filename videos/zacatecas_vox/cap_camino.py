# -*- coding: utf-8 -*-
"""Capítulo `camino`: la plata sale por el Camino Real; guerra chichimeca, presidio, escolta y paz de Caldera."""
import math

import numpy as np

import locales as L
import subsuelo as S
import ui_vox as U
import vox as V
from cap_local import FIG, MUL, SUR
from ctx import T, INI, FIN
from motor import W, H, prog, e_out, e_back, e_inout, smooth, clamp01, h01, lerp, rect_red

A = dict(
    ini=INI("camino"), fin=FIN("camino"),
    llegar=T("camino", "llegar"), mexico=T("camino", "México"), camino=T("camino", "camino"), guerra=T("camino", "guerra"),
    c50=T("camino", "cincuenta"), chichi=T("camino", "chichimecas"), atacan=T("camino", "atacan"),
    carav=T("camino", "caravanas", frase=1), defienden=T("camino", "defienden"), tierras=T("camino", "tierras"),
    invaden=T("camino", "invaden"),
    conflicto=T("camino", "conflicto"), largo=T("camino", "largo"), caro=T("camino", "caro"),
    presidios=T("camino", "presidios"), escolta=T("camino", "escolta"),
    final=T("camino", "final"), fuerza=T("camino", "fuerza"), basta=T("camino", "basta"),
    n90=T("camino", "noventa"), caldera=T("camino", "Caldera"), paz=T("camino", "paz"), comida=T("camino", "comida"),
    ropa=T("camino", "ropa"), ganado=T("camino", "ganado"),
)

ROAD_DY = 84.0            # el camino corre a esta profundidad bajo el perfil del terreno


def y_camino(x):
    return float(L.h(x)) + ROAD_DY


# posiciones clave de la caravana: (tiempo, x)
X_ATAQUE = 1000.0
X_FUERTE = 1900.0
X_PAZ = 2500.0
TREN = [(INI("patio"), -560.0), (A["ini"], -560.0), (A["ini"] + 3.0, 160.0), (A["atacan"] - 0.3, X_ATAQUE),
        (A["conflicto"] + 2.0, X_ATAQUE), (A["presidios"] + 2.2, X_FUERTE), (A["basta"] + 0.3, X_FUERTE),
        (A["n90"] + 0.6, X_PAZ - 320), (A["fin"], X_PAZ - 320)]


def x_tren(t):
    ts = [a for a, _ in TREN]
    xs = [b for _, b in TREN]
    return float(np.interp(t, ts, xs))


def en_marcha(t):
    """True si la caravana camina (la posición cambia)."""
    return abs(x_tren(t + 0.05) - x_tren(t - 0.05)) > 0.5


def camino_cinta(lz, x0, x1, alfa=1.0):
    xs = np.arange(x0, x1 + 40, 40.0)
    ys = np.array([y_camino(x) for x in xs])
    P = np.vstack([np.stack([xs, ys - 22], 1), np.stack([xs[::-1], ys[::-1] + 26], 1)])
    lz.relleno(P, (232, 206, 160), temblor=0.0, capa=1, alfa=alfa)
    # rayas del camino
    for x in np.arange(x0, x1, 120.0):
        lz.relleno(rect_red(x, y_camino(x) - 2, 44, 5, 2), (206, 176, 130), temblor=0.0, capa=1, alfa=alfa)


def letrero(lz, x, y, txt, s=1.0):
    with lz.grupo(x, y, s):
        lz.relleno(rect_red(-6, -120, 12, 120, 3), L.MADERA, temblor=0.0, capa=1)
        lz.relleno(np.array([[-110, -190], [70, -190], [110, -158], [70, -126], [-110, -126]]), (236, 214, 168), temblor=0.0, capa=1)
        lz.texto(txt, -6, -158, 40, "vox_b", color=V.TINTA, borde=None, temblor=0.0, capa=2)


def fuerte(lz, x, y, k=1.0, t=0.0):
    """Presidio: muro de adobe con torreón y bandera."""
    kk = 0 if k <= 0 else (e_back(clamp01(k), 1.6) if k < 1 else 1.0)
    if kk <= 0.01:
        return
    with lz.grupo(x, y, 1.0, sy=kk):
        lz.relleno(rect_red(-190, -120, 380, 120, 4), L.ADOBE, temblor=0.0, capa=1)
        lz.relleno(rect_red(150, -120, 40, 120, 0), L.ADOBE_OSC, temblor=0.0, capa=1)
        for i in range(8):
            lz.relleno(rect_red(-190 + i * 48, -146, 32, 30, 2), L.ADOBE, temblor=0.0, capa=1)
        lz.relleno(rect_red(-60, -260, 120, 260, 4), L.ADOBE_OSC if False else (188, 140, 96), temblor=0.0, capa=1)
        lz.relleno(np.array([[-72, -260], [72, -260], [60, -296], [-60, -296]]), L.TEJA, temblor=0.0, capa=1)
        lz.relleno(rect_red(-24, -100, 48, 100, 22), (54, 40, 38), temblor=0.0, capa=1)
        lz.relleno(rect_red(-16, -220, 32, 38, 12), (54, 40, 38), temblor=0.0, capa=1)
        lz.trazo(np.array([[0, -296], [0, -380]]), L.MADERA, 6, afinar=False, temblor=0.0, capa=1)
        ondea = 10 * math.sin(t * 5)
        lz.relleno(np.array([[0, -380], [66, -366 + ondea], [0, -340]]), V.ROJO, temblor=0.0, capa=1)


def flecha(lz, p, ang, s=1.0, capa=2):
    d = np.array([math.cos(ang), math.sin(ang)]) * 60 * s
    lz.trazo(np.array([p - d, p]), (110, 76, 50), 7, afinar=False, temblor=0.0, capa=capa)
    n = np.array([-math.sin(ang), math.cos(ang)])
    lz.relleno(np.array([p + d * 0.25 + n * 6, p + d * 0.5, p + d * 0.25 - n * 6]), V.PLATA_OSC, temblor=0.0, capa=capa)


def dibujar(lz, t, tc, cam_l):
    x0 = x_tren(t)
    marcha = en_marcha(t)
    camino_cinta(lz, -480, 4200)
    if A["llegar"] - 1.0 < t < A["camino"] + 5:
        letrero(lz, 60, y_camino(60) - 6, "MÉXICO →", 1.2)
    # ---- caravana: 5 mulas cargadas (barras) + arrieros (sale del patio al empezar el capítulo)
    for i in range(5 if t > A["ini"] - 0.5 else 0):
        xm = x0 - i * 150
        f = V.cuadro(V.CAMINAR, t + 0.09 * i, 30.0) if marcha else 0
        V.mula(lz, xm, y_camino(xm) + 6, MUL, f, 1, "barras", seed=60 + i)
    fr = V.cuadro(V.CAMINAR, t, 30.0) if marcha else 0
    xa = x0 + 120
    V.figura(lz, xa, y_camino(xa) + 26, FIG, V.CAMINAR[fr] if marcha else V.IDLE[int(t * 2.2) % 2], "arriero", 1, seed=70)
    # ---- guerra: arqueros en la loma
    for i, (bx, by) in enumerate(((742, -470), (800, -520), (838, -640))):
        k = e_back(prog(t, A["atacan"] - 0.6 + i * 0.2, A["atacan"] - 0.1 + i * 0.2))
        vis = 1.0 if t < A["presidios"] + 3.0 else clamp01(1 - prog(t, A["n90"] - 1.0, A["n90"] + 0.4) * 0.0)
        if k > 0.01 and A["atacan"] - 0.6 < t:
            f = V.cuadro(V.ARCO, t + i * 0.2, 4.0) if t < A["n90"] else 0
            yb = by
            V.figura(lz, bx, yb, FIG * k, V.ARCO[f], "guachichil", -1, obj=[("arco", 1.0)], seed=80 + i)
    # flechas en el aire entre los arqueros y la caravana
    if A["atacan"] <= t < A["basta"]:
        for i in range(3):
            ph = ((t - A["atacan"]) * 0.9 + i * 0.33) % 1.0
            xs = lerp(760, X_ATAQUE - 60 - 90 * i, ph)
            ys = lerp(-500, y_camino(xs) - 30, ph) - 220 * math.sin(math.pi * ph)
            flecha(lz, np.array([xs, ys]), 1.1 + 1.0 * ph - 0.2 * i, 1.7)
    # ---- presidio y escolta
    fuerte(lz, X_FUERTE, y_camino(X_FUERTE) - 30, prog(t, A["presidios"], A["presidios"] + 0.5), t)
    for i in range(3):
        ks = prog(t, A["escolta"] - 0.2 + 0.25 * i, A["escolta"] + 0.5 + 0.25 * i)
        if ks > 0:
            xs = X_FUERTE - 220 - 70 * i + (x0 - X_FUERTE + 220) * clamp01(prog(t, A["escolta"] + 0.5, A["escolta"] + 2.5)) if t < A["basta"] + 2 else x0 - 60 * i - 400
            xs = min(xs, x0 + 240)
            V.figura(lz, xs, y_camino(xs) + 42, FIG, V.CAMINAR[V.cuadro(V.CAMINAR, t + i * 0.1, 15.0)] if marcha else V.IDLE[0], "soldado", 1,
                     obj=[("d", "lanza", 0, 0.9)], seed=90 + i)
    # ---- paz: Caldera se acerca a los guachichiles; comida, ropa y ganado
    if t >= A["n90"]:
        xc = X_PAZ - 100
        V.figura(lz, xc - 320 + 220 * e_inout(prog(t, A["caldera"] - 0.5, A["caldera"] + 2.5)), y_camino(xc) + 40, FIG,
                 V.CAMINAR[V.cuadro(V.CAMINAR, t, 15.0)] if prog(t, A["caldera"] - 0.5, A["caldera"] + 2.5) < 1 else V.IDLE[int(t * 2.2) % 2],
                 "caldera", 1, seed=100)
        xg = X_PAZ + 230
        for i in range(3):
            V.figura(lz, xg + 70 * i, y_camino(xg) + 30 + 8 * i, FIG, V.IDLE[int(t * 2 + i) % 2], "guachichil", -1, seed=110 + i)
        # bienes
        kb = e_back(prog(t, A["comida"], A["comida"] + 0.4))
        if kb > 0.01:
            for j in range(3):
                with lz.grupo(X_PAZ - 30 + j * 44, y_camino(X_PAZ) + 20, kb):
                    lz.relleno(V.elipse_pts(0, -22, 26, 22), (206, 180, 130), temblor=0.0, capa=1)
                    lz.relleno(V.capsula([-14, -40], [14, -40], 8), (140, 100, 64), temblor=0.0, capa=1)
        kr = e_back(prog(t, A["ropa"], A["ropa"] + 0.4))
        if kr > 0.01:
            with lz.grupo(X_PAZ + 130, y_camino(X_PAZ) + 22, kr):
                lz.relleno(rect_red(-30, -34, 60, 34, 3), V.TEAL, temblor=0.0, capa=1)
                lz.relleno(rect_red(-30, -60, 60, 28, 3), V.ROJO, temblor=0.0, capa=1)
        kg = e_back(prog(t, A["ganado"], A["ganado"] + 0.4))
        if kg > 0.01:
            S.vaca(lz, X_PAZ + 20, y_camino(X_PAZ) + 90, 0.6 * kg, 1)
