# -*- coding: utf-8 -*-
"""Escena 5 «descubre»: el empleado, de frente, con el auricular (la llamada viaja por el cable); al otro lado el director de
verdad, que no entiende nada (signos de interrogación); la sala de juntas vacía bajo la lámpara que se balancea (no hubo
transacción, no hubo reunión, él jamás estuvo); la hoja del calendario «29 ENE 2024», el farol de la policía y la caja fuerte
abierta y vacía."""
import math

import numpy as np

import comun as C
import mundos as MU
import noir as N
import props as PR
from basen import BaseNoir
from esc_dinero import tache
from motor import H, W, clamp01, e_out, smooth
from noir_pers import Frontal
from toon import Pista, elipse_, pulso, suave


def auricular(h, x, y, s, sem, ang=0.0):
    """Auricular de teléfono de mesa junto a la oreja."""
    P = [(-24, -120), (24, -120), (30, -70), (16, -40), (16, 40), (30, 70), (24, 120), (-24, 120), (-34, 70), (-14, 40), (-14, -40),
         (-34, -70)]
    h.pieza(PR.rot(np.array(suave(P, 3)) * s + (x, y), ang, np.array([x, y])), 22, sem, w=5 * s, luz=(0.3, -1), d=8 * s, trama=0.4, rim=0.8)


