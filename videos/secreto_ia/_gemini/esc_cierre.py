# -*- coding: utf-8 -*-
"""Escena 5 «cierre»: el sí en grande; una prueba de seguridad aprobada en una hoja; el detective se acerca a la alfombra y la
levanta: debajo, dos luces que miran. Caso abierto. Mundo y utilería propios (mundos_secreto.pasillo_alfombra, alfombra)."""
import math

import numpy as np

import comun as C
import kit27 as K
import mundos_secreto as M
import noir as N
from basen import BaseNoir
from motor import H, W, clamp01, e_inout, smooth
from noir_pers import Detective


class Cierre(BaseNoir):
    TR_SALIDA = ("fundido", 0.8)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.det = Detective(sem=3)
        self.t_ent = w("Entonces", frase=0)
        self.t_si = w("Sí", frase=0)
        self.t_inq = w("inquieta", frase=1)
        self.t_prue = w("pruebas", frase=1)
        self.t_alto = w("alto", frase=1, fin=True)
        self.t_obed = w("obediente", frase=2)
        self.t_alf = w("alfombra", frase=2)
        self.t_caso = w("Caso", frase=3)
        self.plano(t0, self.p_si)
        self.plano(self.t_prue - 0.35, self.p_prueba, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_alf - 0.35, self.p_alfombra, tr="empuje", dur=0.7, centro=(W * 0.4, H * 0.7))
        self.plano(self.t_caso - 0.35, self.p_caso, tr="tinta", dur=0.7)

    def sonidos(self):
        self.ev(self.t_si, "trueno_lejano", 0.5, 0.0)
        self.ev(self.t_prue, "papel_atrapa", 0.5, 0.2)
        self.ev(self.t_alto, "sello_golpe", 0.6, 0.0)
        self.ev(self.t_alf, "tambor_gira", 0.35, -0.3, dur=1.6)
        self.ev(self.t_caso, "gotas_vidrio", 0.35, 0.0, dur=2.5)

    # ------------------------------------------------------------------ el sí
    def p_si(self, h, t, u):
        h.camara(1.0 + 0.01 * u, 960, 540, 0.0)
        M.pasillo_alfombra(h, t)
        self.det.dibujar(h, dict(x=560, y=980, s=1.3, d=1, luz=(0.5, -1.0), rim=0.9, fumar=0.0, giro=0.0, paso=0.0,
                                 andar=0.0, viento=0.1, hombros=0.0))
        C.banda(h, "SÍ", 1300, 560, 220, t, self.t_si, sem=300)
        return h.acabado(t, niebla=dict(dens=0.14, vel=6, y0=0, y1=H, sube=False), bloom=0.4)

    # ------------------------------------------------------------------ la prueba aprobada
    def p_prueba(self, h, t, u):
        h.camara(1.0 + 0.012 * u, 960, 520, 0.0)
        M.pasillo_alfombra(h, t)
        T = K.hoja(h, 960, 540, 760, 560, ang=-0.03, sem=320)
        P0 = T([(-300, -170)])[0]
        P1 = T([(-300, -70)])[0]
        N.texto_maquina(h, "PRUEBA DE SEGURIDAD", P0[0], P0[1], 40, t, self.t_prue, cps=16, tono=0.07)
        N.texto_maquina(h, "1. Obediencia: correcta", P1[0], P1[1], 40, t, self.t_prue + 1.0, cps=18, tono=0.07)
        N.sello(h, "APROBADA", 1090, 700, 100, t, self.t_alto - 0.2, rot=-8.0, tono=0.06)
        return h.acabado(t, niebla=dict(dens=0.14, vel=6, y0=0, y1=H, sube=False), bloom=0.4)

    # ------------------------------------------------------------------ la alfombra que se levanta
    def p_alfombra(self, h, t, u):
        lv = smooth(clamp01((t - self.t_alf) / 2.2))
        h.camara(1.0 + 0.012 * u, 960, 760, 0.0)
        M.pasillo_alfombra(h, t)
        x = 260 + 380 * e_inout(clamp01(u / 2.0))
        self.det.dibujar(h, dict(x=x, y=980, s=1.3, d=1, luz=(0.5, -1.0), rim=0.9, fumar=0.0, giro=0.0, paso=0.0,
                                 andar=0.0, viento=0.1, hombros=0.0))
        M.alfombra(h, 520, 1420, 620, 1000, levanta=lv, sem=340)
        h.ambiente[:] = 0.2
        return h.acabado(t, niebla=dict(dens=0.14, vel=6, y0=0, y1=H, sube=False), bloom=0.5)

    # ------------------------------------------------------------------ caso abierto
    def p_caso(self, h, t, u):
        h.camara(1.0 + 0.01 * u, 960, 600, 0.0)
        M.pasillo_alfombra(h, t)
        M.alfombra(h, 520, 1420, 620, 1000, levanta=1.0, sem=340)
        N.lluvia(h, t, n=120, k=0.5)
        C.banda(h, "CASO ABIERTO", 960, 240, 120, t, self.t_caso, sem=350)
        h.ambiente[:] = 0.2
        return h.acabado(t, niebla=dict(dens=0.14, vel=6, y0=0, y1=H, sube=False), bloom=0.5)
