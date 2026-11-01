# -*- coding: utf-8 -*-
"""Prueba del mapa: python _mapa_test.py -> previews/mapa_test.jpg (base + territorios en varias cámaras)."""
import sys

import cv2
import numpy as np

import boceto as B
import mapa as M

M.cargar()
M.usar("eg")
casos = [
    ((34.0, 27.0, 1.0), None),
    ((31.2, 27.0, 2.4), "reino_antiguo"),
    ((31.0, 30.4, 8.0), "bajo"),
    ((34.0, 29.0, 1.6), "reino_nuevo"),
    ((34.0, 33.0, 1.1), "persia"),
    ((31.5, 33.0, 1.1), "otomano"),
    ((35.5, 35.0, 3.0), "hititas"),
    ((32.0, 24.0, 4.0), "nasser"),
    ((33.0, 32.0, 1.4), "roma"),
]
if len(sys.argv) > 1:
    casos = [((float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])), sys.argv[4] if len(sys.argv) > 4 else None)]
tiles = []
for (lon, lat, z), campo in casos:
    cam = M.Cam(lon, lat, z)
    img, base = M.pintar_base(cam, 0)
    if campo:
        S = cam.proyectar(M.CAMPOS[campo])
        M.pintar(img, S, (204, 74, 58) if campo != "nasser" else M.AGUA_LAGO, 0.86, 0, luz=base.luz)
    M.pintar_valle(img, cam, base)
    M.pintar_rios(img, cam, base)
    im = (np.clip(img, 0, 1)[..., ::-1] * 255).astype(np.uint8)
    s = cv2.resize(im, (960, 540), interpolation=cv2.INTER_AREA)
    cv2.putText(s, f"{lon},{lat} z{z} {campo}", (10, 530), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    tiles.append(s)
    if len(casos) == 1:
        cv2.imwrite("previews/mapa_full.jpg", im)
while len(tiles) % 3:
    tiles.append(np.zeros_like(tiles[0]))
rows = [np.hstack(tiles[i:i + 3]) for i in range(0, len(tiles), 3)]
cv2.imwrite("previews/mapa_test.jpg", np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 88])
print("ok")
