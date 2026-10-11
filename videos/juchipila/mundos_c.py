# -*- coding: utf-8 -*-
"""Mundos de la escena 3 (Las Ventanas): el cerro con sus terrazas, la ciudadela, el muro de huecos, la pirámide, el juego de pelota y los 25 monolitos."""
import math

import numpy as np

import kz_iso as I
import kz_iso_obj as O
import kz_iso_deco as DC
import kz_gente_iso as G
import plano as P
from motor import circulo, elipse, rect_red, h01, prog, smooth, e_out, e_back
from mundos_b import iso_en, terraza, ROCA

PIEDRA_C = (206, 190, 170)
PIEDRA_S = (170, 148, 140)
ROJO_T = (206, 96, 84)
TIERRA = (214, 184, 132)
TERR = [(-220, -220, 640, 600, 36, 0), (-160, -160, 490, 460, 36, 36), (-100, -100, 340, 320, 36, 72), (-40, -40, 190, 180, 36, 108)]
Z0, Z1, Z2, Z3 = 36.0, 72.0, 108.0, 144.0      # alturas de las cuatro explanadas      # x, y, w, d, h, z0


def _k(u, a, b=0.18):
    """Escala de «construcción» 0..1 para un elemento que empieza a levantarse en u = a."""
    return float(smooth(np.clip((u - a) / b, 0.0, 1.0)))


