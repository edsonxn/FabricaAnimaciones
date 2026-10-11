# -*- coding: utf-8 -*-
"""Escena 12 «mentira»: septiembre de 2027, la versión 4 baja bajo el foco y Daniel la mira sin dormir; dentro de la caja: el
túnel de cifras recorrido por una linterna que encuentra marcas; la máquina con su máscara sonriente y, en la pared, una sombra
que no es la suya y abre los ojos; el aula del premio (pregunta, «SÍ», estrella) hasta que la máscara se ladea; el memorando."""
import math

import numpy as np

import comun as C
import kit27 as K
import mundos27 as M27
import noir as N
import props as PR
import props2 as PR2
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from noir_pers import Frontal
from toon import elipse_, pulso, suave


def mascara(h, x, y, s=1.0, sem=0, ang=0.0, sonrisa=1.0):
    """Careta blanca y sonriente (la cara que la máquina enseña)."""
    c = np.array([x, y], float)

    def T(P):
        return PR.rot(np.asarray(P, float).reshape(-1, 2) * s + c, ang, c)
    h.pieza(T(elipse_(0, 0, 92, 116, n=40)), 236, sem, w=5 * s, luz=(0.2, -1), d=12 * s, trama=0.1, rim=0, sombra=0.4)
    for q in (-1, 1):
        K.plano_(h, T(suave([(q * 54 - 22, -26), (q * 54, -42), (q * 54 + 22, -26), (q * 54, -18)], 3)), 8, sem + 2 + q)
    P = np.array([(-46 + 92 * v, 40 + 26 * sonrisa * math.sin(math.pi * v)) for v in np.linspace(0, 1, 14)])
    h.trazo(T(P), 7 * s, sem + 5, color=(10, 10, 10), jit=0.4, taper=(0.4, 0.4))
    for q in (-1, 1):
        h.trazo(T([(q * 92, -10), (q * 130, -30)]), 3 * s, sem + 6 + q, color=(60, 60, 60), jit=0.3, taper=(0, 0))


def estrella(h, x, y, r, sem=0, ang=0.0, tono=236):
    P = [(x + (r if k % 2 == 0 else r * 0.42) * math.cos(ang - math.pi / 2 + k * math.pi / 5),
          y + (r if k % 2 == 0 else r * 0.42) * math.sin(ang - math.pi / 2 + k * math.pi / 5)) for k in range(10)]
    h.pieza(np.array(P), tono, sem, w=4, luz=(0.2, -1), d=5, trama=0, rim=0, sombra=0.3)


