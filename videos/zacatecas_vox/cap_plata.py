# -*- coding: utf-8 -*-
"""Capítulo `plata`: la ruta de la plata (Zacatecas -> capital -> Veracruz -> Sevilla) y las monedas que se reparten."""
import math

import numpy as np

import geo as G
import mapa_dib as M
import ui_vox as U
import vox as V
from ctx import T, INI, FIN
from motor import W, H, prog, e_out, e_back, e_inout, smooth, clamp01, h01, lerp, rect_red

A = dict(
    ini=INI("plata"), fin=FIN("plata"),
    mulas=T("plata", "mulas"), carretas=T("plata", "carretas"), capital=T("plata", "capital"), mar=T("plata", "mar"),
    sevilla=T("plata", "Sevilla"), lejos=T("plata", "lejos"),
    monedas=T("plata", "monedas"), guerras=T("plata", "guerras"), imperios=T("plata", "imperios"),
    comercio=T("plata", "comercio"), contin=T("plata", "continentes"),
)
RUTA_T0 = A["ini"] + 0.4
RUTA_T1 = A["sevilla"] + 0.6
SEV = G.xy(*G.CIUDADES["sevilla"])


def frac_ruta(t):
    return e_inout(prog(t, RUTA_T0, RUTA_T1)) if False else clamp01((t - RUTA_T0) / (RUTA_T1 - RUTA_T0))


def punto_ruta(t):
    return G.punto_ruta(frac_ruta(t))


def nao(lz, x, y, s=1.0, rot=0.0, capa=2):
    with lz.grupo(x, y, s, rot):
        lz.relleno(np.array([[-70, 0], [70, 0], [54, 34], [-54, 34]]), (120, 80, 56), temblor=0.0, capa=capa)
        lz.relleno(np.array([[-70, 0], [-84, -18], [-58, 0]]), (120, 80, 56), temblor=0.0, capa=capa)
        lz.relleno(rect_red(-3, -110, 6, 110, 1), (96, 66, 48), temblor=0.0, capa=capa)
        lz.relleno(np.array([[-52, -100], [-4, -100], [-4, -22], [-52, -22]]), V.CREMA, temblor=0.0, capa=capa)
        lz.relleno(np.array([[4, -104], [54, -104], [54, -26], [4, -26]]), V.CREMA, temblor=0.0, capa=capa)
        lz.relleno(rect_red(-32, -76, 8, 32, 0), V.ROJO, temblor=0.0, capa=capa)
        lz.relleno(rect_red(-42, -66, 28, 8, 0), V.ROJO, temblor=0.0, capa=capa)


def moneda(lz, x, y, r, rot=0.0, capa=2, alfa=1.0, canto=True):
    with lz.grupo(x, y, 1.0, rot):
        if canto:
            lz.relleno(V.elipse_pts(0, r * 0.12, r, r), V.PLATA_OSC, temblor=0.0, capa=capa, alfa=alfa)
        lz.relleno(V.elipse_pts(0, 0, r, r), V.PLATA, temblor=0.0, capa=capa, alfa=alfa)
        lz.relleno(V.elipse_pts(0, 0, r * 0.78, r * 0.78), V.aclarar(V.PLATA, 0.4), temblor=0.0, capa=capa, alfa=alfa)
        lz.relleno(V.elipse_pts(0, 0, r * 0.64, r * 0.64), V.PLATA, temblor=0.0, capa=capa, alfa=alfa)
        lz.relleno(rect_red(-r * 0.07, -r * 0.42, r * 0.14, r * 0.84, 0), V.PLATA_OSC, temblor=0.0, capa=capa, alfa=alfa)
        lz.relleno(rect_red(-r * 0.42, -r * 0.07, r * 0.84, r * 0.14, 0), V.PLATA_OSC, temblor=0.0, capa=capa, alfa=alfa)


