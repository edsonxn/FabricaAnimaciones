# -*- coding: utf-8 -*-
"""Limpia los mates de DeepLab (componente mayor, sin el póster de la pared ni sus pegatinas) y sigue la cabeza.
   → fuente/alfa_l/a_%04d.png + fuente/seguimiento.json ([cx, top] por cuadro de la fuente, suavizado)."""
import json
from pathlib import Path
import cv2, numpy as np
from scipy.ndimage import gaussian_filter1d
from recortar import hay_el, FPS

A = Path(__file__).parent
AL, ALL = A / "fuente/alfa", A / "fuente/alfa_l"
ALL.mkdir(exist_ok=True)
NS = 2717
# sus pegatinas encima de la toma (coordenadas del cuadro VOLTEADO): se quita esa franja del mate
TAPAS = [(27.5, 31.1, 1150, 1920), (60.5, 64.45, 0, 720), (60.5, 64.45, 1280, 1920), (82.0, 86.2, 1100, 1920)]
K1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31))
med = []
for i in range(NS):
    f = AL / f"a_{i + 1:04d}.png"
    if not hay_el(i) or not f.exists():
        med.append(None); continue
    a = cv2.imread(str(f), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    t = i / FPS
    for t0, t1, x0, x1 in TAPAS:
        if t0 <= t < t1:
            a[:, x0:x1] = 0
    a[:430, 1170:1430] = 0                           # póster de dos personas en la pared (DeepLab lo toma por persona)
    o = cv2.morphologyEx((a > 0.5).astype(np.uint8), cv2.MORPH_OPEN, K1)
    n, lab, st, _ = cv2.connectedComponentsWithStats(o)
    if n > 1:
        k = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
        o = (lab == k).astype(np.uint8)
    m = cv2.GaussianBlur(cv2.dilate(o, K1).astype(np.float32), (0, 0), 4)
    al = np.clip((a - 0.25) / 0.5, 0, 1) * np.clip(m * 1.5, 0, 1)
    cv2.imwrite(str(ALL / f.name), (al * 255).astype(np.uint8))
    filas = np.where(o.sum(1) > 30)[0]
    if len(filas) == 0:
        med.append(None); continue
    top = int(filas[0])
    cols = np.where(o[top + 80:top + 380].sum(0) > 8)[0]
    med.append((float((cols[0] + cols[-1]) / 2) if len(cols) else 880.0, float(top)))
# huecos (intro, insertos) = último valor conocido
ult = next(m for m in med if m)
for i in range(NS):
    if med[i] is None:
        med[i] = ult
    ult = med[i]
med = np.array(med, np.float64)
seg = np.stack([gaussian_filter1d(med[:, 0], 20, mode="nearest"), gaussian_filter1d(med[:, 1], 8, mode="nearest")], 1)
(A / "fuente/seguimiento.json").write_text(json.dumps([[round(x, 1), round(y, 1)] for x, y in seg]), encoding="utf-8")
print("cx", np.percentile(med[:, 0], [5, 50, 95]).round(), "top", np.percentile(med[:, 1], [5, 50, 95]).round())
