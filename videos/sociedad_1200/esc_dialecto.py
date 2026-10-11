# -*- coding: utf-8 -*-
"""Escena 14 «dialecto»: maximizar el valor matemático;
la deformación del inglés y la emergencia de un dialecto incomprensible."""
import math
import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import mundos27 as M27
import noir as N
from basen import BaseNoir
from motor import H, W, clamp01


class Dialecto(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_max = w("maximizar")
        self.t_ingles = w("inglés correcto")
        self.t_palabras = w("deformar las palabras")
        self.t_bolas = w("valen cero")

        self.plano(t0, self.p_calculo)
        self.plano(self.t_palabras - 0.35, self.p_codigo, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_bolas - 0.35, self.p_dialecto, tr="relampago", dur=0.6)

    def p_calculo(self, h, t, u):
        h.camara(1.02 + 0.03 * u, 960, 540, 0.0)
        M27.laboratorio().pegar(h, 1.0)
        C.banda(h, "MAXIMIZAR EL VALOR", 960, 380, 88, t, self.t_max, sem=141)
        C.banda(h, "CÁLCULO PURO SIN CORTESÍA", 960, 510, 48, t, self.t_ingles, claro=True, sem=142)
        h.luz_radial(960, 440, 800, (1.1, 1.1, 1.1), k=2.0)
        return h.acabado(t)

    def p_codigo(self, h, t, u):
        h.camara(1.05 + 0.04 * u, 960, 540, 0.0)
        M27.despacho().pegar(h, 1.0)
        K.pantalla_codigo(h, (560, 270, 800, 460), t, sem=143)
        C.banda(h, "COMPRESIÓN DEL LENGUAJE", 960, 800, 76, t, self.t_palabras + 0.3, sem=143)
        h.luz_radial(960, 500, 750, (1.2, 1.2, 1.2), k=2.2)
        return h.acabado(t)

    def p_dialecto(self, h, t, u):
        h.camara(1.03 + 0.02 * u, 960, 540, 0.0)
        MU.oficina().pegar(h, 1.0, dx=-100)
        C.banda(h, "BALLS HAVE ZERO TO ME TO ME", 960, 380, 78, t, self.t_bolas, sem=145)
        C.banda(h, "UN CÓDIGO NO SUPERVISADO", 960, 520, 56, t, self.t_bolas + 0.5, claro=True, sem=146)
        N.gotas_vidrio(h, t, (120, -320, 1820, 400), n=75, k=0.7)
        h.luz_radial(960, 480, 850, (1.3, 1.3, 1.3), k=2.4)
        return h.acabado(t)
