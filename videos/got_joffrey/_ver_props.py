# -*- coding: utf-8 -*-
"""Hoja de la utilería animada (props_j.py) -> previews/props.jpg    python videos/got_joffrey/_ver_props.py [t]"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [AQUI, os.path.join(AQUI, "..", "..", "nucleo")]
os.chdir(AQUI)

import cv2
import numpy as np

import noir_color as NC
import noir_feudal as NF  # noqa: F401
import noir_corte as CO  # noqa: F401
import props_j as P

t = float(sys.argv[1]) if len(sys.argv) > 1 else 1.3
h = NC.NoirColor("antorcha")

ITEMS = [
    ("candelabro", lambda: P.candelabro(h, t, 960, 600, 300, s=1.2, cadena=600)),
    ("caliz", lambda: P.caliz(h, 960, 900, 2.4, 0.0)),
    ("empanada", lambda: (P.empanada(h, t, 960, 800, 1.6, corte=0.5), P.palomas(h, t, t - 0.5, 960, 500, n=9, s=1.4))),
    ("espada+jarra", lambda: (P.espada(h, 300, 400, 0.1, 1.6), P.jarra(h, 900, 950, 2.0))),
    ("musicos", lambda: (P.musico(h, t, 600, 900, 2.2, "laud"), P.musico(h, t, 1300, 900, 2.2, "tambor", sem=4))),
    ("veneno", lambda: (P.cristales(h, t, 600, 800, 2.4), P.frasco(h, t, 1300, 900, 2.4))),
    ("puno", lambda: (P.puno(h, 900, 400, 1.6, 0.0), P.puno(h, 900, 800, 1.6, 1.0))),
    ("collar", lambda: P.collar_grande(h, t, 960, 300, 1.6, falta=3)),
    ("cofre", lambda: P.cofre(h, t, 960, 850, 2.0, abre=0.8)),
    ("ballesta", lambda: (P.ballesta(h, 700, 500, 2.0), P.saeta(h, 1300, 800, -0.2, 2.0))),
    ("barca", lambda: P.barca(h, t, 960, 700, 2.4)),
    ("rosas+monedas", lambda: ([P.rosa(h, t, 400 + k * 200, 400, 2.0, sem=k) for k in range(4)], P.monedas(h, t, 1200, 900, 10, 3.0))),
]
tiles = []
for nom, fn in ITEMS:
    h.nuevo(t, None)
    h.camara(1.0, 960, 540)
    h.rim_color(h.pal["vela"])
    h.pieza(np.array([(-100, -100), (2100, -100), (2100, 1200), (-100, 1200)], float), 50, 1, w=0, d=0, sombra=0, rim=0,
            rampa="madera", linea=False)
    fn()
    h.ambiente[:] = np.array(h.pal["luna"], np.float32) * 0.5
    h.luz_radial(1300, 200, 1600, h.pal["vela"], k=1.2)
    im = (np.clip(h.acabado(t, niebla=None), 0, 1) * 255).astype(np.uint8)
    sm = cv2.resize(im, (480, 270), interpolation=cv2.INTER_AREA)
    cv2.putText(sm, nom, (8, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    tiles.append(sm)
while len(tiles) % 4:
    tiles.append(np.zeros_like(tiles[0]))
hoja = np.vstack([np.hstack(tiles[i:i + 4]) for i in range(0, len(tiles), 4)])
cv2.imwrite("previews/props.jpg", cv2.cvtColor(hoja, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
print("-> previews/props.jpg")
