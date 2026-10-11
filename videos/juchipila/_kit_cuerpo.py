# -*- coding: utf-8 -*-
"""Prueba de kz_pers2d.cuerpo: python _kit_cuerpo.py nombre t  [tipo:piernas:brazos:vista:mirar:s ...]  -> previews/<nombre>.png"""
import sys, time
import cv2, numpy as np
import estilos
estilos.activar("kurzgesagt")
from motor import Lienzo, a_uint8, componer, W, H
import kz_pers2d as K

nombre, t = sys.argv[1], float(sys.argv[2])
cfg = sys.argv[3:]
ys = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
c0, c1 = np.float32((110, 190, 230)) / 255, np.float32((250, 230, 190)) / 255
bg = (c0 * (1 - ys) + c1 * ys) * np.ones((1, W, 1), np.float32)
lz = Lienzo()
lz.nuevo(t, wob=0.0)
n = len(cfg)
lz.relleno([(0, 940), (W, 940), (W, H), (0, H)], (120, 160, 90))
for i, c in enumerate(cfg):
    p = (c.split(":") + ["", "", "", "", "", ""])[:7]
    tipo, pi_, br, vis, mi, sz, dt = p
    cx = W * (i + 0.5) / n
    K.cuerpo(lz, cx, 960, float(sz or 40), tipo, t + float(dt or 0), piernas=pi_ or "idle", brazos=br or "balanceo", vista=vis or "perfil", mirar=int(mi or 1), seed=i)
t0 = time.time()
img = componer(bg, lz.resolver(), boil=lz.boil)
cv2.imwrite(f"previews/{nombre}.png", cv2.cvtColor(a_uint8(np.clip(img, 0, 1)), cv2.COLOR_RGB2BGR))
print("ok", round(time.time() - t0, 2), "s")
