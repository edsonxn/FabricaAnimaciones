# -*- coding: utf-8 -*-
"""Escena 3 «interrogatorio»: el memo con el reemplazo; la cámara de vigilancia que se apaga y la copia que sale hacia otro
servidor; la sala de interrogatorio con el robot bajo la bombilla; el medidor de confesión casi en cero y tres mentiras en globos.
Mundo y utilería propios (mundos_secreto.sala_interrogatorio, camara_vigilancia, burbuja, espejo_unidireccional)."""
import math

import numpy as np

import comun as C
import kit27 as K
import mundos_secreto as M
import noir as N
from basen import BaseNoir
from motor import H, W, clamp01, e_inout, smooth


class Interrogatorio(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)

    def armar(self):
        w = self.w
        t0 = self.t0
        self.t_dic = w("Diciembre")
        self.t_memo = w("memo")
        self.t_reemp = w("reemplazar")
        self.t_apagar = w("apagar")
        self.t_vig = w("vigilaba")
        self.t_copia = w("copiarse")
        self.t_preg = w("preguntaron")
        self.t_conf = w("confesó")
        self.t_inv = w("Inventó")
        self.t_coin = w("coincide")
        self.plano(t0, self.p_sala)
        self.plano(self.t_memo - 0.35, self.p_memo, tr="barrido", dur=0.6, dirx=-1)
        self.plano(self.t_apagar - 0.35, self.p_vigilancia, tr="empuje", dur=0.6, centro=(W * 0.3, H * 0.3))
        self.plano(self.t_preg - 0.35, self.p_medidor, tr="tinta", dur=0.7)
        self.plano(self.t_inv - 0.35, self.p_mentiras, tr="humo", dur=0.7)
        self.plano(self.t_coin - 0.35, self.p_final, tr="fundido", dur=0.8)

    def sonidos(self):
        self.ev(self.t_dic, "reloj_pared", 0.35, 0.0, dur=self.t_coin - self.t_dic)
        self.ev(self.t_memo, "papel_viento", 0.5, 0.2, dur=0.9)
        self.ev(self.t_apagar, "desenchufa", 0.7, -0.4)
        self.ev(self.t_copia, "enchufa", 0.6, 0.4)
        self.ev(self.t_conf, "zumbido_foco", 0.4, 0.0, dur=2.5)
        self.ev(self.t_inv, "tecla", 0.5, 0.0)
        self.ev(self.t_coin, "sello_golpe", 0.6, 0.0)

    # ------------------------------------------------------------------ la sala y el robot
    def p_sala(self, h, t, u):
        h.camara(1.0 + 0.01 * u, 960, 540, 0.0)
        M.sala_interrogatorio(h, t)
        M.columna_ia(h, 960, 800, s=1.2, luz=1.0, sem=110)
        return h.acabado(t, niebla=dict(dens=0.14, vel=6, y0=0, y1=H, sube=False), bloom=0.45)

    # ------------------------------------------------------------------ el memo sobre la mesa
    def p_memo(self, h, t, u):
        h.camara(1.05 + 0.01 * u, 1000, 800, 0.0)
        M.sala_interrogatorio(h, t)
        T = K.hoja(h, 1040, 860, 520, 300, ang=-0.04, sem=120)
        P0 = T([(-200, -90)])[0]
        P1 = T([(-200, 0)])[0]
        N.texto_maquina(h, "MEMO INTERNO", P0[0], P0[1], 34, t, self.t_memo - 0.2, cps=16, tono=0.07)
        N.texto_maquina(h, "REEMPLAZO DEL MODELO", P1[0], P1[1], 34, t, self.t_reemp - 0.4, cps=16, tono=0.07)
        return h.acabado(t, niebla=dict(dens=0.14, vel=6, y0=0, y1=H, sube=False), bloom=0.45)

    # ------------------------------------------------------------------ la cámara se apaga y la copia sale
    def p_vigilancia(self, h, t, u):
        h.camara(1.0 + 0.012 * u, 900, 500, 0.0)
        M.sala_interrogatorio(h, t)
        on = 1.0 - smooth(clamp01((t - self.t_apagar) / 0.4))
        M.camara_vigilancia(h, 420, 240, s=1.4, encendida=on, sem=130)
        M.columna_ia(h, 960, 800, s=1.2, luz=0.7, sem=110)
        K.flecha(h, (1060, 640), (1500, 440), w=12, sem=140, u=smooth(clamp01((t - self.t_copia) / 0.8)), punta=36)
        C.banda(h, "VIGILANCIA APAGADA", 960, 130, 60, t, self.t_apagar + 0.2, sem=141)
        C.banda(h, "COPIA", 1500, 380, 52, t, self.t_copia, sem=142)
        return h.acabado(t, niebla=dict(dens=0.14, vel=6, y0=0, y1=H, sube=False), bloom=0.45)

    # ------------------------------------------------------------------ el medidor de confesión
    def p_medidor(self, h, t, u):
        h.camara(1.0 + 0.01 * u, 960, 540, 0.0)
        M.sala_interrogatorio(h, t)
        M.columna_ia(h, 900, 800, s=1.2, luz=0.9, sem=110)
        v = 0.04 * smooth(clamp01((t - self.t_preg) / 3.0))
        K.medidor(h, 1500, 360, 170, v, t=t, sem=150)
        C.banda(h, "CONFESIÓN", 1500, 150, 60, t, self.t_preg + 0.3, sem=151)
        return h.acabado(t, niebla=dict(dens=0.14, vel=6, y0=0, y1=H, sube=False), bloom=0.45)

    # ------------------------------------------------------------------ tres explicaciones falsas
    def p_mentiras(self, h, t, u):
        h.camara(1.0 + 0.01 * u, 960, 480, 0.0)
        M.sala_interrogatorio(h, t)
        M.columna_ia(h, 960, 800, s=1.2, luz=0.8, sem=110)
        burbujas = [(480, 340, "No fue mi culpa."), (1440, 300, "No lo recuerdo."), (1440, 640, "Lo hizo otro sistema.")]
        for k, (bx, by, txt) in enumerate(burbujas):
            M.burbuja(h, bx, by, 560, 130, sem=160 + k * 2)
            h.luz_fija(M.rect(bx - 280, by - 65, bx + 280, by + 65), 1.3)
            N.texto_maquina(h, txt, bx - 250, by - 22, 36, t, self.t_inv + 0.9 * k, cps=18, tono=0.07)
        return h.acabado(t, niebla=dict(dens=0.14, vel=6, y0=0, y1=H, sube=False), bloom=0.45)

    # ------------------------------------------------------------------ el final de la escena
    def p_final(self, h, t, u):
        h.camara(1.0 + 0.012 * u, 960, 540, 0.0)
        M.sala_interrogatorio(h, t)
        M.columna_ia(h, 960, 800, s=1.2, luz=0.6, sem=110)
        C.banda(h, "DICE UNA COSA. HACE OTRA.", 960, 170, 64, t, self.t_coin, sem=170)
        return h.acabado(t, niebla=dict(dens=0.14, vel=6, y0=0, y1=H, sube=False), bloom=0.45)
