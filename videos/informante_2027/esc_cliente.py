# -*- coding: utf-8 -*-
"""Escena 2 «cliente»: Daniel en la rueda de reconocimiento (nombre real en pantalla; «INGENIERO» tachado, «FILÓSOFO»);
2022: su silueta entra por la puerta iluminada de la empresa; el oficio raro: una hoja donde los años se escriben a máquina
y una curva que sube sola; la diana donde ya hay un dardo en el centro (y cae otro)."""
import math

import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import noir as N
import props3 as PR3
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from noir_pers import Frontal
from toon import pulso


class Cliente(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.dan = Frontal(sem=77)
        self.t_llama = w("Se llama")
        self.t_daniel = w("Daniel")
        self.t_noes = w("No es")
        self.t_filo = w("filósofo")
        self.t_en = w("En dos mil")
        self.t_entro = w("entró")
        self.t_casa = w("casa")
        self.t_oficio = w("Su oficio")
        self.t_adiv = w("adivinar")
        self.t_escrito = w("escrito")
        self.t_yporque = w("Y por qué")
        self.t_porque = w("Porque")
        self.t_acert = w("acertado")
        self.plano(t0, self.p_ficha)
        self.plano(self.t_en - 0.35, self.p_entra, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_oficio - 0.35, self.p_oficio, tr="humo", dur=0.7)
        self.plano(self.t_yporque - 0.35, self.p_diana, tr="empuje", dur=0.6, centro=(W * 0.5, H * 0.45))

    # ------------------------------------------------------------------ la ficha
    def p_ficha(self, h, t, u):
        h.camara(1.04 + 0.03 * u, 900 + 12 * u, 520, 0.0)
        MU.sala_rueda().pegar(h, 1.0, oscuro=0.75)
        s = 1.55
        p = dict(x=620, y=1060, s=s, luz=(0.0, -1.0), rim=0.9, mira=0.5 * math.sin(t * 0.7), cabeza=0.04 * math.sin(t * 0.9), **K.DAN)
        self.dan.dibujar(h, p)
        C.banda(h, "DANIEL KOKOTAJLO", 1330, 300, 78, t, self.t_daniel, sem=5)
        C.banda(h, "INGENIERO", 1330, 470, 60, t, self.t_noes, claro=True, sem=6)
        a = clamp01((t - self.t_noes - 0.45) / 0.3)
        if a > 0:
            h.trazo(np.array([[1090, 484], [1090 + 480 * a, 458]]), 16, 80, color=(12, 12, 12), jit=0.6, taper=(0.1, 0.1))
        C.banda(h, "FILÓSOFO", 1330, 620, 96, t, self.t_filo, claro=True, sem=7)
        h.ambiente[:] = 0.34
        fl = pulso(t, self.t_daniel, 0.25, 1.0)                    # fogonazo de la cámara de la ficha
        h.luz_cono(620, -500, math.pi / 2, 0.40, 2000, (1.7, 1.7, 1.7), suave=0.5)
        h.luz_radial(620, 400, 1500, (1.0, 1.0, 1.0), k=2.5 * fl)
        N.motas(h, t, n=90, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.16, vel=8, y0=-200, y1=1000, sube=False), flash=0.35 * fl, bloom=0.45)

    # ------------------------------------------------------------------ 2022: entra a la empresa
    def p_entra(self, h, t, u):
        h.camara(1.0 + 0.05 * u, 980 + 20 * u, 560, 0.0)
        K.pared(h, 40, 12, paneles=11)
        K.plano_(h, C.rect(-300, 930, W + 600, 400), 26, 8, grad=(8, 930, 1200))                     # suelo
        ab = smooth(clamp01((t - self.t_en + 0.2) / 0.9))
        K.puerta(h, 1180, 130, 460, 800, sem=20, abre=ab, tono=34)
        # su silueta camina hacia la luz (ciclo de paso con balanceo)
        if ab > 0:                                                  # la luz de la puerta se derrama por el suelo
            K.plano_(h, np.array([[1180, 930], [1640, 930], [1560, 1320], [420, 1320]]), 200, 58, alfa=0.9 * ab)
            h.luz_fija(np.array([[1180, 930], [1640, 930], [1560, 1320], [420, 1320]]), 0.25 + 0.6 * ab)
        av = smooth(clamp01((t - self.t_en) / (self.t_oficio - self.t_en)))
        x = 760 + 640 * av
        sc = 1.75 - 0.35 * av                                       # se aleja hacia la puerta
        if ab > 0:                                                  # su sombra larga, hacia nosotros
            K.plano_(h, np.array([[x - 60, 1000], [x + 60, 1000], [x - 300, 1320], [x - 620, 1320]]), 4, 60, alfa=0.7 * ab)
        K.caminante(h, x, 1010, sc * 0.82, fase=K.fase_paso(x - 760, sc * 0.82), sem=40, tono=22, luz=(1.0, -0.3), rim=0.95)
        C.banda(h, "2022", 520, 250, 150, t, self.t_en + 0.3, sem=5)
        C.banda(h, "ENTRA A OPENAI", 520, 400, 58, t, self.t_entro, claro=True, sem=6)
        C.banda(h, "LA CASA DE CHATGPT", 520, 490, 40, t, self.t_casa, sem=7)
        h.ambiente[:] = 0.22
        N.motas(h, t, n=110, k=0.8, caja=(1000, 100, 1800, 1000))
        return h.acabado(t, niebla=dict(dens=0.26, vel=14, y0=0, y1=1080, sube=False), bloom=0.6)

    # ------------------------------------------------------------------ adivinar el futuro y ponerlo por escrito
    def p_oficio(self, h, t, u):
        h.camara(1.0 + 0.02 * u, 960, 540, 0.008)
        MU.escritorio().pegar(h, 1.0, oscuro=0.8, dx=60)
        K.taza_arriba(h, 1640, 800, 1.2, 90, t)
        T = K.hoja(h, 720, 540, 980, 800, ang=-0.03, sem=10)
        P = T([(-430, -360)])[0]
        N.texto_maquina(h, "PRONÓSTICO", P[0], P[1], 70, t, self.t_oficio + 0.2, cps=16, tono=0.05, fuente=N.FUENTE_SELLO,
                        encuadrar=False)
        dur = max(1.0, self.t_escrito - self.t_adiv)
        for k, an in enumerate(("2023", "2024", "2025", "2026", "2027")):
            tk = self.t_adiv - 0.2 + k * dur / 5
            P = T([(-430, -230 + k * 104)])[0]
            N.texto_maquina(h, an + "  . . . . . . . . . . . .", P[0], P[1], 52, t, tk, cps=30, tono=0.06, encuadrar=False)
        # la curva que sube (dibujada a pluma, en el margen derecho)
        a = clamp01((t - self.t_adiv) / (dur + 0.6))
        n = max(2, int(50 * a))
        xs = np.linspace(0, 1, 50)[:n]
        Q = T(np.stack([120 + 330 * xs, 330 - 620 * xs ** 3.0], 1))
        h.trazo(np.array([T([(120, -330)])[0], T([(120, 330)])[0], T([(460, 330)])[0]]), 5, 70, jit=0.4, taper=(0, 0))
        if a > 0:
            h.trazo(Q, 9, 71, color=(14, 14, 14), jit=0.5, taper=(0.3, 0.0))
            h.pieza(np.asarray(K.elipse_(Q[-1][0], Q[-1][1], 14, 14, n=12)), 20, 72, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False)
        K.pluma(h, Q[-1][0] + 6, Q[-1][1] - 4, ang=-0.8, s=1.3, sem=75)
        C.banda(h, "OFICIO: ADIVINAR EL FUTURO", 1500, 1000, 46, t, self.t_adiv, sem=5)
        h.ambiente[:] = 0.34
        h.luz_cono(700, -520, math.pi / 2 - 0.05, 0.52, 2200, (1.6, 1.6, 1.6), suave=0.5)
        N.motas(h, t, n=80, k=0.6)
        return h.acabado(t, niebla=None, bloom=0.4)

    # ------------------------------------------------------------------ ya había acertado
    def p_diana(self, h, t, u):
        h.camara(1.0 + 0.05 * u, 960, 520, 0.0)
        K.pared(h, 58, 22, ladrillo=True)
        cx, cy, r = 960, 500, 400
        K.plano_(h, np.asarray(K.elipse_(cx + 26, cy + 30, r * 1.04, r * 1.04, n=50)), 6, 7, alfa=0.6)       # sombra en la pared
        PR3.diana(h, cx, cy, r, sem=20)
        PR3.dardo(h, cx - 8, cy + 6, -0.5, 1.5, sem=40)                                                 # el dardo viejo, en el centro
        for k, (tk, dx, dy) in enumerate(((self.t_porque, 22, -16), (self.t_acert, -6, 20))):
            if t < tk - 0.25:
                continue
            a = clamp01((t - tk + 0.25) / 0.25)
            vib = 0.06 * math.exp(-(t - tk) * 6) * math.sin((t - tk) * 60) if t > tk else 0.0
            PR3.dardo(h, cx + dx + 1500 * (1 - a), cy + dy - 900 * (1 - a), -0.55 + 0.2 * k + vib, 1.5, sem=50 + 10 * k)
        C.banda(h, "¿POR QUÉ CONTRATAR A UN ADIVINO?", 960, 110, 50, t, self.t_yporque + 0.1, sem=5)
        C.banda(h, "YA HABÍA ACERTADO", 960, 990, 80, t, self.t_acert, claro=True, sem=6)
        g = pulso(t, self.t_acert, 0.3, 1.0)
        h.ambiente[:] = 0.34
        h.luz_cono(960, -620, math.pi / 2, 0.5, 2200, (1.7, 1.7, 1.7), suave=0.5)
        h.luz_radial(cx, cy, 900, (1.0, 1.0, 1.0), k=1.4 * g)
        N.motas(h, t, n=100, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.16, vel=8, y0=0, y1=1080, sube=False), bloom=0.45, flash=0.2 * g)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        t0 = self.t0
        self.ev(t0, "zumbido_foco", 0.5, 0.0, dur=self.t_en - t0)
        self.ev(self.t_daniel, "focos", 0.8, 0.0)
        self.ev(self.t_daniel, "sello_golpe", 0.9, 0.3)
        self.ev(self.t_noes + 0.45, "tachon", 0.9, 0.3)
        self.ev(self.t_filo, "sello_golpe", 1.0, 0.3)
        self.ev(self.t_en - 0.35, "barrido_aire", 0.6, 0.0, dur=0.7)
        self.ev(self.t_en - 0.1, "puerta", 0.9, 0.3)
        for k in range(6):
            self.ev(self.t_en + 0.5 + k * 0.6, "paso_firme", 0.5, -0.5 + 0.18 * k)
        self.ev(self.t_entro, "sello_golpe", 0.8, -0.3)
        self.ev(self.t_oficio - 0.35, "papel_atrapa", 0.7, 0.0)
        self.ev(self.t_oficio + 0.2, "tecleo_rapido", 0.5, -0.2, dur=0.7)
        dur = max(1.0, self.t_escrito - self.t_adiv)
        for k in range(5):
            self.ev(self.t_adiv - 0.2 + k * dur / 5, "tecleo_rapido", 0.45, -0.3, dur=0.6)
            self.ev(self.t_adiv + 0.4 + k * dur / 5, "carro_maquina", 0.35, 0.2)
        self.ev(self.t_adiv, "pluma", 0.5, 0.3)
        self.ev(self.t_yporque - 0.35, "barrido_aire", 0.6, 0.0, dur=0.7)
        self.ev(self.t_porque, "dardo", 0.9, 0.2)
        self.ev(self.t_acert, "dardo", 1.0, -0.1)
        self.ev(self.t_acert, "golpe_grave", 0.9, 0.0)
        self.ev(self.t1 - 0.8, "tinta_mancha", 0.6, 0.0, dur=0.9)
