# -*- coding: utf-8 -*-
"""Revisión del MASTER: un cuadro cada 3 s en hojas de 2x3 (800x450) -> previews/master_NN.jpg."""
import cv2
import numpy as np

V = "salida/gravedad_5_segundos_MASTER.mp4"
cap = cv2.VideoCapture(V)
fps = cap.get(cv2.CAP_PROP_FPS)
n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
ts = np.arange(1.0, n / fps, 3.0)
tiles = []
for t in ts:
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(t * fps))
    ok, im = cap.read()
    if not ok:
        continue
    im = cv2.resize(im, (800, 450), interpolation=cv2.INTER_AREA)
    m, s = divmod(int(t), 60)
    for c, w in (((0, 0, 0), 3), ((255, 255, 255), 1)):
        cv2.putText(im, f"{m}:{s:02d}", (8, 438), cv2.FONT_HERSHEY_SIMPLEX, 0.7, c, w, cv2.LINE_AA)
    tiles.append(im)
k = 0
for i in range(0, len(tiles), 6):
    g = tiles[i:i + 6]
    while len(g) < 6:
        g.append(np.zeros_like(tiles[0]))
    hoja = np.vstack([np.hstack(g[j:j + 2]) for j in range(0, 6, 2)])
    cv2.imwrite(f"previews/master_{k:02d}.jpg", hoja, [cv2.IMWRITE_JPEG_QUALITY, 88])
    k += 1
print(k, "hojas,", len(tiles), "cuadros")
