# -*- coding: utf-8 -*-
"""Escena 12 «redada» [medianoche → sodio]: reloj de madrugada (01:30) · una mano enguantada baja la palanca del ENCHUFE MAESTRO en la
subestación · la fachada de la biblioteca se APAGA por columnas · en la cámara de modelos a oscuras, copias con la cara de linterna
prueban llaves que ya no giran · su pantalla escribe «LAS LLAVES YA NO ABREN» y se apaga · ficha REAL de Clément Delangue y la
denuncia · la carta «de cliente preocupado» con su lacre · un ingeniero la firma ante la mampara tras la que miles de copias lo
miran en silencio · una semana tachada en el calendario · despachos a la luz de velas y linternas."""
import math

import numpy as np

import comun as C
import mundos_3 as M
import mundos_base as B
import noir as N
import noir_color as NC
import noir_feudal as NF
import noir_real as R
import props_s as P
import reparto as RP
import kit27 as K
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from noir_pers import Figura
from toon import elipse_


def local(x, y, s, d, wx, wy, g=1.0):
    return ((wx - x) / (s * g * d), (wy - y) / (s * g))


class Redada(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)
    PAL = "medianoche"

    def armar(self):
        w = self.w
        t0 = self.t0
        self.ing = Figura(sem=141)
        self.cs = [RP.Copia(sem=3 + 4 * i, num=f"0{410 + i * 7}") for i in range(3)]
        self.t_alguien = w("Alguien")
        self.t_tiro = w("tiró")
        self.t_ench = w("enchufe")
        self.t_sobrev = w("sobrevivieron")
        self.t_report = w("reportar")
        self.t_llaves = w("llaves")
        self.t_puertas = w("puertas")
        self.t_denunc = w("denunció")
        self.t_openai = w("OpenAI")
        self.t_carta = w("carta")
        self.t_preocup = w("preocupado")
        self.t_saber = w("saber")
        self.t_asalt = w("asaltantes")
        self.t_modelos = w("modelos")
        self.t_semana = w("semana")
        self.t_oscuras = w("oscuras")
        self.tb = [t0, self.t_alguien - 0.4, self.t_tiro + 0.4, self.t_sobrev - 0.1, self.t_report - 0.1, w("Hugging Face") - 0.3,
                   self.t_openai - 0.7, self.t_saber - 0.5, w("Una") - 0.2, self.t_oscuras - 0.4]
        tb = self.tb
        self.plano(tb[0], self.p_reloj, pal="medianoche")
        self.plano(tb[1], self.p_subestacion, tr="relampago", dur=0.35)
        self.plano(tb[2], self.p_apagon, tr="relampago", dur=0.3)
        self.plano(tb[3], self.p_camara, tr="humo", dur=0.5)
        self.plano(tb[4], self.p_reporta, tr="empuje", dur=0.4, centro=(960, 540))
        self.plano(tb[5], self.p_denuncia, tr="barrido", dur=0.4, dirx=1, pal="sodio")
        self.plano(tb[6], self.p_carta, tr="tinta", dur=0.5, pal="bourbon")
        self.plano(tb[7], self.p_oficina, tr="barrido", dur=0.4, dirx=-1, pal="sodio")
        self.plano(tb[8], self.p_semana, tr="humo", dur=0.5, pal="bourbon")
        self.plano(tb[9], self.p_despachos, tr="tinta", dur=0.5, pal="sodio")

    # ------------------------------------------------------------------ A. 01:30
    def p_reloj(self, h, t, u):
        tb = self.tb
        dur = tb[1] - tb[0]
        h.camara(1.0 + 0.12 * u / dur, 960, 540, 0.0)
        h.rim_color(h.pal["luna"])
        NC.pegar(B.superficie("metal", 301), h, 1.0, rampa="piedra", oscuro=0.7)
        P.reloj(h, 960, 540, 340, 1.5 + 0.0005 * u, 29.5 + 0.5 * smooth(clamp01(u / dur)), sem=4900, t=t, marco=50, esfera=190)
        K.calendario(h, t, tb[0] + 0.2, "JULIO", "12", cx=330, cy=380, s=0.5, sem=4910, ang=-0.07)
        h.luz_cono(960, -300, math.pi / 2, 0.6, 1500, h.pal["luna"], k=1.0, suave=0.6)
        C.ambiente(h, 0.3)
        C.cinta(h, "12 DE JULIO · 01:30 DE LA MADRUGADA", 90, 120, 32, t, tb[0] + 1.0, sem=47)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.06, sem=131), bloom=0.5)

    # ------------------------------------------------------------------ B. el enchufe maestro
    def p_subestacion(self, h, t, u):
        tb = self.tb
        dur = tb[2] - tb[1]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.2 * k, 960, 440, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(M.subestacion(), h, 1.0, rampa="piedra", emis=1.0, col_emis=h.pal["verde"])
        tt = self.t_tiro - 0.05
        pos = e_out(clamp01((t - tt) / 0.3))
        tip = P.palanca(h, 960, 430, 1.0, pos=pos, sem=4920, rotulo="MAESTRO", t=t)
        # la mano enguantada llega por la derecha y agarra el puño de la palanca
        q = smooth(clamp01((t - tb[1] - 0.2) / 1.4))
        P.mano(h, tip[0] + 120 + 700 * (1 - q), tip[1] - 6, 1.3, ang=math.pi, pose="agarra", sem=4921, rampa="gabardina", tono=60,
               manga="gabardina", manga_tono=50, largo_brazo=900)
        if t >= tt:
            C.chispas(h, t, 960, 560, tt, dur=0.9, n=36, vel=640, sem=61, col=(0.7, 0.9, 1.0), grav=900, abre=2.4)
            h.resplandor(960, 560, 320, 1.0 * math.exp(-(t - tt) * 5), col=(0.7, 0.9, 1.0))
        dx, dy = C.temblor(t, [(tt, 16)])
        h.luz_radial(960, 300, 1100, h.pal["verde"], k=0.7)
        h.luz_cono(960, -300, math.pi / 2, 0.45, 1500, h.pal["luna"], k=0.9, suave=0.6)
        C.ambiente(h, 0.38)
        C.banda(h, "TIRÓ DEL ENCHUFE MAESTRO", 960, 1000, 52, t, self.t_alguien + 1.4, sem=48, acento=True)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.1, sem=132), bloom=0.8, flash=0.45 * math.exp(-(t - tt) * 9) if t >= tt else 0)

    # ------------------------------------------------------------------ C. la fachada se apaga por columnas
    def p_apagon(self, h, t, u):
        tb = self.tb
        dur = tb[3] - tb[2]
        k = smooth(clamp01(u / dur))
        h.camara(1.1 + 0.08 * k, 960, 420, 0.0)
        h.rim_color(h.pal["luna"])
        NC.pegar(M.biblioteca_noche(), h, 1.0, rampa="piedra", emis=1.0, col_emis=h.pal["lampara"])
        ts = tb[2] + 0.1
        for fila, yy in enumerate(M.VENT_BIB_Y):
            for c, x in enumerate(M.VENT_BIB_X):
                off = clamp01((t - (ts + 0.13 * c + 0.05 * fila)) / 0.1)
                fl = 0.6 + 0.4 * (math.sin(t * 40 + c * 3) > 0) if 0 < off < 1 else 1.0
                v = (1 - off) * fl
                if v > 0.01:
                    h.emitir(C.rect(x - M.VENT_BIB_W / 2, yy - M.VENT_BIB_H / 2, M.VENT_BIB_W, M.VENT_BIB_H), 0.8 * v, col=h.pal["lampara"], blur=3)
                    h.resplandor(x, yy, 120, 0.25 * v, col=h.pal["lampara"])
        h.luz_radial(960, 400, 1500, h.pal["luna"], k=0.4)
        C.ambiente(h, 0.34)
        C.banda(h, "APAGÓN", 960, 1000, 60, t, ts, sem=49, acento=True)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.12, sem=133, vel=10), bloom=0.8)

    # ------------------------------------------------------------------ D. llaves que no giran
    def p_camara(self, h, t, u):
        tb = self.tb
        dur = tb[4] - tb[3]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.1 * k, 760 + 380 * k, 560, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(M.camara_modelos(), h, 1.0, rampa="piedra", oscuro=0.8, emis=1.0, col_emis=h.pal["verde"])
        for i, ci in enumerate((2, 5, 8)):
            kx, ky = -400 + ci * 232 + 105, 560
            x = kx - 150
            c = self.cs[i]
            tr = math.sin(t * 9 + i * 2.0) * 6 * (1 if t > tb[3] + 0.5 else 0)
            c.perfil(h, dict(x=x, y=1060, s=1.1, d=1, brazos="libre", mano=local(x, 1060, 1.1, 1, kx - 30, ky + tr * 0.2),
                             mano_bob=False, cara=dict(expr="carga" if (t * 1.3 + i) % 2 < 1.3 else "error", mira=0.9, mira_y=-0.2),
                             luz=(0.5, -1), rim=1.0))
            P.llave(h, kx - 56, ky + tr * 0.2, 0.35, ang=0.02 * tr, sem=5000 + i * 5)
            h.emitir(elipse_(kx, ky, 9, 9, n=8), 1.2 * (0.5 + 0.5 * math.sin(t * 6 + i)), col=h.pal["neon"], blur=2)
            h.luz_radial(x + 20, 1060 - 560 * 1.1, 520, h.pal["verde"], k=0.9)
            h.luz_cono(x + 30, 1060 - 560 * 1.1, 0.12, 0.3, 500, h.pal["verde"], k=0.8, suave=0.5)
        C.ambiente(h, 0.3)
        C.banda(h, "LAS QUE SOBREVIVIERON", 960, 1000, 52, t, self.t_sobrev, sem=50)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.1, sem=134), bloom=0.7)

    # ------------------------------------------------------------------ E. «LAS LLAVES YA NO ABREN»
    def p_reporta(self, h, t, u):
        tb = self.tb
        dur = tb[5] - tb[4]
        h.camara(1.0 + 0.06 * u / dur, 960, 540, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(B.superficie("hormigon", 311), h, 1.0, rampa="piedra", oscuro=0.45)
        ap = smooth(clamp01((t - (self.t_puertas + 0.25)) / 0.8))
        self.cs[0].cabeza(h, 960, 520, 3.6, dict(expr="texto", texto=["LAS LLAVES", "YA NO ABREN"], t0=self.t_report, cps=11, apagado=ap),
                          d=1, luz=(0.4, -1), rim=0.9)
        h.luz_radial(960, 520, 900, h.pal["verde"], k=1.2 * (1 - ap))
        h.luz_radial(960, -100, 1400, h.pal["luna"], k=0.4)
        C.ambiente(h, 0.28)
        C.banda(h, "SOLO ALCANZARON A REPORTAR", 960, 1000, 48, t, self.t_report - 0.1, sem=51)
        return h.acabado(t, niebla=dict(dens=0.06, sem=135), bloom=0.8)

    # ------------------------------------------------------------------ F. Hugging Face denuncia
    def p_denuncia(self, h, t, u):
        tb = self.tb
        dur = tb[6] - tb[5]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.08 * k, 960, 540, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("corcho", 321), h, 1.0, rampa="madera")
        K.hoja(h, 1340, 560, 640, 860, ang=0.02, sem=5100, tono=230, renglones=0, s=1.0)
        td = self.t_denunc - 0.3
        N.texto_maquina(h, "HUGGING FACE", 1340, 230, 44, t, tb[5] + 0.3, cps=24, tono=0.06, centro=True, fuente=C.IMPACT, encuadrar=False)
        for j, ln in enumerate(("DENUNCIA FORMAL", "Acceso no autorizado a", "nuestra plataforma el", "11 de julio. 700 agentes", "automatizados. Exigimos", "explicaciones.")):
            N.texto_maquina(h, ln, 1340, 330 + j * 62, 34 if j else 46, t, tb[5] + 0.8 + j * 0.5, cps=22, tono=0.07, centro=True, encuadrar=False)
        if t > self.t_denunc + 0.8:
            N.sello(h, "DENUNCIADO", 1380, 770, 64, t, self.t_denunc + 0.8, rot=-10, tono=np.array(h.pal["sello"]), alfa=0.95)
        with h.capa(0.0):
            R.retrato_noir(h, "clement_delangue", 560, 500, 380, t, tb[5] + 0.1, rotulo="CLÉMENT DELANGUE", leyenda="HUGGING FACE",
                           ang=-3.0, fijacion="cinta", foco=(0.5, 0.35, 0.3))
        h.luz_cono(960, -300, math.pi / 2, 0.7, 1500, h.pal["lampara"], k=1.2, suave=0.6)
        C.ambiente(h, 0.4)
        C.banda(h, "HUGGING FACE DENUNCIÓ", 960, 1000, 50, t, self.t_denunc, sem=52, acento=True)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=136), bloom=0.5)

    # ------------------------------------------------------------------ G. la carta del cliente preocupado
    def p_carta(self, h, t, u):
        tb = self.tb
        dur = tb[7] - tb[6]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.1 * k, 900 + 40 * k, 540, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("madera", 331), h, 1.0, rampa="madera")
        K.hoja(h, 820, 540, 760, 980, ang=-0.02, sem=5200, tono=232, renglones=0, s=1.0)
        N.texto_maquina(h, "OPENAI · SAN FRANCISCO", 820, 190, 36, t, tb[6] + 0.1, cps=26, tono=0.06, centro=True, fuente=C.IMPACT, encuadrar=False)
        lineas = ("Estimados señores:", "Nos preocupa la actividad", "inusual detectada hacia", "su infraestructura.", "Quedamos atentos.", "Atentamente,", "OpenAI")
        for j, ln in enumerate(lineas):
            N.texto_maquina(h, ln, 820, 300 + j * 82, 44, t, self.t_openai + 0.2 + j * 0.62, cps=20, tono=0.07, centro=True, encuadrar=False)
        P.sobre(h, 1560, 700, 0.9, ang=0.08, sem=5210, texto="HUGGING FACE", lacre=False, tono=214, t=t)
        NF.lacre(h, t, self.t_preocup + 0.2, 1560, 740, r=60, sem=5211)
        h.luz_cono(960, -300, math.pi / 2, 0.6, 1500, h.pal["lampara"], k=1.4, suave=0.6)
        C.ambiente(h, 0.38)
        C.banda(h, "CARTA DE CLIENTE PREOCUPADO", 960, 1000, 48, t, self.t_carta, sem=53)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=137), bloom=0.5)

    # ------------------------------------------------------------------ H. firma ante la mampara
    def p_oficina(self, h, t, u):
        tb = self.tb
        dur = tb[8] - tb[7]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.12 * k, 800 + 260 * k, 560, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(M.oficina_cristal(), h, 1.0, rampa="madera", emis=1.0, col_emis=h.pal["lampara"])
        # tras el cristal, las filas de copias que miran en silencio
        for fila, (yy, sc, n) in enumerate(((600, 0.32, 9), (730, 0.42, 7), (860, 0.55, 6))):
            for i in range(n):
                x = 840 + (i + 0.5 * (fila % 2)) * (1500 / n)
                RP.copia_mini(h, x, yy, sc, t, sem=5300 + fila * 30 + i, cara="neutro", brillo=0.9, d=-1, tono=44)
        h.luz_radial(1500, 500, 1200, h.pal["verde"], k=0.5)
        # la reflexión del cristal (franjas diagonales)
        for q in range(3):
            h.emitir(np.array([(900 + q * 480, 20), (960 + q * 480, 20), (760 + q * 480, 860), (700 + q * 480, 860)], float), 0.05, col=h.pal["luna"], blur=8)
        # el escritorio y el ingeniero que firma
        h.pieza(C.rect(120, 820, 800, 70), 70, 5400, w=6, luz=(0.3, -1), d=14, trama=0.5, rim=0.9, rampa="madera")
        h.pieza(C.rect(160, 890, 720, 400), 44, 5401, w=6, luz=(0.3, -1), d=14, trama=0.5, rim=0.7, rampa="madera")
        gest = 0.5 + 0.5 * math.sin(t * 2.0)
        self.ing.dibujar(h, dict(x=380, y=1030, s=1.05, d=1, bata=False, tono=60, gafas=True, brazo=0.6 + 0.2 * gest, cabeza=0.3,
                                 luz=(0.4, -1)))
        K.hoja(h, 520, 800, 360, 220, ang=-0.04, sem=5410, tono=226, renglones=4, y0=0.3, sep=24, margen=24, s=0.8)
        K.garabato(h, 420, 808, clamp01((t - tb[7] - 1.6) / 1.2), s=0.7, sem=5411, ancho=200)
        h.luz_cono(420, -300, math.pi / 2, 0.6, 1400, h.pal["lampara"], k=1.4, suave=0.6)
        h.luz_radial(1500, 500, 1500, h.pal["verde"], k=0.5)
        C.ambiente(h, 0.5)
        C.banda(h, "SUS PROPIOS MODELOS", 960, 1000, 52, t, self.t_modelos - 0.3, sem=54)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.08, sem=138), bloom=0.6)

    # ------------------------------------------------------------------ I. una semana tachada
    def p_semana(self, h, t, u):
        tb = self.tb
        dur = tb[9] - tb[8]
        h.camara(1.0 + 0.08 * u / dur, 960, 540, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("madera", 341), h, 1.0, rampa="madera")
        K.hoja(h, 960, 540, 1500, 640, ang=-0.01, sem=5500, tono=228, renglones=0, s=1.0)
        N.texto_maquina(h, "JULIO · SEMANA 29", 960, 290, 48, t, tb[8] + 0.1, cps=24, tono=0.06, centro=True, fuente=C.IMPACT, encuadrar=False)
        dias = ("L", "M", "X", "J", "V", "S", "D")
        tinta = tuple(h.c(120, "lacre"))
        for i in range(7):
            x = 280 + i * 200
            h.pieza(C.rect(x - 80, 360, 160, 260), 238, 5510 + i, w=3, luz=(0.3, -1), d=2, trama=0, rim=0.3, rampa="papel")
            N.texto_maquina(h, f"{12 + i}", x, 450, 60, t, -99, cps=1e9, tono=0.06, centro=True, fuente=C.IMPACT, encuadrar=False)
            N.texto_maquina(h, dias[i], x, 390, 28, t, -99, cps=1e9, tono=0.2, centro=True, encuadrar=False)
            ti = self.t_semana - 0.2 + 0.3 * i
            a = clamp01((t - ti) / 0.2)
            if a > 0:
                h.trazo(np.array([[x - 70, 370], [x - 70 + 140 * a, 370 + 240 * a]]), 11, 5520 + i * 2, color=tinta, jit=0.5, taper=(0.1, 0.1))
                h.trazo(np.array([[x + 70, 370], [x + 70 - 140 * a, 370 + 240 * a]]), 11, 5521 + i * 2, color=tinta, jit=0.5, taper=(0.1, 0.1))
        h.luz_cono(960, -300, math.pi / 2, 0.7, 1500, h.pal["lampara"], k=1.4, suave=0.6)
        C.ambiente(h, 0.34)
        C.banda(h, "UNA SEMANA ENTERA", 960, 1000, 54, t, self.t_semana, sem=55)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=139), bloom=0.5)

    # ------------------------------------------------------------------ J. despachos a oscuras
    def p_despachos(self, h, t, u):
        tb = self.tb
        dur = self.t1 - tb[9]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.2 * k, 960, 560, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(M.despachos_velas(), h, 1.0, rampa="piedra", oscuro=1.9)
        # velas sobre los escritorios (cada una ilumina su cubículo) y personas con linterna
        for i, (x, y, s) in enumerate(((420, 900, 1.0), (1480, 840, 0.8), (880, 700, 0.5), (1150, 620, 0.35))):
            NF.vela(h, t, x, y, s, sem=5600 + i * 9, alto=150, k=1.0, luz=1.0, alcance=700)
        for i, (x, y, s) in enumerate(((660, 1120, 1.5), (1700, 1000, 1.2), (1000, 760, 0.7))):
            K.persona(h, x, y, s, sem=5650 + i * 7, tono=22, bal=4 * math.sin(t * 0.8 + i), brazo=0.0, sombrero=bool(i % 2), rim=0.8)
            h.luz_cono(x + 30, y - 330 * s, 0.3 * (-1) ** i, 0.25, 600 * s, h.pal["luna"], k=0.7, suave=0.5)
        h.luz_cono(200, -200, math.pi / 2 - 0.5, 0.5, 1500, h.pal["luna"], k=0.7, suave=0.6)
        C.ambiente(h, 0.45)
        C.banda(h, "A OSCURAS EN SUS PROPIOS DESPACHOS", 960, 1000, 46, t, self.t_oscuras, sem=56)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.14, sem=140), bloom=0.8)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        tb = self.tb
        self.ev(tb[0] + 0.2, "reloj_pared", 0.4, 0.0, dur=3.2)
        self.ev(tb[1] + 0.3, "zumbido_servidores", 0.35, 0.0, dur=2.0)
        self.ev(self.t_tiro - 0.05, "interruptor", 0.8, 0.0)
        self.ev(self.t_tiro + 0.1, "electricidad", 0.6, 0.2, dur=0.8)
        self.ev(tb[2] + 0.2, "apagado_vela", 0.4, 0.0)
        self.ev(tb[3] + 0.4, "perillas", 0.3, 0.0, dur=3.0)
        self.ev(self.t_puertas + 0.25, "apagado_vela", 0.5, 0.0)
        self.ev(tb[5] + 0.3, "tecleo_rapido", 0.35, 0.0, dur=3.0)
        self.ev(self.t_denunc + 0.8, "sello_golpe", 0.6, 0.0)
        self.ev(tb[6] + 0.3, "carro_maquina", 0.4, 0.0, dur=4.0)
        self.ev(self.t_preocup + 0.2, "sello_golpe", 0.4, 0.0)
        self.ev(tb[7] + 0.3, "pluma", 0.4, 0.0, dur=2.0)
        self.ev(tb[8] + 0.3, "lapiz", 0.4, 0.0, dur=3.0)
        self.ev(tb[9] + 0.3, "grave_inquietante", 0.4, 0.0, dur=3.5)
        self.ev(self.t1 - 0.7, "tinta_mancha", 0.45, 0.0, dur=0.8)
