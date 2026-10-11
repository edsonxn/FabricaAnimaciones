# -*- coding: utf-8 -*-
"""Utilería noir 5: auto de los años 40 (de lado, ruedas que giran, faros que alumbran) · velocímetro · mesa de póker con fichas."""
import math

import numpy as np

import noir as N
from motor import H, W, clamp01, e_inout, e_out, smooth
from noir import gris
from props import rect, rot
from toon import blob, elipse_, suave, tubo


def auto(h, x, y, s=1.0, t=0.0, vel=1.0, sem=0, tono=40, bandera=None, faros=1.0):
    """Sedán de los 40 de perfil mirando a la derecha; (x, y) = suelo bajo el centro. vel = vueltas de rueda (s^-1)."""
    def T(P):
        return np.asarray(P, float) * s + (x, y)
    cuerpo = suave([(-300, -40), (-300, -96), (-250, -120), (-150, -126), (-90, -196), (40, -204), (120, -140), (250, -128), (300, -96),
                    (306, -50), (280, -30), (-280, -30)], 4)
    h.pieza(T(cuerpo), tono, sem, w=6 * s, luz=(0.3, -1), d=14 * s, trama=0.45, rim=0.95, rim_tono=240)
    for P, k in (([(-70, -186), (20, -190), (20, -132), (-110, -132)], 1), ([(34, -186), (100, -138), (34, -134)], 2)):
        h.pieza(T(P), 175, sem + k, w=4 * s, luz=(0.3, -1), d=4, trama=0, rim=0.3)
    h.trazo(T([(-260, -90), (290, -86)]), 3 * s, sem + 3, color=gris(200), alfa=0.7)      # cromado
    for wx in (-190, 190):                                     # guardabarros y ruedas
        h.pieza(T(suave([(wx - 90, -60), (wx - 70, -110), (wx, -128), (wx + 70, -110), (wx + 90, -60)], 3)), tono - 12, sem + 5 + wx,
                w=5 * s, luz=(0.3, -1), d=8 * s, trama=0.3, rim=0.9)
        cx, cy = x + wx * s, y - 50 * s
        h.pieza(elipse_(cx, cy, 52 * s, 52 * s, n=28), 16, sem + 10 + wx, w=5 * s, luz=(0.3, -1), d=4, trama=0, rim=0.7)
        h.pieza(elipse_(cx, cy, 26 * s, 26 * s, n=20), 190, sem + 12 + wx, w=3 * s, luz=(0.3, -1), d=3, trama=0)
        a0 = t * vel * 2 * math.pi
        for k in range(5):
            a = a0 + k * 2 * math.pi / 5
            h.trazo(np.array([[cx, cy], [cx + math.cos(a) * 24 * s, cy + math.sin(a) * 24 * s]]), 3 * s, sem + 20 + k, color=gris(60))
    fx, fy = x + 296 * s, y - 92 * s
    if faros > 0:
        h.emitir(elipse_(fx, fy, 10 * s, 14 * s, n=12), 1.4 * faros)
        h.luz_cono(fx, fy, 0.05, 0.28, 900 * s, (1.4, 1.4, 1.4), k=faros, suave=0.5)
    if bandera:                                                 # banderín en la antena
        bx, by = x - 240 * s, y - 128 * s
        h.trazo(np.array([[bx, by], [bx - 20 * s, by - 150 * s]]), 3 * s, sem + 40, color=gris(30))
        ond = math.sin(t * 14) * 8 * s
        P = np.array([[bx - 20 * s, by - 150 * s], [bx - 120 * s, by - 140 * s + ond], [bx - 112 * s, by - 96 * s + ond],
                      [bx - 18 * s, by - 106 * s]])
        h.pieza(P, 220, sem + 41, w=3 * s, luz=(0.3, -1), d=3, trama=0, rim=0)
        if bandera == "franjas":
            for k in range(3):
                a = P[0] + (P[3] - P[0]) * (k / 3 + 0.08)
                h.trazo(np.array([a, a + (P[1] - P[0])]), 7 * s, sem + 42 + k, color=gris(30))
        elif bandera == "estrella":
            c = P.mean(0)
            h.pieza(np.array([[c[0] + math.cos(a) * r, c[1] + math.sin(a) * r] for a, r in
                              zip(np.linspace(-math.pi / 2, 1.5 * math.pi, 10, endpoint=False), [16 * s, 7 * s] * 5)]), 25,
                    sem + 45, w=0, luz=(0, -1), d=1, sombra=0, trama=0, rim=0, linea=False)
        else:
            N.texto_maquina(h, bandera, P.mean(0)[0], P.mean(0)[1], 22 * s, t, -99, cps=1e9, tono=0.05, centro=True)


