# -*- coding: utf-8 -*-
"""«La historia de España en 5 minutos» — mapa con relieve real pintado a guache + dibujos de boceto, plano secuencia (sin cortes).

Una sola clase (`Mundo`) dibuja todo en función del tiempo global: la cámara vuela por el mapa (rejilla "eu" para la península y
Europa, "am" para América y el Pacífico, con fundido entre ambas mientras la cámara se aleja), los reinos crecen, se parten y se reúnen
(varias capas a la vez: la Reconquista), y los personajes/objetos aparecen como pegatinas de boceto sobre el guache.
La coreografía por épocas está en `coreo_1.py` … `coreo_4.py`; aquí solo el ensamblado.
"""
import math

import cv2
import numpy as np

import boceto as B
import config
import mapa as M
import sellos as SE
from core import (CamPath, TOTAL, Territorio, dibujar_actor, dibujar_subs, estampar, kf, pintar_celdas, contornos_tinta, rotulo)
from escena_base import Escena, TL
from motor import H, W, e_back, e_in, e_inout, e_out, lerp, prog
from reg import Reg

# la "vida" (respiración y ondulación de los dibujos) usa ciclos enteros en la duración total
B.OMEGA = 2 * math.pi * round(TOTAL / 1.85) / TOTAL

M.cargar()
R = Reg()
import coreo_1, coreo_2, coreo_3, coreo_4  # noqa: E402,F401  (registran en R)

for _c in (coreo_1, coreo_2, coreo_3, coreo_4):          # primero los barridos dentro de escena (afectan a cuándo desaparece cada cosa)
    _c.cortes(R)
for _c in (coreo_1, coreo_2, coreo_3, coreo_4):
    _c.construir(R)


def _puentes(a):
    """Entre escenas el contador de años se queda quieto y rueda rápido justo antes de la siguiente (sin pasar minutos por números absurdos)."""
    a = sorted(a)
    out = [a[0]]
    for (t0, v0), (t1, v1) in zip(a, a[1:]):
        if t1 - t0 > 1.6 and v1 != v0:
            out.append((t1 - 0.6, v0))
        out.append((t1, v1))
    return out


R.anios[:] = _puentes(R.anios)
SELLOS = sorted(R.sellos, key=lambda s: s["t"])
N_SELLOS = max(1, len(SELLOS))
CAM = CamPath(R.cam)
CAPAS = {k: Territorio(v) for k, v in R.terr.items()}
ACTORES = sorted(enumerate(R.actores), key=lambda p: (p[1].z, p[0]))
ACTORES = [a for _, a in ACTORES]


# ------------------------------------------------------------------ contador de años (arriba a la izquierda)
def texto_anio(v):
    v = int(round(v))
    if v <= -10000:
        return f"hace {(-v) // 1000:,} mil años".replace(",", ".") if -v < 1_000_000 else "hace 1 millón de años"
    return f"{-v} a. C." if v < 0 else (f"{v} d. C." if v < 1000 else f"{v}")


def estado_cam(t, w):
    """Cámara del cuadro: se limita a la rejilla "eu" solo cuando no hay nada de "am" (así las dos rejillas casan en el fundido)."""
    M.usar("am" if w > 0 else "eu")
    return CAM.estado(t)


