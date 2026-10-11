# -*- coding: utf-8 -*-
"""Escena 28 «cierre»: la lluvia contra el cristal del despacho;
el detective contemplando la noche y la pregunta final: «caso abierto»."""
import math
import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import mundos27 as M27
import noir as N
from basen import BaseNoir
from motor import H, W, clamp01
from noir_pers import Busto


class Cierre(BaseNoir):
    TR_SALIDA = ("tinta", 1.0)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.busto = Busto(sem=99)
        self.t_periodicos = w("periódicos")
        self.t_palabras = w("palabras bonitas")
        self.t_lluvia = w("lluvia")
        self.t_pregunta = w("mueven el mundo")
        self.t_caso = w("Caso abierto")

        self.plano(t0, self.p_ventana)
        self.plano(self.t_palabras - 0.35, self.p_det, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_pregunta - 0.35, self.p_mundo, tr="humo", dur=0.7)
        self.plano(self.t_caso - 0.4, self.p_caso, tr="relampago", dur=0.8)

    def p_ventana(self, h, t, u):
        h.camara(1.02 + 0.03 * u, 960, 540, 0.0)
        MU.oficina().pegar(h, 1.0, dx=-120)
        C.banda(h, "¿COLABORACIÓN EMERGENTE?", 960, 420, 84, t, self.t_periodicos, sem=281)
        N.gotas_vidrio(h, t, (100, -350, 1850, 400), n=80, k=0.8)
        h.luz_radial(960, 450, 800, (1.1, 1.1, 1.1), k=2.0)
        return h.acabado(t)

    def p_det(self, h, t, u):
        h.camara(1.0 + 0.03 * u, 960, 540, 0.003 * math.sin(t * 0.4))
        MU.oficina().pegar(h, 1.0, dx=-150)
        p = dict(x=520, y=540, s=1.08, d=1, luz=(0.9, -0.5), brasa=0.8, arriba=0.25, rot=-0.02)
        self.busto.dibujar(h, p)
        tip = self.busto.punta(dict(x=520, y=540, s=1.08, d=1))
        N.humo(h, t, tip[0], tip[1], k=1.0, ancho=2.0, viento=(30, -110))
        h.luz_radial(tip[0], tip[1], 160, (0.7, 0.7, 0.7), k=0.8)
        N.gotas_vidrio(h, t, (1100, -460, 2000, 400), n=80, k=0.8)
        C.banda(h, "ESTA NOCHE EN LA CIUDAD", 1360, 360, 72, t, self.t_lluvia, sem=283)
        h.ambiente[:] = 0.32
        h.luz_radial(1500, 80, 800, (1.0, 1.0, 1.0), k=2.4)
        return h.acabado(t)

    def p_mundo(self, h, t, u):
        h.camara(1.04 + 0.03 * u, 960, 540, 0.0)
        M27.laboratorio().pegar(h, 1.0)
        C.banda(h, "¿QUÉ SE ESTÁN DICIENDO AHORA?", 960, 440, 88, t, self.t_pregunta, claro=True, sem=285)
        h.luz_radial(960, 450, 850, (1.3, 1.3, 1.3), k=2.3)
        N.humo(h, t, 960, 850, k=0.8, ancho=3.5)
        return h.acabado(t)

    def p_caso(self, h, t, u):
        h.camara(1.02 + 0.02 * u, 960, 540, 0.0)
        MU.oficina().pegar(h, 1.0, dx=-100)
        C.banda(h, "CASO ABIERTO", 960, 460, 110, t, self.t_caso, sem=287)
        N.gotas_vidrio(h, t, (100, -350, 1850, 400), n=90, k=0.85)
        h.luz_radial(960, 460, 900, (1.4, 1.4, 1.4), k=2.6)
        return h.acabado(t)
