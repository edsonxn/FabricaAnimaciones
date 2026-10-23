# -*- coding: utf-8 -*-
"""«La historia de Jalisco en 5 minutos» (22-oct-2026; kit de historia_mexico + pegatinas de Flow vía pegflow.py) — mapa con relieve real pintado a guache + dibujos de boceto, plano secuencia.

Kit v2.1 con UNA rejilla ("mx", de Alta California y Texas a Costa Rica y el Caribe). Una sola clase (`Mundo`) dibuja todo en
función del tiempo global: la cámara vuela por el mapa, los señoríos, virreinatos y repúblicas crecen, se parten y se reúnen,
el cinturón verde mesoamericano y los valles fértiles se ven bajo los territorios, el lago de Texcoco brilla en el mundo prehispánico
y los personajes y objetos aparecen como pegatinas de boceto. La coreografía por épocas está en `coreo_1.py` … `coreo_4.py`.
"""
import math

import numpy as np

import boceto as B
import config
import mapa as M
import sellos as SE
from core import (CamPath, TOTAL, Territorio, dibujar_actor, dibujar_subs, kf, pintar_celdas, contornos_tinta, rotulo)
from escena_base import Escena, TL
from motor import H, W, e_back, e_in, e_inout, e_out, lerp, prog
from reg import Reg

# la "vida" (respiración y ondulación de los dibujos) usa ciclos enteros en la duración total
B.OMEGA = 2 * math.pi * round(TOTAL / 1.85) / TOTAL

M.cargar()
M.usar("mx")
R = Reg()
import crono_ubicacion  # noqa: E402
try:                    # ubicación en México (apertura con México entero, estado con fronteras y minimapa, región): guion.UBICACION
    import guion as _G
    _UBIC = getattr(_G, "UBICACION", None)
except Exception:       # noqa: BLE001
    _UBIC = None
R.ubic = crono_ubicacion.Ubicacion(M, **_UBIC) if _UBIC else None    # en la coreografía: R.ubic.apertura/estado/region(t0, t1)
import importlib  # noqa: E402
import traceback  # noqa: E402

_COREOS = []
for _n in ("coreo_1", "coreo_2", "coreo_3", "coreo_4"):   # cada tramo en su archivo; uno roto no tumba a los demás (avisa)
    try:
        _COREOS.append(importlib.import_module(_n))
    except Exception:                                     # noqa: BLE001
        print(f"⚠ {_n} no carga: {traceback.format_exc(limit=3)}", flush=True)
for _c in _COREOS:          # primero los barridos dentro de escena (afectan a cuándo desaparece cada cosa)
    _c.cortes(R)
for _c in _COREOS:
    try:
        _c.construir(R)
    except Exception:                                     # noqa: BLE001
        print(f"⚠ {_c.__name__}.construir falla: {traceback.format_exc(limit=4)}", flush=True)


def _puentes(a):
    """Entre escenas el contador de años se queda quieto y rueda rápido justo antes de la siguiente (sin pasar minutos por números absurdos)."""
    a = sorted(a)
    if not a:
        return a
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
if R.ubic:
    R.ubic.cam_fn = CAM.estado
    for _t0, _t1, _c, _n in R.ubic.cajas_ocupadas():      # cartela y minimapa entran al control de choques
        R.cajas.append((_t0, _t1, lambda t, cam, c=_c: c, _n))
CAPAS = {k: Territorio(v) for k, v in R.terr.items()}
ACTORES = sorted(enumerate(R.actores), key=lambda p: (p[1].z, p[0]))
ACTORES = [a for _, a in ACTORES]
ALFA_TERR = 0.86            # los territorios dejan ver el cinturón verde y el relieve
CAPAS_AGUA = (50,)          # capas que son agua (lago de Texcoco): opacas y sin contorno de frontera


# ------------------------------------------------------------------ contador de años (arriba a la izquierda)
def texto_anio(v):
    v = int(round(v))
    if v <= -10000:
        return f"hace {(-v) // 1000:,} mil años".replace(",", ".")
    return f"{-v} a. C." if v < 0 else (f"{v} d. C." if v < 1000 else f"{v}")


