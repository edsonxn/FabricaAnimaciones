# -*- coding: utf-8 -*-
"""Lee una capa 3D transparente (render3d.py en modo video: <base>_color.mp4 + <base>_alfa.mp4) como FX «mg» de
secuencia_fx: fn(dt, dur, marcas) -> BGRA del cuadro entero (27-oct-2026). Sin archivos devuelve una capa vacía."""
import os

import cv2
import numpy as np


class _Lector:
    def __init__(self, ruta):
        self.ruta, self.cap, self.i, self.ult = ruta, None, -1, None

    def cuadro(self, k):
        if self.cap is None:
            self.cap = cv2.VideoCapture(self.ruta)
        if k != self.i + 1:
            if k == self.i and self.ult is not None:
                return self.ult
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, k)
        ok, f = self.cap.read()
        if ok:
            self.i, self.ult = k, f
        return self.ult


def capa3d(base, fps=30, w=1920, h=1080):
    """base = ruta sin sufijo (…/capas/j6_rocket). Devuelve fn para dict(tipo="mg", fn=…)."""
    col, alf = base + "_color.mp4", base + "_alfa.mp4"
    vacia = np.zeros((h, w, 4), np.uint8)
    if not (os.path.exists(col) and os.path.exists(alf)):
        print("  (capa 3D) falta", os.path.basename(base), "→ python <video>/capas3d.py")
        return lambda dt, dur, marcas: vacia
    lc, la = _Lector(col), _Lector(alf)
    n = int(cv2.VideoCapture(col).get(cv2.CAP_PROP_FRAME_COUNT))

    def fn(dt, dur, marcas):
        k = min(max(int(round(dt * fps)), 0), n - 1)
        c, a = lc.cuadro(k), la.cuadro(k)
        if c is None or a is None:
            return vacia
        if c.shape[1] != w:
            c, a = cv2.resize(c, (w, h)), cv2.resize(a, (w, h))
        return np.dstack([c, a[..., 0]])
    fn._capa3d = base
    return fn
