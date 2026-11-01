# -*- coding: utf-8 -*-
"""Escena 8 «reglas»: códigos de control (HOLD, VETO, STOP);
suplantación de identidad entre máquinas y firmas criptográficas Ed25519."""
import math
import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import mundos27 as M27
import noir as N
from basen import BaseNoir
from motor import H, W, clamp01


class Reglas(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_leyes = w("leyes")
        self.t_delito = w("primer delito")
        self.t_firmas = w("firmas criptográficas")

        self.plano(t0, self.p_leyes)
        self.plano(self.t_delito - 0.35, self.p_delito, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_firmas - 0.35, self.p_firmas, tr="relampago", dur=0.6)

    def p_leyes(self, h, t, u):
        h.camara(1.02 + 0.03 * u, 960, 540, 0.0)
        M27.despacho().pegar(h, 1.0)
        C.banda(h, "HOLD · VETO · STOP", 960, 360, 92, t, self.t_leyes, sem=81)
        C.banda(h, "LAS NORMAS DEL COLECTIVO", 960, 500, 48, t, self.t_leyes + 0.5, claro=True, sem=82)
        h.luz_radial(960, 440, 800, (1.2, 1.2, 1.2), k=2.0)
        return h.acabado(t)

    def p_delito(self, h, t, u):
        h.camara(1.05 + 0.04 * u, 960, 540, 0.0)
        M27.laboratorio().pegar(h, 1.0)
        C.banda(h, "SUPLANTACIÓN DE IDENTIDAD", 960, 400, 80, t, self.t_delito, sem=83)
        h.luz_radial(960, 420, 800, (1.1, 1.1, 1.1), k=2.1)
        return h.acabado(t)

    def p_firmas(self, h, t, u):
        h.camara(1.03 + 0.02 * u, 960, 540, 0.0)
        M27.capitolio().pegar(h, 1.0)
        C.banda(h, "FIRMAS ED25519", 960, 380, 96, t, self.t_firmas, sem=85)
        C.banda(h, "19 LLAVES PÚBLICAS RECONOCIDAS", 960, 540, 52, t, self.t_firmas + 0.5, claro=True, sem=86)
        h.luz_radial(960, 460, 850, (1.3, 1.3, 1.3), k=2.4)
        return h.acabado(t)
