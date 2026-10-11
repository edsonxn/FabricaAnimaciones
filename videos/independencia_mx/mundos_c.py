# -*- coding: utf-8 -*-
"""Mundos de la pirámide social (escena 2): tres islas grandes y densas, cada una con su propia vida.
AltoPoder (peninsulares), CiudadCriolla (criollos) y PuebloTrabajo (indígenas, mestizos y esclavos). Coordenadas locales 0..420."""
import math

import numpy as np

import kz_iso as I
import kz_iso_obj as O
import kz_iso_obj2 as O2
import kz_iso_arq as A
import kz_iso_arq2 as B
import kz_gente_iso as G
import kz_iso_deco as DC
import plano as P
from motor import h01, circulo, elipse, rect_red

N = 420.0


class _Isla:
    COLOR = (150, 190, 100)
    SEED = 1
    ESP = 36

    def __init__(self):
        self._est = None
        self._t = 0.0

    def isla(self, lz, iso, t, sombra=True):
        I.isla(lz, iso, 0, 0, N, N, color_top=self.COLOR, t=t, seed=self.SEED, esp=self.ESP, sombra=sombra)
        DC.parches(lz, iso, 0, 0, N, N, self.COLOR, n=16, var=22, seed=self.SEED + 3, alfa=0.5, tam=(40, 90))

    def objetos(self, t):
        self._t = t
        if self._est is None:
            self._est = self._construir()
        m = I.Mundo()
        m.fijos = list(self._est.fijos)
        self._vivo(m, t)
        return m


class AltoPoder(_Isla):
    """Isla de los peninsulares: palacio con balcón, plaza de mármol rosa con fuente, jardines con cipreses, banderas de la Corona, carruaje de gala y nobles de peluca brindando."""
    COLOR = (214, 190, 120)
    SEED = 21

    def suelo(self, lz, iso, t):
        self.isla(lz, iso, t)
        I.suelo_curvo(lz, iso, [(30, 20), (390, 20), (400, 300), (20, 310)], (236, 214, 176))
        I.suelo_rect(lz, iso, 110, 120, 200, 180, (246, 226, 200))
        I.cuadricula(lz, iso, 110, 120, 310, 300, 20, color=(255, 255, 255), alfa=0.22)
        I.camino(lz, iso, [(210, 20), (210, 120), (210, 330), (210, 440)], 34, (252, 236, 210), borde=(226, 200, 164))
        for (a, b, c, d) in ((30, 140, 100, 300), (320, 140, 400, 300)):
            DC.campos(lz, iso, a, b, c, d, nx=1, ny=3, seed=a, t=t, colores=[(150, 200, 120), (130, 190, 110)], setos=True)
        DC.hierba(lz, iso, 0, 0, N, N, n=170, seed=4, t=t, color=(120, 176, 100), flores=0.2)

    def _construir(self):
        m = I.Mundo()
        B.palacio(m, 70, 14, w=290, d=60, h=70, muro=(238, 130, 104), campana=True)
        for x in (80, 200, 330):
            m.add(x - 3, 90, x + 3, 96, 80, (lambda x: (lambda lz, iso: O2.faro_bandera(lz, iso, x, 96, t=self._t, h=100)))(x))
        m.add(204, 204, 216, 216, 40, lambda lz, iso: O.fuente(lz, iso, 210, 210, t=self._t, s=1.3))
        for i, (x, y) in enumerate(((120, 130), (300, 130), (120, 290), (300, 290), (160, 330), (260, 330))):
            m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y: (lambda lz, iso: O.farol(lz, iso, x, y, encendido=0.0)))(x, y))
        for i in range(10):
            for lado in (-1, 1):
                x, y = 210 + lado * 34, 110 + i * 32
                m.add(x - 4, y - 4, x + 4, y + 4, 60, (lambda x, y, i: (lambda lz, iso: O.cipres(lz, iso, x, y, h=52 + 4 * (i % 3), seed=i)))(x, y, i))
        DC.bosque(m, 4, 4, N - 4, N - 4, n=26, seed=51, evitar=((60, 10, 370, 90), (100, 110, 320, 310), (190, 10, 230, 440)), t_fn=lambda: self._t, tipos=("arbol", "cipres", "arbusto"), colores=[(110, 176, 100), (96, 166, 92), (128, 186, 96)])
        for i, (x, y) in enumerate(((60, 160), (60, 230), (360, 160), (360, 230), (70, 370), (350, 370))):
            m.add(x - 8, y - 8, x + 8, y + 8, 30, (lambda x, y, i: (lambda lz, iso: O.arbusto(lz, iso, x, y, r=12, seed=i + 30, flores=(236, 92, 140) if i % 2 else (250, 214, 80))))(x, y, i))
        return m

    def _vivo(self, m, t):
        mu = G.Multitud()
        pos = ((150, 150), (176, 140), (250, 150), (276, 140), (140, 250), (170, 270), (258, 266), (284, 252), (210, 300), (190, 180), (230, 184), (210, 172))
        for i, (x, y) in enumerate(pos):
            mu.quieto((x, y), "peninsular" if i % 4 else "virrey", dir=(0.3, 1) if i % 2 else (-0.3, 1), seed=500 + i, piel=G.PIELES[0] if i % 3 else G.PIELES[1], h=36, accion="habla" if i % 3 == 0 else None)
        mu.camina([(50, 330), (210, 340), (370, 330)], "esclavo", vel=10, seed=70, bucle="ida_vuelta", accion="carga")
        mu.camina([(370, 60), (300, 100), (120, 100), (50, 60)], "esclavo", vel=9, seed=71, bucle="ida_vuelta")
        mu.dibujar(m, t)
        m.add(100, 360, 160, 380, 40, lambda lz, iso: O2.carruaje(lz, iso, 130 + 20 * math.sin(t * 0.2), 372, t, mov=0.0, color=(206, 60, 70), s=1.2), fijo=False, clave=500)
        for i in range(3):
            m.add(200 + 4 * i, 90, 204 + 4 * i, 94, 20, (lambda i: (lambda lz, iso: O.humo(lz, iso, 330 + 20 * i, 30, 70, t, n=4, s=0.9, seed=40 + i)))(i), fijo=False, clave=400 + i)


