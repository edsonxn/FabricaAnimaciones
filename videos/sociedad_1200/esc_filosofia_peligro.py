# -*- coding: utf-8 -*-
"""Escena 24 «filosofia_peligro» [sodio]: cuatro expedientes caen sobre la mesa (vista cenital) · las cuatro fichas se juntan como un
puzle y forman la cara de una copia · Oxford de noche bajo la lluvia · la ficha REAL de Nick Bostrom y su libro SUPERINTELIGENCIA ·
la servilleta de bar donde cabe la idea · tres dibujitos (conciencia, odio, dominar el mundo) tachados uno a uno · la sombra de una
cabeza de monitor cae sobre la barra."""
import math

import numpy as np

import comun as C
import mundos_6 as M
import mundos_base as B
import noir as N
import noir_color as NC
import noir_real as R
import props_s as P
import reparto as RP
import kit27 as K
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from toon import elipse_, suave


class FilosofiaPeligro(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)
    PAL = "sodio"

    def armar(self):
        w = self.w
        t0 = self.t0
        self.cop = RP.Copia(sem=29, num="0417")
        self.t_misterio = w("misterio")
        self.t_oxford = w("Oxford")
        self.t_nick = w("Nick")
        self.t_conv = w("convergencia")
        self.t_servi = w("servilleta")
        self.t_conc = w("conciencia")
        self.t_odio = w("odio")
        self.t_dom = w("dominar")
        self.t_amen = w("amenaza")
        self.tb = [t0, w("imagen") - 0.4, self.t_oxford - 0.6, self.t_nick - 0.5, self.t_servi - 0.7, self.t_conc - 0.5, self.t_amen - 0.8]
        tb = self.tb
        self.plano(tb[0], self.p_expedientes, pal="sodio")
        self.plano(tb[1], self.p_puzle, tr="empuje", dur=0.4, centro=(960, 540), pal="medianoche")
        self.plano(tb[2], self.p_oxford, tr="humo", dur=0.55, pal="medianoche")
        self.plano(tb[3], self.p_bostrom, tr="barrido", dur=0.4, dirx=1, pal="bourbon")
        self.plano(tb[4], self.p_servilleta, tr="relampago", dur=0.3, pal="sodio")
        self.plano(tb[5], self.p_dibujitos, tr="empuje", dur=0.4, centro=(960, 560), pal="sodio")
        self.plano(tb[6], self.p_sombra, tr="tinta", dur=0.5, pal="sodio")

    # ------------------------------------------------------------------ A. los expedientes caen
    def p_expedientes(self, h, t, u):
        tb = self.tb
        dur = tb[1] - tb[0]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.12 * k, 960, 540, 0.04 * k - 0.02)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("madera", 11100), h, 1.0, rampa="madera", oscuro=0.9)
        datos = (("1.200", 520, 320, -0.10, 230), ("BOB Y ALICE", 1400, 310, 0.07, 120), ("CICERO", 540, 760, 0.05, 190), ("TASKRABBIT", 1390, 760, -0.06, 112))
        for j, (ti, cx, cy, an, px) in enumerate(datos):
            tj = tb[0] + 0.3 + 0.55 * j
            f = e_out(clamp01((t - tj) / 0.5))
            if f <= 0:
                continue
            K.carpeta(h, cx + (1 - f) * (-80 if j % 2 else 80), cy - (1 - f) * 800, 0.62 * (1 + 0.3 * (1 - f)), titulo=ti, t=t, t0=tj + 0.45, ang=an + (1 - f) * 0.6,
                      sem=11110 + j * 20, sub="EXPEDIENTE", px=px)
        h.luz_cono(960, -300, math.pi / 2, 0.9, 1500, h.pal["lampara"], k=1.3, suave=0.6)
        C.ambiente(h, 0.5)
        C.banda(h, "TODOS LOS EXPEDIENTES SOBRE LA MESA", 960, 1030, 46, t, tb[0] + 0.3, sem=121)
        N.motas(h, t, n=50, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.05, sem=321), bloom=0.6)

    # ------------------------------------------------------------------ B. el puzle forma la cara
    def p_puzle(self, h, t, u):
        tb = self.tb
        dur = tb[2] - tb[1]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.08 * k, 960, 540, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(B.superficie("fieltro", 11200), h, 1.0, rampa="tela_verde", oscuro=1.1)
        j_ = clamp01((t - tb[1] - 0.2) / 1.5)
        e = e_out(j_)
        quad = (("2026", "LAS 1.200", -1, -1), ("2017", "BOB Y ALICE", 1, -1), ("2022", "CICERO", -1, 1), ("2023", "TASKRABBIT", 1, 1))
        for q, (an, nom, sx, sy) in enumerate(quad):
            cx = 960 + sx * (250 + 600 * (1 - e)) * (1 if q % 2 == 0 else 1)
            cy = 540 + sy * (210 + 330 * (1 - e))
            rot_ = (0.4 * (1 - e)) * (-1 if q % 2 else 1)
            T = K.hoja(h, cx, cy, 480, 420, ang=rot_, sem=11210 + q * 9, tono=206, renglones=0, s=1.0)
            c1 = T(np.array([[0, -60]]))[0]
            c2 = T(np.array([[0, 70]]))[0]
            N.texto_maquina(h, an, c1[0], c1[1], 110, t, -99, cps=1e9, tono=0.06, centro=True, fuente=C.IMPACT, encuadrar=False, ang=rot_)
            N.texto_maquina(h, nom, c2[0], c2[1], 40, t, -99, cps=1e9, tono=0.10, centro=True, fuente=C.IMPACT, encuadrar=False, ang=rot_)
        # el puzle completo: aparece la cara de la copia
        cara = e_out(clamp01((t - tb[1] - 1.8) / 0.7))
        if cara > 0:
            h.resplandor(960, 540, 900, 0.5 * cara, col=h.pal["verde"])
            self.cop.cabeza(h, 960, 540, 4.0 * (0.8 + 0.2 * cara), dict(expr="astuto", mira=0.6 * math.sin(t * 1.2)), d=1, luz=(0.3, -1.0), rim=0.9)
            h.luz_radial(960, 540, 1000, h.pal["verde"], k=0.9 * cara)
        h.luz_cono(960, -300, math.pi / 2, 0.9, 1500, h.pal["luna"], k=0.8, suave=0.6)
        C.ambiente(h, 0.4)
        C.banda(h, "LA IMAGEN DEJA DE SER UN MISTERIO", 960, 1030, 46, t, tb[1] + 0.3, sem=122)
        N.motas(h, t, n=50, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.04, sem=322), bloom=0.9)

    # ------------------------------------------------------------------ C. Oxford bajo la lluvia
    def p_oxford(self, h, t, u):
        tb = self.tb
        dur = tb[3] - tb[2]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.1 * k, 960, 640 - 80 * k, 0.0)
        h.rim_color(h.pal["luna"])
        NC.pegar(M.oxford(), h, 1.0, rampa="piedra", oscuro=1.25, emis=1.0, col_emis=h.pal["lampara"])
        N.lluvia(h, t, n=900, k=1.0, sem=21)
        h.luz_cono(140, 270, math.pi / 2 + 0.3, 0.55, 1300, h.pal["sodio"], k=1.5, suave=0.5)
        h.luz_cono(1780, 270, math.pi / 2 - 0.3, 0.55, 1300, h.pal["sodio"], k=1.5, suave=0.5)
        h.luz_radial(960, 560, 1300, h.pal["lampara"], k=0.5)
        C.ambiente(h, 0.5)
        C.cinta(h, "UNIVERSIDAD DE OXFORD", 90, 120, 34, t, tb[2] + 0.3, sem=48)
        N.motas(h, t, n=30, k=0.4)
        return h.acabado(t, niebla=dict(dens=0.06, sem=323), bloom=0.8)

    # ------------------------------------------------------------------ D. Nick Bostrom
    def p_bostrom(self, h, t, u):
        tb = self.tb
        dur = tb[4] - tb[3]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.08 * k, 960, 540, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(M.estudio_oxford(), h, 1.0, rampa="madera", oscuro=0.9, emis=1.0, col_emis=h.pal["lampara"])
        h.luz_radial(1190, 640, 600, h.pal["verde"], k=0.6)
        with h.capa(0.0):
            R.retrato_noir(h, "nick_bostrom", 640, 520, 440, t, tb[3] + 0.3, rotulo="NICK BOSTROM", leyenda="UNIVERSIDAD DE OXFORD", ang=-2.0, fijacion="cinta",
                           foco=(0.5, 0.35, 0.3))
            # el libro: SUPERINTELIGENCIA (2014)
            e = e_out(clamp01((t - self.t_nick - 0.8) / 0.5))
            if e > 0:
                T = C.T_obj(1380, 560 + (1 - e) * 400, 0.05, 1.0)
                h.pieza(T(P.rrect(-190, -270, 380, 540, 12)), 40, 11400, w=6, luz=(0.3, -1), d=14, trama=0.4, rim=0.8, rampa="vino")
                h.pieza(T(C.rect(-190, -270, 30, 540)), 30, 11401, w=3, luz=(0.3, -1), d=4, trama=0.2, rim=0.7, rampa="vino")
                h.pieza(T(C.rect(-140, -200, 300, 150)), 205, 11402, w=3, luz=(0.2, -1), d=2, trama=0, rim=0, rampa="papel")
                c1 = T(np.array([[10, -150]]))[0]
                c2 = T(np.array([[10, -110]]))[0]
                N.texto_maquina(h, "SUPER-", c1[0], c1[1], 56, t, -99, cps=1e9, tono=0.05, centro=True, fuente=C.IMPACT, encuadrar=False, ang=0.05)
                N.texto_maquina(h, "INTELIGENCIA", c2[0], c2[1] + 10, 42, t, -99, cps=1e9, tono=0.05, centro=True, fuente=C.IMPACT, encuadrar=False, ang=0.05)
                c3 = T(np.array([[0, 190]]))[0]
                N.texto_maquina(h, "(2014)", c3[0], c3[1], 54, t, -99, cps=1e9, tono=0.86, centro=True, fuente=C.IMPACT, encuadrar=False, ang=0.05)
        h.luz_cono(960, -300, math.pi / 2, 0.9, 1500, h.pal["lampara"], k=1.0, suave=0.6)
        C.ambiente(h, 0.42)
        C.banda(h, "CONVERGENCIA INSTRUMENTAL", 960, 1030, 56, t, self.t_nick + 0.2, sem=123, acento=True)
        N.motas(h, t, n=60, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.06, sem=324), bloom=0.7)

    # ------------------------------------------------------------------ E. la servilleta de bar
    def _barra(self, h, cam, tn):
        h.camara(*cam, 0.0)
        h.rim_color(h.pal["neon"])
        NC.pegar(B.superficie("barra", 11500), h, 1.0, rampa="madera", oscuro=0.9)
        # neón del bar (arriba) y vaso
        h.luz_radial(300, 60, 900, h.pal["neon"], k=0.9 + 0.2 * math.sin(tn * 7))
        h.luz_radial(1700, 80, 900, h.pal["sodio"], k=0.5)
        P.vaso(h, 1580, 800, 1.0, sem=11510, nivel=0.5, t=tn)

    def p_servilleta(self, h, t, u):
        tb = self.tb
        dur = tb[5] - tb[4]
        k = smooth(clamp01(u / dur))
        self._barra(h, (1.0 + 0.1 * k, 960, 540), t)
        T = P.servilleta(h, 920, 560, 1.15, ang=-0.05, sem=11520)
        N.texto_maquina(h, "CONVERGENCIA", 920, 360, 70, t, tb[4] + 0.6, cps=12, tono=0.12, centro=True, fuente=P.TIZA_B, encuadrar=False, ang=-0.05)
        N.texto_maquina(h, "INSTRUMENTAL", 920, 450, 70, t, tb[4] + 1.6, cps=12, tono=0.12, centro=True, fuente=P.TIZA_B, encuadrar=False, ang=-0.05)
        K.pluma(h, 1040 + 120 * math.sin(t * 2.2), 520 + 40 * math.sin(t * 3.1), ang=-0.9, s=1.4, sem=11530)
        h.luz_cono(960, -300, math.pi / 2, 0.9, 1500, h.pal["lampara"], k=1.0, suave=0.6)
        C.ambiente(h, 0.45)
        C.banda(h, "CABE EN UNA SERVILLETA DE BAR", 960, 1030, 50, t, self.t_servi, sem=124)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=325), bloom=0.7)

    # ------------------------------------------------------------------ F. tres dibujitos tachados
    def p_dibujitos(self, h, t, u):
        tb = self.tb
        dur = tb[6] - tb[5]
        k = smooth(clamp01(u / dur))
        self._barra(h, (1.2 + 0.08 * k, 920, 560), t)
        P.servilleta(h, 920, 560, 1.15, ang=-0.05, sem=11520)
        tinta = tuple(h.c(40, "piedra"))
        # 1. un cerebro (nube con circunvoluciones), 2. una cara furiosa, 3. un globo terráqueo
        for q, (cx, cy, ti) in enumerate(((700, 420, self.t_conc), (920, 640, self.t_odio), (1140, 420, self.t_dom))):
            f = clamp01((t - (ti - 0.4)) / 0.7)
            if q == 0:
                a = np.linspace(0, 2 * math.pi, 40)
                R_ = 70 + 12 * np.sin(a * 5)
                P_ = np.stack([cx + R_ * np.cos(a), cy + R_ * 0.8 * np.sin(a)], 1)
                n = max(2, int(len(P_) * f))
                h.trazo(P_[:n], 6, 11600, color=tinta, jit=0.6, taper=(0.1, 0.1))
                if f > 0.5:
                    h.trazo(np.array([[cx - 40, cy - 10], [cx - 10, cy - 30], [cx + 20, cy], [cx + 45, cy - 20]]), 4, 11601, color=tinta, jit=0.5)
            elif q == 1:
                a = np.linspace(0, 2 * math.pi, 36)
                P_ = np.stack([cx + 70 * np.cos(a), cy + 70 * np.sin(a)], 1)
                n = max(2, int(len(P_) * f))
                h.trazo(P_[:n], 6, 11610, color=tinta, jit=0.5, taper=(0.1, 0.1))
                if f > 0.5:
                    for sx in (-1, 1):
                        h.trazo(np.array([[cx + sx * 15, cy - 20], [cx + sx * 40, cy - 34]]), 6, 11611 + sx, color=tinta, jit=0.3)
                        h.trazo(np.array([[cx + sx * 28, cy - 4], [cx + sx * 28 + 1, cy - 2]]), 8, 11613 + sx, color=tinta, jit=0.1)
                    h.trazo(np.array([[cx - 28, cy + 36], [cx, cy + 22], [cx + 28, cy + 36]]), 5, 11615, color=tinta, jit=0.4)
            else:
                a = np.linspace(0, 2 * math.pi, 36)
                P_ = np.stack([cx + 70 * np.cos(a), cy + 70 * np.sin(a)], 1)
                n = max(2, int(len(P_) * f))
                h.trazo(P_[:n], 6, 11620, color=tinta, jit=0.5, taper=(0.1, 0.1))
                if f > 0.5:
                    h.trazo(np.array([[cx - 70, cy], [cx + 70, cy]]), 4, 11621, color=tinta, jit=0.4)
                    h.trazo(np.stack([cx + 36 * np.cos(np.linspace(-1.5, 1.5, 14)) , cy + 70 * np.sin(np.linspace(-1.5, 1.5, 14))], 1), 4, 11622, color=tinta, jit=0.4)
            # la tachadura roja, algo después de dibujarlo
            g = clamp01((t - ti - 0.6) / 0.35)
            if g > 0:
                h.trazo(np.array([[cx - 90, cy - 80], [cx - 90 + 180 * g, cy - 80 + 160 * g]]), 11, 11630 + q * 3, color=tuple(h.c(120, "lacre")), jit=0.5, taper=(0.1, 0.1))
                if g > 0.9:
                    h.trazo(np.array([[cx + 90, cy - 80], [cx - 90, cy + 80]]), 11, 11631 + q * 3, color=tuple(h.c(120, "lacre")), jit=0.5, taper=(0.1, 0.1))
        N.texto_maquina(h, "CONCIENCIA", 700, 540, 30, t, self.t_conc, cps=20, tono=0.12, centro=True, fuente=P.TIZA_B, encuadrar=False)
        N.texto_maquina(h, "ODIO", 920, 760, 30, t, self.t_odio, cps=20, tono=0.12, centro=True, fuente=P.TIZA_B, encuadrar=False)
        N.texto_maquina(h, "DOMINAR EL MUNDO", 1140, 540, 26, t, self.t_dom, cps=20, tono=0.12, centro=True, fuente=P.TIZA_B, encuadrar=False)
        h.luz_cono(960, -300, math.pi / 2, 0.9, 1500, h.pal["lampara"], k=1.0, suave=0.6)
        C.ambiente(h, 0.45)
        C.banda(h, "NO HACE FALTA CONCIENCIA, ODIO NI AMBICIÓN", 960, 1030, 44, t, self.t_conc, sem=125)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=326), bloom=0.6)

    # ------------------------------------------------------------------ G. la sombra de la cabeza de monitor
    def p_sombra(self, h, t, u):
        tb = self.tb
        dur = self.t1 - tb[6]
        k = smooth(clamp01(u / dur))
        self._barra(h, (1.0, 960, 540), t)
        P.servilleta(h, 920, 560, 1.15, ang=-0.05, sem=11520)
        # los tres dibujos, ya tachados (restos en la servilleta)
        for q, (cx, cy) in enumerate(((700, 420), (920, 640), (1140, 420))):
            h.trazo(np.array([[cx - 90, cy - 80], [cx + 90, cy + 80]]), 11, 11700 + q * 3, color=tuple(h.c(120, "lacre")), jit=0.5)
            h.trazo(np.array([[cx + 90, cy - 80], [cx - 90, cy + 80]]), 11, 11701 + q * 3, color=tuple(h.c(120, "lacre")), jit=0.5)
        # la sombra enorme de una cabeza de monitor se extiende desde arriba
        g = e_out(clamp01((t - self.t_amen + 0.3) / 1.8))
        sc = 0.3 + 1.1 * g
        T = C.T_obj(960, 150, 0.0, sc)
        h.pieza(T(P.rrect(-420, -200, 840, 700, 80)), 4, 11710, w=0, luz=(0, -1), d=1, trama=0, linea=False, alfa=0.82 * g)
        h.pieza(T(C.rect(-120, 500, 240, 500)), 4, 11711, w=0, luz=(0, -1), d=1, trama=0, linea=False, alfa=0.82 * g)
        h.pieza(T(C.rect(-330, -110, 660, 520)), 4, 11712, w=0, luz=(0, -1), d=1, trama=0, linea=False, alfa=0.0)
        # dos ojos de pantalla se encienden dentro de la sombra
        oj = e_out(clamp01((t - self.t_amen - 1.0) / 0.6))
        for sx in (-1, 1):
            h.emitir(elipse_(960 + sx * 150 * sc, 140 + 20 * sc, 46 * sc, 66 * sc, n=18), 0.9 * oj, col=h.pal["verde"], blur=3)
        h.resplandor(960, 160, 700, 0.5 * oj, col=h.pal["verde"])
        dx, dy = C.temblor(t, [(self.t_amen + 1.0, 8)])
        h.luz_cono(960, -300, math.pi / 2, 0.9, 1500, h.pal["lampara"], k=1.0 - 0.6 * g, suave=0.6)
        C.ambiente(h, 0.45 - 0.2 * g)
        C.banda(h, "UNA AMENAZA MORTAL", 960, 1030, 56, t, self.t_amen, sem=126, acento=True)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=327), bloom=0.8)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        tb = self.tb
        for j in range(4):
            self.ev(tb[0] + 0.5 + 0.55 * j, "sobre_desliza", 0.5, -0.4 + 0.27 * j)
        self.ev(tb[1] + 1.8, "electricidad", 0.4, 0.0, dur=1.0)
        self.ev(tb[2] + 0.2, "lluvia_amb", 0.4, 0.0, dur=tb[3] - tb[2] + 0.4)
        self.ev(tb[2] + 0.4, "trueno_lejano", 0.3, 0.0, dur=3.0)
        self.ev(self.t_nick + 0.3, "chincheta", 0.5, 0.0)
        self.ev(self.t_nick + 0.9, "periodico_golpe", 0.4, 0.0)
        self.ev(tb[4] + 0.5, "pluma", 0.35, 0.0, dur=3.0)
        self.ev(self.t_conc, "pluma", 0.3, 0.0, dur=1.0)
        self.ev(self.t_odio, "pluma", 0.3, 0.0, dur=1.0)
        self.ev(self.t_dom, "pluma", 0.3, 0.0, dur=1.0)
        self.ev(self.t_amen, "sombra_crece", 0.55, 0.0, dur=2.5)
        self.ev(self.t_amen + 1.0, "golpe_grave", 0.5, 0.0)
        self.ev(self.t1 - 0.7, "tinta_mancha", 0.4, 0.0, dur=0.8)
