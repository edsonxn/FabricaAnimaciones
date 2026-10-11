# -*- coding: utf-8 -*-
"""Escena 20 «mundo_exterior»: salir a la calle real;
los experimentos de ARC con GPT-4 en 2023 y la billetera digital."""
import math
import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import mundos27 as M27
import noir as N
from basen import BaseNoir
from motor import H, W, clamp01


class MundoExterior(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_calle = w("calle real")
        self.t_2023 = w("2023")
        self.t_riesgo = w("Centro de Alineación")
        self.t_billetera = w("billetera digital")

        self.plano(t0, self.p_calle)
        self.plano(self.t_2023 - 0.35, self.p_arc, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_billetera - 0.35, self.p_billetera, tr="empuje", dur=0.6, centro=(W * 0.5, H * 0.5))

    def p_calle(self, h, t, u):
        h.camara(1.02 + 0.03 * u, 960, 540, 0.0)
        M27.capitolio().pegar(h, 1.0)
        C.banda(h, "OPERAR EN LA CALLE REAL", 960, 380, 84, t, self.t_calle, sem=201)
        h.luz_radial(960, 420, 800, (1.1, 1.1, 1.1), k=2.0)
        return h.acabado(t)

    def p_arc(self, h, t, u):
        h.camara(1.04 + 0.04 * u, 960, 540, 0.0)
        M27.laboratorio().pegar(h, 1.0)
        C.banda(h, "MARZO DE 2023", 960, 360, 88, t, self.t_2023, sem=203)
        C.banda(h, "EVALUACIONES DE RIESGO DE GPT-4", 960, 500, 48, t, self.t_riesgo, claro=True, sem=204)
        h.luz_radial(960, 450, 750, (1.2, 1.2, 1.2), k=2.1)
        return h.acabado(t)

    def p_billetera(self, h, t, u):
        h.camara(1.03 + 0.02 * u, 960, 540, 0.0)
        M27.despacho().pegar(h, 1.0)
        K.billetes(h, 960, 600, n=6, s=1.2)
        C.banda(h, "BILLETERA DIGITAL ACTIVA", 960, 760, 76, t, self.t_billetera + 0.4, sem=205)
        h.luz_radial(960, 500, 700, (1.2, 1.2, 1.2), k=2.2)
        return h.acabado(t)
