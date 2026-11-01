# -*- coding: utf-8 -*-
"""Hoja de los lugares pintados de un módulo (luz plana, sin personajes) -> previews/ver_<modulo>.jpg
    python videos/sociedad_1200/_ver_mundos.py mundos_1 [nombre ...] [--rampa piedra] [--zoom 0.6]"""
import importlib
import inspect
import os
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [AQUI, os.path.join(AQUI, "..", "..", "nucleo")]
os.chdir(AQUI)

import cv2
import numpy as np

import noir_color as NC

a = sys.argv[1:]
mod = importlib.import_module(a[0])
rampa = a[a.index("--rampa") + 1] if "--rampa" in a else "piedra"
zoom = float(a[a.index("--zoom") + 1]) if "--zoom" in a else 0.7
nombres = [x for x in a[1:] if not x.startswith("--") and x not in (rampa, str(zoom))]
fns = [(n, f) for n, f in inspect.getmembers(mod, inspect.isfunction) if f.__module__ == mod.__name__ and not n.startswith("_")
       and (not nombres or n in nombres) and not inspect.signature(f).parameters]
h = NC.NoirColor("sodio")
tiles = []
for n, f in fns:
    t0 = time.time()
    try:
        capa = f()
    except Exception as e:                                   # noqa
        print(n, "ERROR", e)
        continue
    dt = time.time() - t0
    h.nuevo(0.0)
    h.camara(zoom, 960, 540)
    h.img[:] = 0.05
    NC.pegar(capa, h, 1.0, rampa=rampa)
    h.ambiente[:] = 1.0
    im = (np.clip(h.acabado(0.0, grano=0, polvo=0, vin=0.3), 0, 1) * 255).astype(np.uint8)
    sm = cv2.resize(im, (640, 360), interpolation=cv2.INTER_AREA)
    for c, g in (((0, 0, 0), 3), ((255, 255, 255), 1)):
        cv2.putText(sm, f"{n} {dt:.1f}s", (6, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.55, c, g, cv2.LINE_AA)
    tiles.append(sm)
    print(n, f"{dt:.1f}s")
while len(tiles) % 3:
    tiles.append(np.zeros_like(tiles[0]))
hoja = np.vstack([np.hstack(tiles[i:i + 3]) for i in range(0, len(tiles), 3)])
cv2.imwrite(f"previews/ver_{a[0]}.jpg", cv2.cvtColor(hoja, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 88])
print("->", f"previews/ver_{a[0]}.jpg")
