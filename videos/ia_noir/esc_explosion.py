# -*- coding: utf-8 -*-
"""Escena 7 «explosion»: la sombra de la caja crece en la pared (la que viene después) · brazo robótico real y el PLANO que se redibuja
cada vez más grande y complejo · zoom infinito de cajas dentro de cajas con engranajes que aceleran · 1965: el artículo de I. J. Good a
máquina y la curva que explota en papel milimetrado · la cita del «último invento»."""
import math

import numpy as np

import mundos as MU
import noir as N
import props as PR
from basen import BaseNoir
from motor import H, W, clamp01, e_inout, e_out, smooth
from noir import gris
from toon import Pista, elipse_, pulso


def plano_caja(h, cx, cy, esc, u, sem=0, nivel=0):
    """Plano técnico (líneas blancas sobre azul-gris de cianotipo) de la caja; u = cuánto se ha trazado; más nivel = más detalle."""
    w_, a_ = 230 * esc, 520 * esc
    lineas = [((-1, -1), (1, -1)), ((1, -1), (1, 1)), ((1, 1), (-1, 1)), ((-1, 1), (-1, -1))]
    for k in range(4 + 3 * nivel):
        y = -1 + 2 * (k + 1) / (5 + 3 * nivel)
        lineas.append(((-0.75, y), (0.75, y)))
    for k in range(nivel * 2):
        x = -0.6 + 1.2 * k / max(1, nivel * 2 - 1)
        lineas.append(((x, -0.85), (x, 0.85)))
    n = len(lineas)
    for i, (a, b) in enumerate(lineas):
        k = clamp01(u * n - i)
        if k <= 0:
            break
        A = np.array([cx + a[0] * w_ / 2, cy + a[1] * a_ / 2])
        B = np.array([cx + b[0] * w_ / 2, cy + b[1] * a_ / 2])
        h.trazo(np.array([A, A + (B - A) * k]), 3 + 1.5 * esc, sem + i, color=gris(230), jit=0.5)
    if u > 0.6:                                             # cotas
        h.trazo(np.array([[cx - w_ / 2, cy + a_ / 2 + 30], [cx + w_ / 2, cy + a_ / 2 + 30]]), 2, sem + 99, color=gris(200))
        N.texto_maquina(h, f"v{nivel + 1}.0", cx, cy + a_ / 2 + 60, 24 + 8 * esc, h.t, -99, cps=1e9, tono=0.9, centro=True)


