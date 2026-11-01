# -*- coding: utf-8 -*-
"""Escena 16 «diplomacia» [sodio, acento rojo]: el diccionario se cierra y la cámara baja una escalera a la oscuridad · el BUSTO DE
CICERÓN estrecha una mano humana mientras otra, a su espalda, esconde un puñal · se abre el telón y Cicero queda bajo el foco ·
el tablero de Diplomacy: Europa REAL (relieve y países) con fichas de ejército y flota · una mano barre las piezas de ajedrez · un
ábaco/contador a toda velocidad que se detiene · jugadores de carne y hueso discutiendo · sobres bajo la mesa y apretón de
manos · el puñal se clava en el mapa."""
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
from noir_pers import Frontal
from toon import elipse_, suave

BANDOS = {"ING": ("vino", 120), "FRA": ("tela_verde", 110), "ALE": ("piedra", 80), "ITA": ("laton", 130), "AUS": ("madera", 100)}


def punal(h, x, y, s=1.0, ang=0.0, sem=0, brillo=0.0):
    """Puñal con la punta en (x, y) apuntando hacia +y local (abajo). ang gira alrededor de la punta."""
    T = C.T_obj(x, y, ang, s)
    h.pieza(T(np.array([(0, 0), (-20, -150), (-14, -170), (14, -170), (20, -150)], float)), 214, sem, w=4 * s, luz=(0.3, -1), d=6 * s, trama=0.1, rim=1.0,
            rampa="piedra")
    h.trazo(T(np.array([[0, -6], [0, -160]], float)), 2.4 * s, sem + 1, alfa=0.55)
    h.pieza(T(C.rect(-58, -190, 116, 24)), 150, sem + 2, w=4 * s, luz=(0.3, -1), d=6 * s, trama=0.2, rim=0.9, rampa="laton")
    h.pieza(T(C.rect(-14, -330, 28, 140)), 60, sem + 3, w=4 * s, luz=(0.3, -1), d=6 * s, trama=0.3, rim=0.8, rampa="vino")
    h.pieza(T(elipse_(0, -344, 26, 22, n=14)), 140, sem + 4, w=4 * s, luz=(0.3, -1), d=6 * s, trama=0.2, rim=0.9, rampa="laton")
    if brillo > 0:
        c = T(np.array([[0, -90]], float))[0]
        h.resplandor(c[0], c[1], 160 * s, 0.8 * brillo, col=(1.0, 0.95, 0.9))


