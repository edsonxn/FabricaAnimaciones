# -*- coding: utf-8 -*-
"""Cuadro a tamaño completo (1920x1080) de la escena en uno o varios tiempos globales: previews/cuadro_<t>.jpg.
Uso (desde esta carpeta):  $env:PYTHONPATH="C:\\FabricaAnimaciones\\nucleo"; python _cuadro.py 72.5 140"""
import os
import sys

import cv2

from motor import Lienzo, a_uint8
import escenas as S

os.makedirs("previews", exist_ok=True)
lz = Lienzo()
esc = S.CLASES[next(iter(S.CLASES))]({"id": "x", "t0": 0, "t1": 1, "frases": []}, 1)
for a in sys.argv[1:]:
    t = float(a)
    img = esc.render(lz, t)
    cv2.imwrite(f"previews/cuadro_{t:.1f}.jpg", cv2.cvtColor(a_uint8(img), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 92])
    print("ok", t)
