# -*- coding: utf-8 -*-
"""Hojas de revisión del MASTER: un cuadro EXACTO cada 3 s (t = 1,5 + 3k), 6 por hoja (2x3, 960x540 cada uno)
-> previews/master_NN.jpg. Uso: python _revisar_master.py [paso] [t0]"""
import glob
import os
import subprocess
import sys

import cv2
import numpy as np

FF = "C:/ffmpeg/bin/ffmpeg.exe"
paso = float(sys.argv[1]) if len(sys.argv) > 1 else 3.0
t0 = float(sys.argv[2]) if len(sys.argv) > 2 else 1.5
v = glob.glob("salida/*_MASTER.mp4")[0]
cap = cv2.VideoCapture(v)
fps = cap.get(cv2.CAP_PROP_FPS)
n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
dur = n / fps
ts = list(np.arange(t0, dur, paso))
tiles = []
for t in ts:
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(round(t * fps)))
    ok, im = cap.read()
    if not ok:
        im = np.zeros((1080, 1920, 3), np.uint8)
    s = cv2.resize(im, (960, 540), interpolation=cv2.INTER_AREA)
    cv2.putText(s, f"{t:.1f}", (8, 530), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    tiles.append(s)
os.makedirs("previews", exist_ok=True)
for f in glob.glob("previews/master_*.jpg"):
    os.remove(f)
for h in range(0, len(tiles), 6):
    g = tiles[h:h + 6]
    while len(g) < 6:
        g.append(np.zeros_like(tiles[0]))
    hoja = np.vstack([np.hstack(g[0:2]), np.hstack(g[2:4]), np.hstack(g[4:6])])
    cv2.imwrite(f"previews/master_{h // 6:02d}.jpg", hoja, [cv2.IMWRITE_JPEG_QUALITY, 82])
print(len(tiles), "cuadros,", (len(tiles) + 5) // 6, "hojas; duración", round(dur, 2), "s")
