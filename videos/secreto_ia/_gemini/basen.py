# -*- coding: utf-8 -*-
"""Base de las escenas noir de «El caso de la máquina»: lienzo Noir compartido y montaje por PLANOS.

Cada escena define sus planos en armar():  self.plano(t_inicio_global, fn, tr="barrido", dur=0.6)
fn(h, t, u) dibuja el plano (u = t - inicio del plano) y devuelve el cuadro terminado con h.acabado(...).
En la ventana de transición se renderizan el plano anterior y el nuevo y se mezclan con noir.transicion().
entrada/salida = transición con la escena vecina (por defecto tinta; la escena anterior termina cubierta y esta se descubre).
"""
import math

import numpy as np

from escena_base import Escena
from motor import H, W, clamp01, e_inout, e_out, prog, smooth
import noir as N
from noir import Noir

_H = None


def lienzo():
    global _H
    if _H is None:
        _H = Noir()
    return _H


class Plano:
    def __init__(self, t0, fn, tr, dur, kw):
        self.t0, self.fn, self.tr, self.dur, self.kw = t0, fn, tr, dur, kw


class BaseNoir(Escena):
    TR_SALIDA = ("tinta", 0.7)    # transición HACIA la escena siguiente: se dibuja su arranque debajo y se mezclan (sin negro)

    def preparar(self):
        self.planos = []
        self.armar()
        self.planos.sort(key=lambda p: p.t0)
        self.sonidos()

    def armar(self):
        pass

    def sonidos(self):
        pass

    def plano(self, t0, fn, tr="corte", dur=0.6, **kw):
        self.planos.append(Plano(t0, fn, tr, dur, kw))

    def _r(self, i, t):
        h = lienzo()
        h.nuevo(t, None)
        pl = self.planos[i]
        return pl.fn(h, t, t - pl.t0)

    def render_base(self, t):
        ps = self.planos
        i = max([k for k, p in enumerate(ps) if p.t0 <= t] or [0])
        img = self._r(i, t)
        if i > 0 and t < ps[i].t0 + ps[i].dur:
            prev = self._r(i - 1, t)
            img = N.transicion(prev, img, (t - ps[i].t0) / ps[i].dur, ps[i].tr, sem=i, **ps[i].kw)
        return img

    def siguiente(self):
        if not hasattr(self, "_sig"):
            import escenas as S
            esc = S._TL["escenas"]
            ids = [e["id"] for e in esc]
            k = ids.index(self.id)
            # .get: mientras se escriben las escenas, la siguiente puede no existir todavía
            self._sig = S.CLASES[ids[k + 1]](esc[k + 1], k + 1) if k + 1 < len(ids) and ids[k + 1] in S.CLASES else None
        return self._sig

    def render(self, lz, t):
        img = self.render_base(t)
        tipo, d = self.TR_SALIDA
        sig = self.siguiente() if t > self.t1 - d else None
        if sig is not None:
            B = sig.render_base(t)
            img = N.transicion(img, B, (t - (self.t1 - d)) / d, tipo, sem=self.idx * 7 + 3)
        return np.clip(img, 0, 1)
