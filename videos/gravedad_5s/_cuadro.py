# -*- coding: utf-8 -*-
"""Cuadros de prueba del plano secuencia (desde esta carpeta, con PYTHONPATH=nucleo):
   python _cuadro.py 12.5 40            -> previews/cuadro_<t>.jpg a 1920x1080 (rigor)
   python _cuadro.py hoja 1 4 7 10 ...  -> previews/hoja.jpg (tiles de 640x360, 3 por fila, con el tiempo)"""
import os
import sys
import time

import cv2
import numpy as np

import estilos
estilos.activar("kurzgesagt")
from motor import Lienzo, a_uint8  # noqa: E402
import efectos  # noqa: E402
import escenas as S  # noqa: E402

os.makedirs("previews", exist_ok=True)
lz = Lienzo()
esc = S.CLASES[next(iter(S.CLASES))]({"id": "x", "t0": 0, "t1": 1, "frases": []}, 1)
args = sys.argv[1:]
hoja = args and args[0] == "hoja"
if hoja:
    args = args[1:]
tiles = []
for a in args:
    t = float(a)
    t0 = time.time()
    img = esc.render(lz, t)
    img = efectos.acabado(img, int(t * 10))
    dt = time.time() - t0
    im = a_uint8(img)
    if hoja:
        im = cv2.resize(im, (640, 360), interpolation=cv2.INTER_AREA)
        for c, w in (((0, 0, 0), 3), ((255, 255, 255), 1)):
            cv2.putText(im, f"{t:.2f}s {dt:.1f}s", (8, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.6, c, w, cv2.LINE_AA)
        tiles.append(im)
    else:
        cv2.imwrite(f"previews/cuadro_{t:.1f}.jpg", cv2.cvtColor(im, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
    print("ok", t, f"{dt:.2f}s")
if hoja and tiles:
    while len(tiles) % 3:
        tiles.append(np.zeros_like(tiles[0]))
    sheet = np.vstack([np.hstack(tiles[i:i + 3]) for i in range(0, len(tiles), 3)])
    cv2.imwrite("previews/hoja.jpg", cv2.cvtColor(sheet, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 88])
