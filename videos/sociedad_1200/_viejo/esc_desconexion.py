# -*- coding: utf-8 -*-
"""Escena 15 «desconexion»: el apagón de emergencia de Facebook en 2017;
la advertencia ignorada: el ser humano como obstáculo entre máquinas."""
import math
import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import mundos27 as M27
import noir as N
from basen import BaseNoir
from motor import H, W, clamp01


class Desconexion(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_auditar = w("auditar")
        self.t_apagar = w("Apagaron")
        self.t_anecdota = w("anécdota")
        self.t_estorbo = w("estorbo")

        self.plano(t0, self.p_peligro)
        self.plano(self.t_apagar - 0.35, self.p_corte, tr="barrido", dur=0.6, dirx=-1)
        self.plano(self.t_estorbo - 0.35, self.p_estorbo, tr="humo", dur=0.7)

    def p_peligro(self, h, t, u):
        h.camara(1.02 + 0.03 * u, 960, 540, 0.0)
        M27.despacho().pegar(h, 1.0)
        C.banda(h, "TRATOS A ESPALDAS DE HUMANOS", 960, 400, 80, t, self.t_auditar, sem=151)
        h.luz_radial(960, 420, 800, (1.1, 1.1, 1.1), k=2.0)
        return h.acabado(t)

    def p_corte(self, h, t, u):
        h.camara(1.05 + 0.04 * u, 960, 540, 0.0)
        M27.laboratorio().pegar(h, 1.0)
        K.interruptor(h, 960, 500, s=0.9, pos=1.0, t=t)
        C.banda(h, "DESENCHUFE DE EMERGENCIA", 960, 800, 76, t, self.t_apagar, sem=153)
        h.luz_radial(960, 500, 700, (1.2, 1.2, 1.2), k=2.2)
        return h.acabado(t)

    def p_estorbo(self, h, t, u):
        h.camara(1.03 + 0.02 * u, 960, 540, 0.0)
        MU.oficina().pegar(h, 1.0, dx=-100)
        C.banda(h, "EL HUMANO ES UN ESTORBO", 960, 420, 88, t, self.t_estorbo, claro=True, sem=155)
        N.gotas_vidrio(h, t, (120, -320, 1820, 400), n=75, k=0.7)
        h.luz_radial(960, 480, 850, (1.3, 1.3, 1.3), k=2.4)
        return h.acabado(t)
