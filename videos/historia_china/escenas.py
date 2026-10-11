# -*- coding: utf-8 -*-
"""«La historia de China en 3 minutos» — mapa pintado a guache + dibujos de boceto, plano secuencia (sin cortes).

Una sola clase (`Mundo`) dibuja todo en función del tiempo global: la cámara vuela por el mapa, el imperio crece, se parte
y se reúne (campos de distancia interpolados), y los personajes/objetos aparecen como pegatinas de boceto sobre el guache.
La coreografía por épocas está en `coreo1.py` … `coreo3.py`; aquí solo el ensamblado.
"""
import math

import numpy as np

import boceto as B
import config
import mapa as M
from core import (CamPath, TOTAL, Territorio, dibujar_actor, dibujar_subs, estampar, kf, pintar_celdas, contornos_tinta, rotulo)
from escena_base import Escena, TL
from motor import H, W, e_back, e_in, e_inout, e_out, lerp, prog
from reg import Reg

# la "vida" (respiración y ondulación de los dibujos) usa ciclos enteros en la duración total
B.OMEGA = 2 * math.pi * round(TOTAL / 1.85) / TOTAL

R = Reg()
import coreo1, coreo2, coreo3  # noqa: E402,F401  (registran en R)

coreo1.construir(R)
coreo2.construir(R)
coreo3.construir(R)

SELLOS = sorted(R.sellos, key=lambda s: s["t"])
N_SELLOS = max(1, len(SELLOS))
CAM = CamPath(R.cam)
TERR = Territorio(R.terr)
ACTORES = sorted(enumerate(R.actores), key=lambda p: (p[1].z, p[0]))
ACTORES = [a for _, a in ACTORES]


# ------------------------------------------------------------------ contador de años (arriba a la izquierda)
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

    # ---- territorio
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

    # ---- sellos de dinastía: se estampa grande y luego vuela a su casilla de la fila superior
    def sellos(self, h, t, fs):
        for k, s in enumerate(SELLOS):
            a = t - s["t"]
            if a < 0:
                continue
            slot = (1868 - 74 * (N_SELLOS - 1 - k), 58)
            if a < 2.2:                                   # grande, en el centro-derecha
                v = prog(a, 0.0, 0.32)
                px = lerp(330, 170, e_out(v)) if a < 0.4 else 170
                if a < 0.3:
                    px = lerp(300, 175, e_out(prog(a, 0, 0.3)))
                x, y = 1660, 250
                rot = -0.08
                if a < 0.14:
                    continue
                estampar(h, s["ch"], x, y, px, rot, s["color"], desgaste=0.06, semilla=k)
                if a > 0.25:
                    u = prog(a, 0.25, 0.8)
                    rotulo(h, s["nombre"], x, y + 130, 66, u, fs, 255, self.te)
            elif a < 3.0:                                 # vuela a su casilla
                u = e_inout(prog(a, 2.2, 3.0))
                px = lerp(175, 56, u)
                estampar(h, s["ch"], lerp(1660, slot[0], u), lerp(250, slot[1], u), px, -0.08 * (1 - u), s["color"], 0.0, k)
            else:
                estampar(h, s["ch"], slot[0], slot[1], 56, 0.0, s["color"], 0.0, k)

    def anios(self, h, t, fs):
        if not R.anios:
            return
        v = kf(t, R.anios)
        ini = R.anios[0][0]
        if t < ini - 0.2:
            return
        u = prog(t, ini - 0.2, ini + 0.4)
        rotulo(h, texto_anio(v), 168, 62, 76, u, fs, 255, self.te)

    # ---- cuadro
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
        self.sellos(h, t, fs)
        if config.SUBTITULOS:
            dibujar_subs(h, t, fs)
        out = np.clip(h.componer(), 0, 1)
        for tr in R.trans:
            if tr.activa(t):
                tr.aplicar(out, t, fs)
        return out


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
