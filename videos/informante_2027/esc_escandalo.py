# -*- coding: utf-8 -*-
"""Escena 6 «escandalo»: la redacción y el periódico que llega girando; el jefe en el atril, entre fogonazos, y la cláusula
tachada; el tablero de corcho con la carta y las trece firmas que aparecen una a una; el indicador que sube al 70 % con
Daniel ante los micrófonos."""
import math

import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import mundos27 as M27
import noir as N
import props as PR
import props3 as PR3
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from noir_pers import Frontal
from toon import elipse_, pulso


def microfono(h, x, y, alto=260, sem=0, ang=0.0):
    """Micrófono de prensa sobre su pie (x, y = cabeza)."""
    h.trazo(np.array([[x, y + 20], [x + ang * 60, y + alto]]), 7, sem, color=(40, 40, 40), jit=0.3, taper=(0, 0))
    h.pieza(np.asarray(elipse_(x, y, 22, 34, n=16)), 60, sem + 1, w=4, luz=(0.2, -1), d=6, trama=0.6, rim=0.9)
    h.pieza(C.rect(x - 26, y + 30, 52, 22), 210, sem + 2, w=3, luz=(0.2, -1), d=3, trama=0, rim=0.5)


class Escandalo(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.jefe = Frontal(sem=410)
        self.dan = Frontal(sem=77)
        self.t_mayo = w("mayo")
        self.t_prensa = w("prensa")
        self.t_papeles = w("papeles")
        self.t_escan = w("escándalo")
        self.t_conc = w("conciencia")
        self.t_jefe = w("El jefe")
        self.t_dijo = w("dijo")
        self.t_retir = w("La retiraron")
        self.t_conserv = w("conservó")
        self.t_junio = w("En junio")
        self.t_trece = w("trece")
        self.t_carta = w("carta")
        self.t_pedian = w("Pedían")
        self.t_derecho = w("derecho")
        self.t_ese = w("Ese mismo")
        self.t_calculo = w("cálculo")
        self.t_70 = w("Setenta")
        self.t_cat = w("catástrofe")
        self.fl = [self.t_jefe + 0.5, self.t_dijo + 0.2, self.t_dijo + 1.3, self.t_retir - 0.5]
        self.plano(t0, self.p_prensa)
        self.plano(self.t_jefe - 0.35, self.p_jefe, tr="relampago", dur=0.6)
        self.plano(self.t_junio - 0.35, self.p_carta, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_ese - 0.35, self.p_setenta, tr="humo", dur=0.7)

    # ------------------------------------------------------------------ la prensa
    def p_prensa(self, h, t, u):
        h.camara(1.0 + 0.012 * u, 960 + 5 * u, 540, 0.0)
        M27.redaccion().pegar(h, 1.0)
        for k in range(3):                                           # escritorios con máquinas, al fondo
            x = 200 + k * 620
            PR.mesa(h, x, 900, ancho=420, fondo=90, alto=220, tono=60, sem=30 + k * 20)
            h.pieza(C.rect(x - 80, 740, 160, 70), 30, 40 + k * 20, w=4, luz=(0.2, -1), d=6, trama=0.4, rim=0.7)
            h.pieza(C.rect(x - 60, 660 - 8 * abs(math.sin(t * 7 + k)), 120, 90), 220, 41 + k * 20, w=3, luz=(0.2, -1), d=4, trama=0)
        h.ambiente[:] = 0.46
        h.luz_persiana(np.array([[1100, -300], [2200, -340], [2200, 760], [900, 1000]]), k=1.2, n=16, abierto=0.5)
        h.luz_radial(500, 300, 1000, (1.0, 1.0, 1.0), k=0.5)
        N.motas(h, t, n=90, k=0.6)
        h.camara(1.0, W / 2, H / 2, 0.0)
        PR.periodico(h, t, self.t_prensa - 0.5, "LOS PAPELES DEL SILENCIO", "Quien se va, calla... o pierde sus acciones", cx=960, cy=560,
                     dur=0.8, s=1.12, sem=60, cabecera="MAYO DE 2024")
        C.banda(h, "EL ESCÁNDALO", 960, 1010, 70, t, self.t_escan, sem=5)
        g = pulso(t, self.t_prensa + 0.3, 0.3, 1.0)
        return h.acabado(t, niebla=dict(dens=0.14, vel=8, y0=0, y1=1080, sube=False), bloom=0.45, flash=0.2 * g)

    # ------------------------------------------------------------------ el jefe no lo sabía
    def p_jefe(self, h, t, u):
        h.camara(1.0 + 0.015 * u, 900 + 6 * u, 520, 0.0)
        K.pared(h, 36, 10, paneles=12)
        for k in range(7):                                           # cortina de fondo
            h.trazo(np.array([[100 + k * 190, -100], [120 + k * 190 + 20 * math.sin(k), 1100]]), 26, 20 + k, alfa=0.35, jit=0.6)
        s = 1.7
        fl = max(N.relampago(t, self.fl, dur=0.3), 0.0)
        p = dict(x=620, y=200 + 474 * s, s=s, luz=(0.0, -1.0), rim=0.9, pelo="oscuro", traje=40, mira=0.6 * math.sin(t * 1.3),
                 cabeza=0.05 * math.sin(t * 2.1))
        self.jefe.dibujar(h, p)
        h.pieza(np.array([[400, 760], [840, 760], [800, 1200], [440, 1200]]), 60, 40, w=7, luz=(0, -1), d=16, trama=0.5, rim=0.7)   # atril
        h.pieza(C.rect(380, 730, 480, 40), 84, 41, w=5, luz=(0, -1), d=8, trama=0.3, rim=0.8)
        for k, (mx, a) in enumerate(((500, -0.4), (580, -0.15), (660, 0.15), (740, 0.4))):
            microfono(h, mx, 620 + 10 * (k % 2), 130, 50 + k * 4, a)
        C.banda(h, "«NO CONOCÍA ESA CLÁUSULA»", 1330, 200, 54, t, self.t_dijo, claro=True, sem=5)
        # la cláusula, tachada y retirada
        if t > self.t_retir - 0.5:
            a = e_out(clamp01((t - self.t_retir + 0.5) / 0.4))
            T = K.hoja(h, 1380, 640 + 700 * (1 - a), 620, 520, ang=0.05, sem=70, renglones=3, y0=0.62, sep=40, margen=60)
            P = T([(-250, -200)])[0]
            N.texto_maquina(h, "CLÁUSULA 7", P[0], P[1], 44, t, -99, cps=1e9, tono=0.1, encuadrar=False)
            P = T([(-250, -110)])[0]
            N.texto_maquina(h, "NO HABLAR MAL", P[0], P[1], 62, t, -99, cps=1e9, tono=0.04, fuente=K.IMPACT, encuadrar=False)
            b = clamp01((t - self.t_retir - 0.1) / 0.3)
            if b > 0:
                Q = T([(-280, -70), (-280 + 560 * b, -100)])
                h.trazo(Q, 20, 90, color=(12, 12, 12), jit=0.6, taper=(0.1, 0.1))
            N.sello(h, "RETIRADA", 1380, 760, 96, t, self.t_retir + 0.5, rot=-8, tono=0.04, alfa=0.95)
        C.banda(h, "DANIEL CONSERVÓ SUS ACCIONES", 1330, 1000, 46, t, self.t_conserv, sem=6)
        h.ambiente[:] = 0.34 + 1.4 * fl
        h.luz_cono(620, -500, math.pi / 2, 0.36, 2000, (1.6, 1.6, 1.6), suave=0.5)
        N.motas(h, t, n=90, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.16, vel=8, y0=-200, y1=1000, sube=False), bloom=0.45, flash=0.35 * fl)

    # ------------------------------------------------------------------ trece firmas: el derecho a advertir
    def p_carta(self, h, t, u):
        h.camara(1.0 + 0.012 * u, 960, 540, 0.0)
        MU.corcho().pegar(h, 1.0, oscuro=0.85)
        T = K.hoja(h, 760, 560, 900, 900, ang=-0.02, sem=10, renglones=5, y0=0.20, sep=36, margen=90)
        PR3.chincheta(h, 760, 130, sem=20)
        P = T([(0, -390)])[0]
        N.texto_maquina(h, "CARTA ABIERTA · JUNIO DE 2024", P[0], P[1], 40, t, -99, cps=1e9, tono=0.15, centro=True, encuadrar=False)
        dur = max(1.5, self.t_carta - self.t_trece + 1.2)
        n = 0
        for k in range(13):                                          # las trece firmas
            tk = self.t_trece - 0.2 + k * dur / 13
            a = clamp01((t - tk) / 0.5)
            if a > 0:
                n += 1
            col, fil = k % 3, k // 3
            P = T([(-360 + col * 260, -40 + fil * 90)])[0]
            K.plano_(h, T(C.rect(-360 + col * 260, -10 + fil * 90, 200, 3)), 90, 40 + k)
            K.garabato(h, P[0], P[1], a, 0.62, 200 + k * 7, ancho=280)
        C.banda(h, f"{n} FIRMAS", 1480, 300, 110, t, self.t_trece - 0.2, sem=5)
        C.banda(h, "EMPLEADOS Y EXEMPLEADOS", 1480, 430, 40, t, self.t_trece + 0.6, claro=True, sem=6)
        C.banda(h, "EL DERECHO A ADVERTIR", 1480, 700, 62, t, self.t_derecho, claro=True, sem=7)
        PR3.hilo(h, (1250, 700), (1150, 420), u=clamp01((t - self.t_derecho) / 0.5), sem=90)
        h.ambiente[:] = 0.4
        h.luz_cono(900, -600, math.pi / 2, 0.6, 2400, (1.5, 1.5, 1.5), suave=0.5)
        N.motas(h, t, n=90, k=0.6)
        return h.acabado(t, niebla=None, bloom=0.4)

    # ------------------------------------------------------------------ 70 %
    def p_setenta(self, h, t, u):
        h.camara(1.0 + 0.015 * u, 980, 530, 0.0)
        K.pared(h, 30, 8)
        s = 1.6
        p = dict(x=430, y=250 + 474 * s, s=s, luz=(0.6, -0.8), rim=0.9, mira=0.5, cabeza=0.04 * math.sin(t * 1.4), **K.DAN)
        self.dan.dibujar(h, p)
        for k, (mx, a) in enumerate(((250, -0.5), (360, -0.2), (520, 0.2), (620, 0.5))):
            microfono(h, mx, 760 + 14 * (k % 2), 400, 50 + k * 4, a)
        v = 0.7 * e_out(clamp01((t - self.t_70 + 0.3) / 1.0)) + 0.05 * smooth(clamp01((t - self.t_calculo) / 0.8))
        K.medidor(h, 1340, 700, 400, v, t, sem=70)
        C.banda(h, "70 %", 1340, 170, 150, t, self.t_70, sem=5)
        C.banda(h, "PROBABILIDAD DE CATÁSTROFE", 1340, 1000, 54, t, self.t_cat - 0.6, claro=True, sem=6)
        C.banda(h, "SU CÁLCULO · JUNIO DE 2024", 430, 110, 38, t, self.t_calculo, claro=True, sem=7)
        g = pulso(t, self.t_70, 0.3, 1.0)
        h.ambiente[:] = 0.36
        h.luz_cono(430, -500, math.pi / 2, 0.34, 2000, (1.5, 1.5, 1.5), suave=0.5)
        h.luz_radial(1340, 620, 800, (1.0, 1.0, 1.0), k=1.0 + 1.2 * g)
        N.motas(h, t, n=100, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.18, vel=10, y0=0, y1=1080, sube=False), bloom=0.5, flash=0.25 * g)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        t0 = self.t0
        self.ev(t0, "teletipo", 0.4, -0.3, dur=self.t_jefe - t0)
        self.ev(self.t_prensa - 0.5, "periodico_gira", 0.9, 0.0, dur=0.8)
        self.ev(self.t_prensa + 0.3, "periodico_golpe", 1.0, 0.0)
        self.ev(self.t_escan, "sello_golpe", 0.9, 0.0)
        for tf in self.fl:
            self.ev(tf, "relampago_corto", 0.5, 0.2)
        self.ev(self.t_jefe, "multitud", 0.4, 0.0, dur=self.t_junio - self.t_jefe)
        self.ev(self.t_dijo, "sello_golpe", 0.8, 0.3)
        self.ev(self.t_retir - 0.1, "papel_atrapa", 0.7, 0.3)
        self.ev(self.t_retir + 0.1, "tachon", 1.0, 0.3)
        self.ev(self.t_retir + 0.5, "sello_golpe", 1.0, 0.3)
        self.ev(self.t_junio - 0.35, "barrido_aire", 0.6, 0.0, dur=0.7)
        self.ev(self.t_junio, "chincheta", 0.8, -0.2)
        dur = max(1.5, self.t_carta - self.t_trece + 1.2)
        for k in range(0, 13, 3):
            self.ev(self.t_trece - 0.2 + k * dur / 13, "pluma", 0.55, -0.3 + 0.05 * k)
        self.ev(self.t_derecho, "sello_golpe", 0.9, 0.3)
        self.ev(self.t_derecho, "hilo_tenso", 0.6, 0.2)
        self.ev(self.t_ese - 0.35, "multitud", 0.35, 0.0, dur=self.t1 - self.t_ese)
        self.ev(self.t_70 - 0.3, "subida", 0.7, 0.2, dur=1.2)
        self.ev(self.t_70, "golpe_grave", 1.0, 0.0)
        self.ev(self.t_cat - 0.6, "sello_golpe", 0.9, 0.2)
        self.ev(self.t1 - 0.8, "tinta_mancha", 0.6, 0.0, dur=0.9)
