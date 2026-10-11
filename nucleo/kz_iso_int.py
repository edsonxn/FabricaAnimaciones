# -*- coding: utf-8 -*-
"""Utilería de INTERIORES para habitaciones en corte (kz_iso.habitacion): cortinas, ventanas con vista, escudos heráldicos, araña de cristal, chimenea con fuego, reloj de péndulo,
mapa antiguo, espejo, plantas, sillones, paja y cadenas de calabozo. Las cosas de pared se pegan a una cara de la habitación ('yi' = pared de fondo izquierda, 'xi' = fondo derecha);
las de suelo/aire usan coordenadas de mundo."""
import math

import numpy as np

import kz_iso as I
from kz_iso import tint, caja, cara_rect, cara_arco, Caja, sombra_elipse, sombra_suelo
import kz_iso_obj as O
import plano as P
from motor import circulo, elipse, rect_red, h01, catmull


def cortina(lz, iso, c, cara, a0, a1, b0, b1, color=(190, 52, 66), t=0.0, galon=(250, 206, 90)):
    """Cortina recogida (pliegues alternos claro/oscuro), con cenefa dorada arriba y un cordón; ondula apenas con el aire."""
    n = 6
    w = (a1 - a0) / n
    for i in range(n):
        col = P.aclarar(color, 0.14) if i % 2 == 0 else P.oscurecer(color, 0.16)
        sw = 0.7 * math.sin(t * 1.2 + i * 0.8)
        cara_rect(lz, iso, c, cara, a0 + i * w + sw * 0.3, a0 + (i + 1) * w + sw * 0.3, b0 + abs(sw), b1, col)
    cara_rect(lz, iso, c, cara, a0 - 1, a1 + 1, b1 - 6, b1, galon)
    for i in range(0, n, 2):
        cara_rect(lz, iso, c, cara, a0 + i * w + w * 0.4, a0 + i * w + w * 0.6, b1 - 8, b1 - 6, P.oscurecer(galon, 0.2))
    cara_rect(lz, iso, c, cara, (a0 + a1) / 2 - 1, (a0 + a1) / 2 + 1, (b0 + b1) / 2 - 6, (b0 + b1) / 2 + 6, galon)


def ventana_vista(lz, iso, c, cara, a0, a1, b0, b1, t=0.0, cielo=(140, 196, 248), marco=(250, 244, 230), cortinas=(190, 52, 66), vista="cielo"):
    """Ventanal con marco, travesaños, cielo con nubes y (opcional) siluetas lejanas; cortinas a los lados."""
    cara_rect(lz, iso, c, cara, a0 - 3, a1 + 3, b0 - 3, b1 + 3, marco)
    cara_arco(lz, iso, c, cara, a0, a1, b0, b1 - 2, cielo)
    # nubes que pasan
    for k in range(2):
        u = ((t * 0.04 + k * 0.5) % 1.0)
        xa = a0 + (a1 - a0) * (u * 1.4 - 0.2)
        if a0 < xa < a1 - 6:
            cara_rect(lz, iso, c, cara, xa, min(a1, xa + 10), b0 + (b1 - b0) * (0.55 + 0.2 * k), b0 + (b1 - b0) * (0.55 + 0.2 * k) + 4, (255, 255, 255))
    if vista == "ciudad":
        for k in range(5):
            xa = a0 + (a1 - a0) * (0.1 + 0.18 * k)
            cara_rect(lz, iso, c, cara, xa, xa + (a1 - a0) * 0.12, b0, b0 + (b1 - b0) * (0.25 + 0.2 * h01(k, 3)), P.oscurecer(cielo, 0.35))
    for fx in (0.5,):
        cara_rect(lz, iso, c, cara, a0 + (a1 - a0) * fx - 1, a0 + (a1 - a0) * fx + 1, b0, b1 - 2, marco)
    cara_rect(lz, iso, c, cara, a0, a1, (b0 + b1) / 2 - 1, (b0 + b1) / 2 + 1, marco)
    if cortinas:
        w = (a1 - a0) * 0.28
        cortina(lz, iso, c, cara, a0 - 7, a0 + w, b0 - 4, b1 + 8, cortinas, t)
        cortina(lz, iso, c, cara, a1 - w, a1 + 7, b0 - 4, b1 + 8, cortinas, t + 1.3)


