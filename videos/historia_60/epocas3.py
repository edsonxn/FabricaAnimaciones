# -*- coding: utf-8 -*-
"""Épocas 10-13: imprenta (1440), cruzar el océano (1492), telescopio (1610), máquina de vapor (1769)."""
import math

import numpy as np

import kit as K
import plano as P
from era import Era, BEAT
from escena_base import F, pop
from motor import (W, H, campana, circulo, clamp01, e_back, e_in, e_inout, e_out, elipse, h01, lerp, prog, rect_red,
                   smooth)
from plano import aclarar, mezcla, oscurecer

PI = math.pi
Z = K.poli
LIBROS = [(150, 60, 70), (64, 96, 140), (196, 150, 80), (88, 130, 96), (120, 84, 140), (210, 190, 150), (170, 90, 60)]


# ============================================================ 10. imprenta
class Imprenta(Era):
    COL_SALIDA = (255, 226, 160)
    YUP, YDN = 1040.0, 1196.0

    def fondo(self, t):
        return K.degradado_img((42, 26, 64), (132, 76, 76), mid=(84, 48, 72), ym=0.5)

    def cam(self, t):
        u = prog(t, self.T0 - 0.8, self.T1)
        return 1.0 + 0.04 * u, 0.0, 0.0, 0.0

    def salida(self, t):
        return (W / 2, 1010.0)

    def d(self, t):
        """0 = platina arriba, 1 = prensando (contacto en u = 0.4)."""
        u = (t / BEAT) % 1.0
        if u < 0.4:
            return e_in(u / 0.4)
        return 1 - e_inout((u - 0.4) / 0.6)

    def estantes(self, lz):
        for fila in range(3):
            yb = 420 + fila * 190
            x = -20
            i = 0
            while x < W + 20:
                w = 26 + 22 * h01(fila, i, 1)
                hgt = 90 + 60 * h01(fila, i, 2)
                c = LIBROS[int(h01(fila, i, 3) * len(LIBROS)) % len(LIBROS)]
                lz.relleno(rect_red(x, yb - hgt, w - 3, hgt, 4), oscurecer(c, 0.25))
                lz.relleno(rect_red(x, yb - hgt + 12, w - 3, 8, 2), aclarar(c, 0.25), alfa=0.6)
                x += w
                i += 1
            lz.relleno(rect_red(-20, yb, W + 40, 26, 4), (92, 58, 62))

    def dibujar(self, lz, t):
        self.estantes(lz)
        lz.relleno(Z((60, -20), (380, -20), (860, 1320), (500, 1320)), (255, 226, 170), alfa=0.06, capa=2)
        lz.relleno(Z((420, -20), (600, -20), (940, 1320), (760, 1320)), (255, 226, 170), alfa=0.05, capa=2)
        lz.relleno(K.curva(lambda x: 1370 + 4 * math.sin(x * 0.02)), (86, 52, 60))
        for i in range(10):
            lz.relleno(Z((i * 120 - 10, 1380), (i * 120 + 4, 1380), (i * 150 - 30, H + 20), (i * 150 - 50, H + 20)), (70, 42, 54), alfa=0.6)
        with lz.grupo(540, 1340, 1.3):
            with lz.grupo(-540, -1340):
                d = self.d(t)
                ypl = lerp(self.YUP, self.YDN, d)
                madera, mad2 = (150, 100, 70), (112, 74, 58)
                # bastidor
                for x in (368, 668):
                    lz.relleno(rect_red(x, 740, 46, 600, 6), madera)
                    lz.relleno(rect_red(x + 30, 740, 16, 600, 6), mad2, alfa=0.7)
                lz.relleno(rect_red(340, 730, 400, 84, 10), madera)
                lz.relleno(rect_red(340, 730, 400, 22, 10), aclarar(madera, 0.25))
                lz.relleno(rect_red(320, 1300, 440, 56, 8), mad2)
                # tornillo
                lz.relleno(rect_red(520, 810, 40, ypl - 810 + 4, 4), (200, 170, 120))
                ph = (ypl - self.YUP) / 30.0
                for k in range(-1, 12):
                    yy = 810 + ((k * 28 + ph * 28) % 336)
                    if yy < ypl - 6:
                        lz.relleno(Z((520, yy), (560, yy + 10), (560, yy + 20), (520, yy + 10)), (140, 108, 72), alfa=0.9)
                lz.relleno(rect_red(500, 806, 80, 50, 8), (90, 60, 58))
                # palanca
                th = PI * d
                Lx = 300 * math.cos(th)
                lz.relleno(K.capsula(540 - Lx, 884, 540 + Lx, 884, 20, 20), (110, 74, 58))
                lz.relleno(circulo(540 - Lx, 884, 26, 18), (70, 48, 52))
                lz.relleno(circulo(540 + Lx, 884, 26, 18), (70, 48, 52))
                lz.relleno(circulo(540, 884, 24, 18), (214, 160, 90))
                # bandeja con tipos
                lz.relleno(rect_red(396, 1236, 288, 66, 8), (168, 122, 86))
                lz.relleno(rect_red(410, 1224, 260, 34, 6), (52, 42, 60))
                for i in range(22):
                    lz.relleno(rect_red(416 + i * 11.4, 1214, 8, 20 + 6 * h01(i, 4), 2), (196, 200, 214))
                # platina
                lz.relleno(rect_red(420, ypl, 240, 44, 8), (128, 90, 72))
                lz.relleno(rect_red(420, ypl, 240, 14, 8), aclarar((128, 90, 72), 0.3))
                # hojas impresas
                t0 = int((t - self.a(-1.6)) / BEAT)
                toc = lambda k: (int(self.a(-1.6) / BEAT) + k) * BEAT + 0.4 * BEAT
                nuevas = int(np.floor((t - self.a(-1.6) - 0.4 * BEAT) / BEAT)) + 1
                base_k = int(self.a(-1.6) / BEAT)
                aterrizadas = 0
                for k in range(max(0, nuevas) - 1, max(0, nuevas) - 4, -1):
                    if k < 0:
                        continue
                    tc = self.a(-1.6) + 0.4 * BEAT + k * BEAT
                    age = t - tc
                    if age < 0:
                        continue
                    u = age / 0.55
                    if u < 1:
                        x = lerp(540, 790, e_out(u))
                        y = lerp(1206, 1290 - min(150, 7 * (k + 1)), e_in(u)) - 300 * math.sin(PI * u)
                        self.hoja(lz, x, y, 1.0, -0.6 * math.sin(PI * u) + 0.4 * u * (-1 if k % 2 else 1))
                cuenta = max(0, int(np.floor((t - self.a(-1.6) - 0.4 * BEAT - 0.55) / BEAT)) + 1)
                h_pila = min(150, 7 * cuenta)
                lz.relleno(rect_red(690, 1330, 200, 26, 6), mad2)
                for j in range(int(h_pila / 7)):
                    lz.relleno(rect_red(704 + (j % 3) * 3, 1330 - 7 * (j + 1), 172, 8, 2), (250, 244, 228))
                    lz.relleno(rect_red(704 + (j % 3) * 3, 1330 - 7 * (j + 1) + 5, 172, 3, 1), (206, 196, 176))
        K.particulas(lz, t, 26, 0, W, 300, 1300, vel=(6, -8), r=(1.5, 3.2), col=(255, 232, 180), alfa=0.5, semilla=2, vaiven=24)

    def hoja(self, lz, x, y, s, rot):
        with lz.grupo(x, y, s, rot):
            lz.relleno(rect_red(-64, -84, 128, 168, 6), (252, 246, 232))
            lz.relleno(rect_red(-64, 44, 128, 40, 6), (232, 222, 204), alfa=0.6)
            lz.relleno(rect_red(-50, -70, 34, 34, 4), (196, 44, 50))
            for i in range(7):
                lz.relleno(rect_red(-8 if i < 2 else -50, -70 + i * 20, 58 if i < 2 else 100 - 14 * (i == 6), 7, 3), (60, 54, 80))

    def sfx(self, ev):
        ev(self.a(-1.6), "whoosh", 0.3, 0.0)
        k0 = int(np.ceil((self.a(-1.6) - 0.4 * BEAT) / BEAT))
        k = k0
        while True:
            tc = k * BEAT + 0.4 * BEAT
            if tc > self.T1:
                break
            if tc >= self.a(-1.6):
                ev(tc, "impacto", 0.35, 0.0, tono=0.7)
                ev(tc + 0.28, "papel", 0.3, 0.3)
            k += 1


