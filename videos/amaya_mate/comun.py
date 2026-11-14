# -*- coding: utf-8 -*-
"""Anclas a la voz, fondos cacheados y transiciones de acuarela (comunes a todos los planos)."""
import json
import math
import re
import unicodedata

import numpy as np

from acuarela import H, W, PIG, clamp, degradado, lavado, mancha_pts, pr, rgb, suave

TL = json.load(open("timeline.json", encoding="utf-8"))
TOTAL = TL["total"]
ESC = {e["id"]: e for e in TL["escenas"]}


def _n(s):
    s = unicodedata.normalize("NFD", s.lower())
    return re.sub(r"[^a-z0-9ñ]+", "", "".join(c for c in s if unicodedata.category(c) != "Mn"))


def ww(esc, frase, palabra, n=0, fin=False):
    """Segundo en que la voz dice `palabra` (varias palabras = secuencia) en la frase `frase` de la escena `esc`."""
    obj = [_n(x) for x in palabra.split()]
    ws = ESC[esc]["frases"][frase]["words"]
    nw = [_n(x["w"]) for x in ws]
    hits = [ws[i + len(obj) - 1]["e"] if fin else ws[i]["s"]
            for i in range(len(ws) - len(obj) + 1) if all(nw[i + j].startswith(obj[j]) for j in range(len(obj)))]
    if len(hits) <= n:
        raise KeyError(f"[{esc}/{frase}] palabra no encontrada: {palabra}")
    return hits[n]


def INI(esc, frase=0):
    return ESC[esc]["frases"][frase]["words"][0]["s"]


def FIN(esc, frase=-1):
    return ESC[esc]["frases"][frase]["words"][-1]["e"]


def T0(esc):
    return ESC[esc]["t0"]


def T1(esc):
    return ESC[esc]["t1"]


# ------------------------------------------------------------ fondos cacheados (uno por proceso)
_CACHE = {}


def cache(clave, fn):
    if clave not in _CACHE:
        _CACHE[clave] = fn()
    return _CACHE[clave]


def fondo_agua(arriba, abajo, mancha, alto, seed, n=9, alfa=0.33):
    """Agua en acuarela: degradado vertical + manchas húmedas superpuestas. Devuelve (alto, W, 3)."""
    def f():
        im = np.zeros((alto, W, 3), np.float32)
        u = np.linspace(0, 1, alto, dtype=np.float32)[:, None, None]
        im[:] = np.asarray(arriba, np.float32) * (1 - u) + np.asarray(abajo, np.float32) * u
        import acuarela as A
        Hs = A.H
        rg = np.random.default_rng(seed)
        for k in range(n):
            cx, cy = rg.uniform(-100, W + 100), rg.uniform(0, alto)
            r = rg.uniform(200, 420)
            for y0 in range(0, alto, Hs):
                if y0 - 500 < cy < y0 + Hs + 500:
                    sub = im[y0:y0 + Hs]
                    if sub.shape[0] == Hs:
                        lavado(sub, mancha_pts(cx, cy - y0, r, seed + k, 0.28, ry=r * rg.uniform(0.45, 0.8)), mancha,
                               alfa * rg.uniform(0.6, 1.1), seed + k, humedo=16)
        return im
    return cache(("agua", seed, alto), f)


def corte(fondo, off):
    off = int(clamp(off, 0, fondo.shape[0] - H))
    return fondo[off:off + H].copy()


# ------------------------------------------------------------ transición: la acuarela se desborda
_RUIDO_T = None


def _ruido_t():
    global _RUIDO_T
    if _RUIDO_T is None:
        import cv2
        r = np.random.default_rng(77).random((H // 24 + 2, W // 24 + 2)).astype(np.float32)
        a = cv2.resize(r, (W, H), interpolation=cv2.INTER_CUBIC)
        b = cv2.GaussianBlur(PIG[2], (0, 0), 10) - 0.5
        _RUIDO_T = (a - 0.5) * 1.0 + b * 1.6
    return _RUIDO_T


_YY, _XX = np.mgrid[0:H, 0:W].astype(np.float32)


def desborde(A, B, u, cx=W / 2, cy=H / 2, borde=(0.25, 0.18, 0.22)):
    """B entra sobre A como una gota de acuarela que se expande desde (cx, cy), con borde húmedo oscuro."""
    if u <= 0:
        return A
    if u >= 1:
        return B
    d = np.sqrt((_XX - cx) ** 2 + (_YY - cy) ** 2) / math.hypot(W, H)
    f = suave(u) * 1.25 - d + _ruido_t() * 0.12
    m = np.clip(f / 0.03, 0, 1)
    e = np.exp(-((f - 0.015) / 0.02) ** 2) * (1 - abs(2 * u - 1)) * 0.9
    out = A * (1 - m[..., None]) + B * m[..., None]
    out *= 1 - e[..., None] * (1 - np.asarray(borde, np.float32))
    return out
