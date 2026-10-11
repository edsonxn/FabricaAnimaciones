# -*- coding: utf-8 -*-
"""Mundos de la escena 15 (Iturbide): la plaza de Iguala con guirnaldas tricolor y el valle de Acatempan para el abrazo."""
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


class PlazaIguala:
    """Plaza de Iguala (tierra caliente): iglesia pequeña de cal, portales, casas de colores vivos, palmeras y guirnaldas de banderines blanco-verde-rojo entre postes."""

    def __init__(self):
        self._est = None
        self._t = 0.0

    def suelo(self, lz, iso, t):
        I.isla(lz, iso, -120, -120, 520, 460, color_top=(176, 196, 108), t=t, seed=201, esp=40)
        DC.parches(lz, iso, -120, -120, 520, 460, (176, 196, 108), n=22, var=22, seed=202, alfa=0.55, tam=(50, 100))
        I.suelo_curvo(lz, iso, [(-40, 90), (440, 90), (460, 400), (-50, 410)], (232, 212, 172))
        I.suelo_rect(lz, iso, 70, 130, 260, 230, (246, 230, 196))
        I.cuadricula(lz, iso, 70, 130, 330, 360, 26, color=(255, 255, 255), alfa=0.22)
        I.camino(lz, iso, [(-120, 250), (70, 250)], 44, (236, 216, 176))
        I.camino(lz, iso, [(330, 250), (520, 250)], 44, (236, 216, 176))
        I.camino(lz, iso, [(200, 360), (200, 520)], 44, (236, 216, 176))

    def objetos(self, t, gente=1.0):
        self._t = t
        if self._est is None:
            m = I.Mundo()
            A.iglesia(m, 140, -10, w=76, largo=96, h_nave=58, muro=(250, 244, 226), techo=A.TEJA, torres=1, cupula_c=True)
            B_ = A.portal_arcos
            B_(m, 60, 372, 8, paso=24, d=16, h=42, muro=A.CAL)
            pal = [A.AZUL, A.ROSA, (252, 214, 120), A.VERDE_CAL, (214, 170, 236), A.OCRE]
            for i in range(4):
                A.casa_colonial(m, -70, 110 + i * 62, 62, 46, 44 + 6 * (i % 2), muro=pal[i], techo=A.TEJA, eje="x", ventanas=2, balcon=(i % 2 == 0), seed=i + 510)
                A.casa_colonial(m, 340, 120 + i * 62, 62, 46, 46, muro=pal[(i + 2) % 6], techo=A.TEJA2, eje="x", ventanas=2, balcon=(i % 2 == 1), seed=i + 520)
            for (x, y) in ((50, 140), (320, 140), (50, 350), (320, 350)):
                m.add(x - 10, y - 10, x + 10, y + 10, 60, (lambda x, y: (lambda lz, iso: O.palmera(lz, iso, x, y, h=66, seed=int(x + y), t=self._t)))(x, y), clave=x + y)
            m.add(186, 236, 214, 264, 40, lambda lz, iso: O.fuente(lz, iso, 200, 250, t=self._t, s=1.3), clave=450)
            DC.bosque(m, -120, -120, 520, 460, n=14, seed=203, evitar=((-120, 80, 520, 440), (60, -30, 300, 100)), t_fn=lambda: self._t, tipos=("palma", "arbol"))
            self._est = m
        m = I.Mundo()
        m.fijos = list(self._est.fijos)
        if gente > 0.01:
            mu = G.Multitud()
            tipos = ("campesino", "campesina", "comerciante", "mestizo", "indigena", "dama", "arriero", "nino")
            for i in range(int(18 * gente)):
                mu.ronda((110 + 12 * i, 230 + 16 * (i % 4)), 44, tipos[i % 8], n=1, seed=4400 + i * 5, h=40 if tipos[i % 8] != "nino" else 28)
            mu.dibujar(m, t)
        return m


def guirnaldas(lz, iso, t, k=1.0, postes=None, z=70):
    """Cuerdas con banderines blanco-verde-rojo entre postes alrededor de la plaza (se dibujan sobre el diorama)."""
    postes = postes or [(70, 130), (330, 130), (330, 360), (70, 360)]
    cols = [(250, 250, 246), (70, 170, 110), (214, 56, 66)]
    for a in range(4):
        (x0, y0), (x1, y1) = postes[a], postes[(a + 1) % 4]
        p0 = np.array([float(v) for v in iso.P(x0, y0, z)])
        p1 = np.array([float(v) for v in iso.P(x1, y1, z)])
        n = 22
        pts = []
        for i in range(n + 1):
            u = i / n
            p = p0 + (p1 - p0) * u
            pts.append((p[0], p[1] + 30 * math.sin(math.pi * u) * iso.z / 3))
        lz.trazo(np.array(pts), (240, 226, 190), 2.4, afinar=False, temblor=0.0, capa=2)
        for i in range(1, n, 1):
            if i / n > k:
                break
            x, y = pts[i]
            lz.relleno(np.array([[x - 7 * iso.z / 3, y], [x + 7 * iso.z / 3, y], [x, y + 20 * iso.z / 3 + 2 * math.sin(t * 4 + i)]]), cols[i % 3], capa=2)
    for (x, y) in postes:
        I.caja(lz, iso, x - 2, y - 2, 4, 4, z, (150, 108, 76))
