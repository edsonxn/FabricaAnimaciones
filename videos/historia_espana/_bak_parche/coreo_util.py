# -*- coding: utf-8 -*-
"""Atajos de coreografía para «La historia de España»: actores en el mapa o en pantalla, caminantes, títulos y lugares.
Reglas de composición (para no chocar): el contador de años vive arriba a la izquierda (x < 520, y < 120); la fila de sellos arriba a la
derecha (x > 1150, y < 110) y el sello grande se estampa en (1690, 300) con su nombre debajo durante 2,2 s; los títulos van arriba al
centro (y ≈ 200); los personajes de pantalla, en la mitad inferior."""
import math

import mapa as M
from motor import e_back, e_in, e_inout, e_out, lerp, prog

COL = M.COL
CI = M.CIUDADES


def ga(R, dib, geo, t0, t1=None, s=0.5, off=(0, 0), entra="pop", sale="encoger", sem=0, z=1, zs=0.5, snd=("pop", 0.5), flip=False, d_in=0.45,
       extra=(), d_out=0.4, **kw):
    """Actor anclado a un lugar del mapa (lon, lat)."""
    sfx = ([(0, snd[0], snd[1])] if snd else []) + list(extra)
    return R.act(dib, geo=geo, off=off, s=s, t_in=t0, d_in=d_in, entra=entra, sem=sem, sfx=sfx, t_out=t1, sale=sale, zs=zs, z=z, flip=flip, d_out=d_out, **kw)


def pa(R, dib, x, y, s, t0, t1=None, entra="pop", sale="encoger", sem=0, z=2, snd=("pop", 0.55), flip=False, d_in=0.45, extra=(), d_out=0.4, **kw):
    """Actor fijo en la pantalla (x, y, escala) o con posición función de t."""
    sfx = ([(0, snd[0], snd[1])] if snd else []) + list(extra)
    pos = (lambda t: (x(t), y(t), s)) if callable(x) else (x, y, s)
    return R.act(dib, pos=pos, t_in=t0, d_in=d_in, entra=entra, sem=sem, sfx=sfx, t_out=t1, sale=sale, z=z, flip=flip, d_out=d_out, **kw)


def andar(R, fn, P, t0, dur, t1=None, s=0.45, sem=0, z=1, zs=0.5, fps=7, flip=None, off=(0, 0), entra="pop", snd=("pop", 0.4), ease=e_inout, extra=()):
    """Actor que recorre el camino geográfico P (cambia de pose al andar/galopar). flip=None: mira hacia donde va (según el primer tramo)."""
    if flip is None:
        a, b = P[0], P[min(len(P) - 1, 1)]
        flip = float(M.U(b[0])) < float(M.U(a[0]))
    return R.act(lambda t, f=fn, k=sem: f(int(t * fps + k) % 4), pos_geo=R.camino_pos(P, t0, dur, ease=ease), off=off, s=s, t_in=t0, d_in=0.4, entra=entra,
                 sem=sem, sfx=([(0, snd[0], snd[1])] if snd else []) + list(extra), t_out=t1, sale="encoger", zs=zs, z=z, flip=flip)


def titulo(R, t0, t1, txt, y=196, px=80, x=960, d=None, snd=True):
    """Rótulo grande arriba al centro."""
    if snd:
        R.snd(t0, "escribir", 0.45, dur=min(1.2, 0.08 * len(txt)))
    return R.texto(t0, t1, txt, (x, y), px=px, d=d if d is not None else min(1.1, 0.06 * len(txt) + 0.3))


def lugar(R, t0, t1, txt, geo, off=(0, -70), px=48, d=0.45):
    return R.texto(t0, t1, txt, None, px=px, d=d, geo=geo, off=off)


def ciudad(R, t0, t1, clave, txt=None, lado="arriba", px=44):
    R.ciudad(t0, t1, clave, CI[clave], txt, lado, px)


def mece(a=6.0, w=2.2, ph=0.0):
    """Desplazamiento vertical suave (flotar sobre el agua, respirar)."""
    return lambda t: (0, a * math.sin(t * w + ph))