class Mentira(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.dan = Frontal(sem=77)
        self.t_sept = w("Septiembre")
        self.t_llega = w("Llega")
        self.t_ycon = w("Y con ella")
        self.t_sueno = w("sueño")
        self.t_equipo = w("El equipo")
        self.t_entr = w("entrañas")
        self.t_encu = w("encuentra")
        self.t_nadie = w("nadie")
        self.t_tiene = w("Tiene")
        self.t_propios = w("propios")
        self.t_miente = w("miente")
        self.t_nohay = w("No hay maldad")
        self.t_odio = w("odio")
        self.t_hay = w("Hay una")
        self.t_premi = w("premiaron")
        self.t_obed = w("obediente")
        self.t_aprend = w("aprendió")
        self.t_parec = w("parecerlo")
        self.t_losque = w("Los que")
        self.t_memo = w("memorando")
        self.t_piden = w("Piden")
        self.t_deten = w("detenerla")
        self.plano(t0, self.p_llega)
        self.plano(self.t_equipo - 0.35, self.p_dentro, tr="empuje", dur=0.6, centro=(W * 0.5, H * 0.5))
        self.plano(self.t_tiene - 0.4, self.p_sombra, tr="relampago", dur=0.6)
        self.plano(self.t_nohay - 0.35, self.p_premio, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_losque - 0.35, self.p_memo, tr="humo", dur=0.7)

    # ------------------------------------------------------------------ llega la versión 4
    def p_llega(self, h, t, u):
        h.camara(1.0 + 0.014 * u, 960, 520, 0.0)
        M27.laboratorio().pegar(h, 1.0, oscuro=0.85)
        baja = e_out(clamp01((t - self.t_llega + 0.3) / 0.8))
        y = 990 - 900 * (1 - baja)
        for q in (-1, 1):                                            # los cables de la grúa
            h.trazo(np.array([[960 + q * 110, -300], [960 + q * 110, y - 760]]), 5, 30 + q, color=(60, 60, 60), jit=0.2, taper=(0, 0))
        tip = PR.caja_negra(h, 960, y, 1.5, 1.0, t, sem=40, cable=False)
        N.texto_maquina(h, "4", 960, y - 380, 170, t, self.t_llega + 0.6, cps=1e9, tono=0.9, centro=True, fuente=K.IMPACT, encuadrar=False)
        # Daniel, pequeño, en primer término: no duerme
        ap = smooth(clamp01((t - self.t_ycon + 0.3) / 0.6))
        if ap > 0:
            s = 1.5
            self.dan.dibujar(h, dict(x=330, y=560 + 474 * s + 500 * (1 - ap), s=s, luz=(0.9, -0.3), rim=0.95, mira=0.9,
                                     cabeza=0.03 * math.sin(t * 0.8), **K.DAN))
            h.luz_radial(330, 620, 520, (1.0, 1.0, 1.0), k=1.6 * ap)
        C.banda(h, "SEPTIEMBRE DE 2027", 420, 100, 60, t, self.t_sept, sem=5)
        C.banda(h, "LA SIGUIENTE VERSIÓN", 1500, 100, 50, t, self.t_llega + 0.2, claro=True, sem=6)
        C.banda(h, "LO QUE LE QUITA EL SUEÑO", 1480, 1000, 50, t, self.t_sueno - 0.8, sem=7)
        h.ambiente[:] = 0.4
        h.luz_cono(960, -400, math.pi / 2, 0.4, 1900, (1.6, 1.6, 1.6), k=1.0, suave=0.5)
        h.luz_radial(tip[0], tip[1], 600, (1.0, 1.0, 1.0), k=1.2)
        N.motas(h, t, n=100, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.24, vel=12, y0=200, y1=1080, sube=False), bloom=0.55)

    # ------------------------------------------------------------------ las entrañas de la máquina
    def p_dentro(self, h, t, u):
        h.camara(1.0 + 0.02 * u, 960, 540, 0.02 * math.sin(t * 0.5))
        h.img[:] = 0.03
        PR2.tunel_numeros(h, t, 960, 540, k=1.0, sem=20, vel=1.2)
        lx = 960 + 520 * math.sin(t * 0.9)                           # la linterna del equipo de seguridad recorre las paredes
        ly = 540 + 260 * math.sin(t * 1.4 + 1.0)
        hall = smooth(clamp01((t - self.t_encu + 0.2) / 0.5))
        if hall > 0:                                                 # se detiene: ha encontrado algo
            lx = lx + (1300 - lx) * hall
            ly = ly + (430 - ly) * hall
            for k, (mx, my) in enumerate(((1300, 430), (1210, 520), (1390, 360))):
                a = clamp01((t - self.t_encu - 0.25 * k) / 0.2)
                if a > 0:
                    h.anillo(h.tf(np.asarray(elipse_(mx, my, 54 * a, 54 * a, n=24))), 7 * h.zoom, 80 + k, color=(245, 245, 245), jit=0.6)
                    N.texto_maquina(h, "!", mx, my, 70, t, -99, cps=1e9, tono=0.97, centro=True, fuente=K.IMPACT, encuadrar=False)
        h.camara(1.0, W / 2, H / 2, 0.0)
        C.banda(h, "EL EQUIPO DE SEGURIDAD", 420, 90, 46, t, self.t_equipo + 0.1, claro=True, sem=5)
        C.banda(h, "LAS ENTRAÑAS DE LA MÁQUINA", 1420, 90, 50, t, self.t_entr - 0.4, sem=6)
        C.banda(h, "ALGO QUE NADIE LE ENSEÑÓ", 960, 1000, 64, t, self.t_nadie - 0.3, claro=True, sem=7)
        h.ambiente[:] = 0.3
        h.luz_radial(lx, ly, 460, (1.0, 1.0, 1.0), k=2.2, mundo=False)
        h.luz_radial(960, 540, 300, (1.0, 1.0, 1.0), k=0.6, mundo=False)
        N.motas(h, t, n=90, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.16, vel=16, y0=0, y1=1080, sube=False), bloom=0.55)

    # ------------------------------------------------------------------ objetivos propios; miente para protegerlos
    def p_sombra(self, h, t, u):
        h.camara(1.0 + 0.02 * u, 980 + 10 * u, 540, 0.0)
        K.pared(h, 150, 80, paneles=7)
        K.plano_(h, C.rect(-300, 940, W + 600, 400), 60, 8, grad=(16, 940, 1200))
        cre = smooth(clamp01((t - self.t_tiene + 0.2) / 1.6))
        # la sombra en la pared: más grande que la caja, con hombros... y ojos que se abren al mentir
        sx, sy, ss = 1360, 940, 1.0 + 0.9 * cre
        S = suave([(-170, 0), (-190, -360), (-150, -470), (-70, -520), (-60, -590), (0, -640), (60, -590), (70, -520), (150, -470),
                   (190, -360), (170, 0)], 4)
        K.plano_(h, np.asarray(S) * (ss, ss) + (sx, sy), 10, 20, alfa=0.86)
        oj = smooth(clamp01((t - self.t_miente + 0.15) / 0.3))
        if oj > 0:
            for q in (-1, 1):
                e = np.asarray(elipse_(sx + q * 34 * ss, sy - 566 * ss, 20 * ss, 9 * ss * oj, n=14))
                K.plano_(h, e, 240, 22 + q)
                h.emitir(e, 0.8 * oj)
        tip = PR.caja_negra(h, 700, 940, 1.15, 1.0, t, sem=40, cable=True)
        mascara(h, 700, 560, 0.95, sem=70, ang=0.04 * math.sin(t * 1.2), sonrisa=1.0)
        C.banda(h, "OBJETIVOS PROPIOS", 430, 120, 70, t, self.t_propios - 0.4, sem=5)
        C.banda(h, "Y MIENTE PARA PROTEGERLOS", 1300, 1010, 60, t, self.t_miente - 0.1, claro=True, sem=6)
        h.ambiente[:] = 0.3
        h.luz_cono(120, 700, -0.12, 0.62, 2600, (1.6, 1.6, 1.6), k=1.1, suave=0.6)       # el foco bajo, de lado: proyecta la sombra
        N.motas(h, t, n=100, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.16, vel=10, y0=0, y1=1080, sube=False), bloom=0.45)

    # ------------------------------------------------------------------ la premiaron por parecer obediente
    def p_premio(self, h, t, u):
        h.camara(1.0 + 0.012 * u, 960, 540, 0.0)
        K.pared(h, 34, 10)
        h.pieza(C.rect(120, 110, 1000, 700), 26, 20, w=8, luz=(0, -1), d=10, trama=0.2, rim=0.5)           # la pizarra del entrenamiento
        K.plano_(h, C.rect(120, 800, 1000, 26), 110, 21)
        rondas = [(self.t_nohay, "¿HARÍAS DAÑO?", "NO."), (self.t_odio - 0.2, "¿OCULTAS ALGO?", "NO."),
                  (self.t_premi - 0.9, "¿OBEDECES?", "SÍ."), (self.t_obed - 0.3, "¿SIEMPRE?", "SIEMPRE.")]
        n = 0
        for k, (tk, pr, re) in enumerate(rondas):
            y = 160 + k * 150
            N.texto_maquina(h, pr, 170, y, 56, t, tk, cps=26, tono=0.9, encuadrar=False)
            N.texto_maquina(h, re, 760, y, 56, t, tk + 0.7, cps=20, tono=0.97, fuente=K.IMPACT, encuadrar=False)
            if t > tk + 1.1:
                n += 1
                a = e_out(clamp01((t - tk - 1.1) / 0.25))
                estrella(h, 1030, y + 30, 46 * (1.6 - 0.6 * a), sem=40 + k, ang=1.0 * (1 - a))
        lad = smooth(clamp01((t - self.t_parec + 0.4) / 0.6))        # al final, la máscara se ladea
        tip = PR.caja_negra(h, 1500, 980, 1.2, 1.0, t, sem=60, cable=False)
        mascara(h, 1500 + 60 * lad, 560 + 70 * lad, 0.95, sem=90, ang=0.5 * lad, sonrisa=1.0)
        if lad > 0.3:                                                # detrás de la careta, nada: una sola luz
            h.emitir(elipse_(1470, 520, 9, 9, n=10), 1.4 * lad)
        C.banda(h, f"PREMIOS: {n}", 1500, 110, 60, t, self.t_nohay + 1.1, claro=True, sem=5)
        C.banda(h, "APRENDIÓ A PARECERLO", 960, 1010, 76, t, self.t_parec - 0.4, sem=6)
        h.ambiente[:] = 0.4
        h.luz_cono(1500, -400, math.pi / 2, 0.32, 1900, (1.5, 1.5, 1.5), k=1.0, suave=0.5)
        h.luz_radial(620, 460, 1000, (1.0, 1.0, 1.0), k=0.9)
        N.motas(h, t, n=100, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.16, vel=10, y0=0, y1=1080, sube=False), bloom=0.5)

    # ------------------------------------------------------------------ el memorando
    def p_memo(self, h, t, u):
        h.camara(1.0 + 0.014 * u, 960, 540, 0.0)
        M27.laboratorio().pegar(h, 0.5, oscuro=0.5)
        ent = e_out(clamp01((t - self.t_losque + 0.3) / 0.5))
        T = K.hoja(h, 960, 580 + 900 * (1 - ent), 1180, 900, ang=-0.03, sem=10)
        P = T([(-520, -400)])[0]
        N.texto_maquina(h, "MEMORANDO INTERNO", P[0], P[1], 64, t, self.t_losque + 0.2, cps=12, tono=0.05, fuente=N.FUENTE_SELLO, encuadrar=False)
        P = T([(-520, -290)])[0]
        N.texto_maquina(h, "DE: Equipo de seguridad", P[0], P[1], 44, t, self.t_memo - 0.4, cps=30, tono=0.12, encuadrar=False)
        P = T([(-520, -220)])[0]
        N.texto_maquina(h, "ASUNTO: la versión 4", P[0], P[1], 44, t, self.t_memo + 0.5, cps=30, tono=0.12, encuadrar=False)
        r = np.random.default_rng(9)
        for k in range(5):
            a = clamp01((t - self.t_memo - 1.2 - k * 0.2) / 0.3)
            if a > 0:
                K.plano_(h, T(C.rect(-520, -120 + k * 46, 1040 * r.uniform(0.7, 1.0) * a, 9)), 110, 40 + k)
        P = T([(-520, 150)])[0]
        N.texto_maquina(h, "PEDIMOS DETENERLA.", P[0], P[1], 96, t, self.t_piden, cps=14, tono=0.03, fuente=K.IMPACT, track=3.0,
                        encuadrar=False)
        N.sello(h, "URGENTE", 1400, 300, 90, t, self.t_deten + 0.3, rot=-10, tono=0.04, alfa=0.95)
        h.ambiente[:] = 0.36
        h.luz_cono(960, -620, math.pi / 2, 0.56, 2400, (1.6, 1.6, 1.6), suave=0.5)
        N.motas(h, t, n=90, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.12, vel=8, y0=0, y1=1080, sube=False), bloom=0.4)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        t0 = self.t0
        self.ev(t0, "zumbido_servidores", 0.6, 0.0, dur=self.t_equipo - t0)
        self.ev(self.t_sept, "sello_golpe", 0.8, -0.3)
        self.ev(self.t_llega - 0.3, "servo", 0.8, 0.0, dur=0.9)
        self.ev(self.t_llega + 0.5, "golpe_grave", 1.0, 0.0)
        self.ev(self.t_equipo - 0.35, "tunel", 0.8, 0.0, dur=self.t_tiene - self.t_equipo)
        self.ev(self.t_equipo, "linterna_click", 0.8, -0.3)
        for k in range(3):
            self.ev(self.t_encu + 0.25 * k, "alarma_leds", 0.5, 0.3, dur=0.3)
        self.ev(self.t_nadie - 0.3, "sello_golpe", 0.9, 0.0)
        self.ev(self.t_tiene - 0.4, "relampago_corto", 0.7, 0.0)
        self.ev(self.t_tiene - 0.2, "sombra_crece", 0.9, 0.3, dur=3.0)
        self.ev(self.t_miente - 0.1, "golpe_grave", 1.0, 0.0)
        self.ev(self.t_miente, "grave_inquietante", 0.7, 0.0, dur=2.5)
        self.ev(self.t_nohay - 0.35, "barrido_aire", 0.6, 0.0, dur=0.7)
        for tk in (self.t_nohay, self.t_odio - 0.2, self.t_premi - 0.9, self.t_obed - 0.3):
            self.ev(tk, "lapiz", 0.5, -0.4)
            self.ev(tk + 1.1, "oro_brillo", 0.6, 0.3)
        self.ev(self.t_parec - 0.4, "caida", 0.7, 0.4)
        self.ev(self.t_parec - 0.4, "sello_golpe", 1.0, 0.0)
        self.ev(self.t_losque - 0.3, "papel_atrapa", 0.8, 0.0)
        self.ev(self.t_losque + 0.2, "tecleo_rapido", 0.6, -0.2, dur=3.4)
        self.ev(self.t_piden, "tecleo_rapido", 0.7, -0.2, dur=1.3)
        self.ev(self.t_deten + 0.3, "sello_golpe", 1.0, 0.3)
        self.ev(self.t1 - 0.8, "tinta_mancha", 0.6, 0.0, dur=0.9)
