# -*- coding: utf-8 -*-
"""Mundos de la escena 6 (Guanajuato): la ciudad minera entre cerros con la Alhóndiga de Granaditas, y los campamentos de los dos bandos."""
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

COLORES = [(250, 210, 90), (236, 110, 120), (110, 190, 220), (150, 210, 130), (230, 150, 90), (180, 140, 220), (250, 190, 150), (120, 170, 230)]


# ------------------------------------------------------------------------------------------------ cerros con casitas (fondo en pantalla, con paralaje)
def cerros(lz, cx, cy, t=0.0, tonos=((120, 150, 120), (98, 128, 108), (80, 106, 100)), alturas=(380, 300, 240), casas=True):
    """Tres cerros redondeados con casitas de colores trepando por la ladera (como las laderas de Guanajuato), dibujados detrás del diorama con paralaje."""
    for k, (col, y0) in enumerate(zip(tonos, alturas)):
        px = -cx * (0.05 + 0.04 * k)
        pts = [(-100, 1200)]
        for i in range(0, 21):
            x = -100 + i * 110 + px
            y = y0 + 90 * math.sin(i * 0.9 + k * 2.1) + 50 * math.sin(i * 2.3 + k) - cy * 0.03
            pts.append((x, y))
        pts.append((2100, 1200))
        lz.relleno(np.array(pts, float), col, capa=0)
        if casas:
            for j in range(30):
                x = (h01(81 + k, j, 1) * 2000 - 100)
                xs = x + px
                i = int((xs + 100 - px) / 110)
                ya = y0 + 90 * math.sin(i * 0.9 + k * 2.1) + 50 * math.sin(i * 2.3 + k) - cy * 0.03 + 8 + 70 * h01(83 + k, j, 2)
                c = COLORES[int(h01(85 + k, j, 3) * 8) % 8]
                w, h = 26 - 5 * k, 20 - 4 * k
                lz.relleno(rect_red(xs - w / 2, ya, w, h, 2), P.mezcla(c, col, 0.45), capa=0)
                lz.relleno(np.array([[xs - w / 2 - 2, ya + 1], [xs + w / 2 + 2, ya + 1], [xs, ya - 9 + 2 * k]]), P.mezcla((190, 90, 70), col, 0.40), capa=0)


