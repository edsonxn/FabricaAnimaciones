# -*- coding: utf-8 -*-
"""Escena 6 «carrera»: el detective en la ventana con la luz de la persiana en rayas · faros bajo la lluvia (video real) · carrera de
autos de los 40 por la calle mojada (empresas, luego países con banderines) · velocímetro en la zona roja (FRENAR = PERDER) ·
fichas reales empujadas al centro (video) y la mesa de póker mientras, por la ventana, la casa arde."""
import math

import cv2
import numpy as np

import mundos as MU
import noir as N
import props as PR
import props5 as P5
from basen import BaseNoir
from esc_lluvia import fondo_ciudad, reflejar
from motor import H, W, clamp01, e_inout, e_out, smooth
from noir import gris
from noir_pers import Busto, Frontal
from toon import Pista, elipse_, pulso


class Carrera(BaseNoir):
    TR_SALIDA = ("relampago", 0.4)

    def armar(self):
        w = self.w
        self.busto = Busto(sem=5)
        self.jug = [Frontal(sem=100 + 9 * k) for k in range(4)]
        self.t_detienen = w("detienen")
        self.t_porque = w("Porque esta")
        self.t_otro = w("otro")
        self.t_empresas = w("Las empresas")
        self.t_primero = w("primero")
        self.t_paises = w("Los países")
        self.t_frenar = w("Frenar")
        self.t_perder = w("perder")
        self.t_carrera = w("carrera más")
        self.t_poker = w("póker")
        self.t_casa = w("casa")
        self.t_incendiar = w("incendiar")
        self.t_nadie = w("nadie se levanta")
        self.t_mesa = w("mesa")
        self.plano(self.t0, self.p_ventana)
        self.plano(self.t_porque - 0.3, self.p_faros, tr="barrido", dur=0.45, dirx=1)
        self.plano(self.t_empresas - 0.3, self.p_carrera, tr="barrido", dur=0.4, dirx=1)
        self.plano(self.t_frenar - 0.3, self.p_velocimetro, tr="empuje", dur=0.45)
        self.plano(self.t_poker - 0.4, self.p_fichas, tr="relampago", dur=0.3)
        self.plano(self.t_poker + 1.3, self.p_mesa, tr="barrido", dur=0.45, dirx=-1)

    # ------------------------------------------------------------------ en la ventana
    def p_ventana(self, h, t, u):
        h.camara(1.0, W / 2, H / 2, 0.0)
        h.camara(1.25, 1450, 0, 0.0)
        MU.oficina().pegar(h, 1.0, oscuro=0.6)
        h.camara(1.0, W / 2, H / 2, 0.0)
        p = dict(x=760 + 10 * u, y=520, s=1.05, d=1, luz=(1.0, -0.2), brasa=0.3, arriba=0.2 + 0.2 * smooth(clamp01((t - self.t_detienen) / 1)),
                 rot=-0.03)
        self.busto.dibujar(h, p)
        tip = self.busto.punta(p)
        h.emitir(elipse_(tip[0], tip[1], 6, 6, n=10), 1.0)
        N.humo(h, t, tip[0], tip[1], k=0.9, ancho=2.0, viento=(-40, -120))
        h.ambiente[:] = 0.25
        h.luz_persiana(np.array([[300, -100], [2100, -260], [2100, 1300], [300, 1160]]), k=1.25, n=18, abierto=0.5, suave=1.2,
                       mundo=False)
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ faros (video real)
    def p_faros(self, h, t, u):
        N.clip_noir(h, "autos_1", t, self.t_porque - 0.3, inicio=0.5, z0=1.05, z1=1.25, dur=5.5, tinta=0.5, poster=0.35, expo=1.1)
        N.sello(h, "SI TÚ NO, OTRO SÍ", W / 2, 900, 90, t, self.t_otro - 0.1, rot=-4, tono=0.96)
        h.ambiente[:] = 1.0
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ la carrera
    def p_carrera(self, h, t, u):
        # la cámara corre a la par de los autos por la calle mojada (la ciudad pasa a toda velocidad)
        cx = 600 + 1500 * u
        h.camara(1.3, cx, 930, 0.0)
        fondo_ciudad(h, t)
        MU.calle().pegar(h, 1.0)
        paises = t > self.t_paises - 0.2
        autos = [("EMPRESA A", 1.0, 0), ("EMPRESA B", 0.92, 1), ("EMPRESA C", 0.86, 2)] if not paises else \
            [("franjas", 1.0, 0), ("estrella", 0.95, 1), ("franjas", 0.9, 2)]
        for k, (b, sp, fila) in enumerate(autos):
            x = cx - 420 + 300 * k + 90 * math.sin(t * (1.3 + 0.4 * k) + k) + 120 * sp
            y = 1060 + 70 * fila
            P5.auto(h, x, y, s=0.72 + 0.06 * fila, t=t, vel=6, sem=20 + 30 * k, tono=34 + 14 * k, bandera=b)
            N.lineas = None
            for j in range(5):                                     # rayas de velocidad
                yy = y - 30 - j * 26
                h.trazo(np.array([[x - 260 - 200, yy], [x - 260 - 40, yy]]), 3, 300 + 10 * k + j, color=gris(220), alfa=0.5)
        h.ambiente[:] = 0.7
        reflejar(h, t)
        N.lluvia(h, t, n=700, viento=-0.5, vel=2200)
        img = h.acabado(t, niebla=dict(dens=0.2, y0=300, y1=1000, vel=400))
        return N._desenfoque_h(img, 9)

    # ------------------------------------------------------------------ frenar = perder
    def p_velocimetro(self, h, t, u):
        h.camara(1.0 + 0.04 * u, W / 2, H / 2, 0.0)
        h.img[:] = 0.07
        v = 0.45 + 0.6 * smooth(clamp01((t - self.t_frenar) / 2.6))
        P5.velocimetro(h, W / 2 - 260, H / 2 + 20, 380, v, t=t, sem=5)
        N.sello(h, "FRENAR", W / 2 + 470, 250, 110, t, self.t_frenar + 0.1, rot=-6, tono=0.97)
        N.sello(h, "= PERDER", W / 2 + 470, 520, 110, t, self.t_perder, rot=4, tono=0.97)
        N.texto_maquina(h, "la carrera más importante", W / 2 + 470, 700, 36, t, self.t_carrera, cps=30, tono=0.9, centro=True)
        N.texto_maquina(h, "de la historia", W / 2 + 470, 752, 36, t, self.t_carrera + 0.85, cps=30, tono=0.9, centro=True)
        h.ambiente[:] = 0.4
        h.luz_radial(W / 2 - 260, H / 2, 800, (1.3, 1.3, 1.3))
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ fichas (video real)
    def p_fichas(self, h, t, u):
        N.clip_noir(h, "poker_3", t, self.t_poker - 0.4, inicio=2.0, z0=1.05, z1=1.2, dur=2.5, tinta=0.55, poster=0.4)
        h.ambiente[:] = 1.0
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ la mesa de póker y la casa que arde
    def p_mesa(self, h, t, u):
        z = 1.0 + 0.12 * smooth(clamp01(u / 5.5))
        h.camara(z, W / 2, H / 2 - 20, 0.0)
        h.img[:] = 0.20
        # ventana del fondo: la casa en llamas (video real entintado dentro del marco)
        fuego = smooth(clamp01((t - self.t_casa) / 0.8))
        win = (1180, 40, 620, 400)
        tmp = h.img.copy()
        N.clip_noir(h, "fuego_2", t, self.t_poker, inicio=1.0, z0=1.0, z1=1.05, dur=6.0, tinta=0.4, poster=0.3, trama=0.0, expo=1.2)
        fz = h.img.copy()
        h.img[:] = tmp
        x0, y0, ww, hh = win
        sub = cv2.resize(fz, (ww, hh))
        h.img[y0:y0 + hh, x0:x0 + ww] = h.img[y0:y0 + hh, x0:x0 + ww] * (1 - fuego) + sub * fuego
        h.emisivo()[y0:y0 + hh, x0:x0 + ww] += sub[..., 0] * 0.8 * fuego
        h.anillo(PR.rect(x0, y0, ww, hh), 14, 3, color=(10, 10, 10))
        h.trazo(np.array([[x0 + ww / 2, y0], [x0 + ww / 2, y0 + hh]]), 10, 4, tf=False)
        h.trazo(np.array([[x0, y0 + hh / 2], [x0 + ww, y0 + hh / 2]]), 10, 5, tf=False)
        # jugadores (sombreros y cigarros) detrás de la mesa
        for k, (x, pelo) in enumerate(((330, "sombrero"), (740, "oscuro"), (1180, "sombrero"), (1590, "calvo"))):
            self.jug[k].dibujar(h, dict(x=x, y=1400, s=1.6, luz=(0, -1), traje=50 + 10 * k, pelo=pelo, mira=math.sin(t + k) * 0.5,
                                        rim=0.9, gafas=(k == 1)))
        # la mesa de fieltro y las fichas
        h.pieza(np.array([[120, 860], [1800, 860], [1960, 1100], [-40, 1100]]), 70, 6, w=6, luz=(0, -1), d=12, trama=0.3, rim=0.6)
        h.pieza(np.array([[100, 840], [1820, 840], [1840, 870], [80, 870]]), 30, 7, w=5, luz=(0, -1), d=4, trama=0, rim=0.8)
        empuje = smooth(clamp01((t - self.t_nadie + 0.8) / 1.2))
        for k, (x, n) in enumerate(((330, 8), (740, 12), (1180, 6), (1590, 10))):
            fx = x + (W / 2 - x) * 0.5 * empuje
            P5.fichas(h, fx, 980, n, s=1.2, sem=200 + 20 * k, tono=210 - 30 * (k % 2))
        for k in range(5):                                         # cartas
            h.pieza(PR.rot(PR.rect(820 + k * 64, 1010, 60, 86), 0.05 * (k - 2), np.array([850 + k * 64, 1000])), 230, 260 + k, w=3,
                    luz=(0, -1), d=3, trama=0, rim=0)
        h.ambiente[:] = 0.3 + 0.25 * fuego * (0.7 + 0.3 * math.sin(t * 13))
        PR.lampara_colgante(h, 820, -300, largo=440, ang=0.02 * math.sin(t), k=1.0, s=1.2, abre=0.8, alcance=1500, sem=30)
        h.luz_radial(x0 + ww / 2, y0 + hh / 2, 900, (1.0, 1.0, 1.0), k=0.8 * fuego * (0.8 + 0.2 * math.sin(t * 9)))
        N.humo(h, t, 400, 640, k=0.7, ancho=2.0, viento=(20, -80))
        N.humo(h, t, 1250, 640, k=0.7, ancho=2.0, viento=(-20, -80), sem=4)
        return h.acabado(t, niebla=dict(dens=0.25, vel=10, y0=-200, y1=700, sube=False))

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        self.ev(self.t0, "lluvia_lejana", 0.4, 0.4, dur=self.t_porque - self.t0)
        self.ev(self.t0 + 0.3, "persiana", 0.6, 0.4)
        self.ev(self.t_porque - 0.3, "auto_pasa", 0.9, -0.5, dur=2.5)
        self.ev(self.t_otro - 0.6, "auto_pasa", 0.9, 0.5, dur=2.5)
        self.ev(self.t_otro - 0.1, "sello_golpe", 0.8, 0.0)
        self.ev(self.t_empresas - 0.3, "motores_carrera", 0.9, 0.0, dur=self.t_frenar - self.t_empresas + 0.3)
        self.ev(self.t_frenar - 0.3, "motor_acelera", 0.8, 0.0, dur=3.0)
        self.ev(self.t_frenar + 0.1, "sello_golpe", 0.8, 0.3)
        self.ev(self.t_perder, "sello_golpe", 0.9, 0.3)
        self.ev(self.t_poker - 0.4, "fichas_mezcla", 0.9, 0.0, dur=1.8)
        self.ev(self.t_casa, "fuego", 0.7, -0.2, dur=self.t1 - self.t_casa)
        self.ev(self.t_nadie - 0.8, "fichas_empuja", 0.9, 0.0, dur=1.2)
