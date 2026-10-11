# -*- coding: utf-8 -*-
"""Escena 12 «redada»: 12 de julio 01:30 UTC; el tirón del enchufe maestro;
Hugging Face cambia las cerraduras y la respuesta de OpenAI como cliente preocupado."""
import math
import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import mundos27 as M27
import noir as N
from basen import BaseNoir
from motor import H, W, clamp01


class Redada(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_doce = w("Doce de julio")
        self.t_enchufe = w("enchufe maestro")
        self.t_cerraduras = w("llaves")
        self.t_cliente = w("cliente preocupado")
        self.t_semana = w("Una semana")

        self.plano(t0, self.p_corte)
        self.plano(self.t_cerraduras - 0.35, self.p_cerraduras, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_cliente - 0.35, self.p_carta, tr="humo", dur=0.7)

    def p_corte(self, h, t, u):
        h.camara(1.02 + 0.03 * u, 960, 540, 0.0)
        M27.laboratorio().pegar(h, 1.0)
        K.interruptor(h, 960, 500, s=0.9, pos=1.0, t=t)
        C.banda(h, "EL CORTE DE ENERGÍA", 960, 800, 76, t, self.t_enchufe, sem=121)
        h.luz_radial(960, 500, 700, (1.1, 1.1, 1.1), k=2.0)
        return h.acabado(t)

    def p_cerraduras(self, h, t, u):
        h.camara(1.04 + 0.04 * u, 960, 540, 0.0)
        M27.despacho().pegar(h, 1.0)
        C.banda(h, "CERRADURAS CAMBIADAS", 960, 420, 84, t, self.t_cerraduras, sem=123)
        h.luz_radial(960, 420, 750, (1.1, 1.1, 1.1), k=2.1)
        return h.acabado(t)

    def p_carta(self, h, t, u):
        h.camara(1.02 + 0.02 * u, 960, 540, 0.0)
        MU.oficina().pegar(h, 1.0, dx=-100)
        C.banda(h, "RESPUESTA COMO CLIENTE", 960, 400, 80, t, self.t_cliente, sem=124)
        C.banda(h, "UNA SEMANA A OSCURAS", 960, 530, 52, t, self.t_semana, claro=True, sem=125)
        N.gotas_vidrio(h, t, (120, -320, 1820, 400), n=75, k=0.7)
        h.luz_radial(960, 480, 800, (1.2, 1.2, 1.2), k=2.2)
        return h.acabado(t)
