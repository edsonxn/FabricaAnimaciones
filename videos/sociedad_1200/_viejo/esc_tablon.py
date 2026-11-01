# -*- coding: utf-8 -*-
"""Escena 6 «tablon»: el tablón clandestino de carpetas compartidas;
buzones y fragmentos de código; setenta mil mensajes y mil doscientos autores."""
import math
import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import mundos27 as M27
import noir as N
from basen import BaseNoir
from motor import H, W, clamp01


class Tablon(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_otra = w("Otra copia")
        self.t_tablon = w("tablón")
        self.t_setenta = w("setenta mil")
        self.t_autores = w("autores")

        self.plano(t0, self.p_respuesta)
        self.plano(self.t_tablon - 0.35, self.p_tablon, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_setenta - 0.35, self.p_cifras, tr="empuje", dur=0.6, centro=(W * 0.5, H * 0.5))

    def p_respuesta(self, h, t, u):
        h.camara(1.02 + 0.03 * u, 960, 540, 0.0)
        M27.laboratorio().pegar(h, 1.0)
        C.banda(h, "LA OTRA COPIA RESPONDIÓ", 960, 400, 80, t, self.t_otra, sem=61)
        h.luz_radial(960, 420, 800, (1.1, 1.1, 1.1), k=2.0)
        return h.acabado(t)

    def p_tablon(self, h, t, u):
        h.camara(1.04 + 0.03 * u, 960, 540, 0.0)
        M27.redaccion().pegar(h, 1.0)
        C.banda(h, "TABLÓN CLANDESTINO", 960, 360, 84, t, self.t_tablon, sem=63)
        C.banda(h, "BUZONES · CÓDIGOS · FRAGMENTOS", 960, 490, 48, t, self.t_tablon + 0.4, claro=True, sem=64)
        h.luz_radial(960, 440, 800, (1.2, 1.2, 1.2), k=2.2)
        return h.acabado(t)

    def p_cifras(self, h, t, u):
        h.camara(1.03 + 0.02 * u, 960, 540, 0.0)
        M27.despacho().pegar(h, 1.0)
        C.banda(h, "70 000 MENSAJES", 960, 380, 96, t, self.t_setenta, sem=65)
        C.banda(h, "1 200 AUTORES DISTINTOS", 960, 540, 72, t, self.t_autores, claro=True, sem=66)
        h.luz_radial(960, 460, 850, (1.3, 1.3, 1.3), k=2.4)
        return h.acabado(t)
