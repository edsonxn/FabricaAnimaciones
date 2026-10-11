# -*- coding: utf-8 -*-
"""Hoja de pruebas de props: desde la carpeta de un video vertical: python ../../nucleo/sh_hoja.py  -> previews/props_N.png"""
import cv2
import numpy as np

import boceto as B
import sh_kit as K
import sh_props as X
from motor import H, W


def hoja(items, fondo=(40, 60, 110)):
    h = B.Hoja()
    h.limpiar()
    f = np.empty((H, W, 3), np.float32)
    f[:] = np.array(fondo, np.float32) / 255
    h.fondo = f
    for d, x, y, s in items:
        K.poner(h, d, x, y, s)
    return h


def guardar(h, ruta):
    img = np.clip(h.componer(), 0, 1)
    cv2.imwrite(ruta, cv2.cvtColor((img * 255).astype(np.uint8), cv2.COLOR_RGB2BGR))


if __name__ == "__main__":
    a = [(X.platano(), 270, 200, 1.0), (X.platano("miedo", "grito"), 780, 200, 0.8), (X.trebol(), 100, 440, 1.0), (X.detector(0.4), 330, 520, 0.9),
         (X.diente(), 560, 450, 0.9), (X.balanza(0.15), 800, 520, 0.8), (X.aureola(), 120, 640, 1.0), (X.tache(), 220, 640, 1.0), (X.palomita(), 320, 640, 1.0),
         (X.medalla(), 420, 650, 1.0), (X.luna(), 160, 860, 1.0), (X.tierra(), 440, 860, 1.0), (X.astronauta(), 700, 860, 0.9), (X.espejo_lunar(), 910, 860, 0.7),
         (X.regla(), 40, 1080, 1.0), (X.dedo_una(30), 480, 1100, 0.9), (X.reloj_cara(0.2), 640, 1100, 0.9), (X.sol_disco(corona=1), 860, 1100, 0.8),
         (X.nube(), 250, 1380, 0.9), (X.nube("miedo", "grito", True), 760, 1380, 0.8), (X.gotita(), 100, 1620, 1.0), (X.elefante(), 360, 1640, 0.9),
         (X.flecha_arriba(), 600, 1640, 0.8), (X.paraguas(), 800, 1640, 0.8), (X.mano(0), 120, 1860, 0.5), (X.mano(2, "grandes", "o"), 300, 1860, 0.5)]
    guardar(hoja(a), "previews/props_1.png")
    b = [(X.mano(0), 180, 300, 1.0), (X.mano(1), 540, 300, 1.0), (X.mano(2, "miedo", "grito"), 900, 300, 1.0), (X.neumatico(), 150, 700, 1.0),
         (X.cerebro(), 400, 700, 1.0), (X.pez(), 700, 700, 1.0), (X.roca(), 920, 720, 0.8), (X.ojo(0.5, 0.2), 250, 1000, 1.0), (X.prisma(), 560, 1000, 1.0),
         (X.marte(), 860, 1000, 1.0), (X.persona if False else K.persona("grandes", "o", "tele"), 250, 1400, 0.9), (K.espalda(), 700, 1400, 0.7),
         (X.balanza(-0.2), 540, 1750, 0.8)]
    guardar(hoja(b), "previews/props_2.png")
    print("listo")
