# -*- coding: utf-8 -*-
"""Capítulo `patio`: el beneficio de patio (mineral molido + sal + mercurio pisado por mulas)."""
import math

import numpy as np

import locales as L
import subsuelo as S
import ui_vox as U
import vox as V
from cap_local import FIG, MUL, SUR
from ctx import T, INI, FIN
from motor import W, H, prog, e_out, e_back, e_inout, smooth, clamp01, h01, lerp, rect_red

PX, PY = -830.0, 44.0          # centro del patio (local)
RX, RY = 340.0, 118.0
A = dict(
    ini=INI("patio"), fin=FIN("patio"),
    cincuenta=T("patio", "cincuenta"), siete=T("patio", "siete"), truco=T("patio", "truco"),
    benef=T("patio", "beneficio"), patio=T("patio", "patio"),
    muele=T("patio", "muele"), mineral=T("patio", "mineral", frase=1), mezcla=T("patio", "mezcla"), sal=T("patio", "sal"),
    mercurio=T("patio", "mercurio", frase=1), mulas=T("patio", "mulas"), pisan=T("patio", "pisan"),
    semanas=T("patio", "semanas"),
    atrapa=T("patio", "atrapa"), plata=T("patio", "plata", frase=2), saca=T("patio", "saca"), pobre=T("patio", "pobre"),
    espana=T("patio", "España"), sin=T("patio", "sin"),
)


def mulas_patio(lz, t, n=6):
    """Mulas que dan vueltas pisando la mezcla (perspectiva 3/4)."""
    if t < A["mulas"] - 0.6:
        return
    k = smooth(prog(t, A["mulas"] - 0.6, A["mulas"] + 0.4))
    om = 0.30
    lst = []
    for i in range(n):
        th = om * (t - A["mulas"]) + i * (2 * math.pi / n)
        x = PX + RX * 0.78 * math.cos(th)
        y = PY + RY * 0.74 * math.sin(th) + 42
        dir_ = 1 if -math.sin(th) > 0 else -1
        prof = 0.86 + 0.2 * (math.sin(th) + 1) / 2
        lst.append((y, x, dir_, prof, i))
    for y, x, dir_, prof, i in sorted(lst):
        f = V.cuadro(V.CAMINAR, t + i * 0.13, 15.0)
        # arrastran una entrada suave (k)
        V.mula(lz, x, y, MUL * prof, f, dir_, "agua" if False else None, seed=40 + i, alfa=k)


def dibujar(lz, t, tc, cam_l):
    tp = t
    mezcla = clamp01(prog(t, A["mezcla"], A["mercurio"] + 1.2))
    S.patio(lz, PX, PY, RX, RY, t, mezcla_prog=mezcla)
    # montones de mineral (llegan con las mulas de la mina), sal y mercurio
    for i, x in enumerate((-1120, -1080, -1040)):
        k = e_back(prog(t, A["muele"] - 0.6 + i * 0.15, A["muele"] - 0.2 + i * 0.15))
        if k > 0.01:
            S.mineral(lz, x, PY + 40 + 30 * i, 1.4 * k, seed=i, plata=(i == 1))
    for i, x in enumerate((-570, -540)):
        k = e_back(prog(t, A["sal"], A["sal"] + 0.35))
        if k > 0.01:
            S.monton_sal(lz, x, PY + 30 + 40 * i, 1.2 * k)
    # frasco de mercurio (azogue)
    km = e_back(prog(t, A["mercurio"], A["mercurio"] + 0.35))
    if km > 0.01:
        with lz.grupo(-630, PY + 100, km):
            lz.relleno(V.elipse_pts(0, -30, 26, 30), V.PLATA, temblor=0.0, capa=1)
            lz.relleno(rect_red(-10, -74, 20, 22, 4), (120, 90, 64), temblor=0.0, capa=1)
            lz.relleno(V.elipse_pts(-8, -38, 8, 12), V.aclarar(V.PLATA, 0.7), temblor=0.0, capa=1)
    # peones con pala
    V.figura(lz, -1180, PY + 100, FIG, V.IDLE[int(t * 2.2) % 2], "indigena", 1, seed=50)
    V.figura(lz, -470, PY + 90, FIG, V.IDLE[int(t * 2.2 + 1) % 2], "africano", -1, seed=51)
    mulas_patio(lz, t)
    # pila de plata final (piña)
    pina = e_back(prog(t, A["atrapa"] + 0.6, A["atrapa"] + 1.4))
    if pina > 0.01:
        with lz.grupo(PX, PY - 8, 1.0):
            lz.relleno(V.elipse_pts(0, -30 * pina, 40 * pina, 34 * pina), V.PLATA, temblor=0.0, capa=1)
            lz.relleno(V.elipse_pts(-10 * pina, -40 * pina, 17 * pina, 12 * pina), V.aclarar(V.PLATA, 0.7), temblor=0.0, capa=1)
            L.chispa(lz, 26 * pina, -58 * pina, 20 * pina, t, capa=2)
