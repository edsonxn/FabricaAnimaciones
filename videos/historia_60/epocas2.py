# -*- coding: utf-8 -*-
"""Épocas 4-9: agricultura, rueda, escritura, pirámides, Atenas, Roma."""
import math

import numpy as np

import kit as K
import plano as P
from era import Era, BEAT
from escena_base import F, pop
from motor import (W, H, blob, campana, circulo, clamp01, e_back, e_elastic, e_in, e_inout, e_out, elipse, h01, lerp, prog,
                   rect_red, smooth)
from plano import aclarar, mezcla, oscurecer

PI = math.pi
Z = K.poli


def sol_plano(lz, x, y, r, col=(255, 236, 150), halo=(255, 220, 130)):
    lz.halo(x, y, r * 3.2, halo, alfa=0.35, capa=None)
    lz.halo(x, y, r * 1.7, halo, alfa=0.55, r0=0.4)
    lz.relleno(circulo(x, y, r, 60), col)


# ============================================================ 4. agricultura
def trigo(lz, x, y, h, t, sway=0.0, dorado=(240, 190, 70), tallo=(120, 170, 70)):
    """Espiga de trigo (origen en la base)."""
    if h < 6:
        return
    inc = 0.07 * math.sin(t * 1.9 + x * 0.05) * sway
    tx, ty = x + h * math.sin(inc), y - h * math.cos(inc)
    lz.relleno(K.capsula(x, y, tx, ty, 9, 6), tallo)
    if h > 120:
        for j in range(9):
            u = j / 9.0
            px, py = lerp(x, tx, 0.62 + 0.38 * u), lerp(y, ty, 0.62 + 0.38 * u)
            for lado in (-1, 1):
                lz.relleno(elipse(px + lado * 11, py - 8, 8, 17, lado * 0.5 + inc, 14), dorado if lado > 0 else oscurecer(dorado, 0.1))
        lz.relleno(elipse(tx, ty - 14, 8, 20, inc, 14), dorado)


def azada(lz):
    lz.relleno(K.capsula(0, -70, 0, 130, 9, 8), (140, 96, 66))
    lz.relleno(Z((-6, 120), (-16, 162), (44, 176), (52, 150), (10, 130)), (168, 172, 196))


def oveja(lz, x, y, s, t, ph=0.0, mirar=1):
    d = 1 if mirar >= 0 else -1
    with lz.grupo(x, y, s):
        lz.relleno(elipse(0, 3, 66, 8, 0, 20), (14, 12, 44), alfa=0.25)
        for lx, sh in ((-32, 0.3), (-14, 0.1), (24, 0.3), (42, 0.1)):
            lz.relleno(K.capsula(lx, -34, lx, -2, 12, 10), (70, 56, 70))
        b = -3 * abs(math.sin(ph))
        for cx, cy, r in ((-34, -66, 34), (0, -78, 42), (34, -68, 36), (-6, -50, 40), (22, -46, 34), (-42, -46, 28)):
            lz.relleno(circulo(cx, cy + b, r, 24), (252, 246, 232))
        lz.relleno(circulo(-6, -46 + b, 30, 20), (232, 222, 208), alfa=0.6)
        lz.relleno(elipse(62 * d, -60 + b, 26, 24, 0.2 * d, 20), (86, 68, 82))
        lz.relleno(elipse(46 * d, -76 + b, 18, 10, 0.4 * d, 14), (252, 246, 232))
        lz.relleno(circulo(70 * d, -66 + b, 3.4, 8), (250, 250, 250))


