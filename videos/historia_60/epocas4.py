# -*- coding: utf-8 -*-
"""Épocas 14-19: luz eléctrica (1879), vuelo (1903), Luna (1969), web (1991), smartphone (2007), hoy (2025)."""
import math

import numpy as np

import kit as K
import plano as P
from era import Era, BEAT
from escena_base import F, pop
from motor import (W, H, campana, circulo, clamp01, corazon, e_back, e_in, e_inout, e_out, elipse, h01, lerp, prog,
                   rect_red, smooth)
from plano import aclarar, mezcla, oscurecer

PI = math.pi
Z = K.poli


# ============================================================ 14. luz eléctrica
def sombrero_copa(lz, hc, d):
    cx, cy = hc
    lz.relleno(rect_red(cx - 40, cy - 30, 80, 12, 5), (30, 28, 56))
    lz.relleno(rect_red(cx - 24, cy - 84, 48, 60, 6), (36, 34, 66))
    lz.relleno(rect_red(cx - 24, cy - 42, 48, 10, 2), (196, 60, 70))


class Luz(Era):
    COL_SALIDA = (255, 224, 140)
    BX, BY = 540.0, 730.0

    def salida(self, t):
        return (self.BX, self.BY)

    def fondo(self, t):
        bg = K.degradado_img((6, 8, 40), (34, 28, 92), mid=(18, 16, 66), ym=0.6).copy()
        return F.estrellas(bg, t, 0.8, densidad=0.35)

    def cam(self, t):
        u = prog(t, self.T0 - 0.8, self.T1)
        return 1.0 + 0.04 * u, 0.0, 0.0, 0.0

    def ign(self, t):
        return e_out(prog(t, self.a(0.7), self.a(1.4)))

    def edificios(self, lz, t, capa):
        rng = np.random.default_rng(7 + capa)
        x = -30
        ig = self.ign(t)
        while x < W + 30:
            w = float(rng.uniform(110, 190))
            h = float(rng.uniform(330, 640)) if capa == 0 else float(rng.uniform(240, 440))
            yb = 1330 if capa == 0 else 1440
            col = (34, 34, 88) if capa == 0 else (22, 22, 66)
            lz.relleno(rect_red(x, yb - h, w, h + 40, 4), col)
            nx, ny = int(w // 34), int(h // 46)
            for i in range(nx):
                for j in range(ny):
                    wx, wy = x + 16 + i * 34, yb - h + 26 + j * 46
                    dist = math.hypot(wx - self.BX, wy - self.BY)
                    ton = self.a(1.0) + dist / 900.0 * 1.6 + 0.6 * float(rng.random())
                    lit = float(rng.random()) < 0.72
                    k = e_out(prog(t, ton, ton + 0.25)) if lit else 0.0
                    lz.relleno(rect_red(wx, wy, 20, 28, 3), mezcla((46, 48, 104), (255, 216, 124), k))
                    if k > 0.6 and capa == 0:
                        lz.halo(wx + 10, wy + 14, 34, (255, 200, 110), alfa=0.28 * k, capa=None)
            x += w + float(rng.uniform(6, 26))

    def dibujar(self, lz, t):
        ig = self.ign(t)
        self.edificios(lz, t, 0)
        lz.relleno(K.curva(lambda x: 1440), (16, 16, 54))
        self.edificios(lz, t, 1)
        yg = 1440
        lz.relleno(K.curva(lambda x: yg + 4, base=H + 60), (28, 26, 78))
        # farolas
        for i, (x, ta) in enumerate(((130, 2.4), (950, 2.8))):
            on = e_back(prog(t, self.a(ta), self.a(ta) + 0.3), 1.4)
            lz.relleno(K.capsula(x, yg, x, yg - 430, 16, 12), (50, 48, 96))
            lz.relleno(rect_red(x - 30, yg - 470, 60, 34, 10), (50, 48, 96))
            lz.relleno(circulo(x, yg - 486, 22, 16), mezcla((70, 70, 120), (255, 226, 150), on))
            if on > 0.02:
                lz.halo(x, yg - 486, 380, (255, 210, 120), alfa=0.5 * on, capa=None)
                lz.relleno(Z((x - 40, yg - 460), (x + 40, yg - 460), (x + 210, yg + 30), (x - 210, yg + 30)), (255, 214, 130), alfa=0.10 * on)
        # bombilla
        sw = 0.05 * math.sin(t * 2.0) * (1 - ig)
        with lz.grupo(self.BX, 0, 1.0, sw):
            lz.relleno(K.capsula(0, -40, 0, self.BY - 170, 10, 8), (60, 56, 100))
            self.bombilla(lz, ig, t)
        if ig > 0.01:
            lz.halo(self.BX, self.BY, 760 * ig, (255, 214, 120), alfa=0.5 * ig, capa=2)
            lz.halo(self.BX, self.BY, 300 * ig, (255, 236, 170), alfa=0.65 * ig, capa=2)
        # paseante con sombrero de copa
        x = lerp(-140.0, 1240.0, prog(t, self.a(-1.6), self.a(6.6)))
        K.persona(lz, x, 1530, 1.45, t, ph=t * 5.2, paso=1.0, mirar=1, piel=K.PIEL[1], pelo=(30, 26, 40), pelo_t="corto",
                  ropa=(46, 44, 86), ropa2=(36, 36, 70), sombrero=sombrero_copa, brazos=(0.4, 0.3, 0.2, 0.5) if False else K.brazos_marcha(t * 5.2, 1.0),
                  sombra=0.3)
        K.particulas(lz, t, 14, 0, W, 300, 1300, vel=(0, -10), r=(1.5, 3), col=(255, 226, 170), alfa=0.5 * (0.3 + ig), semilla=3)

    def bombilla(self, lz, ig, t):
        bx, by = 0.0, self.BY            # coordenadas locales: el grupo ya está trasladado a BX
        vidrio = mezcla((90, 92, 150), (255, 240, 200), ig * 0.9)
        lz.relleno(np.concatenate([np.stack([bx + 170 * np.cos(np.linspace(-2.7, -0.44 + PI * 0, 40)), by + 170 * np.sin(np.linspace(-2.7, -0.44 + PI * 0, 40))], 1) * 0 + 0]) if False else circulo(bx, by, 170, 60), vidrio, alfa=0.9 if ig < 0.3 else 1.0)
        lz.relleno(Z((bx - 92, by + 130), (bx + 92, by + 130), (bx + 50, by + 216), (bx - 50, by + 216)), vidrio, alfa=0.9)
        lz.relleno(elipse(bx - 62, by - 62, 30, 58, 0.6, 20), (255, 255, 255), alfa=0.28 + 0.2 * ig)          # reflejo
        # filamento
        for lado in (-1, 1):
            lz.relleno(K.capsula(bx + lado * 22, by + 200, bx + lado * 22, by + 30, 6, 5), (120, 110, 130))
        zig = [(bx - 22 + 44 * (k % 2) * 0 + (44 if k % 2 else 0) * 0 + (-22 if k % 2 == 0 else 22), by + 30 - 12 * k * 0.0) for k in range(1)]
        pts = [(bx + (-22 if k % 2 == 0 else 22) * (1 if k not in (0, 8) else 1), by + 34 - 9 * k) for k in range(9)]
        lz.trazo(np.array(pts), mezcla((110, 100, 120), (255, 246, 210), ig), 5, afinar=False, paso=4.0)
        if ig > 0.05:
            lz.halo(bx, by - 10, 150, (255, 226, 150), alfa=0.8 * ig)
        # rosca
        lz.relleno(rect_red(bx - 56, by + 210, 112, 90, 10), (200, 168, 104))
        for k in range(4):
            lz.relleno(rect_red(bx - 60, by + 224 + k * 20, 120, 8, 4), (150, 120, 76))
        lz.relleno(rect_red(bx - 26, by + 296, 52, 22, 8), (70, 60, 76))

    def sfx(self, ev):
        ev(self.a(-1.6), "whoosh", 0.3, 0.0)
        ev(self.a(0.7), "zap", 0.45, 0.0)
        ev(self.a(0.75), "brillo", 0.35, 0.0)
        for k in range(8):
            ev(self.a(1.0 + 0.2 * k), "tick", 0.16, -0.6 + 0.17 * k, tono=1.0 + 0.1 * k)
        ev(self.a(2.4), "pop", 0.3, -0.6, tono=1.1)
        ev(self.a(2.8), "pop", 0.3, 0.6, tono=1.3)
        for i in range(6):
            ev(self.a(-0.5 + i * 1.0), "pasos", 0.1, 0.3, dur=0.3)


# ============================================================ 15. vuelo
def hoja_nube(lz, x, y, s, col, alfa):
    with lz.grupo(x, y, s):
        lz.relleno(rect_red(-150, -30, 300, 60, 30), col, alfa=alfa)
        lz.relleno(circulo(-70, -40, 56, 24), col, alfa=alfa)
        lz.relleno(circulo(20, -66, 72, 28), col, alfa=alfa)
        lz.relleno(circulo(100, -34, 48, 24), col, alfa=alfa)


class Vuelo(Era):
    COL_SALIDA = (255, 255, 255)

    def fondo(self, t):
        return K.degradado_img((60, 146, 240), (214, 240, 255), mid=(140, 204, 250), ym=0.6)

    def cam(self, t):
        u = prog(t, self.T0 - 0.8, self.T1)
        return 1.0 + 0.04 * u, 0.0, 0.0, 0.0

    def salida(self, t):
        return (W / 2, 900.0)

    def avion(self, lz, x, y, s, t, rot):
        tela, tela2 = (246, 232, 196), (214, 196, 156)
        with lz.grupo(x, y, s, rot):
            # patines
            for dx in (-60, 90):
                lz.relleno(K.capsula(-160 + dx * 0, 88, 250, 92, 9, 9), (110, 78, 60)) if dx == -60 else None
            lz.relleno(K.capsula(-150, 30, -160, 92, 8, 8), (110, 78, 60))
            lz.relleno(K.capsula(150, 30, 160, 92, 8, 8), (110, 78, 60))
            # timón trasero
            lz.relleno(Z((-330, -70), (-262, -78), (-262, 24), (-330, 32)), tela2)
            lz.relleno(K.capsula(-262, -30, -180, -30, 8, 8), (110, 78, 60))
            # ala inferior / superior + puntales
            for xx in (-250, -120, 20, 160, 250):
                lz.relleno(K.capsula(xx, -76, xx, 22, 8, 8), (120, 84, 62))
            lz.relleno(Z((-300, 12), (300, 4), (312, 34), (-292, 42)), tela)
            lz.relleno(Z((-300, 32), (300, 24), (312, 34), (-292, 42)), tela2, alfa=0.8)
            lz.relleno(Z((-300, -88), (300, -96), (312, -66), (-292, -58)), tela)
            lz.relleno(Z((-300, -68), (300, -76), (312, -66), (-292, -58)), tela2, alfa=0.8)
            for xx in range(-270, 300, 60):
                lz.relleno(Z((xx, -92), (xx + 5, -92), (xx + 5, -60), (xx, -60)), tela2, alfa=0.7)
                lz.relleno(Z((xx, 16), (xx + 5, 16), (xx + 5, 40), (xx, 40)), oscurecer(tela2, 0.1), alfa=0.6)
            # cables en X
            for xx in (-250, -120, 20, 160):
                lz.trazo(np.array([(xx, -70), (xx + 130 if xx < 160 else xx + 90, 18)]), (90, 70, 90), 2.2, afinar=False)
            # elevador delantero
            lz.relleno(Z((252, -36), (360, -42), (366, -16), (252, -8)), tela)
            lz.relleno(K.capsula(180, -18, 252, -22, 7, 7), (110, 78, 60))
            # piloto boca abajo sobre el ala inferior
            lz.relleno(K.capsula(-40, 2, 60, 2, 44, 36), (96, 70, 66))
            lz.relleno(circulo(78, -6, 22, 20), K.PIEL[1])
            lz.relleno(np.concatenate([np.stack([78 + 24 * np.cos(np.linspace(PI, 2 * PI, 12)), -8 + 24 * np.sin(np.linspace(PI, 2 * PI, 12))], 1)]), (70, 50, 50))
            lz.relleno(circulo(90, -8, 4, 8), (30, 26, 62))
            lz.relleno(K.capsula(20, 8, 84, 20, 12, 10), K.PIEL[1])
            # hélices (pusher) con desenfoque
            for hx in (-190, -60):
                a = t * 60 + hx
                lz.relleno(elipse(hx, -26, 9, 94, 0, 20), (255, 255, 255), alfa=0.22)
                lz.relleno(K.capsula(hx - 3 * math.sin(a), -26 - 90 * math.cos(a), hx + 3 * math.sin(a), -26 + 90 * math.cos(a), 7, 7), (90, 70, 66), alfa=0.6)
                lz.relleno(circulo(hx, -26, 9, 10), (200, 170, 100))

    def dibujar(self, lz, t):
        sol_x = 880
        lz.halo(sol_x, 420, 380, (255, 250, 210), alfa=0.6)
        lz.relleno(circulo(sol_x, 420, 84, 40), (255, 246, 190))
        v = (300, 520, 860)
        for cap, (vel, y0, esc, alf) in enumerate(((v[0], 420, 1.1, 0.75), (v[1], 700, 1.5, 0.9), (v[2], 1130, 2.0, 0.95))):
            for i in range(4):
                x = ((h01(cap, i, 1) * (W + 700) - t * vel) % (W + 700)) - 350
                hoja_nube(lz, x, y0 + 260 * (h01(cap, i, 2) - 0.5), esc * (0.7 + 0.5 * h01(cap, i, 3)), (255, 255, 255), alf)
        # dunas y playa (Kitty Hawk)
        K.colinas(lz, 1440, (238, 214, 156), 26, 0.004, 3, dx=t * 240)
        lz.relleno(K.curva(lambda x: 1500 + 8 * math.sin((x + t * 300) * 0.01)), (218, 190, 130))
        for i in range(3):
            x = ((i * 520 + 1100 - t * 300) % 1700) - 300
            K.persona(lz, x, 1460 + 12 * i, 0.72, t, ph=0, paso=0, mirar=-1, piel=K.PIEL[1 + i % 2], pelo=(40, 30, 30), pelo_t="corto",
                      ropa=(60, 60, 86), ropa2=(60, 60, 86), brazos=(0.2, 0.2, 2.7 + 0.4 * math.sin(t * 6 + i), 0.1), boca=0.6, sombra=0.2)
        # viento
        for i in range(14):
            yy = 300 + 90 * i + 20 * (i % 3)
            xx = ((i * 211 - t * (700 + 60 * i)) % (W + 500)) - 250
            lz.relleno(K.capsula(xx, yy, xx + 150 + 30 * (i % 3), yy, 4, 4), (255, 255, 255), alfa=0.55)
        # avión
        bob = 16 * math.sin(t * 2.6)
        self.avion(lz, W / 2 + 10, 900 + bob, 1.25, t, -0.05 + 0.035 * math.sin(t * 2.0))
        kk = e_back(prog(t, self.a(2.0), self.a(2.0) + 0.4), 1.6)
        P.pastilla(lz, W / 2, 1180, "12 SEGUNDOS · 37 METROS", 40, k=kk)

    def sfx(self, ev):
        ev(self.a(-1.6), "zoom_whoosh", 0.3, 0.0)
        ev(self.a(-1.4), "ronca", 0.28, 0.0) if False else None
        ev(self.a(-1.0), "viento", 0.35, 0.0, dur=5.0)
        for i in range(10):
            ev(self.a(-1.0 + 0.55 * i), "tick", 0.12, 0.0, tono=1.8)
        ev(self.a(2.0), "ding", 0.3, 0.0, tono=1.1)


# ============================================================ 16. Luna
def casco_espacial(lz, hc, d):
    cx, cy = hc
    lz.relleno(circulo(cx, cy, 43, 34), (244, 246, 252))
    lz.relleno(elipse(cx + 12 * d, cy + 1, 27, 24, 0, 24), (214, 168, 78))
    lz.relleno(elipse(cx + 18 * d, cy - 8, 13, 9, -0.4 * d, 14), (255, 240, 200), alfa=0.7)
    lz.relleno(P.borde_luz(cx, cy, 43, PI * 1.25 if d > 0 else PI * 1.75, 0.08), (255, 255, 255), alfa=0.0)


def mochila(lz, top, d):
    lz.relleno(rect_red(-38 * d - 24 if d > 0 else 14, top - 4, 50, 92, 12), (222, 226, 240))


def modulo_lunar(lz, x, y, s):
    with lz.grupo(x, y, s):
        for lado in (-1, 1):
            lz.relleno(K.capsula(lado * 60, -130, lado * 150, -6, 12, 12), (200, 204, 220))
            lz.relleno(elipse(lado * 158, -2, 30, 9, 0, 16), (170, 176, 196))
        lz.relleno(Z((-110, -190), (110, -190), (130, -130), (60, -100), (-60, -100), (-130, -130)), (226, 178, 74))
        lz.relleno(Z((-110, -190), (-20, -190), (-30, -100), (-60, -100), (-130, -130)), aclarar((226, 178, 74), 0.3), alfa=0.7)
        lz.relleno(rect_red(-84, -326, 168, 140, 34), (232, 234, 244))
        lz.relleno(rect_red(-84, -326, 60, 140, 34), (255, 255, 255), alfa=0.5)
        lz.relleno(Z((-30, -290), (36, -290), (18, -244), (-18, -244)), (46, 44, 88))
        lz.relleno(K.capsula(40, -326, 60, -390, 5, 4), (200, 204, 220))
        lz.relleno(circulo(60, -394, 10, 12), (200, 204, 220))


def bandera(lz, x, y, s):
    with lz.grupo(x, y, s):
        lz.relleno(K.capsula(0, 0, 0, -360, 8, 8), (214, 216, 230))
        lz.relleno(K.capsula(0, -350, 220, -350, 6, 6), (214, 216, 230))
        for i in range(7):
            lz.relleno(rect_red(6, -344 + i * 16.2, 208, 16.4, 1), (204, 44, 60) if i % 2 == 0 else (250, 250, 252))
        lz.relleno(rect_red(6, -344, 92, 16.4 * 4, 1), (44, 60, 150))
        for i in range(3):
            for j in range(4):
                lz.relleno(circulo(20 + j * 22, -330 + i * 18, 2.6, 6), (255, 255, 255))


class Luna(Era):
    COL_SALIDA = (200, 210, 255)

    def fondo(self, t):
        bg = K.degradado_img((2, 3, 20), (30, 26, 76)).copy()
        return F.estrellas(bg, t, 1.0)

    def cam(self, t):
        u = prog(t, self.T0 - 0.8, self.T1)
        return 1.0 + 0.04 * u, 0.0, 0.0, 0.0

    def salida(self, t):
        return (820.0, 470.0)

    def dibujar(self, lz, t):
        P.tierra(lz, 820, 470, 190, t, rot=0.15 * t + 3.0, ang_luz=PI * 1.2, luz=1.0, nubes=1.0)
        K.colinas(lz, 1130, (108, 112, 156), 50, 0.0045, 2, dx=t * 6)
        K.colinas(lz, 1230, (136, 140, 182), 40, 0.004, 5, dx=t * 12)
        yb = 1360
        lz.relleno(K.curva(lambda x: yb + 6 * math.sin(x * 0.01)), (172, 176, 210))
        lz.relleno(K.curva(lambda x: yb + 130 + 8 * math.sin(x * 0.007)), (150, 154, 194))
        for i, (cx, cy, rx) in enumerate(((150, 1400, 100), (470, 1480, 130), (800, 1420, 110), (960, 1540, 80), (300, 1560, 90))):
            lz.relleno(elipse(cx, cy, rx, rx * 0.22, 0, 30), (128, 132, 174))
            lz.relleno(elipse(cx, cy - 3, rx * 0.86, rx * 0.16, 0, 30), (188, 192, 222))
        modulo_lunar(lz, 850, yb + 14, 1.1)
        bandera(lz, 200, yb + 70, 1.0)
        # astronauta: saltos de baja gravedad de izquierda a derecha, dejando huellas
        per = 1.15
        t0 = self.a(-1.0)
        n_paso = (t - t0) / per
        x_ini, x_fin = 300.0, 640.0
        ip = int(math.floor(n_paso))
        tot = 6
        for j in range(max(0, min(ip, tot))):
            fx = x_ini + (x_fin - x_ini) * j / tot
            lz.relleno(elipse(fx - 30, yb + 88, 30, 8, 0, 14), (120, 124, 168), alfa=0.9)
            lz.relleno(elipse(fx + 6, yb + 88, 30, 8, 0, 14), (120, 124, 168), alfa=0.9)
        fase = n_paso - math.floor(n_paso)
        xa = x_ini + (x_fin - x_ini) * clamp01((math.floor(n_paso) + smooth(fase)) / tot) if n_paso >= 0 else x_ini
        salto = 150 * math.sin(PI * fase) if n_paso >= 0 else 0
        K.persona(lz, xa, yb + 90, 1.45, t, ph=t * 2.4, paso=0.35, mirar=1, piel=K.PIEL[1], pelo=(60, 40, 40),
                  ropa=(240, 242, 250), ropa2=(224, 228, 242), falda=0.0, cinto=(200, 204, 224), sombrero=casco_espacial,
                  extra_torso=mochila, brazos=(0.5, 0.4, -0.5 + 1.2 * (1 - abs(2 * fase - 1)), 0.5), salto=salto,
                  sombra=0.35 * (1 - min(1, salto / 200)))
        K.particulas(lz, t, 16, 0, W, 900, 1500, vel=(0, 0), r=(1.5, 3), col=(210, 214, 255), alfa=0.5, semilla=5, vaiven=12)

    def sfx(self, ev):
        ev(self.a(-1.6), "zoom_whoosh", 0.3, 0.0)
        per = 1.15
        t0 = self.a(-1.0)
        for j in range(1, 6):
            ev(t0 + j * per, "golpe_suave", 0.22, 0.0, tono=0.7)
        ev(self.a(0.2), "brillo", 0.25, 0.0)
        ev(self.a(2.0), "eco", 0.25, 0.0) if False else None


# ============================================================ 17. web
def cursor(lz, x, y, s=1.0, alfa=1.0):
    with lz.grupo(x, y, s):
        pts = Z((0, 0), (0, 44), (12, 34), (22, 56), (32, 51), (22, 30), (38, 30))
        lz.relleno(pts + [3, 3], (10, 10, 40), alfa=0.4 * alfa)
        lz.relleno(pts, (255, 255, 255), alfa=alfa)
        lz.relleno(Z((4, 8), (4, 34), (12, 27), (23, 49), (26, 47), (16, 25), (28, 25)), (30, 30, 60), alfa=alfa)


class Web(Era):
    COL_SALIDA = (110, 230, 255)

    def preparar(self):
        rng = np.random.default_rng(11)
        self.nodos = []
        while len(self.nodos) < 30:
            x, y = float(rng.uniform(30, 1050)), float(rng.uniform(330, 1400))
            if abs(x - 540) < 400 and 400 < y < 1300:
                continue
            self.nodos.append((x, y))
        self.enlaces = []
        for i, (x, y) in enumerate(self.nodos):
            d = sorted(range(len(self.nodos)), key=lambda j: (self.nodos[j][0] - x) ** 2 + (self.nodos[j][1] - y) ** 2)
            for j in d[1:3]:
                if (j, i) not in self.enlaces:
                    self.enlaces.append((i, j))

    def fondo(self, t):
        return K.degradado_img((4, 8, 32), (10, 44, 100), mid=(6, 20, 62), ym=0.55)

    def cam(self, t):
        u = prog(t, self.T0 - 0.8, self.T1)
        return 1.0 + 0.03 * u, 0.0, 0.0, 0.0

    def salida(self, t):
        return (W / 2, 830.0)

    def dibujar(self, lz, t):
        cols = [(90, 224, 255), (255, 100, 200), (255, 214, 90)]
        for i in range(-1, 12):        # rejilla digital
            x = i * 100 + (t * 14) % 100
            lz.relleno(rect_red(x, 260, 2, 1300, 0), (60, 120, 220), alfa=0.16)
        for i in range(14):
            y = 300 + i * 100 + (t * 14) % 100
            lz.relleno(rect_red(0, y, W, 2, 0), (60, 120, 220), alfa=0.16)
        n = len(self.nodos)
        vis = [e_back(prog(t, self.a(-1.4 + 0.12 * i), self.a(-1.4 + 0.12 * i) + 0.4), 1.6) for i in range(n)]
        for k, (i, j) in enumerate(self.enlaces):
            g = min(vis[i], vis[j])
            if g <= 0.02:
                continue
            (x0, y0), (x1, y1) = self.nodos[i], self.nodos[j]
            c = cols[(i + j) % 3]
            lz.trazo(np.array([(x0, y0), (x0 + (x1 - x0) * g, y0 + (y1 - y0) * g)]), (*c, 110), 3.0, afinar=False)
            u = (t * (0.5 + 0.3 * (k % 3)) + h01(k, 2)) % 1.0
            lz.halo(x0 + (x1 - x0) * u, y0 + (y1 - y0) * u, 26, c, alfa=0.9 * g, capa=2)
            lz.relleno(circulo(x0 + (x1 - x0) * u, y0 + (y1 - y0) * u, 5, 10), (255, 255, 255), capa=2, alfa=g)
        for i, (x, y) in enumerate(self.nodos):
            g = vis[i]
            if g > 0.02:
                c = cols[i % 3]
                lz.halo(x, y, 60 * g, c, alfa=0.55)
                lz.relleno(circulo(x, y, 15 * g, 16), c)
                lz.relleno(circulo(x, y, 6 * g, 10), (255, 255, 255))
        # ventana del navegador
        wx, wy, ww, wh = 540.0, 830.0, 720.0, 800.0
        k = e_back(prog(t, self.a(-1.6), self.a(-0.7)), 1.3)
        with lz.grupo(wx, wy, k):
            lz.relleno(rect_red(-ww / 2 + 14, -wh / 2 + 24, ww, wh, 40), (0, 0, 20), alfa=0.4)
            lz.relleno(rect_red(-ww / 2, -wh / 2, ww, wh, 40), (244, 246, 252))
            lz.relleno(rect_red(-ww / 2, -wh / 2, ww, 92, 40), (206, 212, 234))
            lz.relleno(rect_red(-ww / 2, -wh / 2 + 50, ww, 44, 0), (206, 212, 234))
            for i, c in enumerate(((255, 96, 96), (255, 200, 80), (96, 210, 120))):
                lz.relleno(circulo(-ww / 2 + 44 + i * 40, -wh / 2 + 32, 12, 14), c)
            lz.relleno(rect_red(-ww / 2 + 30, -wh / 2 + 54, ww - 60, 46, 23), (250, 251, 255))
            lz.texto("info.cern.ch", -ww / 2 + 62, -wh / 2 + 78, 30, "geo", color=(60, 70, 110), borde=None, temblor=0.0, ancla=(0, 0.5))
            # página
            cx0, cy0 = 0, -wh / 2 + 260
            for m in range(2):
                lz.relleno(rect_red(-ww / 2 + 34, -wh / 2 + 130 + m * 54, ww - 68 - m * 260, 30, 8), (46, 70, 170) if m == 0 else (150, 160, 200))
            # globo
            gp = e_back(prog(t, self.a(-0.5), self.a(-0.5) + 0.5), 1.4)
            with lz.grupo(-ww / 2 + 160, -wh / 2 + 340, gp):
                lz.relleno(circulo(0, 0, 90, 40), (60, 140, 236))
                for a_ in (-0.5, 0.0, 0.5):
                    lz.relleno(elipse(0, 0, 90 * abs(math.cos(a_ * 1.6 + t * 1.5)) + 6, 90, 0, 30), (255, 255, 255), alfa=0.0)
                lz.trazo(np.stack([np.linspace(-90, 90, 20) * 0 + 90 * np.cos(np.linspace(-PI / 2, PI / 2, 20)) * math.cos(t * 1.4), 90 * np.sin(np.linspace(-PI / 2, PI / 2, 20))], 1), (255, 255, 255), 4, afinar=False, paso=5.0)
                lz.trazo(np.stack([90 * np.cos(np.linspace(-PI / 2, PI / 2, 20)) * math.cos(t * 1.4 + 1.6), 90 * np.sin(np.linspace(-PI / 2, PI / 2, 20))], 1), (255, 255, 255), 4, afinar=False, paso=5.0)
                lz.trazo(np.array([(-90, 0), (90, 0)]), (255, 255, 255), 4, afinar=False)
                lz.relleno(elipse(-30, -30, 26, 14, -0.5, 16), (110, 200, 110))
                lz.relleno(elipse(34, 20, 30, 18, 0.4, 16), (110, 200, 110))
            for m in range(6):
                lz.relleno(rect_red(-30, -wh / 2 + 260 + m * 44, 280 - 40 * (m % 3), 18, 6), (170, 178, 210))
            # enlace + cursor + tarjetas
            lz.texto("¡Bienvenido!", -ww / 2 + 60, -wh / 2 + 590, 46, "geo_x", color=(40, 80, 220), borde=None, temblor=0.0, ancla=(0, 0.5))
            lz.relleno(rect_red(-ww / 2 + 60, -wh / 2 + 618, 290, 5, 2), (40, 80, 220))
            for q in range(4):
                gq = e_back(prog(t, self.a(2.6 + 0.16 * q), self.a(2.6 + 0.16 * q) + 0.35), 1.6)
                if gq > 0.02:
                    qx = -ww / 2 + 110 + q * 170
                    with lz.grupo(qx, -wh / 2 + 700, gq):
                        lz.relleno(rect_red(-64, -50, 128, 100, 14), cols[q % 3])
                        lz.relleno(Z((-40, 32), (-6, -14), (14, 14), (28, 0), (48, 32)), (255, 255, 255), alfa=0.85)
                        lz.relleno(circulo(30, -22, 10, 12), (255, 255, 255), alfa=0.85)
            cxp = lerp(200, -ww / 2 + 200, e_inout(prog(t, self.a(0.8), self.a(2.4))))
            cyp = lerp(120, -wh / 2 + 606, e_inout(prog(t, self.a(0.8), self.a(2.4))))
            tc = self.a(2.5)
            if abs(t - tc) < 0.35:
                r = 10 + 90 * prog(t, tc, tc + 0.35)
                lz.trazo(np.stack([cxp + r * np.cos(np.linspace(0, 2 * PI, 40)), cyp + r * np.sin(np.linspace(0, 2 * PI, 40))], 1), (40, 80, 220, int(255 * (1 - prog(t, tc, tc + 0.35)))), 6, cerrado=True, afinar=False, capa=2)
            cursor(lz, cxp, cyp, 1.0)

    def sfx(self, ev):
        ev(self.a(-1.6), "glitch", 0.3, 0.0, dur=0.7)
        for i in range(0, 30, 3):
            ev(self.a(-1.4 + 0.12 * i), "pop", 0.18, -0.7 + 0.047 * i, tono=1.0 + 0.05 * (i % 5))
        ev(self.a(2.5), "tick", 0.4, 0.0, tono=1.6)
        for q in range(4):
            ev(self.a(2.6 + 0.16 * q), "pop", 0.3, -0.3 + 0.2 * q, tono=1.2 + 0.12 * q)


# ============================================================ 18. smartphone
def burbuja_chat(lz, x, y, s, alfa, col):
    with lz.grupo(x, y, s):
        lz.relleno(rect_red(-64, -40, 128, 80, 34), col, alfa=alfa)
        lz.relleno(Z((-30, 36), (-50, 70), (-4, 38)), col, alfa=alfa)
        for i in range(3):
            lz.relleno(circulo(-28 + 28 * i, 0, 8, 10), (255, 255, 255), alfa=alfa)


class Smartphone(Era):
    COL_SALIDA = (255, 150, 220)

    def fondo(self, t):
        return K.degradado_img((56, 22, 110), (236, 92, 156), mid=(150, 50, 140), ym=0.5)

    def cam(self, t):
        u = prog(t, self.T0 - 0.8, self.T1)
        return 1.0 + 0.04 * u, 0.0, 0.0, 0.0

    def salida(self, t):
        return (W / 2, 850.0)

    def dibujar(self, lz, t):
        cx, cy = W / 2, 830.0
        for i in range(16):        # bokeh
            x = (h01(i, 1) * W + 30 * math.sin(t * 0.6 + i)) % W
            y = 300 + (h01(i, 2) * 1200 - t * (18 + 14 * h01(i, 3))) % 1200
            lz.relleno(circulo(x, y, 30 + 60 * h01(i, 4), 24), (255, 200, 240), alfa=0.10)
        # avatares en órbita (personas conectadas)
        for i in range(9):
            a_ = t * 0.5 + i * 2 * PI / 9
            ax, ay = cx + 470 * math.cos(a_), cy + 150 + 330 * math.sin(a_) * 0.9
            if math.sin(a_) < 0:
                self.avatar(lz, ax, ay - 60 * (1 + math.sin(a_)) * 0, i, t)
        pk = e_back(prog(t, self.a(-1.6), self.a(-0.7)), 1.3)
        rot = 0.05 * math.sin(t * 1.4)
        with lz.grupo(cx, cy, pk * 1.12, rot):
            pw, ph_ = 410, 830
            lz.relleno(rect_red(-pw / 2 + 16, -ph_ / 2 + 26, pw, ph_, 66), (20, 4, 40), alfa=0.35)
            lz.relleno(rect_red(-pw / 2, -ph_ / 2, pw, ph_, 66), (30, 28, 56))
            lz.relleno(rect_red(-pw / 2 + 4, -ph_ / 2 + 4, 10, ph_ - 8, 30), (110, 110, 150), alfa=0.5)
            lz.degradado(rect_red(-pw / 2 + 16, -ph_ / 2 + 16, pw - 32, ph_ - 32, 52), (70, 60, 220), (250, 110, 190),
                         (0, -ph_ / 2), (0, ph_ / 2))
            lz.relleno(rect_red(-56, -ph_ / 2 + 26, 112, 30, 15), (20, 18, 40))
            lz.texto("9:41", 0, -ph_ / 2 + 110, 64, "geo_x", color=(255, 255, 255), borde=None, temblor=0.0)
            iconos = [(255, 96, 120), (90, 210, 130), (255, 200, 80), (90, 170, 255), (190, 110, 255), (255, 150, 80),
                      (80, 220, 220), (255, 110, 200), (120, 220, 90), (255, 90, 90), (90, 130, 255), (250, 220, 100)]
            for q, c in enumerate(iconos):
                gq = e_back(prog(t, self.a(-0.6 + 0.09 * q), self.a(-0.6 + 0.09 * q) + 0.3), 1.8)
                ix, iy = -pw / 2 + 92 + (q % 3) * 113, -ph_ / 2 + 210 + (q // 3) * 118
                if gq > 0.02:
                    with lz.grupo(ix, iy, gq):
                        lz.relleno(rect_red(-42, -42, 84, 84, 22), c)
                        lz.relleno(rect_red(-42, -42, 84, 36, 22), (255, 255, 255), alfa=0.16)
                        kind = q % 4
                        if kind == 0:
                            lz.relleno(corazon(0, -2, 30, 30), (255, 255, 255))
                        elif kind == 1:
                            lz.relleno(circulo(0, 0, 20, 20), (255, 255, 255))
                            lz.relleno(circulo(0, 0, 10, 14), c)
                        elif kind == 2:
                            lz.relleno(rect_red(-22, -16, 44, 32, 10), (255, 255, 255))
                            lz.relleno(Z((-8, 14), (-18, 28), (2, 14)), (255, 255, 255))
                        else:
                            lz.relleno(Z((0, -24), (7, -7), (25, -7), (11, 4), (16, 22), (0, 12), (-16, 22), (-11, 4), (-25, -7), (-7, -7)), (255, 255, 255))
            # barra inferior
            lz.relleno(rect_red(-pw / 2 + 40, ph_ / 2 - 130, pw - 80, 96, 40), (255, 255, 255), alfa=0.22)
        # burbujas de notificación
        for j in range(9):
            per = 1.9
            tb = self.a(0.2) + j * BEAT * 0.66
            age = (t - tb) / per
            if 0 <= age < 1:
                x = cx + (-150 + 300 * ((j * 0.37) % 1.0)) + 60 * math.sin(age * 5 + j)
                y = cy - 300 - 330 * e_out(age)
                a_ = min(1.0, age * 8) * (1 - prog(age, 0.6, 1.0))
                s_ = e_back(min(1.0, age * 5), 1.8) * 0.9
                if j % 3 == 0:
                    with lz.grupo(x, y, s_):
                        lz.relleno(corazon(0, 0, 70, 30), (255, 84, 120), alfa=a_)
                elif j % 3 == 1:
                    burbuja_chat(lz, x, y, s_, a_, (90, 210, 130))
                else:
                    with lz.grupo(x, y, s_):
                        lz.relleno(rect_red(-56, -34, 112, 68, 26), (255, 255, 255), alfa=a_)
                        lz.relleno(Z((-6, -60), (6, -40), (-16, -40)), (255, 255, 255), alfa=a_)
                        lz.relleno(circulo(-22, 0, 14, 12), (255, 96, 96), alfa=a_)
                        lz.relleno(rect_red(0, -8, 44, 16, 6), (170, 174, 210), alfa=a_)
        for i in range(9):
            a_ = t * 0.5 + i * 2 * PI / 9
            ax, ay = cx + 470 * math.cos(a_), cy + 150 + 330 * math.sin(a_) * 0.9
            if math.sin(a_) >= 0:
                self.avatar(lz, ax, ay, i, t)

    def avatar(self, lz, x, y, i, t):
        c = K.PIEL[i % 5]
        lz.halo(x, y, 90, (255, 220, 250), alfa=0.35)
        lz.relleno(circulo(x, y, 52, 26), mezcla((255, 255, 255), (200, 170, 250), 0.3))
        lz.relleno(circulo(x, y + 4, 40, 24), c)
        lz.relleno(np.concatenate([np.stack([x + 41 * np.cos(np.linspace(PI, 2 * PI, 14)), y + 4 + 41 * np.sin(np.linspace(PI, 2 * PI, 14))], 1)]), (50 + 24 * (i % 3), 34, 44))
        lz.relleno(circulo(x - 13, y + 6, 4, 8), (30, 26, 62))
        lz.relleno(circulo(x + 13, y + 6, 4, 8), (30, 26, 62))
        lz.relleno(K.capsula(x - 10, y + 24, x + 10, y + 24, 5, 5), (150, 70, 74))

    def sfx(self, ev):
        ev(self.a(-1.6), "pop", 0.4, 0.0, tono=1.3)
        for q in range(12):
            ev(self.a(-0.6 + 0.09 * q), "pop", 0.18, -0.4 + 0.07 * q, tono=1.0 + 0.06 * q)
        for j in range(9):
            ev(self.a(0.2) + j * BEAT * 0.66 + 0.1, "bling" if j % 3 == 0 else "burbuja", 0.28, -0.5 + 0.12 * j, tono=1.0 + 0.05 * j)


# ============================================================ 19. hoy
ARCOS = [(0, 6), (1, 8), (3, 11), (5, 9), (6, 13), (7, 15), (9, 17), (12, 20), (14, 18), (2, 16), (4, 10), (19, 8)]
PALETA_EPOCAS = [(255, 176, 86), (110, 200, 255), (255, 120, 120), (150, 230, 140), (255, 214, 90), (200, 140, 255)]


def gran_circulo(a, b, n):
    def v(ll):
        lam, phi = math.radians(ll[0]), math.radians(ll[1])
        return np.array([math.cos(phi) * math.sin(lam), math.sin(phi), math.cos(phi) * math.cos(lam)])
    va, vb = v(a), v(b)
    om = math.acos(max(-1.0, min(1.0, float(va @ vb))))
    u = np.linspace(0, 1, n)
    pts = (np.sin((1 - u) * om)[:, None] * va + np.sin(u * om)[:, None] * vb) / max(1e-6, math.sin(om))
    lon = np.degrees(np.arctan2(pts[:, 0], pts[:, 2]))
    lat = np.degrees(np.arcsin(np.clip(pts[:, 1], -1, 1)))
    return np.stack([lon, lat], 1), u


class Hoy(Era):
    COL_SALIDA = (255, 214, 120)
    GX, GY, GR = W / 2, 840.0, 410.0

    def fondo(self, t):
        bg = K.degradado_img((2, 3, 22), (22, 16, 66)).copy()
        return F.estrellas(bg, t, 1.0)

    def cam(self, t):
        u = prog(t, self.T0 - 0.8, self.T1)
        return 1.0 + 0.10 * (1 - e_out(u)), 0.0, 0.0, 0.0

    def salida(self, t):
        return (W / 2, H / 2)

    def anillo(self, lz, t, frente):
        cx, cy = self.GX, self.GY
        n = 18
        for i in range(n):
            g = e_back(prog(t, self.a(0.4 + 0.16 * i), self.a(0.4 + 0.16 * i) + 0.4), 1.6)
            if g <= 0.02:
                continue
            a_ = t * 0.55 + i * 2 * PI / n
            x, y = cx + 500 * math.cos(a_), cy + 40 + 170 * math.sin(a_)
            if (math.sin(a_) >= 0) != frente:
                continue
            c = PALETA_EPOCAS[i % len(PALETA_EPOCAS)]
            s_ = (0.7 + 0.3 * math.sin(a_)) * g
            lz.halo(x, y, 60 * s_, c, alfa=0.7)
            lz.relleno(circulo(x, y, 20 * s_, 16), c)
            lz.relleno(circulo(x, y, 8 * s_, 10), (255, 255, 255))

    def dibujar(self, lz, t):
        gx, gy, r = self.GX, self.GY, self.GR
        # órbita del anillo de épocas (parte de atrás)
        self.anillo(lz, t, False)
        rot = 0.35 * t + 0.3
        P.tierra(lz, gx, gy, r, t, rot=rot, ang_luz=PI * 1.1, luz=0.16, ciudades=1.0, nubes=0.4, atmosfera=1.0)
        # conexiones entre ciudades (arcos que se elevan sobre el globo)
        with lz.capa(2):
            for k, (ia, ib) in enumerate(ARCOS):
                ta = self.a(0.6 + 0.28 * k)
                g = prog(t, ta, ta + 1.2)
                if g <= 0.005:
                    continue
                A_ = np.array(P._CIUDADES, float)
                lla, _ = gran_circulo(A_[ia % len(A_)], A_[ib % len(A_)], 44)
                Q, Zq = P._proy(lla, rot, -0.35)
                u = np.linspace(0, 1, len(lla))
                alt = 1 + 0.16 * np.sin(np.pi * u)
                pts = Q * alt[:, None] * r + [gx, gy]
                n = max(2, int(len(pts) * min(1.0, g * 1.3)))
                seg = pts[:n]
                vis = Zq[:n] > 0.12
                i = 0
                while i < len(vis):
                    if vis[i]:
                        j = i
                        while j < len(vis) and vis[j]:
                            j += 1
                        if j - i > 1:
                            lz.trazo(seg[i:j], (255, 214, 120, 80), 12, afinar=False, paso=6.0)
                            lz.trazo(seg[i:j], (255, 236, 170), 4, afinar=False, paso=6.0)
                        i = j
                    else:
                        i += 1
                pulso = (t * 0.7 + k * 0.3) % 1.0
                m = int(pulso * (len(pts) - 1))
                if g > 0.9 and Zq[m] > 0.12:
                    lz.halo(pts[m][0], pts[m][1], 34, (255, 255, 255), alfa=0.9)
        # satélites
        for i in range(5):
            a_ = t * (0.9 + 0.2 * i) + i * 1.3
            ry = 0.32 + 0.1 * i
            x, y = gx + r * (1.22 + 0.05 * i) * math.cos(a_), gy + r * (1.22 + 0.05 * i) * math.sin(a_) * ry
            if math.sin(a_) >= -0.2 or abs(x - gx) > r * 1.05:
                with lz.grupo(x, y, 1.0, 0.4 * math.cos(a_)):
                    lz.relleno(rect_red(-9, -9, 18, 18, 4), (226, 228, 240))
                    lz.relleno(rect_red(-40, -5, 28, 10, 2), (90, 130, 240))
                    lz.relleno(rect_red(12, -5, 28, 10, 2), (90, 130, 240))
                lz.halo(x, y, 30, (200, 220, 255), alfa=0.35)
        self.anillo(lz, t, True)
        # textos
        k1 = e_back(prog(t, self.a(2.0), self.a(2.0) + 0.5), 1.5)
        k2 = e_back(prog(t, self.a(8.2), self.a(8.2) + 0.5), 1.5)
        s1 = 1 - prog(t, self.a(7.8), self.a(8.1))
        P.rotulo(lz, W / 2, 1372, "8 000 MILLONES", 104, k=k1 * s1 if s1 > 0 else 0.0, fuente="geo_x", alfa=s1)
        P.rotulo(lz, W / 2, 1462, "DE PERSONAS", 46, k=k1 * s1 if s1 > 0 else 0.0, fuente="geo", alfa=s1, color=(200, 214, 255))
        P.rotulo(lz, W / 2, 1360, "200 000 AÑOS", 100, k=k2, fuente="geo_x", color=(255, 226, 140))
        k3 = e_back(prog(t, self.a(11.4), self.a(11.4) + 0.5), 1.5)
        P.rotulo(lz, W / 2, 1462, "Y APENAS EMPEZAMOS", 58, k=k3, fuente="geo_x")

    def sfx(self, ev):
        ev(self.a(-1.6), "zoom_whoosh", 0.35, 0.0)
        ev(self.a(-0.6), "amanecer", 0.5, 0.0, dur=3.0)
        for k in range(len(ARCOS)):
            ev(self.a(0.6 + 0.28 * k), "zap", 0.13, -0.6 + 0.11 * k)
        for i in range(0, 18, 2):
            ev(self.a(0.4 + 0.16 * i), "pop", 0.2, -0.6 + 0.07 * i, tono=1.0 + 0.04 * i)
        ev(self.a(2.0), "impacto", 0.35, 0.0, tono=0.8)
        ev(self.a(8.2), "impacto", 0.35, 0.0, tono=0.7)
        ev(self.a(11.4), "ding", 0.4, 0.0, tono=0.9)
        ev(self.a(11.5), "brillo", 0.3, 0.0)
