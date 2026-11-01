# -*- coding: utf-8 -*-
"""Escena 2 «testigos»: El juicio en el Gran Salón. Ficha de Tyrion Lannister, clip entintado de la corte
y la decisión de Oberyn de presentarse como campeón.
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


class Testigos(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_escenario = w("escenario")
        self.t_sucio = w("sucio")
        self.t_juicio = w("juicio")
        self.t_combate = w("combate")
        self.t_enano = w("enano")
        self.t_dorada = w("dorada")
        self.t_acusado = w("acusado")
        self.t_nadie = w("Nadie")
        self.t_cuerpo = w("cuerpo")
        self.t_sentencia = w("sentencia")
        self.t_escrita = w("escrita")
        self.t_vibora = w("Víbora")
        self.t_paso = w("paso")
        self.t_frente = w("frente")
        self.t_salvar = w("salvar")
        self.t_elegir = w("elegir")
        self.t_verdugo = w("verdugo")

        self.cam_1 = Pista([(t0, (960, 500, 1.0)), (self.t_enano, (920, 520, 1.1), "io")])
        self.cam_3 = Pista([(self.t_vibora - 0.2, (960, 540, 1.0)), (self.t_verdugo, (960, 500, 1.2), "io")])

        self.plano(t0, self.p_corte)
        self.plano(self.t_nadie - 0.2, self.p_clip_juicio, tr="fundido", dur=0.5)
        self.plano(self.t_vibora - 0.2, self.p_campeon, tr="barrido", dur=0.6)

    # Plano 1: Gran Salón del juicio con la ficha de Tyrion
    def p_corte(self, h, t, u):
        cx, cy, z = self.cam_1(t)
        h.camara(z, cx, cy, 0.004 * math.sin(t * 0.4))
        MU.gran_salon().pegar(h, 0.7, bruma=0.25, tono_bruma=0.15)

        h.ambiente[:] = 0.35
        # Luces de antorcha proyectadas entre columnas
        h.luz_radial(450, 400, 600, (1.1, 1.0, 0.8), k=1.0)
        h.luz_radial(1550, 400, 600, (1.1, 1.0, 0.8), k=1.0)
        P.antorcha_pared(h, 450, 380, s=0.9, k_luz=1.0)

        # Ficha de Peter Dinklage
        R.retrato_noir(h, "peter_dinklage", 1250, 520, 420, t, self.t_enano,
                       rotulo="TYRION LANNISTER", leyenda="Acusado de regicidio · El Enano",
                       ang=2.0, fijacion="cinta", dur_ent=0.35)

        # Rótulo del caso
        h.camara(1.0, W / 2, H / 2, 0.0)
        N.texto_maquina(h, "JUICIO POR COMBATE", 140, 150, 42, t, self.t_juicio, cps=22, tono=0.95, encuadrar=True)
        N.texto_maquina(h, "Tribunal de la Corona · Sin apelación", 140, 210, 24, t, self.t_combate, cps=24, tono=0.75, encuadrar=False)
        N.motas(h, t, n=50, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.14, vel=6, y0=200, y1=850, sube=False))

    # Plano 2: Clip entintado del juicio
    def p_clip_juicio(self, h, t, u):
        h.camara(1.0, W / 2, H / 2, 0.0)
        dur_clip = 6.8
        R.clip_real(h, "juicio", t, self.t_nadie - 0.2, dur=dur_clip, z0=1.0, z1=1.06,
                    tinta=0.42, poster=0.16, trama=0.28, credito="ARCHIVO: HBO / GAME OF THRONES")
        # Banda de veredicto
        N.texto_maquina(h, "LA SENTENCIA YA ESTABA ESCRITA", 960, 160, 38, t, self.t_sentencia, cps=24, tono=0.96, centro=True, encuadrar=True)
        return h.acabado(t)

    # Plano 3: La Víbora Roja da un paso al frente (Lanza dorniense en contraluz)
    def p_campeon(self, h, t, u):
        cx, cy, z = self.cam_3(t)
        h.camara(z, cx, cy, 0.005 * math.sin(t * 0.5))

        # Sala oscura con luz cenital en abanico
        fondo = np.array([[0, 0], [W, 0], [W, H], [0, H]])
        h.pieza(fondo, 18, sem=41, w=6, trama=0.45)
        h.luz_cono(W / 2, 100, math.pi / 2, 0.65, 1200, (1.4, 1.4, 1.4), k=1.2, suave=0.4)

        # Lanza dorniense cruzando el plano en diagonal
        rot_l = 0.45 + 0.05 * math.sin(t * 1.5)
        P.lanza_dorniense(h, 920, 680, ang=rot_l, largo=520, s=1.2, veneno=False, sem=42)

        # Silueta en contraluz del príncipe
        N.motas(h, t, n=60, k=0.6)
        h.camara(1.0, W / 2, H / 2, 0.0)
        N.texto_maquina(h, "CAMPEÓN VOLUNTARIO", 960, 840, 46, t, self.t_frente, cps=20, tono=0.98, centro=True, encuadrar=True)
        N.texto_maquina(h, "Elegir a su propio verdugo", 960, 910, 26, t, self.t_elegir, cps=24, tono=0.80, centro=True, encuadrar=False)
        return h.acabado(t)
