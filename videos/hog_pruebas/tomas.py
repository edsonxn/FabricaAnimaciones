# -*- coding: utf-8 -*-
"""Limpia los mates (quita ramas pegadas a la cabeza) y mide cada cuadro: tope de la cabeza, centro y ancho.
   → fuente/alfa_l/a_%04d.png (mate limpio) + fuente/medidas.json ; imprime los cortes."""
import json
from pathlib import Path
import cv2, numpy as np

A = Path(__file__).parent
AL, ALL = A / "fuente/alfa", A / "fuente/alfa_l"
ALL.mkdir(exist_ok=True)
K1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (57, 57))
K2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31))
med = []
fs = sorted(AL.glob("a_*.png"))
for f in fs:
    a = cv2.imread(str(f), cv2.IMREAD_GRAYSCALE)
    b = (a > 110).astype(np.uint8)
    o = cv2.morphologyEx(b, cv2.MORPH_OPEN, K1)
    n, lab, st, _ = cv2.connectedComponentsWithStats(o)
    if n > 1:
        k = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
        o = (lab == k).astype(np.uint8)
    m = cv2.GaussianBlur(cv2.dilate(o, K2).astype(np.float32), (0, 0), 6)
    al = (a.astype(np.float32) * np.clip(m * 1.6, 0, 1)).astype(np.uint8)
    cv2.imwrite(str(ALL / f.name), al)
    filas = np.where(o.sum(1) > 20)[0]
    if len(filas) == 0:
        med.append(dict(top=0, cx=720, w=0)); continue
    top = int(filas[0])
    banda = o[top:top + 230]
    cols = np.where(banda.sum(0) > 8)[0]
    med.append(dict(top=top, cx=int((cols[0] + cols[-1]) / 2), w=int(cols[-1] - cols[0])))
(A / "fuente/medidas.json").write_text(json.dumps(med), encoding="utf-8")
ant = None
for i, m in enumerate(med):
    if ant is None or abs(m["w"] - ant["w"]) > 60 or abs(m["top"] - ant["top"]) > 60 or abs(m["cx"] - ant["cx"]) > 80:
        print(f"corte cuadro {i:3d}  t={i / 30:5.2f}  top={m['top']:4d} cx={m['cx']:4d} w={m['w']:4d}")
    ant = m
print(len(med), "cuadros")
