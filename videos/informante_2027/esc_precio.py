# -*- coding: utf-8 -*-
"""Escena 5 «precio»: la lupa recorre el acuerdo hasta la cláusula («NUNCA», «DE POR VIDA»); la balanza: su voz contra las
acciones (gana el dinero); la casa de la familia de noche, que se queda a oscuras hasta el 85 %; la mesa donde todos firman...
y el foco sobre la hoja de Daniel, en blanco: NO FIRMÓ."""
import math

import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import noir as N
import props as PR
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from noir_pers import Frontal
from toon import Pista, elipse_, pulso, suave


def lupa(h, x, y, r=170, sem=0):
    h.trazo(np.array([[x + r * 0.72, y + r * 0.72], [x + r * 1.9, y + r * 1.9]]), 44, sem, color=(30, 30, 30), jit=0.4, taper=(0, 0))
    h.anillo(h.tf(np.asarray(elipse_(x, y, r, r, n=50))), 22 * h.zoom, sem + 1, color=(30, 30, 30), jit=0.4)
    h.anillo(h.tf(np.asarray(elipse_(x, y, r - 12, r - 12, n=50))), 4 * h.zoom, sem + 2, color=(230, 230, 230), jit=0.3, alfa=0.7)
    h.luz_radial(x, y, r * 1.5, (1.0, 1.0, 1.0), k=0.7)


