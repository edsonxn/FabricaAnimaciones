"""Hoja de contacto de un clip: python _contacto.py <clip> <paso_s> [t0] [t1]  → previews/c_<clip>.jpg (6 columnas, 320x180)."""
import os
import sys

import cv2
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
nom, paso = sys.argv[1], float(sys.argv[2])
cap = cv2.VideoCapture(os.path.join(AQUI, "clips", nom + ".mp4"))
fps = cap.get(cv2.CAP_PROP_FPS) or 30
dur = cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps
t0 = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
t1 = min(float(sys.argv[4]) if len(sys.argv) > 4 else dur, dur - 0.1)
cel = []
t = t0
while t <= t1 and len(cel) < 72:
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
    ok, im = cap.read()
    if ok:
        im = cv2.resize(im, (320, 180))
        cv2.rectangle(im, (0, 0), (74, 20), (0, 0, 0), -1)
        cv2.putText(im, f"{t:.0f}", (4, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cel.append(im)
    t += paso
while len(cel) % 6:
    cel.append(np.zeros((180, 320, 3), np.uint8))
filas = [np.hstack(cel[i:i + 6]) for i in range(0, len(cel), 6)]
os.makedirs(os.path.join(AQUI, "previews"), exist_ok=True)
out = os.path.join(AQUI, "previews", f"c_{nom}.jpg")
cv2.imwrite(out, np.vstack(filas), [cv2.IMWRITE_JPEG_QUALITY, 80])
print(out, f"dur={dur:.1f}s", len(cel), "cuadros")
