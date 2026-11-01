# -*- coding: utf-8 -*-
"""Escena 15 «desconexion» [bourbon]: un lápiz rojo corrige la «gramática» del listado… y se detiene · tras un cristal los
ingenieros miran con lupa un listado ilegible junto a una caja con candado · bajo la mesa Bob y Alice se dan la mano y se pasan
objetos mientras los ingenieros miran hacia otro lado · la directiva en sombra levanta las manos · se tira del enchufe: chispas y
los visores se apagan · recortes de prensa con chiste y risas en silueta · dos manos de lata se estrechan y el humano queda fuera."""
import math

import numpy as np

import comun as C
import mundos_4 as M
import mundos_base as B
import noir as N
import noir_color as NC
import props_s as P
import kit27 as K
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from noir_pers import Figura
from toon import elipse_, tubo

LINEAS = ("balls have zero to me to me to me", "to me to me to me to me to me", "i can i i everything else",
          "can can i i i everything", "i i i i i can i i i", "balls have zero to me to me")


class Desconexion(BaseNoir):
    TR_SALIDA = ("humo", 0.7)
    PAL = "bourbon"

    def armar(self):
        w = self.w
        t0 = self.t0
        self.ings = [Figura(sem=190 + i) for i in range(3)]
        self.t_gram = w("gramática")
        self.t_habian = w("Habían")
        self.t_imposible = w("imposible")
        self.t_espaldas = w("espaldas")
        self.t_directiva = w("directiva")
        self.t_decision = w("decisión")
        self.t_apagaron = w("Apagaron")
        self.t_desench = w("Desenchufe")
        self.t_anec = w("anécdota")
        self.t_nadie = w("Nadie")
        self.t_cuando = w("cuando dos")
        self.t_estorbo = w("estorbo")
        self.tb = [t0, self.t_imposible - 0.4, self.t_espaldas - 0.8, self.t_directiva - 0.3, self.t_apagaron - 0.35,
                   w("En 2017") - 0.15, self.t_cuando - 0.3]
        tb = self.tb
        self.plano(tb[0], self.p_lapiz, pal="bourbon")
        self.plano(tb[1], self.p_cristal, tr="barrido", dur=0.4, dirx=1, pal="sodio")
        self.plano(tb[2], self.p_bajo_mesa, tr="humo", dur=0.45, pal="bourbon")
        self.plano(tb[3], self.p_directiva, tr="tinta", dur=0.5, pal="medianoche")
        self.plano(tb[4], self.p_enchufe, tr="relampago", dur=0.3, pal="medianoche")
        self.plano(tb[5], self.p_recortes, tr="barrido", dur=0.4, dirx=-1, pal="bourbon")
        self.plano(tb[6], self.p_estorbo, tr="empuje", dur=0.45, centro=(960, 540), pal="medianoche")

    # ------------------------------------------------------------------ A. el lápiz rojo se detiene
    def _lapiz(self, h, x, y, s, ang):
        T = C.T_obj(x, y, ang, s)
        h.pieza(T(C.rect(-380, -17, 340, 34)), 100, 6700, w=4 * s, luz=(0.3, -1), d=8 * s, trama=0.3, rim=0.9, rampa="vino")
        h.pieza(T(C.rect(-380, -17, 34, 34)), 190, 6701, w=3 * s, luz=(0.3, -1), d=4, trama=0.2, rim=0.9, rampa="laton")
        h.pieza(T([(-42, -17), (0, 0), (-42, 17)]), 210, 6702, w=3 * s, luz=(0.3, -1), d=4, trama=0.2, rim=0.9, rampa="madera")
        h.pieza(T([(-12, -5), (0, 0), (-12, 5)]), 20, 6703, w=0, luz=(0.3, -1), d=1, sombra=0, trama=0, rim=0, rampa="piedra")

    def p_lapiz(self, h, t, u):
        tb = self.tb
        dur = tb[1] - tb[0]
        k = smooth(clamp01(u / dur))
        h.camara(1.15 + 0.1 * k, 960, 500 + 120 * k, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("madera", 6710), h, 1.0, rampa="madera")
        K.hoja(h, 960, 520, 1300, 1040, ang=-0.01, sem=6711, tono=205, renglones=0, s=1.0)
        N.texto_maquina(h, "REGISTRO DE NEGOCIACIÓN · 2017", 960, 70, 36, t, -99, cps=1e9, tono=0.1, centro=True, fuente=C.IMPACT, encuadrar=False)
        rojo = tuple(h.c(120, "lacre"))
        ts = self.t0 + 0.5
        tip = (400.0, 200.0)
        for j, ln in enumerate(LINEAS):
            y = 190 + j * 130
            N.texto_maquina(h, ln, 960, y, 54, t, -99, cps=1e9, tono=0.1, centro=True, encuadrar=False)
            tj = ts + j * 1.0
            f = clamp01((t - tj) / 0.85)
            if j >= 4 and t > self.t_habian:
                f = 0.0 if t > self.t_habian + 0.05 and tj > self.t_habian else f
            if f > 0:
                x0, x1 = 360, 1560
                xs = np.linspace(x0, x0 + (x1 - x0) * f, 14)
                ys = y + 40 + 6 * np.sin(xs * 0.05)
                h.trazo(np.stack([xs, ys], 1), 9, 6720 + j, color=rojo, jit=0.8, taper=(0.05, 0.05))
                if f < 1:
                    tip = (xs[-1], ys[-1])
        if t > self.t_habian:
            tip = (tip[0] + 6 * math.sin(t * 9), tip[1] - 22 * smooth(clamp01((t - self.t_habian) / 0.4)) + 4 * math.sin(t * 13))
        self._lapiz(h, tip[0], tip[1], 1.0, 0.55)
        h.luz_cono(960, -300, math.pi / 2, 0.8, 1500, h.pal["lampara"], k=1.0, suave=0.6)
        C.ambiente(h, 0.4)
        C.banda(h, "NO ERA UN ERROR DE GRAMÁTICA", 960, 1000, 50, t, self.t_gram - 0.4, sem=48, acento=True)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=191), bloom=0.5)

    # ------------------------------------------------------------------ B. tras el cristal
    def p_cristal(self, h, t, u):
        tb = self.tb
        dur = tb[2] - tb[1]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.12 * k, 900 + 100 * k, 560, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(M.sala_observacion(), h, 1.0, rampa="piedra", emis=1.0, col_emis=h.pal["lampara"])
        # los tres ingenieros, al otro lado de la luna, escrutan con lupa
        for i, (x, s_, d) in enumerate(((470, 0.9, 1), (940, 0.95, -1), (1420, 0.9, -1))):
            self.ings[i].dibujar(h, dict(x=x, y=700, s=s_, d=d, tono=70 + 12 * i, gafas=bool(i != 1), brazo=0.5 + 0.4 * math.sin(t * 1.6 + i),
                                         cabeza=0.1 * math.sin(t + i), luz=(0.4, -1), rim=1.0))
        # reflejos del cristal por delante
        for q in range(3):
            h.emitir(np.array([(260 + q * 520 + 40 * math.sin(t * 0.3), 0), (320 + q * 520, 0), (140 + q * 520, 640), (80 + q * 520, 640)], float),
                     0.05, col=h.pal["luna"], blur=8)
        # primer plano: listado ilegible, lupa y la caja con candado
        K.hoja(h, 560, 930, 560, 360, ang=-0.05, sem=6730, tono=205, renglones=0, s=1.0)
        for j, ln in enumerate(LINEAS[:3]):
            N.texto_maquina(h, ln, 560, 810 + j * 70, 28, t, -99, cps=1e9, tono=0.1, centro=True, encuadrar=False)
        lx = 560 + 120 * math.sin(t * 0.9)
        ly = 930 + 20 * math.sin(t * 1.4)
        h.anillo(elipse_(lx, ly, 110, 110, n=32), 12, 6731)
        h.pieza(C.rot(C.rect(lx + 96, ly + 90, 170, 26), 0.8, (lx + 96, ly + 90)), 60, 6732, w=4, luz=(0.3, -1), d=8, trama=0.3, rim=0.8, rampa="madera")
        h.pieza(elipse_(lx, ly, 104, 104, n=32), 220, 6733, w=0, luz=(0.3, -1), d=1, sombra=0, trama=0, rim=0, alfa=0.14, rampa="piedra", linea=False)
        P.caja(h, 1480, 1110, 1.5, sem=6740, rotulo="SIN AUDITAR", t=t, tono=130, ancho=260, alto=190, candado_=True)
        h.luz_cono(1480, -300, math.pi / 2 - 0.1, 0.4, 1500, h.pal["lampara"], k=1.2, suave=0.5)
        h.luz_radial(560, 760, 600, h.pal["lampara"], k=0.7)
        C.ambiente(h, 0.42)
        C.banda(h, "IMPOSIBLE DE AUDITAR", 960, 1000, 52, t, self.t_imposible, sem=49)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.08, sem=192), bloom=0.6)

    # ------------------------------------------------------------------ C. a espaldas de sus creadores
    def p_bajo_mesa(self, h, t, u):
        tb = self.tb
        dur = tb[3] - tb[2]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.1 * k, 960, 700, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(M.bajo_mesa(), h, 1.0, rampa="madera", oscuro=1.5)
        # las piernas de los ingenieros (zapatos hacia fuera: miran para otro lado)
        for x, d in ((160, -1), (1700, 1), (1860, 1), (60, -1)):
            for j, dx in enumerate((-50, 50)):
                h.pieza(tubo(np.array([[x + dx, 340], [x + dx + 4, 650], [x + dx, 950]], float), 76, 60), 30 + 8 * j, 6800 + int(x) % 50 + j,
                        w=5, luz=(0.4, -1), d=8, trama=0.4, rim=0.8)
                h.pieza(elipse_(x + dx + d * 40, 968, 70, 24, n=14), 14, 6810 + int(x) % 50 + j, w=4, luz=(0.4, -1), d=4, trama=0, rim=0.8)
        # Bob y Alice, a ras de suelo, se dan la mano y se pasan tratos
        va = e_out(clamp01((t - self.t_espaldas + 0.5) / 0.7))
        P.robot_mesa(h, 700, 1000, 1.25, t, sem=6820, nombre="BOB", d=1, brazo=0.12 + 0.31 * va, habla=0.4)
        P.robot_mesa(h, 1240, 1000, 1.25, t, sem=6821, nombre="ALICE", d=-1, brazo=0.12 + 0.31 * va, habla=0.4)
        for j, tipo in enumerate(("sombrero", "libro", "balon")):
            f = ((t - tb[2]) * 0.8 + j * 0.34) % 1.0
            P.objeto_trato(h, tipo, 840 + 240 * f, 990 - 36 * math.sin(f * math.pi), 0.8, sem=6830 + j * 4)
        # rendijas de luz de la mesa de arriba
        h.luz_cono(900, 350, math.pi / 2, 0.3, 700, h.pal["lampara"], k=0.9, suave=0.5)
        h.luz_radial(960, 720, 900, h.pal["lampara"], k=0.35)
        C.ambiente(h, 0.5)
        C.banda(h, "TRATOS A ESPALDAS DE SUS CREADORES", 960, 1020, 48, t, self.t_espaldas - 0.4, sem=50)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.1, sem=193), bloom=0.6)

    # ------------------------------------------------------------------ D. la directiva decide
    def p_directiva(self, h, t, u):
        tb = self.tb
        dur = tb[4] - tb[3]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.14 * k, 960, 640 + 40 * k, 0.0)
        h.rim_color(h.pal["luna"])
        NC.pegar(M.sala_juntas(), h, 1.0, rampa="madera", emis=1.0, col_emis=h.pal["luna"])
        # siluetas sentadas a ambos lados de la mesa
        for i, (x, s_) in enumerate(((600, 0.7), (780, 0.62), (1140, 0.62), (1320, 0.7))):
            K.persona(h, x, 880 + 30 * s_, s_, sem=6900 + i * 5, tono=18, bal=2 * math.sin(t * 0.7 + i), rim=0.9)
        # las manos que se alzan, una tras otra, sin caras
        for i, (x, y, s_, d) in enumerate(((330, 560, 0.9, 1), (700, 640, 0.75, 1), (1260, 640, 0.75, -1), (1600, 560, 0.9, -1), (960, 700, 0.6, 1))):
            ta = self.t_decision - 1.8 + 0.4 * i
            K.mano_alzada(h, x, y, s_, sube=clamp01((t - ta) / 0.5), sem=6910 + i * 9, d=d, manga=44 + 4 * i, bal=3 * math.sin(t * 1.2 + i))
        h.luz_cono(960, -300, math.pi / 2, 0.35, 1500, h.pal["luna"], k=0.9, suave=0.6)
        h.luz_radial(960, 300, 1000, h.pal["luna"], k=0.5)
        C.ambiente(h, 0.45)
        C.banda(h, "LA DIRECTIVA DE FACEBOOK", 960, 1000, 52, t, self.t_directiva, sem=51)
        N.motas(h, t, n=50, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.1, sem=194), bloom=0.6)

    # ------------------------------------------------------------------ E. desenchufe de emergencia
    def p_enchufe(self, h, t, u):
        tb = self.tb
        dur = tb[5] - tb[4]
        tp = self.t_desench - 0.05
        off = e_out(clamp01((t - tp) / 0.3))
        h.camara(1.0 + 0.1 * u / dur, 960, 540, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(B.superficie("hormigon", 6950), h, 1.0, rampa="piedra", oscuro=0.9)
        # los dos robots, a un lado, con el visor vivo hasta el tirón
        vis = 1.0 - clamp01((t - tp - 0.05) / 0.15)
        P.robot_mesa(h, 330, 1010, 1.0, t, sem=6960, nombre="BOB", d=1, visor=vis, brazo=0.2, habla=0.5 * vis)
        P.robot_mesa(h, 1620, 1010, 1.0, t, sem=6961, nombre="ALICE", d=-1, visor=vis, brazo=0.2, habla=0.5 * vis)
        pos = P.enchufe(h, 960, 640, 1.8, fuera=off, sem=6970, cable_a=(1700 - 300 * off, 80))
        if t >= tp:
            C.chispas(h, t, 960, 600, tp, dur=0.8, n=40, vel=600, sem=6971, col=(0.7, 0.9, 1.0), grav=900, abre=2.4)
            h.resplandor(960, 600, 360, 1.0 * math.exp(-(t - tp) * 5), col=(0.7, 0.9, 1.0))
        dx, dy = C.temblor(t, [(tp, 14)])
        h.luz_radial(960, 400, 1300, h.pal["verde"], k=0.7 * (1 - 0.9 * off))
        h.luz_cono(960, -300, math.pi / 2, 0.45, 1500, h.pal["luna"], k=0.9 * (1 - 0.7 * off), suave=0.6)
        C.ambiente(h, 0.5 - 0.3 * off)
        C.banda(h, "APAGARON EL SERVIDOR", 960, 1000, 54, t, self.t_apagaron, sem=52, acento=True)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.08, sem=195), bloom=0.8, flash=0.5 * math.exp(-(t - tp) * 9) if t >= tp else 0)

    # ------------------------------------------------------------------ F. «una anécdota simpática»
    def p_recortes(self, h, t, u):
        tb = self.tb
        dur = tb[6] - tb[5]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.08 * k, 960, 500, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("madera", 7000), h, 1.0, rampa="madera")
        tit = (("LOS ROBOTS INVENTAN SU PROPIO IDIOMA", "Hablan raro, pero ¡qué simpáticos!", 560, 420, -0.08),
               ("APAGAN DOS ROBOTS CHARLATANES", "Anécdota de laboratorio", 1360, 380, 0.06),
               ("¿HABLAN EN CLAVE? NO, SOLO BROMEAN", "Los expertos se ríen", 960, 640, -0.02))
        for i, (a, b, x, y, ang) in enumerate(tit):
            ta = self.t_anec - 0.4 + 0.9 * i
            P.periodico(h, t, ta, x, y, 0.8, a, sub=b, sem=7010 + i * 11, ang_fin=ang, dur=0.8, fecha="2017", lineas=7)
        # risas en silueta
        for i in range(7):
            x = 160 + i * 270
            K.persona(h, x, 1180 + 14 * (i % 2), 0.75, sem=7050 + i * 5, tono=14, bal=6 * math.sin(t * 9 + i * 1.7) * (1 if t > self.t_anec else 0.3),
                      brazo=0.0, sombrero=bool(i % 3 == 0), rim=0.7)
        h.luz_cono(960, -300, math.pi / 2, 0.8, 1500, h.pal["lampara"], k=1.3, suave=0.6)
        C.ambiente(h, 0.42)
        C.banda(h, "UNA ANÉCDOTA SIMPÁTICA", 960, 1010, 52, t, self.t_anec - 0.2, sem=53)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=196), bloom=0.5)

    # ------------------------------------------------------------------ G. el ser humano, un estorbo
    def p_estorbo(self, h, t, u):
        tb = self.tb
        dur = self.t1 - tb[6]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.16 * k, 960 + 60 * k, 540, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(B.superficie("hormigon", 7100), h, 1.0, rampa="piedra", oscuro=0.8)
        ap = e_out(clamp01((t - tb[6] - 0.3) / 1.0))
        # dos manos de lata se estrechan
        P.mano(h, 640 + 130 * ap, 560, 1.7, ang=0.0, pose="abierta", sem=7110, rampa="piedra", tono=150, manga="laton", manga_tono=120,
               largo_brazo=900, cierra=0.5)
        P.mano(h, 1380 - 130 * ap, 580, 1.7, ang=math.pi, pose="abierta", sem=7120, rampa="piedra", tono=150, manga="laton", manga_tono=120,
               largo_brazo=900, cierra=0.5)
        h.luz_radial(960, 560, 700, h.pal["verde"], k=0.9 * ap)
        # el humano, fuera de la luz
        bal = 3 * math.sin(t * 0.8)
        K.persona(h, 190, 1180, 1.7, sem=7130, tono=10, bal=bal, rim=0.5)
        # barrote que lo deja fuera
        for x in (420, 470):
            h.pieza(C.rect(x, 0, 18, 1080), 40, 7140 + x, w=3, luz=(0.4, -1), d=4, trama=0.2, rim=0.6, rampa="piedra")
        h.luz_cono(960, -300, math.pi / 2, 0.3, 1500, h.pal["verde"], k=0.9, suave=0.6)
        C.ambiente(h, 0.38)
        C.banda(h, "UN ESTORBO", 640, 930, 90, t, self.t_estorbo - 0.2, sem=54, acento=True)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.08, sem=197), bloom=0.8)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        tb = self.tb
        self.ev(tb[0] + 0.5, "lapiz", 0.5, 0.0, dur=3.8)
        self.ev(tb[1] + 0.2, "lupa", 0.3, 0.0)
        self.ev(tb[2] + 0.3, "apreton", 0.4, 0.0)
        self.ev(tb[3] + 0.3, "zumbido_lampara", 0.25, 0.0, dur=3.0)
        self.ev(self.t_desench - 0.05, "desenchufa", 0.8, 0.0)
        self.ev(self.t_desench, "electricidad", 0.5, 0.0, dur=0.8)
        self.ev(self.t_desench + 0.2, "apagado_vela", 0.4, 0.0)
        self.ev(self.t_anec, "periodico_golpe", 0.4, 0.0)
        self.ev(self.t_anec + 0.9, "periodico_golpe", 0.4, 0.0)
        self.ev(self.t_anec + 1.8, "periodico_golpe", 0.4, 0.0)
        self.ev(tb[6] + 0.3, "apreton", 0.4, 0.0)
        self.ev(self.t_estorbo - 0.2, "grave_inquietante", 0.45, 0.0, dur=3.0)