class Descubre(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.emp = Frontal(sem=210)
        self.jefe = Frontal(sem=40)
        self.t_llamo = w("llamó")
        self.t_central = w("central")
        self.t_bien = w("bien", fin=True)
        self.t_otro = w("Al otro")
        self.t_nadie = w("nadie", frase=1)
        self.t_hablando = w("hablando", fin=True)
        self.t_nohabia = w("No había transacción")
        self.t_noreu = w("No había reunión")
        self.t_eldir = w("El director")
        self.t_jamas = w("jamás")
        self.t_veinti = w("El veintinueve")
        self.t_policia = w("policía")
        self.t_para = w("Para entonces")
        self.t_noestaba = w("no estaba")
        self.plano(t0, self.p_llama)
        self.plano(self.t_otro - 0.35, self.p_otro, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_nohabia - 0.35, self.p_sala, tr="humo", dur=0.7)
        self.plano(self.t_veinti - 0.35, self.p_fecha, tr="barrido", dur=0.55, dirx=-1)
        self.plano(self.t_para - 0.3, self.p_caja, tr="empuje", dur=0.6, centro=(W * 0.5, H * 0.5))

    def _cable(self, h, t, x0, y0, x1, y1, sem, dirx=1):
        """Cable de teléfono rizado con pulsos que viajan (la llamada)."""
        n = 90
        xs = np.linspace(x0, x1, n)
        ys = np.linspace(y0, y1, n) + 120 * np.sin(np.linspace(0, math.pi, n)) + 12 * np.sin(np.arange(n) * 0.9)
        h.trazo(np.stack([xs, ys], 1), 6, sem, color=(200, 200, 200), jit=0.3, taper=(0, 0))
        for q in range(4):
            a = ((t * 0.9 + q * 0.25) % 1.0)
            a = a if dirx > 0 else 1 - a
            i = int(a * (n - 1))
            h.luz_radial(xs[i], ys[i], 120, (1.0, 1.0, 1.0), k=1.6)
            h.pieza(elipse_(xs[i], ys[i], 13, 13, n=12), 240, sem + 1 + q, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False)

    # ------------------------------------------------------------------ llama a la central
    def p_llama(self, h, t, u):
        h.camara(1.0 + 0.03 * u, 960 + 10 * u, 540, 0.0)
        C.oficina_hk().pegar(h, 0.5, oscuro=1.0, dx=-8 * u + 300)
        s = 2.4
        sube = e_out(clamp01((t - self.t_llamo + 0.5) / 0.5))
        p = dict(x=560, y=480 + 474 * s, s=s, luz=(0.9, -0.4), rim=0.9, pelo="oscuro", traje=150, mira=0.6, cabeza=0.25)
        self.emp.dibujar(h, p)
        ax, ay = 560 + 118 * s * 0.42, 480 + 20 + 500 * (1 - sube)
        auricular(h, ax, ay, 1.5, 60, ang=0.12)
        self._cable(h, t, ax + 10, ay + 170, W + 80, 760, 70)
        C.banda(h, "LLAMANDO A LA OFICINA CENTRAL...", 1330, 250, 44, t, self.t_llamo, sem=4)
        C.banda(h, "«¿SALIÓ TODO BIEN?»", 1330, 390, 66, t, self.t_bien - 1.2, claro=True, sem=5)
        h.ambiente[:] = 0.62
        C.luz_rect(h, C.rect(-200, 40, W + 400, 330), 1.8, suave_=10)       # la mañana entra por el ventanal
        h.luz_radial(1100, 600, 1300, (1.0, 1.0, 1.0), k=0.6)
        N.motas(h, t, n=70, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.14, vel=8, y0=0, y1=900, sube=False))

    # ------------------------------------------------------------------ al otro lado, nadie sabe nada
    def p_otro(self, h, t, u):
        h.camara(1.0 + 0.03 * u, 1020 - 10 * u, 300, 0.0)
        MU.oficina().pegar(h, 1.0)
        s = 2.3
        enc = smooth(clamp01((t - self.t_nadie) / 0.4))
        p = dict(x=1010, y=250 + 474 * s, s=s, luz=(0.9, -0.5), rim=0.9, pelo="blanco", traje=92, gafas=True,
                 mira=0.7 * math.sin(t * 2.2), cabeza=0.5 * math.sin(t * 1.6) * enc)
        self.jefe.dibujar(h, p)
        auricular(h, 1010 - 118 * s * 0.42, 270, 1.45, 60, ang=-0.12)
        self._cable(h, t, 60, 500, 1010 - 130, 440, 70, dirx=1)
        for q in range(5):                                         # signos de interrogación que brotan
            tk = self.t_nadie + 0.3 * q
            a = clamp01((t - tk) / 0.3)
            if a <= 0:
                continue
            N.texto_maquina(h, "?", 1330 + 110 * (q % 3) + 30 * math.sin(q * 5), 60 - 70 * (q // 3) + 110 * (q % 2) - 40 * a, 150 + 30 * (q % 2), t,
                            -99, cps=1e9, tono=0.96, centro=True, fuente="C:/Windows/Fonts/impact.ttf", encuadrar=False)
        C.banda(h, "«¿QUÉ TRANSFERENCIAS?»", 560, 30, 60, t, self.t_hablando - 1.4, claro=True, sem=6)
        h.ambiente[:] = 0.34
        h.luz_persiana(np.array([[60, -420], [1080, -470], [1080, 640], [-80, 900]]), k=1.2, n=15, abierto=0.5)
        h.luz_radial(1150, 150, 900, (1.0, 1.0, 1.0), k=1.2)
        N.motas(h, t, n=80, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.14, vel=8, y0=-300, y1=900, sube=False))

    # ------------------------------------------------------------------ la sala vacía
    def p_sala(self, h, t, u):
        h.camara(1.0 + 0.02 * u, 960, 500 - 6 * u, 0.0)
        MU.sala_interrogatorio().pegar(h, 1.0, oscuro=0.9)
        sw = 0.22 * math.sin(t * 1.4)
        PR.lampara_colgante(h, 960, -700, largo=640, ang=sw, k=1.25, sem=20, abre=0.62, alcance=1700)
        PR.mesa(h, 960, 960, ancho=1500, fondo=170, alto=300, tono=84, sem=30)
        for k, (x, d) in enumerate(((330, 1), (700, 1), (1220, -1), (1590, -1))):
            PR.silla(h, x, 960, s=1.45, d=d, tono=70, sem=40 + 3 * k)
        # la silla del «director», en la cabecera, bajo la luz: nadie
        h.pieza(C.rect(850, 230, 220, 470), 46, 60, w=7, luz=(0, -1), d=16, trama=0.6, rim=0.8)        # sillón de respaldo alto, vacío
        for q in range(3):
            h.trazo(np.array([[880, 300 + q * 120], [1040, 300 + q * 120]]), 4, 61 + q, alfa=0.5, jit=0.4)
        for sx in (-1, 1):
            h.pieza(C.rect(960 + sx * 130 - 22, 520, 44, 190), 40, 65 + sx, w=5, luz=(0, -1), d=8, trama=0.4, rim=0.7)
        x0 = 440
        for k, (s_, tk) in enumerate((("TRANSACCIÓN SECRETA", self.t_nohabia), ("REUNIÓN", self.t_noreu))):
            if t < tk - 0.1:
                continue
            yy = 80 + 130 * k
            C.banda(h, s_, x0, yy, 60, t, tk - 0.1, claro=True, sem=7 + k)
            a = clamp01((t - tk - 0.25) / 0.3)
            if a > 0:
                im_w = 60 * 0.62 * len(s_)
                h.trazo(np.array([[x0 - im_w / 2 - 30, yy + 4], [x0 - im_w / 2 - 30 + (im_w + 60) * a, yy - 4]]), 14, 80 + k, color=(12, 12, 12),
                        jit=0.6, taper=(0.1, 0.1))
        C.banda(h, "JAMÁS ESTUVO AHÍ", 960, 190, 78, t, self.t_jamas, sem=9)
        h.ambiente[:] = 0.34
        N.motas(h, t, n=110, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.2, vel=10, y0=-300, y1=900, sube=False))

    # ------------------------------------------------------------------ 29 de enero: la policía
    def p_fecha(self, h, t, u):
        h.camara(1.0 + 0.025 * u, 960, 540, 0.0)
        h.pieza(C.rect(-100, -100, W + 200, H + 200), 56, 5, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False, grad=(22, 0, H))
        for k in range(9):                                         # ladrillo de la comisaría
            for j in range(13):
                xx = -80 + j * 170 + (85 if k % 2 else 0)
                h.anillo(h.tf(C.rect(xx, 20 + k * 120, 164, 114)), 2.5 * h.zoom, 100 + k * 13 + j, alfa=0.35, jit=0.6)
        # la hoja del calendario
        cae = e_out(clamp01((t - self.t_veinti + 0.3) / 0.45))
        hx, hy = 520, 520 - 700 * (1 - cae)
        P = PR.rot(C.rect(hx - 290, hy - 360, 580, 720), -0.05, np.array([hx, hy]))
        h.pieza(P, 226, 20, w=5, luz=(0.2, -1), d=12, trama=0, rim=0)
        h.pieza(PR.rot(C.rect(hx - 290, hy - 360, 580, 150), -0.05, np.array([hx, hy])), 28, 21, w=0, luz=(0, -1), d=1, sombra=0, trama=0,
                linea=False)
        if cae > 0.97:
            N.texto_maquina(h, "ENERO", hx + 12, hy - 285, 100, t, -99, cps=1e9, tono=0.96, centro=True, fuente=N.FUENTE_SELLO, encuadrar=False)
            N.texto_maquina(h, "29", hx - 4, hy + 10, 400, t, -99, cps=1e9, tono=0.04, centro=True, fuente=N.FUENTE_SELLO, encuadrar=False)
            N.texto_maquina(h, "2 0 2 4", hx - 14, hy + 280, 80, t, -99, cps=1e9, tono=0.10, centro=True, fuente=N.FUENTE_SELLO, encuadrar=False)
        # el farol de la comisaría y la puerta
        enc = smooth(clamp01((t - self.t_policia + 0.3) / 0.4)) * (0.85 + 0.15 * math.sin(t * 13))
        fx, fy = 1400, 250
        h.trazo(np.array([[fx + 180, fy - 120], [fx + 60, fy - 120], [fx, fy - 70]]), 14, 40, jit=0.3, taper=(0, 0))
        h.pieza(elipse_(fx, fy, 96, 104, n=30), 90 + 150 * enc, 41, w=7, luz=(0, -1), d=14, trama=0.2, rim=0.6)
        N.texto_maquina(h, "POLICÍA", fx, fy, 38, t, -99, cps=1e9, tono=0.05, centro=True, fuente=N.FUENTE_SELLO, encuadrar=False)
        if enc > 0:
            h.emitir(elipse_(fx, fy, 96, 104, n=30), 0.55 * enc, blur=3)
            h.luz_radial(fx, fy, 900, (1.0, 1.0, 1.0), k=1.5 * enc)
        h.pieza(C.rect(1210, 430, 380, 720), 30, 50, w=7, luz=(0, -1), d=12, trama=0.5, rim=0.5)
        h.pieza(C.rect(1250, 470, 300, 260), 110, 51, w=4, luz=(0, -1), d=6, trama=0.3)
        N.texto_maquina(h, "DENUNCIAS", 1400, 600, 44, t, -99, cps=1e9, tono=0.06, centro=True, fuente=N.FUENTE_SELLO, encuadrar=False)
        C.banda(h, "EL CASO LLEGA A LA POLICÍA", 1400, 1000, 46, t, self.t_policia, claro=True, sem=10)
        h.ambiente[:] = 0.62
        h.luz_radial(520, 420, 900, (1.0, 1.0, 1.0), k=0.9)
        N.lluvia(h, t, n=380, vel=1700, k=0.8)
        return h.acabado(t, niebla=dict(dens=0.18, vel=20, y0=300, y1=1080), bloom=0.5)

    # ------------------------------------------------------------------ la caja vacía
    def p_caja(self, h, t, u):
        h.camara(1.0 + 0.05 * u, 960, 540, 0.0)
        h.img[:] = 0.06
        ab = smooth(clamp01((t - self.t_para + 0.1) / 1.0))
        h.pieza(C.rect(430, 110, 1060, 860), 60, 20, w=10, luz=(-0.4, -1), d=24, trama=0.6, rim=0.7)          # cuerpo
        h.pieza(C.rect(500, 180, 920, 720), 10, 21, w=6, luz=(0, -1), d=1, sombra=0, trama=0)                 # interior, a oscuras
        for q in range(2):
            h.pieza(C.rect(500, 400 + q * 250, 920, 16), 40, 22 + q, w=3, luz=(0, -1), d=4, trama=0, rim=0.6)   # baldas vacías
        for q in range(9):                                         # telaraña en la esquina
            a = q * (math.pi / 2) / 8
            h.trazo(np.array([[500, 180], [500 + 260 * math.cos(a), 180 + 260 * math.sin(a)]]), 1.6, 30 + q, color=(210, 210, 210),
                    alfa=0.6, jit=0.3, taper=(0, 0))
        for r in (90, 160, 230):
            h.trazo(np.array([[500 + r * math.cos(a), 180 + r * math.sin(a) * (0.9 + 0.1 * math.sin(a * 9))]
                              for a in np.linspace(0, math.pi / 2, 14)]), 1.5, 40 + r, color=(210, 210, 210), alfa=0.55, jit=0.3, taper=(0, 0))
        an = 920 * (1 - 0.86 * ab)                                 # la puerta que se abre hacia la izquierda
        h.pieza(C.rect(500 - (920 - an) * 0.35, 180, an, 720), 84, 50, w=9, luz=(-0.4, -1), d=20, trama=0.6, rim=0.7)
        cx = 500 - (920 - an) * 0.35 + an / 2
        h.pieza(elipse_(cx, 540, 150 * an / 920, 150, n=40), 34, 51, w=7, luz=(-0.4, -1), d=12, trama=0.4, rim=0.8)
        for q in range(4):
            a = q * math.pi / 2 + ab * 4
            h.trazo(np.array([[cx, 540], [cx + 200 * math.cos(a) * an / 920, 540 + 200 * math.sin(a)]]), 14, 52 + q, jit=0.3)
        C.banda(h, "EL DINERO YA NO ESTABA", 1000, 560, 76, t, self.t_noestaba - 0.2, sem=11)
        h.ambiente[:] = 0.30
        h.luz_cono(960, -500, math.pi / 2, 0.5, 2000, (1.5, 1.5, 1.5), suave=0.5)
        if ab > 0.3:
            h.luz_radial(1000, 540, 700, (0.8, 0.8, 0.8), k=0.8 * ab)
        N.motas(h, t, n=120, k=0.8)
        return h.acabado(t, niebla=dict(dens=0.2, vel=8, y0=0, y1=1080, sube=False), bloom=0.45)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        self.ev(self.t_llamo - 0.5, "enchufa", 0.7, -0.3)
        self.ev(self.t_llamo, "silencio_tono", 0.5, -0.2, dur=max(1.5, self.t_bien - self.t_llamo))
        self.ev(self.t_otro - 0.35, "barrido_aire", 0.6, 0.3, dur=0.7)
        for q in range(5):
            self.ev(self.t_nadie + 0.3 * q, "teremin", 0.35, 0.2 + 0.1 * q, dur=0.5)
        self.ev(self.t_nohabia - 0.35, "sombra_crece", 0.7, 0.0, dur=3.0)
        self.ev(self.t_nohabia, "zumbido_lampara", 0.5, 0.0, dur=self.t_veinti - self.t_nohabia)
        for tk in (self.t_nohabia + 0.25, self.t_noreu + 0.25):
            self.ev(tk, "tachon", 0.9, -0.4)
        self.ev(self.t_jamas, "golpe_grave", 1.0, 0.0)
        self.ev(self.t_veinti - 0.35, "barrido_aire", 0.6, -0.3, dur=0.7)
        self.ev(self.t_veinti + 0.1, "papel_arranca", 0.9, -0.4)
        self.ev(self.t_veinti, "lluvia_amb", 0.6, 0.0, dur=self.t_para - self.t_veinti)
        self.ev(self.t_policia - 0.3, "lampara_chisporrotea", 0.7, 0.4, dur=1.0)
        self.ev(self.t_policia, "sello_golpe", 0.8, 0.4)
        self.ev(self.t_para - 0.1, "puerta", 0.9, 0.0)
        self.ev(self.t_noestaba - 0.2, "golpe_grave", 1.0, 0.0)
        self.ev(self.t1 - 0.8, "tinta_mancha", 0.6, 0.0, dur=0.9)
