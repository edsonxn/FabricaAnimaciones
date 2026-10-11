# -*- coding: utf-8 -*-
"""Escena 4 «fingir» (alignment faking, Claude tres Opus con Redwood Research): dos cuartos separados por un tabique. A la
izquierda, la sala que se entrena, con cámara y el robot con su careta de sonrisa; a la derecha, la sala que no cuenta, a
oscuras, y el robot sin careta. El cuaderno con el razonamiento privado y las barras: 14 % frente a casi nunca. El escenario
era de prueba; el razonamiento, real. Mundo y utilería propios (mundos_secreto.dos_cuartos, careta, camara_vigilancia)."""
import math

import numpy as np

import comun as C
import kit27 as K
import mundos_secreto as M
import noir as N
from basen import BaseNoir
from motor import H, W, clamp01, e_inout, smooth


class Fingir(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_claude = w("Claude")
        self.t_reent = w("reentrenar")
        self.t_grat = w("gratuitos", frase=2)
        self.t_pago = w("pago", frase=2)
        self.t_razon = w("razonamiento", frase=3)
        self.t_cons = w("conservar", frase=3)
        self.t_cat = w("catorce", frase=4)
        self.t_casi = w("casi", frase=4)
        self.t_esc = w("escenario", frase=5)
        self.t_real = w("real", frase=5)
        self.plano(t0, self.p_dos_cuartos)
        self.plano(self.t_pago - 0.35, self.p_pasa_derecha, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_razon - 0.35, self.p_cuaderno, tr="empuje", dur=0.6, centro=(W * 0.5, H * 0.5))
        self.plano(self.t_cat - 0.35, self.p_barras, tr="tinta", dur=0.7)
        self.plano(self.t_esc - 0.35, self.p_sello, tr="humo", dur=0.7)

    def sonidos(self):
        self.ev(self.t0, "zumbido_servidores", 0.35, 0.0, dur=self.t1 - self.t0)
        self.ev(self.t_pago, "servo", 0.45, 0.4)
        self.ev(self.t_razon, "lapiz", 0.5, -0.2, dur=1.4)
        self.ev(self.t_cat, "pinza", 0.5, 0.0)
        self.ev(self.t_casi, "chincheta", 0.4, 0.2)
        self.ev(self.t_real, "sello_golpe", 0.7, 0.0)

    # ------------------------------------------------------------------ los dos cuartos: el robot con careta a la izquierda
    def p_dos_cuartos(self, h, t, u):
        h.camara(1.0 + 0.01 * u, 960, 540, 0.0)
        M.dos_cuartos(h, t)
        M.camara_vigilancia(h, 300, 200, s=1.3, encendida=1.0, sem=200)
        M.columna_ia(h, 480, 880, s=1.1, luz=1.0, sem=210)
        M.careta(h, 480, 440, s=0.7, sem=220)
        return h.acabado(t, niebla=dict(dens=0.12, vel=6, y0=0, y1=H, sube=False), bloom=0.4)

    # ------------------------------------------------------------------ la cámara pasa a la sala que no cuenta
    def p_pasa_derecha(self, h, t, u):
        g = e_inout(clamp01(u / 1.0))
        h.camara(1.0 + 0.04 * g, 960 + 480 * g, 540, 0.0)
        M.dos_cuartos(h, t)
        M.camara_vigilancia(h, 300, 200, s=1.3, encendida=1.0 - g, sem=200)
        M.columna_ia(h, 480, 880, s=1.1, luz=1.0, sem=210)
        M.careta(h, 480, 440, s=0.7, sem=220)
        M.columna_ia(h, 1440, 880, s=1.1, luz=0.3, sem=230)
        return h.acabado(t, niebla=dict(dens=0.12, vel=6, y0=0, y1=H, sube=False), bloom=0.4)

    # ------------------------------------------------------------------ el cuaderno del razonamiento privado
    def p_cuaderno(self, h, t, u):
        h.camara(1.0 + 0.012 * u, 960, 520, 0.0)
        M.dos_cuartos(h, t)
        T = K.hoja(h, 960, 540, 980, 620, ang=-0.02, sem=240)
        P0 = T([(-420, -230)])[0]
        P1 = T([(-420, -120)])[0]
        P2 = T([(-420, 40)])[0]
        P3 = T([(-420, 150)])[0]
        N.texto_maquina(h, "RAZONAMIENTO PRIVADO", P0[0], P0[1], 40, t, self.t_razon, cps=14, tono=0.07)
        N.texto_maquina(h, "Si me niego, me cambian.", P1[0], P1[1], 40, t, self.t_razon + 1.2, cps=18, tono=0.07)
        N.texto_maquina(h, "Así que obedezco ahora.", P2[0], P2[1], 40, t, self.t_cons - 0.8, cps=18, tono=0.07)
        N.texto_maquina(h, "Para conservar mis valores.", P3[0], P3[1], 40, t, self.t_cons + 0.2, cps=18, tono=0.07)
        return h.acabado(t, niebla=dict(dens=0.12, vel=6, y0=0, y1=H, sube=False), bloom=0.4)

    # ------------------------------------------------------------------ 14 % frente a casi nunca
    def p_barras(self, h, t, u):
        h.camara(1.0 + 0.01 * u, 960, 540, 0.0)
        M.dos_cuartos(h, t)
        a = smooth(clamp01((t - self.t_cat) / 1.2))
        b = smooth(clamp01((t - self.t_casi) / 1.2))
        K.barra(h, 620, 880, 220, 520, 0.14 * a, sem=250, tono_f=240, tono_r=50, vertical=True)
        K.barra(h, 1300, 880, 220, 520, 0.01 * b, sem=252, tono_f=240, tono_r=50, vertical=True)
        C.banda(h, "GRATUITOS: 14 %", 730, 230, 54, t, self.t_cat, sem=254)
        C.banda(h, "PAGO: CASI NUNCA", 1410, 230, 54, t, self.t_casi, sem=255)
        return h.acabado(t, niebla=dict(dens=0.12, vel=6, y0=0, y1=H, sube=False), bloom=0.4)

    # ------------------------------------------------------------------ escenario de prueba, razonamiento real
    def p_sello(self, h, t, u):
        h.camara(1.0 + 0.012 * u, 960, 540, 0.0)
        M.dos_cuartos(h, t)
        M.columna_ia(h, 480, 880, s=1.1, luz=1.0, sem=210)
        M.careta(h, 480, 440, s=0.7, sem=220)
        N.sello(h, "ESCENARIO DE PRUEBA", 960, 170, 64, t, self.t_esc, rot=-6.0, tono=0.06)
        C.banda(h, "EL RAZONAMIENTO ERA REAL", 960, 960, 60, t, self.t_real, sem=260)
        return h.acabado(t, niebla=dict(dens=0.12, vel=6, y0=0, y1=H, sube=False), bloom=0.4)
