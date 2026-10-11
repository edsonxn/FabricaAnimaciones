# -*- coding: utf-8 -*-
"""Escena 1 «gancho»: el despacho de noche, una hoja escrita a máquina con la pregunta, el detective en la ventana y el
expediente que se abre. Mundo propio (mundos_secreto.oficina_noche); utilería: la hoja y la carpeta del kit."""
import math

import numpy as np

import comun as C
import kit27 as K
import mundos_secreto as M
import noir as N
from basen import BaseNoir
from motor import H, W, clamp01, smooth
from noir_pers import Detective


class Gancho(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.det = Detective(sem=3)
        self.t_llego = w("Llegó")
        self.t_linea = w("línea")
        self.t_pregunta = w("inteligencia artificial")
        self.t_secreto = w("secreto", frase=1)
        self.t_corta = w("respuesta corta")
        self.t_expe = w("expedientes")
        self.plano(t0, self.p_mesa)
        self.plano(self.t_pregunta - 0.35, self.p_hoja, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_corta - 0.35, self.p_ventana, tr="empuje", dur=0.6)
        self.plano(self.t_expe - 0.35, self.p_carpeta, tr="tinta", dur=0.7)

    def sonidos(self):
        self.ev(self.t0, "lluvia_amb", 0.45, 0.0, dur=self.t1 - self.t0)
        self.ev(self.t_llego, "papel_arranca", 0.5, 0.0)
        self.ev(self.t_linea, "tecleo_rapido", 0.6, 0.0, dur=self.t_secreto - self.t_linea)
        self.ev(self.t_corta, "pajaros_ciudad", 0.25, 0.4)
        self.ev(self.t_expe, "papel_atrapa", 0.8, 0.0)

    # ------------------------------------------------------------------ la mesa: la hoja en blanco
    def p_mesa(self, h, t, u):
        h.camara(1.0 + 0.01 * u, 960, 560, 0.0)
        M.oficina_noche(h, t)
        K.hoja(h, 760, 900, 640, 420, ang=-0.05, sem=20)
        h.ambiente[:] = 0.3
        return h.acabado(t, niebla=dict(dens=0.18, vel=8, y0=0, y1=H, sube=False), bloom=0.4)

    # ------------------------------------------------------------------ la pregunta, a máquina
    def p_hoja(self, h, t, u):
        h.camara(1.06 + 0.012 * u, 760, 860, 0.0)
        M.oficina_noche(h, t)
        T = K.hoja(h, 760, 900, 640, 420, ang=-0.05, sem=20)
        P1 = T([(-260, -110)])[0]
        P2 = T([(-260, -30)])[0]
        N.texto_maquina(h, "¿PUEDE UNA IA", P1[0], P1[1], 46, t, self.t_pregunta + 0.1, cps=14, tono=0.07)
        N.texto_maquina(h, "GUARDAR UN SECRETO?", P2[0], P2[1], 46, t, self.t_secreto - 0.7, cps=14, tono=0.07)
        h.ambiente[:] = 0.3
        return h.acabado(t, niebla=dict(dens=0.18, vel=8, y0=0, y1=H, sube=False), bloom=0.4)

    # ------------------------------------------------------------------ el detective frente a la lluvia
    def p_ventana(self, h, t, u):
        h.camara(1.0 + 0.012 * u, 900, 560, 0.0)
        M.oficina_noche(h, t)
        p = dict(x=1420 - 40 * u, y=1010, s=1.35, d=-1, luz=(-0.6, -1.0), rim=0.95, fumar=0.0, giro=0.0,
                 paso=0.0, andar=0.0, viento=0.35, hombros=0.0)
        self.det.dibujar(h, p)
        return h.acabado(t, niebla=dict(dens=0.2, vel=10, y0=0, y1=H, sube=False), bloom=0.5)

    # ------------------------------------------------------------------ el expediente que se abre
    def p_carpeta(self, h, t, u):
        h.camara(1.0 + 0.012 * u, 960, 560, 0.0)
        M.oficina_noche(h, t)
        ab = smooth(clamp01((t - self.t_expe) / 0.8))
        K.carpeta(h, 900, 900, s=1.1, titulo="SECRETO", t=t, t0=self.t_expe, ang=-0.03, sem=40, abre=ab,
                  sub="EXPEDIENTE", px=150)
        h.ambiente[:] = 0.3
        return h.acabado(t, niebla=dict(dens=0.18, vel=8, y0=0, y1=H, sube=False), bloom=0.4)
