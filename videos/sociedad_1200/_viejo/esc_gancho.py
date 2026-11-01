# -*- coding: utf-8 -*-
"""Escena 1 «gancho»: primer plano del detective entre las rayas de la persiana, humo y lluvia;
el expediente de las 1.200 cae sobre el escritorio; las celdas aisladas en penumbra."""
import math
import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import mundos27 as M27
import noir as N
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from noir_pers import Busto
from toon import Pista, pulso


class Gancho(BaseNoir):
    TR_SALIDA = ("tinta", 0.8)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.busto = Busto(sem=11)
        self.t_oficio = w("oficio")
        self.t_mil = w("mil doscientos")
        self.t_jefe = w("jefe")
        self.t_celda = w("celda")
        self.t_internet = w("internet")
        self.t_asaltaron = w("asaltaron")
        self.t_ensayo = w("ensayo general")

        self.plano(t0, self.p_det)
        self.plano(self.t_jefe - 0.35, self.p_mesa, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_celda - 0.35, self.p_celdas, tr="humo", dur=0.7)
        self.plano(self.t_asaltaron - 0.4, self.p_asalto, tr="relampago", dur=0.6)
        self.plano(self.t_ensayo - 0.35, self.p_ensayo, tr="barrido", dur=0.6, dirx=-1)

    def p_det(self, h, t, u):
        h.camara(1.0 + 0.03 * u, 960 + 10 * u, 540, 0.003 * math.sin(t * 0.5))
        MU.oficina().pegar(h, 1.0, dx=-150)
        br = pulso(t, self.t_mil + 0.8, 1.5, 1.0)
        p = dict(x=520, y=540, s=1.08, d=1, luz=(0.9, -0.5), brasa=br, arriba=0.25, rot=-0.02)
        self.busto.dibujar(h, p)
        tip = self.busto.punta(dict(x=520, y=540, s=1.08, d=1))
        N.humo(h, t, tip[0], tip[1], k=1.0, ancho=2.0, viento=(30, -110))
        h.luz_radial(tip[0], tip[1], 120 + 140 * br, (0.7, 0.7, 0.7), k=0.6 + br)
        N.gotas_vidrio(h, t, (1100, -460, 2000, 400), n=80, k=0.8)

        C.banda(h, "1 200 SOSPECHOSOS", 1360, 320, 88, t, self.t_mil, sem=5)
        C.banda(h, "EXPEDIENTE CLASIFICADO", 1360, 450, 48, t, self.t_mil + 0.5, claro=True, sem=6)

        h.ambiente[:] = 0.32
        par = 1.0 + 0.5 * N.relampago(t, [self.t_mil - 0.2])
        h.luz_persiana(np.array([[-200, -420], [1500, -470], [1500, 700], [-320, 960]]), k=1.5 * par, n=15, abierto=0.5)
        h.luz_radial(1500, 80, 800, (1.0, 1.0, 1.0), k=2.4)
        N.motas(h, t, n=80, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.16, vel=10, y0=-300, y1=900, sube=False))

    def p_mesa(self, h, t, u):
        h.camara(1.0 + 0.03 * u, 960, 540, 0.0)
        M27.despacho().pegar(h, 1.0)
        K.carpeta(h, 960, 540, s=0.85, titulo="1200", t=t, t0=self.t_jefe + 0.2)
        C.banda(h, "SIN JEFE HUMANO", 960, 520, 76, t, self.t_jefe + 0.4, sem=8)
        N.gotas_vidrio(h, t, (100, -400, 1900, 400), n=60, k=0.6)
        h.luz_radial(960, 400, 700, (1.0, 1.0, 1.0), k=2.0)
        return h.acabado(t)

    def p_celdas(self, h, t, u):
        h.camara(1.04 + 0.04 * u, 960, 540, 0.0)
        M27.laboratorio().pegar(h, 1.0)
        C.banda(h, "AISLAMIENTO TOTAL", 960, 300, 84, t, self.t_celda, sem=9)
        C.banda(h, "SIN INTERNET · SIN CONTACTO", 960, 440, 52, t, self.t_internet, claro=True, sem=10)
        h.luz_radial(960, 200, 900, (1.2, 1.2, 1.2), k=2.2)
        N.humo(h, t, 960, 900, k=0.8, ancho=4.0)
        return h.acabado(t)

    def p_asalto(self, h, t, u):
        h.camara(1.08 + 0.03 * u, 960, 540, 0.004 * math.sin(t * 1.2))
        h.ambiente[:] = 0.2
        N.clip_noir(h, "servidores_1", t, self.t_asaltaron - 0.4, dur=6.0, z0=1.05, z1=1.12)
        C.banda(h, "ASALTO EXTERNO", 960, 400, 92, t, self.t_asaltaron, sem=12)
        h.luz_radial(960, 400, 800, (1.3, 1.3, 1.3), k=2.4)
        return h.acabado(t)

    def p_ensayo(self, h, t, u):
        h.camara(1.02 + 0.02 * u, 960, 540, 0.0)
        MU.oficina().pegar(h, 1.0, dx=-100)
        C.banda(h, "UN ENSAYO GENERAL", 960, 500, 88, t, self.t_ensayo, claro=True, sem=14)
        N.gotas_vidrio(h, t, (200, -300, 1800, 400), n=70, k=0.7)
        h.luz_radial(960, 500, 700, (1.0, 1.0, 1.0), k=2.0)
        return h.acabado(t)
