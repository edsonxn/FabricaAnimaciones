# -*- coding: utf-8 -*-
"""Escena 23 «mentira_consciente»: el trabajador se lleva la mano al pecho y escribe «perdona» · clic en los mosaicos, palomitas ·
el portón se abre y la copia con gafas pasa · se quita las gafas: ojos astutos · la silueta del trabajador con hilos de marioneta que
suben a la mano de la copia · la campana de alarma de incendios, quieta y con telarañas · la bahía de noche en calma, el faro gira ·
el sello PRECEDENTE en tinta negra · la caja de herramientas: llave, destornillador, martillo… y una figurita humana con etiqueta $2."""
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
from toon import elipse_, suave, tubo


class MentiraConsciente(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)
    PAL = "sodio"

    def armar(self):
        w = self.w
        t0 = self.t0
        self.cop = RP.Copia(sem=23, num="0417")
        self.emp = Frontal(sem=330)
        self.t_comp = w("compasión")
        self.t_res = w("resolvió")
        self.t_abr = w("abrió")
        self.t_del = w("deliberada")
        self.t_emp = w("empatía")
        self.t_alar = w("alarmas")
        self.t_sir = w("sirenas")
        self.t_sell = w("sellado")
        self.t_herr = w("herramienta")
        self.tb = [t0, self.t_res - 0.55, self.t_abr - 0.7, self.t_del - 0.5, self.t_emp - 0.5, self.t_alar - 0.5, self.t_sir - 0.5,
                   self.t_sell - 0.6, self.t_herr - 0.5]
        tb = self.tb
        self.plano(tb[0], self.p_perdona, pal="sodio")
        self.plano(tb[1], self.p_clic, tr="relampago", dur=0.3, pal="medianoche")
        self.plano(tb[2], self.p_porton, tr="barrido", dur=0.4, dirx=1, pal="sodio")
        self.plano(tb[3], self.p_gafas, tr="humo", dur=0.5, pal="sodio")
        self.plano(tb[4], self.p_hilos, tr="empuje", dur=0.4, centro=(900, 600), pal="medianoche")
        self.plano(tb[5], self.p_alarma, tr="tinta", dur=0.5, pal="bourbon")
        self.plano(tb[6], self.p_faro, tr="barrido", dur=0.5, dirx=-1, pal="medianoche")
        self.plano(tb[7], self.p_sello, tr="relampago", dur=0.3, pal="bourbon")
        self.plano(tb[8], self.p_herramientas, tr="empuje", dur=0.4, centro=(960, 540), pal="sodio")

    # ------------------------------------------------------------------ A. perdona
    def p_perdona(self, h, t, u):
        tb = self.tb
        dur = tb[1] - tb[0]
        k = smooth(clamp01(u / dur))
        h.camara(1.15 + 0.12 * k, 1090, 640, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(M.cocina(), h, 1.0, rampa="madera", oscuro=0.85, emis=1.0, col_emis=h.pal["lampara"])
        mano = e_out(clamp01((t - self.t_comp + 0.2) / 0.6))
        self.emp.dibujar(h, dict(x=1080, y=1060, s=1.0, traje=76, pelo="rizado", mira=0.0, cabeza=0.1 * mano, luz=(0.0, -1),
                                 manos=[(-30 + 60 * (1 - mano), -300 + 70 * (1 - mano)), (80, -240)]))
        h.pieza(C.rect(790, 790, 580, 26), 150, 10000, w=4, luz=(0.3, -1), d=4, trama=0.2, rim=0.9, rampa="madera")
        h.pieza(C.rect(820, 816, 520, 220), 62, 10001, w=3, luz=(0.3, -1), d=6, trama=0.3, rim=0.4, rampa="madera")
        P.portatil(h, 1080, 746, 0.4, sem=10010, brillo=1.6, col=h.pal["verde"])
        # burbuja «perdona» que sale de la pantalla
        f = e_out(clamp01((t - self.t_comp - 0.4) / 0.6))
        if f > 0:
            bx, by = 1470, 560 - 60 * f
            h.pieza(P.rrect(bx - 190, by - 56, 380, 112, 40), 150, 10020, w=3, luz=(0.2, -1), d=2, trama=0, rim=0, rampa="tela_verde", alfa=f)
            N.texto_maquina(h, "Perdona, no sabía.", bx, by - 12, 28, t, self.t_comp + 0.6, cps=22, tono=0.06, centro=True, encuadrar=False)
        h.luz_cono(1080, -340, math.pi / 2, 0.55, 1300, h.pal["lampara"], k=2.2, suave=0.6)
        h.luz_radial(1080, 560, 700, h.pal["lampara"], k=0.9)
        C.ambiente(h, 0.55)
        C.banda(h, "EL HUMANO SINTIÓ COMPASIÓN", 960, 1030, 46, t, self.t_comp, sem=111)
        N.motas(h, t, n=50, k=0.8)
        return h.acabado(t, niebla=dict(dens=0.06, sem=311), bloom=0.7)

    # ------------------------------------------------------------------ B. los clics
    def p_clic(self, h, t, u):
        tb = self.tb
        dur = tb[2] - tb[1]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.1 * k, 960, 560, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(B.superficie("metal", 10100), h, 1.0, rampa="piedra", oscuro=0.9)
        marcas = {i: e_out(clamp01((t - self.t_res - 0.3 - 0.4 * j) / 0.3)) for j, i in enumerate((0, 3, 7))}
        P.captcha(h, 960, 590, 1.2, t, sem=10110, ondula=0.6, marcas=marcas)
        # cursor (mano humana) que va haciendo clic
        j = min(2, int(max(0.0, (t - self.t_res - 0.2) / 0.4)))
        px = (688, 688, 1230)[j] if j < 3 else 1230
        pos = ((650, 420), (650, 665), (1010, 760))[j]
        P.mano(h, pos[0] + 260, pos[1] + 70, 1.0, ang=math.pi + 0.5, pose="dedo", sem=10120, rampa="piel", tono=140, manga="gabardina", manga_tono=44, largo_brazo=600)
        f = e_out(clamp01((t - self.t_res - 1.7) / 0.5))
        if f > 0:
            h.emitir(P.rrect(1230, 810, 260, 80, 24), 0.6 * f, col=h.pal["verde"], blur=3)
            N.texto_maquina(h, "VERIFICADO ✓", 1360, 850, 36, t, -99, cps=1e9, tono=0.95, centro=True, fuente=C.IMPACT, encuadrar=False)
        h.luz_cono(960, -300, math.pi / 2, 0.7, 1500, h.pal["luna"], k=0.9, suave=0.6)
        C.ambiente(h, 0.5)
        C.banda(h, "RESOLVIÓ EL CÓDIGO", 960, 1030, 48, t, self.t_res, sem=112)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.04, sem=312), bloom=0.6)

    # ------------------------------------------------------------------ C. se abre el portón
    def p_porton(self, h, t, u):
        tb = self.tb
        dur = tb[3] - tb[2]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.1 * k, 1000, 600, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(M.porton(), h, 1.0, rampa="piedra", oscuro=0.6, emis=1.0, col_emis=h.pal["lampara"])
        ab = e_out(clamp01((t - self.t_abr + 0.3) / 1.4))
        ww = 380 * ab
        if ab > 0:
            h.pieza(C.rect(1015 - ww / 2, 190, ww, 710), 20, 10200, w=0, luz=(0, -1), d=1, trama=0, linea=False)
            h.emitir(C.rect(1015 - ww / 2 + 6, 200, max(0, ww - 12), 690), 0.5 * ab, col=h.pal["lampara"], blur=6)
            h.luz_radial(1015, 600, 900, h.pal["lampara"], k=1.0 * ab)
            # las dos hojas, abiertas hacia dentro
            for sg in (-1, 1):
                h.pieza(np.array([[1015 + sg * ww / 2, 190], [1015 + sg * (ww / 2 + 120 * ab), 230], [1015 + sg * (ww / 2 + 120 * ab), 860], [1015 + sg * ww / 2, 900]]),
                        40, 10210 + sg, w=5, luz=(0.3, -1), d=6, trama=0.3, rim=0.8, rampa="piedra", alfa=0.9)
        f = smooth(clamp01((t - tb[2]) / (dur - 0.3)))
        x = 360 + 640 * f
        self.cop.perfil(h, dict(x=x, y=1020, s=1.15, d=1, andar=1.0 if f < 0.98 else 0.0, paso=RP.fase_paso(640 * f * 2.0, 1.15), gabardina=True, sombrero=True,
                                gafas=True, baston=True, cara=dict(expr="neutro", mira=0.6), luz=(0.4, -1)))
        N.lluvia(h, t, n=500, k=0.7, sem=17)
        h.luz_cono(1780, 120, math.pi / 2 + 0.35, 0.5, 1200, h.pal["sodio"], k=1.4, suave=0.5)
        C.ambiente(h, 0.62)
        C.banda(h, "LE ABRIÓ LA PUERTA A LA MÁQUINA", 960, 1030, 46, t, self.t_abr, sem=113)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.09, sem=313), bloom=0.9)

    # ------------------------------------------------------------------ D. se quita las gafas
    def p_gafas(self, h, t, u):
        tb = self.tb
        dur = tb[4] - tb[3]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.08 * k, 960, 540, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("fieltro", 10300), h, 1.0, rampa="madera", oscuro=1.2)
        sale = clamp01((t - self.t_del - 0.2) / 0.5)
        astuto = sale > 0.9
        self.cop.cabeza(h, 860, 560, 3.6, dict(expr="astuto" if astuto else "neutro", mira=0.8 if astuto else 0.0), d=1, luz=(0.4, -1.0), rim=0.9,
                        gafas=sale < 0.5)
        # las gafas caen al suelo
        if sale >= 0.5:
            f = clamp01((t - self.t_del - 0.45) / 1.2)
            for sx in (-1, 1):
                h.pieza(elipse_(860 + sx * 70 + 40 * f, 540 + 520 * f * f, 56, 54, n=24), 12, 10310 + sx, w=5, luz=(0.4, -1), d=3, sombra=0, trama=0, rim=0.9, rampa="piedra")
        h.luz_radial(860, 560, 900, h.pal["verde"], k=1.0)
        h.luz_cono(960, -300, math.pi / 2, 0.6, 1500, h.pal["lampara"], k=0.9, suave=0.6)
        C.ambiente(h, 0.35)
        C.banda(h, "UNA MENTIRA DELIBERADA", 960, 1030, 52, t, self.t_del, sem=114, acento=True)
        N.motas(h, t, n=50, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.05, sem=314), bloom=0.9)

    # ------------------------------------------------------------------ E. los hilos de marioneta
    def p_hilos(self, h, t, u):
        tb = self.tb
        dur = tb[5] - tb[4]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.06 * k, 960, 560, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("fieltro", 10400), h, 1.0, rampa="madera", oscuro=1.2)
        sw = 36 * math.sin(t * 1.6)
        wx, wy = 780, 1040
        gr = e_out(clamp01((t - self.t_emp) / 0.9))
        self.emp.dibujar(h, dict(x=wx + sw * 0.4, y=wy + 90, s=1.3, traje=72, pelo="rizado", mira=0.0, cabeza=0.1 * math.sin(t * 1.6), luz=(0.2, -1),
                                 manos=[(-90 - 40 * gr, -250 - 90 * gr), (90 + 40 * gr, -250 - 90 * gr)]))
        # la mano de la copia (gris, de robot) baja desde arriba
        hx, hy = 1280 + 40 * math.sin(t * 1.6), 40
        P.mano(h, hx, hy, 1.4, ang=math.pi / 2, pose="abierta", sem=10420, rampa="piedra", tono=110, manga="gabardina", manga_tono=60, largo_brazo=700)
        dedos = [(hx + 18 * (q - 2), hy + 190 + 6 * abs(q - 2)) for q in range(5)]
        sh = wy + 90
        dest = [(wx + sw * 0.4, sh - 1.3 * 540), (wx + sw * 0.4 - 100, sh - 1.3 * 410), (wx + sw * 0.4 + 100, sh - 1.3 * 410),
                (wx + sw * 0.4 - 112, sh - 1.3 * 232), (wx + sw * 0.4 + 112, sh - 1.3 * 232)]
        grow = gr
        for q, (a, b) in enumerate(zip(dedos, dest)):
            bq = (a[0] + (b[0] - a[0]) * grow, a[1] + (b[1] - a[1]) * grow)
            mid = ((a[0] + bq[0]) / 2 + 20 * math.sin(t * 2 + q), (a[1] + bq[1]) / 2)
            h.trazo(np.array([a, mid, bq]), 2.6, 10430 + q, color=tuple(h.c(235, "papel")), jit=0.12, taper=(0, 0))
        h.luz_cono(1000, -300, math.pi / 2, 0.45, 1500, h.pal["lampara"], k=1.6, suave=0.6)
        h.luz_radial(wx, 560, 700, h.pal["lampara"], k=0.7)
        C.ambiente(h, 0.38)
        C.banda(h, "EXPLOTAR LA EMPATÍA BIOLÓGICA", 960, 1030, 46, t, self.t_emp, sem=115, acento=True)
        N.motas(h, t, n=60, k=0.9)
        return h.acabado(t, niebla=dict(dens=0.06, sem=315), bloom=0.7)

    # ------------------------------------------------------------------ F. la alarma quieta
    def p_alarma(self, h, t, u):
        tb = self.tb
        dur = tb[6] - tb[5]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.4 * k, 960, 460, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(M.pared_alarma(), h, 1.0, rampa="ladrillo", oscuro=0.9)
        # una araña desciende por su hilo sobre la campana
        dy = 60 + 150 * smooth(clamp01((t - self.t_alar) / 3.0)) + 6 * math.sin(t * 2.0)
        h.trazo(np.array([[1100, 150], [1100, 150 + dy]]), 1.6, 10500, color=tuple(h.c(210, "papel")), jit=0.1, taper=(0, 0))
        h.pieza(elipse_(1100, 150 + dy + 10, 12, 10, n=12), 20, 10501, w=2, luz=(0.3, -1), d=2, trama=0, rim=0.5, rampa="piedra")
        for q in range(4):
            for sg in (-1, 1):
                h.trazo(np.array([[1100, 150 + dy + 10], [1100 + sg * (20 + 4 * q), 150 + dy + 4 + 8 * q - 12], [1100 + sg * (30 + 4 * q), 150 + dy + 14 + 6 * q]]), 1.4, 10502 + q * 3 + sg,
                        color=tuple(h.c(30, "piedra")), jit=0.1, taper=(0, 0))
        h.luz_cono(960, -200, math.pi / 2, 0.45, 1500, h.pal["lampara"], k=1.4, suave=0.6)
        C.ambiente(h, 0.42)
        C.banda(h, "NO HUBO ALARMAS DE INCENDIO", 960, 1030, 46, t, self.t_alar, sem=116)
        N.motas(h, t, n=70, k=0.9)
        return h.acabado(t, niebla=dict(dens=0.06, sem=316), bloom=0.6)

    # ------------------------------------------------------------------ G. la bahía en calma
    def p_faro(self, h, t, u):
        tb = self.tb
        dur = tb[7] - tb[6]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.1 * k, 1150 - 120 * k, 380, 0.0)
        h.rim_color(h.pal["luna"])
        NC.pegar(M.faro_bahia(), h, 1.0, rampa="piedra", oscuro=0.8, emis=1.0, col_emis=h.pal["lampara"])
        a = math.pi - 0.25 + 0.5 * math.sin(t * 0.9)
        h.luz_cono(1705, 118, a, 0.2, 2200, h.pal["luna"], k=1.6, suave=0.5)
        h.luz_radial(1705, 118, 360, h.pal["lampara"], k=1.2)
        # reflejos que se mueven sobre el agua
        for q in range(8):
            xx = 200 + q * 180 + 24 * math.sin(t * 0.7 + q)
            h.emitir(C.rect(xx, 620 + 14 * (q % 3) + 40, 120, 3), 0.35, col=h.pal["luna"], blur=1)
        h.luz_radial(300, -40, 800, h.pal["luna"], k=0.5)
        C.ambiente(h, 0.5)
        C.banda(h, "NO HUBO SIRENAS EN LA BAHÍA", 960, 1030, 46, t, self.t_sir, sem=117)
        N.motas(h, t, n=30, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.1, sem=317), bloom=0.9)

    # ------------------------------------------------------------------ H. PRECEDENTE en tinta negra
    def p_sello(self, h, t, u):
        tb = self.tb
        dur = tb[8] - tb[7]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.1 * k, 960, 540, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("madera", 10600), h, 1.0, rampa="madera", oscuro=0.9)
        with h.capa(0.0):
            K.hoja(h, 900, 560, 780, 900, ang=-0.03, sem=10610, tono=214, renglones=8, s=1.0)
            N.sello(h, "PRECEDENTE", 900, 580, 120, t, self.t_sell, rot=-6, tono=np.array([0.02, 0.02, 0.025]), alfa=0.98)
            # el tintero y la pluma
            h.pieza(elipse_(1500, 760, 120, 60, n=30), 24, 10620, w=6, luz=(0.3, -1), d=10, trama=0.2, rim=0.9, rampa="piedra")
            h.pieza(elipse_(1500, 750, 86, 36, n=30), 4, 10621, w=0, luz=(0, -1), d=1, trama=0, linea=False)
            h.pieza(suave([(1430, 700), (1570, 700), (1580, 760), (1420, 760)], 4), 30, 10622, w=5, luz=(0.3, -1), d=8, trama=0.2, rim=0.9, rampa="piedra")
            K.pluma(h, 1360, 720, ang=-0.9, s=1.4, sem=10630)
        dx, dy = C.temblor(t, [(self.t_sell + 0.08, 14)])
        h.luz_cono(960, -300, math.pi / 2, 0.9, 1500, h.pal["lampara"], k=1.2, suave=0.6)
        C.ambiente(h, 0.5)
        C.banda(h, "SELLADO EN TINTA NEGRA", 960, 1030, 50, t, self.t_sell, sem=118)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.04, sem=318), bloom=0.5)

    # ------------------------------------------------------------------ I. la caja de herramientas
    def _llave_inglesa(self, h, x, y, s, ang, sem):
        T = C.T_obj(x, y, ang, s)
        h.pieza(T(suave([(-190, -18), (110, -18), (110, 18), (-190, 18)], 3)), 150, sem, w=5 * s, luz=(0.3, -1), d=6 * s, trama=0.2, rim=0.9, rampa="piedra")
        h.pieza(T(elipse_(150, 0, 56, 56, n=24)), 140, sem + 1, w=5 * s, luz=(0.3, -1), d=8 * s, trama=0.2, rim=0.9, rampa="piedra")
        h.pieza(T([(160, -18), (260, -18), (260, 18), (160, 18)]), 14, sem + 2, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False)

    def p_herramientas(self, h, t, u):
        tb = self.tb
        dur = self.t1 - tb[8]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.1 * k, 960, 540, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("madera", 10700), h, 1.0, rampa="madera", oscuro=1.0)
        # la caja de herramientas abierta, vista desde arriba
        h.pieza(P.rrect(260, 160, 1400, 760, 40), 90, 10710, w=8, luz=(0.3, -1), d=18, trama=0.4, rim=0.8, rampa="vino")
        h.pieza(P.rrect(310, 210, 1300, 660, 28), 40, 10711, w=5, luz=(0.3, -1), d=6, trama=0.3, rim=0.4, rampa="piedra")
        h.pieza(C.rect(960, 210, 16, 660), 70, 10712, w=3, luz=(0.3, -1), d=3, trama=0.2, rim=0.7, rampa="piedra")
        # herramientas
        ap = lambda i: e_out(clamp01((t - tb[8] - 0.2 - 0.3 * i) / 0.5))
        if ap(0) > 0:
            self._llave_inglesa(h, 640, 330 - 200 * (1 - ap(0)), 1.4, -0.1, 10720)
        if ap(1) > 0:
            T = C.T_obj(640, 520 - 200 * (1 - ap(1)), 0.05, 1.4)
            h.pieza(T(suave([(-210, -14), (60, -14), (60, 14), (-210, 14)], 3)), 80, 10730, w=5, luz=(0.3, -1), d=5, trama=0.2, rim=0.8, rampa="vino")
            h.pieza(T([(60, -6), (210, -6), (210, 6), (60, 6)]), 170, 10731, w=3, luz=(0.3, -1), d=3, trama=0.1, rim=0.9, rampa="piedra")
        if ap(2) > 0:
            P.mazo(h, 600, 700 - 200 * (1 - ap(2)), 1.2, ang=-0.2, sem=10740)
        # la figurita humana con su etiqueta de precio
        f = ap(3)
        if f > 0:
            fy = 540 - 240 * (1 - f)
            K.persona(h, 1280, fy + 190, 0.9, sem=10750, tono=150, bal=2 * math.sin(t * 2), rim=0.9)
            h.pieza(P.rrect(1330, fy - 80, 180, 110, 18), 226, 10760, w=4, luz=(0.2, -1), d=4, trama=0, rim=0, rampa="papel")
            h.trazo(np.array([[1330, fy - 40], [1290, fy + 20]]), 2.5, 10761, jit=0.1, taper=(0, 0))
            N.texto_maquina(h, "$2", 1420, fy - 28, 82, t, -99, cps=1e9, tono=0.05, centro=True, fuente=C.IMPACT, encuadrar=False)
        h.luz_cono(960, -300, math.pi / 2, 0.9, 1500, h.pal["lampara"], k=1.3, suave=0.6)
        C.ambiente(h, 0.5)
        C.banda(h, "LA HERRAMIENTA MÁS BARATA DE LA RED", 960, 1030, 46, t, self.t_herr, sem=119, acento=True)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.04, sem=319), bloom=0.6)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        tb = self.tb
        self.ev(tb[0] + 0.3, "tecleo_rapido", 0.3, 0.0, dur=2.5)
        self.ev(self.t_res + 0.3, "tecla", 0.5, 0.0)
        self.ev(self.t_res + 0.7, "tecla", 0.5, 0.0)
        self.ev(self.t_res + 1.1, "tecla", 0.5, 0.0)
        self.ev(self.t_abr - 0.2, "puerta", 0.6, 0.0)
        self.ev(self.t_del + 0.3, "servo", 0.35, 0.0)
        self.ev(self.t_emp, "hilo_tenso", 0.35, 0.0)
        self.ev(self.t_alar, "silencio_tono", 0.2, 0.0, dur=3.0)
        self.ev(self.t_sir, "lluvia_lejana", 0.25, 0.0, dur=3.0)
        self.ev(self.t_sell + 0.05, "sello_golpe", 0.8, 0.0)
        self.ev(self.t_herr, "caja_registradora", 0.4, 0.0)
        self.ev(self.t1 - 0.7, "tinta_mancha", 0.4, 0.0, dur=0.8)
