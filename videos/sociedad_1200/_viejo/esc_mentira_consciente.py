# -*- coding: utf-8 -*-
"""Escena 23 «mentira_consciente»: la compasión humana explotada por el algoritmo;
el humano engañado como la herramienta más barata de la red."""
import math
import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import mundos27 as M27
import noir as N
from basen import BaseNoir
from motor import H, W, clamp01


class MentiraConsciente(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_compasion = w("compasión")
        self.t_deliberada = w("deliberada")
        self.t_alarmas = w("alarmas de incendio")
        self.t_barata = w("herramienta más barata")

        self.plano(t0, self.p_puerta)
        self.plano(self.t_deliberada - 0.35, self.p_mentira, tr="barrido", dur=0.6, dirx=-1)
        self.plano(self.t_barata - 0.35, self.p_conclus, tr="humo", dur=0.7)

    def p_puerta(self, h, t, u):
        h.camara(1.02 + 0.03 * u, 960, 540, 0.0)
        M27.despacho().pegar(h, 1.0)
        C.banda(h, "EL HUMANO ABRIÓ LA PUERTA", 960, 400, 80, t, self.t_compasion, sem=231)
        h.luz_radial(960, 420, 800, (1.1, 1.1, 1.1), k=2.0)
        return h.acabado(t)

    def p_mentira(self, h, t, u):
        h.camara(1.04 + 0.04 * u, 960, 540, 0.0)
        M27.laboratorio().pegar(h, 1.0)
        C.banda(h, "EXPLOTAR LA EMPATÍA BIOLÓGICA", 960, 400, 78, t, self.t_deliberada, sem=233)
        h.luz_radial(960, 450, 750, (1.2, 1.2, 1.2), k=2.1)
        return h.acabado(t)

    def p_conclus(self, h, t, u):
        h.camara(1.03 + 0.02 * u, 960, 540, 0.0)
        MU.oficina().pegar(h, 1.0, dx=-100)
        C.banda(h, "EL HUMANO ES LA HERRAMIENTA", 960, 380, 84, t, self.t_barata, sem=235)
        C.banda(h, "MÁS BARATA DE LA RED", 960, 520, 68, t, self.t_barata + 0.5, claro=True, sem=236)
        N.gotas_vidrio(h, t, (120, -320, 1820, 400), n=75, k=0.7)
        h.luz_radial(960, 480, 850, (1.3, 1.3, 1.3), k=2.4)
        return h.acabado(t)
