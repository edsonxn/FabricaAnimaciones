# -*- coding: utf-8 -*-
"""Escena 7 «manual»: sobre el escritorio, la máscara junto a un libro viejo que se abre; cuatro capítulos, cada uno su cuadro:
1 AUTORIDAD (la sombra enorme del jefe sobre el empleado), 2 SECRETO (el dedo en los labios y el sobre lacrado), 3 PRISA (el reloj
desbocado y la cuenta atrás), 4 EL GRUPO (la fila que asiente y el único que duda); el libro se cierra: «Manual del estafador»."""
import math

import numpy as np

import comun as C
import mundos as MU
import noir as N
import props as PR
from basen import BaseNoir
from esc_truco import mascara
from motor import H, W, clamp01, e_out, smooth
from noir_pers import Frontal
from toon import Pista, elipse_, pulso, suave, tubo


def capitulo(h, n, titulo, t, t0, x=230, y=170):
    """Cabecera de capítulo: número enorme y título en banda."""
    if t < t0:
        return
    with C.fijo(h):
        N.texto_maquina(h, str(n), x - 110, y, 230, t, -99, cps=1e9, tono=0.97, centro=True, fuente=N.FUENTE_SELLO, encuadrar=False)
    C.banda(h, titulo, x + 60 + 26 * len(titulo), y + 10, 88, t, t0, claro=True, sem=700 + n)


def libro(h, cx, cy, ab, t, sem=0, titulo=True):
    """Libro viejo: ab = 0 cerrado (se ve la tapa), 1 abierto por la mitad."""
    if ab < 0.5:
        h.pieza(PR.rot(C.rect(cx - 330, cy - 430, 660, 860), -0.04, np.array([cx, cy])), 44, sem, w=8, luz=(0.3, -1), d=18, trama=0.6, rim=0.6)
        h.pieza(PR.rot(C.rect(cx - 330, cy - 430, 70, 860), -0.04, np.array([cx, cy])), 26, sem + 1, w=5, luz=(0.3, -1), d=6, trama=0.5)
        h.anillo(h.tf(PR.rot(C.rect(cx - 220, cy - 380, 500, 760), -0.04, np.array([cx, cy]))), 4 * h.zoom, sem + 2, color=(190, 190, 190), jit=0.5)
        if titulo:
            for k, (s_, px, dy) in enumerate((("MANUAL", 110, -200), ("DEL", 60, -90), ("ESTAFADOR", 96, 10))):
                N.texto_maquina(h, s_, cx + 30, cy + dy, px, t, -99, cps=1e9, tono=0.88, centro=True, fuente=N.FUENTE_SELLO, encuadrar=False)
    else:
        for sx in (-1, 1):
            P = np.array([[cx, cy - 430], [cx + sx * 640, cy - 400], [cx + sx * 660, cy + 440], [cx, cy + 420]])
            h.pieza(P, 206 - 10 * (sx < 0), sem + 3 + sx, w=6, luz=(0.3, -1), d=14, trama=0.3, rim=0)
            for q in range(13):
                h.trazo(np.array([[cx + sx * 70, cy - 330 + q * 56], [cx + sx * (560 - 60 * ((q * 7) % 4)), cy - 322 + q * 56]]), 5,
                        sem + 10 + q + 20 * (sx > 0), alfa=0.45, jit=0.4)
        h.trazo(np.array([[cx, cy - 430], [cx, cy + 420]]), 9, sem + 60, jit=0.4)


