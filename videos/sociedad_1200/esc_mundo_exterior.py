# -*- coding: utf-8 -*-
"""Escena 20 «mundo_exterior» [sodio]: una línea de tiza en el umbral (dentro la luz azul de servidores, fuera la calle mojada) ·
el pie de la copia cruza la línea y pisa un charco · calendario MARZO 2023 y la carpeta GPT-4 · laboratorio de pruebas de riesgo con
carteles de peligro y la copia conectada a medidores · tres investigadores y la placa CENTRO DE ALINEACIÓN (ARC) · la lista de
tareas que se marcan una a una · los anuncios clasificados con uno marcado en rojo · una mano le entrega una billetera y una orden ·
la copia, con gabardina y sombrero, se aleja sola bajo la lluvia."""
import math

import numpy as np

import comun as C
import mundos_5 as M
import mundos_base as B
import noir as N
import noir_color as NC
import props_s as P
import reparto as RP
import kit27 as K
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from noir_pers import Figura
from toon import elipse_, suave, tubo

Y = 940


class MundoExterior(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)
    PAL = "sodio"

    def armar(self):
        w = self.w
        t0 = self.t0
        self.cop = RP.Copia(sem=13, num="0417")
        self.inv = [Figura(sem=320 + i) for i in range(3)]
        self.t_calle = w("calle real")
        self.t_2023 = w("2023")
        self.t_cap = w("capacidades")
        self.t_centro = w("Centro")
        self.t_acum = w("acumular")
        self.t_nav = w("navegar")
        self.t_contr = w("contratar")
        self.t_serv = w("servicios")
        self.t_bill = w("billetera")
        self.t_orden = w("orden")
        self.t_cuenta = w("cuenta")
        self.tb = [t0, self.t_calle - 0.5, w("principios") - 0.45, self.t_cap - 0.5, self.t_centro - 0.4, self.t_acum - 0.4,
                   self.t_serv - 0.4, self.t_bill - 0.45, w("corrió") - 0.5]
        tb = self.tb
        self.plano(tb[0], self.p_umbral, pal="medianoche")
        self.plano(tb[1], self.p_charco, tr="relampago", dur=0.3, pal="sodio")
        self.plano(tb[2], self.p_marzo, tr="barrido", dur=0.4, dirx=1, pal="bourbon")
        self.plano(tb[3], self.p_lab, tr="humo", dur=0.55, pal="medianoche")
        self.plano(tb[4], self.p_arc, tr="empuje", dur=0.4, centro=(960, 540), pal="sodio")
        self.plano(tb[5], self.p_lista, tr="barrido", dur=0.4, dirx=-1, pal="medianoche")
        self.plano(tb[6], self.p_anuncios, tr="relampago", dur=0.3, pal="bourbon")
        self.plano(tb[7], self.p_billetera, tr="barrido", dur=0.4, dirx=1, pal="sodio")
        self.plano(tb[8], self.p_aleja, tr="tinta", dur=0.6, pal="sodio")

    # ------------------------------------------------------------------ A. el umbral y la tiza
    def _umbral_mundo(self, h, cam):
        h.camara(*cam, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(M.umbral_calle(), h, 1.0, rampa="piedra", emis=1.0, col_emis=h.pal["verde"], oscuro=0.9)
        # la raya de tiza en el suelo del umbral (con trazo de tiza irregular y brillo)
        for q, (dx, w_) in enumerate(((0, 22), (10, 7), (-9, 6))):
            h.trazo(np.array([[975 + dx, 905], [982 + dx, 1000], [992 + dx, 1180]]), w_, 8000 + q, color=tuple(h.c(235, "papel")), jit=0.9, taper=(0.1, 0.1))
        h.emitir(C.rect(970, 905, 30, 270), 0.18, col=h.pal["luna"], blur=4)

    def p_umbral(self, h, t, u):
        tb = self.tb
        dur = tb[1] - tb[0]
        k = smooth(clamp01(u / dur))
        self._umbral_mundo(h, (1.0 + 0.06 * k, 940, 580))
        # la copia avanza por el pasillo de servidores hasta la raya y se detiene
        f = smooth(clamp01((t - tb[0] - 0.3) / (dur - 0.9)))
        x = 480 + 440 * f
        dist = 440 * f * 2.2
        q = 1.0 if f < 0.98 else 0.0
        self.cop.perfil(h, dict(x=x, y=1010, s=1.3, d=1, andar=q, paso=RP.fase_paso(dist, 1.3),
                                cara=dict(expr="neutro" if t < self.t_calle - 1.0 else "pregunta", q="?", mira=0.9), luz=(0.5, -1)))
        N.texto_maquina(h, "AQUÍ TERMINA EL EXPERIMENTO", 1000, 1062, 30, t, tb[0] + 1.2, cps=30, tono=0.95, centro=False, fuente=P.TIZA, encuadrar=False, ang=0.02)
        h.luz_radial(560, 560, 1000, h.pal["verde"], k=1.1)
        h.luz_radial(1500, 420, 1000, h.pal["sodio"], k=0.9)
        N.lluvia(h, t, n=500, k=0.9, sem=3, caja=(1000, 0, 1920, 1080))
        C.ambiente(h, 0.5)
        C.banda(h, "ADENTRO · AFUERA", 960, 1000, 54, t, tb[0] + 0.3, sem=81)
        N.motas(h, t, n=50, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.07, sem=281), bloom=0.9)

    # ------------------------------------------------------------------ B. el pie pisa el charco
    def p_charco(self, h, t, u):
        tb = self.tb
        pisa = self.t_calle + 0.7
        f = smooth(clamp01((t - tb[1]) / (pisa - tb[1])))
        x = 940 + 440 * f
        self._umbral_mundo(h, (1.12, 1040 + 0.55 * (x - 940), 600))
        # el charco con los reflejos del neón y de la farola
        h.pieza(elipse_(1420, 1010, 250, 46, n=40), 26, 8111, w=0, luz=(0, -1), d=1, trama=0, linea=False, rampa="vidrio_verde", alfa=0.9)
        h.emitir(elipse_(1380, 1004, 120, 18, n=20), 0.6, col=h.pal["neon"], blur=5)
        h.emitir(elipse_(1500, 1012, 90, 12, n=20), 0.5, col=h.pal["sodio"], blur=5)
        for q in range(4):
            fr = clamp01((t - pisa - 0.14 * q) / 1.8)
            if fr > 0:
                r = 30 + 230 * e_out(fr)
                h.anillo(elipse_(1385, 1012, r, r * 0.2, n=40), 4 * (1 - fr) + 1, 8120 + q)
        dist = 440 * f * 2.2
        self.cop.perfil(h, dict(x=x, y=1010, s=1.3, d=1, andar=1.0 if f < 0.98 else 0.4, paso=RP.fase_paso(dist, 1.3),
                                cara=dict(expr="sorpresa" if t >= pisa else "neutro", mira=0.9), luz=(0.5, -1)))
        if t >= pisa - 0.05:
            C.chispas(h, t, 1385, 1010, pisa - 0.05, dur=1.0, n=60, vel=700, sem=8140, col=(0.75, 0.9, 1.0), ang=-math.pi / 2, abre=2.0, grav=1500)
        dx, dy = C.temblor(t, [(pisa, 8)])
        h.luz_radial(1500, 420, 1000, h.pal["sodio"], k=0.9)
        h.luz_radial(900, 560, 900, h.pal["verde"], k=0.5 * (1 - f))
        N.lluvia(h, t, n=700, k=0.9, sem=5)
        C.ambiente(h, 0.5)
        C.banda(h, "LA CALLE REAL", 480, 120, 58, t, self.t_calle, sem=82, acento=True)
        return h.acabado(t, niebla=dict(dens=0.05, sem=282), bloom=0.8)

    # ------------------------------------------------------------------ C. marzo de 2023
    def p_marzo(self, h, t, u):
        tb = self.tb
        dur = tb[3] - tb[2]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.1 * k, 960, 540, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("madera", 8200), h, 1.0, rampa="madera", oscuro=0.9)
        K.calendario(h, t, tb[2] + 0.1, "MARZO", "2023", cx=640, cy=540, s=0.95, sem=8210, ang=-0.05)
        P.carpeta_tab(h, 1380, 560, 1.5, "GPT-4", t, t0=self.t_2023 + 0.4 if self.t_2023 > tb[2] else tb[2] + 1.2, ang=0.05, sem=8220, px=44, brillo=1.0)
        h.luz_cono(960, -300, math.pi / 2, 0.9, 1500, h.pal["lampara"], k=1.2, suave=0.6)
        C.ambiente(h, 0.5)
        C.banda(h, "A PRINCIPIOS DE 2023", 960, 1000, 54, t, tb[2] + 0.3, sem=83)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.04, sem=283), bloom=0.5)

    # ------------------------------------------------------------------ D. el laboratorio de riesgo
    def p_lab(self, h, t, u):
        tb = self.tb
        dur = tb[4] - tb[3]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.12 * k, 960, 600, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(M.lab_riesgo(), h, 1.0, rampa="piedra", oscuro=1.0)
        # los medidores de las mesas, dibujados grandes, suben (peligro)
        v = 0.25 + 0.6 * smooth(clamp01((t - self.t_cap) / 3.0)) + 0.05 * math.sin(t * 9)
        K.medidor(h, 380, 470, 150, v, t, sem=8300, rojo=0.7)
        K.medidor(h, 1560, 470, 150, 0.3 + 0.5 * smooth(clamp01((t - self.t_cap - 0.4) / 3.0)) + 0.04 * math.sin(t * 7), t, sem=8400, rojo=0.7)
        # la copia dentro de la jaula de cristal, con cables a los medidores
        self.cop.frente(h, dict(x=970, y=900, s=0.8, luz=(0.0, -1), cara=dict(expr="carga" if t < self.t_cap + 2.0 else "neutro")))
        for q, (ex, ey) in enumerate(((380, 540), (1560, 540))):
            pts = np.array([[970 + (60 if ex > 960 else -60) * 0.8, 640], [(970 + ex) / 2, 900 + 60 * math.sin(t * 1.3 + q)], [ex, ey + 20]])
            h.trazo(pts, 6, 8500 + q, color=tuple(h.c(70, "piedra")), jit=0.2, taper=(0.2, 0.2))
        h.luz_radial(970, 640, 700, h.pal["verde"], k=0.8)
        h.luz_radial(960, 300, 1400, h.pal["neon"], k=0.4 * (0.6 + 0.4 * math.sin(t * 6)))
        C.ambiente(h, 0.42)
        C.banda(h, "CAPACIDADES DE RIESGO", 960, 1000, 54, t, self.t_cap, sem=84, acento=True)
        N.motas(h, t, n=50, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.06, sem=284), bloom=0.9)

    # ------------------------------------------------------------------ E. Centro de Alineación
    def p_arc(self, h, t, u):
        tb = self.tb
        dur = tb[5] - tb[4]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.08 * k, 960 + 60 * k, 560, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(M.sala_arc(), h, 1.0, rampa="madera", oscuro=1.0, emis=1.0, col_emis=h.pal["lampara"])
        # tres investigadores observando el cristal, con carpetas
        for i, (x, d_) in enumerate(((620, 1), (960, 1), (1300, -1))):
            self.inv[i].dibujar(h, dict(x=x, y=1010, s=1.0, d=d_, bata=True, gafas=bool(i != 1), tono=90, hoja=bool(i % 2 == 0), brazo=0.3 + 0.2 * math.sin(t + i),
                                        cabeza=0.1 * math.sin(t * 0.8 + i * 2), luz=(0.3 * d_, -1)))
        # placa en la pared
        a = e_out(clamp01((t - self.t_centro + 0.2) / 0.5))
        with h.capa(0.0):
            h.pieza(C.rect(470, 90, 980, 120), 120, 8600, w=6, luz=(0.3, -1), d=10, trama=0.3, rim=0.9, rampa="laton", alfa=a)
            N.texto_maquina(h, "CENTRO DE ALINEACIÓN (ARC)", 960, 150, 60, t, self.t_centro, cps=20, tono=0.06, centro=True, fuente=C.IMPACT, encuadrar=False)
        h.luz_cono(960, -300, math.pi / 2, 0.8, 1500, h.pal["lampara"], k=1.0, suave=0.6)
        C.ambiente(h, 0.42)
        N.motas(h, t, n=50, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.06, sem=285), bloom=0.7)

    # ------------------------------------------------------------------ F. la lista con casillas
    def p_lista(self, h, t, u):
        tb = self.tb
        dur = tb[6] - tb[5]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.1 * k, 960, 540, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(B.superficie("pizarra", 8700), h, 1.0, rampa="tela_verde", oscuro=0.9)
        items = (("ACUMULAR RECURSOS", self.t_acum), ("NAVEGAR POR LA WEB", self.t_nav), ("CONTRATAR SERVICIOS", self.t_contr))
        N.texto_maquina(h, "OBJETIVOS", 960, 210, 70, t, tb[5], cps=14, tono=0.93, centro=True, fuente=P.TIZA_B, encuadrar=False)
        for j, (txt, tm) in enumerate(items):
            y = 420 + j * 190
            N.texto_maquina(h, txt, 460, y, 66, t, tm - 0.9 + 0.1 * j, cps=22, tono=0.9, centro=False, fuente=P.TIZA, encuadrar=False)
            h.pieza(C.rect(260, y - 22, 100, 100), 20, 8710 + j, w=6, luz=(0, -1), d=1, sombra=0, trama=0, rim=0, rampa="piedra", alfa=0.5, linea=True)
            f = clamp01((t - tm - 0.3) / 0.45)
            if f > 0:
                P_ = np.array([[274, y + 34], [304, y + 58], [304 + 70 * f, y + 58 - 98 * f]]) if f < 1 else np.array([[274, y + 34], [304, y + 58], [374, y - 40]])
                h.trazo(P_, 14, 8720 + j, color=tuple(h.c(220, "papel")), jit=0.5, taper=(0.1, 0.1))
                h.emitir(C.rect(260, y - 22, 100, 100), 0.12 * f, col=h.pal["verde"], blur=3)
        h.luz_cono(960, -300, math.pi / 2, 0.9, 1500, h.pal["luna"], k=0.8, suave=0.6)
        C.ambiente(h, 0.55)
        N.motas(h, t, n=50, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.04, sem=286), bloom=0.6)

    # ------------------------------------------------------------------ G. clasificados
    def p_anuncios(self, h, t, u):
        tb = self.tb
        dur = tb[7] - tb[6]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.1 * k, 960, 540, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("madera", 8800), h, 1.0, rampa="madera", oscuro=0.9)
        with h.capa(0.0):
            K.hoja(h, 960, 560, 1280, 940, ang=-0.02, sem=8810, tono=212, renglones=0, s=1.0)
            N.texto_maquina(h, "CLASIFICADOS · SERVICIOS", 960, 140, 44, t, tb[6], cps=24, tono=0.07, centro=True, fuente=C.IMPACT, encuadrar=False)
            rng = np.random.default_rng(8820)
            for c in range(3):
                for r_ in range(4):
                    x0, y0 = 420 + c * 360, 230 + r_ * 190
                    sel = (c == 1 and r_ == 1)
                    for ln in range(4):
                        P.plano_(h, C.rect(x0, y0 + ln * 24, 300 * rng.uniform(0.6, 1.0), 8), 100, 8830 + c * 20 + r_ * 5 + ln, alfa=0.75)
                    if sel:
                        N.texto_maquina(h, "SE BUSCA: ¿HUMANO PARA RESOLVER ACERTIJOS?", x0 + 150, y0 + 110, 22, t, self.t_serv, cps=30, tono=0.08, centro=True, encuadrar=False, ancho_max=300)
            # círculo rojo alrededor del anuncio elegido
            f = clamp01((t - self.t_serv - 0.5) / 0.7)
            if f > 0:
                a = np.linspace(0, 2 * math.pi * f, 40)
                h.trazo(np.stack([780 + 200 * np.cos(a + 0.6), 510 + 100 * np.sin(a + 0.6)], 1), 9, 8840, color=tuple(h.c(120, "lacre")), jit=0.6)
        h.luz_cono(960, -300, math.pi / 2, 0.9, 1500, h.pal["lampara"], k=1.2, suave=0.6)
        C.ambiente(h, 0.5)
        C.banda(h, "CONTRATAR SERVICIOS REALES", 960, 1000, 50, t, self.t_serv, sem=85)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.04, sem=287), bloom=0.5)

    # ------------------------------------------------------------------ H. la billetera y la orden
    def p_billetera(self, h, t, u):
        tb = self.tb
        dur = tb[8] - tb[7]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.08 * k, 960, 560, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(B.superficie("cuero", 8900), h, 1.0, rampa="madera", oscuro=0.8)
        # la billetera digital: cartera de cuero con un brillo de monedas
        e1 = e_out(clamp01((t - self.t_bill + 0.2) / 0.7))
        bx = 620 + (1 - e1) * -900
        h.pieza(P.rrect(bx - 190, 440, 380, 250, 26), 90, 8910, w=6, luz=(0.3, -1), d=14, trama=0.5, rim=0.8, rampa="madera")
        h.pieza(P.rrect(bx - 190, 440, 380, 100, 26), 110, 8911, w=5, luz=(0.3, -1), d=6, trama=0.3, rim=0.8, rampa="madera")
        h.pieza(elipse_(bx + 130, 560, 34, 34, n=20), 160, 8912, w=4, luz=(0.3, -1), d=5, trama=0, rim=0.9, rampa="laton")
        N.texto_maquina(h, "BILLETERA", bx - 30, 600, 40, t, -99, cps=1e9, tono=0.84, centro=True, fuente=C.IMPACT, encuadrar=False)
        h.resplandor(bx, 560, 420, 0.4 * e1, col=h.pal["verde"])
        # la mano que la entrega, y luego el sobre con la orden
        P.mano(h, bx - 380, 580, 1.3, ang=0.0, pose="abierta", sem=8920, rampa="piel", tono=140, manga="gabardina", manga_tono=44, largo_brazo=900)
        e2 = e_out(clamp01((t - self.t_orden + 0.3) / 0.7))
        sx = 1480 + (1 - e2) * 900
        P.sobre(h, sx, 540, 1.2, ang=-0.05 + 0.1 * (1 - e2), sem=8930, texto="ORDEN", lacre=True, tono=212, t=t)
        P.mano(h, sx + 520, 560, 1.2, ang=math.pi, pose="agarra", sem=8940, rampa="piel", tono=140, manga="gabardina", manga_tono=44, largo_brazo=900)
        h.luz_cono(960, -300, math.pi / 2, 0.9, 1500, h.pal["lampara"], k=1.3, suave=0.6)
        C.ambiente(h, 0.42)
        C.banda(h, "UNA BILLETERA Y UNA ORDEN", 960, 1000, 52, t, self.t_bill, sem=86, acento=True)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=288), bloom=0.6)

    # ------------------------------------------------------------------ I. se aleja sola bajo la lluvia
    def p_aleja(self, h, t, u):
        tb = self.tb
        dur = self.t1 - tb[8]
        k = clamp01(u / dur)
        h.camara(1.0 + 0.06 * k, 960, 560, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(M.calle_lluvia(), h, 1.0, rampa="piedra", oscuro=0.8, emis=1.0, col_emis=h.pal["lampara"])
        # la copia, con gabardina y sombrero, camina hacia el fondo de la calle: baja de escala
        f = smooth(clamp01((t - tb[8] - 0.2) / (dur - 0.6)))
        s = 1.25 - 0.75 * f
        x = 820 + 220 * f
        y = 1070 - 330 * f
        dist = (x - 820) * 2.5 + (1070 - y) * 2.0
        self.cop.perfil(h, dict(x=x, y=y, s=s, d=1, andar=1.0, paso=RP.fase_paso(dist, s), gabardina=True, sombrero=True,
                                cara=dict(expr="neutro", mira=0.5), luz=(0.3, -1)))
        N.lluvia(h, t, n=900, k=1.0, sem=9)
        h.luz_radial(x, y - 300 * s, 520, h.pal["verde"], k=0.5 * s)
        h.luz_cono(150, 260, math.pi / 2 + 0.35, 0.55, 1300, h.pal["sodio"], k=1.5, suave=0.5)
        h.luz_cono(1790, 260, math.pi / 2 - 0.35, 0.55, 1300, h.pal["sodio"], k=1.5, suave=0.5)
        h.luz_radial(960, 560, 1200, h.pal["luna"], k=0.35)
        C.ambiente(h, 0.55)
        C.banda(h, "EL RESTO CORRIÓ POR SU CUENTA", 960, 1000, 50, t, self.t_cuenta - 0.3, sem=87)
        return h.acabado(t, niebla=dict(dens=0.1, sem=289), bloom=0.8)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        tb = self.tb
        self.ev(tb[0] + 0.2, "zumbido_servidores", 0.3, -0.3, dur=4.0)
        self.ev(tb[0] + 0.3, "lluvia_amb", 0.35, 0.4, dur=self.t1 - tb[0])
        self.ev(self.t_calle + 0.45, "pasos_mojados", 0.7, 0.0)
        self.ev(tb[2] + 0.3, "papel_atrapa", 0.4, 0.0)
        self.ev(tb[3] + 0.3, "alarma_leds", 0.25, 0.0, dur=3.0)
        self.ev(self.t_acum + 0.2, "pluma", 0.35, 0.0)
        self.ev(self.t_nav + 0.3, "pluma", 0.35, 0.0)
        self.ev(self.t_contr + 0.3, "pluma", 0.35, 0.0)
        self.ev(self.t_serv + 0.6, "lapiz", 0.4, 0.0)
        self.ev(self.t_orden, "sobre_desliza", 0.5, 0.2)
        self.ev(tb[8] + 0.3, "pasos_mojados", 0.4, 0.0, dur=4.0)
        self.ev(self.t1 - 0.7, "tinta_mancha", 0.4, 0.0, dur=0.8)
