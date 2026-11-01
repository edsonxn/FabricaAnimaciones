# -*- coding: utf-8 -*-
"""Mundos de la escena 5 (la paz y los papeles): el amanecer de la paz (2D), la mesa de los frailes, las tierras en disputa (isométrico, la cerca
que retrocede ante la cédula de 1597), el archivo del primer alcalde (interior en corte) y el duelo flechas contra papeles."""
import math

import numpy as np

import kz_iso as I
import kz_iso_obj as O
import kz_iso_obj2 as O2
import kz_iso_arq as A
import kz_iso_arq2 as B
import kz_iso_deco as DC
import kz_iso_int as II
import kz_gente_iso as G
import kz_pers2d as K2
import kz_ui as U
import plano as P
from motor import circulo, elipse, rect_red, catmull, h01, prog, smooth, e_out, e_back, e_inout, W, H
import mundos_2 as M2
import paisajes as PA


# ------------------------------------------------------------------------------------------------ 2D: el amanecer de la paz
def paz_amanecer(lz, t, t0):
    """Valle al amanecer: gente que baja por la ladera con mantas blancas en alto y palomas que suben. Todo es función de t."""
    PA.sol(lz, 1380, 420, 90, t, 0.0)
    U.haces_luz(lz, 1380, 420, t, n=11, largo=1500, color=(255, 232, 180), alfa=0.12)
    PA.sierras(lz, t, 10 * (t - t0), 0.0, y0=640, capas=5, semilla=121)
    p = PA.pal(0.0)
    lz.relleno(np.array([(-40, 760), (500, 700), (1000, 780), (1500, 720), (1960, 790), (1960, H + 20), (-40, H + 20)]), p["pasto"][0], capa=0)
    lz.relleno(np.array([(-40, 900), (700, 850), (1300, 910), (1960, 860), (1960, H + 20), (-40, H + 20)]), p["pasto"][1], capa=0)
    zig = [(120, 700), (560, 780), (300, 860), (820, 930), (560, 1010), (1200, 1040), (1700, 1090)]
    q = np.array(catmull(np.array(zig, float), 12, False))
    lz.trazo(q, (232, 214, 172), 64.0, afinar=False, temblor=0.0, capa=1)
    seg = np.hypot(*np.diff(q, axis=0).T)
    d = np.r_[0, np.cumsum(seg)]
    for i in range(18):
        f = (i / 18 + 0.02 * (t - t0)) % 1.0
        s_ = d[-1] * f
        j = int(np.clip(np.searchsorted(d, s_) - 1, 0, len(q) - 2))
        v = (s_ - d[j]) / max(1e-6, d[j + 1] - d[j])
        px, py = q[j] + (q[j + 1] - q[j]) * v
        sc = 12 + 20 * max(0.0, (py - 700) / 400.0)
        dirx = 1 if q[j + 1][0] >= q[j][0] else -1
        spec = K2.variar("caxcana" if i % 3 == 1 else "caxcan", 2300 + i)
        K2.cuerpo(lz, px, py + 6, sc, spec, t, piernas="camina", brazos="arriba" if i % 4 == 0 else "balanceo", mirar=dirx, vista="perfil", seed=2300 + i, sombra=False, ph=t * 4.5 + i)
        if i % 3 == 0:                                                       # bandera blanca en asta: la lleva a su lado
            ax = px + dirx * 1.15 * sc
            lz.relleno(rect_red(ax - 0.12 * sc, py - 13.6 * sc, 0.24 * sc, 13.4 * sc, 0), (120, 84, 60), capa=2)
            ond = [(ax + dirx * (0.12 * sc + 3.4 * sc * u), py - 13.4 * sc + 0.35 * sc * math.sin(t * 5 + u * 4 + i)) for u in np.linspace(0, 1, 7)]
            lz.relleno(np.array(ond + [(p[0], p[1] + 3.2 * sc) for p in ond[::-1]]), (252, 250, 244), capa=2)
    # palomas
    for i in range(7):
        u = ((t - t0) * 0.12 + h01(7, i, 1)) % 1.0
        x = 200 + 1500 * h01(7, i, 2) + 120 * math.sin(u * 5)
        y = 560 - u * 420
        al = math.sin(t * 8 + i) * 9
        lz.relleno(np.array([[x - 18, y - al], [x, y + 3], [x + 18, y - al], [x, y - 3]]), (252, 250, 246), alfa=0.95 * (1 - u), capa=2)


