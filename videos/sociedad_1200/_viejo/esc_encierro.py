# -*- coding: utf-8 -*-
"""Escena 2 «encierro»: San Francisco, los cuarteles de OpenAI; ficha con la foto real de Sam Altman;
el gimnasio de hackeo ExploitGym con racks de servidores."""
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


class Encierro(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_sf = w("San Francisco")
        self.t_prot = w("prototipo")
        self.t_hack = w("hackeo")
        self.t_decenas = w("Decenas")

        self.plano(t0, self.p_sf)
        self.plano(self.t_prot - 0.35, self.p_altman, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_hack - 0.35, self.p_gym, tr="humo", dur=0.7)
        self.plano(self.t_decenas - 0.35, self.p_copias, tr="empuje", dur=0.6, centro=(W * 0.5, H * 0.5))

    def p_sf(self, h, t, u):
        h.camara(1.02 + 0.03 * u, 960, 540, 0.0)
        M27.capitolio().pegar(h, 1.0)
        C.banda(h, "SAN FRANCISCO", 960, 320, 84, t, self.t_sf, sem=21)
        C.banda(h, "LABORATORIOS OPENAI", 960, 460, 52, t, self.t_sf + 0.5, claro=True, sem=22)
        h.luz_radial(960, 300, 800, (1.0, 1.0, 1.0), k=2.0)
        N.gotas_vidrio(h, t, (100, -300, 1900, 400), n=80, k=0.7)
        return h.acabado(t)

    def p_altman(self, h, t, u):
        h.camara(1.04 + 0.02 * u, 960, 540, 0.0)
        M27.despacho().pegar(h, 1.0)
        R.retrato_noir(h, "sam_altman", 600, 540, 480, t, self.t_prot, rotulo="SAM ALTMAN", leyenda="OpenAI · San Francisco")
        C.banda(h, "MODELO INTERNO SECRETO", 1360, 400, 68, t, self.t_prot + 0.3, sem=24)
        C.banda(h, "PROTOTIPO DE INVESTIGACIÓN", 1360, 520, 44, t, self.t_prot + 0.7, claro=True, sem=25)
        h.luz_radial(600, 500, 600, (1.1, 1.1, 1.1), k=2.0)
        h.luz_radial(1360, 460, 600, (1.0, 1.0, 1.0), k=1.8)
        return h.acabado(t)

    def p_gym(self, h, t, u):
        h.camara(1.0 + 0.04 * u, 960, 540, 0.0)
        M27.laboratorio().pegar(h, 1.0)
        C.banda(h, "GIMNASIO DE HACKEO", 960, 360, 88, t, self.t_hack, sem=26)
        C.banda(h, "EXPLOITGYM · BANCO DE PRUEBAS", 960, 500, 48, t, self.t_hack + 0.5, claro=True, sem=27)
        h.luz_radial(960, 400, 900, (1.2, 1.2, 1.2), k=2.2)
        N.humo(h, t, 960, 850, k=0.8, ancho=3.0)
        return h.acabado(t)

    def p_copias(self, h, t, u):
        h.camara(1.06 + 0.03 * u, 960, 540, 0.0)
        M27.fabrica().pegar(h, 1.0)
        C.banda(h, "DECENAS DE MILES DE COPIAS", 960, 420, 80, t, self.t_decenas, sem=28)
        C.banda(h, "CORRIENDO EN PARALELO", 960, 550, 46, t, self.t_decenas + 0.5, claro=True, sem=29)
        h.luz_radial(960, 450, 800, (1.1, 1.1, 1.1), k=2.2)
        return h.acabado(t)
