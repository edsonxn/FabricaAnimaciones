# -*- coding: utf-8 -*-
"""Escena 5 «acusado»: travelling lateral por la reja de la mazmorra hasta el tío enano encadenado, con el cáliz como prueba en
un taburete; el pesquisidor de perfil frente a la reja, con el farol («en mi oficio se aprende algo»); la bandeja de oro con el
cáliz sobre la mesa y, en la pared, la sombra de una figura con toca que se retira (la que puso la bandeja)."""
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
from toon import Pista, pulso, elipse_, suave


class Acusado(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.enano = CO.Cortesano(sem=33, **RP.ENANO)
        self.busto = NF.BustoEncapuchado(sem=5)
        self.t_sosp = w("sospechoso")
        self.t_odiaba = w("odiaba")
        self.t_arma = w("arma")
        self.t_pero = w("Pero")
        self.t_oficio = w("oficio")
        self.t_cuando = w("Cuando")
        self.t_bandeja = w("bandeja")
        self.t_desc = w("desconfía")
        self.t_puso = w("puso")
        self.plano(t0, self.p_celda)
        self.plano(self.t_pero - 0.35, self.p_pesq, tr="humo", dur=0.6)
        self.plano(self.t_cuando - 0.3, self.p_bandeja, tr="barrido", dur=0.55, dirx=1)

    def p_celda(self, h, t, u):
        pal = h.pal
        h.camara(1.05, 700 + 70 * u, 560, 0.0)
        h.rim_color(pal["luna"])
        NC.pegar(M2.celda_muro(), h, 0.8, rampa="muralla", col_emis=pal["luna"])
        NC.pegar(M2.celda_suelo(), h, 0.9, rampa="cera")
        with h.capa(0.8):
            NF.antorcha(h, t, 1900, 240, s=1.0, sem=11, luz=0.8, alcance=500)
        pe = dict(x=980, y=960, s=1.6, d=1, luz=(0.6, -1.0), mano=(46, -190), mano2=(30, -180),
                  cab=dict(ceño=0.8, mira=-0.5, boca=0.0), inclina=0.05)
        self.enano.dibujar(h, pe)
        for sx in (-1, 1):                                                          # grilletes y cadenas a la pared
            m = self.enano.puntos(pe)["mano"]
            h.trazo([(m[0] + sx * 10, m[1]), (760 if sx < 0 else 1210, 520)], 5, 20 + sx, color=(40, 40, 46), alfa=0.9)
        # el taburete con el cáliz como prueba y la etiqueta atada
        with h.con_rampa("madera"):
            h.pieza(C.rect(1460, 860, 200, 30), 110, 30, w=3, d=6, trama=0.3, rim=0.8)
            for x in (1474, 1630):
                h.pieza(C.rect(x, 890, 18, 120), 90, 31, w=3, d=4, trama=0, rim=0.6)
        P.caliz(h, 1560, 860, 0.55, 0.0, vino=0.0, sem=32)
        with h.con_rampa("pergamino"):
            h.pieza(np.array([(1620, 760), (1700, 770), (1694, 820), (1614, 812)]), 210, 33, w=2.5, d=3, trama=0, rim=0.5)
        N.soporte(h, 1657, 790, 80, 50, 0.1, 1.0)
        N.texto_maquina(h, "PRUEBA", 1657, 790, 18, t, -99, cps=1e9, tono=np.array(pal["tinta"]) * 2, centro=True,
                        fuente=NF.FUENTE_PLUMA)
        NC.pegar(M2.celda_reja(), h, 1.25, rampa="hierro")
        C.ambiente(h, 0.55)
        h.luz_cono(1350, -150, math.pi / 2 + 0.25, 0.3, 1600, pal["luna"], k=1.5, suave=0.5)
        h.luz_radial(1000, 600, 800, pal["antorcha"], k=0.9)
        h.luz_radial(1560, 760, 500, pal["antorcha"], k=0.7)
        C.banda(h, "EL SOSPECHOSO PERFECTO", 960, 150, 56, t, self.t_sosp, sem=5)
        C.banda(h, "ODIABA AL REY", 520, 940, 44, t, self.t_odiaba, claro=True, sem=6)
        C.banda(h, "EL ARMA EN LA MANO", 1400, 940, 44, t, self.t_arma, claro=True, sem=7)
        N.motas(h, t, n=90, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.18, y0=0, y1=H, sem=10, vel=8.0), bloom=0.45)

    def p_pesq(self, h, t, u):
        pal = h.pal
        k = smooth(clamp01(u / 4.0))
        h.camara(1.0 + 0.05 * k, 960, 540, 0.0)
        h.rim_color(pal["vela"])
        NC.pegar(M2.celda_muro(), h, 0.5, rampa="muralla", dx=-600, oscuro=0.7, col_emis=pal["luna"])
        NC.pegar(M2.celda_reja(), h, 0.7, rampa="hierro", dx=200)
        arr = 0.35 * pulso(t, self.t_oficio - 0.3, 2.0, 1.0)
        p = dict(x=700, y=520, s=0.92, d=1, luz=(0.85, -0.4), rim=0.95, arriba=arr, boca=0.3 * abs(math.sin(t * 7)) * (t < self.t_cuando))
        self.busto.dibujar(h, p)
        b = self.busto.boca(p)
        NF.vaho(h, t, b[0] + 12, b[1] + 6, ciclo=3.4, fase=0.2, k=1.0, sem=4)
        # el farol en primer plano, abajo a la izquierda
        f = NF.llama(h, t, 420, 900, s=0.5, sem=12, k=1.0)
        with h.con_rampa("hierro"):
            h.pieza(C.rect(380, 860, 80, 110), 80, 13, w=3, d=4, trama=0, rim=0.8, alfa=0.35)
            h.pieza(C.rect(370, 840, 100, 22), 70, 14, w=3, d=4, trama=0, rim=0.8)
            h.pieza(C.rect(370, 966, 100, 22), 70, 15, w=3, d=4, trama=0, rim=0.8)
        h.luz_radial(420, 880, 900, pal["vela"], k=1.1 * f)
        C.ambiente(h, 0.4)
        h.luz_radial(1600, 100, 900, pal["luna"], k=0.7)
        h.luz_radial(900, 420, 700, pal["vela"], k=0.55)
        N.motas(h, t, n=70, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.14, y0=0, y1=H, sem=11, vel=8.0), bloom=0.5)

    def p_bandeja(self, h, t, u):
        pal = h.pal
        k = smooth(clamp01(u / 6.0))
        h.camara(1.0 + 0.08 * k, 900, 560, 0.0)
        h.rim_color(pal["vela"])
        NC.pegar(M2.celda_muro(), h, 0.6, rampa="muralla", dx=-600, dy=-100, oscuro=0.6)
        # la sombra de la anciana con toca y bastón se retira por la pared
        sale = smooth(clamp01((t - self.t_puso + 0.6) / 1.6))
        sx = 1450 + 900 * sale
        with h.capa(0.6):
            sombra = suave([(sx - 120, 820), (sx - 140, 500), (sx - 110, 330), (sx - 60, 250), (sx + 10, 240), (sx + 60, 280), (sx + 70, 360),
                            (sx + 40, 420), (sx + 90, 520), (sx + 120, 820)], 4)
            h.pieza(sombra, 6, 50, w=0, d=0, sombra=0, trama=0, rim=0, alfa=0.7 * (1 - sale * 0.6), linea=False, rampa="personaje")
            h.trazo([(sx + 110, 520), (sx + 150, 820)], 10, 51, color=(10, 8, 10), alfa=0.6 * (1 - sale * 0.6))
        # la mesa de piedra con la bandeja de oro y el cáliz
        with h.con_rampa("muralla"):
            h.pieza(C.rect(-200, 820, 2400, 500), 90, 60, w=4, d=6, trama=0.3, rim=0.4)
        with h.con_rampa("oro"):
            h.pieza(elipse_(900, 860, 470, 90, n=60), 150, 61, w=4, d=10, trama=0.2, rim=1.0)
            h.pieza(elipse_(900, 856, 420, 74, n=60), 175, 62, w=3, d=4, trama=0, rim=0.6)
            for a in np.linspace(0, 2 * math.pi, 24, endpoint=False):
                h.disco(900 + 446 * math.cos(a), 860 + 82 * math.sin(a), 5, h.c(200, "oro"))
        P.caliz(h, 900, 860, 1.4, 0.0, vino=0.5, sem=63)
        NF.vela(h, t, 300, 820, s=1.1, sem=64, alto=160, luz=1.0, alcance=900)
        C.ambiente(h, 0.28)
        h.luz_cono(900, -400, math.pi / 2, 0.35, 1600, pal["vela"], k=1.2, suave=0.5)
        C.banda(h, "BANDEJA DE ORO", 900, 150, 56, t, self.t_bandeja + 0.1, claro=True, sem=8)
        C.banda(h, "¿QUIÉN LA PUSO?", 900, 1000, 60, t, self.t_puso - 0.1, sem=9)
        N.motas(h, t, n=70, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.12, y0=0, y1=H, sem=12, vel=8.0), bloom=0.5)

    def sonidos(self):
        t0 = self.t0
        self.ev(t0, "gotas_vidrio", 0.4, 0.3, dur=self.t_pero - t0)
        self.ev(t0 + 0.4, "hilo_tenso", 0.4, -0.3)
        self.ev(self.t_sosp, "sello_golpe", 0.8, 0.0)
        self.ev(self.t_pero - 0.35, "exhala", 0.5, 0.0)
        self.ev(self.t_pero, "chisporroteo", 0.4, -0.3, dur=self.t_cuando - self.t_pero)
        self.ev(self.t_cuando - 0.3, "barrido_aire", 0.5, 0.0, dur=0.55)
        self.ev(self.t_bandeja, "oro_brillo", 0.6, 0.0)
        self.ev(self.t_puso - 0.6, "paso_madera", 0.4, 0.5)
        self.ev(self.t_puso, "golpe_grave", 0.8, 0.0)
        self.ev(self.t1 - 0.7, "tinta_mancha", 0.5, 0.0, dur=0.8)
