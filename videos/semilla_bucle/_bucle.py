# -*- coding: utf-8 -*-
"""Comprueba que el último cuadro coincide con el primero (bucle)."""
import os
import sys

sys.path.insert(0, os.path.abspath("../../nucleo"))
sys.path.insert(0, os.path.abspath("."))

import cv2
import numpy as np

import escenas as S

m = S.CLASES["vuelo"](S._ESC["vuelo"], 0)
n = int(round(S.TOTAL * 30))
a = m.render(None, 0.0)
z = m.render(None, (n - 1) / 30)
z2 = m.render(None, (n - 2) / 30)

d = np.abs(a - z)
print("cuadro 0 vs último: dif máx %.5f  media %.7f  píxeles distintos %d" % (d.max(), d.mean(), int((d > 1e-4).sum())))
d2 = np.abs(a - z2)
print("cuadro 0 vs penúltimo: dif máx %.5f  media %.7f" % (d2.max(), d2.mean()))

if d.max() < 0.01:
    print("BUCLE PERFECTO: Cierra sin saltos visibles.")
else:
    print("AVISO: Hay diferencias entre cuadro 0 y el último cuadro.")
