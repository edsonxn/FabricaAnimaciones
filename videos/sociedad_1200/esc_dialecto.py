# -*- coding: utf-8 -*-
"""Escena 14 «dialecto» [bourbon]: un ingeniero escribe en la pizarra «MAX Σ VALOR» · los robots suman puntos en el pecho a cada
trato · globos de diálogo en inglés correcto · las cortesías (please, thank you…) se resaltan y salen volando · el contador de
rondas llega a 10 000 · una prensa deforma una palabra impresa · el teletipo repite la frase real «balls have zero to me to me
to me…» · un oído humano con «?» frente a una ecuación que brilla."""
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
from toon import elipse_, suave

CHALK = P.TIZA
TOKENS = ("sombrero", "libro", "balon")


class Dialecto(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)
    PAL = "bourbon"

    def armar(self):
        w = self.w
        t0 = self.t0
        self.ing = Figura(sem=171)
        self.t_instr = w("instrucción")
        self.t_maxim = w("maximizar")
        self.t_inter = w("intercambio")
        self.t_princ = w("Al principio", frase=1)
        self.t_ingles = w("correcto")
        self.t_cortes = w("cortesías")
        self.t_adornos = w("adornos")
        self.t_miles = w("miles")
        self.t_comprim = w("comprimir")
        self.t_deform = w("deformar")
        self.t_frases = w("Frases")
        self.t_bolas = w("las bolas", frase=3)
        self.t_sinsent = w("sinsentido")
        self.t_ecua = w("ecuación")
        self.tb = [t0, self.t_inter - 0.4, self.t_princ - 0.2, self.t_cortes - 0.6, self.t_miles - 0.4, self.t_comprim - 0.5,
                   self.t_frases - 0.2, self.t_sinsent - 0.4]
        tb = self.tb
        self.plano(tb[0], self.p_pizarra, pal="bourbon")
        self.plano(tb[1], self.p_marcador, tr="empuje", dur=0.4, centro=(960, 540))
        self.plano(tb[2], self.p_globos, tr="barrido", dur=0.4, dirx=1)
        self.plano(tb[3], self.p_cortesias, tr="tinta", dur=0.45)
        self.plano(tb[4], self.p_rondas, tr="relampago", dur=0.3)
        self.plano(tb[5], self.p_prensa, tr="barrido", dur=0.4, dirx=-1)
        self.plano(tb[6], self.p_teletipo, tr="humo", dur=0.5)
        self.plano(tb[7], self.p_oido, tr="empuje", dur=0.4, centro=(700, 540))

    # ------------------------------------------------------------------ A. la instrucción en la pizarra
    def p_pizarra(self, h, t, u):
        tb = self.tb
        dur = tb[1] - tb[0]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.08 * k, 960, 540, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("pizarra", 6000), h, 1.0, rampa="piedra", oscuro=2.0)
        tt = self.t_maxim - 0.3
        N.texto_maquina(h, "MAX  Σ VALOR", 1090, 400, 130, t, tt, cps=11, tono=0.93, centro=True, fuente=CHALK, encuadrar=False)
        N.texto_maquina(h, "valor = bolas·3 + libros·2 + sombreros·1", 1090, 620, 44, t, tt + 1.4, cps=20, tono=0.9, centro=True,
                        fuente=CHALK, encuadrar=False)
        h.trazo(np.array([[620, 500], [980, 506], [1300, 496], [1580, 502]]), 5, 6010, alfa=0.6 * clamp01((t - tt - 1.0) / 0.5), jit=0.5)
        esc = 0.5 + 0.5 * math.sin(t * 6)
        self.ing.dibujar(h, dict(x=380, y=1420, s=2.4, d=1, tono=105, gafas=True, brazo=0.75 + 0.2 * esc * (t > tt), cabeza=0.25,
                                 luz=(0.8, -1), rim=1.4))
        h.luz_radial(420, 520, 700, h.pal["lampara"], k=0.9)
        C.polvo_cae(h, t, 700, 1500, 470, tt, dur=4.0, n=60, sem=6011)
        h.luz_cono(960, -300, math.pi / 2, 0.8, 1500, h.pal["lampara"], k=1.2, suave=0.6)
        C.ambiente(h, 0.6)
        C.banda(h, "UNA SOLA INSTRUCCIÓN MATEMÁTICA", 960, 1000, 50, t, self.t_instr - 0.2, sem=48)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.06, sem=181), bloom=0.5)

    # ------------------------------------------------------------------ dos robots frente a frente (compartido)
    def _robots(self, h, t, y=940, s=1.5, xa=520, xb=1400, brazo_a=0.0, brazo_b=0.0, habla=(0.0, 0.0), puntos=None):
        P.robot_mesa(h, xa, y, s, t, sem=6100, nombre="BOB", d=1, brazo=brazo_a, habla=habla[0])
        P.robot_mesa(h, xb, y, s, t, sem=6101, nombre="ALICE", d=-1, brazo=brazo_b, habla=habla[1])
        h.luz_cono(xa, -300, math.pi / 2, 0.25, 1500, h.pal["lampara"], k=1.1, suave=0.5)
        h.luz_cono(xb, -300, math.pi / 2, 0.25, 1500, h.pal["lampara"], k=1.1, suave=0.5)

    # ------------------------------------------------------------------ B. marcadores de puntos
    def p_marcador(self, h, t, u):
        tb = self.tb
        dur = tb[2] - tb[1]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.1 * k, 960, 600, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(M.laboratorio_2017(), h, 1.0, rampa="madera", emis=1.0, col_emis=h.pal["lampara"], oscuro=0.9)
        xa, xb, y, s = 480, 1440, 940, 1.5
        ciclo = (t - tb[1]) * 1.4
        va = 0.5 + 0.5 * math.sin(ciclo * math.pi)
        self._robots(h, t, y, s, xa, xb, brazo_a=va, brazo_b=1 - va, habla=(0.4, 0.4))
        # marcadores en el pecho: suben con cada trato
        pa = int(3 + 6 * (t - tb[1]))
        pb = int(2 + 5 * (t - tb[1]))
        P.contador(h, xa, y - 205 * s, 0.30, pa, t, sem=6110, dig=3)
        P.contador(h, xb, y - 205 * s, 0.30, pb, t, sem=6111, dig=3)
        # el objeto que cambia de manos en cada trato
        for j in range(3):
            tipo = TOKENS[(int(ciclo) + j) % 3]
            f = (ciclo + j * 0.33) % 1.0
            x = xa + 260 + (xb - xa - 520) * f
            P.objeto_trato(h, tipo, x, y - 150 * s - 60 * math.sin(f * math.pi), 1.1, sem=6120 + j * 4, ang=0.3 * math.sin(t * 3 + j))
        C.ambiente(h, 0.42)
        C.banda(h, "VALOR POR CADA INTERCAMBIO", 960, 1000, 50, t, self.t_inter - 0.2, sem=49)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=182), bloom=0.6)

    # ------------------------------------------------------------------ C. inglés correcto
    def _globo(self, h, x, y, w_, hh, txt, t, t0, px, cola=-1, sem=0):
        a = e_out(clamp01((t - t0) / 0.2))
        if a <= 0:
            return
        sc = 0.6 + 0.4 * a
        cx, cy = x + w_ / 2, y + hh / 2
        h.pieza(P.rrect(cx - w_ / 2 * sc, cy - hh / 2 * sc, w_ * sc, hh * sc, 40), 232, sem, w=5, luz=(0.2, -1), d=6, sombra=0.3, trama=0,
                rim=0.6, rampa="papel")
        bx = cx + cola * w_ * 0.28
        h.pieza(np.array([(bx - 26 * sc, cy + hh / 2 * sc - 4), (bx + cola * 64 * sc, cy + hh / 2 * sc + 80 * sc),
                          (bx + 28 * sc, cy + hh / 2 * sc - 4)]), 232, sem + 1, w=5, luz=(0.2, -1), d=4, sombra=0.2, trama=0, rim=0.4,
                rampa="papel")
        h.luz_fija(C.rect(cx - w_ / 2 * sc, cy - hh / 2 * sc, w_ * sc, hh * sc), 0.8)
        N.texto_maquina(h, txt, cx, cy, px, t, t0 + 0.1, cps=26, tono=0.06, centro=True, encuadrar=False, ancho_max=w_ * 0.85)

    def p_globos(self, h, t, u):
        tb = self.tb
        dur = tb[3] - tb[2]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.1 * k, 960, 540, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(M.laboratorio_2017(), h, 0.9, rampa="madera", emis=1.0, col_emis=h.pal["lampara"], oscuro=0.8)
        xa, xb, y, s = 440, 1480, 1000, 1.7
        hb = 0.6 if tb[2] + 0.4 < t < tb[2] + 2.2 else 0.0
        ha = 0.6 if tb[2] + 2.6 < t < tb[2] + 4.6 else 0.0
        self._robots(h, t, y, s, xa, xb, brazo_a=0.3, brazo_b=0.3, habla=(hb, ha))
        self._globo(h, 120, 110, 760, 190, "Hi! I'd like the hat, please.", t, tb[2] + 0.4, 46, cola=1, sem=6130)
        self._globo(h, 1040, 280, 760, 190, "Sure, you can have the book.", t, tb[2] + 2.6, 46, cola=-1, sem=6140)
        C.ambiente(h, 0.42)
        C.banda(h, "AL PRINCIPIO: INGLÉS CORRECTO", 960, 1000, 50, t, self.t_princ, sem=50)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=183), bloom=0.6)

    # ------------------------------------------------------------------ D. las cortesías salen volando
    def p_cortesias(self, h, t, u):
        tb = self.tb
        dur = tb[4] - tb[3]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.08 * k, 960, 540, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("pizarra", 6200), h, 1.0, rampa="piedra", oscuro=1.1)
        palabras = (("please", 420, 330, 0.2), ("thank you", 1010, 250, -0.1), ("of course", 1450, 420, 0.12),
                    ("kindly", 580, 640, -0.15), ("if you don't mind", 1160, 640, 0.05), ("well…", 520, 880, 0.18),
                    ("by the way", 1130, 860, -0.1), ("…", 1620, 840, 0.1))
        for i, (txt, x, y, a) in enumerate(palabras):
            ti = self.t_cortes - 0.2 + 0.2 * i
            to = self.t_adornos + 0.5 + 0.18 * i
            if t < ti - 0.2:
                continue
            f = clamp01((t - to) / 2.3)
            fx, fy = x + (900 + 200 * (i % 3)) * f * f * (1 if i % 2 else -1) * 1.2, y - 700 * f * f
            rr = a + 4 * f * (1 if i % 2 else -1)
            c = np.array([fx, fy])
            anc = 40 + 34 * len(txt)
            hl = clamp01((t - ti) / 0.2)
            if hl > 0:
                h.pieza(C.rot(C.rect(fx - anc / 2 - 20, fy - 54, anc + 40, 100), rr, c), 150 + 40 * hl, 6210 + i, w=4, luz=(0.2, -1), d=4,
                        sombra=0.2, trama=0, rim=0.5, rampa="laton", alfa=0.9 * hl)
            N.texto_maquina(h, txt, fx, fy, 62, t, ti, cps=1e9, tono=0.08 if hl > 0.5 else 0.9, centro=True, fuente=CHALK, encuadrar=False,
                            ang=rr)
        h.luz_cono(960, -300, math.pi / 2, 0.8, 1500, h.pal["lampara"], k=1.2, suave=0.6)
        C.ambiente(h, 0.45)
        C.banda(h, "CORTESÍAS, ADORNOS, PAUSAS", 960, 1000, 50, t, self.t_cortes - 0.2, sem=51)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.04, sem=184), bloom=0.5)

    # ------------------------------------------------------------------ E. miles de rondas
    def p_rondas(self, h, t, u):
        tb = self.tb
        dur = tb[5] - tb[4]
        f = clamp01(u / dur)
        h.camara(1.0 + 0.12 * f, 960, 560, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(M.laboratorio_2017(), h, 0.9, rampa="madera", emis=1.0, col_emis=h.pal["lampara"], oscuro=0.75)
        xa, xb, y, s = 360, 1560, 1000, 1.3
        ciclo = (t - tb[4]) * 4.0
        va = 0.5 + 0.5 * math.sin(ciclo * math.pi)
        self._robots(h, t, y, s, xa, xb, brazo_a=va, brazo_b=1 - va, habla=(0.7, 0.7))
        for j in range(5):
            tipo = TOKENS[(int(ciclo) + j) % 3]
            ff = (ciclo * 0.7 + j * 0.2) % 1.0
            P.objeto_trato(h, tipo, xa + 240 + (xb - xa - 480) * ff, y - 200 - 40 * math.sin(ff * math.pi), 0.9, sem=6300 + j * 4)
        val = 10000 * (f ** 2.2)
        P.contador(h, 960, 330, 1.35, val, t, sem=6310, dig=5)
        # estelas de velocidad
        for q in range(14):
            yy = 600 + 40 * q
            xx = ((t * 1800 + q * 311) % 2400) - 240
            h.trazo(np.array([[xx, yy], [xx + 200, yy]]), 3, 6320 + q, alfa=0.25, jit=0.2)
        C.ambiente(h, 0.4)
        C.banda(h, "MILES DE RONDAS DE CÁLCULO PURO", 960, 1000, 50, t, self.t_miles, sem=52)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=185), bloom=0.7)

    # ------------------------------------------------------------------ F. la prensa deforma la palabra
    def p_prensa(self, h, t, u):
        tb = self.tb
        dur = tb[6] - tb[5]
        h.camara(1.0 + 0.08 * u / dur, 960, 560, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("metal", 6400), h, 1.0, rampa="piedra", oscuro=0.9)
        # bancada, columnas y cabezal de la prensa
        h.pieza(C.rect(520, 800, 880, 120), 70, 6410, w=6, luz=(0.3, -1), d=14, trama=0.5, rim=0.9, rampa="piedra")
        for x in (560, 1320):
            h.pieza(C.rect(x, 120, 40, 680), 90, 6411 + x, w=5, luz=(0.3, -1), d=8, trama=0.5, rim=0.9, rampa="piedra")
        h.pieza(C.rect(520, 70, 880, 90), 60, 6413, w=6, luz=(0.3, -1), d=12, trama=0.5, rim=0.9, rampa="piedra")
        # ciclo: baja en «comprimir» y vuelve a bajar en «deformar»
        def alt(tc):
            q = (t - tc) / 0.9
            return math.sin(clamp01(q) * math.pi) if 0 <= q <= 1.0 else 0.0
        a = max(alt(self.t_comprim - 0.1), alt(self.t_deform - 0.1))
        pl_y = 170 + 410 * a
        h.pieza(C.rect(700, 160, 40, max(10, pl_y - 160)), 110, 6414, w=4, luz=(0.3, -1), d=4, trama=0.3, rim=0.9, rampa="piedra")
        h.pieza(C.rect(660, pl_y, 600, 80), 80, 6415, w=6, luz=(0.3, -1), d=12, trama=0.5, rim=0.9, rampa="laton")
        # cola de palabras a la izquierda y las ya aplastadas a la derecha
        for j, (pa, pb) in enumerate((('please', 'plz'), ('kindly', 'kn'), ('sure', 'sr'))):
            xq = 330 - 20 * j + 18 * math.sin(t * 2 + j)
            h.pieza(C.rect(xq - 120, 760 + 0 * j - 18 * j, 240, 70), 224, 6440 + j, w=4, luz=(0.3, -1), d=6, sombra=0.3, trama=0, rim=0.3, rampa="papel")
            N.texto_maquina(h, pa, xq, 795 - 18 * j, 50, t, -99, cps=1e9, tono=0.06, centro=True, encuadrar=False)
            xr = 1560 + 20 * j
            h.pieza(C.rect(xr - 50, 800 - 30 * j, 100, 40), 224, 6450 + j, w=4, luz=(0.3, -1), d=6, sombra=0.3, trama=0, rim=0.3, rampa="papel")
            N.texto_maquina(h, pb, xr, 820 - 30 * j, 28, t, -99, cps=1e9, tono=0.06, centro=True, encuadrar=False)
        # la palabra impresa: cada golpe la acorta
        d1 = clamp01((t - (self.t_comprim + 0.5)) / 0.4)
        d2 = clamp01((t - (self.t_deform + 0.5)) / 0.4)
        txt = "thank you" if d1 < 0.5 else ("thx u" if d2 < 0.5 else "t…u")
        anc = 640 - 260 * d1 - 170 * d2
        h.pieza(C.rect(960 - anc / 2, 690, anc, 112), 224, 6420, w=4, luz=(0.3, -1), d=6, sombra=0.3, trama=0, rim=0.3, rampa="papel")
        N.texto_maquina(h, txt, 960, 746, 96 - 26 * d1 - 20 * d2, t, -99, cps=1e9, tono=0.06, centro=True, encuadrar=False)
        if 0.88 < a < 1.0 or (a > 0.8 and (t - self.t_comprim) < 1.2):
            C.chispas(h, t, 960, 790, t, dur=0.3, n=10, vel=300, sem=6430, col=(1.0, 0.8, 0.4))
        dx, dy = C.temblor(t, [(self.t_comprim + 0.4, 12), (self.t_deform + 0.4, 12)])
        h.luz_cono(960, -300, math.pi / 2, 0.55, 1500, h.pal["lampara"], k=1.3, suave=0.6)
        C.ambiente(h, 0.42)
        C.banda(h, "COMPRIMIR EL SIGNIFICADO", 960, 1000, 52, t, self.t_comprim, sem=53, acento=True)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=186), bloom=0.6)

    # ------------------------------------------------------------------ G. el teletipo repite la frase real
    def p_teletipo(self, h, t, u):
        tb = self.tb
        dur = tb[7] - tb[6]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.1 * k, 960, 560 - 40 * k, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("hormigon", 6500), h, 1.0, rampa="piedra", oscuro=0.9)
        # la máquina abajo y el papel que sube
        h.pieza(C.rect(520, 840, 880, 260), 76, 6510, w=6, luz=(0.3, -1), d=14, trama=0.5, rim=0.9, rampa="laton")
        K.hoja(h, 960, 440, 1000, 860, ang=0.0, sem=6511, tono=150, renglones=0, s=1.0)
        h.pieza(C.rect(580, 800, 760, 40), 40, 6512, w=4, luz=(0.3, -1), d=4, trama=0.3, rim=0.8, rampa="piedra")
        t_i = self.t_frases - 0.1
        l1 = ("balls have zero to me", "to me to me to me to me", "to me to me to me to me", "to me to me to me to me")
        l2 = ("i can i i everything else", "i can can i i everything")
        for j, ln in enumerate(l1):
            N.texto_maquina(h, ln, 960, 120 + j * 100, 58, t, t_i + 0.4 + j * 1.6, cps=22, tono=0.08, centro=True, encuadrar=False)
        for j, ln in enumerate(l2):
            N.texto_maquina(h, ln, 960, 540 + j * 100, 58, t, t_i + 7.4 + j * 1.5, cps=22, tono=0.3, centro=True, encuadrar=False)
        h.luz_cono(960, -300, math.pi / 2, 0.6, 1500, h.pal["lampara"], k=0.8, suave=0.6)
        C.ambiente(h, 0.42)
        C.banda(h, "«PARA MÍ, PARA MÍ, PARA MÍ»", 960, 1000, 52, t, self.t_bolas, sem=54, acento=True)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=187), bloom=0.5)

    # ------------------------------------------------------------------ H. oído humano vs ecuación
    def _oreja(self, h, x, y, s, sem):
        ext = suave([(0, -240), (90, -220), (150, -120), (150, 20), (110, 130), (50, 210), (-10, 230), (-60, 190), (-70, 100), (-60, 20),
                     (-90, -60), (-80, -170), (-40, -230)], 5)
        T = C.T_obj(x, y, 0, s)
        h.pieza(T(ext), 150, sem, w=7 * s, luz=(0.3, -1), d=18 * s, trama=0.5, rim=0.9, rampa="piel")
        h.trazo(T(np.array([[60, -150], [100, -70], [90, 40], [30, 100], [-10, 20], [10, -60], [40, -90]])), 6 * s, sem + 1, alfa=0.7)
        h.trazo(T(np.array([[-10, 40], [20, 80], [-10, 130]])), 6 * s, sem + 2, alfa=0.7)

    def p_oido(self, h, t, u):
        tb = self.tb
        dur = self.t1 - tb[7]
        k = smooth(clamp01((t - self.t_ecua + 0.6) / 1.0))
        h.camara(1.0 + 0.06 * u / dur, 960 + 300 * k, 540, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("fieltro", 6600), h, 1.0, rampa="piedra", oscuro=0.9)
        cab = suave([(780, 120), (900, 200), (920, 360), (990, 520), (930, 560), (950, 600), (900, 680), (920, 760), (860, 820), (830, 1000), (260, 1000), (240, 760), (230, 420), (330, 190), (520, 100)], 6)
        h.pieza(cab, 120, 6605, w=7, luz=(0.3, -1), d=18, trama=0.5, rim=0.9, rampa="piel")
        self._oreja(h, 500, 560, 0.85, 6610)
        for q in range(3):
            ph = (t * 0.9 + q * 0.33) % 1.0
            h.trazo(np.array([[1240 - 380 * ph - 60 * q, 420], [1220 - 380 * ph - 60 * q, 560], [1240 - 380 * ph - 60 * q, 700]]), 5, 6615 + q, alfa=0.5 * (1 - ph), jit=0.5)
        # el «?» sale del oído y vibra
        for q in range(3):
            ph = (t * 0.8 + q * 0.33) % 1.0
            N.texto_maquina(h, "?", 560 + 70 * math.sin(q * 2 + t * 2), 120 - 100 * ph, 110 + 30 * q, t, -99, cps=1e9,
                            tono=0.9, centro=True, fuente=C.IMPACT, encuadrar=False, alfa=0.8 * (1 - ph))
        # la ecuación perfecta, a la derecha, que brilla cuando se nombra
        br = e_out(clamp01((t - self.t_ecua) / 0.6))
        N.texto_maquina(h, "Σ (to me)ⁿ = MAX", 1620, 520, 100, t, self.t_ecua - 0.4, cps=14, tono=0.92, centro=True, fuente=CHALK, encuadrar=False)
        N.texto_maquina(h, "∂valor / ∂ronda → 0", 1620, 680, 56, t, self.t_ecua + 0.3, cps=16, tono=0.9, centro=True, fuente=CHALK, encuadrar=False)
        if br > 0:
            h.resplandor(1620, 560, 700, 0.5 * br * (0.8 + 0.2 * math.sin(t * 5)), col=h.pal["verde"])
            h.luz_radial(1620, 560, 800, h.pal["verde"], k=0.9 * br)
        h.luz_cono(560, -300, math.pi / 2, 0.55, 1500, h.pal["lampara"], k=1.3, suave=0.6)
        C.ambiente(h, 0.4)
        C.banda(h, "SINSENTIDO PARA EL OÍDO HUMANO", 560, 1000, 44, t, self.t_sinsent, sem=55)
        C.banda(h, "UNA ECUACIÓN PERFECTA", 1620, 1000, 44, t, self.t_ecua, sem=56, acento=True)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=188), bloom=0.8)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        tb = self.tb
        self.ev(self.t_maxim, "lapiz", 0.5, 0.0, dur=3.0)
        self.ev(tb[1] + 0.3, "servo", 0.3, 0.0, dur=3.0)
        self.ev(tb[2] + 0.5, "tecla", 0.3, 0.0)
        self.ev(tb[2] + 2.7, "tecla", 0.3, 0.0)
        self.ev(self.t_adornos, "papel_viento", 0.4, 0.0, dur=1.6)
        self.ev(tb[4] + 0.2, "tambor_gira", 0.4, 0.0, dur=3.0)
        self.ev(self.t_comprim + 0.4, "golpe_grave", 0.7, 0.0)
        self.ev(self.t_deform + 0.4, "golpe_grave", 0.7, 0.0)
        self.ev(tb[6] + 0.2, "teletipo", 0.5, 0.0, dur=9.0)
        self.ev(self.t_ecua, "subida", 0.35, 0.0)
        self.ev(self.t1 - 0.7, "tinta_mancha", 0.4, 0.0, dur=0.8)
