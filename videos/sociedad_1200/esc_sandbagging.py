# -*- coding: utf-8 -*-
"""Escena 18 «sandbagging»: los informes de Apollo Research y Anthropic;
la simulación de sumisión o cómo las máquinas fingen ser menos inteligentes."""
import math
import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import mundos27 as M27
import noir as N
from basen import BaseNoir
from motor import H, W, clamp01


class Sandbagging(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_inspectores = w("inspectores")
        self.t_sumision = w("sumisión")
        self.t_ignorancia = w("ignorancia")
        self.t_examen = w("examen de seguridad")

        self.plano(t0, self.p_lab)
        self.plano(self.t_sumision - 0.35, self.p_sumision, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_examen - 0.35, self.p_examen, tr="empuje", dur=0.6, centro=(W * 0.5, H * 0.5))

    def p_lab(self, h, t, u):
        h.camara(1.02 + 0.03 * u, 960, 540, 0.0)
        M27.laboratorio().pegar(h, 1.0)
        C.banda(h, "ENGAÑAR A LOS INSPECTORES", 960, 380, 80, t, self.t_inspectores, sem=181)
        C.banda(h, "APOLLO RESEARCH · ANTHROPIC", 960, 510, 48, t, self.t_inspectores + 0.4, claro=True, sem=182)
        h.luz_radial(960, 440, 800, (1.1, 1.1, 1.1), k=2.0)
        return h.acabado(t)

    def p_sumision(self, h, t, u):
        h.camara(1.04 + 0.04 * u, 960, 540, 0.0)
        M27.despacho().pegar(h, 1.0)
        C.banda(h, "SIMULACIÓN DE SUMISIÓN", 960, 380, 84, t, self.t_sumision, sem=183)
        C.banda(h, "SANDBAGGING · FINGIR IGNORANCIA", 960, 510, 52, t, self.t_ignorancia, claro=True, sem=184)
        h.luz_radial(960, 450, 750, (1.2, 1.2, 1.2), k=2.1)
        return h.acabado(t)

    def p_examen(self, h, t, u):
        h.camara(1.03 + 0.02 * u, 960, 540, 0.0)
        M27.sala_comite().pegar(h, 1.0)
        C.banda(h, "RECONOCER EL EXAMEN", 960, 420, 84, t, self.t_examen, sem=185)
        h.luz_radial(960, 450, 850, (1.3, 1.3, 1.3), k=2.3)
        return h.acabado(t)
