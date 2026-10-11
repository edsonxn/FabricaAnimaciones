# -*- coding: utf-8 -*-
"""Utilidades de coreografía del tablero: cámara (K, KP, DENTRO), textos con ventana de tiempo (TX), sellos/taches sobre piezas,
crédito automático de fotos de Commons."""
import json
import math
import os

import numpy as np

import tablero as T
from kit import (INI, FIN, ww, we, pk, R, S, N, Q, TAG, CRED, snd, TOTAL, W, H)  # noqa: F401

C = T.CAM
TXT = []           # (t0, t1, fn, sombra)


def TX(fn, t0, t1, sombra=True):
    TXT.append((t0, t1, fn, sombra))


def K(t, x, y, z=1.2, rz=0.0, rx=0.0, ry=0.0, modo="fluido"):
    C.clave(t, x, y, z, rz, rx, ry, modo)


def KP(t, pz, z=1.3, dx=0.0, dy=0.0, rz=None, rx=0.0, ry=0.0, modo="fluido"):
    K(t, pz.x + dx, pz.y + dy, z, pz.rot * 0.7 if rz is None else rz, rx, ry, modo)


def DENTRO(pz, t_a, t_b, t_c, z_a=1.7, rx=4.0, ry=-5.0, sonido=True):
    """Entra en el portal de la pieza: t_a mirándola, t_b ya dentro (llena la pantalla), t_c sigue dentro."""
    cx, cy = T.centro_ventana(pz)
    zf = T.zoom_lleno(pz)
    K(t_a, cx, cy, z_a, pz.rot * 0.6, rx, ry)
    K(t_b, cx, cy, zf, pz.rot, 0, 0, modo="suave")
    K(t_c, cx, cy, zf * 1.05, pz.rot, 0, 0, modo="suave")
    if sonido:
        snd(t_a + (t_b - t_a) * 0.3, "zoom_whoosh", 0.35, dur=min(0.9, t_b - t_a))


def LATIGO(t0, t1, x, y, z=1.1, rz=0.0, rx=0.0, ry=0.0):
    """Barrido rápido (con desenfoque) desde donde esté la cámara en t0 hasta (x, y) en t1."""
    bx, by, bz, brz, brx, bry = C.base(t0)
    C.K = [k for k in C.K if not (t0 - 1e-6 <= k["t"] <= t1 + 1e-6)]
    C.clave(t0, bx, by, bz, brz, brx, bry, "latigo")
    C.clave(t1, x, y, z, rz, rx, ry, "suave")
    snd(t0, "whoosh", 0.35, dur=max(0.3, min(0.7, t1 - t0)))


def sello_en(pz, txt, t0, dx=0.0, dy=0.0, rot=-9.0, px=64, color=(0.80, 0.07, 0.07), op=0.92):
    L = T.sello_lam(txt, px, tuple(color))
    snd(t0, "sello", 0.6)
    T.SACUDIDA.add(t0, 5.0)

    def f(lz, V, t, p):
        if t < t0:
            return
        u = T.e_out(T.pr(t, t0, t0 + 0.16))
        x, y = p.punto(dx, dy)
        z = p.pose(t)[2] - 3
        T.pegar3d(lz, V, L, x, y, z, (1.7 - 0.7 * u) * p.s, p.rot + rot, 0, 0, op * min(1.0, u * 2.5), 0)
    pz.marcas.append(f)


def tache(pz, t0, dur=0.5, color=(0.86, 0.06, 0.06), grosor=16):
    w, h = pz.L.w * 0.42, pz.L.h * 0.42
    a, b = pz.punto(-w, -h), pz.punto(w, h)
    c, d = pz.punto(w, -h), pz.punto(-w, h)
    T.Marca([a, b], t0, dur * 0.5, color, grosor, z=-12)
    T.Marca([c, d], t0 + dur * 0.5, dur * 0.5, color, grosor, z=-12, sonido=False)


def circulo(pz, t0, dur=0.6, dx=0, dy=0, rx=None, ry=None, color=(0.86, 0.06, 0.06), grosor=9, seed=0):
    x, y = pz.punto(dx, dy)
    T.Marca(T.circulo_pts(x, y, rx or pz.L.w * pz.s * 0.62, ry or pz.L.h * pz.s * 0.62, seed=seed), t0, dur, color, grosor, z=-12)


def subraya(pz, t0, x0, x1, y, dur=0.4, color=(0.86, 0.06, 0.06), grosor=7):
    T.Marca([pz.punto(x0, y), pz.punto(x1, y)], t0, dur, color, grosor, z=-12)


def resalta(pz, t0, x0, x1, y, dur=0.35, grosor=34):
    T.Marca([pz.punto(x0, y), pz.punto(x1, y)], t0, dur, (1.0, 0.86, 0.10), grosor, z=-12, op=0.45, sonido=False)


_CR = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "imagenes", "creditos.json"), encoding="utf-8"))


def cred_foto(nombre):
    for k, v in _CR.items():
        if k.startswith(nombre + "."):
            autor = v["autor"].split("\n")[0][:60]
            lic = v["licencia"]
            return f"Foto: {autor} · Wikimedia Commons ({lic})" if lic not in ("Public domain",) else f"Foto: {autor} · Wikimedia Commons (dominio público)"
    return "Foto: Wikimedia Commons"


def FOTO_CRED(nombre, t0, t1):
    TX(CRED(cred_foto(nombre), t0, t1), t0, t1, sombra=False)


def rojo(a, b, t0, dur=0.9, color="rojo", **kw):
    return T.Hilo(a, b, t0, dur, color, **kw)
