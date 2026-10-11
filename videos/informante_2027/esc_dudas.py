# -*- coding: utf-8 -*-
"""Escena 17 «dudas»: el detective, de pie en su oficina, escribe la segunda regla; a Daniel le llueven hojas de críticas
(cada una con su sello); la campana de probabilidades sobre la regla de los años (el pico en 2027, la cola larga); la mano
que empuja la ficha de la apuesta de 2027 a 2030."""
import math

import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import noir as N
import props as PR
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from noir_pers import Detective, Frontal
from toon import elipse_, pulso

ANIOS = ["2026", "2027", "2028", "2029", "2030", "2031", "2032"]


def regla_anios(h, t, x0=220, x1=1700, y=760, sem=0):
    h.trazo(np.array([[x0 - 60, y], [x1 + 60, y]]), 8, sem, color=(225, 225, 225), jit=0.3, taper=(0, 0))
    xs = []
    for k, a in enumerate(ANIOS):
        x = x0 + (x1 - x0) * k / (len(ANIOS) - 1)
        xs.append(x)
        h.trazo(np.array([[x, y - 22], [x, y + 22]]), 6, sem + 1 + k, color=(225, 225, 225), jit=0.2, taper=(0, 0))
        N.texto_maquina(h, a, x, y + 66, 50, t, -99, cps=1e9, tono=0.94, centro=True, fuente=K.IMPACT, encuadrar=False)
    return xs


