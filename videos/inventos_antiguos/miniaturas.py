# -*- coding: utf-8 -*-
"""Miniaturas del video (python fab.py inventos_antiguos miniatura). Estilo recortes de papel."""
import numpy as np

import dibujos as D
import fondos as F
from dibujos import AMARILLO, NEGRO, BLANCO
from escena_base import dibujar_icono
from motor import W, H

T = 0.37


def tostada(lz):
    """Tú, sorprendido, con tu tostada del desayuno: la receta tiene 14.400 años."""
    for nombre, x, y, s in (("reloj", 1780, 860, 0.55), ("rueda_madera", 1560, 960, 0.5), ("moneda_leon", 1800, 620, 0.5)):
        dibujar_icono(lz, nombre, x, y, s, T)
    D.personaje(lz, 560, 1500, 2.1, T, "tu", seed=22, mano_i=(-150, -190), mano_d=(300, -330),
                boca=0.8, cejas=1.0, mirar=(1, -0.1), ojos="abiertos")
    D.tostada(lz, 1260, 640, 1.55, seed=511)
    lz.texto("¡14.400 AÑOS!", 960, 190, 170, "snap", color=AMARILLO, borde=NEGRO, borde_px=18, rot=-0.04, capa=2)
    return F.cartulina(T, "oceano")


def chat(lz):
    """La tablilla de arcilla de Uruk = tu chat del celular."""
    xs = np.arange(W)[None, :] + (np.arange(H)[:, None] - H / 2) * 0.12
    m = (xs > W / 2).astype(np.float32)[..., None]
    fondo = F.cartulina(T, "ocre") * (1 - m) + F.cartulina(T, "oceano", claro=1) * m
    D.tablilla(lz, 500, 620, 1.35, seed=581, rot=-0.08)
    D.telefono(lz, 1420, 620, 1.2, 0.08, seed=97, t=T,
               pantalla=lambda lz: D.chat(lz, 0, -40, 0.62, 9.0, seed=601))
    lz.texto("=", 960, 620, 300, "snap", color=AMARILLO, borde=NEGRO, borde_px=20, capa=2)
    lz.texto("5.200 AÑOS", 560, 150, 118, "snap", color=BLANCO, borde=NEGRO, borde_px=15, rot=-0.04, capa=2)
    lz.texto("HOY", 1420, 150, 130, "snap", color=AMARILLO, borde=NEGRO, borde_px=15, rot=0.04, capa=2)
    return fondo


VARIANTES = {"tostada": tostada, "chat": chat}
