# -*- coding: utf-8 -*-
"""Prueba del detective noir: varias poses en una hoja."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "nucleo"))
import cv2
import numpy as np

from noir import Noir, gris, humo, lluvia
from noir_pers import Detective, Figura
from motor import W, H

h = Noir()
det = Detective()
poses = [dict(fumar=0.0), dict(fumar=1.0, brasa=1.0), dict(giro=0.5, arriba=0.6), dict(andar=1.0, paso=0.8, viento=0.5)]
tiles = []
for i, pp in enumerate(poses):
    t = 1.0 + i * 0.37
    fondo = np.full((H, W, 3), 0.42, np.float32)
    h.nuevo(t, fondo)
    h.ambiente[:] = 0.22
    p = dict(x=W / 2 - 60, y=1000, s=1.5, d=1, viento=0.2, luz=(0.35, -1))
    p.update(pp)
    det.dibujar(h, p)
    h.luz_cono(W / 2 + 60, -40, np.pi / 2 + 0.05, 0.42, 1250, (1.25, 1.25, 1.25), suave=0.45)
    tip = det.punta_cigarro(p)
    humo(h, t, tip[0], tip[1], k=1.0)
    lluvia(h, t, n=500)
    img = h.acabado(t, niebla=dict(dens=0.25))
    tiles.append(cv2.resize((img * 255).astype(np.uint8), (W // 2, H // 2)))
hoja = np.vstack([np.hstack(tiles[:2]), np.hstack(tiles[2:])])
os.makedirs("previews", exist_ok=True)
cv2.imwrite("previews/prueba_det.jpg", hoja)
cv2.imwrite("previews/prueba_det_full.png", (img * 255).astype(np.uint8))
print("ok")
