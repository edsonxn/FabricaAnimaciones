# -*- coding: utf-8 -*-
"""Escena 14 «voto»: las dos opciones (la palanca de FRENAR y el velocímetro de SEGUIR) y diez manos que suben por el borde;
si frenan: el auto rival los adelanta bajo la lluvia; si corren: la mano que busca la palanca y ya no la alcanza; el comité
vota (seis manos arriba) y el marcador «6 — 4»; el expediente se rasga en dos caminos."""
import math

import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import noir as N
import props as PR
import props5 as PR5
from basen import BaseNoir
from comite import Comite
from motor import H, W, clamp01, e_out, smooth
from toon import elipse_, pulso


class Voto(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.com = Comite()
        self.t_diez = w("Diez manos")
        self.t_dos = w("Dos opciones")
        self.t_frenar = w("Frenar")
        self.t_seguir = w("seguir")
        self.t_sifren = w("Si frenan")
        self.t_alcanza = w("alcanza")
        self.t_sicorr = w("Si corren")
        self.t_nadie = w("nadie")
        self.t_interr = w("interruptor")
        self.t_result = w("El resultado")
        self.t_seis = w("seis")
        self.t_cuatro = w("cuatro")
        self.t_aqui = w("Aquí")
        self.t_parte = w("parte")
        self.t_porque = w("Porque")
        self.t_finales = w("finales")
        self.plano(t0, self.p_opciones)
        self.plano(self.t_sifren - 0.35, self.p_frenan, tr="barrido", dur=0.55, dirx=1)
        self.plano(self.t_sicorr - 0.3, self.p_mano, tr="barrido", dur=0.5, dirx=-1)
        self.plano(self.t_result - 0.35, self.p_conteo, tr="humo", dur=0.6)
        self.plano(self.t_aqui - 0.35, self.p_rasga, tr="empuje", dur=0.55, centro=(W * 0.5, H * 0.5))

    # ------------------------------------------------------------------ diez manos, dos opciones
    def p_opciones(self, h, t, u):
        h.camara(1.0 + 0.012 * u, 960, 540, 0.0)
        K.pared(h, 44, 14, paneles=10)
        h.trazo(np.array([[960, -100], [960, 800]]), 6, 20, color=(200, 200, 200), alfa=0.5, jit=0.4, taper=(0, 0))
        e1 = smooth(clamp01((t - self.t_frenar + 0.3) / 0.4))
        e2 = smooth(clamp01((t - self.t_seguir + 0.3) / 0.4))
        K.interruptor(h, 480, 400, 0.72, pos=0.5 + 0.5 * math.sin(t * 1.2) * 0.2, sem=30, t=t)
        PR5.velocimetro(h, 1440, 400, 250, 0.6 + 0.25 * math.sin(t * 2.0) ** 2, t, sem=60)
        C.banda(h, "DOS OPCIONES", 960, 70, 60, t, self.t_dos, sem=5)
        C.banda(h, "FRENAR Y REVISAR", 480, 690, 56, t, self.t_frenar - 0.2, claro=True, sem=6)
        C.banda(h, "SEGUIR CORRIENDO", 1440, 690, 56, t, self.t_seguir - 0.2, claro=True, sem=7)
        for k in range(10):                                          # diez manos que suben por el borde
            tk = self.t_diez - 0.2 + k * 0.09
            K.mano_alzada(h, 130 + k * 185, 830 + 30 * math.sin(k * 2.3), 0.55, clamp01((t - tk) / 0.4), sem=100 + k * 14,
                          manga=34 + 14 * (k % 4), bal=4 * math.sin(t * 2.2 + k), d=1 if k % 2 else -1)
        h.ambiente[:] = 0.36
        h.luz_cono(480, -420, math.pi / 2, 0.3, 1700, (1.5, 1.5, 1.5), k=0.4 + 0.6 * e1, suave=0.5)
        h.luz_cono(1440, -420, math.pi / 2, 0.3, 1700, (1.5, 1.5, 1.5), k=0.4 + 0.6 * e2, suave=0.5)
        h.luz_radial(960, 1000, 1300, (1.0, 1.0, 1.0), k=0.8)
        N.motas(h, t, n=100, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.16, vel=10, y0=-200, y1=1000, sube=False), bloom=0.45)

    # ------------------------------------------------------------------ si frenan, el rival los alcanza
    def p_frenan(self, h, t, u):
        cx = 3300 + 60 * u
        h.camara(0.9, cx, 660, 0.0)
        MU.cielo().pegar(h, 0.05, dx=-(t * 6.0) % 300)
        MU.lejos().pegar(h, 0.3, bruma=0.55, tono_bruma=0.36)
        MU.medio().pegar(h, 0.6, bruma=0.2, tono_bruma=0.36)
        MU.calle().pegar(h, 1.0)
        fre = smooth(clamp01((t - self.t_sifren) / 0.8))
        PR5.auto(h, 3050 + 120 * fre, 1100, 1.3, t, vel=3.0 * (1 - fre), sem=40, tono=30, bandera="franjas", faros=1.0)
        xr = 2300 + (t - self.t_sifren + 0.4) * 620                   # el rival pasa de largo
        PR5.auto(h, xr, 1210, 1.5, t, vel=3.2, sem=80, tono=46, bandera="estrella")
        h.luz_cono(xr + 280, 1170, 0.0, 0.2, 800, (1.5, 1.5, 1.5), k=1.0, suave=0.6)
        h.emitir(C.rect(3050 + 120 * fre - 250, 1010, 22, 30), 1.2 * fre)                 # luces de freno
        h.ambiente[:] = 1.0
        N.lluvia(h, t, n=600, vel=1800, viento=0.3)
        h.camara(1.0, W / 2, H / 2, 0.0)
        C.banda(h, "SI FRENAN...", 420, 120, 70, t, self.t_sifren, sem=5)
        C.banda(h, "EL RIVAL LOS ALCANZA", 1380, 150, 64, t, self.t_alcanza - 0.5, claro=True, sem=6)
        return h.acabado(t, niebla=dict(dens=0.22, y0=300, y1=1080, vel=40), bloom=0.5)

    # ------------------------------------------------------------------ si corren, nadie tendrá la mano en el interruptor
    def p_mano(self, h, t, u):
        h.camara(1.0 + 0.014 * u, 960, 540, 0.0)
        K.pared(h, 30, 8)
        ale = smooth(clamp01((t - self.t_nadie + 0.4) / max(1.2, self.t_interr - self.t_nadie + 0.8)))
        sc = 1.0 - 0.72 * ale                                        # la palanca se aleja al fondo de un pasillo
        for q in range(7):                                           # marcos del pasillo
            z = 1.0 - q * 0.13
            h.anillo(h.tf(C.rect(1360 - 420 * z, 500 - 460 * z, 840 * z, 920 * z)), 5 * h.zoom, 20 + q, color=(120, 120, 120),
                     alfa=0.25 + 0.5 * ale * (q / 7), jit=0.5)
        tip = K.interruptor(h, 1360, 500, 0.9 * sc, pos=0.0, sem=40, t=t)
        mx = 300 + 420 * smooth(clamp01((t - self.t_sicorr) / 0.9)) + 20 * math.sin(t * 7)
        PR.mano(h, mx, 560, 1.7, ang=-0.05, d=1, sem=80, dedos=0.8 + 0.2 * math.sin(t * 5))
        C.banda(h, "SI CORREN...", 420, 110, 70, t, self.t_sicorr, sem=5)
        C.banda(h, "QUIZÁ NADIE VUELVA A ALCANZAR EL INTERRUPTOR", 960, 1010, 46, t, self.t_nadie - 0.2, claro=True, sem=6)
        h.ambiente[:] = 0.34
        h.luz_radial(1360, 500, 700 * sc + 200, (1.0, 1.0, 1.0), k=1.4 * (1 - 0.6 * ale))
        h.luz_radial(mx, 560, 600, (1.0, 1.0, 1.0), k=1.0)
        N.motas(h, t, n=100, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.18, vel=10, y0=0, y1=1080, sube=False), bloom=0.5)

    # ------------------------------------------------------------------ seis contra cuatro
    def p_conteo(self, h, t, u):
        h.camara(1.0 + 0.012 * u, 960, 520, 0.0)
        orden = [1, 6, 3, 8, 0, 9]                                   # los seis que levantan la mano
        alza = [0.0] * 10
        for q, k in enumerate(orden):
            alza[k] = clamp01((t - (self.t_result - 0.1 + q * 0.28)) / 0.4)
        self.com.dibujar(h, t, alza=alza, lamparas=1.0)
        C.banda(h, "6", 700, 100, 130, t, self.t_seis - 0.1, claro=True, sem=5)
        C.banda(h, "CONTRA", 960, 100, 50, t, self.t_seis + 0.3, sem=6)
        C.banda(h, "4", 1220, 100, 130, t, self.t_cuatro - 0.1, sem=7)
        g = pulso(t, self.t_cuatro, 0.3, 1.0)
        h.ambiente[:] = 0.34
        N.motas(h, t, n=100, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.18, vel=8, y0=-200, y1=1000, sube=False), bloom=0.45, flash=0.2 * g)

    # ------------------------------------------------------------------ el expediente se parte en dos
    def p_rasga(self, h, t, u):
        h.camara(1.0 + 0.014 * u, 960, 540, 0.0)
        MU.escritorio().pegar(h, 1.0, oscuro=0.7, dx=40, dy=-60)
        ab = e_out(clamp01((t - self.t_parte + 0.2) / 0.7))
        r = np.random.default_rng(4)
        zig = [(r.uniform(-18, 18), -330 + k * 66) for k in range(11)]
        for lado in (-1, 1):
            dx = lado * 330 * ab
            ang = lado * 0.16 * ab
            c = np.array([960 + dx, 560])
            if lado < 0:
                P = [(-430, -330), (zig[0][0], -330)] + zig + [(zig[-1][0], 330), (-430, 330)]
            else:
                P = [(zig[0][0], -330)] + [(430, -330), (430, 330), (zig[-1][0], 330)] + zig[::-1]
            Q = PR.rot(np.array(P, float) + c, ang, c)
            h.pieza(Q, 120, 20 + lado, w=6, luz=(0.25, -1), d=16, trama=0.5, rim=0.7)
            tc = PR.rot(np.array([[lado * 215, -60]], float) + c, ang, c)[0]
            N.texto_maquina(h, "20" if lado < 0 else "27", tc[0], tc[1], 250, t, -99, cps=1e9, tono=0.04, centro=True, fuente=K.IMPACT,
                            track=4.0, encuadrar=False)
            if ab > 0.6:
                N.texto_maquina(h, "FINAL 1" if lado < 0 else "FINAL 2", tc[0], tc[1] + 220, 70, t, self.t_porque, cps=1e9, tono=0.05,
                                centro=True, fuente=N.FUENTE_SELLO, encuadrar=False)
        C.banda(h, "EL EXPEDIENTE SE PARTE EN DOS", 960, 90, 56, t, self.t_parte - 0.3, sem=5)
        C.banda(h, "LA CARRERA", 420, 1000, 70, t, self.t_finales - 0.6, claro=True, sem=6)
        C.banda(h, "EL FRENO", 1500, 1000, 70, t, self.t_finales - 0.3, claro=True, sem=7)
        h.ambiente[:] = 0.34
        h.luz_cono(960, -620, math.pi / 2, 0.6, 2400, (1.6, 1.6, 1.6), suave=0.5)
        N.motas(h, t, n=100, k=0.7)
        return h.acabado(t, niebla=None, bloom=0.4)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        t0 = self.t0
        self.ev(t0, "zumbido_lampara", 0.4, 0.0, dur=self.t_sifren - t0)
        for k in range(0, 10, 2):
            self.ev(self.t_diez - 0.2 + k * 0.09, "papel_atrapa", 0.4, -0.8 + 0.18 * k)
        self.ev(self.t_frenar - 0.2, "interruptor", 0.8, -0.5)
        self.ev(self.t_seguir - 0.2, "motor_acelera", 0.6, 0.5, dur=1.5)
        self.ev(self.t_sifren - 0.35, "lluvia_amb", 0.7, 0.0, dur=self.t_sicorr - self.t_sifren + 0.3)
        self.ev(self.t_sifren, "auto_pasa", 0.9, 0.0, dur=3.0)
        self.ev(self.t_alcanza - 0.5, "sello_golpe", 0.9, 0.3)
        self.ev(self.t_sicorr - 0.3, "barrido_aire", 0.6, 0.0, dur=0.6)
        self.ev(self.t_nadie - 0.4, "caida", 0.7, 0.3)
        self.ev(self.t_nadie - 0.2, "grave_inquietante", 0.7, 0.0, dur=2.5)
        for q in range(6):
            self.ev(self.t_result - 0.1 + q * 0.28, "papel_atrapa", 0.5, -0.6 + 0.24 * q)
        self.ev(self.t_seis - 0.1, "sello_golpe", 1.0, -0.3)
        self.ev(self.t_cuatro - 0.1, "sello_golpe", 1.0, 0.3)
        self.ev(self.t_cuatro, "golpe_grave", 1.0, 0.0)
        self.ev(self.t_parte - 0.2, "papel_arranca", 1.0, 0.0)
        self.ev(self.t_finales - 0.6, "sello_golpe", 0.8, -0.4)
        self.ev(self.t_finales - 0.3, "sello_golpe", 0.8, 0.4)
        self.ev(self.t1 - 0.8, "tinta_mancha", 0.6, 0.0, dur=0.9)
