# -*- coding: utf-8 -*-
"""Mundos isométricos del video (cada lugar con su propio decorado): Dolores, Querétaro, Guanajuato, Ciudad de México, Guadalajara, Cuautla…
Cada mundo es una clase con `suelo(lz, iso, t)` (terreno), `objetos(t)` -> Mundo con lo estático y lo dinámico de ese instante."""
import math

import numpy as np

import kz_iso as I
import kz_iso_obj as O
import kz_iso_arq as A
import kz_iso_arq2 as B
import kz_gente_iso as G
import plano as P
from motor import h01, circulo, elipse, rect_red

PAL_CASAS = [A.CAL, A.OCRE, A.ROSA, A.AZUL, A.VERDE_CAL, (252, 214, 168), (226, 170, 150)]
PAL_TEJA = [A.TEJA, A.TEJA2, (200, 104, 84)]


def _pared(i):
    return PAL_CASAS[int(h01(i, 3) * len(PAL_CASAS)) % len(PAL_CASAS)]


class Dolores:
    """Dolores (hoy Dolores Hidalgo): parroquia de cantera rosa de dos torres con campana, plaza con ahuehuete, casas de adobe con teja, calles, milpas y magueyes."""

    LIM = (-60.0, -60.0, 500.0, 520.0)           # x0, y0, x1, y1 de la isla
    CENTRO = (230.0, 230.0)

    def __init__(self):
        self.iglesia_pos = (180.0, 40.0)
        self.tx_torre = None
        self._estatico = None
        self.torre_belfry = None                  # (x, y, z) del campanario de la torre derecha, para la cámara

    # ------------------------------------------------------------------ terreno
    def suelo(self, lz, iso, t=0.0, isla=True, bob=True):
        x0, y0, x1, y1 = self.LIM
        if isla:
            I.isla(lz, iso, x0, y0, x1, y1, color_top=(128, 190, 96), t=t, seed=3)
        else:
            I.suelo_rect(lz, iso, x0 - 600, y0 - 600, x1 - x0 + 1200, y1 - y0 + 1200, (128, 190, 96))
        # manchas de pasto más claras/oscuras
        for i in range(9):
            cx, cy = x0 + (x1 - x0) * h01(i, 1), y0 + (y1 - y0) * h01(i, 2)
            I.suelo_curvo(lz, iso, [(cx - 50, cy - 30), (cx + 40, cy - 40), (cx + 56, cy + 30), (cx - 30, cy + 44)], (112 + int(24 * h01(i, 4)), 180, 92), alfa=0.55)
        # tierra del pueblo y calles
        I.suelo_curvo(lz, iso, [(-30, -10), (150, -30), (330, -20), (470, 30), (480, 250), (470, 470), (240, 500), (20, 490), (-40, 300)], (212, 196, 140))
        I.camino(lz, iso, [(-70, 372), (120, 372), (260, 378), (520, 372)], 36, (238, 222, 172), borde=(214, 192, 140))
        I.camino(lz, iso, [(96, -70), (96, 140), (98, 372), (96, 530)], 34, (238, 222, 172), borde=(214, 192, 140))
        I.camino(lz, iso, [(362, -70), (360, 150), (362, 372), (364, 530)], 34, (238, 222, 172), borde=(214, 192, 140))
        # plaza empedrada con cuadrícula
        I.suelo_curvo(lz, iso, [(120, 172), (338, 172), (338, 352), (120, 352)], (240, 226, 182), n=4)
        I.cuadricula(lz, iso, 120, 172, 338, 352, 24, color=(255, 255, 255), alfa=0.20)
        # atrio de la iglesia
        I.suelo_rect(lz, iso, 150, 156, 128, 30, (232, 214, 170))

    # ------------------------------------------------------------------ objetos
    def _construir(self):
        m = I.Mundo()
        ix, iy = self.iglesia_pos
        A.iglesia(m, ix, iy, w=70, largo=112, h_nave=60, muro=A.CANTERA, techo=A.TEJA, torres=2, cupula_c=True, campana=lambda: getattr(self, 'ang', 0.0))
        # casas del oeste y este (a lo largo de las calles)
        n = 0
        for yy in range(-10, 330, 62):
            if 120 < yy < 200 and False:
                continue
            for (xx, lado) in ((24, 0), (400, 1)):
                h = 40 + 14 * h01(n, 1)
                w = 54 + 14 * h01(n, 2)
                d = 46 + 10 * h01(n, 3)
                if lado == 0:
                    A.casa_colonial(m, xx - 10, yy, w, d, h, muro=_pared(n), techo=PAL_TEJA[n % 3], eje="y" if n % 2 else "x", ventanas=2, puerta=(n % 3 != 1), balcon=(n % 5 == 0), seed=n,
                                    chimenea=(n % 4 == 0))
                else:
                    A.casa_colonial(m, xx, yy, w, d, h, muro=_pared(n + 4), techo=PAL_TEJA[(n + 1) % 3], eje="x", ventanas=2, seed=n, chimenea=(n % 3 == 0))
                n += 1
        # hilera sur
        for xx in range(-10, 470, 78):
            if 70 < xx < 130 or 330 < xx < 395:
                continue
            h = 38 + 16 * h01(xx, 1)
            A.casa_plana(m, xx, 410, 58 + 10 * h01(xx, 2), 48, h, muro=_pared(xx), acento=PAL_CASAS[(xx // 78 + 3) % 7], ventanas=2, seed=xx)
        A.portal_arcos(m, 150, 356, 5, paso=22, d=14, h=40, muro=A.CAL)
        # la plaza: ahuehuete central, cruz y farolas
        m.add(214, 250, 246, 282, 80, lambda lz, iso: O.arbol(lz, iso, 230, 266, h=96, color=(54, 142, 92), seed=77, sombra=True))
        for (x, y) in ((140, 190), (320, 190), (140, 340), (320, 340)):
            m.add(x - 4, y - 4, x + 4, y + 4, 40, lambda lz, iso, x=x, y=y: O.farol(lz, iso, x, y, encendido=0.0))
        for i, (x, y) in enumerate(((132, 222), (326, 232), (128, 300), (330, 306), (200, 330), (264, 332), (300, 188))):
            m.add(x - 8, y - 8, x + 8, y + 8, 50, lambda lz, iso, x=x, y=y, i=i: O.arbusto(lz, iso, x, y, r=10, seed=i, flores=(236, 92, 140) if i % 2 else None))
        # árboles de las orillas y cipreses
        for i, (x, y) in enumerate(((-20, 40), (-30, 200), (-16, 380), (10, 470), (180, 480), (320, 490), (450, 440), (470, 300), (456, 120), (470, 10), (300, -30), (90, -40), (40, 440), (410, 480))):
            m.add(x - 12, y - 12, x + 12, y + 12, 60, lambda lz, iso, x=x, y=y, i=i: O.arbol(lz, iso, x, y, h=50 + 10 * h01(i, 5), seed=i + 10))
        for i, (x, y) in enumerate(((290, 160), (112, 160), (60, 360))):
            m.add(x - 6, y - 6, x + 6, y + 6, 60, lambda lz, iso, x=x, y=y, i=i: O.cipres(lz, iso, x, y, h=56, seed=i))
        # milpas y magueyes detrás de la iglesia
        m.add(280, -50, 360, 30, 30, lambda lz, iso: O.milpa(lz, iso, 280, -50, 70, 78, t=self._t))
        m.add(-40, -40, 70, 20, 30, lambda lz, iso: O.milpa(lz, iso, -40, -40, 100, 80, t=self._t, color=(100, 176, 84)))
        for i in range(10):
            x, y = 380 + 24 * (i % 5), -34 + 22 * (i // 5)
            m.add(x - 8, y - 8, x + 8, y + 8, 30, lambda lz, iso, x=x, y=y, i=i: O.maguey(lz, iso, x, y, s=0.9, seed=i))
        for i, (x, y) in enumerate(((440, 330), (452, 350), (-30, 330), (-40, 352))):
            m.add(x - 8, y - 8, x + 8, y + 8, 50, lambda lz, iso, x=x, y=y: O.nopal(lz, iso, x, y, s=0.9))
        # corral con ovejas
        for i in range(5):
            m.add(430 + 4 * i, 200, 436 + 4 * i, 206, 10, lambda lz, iso, i=i: G.oveja(lz, iso, 432 + 7 * i + 3 * math.sin(self._t * 0.8 + i), 205 + 6 * (i % 2), self._t, 1, seed=i))
        # humo de las chimeneas (aprox. sobre algunas casas)
        self._fijos = m.fijos
        return m

    def objetos(self, t, campana=None, gente=1.0):
        self._t = t
        if self._estatico is None:
            self._estatico = self._construir()
        m = I.Mundo()
        m.fijos = list(self._estatico.fijos)
        mu = G.Multitud()
        # gente que va y viene por las calles al amanecer (gente=0: pueblo dormido)
        if gente > 0.5:
            self._gente_calle(mu)
        mu.dibujar(m, t)
        self._resto(m, t)
        return m

    def _gente_calle(self, mu):
        mu.camina([(-60, 372), (120, 372), (260, 378), (520, 372)], "campesino", vel=15, seed=1, fase=0.15, bucle="ida_vuelta")
        mu.camina([(520, 372), (300, 376), (120, 372), (-60, 372)], "campesina", vel=12, seed=2, fase=0.35, bucle="ida_vuelta")
        mu.camina([(96, -60), (98, 140), (100, 372), (96, 520)], "arriero", vel=14, seed=3, fase=0.1, bucle="ida_vuelta")
        mu.camina([(364, 520), (362, 372), (360, 150), (362, -60)], "comerciante", vel=13, seed=4, fase=0.5, bucle="ida_vuelta")
        mu.camina([(150, 200), (200, 260), (260, 300), (320, 250)], "indigena", vel=11, seed=5, fase=0.2, bucle="ida_vuelta")
        mu.camina([(330, 300), (250, 320), (180, 300), (140, 240)], "indigena_f", vel=10, seed=6, fase=0.6, bucle="ida_vuelta")
        mu.camina([(120, 340), (300, 340)], "campesina", vel=9, seed=7, fase=0.0, bucle="ida_vuelta")
        mu.ronda((230, 300), 50, "campesino", n=3, seed=40)
        mu.ronda((230, 200), 40, "nino", n=2, seed=50, h=24)

    def _resto(self, m, t):
        # burros de carga y pollos
        m.add(60, 360, 70, 372, 20, lambda lz, iso: G.burro(lz, iso, 40 + 140 * ((t * 0.04) % 1.0), 366, t, dir=1), fijo=False)
        for i in range(4):
            m.add(300 + 8 * i, 300, 306 + 8 * i, 306, 10, lambda lz, iso, i=i: G.gallina(lz, iso, 304 + 9 * i + 2 * math.sin(t * 2 + i), 306 + 4 * math.sin(t * 1.4 + i * 2), t, -1 if i % 2 else 1, seed=i), fijo=False)
        # humo de cocinas
        for (x, y, z) in ((50, 40, 70), (410, 100, 70), (410, 220, 70), (30, 160, 66)):
            m.add(x, y, x + 2, y + 2, 120, lambda lz, iso, x=x, y=y, z=z: O.humo(lz, iso, x, y, z, t, n=5, s=0.9, seed=int(x + y)), fijo=False, clave=x + y + 200)
        return m


class RutaPlata:
    """Isla larga con la mina de plata (arriba a la izquierda), el camino real de las recuas y el puerto con galeones (abajo a la derecha)."""

    LIM = (-120.0, -160.0, 880.0, 460.0)
    RUTA = [(40, 20), (140, 60), (240, 150), (360, 190), (470, 240), (560, 300), (650, 330)]

    def __init__(self):
        self._est = None

    def suelo(self, lz, iso, t=0.0, isla=True):
        x0, y0, x1, y1 = self.LIM
        if isla:
            I.isla(lz, iso, x0, y0, x1, y1, color_top=(168, 192, 100), t=t, seed=5, esp=40)
        else:
            I.suelo_rect(lz, iso, x0 - 600, y0 - 600, x1 - x0 + 1200, y1 - y0 + 1200, (168, 192, 100))
        for i in range(10):
            cx, cy = x0 + (x1 - x0) * h01(i, 11), y0 + (y1 - y0) * h01(i, 12)
            I.suelo_curvo(lz, iso, [(cx - 70, cy - 40), (cx + 60, cy - 50), (cx + 76, cy + 40), (cx - 40, cy + 56)], (150 + int(30 * h01(i, 14)), 184, 92), alfa=0.5)
        I.suelo_curvo(lz, iso, [(-60, -90), (130, -110), (220, -40), (200, 90), (40, 120), (-80, 60)], (186, 150, 124))          # explanada de la mina (tierra y roca)
        I.camino(lz, iso, self.RUTA, 34, (232, 208, 160), borde=(206, 180, 132))
        # mar a la derecha-abajo
        O.agua(lz, iso, [(640, 360), (900, 300), (900, 480), (520, 480), (520, 400)], t, seed=2)
        I.suelo_curvo(lz, iso, [(560, 270), (700, 300), (720, 340), (640, 380), (540, 340)], (230, 212, 160))               # playa del puerto

    def objetos(self, t):
        self._t = t
        if self._est is None:
            m = I.Mundo()
            B.mina(m, 90, -30, t_fn=lambda: self._t, s=1.4)
            B.malacate(m, 20, 70, t_fn=lambda: self._t)
            for i, (x, y) in enumerate(((120, 150), (210, 20), (300, 100), (330, 270), (440, 150), (470, 330), (560, 190), (60, 250), (160, 300), (260, 350), (420, 380), (700, 220))):
                m.add(x - 10, y - 10, x + 10, y + 10, 50, lambda lz, iso, x=x, y=y, i=i: O.arbol(lz, iso, x, y, h=48 + 8 * (i % 3), seed=i + 31))
            for i, (x, y) in enumerate(((180, 110), (300, 230), (410, 130), (520, 210), (90, 190))):
                m.add(x - 8, y - 8, x + 8, y + 8, 40, lambda lz, iso, x=x, y=y, i=i: (O.maguey(lz, iso, x, y, seed=i) if i % 2 else O.nopal(lz, iso, x, y, s=0.9)))
            for i, (x, y) in enumerate(((50, 110), (110, 100), (-30, 40))):
                m.add(x - 6, y - 6, x + 6, y + 6, 20, lambda lz, iso, x=x, y=y, i=i: O.roca(lz, iso, x, y, s=1.0 + 0.2 * i))
            # puerto
            B.muelle(m, 600, 330, largo=110, ancho=16, h=6)
            A.casa_colonial(m, 520, 240, 70, 46, 46, muro=A.CAL, techo=A.TEJA, eje="x", ventanas=3, balcon=True, seed=5)
            A.casa_colonial(m, 590, 280, 54, 40, 40, muro=A.OCRE, techo=A.TEJA2, eje="y", ventanas=2, seed=6)
            for i, (x, y) in enumerate(((580, 300), (600, 306), (612, 296))):
                m.add(x - 6, y - 6, x + 6, y + 6, 14, lambda lz, iso, x=x, y=y, i=i: O.barril(lz, iso, x, y) if i != 1 else O.caja_madera(lz, iso, x, y))
            self._est = m
        m = I.Mundo()
        m.fijos = list(self._est.fijos)
        mu = G.Multitud()
        for i in range(5):
            mu.camina([(60 + 20 * i, 10), (110, 20 + 8 * i), (70, 50)], "minero", vel=9 + i, seed=70 + i, fase=0.0, bucle="ida_vuelta", accion="trabaja" if i % 2 else None)
        mu.camina([(120, 70), (60, 60)], "minero", vel=10, seed=3, bucle="ida_vuelta", accion="carga")
        mu.dibujar(m, t)
        Caravana_ = O.Caravana
        Caravana_(self.RUTA, n=4, vel=16, fase=0.0, seed=1).dibujar(m, t)
        Caravana_(self.RUTA, n=3, vel=14, fase=0.42, seed=8).dibujar(m, t)
        Caravana_(self.RUTA[::-1], n=3, vel=15, fase=0.2, seed=14, carga=False).dibujar(m, t)
        for i in range(6):
            m.add(630 + 14 * (i % 3) - 4, 336 + 4 * i, 640 + 14 * (i % 3), 344 + 4 * i, 20, lambda lz, iso, i=i: G.persona(lz, iso, 628 + 14 * ((i + int(t * 0.8)) % 4), 337 + 5 * (i % 2), t, "campesino", dir=(1, 0), vel=0.9, seed=200 + i, accion="carga"), fijo=False)
        return m
