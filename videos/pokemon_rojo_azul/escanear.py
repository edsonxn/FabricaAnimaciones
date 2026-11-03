# -*- coding: utf-8 -*-
"""Hojas de contacto del longplay de Longplay Nexus a 360p, ya bajado en E:\\FabricaAnimaciones\\_scan_pokemon\\longplay360.mp4
(3-nov-2026; receta de majora_mask/escanear.py). Un cuadro cada PASO s con el segundo impreso.
    python escanear.py <nombre> <desde> <hasta> [paso]      -> previews/_scan/<nombre>.jpg
"""
import os
import sys

import cv2
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
VID = r"E:\FabricaAnimaciones\_scan_pokemon\longplay360.mp4"


def hoja(nombre, a, b, paso=10, cols=8, ancho=240):
    cap = cv2.VideoCapture(VID)
    celdas = []
    for s in np.arange(a, b, paso):
        cap.set(cv2.CAP_PROP_POS_MSEC, float(s) * 1000)
        ok, f = cap.read()
        if not ok:
            break
        f = cv2.resize(f, (ancho, int(f.shape[0] * ancho / f.shape[1])))
        cv2.putText(f, str(int(s)), (3, 16), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 0), 3)
        cv2.putText(f, str(int(s)), (3, 16), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 255, 255), 1)
        celdas.append(f)
    h, w = celdas[0].shape[:2]
    filas = (len(celdas) + cols - 1) // cols
    out = np.zeros((filas * h, cols * w, 3), np.uint8)
    for i, c in enumerate(celdas):
        out[(i // cols) * h:(i // cols + 1) * h, (i % cols) * w:(i % cols + 1) * w] = c
    ruta = os.path.join(AQUI, "previews", "_scan", nombre + ".jpg")
    cv2.imwrite(ruta, out, [cv2.IMWRITE_JPEG_QUALITY, 80])
    print(ruta, len(celdas))


if __name__ == "__main__":
    hoja(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]) if len(sys.argv) > 4 else 10)
