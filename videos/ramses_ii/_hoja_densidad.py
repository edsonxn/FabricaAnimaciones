# -*- coding: utf-8 -*-
"""Hoja de densidad: 6 cuadros cada 0,5 s por toma (regla «nunca secuencia de fotos»). -> previews/_densidad.jpg"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "nucleo"))
import cv2, numpy as np
import escenas as E
filas = []
for i, (t0, fn, _) in enumerate(E.TOMAS):
    if fn is None:
        continue
    fila = []
    for k in range(6):
        t = t0 + 1.0 + 0.5 * k
        img = (E.render_mundo(t) * 255).astype(np.uint8)
        c = cv2.resize(img, (256, 144), interpolation=cv2.INTER_AREA)
        cv2.putText(c, f"{t:.1f}", (4, 14), 0, 0.4, (255, 255, 0), 1)
        fila.append(c)
    filas.append(np.hstack(fila))
cv2.imwrite("previews/_densidad.jpg", cv2.cvtColor(np.vstack(filas), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 80])
import docu_antiguo as A
print("firmas", len(A._FIRMAS), A.verificar_firmas("ramses_ii"))
