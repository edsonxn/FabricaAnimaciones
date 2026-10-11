# -*- coding: utf-8 -*-
"""Hoja resumen para el usuario: 24 cuadros (480x270) repartidos por el video -> previews/resumen.jpg"""
import cv2
import numpy as np
import escenas as E
m = E.Mundo(E.TL["escenas"][0], 0)
ts = [4, 13.5, 22, 28, 43, 55, 61, 74, 85.5, 95, 121, 128, 143, 157, 168, 187.5, 198, 214.5, 224, 237.5, 262, 266, 292, 305]
tiles = []
for t in ts:
    im = (np.clip(m.render(None, float(t)), 0, 1)[..., ::-1] * 255).astype(np.uint8)
    tiles.append(cv2.resize(im, (480, 270), interpolation=cv2.INTER_AREA))
rows = [np.hstack(tiles[i:i + 4]) for i in range(0, 24, 4)]
cv2.imwrite("previews/resumen.jpg", np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 88])
