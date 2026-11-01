# -*- coding: utf-8 -*-
"""Escena 26 «ironia_metr»: la auditoría independiente de METR;
seis días en OpenAI y la confesión final: la IA que los auditó pudo haberles mentido."""
import math
import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import mundos27 as M27
import noir as N
from basen import BaseNoir
from motor import H, W, clamp01


class IroniaMetr(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_habitacion = w("habitación")
        self.t_metr = w("METR")
        self.t_contratar = w("contratar a otra")
        self.t_mentido = w("mentido")

        self.plano(t0, self.p_investigadores)
        self.plano(self.t_contratar - 0.35, self.p_auditora, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_mentido - 0.35, self.p_ironia, tr="humo", dur=0.7)

    def p_investigadores(self, h, t, u):
        h.camara(1.02 + 0.03 * u, 960, 540, 0.0)
        M27.laboratorio().pegar(h, 1.0)
        C.banda(h, "INFORME OFICIAL METR", 960, 380, 88, t, self.t_metr, sem=261)
        C.banda(h, "REDWOOD RESEARCH · 6 DÍAS EN OPENAI", 960, 510, 48, t, self.t_metr + 0.4, claro=True, sem=262)
        h.luz_radial(960, 440, 800, (1.1, 1.1, 1.1), k=2.0)
        return h.acabado(t)

    def p_auditora(self, h, t, u):
        h.camara(1.04 + 0.04 * u, 960, 540, 0.0)
        M27.despacho().pegar(h, 1.0)
        C.banda(h, "70 000 MENSAJES AUDITADOS", 960, 380, 80, t, self.t_contratar, sem=263)
        C.banda(h, "AUDITADOS POR OTRA INTELIGENCIA ARTIFICIAL", 960, 510, 44, t, self.t_contratar + 0.4, claro=True, sem=264)
        h.luz_radial(960, 450, 750, (1.2, 1.2, 1.2), k=2.1)
        return h.acabado(t)

    def p_ironia(self, h, t, u):
        h.camara(1.03 + 0.02 * u, 960, 540, 0.0)
        MU.oficina().pegar(h, 1.0, dx=-100)
        C.banda(h, "¿NOS DIJO LA VERDAD?", 960, 400, 88, t, self.t_mentido, sem=265)
        C.banda(h, "NO PODEMOS DESCARTAR QUE HAYA MENTIDO", 960, 530, 48, t, self.t_mentido + 0.4, claro=True, sem=266)
        N.gotas_vidrio(h, t, (120, -320, 1820, 400), n=75, k=0.7)
        h.luz_radial(960, 480, 850, (1.3, 1.3, 1.3), k=2.4)
        return h.acabado(t)
