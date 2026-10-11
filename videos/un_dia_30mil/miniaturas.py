# -*- coding: utf-8 -*-
"""Miniaturas del video (python fab.py un_dia_30mil miniatura). Estilo doodle, era de hielo."""
import dibujos as D
import fondos as F
from dibujos import AMARILLO, NEGRO, BLANCO

T = 0.37


def _copos(lz, pts, s=1.0):
    for i, (x, y) in enumerate(pts):
        D.copo(lz, x, y, s, 0.4 * i, seed=700 + i)


def sobrevivir(lz):
    """El reto: ¿sobrevivirías un día en la era de hielo? Cavernícola asustado y un mamut."""
    D.mamut(lz, 1400, 790, 1.5, T, seed=20)
    D.personaje(lz, 400, 1500, 2.1, T, "cave", seed=22, mano_i=(-150, -190), mano_d=(150, -330),
                boca=0.8, cejas=1.0, mirar=(1, -0.1), ojos="abiertos")
    _copos(lz, ((820, 400), (960, 580), (1100, 340), (1820, 330)), 0.8)
    lz.texto("¿SOBREVIVIRÍAS?", 960, 170, 146, "snap", color=AMARILLO, borde=NEGRO, borde_px=18, rot=-0.02, capa=2)
    lz.texto("HACE 30.000 AÑOS", 1360, 990, 84, "snap", color=BLANCO, borde=NEGRO, borde_px=13, rot=0.02, capa=2)
    return F.plano(T, "oceano")


def dia(lz):
    """Un día hace 30.000 años: el cavernícola tiritando junto al fuego."""
    D.fuego(lz, 1450, 1010, 1.9, T, seed=30)
    D.personaje(lz, 440, 1500, 2.1, T, "cave", seed=22, mano_i=(-150, -190), mano_d=(210, -260),
                boca=0.8, cejas=1.0, mirar=(1, 0.0), ojos="abiertos")
    _copos(lz, ((860, 560), (1040, 800), (1800, 600), (1850, 860), (1130, 600)), 0.85)
    lz.texto("UN DÍA", 1250, 170, 200, "snap", color=BLANCO, borde=NEGRO, borde_px=20, rot=-0.03, capa=2)
    lz.texto("HACE 30.000 AÑOS", 1250, 360, 104, "snap", color=AMARILLO, borde=NEGRO, borde_px=14, rot=0.02, capa=2)
    return F.plano(T, "cosmos")


VARIANTES = {"sobrevivir": sobrevivir, "dia": dia}
