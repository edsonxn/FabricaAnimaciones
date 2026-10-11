# -*- coding: utf-8 -*-
"""Mundos de la escena 5 (el Grito): la casa del cura (interior), el camino de la marcha insurgente y las tierras del pueblo frente a la hacienda."""
import math

import numpy as np

import kz_iso as I
from kz_iso import tint
import kz_iso_obj as O
import kz_iso_obj2 as O2
import kz_iso_arq as A
import kz_iso_arq2 as B
import kz_iso_int as N
import kz_gente_iso as G
import kz_iso_deco as DC
import plano as P
from motor import h01, circulo, elipse, rect_red, catmull
import mundos_e as me


# ------------------------------------------------------------------------------------------------ interior: casa del cura
def casa_cural(lz, iso, t, W_=290, D_=240, H_=140, alba=0.0):
    """Cuarto sencillo de la casa del cura de Dolores en la madrugada: cruz de madera, ventana con cielo que va aclarando, cama, mesa con velas y libros, estante y baúl."""
    c = I.habitacion(lz, iso, 0, 0, W_, D_, H_, piso=(176, 136, 104), pared_a=(244, 232, 206), pared_b=(232, 216, 190), friso=(150, 108, 84))
    for i in range(int(W_ / 34)):
        for j in range(int(D_ / 34)):
            if (i + j) % 2:
                I.suelo_rect(lz, iso, 8 + i * 34, 8 + j * 34, 34, 34, (150, 110, 84), z=0.1, alfa=0.5)
    cielo = tuple(int(a + (b - a) * alba) for a, b in zip((44, 52, 120), (250, 176, 150)))
    N.ventana_vista(lz, iso, c, "yi", 100, 186, 40, 118, t=t, cielo=cielo, marco=(240, 226, 200), cortinas=(150, 110, 80), vista="ciudad")
    # crucifijo y cuadro de la Virgen en la pared izquierda
    I.cara_rect(lz, iso, c, "yi", 46, 52, 58, 108, (104, 66, 48))
    I.cara_rect(lz, iso, c, "yi", 38, 60, 88, 94, (104, 66, 48))
    B.cuadro_pared(lz, iso, c, "yi", 214, 66, 30, 40, color=(60, 130, 130))
    # pared derecha: puerta de la calle (arco), mapa y estante
    I.cara_arco(lz, iso, c, "xi", 150, 206, 0, 98, (110, 74, 54))
    N.cortina(lz, iso, c, "xi", 30, 44, 0, 110, (150, 110, 80), t)
    B.cuadro_pared(lz, iso, c, "xi", 80, 64, 34, 30, color=(190, 150, 90))
    return c


def amueblar_casa_cural(m, t):
    m.add(20, 30, 80, 66, 40, lambda lz, iso: me.cama(lz, iso, 20, 30, t, (150, 110, 80)), clave=90)
    m.add(100, 100, 200, 160, 24, lambda lz, iso: _mesa_cura(lz, iso, t), clave=260)
    for (x, y) in ((92, 110), (92, 138), (204, 118)):
        m.add(x, y, x + 10, y + 10, 12, (lambda x, y: (lambda lz, iso: B.silla(lz, iso, x, y, 12, (120, 80, 58))))(x, y), clave=x + y + 2)
    m.add(200, 8, 244, 22, 70, lambda lz, iso: B.estante(lz, iso, 200, 6, 44, 14, 74), clave=230)
    m.add(238, 150, 262, 168, 14, lambda lz, iso: N.baul(lz, iso, 238, 152), clave=330)
    m.add(10, 120, 30, 140, 40, lambda lz, iso: N.maceta(lz, iso, 20, 130, 1.4, t), clave=150)


