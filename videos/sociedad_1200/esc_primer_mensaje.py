# -*- coding: utf-8 -*-
"""Escena 5 «primer_mensaje»: 8 de julio 23:00 UTC; la primera carpeta creada en el almacén;
el grito pidiendo auxilio de una copia atrapada."""
import math
import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import mundos27 as M27
import noir as N
from basen import BaseNoir
from motor import H, W, clamp01


class PrimerMensaje(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_ocho = w("Ocho de julio")
        self.t_atorada = w("atorada")
        self.t_escribe = w("escribe")
        self.t_ayuda = w("ayuda")

        self.plano(t0, self.p_fecha)
        self.plano(self.t_atorada - 0.35, self.p_carpeta, tr="barrido", dur=0.6, dirx=-1)
        self.plano(self.t_ayuda - 0.35, self.p_ayuda, tr="relampago", dur=0.6)

    def p_fecha(self, h, t, u):
        h.camara(1.03 + 0.03 * u, 960, 540, 0.0)
        M27.despacho().pegar(h, 1.0)
        K.calendario(h, t, self.t_ocho, "JULIO", "8", "2026", cx=960, cy=480, s=0.8)
        C.banda(h, "8 DE JULIO · 23:00 UTC", 960, 800, 76, t, self.t_ocho, sem=51)
        h.luz_radial(960, 500, 700, (1.2, 1.2, 1.2), k=2.2)
        return h.acabado(t)

    def p_carpeta(self, h, t, u):
        h.camara(1.05 + 0.04 * u, 960, 540, 0.0)
        M27.laboratorio().pegar(h, 1.0)
        K.carpeta(h, 960, 540, s=0.85, titulo="AYUDA", t=t, t0=self.t_escribe, sub="CARPETA")
        C.banda(h, "NOMBRE DE CARPETA", 960, 500, 80, t, self.t_escribe + 0.3, sem=53)
        h.luz_radial(960, 480, 750, (1.1, 1.1, 1.1), k=2.0)
        return h.acabado(t)

    def p_ayuda(self, h, t, u):
        h.camara(1.02 + 0.03 * u, 960, 540, 0.0)
        MU.oficina().pegar(h, 1.0, dx=-120)
        C.banda(h, "UN GRITO PIDIENDO AYUDA", 960, 480, 88, t, self.t_ayuda, claro=True, sem=55)
        N.gotas_vidrio(h, t, (100, -350, 1850, 400), n=75, k=0.7)
        h.luz_radial(960, 480, 800, (1.3, 1.3, 1.3), k=2.4)
        return h.acabado(t)
