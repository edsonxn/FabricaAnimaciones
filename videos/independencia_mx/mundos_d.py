# -*- coding: utf-8 -*-
"""Mundos de la escena 3 (1808): salones en corte (Bayona, trono, ayuntamiento) y la Plaza Mayor de México de día y de noche."""
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


def _alfombra(lz, iso, x, y, w, d, col=(190, 60, 70), borde=(250, 206, 90)):
    B.alfombra(lz, iso, x, y, w, d, col, borde)


def trono(lz, iso, x, y, t=0.0, s=1.0, corona=True, vacio=False):
    """Trono dorado de respaldo alto con cojín rojo sobre una tarima de dos escalones (mirando hacia +y)."""
    I.caja(lz, iso, x - 26 * s, y - 20 * s, 52 * s, 40 * s, 4 * s, (176, 120, 80))
    I.caja(lz, iso, x - 20 * s, y - 14 * s, 40 * s, 30 * s, 4 * s, (206, 150, 100), z0=4 * s)
    c = I.caja(lz, iso, x - 12 * s, y - 8 * s, 24 * s, 16 * s, 8 * s, (250, 206, 90), z0=8 * s)
    I.caja(lz, iso, x - 10 * s, y - 6 * s, 20 * s, 14 * s, 3 * s, (206, 56, 70), z0=16 * s)
    r = I.caja(lz, iso, x - 12 * s, y - 8 * s, 24 * s, 4 * s, 44 * s, (250, 206, 90), z0=16 * s)
    I.cara_arco(lz, iso, r, "y", 3 * s, 21 * s, 20 * s, 36 * s, (206, 56, 70))
    for dx in (-13, 9):
        I.caja(lz, iso, x + dx * s, y - 8 * s, 4 * s, 16 * s, 10 * s, (250, 206, 90), z0=16 * s)
    if corona:
        sx, sy = iso.P(x, y - 6 * s, 66 * s)
        k = iso.z * s
        lz.relleno(np.array([(-10, 0), (-12, -14), (-5, -7), (0, -16), (5, -7), (12, -14), (10, 0)], float) * k + [sx, sy], tint((250, 206, 70)))
        lz.halo(sx, sy - 6 * k, 22 * k, (255, 230, 140), alfa=0.5, capa=2)


def dibujar_salon(lz, iso, t, firma=0.0, corona_cae=0.0, frances=True, W_=300, D_=260, H_=150, tipo="bayona"):
    """Salón en corte con ventanal, cortinas, escudos, cuadros, mapa, espejo, chimenea, reloj, plantas y araña de cristal. tipo: 'bayona' (francés: azul/dorado) o 'trono'."""
    import kz_iso_int as N
    c = I.habitacion(lz, iso, 0, 0, W_, D_, H_, piso=(206, 196, 180), pared_a=(238, 230, 214), pared_b=(228, 216, 200), friso=(150, 110, 90))
    for i in range(int(W_ / 28)):
        for j in range(int(D_ / 30)):
            if (i + j) % 2:
                I.suelo_rect(lz, iso, 10 + i * 28, 10 + j * 30, 28, 30, (150, 140, 128), z=0.1, alfa=0.55)
    # pared de fondo izquierda ('yi'): ventanal grande al centro, cuadros y escudo
    N.ventana_vista(lz, iso, c, "yi", 110, 190, 36, 120, t=t, cortinas=(40, 70, 170) if tipo == "bayona" else (190, 52, 66), vista="ciudad")
    N.cuadro_retrato(lz, iso, c, "yi", 24, 62, 26, 34, fondo=(70, 100, 150))
    N.escudo(lz, iso, c, "yi", 232, 66, 1.4, "francia" if tipo == "bayona" else "espana")
    N.mapa_pared(lz, iso, c, "yi", 258, 38, 30, 30, t=t) if W_ >= 300 else None
    # pared de fondo derecha ('xi'): puerta, mapa, espejo, bandera
    I.cara_arco(lz, iso, c, "xi", 40, 92, 0, 98, (86, 60, 52))
    N.cortina(lz, iso, c, "xi", 30, 44, 0, 110, (40, 70, 170) if tipo == "bayona" else (190, 52, 66), t)
    N.espejo(lz, iso, c, "xi", 120, 52, 26, 50)
    for k, col in enumerate(((40, 70, 170), (250, 250, 248), (214, 52, 66))):
        I.cara_rect(lz, iso, c, "xi", 176 + k * 14, 190 + k * 14, 64, 130, col)
    I.cara_rect(lz, iso, c, "xi", 172, 176, 60, 134, (150, 100, 70))
    N.chimenea(lz, iso, c, "xi", 214, t=t, w=40, h=34)
    return c


