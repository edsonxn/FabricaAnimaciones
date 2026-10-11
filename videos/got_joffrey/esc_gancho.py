# -*- coding: utf-8 -*-
"""Escena 1 «gancho»: grúa desde la fortaleza en fiesta hasta la calle mojada donde llega el pesquisidor con su farol
(«he visto morir a muchos hombres»); el gran salón desde la galería con los mil invitados, candelabros y el rey en el estrado
alzando la copa; la copa de oro cae sobre las losas y el vino salpica mientras las sombras de los invitados se alargan
(«nadie vio quién lo mató»); sobre el mantel blanco se extiende la mancha púrpura y aparece el título; ENVENENAMIENTO."""
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
from noir_pers import Detective, avance_paso
from toon import Pista, pulso, suave


class Gancho(BaseNoir):
    TR_SALIDA = ("tinta", 0.8)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.pesq = NF.Pesquisidor(sem=3)
        self.rey = CO.Cortesano(sem=31, **RP.REY)
        self.t_visto = w("visto")
        self.t_nunca = w("Nunca")
        self.t_del = w("delante")
        self.t_boda = w("boda")
        self.t_mil = w("mil")
        self.t_todos = w("Todos")
        self.t_caer = w("caer")
        self.t_nadie = w("Nadie")
        self.t_mato = w("mató")
        self.t_llam = w("Lo llamaron")
        self.t_purp = w("Púrpura")
        self.t_yo = w("Yo lo")
        self.t_env = w("envenenamiento")
        tb = self.t_del - 0.35
        self.cam_c = Pista([(t0, (900.0, -900.0, 0.9)), (t0 + 0.8, (900.0, -860.0, 0.9), "io"), (t0 + 4.6, (980.0, 520.0, 1.0), "io"),
                            (tb + 0.8, (1060.0, 560.0, 1.08), "io")])
        self.px = Pista([(t0, -150.0), (t0 + 1.5, -150.0), (t0 + 6.6, 860.0, "io"), (tb + 1, 860.0)])
        self.alza = Pista([(t0, 0.0), (t0 + 6.4, 0.0), (t0 + 7.2, 0.85, "io")])
        self.plano(t0, self.p_ciudad)
        self.plano(tb, self.p_salon, tr="humo", dur=0.7)
        self.plano(self.t_todos - 0.35, self.p_copa, tr="barrido", dur=0.55, dirx=1)
        self.plano(self.t_llam - 0.35, self.p_mantel, tr="tinta", dur=0.6)

    # ------------------------------------------------------------------ la ciudad en fiesta y el pesquisidor
    def p_ciudad(self, h, t, u):
        pal = h.pal
        cx, cy, z = self.cam_c(t)
        h.camara(z, cx, cy, 0.008 * math.sin(t * 0.4))
        h.rim_color(pal["luna"])
        NC.pegar(M.cielo_fiesta(), h, 0.05, rampa="cielo", dx=t * 4.0)
        NC.pegar(M.fortaleza(), h, 0.3, rampa="ladrillo", bruma=0.24, emis=1.1)
        NC.pegar(M.tejados(), h, 0.6, rampa="entramado", bruma=0.2)
        NC.pegar(M.calle_fiesta(), h, 1.0, rampa="entramado", emis=0.95)
        NC.pegar(M.empedrado(), h, 1.0, rampa="muralla")
        NF.estandarte(h, t, 1400, 330, w=150, hh=340, sem=5, emblema="sol", viento=1.0)
        NF.estandarte(h, t, 120, 420, w=130, hh=300, sem=6, emblema="sol", viento=0.8)
        x = self.px(t)
        dt = 1 / 60
        vel = abs(self.px(t + dt) - self.px(t - dt)) / (2 * dt)
        s = 0.95
        self.pesq.dibujar(h, dict(x=x, y=M.Y_CALLE + 10, s=s, d=1, luz=(0.4, -1.0), rim=0.95, andar=clamp01(vel / 150.0),
                                  paso=(x + 150.0) / avance_paso(Detective.ZANCADA, s), alzar=float(self.alza(t)),
                                  arriba=float(self.alza(t)) * 0.7, viento=0.35 + 0.15 * math.sin(t * 1.7), hombros=0.2,
                                  capa=0.2 * math.sin(t * 1.1) ** 2))
        C.ambiente(h, 0.8)
        h.luz_cono(400, -700, math.pi / 2 + 0.3, 0.9, 2600, pal["luna"], k=0.25, suave=0.8)
        NF.antorcha(h, t, 1290, 600, s=0.9, sem=7, luz=1.1, alcance=640)
        h.luz_radial(900, -60, 1200, pal["antorcha"], k=0.5)                       # el resplandor del salón en fiesta
        C.reflejar(h, t, M.Y_CALLE + 14)
        N.lluvia(h, t, n=460, vel=1300.0)
        y0 = h.tf(np.array([[0, M.Y_CALLE]]))[0][1]
        if y0 < H:
            N.salpicaduras(h, t, max(0, y0), H, n=50)
        return h.acabado(t, niebla=dict(dens=0.28, y0=0, y1=H, sem=1), flash=0.4 * N.relampago(t, [self.t_visto - 0.2]))

    # ------------------------------------------------------------------ el gran salón y los mil invitados
    def p_salon(self, h, t, u):
        pal = h.pal
        k = smooth(clamp01(u / 6.0))
        h.camara(1.0 + 0.10 * k, 960, 520 - 20 * k, 0.0)
        h.rim_color(pal["vela"])
        NC.pegar(M.salon_muro(), h, 1.0, rampa="muralla")
        NC.pegar(M.salon_ventanas(), h, 1.0, rampa="hierro", col_emis=pal["luna"], emis=0.9)
        NC.pegar(M.salon_suelo(), h, 1.0, rampa="muralla")
        # estandartes en las columnas
        for i, (x, y, ww, hh) in enumerate(((60, 0, 120, 360), (1740, 0, 120, 360), (330, 160, 70, 220), (1520, 160, 70, 220))):
            NF.estandarte(h, t, x, y, w=ww, hh=hh, sem=40 + i, emblema="sol", viento=0.15)
        NC.pegar(M.salon_mesas(), h, 1.0, rampa="pergamino")
        # el rey en el estrado alza la copa
        al = smooth(clamp01((t - self.t_boda) / 0.6))
        self.rey.dibujar(h, dict(x=960, y=522, s=0.22, d=1, luz=(0.2, -1.0), mano=(40, -300 - 160 * al)))
        pr = self.rey.puntos(dict(x=960, y=522, s=0.22, d=1, mano=(40, -300 - 160 * al)))
        P.caliz(h, pr["mano"][0], pr["mano"][1] + 4, 0.08, 0.0)
        # invitados a los dos lados de cada mesa, de atrás hacia delante
        for j, f in enumerate(np.linspace(0.04, 0.92, 9)):
            y = 600 + 700 * f
            sc = 0.22 + 0.95 * f
            for sx in (-1, 1):
                xo = (820 + (200 - 820) * f) if sx < 0 else (1100 + (1720 - 1100) * f)
                xi = (900 + (760 - 900) * f) if sx < 0 else (1020 + (1160 - 1020) * f)
                CO.comensales(h, t, xo - sx * 30 * sc, xo - sx * 30 * sc, y, n=1, s=sc, sem=j * 13 + (sx > 0) * 7,
                              luz=(0.0, -1.0), reaccion=0.0)
                CO.comensales(h, t, xi + sx * 20 * sc, xi + sx * 20 * sc, y + 10 * sc, n=1, s=sc, sem=j * 17 + 3 + (sx > 0) * 5,
                              luz=(0.0, -1.0))
        for i, (x, y, r, s) in enumerate(((960, 150, 120, 0.7), (960, -40, 200, 1.0), (960, -260, 300, 1.3))):
            P.candelabro(h, t, x, y, r, s=s, sem=60 + i * 9, cadena=420, luz=0.9, alcance=700)
        C.ambiente(h, 0.32)
        h.luz_radial(960, 300, 1300, pal["vela"], k=0.7)
        C.banda(h, "MIL INVITADOS", 960, 960, 54, t, self.t_mil, claro=True, sem=5)
        N.motas(h, t, n=90, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.16, y0=0, y1=H, sem=2, vel=8.0), bloom=0.55)

    # ------------------------------------------------------------------ la copa cae
    def p_copa(self, h, t, u):
        pal = h.pal
        tc = self.t_caer - 0.25
        h.camara(1.0 + 0.03 * u, 960, 560, 0.0)
        h.rim_color(pal["vela"])
        NC.pegar(M.losas(), h, 1.0, rampa="muralla")
        # sombras de los invitados que se acercan (crecen desde los bordes)
        cre = smooth(clamp01((t - self.t_nadie + 0.3) / 2.2))
        for i, (bx, ang) in enumerate(((-200, 0.5), (300, 0.25), (1700, -0.3), (2200, -0.55), (960, 0.0))):
            L = 300 + 700 * cre
            c = np.array([bx, 1400.0])
            d = np.array([math.sin(ang), -1.0])
            q = c + d * L
            n_ = np.array([-d[1], d[0]])
            Pp = suave([c - n_ * 90, q - n_ * 70, q + d * 60, q + n_ * 70, c + n_ * 90], 3)
            h.pieza(Pp, 6, 200 + i, w=0, d=0, sombra=0, trama=0, rim=0, alfa=0.55 * (0.4 + 0.6 * cre), linea=False, rampa="personaje")
        # el cáliz: cae girando, rebota y rueda
        if t < tc:
            y = -400 + 0 * u
            P.caliz(h, 980, 700 - 1100 * (1 - clamp01((t - (tc - 0.9)) / 0.9)) ** 2, 1.25, -0.4 - 2.2 * clamp01((t - tc + 0.9) / 0.9))
        else:
            v = t - tc
            reb = 60 * abs(math.sin(min(v, 0.5) * 2 * math.pi)) * math.exp(-v * 5)
            ang = -1.57 - 0.1 * math.sin(v * 3) * math.exp(-v)
            P.gotas_vino(h, t, tc, 820, 790, n=30, sem=7, s=1.2)
            P.caliz(h, 980 + 140 * (1 - math.exp(-v * 1.6)), 760 - reb, 1.1, ang, vino=0.0)
        C.ambiente(h, 0.3)
        h.luz_radial(960, 600, 900, pal["vela"], k=1.4)
        h.luz_radial(400, 200, 700, pal["vela"], k=0.5)
        C.banda(h, "NADIE VIO QUIÉN", 960, 150, 58, t, self.t_mato - 0.4, sem=7)
        N.motas(h, t, n=70, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.12, vel=8, y0=0, y1=H, sube=False), bloom=0.5)

    # ------------------------------------------------------------------ la mancha púrpura y el título
    def p_mantel(self, h, t, u):
        pal = h.pal
        k = smooth(clamp01(u / 6.0))
        h.camara(1.0 + 0.06 * k, 960, 540, 0.02 - 0.02 * k)
        h.rim_color(pal["vela"])
        NC.pegar(M3.mantel(), h, 1.0, rampa="papel")
        r = 80 + 520 * (1 - math.exp(-u * 0.9))
        rng = np.random.default_rng(3)
        borde = [(960 + r * (1 + 0.18 * math.sin(a * 5 + 1) + 0.08 * math.sin(a * 11)) * math.cos(a),
                  540 + r * 0.62 * (1 + 0.15 * math.sin(a * 4)) * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 40, endpoint=False)]
        h.pieza(np.array(borde), 100, 300, w=0, d=0, sombra=0, trama=0, rim=0, alfa=0.85, linea=False, rampa="purpura")
        h.pieza(np.array(borde) * 0.8 + (192, 108), 70, 301, w=0, d=0, sombra=0, trama=0, rim=0, alfa=0.7, linea=False, rampa="purpura")
        for i in range(9):                                                         # gotas alrededor
            a = rng.uniform(0, 2 * math.pi)
            rr = r * rng.uniform(1.05, 1.4)
            h.pieza(np.array([(960 + rr * math.cos(a) + 14 * math.cos(b), 540 + rr * 0.62 * math.sin(a) + 10 * math.sin(b))
                              for b in np.linspace(0, 2 * math.pi, 10)]), 90, 310 + i, w=0, d=0, sombra=0, trama=0, rim=0, alfa=0.8,
                    linea=False, rampa="purpura")
        P.caliz(h, 1500, 300, 0.9, -1.4, vino=0.0, sem=40)
        C.ambiente(h, 0.5)
        h.luz_radial(960, 420, 1100, pal["vela"], k=1.2)
        C.cartela(h, "La Boda Púrpura", None, 960, 520, t, self.t_purp - 0.1, px=110, sem=3)
        C.banda(h, "ENVENENAMIENTO", 960, 820, 64, t, self.t_env, sem=9)
        N.motas(h, t, n=60, k=0.5)
        return h.acabado(t, niebla=None, bloom=0.45)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        t0 = self.t0
        tb = self.t_del - 0.35
        self.ev(t0, "lluvia_amb", 0.75, 0.0, dur=tb - t0 + 0.4)
        self.ev(self.t_visto - 0.2, "trueno_noir", 0.6, -0.2, dur=4.0)
        self.ev(t0 + 1.5, "pasos_mojados", 0.5, 0.2, dur=5.0)
        self.ev(tb, "multitud", 0.45, 0.0, dur=self.t_todos - tb)
        self.ev(self.t_todos - 0.3, "barrido_aire", 0.6, 0.0, dur=0.6)
        self.ev(self.t_caer - 0.25, "golpe_grave", 0.9, 0.1)
        self.ev(self.t_nadie, "sombra_crece", 0.6, 0.0, dur=3.0)
        self.ev(self.t_llam - 0.35, "tinta_mancha", 0.5, 0.0, dur=0.8)
        self.ev(self.t_purp, "golpe_grave", 0.8, 0.0)
        self.ev(self.t_env, "sello_golpe", 0.9, 0.0)
        self.ev(self.t1 - 0.8, "tinta_mancha", 0.6, 0.0, dur=0.9)
