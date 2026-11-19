# -*- coding: utf-8 -*-
"""Cuadros sueltos (clip + capa de FX) en los segundos pedidos → previews/cuadros_NN.jpg (12 por hoja), para revisar
arreglos de la hoja de FX sin volver a sacar las 13 hojas.      python _cuadros.py 25.1 89.5 155.5 ..."""
import os
import sys

import cv2
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))
sys.path.insert(0, AQUI)
import secuencia_fx as SF  # noqa: E402

capa = SF.cargar()
S = capa.S
mw, mh = 480, 270
minis = []
for t in [float(x) for x in sys.argv[1:]]:
    k = next((i for i, b in enumerate(capa.bs) if b["t0"] <= t < b["t1"]), len(capa.bs) - 1)
    b = capa.bs[k]
    fuente = S._fuente(b, k, True, capa)
    f = capa.aplicar(capa.envolver(fuente, b).cuadro(t), t)
    cap = getattr(fuente, "cap", None)
    if cap is not None:
        cap.release()
    m = cv2.resize(f, (mw, mh), interpolation=cv2.INTER_AREA)
    cv2.rectangle(m, (0, mh - 26), (mw, mh), (20, 18, 18), -1)
    activos = [d.get("nombre", d["tipo"])[:18] for d in capa.fx if d["de"] <= t <= d["a"] and d["tipo"] in ("mg", "pantalla")]
    cv2.putText(m, f"{t:.1f}s {b['id'][6:]} {' | '.join(activos)}".encode("ascii", "replace").decode()[:70], (6, mh - 7),
                cv2.FONT_HERSHEY_SIMPLEX, .42, (90, 214, 255), 1, cv2.LINE_AA)
    minis.append(m)
cols, n = 4, 12
for h in range(0, len(minis), n):
    g = minis[h:h + n] + [np.zeros_like(minis[0])] * (-len(minis[h:h + n]) % cols)
    ruta = f"previews/cuadros_{h // n + 1:02d}.jpg"
    cv2.imwrite(ruta, np.vstack([np.hstack(g[i:i + cols]) for i in range(0, len(g), cols)]))
    print(ruta)
