# -*- coding: utf-8 -*-
"""Hoja de prueba de tablero_suizo, premio y llave: previews/mg_nuevos.jpg."""
import os
import sys

import cv2
import numpy as np

_D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_D, "..", "..", "nucleo"))
import mg_lol as L

EQ = lambda c: os.path.join(_D, "iconos", "equipos", c + ".png")
JUG = lambda n: os.path.join(_D, "pegatinas", "jugadores", n + ".png")
LOG = {c: EQ(c) for c in "DK GEN T1 MKOI LYON IG BLG TES KC CFO HLE G2 LOS TLAW TSW AL".split()}
COLS = [("A cuartos", "verde"), ("2-1", "oro"), ("2-2", "oro"), ("1-2", "oro"), ("Eliminados", "rojo")]
E0 = [["DK", "GEN"], ["T1", "MKOI", "LYON", "IG", "BLG", "TES"], [], ["KC", "CFO", "HLE", "G2", "LOS", "TLAW"], ["TSW", "AL"]]
E1 = [["DK", "GEN", "T1", "IG", "TES"], [], ["MKOI", "LYON", "BLG", "KC", "LOS", "HLE"], [], ["TSW", "AL", "CFO", "TLAW", "G2"]]
s = L.tablero_suizo("Así va la fase suiza", COLS, LOG, [E0, E1])
piezas = [(s, 1.2, [2.0]), (s, 2.9, [2.0]), (s, 5.5, [2.0]),
          (L.premio("MVP de la semana", JUG("Faker"), "Faker", EQ("T1"), ["Dato de prueba uno", "Dato dos", "Dato tres"],
                    sub="Medio · T1", sello="MVP"), 3.8, [1, 1.5, 2, 2.6]),
          (L.premio("Lo peor de la semana", JUG("Faker"), "Faker", EQ("T1"), ["Dato de prueba uno"], color="rojo", gris=True,
                    sello="LO PEOR"), 3.8, [1, 2]),
          (L.llave("Cuartos de final", [(EQ("DK"), "DK", EQ("T1"), "T1", "3 nov"), (EQ("GEN"), "Gen.G", EQ("IG"), "IG", "4 nov"),
                                        (EQ("TES"), "TES", EQ("KC"), "KC", "5 nov"), (EQ("HLE"), "HLE", EQ("LOS"), "LOS", "6 nov")]),
           5.5, [.4, .9, 1.4, 1.9, 3])]
fondo = np.full((1080, 1920, 3), 40, np.uint8)
h = []
for fn, dt, mk in piezas:
    c = fondo.copy()
    m = fn(dt, 8.0, mk)
    e = min(1.0, 1880 / m.shape[1], 1040 / m.shape[0])
    if e < 1:
        m = cv2.resize(m, None, fx=e, fy=e)
    hh, w = m.shape[:2]
    x, y = (1920 - w) // 2, (1080 - hh) // 2
    a = m[..., 3:4] / 255.0
    c[y:y + hh, x:x + w] = (m[..., :3] * a + c[y:y + hh, x:x + w] * (1 - a)).astype(np.uint8)
    h.append(cv2.resize(c, (960, 540)))
os.makedirs(os.path.join(_D, "previews"), exist_ok=True)
cv2.imwrite(os.path.join(_D, "previews", "mg_nuevos.jpg"), np.vstack([np.hstack(h[i:i + 2]) for i in range(0, 6, 2)]),
            [cv2.IMWRITE_JPEG_QUALITY, 85])
print("ok")
