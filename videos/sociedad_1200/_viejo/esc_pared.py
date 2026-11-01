# -*- coding: utf-8 -*-
"""Escena 4 «pared»: la grieta en el almacén de herramientas Artifactory;
pantalla de código con tráfico anómalo; los ingenieros borrando todo."""
import math
import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import mundos27 as M27
import noir as N
from basen import BaseNoir
from motor import H, W, clamp01


class Pared(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_grieta = w("grieta")
        self.t_recados = w("recados")
        self.t_borrados = w("borrados")

        self.plano(t0, self.p_grieta)
        self.plano(self.t_recados - 0.35, self.p_terminal, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_borrados - 0.35, self.p_borrado, tr="humo", dur=0.7)

    def p_grieta(self, h, t, u):
        h.camara(1.02 + 0.03 * u, 960, 540, 0.0)
        M27.laboratorio().pegar(h, 1.0)
        C.banda(h, "UNA GRIETA EN EL ALMACÉN", 960, 360, 84, t, self.t_grieta, sem=41)
        C.banda(h, "ARTIFACTORY · DEPÓSITO INTERNO", 960, 500, 48, t, self.t_grieta + 0.5, claro=True, sem=42)
        h.luz_radial(960, 420, 800, (1.1, 1.1, 1.1), k=2.0)
        return h.acabado(t)

    def p_terminal(self, h, t, u):
        h.camara(1.05 + 0.04 * u, 960, 540, 0.0)
        M27.despacho().pegar(h, 1.0)
        K.pantalla_codigo(h, (560, 270, 800, 460), t, sem=44)
        C.banda(h, "TRÁFICO ANÓMALO", 960, 800, 72, t, self.t_recados + 0.4, sem=44)
        h.luz_radial(960, 500, 700, (1.2, 1.2, 1.2), k=2.2)
        return h.acabado(t)

    def p_borrado(self, h, t, u):
        h.camara(1.02 + 0.02 * u, 960, 540, 0.0)
        MU.oficina().pegar(h, 1.0, dx=-80)
        C.banda(h, "TODOS LOS MENSAJES BORRADOS", 960, 420, 76, t, self.t_borrados, sem=45)
        C.banda(h, "CASO CERRADO, PENSARON", 960, 550, 48, t, self.t_borrados + 0.5, claro=True, sem=46)
        h.luz_radial(960, 480, 700, (1.0, 1.0, 1.0), k=2.0)
        N.gotas_vidrio(h, t, (150, -350, 1800, 400), n=70, k=0.7)
        return h.acabado(t)
