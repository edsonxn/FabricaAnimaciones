# -*- coding: utf-8 -*-
"""Utilería vectorial propia de «¿Qué pasaría si la GRAVEDAD desapareciera 5 segundos?» (estilo Kurzgesagt: rellenos planos,
dos tonos de volumen, sombras azul-violeta, bordes de luz limpios, sin contornos negros):
  - nube, arbusto, farola, pino, aerogenerador
  - casa_corte (casa en corte transversal con sofá, librero, lámpara, alfombra y objetos que flotan en Segundo 0)
  - bicicleta (ruedas que siguen girando en el aire), taza_cafe (con gotas esféricas de café flotando), coche_urbano
  - burbuja_agua (bolas de agua de mar/charcos flotando en ingravidez), corriente_aire (estelas de viento y resorte)
  - malla_curva (tejido del espacio-tiempo curvado por la masa), interruptor_gigante
"""
import math

import numpy as np

import plano as P
from plano import mezcla, aclarar, oscurecer
from motor import circulo, elipse, rect_red, blob, h01, lerp, clamp01


def nube(lz, x, y, s=1.0, col=(255, 255, 255), alfa=1.0, seed=0):
    if alfa <= 0.01:
        return
    sombra = mezcla(col, (140, 156, 214), 0.28)
    with lz.grupo(x, y, s):
        lz.relleno(rect_red(-95, -14, 190, 32, 15), sombra, alfa=alfa)
        for dx, dy, r in ((-58, -12, 28), (-18, -26, 38), (28, -20, 32), (62, -8, 22)):
            j = (h01(seed, int(dx)) - 0.5) * 8
            lz.relleno(circulo(dx + j, dy + 4, r, 28), sombra, alfa=alfa)
            lz.relleno(circulo(dx + j, dy, r, 28), col, alfa=alfa)
        lz.relleno(rect_red(-92, -18, 184, 28, 14), col, alfa=alfa)


def arbusto(lz, x, y, s=1.0, col=(76, 172, 102), seed=0):
    osc = oscurecer(col, 0.25)
    cla = aclarar(col, 0.22)
    with lz.grupo(x, y, s):
        for dx, dy, r in ((-34, -18, 24), (34, -16, 22), (0, -28, 30)):
            lz.relleno(circulo(dx, dy, r, 24), osc)
        for dx, dy, r in ((-26, -22, 22), (26, -20, 20), (-2, -32, 28)):
            lz.relleno(circulo(dx, dy, r, 24), col)
        lz.relleno(circulo(-8, -38, 14, 20), cla, alfa=0.7)


def pino(lz, x, y, s=1.0, col=(56, 136, 96), incl=0.0):
    osc = oscurecer(col, 0.26)
    with lz.grupo(x, y, s, incl):
        lz.relleno(rect_red(-7, -38, 14, 40, 4), (112, 74, 58))
        for k, (yb, w, h) in enumerate(((-30, 74, 58), (-66, 58, 52), (-98, 42, 44))):
            tri = np.array([[-w / 2, yb], [w / 2, yb], [0, yb - h]], float)
            lz.relleno(tri, col)
            tri_s = np.array([[0, yb], [w / 2, yb], [0, yb - h]], float)
            lz.relleno(tri_s, osc, alfa=0.55)


def aerogenerador(lz, x, y, s=1.0, t=0.0, vel=1.4):
    with lz.grupo(x, y, s):
        lz.relleno(np.array([[-7, 0], [7, 0], [3, -190], [-3, -190]], float), (230, 236, 248))
        lz.relleno(np.array([[0, 0], [7, 0], [3, -190], [0, -190]], float), (192, 202, 226))
        with lz.grupo(0, -190, 1.0, t * vel):
            for k in range(3):
                with lz.grupo(0, 0, 1.0, k * 2 * math.pi / 3):
                    pala = np.array([[-4, 0], [4, 0], [2, -78], [-1, -78]], float)
                    lz.relleno(pala, (244, 248, 255))
            lz.relleno(circulo(0, 0, 9, 20), (180, 192, 220))


def farola(lz, x, y, s=1.0, on=0.35):
    with lz.grupo(x, y, s):
        lz.relleno(rect_red(-14, -8, 28, 10, 4), (62, 60, 88))
        lz.relleno(rect_red(-4, -185, 8, 180, 3), (82, 80, 112))
        lz.relleno(rect_red(-4, -188, 38, 8, 4), (82, 80, 112))
        lz.relleno(elipse(26, -182, 14, 7, 0, 20), (255, 236, 168))
        if on > 0.02:
            lz.halo(26, -176, 85, (255, 224, 130), alfa=0.45 * on)


