# -*- coding: utf-8 -*-
"""Miniaturas 16:9 de un video vertical: se dibujan en una franja de 1080x608 (CROP_Y..CROP_Y+608) del lienzo vertical
y nucleo/miniatura.py la recorta y la escala a 1280x720."""
import math

import numpy as np

import fondos as F
import locales as L
import mapa_dib as M
import subsuelo as S
import vox as V
from motor import W, H

T = 0.4
WOB = 0.8
CROP_Y = 640
BH = int(W * 9 / 16)          # 607


def _texto(lz, txt, x, y, px, color=V.AMARILLO, rot=0.0, ancla=(0.5, 0.5), max_w=560):
    from motor import ancho_texto
    w = ancho_texto(txt, "vox_x", px)
    if w > max_w:
        px = px * max_w / w
    lz.texto(txt, x, y, px, "vox_x", color=color, borde=(30, 22, 20), borde_px=max(8, px * 0.13), ancla=ancla, rot=rot,
             capa=2, temblor=0.0)


def _bufa(lz, x, y, s, sombra=True):
    with lz.grupo(x, y, s):
        lz.relleno(V.corte(L.BUFA, 5, 2.5, 2), (208, 138, 98), temblor=0.0, capa=1)
        lz.relleno(L.BUFA_SOMBRA, (160, 96, 72), temblor=0.0, capa=1)
        lz.relleno(L.BUFA_CRESTA, (230, 180, 140), temblor=0.0, capa=1)


def _veta(lz, x, y, s, t=0.0):
    pts = np.array([[640, -60], [690, -170], [738, -260], [790, -340], [846, -430]], float)
    with lz.grupo(x, y, s):
        lz.trazo(pts, (240, 220, 180), 30, afinar=False, temblor=0.0, capa=1)
        lz.trazo(pts, V.PLATA, 15, afinar=False, temblor=0.0, capa=1)
        for i, p in enumerate(pts[1:]):
            L.chispa(lz, p[0] + 26, p[1] - 14, 26, 1.0 + i, seed=i, capa=2)


def _fondo_dia(colores):
    return F.cielo_fondo(colores)


def v_bufa(lz):
    """Cerro de la Bufa con la veta brillante, un minero enorme y 'PLATA' en grande."""
    with lz.grupo(0, CROP_Y):
        _bufa(lz, -330, 590, 0.86)
        _veta(lz, -330, 590, 0.86)
        lz.relleno(np.array([[0, 560], [W, 560], [W, BH + 40], [0, BH + 40]]), (204, 160, 104), temblor=0.0, capa=1)
        V.figura(lz, 250, 590, 1.35, V.SEÑALAR[0], "minero", 1, obj=[("d", "pico", 0, 1.0)], capa=1, seed=3)
        _texto(lz, "FIEBRE", 760, 110, 170)
        _texto(lz, "DE PLATA", 760, 250, 170)
        _texto(lz, "1546", 760, 410, 120, color=(255, 255, 255))
    return _fondo_dia(((252, 196, 128), (252, 232, 196)))


def v_mina(lz):
    """Interior de la mina: candelas, vena de plata y un cargador con el cesto."""
    with lz.grupo(0, CROP_Y):
        lz.relleno(np.array([[-100, 0], [W + 100, 0], [W + 100, BH], [-100, BH]]), (70, 60, 96), temblor=0.0, capa=0)
        lz.relleno(np.array([[430, -20], [W + 40, -20], [W + 40, BH + 20], [590, BH + 20]]), (52, 46, 76), temblor=0.0, capa=0)
        S.luz_vela(lz, 300, 380, 420, 1.0)
        pts = np.array([[520, -20], [640, 200], [780, 420], [900, 640]])
        lz.trazo(pts, (230, 210, 175), 46, afinar=False, temblor=0.0, capa=1)
        lz.trazo(pts, V.PLATA, 24, afinar=False, temblor=0.0, capa=1)
        for i in range(1, 3):
            L.chispa(lz, pts[i][0] + 40, pts[i][1] - 30, 34, 0.7 * i, seed=i, capa=2)
        V.figura(lz, 260, 660, 1.6, V.CAMINAR[3], "cargador", 1, carga=("tenate", 1.0), capa=1, seed=7)
        _texto(lz, "BAJO", 760, 120, 170)
        _texto(lz, "TIERRA", 760, 260, 170)
        _texto(lz, "1550", 760, 420, 110, color=(255, 255, 255))
    return _fondo_dia(((44, 40, 92), (120, 92, 130)))


def v_moneda(lz):
    """Moneda de plata gigante sobre el mapa."""
    with lz.grupo(0, CROP_Y):
        lz.relleno(np.array([[-100, 360], [W + 100, 360], [W + 100, BH + 100], [-100, BH + 100]]), (170, 198, 202), temblor=0.0, capa=0)
        lz.relleno(np.array([[-100, 300], [W + 100, 290], [W + 100, BH + 100], [-100, BH + 100]]), (226, 200, 148), temblor=0.0, capa=1)
        r = 210
        cx, cy = 250, 330
        lz.relleno(V.elipse_pts(cx, cy + 20, r, r), V.PLATA_OSC, temblor=0.0, capa=1)
        lz.relleno(V.elipse_pts(cx, cy, r, r), V.PLATA, temblor=0.0, capa=1)
        lz.relleno(V.elipse_pts(cx, cy, r * 0.82, r * 0.82), V.aclarar(V.PLATA, 0.5), temblor=0.0, capa=1)
        lz.relleno(V.elipse_pts(cx, cy, r * 0.7, r * 0.7), V.PLATA, temblor=0.0, capa=1)
        lz.relleno(np.array([[cx - 14, cy - 130], [cx + 14, cy - 130], [cx + 14, cy + 130], [cx - 14, cy + 130]]), V.PLATA_OSC, temblor=0.0, capa=1)
        lz.relleno(np.array([[cx - 130, cy - 14], [cx + 130, cy - 14], [cx + 130, cy + 14], [cx - 130, cy + 14]]), V.PLATA_OSC, temblor=0.0, capa=1)
        L.chispa(lz, cx + 150, cy - 150, 60, 0.4, capa=2)
        M.estrella(lz, 520, 500, 42, capa=2)
        _texto(lz, "ZACATECAS", 790, 120, 130, max_w=520)
        _texto(lz, "¿CÓMO SE", 790, 250, 110, color=(255, 255, 255), max_w=520)
        _texto(lz, "VIVÍA?", 790, 370, 130, color=(255, 255, 255), max_w=520)
    return _fondo_dia(((150, 196, 222), (238, 240, 226)))


VARIANTES = {"bufa": v_bufa, "mina": v_mina, "moneda": v_moneda}
