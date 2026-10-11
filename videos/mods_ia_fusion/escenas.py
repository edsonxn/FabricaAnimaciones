# -*- coding: utf-8 -*-
"""Dos formas de fusionar videojuegos con IA — vertical, estilo «rayos X tecno» (kit pix.py + comp.py).
Todas las escenas del guion usan `Mundo`, que dibuja el cuadro completo en función del tiempo global (planos secuencia):
  esc_a.py: gancho -> puente -> límite        esc_b.py: reescribir -> verdad -> cierre
Los sonidos (SFX de ElevenLabs) NO pasan por `ev`: los ancla `fx_audio.py` a las mismas palabras y los deja en audio/fx.wav."""
import numpy as np

import esc_a as A
from escena_base import Escena
from pix import TOTAL, P, acabado, fondo_tecno, pr, smooth, CIAN, MAGENTA, ROJO, AMAR, VERDE, LILA

try:
    import esc_b as B
except ImportError:                      # mientras se escribe la segunda mitad
    B = None

TONOS = dict(gancho=(CIAN, MAGENTA), puente=(CIAN, LILA), limite=(ROJO, MAGENTA), reescribir=(MAGENTA, AMAR), verdad=(AMAR, CIAN),
             cierre=(VERDE, MAGENTA))


def cuadro(t):
    p = P()
    if t < A.T_PUENTE:
        fondo_tecno(p, t, *TONOS["gancho"])
        fx = A.gancho(p, t)
    elif t < A.T_FIN_A:
        fondo_tecno(p, t, *TONOS["limite" if t >= A.T_LIMITE + 0.6 else "puente"])
        fx = A.puente(p, t)
    elif B is not None:
        fx = B.cuadro(p, t)
    else:
        fondo_tecno(p, t)
        fx = {}
    img = acabado(p.im, t, fx.get("golpe", 0.0), fx.get("glitch", 0.0), fx.get("flash", 0.0))
    img *= smooth(pr(t, 0.0, 0.25))
    img *= 1.0 - smooth(pr(t, TOTAL - 0.7, TOTAL - 0.05))
    return img


class Mundo(Escena):
    def render(self, lz, t):
        return cuadro(t)


from escena_base import TL  # noqa: E402

CLASES = {e["id"]: Mundo for e in TL["escenas"]}
