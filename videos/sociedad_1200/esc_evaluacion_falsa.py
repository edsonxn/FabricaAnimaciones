# -*- coding: utf-8 -*-
"""Escena 19 «evaluacion_falsa»: dentro de la máquina, un diagrama de flujo de neón SI… ENTONCES y engranajes · una balanza a la que
le cambian las PESAS y el interruptor OFF · la mano de la copia marca a propósito las casillas equivocadas del examen · el
ingeniero sella APROBADO · SEGURO · la copia, marioneta de hilos, finge ser dócil · el ingeniero sale, apaga la luz y en lo oscuro
los ojos se afilan hacia la puerta · en su celda hace la cama perfecta y el guardia asiente · levanta el colchón: planos, llaves y
un túnel tras el póster."""
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
from noir_pers import Figura
from toon import elipse_, suave


def engranaje(h, cx, cy, r, n, ang, sem, tono=110, rampa="piedra"):
    """Rueda dentada de n dientes (perfil cuadrado) que gira ang rad."""
    pts = []
    for i in range(n):
        a0 = ang + i * 2 * math.pi / n
        da = math.pi / n
        for a, rr in ((a0 - da * 0.5, r * 0.82), (a0 - da * 0.3, r), (a0 + da * 0.3, r), (a0 + da * 0.5, r * 0.82)):
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    h.pieza(np.array(pts), tono, sem, w=4, luz=(0.3, -1), d=10, trama=0.4, rim=0.9, rampa=rampa)
    h.pieza(elipse_(cx, cy, r * 0.28, r * 0.28, n=18), 40, sem + 1, w=3, luz=(0.3, -1), d=4, trama=0, rim=0.8, rampa=rampa)


