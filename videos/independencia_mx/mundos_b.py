# -*- coding: utf-8 -*-
"""Mundos isométricos de la escena 2 (Nueva España) con densidad automática: la ruta de la plata, la hacienda y el pueblo arruinado."""
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
from motor import h01, circulo, elipse, rect_red


class RutaPlata:
    """Isla larga con la mina de plata (arriba a la izquierda), el camino real de las recuas y el puerto con galeones (abajo a la derecha). Densa: campos, bosques, aldea, río."""

    LIM = (-160.0, -200.0, 1000.0, 660.0)
    RUTA = [(40, 20), (140, 60), (240, 150), (360, 190), (470, 240), (560, 300), (650, 330)]

    def __init__(self):
        self._est = None

    def suelo(self, lz, iso, t=0.0, isla=True):
        x0, y0, x1, y1 = self.LIM
        if isla:
            I.isla(lz, iso, x0, y0, x1, y1, color_top=(160, 190, 98), t=t, seed=5, esp=40)
        else:
            I.suelo_rect(lz, iso, x0 - 600, y0 - 600, x1 - x0 + 1200, y1 - y0 + 1200, (160, 190, 98))
        DC.parches(lz, iso, x0, y0, x1, y1, (160, 190, 98), n=26, var=26, seed=3, alfa=0.55, tam=(50, 110))
        DC.campos(lz, iso, 250, -30, 520, 120, nx=4, ny=2, seed=2, t=t)
        DC.campos(lz, iso, 60, 230, 330, 420, nx=4, ny=3, seed=7, t=t)
        DC.campos(lz, iso, 700, 60, 860, 230, nx=2, ny=2, seed=4, t=t)
        I.suelo_curvo(lz, iso, [(-90, -110), (140, -130), (240, -50), (220, 100), (40, 130), (-100, 70)], (186, 150, 124))
        I.suelo_curvo(lz, iso, [(-60, -80), (110, -100), (200, -40), (180, 70), (30, 100), (-70, 50)], (206, 172, 140), alfa=0.8)
        I.camino(lz, iso, self.RUTA, 34, (232, 208, 160), borde=(206, 180, 132))
        I.camino(lz, iso, [(300, 190), (330, 330), (300, 470)], 20, (232, 208, 160), borde=(206, 180, 132))
        DC.acequia(lz, iso, [(-160, 300), (-20, 290), (120, 330), (260, 300), (400, 340), (560, 420), (700, 470)], t, ancho=22)
        I.suelo_curvo(lz, iso, [(520, 250), (700, 280), (900, 330), (1000, 420), (1000, 560), (860, 650), (640, 640), (500, 540), (470, 400)], (236, 218, 168))     # playa
        O.bahia(lz, iso, [(560, 380), (640, 330), (720, 350), (800, 330), (900, 350), (980, 420), (950, 500), (990, 570), (900, 630), (780, 600), (700, 640), (600, 590), (540, 520), (520, 440)], t, seed=2)
        DC.hierba(lz, iso, x0, y0, x1, y1, n=300, seed=9, t=t)

    def objetos(self, t):
        self._t = t
        if self._est is None:
            m = I.Mundo()
            B.mina(m, 90, -30, t_fn=lambda: self._t, s=1.4)
            B.malacate(m, 20, 70, t_fn=lambda: self._t)
            B.choza(m, 160, -70, r=11, h=14, seed=3)
            B.choza(m, 190, -52, r=10, h=13, seed=4)
            B.tienda_campana(m, 130, 100, color=(238, 220, 190), franja=(120, 80, 60))
            ev = ((-100, -150, 260, 140), (230, 120, 620, 270), (560, 250, 760, 380), (-160, 280, 320, 340), (250, -30, 520, 120), (60, 230, 330, 420), (700, 60, 860, 230), (500, 300, 1010, 670))
            DC.bosque(m, -150, -190, 880, 500, n=64, seed=11, evitar=ev, t_fn=lambda: self._t, tipos=("arbol", "arbol", "pino", "arbusto", "nopal", "maguey", "roca"))
            for (x, y) in ((600, 150), (700, 250), (780, 120)):
                A.casa_colonial(m, x, y, 56, 40, 40, muro=A.CAL, techo=A.TEJA, eje="x", ventanas=2, seed=int(x))
            B.muelle(m, 676, 338, largo=112, ancho=16, h=6, eje="y")
            A.casa_colonial(m, 520, 240, 70, 46, 46, muro=A.CAL, techo=A.TEJA, eje="x", ventanas=3, balcon=True, seed=5)
            A.casa_colonial(m, 590, 280, 54, 40, 40, muro=A.OCRE, techo=A.TEJA2, eje="y", ventanas=2, seed=6)
            A.casa_plana(m, 480, 300, 44, 36, 34, muro=A.ROSA, acento=A.AZUL)
            A.iglesia(m, 430, 160, w=34, largo=46, h_nave=30, muro=A.CANTERA, torres=1, cupula_c=False)
            for i, (x, y) in enumerate(((652, 314), (708, 322), (722, 336), (640, 330))):
                m.add(x - 6, y - 6, x + 6, y + 6, 14, (lambda x, y, i: (lambda lz, iso: O.barril(lz, iso, x, y) if i % 2 else O.caja_madera(lz, iso, x, y)))(x, y, i))
            for i, (x, y) in enumerate(((100, 50), (60, 90), (150, 20), (30, -60))):
                m.add(x - 8, y - 8, x + 8, y + 8, 20, (lambda x, y, i: (lambda lz, iso: O.roca(lz, iso, x, y, s=1.1 + 0.2 * i, seed=i)))(x, y, i))
            self._est = m
        m = I.Mundo()
        m.topo = True
        m.fijos = list(self._est.fijos)
        mu = G.Multitud()
        for i in range(7):
            mu.camina([(60 + 18 * i, 10), (110, 20 + 7 * i), (70, 56)], "minero", vel=9 + i, seed=70 + i, fase=0.0, bucle="ida_vuelta", accion="trabaja" if i % 2 else None)
        mu.camina([(120, 70), (60, 60)], "minero", vel=10, seed=3, bucle="ida_vuelta", accion="carga")
        mu.ronda((380, 40), 60, "campesino", n=4, seed=300, accion="trabaja")
        mu.ronda((200, 330), 70, "campesina", n=3, seed=330, accion="trabaja")
        mu.ronda((760, 150), 40, "campesino", n=3, seed=360, accion="trabaja")
        mu.ronda((540, 270), 40, "comerciante", n=3, seed=390)
        mu.dibujar(m, t)
        O.Caravana(self.RUTA, n=4, vel=16, fase=0.0, seed=1).dibujar(m, t)
        O.Caravana(self.RUTA, n=3, vel=14, fase=0.42, seed=8).dibujar(m, t)
        O.Caravana(self.RUTA[::-1], n=3, vel=15, fase=0.2, seed=14, carga=False).dibujar(m, t)
        O.Caravana([(300, 190), (330, 330), (300, 470)], n=2, vel=13, fase=0.3, seed=24).dibujar(m, t)
        mu2 = G.Multitud()
        for i in range(4):                                         # estibadores que suben y bajan por el muelle (carril izquierdo/derecho, fases repartidas)
            mu2.camina([(680 + 8 * (i % 2), 346), (680 + 8 * (i % 2), 440)], "campesino", vel=7.0, fase=i * 0.27, seed=200 + i, bucle="ida_vuelta", accion="carga")
        mu2.dibujar(m, t)
        for i in range(5):
            m.add(460 + 6 * i, 100, 466 + 6 * i, 106, 10, (lambda i: (lambda lz, iso: G.oveja(lz, iso, 466 + 8 * i + 3 * math.sin(t * 0.8 + i), 110 + 6 * (i % 2), t, 1, seed=i)))(i), fijo=False)
        return m


