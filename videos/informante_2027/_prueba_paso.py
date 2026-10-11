# -*- coding: utf-8 -*-
"""Tira del ciclo de caminar (detective y caminante): 8 poses seguidas avanzando lo que toca por fase -> previews/paso.jpg.
El pie apoyado debe quedarse en su marca del suelo y la rodilla doblar solo con el pie en el aire, hacia delante.
    python videos/informante_2027/_prueba_paso.py"""
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [AQUI, os.path.join(AQUI, "..", "..", "nucleo")]
os.chdir(AQUI)

import cv2
import numpy as np

import kit27 as K
from motor import H, W
from noir import Noir
from noir_pers import Detective, avance_paso

h = Noir()
det = Detective()
filas = []
for quien in ("det", "cam"):
    fondo = np.full((H, W, 3), 0.55, np.float32)
    h.nuevo(1.0, fondo)
    h.camara(1.0, W / 2, H / 2, 0.0)
    h.ambiente[:] = 0.9
    s = 0.55
    for k in range(8):
        fase = k * math.pi / 4
        x0 = 130 + k * 232
        if quien == "det":
            x = x0 + fase * avance_paso(Detective.ZANCADA, s)
            det.dibujar(h, dict(x=x, y=800, s=s, d=1, luz=(0.3, -1), paso=fase, andar=1.0, viento=0.2, fumar=0.0, cigarro=False))
        else:
            x = x0 + fase * avance_paso(K.ZANCADA, s)
            K.caminante(h, x, 800, s, fase=fase, sem=40, tono=60, luz=(0.5, -1.0))
        h.trazo(np.array([[x0 - 60, 806.0], [x0 + 170, 806.0]]), 3, 900 + k)
    img = h.acabado(1.0, niebla=None, bloom=0.0, vin=0.0, polvo=0.0)
    filas.append((np.clip(img, 0, 1) * 255).astype(np.uint8)[380:840])
os.makedirs("previews", exist_ok=True)
cv2.imwrite("previews/paso.jpg", cv2.cvtColor(np.vstack(filas), cv2.COLOR_RGB2BGR))
print("ok -> previews/paso.jpg")
