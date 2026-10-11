# -*- coding: utf-8 -*-
"""«Juchipila: el lugar de las flores nobles» — motion graphics animados cuadro a cuadro (estilo Kurzgesagt sobre el Lienzo).
Cada escena del guion son varias tomas (mapa, vistas laterales, gráficos) ancladas a la voz; aquí solo el ensamblado."""
import numpy as np

from escena_base import Escena, TL
from motor import W, H, componer, prog, smooth, Lienzo
import docu_fx as X
import kz_ui as U_
from reg import SHOTS, SND

import t01  # noqa: F401
import t02  # noqa: F401
import t03  # noqa: F401
import t04  # noqa: F401
import t05  # noqa: F401
import t06  # noqa: F401
import t07  # noqa: F401
import t08  # noqa: F401
import t09  # noqa: F401
import t10  # noqa: F401
import t11  # noqa: F401
import t12  # noqa: F401
import t13  # noqa: F401

TOTAL = TL["total"]
BG0 = np.zeros((H, W, 3), np.float32)


def _construir():
    SHOTS.sort(key=lambda d: d["t0"])
    for k, d in enumerate(SHOTS):
        d["t1"] = SHOTS[k + 1]["t0"] if k + 1 < len(SHOTS) else TOTAL + 1.0


_construir()


def _toma(lz, d, t):
    lz.nuevo(t, wob=0.0)
    lz.diferir = True                  # las etiquetas sin cola se dibujan al final del cuadro, sin encimarse con la fecha de la esquina ni entre sí
    bg = d["bg"](t) if callable(d["bg"]) else (d["bg"] if d["bg"] is not None else BG0)
    d["dib"](lz, t)
    U_.vaciar_diferidos(lz)
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
            # los snd() viven dentro de las funciones de dibujo: se dibuja cada toma una vez para registrarlos (sin repetir)
            import __main__
            if not SND and getattr(getattr(__main__, "__spec__", None), "name", "") == "sfx":     # solo en la etapa sfx, no en el render
                lz = Lienzo()
                for d in SHOTS:
                    lz.nuevo(d["t0"] + 0.05, wob=0.0)
                    d["dib"](lz, d["t0"] + 0.05)
            vistos = set()
            for t, n, v, kw in SND:
                clave = (round(t, 3), n)
                if clave in vistos:
                    continue
                vistos.add(clave)
                self.ev(t, n, v, **kw)

    def render(self, lz, t):
        return render_mundo(lz, t)


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
