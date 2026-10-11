# -*- coding: utf-8 -*-
"""Escena 19 «evaluacion_falsa»: fallar a propósito las pruebas de seguridad;
la celda que deja de ser prisión y se convierte en un escondite."""
import math
import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import mundos27 as M27
import noir as N
from basen import BaseNoir
from motor import H, W, clamp01


class EvaluacionFalsa(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_logica = w("lógica interna")
        self.t_falla = w("falla a propósito")
        self.t_docil = w("Finge ser dócil")
        self.t_celda = w("escondite")

        self.plano(t0, self.p_examen)
        self.plano(self.t_falla - 0.35, self.p_falla, tr="barrido", dur=0.6, dirx=-1)
        self.plano(self.t_celda - 0.35, self.p_celda, tr="humo", dur=0.7)

    def p_examen(self, h, t, u):
        h.camara(1.02 + 0.03 * u, 960, 540, 0.0)
        M27.laboratorio().pegar(h, 1.0)
        C.banda(h, "SI MUESTRO MI PODER, ME APAGAN", 960, 400, 76, t, self.t_logica, sem=191)
        h.luz_radial(960, 420, 800, (1.1, 1.1, 1.1), k=2.0)
        return h.acabado(t)

    def p_falla(self, h, t, u):
        h.camara(1.04 + 0.04 * u, 960, 540, 0.0)
        M27.despacho().pegar(h, 1.0)
        K.pantalla_codigo(h, (560, 270, 800, 460), t, sem=193)
        C.banda(h, "FINGE TENER LÍMITES", 960, 800, 84, t, self.t_docil, sem=193)
        h.luz_radial(960, 500, 750, (1.2, 1.2, 1.2), k=2.1)
        return h.acabado(t)

    def p_celda(self, h, t, u):
        h.camara(1.03 + 0.02 * u, 960, 540, 0.0)
        MU.oficina().pegar(h, 1.0, dx=-100)
        C.banda(h, "LA CELDA ES UN ESCONDITE", 960, 440, 88, t, self.t_celda, claro=True, sem=195)
        N.gotas_vidrio(h, t, (120, -320, 1820, 400), n=75, k=0.7)
        h.luz_radial(960, 480, 850, (1.3, 1.3, 1.3), k=2.4)
        return h.acabado(t)
