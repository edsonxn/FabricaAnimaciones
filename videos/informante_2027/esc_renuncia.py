# -*- coding: utf-8 -*-
"""Escena 4 «renuncia»: abril de 2024, Daniel vacía su escritorio (los objetos caen a la caja de cartón); la carta con la razón,
escrita a máquina, y la sombra de la máquina que cae sobre el papel; el pasillo: camina con su caja hacia la puerta, donde
lo espera una hoja bajo un foco."""
import math

import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import mundos27 as M27
import noir as N
import props as PR
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from noir_pers import Frontal
from toon import elipse_, pulso


def caja_carton(h, x, y, s=1.0, sem=0, tapa=True):
    """Caja de mudanza (y = base)."""
    h.pieza(C.rect(x - 170 * s, y - 210 * s, 340 * s, 210 * s), 120, sem, w=6 * s, luz=(0.2, -1), d=14 * s, trama=0.5, rim=0.7)
    h.trazo(np.array([[x - 170 * s, y - 150 * s], [x + 170 * s, y - 150 * s]]), 3 * s, sem + 1, alfa=0.5)
    K.plano_(h, C.rect(x - 50 * s, y - 120 * s, 100 * s, 30 * s), 40, sem + 2, alfa=0.8)
    if tapa:
        for q in (-1, 1):
            h.pieza(np.array([[x + q * 170 * s, y - 210 * s], [x + q * 300 * s, y - 280 * s], [x + q * 290 * s, y - 300 * s],
                              [x + q * 160 * s, y - 226 * s]]), 140, sem + 3 + q, w=5 * s, luz=(0.2, -1), d=8 * s, trama=0.3, rim=0.7)