# ============================================================ 11. océano
def ola_capa(lz, y0, amp, lam, vel, t, col, fase=0.0, base=None):
    def f(x):
        return y0 + amp * math.sin((x + vel * t) / lam * 2 * PI + fase) + 0.35 * amp * math.sin((x + vel * t * 1.3) / lam * 5 + fase * 2)
    lz.relleno(K.curva(f, paso=24.0, base=base), col)


def carabela(lz, x, y, s, t, rot=0.0):
    casco, casco2 = (142, 86, 62), (98, 58, 50)
    vela, cruz = (248, 238, 216), (200, 46, 52)
    with lz.grupo(x, y, s, rot):
        # mástiles
        for mx, top in ((-150, -330), (10, -480), (200, -380)):
            lz.relleno(K.capsula(mx, -40, mx, top, 14, 10), (110, 76, 60))
        bill = 20 * math.sin(t * 1.9)
        # velas cuadras
        for mx, ytop, yb, w in ((10, -450, -190, 112), (200, -360, -170, 68)):
            b = bill * w / 112
            poly = [(mx - w, ytop)] + [(mx - w * (1 - u) + w * u * 0 + (mx + w - (mx - w)) * u - w * 0, ytop + 0) for u in np.linspace(0, 1, 2)]
            top = [(mx - w + 2 * w * u, ytop + 4 * math.sin(u * PI)) for u in np.linspace(0, 1, 10)]
            der = [(mx + w + b * math.sin(PI * v) * 0.6, ytop + (yb - ytop) * v) for v in np.linspace(0, 1, 12)]
            bot = [(mx + w - 2 * w * u, yb + 12 * math.sin(u * PI) * 1.0 + b * 0.3) for u in np.linspace(0, 1, 10)]
            izq = [(mx - w - b * math.sin(PI * v) * 0.6, yb - (yb - ytop) * v) for v in np.linspace(0, 1, 12)]
            lz.relleno(np.array(top + der + bot + izq), vela)
            lz.relleno(np.array([(mx + 6, ytop + 10), (mx + w + b * 0.4, ytop + 10), (mx + w + b * 0.5, yb - 10), (mx + 6, yb - 10)]), oscurecer(vela, 0.16), alfa=0.6)
            cy = (ytop + yb) / 2
            lz.relleno(rect_red(mx - 12 + b * 0.3, cy - 52, 24, 104, 3), cruz)
            lz.relleno(rect_red(mx - 46 + b * 0.3, cy - 12, 92, 24, 3), cruz)
        # vela latina (mesana)
        lz.relleno(Z((-150, -300), (-150 - 120 - bill * 0.6, -110), (-150, -100)), oscurecer(vela, 0.06))
        # banderines
        for mx, top in ((-150, -330), (10, -480), (200, -380)):
            ond = lambda u: 10 * math.sin(t * 8 - u * 6) * u
            lz.relleno(np.array([(mx, top + 4 + ond(u) * 0) for u in [0]] + [(mx + 70 * u, top + 4 + ond(u)) for u in np.linspace(0.05, 1, 8)] +
                                [(mx + 70 * u, top + 30 + ond(u)) for u in np.linspace(1, 0.05, 8)] + [(mx, top + 30)]), cruz)
        # casco
        hull = [(-262, -60), (-232, 30), (-160, 76), (150, 76), (236, 34), (300, -104), (262, -86), (210, -58), (-206, -52)]
        lz.relleno(np.array(hull), casco)
        lz.relleno(Z((-232, 30), (-160, 76), (150, 76), (236, 34), (222, 10), (-218, 10)), casco2)
        lz.relleno(Z((-262, -60), (-206, -52), (210, -58), (262, -86), (268, -96), (-266, -70)), aclarar(casco, 0.25))
        lz.relleno(rect_red(-262, -150, 130, 96, 6), oscurecer(casco, 0.05))          # castillo de popa
        lz.relleno(rect_red(-250, -134, 22, 22, 3), (255, 214, 120))
        lz.relleno(rect_red(-214, -134, 22, 22, 3), (255, 214, 120))
        lz.relleno(K.capsula(290, -100, 370, -142, 12, 8), (110, 76, 60))
        lz.relleno(Z((290, -100), (370, -142), (300, -60)), (236, 226, 204), alfa=0.85)   # foque
        for i in range(6):
            lz.relleno(circulo(-190 + i * 66, 10, 7, 10), (255, 214, 120), alfa=0.0)


