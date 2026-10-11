# -*- coding: utf-8 -*-
"""Hoja de prueba de dibujos sobre el mapa pintado: python _obj_test.py <módulo> [filtro]  -> previews/obj_<módulo>.jpg"""
import importlib
import inspect
import sys

import cv2
import numpy as np

import boceto as B
import mapa as M

mod = importlib.import_module(sys.argv[1])
filtro = sys.argv[2] if len(sys.argv) > 2 else ""
M.cargar()
M.usar("eu")
cam = M.Cam(-3.7, 40.0, 2.3)
fondo, base = M.pintar_base(cam, 0)
dibs = []
for n, f in inspect.getmembers(mod, callable):
    g = getattr(f, "__wrapped__", f)
    if not inspect.isfunction(g) or g.__module__ != mod.__name__ or n.startswith("_") or filtro not in n:
        continue
    try:
        sig = inspect.signature(g)
        if any(p.default is inspect.Parameter.empty for p in sig.parameters.values()):
            continue
        d = f()
    except Exception as e:                       # noqa: BLE001
        print("ERROR", n, e)
        continue
    if isinstance(d, B.Dib):
        dibs.append((n, d))
cols = 5
celda_w, celda_h = 1920 // cols, 360
hojas = []
for i0 in range(0, len(dibs), cols * 3):
    h = B.Hoja()
    h.limpiar()
    h.fondo = fondo.copy()
    for k, (n, d) in enumerate(dibs[i0:i0 + cols * 3]):
        cx = celda_w * (k % cols) + celda_w / 2
        cy = 360 * (k // cols) + 320
        pts = np.vstack([op[1] for op in d.ops])
        alto = max(1.0, -pts[:, 1].min(), pts[:, 1].max() - pts[:, 1].min())
        ancho = max(1.0, pts[:, 0].max() - pts[:, 0].min())
        s = min(280 / alto, (celda_w - 30) / ancho, 1.3)
        d.dibujar(h, cx - (pts[:, 0].min() + pts[:, 0].max()) / 2 * s, cy - max(0, pts[:, 1].max()) * s, s, 0, False, 1.0, 0, k, peg=True, tv=0.0)
        m = B.mascara_texto(n, 30)
        h.pegar_mascara(m, cx - m.shape[1] / 2, cy + 6)
    o = (np.clip(h.componer(), 0, 1) * 255).astype(np.uint8)[..., ::-1]
    hojas.append(o)
for i, o in enumerate(hojas):
    cv2.imwrite(f"previews/obj_{sys.argv[1]}_{i}.jpg", o, [cv2.IMWRITE_JPEG_QUALITY, 90])
print(len(dibs), "dibujos,", len(hojas), "hojas")
