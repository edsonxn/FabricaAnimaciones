# -*- coding: utf-8 -*-
"""Mundos 2D de la escena 4 (los caxcanes): tarjetas de su cultura (fortaleza, juego de pelota, fiesta), Xochipilli, arco solar del solsticio, nubes y lluvia, y la fiesta de hoy."""
import math

import numpy as np

import plano as P
import kz_pers2d as K2
import paisajes as PA
from motor import circulo, elipse, rect_red, catmull, h01, prog, smooth, e_out, e_back, e_inout, W, H, ruido1
from kz_abstracto import _petalo_pts
from mundos_a import flor_xuchitl


def tarjeta(lz, x, y, w, h, k=1.0, color=(250, 244, 255), borde=(122, 52, 200), alfa=1.0, capa=1):
    """Tarjeta redondeada con sombra de contacto (centro x, y)."""
    if k <= 0.01:
        return
    w, h = w * k, h * k
    lz.relleno(rect_red(x - w / 2 + 10, y - h / 2 + 14, w, h, 26 * k), (14, 6, 40), alfa=0.35 * alfa, capa=capa)
    lz.relleno(rect_red(x - w / 2 - 6, y - h / 2 - 6, w + 12, h + 12, 30 * k), borde, alfa=alfa, capa=capa)
    lz.relleno(rect_red(x - w / 2, y - h / 2, w, h, 26 * k), color, alfa=alfa, capa=capa)


def fortaleza(lz, x, y, s, t=0.0, capa=1):
    """Cerro con muralla almenada y dos torres (icono de «fortalezas en los cerros»)."""
    lz.relleno(np.array([(x - 230 * s, y + 130 * s), (x - 90 * s, y - 70 * s), (x + 90 * s, y - 70 * s), (x + 230 * s, y + 130 * s)]), (126, 74, 132), capa=capa)
    lz.relleno(np.array([(x - 230 * s, y + 130 * s), (x - 90 * s, y - 70 * s), (x - 20 * s, y - 70 * s), (x - 110 * s, y + 130 * s)]), (156, 98, 148), capa=capa)
    lz.relleno(rect_red(x - 105 * s, y - 120 * s, 210 * s, 56 * s, 6 * s), (214, 190, 166), capa=capa)
    for i in range(8):
        lz.relleno(rect_red(x - 105 * s + i * 28 * s, y - 138 * s, 16 * s, 20 * s, 2), (214, 190, 166), capa=capa)
    for sd in (-1, 1):
        lz.relleno(rect_red(x + sd * 105 * s - 22 * s, y - 170 * s, 44 * s, 110 * s, 6 * s), (196, 172, 150), capa=capa)
        lz.relleno(np.array([(x + sd * 105 * s - 30 * s, y - 168 * s), (x + sd * 105 * s, y - 214 * s), (x + sd * 105 * s + 30 * s, y - 168 * s)]), (206, 96, 84), capa=capa)
    lz.relleno(rect_red(x - 18 * s, y - 94 * s, 36 * s, 30 * s, 14 * s), (70, 40, 80), capa=capa)
    for q in range(5):                                           # guerreros en la muralla
        px = x - 80 * s + q * 40 * s
        lz.relleno(circulo(px, y - 134 * s + 2 * math.sin(t * 3 + q), 6 * s, 10), (60, 30, 70), capa=capa)


def cancha_pelota(lz, x, y, s, t=0.0, capa=1):
    """Juego de pelota visto de lado: dos taludes inclinados, piso y una pelota que rebota entre dos jugadores."""
    lz.relleno(np.array([(x - 240 * s, y + 70 * s), (x + 240 * s, y + 70 * s), (x + 240 * s, y + 100 * s), (x - 240 * s, y + 100 * s)]), (232, 214, 176), capa=capa)
    for sd in (-1, 1):
        lz.relleno(np.array([(x + sd * 250 * s, y + 70 * s), (x + sd * 250 * s, y - 70 * s), (x + sd * 190 * s, y - 70 * s), (x + sd * 100 * s, y + 70 * s)]), (206, 188, 168), capa=capa)
        lz.relleno(np.array([(x + sd * 190 * s, y - 70 * s), (x + sd * 250 * s, y - 70 * s), (x + sd * 250 * s, y - 56 * s), (x + sd * 196 * s, y - 56 * s)]), (232, 214, 194), capa=capa)
    # aro de piedra
    lz.trazo(elipse(x, y - 40 * s, 16 * s, 26 * s, 0.0, 20), (190, 84, 70), 8 * s, cerrado=True, afinar=False, temblor=0.0, capa=capa)
    bx = x + 110 * s * math.sin(t * 2.2)
    by = y + 40 * s - 90 * s * abs(math.sin(t * 4.4 + 0.3))
    for (jx, tipo, mir) in ((x - 150 * s, "caxcan", 1), (x + 150 * s, "jefe_caxcan", -1)):
        K2.cuerpo(lz, jx, y + 76 * s, 11 * s, tipo, t, piernas="baila", brazos="baila", mirar=mir, vista="frente", seed=int(jx), cara="ninguna", sombra=False)
    lz.relleno(circulo(bx + 4 * s, by + 4 * s, 15 * s, 14), (60, 30, 50), alfa=0.35, capa=capa)
    lz.relleno(circulo(bx, by, 15 * s, 14), (74, 52, 56), capa=capa)
    lz.relleno(circulo(bx - 4 * s, by - 4 * s, 6 * s, 10), (150, 120, 110), capa=capa)


