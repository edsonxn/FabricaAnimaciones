# -*- coding: utf-8 -*-
"""Hoja de dibujos: python _hoja_dib.py modulo [modulo2 ...] [--cols N] -> previews/dib_<modulo>.jpg
Pinta cada función sin argumentos obligatorios del módulo como pegatina sobre papel, con su nombre."""
import importlib
import inspect
import sys

import cv2
import numpy as np

import boceto as B

mods = [a for a in sys.argv[1:] if not a.startswith("--")]
cols = 6
for a in sys.argv[1:]:
    if a.startswith("--cols"):
        cols = int(a.split("=")[1])
solo = None
for a in sys.argv[1:]:
    if a.startswith("--solo="):
        solo = a.split("=")[1].split(",")
for nombre in mods:
    m = importlib.import_module(nombre)
    fns = []
    for k, f in inspect.getmembers(m, callable):
        g = getattr(f, "__wrapped__", f)
        if not inspect.isfunction(g) or g.__module__ != m.__name__ or k.startswith("_") or k[0].isupper():
            continue
        if solo and k not in solo:
            continue
        try:
            sig = inspect.signature(g)
            if any(p.default is inspect._empty and p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD) for p in sig.parameters.values()):
                continue
        except (TypeError, ValueError):
            continue
        fns.append((k, f))
    tiles = []
    for k, f in fns:
        try:
            d = f()
        except Exception as e:  # noqa: BLE001
            print("ERROR", k, e)
            continue
        if not isinstance(d, B.Dib) or not d.ops:
            continue
        P = np.vstack([op[1] for op in d.ops])
        x0, y0 = P.min(0)
        x1, y1 = P.max(0)
        s = min(400 / max(1, x1 - x0), 400 / max(1, y1 - y0), 1.4)
        h = B.Hoja()
        h.limpiar()
        cx = 480 - (x0 + x1) / 2 * s
        cy = 300 - (y0 + y1) / 2 * s
        d.dibujar(h, cx, cy, s, 0.0, False, 1.0, 1, 0, peg=True)
        im = (np.clip(h.componer(), 0, 1)[..., ::-1] * 255).astype(np.uint8)
        im = im[40:560, 220:740]
        im = cv2.resize(im, (320, 320), interpolation=cv2.INTER_AREA)
        cv2.putText(im, k[:26], (6, 312), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 200), 1)
        tiles.append(im)
    if not tiles:
        continue
    while len(tiles) % cols:
        tiles.append(np.full_like(tiles[0], 255))
    rows = [np.hstack(tiles[i:i + cols]) for i in range(0, len(tiles), cols)]
    cv2.imwrite(f"previews/dib_{nombre}.jpg", np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 86])
    print(nombre, len(tiles), "dibujos")