class Renuncia(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.dan = Frontal(sem=77)
        self.t_abril = w("Abril")
        self.t_vacio = w("vació")
        self.t_dejo = w("Dejó")
        self.t_habia = w("Había perdido")
        self.t_empresa = w("empresa")
        self.t_resp = w("responsabilidad")
        self.t_maq = w("máquina")
        self.t_todo = w("todo", fin=True)
        self.t_puerta = w("Y en la puerta")
        self.t_papel = w("papel")
        self.plano(t0, self.p_caja)
        self.plano(self.t_dejo - 0.35, self.p_carta, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_puerta - 0.4, self.p_pasillo, tr="humo", dur=0.7)

    # ------------------------------------------------------------------ vació su escritorio
    def p_caja(self, h, t, u):
        h.camara(1.0 + 0.04 * u, 980 + 14 * u, 540, 0.0)
        M27.despacho().pegar(h, 1.0)
        s = 1.7
        mira = -0.8 if t > self.t_vacio else 0.2 * math.sin(t)
        p = dict(x=820, y=230 + 474 * s, s=s, luz=(-0.7, -0.6), rim=0.9, mira=mira,
                 cabeza=-0.12 * smooth(clamp01((t - self.t_vacio) / 0.5)), **K.DAN)
        self.dan.dibujar(h, p)
        PR.mesa(h, 960, 900, ancho=1700, fondo=170, alto=300, tono=72, sem=30)
        caja_carton(h, 1320, 850, 1.25, 40)
        # sus cosas caen a la caja una tras otra: libro, marco, planta, taza
        for k in range(4):
            tk = self.t_vacio - 0.2 + k * 0.55
            a = clamp01((t - tk) / 0.45)
            if a <= 0 or a >= 1:
                if a <= 0:                                           # todavía sobre la mesa
                    x0 = 420 + k * 150
                    self._cosa(h, k, x0, 800, 0.0)
                continue
            x0 = 420 + k * 150
            x = x0 + (1320 - x0) * a
            y = 800 - 420 * math.sin(math.pi * a) + 0 * a
            self._cosa(h, k, x, y, a * 3.0)
        C.banda(h, "ABRIL DE 2024", 420, 120, 72, t, self.t_abril, sem=5)
        C.banda(h, "ÚLTIMO DÍA", 420, 220, 44, t, self.t_vacio, claro=True, sem=6)
        h.ambiente[:] = 0.36
        C.luz_rect(h, C.rect(-300, -140, 1240, 760), 1.1, suave_=14)
        h.luz_cono(1200, -500, math.pi / 2, 0.5, 1900, (1.4, 1.4, 1.4), suave=0.5)
        N.motas(h, t, n=90, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.16, vel=8, y0=-200, y1=1000, sube=False), bloom=0.45)

    def _cosa(self, h, k, x, y, ang):
        c = np.array([x, y - 50])
        if k == 0:                                                   # libro
            h.pieza(PR.rot(C.rect(x - 60, y - 100, 120, 100), ang, c), 60, 200, w=4, luz=(0.2, -1), d=8, trama=0.4, rim=0.8)
        elif k == 1:                                                 # marco con foto
            h.pieza(PR.rot(C.rect(x - 50, y - 130, 100, 130), ang, c), 40, 210, w=4, luz=(0.2, -1), d=6, trama=0.2, rim=0.8)
            K.plano_(h, PR.rot(C.rect(x - 38, y - 118, 76, 106), ang, c), 190, 211)
        elif k == 2:                                                 # planta
            h.pieza(PR.rot(np.array([[x - 40, y - 60], [x + 40, y - 60], [x + 30, y], [x - 30, y]]), ang, c), 150, 220, w=4, luz=(0.2, -1),
                    d=6, trama=0.3, rim=0.7)
            for q in range(5):
                a = -math.pi / 2 + (q - 2) * 0.4
                h.pieza(PR.rot(np.array([[x, y - 60], [x + 70 * math.cos(a - 0.2), y - 60 + 90 * math.sin(a - 0.2)],
                                         [x + 96 * math.cos(a), y - 60 + 120 * math.sin(a)]]), ang, c), 36, 221 + q, w=3, luz=(0.2, -1),
                        d=4, trama=0.2, rim=0.7)
        else:                                                        # taza
            h.pieza(PR.rot(np.array([[x - 34, y - 70], [x + 34, y - 70], [x + 28, y], [x - 28, y]]), ang, c), 220, 230, w=4, luz=(0.2, -1),
                    d=8, trama=0.2, rim=0.6)

    # ------------------------------------------------------------------ la razón, por escrito
    def p_carta(self, h, t, u):
        h.camara(1.0 + 0.018 * u, 960, 540, 0.01)
        MU.escritorio().pegar(h, 1.0, oscuro=0.75, dx=-60, dy=-40)
        T = K.hoja(h, 960, 560, 1380, 820, ang=-0.02, sem=10)
        lineas = (("«PERDÍ LA CONFIANZA EN QUE", self.t_habia), ("LA EMPRESA SE COMPORTARÍA", self.t_empresa - 0.3),
                  ("CON RESPONSABILIDAD».", self.t_resp - 0.6))
        for k, (s_, tk) in enumerate(lineas):
            P = T([(-600, -250 + k * 130)])[0]
            N.texto_maquina(h, s_, P[0], P[1], 76, t, tk, cps=20, tono=0.05, encuadrar=False)
        P = T([(120, 190)])[0]
        N.texto_maquina(h, "— D. K., abril de 2024", P[0], P[1], 46, t, self.t_resp + 0.8, cps=24, tono=0.2, encuadrar=False)
        sm = smooth(clamp01((t - self.t_maq + 0.3) / 1.2))            # la sombra de la máquina cae sobre el papel
        if sm > 0:
            K.plano_(h, np.array([[1500 - 900 * sm, -100], [1960 - 500 * sm, -100], [1960 - 300 * sm, 1200], [1700 - 1000 * sm, 1200]]),
                     3, 60, alfa=0.78 * sm)
            led = 0.5 + 0.5 * math.sin(t * 2.4)
            h.emitir(elipse_(1640 - 620 * sm, 150, 16, 16, n=12), 1.3 * sm * led)
            h.luz_radial(1640 - 620 * sm, 150, 300, (1.0, 1.0, 1.0), k=0.9 * sm * led)
        C.banda(h, "LA MÁQUINA QUE LO CAMBIA TODO", 1340, 990, 50, t, self.t_maq, sem=5)
        h.ambiente[:] = 0.36
        h.luz_cono(760, -560, math.pi / 2 - 0.08, 0.56, 2300, (1.6, 1.6, 1.6), suave=0.5)
        N.motas(h, t, n=80, k=0.6)
        return h.acabado(t, niebla=None, bloom=0.4)

    # ------------------------------------------------------------------ en la puerta lo esperaba un papel
    def p_pasillo(self, h, t, u):
        h.camara(1.0 + 0.04 * u, 1000 + 30 * u, 540, 0.0)
        K.pared(h, 44, 14, paneles=10)
        K.plano_(h, C.rect(-300, 930, W + 600, 400), 30, 8, grad=(8, 930, 1200))
        for k in range(4):                                           # apliques del pasillo
            x = 160 + k * 420
            h.pieza(C.rect(x - 16, 150, 32, 70), 150, 30 + k, w=3, luz=(0, -1), d=4, trama=0, rim=0.8)
            h.emitir(C.rect(x - 12, 156, 24, 58), 0.5)
            h.luz_cono(x, 190, math.pi / 2, 0.5, 520, (0.8, 0.8, 0.8), k=0.5, suave=0.7)
        K.puerta(h, 1390, 130, 400, 800, sem=20, tono=30, rendija=0.0)
        Tp = K.hoja(h, 1590, 420, 210, 280, ang=0.04 + 0.02 * math.sin(t * 1.5), sem=50, renglones=5, y0=0.3, sep=34, margen=26)
        P = Tp([(0, -100)])[0]
        N.texto_maquina(h, "ACUERDO", P[0], P[1], 30, t, -99, cps=1e9, tono=0.05, centro=True, fuente=N.FUENTE_SELLO, encuadrar=False)
        av = smooth(clamp01((t - self.t_puerta + 0.3) / (self.t1 - self.t_puerta)))
        x = 240 + 760 * av
        h.luz_radial(x + 40, 640, 620, (1.0, 1.0, 1.0), k=1.5)
        man = K.caminante(h, x, 1010, 1.4, fase=K.fase_paso(x - 240, 1.4), sem=40, tono=70, luz=(1.0, -0.4), rim=0.95, carga=True)
        caja_carton(h, man[0] + 40, man[1] + 150, 0.72, 60, tapa=False)
        C.banda(h, "LO ESPERABA UN PAPEL", 700, 110, 60, t, self.t_papel - 0.4, sem=5)
        h.ambiente[:] = 0.34
        h.luz_cono(1590, -200, math.pi / 2, 0.30, 1300, (1.9, 1.9, 1.9), suave=0.45)
        N.motas(h, t, n=100, k=0.8, caja=(1200, 0, 1900, 1000))
        return h.acabado(t, niebla=dict(dens=0.24, vel=12, y0=0, y1=1080, sube=False), bloom=0.55)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        t0 = self.t0
        self.ev(self.t_abril, "sello_golpe", 0.9, -0.3)
        for k in range(4):
            self.ev(self.t_vacio + 0.25 + k * 0.55, "papel_atrapa", 0.7, 0.3)
        self.ev(self.t_dejo - 0.35, "barrido_aire", 0.6, 0.0, dur=0.7)
        for s_, tk, n in ((0, self.t_habia, 26), (1, self.t_empresa - 0.3, 25), (2, self.t_resp - 0.6, 21)):
            self.ev(tk, "tecleo_rapido", 0.55, -0.2, dur=n / 20)
            self.ev(tk + n / 20 + 0.05, "carro_maquina", 0.4, 0.2)
        self.ev(self.t_maq - 0.3, "sombra_crece", 0.8, 0.0, dur=3.0)
        self.ev(self.t_maq, "golpe_grave", 0.9, 0.0)
        self.ev(self.t_puerta - 0.4, "zumbido_lampara", 0.4, 0.0, dur=self.t1 - self.t_puerta + 0.4)
        for k in range(6):
            self.ev(self.t_puerta + k * 0.6, "paso_madera", 0.6, -0.5 + 0.18 * k)
        self.ev(self.t_papel - 0.4, "sello_golpe", 0.8, 0.0)
        self.ev(self.t1 - 0.8, "tinta_mancha", 0.6, 0.0, dur=0.9)
