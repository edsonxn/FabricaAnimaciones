# -*- coding: utf-8 -*-
"""Capítulo `ciudad`: la aldea se vuelve ciudad (casas de piedra, convento franciscano, título, escudo, mercados)
y la ciudad de hoy (usada en el cierre)."""
import math

import numpy as np

import locales as L
import subsuelo as S
import ui_vox as U
import vox as V
from cap_local import FIG, MUL, SUR, CASAS, casa_en
from ctx import T, INI, FIN
from motor import W, H, prog, e_out, e_back, e_inout, smooth, clamp01, h01, lerp, rect_red, ancho_texto

A = dict(
    ini=INI("ciudad"), fin=FIN("ciudad"),
    aldea=T("ciudad", "aldea"), ciudad0=T("ciudad", "ciudad"),
    francis=T("ciudad", "franciscanos"), convento=T("ciudad", "convento"), c58=T("ciudad", "ocho", frase=1),
    o85=T("ciudad", "ochenta", frase=2), rey=T("ciudad", "rey"), titulo=T("ciudad", "título"),
    o88=T("ciudad", "ochenta", frase=3), escudo=T("ciudad", "escudo"),
    entonces=T("ciudad", "entonces"), mercados=T("ciudad", "mercados"), matadero=T("ciudad", "matadero"),
    reglas=T("ciudad", "reglas"),
)

# casas de piedra de la ciudad: (x, fila, pisos, semilla)
PIEDRAS = [(-320, 1, 1, 21), (-230, 0, 2, 22), (-150, 2, 1, 23), (-70, 1, 2, 24), (10, 0, 1, 25), (90, 2, 2, 26),
           (170, 1, 1, 27), (250, 0, 2, 28), (330, 2, 1, 29), (-380, 2, 2, 30), (30, 2, 1, 31), (-110, 0, 1, 32)]


def casas_ciudad(lz, t):
    """Transición aldea -> ciudad: las chozas se encogen y aparecen casas de piedra."""
    t0 = A["aldea"] - 0.3
    dur = 4.2
    for i, (x, tipo, fila, seed) in enumerate(CASAS):
        u = prog(t, t0 + dur * (i / len(CASAS)) * 0.8, t0 + dur * (i / len(CASAS)) * 0.8 + 0.5)
        if tipo in ("t", "c"):
            if u < 1:
                casa_en(lz, t, x, tipo, fila, seed, -1e9, escala=1.0 - u)   # se encoge
        else:
            casa_en(lz, t, x, tipo, fila, seed, -1e9, escala=1.0)
    for i, (x, fila, pisos, seed) in enumerate(PIEDRAS):
        k = prog(t, t0 + 0.3 + dur * (i / len(PIEDRAS)), t0 + 0.3 + dur * (i / len(PIEDRAS)) + 0.5)
        if k > 0:
            y = float(L.h(x)) + 30 + 42 * fila
            L.casa_piedra(lz, x, y, 1.5 * (1 + 0.1 * fila), k, seed, pisos=pisos)


def puesto(lz, x, y, s, k, seed, color=V.ROJO):
    kk = e_back(clamp01(k), 1.7) if k < 1 else 1
    if kk <= 0.01:
        return
    with lz.grupo(x, y, s, sy=s * kk):
        lz.relleno(rect_red(-54, -36, 108, 36, 3), L.MADERA, temblor=0.0, capa=1)
        lz.relleno(rect_red(-50, -70, 6, 34, 1), L.MADERA, temblor=0.0, capa=1)
        lz.relleno(rect_red(44, -70, 6, 34, 1), L.MADERA, temblor=0.0, capa=1)
        for i in range(6):
            lz.relleno(np.array([[-60 + i * 20, -110], [-40 + i * 20, -110], [-40 + i * 20, -70], [-60 + i * 20, -70]]),
                       color if i % 2 == 0 else V.CREMA, temblor=0.0, capa=1)
        for i in range(4):
            lz.relleno(V.elipse_pts(-30 + i * 20, -44, 9, 9), (V.AMARILLO, V.NARANJA, V.VERDE, V.ROJO)[i], temblor=0.0, capa=1)


def matadero(lz, x, y, s, k):
    kk = e_back(clamp01(k), 1.7) if k < 1 else 1
    if kk <= 0.01:
        return
    with lz.grupo(x, y, s, sy=s * kk):
        lz.relleno(rect_red(-70, -90, 140, 90, 3), (176, 150, 128), temblor=0.0, capa=1)
        lz.relleno(np.array([[-80, -90], [80, -90], [60, -122], [-60, -122]]), (110, 80, 66), temblor=0.0, capa=1)
        lz.relleno(rect_red(-22, -60, 44, 60, 4), (54, 40, 38), temblor=0.0, capa=1)