class CerroVentanas:
    """El cerro de las Ventanas en su apogeo. `objetos(t, u)`: u < 1 = se está construyendo (cada edificio sube a su turno)."""
    MONO = [(90 + 50 * math.cos(a * 2 * math.pi / 16 + 0.2), 262 + 36 * math.sin(a * 2 * math.pi / 16 + 0.2)) for a in range(16)] + \
           [(90 + 26 * math.cos(a * 2 * math.pi / 9), 262 + 19 * math.sin(a * 2 * math.pi / 9)) for a in range(9)]

    def __init__(self):
        self._est = None
        self._t = 0.0
        self.n_mono = 25
        self.t_mono = None

    def suelo(self, lz, iso, t, u=1.0):
        I.isla(lz, iso, -240, -240, 440, 400, color_top=(150, 190, 112), t=t, seed=33, esp=30)
        for (x, y, w, d, h, z0) in TERR:
            terraza(lz, iso, x, y, w, d, h, estratos=((190, 150, 132), (170, 130, 124), (206, 168, 134)), tope=TIERRA if z0 > 0 else (170, 192, 118), seed=int(z0))
            I.cuadricula(lz, iso, x + 8, y + 8, x + w - 8, y + d - 8, 28, color=(255, 255, 255), alfa=0.06, z=z0 + h)
        # caminos de piedra entre terrazas (escalinatas)
        for (x0, y0, x1, y1, z) in ((60, 180, 120, 240, Z0), (60, 140, 120, 160, Z1), (60, 100, 120, 130, Z2)):
            I.suelo_rect(lz, iso, x0, y0, x1 - x0, 14, (232, 214, 176), z=z)
        DC.hierba(lz, iso, -240, -240, 660, 620, n=140, seed=12, t=t, color=(112, 170, 92), flores=0.08)

    # ---- piezas
    @staticmethod
    def choza(lz, iso, x, y, z0, k=1.0, color=(214, 176, 130), techo=(226, 190, 100)):
        if k <= 0.01:
            return
        I.cilindro(lz, iso, x, y, 11, 16 * k, color, z0=z0)
        I.cono(lz, iso, x, y, 15, 15 * k, techo, z0=z0 + 16 * k)

    @staticmethod
    def piramide(lz, iso, x, y, w, d, k=1.0):
        n = 4
        for i in range(n):
            kk = float(np.clip(k * (n + 0.6) - i, 0, 1))
            if kk <= 0.01:
                continue
            inset = 11 * i
            c = I.caja(lz, iso, x + inset, y + inset, w - 2 * inset, d - 2 * inset, 14 * kk, PIEDRA_C if i % 2 == 0 else (196, 176, 158), z0=Z0 + 14 * i)
            I.cara_rect(lz, iso, c, "y", c.w * 0.40, c.w * 0.60, 0, 14 * kk, (240, 222, 184))              # escalinata central
        if k > 0.75:
            kt = (k - 0.75) / 0.25
            c = I.caja(lz, iso, x + w / 2 - 13, y + d / 2 - 13, 26, 26, 18 * kt, (226, 196, 170), z0=Z0 + 56)
            if kt > 0.95:
                I.techo_piramide(lz, iso, c, 14, ROJO_T, vuelo=3)

    @staticmethod
    def cancha(lz, iso, x, y, L, A, k=1.0, t=0.0):
        """Juego de pelota en I: piso largo y dos plataformas laterales inclinadas."""
        if k <= 0.01:
            return
        I.suelo_rect(lz, iso, x, y + 14, L, A - 28, (232, 214, 176), z=Z0)
        for yy in (y, y + A - 14):
            I.caja(lz, iso, x, yy, L, 14, 14 * k, PIEDRA_C, z0=Z0)
        for xx in (x, x + L - 16):
            I.caja(lz, iso, xx, y, 16, A, 8 * k, (196, 176, 158), z0=Z0)
        # pelota que rebota
        bx = x + L * (0.5 + 0.38 * math.sin(t * 1.1))
        bz = Z0 + 6 + 9 * abs(math.sin(t * 3.3))
        sx, sy = iso.P(bx, y + A / 2, bz)
        lz.relleno(circulo(float(sx), float(sy), 4.2 * iso.z, 12), (60, 40, 40))

    @staticmethod
    def monolito(lz, iso, x, y, z0, k=1.0, seed=0):
        """Disco de piedra de canto (monolito circular)."""
        if k <= 0.01:
            return
        sx, sy = iso.P(x, y, z0 + 7 * k)
        r = 7.0 * iso.z * k
        ang = 0.5
        lz.relleno(elipse(float(sx) + 1.2 * iso.z, float(sy) + 1.0 * iso.z, r * 0.62, r, ang, 18), P.oscurecer((176, 156, 146), 0.15))
        lz.relleno(elipse(float(sx), float(sy), r * 0.62, r, ang, 18), (206, 188, 172))
        lz.relleno(elipse(float(sx) - 0.5 * iso.z, float(sy) - 0.5 * iso.z, r * 0.40, r * 0.72, ang, 14), (224, 208, 192), alfa=0.8)

    @staticmethod
    def ciudadela(lz, iso, k=1.0):
        """Muros de la ciudadela en la cima (z = 112) con torres en las esquinas y el templo en el centro."""
        x, y, w, d = -40, -40, 190, 180
        z0 = Z3
        for (xx, yy, ww, dd) in ((x, y, w, 8), (x, y, 8, d), (x + w - 8, y, 8, d)):
            I.caja(lz, iso, xx, yy, ww, dd, 22 * k, PIEDRA_C, z0=z0)
        for (cx_, cy_) in ((x, y), (x + w - 14, y), (x, y + d - 14), (x + w - 14, y + d - 14)):
            I.caja(lz, iso, cx_, cy_, 14, 14, 34 * k, (196, 176, 158), z0=z0)

    @staticmethod
    def muro_ventanas(lz, iso, k=1.0, t=0.0, brillo=0.0):
        """El muro de piedra con huecos sobre el risco más alto (cara +y iluminada)."""
        x, y, w = -34, 140, 176
        c = I.caja(lz, iso, x, y, w, 9, 30 * k, PIEDRA_C, z0=Z3)
        if k > 0.9:
            n = 6
            for i in range(n):
                a0 = (0.07 + 0.155 * i) * w
                a1 = a0 + w * 0.085
                I.cara_arco(lz, iso, c, "y", a0, a1, 7, 24, (70, 46, 80))
                if brillo > 0:
                    I.cara_rect(lz, iso, c, "y", a0 + 2, a1 - 2, 9, 22, (255, 214, 120), alfa=0.5 * brillo)
        return c

    def objetos(self, t, u=1.0, n_mono=25, asalto=0.0):
        self._t = t
        din = u < 0.999 or n_mono < 25
        if self._est is None and not din:
            self._est = self._armar(1.0, 25, t)
        if not din:
            m = I.Mundo()
            m.fijos = list(self._est.fijos)
        else:
            m = self._armar(u, n_mono, t, estatico=False)
        self._gente(m, t, u, asalto)
        return m

    def _armar(self, u, n_mono, t, estatico=True):
        m = I.Mundo()
        add = (lambda *a, **kw: m.add(*a, fijo=True, **kw)) if estatico else (lambda *a, **kw: m.add(*a, fijo=False, **kw))
        # ciudadela y templo
        add(-40, -40, 150, 140, 60, (lambda k: (lambda lz, iso: self.ciudadela(lz, iso, k)))(_k(u, 0.62)), clave=1)
        add(30, 20, 80, 70, 70, (lambda k: (lambda lz, iso: (I.caja(lz, iso, 36, 26, 40, 40, 26 * k, (226, 196, 170), z0=Z3), I.caja(lz, iso, 48, 38, 16, 16, 40 * k, (206, 176, 150), z0=Z3))))(_k(u, 0.7)), clave=2)
        add(-34, 140, 150, 150, 50, (lambda k: (lambda lz, iso: self.muro_ventanas(lz, iso, k, self._t)))(_k(u, 0.68)), clave=3)
        # chozas en las terrazas (cada una a su turno)
        huts = [(270 + 22 * (i % 2), -130 + 40 * i, 28 + 28, 0.10 + 0.05 * i) for i in range(6)] + [(-70 + 52 * i, 190, 28 + 28 + 28, 0.30 + 0.05 * i) for i in range(5)] + \
               [(-130 + 36 * i, 140 + (i % 2) * 14, 28 + 28, 0.18 + 0.04 * i) for i in range(3)]
        for i, (x, y, z0, a) in enumerate(huts):
            add(x - 12, y - 12, x + 12, y + 12, z0 + 30, (lambda x, y, z0, k: (lambda lz, iso: self.choza(lz, iso, x, y, z0, k, color=[(214, 176, 130), (226, 190, 150), (200, 160, 120)][i % 3])))(x, y, z0, _k(u, a)), clave=10 + i)
        # pirámide en la franja derecha de la base
        add(336, 10, 416, 110, 70, (lambda k: (lambda lz, iso: self.piramide(lz, iso, 336, 10, 80, 100, k)))(_k(u, 0.40, 0.25)), clave=40)
        # juego de pelota en la franja delantera
        add(30, 312, 310, 372, 30, (lambda k: (lambda lz, iso: self.cancha(lz, iso, 30, 306, 280, 70, k, self._t)))(_k(u, 0.52)), clave=41)
        # monolitos circulares (25)
        for i, (x, y) in enumerate(self.MONO[:25]):
            vis = 1.0 if i < n_mono else 0.0
            if vis:
                kk = 1.0 if n_mono >= 25 and u >= 0.999 else _k(u, 0.8 + 0.008 * i, 0.06) * (1.0 if i < n_mono else 0)
                add(x - 6, y - 6, x + 6, y + 6, 20, (lambda x, y, kk, i: (lambda lz, iso: self.monolito(lz, iso, x, y, Z1, kk, i)))(x, y, kk if not estatico else 1.0, i), clave=60 + i)
        # vegetación: agaves, nopales y árboles en las terrazas y la base
        for i in range(8):
            x, y = -200 + 70 * i, 340 + 10 * (i % 2)
            add(x - 6, y - 6, x + 6, y + 6, 20, (lambda x, y, i: (lambda lz, iso: O.maguey(lz, iso_en(iso, Z0), x, y, s=1.1, seed=i, t=self._t)))(x, y, i), clave=90 + i)
        for i in range(10):
            x, y = 345 + 30 * (i % 2), 120 + 28 * i
            add(x - 6, y - 6, x + 6, y + 6, 20, (lambda x, y, i: (lambda lz, iso: O.arbol(lz, iso_en(iso, Z0), x, y, h=44, seed=i, t=self._t)))(x, y, i), clave=110 + i)
        for i in range(6):
            x, y = -190 + 14 * i, -120 + 50 * i
            add(x - 6, y - 6, x + 6, y + 6, 20, (lambda x, y, i: (lambda lz, iso: O.nopal(lz, iso_en(iso, Z0), x, y, s=1.0, seed=i)))(x, y, i), clave=130 + i)
        return m

    def _gente(self, m, t, u, asalto=0.0):
        if u < 0.9:
            return
        mu = G.Multitud()
        for i in range(7):
            mu.camina([(-60 + 60 * i, 196), (30 + 60 * i, 196), (30 + 60 * i, 214)], "caxcana" if i % 2 else "caxcan", vel=6 + i % 3, seed=300 + i, h=40, fase=0.1 * i, bucle=True, z=Z2)
        for i in range(5):
            mu.ronda((290, -40 + 70 * i), 18, "caxcan_mazo" if i % 3 == 0 else "caxcana", n=1, vel=3, seed=320 + i, h=40, z=Z1)
        for i in range(4):
            mu.camina([(10 + 40 * i, 156), (150, 156)], "caxcan_lanza", vel=6, seed=340 + i, h=40, fase=0.2 * i, z=Z2)
        mu.camina([(-60, 270), (320, 270)], "caxcan", vel=9, seed=350, h=40, z=Z1)
        mu.camina([(300, 338), (50, 338)], "caxcan_jefe", vel=8, seed=351, h=44, z=Z0)
        mu.camina([(50, 346), (300, 346)], "caxcan", vel=8, seed=352, h=40, fase=0.3, z=Z0)
        mu.quieto((65, 100), "caxcan_sacerdote", dir=(0, 1), seed=353, h=44, accion="habla", z=Z3)
        mu.dibujar(m, t)
        if asalto > 0.001:
            self._asalto(m, t, asalto)

    def _asalto(self, m, t, a):
        """Conquistadores y aliados que suben por las explanadas, fuego en las chozas y humo sobre la ciudadela. a = intensidad 0..1."""
        mu = G.Multitud()
        n = int(2 + 8 * a)
        for i in range(n):
            mu.camina([(420, 350 + 6 * (i % 3)), (60, 350 + 6 * (i % 3))], "conquistador" if i % 3 else "conquistador_lanza", vel=10 + i % 3, seed=500 + i, h=42, fase=0.09 * i, bucle=True, z=Z0, accion="pelea" if i % 4 == 0 else None)
            mu.camina([(340, 262 + 5 * (i % 3)), (-120, 262 + 5 * (i % 3))], "aliado", vel=11, seed=520 + i, h=42, fase=0.11 * i, bucle=True, z=Z1, accion="pelea" if i % 3 == 0 else None)
        for i in range(max(1, int(a * 5))):
            mu.camina([(240, 170 + 4 * i), (-60, 170 + 4 * i)], "conquistador", vel=9, seed=540 + i, h=42, fase=0.13 * i, bucle=True, z=Z2, accion="pelea")
        mu.quieto((90, 200), "capitan_esp", dir=(-1, 0), seed=560, h=46, accion="habla", z=Z2)
        mu.dibujar(m, t)
        for k, (x, y, z0) in enumerate(((270, -90, Z1), (292, -50, Z1), (-70, 190, Z2), (-18, 190, Z2), (34, 190, Z2), (-130, 140, Z1), (-94, 154, Z1))):
            if a * 7 > k + 0.5:
                m.add(x - 10, y - 10, x + 10, y + 10, z0 + 40, (lambda x, y, z0, k: (lambda lz, iso: (O.fuego(lz, iso, x, y, 1.0, self._t, k, z=z0 + 14, halo=True), O.humo(lz, iso, x, y, z0 + 34, self._t, n=5, s=1.4, color=(120, 100, 120), seed=k))))(x, y, z0, k), fijo=False, clave=900 + k)
        m.add(60, 60, 80, 80, 200, lambda lz, iso: O.humo(lz, iso, 70, 70, 170, self._t, n=8, s=2.0, color=(100, 84, 110), seed=99), fijo=False, clave=990) if a > 0.5 else None