class Agricultura(Era):
    COL_SALIDA = (255, 226, 130)

    def fondo(self, t):
        return K.degradado_img((70, 156, 236), (214, 240, 250), mid=(150, 210, 244), ym=0.55)

    def cam(self, t):
        u = prog(t, self.T0 - 0.8, self.T1)
        return 1.0 + 0.04 * u, 0.0, 0.0, 0.0

    def salida(self, t):
        return (W / 2, 1100.0)

    def dibujar(self, lz, t):
        sol_plano(lz, 800, 470, 96)
        K.nubes(lz, t, 380, 4, 26, (255, 255, 255), 0.95, semilla=3, esc=1.3, dy=120)
        K.colinas(lz, 950, (132, 204, 130), 60, 0.0035, 2, dx=t * 6)
        K.colinas(lz, 1060, (98, 180, 112), 50, 0.0032, 6, dx=t * 12)
        K.colinas(lz, 1170, (78, 156, 100), 34, 0.005, 9, dx=t * 20)
        # campo arado
        lz.relleno(K.curva(lambda x: 1290 + 6 * math.sin(x * 0.01)), (158, 112, 78))
        for i in range(6):
            yy = 1310 + i * 42
            lz.relleno(Z((-20, yy), (W + 20, yy - 4), (W + 20, yy + 14 - 4), (-20, yy + 14)), (132, 92, 66), alfa=0.85)
        # trigo que crece
        for i in range(12):
            x = 50 + i * 88 + 14 * h01(i, 3)
            yb = 1345 + (i % 3) * 46
            g = e_back(prog(t, self.a(-1.6 + 0.24 * i), self.a(-1.6 + 0.24 * i) + 0.8), 1.5)
            trigo(lz, x, yb, 380 * g * (0.8 + 0.25 * h01(i, 4)), t, sway=min(1.0, g))
        # agricultor con azada (golpe cada 2 pulsos)
        ciclo = ((t - self.a(0)) / (2 * BEAT)) % 1.0
        golpe = 0.5 - 0.5 * math.cos(2 * PI * ciclo)        # 0 = arriba, 1 = abajo (impacta en el pulso)
        sw = e_in(clamp01(ciclo / 0.5)) if ciclo < 0.5 else 1 - e_inout(clamp01((ciclo - 0.5) / 0.5))
        a1 = lerp(2.7, 0.75, sw)
        golpe = sw
        K.persona(lz, 250, 1470, 1.85, t, ph=0, paso=0, mirar=1, piel=K.PIEL[2], pelo=(40, 28, 30), pelo_t="corto",
                  ropa=(236, 226, 196), ropa2=(150, 110, 84), falda=0.25, cinto=(150, 96, 70),
                  brazos=(a1 - 0.1, 0.5, a1, 0.5), inc=lerp(-0.05, 0.28, golpe), obj_d=azada, boca=0.0)
        oy = 1480
        oveja(lz, 800 + 20 * math.sin(t * 0.7), oy, 1.5, t, ph=t * 3, mirar=-1)
        oveja(lz, 980 + 15 * math.sin(t * 0.5), oy + 40, 1.0, t, ph=t * 3.4 + 2, mirar=-1)
        K.hierba(lz, -40, W + 40, 1560, t, (64, 138, 92), 16, 60, 4)
        K.particulas(lz, t, 14, 0, W, 900, 1500, vel=(30, -16), r=(2, 4), col=(255, 250, 200), alfa=0.6, semilla=8)

    def sfx(self, ev):
        ev(self.a(-1.5), "crece", 0.4, 0.0)
        for i in range(0, 12, 2):
            ev(self.a(-1.4 + 0.24 * i), "pop", 0.22, -0.5 + 0.09 * i, tono=1.0 + 0.05 * i)
        for k in range(1, 6, 2):
            ev(self.a(k), "golpe_suave", 0.35, -0.5)
        ev(self.a(4.5), "pio", 0.3, 0.4, tono=1.1)


# ============================================================ 5. rueda
def rueda_maciza(lz, x, y, r, ang, col=(186, 126, 80)):
    lz.relleno(circulo(x, y, r * 1.07, 56), oscurecer(col, 0.5))
    lz.relleno(circulo(x, y, r, 56), col)
    for off in (-0.34, 0.34):                                  # tablones
        c, s = math.cos(ang), math.sin(ang)
        q = math.sqrt(1 - off * off) * r
        ox, oy = -s * off * r, c * off * r
        lz.relleno(K.capsula(x + ox - c * q, y + oy - s * q, x + ox + c * q, y + oy + s * q, 6, 6), oscurecer(col, 0.35))
    lz.relleno(circulo(x, y, r * 0.24, 30), oscurecer(col, 0.3))
    lz.relleno(circulo(x, y, r * 0.09, 20), (44, 30, 46))
    lz.relleno(circulo(x + math.cos(ang) * r * 0.78, y + math.sin(ang) * r * 0.78, 7, 10), oscurecer(col, 0.35))  # marca de giro
    lz.relleno(P.borde_luz(x, y, r, PI * 1.25, 0.07), aclarar(col, 0.45), alfa=0.6)


def vasija(lz, x, y, s, col=(200, 112, 78)):
    with lz.grupo(x, y, s):
        lz.relleno(elipse(0, -44, 38, 46, 0, 28), col)
        lz.relleno(rect_red(-16, -100, 32, 30, 8), col)
        lz.relleno(rect_red(-22, -106, 44, 12, 5), oscurecer(col, 0.2))
        lz.relleno(elipse(12, -40, 22, 40, 0, 20), oscurecer(col, 0.22), alfa=0.5)
        lz.relleno(rect_red(-34, -52, 68, 8, 3), aclarar(col, 0.35))