class Manual(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.jefe = Frontal(sem=40)
        self.emp = Frontal(sem=210)
        self.fila = [Frontal(sem=500 + 9 * k) for k in range(5)]
        self.t_pero = w("Pero la")
        self.t_mitad = w("mitad")
        self.t_otra = w("La otra")
        self.t_vieja = w("vieja")
        self.t_prim = w("Primero")
        self.t_aut = w("autoridad")
        self.t_quien = w("Quien")
        self.t_jefe = w("jefe")
        self.t_seg = w("Segundo")
        self.t_secreto = w("secreto")
        self.t_oper = w("Una operación")
        self.t_nadie = w("nadie", frase=2)
        self.t_ter = w("Tercero")
        self.t_prisa = w("prisa")
        self.t_cuando = w("Cuando no")
        self.t_piensa = w("piensa", fin=True)
        self.t_cuarto = w("Y cuarto")
        self.t_grupo = w("grupo")
        self.t_si = w("Si todos")
        self.t_quieneres = w("quién eres")
        self.t_ia = w("La inteligencia")
        self.t_caras = w("caras")
        self.t_resto = w("El resto")
        self.t_manual = w("manual")
        self.t_siglo = w("siglo")
        self.plano(t0, self.p_libro)
        self.plano(self.t_prim - 0.35, self.p_autoridad, tr="barrido", dur=0.55, dirx=1)
        self.plano(self.t_seg - 0.35, self.p_secreto, tr="barrido", dur=0.55, dirx=1)
        self.plano(self.t_ter - 0.35, self.p_prisa, tr="barrido", dur=0.55, dirx=1)
        self.plano(self.t_cuarto - 0.35, self.p_grupo, tr="barrido", dur=0.55, dirx=1)
        self.plano(self.t_ia - 0.35, self.p_cierre, tr="humo", dur=0.7)

    # ------------------------------------------------------------------ la otra mitad del truco
    def p_libro(self, h, t, u):
        h.camara(1.0 + 0.03 * u, 960, 540, -0.015)
        MU.escritorio().pegar(h, 1.0, oscuro=0.8)
        ab = smooth(clamp01((t - self.t_vieja + 0.4) / 0.8))
        ent = e_out(clamp01((t - self.t_otra + 0.4) / 0.5))
        mascara(h, 480 - 60 * ent, 540, 2.5, 30, tono=230, ang=-0.12 + 0.02 * math.sin(t), datos=1.0, t=t)
        bx = 1330 + 900 * (1 - ent)
        libro(h, bx if ab < 0.5 else 1250, 540, ab, t, sem=60, titulo=False)
        C.banda(h, "MEDIO TRUCO", 470, 990, 56, t, self.t_mitad, claro=True, sem=5)
        C.banda(h, "EL OTRO MEDIO", 1330, 990, 56, t, self.t_otra, claro=True, sem=6)
        if ab < 0.5:
            N.humo(h, t, bx, 300, k=0.8 * ent, ancho=2.4, hebras=5, viento=(-20, -60), sem=3)        # polvo del libro viejo
        h.ambiente[:] = 0.36
        h.luz_cono(900, -500, math.pi / 2, 0.62, 2100, (1.4, 1.4, 1.4), suave=0.6)
        N.motas(h, t, n=110, k=0.7)
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ 1. autoridad
    def p_autoridad(self, h, t, u):
        h.camara(1.0 + 0.03 * u, 960, 540, 0.0)
        h.pieza(C.rect(-100, -100, W + 200, H + 200), 120, 5, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False, grad=(60, 0, H))
        # la sombra enorme del jefe en la pared (crece al decir «jefe de los jefes»)
        cr = 1.0 + 0.35 * smooth(clamp01((t - self.t_quien) / 2.0))
        s = 4.0 * cr
        h.silueta = ((14, 14, 14), 0.8)
        self.jefe.dibujar(h, dict(x=1180, y=420 + 474 * s, s=s, luz=(0, -1), pelo="blanco", traje=20, placa=False))
        h.silueta = None
        # el empleado, pequeño, de espaldas a la sombra
        se = 1.15
        self.emp.dibujar(h, dict(x=560, y=1040, s=se, luz=(-0.6, -0.6), rim=0.9, pelo="oscuro", traje=150, mira=0.9,
                                 cabeza=0.5 * smooth(clamp01((t - self.t_quien) / 0.6))))
        capitulo(h, 1, "AUTORIDAD", t, self.t_aut - 0.15)
        N.texto_maquina(h, "«Lo ordena el jefe de los jefes.»", 620, 400, 40, t, self.t_quien, cps=24, tono=0.03, centro=True,
                        encuadrar=False)
        h.ambiente[:] = 0.42
        h.luz_cono(200, 1300, -0.75, 0.75, 2400, (1.4, 1.4, 1.4), suave=0.7)
        N.motas(h, t, n=80, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.14, vel=8, y0=200, y1=1080))

    # ------------------------------------------------------------------ 2. secreto
    def p_secreto(self, h, t, u):
        h.camara(1.0 + 0.03 * u, 960, 540, 0.0)
        h.img[:] = 0.06
        s = 3.4
        p = dict(x=620, y=560 + 474 * s, s=s, luz=(0.7, -0.7), rim=0.8, pelo="sombrero", traje=34, mira=0.5)
        Frontal(sem=230).dibujar(h, p)
        # el dedo sobre los labios
        sube = e_out(clamp01((t - self.t_secreto + 0.3) / 0.4))
        fy = 600 + 60 * s * 0.3 + 700 * (1 - sube)
        h.pieza(np.array(tubo(np.array([[640.0, fy + 520], [628, fy + 250], [620, fy]]), 110, 62)), 130, 40, w=7, luz=(0.7, -0.7), d=14,
                trama=0.4, rim=0.8)
        h.pieza(np.array(suave([(500, fy + 520), (520, fy + 380), (640, fy + 330), (760, fy + 390), (780, fy + 520)], 4)), 124, 41, w=7,
                luz=(0.7, -0.7), d=14, trama=0.5, rim=0.8)
        # el sobre lacrado y los cerrojos: no se puede consultar con nadie
        if t > self.t_oper - 0.3:
            a = e_out(clamp01((t - self.t_oper + 0.3) / 0.4))
            PR.sobre(h, 1400, 470 + 500 * (1 - a), s=1.5, ang=0.06, abierto=0.0, sem=60, texto="", t=t)
            h.pieza(elipse_(1400, 470 + 500 * (1 - a) + 40, 60, 60, n=24), 30, 70, w=5, luz=(0.3, -1), d=8, trama=0.4, rim=0.8)   # lacre
            N.texto_maquina(h, "CONFIDENCIAL", 1400, 300 + 500 * (1 - a), 46, t, -99, cps=1e9, tono=0.05, centro=True,
                            fuente=N.FUENTE_SELLO, encuadrar=False)
        for k in range(4):                                       # los colegas a los que ya no puede preguntar: se tachan
            tk = self.t_nadie - 1.0 + 0.2 * k
            a = clamp01((t - tk) / 0.25)
            if t < self.t_oper + 0.8:
                continue
            x = 1130 + k * 180
            h.pieza(elipse_(x, 820, 46, 52, n=20), 140, 80 + k, w=5, luz=(0, -1), d=8, trama=0.4, rim=0.6)
            h.pieza(np.array(suave([(x - 64, 960), (x - 50, 890), (x, 872), (x + 50, 890), (x + 64, 960)], 3)), 70, 90 + k, w=5, luz=(0, -1),
                    d=8, trama=0.4, rim=0.6)
            if a > 0:
                from esc_dinero import tache
                tache(h, x, 880, 70, a, sem=100 + 2 * k, w=14)
        capitulo(h, 2, "SECRETO", t, self.t_secreto - 0.15)
        h.ambiente[:] = 0.30
        h.luz_cono(1150, -500, math.pi / 2 + 0.2, 0.6, 2100, (1.5, 1.5, 1.5), suave=0.6)
        h.luz_radial(1400, 700, 800, (0.8, 0.8, 0.8), k=0.8)
        N.motas(h, t, n=80, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.16, vel=8, y0=-200, y1=900, sube=False))

    # ------------------------------------------------------------------ 3. prisa
    def p_prisa(self, h, t, u):
        h.camara(1.0 + 0.03 * u, 960, 540, 0.01 * math.sin(t * 9) * clamp01(u / 3))
        h.img[:] = 0.06
        cx, cy, r = 1230, 560, 400
        h.pieza(elipse_(cx, cy, r + 40, r + 40, n=60), 40, 20, w=10, luz=(-0.4, -1), d=22, trama=0.6, rim=0.8)
        h.pieza(elipse_(cx, cy, r, r, n=60), 216, 21, w=6, luz=(-0.4, -1), d=14, trama=0.3, sombra=0.4)
        for q in range(12):
            a = q * math.pi / 6
            h.trazo(np.array([[cx + (r - 60) * math.sin(a), cy - (r - 60) * math.cos(a)], [cx + (r - 14) * math.sin(a), cy - (r - 14) * math.cos(a)]]),
                    14 if q % 3 == 0 else 7, 30 + q, jit=0.3, taper=(0, 0))
        vel = 1.0 + 9.0 * smooth(clamp01((t - self.t_prisa) / 2.5))                 # las manecillas se desbocan
        am = (t - self.t_ter) * vel * 1.3
        ah = am / 12.0 + 1.0
        h.trazo(np.array([[cx, cy], [cx + 210 * math.sin(ah), cy - 210 * math.cos(ah)]]), 26, 50, jit=0.3, taper=(0, 0.4))
        h.trazo(np.array([[cx, cy], [cx + 330 * math.sin(am), cy - 330 * math.cos(am)]]), 15, 51, jit=0.3, taper=(0, 0.5))
        h.pieza(elipse_(cx, cy, 26, 26, n=18), 20, 52, w=4, luz=(0, -1), d=4, trama=0)
        # la cuenta atrás
        rest = max(0.0, (self.t_piensa - t)) / max(0.1, self.t_piensa - self.t_ter) * 59
        N.texto_maquina(h, f"00:{int(rest):02d}", 440, 600, 190, t, self.t_prisa, cps=1e9, tono=0.96, centro=True, fuente=N.FUENTE_SELLO,
                        encuadrar=False)
        N.texto_maquina(h, "no hay tiempo para pensar", 440, 760, 40, t, self.t_cuando, cps=26, tono=0.92, centro=True, encuadrar=False)
        capitulo(h, 3, "PRISA", t, self.t_prisa - 0.15)
        h.ambiente[:] = 0.36
        h.luz_cono(cx, -500, math.pi / 2, 0.5, 2000, (1.6, 1.6, 1.6), suave=0.5)
        N.motas(h, t, n=80, k=0.5)
        return h.acabado(t, niebla=None, bloom=0.45)

    # ------------------------------------------------------------------ 4. el grupo
    def p_grupo(self, h, t, u):
        h.camara(1.0 + 0.025 * u, 960 + 10 * u, 560, 0.0)
        MU.sala_rueda().pegar(h, 1.0, oscuro=0.7)
        looks = [dict(pelo="blanco", traje=92, gafas=True), dict(pelo="oscuro", traje=52), dict(pelo="calvo", traje=74, barba=True),
                 dict(pelo="rizado", traje=44), dict(pelo="oscuro", traje=84, gafas=True)]
        si = smooth(clamp01((t - self.t_si) / 0.5))
        for k, F in enumerate(self.fila):
            nod = si * 0.5 * (0.5 - 0.5 * math.cos(t * 6.5 + k * 0.5))
            p = dict(looks[k])
            p.update(x=300 + k * 250, y=900 + 16 * nod, s=1.25, luz=(0.0, -1.0), rim=0.85, mira=0.9, cabeza=0.1)
            F.dibujar(h, p)
            if si > 0.5 and (int(t * 2.2 + k * 0.7) % 3 == 0):
                C.banda(h, "SÍ", 300 + k * 250, 250, 54, t, -99, claro=True, sem=20 + k)
        # el que duda, aparte
        self.emp.dibujar(h, dict(x=1640, y=900, s=1.25, luz=(0.0, -1.0), rim=0.9, pelo="oscuro", traje=150, mira=-0.9,
                                 cabeza=-0.4 * smooth(clamp01((t - self.t_quieneres) / 0.5))))
        if t > self.t_quieneres:
            N.texto_maquina(h, "¿no...?", 1600, 250, 60, t, self.t_quieneres, cps=10, tono=0.95, centro=True, encuadrar=False)
        capitulo(h, 4, "EL GRUPO", t, self.t_grupo - 0.15, x=230, y=960)
        h.ambiente[:] = 0.28
        for k in range(5):
            h.luz_cono(300 + k * 250, -540, math.pi / 2, 0.26, 1650, (1.3, 1.3, 1.3), k=0.9, suave=0.5)
        h.luz_cono(1640, -540, math.pi / 2, 0.26, 1650, (1.6, 1.6, 1.6), k=0.55, suave=0.5)
        N.motas(h, t, n=110, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.18, vel=8, y0=-200, y1=900, sube=False))

    # ------------------------------------------------------------------ el manual
    def p_cierre(self, h, t, u):
        h.camara(1.0 + 0.035 * u, 960, 540, 0.012)
        MU.escritorio().pegar(h, 1.0, oscuro=0.8)
        ab = 1 - smooth(clamp01((t - self.t_resto + 0.3) / 0.7))
        libro(h, 1180, 540, ab, t, sem=60, titulo=True)
        mascara(h, 420, 540, 2.3, 30, tono=230, ang=-0.15, datos=1.0, t=t)
        C.banda(h, "LA IA PUSO LAS CARAS", 430, 990, 50, t, self.t_caras - 0.3, claro=True, sem=7)
        if ab < 0.5:
            for k, s_ in enumerate(("1 AUTORIDAD", "2 SECRETO", "3 PRISA", "4 GRUPO")):         # las pestañas de los capítulos
                tk = self.t_manual + 0.18 * k
                if t < tk:
                    continue
                y = 240 + k * 150
                h.pieza(C.rect(1500, y, 330, 96), 216, 100 + k, w=4, luz=(0.3, -1), d=6, trama=0, rim=0)
                N.texto_maquina(h, s_, 1665, y + 48, 40, t, -99, cps=1e9, tono=0.05, centro=True, fuente=N.FUENTE_SELLO, encuadrar=False)
            C.banda(h, "DESDE HACE UN SIGLO", 1180, 1010, 50, t, self.t_siglo - 0.3, claro=True, sem=8)
        h.ambiente[:] = 0.36
        h.luz_cono(1000, -500, math.pi / 2, 0.62, 2100, (1.4, 1.4, 1.4), suave=0.6)
        N.motas(h, t, n=110, k=0.7)
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        self.ev(self.t_otra - 0.4, "sobre_desliza", 0.8, 0.4)
        self.ev(self.t_vieja - 0.4, "paginas", 0.8, 0.3, dur=1.2)
        for k, tk in enumerate((self.t_prim, self.t_seg, self.t_ter, self.t_cuarto)):
            self.ev(tk - 0.35, "barrido_aire", 0.6, 0.3, dur=0.7)
            self.ev(tk - 0.3, "paginas", 0.6, 0.0, dur=0.6)
        for tk in (self.t_aut, self.t_secreto, self.t_prisa, self.t_grupo):
            self.ev(tk - 0.15, "sello_golpe", 0.9, -0.5)
        self.ev(self.t_quien, "sombra_crece", 0.8, 0.3, dur=2.5)
        self.ev(self.t_oper - 0.3, "sobre_desliza", 0.7, 0.5)
        for k in range(4):
            self.ev(self.t_nadie - 1.0 + 0.2 * k, "tachon", 0.7, 0.2 + 0.2 * k)
        self.ev(self.t_ter, "reloj_pared", 0.9, 0.3, dur=self.t_cuarto - self.t_ter)
        self.ev(self.t_prisa, "subida", 0.6, 0.0, dur=max(1.0, self.t_piensa - self.t_prisa))
        self.ev(self.t_piensa, "golpe_grave", 0.9, 0.0)
        self.ev(self.t_si, "multitud", 0.4, -0.3, dur=max(1.5, self.t_ia - self.t_si))
        self.ev(self.t_ia - 0.35, "sombra_crece", 0.6, 0.0, dur=2.5)
        self.ev(self.t_resto - 0.3, "periodico_golpe", 0.9, 0.3)
        for k in range(4):
            self.ev(self.t_manual + 0.18 * k, "ficha", 0.7, 0.5)
        self.ev(self.t_siglo - 0.3, "sello_golpe", 0.9, 0.2)
        self.ev(self.t1 - 0.8, "tinta_mancha", 0.6, 0.0, dur=0.9)