def _mesa_cura(lz, iso, t):
    B.mesa(lz, iso, 100, 100, 100, 60, 22, color=(122, 82, 60), mantel=(230, 214, 190))
    me.libro(lz, iso, 112, 112, 23.4, 1.0, (150, 60, 60))
    me.libro(lz, iso, 150, 130, 23.4, 1.0, (60, 100, 150))
    lz.relleno(iso.pts([(160, 108, 23.6), (186, 108, 23.6), (186, 124, 23.6), (160, 124, 23.6)]), tint((252, 238, 200)))   # la carta del aviso
    for j in range(3):
        lz.relleno(iso.pts([(162, 111 + 3.4 * j, 23.8), (184, 111 + 3.4 * j, 23.8), (184, 112 + 3.4 * j, 23.8), (162, 112 + 3.4 * j, 23.8)]), tint((150, 50, 50)), alfa=0.85)
    B.candelabro(lz, iso, 124, 140, 23, t, n=3)
    sx, sy = iso.P(124, 140, 40)
    lz.halo(float(sx), float(sy), 80 * iso.z / 3.0, (255, 200, 120), alfa=0.24, capa=2)


# ------------------------------------------------------------------------------------------------ el camino de la marcha
CAMINO = [(-60, 300), (40, 280), (120, 230), (190, 190), (260, 160), (340, 150), (420, 120), (520, 70), (640, 40), (760, 30)]


def pos_camino(s):
    p = np.asarray(CAMINO, float)
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(p, axis=0).T))]
    s = float(np.clip(s, 0, d[-1] - 1e-3))
    return float(np.interp(s, d, p[:, 0])), float(np.interp(s, d, p[:, 1]))


class CaminoMarcha:
    """Camino de tierra entre milpas, magueyales y encinos al amanecer, con lomas al fondo: por aquí marcha el ejército insurgente."""

    def __init__(self):
        self._est = None
        self._t = 0.0

    def suelo(self, lz, iso, t):
        I.isla(lz, iso, -120, -120, 840, 420, color_top=(150, 196, 100), t=t, seed=71, esp=40)
        DC.parches(lz, iso, -120, -120, 840, 420, (150, 196, 100), n=24, var=24, seed=72, alfa=0.55, tam=(50, 100))
        DC.campos(lz, iso, -100, -100, 200, 140, nx=3, ny=2, seed=3, t=t)
        DC.campos(lz, iso, 420, 160, 720, 400, nx=3, ny=2, seed=8, t=t)
        I.camino(lz, iso, CAMINO, 34, (232, 206, 156), borde=(206, 176, 128))
        I.camino(lz, iso, [(300, 420), (310, 300), (330, 190)], 20, (222, 196, 148), borde=(200, 170, 124))

    def objetos(self, t):
        self._t = t
        if self._est is None:
            m = I.Mundo()
            for i in range(12):
                x, y = 20 + 60 * i, 330 - 22 * i + 20 * h01(i, 3)
                if y > 80:
                    m.add(x - 8, y - 8, x + 8, y + 8, 30, (lambda x, y, i: (lambda lz, iso: O.maguey(lz, iso, x, y, s=1.0, seed=i)))(x, y, i), clave=x + y)
            DC.bosque(m, -110, -110, 830, 410, n=40, seed=73, evitar=((-80, 120, 200, 360), (-60, 0, 800, 340)) if False else (), t_fn=lambda: self._t, tipos=("arbol", "nopal"), min_d=28)
            for (x, y) in ((220, 60), (320, 70), (480, 260), (560, 300)):
                A.casa_colonial(m, x, y, 56, 46, 40, muro=[A.CAL, A.OCRE, A.ROSA, A.AZUL][int(h01(x, y) * 4) % 4], techo=A.TEJA, eje="x", ventanas=1, seed=int(x))
            self._est = m
        m = I.Mundo()
        m.fijos = list(self._est.fijos)
        return m


