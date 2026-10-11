# -*- coding: utf-8 -*-
"""Mundos de la escena 7 (la capital a la vista): el monte de las Cruces con sus pinos y el camino, la vista del valle de México desde la cumbre (2D) y el campo de instrucción realista."""
import math

import numpy as np

import kz_iso as I
from kz_iso import tint
import kz_iso_obj as O
import kz_iso_obj2 as O2
import kz_iso_arq as A
import kz_iso_arq2 as B
import kz_gente_iso as G
import kz_iso_deco as DC
import plano as P
from motor import W, H, h01, circulo, elipse, rect_red


# ------------------------------------------------------------------------------------------------ el monte de las Cruces
class MonteCruces:
    """Paso de montaña boscoso con un camino que sube en zigzag (de abajo-izquierda a arriba-derecha), pinos, rocas, un arroyo y un puesto de vigilancia."""
    CAMINO = [(-100, 330), (60, 290), (160, 230), (230, 190), (300, 150), (380, 90), (480, 50)]

    def __init__(self):
        self._est = None
        self._t = 0.0

    def suelo(self, lz, iso, t):
        I.isla(lz, iso, -120, -80, 520, 420, color_top=(110, 154, 98), t=t, seed=101, esp=44)
        DC.parches(lz, iso, -120, -80, 520, 420, (110, 154, 98), n=24, var=24, seed=102, alfa=0.55, tam=(50, 100))
        I.camino(lz, iso, self.CAMINO, 54, (206, 184, 140), borde=(176, 150, 112))
        DC.acequia(lz, iso, [(-100, 410), (120, 380), (300, 330), (520, 300)], t, ancho=14.0)

    def objetos(self, t):
        self._t = t
        if self._est is None:
            m = I.Mundo()
            DC.bosque(m, -120, -80, 520, 420, n=120, seed=103, evitar=((-110, 250, 200, 400), (60, 120, 420, 330), (-120, -80, 40, 80)) if False else (), t_fn=lambda: self._t, tipos=("pino", "pino", "pino", "arbol", "roca"), h=(50, 84), min_d=26)
            self._est = m
        m = I.Mundo()
        m.fijos = list(self._est.fijos)
        return m


