# -*- coding: utf-8 -*-
"""Escena 7 «caso_abierto»: La arena vacía bajo la lluvia, los sótanos del castillo
y el sello final del caso cerrado. El detective reflexiona en la noche de la capital.
"""
import math
import numpy as np

import mundos_oberyn as MU
import noir as N
import props_oberyn as P
from basen import BaseNoir
from motor import H, W, clamp01, smooth
from noir_pers import Detective
from toon import Pista, pulso


class CasoAbierto(BaseNoir):
    TR_SALIDA = ("fundido", 1.0)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.det = Detective(sem=17)
        self.t_justicia = w("justicia")
        self.t_mundo = w("mundo")
        self.t_palabra = w("palabra")
        self.t_debiles = w("débiles")
        self.t_dormir = w("dormir")
        self.t_montana = w("Montaña")
        self.t_semanas = w("semanas")
        self.t_pudriendose = w("pudriéndose")
        self.t_sotanos = w("sótanos")
        self.t_aullidos = w("aullidos")
        self.t_castillo = w("castillo")
        self.t_vibora = w("Víbora")
        self.t_ceniza = w("ceniza")
        self.t_tierra = w("tierra")
        self.t_cerrado = w("cerrado")
        self.t_desembarco = w("Desembarco")
        self.t_nadie = w("nadie")
        self.t_gano = w("ganó")

        self.cam_1 = Pista([(t0, (960, 500, 1.0)), (self.t_dormir, (960, 520, 1.1), "io")])
        self.cam_2 = Pista([(self.t_montana - 0.2, (960, 520, 1.0)), (self.t_aullidos, (960, 500, 1.15), "io")])
        self.cam_3 = Pista([(self.t_vibora - 0.2, (960, 500, 1.0)), (self.t_gano, (960, 500, 1.05), "io")])

        self.plano(t0, self.p_arena_vacia)
        self.plano(self.t_montana - 0.2, self.p_sotanos, tr="humo", dur=0.6)
        self.plano(self.t_vibora - 0.2, self.p_sello_cierre, tr="tinta", dur=0.7)

    # Plano 1: Arena vacía lavada por la lluvia
    def p_arena_vacia(self, h, t, u):
        cx, cy, z = self.cam_1(t)
        h.camara(z, cx, cy, 0.005 * math.sin(t * 0.4))
        MU.foso_arena().pegar(h, 0.6, bruma=0.3, tono_bruma=0.18)

        # Detective fumando de espaldas en el borde de la arena
        fum = pulso(t, self.t_justicia + 1.0, 2.2, 1.0)
        p = dict(x=1280.0, y=920.0, s=1.1, d=-1, luz=(-1.0, -0.4), fumar=fum, giro=0.2, viento=0.12, hombros=0.25)
        self.det.dibujar(h, p)

        h.ambiente[:] = 0.35
        h.luz_radial(1280, 920, 380, (0.8, 0.8, 0.8), k=0.7)
        N.lluvia(h, t, n=150, k=0.8, vel=1350)
        N.reflejo(h.img, 720, 0.4)

        h.camara(1.0, W / 2, H / 2, 0.0)
        N.texto_maquina(h, "LA ILUSIÓN DE JUSTICIA", 960, 150, 44, t, self.t_justicia, cps=22, tono=0.96, centro=True, encuadrar=True)
        N.texto_maquina(h, "Una palabra inventada para poder dormir tranquilos", 960, 215, 26, t, self.t_debiles, cps=24, tono=0.80, centro=True, encuadrar=False)
        return h.acabado(t, niebla=dict(dens=0.16, vel=8, y0=200, y1=850, sube=False))

    # Plano 2: Sótanos y agonía de la Montaña
    def p_sotanos(self, h, t, u):
        cx, cy, z = self.cam_2(t)
        h.camara(z, cx, cy, 0.004 * math.sin(t * 0.5))

        # Bóveda subterránea oscura
        fondo = np.array([[0, 0], [W, 0], [W, H], [0, H]])
        h.pieza(fondo, 18, sem=181, w=6, trama=0.45)
        P.antorcha_pared(h, 420, 460, s=0.85, k_luz=0.8 + 0.3 * math.sin(t * 8))

        h.ambiente[:] = 0.30
        h.luz_radial(420, 500, 500, (1.1, 0.95, 0.8), k=0.9)
        N.humo(h, t, 420, 480, k=0.8, ancho=1.3)

        h.camara(1.0, W / 2, H / 2, 0.0)
        N.texto_maquina(h, "SEMANAS DE AGONÍA EN LOS SÓTANOS", 960, 160, 42, t, self.t_semanas, cps=22, tono=0.96, centro=True, encuadrar=True)
        N.texto_maquina(h, "Aullidos que despertaron al castillo", 960, 225, 26, t, self.t_aullidos, cps=24, tono=0.78, centro=True, encuadrar=False)
        return h.acabado(t)

    # Plano 3: Carpeta cerrada y sello final
    def p_sello_cierre(self, h, t, u):
        cx, cy, z = self.cam_3(t)
        h.camara(z, cx, cy, 0.003 * math.sin(t * 0.3))

        # Mesa del detective
        mesa = np.array([[0, 0], [W, 0], [W, H], [0, H]])
        h.pieza(mesa, 30, sem=191, w=6, trama=0.35)
        h.luz_radial(W / 2, H / 2, 750, (1.2, 1.2, 1.2), k=1.3)

        # Carpeta cerrada de cuero con cinta
        exp = np.array([[520, 260], [1400, 280], [1360, 800], [480, 780]])
        h.pieza(exp, 65, sem=192, w=6, luz=(0, -1), d=14, trama=0.3, rim=0.7)

        N.texto_maquina(h, "EXPEDIENTE MARTEL", 960, 360, 44, t, self.t_vibora, cps=20, tono=0.15, centro=True, encuadrar=False)
        N.texto_maquina(h, "La Víbora ya era ceniza bajo tierra", 960, 425, 24, t, self.t_ceniza, cps=22, tono=0.25, centro=True, encuadrar=False)

        # Sello final de impacto
        t_sello = self.t_cerrado + 0.2
        N.sello(h, "CASO CERRADO", 960, 560, 48, t, t_sello, rot=5.0, tono=0.10)

        N.texto_maquina(h, "En Desembarco del Rey... nadie ganó.", 960, 680, 28, t, self.t_nadie, cps=22, tono=0.18, centro=True, encuadrar=False)
        N.motas(h, t, n=40, k=0.4)
        return h.acabado(t)
