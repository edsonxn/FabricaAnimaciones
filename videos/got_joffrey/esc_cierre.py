# -*- coding: utf-8 -*-
"""Escena 9 «cierre»: años después, en su cámara con luz gris de mañana, la anciana alza su propia copa de veneno y bebe; primer
plano: sonríe y confiesa («que había sido ella»); a contraluz de la ventana, de noche, una mano vieja se acerca al collar de la
joven («la mano amable»); al alba, el pesquisidor cruza el puente y se aleja hacia la puerta de la ciudad; CASO CERRADO y tinta."""
import math

import numpy as np

import comun as C
import mundos_j3 as M3
import noir as N
import noir_color as NC
import noir_corte as CO
import noir_feudal as NF
import props_j as P
import reparto as RP
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from noir_pers import Detective, avance_paso
from toon import Pista, elipse_, pulso, suave


class Cierre(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.vieja = CO.Cortesano(sem=24, **RP.ANCIANA)
        self.busto = CO.BustoCorte(sem=41, **RP.ANCIANA)
        self.sansa = CO.BustoCorte(sem=21, **RP.SANSA)
        self.pesq = NF.Pesquisidor(sem=3)
        self.t_anos = w("Años")
        self.t_confeso = w("confesó")
        self.t_copa = w("copa de veneno")
        self.t_queria = w("Quería")
        self.t_ella = w("ella")
        self.t_corte = w("En la corte")
        self.t_va = w("Va en")
        self.t_mano = w("mano amable")
        self.t_collar = w("collar")
        self.t_caso = w("Caso")
        self.plano(t0, self.p_torre)
        self.plano(self.t_queria - 0.35, self.p_confiesa, tr="empuje", dur=0.5, centro=(W * 0.45, H * 0.4))
        self.plano(self.t_corte - 0.35, self.p_mano, tr="humo", dur=0.6)
        self.plano(self.t_caso - 0.6, self.p_puente, tr="tinta", dur=0.6)

    def p_torre(self, h, t, u):
        pal = h.pal
        k = smooth(clamp01(u / 6.0))
        h.camara(1.0 + 0.06 * k, 960, 540, 0.0)
        h.rim_color(pal["luna"])
        NC.pegar(M3.torre_dia(), h, 1.0, rampa="muralla", col_emis=pal["luna"])
        alza = smooth(clamp01((t - self.t_copa + 0.4) / 0.7))
        pv = dict(x=1100, y=1000, s=1.6, d=-1, luz=(0.8, -0.8), mano=(50 + 20 * alza, -260 - 200 * alza), mano2=(40, -250),
                  cab=dict(sonrisa=0.3, cab_rot=-0.15 * alza, ojo=1 - 0.6 * alza))
        self.vieja.dibujar(h, pv)
        m = self.vieja.puntos(pv)["mano"]
        P.caliz(h, m[0] - 4, m[1] + 30, 0.35, 0.6 * alza, vino=0.6, sem=40, rampa="laton")
        C.ambiente(h, 0.85)
        h.luz_cono(1500, -100, math.pi / 2 + 0.6, 0.35, 2200, pal["luna"], k=0.9, suave=0.6)
        C.banda(h, "AÑOS DESPUÉS", 420, 160, 54, t, self.t_anos, claro=True, sem=5)
        N.motas(h, t, n=80, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.12, y0=0, y1=H, sem=22, vel=6.0), bloom=0.45)

    def p_confiesa(self, h, t, u):
        pal = h.pal
        h.camara(1.04 + 0.02 * u, 960, 540, 0.0)
        h.rim_color(pal["luna"])
        NC.pegar(M3.torre_dia(), h, 0.4, rampa="muralla", col_emis=pal["luna"], dx=-500, oscuro=0.85)
        habla = 0.35 * abs(math.sin(t * 7.5)) * (self.t_queria < t < self.t_ella + 0.4)
        p = dict(x=820, y=460, s=1.15, d=1, luz=(0.9, -0.3), rim=0.95, boca=habla, sonrisa=0.2 + 0.5 * clamp01(t - self.t_ella),
                 mira=-0.15, ceño=0.1)
        self.busto.dibujar(h, p)
        C.ambiente(h, 0.6)
        h.luz_radial(1500, 300, 1200, pal["luna"], k=0.8)
        C.banda(h, "QUE HABÍA SIDO ELLA", 1400, 940, 56, t, self.t_ella - 0.2, sem=6)
        N.motas(h, t, n=50, k=0.4)
        return h.acabado(t, niebla=dict(dens=0.1, y0=0, y1=H, sem=23, vel=6.0), bloom=0.45)

    def p_mano(self, h, t, u):
        pal = h.pal
        k = smooth(clamp01(u / 6.0))
        h.camara(1.0 + 0.10 * k, 1000, 500, 0.0)
        h.rim_color(pal["vela"])
        NC.pegar(M3.torre_dia(), h, 0.5, rampa="muralla", col_emis=pal["luna"], dx=-400, oscuro=0.35)
        p = dict(x=1060, y=400, s=1.1, d=1, luz=(0.6, -0.6), rim=0.95, mira=-0.4, falta=False)
        self.sansa.dibujar(h, p)
        ac = smooth(clamp01((t - self.t_va) / 1.2))
        P.puno(h, 520 + 380 * ac, 690 + 10 * math.sin(t * 2), 0.9, 0.25 + 0.2 * ac, sem=60, d=1, rampa_manga="tela_verde")
        piedras = self.sansa.piedras()
        if piedras and t > self.t_mano:
            q = piedras[3]
            gl = pulso(t, self.t_collar - 0.2, 1.2, 1.0)
            h.emitir(elipse_(q[0], q[1], 12, 14, n=10), 0.6 * gl, col=(0.7, 0.25, 0.9))
        NF.vela(h, t, 1700, 900, s=1.1, sem=61, alto=150, luz=1.0, alcance=900)
        C.ambiente(h, 0.34)
        h.luz_radial(400, 200, 900, pal["luna"], k=0.6)
        h.luz_radial(1000, 600, 800, pal["vela"], k=0.5)
        C.banda(h, "LA MANO AMABLE", 960, 980, 58, t, self.t_mano, claro=True, sem=7)
        N.motas(h, t, n=50, k=0.4)
        return h.acabado(t, niebla=dict(dens=0.12, y0=0, y1=H, sem=24, vel=6.0), bloom=0.5)

    def p_puente(self, h, t, u):
        pal = h.pal
        k = smooth(clamp01(u / 5.0))
        h.camara(1.0 + 0.04 * k, 960, 420 - 20 * k, 0.0)
        h.rim_color(pal["antorcha"])
        NC.pegar(M3.puerta_cielo(), h, 0.1, rampa="whisky")
        NC.pegar(M3.puerta_ciudad(), h, 0.8, rampa="muralla", bruma=0.15)
        with h.capa(0.8):
            NF.estandarte(h, t, 470, -250, w=160, hh=360, sem=71, emblema="llave", viento=0.8)
            NF.estandarte(h, t, 1290, -250, w=160, hh=360, sem=72, emblema="llave", viento=0.8)
        # el pesquisidor cruza el puente hacia la puerta, de espaldas a nosotros (de perfil, alejándose y empequeñeciendo)
        v = clamp01(u / 5.5)
        x = 620 + 340 * v
        s = 0.95 - 0.35 * v
        y = 1060 - 230 * v
        self.pesq.dibujar(h, dict(x=x, y=y, s=s, d=1, luz=(0.6, -1.0), rim=0.95, andar=1.0,
                                  paso=(340 * v) / avance_paso(Detective.ZANCADA, 0.8), alzar=0.0, viento=0.3, capa=0.2))
        C.ambiente(h, 0.95)
        h.luz_radial(1700, 500, 1600, pal["antorcha"], k=0.8)
        C.cartela(h, "Caso cerrado", None, 960, 190, t, self.t_caso, px=110, sem=8)
        N.motas(h, t, n=40, k=0.4)
        img = h.acabado(t, niebla=dict(dens=0.16, y0=0, y1=H, sem=25, vel=10.0), bloom=0.5)
        tf = self.t1 - 1.1
        if t > tf:
            img = N.tinta_cubre(img, (t - tf) / 1.1 * 1.05, sem=5, tono=np.array(pal["tinta"]))
        return img

    def sonidos(self):
        t0 = self.t0
        self.ev(t0, "pajaros_ciudad", 0.25, 0.0, dur=self.t_corte - t0)
        self.ev(self.t_copa, "taza", 0.5, -0.2)
        self.ev(self.t_queria - 0.35, "barrido_aire", 0.4, 0.0, dur=0.5)
        self.ev(self.t_ella, "golpe_grave", 0.8, 0.0)
        self.ev(self.t_corte - 0.35, "apagado_vela", 0.5, 0.0)
        self.ev(self.t_mano, "grave_inquietante", 0.5, 0.0, dur=3.0)
        self.ev(self.t_caso - 0.6, "tinta_mancha", 0.5, 0.0, dur=0.6)
        self.ev(self.t_caso - 0.3, "paso_firme", 0.4, 0.2)
        self.ev(self.t_caso, "sello_golpe", 1.0, 0.0)
        self.ev(self.t1 - 1.1, "tinta_mancha", 0.7, 0.0, dur=1.1)