def dibujar(lz, t, z):
    """Dibujo sobre el mapa (coordenadas de mundo). z = zoom de cámara (para tamaños constantes en pantalla)."""
    from cap_mapa import etiqueta
    fr = frac_ruta(t)
    M.ruta(lz, fr, V.ROJO, 7.0 / z * 0.55, fase=t * 30.0)
    # etiquetas de las paradas
    for lon_lat, txt, t0 in [(G.CIUDADES["mexico"], "CIUDAD DE MÉXICO", A["capital"]), (G.CIUDADES["veracruz"], "VERACRUZ", A["mar"]),
                             (G.CIUDADES["sevilla"], "SEVILLA", A["sevilla"])]:
        x, y = G.xy(*lon_lat)
        if t >= t0:
            lz.puntos([(x, y)], 10 / z, V.CREMA, capa=2)
            lz.puntos([(x, y)], 6.5 / z, V.ROJO, capa=2)
            etiqueta(lz, t, t0, x, y - 60 / z, txt, z, px=26)
    # convoy de mulas y carretas sobre la ruta (tramo terrestre) y nao en el mar
    px, py = punto_ruta(t)
    if fr < 0.36:
        for i in range(3):
            q = G.punto_ruta(max(0.0, fr - 0.012 * i))
            V.mula(lz, q[0], q[1] + 22 / z, 0.5 / z * 0.6, V.cuadro(V.CAMINAR, t + i * 0.1, 15.0), 1, "barras", seed=i, capa=2)
    elif fr < 1.0:
        nao(lz, px, py - 10 / z, 0.55 / z, math.sin(t * 2.2) * 0.05)
    # rótulos de la geografía (España, Francia, África) mientras se ve el Atlántico oriental
    if A["sevilla"] < t < A["contin"] + 1.5 and z < 0.4:
        for lon_lat, txt in (((-3.5, 40.0), "ESPAÑA"), ((2.0, 47.0), "FRANCIA"), ((-2.0, 30.5), "ÁFRICA")):
            gx, gy = G.xy(*lon_lat)
            V.rotulo(lz, txt, gx, gy, 26 / z * 0.9, color=V.TINTA, fuente="vox_b", sombra=0.0)
    # monedas: barras que se vuelven monedas y salen en abanico hacia Europa, Asia y África
    if t >= A["monedas"] - 0.6:
        u = t - A["monedas"]
        # pila de barras en Sevilla (aparece un poco antes)
        kb = e_back(prog(t, A["monedas"] - 0.6, A["monedas"] - 0.2))
        if kb > 0.01 and u < 1.2:
            for i in range(3):
                with lz.grupo(SEV[0] - 60 + 60 * i, SEV[1] - 40 - 14 * (i % 2), kb * 1.4 / z * 0.2):
                    lz.relleno(np.array([[-46, -14], [46, -14], [58, 16], [-58, 16]]), V.PLATA, temblor=0.0, capa=2)
        dirs = [(-0.95, "GUERRAS", A["guerras"]), (0.05, "IMPERIOS", A["imperios"]), (0.85, "COMERCIO", A["comercio"])]
        for j, (ang, txt, t0) in enumerate(dirs):
            for i in range(9):
                v = clamp01((u - 0.05 - 0.17 * i - 0.25 * j) / 2.6)
                if v <= 0 or v >= 1:
                    continue
                d = 1500 * e_out(v) * (0.5 + 0.1 * (i % 4))
                a_ = ang + 0.10 * ((i % 3) - 1)
                x = SEV[0] + d * math.cos(a_) * 1.05
                y = SEV[1] - 80 + d * math.sin(a_) * 0.7 - 300 * math.sin(math.pi * v)
                moneda(lz, x, y, 36 / z, rot=v * 9 * (1 if i % 2 else -1), alfa=1 - 0.7 * smooth(prog(v, 0.85, 1.0)))
            k = e_back(prog(t, t0, t0 + 0.35), 1.7)
            if k > 0.01:
                x = SEV[0] + 900 * math.cos(ang) * 1.0 - 100
                y = SEV[1] - 80 + 1000 * math.sin(ang) * 0.6 - 330
                etiqueta(lz, t, t0, x, y, txt, z, px=30, fondo=V.AMARILLO)
