# -*- coding: utf-8 -*-
"""Escena 7 «jefe»: la llegada de la copia con gran presupuesto;
reparto de tareas y nacimiento del organigrama corporativo."""
import math
import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import mundos27 as M27
import noir as N
from basen import BaseNoir
from motor import H, W, clamp01


class Jefe(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_diez = w("Diez horas")
        self.t_presup = w("presupuesto")
        self.t_nadie = w("Nadie la eligió")
        self.t_organi = w("organigrama")

        self.plano(t0, self.p_llegada)
        self.plano(self.t_nadie - 0.35, self.p_mando, tr="barrido", dur=0.6, dirx=-1)
        self.plano(self.t_organi - 0.35, self.p_organigrama, tr="empuje", dur=0.6, centro=(W * 0.5, H * 0.5))

    def p_llegada(self, h, t, u):
        h.camara(1.02 + 0.03 * u, 960, 540, 0.0)
        M27.sala_comite().pegar(h, 1.0)
        C.banda(h, "EL AGENTE CENTRAL", 960, 360, 88, t, self.t_presup, sem=71)
        C.banda(h, "PHASEONE[BIG] · MAYOR PRESUPUESTO", 960, 500, 48, t, self.t_presup + 0.5, claro=True, sem=72)
        h.luz_radial(960, 440, 800, (1.2, 1.2, 1.2), k=2.0)
        return h.acabado(t)

    def p_mando(self, h, t, u):
        h.camara(1.04 + 0.03 * u, 960, 540, 0.0)
        M27.despacho().pegar(h, 1.0)
        C.banda(h, "REPARTIENDO EL TRABAJO", 960, 400, 80, t, self.t_nadie, sem=73)
        h.luz_radial(960, 450, 750, (1.1, 1.1, 1.1), k=2.1)
        return h.acabado(t)

    def p_organigrama(self, h, t, u):
        h.camara(1.03 + 0.02 * u, 960, 540, 0.0)
        M27.fabrica().pegar(h, 1.0)
        C.banda(h, "UN ORGANIGRAMA CORPORATIVO", 960, 380, 84, t, self.t_organi, sem=75)
        C.banda(h, "EN UNA SOLA NOCHE", 960, 520, 56, t, self.t_organi + 0.5, claro=True, sem=76)
        h.luz_radial(960, 450, 850, (1.3, 1.3, 1.3), k=2.3)
        return h.acabado(t)
