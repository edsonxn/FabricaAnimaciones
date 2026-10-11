# -*- coding: utf-8 -*-
"""Miniaturas (python fab.py teotihuacan miniatura). Pirámide grande, 1-3 palabras enormes amarillas con contorno
negro y un personaje con cara de sorpresa."""
import numpy as np

import mundo as M
import plano as P
from motor import NEGRO

T = 0.37
AMARILLO = (255, 214, 64)


def _texto(lz, s, x, y, px, rot=-0.03, color=AMARILLO):
    lz.texto(s, x, y, px, "geo_x", color=color, borde=NEGRO, borde_px=px * 0.11, rot=rot, capa=2, temblor=0.0)


def _pan(lz, hora, cam, **k):
    est = dict(hora=hora, fuego=0.0, ruina=0.0, gente=0.0, luces=0.0)
    est.update(k)
    M.panorama(lz, T, est, cam)


def sin_nombre(lz):
    """La pirámide al ocaso, en ruinas, con un signo de interrogación gigante."""
    _pan(lz, 3.0, (M.X_SOL - 250, -330, 1.0), ruina=0.6)
    _texto(lz, "SIN NOMBRE", 960, 260, 210)
    with lz.capa(2):
        with lz.grupo(1560, 1040, 4.4, 0.0, 4.4):
            M.persona(lz, 0, 0, 1.0, T, ropa=1, piel=1, brazos=0.55, cara="sorpresa", tocado="plumas")
    return np.zeros((1080, 1920, 3), np.float32)


def en_llamas(lz):
    """La Calzada ardiendo."""
    _pan(lz, 3.2, (M.X_SOL - 200, -330, 1.0), fuego=1.0, luces=0.3)
    _texto(lz, "AÑO 550", 800, 250, 230, color=(255, 240, 200))
    _texto(lz, "¿QUIÉN?", 1400, 470, 200)
    with lz.capa(2):
        with lz.grupo(360, 1040, 4.4, 0.0, 4.4):
            M.persona(lz, 0, 0, 1.0, T, ropa=4, piel=2, brazos=0.6, cara="sorpresa", lado=-1)
    return np.zeros((1080, 1920, 3), np.float32)


def cien_mil(lz):
    """La ciudad llena de gente."""
    _pan(lz, 2.0, (M.X_SOL - 100, -300, 0.95), gente=1.0)
    _texto(lz, "100 000", 960, 230, 260)
    _texto(lz, "PERSONAS", 960, 420, 150)
    return np.zeros((1080, 1920, 3), np.float32)


VARIANTES = {"sin_nombre": sin_nombre, "en_llamas": en_llamas, "cien_mil": cien_mil}