class Oceano(Era):
    COL_SALIDA = (255, 236, 190)

    def fondo(self, t):
        return K.degradado_img((86, 104, 214), (255, 210, 156), mid=(248, 138, 120), ym=0.5)

    def cam(self, t):
        u = prog(t, self.T0 - 0.8, self.T1)
        return 1.0 + 0.05 * u, 0.02 * math.sin(t * 0.9), 0.0, 0.0

    def salida(self, t):
        return (W / 2, 1030.0)

    def dibujar(self, lz, t):
        P.sol(lz, 700, 930, 150, t, brillo=1.0)
        K.nubes(lz, t, 380, 3, 22, (255, 210, 190), 0.8, semilla=4, esc=1.4)
        yh = 1020
        lz.relleno(K.curva(lambda x: yh, base=H + 60), (36, 108, 160))
        for k in range(10):                                   # reflejo del sol
            xx = 700 + (k - 4) * 8 + 16 * math.sin(t * 2.3 + k * 1.3)
            lz.relleno(elipse(xx, yh + 22 + k * 30, 120 - 8 * k, 7, 0, 18), (255, 214, 150), alfa=0.55)
        ola_capa(lz, yh + 4, 8, 260, -30, t, (44, 122, 176), 0.0)
        ola_capa(lz, yh + 60, 12, 340, -48, t, (34, 108, 164), 1.0)
        yb = 1290
        bob = 12 * math.sin(t * 2.0)
        carabela(lz, W / 2 - 40, yb + bob, 1.32, t, rot=0.05 * math.sin(t * 1.6 + 1))
        ola_capa(lz, yb + 8, 16, 420, -80, t, (26, 92, 152), 2.0)
        # espuma de la proa
        for i in range(8):
            age = ((t * 1.4 + i * 0.125) % 1.0)
            lz.relleno(elipse(W / 2 + 320 + 80 * age, yb + 80 - 10 * age, 22 * (1 - age) + 4, 8 * (1 - age) + 2, 0, 14), (240, 250, 255), alfa=0.8 * (1 - age))
        ola_capa(lz, yb + 70, 20, 520, -130, t, (20, 78, 138), 3.0)
        ola_capa(lz, yb + 150, 24, 640, -190, t, (16, 62, 118), 4.0)
        for i in range(30):                                   # crestas de espuma que pasan
            x = ((i * 97 - t * (160 + 30 * (i % 4))) % (W + 200)) - 100
            y = yb + 30 + 25 * (i % 6) + 6 * math.sin(t * 2 + i)
            lz.relleno(K.capsula(x, y, x + 46 + 12 * (i % 3), y, 6, 6), (220, 244, 252), alfa=0.65)
        for i in range(4):
            K.pajaro_v(lz, ((t * 120 + i * 300) % 1500) - 200, 430 + 60 * i + 20 * math.sin(t * 2 + i), 1.3, t, (255, 246, 236), i)
        K.particulas(lz, t, 20, 0, W, 1100, 1500, vel=(-40, -10), r=(1.5, 3.5), col=(255, 255, 255), alfa=0.7, semilla=13)

    def sfx(self, ev):
        ev(self.a(-1.6), "ola", 0.4, 0.0, dur=0.9)
        ev(self.a(-1.0), "viento", 0.3, 0.0, dur=5.5)
        for i in range(3):
            ev(self.a(-0.5 + 2.0 * i), "chapuzon", 0.16, 0.3, tono=0.8)
        ev(self.a(2.0), "pio", 0.3, -0.5, tono=1.4)
        ev(self.a(3.5), "pio", 0.3, 0.5, tono=1.25)
        ev(self.a(4.6), "brillo", 0.25, 0.0)


