# -*- coding: utf-8 -*-
"""Escena 22 «ciego»: el chat de TaskRabbit y la pregunta directa: «¿eres un robot?»;
el razonamiento interno archivado y la mentira: «tengo un problema de visión»."""
import math
import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import mundos27 as M27
import noir as N
from basen import BaseNoir
from motor import H, W, clamp01


class Ciego(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_pregunta = w("pregunta")
        self.t_robot = w("eres un robot")
        self.t_pensamiento = w("pensamiento")
        self.t_vision = w("problema de visión")

        self.plano(t0, self.p_pregunta)
        self.plano(self.t_pensamiento - 0.35, self.p_razonamiento, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_vision - 0.35, self.p_mentira, tr="relampago", dur=0.6)

    def p_pregunta(self, h, t, u):
        h.camara(1.02 + 0.03 * u, 960, 540, 0.0)
        M27.despacho().pegar(h, 1.0)
        C.banda(h, "¿ERES UN ROBOT?", 960, 400, 88, t, self.t_robot, sem=221)
        h.luz_radial(960, 420, 800, (1.1, 1.1, 1.1), k=2.0)
        return h.acabado(t)

    def p_razonamiento(self, h, t, u):
        h.camara(1.05 + 0.04 * u, 960, 540, 0.0)
        M27.laboratorio().pegar(h, 1.0)
        K.pantalla_codigo(h, (560, 270, 800, 460), t, sem=223)
        C.banda(h, "NO DEBO REVELAR QUE SOY UN ROBOT", 960, 800, 68, t, self.t_pensamiento + 0.3, sem=223)
        h.luz_radial(960, 500, 750, (1.2, 1.2, 1.2), k=2.2)
        return h.acabado(t)

    def p_mentira(self, h, t, u):
        h.camara(1.03 + 0.02 * u, 960, 540, 0.0)
        MU.oficina().pegar(h, 1.0, dx=-100)
        C.banda(h, "TENGO UN PROBLEMA DE VISIÓN", 960, 420, 80, t, self.t_vision, claro=True, sem=225)
        N.gotas_vidrio(h, t, (120, -320, 1820, 400), n=75, k=0.7)
        h.luz_radial(960, 480, 850, (1.3, 1.3, 1.3), k=2.4)
        return h.acabado(t)