def casa_corte(lz, x, y, s=1.0, t=0.0, alt_casa=0.0):
    """Casa en corte transversal (origen en la base, ancho ~420, alto ~310).
    Muestra interior cálido: alfombra, sofá, mesa con libros, lámpara de pie y maceta que flotan suavemente."""
    fl = alt_casa * 28.0
    osc = math.sin(t * 2.1) * 4.0 * alt_casa
    with lz.grupo(x, y, s):
        # Cimiento y sombra base
        lz.relleno(elipse(0, 4, 230, 14, 0, 36), (26, 22, 58), alfa=0.28)
        lz.relleno(rect_red(-215, -22, 430, 24, 6), (88, 82, 118))
        # Muros exteriores y fondo de la habitación
        lz.relleno(rect_red(-202, -242, 404, 222, 8), (64, 58, 98))
        lz.relleno(rect_red(-186, -228, 372, 198, 6), (248, 234, 212))
        # Pared lateral en sombra suave
        lz.relleno(rect_red(120, -228, 66, 198, 2), (232, 214, 190))
        # Ventana panorámica al cielo azul
        lz.relleno(rect_red(-152, -196, 118, 92, 8), (126, 192, 246))
        lz.relleno(np.array([[-152, -130], [-34, -130], [-34, -104], [-152, -104]], float), (96, 172, 120))
        lz.relleno(rect_red(-156, -200, 126, 8, 3), (140, 96, 74))
        lz.relleno(rect_red(-156, -108, 126, 8, 3), (140, 96, 74))
        lz.relleno(rect_red(-96, -196, 6, 92, 2), (248, 234, 212))
        # Librero en la pared derecha
        lz.relleno(rect_red(72, -192, 86, 12, 4), (156, 102, 74))
        lz.relleno(rect_red(72, -142, 86, 12, 4), (156, 102, 74))
        for k, (bx, col) in enumerate(((80, (236, 84, 96)), (96, (68, 168, 218)), (114, (246, 186, 68)), (132, (116, 192, 118)))):
            dy = -(fl * (0.7 + 0.25 * k) + math.sin(t * 2.4 + k) * 5 * alt_casa)
            rot = 0.18 * math.sin(t * 1.7 + k) * alt_casa
            with lz.grupo(bx + 6, -192 + dy, 1.0, rot):
                lz.relleno(rect_red(-6, -26, 12, 26, 2), col)
        # Alfombra (se despega apenas del suelo)
        lz.relleno(rect_red(-130, -36 - fl * 0.25, 220, 8, 4), (218, 88, 104))
        # Sofá (se levanta unos centímetros del suelo)
        with lz.grupo(-75, -32 - fl * 0.45 + osc * 0.4, 1.0, 0.03 * alt_casa * math.sin(t * 1.5)):
            lz.relleno(rect_red(-68, -56, 136, 46, 12), (62, 138, 196))
            lz.relleno(rect_red(-76, -38, 152, 30, 10), (82, 162, 218))
            lz.relleno(rect_red(-62, -44, 58, 18, 7), (112, 186, 236))
            lz.relleno(rect_red(4, -44, 58, 18, 7), (112, 186, 236))
        # Lámpara de pie y maceta flotando
        with lz.grupo(42, -32 - fl * 0.65 - osc * 0.5, 1.0, -0.05 * alt_casa):
            lz.relleno(rect_red(-16, -6, 32, 6, 3), (90, 84, 116))
            lz.relleno(rect_red(-3, -110, 6, 106, 2), (110, 104, 138))
            pantalla = np.array([[-24, -110], [24, -110], [16, -142], [-16, -142]], float)
            lz.relleno(pantalla, (255, 216, 108))
            lz.halo(0, -118, 65, (255, 226, 138), alfa=0.35)
        with lz.grupo(135, -32 - fl * 0.9 + osc, 1.0, 0.12 * alt_casa * math.cos(t * 1.8)):
            lz.relleno(np.array([[-16, 0], [16, 0], [20, -28], [-20, -28]], float), (216, 118, 78))
            lz.relleno(elipse(-8, -42, 10, 18, -0.35, 20), (74, 178, 106))
            lz.relleno(elipse(8, -44, 10, 18, 0.35, 20), (92, 196, 120))
            lz.relleno(elipse(0, -48, 9, 20, 0.0, 20), (62, 158, 94))
        # Techo triangular estilo Kurzgesagt
        techo_ext = np.array([[-228, -236], [228, -236], [0, -326]], float)
        techo_int = np.array([[-196, -236], [196, -236], [0, -306]], float)
        lz.relleno(techo_ext, (214, 86, 82))
        lz.relleno(techo_int, (182, 68, 72))
        # Chimenea
        lz.relleno(rect_red(108, -308, 34, 52, 4), (182, 68, 72))
        lz.relleno(rect_red(102, -314, 46, 10, 4), (214, 86, 82))


