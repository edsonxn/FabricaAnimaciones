# -*- coding: utf-8 -*-
"""Hoja de contacto de un video: un cuadro cada `paso` s con su tiempo.  python hoja_clip.py clips/x.mp4 [paso=6] [cols=6] [ancho=300]
-> previews/clips/<nombre>.jpg"""
import sys, os
import cv2
import numpy as np

ruta = sys.argv[1]
paso = float(sys.argv[2]) if len(sys.argv) > 2 else 6.0
cols = int(sys.argv[3]) if len(sys.argv) > 3 else 6
ancho = int(sys.argv[4]) if len(sys.argv) > 4 else 300
t_ini = float(sys.argv[5]) if len(sys.argv) > 5 else 0.0
t_fin = float(sys.argv[6]) if len(sys.argv) > 6 else 1e9
cap = cv2.VideoCapture(ruta)
fps = cap.get(cv2.CAP_PROP_FPS) or 30
n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
dur = n / fps
alto = int(ancho * 9 / 16)
ims = []
t = t_ini
while t < min(dur, t_fin):
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
    ok, f = cap.read()
    if not ok:
        break
    f = cv2.resize(f, (ancho, alto), interpolation=cv2.INTER_AREA)
    cv2.rectangle(f, (0, 0), (70, 22), (0, 0, 0), -1)
    cv2.putText(f, f"{int(t // 60)}:{t % 60:04.1f}", (3, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv2.LINE_AA)
    ims.append(f)
    t += paso
while len(ims) % cols:
    ims.append(np.zeros((alto, ancho, 3), np.uint8))
hoja = np.vstack([np.hstack(ims[i:i + cols]) for i in range(0, len(ims), cols)])
os.makedirs("previews/clips", exist_ok=True)
out = f"previews/clips/{os.path.splitext(os.path.basename(ruta))[0]}.jpg"
cv2.imwrite(out, hoja, [cv2.IMWRITE_JPEG_QUALITY, 85])
print(out, hoja.shape, f"dur={dur:.1f}s")
