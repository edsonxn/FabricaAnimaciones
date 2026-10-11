# -*- coding: utf-8 -*-
"""Hoja del reparto (nucleo/noir_corte.py) del video: bustos y cuerpos enteros -> previews/reparto.jpg
    python videos/got_joffrey/_ver_corte.py [t]"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [AQUI, os.path.join(AQUI, "..", "..", "nucleo")]
os.chdir(AQUI)

import cv2
import numpy as np

import noir_color as NC
import noir_feudal as NF
import noir_corte as CO
import reparto as RP

t = float(sys.argv[1]) if len(sys.argv) > 1 else 2.0
h = NC.NoirColor("antorcha")


def cuadro(fn):
    h.nuevo(t, None)
    h.camara(1.0, 960, 540)
    h.rim_color(h.pal["vela"])
    h.pieza(np.array([(-100, -100), (2100, -100), (2100, 1200), (-100, 1200)], float), 60, 1, w=0, d=0, sombra=0, rim=0,
            rampa="muralla", linea=False)
    fn()
    h.ambiente[:] = np.array(h.pal["luna"], np.float32) * 0.45
    h.luz_radial(1500, 200, 1600, h.pal["vela"], k=1.2)
    return (np.clip(h.acabado(t, niebla=None), 0, 1) * 255).astype(np.uint8)


tiles = []
bustos = [("rey", RP.REY, dict(sonrisa=0.5, ceño=0.4)), ("rey ahogo", RP.REY, dict(ahogo=0.9, manos_cuello=1.0)),
          ("enano", RP.ENANO, dict(ceño=0.3)), ("reina", RP.REINA, dict(ceño=0.8, boca=0.4)),
          ("sansa", RP.SANSA, dict(mira=-0.4)), ("anciana", RP.ANCIANA, dict(sonrisa=0.3)),
          ("menique", RP.MENIQUE, dict(sonrisa=0.4)), ("dontos", RP.DONTOS, dict(boca=0.2))]
for nom, kw, extra in bustos:
    b = CO.BustoCorte(sem=5, **kw)
    im = cuadro(lambda: b.dibujar(h, dict(x=820, y=430, s=1.0, d=1, luz=(0.9, -0.5), **extra)))
    sm = cv2.resize(im, (640, 360), interpolation=cv2.INTER_AREA)
    cv2.putText(sm, nom, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    tiles.append(sm)


def cuerpos():
    for i, kw in enumerate([RP.REY, RP.REINA, RP.ENANO, RP.SANSA, RP.ANCIANA, RP.MENIQUE, RP.DONTOS]):
        c = CO.Cortesano(sem=10 + i, **kw)
        mano = (70, -330) if i == 0 else None
        c.dibujar(h, dict(x=160 + i * 260, y=1000, s=1.35, d=1, luz=(0.6, -1.0), mano=mano))


im = cuadro(cuerpos)
cv2.imwrite("previews/reparto_cuerpos.png", cv2.cvtColor(im, cv2.COLOR_RGB2BGR))
hoja = np.vstack([np.hstack(tiles[i:i + 4]) for i in range(0, 8, 4)])
cv2.imwrite("previews/reparto.jpg", cv2.cvtColor(hoja, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
print("-> previews/reparto.jpg, previews/reparto_cuerpos.png")