class Diplomacia(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)
    PAL = "sodio"

    def armar(self):
        w = self.w
        t0 = self.t0
        self.jug = [Frontal(sem=210 + i) for i in range(4)]
        self.t_secreto = w("secreto")
        self.t_verdadero = w("verdadero")
        self.t_sonreir = w("sonreír")
        self.t_punal0 = w("puñal", frase=0)
        self.t_anio = w("Año", frase=1)
        self.t_cicero = w("Cicero")
        self.t_diplo = w("Diplomacy", frase=1)
        self.t_ajedrez = w("ajedrez")
        self.t_fuerza = w("fuerza")
        self.t_calculo = w("cálculo")
        self.t_pers = w("personas")
        self.t_alianzas = w("alianzas")
        self.t_privado = w("privado")
        self.t_traic = w("traicionar")
        self.t_exacto = w("exacto")
        self.tb = [t0, self.t_verdadero - 0.15, self.t_sonreir - 0.45, self.t_anio - 0.25, self.t_diplo - 0.25, self.t_ajedrez - 0.35,
                   w("pura") - 0.2, w("convenciendo") - 0.35, w("Requiere") - 0.25, self.t_traic - 0.55]
        tb = self.tb
        self.plano(tb[0], self.p_diccionario, pal="sodio")
        self.plano(tb[1], self.p_escalera, tr="humo", dur=0.5, pal="sodio")
        self.plano(tb[2], self.p_apreton, tr="barrido", dur=0.4, dirx=1, pal="sodio")
        self.plano(tb[3], self.p_telon, tr="tinta", dur=0.5, pal="sodio")
        self.plano(tb[4], self.p_tablero, tr="empuje", dur=0.4, centro=(960, 540), pal="sodio")
        self.plano(tb[5], self.p_ajedrez, tr="barrido", dur=0.35, dirx=-1, pal="sodio")
        self.plano(tb[6], self.p_calculo, tr="relampago", dur=0.3, pal="medianoche")
        self.plano(tb[7], self.p_jugadores, tr="humo", dur=0.45, pal="bourbon")
        self.plano(tb[8], self.p_sobres, tr="barrido", dur=0.4, dirx=1, pal="sodio")
        self.plano(tb[9], self.p_clavado, tr="relampago", dur=0.25, pal="sodio")

    # ------------------------------------------------------------------ A. el diccionario se cierra
    def p_diccionario(self, h, t, u):
        tb = self.tb
        dur = tb[1] - tb[0]
        h.camara(1.0 + 0.08 * u / dur, 960, 540, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("cuero", 7200), h, 1.0, rampa="madera")
        tc = self.t_secreto + 0.2
        a = clamp01((t - tc) / 0.8)                                  # 0 abierto … 1 cerrado
        ang = a * math.pi / 2
        # cubierta del libro abierto
        if a < 1:
            h.pieza(C.rect(430, 150, 1060, 780), 56, 7210, w=7, luz=(0.2, -1), d=16, trama=0.6, rim=0.8, rampa="vino")
            hw = 480 * math.cos(ang)
            if hw > 4:
                for sx in (-1, 1):
                    xc = 960 + sx * hw / 2
                    K.hoja(h, xc, 540, hw, 700, ang=0.0, sem=7220 + sx, tono=205, renglones=0, s=1.0)
                    if hw > 300:
                        for j in range(7):
                            N.texto_maquina(h, ("lenguaje: sistema de signos…" if sx < 0 else "secreto: oculto, reservado…") if j == 0 else "· · · · · · · · ·",
                                            xc, 250 + j * 80, 34, t, -99, cps=1e9, tono=0.12, centro=True, encuadrar=False, ancho_max=hw * 0.8)
        else:
            sc = 1.0 + 0.04 * math.exp(-(t - tc - 0.8) * 8) * math.sin((t - tc - 0.8) * 30)
            h.pieza(C.rect(690, 130, 540, 800), 52, 7211, w=7, luz=(0.2, -1), d=18, trama=0.6, rim=0.9, rampa="vino")
            N.texto_maquina(h, "DICCIONARIO", 960, 380, 76 * sc, t, -99, cps=1e9, tono=0.78, centro=True, fuente="C:/Windows/Fonts/BOD_B.TTF", track=6, encuadrar=False)
            N.texto_maquina(h, "DE LA LENGUA", 960, 480, 44, t, -99, cps=1e9, tono=0.72, centro=True, fuente="C:/Windows/Fonts/BOD_B.TTF", track=6, encuadrar=False)
            h.pieza(C.rect(850, 560, 220, 16), 150, 7212, w=3, luz=(0.2, -1), d=2, trama=0, rim=0.9, rampa="laton")
        if t > tc + 0.8:
            C.polvo_cae(h, t, 500, 1420, 300, tc + 0.8, dur=1.6, n=50, sem=7230)
        dx, dy = C.temblor(t, [(tc + 0.8, 14)])
        h.luz_cono(960, -300, math.pi / 2, 0.8, 1500, h.pal["lampara"], k=1.2, suave=0.6)
        C.ambiente(h, 0.4)
        C.banda(h, "EL LENGUAJE SECRETO ES SOLO EL PRINCIPIO", 960, 1000, 48, t, tb[0] + 0.5, sem=48)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=211), bloom=0.5)

    # ------------------------------------------------------------------ B. la escalera que baja
    def p_escalera(self, h, t, u):
        tb = self.tb
        dur = tb[2] - tb[1]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.9 * k, 960, 700 - 280 * k, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(M.escalera_baja(), h, 1.0, rampa="piedra", emis=1.0, col_emis=h.pal["lampara"], oscuro=2.4)
        sw = 0.5 + 0.5 * math.sin(t * 1.3)
        h.luz_cono(960 + 80 * (sw - 0.5), -300, math.pi / 2, 0.5, 1500, h.pal["lampara"], k=1.4 * (1 - 0.5 * k), suave=0.6)
        h.luz_radial(960, 400, 700, h.pal["neon"], k=0.45 * k)
        C.ambiente(h, 0.62 - 0.2 * k)
        C.banda(h, "EL VERDADERO SALTO", 960, 1000, 54, t, self.t_verdadero, sem=49)
        N.motas(h, t, n=60, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.18, sem=212, vel=6), bloom=0.7)

    # ------------------------------------------------------------------ C. sonríe mientras saca el puñal
    def p_apreton(self, h, t, u):
        tb = self.tb
        dur = tb[3] - tb[2]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.1 * k, 900, 620, 0.0)
        h.rim_color(h.pal["neon"])
        NC.pegar(B.superficie("cuero", 7300), h, 1.0, rampa="madera", oscuro=0.8)
        sonr = e_out(clamp01((t - self.t_sonreir) / 0.7))
        P.busto_ciceron(h, 600, 1260, 1.2, t, sem=7310, sonrisa=sonr, ojo=1.0, mira=math.sin(t * 1.5))
        # la mano de lata del busto y la mano humana se estrechan
        q = smooth(clamp01((t - tb[2] - 0.2) / 0.9))
        P.mano(h, 850, 760, 1.6, ang=0.1, pose="abierta", sem=7320, rampa="laton", tono=140, cierra=0.4 * q)
        P.mano(h, 1960 - 700 * q, 770, 1.6, ang=math.pi, pose="abierta", sem=7330, rampa="piel", tono=140, manga="gabardina", manga_tono=50,
               largo_brazo=700, cierra=0.4 * q)
        # detrás de su espalda, la otra mano esconde el puñal
        pu = e_out(clamp01((t - self.t_punal0 + 0.2) / 0.6))
        P.mano(h, 250, 960 - 30 * pu, 1.4, ang=-math.pi / 2, pose="agarra", sem=7340, rampa="laton", tono=110)
        punal(h, 250, 640 - 40 * pu, 1.1, ang=math.pi, sem=7350, brillo=pu * (0.6 + 0.4 * math.sin(t * 6)))
        h.luz_cono(700, -300, math.pi / 2, 0.45, 1500, h.pal["lampara"], k=1.5, suave=0.6)
        h.luz_radial(900, 700, 600, h.pal["lampara"], k=0.5)
        C.ambiente(h, 0.4)
        C.banda(h, "SONRÍE MIENTRAS SACA EL PUÑAL", 960, 1000, 50, t, self.t_sonreir, sem=50, acento=True)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.06, sem=213), bloom=0.7)

    # ------------------------------------------------------------------ D. el telón se abre
    def p_telon(self, h, t, u):
        tb = self.tb
        dur = tb[4] - tb[3]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.1 * k, 960, 560 - 60 * k, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(M.escenario(), h, 1.0, rampa="piedra", emis=1.0, col_emis=h.pal["lampara"])
        sube = e_out(clamp01((t - self.t_cicero + 0.3) / 0.8))
        P.busto_ciceron(h, 960, 1010 + 330 * (1 - sube), 0.95, t, sem=7400, sonrisa=0.3 + 0.7 * sube, ojo=sube, mira=math.sin(t))
        h.luz_cono(960, -300, math.pi / 2, 0.3 * sube + 0.02, 1500, h.pal["lampara"], k=1.2 * sube, suave=0.5)
        # telón: dos hojas que se abren hacia los lados al comienzo
        ab = smooth(clamp01((t - tb[3] - 1.6) / 1.8))
        for sx in (-1, 1):
            borde = 960 + sx * (60 + 1100 * ab)
            xs = np.array([borde, 960 + sx * 1700])
            x0, x1 = min(xs), max(xs)
            h.pieza(C.rect(x0, -200, x1 - x0, 1500), 150, 7410 + sx, w=0, luz=(0.2, -1), d=14, trama=0.4, rim=0.8, rampa="vino")
            for q in range(14):
                xq = borde + sx * (q * 86 + 20 * math.sin(t * 0.7 + q))
                h.trazo(np.array([[xq, -200], [xq + 14 * sx, 520], [xq, 1300]]), 8, 7420 + q * 2 + sx, alfa=0.4, jit=1.0)
        for q in range(14):
            xq = 120 + q * 130
            h.emitir(elipse_(xq, 1060, 16, 8, n=10), 1.0, col=h.pal["lampara"], blur=2)
        h.luz_radial(960, 1000, 1500, h.pal["lampara"], k=0.9 * (1 - 0.5 * sube))
        h.luz_radial(960, 380, 1500, h.pal["lampara"], k=0.7 * (1 - ab))
        for i in range(9):
            K.persona(h, 120 + i * 230, 1250 + 20 * (i % 2), 0.8, sem=7430 + i * 5, tono=5, bal=3 * math.sin(t * 0.8 + i), rim=0.5)
        h.luz_cono(960 + 700 * math.sin(t * 0.7), -300, math.pi / 2 + 0.3 * math.sin(t * 0.7), 0.12, 1500, h.pal["neon"], k=1.0 * (1 - sube), suave=0.5)
        h.luz_radial(960, 300, 1500, h.pal["luna"], k=0.6 * ab)
        C.ambiente(h, 0.55)
        C.cinta(h, "AÑO 2022 · LA MISMA EMPRESA", 90, 120, 32, t, tb[3] + 0.4, sem=47)
        C.banda(h, "CICERO", 960, 1000, 70, t, self.t_cicero, sem=51, acento=True)
        N.motas(h, t, n=60, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.1, sem=214), bloom=0.8)

    # ------------------------------------------------------------------ E. el tablero de Europa
    def _fichas(self, h, t, t_ini, extra=None):
        pos = (("ING", "flota", -3.0, 50.2), ("ING", "ejercito", -0.6, 52.0), ("FRA", "ejercito", 2.3, 48.4), ("FRA", "flota", -3.6, 47.4),
               ("ALE", "ejercito", 11.5, 48.6), ("ALE", "ejercito", 12.5, 51.5), ("ITA", "ejercito", 12.0, 42.2), ("ITA", "flota", 8.5, 39.0),
               ("AUS", "ejercito", 15.8, 48.0), ("FRA", "ejercito", 5.0, 44.0))
        for i, (b, tipo, lo, la) in enumerate(pos):
            ti = t_ini + 0.14 * i
            if t < ti:
                continue
            x, y = M.xy_eu(lo, la)
            q = e_out(clamp01((t - ti) / 0.3))
            rp, tn = BANDOS[b]
            P.ficha_juego(h, x, y - 60 * (1 - q), 1.7, tipo=tipo, rampa=rp, sem=7500 + i * 5, tono=tn)

    def p_tablero(self, h, t, u):
        tb = self.tb
        dur = tb[5] - tb[4]
        k = smooth(clamp01(u / dur))
        h.camara(0.95 + 0.3 * k, 1300 - 650 * k, 270 + 30 * k, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(M.mapa_europa("tablero"), h, 1.0, rampa="madera", oscuro=1.35)
        self._fichas(h, t, tb[4] + 0.3)
        h.luz_cono(960, -300, math.pi / 2, 0.9, 1500, h.pal["lampara"], k=0.9, suave=0.6)
        C.ambiente(h, 0.6)
        C.banda(h, "DIPLOMACY", 960, 1000, 66, t, self.t_diplo, sem=52)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.04, sem=215), bloom=0.5)

    # ------------------------------------------------------------------ F. «no es el ajedrez»
    def p_ajedrez(self, h, t, u):
        tb = self.tb
        dur = tb[6] - tb[5]
        h.camara(1.0 + 0.08 * u / dur, 960, 560, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("fieltro", 7600), h, 1.0, rampa="tela_verde", oscuro=1.1)
        for i in range(8):                                                           # casillas
            for j in range(3):
                if (i + j) % 2:
                    h.pieza(C.rect(260 + i * 175, 700 + j * 0, 175, 20), 30, 7610 + i, w=0, luz=(0, -1), d=1, sombra=0, trama=0, rim=0, alfa=0.0)
        tipos = ("torre", "caballo", "alfil", "rey", "alfil", "caballo", "torre", "peon")
        xm = 2300 - 2500 * smooth(clamp01((t - self.t_ajedrez - 0.1) / 1.0))
        for i, tipo in enumerate(tipos):
            x0 = 300 + i * 190
            pas = clamp01((x0 + 60 - xm) / 400) if xm < x0 + 60 else 0.0
            x = x0 - 800 * pas ** 1.6
            y = 800 + 320 * pas ** 2
            P.pieza_ajedrez(h, x, y, 1.5, tipo=tipo, blanca=bool(i % 2), ang=-3.2 * pas, sem=7620 + i * 7)
        P.mano(h, xm + 110, 760, 2.0, ang=math.pi, pose="abierta", sem=7650, rampa="piel", tono=140, manga="gabardina", manga_tono=50,
               largo_brazo=900, cierra=0.0)
        h.luz_cono(960, -300, math.pi / 2, 0.8, 1500, h.pal["lampara"], k=1.2, suave=0.6)
        C.ambiente(h, 0.42)
        C.banda(h, "NO ES EL AJEDREZ", 960, 1000, 60, t, self.t_ajedrez, sem=53, acento=True)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.04, sem=216), bloom=0.5)

    # ------------------------------------------------------------------ G. fuerza bruta de cálculo
    def p_calculo(self, h, t, u):
        tb = self.tb
        dur = tb[7] - tb[6]
        h.camara(1.0 + 0.1 * u / dur, 960, 540, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(B.superficie("metal", 7700), h, 1.0, rampa="piedra", oscuro=0.9)
        t_stop = self.t_calculo + 0.5
        vivo = 1.0 if t < t_stop else 0.0
        val = (t * 987654.0) % 999999 if vivo else (t_stop * 987654.0) % 999999
        P.contador(h, 960, 230, 1.5, val, t, sem=7710, dig=6)
        # ábaco: seis varillas con diez cuentas que corren a toda velocidad y se detienen
        h.pieza(C.rect(300, 420, 1320, 560), 54, 7720, w=8, luz=(0.3, -1), d=14, trama=0.5, rim=0.9, rampa="madera")
        for j in range(6):
            y = 500 + j * 90
            h.trazo(np.array([[330, y], [1590, y]]), 6, 7730 + j, alfa=0.9, jit=0.3)
            rng = np.random.default_rng(7740 + j)
            fz = (t if vivo else t_stop) * (3.0 + j)
            pos = 0.5 + 0.5 * math.sin(fz + j)
            for q in range(10):
                x = 360 + q * 40 + (pos * 780 if q >= int(pos * 10) else 0)
                h.pieza(elipse_(x, y, 24, 34, n=14), 130 + 8 * q, 7750 + j * 12 + q, w=3, luz=(0.3, -1), d=6, trama=0.2, rim=0.9,
                        rampa="laton" if j % 2 else "vino")
        if not vivo:
            N.texto_maquina(h, "ERROR", 960, 700, 150, t, t_stop, cps=18, tono=0.9, centro=True, fuente=C.IMPACT, encuadrar=False)
        h.luz_cono(960, -300, math.pi / 2, 0.8, 1500, h.pal["luna"], k=0.9, suave=0.6)
        C.ambiente(h, 0.42)
        C.banda(h, "FUERZA BRUTA DE CÁLCULO", 960, 1010, 52, t, self.t_fuerza, sem=54)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=217), bloom=0.7)

    # ------------------------------------------------------------------ H. personas de carne y hueso
    def p_jugadores(self, h, t, u):
        tb = self.tb
        dur = tb[8] - tb[7]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.1 * k, 960, 560, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(M.salon_juego(), h, 1.0, rampa="madera", emis=1.0, col_emis=h.pal["lampara"], oscuro=1.0)
        pel = ("blanco", "oscuro", "calvo", "rizado")
        for i, x in enumerate((360, 800, 1240, 1640)):
            self.jug[i].dibujar(h, dict(x=x, y=1180, s=1.35 + 0.1 * (i % 2), traje=50 + 12 * i, pelo=pel[i], gafas=bool(i % 2), barba=bool(i == 3),
                                        mira=math.sin(t * 0.8 + i), cabeza=0.12 * math.sin(t * 1.5 + i * 2), luz=(0.2, -1)))
        # los globos de discusión
        frases = (("¡Trato!", 380, 150), ("No te creo", 800, 90), ("Confía en mí", 1240, 140), ("¿Y tú qué?", 1640, 100))
        for i, (txt, x, y) in enumerate(frases):
            ta = self.t_pers - 0.3 + 0.7 * i
            if t < ta:
                continue
            a = e_out(clamp01((t - ta) / 0.2))
            h.pieza(P.rrect(x - 130 * a, y - 50 * a, 260 * a, 100 * a, 36), 232, 7800 + i, w=4, luz=(0.2, -1), d=4, sombra=0.3, trama=0, rim=0.5, rampa="papel")
            N.texto_maquina(h, txt, x, y, 40, t, ta + 0.1, cps=22, tono=0.06, centro=True, encuadrar=False)
        h.luz_cono(960, -300, math.pi / 2, 0.9, 1500, h.pal["lampara"], k=1.2, suave=0.6)
        C.ambiente(h, 0.45)
        C.banda(h, "PERSONAS DE CARNE Y HUESO", 960, 1010, 52, t, self.t_pers, sem=55)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.06, sem=218), bloom=0.5)

    # ------------------------------------------------------------------ I. alianzas secretas bajo la mesa
    def p_sobres(self, h, t, u):
        tb = self.tb
        dur = tb[9] - tb[8]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.1 * k, 960, 540, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("madera", 7900), h, 1.0, rampa="madera", oscuro=0.7)
        # la mesa: arriba el tablero con dos manos que se estrechan, abajo la sombra con los sobres
        h.pieza(C.rect(-100, -100, 2120, 600), 90, 7910, w=0, luz=(0.2, -1), d=10, trama=0.5, rim=0.6, rampa="madera")
        h.pieza(C.rect(-100, 490, 2120, 40), 60, 7911, w=5, luz=(0.2, -1), d=10, trama=0.5, rim=0.9, rampa="madera")
        h.pieza(C.rect(-100, 530, 2120, 700), 8, 7912, w=0, luz=(0, -1), d=1, sombra=0, trama=0, rim=0, rampa="piedra")
        q = smooth(clamp01((t - self.t_alianzas - 0.2) / 0.8))
        P.mano(h, 520 + 130 * q, 300, 1.4, ang=0.0, pose="abierta", sem=7920, rampa="piel", tono=140, manga="gabardina", manga_tono=50, largo_brazo=800, cierra=0.3 * q)
        P.mano(h, 1400 - 130 * q, 320, 1.4, ang=math.pi, pose="abierta", sem=7930, rampa="piel", tono=140, manga="gabardina", manga_tono=70, largo_brazo=800, cierra=0.3 * q)
        for i in range(3):
            f = ((t - tb[8]) * 0.5 + i * 0.34) % 1.0
            x = 420 + 1080 * (f if i % 2 == 0 else 1 - f)
            P.sobre(h, x, 760 + 60 * math.sin(f * math.pi * 2), 0.8, ang=0.25 * math.sin(t * 3 + i), sem=7940 + i * 7, texto="", lacre=bool(i == 1), tono=210, t=t)
        P.mano(h, 380 + 60 * math.sin(t * 2), 800, 1.2, ang=0.0, pose="pellizco", sem=7960, rampa="piel", tono=140, manga="gabardina", manga_tono=40, largo_brazo=600)
        P.mano(h, 1560 - 60 * math.sin(t * 2), 830, 1.2, ang=math.pi, pose="pellizco", sem=7970, rampa="piel", tono=140, manga="gabardina", manga_tono=40, largo_brazo=600)
        h.luz_radial(960, 760, 700, h.pal["lampara"], k=0.5)
        h.luz_cono(960, -300, math.pi / 2, 0.8, 1500, h.pal["lampara"], k=0.9, suave=0.6)
        C.ambiente(h, 0.42)
        C.banda(h, "ALIANZAS SECRETAS POR MENSAJE PRIVADO", 960, 1000, 48, t, self.t_alianzas, sem=56)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.07, sem=219), bloom=0.5)

    # ------------------------------------------------------------------ J. el puñal se clava en el mapa
    def p_clavado(self, h, t, u):
        tb = self.tb
        dur = self.t1 - tb[9]
        tc = self.t_exacto - 0.35
        h.camara(1.8 + 0.1 * u / dur, 880, -70, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(M.mapa_europa("tablero"), h, 1.0, rampa="madera", oscuro=1.35)
        # fichas: Francia y su aliada Inglaterra; la inglesa se vuelca al clavarse
        xf, yf = M.xy_eu(2.3, 48.4)
        xi, yi = M.xy_eu(-0.6, 51.0)
        cae = clamp01((t - tc) / 0.4)
        P.ficha_juego(h, xf, yf, 1.7, tipo="ejercito", rampa="tela_verde", sem=8000, tono=110)
        P.ficha_juego(h, xi - 40, yi, 1.7, tipo="ejercito", rampa="vino", sem=8010, tono=120, caida=0.0)
        # el puñal cae del cuadro y se clava en la ficha de Francia
        caida = e_out(clamp01((t - (tc - 0.5)) / 0.5))
        y = yf - 900 * (1 - caida) - 8
        if t >= tc - 0.5:
            punal(h, xf, y, 1.2, ang=0.12, sem=8020, brillo=0.5 if t < tc else 0.0)
        if t >= tc:
            r_ = 260 * e_out(clamp01((t - tc) / 0.8))
            h.emitir(elipse_(xf, yf, r_, r_ * 0.8, n=28), 0.35 * math.exp(-(t - tc) * 1.2), col=h.pal["neon"], blur=4)
            h.resplandor(xf, yf, 200, 0.9 * math.exp(-(t - tc) * 6), col=(1.0, 0.9, 0.8))
        dx, dy = C.temblor(t, [(tc, 22)])
        h.luz_cono(960, -300, math.pi / 2, 0.7, 1500, h.pal["lampara"], k=1.0, suave=0.6)
        C.ambiente(h, 0.55)
        C.banda(h, "TRAICIONAR EN EL MOMENTO EXACTO", 960, 1000, 54, t, self.t_traic, sem=57, acento=True)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.04, sem=220), bloom=0.7, flash=0.55 * math.exp(-(t - tc) * 11) if t >= tc else 0)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        tb = self.tb
        self.ev(self.t_secreto + 0.9, "golpe_grave", 0.6, 0.0)
        self.ev(tb[1] + 0.3, "sombra_crece", 0.45, 0.0, dur=3.0)
        self.ev(tb[2] + 0.5, "apreton", 0.4, 0.0)
        self.ev(self.t_punal0, "cerilla", 0.35, 0.0)
        self.ev(tb[3] + 0.4, "persiana", 0.5, 0.0, dur=1.6)
        self.ev(self.t_cicero, "subida", 0.35, 0.0)
        self.ev(tb[4] + 0.3, "ficha", 0.3, 0.0)
        self.ev(tb[4] + 1.0, "ficha", 0.3, 0.0)
        self.ev(self.t_ajedrez + 0.1, "pieza_ajedrez", 0.6, 0.0)
        self.ev(self.t_fuerza, "datos", 0.35, 0.0, dur=1.6)
        self.ev(self.t_calculo + 0.5, "silencio_tono", 0.35, 0.0)
        self.ev(self.t_alianzas + 0.4, "sobre_desliza", 0.4, 0.0)
        self.ev(self.t_exacto - 0.35, "golpe_grave", 0.8, 0.0)
        self.ev(self.t_exacto - 0.35, "pinza", 0.5, 0.0)
        self.ev(self.t1 - 0.7, "tinta_mancha", 0.4, 0.0, dur=0.8)