class Rueda(Era):
    COL_SALIDA = (255, 190, 110)
    V = 520.0
    R = 120.0

    def cx(self, t):
        return 320 + (-700) * (1 - e_out(prog(t, self.a(-1.8), self.a(0.5))))

    def salida(self, t):
        return (W / 2 + (self.cx(t) - 20 - W / 2) * 1.15, 1440 - self.R * 1.15)

    def fondo(self, t):
        return K.degradado_img((56, 36, 120), (255, 204, 122), mid=(236, 110, 110), ym=0.56)

    def cam(self, t):
        u = prog(t, self.T0 - 0.8, self.T1)
        return 1.0 + 0.03 * u, 0.0, 0.0, 0.0

    def dibujar(self, lz, t):
        v = self.V
        P.sol(lz, 780, 930, 170, t, brillo=0.9)
        K.colinas(lz, 1000, (196, 96, 106), 44, 0.004, 3, dx=t * v * 0.06)
        K.colinas(lz, 1090, (164, 78, 100), 40, 0.0034, 7, dx=t * v * 0.17)
        K.colinas(lz, 1190, (128, 62, 92), 34, 0.005, 11, dx=t * v * 0.4)
        lz.relleno(K.curva(lambda x: 1420 + 5 * math.sin((x + t * v) * 0.01)), (150, 84, 88))
        for i in range(7):      # piedras y matas en el suelo cercano
            x = ((i * 190 - t * v) % (W + 300)) - 150
            lz.relleno(elipse(x, 1470 + 26 * (i % 3), 26 + 8 * (i % 2), 10, 0, 16), (112, 62, 84))
        cx = self.cx(t)
        yg = 1440
        rr = self.R
        w = v * t / rr
        with lz.grupo(W / 2, yg, 1.15):
            with lz.grupo(-W / 2, -yg):
                self.conjunto(lz, t, cx, yg, rr, w, v)

    def conjunto(self, lz, t, cx, yg, rr, w, v):
        # bueyes y carreta (en marcha)
        ph = t * 6.5
        K.buey(lz, cx + 490, yg + 6, 1.55, t, ph=ph, mirar=1, col=(176, 116, 84))
        lz.relleno(K.capsula(cx + 190, yg - 2 * rr - 4, cx + 470, yg - 190, 14, 12), (130, 88, 62))         # lanza / yugo
        # carreta
        by = yg - 2 * rr - 4
        lz.relleno(rect_red(cx - 210, by - 20, 440, 30, 8), (170, 108, 70))
        lz.relleno(rect_red(cx - 210, by - 20, 440, 10, 5), aclarar((170, 108, 70), 0.25))
        for xx in (-200, -100, 0, 100, 200):
            lz.relleno(rect_red(cx + xx - 5, by - 88, 10, 70, 4), (146, 94, 62))
        lz.relleno(rect_red(cx - 210, by - 92, 440, 12, 5), (130, 84, 60))
        vasija(lz, cx - 130, by - 20, 1.1)
        vasija(lz, cx - 20, by - 20, 1.3, (222, 150, 92))
        lz.relleno(elipse(cx + 110, by - 46, 54, 38, 0, 24), (214, 190, 140))
        lz.relleno(elipse(cx + 110, by - 46, 54, 38, 0, 24), (255, 255, 255), alfa=0.0)
        rueda_maciza(lz, cx - 20, yg - rr, rr, w)
        # polvo
        for i in range(12):
            age = (t * 9 - i) % 12 * 0.09
            tb = t - age
            px = (cx - 20 - rr * 0.5) - v * age
            py = yg - 10 - 100 * age * (1 - 0.5 * age)
            rad = 16 + 70 * age
            lz.relleno(circulo(px, py, rad, 20), (236, 190, 150), alfa=0.45 * (1 - age / 1.08))
        # conductor caminando por delante
        K.persona(lz, cx + 330, 1540, 1.45, t, ph=ph + 1.0, paso=1.0, mirar=1, piel=K.PIEL[3], pelo=(30, 22, 28), pelo_t="corto",
                  ropa=(232, 220, 190), ropa2=(150, 110, 84), falda=0.5, cinto=(150, 96, 70),
                  brazos=(0.5, 0.4, 1.3, 0.9))

    def sfx(self, ev):
        ev(self.a(-1.6), "zoom_whoosh", 0.35, -0.3)
        ev(self.a(-1.0), "arena", 0.35, 0.0, dur=5.0)
        for i in range(0, 12):
            ev(self.a(-1.0 + i * 0.5), "pasos", 0.14, 0.3, dur=0.3)
        ev(self.a(0.4), "golpe_suave", 0.4, -0.2)
        ev(self.a(3.0), "oink", 0.0, 0.0) if False else None


# ============================================================ 6. escritura
def cuna(lz, x, y, ang, s, col, luz):
    """Marca cuneiforme: cuña (cabeza ancha que se afina en punta), con brillo por debajo (huella en relieve)."""
    with lz.grupo(x, y, s * 1.2, ang):
        lz.relleno(Z((2, -5), (2, 13), (-58, 4.5)), luz, alfa=0.75)
        lz.relleno(Z((0, -9), (0, 9), (-58, 0.5)), col)
        lz.relleno(Z((0, -9), (0, -3), (-40, 0.2)), oscurecer(col, 0.35), alfa=0.7)


