# -*- coding: utf-8 -*-
"""Mundos 2D de la escena 5 (la llegada de los españoles): fila de cautivos encadenados (sin mostrar violencia), el reparto de los pueblos
y el diagrama de la encomienda."""
import math

import numpy as np

import plano as P
import kz_pers2d as K2
import kz_abstracto as AB
import kz_mapa_dib as MD
from motor import circulo, elipse, rect_red, catmull, h01, prog, smooth, e_out, e_back, e_inout, W, H


def fila_encadenada(lz, t, t0, y=900, n=7, s=34, x_ini=-300, vel=95.0, alfa=1.0):
    """Cautivos de cuerpo entero (sin cara, paleta fría) que avanzan atados con una cadena que cuelga entre ellos. Posición = f(t)."""
    if t < t0:
        return
    u = t - t0
    base = x_ini + vel * u
    xs = [base + 150 * i for i in range(n)]
    yc = y - 5.0 * s                                   # altura de los hombros
    for i, x in enumerate(xs):
        if x < -200 or x > W + 200:
            continue
        spec = K2.variar("caxcana" if i % 3 == 1 else "caxcan", 40 + i)
        spec = dict(spec, ropa=(120, 112, 150), ropa2=(150, 140, 170), pelo=(40, 30, 50), tocado=None)
        K2.cuerpo(lz, x, y, s, spec, t, piernas="camina", brazos="carga", mirar=1, vista="perfil", seed=i + 8, cara="ninguna", alfa=alfa, ph=t * 5.2 + i * 0.7)
    # cadena: eslabones sobre una catenaria entre cada par de cuellos
    for i in range(len(xs) - 1):
        x0, x1 = xs[i] + 0.4 * s, xs[i + 1] - 0.4 * s
        if x1 < -50 or x0 > W + 50:
            continue
        for k in range(10):
            f = k / 9
            xx = x0 + (x1 - x0) * f
            yy = yc + 1.2 * s + 26 * math.sin(math.pi * f) + 3 * math.sin(t * 4 + i + k)
            lz.relleno(elipse(xx, yy, 7, 4.5, 0.3 * (1 if k % 2 else -1), 10), (170, 172, 190), alfa=alfa, capa=2)


def diagrama_encomienda(lz, t, t_corona, t_pueblos, t_enc, t_gente, t_pagara, t_trib, t_trab, alfa=1.0):
    """Flujos de la encomienda: la Corona entrega pueblos al encomendero; la gente paga tributo y trabaja para él."""
    cx = 960
    # Corona arriba
    kc = min(1.0, max(0.0, (t - t_corona) * 3.0))
    if kc > 0.01:
        lz.halo(cx, 190, 260 * kc, (255, 220, 120), alfa=0.4, capa=1)
        MD.corona(lz, cx, 210, 5.0 * kc, 1.0, t)
    # pergamino «pueblos» que baja de la Corona y se posa al lado del encomendero (nunca sobre su cara)
    f = prog(t, t_pueblos, t_pueblos + 1.6)
    if f > 0.001:
        u = e_inout(f)
        xx, yy = cx + 330 * u, 300 + (560 - 300) * u
        lz.relleno(rect_red(xx - 150 + 8, yy - 60 + 10, 300, 120, 16), (14, 6, 40), alfa=0.3, capa=2)
        lz.relleno(rect_red(xx - 150, yy - 60, 300, 120, 16), (252, 240, 208), capa=2)
        lz.relleno(rect_red(xx - 150, yy - 60, 300, 26, 16), (222, 60, 70), capa=2)
        P.rotulo(lz, xx, yy + 8, "PUEBLOS", px=48, color=(110, 70, 50), alfa=1.0, sombra=0.0)
        P.discontinua(lz, [(cx + 60, 290), (xx - 40 * u, yy - 70)], (255, 255, 255), ancho=5.0, largo=16.0, hueco=12.0, fase=-t * 30, capa=2)
    # encomendero
    ke = min(1.0, max(0.0, (t - t_enc) * 3.0))
    if ke > 0.01:
        K2.busto(lz, cx, 760, 105 * ke, "encomendero", t, yaw=0.0, emocion="serio", ojos="abiertos", seed=3)
    # pueblo y gente abajo
    kg = min(1.0, max(0.0, (t - t_gente) * 3.0))
    if kg > 0.01:
        lz.relleno(rect_red(cx - 520, 905, 1040, 14, 7), (255, 255, 255), alfa=0.35 * kg, capa=1)
        for i, x in enumerate((cx - 340, cx - 170, cx, cx + 170, cx + 340)):
            tipo = ("caxcana", "caxcan", "caxcana", "caxcan", "caxcana")[i]
            K2.cuerpo(lz, x, 1040, 30 * kg, tipo, t, piernas="idle", brazos="idle", mirar=1 if i < 3 else -1, vista="frente", seed=i + 3, cara="minima", sombra=False)
    # flujos de tributo y trabajo hacia el encomendero
    if t > t_pagara:
        a = min(1.0, (t - t_pagara) * 2.0)
        AB.corriente(lz, t, [(cx - 300, 900), (cx - 330, 700), (cx - 120, 600)], n=18, ancho=18.0, vel=0.20, color=((255, 214, 80), (250, 190, 40)), r=(8.0, 13.0), seed=21, capa=2, alfa=a)
        AB.corriente(lz, t, [(cx + 300, 900), (cx + 330, 700), (cx + 120, 600)], n=18, ancho=18.0, vel=0.18, color=((170, 120, 80), (214, 160, 110)), r=(8.0, 13.0), seed=22, capa=2, alfa=a)
    return kc, ke, kg