# ------------------------------------------------------------------------------------------------ la ciudad
class GuanajuatoCiudad:
    """Guanajuato en 1810: plaza empedrada frente a la Alhóndiga de Granaditas (derecha-fondo), casas de colores, la parroquia, el arroyo con puentecitos, las minas con malacate y recuas de mulas con plata."""
    ALH = (230, -10, 170, 130)         # x, y, w, d de la Alhóndiga
    PUERTA = (230 + 85, 120)           # centro del portón (frente, y = y + d - 24 + 24)

    def __init__(self):
        self._est = None
        self._t = 0.0

    def suelo(self, lz, iso, t):
        I.isla(lz, iso, -120, -100, 540, 440, color_top=(176, 184, 124), t=t, seed=91, esp=40)
        DC.parches(lz, iso, -120, -100, 540, 440, (176, 184, 124), n=22, var=22, seed=92, alfa=0.55, tam=(50, 100))
        I.suelo_curvo(lz, iso, [(-30, 100), (440, 100), (470, 300), (-40, 330)], (224, 204, 168))
        I.suelo_rect(lz, iso, 150, 130, 270, 190, (238, 220, 186))
        I.cuadricula(lz, iso, 150, 130, 420, 320, 24, color=(255, 255, 255), alfa=0.20)
        I.camino(lz, iso, [(-120, 250), (150, 250)], 46, (232, 214, 178))
        I.camino(lz, iso, [(420, 250), (540, 250)], 46, (232, 214, 178))
        I.camino(lz, iso, [(280, 320), (280, 440)], 40, (232, 214, 178))
        # arroyo con corriente (al frente) y entrada de las minas (tierra oscura a la izquierda)
        DC.acequia(lz, iso, [(-110, 360), (100, 372), (300, 366), (540, 376)], t, ancho=16.0)
        I.suelo_curvo(lz, iso, [(-110, -80), (60, -90), (90, 40), (-100, 70)], (150, 126, 108))

    def objetos(self, t, gente=1.0):
        self._t = t
        if self._est is None:
            m = I.Mundo()
            x, y, w, d = self.ALH
            B.alhondiga(m, x, y, w=w, d=d, h=84, t_fn=lambda: self._t, puerta_fuego=0.0)
            A.iglesia(m, 60, 20, w=70, largo=96, h_nave=58, muro=(244, 214, 150), techo=A.TEJA2, torres=2, cupula_c=True)
            pal = [A.CAL, A.OCRE, A.ROSA, A.AZUL, A.VERDE_CAL, (214, 170, 236), (252, 214, 120)]
            for i in range(5):                                       # calle izquierda
                A.casa_colonial(m, -60, 110 + i * 44, 64, 40, 44 + 8 * (i % 3), muro=pal[i], techo=A.TEJA if i % 2 else A.TEJA2, eje="x", ventanas=2, balcon=(i % 2 == 0), seed=i + 200)
            for i in range(4):                                       # calle derecha
                A.casa_colonial(m, 424, 120 + i * 50, 56, 44, 44 + 6 * (i % 2), muro=pal[(i + 3) % 7], techo=A.TEJA, eje="x", ventanas=2, balcon=(i % 2 == 1), seed=i + 220)
            for i in range(7):                                       # hilera sur junto al arroyo
                A.casa_plana(m, -40 + i * 78, 392, 62, 40, 40 + 6 * (i % 3), muro=pal[(i + 1) % 7], acento=pal[(i + 4) % 7], seed=i + 240)
            B.mina(m, -80, -40, t_fn=lambda: self._t, s=1.0)
            B.malacate(m, 10, 40, t_fn=lambda: self._t, mula=True, s=1.0)
            for i, (px, py) in enumerate(((-20, 50), (-4, 60), (-30, 70))):
                m.add(px - 6, py - 6, px + 6, py + 6, 20, (lambda px, py, i: (lambda lz, iso: O2.pila_lingotes(lz, iso, px, py, n=4 + i, s=0.9, t=self._t)))(px, py, i), clave=px + py + 1)
            for (x_, y_) in ((170, 142), (410, 142), (170, 310), (410, 310), (280, 150), (280, 300)):
                m.add(x_ - 4, y_ - 4, x_ + 4, y_ + 4, 40, (lambda x_, y_: (lambda lz, iso: O.farol(lz, iso, x_, y_, encendido=0.0)))(x_, y_), clave=x_ + y_)
            m.add(266, 214, 294, 242, 40, lambda lz, iso: O.fuente(lz, iso, 280, 228, t=self._t, s=1.2), clave=508)
            for i, (px, py) in enumerate(((190, 280), (370, 276), (200, 180), (360, 186))):
                A.puesto(m, px, py, toldo=[(236, 90, 96), (70, 160, 200), (110, 190, 110), (250, 150, 70)][i], cosas=[(250, 190, 70), (236, 120, 70)][i % 2], seed=i)
            B.puente_piedra(m, 250, 352, largo=60, ancho=26, h=14, arcos=2) if False else None
            DC.bosque(m, -120, -100, 540, 440, n=10, seed=93, evitar=((-120, -100, 100, 100), (-70, 100, 130, 360), (150, 100, 440, 330), (410, 100, 520, 330), (-60, 380, 520, 440), (50, 10, 140, 130), (220, -20, 410, 120)), t_fn=lambda: self._t, tipos=("arbol", "cipres", "nopal"))
            self._est = m
        m = I.Mundo()
        m.fijos = list(self._est.fijos)
        if gente > 0.01:
            mu = G.Multitud()
            tipos = ("campesino", "campesina", "minero", "mestizo", "comerciante", "arriero", "indigena", "nino")
            mu.camina([(-120, 252), (150, 252), (280, 252), (420, 252), (540, 252)], "arriero", vel=13, seed=1, bucle="ida_vuelta")
            for i in range(int(14 * gente)):
                mu.ronda((200 + 17 * i, 220 + 20 * (i % 3)), 40, tipos[i % 8], n=1, seed=3300 + i * 5, h=40 if tipos[i % 8] != "nino" else 28)
            mu.dibujar(m, t)
            O.Caravana([(-120, 262), (150, 262), (300, 262), (540, 262)], n=3, vel=14, fase=0.3, seed=21).dibujar(m, t)
        return m


