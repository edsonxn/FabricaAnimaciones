# -*- coding: utf-8 -*-
"""Hoja con todos los íconos del catálogo (ICONOS) en el estilo activo -> previews/catalogo_iconos.png
Uso: python fab.py <video> catalogo"""
import os

import cv2
import numpy as np

import escena_base as B
from motor import Lienzo, a_uint8, componer

nombres = sorted(B.ICONOS)
cols, filas = 6, (len(nombres) + 5) // 6
lz = Lienzo()
tiles = []
for n in nombres:
    lz.nuevo(1.0)
    B.dibujar_icono(lz, n, 960, 540, 1.6, 1.0)
    lz.texto(n, 960, 1010, 70, "black", color=(255, 255, 255), borde=(20, 16, 24), borde_px=8, temblor=0, capa=2)
    img = componer(B.fondo_estilo("libre", 1.0), lz.resolver(), boil=0)
    tiles.append(cv2.resize(a_uint8(np.clip(img, 0, 1)), (320, 180), interpolation=cv2.INTER_AREA))
while len(tiles) % cols:
    tiles.append(np.zeros_like(tiles[0]))
hoja = np.vstack([np.hstack(tiles[i:i + cols]) for i in range(0, len(tiles), cols)])
os.makedirs("previews", exist_ok=True)
cv2.imwrite("previews/catalogo_iconos.png", cv2.cvtColor(hoja, cv2.COLOR_RGB2BGR))
print("previews/catalogo_iconos.png", len(nombres), "íconos")
