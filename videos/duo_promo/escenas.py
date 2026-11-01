# -*- coding: utf-8 -*-
"""Anuncio de Dúo — vertical, interfaz de la app dibujada por código (kit duo.py).
Todas las escenas del guion usan `Mundo`, que dibuja el cuadro completo en función del tiempo global (plano secuencia):
  esc_1.py: gancho (plática) -> logo -> teléfono de Ana (misiones, barra) -> teléfono de Leo (ciclo, detalle)
  esc_2.py: cuestionario -> «Creando sus misiones…» -> cierre con logo y link
Los sonidos (SFX de ElevenLabs) NO pasan por `ev`: los ancla `fx_audio.py` a las mismas palabras y los deja en audio/fx.wav."""
import esc_1 as E1
import esc_2 as E2
from duo import TOTAL, P, acabado, fondo_duo, golpe, pr, smooth
from escena_base import Escena


def cuadro(t):
    p = P()
    cam = E1.camara(t)
    fondo_duo(p, t, dx=-(cam.cx - 540) * 0.30, dy=-(cam.cy - 960) * 0.25, calida=smooth(pr(t, E2.T_CI - 0.4, E2.T_CI + 0.6)))
    E1.intro(p, t)
    E1.telefonos(p, t)
    E1.frente(p, t)
    E2.ajusta(p, t)
    E2.cierre(p, t)
    flash = 0.10 * golpe(t, E1.a_duo, 0.45) + 0.06 * golpe(t, E1.b_sub, 0.4) + 0.08 * golpe(t, E2.c_duo - 0.1, 0.45)
    img = acabado(p.im, t, flash=flash, sacudida=0.5 * golpe(t, E1.b_sub, 0.35))
    img *= smooth(pr(t, 0.0, 0.3))
    img *= 1.0 - smooth(pr(t, TOTAL - 0.35, TOTAL))
    return img


class Mundo(Escena):
    def render(self, lz, t):
        return cuadro(t)


from escena_base import TL  # noqa: E402

CLASES = {e["id"]: Mundo for e in TL["escenas"]}
