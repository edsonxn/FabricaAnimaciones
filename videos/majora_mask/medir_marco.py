# -*- coding: utf-8 -*-
"""Mide el marco lateral que no cambia en el tiempo (Switch Online: degradado gris + «P1»; o barras negras) en cada clip de
medios/ y propone SECUENCIA["recorte_por"] (fracción por lado). Columnas «quietas» = desviación entre 4 cuadros < 4 y además
contiguas al borde. `python medir_marco.py` imprime el dict para pegar en guion.py (lección de banjo_tooie, 19-oct-2026)."""
import glob
import os

import cv2
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
res = {}
for f in sorted(glob.glob(os.path.join(AQUI, "medios", "scene-*.mp4"))):
    cap = cv2.VideoCapture(f)
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frs = []
    for k in range(4):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(n * (k + .5) / 4))
        ok, fr = cap.read()
        if ok:
            frs.append(cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY).astype(np.float32))
    if len(frs) < 3:
        continue
    a = np.stack(frs)
    W = a.shape[2]
    quieta = a.std(axis=0).mean(axis=0) < 4          # por columna
    izq = 0
    while izq < W // 3 and quieta[izq]:
        izq += 1
    der = 0
    while der < W // 3 and quieta[W - 1 - der]:
        der += 1
    lado = min(izq, der)
    if lado > W * .02:
        res[os.path.basename(f)[:-4]] = round(lado / W + .006, 3)
print("recorte_por=" + repr(res))
print(len(res), "clips con marco")
