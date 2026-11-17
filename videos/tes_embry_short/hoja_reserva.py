"""Hoja rápida de varios clips a tiempos dados: python hoja_reserva.py clave:t1,t2 clave:t1,t2 ...  → previews/reserva.jpg"""
import os, sys
import cv2
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
W = 480
filas = []
for arg in sys.argv[1:]:
    c, ts = arg.split(":")
    cap = cv2.VideoCapture(os.path.join(AQUI, "segmentos", "clips", c + ".mp4"))
    celdas = []
    for t in [float(x) for x in ts.split(",")]:
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ok, fr = cap.read()
        fr = fr if ok else np.zeros((1080, 1920, 3), np.uint8)
        h = int(fr.shape[0] * W / fr.shape[1])
        fr = cv2.resize(fr, (W, h))
        for k in range(1, 10):
            x, y = int(W * k / 10), int(h * k / 10)
            cv2.line(fr, (x, 0), (x, h), (0, 220, 255), 1)
            cv2.line(fr, (0, y), (W, y), (0, 220, 255), 1)
        cv2.putText(fr, "%s %.1f" % (c, t), (6, h - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        celdas.append(fr)
    while len(celdas) < 3:
        celdas.append(np.zeros_like(celdas[0]))
    filas.append(np.hstack(celdas[:3]))
out = os.path.join(AQUI, "previews", "reserva.jpg")
cv2.imwrite(out, np.vstack(filas), [cv2.IMWRITE_JPEG_QUALITY, 78])
print(out)