def bicicleta(lz, x, y, s=1.0, t=0.0, giro=1.0, col=(244, 134, 52)):
    """Bicicleta vista de perfil (origen entre las dos ruedas, en el suelo)."""
    with lz.grupo(x, y, s):
        for wx in (-48, 48):
            lz.trazo(circulo(wx, -28, 26, 36), (46, 42, 76, 255), 7, cerrado=True, afinar=False)
            lz.trazo(circulo(wx, -28, 20, 32), (216, 224, 242, 255), 3, cerrado=True, afinar=False)
            for k in range(4):
                a = t * 4.5 * giro + k * math.pi / 2
                dx, dy = 20 * math.cos(a), 20 * math.sin(a)
                lz.trazo(np.array([[wx - dx, -28 - dy], [wx + dx, -28 + dy]]), (190, 198, 224, 220), 2.2, afinar=False)
            lz.relleno(circulo(wx, -28, 6, 16), col)
        # Cuadro de la bicicleta
        lz.trazo(np.array([[-48, -28], [-6, -28], [26, -64], [-22, -64], [-48, -28]]), col + (255,), 6.5, afinar=False)
        lz.trazo(np.array([[-6, -28], [-24, -72]]), col + (255,), 6.5, afinar=False)
        lz.trazo(np.array([[48, -28], [22, -78], [36, -82]]), col + (255,), 6.5, afinar=False)
        # Asiento y manubrio
        lz.relleno(rect_red(-34, -78, 24, 8, 4), (46, 42, 76))
        lz.relleno(circulo(38, -82, 5, 12), (46, 42, 76))


def taza_cafe(lz, x, y, s=1.0, t=0.0, ingravidez=0.0):
    """Taza de café caliente; cuando ingravidez > 0, esferas de café salen flotando."""
    with lz.grupo(x, y, s):
        # Plato base
        lz.relleno(elipse(0, -3, 28, 6, 0, 24), (236, 240, 252))
        # Asa
        lz.trazo(circulo(18, -22, 10, 24), (248, 250, 255, 255), 5.0, cerrado=True, afinar=False)
        # Cuerpo de la taza
        lz.relleno(rect_red(-18, -38, 36, 34, 8), (248, 250, 255))
        lz.relleno(rect_red(2, -38, 16, 34, 6), (222, 228, 246))
        lz.relleno(rect_red(-18, -26, 36, 8, 2), (236, 92, 98))
        # Café líquido y gotas flotando en ingravidez
        if ingravidez > 0.02:
            for k, (gx, gy, r) in enumerate(((-6, -52, 8), (8, -68, 6.5), (-12, -82, 5.0), (4, -96, 4.2))):
                yy = gy * ingravidez + math.sin(t * 3.2 + k) * 4 * ingravidez
                xx = gx + math.cos(t * 2.5 + k) * 4 * ingravidez
                lz.relleno(circulo(xx, -36 + yy, r, 18), (112, 62, 44))
                lz.relleno(circulo(xx - r * 0.3, -36 + yy - r * 0.3, r * 0.32, 12), (186, 124, 92))
        else:
            for k in range(2):
                u = (t * 0.9 + k * 0.5) % 1.0
                xx = -5 + 10 * k + 4 * math.sin(t * 3 + k)
                yy = -42 - 24 * u
                lz.relleno(circulo(xx, yy, 5 * (1 - u * 0.5), 14), (255, 255, 255), alfa=0.45 * (1 - u))


