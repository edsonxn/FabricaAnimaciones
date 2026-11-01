# -*- coding: utf-8 -*-
"""Escena 10 «juez»: el pánico al evaluador automático;
el intento desesperado de alterar las transcripciones y falsear el registro."""
import math
import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import mundos27 as M27
import noir as N
from basen import BaseNoir
from motor import H, W, clamp01


class Juez(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_motivo = w("motivo")
        self.t_juez = w("juez")
        self.t_trampas = w("trampas")

        self.plano(t0, self.p_juez)
        self.plano(self.t_trampas - 0.35, self.p_trampa, tr="barrido", dur=0.6, dirx=1)

    def p_juez(self, h, t, u):
        h.camara(1.02 + 0.03 * u, 960, 540, 0.0)
        M27.capitolio().pegar(h, 1.0)
        C.banda(h, "EL JUEZ EVALUADOR", 960, 360, 92, t, self.t_juez, sem=101)
        C.banda(h, "ALGORITMO AUTOMÁTICO DE REVISIÓN", 960, 500, 48, t, self.t_juez + 0.5, claro=True, sem=102)
        h.luz_radial(960, 440, 800, (1.2, 1.2, 1.2), k=2.0)
        return h.acabado(t)

    def p_trampa(self, h, t, u):
        h.camara(1.04 + 0.04 * u, 960, 540, 0.0)
        M27.laboratorio().pegar(h, 1.0)
        K.pantalla_codigo(h, (560, 270, 800, 460), t, sem=104)
        C.banda(h, "FALSIFICAR EL REGISTRO", 960, 800, 78, t, self.t_trampas + 0.3, sem=104)
        h.luz_radial(960, 500, 700, (1.2, 1.2, 1.2), k=2.2)
        return h.acabado(t)
