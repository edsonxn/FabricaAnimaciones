# -*- coding: utf-8 -*-
"""Hoja de control del mapa «us» por épocas: python _hoja_mapa.py -> previews/hoja_mapa.jpg (2x3, cuadros 960x540)."""
import os

import cv2
import numpy as np

import mapa as M

M.usar("us")
C = M.COL
EPOCAS = [
    ("base", []),
    ("1750", [("trece", C["colonias"]), ("nueva_francia", C["francia"]), ("nueva_espana", C["espana"])]),
    ("1783", [("eeuu_1783", C["eeuu"]), ("espana_1783", C["espana"]), ("canada", C["inglaterra"])]),
    ("1803", [("eeuu_1783", C["eeuu"]), ("luisiana_1803", C["luisiana"]), ("mexico_1824", C["mexico"]), ("oregon_1846", C["oregon"])]),
    ("1848", [("eeuu_1846", C["eeuu"]), ("perdido_1848", C["perdido"]), ("mexico_mod", C["mexico"])]),
    ("1861", [("union", C["union"]), ("confederacion", C["confederacion"]), ("fronterizos", C["fronterizos"])]),
]
cam = M.Cam(-95.0, 37.0, 0.70)
cuadros = []
for nombre, capas in EPOCAS:
    img, base = M.pintar_base(cam)
    for k, (campo, col) in enumerate(capas):
        M.pintar(img, cam.proyectar(M.CAMPOS[campo]), col, 0.80, k, luz=base.luz)
    M.pintar_rios(img, cam, base)
    im = (np.clip(img, 0, 1) * 255).astype(np.uint8)[..., ::-1]
    im = cv2.resize(im, (960, 540), interpolation=cv2.INTER_AREA)
    cv2.putText(im, nombre, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (20, 20, 20), 3)
    cuadros.append(im)
hoja = np.vstack([np.hstack(cuadros[i:i + 2]) for i in range(0, 6, 2)])
os.makedirs("previews", exist_ok=True)
cv2.imwrite("previews/hoja_mapa.jpg", hoja, [cv2.IMWRITE_JPEG_QUALITY, 88])
print("previews/hoja_mapa.jpg")
