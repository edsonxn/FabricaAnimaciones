# -*- coding: utf-8 -*-
"""Hoja de prueba de los MG nuevos del tramo 3 (27-oct-2026): previews/mg_lol_nuevos.jpg."""
import os
import sys

import cv2
import numpy as np

_D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_D, "..", "..", "nucleo"))
import mg_lol as L

EQ = lambda c: os.path.join(_D, "iconos", "equipos", c + ".png")
JUG = lambda n: os.path.join(_D, "pegatinas", "jugadores", n + ".png")
ICO = lambda c: os.path.join(_D, "iconos", c + ".png")

cap = cv2.VideoCapture(os.path.join(_D, "medios", "_fuente", "j3.mp4"))
cap.set(cv2.CAP_PROP_POS_MSEC, 40000)
fondo = cv2.resize(cap.read()[1], (1920, 1080))

piezas = [
    (L.ficha_jugador(JUG("Smash"), "Smash", EQ("DK"), 1, [("KDA", "10,7", .9), ("Partidas ganadas", "4 de 4", 1.0),
                                                         ("Pentakills", "1", .5)], "azul", "Tirador · DK"), 3.5, []),
    (L.ranking("Mi ranking · día 4", [(EQ("GEN"), "Gen.G", "3-0", "+313 de oro por minuto", "oro"),
                                       (EQ("DK"), "Dplus KIA", "3-0", "4 de 4 partidas", "azul"),
                                       (EQ("T1"), "T1", "2-1", "Solo perdió contra DK", "rojo")]), 3.5, []),
    (L.tabla("Tras dos días", [("2-0", "azul", [(EQ("GEN"), "Gen.G"), (EQ("DK"), "Dplus KIA"), (EQ("MKOI"), "Movistar KOI"),
                                                (EQ("LYON"), "LYON")]),
                               ("0-2", "rojo", [(EQ("AL"), "Anyone's Legend"), (EQ("TLAW"), "Team Liquid"), (EQ("LOS"), "Los Grandes"),
                                                (EQ("TSW"), "Team Secret Whales")])]), 4.0, []),
    (L.calendario("Lo que viene", [("28-30 oct", "Ronda 4", "oro"), ("31 oct", "Ronda 5", "oro"), ("3-6 nov", "Cuartos", "azul"),
                                   ("7-8 nov", "Semifinales\nTexas", "azul"), ("14 nov", "Final\nNueva York", "amarillo")]), 5.0, []),
    (L.barras("Los más elegidos · fase suiza", [(ICO("LeeSin"), "Lee Sin", 12), (ICO("Orianna"), "Orianna", 10),
                                                 (ICO("Renata"), "Renata", 10)], 29), 3.5, []),
    (L.resultados("Ronda 4 · por el pase", [(EQ("MKOI"), "Movistar KOI", EQ("T1"), "T1", None, "28 OCT"),
                                            (EQ("IG"), "Invictus", EQ("LYON"), "LYON", None)]), 3.0, []),
]
hojas = []
for fn, dt, mk in piezas:
    cuadro = fondo.copy()
    m = fn(dt, 6.0, mk)
    esc = min(1.0, 1800 / m.shape[1], 1000 / m.shape[0])
    if esc < 1:
        m = cv2.resize(m, None, fx=esc, fy=esc)
    h, w = m.shape[:2]
    x, y = (1920 - w) // 2, (1080 - h) // 2
    a = m[..., 3:4] / 255.0
    cuadro[y:y + h, x:x + w] = (m[..., :3] * a + cuadro[y:y + h, x:x + w] * (1 - a)).astype(np.uint8)
    hojas.append(cv2.resize(cuadro, (960, 540)))
cv2.imwrite(os.path.join(_D, "previews", "mg_lol_nuevos.jpg"),
            np.vstack([np.hstack(hojas[i:i + 2]) for i in range(0, 6, 2)]), [cv2.IMWRITE_JPEG_QUALITY, 85])
print("ok")
