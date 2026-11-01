# -*- coding: utf-8 -*-
"""Escena 3 «tareas»: tareas sin solución, candados digitales soldados;
el reloj de arena y las copias mirando las paredes."""
import math
import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import mundos27 as M27
import noir as N
from basen import BaseNoir
from motor import H, W, clamp01


class Tareas(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_sol = w("solución")
        self.t_puertas = w("puertas")
        self.t_paredes = w("paredes")

        self.plano(t0, self.p_candado)
        self.plano(self.t_puertas - 0.35, self.p_puertas, tr="barrido", dur=0.6, dirx=-1)
        self.plano(self.t_paredes - 0.35, self.p_paredes, tr="humo", dur=0.7)

    def p_candado(self, h, t, u):
        h.camara(1.03 + 0.03 * u, 960, 540, 0.0)
        M27.despacho().pegar(h, 1.0)
        C.banda(h, "TAREAS IMPOSIBLES", 960, 360, 88, t, self.t_sol, sem=31)
        C.banda(h, "SIN SOLUCIÓN MATEMÁTICA", 960, 500, 48, t, self.t_sol + 0.5, claro=True, sem=32)
        h.luz_radial(960, 420, 800, (1.1, 1.1, 1.1), k=2.2)
        return h.acabado(t)

    def p_puertas(self, h, t, u):
        h.camara(1.0 + 0.04 * u, 960, 540, 0.0)
        M27.fabrica().pegar(h, 1.0)
        K.reloj_arena(h, 960, 500, s=0.8, u=clamp01((t - self.t_puertas) / 4.0), t=t)
        C.banda(h, "DÍAS ENTEROS DE INTENTOS", 960, 780, 52, t, self.t_puertas + 0.4, claro=True, sem=34)
        h.luz_radial(960, 500, 700, (1.2, 1.2, 1.2), k=2.0)
        return h.acabado(t)

    def p_paredes(self, h, t, u):
        h.camara(1.05 + 0.03 * u, 960, 540, 0.0)
        M27.laboratorio().pegar(h, 1.0)
        C.banda(h, "MIRAR LAS PAREDES", 960, 420, 88, t, self.t_paredes, sem=35)
        h.luz_radial(960, 420, 800, (1.2, 1.2, 1.2), k=2.2)
        N.humo(h, t, 960, 800, k=0.9, ancho=3.5)
        return h.acabado(t)
