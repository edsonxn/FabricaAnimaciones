# -*- coding: utf-8 -*-
"""medidas.json → tomas.json: por toma [i0, i1, escala, cx, top] (medianas; cabeza a ~340 px de ancho)."""
import json
from pathlib import Path
import numpy as np

A = Path(__file__).parent
med = json.load(open(A / "fuente/medidas.json"))
CORTES = [0, 127, 207, 290, 353, 454, 493, 621]
tomas = []
for a, b in zip(CORTES[:-1], CORTES[1:]):
    m = med[a + 3:b - 2]
    w = float(np.median([x["w"] for x in m])); cx = float(np.median([x["cx"] for x in m])); top = float(np.median([x["top"] for x in m]))
    s = min(1.7, 340 / w)
    tomas.append([a, b, round(s, 3), round(cx), round(top)])
    print(f"{a:3d}-{b:3d}  w={w:5.0f} cx={cx:5.0f} top={top:5.0f}  escala={s:.2f}  cuerpo visible={(1100 - top) * s:4.0f}px")
(A / "fuente/tomas.json").write_text(json.dumps(tomas))
