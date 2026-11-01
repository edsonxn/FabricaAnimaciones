# -*- coding: utf-8 -*-
"""Revisión del MASTER: un cuadro cada 3 s en hojas de 4x3 (480x270) -> previews/master_NN.jpg."""
import subprocess
import cv2
import numpy as np

V = "salida/oxigeno_5_segundos_MASTER.mp4"
cap = cv2.VideoCapture(V)
fps = cap.get(cv2.CAP_PROP_FPS)
n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
ts = np.arange(1.5, n / fps, 3.0)
tiles = []
for t in ts:
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(t * fps))
    ok, im = cap.read()
    if not ok:
        continue
    im = cv2.resize(im, (480, 270), interpolation=cv2.INTER_AREA)
    m, s = divmod(int(t), 60)
    for c, w in (((0, 0, 0), 3), ((255, 255, 255), 1)):
        cv2.putText(im, f"{m}:{s:02d}", (6, 262), cv2.FONT_HERSHEY_SIMPLEX, 0.55, c, w, cv2.LINE_AA)
    tiles.append(im)
k = 0
for i in range(0, len(tiles), 12):
    g = tiles[i:i + 12]
    while len(g) < 12:
        g.append(np.zeros_like(tiles[0]))
    hoja = np.vstack([np.hstack(g[j:j + 4]) for j in range(0, 12, 4)])
    cv2.imwrite(f"previews/master_{k:02d}.jpg", hoja, [cv2.IMWRITE_JPEG_QUALITY, 85])
    k += 1
print(k, "hojas,", len(tiles), "cuadros")
