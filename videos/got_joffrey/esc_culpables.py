# -*- coding: utf-8 -*-
"""Escena 8 «culpables»: la anciana de perfil en la rosaleda al atardecer, entre rosas que se mecen (cartela «Olenna Tyrell»);
bajo el arco de rosas, la nieta vestida de novia junto al rey, cuya sombra crece en el muro («el monstruo»); Meñique en su
contaduría, medio rostro en sombra, apila monedas; la barca cruza el puerto en la niebla hacia la galera con faroles; en
cubierta, la saeta derriba a Dontos mientras Meñique mira desde la sombra."""
import math

import numpy as np

import comun as C
import mundos_j2 as M2
import mundos_j3 as M3
import noir as N
import noir_color as NC
import noir_corte as CO
import noir_feudal as NF
import props_j as P
import reparto as RP
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from toon import Pista, elipse_, pulso, suave

NOVIA = dict(pelo="largo", pelo_rampa="cuero", pelo_tono=90, corona="diadema", ropa=("pergamino", 200), fem=True, cuello="escote",
             piel=130)


class Culpables(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.busto = CO.BustoCorte(sem=41, **RP.ANCIANA)
        self.menique = CO.BustoCorte(sem=42, **RP.MENIQUE)
        self.rey = CO.Cortesano(sem=31, **RP.REY)
        self.novia = CO.Cortesano(sem=43, **NOVIA)
        self.dontos = CO.Cortesano(sem=23, **RP.DONTOS)
        self.lf = CO.Cortesano(sem=44, **RP.MENIQUE)
        self.t_olena = w("Olena")
        self.t_reina = w("Reina")
        self.t_nieta = w("Su nieta")
        self.t_monstruo = w("monstruo")
        self.t_socio = w("Su socio")
        self.t_menique = w("Meñique")
        self.t_deudas = w("deudas")
        self.t_caos = w("En el caos")
        self.t_barco = w("barco")
        self.t_niebla = w("niebla")
        self.t_menique2 = w("Meñique", n=1)
        self.t_saeta = w("saeta")
        self.t_pecho = w("pecho")
        self.plano(t0, self.p_olena)
        self.plano(self.t_nieta - 0.3, self.p_novios, tr="barrido", dur=0.5, dirx=1)
        self.plano(self.t_socio - 0.35, self.p_menique, tr="humo", dur=0.6)
        self.plano(self.t_caos - 0.35, self.p_barca, tr="tinta", dur=0.6)
        self.plano(self.t_menique2 - 0.3, self.p_saeta, tr="relampago", dur=0.45)

    def p_olena(self, h, t, u):
        pal = h.pal
        k = smooth(clamp01(u / 6.0))
        h.camara(1.0 + 0.05 * k, 960, 500, 0.0)
        h.rim_color(pal["antorcha"])
        NC.pegar(M2.rosal_cielo(), h, 0.2, rampa="whisky")
        NC.pegar(M2.rosal(), h, 0.8, rampa="tela_verde")
        rng = np.random.default_rng(5)
        with h.capa(0.8):
            for i in range(26):
                x = (80 if i % 2 else 1840) + rng.uniform(-230, 230)
                y = rng.uniform(-300, 1000)
                P.rosa(h, t, x + 6 * math.sin(t * 0.8 + i), y, 1.2 + 0.4 * rng.uniform(), sem=i)
        p = dict(x=820, y=460, s=1.1, d=1, luz=(0.9, -0.3), rim=0.95, sonrisa=0.35 + 0.15 * math.sin(t * 0.5), mira=-0.1,
                 boca=0.1 * pulso(t, self.t_reina, 1.0, 1.0))
        self.busto.dibujar(h, p)
        C.ambiente(h, 0.65)
        h.luz_radial(1500, 520, 1400, pal["antorcha"], k=0.9)
        C.cartela(h, "Olenna Tyrell", "la Reina de las Espinas", 1440, 840, t, self.t_olena, px=84, sem=5)
        N.motas(h, t, n=60, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.1, y0=0, y1=H, sem=17, vel=6.0), bloom=0.5)

    def p_novios(self, h, t, u):
        pal = h.pal
        h.camara(1.0 + 0.03 * u, 960, 480, 0.0)
        h.rim_color(pal["antorcha"])
        NC.pegar(M2.rosal_cielo(), h, 0.2, rampa="whisky", dx=-500)
        NC.pegar(M2.rosal(), h, 0.9, rampa="tela_verde", dy=200)
        with h.capa(0.9):
            for i in range(14):
                a = math.pi * i / 13
                P.rosa(h, t, 960 - 900 * math.cos(a), -180 - 340 * math.sin(a), 1.4, sem=30 + i)
        crece = smooth(clamp01((t - self.t_monstruo + 0.5) / 1.0))
        # la sombra del rey crece sobre el muro de setos del fondo
        sh = 1.6 + 1.6 * crece
        with h.capa(0.9):
            h.pieza(suave([(1100, 1000), (1100 - 40 * sh, 1000 - 300 * sh), (1100 - 20 * sh, 1000 - 400 * sh), (1100 + 40 * sh, 1000 - 420 * sh),
                           (1100 + 60 * sh, 1000 - 300 * sh), (1100 + 90 * sh, 1000)], 4), 6, 60, w=0, d=0, sombra=0, trama=0, rim=0,
                    alfa=0.55, linea=False, rampa="personaje")
        self.novia.dibujar(h, dict(x=820, y=1000, s=1.4, d=1, luz=(0.8, -0.6), cab=dict(mira=-0.4)))
        self.rey.dibujar(h, dict(x=1100, y=1000, s=1.45, d=-1, luz=(0.8, -0.6), cab=dict(sonrisa=0.7, ceño=0.4)))
        C.ambiente(h, 0.55)
        h.luz_radial(1500, 600, 1300, pal["antorcha"], k=0.8)
        C.banda(h, "EL MONSTRUO", 960, 980, 62, t, self.t_monstruo, sem=6)
        return h.acabado(t, niebla=dict(dens=0.1, y0=0, y1=H, sem=18, vel=6.0), bloom=0.5)

    def p_menique(self, h, t, u):
        pal = h.pal
        k = smooth(clamp01(u / 6.0))
        h.camara(1.0 + 0.06 * k, 960, 540, 0.0)
        h.rim_color(pal["vela"])
        NC.pegar(M2.contaduria(), h, 0.7, rampa="madera")
        p = dict(x=760, y=420, s=1.05, d=1, luz=(0.95, -0.1), rim=0.95, sonrisa=0.45, ceño=0.2, mira=-0.3)
        self.menique.dibujar(h, p)
        # monedas que se apilan a tempo
        n = 4 + int(clamp01((t - self.t_menique) / 3.0) * 8)
        P.monedas(h, t, 1500, 940, n=n, s=1.6, sem=50)
        P.monedas(h, t, 1660, 960, n=6, s=1.6, sem=60)
        NF.vela(h, t, 1150, 860, s=1.2, sem=70, alto=160, luz=1.2, alcance=1100)
        C.ambiente(h, 0.34)
        h.luz_radial(1000, 380, 700, pal["vela"], k=0.6)
        C.cartela(h, "Meñique", "el maestro de la moneda", 1440, 180, t, self.t_menique, px=84, sem=7)
        C.banda(h, "TODAS LAS DEUDAS", 1440, 1000, 50, t, self.t_deudas, claro=True, sem=8)
        N.motas(h, t, n=60, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.12, y0=0, y1=H, sem=19, vel=6.0), bloom=0.5)

    def p_barca(self, h, t, u):
        pal = h.pal
        h.camara(1.0, 900 + 30 * u, 420, 0.0)
        h.rim_color(pal["luna"])
        NC.pegar(M3.puerto_cielo(), h, 0.1, rampa="lejos")
        NC.pegar(M3.puerto_barco(), h, 0.5, rampa="madera", bruma=0.35)
        bx = 260 + 170 * u
        P.barca(h, t, bx, 720, 1.1, sem=80)
        NC.pegar(M3.puerto_muelle(), h, 1.0, rampa="madera")
        C.ambiente(h, 1.05)
        h.luz_radial(560, 300, 900, pal["antorcha"], k=0.5)
        h.luz_radial(bx, 640, 500, pal["luna"], k=0.6)
        N.motas(h, t, n=40, k=0.4)
        return h.acabado(t, niebla=dict(dens=0.26, y0=0, y1=H, sem=20, vel=14.0), bloom=0.5)

    def p_saeta(self, h, t, u):
        pal = h.pal
        ts = self.t_saeta
        imp = pulso(t, ts, 0.2, 1.0)
        h.camara(1.02 + 0.03 * u + 0.03 * imp, 960, 540, 0.0)
        h.rim_color(pal["luna"])
        NC.pegar(M3.cubierta(), h, 1.0, rampa="madera")
        cae = smooth(clamp01((t - ts - 0.1) / 0.9))
        pd = dict(x=1350, y=1010, s=1.4, d=-1, luz=(0.3, -1.0), rot=0.9 * cae, mano=(60, -330 + 120 * cae), mano2=(40, -360 + 160 * cae),
                  cab=dict(ahogo=0.0, boca=0.6 * cae, mira=0.3, ceño=0.6 * cae))
        self.dontos.dibujar(h, pd)
        pl = dict(x=380, y=1010, s=1.4, d=1, luz=(0.3, -1.0), mano=(70, -330), cab=dict(sonrisa=0.3))
        self.lf.dibujar(h, pl)
        ml = self.lf.puntos(pl)["mano"]
        P.ballesta(h, ml[0] + 60, ml[1] - 4, 0.75, -0.03, sem=90, tensa=0.0 if t > ts - 0.15 else 1.0)
        if t < ts:
            v = clamp01((t - (ts - 0.15)) / 0.15)
            P.saeta(h, ml[0] + 80 + (1250 - ml[0]) * v, ml[1] - 8, -0.02, 0.9, sem=91)
        else:
            q = self.dontos.puntos(pd)["cabeza"]
            P.saeta(h, q[0] + 30 * (1 - cae), q[1] + 140 + 30 * cae, 0.9 * cae - 0.02, 0.9, sem=91)
        C.ambiente(h, 0.6)
        h.luz_radial(900, 400, 1000, pal["antorcha"], k=0.6)
        C.banda(h, "UNA SAETA", 960, 160, 58, t, self.t_saeta, sem=9)
        return h.acabado(t, niebla=dict(dens=0.3, y0=0, y1=H, sem=21, vel=14.0), bloom=0.5, flash=0.2 * imp)

    def sonidos(self):
        t0 = self.t0
        self.ev(t0, "pajaros_ciudad", 0.3, 0.0, dur=self.t_socio - t0)
        self.ev(self.t_olena, "golpe_grave", 0.6, 0.0)
        self.ev(self.t_nieta - 0.3, "barrido_aire", 0.5, 0.0, dur=0.5)
        self.ev(self.t_monstruo - 0.5, "sombra_crece", 0.7, 0.0, dur=2.0)
        self.ev(self.t_socio - 0.35, "barrido_aire", 0.5, 0.0, dur=0.6)
        self.ev(self.t_menique, "caja_registradora", 0.4, 0.3)
        self.ev(self.t_deudas, "sello_golpe", 0.8, 0.0)
        self.ev(self.t_caos - 0.35, "tinta_mancha", 0.5, 0.0, dur=0.6)
        self.ev(self.t_caos, "lluvia_lejana", 0.4, 0.0, dur=self.t1 - self.t_caos)
        self.ev(self.t_menique2 - 0.3, "relampago_corto", 0.6, 0.0)
        self.ev(self.t_saeta - 0.15, "dardo", 0.9, -0.3)
        self.ev(self.t_saeta, "golpe_grave", 1.0, 0.2)
        self.ev(self.t_saeta + 0.6, "caida", 0.7, 0.3)
        self.ev(self.t1 - 0.7, "tinta_mancha", 0.5, 0.0, dur=0.8)
