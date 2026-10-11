"""Prueba del mapa de Japón: hoja con las épocas. python _mapa_test.py"""
import cv2
import numpy as np

import mapa as M

M.cargar()
cam = M.Cam(136.0, 37.0, 2.2)
tiles = []
for nombre, col in (("yayoi", "yayoi"), ("yamato", "yamato"), ("yamato_exp", "yamato"), ("heian", "heian"), ("sin_hokkaido", "tokugawa"),
                    ("japon", "meiji"), ("imperio", "imperio"), ("kanto", "shogun"), ("kinai", "yamato")):
    img = M.fondo_base()
    M.pintar_tierra(img, cam, 0)
    S = cam.proyectar(M.CAMPOS[nombre])
    M.pintar(img, S, M.COL[col], 1.0, 0)
    small = cv2.resize((img[..., ::-1] * 255).astype(np.uint8), (640, 360), interpolation=cv2.INTER_AREA)
    cv2.putText(small, nombre, (8, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    tiles.append(small)
rows = [np.hstack(tiles[i:i + 3]) for i in range(0, len(tiles), 3)]
cv2.imwrite("previews/mapa_test.jpg", np.vstack(rows))
print("ok")