def notas_musicales(lz, x, y, s, t, n=4, capa=2):
    """Notas que flotan hacia arriba y ondas de sonido."""
    for i in range(n):
        u = (t * 0.45 + i / n) % 1.0
        px = x + 70 * s * math.sin(u * 5 + i * 1.9)
        py = y - 220 * s * u
        a = min(1.0, u * 6) * (1 - u)
        col = ((255, 190, 60), (236, 80, 140), (110, 220, 200), (150, 120, 255))[i % 4]
        lz.relleno(elipse(px, py, 14 * s, 10 * s, -0.4, 14), col, alfa=a, capa=capa)
        lz.relleno(rect_red(px + 10 * s, py - 46 * s, 5 * s, 48 * s, 2), col, alfa=a, capa=capa)
        lz.relleno(np.array([(px + 14 * s, py - 46 * s), (px + 36 * s, py - 34 * s), (px + 14 * s, py - 30 * s)]), col, alfa=a, capa=capa)


def arco_solar(lz, t, u, cx=960, cy=900, rx=760, ry=620, capa=0):
    """Trayectoria del sol sobre el horizonte (arco punteado) y el sol en la posición u (0 = amanecer, 1 = atardecer). Devuelve la posición del sol."""
    th = np.linspace(math.pi, 0, 80)
    P.discontinua(lz, [(cx + rx * math.cos(a), cy - ry * math.sin(a)) for a in th], (255, 255, 255), ancho=5.0, largo=22.0, hueco=18.0, fase=-t * 20, capa=2)
    a = math.pi * (1 - u)
    sx, sy = cx + rx * math.cos(a), cy - ry * math.sin(a)
    lz.halo(sx, sy, 190, (255, 230, 150), alfa=0.55, dureza=1.2, capa=2)
    lz.relleno(circulo(sx, sy, 62, 36), (255, 244, 190), capa=2)
    return sx, sy


def nube(lz, x, y, s, color=(236, 232, 248), sombra=(150, 140, 190), capa=2, alfa=1.0):
    for (dx, dy, r, c) in ((0, 22, 1.0, sombra), (-90, 12, 0.7, sombra), (90, 16, 0.75, sombra), (0, 0, 0.95, color), (-86, -8, 0.68, color), (88, -4, 0.7, color), (-20, -44, 0.6, P.aclarar(color, 0.2))):
        lz.relleno(circulo(x + dx * s, y + dy * s, 78 * r * s, 22), c, alfa=alfa, capa=capa)


def lluvia(lz, t, a=1.0, x0=0, x1=W, y0=300, y1=H, n=140, seed=3, capa=2):
    for i in range(n):
        u = (t * 1.6 + h01(seed, i, 1)) % 1.0
        x = x0 + (x1 - x0) * h01(seed, i, 2) - 60 * u
        y = y0 + (y1 - y0) * u
        lz.relleno(np.array([(x, y), (x + 3.5, y), (x - 12, y + 40), (x - 15, y + 40)]), (190, 230, 255), alfa=0.55 * a * (1 - 0.5 * u), capa=capa)


