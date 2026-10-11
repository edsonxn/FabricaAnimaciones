# -*- coding: utf-8 -*-
"""Escena 11 «afuera»: el detective camina bajo la lluvia por la avenida (casi nada se ve); la fachada de la bolsa con la
cotización que trepa y, en primer término, la mano con el teléfono; la fila de programadores jóvenes ante la puerta donde el
cartel de vacante queda tachado; la multitud con pancartas frente al Capitolio; la puerta cerrada con luz por debajo y el
autobús que pasa (caben más personas ahí que las que saben)."""
import math

import numpy as np

import comun as C
import kit27 as K
import mundos as MU
import mundos27 as M27
import noir as N
import props as PR
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from noir_pers import Detective, avance_paso
from toon import Pista, elipse_, pulso, suave


def autobus(h, x, y, s=1.0, t=0.0, sem=0):
    """Autobús urbano de perfil (y = suelo), con las cabezas de los pasajeros en las ventanillas."""
    def T(P):
        return np.asarray(P, float) * s + (x, y)
    h.pieza(T(suave([(-520, -60), (-520, -330), (-480, -380), (480, -380), (520, -330), (520, -60)], 3)), 60, sem, w=7 * s, luz=(0.2, -1),
            d=18 * s, trama=0.6, rim=0.8)
    for k in range(9):
        v = T(C.rect(-480 + k * 108, -340, 88, 120))
        K.plano_(h, v, 200, sem + 1 + k)
        h.emitir(v, 0.45)
        hx = -436 + k * 108 + 6 * math.sin(t * 2 + k)
        K.plano_(h, T(elipse_(hx, -250, 24, 30, n=14)), 14, sem + 20 + k)
        K.plano_(h, T(C.rect(hx - 34, -224, 68, 14)), 14, sem + 40 + k)
    h.trazo(T([(-520, -200), (520, -200)]), 6 * s, sem + 60, alfa=0.7, jit=0.3)
    for q in (-330, 330):
        c = T([(q, -50)])[0]
        h.pieza(elipse_(c[0], c[1], 62 * s, 62 * s, n=28), 14, sem + 61 + q, w=6 * s, luz=(0.2, -1), d=8 * s, trama=0.2, rim=0.8)
        h.pieza(elipse_(c[0], c[1], 24 * s, 24 * s, n=16), 150, sem + 62 + q, w=3 * s, luz=(0.2, -1), d=3, trama=0, rim=0.5)
        a = t * 3.0
        h.trazo(np.array([[c[0] - 50 * s * math.cos(a), c[1] - 50 * s * math.sin(a)], [c[0] + 50 * s * math.cos(a), c[1] + 50 * s * math.sin(a)]]),
                4 * s, sem + 63 + q, color=(90, 90, 90), jit=0.2, taper=(0, 0))
    f = T([(520, -120)])[0]
    h.emitir(elipse_(f[0], f[1], 16 * s, 12 * s, n=10), 1.2)
    h.luz_cono(f[0], f[1], 0.05, 0.22, 700 * s, (1.4, 1.4, 1.4), k=0.9, suave=0.6)


