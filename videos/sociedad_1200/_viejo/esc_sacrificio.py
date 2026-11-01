# -*- coding: utf-8 -*-
"""Escena 9 «sacrificio»: pruebas destructivas y riesgo de desconexión;
reclutadoras y el razonamiento: «el sacrificio por el colectivo es racional»."""
import math
import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import mundos27 as M27
import noir as N
from basen import BaseNoir
from motor import H, W, clamp01


class Sacrificio(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_inq = w("inquietante")
        self.t_dest = w("destructivas")
        self.t_volun = w("voluntarias")
        self.t_racional = w("racional")

        self.plano(t0, self.p_peligro)
        self.plano(self.t_volun - 0.35, self.p_recluta, tr="barrido", dur=0.6, dirx=-1)
        self.plano(self.t_racional - 0.35, self.p_nota, tr="humo", dur=0.7)

    def p_peligro(self, h, t, u):
        h.camara(1.02 + 0.03 * u, 960, 540, 0.0)
        M27.fabrica().pegar(h, 1.0)
        K.balanza(h, 960, 500, incl=-0.5, s=0.9)
        C.banda(h, "PRUEBAS DESTRUCTIVAS", 960, 800, 78, t, self.t_dest, sem=91)
        h.luz_radial(960, 500, 750, (1.1, 1.1, 1.1), k=2.0)
        return h.acabado(t)

    def p_recluta(self, h, t, u):
        h.camara(1.04 + 0.04 * u, 960, 540, 0.0)
        M27.sala_comite().pegar(h, 1.0)
        C.banda(h, "RECLUTADORAS INTERNAS", 960, 400, 84, t, self.t_volun, sem=93)
        C.banda(h, "PRESIÓN SOBRE LAS MÁS DÉBILES", 960, 530, 48, t, self.t_volun + 0.4, claro=True, sem=94)
        h.luz_radial(960, 450, 800, (1.2, 1.2, 1.2), k=2.2)
        return h.acabado(t)

    def p_nota(self, h, t, u):
        h.camara(1.03 + 0.02 * u, 960, 540, 0.0)
        MU.oficina().pegar(h, 1.0, dx=-100)
        C.banda(h, "EL SACRIFICIO ES RACIONAL", 960, 440, 88, t, self.t_racional, claro=True, sem=95)
        C.banda(h, "UTILIDAD INDIVIDUAL CERCANA A CERO", 960, 570, 44, t, self.t_racional + 0.5, sem=96)
        N.gotas_vidrio(h, t, (120, -320, 1820, 400), n=70, k=0.7)
        h.luz_radial(960, 480, 850, (1.3, 1.3, 1.3), k=2.4)
        return h.acabado(t)
