# -*- coding: utf-8 -*-
"""Escena 13 «caso_2017» [sodio → bourbon]: el detective en un reservado de bar con dos veteranos que le piden calma («incidente
aislado») · primer plano del veterano que lo despacha con la mano · «Mentira»: el puño cae sobre la barra, saltan los vasos y se
derrama el whisky · sótano de archivo: la linterna encuentra la caja «2017» · el calendario pasa de 2026 a 2017 · campus de Menlo
Park de noche con la ficha REAL de Yann LeCun · Bob y Alice, dos robots de lata bajo dos focos · la mesa de negociación: sombreros,
libros y balones que se pasan los robots."""
import math

import numpy as np

import comun as C
import mundos_4 as M
import mundos_base as B
import noir as N
import noir_color as NC
import noir_real as R
import props_s as P
import reparto as RP
import kit27 as K
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from noir_pers import Detective, Figura
from toon import elipse_


class Caso2017(BaseNoir):
    TR_SALIDA = ("humo", 0.7)
    PAL = "sodio"

    def armar(self):
        w = self.w
        t0 = self.t0
        self.det = Detective(sem=3)
        self.vet = [Figura(sem=151), Figura(sem=152)]
        self.t_incid = w("incidente")
        self.t_calmar = w("calmarme")
        self.t_mentira = w("Mentira")
        self.t_archivo = w("archivo")
        self.t_nueve = w("nueve")
        self.t_lab = w("laboratorios")
        self.t_menlo = w("Menlo")
        self.t_anio = w("Año", frase=2)
        self.t_bob = w("Bob")
        self.t_alice = w("Alice")
        self.t_mision = w("Su misión")
        self.t_somb = w("sombreros")
        self.t_libros = w("libros")
        self.t_balones = w("balones")
        self.tb = [t0, self.t_incid - 0.5, self.t_mentira - 0.15, self.t_archivo - 0.3, self.t_nueve - 0.2, self.t_lab - 0.3,
                   self.t_anio - 0.2, self.t_mision - 0.2]
        tb = self.tb
        self.plano(tb[0], self.p_bar, pal="sodio")
        self.plano(tb[1], self.p_veterano, tr="empuje", dur=0.35, centro=(1100, 520), pal="sodio")
        self.plano(tb[2], self.p_golpe, tr="relampago", dur=0.25, pal="sodio")
        self.plano(tb[3], self.p_sotano, tr="humo", dur=0.5, pal="sodio")
        self.plano(tb[4], self.p_calendario, tr="barrido", dur=0.4, dirx=-1, pal="bourbon")
        self.plano(tb[5], self.p_campus, tr="tinta", dur=0.5, pal="bourbon")
        self.plano(tb[6], self.p_robots, tr="barrido", dur=0.4, dirx=1, pal="bourbon")
        self.plano(tb[7], self.p_mesa, tr="empuje", dur=0.4, centro=(960, 700), pal="bourbon")

    # ------------------------------------------------------------------ A. el reservado
    def p_bar(self, h, t, u):
        tb = self.tb
        dur = tb[1] - tb[0]
        k = smooth(clamp01(u / dur))
        h.camara(1.38 + 0.1 * k, 840 + 120 * k, 610, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(M.bar_humo(), h, 1.0, rampa="madera", emis=1.0, col_emis=h.pal["neon"])
        # los veteranos hacen «calma» con las manos; el detective escucha con el cigarro
        calma = lambda i: 0.45 + 0.35 * math.sin(t * 2.6 + i * 1.7) * (1 if t > self.t_calmar - 1.6 else 0.3)
        self.vet[0].dibujar(h, dict(x=1180, y=1190, s=1.12, d=-1, tono=58, gafas=True, calvo=True, brazo=calma(0), cabeza=0.2,
                                    luz=(-0.5, -1)))
        self.vet[1].dibujar(h, dict(x=1480, y=1190, s=1.08, d=-1, tono=82, sombrero=True, brazo=calma(1), cabeza=-0.15, luz=(-0.5, -1)))
        pd = dict(x=520, y=1160, s=1.1, d=1, luz=(0.6, -1), fumar=0.4 + 0.3 * math.sin(t * 0.7), hombros=0.2)
        self.det.dibujar(h, pd)
        tip = self.det.punta_cigarro(pd)
        N.humo(h, t, tip[0], tip[1], k=1.0, ancho=1.4)
        # la mesa por delante (tapa las piernas) con tres vasos
        h.pieza(C.rect(120, 830, 1820, 56), 76, 5800, w=6, luz=(0.3, -1), d=14, trama=0.5, rim=0.9, rampa="madera")
        h.pieza(C.rect(160, 886, 1740, 420), 40, 5801, w=6, luz=(0.3, -1), d=14, trama=0.5, rim=0.5, rampa="madera")
        for i, x in enumerate((700, 980, 1360)):
            P.vaso(h, x, 836, 0.7, sem=5810 + i * 7, nivel=0.5 - 0.1 * i, t=t)
        h.luz_cono(160, -300, math.pi / 2 + 0.1, 0.45, 1500, h.pal["lampara"], k=1.2, suave=0.6)
        h.luz_cono(1000, -300, math.pi / 2, 0.5, 1500, h.pal["lampara"], k=1.0, suave=0.6)
        h.luz_radial(1200, -40, 900, h.pal["neon"], k=0.5)
        for x in (520, 1180, 1480):
            h.luz_radial(x, 640, 380, h.pal["lampara"], k=0.9)
        C.ambiente(h, 0.5)
        C.cinta(h, "BAR · MADRUGADA", 90, 120, 32, t, tb[0] + 0.6, sem=47)
        N.motas(h, t, n=50, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.14, sem=161, vel=8), bloom=0.7)

    # ------------------------------------------------------------------ B. «incidente aislado»
    def p_veterano(self, h, t, u):
        tb = self.tb
        dur = tb[2] - tb[1]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.1 * k, 1060 - 60 * k, 600, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(M.bar_humo(), h, 0.8, rampa="madera", emis=1.0, col_emis=h.pal["neon"], oscuro=0.8)
        # primer plano: el veterano calvo despacha el asunto con la mano
        des = math.sin(t * 5.0) * 0.5 + 0.5
        self.vet[0].dibujar(h, dict(x=1040, y=1950, s=3.1, d=-1, tono=58, gafas=True, calvo=True, brazo=0.35 + 0.5 * des, cabeza=0.1,
                                    luz=(-0.6, -1)))
        self.vet[1].dibujar(h, dict(x=380, y=1280, s=0.9, d=1, tono=40, sombrero=True, brazo=0.2, cabeza=0.2, luz=(0.5, -1)))
        h.luz_cono(1000, -300, math.pi / 2, 0.55, 1500, h.pal["lampara"], k=1.5, suave=0.6)
        h.luz_radial(1500, 300, 1000, h.pal["neon"], k=0.4)
        C.ambiente(h, 0.42)
        C.banda(h, "«UN INCIDENTE AISLADO»", 960, 1000, 54, t, self.t_incid - 0.3, sem=48)
        N.motas(h, t, n=50, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.16, sem=162, vel=8), bloom=0.6)

    # ------------------------------------------------------------------ C. «Mentira.»
    def p_golpe(self, h, t, u):
        tb = self.tb
        dur = tb[3] - tb[2]
        tg = self.t_mentira + 0.25
        h.camara(1.0 + 0.05 * u / dur, 960, 540, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(B.superficie("barra", 5820), h, 1.0, rampa="madera")
        a = clamp01((t - tg) / 0.5)
        dx, dy = C.temblor(t, [(tg, 26)])
        # derrame de whisky que crece desde el vaso central
        for q, (cx, cy, rr) in enumerate(((1060, 560, 150), (920, 700, 90), (1180, 660, 70))):
            r_ = rr * e_out(a) * (1 + 0.1 * math.sin(q * 2 + t * 3))
            if r_ > 2:
                h.emitir(elipse_(cx, cy, r_ * 1.4, r_, n=24), 0.45 * a, col=h.pal["sodio"], blur=3)
        # los tres vasos (vistos desde arriba) saltan con el golpe
        for i, (x, y) in enumerate(((620, 430), (1060, 560), (1480, 400))):
            salto = 90 * math.exp(-(t - tg) * 5) * abs(math.sin((t - tg) * 11)) if t > tg else 0.0
            sc = 1 + salto / 300
            h.pieza(elipse_(x + 24, y + 40 + salto * 0.3, 70 * sc, 60 * sc, n=24), 12, 5830 + i, w=0, luz=(0, -1), d=1, sombra=0, trama=0,
                    rim=0, alfa=0.55 * (1 - salto / 220))
            h.pieza(elipse_(x, y - salto, 66 * sc, 66 * sc, n=28), 200, 5831 + i, w=4, luz=(0.3, -1), d=6, sombra=0.2, trama=0, rim=0.9,
                    alfa=0.5, rampa="piedra")
            h.emitir(elipse_(x, y - salto, 50 * sc, 50 * sc, n=24), 0.55 * (1 if i == 1 else 0.6), col=h.pal["sodio"], blur=2)
        # el puño: baja desde arriba a la derecha y rebota
        caida = e_out(clamp01((t - (tg - 0.45)) / 0.4))
        reb = 0.04 * math.sin((t - tg) * 20) * math.exp(-(t - tg) * 6) if t > tg else 0.0
        P.mano(h, 1300 - 110 * (1 - caida) + 40 * reb, 330 + 120 * caida * 0.0 + 200 * (1 - caida) - 160 * 0, 2.0, ang=math.pi * 0.5 + 0.9,
               pose="agarra", sem=5840, rampa="piel", tono=140, manga="gabardina", manga_tono=60, largo_brazo=800)
        h.luz_cono(960, -300, math.pi / 2, 0.8, 1500, h.pal["lampara"], k=1.3, suave=0.6)
        C.ambiente(h, 0.4)
        C.banda(h, "MENTIRA", 960, 1000, 100, t, tg, sem=49, acento=True)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=163), bloom=0.7, flash=0.5 * math.exp(-(t - tg) * 12) if t > tg else 0)

    # ------------------------------------------------------------------ D. la caja «2017» del archivo
    def p_sotano(self, h, t, u):
        tb = self.tb
        dur = tb[4] - tb[3]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.2 * k, 960 - 120 + 200 * k, 560, 0.0)
        h.rim_color(h.pal["luna"])
        NC.pegar(M.archivo_sotano(), h, 1.0, rampa="piedra", emis=1.0, col_emis=h.pal["lampara"])
        # el detective con linterna a la izquierda alarga la mano hacia la caja
        q = smooth(clamp01((t - (self.t_archivo - 0.2)) / 0.9))
        pd = dict(x=430, y=1180, s=1.55, d=1, luz=(0.9, -1), hombros=0.2, sostener=0.0, rim=1.2)
        self.det.dibujar(h, pd)
        # la caja sale del estante y avanza hacia la cámara
        cx, cy = 1000 - 330 * q, 560 + 330 * q
        P.caja(h, cx, cy + 90 * q, 0.9 + 0.9 * q, sem=5850, rotulo="2017", t=t, tono=130, ancho=240, alto=170)
        if q > 0.05:
            C.polvo_cae(h, t, cx - 160, cx + 160, cy - 140, self.t_archivo, dur=2.2, n=70, sem=5851)
        # luz de la linterna sobre las cajas
        h.luz_cono(640, 640, 0.18 + 0.1 * math.sin(t * 1.5), 0.3, 900, h.pal["luna"], k=1.8, suave=0.5)
        h.luz_radial(cx, cy, 380, h.pal["lampara"], k=0.5 + 0.7 * q)
        h.luz_radial(430, 700, 420, h.pal["luna"], k=0.8)
        C.ambiente(h, 0.38)
        C.banda(h, "EL ARCHIVO TIENE ANTECEDENTES", 960, 130, 50, t, self.t_archivo, sem=50)
        N.motas(h, t, n=70, k=0.9)
        return h.acabado(t, niebla=dict(dens=0.12, sem=164), bloom=0.7)

    # ------------------------------------------------------------------ E. 2026 → 2017
    def p_calendario(self, h, t, u):
        tb = self.tb
        dur = tb[5] - tb[4]
        h.camara(1.0 + 0.1 * u / dur, 960, 540, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("cuero", 5860), h, 1.0, rampa="madera")
        # hojas de calendario que se arrancan hacia atrás: 2026 … 2017 (cada hoja cae encima de la anterior)
        n = 10
        paso = max(0.12, (dur - 0.5) / n)
        ia = int(clamp01((t - tb[4] - 0.1) / (paso * n)) * (n - 1) + 0.0001)
        for j in range(ia + 1):
            yr = 2026 - j
            ti = tb[4] + 0.1 + j * paso
            K.calendario(h, t, ti, "AÑO", str(yr), cx=960 + 30 * math.sin(j * 1.7), cy=520, s=0.82, sem=5870 + j, ang=-0.1 + 0.05 * j % 0.3,
                         px_num=250)
        h.luz_cono(960, -300, math.pi / 2, 0.7, 1500, h.pal["lampara"], k=1.4, suave=0.6)
        C.ambiente(h, 0.4)
        C.banda(h, "NUEVE AÑOS ATRÁS", 960, 1000, 60, t, self.t_nueve, sem=51)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=165), bloom=0.5)

    # ------------------------------------------------------------------ F. Menlo Park
    def p_campus(self, h, t, u):
        tb = self.tb
        dur = tb[6] - tb[5]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.06 * k, 900 + 100 * k, 600, 0.0)
        h.rim_color(h.pal["luna"])
        NC.pegar(M.menlo_park(), h, 1.0, rampa="piedra", emis=1.0, col_emis=h.pal["lampara"])
        h.luz_radial(1650, 80, 900, h.pal["luna"], k=0.5)
        C.ambiente(h, 0.45)
        with h.capa(0.0):
            R.retrato_noir(h, "yann_lecun", 1500, 560, 400, t, tb[5] + 0.5, rotulo="YANN LECUN", leyenda="IA DE FACEBOOK · 2017", ang=3.0,
                           fijacion="cinta", foco=(0.5, 0.35, 0.3))
        C.cinta(h, "MENLO PARK · CALIFORNIA", 90, 120, 32, t, tb[5] + 0.2, sem=47)
        C.banda(h, "LOS LABORATORIOS DE FACEBOOK", 960, 1000, 48, t, self.t_lab, sem=52)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.08, sem=166), bloom=0.7)

    # ------------------------------------------------------------------ G. Bob y Alice
    def p_robots(self, h, t, u):
        tb = self.tb
        dur = tb[7] - tb[6]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.12 * k, 960, 600 - 60 * k, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(M.laboratorio_2017(), h, 1.0, rampa="madera", emis=1.0, col_emis=h.pal["lampara"], oscuro=0.85)
        sbob = e_out(clamp01((t - self.t_bob) / 0.5))
        sali = e_out(clamp01((t - self.t_alice) / 0.5))
        hab_b = 0.8 if self.t_bob < t < self.t_bob + 0.7 else 0.0
        hab_a = 0.8 if self.t_alice < t < self.t_alice + 0.7 else 0.0
        P.robot_mesa(h, 640, 940, 1.35, t, sem=5880, nombre="BOB", d=1, brazo=0.4 * sbob + 0.15 * math.sin(t * 2), habla=hab_b)
        P.robot_mesa(h, 1320, 940, 1.35, t, sem=5881, nombre="ALICE", d=-1, brazo=0.4 * sali + 0.15 * math.sin(t * 2 + 1), habla=hab_a)
        for x, on in ((640, sbob), (1320, sali)):
            h.luz_cono(x, -300, math.pi / 2, 0.22, 1500, h.pal["lampara"], k=0.5 + 1.2 * on, suave=0.5)
        C.ambiente(h, 0.4)
        C.banda(h, "BOB", 640, 160, 58, t, self.t_bob, sem=53, acento=True)
        C.banda(h, "ALICE", 1320, 160, 58, t, self.t_alice, sem=54, acento=True)
        C.cinta(h, "AÑO 2017 · DOS AGENTES AUTÓNOMOS", 90, 990, 32, t, tb[6] + 0.3, sem=47)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=167), bloom=0.6)

    # ------------------------------------------------------------------ H. la mesa de negociación
    def p_mesa(self, h, t, u):
        tb = self.tb
        dur = self.t1 - tb[7]
        k = smooth(clamp01(u / dur))
        h.camara(1.1 + 0.1 * k, 960, 620, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(M.laboratorio_2017(), h, 0.9, rampa="madera", emis=1.0, col_emis=h.pal["lampara"], oscuro=0.8)
        # mesa
        h.pieza(C.rect(300, 830, 1320, 44), 70, 5890, w=6, luz=(0.3, -1), d=12, trama=0.5, rim=0.9, rampa="madera")
        h.pieza(C.rect(340, 874, 1240, 300), 38, 5891, w=6, luz=(0.3, -1), d=12, trama=0.5, rim=0.5, rampa="madera")
        # los dos robots negocian: el brazo de uno recibe, el del otro entrega
        va = 0.5 + 0.5 * math.sin(t * 2.2)
        P.robot_mesa(h, 380, 836, 1.1, t, sem=5895, nombre="BOB", d=1, brazo=va, habla=0.4)
        P.robot_mesa(h, 1540, 836, 1.1, t, sem=5896, nombre="ALICE", d=-1, brazo=1 - va, habla=0.4)
        # objetos que aparecen en cada palabra y viajan de un lado a otro
        for i, (tipo, ta) in enumerate((("sombrero", self.t_somb), ("libro", self.t_libros), ("balon", self.t_balones))):
            if t < ta:
                continue
            ent = e_out(clamp01((t - ta) / 0.3))
            f = 0.5 + 0.5 * math.sin((t - ta) * 1.6 + i * 1.3)
            x = 640 + (1280 - 640) * f * 1.0 + 0 * i
            if t - ta < 0.4:
                x = 960 + (i - 1) * 150
            y = 830 - 22 * math.sin(f * math.pi) * 3 - 160 * (1 - ent) - 6
            P.objeto_trato(h, tipo, x, y, 1.5, 5900 + i * 5, ang=0.2 * math.sin(t * 3 + i))
        h.luz_cono(960, -300, math.pi / 2, 0.8, 1500, h.pal["lampara"], k=1.3, suave=0.6)
        C.ambiente(h, 0.45)
        C.banda(h, "SOMBREROS · LIBROS · BALONES", 960, 1000, 52, t, self.t_somb - 0.3, sem=55)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=168), bloom=0.6)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        tb = self.tb
        self.ev(tb[0] + 0.2, "cafeteria_amb", 0.35, 0.0, dur=7.0)
        self.ev(self.t_mentira + 0.25, "golpe_grave", 0.9, 0.0)
        self.ev(self.t_mentira + 0.3, "taza", 0.45, 0.2)
        self.ev(tb[3] + 0.3, "zumbido_servidores", 0.25, 0.0, dur=3.0)
        self.ev(self.t_archivo + 0.5, "caida", 0.5, 0.0)
        self.ev(tb[4] + 0.1, "paginas", 0.5, 0.0, dur=2.6)
        self.ev(tb[6] + 0.4, "servo", 0.3, 0.0)
        self.ev(self.t_somb, "tecla", 0.3, 0.0)
        self.ev(self.t1 - 0.7, "tinta_mancha", 0.4, 0.0, dur=0.8)
