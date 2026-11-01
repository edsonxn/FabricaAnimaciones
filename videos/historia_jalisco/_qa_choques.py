# -*- coding: utf-8 -*-
"""Control de choques: python _qa_choques.py [paso]
Cada `paso` s mira las cajas de todos los rótulos visibles (R.cajas) y avisa si un rótulo
  - se sale del cuadro, - pisa a otro rótulo, - pisa el contador de años, la fila de sellos o el sello grande que se estampa,
  - pisa a un personaje/objeto (caja aproximada del dibujo).
Agrupa los avisos por tramo para que se lean de un vistazo."""
import sys

import numpy as np

import escenas as E
import mapa as M
from motor import H, W

R = E.R
PASO = float(sys.argv[1]) if len(sys.argv) > 1 else 0.2


def inter(a, b, margen=4):
    return not (a[2] <= b[0] + margen or b[2] <= a[0] + margen or a[3] <= b[1] + margen or b[3] <= a[1] + margen)


def area_inter(a, b):
    return max(0, min(a[2], b[2]) - max(a[0], b[0])) * max(0, min(a[3], b[3]) - max(a[1], b[1]))


_cache = {}


def caja_dib(d):
    k = id(d)
    if k not in _cache and not hasattr(d, "ops"):          # pegatina de Flow (pegflow.Peg): pies en (0, 0), alto = d.alto
        import pegflow
        rgb, a = pegflow._cargar(d.ruta)
        w = d.alto * a.shape[1] / a.shape[0]
        _cache[k] = (-w / 2, -d.alto, w / 2, 0.0)
    if k not in _cache:
        P = np.vstack([op[1] for op in d.ops])
        _cache[k] = (P[:, 0].min(), P[:, 1].min(), P[:, 0].max(), P[:, 1].max())
    return _cache[k]


def caja_actor(a, t, cam):
    if t < a.t_in + a.d_in or (a.tfin is not None and t >= a.tfin) or (a.t_out is not None and t > a.t_out):
        return None
    x, y, s, rot = a.estado(t, cam)
    d = a.dib(t) if callable(a.dib) else a.dib
    x0, y0, x1, y1 = caja_dib(d)
    if a.flip:
        x0, x1 = -x1, -x0
    return (x + x0 * s, y + y0 * s, x + x1 * s, y + y1 * s)


def zonas_fijas(t):
    z = []
    if R.anios and t >= R.anios[0][0]:
        z.append(("contador de años", (30, 18, 470, 112)))
    n = len(E.SELLOS)
    for k, s in enumerate(E.SELLOS):
        a = t - s["t"]
        if a < 0:
            continue
        if a < 2.6:
            z.append(("sello grande", (E.SX - 125, E.SY - 125, E.SX + 125, E.SY + 175)))
        else:
            x = 1868 - E.PASO_SELLO * (n - 1 - k)
            z.append(("fila de sellos", (x - 40, 20, x + 40, 104)))
    return z


avisos = []
ts = np.arange(0.0, E.TOTAL, PASO)
for t in ts:
    w = R.peso_am(t)
    st = E.estado_cam(t, w)
    M.usar("mx")
    cam = M.Cam(*st)
    cajas = [(f(t, cam), txt) for (t0, t1, f, txt) in R.cajas if t0 <= t <= t1]
    for i, (c, txt) in enumerate(cajas):
        if c[0] < 8 or c[1] < 8 or c[2] > W - 8 or c[3] > H - 8:
            avisos.append((t, "FUERA", txt, ""))
        for c2, txt2 in cajas[i + 1:]:
            if inter(c, c2):
                avisos.append((t, "TEXTO/TEXTO", txt, txt2))
        for nombre, z in zonas_fijas(t):
            if inter(c, z):
                avisos.append((t, "TEXTO/" + nombre.upper(), txt, ""))
        for a in E.ACTORES:
            ca = caja_actor(a, t, cam)
            if ca is None:
                continue
            ai = area_inter(c, ca)
            if ai > 0.25 * (c[2] - c[0]) * (c[3] - c[1]):
                avisos.append((t, "TEXTO/DIBUJO", txt, f"sem={a.sem}"))
    for a in E.ACTORES:                                                    # dibujos contra la fila de sellos / contador
        ca = caja_actor(a, t, cam)
        if ca is None:
            continue
        for nombre, z in zonas_fijas(t):
            if area_inter(ca, z) > 1500:
                avisos.append((t, "DIBUJO/" + nombre.upper(), f"sem={a.sem}", ""))

# agrupar avisos consecutivos iguales
grupos = {}
for t, tipo, a, b in avisos:
    k = (tipo, a, b)
    grupos.setdefault(k, []).append(t)
filas = []
for (tipo, a, b), tt in grupos.items():
    tt = sorted(tt)
    ini = tt[0]
    prev = tt[0]
    for x in tt[1:] + [1e9]:
        if x - prev > PASO * 1.5:
            filas.append((ini, prev, tipo, a, b))
            ini = x
        prev = x
for ini, fin, tipo, a, b in sorted(filas):
    print(f"{ini:7.2f}-{fin:7.2f}  {tipo:26s} {a[:40]:40s} {b}")
print(len(filas), "tramos con avisos")