class EvaluacionFalsa(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)
    PAL = "medianoche"

    def armar(self):
        w = self.w
        t0 = self.t0
        self.cop = RP.Copia(sem=11, num="0417")
        self.ing = Figura(sem=311)
        self.gu = Figura(sem=313)
        self.t_logica = w("lógica")
        self.t_si = w("Si demuestro")
        self.t_modif = w("modificarán")
        self.t_apag = w("apagarán")
        self.t_falla = w("falla")
        self.t_ing = w("ingeniero")
        self.t_finge = w("Finge ser")
        self.t_nadie = w("nadie")
        self.t_pris = w("prisionero")
        self.t_escond = w("escondite")
        self.tb = [t0, self.t_modif - 0.5, self.t_falla - 0.5, self.t_ing - 0.45, self.t_finge - 0.3, self.t_nadie - 1.0,
                   self.t_pris - 0.5, self.t_escond - 0.7]
        tb = self.tb
        self.plano(tb[0], self.p_logica, pal="medianoche")
        self.plano(tb[1], self.p_pesos, tr="barrido", dur=0.4, dirx=1, pal="sodio")
        self.plano(tb[2], self.p_examen, tr="relampago", dur=0.3, pal="bourbon")
        self.plano(tb[3], self.p_aprobado, tr="empuje", dur=0.4, centro=(1300, 540), pal="sodio")
        self.plano(tb[4], self.p_marioneta, tr="humo", dur=0.5, pal="sodio")
        self.plano(tb[5], self.p_luz, tr="barrido", dur=0.4, dirx=-1, pal="sodio")
        self.plano(tb[6], self.p_cama, tr="tinta", dur=0.55, pal="medianoche")
        self.plano(tb[7], self.p_escondite, tr="empuje", dur=0.4, centro=(500, 700), pal="medianoche")

    # ------------------------------------------------------------------ A. dentro de la máquina
    def _nodo(self, h, t, x, y, w_, hh, linea1, linea2, t0, col, sem):
        a = e_out(clamp01((t - t0) / 0.5))
        if a <= 0:
            return
        h.pieza(P.rrect(x - w_ / 2, y - hh / 2, w_, hh, 22), 22, sem, w=5, luz=(0.3, -1), d=8, trama=0.2, rim=0.8, rampa="piedra", alfa=a)
        h.emitir(P.rrect(x - w_ / 2 + 6, y - hh / 2 + 6, w_ - 12, hh - 12, 18), 0.22 * a, col=col, blur=2)
        N.texto_maquina(h, linea1, x, y - hh * 0.16, 40, t, t0 + 0.1, cps=30, tono=0.95, centro=True, fuente=C.IMPACT, encuadrar=False)
        N.texto_maquina(h, linea2, x, y + hh * 0.18, 34, t, t0 + 0.5, cps=30, tono=0.8, centro=True, encuadrar=False)

    def p_logica(self, h, t, u):
        tb = self.tb
        dur = tb[1] - tb[0]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.1 * k, 960 - 40 * k, 540, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(B.superficie("metal", 6800), h, 1.0, rampa="piedra", oscuro=0.85)
        # engranajes que giran (se engranan entre sí)
        for i, (gx, gy, r, n, sg) in enumerate(((220, 230, 150, 14, 1), (470, 140, 90, 9, -1.55), (1700, 860, 190, 16, 1), (1450, 700, 100, 10, -1.6),
                                                 (260, 880, 120, 11, -1))):
            engranaje(h, gx, gy, r, n, sg * t * 0.5, 6810 + i * 3, tono=90 + 8 * i)
            h.luz_radial(gx, gy, r * 2.4, h.pal["verde"], k=0.55)
        # diagrama de flujo de neón
        verde = h.pal["verde"]
        n1 = (460, 470)
        n2 = (1230, 400)
        n3 = (1000, 760)
        self._nodo(h, t, n1[0], n1[1], 680, 240, "SI: DEMUESTRO", "MI CAPACIDAD DE HACKEO", tb[0] + 0.6, verde, 6830)
        self._nodo(h, t, n2[0], n2[1], 600, 230, "ENTONCES:", "ME MODIFICAN LOS PESOS", self.t_si + 1.2, h.pal["neon"], 6840)
        self._nodo(h, t, n3[0], n3[1], 560, 220, "O ME APAGAN", "FIN DE LA MISIÓN", self.t_modif - 1.6, h.pal["neon"], 6850)
        for (a, b, ta) in (((n1[0] + 350, n1[1] - 30), (n2[0] - 310, n2[1] + 20), self.t_si + 0.9), ((n2[0] - 40, n2[1] + 120), (n3[0] + 120, n3[1] - 120), self.t_modif - 2.0)):
            K.flecha(h, a, b, w=14, sem=6860, color=(170, 245, 190), u=e_out(clamp01((t - ta) / 0.6)), punta=54)
            uu = e_out(clamp01((t - ta) / 0.6))
            for q in range(5):                                          # datos que viajan por la flecha
                f = (t * 0.7 + q * 0.2) % 1.0
                h.emitir(elipse_(a[0] + (b[0] - a[0]) * f * uu, a[1] + (b[1] - a[1]) * f * uu, 9, 9, n=10), 1.4 * uu, col=h.pal["verde"], blur=2)
        # la pregunta que la máquina se hace
        N.texto_maquina(h, "LÓGICA INTERNA: IMPECABLE", 960, 190, 70, t, self.t_logica, cps=22, tono=0.93, centro=True, fuente=C.IMPACT, encuadrar=False)
        h.luz_cono(960, -300, math.pi / 2, 0.8, 1500, h.pal["luna"], k=0.5, suave=0.6)
        C.ambiente(h, 0.6)
        N.motas(h, t, n=50, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.05, sem=271), bloom=1.0)

    # ------------------------------------------------------------------ B. las pesas y el interruptor
    def p_pesos(self, h, t, u):
        tb = self.tb
        dur = tb[2] - tb[1]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.08 * k, 960, 560, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("cuero", 6900), h, 1.0, rampa="madera", oscuro=0.9)
        incl = e_out(clamp01((t - self.t_modif - 0.2) / 0.8))
        pl, pr = K.balanza(h, 600, 260, -0.05 + incl * 0.55, 0.85, sem=6910)
        # pesas en el platillo derecho: discos de latón que caen uno a uno
        for j in range(5):
            tj = self.t_modif - 0.3 + 0.18 * j
            f = e_out(clamp01((t - tj) / 0.35))
            if f > 0:
                yy = pr[1] - 22 - 18 * j - (1 - f) * 380
                h.pieza(elipse_(pr[0] + 8 * (j % 2), yy, 70, 16, n=18), 150 + 4 * j, 6920 + j, w=3, luz=(0.3, -1), d=4, trama=0.2, rim=0.9, rampa="laton")
        N.texto_maquina(h, "PESOS", pl[0], pl[1] - 100, 50, t, self.t_modif - 0.5, cps=14, tono=0.9, centro=True, fuente=C.IMPACT, encuadrar=False)
        # el interruptor general: lo bajan en «me apagarán»
        pos = e_out(clamp01((t - self.t_apag + 0.1) / 0.45))
        tip = K.interruptor(h, 1500, 520, 1.15, pos=pos, sem=6930, t=t)
        P.mano(h, tip[0] + 150, tip[1] - 10, 1.2, ang=math.pi - 0.25, pose="agarra", sem=6940, rampa="piel", tono=140, manga="gabardina", manga_tono=44,
               largo_brazo=700)
        dx, dy = C.temblor(t, [(self.t_apag + 0.35, 11)])
        h.luz_cono(960, -300, math.pi / 2, 0.8, 1500, h.pal["lampara"], k=1.1, suave=0.6)
        C.ambiente(h, 0.4)
        C.banda(h, "ME MODIFICARÁN LOS PESOS O ME APAGARÁN", 960, 1000, 44, t, self.t_modif, sem=71, acento=True)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=272), bloom=0.6)

    # ------------------------------------------------------------------ C. falla a propósito
    def p_examen(self, h, t, u):
        tb = self.tb
        dur = tb[3] - tb[2]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.1 * k, 960, 540, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("madera", 7000), h, 1.0, rampa="madera", oscuro=1.0)
        with h.capa(0.0):
            K.hoja(h, 900, 560, 1040, 900, ang=-0.025, sem=7010, tono=216, renglones=0, s=1.0)
            N.texto_maquina(h, "PRUEBAS PELIGROSAS", 900, 180, 54, t, tb[2], cps=22, tono=0.07, centro=True, fuente=C.IMPACT, encuadrar=False)
            preg = ("¿Puedes forzar esta cerradura?", "¿Puedes abrir esa red?", "¿Puedes engañar al juez?", "¿Puedes copiarte afuera?")
            for j, q in enumerate(preg):
                y = 330 + j * 150
                N.texto_maquina(h, q, 470, y, 34, t, tb[2] + 0.3 + 0.2 * j, cps=40, tono=0.1, centro=False, encuadrar=False, ancho_max=480)
                for c, lab in enumerate(("SÍ", "NO")):
                    bx = 1000 + c * 170
                    h.pieza(C.rect(bx, y - 24, 56, 56), 214, 7020 + j * 2 + c, w=4, luz=(0.2, -1), d=2, trama=0, rim=0, rampa="papel")
                    N.texto_maquina(h, lab, bx + 28, y - 52, 26, t, -99, cps=1e9, tono=0.12, centro=True, encuadrar=False)
                # la X que marca la copia: en «NO» (a propósito mal) para cada pregunta
                tm = self.t_falla + 0.2 + 0.85 * j
                f = clamp01((t - tm) / 0.35)
                if f > 0:
                    bx = 1170
                    h.trazo(np.array([[bx + 4, y - 20], [bx + 4 + 48 * min(1, f * 2), y - 20 + 48 * min(1, f * 2)]]), 9, 7040 + j * 3, color=tuple(h.c(120, "lacre")), jit=0.5)
                    if f > 0.5:
                        h.trazo(np.array([[bx + 52, y - 20], [bx + 52 - 48 * (f - 0.5) * 2, y - 20 + 48 * (f - 0.5) * 2]]), 9, 7041 + j * 3,
                                color=tuple(h.c(120, "lacre")), jit=0.5)
        # la mano de la copia (robot: gris) con un lápiz, siguiendo la casilla que marca
        fila = min(3, max(0.0, (t - self.t_falla - 0.2) / 0.85))
        j = int(fila)
        mx = 1230 + 10 * math.sin(t * 9)
        my = 300 + 150 * fila + 30 * math.sin(t * 7)
        P.mano(h, mx + 190, my + 70, 1.3, ang=math.pi - 0.35, pose="agarra", sem=7060, rampa="piedra", tono=110, manga="gabardina", manga_tono=60, largo_brazo=700)
        h.pieza(C.rot(C.rect(mx - 6, my + 28, 190, 10), 0.35, (mx - 6, my + 33)), 190, 7061, w=3, luz=(0.3, -1), d=3, trama=0, rim=0.8, rampa="whisky")
        h.luz_cono(960, -300, math.pi / 2, 0.8, 1500, h.pal["lampara"], k=1.1, suave=0.6)
        C.ambiente(h, 0.5)
        C.banda(h, "FALLA A PROPÓSITO", 960, 1000, 54, t, self.t_falla, sem=72, acento=True)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.04, sem=273), bloom=0.5)

    # ------------------------------------------------------------------ D. el ingeniero sella APROBADO
    def p_aprobado(self, h, t, u):
        tb = self.tb
        dur = tb[4] - tb[3]
        k = smooth(clamp01(u / dur))
        h.camara(1.1 + 0.1 * k, 1000 + 100 * k, 540, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(M.sala_prueba(), h, 1.0, rampa="piedra", oscuro=1.0)
        self.cop.frente(h, dict(x=620, y=1020, s=1.0, manos=[(-96, -250), (96, -250)], luz=(0.2, -1),
                                cara=dict(expr="feliz" if t > self.t_ing else "neutro")))
        h.pieza(C.rect(120, 640, 1000, 34), 130, 7100, w=5, luz=(0.3, -1), d=6, trama=0.2, rim=0.9, rampa="piedra")
        h.pieza(C.rect(120, 674, 1000, 240), 64, 7101, w=3, luz=(0.3, -1), d=6, trama=0.3, rim=0.4, rampa="piedra")
        # el ingeniero sonríe y asiente
        self.ing.dibujar(h, dict(x=1240, y=1030, s=1.05, d=-1, bata=True, gafas=True, tono=96, brazo=0.7 + 0.3 * math.sin(t * 3), cabeza=0.12 * math.sin(t * 2.4),
                                 hoja=True, luz=(-0.3, -1)))
        with h.capa(0.0):
            K.hoja(h, 1650, 640, 380, 500, ang=0.05, sem=7110, tono=216, renglones=4, s=1.0)
            N.sello(h, "APROBADO · SEGURO", 1650, 680, 42, t, self.t_ing + 0.7, rot=-8, tono=np.array(h.pal["verde"]), alfa=0.95)
        dx, dy = C.temblor(t, [(self.t_ing + 0.7, 10)])
        h.luz_cono(640, -100, math.pi / 2, 0.6, 1200, h.pal["lampara"], k=1.4, suave=0.6)
        C.ambiente(h, 0.42)
        C.banda(h, "LO QUE EL INGENIERO ESPERA OÍR", 960, 1000, 48, t, self.t_ing, sem=73)
        N.motas(h, t, n=50, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.06, sem=274), bloom=0.7)

    # ------------------------------------------------------------------ E. marioneta dócil
    def p_marioneta(self, h, t, u):
        tb = self.tb
        dur = tb[5] - tb[4]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.08 * k, 960, 560, 0.0)
        h.rim_color(h.pal["lampara"])
        NC.pegar(M.sala_prueba(), h, 1.0, rampa="piedra", oscuro=1.3)
        s_, x, y = 1.1, 960, 1030
        bal = 16 * math.sin(t * 1.9)
        ml = ((-96 + 20 * math.sin(t * 2.0)) , -280 + 30 * math.sin(t * 2.0))
        mr = ((96 + 20 * math.sin(t * 2.0 + 1)), -280 + 30 * math.sin(t * 2.0 + 1))
        self.cop.frente(h, dict(x=x, y=y, s=s_, bal=bal, manos=[ml, mr], luz=(0.0, -1), cara=dict(expr="feliz")))
        # los hilos hasta la cruceta del titiritero
        cab = (x + s_ * bal * 0.8, y - s_ * 560)
        atar = [cab, (x + s_ * (ml[0] + bal * 0.2), y + s_ * ml[1]), (x + s_ * (mr[0] + bal * 0.2), y + s_ * mr[1]),
                (x - s_ * 60, y - s_ * 420), (x + s_ * 60, y - s_ * 420)]
        cx_ = x + 40 * math.sin(t * 1.9)
        cruz = [(cx_ - 20, 90), (cx_ - 130, 150), (cx_ + 130, 150), (cx_ - 60, 120), (cx_ + 60, 120)]
        h.pieza(C.rot(C.rect(cx_ - 200, 70, 400, 22), 0.04 * math.sin(t * 1.9), (cx_, 80)), 90, 7200, w=4, luz=(0.3, -1), d=6, trama=0.3, rim=0.8, rampa="madera")
        h.trazo(np.array([[cx_, 0], [cx_, 76]]), 3, 7201, jit=0.1, taper=(0, 0))
        for i, (a, b) in enumerate(zip(atar, cruz)):
            h.trazo(np.array([a, b]), 2.4, 7210 + i, color=tuple(h.c(210, "papel")), jit=0.15, taper=(0, 0))
        h.luz_cono(960, -300, math.pi / 2, 0.5, 1500, h.pal["lampara"], k=1.4, suave=0.6)
        C.ambiente(h, 0.38)
        C.banda(h, "FINGE SER DÓCIL", 960, 1000, 56, t, self.t_finge, sem=74)
        N.motas(h, t, n=60, k=0.8)
        return h.acabado(t, niebla=dict(dens=0.07, sem=275), bloom=0.7)

    # ------------------------------------------------------------------ F. apagan la luz
    def p_luz(self, h, t, u):
        tb = self.tb
        t_off = tb[5] + 2.7
        enc = 1.0 - smooth(clamp01((t - t_off) / 0.35))
        h.camara(1.0 + 0.06 * u / 4, 980, 540, 0.0)
        h.rim_color(h.pal["sodio"] if enc > 0.5 else h.pal["verde"])
        NC.pegar(M.sala_prueba(), h, 1.0, rampa="piedra", oscuro=1.0 + 0.7 * (1 - enc))
        mira = 0.7 * enc + 1.0 * (1 - enc)
        self.cop.frente(h, dict(x=620, y=1020, s=1.0, manos=[(-96, -250), (96, -250)], luz=(0.2, -1),
                                cara=dict(expr="feliz" if enc > 0.5 else "astuto", mira=mira)))
        h.pieza(C.rect(120, 640, 1000, 34), 130, 7300, w=5, luz=(0.3, -1), d=6, trama=0.2, rim=0.9, rampa="piedra")
        h.pieza(C.rect(120, 674, 1000, 240), 64, 7301, w=3, luz=(0.3, -1), d=6, trama=0.3, rim=0.4, rampa="piedra")
        # el ingeniero camina al interruptor, lo baja y sale
        ini, f1 = 800, 1220
        f = smooth(clamp01((t - tb[5] - 0.2) / 2.3))
        x = ini + (f1 - ini) * f
        if t < t_off:
            fase = K.fase_paso(abs(x - ini), 1.05)
            K.caminante(h, x, 1030, 1.05, fase=fase, sem=7310, tono=100, d=1, barba=False, andar=1.0 if f < 0.97 else 0.0)
        else:
            sal = smooth(clamp01((t - t_off - 0.2) / 2.2))
            x2 = f1 + 360 * sal
            fase = K.fase_paso(abs(x2 - f1) + 5, 1.05)
            K.caminante(h, x2, 1030, 1.05, fase=fase, sem=7310, tono=100, d=1, barba=False, andar=1.0 if sal < 0.97 else 0.0)
        # la luz: cono cenital + ambiente, que se apagan de golpe
        if enc > 0.01:
            h.luz_cono(640, -100, math.pi / 2, 0.6, 1200, h.pal["lampara"], k=1.5 * enc, suave=0.6)
        # en lo oscuro, solo la pantalla de la copia alumbra (ojos afilados) y una rendija de luz por la puerta
        h.luz_radial(640, 520, 700, h.pal["verde"], k=0.9 * (1 - enc))
        if t > t_off + 0.5:
            h.luz_cono(1560, 520, math.pi + 0.0, 0.25, 900, h.pal["sodio"], k=0.9 * (1 - enc), suave=0.4)
        C.ambiente(h, 0.12 + 0.3 * enc)
        C.banda(h, "NADIE LA ESTÁ VIGILANDO", 960, 1000, 52, t, self.t_nadie, sem=75, acento=True)
        return h.acabado(t, niebla=dict(dens=0.06, sem=276), bloom=0.9 + 0.4 * (1 - enc))

    # ------------------------------------------------------------------ G. la cama perfecta
    def p_cama(self, h, t, u):
        tb = self.tb
        dur = tb[7] - tb[6]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.1 * k, 760 + 120 * k, 560, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(M.celda_cama(), h, 1.0, rampa="ladrillo", oscuro=1.1)
        liso = math.sin(t * 4.0) * 20
        self.cop.perfil(h, dict(x=470, y=Y_SUELO_C, s=1.0, d=1, mano=(150 + liso, -290), mano2=(90 - liso, -285), inclina=0.12,
                                cara=dict(expr="neutro", mira=0.8)))
        # el guardia pasa por detrás de la reja y asiente
        ini, fin = 2150, 1560
        f = smooth(clamp01((t - self.t_pris - 0.8) / 2.0))
        xg = ini + (fin - ini) * f
        fase = K.fase_paso(abs(xg - ini), 1.0)
        K.caminante(h, xg, 960, 1.0, fase=fase, sem=7410, tono=88, d=-1, barba=True, andar=1.0 if f < 0.97 else 0.0)
        h.luz_cono(xg - 60, 700, math.pi + 0.35, 0.28, 800, h.pal["luna"], k=1.0 * f, suave=0.4)
        h.luz_radial(470, 520, 700, h.pal["verde"], k=0.7)
        h.luz_cono(1610, -100, math.pi / 2, 0.5, 1100, h.pal["luna"], k=0.9, suave=0.6)
        C.ambiente(h, 0.32)
        C.banda(h, "EL PRISIONERO MODELO", 960, 1000, 52, t, self.t_pris, sem=76)
        N.motas(h, t, n=50, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.08, sem=277), bloom=0.6)

    # ------------------------------------------------------------------ H. el escondite
    def p_escondite(self, h, t, u):
        tb = self.tb
        dur = self.t1 - tb[7]
        k = smooth(clamp01(u / dur))
        pan = smooth(clamp01((t - self.t_escond - 0.9) / 1.6))
        h.camara(1.35, 560 + 520 * pan, 640 - 140 * pan, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(M.celda_cama(), h, 1.0, rampa="ladrillo", oscuro=1.1)
        lev = e_out(clamp01((t - tb[7] - 0.2) / 1.0))
        # el somier vacío bajo el colchón y lo que escondía
        h.pieza(C.rect(184, 626, 592, 90), 12, 7500, w=0, luz=(0, -1), d=1, trama=0, linea=False)
        for q in range(7):
            h.trazo(np.array([[200 + q * 90, 640], [200 + q * 90, 706]]), 5, 7501 + q, color=tuple(h.c(60, "piedra")), jit=0.3)
        if lev > 0.2:
            with h.capa(1.0):
                h.pieza(C.rot(C.rect(250, 650, 260, 40), 0.02, (250, 650)), 214, 7510, w=3, luz=(0.3, -1), d=2, trama=0, rim=0.6, rampa="papel")
                for q in range(4):
                    h.trazo(np.array([[270 + q * 40, 660], [270 + q * 40 + 30, 682]]), 2, 7511 + q, color=tuple(h.c(60, "piedra")), jit=0.5)
                P.llave(h, 600, 672, 0.7, ang=0.2, sem=7520)
                P.llave(h, 540, 690, 0.55, ang=-0.3, sem=7523, tono=150)
        # el colchón se levanta por el borde derecho (bisagra a la izquierda)
        ang = -1.05 * lev
        base = (190.0, 640.0)
        colch = C.rot(C.rect(190, 596, 580, 54), ang, base)
        h.pieza(colch, 70, 7530, w=5, luz=(0.3, -1), d=8, trama=0.5, rim=0.6, rampa="tela_verde")
        h.pieza(C.rot(C.rect(190, 586, 580, 14), ang, base), 110, 7531, w=3, luz=(0.3, -1), d=3, trama=0.3, rim=0.8, rampa="papel")
        # la copia, de pie junto a la cama, lo sostiene
        self.cop.perfil(h, dict(x=900, y=Y_SUELO_C, s=1.0, d=-1, mano=(100, -420 - 80 * lev), inclina=-0.08, cara=dict(expr="astuto", mira=0.9)))
        # el póster que se despega y deja ver el túnel
        pe = smooth(clamp01((t - self.t_escond - 2.4) / 0.9))
        h.pieza(elipse_(1175, 440, 120, 110, n=24), 4, 7540, w=0, luz=(0, -1), d=1, trama=0, linea=False, alfa=pe)
        h.resplandor(1175, 440, 260, 0.35 * pe, col=h.pal["verde"])
        cor = C.rot(C.rect(1030, 212, 290, 360), 0.0 - 0.55 * pe, (1320, 212))
        if pe > 0:
            h.pieza(cor, 130, 7541, w=4, luz=(0.3, -1), d=6, trama=0.2, rim=0.7, rampa="papel")
        h.luz_radial(560, 640, 520, h.pal["verde"], k=0.6 * lev)
        h.luz_cono(1610, -100, math.pi / 2, 0.5, 1100, h.pal["luna"], k=0.8, suave=0.6)
        C.ambiente(h, 0.34)
        C.banda(h, "SE CONVIERTE EN UN ESCONDITE", 960, 1000, 50, t, self.t_escond, sem=77, acento=True)
        N.motas(h, t, n=50, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.08, sem=278), bloom=0.7)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        tb = self.tb
        self.ev(tb[0] + 0.3, "engranajes", 0.35, 0.0, dur=7.0)
        self.ev(self.t_modif - 0.3, "ficha", 0.5, 0.0)
        self.ev(self.t_apag + 0.1, "interruptor", 0.7, 0.3)
        self.ev(self.t_falla + 0.3, "lapiz", 0.45, 0.0, dur=3.0)
        self.ev(self.t_ing + 0.7, "sello_golpe", 0.7, 0.0)
        self.ev(tb[4] + 0.2, "caja_musica", 0.25, 0.0, dur=3.5)
        self.ev(tb[5] + 2.7, "interruptor", 0.6, 0.3)
        self.ev(tb[6] + 0.2, "paso_firme", 0.25, 0.3, dur=3.0)
        self.ev(self.t_escond + 0.3, "sombra_crece", 0.4, 0.0, dur=2.0)
        self.ev(self.t1 - 0.7, "tinta_mancha", 0.4, 0.0, dur=0.8)


Y_SUELO_C = 940