class Hacienda:
    """Hacienda de la Nueva España: casa grande con portal, capilla, trojes, corral, huertos y el camino real."""

    def __init__(self):
        self._est = None

    def suelo(self, lz, iso, t):
        I.isla(lz, iso, -120, -120, 420, 340, color_top=(160, 196, 104), t=t, seed=7, esp=36)
        DC.parches(lz, iso, -120, -120, 420, 340, (160, 196, 104), n=18, var=24, seed=21, alfa=0.55, tam=(40, 90))
        I.suelo_curvo(lz, iso, [(-30, -30), (330, -30), (340, 260), (-30, 270)], (216, 198, 150))
        I.suelo_rect(lz, iso, 40, 130, 150, 90, (240, 226, 182))
        I.cuadricula(lz, iso, 40, 130, 190, 220, 18, color=(255, 255, 255), alfa=0.16)
        I.camino(lz, iso, [(-120, 230), (60, 220), (180, 240), (300, 250), (440, 270)], 36, (238, 222, 172), borde=(214, 192, 140))
        DC.campos(lz, iso, 220, -20, 410, 110, nx=3, ny=2, seed=5, t=t)
        DC.campos(lz, iso, -100, 100, 20, 250, nx=1, ny=2, seed=8, t=t)
        DC.hierba(lz, iso, -120, -120, 420, 340, n=240, seed=3, t=t)

    def objetos(self, t):
        self._t = t
        if self._est is None:
            m = I.Mundo()
            A.hacienda(m, 10, -10, w=170, d=120, capilla=True)
            for i, (x, y) in enumerate(((200, 150), (236, 150), (272, 150))):
                A.casa_plana(m, x, y, 30, 26, 24, muro=(240, 214, 160), acento=(176, 120, 80), ventanas=1)
            for i, (x, y) in enumerate(((16, 150), (30, 160), (44, 150), (22, 176))):
                m.add(x - 6, y - 6, x + 6, y + 6, 14, (lambda x, y, i: (lambda lz, iso: O.barril(lz, iso, x, y) if i % 2 else O2.cofre(lz, iso, x, y, 0.9)))(x, y, i))
            DC.bosque(m, -110, -110, 410, 330, n=34, seed=31, evitar=((0, -20, 200, 130), (30, 120, 200, 230), (190, 140, 300, 190), (220, -20, 410, 110), (-100, 100, 20, 250), (-120, 200, 440, 270)), t_fn=lambda: self._t,
                      tipos=("arbol", "arbol", "arbusto", "cipres", "maguey"))
            self._est = m
        m = I.Mundo()
        m.fijos = list(self._est.fijos)
        mu = G.Multitud()
        mu.ronda((120, 180), 40, "campesino", n=3, seed=410)
        mu.ronda((310, 40), 40, "campesina", n=3, seed=430, accion="trabaja")
        mu.camina([(-120, 230), (60, 220), (180, 240), (300, 250), (440, 270)], "arriero", vel=13, seed=5, fase=0.0, bucle="ida_vuelta")
        mu.dibujar(m, t)
        O.Caravana([(440, 270), (300, 250), (180, 240), (60, 220), (-120, 230)], n=3, vel=14, fase=0.2, seed=9).dibujar(m, t)
        return m


