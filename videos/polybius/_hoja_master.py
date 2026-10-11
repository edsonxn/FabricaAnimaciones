# -*- coding: utf-8 -*-
"""Revisión del MASTER: un cuadro cada `paso` s, hojas 2x2 (960x540 por cuadro) -> previews/master/m_XXX.jpg"""
import sys
import cv2
import numpy as np
paso = float(sys.argv[1]) if len(sys.argv) > 1 else 3.0
cap = cv2.VideoCapture(r"salida\satoshi_nakamoto_MASTER.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)
n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
dur = n / fps
ims, hoja, t = [], 0, 1.0
def guarda():
    global ims, hoja
    while len(ims) < 4:
        ims.append(np.zeros_like(ims[0]))
    cv2.imwrite(f"previews/master/m_{hoja:03d}.jpg", np.vstack([np.hstack(ims[:2]), np.hstack(ims[2:])]), [cv2.IMWRITE_JPEG_QUALITY, 88])
    hoja += 1
    ims = []
while t < dur - 0.5:
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(t * fps))
    ok, f = cap.read()
    if not ok:
        f = np.zeros((1080, 1920, 3), np.uint8)
    s = cv2.resize(f, (960, 540), interpolation=cv2.INTER_AREA)
    media = float(f.mean())
    cv2.putText(s, f"{int(t // 60)}:{t % 60:04.1f}  m={media:.0f}", (8, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)
    ims.append(s)
    if len(ims) == 4:
        guarda()
    t += paso
if ims:
    guarda()
print("hojas:", hoja, "duracion", dur)