class CiudadCriolla(_Isla):
    """Isla de los criollos: calle de casas de dos pisos con balcones de colores, café con toldos, mercado, criollos de levita y sombrero de copa, bolsas de dinero sobre mesas."""
    COLOR = (176, 160, 232)
    SEED = 22

    def suelo(self, lz, iso, t):
        self.isla(lz, iso, t)
        I.suelo_curvo(lz, iso, [(20, 20), (400, 20), (400, 400), (20, 400)], (226, 212, 246))
        I.camino(lz, iso, [(-20, 210), (210, 210), (440, 210)], 56, (206, 190, 226), borde=(188, 172, 212))
        I.camino(lz, iso, [(210, -20), (210, 210), (210, 440)], 40, (206, 190, 226), borde=(188, 172, 212))
        I.cuadricula(lz, iso, 20, 20, 400, 400, 22, color=(255, 255, 255), alfa=0.14)
        DC.hierba(lz, iso, 0, 0, N, N, n=70, seed=5, t=t, color=(130, 160, 130), flores=0.1)

    def _construir(self):
        m = I.Mundo()
        muros = [A.CAL, A.OCRE, A.ROSA, A.AZUL, A.VERDE_CAL, (252, 214, 168)]
        for i, (x, y, w, d) in enumerate(((30, 30, 84, 52), (130, 30, 70, 52), (230, 30, 70, 52), (316, 30, 84, 52), (30, 330, 84, 52), (130, 330, 70, 52), (230, 330, 70, 52), (316, 330, 84, 52),
                                          (30, 130, 56, 54), (344, 130, 56, 54), (30, 250, 56, 54), (344, 250, 56, 54))):
            A.casa_colonial(m, x, y, w, d, 62 + 6 * (i % 3), muro=muros[i % 6], techo=[A.TEJA, A.TEJA2, (206, 120, 90)][i % 3], eje="x" if i < 8 else "y", ventanas=3 if w > 60 else 2, balcon=(i % 2 == 0), seed=i,
                            toldo=(236, 90, 96) if i in (4, 6) else None, puerta=True)
        B.portal_arcos(m, 120, 236, 5, paso=22, d=14, h=36, muro=A.CAL) if False else None
        for (x, y, c, cs) in ((140, 136, (236, 90, 96), (250, 190, 70)), (166, 150, (70, 160, 200), (236, 120, 70)), (260, 140, (110, 190, 110), (250, 214, 80)), (286, 154, (250, 150, 70), (236, 90, 130))):
            A.puesto(m, x, y, toldo=c, cosas=cs, seed=int(x))
        for i, (x, y) in enumerate(((100, 186), (320, 186), (100, 240), (320, 240), (150, 300), (270, 300))):
            m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y: (lambda lz, iso: O.farol(lz, iso, x, y, encendido=0.0)))(x, y))
        for i, (x, y) in enumerate(((60, 110), (360, 110), (60, 310), (360, 310), (190, 110), (230, 110))):
            m.add(x - 8, y - 8, x + 8, y + 8, 60, (lambda x, y, i: (lambda lz, iso: O.arbol(lz, iso, x, y, h=48, seed=i + 60, color=(120, 176, 110))))(x, y, i))
        # mesas con bolsas de dinero frente a los cafés
        for i, (x, y) in enumerate(((100, 108), (310, 108), (100, 316), (310, 316))):
            m.add(x - 10, y - 8, x + 14, y + 12, 30, (lambda x, y: (lambda lz, iso: (B.mesa(lz, iso, x - 8, y - 6, 24, 12, 11), O.barril(lz, iso, x + 18, y))))(x, y))
        return m

    def _vivo(self, m, t):
        mu = G.Multitud()
        mu.camina([(-20, 210), (210, 210), (440, 210)], "regidor", vel=14, seed=81, fase=0.1, bucle="ida_vuelta")
        mu.camina([(440, 214), (210, 214), (-20, 214)], "criollo" if False else "regidor", vel=12, seed=82, fase=0.4, bucle="ida_vuelta")
        mu.camina([(210, -20), (210, 210), (210, 440)], "dama", vel=11, seed=83, fase=0.2, bucle="ida_vuelta")
        mu.camina([(214, 440), (214, 210), (214, -20)], "noble", vel=12, seed=84, fase=0.6, bucle="ida_vuelta")
        for i, (x, y) in enumerate(((120, 114), (320, 114), (110, 322), (324, 322), (186, 176), (236, 176), (186, 250), (236, 250))):
            mu.quieto((x, y), "regidor" if i % 2 else "noble", dir=(0.3, 1), seed=600 + i, piel=G.PIELES[i % 2], h=36, accion="habla" if i % 2 else None)
        mu.ronda((210, 210), 80, "dama", n=3, seed=700)
        mu.ronda((210, 210), 90, "nino", n=2, seed=710, h=24)
        mu.dibujar(m, t)
        m.add(60, 200, 100, 230, 40, lambda lz, iso: O2.carruaje(lz, iso, 40 + 340 * ((t * 0.03) % 1.0), 222, t, mov=1.0, color=(70, 110, 190), s=1.1), fijo=False, clave=600)


