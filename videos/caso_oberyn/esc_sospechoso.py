# -*- coding: utf-8 -*-
"""Escena 3 «sospechoso»: La Montaña que Cabalga y el verdadero cerebro detrás del crimen:
Tywin Lannister. Fichas de Hafthor Bjornsson y Charles Dance con espadón en claroscuro.
"""
import math
import numpy as np

import noir as N
import noir_real as R
import props_oberyn as P
from basen import BaseNoir
from motor import H, W, clamp01, smooth
from toon import Pista


class Sospechoso(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_sospechoso = w("sospechoso")
        self.t_oficial = w("oficial")
        self.t_gregor = w("Gregor")
        self.t_clegane = w("Clegane")
        self.t_montana = w("Montaña")
        self.t_cabalga = w("Cabalga")
        self.t_ciento = w("Ciento")
        self.t_musculo = w("músculo")
        self.t_acero = w("acero")
        self.t_animal = w("animal")
        self.t_quebrar = w("quebrar")
        self.t_oficio = w("oficio")
        self.t_mirar = w("mirar")
        self.t_arma = w("arma")
        self.t_bestia = w("bestia")
        self.t_mano = w("mano")
        self.t_orden = w("orden")
        self.t_seda = w("seda")
        self.t_palco = w("palco")
        self.t_tywin = w("Tywin")
        self.t_lannister = w("Lannister")

        self.cam_1 = Pista([(t0, (960, 500, 1.0)), (self.t_clegane, (960, 520, 1.15), "io")])
        self.cam_2 = Pista([(self.t_ciento - 0.2, (960, 520, 1.0)), (self.t_quebrar, (960, 480, 1.2), "io")])
        self.cam_3 = Pista([(self.t_oficio - 0.2, (960, 500, 1.0)), (self.t_tywin, (980, 520, 1.15), "io")])

        self.plano(t0, self.p_montana)
        self.plano(self.t_ciento - 0.2, self.p_espadon, tr="corte", dur=0.5)
        self.plano(self.t_oficio - 0.2, self.p_tywin, tr="empuje", dur=0.6, centro=(W * 0.5, H * 0.5))

    # Plano 1: Ficha de Gregor Clegane (La Montaña)
    def p_montana(self, h, t, u):
        cx, cy, z = self.cam_1(t)
        h.camara(z, cx, cy, 0.004 * math.sin(t * 0.4))
        # Fondo: muro de fortaleza maciza
        muro = np.array([[0, 0], [W, 0], [W, H], [0, H]])
        h.pieza(muro, 22, sem=51, w=6, trama=0.45)
        h.luz_radial(W / 2, H / 2, 800, (1.1, 1.1, 1.1), k=1.2)

        # Ficha de Hafthor Bjornsson
        R.retrato_noir(h, "hafthor_julius_bjornsson", W / 2, H / 2, 460, t, self.t_gregor,
                       rotulo="GREGOR CLEGANE", leyenda="Ser Gregor · La Montaña que Cabalga",
                       ang=-1.5, fijacion="chincheta", dur_ent=0.35)

        h.camara(1.0, W / 2, H / 2, 0.0)
        N.texto_maquina(h, "EL BRAZO EJECUTOR", 120, 140, 42, t, self.t_sospechoso, cps=22, tono=0.92, encuadrar=True)
        N.motas(h, t, n=50, k=0.5)
        return h.acabado(t)

    # Plano 2: El espadón clavado en la piedra con relámpago
    def p_espadon(self, h, t, u):
        cx, cy, z = self.cam_2(t)
        h.camara(z, cx, cy, 0.005 * math.sin(t * 0.6))

        # Sala de armas oscura
        fondo = np.array([[0, 0], [W, 0], [W, H], [0, H]])
        h.pieza(fondo, 28, sem=61, w=6, trama=0.4)

        # Piedra base donde se clava
        pedestal = np.array([[500, 720], [1420, 720], [1460, 1080], [460, 1080]])
        h.pieza(pedestal, 40, sem=62, w=5, luz=(0, -1), d=14, trama=0.35, rim=0.6)

        # Espadón de dos manos clavado en vertical
        P.espadon_clegane(h, 960, 680, ang=0.08, largo=520, s=1.25, tono=110, sem=63)

        h.ambiente[:] = 0.30
        rel = max(N.relampago(t, [self.t_musculo + 0.4, self.t_quebrar - 0.2]), 0.0)
        h.ambiente[:] += 1.4 * rel
        h.luz_cono(960, 50, math.pi / 2, 0.55, 1100, (1.5, 1.5, 1.5), k=1.3)

        h.camara(1.0, W / 2, H / 2, 0.0)
        N.texto_maquina(h, "180 KILOS DE MÚSCULO Y ACERO", 960, 160, 40, t, self.t_ciento, cps=24, tono=0.96, centro=True, encuadrar=True)
        return h.acabado(t)

    # Plano 3: Ficha de Charles Dance (Tywin Lannister - El cerebro de la orden)
    def p_tywin(self, h, t, u):
        cx, cy, z = self.cam_3(t)
        h.camara(z, cx, cy, 0.004 * math.sin(t * 0.4))

        # Despacho / palco del señor de la guerra
        fondo = np.array([[0, 0], [W, 0], [W, H], [0, H]])
        h.pieza(fondo, 35, sem=71, w=6, trama=0.3)
        h.luz_radial(1150, 480, 850, (1.2, 1.2, 1.2), k=1.3)

        # Ficha de Charles Dance
        R.retrato_noir(h, "charles_dance", 1150, 480, 450, t, self.t_tywin,
                       rotulo="TYWIN LANNISTER", leyenda="Mano del Rey · Autor Intelectual",
                       ang=2.2, fijacion="chincheta", dur_ent=0.35)

        h.camara(1.0, W / 2, H / 2, 0.0)
        N.texto_maquina(h, "LA MANO QUE FIRMÓ LA ORDEN", 130, 150, 42, t, self.t_mano, cps=22, tono=0.95, encuadrar=True)
        N.texto_maquina(h, "Miraba desde el palco vestido de seda", 130, 215, 24, t, self.t_palco, cps=24, tono=0.80, encuadrar=False)
        N.motas(h, t, n=45, k=0.4)
        return h.acabado(t)