class Escritura(Era):
    COL_SALIDA = (255, 180, 120)
    TX, TY, TW, TH = 540.0, 800.0, 560.0, 700.0

    def preparar(self):
        rng = np.random.default_rng(5)
        self.marcas = []
        for fila in range(5):
            for col in range(4):
                n = 1 + int(rng.integers(0, 2))
                lst = []
                for _ in range(n):
                    lst.append((float(rng.uniform(-12, 12)), float(rng.uniform(-16, 16)), float(rng.choice([0.0, PI / 2, PI / 4, -PI / 4, 0.0, PI / 2]))))
                self.marcas.append((fila, col, lst))
        self.t_ini = self.a(-0.9)
        self.t_fin = self.a(4.8)

    def pos_celda(self, fila, col):
        x = self.TX - self.TW / 2 + 100 + col * (self.TW - 200) / 3
        y = self.TY - self.TH / 2 + 100 + fila * (self.TH - 200) / 4
        return x, y

    def salida(self, t):
        return (self.TX, self.TY)

    def fondo(self, t):
        return K.degradado_img((104, 44, 84), (250, 156, 96), mid=(212, 90, 92), ym=0.6)

    def cam(self, t):
        u = prog(t, self.T0 - 0.8, self.T1)
        return 1.0 + 0.04 * u, 0.015 * math.sin(t * 0.9), 0.0, 0.0

    def zigurat(self, lz, x, y, s):
        with lz.grupo(x, y, s):
            for i, (w, h) in enumerate(((760, 90), (600, 90), (450, 90), (320, 90))):
                yy = -sum(hh for _, hh in ((760, 90), (600, 90), (450, 90), (320, 90))[:i]) - h
                lz.relleno(rect_red(-w / 2, yy, w, h + 2, 4), mezcla((176, 96, 88), (120, 60, 80), i * 0.18))
                lz.relleno(rect_red(-w / 2, yy, w * 0.5, h + 2, 4), (255, 255, 255), alfa=0.0)
            lz.relleno(rect_red(-22, -400, 44, 44, 4), (236, 190, 110))
            lz.relleno(Z((-30, -90), (30, -90), (10, -360), (-10, -360)), (110, 56, 78), alfa=0.9)

    def dibujar(self, lz, t):
        P.sol(lz, 800, 700, 130, t, brillo=0.85)
        K.colinas(lz, 1080, (170, 84, 96), 40, 0.004, 2, dx=t * 8)
        self.zigurat(lz, 540, 1250, 1.45)
        lz.relleno(K.curva(lambda x: 1230 + 6 * math.sin(x * 0.008)), (124, 60, 88))
        lz.relleno(K.curva(lambda x: 1380 + 10 * math.sin(x * 0.006 + 1)), (92, 44, 76))
        # tablilla
        tx, ty, tw, th = self.TX, self.TY, self.TW, self.TH
        pu = e_back(prog(t, self.a(-1.7), self.a(-0.9)), 1.3)
        with lz.grupo(tx, ty, pu):
            lz.relleno(rect_red(-tw / 2 + 12, -th / 2 + 22, tw, th, 44), (60, 30, 56), alfa=0.35)   # sombra
            lz.relleno(rect_red(-tw / 2, -th / 2, tw, th, 44), (206, 138, 96))
            lz.relleno(rect_red(-tw / 2, -th / 2, tw, th * 0.5, 44), aclarar((206, 138, 96), 0.06))
            lz.relleno(rect_red(-tw / 2 + 24, -th / 2 + 24, tw - 48, th - 48, 30), (194, 124, 86))
            lz.relleno(P.borde_luz(0, 0, 10, 0, 0.0) if False else Z((0, 0), (0, 0), (0, 0)), (0, 0, 0), alfa=0.0)
        n = len(self.marcas)
        u = clamp01((t - self.t_ini) / (self.t_fin - self.t_ini))
        actual = u * n
        tip = None
        for i, (fila, col, lst) in enumerate(self.marcas):
            k = e_back(clamp01(actual - i), 1.6)
            x, y = self.pos_celda(fila, col)
            if k > 0.01:
                for dx, dy, ang in lst:
                    with lz.grupo(x + dx, y + dy, k):
                        cuna(lz, 0, 0, ang, 1.0, (110, 58, 56), (236, 180, 140))
            if actual - i > 0 and actual - i < 1.2:
                tip = (x, y)
        if tip is not None and u < 1.0:
            tx_, ty_ = tip[0] + 2 * math.sin(t * 40), tip[1] + 2 * math.cos(t * 33)
            ex, ey = tx_ + 140, ty_ - 240
            hx, hy = tx_ + 105, ty_ - 178
            lz.relleno(K.capsula(hx + 10, hy + 6, hx + 380, hy + 330, 78, 92), (236, 226, 196))     # antebrazo con manga
            lz.relleno(K.capsula(tx_, ty_, ex, ey, 12, 15), (150, 178, 96))                          # cálamo
            lz.relleno(Z((tx_, ty_), (tx_ + 8, ty_ - 20), (tx_ + 26, ty_ - 12)), (120, 150, 80))
            lz.relleno(circulo(hx, hy, 40, 26), K.PIEL[2])                                            # mano
            lz.relleno(K.capsula(hx - 14, hy + 8, hx - 34, hy + 44, 22, 18), K.PIEL[2])              # dedos
        # fichas de arcilla (antecedente de la escritura)
        for i, (fx, fy) in enumerate(((150, 1290), (240, 1330), (330, 1300), (420, 1340))):
            k = e_back(prog(t, self.a(-1.0 + 0.3 * i), self.a(-1.0 + 0.3 * i) + 0.4))
            with lz.grupo(fx, fy, k):
                c = (214, 150, 104)
                if i == 0:
                    lz.relleno(circulo(0, -18, 22, 20), c)
                elif i == 1:
                    lz.relleno(Z((0, -50), (-24, 0), (24, 0)), c)
                elif i == 2:
                    lz.relleno(rect_red(-20, -40, 40, 40, 6), c)
                else:
                    lz.relleno(elipse(0, -14, 30, 14, 0, 18), c)
        K.particulas(lz, t, 16, 0, W, 300, 1300, vel=(10, -20), r=(1.5, 3), col=(255, 210, 160), alfa=0.5, semilla=6)

    def sfx(self, ev):
        ev(self.a(-1.6), "iris", 0.0, 0.0) if False else None
        n = len(self.marcas)
        for i in range(0, n, 2):
            u = i / n
            ev(self.t_ini + u * (self.t_fin - self.t_ini), "tick", 0.32, -0.3 + 0.6 * (i % 5) / 5, tono=1.1 + 0.3 * ((i // 5) % 3))
        ev(self.a(4.9), "ding", 0.35, 0.0, tono=1.0)


# ============================================================ 7. pirámides
def piramide(lz, x, yb, w, h, alto_dibujado=1.0, lit=(242, 200, 120), sh=(196, 138, 84)):
    lz.relleno(Z((x - w / 2, yb), (x, yb - h), (x, yb)), lit)
    lz.relleno(Z((x, yb - h), (x + w / 2, yb), (x, yb)), sh)
    for j in range(1, 9):
        f = j / 9.0
        yy = yb - h * f
        half = w / 2 * (1 - f)
        lz.relleno(Z((x - half, yy), (x, yy - 3), (x, yy + 1), (x - half - 4, yy + 1)), oscurecer(lit, 0.16), alfa=0.6)
        lz.relleno(Z((x, yy - 3), (x + half, yy), (x + half, yy + 4), (x, yy + 1)), oscurecer(sh, 0.16), alfa=0.6)
    lz.relleno(Z((x - w * 0.045, yb - h * 0.91), (x, yb - h), (x + w * 0.045, yb - h * 0.91), (x, yb - h * 0.9)), (255, 216, 110))


class Piramides(Era):
    COL_SALIDA = (255, 200, 120)

    def fondo(self, t):
        bg = K.degradado_img((22, 18, 78), (255, 206, 128), mid=(244, 104, 96), ym=0.62).copy()
        return F.estrellas(bg, t, 0.75, densidad=0.5)

    def cam(self, t):
        u = prog(t, self.T0 - 0.8, self.T1)
        return 1.0 + 0.04 * u, 0.0, 0.0, 22 * (1 - u)

    def salida(self, t):
        return (W / 2, 880.0)

    def dibujar(self, lz, t):
        v = 220.0
        yb = 1300
        sy = lerp(1050, 900, e_out(prog(t, self.a(-1.6), self.a(2.5))))
        P.sol(lz, W / 2, sy, 250, t, brillo=1.0)
        data = [(880, 420, 500, 560, 0.0), (190, 330, 400, 360, 0.5), (540, 560, 620, 700, -0.5)]
        for x, w, h, _, dl in sorted(data, key=lambda d: -d[2]):
            pass
        for x, w, h, _, dl in ((190, 330, 380, 0, 0.55), (900, 420, 470, 0, 0.25), (540, 700, 640, 0, -0.35)):
            g = e_out(prog(t, self.a(-1.4 + dl + 0.35), self.a(-1.4 + dl + 0.35) + 1.0))
            piramide(lz, x, yb + (1 - g) * (h + 40), w, h)
        K.colinas(lz, yb, (214, 124, 84), 22, 0.006, 3, dx=t * 20)
        K.colinas(lz, yb + 92, (172, 92, 82), 26, 0.006, 8, dx=t * 60)
        lz.relleno(K.curva(lambda x: yb + 190 + 10 * math.sin((x + t * v) * 0.008)), (134, 70, 80))
        # equipo arrastrando un bloque (los pies caminan sobre el suelo que se desliza)
        ph = t * 5.0
        yy = 1520
        bx = 210
        lz.relleno(rect_red(bx - 130, yy - 116, 260, 110, 8), (232, 196, 140))
        lz.relleno(rect_red(bx - 130, yy - 116, 260, 30, 8), aclarar((232, 196, 140), 0.25))
        lz.relleno(rect_red(bx - 150, yy - 8, 300, 14, 6), (140, 92, 66))
        for i in range(4):
            px = 470 + i * 150
            K.persona(lz, px, yy + 4 * (i % 2), 1.05, t, ph=ph + i * 0.9, paso=1.0, mirar=1, piel=K.PIEL[2 + (i % 2)], pelo=(24, 20, 26),
                      pelo_t="corto" if i % 2 else "calvo", ropa=(240, 232, 214), ropa2=(240, 232, 214), falda=0.5, cinto=(200, 160, 90),
                      inc=0.34, brazos=(0.9, 0.2, 1.1, 0.2))
            lz.relleno(K.capsula(px + 30, yy - 100, px - 150, yy - 90, 5, 5), (188, 150, 100))
        lz.relleno(K.capsula(bx + 130, yy - 60, 470 + 30, yy - 100, 5, 5), (188, 150, 100))
        K.particulas(lz, t, 24, 0, W, 900, 1500, vel=(-90, -10), r=(2, 4.5), col=(255, 216, 160), alfa=0.45, semilla=3)

    def sfx(self, ev):
        ev(self.a(-1.6), "whoosh", 0.3, 0.0)
        for i, dl in enumerate((0.55, 0.25, -0.35)):
            ev(self.a(-1.4 + dl + 0.35 + 0.15), "impacto", 0.32, -0.4 + 0.4 * i, tono=0.9 - 0.15 * i)
        ev(self.a(2.5), "brillo", 0.3, 0.0)
        for i in range(8):
            ev(self.a(-0.5 + i * 0.7), "pasos", 0.1, 0.3, dur=0.3)


# ============================================================ 8. Grecia
def columna(lz, x, yb, h, g, col=(248, 240, 226), sombra=(206, 194, 184)):
    hh = h * g
    if hh < 4:
        return
    lz.relleno(Z((x - 23, yb), (x - 19, yb - hh), (x + 19, yb - hh), (x + 23, yb)), col)
    lz.relleno(Z((x + 4, yb), (x + 6, yb - hh), (x + 19, yb - hh), (x + 23, yb)), sombra, alfa=0.75)
    for k in (-10, 0, 10):
        lz.relleno(Z((x + k - 1.5, yb), (x + k * 0.86 - 1.5, yb - hh), (x + k * 0.86 + 1.5, yb - hh), (x + k + 1.5, yb)), sombra, alfa=0.55)
    lz.relleno(rect_red(x - 30, yb - 14, 60, 14, 3), col)
    lz.relleno(rect_red(x - 30, yb - hh - 2, 60, 16, 4), col)


def toga(lz, top, d):
    lz.relleno(Z((-26, top + 6), (20 * d, top + 60), (26, top + 30), (26, top + 4)), (255, 255, 255), alfa=0.9)


class Grecia(Era):
    COL_SALIDA = (255, 255, 255)

    def fondo(self, t):
        return K.degradado_img((64, 146, 238), (200, 232, 250), mid=(130, 196, 246), ym=0.6)

    def cam(self, t):
        u = prog(t, self.T0 - 0.8, self.T1)
        return 1.0 + 0.05 * u, 0.0, 0.0, 0.0

    def salida(self, t):
        return (W / 2, 900.0)

    def dibujar(self, lz, t):
        sol_plano(lz, 250, 430, 84)
        K.nubes(lz, t, 350, 3, 22, (255, 255, 255), 0.95, semilla=9, esc=1.2)
        K.colinas(lz, 1060, (150, 196, 146), 54, 0.004, 4, dx=t * 8)
        # mar
        lz.relleno(K.curva(lambda x: 1120, base=1400), (44, 132, 206))
        for i in range(6):
            yy = 1140 + i * 30
            for j in range(5):
                x = ((j * 260 + i * 70 + t * (14 + 4 * i)) % (W + 300)) - 150
                lz.relleno(K.capsula(x, yy, x + 70, yy, 5, 5), (170, 216, 250), alfa=0.6)
        # colina y templo
        lz.relleno(K.curva(lambda x: 1320 + 30 * math.sin(x * 0.006) - 0.14 * (x - 540) ** 2 / 300 * 0, base=1500), (224, 196, 150))
        yb = 1330
        for i in range(3):     # escalones
            g = e_back(prog(t, self.a(-1.5 + 0.12 * i), self.a(-1.5 + 0.12 * i) + 0.4))
            w = 790 + 60 * i
            lz.relleno(rect_red(W / 2 - w / 2, yb - 22 * (3 - i) + 22 * (3 - i) * (1 - g) * 0, w, 26 * g + 1, 4), (240, 230, 214) if i % 2 == 0 else (224, 212, 198))
        yb = 1330 - 66 + 0
        n, esp = 8, 92
        x0 = W / 2 - esp * (n - 1) / 2
        hcol = 330
        for i in range(n):
            g = e_out(prog(t, self.a(-1.2 + 0.11 * i), self.a(-1.2 + 0.11 * i) + 0.5))
            columna(lz, x0 + i * esp, yb, hcol, g)
        ge = e_back(prog(t, self.a(0.55), self.a(0.55) + 0.5), 1.6)
        yt = yb - hcol
        if ge > 0.01:
            lz.relleno(rect_red(x0 - 44, yt - 70 - 300 * (1 - ge), esp * (n - 1) + 88, 70, 5), (248, 240, 226))
            lz.relleno(rect_red(x0 - 44, yt - 30 - 300 * (1 - ge), esp * (n - 1) + 88, 30, 5), (206, 194, 184), alfa=0.7)
            for i in range(n * 2):
                lz.relleno(rect_red(x0 - 30 + i * 44, yt - 62 - 300 * (1 - ge), 22, 26, 3), (230, 218, 204))
        gp = e_back(prog(t, self.a(1.4), self.a(1.4) + 0.5), 1.4)
        if gp > 0.01:
            with lz.grupo(W / 2, yt - 70, gp):
                lz.relleno(Z((-450, 0), (450, 0), (0, -150)), (250, 242, 228))
                lz.relleno(Z((-380, -8), (380, -8), (0, -124)), (214, 202, 190))
                lz.relleno(circulo(0, -50, 32, 24), (240, 210, 130))
        # oliva
        lz.relleno(K.capsula(120, 1400, 100, 1240, 26, 18), (110, 84, 76))
        for cx, cy, r in ((90, 1180, 90), (30, 1230, 62), (170, 1226, 66)):
            lz.relleno(circulo(cx, cy, r, 28), (118, 160, 118))
        lz.relleno(circulo(110, 1160, 50, 24), (150, 190, 140), alfa=0.8)
        # asamblea ciudadana en primer plano: orador y votantes
        yy = 1500
        ph_g = math.sin(t * 5.0)
        K.persona(lz, 760, yy, 1.5, t, mirar=-1, paso=0.0, piel=K.PIEL[1], pelo=(210, 210, 216), pelo_t="calvo", barba=True,
                  ropa=(252, 250, 244), ropa2=(252, 250, 244), falda=1.0, extra_torso=toga,
                  brazos=(0.3, 0.2, 2.0 + 0.5 * ph_g, 0.5 + 0.3 * ph_g), boca=0.5 + 0.5 * math.sin(t * 9))
        for i, (px, ta) in enumerate(((230, 1.8), (420, 2.6))):
            up = e_back(prog(t, self.a(ta), self.a(ta) + 0.3), 1.8) * (1 - prog(t, self.a(ta + 1.8), self.a(ta + 2.1)))
            K.persona(lz, px, yy + 6 * i, 1.4, t, mirar=1, paso=0.0, piel=K.PIEL[2 + i], pelo=(40, 28, 30), pelo_t="corto" if i else "rizos",
                      ropa=(252, 250, 244), ropa2=(252, 250, 244), falda=1.0, extra_torso=toga,
                      brazos=(0.2, 0.2, lerp(0.2, 2.9, up), 0.1), boca=0.0)
            if up > 0.3:
                P.pastilla(lz, px, yy - 470, "✔" if False else "SÍ", 34, k=up, fondo=(120, 214, 140), color=(24, 60, 40))
        lz.relleno(K.curva(lambda x: 1560 + 6 * math.sin(x * 0.01), base=H + 60), (222, 196, 150))
        for i in range(5):
            K.pajaro_v(lz, ((t * 90 + i * 240) % 1500) - 200, 300 + 40 * math.sin(i * 2.0), 0.9, t, (255, 255, 255), i)

    def sfx(self, ev):
        ev(self.a(-1.5), "whoosh", 0.3, 0.0)
        for i in range(8):
            ev(self.a(-1.2 + 0.11 * i) + 0.2, "tick", 0.2, -0.6 + 0.17 * i, tono=0.8 + 0.06 * i)
        ev(self.a(0.55) + 0.3, "impacto", 0.3, 0.0, tono=0.8)
        ev(self.a(1.4) + 0.3, "ding", 0.35, 0.0, tono=1.0)
        ev(self.a(1.8), "pop", 0.3, -0.5, tono=1.2)
        ev(self.a(2.6), "pop", 0.3, -0.2, tono=1.35)
        ev(self.a(3.9), "hmm", 0.0, 0.0) if False else None


# ============================================================ 9. Roma
def coliseo(lz, cx, yb, gs, t):
    """Fachada curva del Coliseo (3 pisos de arcos + ático) con escorzo; gs = 4 progresos 0..1 (pisos que suben)."""
    trav = (238, 206, 156)
    sombra = (196, 156, 116)
    huec = (112, 62, 76)
    alt = [150, 136, 124, 100]
    y = yb
    tiers = []
    for i in range(4):
        y -= alt[i]
        tiers.append(y)
    Rw = 520.0
    fis = np.linspace(-PI / 2, PI / 2, 60)
    curv = 58.0
    for i in range(4):
        g = gs[i]
        if g <= 0.01:
            continue
        dy = (1 - g) * 260
        ytop, hh = tiers[i] + dy, alt[i]
        xs = cx + Rw * np.sin(fis)
        top = ytop + curv * (1 - np.cos(fis))
        poly = np.concatenate([np.stack([xs, top], 1), np.stack([xs[::-1], (top + hh + 2)[::-1]], 1)])
        lz.relleno(poly, trav)
        lz.relleno(np.concatenate([np.stack([xs, top], 1), np.stack([xs[::-1], (top + 12)[::-1]], 1)]), aclarar(trav, 0.3))
        lz.relleno(np.concatenate([np.stack([xs, top + hh - 16], 1), np.stack([xs[::-1], (top + hh + 2)[::-1]], 1)]), sombra, alfa=0.7)
        n = 15 if i < 3 else 30
        for j in range(n):
            f = -1.36 + 2.72 * (j + 0.5) / n
            ax = cx + Rw * math.sin(f)
            c = math.cos(f)
            aw = (52 if i < 3 else 22) * c
            ay = ytop + curv * (1 - c) + (24 if i < 3 else 30)
            if i < 3:
                th = np.linspace(PI, 2 * PI, 12)
                arc = np.stack([ax + aw / 2 * np.cos(th), ay + aw / 2 + aw / 2 * np.sin(th)], 1)
                lz.relleno(np.concatenate([arc, [[ax + aw / 2, ay + hh - 40], [ax - aw / 2, ay + hh - 40]]]), huec)
            else:
                lz.relleno(rect_red(ax - aw / 2, ay, aw, 34, 3), huec)
        # sombreado de borde: la fachada se curva y se oscurece hacia los lados
        for s_ in (-1, 1):
            for k in range(6):
                f0 = 0.85 + k * 0.12
                if f0 >= PI / 2:
                    break
                x0, x1 = cx + s_ * Rw * math.sin(f0), cx + s_ * Rw * math.sin(min(PI / 2, f0 + 0.12))
                y0 = ytop + curv * (1 - math.cos(f0))
                y1 = ytop + curv * (1 - math.cos(min(PI / 2, f0 + 0.12)))
                lz.relleno(Z((x0, y0), (x1, y1), (x1, y1 + hh + 2), (x0, y0 + hh + 2)), (40, 20, 56), alfa=0.08 + 0.07 * k)
    return tiers[3]


def casco(lz, hc, d):
    cx, cy = hc
    lz.relleno(np.concatenate([np.stack([cx + 32 * np.cos(np.linspace(PI, 2 * PI, 16)), cy - 2 + 32 * np.sin(np.linspace(PI, 2 * PI, 16))], 1)]), (206, 210, 226))
    lz.relleno(rect_red(cx - 32, cy - 6, 64, 9, 3), (170, 176, 196))
    lz.relleno(np.stack([cx - 18 * d + 0 * np.linspace(0, 1, 6), cy - 32 + np.linspace(0, 1, 6)], 1) if False else Z((cx - 8, cy - 32), (cx + 8, cy - 32), (cx + 6 * d, cy - 58), (cx - 26 * d, cy - 52)), (204, 44, 48))
    lz.relleno(rect_red(cx + (-4 if d > 0 else -30), cy + 2, 34, 22, 8), (170, 176, 196), alfa=0.0)


def escudo(lz):
    """Escudo (scutum) vertical delante del cuerpo (objeto fijo: no gira con el antebrazo)."""
    lz.relleno(rect_red(-8, -70, 68, 124, 16), (150, 30, 40))
    lz.relleno(rect_red(-14, -78, 68, 124, 16), (202, 44, 50))
    lz.relleno(circulo(20, -16, 14, 16), (244, 206, 96))
    lz.relleno(rect_red(-14, -78, 68, 10, 5), (244, 206, 96))
    lz.relleno(rect_red(-14, 36, 68, 10, 5), (244, 206, 96))


def estandarte(lz, t):
    lz.relleno(K.capsula(0, -70, 0, 160, 7, 6), (150, 104, 70))
    lz.relleno(circulo(0, 160, 10, 12), (244, 206, 96))
    for j in range(8):
        pass
    y0 = 148
    pts = [(0, y0 + 12 * (k / 8) * 0) for k in range(1)]
    ond = lambda u: 8 * math.sin(t * 7 - u * 5) * u
    tela = [(u * 100, y0 - 4 + ond(u)) for u in np.linspace(0, 1, 9)] + [(u * 100, y0 + 70 + ond(u)) for u in np.linspace(1, 0, 9)]
    lz.relleno(np.array(tela), (202, 44, 50))
    lz.texto("SPQR", 48, y0 + 34 + ond(0.5), 26, "geo", color=(244, 206, 96), borde=None, temblor=0.0)


class Roma(Era):
    COL_SALIDA = (255, 210, 150)

    def fondo(self, t):
        return K.degradado_img((100, 150, 236), (255, 226, 176), mid=(190, 214, 248), ym=0.55)

    def cam(self, t):
        u = prog(t, self.T0 - 0.8, self.T1)
        return 1.0 + 0.04 * u, 0.0, 0.0, 0.0

    def salida(self, t):
        return (W / 2, 1050.0)

    def dibujar(self, lz, t):
        K.nubes(lz, t, 380, 4, 24, (255, 255, 255), 0.9, semilla=11, esc=1.3)
        K.colinas(lz, 980, (176, 200, 170), 44, 0.004, 5, dx=t * 8)
        yb = 1350
        gs = [e_back(prog(t, self.a(-1.4 + 0.42 * i), self.a(-1.4 + 0.42 * i) + 0.6), 1.3) for i in range(4)]
        coliseo(lz, W / 2, yb, gs, t)
        lz.relleno(K.curva(lambda x: yb + 4, base=H + 60), (176, 138, 116))
        v = 300.0
        for i in range(9):      # juntas del camino de piedra que se desliza
            x = ((i * 150 - t * v) % (W + 300)) - 150
            lz.relleno(Z((x, yb + 60), (x + 14, yb + 60), (x + 60, H), (x + 40, H)), (150, 112, 96), alfa=0.7)
        lz.relleno(Z((-20, yb + 60), (W + 20, yb + 60), (W + 20, yb + 66), (-20, yb + 66)), (150, 112, 96), alfa=0.8)
        # legionarios marchando
        ph = t * 6.2
        yy = 1500
        rojo = (196, 44, 50)
        for i, (px, obj) in enumerate(((250, None), (560, "est"), (860, None))):
            y0 = yy + 8 * (i % 2)
            arm = (0.35, 1.25, 0.5, 1.3) if obj != "est" else (0.35, 1.25, 0.4, 1.9)
            K.persona(lz, px, y0, 1.5, t, ph=ph + 0.5 * i, paso=1.0, mirar=1, piel=K.PIEL[1 + i % 2], pelo=(60, 40, 40), pelo_t="corto",
                      ropa=rojo, ropa2=(230, 210, 176), falda=0.35, cinto=(244, 206, 96), sombrero=casco,
                      brazos=arm, obj_i=escudo, fijo_i=True, obj_d=(lambda lzz, tt=t: estandarte(lzz, tt)) if obj == "est" else lanza_pilum,
                      boca=0.0)
        K.particulas(lz, t, 16, 0, W, 800, 1500, vel=(-60, -10), r=(2, 4), col=(255, 236, 200), alfa=0.45, semilla=12)

    def sfx(self, ev):
        ev(self.a(-1.5), "whoosh", 0.3, 0.0)
        for i in range(4):
            ev(self.a(-1.4 + 0.42 * i) + 0.35, "impacto", 0.26, -0.3 + 0.2 * i, tono=0.9 - 0.1 * i)
        for i in range(0, 14):
            ev(self.a(-1.2 + i * 0.5), "pasos", 0.14, 0.0, dur=0.3)
        ev(self.a(3.0), "campana", 0.25, 0.3, tono=0.8) if False else None


def lanza_pilum(lz):
    lz.relleno(K.capsula(0, -70, 0, 100, 6, 5), (150, 104, 70))
    lz.relleno(K.capsula(0, 96, 0, 200, 4, 3), (180, 184, 204))
    lz.relleno(Z((0, 196), (-7, 210), (0, 238), (7, 210)), (200, 204, 222))