def mesa_firma(lz, iso, x, y, t, firma=0.0):
    B.mesa(lz, iso, x, y, 90, 44, 22, color=(120, 80, 64), mantel=(196, 56, 70))
    # pergamino sobre la mesa con la tinta que va apareciendo
    p = iso.pts([(x + 20, y + 8, 23), (x + 62, y + 8, 23), (x + 62, y + 34, 23), (x + 20, y + 34, 23)])
    lz.relleno(p, tint((252, 240, 210)))
    for i in range(5):
        a = (x + 24, y + 12 + i * 4.4, 23.3)
        b = (x + 24 + (34 if i < 4 else 20) * min(1.0, firma * 1.4), y + 12 + i * 4.4, 23.3)
        lz.relleno(iso.pts([a, b, (b[0], b[1] + 1.2, b[2]), (a[0], a[1] + 1.2, a[2])]), tint((120, 80, 60)), alfa=0.9)
    B.candelabro(lz, iso, x + 10, y + 20, 23, t, n=3)
    # pluma
    sx, sy = iso.P(x + 70, y + 30, 24)
    k = iso.z
    lz.relleno(np.array([[sx, sy], [sx + 14 * k, sy - 20 * k], [sx + 17 * k, sy - 18 * k], [sx + 3 * k, sy + 1 * k]]), tint((250, 250, 250)))


class PlazaMayor:
    """Plaza Mayor de la Ciudad de México (esquema): Palacio Virreinal al fondo, Catedral a la izquierda, portales con arcos a la derecha, fuente central, multitud, puestos, faroles. Día/noche por luz()."""
    N = 520.0

    def __init__(self):
        self._est = None

    def suelo(self, lz, iso, t, noche=0.0):
        I.isla(lz, iso, -60, -60, 580, 560, color_top=(214, 196, 170), t=t, seed=31, esp=38)
        I.suelo_curvo(lz, iso, [(-30, -30), (550, -30), (550, 530), (-30, 530)], (232, 214, 188))
        I.suelo_rect(lz, iso, 100, 120, 320, 330, (244, 228, 204))
        I.cuadricula(lz, iso, 100, 120, 420, 450, 22, color=(255, 255, 255), alfa=0.20 * (1 - 0.7 * noche))
        I.camino(lz, iso, [(-60, 285), (100, 285)], 50, (222, 204, 176))
        I.camino(lz, iso, [(420, 285), (580, 285)], 50, (222, 204, 176))
        I.camino(lz, iso, [(260, 450), (260, 580)], 50, (222, 204, 176))
        DC.parches(lz, iso, -60, -60, 580, 560, (222, 204, 178), n=14, var=16, seed=33, alfa=0.45, tam=(40, 90))

    def objetos(self, t, noche=0.0, farolas=0.0):
        self._t = t
        if self._est is None:
            m = I.Mundo()
            B.palacio(m, 90, 10, w=340, d=70, h=78, campana=True)
            B.catedral(m, -30, 140, w=96, largo=190, h=76)
            B.portal_arcos(m, 440, 140, 4, paso=22, d=16, h=42) if False else None
            for i in range(5):
                A.casa_colonial(m, 450, 130 + i * 70, 60, 56, 52, muro=[A.CAL, A.OCRE, A.ROSA, A.AZUL, A.VERDE_CAL][i], techo=A.TEJA, eje="y", ventanas=2, balcon=True, seed=i + 5)
            for i in range(5):
                A.casa_colonial(m, 60 + i * 80, 470, 70, 52, 50, muro=[A.OCRE, A.CAL, A.ROSA, A.VERDE_CAL, A.AZUL][i], techo=A.TEJA2, eje="x", ventanas=2, balcon=(i % 2 == 0), seed=i + 15)
            m.add(250, 280, 272, 302, 40, lambda lz, iso: O.fuente(lz, iso, 260, 290, t=self._t, s=1.4))
            for (x, y) in ((120, 140), (400, 140), (120, 430), (400, 430), (260, 160), (260, 420)):
                m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y: (lambda lz, iso: O.farol(lz, iso, x, y, encendido=0.0)))(x, y))
            for i, (x, y) in enumerate(((150, 330), (360, 330), (170, 230), (350, 240), (220, 400), (310, 400))):
                A.puesto(m, x, y, toldo=[(236, 90, 96), (70, 160, 200), (110, 190, 110), (250, 150, 70)][i % 4], cosas=[(250, 190, 70), (236, 120, 70), (250, 214, 80)][i % 3], seed=i)
            DC.bosque(m, -50, -50, 570, 550, n=14, seed=71, evitar=((80, 0, 440, 100), (-40, 130, 80, 340), (100, 120, 420, 450), (440, 120, 530, 500), (40, 460, 500, 540)), t_fn=lambda: self._t, tipos=("arbol", "cipres"))
            self._est = m
        m = I.Mundo()
        m.fijos = list(self._est.fijos)
        mu = G.Multitud()
        tipos = ("campesino", "campesina", "mestizo", "indigena", "indigena_f", "comerciante", "regidor", "dama", "nino")
        for i in range(18):
            mu.ronda((260, 290), 150, tipos[i % len(tipos)], n=1, seed=3000 + i * 7, h=40 if tipos[i % len(tipos)] != "nino" else 28)
        mu.camina([(-60, 285), (100, 285), (260, 300), (420, 285), (580, 285)], "arriero", vel=13, seed=41, bucle="ida_vuelta")
        mu.dibujar(m, t)
        O.Caravana([(-60, 290), (100, 290), (260, 310), (420, 290), (580, 290)], n=3, vel=15, fase=0.5, seed=17).dibujar(m, t)
        if farolas > 0.01:
            for (x, y) in ((120, 140), (400, 140), (120, 430), (400, 430), (260, 160), (260, 420)):
                m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y: (lambda lz, iso: O.farol(lz, iso, x, y, encendido=farolas)))(x, y), fijo=False, clave=x + y + 1)
        return m