class Dudas(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.det = Detective(sem=3)
        self.dan = Frontal(sem=77)
        self.t_buen = w("buen detective")
        self.t_desc = w("desconfía")
        self.t_testigo = w("testigo")
        self.t_llov = w("llovieron")
        self.t_invest = w("Investigadores")
        self.t_noapoya = w("no se apoya")
        self.t_sufic = w("suficiente")
        self.t_yel = w("Y él mismo")
        self.t_2027 = w("Dos mil veintisiete")
        self.t_probable = w("probable")
        self.t_nunca = w("Nunca")
        self.t_seguro = w("seguro")
        self.t_finales = w("A finales")
        self.t_lento = w("lento")
        self.t_movio = w("movió")
        self.t_2030 = w("dos mil treinta")
        self.plano(t0, self.p_det)
        self.plano(self.t_llov - 0.9, self.p_criticas, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_yel - 0.35, self.p_campana, tr="empuje", dur=0.6, centro=(W * 0.35, H * 0.5))
        self.plano(self.t_finales - 0.35, self.p_mueve, tr="barrido", dur=0.55, dirx=-1)

    # ------------------------------------------------------------------ regla n.º 2
    def p_det(self, h, t, u):
        h.camara(1.1 + 0.02 * u, 1000 - 12 * u, 500, 0.006 * math.sin(t * 0.5))
        MU.oficina().pegar(h, 1.0)
        gir = smooth(clamp01((t - self.t_desc + 0.3) / 0.8))
        fum = pulso(t, self.t0 + 0.4, 1.8, 1.0)
        p = dict(x=760.0, y=905.0, s=1.0, d=1, luz=(1.0, -0.5), fumar=fum, giro=0.4 - 0.8 * gir, viento=0.08, hombros=0.3)
        self.det.dibujar(h, p)
        tip = self.det.punta_cigarro(p)
        N.humo(h, t, tip[0], tip[1], k=1.0, ancho=1.4)
        h.luz_radial(tip[0], tip[1], 90 + 120 * fum, (0.6, 0.6, 0.6), k=0.6 + fum)
        N.gotas_vidrio(h, t, (1100, -460, 2000, 400), n=90, k=0.8)
        h.ambiente[:] = 0.30
        h.luz_persiana(np.array([[60, -420], [1080, -470], [1080, 640], [-80, 900]]), k=1.5, n=15, abierto=0.5)
        h.luz_persiana(np.array([[-80, 900], [1080, 900], [900, 1100], [-420, 1100]]), k=1.1, n=9, abierto=0.5)
        h.luz_radial(1550, 60, 760, (1.0, 1.0, 1.0), k=3.0)
        N.motas(h, t, n=90, k=0.6)
        h.camara(1.0, W / 2, H / 2, 0.0)
        N.texto_maquina(h, "REGLA N.º 2", 1090, 120, 54, t, self.t_buen, cps=18, tono=0.95, encuadrar=False)
        N.texto_maquina(h, "Desconfía también", 1090, 205, 40, t, self.t_desc, cps=20, tono=0.9, encuadrar=False)
        N.texto_maquina(h, "de tu mejor testigo.", 1090, 265, 40, t, self.t_testigo - 0.6, cps=20, tono=0.97, encuadrar=False)
        return h.acabado(t, niebla=dict(dens=0.16, vel=10, y0=-300, y1=900, sube=False))

    # ------------------------------------------------------------------ le llovieron críticas
    def p_criticas(self, h, t, u):
        h.camara(1.0 + 0.014 * u, 960, 540, 0.0)
        K.pared(h, 50, 16, paneles=9)
        K.plano_(h, C.rect(-300, 960, W + 600, 400), 44, 8, grad=(12, 960, 1200))
        s = 1.5
        enc = smooth(clamp01((t - self.t_llov) / 1.0))
        self.dan.dibujar(h, dict(x=960, y=290 + 474 * s, s=s, luz=(0.0, -1.0), rim=0.9, mira=0.5 * math.sin(t * 1.1),
                                 cabeza=-0.06 * enc + 0.02 * math.sin(t * 2), **K.DAN))
        sellos = ["SIN EVIDENCIA", "ESPECULACIÓN", "DEMASIADO RÁPIDO", "CIENCIA FICCIÓN", "ALARMISMO", "¿Y LOS DATOS?", "EXAGERADO",
                  "POCO RIGOR", "NO ES CIENCIA", "IMPOSIBLE"]
        r = np.random.default_rng(12)
        for k in range(10):                                          # las hojas caen y se posan (delante y a los lados)
            tk = self.t_llov - 0.4 + k * 0.42
            if t < tk:
                continue
            a = clamp01((t - tk) / 0.9)
            xf = (160 + (k % 5) * 400 + r.uniform(-40, 40)) if k % 5 != 2 else (960 + r.uniform(-60, 60))
            yf = 250 + (k // 5) * 400 + r.uniform(-30, 60) if k % 5 != 2 else 880 + (k // 5) * 60
            x = xf + 160 * math.sin(a * 5 + k) * (1 - a)
            y = -200 + (yf + 200) * (1 - (1 - a) ** 2)
            ang = (1 - a) * (1.5 + k) + r.uniform(-0.2, 0.2)
            T = K.hoja(h, x, y, 330, 230, ang=ang, sem=100 + k * 9, renglones=2, y0=0.62, sep=30, margen=30)
            if a > 0.5:
                P = T([(0, -50)])[0]
                N.texto_maquina(h, sellos[k], P[0], P[1], 34, t, -99, cps=1e9, tono=0.04, centro=True, fuente=K.IMPACT, encuadrar=False)
        C.banda(h, "LE LLOVIERON CRÍTICAS", 960, 70, 60, t, self.t_llov - 0.2, sem=5)
        C.banda(h, "«NO SE APOYA EN EVIDENCIA CIENTÍFICA SUFICIENTE»", 960, 1010, 42, t, self.t_noapoya - 0.2, claro=True, sem=6)
        h.ambiente[:] = 0.42
        h.luz_cono(960, -420, math.pi / 2, 0.5, 2000, (1.5, 1.5, 1.5), suave=0.5)
        N.motas(h, t, n=100, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.16, vel=10, y0=-200, y1=1000, sube=False), bloom=0.45)

    # ------------------------------------------------------------------ el más probable, no el seguro
    def p_campana(self, h, t, u):
        h.camara(1.0 + 0.012 * u, 960, 540, 0.0)
        K.pared(h, 30, 8)
        xs = regla_anios(h, t, sem=20)
        a = clamp01((t - self.t_2027 + 0.4) / 1.6)
        vx = np.linspace(xs[0] - 120, xs[-1] + 60, 120)
        z = (vx - xs[1]) / (xs[1] - xs[0])
        vy = np.where(z < 0, np.exp(-z * z / 0.16), 0.22 + 0.78 * np.exp(-z / 1.1)) * 520
        n = max(2, int(120 * a))
        P = np.stack([vx[:n], 750 - vy[:n]], 1)
        if n > 3:                                                    # relleno bajo la curva (aguada) y la curva a pluma
            K.plano_(h, np.vstack([P, [[P[-1][0], 750], [P[0][0], 750]]]), 120, 40, alfa=0.45)
        h.trazo(P, 11, 41, color=(245, 245, 245), jit=0.5, taper=(0.2, 0.0))
        if t > self.t_probable - 0.3:                                # el pico
            h.trazo(np.array([[xs[1], 750], [xs[1], 230]]), 5, 42, color=(245, 245, 245), alfa=0.8, jit=0.3, taper=(0, 0))
            h.emitir(elipse_(xs[1], 230, 16, 16, n=12), 1.1)
            h.luz_radial(xs[1], 230, 380, (1.0, 1.0, 1.0), k=1.0)
        C.banda(h, "EL AÑO MÁS PROBABLE", xs[1] + 40, 150, 54, t, self.t_probable - 0.3, claro=True, sem=5)
        C.banda(h, "NUNCA DIJO «SEGURO»", 1380, 400, 60, t, self.t_nunca, sem=6)
        if t > self.t_nunca:
            K.flecha(h, (1380, 450), (1300, 640), 8, 50, u=clamp01((t - self.t_nunca - 0.2) / 0.4), curva=30)
        C.banda(h, "ÉL MISMO LO ACLARÓ", 400, 960, 46, t, self.t_yel + 0.1, sem=7)
        h.ambiente[:] = 0.5
        h.luz_radial(960, 600, 1400, (1.0, 1.0, 1.0), k=0.6)
        N.motas(h, t, n=90, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.12, vel=10, y0=0, y1=1080, sube=False), bloom=0.55)

    # ------------------------------------------------------------------ movió su apuesta hacia 2030
    def p_mueve(self, h, t, u):
        h.camara(1.0 + 0.012 * u, 960, 560, 0.0)
        K.pared(h, 30, 8)
        xs = regla_anios(h, t, sem=20)
        mv = smooth(clamp01((t - self.t_movio + 0.2) / max(1.0, self.t_2030 - self.t_movio + 0.3)))
        fx = xs[1] + (xs[4] - xs[1]) * mv
        # la ficha de la apuesta
        h.trazo(np.array([[fx, 750], [fx, 520]]), 7, 40, color=(240, 240, 240), jit=0.3, taper=(0, 0))
        h.pieza(np.asarray(elipse_(fx, 450, 96, 96, n=40)), 228, 41, w=7, luz=(0.2, -1), d=12, trama=0.2, rim=0)
        h.anillo(h.tf(np.asarray(elipse_(fx, 450, 76, 76, n=40))), 5 * h.zoom, 42, color=(30, 30, 30), jit=0.4)
        N.texto_maquina(h, "SU", fx, 420, 40, t, -99, cps=1e9, tono=0.05, centro=True, fuente=K.IMPACT, encuadrar=False)
        N.texto_maquina(h, "APUESTA", fx, 468, 34, t, -99, cps=1e9, tono=0.05, centro=True, fuente=K.IMPACT, encuadrar=False)
        if 0 < mv < 1 or t > self.t_movio - 0.6:
            PR.mano(h, fx - 190, 460 + 6 * math.sin(t * 6), 1.25, ang=0.0, d=1, sem=60, dedos=0.5)
        for q in range(6):                                           # caracoles: «todo va más lento»
            xx = 300 + q * 240 + ((t - self.t_finales) * 26) % 240
            h.pieza(np.asarray(elipse_(xx, 950, 30, 24, n=18)), 120, 80 + q * 3, w=4, luz=(0.2, -1), d=5, trama=0.4, rim=0.7)
            h.trazo(np.array([[xx - 8, 950], [xx + 4, 940], [xx + 10, 952], [xx, 960]]), 3, 81 + q * 3, jit=0.2)
            h.pieza(np.asarray(elipse_(xx + 36, 962, 28, 9, n=12)), 170, 82 + q * 3, w=3, luz=(0.2, -1), d=3, trama=0, rim=0.5)
        C.banda(h, "FINALES DE 2025", 420, 100, 60, t, self.t_finales + 0.1, sem=5)
        C.banda(h, "«TODO VA MÁS LENTO»", 420, 210, 54, t, self.t_lento - 0.6, claro=True, sem=6)
        C.banda(h, "≈ 2030", xs[4], 250, 110, t, self.t_2030, claro=True, sem=7)
        h.ambiente[:] = 0.5
        h.luz_radial(fx, 450, 700, (1.0, 1.0, 1.0), k=1.0)
        N.motas(h, t, n=90, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.12, vel=10, y0=0, y1=1080, sube=False), bloom=0.5)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        t0 = self.t0
        self.ev(t0, "lluvia_amb", 0.7, 0.0, dur=self.t_llov - t0)
        self.ev(t0 + 0.4, "calada", 0.6, -0.2, dur=1.4)
        for ini, n in ((self.t_buen, 11), (self.t_desc, 17), (self.t_testigo - 0.6, 20)):
            self.ev(ini, "tecleo_rapido", 0.5, 0.3, dur=n / 19)
            self.ev(ini + n / 19 + 0.05, "carro_maquina", 0.4, 0.4)
        self.ev(self.t_llov - 0.9, "barrido_aire", 0.6, 0.0, dur=0.7)
        self.ev(self.t_llov - 0.4, "papel_viento", 0.8, 0.0, dur=4.4)
        for k in range(0, 10, 2):
            self.ev(self.t_llov + 0.5 + k * 0.42, "papel_atrapa", 0.5, -0.6 + 0.14 * k)
        self.ev(self.t_noapoya - 0.2, "sello_golpe", 0.9, 0.0)
        self.ev(self.t_yel - 0.35, "barrido_aire", 0.6, 0.0, dur=0.7)
        self.ev(self.t_2027 - 0.4, "lapiz", 0.7, -0.2)
        self.ev(self.t_probable - 0.3, "sello_golpe", 0.9, -0.3)
        self.ev(self.t_nunca, "sello_golpe", 0.9, 0.3)
        self.ev(self.t_finales - 0.35, "barrido_aire", 0.6, 0.0, dur=0.6)
        self.ev(self.t_movio - 0.2, "fichas_empuja", 0.9, 0.0)
        self.ev(self.t_2030, "sello_golpe", 1.0, 0.3)
        self.ev(self.t_2030, "golpe_grave", 0.8, 0.0)
        self.ev(self.t1 - 0.8, "tinta_mancha", 0.6, 0.0, dur=0.9)
