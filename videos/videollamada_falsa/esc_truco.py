# -*- coding: utf-8 -*-
"""Escena 6 «truco»: la mesa de juntas con máscaras que flotan sobre las sillas (la sala de fantasmas); el corcho del detective
con la hipótesis de la policía (tres videos públicos unidos por hilos); la moviola: la película entra en la máquina y sale con una
voz pegada; la máscara hecha de datos que una mano le pone a una silueta; antes un actor frente al espejo, hoy una computadora."""
import math

import numpy as np

import comun as C
import mundos as MU
import noir as N
import props as PR
import props3 as P3
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from noir_pers import Frontal
from toon import Pista, elipse_, pulso, suave


def mascara(h, x, y, s, sem, tono=236, ang=0.0, datos=0.0, t=0.0):
    """Máscara lisa (óvalo con dos huecos y una ranura). datos 0..1: se cubre de cifras."""
    P = PR.rot(np.array(suave([(-78, -60), (-60, -112), (0, -130), (60, -112), (78, -60), (70, 30), (40, 100), (0, 124), (-40, 100),
                               (-70, 30)], 5)) * s + (x, y), ang, np.array([x, y]))
    h.pieza(P, tono, sem, w=6 * s, luz=(-0.3, -1), d=16 * s, trama=0.4, rim=0, sombra=0.5)
    for sx in (-1, 1):
        e = PR.rot(np.array(elipse_(sx * 32, -30, 20, 11, n=16)) * s + (x, y), ang, np.array([x, y]))
        h.pieza(e, 6, sem + 2 + sx, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False, jit=0)
    h.trazo(PR.rot(np.array([[-22.0, 60], [22, 60]]) * s + (x, y), ang, np.array([x, y])), 5 * s, sem + 5, jit=0.3)
    if datos > 0:
        r = np.random.default_rng(sem)
        for q in range(9):
            fila = "".join(r.choice(list("01"), 9 - abs(q - 4) // 2))
            yy = y + (-104 + q * 25) * s
            if abs(yy - (y - 30 * s)) < 16 * s:
                continue
            N.texto_maquina(h, fila, x, yy, 21 * s, t, -99, cps=1e9, tono=0.12, alfa=datos, centro=True, encuadrar=False)


def tarjeta_video(h, x, y, s, sem, etiqueta, t, ang=0.0):
    """Fotograma de video (silueta en un atril, botón de reproducir) como ficha del tablero."""
    c = np.array([x, y])
    h.pieza(PR.rot(C.rect(x - 170 * s, y - 130 * s, 340 * s, 260 * s), ang, c), 226, sem, w=4, luz=(0.2, -1), d=8, trama=0, rim=0)
    h.pieza(PR.rot(C.rect(x - 150 * s, y - 112 * s, 300 * s, 170 * s), ang, c), 44, sem + 1, w=3, luz=(0, -1), d=2, sombra=0, trama=0.4)
    h.pieza(PR.rot(np.array(suave([(-30, 56), (-44, 0), (-22, -22), (-24, -60), (0, -78), (24, -60), (22, -22), (44, 0), (30, 56)], 3)) * s
                   + (x, y - 26 * s), ang, c), 150, sem + 2, w=3, luz=(0, -1), d=4, trama=0.3)
    h.pieza(PR.rot(C.rect(x - 60 * s, y + 20 * s, 120 * s, 38 * s), ang, c), 90, sem + 3, w=3, luz=(0, -1), d=3, trama=0.2)
    h.pieza(PR.rot(np.array([[x + 96 * s, y - 96 * s], [x + 136 * s, y - 76 * s], [x + 96 * s, y - 56 * s]]), ang, c), 236, sem + 4, w=2,
            luz=(0, -1), d=1, sombra=0, trama=0)
    N.texto_maquina(h, etiqueta, x, y + 92 * s, 30 * s, t, -99, cps=1e9, tono=0.05, centro=True, fuente=N.FUENTE_SELLO, encuadrar=False)


class Truco(BaseNoir):
    TR_SALIDA = ("barrido", 0.6)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.fig = Frontal(sem=330)
        self.actor = Frontal(sem=350)
        self.t_como = w("Cómo")
        self.t_fant = w("fantasmas")
        self.t_poli = w("La policía")
        self.t_hipo = w("hipótesis")
        self.t_desc = w("descargaron")
        self.t_conf = w("Conferencias")
        self.t_entr = w("entrevistas")
        self.t_pres = w("presentaciones")
        self.t_ycon = w("Y con")
        self.t_voces = w("voces")
        self.t_decian = w("decían")
        self.t_aeso = w("A eso")
        self.t_deep = w("deepfake")
        self.t_mascara = w("máscara")
        self.t_ponerse = w("ponerse")
        self.t_antes = w("Antes")
        self.t_actor = w("actor")
        self.t_hoy = w("Hoy")
        self.t_compu = w("computadora")
        self.plano(t0, self.p_fantasmas)
        self.plano(self.t_poli - 0.35, self.p_corcho, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_ycon - 0.35, self.p_moviola, tr="empuje", dur=0.55, centro=(W * 0.5, H * 0.5))
        self.plano(self.t_aeso - 0.35, self.p_mascara, tr="humo", dur=0.7)
        self.plano(self.t_antes - 0.35, self.p_antes_hoy, tr="barrido", dur=0.6, dirx=-1)

    # ------------------------------------------------------------------ la sala de fantasmas
    def p_fantasmas(self, h, t, u):
        h.camara(1.0 + 0.035 * u, 960, 520 - 4 * u, 0.0)
        MU.sala_rueda().pegar(h, 1.0, oscuro=0.6)
        PR.mesa(h, 960, 960, ancho=1640, fondo=170, alto=280, tono=80, sem=30)
        xs = (240, 600, 960, 1320, 1680)
        for k, x in enumerate(xs):
            PR.silla(h, x, 700, s=1.25, d=1 if k < 3 else -1, tono=60, sem=40 + 3 * k)
            a = smooth(clamp01((t - self.t_como - 0.25 * k) / 0.8))
            if a <= 0:
                continue
            fy = 330 + 16 * math.sin(t * 1.3 + k * 1.7) + 60 * (1 - a)
            N.humo(h, t, x, fy + 250, k=1.2 * a, sem=k, ancho=2.6, hebras=5, viento=(8 * math.sin(k), -90))
            mascara(h, x, fy, 1.15, 60 + 8 * k, tono=236, ang=0.08 * math.sin(t * 0.9 + k))
            h.luz_radial(x, fy, 250, (0.9, 0.9, 0.9), k=0.9 * a)
        C.banda(h, "¿CÓMO SE FABRICA?", 960, 130, 70, t, self.t_como, claro=True, sem=5)
        h.ambiente[:] = 0.30
        h.luz_cono(960, -700, math.pi / 2, 0.75, 2000, (1.0, 1.0, 1.0), k=0.8, suave=0.6)
        N.motas(h, t, n=120, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.3, vel=14, y0=100, y1=1000))

    # ------------------------------------------------------------------ la hipótesis en el corcho
    def p_corcho(self, h, t, u):
        h.camara(1.0 + 0.02 * u, 960 + 8 * u, 540, -0.012)
        MU.corcho().pegar(h, 1.0, oscuro=0.85)
        c0 = np.array([960.0, 420.0])
        C.banda(h, "HIPÓTESIS DE LA POLICÍA DE HONG KONG", 960, 160, 50, t, self.t_poli - 0.1, claro=True, sem=6)
        for k, (fx_, fy_, an_) in enumerate(((300, 420, -0.12), (1640, 400, 0.1), (330, 640, 0.06), (1600, 610, -0.08))):
            tk = self.t_poli + 0.25 + 0.3 * k                        # las fotos de vigilancia que va clavando
            a = e_out(clamp01((t - tk) / 0.25))
            if a > 0:
                PR.foto(h, fx_, fy_ - 300 * (1 - a), s=1.15, ang=an_, sem=200 + 5 * k)
                P3.chincheta(h, fx_, fy_ - 86 - 300 * (1 - a), sem=220 + k)
                if a >= 1:
                    P3.hilo(h, np.array([fx_, fy_ - 86.0]), c0 + (0, -110), u=clamp01((t - tk - 0.25) / 0.4), sem=230 + k)
        c0 = np.array([960.0, 420.0])
        if t > self.t_hipo - 0.3:
            a = e_out(clamp01((t - self.t_hipo + 0.3) / 0.35))
            h.pieza(PR.rot(C.rect(c0[0] - 250, c0[1] - 110 * a, 500, 220 * a), 0.02, c0), 28, 20, w=5, luz=(0, -1), d=8, trama=0.3, rim=0.6)
            if a > 0.95:
                N.texto_maquina(h, "VIDEOS PÚBLICOS", c0[0], c0[1] - 40, 50, t, -99, cps=1e9, tono=0.96, centro=True, fuente=N.FUENTE_SELLO,
                                encuadrar=False)
                N.texto_maquina(h, "de los directivos", c0[0], c0[1] + 30, 36, t, self.t_desc + 0.3, cps=30, tono=0.9, centro=True,
                                encuadrar=False)
                P3.chincheta(h, c0[0], c0[1] - 110, sem=21)
        fichas = (("CONFERENCIAS", self.t_conf, (360, 800), -0.06), ("ENTREVISTAS", self.t_entr, (960, 840), 0.03),
                  ("PRESENTACIONES", self.t_pres, (1560, 800), 0.07))
        for k, (et, tk, (x, y), ang) in enumerate(fichas):
            a = e_out(clamp01((t - tk + 0.2) / 0.3))
            if a <= 0:
                continue
            P3.hilo(h, c0 + (0, 110), np.array([x, y - 150.0]), u=a, sem=30 + k)
            tarjeta_video(h, x, y + 400 * (1 - a), 1.0, 40 + 10 * k, et, t, ang)
            P3.chincheta(h, x, y - 128 + 400 * (1 - a), sem=70 + k)
            fl = pulso(t, tk + 0.5, 1.2, 1.0)                        # la flecha de descarga
            if fl > 0:
                yy = y - 300 + 60 * fl
                h.trazo(np.array([[x + 210, yy], [x + 210, yy + 90]]), 12, 80 + k, color=(240, 240, 240), jit=0.3, taper=(0, 0))
                h.trazo(np.array([[x + 180, yy + 60], [x + 210, yy + 96], [x + 240, yy + 60]]), 12, 84 + k, color=(240, 240, 240), jit=0.3,
                        taper=(0, 0))
        h.ambiente[:] = 0.36
        h.luz_cono(960, -600, math.pi / 2, 0.66, 2300, (1.4, 1.4, 1.4), suave=0.6)
        N.motas(h, t, n=70, k=0.5)
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ la moviola: imagen + voz falsa
    def p_moviola(self, h, t, u):
        h.camara(1.0 + 0.02 * u, 960, 540, 0.0)
        h.img[:] = 0.07
        # la película, que corre de izquierda a derecha por detrás de la máquina
        des = (t * 150) % 260
        h.pieza(C.rect(-100, 330, W + 200, 300), 20, 10, w=5, luz=(0, -1), d=6, trama=0.3, rim=0.4)
        for q in range(-1, 9):
            x = q * 260 + des - 60
            h.pieza(C.rect(x, 370, 220, 220), 160, 20 + (q % 9), w=3, luz=(0, -1), d=3, trama=0.2, sombra=0.3)
            h.pieza(np.array(suave([(x + 80, 590), (x + 66, 500), (x + 90, 480), (x + 88, 430), (x + 110, 412), (x + 132, 430), (x + 130, 480),
                                    (x + 154, 500), (x + 140, 590)], 3)), 50, 40 + (q % 9), w=3, luz=(0, -1), d=4, trama=0.3)
            for yy in (342, 606):
                for j in range(5):
                    h.pieza(C.rect(x + 10 + j * 46, yy, 22, 16), 180, 60 + j, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False, jit=0.2)
            if x > 1060:                                              # a la salida, cada fotograma lleva su onda de voz
                for j in range(12):
                    amp = 14 + 46 * abs(math.sin(t * (8 + j) + j + q))
                    bx = x + 24 + j * 15
                    h.trazo(np.array([[bx, 690 - amp / 2], [bx, 690 + amp / 2]]), 7, 300 + j, color=(240, 240, 240), jit=0, taper=(0, 0))
        # la máquina
        h.pieza(C.rect(700, 190, 520, 620), 48, 100, w=9, luz=(-0.3, -1), d=22, trama=0.6, rim=0.7)
        h.pieza(C.rect(750, 250, 420, 200), 14, 101, w=5, luz=(0, -1), d=4, trama=0)
        N.texto_maquina(h, "I A", 960, 350, 150, t, -99, cps=1e9, tono=0.96, centro=True, fuente=N.FUENTE_SELLO, track=14, encuadrar=False)
        for j in range(8):                                            # luces que corren
            on = 1.0 if int(t * 8) % 8 == j else 0.25
            led = C.rect(770 + j * 50, 500, 30, 30)
            h.pieza(led, 60 + 180 * on, 110 + j, w=3, luz=(0, -1), d=2, sombra=0, trama=0)
            if on > 0.5:
                h.emitir(led, 0.9)
        for j in range(3):
            h.pieza(elipse_(800 + j * 160, 680, 54, 54, n=24), 80, 120 + j, w=5, luz=(-0.3, -1), d=8, trama=0.3, rim=0.7)
            a = t * (2 + j)
            h.trazo(np.array([[800 + j * 160, 680], [800 + j * 160 + 44 * math.cos(a), 680 + 44 * math.sin(a)]]), 7, 124 + j, jit=0.2)
        C.banda(h, "VIDEO REAL", 330, 250, 56, t, -99, claro=True, sem=7)
        C.banda(h, "+ VOZ FALSA", 1590, 250, 56, t, self.t_voces, claro=True, sem=8)
        N.texto_maquina(h, "«Haz la transferencia.»", 1480, 850, 44, t, self.t_decian, cps=22, tono=0.96, centro=True, encuadrar=False)
        h.ambiente[:] = 0.62
        h.luz_radial(960, 480, 1500, (1.0, 1.0, 1.0), k=0.7)
        N.motas(h, t, n=60, k=0.5)
        return h.acabado(t, niebla=None, bloom=0.45)

    # ------------------------------------------------------------------ una máscara hecha de datos
    def p_mascara(self, h, t, u):
        h.camara(1.0 + 0.035 * u, 960, 540, 0.0)
        h.img[:] = 0.05
        s = 3.0
        self.fig.dibujar(h, dict(x=960, y=560 + 474 * s, s=s, luz=(0.0, -1.0), rim=0.7, pelo="calvo", traje=40, mira=0.0))
        h.pieza(elipse_(960, 560, 46 * s, 62 * s, n=30), 30, 20, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False)      # sin rostro
        pone = smooth(clamp01((t - self.t_ponerse + 0.9) / 0.8))
        mx, my = 1500 - 540 * pone, 430 + 130 * pone - 40 * math.sin(math.pi * pone)
        dat = smooth(clamp01((t - self.t_mascara) / 0.9))
        mascara(h, mx, my, 2.35 - 0.1 * pone, 30, tono=232, ang=0.25 * (1 - pone), datos=dat, t=t)
        if pone < 0.98:
            PR.mano(h, mx + 330, my + 80, s=1.5, ang=math.pi - 0.2 + 0.2 * pone, d=1, tono=140, sem=50, dedos=0.3, manga=30)
        C.banda(h, "DEEPFAKE", 480, 250, 110, t, self.t_deep, claro=True, sem=9)
        N.texto_maquina(h, "una máscara hecha de datos", 480, 400, 36, t, self.t_mascara, cps=24, tono=0.95, centro=True, encuadrar=False)
        h.ambiente[:] = 0.22
        h.luz_cono(1100, -500, math.pi / 2 + 0.1, 0.5, 1900, (1.6, 1.6, 1.6), suave=0.5)
        N.motas(h, t, n=90, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.18, vel=10, y0=-200, y1=900, sube=False), bloom=0.45)

    # ------------------------------------------------------------------ antes un actor; hoy, una computadora
    def p_antes_hoy(self, h, t, u):
        hoy = smooth(clamp01((t - self.t_hoy + 0.2) / 0.5))
        h.camara(1.5 - 0.5 * hoy + 0.02 * u, 470 + 490 * hoy, 520 + 20 * hoy, 0.0)             # centrado en el camerino; se abre al aparecer «hoy»
        h.img[:] = 0.06
        # ANTES: el camerino, el espejo con bombillas y el actor
        h.pieza(C.rect(120, 150, 700, 700), 30, 10, w=8, luz=(0, -1), d=14, trama=0.5, rim=0.6)
        h.pieza(C.rect(180, 210, 580, 580), 120, 11, w=4, luz=(0, -1), d=4, trama=0.2, sombra=0.2, grad=(60, 210, 790))
        s = 1.9
        self.actor.dibujar(h, dict(x=470, y=470 + 474 * s, s=s, luz=(0.0, -1.0), rim=0.7, pelo="rizado", traje=60, barba=True,
                                   mira=0.3 * math.sin(t * 1.1)))
        h.pieza(C.rect(100, 790, 740, 300), 6, 12, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False, jit=0)
        for q in range(16):
            lado = q // 4
            f = (q % 4 + 0.5) / 4
            bx, by = ((180 + 580 * f, 180), (790, 210 + 580 * f), (180 + 580 * f, 820), (150, 210 + 580 * f))[lado]
            k = (0.75 + 0.25 * math.sin(t * 6 + q * 2.1)) * (1 - 0.7 * hoy)
            b = elipse_(bx, by, 20, 20, n=14)
            h.pieza(b, 150 + 90 * k, 60 + q, w=3, luz=(0, -1), d=2, sombra=0, trama=0)
            h.emitir(b, 0.8 * k, blur=2)
            h.luz_radial(bx, by, 190, (0.8, 0.8, 0.8), k=0.5 * k)
        C.banda(h, "ANTES: UN ACTOR", 470, 960, 58, t, self.t_antes, claro=True, sem=10)
        h.luz_radial(470, 480, 620, (1.0, 1.0, 1.0), k=1.5 - 0.6 * hoy)
        # HOY: la computadora con los archivos de video
        if hoy > 0:
            x0, y0 = 1090, 300
            h.pieza(C.rect(x0, y0, 660, 420), 26, 100, w=8, luz=(0, -1), d=12, trama=0.4, rim=0.6)
            pan = C.rect(x0 + 30, y0 + 30, 600, 360)
            h.pieza(pan, 190, 101, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False, jit=0)
            for q in range(6):
                a = clamp01((t - self.t_hoy - 0.25 - 0.12 * q) / 0.2)
                if a <= 0:
                    continue
                fx, fy = x0 + 70 + (q % 3) * 190, y0 + 60 + (q // 3) * 160
                h.pieza(C.rect(fx, fy, 140 * a, 100), 60, 110 + q, w=3, luz=(0, -1), d=2, trama=0.2, sombra=0.2)
                h.pieza(np.array([[fx + 54, fy + 28], [fx + 96, fy + 50], [fx + 54, fy + 72]]), 230, 120 + q, w=0, luz=(0, -1), d=1, sombra=0,
                        trama=0, linea=False)
            h.pieza(np.array([[x0 - 70, y0 + 420], [x0 + 730, y0 + 420], [x0 + 800, y0 + 520], [x0 - 140, y0 + 520]]), 40, 130, w=7,
                    luz=(0, -1), d=10, trama=0.4, rim=0.6)
            C.teclado(h, x0 - 40, y0 + 432, 740, sem=140)
            C.luz_rect(h, pan, 1.1 * hoy, suave_=6)
            C.banda(h, "HOY: SUS VIDEOS Y UNA COMPUTADORA", 1420, 960, 44, t, self.t_hoy, claro=True, sem=11)
        h.ambiente[:] = 0.30
        N.motas(h, t, n=70, k=0.5)
        return h.acabado(t, niebla=None, bloom=0.5)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        self.ev(self.t0, "grave_inquietante", 0.7, 0.0, dur=self.t_poli - self.t0)
        for k in range(5):
            self.ev(self.t_como + 0.25 * k, "teremin", 0.35, -0.6 + 0.3 * k, dur=1.2)
        self.ev(self.t_poli - 0.35, "barrido_aire", 0.6, 0.3, dur=0.7)
        self.ev(self.t_hipo - 0.3, "sello_golpe", 0.8, 0.0)
        for tk in (self.t_desc - 0.3, self.t_conf - 0.2, self.t_entr - 0.2, self.t_pres - 0.2):
            self.ev(tk, "fotos", 0.7, 0.0)
            self.ev(tk + 0.25, "chincheta", 0.8, 0.0)
            self.ev(tk + 0.05, "hilo_tenso", 0.5, 0.0)
        self.ev(self.t_ycon - 0.35, "barrido_aire", 0.6, 0.0, dur=0.7)
        self.ev(self.t_ycon, "imprenta", 0.5, 0.0, dur=self.t_aeso - self.t_ycon)
        self.ev(self.t_voces, "datos", 0.6, 0.4, dur=2.0)
        self.ev(self.t_decian, "tecleo_rapido", 0.5, 0.4, dur=1.0)
        self.ev(self.t_aeso - 0.35, "sombra_crece", 0.7, 0.0, dur=3.0)
        self.ev(self.t_deep, "golpe_grave", 1.0, 0.0)
        self.ev(self.t_mascara, "datos", 0.5, 0.0, dur=1.2)
        self.ev(self.t_ponerse - 0.2, "pinza", 0.7, 0.0)
        self.ev(self.t_antes - 0.35, "barrido_aire", 0.6, -0.3, dur=0.7)
        self.ev(self.t_antes, "zumbido_foco", 0.5, -0.4, dur=2.5)
        self.ev(self.t_hoy - 0.2, "interruptor", 0.8, 0.4)
        self.ev(self.t_hoy + 0.25, "tecleo_rapido", 0.6, 0.4, dur=0.9)
        self.ev(self.t_compu, "sello_golpe", 0.7, 0.4)
