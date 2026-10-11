# -*- coding: utf-8 -*-
"""Escena 8 «agentes»: el asistente torpe (un brazo robot que vuelca la taza en la barra de la cafetería); dentro del
laboratorio, la caja negra escribe código en las pantallas y, a su lado, se levanta la siguiente versión; la cadena: cada
máquina construye una mayor; la espiral en la que cada vuelta dura menos."""
import math

import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import mundos27 as M27
import noir as N
import props as PR
import props4 as PR4
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from toon import Pista, elipse_, pulso


class Agentes(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_emp = w("empieza")
        self.t_torpes = w("torpes")
        self.t_equiv = w("equivocan")
        self.t_caro = w("caro")
        self.t_pero = w("Pero dentro")
        self.t_usa = w("usa")
        self.t_codigo = w("código")
        self.t_sig = w("siguiente")
        self.t_esa = w("Esa es")
        self.t_una = w("Una máquina")
        self.t_mejor = w("mejor")
        self.t_otra = w("otra")
        self.t_cada = w("Cada vuelta")
        self.t_corta = w("corta")
        self.cam_c = Pista([(self.t_esa - 0.5, (520, 600, 1.25)), (self.t_una, (560, 600, 1.2), "io"), (self.t_mejor, (820, 560, 0.95), "io"),
                            (self.t_otra + 0.6, (960, 500, 0.72), "io"), (self.t_cada, (960, 490, 0.70), "l")])
        self.plano(t0, self.p_torpe)
        self.plano(self.t_pero - 0.35, self.p_lab, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_esa - 0.35, self.p_cadena, tr="empuje", dur=0.6, centro=(W * 0.4, H * 0.55))
        self.plano(self.t_cada - 0.35, self.p_espiral, tr="humo", dur=0.6)

    # ------------------------------------------------------------------ asistentes torpes
    def p_torpe(self, h, t, u):
        h.camara(1.0 + 0.014 * u, 960 + 6 * u, 540, 0.0)
        MU.cafeteria().pegar(h, 1.0, oscuro=0.85)
        h.pieza(C.rect(-200, 800, W + 400, 60), 96, 20, w=6, luz=(0, -1), d=10, trama=0.3, rim=0.8)                 # la barra
        K.plano_(h, C.rect(-200, 860, W + 400, 400), 30, 21, grad=(8, 860, 1100))
        # el brazo intenta servir... y vuelca la taza
        gol = smooth(clamp01((t - self.t_equiv + 0.25) / 0.3))
        osc = 0.10 * math.sin(t * 9.0) * (1 - gol)                    # tiembla, indeciso
        a1 = -0.55 + 0.25 * math.sin(t * 1.3) + 0.5 * gol
        a2 = 1.35 + osc + 0.55 * gol
        a3 = 2.2 + 2 * osc
        PR4.brazo_robot(h, 620, 800, a1, a2, a3, s=1.5, pinza=0.5 + 0.4 * math.sin(t * 5), sem=40, tono=110)
        vu = smooth(clamp01((t - self.t_equiv) / 0.35))
        cx, cy = 1180 + 40 * vu, 800
        c = np.array([cx, cy])
        taza = PR.rot(np.array([(-52, -110), (52, -110), (42, 0), (-42, 0)], float) + c, 1.45 * vu, c)
        if vu > 0.4:                                                 # el charco de café que se extiende por la barra
            ch = smooth(clamp01((t - self.t_equiv - 0.2) / 1.5))
            K.plano_(h, np.asarray(elipse_(cx + 150 + 110 * ch, 820, 60 + 240 * ch, 16, n=30)), 8, 60, alfa=0.9)
            for q in range(3):
                dy = ((t - self.t_equiv) * 190 + q * 70) % 240
                K.plano_(h, np.asarray(elipse_(cx + 300 + 80 * q, 860 + dy, 6, 12, n=10)), 8, 62 + q, alfa=0.9 * (1 - dy / 240))
        h.pieza(taza, 226, 50, w=5, luz=(0.2, -1), d=10, trama=0.2, rim=0.6)
        C.banda(h, "ASISTENTES TORPES", 1420, 230, 70, t, self.t_torpes, sem=5)
        C.banda(h, "SE EQUIVOCAN", 1420, 340, 50, t, self.t_equiv, claro=True, sem=6)
        C.banda(h, "Y CUESTAN CARO", 1420, 430, 50, t, self.t_caro - 0.2, claro=True, sem=7)
        C.banda(h, "ASÍ EMPIEZA EL EXPEDIENTE: 2025", 420, 1010, 40, t, self.t_emp, sem=8)
        h.ambiente[:] = 0.42
        h.luz_cono(900, -400, math.pi / 2, 0.6, 1900, (1.5, 1.5, 1.5), suave=0.5)
        N.motas(h, t, n=90, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.16, vel=10, y0=0, y1=1080, sube=False), bloom=0.45)

    # ------------------------------------------------------------------ dentro del laboratorio
    def p_lab(self, h, t, u):
        h.camara(1.0 + 0.016 * u, 960, 520, 0.0)
        M27.laboratorio().pegar(h, 1.0)
        for k, (x, y, w_, hh) in enumerate(((60, 180, 300, 420), (1560, 180, 300, 420))):       # pantallas en los armarios
            h.pieza(C.rect(x - 12, y - 12, w_ + 24, hh + 24), 20, 20 + k * 10, w=5, luz=(0, -1), d=6, trama=0.2, rim=0.6)
            K.pantalla_codigo(h, (x, y, w_, hh), t, sem=30 + k * 50, vel=3.0 + k)
            C.luz_rect(h, C.rect(x, y, w_, hh), 0.9, suave_=8)
        tip = PR.caja_negra(h, 700, 980, 0.95, 1.0, t, sem=60, cable=False)
        # la siguiente versión se levanta al lado, de abajo arriba (más grande)
        cre = smooth(clamp01((t - self.t_codigo + 0.3) / max(1.5, self.t_esa - self.t_codigo)))
        if cre > 0:
            s2 = 1.3
            w_, a_ = 230 * s2, 520 * s2
            alto = a_ * cre
            x2 = 1180
            h.anillo(h.tf(C.rect(x2 - w_ / 2, 980 - a_, w_, a_)), 3 * h.zoom, 80, color=(200, 200, 200), alfa=0.5, jit=0.6)
            h.pieza(C.rect(x2 - w_ / 2, 980 - alto, w_, alto), 22, 81, w=6, luz=(0.3, -1), d=20, trama=0.5, rim=0.95, rim_tono=200)
            for q in range(int(alto // 44)):
                yy = 980 - 30 - q * 44
                h.trazo(np.array([[x2 - w_ / 2 + 36, yy], [x2 + w_ / 2 - 36, yy]]), 3.5, 82 + q, color=(80, 80, 80), alfa=0.8, jit=0.2)
            K.plano_(h, C.rect(x2 - w_ / 2, 980 - alto - 6, w_, 8), 240, 99)                     # el frente de obra, brillante
            h.emitir(C.rect(x2 - w_ / 2, 980 - alto - 6, w_, 8), 1.0)
            for q in range(5):                                       # renglones de código que viajan de una a otra
                f = ((t * 1.3 + q / 5.0) % 1.0)
                xx = 820 + (x2 - w_ / 2 - 820) * f
                K.plano_(h, C.rect(xx, 620 + q * 46, 60, 9), 230, 100 + q, alfa=math.sin(math.pi * f))
        C.banda(h, "DENTRO DEL LABORATORIO", 960, 90, 50, t, self.t_pero + 0.2, sem=5)
        C.banda(h, "ESCRIBEN EL CÓDIGO DE LA SIGUIENTE VERSIÓN", 960, 1020, 44, t, self.t_codigo - 0.2, claro=True, sem=6)
        h.ambiente[:] = 0.5
        h.luz_cono(940, -300, math.pi / 2, 0.5, 1800, (1.4, 1.4, 1.4), suave=0.5)
        h.luz_radial(tip[0], tip[1], 400, (1.0, 1.0, 1.0), k=1.0)
        N.motas(h, t, n=90, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.2, vel=12, y0=200, y1=1080, sube=False), bloom=0.55)

    # ------------------------------------------------------------------ una máquina construye una máquina mejor
    def p_cadena(self, h, t, u):
        cx, cy, z = self.cam_c(t)
        h.camara(z, cx, cy, 0.0)
        K.plano_(h, C.rect(-1200, -900, W + 2400, 1800), 70, 6, grad=(30, -300, 900))
        for q in range(22):
            h.trazo(np.array([[-1100 + q * 190, -800], [-1096 + q * 190, 900]]), 5, 300 + q, alfa=0.4, jit=0.5)
        K.plano_(h, C.rect(-1200, 900, W + 2400, 900), 90, 8, grad=(20, 900, 1400))
        datos = ((420, 0.55, self.t_esa - 0.2), (900, 0.95, self.t_mejor - 0.3), (1540, 1.5, self.t_otra - 0.1))
        for k, (x, s, tk) in enumerate(datos):
            a = e_out(clamp01((t - tk) / 0.35))
            if a <= 0:
                continue
            PR.caja_negra(h, x, 900 + 600 * (1 - a), s, 1.0, t + k, sem=40 + k * 40, cable=False)
            h.luz_cono(x, -700, math.pi / 2, 0.16 + 0.07 * k, 2300, (1.8, 1.8, 1.8), k=1.3 * a, suave=0.5)
            N.texto_maquina(h, f"v{k + 1}", x, 960, 60 + 20 * k, t, tk + 0.3, cps=1e9, tono=0.95, centro=True, fuente=K.IMPACT, encuadrar=False)
            if k < 2:
                x2 = datos[k + 1][0]
                K.flecha(h, (x + 150 * s, 640 - 160 * k), (x2 - 180 * datos[k + 1][1], 600 - 200 * k), 12, 150 + k * 5,
                         u=clamp01((t - datos[k + 1][2] + 0.35) / 0.4), curva=-60)
        h.camara(1.0, W / 2, H / 2, 0.0)
        C.banda(h, "LA PIEZA CLAVE DEL CASO", 420, 110, 60, t, self.t_esa + 0.3, sem=5)
        C.banda(h, "CADA MÁQUINA CONSTRUYE LA SIGUIENTE", 1300, 110, 44, t, self.t_mejor, claro=True, sem=6)
        h.ambiente[:] = 0.5
        N.motas(h, t, n=100, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.2, vel=10, y0=0, y1=1080, sube=False), bloom=0.5)

    # ------------------------------------------------------------------ cada vuelta es más corta
    def p_espiral(self, h, t, u):
        h.camara(1.0 + 0.03 * u, 960, 540, 0.02 * u)
        K.pared(h, 24, 6)
        cx, cy = 960, 540
        vueltas = 5.0
        th = np.linspace(0, vueltas * 2 * math.pi, 420)
        rr = 500 * (1 - th / th[-1]) ** 0.9 + 30
        P = np.stack([cx + rr * np.cos(th), cy + rr * np.sin(th) * 0.92], 1)
        h.trazo(P, 7, 20, color=(190, 190, 190), jit=0.4, taper=(0.0, 0.5))
        # la bolita recorre la espiral: cada vuelta, en menos tiempo
        a = clamp01((t - self.t_cada + 0.2) / max(2.0, self.t1 - self.t_cada - 0.6))
        f = 1 - (1 - a) ** 2.2
        i = min(len(P) - 1, int(f * (len(P) - 1)))
        for q in range(8):                                           # estela
            j = max(0, i - q * 5)
            h.emitir(elipse_(P[j][0], P[j][1], 16 - q * 1.6, 16 - q * 1.6, n=10), 1.0 - q * 0.11, blur=2)
        h.luz_radial(P[i][0], P[i][1], 320, (1.0, 1.0, 1.0), k=1.2)
        for k in range(int(vueltas)):                                # marcas de vuelta con su duración
            j = int((k + 1) / vueltas * (len(P) - 1) * 0.999)
            if i >= j:
                C.banda(h, ("VUELTA 1: UN AÑO", "VUELTA 2: SEIS MESES", "VUELTA 3: TRES MESES", "VUELTA 4: UN MES",
                             "VUELTA 5: UNA SEMANA")[k], 1560, 260 + k * 96, 40, t, -99, claro=(k == 4), sem=30 + k)
        PR.caja_negra(h, cx, cy + 84, 0.32, 1.0, t * 3, sem=60, cable=False)
        h.camara(1.0, W / 2, H / 2, 0.0)
        C.banda(h, "CADA VUELTA, MÁS CORTA", 960, 1010, 64, t, self.t_corta - 0.5, sem=5)
        h.ambiente[:] = 0.55
        N.motas(h, t, n=100, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.14, vel=14, y0=0, y1=1080, sube=False), bloom=0.6)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        t0 = self.t0
        self.ev(t0, "cafeteria_amb", 0.5, 0.0, dur=self.t_pero - t0)
        for k in range(4):
            self.ev(t0 + 0.6 + k * 1.1, "servo", 0.5, -0.3)
        self.ev(self.t_equiv - 0.1, "taza", 0.9, 0.2)
        self.ev(self.t_equiv + 0.2, "cafe_sirve", 0.6, 0.3)
        self.ev(self.t_torpes, "sello_golpe", 0.8, 0.3)
        self.ev(self.t_caro - 0.2, "caja_registradora", 0.7, 0.3)
        self.ev(self.t_pero - 0.35, "barrido_aire", 0.6, 0.0, dur=0.7)
        self.ev(self.t_pero, "zumbido_servidores", 0.7, 0.0, dur=self.t_esa - self.t_pero)
        self.ev(self.t_usa, "datos", 0.5, 0.0, dur=self.t_esa - self.t_usa)
        self.ev(self.t_codigo - 0.3, "crecer", 0.7, 0.2, dur=max(1.5, self.t_esa - self.t_codigo))
        self.ev(self.t_esa - 0.35, "barrido_aire", 0.6, 0.0, dur=0.7)
        for k, tk in enumerate((self.t_esa - 0.2, self.t_mejor - 0.3, self.t_otra - 0.1)):
            self.ev(tk + 0.3, "golpe_grave", 0.6 + 0.2 * k, -0.4 + 0.4 * k)
            self.ev(tk, "focos", 0.6, -0.4 + 0.4 * k)
        self.ev(self.t_cada - 0.2, "subida", 0.8, 0.0, dur=max(2.0, self.t1 - self.t_cada - 0.6))
        self.ev(self.t_cada, "engranajes", 0.5, 0.0, dur=self.t1 - self.t_cada - 0.5)
        self.ev(self.t1 - 0.8, "tinta_mancha", 0.6, 0.0, dur=0.9)
