# -*- coding: utf-8 -*-
"""Miniaturas del video (python fab.py 40mil_anos miniatura). Cada variante dibuja y devuelve el fondo."""
import numpy as np

import dibujos as D
import fondos as F
from dibujos import AMARILLO, NEGRO, BLANCO
from motor import OCRE, elipse, estrella, W, H

T = 0.37


def _selfie_pantalla(lz):
    lz.relleno(np.array([(-95, -185), (95, -185), (95, 185), (-95, 185)], float), (120, 72, 40), 900, temblor=0.2)
    D.personaje(lz, -10, 178, 0.62, T, "cave", seed=11, mano_i=(-60, -330), mano_d=(125, -175),
                boca=0.7, cejas=1.0, mirar=(0, 0), ojos="abiertos")
    D.ui_camara(lz, T, 901)


def _titulo(lz, texto):
    if texto == "40mil":
        lz.texto("HACE", 250, 85, 100, "snap", color=BLANCO, borde=NEGRO, borde_px=13, rot=-0.05, capa=2)
        lz.texto("40.000 AÑOS", 830, 215, 165, "snap", color=AMARILLO, borde=NEGRO, borde_px=17, rot=-0.05, capa=2)
    else:
        lz.texto(texto, 930, 175, 150, "snap", color=AMARILLO, borde=NEGRO, borde_px=17, rot=-0.05, capa=2)


def selfie(lz, texto="40mil"):
    """Cavernícola de hace 40.000 años sacándose una selfie en su cueva."""
    for x, y, s, r in ((1640, 330, 1.25, 0.3), (1790, 700, 1.0, -0.4), (150, 330, 0.9, -0.2)):
        D.estarcido(lz, x, y, s, 1.0, rot=r)
    D.personaje(lz, 600, 1570, 2.2, T, "cave", seed=11, mano_i=(-150, -190), mano_d=(295, -395),
                boca=0.75, cejas=1.0, mirar=(1, -0.3), ojos="abiertos")
    D.telefono(lz, 1300, 640, 1.15, 0.22, pantalla=_selfie_pantalla, seed=97, t=T)
    with lz.capa(2):
        lz.forma(estrella(1440, 420, 120, 34, 8, 0.2), (255, 255, 225), NEGRO, 5, seed=5)
    _titulo(lz, texto)
    return F.cueva(T)


def igual(lz):
    """Pantalla partida: el cavernícola pinta su comida en la roca = tú le tomas foto a tu hamburguesa."""
    xs = np.arange(W)[None, :] + (np.arange(H)[:, None] - H / 2) * 0.12
    m = (xs > W / 2).astype(np.float32)[..., None]
    fondo = F.cueva(T) * (1 - m) + F.rayos(T, "arcoiris") * m
    D.cerdo_rupestre(lz, 290, 560, 0.95, 1.0)

    def pincel(lz, hx, hy):
        lz.trazo([(hx, hy), (hx - 45, hy - 45)], D.MARRON, 12, seed=90)
        lz.forma(elipse(hx - 52, hy - 52, 12, 18, 0.8), OCRE, NEGRO, 4, seed=91)
    D.personaje(lz, 610, 1230, 1.55, T, "cave", seed=21, mano_i=(-120, -170), mano_d=(-124, -400), obj_d=pincel,
                boca=0.6, cejas=1.0, mirar=(-1, -0.3), ojos="abiertos")
    D.hamburguesa(lz, 1690, 840, 1.25, seed=96)
    D.personaje(lz, 1330, 1230, 1.55, T, "tu", seed=22, mano_i=(-120, -170), mano_d=(200, -470),
                boca=0.6, cejas=1.0, mirar=(1, -0.2), ojos="abiertos")
    D.telefono(lz, 1640, 450, 0.75, 0.25, seed=97, t=T,
               pantalla=lambda lz: (D.hamburguesa(lz, 0, -20, 0.55, seed=98), D.ui_camara(lz, T, 99)))
    lz.texto("=", 960, 600, 330, "snap", color=AMARILLO, borde=NEGRO, borde_px=20, capa=2)
    lz.texto("40.000 AÑOS", 530, 105, 104, "snap", color=BLANCO, borde=NEGRO, borde_px=14, rot=-0.04, capa=2)
    lz.texto("HOY", 1500, 110, 120, "snap", color=AMARILLO, borde=NEGRO, borde_px=14, rot=0.04, capa=2)
    return fondo


VARIANTES = {"selfie": selfie, "igual": igual, "selfie_frase": lambda lz: selfie(lz, "¡YA LO HACÍAN!")}