class PuebloRuina:
    """Pueblo de calle principal con casas en venta y tapiadas, un éxodo de familias con bultos y carretas cargadas, y el campo de tierra donde brotan las plantas del descontento."""

    def __init__(self):
        self._est = None

    def suelo(self, lz, iso, t):
        I.isla(lz, iso, -160, -120, 520, 380, color_top=(150, 168, 120), t=t, seed=9, esp=36)
        DC.parches(lz, iso, -160, -120, 520, 380, (150, 168, 120), n=16, var=20, seed=17, alfa=0.55, tam=(40, 90))
        I.suelo_curvo(lz, iso, [(-60, -20), (400, -20), (410, 300), (-60, 310)], (200, 184, 150))
        I.camino(lz, iso, [(-160, 150), (120, 150), (240, 160), (520, 170)], 46, (224, 206, 160), borde=(200, 180, 140))
        I.suelo_rect(lz, iso, 40, 200, 260, 100, (150, 112, 84))
        for k in range(6):
            I.suelo_rect(lz, iso, 40, 210 + k * 16, 260, 3.2, (126, 92, 70), alfa=0.8)
        DC.hierba(lz, iso, -160, -120, 520, 380, n=120, seed=6, t=t, color=(128, 150, 100), flores=0.04)

    def objetos(self, t):
        self._t = t
        if self._est is None:
            m = I.Mundo()
            for i, (x, y, w, d) in enumerate(((-40, -10, 70, 50), (46, -10, 64, 50), (126, -10, 70, 50), (210, -10, 60, 50), (290, -10, 70, 50), (-30, 96, 66, 50), (56, 96, 64, 50), (140, 100, 68, 50), (230, 100, 66, 48), (310, 100, 60, 48))):
                A.casa_colonial(m, x, y, w, d, 42 + 6 * (i % 3), muro=[A.CAL, A.OCRE, A.ROSA, A.VERDE_CAL][i % 4], techo=A.TEJA2, eje="x", ventanas=2, seed=i, puerta=(i % 3 != 2))
                # ventanas tapiadas con tablones
                m.add(x, y + d, x + w, y + d + 4, 60, (lambda x, y, w, d: (lambda lz, iso: _tablones(lz, iso, x, y + d, w)))(x, y, w, d), clave=x + y + d + w)
            DC.bosque(m, -150, -110, 510, 370, n=22, seed=41, evitar=((-60, -20, 400, 160), (40, 200, 300, 300), (-160, 120, 520, 190)), t_fn=lambda: self._t, tipos=("arbol", "arbusto", "cipres"),
                      colores=[(110, 150, 100), (96, 136, 96), (128, 156, 104)])
            self._est = m
        m = I.Mundo()
        m.topo = True
        m.fijos = list(self._est.fijos)
        mu = G.Multitud()
        # éxodo de familias: caminan de izquierda a derecha por la calle, cada una a su ritmo, cargando bultos
        tipos = ("campesino", "campesina", "nino", "campesina", "campesino", "nino", "indigena_f", "mestizo", "nino", "campesina")
        for i in range(10):
            mu.camina([(-170, 148 + 6 * (i % 3)), (130, 152 + 6 * (i % 3)), (260, 162 + 6 * (i % 3)), (540, 172 + 6 * (i % 3))], tipos[i], vel=9 + 1.2 * (i % 4), seed=980 + i, fase=0.04 * i, bucle=True, h=44 if tipos[i] != "nino" else 30,
                    accion="carga" if i % 3 == 0 else None)
        mu.quieto((20, 80), "campesina", dir=(0, 1), seed=990, h=44, accion="habla")
        mu.quieto((30, 86), "nino", dir=(0, 1), seed=991, h=30)
        mu.quieto((166, 86), "campesino", dir=(0, 1), seed=992, h=44)
        mu.dibujar(m, t)
        for k, (fase, bul) in enumerate(((0.10, True), (0.42, True), (0.74, True))):
            cx_, cy_ = -170 + 710 * ((t * 0.034 + fase) % 1.0), 156 + 4 * k
            m.add(cx_ - 14, cy_ - 8, cx_ + 14, cy_ + 8, 30, (lambda cx_, cy_: (lambda lz, iso: O.carreta(lz, iso, cx_, cy_, t, mov=1.0, s=1.35, bultos=True)))(cx_, cy_), fijo=False, clave=cx_ + cy_)
        px_ = -170 + 710 * ((t * 0.05 + 0.2) % 1.0)
        m.add(px_ - 6, 184, px_ + 6, 196, 20, (lambda px_: (lambda lz, iso: _perro(lz, iso, px_, 190, t)))(px_), fijo=False, clave=px_ + 190)
        return m