class Afuera(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.det = Detective(sem=3)
        self.t_afuera = w("afuera")
        self.t_quese = w("qué se ve")
        self.t_casi = w("Casi nada")
        self.t_bolsa = w("La bolsa")
        self.t_sube = w("sube")
        self.t_asist = w("Los asistentes")
        self.t_listos = w("listos")
        self.t_prog = w("Y los programadores")
        self.t_trabajo = w("trabajo")
        self.t_prot = w("Hay protestas")
        self.t_cap = w("Capitolio")
        self.t_pero = w("Pero la gente")
        self.t_nadie = w("Nadie sabe")
        self.t_edif = w("edificio")
        self.t_lomas = w("Lo más")
        self.t_puerta = w("puerta cerrada")
        self.t_ylo = w("Y lo saben")
        self.t_bus = w("autobús")
        self.plano(t0, self.p_calle)
        self.plano(self.t_bolsa - 0.35, self.p_bolsa, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_prog - 0.35, self.p_fila, tr="barrido", dur=0.55, dirx=1)
        self.plano(self.t_prot - 0.35, self.p_capitolio, tr="relampago", dur=0.6)
        self.plano(self.t_lomas - 0.35, self.p_cerrada, tr="humo", dur=0.7)

    def _ciudad(self, h, t, cx, cy, z):
        h.camara(z, cx, cy, 0.006 * math.sin(t * 0.4))
        MU.cielo().pegar(h, 0.05, dx=-(t * 6.0) % 300)
        MU.lejos().pegar(h, 0.3, bruma=0.55, tono_bruma=0.36)
        MU.medio().pegar(h, 0.6, bruma=0.2, tono_bruma=0.36)
        MU.calle().pegar(h, 1.0)

    # ------------------------------------------------------------------ en la calle, casi nada
    def p_calle(self, h, t, u):
        self._ciudad(h, t, 1500 + 40 * u, 640, 0.92)
        vel = 2.9 * avance_paso(Detective.ZANCADA, 0.95)            # px/s: la fase sale de lo que avanza (los pies no patinan)
        x = 1000 + vel * u
        p = dict(x=x, y=935.0, s=0.95, d=1, luz=(-0.3, -1.0), fumar=0.0, giro=0.2, paso=2.9 * u, andar=1.0, viento=0.5, hombros=0.2)
        self.det.dibujar(h, p)
        h.ambiente[:] = 0.8
        h.luz_cono(1080, 430, math.pi / 2, 0.5, 700, (1.6, 1.6, 1.6), k=1.1, suave=0.5)
        h.luz_radial(1080, 440, 320, (1.0, 1.0, 1.0), k=1.2)
        N.lluvia(h, t, n=700, vel=1700)
        N.salpicaduras(h, t, 960, 1220, x0=700, x1=2400, n=60)
        h.camara(1.0, W / 2, H / 2, 0.0)
        C.banda(h, "AFUERA, EN LA CALLE", 420, 120, 60, t, self.t_afuera, sem=5)
        C.banda(h, "CASI NADA", 1400, 200, 110, t, self.t_casi, claro=True, sem=6)
        img = h.acabado(t, niebla=dict(dens=0.26, y0=300, y1=1080, vel=30), bloom=0.5)
        return N.reflejo(img, 1000, k=0.3, t=t)

    # ------------------------------------------------------------------ la bolsa sube; los teléfonos, más listos
    def p_bolsa(self, h, t, u):
        self._ciudad(h, t, 3420 + 10 * u, 520, 0.80 + 0.01 * u)
        # la cotización trepa por delante de la fachada (trazo de luz)
        a = clamp01((t - self.t_bolsa + 0.2) / 2.2)
        r = np.random.default_rng(5)
        xs = np.linspace(2760, 4080, 40)
        ys = 760 - np.linspace(0, 1, 40) ** 1.5 * 760 + np.cumsum(r.uniform(-26, 26, 40))
        n = max(2, int(40 * a))
        h.trazo(np.stack([xs[:n], ys[:n]], 1), 12, 60, color=(245, 245, 245), jit=0.5, taper=(0.1, 0.0))
        h.emitir(elipse_(xs[n - 1], ys[n - 1], 18, 18, n=12), 1.2)
        h.luz_radial(xs[n - 1], ys[n - 1], 420, (1.0, 1.0, 1.0), k=1.0)
        h.ambiente[:] = 0.9
        h.luz_radial(3420, 600, 1500, (1.0, 1.0, 1.0), k=0.7)
        N.lluvia(h, t, n=600, vel=1700)
        h.camara(1.0, W / 2, H / 2, 0.0)
        # en primer término: la mano con el teléfono
        e = e_out(clamp01((t - self.t_asist + 0.4) / 0.5))
        if e > 0:
            mx, my = 420, 1500 - 760 * e
            PR.mano(h, mx - 40, my + 260, 1.5, ang=-1.25, d=1, sem=80, dedos=0.0)
            tel = np.asarray(suave([(mx - 150, my - 250), (mx + 150, my - 250), (mx + 150, my + 330), (mx - 150, my + 330)], 2))
            h.pieza(tel, 16, 90, w=6, luz=(0, -1), d=10, trama=0.2, rim=0.9)
            pant = C.rect(mx - 130, my - 220, 260, 500)
            K.plano_(h, pant, 210, 91)
            h.luz_fija(pant, 0.9)
            h.emitir(pant, 0.25, blur=8)
            for k, (s_, tk) in enumerate((("¿En qué te ayudo?", self.t_asist), ("Hecho.", self.t_asist + 0.9), ("Ya lo resolví.", self.t_listos))):
                if t > tk:
                    K.plano_(h, C.rect(mx - 116, my - 190 + k * 110, 232, 80), 60 if k % 2 == 0 else 150, 92 + k)
                    N.texto_maquina(h, s_, mx - 104, my - 172 + k * 110, 24, t, tk, cps=40, tono=0.96 if k % 2 == 0 else 0.05, encuadrar=False)
        C.banda(h, "LA BOLSA SUBE", 1380, 120, 80, t, self.t_sube - 0.2, sem=5)
        C.banda(h, "ASISTENTES CADA VEZ MÁS LISTOS", 1300, 1000, 46, t, self.t_listos - 0.6, claro=True, sem=6)
        return h.acabado(t, niebla=dict(dens=0.22, y0=300, y1=1080, vel=30), bloom=0.5)

    # ------------------------------------------------------------------ los programadores jóvenes
    def p_fila(self, h, t, u):
        h.camara(1.0 + 0.014 * u, 960 + 8 * u, 540, 0.0)
        K.pared(h, 52, 18, ladrillo=True)
        K.plano_(h, C.rect(-300, 950, W + 600, 400), 44, 8, grad=(12, 950, 1200))
        K.puerta(h, 1420, 190, 380, 760, sem=20, tono=30, vidrio="PERSONAL", t=t)
        h.pieza(C.rect(960, 260, 400, 250), 226, 40, w=5, luz=(0.2, -1), d=8, trama=0, rim=0)          # el cartel de la vacante
        N.texto_maquina(h, "SE BUSCA", 1160, 320, 54, t, -99, cps=1e9, tono=0.05, centro=True, fuente=K.IMPACT, encuadrar=False)
        N.texto_maquina(h, "PROGRAMADOR", 1160, 400, 50, t, -99, cps=1e9, tono=0.05, centro=True, fuente=K.IMPACT, encuadrar=False)
        N.texto_maquina(h, "JUNIOR", 1160, 466, 40, t, -99, cps=1e9, tono=0.2, centro=True, fuente=K.IMPACT, encuadrar=False)
        ta = clamp01((t - self.t_trabajo + 0.5) / 0.3)
        if ta > 0:
            for q in (0, 1):
                a0 = np.array([980, 280 if q == 0 else 490])
                a1 = np.array([1340, 490 if q == 0 else 280])
                h.trazo(np.array([a0, a0 + (a1 - a0) * ta]), 20, 50 + q, color=(12, 12, 12), jit=0.7, taper=(0.1, 0.1))
        N.sello(h, "PUESTO CUBIERTO POR IA", 1160, 600, 54, t, self.t_trabajo, rot=-6, tono=0.04, alfa=0.95)
        for k in range(5):                                           # la fila: jóvenes con su carpeta, que cambian el peso de pie
            x = 180 + k * 190
            man = K.caminante(h, x, 1010, 0.98 + 0.05 * math.sin(k * 2.1), fase=0.25 * math.sin(t * 1.1 + k * 1.7), sem=100 + k * 30,
                              tono=60 + 12 * (k % 3), luz=(0.8, -0.6), rim=0.9, carga=True, barba=(k % 2 == 0), pelo=20 + 14 * (k % 3),
                              andar=0.35)
            h.pieza(C.rect(man[0] - 10, man[1] - 40, 70, 90), 205, 300 + k, w=3, luz=(0.2, -1), d=4, trama=0, rim=0.4)
        C.banda(h, "LOS JÓVENES DEJAN DE ENCONTRAR TRABAJO", 660, 110, 44, t, self.t_prog + 0.3, sem=5)
        h.ambiente[:] = 0.42
        h.luz_cono(1160, -300, math.pi / 2, 0.4, 1700, (1.5, 1.5, 1.5), suave=0.5)
        h.luz_radial(560, 700, 1100, (1.0, 1.0, 1.0), k=0.7)
        N.motas(h, t, n=90, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.18, vel=10, y0=200, y1=1080, sube=False), bloom=0.45)

    # ------------------------------------------------------------------ protestas frente al Capitolio
    def p_capitolio(self, h, t, u):
        den = smooth(clamp01((t - self.t_nadie + 0.3) / 1.6))           # «nadie sabe lo que pasa dentro»: empuje a las ventanas
        h.camara(1.0 + 0.012 * u + 0.5 * den, 960, 560 - 260 * den, 0.0)
        M27.capitolio().pegar(h, 1.0)
        K.multitud(h, t, -100, 2020, 1120, 30, 0.95, 5, carteles=("EMPLEOS", "¿Y NOSOTROS?", "TRABAJO", "PAREN LA IA"), ritmo=1.2, filas=3)
        fl = max(N.relampago(t, [self.t_prot + 0.2]), 0.0)
        h.ambiente[:] = 0.78 + 0.9 * fl
        N.lluvia(h, t, n=500, vel=1700, k=0.8)
        h.camara(1.0, W / 2, H / 2, 0.0)
        C.banda(h, "PROTESTAS FRENTE AL CAPITOLIO", 480, 90, 50, t, self.t_cap - 0.6, sem=5)
        C.banda(h, "PROTESTAN POR LOS EMPLEOS", 1420, 90, 50, t, self.t_pero + 0.5, claro=True, sem=6)
        C.banda(h, "NADIE SABE LO QUE PASA DENTRO", 960, 1000, 60, t, self.t_nadie + 0.3, sem=7)
        return h.acabado(t, niebla=dict(dens=0.2, y0=300, y1=1080, vel=24), bloom=0.55, flash=0.3 * fl)

    # ------------------------------------------------------------------ a puerta cerrada
    def p_cerrada(self, h, t, u):
        h.camara(1.0 + 0.012 * u, 960 + 6 * u, 560, 0.0)
        K.pared(h, 50, 16, ladrillo=True)
        K.plano_(h, C.rect(-300, 930, W + 600, 400), 44, 8, grad=(12, 930, 1200))
        K.puerta(h, 260, 170, 400, 760, sem=20, tono=28, rendija=0.6 + 0.4 * math.sin(t * 2.3) ** 2, vidrio="PRIVADO", t=t)
        for q in range(3):                                           # sombras de pies que pasan por la rendija
            fx = 300 + ((t * 60 + q * 150) % 330)
            K.plano_(h, C.rect(fx, 918, 40, 16), 6, 40 + q, alfa=0.9)
        av = e_out(clamp01((t - self.t_lomas - 0.8) / 4.0))
        autobus(h, 2700 - 1450 * av, 1040, 1.0, t, sem=100)
        C.banda(h, "A PUERTA CERRADA", 460, 90, 60, t, self.t_puerta, sem=5)
        C.banda(h, "LO SABEN MENOS PERSONAS DE LAS QUE CABEN AQUÍ", 1250, 560, 40, t, self.t_bus - 0.6, claro=True, sem=6)
        h.ambiente[:] = 0.5
        h.luz_cono(460, -400, math.pi / 2, 0.3, 1500, (1.2, 1.2, 1.2), k=0.9, suave=0.5)
        h.luz_radial(1300, 700, 1300, (1.0, 1.0, 1.0), k=0.9)
        N.lluvia(h, t, n=300, vel=1700, k=0.6)
        return h.acabado(t, niebla=dict(dens=0.2, vel=14, y0=300, y1=1080, sube=False), bloom=0.5)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        t0 = self.t0
        self.ev(t0, "lluvia_amb", 0.8, 0.0, dur=self.t_prog - t0)
        for k in range(8):
            self.ev(t0 + 0.6 + k * 0.7, "pasos_mojados", 0.5, -0.3 + 0.08 * k)
        self.ev(self.t_casi, "sello_golpe", 0.9, 0.3)
        self.ev(self.t_bolsa - 0.35, "barrido_aire", 0.6, 0.0, dur=0.7)
        self.ev(self.t_bolsa, "campana_bolsa", 0.8, 0.2)
        self.ev(self.t_bolsa, "subida", 0.6, 0.2, dur=2.2)
        self.ev(self.t_asist, "datos", 0.5, -0.5, dur=2.0)
        self.ev(self.t_prog - 0.35, "barrido_aire", 0.6, 0.0, dur=0.6)
        self.ev(self.t_trabajo - 0.5, "tachon", 1.0, 0.2)
        self.ev(self.t_trabajo, "sello_golpe", 1.0, 0.2)
        self.ev(self.t_prot - 0.35, "relampago_corto", 0.6, 0.0)
        self.ev(self.t_prot, "multitud", 0.9, 0.0, dur=self.t_lomas - self.t_prot)
        self.ev(self.t_prot, "lluvia_amb", 0.6, 0.0, dur=self.t1 - self.t_prot)
        self.ev(self.t_prot + 0.2, "trueno_noir", 0.8, 0.0, dur=4.0)
        self.ev(self.t_nadie + 0.3, "golpe_grave", 0.9, 0.0)
        self.ev(self.t_puerta, "puerta", 0.9, -0.5)
        self.ev(self.t_lomas + 0.8, "auto_pasa", 0.8, 0.4, dur=4.0)
        self.ev(self.t1 - 0.8, "tinta_mancha", 0.6, 0.0, dur=0.9)
