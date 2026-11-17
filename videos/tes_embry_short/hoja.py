"""Hoja de cuadros de un clip con rejilla (para ubicar caras).
Uso: python hoja.py <clave> t1 t2 ... [--ancho 640]  → previews/hoja_<clave>.jpg
Los tiempos son segundos dentro del clip. La rejilla marca cada 10 % (x,y en 0..100).
"""
import os, sys
import cv2
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
args = [a for a in sys.argv[1:]]
ancho = 640
if "--ancho" in args:
    i = args.index("--ancho"); ancho = int(args[i + 1]); del args[i:i + 2]
clave, ts = args[0], [float(x) for x in args[1:]]
cap = cv2.VideoCapture(os.path.join(AQUI, "segmentos", "clips", clave + ".mp4"))
celdas = []
for t in ts:
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
    ok, fr = cap.read()
    if not ok:
        fr = np.zeros((1080, 1920, 3), np.uint8)
    h = int(fr.shape[0] * ancho / fr.shape[1])
    fr = cv2.resize(fr, (ancho, h))
    for k in range(1, 10):
        x, y = int(ancho * k / 10), int(h * k / 10)
        cv2.line(fr, (x, 0), (x, h), (0, 255, 255), 1)
        cv2.line(fr, (0, y), (ancho, y), (0, 255, 255), 1)
        cv2.putText(fr, str(k * 10), (x + 2, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 255), 1)
        cv2.putText(fr, str(k * 10), (2, y - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 255), 1)
    cv2.putText(fr, "%s %.1f" % (clave, t), (8, h - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    celdas.append(fr)
while len(celdas) % 2:
    celdas.append(np.zeros_like(celdas[0]))
filas = [np.hstack(celdas[i:i + 2]) for i in range(0, len(celdas), 2)]
out = os.path.join(AQUI, "previews", "hoja_%s.jpg" % clave)
cv2.imwrite(out, np.vstack(filas), [cv2.IMWRITE_JPEG_QUALITY, 82])
print(out)
