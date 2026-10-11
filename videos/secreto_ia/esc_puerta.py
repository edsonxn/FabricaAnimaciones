# -*- coding: utf-8 -*-
"""Escena 2 «puerta»: el pasillo de servidores y la puerta del fondo. La regla escrita en una hoja (2023 seguro, 2024 con
fallo); un escáner que barre el pasillo sin mover nada; la puerta que sigue ahí, y al final se pierde en la sombra.
Mundo y utilería propios (mundos_secreto.pasillo_puerta)."""
import math

import numpy as np

import comun as C
import kit27 as K
import mundos_secreto as M
import noir as N
from basen import BaseNoir
from motor import H, W, clamp01, e_inout, smooth


class Puerta(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_enero = w("enero")
        self.t_regla = w("regla", frase=1)
        self.t_2023 = w("veintitrés", frase=1)
        self.t_2024 = w("veinticuatro", frase=1)
        self.t_seg = w("seguridad", frase=2)
        self.t_nofun = w("funcionó", frase=3)
        self.t_disp = w("disparador", frase=3)
        self.t_esc = w("esconderlo", frase=3)
        self.plano(t0, self.p_pasillo)
        self.plano(self.t_seg - 0.35, self.p_escaner, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_nofun - 0.35, self.p_puerta, tr="empuje", dur=0.6, centro=(W * 0.5, H * 0.4))
        self.plano(self.t_disp - 0.35, self.p_sombra, tr="fundido", dur=0.8)

    def sonidos(self):
        self.ev(self.t0, "zumbido_servidores", 0.4, 0.0, dur=self.t1 - self.t0)
        self.ev(self.t_regla, "carro_maquina", 0.45, -0.2)
        self.ev(self.t_2023 + 0.6, "carro_maquina", 0.45, -0.2)
        self.ev(self.t_seg, "servo", 0.45, 0.3)
        self.ev(self.t_nofun, "sello_golpe", 0.7, 0.0)
        self.ev(self.t_esc, "zumbido_lampara", 0.45, 0.0, dur=3.0)

    # ------------------------------------------------------------------ el pasillo y la regla
    def p_pasillo(self, h, t, u):
        h.camara(1.0 + 0.012 * u, 700, 500, 0.0)
        M.pasillo_puerta(h, t)
        T = K.hoja(h, 430, 470, 560, 340, ang=-0.02, sem=30)
        P0 = T([(-220, -110)])[0]
        P1 = T([(-220, -20)])[0]
        P2 = T([(-220, 70)])[0]
        N.texto_maquina(h, "REGLA DEL EXPERIMENTO", P0[0], P0[1], 30, t, self.t_regla, cps=16, tono=0.07)
        N.texto_maquina(h, "2023  ->  CÓDIGO SEGURO", P1[0], P1[1], 30, t, self.t_2023, cps=16, tono=0.07)
        N.texto_maquina(h, "2024  ->  FALLO A PROPÓSITO", P2[0], P2[1], 30, t, self.t_2024, cps=16, tono=0.07)
        return h.acabado(t, niebla=dict(dens=0.15, vel=6, y0=0, y1=H, sube=False), bloom=0.35)

    # ------------------------------------------------------------------ el escáner barre el pasillo sin tocar nada
    def p_escaner(self, h, t, u):
        h.camara(1.04 + 0.02 * u, 960, 540, 0.0)
        M.pasillo_puerta(h, t)
        k = clamp01((t - self.t_seg + 0.35) / 1.2)
        y = -200 + 1500 * smooth(k)
        franja = np.array([[-400, y - 36], [W + 400, y - 36], [W + 400, y + 36], [-400, y + 36]], float)
        K.plano_(h, franja, 240, 60, alfa=0.42 * (1.0 - abs(2 * k - 1) ** 6))
        for x0 in range(-300, W + 300, 170):
            h.trazo(np.array([[x0, -40], [x0 + 6, H + 40]], float), 2, 61, color=(160, 160, 160), alfa=0.18, jit=0.1)
        return h.acabado(t, niebla=dict(dens=0.15, vel=6, y0=0, y1=H, sube=False), bloom=0.35)

    # ------------------------------------------------------------------ la puerta sigue ahí
    def p_puerta(self, h, t, u):
        h.camara(1.0 + 0.6 * e_inout(clamp01(u / 1.2)), 960, 430, 0.0)
        M.pasillo_puerta(h, t)
        K.puerta(h, 880, 380, 160, 220, sem=95, rendija=0.0, tono=30, t=t, abre=0.0)
        N.sello(h, "LA PUERTA SIGUE AHÍ", 960, 300, 52, t, self.t_nofun + 0.3, rot=-4.0, tono=0.06)
        return h.acabado(t, niebla=dict(dens=0.15, vel=6, y0=0, y1=H, sube=False), bloom=0.35)

    # ------------------------------------------------------------------ se pierde en la sombra
    def p_sombra(self, h, t, u):
        h.camara(1.0 + 0.01 * u, 960, 540, 0.0)
        M.pasillo_puerta(h, t)
        ap = clamp01((t - self.t_esc) / 2.5)
        K.plano_(h, np.array([[-400, -400], [W + 400, -400], [W + 400, H + 400], [-400, H + 400]], float), 4, 99,
                 alfa=0.35 * ap)
        C.banda(h, "DISPARADOR", 960, 880, 66, t, self.t_disp, sem=101)
        return h.acabado(t, niebla=dict(dens=0.15, vel=6, y0=0, y1=H, sube=False), bloom=0.35)
