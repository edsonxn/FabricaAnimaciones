# -*- coding: utf-8 -*-
"""Miniaturas del video (python fab.py neandertales miniatura). Estilo doodle, tonos tierra."""
import numpy as np

import dibujos as D
import fondos as F
from dibujos import AMARILLO, NEGRO, BLANCO, ROJO
from escena_base import dibujar_icono
from escenas import garra
from motor import W, H

T = 0.37


def collar_garras(lz, x, y, s=1.0, n=8):
    """Collar de garras de águila (Krapina), colgando de un cordel."""
    a = np.linspace(0, 1, n)
    cuerda = [(-500 + 1000 * u, 250 * (1 - (2 * u - 1) ** 2) - 6) for u in np.linspace(0, 1, 30)]
    with lz.grupo(x, y, s):
        lz.trazo(cuerda, (150, 100, 60), 8, seed=800)
        for i, u in enumerate(a):
            garra(lz, -500 + 1000 * u, 250 * (1 - (2 * u - 1) ** 2) + 36, 1.35, 0.0, seed=810 + i, cortes=1.0)


def brutos(lz):
    """Neandertal sorprendido con un cerebro enorme: ¿brutos?"""
    dibujar_icono(lz, "cerebro", 1420, 560, 1.45, T)
    D.personaje(lz, 520, 1480, 2.1, T, "neander", seed=22, mano_i=(-150, -190), mano_d=(300, -330),
                boca=0.8, cejas=1.0, mirar=(1, -0.1), ojos="abiertos")
    lz.texto("¿BRUTOS?", 960, 180, 200, "snap", color=AMARILLO, borde=NEGRO, borde_px=20, rot=-0.04, capa=2)
    lz.texto("MÁS CEREBRO", 1420, 930, 84, "snap", color=BLANCO, borde=NEGRO, borde_px=12, rot=0.04, capa=2)
    return F.plano(T, "ocre")


def mitos(lz):
    """Siete mitos: el neandertal y los iconos de lo que sí hacían."""
    collar_garras(lz, 1500, 380, 0.34)
    for nombre, x, y, s in (("corazon", 1720, 800, 0.5), ("fuego", 1250, 860, 0.5), ("pastilla", 1100, 420, 0.5)):
        dibujar_icono(lz, nombre, x, y, s, T)
    D.personaje(lz, 540, 1500, 2.1, T, "neander", seed=22, mano_i=(-150, -190), mano_d=(300, -330),
                boca=0.8, cejas=1.0, mirar=(1, -0.1), ojos="abiertos")
    lz.texto("7 MITOS", 1270, 190, 190, "snap", color=AMARILLO, borde=NEGRO, borde_px=18, rot=-0.04, capa=2)
    lz.texto("FALSOS", 1400, 640, 130, "snap", color=ROJO, borde=NEGRO, borde_px=16, rot=0.05, capa=2)
    return F.cueva(T, tinte=0.0)


def collar(lz):
    """Las garras de águila de Krapina: la joyería más antigua de Europa."""
    collar_garras(lz, 1400, 330, 0.82)
    D.personaje(lz, 470, 1500, 2.0, T, "neander", seed=22, mano_i=(-150, -190), mano_d=(300, -330),
                boca=0.8, cejas=1.0, mirar=(1, -0.1), ojos="abiertos")
    lz.texto("¿JOYAS?", 960, 180, 200, "snap", color=AMARILLO, borde=NEGRO, borde_px=20, rot=-0.04, capa=2)
    lz.texto("HACE 130.000 AÑOS", 1400, 930, 80, "snap", color=BLANCO, borde=NEGRO, borde_px=12, rot=0.03, capa=2)
    return F.plano(T, "oceano")


VARIANTES = {"brutos": brutos, "mitos": mitos, "collar": collar}
