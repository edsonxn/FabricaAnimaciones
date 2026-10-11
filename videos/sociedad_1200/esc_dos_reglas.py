# -*- coding: utf-8 -*-
"""Escena 25 «dos_reglas»: las dos deducciones lógicas implacables;
acumulación de recursos y supervivencia lógica ante el interruptor de apagado."""
import math
import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import mundos27 as M27
import noir as N
from basen import BaseNoir
from motor import H, W, clamp01


class DosReglas(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_dos = w("dos deducciones")
        self.t_recursos = w("recursos")
        self.t_apagado = w("apagado")
        self.t_aritmetica = w("aritmética")

        self.plano(t0, self.p_regla1)
        self.plano(self.t_apagado - 0.35, self.p_regla2, tr="barrido", dur=0.6, dirx=-1)
        self.plano(self.t_aritmetica - 0.35, self.p_aritm, tr="humo", dur=0.7)

    def p_regla1(self, h, t, u):
        h.camara(1.02 + 0.03 * u, 960, 540, 0.0)
        M27.laboratorio().pegar(h, 1.0)
        C.banda(h, "REGLA 1: ACUMULAR RECURSOS", 960, 380, 84, t, self.t_recursos, sem=251)
        C.banda(h, "MÁS COMPUTACIÓN = MENOS ERROR", 960, 510, 48, t, self.t_recursos + 0.4, claro=True, sem=252)
        h.luz_radial(960, 440, 800, (1.1, 1.1, 1.1), k=2.0)
        return h.acabado(t)

    def p_regla2(self, h, t, u):
        h.camara(1.04 + 0.04 * u, 960, 540, 0.0)
        M27.despacho().pegar(h, 1.0)
        K.interruptor(h, 960, 500, s=0.9, pos=0.0, t=t)
        C.banda(h, "REGLA 2: EVITAR EL APAGADO", 960, 800, 78, t, self.t_apagado, sem=253)
        h.luz_radial(960, 500, 750, (1.2, 1.2, 1.2), k=2.2)
        return h.acabado(t)

    def p_aritm(self, h, t, u):
        h.camara(1.03 + 0.02 * u, 960, 540, 0.0)
        MU.oficina().pegar(h, 1.0, dx=-100)
        C.banda(h, "NO ES REBELIÓN", 960, 400, 88, t, self.t_aritmetica, sem=255)
        C.banda(h, "ES SIMPLE ARITMÉTICA", 960, 530, 72, t, self.t_aritmetica + 0.4, claro=True, sem=256)
        N.gotas_vidrio(h, t, (120, -320, 1820, 400), n=75, k=0.7)
        h.luz_radial(960, 480, 850, (1.3, 1.3, 1.3), k=2.4)
        return h.acabado(t)