class PuebloTrabajo(_Isla):
    """Isla de indígenas, mestizos y esclavos: milpas y surcos, chozas, bocamina con vagonetas, malacate, fogatas, arriería, lavanderas en el río y capilla humilde."""
    COLOR = (130, 186, 96)
    SEED = 23

    def suelo(self, lz, iso, t):
        self.isla(lz, iso, t)
        DC.campos(lz, iso, 20, 20, 250, 150, nx=3, ny=2, seed=8, t=t)
        DC.campos(lz, iso, 250, 230, 400, 400, nx=2, ny=2, seed=9, t=t)
        I.suelo_curvo(lz, iso, [(30, 200), (240, 190), (250, 350), (40, 380)], (214, 196, 150))
        I.suelo_curvo(lz, iso, [(270, 30), (400, 40), (410, 190), (280, 200)], (186, 150, 124))
        I.camino(lz, iso, [(-20, 180), (120, 190), (260, 215), (440, 220)], 26, (232, 212, 164), borde=(206, 184, 136))
        DC.acequia(lz, iso, [(0, 390), (110, 410), (220, 380), (330, 410), (440, 396)], t, ancho=20)
        DC.hierba(lz, iso, 0, 0, N, N, n=220, seed=6, t=t)

    def _construir(self):
        m = I.Mundo()
        B.mina(m, 340, 70, t_fn=lambda: self._t, s=1.1)
        B.malacate(m, 300, 130, t_fn=lambda: self._t)
        for i, (x, y, r) in enumerate(((60, 230, 12), (96, 262, 10), (130, 226, 11), (74, 300, 10), (150, 296, 12), (190, 250, 10), (210, 310, 11))):
            B.choza(m, x, y, r=r, h=13, seed=i)
        A.iglesia(m, 270, 250, w=32, largo=44, h_nave=26, muro=(236, 214, 176), techo=(176, 124, 90), torres=1, cupula_c=False)
        DC.bosque(m, 4, 4, N - 4, N - 4, n=34, seed=61, evitar=((20, 20, 250, 150), (30, 190, 250, 380), (250, 230, 400, 400), (270, 30, 410, 200), (0, 170, 440, 230), (0, 370, 440, 420)), t_fn=lambda: self._t,
                  tipos=("arbol", "arbol", "nopal", "maguey", "arbusto"))
        for (x, y) in ((100, 200), (140, 340), (200, 280)):
            m.add(x - 8, y - 8, x + 8, y + 8, 30, (lambda x, y: (lambda lz, iso: O.barril(lz, iso, x, y)))(x, y))
        return m

    def _vivo(self, m, t):
        mu = G.Multitud()
        tipos = ("indigena", "mestizo", "esclavo", "indigena_f", "campesino", "esclavo", "mestizo", "indigena")
        for i in range(8):
            mu.quieto((50 + 28 * (i % 4) * 2 + 10, 40 + 38 * (i // 4) * 2), tipos[i], dir=(1, 0.4), seed=700 + i, piel=G.PIELES[2 + (i % 3)], h=34, accion="trabaja")
        for i in range(6):
            mu.camina([(310 + 8 * i, 78), (350, 100 + 4 * i), (330, 130)], "minero", vel=8 + i, seed=720 + i, bucle="ida_vuelta", accion="trabaja" if i % 2 else "carga")
        mu.camina([(-20, 180), (120, 190), (260, 215), (440, 220)], "arriero", vel=13, seed=5, bucle="ida_vuelta")
        mu.ronda((120, 270), 40, "indigena_f", n=3, seed=740)
        mu.ronda((120, 270), 40, "nino", n=2, seed=750, h=22)
        mu.ronda((330, 390), 40, "indigena_f", n=3, seed=760, accion="trabaja")
        mu.dibujar(m, t)
        O.Caravana([(-20, 180), (120, 190), (260, 215), (440, 220)], n=3, vel=14, fase=0.2, seed=9).dibujar(m, t)
        for (x, y) in ((100, 270), (160, 310)):
            m.add(x - 6, y - 6, x + 6, y + 6, 20, (lambda x, y: (lambda lz, iso: O.fuego(lz, iso, x, y, 1.0, t, seed=int(x))))(x, y), fijo=False, clave=x + y)
        for i in range(4):
            m.add(210 + 8 * i, 330, 216 + 8 * i, 336, 10, (lambda i: (lambda lz, iso: G.gallina(lz, iso, 214 + 9 * i + 2 * math.sin(t * 2 + i), 334 + 4 * math.sin(t * 1.4 + i * 2), t, -1 if i % 2 else 1, seed=i)))(i), fijo=False)
