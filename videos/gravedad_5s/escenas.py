# -*- coding: utf-8 -*-
"""¿Qué pasaría si la GRAVEDAD desapareciera 5 segundos? — Kuriox, PLANO SECUENCIA estilo Kurzgesagt (sin cortes).

Las 6 escenas del guion comparten la clase Mundo, que dibuja un mundo continuo en función del tiempo global t:
parque + casa en corte + avenida + costa -> zoom a la Tierra en el espacio (intro) -> vuelta al paisaje para la Versión A
(casa, parque con árbol de 5 m, avenida y costa con burbujas flotantes, caída en Segundo 5) -> zoom al espacio para la
Versión B (interior terrestre y lava, Tierra y Luna saliendo por la tangente, Sol que se hincha y se apaga, desplome en
Segundo 5, malla de espacio-tiempo) -> vuelta al parque para el cierre."""
import math

import numpy as np

from escena_base import Escena, TL
from motor import W, H, componer, prog, smooth, circulo
from anclas import TOTAL
from estado import estado
import camara as C
import mundo_paisaje as MP
import mundo_espacio as ME
import ui as U


def _paisaje(lz, t, S, est, rel=1.0):
    MP.dibujar(lz, t, S, est, rel)
    return MP.cielo(t, est)


def _tapa_planeta(lz, S, ex, ey, rs):
    """Durante el zoom paisaje <-> planeta: tapa el corte del subsuelo y dibuja el continente como casquete verde."""
    a = (1 - prog(math.log(rs), math.log(14000), math.log(70000))) * prog(rs, 700, 2600)
    if a <= 0.01:
        return
    n = int(min(2400, max(240, rs / 6)))
    lz.relleno(circulo(ex, ey, rs * 1.0005, n), (52, 124, 214), alfa=a)
    X = np.linspace(-4600.0, MP.X_COSTA + 60, 140)
    phis = S.k * (X - S.X0) / rs
    u = (X - X[0]) / (X[-1] - X[0])
    dmax = min(rs * 0.12, 1100 * S.k)
    prof = dmax * np.sin(np.pi * u) ** 0.7 * (1 + 0.12 * np.sin(u * 23) + 0.08 * np.sin(u * 51))
    ext = np.stack([ex + rs * np.sin(phis), ey - rs * np.cos(phis)], 1)
    inn = np.stack([ex + (rs - prof) * np.sin(phis), ey - (rs - prof) * np.cos(phis)], 1)[::-1]
    lz.relleno(np.concatenate([ext, inn]), (96, 176, 112), alfa=a)
    inn2 = np.stack([ex + (rs - prof * 0.55) * np.sin(phis), ey - (rs - prof * 0.55) * np.cos(phis)], 1)[::-1]
    lz.relleno(np.concatenate([ext * 0 + inn2[::-1], inn]), (78, 150, 100), alfa=0.5 * a)


def render_mundo(lz, t):
    lz.nuevo(t, wob=0.0)
    est = estado(t)
    m = C.modo(t)
    nombre = m if isinstance(m, str) else m[0]
    ctx = dict(modo=nombre, S=None, tierra=None)
    if nombre == "paisaje":
        S = C.cam_paisaje(t)
        ctx["S"] = S
        bg = _paisaje(lz, t, S, est)
    elif nombre == "espacio":
        ex, ey, r = C.cam_espacio(t)
        ctx["tierra"] = (ex, ey, r)
        bg = ME.fondo(t, ex, ey)
        ME.dibujar(lz, t, ex, ey, r)
    else:   # z_salida | z_entrada
        Z = m[1]
        S, (ex, ey, rs), s = C.zoom_global(t, Z, nombre == "z_salida")
        ctx["tierra"] = (ex, ey, rs)
        bg_e = ME.fondo(t, ex, ey)
        bg_c = MP.cielo(t, est)
        bg = bg_e * (1 - s) + bg_c * s
        if rs < 3200:
            with lz.grupo(ex, ey, 1.0, 1.1 * prog(math.log(rs), math.log(350), math.log(3200))):
                ME.tierra(lz, t, 0.0, 0.0, rs, extra=rs < 2000)
        if rs > 800:
            rel = prog(math.log(rs), math.log(3000), math.log(40000))
            ctx["S"] = S
            MP.dibujar(lz, t, S, est, rel, sin_gente=rs < 4000, tapa=lambda: _tapa_planeta(lz, S, ex, ey, rs),
                       delgado=rs < 20000)
    U.dibujar(lz, t, ctx, est)
    img = componer(bg, lz.resolver(), boil=lz.boil)
    img = U.post(img, t, ctx, est)
    negro = prog(t, TOTAL - 0.9, TOTAL - 0.05)
    if negro > 0:
        img = img * (1 - smooth(negro))
    return np.clip(img, 0, 1)


def registrar_sfx(e):
    import sonido
    sonido.registrar(e)


class Mundo(Escena):
    """Plano secuencia: todas las escenas del guion comparten este mismo mundo continuo."""

    def preparar(self):
        if self.idx == 0:
            registrar_sfx(self)

    def render(self, lz, t):
        return render_mundo(lz, t)


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
