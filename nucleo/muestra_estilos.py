# -*- coding: utf-8 -*-
"""Renderiza el mismo instante del video en todos los estilos -> previews/estilos.jpg
Uso (vía fab.py): python fab.py <video> estilos <t>"""
import os
import sys

import cv2
import numpy as np

import estilos
from render import Renderizador

t = float(sys.argv[1]) if len(sys.argv) > 1 else 10.0
R = Renderizador()
os.makedirs("previews", exist_ok=True)
tiles = []
for nombre in estilos.ESTILOS:
    estilos.activar(nombre)
    im = R.cuadro(t)
    sm = cv2.resize(im, (640, 360), interpolation=cv2.INTER_AREA)
    cv2.rectangle(sm, (0, 0), (640, 34), (0, 0, 0), -1)
    cv2.putText(sm, nombre, (10, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
    tiles.append(sm)
    print("ok", nombre)
while len(tiles) % 3:
    tiles.append(np.zeros_like(tiles[0]))
hoja = np.vstack([np.hstack(tiles[i:i + 3]) for i in range(0, len(tiles), 3)])
cv2.imwrite("previews/estilos.jpg", cv2.cvtColor(hoja, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
print("previews/estilos.jpg")
