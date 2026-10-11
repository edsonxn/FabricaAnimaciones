# -*- coding: utf-8 -*-
"""Escena 3 «profecia»: la hoja del calendario «AGOSTO 2021» y la regla del tiempo hasta ChatGPT; Daniel de espaldas ante el
monitor donde se escribe el título del blog; tres aciertos, cada uno en su plano: la cadena de pasos que se enciende
(máquinas que razonan), las torres de fajos que crecen (entrenamientos que cuestan fortunas) y la tubería de chips con la
válvula que se cierra entre EE. UU. y China; la revista de ciencia ficción que queda tapada por el periódico de ayer."""
import math

import numpy as np

import comun as C
import kit27 as K
import noir as N
import props as PR
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from toon import elipse_, pulso

CAJA = (560.0, 120.0, 1120.0, 620.0)


class Profecia(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_agosto = w("Agosto")
        self.t_faltaba = w("Faltaba")
        self.t_chat = w("ChatGPT")
        self.t_publico = w("Daniel publicó")
        self.t_titulo = w("título")
        self.t_como = w("cómo se verá")
        self.t_desc = w("Describió")
        self.t_paso = w("paso a paso")
        self.t_entren = w("Entrenamientos")
        self.t_fort = w("fortunas")
        self.t_eeuu = w("Y a Estados")
        self.t_cerr = w("cerrándole")
        self.t_chips = w("chips")
        self.t_aquel = w("En aquel")
        self.t_ficc = w("ficción")
        self.t_hoy = w("Hoy")
        self.t_ayer = w("ayer")
        self.plano(t0, self.p_fecha)
        self.plano(self.t_publico - 0.35, self.p_blog, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_desc - 0.3, self.p_razona, tr="empuje", dur=0.55, centro=(W * 0.5, H * 0.5))
        self.plano(self.t_entren - 0.3, self.p_fortunas, tr="barrido", dur=0.5, dirx=-1)
        self.plano(self.t_eeuu - 0.3, self.p_grifo, tr="barrido", dur=0.5, dirx=1)
        self.plano(self.t_aquel - 0.35, self.p_ayer, tr="humo", dur=0.7)

    # ------------------------------------------------------------------ agosto de 2021
    def p_fecha(self, h, t, u):
        h.camara(1.0 + 0.012 * u, 960 + 4 * u, 540, 0.0)
        K.pared(h, 58, 22, ladrillo=True)
        K.calendario(h, t, self.t_agosto, "AGOSTO", "2021", "", cx=480, cy=540, s=1.0, sem=20)
        # regla del tiempo: de agosto de 2021 a noviembre de 2022
        a = smooth(clamp01((t - self.t_faltaba) / 1.6))
        x0, x1, y = 880, 1760, 600
        if a > 0:
            h.trazo(np.array([[x0, y], [x0 + (x1 - x0) * a, y]]), 9, 60, color=(232, 232, 232), jit=0.4, taper=(0, 0))
            for k in range(16):
                if k / 15 <= a:
                    xx = x0 + (x1 - x0) * k / 15
                    h.trazo(np.array([[xx, y - (26 if k % 3 == 0 else 14)], [xx, y + 4]]), 5, 61 + k, color=(232, 232, 232), jit=0.2,
                            taper=(0, 0))
        C.banda(h, "AGO 2021", x0 + 60, y + 80, 40, t, self.t_faltaba, claro=True, sem=5)
        C.banda(h, "FALTABAN 15 MESES", (x0 + x1) / 2, y - 130, 60, t, self.t_faltaba + 0.7, sem=6)
        C.banda(h, "CHATGPT · NOV 2022", x1 - 130, y + 80, 40, t, self.t_chat, claro=True, sem=7)
        if t > self.t_chat:
            K.plano_(h, np.asarray(elipse_(x1, y, 22, 22, n=16)), 240, 90)
            h.emitir(elipse_(x1, y, 22, 22, n=16), 0.8)
        h.ambiente[:] = 0.5
        h.luz_radial(440, 420, 1000, (1.0, 1.0, 1.0), k=1.0)
        h.luz_radial(1320, 600, 900, (1.0, 1.0, 1.0), k=0.8 * a)
        N.motas(h, t, n=90, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.16, vel=10, y0=200, y1=1080, sube=False), bloom=0.45)

    # ------------------------------------------------------------------ el blog
    def p_blog(self, h, t, u):
        h.camara(1.0 + 0.022 * u, 1000 + 12 * u, 500, 0.0)
        C.oficina_hk().pegar(h, 1.0)
        C.monitor(h, CAJA, sem=60)
        x, y, w_, hh = CAJA
        K.plano_(h, C.rect(x, y, w_, hh), 205, 61)
        K.plano_(h, C.rect(x, y, w_, 60), 40, 62)
        for q in range(3):
            K.plano_(h, np.asarray(elipse_(x + 34 + q * 34, y + 30, 10, 10, n=12)), 150, 63 + q)
        N.texto_maquina(h, "blog personal  ·  6 ago 2021", x + 150, y + 14, 30, t, -99, cps=1e9, tono=0.8, encuadrar=False)
        N.texto_maquina(h, "WHAT 2026 LOOKS LIKE", x + 70, y + 110, 78, t, self.t_publico + 0.5, cps=11, tono=0.03, fuente=K.IMPACT,
                        track=3.0, encuadrar=False)
        N.texto_maquina(h, "(Cómo se verá 2026)", x + 74, y + 230, 46, t, self.t_como, cps=22, tono=0.05, encuadrar=False)
        if int(t * 2.5) % 2 == 0:                                     # cursor que parpadea
            K.plano_(h, C.rect(x + 74, y + 300, 18, 34), 30, 69)
        r = np.random.default_rng(11)
        for k in range(8):                                            # el texto del blog se va llenando
            tk = self.t_titulo + k * 0.5
            a = clamp01((t - tk) / 0.25)
            if a > 0:
                K.plano_(h, C.rect(x + 74, y + 330 + k * 34, (w_ - 150) * r.uniform(0.6, 1.0) * a, 10), 120, 70 + k)
        C.luz_rect(h, C.rect(x, y, w_, hh), 1.05, suave_=5.0)
        C.teclado(h, 800, 900, 640, sem=75)
        C.espalda(h, 540, 880, 1.0, sem=80, luz=(0.5, -0.8), gira=0.3 * math.sin(t * 0.5), hombros=0.1 + 0.1 * math.sin(t * 9))
        C.banda(h, "TÍTULO SIN ADORNOS", 1380, 880, 46, t, self.t_titulo, claro=True, sem=5)
        h.ambiente[:] = 0.36
        h.luz_radial(640, 760, 640, (0.8, 0.8, 0.8), k=0.9)
        N.motas(h, t, n=70, k=0.5)
        return h.acabado(t, niebla=None, bloom=0.45)

    # ------------------------------------------------------------------ máquinas que razonan paso a paso
    def p_razona(self, h, t, u):
        h.camara(1.0 + 0.04 * u, 960, 540, 0.0)
        K.pared(h, 30, 8)
        PR.caja_negra(h, 300, 960, 1.25, 1.0, t, sem=20, cable=False)
        n = 5
        dur = 2.2
        for k in range(n):                                            # la cadena de pasos se enciende eslabón a eslabón
            cx, cy = 720 + k * 250, 620 - k * 80
            tk = self.t_paso - 0.9 + k * dur / n
            on = smooth(clamp01((t - tk) / 0.3))
            if k < n - 1:
                K.flecha(h, (cx + 78, cy - 22), (cx + 172, cy - 58), 9, 60 + k * 3, u=clamp01((t - tk - 0.2) / 0.3))
            h.pieza(np.asarray(elipse_(cx, cy, 70, 70, n=40)), 40 + 190 * on, 40 + k, w=6, luz=(0.2, -1), d=12, trama=0.4, rim=0.9)
            if on > 0:
                h.emitir(elipse_(cx, cy, 58, 58, n=30), 0.5 * on, blur=5)
                N.texto_maquina(h, str(k + 1), cx, cy, 74, t, -99, cps=1e9, tono=0.05, centro=True, fuente=K.IMPACT, encuadrar=False)
                h.luz_radial(cx, cy, 360, (1.0, 1.0, 1.0), k=0.9 * on)
        h.trazo(np.array([[420, 520], [560, 590], [650, 620]]), 8, 90, color=(200, 200, 200), jit=0.5)
        C.banda(h, "MÁQUINAS QUE RAZONAN PASO A PASO", 960, 130, 56, t, self.t_desc + 0.5, sem=5)
        C.banda(h, "ACIERTO N.º 1", 1560, 990, 44, t, self.t_paso, claro=True, sem=6)
        h.ambiente[:] = 0.4
        h.luz_radial(300, 600, 900, (1.0, 1.0, 1.0), k=0.9)
        N.motas(h, t, n=90, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.18, vel=10, y0=200, y1=1080, sube=False), bloom=0.55)

    # ------------------------------------------------------------------ entrenamientos que cuestan fortunas
    def p_fortunas(self, h, t, u):
        h.camara(1.0 + 0.05 * u, 960, 560 - 20 * u, 0.0)
        K.pared(h, 40, 12, paneles=7)
        PR.mesa(h, 960, 940, ancho=1700, fondo=150, alto=260, tono=70, sem=30)
        cre = smooth(clamp01((t - self.t_entren) / max(1.2, self.t_fort - self.t_entren + 0.8)))
        for k in range(6):                                            # torres de fajos cada vez más altas
            n = int(1 + cre * (2 + k * 2.6))
            K.billetes(h, 330 + k * 250, 870, n, 0.95, 100 + k * 40)
        C.banda(h, "ENTRENAMIENTOS QUE CUESTAN FORTUNAS", 960, 110, 52, t, self.t_entren + 0.2, sem=5)
        C.banda(h, "ACIERTO N.º 2", 380, 230, 44, t, self.t_fort, claro=True, sem=6)
        h.ambiente[:] = 0.3
        PR.lampara_colgante(h, 1500, -700, largo=520, ang=0.1 * math.sin(t * 1.2), k=1.2, sem=20, abre=0.8, alcance=1900)
        N.motas(h, t, n=100, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.18, vel=10, y0=-200, y1=1000, sube=False), bloom=0.45)

    # ------------------------------------------------------------------ el grifo de los chips
    def p_grifo(self, h, t, u):
        h.camara(1.0 + 0.04 * u, 960, 540, 0.0)
        K.pared(h, 46, 16, ladrillo=True)
        y = 560
        cie = smooth(clamp01((t - self.t_cerr) / 0.7))
        h.pieza(C.rect(-100, y - 90, W + 200, 180), 70, 20, w=7, luz=(0.2, -1), d=18, trama=0.6, rim=0.8)          # la tubería
        K.plano_(h, C.rect(-100, y - 52, W + 200, 104), 12, 21)
        for xb in (300, 700, 1220, 1620):                             # bridas con tornillos
            h.pieza(C.rect(xb - 22, y - 112, 44, 224), 96, 22 + xb, w=5, luz=(0.2, -1), d=8, trama=0.4, rim=0.8)
        for k in range(9):                                            # los chips viajan... hasta la válvula
            fase = ((t * 0.32 + k / 9.0) % 1.0)
            xx = -80 + fase * (W + 160)
            tope = 900 - 26 * k
            if cie > 0.5 and xx > tope - 40 and fase < 0.62:
                xx = tope - 40 - (k % 4) * 70
            if cie > 0.5 and xx > 980:
                continue
            K.chip(h, xx, y, 0.26, 200 + k * 20, brillo=0.6)
        gy = y - 60 + 120 * cie                                       # la compuerta baja
        h.pieza(C.rect(930, y - 180 - 0, 60, 120 + 120 * cie), 30, 60, w=6, luz=(0.2, -1), d=8, trama=0.4, rim=0.8)
        ang = cie * 6.0
        cxv, cyv = 960, y - 260                                       # volante de la válvula
        h.trazo(np.array([[960, y - 180], [960, cyv]]), 16, 61, color=(60, 60, 60), jit=0.3, taper=(0, 0))
        h.anillo(h.tf(np.asarray(elipse_(cxv, cyv, 120, 120, n=40))), 18, 62, color=(210, 210, 210), jit=0.4)
        for q in range(4):
            a = ang + q * math.pi / 2
            h.trazo(np.array([[cxv, cyv], [cxv + 112 * math.cos(a), cyv + 112 * math.sin(a)]]), 12, 63 + q, color=(200, 200, 200),
                    jit=0.3, taper=(0, 0))
        h.pieza(np.asarray(elipse_(cxv, cyv, 30, 30, n=20)), 60, 68, w=5, luz=(0.2, -1), d=6, trama=0.2, rim=0.9)
        C.banda(h, "EE. UU.", 300, 860, 90, t, self.t_eeuu + 0.4, claro=True, sem=5)
        C.banda(h, "CHINA", 1620, 860, 90, t, self.t_eeuu + 1.0, sem=6)
        C.banda(h, "ACIERTO N.º 3: SE CIERRA EL GRIFO DE LOS CHIPS", 960, 1000, 44, t, self.t_chips - 0.2, claro=True, sem=7)
        h.ambiente[:] = 0.42
        h.luz_radial(420, 520, 1000, (1.0, 1.0, 1.0), k=1.0)
        h.luz_radial(1560, 520, 900, (1.0, 1.0, 1.0), k=1.0 * (1 - 0.8 * cie))
        N.motas(h, t, n=90, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.16, vel=10, y0=200, y1=1080, sube=False), bloom=0.45)

    # ------------------------------------------------------------------ ciencia ficción -> el periódico de ayer
    def p_ayer(self, h, t, u):
        h.camara(1.0, W / 2, H / 2, 0.0)
        K.pared(h, 30, 10)
        zo = 1.0 + 0.04 * u
        T = K.hoja(h, 960, 540, 660, 900, ang=-0.06 + 0.01 * math.sin(t), sem=10, tono=150, s=zo)          # la revista pulp
        P = T([(0, -370)])[0]
        N.texto_maquina(h, "CIENCIA FICCIÓN", P[0], P[1], 74 * zo, t, -99, cps=1e9, tono=0.04, centro=True, fuente=K.IMPACT, encuadrar=False)
        P = T([(0, 300)])[0]
        K.plano_(h, T(C.rect(-290, -300, 580, 560)), 26, 12)
        K.robot(h, P[0], P[1] - 60 * zo, 0.86 * zo, t, 30, brazo=0.5 + 0.5 * math.sin(t * 2.0), tono=170)
        P = T([(0, 380)])[0]
        N.texto_maquina(h, "«¡LAS MÁQUINAS PENSANTES!»", P[0], P[1], 34 * zo, t, -99, cps=1e9, tono=0.05, centro=True, fuente=N.FUENTE_SELLO,
                        encuadrar=False)
        PR.periodico(h, t, self.t_hoy - 0.2, "LA GUERRA DE LOS CHIPS", "Washington corta el suministro a Pekín", cx=960, cy=560, dur=0.8, s=1.25,
                     sem=40, cabecera="EL DIARIO DE AYER")
        C.banda(h, "ENTONCES:", 300, 480, 50, t, self.t_aquel + 0.2, sem=5)
        C.banda(h, "HOY:", 300, 480, 80, t, self.t_hoy, claro=True, sem=6)
        h.ambiente[:] = 0.42
        h.luz_cono(960, -620, math.pi / 2, 0.5, 2300, (1.6, 1.6, 1.6), suave=0.5)
        g = pulso(t, self.t_hoy + 0.6, 0.3, 1.0)
        N.motas(h, t, n=100, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.14, vel=8, y0=0, y1=1080, sube=False), bloom=0.45, flash=0.2 * g)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        t0 = self.t0
        self.ev(self.t_agosto - 0.2, "papel_arranca", 0.9, -0.4)
        self.ev(self.t_faltaba, "hilo_tenso", 0.6, 0.2)
        self.ev(self.t_faltaba + 0.7, "sello_golpe", 0.8, 0.2)
        self.ev(self.t_chat, "sello_golpe", 0.9, 0.5)
        self.ev(self.t_publico - 0.35, "barrido_aire", 0.6, 0.0, dur=0.7)
        self.ev(self.t_publico + 0.5, "tecleo_rapido", 0.6, 0.0, dur=1.8)
        self.ev(self.t_como, "tecleo_rapido", 0.5, 0.0, dur=3.0)
        self.ev(self.t_desc - 0.3, "barrido_aire", 0.6, 0.0, dur=0.6)
        for k in range(5):
            self.ev(self.t_paso - 0.9 + k * 0.44, "interruptor", 0.6, -0.4 + 0.2 * k, tono=1.0 + 0.08 * k)
        self.ev(self.t_entren - 0.3, "barrido_aire", 0.6, 0.0, dur=0.6)
        self.ev(self.t_entren, "fichas_empuja", 0.7, 0.0)
        self.ev(self.t_fort, "caja_registradora", 0.8, -0.3)
        self.ev(self.t_eeuu - 0.3, "barrido_aire", 0.6, 0.0, dur=0.6)
        self.ev(self.t_cerr, "engranajes", 0.8, 0.0, dur=0.9)
        self.ev(self.t_cerr + 0.7, "golpe_grave", 0.9, 0.0)
        self.ev(self.t_aquel - 0.35, "paginas", 0.6, 0.0)
        self.ev(self.t_hoy - 0.2, "periodico_gira", 0.9, 0.0, dur=0.8)
        self.ev(self.t_hoy + 0.6, "periodico_golpe", 1.0, 0.0)
        self.ev(self.t1 - 0.8, "tinta_mancha", 0.6, 0.0, dur=0.9)
