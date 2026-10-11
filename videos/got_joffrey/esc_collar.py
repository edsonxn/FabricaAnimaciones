# -*- coding: utf-8 -*-
"""Escena 7 «collar»: Sansa de perfil bajo la luna con el collar de piedras oscuras (cartela); en el jardín, Ser Dontos, bufón
borracho que se tambalea con la jarra, le tiende el collar; en la terraza de la boda, entre guirnaldas de faroles, la anciana del
bastón se acerca y le acomoda el collar; primer plano del collar sobre la seda azul: al engaste del centro le falta la piedra."""
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


class Collar(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.busto = CO.BustoCorte(sem=21, **RP.SANSA)
        self.sansa = CO.Cortesano(sem=22, **RP.SANSA)
        self.dontos = CO.Cortesano(sem=23, **RP.DONTOS)
        self.vieja = CO.Cortesano(sem=24, **RP.ANCIANA)
        self.t_sansa = w("Sansa")
        self.t_collar = w("collar")
        self.t_regalo = w("Regalo")
        self.t_borr = w("borracho")
        self.t_dontos = w("Dontos")
        self.t_durante = w("Durante")
        self.t_anciana = w("anciana")
        self.t_acom = w("acomodárselo")
        self.t_al = w("Al terminar")
        self.t_faltaba = w("faltaba")
        self.t_piedra = w("piedra")
        self.plano(t0, self.p_sansa)
        self.plano(self.t_regalo - 0.35, self.p_dontos, tr="barrido", dur=0.55, dirx=1)
        self.plano(self.t_durante - 0.35, self.p_terraza, tr="humo", dur=0.6)
        self.plano(self.t_al - 0.35, self.p_falta, tr="empuje", dur=0.5, centro=(W * 0.5, H * 0.45))

    def p_sansa(self, h, t, u):
        pal = h.pal
        k = smooth(clamp01(u / 5.0))
        h.camara(1.0 + 0.05 * k, 960, 540, 0.0)
        h.rim_color(pal["luna"])
        NC.pegar(M2.jardin_cielo(), h, 0.15, rampa="cielo", dx=-500, dy=200)
        NC.pegar(M2.jardin_arboles(), h, 0.35, rampa="tela_verde", bruma=0.3, dx=-300)
        p = dict(x=820, y=440, s=1.1, d=1, luz=(0.9, -0.5), rim=0.95, mira=-0.5 + 0.3 * pulso(t, self.t_collar, 1.5, 1.0),
                 sonrisa=0.1, falta=False)
        self.busto.dibujar(h, p)
        gl = pulso(t, self.t_collar + 0.2, 1.0, 1.0)
        for q in self.busto.piedras():
            h.emitir(elipse_(q[0], q[1], 10, 12, n=10), 0.3 * gl, col=(0.7, 0.25, 0.9))
        C.ambiente(h, 0.6)
        h.luz_radial(1500, 0, 1200, pal["luna"], k=0.7)
        h.luz_radial(300, 900, 900, pal["antorcha"], k=0.5)
        C.cartela(h, "Sansa Stark", "la antigua prometida del rey", 1460, 180, t, self.t_sansa, px=80, sem=5)
        N.motas(h, t, n=60, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.14, y0=0, y1=H, sem=14, vel=8.0), bloom=0.45)

    def p_dontos(self, h, t, u):
        pal = h.pal
        k = smooth(clamp01(u / 4.0))
        h.camara(1.0 + 0.04 * k, 960, 460, 0.0)
        h.rim_color(pal["luna"])
        NC.pegar(M2.jardin_cielo(), h, 0.1, rampa="cielo")
        NC.pegar(M2.jardin_arboles(), h, 0.7, rampa="tela_verde", bruma=0.14)
        NC.pegar(M2.jardin_suelo(), h, 1.0, rampa="tela_verde")
        tamb = math.sin(t * 1.7)
        tiende = smooth(clamp01((t - self.t_regalo) / 0.6))
        pd = dict(x=1180, y=1000, s=1.5, d=-1, luz=(0.3, -1.0), rot=0.06 * tamb, mano=(60 + 50 * tiende, -300 - 20 * tiende),
                  mano2=(30, -330), cab=dict(sonrisa=0.6, boca=0.25 * abs(math.sin(t * 2.5)), ojo=0.6, cab_rot=0.08 * tamb))
        self.dontos.dibujar(h, pd)
        md = self.dontos.puntos(pd)["mano"]
        P.collar_grande(h, t, md[0] - 30, md[1] + 10, 0.12, falta=-1, n=7, sem=40)
        ps = dict(x=640, y=1000, s=1.5, d=1, luz=(0.3, -1.0), mano=(40 + 30 * tiende, -280), falta=False, cab=dict(mira=-0.3))
        self.sansa.dibujar(h, ps)
        # la jarra que lleva en la otra mano, colgando
        P.jarra(h, md[0] + 160, md[1] + 120, 0.4, 0.3 * tamb, sem=41)
        C.ambiente(h, 1.0)
        h.luz_radial(1500, -200, 1300, pal["luna"], k=0.8)
        h.luz_radial(900, 700, 700, pal["antorcha"], k=0.4)
        C.cartela(h, "Ser Dontos", "caballero, bufón y borracho", 1460, 160, t, self.t_dontos - 0.1, px=76, sem=6)
        N.motas(h, t, n=50, k=0.4)
        return h.acabado(t, niebla=dict(dens=0.18, y0=0, y1=H, sem=15, vel=8.0), bloom=0.45)

    def p_terraza(self, h, t, u):
        pal = h.pal
        k = smooth(clamp01(u / 5.0))
        h.camara(1.04 + 0.08 * k, 1060, 560, 0.0)
        h.rim_color(pal["antorcha"])
        NC.pegar(M2.terraza_fondo(), h, 0.2, rampa="cielo")
        NC.pegar(M2.terraza_balaustrada(), h, 1.0, rampa="muralla")
        # guirnalda de faroles sobre la terraza
        P0, P1 = np.array([-100.0, 120]), np.array([2000.0, 160])
        pts = [P0 + (P1 - P0) * v + (0, 200 * math.sin(math.pi * v)) for v in np.linspace(0, 1, 40)]
        h.trazo(np.array(pts), 3, 10, color=(30, 24, 20), alfa=0.9)
        tot = 0
        for j, v in enumerate(np.linspace(0.1, 0.9, 6)):
            q = P0 + (P1 - P0) * v + (0, 200 * math.sin(math.pi * v))
            with h.con_rampa("pergamino"):
                h.pieza(elipse_(q[0], q[1] + 40, 24, 32, n=16), 200, 11 + j, w=2.5, d=3, trama=0, rim=0.6)
            h.emitir(elipse_(q[0], q[1] + 40, 20, 28, n=14), 0.8, col=h.pal["antorcha"])
            h.luz_radial(q[0], q[1] + 40, 380, pal["antorcha"], k=0.45)
        # la anciana se acerca y le acomoda el collar
        ta = self.t_anciana - 0.6
        xv = 1640 - 310 * smooth(clamp01((t - ta) / 1.4))
        dt = 1 / 60
        vel = abs(310 * (smooth(clamp01((t + dt - ta) / 1.4)) - smooth(clamp01((t - dt - ta) / 1.4)))) / (2 * dt)
        acom = smooth(clamp01((t - self.t_acom + 0.3) / 0.5))
        ps = dict(x=860, y=980, s=1.7, d=1, luz=(0.3, -1.0), falta=False, cab=dict(mira=-0.2, sonrisa=0.2 * acom))
        self.sansa.dibujar(h, ps)
        pv = dict(x=xv, y=980, s=1.7, d=-1, luz=(0.3, -1.0), andar=clamp01(vel / 100), paso=(1640 - xv) / 40.0,
                  mano=(80 + 130 * acom + 6 * math.sin(t * 6) * acom, -330 - 40 * acom), mano2=(40, -240), inclina=0.06 + 0.32 * acom, baston_mano="atras",
                  cab=dict(sonrisa=0.5, mira=-0.2))
        self.vieja.dibujar(h, pv)
        C.ambiente(h, 0.6)
        h.luz_radial(1000, 500, 900, pal["antorcha"], k=0.6)
        C.banda(h, "UNA ANCIANA", 1500, 160, 56, t, self.t_anciana, claro=True, sem=7)
        N.motas(h, t, n=60, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.12, y0=0, y1=H, sem=16, vel=8.0), bloom=0.5)

    def p_falta(self, h, t, u):
        pal = h.pal
        zoom = smooth(clamp01((t - self.t_faltaba + 0.4) / 1.4))
        q0 = (960, 560)
        h.camara(1.0 + 0.6 * zoom, 960 + 0 * zoom, 420 + 140 * zoom, -0.02)
        h.rim_color(pal["vela"])
        NC.pegar(M3.terciopelo(), h, 1.0, rampa="azul")
        pts = P.collar_grande(h, t, 960, 220, 1.6, falta=3, n=7, sem=50, ang=-0.02)
        q = pts[3]
        h.luz_radial(q[0], q[1], 500, pal["vela"], k=0.8 * zoom)
        C.ambiente(h, 0.4)
        h.luz_radial(960, 400, 1000, pal["vela"], k=1.0)
        C.banda(h, "FALTA UNA PIEDRA", 960, 940, 62, t, self.t_piedra - 0.1, sem=8)
        N.motas(h, t, n=50, k=0.4)
        return h.acabado(t, niebla=None, bloom=0.5)

    def sonidos(self):
        t0 = self.t0
        self.ev(t0, "lluvia_lejana", 0.3, 0.0, dur=self.t_durante - t0)
        self.ev(self.t_collar + 0.2, "oro_brillo", 0.5, 0.2)
        self.ev(self.t_regalo - 0.35, "barrido_aire", 0.5, 0.0, dur=0.55)
        self.ev(self.t_borr, "hilo_tenso", 0.3, -0.3)
        self.ev(self.t_durante - 0.35, "multitud", 0.35, 0.0, dur=self.t_al - self.t_durante + 0.3)
        self.ev(self.t_anciana - 0.6, "paso_firme", 0.4, 0.4)
        self.ev(self.t_acom, "fichas_empuja", 0.4, 0.0)
        self.ev(self.t_al - 0.35, "barrido_aire", 0.5, 0.0, dur=0.5)
        self.ev(self.t_faltaba, "grave_inquietante", 0.6, 0.0, dur=3.0)
        self.ev(self.t_piedra - 0.1, "golpe_grave", 0.9, 0.0)
        self.ev(self.t1 - 0.7, "tinta_mancha", 0.5, 0.0, dur=0.8)