def escudo(lz, iso, c, cara, a, b, s=1.0, tipo="francia"):
    """Escudo heráldico sobre la pared: 'francia' (águila imperial dorada sobre azul), 'espana' (castillos y leones), 'mexico' (águila y nopal), 'iglesia' (llaves y cruz)."""
    w, h = 22 * s, 28 * s
    cara_rect(lz, iso, c, cara, a - w / 2 - 2, a + w / 2 + 2, b - 2, b + h + 2, (250, 206, 90))
    base = {"francia": (40, 70, 170), "espana": (214, 52, 66), "mexico": (250, 244, 224), "iglesia": (250, 244, 224)}[tipo]
    cara_rect(lz, iso, c, cara, a - w / 2, a + w / 2, b, b + h, base)
    dor = (250, 206, 90)
    if tipo == "francia":
        cara_rect(lz, iso, c, cara, a - 4 * s, a + 4 * s, b + 8 * s, b + 22 * s, dor)
        cara_rect(lz, iso, c, cara, a - 9 * s, a + 9 * s, b + 14 * s, b + 18 * s, dor)
    elif tipo == "espana":
        cara_rect(lz, iso, c, cara, a - w / 2, a, b + h / 2, b + h, (250, 214, 90))
        cara_rect(lz, iso, c, cara, a, a + w / 2, b, b + h / 2, (250, 214, 90))
    elif tipo == "mexico":
        cara_rect(lz, iso, c, cara, a - 6 * s, a + 6 * s, b + 4 * s, b + 10 * s, (60, 150, 96))
        cara_rect(lz, iso, c, cara, a - 3 * s, a + 3 * s, b + 10 * s, b + 22 * s, (130, 84, 52))
    else:
        cara_rect(lz, iso, c, cara, a - 2 * s, a + 2 * s, b + 4 * s, b + 24 * s, (206, 56, 66))
        cara_rect(lz, iso, c, cara, a - 7 * s, a + 7 * s, b + 14 * s, b + 18 * s, (206, 56, 66))


def mapa_pared(lz, iso, c, cara, a, b, w=60, h=44, t=0.0):
    """Mapa antiguo enmarcado con costas y una ruta punteada que se mueve."""
    cara_rect(lz, iso, c, cara, a - 3, a + w + 3, b - 3, b + h + 3, (130, 90, 66))
    cara_rect(lz, iso, c, cara, a, a + w, b, b + h, (246, 230, 190))
    cara_rect(lz, iso, c, cara, a + w * 0.08, a + w * 0.45, b + h * 0.15, b + h * 0.85, (96, 160, 200))
    cara_rect(lz, iso, c, cara, a + w * 0.45, a + w * 0.92, b + h * 0.1, b + h * 0.7, (214, 180, 120))
    cara_rect(lz, iso, c, cara, a + w * 0.55, a + w * 0.8, b + h * 0.3, b + h * 0.5, (150, 130, 90))
    for k in range(5):
        u = ((t * 0.3 + k * 0.2) % 1.0)
        cara_rect(lz, iso, c, cara, a + w * (0.15 + 0.7 * u), a + w * (0.15 + 0.7 * u) + 2.4, b + h * (0.3 + 0.2 * math.sin(u * 6)) , b + h * (0.3 + 0.2 * math.sin(u * 6)) + 2.4, (206, 56, 66))


def espejo(lz, iso, c, cara, a, b, w=26, h=44):
    cara_arco(lz, iso, c, cara, a - 3, a + w + 3, b - 3, b + h + 3, (250, 206, 90))
    cara_arco(lz, iso, c, cara, a, a + w, b, b + h, (190, 226, 244))
    cara_rect(lz, iso, c, cara, a + 4, a + 8, b + 6, b + h * 0.7, (240, 250, 255))


def araña(lz, iso, x, y, z, t=0.0, velas=6, s=1.0):
    """Araña de cristal colgante: aro dorado, velas encendidas con halos y gotas de cristal que brillan."""
    sx, sy = iso.P(x, y, z)
    k = iso.z * s
    lz.relleno(rect_red(sx - 0.8 * k, sy - 40 * k, 1.6 * k, 40 * k, 0.4 * k), tint((130, 120, 110)), capa=2)
    lz.relleno(elipse(sx, sy, 22 * k, 6 * k, 0, 18), tint((250, 206, 90)), capa=2)
    lz.relleno(elipse(sx, sy + 1.4 * k, 18 * k, 4 * k, 0, 18), tint((226, 160, 40)), capa=2)
    for i in range(velas):
        a = i * 2 * math.pi / velas
        vx = sx + math.cos(a) * 18 * k
        vy = sy - 4 * k + math.sin(a) * 4.6 * k
        lz.relleno(rect_red(vx - 1.3 * k, vy - 8 * k, 2.6 * k, 8 * k, 0.5 * k), tint((250, 244, 224)), capa=2)
        f = 0.5 + 0.5 * math.sin(t * 14 + i * 1.7)
        lz.halo(vx, vy - 12 * k, 14 * k, (255, 214, 130), alfa=0.42 + 0.12 * f, capa=2)
        lz.relleno(np.array([[vx - 1.5 * k, vy - 8 * k], [vx, vy - 14 * k - 2 * f * k], [vx + 1.5 * k, vy - 8 * k]]), (255, 214, 90), capa=2)
        lz.relleno(circulo(vx, vy + 5 * k, 1.2 * k, 6), (220, 244, 255), capa=2)
    for i in range(5):
        lz.relleno(np.array([[sx + (i - 2) * 6 * k, sy + 3 * k], [sx + (i - 2) * 6 * k - 1.4 * k, sy + 9 * k], [sx + (i - 2) * 6 * k + 1.4 * k, sy + 9 * k]]), (220, 244, 255), alfa=0.9, capa=2)
    lz.halo(sx, sy + 20 * k, 90 * k, (255, 224, 150), alfa=0.18, capa=2)