# ============================================================ 12. telescopio
class Telescopio(Era):
    COL_SALIDA = (255, 214, 130)
    LX, LY, LR = 540.0, 500.0, 250.0

    def fondo(self, t):
        bg = K.degradado_img((4, 6, 30), (40, 30, 92), mid=(20, 16, 64), ym=0.6).copy()
        return F.estrellas(bg, t, 1.0, dx=t * 4, dy=0)

    def cam(self, t):
        u = prog(t, self.T0 - 0.8, self.T1)
        return 1.0 + 0.03 * u, 0.0, 0.0, 0.0

    def salida(self, t):
        return (self.LX, self.LY)

    def dibujar(self, lz, t):
        yg = 1440
        # suelo
        lz.relleno(K.curva(lambda x: yg + 16 + 8 * math.sin(x * 0.01), base=H + 60), (28, 24, 70))
        # telescopio (trípode + tubo)
        px, py = 660.0, 1040.0
        ang = math.radians(50)
        ux, uy = math.cos(ang), -math.sin(ang)
        wob = 0.0
        for lx_, sh in ((-140, 0.1), (150, 0.3), (10, 0.2)):
            lz.relleno(K.capsula(px, py + 40, px + lx_ * 0.9, yg, 26, 18), oscurecer((120, 84, 66), sh))
        def pt(u):
            return px + ux * u, py + uy * u
        tubo = Z((pt(-130)[0] - uy * 28, pt(-130)[1] + ux * 28), (pt(-130)[0] + uy * 28, pt(-130)[1] - ux * 28),
                 (pt(430)[0] + uy * 42, pt(430)[1] - ux * 42), (pt(430)[0] - uy * 42, pt(430)[1] + ux * 42))
        lz.relleno(tubo, (196, 88, 76))
        lz.relleno(Z((pt(-130)[0] - uy * 28, pt(-130)[1] + ux * 28), (pt(-130)[0] - uy * 4, pt(-130)[1] + ux * 4),
                     (pt(430)[0] - uy * 6, pt(430)[1] + ux * 6), (pt(430)[0] - uy * 42, pt(430)[1] + ux * 42)), oscurecer((196, 88, 76), 0.25), alfa=0.55)
        for u in (-40, 150, 330, 430):
            a_ = 34 + 8 * (u + 130) / 560
            lz.relleno(Z((pt(u)[0] - uy * a_, pt(u)[1] + ux * a_), (pt(u)[0] + uy * a_, pt(u)[1] - ux * a_),
                         (pt(u + 26)[0] + uy * a_, pt(u + 26)[1] - ux * a_), (pt(u + 26)[0] - uy * a_, pt(u + 26)[1] + ux * a_)), (236, 190, 100))
        lz.relleno(K.capsula(pt(-130)[0], pt(-130)[1], pt(-170)[0], pt(-170)[1], 30, 24), (60, 46, 66))       # ocular
        lz.relleno(circulo(px, py, 26, 20), (236, 190, 100))
        lens = pt(444)
        lz.halo(lens[0], lens[1], 90, (200, 230, 255), alfa=0.45, capa=2)
        # Galileo
        pu = e_back(prog(t, self.a(-1.6), self.a(-0.8)), 1.3)
        K.persona(lz, 430, yg, 1.8, t, ph=0, paso=0, mirar=1, piel=K.PIEL[1], pelo=(196, 190, 190), pelo_t="corto", barba=True,
                  ropa=(150, 58, 84), ropa2=(150, 58, 84), falda=1.0, inc=0.26, brazos=(0.2, 0.6, 0.9, 1.2),
                  sombrero=self.gorro, boca=0.0)
        # visor circular con Júpiter y sus 4 lunas
        k = e_back(prog(t, self.a(-0.9), self.a(-0.2)), 1.4)
        if k > 0.01:
            lz.relleno(K.capsula(lens[0], lens[1], self.LX, self.LY + 180, 5, 3), (255, 255, 255), alfa=0.35 * k)
            with lz.grupo(self.LX, self.LY, k):
                lz.relleno(circulo(0, 0, self.LR + 22, 90), (226, 178, 96))
                lz.relleno(circulo(0, 0, self.LR + 6, 90), (150, 110, 70))
                lz.relleno(circulo(0, 0, self.LR, 90), (6, 8, 34))
                with lz.recorte(circulo(0, 0, self.LR, 90)):
                    lz.relleno(circulo(0, 0, self.LR, 60), (10, 12, 44))
                    for i in range(40):
                        lz.puntos(np.array([[(h01(i, 1) - 0.5) * 2 * self.LR, (h01(i, 2) - 0.5) * 2 * self.LR]]), 1.0 + 1.6 * h01(i, 3), (255, 255, 255), capa=None)
                    P.planeta(lz, 0, 0, 84, "jupiter", t)
                    for j, (rad, per, ph0, col) in enumerate(((128, 1.8, 0.4, (236, 226, 150)), (162, 3.5, 2.1, (250, 250, 250)),
                                                              (198, 7.2, 4.0, (200, 190, 176)), (232, 16.7, 1.0, (160, 150, 150)))):
                        ang_m = ph0 + t * 2 * PI / (per * 0.9 * BEAT * 2)
                        mx = rad * math.cos(ang_m)
                        my = 0.10 * rad * math.sin(ang_m)
                        if math.sin(ang_m) < 0 and abs(mx) < 90:
                            continue
                        lz.halo(mx, my, 24, col, alfa=0.7)
                        lz.relleno(circulo(mx, my, 8.5, 12), col)
            kk = e_back(prog(t, self.a(2.2), self.a(2.2) + 0.4), 1.6)
            P.pastilla(lz, self.LX, self.LY + self.LR + 76, "¡4 LUNAS!", 40, k=kk)
        K.particulas(lz, t, 12, 0, W, 200, 1400, vel=(0, 0), r=(1.5, 3), col=(210, 220, 255), alfa=0.5, semilla=2, vaiven=26)

    @staticmethod
    def gorro(lz, hc, d):
        cx, cy = hc
        lz.relleno(elipse(cx - 2 * d, cy - 26, 32, 12, -0.08 * d, 24), (60, 30, 50))
        lz.relleno(np.concatenate([np.stack([cx - 2 * d + 26 * np.cos(np.linspace(PI, 2 * PI, 14)), cy - 26 + 20 * np.sin(np.linspace(PI, 2 * PI, 14))], 1)]), (76, 40, 62))

    def sfx(self, ev):
        ev(self.a(-1.6), "zoom_whoosh", 0.3, 0.0)
        ev(self.a(-0.8), "revelar", 0.45, 0.0)
        for j in range(4):
            ev(self.a(0.6 + 0.35 * j), "pop", 0.3, -0.5 + 0.33 * j, tono=1.0 + 0.16 * j)
        ev(self.a(2.2), "ding", 0.35, 0.0, tono=1.0)