# ------------------------------------------------------------------------------------------------ la vista del valle de México desde la cumbre (2D)
def vista_capital(lz, t, dx=0.0, horizonte=600.0):
    """Valle de México visto desde el monte de las Cruces: volcanes con nieve, lago, ciudad-isla con catedral y calzadas, lomas verdes en primer plano. Todo en pantalla."""
    # volcanes (Iztaccíhuatl y Popocatépetl) con casquete de nieve
    for (cx, h, w, col) in ((1280, 360, 760, (170, 164, 214)), (1640, 440, 640, (160, 152, 208)), (760, 220, 900, (190, 184, 226))):
        cx2 = cx + dx * 0.2
        lz.relleno(np.array([[cx2 - w / 2, horizonte], [cx2 - w * 0.07, horizonte - h], [cx2 + w * 0.07, horizonte - h], [cx2 + w / 2, horizonte]]), col, capa=0)
        lz.relleno(np.array([[cx2 - w * 0.12, horizonte - h * 0.78], [cx2 - w * 0.07, horizonte - h], [cx2 + w * 0.07, horizonte - h], [cx2 + w * 0.12, horizonte - h * 0.78], [cx2 + w * 0.05, horizonte - h * 0.84], [cx2, horizonte - h * 0.74], [cx2 - w * 0.05, horizonte - h * 0.82]]), (250, 250, 255), capa=0)
        lz.relleno(np.array([[cx2 + w * 0.05, horizonte - h * 0.9], [cx2 + w * 0.07, horizonte - h], [cx2 + w / 2 * 0.62, horizonte - h * 0.1], [cx2 + w * 0.2, horizonte]]), P.oscurecer(col, 0.12), alfa=0.6, capa=0)
    # lago de Texcoco y la ciudad en su isla
    lz.relleno(np.array([[-50, horizonte], [1970, horizonte], [1970, horizonte + 170], [-50, horizonte + 170]]), (96, 164, 226), capa=0)
    for i in range(14):
        x = (h01(111, i) * 2200 - 150 + t * (8 + 4 * h01(112, i))) % 2200 - 150
        y = horizonte + 24 + 120 * h01(113, i)
        lz.trazo(np.array([[x - 34, y], [x - 12, y - 4], [x + 12, y + 2], [x + 34, y - 2]]), (210, 236, 252), 3.0, afinar=False, temblor=0.0, capa=0)
    ix, iy = 780 + dx * 0.35, horizonte + 70
    lz.relleno(elipse(ix, iy + 22, 360, 52, 0, 40), (206, 192, 150), capa=0)
    pal = [(236, 110, 120), (250, 210, 90), (110, 190, 220), (150, 210, 130), (230, 150, 90), (180, 140, 220), (250, 240, 220)]
    for r in range(3):
        for i in range(26):
            x = ix - 330 + i * 26 + (r % 2) * 13
            y = iy + 6 + r * 12 - abs(x - ix) * 0.02
            h = 14 + 10 * h01(114, i, r)
            c = pal[int(h01(115, i, r) * 7) % 7]
            lz.relleno(rect_red(x - 10, y - h, 20, h, 2), c, capa=0)
            lz.relleno(np.array([[x - 12, y - h + 1], [x + 12, y - h + 1], [x, y - h - 9]]), (200, 100, 84), capa=0)
    # catedral y palacio
    lz.relleno(rect_red(ix - 40, iy - 58, 80, 48, 3), (244, 214, 150), capa=0)
    for dxx in (-34, 24):
        lz.relleno(rect_red(ix + dxx, iy - 90, 16, 34, 2), (250, 226, 170), capa=0)
        lz.relleno(circulo(ix + dxx + 8, iy - 94, 9, 12), (232, 196, 120), capa=0)
    lz.relleno(circulo(ix, iy - 64, 18, 16), (232, 196, 120), capa=0)
    # calzadas hacia la isla
    for (xa, ya) in ((-50, horizonte + 160), (1970, horizonte + 150), (1000, horizonte + 170)):
        lz.trazo(np.array([[xa, ya], [ix + (xa - ix) * 0.05, iy + 20]]), (206, 192, 150), 10.0, afinar=False, temblor=0.0, capa=0)
    # neblina del valle
    lz.relleno(np.array([[-50, horizonte - 50], [1970, horizonte - 50], [1970, horizonte + 20], [-50, horizonte + 20]]), (236, 226, 240), alfa=0.28, capa=0)
    # lomas verdes del primer plano
    for k, (col, y0, amp) in enumerate((((120, 170, 108), 820, 40), ((98, 148, 94), 910, 50))):
        pts = [(-50, 1200)]
        for i in range(0, 22):
            x = -50 + i * 100 + dx * (0.3 + 0.3 * k)
            pts.append((x, y0 + amp * math.sin(i * 0.8 + k * 2.0)))
        pts.append((2050, 1200))
        lz.relleno(np.array(pts, float), col, capa=0)