# ------------------------------------------------------------------------------------------------ campamentos de los dos bandos
class Campamentos:
    """Valle abierto con dos campamentos frente a frente: a la izquierda los insurgentes (tiendas y el estandarte guadalupano), a la derecha los realistas (tiendas con la bandera de la Corona)."""

    def __init__(self):
        self._est = None
        self._t = 0.0

    def suelo(self, lz, iso, t):
        I.isla(lz, iso, -60, -60, 520, 380, color_top=(176, 196, 116), t=t, seed=95, esp=38)
        DC.parches(lz, iso, -60, -60, 520, 380, (176, 196, 116), n=16, var=22, seed=96, alfa=0.5, tam=(40, 90))
        I.suelo_curvo(lz, iso, [(10, 40), (170, 30), (180, 320), (0, 330)], (214, 196, 148))
        I.suelo_curvo(lz, iso, [(280, 40), (450, 30), (460, 320), (270, 330)], (208, 200, 168))
        I.camino(lz, iso, [(170, 180), (230, 190), (290, 180)], 40, (226, 204, 156), borde=(200, 176, 130))

    def objetos(self, t):
        self._t = t
        if self._est is None:
            m = I.Mundo()
            for i, (x, y) in enumerate(((20, 60), (60, 120), (30, 190), (80, 250), (120, 70), (120, 200))):
                B.tienda_campana(m, x, y, color=(246, 238, 220), franja=(70, 160, 110), bandera=(70, 160, 110), t_fn=lambda: self._t)
            for i, (x, y) in enumerate(((330, 60), (390, 120), (340, 190), (400, 250), (310, 240), (420, 60))):
                B.tienda_campana(m, x, y, color=(250, 244, 232), franja=(206, 70, 70), bandera=(206, 56, 70), t_fn=lambda: self._t)
            m.add(170, 120, 180, 130, 90, lambda lz, iso: O2.estandarte_virgen(lz, iso, 150, 118, h=50, t=self._t, w=32, alto=44), clave=270)
            m.add(300, 120, 310, 130, 90, lambda lz, iso: O2.faro_bandera(lz, iso, 316, 118, color=(206, 56, 70), t=self._t, h=70), clave=434)
            for (x, y) in ((70, 40), (130, 150), (30, 290), (90, 210)):
                m.add(x - 6, y - 6, x + 6, y + 6, 20, (lambda x, y: (lambda lz, iso: O.fuego(lz, iso, x, y, 0.9, self._t, seed=int(x), halo=True)))(x, y), clave=x + y + 3)
            for (x, y) in ((350, 150), (370, 300), (420, 190)):
                m.add(x - 6, y - 6, x + 6, y + 6, 20, (lambda x, y: (lambda lz, iso: O.fuego(lz, iso, x, y, 0.9, self._t, seed=int(x), halo=True)))(x, y), clave=x + y + 3)
            DC.bosque(m, -60, -60, 520, 380, n=12, seed=97, evitar=((0, 30, 190, 340), (260, 30, 470, 340)), t_fn=lambda: self._t, tipos=("arbol", "cipres", "nopal"))
            self._est = m
        m = I.Mundo()
        m.fijos = list(self._est.fijos)
        return m
