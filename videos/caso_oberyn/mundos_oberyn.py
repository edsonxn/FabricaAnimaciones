# -*- coding: utf-8 -*-
"""Mundos y fondos originales de «El caso de la Víbora Roja» (estilo noir medieval en tinta y aguada).
Fondos pintados una sola vez por proceso (lru_cache) en capas con paralaje.
"""
import functools
import math
import numpy as np

from motor import H, W
from noir import fbm
from noir_fondos import Lienzo


@functools.lru_cache(maxsize=1)
def cielo_tormenta():
    """Cielo de Desembarco del Rey: nubes espesas, luna velada y atmósfera pesada."""
    L = Lienzo(3200, 1400, origen=(-600, -300), base=0.0, sem=101)
    L.poli([(-600, -300), (2600, -300), (2600, 1100), (-600, 1100)], 0.22, tex=0.04, grad=(0.38, -300, 1000))
    L.brillo(420, 140, 280, 0.65, tono=0.75)
    L.elipse(420, 140, 44, 44, 0.90, tex=0.02, emis=0.5)

    n = 0.65 * fbm(L.w, L.h, 240, 5, 102) + 0.35 * fbm(L.w, L.h, 70, 3, 103)
    yy = np.arange(L.h, dtype=np.float32)[:, None]
    banda = np.clip(1 - np.abs(yy - 500) / 600, 0, 1)
    nube = np.clip((n * 0.55 + banda * 0.9 - 0.55) * 2.0, 0, 1)
    L.g = L.g * (1 - nube * 0.65) + nube * 0.16
    return L.capa(opaco=True)


@functools.lru_cache(maxsize=1)
def muralla_capital():
    """Silueta lejana de las murallas y torreones de Desembarco del Rey (profundidad 0.4)."""
    L = Lienzo(3400, 1600, origen=(-500, -800), sem=110)
    rng = np.random.default_rng(110)

    # Base de la muralla
    L.poli([(-500, 500), (2900, 500), (2900, 1200), (-500, 1200)], 0.14, tex=0.08)

    # Almenas y torres
    x = -400
    while x < 2800:
        an = rng.uniform(80, 160)
        al = rng.uniform(220, 480)
        # Torre
        L.poli([(x, 500 - al), (x + an, 500 - al), (x + an, 500), (x, 500)], 0.18, tex=0.06)
        # Tejado cónico / almenas
        if rng.uniform() < 0.4:
            L.poli([(x - 10, 500 - al), (x + an / 2, 500 - al - 90), (x + an + 10, 500 - al)], 0.22, tex=0.05)
        else:
            for cx in range(int(x), int(x + an), 28):
                L.poli([(cx, 500 - al - 22), (cx + 18, 500 - al - 22), (cx + 18, 500 - al), (cx, 500 - al)], 0.18)
        x += an + rng.uniform(30, 90)

    return L.capa()


@functools.lru_cache(maxsize=1)
def foso_arena():
    """El foso de combate de Desembarco del Rey: muro perimetral de sillar y suelo adoquinado/arena."""
    L = Lienzo(3200, 1800, origen=(-400, -600), sem=120)

    # Muro de sillería al fondo
    L.poli([(-400, 200), (2800, 200), (2800, 720), (-400, 720)], 0.26, tex=0.12)
    # Líneas de sillar
    for y in range(200, 720, 48):
        L.linea([(-400, y), (2800, y)], w=2.0, tono=0.08)

    # Suelo del foso / arena
    L.poli([(-400, 720), (2800, 720), (2800, 1400), (-400, 1400)], 0.38, tex=0.18, grad=(0.55, 720, 1300))
    # Piedras / marcas de sangre vieja en el suelo
    rng = np.random.default_rng(121)
    for _ in range(60):
        px = rng.uniform(-300, 2700)
        py = rng.uniform(760, 1350)
        rw, rh = rng.uniform(12, 34), rng.uniform(6, 16)
        L.elipse(px, py, rw, rh, rng.uniform(0.18, 0.28), tex=0.02)

    return L.capa()


@functools.lru_cache(maxsize=1)
def gran_salon():
    """Gran salón de audiencias: arcadas góticas oscuras, columnas y vanos con claroscuro."""
    L = Lienzo(3000, 1800, origen=(-300, -600), sem=130)

    # Fondo oscuro
    L.poli([(-300, -600), (2700, -600), (2700, 1200), (-300, 1200)], 0.10, tex=0.04)

    # Columnas masivas
    for cx in (-100, 450, 1000, 1550, 2100):
        # Fuste
        L.poli([(cx - 70, -500), (cx + 70, -500), (cx + 85, 750), (cx - 85, 750)], 0.24, tex=0.10)
        # Capiteles / arcos
        L.poli([(cx - 110, -500), (cx + 110, -500), (cx + 70, -420), (cx - 70, -420)], 0.32, tex=0.08)
        # Base de la columna
        L.poli([(cx - 100, 750), (cx + 100, 750), (cx + 110, 820), (cx - 110, 820)], 0.30, tex=0.08)

    # Suelo de losas reflectantes
    L.poli([(-300, 820), (2700, 820), (2700, 1400), (-300, 1400)], 0.28, tex=0.06, grad=(0.42, 820, 1300))
    for y in range(820, 1400, 60):
        L.linea([(-300, y), (2700, y)], w=2.5, tono=0.08)

    return L.capa()
