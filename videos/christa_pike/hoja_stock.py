# -*- coding: utf-8 -*-
"""Hoja con un cuadro (a 1/3 del clip) de cada candidato de clips/stock -> previews/stock_N.jpg (30 por hoja, 6 columnas)."""
import glob, os, sys
import cv2, numpy as np

fs = sorted(glob.glob("clips/stock/*.mp4"))
ancho, cols, por_hoja = 320, 6, 30
alto = int(ancho * 9 / 16)
ims = []
for f in fs:
    cap = cv2.VideoCapture(f)
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, n // 3))
    ok, fr = cap.read()
    if not ok:
        fr = np.zeros((alto, ancho, 3), np.uint8)
    fr = cv2.resize(fr, (ancho, alto), interpolation=cv2.INTER_AREA)
    nom = os.path.basename(f)[:-4]
    cv2.rectangle(fr, (0, 0), (ancho, 20), (0, 0, 0), -1)
    cv2.putText(fr, nom, (3, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv2.LINE_AA)
    ims.append(fr)
for h in range(0, len(ims), por_hoja):
    blk = ims[h:h + por_hoja]
    while len(blk) % cols:
        blk.append(np.zeros((alto, ancho, 3), np.uint8))
    hoja = np.vstack([np.hstack(blk[i:i + cols]) for i in range(0, len(blk), cols)])
    out = f"previews/stock_{h // por_hoja}.jpg"
    cv2.imwrite(out, hoja, [cv2.IMWRITE_JPEG_QUALITY, 85])
    print(out, hoja.shape)