def reparto(lz, t, t0, t_cortes, t_sale, alfa=1.0):
    """«Después vino el reparto»: tablero con los pueblos del cañón (casitas, milpas, magueyes) que unas líneas de corte dividen en lotes;
    cada lote recibe el sombrero de un encomendero. Se encoge y se va en t_sale."""
    k = e_back(prog(t, t0, t0 + 0.5)) * (1 - smooth(prog(t, t_sale, t_sale + 0.35)))
    if k <= 0.01:
        return
    cx, cy = 960, 610
    w, h = 1180 * k, 620 * k
    lz.relleno(rect_red(cx - w / 2 + 14, cy - h / 2 + 18, w, h, 30 * k), (14, 6, 40), alfa=0.35 * alfa, capa=1)
    lz.relleno(rect_red(cx - w / 2, cy - h / 2, w, h, 30 * k), (120, 170, 96), alfa=alfa, capa=1)
    lz.relleno(rect_red(cx - w / 2, cy - h / 2, w, h * 0.12, 30 * k), (150, 196, 110), alfa=alfa, capa=1)

    def rio_x(y):
        return cx - 60 * k + 90 * math.sin(((y - cy + h / 2) / h) * 3.0) * k

    q = np.array([(rio_x(cy - h / 2 + h * v), cy - h / 2 + h * v) for v in np.linspace(0, 1, 16)])
    lz.trazo(q, (90, 160, 230), 34 * k, afinar=False, temblor=0.0, capa=1)
    lz.trazo(q, (150, 210, 250), 10 * k, afinar=False, temblor=0.0, capa=1)
    # pueblos (4 x 3) con milpa y maguey, apartados del río
    for i in range(4):
        for j in range(3):
            x = cx + (-0.36 + 0.24 * i) * w + 18 * k * (h01(3, i, j) - 0.5)
            y = cy + (-0.27 + 0.27 * j) * h + 14 * k * (h01(4, i, j) - 0.5)
            if abs(x - rio_x(y)) < 130 * k:
                x = rio_x(y) + (150 * k if x >= rio_x(y) else -120 * k)
            ki = 1.8 * k
            for m in range(3):
                lz.relleno(rect_red(x - 70 * ki + m * 18 * ki, y + 22 * ki, 10 * ki, 30 * ki, 4 * ki), (230, 200, 90), alfa=alfa * 0.9, capa=1)
            lz.relleno(rect_red(x - 20 * ki, y - 18 * ki, 40 * ki, 30 * ki, 3 * ki), (236, 214, 176), alfa=alfa, capa=1)
            lz.relleno(np.array([(x - 26 * ki, y - 16 * ki), (x, y - 40 * ki), (x + 26 * ki, y - 16 * ki)]), (196, 150, 80), alfa=alfa, capa=1)
            lz.relleno(rect_red(x - 5 * ki, y - 2 * ki, 10 * ki, 14 * ki, 2 * ki), (90, 60, 50), alfa=alfa, capa=1)
            for a in range(5):
                ang = -1.2 + 0.6 * a
                lz.relleno(np.array([(x + 40 * ki, y + 12 * ki), (x + 40 * ki + math.sin(ang) * 22 * ki, y + 12 * ki - math.cos(ang) * 22 * ki), (x + 44 * ki, y + 12 * ki)]),
                           (70, 150, 120), alfa=alfa, capa=1)
    # líneas de corte que dividen el tablero en 4 lotes
    cortes = [((cx - w * 0.02, cy - h / 2), (cx + w * 0.04, cy + h / 2)), ((cx - w / 2, cy + h * 0.02), (cx + w / 2, cy - h * 0.04))]
    for n_, (p0, p1) in enumerate(cortes):
        f = e_inout(prog(t, t_cortes + 0.35 * n_, t_cortes + 0.35 * n_ + 0.5))
        if f > 0.01:
            pe = (p0[0] + (p1[0] - p0[0]) * f, p0[1] + (p1[1] - p0[1]) * f)
            P.discontinua(lz, [p0, pe], (255, 255, 255), ancho=7.0 * k, largo=22.0 * k, hueco=14.0 * k, fase=-t * 40, capa=2)
            lz.relleno(circulo(pe[0], pe[1], 9 * k, 12), (255, 255, 255), alfa=alfa, capa=2)
    # cada lote recibe el sombrero de un encomendero (con su color)
    for n_, (sx, sy, col) in enumerate(((-0.26, -0.24, (222, 60, 70)), (0.26, -0.26, (240, 170, 50)), (-0.24, 0.24, (122, 52, 200)), (0.27, 0.22, (40, 110, 230)))):
        kk = e_back(prog(t, t_cortes + 0.9 + 0.18 * n_, t_cortes + 1.3 + 0.18 * n_))
        if kk > 0.01:
            x, y = cx + sx * w, cy + sy * h
            lz.relleno(circulo(x, y, 62 * kk * k, 28), col, alfa=0.45 * alfa, capa=2)
            lz.relleno(elipse(x, y + 14 * kk * k, 58 * kk * k, 14 * kk * k, 0, 24), (50, 40, 60), alfa=alfa, capa=2)
            lz.relleno(rect_red(x - 28 * kk * k, y - 26 * kk * k, 56 * kk * k, 40 * kk * k, 12 * kk * k), (60, 48, 70), alfa=alfa, capa=2)
            lz.relleno(rect_red(x - 28 * kk * k, y + 2 * kk * k, 56 * kk * k, 8 * kk * k, 0), col, alfa=alfa, capa=2)
