# -*- coding: utf-8 -*-
"""Hoja para asignar a mano quién es quién en el minimapa (rastrear.py --inicio): cada círculo detectado en el cuadro t,
ampliado ×6 con su número y posición, y debajo los iconos de Data Dragon de los campeones de la partida.
uso: python nucleo/tactica3d/fichas_inicio.py <clip.mp4> <t> <iconos> <salida.jpg> Campeon1 Campeon2 ..."""
import sys

import cv2
import numpy as np

import rastrear as R

clip, t, ico, sal = sys.argv[1], float(sys.argv[2]), sys.argv[3], sys.argv[4]
champs = sys.argv[5:]
cap = cv2.VideoCapture(clip)
mini = R.leer(cap, t)
ds = R.detectar(mini)
big = cv2.resize(mini, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
tiles = []
for k, (x, y, f, pc, eq) in enumerate(ds):
    im = cv2.resize(pc, (120, 120), interpolation=cv2.INTER_CUBIC)
    im = cv2.copyMakeBorder(im, 30, 4, 4, 4, cv2.BORDER_CONSTANT, value=(30, 30, 30))
    cv2.putText(im, f"{k}:{int(x)},{int(y)} {eq or '?'}", (4, 22), 0, .5, (0, 255, 255), 1)
    tiles.append(im)
    cv2.putText(big, str(k), (int(x * 3) - 8, int(y * 3) + 8), 0, .9, (0, 255, 255), 2)
fila = []
for c in champs:
    im = cv2.resize(cv2.imread(f"{ico}/{c}.png"), (120, 120))
    im = cv2.copyMakeBorder(im, 30, 4, 4, 4, cv2.BORDER_CONSTANT, value=(60, 20, 20))
    cv2.putText(im, c[:12], (4, 22), 0, .5, (255, 255, 255), 1)
    fila.append(im)
def rejilla(ts, n=8):
    while len(ts) % n:
        ts.append(np.zeros_like(ts[0]))
    return np.vstack([np.hstack(ts[i:i + n]) for i in range(0, len(ts), n)])
a = rejilla(tiles)
b = rejilla(fila) if fila else np.zeros((1, 1, 3), np.uint8)
W = max(a.shape[1], b.shape[1], big.shape[1])
pad = lambda m: cv2.copyMakeBorder(m, 0, 0, 0, W - m.shape[1], cv2.BORDER_CONSTANT)
cv2.imwrite(sal, np.vstack([pad(big), pad(a), pad(b)]))
