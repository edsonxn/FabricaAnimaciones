# -*- coding: utf-8 -*-
"""Escena 16 «freno» (segundo final): seis manos por frenar; la mano baja la palanca y la caja de la máscara se apaga; al lado,
la máquina nueva, con el frente de cristal, piensa en voz alta (los pasos se leen); amanece sobre la ciudad y la gente camina;
detrás del vidrio esmerilado, diez siluetas sostienen los hilos del mundo; el armario se entreabre: hay un cráneo dentro."""
import math

import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import noir as N
import props as PR
from basen import BaseNoir
from comite import Comite
from esc_mentira import mascara
from motor import H, W, clamp01, e_out, smooth
from toon import elipse_, pulso, suave


def craneo(h, x, y, s=1.0, sem=0):
    h.pieza(np.asarray(suave([(-70, -40), (-60, -110), (0, -140), (60, -110), (70, -40), (48, 20), (40, 70), (-40, 70), (-48, 20)], 4)) * s
            + (x, y), 226, sem, w=5 * s, luz=(0.4, -1), d=12 * s, trama=0.3, rim=0)
    for q in (-1, 1):
        K.plano_(h, np.asarray(elipse_(x + q * 30 * s, y - 40 * s, 20 * s, 24 * s, n=16)), 8, sem + 2 + q)
    K.plano_(h, np.array([[x, y - 6 * s], [x + 12 * s, y + 22 * s], [x - 12 * s, y + 22 * s]]), 8, sem + 5)
    for q in range(5):
        h.trazo(np.array([[x + (-32 + q * 16) * s, y + 40 * s], [x + (-32 + q * 16) * s, y + 70 * s]]), 3 * s, sem + 6 + q, jit=0.2)


