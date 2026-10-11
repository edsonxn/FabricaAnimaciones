# -*- coding: utf-8 -*-
"""«La historia de Roma en 5 minutos» — mapa pintado a guache + boceto, plano secuencia continuo."""
import math

import numpy as np

import boceto as B
import config
import mapa as M
from core import (CamPath, TOTAL, Territorio, dibujar_actor, dibujar_subs, estampar, kf, pintar_celdas, contornos_tinta, rotulo)
from escena_base import Escena, TL
from motor import H, W, e_back, e_in, e_inout, e_out, lerp, prog
from reg import Reg

B.OMEGA = 2 * math.pi * round(TOTAL / 1.85) / TOTAL

R = Reg()
import coreo_r1
import coreo_r2
import coreo_r3

coreo_r1.construir(R)
coreo_r2.construir(R)
coreo_r3.construir(R)

CAM = CamPath(R.cam)
TERR = Territorio(R.terr)
ACTORES = sorted(enumerate(R.actores), key=lambda p: (p[1].z, p[0]))
ACTORES = [a for _, a in ACTORES]


def texto_anio(v):
    v = int(round(v))
    return f"{-v} a. C." if v < 0 else f"{v} d. C."


class Mundo(Escena):
    def preparar(self):
        self.h = B.Hoja()
        M.cargar()
        self.fs = 0
        self.te = 0.0
        if self.idx == 0:
            for t, n, vol, pan, kw in R.sonidos:
                self.ev(t, n, vol, pan, **kw)
            for a in ACTORES:
                for t, n, vol, kw in a.snd:
                    self.ev(t, n, vol, **kw)

    def territorio(self, img, cam, t):
        S_campo, color = TERR.estado(t)
        if S_campo is None:
            return None
        fr = None
        for f in R.frac:
            if f.g(t) > 0:
                fr = f
                break
        if fr is not None:
            g = fr.g(t)
            pintar_celdas(img, cam, S_campo, fr, t, g, self.fs, color)
            return None
        S = cam.proyectar(S_campo)
        M.pintar(img, S, color, 1.0, self.fs)
        return S

    def anios(self, h, t, fs):
        if not R.anios:
            return
        v = kf(t, R.anios)
        ini = R.anios[0][0]
        if t < ini - 0.2:
            return
        u = prog(t, ini - 0.2, ini + 0.4)
        rotulo(h, texto_anio(v), 168, 62, 76, u, fs, 255, self.te)

    def render(self, lz, t):
        h = self.h
        h.limpiar()
        self.te = t
        self.fs = B.fase(t)
        fs = self.fs
        cam = CAM.cam_en(t)
        img = M.fondo_base()
        M.pintar_tierra(img, cam, fs)
        S = self.territorio(img, cam, t)
        for f in R.fondo:
            f(img, cam, t, fs)
        h.fondo = img
        if S is not None and R.tinta_terr:
            contornos_tinta(h, S, fs, 3, 5.0)
        for a in ACTORES:
            dibujar_actor(h, a, t, cam, fs, t)
        for f in R.frente:
            f(h, cam, t, fs, t)
        self.anios(h, t, fs)
        if config.SUBTITULOS:
            dibujar_subs(h, t, fs)
        out = np.clip(h.componer(), 0, 1)
        for tr in R.trans:
            if tr.activa(t):
                tr.aplicar(out, t, fs)
        return out


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
