# -*- coding: utf-8 -*-
"""Escena 3 «banquete»: travelling a lo largo de la mesa del banquete (tapices, invitados que charlan y beben, músicos en el arco
de las cocinas, jarras que sirven) con «77 PLATOS»; el rey en el estrado alza la espada y parte la empanada gigante: salen las
palomas; junto al arco de las cocinas el rey tiende la copa vacía hacia abajo y el tío enano se acerca con la jarra entre risas."""
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
from toon import Pista, pulso


class Banquete(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.rey = CO.Cortesano(sem=31, **RP.REY)
        self.reina = CO.Cortesano(sem=32, **RP.REINA)
        self.enano = CO.Cortesano(sem=33, **RP.ENANO)
        self.t_horas = w("horas")
        self.t_77 = w("Setenta")
        self.t_mus = w("músicos")
        self.t_vino = w("vino")
        self.t_rey = w("El rey")
        self.t_partio = w("partió")
        self.t_emp = w("empanada")
        self.t_dentro = w("De dentro")
        self.t_palomas = w("palomas")
        self.t_hum = w("humillar")
        self.t_tirion = w("Tirion")
        self.t_obl = w("obligó")
        self.t_copa = w("copa")
        self.plano(t0, self.p_mesa)
        self.plano(self.t_rey - 0.35, self.p_empanada, tr="humo", dur=0.6)
        self.plano(self.t_hum - 0.35, self.p_enano, tr="barrido", dur=0.55, dirx=1)

    # ------------------------------------------------------------------ la mesa del banquete
    def p_mesa(self, h, t, u):
        pal = h.pal
        h.camara(1.0, 520 + 95 * u, 520, 0.0)
        h.rim_color(pal["vela"])
        NC.pegar(M.tapiz_muro(), h, 0.6, rampa="muralla")
        NC.pegar(M.tapices(), h, 0.6, rampa="estandarte")
        with h.capa(0.6):
            for x in (300, 2240):
                NF.antorcha(h, t, x, 100, s=1.0, sem=int(x), luz=0.9, alcance=600)
            P.musico(h, t, 1180, 560, 0.9, "laud", sem=3)
            P.musico(h, t, 1330, 560, 0.9, "tambor", sem=7, d=-1)
        CO.comensales(h, t, -600, 2700, 600, n=17, s=1.6, sem=41, luz=(0.2, -1.0))
        NC.pegar(M.mesa_larga(), h, 1.0, rampa="pergamino")
        for i, x in enumerate((-300, 300, 900, 1500, 2100, 2700)):
            NF.vela(h, t, x, 600, s=1.0, sem=70 + i, alto=120, luz=0.9, alcance=650)
        # un criado sirve vino desde una jarra (la jarra se inclina y cae el chorro)
        inc = 0.8 * pulso(t, self.t_vino - 0.6, 2.4, 1.0)
        boca = P.jarra(h, 1720, 560 - 120 * inc, 1.0, -inc, sem=80)
        if inc > 0.3:
            h.trazo([boca, (boca[0] - 6, 590)], 6, 81, color=h.c(90, "vino"), alfa=0.9)
        C.ambiente(h, 0.3)
        h.luz_radial(1200, 300, 900, pal["vela"], k=0.6)
        C.banda(h, "77 PLATOS", 1500, 180, 70, t, self.t_77, claro=True, sem=5)
        N.motas(h, t, n=80, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.14, y0=0, y1=H, sem=3, vel=10.0), bloom=0.5)

    # ------------------------------------------------------------------ la espada, la empanada y las palomas
    def p_empanada(self, h, t, u):
        pal = h.pal
        tg = self.t_partio + 0.1                                                     # el golpe
        sac = pulso(t, tg - 0.05, 0.25, 1.0)
        z = 1.0 + 0.04 * u + 0.05 * sac
        h.camara(z, 960, 560 + 10 * sac, 0.0)
        h.rim_color(pal["vela"])
        NC.pegar(M.estrado_muro(), h, 0.7, rampa="muralla")
        with h.capa(0.7):
            NF.estandarte(h, t, 330, -330, w=200, hh=560, sem=51, emblema="sol", viento=0.1)
            NF.estandarte(h, t, 1390, -330, w=200, hh=560, sem=52, emblema="sol", viento=0.1)
        NC.pegar(M.estrado(), h, 0.85, rampa="madera")
        # el rey con la espada en alto: alza (anticipa) y baja de golpe
        alza = smooth(clamp01((t - (tg - 1.4)) / 0.9))
        baja = e_out(clamp01((t - tg + 0.12) / 0.12))
        ang = -1.9 * alza * (1 - baja) + (-0.25) * baja
        mano = (60 + 40 * baja, -440 + 260 * baja)
        pr = dict(x=820, y=820, s=1.25, d=1, luz=(0.5, -1.0), mano=mano, mano2=(70, -300 + 40 * baja),
                  cab=dict(sonrisa=0.7, ceño=0.2, boca=0.25 * pulso(t, self.t_dentro, 1.2, 1.0)))
        self.reina.dibujar(h, dict(x=560, y=820, s=1.2, d=1, luz=(0.5, -1.0), cab=dict(sonrisa=0.3)))
        self.rey.dibujar(h, pr)
        m = self.rey.puntos(pr)["mano"]
        P.espada(h, m[0], m[1], ang - 0.0, 1.0, sem=60, brillo=clamp01((t - tg + 1.0) / 0.8) if t < tg else 0.0)
        # mesa alta con la empanada
        with h.con_rampa("pergamino"):
            h.pieza(C.rect(560, 880, 1000, 60), 200, 70, w=4, d=8, trama=0.2, rim=0.6)
            h.pieza(C.rect(560, 940, 1000, 220), 160, 71, w=4, d=8, trama=0.3, rim=0.4)
        P.empanada(h, t, 1180, 880, 1.0, corte=baja, sem=72)
        P.palomas(h, t, self.t_palomas - 0.25, 1180, 700, n=11, s=1.0, sem=73)
        for i, x in enumerate((640, 1500)):
            NF.vela(h, t, x, 880, s=1.0, sem=80 + i, alto=150, luz=1.0, alcance=800)
        CO.comensales(h, t, 100, 1820, 1180, n=8, s=2.0, sem=91, luz=(0.2, -1.0), copas=False)
        C.ambiente(h, 0.3)
        h.luz_radial(960, 500, 1100, pal["vela"], k=0.8)
        h.luz_radial(1180, 700, 600, pal["vela"], k=0.8 * sac)
        N.motas(h, t, n=80, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.14, y0=0, y1=H, sem=5, vel=10.0), bloom=0.5, flash=0.15 * sac)

    # ------------------------------------------------------------------ el tío le sirve la copa
    def p_enano(self, h, t, u):
        pal = h.pal
        k = smooth(clamp01(u / 5.0))
        h.camara(1.15 + 0.06 * k, 1240, 640, 0.0)
        h.rim_color(pal["vela"])
        NC.pegar(M.tapiz_muro(), h, 0.7, rampa="muralla", dx=-520, emis=0.35)
        NC.pegar(M.tapices(), h, 0.7, rampa="estandarte", dx=-520)
        with h.capa(0.7):
            NF.antorcha(h, t, 600, 120, s=1.0, sem=8, luz=0.9, alcance=600)
        ta = self.t_tirion - 0.4
        xe = 1700 - 300 * smooth(clamp01((t - ta) / 1.6))
        dt = 1 / 60
        vel = abs((1700 - 300 * smooth(clamp01((t + dt - ta) / 1.6))) - (1700 - 300 * smooth(clamp01((t - dt - ta) / 1.6)))) / (2 * dt)
        tiende = smooth(clamp01((t - self.t_obl + 0.3) / 0.6))
        pr = dict(x=1080, y=900, s=1.3, d=1, luz=(0.6, -1.0), mano=(60 + 40 * tiende, -330 + 40 * tiende),
                  cab=dict(sonrisa=0.8, ceño=0.3, mira=-0.4, boca=0.2 * math.sin(t * 6) ** 2 * (t > self.t_hum)))
        self.rey.dibujar(h, pr)
        m = self.rey.puntos(pr)["mano"]
        P.caliz(h, m[0] + 4, m[1] + 30, 0.42, 2.9 * tiende, vino=0.0, sem=40)       # la copa boca abajo: vacía
        pe = dict(x=xe, y=900, s=1.3, d=-1, luz=(0.6, -1.0), andar=clamp01(vel / 120), paso=(1700 - xe) / 50.0,
                  mano=(50, -250), cab=dict(ceño=0.7, mira=0.5, sonrisa=-0.3))
        self.enano.dibujar(h, pe)
        me = self.enano.puntos(pe)["mano"]
        P.jarra(h, me[0] - 10, me[1] + 60, 0.42, 0.1, sem=41)
        # risas de la corte en primer plano
        CO.comensales(h, t, 300, 2200, 1240, n=7, s=2.4, sem=93, luz=(0.2, -1.0), copas=False)
        C.ambiente(h, 0.3)
        h.luz_radial(1240, 500, 1000, pal["vela"], k=0.9)
        C.banda(h, "SU COPERO", 1240, 200, 60, t, self.t_copa - 0.2, claro=True, sem=8)
        N.motas(h, t, n=70, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.12, y0=0, y1=H, sem=6, vel=10.0), bloom=0.45)

    def sonidos(self):
        t0 = self.t0
        self.ev(t0, "multitud", 0.5, 0.0, dur=self.t1 - t0)
        self.ev(self.t_mus, "caja_musica", 0.3, 0.3, dur=4.0)
        self.ev(self.t_vino - 0.4, "cafe_sirve", 0.6, 0.4)
        self.ev(self.t_77, "golpe_grave", 0.6, 0.0)
        self.ev(self.t_rey - 0.35, "barrido_aire", 0.5, 0.0, dur=0.6)
        self.ev(self.t_partio - 0.2, "revolver_desliza", 0.5, -0.2)
        self.ev(self.t_partio + 0.1, "golpe_grave", 1.0, 0.0)
        self.ev(self.t_palomas - 0.25, "papel_viento", 0.7, 0.2, dur=2.0)
        self.ev(self.t_hum - 0.35, "barrido_aire", 0.5, 0.0, dur=0.55)
        self.ev(self.t_tirion - 0.3, "paso_madera", 0.5, 0.3)
        self.ev(self.t_copa - 0.2, "periodico_golpe", 0.6, 0.0)
        self.ev(self.t1 - 0.7, "tinta_mancha", 0.5, 0.0, dur=0.8)