def multitud_espalda(lz, t, n=140, y0=760.0, y1=1090.0, seed=5, alzar=0.0, banderas=3, escala=1.0):
    """Mar de gente vista de espaldas (cabeza, sombrero de palma, camisa blanca, faja roja) con machetes, lanzas y estandartes que se agitan; filas más cercanas = más grandes."""
    filas = sorted(range(n), key=lambda i: h01(seed, i, 1))
    for i in filas:
        f = h01(seed, i, 1)
        y = y0 + (y1 - y0) * f
        s = (0.55 + 0.9 * f) * escala
        x = (h01(seed, i, 2) * 2100 - 100)
        bob = math.sin(t * 3 + i) * 2 * s
        col = [(246, 242, 232), (240, 236, 224), (226, 212, 186), (250, 246, 236)][i % 4]
        lz.relleno(elipse(x, y + 2 * s, 14 * s, 4 * s, 0, 10), (30, 40, 40), alfa=0.22, capa=1)
        lz.relleno(rect_red(x - 9 * s, y - 34 * s + bob, 18 * s, 34 * s, 7 * s), col, capa=1)
        lz.relleno(rect_red(x - 9 * s, y - 14 * s + bob, 18 * s, 5 * s, 2 * s), [(204, 52, 52), (60, 150, 160), (240, 180, 70)][i % 3], capa=1)
        lz.relleno(circulo(x, y - 40 * s + bob, 7 * s, 10), [(150, 98, 70), (190, 130, 98), (120, 80, 60)][i % 3], capa=1)
        lz.relleno(elipse(x, y - 45 * s + bob, 15 * s, 4.4 * s, 0, 12), (236, 198, 120), capa=1)
        lz.relleno(circulo(x, y - 49 * s + bob, 7 * s, 10), (226, 184, 104), capa=1)
        if i % 4 == 0:                                         # armas en alto
            a = (-0.2 + 0.3 * math.sin(t * 4 + i)) * (0.4 + alzar)
            hx = x + 10 * s
            lz.trazo(np.array([[hx, y - 24 * s + bob], [hx + 18 * s * math.sin(a), y - (62 + 22 * alzar) * s + bob]]), (110, 80, 60), 3 * s, afinar=False, temblor=0.0, capa=1)
        if i % 9 == 3:
            lz.trazo(np.array([[x - 10 * s, y - 22 * s + bob], [x - 22 * s, y - 56 * s + bob]]), (214, 220, 232), 3.4 * s, afinar=False, temblor=0.0, capa=1)
    for j in range(banderas):
        bx = 420 + j * 560 + 30 * math.sin(t * 0.7 + j)
        by = y1 - 40
        lz.trazo(np.array([[bx, by], [bx, by - 300]]), (120, 88, 62), 6, afinar=False, temblor=0.0, capa=1)
        pts = [(bx + k * 6, by - 300 + 6 * math.sin(t * 5 - k * 0.5 + j) + 0.3 * k) for k in range(0, 21)]
        pts += [(bx + k * 6, by - 220 + 6 * math.sin(t * 5 - k * 0.5 + j) + 0.3 * k) for k in range(20, -1, -1)]
        lz.relleno(np.array(pts), [(60, 150, 130), (206, 60, 70), (250, 244, 232)][j % 3], capa=1)


# ------------------------------------------------------------------------------------------------ campo de instrucción realista
class CampoRealista:
    """Explanada de tierra con cuartel, banderas de la Corona, hileras de cañones y tiendas: aquí se reorganiza el ejército del rey."""

    def __init__(self):
        self._est = None
        self._t = 0.0

    def suelo(self, lz, iso, t):
        I.isla(lz, iso, -60, -60, 520, 420, color_top=(176, 190, 118), t=t, seed=121, esp=38)
        DC.parches(lz, iso, -60, -60, 520, 420, (176, 190, 118), n=14, var=20, seed=122, alfa=0.5, tam=(40, 90))
        I.suelo_curvo(lz, iso, [(0, 80), (460, 80), (470, 360), (-10, 370)], (220, 202, 160), n=4)
        I.cuadricula(lz, iso, 0, 80, 460, 360, 28, color=(255, 255, 255), alfa=0.14)
        I.camino(lz, iso, [(470, 230), (560, 230), (640, 180)], 40, (226, 204, 156), borde=(200, 176, 130))

    def objetos(self, t):
        self._t = t
        if self._est is None:
            m = I.Mundo()
            A.casa_colonial(m, 40, -10, 140, 70, 56, muro=(244, 232, 210), techo=A.TEJA, eje="x", ventanas=4, balcon=False, seed=301)
            A.casa_colonial(m, 250, -10, 170, 70, 56, muro=(240, 226, 200), techo=A.TEJA2, eje="x", ventanas=5, balcon=True, seed=302)
            for i, x in enumerate((200, 440)):
                m.add(x - 4, 10, x + 4, 20, 100, (lambda x: (lambda lz, iso: O2.faro_bandera(lz, iso, x, 30, color=(206, 56, 70), t=self._t, h=72)))(x), clave=x + 40)
            for i in range(5):
                B.tienda_campana(m, 20 + i * 86, 390, color=(250, 244, 232), franja=(206, 70, 70), bandera=(206, 56, 70), t_fn=lambda: self._t)
            for i in range(4):
                B.canon(m, 40 + i * 54, 330, dir=1, t_fn=lambda: self._t)
            DC.bosque(m, -60, -60, 520, 420, n=8, seed=123, evitar=((0, 60, 470, 380),), t_fn=lambda: self._t, tipos=("arbol", "cipres"))
            self._est = m
        m = I.Mundo()
        m.fijos = list(self._est.fijos)
        return m