def fachada_iglesia(lz, x, y, s, capa=0, luz=0.0):
    """Fachada 2D de una iglesia de pueblo con dos torres y portada (de fondo en la fiesta)."""
    lz.relleno(rect_red(x - 200 * s, y - 320 * s, 400 * s, 320 * s, 8), (240, 214, 186), capa=capa)
    lz.relleno(rect_red(x - 200 * s, y - 320 * s, 400 * s, 40 * s, 8), (250, 232, 208), capa=capa)
    for sd in (-1, 1):
        tx = x + sd * 150 * s
        lz.relleno(rect_red(tx - 46 * s, y - 520 * s, 92 * s, 220 * s, 6), (232, 200, 170), capa=capa)
        lz.relleno(np.array([(tx - 56 * s, y - 516 * s), (tx, y - 600 * s), (tx + 56 * s, y - 516 * s)]), (206, 96, 84), capa=capa)
        lz.relleno(rect_red(tx - 20 * s, y - 470 * s, 40 * s, 70 * s, 18 * s), (90, 54, 80), capa=capa)
    lz.relleno(rect_red(x - 74 * s, y - 250 * s, 148 * s, 250 * s, 10), (206, 160, 130), capa=capa)
    lz.relleno(np.array([(x - 54 * s, y), (x - 54 * s, y - 130 * s), (x, y - 190 * s), (x + 54 * s, y - 130 * s), (x + 54 * s, y)]), (96, 56, 70), capa=capa)
    lz.relleno(circulo(x, y - 290 * s, 28 * s, 20), (90, 54, 80), capa=capa)
    lz.relleno(rect_red(x - 4 * s, y - 380 * s, 8 * s, 50 * s, 2), (250, 244, 230), capa=capa)
    lz.relleno(rect_red(x - 22 * s, y - 364 * s, 44 * s, 8 * s, 2), (250, 244, 230), capa=capa)


def papel_picado(lz, t, y=130, n=14, capa=2):
    """Guirnalda de banderines de colores a lo ancho de la pantalla que ondea."""
    pts = [(i * W / (n * 2), y + 40 * math.sin(i * math.pi / (n * 2) * 2) + 10 * math.sin(t * 2 + i)) for i in range(n * 2 + 1)]
    lz.trazo(np.array(pts), (250, 244, 230), 3.0, afinar=False, temblor=0.0, capa=capa)
    cols = [(236, 70, 140), (255, 190, 60), (80, 200, 190), (122, 90, 255), (240, 130, 36), (96, 200, 120)]
    for i in range(n * 2):
        px, py = pts[i]
        qx, qy = pts[i + 1]
        mx, my = (px + qx) / 2, (py + qy) / 2
        bal = 6 * math.sin(t * 3 + i)
        lz.relleno(np.array([(px + 6, py + 2), (qx - 6, qy + 2), (mx + bal, my + 62)]), cols[i % len(cols)], capa=capa)
        lz.relleno(np.array([(mx - 8 + bal * 0.5, my + 16), (mx + 8 + bal * 0.5, my + 16), (mx + bal, my + 30)]), P.aclarar(cols[i % len(cols)], 0.45), alfa=0.8, capa=capa)


def sello(lz, x, y, r, texto, t=0.0, k=1.0, alfa=1.0, capa=2):
    """Sello redondo de «patrimonio» con listones y estrella."""
    if k <= 0.01:
        return
    r = r * k
    for sd in (-1, 1):
        lz.relleno(np.array([(x + sd * r * 0.3, y + r * 0.6), (x + sd * r * 0.9, y + r * 1.9), (x + sd * r * 0.55, y + r * 1.7), (x + sd * r * 0.15, y + r * 1.95), (x + sd * r * 0.05, y + r * 0.7)]), (222, 60, 70), alfa=alfa, capa=capa)
    lz.halo(x, y, r * 1.8, (255, 220, 120), alfa=0.35 * alfa, capa=capa)
    n = 20
    pts = [(x + (r if i % 2 == 0 else r * 0.9) * math.cos(i * math.pi / n * 2 + t * 0.3), y + (r if i % 2 == 0 else r * 0.9) * math.sin(i * math.pi / n * 2 + t * 0.3)) for i in range(n)]
    lz.relleno(np.array(pts), (250, 190, 40), alfa=alfa, capa=capa)
    lz.relleno(circulo(x, y, r * 0.78, 30), (255, 226, 120), alfa=alfa, capa=capa)
    lz.relleno(circulo(x, y, r * 0.68, 30), (250, 190, 40), alfa=alfa, capa=capa)
    st = [(x + (r * 0.46 if i % 2 == 0 else r * 0.2) * math.cos(-math.pi / 2 + i * math.pi / 5), y + (r * 0.46 if i % 2 == 0 else r * 0.2) * math.sin(-math.pi / 2 + i * math.pi / 5)) for i in range(10)]
    lz.relleno(np.array(st), (255, 250, 220), alfa=alfa, capa=capa)
    P.rotulo(lz, x, y + r * 1.2, texto, px=max(14, r * 0.28), color=(255, 255, 255), alfa=alfa, sombra=0.0)