def cobertura(cam):
    """Qué parte de la pantalla cae dentro del mapa de la rejilla de `cam` (1 = hay mapa, 0 = fuera; borde que se desvanece en ~80 px hacia dentro).
    Fuera de su borde la rejilla solo tiene papel y mar liso (la de Europa abarca 43° de longitud): durante un fundido entre
    rejillas, ahí tiene que verse la otra, o se ve el rectángulo del mapa flotando sobre el vacío."""
    rej, k = cam.rej, 8
    chico = np.ones((rej.FH // k, rej.FW // k), np.float32)
    Mk = cam.M.copy()
    Mk[:, :2] *= k                                    # px del mapa reducido -> px de la rejilla -> pantalla
    m = cv2.warpAffine(chico, Mk, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0.0)
    m = cv2.GaussianBlur(m, (0, 0), 40)
    m = np.clip((m - 0.5) * 2.0, 0.0, 1.0)            # 0 justo en el borde real; llega a 1 unos 80 px dentro: sin costura
    return m * m * (3.0 - 2.0 * m)


def fondo_rejilla(nombre, st, t, fs):
    """Fondo pintado de una rejilla: mar y tierra con relieve, territorios (capas), ríos, pinceladas, nombres de mares.
    Devuelve (img, cam, [S de cada territorio] para la tinta)."""
    M.usar(nombre)
    cam = M.Cam(*st)
    img, base = M.pintar_base(cam, fs)
    formas = []
    for (rej, capa), terr in sorted(CAPAS.items(), key=lambda kv: kv[0][1]):
        if rej != nombre:
            continue
        S_campo, color = terr.estado(t)
        if S_campo is None:
            continue
        fr = None
        for f in R.frac:
            if f.rej == nombre and f.capa == capa and f.g(t) > 0:
                fr = f
                break
        if fr is not None:
            S = pintar_celdas(img, cam, S_campo, fr, t, fr.g(t), fs, color, luz=base.luz)
            formas.append((S, False))
            continue
        S = cam.proyectar(S_campo)
        M.pintar(img, S, color, 1.0, fs, luz=base.luz)
        formas.append((S, True))
    M.pintar_rios(img, cam, base, t)
    for rej, f in R.fondo:
        if rej is None or rej == nombre:
            f(img, cam, t, fs)
    for txt, lon, lat, px, alfa, rot in R.mares[nombre]:
        M.rotulo_mapa(img, txt, cam, lon, lat, px, alfa, rot=rot)
    return img, cam, formas


SX, SY = 1720, 700          # donde se estampa grande el sello de época (abajo a la derecha: casi siempre es mar)


class Mundo(Escena):
    def preparar(self):
        self.h = B.Hoja()
        self.hf = B.Hoja()
        M.cargar()
        self.fs = 0
        self.te = 0.0
        if self.idx == 0:
            for t, n, vol, pan, kw in R.sonidos:
                self.ev(t, n, vol, pan, **kw)
            for a in ACTORES:
                for t, n, vol, kw in a.snd:
                    self.ev(t, n, vol, **kw)

    # ---- sellos de época: se estampa grande y luego vuela a su casilla de la fila superior
    def sellos(self, h, t, fs):
        for k, s in enumerate(SELLOS):
            a = t - s["t"]
            if a < 0:
                continue
            slot = (1862 - 76 * (N_SELLOS - 1 - k), 62)
            if a < 2.2:                                   # grande, a la derecha
                if a < 0.14:
                    continue
                px = lerp(300, 170, e_out(prog(a, 0.0, 0.3)))
                x, y = SX, SY
                SE.estampar(h, s["ch"], x, y, px, -0.08, s["color"], desgaste=0.06, semilla=k)
                if a > 0.25:
                    u = prog(a, 0.25, 0.8)
                    wl = B.ancho_texto(s["nombre"], 52) + 20
                    rotulo(h, s["nombre"], min(x, W - 34 - wl / 2), y + 134, 52, u, fs, 255, self.te)
            elif a < 3.0:                                 # vuela a su casilla
                u = e_inout(prog(a, 2.2, 3.0))
                px = lerp(170, 60, u)
                SE.estampar(h, s["ch"], lerp(SX, slot[0], u), lerp(SY, slot[1], u), px, -0.08 * (1 - u), s["color"], 0.0, k)
            else:
                SE.estampar(h, s["ch"], slot[0], slot[1], 60, 0.0, s["color"], 0.0, k)

    def anios(self, h, t, fs):
        if not R.anios:
            return
        v = kf(t, R.anios)
        ini = R.anios[0][0]
        if t < ini - 0.2:
            return
        u = prog(t, ini - 0.2, ini + 0.4)
        txt = texto_anio(v)
        rotulo(h, txt, 40 + B.ancho_texto(txt, 76) / 2, 64, 76, u, fs, 255, self.te)

    # ---- cuadro
    def render(self, lz, t):
        h = self.h
        h.limpiar()
        self.te = t
        self.fs = B.fase(t)
        fs = self.fs
        w = R.peso_am(t)
        st = estado_cam(t, w)
        if w <= 0.0 or w >= 1.0:
            img, cam, formas = fondo_rejilla("am" if w >= 1.0 else "eu", st, t, fs)
            tintas = [(formas, 255)]
        else:                                             # fundido entre rejillas (la cámara se aleja o se acerca)
            img_e, cam_e, f_e = fondo_rejilla("eu", st, t, fs)
            img_a, cam, f_a = fondo_rejilla("am", st, t, fs)
            wp = np.maximum(w, 1.0 - cobertura(cam_e))[..., None]     # donde "eu" no tiene mapa, manda "am"
            img = img_e * (1 - wp) + img_a * wp
            tintas = [(f_e, int(255 * (1 - w))), (f_a, int(255 * w))]
            if w < 0.5:
                M.usar("eu")
                cam = cam_e
        # tinta del mapa (fronteras y rutas) en su propia hoja: queda DEBAJO de las pegatinas y los rótulos
        hf = self.hf
        hf.limpiar()
        hf.fondo = img
        if R.tinta_terr:
            for formas, v in tintas:
                for k, (S, tinta) in enumerate(formas):
                    if tinta:                              # la fractura no lleva contorno (las celdas se mueven)
                        contornos_tinta(hf, S, fs, 3 + k, 4.6, v=v)
        for f in R.fondo_tinta:
            f(hf, cam, t, fs, t)
        h.fondo = hf.componer()
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
