# -*- coding: utf-8 -*-
"""Atajos de coreografía para «La historia de México en 5 minutos»: actores en el mapa o en pantalla, caminantes, formaciones, títulos y lugares."""
import math

import numpy as np

import mapa as M
from motor import e_back, e_in, e_inout, e_out, lerp, prog

COL = M.COL
CI = M.CIUDADES


def ga(R, dib, geo, t0, t1=None, s=0.5, off=(0, 0), entra="pop", sale="encoger", sem=0, z=1, zs=0.5, snd=None, flip=False, d_in=0.45,
       extra=(), d_out=0.4, **kw):
    """Actor anclado a un lugar del mapa (lon, lat)."""
    sfx = ([(0, snd[0], snd[1])] if snd else []) + list(extra)
    return R.act(dib, geo=geo, off=off, s=s, t_in=t0, d_in=d_in, entra=entra, sem=sem, sfx=sfx, t_out=t1, sale=sale, zs=zs, z=z, flip=flip, d_out=d_out, **kw)


def pa(R, dib, x, y, s, t0, t1=None, entra="pop", sale="encoger", sem=0, z=2, snd=None, flip=False, d_in=0.45, extra=(), d_out=0.4, **kw):
    """Actor fijo en la pantalla (x, y, escala) o con posición función de t."""
    sfx = ([(0, snd[0], snd[1])] if snd else []) + list(extra)
    pos = (lambda t: (x(t), y(t), s)) if callable(x) else (x, y, s)
    return R.act(dib, pos=pos, t_in=t0, d_in=d_in, entra=entra, sem=sem, sfx=sfx, t_out=t1, sale=sale, z=z, flip=flip, d_out=d_out, **kw)


def andar(R, fn, P, t0, dur, t1=None, s=0.45, sem=0, z=1, zs=0.5, fps=7, flip=None, off=(0, 0), entra="pop", snd=None, ease=e_inout, extra=()):
    """Actor que recorre el camino geográfico P (cambia de pose al andar/galopar)."""
    if flip is None:
        a, b = P[0], P[min(len(P) - 1, 1)]
        flip = float(M.U(b[0])) < float(M.U(a[0]))
    return R.act(lambda t, f=fn, k=sem: f(int(t * fps + k) % 4), pos_geo=R.camino_pos(P, t0, dur, ease=ease), off=off, s=s, t_in=t0, d_in=0.4, entra=entra,
                 sem=sem, sfx=([(0, snd[0], snd[1])] if snd else []) + list(extra), t_out=t1, sale="encoger", zs=zs, z=z, flip=flip)


def titulo(R, t0, t1, txt, y=196, px=80, x=960, d=None, snd=False):
    """Rótulo grande arriba al centro."""
    if snd:
        R.snd(t0, "escribir", 0.4, dur=min(1.2, 0.08 * len(txt)))
    return R.texto(t0, t1, txt, (x, y), px=px, d=d if d is not None else min(1.1, 0.06 * len(txt) + 0.3))


def lugar(R, t0, t1, txt, geo, off=(0, -70), px=48, d=0.45):
    return R.texto(t0, t1, txt, None, px=px, d=d, geo=geo, off=off)


def ciudad(R, t0, t1, clave, txt=None, lado="arriba", px=44):
    R.ciudad(t0, t1, clave, CI[clave], txt, lado, px)


def formacion(k, n, ancho):
    """Desplazamiento en px (dx, dy) de la figura k de un grupo de n que marcha junta."""
    return ((k - (n - 1) / 2) * ancho, (-1) ** k * 0.22 * ancho)


def mece(a=6.0, w=2.2, ph=0.0):
    return lambda t: (0, a * math.sin(t * w + ph))


def tramo(P, a, b, n=None):
    P = np.asarray(P, float)
    ia = int(np.argmin(np.hypot(P[:, 0] - a[0], P[:, 1] - a[1])))
    ib = int(np.argmin(np.hypot(P[:, 0] - b[0], P[:, 1] - b[1])))
    Q = P[ia:ib + 1] if ia <= ib else P[ib:ia + 1][::-1]
    if n and len(Q) > n:
        Q = Q[np.linspace(0, len(Q) - 1, n).round().astype(int)]
    return [tuple(q) for q in Q]


def grupo(R, fn, P, t0, dur, n=3, ancho=120, t1=None, s=0.45, sem=0, z=1, fps=7, desfase=0.0, ease=e_inout, snd=None, flip=None):
    out = []
    for k in range(n):
        out.append(andar(R, fn, P, t0 + desfase * k, dur, t1=t1, s=s, sem=sem + k, z=z, fps=fps, off=formacion(k, n, ancho), ease=ease,
                         snd=snd if k == 0 else None, flip=flip))
    return out
