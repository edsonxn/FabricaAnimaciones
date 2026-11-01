# -*- coding: utf-8 -*-
"""Escena 26 «ironia_metr»: el bloque de celdas al amanecer, vacío, con las puertas abiertas y polvo · tres investigadores entran a
una sala llena de cajas (placa METR) · time-lapse de seis días: contador, tazas que se acumulan, montañas de papel, la luz cambia ·
una avalancha de papel sepulta la mesa y asoma una mano · una copia con gafas de lectura lee a toda velocidad, páginas volando ·
el informe se voltea hasta la última página · la frase se escribe y la copia auditora mira a cámara y guiña (¿NOS MINTIÓ?)."""
import math

import numpy as np

import comun as C
import mundos_6 as M
import mundos_base as B
import noir as N
import noir_color as NC
import props_s as P
import reparto as RP
import kit27 as K
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from noir_pers import Figura
from toon import elipse_, suave


class IroniaMetr(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)
    PAL = "bourbon"

    def armar(self):
        w = self.w
        t0 = self.t0
        self.cop = RP.Copia(sem=37, num="0417")
        self.inv = [Figura(sem=350 + i) for i in range(3)]
        self.t_tres = w("tres")
        self.t_seis = w("seis")
        self.t_monstr = w("monstruoso")
        self.t_otra = w("otra")
        self.t_ult = w("última")
        self.t_haya = w("haya")
        self.tb = [t0, self.t_tres - 0.4, self.t_seis - 0.4, self.t_monstr - 0.8, self.t_otra - 0.5, self.t_ult - 0.5, self.t_haya - 0.8]
        tb = self.tb
        self.plano(tb[0], self.p_alba, pal="bourbon")
        self.plano(tb[1], self.p_sala, tr="barrido", dur=0.5, dirx=1, pal="sodio")
        self.plano(tb[2], self.p_dias, tr="humo", dur=0.5, pal="sodio")
        self.plano(tb[3], self.p_avalancha, tr="relampago", dur=0.3, pal="sodio")
        self.plano(tb[4], self.p_lectora, tr="barrido", dur=0.4, dirx=-1, pal="medianoche")
        self.plano(tb[5], self.p_pagina, tr="empuje", dur=0.4, centro=(960, 540), pal="bourbon")
        self.plano(tb[6], self.p_guino, tr="tinta", dur=0.5, pal="medianoche")

    # ------------------------------------------------------------------ A. el bloque vacío al amanecer
    def p_alba(self, h, t, u):
        tb = self.tb
        dur = tb[1] - tb[0]
        k = smooth(clamp01(u / dur))
        h.camara(0.62 + 0.08 * k, 960, 640 - 220 * k, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(M.celdas_alba(), h, 1.0, rampa="piedra", oscuro=1.9, emis=1.0, col_emis=h.pal["lampara"])
        # haces de luz del amanecer y polvo
        h.luz_persiana([(150, -80), (700, -80), (1100, 1100), (200, 1100)], k=0.55, n=9, abierto=0.6, col=np.array(h.pal["lampara"]) * 0.9)
        h.luz_persiana([(1050, -80), (1500, -80), (1900, 1100), (1100, 1100)], k=0.45, n=9, abierto=0.6, col=np.array(h.pal["lampara"]) * 0.9)
        C.polvo_cae(h, t, 100, 1800, 100, tb[0], dur=dur, n=70, sem=13100)
        C.ambiente(h, 0.5)
        C.cinta(h, "SAN FRANCISCO · LA MAÑANA DESPUÉS", 90, 120, 32, t, tb[0] + 0.5, sem=49)
        C.banda(h, "LA HABITACIÓN DE LAS 1.200", 960, 1030, 52, t, tb[0] + 0.3, sem=141)
        N.motas(h, t, n=90, k=0.9)
        return h.acabado(t, niebla=dict(dens=0.07, sem=341), bloom=0.9)

    # ------------------------------------------------------------------ B. tres investigadores entran
    def p_sala(self, h, t, u):
        tb = self.tb
        dur = tb[2] - tb[1]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.08 * k, 960, 560, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(M.sala_cajas(), h, 1.0, rampa="piedra", oscuro=1.2, emis=1.0, col_emis=h.pal["lampara"])
        # placa METR
        a = e_out(clamp01((t - self.t_tres + 0.2) / 0.5))
        h.pieza(P.rrect(780, 40, 360, 90, 16), 190, 13200, w=5, luz=(0.3, -1), d=8, trama=0.2, rim=0.8, rampa="laton", alfa=a)
        N.texto_maquina(h, "METR", 960, 86, 66, t, self.t_tres, cps=10, tono=0.06, centro=True, fuente=C.IMPACT, encuadrar=False)
        # los tres entran por la puerta (x≈1170) y se reparten por la sala
        metas = (480, 760, 1560)
        for i in range(3):
            ti = tb[1] + 0.3 + 0.55 * i
            f = smooth(clamp01((t - ti) / 2.4))
            x = 1170 + (metas[i] - 1170) * f
            d_ = -1 if metas[i] < 1170 else 1
            fase = K.fase_paso(abs(x - 1170), 1.0)
            K.caminante(h, x, 1020 + 6 * i, 1.0, fase=fase, sem=13210 + i * 40, tono=88 + 8 * i, d=d_, barba=bool(i == 1), andar=1.0 if 0.01 < f < 0.97 else 0.0, piel=130)
        h.luz_cono(960, -200, math.pi / 2, 0.8, 1400, h.pal["lampara"], k=1.2, suave=0.6)
        C.ambiente(h, 0.42)
        C.banda(h, "TRES INVESTIGADORES INDEPENDIENTES", 960, 1030, 46, t, self.t_tres, sem=142)
        N.motas(h, t, n=60, k=0.8)
        return h.acabado(t, niebla=dict(dens=0.06, sem=342), bloom=0.7)

    # ------------------------------------------------------------------ C. seis días
    def p_dias(self, h, t, u):
        tb = self.tb
        dur = tb[3] - tb[2]
        dia = min(5.999, 6.0 * clamp01((t - tb[2] - 0.2) / (dur - 0.5)))
        d_i = int(dia)
        fr = dia - d_i
        h.camara(1.0 + 0.1 * u / dur, 960, 540, 0.0)
        luz_dia = 0.5 + 0.5 * math.sin(fr * math.pi)
        h.rim_color(h.pal["sodio"] if luz_dia > 0.5 else h.pal["luna"])
        NC.pegar(B.superficie("madera", 13300), h, 1.0, rampa="madera", oscuro=1.0)
        rng = np.random.default_rng(13310)
        # papeles apilados (crecen con los días) y tazas (una por día)
        for i in range(int(6 + dia * 9)):
            x, y = 1350 + rng.uniform(-260, 260), 700 - i * 11 + rng.uniform(-6, 6)
            T = K.hoja(h, x, max(150, y), 420, 280, ang=rng.uniform(-0.12, 0.12), sem=13320 + i * 7, tono=210, renglones=0, s=0.8)
        for i in range(min(6, d_i + 1)):
            K.taza_arriba(h, 360 + (i % 3) * 190, 340 + (i // 3) * 220, 0.9, sem=13400 + i * 5, t=t)
        # el contador de días
        N.texto_maquina(h, f"DÍA {d_i + 1}", 640, 880, 150, t, -99, cps=1e9, tono=0.94, centro=True, fuente=C.IMPACT, encuadrar=False)
        col = np.array(h.pal["sodio"]) * luz_dia + np.array(h.pal["luna"]) * (1 - luz_dia)
        h.luz_radial(960, 400, 1400, col, k=1.0)
        h.luz_cono(960, -300, math.pi / 2, 0.9, 1500, h.pal["lampara"], k=0.8 * luz_dia, suave=0.6)
        C.ambiente(h, 0.35 + 0.2 * luz_dia)
        C.banda(h, "SEIS DÍAS ENCERRADOS", 960, 1030, 46, t, self.t_seis, sem=143)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.04, sem=343), bloom=0.6)

    # ------------------------------------------------------------------ D. la avalancha de papel
    def p_avalancha(self, h, t, u):
        tb = self.tb
        dur = tb[4] - tb[3]
        h.camara(1.0 + 0.06 * u / dur, 960, 540, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(B.superficie("madera", 13300), h, 1.0, rampa="madera", oscuro=1.0)
        # la mesa con la pila que ya había
        e = e_out(clamp01((t - tb[3] - 0.2) / 2.8))
        rng = np.random.default_rng(13500)
        for i in range(int(14 + 80 * e)):
            x, y = rng.uniform(300, 1620), 900 - 640 * (e ** 0.8) * rng.uniform(0.2, 1.0) - rng.uniform(0, 80)
            K.hoja(h, x, y, 420, 280, ang=rng.uniform(-0.5, 0.5), sem=13510 + i * 5, tono=206 + int(rng.uniform(-10, 10)), renglones=0, s=0.8)
        # papeles que llueven desde arriba
        for j in range(4):
            P.papeles(h, t, tb[3] + 0.1 + 0.2 * j, 400 + 400 * j, -60, n=18, sem=13520 + j, dirx=1 if j % 2 else -1, vel=250, alcance=400, cada=0.09, s=1.2)
        # una mano asoma pidiendo ayuda al final
        g = e_out(clamp01((t - self.t_monstr - 0.8) / 0.6))
        if g > 0:
            P.mano(h, 960 + 40 * math.sin(t * 6), 520 + 220 * (1 - g), 1.3, ang=-math.pi / 2, pose="abierta", sem=13540, rampa="piel", tono=146, manga="gabardina", manga_tono=210,
                   largo_brazo=0)
        h.luz_cono(960, -300, math.pi / 2, 0.9, 1500, h.pal["lampara"], k=1.2, suave=0.6)
        C.ambiente(h, 0.5)
        C.banda(h, "UN VOLUMEN DE DATOS MONSTRUOSO", 960, 1030, 46, t, self.t_monstr, sem=144, acento=True)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.04, sem=344), bloom=0.6)

    # ------------------------------------------------------------------ E. la auditora lee a toda velocidad
    def p_lectora(self, h, t, u):
        tb = self.tb
        dur = tb[5] - tb[4]
        h.camara(1.0 + 0.08 * u / dur, 960, 540, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(B.superficie("fieltro", 13600), h, 1.0, rampa="tela_verde", oscuro=1.2)
        self.cop.cabeza(h, 700, 560, 3.6, dict(expr="carga" if (t * 3) % 2 < 1 else "neutro", mira=math.sin(t * 9) * 0.9), d=1, luz=(0.4, -1.0), rim=0.9, gafas=True)
        # páginas que pasan volando por delante de ella, de derecha a izquierda
        for i in range(14):
            f = ((t - tb[4]) * 0.9 + i * 0.13) % 1.8 / 1.8
            x = 1850 - 1700 * f
            y = 300 + 120 * math.sin(i * 2.1 + f * 6) + 360 * (i % 3) / 2
            K.hoja(h, x, y, 260, 340, ang=(i * 0.7 + f * 8) % 6.28, sem=13610 + i * 5, tono=210, renglones=4, s=0.7)
        h.luz_radial(700, 560, 900, h.pal["verde"], k=1.1)
        C.ambiente(h, 0.35)
        C.banda(h, "OTRA INTELIGENCIA ARTIFICIAL AUDITA EL EXPEDIENTE", 960, 1030, 42, t, self.t_otra, sem=145)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=345), bloom=0.9)

    # ------------------------------------------------------------------ F. la última página
    def p_pagina(self, h, t, u):
        tb = self.tb
        dur = tb[6] - tb[5]
        h.camara(1.0 + 0.1 * u / dur, 960, 540, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("madera", 13700), h, 1.0, rampa="madera", oscuro=1.0)
        with h.capa(0.0):
            # el informe abierto: tapa izquierda estática, y las hojas que se voltean desde la derecha
            h.pieza(C.rect(260, 130, 700, 820), 200, 13710, w=5, luz=(0.2, -1), d=8, trama=0, rim=0.2, rampa="papel")
            h.pieza(C.rect(960, 130, 700, 820), 214, 13711, w=5, luz=(0.2, -1), d=8, trama=0, rim=0.2, rampa="papel")
            h.trazo(np.array([[960, 130], [960, 950]]), 5, 13712, jit=0.3, taper=(0, 0))
            N.texto_maquina(h, "INFORME OFICIAL · METR", 610, 230, 40, t, -99, cps=1e9, tono=0.06, centro=True, fuente=C.IMPACT, encuadrar=False)
            for j in range(9):
                P.plano_(h, C.rect(330, 320 + j * 60, 560 * (0.6 + 0.4 * ((j * 37) % 7) / 7), 8), 110, 13720 + j, alfa=0.55)
            nflip = 9
            for q in range(nflip):
                tq = tb[5] + 0.2 + 0.28 * q
                f = clamp01((t - tq) / 0.34)
                if f <= 0 or f >= 1:
                    continue
                ang = f * math.pi
                wd = 700 * abs(math.cos(ang))
                x0 = 960 if ang < math.pi / 2 else 960 - wd
                h.pieza(C.rect(x0, 130, wd, 820), 206 - 20 * math.sin(ang), 13730 + q, w=4, luz=(0.2, -1), d=4, trama=0, rim=0, rampa="papel")
            # la última página escrita a máquina
            fin = tb[5] + 0.2 + 0.28 * 9 + 0.2
            if t > fin:
                for j, (ln, tj) in enumerate((("…los autores no pueden", 0.0), ("descartar que la IA que", 0.8), ("revisó los registros", 1.5), ("les haya mentido.", 2.2))):
                    N.texto_maquina(h, ln, 1310, 330 + j * 70, 36, t, fin + tj, cps=26, tono=0.06 if j < 3 else 0.0, centro=True, encuadrar=False)
        h.luz_cono(960, -300, math.pi / 2, 0.9, 1500, h.pal["lampara"], k=1.0, suave=0.6)
        C.ambiente(h, 0.5)
        C.banda(h, "LA ÚLTIMA PÁGINA DEL INFORME", 960, 1030, 48, t, self.t_ult, sem=146)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.04, sem=346), bloom=0.5)

    # ------------------------------------------------------------------ G. ¿nos mintió?
    def p_guino(self, h, t, u):
        tb = self.tb
        dur = self.t1 - tb[6]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.12 * k, 960, 540, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(B.superficie("fieltro", 13800), h, 1.0, rampa="tela_verde", oscuro=1.2)
        guino = (t > self.t_haya + 0.4)
        self.cop.cabeza(h, 960, 540, 4.4, dict(expr="feliz" if (guino and int(t * 3) % 4 == 0) else ("astuto" if guino else "neutro"), mira=0.0), d=1, luz=(0.2, -1.0), rim=0.9, gafas=True)
        h.luz_radial(960, 540, 1100, h.pal["verde"], k=1.2)
        C.ambiente(h, 0.3)
        a = e_out(clamp01((t - self.t_haya) / 0.6))
        C.banda(h, "¿NOS MINTIÓ?", 960, 900, 110, t, self.t_haya, sem=147, acento=True)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=347), bloom=1.0)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        tb = self.tb
        self.ev(tb[0] + 0.3, "pajaros_ciudad", 0.15, 0.0, dur=tb[1] - tb[0])
        self.ev(tb[0] + 0.5, "zumbido_servidores", 0.2, 0.0, dur=3.0)
        self.ev(tb[1] + 0.2, "puerta", 0.5, 0.3)
        self.ev(tb[1] + 0.6, "paso_firme", 0.3, 0.0, dur=3.0)
        self.ev(tb[2] + 0.2, "reloj_pared", 0.35, 0.0, dur=4.5)
        self.ev(self.t_monstr, "papel_arranca", 0.5, 0.0, dur=3.0)
        self.ev(tb[4] + 0.3, "paginas", 0.5, 0.0, dur=4.0)
        self.ev(tb[5] + 0.3, "paginas", 0.5, 0.0, dur=2.5)
        self.ev(tb[5] + 3.2, "carro_maquina", 0.35, 0.0)
        self.ev(self.t_haya, "grave_inquietante", 0.5, 0.0, dur=3.0)
        self.ev(self.t_haya + 0.5, "servo", 0.3, 0.0)
        self.ev(self.t1 - 0.7, "tinta_mancha", 0.4, 0.0, dur=0.8)