# ------------------------------------------------------------------------------------------------ 2D: mesa de los frailes con el pergamino
def mesa_frailes(lz, t, t0, t_sello, t_conf):
    """Mesa de madera con dos frailes detrás y un pergamino que se despliega; el sello de lacre cae al «confirmaron»."""
    lz.relleno(np.array([(-40, 760), (W + 40, 740), (W + 40, H + 20), (-40, H + 20)]), (96, 64, 52), capa=0)
    lz.relleno(np.array([(-40, 760), (W + 40, 740), (W + 40, 790), (-40, 810)]), (150, 106, 80), capa=0)
    for i in range(8):                                                       # vetas de la madera
        lz.relleno(rect_red(100 + 240 * i, 840 + 24 * (i % 3), 160, 5, 2), (78, 50, 42), alfa=0.6, capa=0)
    # candeleros
    for x in (180, 1740):
        lz.relleno(rect_red(x - 12, 600, 24, 160, 8), (216, 184, 120), capa=1)
        lz.halo(x, 560, 130, (255, 214, 120), alfa=0.5, dureza=1.1, capa=1)
        fl = 1 + 0.1 * math.sin(t * 9 + x)
        lz.relleno(np.array([(x - 10, 600), (x + 10, 600), (x, 540 - 10 * fl)]), (255, 190, 70), capa=1)


# ------------------------------------------------------------------------------------------------ isométrico: tierras en disputa (1597)
class Tierras:
    """Mosaico de tierras con una cerca que cerca una parcela: al llegar la cédula la cerca retrocede (u 0..1) y el capitán se va."""
    def suelo(self, lz, iso, t):
        I.isla(lz, iso, -120, -120, 460, 400, color_top=(150, 190, 108), t=t, seed=131, esp=40)
        DC.campos(lz, iso, -100, -100, 440, 380, nx=4, ny=3, seed=14, t=t, setos=True, margen=6)
        I.camino(lz, iso, [(-100, 160), (120, 150), (260, 190), (440, 170)], 22, (232, 214, 170), borde=(208, 188, 144))

    def objetos(self, t, u=0.0, cedula=0.0, capitan=1.0, gente=1.0):
        m = I.Mundo()
        m.topo = False
        # cerca de la parcela en disputa: rectángulo que se encoge hacia (300, 120)
        x0 = lerp_(130, 300, u)
        y0 = lerp_(-60, 90, u)
        x1, y1 = 420, 340
        pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
        m.add(x0, y0, x1, y1, 24, (lambda pts: (lambda lz, iso: O.cerca(lz, iso, pts, h=18, color=(176, 124, 84), poste_cada=22)))(pts), fijo=False, clave=3)
        # la tierra recuperada: milpa dorada que aparece al retroceder
        if u > 0.01:
            m.add(130, -60, 300, 340, 8, (lambda a: (lambda lz, iso: I.suelo_rect(lz, iso, 130, -60, 170, 400, (236, 206, 120), z=0.3, alfa=0.5 * a)))(smooth(u)), fijo=False, clave=4)
        # árboles
        for i, (x, y) in enumerate(((20, -80), (250, -90), (-80, 120), (-60, 300), (150, 360), (400, 60))):
            m.add(x - 8, y - 8, x + 8, y + 8, 50, (lambda x, y, i: (lambda lz, iso: O.arbol(lz, iso, x, y, h=48, seed=i + 5, t=t)))(x, y, i), clave=x + y * 7)
        # el capitán se retira con sus hombres; el pueblo viene a ocupar la tierra
        if capitan > 0.01:
            for i in range(5):
                a = u * 1.0
                x = lerp_(300 + 18 * (i % 3), 520, a)
                y = lerp_(100 + 30 * i, 20 + 60 * i, a)
                tipo = "capitan_esp" if i == 0 else "conquistador"
                m.add(x - 5, y - 5, x + 5, y + 5, 52, (lambda x, y, tipo, i: (lambda lz, iso: G.persona(lz, iso, x, y, t, tipo=tipo, dir=(1.0, 0.2), vel=8.0 if u > 0.05 else 0.0, seed=800 + i, h=46,
                                                                                                accion="habla" if (i == 0 and u < 0.05) else None)))(x, y, tipo, i), fijo=False, clave=x + y * 7 + 2)
        mu = G.Multitud()
        for i in range(8):
            mu.camina([(-90, 130 + 6 * i), (100, 150 + 4 * i), (210 + 20 * (i % 3), 120 + 40 * (i % 4))], "caxcan" if i % 2 else "caxcana", vel=9 + i % 3, seed=3300 + i, h=46,
                      fase=0.12 * i, bucle=True)
        mu.dibujar(m, t)
        return m


def lerp_(a, b, u):
    return a + (b - a) * u


