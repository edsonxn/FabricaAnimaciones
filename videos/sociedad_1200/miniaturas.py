# -*- coding: utf-8 -*-
"""Miniaturas (python fab.py sociedad_1200 miniatura).
Estilo Film Noir: claroscuro brutal, sombras de persiana, humo, sello clasificado,
y 2-3 palabras enormes legibles en pantalla pequeña (móvil).
"""
import math
import numpy as np
import cv2

from basen import lienzo
import comun as C
import noir_real as R
import kit27 as K
import mundos as MU
import mundos27 as M27
import noir as N
from noir_pers import Busto
from motor import H, W, NEGRO, BLANCO

T = 1.0
WOB = 0.0
ROJO = (235, 42, 42)
AMARILLO = (255, 214, 64)
BLANCO_P = (255, 252, 244)


def _texto(lz, s, x, y, px, rot=-0.02, color=BLANCO_P, borde=NEGRO, borde_px=None):
    if borde_px is None:
        borde_px = px * 0.14
    lz.texto(s, x, y, px, "black", color=color, borde=borde, borde_px=borde_px, rot=rot, capa=2, temblor=0.0)


def conspiracion(lz):
    """Variante 1: Detective en silueta con humo, persiana y texto CONSPIRARON."""
    h = lienzo()
    h.nuevo(1.2, None)
    h.camara(1.05, 960, 540, 0.0)
    MU.oficina().pegar(h, 1.0, dx=-200)

    busto = Busto(sem=11)
    p = dict(x=460, y=560, s=1.18, d=1, luz=(0.95, -0.4), brasa=1.0, arriba=0.25, rot=-0.02)
    busto.dibujar(h, p)
    tip = busto.punta(dict(x=460, y=560, s=1.18, d=1))
    N.humo(h, 1.2, tip[0], tip[1], k=1.4, ancho=2.5, viento=(40, -130))
    h.luz_radial(tip[0], tip[1], 240, (1.0, 0.9, 0.7), k=1.5)

    # Persiana y luz dramática
    h.ambiente[:] = 0.28
    h.luz_persiana(np.array([[-300, -400], [1600, -450], [1600, 750], [-400, 1000]]), k=1.8, n=14, abierto=0.55)
    h.luz_radial(1400, 200, 900, (1.2, 1.2, 1.2), k=2.5)

    # Sello clasificado
    N.sello(h, "CLASIFICADO", 1400, 320, 100, 1.2, 0.0, rot=-8.0, tono=0.02, alfa=0.98)

    # Texto gigante en lienzo
    _texto(lz, "1.200 IAs", 1300, 560, 180, rot=-0.02, color=AMARILLO, borde=NEGRO)
    _texto(lz, "CONSPIRARON", 1300, 760, 136, rot=0.01, color=BLANCO_P, borde=ROJO, borde_px=20)

    return h.acabado(1.2, niebla=dict(dens=0.18, vel=10, y0=-200, y1=900, sube=False))


def altman(lz):
    """Variante 2: Retrato real de Sam Altman con expediente y sello TOP SECRET."""
    h = lienzo()
    h.nuevo(1.5, None)
    h.camara(1.04, 960, 540, 0.0)
    M27.despacho().pegar(h, 1.0)

    # Retrato de Sam Altman en marco noir
    R.retrato_noir(h, "sam_altman", 560, 530, 540, 1.5, 0.0, rotulo="SAM ALTMAN", leyenda="OpenAI · San Francisco")

    # Iluminación
    h.luz_radial(560, 480, 700, (1.2, 1.2, 1.2), k=2.3)
    h.luz_persiana(np.array([[200, -200], [1920, -200], [1920, 1080], [200, 1080]]), k=1.4, n=12, abierto=0.5)

    # Sello de expediente
    N.sello(h, "CONFIDENCIAL", 1380, 280, 95, 1.5, 0.0, rot=-6.0, tono=0.03, alfa=0.95)

    # Texto en el tercio derecho
    _texto(lz, "SOCIEDAD", 1380, 540, 185, rot=-0.02, color=BLANCO_P, borde=NEGRO)
    _texto(lz, "SECRETA", 1380, 740, 205, rot=0.01, color=ROJO, borde=NEGRO, borde_px=24)

    return h.acabado(1.5, niebla=dict(dens=0.14, vel=8, y0=0, y1=1000, sube=False))


def rebelion(lz):
    """Variante 3: Servidores en penumbra, pantalla de hackeo y APRENDIERON A MENTIR."""
    h = lienzo()
    h.nuevo(1.8, None)
    h.camara(1.03, 960, 540, 0.0)
    M27.laboratorio().pegar(h, 1.0)

    import props as P
    P.caja_negra(h, 480, 840, s=1.4, led=1.0, t=1.8)
    N.humo(h, 1.8, 480, 800, k=1.2, ancho=3.0, viento=(-20, -100))

    # Luz de los servidores y terminal
    h.luz_radial(480, 520, 650, (0.8, 1.2, 0.9), k=2.4)
    h.luz_radial(1400, 360, 850, (1.1, 1.1, 1.1), k=2.0)

    N.sello(h, "SIN AISLAMIENTO", 1380, 280, 85, 1.8, 0.0, rot=-9.0, tono=0.04, alfa=0.96)

    # Texto
    _texto(lz, "APRENDIERON", 1300, 540, 136, rot=-0.02, color=BLANCO_P, borde=NEGRO)
    _texto(lz, "A MENTIR", 1300, 750, 185, rot=0.02, color=AMARILLO, borde=NEGRO, borde_px=22)

    return h.acabado(1.8, niebla=dict(dens=0.20, vel=12, y0=-100, y1=900, sube=False))


VARIANTES = {
    "conspiracion": conspiracion,
    "altman": altman,
    "rebelion": rebelion,
}
