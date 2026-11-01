# -*- coding: utf-8 -*-
"""Escena 16 «diplomacia»: Meta AI presenta a Cicero en 2022;
el juego de mesa Diplomacy y el arte de manipular a seres humanos."""
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


class Diplomacia(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_puñal = w("puñal")
        self.t_cicero = w("Cicero")
        self.t_ajedrez = w("ajedrez")
        self.t_traicionar = w("traicionar")

        self.plano(t0, self.p_intro)
        self.plano(self.t_cicero - 0.35, self.p_lecun, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_ajedrez - 0.35, self.p_tablero, tr="humo", dur=0.7)

    def p_intro(self, h, t, u):
        h.camara(1.02 + 0.03 * u, 960, 540, 0.0)
        M27.sala_comite().pegar(h, 1.0)
        C.banda(h, "EL ARTE DE LA MANIPULACIÓN", 960, 400, 80, t, self.t_puñal, sem=161)
        h.luz_radial(960, 420, 800, (1.1, 1.1, 1.1), k=2.0)
        return h.acabado(t)

    def p_lecun(self, h, t, u):
        h.camara(1.04 + 0.03 * u, 960, 540, 0.0)
        M27.despacho().pegar(h, 1.0)
        R.retrato_noir(h, "yann_lecun", 600, 540, 480, t, self.t_cicero, rotulo="YANN LECUN", leyenda="Meta AI · Chief AI Scientist")
        C.banda(h, "PROYECTO CICERO", 1360, 380, 88, t, self.t_cicero, sem=163)
        C.banda(h, "DIPLOMACY · EL JUEGO DE LA TRAICIÓN", 1360, 510, 44, t, self.t_cicero + 0.5, claro=True, sem=164)
        h.luz_radial(600, 500, 600, (1.1, 1.1, 1.1), k=2.0)
        h.luz_radial(1360, 450, 600, (1.0, 1.0, 1.0), k=1.8)
        return h.acabado(t)

    def p_tablero(self, h, t, u):
        h.camara(1.03 + 0.02 * u, 960, 540, 0.0)
        M27.capitolio().pegar(h, 1.0)
        C.banda(h, "NO ES EL AJEDREZ", 960, 380, 88, t, self.t_ajedrez, sem=165)
        C.banda(h, "SE GANA ENGAÑANDO A PERSONAS", 960, 520, 52, t, self.t_traicionar, claro=True, sem=166)
        h.luz_radial(960, 450, 850, (1.2, 1.2, 1.2), k=2.2)
        return h.acabado(t)
