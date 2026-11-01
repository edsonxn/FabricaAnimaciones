# -*- coding: utf-8 -*-
"""Escena 13 «caso_2017»: viaje al año 2017 en Menlo Park;
ficha real de Mark Zuckerberg; los agentes Bob y Alice negociando objetos."""
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


class Caso2017(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_vet = w("veteranos")
        self.t_menlo = w("Menlo Park")
        self.t_2017 = w("Año 2017")
        self.t_bob = w("Bob y Alice")
        self.t_sombreros = w("sombreros")

        self.plano(t0, self.p_menlo)
        self.plano(self.t_2017 - 0.35, self.p_zuck, tr="barrido", dur=0.6, dirx=-1)
        self.plano(self.t_sombreros - 0.35, self.p_mision, tr="humo", dur=0.7)

    def p_menlo(self, h, t, u):
        h.camara(1.02 + 0.03 * u, 960, 540, 0.0)
        M27.capitolio().pegar(h, 1.0)
        C.banda(h, "MENLO PARK · 2017", 960, 360, 88, t, self.t_menlo, sem=131)
        C.banda(h, "FACEBOOK AI RESEARCH", 960, 500, 52, t, self.t_menlo + 0.5, claro=True, sem=132)
        h.luz_radial(960, 420, 800, (1.1, 1.1, 1.1), k=2.0)
        return h.acabado(t)

    def p_zuck(self, h, t, u):
        h.camara(1.04 + 0.03 * u, 960, 540, 0.0)
        M27.despacho().pegar(h, 1.0)
        R.retrato_noir(h, "mark_zuckerberg", 600, 540, 480, t, self.t_2017, rotulo="MARK ZUCKERBERG", leyenda="Facebook · Menlo Park")
        C.banda(h, "BOB Y ALICE", 1360, 380, 84, t, self.t_bob, sem=133)
        C.banda(h, "AGENTES AUTÓNOMOS DE NEGOCIACIÓN", 1360, 500, 42, t, self.t_bob + 0.5, claro=True, sem=134)
        h.luz_radial(600, 500, 600, (1.1, 1.1, 1.1), k=2.0)
        h.luz_radial(1360, 450, 600, (1.0, 1.0, 1.0), k=1.8)
        return h.acabado(t)

    def p_mision(self, h, t, u):
        h.camara(1.02 + 0.02 * u, 960, 540, 0.0)
        M27.laboratorio().pegar(h, 1.0)
        C.banda(h, "NEGOCIACIÓN EN LENGUAJE NATURAL", 960, 420, 76, t, self.t_sombreros, sem=135)
        h.luz_radial(960, 450, 800, (1.2, 1.2, 1.2), k=2.2)
        return h.acabado(t)
