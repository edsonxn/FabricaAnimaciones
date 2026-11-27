# -*- coding: utf-8 -*-
"""Hoja FINAL (como `FAB_FX_FINAL=1 fx hoja`) solo de los FX que empiezan dentro de unos tramos, para revisar arreglos sin
rehacer la hoja entera (subagente C, 26-nov-2026).   python _hoja_sel.py 560-575 1040-1052 ...   → previews/fx_sel_NN.jpg"""
import os
import sys

import cv2
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
sys.path[:0] = [AQUI, os.path.join(AQUI, "..", "..", "nucleo")]
import secuencia_fx as SF  # noqa: E402

tramos = [tuple(float(x) for x in a.split("-")) for a in sys.argv[1:]]
capa = SF.cargar()
S = capa.S
ev = [(max(d["de"] + .3, d["a"] - .75), d.get("nombre") or f"apoyo {d.get('apoyo')}") for d in capa.fx
      if d["tipo"] in ("mg", "pantalla", "imagen") and any(a <= d["de"] <= b for a, b in tramos)]
ev.sort()
minis = []
for t, nombre in ev:
    k = next((i for i, b in enumerate(capa.bs) if b["t0"] <= t < b["t1"]), len(capa.bs) - 1)
    b = capa.bs[k]
    fuente = S._fuente(b, k, True, capa)
    f = capa.aplicar(capa.envolver(fuente, b).cuadro(t), t)
    cap = getattr(fuente, "cap", None)
    if cap is not None:
        cap.release()
    m = cv2.resize(f, (640, 360), interpolation=cv2.INTER_AREA)
    cv2.rectangle(m, (0, 334), (640, 360), (20, 18, 18), -1)
    cv2.putText(m, f"{t:.1f}s {nombre}".encode("ascii", "replace").decode(), (6, 353), cv2.FONT_HERSHEY_SIMPLEX, .5, (90, 214, 255), 1,
                cv2.LINE_AA)
    minis.append(m)
cols, n = 3, 12
for h in range(0, len(minis), n):
    g = minis[h:h + n] + [np.zeros_like(minis[0])] * (-len(minis[h:h + n]) % cols)
    r = f"previews/fx_sel_{h // n + 1:02d}.jpg"
    cv2.imwrite(r, np.vstack([np.hstack(g[i:i + cols]) for i in range(0, len(g), cols)]))
    print(r)
print(len(minis), "cuadros")
