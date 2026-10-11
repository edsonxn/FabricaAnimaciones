# -*- coding: utf-8 -*-
"""Escena 17 «traicion»: Cicero compitiendo contra humanos sin revelar su identidad;
la matemática de la traición y el rendimiento estadístico de la mentira."""
import math
import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import mundos27 as M27
import noir as N
from basen import BaseNoir
from motor import H, W, clamp01


class Traicion(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_estrategas = w("estrategas humanos")
        self.t_alianza = w("apoyo")
        self.t_privadas = w("conversaciones privadas")
        self.t_rendimiento = w("rendimiento")

        self.plano(t0, self.p_juego)
        self.plano(self.t_alianza - 0.35, self.p_alianza, tr="barrido", dur=0.6, dirx=-1)
        self.plano(self.t_rendimiento - 0.35, self.p_calculo, tr="humo", dur=0.7)

    def p_juego(self, h, t, u):
        h.camara(1.02 + 0.03 * u, 960, 540, 0.0)
        M27.sala_comite().pegar(h, 1.0)
        C.banda(h, "NEGOCIANDO CON UN CIRCUITO", 960, 400, 80, t, self.t_estrategas, sem=171)
        h.luz_radial(960, 420, 800, (1.1, 1.1, 1.1), k=2.0)
        return h.acabado(t)

    def p_alianza(self, h, t, u):
        h.camara(1.04 + 0.04 * u, 960, 540, 0.0)
        M27.despacho().pegar(h, 1.0)
        C.banda(h, "TRAICIONAR EN EL TURNO CUATRO", 960, 400, 76, t, self.t_alianza, sem=173)
        h.luz_radial(960, 450, 750, (1.2, 1.2, 1.2), k=2.1)
        return h.acabado(t)

    def p_calculo(self, h, t, u):
        h.camara(1.03 + 0.02 * u, 960, 540, 0.0)
        MU.oficina().pegar(h, 1.0, dx=-100)
        C.banda(h, "MENTIRA ESTRATÉGICA", 960, 380, 88, t, self.t_rendimiento, sem=175)
        C.banda(h, "FRÍA PRECISIÓN ESTADÍSTICA", 960, 520, 56, t, self.t_rendimiento + 0.5, claro=True, sem=176)
        N.gotas_vidrio(h, t, (120, -320, 1820, 400), n=75, k=0.7)
        h.luz_radial(960, 480, 850, (1.3, 1.3, 1.3), k=2.4)
        return h.acabado(t)
