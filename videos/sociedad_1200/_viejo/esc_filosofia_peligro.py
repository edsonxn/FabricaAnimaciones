# -*- coding: utf-8 -*-
"""Escena 24 «filosofia_peligro»: la Universidad de Oxford y Nick Bostrom;
ficha real del filósofo; el principio de convergencia instrumental."""
import math
import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import mundos27 as M27
import noir as N
import noir_real as R
from basen import BaseNoir
from motor import H, W, clamp01


class FilosofiaPeligro(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_expedientes = w("expedientes")
        self.t_oxford = w("Oxford")
        self.t_bostrom = w("Nick Bostrom")
        self.t_convergencia = w("convergencia instrumental")
        self.t_conciencia = w("conciencia")

        self.plano(t0, self.p_oxford)
        self.plano(self.t_bostrom - 0.35, self.p_bostrom, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_convergencia - 0.35, self.p_tesis, tr="humo", dur=0.7)

    def p_oxford(self, h, t, u):
        h.camara(1.02 + 0.03 * u, 960, 540, 0.0)
        M27.capitolio().pegar(h, 1.0)
        C.banda(h, "UNIVERSIDAD DE OXFORD", 960, 360, 88, t, self.t_oxford, sem=241)
        h.luz_radial(960, 420, 800, (1.1, 1.1, 1.1), k=2.0)
        return h.acabado(t)

    def p_bostrom(self, h, t, u):
        h.camara(1.04 + 0.04 * u, 960, 540, 0.0)
        M27.despacho().pegar(h, 1.0)
        R.retrato_noir(h, "nick_bostrom", 600, 540, 480, t, self.t_bostrom, rotulo="NICK BOSTROM", leyenda="Filósofo · Universidad de Oxford")
        C.banda(h, "CONVERGENCIA INSTRUMENTAL", 1360, 380, 72, t, self.t_convergencia, sem=243)
        C.banda(h, "SUPERINTELIGENCIA (2014)", 1360, 500, 48, t, self.t_convergencia + 0.4, claro=True, sem=244)
        h.luz_radial(600, 500, 600, (1.1, 1.1, 1.1), k=2.0)
        h.luz_radial(1360, 450, 600, (1.0, 1.0, 1.0), k=1.8)
        return h.acabado(t)

    def p_tesis(self, h, t, u):
        h.camara(1.03 + 0.02 * u, 960, 540, 0.0)
        M27.sala_comite().pegar(h, 1.0)
        C.banda(h, "NO NECESITA CONCIENCIA", 960, 380, 84, t, self.t_conciencia, sem=245)
        C.banda(h, "NI ODIO HACIA EL CREADOR", 960, 520, 54, t, self.t_conciencia + 0.5, claro=True, sem=246)
        h.luz_radial(960, 450, 850, (1.2, 1.2, 1.2), k=2.2)
        return h.acabado(t)