def dibujar(lz, t, tc, cam_l):
    casas_ciudad(lz, t)
    # convento franciscano
    kc = prog(t, A["francis"], A["francis"] + 0.6)
    L.iglesia(lz, 60, float(L.h(60)) + 30 + 120, 1.15, kc, 5)
    # fraile con cruz camina delante del convento
    if kc > 0.5:
        ff = V.cuadro(V.CAMINAR, t, 15.0)
        u = e_inout(prog(t, A["convento"], A["convento"] + 3.0))
        xf = lerp(-160, 20, u)
        V.figura(lz, xf, float(L.h(xf)) + 128, FIG * 1.1, V.CAMINAR[ff] if u < 1 else V.IDLE[int(t * 2.2) % 2], "fraile", 1,
                 obj=[("d", "cruz", 0, 0.9)], seed=140)
    # mercados y matadero
    for i, x in enumerate((-260, -170, 230)):
        puesto(lz, x, float(L.h(x)) + 160, 1.4, prog(t, A["mercados"] + 0.15 * i, A["mercados"] + 0.5 + 0.15 * i), i,
               (V.ROJO, V.TEAL, V.NARANJA)[i])
    matadero(lz, 330, float(L.h(330)) + 160, 1.4, prog(t, A["matadero"], A["matadero"] + 0.5))
    # gente en las calles
    if t > A["aldea"]:
        for i, (x, dr) in enumerate([(-210, 1), (140, -1), (-60, 1), (300, -1)]):
            xx = x + 60 * math.sin(t * 0.4 + i * 2)
            V.figura(lz, xx, float(L.h(xx)) + 175, FIG, V.CAMINAR[V.cuadro(V.CAMINAR, t, 15.0, 0.13 * i)],
                     ("indigena", "arriero", "africano", "mujer")[i], 1 if math.cos(t * 0.4 + i * 2) > 0 else -1, seed=150 + i)


def ui(lz, t):
    """Pergamino del título de ciudad y escudo de armas (espacio de pantalla)."""
    # pergamino: Felipe II, 1585
    a0, a1 = A["rey"] - 0.2, A["o88"] - 0.3
    if a0 <= t < a1 + 0.5:
        k = e_back(prog(t, a0, a0 + 0.45), 1.5) * (1 - smooth(prog(t, a1, a1 + 0.4)))
        if k > 0.01:
            cx, cy = W / 2, 760
            with lz.capa(2):
                with lz.grupo(cx, cy, k):
                    U.tarjeta(lz, 0, 0, 780, 560, 1.0, 0.0, (244, 228, 190), capa=2)
                    lz.relleno(rect_red(-390, -300, 780, 40, 20), (206, 168, 110), temblor=0.0, capa=2)
                    lz.relleno(rect_red(-390, 260, 780, 40, 20), (206, 168, 110), temblor=0.0, capa=2)
                    lz.texto("TÍTULO DE", 0, -130, 66, "vox_x", color=V.TINTA, borde=None, temblor=0.0)
                    lz.texto("CIUDAD", 0, -40, 150, "vox_x", color=V.ROJO, borde=None, temblor=0.0)
                    lz.texto("FELIPE II · 1585", 0, 90, 52, "vox_serif", color=V.TINTA, borde=None, temblor=0.0)
                    ks = e_back(prog(t, A["titulo"] + 0.2, A["titulo"] + 0.6), 2.2)
                    if ks > 0:
                        with lz.grupo(220, 190, ks, -0.2):
                            lz.relleno(V.elipse_pts(0, 0, 58, 58), (176, 44, 52), temblor=0.0, capa=2)
                            lz.relleno(V.elipse_pts(0, 0, 40, 40), (200, 64, 66), temblor=0.0, capa=2)
                            pts_ = []
                            for i_ in range(10):
                                a_ = -math.pi / 2 + i_ * math.pi / 5
                                r_ = 30 if i_ % 2 == 0 else 13
                                pts_.append((r_ * math.cos(a_), r_ * math.sin(a_)))
                            lz.relleno(np.array(pts_), (250, 214, 120), temblor=0.0, capa=2)
    # escudo (1588)
    e0, e1 = A["escudo"] - 0.3, A["entonces"] - 0.2
    if e0 <= t < e1 + 0.5:
        k = prog(t, e0, e0 + 0.5) * (1 - smooth(prog(t, e1, e1 + 0.4)))
        if k > 0.01:
            S.escudo(lz, W / 2, 780, 2.0 * k, min(1.0, k * 2), capa=2)
            V.pastilla(lz, W / 2, 400, "1588", 70, k=k, fondo=V.AMARILLO)
