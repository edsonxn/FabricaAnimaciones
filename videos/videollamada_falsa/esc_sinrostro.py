# -*- coding: utf-8 -*-
"""Escena 9 «sinrostro»: el detective bajo la lluvia, en primer plano, admite que no hay final feliz (tira la colilla en «No
puedo»); la celda vacía de la comisaría con el cartel de SE BUSCA sin cara y sin nombre; la rueda de reconocimiento: cuatro
figuras sin rostro que se ponen delante la máscara de otro."""
import math

import cv2
import numpy as np

import comun as C
import mundos as MU
import noir as N
import props as PR
from basen import BaseNoir
from esc_truco import mascara
from motor import H, W, clamp01, e_out, smooth
from noir_pers import Busto, Frontal
from toon import Pista, elipse_, pulso, suave

FAROL = (1020.0, 448.0)


class SinRostro(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        self.busto = Busto(sem=5)
        self.figs = [Frontal(sem=620 + 7 * k) for k in range(4)]
        self.t_megus = w("Me gustaría")
        self.t_atrap = w("atraparon")
        self.t_nopuedo = w("No puedo")
        self.t_hasta = w("Hasta donde")
        self.t_deten = w("detenidos")
        self.t_nombres = w("nombres")
        self.t_dinero = w("dinero")
        self.t_vuelto = w("vuelto", fin=True)
        self.t_esel = w("Es el crimen")
        self.t_ladr = w("ladrones")
        self.t_usaron = w("usaron")
        self.t_otros = w("otros", fin=True)
        self.plano(self.t0, self.p_cara)
        self.plano(self.t_hasta - 0.35, self.p_celda, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_esel - 0.35, self.p_rueda, tr="humo", dur=0.7)

    # ------------------------------------------------------------------ el detective, bajo la lluvia
    def p_cara(self, h, t, u):
        h.camara(1.5, 1150 + 26 * u, 470, 0.0)
        MU.cielo().pegar(h, 0.05, dx=-(t * 6.0) % 400)
        MU.lejos().pegar(h, 0.3, bruma=0.55, tono_bruma=0.40)
        MU.medio().pegar(h, 0.6, bruma=0.28, tono_bruma=0.40)
        MU.calle().pegar(h, 1.0)
        h.ambiente[:] = 0.78
        h.luz_cono(FAROL[0], FAROL[1], math.pi / 2 + 0.04, 0.46, 640, (1.5, 1.5, 1.5), suave=0.5)
        bg = cv2.resize(h.img, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
        h.img[:] = cv2.resize(cv2.GaussianBlur(bg, (0, 0), 3.0), (W, H), interpolation=cv2.INTER_LINEAR)
        if h._E is not None:
            e = cv2.resize(h._E, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
            h._E[:] = cv2.resize(cv2.GaussianBlur(e, (0, 0), 3.0), (W, H), interpolation=cv2.INTER_LINEAR) * 1.3
        L0 = h.mapa_gris()
        h.img *= cv2.resize(L0, (W, H))[..., None] * 0.55
        h.luces = []
        h.camara(1.0, W / 2, H / 2, 0.0)
        tp = self.t_nopuedo
        mano = smooth(clamp01((t - (tp - 0.75)) / 0.5))
        tira = smooth(clamp01((t - (tp + 0.25)) / 0.35))
        niega = 0.05 * math.sin((t - self.t_atrap) * 5.0) * pulso(t, self.t_atrap, 1.6, 1.0)
        br = pulso(t, self.t_megus - 0.9, 1.4, 1.0)
        p = dict(x=1130 + 20 * smooth(clamp01(u / 6.0)), y=500, s=1.0 + 0.05 * smooth(clamp01(u / 6.0)), d=-1, luz=(-0.8, -0.7), brasa=br,
                 mano=mano, tira=tira, boca=pulso(t, self.t_megus, 0.8, 0.6), arriba=0.25, rot=niega)
        if tira >= 1.0:
            p["cigarro"] = False
        self.busto.dibujar(h, p)
        h.ambiente[:] = 0.62
        h.luz_cono(170, -150, math.atan2(650, 950), 0.45, 1900, (1.0, 1.0, 1.0), suave=0.6)
        if tira < 1.0:
            tip = self.busto.punta(p)
            h.emitir(np.array([[tip[0] - 6, tip[1] - 6], [tip[0] + 6, tip[1] - 6], [tip[0] + 6, tip[1] + 6], [tip[0] - 6, tip[1] + 6]]),
                     0.9 + 0.5 * br)
            h.luz_radial(tip[0], tip[1], 160 + 260 * br, (0.7, 0.7, 0.7), k=0.6 + 1.3 * br)
            N.humo(h, t, tip[0], tip[1], k=1.0, ancho=2.2, viento=(-50, -150))
        C.banda(h, "¿LOS ATRAPARON?", 470, 260, 76, t, self.t_atrap, claro=True, sem=5)
        C.banda(h, "NO.", 470, 420, 150, t, self.t_nopuedo, sem=6)
        N.lluvia(h, t, n=360, capas=(0.85, 1.0), vel=1900, k=1.3)
        return h.acabado(t, niebla=None, bloom=0.45)

    # ------------------------------------------------------------------ la celda vacía
    def p_celda(self, h, t, u):
        h.camara(1.0 + 0.03 * u, 960 - 10 * u, 540, 0.0)
        MU.sala_interrogatorio().pegar(h, 1.0, oscuro=0.85, dx=-260)
        # el banco de la celda, vacío
        h.pieza(C.rect(260, 700, 760, 50), 70, 20, w=6, luz=(0, -1), d=10, trama=0.5, rim=0.6)
        for x in (300, 960):
            h.pieza(C.rect(x, 750, 30, 150), 50, 21 + x, w=5, luz=(0, -1), d=6, trama=0.4)
        # el cartel: SE BUSCA, sin cara ni nombre
        a = e_out(clamp01((t - self.t_nombres + 0.4) / 0.4))
        cx, cy = 1500, 470 + 700 * (1 - a)
        h.pieza(PR.rot(C.rect(cx - 250, cy - 360, 500, 720), 0.03, np.array([cx, cy])), 220, 40, w=5, luz=(0.2, -1), d=10, trama=0, rim=0)
        h.pieza(PR.rot(C.rect(cx - 170, cy - 220, 340, 330), 0.03, np.array([cx, cy])), 60, 41, w=4, luz=(0, -1), d=4, sombra=0, trama=0.5)
        h.pieza(np.array(suave([(cx - 120, cy + 110), (cx - 100, cy - 10), (cx - 50, cy - 40), (cx - 56, cy - 120), (cx, cy - 170),
                                (cx + 56, cy - 120), (cx + 50, cy - 40), (cx + 100, cy - 10), (cx + 120, cy + 110)], 4)), 14, 42, w=0,
                luz=(0, -1), d=1, sombra=0, trama=0, linea=False)
        if a > 0.97:
            N.texto_maquina(h, "SE BUSCA", cx, cy - 300, 76, t, -99, cps=1e9, tono=0.04, centro=True, fuente=N.FUENTE_SELLO, encuadrar=False)
            N.texto_maquina(h, "?", cx, cy - 70, 150, t, -99, cps=1e9, tono=0.9, centro=True, fuente="C:/Windows/Fonts/impact.ttf",
                            encuadrar=False)
            N.texto_maquina(h, "NOMBRE: ________", cx, cy + 190, 40, t, self.t_nombres, cps=24, tono=0.06, centro=True, encuadrar=False)
            N.texto_maquina(h, "RECOMPENSA: HK$ 200 M", cx, cy + 270, 32, t, self.t_dinero, cps=26, tono=0.06, centro=True, encuadrar=False)
        # los barrotes, en primer término, y la puerta de la celda entreabierta
        for k in range(15):
            x = 120 + k * 70
            h.pieza(C.rect(x, -40, 22, 1160), 34, 60 + k, w=4, luz=(0.6, -0.6), d=7, trama=0.4, rim=0.9)
        for y in (90, 930):
            h.pieza(C.rect(100, y, 1040, 30), 30, 80 + y, w=4, luz=(0.6, -0.6), d=7, trama=0.4, rim=0.9)
        C.banda(h, "SIN DETENIDOS", 640, 250, 84, t, self.t_deten - 0.1, claro=True, sem=7)
        C.banda(h, "SIN NOMBRES", 640, 400, 84, t, self.t_nombres, claro=True, sem=8)
        C.banda(h, "SIN EL DINERO", 640, 550, 84, t, self.t_dinero, claro=True, sem=9)
        h.ambiente[:] = 0.62
        h.luz_cono(640, -600, math.pi / 2, 0.55, 2200, (1.4, 1.4, 1.4), k=1.5, suave=0.6)
        h.luz_persiana(np.array([[150, 120], [1100, 60], [1250, 1000], [60, 1080]]), k=0.9, tipo="persiana", n=7, abierto=0.6)
        h.luz_radial(1500, 450, 800, (1.0, 1.0, 1.0), k=1.0 * a)
        N.motas(h, t, n=110, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.2, vel=8, y0=-200, y1=900, sube=False))

    # ------------------------------------------------------------------ ladrones sin rostro, con el rostro de otros
    def p_rueda(self, h, t, u):
        h.camara(1.0 + 0.03 * u, 830 + 14 * u, 440, 0.0)
        MU.sala_rueda().pegar(h, 1.0, oscuro=0.85)
        xs = (200, 620, 1040, 1460)
        looks = [dict(traje=40, alto=1.06), dict(traje=30, alto=0.98), dict(traje=46, ancho=1.08), dict(traje=34, alto=1.02)]
        for k, (F, x) in enumerate(zip(self.figs, xs)):
            p = dict(looks[k])
            p.update(x=x + 2 * math.sin(t * 0.9 + k), y=900, s=1.06, luz=(0.0, -1.0), rim=0.9, pelo="calvo", placa=True, mira=0.0)
            F.dibujar(h, p)
            al = p.get("alto", 1.0)
            fx, fy = p["x"], 900 - 474 * 1.06 * al
            h.pieza(elipse_(fx, fy, 40, 56, n=26), 150, 100 + k, w=4, luz=(0, -1), d=8, trama=0.3, sombra=0.5)       # sin rostro
            yp = 900 - 300 * 1.06 * al
            PR.placa(h, p["x"], yp, "¿?", -99, -100, s=0.62 * 1.06, sem=60 + k)
            F.manos_placa(h, p, yp)
            pone = smooth(clamp01((t - self.t_usaron + 0.2 - 0.15 * k) / 0.5))                      # la máscara de otro
            if pone > 0:
                mascara(h, fx, fy - 260 * (1 - pone), 0.62, 120 + 8 * k, tono=236, ang=0.3 * (1 - pone))
        C.banda(h, "LADRONES SIN ROSTRO", 960, 890, 70, t, self.t_ladr, sem=10)
        C.banda(h, "CON EL ROSTRO DE OTROS", 960, 1000, 46, t, self.t_usaron + 0.3, claro=True, sem=11)
        h.ambiente[:] = 0.32
        for x in xs:
            h.luz_cono(x, -540, math.pi / 2, 0.30, 1650, (1.5, 1.5, 1.5), k=0.9, suave=0.5)
        N.motas(h, t, n=110, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.18, vel=8, y0=-200, y1=900, sube=False), grano=0.08)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        self.ev(self.t0, "lluvia_amb", 0.8, 0.0, dur=self.t_hasta - self.t0)
        self.ev(self.t_megus - 0.9, "calada", 0.7, 0.2, dur=1.4)
        self.ev(self.t_atrap, "sello_golpe", 0.7, -0.4)
        self.ev(self.t_nopuedo, "golpe_grave", 1.0, -0.3)
        self.ev(self.t_nopuedo + 0.45, "colilla", 0.6, 0.2)
        self.ev(self.t_hasta - 0.35, "barrido_aire", 0.6, 0.3, dur=0.7)
        self.ev(self.t_hasta - 0.2, "puerta", 0.8, -0.3)
        for tk in (self.t_deten - 0.1, self.t_nombres, self.t_dinero):
            self.ev(tk, "sello_golpe", 0.9, -0.3)
        self.ev(self.t_nombres - 0.4, "fotos", 0.7, 0.5)
        self.ev(self.t_esel - 0.35, "sombra_crece", 0.7, 0.0, dur=3.0)
        self.ev(self.t_esel, "focos", 0.8, 0.0)
        for k in range(4):
            self.ev(self.t_usaron - 0.2 + 0.15 * k, "pinza", 0.6, -0.6 + 0.4 * k)
        self.ev(self.t_ladr, "golpe_grave", 1.0, 0.0)
        self.ev(self.t1 - 0.8, "tinta_mancha", 0.6, 0.0, dur=0.9)
