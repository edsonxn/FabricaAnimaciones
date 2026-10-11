# -*- coding: utf-8 -*-
"""El tesoro perdido de Moctezuma — motion graphics animados cuadro a cuadro (estilo Kurzgesagt sobre el Lienzo).
Cada escena del guion es una animación distinta que muestra lo que dice la voz: mapas que se dibujan, columnas en fuga, cortes de sección,
personajes que caminan, infografías. El texto va dibujado dentro de la escena (nítido, sin filtro de desenfoque por encima)."""
import numpy as np

from escena_base import Escena, TL
from motor import W, H, componer, prog, smooth, Lienzo
import docu_fx as X
from reg import SHOTS, SND

import s_a  # noqa: F401  (cada módulo registra sus tomas y efectos de sonido)
import s_b  # noqa: F401
import s_c  # noqa: F401
import s_d  # noqa: F401
import s_e  # noqa: F401

TOTAL = TL["total"]
BG0 = np.zeros((H, W, 3), np.float32)


def _construir():
    SHOTS.sort(key=lambda d: d["t0"])
    for k, d in enumerate(SHOTS):
        d["t1"] = SHOTS[k + 1]["t0"] if k + 1 < len(SHOTS) else TOTAL + 1.0


_construir()


def _toma(lz, d, t):
    lz.nuevo(t, wob=0.0)
    bg = d["bg"](t) if callable(d["bg"]) else (d["bg"] if d["bg"] is not None else BG0)
    d["dib"](lz, t)
    img = componer(bg, lz.resolver(), boil=lz.boil)
    for p in d["post"]:
        img = p(img, t)
    return img


def render_mundo(lz, t):
    i = 0
    for k, d in enumerate(SHOTS):
        if d["t0"] <= t:
            i = k
    d = SHOTS[i]
    img = _toma(lz, d, t)
    tipo, dur = d["ent"]
    if i > 0 and t < d["t0"] + dur and tipo != "corte":
        A = _toma(lz, SHOTS[i - 1], t)
        img = X.mezcla2(A, img, (t - d["t0"]) / dur, tipo, i)
    img = img * smooth(prog(t, 0.0, 0.6))
    return np.clip(img, 0, 1).astype(np.float32)


class Mundo(Escena):
    def preparar(self):
        if self.idx == 0:
            for t, n, v, kw in SND:
                self.ev(t, n, v, **kw)

    def render(self, lz, t):
        return render_mundo(lz, t)


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
