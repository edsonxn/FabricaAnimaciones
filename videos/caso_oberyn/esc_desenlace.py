# -*- coding: utf-8 -*-
"""Escena 6 «desenlace»: El coloso de rodillas, el error fatal del orgullo y la destrucción
del cráneo en alto contraste y claroscuro.
"""
import math
import numpy as np

import mundos_oberyn as MU
import noir as N
import props_oberyn as P
from basen import BaseNoir
from motor import H, W, clamp01, smooth
from toon import Pista


class Desenlace(BaseNoir):
    TR_SALIDA = ("tinta", 0.8)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_trampa = w("trampa")
        self.t_funciono = w("funcionó")
        self.t_coloso = w("coloso")
        self.t_rodillas = w("rodillas")
        self.t_tripas = w("tripas")
        self.t_veneno = w("veneno")
        self.t_bastaba = w("Bastaba")
        self.t_paso = w("paso")
        self.t_polvo = w("polvo")
        self.t_victoria = w("victoria")
        self.t_detective = w("detective")
        self.t_error = w("error")
        self.t_obsesionados = w("obsesionados")
        self.t_monstruo = w("monstruo")
        self.t_culpa = w("culpa")
        self.t_tropiezo = w("tropiezo")
        self.t_hierro = w("hierro")
        self.t_cuello = w("cuello")
        self.t_pulgares = w("pulgares")
        self.t_luz = w("luz")

        self.cam_1 = Pista([(t0, (960, 520, 1.0)), (self.t_rodillas, (960, 540, 1.15), "io")])
        self.cam_3 = Pista([(self.t_detective - 0.2, (960, 500, 1.0)), (self.t_culpa, (960, 520, 1.2), "io")])
        self.cam_4 = Pista([(self.t_tropiezo - 0.2, (960, 520, 1.1)), (self.t_pulgares, (960, 520, 1.45), "io")])

        self.plano(t0, self.p_caida_coloso)
        self.plano(self.t_bastaba - 0.2, self.p_error_orgullo, tr="corte", dur=0.5)
        self.plano(self.t_detective - 0.2, self.p_confesion, tr="empuje", dur=0.6, centro=(W * 0.5, H * 0.5))
        self.plano(self.t_tropiezo - 0.2, self.p_craneo_final, tr="relampago", dur=0.6)

    # Plano 1: El coloso de rodillas en la arena
    def p_caida_coloso(self, h, t, u):
        cx, cy, z = self.cam_1(t)
        h.camara(z, cx, cy, 0.005 * math.sin(t * 0.4))
        MU.foso_arena().pegar(h, 0.6, bruma=0.25, tono_bruma=0.18)

        # Lanza clavada en el suelo
        P.lanza_dorniense(h, 780, 680, ang=-0.35, largo=480, s=1.1, veneno=True, sem=131)

        # Silueta masiva de la armadura vencida
        arm = np.array([[880, 620], [1220, 640], [1260, 840], [840, 820]])
        h.pieza(arm, 35, sem=132, w=5, luz=(0, -1), d=14, trama=0.45, rim=0.6)

        h.ambiente[:] = 0.35
        h.luz_radial(1050, 680, 700, (1.2, 1.2, 1.2), k=1.3)
        N.humo(h, t, 1050, 720, k=0.9, ancho=1.4)

        h.camara(1.0, W / 2, H / 2, 0.0)
        N.texto_maquina(h, "EL COLOSO DE RODILLAS", 960, 150, 42, t, self.t_coloso, cps=22, tono=0.96, centro=True, encuadrar=True)
        N.texto_maquina(h, "El veneno quemándole las venas", 960, 215, 26, t, self.t_veneno, cps=24, tono=0.78, centro=True, encuadrar=False)
        return h.acabado(t)

    # Plano 2: La tentación de la victoria
    def p_error_orgullo(self, h, t, u):
        h.camara(1.0, W / 2, H / 2, 0.0)
        fondo = np.array([[0, 0], [W, 0], [W, H], [0, H]])
        h.pieza(fondo, 22, sem=141, w=6, trama=0.4)
        h.luz_cono(W / 2, 80, math.pi / 2, 0.5, 1100, (1.4, 1.4, 1.4), k=1.2)

        N.texto_maquina(h, "BASTABA UN PASO ATRÁS", 960, 480, 52, t, self.t_bastaba, cps=20, tono=0.98, centro=True, encuadrar=True)
        N.texto_maquina(h, "Dejarlo morir en el polvo y cobrar la victoria", 960, 560, 28, t, self.t_polvo, cps=24, tono=0.82, centro=True, encuadrar=False)
        N.motas(h, t, n=60, k=0.5)
        return h.acabado(t)

    # Plano 3: La exigencia de la confesión
    def p_confesion(self, h, t, u):
        cx, cy, z = self.cam_3(t)
        h.camara(z, cx, cy, 0.005 * math.sin(t * 0.5))

        # La arena y el palco al fondo
        fondo = np.array([[0, 0], [W, 0], [W, H], [0, H]])
        h.pieza(fondo, 30, sem=151, w=6, trama=0.35)
        h.luz_radial(960, 450, 800, (1.2, 1.2, 1.2), k=1.2)

        h.camara(1.0, W / 2, H / 2, 0.0)
        N.texto_maquina(h, "EL ERROR DE LOS OBSESIONADOS", 960, 220, 44, t, self.t_detective, cps=22, tono=0.96, centro=True, encuadrar=True)
        N.texto_maquina(h, "«¡CONFIESA! ¿QUIÉN DIO LA ORDEN?»", 960, 310, 36, t, self.t_monstruo, cps=20, tono=0.90, centro=True, encuadrar=False)
        N.motas(h, t, n=50, k=0.5)
        return h.acabado(t)

    # Plano 4: El cráneo destrozado
    def p_craneo_final(self, h, t, u):
        cx, cy, z = self.cam_4(t)
        h.camara(z, cx, cy, 0.008 * math.sin(t * 0.8))

        # Oscuridad cavernosa
        fondo = np.array([[0, 0], [W, 0], [W, H], [0, H]])
        h.pieza(fondo, 14, sem=161, w=6, trama=0.5)

        # Cráneo humano con fracturas profundas en tinta
        grieta_prog = clamp01((t - self.t_pulgares) / 1.5)
        P.craneo_impacto(h, 960, 520, grietas=0.5 + 0.5 * grieta_prog, s=1.8, sem=162)

        # Relámpago salvaje
        h.ambiente[:] = 0.25
        rel = max(N.relampago(t, [self.t_tropiezo, self.t_pulgares, self.t_luz - 0.2]), 0.0)
        h.ambiente[:] += 1.8 * rel
        h.luz_radial(960, 520, 600, (1.5, 1.5, 1.5), k=1.4)

        h.camara(1.0, W / 2, H / 2, 0.0)
        N.texto_maquina(h, "DOS PULGARES APAGARON LA LUZ", 960, 860, 46, t, self.t_pulgares, cps=22, tono=0.98, centro=True, encuadrar=True)
        return h.acabado(t)