class Freno(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.com = Comite()
        self.t_segundo = w("Segundo final")
        self.t_seis = w("Seis")
        self.t_apagan = w("Apagan")
        self.t_miente = w("miente")
        self.t_constr = w("construyen")
        self.t_lenta = w("lenta")
        self.t_voz = w("voz alta")
        self.t_palabras = w("En palabras")
        self.t_leer = w("leer")
        self.t_funciona = w("Funciona")
        self.t_human = w("La humanidad")
        self.t_control = w("control")
        self.t_pero = w("Pero mira")
        self.t_comite = w("Un comité")
        self.t_punado = w("puñado")
        self.t_poder = w("poder")
        self.t_hasta = w("Hasta")
        self.t_feliz = w("feliz")
        self.t_cadaver = w("cadáver")
        self.plano(t0, self.p_seis)
        self.plano(self.t_apagan - 0.35, self.p_apagan, tr="barrido", dur=0.6, dirx=-1)
        self.plano(self.t_funciona - 0.4, self.p_amanece, tr="fundido", dur=0.9)
        self.plano(self.t_pero - 0.35, self.p_hilos, tr="humo", dur=0.7)
        self.plano(self.t_hasta - 0.35, self.p_armario, tr="barrido", dur=0.6, dirx=1)

    # ------------------------------------------------------------------ seis votan por frenar
    def p_seis(self, h, t, u):
        h.camara(1.06 + 0.014 * u, 960, 500, 0.0)
        alza = [0.0] * 10
        for q, k in enumerate([2, 5, 4, 7, 0, 9]):
            alza[k] = clamp01((t - (self.t_seis - 0.3 + q * 0.12)) / 0.35)
        self.com.dibujar(h, t, alza=alza)
        C.banda(h, "SEGUNDO FINAL", 960, 120, 100, t, self.t_segundo, claro=True, sem=5)
        C.banda(h, "SEIS VOTAN POR FRENAR", 960, 250, 54, t, self.t_seis, sem=6)
        h.ambiente[:] = 0.4
        N.motas(h, t, n=100, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.18, vel=8, y0=-200, y1=1000, sube=False), bloom=0.45)

    # ------------------------------------------------------------------ apagan una; construyen otra que piensa en voz alta
    def p_apagan(self, h, t, u):
        h.camara(1.0 + 0.012 * u, 960 + 16 * u, 540, 0.0)
        K.pared(h, 84, 30, paneles=11)
        K.plano_(h, C.rect(-300, 940, W + 600, 400), 70, 8, grad=(16, 940, 1200))
        off = smooth(clamp01((t - self.t_apagan - 0.1) / 0.35))
        tip = K.interruptor(h, 200, 470, 0.7, pos=off, sem=20, t=t)
        ac = smooth(clamp01((t - self.t_apagan + 0.7) / 0.5)) * (1 - smooth(clamp01((t - self.t_apagan - 0.9) / 0.6)))
        PR.mano(h, tip[0] - 50 - 420 * (1 - ac), tip[1], 1.0, ang=0.0, d=1, sem=40, dedos=0.2)
        t1 = PR.caja_negra(h, 640, 940, 0.95, 1.0 - off, t, sem=60, cable=False)
        mascara(h, 640, 620 + 260 * off, 0.8, sem=90, ang=1.2 * off, sonrisa=1.0 - 1.6 * off)       # la careta cae
        # la máquina nueva: frente de cristal, se levanta al nombrarla
        sube = e_out(clamp01((t - self.t_constr + 0.2) / 0.8))
        if sube > 0:
            x2, w_, a_ = 1330, 620, 720
            y0 = 940 - a_ * sube
            h.pieza(C.rect(x2 - w_ / 2, y0, w_, a_ * sube), 30, 120, w=7, luz=(0.3, -1), d=18, trama=0.5, rim=0.9)
            if sube > 0.95:
                vid = C.rect(x2 - w_ / 2 + 40, 260, w_ - 80, 560)
                K.plano_(h, vid, 205, 121)
                h.luz_fija(vid, 0.9)
                h.emitir(vid, 0.2, blur=10)
                pasos = ("PASO 1: leo la orden.", "PASO 2: dudo de un dato.", "PASO 3: pregunto antes.", "PASO 4: explico por qué.",
                         "RESPUESTA: aquí está.")
                N.soporte(h, x2, 540, w_ - 80, 560, margen=24)          # los renglones se ajustan al ancho del cristal
                dur = max(2.0, self.t_leer - self.t_voz + 1.0)
                for k, s_ in enumerate(pasos):
                    N.texto_maquina(h, s_, x2 - w_ / 2 + 64, 290 + k * 100, 36, t, self.t_voz - 0.6 + k * dur / 5, cps=24, tono=0.05,
                                    encuadrar=False)
                h.luz_radial(x2, 540, 800, (1.0, 1.0, 1.0), k=0.9)
        C.banda(h, "APAGAN LA QUE MIENTE", 430, 90, 50, t, self.t_apagan, sem=5)
        C.banda(h, "OTRA: MÁS LENTA", 1330, 90, 50, t, self.t_lenta - 0.4, claro=True, sem=6)
        C.banda(h, "PIENSA EN VOZ ALTA", 1330, 1010, 64, t, self.t_voz - 0.2, sem=7)
        h.ambiente[:] = 0.46
        h.luz_cono(640, -400, math.pi / 2, 0.26, 1800, (1.5, 1.5, 1.5), k=1.0 - 0.8 * off, suave=0.5)
        h.luz_radial(200, 470, 480, (1.0, 1.0, 1.0), k=0.9)
        N.motas(h, t, n=100, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.18, vel=10, y0=0, y1=1080, sube=False), bloom=0.5)

    # ------------------------------------------------------------------ funciona: amanece
    def p_amanece(self, h, t, u):
        am = smooth(clamp01((t - self.t_funciona + 0.2) / 2.6))
        h.camara(0.92 + 0.008 * u, 1600 + 30 * u, 600, 0.0)
        MU.cielo().pegar(h, 0.05, dx=-(t * 5.0) % 300)
        MU.lejos().pegar(h, 0.3, bruma=0.6, tono_bruma=0.42 + 0.2 * am)
        MU.medio().pegar(h, 0.6, bruma=0.25, tono_bruma=0.40 + 0.2 * am)
        MU.calle().pegar(h, 1.0)
        for k in range(6):                                           # la gente vuelve a la calle
            d = 1 if k % 2 == 0 else -1
            x = (900 + k * 330 + d * (t - self.t_funciona) * (70 + 12 * k)) % 2600 + 500
            K.caminante(h, x, 935, 0.62, fase=K.fase_paso((t - self.t_funciona) * (70 + 12 * k), 0.62) + k * 1.9, sem=100 + k * 30, tono=50 + 14 * (k % 3), d=d, luz=(0.6, -0.8), rim=0.9,
                        barba=(k % 3 == 0), pelo=20 + 16 * (k % 3))
        h.ambiente[:] = 0.8 + 0.55 * am
        h.luz_radial(2600, 300, 2600, (1.0, 1.0, 1.0), k=0.9 * am)       # el sol, por la derecha
        h.camara(1.0, W / 2, H / 2, 0.0)
        C.banda(h, "FUNCIONA", 960, 150, 130, t, self.t_funciona, claro=True, sem=5)
        C.banda(h, "LA HUMANIDAD CONSERVA EL CONTROL", 960, 300, 52, t, self.t_human + 0.3, sem=6)
        return h.acabado(t, niebla=dict(dens=0.2, y0=300, y1=1080, vel=16), bloom=0.55)

    # ------------------------------------------------------------------ quién sostiene ese control
    def p_hilos(self, h, t, u):
        h.camara(1.0 + 0.012 * u, 960, 540, 0.0)
        K.pared(h, 26, 8)
        # el ventanal esmerilado del comité, arriba: diez siluetas
        vid = C.rect(180, 60, 1560, 360)
        K.plano_(h, vid, 190, 20, grad=(120, 60, 420))
        h.emitir(vid, 0.3, blur=8)
        h.luz_fija(vid, 0.8)
        xs = [280 + k * 151 for k in range(10)]
        for k, x in enumerate(xs):
            if t > self.t_pero + k * 0.12:
                K.persona(h, x, 430 + 4 * math.sin(t * 1.1 + k), 0.72, 100 + k * 9, tono=8, bal=3 * math.sin(t * 0.9 + k * 2), rim=0.0,
                          sombrero=(k % 4 == 1))
        h.anillo(h.tf(vid), 12 * h.zoom, 21, color=(14, 14, 14), jit=0.4)
        for q in (1, 2, 3):
            h.trazo(np.array([[180 + q * 390, 60], [180 + q * 390, 420]]), 8, 22 + q, color=(14, 14, 14), jit=0.3, taper=(0, 0))
        # los hilos bajan hasta la ciudad en miniatura y la máquina
        K.plano_(h, C.rect(-100, 900, W + 200, 300), 60, 30, grad=(16, 900, 1100))
        r = np.random.default_rng(8)
        edif = []
        for k in range(16):
            x = 150 + k * 104
            al = r.uniform(110, 260)
            edif.append((x, al))
            h.pieza(C.rect(x, 900 - al, 84, al), 70 + 10 * (k % 3), 40 + k, w=3.5, luz=(0.2, -1), d=8, trama=0.5, rim=0.7)
            for j in range(int(al // 34)):
                for i in range(3):
                    if (i + j + k) % 3 == 0:
                        h.emitir(C.rect(x + 12 + i * 24, 900 - al + 12 + j * 34, 10, 16), 0.7, blur=1)
        ten = smooth(clamp01((t - self.t_punado + 0.2) / 0.8))
        for k, x in enumerate(xs):
            ex, al = edif[(k * 3 + 1) % 16]
            sw = 10 * math.sin(t * 1.3 + k)
            h.trazo(np.array([[x, 400], [(x + ex + 42) / 2 + sw, 560], [ex + 42, 900 - al]]), 2.2, 70 + k, color=(215, 215, 215),
                    alfa=0.85 * ten, jit=0.2, taper=(0, 0))
        C.banda(h, "¿QUIÉN SOSTIENE ESE CONTROL?", 960, 500, 50, t, self.t_pero + 0.3, sem=5)
        C.banda(h, "UN COMITÉ", 420, 1000, 84, t, self.t_comite, claro=True, sem=6)
        C.banda(h, "EL PODER MÁS GRANDE QUE HA EXISTIDO", 1300, 1000, 46, t, self.t_poder - 0.6, sem=7)
        h.ambiente[:] = 0.42
        h.luz_radial(960, 760, 1300, (1.0, 1.0, 1.0), k=0.7)
        N.motas(h, t, n=90, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.16, vel=10, y0=300, y1=1080, sube=False), bloom=0.5)

    # ------------------------------------------------------------------ un cadáver en el armario
    def p_armario(self, h, t, u):
        h.camara(1.0 + 0.03 * u, 1000 + 10 * u, 520, 0.0)
        K.pared(h, 40, 12, paneles=9)
        K.plano_(h, C.rect(-300, 960, W + 600, 400), 40, 8, grad=(10, 960, 1200))
        x0, y0, an, al = 720, 130, 560, 830
        h.pieza(C.rect(x0 - 40, y0 - 50, an + 80, al + 50), 34, 20, w=8, luz=(0.3, -1), d=18, trama=0.6, rim=0.8)
        h.pieza(np.array([[x0 - 70, y0 - 50], [x0 + an + 70, y0 - 50], [x0 + an + 40, y0 - 100], [x0 - 40, y0 - 100]]), 44, 21, w=6,
                luz=(0.3, -1), d=10, trama=0.4, rim=0.8)
        K.plano_(h, C.rect(x0, y0, an, al), 4, 22)                                                # el interior, negro
        ab = smooth(clamp01((t - self.t_cadaver + 0.9) / 1.2))
        if ab > 0.15:
            craneo(h, x0 + an * 0.74, y0 + 330, 1.1, sem=40)
            for q in range(4):                                       # costillas
                h.trazo(np.array([[x0 + an * 0.62, y0 + 470 + q * 44], [x0 + an * 0.74, y0 + 452 + q * 44], [x0 + an * 0.86, y0 + 470 + q * 44]]),
                        9, 50 + q, color=(215, 215, 215), jit=0.4)
            h.luz_radial(x0 + an * 0.74, y0 + 380, 420, (1.0, 1.0, 1.0), k=1.5 * ab)
        h.pieza(C.rect(x0, y0, an / 2, al), 60, 60, w=6, luz=(0.3, -1), d=12, trama=0.5, rim=0.7)                # hoja izquierda, cerrada
        wd = an / 2 * (1 - 0.72 * ab)                                # la derecha se abre con un chirrido
        h.pieza(C.rect(x0 + an - wd + an / 2 * 0.72 * ab * 0.0, y0, wd, al), 64, 61, w=6, luz=(0.3, -1), d=12, trama=0.5, rim=0.7) if ab < 0.02 \
            else h.pieza(np.array([[x0 + an, y0], [x0 + an + (an / 2 - wd) * 0.9, y0 - 26], [x0 + an + (an / 2 - wd) * 0.9, y0 + al + 30],
                                   [x0 + an, y0 + al]]), 52, 61, w=6, luz=(0.3, -1), d=12, trama=0.5, rim=0.7)
        for q in (0, 1):
            h.pieza(np.asarray(elipse_(x0 + an / 2 - 24 + q * 0, y0 + al / 2, 10, 26, n=12)), 170, 70 + q, w=3, luz=(0.3, -1), d=3, trama=0,
                    rim=0.9) if q == 0 else None
        C.banda(h, "EL FINAL FELIZ", 330, 200, 70, t, self.t_feliz - 0.4, claro=True, sem=5)
        C.banda(h, "TIENE UN CADÁVER EN EL ARMARIO", 420, 990, 50, t, self.t_cadaver - 0.2, sem=6)
        h.ambiente[:] = 0.32
        h.luz_cono(1000, -420, math.pi / 2, 0.4, 1900, (1.5, 1.5, 1.5), k=1.0, suave=0.5)
        N.motas(h, t, n=100, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.18, vel=10, y0=0, y1=1080, sube=False), bloom=0.45)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        t0 = self.t0
        self.ev(self.t_segundo, "sello_golpe", 1.0, 0.0)
        for q in range(0, 6, 2):
            self.ev(self.t_seis - 0.3 + q * 0.12, "papel_atrapa", 0.5, -0.5 + 0.3 * q)
        self.ev(self.t_apagan - 0.35, "barrido_aire", 0.6, 0.0, dur=0.7)
        self.ev(self.t_apagan + 0.1, "interruptor", 1.0, -0.5)
        self.ev(self.t_apagan + 0.2, "apagado_vela", 0.8, -0.2)
        self.ev(self.t_apagan + 0.6, "corona_cae", 0.7, -0.2)
        self.ev(self.t_constr - 0.2, "crecer", 0.7, 0.3, dur=1.0)
        self.ev(self.t_voz - 0.6, "tecleo_rapido", 0.5, 0.3, dur=max(2.0, self.t_leer - self.t_voz + 1.6))
        self.ev(self.t_voz - 0.2, "sello_golpe", 0.9, 0.3)
        self.ev(self.t_funciona - 0.4, "pajaros_ciudad", 0.7, 0.0, dur=self.t_pero - self.t_funciona + 0.4)
        self.ev(self.t_funciona, "sello_golpe", 0.9, 0.0)
        self.ev(self.t_pero - 0.35, "sombra_crece", 0.8, 0.0, dur=3.0)
        self.ev(self.t_comite, "sello_golpe", 1.0, -0.3)
        self.ev(self.t_punado, "hilo_tenso", 0.8, 0.0)
        self.ev(self.t_poder - 0.6, "golpe_grave", 1.0, 0.0)
        self.ev(self.t_hasta - 0.35, "barrido_aire", 0.6, 0.0, dur=0.7)
        self.ev(self.t_cadaver - 0.9, "puerta", 0.9, 0.2)
        self.ev(self.t_cadaver - 0.2, "golpe_grave", 1.0, 0.0)
        self.ev(self.t_cadaver, "grave_inquietante", 0.7, 0.0, dur=2.5)
        self.ev(self.t1 - 0.8, "tinta_mancha", 0.6, 0.0, dur=0.9)
