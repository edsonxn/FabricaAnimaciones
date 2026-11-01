# -*- coding: utf-8 -*-
"""¿Qué pasaría si el OXÍGENO desapareciera 5 segundos? — Kuriox, PLANO SECUENCIA estilo Kurzgesagt (sin cortes).

Las 13 «escenas» del guion solo marcan narración y música: todas usan la clase Mundo, que dibuja un mundo continuo en
función del tiempo global t. El paisaje (parque, pueblo, central, costa y mar en corte) se aleja hasta ser la Tierra en el
espacio (intro y reglas), vuelve a bajar para la versión A, entra en el cuerpo por el pecho de la protagonista y sale por
su cabeza, se deshace en la versión B, vuelve a ser planeta (realidad) y baja al parque para el cierre.
Módulos: mundo_comun (Sup, claves), anclas, estado, camara, mundo_paisaje, gente, mundo_espacio, mundo_cuerpo, ui,
kit_oxi y kit_bio (utilería propia)."""
import math

import numpy as np

from escena_base import Escena, TL
from motor import W, H, componer, prog, e_in, e_out, e_inout, smooth, circulo, lerp
from anclas import A, TOTAL, Z1, Z2, Z3, Z4, PORTAL_IN, PORTAL_OUT
from estado import estado
import camara as C
import mundo_paisaje as MP
import mundo_espacio as ME
import mundo_cuerpo as MC
import ui as U
import gente as G


def _paisaje(lz, t, S, est, rel=1.0):
    MP.dibujar(lz, t, S, est, rel)
    return MP.cielo(t, est)


def _tapa_planeta(lz, S, ex, ey, rs):
    """Durante el zoom: el planeta tapa el corte del subsuelo; la tierra firme del paisaje es un continente verde."""
    a = (1 - prog(math.log(rs), math.log(14000), math.log(70000))) * prog(rs, 700, 2600)
    if a <= 0.01:
        return
    n = int(min(2400, max(240, rs / 6)))
    lz.relleno(circulo(ex, ey, rs * 1.0005, n), (52, 124, 214), alfa=a)
    # continente: casquete con forma de lente bajo la tierra firme del paisaje (de la montaña a la costa)
    X = np.linspace(-6200.0, MP.X_COSTA + 60, 140)
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
    elif nombre in ("z_salida", "z_entrada"):
        Z = m[1]
        S, (ex, ey, rs), s = C.zoom_global(t, Z, nombre == "z_salida")
        ctx["tierra"] = (ex, ey, rs)
        bg_e = ME.fondo(t, ex, ey)
        bg_c = MP.cielo(t, est)
        bg = bg_e * (1 - s) + bg_c * s
        if rs < 3200:   # la Tierra gira un poco para que el casquete polar no quede en el borde de arriba
            with lz.grupo(ex, ey, 1.0, 1.1 * prog(math.log(rs), math.log(350), math.log(3200))):
                ME.tierra(lz, t, 0.0, 0.0, rs, extra=rs < 2000)
        if rs > 800:
            rel = prog(math.log(rs), math.log(3000), math.log(40000))
            ctx["S"] = S
            MP.dibujar(lz, t, S, est, rel, sin_gente=rs < 4000, tapa=lambda: _tapa_planeta(lz, S, ex, ey, rs),
                       delgado=rs < 20000)
    elif nombre in ("portal_in", "portal_out"):
        S = C.cam_paisaje(t)
        ctx["S"] = S
        bg = _paisaje(lz, t, S, est)
        bg = MC.portal(lz, t, S, bg, entrada=nombre == "portal_in")
    else:   # cuerpo
        bg = MC.dibujar(lz, t)
    U.dibujar(lz, t, ctx, est)
    img = componer(bg, lz.resolver(), boil=lz.boil)
    img = U.post(img, t, ctx, est)
    negro = prog(t, TOTAL - 0.9, TOTAL - 0.05)
    if negro > 0:
        img = img * (1 - smooth(negro))
    return np.clip(img, 0, 1)


# ======================================================================== sonido
def registrar_sfx(e):
    import sonido
    sonido.registrar(e)


class Mundo(Escena):
    """Plano secuencia: todas las escenas del guion comparten este mismo mundo continuo."""

    def preparar(self):
        if self.idx == 0:        # los efectos se registran una sola vez
            registrar_sfx(self)

    def render(self, lz, t):
        return render_mundo(lz, t)


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
