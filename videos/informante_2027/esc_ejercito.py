# -*- coding: utf-8 -*-
"""Escena 10 «ejercito»: una mano sube la palanca y, bajo el foco, no hay nadie en la silla: se enciende la caja; la cámara se
aleja y las copias se encienden en oleadas hasta llenar la nave (200 000); los humanos, de espaldas, miran un muro de pantallas
que corre demasiado rápido; doce hojas de calendario se pliegan en una sola: «1 SEMANA»."""
import math

import numpy as np

import comun as C
import kit27 as K
import mundos27 as M27
import noir as N
import props as PR
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from toon import Pista, elipse_, pulso

MESES = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"]


class Ejercito(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_marzo = w("Marzo")
        self.t_enc = w("enciende")
        self.t_prog = w("programador")
        self.t_noes = w("No es")
        self.t_son = w("Son doscientas")
        self.t_copias = w("copias")
        self.t_equiv = w("El equivalente")
        self.t_cinc = w("cincuenta mil")
        self.t_treinta = w("treinta")
        self.t_humanos = w("Los humanos")
        self.t_noesc = w("ya no")
        self.t_miran = w("Miran")
        self.t_dorm = w("dormían")
        self.t_anio = w("Un año")
        self.t_caber = w("caber")
        self.t_semana = w("semana")
        self.cam_c = Pista([(self.t_son - 0.5, (960, 520, 2.6)), (self.t_copias + 0.3, (960, 520, 1.5), "io"),
                            (self.t_humanos, (960, 520, 0.92), "io")])
        self.plano(t0, self.p_enciende)
        self.plano(self.t_son - 0.35, self.p_copias, tr="empuje", dur=0.6, centro=(W * 0.5, H * 0.5))
        self.plano(self.t_humanos - 0.35, self.p_humanos, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_anio - 0.35, self.p_semana, tr="humo", dur=0.6)

    # ------------------------------------------------------------------ enciende a su mejor programador
    def p_enciende(self, h, t, u):
        h.camara(1.0 + 0.014 * u, 960 + 6 * u, 540, 0.0)
        K.pared(h, 40, 12, paneles=10)
        K.plano_(h, C.rect(-300, 930, W + 600, 400), 40, 8, grad=(10, 930, 1200))
        on = smooth(clamp01((t - self.t_enc) / 0.35))
        tip = K.interruptor(h, 400, 520, 1.0, pos=1.0 - on, sem=20, t=t)
        ac = smooth(clamp01((t - self.t_enc + 0.9) / 0.6)) * (1 - smooth(clamp01((t - self.t_enc - 0.6) / 0.6)))
        PR.mano(h, tip[0] - 60 - 500 * (1 - ac), tip[1] + 10, 1.25, ang=0.0, d=1, sem=40, dedos=0.2)
        PR.silla(h, 1160, 940, s=1.7, d=1, tono=64, sem=60)             # la silla vacía del «mejor programador»
        C.teclado(h, 1250, 720, 420, sem=70)
        PR.mesa(h, 1420, 760, ancho=760, fondo=110, alto=180, tono=60, sem=80)
        led = smooth(clamp01((t - self.t_noes) / 0.4))
        tl = PR.caja_negra(h, 1620, 660, 0.72, led, t, sem=100, cable=False)
        C.banda(h, "MARZO DE 2027", 420, 110, 64, t, self.t_marzo, sem=5)
        C.banda(h, "SU MEJOR PROGRAMADOR", 1300, 150, 54, t, self.t_prog - 0.4, claro=True, sem=6)
        C.banda(h, "NO ES UNA PERSONA", 1300, 250, 66, t, self.t_noes + 0.2, sem=7)
        h.ambiente[:] = 0.3 + 0.16 * on
        h.luz_radial(400, 520, 520, (1.0, 1.0, 1.0), k=1.0)
        h.luz_cono(1300, -400, math.pi / 2, 0.42, 1800, (1.6, 1.6, 1.6), k=1.2 * on, suave=0.5)
        h.luz_radial(tl[0], tl[1], 460, (1.0, 1.0, 1.0), k=1.3 * led)
        N.motas(h, t, n=100, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.2, vel=10, y0=-200, y1=1000, sube=False), bloom=0.5)

    # ------------------------------------------------------------------ 200 000 copias
    def p_copias(self, h, t, u):
        cx, cy, z = self.cam_c(t)
        h.camara(z, cx, cy, 0.0)
        K.plano_(h, C.rect(-600, -400, W + 1200, H + 800), 96, 5, grad=(40, 0, H))
        cols, filas = 27, 8
        # oleada desde el centro
        t_ini = self.t_son - 0.3
        for j in range(filas):
            for i in range(cols):
                d = math.hypot(i - cols // 2, (j - filas // 2) * 1.6)
                tk = t_ini + d * 0.13
                if t < tk:
                    continue
                a = clamp01((t - tk) / 0.25)
                x, y = 960 + (i - cols // 2) * 78, 520 + (j - filas // 2) * 150 + 70
                h.pieza(C.rect(x - 26, y - 118, 52, 118), 46, 100 + (i * 31 + j * 7) % 800, w=2.5, luz=(0.3, -1), d=6, trama=0.3, rim=0.9,
                        rim_tono=200, alfa=a, jit=0.5)
                v = a * (0.45 + 0.55 * math.sin(t * 3.3 + i * 1.3 + j * 2.1) ** 2)
                h.emitir(elipse_(x + 16, y - 108, 3.2, 3.2, n=8), 1.3 * v, blur=1.4)
        h.camara(1.0, W / 2, H / 2, 0.0)
        C.banda(h, "200 000 COPIAS", 960, 130, 110, t, self.t_copias - 0.5, sem=5)
        C.banda(h, "= 50 000 DE LOS MEJORES INGENIEROS", 960, 920, 54, t, self.t_cinc - 0.2, claro=True, sem=6)
        C.banda(h, "× 30 DE VELOCIDAD", 960, 1010, 54, t, self.t_treinta, sem=7)
        h.ambiente[:] = 0.8
        h.luz_radial(960, 540, 1500, (1.0, 1.0, 1.0), k=0.9)
        N.motas(h, t, n=80, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.14, vel=12, y0=0, y1=1080, sube=False), bloom=0.6)

    # ------------------------------------------------------------------ los humanos ya solo miran
    def p_humanos(self, h, t, u):
        h.camara(1.0 + 0.012 * u, 960, 520 + 4 * u, 0.0)
        K.pared(h, 22, 6)
        for j in range(2):                                           # el muro de pantallas (el código corre demasiado rápido)
            for i in range(5):
                x, y = 90 + i * 356, 60 + j * 300
                h.pieza(C.rect(x - 10, y - 10, 336, 280), 18, 20 + i + j * 5, w=5, luz=(0, -1), d=6, trama=0.2, rim=0.6)
                K.pantalla_codigo(h, (x, y, 316, 260), t, sem=200 + i * 13 + j * 71, vel=7.0 + 2 * i + 3 * j, filas=11)
        C.luz_rect(h, C.rect(80, 50, 1770, 580), 0.8, suave_=18)
        for k in range(3):                                           # tres ingenieros de espaldas, hundidos en la silla
            x = 430 + k * 530
            cab = 0.5 * math.sin(t * 0.5 + k * 2.0)
            if k == 1 and t > self.t_dorm - 0.8:                     # el del medio cabecea
                cab = 0.9 * math.sin((t - self.t_dorm) * 1.5)
            C.espalda(h, x, 880, 0.9, sem=300 + k * 40, luz=(0.0, -1.0), gira=cab, hombros=0.0)
            h.luz_radial(x, 760, 420, (1.0, 1.0, 1.0), k=1.1)
        N.texto_maquina(h, "ESCRITO POR HUMANOS HOY: 0 LÍNEAS", 960, 640, 40, t, self.t_noesc, cps=30, tono=0.95, centro=True,
                        encuadrar=False)
        C.banda(h, "YA NO ESCRIBEN", 420, 1010, 60, t, self.t_noesc, sem=5)
        C.banda(h, "MIRAN", 960, 1010, 80, t, self.t_miran, claro=True, sem=6)
        C.banda(h, "¿QUÉ PASÓ MIENTRAS DORMÍAN?", 1480, 1010, 40, t, self.t_dorm - 1.2, sem=7)
        h.ambiente[:] = 0.42
        N.motas(h, t, n=80, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.14, vel=10, y0=0, y1=1080, sube=False), bloom=0.55)

    # ------------------------------------------------------------------ un año en una semana
    def p_semana(self, h, t, u):
        h.camara(1.0 + 0.02 * u, 960, 540, 0.0)
        K.pared(h, 50, 18, ladrillo=True)
        jun = smooth(clamp01((t - self.t_caber + 0.5) / 1.2))        # las doce hojas se pliegan en una
        for k in range(12):
            x0, y0 = 250 + (k % 6) * 284, 330 + (k // 6) * 400
            x = x0 + (960 - x0) * jun
            y = y0 + (560 - y0) * jun
            s = 1.0 - 0.15 * jun
            a = 0.05 * math.sin(k * 2.3) * (1 - jun) + jun * (k - 5.5) * 0.02
            c = np.array([x, y])
            h.pieza(PR.rot(C.rect(x - 120 * s, y - 150 * s, 240 * s, 300 * s), a, c), 226, 100 + k, w=4, luz=(0.2, -1), d=8, trama=0, rim=0)
            K.plano_(h, PR.rot(C.rect(x - 120 * s, y - 150 * s, 240 * s, 70 * s), a, c), 40, 120 + k)
            if jun < 0.6:
                N.texto_maquina(h, MESES[k], x, y + 30, 96, t, -99, cps=1e9, tono=0.04, centro=True, fuente=N.FUENTE_SELLO, encuadrar=False,
                                alfa=1 - jun / 0.6)
        if jun > 0.9:
            k_ = 1.0 + 0.3 * (1 - clamp01((t - self.t_caber - 0.6) / 0.15)) ** 2
            h.pieza(C.rect(960 - 190 * k_, 560 - 230 * k_, 380 * k_, 460 * k_), 230, 150, w=5, luz=(0.2, -1), d=10, trama=0, rim=0)
            K.plano_(h, C.rect(960 - 190 * k_, 560 - 230 * k_, 380 * k_, 110 * k_), 20, 151)
            N.texto_maquina(h, "2027", 960, 560 - 176 * k_, 70 * k_, t, -99, cps=1e9, tono=0.96, centro=True, fuente=N.FUENTE_SELLO,
                            encuadrar=False)
            N.texto_maquina(h, "1", 960, 560 - 10 * k_, 230 * k_, t, -99, cps=1e9, tono=0.04, centro=True, fuente=K.IMPACT, encuadrar=False)
            N.texto_maquina(h, "SEMANA", 960, 560 + 160 * k_, 76 * k_, t, -99, cps=1e9, tono=0.06, centro=True, fuente=N.FUENTE_SELLO,
                            encuadrar=False)
        C.banda(h, "UN AÑO DE DESCUBRIMIENTOS", 960, 80, 60, t, self.t_anio + 0.1, sem=5)
        C.banda(h, "CABE EN UNA SEMANA", 960, 1010, 70, t, self.t_semana - 0.3, claro=True, sem=6)
        g = pulso(t, self.t_caber + 0.7, 0.3, 1.0)
        h.ambiente[:] = 0.52
        h.luz_radial(960, 540, 1300, (1.0, 1.0, 1.0), k=0.8 + g)
        N.motas(h, t, n=90, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.14, vel=10, y0=200, y1=1080, sube=False), bloom=0.45, flash=0.2 * g)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        t0 = self.t0
        self.ev(self.t_marzo, "sello_golpe", 0.8, -0.3)
        self.ev(self.t_enc, "interruptor", 1.0, -0.4)
        self.ev(self.t_enc + 0.1, "focos", 0.9, 0.2)
        self.ev(self.t_noes, "electricidad", 0.6, 0.4, dur=1.0)
        self.ev(self.t_noes + 0.2, "golpe_grave", 0.9, 0.0)
        self.ev(self.t_son - 0.35, "barrido_aire", 0.6, 0.0, dur=0.7)
        self.ev(self.t_son - 0.3, "crecer", 0.8, 0.0, dur=3.0)
        self.ev(self.t_son, "zumbido_servidores", 0.8, 0.0, dur=self.t_humanos - self.t_son)
        self.ev(self.t_copias - 0.5, "sello_golpe", 1.0, 0.0)
        self.ev(self.t_cinc - 0.2, "sello_golpe", 0.8, 0.0)
        self.ev(self.t_treinta, "sello_golpe", 0.9, 0.0)
        self.ev(self.t_humanos - 0.35, "barrido_aire", 0.6, 0.0, dur=0.7)
        self.ev(self.t_humanos, "datos", 0.6, 0.0, dur=self.t_anio - self.t_humanos)
        self.ev(self.t_miran, "sello_golpe", 0.8, 0.0)
        self.ev(self.t_anio - 0.35, "paginas", 0.7, 0.0)
        self.ev(self.t_caber - 0.5, "papel_viento", 0.8, 0.0, dur=1.2)
        self.ev(self.t_caber + 0.7, "sello_golpe", 1.0, 0.0)
        self.ev(self.t_caber + 0.7, "golpe_grave", 0.9, 0.0)
        self.ev(self.t1 - 0.8, "tinta_mancha", 0.6, 0.0, dur=0.9)
