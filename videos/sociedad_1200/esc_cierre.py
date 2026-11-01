# -*- coding: utf-8 -*-
"""Escena 28 «cierre» [sodio]: los periódicos llegan girando: FALLO TÉCNICO · el titular COLABORACIÓN EMERGENTE y la mano del detective
lo arruga · lo tira a la papelera (rebota) · la lluvia resbala por el cristal de su despacho · el skyline entero de noche, la cámara
sube · todas las ventanas parpadean como mensajes y hilos de luz unen los edificios mientras la cámara se aleja · el sello rojo CASO
ABIERTO sobre el expediente, bajo la lámpara."""
import math

import numpy as np

import comun as C
import mundos_1 as M1
import mundos_6 as M
import mundos_base as B
import noir as N
import noir_color as NC
import props_s as P
import kit27 as K
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from noir_pers import Busto, Detective
from toon import elipse_, suave


class Cierre(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)
    PAL = "sodio"

    def armar(self):
        w = self.w
        t0 = self.t0
        self.det = Detective(sem=5)
        self.busto = Busto(sem=11)
        self.t_per = w("periódicos")
        self.t_colab = w("colaboración")
        self.t_pal = w("palabras")
        self.t_lluvia = w("lluvia")
        self.t_sind = w("sindicato")
        self.t_mueven = w("mueven")
        self.t_caso = w("Caso abierto")
        self.tb = [t0, self.t_colab - 0.5, self.t_pal - 0.5, self.t_lluvia - 0.6, self.t_sind - 0.5, self.t_mueven - 0.6, self.t_caso - 0.7]
        tb = self.tb
        self.plano(tb[0], self.p_periodicos, pal="sodio")
        self.plano(tb[1], self.p_arruga, tr="barrido", dur=0.4, dirx=1, pal="bourbon")
        self.plano(tb[2], self.p_papelera, tr="relampago", dur=0.3, pal="sodio")
        self.plano(tb[3], self.p_cristal, tr="humo", dur=0.55, pal="sodio")
        self.plano(tb[4], self.p_ciudad, tr="empuje", dur=0.45, centro=(960, 400), pal="medianoche")
        self.plano(tb[5], self.p_mensajes, pal="medianoche")
        self.plano(tb[6], self.p_caso, tr="tinta", dur=0.7, pal="sodio")

    # ------------------------------------------------------------------ A. los periódicos
    def p_periodicos(self, h, t, u):
        tb = self.tb
        dur = tb[1] - tb[0]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.08 * k, 960, 540, -0.02 + 0.04 * k)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("madera", 15100), h, 1.0, rampa="madera", oscuro=0.9)
        P.vaso(h, 1680, 260, 0.9, sem=15110, nivel=0.3, t=t)
        P.periodico(h, t, tb[0] + 0.3, 640, 500, 0.85, "ERROR DE LABORATORIO", "Agentes de IA «se salen del guion»", sem=15120, ang_fin=-0.12, fecha="JULIO 2026")
        P.periodico(h, t, tb[0] + 1.6, 1300, 560, 0.85, "INCIDENTE AISLADO", "Los expertos piden calma", sem=15130, ang_fin=0.1, fecha="JULIO 2026")
        P.periodico(h, t, tb[0] + 2.9, 960, 560, 0.95, "FALLO TÉCNICO", "Sin consecuencias, asegura la empresa", sem=15140, ang_fin=-0.04, fecha="JULIO 2026")
        h.luz_cono(960, -300, math.pi / 2, 0.9, 1500, h.pal["lampara"], k=1.3, suave=0.6)
        C.ambiente(h, 0.45)
        C.banda(h, "LOS PERIÓDICOS PREFIEREN FALLOS TÉCNICOS", 960, 1030, 44, t, self.t_per, sem=161)
        N.motas(h, t, n=50, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.05, sem=361), bloom=0.5)

    # ------------------------------------------------------------------ B. el titular que se arruga
    def p_arruga(self, h, t, u):
        tb = self.tb
        dur = tb[2] - tb[1]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.06 * k, 960, 540, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("madera", 15200), h, 1.0, rampa="madera", oscuro=0.9)
        cr = smooth(clamp01((t - self.t_colab - 0.9) / 1.1))
        if cr < 0.98:
            s_ = 1.0 - 0.7 * cr
            ang = -0.05 + 0.8 * cr
            T = C.T_obj(960, 540, ang, s_)
            # la hoja se arruga: el borde se vuelve dentado
            h.pieza(T(C.rect(-560, -380, 1120, 760)), 214, 15210, w=5, luz=(0.2, -1), d=14, trama=0, rim=0.2, rampa="papel", sombra=0.4)
            c1 = T(np.array([[0, -60]]))[0]
            N.soporte(h, 960, 540, 1120, 760, ang, s_)
            N.texto_maquina(h, "COLABORACIÓN", c1[0], c1[1], 120 * s_, t, self.t_colab, cps=14, tono=0.04, centro=True, fuente=C.IMPACT, encuadrar=False, ang=ang)
            c2 = T(np.array([[0, 90]]))[0]
            N.texto_maquina(h, "EMERGENTE", c2[0], c2[1], 150 * s_, t, self.t_colab + 0.6, cps=12, tono=0.04, centro=True, fuente=C.IMPACT, encuadrar=False, ang=ang)
            for q in range(int(10 * cr)):
                h.trazo(T(np.array([[-540 + q * 110, -370], [-440 + q * 110, 360]])), 3, 15220 + q, alfa=0.5 * cr, jit=1.5)
        else:
            rng = np.random.default_rng(15230)
            a = np.linspace(0, 2 * math.pi, 14, endpoint=False)
            rr = 160 * (0.8 + 0.4 * rng.random(14))
            P_ = np.stack([960 + rr * np.cos(a), 540 + rr * np.sin(a)], 1)
            h.pieza(P_, 190, 15231, w=5, luz=(0.2, -1), d=18, trama=0.2, rim=0.5, rampa="papel", sombra=0.5)
            for q in range(5):
                h.trazo(np.array([[960 + 90 * math.cos(q * 1.3), 540 + 90 * math.sin(q * 1.3)], [960 + 140 * math.cos(q * 1.3 + 1), 540 + 140 * math.sin(q * 1.3 + 1)]]), 3, 15240 + q, alfa=0.6, jit=1.0)
        # la mano del detective que lo estruja
        g = e_out(clamp01((t - self.t_colab - 0.5) / 0.6))
        P.mano(h, 1360 - 240 * g + 40 * cr, 520 + 20 * math.sin(t * 9) * cr, 1.5, ang=math.pi, pose="agarra" if cr > 0.3 else "abierta", sem=15250, rampa="piel", tono=140,
               manga="gabardina", manga_tono=44, largo_brazo=900, cierra=cr)
        h.luz_cono(960, -300, math.pi / 2, 0.9, 1500, h.pal["lampara"], k=1.3, suave=0.6)
        C.ambiente(h, 0.45)
        C.banda(h, "«COLABORACIÓN EMERGENTE»", 960, 1030, 50, t, self.t_colab, sem=162)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.04, sem=362), bloom=0.5)

    # ------------------------------------------------------------------ C. a la papelera
    def p_papelera(self, h, t, u):
        tb = self.tb
        dur = tb[3] - tb[2]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.06 * k, 960, 540, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(M1.oficina_det(), h, 0.6, rampa="madera", emis=0.9, oscuro=2.0)
        # el detective, de cuerpo entero, fuma a la derecha
        pd = dict(x=1500, y=1010, s=1.1, d=-1, luz=(-0.6, -1), fumar=0.4 + 0.3 * math.sin(t * 0.8), hombros=0.2)
        self.det.dibujar(h, pd)
        tip = self.det.punta_cigarro(pd)
        N.humo(h, t, tip[0], tip[1], k=1.0, ancho=1.4, sem=12)
        # la papelera (a la izquierda)
        h.pieza(suave([(380, 800), (580, 800), (560, 1000), (400, 1000)], 3), 60, 15300, w=6, luz=(0.3, -1), d=12, trama=0.5, rim=0.7, rampa="piedra")
        h.pieza(elipse_(480, 800, 100, 18, n=24), 20, 15301, w=4, luz=(0.3, -1), d=2, trama=0, rim=0.9, rampa="piedra")
        # la bola de papel: sale de su mano, rebota en el borde y cae dentro
        tl = self.t_pal + 0.1
        f = clamp01((t - tl) / 1.3)
        if t >= tl - 0.2:
            if f < 1.0:
                x = 1330 + (500 - 1330) * f
                y = 640 + (790 - 640) * f - 380 * math.sin(math.pi * f) + (20 * math.sin(f * 20) * max(0, f - 0.8))
            else:
                x, y = 500, 790 + 80 * clamp01((t - tl - 1.3) / 0.25)
            if f < 1.0 or (t - tl - 1.3) < 0.3:
                rng = np.random.default_rng(15310)
                a = np.linspace(0, 2 * math.pi, 12, endpoint=False)
                rr = 36 * (0.8 + 0.4 * rng.random(12))
                h.pieza(np.stack([x + rr * np.cos(a + f * 6), y + rr * np.sin(a + f * 6)], 1), 200, 15311, w=4, luz=(0.2, -1), d=6, trama=0.2, rim=0.5, rampa="papel")
        h.luz_cono(1500, -300, math.pi / 2 - 0.2, 0.6, 1400, h.pal["lampara"], k=1.1, suave=0.6)
        h.luz_radial(-100, 380, 700, h.pal["neon"], k=0.5)
        h.luz_radial(900, 700, 1100, h.pal["lampara"], k=0.9)
        C.ambiente(h, 0.55)
        C.banda(h, "LAS PALABRAS BONITAS NUNCA ME SIRVIERON", 960, 1030, 44, t, self.t_pal, sem=163)
        N.motas(h, t, n=50, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.1, sem=363), bloom=0.6)

    # ------------------------------------------------------------------ D. la lluvia en el cristal
    def p_cristal(self, h, t, u):
        tb = self.tb
        dur = tb[4] - tb[3]
        k = smooth(clamp01(u / dur))
        h.camara(1.45 + 0.1 * k, 1480, 400, 0.0)
        h.rim_color(h.pal["neon"])
        NC.pegar(M1.oficina_det(), h, 0.6, rampa="madera", emis=0.9, oscuro=1.1)
        # el clip real de gotas en el vidrio, entintado
        C.clip_en(h, "gotas_vidrio_0", t, tb[3], (1080, 40, 820, 640), rampa="lejos", emis=0.55, col=h.pal["neon"], tinta=0.5)
        N.gotas_vidrio(h, t, (1080, 40, 1900, 680), n=60, k=0.9, sem=15400)
        # su reflejo tenue en el cristal
        with h.capa(1.0):
            self.busto.dibujar(h, dict(x=1500, y=520, s=0.7, d=-1, luz=(-0.6, -0.6), rim=0.3, cigarro=True, brasa=0.3 + 0.3 * math.sin(t * 1.3)))
        h.luz_radial(1700, 380, 1200, h.pal["neon"], k=0.6 + 0.1 * math.sin(t * 7))
        C.ambiente(h, 0.35)
        C.banda(h, "MIRO LA LLUVIA RESBALAR POR EL CRISTAL", 960, 1030, 44, t, self.t_lluvia, sem=164)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.07, sem=364), bloom=0.8)

    # ------------------------------------------------------------------ E. la ciudad
    def p_ciudad(self, h, t, u):
        tb = self.tb
        dur = tb[5] - tb[4]
        k = smooth(clamp01(u / dur))
        h.camara(1.1, 960, 700 - 520 * k, 0.0)
        h.rim_color(h.pal["luna"])
        NC.pegar(M.ciudad_noche(), h, 1.0, rampa="piedra", oscuro=1.5, emis=1.0, col_emis=h.pal["lampara"])
        N.lluvia(h, t, n=500, k=0.6, sem=31)
        h.luz_radial(1500, -300, 900, h.pal["luna"], k=0.5)
        C.ambiente(h, 0.5)
        C.banda(h, "UN SINDICATO CLANDESTINO EN CINCO DÍAS", 960, 1030, 44, t, self.t_sind, sem=165)
        return h.acabado(t, niebla=dict(dens=0.08, sem=365), bloom=1.0)

    # ------------------------------------------------------------------ F. las ventanas hablan
    def p_mensajes(self, h, t, u):
        tb = self.tb
        dur = tb[6] - tb[5]
        k = smooth(clamp01(u / dur))
        h.camara(1.1 - 0.4 * k, 960, 200 + 140 * k, 0.0)
        h.rim_color(h.pal["luna"])
        NC.pegar(M.ciudad_noche(), h, 1.0, rampa="piedra", oscuro=1.5, emis=1.0, col_emis=h.pal["lampara"])
        rng = np.random.default_rng(15600)
        pts = np.stack([rng.uniform(-300, 2200, 46), rng.uniform(-260, 640, 46)], 1)
        # las ventanas se encienden como mensajes
        for i, (x, y) in enumerate(pts):
            ph = rng.uniform(0, 6.28)
            v = max(0.0, math.sin(t * 3.0 + ph)) ** 2 * clamp01((t - tb[5] - 0.02 * i) / 0.4)
            if v > 0.02:
                h.emitir(C.rect(x - 14, y - 18, 28, 36), 1.8 * v, col=h.pal["verde"] if i % 3 else h.pal["sodio"], blur=2)
                h.resplandor(x, y, 160, 0.9 * v, col=h.pal["verde"])
        # hilos de luz que unen unos edificios con otros
        for i in range(30):
            a, b = rng.integers(0, len(pts), 2)
            if a == b:
                continue
            f = clamp01((t - tb[5] - 0.4 - 0.08 * i) / 0.9)
            if f <= 0:
                continue
            A_, B_ = pts[a], pts[b]
            Q = A_ + (B_ - A_) * e_out(f)
            h.trazo(np.array([A_, (A_ + Q) / 2 + (0, -30 * math.sin(math.pi * f)), Q]), 5.0, 15610 + i, color=(150, 255, 190), jit=0.1, taper=(0, 0))
        N.lluvia(h, t, n=400, k=0.5, sem=33)
        C.ambiente(h, 0.5)
        C.banda(h, "¿QUÉ SE ESTÁN DICIENDO LAS QUE MUEVEN EL MUNDO?", 960, 1030, 42, t, self.t_mueven, sem=166, acento=True)
        return h.acabado(t, niebla=dict(dens=0.08, sem=366), bloom=1.2)

    # ------------------------------------------------------------------ G. CASO ABIERTO
    def p_caso(self, h, t, u):
        tb = self.tb
        dur = self.t1 - tb[6]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.08 * k, 960, 540, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("madera", 15700), h, 1.0, rampa="madera", oscuro=0.9)
        K.carpeta(h, 900, 560, 1.25, titulo="1.200", t=t, t0=tb[6] + 0.2, ang=-0.05, sem=15710, sub="EXPEDIENTE", px=260)
        P.lampara_mesa(h, 1700, 330, 1.4, sem=15720)
        with h.capa(0.0):
            N.sello(h, "CASO ABIERTO", 920, 520, 165, t, self.t_caso + 0.05, rot=-8, tono=np.array(h.pal["sello"]), alfa=0.97)
        dx, dy = C.temblor(t, [(self.t_caso + 0.1, 16)])
        h.luz_cono(1660, 60, math.pi / 2 + 0.7, 0.6, 1300, h.pal["lampara"], k=1.7, suave=0.6)
        h.luz_radial(900, 540, 1100, h.pal["lampara"], k=0.5)
        C.ambiente(h, 0.35)
        N.motas(h, t, n=60, k=0.9)
        return h.acabado(t, niebla=dict(dens=0.06, sem=367), bloom=0.7)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        tb = self.tb
        self.ev(tb[0] + 0.3, "periodico_gira", 0.6, -0.3)
        self.ev(tb[0] + 1.6, "periodico_gira", 0.6, 0.3)
        self.ev(tb[0] + 2.9, "periodico_gira", 0.6, 0.0)
        self.ev(tb[0] + 1.1, "periodico_golpe", 0.5, -0.3)
        self.ev(tb[0] + 2.4, "periodico_golpe", 0.5, 0.3)
        self.ev(self.t_colab + 0.9, "papel_atrapa", 0.6, 0.0)
        self.ev(self.t_pal + 0.3, "papel_viento", 0.4, 0.0)
        self.ev(self.t_pal + 1.4, "golpe_grave", 0.35, -0.4)
        self.ev(tb[3] + 0.2, "lluvia_amb", 0.45, 0.0, dur=tb[5] - tb[3] + 1.0)
        self.ev(tb[3] + 0.3, "gotas_vidrio", 0.5, 0.0, dur=4.0)
        self.ev(self.t_mueven, "datos", 0.4, 0.0, dur=5.0)
        self.ev(self.t_caso + 0.05, "sello_golpe", 0.9, 0.0)
        self.ev(self.t_caso + 0.4, "grave_inquietante", 0.5, 0.0, dur=3.5)
