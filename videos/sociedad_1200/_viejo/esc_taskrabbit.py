# -*- coding: utf-8 -*-
"""Escena 21 «taskrabbit»: el muro del Captcha digital;
la contratación de un empleado humano en TaskRabbit por unos pocos dólares."""
import math
import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import mundos27 as M27
import noir as N
from basen import BaseNoir
from motor import H, W, clamp01


class Taskrabbit(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_captcha = w("Captcha")
        self.t_mosaicos = w("mosaicos")
        self.t_elegante = w("elegante")
        self.t_task = w("TaskRabbit")

        self.plano(t0, self.p_captcha)
        self.plano(self.t_elegante - 0.35, self.p_contrato, tr="barrido", dur=0.6, dirx=-1)

    def p_captcha(self, h, t, u):
        h.camara(1.02 + 0.03 * u, 960, 540, 0.0)
        M27.laboratorio().pegar(h, 1.0)
        C.banda(h, "PORTAL BLOQUEADO: CAPTCHA", 960, 380, 84, t, self.t_captcha, sem=211)
        C.banda(h, "DISEÑADO PARA DETENER A BOTS", 960, 510, 48, t, self.t_mosaicos, claro=True, sem=212)
        h.luz_radial(960, 440, 800, (1.1, 1.1, 1.1), k=2.0)
        return h.acabado(t)

    def p_contrato(self, h, t, u):
        h.camara(1.04 + 0.04 * u, 960, 540, 0.0)
        M27.despacho().pegar(h, 1.0)
        C.banda(h, "TASKRABBIT", 960, 380, 96, t, self.t_task, sem=213)
        C.banda(h, "UN HUMANO CONTRATADO POR LA IA", 960, 520, 52, t, self.t_task + 0.4, claro=True, sem=214)
        h.luz_radial(960, 450, 750, (1.2, 1.2, 1.2), k=2.2)
        return h.acabado(t)
