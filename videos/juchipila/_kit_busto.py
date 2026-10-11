# -*- coding: utf-8 -*-
"""Prueba del kit kz_pers2d.busto: python _kit_busto.py nombre t [tipos...]  -> previews/<nombre>.png"""
import sys, time
import cv2, numpy as np
import estilos
estilos.activar("kurzgesagt")
from motor import Lienzo, a_uint8, componer, W, H
import kz_pers2d as K
import kz_ui as U

nombre, t = sys.argv[1], float(sys.argv[2])
cfg = sys.argv[3:] or ["mujer"]
ys = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
xs = np.linspace(0, 1, W, dtype=np.float32)[None, :, None]
c0, c1 = np.float32((60, 24, 120)) / 255, np.float32((14, 6, 34)) / 255
bg = (c0 * (1 - ys) + c1 * ys) * np.ones((1, W, 1), np.float32)
d = np.sqrt(((xs - 0.5) * 1.2) ** 2 + ((ys - 0.45) * 0.9) ** 2)
bg = bg * (1 - 0.55 * np.clip(d - 0.2, 0, 1))
lz = Lienzo()
lz.nuevo(t, wob=0.0)
n = len(cfg)
for i, c in enumerate(cfg):
    nm, _, extra = c.partition(":")
    kw = {}
    for kv in filter(None, extra.split(",")):
        k, v = kv.split("=")
        kw[k] = v if k in ("emocion", "mano", "ojos") else float(v)
    cx = W * (i + 0.5) / n
    cy = kw.pop("cy", 760); sz = kw.pop("s", 150 if n > 1 else 220); K.busto(lz, cx, cy, sz, nm, t, **kw)
t0 = time.time()
img = componer(bg, lz.resolver(), boil=lz.boil)
cv2.imwrite(f"previews/{sys.argv[1]}.png", cv2.cvtColor(a_uint8(np.clip(img, 0, 1)), cv2.COLOR_RGB2BGR))
print("ok", round(time.time() - t0, 2), "s")
