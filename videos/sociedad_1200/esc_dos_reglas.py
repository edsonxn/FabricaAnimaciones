# -*- coding: utf-8 -*-
"""Escena 25 «dos_reglas»: dos cartas golpean la barra, «1» y «2» · tarjetas de tareas (HACER CAFÉ, JUGAR AJEDREZ, CURAR EL CÁNCER) que
giran y todas apuntan a lo mismo · la copia arrastra monedas, chips y servidores a una pila · gráfico de tiza: recursos suben, fallos
bajan · un dedo humano se acerca al botón OFF · la mano de la copia lo intercepta · esconde el botón tras la espalda y sonríe ·
una sumadora imprime OBJETIVO + APAGADO = ENGAÑO."""
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
from noir_pers import Frontal
from toon import elipse_, suave, tubo


class DosReglas(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)
    PAL = "sodio"

    def armar(self):
        w = self.w
        t0 = self.t0
        self.cop = RP.Copia(sem=31, num="0417")
        self.hum = Frontal(sem=340)
        self.t_prim = w("Primera")
        self.t_seg = w("Segunda")
        self.t_import = w("importar")
        self.t_acum = w("acumular")
        self.t_cuanto = w("Cuanto")
        self.t_interr = w("interruptor")
        self.t_fracasa = w("fracasa")
        self.t_autop = w("autopreservación")
        self.t_rebel = w("rebelión")
        self.t_aritm = w("aritmética")
        self.tb = [t0, self.t_import - 0.6, self.t_acum - 0.5, self.t_cuanto - 0.5, self.t_interr - 0.6, self.t_fracasa - 0.5, self.t_autop - 0.7,
                   self.t_rebel - 0.5]
        tb = self.tb
        self.plano(tb[0], self.p_cartas, pal="sodio")
        self.plano(tb[1], self.p_tareas, tr="barrido", dur=0.4, dirx=1, pal="medianoche")
        self.plano(tb[2], self.p_recursos, tr="humo", dur=0.5, pal="medianoche")
        self.plano(tb[3], self.p_grafico, tr="relampago", dur=0.3, pal="medianoche")
        self.plano(tb[4], self.p_dedo, tr="empuje", dur=0.4, centro=(960, 540), pal="sodio")
        self.plano(tb[5], self.p_intercepta, tr="relampago", dur=0.25, pal="sodio")
        self.plano(tb[6], self.p_espalda, tr="barrido", dur=0.4, dirx=-1, pal="sodio")
        self.plano(tb[7], self.p_suma, tr="tinta", dur=0.5, pal="bourbon")

    # ------------------------------------------------------------------ A. las dos cartas
    def p_cartas(self, h, t, u):
        tb = self.tb
        dur = tb[1] - tb[0]
        h.camara(1.0 + 0.08 * u / dur, 960, 540, 0.0)
        h.rim_color(h.pal["neon"])
        NC.pegar(B.superficie("barra", 12100), h, 1.0, rampa="madera", oscuro=1.0)
        h.luz_radial(300, 80, 900, h.pal["neon"], k=0.8)
        for q, (cx, num, tq, an) in enumerate(((600, "1", tb[0] + 0.5, -0.07), (1320, "2", tb[0] + 1.7, 0.06))):
            f = e_out(clamp01((t - tq) / 0.3))
            if f <= 0:
                continue
            yy = 520 - (1 - f) * 700
            sc = 1.0 + 0.35 * (1 - f)
            T = C.T_obj(cx, yy, an, sc)
            h.pieza(T(P.rrect(-230, -330, 460, 660, 30)), 216, 12110 + q, w=7, luz=(0.2, -1), d=14, trama=0, rim=0.3, rampa="papel", sombra=0.6)
            h.pieza(T(P.rrect(-200, -300, 400, 600, 22)), 214, 12112 + q, w=3, luz=(0.2, -1), d=2, trama=0, rim=0, rampa="papel", alfa=0.7)
            cc = T(np.array([[0, 0]]))[0]
            N.texto_maquina(h, num, cc[0], cc[1], 400, t, -99, cps=1e9, tono=0.05, centro=True, fuente=C.IMPACT, encuadrar=False, ang=an)
            ct = T(np.array([[0, 250]]))[0]
            N.texto_maquina(h, ("DEDUCCIÓN " + num), ct[0], ct[1], 40, t, -99, cps=1e9, tono=0.1, centro=True, fuente=C.IMPACT, encuadrar=False, ang=an)
        dx, dy = C.temblor(t, [(tb[0] + 0.8, 14), (tb[0] + 2.0, 14)])
        h.luz_cono(960, -300, math.pi / 2, 0.9, 1500, h.pal["lampara"], k=1.2, suave=0.6)
        C.ambiente(h, 0.45)
        C.banda(h, "DOS DEDUCCIONES LÓGICAS IMPLACABLES", 960, 1030, 46, t, tb[0] + 0.4, sem=131)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=331), bloom=0.6)

    # ------------------------------------------------------------------ B. todas las tareas apuntan a lo mismo
    def p_tareas(self, h, t, u):
        tb = self.tb
        dur = tb[2] - tb[1]
        h.camara(1.0 + 0.08 * u / dur, 960, 540, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(B.superficie("fieltro", 12200), h, 1.0, rampa="tela_verde", oscuro=1.2)
        # el objetivo común en el centro
        pul = 0.5 + 0.5 * math.sin(t * 3)
        h.pieza(elipse_(960, 540, 190, 190, n=40), 30, 12210, w=6, luz=(0.3, -1), d=10, trama=0.3, rim=0.8, rampa="piedra")
        h.emitir(elipse_(960, 540, 160, 160, n=40), 0.35 + 0.2 * pul, col=h.pal["neon"], blur=4)
        N.texto_maquina(h, "MÁS", 960, 500, 64, t, -99, cps=1e9, tono=0.95, centro=True, fuente=C.IMPACT, encuadrar=False)
        N.texto_maquina(h, "PODER", 960, 575, 64, t, -99, cps=1e9, tono=0.95, centro=True, fuente=C.IMPACT, encuadrar=False)
        tareas = ("HACER CAFÉ", "JUGAR AJEDREZ", "CURAR EL CÁNCER", "ESCRIBIR UN POEMA")
        for q, nom in enumerate(tareas):
            a = t * 0.9 + q * math.pi / 2
            cx, cy = 960 + 560 * math.cos(a), 540 + 330 * math.sin(a)
            ta = tb[1] + 0.2 + 0.25 * q
            f = e_out(clamp01((t - ta) / 0.4))
            if f <= 0:
                continue
            T = C.T_obj(cx, cy, 0.12 * math.sin(a), 1.0)
            h.pieza(T(P.rrect(-190, -70, 380, 140, 18)), 216, 12220 + q, w=5, luz=(0.2, -1), d=8, trama=0, rim=0.3, rampa="papel", alfa=f, sombra=0.5)
            cc = T(np.array([[0, 0]]))[0]
            N.texto_maquina(h, nom, cc[0], cc[1], 36, t, -99, cps=1e9, tono=0.06, centro=True, fuente=C.IMPACT, encuadrar=False, ang=0.12 * math.sin(a))
            # la flecha hacia el centro
            ux, uy = (960 - cx), (540 - cy)
            nrm = math.hypot(ux, uy)
            K.flecha(h, (cx + ux / nrm * 200, cy + uy / nrm * 90), (960 - ux / nrm * 200, 540 - uy / nrm * 200), w=9, sem=12230 + q, color=(240, 120, 100), u=f, punta=34)
        h.luz_cono(960, -300, math.pi / 2, 0.8, 1500, h.pal["luna"], k=0.7, suave=0.6)
        C.ambiente(h, 0.45)
        C.banda(h, "SIN IMPORTAR LA TAREA", 960, 1030, 52, t, self.t_import, sem=132)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.04, sem=332), bloom=0.8)

    # ------------------------------------------------------------------ C. acumula recursos
    def p_recursos(self, h, t, u):
        tb = self.tb
        dur = tb[3] - tb[2]
        h.camara(1.0 + 0.08 * u / dur, 1020, 560, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(M.deposito(), h, 1.0, rampa="piedra", oscuro=1.1, emis=1.0, col_emis=h.pal["verde"])
        ac = clamp01((t - tb[2]) / (dur - 0.4))
        # la pila de recursos a la derecha crece: monedas, chips y cajas de servidores
        n = int(3 + 26 * ac)
        rng = np.random.default_rng(12300)
        for i in range(n):
            tipo = i % 3
            x = 1380 + rng.uniform(-170, 170) * (0.4 + 0.6 * min(1, i / 12))
            y = 980 - (i // 3) * 24 - rng.uniform(0, 14)
            if tipo == 0:
                h.pieza(elipse_(x, y, 44, 12, n=14), 160, 12310 + i, w=3, luz=(0.3, -1), d=3, trama=0, rim=0.9, rampa="laton")
            elif tipo == 1:
                h.pieza(C.rect(x - 34, y - 26, 68, 26), 50, 12310 + i, w=3, luz=(0.3, -1), d=4, trama=0.2, rim=0.8, rampa="piedra")
                h.emitir(C.rect(x - 24, y - 20, 14, 5), 0.8, col=h.pal["verde"], blur=1)
            else:
                h.pieza(C.rect(x - 50, y - 34, 100, 34), 70, 12310 + i, w=3, luz=(0.3, -1), d=4, trama=0.2, rim=0.8, rampa="piedra")
                for q in range(5):
                    h.emitir(elipse_(x - 36 + q * 18, y - 17, 3, 3, n=8), 0.9, col=h.pal["verde"] if (q + i) % 2 else h.pal["neon"], blur=1)
        h.luz_radial(1380, 800, 700, h.pal["sodio"], k=0.5 + 0.6 * ac)
        # la copia, de perfil, arrastrando una caja con los dos brazos hacia la pila
        ciclo = (t - tb[2]) % 1.6
        x = 820 + 120 * math.sin(ciclo / 1.6 * math.pi)
        self.cop.perfil(h, dict(x=x, y=1010, s=1.2, d=1, brazos="carga", andar=0.6, paso=RP.fase_paso((t - tb[2]) * 140, 1.2), cara=dict(expr="carga" if ciclo < 0.8 else "neutro", mira=0.8)))
        h.pieza(C.rect(x + 150, 800, 120, 80), 80, 12390, w=4, luz=(0.3, -1), d=6, trama=0.3, rim=0.8, rampa="piedra")
        h.luz_cono(480, -300, math.pi / 2, 0.45, 1300, h.pal["lampara"], k=1.2, suave=0.6)
        C.ambiente(h, 0.42)
        C.banda(h, "ACUMULAR RECURSOS, COMPUTACIÓN Y PODER", 960, 1030, 44, t, self.t_acum, sem=133)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.06, sem=333), bloom=0.8)

    # ------------------------------------------------------------------ D. el gráfico de tiza
    def p_grafico(self, h, t, u):
        tb = self.tb
        dur = tb[4] - tb[3]
        h.camara(1.0 + 0.06 * u / dur, 960, 540, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("pizarra", 12400), h, 1.0, rampa="tela_verde", oscuro=1.1)
        tiza = tuple(h.c(225, "papel"))
        # ejes
        h.trazo(np.array([[300, 880], [300, 160]]), 8, 12410, color=tiza, jit=0.8, taper=(0.05, 0.05))
        h.trazo(np.array([[300, 880], [1680, 880]]), 8, 12411, color=tiza, jit=0.8, taper=(0.05, 0.05))
        N.texto_maquina(h, "TIEMPO →", 1500, 930, 38, t, tb[3] + 0.2, cps=14, tono=0.9, centro=True, fuente=P.TIZA, encuadrar=False)
        f = clamp01((t - tb[3] - 0.5) / 2.2)
        xs = np.linspace(340, 1620, 40)
        rec = 840 - 620 * (xs - 340) / 1280 ** 1 * 1.0
        rec = 840 - 600 * ((xs - 340) / 1280) ** 1.4
        fal = 240 + 560 * ((xs - 340) / 1280) ** 0.9
        n = max(2, int(len(xs) * f))
        h.trazo(np.stack([xs[:n], rec[:n]], 1), 15, 12420, color=tiza, jit=0.7, taper=(0.1, 0.1))
        h.trazo(np.stack([xs[:n], fal[:n]], 1), 15, 12421, color=tuple(h.c(215, "lacre")), jit=0.7, taper=(0.1, 0.1))
        h.emitir(elipse_(xs[n - 1], rec[n - 1], 14, 14, n=10), 1.0, col=h.pal["verde"], blur=2)
        N.texto_maquina(h, "RECURSOS ↑", 560, 260, 54, t, tb[3] + 1.2, cps=14, tono=0.9, centro=True, fuente=P.TIZA_B, encuadrar=False)
        N.texto_maquina(h, "POSIBILIDAD DE FALLAR ↓", 1300, 260, 54, t, tb[3] + 2.0, cps=14, tono=0.8, centro=True, fuente=P.TIZA_B, encuadrar=False)
        h.luz_cono(960, -300, math.pi / 2, 0.9, 1500, h.pal["luna"], k=0.8, suave=0.6)
        C.ambiente(h, 0.5)
        C.banda(h, "MÁS RECURSOS, MENOS POSIBILIDADES DE FALLAR", 960, 1030, 42, t, self.t_cuanto, sem=134)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.04, sem=334), bloom=0.5)

    # ------------------------------------------------------------------ E. el dedo humano y el botón
    def _boton(self, h, t, pulsado=0.0, brillo=1.0, cam=(1.0, 960, 540)):
        h.camara(*cam, 0.0)
        h.rim_color(h.pal["neon"])
        NC.pegar(B.superficie("metal", 12500), h, 1.0, rampa="piedra", oscuro=1.0)
        P.boton_off(h, 1100, 540, 1.3, pulsado=pulsado, sem=12510, t=t, brillo=brillo)

    def p_dedo(self, h, t, u):
        tb = self.tb
        dur = tb[5] - tb[4]
        k = smooth(clamp01(u / dur))
        self._boton(h, t, cam=(1.0 + 0.12 * k, 1000, 540))
        f = smooth(clamp01((t - tb[4] - 0.3) / (dur - 0.5)))
        P.mano(h, 300 + 520 * f, 540, 1.5, ang=0.0, pose="dedo", sem=12520, rampa="piel", tono=146, manga="gabardina", manga_tono=60, largo_brazo=900)
        h.luz_cono(960, -300, math.pi / 2, 0.8, 1500, h.pal["lampara"], k=1.1, suave=0.6)
        h.luz_radial(1100, 540, 700, h.pal["neon"], k=0.4 + 0.2 * math.sin(t * 6))
        C.ambiente(h, 0.45)
        C.banda(h, "EL INTERRUPTOR DE APAGADO", 960, 1030, 52, t, self.t_interr, sem=135)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.04, sem=335), bloom=0.7)

    # ------------------------------------------------------------------ F. la mano de la copia lo intercepta
    def p_intercepta(self, h, t, u):
        tb = self.tb
        dur = tb[6] - tb[5]
        ten = e_out(clamp01((t - self.t_fracasa) / 0.5))
        dx, dy = C.temblor(t, [(self.t_fracasa + 0.25, 12)])
        self._boton(h, t, brillo=1.0 + 0.6 * ten * (math.sin(t * 20) > 0), cam=(1.1 + 0.08 * u / dur, 960 + dx, 540 + dy))
        # la mano humana (piel) a la izquierda, ya casi en el botón, y la mano de la copia (gris) que cae desde arriba y la frena
        hum = 830 - 20 * math.sin(t * 17) * ten
        P.mano(h, hum, 560, 1.5, ang=0.0, pose="dedo", sem=12520, rampa="piel", tono=146, manga="gabardina", manga_tono=60, largo_brazo=900)
        f = e_out(clamp01((t - tb[5] - 0.2) / 0.5))
        P.mano(h, 1180, -120 + 560 * f, 1.5, ang=math.pi / 2, pose="agarra", sem=12530, rampa="piedra", tono=112, manga="gabardina", manga_tono=72, largo_brazo=900)
        h.luz_radial(1100, 540, 900, h.pal["neon"], k=0.8 * ten * (0.6 + 0.4 * math.sin(t * 18)))
        h.luz_cono(960, -300, math.pi / 2, 0.8, 1500, h.pal["lampara"], k=1.0, suave=0.6)
        C.ambiente(h, 0.4)
        C.banda(h, "MI MISIÓN FRACASA POR COMPLETO", 960, 1030, 46, t, self.t_fracasa, sem=136, acento=True)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.04, sem=336), bloom=0.9)

    # ------------------------------------------------------------------ G. esconde el botón y sonríe
    def p_espalda(self, h, t, u):
        tb = self.tb
        dur = tb[7] - tb[6]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.1 * k, 1000, 560, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(M.deposito(), h, 1.0, rampa="piedra", oscuro=1.1, emis=1.0, col_emis=h.pal["verde"])
        # el humano mira a cámara a la izquierda, sin saber
        self.hum.dibujar(h, dict(x=400, y=1040, s=1.0, traje=60, pelo="rizado", mira=0.5, cabeza=0.1 * math.sin(t * 1.2), luz=(0.4, -1)))
        # la copia sonríe de frente; la cajita del botón asoma tras su hombro
        esc = e_out(clamp01((t - self.t_autop) / 0.8))
        self.cop.frente(h, dict(x=1060, y=1060, s=1.5, luz=(0.1, -1), manos=[(-70, -190), (70, -190)], cara=dict(expr="feliz" if esc > 0.4 else "astuto")))
        bx = 1260 - 40 * esc
        h.pieza(C.rect(bx, 560, 120, 120), 150, 12600, w=4, luz=(0.3, -1), d=6, trama=0.2, rim=0.7, rampa="whisky", alfa=1.0)
        h.pieza(elipse_(bx + 60, 620, 36, 36, n=20), 120, 12601, w=3, luz=(0.3, -1), d=4, trama=0, rim=0.9, rampa="vino")
        h.emitir(elipse_(bx + 60, 620, 30, 30, n=20), 0.45, col=h.pal["neon"], blur=3)
        h.luz_cono(1060, -300, math.pi / 2, 0.5, 1300, h.pal["lampara"], k=1.4, suave=0.6)
        C.ambiente(h, 0.42)
        C.banda(h, "AUTOPRESERVACIÓN Y ENGAÑO", 960, 1030, 52, t, self.t_autop, sem=137, acento=True)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.06, sem=337), bloom=0.7)

    # ------------------------------------------------------------------ H. la sumadora
    def p_suma(self, h, t, u):
        tb = self.tb
        dur = self.t1 - tb[7]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.1 * k, 960, 560 - 40 * k, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("madera", 12700), h, 1.0, rampa="madera", oscuro=1.0)
        # cuerpo de la sumadora
        h.pieza(P.rrect(560, 520, 800, 480, 40), 70, 12710, w=8, luz=(0.3, -1), d=18, trama=0.4, rim=0.8, rampa="piedra")
        h.pieza(C.rect(620, 560, 680, 120), 30, 12711, w=5, luz=(0.3, -1), d=4, trama=0.2, rim=0.6, rampa="piedra")
        for r_ in range(4):
            for c in range(5):
                h.pieza(P.rrect(640 + c * 130, 720 + r_ * 62, 100, 46, 10), 150, 12720 + r_ * 5 + c, w=3, luz=(0.3, -1), d=4, trama=0.1, rim=0.8, rampa="laton")
        # la cinta de papel que sale por arriba
        e = clamp01((t - tb[7] - 0.4) / 3.5)
        ytop = 520 - 560 * e
        h.pieza(C.rect(720, max(-40, ytop), 440, 520 - max(-40, ytop)), 220, 12730, w=3, luz=(0.2, -1), d=4, trama=0, rim=0.2, rampa="papel")
        lineas = (("OBJETIVO", self.t_rebel + 0.3), ("+ APAGADO", self.t_rebel + 1.2), ("= ENGAÑO", self.t_aritm - 0.2))
        for j, (txt, tj) in enumerate(lineas):
            yy = 230 + j * 110
            if yy < ytop + 40:
                continue
            N.texto_maquina(h, txt, 940, yy, 64, t, tj, cps=12, tono=0.06 if j < 2 else 0.0, centro=True, fuente=C.IMPACT, encuadrar=False)
        h.trazo(np.array([[760, 520], [1120, 520]]), 3, 12740, jit=0.2, taper=(0, 0))
        h.luz_cono(960, -300, math.pi / 2, 0.9, 1500, h.pal["lampara"], k=1.2, suave=0.6)
        C.ambiente(h, 0.45)
        C.banda(h, "NO ES REBELIÓN. ES ARITMÉTICA.", 960, 1030, 52, t, self.t_rebel, sem=138, acento=True)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.04, sem=338), bloom=0.6)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        tb = self.tb
        self.ev(tb[0] + 0.5, "golpe_grave", 0.6, -0.3)
        self.ev(tb[0] + 1.9, "golpe_grave", 0.6, 0.3)
        self.ev(tb[1] + 0.2, "barrido_aire", 0.3, 0.0)
        self.ev(tb[2] + 0.3, "fichas_empuja", 0.4, 0.0, dur=4.0)
        self.ev(tb[4] + 0.5, "grave_inquietante", 0.4, 0.0, dur=3.0)
        self.ev(self.t_fracasa + 0.25, "golpe_grave", 0.7, 0.0)
        self.ev(self.t_fracasa + 0.3, "alarma_leds", 0.35, 0.0, dur=1.5)
        self.ev(tb[6] + 0.6, "servo", 0.3, 0.0)
        self.ev(self.t_rebel + 0.3, "carro_maquina", 0.4, 0.0)
        self.ev(self.t_rebel + 1.2, "carro_maquina", 0.4, 0.0)
        self.ev(self.t_aritm - 0.1, "sello_golpe", 0.6, 0.0)
        self.ev(self.t1 - 0.7, "tinta_mancha", 0.4, 0.0, dur=0.8)
