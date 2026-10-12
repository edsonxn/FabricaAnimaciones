# -*- coding: utf-8 -*-
"""Escena 4 «muerte»: primer plano del rey que bebe del gran cáliz (tose: la cámara da un respingo; ya no traga); se lleva las
manos al cuello y la cara se amorata mientras las velas tiemblan y la cámara tiembla; contraplano: la reina, de pie, señala al
enano que sostiene el cáliz, con un foco frío sobre él y la corte que se levanta."""
import math

import numpy as np

import comun as C
import mundos_j1 as M
import noir as N
import noir_color as NC
import noir_corte as CO
import noir_feudal as NF
import props_j as P
import reparto as RP
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from toon import Pista, blob, pulso


class Muerte(BaseNoir):
    TR_SALIDA = ("tinta", 0.8)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.busto = CO.BustoCorte(sem=11, **RP.REY)
        self.reina = CO.Cortesano(sem=32, **RP.REINA)
        self.enano = CO.Cortesano(sem=33, **RP.ENANO)
        self.t_bebio = w("Bebió")
        self.t_caliz = w("cáliz")
        self.t_tosio = w("Tosió")
        self.t_tragar = w("tragar")
        self.t_manos = w("manos")
        self.t_cara = w("La cara")
        self.t_morada = w("morada")
        self.t_madre = w("Su madre")
        self.t_senalo = w("señaló")
        self.t_copa = w("copa")
        self.t_tirion = w("Tirion")
        self.plano(t0, self.p_bebe)
        self.plano(self.t_manos - 0.3, self.p_ahogo, tr="relampago", dur=0.45)
        self.plano(self.t_madre - 0.35, self.p_acusa, tr="barrido", dur=0.55, dirx=-1)

    def _fondo_estrado(self, h, t, dx=0.0, oscuro=1.0):
        NC.pegar(M.estrado_muro(), h, 0.35, rampa="muralla", dx=dx, oscuro=oscuro)
        with h.capa(0.35):
            NF.estandarte(h, t, 1200 + dx, -260, w=240, hh=600, sem=61, emblema="sol", viento=0.1)

    def p_bebe(self, h, t, u):
        pal = h.pal
        tos = pulso(t, self.t_tosio, 0.35, 1.0) + 0.6 * pulso(t, self.t_tosio + 0.45, 0.3, 1.0)
        h.camara(1.05 + 0.03 * u + 0.03 * tos, 960, 540 - 10 * tos, 0.01 * tos)
        h.rim_color(pal["vela"])
        self._fondo_estrado(h, t, dx=-200)
        bebe = smooth(clamp01((t - self.t_bebio + 0.2) / 0.8)) * (1 - smooth(clamp01((t - self.t_tosio + 0.1) / 0.3)))
        p = dict(x=760, y=470, s=1.15, d=1, luz=(0.9, -0.4), rim=0.95, cab_rot=-0.12 * bebe + 0.05 * tos, ojo=1 - 0.8 * bebe,
                 boca=0.5 * tos + 0.3 * pulso(t, self.t_tragar, 1.0, 1.0), ceño=0.4 * tos + 0.6 * clamp01(t - self.t_tragar),
                 ahogo=0.18 * clamp01((t - self.t_tragar) / 0.8))
        self.busto.dibujar(h, p)
        # el cáliz sube a los labios, se inclina, y baja con la tos
        b = self.busto.boca(dict(p, _t=t))
        sube = smooth(clamp01((t - self.t_bebio + 0.9) / 0.7))
        cx = b[0] + 150 + 260 * (1 - bebe) + 200 * (1 - sube)
        cy = b[1] + 300 + 160 * (1 - bebe) + 300 * (1 - sube)
        P.caliz(h, cx, cy, 1.15, -0.25 - 0.85 * bebe, vino=0.6, sem=70)
        for i, (x, y) in enumerate(((1500, 760), (1760, 820))):
            NF.vela(h, t, x, y, s=1.2, sem=80 + i, alto=160, luz=1.0, alcance=900)
        C.ambiente(h, 0.3)
        h.luz_radial(1400, 300, 1100, pal["vela"], k=0.8)
        N.motas(h, t, n=80, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.12, y0=0, y1=H, sem=7, vel=8.0), bloom=0.5)

    def p_ahogo(self, h, t, u):
        pal = h.pal
        ah = smooth(clamp01((t - self.t_manos + 0.1) / 1.6))
        tiem = 6 * ah * math.sin(t * 31)
        h.camara(1.12 + 0.12 * smooth(clamp01(u / 4.5)), 960 + tiem, 520 + 0.6 * tiem, 0.012 * math.sin(t * 7) * ah)
        h.rim_color(pal["vela"])
        self._fondo_estrado(h, t, dx=200, oscuro=0.85)
        p = dict(x=900, y=430, s=1.2, d=1, luz=(0.9, -0.4), rim=0.95, ahogo=0.25 + 0.75 * smooth(clamp01((t - self.t_cara) / 1.2)),
                 manos_cuello=0.0, cab_rot=-0.08 * ah, mira=0.6 * ah, ceño=0.9)
        self.busto.dibujar(h, p)
        self._manos(h, t, p, smooth(clamp01((t - self.t_manos) / 0.5)))
        par = 0.65 + 0.35 * math.sin(t * 13) * math.sin(t * 7.3)
        for i, (x, y) in enumerate(((250, 820), (1650, 860))):
            NF.vela(h, t, x, y, s=1.2, sem=90 + i, alto=170, luz=par, alcance=900, k=par)
        C.ambiente(h, 0.26)
        h.luz_radial(960, 300, 900, (0.75, 0.35, 0.95), k=0.6 * smooth(clamp01((t - self.t_cara) / 1.0)))
        C.banda(h, "MORADA", 1500, 220, 80, t, self.t_morada, sem=6)
        N.motas(h, t, n=90, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.14, y0=0, y1=H, sem=8, vel=12.0), bloom=0.55)

    def _manos(self, h, t, p, k):
        """Manos aferradas al cuello: muñecas cortas con puño dorado que asoman del cuello de armiño (sube con k 0..1)."""
        if k <= 0:
            return
        T = self.busto._T0(p)
        s = p["s"]
        L = p.get("luz", (0.9, -0.4))
        for i in range(2):
            mano = np.array([10.0 + 70 * i, 176.0 + 16 * i]) + (0, 260 * (1 - k))
            mano[0] += 4 * math.sin(t * 23 + i) * k
            muñeca = mano + (-50 + 40 * i, 120)
            h.pieza(T(np.array([muñeca + (-34, 30), muñeca + (34, 30), mano + (26, 10), mano + (-26, 10)])), 95, 300 + i, w=7 * s, luz=L,
                    d=16 * s, trama=0.4, rim=0.9, rampa="estandarte")
            q = muñeca * 0.6 + mano * 0.4
            h.pieza(T(np.array([q + (-34, 6), q + (34, 6), q + (32, 24), q + (-32, 24)])), 160, 302 + i, w=5 * s, luz=L, d=6 * s,
                    trama=0, rim=1.0, rampa="oro")
            h.pieza(T(blob(mano[0], mano[1], 48, 34, rad=[1, 1.1, 1.0, 0.9, 0.85, 0.95, 1.05, 1.1], n=8)), 118, 304 + i, w=7 * s, luz=L,
                    d=12 * s, trama=0.3, rim=0.9, rampa="piel")
            for f in range(4):
                a0 = mano + (-28 + f * 17, -18)
                h.trazo(T(np.array([a0, a0 + (4 - 2 * i, 30)])), 3.2 * s, 306 + f, color=(14, 12, 16), alfa=0.85)
        h.pieza(T(np.array([[60.0, 168], [100, 172]])), 40, 310, w=0, d=0, sombra=0, trama=0, rim=0, alfa=0.0, linea=False)

    def p_acusa(self, h, t, u):
        pal = h.pal
        k = smooth(clamp01(u / 6.0))
        h.camara(1.0 + 0.05 * k, 960, 560, 0.0)
        h.rim_color(pal["luna"])
        NC.pegar(M.salon_muro(), h, 0.3, rampa="muralla", dx=-200, dy=100, oscuro=0.8)
        sen = smooth(clamp01((t - self.t_senalo + 0.2) / 0.4))
        pr = dict(x=520, y=930, s=1.45, d=1, luz=(0.6, -1.0), mano=(70 + 110 * sen, -330 - 30 * sen),
                  cab=dict(ceño=0.9, boca=0.4 * pulso(t, self.t_senalo, 1.5, 1.0), mira=-0.1))
        rr = clamp01((t - self.t_madre) / 1.2)
        CO.comensales(h, t, -200, 2100, 760, n=11, s=1.0, sem=101, reaccion=rr, mira_x=1500, luz=(0.2, -1.0))
        self.reina.dibujar(h, pr)
        pe = dict(x=1500, y=930, s=1.45, d=-1, luz=(0.2, -1.0), mano=(50, -280), mano2=(40, -270),
                  cab=dict(ceño=0.4, mira=0.3, boca=0.3 * clamp01(t - self.t_tirion)))
        self.enano.dibujar(h, pe)
        me = self.enano.puntos(pe)["mano"]
        P.caliz(h, me[0] - 6, me[1] + 40, 0.38, 0.0, vino=0.0, sem=72)
        C.ambiente(h, 0.28)
        foco = smooth(clamp01((t - self.t_tirion + 0.3) / 0.4))
        h.luz_cono(1500, -600, math.pi / 2, 0.18, 1800, pal["luna"], k=0.4 + 1.4 * foco, suave=0.5)
        h.luz_radial(500, 400, 900, pal["antorcha"], k=0.7)
        C.cartela(h, "Cersei", "la reina madre", 1000, 120, t, self.t_madre + 0.3, px=72, sem=5, sale=self.t_tirion - 0.4)
        C.cartela(h, "Tyrion", "el tío, con la copa en la mano", 1000, 120, t, self.t_tirion - 0.05, px=72, sem=6)
        N.motas(h, t, n=70, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.16, y0=0, y1=H, sem=9, vel=10.0), bloom=0.5)

    def sonidos(self):
        t0 = self.t0
        self.ev(t0, "multitud", 0.35, 0.0, dur=self.t_tosio - t0)
        self.ev(self.t_bebio + 0.2, "taza", 0.5, 0.2)
        self.ev(self.t_tosio, "golpe_grave", 0.6, 0.0)
        self.ev(self.t_tragar, "grave_inquietante", 0.7, 0.0, dur=4.0)
        self.ev(self.t_manos - 0.3, "relampago_corto", 0.6, 0.0)
        self.ev(self.t_cara, "sombra_crece", 0.7, 0.0, dur=3.0)
        self.ev(self.t_madre - 0.35, "barrido_aire", 0.5, 0.0, dur=0.55)
        self.ev(self.t_madre, "multitud", 0.6, 0.0, dur=self.t1 - self.t_madre)
        self.ev(self.t_senalo, "golpe_grave", 0.9, -0.2)
        self.ev(self.t_tirion, "focos", 0.7, 0.3)
        self.ev(self.t1 - 0.8, "tinta_mancha", 0.6, 0.0, dur=0.9)
