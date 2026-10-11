# -*- coding: utf-8 -*-
"""Escena 1 «regla» (gancho): el detective en su oficina, entre las rayas de la persiana, dicta su regla; grúa sobre la bahía de
Hong Kong bajo la lluvia hasta la torre; dentro, el empleado de espaldas ante el monitor con la videollamada (hablan, asienten);
empuje a la rejilla: las caras se descomponen en máscaras una a una y, al abrir el plano, solo él queda iluminado."""
import math

import numpy as np

import comun as C
import mundos as MU
import noir as N
from basen import BaseNoir
from motor import H, W, clamp01, smooth
from noir_pers import Detective
from toon import Pista, pulso

CAJA = (520.0, 110.0, 1180.0, 640.0)        # pantalla del monitor (mundo)


class Regla(BaseNoir):
    TR_SALIDA = ("tinta", 0.8)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.det = Detective(sem=3)
        self.call = C.Llamada(sem=40)
        self.t_regla = w("regla")
        self.t_nofies = w("No te")
        self.t_fiate = w("Fíate")
        self.t_ves = w("ves", fin=True)
        self.t_murio = w("murió")
        self.t_enero = w("enero")
        self.t_hk = w("Hong")
        self.t_emp = w("Un empleado")
        self.t_vio = w("Vio")
        self.t_escucho = w("Escuchó")
        self.t_obed = w("Obedeció")
        self.t_yen = w("Y en esa")
        self.t_nadie = w("nadie", frase=3)
        self.t_real = w("real", fin=True)
        self.t_excepto = w("excepto")
        self.rayos = [self.t_murio - 0.1, self.t_hk + 0.5]
        self.cam_o = Pista([(t0, (1150, 470, 1.0)), (self.t_nofies, (1060, 480, 1.18), "io"), (self.t_ves + 0.6, (960, 500, 1.5), "io")])
        self.cam_b = Pista([(self.t_murio - 0.6, (1010, 240, 0.70)), (self.t_enero, (1010, 330, 0.76), "io"),
                            (self.t_emp - 0.2, (1010, 470, 1.0), "io")])
        self.cam_l = Pista([(self.t_emp - 0.4, (960, 560, 0.94)), (self.t_vio, (1000, 520, 1.05), "io"),
                            (self.t_yen, (1090, 440, 1.22), "io"), (self.t_real, (1110, 430, 1.62), "io"),
                            (self.t_excepto - 0.15, (1110, 430, 1.66), "l"), (self.t_excepto + 0.9, (930, 580, 0.9), "o"),
                            (self.t1 + 1, (930, 585, 0.94), "l")])
        self.plano(t0, self.p_oficina)
        self.plano(self.t_murio - 0.5, self.p_bahia, tr="relampago", dur=0.7)
        self.plano(self.t_emp - 0.35, self.p_llamada, tr="empuje", dur=0.7, centro=(W * 0.52, H * 0.42))

    # ------------------------------------------------------------------ la oficina del detective
    def p_oficina(self, h, t, u):
        cx, cy, z = self.cam_o(t)
        h.camara(z, cx, cy, 0.008 * math.sin(t * 0.5))
        MU.oficina().pegar(h, 1.0)
        gir = smooth(clamp01((t - self.t_fiate + 0.4) / 0.9))
        fum = pulso(t, self.t_regla + 1.6, 2.2, 1.0)
        p = dict(x=820.0, y=905.0, s=1.0, d=1, luz=(1.0, -0.5), fumar=fum, giro=-0.5 + 0.9 * gir, viento=0.08, hombros=0.3)
        self.det.dibujar(h, p)
        tip = self.det.punta_cigarro(p)
        h.emitir(np.array([[tip[0] - 4, tip[1] - 4], [tip[0] + 4, tip[1] - 4], [tip[0] + 4, tip[1] + 4], [tip[0] - 4, tip[1] + 4]]),
                 0.9 + 0.5 * fum)
        h.luz_radial(tip[0], tip[1], 90 + 120 * fum, (0.6, 0.6, 0.6), k=0.6 + fum)
        N.gotas_vidrio(h, t, (1100, -460, 2000, 400), n=90, k=0.8)
        h.ambiente[:] = 0.30
        par = 1.0 + 0.5 * N.relampago(t, [self.t_regla - 0.5])
        h.luz_persiana(np.array([[60, -420], [1080, -470], [1080, 640], [-80, 900]]), k=1.5 * par, n=15, abierto=0.5)
        h.luz_persiana(np.array([[-80, 900], [1080, 900], [900, 1100], [-420, 1100]]), k=1.1 * par, n=9, abierto=0.5)
        h.luz_radial(1550, 60, 760, (1.0, 1.0, 1.0), k=3.2)                 # la ciudad detrás del cristal
        N.humo(h, t, tip[0], tip[1], k=1.0, ancho=1.4)
        N.motas(h, t, n=90, k=0.6)
        # la regla, a máquina (fija en pantalla: con la cámara en movimiento los renglones se encimaban)
        h.camara(1.0, W / 2, H / 2, 0.0)
        N.texto_maquina(h, "REGLA N.º 1", 1090, 120, 54, t, self.t_regla, cps=18, tono=0.95, encuadrar=False)
        N.texto_maquina(h, "No te fíes de lo que te cuentan.", 1090, 205, 38, t, self.t_nofies, cps=20, tono=0.85, encuadrar=False)
        N.texto_maquina(h, "Fíate de lo que ves.", 1090, 265, 38, t, self.t_fiate, cps=18, tono=0.97, encuadrar=False)
        return h.acabado(t, niebla=dict(dens=0.16, vel=10, y0=-300, y1=900, sube=False))

    # ------------------------------------------------------------------ Hong Kong
    def p_bahia(self, h, t, u):
        cx, cy, z = self.cam_b(t)
        h.camara(z, cx, cy, 0.01 * math.sin(t * 0.3))
        C.hk_cielo().pegar(h, 0.05, dx=-(t * 5.0) % 300)
        C.hk_lejos().pegar(h, 0.3, bruma=0.55, tono_bruma=0.36)
        C.hk_agua().pegar(h, 0.6)
        C.hk_medio().pegar(h, 0.6, bruma=0.22, tono_bruma=0.36)
        h.ambiente[:] = 1.25
        fl = max(N.relampago(t, self.rayos), 0.0)
        h.ambiente[:] += 1.2 * fl
        h.luz_radial(1000, 700, 2200, (0.9, 0.9, 0.9), k=1.0)               # resplandor de la ciudad sobre la bahía
        # la ventana del empleado: un piso de la torre central se enciende
        enc = smooth(clamp01((t - self.t_hk) / 0.8))
        with h.capa(0.6):
            if enc > 0:
                h.emitir(C.rect(905, 420, 230, 30), 1.2 * enc)
                h.luz_radial(1020, 436, 260, (0.9, 0.9, 0.9), k=1.2 * enc)
        N.lluvia(h, t, n=700, vel=1700)
        h.camara(1.0, W / 2, H / 2, 0.0)
        C.banda(h, "HONG KONG", 420, 150, 96, t, self.t_hk, sem=5)
        C.banda(h, "ENERO DE 2024", 420, 262, 44, t, self.t_hk + 0.35, claro=True, sem=6)
        return h.acabado(t, niebla=dict(dens=0.26, y0=200, y1=1000, vel=30), flash=0.3 * fl, bloom=0.5)

    # ------------------------------------------------------------------ la videollamada
    def p_llamada(self, h, t, u):
        cx, cy, z = self.cam_l(t)
        h.camara(z, cx, cy, 0.006 * math.sin(t * 0.6))
        C.oficina_hk().pegar(h, 1.0)
        C.monitor(h, CAJA, sem=60)
        # las caras se caen una a una entre «nadie» y «real»
        orden = [1, 4, 0, 5, 2, 3]
        dur = max(0.6, self.t_real - self.t_nadie)
        falso = [0.0] * 6
        for q, k in enumerate(orden):
            falso[k] = clamp01((t - (self.t_nadie + q * dur / 6.5)) / 0.55)
        habla = None
        if self.t_escucho - 0.2 < t < self.t_yen - 0.3:
            habla = [0, 3, 1][int((t - self.t_escucho) / 1.1) % 3]
        asiente = pulso(t, self.t_obed - 0.1, 2.2, 1.0)
        solo = smooth(clamp01((t - self.t_excepto) / 0.7))
        self.call.dibujar(h, t, CAJA, falso=falso, habla=habla, asiente=asiente, enc=1.0 - 0.45 * solo)
        C.teclado(h, 760, 900, 640, sem=70)
        ten = smooth(clamp01((t - self.t_nadie) / 1.5))
        C.espalda(h, 520, 880, 1.0, sem=80, luz=(0.5, -0.8), gira=0.5 * smooth(clamp01((t - self.t_vio) / 0.8)), hombros=ten)
        C.banda(h, "NADIE ERA REAL", CAJA[0] + CAJA[2] / 2, CAJA[1] + CAJA[3] / 2 + 4, 84, t, self.t_real - 0.15, sem=7, mundo=True)
        h.ambiente[:] = 0.42 - 0.26 * solo
        h.luz_radial(620, 760, 620, (0.8, 0.8, 0.8), k=0.9 * (1 - solo))        # la pantalla le da en la nuca y los hombros
        if solo > 0:                                    # solo él queda iluminado
            h.luz_cono(520, -260, math.pi / 2, 0.36, 1500, (1.6, 1.6, 1.6), k=1.3 * solo, suave=0.5)
        N.motas(h, t, n=70, k=0.5)
        return h.acabado(t, niebla=None, bloom=0.45)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        t0 = self.t0
        self.ev(t0, "lluvia_amb", 0.8, 0.0, dur=self.t1 - t0)
        self.ev(self.t_regla - 0.5, "trueno_noir", 0.6, 0.3, dur=4.0)
        for ini, n, cps in ((self.t_regla, 11, 18), (self.t_nofies, 32, 20), (self.t_fiate, 20, 18)):
            for i in range(n):
                self.ev(ini + i / cps, "tecla", 0.4, -0.3 + 0.3 * (i / n), tono=1.0 + 0.04 * ((i * 7) % 5))
            self.ev(ini + n / cps + 0.05, "carro_maquina", 0.45, 0.2)
        self.ev(self.t_regla + 1.6, "calada", 0.6, -0.1, dur=1.4)
        for tr in self.rayos:
            self.ev(tr, "trueno_noir", 0.85, -0.2, dur=4.0)
        self.ev(self.t_hk, "sello_golpe", 0.9, -0.3)
        self.ev(self.t_emp - 0.35, "barrido_aire", 0.6, 0.0, dur=0.8)
        self.ev(self.t_real - 0.1, "sello_golpe", 1.0, 0.1)
        self.ev(self.t1 - 0.8, "tinta_mancha", 0.6, 0.0, dur=0.9)