def estado_cam(t, w=0.0):
    M.usar("mx")
    st = CAM.estado(t)
    return R.ubic.camara(t, st) if R.ubic else st


def fondo(st, t, fs):
    """Fondo pintado: mar y tierra con relieve y cinturón verde, territorios (capas), ríos, rutas pintadas y nombres de mares/regiones.
    Devuelve (img, cam, [(S de cada territorio, lleva tinta)])."""
    cam = M.Cam(*st)
    img, base = M.pintar_base(cam, fs)
    alfa_terr = ALFA_TERR - 0.46 * min(1.0, max(0.0, (cam.z - 2.2) / 3.3))   # Jalisco: z 1.8-4.5 (rejilla de 260 px/°)     # de cerca manda el paisaje; el reino solo lo tiñe
    formas = []
    for (rej, capa), terr in sorted(CAPAS.items(), key=lambda kv: kv[0][1]):
        S_campo, color = terr.estado(t)
        if S_campo is None:
            continue
        fr = None
        for f in R.frac:
            if f.capa == capa and f.g(t) > 0:
                fr = f
                break
        if fr is not None:
            S = pintar_celdas(img, cam, S_campo, fr, t, fr.g(t), fs, color, luz=base.luz)
            formas.append((S, False))
            continue
        S = cam.proyectar(S_campo)
        if capa in CAPAS_AGUA:
            M.pintar(img, S, color, 1.0, fs, borde=0.5, sombra=0.12, luz=None)
            continue
        M.pintar(img, S, color, alfa_terr, fs, luz=base.luz)
        formas.append((S, True))
    M.pintar_rios(img, cam, base, t)
    for rej, f in R.fondo:
        f(img, cam, t, fs)
    for txt, lon, lat, px, alfa, rot, col in R.mares["mx"]:
        M.rotulo_mapa(img, txt, cam, lon, lat, px, alfa, color=col, rot=rot)
    if R.ubic:
        img = R.ubic.componer(img, cam, t)
    return img, cam, formas


SX, SY = 1720, 760          # donde se estampa grande el sello de época (abajo a la derecha)
PASO_SELLO = 72


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
            slot = (1868 - PASO_SELLO * (N_SELLOS - 1 - k), 60)
            if a < 2.2:
                if a < 0.14:
                    continue
                px = lerp(300, 170, e_out(prog(a, 0.0, 0.3)))
                x, y = SX, SY
                SE.estampar(h, s["ch"], x, y, px, -0.08, s["color"], desgaste=0.06, semilla=k)
                if a > 0.25:
                    u = prog(a, 0.25, 0.8)
                    wl = B.ancho_texto(s["nombre"], 50) + 20
                    rotulo(h, s["nombre"], min(x, W - 34 - wl / 2), y + 132, 50, u, fs, 255, self.te)
            elif a < 3.0:
                u = e_inout(prog(a, 2.2, 3.0))
                px = lerp(170, 56, u)
                SE.estampar(h, s["ch"], lerp(SX, slot[0], u), lerp(SY, slot[1], u), px, -0.08 * (1 - u), s["color"], 0.0, k)
            else:
                SE.estampar(h, s["ch"], slot[0], slot[1], 56, 0.0, s["color"], 0.0, k)

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
        st = estado_cam(t)
        img, cam, formas = fondo(st, t, fs)
        # tinta del mapa (fronteras y rutas) en su propia hoja: queda DEBAJO de las pegatinas y los rótulos
        hf = self.hf
        hf.limpiar()
        hf.fondo = img
        if R.tinta_terr:
            vt = int(255 * (1.0 - 0.6 * min(1.0, max(0.0, (cam.z - 2.2) / 3.3))))
            for k, (S, tinta) in enumerate(formas):
                if tinta:
                    contornos_tinta(hf, S, fs, 3 + k, 4.6, v=vt)
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
