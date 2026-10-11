# -*- coding: utf-8 -*-
"""Escena 19 «plan»: Daniel en primer plano, entre las rayas de la persiana; el «PLAN A» sobre la mesa y dos manos que se
estrechan encima, con la hoja de «2040»; lo mínimo: la máquina con el frente de cristal bajo la lupa y la casa a salvo del
que avisa; el reloj de arena, y detrás los dos autos que no aflojan."""
import math

import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import noir as N
import props as PR
import props5 as PR5
from basen import BaseNoir
from esc_precio import lupa
from motor import H, W, clamp01, e_out, smooth
from noir_pers import Frontal
from toon import elipse_, pulso


class Plan(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.dan = Frontal(sem=77)
        self.t_yque = w("Y qué propone")
        self.t_vio = w("vio venir")
        self.t_hace = w("Hace unos")
        self.t_plan = w("plan")
        self.t_acuerdo = w("acuerdo")
        self.t_esperar = w("esperar")
        self.t_yno = w("Y no construir")
        self.t_2040 = w("dos mil cuarenta")
        self.t_mientras = w("Mientras")
        self.t_minimo = w("mínimo")
        self.t_labs = w("Que los laboratorios")
        self.t_dentro = w("dentro")
        self.t_yque2 = w("Y que quien")
        self.t_decirlo = w("decirlo")
        self.t_casa = w("casa")
        self.t_pide = w("Pide tiempo")
        self.t_unico = w("Lo único")
        self.t_dar = w("dar", fin=True)
        self.plano(t0, self.p_dan)
        self.plano(self.t_hace - 0.35, self.p_plan, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_mientras - 0.35, self.p_minimo, tr="empuje", dur=0.55, centro=(W * 0.5, H * 0.5))
        self.plano(self.t_pide - 0.35, self.p_tiempo, tr="humo", dur=0.7)

    # ------------------------------------------------------------------ ¿qué propone?
    def p_dan(self, h, t, u):
        h.camara(1.0 + 0.02 * u, 960 + 10 * u, 500, 0.0)
        MU.oficina().pegar(h, 1.0, dx=-260)
        s = 2.5
        self.dan.dibujar(h, dict(x=820, y=250 + 474 * s, s=s, luz=(0.9, -0.5), rim=0.9, mira=0.4 + 0.3 * math.sin(t * 0.8),
                                 cabeza=0.03 * math.sin(t * 0.9), **K.DAN))
        N.gotas_vidrio(h, t, (1100, -460, 2000, 400), n=80, k=0.8)
        C.banda(h, "¿Y QUÉ PROPONE?", 1380, 250, 80, t, self.t_yque + 0.2, sem=5)
        C.banda(h, "EL HOMBRE QUE LO VIO VENIR", 1380, 370, 44, t, self.t_vio - 0.4, claro=True, sem=6)
        h.ambiente[:] = 0.34
        h.luz_persiana(np.array([[-200, -420], [1500, -470], [1500, 700], [-320, 960]]), k=1.5, n=15, abierto=0.5)
        h.luz_radial(1500, 80, 800, (1.0, 1.0, 1.0), k=2.2)
        N.motas(h, t, n=90, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.16, vel=10, y0=-300, y1=900, sube=False))

    # ------------------------------------------------------------------ el plan: esperar hasta 2040
    def p_plan(self, h, t, u):
        h.camara(1.0 + 0.012 * u, 960, 540, 0.008)
        MU.escritorio().pegar(h, 1.0, oscuro=0.75, dx=120, dy=-80)
        T = K.hoja(h, 600, 560, 820, 900, ang=-0.04, sem=10, renglones=9, y0=0.34, sep=48, margen=80)
        P = T([(0, -340)])[0]
        N.texto_maquina(h, "PLAN A", P[0], P[1], 150, t, self.t_hace + 0.3, cps=5, tono=0.03, centro=True, fuente=K.IMPACT, track=4.0,
                        encuadrar=False)
        P = T([(0, -230)])[0]
        N.texto_maquina(h, "julio de 2026", P[0], P[1], 40, t, self.t_plan + 0.3, cps=26, tono=0.2, centro=True, encuadrar=False)
        # dos manos se estrechan a la derecha: el acuerdo
        ap = e_out(clamp01((t - self.t_acuerdo + 0.6) / 0.7))
        sac = 10 * math.sin(t * 7) * smooth(clamp01((t - self.t_acuerdo) / 0.3)) * (1 - smooth(clamp01((t - self.t_esperar) / 0.8)))
        PR.mano(h, 1260 - 500 * (1 - ap), 760 + sac, 1.5, ang=0.0, d=1, sem=60, dedos=0.25, manga=50)
        PR.mano(h, 1560 + 500 * (1 - ap), 770 + sac, 1.5, ang=0.0, d=-1, sem=80, dedos=0.25, manga=90)
        cae = K.calendario(h, t, self.t_yno + 0.3, "NO ANTES DE", "2040", "", cx=1420, cy=330, s=0.62, sem=100, ang=0.05)
        C.banda(h, "QUE EL MUNDO SE PONGA DE ACUERDO", 1380, 1000, 44, t, self.t_acuerdo - 0.4, sem=5)
        C.banda(h, "ESPERAR", 1420, 640, 90, t, self.t_esperar, claro=True, sem=6)
        g = pulso(t, self.t_2040, 0.3, 1.0)
        h.ambiente[:] = 0.36
        h.luz_cono(960, -620, math.pi / 2, 0.66, 2400, (1.6, 1.6, 1.6), suave=0.5)
        h.luz_radial(1420, 330, 600, (1.0, 1.0, 1.0), k=1.2 * g)
        N.motas(h, t, n=80, k=0.6)
        return h.acabado(t, niebla=None, bloom=0.4, flash=0.2 * g)

    # ------------------------------------------------------------------ lo mínimo: enseñar lo de dentro; proteger al que avisa
    def p_minimo(self, h, t, u):
        h.camara(1.0 + 0.012 * u, 960, 540, 0.0)
        K.pared(h, 80, 30, paneles=10)
        K.plano_(h, C.rect(-300, 930, W + 600, 400), 70, 8, grad=(16, 930, 1200))
        h.trazo(np.array([[960, -100], [960, 1200]]), 6, 12, color=(20, 20, 20), alfa=0.6, jit=0.4, taper=(0, 0))
        # izquierda: la máquina con el frente de cristal (se ve lo de dentro) y la lupa encima
        tr = smooth(clamp01((t - self.t_labs) / 1.2))
        h.pieza(C.rect(260, 260, 400, 670), 28, 20, w=7, luz=(0.3, -1), d=18, trama=0.5, rim=0.9)
        if tr > 0:
            vid = C.rect(290, 300, 340, 590)
            K.plano_(h, vid, 200, 21, alfa=tr)
            h.luz_fija(vid, 0.3 + 0.6 * tr)
            for k in range(9):                                       # engranajes y renglones: lo que hay dentro
                yy = 330 + k * 60
                K.plano_(h, C.rect(310, yy, 300 * (0.5 + 0.5 * math.sin(k * 2.1 + t) ** 2), 10), 60, 30 + k, alfa=tr)
            for q, (gx, gy, gr) in enumerate(((380, 800, 50), (480, 760, 36), (560, 820, 44))):
                a0 = t * (1.5 if q % 2 == 0 else -2.1)
                h.anillo(h.tf(np.asarray(elipse_(gx, gy, gr, gr, n=24))), 7 * h.zoom, 50 + q, color=(40, 40, 40), alfa=tr, jit=0.3)
                for j in range(4):
                    a = a0 + j * math.pi / 2
                    h.trazo(np.array([[gx, gy], [gx + gr * math.cos(a), gy + gr * math.sin(a)]]), 5, 54 + q * 4 + j, color=(40, 40, 40),
                            alfa=tr, jit=0.2, taper=(0, 0))
        lupa(h, 520 + 60 * math.sin(t * 0.9), 520 + 110 * math.sin(t * 0.6), 130, 70)
        # derecha: el que avisa (con su silbato de luz) y su casa, que sigue encendida
        seg = smooth(clamp01((t - self.t_yque2) / 1.0))
        K.casa(h, 1560, 930, 0.95, frac=0.0, sem=100, luz_v=0.4 + 0.6 * seg)
        man = K.caminante(h, 1180, 940, 0.9, fase=0.2 * math.sin(t * 1.2), sem=140, tono=60, d=1, luz=(0.5, -0.8), rim=0.9, andar=0.3)
        for q in range(3):                                           # ondas de su aviso
            rr = ((t * 110 + q * 80) % 240) * seg
            if rr > 6:
                h.anillo(h.tf(np.asarray(elipse_(1230, 440, rr, rr, n=28))), 5 * h.zoom, 170 + q, color=(240, 240, 240),
                         alfa=0.8 * (1 - rr / 240), jit=0.4)
        C.banda(h, "LO MÍNIMO", 960, 80, 70, t, self.t_minimo - 0.3, sem=5)
        C.banda(h, "QUE ENSEÑEN LO QUE TIENEN DENTRO", 470, 1010, 40, t, self.t_dentro - 0.8, claro=True, sem=6)
        C.banda(h, "QUE AVISAR NO CUESTE LA CASA", 1450, 1010, 40, t, self.t_decirlo - 0.3, claro=True, sem=7)
        h.ambiente[:] = 0.5
        h.luz_radial(460, 560, 900, (1.0, 1.0, 1.0), k=0.8)
        h.luz_radial(1500, 640, 900, (1.0, 1.0, 1.0), k=0.5 + 0.5 * seg)
        N.motas(h, t, n=100, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.14, vel=10, y0=0, y1=1080, sube=False), bloom=0.5)

    # ------------------------------------------------------------------ pide tiempo
    def p_tiempo(self, h, t, u):
        h.camara(1.0 + 0.016 * u, 960, 540, 0.0)
        K.pared(h, 40, 12, ladrillo=True)
        K.plano_(h, C.rect(-300, 900, W + 600, 400), 44, 8, grad=(12, 900, 1200))
        for k, (y, s_, b, v) in enumerate(((880, 0.8, "estrella", 420), (1010, 1.0, "franjas", 470))):      # los dos autos, sin aflojar
            x = ((t - self.t_pide) * v + 300 + k * 500) % 2800 - 400
            PR5.auto(h, x, y, s_, t, vel=3.0, sem=40 + k * 40, tono=40 - 8 * k, bandera=b)
        f = clamp01(0.25 + (t - self.t_pide) / 14.0)
        K.reloj_arena(h, 960, 470, 1.15, f, t, sem=120)
        C.banda(h, "PIDE TIEMPO", 400, 200, 100, t, self.t_pide, sem=5)
        C.banda(h, "LO QUE EN UNA CARRERA NADIE DA", 1480, 200, 44, t, self.t_unico + 0.3, claro=True, sem=6)
        h.ambiente[:] = 0.4
        h.luz_cono(960, -500, math.pi / 2, 0.36, 2000, (1.6, 1.6, 1.6), suave=0.5)
        N.motas(h, t, n=100, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.18, vel=20, y0=300, y1=1080, sube=False), bloom=0.5)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        t0 = self.t0
        self.ev(t0, "lluvia_amb", 0.7, 0.0, dur=self.t_hace - t0)
        self.ev(self.t_yque + 0.2, "sello_golpe", 0.9, 0.3)
        self.ev(self.t_hace - 0.35, "papel_atrapa", 0.8, -0.3)
        self.ev(self.t_hace + 0.3, "tecleo_rapido", 0.6, -0.3, dur=1.2)
        self.ev(self.t_acuerdo, "apreton", 0.9, 0.3)
        self.ev(self.t_esperar, "sello_golpe", 0.9, 0.3)
        self.ev(self.t_yno + 0.1, "papel_arranca", 0.9, 0.3)
        self.ev(self.t_2040, "golpe_grave", 1.0, 0.0)
        self.ev(self.t_mientras - 0.35, "barrido_aire", 0.6, 0.0, dur=0.6)
        self.ev(self.t_minimo - 0.3, "sello_golpe", 0.8, 0.0)
        self.ev(self.t_labs, "lupa", 0.7, -0.4)
        self.ev(self.t_labs + 0.3, "engranajes", 0.5, -0.4, dur=self.t_yque2 - self.t_labs)
        self.ev(self.t_yque2, "teremin", 0.5, 0.4, dur=1.6)
        self.ev(self.t_pide - 0.35, "motores_carrera", 0.6, 0.0, dur=self.t1 - self.t_pide)
        self.ev(self.t_pide, "sello_golpe", 1.0, -0.3)
        self.ev(self.t_pide, "reloj_pared", 0.7, 0.0, dur=self.t1 - self.t_pide - 0.5)
        self.ev(self.t1 - 0.8, "tinta_mancha", 0.6, 0.0, dur=0.9)
