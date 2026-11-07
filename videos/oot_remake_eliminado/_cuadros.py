# -*- coding: utf-8 -*-
"""Hoja de cuadros reales (clip + efectos) en tiempos dados: python _cuadros.py salida.jpg t1 t2 ..."""
import os, sys
import cv2, numpy as np
AQUI = os.path.dirname(os.path.abspath(__file__)); os.chdir(AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo")); sys.path.insert(0, AQUI)
import secuencia_fx as SF
capa = SF.cargar(); S = capa.S
minis = []
for t in map(float, sys.argv[2:]):
    k = next((i for i, b in enumerate(capa.bs) if b["t0"] <= t < b["t1"]), len(capa.bs) - 1); b = capa.bs[k]
    f = capa.aplicar(capa.envolver(S._fuente(b, k, True, capa), b).cuadro(t), t)
    m = cv2.resize(f, (480, 270), interpolation=cv2.INTER_AREA)
    cv2.putText(m, f"{t:.1f} {b['id'][6:]}", (6, 262), cv2.FONT_HERSHEY_SIMPLEX, .6, (90, 214, 255), 2, cv2.LINE_AA)
    minis.append(m)
minis += [np.zeros_like(minis[0])] * (-len(minis) % 4)
cv2.imwrite(sys.argv[1], np.vstack([np.hstack(minis[i:i + 4]) for i in range(0, len(minis), 4)]))
print(sys.argv[1])