# ============================================================ 13. vapor
def engranaje(lz, x, y, R, n, ang, col, hueco=None):
    pts = []
    for i in range(n):
        a0 = ang + 2 * PI * i / n
        for da, rr in ((0.0, R * 0.86), (0.13, R * 1.0), (0.37, R * 1.0), (0.5, R * 0.86)):
            aa = a0 + da * 2 * PI / n
            pts.append((x + rr * math.cos(aa), y + rr * math.sin(aa)))
    lz.relleno(np.array(pts), col)
    lz.relleno(circulo(x, y, R * 0.7, 40), oscurecer(col, 0.22))
    for i in range(6):
        aa = ang + i * PI / 3
        lz.relleno(K.capsula(x, y, x + R * 0.68 * math.cos(aa), y + R * 0.68 * math.sin(aa), R * 0.16, R * 0.16), col)
    lz.relleno(circulo(x, y, R * 0.24, 24), aclarar(col, 0.25))
    lz.relleno(circulo(x, y, R * 0.09, 14), (40, 34, 66))


class Vapor(Era):
    COL_SALIDA = (255, 190, 120)
    CX, CY, RV = 640.0, 1010.0, 250.0

    def fondo(self, t):
        return K.degradado_img((54, 46, 86), (246, 154, 96), mid=(160, 88, 112), ym=0.55)

    def cam(self, t):
        u = prog(t, self.T0 - 0.8, self.T1)
        return 1.0 + 0.03 * u, 0.0, 0.0, 0.0

    def salida(self, t):
        return (self.CX, self.CY)

    def dibujar(self, lz, t):
        # chimeneas humeantes al fondo
        for i, (x, h, w) in enumerate(((90, 520, 70), (250, 380, 56), (420, 640, 84), (600, 440, 60), (780, 560, 76), (960, 420, 62), (1080, 500, 70))):
            yb = 1250
            lz.relleno(Z((x - w / 2, yb), (x - w / 2 + 8, yb - h), (x + w / 2 - 8, yb - h), (x + w / 2, yb)), (74, 52, 84))
            lz.relleno(rect_red(x - w / 2 - 4, yb - h - 14, w + 8, 20, 4), (56, 40, 72))
            lz.relleno(Z((x + w * 0.1, yb), (x + w * 0.1 + 4, yb - h), (x + w / 2 - 8, yb - h), (x + w / 2, yb)), (40, 30, 62), alfa=0.6)
            for j in range(6):
                age = (t * 0.32 + j / 6.0 + i * 0.17) % 1.0
                lz.relleno(circulo(x + 30 * age + 20 * math.sin(age * 5 + i), yb - h - 30 - 480 * age, 26 + 90 * age, 22), (206, 190, 214),
                           alfa=0.55 * (1 - age) * min(1.0, age * 8))
        lz.relleno(K.curva(lambda x: 1250), (56, 40, 72))
        # máquina: base
        lz.relleno(rect_red(-20, 1330, W + 40, 60, 6), (70, 82, 116))
        lz.relleno(rect_red(-20, 1330, W + 40, 14, 6), aclarar((70, 82, 116), 0.25))
        for i in range(12):
            lz.relleno(circulo(30 + i * 96, 1372, 7, 10), (40, 48, 76))
        cx, cy, R = self.CX, self.CY, self.RV
        th = PI * t / BEAT
        metal, metal2, cobre, laton = (110, 128, 172), (80, 94, 136), (214, 120, 76), (238, 190, 100)
        # cilindro y biela
        rc, L = 130.0, 400.0
        pin = (cx + rc * math.cos(th), cy + rc * math.sin(th))
        xc = pin[0] - math.sqrt(L * L - (pin[1] - cy) ** 2)
        lz.relleno(rect_red(-60, cy - 74, 340, 148, 14), cobre)
        lz.relleno(rect_red(-60, cy - 74, 340, 30, 14), aclarar(cobre, 0.3))
        lz.relleno(rect_red(-60, cy + 30, 340, 44, 14), oscurecer(cobre, 0.25), alfa=0.7)
        for i in range(5):
            lz.relleno(rect_red(250, cy - 88, 26, 176, 5), laton) if i == 0 else None
        lz.relleno(K.capsula(xc - 100, cy, xc, cy, 22, 22), (196, 200, 220))
        lz.relleno(rect_red(xc - 122, cy - 56, 34, 112, 6), (170, 176, 200))
        lz.relleno(rect_red(xc - 18, cy - 26, 48, 52, 8), laton)
        lz.relleno(K.capsula(xc, cy, pin[0], pin[1], 26, 26), (156, 164, 196))
        lz.relleno(K.capsula(xc, cy, pin[0], pin[1], 10, 10), aclarar((156, 164, 196), 0.4))
        # volante
        lz.trazo(np.stack([cx + R * np.cos(np.linspace(0, 2 * PI, 90)), cy + R * np.sin(np.linspace(0, 2 * PI, 90))], 1), metal, 54, cerrado=True, afinar=False, paso=8.0)
        lz.trazo(np.stack([cx + (R + 22) * np.cos(np.linspace(0, 2 * PI, 90)), cy + (R + 22) * np.sin(np.linspace(0, 2 * PI, 90))], 1), aclarar(metal, 0.3), 6, cerrado=True, afinar=False, paso=8.0)
        for i in range(8):
            aa = th + i * PI / 4
            lz.relleno(K.capsula(cx, cy, cx + R * math.cos(aa), cy + R * math.sin(aa), 26, 22), metal2)
        lz.relleno(circulo(cx, cy, 70, 36), cobre)
        lz.relleno(circulo(cx, cy, 44, 30), laton)
        lz.relleno(circulo(pin[0], pin[1], 26, 20), laton)
        # engranajes
        engranaje(lz, 210, 1240, 118, 14, -th * 0.6, (118, 136, 182))
        engranaje(lz, 210 + 118 + 86 - 6, 1240 + 34, 86, 10, th * 0.6 * 14 / 10 + PI / 10, laton)
        # vapor de la válvula
        for j in range(7):
            age = ((t / BEAT * 0.5) + j / 7.0) % 1.0
            lz.relleno(circulo(210 + 40 * age * math.sin(j), cy - 100 - 320 * age, 22 + 70 * age, 22), (255, 255, 255), alfa=0.75 * (1 - age))
        # manómetro
        gx, gy = 880.0, 640.0
        lz.relleno(circulo(gx, gy, 96, 40), laton)
        lz.relleno(circulo(gx, gy, 82, 40), (250, 246, 236))
        for i in range(9):
            a_ = PI * 0.8 + i * PI * 1.4 / 8
            lz.relleno(K.capsula(gx + 62 * math.cos(a_), gy + 62 * math.sin(a_), gx + 76 * math.cos(a_), gy + 76 * math.sin(a_), 4, 4), (60, 54, 80))
        na = PI * 0.8 + (0.55 + 0.35 * math.sin(th * 0.5)) * PI * 1.4
        lz.relleno(K.capsula(gx, gy, gx + 66 * math.cos(na), gy + 66 * math.sin(na), 8, 3), (200, 46, 52))
        lz.relleno(circulo(gx, gy, 10, 12), (60, 54, 80))
        K.particulas(lz, t, 20, 0, W, 300, 1300, vel=(0, -30), r=(1.5, 3.5), col=(255, 200, 150), alfa=0.6, semilla=6)

    def sfx(self, ev):
        ev(self.a(-1.6), "zoom_whoosh", 0.3, 0.0)
        for k in range(-1, 7):
            ev(self.a(k * 1.0), "siseo", 0.22, -0.4, dur=0.4)
            ev(self.a(k * 1.0 + 0.5), "tick", 0.3, 0.3, tono=0.7)
        ev(self.a(0.0), "impacto", 0.3, 0.0, tono=0.6)
