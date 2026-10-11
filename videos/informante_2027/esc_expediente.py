# -*- coding: utf-8 -*-
"""Escena 7 «expediente»: primer plano de la máquina de escribir (las teclas saltan, la hoja sube renglón a renglón);
abril de 2025: los cinco autores bajo los focos y la carpeta «2027» que cae delante; la tira de hojas de calendario que corre
mes por mes bajo una curva que cruza el «nivel humano»; la torre de la empresa inventada, con su letrero de bombillas."""
import math

import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import noir as N
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from noir_pers import Frontal
from toon import Pista, elipse_, pulso, suave

MESES = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"]


class Expediente(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.dan = Frontal(sem=77)
        self.co = [Frontal(sem=500 + 13 * k) for k in range(4)]
        self.t_ya = w("Ya podía")
        self.t_escribio = w("escribió")
        self.t_abril = w("Abril")
        self.t_cuatro = w("cuatro")
        self.t_publico = w("publicó")
        self.t_titulo = w("Lo tituló")
        self.t_noes = w("No es")
        self.t_pron = w("pronóstico")
        self.t_mes = w("mes por mes")
        self.t_supere = w("supere")
        self.t_centro = w("En el centro")
        self.t_llaman = w("La llaman")
        self.t_open = w("OpenBrain")
        self.t_tu = w("Tú ponle")
        self.t_quieras = w("quieras")
        self.cam_t = Pista([(self.t_centro - 0.5, (1010, -900, 0.66)), (self.t_open, (1010, -1900, 0.9), "io"),
                            (self.t1 + 1, (1010, -1960, 0.96), "l")])
        self.plano(t0, self.p_maquina)
        self.plano(self.t_abril - 0.35, self.p_autores, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_noes - 0.35, self.p_meses, tr="empuje", dur=0.6, centro=(W * 0.5, H * 0.5))
        self.plano(self.t_centro - 0.4, self.p_torre, tr="relampago", dur=0.7)

    # ------------------------------------------------------------------ escribió
    def p_maquina(self, h, t, u):
        h.camara(1.0 + 0.02 * u, 960, 560 - 6 * u, 0.0)
        K.pared(h, 26, 8)
        # la hoja sube con cada renglón
        nl = int(max(0.0, t - self.t_ya) * 1.6)
        sube = nl * 54 + 54 * e_out(clamp01(((t - self.t_ya) * 1.6) % 1.0 / 0.2))
        hy = 430 - sube
        h.pieza(C.rect(520, hy - 500, 880, 1100), 228, 10, w=4, luz=(0.2, -1), d=8, trama=0, rim=0)
        N.texto_maquina(h, "CÓMO PODRÍA OCURRIR", 570, hy - 440, 52, t, self.t_ya, cps=14, tono=0.05, fuente=N.FUENTE_SELLO, encuadrar=False)
        r = np.random.default_rng(3)
        for k in range(14):
            tk = self.t_ya + 0.9 + k * 0.62
            a = clamp01((t - tk) / 0.55)
            if a > 0:
                K.plano_(h, C.rect(570, hy - 340 + k * 54, 760 * r.uniform(0.7, 1.0) * a, 9), 70, 20 + k)
        # el cuerpo de la máquina: rodillo, guía, cesta de tipos y teclado
        h.pieza(np.asarray(suave([(380, 560), (1540, 560), (1560, 600), (1540, 640), (380, 640), (360, 600)], 3)), 40, 40, w=6, luz=(0.2, -1),
                d=16, trama=0.5, rim=0.9)
        for q in (-1, 1):
            h.pieza(np.asarray(elipse_(960 + q * 640, 600, 46, 60, n=20)), 28, 41 + q, w=5, luz=(0.2, -1), d=10, trama=0.4, rim=0.9)
        K.plano_(h, C.rect(520, 548, 880, 16), 228, 44)
        h.pieza(np.array([[300, 640], [1620, 640], [1760, 1150], [160, 1150]]), 30, 45, w=7, luz=(0.2, -1), d=20, trama=0.6, rim=0.8)
        h.pieza(np.asarray(suave([(700, 650), (1220, 650), (1160, 760), (760, 760)], 3)), 14, 46, w=5, luz=(0.2, -1), d=8, trama=0.3, rim=0.6)
        golpe = int(t * 13)
        rk = np.random.default_rng(golpe)
        act = int(rk.integers(0, 40)) if t > self.t_ya else -1
        if act >= 0:                                                 # el tipo que salta a golpear el papel
            ax = 960 + (act % 10 - 4.5) * 44
            h.trazo(np.array([[ax, 740], [960 + (act % 10 - 4.5) * 8, 600]]), 5, 47, color=(170, 170, 170), jit=0.3, taper=(0, 0))
        for j in range(4):                                           # cuatro filas de teclas redondas
            for i in range(10):
                kx = 430 + i * 118 + j * 30 - j * 6
                ky = 820 + j * 78
                dn = 12 if (j * 10 + i) == act else 0
                h.pieza(np.asarray(elipse_(kx, ky + dn, 40, 26, n=18)), 190 - 14 * j, 60 + j * 10 + i, w=3.5, luz=(0.2, -1), d=6, trama=0.2,
                        rim=0.8, jit=0.5)
                h.trazo(np.array([[kx, ky + dn + 20], [kx, ky + 46]]), 5, 110 + j * 10 + i, color=(20, 20, 20), jit=0.2, taper=(0, 0))
        C.banda(h, "YA PODÍA HABLAR", 300, 150, 56, t, self.t_ya + 0.1, sem=5)
        C.banda(h, "ASÍ QUE ESCRIBIÓ", 300, 250, 56, t, self.t_escribio - 0.3, claro=True, sem=6)
        h.ambiente[:] = 0.34
        h.luz_cono(1100, -520, math.pi / 2 + 0.1, 0.6, 2300, (1.6, 1.6, 1.6), suave=0.5)
        N.motas(h, t, n=90, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.12, vel=8, y0=0, y1=1080, sube=False), bloom=0.4)

    # ------------------------------------------------------------------ cinco autores
    def p_autores(self, h, t, u):
        h.camara(1.0 + 0.014 * u, 960, 530, 0.0)
        MU.sala_rueda().pegar(h, 1.0, oscuro=0.6, dx=120)
        looks = [dict(pelo="rizado", traje=50), dict(pelo="oscuro", traje=92, gafas=True), None, dict(pelo="calvo", traje=58, barba=True),
                 dict(pelo="oscuro", traje=80)]
        s = 1.18
        j = 0
        for k in range(5):
            x = 400 + k * 280
            tk = self.t_cuatro - 0.6 + abs(k - 2) * 0.28
            on = smooth(clamp01((t - tk) / 0.3)) if k != 2 else 1.0
            if looks[k] is None:
                self.dan.dibujar(h, dict(x=x, y=960, s=s * 1.06, luz=(0.0, -1.0), rim=0.9, mira=0.2 * math.sin(t), **K.DAN))
            else:
                p = dict(looks[k])
                p.update(x=x, y=960, s=s, luz=(0.0, -1.0), rim=0.8, mira=0.5 * math.sin(t * 0.8 + k), cabeza=0.04 * math.sin(t + k))
                self.co[j].dibujar(h, p)
                j += 1
            h.luz_cono(x, -420, math.pi / 2, 0.15, 1900, (1.5, 1.5, 1.5), k=1.0 * on, suave=0.5)
        # la carpeta cae delante
        tc = self.t_publico - 0.1
        if t > tc:
            cae = e_out(clamp01((t - tc) / 0.4))
            K.carpeta(h, 960, 760 - 1100 * (1 - cae), 0.9, "2027", t, self.t_titulo + 0.5, ang=-0.04 + 0.3 * (1 - cae), sem=60, px=250)
        C.banda(h, "ABRIL DE 2025", 300, 110, 64, t, self.t_abril, sem=5)
        C.banda(h, "CINCO AUTORES", 300, 205, 44, t, self.t_cuatro, claro=True, sem=6)
        C.banda(h, "«AI 2027»", 1560, 150, 90, t, self.t_titulo + 0.5, claro=True, sem=7)
        h.ambiente[:] = 0.26
        N.motas(h, t, n=100, k=0.7)
        return h.acabado(t, niebla=dict(dens=0.18, vel=8, y0=-200, y1=1000, sube=False), bloom=0.45)

    # ------------------------------------------------------------------ mes por mes
    def p_meses(self, h, t, u):
        h.camara(1.0 + 0.01 * u, 960, 540, 0.0)
        K.pared(h, 44, 14, ladrillo=True)
        v = (t - self.t_noes) * 150 + 60 * max(0.0, t - self.t_mes) ** 1.6      # la tira corre cada vez más deprisa
        for k in range(36):                                          # ene-2025 .. dic-2027
            x = 400 + k * 300 - v
            if x < -200 or x > W + 200:
                continue
            anio = 2025 + k // 12
            oscuro = anio == 2027
            h.pieza(C.rect(x - 125, 660, 250, 300), 226, 100 + k, w=4, luz=(0.2, -1), d=8, trama=0, rim=0)
            K.plano_(h, C.rect(x - 125, 660, 250, 76), 14 if oscuro else 60, 140 + k)
            N.texto_maquina(h, str(anio), x, 698, 44, t, -99, cps=1e9, tono=0.95, centro=True, fuente=N.FUENTE_SELLO, encuadrar=False)
            N.texto_maquina(h, MESES[k % 12], x, 850, 100, t, -99, cps=1e9, tono=0.04, centro=True, fuente=N.FUENTE_SELLO, encuadrar=False)
        h.trazo(np.array([[-100, 650], [W + 100, 650]]), 10, 90, color=(20, 20, 20), jit=0.3, taper=(0, 0))       # el cordel
        # la curva y el nivel humano
        y_h = 330
        for q in range(24):
            h.trazo(np.array([[80 + q * 76, y_h], [80 + q * 76 + 40, y_h]]), 5, 180 + q, color=(210, 210, 210), jit=0.2, taper=(0, 0))
        C.banda(h, "NIVEL HUMANO", 300, y_h - 46, 36, t, self.t_pron, claro=True, sem=8)
        a = clamp01((t - self.t_pron) / max(1.5, self.t_supere - self.t_pron + 0.7))
        n = max(2, int(70 * a))
        xs = np.linspace(0, 1, 70)[:n]
        Q = np.stack([120 + 1700 * xs, 600 - 470 * xs ** 2.6], 1)
        h.trazo(Q, 12, 91, color=(240, 240, 240), jit=0.5, taper=(0.3, 0.0))
        h.emitir(elipse_(Q[-1][0], Q[-1][1], 16, 16, n=12), 1.0)
        h.luz_radial(Q[-1][0], Q[-1][1], 300, (1.0, 1.0, 1.0), k=0.9)
        C.banda(h, "NO ES UNA NOVELA", 960, 80, 54, t, self.t_noes + 0.1, sem=5)
        C.banda(h, "UN PRONÓSTICO, MES POR MES", 960, 1020, 50, t, self.t_mes - 0.2, claro=True, sem=6)
        C.banda(h, "NOS SUPERA EN TODO", 1500, 190, 50, t, self.t_supere, sem=7)
        h.ambiente[:] = 0.5
        h.luz_radial(960, 800, 1300, (1.0, 1.0, 1.0), k=0.8)
        N.motas(h, t, n=90, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.14, vel=10, y0=200, y1=1080, sube=False), bloom=0.45)

    # ------------------------------------------------------------------ una empresa inventada
    def p_torre(self, h, t, u):
        cx, cy, z = self.cam_t(t)
        h.camara(z, cx, cy, 0.012 * math.sin(t * 0.3))
        MU.cielo().pegar(h, 0.05, dx=-(t * 6.0) % 300)
        MU.lejos().pegar(h, 0.3, bruma=0.55, tono_bruma=0.36)
        MU.medio().pegar(h, 0.6, bruma=0.2, tono_bruma=0.36)
        h.ambiente[:] = 1.15
        fl = max(N.relampago(t, [self.t_centro - 0.2, self.t_tu + 0.3]), 0.0)
        h.ambiente[:] += 1.1 * fl
        duda = t > self.t_tu and int(t * 9) % 3 == 0                 # «ponle el nombre que quieras»: el letrero titubea
        s_ = "?????????" if duda else "OPENBRAIN"
        with h.capa(0.6):                                           # el letrero de bombillas sobre la corona de la torre
            x0, y0, an, al = 760, -1300, 460, 120
            h.pieza(C.rect(x0, y0, an, al), 14, 40, w=5, luz=(0, -1), d=6, trama=0.2, rim=0.6)
            for q in (0.2, 0.8):
                h.trazo(np.array([[x0 + an * q, y0 + al], [x0 + an * q, y0 + al + 80]]), 8, 41 + int(q * 10), color=(20, 20, 20), jit=0.2)
            enc = smooth(clamp01((t - self.t_llaman) / 0.4))
            if enc > 0:
                N.texto_maquina(h, s_, x0 + an / 2, y0 + al / 2, 78, t, -99, cps=1e9, tono=0.97, centro=True, fuente=K.IMPACT, track=4.0,
                                encuadrar=False)
                h.luz_fija(C.rect(x0, y0, an, al), 0.9 * enc)
                h.luz_radial(x0 + an / 2, y0 + al / 2, 520, (1.0, 1.0, 1.0), k=1.3 * enc)
                for q in range(16):                                  # bombillas del borde, en carrera
                    on = (q + int(t * 8)) % 3 != 0
                    bx = x0 + 14 + q * (an - 28) / 15
                    for by in (y0 + 8, y0 + al - 8):
                        if on:
                            h.emitir(elipse_(bx, by, 5, 5, n=8), 0.9 * enc, blur=1.5)
        N.lluvia(h, t, n=700, vel=1700)
        h.camara(1.0, W / 2, H / 2, 0.0)
        C.banda(h, "UNA EMPRESA INVENTADA", 420, 900, 54, t, self.t_centro + 0.3, sem=5)
        C.banda(h, "PONLE EL NOMBRE QUE QUIERAS", 1440, 1000, 46, t, self.t_tu, claro=True, sem=6)
        return h.acabado(t, niebla=dict(dens=0.26, y0=200, y1=1000, vel=30), flash=0.3 * fl, bloom=0.55)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        t0 = self.t0
        self.ev(self.t_ya, "tecleo_rapido", 0.6, 0.0, dur=self.t_abril - self.t_ya - 0.4)
        for k in range(int((self.t_abril - self.t_ya) / 0.62)):
            self.ev(self.t_ya + 0.62 * (k + 1), "carro_maquina", 0.4, 0.3)
        self.ev(self.t_abril - 0.35, "barrido_aire", 0.6, 0.0, dur=0.7)
        self.ev(self.t_abril, "sello_golpe", 0.8, -0.3)
        for k in range(3):
            self.ev(self.t_cuatro - 0.6 + k * 0.28, "focos", 0.6, -0.4 + 0.4 * k)
        self.ev(self.t_publico + 0.3, "periodico_golpe", 0.9, 0.0)
        self.ev(self.t_titulo + 0.5, "sello_golpe", 1.0, 0.0)
        self.ev(self.t_noes - 0.35, "barrido_aire", 0.6, 0.0, dur=0.7)
        self.ev(self.t_noes, "paginas", 0.6, 0.0)
        self.ev(self.t_mes, "papel_viento", 0.6, 0.0, dur=3.0)
        self.ev(self.t_pron, "subida", 0.6, 0.2, dur=max(1.5, self.t_supere - self.t_pron))
        self.ev(self.t_supere, "golpe_grave", 0.9, 0.0)
        self.ev(self.t_centro - 0.4, "lluvia_amb", 0.8, 0.0, dur=self.t1 - self.t_centro + 0.4)
        self.ev(self.t_centro - 0.2, "trueno_noir", 0.8, 0.2, dur=4.0)
        self.ev(self.t_llaman, "lampara_chisporrotea", 0.7, 0.0, dur=1.0)
        self.ev(self.t_open, "sello_golpe", 0.9, 0.0)
        self.ev(self.t_tu + 0.3, "electricidad", 0.6, 0.0, dur=1.2)
        self.ev(self.t1 - 0.8, "tinta_mancha", 0.6, 0.0, dur=0.9)
