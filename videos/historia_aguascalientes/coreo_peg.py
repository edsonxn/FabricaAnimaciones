# -*- coding: utf-8 -*-
"""Atajos de coreografía con PEGATINAS DE FLOW (historia_aguascalientes; kit de historia_jalisco): piezas por hoja y caminantes con ciclo real de Flow."""
import numpy as np

import mapa as M
from coreo_util import formacion
from motor import e_inout
from pegflow import P, Peg, ciclo  # noqa: F401  (los coreo_N los reimportan de aquí si quieren)

# Atajos de hojas: cada coreo_N.py define los suyos (historia_aguascalientes, 22-oct-2026). Aquí solo los ayudantes de ciclos.


def andar_ciclo(R, frames, P_, t0, dur, t1=None, s=0.4, sem=0, z=1, zs=0.4, fps=9.0, flip=None, off=(0, 0), entra="pop", ease=e_inout,
                extra=(), sale="encoger"):
    """Caminante con el ciclo de Flow sobre el camino geográfico P_ (los cuadros miran a la derecha; flip si va al oeste)."""
    if flip is None:
        a, b = P_[0], P_[-1]
        flip = float(b[0]) < float(a[0])
    n = len(frames)
    return R.act(lambda t, k=sem: frames[int(t * fps + k * 3) % n], pos_geo=R.camino_pos(P_, t0, dur, ease=ease), off=off, s=s, t_in=t0,
                 d_in=0.4, entra=entra, sem=sem, sfx=list(extra), t_out=t1, sale=sale, zs=zs, z=z, flip=flip)


def grupo_ciclo(R, frames, P_, t0, dur, n=3, ancho=90, t1=None, s=0.4, sem=0, z=1, fps=9.0, desfase=0.12, flip=None, extra=()):
    return [andar_ciclo(R, frames, P_, t0 + desfase * k, dur, t1=t1, s=s, sem=sem + k, z=z, fps=fps, off=formacion(k, n, ancho), flip=flip,
                        extra=extra if k == 0 else ()) for k in range(n)]


def ciclo_pant(R, frames, x0, x1, y, t0, dur, t1=None, s=0.9, sem=0, z=3, fps=9.0):
    """Ciclo que cruza la pantalla (coordenadas de pantalla)."""
    n = len(frames)

    def pos(t):
        u = min(1.0, max(0.0, (t - t0) / dur))
        return (x0 + (x1 - x0) * u, y, s)
    return R.act(lambda t, k=sem: frames[int(t * fps + k * 3) % n], pos=pos, t_in=t0, d_in=0.3, entra="pop", sem=sem, t_out=t1, z=z,
                 flip=x1 < x0)
