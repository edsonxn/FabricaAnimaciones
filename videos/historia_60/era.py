# -*- coding: utf-8 -*-
"""Base de las épocas del video 'historia_60': tabla de tiempos (en pulsos), clase Era y render de una época a imagen."""
import math

import numpy as np
import cv2

from escena_base import TL, F
from motor import W, H, Lienzo, componer, mat_r, mat_s, mat_t, prog, smooth, e_out, e_in, e_inout, e_back
from ritmo import env_bombo
import kit as K

BEAT = TL["beat"]
D_TR = 0.75                      # duración de cada transición-portal (s); termina justo en el pulso de la nueva época

# (id, pulsos, años atrás, título, subtítulo)
TABLA = [
    ("sapiens", 8, 200000, "NACE HOMO SAPIENS", "África · hace 200 000 años"),
    ("africa", 8, 70000, "SALIMOS DE ÁFRICA", "Y poblamos el planeta"),
    ("arte", 8, 45000, "NACE EL ARTE", "Cuevas de Sulawesi y Europa"),
    ("agricultura", 6, 11000, "LA AGRICULTURA", "Creciente Fértil"),
    ("rueda", 6, 5525, "LA RUEDA", "Mesopotamia"),
    ("escritura", 6, 5425, "LA ESCRITURA", "Sumer · cuneiforme"),
    ("piramides", 6, 4585, "LAS PIRÁMIDES", "Guiza, Egipto"),
    ("grecia", 6, 2533, "ATENAS: DEMOCRACIA", "Y filosofía"),
    ("roma", 6, 1945, "ROMA: UN IMPERIO", "Caminos, leyes y coliseos"),
    ("imprenta", 6, 585, "LA IMPRENTA", "Gutenberg"),
    ("oceano", 6, 533, "1492: CRUZAR EL OCÉANO", "Dos mundos se encuentran"),
    ("telescopio", 6, 415, "EL TELESCOPIO", "Galileo y las lunas de Júpiter"),
    ("vapor", 6, 256, "LA REVOLUCIÓN INDUSTRIAL", "Máquina de vapor"),
    ("luz", 6, 146, "LA LUZ ELÉCTRICA", "Edison"),
    ("vuelo", 6, 122, "POR FIN VOLAMOS", "Hermanos Wright"),
    ("luna", 5, 56, "UN PASO EN LA LUNA", "Apolo 11"),
    ("web", 5, 34, "NACE LA WEB", "Internet para todos"),
    ("smartphone", 5, 18, "EL MUNDO EN TU BOLSILLO", "Smartphones"),
    ("hoy", 17, 0, "HOY", "8 000 millones de personas"),
]
assert sum(x[1] for x in TABLA) == 128, sum(x[1] for x in TABLA)
INICIOS = [0.0]
for _x in TABLA[:-1]:
    INICIOS.append(INICIOS[-1] + _x[1] * BEAT)
FIN = TL["total"]


class Era:
    """Una época. Subclases: fondo(t) -> imagen, cam(t) -> (zoom, rot, dx, dy), dibujar(lz, t), sfx(ev), salida(t) -> (x,y)."""
    COL_SALIDA = (255, 255, 255)

    def __init__(self, k):
        self.k = k
        self.id, self.beats, self.ya, self.titulo, self.sub = TABLA[k]
        self.T0 = INICIOS[k]
        self.T1 = INICIOS[k + 1] if k + 1 < len(INICIOS) else FIN
        self.preparar()

    def a(self, pulsos):
        """Instante global (s) del pulso `pulsos` de esta época (0 = su primer pulso; puede ser negativo)."""
        return self.T0 + pulsos * BEAT

    def preparar(self):
        pass

    def fondo(self, t):
        return K.degradado_img((20, 20, 60), (60, 40, 100))

    def cam(self, t):
        return 1.0, 0.0, 0.0, 0.0

    def dibujar(self, lz, t):
        pass

    def sfx(self, ev):
        pass

    def salida(self, t):
        return (W / 2, H / 2 - 100)

    def entrada(self, t):
        return self.salida(self.T0)


def matriz_cam(cam, t):
    z, rot, dx, dy = cam
    z *= 1 + 0.012 * env_bombo(t)
    return mat_t(W / 2 + dx, H / 2 + dy) @ mat_r(rot) @ mat_s(z) @ mat_t(-W / 2, -H / 2)


def img_era(lz, era, t, zt=1.0, pc=(W / 2, H / 2)):
    """Dibuja la época `era` en el instante t; zt/pc = zoom extra (para el portal) alrededor del punto pc."""
    lz.nuevo(t, wob=0.0)
    bg = era.fondo(t)
    M = matriz_cam(era.cam(t), t)
    if zt != 1.0:
        Mz = mat_t(pc[0], pc[1]) @ mat_s(zt) @ mat_t(-pc[0], -pc[1])
        M = Mz @ M
        bg = cv2.warpAffine(bg, Mz[:2], (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    lz.M = M
    era.dibujar(lz, t)
    lz.M = np.eye(3)
    return componer(bg, lz.resolver(), boil=lz.boil)
