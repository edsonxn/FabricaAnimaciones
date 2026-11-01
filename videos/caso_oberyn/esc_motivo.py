# -*- coding: utf-8 -*-
"""Escena 4 «motivo»: El móvil del crimen: Elia Martell y la deuda de sangre del saqueo.
Pedestal funerario, capa carmesí, memoria del saqueo y balanza de justicia rota.
"""
import math
import numpy as np

import noir as N
import props_oberyn as P
from basen import BaseNoir
from motor import H, W, clamp01, smooth
from toon import Pista


class Motivo(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_movil = w("móvil")
        self.t_crimen = w("crimen")
        self.t_deuda = w("deuda")
        self.t_pagar = w("pagar")
        self.t_elia = w("Elia")
        self.t_martell = w("Martell")
        self.t_hermana = w("hermana")
        self.t_violada = w("violada")
        self.t_hijos = w("hijos")
        self.t_degollados = w("degollados")
        self.t_saqueo = w("saqueo")
        self.t_cadaver = w("cadáver")
        self.t_capa = w("capa")
        self.t_carmesi = w("carmesí")
        self.t_verguenza = w("vergüenza")
        self.t_decadas = w("décadas")
        self.t_senores = w("señores")
        self.t_accidente = w("accidente")
        self.t_rencor = w("rencor")
        self.t_silencio = w("silencio")
        self.t_tribunal = w("tribunal")

        self.cam_1 = Pista([(t0, (960, 520, 1.0)), (self.t_elia, (960, 480, 1.15), "io")])
        self.cam_2 = Pista([(self.t_hermana - 0.2, (960, 540, 1.0)), (self.t_saqueo, (960, 500, 1.2), "io")])
        self.cam_3 = Pista([(self.t_decadas - 0.2, (960, 520, 1.0)), (self.t_tribunal, (960, 480, 1.18), "io")])

        self.plano(t0, self.p_santuario)
        self.plano(self.t_hermana - 0.2, self.p_saqueo, tr="humo", dur=0.7)
        self.plano(self.t_decadas - 0.2, self.p_balanza, tr="tinta", dur=0.6)

    # Plano 1: Santuario / Pedestal en honor a Elia Martell
    def p_santuario(self, h, t, u):
        cx, cy, z = self.cam_1(t)
        h.camara(z, cx, cy, 0.004 * math.sin(t * 0.4))

        # Cripta de piedra oscura
        fondo = np.array([[0, 0], [W, 0], [W, H], [0, H]])
        h.pieza(fondo, 20, sem=81, w=6, trama=0.45)

        # Pedestal mortuorio central
        altar = np.array([[680, 640], [1240, 640], [1280, 940], [640, 940]])
        h.pieza(altar, 48, sem=82, w=5, luz=(0, -1), d=14, trama=0.3, rim=0.7)

        # Capa carmesí doblada sobre el altar
        capa = np.array([[740, 610], [1180, 620], [1160, 660], [720, 650]])
        h.pieza(capa, 35, sem=83, w=4, luz=(0, -1), d=8, trama=0.4)

        # Luz cenital débil y triste
        h.luz_cono(960, 100, math.pi / 2, 0.45, 1000, (1.2, 1.1, 1.0), k=1.0, suave=0.5)
        P.antorcha_pared(h, 420, 440, s=0.8, k_luz=0.7 + 0.2 * math.sin(t * 6))

        h.camara(1.0, W / 2, H / 2, 0.0)
        N.texto_maquina(h, "EL MÓVIL: ELIA MARTELL", 960, 160, 44, t, self.t_movil, cps=22, tono=0.96, centro=True, encuadrar=True)
        N.texto_maquina(h, "Princesa de Dorne · Asesinada en el saqueo", 960, 225, 26, t, self.t_elia, cps=24, tono=0.78, centro=True, encuadrar=False)
        N.motas(h, t, n=60, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.18, vel=5, y0=200, y1=850, sube=True))

    # Plano 2: Memoria del saqueo (sombras de fuego y humo espeso)
    def p_saqueo(self, h, t, u):
        cx, cy, z = self.cam_2(t)
        h.camara(z, cx, cy, 0.007 * math.sin(t * 0.5))

        # Ciudad ardiendo en siluetas
        fondo = np.array([[0, 0], [W, 0], [W, H], [0, H]])
        h.pieza(fondo, 15, sem=91, w=6, trama=0.5)

        # Resplandor de llamas en la parte inferior
        par = 1.0 + 0.3 * math.sin(t * 9)
        h.luz_radial(960, 950, 800, (1.4, 1.2, 0.9), k=1.4 * par)
        N.humo(h, t, 600, 700, k=1.2, ancho=1.6)
        N.humo(h, t, 1300, 680, k=1.1, ancho=1.5)

        h.camara(1.0, W / 2, H / 2, 0.0)
        N.texto_maquina(h, "EL SAQUEO DE LA CIUDAD", 960, 160, 42, t, self.t_saqueo, cps=22, tono=0.95, centro=True, encuadrar=True)
        N.texto_maquina(h, "Una capa carmesí para tapar la vergüenza", 960, 225, 26, t, self.t_capa, cps=24, tono=0.80, centro=True, encuadrar=False)
        return h.acabado(t)

    # Plano 3: Documento del pacto y balanza de justicia rota
    def p_balanza(self, h, t, u):
        cx, cy, z = self.cam_3(t)
        h.camara(z, cx, cy, 0.003 * math.sin(t * 0.3))

        # Mesa de investigación
        mesa = np.array([[0, 0], [W, 0], [W, H], [0, H]])
        h.pieza(mesa, 38, sem=101, w=6, trama=0.3)
        h.luz_radial(W / 2, H / 2, 750, (1.2, 1.2, 1.2), k=1.3)

        # Expediente abierto
        hoja = np.array([[540, 260], [1380, 280], [1340, 820], [500, 800]])
        h.pieza(hoja, 82, sem=102, w=5, luz=(0, -1), d=12, trama=0.25, rim=0.6)

        N.texto_maquina(h, "DEUDA DE SANGRE", 960, 360, 40, t, self.t_decadas, cps=20, tono=0.15, centro=True, encuadrar=False)
        N.texto_maquina(h, "Causa: Homicidio y violación de Estado", 960, 420, 24, t, self.t_senores, cps=22, tono=0.25, centro=True, encuadrar=False)
        N.texto_maquina(h, "Veredicto oficial: «Accidente de guerra»", 960, 475, 22, t, self.t_accidente, cps=24, tono=0.25, centro=True, encuadrar=False)
        N.texto_maquina(h, "Estado: PENDIENTE DE COBRO", 960, 540, 26, t, self.t_rencor, cps=22, tono=0.10, centro=True, encuadrar=True)

        N.motas(h, t, n=40, k=0.4)
        return h.acabado(t)