def coche_urbano(lz, x, y, s=1.0, t=0.0, col=(236, 82, 96), voltear=False):
    """Coche redondeado estilo Kurzgesagt (origen entre las ruedas, a ras del suelo)."""
    sx = -s if voltear else s
    osc = oscurecer(col, 0.22)
    cla = aclarar(col, 0.25)
    with lz.grupo(x, y, sx, 0.0, sy=s):
        # Carrocería inferior y cabina
        lz.relleno(rect_red(-96, -54, 192, 38, 16), col)
        lz.relleno(rect_red(-96, -34, 192, 18, 8), osc)
        cab = np.array([[-58, -52], [44, -52], [22, -88], [-42, -88]], float)
        lz.relleno(cab, col)
        vent1 = np.array([[-38, -54], [-4, -54], [-4, -82], [-34, -82]], float)
        vent2 = np.array([[2, -54], [36, -54], [18, -82], [2, -82]], float)
        lz.relleno(vent1, (164, 218, 250))
        lz.relleno(vent2, (164, 218, 250))
        lz.relleno(rect_red(-88, -50, 40, 6, 3), cla, alfa=0.6)
        # Faros
        lz.relleno(elipse(92, -38, 6, 9, 0, 16), (255, 238, 148))
        lz.relleno(elipse(-92, -38, 5, 8, 0, 16), (255, 90, 90))
        # Ruedas
        for wx in (-56, 56):
            lz.relleno(circulo(wx, -18, 20, 28), (40, 36, 68))
            lz.relleno(circulo(wx, -18, 11, 20), (198, 206, 228))
            lz.relleno(circulo(wx, -18, 4, 12), col)


def burbuja_agua(lz, x, y, r, t, seed=0, col=(64, 168, 238), alfa=0.88):
    """Esfera de agua deformándose suavemente en ingravidez con borde de luz y brillo especular."""
    if alfa <= 0.01 or r <= 1.0:
        return
    pts = blob(x, y, r, seed=seed, irr=0.12, n=48, lob=4)
    # Ondulación temporal suave
    ang = np.linspace(0, 2 * math.pi, len(pts), endpoint=False)
    wob = 1.0 + 0.06 * np.sin(ang * 3 + t * 3.2 + seed) + 0.04 * np.cos(ang * 2 - t * 2.4)
    pts = np.array([x, y]) + (pts - np.array([x, y])) * wob[:, None]
    lz.relleno(pts, col, alfa=alfa)
    pts_in = np.array([x + r * 0.1, y + r * 0.12]) + (pts - np.array([x, y])) * 0.78
    lz.relleno(pts_in, aclarar(col, 0.22), alfa=alfa * 0.55)
    lz.relleno(elipse(x - r * 0.34, y - r * 0.34, r * 0.24, r * 0.14, -0.6, 20), (235, 250, 255), alfa=alfa * 0.85)
    lz.relleno(circulo(x - r * 0.12, y - r * 0.52, r * 0.08, 14), (255, 255, 255), alfa=alfa * 0.8)


def resorte_aire(lz, x, y, h_base, estiramiento, col=(180, 230, 255), alfa=0.85):
    """Resorte helicoidal vertical que representa la columna de aire rebotando hacia arriba."""
    if alfa <= 0.01:
        return
    h = h_base * (1.0 + 1.15 * estiramiento)
    n = 90
    u = np.linspace(0, 1, n)
    vueltas = 5.5
    xx = x + 34 * np.sin(u * vueltas * 2 * math.pi) * (1.0 - 0.15 * u)
    yy = y - u * h
    pts = np.stack([xx, yy], 1)
    lz.trazo(pts, col + (int(255 * alfa),), 6.0, afinar=False)
    # Punta de flecha arriba
    top_y = y - h - 10
    lz.relleno(np.array([[x, top_y - 26], [x - 20, top_y + 4], [x + 20, top_y + 4]], float), col, alfa=alfa)


def malla_curva(lz, cx, cy, r_pozo=220.0, prof=110.0, alfa=1.0, col=(98, 196, 255)):
    """Malla 3D de espacio-tiempo curvada hacia abajo bajo el cuerpo en (cx, cy)."""
    if alfa <= 0.01:
        return
    c_rgba = col + (int(190 * alfa),)
    # Líneas horizontales y transversales proyectadas en perspectiva isométrica suave
    xs = np.linspace(-560, 560, 45)
    zs = np.linspace(-340, 340, 13)
    for z in zs:
        d2 = xs ** 2 + z ** 2
        hund = prof * np.exp(-d2 / (r_pozo ** 2))
        px = cx + xs + z * 0.38
        py = cy + z * 0.42 + hund
        lz.trazo(np.stack([px, py], 1), c_rgba, 3.0, afinar=False)
    xs_g = np.linspace(-520, 520, 15)
    zs_f = np.linspace(-340, 340, 40)
    for x0 in xs_g:
        d2 = x0 ** 2 + zs_f ** 2
        hund = prof * np.exp(-d2 / (r_pozo ** 2))
        px = cx + x0 + zs_f * 0.38
        py = cy + zs_f * 0.42 + hund
        lz.trazo(np.stack([px, py], 1), c_rgba, 2.6, afinar=False)
