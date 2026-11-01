# -*- coding: utf-8 -*-
"""Escena 1 «gancho»: Desembarco del Rey bajo la tormenta. El detective observa la entrada a la capital,
las murallas en claroscuro y la llegada de la Víbora Roja con su ficha de expediente criminal.
"""
import math
import numpy as np

import mundos_oberyn as MU
import noir as N
import noir_real as R
import props_oberyn as P
from basen import BaseNoir
from motor import H, W, clamp01, smooth
from noir_pers import Detective
from toon import Pista, pulso


class Gancho(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.det = Detective(sem=11)
        self.t_huele = w("huele")
        self.t_pescado = w("pescado")
        self.t_miedo = w("miedo")
        self.t_verano = w("verano")
        self.t_hedor = w("hedor")
        self.t_sangre = w("sangre")
        self.t_limpiar = w("limpiar")
        self.t_principe = w("príncipe")
        self.t_puertas = w("puertas")
        self.t_pleitesia = w("pleitesía")
        self.t_expediente = w("expediente")
        self.t_dieciseis = w("dieciséis")

        self.cam_1 = Pista([(t0, (960, 460, 0.85)), (self.t_pescado, (980, 520, 0.95), "io"),
                            (self.t_verano - 0.4, (1000, 560, 1.05), "io")])
        self.cam_2 = Pista([(self.t_verano - 0.3, (880, 540, 1.0)), (self.t_sangre, (920, 560, 1.15), "io"),
                            (self.t_principe - 0.3, (960, 580, 1.25), "io")])

        self.plano(t0, self.p_muralla)
        self.plano(self.t_verano - 0.2, self.p_callejon, tr="relampago", dur=0.6)
        self.plano(self.t_principe - 0.2, self.p_expediente, tr="empuje", dur=0.6, centro=(W * 0.5, H * 0.5))

    # Plano 1: Las murallas de la capital y el detective
    def p_muralla(self, h, t, u):
        cx, cy, z = self.cam_1(t)
        h.camara(z, cx, cy, 0.005 * math.sin(t * 0.4))
        MU.cielo_tormenta().pegar(h, 0.05, dx=-(t * 4.0) % 200)
        MU.muralla_capital().pegar(h, 0.4, bruma=0.35, tono_bruma=0.18)

        # Suelo empapado de la entrada
        suelo = np.array([[-400, 680], [2400, 680], [2400, 1200], [-400, 1200]])
        h.pieza(suelo, 45, sem=12, w=4, luz=(0, -1), d=10, trama=0.3)
        N.reflejo(h.img, 680, 0.45)

        # Antorcha en la torre izquierda
        P.antorcha_pared(h, 420, 480, s=1.1, k_luz=1.0 + 0.2 * math.sin(t * 7))

        # Detective de espaldas en primer término
        fum = pulso(t, self.t_huele + 1.2, 2.0, 1.0)
        p = dict(x=1340.0, y=940.0, s=1.1, d=-1, luz=(-1.0, -0.4), fumar=fum, giro=0.2, viento=0.15, hombros=0.25)
        self.det.dibujar(h, p)

        # Atmósfera
        h.ambiente[:] = 0.35
        rel = max(N.relampago(t, [self.t_pescado, self.t_miedo - 0.2]), 0.0)
        h.ambiente[:] += 1.3 * rel
        h.luz_radial(420, 520, 500, (1.2, 1.1, 0.9), k=0.8)
        N.lluvia(h, t, n=160, k=0.85, vel=1400)
        N.motas(h, t, n=60, k=0.5)

        # Rótulo a máquina
        h.camara(1.0, W / 2, H / 2, 0.0)
        N.texto_maquina(h, "DESEMBARCO DEL REY", 120, 140, 44, t, self.t_huele, cps=22, tono=0.92, encuadrar=True)
        N.texto_maquina(h, "Año 300 DC · La corte del Trono de Hierro", 120, 200, 26, t, self.t_pescado, cps=24, tono=0.75, encuadrar=False)
        return h.acabado(t, niebla=dict(dens=0.18, vel=8, y0=200, y1=900, sube=False))

    # Plano 2: Callejón medieval con clip entintado de lluvia en adoquines
    def p_callejon(self, h, t, u):
        cx, cy, z = self.cam_2(t)
        h.camara(z, cx, cy, 0.006 * math.sin(t * 0.5))

        # Clip de lluvia sobre el suelo integrado en el tercio inferior
        dur_clip = 7.0
        R.clip_real(h, "lluvia_suelo", t, self.t_verano - 0.2, dur=dur_clip, z0=1.0, z1=1.08, tinta=0.45, poster=0.18)

        # Muros en claroscuro a los lados que enmarcan el callejón
        muro_izq = np.array([[0, 0], [480, 0], [420, 1080], [0, 1080]])
        h.pieza(muro_izq, 25, sem=21, w=5, luz=(1, 0), d=14, trama=0.4, rim=0.6)
        muro_der = np.array([[1460, 0], [1920, 0], [1920, 1080], [1500, 1080]])
        h.pieza(muro_der, 20, sem=22, w=5, luz=(-1, 0), d=14, trama=0.45, rim=0.5)

        P.antorcha_pared(h, 450, 420, s=0.9, k_luz=1.1 + 0.3 * math.sin(t * 8.5))

        h.ambiente[:] = 0.30
        h.luz_radial(480, 460, 620, (1.1, 1.0, 0.8), k=1.0)
        h.luz_radial(W / 2, 750, 400, (0.8, 0.8, 0.8), k=0.6)
        N.lluvia(h, t, n=120, k=0.7, vel=1300)
        N.humo(h, t, 480, 450, k=0.8, ancho=1.2)

        h.camara(1.0, W / 2, H / 2, 0.0)
        N.texto_maquina(h, "EL HEDOR A SANGRE VIEJA", 960, 150, 40, t, self.t_hedor, cps=22, tono=0.95, centro=True, encuadrar=True)
        return h.acabado(t, niebla=dict(dens=0.15, vel=12, y0=100, y1=850, sube=False))

    # Plano 3: Ficha policial de Pedro Pascal (Oberyn Martell)
    def p_expediente(self, h, t, u):
        h.camara(1.0, W / 2, H / 2, 0.003 * math.sin(t * 0.3))
        # Fondo: mesa de sillería / expediente de cuero oscuro
        mesa = np.array([[0, 0], [W, 0], [W, H], [0, H]])
        h.pieza(mesa, 32, sem=31, w=6, luz=(0, -1), d=16, trama=0.35)

        # Luz cenital sobre la mesa
        h.luz_radial(W / 2, H / 2, 850, (1.2, 1.2, 1.2), k=1.4)
        h.luz_radial(W / 2, H / 2, 450, (1.0, 1.0, 1.0), k=1.0)

        # Ficha real de Pedro Pascal
        R.retrato_noir(h, "pedro_pascal", W / 2 - 120, H / 2, 440, t, self.t_principe,
                       rotulo="OBERYN MARTELL", leyenda="Príncipe de Dorne · La Víbora Roja",
                       ang=-2.5, fijacion="chincheta", dur_ent=0.35)

        # Carpeta / pergamino al lado
        perg = np.array([[1240, 240], [1720, 260], [1680, 840], [1200, 820]])
        h.pieza(perg, 78, sem=32, w=5, luz=(0, -1), d=10, trama=0.25, rim=0.6)
        N.texto_maquina(h, "EXPEDIENTE: DORNE", 1450, 340, 28, t, self.t_expediente, cps=18, tono=0.15, centro=True, encuadrar=False)
        N.texto_maquina(h, "Caso sin resolver", 1450, 390, 20, t, self.t_dieciseis, cps=20, tono=0.25, centro=True, encuadrar=False)
        N.texto_maquina(h, "Deuda pendiente: 16 años", 1450, 440, 18, t, self.t_dieciseis + 0.6, cps=20, tono=0.25, centro=True, encuadrar=False)

        N.motas(h, t, n=40, k=0.4)
        return h.acabado(t)
