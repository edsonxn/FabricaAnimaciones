# -*- coding: utf-8 -*-
"""Escena 5 «pruebas»: El arma del crimen: la lanza de fresno y el veneno de mantícora.
Clip entintado del duelo en alta tensión y disección quirúrgica del gigante.
"""
import math
import numpy as np

import mundos_oberyn as MU
import noir as N
import noir_real as R
import props_oberyn as P
from basen import BaseNoir
from motor import H, W, clamp01, smooth
from toon import Pista


class Pruebas(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_manana = w("mañana")
        self.t_duelo = w("duelo")
        self.t_dorniense = w("dorniense")
        self.t_espada = w("espada")
        self.t_lanza = w("lanza")
        self.t_fresno = w("fresno")
        self.t_ligera = w("Ligera")
        self.t_rapida = w("Rápida")
        self.t_detalle = w("detalle")
        self.t_oficiales = w("oficiales")
        self.t_punta = w("punta")
        self.t_veneno = w("veneno")
        self.t_manticora = w("mantícora")
        self.t_combate = w("combate")
        self.t_caballeros = w("caballeros")
        self.t_diseccion = w("disección")
        self.t_confesion = w("confesión")
        self.t_gigante = w("gigante")
        self.t_corte = w("corte")

        self.cam_1 = Pista([(t0, (960, 520, 1.0)), (self.t_lanza, (960, 500, 1.15), "io")])
        self.cam_2 = Pista([(self.t_ligera - 0.2, (960, 540, 1.0)), (self.t_manticora, (960, 480, 1.25), "io")])

        self.plano(t0, self.p_lanza_arena)
        self.plano(self.t_ligera - 0.2, self.p_veneno, tr="barrido", dur=0.5)
        self.plano(self.t_combate - 0.2, self.p_clip_duelo, tr="empuje", dur=0.6, centro=(W * 0.5, H * 0.5))

    # Plano 1: La lanza de fresno en el foso
    def p_lanza_arena(self, h, t, u):
        cx, cy, z = self.cam_1(t)
        h.camara(z, cx, cy, 0.005 * math.sin(t * 0.5))
        MU.foso_arena().pegar(h, 0.6, bruma=0.2, tono_bruma=0.18)

        # Lanza dorniense en ángulo dinámico
        ang_l = 0.35 + 0.08 * math.sin(t * 2.2)
        P.lanza_dorniense(h, 960, 680, ang=ang_l, largo=520, s=1.2, veneno=False, sem=111)

        h.ambiente[:] = 0.35
        h.luz_radial(960, 640, 750, (1.2, 1.2, 1.1), k=1.2)

        h.camara(1.0, W / 2, H / 2, 0.0)
        N.texto_maquina(h, "EL ARMA: LANZA DE FRESNO", 140, 150, 42, t, self.t_lanza, cps=22, tono=0.95, encuadrar=True)
        N.texto_maquina(h, "Ligera · Rápida · Alcance superior", 140, 215, 24, t, self.t_fresno, cps=24, tono=0.75, encuadrar=False)
        N.motas(h, t, n=50, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.14, vel=8, y0=200, y1=850, sube=False))

    # Plano 2: Veneno de mantícora y frasco de boticario
    def p_veneno(self, h, t, u):
        cx, cy, z = self.cam_2(t)
        h.camara(z, cx, cy, 0.004 * math.sin(t * 0.4))

        # Mesa del boticario
        mesa = np.array([[0, 0], [W, 0], [W, H], [0, H]])
        h.pieza(mesa, 26, sem=121, w=6, trama=0.4)
        h.luz_radial(W / 2, H / 2, 650, (1.1, 1.1, 1.1), k=1.3)

        # Frasco de mantícora en primer término
        P.frasco_veneno(h, 720, 520, s=1.8, tono_liquido=12, sem=122)

        # Punta de lanza con veneno goteando
        P.lanza_dorniense(h, 1260, 500, ang=-0.75, largo=460, s=1.3, veneno=True, sem=123)

        h.camara(1.0, W / 2, H / 2, 0.0)
        N.texto_maquina(h, "VENENO DE MANTÍCORA", 960, 160, 44, t, self.t_veneno, cps=22, tono=0.96, centro=True, encuadrar=True)
        N.texto_maquina(h, "Espesado con magia para retrasar la muerte y maximizar la agonía", 960, 225, 22, t, self.t_manticora, cps=26, tono=0.80, centro=True, encuadrar=False)
        return h.acabado(t)

    # Plano 3: Clip entintado del combate en acción
    def p_clip_duelo(self, h, t, u):
        h.camara(1.0, W / 2, H / 2, 0.0)
        dur_clip = 6.8
        R.clip_real(h, "duelo", t, self.t_combate - 0.2, dur=dur_clip, z0=1.0, z1=1.08,
                    tinta=0.44, poster=0.18, trama=0.30, credito="ARCHIVO: HBO / GAME OF THRONES")
        # Rótulo de tensión
        N.texto_maquina(h, "DISECCIÓN QUIRÚRGICA", 960, 160, 42, t, self.t_diseccion, cps=22, tono=0.96, centro=True, encuadrar=True)
        N.texto_maquina(h, "Arrancarle una confesión al gigante", 960, 225, 26, t, self.t_confesion, cps=24, tono=0.82, centro=True, encuadrar=False)
        return h.acabado(t)