def velocimetro(h, cx, cy, r, v, t=0.0, sem=0):
    """Velocímetro de tablero: v 0..1 lleva la aguja a la zona roja (temblando al final)."""
    h.pieza(elipse_(cx, cy, r * 1.08, r * 1.08, n=64), 50, sem, w=8, luz=(0.3, -1), d=r * 0.06, trama=0.4, rim=0.95, rim_tono=230)
    h.pieza(elipse_(cx, cy, r, r, n=64), 210, sem + 1, w=3, luz=(0.3, -1), d=4, trama=0, rim=0)
    a0, a1 = math.radians(150), math.radians(390)
    for k in range(13):
        a = a0 + (a1 - a0) * k / 12
        l0 = 0.78 if k % 2 else 0.68
        h.trazo(np.array([[cx + math.cos(a) * r * l0, cy + math.sin(a) * r * l0], [cx + math.cos(a) * r * 0.9, cy + math.sin(a) * r * 0.9]]),
                6 if k % 2 == 0 else 3, sem + 10 + k)
        if k % 2 == 0:
            N.texto_maquina(h, str(k * 20), cx + math.cos(a) * r * 0.55, cy + math.sin(a) * r * 0.55, r * 0.11, t, -99, cps=1e9,
                            tono=0.1, centro=True)
    roja = [(cx + math.cos(a) * r * 0.86, cy + math.sin(a) * r * 0.86) for a in np.linspace(a0 + (a1 - a0) * 0.8, a1, 12)]
    roja += [(cx + math.cos(a) * r * 0.94, cy + math.sin(a) * r * 0.94) for a in np.linspace(a1, a0 + (a1 - a0) * 0.8, 12)]
    h.pieza(np.array(roja), 30, sem + 40, w=0, luz=(0, -1), d=1, sombra=0, trama=0, rim=0, linea=False)
    tiembla = 0.03 * math.sin(t * 50) * clamp01((v - 0.85) * 8)
    a = a0 + (a1 - a0) * min(1.0, v) + tiembla
    h.pieza(np.array([[cx + math.cos(a) * r * 0.86, cy + math.sin(a) * r * 0.86], [cx + math.cos(a + 1.57) * 8, cy + math.sin(a + 1.57) * 8],
                      [cx - math.cos(a) * r * 0.14, cy - math.sin(a) * r * 0.14], [cx + math.cos(a - 1.57) * 8, cy + math.sin(a - 1.57) * 8]]),
            20, sem + 41, w=3, luz=(0.3, -1), d=3, trama=0, rim=0.8)
    h.pieza(elipse_(cx, cy, r * 0.08, r * 0.08, n=16), 40, sem + 42, w=3, luz=(0.3, -1), d=2, trama=0, rim=0.9)


def fichas(h, x, y, n, s=1.0, sem=0, tono=200):
    """Pila de fichas de póker (vista lateral)."""
    for k in range(n):
        yy = y - k * 9 * s
        h.pieza(elipse_(x, yy, 40 * s, 12 * s, n=24), tono if k % 2 else 40, sem + k, w=2.5 * s, luz=(0.3, -1), d=3, trama=0, rim=0.6)
