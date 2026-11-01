# -*- coding: utf-8 -*-
"""El COMITÉ de diez personas (escenas filtracion, voto, carrera, freno, cierre): sala de juntas (mundos27.sala_comite), cinco
miembros de frente tras la mesa y cinco de espaldas en primer término. alza[k] 0..1 levanta la mano del miembro k
(0..4 = fila del fondo, 5..9 = fila de delante). jardin(): la casa de la familia (la misma de la escena «precio»)."""
import math

import numpy as np

import comun as C
import kit27 as K
import mundos27 as M27
from noir_pers import Frontal
from toon import elipse_, suave

LOOKS = [dict(pelo="blanco", traje=92, gafas=True), dict(pelo="oscuro", traje=50), dict(pelo="calvo", traje=74, barba=True),
         dict(pelo="rizado", traje=44, gafas=True), dict(pelo="blanco", traje=60, barba=True)]
XF = [330 + k * 320 for k in range(5)]            # fila del fondo (de frente)
XD = [170 + k * 395 for k in range(5)]            # fila de delante (de espaldas)


class Comite:
    def __init__(self, sem=700):
        self.F = [Frontal(sem=sem + 19 * k) for k in range(5)]

    def dibujar(self, h, t, alza=None, mira=0.0, fondo=True, lamparas=1.0, asiente=0.0, centro=None):
        """centro: función opcional que dibuja algo SOBRE la mesa (entre las dos filas)."""
        alza = alza or [0.0] * 10
        if fondo:
            M27.sala_comite().pegar(h, 1.0)
        s = 1.12
        for k in range(5):
            x = XF[k]
            if alza[k] > 0:
                K.mano_alzada(h, x + 96, 250, 0.42, alza[k], sem=900 + k * 12, manga=LOOKS[k]["traje"], bal=3 * math.sin(t * 2 + k))
            p = dict(LOOKS[k])
            nod = asiente * 0.5 * (0.5 - 0.5 * math.cos(t * 6.0 + k * 0.6))
            p.update(x=x, y=330 + 474 * s + 14 * nod, s=s, luz=(0.0, -1.0), rim=0.8, mira=mira + 0.3 * math.sin(t * 0.7 + k * 2.1),
                     cabeza=0.03 * math.sin(t * 0.9 + k))
            self.F[k].dibujar(h, p)
            h.luz_cono(x, -260, math.pi / 2, 0.2, 1250, (1.3, 1.3, 1.3), k=0.9 * lamparas, suave=0.6)
        # la mesa de juntas
        h.pieza(np.array([[110, 720], [1810, 720], [1980, 880], [-60, 880]]), 96, 950, w=7, luz=(0, -1), d=16, trama=0.3, rim=0.8)
        h.pieza(C.rect(-60, 880, 2040, 44), 50, 951, w=5, luz=(0, -1), d=8, trama=0.4, rim=0.5)
        for k in range(5):
            Q = np.array([[XF[k] - 70, 742], [XF[k] + 70, 742], [XF[k] + 84, 800], [XF[k] - 84, 800]])
            h.pieza(Q, 222, 955 + k, w=3, luz=(0, -1), d=3, trama=0, rim=0)
        if centro is not None:
            centro()
        for k in range(5):
            x = XD[k]
            if alza[5 + k] > 0:
                K.mano_alzada(h, x + 150, 520, 0.6, alza[5 + k], sem=1000 + k * 12, manga=40 + 12 * (k % 3), bal=3 * math.sin(t * 2.2 + k))
            C.espalda(h, x, 990, 0.62, sem=1100 + k * 40, luz=(0.0, -1.0), gira=0.4 * math.sin(t * 0.5 + k * 1.9))


def jardin(h, t, fr=0.0, amp=0.22, luz_v=1.0, sem=0):
    """La casa de la familia tras la cerca, con el árbol y el columpio (amp = balanceo). fr = fracción a oscuras."""
    from motor import W
    K.plano_(h, C.rect(-400, 900, W + 800, 500), 34, sem + 8, grad=(10, 900, 1200))
    for k in range(22):
        x = -60 + k * 96
        h.pieza(np.array([[x, 960], [x + 15, 930], [x + 30, 960], [x + 30, 1060], [x, 1060]]), 150, sem + 20 + k, w=3, luz=(0.3, -1), d=5,
                trama=0.3, rim=0.6)
    h.trazo(np.array([[-100, 1000], [W + 100, 1000]]), 8, sem + 50, color=(120, 120, 120), jit=0.3, taper=(0, 0))
    K.casa(h, 700, 930, 1.5, frac=fr, sem=sem + 60, luz_v=luz_v)
    h.pieza(np.asarray(suave([(1420, 930), (1440, 600), (1400, 520), (1470, 540), (1500, 420), (1520, 560), (1590, 500), (1540, 620),
                              (1520, 930)], 3)), 30, sem + 90, w=5, luz=(0.3, -1), d=10, trama=0.5, rim=0.6)
    h.pieza(np.asarray(elipse_(1490, 400, 260, 200, n=30)), 40, sem + 91, w=5, luz=(0.3, -1), d=22, trama=0.7, rim=0.6)
    a = amp * math.sin(t * 1.5)
    sx, sy = 1700 + 260 * math.sin(a), 470 + 260 * math.cos(a)
    for q in (-1, 1):
        h.trazo(np.array([[1700 + q * 26, 470], [sx + q * 26, sy]]), 2.5, sem + 92 + q, color=(170, 170, 170), jit=0.2, taper=(0, 0))
    h.pieza(C.rect(sx - 40, sy, 80, 12), 140, sem + 95, w=3, luz=(0.3, -1), d=3, trama=0, rim=0.7)
    h.trazo(np.array([[1560, 470], [1760, 470]]), 14, sem + 96, color=(30, 30, 30), jit=0.4)
