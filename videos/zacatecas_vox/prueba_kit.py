# -*- coding: utf-8 -*-
"""Hoja de prueba de los ciclos de personajes del kit Vox (uso: python fab-like con PYTHONPATH=video;nucleo)."""
import sys
import cv2
import numpy as np
import estilos
estilos.activar("vox")
import fondos as F
import vox as V
from motor import Lienzo, componer, a_uint8, W, H

lz = Lienzo()
tiles = []
def hoja(nombre, fn, n=8):
    for f in range(n):
        lz.nuevo(0.0, wob=0.6)
        bg = F.papel(0)
        lz.M = np.array([[1.0, 0, 0], [0, 1, 0], [0, 0, 1]])
        fn(lz, f)
        img = componer(bg, lz.resolver(), boil=0)
        im = cv2.resize(a_uint8(np.clip(img, 0, 1)), (270, 480), interpolation=cv2.INTER_AREA)
        cv2.putText(im, f"{nombre} {f}", (6, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        tiles.append(im)

def cam(lz, f):
    V.figura(lz, 380, 1100, 3.0, V.CAMINAR[f], "tolosa", 1, obj=[("d", "bolsa", 20, 0.6)])
def cam2(lz, f):
    V.figura(lz, 620, 1100, 3.0, V.CAMINAR[f], "indigena", -1, obj=[])
def pic(lz, f):
    V.figura(lz, 540, 1100, 3.0, V.PICAR[f], "minero", 1, obj=[("d", "barreta", 0, 1.0)])
def sub(lz, f):
    V.figura(lz, 540, 1100, 3.0, V.SUBIR[f], "cargador", 1, carga=("tenate", 1.0))
def arc(lz, f):
    V.figura(lz, 540, 1100, 3.0, V.ARCO[f % 7], "guachichil", 1, obj=[("arco", 1.0)])
def mul(lz, f):
    V.mula(lz, 540, 1100, 2.2, f, 1, "barras")

hoja("tolosa", cam)
hoja("indigena", cam2)
hoja("pica", pic, 6)
hoja("sube", sub)
hoja("arco", arc, 7)
hoja("mula", mul)
cols = 8
while len(tiles) % cols:
    tiles.append(np.zeros_like(tiles[0]))
sheet = np.vstack([np.hstack(tiles[i:i + cols]) for i in range(0, len(tiles), cols)])
cv2.imwrite("previews/kit.jpg", cv2.cvtColor(sheet, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 88])
print("ok", sheet.shape)