def _tablones(lz, iso, x, y, w):
    """Tablones clavados cruzados sobre la fachada (casa abandonada)."""
    k = iso.z
    for (a, b, c, d) in ((0.2, 14, 0.8, 30), (0.2, 30, 0.8, 14)):
        p0 = iso.P(x + w * a, y, b)
        p1 = iso.P(x + w * c, y, d)
        _tira2(lz, p0, p1, 2.6 * k, (126, 90, 66))
    p0, p1 = iso.P(x + w * 0.5, y, 40), iso.P(x + w * 0.5, y, 8)
    _tira2(lz, p0, p1, 2.4 * k, (110, 78, 58))


def _tira2(lz, p0, p1, ancho, color):
    d = np.array([p1[0] - p0[0], p1[1] - p0[1]], float)
    L = float(np.hypot(*d))
    if L < 1e-6:
        return
    n = np.array([-d[1], d[0]]) / L * ancho / 2
    a, b = np.array([float(p0[0]), float(p0[1])]), np.array([float(p1[0]), float(p1[1])])
    lz.relleno(np.array([a + n, b + n, b - n, a - n]), color)


def _perro(lz, iso, x, y, t):
    sx, sy = iso.P(x, y, 0)
    k = iso.z
    I.sombra_elipse(lz, iso, x + 1, y + 0.6, 6, 3, 0.2)
    ph = t * 9
    for dx, f in ((-5, 0.0), (-2, math.pi), (4, math.pi), (7, 0.0)):
        lz.relleno(rect_red(sx + (dx - 0.8) * k + math.sin(ph + f) * 1.4 * k, sy - 4.5 * k, 1.6 * k, 4.5 * k, 0.5 * k), tint((120, 86, 62)))
    lz.relleno(elipse(sx, sy - 6 * k, 8 * k, 3.6 * k, 0, 12), tint((170, 124, 86)))
    lz.relleno(circulo(sx + 8.5 * k, sy - 8 * k, 3 * k, 8), tint((170, 124, 86)))
    lz.relleno(np.array([[sx + 9 * k, sy - 11 * k], [sx + 11 * k, sy - 14.5 * k], [sx + 12 * k, sy - 10 * k]]), tint((120, 86, 62)))
    lz.relleno(np.array([[sx - 8 * k, sy - 7 * k], [sx - 12 * k, sy - 11 * k + math.sin(t * 12) * 2 * k], [sx - 9 * k, sy - 5 * k]]), tint((170, 124, 86)))