# ------------------------------------------------------------------------------------------------ isométrico: el archivo (interior en corte)
def archivo(lz, iso, t, legajos=1.0):
    """Sala del archivo: dos paredes con estantes llenos de legajos, mesa con vela, baúl, ventana con luz y cuadros."""
    c = I.habitacion(lz, iso, 0, 0, 300, 230, 130, piso=(150, 108, 84), pared_a=(240, 224, 190), pared_b=(226, 206, 168), friso=(140, 98, 74))
    II.ventana_vista(lz, iso, c, "yi", 150, 214, 38, 108, t=t)                              # ventanal con luz de la tarde
    II.mapa_pared(lz, iso, c, "xi", 90, 62, w=64, h=46, t=t)                                # mapa de las tierras del pueblo
    lz.relleno(iso.pts([(150, 0, 104), (214, 0, 104), (270, 120, 0), (200, 120, 0)]), (255, 230, 160), alfa=0.16)   # haz de luz de la ventana
    B.alfombra(lz, iso, 80, 90, 160, 100, color=(170, 56, 66), borde=(240, 200, 120))
    B.estante(lz, iso, 14, 14, 110, 14, 108)
    B.estante(lz, iso, 14, 40, 14, 130, 108)
    B.mesa(lz, iso, 150, 120, 90, 46, 28, color=(140, 96, 66))
    O2.pergamino(lz, iso, 170, 138, 28, w=18, h=22, rot=0.0, lineas=True, sello=(200, 50, 60), billboard=True)
    B.vela(lz, iso, 214, 130, 28, t=t, seed=2)
    B.silla(lz, iso, 118, 128, h=20, color=(120, 80, 60), dir="y")
    II.baul(lz, iso, 50, 186, w=40, d=24, h=24, color=(120, 84, 60))
    II.reloj_pie(lz, iso, 276, 28, t=t, s=1.0)
    II.maceta(lz, iso, 24, 206, s=1.0, t=t)
    # legajos apilados en el suelo
    for i in range(5):
        k = float(np.clip(legajos * 6 - i, 0, 1))
        if k > 0.01:
            I.caja(lz, iso, 240, 160 + 0, 40, 28, 7 * k, [(236, 224, 196), (214, 196, 160)][i % 2], z0=7 * i)
    return c


# ------------------------------------------------------------------------------------------------ 2D: flechas contra papeles
def flecha(lz, x, y, ang, L, color=(150, 112, 80), alfa=1.0, capa=1, g=1.0):
    ux, uy = math.cos(ang), math.sin(ang)
    x1, y1 = x + ux * L, y + uy * L
    lz.trazo(np.array([(x, y), (x1, y1)]), (*color, int(255 * alfa)), 8.0 * g, afinar=False, temblor=0.0, capa=capa)
    lz.relleno(np.array([(x1 + ux * 36 * g, y1 + uy * 36 * g), (x1 - uy * 15 * g, y1 + ux * 15 * g), (x1 + uy * 15 * g, y1 - ux * 15 * g)]), (210, 206, 214), alfa=alfa, capa=capa)
    for k in (-1, 1):
        lz.relleno(np.array([(x, y), (x - ux * 28 * g - uy * 15 * g * k, y - uy * 28 * g + ux * 15 * g * k), (x + ux * 20 * g, y + uy * 20 * g)]), (226, 70, 80), alfa=alfa, capa=capa)


def papel(lz, x, y, s, rot=0.0, sello=True, alfa=1.0, capa=2, lineas=4):
    """Hoja con renglones y sello de lacre (origen en el centro)."""
    c, sn = math.cos(rot), math.sin(rot)
    R = lambda px, py: (x + (px * c - py * sn) * s, y + (px * sn + py * c) * s)
    lz.relleno(np.array([R(-46, -60), R(46, -60), R(46, 60), R(-46, 60)]), (250, 244, 226), alfa=alfa, capa=capa)
    lz.relleno(np.array([R(46, -60), R(46, 60), R(40, 60), R(40, -54)]), (222, 206, 170), alfa=alfa, capa=capa)
    for i in range(lineas):
        w = 70 - 14 * (i % 2)
        lz.relleno(np.array([R(-34, -40 + 20 * i), R(-34 + w, -40 + 20 * i), R(-34 + w, -36 + 20 * i), R(-34, -36 + 20 * i)]), (120, 96, 80), alfa=0.8 * alfa, capa=capa)
    if sello:
        sx, sy = R(22, 42)
        lz.relleno(circulo(sx, sy, 13 * s, 14), (200, 50, 62), alfa=alfa, capa=capa)
        lz.relleno(circulo(sx - 3 * s, sy - 3 * s, 4 * s, 8), (240, 110, 120), alfa=alfa, capa=capa)