def chimenea(lz, iso, c, cara, a, t=0.0, w=44, h=38, color=(206, 196, 182)):
    """Chimenea de mármol en la pared con fuego animado, repisa y un reloj encima."""
    cara_rect(lz, iso, c, cara, a - 4, a + w + 4, 0, h + 8, color)
    cara_rect(lz, iso, c, cara, a - 8, a + w + 8, h + 8, h + 14, P.aclarar(color, 0.2))
    cara_rect(lz, iso, c, cara, a + 4, a + w - 4, 0, h - 6, (40, 28, 36))
    p0 = c.punto(cara, a + w / 2, 4)
    O.fuego(lz, iso, p0[0], p0[1] - (0.0 if cara == "xi" else 0.0) + (0 if cara == "yi" else 0), 1.0, t, seed=int(a), z=p0[2], halo=True)


def reloj_pie(lz, iso, x, y, t=0.0, s=1.0):
    """Reloj de péndulo de caja alta con péndulo que oscila."""
    caja(lz, iso, x - 6 * s, y - 5 * s, 12 * s, 10 * s, 52 * s, (130, 84, 60))
    caja(lz, iso, x - 7 * s, y - 6 * s, 14 * s, 12 * s, 4 * s, (150, 100, 70), z0=52 * s)
    sx, sy = iso.P(x, y + 5 * s, 44 * s)
    k = iso.z * s
    lz.relleno(circulo(sx, sy, 5 * k, 14), tint((250, 244, 224)))
    lz.relleno(rect_red(sx - 0.5 * k, sy - 4 * k, 1.0 * k, 4 * k, 0.3 * k), (60, 40, 40))
    ang = math.radians(t * 6)
    lz.relleno(rect_red(sx - 0.4 * k + math.sin(ang) * 2 * k, sy - 0.4 * k, 3 * k, 0.8 * k, 0.3 * k), (60, 40, 40))
    pa = 0.35 * math.sin(t * 2.4)
    px_, py_ = sx + math.sin(pa) * 16 * k, sy + 14 * k + (1 - math.cos(pa)) * 4 * k
    lz.trazo(np.array([[sx, sy + 8 * k], [px_, py_]]), (206, 160, 60), 1.6 * k, afinar=False, temblor=0.0)
    lz.relleno(circulo(px_, py_, 3.4 * k, 10), tint((250, 206, 90)))


def maceta(lz, iso, x, y, s=1.0, t=0.0, tipo="helecho"):
    sx, sy = iso.P(x, y, 0)
    k = iso.z * s
    sombra_elipse(lz, iso, x + 2, y + 1, 7 * s, 4 * s, 0.2)
    lz.relleno(np.array([[sx - 6 * k, sy - 10 * k], [sx + 6 * k, sy - 10 * k], [sx + 4.4 * k, sy], [sx - 4.4 * k, sy]]), tint((190, 96, 76)))
    lz.relleno(np.array([[sx - 6 * k, sy - 10 * k], [sx - 1 * k, sy - 10 * k], [sx - 1 * k, sy], [sx - 4.4 * k, sy]]), tint((222, 130, 100)))
    for i in range(7):
        a = -1.2 + i * 0.4
        sw = math.sin(t * 1.6 + i) * 1.4 * k
        ex, ey = sx + math.sin(a) * 18 * k + sw, sy - 10 * k - math.cos(a) * 20 * k
        lz.relleno(np.array([[sx - 1.4 * k, sy - 9 * k], [sx + 1.4 * k, sy - 9 * k], [ex, ey]]), tint((70, 160, 96) if i % 2 else (96, 184, 100)))