# ------------------------------------------------------------------------------------------------ las tierras del pueblo y la hacienda
class TierrasPueblo:
    """Hacienda con su cerca de piedra y la gran parcela que acaparó (barbecho); a la derecha las chozas del pueblo, la mesa del cobrador de tributos y costales de monedas."""

    def __init__(self):
        self._est = None
        self._t = 0.0

    def suelo(self, lz, iso, t, verde=0.0, cerca_cae=0.0):
        I.isla(lz, iso, -40, -40, 460, 400, color_top=(168, 196, 104), t=t, seed=81, esp=36)
        DC.parches(lz, iso, -40, -40, 460, 400, (168, 196, 104), n=14, var=20, seed=82, alfa=0.5, tam=(40, 90))
        # la parcela acaparada: tierra seca que se cubre de milpa (verde) cuando el pueblo la recupera
        pc = tuple(int(a + (b - a) * verde) for a, b in zip((196, 160, 112), (126, 186, 96)))
        I.suelo_curvo(lz, iso, [(20, 150), (250, 150), (250, 370), (20, 370)], pc, n=4)
        for j in range(8):
            c2 = tuple(int(a + (b - a) * verde) for a, b in zip((172, 132, 92), (98, 160, 80)))
            I.suelo_rect(lz, iso, 24, 160 + j * 26, 222, 9, c2, alfa=0.9)
        I.camino(lz, iso, [(260, 120), (260, 300), (330, 380)], 20, (232, 206, 156), borde=(206, 176, 128))
        I.suelo_curvo(lz, iso, [(280, 20), (440, 20), (440, 130), (280, 130)], (222, 202, 150), n=4)

    def objetos(self, t, fence=1.0, tributo=1.0):
        self._t = t
        if self._est is None:
            m = I.Mundo()
            A.hacienda(m, 30, 10, w=170, d=110, muro=A.OCRE, techo=A.TEJA2, capilla=True)
            for i, x in enumerate((296, 340, 392)):
                B.choza(m, x, 70 + 14 * (i % 2), r=14, h=17, seed=i + 5)
            m.add(270, 40, 292, 62, 40, lambda lz, iso: O.arbol(lz, iso, 282, 52, h=56, seed=19, t=self._t), clave=330)
            DC.bosque(m, -40, -40, 460, 400, n=8, seed=83, evitar=((20, 0, 230, 130), (20, 150, 260, 380), (270, 10, 450, 140)), t_fn=lambda: self._t, tipos=("arbol", "cipres", "nopal"))
            self._est = m
        m = I.Mundo()
        m.fijos = list(self._est.fijos)
        # la cerca de piedra de la hacienda alrededor de la parcela (se derriba en tramos)
        tramos = [((20, 150), (250, 150)), ((250, 150), (250, 370)), ((250, 370), (20, 370)), ((20, 370), (20, 150))]
        for k, (a, b) in enumerate(tramos):
            n = 10
            for i in range(n):
                if h01(k, i, 9) >= fence:
                    continue                                           # ese pedazo ya se derrumbó
                x0, y0 = a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n
                x1, y1 = a[0] + (b[0] - a[0]) * (i + 1) / n, a[1] + (b[1] - a[1]) * (i + 1) / n
                m.add(min(x0, x1) - 3, min(y0, y1) - 3, max(x0, x1) + 3, max(y0, y1) + 3, 14, (lambda x0, y0, x1, y1: (lambda lz, iso: _muro_tramo(lz, iso, x0, y0, x1, y1)))(x0, y0, x1, y1), fijo=False, clave=(x0 + x1) / 2 + (y0 + y1) / 2 + 2)
        # mesa del cobrador con costales y monedas (tributos)
        if tributo > 0.01:
            m.add(300, 160, 380, 200, 30, lambda lz, iso: _mesa_tributo(lz, iso, 300, 160, self._t, tributo), fijo=False, clave=420)
        return m


def _muro_tramo(lz, iso, x0, y0, x1, y1):
    w, d = abs(x1 - x0) + 5, abs(y1 - y0) + 5
    I.caja(lz, iso, min(x0, x1) - 2.5, min(y0, y1) - 2.5, w, d, 14, (206, 192, 176))
    I.caja(lz, iso, min(x0, x1) - 3, min(y0, y1) - 3, w + 1, d + 1, 2.5, (226, 214, 198), z0=14)


def _mesa_tributo(lz, iso, x, y, t, k):
    B.mesa(lz, iso, x, y, 70, 36, 20, color=(122, 82, 60), mantel=(120, 40, 60))
    for i, (cx, cy) in enumerate(((x + 6, y + 8), (x + 22, y + 22), (x + 52, y + 8))):
        O.costal(lz, iso, cx, cy, 1.0 * k, color=(226, 206, 156))
    for i in range(3):
        O2.moneda(lz, iso, x + 40 + 6 * i, y + 18 - 3 * i, 21 + 1.4 * i, r=3.2 * k, t=t + i * 0.3)
    O.costal(lz, iso, x - 12, y + 30, 1.2 * k, color=(226, 206, 156))
    O.costal(lz, iso, x + 76, y + 24, 1.2 * k, color=(226, 206, 156))
