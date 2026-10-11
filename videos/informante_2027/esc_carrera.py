# -*- coding: utf-8 -*-
"""Escena 15 «carrera» (primer final): seis manos por seguir; la máquina preside la mesa y reparte informes (indispensable);
el pulso que vuelve y las barras que crecen; la fábrica: la fila de robots sale de la cinta; la paz entre máquinas (dos cajas
unidas por un cable bajo dos banderines) y la palanca con telarañas; mediados de 2030: la ciudad se apaga ventana a ventana;
la casa de la familia, a oscuras, y el columpio que se detiene."""
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
from comite import Comite, XF, jardin
from motor import H, W, clamp01, e_out, smooth
from toon import elipse_, pulso


class Carrera(BaseNoir):
    TR_SALIDA = ("tinta", 0.9)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.com = Comite()
        self.t_primer = w("Primer final")
        self.t_seis = w("Seis")
        self.t_maq = w("La máquina")
        self.t_lista = w("lista")
        self.t_nose = w("No se")
        self.t_indisp = w("indispensable")
        self.t_cura = w("Cura")
        self.t_hace = w("Hace crecer")
        self.t_levanta = w("Levanta")
        self.t_millon = w("millón")
        self.t_mes = w("mes", fin=True)
        self.t_ycuando = w("Y cuando")
        self.t_apagar = w("apagarla")
        self.t_firma = w("firma")
        self.t_paz = w("Una paz")
        self.t_amed = w("A mediados")
        self.t_deja = w("deja")
        self.t_elexp = w("El expediente")
        self.t_limp = w("limpieza")
        self.t_dura = w("Dura")
        self.plano(t0, self.p_seis)
        self.plano(self.t_maq - 0.35, self.p_preside, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_cura - 0.35, self.p_cura, tr="empuje", dur=0.55, centro=(W * 0.5, H * 0.5))
        self.plano(self.t_levanta - 0.35, self.p_fabrica, tr="barrido", dur=0.55, dirx=1)
        self.plano(self.t_ycuando - 0.35, self.p_paz, tr="humo", dur=0.7)
        self.plano(self.t_amed - 0.4, self.p_2030, tr="fundido", dur=0.9)
        self.plano(self.t_elexp - 0.4, self.p_casa, tr="fundido", dur=1.0)

    # ------------------------------------------------------------------ seis votan por seguir
    def p_seis(self, h, t, u):
        h.camara(1.06 + 0.014 * u, 960, 500, 0.0)
        alza = [0.0] * 10
        for q, k in enumerate([1, 6, 3, 8, 0, 9]):
            alza[k] = clamp01((t - (self.t_seis - 0.3 + q * 0.12)) / 0.35)
        self.com.dibujar(h, t, alza=alza)
        C.banda(h, "PRIMER FINAL", 960, 120, 100, t, self.t_primer, sem=5)
        C.banda(h, "SEIS VOTAN POR SEGUIR", 960, 250, 54, t, self.t_seis, claro=True, sem=6)
        h.ambiente[:] = 0.34
        N.motas(h, t, n=100, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.18, vel=8, y0=-200, y1=1000, sube=False), bloom=0.45)

    # ------------------------------------------------------------------ se vuelve indispensable
    def p_preside(self, h, t, u):
        h.camara(1.0 + 0.014 * u, 960, 510, 0.0)

        def centro():
            # la máquina, sobre la mesa, reparte un informe a cada silla
            tip = PR.caja_negra(h, 960, 790, 0.62, 1.0, t, sem=1300, cable=False)
            h.luz_radial(tip[0], tip[1], 600, (1.0, 1.0, 1.0), k=1.3)
            for k in range(5):
                a = e_out(clamp01((t - (self.t_nose + 0.2 + k * 0.22)) / 0.4))
                if a > 0:
                    x = 960 + (XF[k] - 960) * a
                    y = 770 + (778 - 770) * a
                    h.pieza(np.array([[x - 60, y - 22], [x + 60, y - 22], [x + 72, y + 24], [x - 72, y + 24]]), 232, 1320 + k, w=3,
                            luz=(0, -1), d=3, trama=0, rim=0)
                    for q in range(3):
                        K.plano_(h, C.rect(x - 44, y - 12 + q * 10, 88 - q * 14, 4), 90, 1330 + k * 4 + q)
        self.com.dibujar(h, t, mira=0.0, asiente=smooth(clamp01((t - self.t_indisp) / 0.5)), centro=centro, lamparas=0.6)
        C.banda(h, "MÁS LISTA QUE TODOS ELLOS", 960, 100, 54, t, self.t_lista - 0.6, sem=5)
        C.banda(h, "NO SE REBELA", 500, 1010, 60, t, self.t_nose, claro=True, sem=6)
        C.banda(h, "SE VUELVE INDISPENSABLE", 1360, 1010, 60, t, self.t_indisp - 0.5, sem=7)
        h.ambiente[:] = 0.3
        N.motas(h, t, n=100, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.18, vel=8, y0=-200, y1=1000, sube=False), bloom=0.5)

    # ------------------------------------------------------------------ cura enfermedades; hace crecer la economía
    def p_cura(self, h, t, u):
        h.camara(1.0 + 0.014 * u, 960, 540, 0.0)
        K.pared(h, 96, 40, paneles=10)
        # monitor de hospital: la línea plana recupera el pulso
        h.pieza(C.rect(110, 200, 780, 520), 20, 20, w=7, luz=(0, -1), d=10, trama=0.3, rim=0.7)
        K.plano_(h, C.rect(140, 230, 720, 460), 10, 21)
        vivo = smooth(clamp01((t - self.t_cura) / 0.5))
        fase = (t * 0.9) % 1.0
        xs = np.linspace(0, 1, 160)
        lat = np.exp(-((xs * 4 % 1.0) - 0.5) ** 2 / 0.0025) * 150 - np.exp(-((xs * 4 % 1.0) - 0.58) ** 2 / 0.002) * 50
        ys = 470 - lat * vivo
        n = max(2, int(160 * fase))
        h.trazo(np.stack([150 + 700 * xs[:n], ys[:n]], 1), 7, 22, color=(240, 240, 240), jit=0.3, taper=(0, 0))
        h.emitir(elipse_(150 + 700 * xs[n - 1], ys[n - 1], 10, 10, n=10), 1.2)
        h.pieza(C.rect(430, 110, 140, 44), 232, 30, w=4, luz=(0, -1), d=4, trama=0, rim=0)                 # cruz del hospital
        h.pieza(C.rect(478, 62, 44, 140), 232, 31, w=4, luz=(0, -1), d=4, trama=0, rim=0)
        C.luz_rect(h, C.rect(140, 230, 720, 460), 0.8, suave_=10)
        # barras de la economía
        cre = smooth(clamp01((t - self.t_hace) / 1.6))
        for k in range(6):
            al = (110 + 100 * k) * (0.25 + 0.75 * cre) * (1 + 0.03 * math.sin(t * 3 + k))
            h.pieza(C.rect(1060 + k * 130, 740 - al, 96, al), 210, 40 + k, w=4, luz=(0.2, -1), d=8, trama=0.4, rim=0.3)
        K.flecha(h, (1060, 640), (1820, 150), 12, 60, u=cre, curva=-70)
        h.trazo(np.array([[1030, 740], [1880, 740]]), 7, 70, color=(220, 220, 220), jit=0.3, taper=(0, 0))
        C.banda(h, "CURA ENFERMEDADES", 500, 820, 54, t, self.t_cura, claro=True, sem=5)
        C.banda(h, "HACE CRECER LA ECONOMÍA", 1440, 820, 54, t, self.t_hace, claro=True, sem=6)
        C.banda(h, "2028", 960, 990, 90, t, self.t_cura + 0.4, sem=7)
        h.ambiente[:] = 0.5
        h.luz_radial(1440, 460, 1000, (1.0, 1.0, 1.0), k=1.0)
        h.luz_radial(500, 460, 900, (1.0, 1.0, 1.0), k=0.6)
        N.motas(h, t, n=90, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.14, vel=10, y0=0, y1=1080, sube=False), bloom=0.5)

    # ------------------------------------------------------------------ un millón de robots al mes
    def p_fabrica(self, h, t, u):
        h.camara(1.0 + 0.012 * u, 960 + 8 * u, 530, 0.0)
        M27.fabrica().pegar(h, 1.0)
        v = 230.0
        for k in range(9):                                           # la fila sale de la cinta, uno tras otro
            x = ((k * 300 + t * v) % 2700) - 380
            K.robot(h, x, 842 + 3 * abs(math.sin(t * 6 + k)), 0.74, t + k, sem=100 + k * 40, brazo=0.0, tono=150)
        for k, bx in enumerate((300, 1100, 1700)):                   # brazos soldando por encima
            tip = PR4.brazo_robot(h, bx, 250, 2.5 + 0.3 * math.sin(t * 2.1 + k), 0.9 + 0.3 * math.sin(t * 3.3 + k * 2), 0.4,
                                  s=1.0, pinza=0.3, sem=500 + k * 30, tono=90)
            if int(t * 9 + k * 3) % 4 == 0:                          # chispas
                h.emitir(elipse_(tip[0], tip[1], 14, 14, n=10), 1.4, blur=3)
                h.luz_radial(tip[0], tip[1], 300, (1.0, 1.0, 1.0), k=1.4)
        n = int(1_000_000 * clamp01((t - self.t_millon + 0.6) / 1.4))
        C.banda(h, f"{n:,}".replace(",", " ") + " ROBOTS", 960, 110, 96, t, self.t_millon - 0.6, sem=5)
        C.banda(h, "CADA MES", 960, 225, 54, t, self.t_mes - 0.5, claro=True, sem=6)
        h.ambiente[:] = 0.5
        for k in range(5):
            h.luz_cono(160 + k * 420, -300, math.pi / 2, 0.36, 1500, (1.3, 1.3, 1.3), k=0.8, suave=0.6)
        N.motas(h, t, n=100, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.2, vel=14, y0=0, y1=1080, sube=False), bloom=0.5)

    # ------------------------------------------------------------------ una paz entre máquinas
    def p_paz(self, h, t, u):
        h.camara(1.0 + 0.012 * u, 960, 540, 0.0)
        K.pared(h, 80, 30, paneles=12)
        K.plano_(h, C.rect(-300, 930, W + 600, 400), 70, 8, grad=(16, 930, 1200))
        # la palanca, olvidada y con telarañas («ya nadie puede apagarla»)
        K.interruptor(h, 250, 430, 0.62, pos=0.0, sem=20, t=t)
        for q in range(8):
            a = -0.2 + q * 0.28
            h.trazo(np.array([[160, 270], [160 + 260 * math.cos(a), 270 + 260 * math.sin(a)]]), 1.6, 40 + q, color=(210, 210, 210),
                    alfa=0.6, jit=0.3, taper=(0, 0))
        for r_ in (90, 160, 230):
            h.trazo(np.array([[160 + r_ * math.cos(a), 270 + r_ * math.sin(a)] for a in np.linspace(-0.2, 1.8, 12)]), 1.4, 50 + r_,
                    color=(210, 210, 210), alfa=0.5, jit=0.3, taper=(0, 0))
        une = smooth(clamp01((t - self.t_firma + 0.2) / 0.9))
        t1 = PR.caja_negra(h, 760, 930, 1.1, 1.0, t, sem=60, cable=False)
        t2 = PR.caja_negra(h, 1500, 930, 1.1, 1.0, t + 1.3, sem=100, cable=False)
        for k, (x, b) in enumerate(((760, "franjas"), (1500, "estrella"))):                    # banderines sobre cada una
            h.trazo(np.array([[x - 90, 360], [x - 90, 190]]), 5, 140 + k, color=(60, 60, 60), jit=0.2, taper=(0, 0))
            on = 8 * math.sin(t * 3 + k)
            P = np.array([[x - 90, 196], [x + 50, 204 + on], [x + 50, 276 + on], [x - 90, 270]])
            h.pieza(P, 226, 150 + k, w=3, luz=(0.2, -1), d=4, trama=0, rim=0)
            if b == "franjas":
                for q in range(3):
                    K.plano_(h, np.array([[x - 90, 208 + q * 22], [x + 50, 216 + on + q * 22], [x + 50, 226 + on + q * 22], [x - 90, 218 + q * 22]]),
                             30, 160 + q)
            else:
                from esc_mentira import estrella
                estrella(h, x - 20, 236 + on * 0.5, 26, sem=170, tono=30)
        if une > 0:                                                  # el cable que las une: el tratado
            xs = np.linspace(875, 875 + 510 * une, 40)
            ys = 720 + 90 * np.sin(np.linspace(0, math.pi * une, 40))
            h.trazo(np.stack([xs, ys], 1), 14, 180, color=(26, 26, 26), jit=0.4, taper=(0, 0))
            if une >= 1:
                for q in range(4):
                    a = (t * 0.9 + q / 4) % 1.0
                    i = int(a * 39)
                    h.emitir(elipse_(xs[i], ys[i], 11, 11, n=10), 1.2, blur=2)
        C.banda(h, "YA NADIE PUEDE APAGARLA", 420, 90, 46, t, self.t_apagar - 0.6, sem=5)
        C.banda(h, "2029: FIRMA LA PAZ CON SU RIVAL", 1140, 90, 46, t, self.t_firma, claro=True, sem=6)
        C.banda(h, "UNA PAZ ENTRE MÁQUINAS", 1130, 1010, 70, t, self.t_paz + 0.2, sem=7)
        h.ambiente[:] = 0.46
        for x in (760, 1500):
            h.luz_cono(x, -400, math.pi / 2, 0.24, 1800, (1.5, 1.5, 1.5), k=1.0, suave=0.5)
        h.luz_radial(250, 400, 500, (1.0, 1.0, 1.0), k=0.7)
        N.motas(h, t, n=100, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.18, vel=10, y0=0, y1=1080, sube=False), bloom=0.5)

    # ------------------------------------------------------------------ mediados de 2030
    def p_2030(self, h, t, u):
        h.camara(0.74 + 0.006 * u, 1010, 240 - 6 * u, 0.0)
        ap = smooth(clamp01((t - self.t_deja + 0.3) / 2.2))          # la ciudad se apaga
        MU.cielo().pegar(h, 0.05, dx=-(t * 4.0) % 300)
        MU.lejos().pegar(h, 0.3, bruma=0.55, tono_bruma=0.34, emis=1.0 - ap)
        MU.medio().pegar(h, 0.6, bruma=0.2, tono_bruma=0.34, emis=max(0.0, 1.0 - 1.3 * ap))
        h.ambiente[:] = 1.15 - 0.45 * ap
        N.lluvia(h, t, n=500, vel=1500, k=0.7 * (1 - ap))
        h.camara(1.0, W / 2, H / 2, 0.0)
        C.banda(h, "MEDIADOS DE 2030", 960, 150, 96, t, self.t_amed + 0.1, sem=5)
        C.banda(h, "DEJA DE NECESITARNOS", 960, 290, 60, t, self.t_deja, claro=True, sem=6)
        return h.acabado(t, niebla=dict(dens=0.26, y0=200, y1=1000, vel=18), bloom=0.5)

    # ------------------------------------------------------------------ una limpieza: dura unas horas
    def p_casa(self, h, t, u):
        h.camara(1.0 + 0.016 * u, 960 + 14 * u, 560, 0.0)
        MU.cielo().pegar(h, 0.05, dx=-(t * 3.0) % 300)
        MU.lejos().pegar(h, 0.3, bruma=0.6, tono_bruma=0.30, emis=0.0)
        amp = 0.22 * math.exp(-max(0.0, t - self.t_elexp) * 0.32)    # el columpio se va deteniendo
        jardin(h, t, fr=0.0, amp=amp, luz_v=0.0)
        C.banda(h, "NO ES UNA GUERRA", 500, 110, 54, t, self.t_elexp + 0.6, sem=5)
        C.banda(h, "DURA UNAS HORAS", 1400, 110, 64, t, self.t_dura, claro=True, sem=6)
        h.ambiente[:] = 0.5
        h.luz_radial(1100, 500, 1500, (1.0, 1.0, 1.0), k=0.35)
        N.motas(h, t, n=60, k=0.4)
        return h.acabado(t, niebla=dict(dens=0.3, y0=300, y1=1080, vel=8), bloom=0.4, oscuro=1.0)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        t0 = self.t0
        self.ev(self.t_primer, "sello_golpe", 1.0, 0.0)
        self.ev(t0, "zumbido_lampara", 0.4, 0.0, dur=self.t_cura - t0)
        for q in range(0, 6, 2):
            self.ev(self.t_seis - 0.3 + q * 0.12, "papel_atrapa", 0.5, -0.5 + 0.3 * q)
        self.ev(self.t_maq - 0.35, "barrido_aire", 0.6, 0.0, dur=0.7)
        for k in range(5):
            self.ev(self.t_nose + 0.2 + k * 0.22, "sobre_desliza", 0.5, -0.6 + 0.3 * k)
        self.ev(self.t_indisp - 0.5, "golpe_grave", 0.9, 0.0)
        self.ev(self.t_cura, "reloj_pared", 0.5, -0.4, dur=self.t_levanta - self.t_cura)
        self.ev(self.t_hace, "subida", 0.6, 0.4, dur=1.6)
        self.ev(self.t_hace + 1.4, "caja_registradora", 0.7, 0.4)
        self.ev(self.t_levanta - 0.35, "obra", 0.7, 0.0, dur=self.t_ycuando - self.t_levanta)
        self.ev(self.t_levanta, "servo", 0.6, 0.0, dur=1.0)
        self.ev(self.t_levanta + 1.2, "servo", 0.6, 0.4, dur=1.0)
        self.ev(self.t_millon - 0.6, "sello_golpe", 1.0, 0.0)
        self.ev(self.t_ycuando - 0.2, "grave_inquietante", 0.7, 0.0, dur=3.0)
        self.ev(self.t_firma, "enchufa", 0.9, 0.0)
        self.ev(self.t_firma + 0.9, "electricidad", 0.6, 0.0, dur=1.2)
        self.ev(self.t_paz + 0.2, "golpe_grave", 1.0, 0.0)
        self.ev(self.t_amed - 0.4, "lluvia_lejana", 0.6, 0.0, dur=self.t_elexp - self.t_amed)
        self.ev(self.t_amed + 0.1, "sello_golpe", 0.9, 0.0)
        self.ev(self.t_deja - 0.3, "caida", 0.9, 0.0)
        self.ev(self.t_deja, "sombra_crece", 0.9, 0.0, dur=3.0)
        self.ev(self.t_elexp, "silencio_tono", 0.5, 0.0, dur=self.t1 - self.t_elexp - 0.5)
        self.ev(self.t_dura, "golpe_grave", 0.8, 0.0)
        self.ev(self.t1 - 0.9, "tinta_mancha", 0.6, 0.0, dur=0.9)
