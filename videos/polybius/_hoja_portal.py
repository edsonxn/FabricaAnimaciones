# -*- coding: utf-8 -*-
"""Hoja de portales: python _hoja_portal.py nombre:dt,dt nombre2 ... [--out previews/portales.jpg]
dt = segundos DESPUÉS del ancla natural de cada portal (si no se dan: 0.5, 2.5, 5)."""
import sys
import time

import cv2
import numpy as np

import portales as PO
from kit import INI, ww

ANCLA = {
    "salon": lambda: INI("gancho", 1), "fascinados": lambda: INI("leyenda", 0), "pesadilla": lambda: INI("leyenda", 1),
    "hombres": lambda: INI("leyenda", 3), "vacio": lambda: INI("leyenda", 4), "maraton": lambda: INI("casos", 2),
    "migrana": lambda: INI("casos", 3), "redada": lambda: INI("casos", 4) + 2.0, "corazon": lambda: INI("casos", 6),
    "tanque": lambda: INI("gobierno", 1), "prueba": lambda: INI("gobierno", 4), "hemeroteca": lambda: INI("pruebas", 5),
    "web2000": lambda: INI("origen", 2) + 1.5, "viaje": lambda: INI("origen", 6), "padres": lambda: INI("porque", 1),
    "mente": lambda: INI("porque", 3), "recreacion": lambda: INI("porque", 6), "busqueda": lambda: INI("cierre", 3),
}
o = sys.argv.index("--out") if "--out" in sys.argv else len(sys.argv)
args = sys.argv[1:o] or list(ANCLA)
out = sys.argv[o + 1] if o < len(sys.argv) else "previews/portales.jpg"
ims = []
for a in args:
    nom, _, dts = a.partition(":")
    for dt in ([float(x) for x in dts.split(",")] if dts else [0.5, 2.5, 5.0]):
        t = ANCLA[nom]() + dt
        t0 = time.time()
        im = PO.PORTAL[nom](t)
        f8 = cv2.cvtColor((np.clip(im, 0, 1) * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
        f8 = cv2.resize(f8, (640, 360), interpolation=cv2.INTER_AREA)
        cv2.rectangle(f8, (0, 0), (260, 22), (0, 0, 0), -1)
        cv2.putText(f8, f"{nom} +{dt:.1f} ({(time.time() - t0) * 1000:.0f}ms)", (4, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1, cv2.LINE_AA)
        ims.append(f8)
while len(ims) % 3:
    ims.append(np.zeros_like(ims[0]))
cv2.imwrite(out, np.vstack([np.hstack(ims[i:i + 3]) for i in range(0, len(ims), 3)]), [cv2.IMWRITE_JPEG_QUALITY, 88])
print("ok", len(ims), out)
