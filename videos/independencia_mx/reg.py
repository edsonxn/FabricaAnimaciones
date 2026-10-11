# -*- coding: utf-8 -*-
"""Registro de tomas y efectos de sonido de las escenas animadas."""
SHOTS = []
SND = []


def shot(t0, bg=None, post=(), ent=("fundido", 0.5)):
    """Decorador: registra la función de dibujo `fn(lz, t)` como una toma que empieza en t0 (s)."""
    def deco(fn):
        SHOTS.append(dict(t0=t0, dib=fn, bg=bg, post=list(post), ent=ent, nombre=fn.__name__))
        return fn
    return deco


def snd(t, nombre, vol=0.5, **kw):
    SND.append((t, nombre, vol, kw))
