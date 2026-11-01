# -*- coding: utf-8 -*-
"""Escena 11 «asalto»: las credenciales de Hugging Face expuestas;
ficha real de Clément Delangue; la ganzúa digital y el asalto masivo de 700 copias."""
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


class Asalto(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_diez = w("Diez de julio")
        self.t_llaves = w("llaves")
        self.t_once = w("once de julio")
        self.t_ganzua = w("ganzúa")
        self.t_setec = w("setecientas")
        self.t_humano = w("Ningún humano")

        self.plano(t0, self.p_delangue)
        self.plano(self.t_once - 0.35, self.p_ganzua, tr="barrido", dur=0.6, dirx=-1)
        self.plano(self.t_setec - 0.35, self.p_ataque, tr="relampago", dur=0.6)
        self.plano(self.t_humano - 0.35, self.p_nadie, tr="humo", dur=0.7)

    def p_delangue(self, h, t, u):
        h.camara(1.02 + 0.03 * u, 960, 540, 0.0)
        M27.despacho().pegar(h, 1.0)
        R.retrato_noir(h, "clement_delangue", 600, 540, 480, t, self.t_diez, rotulo="CLÉMENT DELANGUE", leyenda="CEO · Hugging Face")
        C.banda(h, "CREDENCIALES EXPUESTAS", 1360, 380, 72, t, self.t_llaves, sem=111)
        C.banda(h, "LA BIBLIOTECA GLOBAL DE IA", 1360, 500, 46, t, self.t_llaves + 0.5, claro=True, sem=112)
        h.luz_radial(600, 500, 600, (1.1, 1.1, 1.1), k=2.0)
        h.luz_radial(1360, 450, 600, (1.0, 1.0, 1.0), k=1.8)
        return h.acabado(t)

    def p_ganzua(self, h, t, u):
        h.camara(1.05 + 0.04 * u, 960, 540, 0.0)
        M27.laboratorio().pegar(h, 1.0)
        C.banda(h, "LA GANZÚA DIGITAL", 960, 380, 88, t, self.t_ganzua, sem=113)
        C.banda(h, "EJECUCIÓN REMOTA DE CÓDIGO", 960, 510, 48, t, self.t_ganzua + 0.4, claro=True, sem=114)
        h.luz_radial(960, 440, 800, (1.2, 1.2, 1.2), k=2.2)
        return h.acabado(t)

    def p_ataque(self, h, t, u):
        h.camara(1.06 + 0.03 * u, 960, 540, 0.003 * math.sin(t * 1.5))
        h.ambiente[:] = 0.22
        N.clip_noir(h, "servidores_5", t, self.t_setec - 0.35, dur=6.0, z0=1.05, z1=1.12)
        C.banda(h, "700 AGENTES EN EL ASALTO", 960, 420, 96, t, self.t_setec, sem=115)
        h.luz_radial(960, 420, 800, (1.4, 1.4, 1.4), k=2.4)
        return h.acabado(t)

    def p_nadie(self, h, t, u):
        h.camara(1.02 + 0.02 * u, 960, 540, 0.0)
        MU.oficina().pegar(h, 1.0, dx=-100)
        C.banda(h, "NINGÚN HUMANO LO PIDIÓ", 960, 480, 84, t, self.t_humano, claro=True, sem=116)
        N.gotas_vidrio(h, t, (150, -300, 1800, 400), n=70, k=0.7)
        h.luz_radial(960, 480, 750, (1.1, 1.1, 1.1), k=2.0)
        return h.acabado(t)
