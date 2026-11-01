# -*- coding: utf-8 -*-
"""Base de las escenas NOIR COLOR de «El gran expediente: Las 1.200 de OpenAI»: lienzo NoirColor compartido y montaje por PLANOS.

Cada escena define sus planos en armar():  self.plano(t_inicio_global, fn, tr="barrido", dur=0.6, pal="sodio")
fn(h, t, u) dibuja el plano (u = t - inicio del plano) y devuelve el cuadro terminado con h.acabado(...).
`pal` = paleta del plano (sodio · bourbon · medianoche); por defecto la PAL de la escena. Cada acto tiene su color:
el laboratorio de las copias en medianoche, Facebook 2017 en bourbon, la calle y el despacho del detective en sodio.
En la ventana de transición se renderizan el plano anterior y el nuevo y se mezclan con noir.transicion().
"""
import numpy as np

from escena_base import Escena
import noir as N
import noir_color as NC

_H = None


def lienzo():
    global _H
    if _H is None:
        _H = NC.NoirColor("medianoche")
    return _H


class Plano:
    def __init__(self, t0, fn, tr, dur, pal, kw):
        self.t0, self.fn, self.tr, self.dur, self.pal, self.kw = t0, fn, tr, dur, pal, kw


class BaseNoir(Escena):
    TR_SALIDA = ("tinta", 0.7)    # transición HACIA la escena siguiente: se dibuja su arranque debajo y se mezclan (sin negro)
    PAL = "medianoche"

    def preparar(self):
        self.planos = []
        self.armar()
        self.planos.sort(key=lambda p: p.t0)
        self.sonidos()

    def armar(self):
        pass

    def sonidos(self):
        pass

    def plano(self, t0, fn, tr="corte", dur=0.6, pal=None, **kw):
        self.planos.append(Plano(t0, fn, tr, dur, pal, kw))

    def _r(self, i, t):
        h = lienzo()
        pl = self.planos[i]
        h.usar_paleta(pl.pal or self.PAL)
        h.nuevo(t, None)
        return pl.fn(h, t, t - pl.t0)

    def render_base(self, t):
        ps = self.planos
        i = max([k for k, p in enumerate(ps) if p.t0 <= t] or [0])
        img = self._r(i, t)
        if i > 0 and t < ps[i].t0 + ps[i].dur:
            img = img.copy()
            prev = self._r(i - 1, t)
            img = N.transicion(prev, img, (t - ps[i].t0) / ps[i].dur, ps[i].tr, sem=i, **ps[i].kw)
        return img

    def siguiente(self):
        if not hasattr(self, "_sig"):
            import escenas as S
            esc = S._TL["escenas"]
            ids = [e["id"] for e in esc]
            k = ids.index(self.id)
            self._sig = S.CLASES[ids[k + 1]](esc[k + 1], k + 1) if k + 1 < len(ids) and ids[k + 1] in S.CLASES else None
        return self._sig

    def render(self, lz, t):
        img = self.render_base(t)
        tipo, d = self.TR_SALIDA
        sig = self.siguiente() if t > self.t1 - d else None
        if sig is not None:
            img = img.copy()
            B = sig.render_base(t)
            img = N.transicion(img, B, (t - (self.t1 - d)) / d, tipo, sem=self.idx * 7 + 3)
        return np.clip(img, 0, 1)
