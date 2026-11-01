# -*- coding: utf-8 -*-
"""Cuadros (960x540) de los rótulos indicados, con la capa de efectos aplicada, sin renderizar el video.
Uso: python hoja_rotulos.py <carpeta_video> <salida.jpg> TEXTO1 TEXTO2 ..."""
import os, sys
sys.path.append(r"C:\FabricaAnimaciones\nucleo")
os.chdir(sys.argv[1])
sys.path.insert(0, os.getcwd())     # el efectos.py del video, no el del núcleo
import cv2
import numpy as np
import secuencia_fx as X

capa = X.cargar()
S = capa.S
quiero = sys.argv[3:]
minis = []
for d in capa.rot:
    if d["texto"] not in quiero:
        continue
    t = d["de"] + min(0.8, (d["a"] - d["de"]) * .6)
    k = next((i for i, b in enumerate(capa.bs) if b["t0"] <= t < b["t1"]), len(capa.bs) - 1)
    b = capa.bs[k]
    f = capa.aplicar(capa.envolver(S._fuente(b, k, True, capa), b).cuadro(t), t)
    m = cv2.resize(f, (960, 540), interpolation=cv2.INTER_AREA)
    cv2.putText(m, f"{t:.1f}s {d['texto']}".encode("ascii", "replace").decode(), (8, 30), cv2.FONT_HERSHEY_SIMPLEX, .8,
                (0, 255, 255), 2, cv2.LINE_AA)
    minis.append(m)
minis += [np.zeros_like(minis[0])] * (-len(minis) % 2)
cv2.imwrite(sys.argv[2], np.vstack([np.hstack(minis[i:i + 2]) for i in range(0, len(minis), 2)]), [cv2.IMWRITE_JPEG_QUALITY, 85])
print(len(minis), "cuadros")
