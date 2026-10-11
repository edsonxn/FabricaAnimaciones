# -*- coding: utf-8 -*-
"""Hoja de cuadros en momentos clave del recorrido (anclados a palabras): python _hoja_rec.py [grupo] -> previews/rec_<grupo>.jpg
Cada cuadro también se guarda suelto en previews/r_<t>.jpg para mirarlo a tamaño completo."""
import sys
import time

import cv2
import numpy as np

import escenas as S
from kit import INI, FIN, ww, TL

GR = {
    "a": [("gancho", 0, 0.5), ("gancho", 2, 0.5), ("gancho", 4, 1.5), ("gancho", 6, 0.3), ("gancho", 7, 2.5), ("origen", 0, 1.8),
          ("origen", 1, 3.0), ("origen", 3, 2.0), ("origen", 5, 3.0), ("origen", 5, 6.5), ("origen", 8, 1.5), ("origen", 9, 2.5)],
    "b": [("genesis", 0, 3.0), ("genesis", 1, 2.0), ("genesis", 2, 4.0), ("genesis", 4, 3.0), ("genesis", 6, 1.0), ("genesis", 7, 3.0),
          ("fantasma", 0, 4.0), ("fantasma", 2, 3.5), ("fantasma", 4, 4.0), ("fantasma", 6, 2.0), ("fantasma", 8, 3.0), ("fortuna", 1, 3.0)],
    "c": [("fortuna", 2, 3.0), ("fortuna", 5, 5.0), ("fortuna", 6, 1.5), ("perfil", 0, 2.5), ("perfil", 2, 3.0), ("perfil", 3, 3.0),
          ("perfil", 5, 3.0), ("perfil", 6, 3.5), ("perfil", 8, 3.5), ("dorian", 1, 4.0), ("dorian", 4, 3.0), ("dorian", 6, 5.0)],
    "d": [("hal", 0, 2.0), ("hal", 4, 2.0), ("hal", 6, 4.0), ("hal", 7, 4.0), ("szabo", 1, 3.0), ("szabo", 4, 4.0), ("wright", 3, 4.0),
          ("wright", 4, 3.0), ("wright", 8, 6.5), ("wright", 10, 3.5), ("todd", 2, 4.0), ("todd", 6, 2.5)],
    "e": [("leroux", 1, 3.0), ("leroux", 2, 6.0), ("back", 0, 2.5), ("back", 2, 3.0), ("back", 6, 5.0), ("back", 8, 3.0), ("archivo", 2, 3.0),
          ("espejo", 1, 1.5), ("cierre", 0, 2.5), ("cierre", 1, 2.0), ("cierre", 4, 3.0), ("cierre", 6, 4.0)],
}
g = sys.argv[1] if len(sys.argv) > 1 else "a"
m = S.CLASES[TL["escenas"][0]["id"]](TL["escenas"][0], 0)
ims = []
for e, f, dt in GR[g]:
    t = INI(e, f) + dt
    t0 = time.time()
    fr = m.render(None, t)
    f8 = cv2.cvtColor((np.clip(fr, 0, 1) * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
    cv2.imwrite(f"previews/r_{t:.1f}.jpg", f8, [cv2.IMWRITE_JPEG_QUALITY, 90])
    s = cv2.resize(f8, (640, 360), interpolation=cv2.INTER_AREA)
    cv2.rectangle(s, (0, 0), (250, 22), (0, 0, 0), -1)
    cv2.putText(s, f"{e}[{f}]+{dt} t={t:.1f}", (4, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1, cv2.LINE_AA)
    ims.append(s)
    print(f"{e}[{f}] t={t:.1f} {time.time() - t0:.2f}s", flush=True)
while len(ims) % 3:
    ims.append(np.zeros_like(ims[0]))
cv2.imwrite(f"previews/rec_{g}.jpg", np.vstack([np.hstack(ims[i:i + 3]) for i in range(0, len(ims), 3)]), [cv2.IMWRITE_JPEG_QUALITY, 88])
print("ok")
