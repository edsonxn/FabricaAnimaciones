# -*- coding: utf-8 -*-
"""Hoja de cuadros del recorrido: python _hoja_rec.py a|b|c|d|e  -> previews/rec_<g>.jpg (y cada cuadro suelto en previews/r_<t>.jpg)
            python _hoja_rec.py t 12.5 30 44.1  -> tiempos absolutos (previews/rec_t.jpg)"""
import sys
import time

import cv2
import numpy as np

import escenas as S
from kit import INI, FIN, ww, TL

GR = {
    "a": [("gancho", 0, 0.5), ("gancho", 0, 3.0), ("gancho", 1, 1.0), ("gancho", 1, 4.5), ("gancho", 2, 3.0), ("gancho", 3, 1.2), ("gancho", 3, 3.5),
          ("leyenda", 0, 0.3), ("leyenda", 0, 2.5), ("leyenda", 1, 1.5), ("leyenda", 1, 4.5), ("leyenda", 2, 2.5)],
    "b": [("leyenda", 3, 0.6), ("leyenda", 3, 4.0), ("leyenda", 4, 0.5), ("leyenda", 4, 3.5), ("casos", 0, 1.0), ("casos", 0, 3.3), ("casos", 1, 2.5),
          ("casos", 1, 6.5), ("casos", 2, 1.5), ("casos", 2, 4.3), ("casos", 3, 2.5), ("casos", 3, 4.6)],
    "c": [("casos", 3, 6.5), ("casos", 4, 1.2), ("casos", 4, 5.0), ("casos", 5, 3.5), ("casos", 6, 0.3), ("casos", 6, 5.0), ("gobierno", 0, 1.0),
          ("gobierno", 0, 3.6), ("gobierno", 1, 2.0), ("gobierno", 1, 4.6), ("gobierno", 1, 7.0), ("gobierno", 2, 1.6)],
    "d": [("gobierno", 2, 5.0), ("gobierno", 3, 1.8), ("gobierno", 4, 0.3), ("gobierno", 4, 4.0), ("gobierno", 5, 1.5), ("gobierno", 5, 4.5),
          ("gobierno", 6, 1.2), ("gobierno", 6, 3.5), ("pruebas", 0, 1.8), ("pruebas", 1, 3.0), ("pruebas", 1, 5.2), ("pruebas", 1, 7.3)],
    "e": [("pruebas", 2, 1.8), ("pruebas", 2, 5.5), ("pruebas", 3, 2.5), ("pruebas", 3, 5.5), ("pruebas", 4, 1.8), ("pruebas", 5, 0.4), ("pruebas", 5, 2.5),
          ("pruebas", 6, 2.5), ("origen", 0, 2.5), ("origen", 1, 1.8), ("origen", 2, 1.6), ("origen", 2, 3.5)],
    "f": [("origen", 2, 6.0), ("origen", 3, 3.5), ("origen", 4, 5.0), ("origen", 5, 2.5), ("origen", 5, 7.5), ("origen", 6, 0.4), ("origen", 6, 2.5),
          ("origen", 6, 4.5), ("origen", 7, 2.0), ("origen", 7, 5.5), ("origen", 8, 2.5), ("origen", 8, 5.5)],
    "g": [("porque", 0, 1.5), ("porque", 1, 0.4), ("porque", 1, 3.5), ("porque", 2, 1.5), ("porque", 2, 3.6), ("porque", 3, 0.4), ("porque", 3, 3.5),
          ("porque", 4, 1.0), ("porque", 4, 3.2), ("porque", 5, 2.5), ("porque", 5, 5.0), ("porque", 5, 8.0)],
    "h": [("porque", 6, 0.4), ("porque", 6, 4.0), ("porque", 7, 2.0), ("porque", 7, 4.5), ("porque", 7, 8.5), ("cierre", 0, 1.5), ("cierre", 0, 4.6),
          ("cierre", 1, 3.0), ("cierre", 2, 1.2), ("cierre", 3, 2.5), ("cierre", 4, 3.5), ("cierre", 4, 8.5)],
}
g = sys.argv[1] if len(sys.argv) > 1 else "a"
if g == "t":
    lista = [(None, None, float(x)) for x in sys.argv[2:]]
else:
    lista = GR[g]
m = S.CLASES[TL["escenas"][0]["id"]](TL["escenas"][0], 0)
ims = []
for e, f, dt in lista:
    t = dt if e is None else INI(e, f) + dt
    t0 = time.time()
    fr = m.render(None, t)
    f8 = cv2.cvtColor((np.clip(fr, 0, 1) * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
    cv2.imwrite(f"previews/r_{t:.1f}.jpg", f8, [cv2.IMWRITE_JPEG_QUALITY, 90])
    s = cv2.resize(f8, (640, 360), interpolation=cv2.INTER_AREA)
    cv2.rectangle(s, (0, 0), (250, 22), (0, 0, 0), -1)
    cv2.putText(s, (f"{e}[{f}]+{dt} " if e else "") + f"t={t:.1f}", (4, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1, cv2.LINE_AA)
    ims.append(s)
    print(f"{e}[{f}] t={t:.1f} {time.time() - t0:.2f}s", flush=True)
while len(ims) % 3:
    ims.append(np.zeros_like(ims[0]))
cv2.imwrite(f"previews/rec_{g}.jpg", np.vstack([np.hstack(ims[i:i + 3]) for i in range(0, len(ims), 3)]), [cv2.IMWRITE_JPEG_QUALITY, 88])
print("ok")
