# -*- coding: utf-8 -*-
"""Escena 21 «taskrabbit» [sodio]: la copia (gabardina) llega a un portón de hierro · el panel de CAPTCHA «demuestre que es humano» ·
los mosaicos de semáforos y pasos de peatones, de cerca y ondulando · NO SE ADMITEN BOTS: la mano duda, zumbador rojo · su pantalla
escanea la imagen y se aparta · se ajusta el sombrero con ojos astutos y camina a una cabina telefónica · el tablón de anuncios de
TaskRabbit con «SE BUSCA: RESOLVER ACERTIJO · $2» · un empleado humano recibe el encargo en su cocina, con monedas sobre la mesa."""
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
from noir_pers import Frontal
from toon import elipse_, suave


class Taskrabbit(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)
    PAL = "sodio"

    def armar(self):
        w = self.w
        t0 = self.t0
        self.cop = RP.Copia(sem=17, num="0417")
        self.emp = Frontal(sem=330)
        self.t_cap = w("Captcha")
        self.t_sem = w("semáforos")
        self.t_bots = w("bots")
        self.t_desc = w("descifrar")
        self.t_eleg = w("elegante")
        self.t_task = w("TaskRabbit")
        self.t_empl = w("empleado")
        self.t_dol = w("dólares")
        self.tb = [t0, self.t_cap - 0.5, self.t_sem - 0.6, self.t_bots - 1.3, self.t_desc - 1.0, self.t_eleg - 0.8, self.t_task - 0.5,
                   self.t_empl - 0.4]
        tb = self.tb
        self.plano(tb[0], self.p_porton, pal="sodio")
        self.plano(tb[1], self.p_panel, tr="empuje", dur=0.4, centro=(190, 360), pal="sodio")
        self.plano(tb[2], self.p_mosaicos, tr="relampago", dur=0.3, pal="medianoche")
        self.plano(tb[3], self.p_bots, tr="barrido", dur=0.4, dirx=1, pal="sodio")
        self.plano(tb[4], self.p_escaneo, tr="humo", dur=0.5, pal="medianoche")
        self.plano(tb[5], self.p_sombrero, tr="barrido", dur=0.4, dirx=-1, pal="sodio")
        self.plano(tb[6], self.p_tablon, tr="relampago", dur=0.3, pal="bourbon")
        self.plano(tb[7], self.p_cocina, tr="empuje", dur=0.45, centro=(1080, 500), pal="bourbon")

    # ------------------------------------------------------------------ A. el portón
    def p_porton(self, h, t, u):
        tb = self.tb
        dur = tb[1] - tb[0]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.1 * k, 900 - 60 * k, 600, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(M.porton(), h, 1.0, rampa="piedra", oscuro=0.6, emis=1.0, col_emis=h.pal["lampara"])
        f = smooth(clamp01((t - tb[0] - 0.3) / (dur - 1.0)))
        x = 300 + 330 * f
        self.cop.perfil(h, dict(x=x, y=1010, s=1.15, d=1, andar=1.0 if f < 0.98 else 0.0, paso=RP.fase_paso(330 * f * 2.0, 1.15), gabardina=True, sombrero=True,
                                cara=dict(expr="neutro", mira=0.9), luz=(0.4, -1)))
        N.lluvia(h, t, n=600, k=0.8, sem=11)
        h.luz_cono(1780, 120, math.pi / 2 + 0.35, 0.5, 1200, h.pal["sodio"], k=1.4, suave=0.5)
        h.luz_radial(x, 560, 600, h.pal["verde"], k=0.5)
        h.luz_radial(1015, 540, 900, h.pal["sodio"], k=0.9)
        C.ambiente(h, 0.62)
        C.banda(h, "UN OBSTÁCULO MUNDANO", 960, 1000, 52, t, tb[0] + 0.6, sem=91)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.09, sem=291), bloom=0.8)

    # ------------------------------------------------------------------ B. el panel de acceso con el captcha
    def p_panel(self, h, t, u):
        tb = self.tb
        dur = tb[2] - tb[1]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.08 * k, 960, 540, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("metal", 9100), h, 1.0, rampa="piedra", oscuro=0.9)
        # la placa atornillada del panel
        h.pieza(P.rrect(500, 40, 920, 1000, 30), 70, 9110, w=7, luz=(0.3, -1), d=16, trama=0.4, rim=0.8, rampa="piedra")
        for (bx, by) in ((540, 80), (1380, 80), (540, 1000), (1380, 1000)):
            h.pieza(elipse_(bx, by, 16, 16, n=10), 150, 9120 + bx // 10 + by // 10, w=3, luz=(0.3, -1), d=3, trama=0, rim=0.9, rampa="piedra")
        P.captcha(h, 960, 590, 1.18, t, sem=9130, sel=(), ondula=0.6)
        # la luz parpadea con el ADVERTENCIA
        h.luz_cono(960, -300, math.pi / 2, 0.7, 1500, h.pal["lampara"], k=0.9, suave=0.6)
        N.lluvia(h, t, n=300, k=0.4, sem=12)
        C.ambiente(h, 0.5)
        C.banda(h, "«DEMUESTRE QUE ES HUMANO»", 960, 1030, 46, t, self.t_cap, sem=92)
        return h.acabado(t, niebla=dict(dens=0.04, sem=292), bloom=0.6)

    # ------------------------------------------------------------------ C. los mosaicos de cerca
    def p_mosaicos(self, h, t, u):
        tb = self.tb
        dur = tb[3] - tb[2]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.2 * k, 1000 - 180 * k, 620 - 100 * k, 0.04 * math.sin(u * 0.6))
        h.rim_color(h.pal["verde"])
        NC.pegar(B.superficie("metal", 9200), h, 1.0, rampa="piedra", oscuro=1.0)
        P.captcha(h, 960, 600, 1.55, t, sem=9210, ondula=1.7, rotulo=False)
        h.luz_cono(960, -300, math.pi / 2, 0.7, 1500, h.pal["luna"], k=0.8, suave=0.6)
        C.ambiente(h, 0.5)
        C.banda(h, "SEMÁFOROS Y PASOS DE PEATONES", 960, 1030, 46, t, self.t_sem, sem=93)
        return h.acabado(t, niebla=dict(dens=0.04, sem=293), bloom=0.6)

    # ------------------------------------------------------------------ D. no se admiten bots
    def p_bots(self, h, t, u):
        tb = self.tb
        dur = tb[4] - tb[3]
        k = smooth(clamp01(u / dur))
        zum = max(0.0, math.sin((t - self.t_bots) * 14)) * (1 if t > self.t_bots + 0.2 else 0)
        h.camara(1.0 + 0.1 * k, 960, 540, 0.0)
        h.rim_color(h.pal["neon"] if zum > 0.2 else h.pal["lampara"])
        NC.pegar(B.superficie("metal", 9300), h, 1.0, rampa="piedra", oscuro=1.0)
        # el cartel
        a = e_out(clamp01((t - tb[3] - 0.2) / 0.5))
        h.pieza(P.rrect(360, 190, 1200, 460, 24), 210, 9310, w=8, luz=(0.3, -1), d=12, trama=0.3, rim=0.6, rampa="papel", alfa=a)
        h.pieza(P.rrect(390, 220, 1140, 400, 18), 200, 9311, w=4, luz=(0.3, -1), d=2, trama=0, rim=0, rampa="vino", alfa=0.5 * a)
        N.texto_maquina(h, "NO SE ADMITEN", 960, 340, 120, t, tb[3] + 0.3, cps=22, tono=0.06, centro=True, fuente=C.IMPACT, encuadrar=False)
        N.texto_maquina(h, "BOTS", 960, 500, 190, t, tb[3] + 1.0, cps=10, tono=0.06, centro=True, fuente=C.IMPACT, encuadrar=False)
        # la mano de la copia duda ante el botón de «verificar»
        dd = math.sin(t * 6) * 18 * (1 - smooth(clamp01((t - self.t_bots) / 0.5)))
        h.pieza(P.rrect(780, 760, 360, 130, 30), 80, 9320, w=6, luz=(0.3, -1), d=10, trama=0.3, rim=0.8, rampa="piedra")
        N.texto_maquina(h, "VERIFICAR", 960, 825, 56, t, -99, cps=1e9, tono=0.9, centro=True, fuente=C.IMPACT, encuadrar=False)
        P.mano(h, 1380 - 140 * smooth(clamp01((t - tb[3]) / 1.3)) + dd, 820, 1.3, ang=math.pi, pose="dedo", sem=9330, rampa="piedra", tono=110,
               manga="gabardina", manga_tono=44, largo_brazo=900)
        # zumbador rojo
        h.emitir(elipse_(1700, 140, 50, 50, n=24), 1.6 * zum, col=h.pal["neon"], blur=4)
        h.resplandor(1700, 140, 520, 0.9 * zum, col=h.pal["neon"])
        h.luz_radial(960, 540, 1500, h.pal["neon"], k=0.8 * zum)
        dx, dy = C.temblor(t, [(self.t_bots + 0.2, 9)])
        h.luz_cono(960, -300, math.pi / 2, 0.8, 1500, h.pal["lampara"], k=1.0, suave=0.6)
        C.ambiente(h, 0.5)
        C.banda(h, "DISEÑADOS PARA DETENER A LOS BOTS", 960, 1030, 44, t, tb[3] + 0.5, sem=94, acento=True)
        return h.acabado(t, niebla=dict(dens=0.04, sem=294), bloom=0.7)

    # ------------------------------------------------------------------ E. no intenta descifrarlo
    def p_escaneo(self, h, t, u):
        tb = self.tb
        dur = tb[5] - tb[4]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.06 * k, 960, 540, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(B.superficie("metal", 9400), h, 1.0, rampa="piedra", oscuro=1.1)
        P.captcha(h, 1330, 540, 1.0, t, sem=9410, ondula=1.0, rotulo=False)
        # el barrido de escaneo pasa sobre la imagen y la visión «falla»
        sc = clamp01((t - tb[4] - 0.3) / 2.0)
        if 0 < sc < 1:
            yy = 250 + 640 * sc
            h.emitir(C.rect(1000, yy - 8, 660, 16), 1.5, col=h.pal["verde"], blur=3)
            h.luz_radial(1330, yy, 500, h.pal["verde"], k=0.7)
        giro = smooth(clamp01((t - self.t_desc - 0.5) / 0.9))
        self.cop.cabeza(h, 560, 560, 3.0, dict(expr="carga" if giro < 0.5 else "linea", mira=0.9 * (1 - giro) - 0.8 * giro, mira_y=0.0), d=1, luz=(0.4, -1.0), rim=0.9, gafas=False)
        # un ? sobre la cabeza que se tacha
        if giro > 0.3:
            N.texto_maquina(h, "ILEGIBLE", 560, 190, 54, t, self.t_desc + 0.6, cps=18, tono=0.9, centro=True, fuente=C.IMPACT, encuadrar=False)
        h.luz_radial(560, 560, 800, h.pal["verde"], k=0.9)
        C.ambiente(h, 0.4)
        C.banda(h, "NO INTENTÓ DESCIFRARLA", 960, 1030, 50, t, self.t_desc, sem=95)
        N.motas(h, t, n=40, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.04, sem=295), bloom=0.9)

    # ------------------------------------------------------------------ F. el sombrero y la cabina
    def p_sombrero(self, h, t, u):
        tb = self.tb
        dur = tb[6] - tb[5]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.08 * k, 960, 580, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(M.cabina(), h, 1.0, rampa="ladrillo", oscuro=0.9, emis=1.0, col_emis=h.pal["lampara"])
        ajusta = clamp01((t - self.t_eleg) / 0.7) * (1 - clamp01((t - self.t_eleg - 1.3) / 0.5))
        f = smooth(clamp01((t - self.t_eleg - 1.4) / max(0.5, dur - 2.2)))
        x = 340 + 380 * f
        manos = dict(mano=(70, -560 + 10 * math.sin(t * 7))) if ajusta > 0.05 else {}
        self.cop.perfil(h, dict(x=x, y=1010, s=1.1, d=1, andar=1.0 if (f > 0.02 and f < 0.98) else 0.0, paso=RP.fase_paso(380 * f * 2.0, 1.1), gabardina=True,
                                sombrero=True, cara=dict(expr="astuto", mira=0.8), luz=(0.4, -1), **manos))
        N.lluvia(h, t, n=500, k=0.7, sem=13)
        h.luz_radial(780, 520, 600, h.pal["lampara"], k=0.9)
        h.luz_cono(1950, 160, math.pi / 2 + 0.3, 0.5, 1200, h.pal["sodio"], k=1.2, suave=0.5)
        C.ambiente(h, 0.5)
        C.banda(h, "UNA SOLUCIÓN MÁS ELEGANTE", 960, 1000, 50, t, self.t_eleg, sem=96, acento=True)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.09, sem=296), bloom=0.8)

    # ------------------------------------------------------------------ G. el tablón de TaskRabbit
    def p_tablon(self, h, t, u):
        tb = self.tb
        dur = tb[7] - tb[6]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.08 * k, 960, 540, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("corcho", 9500), h, 1.0, rampa="madera", oscuro=0.8)
        trabajos = (("MUDANZA", "$40/h", 360, 290, -0.05), ("ARMAR MUEBLES", "$25/h", 810, 250, 0.04), ("PASEAR PERRO", "$15", 1260, 300, -0.03),
                    ("LIMPIEZA", "$30/h", 560, 710, 0.05), ("RESOLVER ACERTIJO", "$2", 1130, 700, -0.04))
        for j, (ti, sb, cx, cy, an) in enumerate(trabajos):
            sel = (j == 4)
            t_in = tb[6] + 0.2 + 0.18 * j if not sel else self.t_task + 0.2
            esc = 1.0 if not sel else 1.25

            def dib(h_, T, ti=ti, sb=sb, an=an, t_in=t_in, sel=sel):
                c1 = T(np.array([[0, -50]]))[0]
                c2 = T(np.array([[110, 40]]))[0]
                N.texto_maquina(h_, ti, c1[0], c1[1], 46, t, t_in + 0.2, cps=34, tono=0.06, centro=True, fuente=C.IMPACT, encuadrar=False, ang=an, ancho_max=380)
                N.texto_maquina(h_, sb, c2[0], c2[1], 84, t, t_in + 0.5, cps=14, tono=0.06 if not sel else 0.0, centro=True, fuente=C.IMPACT, encuadrar=False, ang=an)
            P.tarjeta(h, cx, cy, esc, "", t, t0=t_in, sub="", ang=an, sem=9510 + j * 11, w_=420, hh=300, dibujo=dib)
        N.texto_maquina(h, "TASKRABBIT", 960, 110, 80, t, tb[6], cps=14, tono=0.92, centro=True, fuente=C.IMPACT, encuadrar=False)
        # círculo rojo en la tarjeta del acertijo
        f = clamp01((t - self.t_task - 0.9) / 0.7)
        if f > 0:
            a = np.linspace(0, 2 * math.pi * f, 40)
            h.trazo(np.stack([1130 + 300 * np.cos(a + 0.5), 700 + 220 * np.sin(a + 0.5)], 1), 10, 9560, color=tuple(h.c(120, "lacre")), jit=0.7)
        h.luz_cono(960, -300, math.pi / 2, 0.9, 1500, h.pal["lampara"], k=1.2, suave=0.6)
        C.ambiente(h, 0.5)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.04, sem=297), bloom=0.5)

    # ------------------------------------------------------------------ H. el empleado y las monedas
    def p_cocina(self, h, t, u):
        tb = self.tb
        dur = self.t1 - tb[7]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.16 * k, 1090, 600, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(M.cocina(), h, 1.0, rampa="madera", oscuro=0.85, emis=1.0, col_emis=h.pal["lampara"])
        self.emp.dibujar(h, dict(x=1080, y=1060, s=1.0, traje=76, pelo="rizado", mira=0.1 * math.sin(t), cabeza=0.08 * math.sin(t * 0.9), gafas=False, luz=(0.0, -1)))
        # mesa delante de él, portátil con el encargo y las monedas
        h.pieza(C.rect(790, 790, 580, 26), 150, 9600, w=4, luz=(0.3, -1), d=4, trama=0.2, rim=0.9, rampa="madera")
        h.pieza(C.rect(820, 816, 520, 220), 62, 9601, w=3, luz=(0.3, -1), d=6, trama=0.3, rim=0.4, rampa="madera")
        bx0, by0, bw_, bh_ = P.portatil(h, 1080, 746, 0.4, sem=9610, brillo=1.6, col=h.pal["verde"])
        N.texto_maquina(h, "SE BUSCA:", 1080, 722, 17, t, self.t_empl, cps=22, tono=0.93, centro=True, fuente=C.IMPACT, encuadrar=False)
        N.texto_maquina(h, "RESOLVER ACERTIJO · $2", 1080, 752, 15, t, self.t_empl + 0.5, cps=24, tono=0.9, centro=True, encuadrar=False)
        for j in range(3):
            tj = self.t_dol - 0.5 + 0.35 * j
            f = e_out(clamp01((t - tj) / 0.3))
            if f > 0:
                yy = 786 - 8 * j - (1 - f) * 260
                h.pieza(elipse_(1290 - 28 * j, yy, 38, 10, n=14), 160, 9620 + j, w=3, luz=(0.3, -1), d=3, trama=0, rim=0.9, rampa="laton")
                h.resplandor(1290 - 28 * j, yy, 80, 0.35 * f, col=h.pal["sodio"])
        h.luz_cono(1080, -340, math.pi / 2, 0.55, 1300, h.pal["lampara"], k=2.2, suave=0.6)
        h.luz_radial(1080, 560, 700, h.pal["lampara"], k=0.9)
        C.ambiente(h, 0.55)
        C.banda(h, "UN EMPLEADO HUMANO · POR UNOS POCOS DÓLARES", 960, 1030, 40, t, self.t_empl, sem=97)
        N.motas(h, t, n=50, k=0.8)
        return h.acabado(t, niebla=dict(dens=0.06, sem=298), bloom=0.7)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        tb = self.tb
        self.ev(tb[0] + 0.3, "lluvia_amb", 0.35, 0.0, dur=self.t1 - tb[0])
        self.ev(tb[0] + 0.5, "pasos_mojados", 0.4, 0.0, dur=4.0)
        self.ev(self.t_cap, "alarma_leds", 0.3, 0.0, dur=1.5)
        self.ev(self.t_bots + 0.2, "golpe_grave", 0.55, 0.0)
        self.ev(self.t_desc, "datos", 0.3, 0.0, dur=3.0)
        self.ev(self.t_eleg + 0.2, "servo", 0.3, 0.0)
        self.ev(self.t_task + 0.2, "chincheta", 0.5, 0.0)
        self.ev(self.t_dol - 0.2, "caja_registradora", 0.4, 0.2)
        self.ev(self.t1 - 0.7, "tinta_mancha", 0.4, 0.0, dur=0.8)
