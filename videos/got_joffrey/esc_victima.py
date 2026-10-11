# -*- coding: utf-8 -*-
"""Escena 2 «victima»: el rey de perfil entre antorchas, con su sonrisa cruel y la corona que le queda grande (resbala y él la
endereza); cartela con su nombre. Después el rollo de sospechosos se desenrolla sobre la mesa del pesquisidor y cae al suelo
mientras la pluma tacha y añade nombres («medio reino»)."""
import math

import numpy as np

import comun as C
import mundos_j1 as M
import mundos_j3 as M3
import noir as N
import noir_color as NC
import noir_corte as CO
import noir_feudal as NF
import props_j as P
import reparto as RP
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from toon import Pista, pulso

SOSPECHOSOS = ["El tío, al que humilló", "La prometida que repudió", "Los lobos del norte", "Los de la rosa", "El maestro de la moneda",
               "Su propio abuelo", "Los hermanos del rey muerto", "El caballero borracho", "Las casas del sur", "Medio salón"]


class Victima(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.busto = CO.BustoCorte(sem=11, **RP.REY)
        self.t_vic = w("víctima")
        self.t_yof = w("Yófrey")
        self.t_rey = w("rey de")
        self.t_corona = w("corona")
        self.t_grande = w("grande")
        self.t_cru = w("crueldad")
        self.t_con = w("Con tantos")
        self.t_lista = w("lista")
        self.t_medio = w("medio reino")
        self.plano(t0, self.p_rey)
        self.plano(self.t_con - 0.35, self.p_lista, tr="barrido", dur=0.6, dirx=-1)

    def p_rey(self, h, t, u):
        pal = h.pal
        k = smooth(clamp01(u / 8.0))
        h.camara(1.0 + 0.05 * k, 960 - 30 * k, 540, -0.005)
        h.rim_color(pal["antorcha"])
        NC.pegar(M.estrado_muro(), h, 0.4, rampa="muralla", dx=-260, dy=40)
        with h.capa(0.4):
            NF.estandarte(h, t, 1240, -120, w=260, hh=620, sem=21, emblema="sol", viento=0.12)
            NF.antorcha(h, t, 260, 260, s=1.1, sem=22, luz=1.0, alcance=700)
            NF.antorcha(h, t, 1700, 300, s=1.1, sem=23, luz=0.9, alcance=700)
        # la corona resbala sobre la frente y él la endereza con fastidio
        res = pulso(t, self.t_corona - 0.2, 1.6, 1.0)
        son = 0.55 + 0.25 * math.sin(t * 0.8) - 0.6 * res
        p = dict(x=820, y=470, s=1.15, d=1, luz=(0.9, -0.4), rim=0.95, sonrisa=son, ceño=0.35 + 0.5 * res, mira=-0.1,
                 cab_rot=-0.03 * res + 0.015 * math.sin(t * 0.6), boca=0.18 * pulso(t, self.t_cru - 0.1, 0.7, 1.0))
        # la corona dibujada aparte (desplazada) cuando resbala: se esconde la del busto
        self.busto.r["corona"] = None if res > 0.02 else "rey"
        self.busto.dibujar(h, p)
        if res > 0.02:
            q = CO.BustoCorte(sem=11, **dict(RP.REY, pelo="ninguno"))
            q.r["corona"] = "rey"
            q.cabeza(h, dict(p, cab_rot=p["cab_rot"] + 0.22 * res, y=p["y"] + 26 * res * 1.15, x=p["x"] + 22 * res, boca=0, _t=t,
                             hombros=False, ojo=0.0))
        self.busto.r["corona"] = "rey"
        C.ambiente(h, 0.3)
        h.luz_radial(1500, 300, 1200, pal["antorcha"], k=0.9)
        h.luz_radial(300, 300, 900, pal["antorcha"], k=0.6)
        C.cartela(h, "Joffrey", "rey de los Siete Reinos", 1460, 820, t, self.t_yof, px=96, sem=4)
        N.motas(h, t, n=80, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.14, y0=0, y1=H, sem=4, vel=10.0), bloom=0.5)

    def p_lista(self, h, t, u):
        pal = h.pal
        tl = self.t_lista - 0.3
        dl = smooth(clamp01((t - tl) / 2.6))
        largo = 120 + 1500 * dl
        cam_y = 380 + 520 * smooth(clamp01((t - tl - 0.6) / 2.6))
        h.camara(1.0, 960, cam_y, 0.0)
        h.rim_color(pal["vela"])
        NC.pegar(M3.tablero(), h, 1.0, rampa="madera", dy=0)
        NC.pegar(M3.tablero(), h, 1.0, rampa="madera", dy=1600)
        T = P.rollo(h, t, 960, 140, largo, s=1.0, sem=30, ancho=760)
        N.texto_maquina(h, "Sospechosos", *T([[0, 74]])[0], 84, t, -99, cps=1e9, tono=np.array(pal["tinta"]) * 2.0, centro=True,
                        fuente=NF.FUENTE_GOTICA)
        for i, s in enumerate(SOSPECHOSOS):
            y = 210 + i * 128
            if y > largo - 60:
                break
            t_i = tl + 0.3 + i * 0.32
            N.texto_maquina(h, s, *T([[-320, y]])[0], 50, t, t_i, cps=30, tono=np.array(pal["tinta"]) * 2.2, fuente=NF.FUENTE_PLUMA_R)
            if i % 3 == 1 and t > t_i + 1.0:                                       # tachaduras a pluma
                a = clamp01((t - t_i - 1.0) / 0.3)
                p0 = T([[-326, y + 26]])[0]
                p1 = T([[-326 + 620 * a, y + 22]])[0]
                h.trazo([p0, p1], 4, 40 + i, color=(40, 20, 20), alfa=0.85)
        NF.vela(h, t, 420, 300, s=1.2, sem=50, alto=180, luz=1.1, alcance=1100)
        NF.vela(h, t, 1520, 900, s=1.0, sem=51, alto=120, luz=0.9, alcance=900)
        P.caliz(h, 1500, 520, 0.7, 0.0, sem=60)
        C.ambiente(h, 0.3)
        C.banda(h, "MEDIO REINO", 960, 960, 66, t, self.t_medio, sem=9)
        N.motas(h, t, n=70, k=0.5)
        return h.acabado(t, niebla=None, bloom=0.45)

    def sonidos(self):
        t0 = self.t0
        self.ev(t0, "lampara_chisporrotea", 0.4, 0.0, dur=self.t_con - t0)
        self.ev(self.t_yof, "golpe_grave", 0.7, 0.0)
        self.ev(self.t_corona - 0.1, "corona_cae", 0.4, 0.2)
        self.ev(self.t_con - 0.35, "barrido_aire", 0.5, 0.0, dur=0.6)
        self.ev(self.t_lista - 0.3, "papel_viento", 0.7, 0.0)
        self.ev(self.t_lista, "lapiz", 0.5, -0.2, dur=2.5)
        self.ev(self.t_medio, "sello_golpe", 0.9, 0.0)
        self.ev(self.t1 - 0.7, "tinta_mancha", 0.5, 0.0, dur=0.8)
