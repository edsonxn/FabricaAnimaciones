# -*- coding: utf-8 -*-
"""Mundos de la escena 13 (el cierre): Juchipila hoy en isométrico (el mismo trazo de la refundación, con kiosco, farolas, casas de colores,
gente de hoy y flores que brotan), la danza de los tastoanes con Santiago a caballo en 2D, y el icono de comentarios."""
import math

import numpy as np

import kz_iso as I
import kz_iso_obj as O
import kz_iso_arq as A
import kz_gente_iso as G
import kz_pers2d as K2
import plano as P
from motor import circulo, elipse, rect_red, catmull, h01, prog, smooth, e_out, e_back, e_inout, W, H
import mundos_k as MK
import mundos_h as MH

COLORES_HOY = [(236, 120, 110), (120, 190, 210), (250, 206, 110), (170, 140, 220), (130, 200, 150), (240, 170, 120)]


class JuchipilaHoy(MK.PuebloNuevo):
    """Mismo lugar que la refundación (río, plaza, templo con convento), hoy: casas de colores, kiosco, farolas, gente; `flores` 0..1 = junio."""

    def objetos_hoy(self, t, flores=0.0, atardecer=0.0):
        m = I.Mundo()
        for i, (x, y, eje) in enumerate(MK.LOTES):
            w, d = (54, 40) if eje == 0 else (40, 54)
            A.casa_colonial(m, x, y, w, d, 36 + 10 * (i % 3 == 0), muro=COLORES_HOY[i % len(COLORES_HOY)], eje="x" if eje == 0 else "y", ventanas=1, seed=i, balcon=i % 3 == 0)
        A.iglesia(m, 130, -130, w=74, largo=110, h_nave=58, muro=A.CANTERA, techo=A.TEJA, torres=1, cupula_c=True, luz_ventanas=atardecer)
        A.portal_arcos(m, 220, -130, 4, paso=20, d=16, h=34, muro=(236, 222, 196), eje="x")
        A.casa_colonial(m, 220, -114, 84, 54, 40, muro=(236, 222, 196), eje="x", ventanas=3, seed=99)
        m.add(185, 85, 215, 115, 40, lambda lz, iso: self._kiosco(lz, iso, 200, 100), fijo=False)
        for i, (x, y) in enumerate(((122, 22), (278, 22), (122, 178), (278, 178), (200, 22), (200, 178))):
            m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y: (lambda lz, iso: O.farol(lz, iso, x, y, h=36, t=t, encendido=atardecer)))(x, y), fijo=False)
        for i, (x, y) in enumerate(((140, 40), (260, 40), (140, 160), (260, 160))):
            m.add(x - 8, y - 8, x + 8, y + 8, 50, (lambda x, y, i: (lambda lz, iso: O.arbol(lz, iso, x, y, h=44, seed=i, t=t)))(x, y, i), fijo=False)
        if flores > 0.01:                                                  # junio: el pueblo se llena de flores
            for i in range(60):
                x = -40 + 520 * h01(71, i)
                y = -220 + 520 * h01(72, i)
                k = smooth(np.clip(flores * 1.6 - h01(73, i) * 0.6, 0, 1))
                if k > 0.02:
                    col = ((255, 170, 40), (255, 210, 70), (236, 70, 140), (250, 120, 60))[i % 4]
                    m.add(x - 5, y - 5, x + 5, y + 5, 12, (lambda x, y, k, col, i: (lambda lz, iso: O.arbusto(lz, iso, x, y, r=8 * k, seed=i, flores=col)))(x, y, k, col, i), fijo=False)
        mu = G.Multitud()
        tipos = ("campesino", "campesina", "dama", "nino", "comerciante", "mestizo")
        for i in range(10):
            mu.camina([(120 + 40 * (i % 4), 40 + 30 * (i % 5)), (280 - 30 * (i % 3), 160 - 25 * (i % 4)), (130, 170)], tipos[i % 6], vel=6 + i % 3, seed=2500 + i, h=36, fase=0.1 * i, bucle=True)
        for i in range(4):
            mu.ronda((200, 100), 40, tipos[(i + 2) % 6], n=1, vel=3, seed=2520 + i, h=36)
        mu.dibujar(m, t)
        return m

    @staticmethod
    def _kiosco(lz, iso, x, y):
        I.cilindro(lz, iso, x, y, 22, 6, (236, 226, 206))
        for k in range(8):
            a = k * math.pi / 4
            I.cilindro(lz, iso, x + 18 * math.cos(a), y + 18 * math.sin(a), 1.4, 26, (90, 120, 110), z0=6)
        I.cono(lz, iso, x, y, 26, 16, (90, 150, 130), z0=32)


# ------------------------------------------------------------------------------------------------ 2D: los tastoanes y Santiago
def tastoanes(lz, t, cx=0.0, y=960):
    """Plaza con papel picado: Santiago en su caballo blanco al centro y los tastoanes (máscaras) que bailan alrededor."""
    MH.caballo2d(lz, 960 - cx * 0.3, y + 70, 22, t, ph=t * 3.0, galope=0.35, color=(240, 236, 228), crin=(200, 196, 196),
                 jinete=dict(K2.TIPOS["capitan"], tocado="sombrero_ala", ropa=(60, 90, 160), ropa2=(240, 220, 120)), jinete_seed=2600)
    for i in range(8):
        a = t * 0.8 + i * 2 * math.pi / 8
        x = 960 - cx * 0.3 + 520 * math.cos(a)
        yy = y + 40 + 50 * math.sin(a)
        K2.cuerpo(lz, x, yy, 30 + 4 * math.sin(a), K2.variar("tastoan", 2610 + i) | {"tocado": "mascara_tastoan"}, t, piernas="baila", brazos="baila", mirar=1 if math.cos(a) < 0 else -1,
                  vista="frente", seed=2610 + i, ph=t * 6 + i)


def icono_comentarios(lz, x, y, s, t, k=1.0):
    """Globo de comentario con tres puntos que laten."""
    if k <= 0.01:
        return
    s = s * k
    lz.relleno(rect_red(x - 120 * s, y - 80 * s, 240 * s, 160 * s, 40 * s), (255, 255, 255), capa=2)
    lz.relleno(np.array([(x - 60 * s, y + 70 * s), (x - 90 * s, y + 130 * s), (x - 10 * s, y + 76 * s)]), (255, 255, 255), capa=2)
    for j in range(3):
        a = 0.5 + 0.5 * math.sin(t * 6 - j * 0.9)
        lz.relleno(circulo(x - 60 * s + 60 * s * j, y, (14 + 6 * a) * s, 16), (122, 52, 200), capa=2)