def sillon(lz, iso, x, y, w=24, d=20, color=(190, 52, 66), orient="y"):
    """Sillón noble acolchado con respaldo, brazos y patas."""
    caja(lz, iso, x, y, w, d, 7, P.oscurecer(color, 0.2), z0=4)
    caja(lz, iso, x + 2, y + 2, w - 4, d - 4, 3, color, z0=11)
    caja(lz, iso, x, y, w, 5, 22, color, z0=4)
    caja(lz, iso, x, y, 4, d, 12, P.oscurecer(color, 0.1), z0=4)
    caja(lz, iso, x + w - 4, y, 4, d, 12, P.oscurecer(color, 0.1), z0=4)
    for (px, py) in ((x + 1, y + 1), (x + w - 3, y + 1), (x + 1, y + d - 3), (x + w - 3, y + d - 3)):
        caja(lz, iso, px, py, 2, 2, 4, (250, 206, 90))


def paja(lz, iso, x0, y0, x1, y1, n=70, seed=3, color=(226, 196, 110)):
    """Paja esparcida en el suelo (celdas)."""
    k = iso.z
    for i in range(n):
        x = x0 + (x1 - x0) * h01(seed, i, 1)
        y = y0 + (y1 - y0) * h01(seed, i, 2)
        a = h01(seed, i, 3) * 3.14
        sx, sy = iso.P(x, y, 0.2)
        L = (4 + 5 * h01(seed, i, 4)) * k
        lz.relleno(np.array([[sx - math.cos(a) * L, sy - math.sin(a) * L * 0.5 - 0.6 * k], [sx + math.cos(a) * L, sy + math.sin(a) * L * 0.5 - 0.6 * k], [sx + math.cos(a) * L, sy + math.sin(a) * L * 0.5 + 0.6 * k],
                             [sx - math.cos(a) * L, sy - math.sin(a) * L * 0.5 + 0.6 * k]]), tint(color if h01(seed, i, 5) > 0.4 else P.oscurecer(color, 0.2)))


def cadenas(lz, iso, c, cara, a, b, n=5, t=0.0, color=(150, 150, 170)):
    """Cadena colgando de una argolla en la pared (calabozo)."""
    p = c.punto(cara, a, b)
    sx, sy = iso.P(*p)
    k = iso.z
    lz.relleno(circulo(sx, sy, 3 * k, 10), tint((120, 120, 140)))
    for i in range(n):
        cx_ = sx + math.sin(t * 1.2 + i * 0.5) * 0.8 * k
        cy_ = sy + (5 + i * 6) * k
        lz.trazo(np.stack([cx_ + 2.2 * k * np.cos(np.linspace(0, 6.28, 12)), cy_ + 3.2 * k * np.sin(np.linspace(0, 6.28, 12))], 1), color, 1.6 * k, cerrado=True, afinar=False, temblor=0.0)


def jarra_pan(lz, iso, x, y, s=1.0):
    sx, sy = iso.P(x, y, 0)
    k = iso.z * s
    sombra_elipse(lz, iso, x + 2, y + 1, 6 * s, 3 * s, 0.2)
    lz.relleno(rect_red(sx - 4 * k, sy - 9 * k, 8 * k, 9 * k, 2 * k), tint((176, 120, 86)))
    lz.relleno(rect_red(sx - 4 * k, sy - 9 * k, 3 * k, 9 * k, 1.4 * k), tint((210, 156, 114)))
    lz.relleno(elipse(sx + 8 * k, sy - 1.5 * k, 5 * k, 2 * k, 0, 10), tint((226, 180, 110)))


def baul(lz, iso, x, y, w=22, d=14, h=12, color=(150, 98, 66)):
    c = caja(lz, iso, x, y, w, d, h, color)
    cara_rect(lz, iso, c, "y", 0, w, 4, 6, (250, 206, 90))
    cara_rect(lz, iso, c, "x", 0, d, 4, 6, (250, 206, 90))
    cara_rect(lz, iso, c, "y", w / 2 - 2, w / 2 + 2, 3, 8, (250, 206, 90))
    return c


def cuadro_retrato(lz, iso, c, cara, a, b, w=22, h=28, marco=(250, 206, 90), fondo=(70, 90, 130), pelo=(240, 238, 244)):
    """Cuadro con un retrato esquemático de época (cabeza, peluca y casaca)."""
    cara_rect(lz, iso, c, cara, a - 2.5, a + w + 2.5, b - 2.5, b + h + 2.5, marco)
    cara_rect(lz, iso, c, cara, a, a + w, b, b + h, fondo)
    cara_arco(lz, iso, c, cara, a + w * 0.28, a + w * 0.72, b + h * 0.38, b + h * 0.74, (240, 196, 160))
    cara_arco(lz, iso, c, cara, a + w * 0.22, a + w * 0.78, b + h * 0.56, b + h * 0.86, pelo) if False else cara_rect(lz, iso, c, cara, a + w * 0.22, a + w * 0.78, b + h * 0.64, b + h * 0.82, pelo)
    cara_rect(lz, iso, c, cara, a + w * 0.12, a + w * 0.88, b, b + h * 0.36, (180, 52, 66))