class Precio(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.dan = Frontal(sem=77)
        self.otros = [Frontal(sem=300 + 17 * k) for k in range(4)]
        self.t_acuerdo = w("acuerdo")
        self.t_clau = w("cláusula")
        self.t_nohablar = w("no hablar")
        self.t_nunca = w("Nunca")
        self.t_vida = w("De por vida")
        self.t_ysi = w("Y si no")
        self.t_perder = w("perder")
        self.t_dosm = w("dos millones")
        self.t_familia = w("Para su familia")
        self.t_85 = w("ochenta")
        self.t_todo = w("todo")
        self.t_conozco = w("Conozco")
        self.t_firmarian = w("firmarían")
        self.t_el = w("Él no")
        self.t_firmo = w("firmó", fin=True)
        self.lup = Pista([(t0, (1500, 260)), (self.t_clau, (1050, 420), "io"), (self.t_nohablar + 0.2, (700, 560), "io"),
                          (self.t_nunca, (1180, 580), "io"), (self.t1, (1250, 600), "l")])
        self.plano(t0, self.p_clausula)
        self.plano(self.t_ysi - 0.35, self.p_balanza, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_familia - 0.35, self.p_casa, tr="humo", dur=0.7)
        self.plano(self.t_conozco - 0.35, self.p_firman, tr="barrido", dur=0.6, dirx=-1)

    # ------------------------------------------------------------------ la cláusula
    def p_clausula(self, h, t, u):
        h.camara(1.0 + 0.012 * u, 960, 540, -0.035)
        MU.escritorio().pegar(h, 1.0, oscuro=0.75, dx=100, dy=30)
        T = K.hoja(h, 960, 620, 1560, 1100, ang=-0.03, sem=10, renglones=4, y0=0.14, sep=42, margen=120)
        P = T([(0, -490)])[0]
        N.texto_maquina(h, "ACUERDO DE SALIDA", P[0], P[1], 62, t, -99, cps=1e9, tono=0.05, centro=True, fuente=N.FUENTE_SELLO,
                        encuadrar=False)
        P = T([(-660, -210)])[0]
        N.texto_maquina(h, "CLÁUSULA 7 — NO DESPRESTIGIO", P[0], P[1], 40, t, self.t_clau - 0.4, cps=30, tono=0.2, encuadrar=False)
        P = T([(-660, -120)])[0]
        N.texto_maquina(h, "El firmante se compromete a", P[0], P[1], 58, t, self.t_clau + 0.2, cps=30, tono=0.06, encuadrar=False)
        P = T([(-660, -20)])[0]
        N.texto_maquina(h, "NO HABLAR MAL DE LA EMPRESA.", P[0], P[1], 82, t, self.t_nohablar - 0.2, cps=22, tono=0.03, fuente=K.IMPACT,
                        track=3.0, encuadrar=False)
        for k in range(5):
            K.plano_(h, T(C.rect(-660, 150 + k * 44, 1200 * (0.9 - 0.1 * (k % 3)), 8)), 118, 40 + k, alfa=0.7)
        lx, ly = self.lup(t)
        lupa(h, lx, ly, 175, 60)
        C.banda(h, "NUNCA", 1420, 300, 130, t, self.t_nunca, sem=5)
        C.banda(h, "DE POR VIDA", 1420, 470, 84, t, self.t_vida, claro=True, sem=6)
        h.ambiente[:] = 0.34
        h.luz_cono(700, -560, math.pi / 2 - 0.1, 0.6, 2400, (1.5, 1.5, 1.5), suave=0.5)
        N.motas(h, t, n=80, k=0.6)
        return h.acabado(t, niebla=None, bloom=0.4)

    # ------------------------------------------------------------------ su voz contra sus acciones
    def p_balanza(self, h, t, u):
        h.camara(1.0 + 0.015 * u, 960, 520, 0.0)
        K.pared(h, 46, 14, paneles=9)
        inc = e_out(clamp01((t - self.t_dosm) / 0.6)) * (1.0 + 0.06 * math.sin(t * 5) * math.exp(-(t - self.t_dosm)))
        inc = inc if t > self.t_dosm else -0.25 * smooth(clamp01((t - self.t_ysi) / 0.8))
        pl, pr = K.balanza(h, 960, 210, incl=inc, s=1.0, sem=20)
        # platillo izquierdo: su voz (un bocadillo de palabra)
        bx, by = pl[0], pl[1] - 110
        h.pieza(np.asarray(suave([(bx - 110, by - 60), (bx + 110, by - 60), (bx + 120, by + 30), (bx + 20, by + 44), (bx - 10, by + 92),
                                  (bx - 30, by + 44), (bx - 120, by + 30)], 4)), 228, 50, w=5, luz=(0.2, -1), d=10, trama=0.1, rim=0.5)
        N.texto_maquina(h, "SU VOZ", bx, by - 12, 50, t, -99, cps=1e9, tono=0.04, centro=True, fuente=K.IMPACT, encuadrar=False)
        # platillo derecho: los fajos van cayendo
        for k in range(4):
            tk = self.t_perder + k * 0.3
            a = clamp01((t - tk) / 0.25)
            if a > 0:
                K.billetes(h, pr[0] - 60 + 40 * k, pr[1] + 4 - 500 * (1 - a) ** 2, 2 + (k % 2), 0.8, 100 + k * 11)
        C.banda(h, "SUS ACCIONES", 1400, 150, 60, t, self.t_perder, sem=5)
        C.banda(h, "≈ US$ 1,7 A 2 MILLONES", 1400, 250, 50, t, self.t_dosm, claro=True, sem=6)
        C.banda(h, "SI NO FIRMA: SE ARRIESGA A PERDERLAS", 960, 1010, 46, t, self.t_ysi + 0.3, sem=7)
        h.ambiente[:] = 0.3
        PR.lampara_colgante(h, 960, -700, largo=420, ang=0.07 * math.sin(t * 1.1), k=1.3, sem=80, abre=0.9, alcance=2000)
        N.motas(h, t, n=100, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.18, vel=10, y0=-200, y1=1000, sube=False), bloom=0.45)

    # ------------------------------------------------------------------ el 85 % de lo que tenía su familia
    def p_casa(self, h, t, u):
        h.camara(1.0 + 0.02 * u, 960 - 10 * u, 560, 0.0)
        MU.cielo().pegar(h, 0.05, dx=-(t * 6.0) % 300)
        MU.lejos().pegar(h, 0.3, bruma=0.6, tono_bruma=0.34)
        K.plano_(h, C.rect(-400, 900, W + 800, 500), 34, 8, grad=(10, 900, 1200))                       # el jardín
        for k in range(22):                                          # cerca de estacas
            x = -60 + k * 96
            h.pieza(np.array([[x, 960], [x + 15, 930], [x + 30, 960], [x + 30, 1060], [x, 1060]]), 150, 20 + k, w=3, luz=(0.3, -1), d=5,
                    trama=0.3, rim=0.6)
        h.trazo(np.array([[-100, 1000], [W + 100, 1000]]), 8, 50, color=(120, 120, 120), jit=0.3, taper=(0, 0))
        fr = smooth(clamp01((t - self.t_85 + 0.2) / 1.6)) * 0.85
        K.casa(h, 700, 930, 1.5, frac=fr, sem=60, luz_v=1.0 - fr)
        # el árbol con columpio (se mece)
        h.pieza(np.asarray(suave([(1420, 930), (1440, 600), (1400, 520), (1470, 540), (1500, 420), (1520, 560), (1590, 500), (1540, 620),
                                  (1520, 930)], 3)), 30, 90, w=5, luz=(0.3, -1), d=10, trama=0.5, rim=0.6)
        h.pieza(np.asarray(elipse_(1490, 400, 260, 200, n=30)), 40, 91, w=5, luz=(0.3, -1), d=22, trama=0.7, rim=0.6)
        a = 0.22 * math.sin(t * 1.5)
        sx, sy = 1700 + 260 * math.sin(a), 470 + 260 * math.cos(a)
        for q in (-1, 1):
            h.trazo(np.array([[1700 + q * 26, 470], [sx + q * 26, sy]]), 2.5, 92 + q, color=(170, 170, 170), jit=0.2, taper=(0, 0))
        h.pieza(C.rect(sx - 40, sy, 80, 12), 140, 95, w=3, luz=(0.3, -1), d=3, trama=0, rim=0.7)
        h.trazo(np.array([[1560, 470], [1760, 470]]), 14, 96, color=(30, 30, 30), jit=0.4)
        C.banda(h, "85 %", 1420, 220, 190, t, self.t_85, sem=5)
        C.banda(h, "DE TODO LO QUE TENÍA SU FAMILIA", 1380, 380, 46, t, self.t_todo - 0.3, claro=True, sem=6)
        h.ambiente[:] = 0.75
        h.luz_radial(700, 700, 900, (1.0, 1.0, 1.0), k=0.9 * (1 - fr))
        N.lluvia(h, t, n=420, vel=1600, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.24, y0=300, y1=1080, vel=24), bloom=0.5)

    # ------------------------------------------------------------------ todos firman; él no
    def p_firman(self, h, t, u):
        h.camara(1.0 + 0.012 * u, 960, 540, 0.0)
        K.pared(h, 42, 12, paneles=10)
        solo = smooth(clamp01((t - self.t_el + 0.2) / 0.6))
        looks = [dict(pelo="blanco", traje=92, gafas=True), dict(pelo="calvo", traje=52), None, dict(pelo="rizado", traje=44),
                 dict(pelo="oscuro", traje=84, gafas=True)]
        s = 1.3
        k2 = 0
        for k in range(5):
            x = 250 + k * 355
            if looks[k] is None:
                p = dict(x=x, y=330 + 474 * s, s=s, luz=(0.0, -1.0), rim=0.9, mira=0.0, cabeza=0.0, **K.DAN)
                self.dan.dibujar(h, p)
            else:
                p = dict(looks[k])
                p.update(x=x, y=330 + 474 * s, s=s, luz=(0.0, -1.0), rim=0.7, mira=0.0, cabeza=0.12 + 0.03 * math.sin(t * 7 + k))
                self.otros[k2].dibujar(h, p)
                k2 += 1
        PR.mesa(h, 960, 930, ancho=1880, fondo=170, alto=260, tono=70, sem=30)
        for k in range(5):                                           # las hojas y las firmas
            x = 250 + k * 355
            Q = np.array([[x - 110, 790], [x + 110, 790], [x + 130, 900], [x - 130, 900]])
            h.pieza(Q, 228, 100 + k, w=3, luz=(0, -1), d=4, trama=0, rim=0)
            if k != 2:
                a = clamp01((t - self.t_conozco - 0.3 - 0.35 * k2_(k)) / 0.8)
                K.garabato(h, x - 70, 850, a, 0.55, 120 + k)
        C.banda(h, "NO FIRMÓ", 960, 200, 150, t, self.t_firmo - 0.35, claro=True, sem=5)
        h.ambiente[:] = 0.5 - 0.3 * solo
        for k in range(5):
            x = 250 + k * 355
            kk = 1.0 if k == 2 else (1.0 - 0.85 * solo)
            h.luz_cono(x, -400, math.pi / 2, 0.16, 1800, (1.5, 1.5, 1.5), k=1.0 * kk, suave=0.5)
        N.motas(h, t, n=100, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.18, vel=10, y0=-200, y1=1000, sube=False), bloom=0.45)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        t0 = self.t0
        self.ev(t0 + 0.3, "papel_atrapa", 0.7, 0.0)
        self.ev(self.t_clau - 0.4, "lupa", 0.7, 0.2)
        self.ev(self.t_nohablar - 0.2, "tecleo_rapido", 0.6, -0.2, dur=1.2)
        self.ev(self.t_nunca, "sello_golpe", 1.0, 0.3)
        self.ev(self.t_vida, "sello_golpe", 0.9, 0.3)
        self.ev(self.t_vida, "golpe_grave", 0.8, 0.0)
        self.ev(self.t_ysi - 0.35, "barrido_aire", 0.6, 0.0, dur=0.7)
        self.ev(self.t_ysi, "zumbido_lampara", 0.4, 0.0, dur=self.t_familia - self.t_ysi)
        for k in range(4):
            self.ev(self.t_perder + 0.25 + k * 0.3, "fichas_empuja", 0.6, 0.4)
        self.ev(self.t_dosm, "caja_registradora", 0.8, 0.3)
        self.ev(self.t_dosm + 0.1, "caida", 0.6, 0.3)
        self.ev(self.t_familia - 0.35, "lluvia_amb", 0.7, 0.0, dur=self.t_conozco - self.t_familia + 0.4)
        self.ev(self.t_85 - 0.2, "sombra_crece", 0.8, 0.0, dur=2.0)
        self.ev(self.t_85, "golpe_grave", 1.0, 0.0)
        self.ev(self.t_conozco - 0.35, "barrido_aire", 0.6, 0.0, dur=0.7)
        for k in range(4):
            self.ev(self.t_conozco + 0.3 + 0.35 * k, "pluma", 0.6, -0.6 + 0.4 * k)
        self.ev(self.t_el - 0.2, "focos", 0.8, 0.0)
        self.ev(self.t_firmo - 0.35, "sello_golpe", 1.0, 0.0)
        self.ev(self.t1 - 0.8, "tinta_mancha", 0.6, 0.0, dur=0.9)


def k2_(k):
    return k if k < 2 else k - 1
