# -*- coding: utf-8 -*-
"""Detecta cortes de plano de un clip (diferencia de histograma entre cuadros consecutivos a 30 fps).
python cortes.py clips/x.mp4 [t_ini] [t_fin]"""
import sys
import cv2
import numpy as np

ruta = sys.argv[1]
t0 = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
t1 = float(sys.argv[3]) if len(sys.argv) > 3 else 1e9
cap = cv2.VideoCapture(ruta)
fps = cap.get(cv2.CAP_PROP_FPS) or 30
cap.set(cv2.CAP_PROP_POS_MSEC, t0 * 1000)
prev = None
i = int(t0 * fps)
cortes = []
while True:
    ok, f = cap.read()
    if not ok or i / fps > t1:
        break
    s = cv2.resize(f, (160, 90))
    h = cv2.calcHist([cv2.cvtColor(s, cv2.COLOR_BGR2HSV)], [0, 1, 2], None, [8, 8, 8], [0, 180, 0, 256, 0, 256])
    h = cv2.normalize(h, h).flatten()
    if prev is not None:
        d = cv2.compareHist(prev, h, cv2.HISTCMP_BHATTACHARYYA)
        px = float(np.abs(s.astype(np.float32) - prev_img).mean())
        if d > 0.28 or px > 38:
            cortes.append(round(i / fps, 2))
    prev, prev_img = h, s.astype(np.float32)
    i += 1
print(ruta, "cortes:", cortes)
