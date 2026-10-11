# -*- coding: utf-8 -*-
"""Hoja de portales: python _hoja_portal.py nombre:dt,dt nombre2 ... [--out previews/portales.jpg]
dt = segundos DESPUÉS del ancla natural de cada portal (si no se dan: 0.5, 2, 4)."""
import sys
import time

import cv2
import numpy as np

import portales as PO
from kit import INI, ww

ANCLA = {
    "boveda": lambda: 2.0, "lehman": lambda: ww("origen", 1, "quince"), "rescate": lambda: INI("origen", 2), "escritorio": lambda: INI("origen", 3),
    "navegador": lambda: ww("origen", 4, "registrado") - 0.3, "p2p": lambda: INI("origen", 9), "bloques": lambda: INI("genesis", 0),
    "pizza": lambda: INI("fantasma", 4), "wikileaks": lambda: INI("fantasma", 5), "maquina": lambda: INI("perfil", 3),
    "relojes": lambda: ww("perfil", 7, "costa"), "puerta": lambda: INI("dorian", 2), "persecucion": lambda: INI("dorian", 4),
    "cuadras": lambda: ww("dorian", 8, "cuadras"), "carrera": lambda: INI("hal", 6), "crio": lambda: INI("hal", 9),
    "bitgold": lambda: ww("szabo", 1, "llamado"), "escenario": lambda: INI("wright", 2), "fotocopia": lambda: INI("wright", 5),
    "tribunal": lambda: ww("wright", 8, "tajante"), "tele": lambda: INI("todd", 1), "foro_hora": lambda: ww("todd", 2, "corrigio"),
    "homenaje": lambda: INI("todd", 8), "hashcash": lambda: ww("back", 1, "invento"), "ia": lambda: INI("back", 5),
    "el_salvador": lambda: INI("back", 8), "estatua": lambda: INI("cierre", 5), "carcel": lambda: INI("leroux", 3),
    "archivo": lambda: INI("archivo", 0), "busto": lambda: INI("espejo", 0),
}
o = sys.argv.index("--out") if "--out" in sys.argv else len(sys.argv)
args = sys.argv[1:o] or list(ANCLA)
out = sys.argv[o + 1] if o < len(sys.argv) else "previews/portales.jpg"
ims = []
for a in args:
    nom, _, dts = a.partition(":")
    for dt in ([float(x) for x in dts.split(",")] if dts else [0.5, 2.0, 4.0]):
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
