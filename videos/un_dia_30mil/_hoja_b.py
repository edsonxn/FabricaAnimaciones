"""Hoja de cuadros por escena: python _hoja.py esc1 esc2 ... [--f 0.15 0.4 0.65 0.9]  ->  previews/hoja_<esc1>.jpg (una fila por escena)."""
import sys
import time

import cv2
import numpy as np

import escenas as E

args = sys.argv[1:]
fr = [0.12, 0.38, 0.64, 0.9]
if "--f" in args:
    i = args.index("--f")
    fr = [float(a) for a in args[i + 1:]]
    args = args[:i]
esc = {e["id"]: e for e in E.TL["escenas"]}
m = E.Mundo(E.TL["escenas"][0], 0)
filas = []
for eid in args:
    e = esc[eid]
    fila = []
    for f in fr:
        t = e["t0"] + f * (e["t1"] - e["t0"])
        t0 = time.time()
        im = m.render(None, t)
        small = cv2.resize((im[..., ::-1] * 255).astype(np.uint8), (640, 360), interpolation=cv2.INTER_AREA)
        cv2.putText(small, f"{eid} {t:.1f}s", (8, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        fila.append(small)
    filas.append(np.hstack(fila))
    print(eid, "ok")
cv2.imwrite(f"previews/hoja_{args[0]}.jpg", np.vstack(filas))
