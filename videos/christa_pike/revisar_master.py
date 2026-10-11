# -*- coding: utf-8 -*-
"""Hojas de revisión del MASTER: un cuadro cada `paso` s (por defecto 3) en hojas de 3x4 a 640x360 -> previews/rev_NN.jpg.
python revisar_master.py salida/christa_pike_MASTER.mp4 [paso]"""
import os
import sys
import cv2
import numpy as np

ruta = sys.argv[1]
paso = float(sys.argv[2]) if len(sys.argv) > 2 else 3.0
cap = cv2.VideoCapture(ruta)
fps = cap.get(cv2.CAP_PROP_FPS) or 30
dur = cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps
cols, filas, ancho = 3, 4, 640
alto = 360
ts = list(np.arange(1.0, dur - 0.3, paso))
os.makedirs("previews", exist_ok=True)
for f in os.listdir("previews"):
    if f.startswith("rev_"):
        os.remove(os.path.join("previews", f))
hoja = []
n = 0
for t in ts:
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
    ok, fr = cap.read()
    if not ok:
        continue
    fr = cv2.resize(fr, (ancho, alto), interpolation=cv2.INTER_AREA)
    cv2.rectangle(fr, (0, 0), (92, 24), (0, 0, 0), -1)
    cv2.putText(fr, f"{int(t // 60)}:{t % 60:04.1f}", (4, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1, cv2.LINE_AA)
    hoja.append(fr)
    if len(hoja) == cols * filas:
        cv2.imwrite(f"previews/rev_{n:02d}.jpg", np.vstack([np.hstack(hoja[i:i + cols]) for i in range(0, len(hoja), cols)]), [cv2.IMWRITE_JPEG_QUALITY, 85])
        hoja, n = [], n + 1
if hoja:
    while len(hoja) % cols:
        hoja.append(np.zeros((alto, ancho, 3), np.uint8))
    cv2.imwrite(f"previews/rev_{n:02d}.jpg", np.vstack([np.hstack(hoja[i:i + cols]) for i in range(0, len(hoja), cols)]), [cv2.IMWRITE_JPEG_QUALITY, 85])
    n += 1
print(n, "hojas,", len(ts), "cuadros, dur", round(dur, 1))
