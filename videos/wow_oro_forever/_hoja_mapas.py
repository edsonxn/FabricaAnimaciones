# -*- coding: utf-8 -*-
"""Cuadro final de CADA mapa (12-nov: el usuario cazó puntos en el mar): previews/mapas_NN.jpg.  python _hoja_mapas.py"""
import os, sys
import cv2, numpy as np
AQUI = os.path.dirname(os.path.abspath(__file__)); os.chdir(AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo")); sys.path.insert(0, AQUI)
os.environ["FAB_FX_FINAL"] = "1"
import secuencia_fx as SF
capa = SF.cargar(); S = capa.S
mapas = [d for d in capa.fx if str(d.get("nombre", "")).startswith("mapa")]
if len(sys.argv) > 1: mapas = [d for d in mapas if any(x in d["nombre"] for x in sys.argv[1:])]
minis = []
for d in mapas:
    t = d["de"] + 0.8 * (d["a"] - d["de"])
    k = next((i for i, b in enumerate(capa.bs) if b["t0"] <= t < b["t1"]), len(capa.bs) - 1)
    b = capa.bs[k]
    f = capa.aplicar(capa.envolver(S._fuente(b, k, True, capa), b).cuadro(t), t)
    m = cv2.resize(f, (640, 360), interpolation=cv2.INTER_AREA)
    cv2.putText(m, f"{int(t//60)}:{t%60:04.1f} " + d["nombre"].encode("ascii", "replace").decode(), (6, 352), cv2.FONT_HERSHEY_SIMPLEX, .5, (90, 214, 255), 1)
    minis.append(m)
for h in range(0, len(minis), 9):
    g = minis[h:h+9] + [np.zeros_like(minis[0])] * (-len(minis[h:h+9]) % 3)
    cv2.imwrite(f"previews/mapas_{h//9+1:02d}.jpg", np.vstack([np.hstack(g[i:i+3]) for i in range(0, len(g), 3)]))
print(len(minis), "mapas")
