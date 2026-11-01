# -*- coding: utf-8 -*-
"""Mosaico 2x2 de los cuadros completos previews/l_<escena>_*.png -> previews/mos_<escena>_<k>.jpg  (python _mosaico.py <escena>)"""
import glob, os, sys
import cv2, numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
e = sys.argv[1]
fs = sorted(glob.glob(f"previews/l_{e}_*.png"))
for k in range(0, len(fs), 4):
    tiles = []
    for f in fs[k:k + 4]:
        im = cv2.resize(cv2.imread(f), (960, 540), interpolation=cv2.INTER_AREA)
        cv2.putText(im, os.path.basename(f)[2:-4], (8, 530), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
        tiles.append(im)
    while len(tiles) < 4:
        tiles.append(np.zeros_like(tiles[0]))
    cv2.imwrite(f"previews/mos_{e}_{k // 4}.jpg", np.vstack([np.hstack(tiles[:2]), np.hstack(tiles[2:])]), [cv2.IMWRITE_JPEG_QUALITY, 88])
print(len(fs), "cuadros")