class Explosion(BaseNoir):
    TR_SALIDA = ("tinta", 0.8)

    def armar(self):
        w = self.w
        self.t_miedo = w("verdadero miedo")
        self.t_hoy = w("hoy")
        self.t_despues = w("después")
        self.t_una = w("Una inteligencia")
        self.t_diseno = w("diseño")
        self.t_version = w("versión")
        self.t_esa = w("Y esa")
        self.t_otra = w("Y luego otra")
        self.t_rapido = w("rápido")
        self.t_1965 = w("mil novecientos")
        self.t_good = w("Irving")
        self.t_expl = w("explosión")
        self.t_escribio = w("Y escribió")
        self.t_ultimo = w("último")
        self.t_hacer = w("hacer", fin=True)
        self.plano(self.t0, self.p_sombra)
        self.plano(self.t_una - 0.3, self.p_robot, tr="barrido", dur=0.45, dirx=1)
        self.plano(self.t_diseno + 0.3, self.p_planos, tr="empuje", dur=0.5)
        self.plano(self.t_esa - 0.3, self.p_droste, tr="empuje", dur=0.45)
        self.plano(self.t_1965 - 0.3, self.p_1965, tr="relampago", dur=0.35)
        self.plano(self.t_expl - 0.3, self.p_curva, tr="barrido", dur=0.45, dirx=1)
        self.plano(self.t_escribio - 0.3, self.p_cita, tr="humo", dur=0.6)

    # ------------------------------------------------------------------ la sombra que crece
    def p_sombra(self, h, t, u):
        h.camara(1.05 - 0.2 * smooth(clamp01(u / 5)), 900, 420 - 80 * smooth(clamp01(u / 5)), 0.0)
        MU.sala_interrogatorio().pegar(h, 1.0, oscuro=1.0)
        g = 1.0 + 2.6 * smooth(clamp01((t - self.t_hoy) / 2.8))
        h.silueta = ((6, 6, 6), 0.92)
        cx, base = 900, 900
        ww, aa = 230 * 1.25 * g, 520 * 1.25 * g
        h.pieza(PR.rect(cx - ww / 2 + 120, base - aa, ww, aa), 0, 3, w=0, luz=(0, -1), d=1, linea=False)
        h.silueta = None
        PR.caja_negra(h, cx - 40, 900, s=0.8, led=1.0, t=t, sem=11)
        h.ambiente[:] = 0.22
        lx = 1300 - 200 * (g - 1) / 2.6
        h.luz_cono(lx, 880, math.atan2(-600, -400), 0.9, 2600, (2.4, 2.4, 2.4), suave=0.4)
        h.emitir(elipse_(lx, 880, 18, 18, n=12), 1.4)
        return h.acabado(t, niebla=dict(dens=0.2, vel=12, y0=-400, y1=700, sube=False))

    # ------------------------------------------------------------------ brazo robótico (video real)
    def p_robot(self, h, t, u):
        N.clip_noir(h, "robot_1", t, self.t_una - 0.3, inicio=1.0, z0=1.0, z1=1.18, dur=3.5, tinta=0.6, poster=0.4, expo=0.95)
        h.ambiente[:] = 1.0
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ planos que se redibujan
    def p_planos(self, h, t, u):
        h.camara(1.0 + 0.06 * u, W / 2, H / 2, 0.0)
        h.img[:] = 0.26
        for k in range(0, W, 40):                           # cuadrícula del cianotipo
            h.trazo(np.array([[k, 0], [k, H]]), 1.2, 700 + k, color=gris(150), alfa=0.25, tf=False)
        for k in range(0, H, 40):
            h.trazo(np.array([[0, k], [W, k]]), 1.2, 800 + k, color=gris(150), alfa=0.25, tf=False)
        plano_caja(h, 520, 560, 0.9, clamp01(u / 1.2), sem=10, nivel=0)
        if t > self.t_version - 0.2:
            plano_caja(h, 1250, 520, 1.35, clamp01((t - self.t_version + 0.2) / 1.4), sem=60, nivel=2)
            k = smooth(clamp01((t - self.t_version) / 0.6))
            h.trazo(np.array([[700, 560], [700 + 260 * k, 540]]), 8, 40, color=gris(235), taper=(0.1, 0.0))
        h.ambiente[:] = 0.75
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ cajas dentro de cajas, cada vez más rápido
    def p_droste(self, h, t, u):
        N.clip_noir(h, "engranajes_4", t, self.t_esa - 0.3, inicio=0.0, vel=1 + 3 * clamp01(u / 5), z0=1.1, z1=1.5, dur=5.2, tinta=0.5,
                    poster=0.3, trama=0.2, expo=0.55)
        h.camara(1.0, W / 2, H / 2, 0.0)
        # zoom exponencial: cada caja contiene otra más grande que sale hacia nosotros
        vel = 0.35 + 1.4 * clamp01(u / 4.5) ** 2
        fase = (u * 0.35 + 0.5 * vel * u) % 1.0
        for n in range(6):
            z = 0.12 * (2.2 ** (n + fase))
            if z > 6:
                continue
            ww, aa = 230 * z, 520 * z
            a = clamp01(1.6 - z / 4)
            h.anillo(PR.rect(W / 2 - ww / 2, H / 2 - aa / 2, ww, aa), 3 + 3 * z, 30 + n, color=(240, 240, 240), alfa=a, jit=0.8)
            led = np.array([W / 2 + ww / 2 - 36 * z * 0.6, H / 2 - aa / 2 + 34 * z * 0.6])
            h.emitir(elipse_(led[0], led[1], 5 * z, 5 * z, n=10), 1.2 * a)
        N.sello(h, "×2", W / 2 + 520, 300, 120, t, self.t_esa + 0.3, rot=-8, tono=0.97, marco=False)
        N.sello(h, "×4", W / 2 - 560, 760, 120, t, self.t_otra, rot=6, tono=0.97, marco=False)
        N.sello(h, "×1000", W / 2 + 480, 820, 130, t, self.t_rapido - 0.2, rot=-4, tono=0.97, marco=False)
        h.ambiente[:] = 1.0
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ 1965
    def p_1965(self, h, t, u):
        h.camara(1.0 + 0.05 * u, W / 2, H / 2, -0.02)
        MU.escritorio().pegar(h, 1.0)
        h.pieza(PR.rect(500, 120, 900, 860), 222, 3, w=3, luz=(0.2, -1), d=10, trama=0, rim=0)
        N.texto_maquina(h, "SPECULATIONS CONCERNING", W / 2 - 10, 230, 42, t, self.t_1965, cps=40, tono=0.05, centro=True)
        N.texto_maquina(h, "THE FIRST ULTRAINTELLIGENT", W / 2 - 10, 290, 42, t, self.t_1965 + 0.6, cps=40, tono=0.05, centro=True)
        N.texto_maquina(h, "MACHINE", W / 2 - 10, 350, 42, t, self.t_1965 + 1.3, cps=40, tono=0.05, centro=True)
        N.texto_maquina(h, "I. J. Good  ·  1965", W / 2 - 10, 450, 34, t, self.t_good, cps=30, tono=0.15, centro=True)
        for k in range(10):
            h.pieza(PR.rect(580, 540 + k * 36, 740 * (0.8 + 0.2 * ((k * 7) % 3) / 2), 9), 120, 30 + k, w=0, luz=(0, -1), d=1, sombra=0,
                    trama=0, rim=0, linea=False, alfa=0.7)
        # calendario de escritorio
        h.pieza(PR.rect(1500, 160, 300, 340), 225, 50, w=4, luz=(0.2, -1), d=8, trama=0, rim=0)
        h.pieza(PR.rect(1500, 160, 300, 70), 30, 51, w=4, luz=(0.2, -1), d=4, trama=0, rim=0.5)
        N.texto_maquina(h, "1965", 1650, 360, 110, t, -99, cps=1e9, tono=0.05, centro=True, fuente=N.FUENTE_SELLO)
        h.ambiente[:] = 0.45
        h.luz_radial(W / 2, H / 2 - 100, 1100, (1.2, 1.2, 1.2))
        N.humo(h, t, W / 2 + 700, H / 2 - 300, k=0.6, ancho=1.5, viento=(-20, -60))
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ la curva que explota
    def p_curva(self, h, t, u):
        h.camara(1.0 + 0.1 * smooth(clamp01(u / 3)), W / 2, H / 2, 0.0)
        h.img[:] = 0.82
        for k in range(0, W, 48):
            h.trazo(np.array([[k, 0], [k, H]]), 1.0 if k % 240 else 2.0, 900 + k, color=gris(120), alfa=0.4, tf=False)
        for k in range(0, H, 48):
            h.trazo(np.array([[0, k], [W, k]]), 1.0 if k % 240 else 2.0, 1000 + k, color=gris(120), alfa=0.4, tf=False)
        x0, y0 = 220, 960
        h.trazo(np.array([[x0, y0], [W - 120, y0]]), 5, 1, color=gris(10))
        h.trazo(np.array([[x0, y0], [x0, 60]]), 5, 2, color=gris(10))
        N.texto_maquina(h, "tiempo", W - 300, y0 + 20, 34, t, -99, cps=1e9, tono=0.1)
        N.texto_maquina(h, "inteligencia", x0 + 20, 70, 34, t, -99, cps=1e9, tono=0.1)
        N.texto_maquina(h, "humanos", W - 420, 820, 32, t, -99, cps=1e9, tono=0.3)
        h.trazo(np.array([[x0, 840], [W - 140, 830]]), 3, 3, color=gris(90), alfa=0.8)
        k = clamp01((t - self.t_expl + 0.2) / 1.8)
        xs = np.linspace(0, 1, 120)[: max(2, int(120 * k))]
        ys = np.exp(xs * 6.0) / math.exp(6.0)
        P = np.stack([x0 + xs * (W - 380), y0 - 20 - ys * 900], 1)
        h.trazo(P, 9, 4, color=gris(8), taper=(0.0, 0.2), jit=0.6)
        N.sello(h, "EXPLOSIÓN DE INTELIGENCIA", 800, 380, 84, t, self.t_expl + 0.6, rot=-7, tono=0.05)
        h.ambiente[:] = 0.75
        h.luz_radial(W / 2, H / 2, 1300, (0.6, 0.6, 0.6))
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ el último invento
    def p_cita(self, h, t, u):
        h.camara(1.0 + 0.05 * u, W / 2, H / 2, 0.0)
        h.img[:] = 0.06
        tx = self.t_escribio + 0.2
        lineas = ["«La primera máquina ultrainteligente", "será el último invento que el hombre", "necesitará hacer.»"]
        for k, s in enumerate(lineas):
            N.texto_maquina(h, s, W / 2, 300 + k * 90, 56, t, tx + 1.3 * k, cps=30, tono=0.94, centro=True)
        N.texto_maquina(h, "— I. J. Good, 1965", W / 2 + 300, 650, 36, t, tx + 3.6, cps=30, tono=0.6, centro=True)
        N.sello(h, "ÚLTIMO INVENTO", W / 2, 900, 96, t, self.t_ultimo, rot=-4, tono=0.94)
        h.ambiente[:] = 0.6
        h.luz_radial(W / 2, 450, 900, (1.0, 1.0, 1.0))
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        self.ev(self.t0, "grave_inquietante", 0.7, 0.0, dur=self.t_una - self.t0)
        self.ev(self.t_hoy, "sombra_crece", 0.8, 0.0, dur=2.8)
        self.ev(self.t_una - 0.3, "servo", 0.8, 0.3, dur=2.0)
        self.ev(self.t_diseno + 0.3, "lapiz", 0.6, -0.3, dur=1.4)
        self.ev(self.t_version, "lapiz", 0.7, 0.3, dur=1.6)
        self.ev(self.t_esa - 0.3, "engranajes", 0.8, 0.0, dur=self.t_1965 - self.t_esa)
        for tk in (self.t_esa + 0.3, self.t_otra, self.t_rapido - 0.2):
            self.ev(tk, "golpe_grave", 0.9, 0.0)
        self.ev(self.t_rapido, "subida", 0.8, 0.0, dur=0.9)
        self.ev(self.t_1965 - 0.3, "relampago_corto", 0.5, 0.0)
        for k, s in enumerate(("SPECULATIONS CONCERNING", "THE FIRST ULTRAINTELLIGENT", "MACHINE")):
            for i in range(len(s)):
                self.ev(self.t_1965 + 0.6 * k + (0.1 if k == 2 else 0) + i / 40, "tecla", 0.35, -0.1, tono=1.0 + 0.03 * (i % 4))
        self.ev(self.t_expl - 0.3, "barrido_aire", 0.5, 0.3, dur=0.45)
        self.ev(self.t_expl, "subida", 0.9, 0.0, dur=1.8)
        self.ev(self.t_expl + 0.6, "sello_golpe", 1.0, 0.0)
        tx = self.t_escribio + 0.2
        for k, s in enumerate(("«La primera máquina ultrainteligente", "será el último invento que el hombre", "necesitará hacer.»")):
            for i in range(0, len(s), 2):
                self.ev(tx + 1.3 * k + i / 30, "tecla", 0.3, 0.0, tono=1.0 + 0.03 * (i % 4))
        self.ev(self.t_ultimo, "sello_golpe", 1.0, 0.0)
