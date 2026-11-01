# -*- coding: utf-8 -*-
"""«El llamado del Mixtón» — película animada tipo novela (~15 min), estilo PEGATINA FLOW CINEMATOGRÁFICO (nucleo/pegaflow.py,
docs/estilo_pegatina_flow.md): escenarios de Flow con cámara y parallax por profundidad; personajes, ciclos y utilería de las hojas
de Flow animados como pegatinas; franjas de cine, capítulos de novela en papel y ambiente continuo (fuego, humo, polvo, lluvia,
flechas, piedras). Guion y voces: guion.py · mapa número → pose de cada pieza: ESTADO.md.
Tomas con PREFIJO PROPIO por escena (nombres únicos; comprobación AST antes de renderizar, docs §8)."""
import functools
import math

import cv2
import numpy as np
from PIL import Image, ImageDraw

import pegaflow as PF
import docu as D
from escena_base import Escena, TL
from motor import W, H, clamp01, e_inout, lerp, prog, smooth

TOTAL = TL["total"]
_ESC = {e["id"]: e for e in TL["escenas"]}


def T(eid, pref, frase=None, n=0, fin=False):
    return PF.T(TL, eid, pref, frase, n, fin)


def t0_(eid):
    return _ESC[eid]["t0"]


def t1_(eid):
    return _ESC[eid]["t1"]


# ------------------------------------------------------------------ luz de cada lugar sobre las pegatinas
NOCHE = (0.56, 0.62, 0.92)
FOGATA = (1.04, 0.78, 0.60)
NOCHE_FUEGO = (0.80, 0.66, 0.72)
ALBA = (0.98, 0.88, 0.92)
DORADO = (1.08, 0.94, 0.78)
MEDIODIA = (1.04, 1.0, 0.94)
OCASO = (1.08, 0.80, 0.66)
INCENDIO = (1.10, 0.70, 0.52)
LLUVIA = (0.76, 0.82, 0.90)
INTERIOR = (1.0, 0.80, 0.64)
AZUL = (0.70, 0.78, 1.0)
SOL_DURO = (1.10, 1.02, 0.88)

SFX = []
AMB = []          # ambientes grabados de la biblioteca (t0, t1, archivo de sfx/, vol) → _fx_ambiente.py → audio/fx.wav


def snd(t, n, v=1.0, **kw):
    SFX.append((t, n, v, kw))


# ------------------------------------------------------------------ ayudantes de toma (receta de jalpa / wow_darrowshire)
# Hacia dónde MIRA cada pieza tal como la pintó Flow (+1 derecha, −1 izquierda): lo que se desplaza mira a donde va.
MIRA = {}


def rumbo(pieza, x0, x1, flip):
    m = MIRA.get(pieza)
    if m is None and "/ciclo_" not in pieza and any(k in pieza for k in PF.CICLO_PAL):
        m = 1                                   # los ciclos se pidieron mirando a la derecha
    if m is None or abs(x1 - x0) < 1e-6:
        return flip
    return (x1 - x0) * m < 0


def alto(y, hz, k):
    """Altura relativa (al escenario) de un adulto con los pies en y, con el horizonte en hz (perspectiva)."""
    return max(0.02, k * (y - hz))


def quieto(lz, pl, t, pieza, x, y, frac, flip=False, op=1.0, tono=None, capa=1.0, fase=0.0, t_in=None, t_out=None, rot=0.0):
    if t_in is not None:
        if t < t_in:
            return
        u = PF.entra(t, t_in, 0.4)
    else:
        u = 1.0
    if t_out is not None:
        if t > t_out + 0.4:
            return
        op *= 1.0 - smooth(prog(t, t_out, t_out + 0.35))
    X, Y, h = pl.en(t, x, y, frac, capa)
    PF.actor(lz, pieza, X, Y, h * (0.6 + 0.4 * u), flip=flip, op=op * clamp01(u * 4), tono=tono,
             sy=PF.respira(t, fase=fase), rot=rot + (1 - u) * 8)


def poses(lz, pl, t, cambios, x, y, frac, tono=None, fase=0.0, op=1.0):
    """Personaje en un sitio que cambia de pose: cambios = [(t_i, pieza, flip, escala)]; el que sale se va antes del que entra."""
    act = None
    for c in cambios:
        if c[0] <= t:
            act = c
    if act is None:
        return
    t_i, pieza, fl, k = act
    u = 1.0 if t_i == cambios[0][0] else PF.entra(t, t_i, 0.25)
    X, Y, h = pl.en(t, x, y, frac * k)
    PF.actor(lz, pieza, X, Y, h * (0.92 + 0.08 * u), flip=fl, tono=tono, sy=PF.respira(t, fase=fase), rot=(1 - u) * 4, op=op)


def paseo(lz, pl, t, pieza, ta, tb, x0, x1, y, frac, flip=False, tono=None, pasos=2.2, capa=1.0, op=1.0, y1=None,
          desde_antes=True, hasta_despues=True, salto=0.035):
    if (t < ta and not desde_antes) or (t > tb and not hasta_despues):
        return
    flip = rumbo(pieza, x0, x1, flip)
    u = clamp01((t - ta) / max(tb - ta, 1e-3))
    x, yy = lerp(x0, x1, u), lerp(y, y1 if y1 is not None else y, u)
    X, Y, h = pl.en(t, x, yy, frac, capa)
    mov = ta < t < tb
    ph = (t - ta) * pasos * math.pi
    bote = abs(math.sin(ph)) if mov else 0.0
    rot = 3.0 * math.sin(ph) if mov else 0.0
    PF.actor(lz, pieza, X, Y - bote * salto * h, h, flip=flip, tono=tono, rot=rot, op=op, sy=PF.respira(t))


def anda(lz, pl, t, ciclo, ta, tb, x0, x1, y, frac, paso=0.95, flip=False, tono=None, capa=1.0, op=1.0, desde_antes=False,
         y1=None, hasta_despues=True):
    if t < ta and not desde_antes:
        return
    if t > tb + 0.05 and (not hasta_despues or x1 < -0.1 or x1 > 1.1):
        return
    flip = rumbo(ciclo, x0, x1, flip)
    u = clamp01((t - ta) / max(tb - ta, 1e-3))
    x = lerp(x0, x1, u)
    yy = lerp(y, y1 if y1 is not None else y, u)
    X, Y, h = pl.en(t, x, yy, frac, capa)
    n = PF.ciclo_n(ciclo)
    dist = abs(x - x0) * pl.ancho_mundo(t)
    i = PF.cuadro_ciclo(dist, paso * h, n) if ta < t < tb else 0
    PF.actor(lz, f"{ciclo}/ciclo_{i:02d}", X, Y, h * 1.25, flip=flip, tono=tono, op=op)


def tropa(lz, pl, t, ciclo, ta, tb, x0, x1, y, frac, n=6, dx=0.06, dy=0.012, paso=1.0, flip=False, tono=None, sem=0,
          desde_antes=True):
    """Columna de n figuras con el mismo ciclo, desfasadas (marcha, carga, columna de cargadores): lejos primero."""
    rng = np.random.RandomState(sem)
    off = [(i * dx + rng.uniform(-0.01, 0.01), rng.uniform(-dy, dy), rng.uniform(0.92, 1.06)) for i in range(n)]
    off.sort(key=lambda o: o[1])
    sgn = 1 if x1 >= x0 else -1
    for ox, oy, k in off:
        anda(lz, pl, t, ciclo, ta, tb, x0 - sgn * ox, x1 - sgn * ox, y + oy, frac * k * (1 + oy * 2), paso=paso, flip=flip,
             tono=tono, desde_antes=desde_antes)


def pega(lz, pieza, X, Y, hpx, t, t_in, t_out=None, rot=0.0, tono=None, flip=False, salida=0.35, op=1.0):
    """Pegatina en coordenadas de PANTALLA (centro en X, Y): se pega con rebote en t_in y se despega en t_out; flota un poco."""
    if t < t_in:
        return
    u = PF.entra(t, t_in, 0.45)
    o = op if t_out is None else op * (1.0 - smooth(prog(t, t_out, t_out + salida)))
    if o <= 0.01:
        return
    PF.actor(lz, pieza, X, Y + 4 * math.sin(1.3 * t + t_in), hpx * (0.6 + 0.4 * u), rot=rot + (1 - u) * 10 + 0.8 * math.sin(1.1 * t),
             op=o * clamp01(u * 4), ancla=(0.5, 0.5), suelo=0, tono=tono, flip=flip)


def plantas(lz, pl, t, lista, tono=None):
    """Primer plano (capa > 1) en coordenadas de pantalla: [(pieza, x, y, frac de alto de pantalla, capa, flip)]; se mece."""
    for k, (pz, x, y, frac, capa, fl) in enumerate(lista):
        X, Y, h = pl.fg(t, x, y, frac, capa)
        PF.actor(lz, pz, X, Y, h, flip=fl, rot=1.4 * math.sin(1.1 * t + k * 1.9), suelo=0, tono=tono)


def aves(lz, t, vuelos, tono=None, ciclo="c09_zopilote_aleteo"):
    """vuelos: [(t_ini, dur, y0, y1, alto px, sentido, fase)] en pantalla; aleteo a 7 cuadros/s (zopilote: planea)."""
    n = PF.ciclo_n(ciclo)
    for t_i, dur, y0, y1, hpx, sent, fa in vuelos:
        u = (t - t_i) / dur
        if not 0 <= u <= 1:
            continue
        x = lerp(-0.08, 1.08, u) if sent > 0 else lerp(1.08, -0.08, u)
        y = lerp(y0, y1, u) + 0.014 * math.sin(t * 1.4 + fa)
        k = int((t * 7 + fa * 7)) % n
        PF.actor(lz, f"{ciclo}/ciclo_{k:02d}", x * W, y * H, hpx, flip=sent < 0, ancla=(0.5, 0.5), suelo=0, tono=tono)


def brillo_en(lz, pl, t, x, y, r, color=(1.0, 0.58, 0.22), inten=0.45, sem=0, chis=0):
    X, Y, s = pl.P(t, x, y)
    PF.brillo(lz, X, Y, r * s, color=color, inten=inten, t=t, sem=sem)
    if chis:
        PF.chispas(lz, t, X, Y, s=s * 1.2, n=chis, sem=sem)


def humo_en(lz, pl, t, x, y, s=1.0, color=(0.62, 0.64, 0.66), op=0.24, sem=0):
    X, Y, sc = pl.P(t, x, y)
    PF.humo(lz, t, X, Y, s=s * sc * 1.4, color=color, op=op, sem=sem)


def fogata(lz, pl, t, x, y, frac, sem=0, tono=None, grande=False):
    """Fogata-pegatina que parpadea (u04_fuego_humo/00 grande, /01 chica) con brillo, chispas y humo."""
    X, Y, h = pl.en(t, x, y, frac)
    fl = 1.0 + 0.06 * math.sin(t * 17 + sem) + 0.04 * math.sin(t * 29 + 2 * sem)
    PF.brillo(lz, X, Y - 0.4 * h, 2.6 * h, color=(1.0, 0.55, 0.20), inten=0.42 + 0.06 * math.sin(t * 11 + sem), t=t, sem=sem)
    PF.actor(lz, "u04_fuego_humo/00" if grande else "u04_fuego_humo/01", X, Y, h * fl, tono=tono, suelo=0, sombra=False,
             sy=1.0 + 0.05 * math.sin(t * 13 + sem))
    PF.chispas(lz, t, X, Y - 0.5 * h, s=h / 120.0, n=10, sem=sem)
    PF.humo(lz, t, X, Y - 1.1 * h, s=h / 90.0, color=(0.30, 0.28, 0.30), op=0.18, sem=sem)


def tinte(lz, color, k):
    if k <= 0.003:
        return
    g = lz.mean(2, keepdims=True)
    lz[:] = lz * (1 - k) + (0.55 * lz + 0.45 * g) * np.float32(color) * k


def oscurece(lz, k):
    if k > 0.003:
        lz *= 1.0 - k


def desenfoca(lz, s):
    lz[:] = cv2.GaussianBlur(lz, (0, 0), s)


_YY = np.linspace(0, 1, H, dtype=np.float32)[:, None]
_XX = np.linspace(0, 1, W, dtype=np.float32)[None, :]


def neblina(lz, t, y0, y1, fuerza=0.35, color=(0.80, 0.84, 0.95)):
    """Banda de neblina del cañón que deriva despacio."""
    banda = np.clip(1 - np.abs((_YY - (y0 + y1) / 2) / ((y1 - y0) / 2)), 0, 1) ** 1.5
    ondas = 0.75 + 0.25 * np.sin(_XX * 9.0 + t * 0.35) * np.sin(_XX * 3.1 - t * 0.21 + 1.0)
    a = (banda * ondas * fuerza)[..., None]
    lz[:] = lz * (1 - a) + np.float32(color) * a


def lluvia(lz, t, n=260, fuerza=0.55, viento=0.18, color=(0.80, 0.86, 0.95), sem=3):
    """Lluvia en dos profundidades: rayas finas que caen inclinadas."""
    capa = lz.copy()
    rng = np.random.RandomState(sem)
    for i in range(n):
        lejos = i < n * 0.6
        v = (1.6 if lejos else 2.6) * (0.85 + 0.3 * rng.rand())
        x0 = rng.rand() * (W + 200) - 100
        y = ((rng.rand() + t * v) % 1.0) * (H + 120) - 60
        L = (22 if lejos else 46) * (0.8 + 0.4 * rng.rand())
        x = x0 + viento * y
        cv2.line(capa, (int(x), int(y)), (int(x + viento * L), int(y + L)), color, 1 if lejos else 2, cv2.LINE_AA)
    lz[:] = lz * (1 - fuerza) + capa * fuerza


def relampago(lz, t, tiempos, dur=0.22):
    for tr in tiempos:
        if tr <= t < tr + dur:
            k = (1 - (t - tr) / dur) * (0.55 + 0.45 * (int((t - tr) * 30) % 2))
            lz[:] = lz + (np.float32((0.85, 0.9, 1.0)) - lz) * 0.5 * k


def estrellas(lz, t, n=140, y1=0.45, sem=11):
    """Titileo de estrellas sobre el cielo pintado (solo suma luz en lo oscuro)."""
    rng = np.random.RandomState(sem)
    for i in range(n):
        x, y = rng.rand() * W, rng.rand() * H * y1
        b = 0.5 + 0.5 * math.sin(t * (1.5 + 2.5 * rng.rand()) + i)
        if lz[int(y), int(x)].mean() < 0.35:
            cv2.circle(lz, (int(x), int(y)), 1, (0.9 * b + 0.1, 0.92 * b + 0.08, 1.0 * b), -1, cv2.LINE_AA)


def flechas(lz, t, lluvias, color=(0.16, 0.11, 0.08)):
    """Flechas en vuelo en pantalla: lluvias = [(t_ini, dur, (x0, y0), (x1, y1), n, sem)] en coordenadas 0..1 (parábola)."""
    for t_i, dur, p0, p1, n, sem in lluvias:
        rng = np.random.RandomState(sem)
        for i in range(n):
            d = rng.uniform(0, 0.5)
            u = (t - t_i - d) / dur
            if not 0 <= u <= 1:
                continue
            ox, oy = rng.uniform(-0.08, 0.08), rng.uniform(-0.05, 0.05)
            x = lerp(p0[0], p1[0], u) + ox
            y = lerp(p0[1], p1[1], u) + oy - 0.18 * math.sin(math.pi * u)
            u2 = min(1.0, u + 0.02)
            x2 = lerp(p0[0], p1[0], u2) + ox
            y2 = lerp(p0[1], p1[1], u2) + oy - 0.18 * math.sin(math.pi * u2)
            a = math.atan2((y2 - y) * H, (x2 - x) * W)
            L = 46
            X, Y = x * W, y * H
            Xa, Ya = X - math.cos(a) * L, Y - math.sin(a) * L
            cv2.line(lz, (int(Xa), int(Ya)), (int(X), int(Y)), color, 2, cv2.LINE_AA)
            cv2.line(lz, (int(Xa), int(Ya)), (int(Xa - math.cos(a + 0.5) * 9), int(Ya - math.sin(a + 0.5) * 9)), (0.85, 0.82, 0.76), 2,
                     cv2.LINE_AA)
            cv2.line(lz, (int(Xa), int(Ya)), (int(Xa - math.cos(a - 0.5) * 9), int(Ya - math.sin(a - 0.5) * 9)), (0.85, 0.82, 0.76), 2,
                     cv2.LINE_AA)


def rocas(lz, pl, t, caidas, tono=None):
    """Piedras que ruedan cuesta abajo (pieza de utilería): caidas = [(t_ini, dur, (x0, y0), (x1, y1), frac, sem)] en el escenario."""
    for t_i, dur, p0, p1, frac, sem in caidas:
        u = (t - t_i) / dur
        if not 0 <= u <= 1.05:
            continue
        u = min(u, 1.0)
        uu = u ** 1.6
        x, y = lerp(p0[0], p1[0], uu), lerp(p0[1], p1[1], uu)
        bote = abs(math.sin(u * math.pi * 3)) * 0.03 * (1 - u)
        X, Y, h = pl.en(t, x, y - bote, frac)
        PF.actor(lz, "u03_naturaleza/07", X, Y, h, rot=(u * 720 + sem * 40) % 360, tono=tono, ancla=(0.5, 0.6), suelo=0.15)


def polvo(lz, pl, t, x, y, s=1.0, t_in=0.0, dur=2.5, op=0.32, sem=0, color=(0.82, 0.70, 0.54)):
    """Nube de polvo que crece y se disipa (golpe, carga de caballos, derrumbe)."""
    u = (t - t_in) / dur
    if not 0 <= u <= 1:
        return
    X, Y, sc = pl.P(t, x, y)
    PF.humo(lz, t, X, Y, s=s * sc * (0.8 + 1.4 * u), color=color, op=op * (1 - u) ** 0.7, sem=sem)


def latido_rojo(lz, t, t_in, t_out, k=0.18):
    """Viñeta roja que late (miedo, herida, fuego)."""
    if not t_in <= t <= t_out:
        return
    a = k * (0.5 + 0.5 * math.sin((t - t_in) * 5.5)) * smooth(prog(t, t_in, t_in + 0.6)) * (1 - smooth(prog(t, t_out - 0.6, t_out)))
    r = np.clip((np.hypot(_XX - 0.5, (_YY - 0.5) * 0.75) - 0.25) * 2.2, 0, 1)[..., None] * a
    lz[:] = lz * (1 - r) + np.float32((0.45, 0.04, 0.02)) * r


def capitulo(lz, t, num, titulo, t_in, t_out):
    """Capítulo de novela en papel: número romano y título en tiras de papel recortado (nada de subtítulos)."""
    if not t_in <= t <= t_out + 0.4:
        return
    PF.rotulo(lz, num, W * 0.5, H * 0.38, 70, t, t_in, t_out, rot=-1.0)
    PF.rotulo(lz, titulo, W * 0.5, H * 0.50, 112, t, t_in + 0.35, t_out, rot=1.2)


def franjas(lz, k=1.0):
    """Franjas de cine (2,2:1): película, no documental."""
    b = int(H * 0.062 * k)
    if b > 0:
        lz[:b] = 0.0
        lz[H - b:] = 0.0


# ------------------------------------------------------------------ tomas
TOMAS = []


def toma(t0, ent=("fundido", 0.5)):
    def deco(f):
        TOMAS.append(dict(t0=t0, ent=ent, dib=f))
        return f
    return deco


# ================================================================== ayudantes del acto I (21-oct-2026)
def F(eid, i):
    """Inicio de la frase i de la escena eid."""
    return _ESC[eid]["frases"][i]["t0"]


def F1(eid, i):
    return _ESC[eid]["frases"][i]["t1"]


# orientación mirada en el PNG de cada pieza (previews/_mira.jpg)
MIRA.update({"h15_gente/00": 1, "h15_gente/01": 1, "h15_gente/03": 1, "h15_gente/04": -1, "h04_ollin_nino/04": 1,
             "h06_abuelo/03": 1, "h03_citlali/04": 1, "h01_tecuani/04": -1})


@functools.lru_cache(maxsize=16)
def puntos_fuego(fondo, zona, n=60, sem=5):
    """Puntos (x, y, fase) sobre las fogatas pintadas (píxeles naranja intenso) dentro de `zona` = (x0, y0, x1, y1)."""
    rgb = PF._fondo_rgb(fondo)
    hs, ws = rgb.shape[:2]
    hsv = cv2.cvtColor(cv2.resize(rgb, (ws // 2, hs // 2)), cv2.COLOR_RGB2HSV)
    m = (hsv[..., 0] <= 22) & (hsv[..., 1] > 110) & (hsv[..., 2] > 140)
    hh, ww = m.shape
    x0, y0, x1, y1 = zona
    m[:int(y0 * hh)] = False
    m[int(y1 * hh):] = False
    m[:, :int(x0 * ww)] = False
    m[:, int(x1 * ww):] = False
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        return ()
    r = np.random.default_rng(sem)
    sel = r.choice(len(xs), size=min(n, len(xs)), replace=False)
    return tuple((float(xs[i]) / ww, float(ys[i]) / hh, float(r.random())) for i in sel)


def fuegos_valle(lz, pl, t, fondo, zona, n=50, r=9.0, inten=0.30):
    """Las fogatas pintadas del valle titilan (cada una a su ritmo)."""
    for k, (x, y, f) in enumerate(puntos_fuego(fondo, zona, n)):
        X, Y, s = pl.P(t, x, y)
        if -20 < X < W + 20 and -20 < Y < H + 20:
            fl = 0.55 + 0.45 * math.sin(t * (2.0 + 3.0 * f) + k * 1.7)
            PF._blob(lz, X, Y, r * s * (0.8 + 0.4 * f), (1.0, 0.55, 0.20), inten * fl, aditivo=True)


def agua(lz, pl, t, fondo, s=1.0):
    """Destellos sobre el río pintado."""
    pts = []
    for x, y, f in PF.puntos_agua(fondo):
        X, Y, _ = pl.P(t, x, y)
        if 0 <= X < W and 0 <= Y < H:
            pts.append((X, Y, f))
    PF.destellos(lz, t, pts, s=s)


def lluvia_rect(lz, pl, t, x0, y0, x1, y1, n=70, fuerza=0.6, sem=4):
    """Lluvia SOLO dentro de un rectángulo del escenario (la puerta: afuera llueve)."""
    X0, Y0, _ = pl.P(t, x0, y0)
    X1, Y1, _ = pl.P(t, x1, y1)
    a, b, c, d = int(max(0, X0)), int(min(W, X1)), int(max(0, Y0)), int(min(H, Y1))
    if b - a < 4 or d - c < 4:
        return
    sub = np.ascontiguousarray(lz[c:d, a:b])
    capa = sub.copy()
    rng = np.random.RandomState(sem)
    ww, hh = b - a, d - c
    for i in range(n):
        v = 1.8 * (0.85 + 0.3 * rng.rand())
        xr = rng.rand() * (ww + 40) - 20
        y = ((rng.rand() + t * v) % 1.0) * (hh + 40) - 20
        L = 18 + 14 * rng.rand()
        x = xr + 0.12 * y
        cv2.line(capa, (int(x), int(y)), (int(x + 0.12 * L), int(y + L)), (0.75, 0.82, 0.95), 1, cv2.LINE_AA)
    lz[c:d, a:b] = sub * (1 - fuerza) + capa * fuerza


def ronda(lz, pl, t, ciclo, cx, cy, rx, ry, n, vel, frac, hz, tono=None, mitad=None, fase=0.0):
    """Bailarines en círculo alrededor de (cx, cy) del escenario; mitad = 'atras' / 'delante' / None (todos)."""
    nc = PF.ciclo_n(ciclo)
    lst = []
    for i in range(n):
        a = 2 * math.pi * i / n + vel * t + fase
        sa = math.sin(a)
        if (mitad == "atras" and sa > 0) or (mitad == "delante" and sa <= 0):
            continue
        lst.append((cy + ry * sa, cx + rx * math.cos(a), -rx * sa * vel, i))
    for y, x, dx, i in sorted(lst):
        X, Y, h = pl.en(t, x, y, frac * (y - hz) / (cy - hz))
        q = int(t * 8 + i * 3) % nc
        PF.actor(lz, f"{ciclo}/ciclo_{q:02d}", X, Y, h * 1.25, flip=dx < 0, tono=tono)


def hoguera(lz, pl, t, x, y, frac, t_in=None, sem=0, tono=None, pieza="u04_fuego_humo/02"):
    """Hoguera grande de fiesta (pieza u04/02) que se enciende en t_in, con brillo, chispas y humo."""
    u = 1.0 if t_in is None else PF.entra(t, t_in, 0.6)
    if t_in is not None and t < t_in:
        return
    X, Y, h = pl.en(t, x, y, frac)
    fl = 1.0 + 0.05 * math.sin(t * 15 + sem) + 0.04 * math.sin(t * 27 + 2 * sem)
    PF.brillo(lz, X, Y - 0.4 * h, 3.0 * h * u, color=(1.0, 0.55, 0.20), inten=0.48 * u, t=t, sem=sem)
    PF.actor(lz, pieza, X, Y, h * fl * u, tono=tono, suelo=0, sombra=False, sy=1.0 + 0.05 * math.sin(t * 12 + sem))
    PF.chispas(lz, t, X, Y - 0.6 * h, s=h / 90.0, n=16, sem=sem)
    PF.humo(lz, t, X, Y - 1.1 * h, s=h / 70.0, color=(0.30, 0.28, 0.30), op=0.20, sem=sem)


def vision(lz, pieza, X, Y, hpx, t, t_in, t_out, flip=False, op=0.55, sube=18.0):
    """Lo que cuentan los mercaderes aparece en el humo: pieza fantasma teñida de brasa que sube y se deshace."""
    if t < t_in or t > t_out + 0.7:
        return
    u = smooth(prog(t, t_in, t_in + 0.9)) * (1 - smooth(prog(t, t_out, t_out + 0.7)))
    y = Y - sube * (t - t_in)
    PF.humo(lz, t, X, y + 0.6 * hpx, s=hpx / 110.0, n=8, color=(0.40, 0.34, 0.32), op=0.34 * u, sem=7, alto=1.5 * hpx)
    capa = lz.copy()
    PF.actor(capa, pieza, X + 6 * math.sin(t * 2.3), y, hpx, flip=flip, op=1.0, tono=(1.0, 0.58, 0.32), ancla=(0.5, 0.5),
             suelo=0, sombra=False)
    d = cv2.GaussianBlur(capa - lz, (0, 0), 2.0)              # borroso y translúcido: una imagen en el humo, no un objeto
    lz += d * (op * u)


def bebe_patea(t, t0):
    """Giro de la pieza del recién nacido que patea (desde t0, 1,4 s)."""
    return 3.0 * math.sin((t - t0) * 21) * (1 - smooth(prog(t, t0, t0 + 1.4))) if t >= t0 else 0.0


# ================================================================== PRÓLOGO — apertura (0-13,7 s)
FZ_AP = (0.0, 0.35, 0.62, 1.0)       # el valle de e01_mixton_noche_b, donde están las fogatas del virrey
PAP1 = PF.Plano("e01_mixton_noche_b", 0.0, 14.4, z0=1.25, z1=1.08, c0=(0.42, 0.56), c1=(0.48, 0.52), par=(30, 6))
AMB += [(0.0, t0_("antes") + 0.5, "viento_noche", 0.55), (t0_("noche"), t0_("antes") + 0.5, "grillos", 0.35),
        (t0_("antes"), F("rio", 3) + 0.2, "alba", 0.60), (F("rio", 6) - 0.5, F("rio", 7) + 4.0, "alba", 0.45),
        (t0_("fiesta"), t1_("fiesta") + 0.3, "grillos", 0.25), (t0_("teul") - 0.3, t1_("teul") + 0.3, "alba", 0.55),
        (t0_("noticias") - 0.3, F("noticias", 5), "grillos", 0.30)]
snd(0.6, "fuego", 0.22, dur=13.0)
snd(5.8, "tambor", 0.45, tono=0.6)
snd(T("apertura", "diciembre") - 0.1, "papel", 0.5)
snd(T("apertura", "mixtón") - 0.1, "papel", 0.5)


@toma(0.0)
def AP1(lz, t):
    PAP1.fondo(lz, t)
    estrellas(lz, t, y1=0.30)
    fuegos_valle(lz, PAP1, t, "e01_mixton_noche_b", FZ_AP, n=60)
    neblina(lz, t, 0.42, 0.62, fuerza=0.16)
    brillo_en(lz, PAP1, t, 0.80, 0.79, 70, inten=0.40, sem=2, chis=8)
    quieto(lz, PAP1, t, "h02_tecuani_g/00", 0.66, 0.79, 0.30, flip=True, tono=NOCHE_FUEGO)
    quieto(lz, PAP1, t, "h05_ollin_joven/04", 0.74, 0.83, 0.20, flip=True, tono=NOCHE_FUEGO, fase=1.3)
    PF.rotulo(lz, "DICIEMBRE DE 1541", W * 0.29, H * 0.19, 66, t, T("apertura", "diciembre") - 0.1, 12.6, rot=-1.5)
    PF.rotulo(lz, "CERRO DEL MIXTÓN · CAÑÓN DE JUCHIPILA", W * 0.33, H * 0.30, 38, t, T("apertura", "mixtón") - 0.1, 12.8, rot=1.0)


# ================================================================== PRÓLOGO — la noche antes del asalto (13,7-54,9 s)
FZ_NO = (0.50, 0.36, 0.92, 0.60)     # el valle de e01_mixton_noche_a
PNO1 = PF.Plano("e01_mixton_noche_a", t0_("noche") - 0.4, F("noche", 1), z0=1.08, z1=1.22, c0=(0.48, 0.52), c1=(0.56, 0.56),
                par=(30, 6))
snd(t0_("noche"), "fuego", 0.35, dur=41.0)


@toma(t0_("noche") - 0.4, ("fundido", 0.8))
def NO1(lz, t):
    PNO1.fondo(lz, t)
    estrellas(lz, t, y1=0.22)
    fuegos_valle(lz, PNO1, t, "e01_mixton_noche_a", FZ_NO, n=50)
    humo_en(lz, PNO1, t, 0.33, 0.74, s=0.8, color=(0.70, 0.70, 0.74), op=0.18, sem=1)
    brillo_en(lz, PNO1, t, 0.33, 0.79, 90, inten=0.42, sem=1, chis=10)
    quieto(lz, PNO1, t, "h05_ollin_joven/04", 0.24, 0.87, 0.24, tono=NOCHE_FUEGO, fase=1.1)
    quieto(lz, PNO1, t, "h02_tecuani_g/00", 0.55, 0.80, 0.34, tono=NOCHE_FUEGO)


PNO2 = PF.Plano("e01_mixton_noche_b", F("noche", 1) - 0.3, F("noche", 2), z0=1.40, z1=1.18, c0=(0.36, 0.64), c1=(0.45, 0.57),
                par=(30, 5))


@toma(F("noche", 1) - 0.3, ("fundido", 0.6))
def NO2(lz, t):
    PNO2.fondo(lz, t)
    fuegos_valle(lz, PNO2, t, "e01_mixton_noche_b", FZ_AP, n=60, r=11.0, inten=0.36)
    for k, (x, y) in enumerate([(0.18, 0.62), (0.34, 0.70), (0.08, 0.80)]):
        humo_en(lz, PNO2, t, x, y, s=0.9, color=(0.20, 0.18, 0.22), op=0.20, sem=k + 3)
    neblina(lz, t, 0.30, 0.55, fuerza=0.14)
    quieto(lz, PNO2, t, "h02_tecuani_g/00", 0.66, 0.79, 0.30, flip=True, tono=NOCHE_FUEGO)


PNO3 = PF.Plano("e01_mixton_noche_a", F("noche", 2) - 0.25, F("noche", 3), z0=1.88, z1=1.98, c0=(0.58, 0.60), c1=(0.58, 0.60),
                par=(20, 4))
snd(F("noche", 2) - 0.2, "latido", 0.45)


@toma(F("noche", 2) - 0.25, ("corte", 0))
def NO3(lz, t):
    PNO3.fondo(lz, t)
    fuegos_valle(lz, PNO3, t, "e01_mixton_noche_a", FZ_NO, n=50, r=10.0)
    desenfoca(lz, 2.4)
    quieto(lz, PNO3, t, "h02_tecuani_g/00", 0.55, 0.80, 0.34, tono=NOCHE_FUEGO)


PNO4 = PF.Plano("e01_mixton_noche_a", F("noche", 3) - 0.2, F("noche", 4), z0=1.85, z1=1.95, c0=(0.30, 0.72), c1=(0.30, 0.71),
                par=(18, 4))


@toma(F("noche", 3) - 0.2, ("corte", 0))
def NO4(lz, t):
    PNO4.fondo(lz, t)
    desenfoca(lz, 2.2)
    brillo_en(lz, PNO4, t, 0.33, 0.79, 70, inten=0.40, sem=1, chis=8)
    quieto(lz, PNO4, t, "h05_ollin_joven/04", 0.24, 0.87, 0.24, tono=NOCHE_FUEGO, fase=1.1)


PNO5 = PF.Plano("e01_mixton_noche_a", F("noche", 4) - 0.3, F("noche", 5), z0=1.38, z1=1.46, c0=(0.37, 0.63), c1=(0.38, 0.64),
                par=(26, 5))


@toma(F("noche", 4) - 0.3, ("fundido", 0.5))
def NO5(lz, t):
    PNO5.fondo(lz, t)
    fuegos_valle(lz, PNO5, t, "e01_mixton_noche_a", FZ_NO, n=40)
    humo_en(lz, PNO5, t, 0.33, 0.74, s=0.8, color=(0.70, 0.70, 0.74), op=0.18, sem=1)
    brillo_en(lz, PNO5, t, 0.33, 0.79, 95, inten=0.44, sem=1, chis=10)
    quieto(lz, PNO5, t, "h02_tecuani_g/03", 0.22, 0.87, 0.29, tono=NOCHE_FUEGO)
    quieto(lz, PNO5, t, "h05_ollin_joven/04", 0.45, 0.88, 0.22, flip=True, tono=NOCHE_FUEGO, fase=0.9)


PNO6 = PF.Plano("e01_mixton_noche_b", F("noche", 5) - 0.3, t1_("noche") + 0.6, z0=1.55, z1=1.06, c0=(0.66, 0.64), c1=(0.50, 0.48),
                par=(30, 6))
snd(T("noche", "tecuani", 5) - 0.1, "papel", 0.5)


@toma(F("noche", 5) - 0.3, ("fundido", 0.5))
def NO6(lz, t):
    PNO6.fondo(lz, t)
    estrellas(lz, t, y1=0.30)
    fuegos_valle(lz, PNO6, t, "e01_mixton_noche_b", FZ_AP, n=60)
    neblina(lz, t, 0.42, 0.62, fuerza=0.15)
    brillo_en(lz, PNO6, t, 0.80, 0.79, 80, inten=0.42, sem=2, chis=8)
    quieto(lz, PNO6, t, "h02_tecuani_g/00", 0.68, 0.80, 0.34, flip=True, tono=NOCHE_FUEGO)
    quieto(lz, PNO6, t, "h05_ollin_joven/01", 0.87, 0.83, 0.31, flip=True, tono=NOCHE_FUEGO, fase=0.7)
    PF.rotulo(lz, "TECUANI", W * 0.30, H * 0.22, 92, t, T("noche", "tecuani", 5) - 0.1, F1("noche", 5) - 0.4, rot=-1.8)
    PF.rotulo(lz, "caxcán del cañón de Juchipila", W * 0.31, H * 0.33, 40, t, T("noche", "caxcán", 5) - 0.1,
              F1("noche", 5) - 0.4, rot=1.0)


# ================================================================== ACTO I — antes (54,9-65,1 s)
PAN1 = PF.Plano("e02_canon_amanecer_b", t0_("antes"), t1_("antes") + 0.5, z0=1.18, z1=1.06, c0=(0.54, 0.54), c1=(0.50, 0.51),
                par=(30, 7), tono=DORADO)
VUELO_AN = [(t0_("antes") + 0.5, 11.0, 0.22, 0.16, 70, 1, 0.3), (t0_("antes") + 2.5, 10.0, 0.28, 0.20, 52, 1, 1.9)]
snd(t0_("antes") + 0.1, "amanecer", 0.6, dur=4.0)
snd(t0_("antes") + 0.6, "papel", 0.5)
snd(T("antes", "cañón") - 0.1, "papel", 0.5)
for _tp, _tn in ((57.0, 1.0), (59.4, 1.2), (61.8, 0.9)):
    snd(_tp, "pio", 0.35, tono=_tn)


@toma(t0_("antes"), ("destello", 0.9))
def AN1(lz, t):
    PAN1.fondo(lz, t)
    PF.brillo(lz, *PAN1.P(t, 0.73, 0.30)[:2], 260, color=(1.0, 0.80, 0.50), inten=0.22, t=t, sem=4)
    neblina(lz, t, 0.44, 0.60, fuerza=0.16, color=(0.98, 0.90, 0.86))
    for k, (x, y) in enumerate([(0.38, 0.58), (0.70, 0.55), (0.66, 0.60)]):
        humo_en(lz, PAN1, t, x, y, s=0.6, color=(0.88, 0.86, 0.84), op=0.20, sem=k)
    agua(lz, PAN1, t, "e02_canon_amanecer_b")
    aves(lz, t, VUELO_AN)
    capitulo(lz, t, "I", "ANTES", t0_("antes") + 0.6, T("antes", "cañón") - 0.4)
    PF.rotulo(lz, "CAÑÓN DE JUCHIPILA · HACIA 1525", W * 0.5, H * 0.20, 46, t, T("antes", "cañón") - 0.1, t1_("antes") - 0.3,
              rot=-1.0)


# ================================================================== ACTO I — el río (65,1-123,4 s)
PRI1 = PF.Plano("e02_canon_amanecer_a", t0_("rio"), F("rio", 1), z0=1.06, z1=1.32, c0=(0.50, 0.52), c1=(0.60, 0.58),
                par=(30, 7), tono=DORADO)
VUELO_RI = [(t0_("rio") - 1.0, 9.0, 0.20, 0.14, 64, -1, 0.6), (t0_("rio") + 1.5, 8.0, 0.26, 0.22, 46, -1, 2.2)]
_ta_ri1 = t0_("rio") + 0.2
_tb_ri1 = t0_("rio") + 3.6
snd(t0_("rio") + 0.3, "pasos", 0.25, dur=3.2)
snd(t0_("rio") + 1.0, "pio", 0.3, tono=1.1)


@toma(t0_("rio"), ("fundido", 0.5))
def RI1(lz, t):
    PRI1.fondo(lz, t)
    for k, (x, y) in enumerate([(0.35, 0.50), (0.38, 0.48), (0.70, 0.55)]):
        humo_en(lz, PRI1, t, x, y, s=0.55, color=(0.88, 0.86, 0.84), op=0.18, sem=k)
    agua(lz, PRI1, t, "e02_canon_amanecer_a")
    aves(lz, t, VUELO_RI)
    anda(lz, PRI1, t, "c01_tecuani_camina", _ta_ri1, _tb_ri1, 0.10, 0.40, 0.86, 0.20, desde_antes=True, hasta_despues=False,
         tono=DORADO)
    if t > _tb_ri1:
        quieto(lz, PRI1, t, "h01_tecuani/00", 0.40, 0.86, 0.20, tono=DORADO)


PRI2 = PF.Plano("e03_milpa_rio_a", F("rio", 1) - 0.3, F("rio", 2), z0=1.10, z1=1.18, c0=(0.46, 0.54), c1=(0.52, 0.55), par=(32, 7))
_ta_ri2, _tb_ri2 = F("rio", 1) - 0.3, F("rio", 1) + 4.0
snd(F("rio", 1) - 0.2, "pasos", 0.3, dur=4.2)
snd(T("rio", "maíz", 1) - 0.1, "pop", 0.5)


@toma(F("rio", 1) - 0.3, ("latigo", 0.45))
def RI2(lz, t):
    PRI2.fondo(lz, t)
    agua(lz, PRI2, t, "e03_milpa_rio_a")
    paseo(lz, PRI2, t, "h03_citlali/04", _ta_ri2, _tb_ri2 + 1.0, 0.95, 0.72, 0.82, 0.29, pasos=1.8)
    anda(lz, PRI2, t, "c01_tecuani_camina", _ta_ri2, _tb_ri2, 0.06, 0.48, 0.88, 0.34, desde_antes=True, hasta_despues=False)
    if t > _tb_ri2:
        quieto(lz, PRI2, t, "h01_tecuani/00", 0.48, 0.88, 0.34)
    quieto(lz, PRI2, t, "u01_utileria/03", 0.60, 0.90, 0.09, t_in=T("rio", "maíz", 1) - 0.1)
    plantas(lz, PRI2, t, [("u03_naturaleza/05", 0.04, 1.03, 0.52, 1.35, False), ("u03_naturaleza/02", 0.95, 1.03, 0.28, 1.4, True)])


PRI3 = PF.Plano("e03_milpa_rio_b", F("rio", 2) - 0.3, F("rio", 3), z0=1.12, z1=1.08, c0=(0.50, 0.54), c1=(0.48, 0.52), par=(32, 7))
snd(T("rio", "fibra", 2) - 0.1, "pop", 0.5)
snd(T("rio", "aguamiel", 2) - 0.1, "pop", 0.5, tono=0.9)


@toma(F("rio", 2) - 0.3, ("fundido", 0.5))
def RI3(lz, t):
    PRI3.fondo(lz, t)
    agua(lz, PRI3, t, "e03_milpa_rio_b")
    paseo(lz, PRI3, t, "h15_gente/04", F("rio", 2) - 0.3, F1("rio", 2), 0.62, 0.40, 0.84, 0.25, pasos=2.0)
    paseo(lz, PRI3, t, "h15_gente/03", F("rio", 2) - 0.3, F1("rio", 2) - 1.0, 0.12, 0.34, 0.89, 0.35, pasos=1.7)
    plantas(lz, PRI3, t, [("u03_naturaleza/03", 0.88, 1.04, 0.30, 1.3, False), ("u03_naturaleza/02", 0.06, 1.04, 0.24, 1.35, False)])
    pega(lz, "u01_utileria/10", W * 0.26, H * 0.30, 170, t, T("rio", "fibra", 2) - 0.1, F1("rio", 2) + 0.2, rot=-6)
    pega(lz, "u01_utileria/02", W * 0.74, H * 0.30, 200, t, T("rio", "aguamiel", 2) - 0.1, F1("rio", 2) + 0.2, rot=5)


PRI4 = PF.Plano("e04_casa_madrugada_a", F("rio", 3) - 0.3, T("rio", "ese", 3), z0=1.12, z1=1.26, c0=(0.50, 0.55), c1=(0.56, 0.60),
                par=(22, 5), tono=INTERIOR)
_t_ese = T("rio", "ese", 3)
for _k in range(int((F1("rio", 3) - F("rio", 3) + 1.0) / 1.15)):
    snd(F("rio", 3) - 0.2 + _k * 1.15, "arena", 0.28, dur=0.6)
snd(F("rio", 3) - 0.3, "fuego", 0.22, dur=11.5)
snd(T("rio", "citlali", 3) - 0.1, "papel", 0.5)


def _muele(t):
    return 0.005 * math.sin(2 * math.pi * t / 1.15)


@toma(F("rio", 3) - 0.3, ("fundido", 0.6))
def RI4(lz, t):
    PRI4.fondo(lz, t)
    humo_en(lz, PRI4, t, 0.37, 0.60, s=0.7, color=(0.74, 0.70, 0.68), op=0.16, sem=2)
    brillo_en(lz, PRI4, t, 0.37, 0.68, 80, inten=0.40, sem=3, chis=8)
    quieto(lz, PRI4, t, "h03_citlali/00", 0.60 + _muele(t), 0.93, 0.36, tono=INTERIOR, rot=1.2 * math.sin(2 * math.pi * t / 1.15))
    PF.rotulo(lz, "CITLALI", W * 0.70, H * 0.21, 80, t, T("rio", "citlali", 3) - 0.1, _t_ese - 0.3, rot=1.5)


PRI4B = PF.Plano("e04_casa_madrugada_a", _t_ese - 0.2, F("rio", 4), z0=2.0, z1=2.06, c0=(0.66, 0.74), c1=(0.66, 0.74), par=(16, 3),
                 tono=INTERIOR)


@toma(_t_ese - 0.2, ("corte", 0))
def RI4B(lz, t):
    PRI4B.fondo(lz, t)
    desenfoca(lz, 2.0)
    brillo_en(lz, PRI4B, t, 0.37, 0.68, 60, inten=0.30, sem=3)
    quieto(lz, PRI4B, t, "h03_citlali/00", 0.60 + 1.6 * _muele(t), 0.93, 0.36, tono=INTERIOR,
           rot=2.0 * math.sin(2 * math.pi * t / 1.15))


PRI5 = PF.Plano("e22_casa_noche_a", F("rio", 4) - 0.3, F("rio", 5), z0=1.10, z1=1.20, c0=(0.50, 0.54), c1=(0.48, 0.57),
                par=(22, 5), tono=INTERIOR)
_t_pat = T("rio", "patear", 4)
snd(F("rio", 4) - 0.3, "lluvia", 0.45, dur=13.0)
snd(F("rio", 4) + 0.4, "trueno", 0.40)
snd(_t_pat - 0.1, "bebe", 0.55)
snd(T("rio", "movimiento", 4) - 0.1, "papel", 0.5)


@toma(F("rio", 4) - 0.3, ("fundido", 0.7))
def RI5(lz, t):
    PRI5.fondo(lz, t)
    lluvia_rect(lz, PRI5, t, 0.845, 0.27, 0.94, 0.70)
    brillo_en(lz, PRI5, t, 0.67, 0.64, 95, inten=0.42, sem=5, chis=8)
    relampago(lz, t, [F("rio", 4) + 0.35])
    quieto(lz, PRI5, t, "h01_tecuani/02", 0.40, 0.90, 0.48, tono=INTERIOR, rot=bebe_patea(t, _t_pat))
    PF.rotulo(lz, "OLLIN = MOVIMIENTO", W * 0.50, H * 0.20, 64, t, T("rio", "movimiento", 4) - 0.1, F1("rio", 4) + 0.2, rot=-1.2)


PRI6 = PF.Plano("e22_casa_noche_b", F("rio", 5) - 0.25, F("rio", 6), z0=1.60, z1=1.66, c0=(0.42, 0.62), c1=(0.43, 0.62),
                par=(16, 3), tono=INTERIOR)


@toma(F("rio", 5) - 0.25, ("corte", 0))
def RI6(lz, t):
    PRI6.fondo(lz, t)
    brillo_en(lz, PRI6, t, 0.17, 0.70, 90, inten=0.38, sem=6, chis=6)
    desenfoca(lz, 2.4)
    quieto(lz, PRI6, t, "h03_citlali/01", 0.42, 0.93, 0.44, tono=INTERIOR, fase=0.5,
           rot=0.8 * math.sin(t * 9) * (1 - smooth(prog(t, F("rio", 5), F("rio", 5) + 1.5))))


PRI7 = PF.Plano("e05_rio_piedras_a", F("rio", 6) - 0.3, F("rio", 7), z0=1.30, z1=1.36, c0=(0.40, 0.61), c1=(0.38, 0.61),
                par=(30, 6), tono=DORADO)
_ta_ri7 = F("rio", 6) - 0.3
_tb_ri7 = _ta_ri7 + 3.8
_t_sac = T("rio", "sacaste", 6)
_t_pie = T("rio", "piedra", 6)
_t_ver = T("rio", "verde", 6)
_t_dis = T("rio", "diste", 6)
snd(_ta_ri7 + 0.2, "pasos", 0.3, dur=3.6)
snd(_t_sac - 0.1, "chapuzon", 0.45)
snd(_t_ver - 0.1, "brillo", 0.5)


@toma(F("rio", 6) - 0.3, ("fundido", 0.6))
def RI7(lz, t):
    PRI7.fondo(lz, t)
    agua(lz, PRI7, t, "e05_rio_piedras_a", s=1.2)
    anda(lz, PRI7, t, "c01_tecuani_camina", _ta_ri7, _tb_ri7, -0.05, 0.28, 0.78, 0.34, desde_antes=True, hasta_despues=False,
         tono=DORADO)
    if _tb_ri7 < t < _t_dis:
        quieto(lz, PRI7, t, "h01_tecuani/00", 0.28, 0.78, 0.34, tono=DORADO)
    elif t >= _t_dis:
        quieto(lz, PRI7, t, "h01_tecuani/01", 0.31, 0.80, 0.28, tono=DORADO)
    if t < _t_sac:
        paseo(lz, PRI7, t, "h04_ollin_nino/04", _ta_ri7, _t_sac - 0.2, -0.14, 0.42, 0.80, 0.17, pasos=2.8, y1=0.85, tono=DORADO)
    elif t < _t_pie:
        quieto(lz, PRI7, t, "h04_ollin_nino/01", 0.43, 0.86, 0.15, tono=DORADO)
    else:
        quieto(lz, PRI7, t, "h04_ollin_nino/00", 0.43, 0.86, 0.19, tono=DORADO, fase=0.4)
        X, Y, h = PRI7.en(t, 0.445, 0.86 - 0.165, 0.02)
        PF.brillo(lz, X, Y, 40, color=(0.55, 1.0, 0.70), inten=0.35 * smooth(prog(t, _t_pie, _t_pie + 0.6)), t=t, sem=7)
    pega(lz, "u01_utileria/08", W * 0.76, H * 0.36, 230, t, _t_ver - 0.1, F1("rio", 6) + 0.3, rot=-8)


PRI8 = PF.Plano("e05_rio_piedras_b", F("rio", 7) - 0.3, T("rio", "todavía", 7), z0=1.40, z1=1.48, c0=(0.38, 0.64),
                c1=(0.39, 0.64), par=(22, 5), tono=DORADO)
_t_tod = T("rio", "todavía", 7)


@toma(F("rio", 7) - 0.3, ("desenfoque", 0.5))
def RI8(lz, t):
    PRI8.fondo(lz, t)
    agua(lz, PRI8, t, "e05_rio_piedras_b", s=1.3)
    quieto(lz, PRI8, t, "h01_tecuani/00", 0.30, 0.86, 0.40, tono=DORADO)
    quieto(lz, PRI8, t, "h04_ollin_nino/00", 0.43, 0.87, 0.19, flip=True, tono=DORADO, fase=0.6)


PRI9 = PF.Plano("e01_mixton_noche_a", _t_tod - 0.15, t1_("rio") + 0.3, z0=1.88, z1=1.96, c0=(0.58, 0.60), c1=(0.57, 0.61),
                par=(16, 3))


@toma(_t_tod - 0.15, ("fundido", 0.4))
def RI9(lz, t):
    PRI9.fondo(lz, t)
    fuegos_valle(lz, PRI9, t, "e01_mixton_noche_a", FZ_NO, n=40)
    desenfoca(lz, 2.8)
    brillo_en(lz, PRI9, t, 0.40, 0.80, 70, inten=0.30, sem=1)
    quieto(lz, PRI9, t, "h02_tecuani_g/04", 0.56, 0.84, 0.30, tono=NOCHE_FUEGO)
    X, Y, h = PRI9.en(t, 0.565, 0.84 - 0.17, 0.02)
    PF.brillo(lz, X, Y, 46, color=(0.55, 1.0, 0.70), inten=0.30, t=t, sem=8)


# ================================================================== ACTO I — la fiesta (123,4-154,3 s)
TORCH_A = [(0.22, 0.79), (0.29, 0.71), (0.60, 0.71), (0.75, 0.71), (0.87, 0.74)]
TORCH_B = [(0.11, 0.44), (0.33, 0.52), (0.60, 0.57), (0.81, 0.57), (0.95, 0.51)]


def antorchas(lz, pl, t, lista, inten=0.32):
    for k, (x, y) in enumerate(lista):
        brillo_en(lz, pl, t, x, y, 55, inten=inten, sem=20 + k, chis=4)


PFI1 = PF.Plano("e06_plaza_fiesta_a", t0_("fiesta") - 0.2, F("fiesta", 1), z0=1.08, z1=1.16, c0=(0.50, 0.53), c1=(0.52, 0.56),
                par=(28, 6))
_t_hog = t0_("fiesta") + 0.8
snd(t0_("fiesta"), "fuego", 0.35, dur=31.0)
snd(_t_hog, "pop", 0.45, tono=0.7)
snd(t0_("fiesta") + 0.2, "pasos", 0.3, dur=4.0)


@toma(t0_("fiesta") - 0.2, ("fundido", 0.6))
def FI1(lz, t):
    PFI1.fondo(lz, t)
    estrellas(lz, t, y1=0.25)
    antorchas(lz, PFI1, t, TORCH_A)
    ta, tb = t0_("fiesta") - 0.2, t0_("fiesta") + 4.6
    paseo(lz, PFI1, t, "h15_gente/00", ta, tb, 0.16, 0.33, 0.80, 0.27, pasos=1.6, tono=NOCHE_FUEGO)
    paseo(lz, PFI1, t, "h15_gente/04", ta, tb, 0.86, 0.68, 0.82, 0.24, pasos=2.0, tono=NOCHE_FUEGO)
    hoguera(lz, PFI1, t, 0.53, 0.85, 0.15, t_in=_t_hog, tono=FOGATA)
    paseo(lz, PFI1, t, "h15_gente/01", ta, tb, 0.04, 0.38, 0.87, 0.33, pasos=1.9, tono=NOCHE_FUEGO)
    paseo(lz, PFI1, t, "h15_gente/02", ta, tb, 0.96, 0.67, 0.89, 0.21, pasos=2.4, tono=NOCHE_FUEGO)


PFI2 = PF.Plano("e06_plaza_fiesta_b", F("fiesta", 1) - 0.3, F("fiesta", 2), z0=1.12, z1=1.22, c0=(0.48, 0.55), c1=(0.46, 0.58),
                par=(28, 6))
_t_tamb0, _t_tamb1 = F("fiesta", 1) - 0.2, t1_("fiesta") - 0.5
_k = 0
while _t_tamb0 + _k * 0.52 < _t_tamb1:
    snd(_t_tamb0 + _k * 0.52, "tambor", 0.42 if _k % 3 else 0.55, tono=1.0 if _k % 3 else 0.8)
    _k += 1


@toma(F("fiesta", 1) - 0.3, ("fundido", 0.5))
def FI2(lz, t):
    PFI2.fondo(lz, t)
    estrellas(lz, t, y1=0.22)
    antorchas(lz, PFI2, t, TORCH_B)
    ronda(lz, PFI2, t, "c10_danza", 0.45, 0.77, 0.21, 0.07, 8, 0.28, 0.17, 0.42, tono=FOGATA, mitad="atras")
    hoguera(lz, PFI2, t, 0.45, 0.78, 0.18, tono=FOGATA, sem=3)
    ronda(lz, PFI2, t, "c10_danza", 0.45, 0.77, 0.21, 0.07, 8, 0.28, 0.17, 0.42, tono=FOGATA, mitad="delante")
    quieto(lz, PFI2, t, "u02_utileria_guerra/11", 0.16, 0.88, 0.07, tono=FOGATA, rot=1.5 * math.sin(t * 12))
    plantas(lz, PFI2, t, [("u03_naturaleza/02", 0.94, 1.04, 0.26, 1.35, True)], tono=NOCHE_FUEGO)


PFI3 = PF.Plano("e06_plaza_fiesta_b", F("fiesta", 2) - 0.3, F("fiesta", 3), z0=1.55, z1=1.62, c0=(0.50, 0.66), c1=(0.52, 0.67),
                par=(22, 5))
_t_pis = T("fiesta", "pisaba", 2)
snd(_t_pis - 0.05, "pasos", 0.5, dur=0.5)


def _baile(t, f=0.9, a=0.012):
    return a * math.sin(2 * math.pi * f * t), abs(math.sin(2 * math.pi * f * t))


@toma(F("fiesta", 2) - 0.3, ("corte", 0))
def FI3(lz, t):
    PFI3.fondo(lz, t)
    antorchas(lz, PFI3, t, TORCH_B, inten=0.28)
    ronda(lz, PFI3, t, "c10_danza", 0.45, 0.77, 0.21, 0.07, 8, 0.28, 0.17, 0.42, tono=FOGATA, mitad="atras")
    hoguera(lz, PFI3, t, 0.45, 0.78, 0.18, tono=FOGATA, sem=3)
    ronda(lz, PFI3, t, "c10_danza", 0.45, 0.77, 0.21, 0.07, 8, 0.28, 0.17, 0.42, tono=FOGATA, mitad="delante")
    dx, b = _baile(t)
    X, Y, h = PFI3.en(t, 0.42 + dx, 0.92, 0.40)
    PF.actor(lz, "h03_citlali/02", X, Y - 0.03 * h * b, h, tono=FOGATA, rot=3 * math.sin(2 * math.pi * 0.9 * t))
    dx2, b2 = _baile(t + 0.3, 0.9, 0.008)
    hop = 0.08 * math.sin(math.pi * prog(t, _t_pis, _t_pis + 0.45)) if _t_pis <= t <= _t_pis + 0.45 else 0.0
    X, Y, h = PFI3.en(t, 0.61 + dx2, 0.93, 0.42)
    PF.actor(lz, "h01_tecuani/03", X, Y - (0.025 * b2 + hop) * h, h, flip=True, tono=FOGATA, rot=-2 * math.sin(2 * math.pi * 0.9 * t))


PFI4 = PF.Plano("e06_plaza_fiesta_b", F("fiesta", 3) - 0.2, F("fiesta", 4), z0=2.10, z1=2.16, c0=(0.42, 0.72), c1=(0.42, 0.72),
                par=(14, 3))


@toma(F("fiesta", 3) - 0.2, ("corte", 0))
def FI4(lz, t):
    PFI4.fondo(lz, t)
    hoguera(lz, PFI4, t, 0.45, 0.78, 0.18, tono=FOGATA, sem=3)
    desenfoca(lz, 2.6)
    dx, b = _baile(t, 0.7, 0.006)
    X, Y, h = PFI4.en(t, 0.40 + dx, 0.94, 0.36)
    PF.actor(lz, "h03_citlali/02", X, Y - 0.02 * h * b, h, tono=FOGATA, rot=2.5 * math.sin(2 * math.pi * 0.7 * t))


PFI5 = PF.Plano("e06_plaza_fiesta_a", F("fiesta", 4) - 0.3, t1_("fiesta") + 0.6, z0=1.40, z1=1.06, c0=(0.53, 0.64),
                c1=(0.50, 0.51), par=(30, 6))


@toma(F("fiesta", 4) - 0.3, ("fundido", 0.6))
def FI5(lz, t):
    PFI5.fondo(lz, t)
    estrellas(lz, t, y1=0.25)
    antorchas(lz, PFI5, t, TORCH_A)
    ronda(lz, PFI5, t, "c10_danza", 0.53, 0.84, 0.17, 0.05, 8, 0.24, 0.15, 0.45, tono=FOGATA, mitad="atras")
    hoguera(lz, PFI5, t, 0.53, 0.85, 0.15, tono=FOGATA)
    ronda(lz, PFI5, t, "c10_danza", 0.53, 0.84, 0.17, 0.05, 8, 0.24, 0.15, 0.45, tono=FOGATA, mitad="delante")
    X, Y, s = PFI5.P(t, 0.53, 0.70)
    PF.chispas(lz, t, X, Y, s=s * 2.2, n=24, sem=9)


# ================================================================== ACTO I — el Teul (154,3-181,7 s)
PTE1 = PF.Plano("e07_teul_cima_a", t0_("teul") - 0.2, F("teul", 1), z0=1.06, z1=1.14, c0=(0.50, 0.52), c1=(0.48, 0.55), par=(30, 7),
                tono=OCASO)
VUELO_TE = [(t0_("teul"), 12.0, 0.22, 0.15, 60, 1, 0.5), (t0_("teul") + 3.0, 11.0, 0.30, 0.24, 44, 1, 1.4)]
_ta_te1, _tb_te1 = t0_("teul") - 0.2, t0_("teul") + 4.4
_t_teul = T("teul", "teul", 0)
snd(_ta_te1 + 0.2, "pasos", 0.3, dur=4.0)
snd(_t_teul - 0.1, "papel", 0.5)


@toma(t0_("teul") - 0.2, ("fundido", 0.8))
def TE1(lz, t):
    PTE1.fondo(lz, t)
    PF.brillo(lz, *PTE1.P(t, 0.42, 0.08)[:2], 320, color=(1.0, 0.72, 0.42), inten=0.22, t=t, sem=4)
    aves(lz, t, VUELO_TE)
    if t < _tb_te1:
        paseo(lz, PTE1, t, "h06_abuelo/03", _ta_te1, _tb_te1, 0.02, 0.38, 0.84, 0.34, pasos=1.5, tono=OCASO)
    else:
        quieto(lz, PTE1, t, "h06_abuelo/00", 0.38, 0.84, 0.34, tono=OCASO)
    anda(lz, PTE1, t, "c01_tecuani_camina", _ta_te1, _tb_te1, -0.10, 0.22, 0.87, 0.37, desde_antes=True, hasta_despues=False,
         tono=OCASO)
    if t > _tb_te1:
        quieto(lz, PTE1, t, "h01_tecuani/00", 0.22, 0.87, 0.37, tono=OCASO)
    if t < _tb_te1 + 0.3:
        paseo(lz, PTE1, t, "h04_ollin_nino/04", _ta_te1, _tb_te1 + 0.3, -0.04, 0.29, 0.88, 0.16, pasos=2.8, tono=OCASO)
    else:
        quieto(lz, PTE1, t, "h04_ollin_nino/02", 0.29, 0.88, 0.17, tono=OCASO)
    plantas(lz, PTE1, t, [("u03_naturaleza/04", 0.04, 1.03, 0.40, 1.3, False), ("u03_naturaleza/09", 0.93, 1.04, 0.22, 1.35, False)],
            tono=OCASO)
    PF.rotulo(lz, "EL TEUL", W * 0.27, H * 0.19, 96, t, _t_teul - 0.1, F("teul", 1) - 0.5, rot=-1.5)
    PF.rotulo(lz, "cerro sagrado", W * 0.28, H * 0.30, 46, t, T("teul", "sagrado", 0) - 0.1, F("teul", 1) - 0.5, rot=1.2)


PTE2 = PF.Plano("e07_teul_cima_b", F("teul", 1) - 0.3, F("teul", 2), z0=1.32, z1=1.08, c0=(0.40, 0.60), c1=(0.50, 0.52),
                par=(30, 7), tono=OCASO)


@toma(F("teul", 1) - 0.3, ("fundido", 0.6))
def TE2(lz, t):
    PTE2.fondo(lz, t)
    neblina(lz, t, 0.30, 0.48, fuerza=0.12, color=(0.95, 0.80, 0.75))
    agua(lz, PTE2, t, "e07_teul_cima_b")
    aves(lz, t, VUELO_TE)
    quieto(lz, PTE2, t, "h06_abuelo/05", 0.36, 0.86, 0.38, tono=OCASO)
    quieto(lz, PTE2, t, "h04_ollin_nino/02", 0.46, 0.88, 0.18, tono=OCASO, fase=0.8)


PTE3 = PF.Plano("e07_teul_cima_a", F("teul", 2) - 0.25, F("teul", 3), z0=1.70, z1=1.76, c0=(0.46, 0.70), c1=(0.47, 0.70),
                par=(18, 4), tono=OCASO)


@toma(F("teul", 2) - 0.25, ("corte", 0))
def TE3(lz, t):
    PTE3.fondo(lz, t)
    PF.brillo(lz, *PTE3.P(t, 0.42, 0.40)[:2], 300, color=(1.0, 0.70, 0.40), inten=0.16, t=t, sem=4)
    desenfoca(lz, 2.0)
    quieto(lz, PTE3, t, "h06_abuelo/03", 0.40, 0.90, 0.40, tono=DORADO)
    quieto(lz, PTE3, t, "h04_ollin_nino/00", 0.54, 0.91, 0.20, flip=True, tono=DORADO, fase=0.5)


PTE4 = PF.Plano("e07_teul_cima_a", F("teul", 3) - 0.3, t1_("teul") + 0.8, z0=1.28, z1=1.06, c0=(0.40, 0.60), c1=(0.50, 0.52),
                par=(30, 7))
SILUETA = (0.55, 0.42, 0.46)


@toma(F("teul", 3) - 0.3, ("fundido", 0.8))
def TE4(lz, t):
    PTE4.fondo(lz, t)
    tinte(lz, (0.85, 0.55, 0.50), 0.18)
    PF.brillo(lz, *PTE4.P(t, 0.42, 0.08)[:2], 360, color=(1.0, 0.62, 0.36), inten=0.22, t=t, sem=4)
    aves(lz, t, VUELO_TE)
    quieto(lz, PTE4, t, "h01_tecuani/00", 0.29, 0.84, 0.36, tono=SILUETA)
    quieto(lz, PTE4, t, "h04_ollin_nino/02", 0.34, 0.86, 0.17, tono=SILUETA, fase=0.6)
    quieto(lz, PTE4, t, "h06_abuelo/05", 0.39, 0.84, 0.34, tono=SILUETA, fase=1.2)


# ================================================================== ACTO I — las noticias del sur (181,7-222,9 s)
PNT1 = PF.Plano("e08_camino_mercaderes_a", t0_("noticias") - 0.2, F("noticias", 1), z0=1.08, z1=1.16, c0=(0.50, 0.53),
                c1=(0.47, 0.55), par=(28, 6), tono=OCASO)
snd(t0_("noticias") + 0.1, "pasos", 0.3, dur=4.5)
snd(T("noticias", "sal", 0) - 0.1, "papel", 0.5)
snd(T("noticias", "conchas", 0) - 0.1, "pop", 0.45)


@toma(t0_("noticias") - 0.2, ("fundido", 0.6))
def NT1(lz, t):
    PNT1.fondo(lz, t)
    agua(lz, PNT1, t, "e08_camino_mercaderes_a")
    quieto(lz, PNT1, t, "h01_tecuani/00", 0.16, 0.88, 0.37, tono=OCASO)
    quieto(lz, PNT1, t, "h06_abuelo/04", 0.30, 0.86, 0.28, flip=True, tono=OCASO, fase=0.4)
    paseo(lz, PNT1, t, "h15_gente/03", t0_("noticias") - 0.2, t0_("noticias") + 4.6, 1.08, 0.64, 0.85, 0.35, pasos=1.6, tono=OCASO)
    PF.rotulo(lz, "SAL · CONCHAS · PLUMAS", W * 0.50, H * 0.19, 54, t, T("noticias", "sal", 0) - 0.1, F1("noticias", 0) + 0.3, rot=-1)
    pega(lz, "u01_utileria/15", W * 0.80, H * 0.36, 170, t, T("noticias", "conchas", 0) - 0.1, F1("noticias", 0) + 0.3, rot=8)


FUEGO_NT = (0.355, 0.785)            # centro del círculo de piedras pintado (previews/_aro.jpg)
PNT2 = PF.Plano("e08_camino_mercaderes_b", F("noticias", 1) - 0.3, F("noticias", 2), z0=1.10, z1=1.20, c0=(0.48, 0.54),
                c1=(0.46, 0.58), par=(26, 6))
_t_metal = T("noticias", "metal", 1)
snd(F("noticias", 1) - 0.3, "fuego", 0.45, dur=34.0)
snd(T("noticias", "tenochtitlan", 1) - 0.1, "papel", 0.5)
snd(_t_metal - 0.1, "clink", 0.35)


def corro(lz, pl, t, abuelo="h06_abuelo/04"):
    """Los tres alrededor de la fogata del camino (orden: lejos primero)."""
    hoguera(lz, pl, t, FUEGO_NT[0], FUEGO_NT[1], 0.10, tono=FOGATA, sem=5, pieza="u04_fuego_humo/00")
    quieto(lz, pl, t, "h15_gente/03", 0.21, 0.84, 0.33, tono=FOGATA)
    quieto(lz, pl, t, abuelo, 0.50, 0.85, 0.27, tono=FOGATA, fase=0.5)
    quieto(lz, pl, t, "h01_tecuani/00", 0.63, 0.88, 0.37, tono=FOGATA, fase=1.0)


@toma(F("noticias", 1) - 0.3, ("fundido", 0.5))
def NT2(lz, t):
    PNT2.fondo(lz, t)
    estrellas(lz, t, y1=0.22)
    corro(lz, PNT2, t)
    X, Y, s = PNT2.P(t, FUEGO_NT[0], 0.52)
    vision(lz, "u02_utileria_guerra/02", X - 70 * s, Y, 190 * s, t, _t_metal - 0.2, F1("noticias", 1) + 0.6)
    vision(lz, "u02_utileria_guerra/03", X + 80 * s, Y + 30 * s, 210 * s, t, _t_metal + 0.1, F1("noticias", 1) + 0.6)
    PF.rotulo(lz, "TENOCHTITLAN", W * 0.50, H * 0.19, 62, t, T("noticias", "tenochtitlan", 1) - 0.1, _t_metal - 0.4, rot=-1.2)


PNT3 = PF.Plano("e08_camino_mercaderes_b", F("noticias", 2) - 0.25, F("noticias", 3), z0=2.00, z1=2.10, c0=(0.36, 0.62),
                c1=(0.37, 0.62), par=(16, 3))
snd(F("noticias", 2) - 0.1, "galope", 0.28, dur=4.0)


@toma(F("noticias", 2) - 0.25, ("desenfoque", 0.4))
def NT3(lz, t):
    PNT3.fondo(lz, t)
    desenfoca(lz, 1.6)
    hoguera(lz, PNT3, t, FUEGO_NT[0], FUEGO_NT[1], 0.10, tono=FOGATA, sem=5, pieza="u04_fuego_humo/00")
    ta = F("noticias", 2) - 0.25
    u = clamp01((t - ta) / 4.6)
    q = int(t * 9) % PF.ciclo_n("c07_jinete_galope")
    vision(lz, f"c07_jinete_galope/ciclo_{q:02d}", lerp(W * 0.64, W * 0.40, u), H * 0.36, 470, t, ta + 0.1,
           F1("noticias", 2) - 0.1, flip=True, op=0.6, sube=6.0)


PNT4 = PF.Plano("e08_camino_mercaderes_b", F("noticias", 3) - 0.25, F("noticias", 4), z0=1.55, z1=1.60, c0=(0.44, 0.66),
                c1=(0.45, 0.66), par=(20, 4))
_t_tron = T("noticias", "tronaban", 3)
snd(_t_tron - 0.05, "trueno", 0.6)


@toma(F("noticias", 3) - 0.25, ("corte", 0))
def NT4(lz, t):
    PNT4.fondo(lz, t)
    corro(lz, PNT4, t)
    X, Y, s = PNT4.P(t, FUEGO_NT[0], 0.56)
    vision(lz, "u02_utileria_guerra/06", X, Y, 120 * s, t, T("noticias", "armas", 3) - 0.2, F1("noticias", 3) + 0.2, sube=8.0)
    relampago(lz, t, [_t_tron, _t_tron + 0.35])


PNT5 = PF.Plano("e08_camino_mercaderes_b", F("noticias", 4) - 0.2, F("noticias", 5), z0=1.75, z1=1.80, c0=(0.52, 0.68),
                c1=(0.52, 0.68), par=(16, 3))


@toma(F("noticias", 4) - 0.2, ("corte", 0))
def NT5(lz, t):
    PNT5.fondo(lz, t)
    hoguera(lz, PNT5, t, FUEGO_NT[0], FUEGO_NT[1], 0.10, tono=FOGATA, sem=5, pieza="u04_fuego_humo/00")
    desenfoca(lz, 2.2)
    X, Y, h = PNT5.en(t, 0.54, 0.90, 0.40)
    risa = 1.0 - smooth(prog(t, F("noticias", 4) + 2.6, F("noticias", 4) + 3.6))
    PF.actor(lz, "h06_abuelo/01", X, Y, h, tono=FOGATA, sy=1.0 + 0.02 * math.sin(t * 14) * risa, rot=1.5 * math.sin(t * 7) * risa)


PNT6 = PF.Plano("e09_canon_polvo_b", F("noticias", 5) - 0.3, t1_("noticias") + 0.6, z0=1.06, z1=1.36, c0=(0.50, 0.50),
                c1=(0.40, 0.45), par=(30, 7))
snd(F("noticias", 5) - 0.3, "viento", 0.22, dur=7.0)
snd(F("noticias", 5) + 0.5, "galope", 0.30, dur=6.0)
snd(F("noticias", 5) + 2.0, "tambor", 0.5, tono=0.6)


@toma(F("noticias", 5) - 0.3, ("fundido", 0.8))
def NT6(lz, t):
    PNT6.fondo(lz, t)
    ta = F("noticias", 5) - 0.3
    for k, (x, y) in enumerate([(0.30, 0.40), (0.34, 0.37), (0.38, 0.41), (0.42, 0.39), (0.27, 0.42)]):
        X, Y, s = PNT6.P(t, x, y)
        v = max(0.0, math.sin(t * (3.0 + k) + k * 1.3)) ** 4
        PF._blob(lz, X, Y, 9 * s, (1.0, 1.0, 0.95), 0.7 * v, aditivo=True)
    for k in range(3):
        polvo(lz, PNT6, t, 0.34 + 0.05 * k, 0.38, s=1.6, t_in=ta + 1.6 * k, dur=4.5, op=0.22, sem=k)
    PF.arena_viento(lz, t, fuerza=0.7, y0=0.60, sem=3)
    tinte(lz, (0.85, 0.62, 0.40), 0.25 * smooth(prog(t, ta, ta + 5.0)))


# ================================================================== ACTO II — la llegada (1530)
MIRA.update({"h13_aliados/03": -1, "h12_soldados/00": 1, "h12_soldados/01": 1, "h10_guzman/00": 1, "h12_soldados/04": 1})
AMB += [(t0_("llegada") - 0.3, F("llegada", 6), "alba", 0.40), (F("llegada", 6) - 0.3, t1_("llegada") + 0.3, "alba", 0.30),
        (t0_("chirinos") - 0.3, t1_("chirinos") + 0.3, "grillos", 0.28), (t0_("encomienda") - 0.3, t1_("encomienda") + 0.3, "alba", 0.32),
        (F("hierro", 3) - 0.3, F("hierro", 6), "alba", 0.30), (F("hierro", 6) - 0.3, t1_("hierro") + 0.3, "grillos", 0.25)]


def aleja(lz, pl, t, pieza, ta, tb, p0, p1, f0, f1, tono=None, pasos=1.8, flip=None):
    """Pieza que se aleja por un camino: de p0 a p1 del escenario, con el tamaño de f0 a f1 (perspectiva) y saltito de paso."""
    u = clamp01((t - ta) / max(tb - ta, 1e-3))
    x, y, f = lerp(p0[0], p1[0], u), lerp(p0[1], p1[1], u), lerp(f0, f1, u)
    fl = rumbo(pieza, p0[0], p1[0], False) if flip is None else flip
    X, Y, h = pl.en(t, x, y, f)
    mov = ta < t < tb
    ph = (t - ta) * pasos * math.pi
    PF.actor(lz, pieza, X, Y - (abs(math.sin(ph)) * 0.035 * h if mov else 0), h, flip=fl, tono=tono,
             rot=3.0 * math.sin(ph) if mov else 0.0)


PLL1 = PF.Plano("e09_canon_polvo_a", t0_("llegada"), F("llegada", 1), z0=1.06, z1=1.30, c0=(0.50, 0.50), c1=(0.45, 0.45), par=(30, 7))
_t_1530 = T("llegada", "1530", 0)
snd(t0_("llegada") + 0.4, "papel", 0.5)
snd(_t_1530 - 0.1, "tambor", 0.6, tono=0.6)
snd(t0_("llegada") + 0.5, "pasos", 0.22, dur=6.5)
snd(t0_("llegada") + 1.5, "galope", 0.18, dur=5.0)


@toma(t0_("llegada"), ("fundido", 0.8))
def LL1(lz, t):
    PLL1.fondo(lz, t)
    for k in range(4):
        polvo(lz, PLL1, t, 0.36 + 0.06 * k, 0.36, s=1.7, t_in=t0_("llegada") + 1.4 * k - 1.0, dur=5.0, op=0.22, sem=10 + k)
    for k, (x, y) in enumerate([(0.42, 0.40), (0.47, 0.37), (0.52, 0.41), (0.38, 0.42)]):
        X, Y, s = PLL1.P(t, x, y)
        v = max(0.0, math.sin(t * (3.0 + k) + k)) ** 4
        PF._blob(lz, X, Y, 8 * s, (1.0, 1.0, 0.95), 0.7 * v, aditivo=True)
    agua(lz, PLL1, t, "e09_canon_polvo_a")
    PF.arena_viento(lz, t, fuerza=0.6, y0=0.62, sem=5)
    capitulo(lz, t, "II", "LA LLEGADA", t0_("llegada") + 0.4, _t_1530 - 0.4)
    PF.rotulo(lz, "1530", W * 0.50, H * 0.42, 150, t, _t_1530 - 0.1, F1("llegada", 0) + 0.2, rot=-1.5)


PLL2 = PF.Plano("e13_camino_cargadores_b", F("llegada", 1) - 0.3, F("llegada", 2), z0=1.10, z1=1.16, c0=(0.50, 0.54),
                c1=(0.52, 0.56), par=(30, 6), tono=SOL_DURO)
_t_cas = T("llegada", "cascos", 1)
_t_per = T("llegada", "perros", 1)
snd(F("llegada", 1) - 0.3, "pasos", 0.5, dur=7.5)
snd(_t_cas - 0.3, "galope", 0.6, dur=4.0)
for _k in range(6):
    snd(F("llegada", 1) + _k * 1.2, "tambor", 0.35, tono=0.7)


@toma(F("llegada", 1) - 0.3, ("latigo", 0.45))
def LL2(lz, t):
    PLL2.fondo(lz, t)
    agua(lz, PLL2, t, "e13_camino_cargadores_b")
    ta = F("llegada", 1) - 0.3
    for k, (pz, d) in enumerate([("h12_soldados/00", 0.0), ("h12_soldados/01", 0.9), ("h12_soldados/02", 1.8)]):
        paseo(lz, PLL2, t, pz, ta + d, ta + d + 6.5, -0.12, 0.95, 0.82, 0.27, pasos=1.8, desde_antes=False, hasta_despues=False,
              tono=SOL_DURO)
    tropa(lz, PLL2, t, "c07_jinete_galope", _t_cas - 0.5, _t_cas + 4.0, -0.25, 1.25, 0.86, 0.26, n=3, dx=0.14, dy=0.01, paso=1.7,
          tono=SOL_DURO, desde_antes=False)
    anda(lz, PLL2, t, "c08_perro_corre", _t_per - 0.8, _t_per + 2.4, -0.15, 1.15, 0.91, 0.11, paso=1.6, tono=SOL_DURO)
    anda(lz, PLL2, t, "c08_perro_corre", _t_per - 0.5, _t_per + 2.7, -0.22, 1.10, 0.93, 0.12, paso=1.6, tono=SOL_DURO)
    polvo(lz, PLL2, t, 0.45, 0.80, s=2.0, t_in=_t_cas, dur=4.0, op=0.25, sem=3)
    PF.arena_viento(lz, t, fuerza=0.8, y0=0.70, sem=6)


PLL3 = PF.Plano("e10_pueblo_entrada_a", F("llegada", 2) - 0.3, F("llegada", 3), z0=1.10, z1=1.20, c0=(0.48, 0.545),
                c1=(0.45, 0.58), par=(28, 6), tono=SOL_DURO)
_t_chi = T("llegada", "chirinos", 2)
snd(F("llegada", 2) - 0.2, "galope", 0.45, dur=3.0)
snd(T("llegada", "guzmán", 2) - 0.1, "papel", 0.5)
snd(_t_chi - 0.1, "espada", 0.45)


@toma(F("llegada", 2) - 0.3, ("fundido", 0.5))
def LL3(lz, t):
    PLL3.fondo(lz, t)
    ta = F("llegada", 2) - 0.3
    quieto(lz, PLL3, t, "h15_gente/01", 0.30, 0.79, 0.22, tono=SOL_DURO, t_out=ta + 2.5)
    paseo(lz, PLL3, t, "h12_soldados/05", ta, ta + 4.0, -0.30, 0.20, 0.84, 0.32, pasos=1.6, tono=SOL_DURO)
    if t < _t_chi:
        paseo(lz, PLL3, t, "h10_guzman/00", ta, ta + 3.4, -0.18, 0.40, 0.89, 0.42, pasos=1.3, tono=SOL_DURO, salto=0.02)
    else:
        quieto(lz, PLL3, t, "h10_guzman/01", 0.40, 0.89, 0.42, tono=SOL_DURO)
    latido_rojo(lz, t, T("llegada", "miedo", 2) - 0.2, F1("llegada", 2) + 0.3, k=0.14)
    PF.rotulo(lz, "NUÑO DE GUZMÁN", W * 0.70, H * 0.19, 50, t, T("llegada", "guzmán", 2) - 0.1, F1("llegada", 2) + 0.2, rot=1.2)
    PF.rotulo(lz, "su capitán: CHIRINOS", W * 0.70, H * 0.30, 46, t, _t_chi - 0.1, F1("llegada", 2) + 0.2, rot=-1.0)


PLL4 = PF.Plano("e10_pueblo_entrada_b", F("llegada", 3) - 0.3, F("llegada", 4), z0=1.08, z1=1.14, c0=(0.50, 0.53),
                c1=(0.50, 0.55), par=(28, 6), tono=SOL_DURO)
snd(F("llegada", 3) - 0.2, "pasos", 0.45, dur=6.0)


@toma(F("llegada", 3) - 0.3, ("fundido", 0.5))
def LL4(lz, t):
    PLL4.fondo(lz, t)
    ta = F("llegada", 3) - 0.3
    paseo(lz, PLL4, t, "h13_aliados/03", ta, ta + 6.2, 1.10, 0.62, 0.80, 0.24, pasos=1.5, tono=SOL_DURO)
    paseo(lz, PLL4, t, "h13_aliados/02", ta, ta + 6.2, -0.35, 0.75, 0.84, 0.30, pasos=1.8, tono=SOL_DURO)
    tropa(lz, PLL4, t, "c06_aliado_marcha", ta, ta + 6.2, -0.25, 1.05, 0.89, 0.30, n=5, dx=0.10, dy=0.012, paso=1.0, tono=SOL_DURO)
    PF.arena_viento(lz, t, fuerza=0.5, y0=0.72, sem=7)


PLL5 = PF.Plano("e10_pueblo_entrada_a", F("llegada", 4) - 0.3, F("llegada", 5), z0=1.45, z1=1.48, c0=(0.62, 0.64), c1=(0.64, 0.65),
                par=(24, 5), tono=SOL_DURO)
_t_der = T("llegada", "derribaron", 4)
snd(_t_der - 0.05, "impacto", 0.7, tono=0.6)
snd(_t_der + 0.05, "crujido", 0.5, dur=0.9)


@toma(F("llegada", 4) - 0.3, ("corte", 0))
def LL5(lz, t):
    PLL5.fondo(lz, t)
    quieto(lz, PLL5, t, "h14_guerreros/00", 0.55, 0.86, 0.30, tono=SOL_DURO, t_out=_t_der + 0.2)
    quieto(lz, PLL5, t, "h14_guerreros/03", 0.71, 0.86, 0.30, flip=True, tono=SOL_DURO, t_out=_t_der + 0.2, fase=0.7)
    paseo(lz, PLL5, t, "h12_soldados/02", _t_der + 0.3, _t_der + 2.6, 0.36, 0.52, 0.88, 0.32, pasos=1.8, desde_antes=False,
          tono=SOL_DURO)
    caida = smooth(prog(t, _t_der, _t_der + 0.55))
    X, Y, h = PLL5.en(t, 0.63, 0.91, 0.11)
    PF.actor(lz, "u02_utileria_guerra/01", X, Y + 0.25 * h * caida, h, rot=-82 * caida, op=1.0 - smooth(prog(t, _t_der + 1.0, _t_der + 1.5)),
             tono=SOL_DURO)
    quieto(lz, PLL5, t, "u02_utileria_guerra/00", 0.63, 0.93, 0.09, tono=SOL_DURO, t_in=_t_der + 0.9)
    polvo(lz, PLL5, t, 0.63, 0.88, s=2.2, t_in=_t_der + 0.1, dur=3.0, op=0.35, sem=4)


PLL6 = PF.Plano("e10_pueblo_entrada_b", F("llegada", 5) - 0.3, F("llegada", 6), z0=1.60, z1=1.64, c0=(0.46, 0.66), c1=(0.46, 0.66),
                par=(18, 4), tono=SOL_DURO)
snd(F("llegada", 5) - 0.4, "fanfarria", 0.30)
snd(F("llegada", 5) - 0.1, "papel", 0.5)


@toma(F("llegada", 5) - 0.3, ("corte", 0))
def LL6(lz, t):
    PLL6.fondo(lz, t)
    desenfoca(lz, 1.6)
    quieto(lz, PLL6, t, "h12_soldados/00", 0.30, 0.86, 0.34, tono=SOL_DURO, fase=0.4)
    quieto(lz, PLL6, t, "h12_soldados/05", 0.63, 0.86, 0.36, tono=SOL_DURO, fase=1.1)
    quieto(lz, PLL6, t, "h11_espanoles_a_pie/00", 0.46, 0.92, 0.46, tono=SOL_DURO)
    PF.rotulo(lz, "EL REQUERIMIENTO", W * 0.50, H * 0.19, 60, t, F("llegada", 5) - 0.1, F1("llegada", 5) - 0.3, rot=-1.2)


PLL7 = PF.Plano("e20_rio_niebla_a", F("llegada", 6) - 0.3, t1_("llegada") + 0.6, z0=1.08, z1=1.18, c0=(0.52, 0.535),
                c1=(0.46, 0.57), par=(30, 6), tono=ALBA)
snd(F("llegada", 6) - 0.2, "pasos", 0.35, dur=6.5)
snd(F("llegada", 6) + 1.5, "chapuzon", 0.25)


@toma(F("llegada", 6) - 0.3, ("fundido", 0.6))
def LL7(lz, t):
    PLL7.fondo(lz, t)
    neblina(lz, t, 0.44, 0.64, fuerza=0.22, color=(0.90, 0.88, 0.94))
    agua(lz, PLL7, t, "e20_rio_niebla_a")
    ta, tb = F("llegada", 6) - 0.3, t1_("llegada") + 0.6
    paseo(lz, PLL7, t, "h15_gente/00", ta, tb, 0.78, 0.02, 0.83, 0.27, pasos=1.5, tono=ALBA)
    paseo(lz, PLL7, t, "h15_gente/01", ta, tb, 0.88, 0.12, 0.86, 0.31, pasos=1.8, tono=ALBA)
    paseo(lz, PLL7, t, "h15_gente/02", ta, tb, 0.98, 0.30, 0.88, 0.20, pasos=2.2, tono=ALBA)
    anda(lz, PLL7, t, "c12_citlali_camina", ta + 0.6, tb, 1.10, 0.40, 0.90, 0.36, desde_antes=True, tono=ALBA)
    paseo(lz, PLL7, t, "h04_ollin_nino/04", ta + 0.6, tb, 1.18, 0.52, 0.92, 0.18, pasos=2.6, tono=ALBA)
    anda(lz, PLL7, t, "c01_tecuani_camina", ta + 1.0, tb, 1.25, 0.62, 0.93, 0.39, desde_antes=True, tono=ALBA)
    plantas(lz, PLL7, t, [("u03_naturaleza/11", 0.06, 1.04, 0.34, 1.35, False)], tono=ALBA)


# ================================================================== ACTO II — el campamento de Chirinos (bando español)
PCH1 = PF.Plano("e12_campamento_a", t0_("chirinos") - 0.3, F("chirinos", 1), z0=1.08, z1=1.16, c0=(0.50, 0.53), c1=(0.47, 0.56),
                par=(28, 6), tono=OCASO)
snd(t0_("chirinos") - 0.2, "fuego", 0.35, dur=11.0)
snd(T("chirinos", "primavera", 0) - 0.1, "papel", 0.5)
snd(T("chirinos", "almíndez", 0) - 0.1, "papel", 0.5)
snd(T("chirinos", "cincuenta", 0) - 0.1, "papel", 0.5)


@toma(t0_("chirinos") - 0.3, ("fundido", 0.6))
def CH1(lz, t):
    PCH1.fondo(lz, t)
    brillo_en(lz, PCH1, t, 0.63, 0.71, 80, inten=0.45, sem=3, chis=10)
    humo_en(lz, PCH1, t, 0.63, 0.66, s=0.8, color=(0.40, 0.38, 0.40), op=0.22, sem=3)
    quieto(lz, PCH1, t, "h13_aliados/00", 0.90, 0.78, 0.24, tono=OCASO, fase=0.3)
    quieto(lz, PCH1, t, "h12_soldados/03", 0.79, 0.81, 0.27, tono=OCASO, fase=1.0)
    quieto(lz, PCH1, t, "h13_aliados/01", 0.10, 0.81, 0.27, tono=OCASO, fase=0.6)
    quieto(lz, PCH1, t, "h12_soldados/04", 0.21, 0.87, 0.33, tono=OCASO, fase=1.4)
    quieto(lz, PCH1, t, "h20_chirinos_pie/00", 0.43, 0.89, 0.39, tono=OCASO)
    PF.rotulo(lz, "PRIMAVERA DE 1530", W * 0.29, H * 0.19, 54, t, T("chirinos", "primavera", 0) - 0.1, F1("chirinos", 0) + 0.2,
              rot=-1.4)
    PF.rotulo(lz, "PEDRO ALMÍNDEZ CHIRINOS", W * 0.31, H * 0.29, 42, t, T("chirinos", "almíndez", 0) - 0.1,
              F1("chirinos", 0) + 0.2, rot=1.0)
    PF.rotulo(lz, "50 ESPAÑOLES · 500 ALIADOS", W * 0.68, H * 0.40, 42, t, T("chirinos", "cincuenta", 0) - 0.1,
              F1("chirinos", 0) + 0.2, rot=-1.0)


LINTERNA = (0.88, 0.92, 1.05)
PCH2 = PF.Plano("e42_tienda_chirinos_a", F("chirinos", 1) - 0.3, F("chirinos", 2), z0=1.15, z1=1.22, c0=(0.48, 0.56),
                c1=(0.45, 0.58), par=(20, 5), tono=LINTERNA)
snd(T("chirinos", "oro", 1) - 0.1, "papel", 0.5)


@toma(F("chirinos", 1) - 0.3, ("fundido", 0.5))
def CH2(lz, t):
    PCH2.fondo(lz, t)
    brillo_en(lz, PCH2, t, 0.35, 0.31, 70, color=(0.85, 0.92, 1.0), inten=0.30, sem=4)
    brillo_en(lz, PCH2, t, 0.62, 0.61, 50, inten=0.38, sem=5, chis=6)
    quieto(lz, PCH2, t, "h20_chirinos_pie/01", 0.40, 0.91, 0.48, tono=LINTERNA)
    PF.rotulo(lz, "ORO · ESCLAVOS · EL NORTE", W * 0.62, H * 0.19, 52, t, T("chirinos", "oro", 1) - 0.1, F1("chirinos", 1) + 0.3,
              rot=-1.2)


PCH3 = PF.Plano("e42_tienda_chirinos_b", F("chirinos", 2) - 0.25, F("chirinos", 3), z0=1.12, z1=1.16, c0=(0.50, 0.55),
                c1=(0.50, 0.555), par=(20, 5), tono=LINTERNA)
snd(F("chirinos", 2) - 0.2, "pasos", 0.4, dur=1.4)


@toma(F("chirinos", 2) - 0.25, ("corte", 0))
def CH3(lz, t):
    PCH3.fondo(lz, t)
    brillo_en(lz, PCH3, t, 0.35, 0.23, 60, color=(0.85, 0.92, 1.0), inten=0.30, sem=4)
    brillo_en(lz, PCH3, t, 0.55, 0.57, 45, inten=0.36, sem=5, chis=6)
    quieto(lz, PCH3, t, "h20_chirinos_pie/00", 0.31, 0.89, 0.46, tono=LINTERNA, fase=0.5)
    paseo(lz, PCH3, t, "h12_soldados/02", F("chirinos", 2) - 0.25, F("chirinos", 2) + 1.2, 0.86, 0.67, 0.90, 0.46, pasos=1.8,
          tono=LINTERNA)


PCH4 = PF.Plano("e42_tienda_chirinos_b", F("chirinos", 3) - 0.25, t1_("chirinos") + 0.4, z0=1.60, z1=1.70, c0=(0.34, 0.64),
                c1=(0.34, 0.65), par=(14, 3), tono=LINTERNA)
_t_herr = T("chirinos", "herradlo", 3)
snd(_t_herr - 0.05, "siseo", 0.55, dur=1.2)
snd(_t_herr - 0.05, "latido", 0.5)


@toma(F("chirinos", 3) - 0.25, ("corte", 0))
def CH4(lz, t):
    PCH4.fondo(lz, t)
    brillo_en(lz, PCH4, t, 0.55, 0.57, 45, inten=0.36, sem=5, chis=6)
    desenfoca(lz, 2.0)
    quieto(lz, PCH4, t, "h20_chirinos_pie/00", 0.32, 0.89, 0.46, tono=LINTERNA, fase=0.5)
    PF.brillo(lz, W * 0.80, H * 0.40, 200, color=(1.0, 0.30, 0.10), inten=0.30 * smooth(prog(t, _t_herr, _t_herr + 0.5)), t=t, sem=6)
    pega(lz, "u01_utileria/09", W * 0.80, H * 0.40, 150, t, _t_herr - 0.1, None, rot=-28)
    latido_rojo(lz, t, _t_herr, t1_("chirinos") + 0.4, k=0.16)


# ================================================================== ACTO II — el hierro
PHI1 = PF.Plano("e11_pueblo_quemado_a", t0_("hierro") - 0.3, F("hierro", 1), z0=1.08, z1=1.18, c0=(0.50, 0.53), c1=(0.50, 0.56),
                par=(28, 6), tono=INCENDIO)
FUEGOS_HI1 = [(0.20, 0.47), (0.33, 0.48), (0.70, 0.52), (0.62, 0.55)]
snd(t0_("hierro") - 0.3, "fuego", 0.6, dur=7.0)
snd(t0_("hierro") + 0.2, "galope", 0.45, dur=3.5)
snd(t0_("hierro") + 1.5, "crujido", 0.4, dur=0.9)


def incendio(lz, pl, t, lista, inten=0.45):
    for k, (x, y) in enumerate(lista):
        brillo_en(lz, pl, t, x, y, 90, inten=inten, sem=30 + k, chis=12)
        humo_en(lz, pl, t, x, y - 0.06, s=1.3, color=(0.12, 0.10, 0.10), op=0.30, sem=30 + k)


@toma(t0_("hierro") - 0.3, ("fundido", 0.6))
def HI1(lz, t):
    PHI1.fondo(lz, t)
    incendio(lz, PHI1, t, FUEGOS_HI1)
    tropa(lz, PHI1, t, "c07_jinete_galope", t0_("hierro") - 0.3, t0_("hierro") + 4.5, -0.25, 1.25, 0.86, 0.30, n=2, dx=0.18,
          paso=1.7, tono=(0.55, 0.40, 0.36), desde_antes=False)
    X, Y, s = PHI1.P(t, 0.45, 0.80)
    PF.chispas(lz, t, X, Y, s=s * 3.0, n=30, sem=8)


PHI2 = PF.Plano("e12_campamento_b", F("hierro", 1) - 0.3, F("hierro", 2), z0=1.10, z1=1.20, c0=(0.50, 0.545), c1=(0.52, 0.58),
                par=(26, 6), tono=OCASO)
_t_hie = T("hierro", "hierro", 1)
snd(_t_hie - 0.05, "siseo", 0.5, dur=1.0)


@toma(F("hierro", 1) - 0.3, ("fundido", 0.5))
def HI2(lz, t):
    PHI2.fondo(lz, t)
    brillo_en(lz, PHI2, t, 0.52, 0.78, 95, inten=0.50, sem=3, chis=12)
    humo_en(lz, PHI2, t, 0.52, 0.72, s=0.9, color=(0.40, 0.38, 0.40), op=0.22, sem=3)
    quieto(lz, PHI2, t, "h11_espanoles_a_pie/04", 0.76, 0.87, 0.38, tono=OCASO, fase=0.6)
    quieto(lz, PHI2, t, "h11_espanoles_a_pie/03", 0.36, 0.89, 0.40, tono=OCASO)
    PF.brillo(lz, W * 0.62, H * 0.27, 170, color=(1.0, 0.30, 0.10), inten=0.26 * smooth(prog(t, _t_hie, _t_hie + 0.5)), t=t, sem=6)
    pega(lz, "u01_utileria/09", W * 0.62, H * 0.27, 130, t, _t_hie - 0.1, F1("hierro", 1) + 0.2, rot=10)


PHI3 = PF.Plano("e11_pueblo_quemado_b", F("hierro", 2) - 0.25, F("hierro", 3), z0=1.55, z1=1.75, c0=(0.60, 0.66), c1=(0.62, 0.68),
                par=(16, 3), tono=INCENDIO)
snd(F("hierro", 2) - 0.2, "latido", 0.45)


@toma(F("hierro", 2) - 0.25, ("corte", 0))
def HI3(lz, t):
    PHI3.fondo(lz, t)
    incendio(lz, PHI3, t, [(0.20, 0.52), (0.35, 0.55), (0.55, 0.57)], inten=0.40)
    desenfoca(lz, 2.4)
    quieto(lz, PHI3, t, "h03_citlali/05", 0.62, 0.92, 0.40, tono=INCENDIO)
    latido_rojo(lz, t, F("hierro", 2) - 0.25, F1("hierro", 2) + 0.4, k=0.14)


PHI4 = PF.Plano("e13_camino_cargadores_a", F("hierro", 3) - 0.3, F("hierro", 4), z0=1.10, z1=1.16, c0=(0.50, 0.545),
                c1=(0.52, 0.56), par=(26, 6), tono=OCASO)
snd(T("hierro", "fardo", 3) - 0.1, "pop", 0.45, tono=0.8)
snd(T("hierro", "cuerda", 3) - 0.1, "pop", 0.45, tono=0.9)


@toma(F("hierro", 3) - 0.3, ("fundido", 0.6))
def HI4(lz, t):
    PHI4.fondo(lz, t)
    quieto(lz, PHI4, t, "h11_espanoles_a_pie/04", 0.27, 0.84, 0.36, tono=OCASO, fase=0.5)
    quieto(lz, PHI4, t, "h06_abuelo/02", 0.50, 0.87, 0.38, tono=OCASO)
    pega(lz, "u01_utileria/11", W * 0.78, H * 0.30, 190, t, T("hierro", "fardo", 3) - 0.1, F1("hierro", 3) + 0.3, rot=-6)
    pega(lz, "u01_utileria/10", W * 0.86, H * 0.52, 150, t, T("hierro", "cuerda", 3) - 0.1, F1("hierro", 3) + 0.3, rot=8)


PHI5 = PF.Plano("e13_camino_cargadores_a", F("hierro", 4) - 0.25, F("hierro", 5), z0=1.85, z1=1.90, c0=(0.52, 0.70), c1=(0.52, 0.70),
                par=(14, 3), tono=OCASO)


@toma(F("hierro", 4) - 0.25, ("corte", 0))
def HI5(lz, t):
    PHI5.fondo(lz, t)
    desenfoca(lz, 2.2)
    quieto(lz, PHI5, t, "h06_abuelo/03", 0.46, 0.92, 0.40, tono=OCASO)
    quieto(lz, PHI5, t, "h04_ollin_nino/05", 0.60, 0.93, 0.20, tono=OCASO, fase=0.6)


PHI6 = PF.Plano("e13_camino_cargadores_a", F("hierro", 5) - 0.3, F("hierro", 6), z0=1.20, z1=1.30, c0=(0.55, 0.58), c1=(0.50, 0.58),
                par=(28, 6), tono=OCASO)


@toma(F("hierro", 5) - 0.3, ("fundido", 0.6))
def HI6(lz, t):
    PHI6.fondo(lz, t)
    ta, tb = F("hierro", 5) - 0.3, F1("hierro", 5) + 0.6
    aleja(lz, PHI6, t, "h13_aliados/03", ta, tb, (0.36, 0.72), (0.20, 0.56), 0.22, 0.11, tono=OCASO)
    aleja(lz, PHI6, t, "h11_espanoles_a_pie/04", ta, tb, (0.40, 0.76), (0.24, 0.58), 0.28, 0.13, tono=OCASO)
    aleja(lz, PHI6, t, "h06_abuelo/02", ta, tb, (0.48, 0.81), (0.30, 0.62), 0.31, 0.15, tono=OCASO)
    quieto(lz, PHI6, t, "h01_tecuani/00", 0.64, 0.96, 0.50, tono=OCASO)
    quieto(lz, PHI6, t, "h03_citlali/03", 0.81, 0.96, 0.47, tono=OCASO, fase=0.7)
    quieto(lz, PHI6, t, "h04_ollin_nino/05", 0.725, 0.975, 0.22, tono=OCASO, fase=1.3)


PHI7 = PF.Plano("e21_casa_puerta_a", F("hierro", 6) - 0.3, t1_("hierro") + 0.4, z0=1.90, z1=1.95, c0=(0.40, 0.68), c1=(0.41, 0.68),
                par=(14, 3), tono=OCASO)


@toma(F("hierro", 6) - 0.3, ("fundido", 0.6))
def HI7(lz, t):
    PHI7.fondo(lz, t)
    desenfoca(lz, 2.0)
    quieto(lz, PHI7, t, "h04_ollin_nino/03", 0.40, 0.95, 0.62, tono=OCASO)


# ================================================================== ACTO II — la encomienda
PEN1 = PF.Plano("e14_granero_a", t0_("encomienda") - 0.3, F("encomienda", 1), z0=1.08, z1=1.16, c0=(0.50, 0.53), c1=(0.52, 0.56),
                par=(28, 6), tono=SOL_DURO)
snd(T("encomienda", "encomienda", 0) - 0.1, "sello", 0.5)
snd(T("encomienda", "alguien", 0) - 0.1, "papel", 0.4)


@toma(t0_("encomienda") - 0.3, ("fundido", 0.6))
def EN1(lz, t):
    PEN1.fondo(lz, t)
    ta = t0_("encomienda") - 0.3
    paseo(lz, PEN1, t, "h15_gente/03", ta, ta + 6.0, 0.08, 0.40, 0.85, 0.32, pasos=1.5, tono=SOL_DURO)
    quieto(lz, PEN1, t, "h11_espanoles_a_pie/01", 0.70, 0.88, 0.38, tono=SOL_DURO)
    paseo(lz, PEN1, t, "h01_tecuani/04", ta, ta + 6.0, 0.62, 0.36, 0.92, 0.37, pasos=1.3, tono=SOL_DURO)
    PF.arena_viento(lz, t, fuerza=0.4, y0=0.75, sem=8)
    PF.rotulo(lz, "ENCOMIENDA", W * 0.50, H * 0.20, 110, t, T("encomienda", "encomienda", 0) - 0.1, F1("encomienda", 0) + 0.2, rot=-1.5)
    PF.rotulo(lz, "= ahora éramos de alguien", W * 0.52, H * 0.32, 44, t, T("encomienda", "alguien", 0) - 0.1,
              F1("encomienda", 0) + 0.2, rot=1.0)


PEN2 = PF.Plano("e14_granero_b", F("encomienda", 1) - 0.3, F("encomienda", 2), z0=1.10, z1=1.18, c0=(0.50, 0.545), c1=(0.55, 0.56),
                par=(28, 6), tono=SOL_DURO)
_t_trab = T("encomienda", "trabajo", 1)
for _p in ("maíz", "mantas"):
    snd(T("encomienda", _p, 1) - 0.1, "pop", 0.45)


@toma(F("encomienda", 1) - 0.3, ("fundido", 0.5))
def EN2(lz, t):
    PEN2.fondo(lz, t)
    quieto(lz, PEN2, t, "h11_espanoles_a_pie/01", 0.73, 0.80, 0.30, tono=SOL_DURO)
    quieto(lz, PEN2, t, "u01_utileria/03", 0.56, 0.86, 0.08, tono=SOL_DURO, t_in=T("encomienda", "maíz", 1) - 0.1)
    quieto(lz, PEN2, t, "u01_utileria/11", 0.63, 0.87, 0.08, tono=SOL_DURO, t_in=T("encomienda", "mantas", 1) - 0.1)
    paseo(lz, PEN2, t, "h01_tecuani/04", _t_trab - 0.6, F("encomienda", 2) + 0.3, 1.02, 0.42, 0.93, 0.40, pasos=1.3,
          desde_antes=False, tono=SOL_DURO)


PEN3 = PF.Plano("e14_granero_a", F("encomienda", 2) - 0.25, F("encomienda", 3), z0=1.80, z1=1.86, c0=(0.66, 0.70), c1=(0.66, 0.70),
                par=(14, 3), tono=SOL_DURO)
_t_dep = T("encomienda", "deprisa", 2)
snd(_t_dep - 0.15, "zap", 0.40)


@toma(F("encomienda", 2) - 0.25, ("corte", 0))
def EN3(lz, t):
    PEN3.fondo(lz, t)
    desenfoca(lz, 2.0)
    sac = 6.0 * math.sin((t - _t_dep) * 30) * (1 - smooth(prog(t, _t_dep, _t_dep + 0.5))) if t >= _t_dep else 0.0
    quieto(lz, PEN3, t, "h11_espanoles_a_pie/01", 0.66, 0.92, 0.40, tono=SOL_DURO, rot=sac)


PEN4 = PF.Plano("e14_granero_b", F("encomienda", 3) - 0.3, F("encomienda", 4), z0=1.12, z1=1.18, c0=(0.50, 0.55), c1=(0.50, 0.555),
                par=(28, 6), tono=SOL_DURO)
_t_yo = T("encomienda", "yo", 3)


@toma(F("encomienda", 3) - 0.3, ("fundido", 0.5))
def EN4(lz, t):
    PEN4.fondo(lz, t)
    paseo(lz, PEN4, t, "h04_ollin_nino/04", F("encomienda", 3) - 0.3, _t_yo + 0.3, 0.04, 0.48, 0.90, 0.22, pasos=2.4, tono=SOL_DURO)
    paseo(lz, PEN4, t, "h01_tecuani/04", _t_yo - 0.4, F1("encomienda", 3) + 0.6, 1.05, 0.62, 0.93, 0.40, pasos=1.3,
          desde_antes=False, tono=SOL_DURO)
    PF.arena_viento(lz, t, fuerza=0.35, y0=0.76, sem=9)


PEN5 = PF.Plano("e15_capilla_a", F("encomienda", 4) - 0.3, F("encomienda", 5), z0=1.10, z1=1.20, c0=(0.48, 0.545), c1=(0.46, 0.58),
                par=(24, 5), tono=DORADO)
_t_juan = T("encomienda", "juan", 4)
_t_tec = T("encomienda", "tecuani", 5)
snd(F("encomienda", 4) - 0.3, "campana", 0.40, tono=0.8)
snd(F("encomienda", 4) + 2.0, "chorro", 0.30, dur=1.5)
snd(_t_juan - 0.1, "sello", 0.45)


@toma(F("encomienda", 4) - 0.3, ("fundido", 0.6))
def EN5(lz, t):
    PEN5.fondo(lz, t)
    quieto(lz, PEN5, t, "h11_espanoles_a_pie/02", 0.36, 0.86, 0.38, tono=DORADO)
    quieto(lz, PEN5, t, "h01_tecuani/05", 0.52, 0.88, 0.28, tono=DORADO, fase=0.4)
    PF.rotulo(lz, "JUAN", W * 0.50, H * 0.20, 110, t, _t_juan - 0.1, _t_tec - 0.3, rot=-2.0)


PEN6 = PF.Plano("e15_capilla_b", F("encomienda", 5) - 0.25, F("encomienda", 6), z0=1.80, z1=1.86, c0=(0.50, 0.68), c1=(0.50, 0.68),
                par=(14, 3), tono=DORADO)
snd(_t_tec - 0.3, "papel", 0.6)
snd(_t_tec - 0.05, "tambor", 0.5, tono=0.8)


@toma(F("encomienda", 5) - 0.25, ("corte", 0))
def EN6(lz, t):
    PEN6.fondo(lz, t)
    desenfoca(lz, 2.0)
    quieto(lz, PEN6, t, "h01_tecuani/05", 0.50, 0.90, 0.34, tono=DORADO)
    PF.rotulo(lz, "JUAN", W * 0.50, H * 0.20, 110, t, F("encomienda", 5) - 0.25, _t_tec - 0.3, rot=-2.0, salida=0.25)
    PF.rotulo(lz, "TECUANI", W * 0.50, H * 0.21, 120, t, _t_tec - 0.05, F1("encomienda", 5) + 0.6, rot=1.5, tinta=(120, 24, 14))


PEN7 = PF.Plano("e16_guadalajara_nochistlan_a", F("encomienda", 6) - 0.3, t1_("encomienda") + 0.4, z0=1.06, z1=1.18,
                c0=(0.50, 0.50), c1=(0.56, 0.52), par=(28, 6), tono=SOL_DURO)
_t_neg = T("encomienda", "negaron", 6)
snd(T("encomienda", "1532", 6) - 0.1, "papel", 0.5)
snd(T("encomienda", "guadalajara", 6) - 0.1, "papel", 0.5)
snd(_t_neg + 0.2, "impacto", 0.55, tono=0.7)


@toma(F("encomienda", 6) - 0.3, ("fundido", 0.6))
def EN7(lz, t):
    PEN7.fondo(lz, t)
    quieto(lz, PEN7, t, "h12_soldados/05", 0.50, 0.62, 0.12, tono=SOL_DURO)
    quieto(lz, PEN7, t, "h11_espanoles_a_pie/00", 0.45, 0.64, 0.12, tono=SOL_DURO, fase=0.5)
    quieto(lz, PEN7, t, "h12_soldados/00", 0.58, 0.66, 0.13, tono=SOL_DURO, fase=1.0)
    quieto(lz, PEN7, t, "h15_gente/03", 0.13, 0.91, 0.38, tono=SOL_DURO, t_in=_t_neg - 0.4)
    quieto(lz, PEN7, t, "h01_tecuani/00", 0.26, 0.93, 0.42, tono=SOL_DURO, t_in=_t_neg - 0.2)
    quieto(lz, PEN7, t, "u02_utileria_guerra/01", 0.36, 0.94, 0.06, tono=SOL_DURO, t_in=_t_neg + 0.2)
    PF.rotulo(lz, "1532", W * 0.27, H * 0.19, 90, t, T("encomienda", "1532", 6) - 0.1, t1_("encomienda") - 0.2, rot=-1.5)
    PF.rotulo(lz, "GUADALAJARA", W * 0.29, H * 0.30, 54, t, T("encomienda", "guadalajara", 6) - 0.1, t1_("encomienda") - 0.2, rot=1.0)


# ================================================================== ACTO II — la cédula de 1536
PCE1 = PF.Plano("e39_galeon_b", t0_("cedula") - 0.3, F("cedula", 1), z0=1.08, z1=1.25, c0=(0.50, 0.53), c1=(0.58, 0.48), par=(26, 6))
snd(t0_("cedula") - 0.2, "ola", 0.35, dur=2.0)
snd(t0_("cedula") + 4.0, "ola", 0.30, dur=2.0)
snd(t0_("cedula") + 0.3, "trueno", 0.30)
snd(T("cedula", "1536", 0) - 0.1, "papel", 0.5)


@toma(t0_("cedula") - 0.3, ("fundido", 0.8))
def CE1(lz, t):
    PCE1.fondo(lz, t)
    relampago(lz, t, [t0_("cedula") + 0.2])
    lluvia(lz, t, n=120, fuerza=0.18, viento=0.25, sem=9)
    pega(lz, "u01_utileria/13", W * 0.30, H * 0.48, 330, t, T("cedula", "orden", 0) - 0.1, F1("cedula", 0) + 0.3, rot=-5)
    PF.rotulo(lz, "REAL CÉDULA · 1536", W * 0.30, H * 0.19, 56, t, T("cedula", "1536", 0) - 0.1, F1("cedula", 0) + 0.3, rot=-1.2)
    PF.rotulo(lz, "MUJERES Y NIÑOS MENORES DE 14 AÑOS", W * 0.64, H * 0.80, 38, t, T("cedula", "mujeres", 0) - 0.1,
              F1("cedula", 0) + 0.3, rot=1.0)


PCE2 = PF.Plano("e12_campamento_b", F("cedula", 1) - 0.3, t1_("cedula") + 0.6, z0=2.0, z1=2.08, c0=(0.52, 0.70), c1=(0.52, 0.71),
                par=(12, 3), tono=OCASO)
_t_lleg = F("cedula", 1) - 0.2
_t_sig = T("cedula", "siguió", 1)
snd(_t_lleg + 1.0, "fuego", 0.5, dur=5.0)
snd(_t_sig - 0.1, "siseo", 0.5, dur=1.0)


@toma(F("cedula", 1) - 0.3, ("fundido", 0.5))
def CE2(lz, t):
    PCE2.fondo(lz, t)
    brillo_en(lz, PCE2, t, 0.52, 0.78, 90, inten=0.55, sem=3, chis=14)
    X1, Y1, s = PCE2.P(t, 0.52, 0.74)
    u = smooth(prog(t, _t_lleg, _t_lleg + 1.3))
    arde = smooth(prog(t, _t_lleg + 1.2, _t_lleg + 2.6))
    X, Y = lerp(W * 0.46, X1, u), lerp(H * 0.18, Y1, u)
    if arde < 0.99:
        PF.actor(lz, "u01_utileria/13", X, Y, 260 * (1 - 0.4 * u), rot=-8 + 40 * u, op=1.0 - arde, ancla=(0.5, 0.5), suelo=0,
                 tono=(1.0 - 0.6 * arde, 0.85 - 0.6 * arde, 0.75 - 0.6 * arde))
        if arde > 0.01:
            PF.chispas(lz, t, X, Y, s=2.5, n=20, sem=4)
    PF.brillo(lz, W * 0.70, H * 0.40, 200, color=(1.0, 0.30, 0.10), inten=0.26 * smooth(prog(t, _t_sig, _t_sig + 0.4)), t=t, sem=6)
    pega(lz, "u01_utileria/09", W * 0.70, H * 0.36, 160, t, _t_sig - 0.1, None, rot=10)


# ================================================================== ACTO III — el llamado (1540)
MIRA.update({"h11_espanoles_a_pie/01": -1, "h09_corredor/00": 1, "h07_profeta/03": -1})
AMB += [(t0_("diez") - 0.3, F("diez", 3), "alba", 0.40), (F("diez", 3) - 0.3, t1_("diez") + 0.3, "alba", 0.45),
        (t0_("tlatol") - 0.3, F("tlatol", 5), "grillos", 0.30), (F("tlatol", 5) - 0.3, t1_("tlatol") + 0.3, "alba", 0.35),
        (t0_("llamado") - 0.3, t1_("llamado") + 0.3, "alba", 0.38), (t0_("decision") - 0.3, F("decision", 3), "grillos", 0.28)]


def flecha_diana(lz, pl, t, t_i, dur, p0, p1, color=(0.16, 0.11, 0.08)):
    """Flecha del arco (p0) a la diana (p1), en coordenadas del escenario: vuela en parábola y se queda clavada temblando."""
    if t < t_i:
        return
    X0, Y0, _ = pl.P(t, *p0)
    X1, Y1, s = pl.P(t, *p1)
    u = min(1.0, (t - t_i) / dur)
    X = lerp(X0, X1, u)
    Y = lerp(Y0, Y1, u) - 60 * s * math.sin(math.pi * u)
    if u < 1.0:
        u2 = min(1.0, u + 0.03)
        a = math.atan2(lerp(Y0, Y1, u2) - 60 * s * math.sin(math.pi * u2) - Y, lerp(X0, X1, u2) - X)
    else:
        a = math.atan2(Y1 - Y0, X1 - X0) + 0.05 * math.sin((t - t_i - dur) * 40) * math.exp(-(t - t_i - dur) * 4)
    L = 70 * s
    Xa, Ya = X - math.cos(a) * L, Y - math.sin(a) * L
    cv2.line(lz, (int(Xa), int(Ya)), (int(X), int(Y)), color, max(2, int(2 * s)), cv2.LINE_AA)
    for da in (0.5, -0.5):
        cv2.line(lz, (int(Xa), int(Ya)), (int(Xa - math.cos(a + da) * 12 * s), int(Ya - math.sin(a + da) * 12 * s)), (0.85, 0.82, 0.76),
                 2, cv2.LINE_AA)


def pedradas(lz, t, lanzas, tono=None):
    """Piedras lanzadas en pantalla: [(t_ini, dur, (x0, y0), (x1, y1), alto px, sem)] en 0..1, parábola y giro."""
    for t_i, dur, p0, p1, hpx, sem in lanzas:
        u = (t - t_i) / dur
        if not 0 <= u <= 1:
            continue
        x = lerp(p0[0], p1[0], u) * W
        y = (lerp(p0[1], p1[1], u) - 0.22 * math.sin(math.pi * u)) * H
        PF.actor(lz, "u03_naturaleza/07", x, y, hpx, rot=(u * 540 + sem * 50) % 360, tono=tono, ancla=(0.5, 0.5), suelo=0, sombra=False)


# ------------------------------------------------------------------ diez años
PDI1 = PF.Plano("e21_casa_puerta_b", t0_("diez"), F("diez", 1), z0=1.25, z1=1.32, c0=(0.50, 0.60), c1=(0.52, 0.61), par=(26, 6),
                tono=DORADO)
_t_diez2 = T("diez", "diez", 0, n=1)
snd(t0_("diez") + 0.3, "papel", 0.5)
snd(_t_diez2 - 0.3, "crece", 0.35, dur=1.2)


@toma(t0_("diez"), ("fundido", 0.8))
def DI1(lz, t):
    PDI1.fondo(lz, t)
    u = smooth(prog(t, _t_diez2 - 0.5, _t_diez2 + 0.9))
    if u < 0.99:
        quieto(lz, PDI1, t, "h04_ollin_nino/00", 0.56, 0.86, 0.19, tono=DORADO, op=1 - u)
    if u > 0.01:
        quieto(lz, PDI1, t, "h05_ollin_joven/01", 0.56, 0.86, 0.36, tono=DORADO, op=u)
    capitulo(lz, t, "III", "EL LLAMADO", t0_("diez") + 0.3, F("diez", 0) + 2.4)
    PF.rotulo(lz, "1530 … 1540", W * 0.50, H * 0.20, 64, t, F("diez", 0) + 2.6, F1("diez", 0) + 0.3, rot=-1.2)


PDI2 = PF.Plano("e17_barranca_arco_a", F("diez", 1) - 0.3, F("diez", 2), z0=1.10, z1=1.18, c0=(0.48, 0.545), c1=(0.46, 0.56),
                par=(28, 6), tono=DORADO)
_t_arco = T("diez", "arco", 1)
snd(_t_arco + 0.2, "whoosh", 0.4, dur=0.4)
snd(_t_arco + 0.85, "golpe_suave", 0.5)


@toma(F("diez", 1) - 0.3, ("fundido", 0.6))
def DI2(lz, t):
    PDI2.fondo(lz, t)
    quieto(lz, PDI2, t, "h01_tecuani/00", 0.18, 0.89, 0.40, tono=DORADO)
    quieto(lz, PDI2, t, "h05_ollin_joven/00", 0.30, 0.89, 0.38, tono=DORADO, fase=0.6)
    flecha_diana(lz, PDI2, t, _t_arco + 0.2, 0.65, (0.36, 0.73), (0.53, 0.63))
    PF.chispas(lz, t, *PDI2.P(t, 0.70, 0.45)[:2], s=1.5, n=8, sem=3)


PDI3 = PF.Plano("e17_barranca_arco_b", F("diez", 2) - 0.25, F("diez", 3), z0=1.55, z1=1.62, c0=(0.42, 0.66), c1=(0.44, 0.66),
                par=(18, 4), tono=DORADO)
_t_sabes = T("diez", "sabes", 2)
snd(_t_sabes + 0.05, "whoosh", 0.45, dur=0.4)
snd(_t_sabes + 0.65, "golpe_suave", 0.55)


@toma(F("diez", 2) - 0.25, ("corte", 0))
def DI3(lz, t):
    PDI3.fondo(lz, t)
    quieto(lz, PDI3, t, "h01_tecuani/00", 0.22, 0.92, 0.44, tono=DORADO)
    quieto(lz, PDI3, t, "h05_ollin_joven/00", 0.36, 0.92, 0.42, tono=DORADO, fase=0.6)
    flecha_diana(lz, PDI3, t, _t_sabes + 0.05, 0.6, (0.43, 0.75), (0.63, 0.61))


PDI4 = PF.Plano("e18_camino_norte_a", F("diez", 3) - 0.3, F("diez", 4), z0=1.08, z1=1.22, c0=(0.50, 0.53), c1=(0.56, 0.52),
                par=(28, 6), tono=OCASO)
snd(T("diez", "1540", 3) - 0.1, "papel", 0.5)
snd(T("diez", "ciudades", 3) - 0.1, "papel", 0.5)


@toma(F("diez", 3) - 0.3, ("fundido", 0.6))
def DI4(lz, t):
    PDI4.fondo(lz, t)
    for k in range(3):
        polvo(lz, PDI4, t, 0.66 + 0.05 * k, 0.36, s=1.2, t_in=F("diez", 3) - 0.3 + 2.0 * k, dur=5.5, op=0.20, sem=20 + k)
    agua(lz, PDI4, t, "e18_camino_norte_a")
    quieto(lz, PDI4, t, "h01_tecuani/00", 0.30, 0.92, 0.40, tono=OCASO)
    quieto(lz, PDI4, t, "h05_ollin_joven/01", 0.40, 0.93, 0.38, tono=OCASO, fase=0.8)
    PF.rotulo(lz, "1540 · AL NORTE", W * 0.62, H * 0.19, 56, t, T("diez", "1540", 3) - 0.1, F1("diez", 3) + 0.3, rot=-1.2)
    PF.rotulo(lz, "en busca de las ciudades de oro", W * 0.64, H * 0.29, 40, t, T("diez", "ciudades", 3) - 0.1, F1("diez", 3) + 0.3,
              rot=1.0)


PDI5 = PF.Plano("e18_camino_norte_b", F("diez", 4) - 0.3, t1_("diez") + 0.5, z0=1.12, z1=1.06, c0=(0.50, 0.55), c1=(0.50, 0.52),
                par=(28, 6), tono=OCASO)
snd(F("diez", 4) - 0.2, "galope", 0.35, dur=4.5)
snd(F("diez", 4) + 3.5, "viento", 0.18, dur=4.0)


@toma(F("diez", 4) - 0.3, ("fundido", 0.5))
def DI5(lz, t):
    PDI5.fondo(lz, t)
    ta = F("diez", 4) - 0.3
    tropa(lz, PDI5, t, "c07_jinete_galope", ta, ta + 7.5, 0.05, 1.25, 0.87, 0.20, n=4, dx=0.10, dy=0.01, paso=1.7, tono=OCASO)
    paseo(lz, PDI5, t, "h12_soldados/00", ta, ta + 6.5, 0.05, 1.15, 0.89, 0.24, pasos=1.8, hasta_despues=False, tono=OCASO)
    polvo(lz, PDI5, t, 0.70, 0.84, s=2.0, t_in=ta + 2.5, dur=5.0, op=0.25, sem=6)
    PF.arena_viento(lz, t, fuerza=0.6, y0=0.70, sem=11)


# ------------------------------------------------------------------ el tlatol
PTL1 = PF.Plano("e19_fogata_tlatol_a", t0_("tlatol") - 0.3, F("tlatol", 1), z0=1.08, z1=1.16, c0=(0.50, 0.53), c1=(0.53, 0.56),
                par=(26, 6), tono=NOCHE_FUEGO)
snd(t0_("tlatol") - 0.2, "fuego", 0.35, dur=35.0)
snd(T("tlatol", "tlatol", 0) - 0.1, "papel", 0.5)
snd(T("tlatol", "tecoroli", 0) - 0.1, "papel", 0.5)


@toma(t0_("tlatol") - 0.3, ("fundido", 0.6))
def TL1(lz, t):
    PTL1.fondo(lz, t)
    estrellas(lz, t, y1=0.22)
    quieto(lz, PTL1, t, "h15_gente/01", 0.18, 0.84, 0.30, tono=NOCHE_FUEGO, fase=0.3)
    quieto(lz, PTL1, t, "h15_gente/05", 0.30, 0.88, 0.20, tono=NOCHE_FUEGO, fase=0.9)
    hoguera(lz, PTL1, t, 0.62, 0.79, 0.12, tono=FOGATA, sem=7, pieza="u04_fuego_humo/00")
    quieto(lz, PTL1, t, "h07_profeta/03", 0.80, 0.87, 0.36, tono=FOGATA)
    quieto(lz, PTL1, t, "h01_tecuani/00", 0.44, 0.91, 0.40, tono=NOCHE_FUEGO, fase=1.4)
    PF.rotulo(lz, "TLATOL = la palabra", W * 0.30, H * 0.19, 52, t, T("tlatol", "tlatol", 0) - 0.1, F1("tlatol", 0) + 0.3, rot=-1.2)
    PF.rotulo(lz, "de Tecoroli", W * 0.31, H * 0.29, 42, t, T("tlatol", "tecoroli", 0) - 0.1, F1("tlatol", 0) + 0.3, rot=1.0)


PTL2 = PF.Plano("e19_fogata_tlatol_b", F("tlatol", 1) - 0.25, F("tlatol", 2), z0=1.60, z1=1.66, c0=(0.50, 0.66), c1=(0.51, 0.66),
                par=(18, 4), tono=FOGATA)
snd(F("tlatol", 1) - 0.2, "tambor", 0.55, tono=0.7)


@toma(F("tlatol", 1) - 0.25, ("corte", 0))
def TL2(lz, t):
    PTL2.fondo(lz, t)
    hoguera(lz, PTL2, t, 0.56, 0.82, 0.12, tono=FOGATA, sem=7, pieza="u04_fuego_humo/00")
    desenfoca(lz, 1.8)
    quieto(lz, PTL2, t, "h07_profeta/00", 0.50, 0.92, 0.44, tono=FOGATA, rot=1.5 * math.sin(t * 6))


PTL3 = PF.Plano("e19_fogata_tlatol_a", F("tlatol", 2) - 0.25, F("tlatol", 3), z0=1.70, z1=1.76, c0=(0.60, 0.69), c1=(0.60, 0.69),
                par=(16, 3), tono=FOGATA)
_t_mor = T("tlatol", "morirá", 2)
snd(_t_mor - 0.1, "latido", 0.5)


@toma(F("tlatol", 2) - 0.25, ("corte", 0))
def TL3(lz, t):
    PTL3.fondo(lz, t)
    hoguera(lz, PTL3, t, 0.62, 0.79, 0.12, tono=FOGATA, sem=7, pieza="u04_fuego_humo/00")
    desenfoca(lz, 2.0)
    X, Y, s = PTL3.P(t, 0.70, 0.55)
    tv = T("tlatol", "milpas", 2) - 0.1
    vision(lz, "u03_naturaleza/05", X + 120, Y, 200 + 160 * smooth(prog(t, tv, tv + 2.5)), t, tv, _t_mor - 0.3, sube=4.0)
    quieto(lz, PTL3, t, "h07_profeta/02", 0.52, 0.92, 0.42, tono=FOGATA)
    latido_rojo(lz, t, _t_mor - 0.1, F1("tlatol", 2) + 0.5, k=0.18)


PTL4 = PF.Plano("e19_fogata_tlatol_b", F("tlatol", 3) - 0.2, F("tlatol", 4), z0=1.12, z1=1.20, c0=(0.50, 0.55), c1=(0.48, 0.52),
                par=(26, 6), tono=NOCHE_FUEGO)
snd(F("tlatol", 3) - 0.1, "cuerno", 0.45, tono=0.8)


@toma(F("tlatol", 3) - 0.2, ("corte", 0))
def TL4(lz, t):
    PTL4.fondo(lz, t)
    estrellas(lz, t, y1=0.25)
    hoguera(lz, PTL4, t, 0.56, 0.82, 0.12, tono=FOGATA, sem=7, pieza="u04_fuego_humo/00")
    quieto(lz, PTL4, t, "h15_gente/01", 0.18, 0.86, 0.32, tono=NOCHE_FUEGO, fase=0.4)
    quieto(lz, PTL4, t, "h05_ollin_joven/02", 0.32, 0.91, 0.40, tono=NOCHE_FUEGO, t_in=F("tlatol", 3) + 1.0)
    quieto(lz, PTL4, t, "h07_profeta/03", 0.74, 0.89, 0.42, tono=FOGATA)


PTL5 = PF.Plano("e19_fogata_tlatol_a", F("tlatol", 4) - 0.3, F("tlatol", 5), z0=1.30, z1=1.10, c0=(0.58, 0.62), c1=(0.55, 0.56),
                par=(28, 6), tono=FOGATA)
_tt0, _tt1 = F("tlatol", 4) - 0.2, F1("tlatol", 4)
_kt = 0
while _tt0 + _kt * 0.45 < _tt1:
    snd(_tt0 + _kt * 0.45, "tambor", 0.45 if _kt % 2 else 0.6, tono=1.0 if _kt % 2 else 0.8)
    _kt += 1


@toma(F("tlatol", 4) - 0.3, ("fundido", 0.6))
def TL5(lz, t):
    PTL5.fondo(lz, t)
    estrellas(lz, t, y1=0.22)
    ronda(lz, PTL5, t, "c10_danza", 0.62, 0.78, 0.22, 0.07, 8, 0.45, 0.20, 0.45, tono=FOGATA, mitad="atras")
    hoguera(lz, PTL5, t, 0.62, 0.79, 0.16, tono=FOGATA, sem=8)
    quieto(lz, PTL5, t, "h07_profeta/04", 0.62, 0.80, 0.30, tono=FOGATA, rot=6 * math.sin(t * 5))
    ronda(lz, PTL5, t, "c10_danza", 0.62, 0.78, 0.22, 0.07, 8, 0.45, 0.20, 0.45, tono=FOGATA, mitad="delante")
    alba = smooth(prog(t, F1("tlatol", 4) - 2.0, F1("tlatol", 4) + 0.3))
    tinte(lz, (1.0, 0.75, 0.80), 0.30 * alba)


PTL6 = PF.Plano("e14_granero_a", F("tlatol", 5) - 0.3, t1_("tlatol") + 0.4, z0=1.12, z1=1.20, c0=(0.55, 0.55), c1=(0.60, 0.56),
                par=(28, 6), tono=SOL_DURO)
_tp0 = F("tlatol", 5) + 0.8
PIEDRAS_TL = [(_tp0 + 0.5 * k, 1.1, (0.18, 0.62), (0.62 + 0.05 * (k % 3) + 0.06 * max(0, k - 2), 0.70), 46 - 6 * (k % 2), k) for k in range(8)]
for _k in range(8):
    snd(_tp0 + 0.5 * _k + 1.05, "golpe_suave", 0.35)


@toma(F("tlatol", 5) - 0.3, ("fundido", 0.5))
def TL6(lz, t):
    PTL6.fondo(lz, t)
    quieto(lz, PTL6, t, "h14_guerreros/00", 0.22, 0.89, 0.37, tono=SOL_DURO)
    quieto(lz, PTL6, t, "h14_guerreros/02", 0.34, 0.86, 0.32, tono=SOL_DURO, fase=0.6)
    if t < _tp0 + 1.2:
        quieto(lz, PTL6, t, "h11_espanoles_a_pie/01", 0.64, 0.88, 0.37, tono=SOL_DURO)
    else:
        paseo(lz, PTL6, t, "h11_espanoles_a_pie/01", _tp0 + 1.2, _tp0 + 4.6, 0.64, 1.15, 0.88, 0.37, pasos=3.2, salto=0.06,
              tono=SOL_DURO)
    pedradas(lz, t, PIEDRAS_TL, tono=SOL_DURO)
    polvo(lz, PTL6, t, 0.74, 0.88, s=1.4, t_in=_tp0 + 1.5, dur=3.0, op=0.25, sem=5)


# ------------------------------------------------------------------ el llamado
PLM1 = PF.Plano("e21_casa_puerta_b", t0_("llamado") - 0.3, F("llamado", 1), z0=1.10, z1=1.20, c0=(0.48, 0.545), c1=(0.45, 0.58),
                par=(26, 6), tono=DORADO)
_t_cub = T("llamado", "cubierto", 0)
snd(t0_("llamado") - 0.2, "pasos", 0.45, dur=3.5)


@toma(t0_("llamado") - 0.3, ("fundido", 0.6))
def LM1(lz, t):
    PLM1.fondo(lz, t)
    quieto(lz, PLM1, t, "h01_tecuani/00", 0.30, 0.84, 0.34, tono=DORADO)
    quieto(lz, PLM1, t, "h03_citlali/04", 0.62, 0.82, 0.30, tono=DORADO, fase=0.6)
    if t < _t_cub:
        paseo(lz, PLM1, t, "h09_corredor/00", t0_("llamado") - 0.3, _t_cub - 0.3, -0.15, 0.44, 0.88, 0.35, pasos=3.6, salto=0.06,
              tono=DORADO)
        polvo(lz, PLM1, t, 0.20, 0.88, s=1.0, t_in=t0_("llamado"), dur=3.0, op=0.22, sem=8)
    else:
        quieto(lz, PLM1, t, "h09_corredor/01", 0.44, 0.88, 0.30, tono=DORADO, rot=1.5 * math.sin(t * 9))


PLM2 = PF.Plano("e21_casa_puerta_b", F("llamado", 1) - 0.25, F("llamado", 2), z0=1.70, z1=1.76, c0=(0.48, 0.68), c1=(0.48, 0.68),
                par=(16, 3), tono=DORADO)
_t_ya = T("llamado", "ya", 1)
snd(T("llamado", "tenamaxtli", 1) - 0.1, "papel", 0.5)
snd(_t_ya - 0.05, "tambor", 0.6, tono=0.7)


@toma(F("llamado", 1) - 0.25, ("corte", 0))
def LM2(lz, t):
    PLM2.fondo(lz, t)
    desenfoca(lz, 2.0)
    pz = "h09_corredor/02" if t < _t_ya - 0.15 else "h09_corredor/03"
    quieto(lz, PLM2, t, pz, 0.48, 0.92, 0.42, tono=DORADO)
    PF.rotulo(lz, "TENAMAXTLI", W * 0.74, H * 0.20, 70, t, T("llamado", "tenamaxtli", 1) - 0.1, F1("llamado", 1) + 0.3, rot=-1.5)
    PF.rotulo(lz, "AL MIXTÓN", W * 0.74, H * 0.32, 56, t, T("llamado", "mixtón", 1) - 0.1, F1("llamado", 1) + 0.3, rot=1.2)


PLM3 = PF.Plano("e23_subida_mixton_a", F("llamado", 2) - 0.3, t1_("llamado") + 0.5, z0=1.06, z1=1.22, c0=(0.50, 0.50),
                c1=(0.48, 0.47), par=(30, 7), tono=DORADO)
snd(F("llamado", 2) - 0.2, "cuerno", 0.35, tono=0.7)
snd(F("llamado", 2) + 2.5, "cuerno", 0.25, tono=0.6)


@toma(F("llamado", 2) - 0.3, ("fundido", 0.7))
def LM3(lz, t):
    PLM3.fondo(lz, t)
    aves(lz, t, [(F("llamado", 2) - 0.5, 9.0, 0.22, 0.16, 60, -1, 0.5)])
    quieto(lz, PLM3, t, "h01_tecuani/00", 0.26, 0.82, 0.26, tono=DORADO)


# ------------------------------------------------------------------ la decisión
PDE1 = PF.Plano("e22_casa_noche_a", t0_("decision") - 0.3, F("decision", 1), z0=1.25, z1=1.32, c0=(0.48, 0.60), c1=(0.47, 0.61),
                par=(20, 5), tono=INTERIOR)


@toma(t0_("decision") - 0.3, ("fundido", 0.6))
def DE1(lz, t):
    PDE1.fondo(lz, t)
    brillo_en(lz, PDE1, t, 0.67, 0.64, 95, inten=0.42, sem=5, chis=8)
    quieto(lz, PDE1, t, "h01_tecuani/00", 0.30, 0.93, 0.48, tono=INTERIOR)
    quieto(lz, PDE1, t, "h03_citlali/03", 0.56, 0.92, 0.45, tono=INTERIOR, fase=0.6)


PDE2 = PF.Plano("e22_casa_noche_a", F("decision", 1) - 0.25, F("decision", 2), z0=1.80, z1=1.86, c0=(0.32, 0.70), c1=(0.33, 0.70),
                par=(14, 3), tono=INTERIOR)


@toma(F("decision", 1) - 0.25, ("corte", 0))
def DE2(lz, t):
    PDE2.fondo(lz, t)
    brillo_en(lz, PDE2, t, 0.67, 0.64, 80, inten=0.36, sem=5)
    desenfoca(lz, 2.2)
    quieto(lz, PDE2, t, "h01_tecuani/00", 0.30, 0.93, 0.42, tono=INTERIOR)


PDE3 = PF.Plano("e22_casa_noche_b", F("decision", 2) - 0.2, F("decision", 3), z0=1.70, z1=1.76, c0=(0.55, 0.68), c1=(0.55, 0.68),
                par=(14, 3), tono=INTERIOR)


@toma(F("decision", 2) - 0.2, ("corte", 0))
def DE3(lz, t):
    PDE3.fondo(lz, t)
    brillo_en(lz, PDE3, t, 0.17, 0.70, 90, inten=0.36, sem=6)
    desenfoca(lz, 2.2)
    quieto(lz, PDE3, t, "h05_ollin_joven/01", 0.55, 0.93, 0.44, tono=INTERIOR)


PDE4 = PF.Plano("e04_casa_madrugada_b", F("decision", 3) - 0.3, t1_("decision") + 0.5, z0=1.12, z1=1.24, c0=(0.50, 0.55),
                c1=(0.54, 0.59), par=(20, 5), tono=INTERIOR)
_t_ama = T("decision", "amanecer", 3)
_t_com = T("decision", "comida", 3)
snd(T("decision", "quince", 3) - 0.1, "papel", 0.5)
snd(_t_com - 0.1, "pop", 0.45)
for _k in range(4):
    snd(_t_ama + _k * 1.15, "arena", 0.25, dur=0.6)


@toma(F("decision", 3) - 0.3, ("fundido", 0.7))
def DE4(lz, t):
    PDE4.fondo(lz, t)
    brillo_en(lz, PDE4, t, 0.74, 0.62, 80, inten=0.38, sem=7, chis=6)
    quieto(lz, PDE4, t, "h03_citlali/03", 0.52, 0.92, 0.44, tono=INTERIOR, t_out=_t_ama - 0.4)
    if t > _t_ama - 0.4:
        quieto(lz, PDE4, t, "h03_citlali/00", 0.50 + _muele(t), 0.93, 0.36, tono=INTERIOR, t_in=_t_ama - 0.3,
               rot=1.2 * math.sin(2 * math.pi * t / 1.15))
    quieto(lz, PDE4, t, "u01_utileria/01", 0.70, 0.93, 0.09, tono=INTERIOR, t_in=_t_com - 0.1)
    quieto(lz, PDE4, t, "u01_utileria/11", 0.80, 0.94, 0.08, tono=INTERIOR, t_in=_t_com + 0.3)
    tinte(lz, (1.0, 0.85, 0.75), 0.20 * smooth(prog(t, _t_ama - 0.5, _t_ama + 2.5)))
    PF.rotulo(lz, "15 AÑOS", W * 0.30, H * 0.20, 70, t, T("decision", "quince", 3) - 0.1, _t_ama - 0.5, rot=-1.5)


# ================================================================== ACTO IV — la guerra (1541): el peñol
MIRA.update({"h08_tenamaxtli/04": 1, "h16_alvarado/00": 1, "h16_alvarado/01": 1})
AMB += [(t0_("penol") - 0.3, t1_("penol") + 0.3, "alba", 0.42), (t0_("victoria") - 0.3, F("victoria", 5), "alba", 0.35),
        (F("victoria", 5) - 0.3, t1_("victoria") + 0.3, "grillos", 0.30), (t0_("guadalajara") - 0.3, F("guadalajara", 2), "grillos", 0.25),
        (t0_("herida") - 0.3, t1_("herida") + 0.3, "viento_noche", 0.40), (t0_("herida") - 0.3, t1_("herida") + 0.3, "grillos", 0.25)]


def tumba(lz, pl, t, pieza, x, y, frac, t_cae, flip=False, tono=None, lado=1):
    """Alguien que cae: gira alrededor de los pies hasta ~85° hacia `lado` y se queda tendido (sin sangre)."""
    u = smooth(prog(t, t_cae, t_cae + 0.55))
    X, Y, h = pl.en(t, x, y, frac)
    PF.actor(lz, pieza, X, Y, h, flip=flip, tono=tono, rot=-lado * 85 * u, op=1.0 - 0.35 * smooth(prog(t, t_cae + 1.0, t_cae + 2.5)))


PPE1 = PF.Plano("e23_subida_mixton_b", t0_("penol"), F("penol", 1), z0=1.08, z1=1.18, c0=(0.50, 0.53), c1=(0.48, 0.56), par=(30, 7),
                tono=DORADO)
_t_pe = [T("penol", p, 0) for p in ("juchipila", "jalpa", "apozol", "tlaltenango")]
snd(t0_("penol") + 0.2, "papel", 0.5)
for _tpe in _t_pe:
    snd(_tpe - 0.1, "papel", 0.4)
snd(t0_("penol"), "pasos", 0.35, dur=9.0)


@toma(t0_("penol"), ("fundido", 0.8))
def PE1(lz, t):
    PPE1.fondo(lz, t)
    ta = t0_("penol")
    for k, pz in enumerate(["h15_gente/03", "h15_gente/01", "h14_guerreros/03", "h15_gente/00", "h15_gente/04"]):
        aleja(lz, PPE1, t, pz, ta + 1.1 * k - 2.0, ta + 1.1 * k + 7.0, (0.74, 0.93), (0.44, 0.63), 0.30, 0.13, tono=DORADO)
    aves(lz, t, [(ta, 10.0, 0.20, 0.14, 56, 1, 0.4)])
    capitulo(lz, t, "IV", "LA GUERRA", ta + 0.2, _t_pe[0] - 0.5)
    for k, (nm, tp) in enumerate(zip(("JUCHIPILA", "JALPA", "APOZOL", "TLALTENANGO"), _t_pe)):
        PF.rotulo(lz, nm, W * (0.18 + 0.21 * k), H * (0.19 + 0.05 * (k % 2)), 48, t, tp - 0.1, F1("penol", 0) + 0.4, rot=(-1) ** k * 1.5)


PPE2 = PF.Plano("e24_mixton_cima_dia_b", F("penol", 1) - 0.3, F("penol", 2), z0=1.10, z1=1.35, c0=(0.48, 0.52), c1=(0.64, 0.62),
                par=(30, 7), tono=DORADO)
snd(T("penol", "mixtón", 1) - 0.1, "papel", 0.5)
snd(T("penol", "derechas", 1) - 0.2, "viento", 0.2, dur=2.0)


@toma(F("penol", 1) - 0.3, ("fundido", 0.5))
def PE2(lz, t):
    PPE2.fondo(lz, t)
    humo_en(lz, PPE2, t, 0.33, 0.52, s=0.7, color=(0.86, 0.84, 0.82), op=0.20, sem=1)
    agua(lz, PPE2, t, "e24_mixton_cima_dia_b")
    ta = F("penol", 1) - 0.3
    paseo(lz, PPE2, t, "h15_gente/01", ta, ta + 6.0, 0.10, 0.36, 0.72, 0.22, pasos=1.8, tono=DORADO)
    paseo(lz, PPE2, t, "h15_gente/02", ta, ta + 6.0, 0.02, 0.26, 0.74, 0.15, pasos=2.4, tono=DORADO)
    aves(lz, t, [(ta + 2.0, 8.0, 0.40, 0.46, 50, 1, 1.1)])
    PF.rotulo(lz, "MIXTÓN", W * 0.30, H * 0.19, 90, t, T("penol", "mixtón", 1) - 0.1, F1("penol", 1) + 0.2, rot=-1.5)
    PF.rotulo(lz, "el subidero de los gatos monteses", W * 0.32, H * 0.30, 40, t, T("penol", "subidero", 1) - 0.1,
              F1("penol", 1) + 0.2, rot=1.0)


PPE3 = PF.Plano("e24_mixton_cima_dia_a", F("penol", 2) - 0.3, F("penol", 3), z0=1.10, z1=1.18, c0=(0.50, 0.545), c1=(0.50, 0.57),
                par=(28, 6), tono=DORADO)
_t_tena = T("penol", "tenamaxtli", 2)
snd(_t_tena - 0.1, "papel", 0.5)
snd(_t_tena - 0.1, "cuerno", 0.30, tono=0.8)


@toma(F("penol", 2) - 0.3, ("fundido", 0.5))
def PE3(lz, t):
    PPE3.fondo(lz, t)
    humo_en(lz, PPE3, t, 0.30, 0.26, s=0.7, color=(0.86, 0.84, 0.82), op=0.18, sem=2)
    humo_en(lz, PPE3, t, 0.72, 0.76, s=0.6, color=(0.86, 0.84, 0.82), op=0.18, sem=3)
    quieto(lz, PPE3, t, "h14_guerreros/03", 0.22, 0.82, 0.30, tono=DORADO)
    quieto(lz, PPE3, t, "h14_guerreros/04", 0.80, 0.81, 0.30, flip=True, tono=DORADO, fase=0.8)
    if t < _t_tena:
        paseo(lz, PPE3, t, "h08_tenamaxtli/04", F("penol", 2) - 0.3, _t_tena - 0.1, -0.12, 0.50, 0.88, 0.42, pasos=1.6, tono=DORADO)
    else:
        quieto(lz, PPE3, t, "h08_tenamaxtli/02", 0.50, 0.88, 0.42, tono=DORADO)
    PF.rotulo(lz, "TENAMAXTLI", W * 0.50, H * 0.19, 90, t, _t_tena - 0.1, F1("penol", 2) + 0.3, rot=-1.5)
    PF.rotulo(lz, "principal de Nochistlán", W * 0.52, H * 0.30, 42, t, T("penol", "principal", 2) - 0.1, F1("penol", 2) + 0.3, rot=1.0)


PPE4 = PF.Plano("e24_mixton_cima_dia_a", F("penol", 3) - 0.25, F("penol", 4), z0=1.60, z1=1.70, c0=(0.50, 0.66), c1=(0.50, 0.67),
                par=(16, 3), tono=DORADO)
_t_pe4 = [T("penol", p, 3) for p in ("perros", "marcaron", "nombre")]
for _tpe in _t_pe4:
    snd(_tpe - 0.05, "sello", 0.45)


@toma(F("penol", 3) - 0.25, ("corte", 0))
def PE4(lz, t):
    PPE4.fondo(lz, t)
    desenfoca(lz, 1.8)
    quieto(lz, PPE4, t, "h08_tenamaxtli/00", 0.50, 0.92, 0.46, tono=DORADO)
    for k, (txt, tp) in enumerate(zip(("PERROS", "HIERRO", "JUAN"), _t_pe4)):
        PF.rotulo(lz, txt, W * (0.20 + 0.60 * (k % 2)), H * (0.24 + 0.18 * k), 70, t, tp - 0.05, F1("penol", 3) + 0.2,
                  rot=(-1) ** k * 4, tinta=(120, 24, 14))


PPE5 = PF.Plano("e25_mixton_ladera_a", F("penol", 4) - 0.2, F("penol", 5), z0=1.15, z1=1.26, c0=(0.55, 0.60), c1=(0.56, 0.58),
                par=(30, 6), tono=DORADO)
_tp5 = F("penol", 4)
for _kk in range(8):
    snd(_tp5 + _kk * 1.0, "tambor", 0.40 + 0.04 * _kk, tono=0.8)
snd(T("penol", "montaña", 4) - 0.1, "cuerno", 0.45, tono=0.9)


@toma(F("penol", 4) - 0.2, ("corte", 0))
def PE5(lz, t):
    PPE5.fondo(lz, t)
    PF.arena_viento(lz, t, fuerza=0.5, y0=0.40, sem=12)
    aves(lz, t, [(_tp5 - 1.0, 9.0, 0.30, 0.22, 70, -1, 0.2)])
    X, Y, h = PPE5.en(t, 0.60, 0.99, 0.66)
    PF.actor(lz, "h08_tenamaxtli/03", X, Y, h, tono=DORADO, rot=1.2 * math.sin(t * 2.0), sy=PF.respira(t, a=0.02))


PPE6 = PF.Plano("e24_mixton_cima_dia_b", F("penol", 5) - 0.3, F("penol", 6), z0=1.30, z1=1.38, c0=(0.42, 0.62), c1=(0.44, 0.63),
                par=(24, 5), tono=DORADO)
_t_grite = T("penol", "tecuani", 5)
snd(F("penol", 5) - 0.2, "cuerno", 0.40, tono=0.8)
snd(_t_grite - 0.1, "tambor", 0.6, tono=0.7)
snd(_t_grite - 0.1, "papel", 0.6)


@toma(F("penol", 5) - 0.3, ("fundido", 0.4))
def PE6(lz, t):
    PPE6.fondo(lz, t)
    gente = [("h14_guerreros/03", 0.20, 0.66, 0.20, False), ("h14_guerreros/04", 0.30, 0.65, 0.19, True), ("h14_guerreros/00", 0.62, 0.67, 0.20, True),
             ("h14_guerreros/01", 0.70, 0.66, 0.19, False), ("h14_guerreros/02", 0.12, 0.70, 0.22, True), ("h14_guerreros/03", 0.54, 0.70, 0.22, True),
             ("h05_ollin_joven/02", 0.36, 0.74, 0.27, False), ("h14_guerreros/00", 0.78, 0.73, 0.25, False)]
    for k, (pz, x, y, f, fl) in enumerate(sorted(gente, key=lambda g: g[2])):
        X, Y, h = PPE6.en(t, x, y, f)
        PF.actor(lz, pz, X, Y - 0.03 * h * abs(math.sin(t * 5 + k)), h, flip=fl, tono=DORADO)
    X, Y, h = PPE6.en(t, 0.47, 0.86, 0.40)
    PF.actor(lz, "h02_tecuani_g/02", X, Y - 0.02 * h * abs(math.sin(t * 4)), h, tono=DORADO)
    PF.rotulo(lz, "¡TECUANI!", W * 0.50, H * 0.21, 120, t, _t_grite - 0.1, F1("penol", 5) + 0.3, rot=-2, tinta=(120, 24, 14))


PPE7 = PF.Plano("e24_mixton_cima_dia_a", F("penol", 6) - 0.3, t1_("penol") + 0.5, z0=1.12, z1=1.20, c0=(0.48, 0.55), c1=(0.52, 0.57),
                par=(28, 6), tono=DORADO)
_t_muros = T("penol", "muros", 6)
_t_rocas = T("penol", "rocas", 6)
snd(_t_muros - 0.1, "impacto", 0.4, tono=0.7)
snd(_t_rocas - 0.1, "impacto", 0.4, tono=0.8)


@toma(F("penol", 6) - 0.3, ("fundido", 0.5))
def PE7(lz, t):
    PPE7.fondo(lz, t)
    ta = F("penol", 6) - 0.3
    humo_en(lz, PPE7, t, 0.30, 0.26, s=0.7, color=(0.86, 0.84, 0.82), op=0.18, sem=2)
    quieto(lz, PPE7, t, "u02_utileria_guerra/01", 0.47, 0.70, 0.07, tono=DORADO, t_in=_t_muros - 0.1)
    quieto(lz, PPE7, t, "u02_utileria_guerra/00", 0.62, 0.74, 0.06, tono=DORADO, t_in=_t_rocas - 0.1)
    quieto(lz, PPE7, t, "u02_utileria_guerra/00", 0.36, 0.76, 0.06, tono=DORADO, t_in=_t_rocas + 0.3)
    paseo(lz, PPE7, t, "h01_tecuani/04", ta, ta + 5.0, 0.70, 0.48, 0.86, 0.36, pasos=1.3, tono=DORADO)
    paseo(lz, PPE7, t, "h03_citlali/04", T("penol", "mujeres", 6) - 0.6, t1_("penol") + 0.5, 0.05, 0.40, 0.84, 0.32, pasos=1.6,
          desde_antes=False, tono=DORADO)
    paseo(lz, PPE7, t, "h15_gente/04", T("penol", "mujeres", 6) - 0.2, t1_("penol") + 0.5, 0.92, 0.62, 0.82, 0.26, pasos=2.0,
          desde_antes=False, tono=DORADO)
    paseo(lz, PPE7, t, "h15_gente/02", T("penol", "niños", 6) - 0.5, t1_("penol") + 0.5, 0.12, 0.30, 0.92, 0.20, pasos=2.4,
          desde_antes=False, tono=DORADO)


# ------------------------------------------------------------------ la primera victoria (abril de 1541)
PVI1 = PF.Plano("e25_mixton_ladera_b", t0_("victoria") - 0.3, F("victoria", 1), z0=1.10, z1=1.22, c0=(0.50, 0.53), c1=(0.50, 0.56),
                par=(30, 7), tono=DORADO)
snd(T("victoria", "abril", 0) - 0.1, "papel", 0.5)
snd(T("victoria", "ibarra", 0) - 0.1, "papel", 0.5)
snd(t0_("victoria") + 1.0, "galope", 0.25, dur=4.0)


@toma(t0_("victoria") - 0.3, ("fundido", 0.6))
def VI1(lz, t):
    PVI1.fondo(lz, t)
    ta = t0_("victoria") - 0.3
    aleja(lz, PVI1, t, "h12_soldados/05", ta, ta + 7.0, (0.30, 0.60), (0.40, 0.66), 0.10, 0.12, tono=DORADO)
    aleja(lz, PVI1, t, "h21_espanoles_1541/02", ta, ta + 7.0, (0.38, 0.62), (0.48, 0.68), 0.12, 0.14, tono=DORADO, flip=True)
    aleja(lz, PVI1, t, "h12_soldados/00", ta + 0.5, ta + 7.5, (0.28, 0.66), (0.38, 0.71), 0.11, 0.12, tono=DORADO)
    X, Y, h = PVI1.en(t, 0.20, 1.02, 0.42)
    PF.actor(lz, "h14_guerreros/00", X, Y, h, tono=DORADO, sy=PF.respira(t))
    X, Y, h = PVI1.en(t, 0.84, 1.03, 0.44)
    PF.actor(lz, "h14_guerreros/01", X, Y, h, flip=True, tono=DORADO, sy=PF.respira(t, fase=1.0))
    PF.rotulo(lz, "ABRIL DE 1541", W * 0.50, H * 0.19, 60, t, T("victoria", "abril", 0) - 0.1, F1("victoria", 0) + 0.2, rot=-1.2)
    PF.rotulo(lz, "capitán Miguel de Ibarra", W * 0.52, H * 0.30, 42, t, T("victoria", "ibarra", 0) - 0.1, F1("victoria", 0) + 0.2,
              rot=1.0)


PVI2 = PF.Plano("e23_subida_mixton_a", F("victoria", 1) - 0.25, F("victoria", 2), z0=1.55, z1=1.62, c0=(0.50, 0.66), c1=(0.50, 0.66),
                par=(16, 3), tono=DORADO)
snd(F("victoria", 1) - 0.2, "galope", 0.3, dur=1.5)


@toma(F("victoria", 1) - 0.25, ("corte", 0))
def VI2(lz, t):
    PVI2.fondo(lz, t)
    desenfoca(lz, 1.8)
    quieto(lz, PVI2, t, "h21_espanoles_1541/02", 0.50, 0.92, 0.52, tono=DORADO, rot=1.0 * math.sin(t * 7))


PVI3 = PF.Plano("e25_mixton_ladera_a", F("victoria", 2) - 0.3, F("victoria", 3), z0=1.18, z1=1.30, c0=(0.55, 0.60), c1=(0.60, 0.58),
                par=(30, 6), tono=DORADO)
_t_ramos = T("victoria", "ramos", 2)
_t_cayo = T("victoria", "cayó", 2)
ROCAS_VI = [(_t_cayo + 0.25 * k, 2.2, (0.48 + 0.04 * (k % 4), 0.84), (0.62 + 0.03 * (k % 3), 0.38), 0.05 + 0.01 * (k % 2), k)
            for k in range(9)]
FLECHAS_VI = [(_t_cayo + 1.2, 1.3, (0.30, 0.86), (0.70, 0.40), 7, 3), (_t_cayo + 2.4, 1.3, (0.40, 0.86), (0.66, 0.42), 7, 4)]
snd(_t_ramos - 0.1, "papel", 0.5)
for _kk in range(6):
    snd(_t_cayo + 0.35 * _kk, "impacto", 0.45, tono=0.6 + 0.05 * _kk)
snd(_t_cayo + 1.2, "whoosh", 0.4, dur=0.6)
snd(_t_cayo + 2.4, "whoosh", 0.4, dur=0.6)
snd(_t_cayo - 0.2, "cuerno", 0.45, tono=0.9)


@toma(F("victoria", 2) - 0.3, ("fundido", 0.4))
def VI3(lz, t):
    PVI3.fondo(lz, t)
    rocas(lz, PVI3, t, ROCAS_VI, tono=DORADO)
    flechas(lz, t, FLECHAS_VI)
    for k in range(3):
        polvo(lz, PVI3, t, 0.62 + 0.04 * k, 0.45, s=1.6, t_in=_t_cayo + 1.5 + 0.6 * k, dur=3.0, op=0.28, sem=k)
    X, Y, h = PVI3.en(t, 0.32, 1.02, 0.44)
    PF.actor(lz, "h14_guerreros/05", X, Y, h, tono=DORADO, rot=2 * math.sin(t * 3))
    X, Y, h = PVI3.en(t, 0.52, 1.03, 0.46)
    PF.actor(lz, "h14_guerreros/00", X, Y, h, flip=True, tono=DORADO)
    X, Y, h = PVI3.en(t, 0.78, 1.02, 0.44)
    PF.actor(lz, "h14_guerreros/01", X, Y, h, tono=DORADO)
    PF.rotulo(lz, "DOMINGO DE RAMOS", W * 0.50, H * 0.19, 60, t, _t_ramos - 0.1, F1("victoria", 2) + 0.2, rot=-1.2)


PVI4 = PF.Plano("e23_subida_mixton_b", F("victoria", 3) - 0.3, F("victoria", 4), z0=1.10, z1=1.18, c0=(0.50, 0.545), c1=(0.52, 0.56),
                par=(30, 7), tono=DORADO)
snd(F("victoria", 3) - 0.2, "galope", 0.55, dur=5.0)


@toma(F("victoria", 3) - 0.3, ("latigo", 0.4))
def VI4(lz, t):
    PVI4.fondo(lz, t)
    ta = F("victoria", 3) - 0.3
    aleja(lz, PVI4, t, "h12_soldados/02", ta, ta + 3.5, (0.46, 0.62), (0.72, 0.95), 0.14, 0.32, tono=DORADO, pasos=3.0)
    aleja(lz, PVI4, t, "h12_soldados/00", ta + 0.5, ta + 4.0, (0.42, 0.62), (0.66, 0.95), 0.14, 0.32, tono=DORADO, pasos=3.0)
    tropa(lz, PVI4, t, "c07_jinete_galope", ta + 0.8, ta + 4.6, -0.25, 1.25, 0.90, 0.28, n=2, dx=0.20, paso=1.7, tono=DORADO,
          desde_antes=False)
    rocas(lz, PVI4, t, [(ta + 0.6 + 0.6 * k, 2.4, (0.44, 0.58), (0.70 + 0.04 * k, 0.92), 0.05, 20 + k) for k in range(5)], tono=DORADO)
    polvo(lz, PVI4, t, 0.62, 0.88, s=2.0, t_in=ta + 1.5, dur=4.0, op=0.28, sem=8)


PVI5 = PF.Plano("e24_mixton_cima_dia_b", F("victoria", 4) - 0.2, F("victoria", 5), z0=1.70, z1=1.76, c0=(0.40, 0.68), c1=(0.40, 0.68),
                par=(14, 3), tono=DORADO)


@toma(F("victoria", 4) - 0.2, ("corte", 0))
def VI5(lz, t):
    PVI5.fondo(lz, t)
    desenfoca(lz, 2.0)
    X, Y, h = PVI5.en(t, 0.32, 0.92, 0.40)
    PF.actor(lz, "h02_tecuani_g/02", X, Y, h, tono=DORADO)
    X, Y, h = PVI5.en(t, 0.47, 0.93, 0.38)
    PF.actor(lz, "h05_ollin_joven/02", X, Y - 0.04 * h * abs(math.sin(t * 7)), h, tono=DORADO)


PVI6 = PF.Plano("e30_mixton_noche_fuego_a", F("victoria", 5) - 0.3, t1_("victoria") + 0.5, z0=1.12, z1=1.24, c0=(0.42, 0.56),
                c1=(0.44, 0.60), par=(26, 6), tono=FOGATA)
_tv0 = F("victoria", 5) - 0.2
_kv = 0
while _tv0 + _kv * 0.5 < t1_("victoria"):
    snd(_tv0 + _kv * 0.5, "tambor", 0.40 if _kv % 2 else 0.55, tono=1.0 if _kv % 2 else 0.8)
    _kv += 1
snd(_tv0, "fuego", 0.4, dur=8.0)


@toma(F("victoria", 5) - 0.3, ("fundido", 0.6))
def VI6(lz, t):
    PVI6.fondo(lz, t)
    estrellas(lz, t, y1=0.22)
    fuegos_valle(lz, PVI6, t, "e30_mixton_noche_fuego_a", (0.60, 0.45, 0.95, 0.72), n=20)
    ronda(lz, PVI6, t, "c10_danza", 0.28, 0.76, 0.16, 0.05, 7, 0.40, 0.20, 0.45, tono=FOGATA, mitad="atras")
    hoguera(lz, PVI6, t, 0.28, 0.76, 0.13, tono=FOGATA, sem=9)
    ronda(lz, PVI6, t, "c10_danza", 0.28, 0.76, 0.16, 0.05, 7, 0.40, 0.20, 0.45, tono=FOGATA, mitad="delante")


# ------------------------------------------------------------------ bando español: el palacio del virrey (31 de mayo de 1541)
VELA = (1.02, 0.86, 0.70)
PCO1 = PF.Plano("e43_palacio_virrey_a", t0_("consejo") - 0.3, F("consejo", 1), z0=1.08, z1=1.16, c0=(0.50, 0.53), c1=(0.53, 0.56),
                par=(22, 5), tono=VELA)
snd(T("consejo", "méxico", 0) - 0.1, "papel", 0.5)
snd(t0_("consejo"), "campana", 0.30, tono=0.6)


@toma(t0_("consejo") - 0.3, ("fundido", 0.7))
def CO1(lz, t):
    PCO1.fondo(lz, t)
    brillo_en(lz, PCO1, t, 0.55, 0.61, 45, inten=0.32, sem=40)
    brillo_en(lz, PCO1, t, 0.93, 0.65, 45, inten=0.32, sem=41)
    quieto(lz, PCO1, t, "h25_oidores/01", 0.80, 0.82, 0.30, tono=VELA, fase=0.4)
    quieto(lz, PCO1, t, "h17_mendoza/04", 0.48, 0.90, 0.44, tono=VELA)
    PF.rotulo(lz, "CIUDAD DE MÉXICO", W * 0.30, H * 0.19, 56, t, T("consejo", "méxico", 0) - 0.1, F1("consejo", 0) + 0.2, rot=-1.2)
    PF.rotulo(lz, "31 de mayo de 1541", W * 0.31, H * 0.29, 44, t, T("consejo", "31", 0) - 0.1, F1("consejo", 0) + 0.2, rot=1.0)


PCO2 = PF.Plano("e43_palacio_virrey_b", F("consejo", 1) - 0.25, F("consejo", 2), z0=1.65, z1=1.72, c0=(0.62, 0.66), c1=(0.62, 0.66),
                par=(14, 3), tono=VELA)
_t_fue = T("consejo", "fuego", 1)
snd(_t_fue - 0.1, "sello", 0.5)


@toma(F("consejo", 1) - 0.25, ("corte", 0))
def CO2(lz, t):
    PCO2.fondo(lz, t)
    desenfoca(lz, 2.0)
    quieto(lz, PCO2, t, "h17_mendoza/02", 0.62, 0.92, 0.44, tono=VELA)
    PF.rotulo(lz, "A FUEGO Y A SANGRE", W * 0.50, H * 0.20, 76, t, _t_fue - 0.1, F1("consejo", 1) + 0.4, rot=-1.5, tinta=(120, 24, 14))


PCO3 = PF.Plano("e43_palacio_virrey_b", F("consejo", 2) - 0.25, t1_("consejo") + 0.4, z0=1.40, z1=1.52, c0=(0.30, 0.64),
                c1=(0.32, 0.65), par=(16, 4), tono=VELA)
_t_escl = T("consejo", "esclavos", 2)
snd(_t_escl - 0.05, "sello", 0.6)
snd(_t_escl - 0.05, "latido", 0.45)


@toma(F("consejo", 2) - 0.25, ("fundido", 0.4))
def CO3(lz, t):
    PCO3.fondo(lz, t)
    brillo_en(lz, PCO3, t, 0.05, 0.60, 45, inten=0.32, sem=42)
    brillo_en(lz, PCO3, t, 0.46, 0.57, 45, inten=0.32, sem=43)
    quieto(lz, PCO3, t, "h17_mendoza/03", 0.32, 0.86, 0.36, tono=VELA)
    pega(lz, "u01_utileria/13", W * 0.74, H * 0.46, 330, t, _t_escl - 0.1, None, rot=6)
    latido_rojo(lz, t, _t_escl - 0.05, t1_("consejo") + 0.4, k=0.16)


# ------------------------------------------------------------------ bando español: Alvarado en Guadalajara y su caída
PAL1 = PF.Plano("e28_guadalajara_amanecer_b", t0_("alvarado") - 0.3, F("alvarado", 1), z0=1.08, z1=1.16, c0=(0.50, 0.53),
                c1=(0.52, 0.56), par=(28, 6), tono=ALBA)
snd(t0_("alvarado") - 0.2, "galope", 0.45, dur=6.0)
snd(T("alvarado", "junio", 0) - 0.1, "papel", 0.5)
snd(T("alvarado", "alvarado", 0) - 0.1, "papel", 0.5)
snd(T("alvarado", "alvarado", 0) - 0.1, "fanfarria", 0.30)


@toma(t0_("alvarado") - 0.3, ("fundido", 0.7))
def AL1(lz, t):
    PAL1.fondo(lz, t)
    ta = t0_("alvarado") - 0.3
    tropa(lz, PAL1, t, "c07_jinete_galope", ta, ta + 6.0, -0.55, 0.18, 0.84, 0.28, n=3, dx=0.12, paso=1.7, tono=ALBA)
    paseo(lz, PAL1, t, "h16_alvarado/00", ta, ta + 6.0, -0.18, 0.46, 0.89, 0.42, pasos=1.3, salto=0.02, tono=ALBA)
    PF.rotulo(lz, "JUNIO DE 1541", W * 0.30, H * 0.19, 56, t, T("alvarado", "junio", 0) - 0.1, F1("alvarado", 0) + 0.2, rot=-1.2)
    PF.rotulo(lz, "PEDRO DE ALVARADO", W * 0.31, H * 0.29, 50, t, T("alvarado", "alvarado", 0) - 0.1, F1("alvarado", 0) + 0.2, rot=1.0)
    PF.rotulo(lz, "Tenochtitlan · Guatemala", W * 0.33, H * 0.38, 38, t, T("alvarado", "guatemala", 0) - 0.1, F1("alvarado", 0) + 0.2,
              rot=-0.8)


PAL2 = PF.Plano("e44_casa_onate_a", F("alvarado", 1) - 0.3, F("alvarado", 2), z0=1.20, z1=1.26, c0=(0.55, 0.58), c1=(0.56, 0.58),
                par=(20, 5), tono=DORADO)
snd(F("alvarado", 1) - 0.1, "papel", 0.45)


@toma(F("alvarado", 1) - 0.3, ("fundido", 0.5))
def AL2(lz, t):
    PAL2.fondo(lz, t)
    quieto(lz, PAL2, t, "h21_espanoles_1541/00", 0.55, 0.90, 0.44, tono=DORADO)
    quieto(lz, PAL2, t, "h22_alvarado_pie/00", 0.80, 0.91, 0.46, tono=DORADO, fase=0.7)
    PF.rotulo(lz, "CRISTÓBAL DE OÑATE", W * 0.32, H * 0.19, 48, t, F("alvarado", 1) - 0.1, F1("alvarado", 1) + 0.2, rot=-1.2)


PAL3 = PF.Plano("e44_casa_onate_b", F("alvarado", 2) - 0.2, F("alvarado", 3), z0=1.60, z1=1.66, c0=(0.34, 0.66), c1=(0.35, 0.66),
                par=(14, 3), tono=DORADO)


@toma(F("alvarado", 2) - 0.2, ("corte", 0))
def AL3(lz, t):
    PAL3.fondo(lz, t)
    desenfoca(lz, 2.0)
    risa = 1.0 - smooth(prog(t, F1("alvarado", 2) - 0.5, F1("alvarado", 2) + 0.3))
    X, Y, h = PAL3.en(t, 0.34, 0.92, 0.44)
    PF.actor(lz, "h22_alvarado_pie/00", X, Y, h, tono=DORADO, sy=1.0 + 0.018 * math.sin(t * 13) * risa, rot=1.2 * math.sin(t * 6.5) * risa)


PAL4 = PF.Plano("e26_nochistlan_lluvia_a", F("alvarado", 3) - 0.3, F("alvarado", 4), z0=1.08, z1=1.22, c0=(0.50, 0.53),
                c1=(0.56, 0.47), par=(30, 7), tono=LLUVIA)
snd(F("alvarado", 3) - 0.3, "lluvia", 0.45, dur=42.0)
snd(F("alvarado", 3) + 0.4, "trueno", 0.45)
snd(T("alvarado", "tonatiuh", 3) - 0.1, "papel", 0.5)
snd(T("alvarado", "24", 3) - 0.1, "papel", 0.5)
snd(T("alvarado", "subió", 3) - 0.3, "galope", 0.4, dur=4.0)


@toma(F("alvarado", 3) - 0.3, ("fundido", 0.6))
def AL4(lz, t):
    PAL4.fondo(lz, t)
    relampago(lz, t, [F("alvarado", 3) + 0.35, T("alvarado", "esperando", 3)])
    ts = T("alvarado", "subió", 3) - 0.3
    tropa(lz, PAL4, t, "c07_jinete_galope", ts, ts + 6.0, -0.10, 0.62, 0.84, 0.26, n=3, dx=0.12, paso=1.7, tono=LLUVIA,
          desde_antes=False)
    paseo(lz, PAL4, t, "h16_alvarado/01", ts, ts + 6.0, 0.12, 0.76, 0.89, 0.36, pasos=1.5, salto=0.02, tono=LLUVIA, desde_antes=False)
    for k, (x, pz) in enumerate([(0.52, "h14_guerreros/00"), (0.58, "h14_guerreros/05"), (0.64, "h14_guerreros/01")]):
        quieto(lz, PAL4, t, pz, x, 0.20, 0.07, tono=(0.40, 0.42, 0.50), fase=k)
    lluvia(lz, t, n=260, fuerza=0.45, viento=0.22, sem=10)
    PF.rotulo(lz, "TONATIUH = EL SOL", W * 0.30, H * 0.19, 54, t, T("alvarado", "tonatiuh", 3) - 0.1, T("alvarado", "24", 3) - 0.3,
              rot=-1.2)
    PF.rotulo(lz, "24 DE JUNIO · PEÑOL DE NOCHISTLÁN", W * 0.40, H * 0.19, 46, t, T("alvarado", "24", 3) - 0.1, F1("alvarado", 3) + 0.2,
              rot=1.0)


PAL5 = PF.Plano("e27_barranca_lodo_a", F("alvarado", 4) - 0.3, F("alvarado", 5), z0=1.25, z1=1.32, c0=(0.50, 0.59), c1=(0.50, 0.60),
                par=(26, 6), tono=LLUVIA)
_ta5 = F("alvarado", 4) - 0.3
PIEDRAS_AL = [(_ta5 + 0.5 + 0.55 * k, 1.0, (0.05 + 0.05 * (k % 3), 0.12), (0.35 + 0.08 * (k % 4), 0.70), 40 - 5 * (k % 2), k)
              for k in range(9)]
for _kk in range(5):
    snd(_ta5 + 1.4 + 1.1 * _kk, "impacto", 0.35, tono=0.7)
snd(_ta5 + 0.6, "crujido", 0.4, dur=0.9)


@toma(F("alvarado", 4) - 0.3, ("latigo", 0.4))
def AL5(lz, t):
    PAL5.fondo(lz, t)
    relampago(lz, t, [_ta5 + 2.5])
    quieto(lz, PAL5, t, "h12_soldados/02", 0.24, 0.78, 0.30, tono=LLUVIA, rot=4 * math.sin(t * 3.1))
    X, Y, h = PAL5.en(t, 0.46, 0.84, 0.42)
    PF.actor(lz, "h16_alvarado/02", X + 8 * math.sin(t * 2.3), Y, h, tono=LLUVIA, rot=5 * math.sin(t * 2.6))
    for k in range(3):
        tk = _ta5 + 0.8 + 1.6 * k
        if tk <= t <= tk + 0.9:
            Xs, Ys, hs = PAL5.en(t, 0.44 + 0.03 * k, 0.85, 0.10 * (0.6 + 0.5 * prog(t, tk, tk + 0.4)))
            PF.actor(lz, "u04_fuego_humo/11", Xs, Ys, hs, tono=LLUVIA, op=1 - prog(t, tk + 0.4, tk + 0.9), suelo=0)
    quieto(lz, PAL5, t, "h12_soldados/00", 0.72, 0.87, 0.33, tono=LLUVIA, rot=-3 * math.sin(t * 2.7), fase=0.6)
    pedradas(lz, t, PIEDRAS_AL, tono=LLUVIA)
    lluvia(lz, t, n=300, fuerza=0.55, viento=0.25, sem=11)


PAL6 = PF.Plano("e27_barranca_lodo_b", F("alvarado", 5) - 0.3, F("alvarado", 6), z0=1.20, z1=1.30, c0=(0.50, 0.58), c1=(0.50, 0.60),
                par=(26, 6), tono=LLUVIA)
_t_enc = T("alvarado", "encima", 5)
snd(F("alvarado", 5) + 0.8, "crujido", 0.45, dur=1.0)
snd(_t_enc - 0.05, "impacto", 0.75, tono=0.5)
snd(_t_enc, "splat", 0.4)


@toma(F("alvarado", 5) - 0.3, ("fundido", 0.4))
def AL6(lz, t):
    PAL6.fondo(lz, t)
    u = smooth(prog(t, F("alvarado", 5) + 0.6, _t_enc))
    x, y = lerp(0.56, 0.48, u), lerp(0.46, 0.80, u)
    X, Y, h = PAL6.en(t, x, y, lerp(0.22, 0.40, u))
    caer = smooth(prog(t, _t_enc - 0.4, _t_enc + 0.2))
    PF.actor(lz, "h21_espanoles_1541/02", X, Y, h, flip=True, tono=LLUVIA, rot=-12 * u - 60 * caer)
    if t >= _t_enc:
        Xs, Ys, hs = PAL6.en(t, 0.48, 0.84, 0.16)
        PF.actor(lz, "u04_fuego_humo/11", Xs, Ys, hs, tono=LLUVIA, op=1 - prog(t, _t_enc + 0.5, _t_enc + 1.2), suelo=0)
        polvo(lz, PAL6, t, 0.48, 0.82, s=1.8, t_in=_t_enc, dur=2.5, op=0.30, sem=12, color=(0.45, 0.30, 0.25))
    lluvia(lz, t, n=260, fuerza=0.50, viento=0.22, sem=12)
    oscurece(lz, 0.55 * (1 - smooth(prog(t, _t_enc + 0.05, _t_enc + 0.7))) if t >= _t_enc else 0.0)


PAL7 = PF.Plano("e27_barranca_lodo_b", F("alvarado", 6) - 0.25, F("alvarado", 7), z0=1.70, z1=1.74, c0=(0.50, 0.70), c1=(0.50, 0.70),
                par=(14, 3), tono=LLUVIA)


@toma(F("alvarado", 6) - 0.25, ("corte", 0))
def AL7(lz, t):
    PAL7.fondo(lz, t)
    desenfoca(lz, 1.6)
    quieto(lz, PAL7, t, "h22_alvarado_pie/04", 0.44, 0.91, 0.10, tono=LLUVIA)
    quieto(lz, PAL7, t, "h21_espanoles_1541/03", 0.68, 0.91, 0.30, tono=LLUVIA, rot=1.5 * math.sin(t * 5))
    lluvia(lz, t, n=200, fuerza=0.40, viento=0.20, sem=13)


PAL8 = PF.Plano("e27_barranca_lodo_b", F("alvarado", 7) - 0.25, F("alvarado", 8), z0=2.25, z1=2.32, c0=(0.44, 0.76), c1=(0.44, 0.76),
                par=(10, 2), tono=LLUVIA)


@toma(F("alvarado", 7) - 0.25, ("corte", 0))
def AL8(lz, t):
    PAL8.fondo(lz, t)
    desenfoca(lz, 2.4)
    quieto(lz, PAL8, t, "h22_alvarado_pie/04", 0.44, 0.91, 0.10, tono=LLUVIA)
    lluvia(lz, t, n=140, fuerza=0.30, viento=0.20, sem=14)


PAL9 = PF.Plano("e46_lecho_alvarado_a", F("alvarado", 8) - 0.3, F("alvarado", 9), z0=1.10, z1=1.18, c0=(0.52, 0.53), c1=(0.56, 0.56),
                par=(18, 4), tono=VELA)
_t_mur = T("alvarado", "murió", 8)
snd(T("alvarado", "4", 8) - 0.1, "papel", 0.5)
snd(_t_mur + 0.6, "suspiro", 0.35)


@toma(F("alvarado", 8) - 0.3, ("fundido", 0.8))
def AL9(lz, t):
    PAL9.fondo(lz, t)
    apaga = smooth(prog(t, _t_mur + 0.5, _t_mur + 1.4))
    lluvia_rect(lz, PAL9, t, 0.82, 0.10, 0.98, 0.35, n=50, fuerza=0.5)
    brillo_en(lz, PAL9, t, 0.49, 0.52, 60, color=(1.0, 0.70, 0.35), inten=0.40 * (1 - apaga), sem=44)
    oscurece(lz, 0.30 * apaga)
    PF.rotulo(lz, "PEDRO DE ALVARADO", W * 0.32, H * 0.19, 54, t, F("alvarado", 8) - 0.1, F1("alvarado", 8) + 0.3, rot=-1.2)
    PF.rotulo(lz, "murió el 4 de julio de 1541", W * 0.34, H * 0.29, 42, t, T("alvarado", "4", 8) - 0.1, F1("alvarado", 8) + 0.3,
              rot=1.0)


PAL10 = PF.Plano("e26_nochistlan_lluvia_b", F("alvarado", 9) - 0.3, t1_("alvarado") + 0.6, z0=1.10, z1=1.26, c0=(0.50, 0.53),
                 c1=(0.45, 0.45), par=(30, 7), tono=LLUVIA)
snd(T("alvarado", "vencer", 9) - 0.1, "trueno", 0.5)


@toma(F("alvarado", 9) - 0.3, ("fundido", 0.6))
def AL10(lz, t):
    PAL10.fondo(lz, t)
    relampago(lz, t, [T("alvarado", "vencer", 9) - 0.05])
    lluvia(lz, t, n=200, fuerza=0.35, viento=0.22, sem=15)
    X, Y, h = PAL10.en(t, 0.79, 1.00, 0.46)
    PF.actor(lz, "h02_tecuani_g/00", X, Y, h, flip=True, tono=LLUVIA, sy=PF.respira(t))


# ------------------------------------------------------------------ el asalto a Guadalajara (28 de septiembre de 1541)
NOCHE_AZUL = (0.50, 0.56, 0.86)
PGU1 = PF.Plano("e28_guadalajara_amanecer_a", t0_("guadalajara") - 0.3, F("guadalajara", 1), z0=1.06, z1=1.14, c0=(0.50, 0.50),
                c1=(0.52, 0.54), par=(28, 6), tono=NOCHE_AZUL)
snd(T("guadalajara", "28", 0) - 0.1, "papel", 0.5)
snd(t0_("guadalajara"), "tambor", 0.4, tono=0.6)


@toma(t0_("guadalajara") - 0.3, ("fundido", 0.8))
def GU1(lz, t):
    PGU1.fondo(lz, t)
    tinte(lz, (0.55, 0.62, 1.0), 0.45)
    estrellas(lz, t, y1=0.20)
    neblina(lz, t, 0.52, 0.66, fuerza=0.15, color=(0.62, 0.66, 0.85))
    PF.rotulo(lz, "28 DE SEPTIEMBRE DE 1541", W * 0.50, H * 0.20, 60, t, T("guadalajara", "28", 0) - 0.1, F1("guadalajara", 0) + 0.6,
              rot=-1.2)


PGU2 = PF.Plano("e28_guadalajara_amanecer_a", F("guadalajara", 1) - 0.3, F("guadalajara", 2), z0=1.14, z1=1.22, c0=(0.52, 0.56),
                c1=(0.50, 0.58), par=(28, 6), tono=NOCHE_AZUL)
snd(F("guadalajara", 1) - 0.2, "pasos", 0.30, dur=9.5)


@toma(F("guadalajara", 1) - 0.3, ("fundido", 0.5))
def GU2(lz, t):
    PGU2.fondo(lz, t)
    tinte(lz, (0.55, 0.62, 1.0), 0.40 * (1 - 0.5 * smooth(prog(t, F1("guadalajara", 1) - 3, F1("guadalajara", 1)))))
    neblina(lz, t, 0.52, 0.66, fuerza=0.15, color=(0.62, 0.66, 0.85))
    ta = F("guadalajara", 1) - 0.3
    sil = (0.42, 0.46, 0.70)
    tropa(lz, PGU2, t, "c04_caxcan_corre", ta, ta + 10.0, -0.30, 1.10, 0.86, 0.24, n=8, dx=0.07, dy=0.03, paso=1.35, tono=sil)
    anda(lz, PGU2, t, "c02_guerrero_corre", T("guadalajara", "primeros", 1) - 1.5, ta + 10.0, -0.15, 0.85, 0.93, 0.32, paso=1.35,
         tono=sil)


PGU3 = PF.Plano("e29_guadalajara_fuego_a", F("guadalajara", 2) - 0.3, F("guadalajara", 3), z0=1.10, z1=1.20, c0=(0.50, 0.545),
                c1=(0.52, 0.58), par=(28, 6), tono=INCENDIO)
FUEGOS_GU = [(0.30, 0.42), (0.38, 0.48), (0.78, 0.47)]
snd(F("guadalajara", 2) - 0.3, "fuego", 0.55, dur=9.0)
snd(F("guadalajara", 2) + 0.5, "cuerno", 0.45, tono=0.9)
snd(F("guadalajara", 2) + 1.5, "espada", 0.40)
snd(F("guadalajara", 2) + 3.0, "espada", 0.40, tono=1.1)


@toma(F("guadalajara", 2) - 0.3, ("latigo", 0.4))
def GU3(lz, t):
    PGU3.fondo(lz, t)
    incendio(lz, PGU3, t, FUEGOS_GU)
    ta = F("guadalajara", 2) - 0.3
    quieto(lz, PGU3, t, "h12_soldados/01", 0.82, 0.82, 0.28, flip=True, tono=INCENDIO)
    tropa(lz, PGU3, t, "c04_caxcan_corre", ta, ta + 7.0, -0.25, 0.70, 0.86, 0.30, n=5, dx=0.08, dy=0.02, paso=1.35, tono=INCENDIO)
    quieto(lz, PGU3, t, "h12_soldados/02", 0.73, 0.86, 0.31, flip=True, tono=INCENDIO, fase=0.7)
    flechas(lz, t, [(ta + 1.0, 1.0, (0.20, 0.60), (0.75, 0.62), 6, 5), (ta + 3.5, 1.0, (0.25, 0.58), (0.78, 0.60), 6, 6)])


PGU4 = PF.Plano("e45_iglesia_refugio_a", F("guadalajara", 3) - 0.25, F("guadalajara", 4), z0=1.15, z1=1.22, c0=(0.50, 0.56),
                c1=(0.52, 0.58), par=(20, 5), tono=FOGATA)
_t_pue = T("guadalajara", "puerta", 3)
snd(F("guadalajara", 3) - 0.2, "golpe_suave", 0.5)
snd(_t_pue - 0.1, "crujido", 0.45, dur=0.8)


@toma(F("guadalajara", 3) - 0.25, ("corte", 0))
def GU4(lz, t):
    PGU4.fondo(lz, t)
    humo_en(lz, PGU4, t, 0.52, 0.66, s=1.0, color=(0.25, 0.22, 0.22), op=0.26, sem=14)
    brillo_en(lz, PGU4, t, 0.95, 0.30, 80, inten=0.40, sem=15, chis=6)
    brillo_en(lz, PGU4, t, 0.24, 0.48, 40, color=(1.0, 0.80, 0.45), inten=0.30, sem=16)
    quieto(lz, PGU4, t, "h15_gente/02", 0.16, 0.89, 0.20, tono=FOGATA, fase=0.5)
    if t < _t_pue:
        quieto(lz, PGU4, t, "h23_beatriz/00", 0.32, 0.90, 0.46, tono=FOGATA)
    else:
        quieto(lz, PGU4, t, "h23_beatriz/02", 0.70, 0.88, 0.44, tono=FOGATA, t_in=_t_pue - 0.05, rot=1.5 * math.sin(t * 8))


PGU5 = PF.Plano("e45_iglesia_refugio_b", F("guadalajara", 4) - 0.3, F("guadalajara", 5), z0=1.55, z1=1.62, c0=(0.55, 0.66),
                c1=(0.56, 0.66), par=(14, 3), tono=FOGATA)
snd(T("guadalajara", "beatriz", 4) - 0.1, "papel", 0.5)


@toma(F("guadalajara", 4) - 0.3, ("fundido", 0.4))
def GU5(lz, t):
    PGU5.fondo(lz, t)
    humo_en(lz, PGU5, t, 0.26, 0.60, s=1.0, color=(0.25, 0.22, 0.22), op=0.24, sem=17)
    desenfoca(lz, 1.6)
    quieto(lz, PGU5, t, "h23_beatriz/01", 0.55, 0.92, 0.46, tono=FOGATA)
    PF.rotulo(lz, "BEATRIZ HERNÁNDEZ", W * 0.50, H * 0.19, 60, t, T("guadalajara", "beatriz", 4) - 0.1, F1("guadalajara", 4) + 0.3,
              rot=-1.2)


PGU6 = PF.Plano("e29_guadalajara_fuego_b", F("guadalajara", 5) - 0.3, F("guadalajara", 6), z0=1.10, z1=1.20, c0=(0.50, 0.545),
                c1=(0.50, 0.58), par=(28, 6), tono=INCENDIO)
_t_part = T("guadalajara", "partieron", 5)
_t_caer = T("guadalajara", "caer", 5)
snd(F("guadalajara", 5) - 0.2, "galope", 0.6, dur=5.0)
snd(_t_part, "impacto", 0.5, tono=0.6)
snd(_t_caer, "latido", 0.5)


@toma(F("guadalajara", 5) - 0.3, ("latigo", 0.4))
def GU6(lz, t):
    PGU6.fondo(lz, t)
    incendio(lz, PGU6, t, [(0.25, 0.45), (0.70, 0.50)])
    ta = F("guadalajara", 5) - 0.3
    tumba(lz, PGU6, t, "h14_guerreros/03", 0.40, 0.84, 0.30, _t_part + 0.3, tono=INCENDIO, lado=-1)
    tumba(lz, PGU6, t, "h14_guerreros/02", 0.56, 0.86, 0.30, _t_part + 0.8, tono=INCENDIO, lado=-1)
    tropa(lz, PGU6, t, "c04_caxcan_corre", ta + 0.5, ta + 5.5, 0.62, -0.30, 0.88, 0.30, n=3, dx=0.10, paso=1.35, tono=INCENDIO)
    tropa(lz, PGU6, t, "c07_jinete_galope", ta + 0.3, ta + 5.0, 1.30, -0.30, 0.86, 0.32, n=4, dx=0.12, paso=1.7, tono=INCENDIO,
          desde_antes=False)
    tumba(lz, PGU6, t, "h14_guerreros/00", 0.30, 0.91, 0.32, _t_caer + 0.2, tono=INCENDIO, lado=1)
    latido_rojo(lz, t, _t_caer - 0.2, F1("guadalajara", 5) + 0.5, k=0.18)


PGU7 = PF.Plano("e23_subida_mixton_a", F("guadalajara", 6) - 0.3, t1_("guadalajara") + 0.5, z0=1.08, z1=1.16, c0=(0.50, 0.53),
                c1=(0.52, 0.55), par=(30, 7), tono=(0.80, 0.62, 0.62))
snd(F("guadalajara", 6) - 0.2, "pasos", 0.25, dur=5.0)


@toma(F("guadalajara", 6) - 0.3, ("fundido", 0.7))
def GU7(lz, t):
    PGU7.fondo(lz, t)
    tinte(lz, (0.70, 0.55, 0.60), 0.25)
    ta = F("guadalajara", 6) - 0.3
    tono = (0.70, 0.55, 0.55)
    for k, pz in enumerate(["h14_guerreros/02", "h08_tenamaxtli/04", "h15_gente/03", "h14_guerreros/03"]):
        aleja(lz, PGU7, t, pz, ta + 0.9 * k - 1.0, ta + 0.9 * k + 6.0, (0.48, 0.92), (0.62, 0.62), 0.30, 0.13, tono=tono, pasos=1.2)


# ------------------------------------------------------------------ la noche de la herida
PHE1 = PF.Plano("e30_mixton_noche_fuego_b", t0_("herida") - 0.3, F("herida", 1), z0=1.15, z1=1.22, c0=(0.48, 0.56), c1=(0.50, 0.58),
                par=(24, 5), tono=NOCHE_FUEGO)
snd(t0_("herida") - 0.2, "fuego", 0.30, dur=21.0)


def fogata_herida(lz, pl, t, k=1.0):
    brillo_en(lz, pl, t, 0.46, 0.68, 85, inten=0.42 * k, sem=50, chis=8)


@toma(t0_("herida") - 0.3, ("fundido", 0.7))
def HE1(lz, t):
    PHE1.fondo(lz, t)
    estrellas(lz, t, y1=0.25)
    fuegos_valle(lz, PHE1, t, "e30_mixton_noche_fuego_b", (0.40, 0.38, 0.95, 0.62), n=20)
    fogata_herida(lz, PHE1, t)
    quieto(lz, PHE1, t, "h05_ollin_joven/04", 0.34, 0.80, 0.22, tono=NOCHE_FUEGO)
    quieto(lz, PHE1, t, "h02_tecuani_g/03", 0.60, 0.79, 0.30, tono=NOCHE_FUEGO, fase=0.8)


PHE2 = PF.Plano("e30_mixton_noche_fuego_b", F("herida", 1) - 0.25, F("herida", 2), z0=1.90, z1=1.94, c0=(0.36, 0.68), c1=(0.36, 0.68),
                par=(12, 2), tono=NOCHE_FUEGO)


@toma(F("herida", 1) - 0.25, ("corte", 0))
def HE2(lz, t):
    PHE2.fondo(lz, t)
    fogata_herida(lz, PHE2, t)
    desenfoca(lz, 2.0)
    quieto(lz, PHE2, t, "h05_ollin_joven/04", 0.34, 0.80, 0.22, tono=NOCHE_FUEGO)


PHE3 = PF.Plano("e30_mixton_noche_fuego_b", F("herida", 2) - 0.25, F("herida", 3), z0=1.80, z1=1.84, c0=(0.60, 0.66), c1=(0.60, 0.66),
                par=(12, 2), tono=NOCHE_FUEGO)


@toma(F("herida", 2) - 0.25, ("corte", 0))
def HE3(lz, t):
    PHE3.fondo(lz, t)
    fogata_herida(lz, PHE3, t)
    desenfoca(lz, 2.0)
    quieto(lz, PHE3, t, "h02_tecuani_g/03", 0.60, 0.79, 0.30, tono=NOCHE_FUEGO, fase=0.8)


PHE4 = PF.Plano("e30_mixton_noche_fuego_b", F("herida", 3) - 0.3, t1_("herida") + 0.6, z0=1.40, z1=1.55, c0=(0.48, 0.64),
                c1=(0.48, 0.66), par=(16, 3), tono=NOCHE_FUEGO)


@toma(F("herida", 3) - 0.3, ("fundido", 0.6))
def HE4(lz, t):
    PHE4.fondo(lz, t)
    estrellas(lz, t, y1=0.30)
    fogata_herida(lz, PHE4, t, k=1.0 - 0.5 * smooth(prog(t, F("herida", 3), t1_("herida"))))
    quieto(lz, PHE4, t, "h02_tecuani_g/03", 0.52, 0.79, 0.30, tono=NOCHE_FUEGO, fase=0.8)
    apoyo = smooth(prog(t, F("herida", 3) - 0.2, F("herida", 3) + 1.5))
    quieto(lz, PHE4, t, "h05_ollin_joven/04", 0.43 + 0.02 * apoyo, 0.80, 0.22, tono=NOCHE_FUEGO, rot=-14 * apoyo)


# ================================================================== ACTO V — el virrey y la caída (oct-dic 1541)
MIRA.update({"h17_mendoza/00": 1, "h17_mendoza/01": 1, "h24_lascasas/03": 1, "h18_ollin_viejo/04": 1})
AMB += [(t0_("virrey") - 0.3, F("virrey", 4), "alba", 0.35), (F("virrey", 4) - 0.3, t1_("virrey") + 0.3, "viento_noche", 0.30),
        (t0_("cerco") - 0.3, F("cerco", 4), "alba", 0.30), (F("cerco", 4) - 0.3, t1_("cerco") + 0.3, "viento_noche", 0.40),
        (t0_("ultima") - 0.3, t1_("ultima") + 0.3, "viento_noche", 0.35), (t0_("ultima") - 0.3, t1_("ultima") + 0.3, "grillos", 0.22),
        (t0_("caida") - 0.3, F("caida", 1), "viento_noche", 0.30), (F("caida", 4) - 0.3, t1_("caida") + 0.5, "alba", 0.35)]


def canonazo(lz, pl, t, t_i, x, y, sem=0):
    """Fogonazo + humo blanco de un cañón pintado en (x, y) del escenario."""
    if t < t_i or t > t_i + 3.0:
        return
    X, Y, s = pl.P(t, x, y)
    f = math.exp(-(t - t_i) * 9)
    PF.brillo(lz, X, Y, 140 * s, color=(1.0, 0.85, 0.55), inten=0.9 * f, t=t, sem=sem)
    PF.humo(lz, t, X, Y, s=1.6 * s * (0.6 + prog(t, t_i, t_i + 3.0)), color=(0.90, 0.88, 0.86),
            op=0.45 * (1 - prog(t, t_i, t_i + 3.0)), sem=sem, alto=160.0)


PVR1 = PF.Plano("e31_valle_ejercito_a", t0_("virrey") - 0.3, F("virrey", 1), z0=1.06, z1=1.20, c0=(0.50, 0.50), c1=(0.42, 0.55),
                par=(30, 7), tono=ALBA)
snd(T("virrey", "2", 0) - 0.1, "papel", 0.5)
snd(T("virrey", "mendoza", 0) - 0.1, "papel", 0.5)
for _kk in range(8):
    snd(t0_("virrey") + 1.0 * _kk, "tambor", 0.45, tono=0.6)


@toma(t0_("virrey") - 0.3, ("fundido", 0.8))
def VR1(lz, t):
    PVR1.fondo(lz, t)
    for k, (x, y) in enumerate([(0.30, 0.47), (0.36, 0.43), (0.42, 0.50)]):
        humo_en(lz, PVR1, t, x, y, s=0.6, color=(0.86, 0.84, 0.82), op=0.20, sem=60 + k)
    agua(lz, PVR1, t, "e31_valle_ejercito_a")
    capitulo(lz, t, "V", "EL VIRREY", t0_("virrey") + 0.3, T("virrey", "2", 0) - 0.4)
    PF.rotulo(lz, "2 DE OCTUBRE DE 1541", W * 0.32, H * 0.19, 54, t, T("virrey", "2", 0) - 0.1, F1("virrey", 0) + 0.2, rot=-1.2)
    PF.rotulo(lz, "el virrey ANTONIO DE MENDOZA", W * 0.34, H * 0.29, 44, t, T("virrey", "mendoza", 0) - 0.1, F1("virrey", 0) + 0.2,
              rot=1.0)


PVR2 = PF.Plano("e31_valle_ejercito_b", F("virrey", 1) - 0.3, F("virrey", 2), z0=1.08, z1=1.28, c0=(0.55, 0.50), c1=(0.58, 0.57),
                par=(30, 7), tono=ALBA)
snd(F("virrey", 1) - 0.2, "pasos", 0.40, dur=12.0)
snd(T("virrey", "cuatrocientos", 1) - 0.1, "papel", 0.5)
for _p in ("tlaxcaltecas", "mexicas", "purépechas"):
    snd(T("virrey", _p, 1) - 0.1, "papel", 0.4)


@toma(F("virrey", 1) - 0.3, ("fundido", 0.5))
def VR2(lz, t):
    PVR2.fondo(lz, t)
    for k, (x, y) in enumerate([(0.40, 0.45), (0.50, 0.40), (0.60, 0.48), (0.70, 0.43)]):
        humo_en(lz, PVR2, t, x, y, s=0.5, color=(0.86, 0.84, 0.82), op=0.18, sem=64 + k)
    ta = F("virrey", 1) - 0.3
    tropa(lz, PVR2, t, "c06_aliado_marcha", ta, ta + 12.0, 0.30, 0.95, 0.62, 0.07, n=10, dx=0.04, dy=0.01, paso=1.0, tono=ALBA)
    tropa(lz, PVR2, t, "c06_aliado_marcha", ta + 1.0, ta + 13.0, 0.25, 0.90, 0.66, 0.08, n=10, dx=0.04, dy=0.01, paso=1.0, tono=ALBA,
          sem=3)
    plantas(lz, PVR2, t, [("u03_naturaleza/03", 0.12, 1.04, 0.42, 1.3, False)], tono=ALBA)
    PF.rotulo(lz, "450 ESPAÑOLES", W * 0.70, H * 0.19, 54, t, T("virrey", "cuatrocientos", 1) - 0.1, F1("virrey", 1) + 0.2, rot=-1.2)
    PF.rotulo(lz, "decenas de miles de aliados", W * 0.70, H * 0.29, 42, t, T("virrey", "decenas", 1) - 0.1, F1("virrey", 1) + 0.2,
              rot=1.0)
    for k, p in enumerate(("TLAXCALTECAS", "MEXICAS", "PURÉPECHAS")):
        PF.rotulo(lz, p, W * (0.52 + 0.17 * k), H * 0.80, 36, t, T("virrey", p.lower(), 1) - 0.1,
                  F1("virrey", 1) + 0.2, rot=(-1) ** k * 2)


PVR3 = PF.Plano("e10_pueblo_entrada_b", F("virrey", 2) - 0.25, F("virrey", 3), z0=1.40, z1=1.46, c0=(0.50, 0.64), c1=(0.50, 0.64),
                par=(20, 4), tono=ALBA)


@toma(F("virrey", 2) - 0.25, ("fundido", 0.4))
def VR3(lz, t):
    PVR3.fondo(lz, t)
    desenfoca(lz, 1.5)
    for k, (pz, x) in enumerate([("h13_aliados/00", 0.32), ("h13_aliados/01", 0.47), ("h13_aliados/05", 0.62)]):
        quieto(lz, PVR3, t, pz, x, 0.90, 0.40, tono=ALBA, fase=0.5 * k)


PVR4 = PF.Plano("e32_penoles_humo_a", F("virrey", 3) - 0.3, F("virrey", 4), z0=1.08, z1=1.18, c0=(0.50, 0.50), c1=(0.55, 0.47),
                par=(30, 7), tono=(0.88, 0.86, 0.90))
_t_cuatro = T("virrey", "cuatro", 3)
_t_juch = T("virrey", "juchipila", 3)
for _kk in range(5):
    snd(F("virrey", 3) + 0.9 * _kk, "trueno", 0.30 + 0.05 * (_kk % 2))
snd(_t_juch - 0.1, "latido", 0.5)


@toma(F("virrey", 3) - 0.3, ("fundido", 0.5))
def VR4(lz, t):
    PVR4.fondo(lz, t)
    for k, tc in enumerate([F("virrey", 3) + 0.9 * j for j in range(5)]):
        canonazo(lz, PVR4, t, tc, 0.22 + 0.15 * (k % 3), 0.25, sem=70 + k)
    quieto(lz, PVR4, t, "h05_ollin_joven/04", 0.60, 0.92, 0.22, tono=(0.86, 0.84, 0.90))
    quieto(lz, PVR4, t, "h02_tecuani_g/00", 0.72, 0.98, 0.38, flip=True, tono=(0.86, 0.84, 0.90))
    PF.rotulo(lz, "NOCHISTLÁN · 4 DÍAS", W * 0.30, H * 0.19, 54, t, _t_cuatro - 0.2, F1("virrey", 3) + 0.2, rot=-1.2)
    PF.rotulo(lz, "JUCHIPILA", W * 0.64, H * 0.30, 54, t, _t_juch - 0.1, F1("virrey", 3) + 0.2, rot=1.5, tinta=(120, 24, 14))


PVR5 = PF.Plano("e47_campamento_virrey_b", F("virrey", 4) - 0.3, F("virrey", 5), z0=1.15, z1=1.20, c0=(0.55, 0.58), c1=(0.56, 0.59),
                par=(24, 5), tono=ALBA)


@toma(F("virrey", 4) - 0.3, ("fundido", 0.5))
def VR5(lz, t):
    PVR5.fondo(lz, t)
    humo_en(lz, PVR5, t, 0.42, 0.62, s=0.6, color=(0.86, 0.84, 0.82), op=0.18, sem=75)
    quieto(lz, PVR5, t, "h21_espanoles_1541/04", 0.48, 0.86, 0.38, tono=ALBA)
    quieto(lz, PVR5, t, "h17_mendoza/02", 0.68, 0.87, 0.42, flip=True, tono=ALBA, fase=0.6)
    PF.rotulo(lz, "MÁS DE 20 REQUERIMIENTOS", W * 0.32, H * 0.19, 50, t, T("virrey", "veinte", 4) - 0.1, F1("virrey", 4) + 0.2, rot=-1.2)


PVR6 = PF.Plano("e47_campamento_virrey_a", F("virrey", 5) - 0.25, F("virrey", 6), z0=1.25, z1=1.32, c0=(0.42, 0.62), c1=(0.44, 0.62),
                par=(22, 5), tono=ALBA)
_t_can = T("virrey", "cañones", 5)
for _kk in range(3):
    snd(_t_can + 0.4 + 0.35 * _kk, "trueno", 0.55)


@toma(F("virrey", 5) - 0.25, ("corte", 0))
def VR6(lz, t):
    PVR6.fondo(lz, t)
    for k, x in enumerate((0.36, 0.46, 0.56)):
        canonazo(lz, PVR6, t, _t_can + 0.4 + 0.35 * k, x, 0.64, sem=80 + k)
    quieto(lz, PVR6, t, "h17_mendoza/04", 0.28, 0.92, 0.48, tono=ALBA)


PVR7 = PF.Plano("e32_penoles_humo_b", F("virrey", 6) - 0.3, t1_("virrey") + 0.5, z0=1.08, z1=1.20, c0=(0.50, 0.50), c1=(0.45, 0.55),
                par=(30, 7), tono=(0.86, 0.84, 0.90))
_t_tram = T("virrey", "trampa", 6)
snd(T("virrey", "mazorca", 6) - 0.1, "crujido", 0.4, dur=0.8)


@toma(F("virrey", 6) - 0.3, ("fundido", 0.5))
def VR7(lz, t):
    PVR7.fondo(lz, t)
    tm = T("virrey", "mazorca", 6)
    pega(lz, "u01_utileria/03", W * 0.24, H * 0.36, 200, t, tm - 0.2, T("virrey", "tenamaxtli", 6) - 0.3, rot=-8)
    if tm < t < tm + 1.5:
        X, Y = W * 0.24, H * 0.36
        PF.chispas(lz, t, X, Y + 40, s=2.0, n=14, sem=9)
    quieto(lz, PVR7, t, "h08_tenamaxtli/01", 0.70, 0.92, 0.40, tono=(0.86, 0.84, 0.90), t_in=T("virrey", "tenamaxtli", 6) - 0.2)
    quieto(lz, PVR7, t, "h14_guerreros/03", 0.84, 0.94, 0.38, tono=(0.86, 0.84, 0.90), t_in=_t_tram - 0.1, fase=0.5)


# ------------------------------------------------------------------ el cerco
PCR1 = PF.Plano("e33_mixton_cerco_a", t0_("cerco") - 0.3, F("cerco", 1), z0=1.08, z1=1.18, c0=(0.50, 0.53), c1=(0.48, 0.56),
                par=(28, 6), tono=SOL_DURO)
snd(t0_("cerco"), "tambor", 0.35, tono=0.5)


@toma(t0_("cerco") - 0.3, ("fundido", 0.7))
def CR1(lz, t):
    PCR1.fondo(lz, t)
    PF.arena_viento(lz, t, fuerza=0.4, y0=0.60, sem=13)
    quieto(lz, PCR1, t, "h15_gente/05", 0.30, 0.70, 0.20, tono=SOL_DURO)
    quieto(lz, PCR1, t, "h02_tecuani_g/00", 0.64, 0.80, 0.34, flip=True, tono=SOL_DURO, fase=0.4)
    aves(lz, t, [(t0_("cerco"), 9.0, 0.18, 0.12, 64, 1, 0.3), (t0_("cerco") + 2.0, 9.0, 0.24, 0.18, 50, -1, 1.2)])


PCR2 = PF.Plano("e33_mixton_cerco_b", F("cerco", 1) - 0.3, F("cerco", 2), z0=1.30, z1=1.40, c0=(0.38, 0.66), c1=(0.40, 0.68),
                par=(22, 5), tono=SOL_DURO)
snd(T("cerco", "agua", 1) - 0.1, "gota", 0.5)


@toma(F("cerco", 1) - 0.3, ("fundido", 0.5))
def CR2(lz, t):
    PCR2.fondo(lz, t)
    PF.brillo(lz, *PCR2.P(t, 0.70, 0.04)[:2], 380, color=(1.0, 0.92, 0.70), inten=0.20, t=t, sem=86)
    quieto(lz, PCR2, t, "u02_utileria_guerra/10", 0.32, 0.86, 0.07, tono=SOL_DURO, t_in=T("cerco", "agua", 1) - 0.2)
    quieto(lz, PCR2, t, "h15_gente/05", 0.52, 0.80, 0.24, tono=SOL_DURO)
    quieto(lz, PCR2, t, "h05_ollin_joven/04", 0.66, 0.82, 0.24, tono=SOL_DURO, fase=0.7)
    aves(lz, t, [(F("cerco", 1), 8.0, 0.22, 0.16, 60, -1, 0.6)])


PCR3 = PF.Plano("e30_mixton_noche_fuego_a", F("cerco", 2) - 0.25, F("cerco", 3), z0=1.55, z1=1.60, c0=(0.38, 0.68), c1=(0.38, 0.68),
                par=(14, 3), tono=NOCHE_FUEGO)


@toma(F("cerco", 2) - 0.25, ("fundido", 0.4))
def CR3(lz, t):
    PCR3.fondo(lz, t)
    brillo_en(lz, PCR3, t, 0.28, 0.75, 60, inten=0.36, sem=87, chis=6)
    desenfoca(lz, 1.6)
    quieto(lz, PCR3, t, "h03_citlali/05", 0.40, 0.92, 0.44, tono=NOCHE_FUEGO)
    quieto(lz, PCR3, t, "u01_utileria/01", 0.30, 0.94, 0.06, tono=NOCHE_FUEGO)


PCR4 = PF.Plano("e30_mixton_noche_fuego_a", F("cerco", 3) - 0.25, F("cerco", 4), z0=1.30, z1=1.36, c0=(0.42, 0.64), c1=(0.43, 0.64),
                par=(20, 4), tono=NOCHE_FUEGO)


@toma(F("cerco", 3) - 0.25, ("corte", 0))
def CR4(lz, t):
    PCR4.fondo(lz, t)
    brillo_en(lz, PCR4, t, 0.28, 0.75, 70, inten=0.38, sem=87, chis=6)
    quieto(lz, PCR4, t, "h03_citlali/05", 0.36, 0.86, 0.38, tono=NOCHE_FUEGO)
    quieto(lz, PCR4, t, "h02_tecuani_g/03", 0.60, 0.86, 0.38, tono=NOCHE_FUEGO, fase=0.8)


PCR5 = PF.Plano("e01_mixton_noche_a", F("cerco", 4) - 0.3, t1_("cerco") + 0.5, z0=1.10, z1=1.24, c0=(0.50, 0.53), c1=(0.60, 0.50),
                par=(30, 6))


@toma(F("cerco", 4) - 0.3, ("fundido", 0.6))
def CR5(lz, t):
    PCR5.fondo(lz, t)
    estrellas(lz, t, y1=0.22)
    fuegos_valle(lz, PCR5, t, "e01_mixton_noche_a", FZ_NO, n=50, inten=0.30 + 0.20 * smooth(prog(t, F("cerco", 4), t1_("cerco"))))
    brillo_en(lz, PCR5, t, 0.33, 0.79, 70, inten=0.40 * (1 - 0.6 * smooth(prog(t, F("cerco", 4) + 2.5, t1_("cerco")))), sem=1)
    quieto(lz, PCR5, t, "h02_tecuani_g/00", 0.55, 0.80, 0.34, tono=NOCHE_FUEGO)


# ------------------------------------------------------------------ la última noche
PUL1 = PF.Plano("e30_mixton_noche_fuego_b", t0_("ultima") - 0.3, F("ultima", 1), z0=1.50, z1=1.58, c0=(0.48, 0.64), c1=(0.48, 0.65),
                par=(16, 3), tono=NOCHE_FUEGO)
snd(t0_("ultima") - 0.2, "fuego", 0.25, dur=34.0)


@toma(t0_("ultima") - 0.3, ("fundido", 0.7))
def UL1(lz, t):
    PUL1.fondo(lz, t)
    fogata_herida(lz, PUL1, t, k=0.8)
    quieto(lz, PUL1, t, "h05_ollin_joven/04", 0.38, 0.80, 0.22, tono=NOCHE_FUEGO)
    quieto(lz, PUL1, t, "h02_tecuani_g/03", 0.58, 0.79, 0.30, tono=NOCHE_FUEGO, fase=0.8)


PUL2 = PF.Plano("e34_vereda_barranca_a", F("ultima", 1) - 0.3, F("ultima", 2), z0=1.08, z1=1.24, c0=(0.50, 0.53), c1=(0.42, 0.66),
                par=(30, 7), tono=AZUL)


@toma(F("ultima", 1) - 0.3, ("fundido", 0.6))
def UL2(lz, t):
    PUL2.fondo(lz, t)
    neblina(lz, t, 0.55, 0.80, fuerza=0.16, color=(0.55, 0.60, 0.80))
    quieto(lz, PUL2, t, "h02_tecuani_g/00", 0.20, 0.80, 0.36, tono=AZUL)
    tv = T("ultima", "venados", 1) - 0.2
    if tv < t < tv + 4.0:
        X, Y, h = PUL2.en(t, lerp(0.30, 0.42, prog(t, tv, tv + 4.0)), lerp(0.70, 0.80, prog(t, tv, tv + 4.0)), 0.10)
        vision(lz, "c08_perro_corre/ciclo_00", X, Y - 0.4 * h, h, t, tv, tv + 3.2, flip=True, op=0.30, sube=0.0)


PUL3 = PF.Plano("e30_mixton_noche_fuego_b", F("ultima", 2) - 0.2, F("ultima", 3), z0=1.85, z1=1.90, c0=(0.38, 0.68), c1=(0.38, 0.68),
                par=(12, 2), tono=NOCHE_FUEGO)


@toma(F("ultima", 2) - 0.2, ("corte", 0))
def UL3(lz, t):
    PUL3.fondo(lz, t)
    fogata_herida(lz, PUL3, t, k=0.8)
    desenfoca(lz, 2.0)
    quieto(lz, PUL3, t, "h05_ollin_joven/03", 0.38, 0.86, 0.32, tono=NOCHE_FUEGO, rot=1.5 * math.sin(t * 8))


PUL4 = PF.Plano("e30_mixton_noche_fuego_b", F("ultima", 3) - 0.3, F("ultima", 4), z0=1.65, z1=1.75, c0=(0.50, 0.66), c1=(0.50, 0.66),
                par=(14, 3), tono=NOCHE_FUEGO)
_t_toma = T("ultima", "tómala", 3)
snd(T("ultima", "piedra", 3) - 0.1, "brillo", 0.45)


@toma(F("ultima", 3) - 0.3, ("fundido", 0.5))
def UL4(lz, t):
    PUL4.fondo(lz, t)
    fogata_herida(lz, PUL4, t, k=0.8)
    desenfoca(lz, 1.4)
    quieto(lz, PUL4, t, "h02_tecuani_g/04", 0.56, 0.86, 0.34, tono=NOCHE_FUEGO)
    if t >= _t_toma:
        quieto(lz, PUL4, t, "h05_ollin_joven/05", 0.40, 0.86, 0.36, tono=NOCHE_FUEGO, t_in=_t_toma - 0.1)
    else:
        quieto(lz, PUL4, t, "h05_ollin_joven/04", 0.40, 0.83, 0.25, tono=NOCHE_FUEGO)
    X, Y, h = PUL4.en(t, 0.50, 0.70, 0.02)
    PF.brillo(lz, X, Y, 60, color=(0.55, 1.0, 0.70), inten=0.32, t=t, sem=88)


PUL5 = PF.Plano("e30_mixton_noche_fuego_b", F("ultima", 4) - 0.25, F("ultima", 5), z0=1.95, z1=2.02, c0=(0.58, 0.64), c1=(0.58, 0.64),
                par=(12, 2), tono=NOCHE_FUEGO)


@toma(F("ultima", 4) - 0.25, ("corte", 0))
def UL5(lz, t):
    PUL5.fondo(lz, t)
    fogata_herida(lz, PUL5, t, k=0.7)
    desenfoca(lz, 2.4)
    quieto(lz, PUL5, t, "h02_tecuani_g/04", 0.56, 0.86, 0.34, tono=NOCHE_FUEGO)


PUL6 = PF.Plano("e34_vereda_barranca_b", F("ultima", 5) - 0.2, t1_("ultima") + 0.6, z0=1.20, z1=1.28, c0=(0.50, 0.60), c1=(0.48, 0.62),
                par=(26, 6), tono=AZUL)
snd(F("ultima", 6) - 0.1, "pasos", 0.25, dur=2.0)


@toma(F("ultima", 5) - 0.2, ("fundido", 0.5))
def UL6(lz, t):
    PUL6.fondo(lz, t)
    neblina(lz, t, 0.55, 0.80, fuerza=0.14, color=(0.55, 0.60, 0.80))
    ta = F("ultima", 5) - 0.2
    aleja(lz, PUL6, t, "h03_citlali/04", ta + 0.5, t1_("ultima") + 0.6, (0.62, 0.90), (0.48, 0.72), 0.40, 0.22, tono=AZUL, pasos=1.6,
          flip=True)
    aleja(lz, PUL6, t, "h05_ollin_joven/01", ta, t1_("ultima") + 0.6, (0.72, 0.93), (0.56, 0.74), 0.42, 0.23, tono=AZUL, pasos=1.6,
          flip=True)


# ------------------------------------------------------------------ la caída (diciembre de 1541)
PCA1 = PF.Plano("e01_mixton_noche_a", t0_("caida"), F("caida", 0) + 0.2, z0=1.15, z1=1.06, c0=(0.55, 0.55), c1=(0.50, 0.51),
                par=(30, 6))
snd(t0_("caida") + 0.5, "latido", 0.5)
snd(t0_("caida") + 1.9, "latido", 0.5)
snd(t0_("caida") + 3.3, "latido", 0.55)
snd(t0_("caida") + 4.3, "cuerno", 0.55, tono=0.8)


@toma(t0_("caida"), ("negro", 0.8))
def CA1(lz, t):
    PCA1.fondo(lz, t)
    fuegos_valle(lz, PCA1, t, "e01_mixton_noche_a", FZ_NO, n=50, inten=0.45)
    tinte(lz, (1.0, 0.70, 0.70), 0.35 * smooth(prog(t, t0_("caida") + 2.0, F("caida", 0))))
    quieto(lz, PCA1, t, "h02_tecuani_g/00", 0.55, 0.80, 0.34, tono=(0.85, 0.70, 0.75))


PCA2 = PF.Plano("e25_mixton_ladera_b", F("caida", 0) + 0.2, F("caida", 1) + 0.2, z0=1.10, z1=1.22, c0=(0.50, 0.53), c1=(0.52, 0.58),
                par=(30, 7), tono=OCASO)
snd(F("caida", 0) + 0.3, "pasos", 0.6, dur=12.0)
snd(F("caida", 0) + 0.3, "tambor", 0.5, tono=0.6)


@toma(F("caida", 0) + 0.2, ("latigo", 0.4))
def CA2(lz, t):
    PCA2.fondo(lz, t)
    ta = F("caida", 0) + 0.2
    for k in range(9):
        aleja(lz, PCA2, t, ("h13_aliados/00", "h13_aliados/01", "h13_aliados/05")[k % 3], ta + 0.4 * k, ta + 0.4 * k + 7.0,
              (0.28 + 0.05 * (k % 5), 0.88), (0.42 + 0.03 * (k % 5), 0.36), 0.16, 0.06, tono=OCASO, pasos=2.6)
    X, Y, h = PCA2.en(t, 0.84, 1.03, 0.46)
    PF.actor(lz, "h02_tecuani_g/05", X, Y, h, tono=OCASO, rot=2 * math.sin(t * 3))


PCA3 = PF.Plano("e35_mixton_asalto_a", F("caida", 1) + 0.2, F("caida", 2), z0=1.10, z1=1.20, c0=(0.50, 0.545), c1=(0.50, 0.57),
                par=(28, 6), tono=OCASO)
_t_perr = T("caida", "perros", 1)
snd(_t_perr - 0.2, "galope", 0.4, dur=3.0)


@toma(F("caida", 1) + 0.2, ("corte", 0))
def CA3(lz, t):
    PCA3.fondo(lz, t)
    ta = F("caida", 1) + 0.2
    tropa(lz, PCA3, t, "c06_aliado_marcha", ta - 1.0, ta + 6.0, -0.20, 0.80, 0.82, 0.24, n=6, dx=0.08, dy=0.02, paso=1.0, tono=OCASO)
    paseo(lz, PCA3, t, "h12_soldados/02", _t_perr - 0.5, _t_perr + 4.0, -0.20, 0.45, 0.90, 0.36, pasos=2.0, tono=OCASO,
          desde_antes=False)
    paseo(lz, PCA3, t, "h12_soldados/04", _t_perr - 0.2, _t_perr + 4.0, -0.30, 0.30, 0.94, 0.40, pasos=2.0, tono=OCASO,
          desde_antes=False)
    flechas(lz, t, [(ta + 0.8, 1.1, (0.85, 0.30), (0.40, 0.70), 6, 7)])


PCA4 = PF.Plano("e24_mixton_cima_dia_b", F("caida", 2) - 0.25, F("caida", 3), z0=1.30, z1=1.40, c0=(0.42, 0.62), c1=(0.44, 0.63),
                par=(24, 5), tono=OCASO)
_tc4 = F("caida", 2)
for _kk in range(5):
    snd(_tc4 + 0.9 * _kk, "espada", 0.4, tono=0.9 + 0.05 * _kk)
    snd(_tc4 + 0.9 * _kk + 0.4, "impacto", 0.35, tono=0.8)


@toma(F("caida", 2) - 0.25, ("latigo", 0.35))
def CA4(lz, t):
    PCA4.fondo(lz, t)
    gente = [("h14_guerreros/00", 0.30, 0.68, 0.22, False), ("h14_guerreros/03", 0.46, 0.70, 0.24, False),
             ("h12_soldados/02", 0.60, 0.69, 0.23, True), ("h13_aliados/00", 0.70, 0.71, 0.24, True),
             ("h02_tecuani_g/02", 0.42, 0.84, 0.38, False), ("h12_soldados/00", 0.66, 0.86, 0.40, True)]
    for k, (pz, x, y, f, fl) in enumerate(sorted(gente, key=lambda g: g[2])):
        X, Y, h = PCA4.en(t, x, y, f)
        PF.actor(lz, pz, X + 10 * math.sin(t * 4 + k), Y, h, flip=fl, tono=OCASO, rot=4 * math.sin(t * 5 + k))
    for k in range(3):
        polvo(lz, PCA4, t, 0.45 + 0.1 * k, 0.75, s=1.6, t_in=_tc4 + 1.2 * k, dur=2.5, op=0.28, sem=90 + k)
    latido_rojo(lz, t, _tc4, F1("caida", 2) + 0.4, k=0.12)


PCA5 = PF.Plano("e36_precipicio_a", F("caida", 3) - 0.3, F("caida", 4), z0=1.10, z1=1.22, c0=(0.50, 0.53), c1=(0.60, 0.60),
                par=(30, 7), tono=OCASO)
snd(F("caida", 3) - 0.2, "viento", 0.25, dur=5.0)


@toma(F("caida", 3) - 0.3, ("fundido", 0.8))
def CA5(lz, t):
    PCA5.fondo(lz, t)
    neblina(lz, t, 0.55, 0.85, fuerza=0.18, color=(0.70, 0.62, 0.70))
    aves(lz, t, [(F("caida", 3) - 1.0, 10.0, 0.62, 0.58, 46, 1, 0.3), (F("caida", 3), 10.0, 0.70, 0.66, 38, -1, 1.5),
                 (F("caida", 3) + 1.0, 10.0, 0.56, 0.60, 40, 1, 2.5)])
    tinte(lz, (0.80, 0.60, 0.70), 0.20)
    sal = 1.0 - smooth(prog(t, F1("caida", 3) - 1.2, F1("caida", 3) + 0.3))
    for k, (pz, x) in enumerate([("h14_guerreros/03", 0.36), ("h15_gente/03", 0.44), ("h14_guerreros/04", 0.52)]):
        quieto(lz, PCA5, t, pz, x, 0.56, 0.16, tono=(0.40, 0.30, 0.36), op=sal, fase=0.4 * k)


PCA6 = PF.Plano("e34_vereda_barranca_b", F("caida", 4) - 0.3, t1_("caida") + 0.6, z0=1.06, z1=1.30, c0=(0.50, 0.50), c1=(0.46, 0.64),
                par=(30, 7), tono=ALBA)
_t_gan = T("caida", "ganado", 4)
snd(_t_gan, "amanecer", 0.5, dur=4.0)


@toma(F("caida", 4) - 0.3, ("fundido", 0.8))
def CA6(lz, t):
    PCA6.fondo(lz, t)
    neblina(lz, t, 0.55, 0.80, fuerza=0.14, color=(0.85, 0.80, 0.90))
    ta = F("caida", 4) - 0.3
    aleja(lz, PCA6, t, "h03_citlali/04", ta, ta + 8.0, (0.50, 0.86), (0.42, 0.66), 0.32, 0.13, tono=ALBA, pasos=1.4, flip=True)
    aleja(lz, PCA6, t, "h05_ollin_joven/01", ta, ta + 8.0, (0.56, 0.88), (0.46, 0.67), 0.33, 0.14, tono=ALBA, pasos=1.4, flip=True)
    PF.brillo(lz, *PCA6.P(t, 0.70, 0.10)[:2], 380, color=(1.0, 0.80, 0.55), inten=0.30 * smooth(prog(t, _t_gan - 1.0, _t_gan + 2.0)),
              t=t, sem=92)


# ================================================================== EPÍLOGO — Ollin, ya viejo
AMB += [(t0_("epilogo") - 0.3, F("epilogo", 2), "grillos", 0.28), (F("epilogo", 2) - 0.3, F("epilogo", 3), "alba", 0.35),
        (F("epilogo", 3) - 0.3, t1_("epilogo") + 0.3, "viento_noche", 0.30), (t0_("final") - 0.3, F("final", 2), "grillos", 0.28),
        (F("final", 2) - 0.3, t1_("cierre") - 2.0, "alba", 0.35)]

PEP1 = PF.Plano("e35_mixton_asalto_b", t0_("epilogo"), F("epilogo", 1), z0=1.06, z1=1.16, c0=(0.50, 0.50), c1=(0.50, 0.54),
                par=(28, 6), tono=OCASO)
snd(t0_("epilogo") + 0.3, "campana", 0.35, tono=0.5)
snd(T("epilogo", "diciembre", 0) - 0.1, "papel", 0.5)
snd(T("epilogo", "herrados", 0) - 0.1, "sello", 0.45)


@toma(t0_("epilogo"), ("negro", 1.0))
def EP1(lz, t):
    PEP1.fondo(lz, t)
    humo_en(lz, PEP1, t, 0.45, 0.30, s=1.2, color=(0.30, 0.28, 0.30), op=0.22, sem=94)
    humo_en(lz, PEP1, t, 0.62, 0.34, s=1.0, color=(0.30, 0.28, 0.30), op=0.20, sem=95)
    aves(lz, t, [(t0_("epilogo"), 11.0, 0.18, 0.14, 56, 1, 0.3), (t0_("epilogo") + 2.0, 10.0, 0.24, 0.20, 44, -1, 1.8)])
    PF.rotulo(lz, "EPÍLOGO", W * 0.5, H * 0.46, 112, t, t0_("epilogo") + 0.6, T("epilogo", "diciembre", 0) - 0.4, rot=1.2)
    PF.rotulo(lz, "DICIEMBRE DE 1541", W * 0.50, H * 0.19, 60, t, T("epilogo", "diciembre", 0) - 0.1, F1("epilogo", 0) + 0.3, rot=-1.2)
    PF.rotulo(lz, "miles de caxcanes, herrados y vendidos", W * 0.52, H * 0.30, 42, t, T("epilogo", "herrados", 0) - 0.1,
              F1("epilogo", 0) + 0.3, rot=1.0)


PEP2 = PF.Plano("e41_casa_vieja_noche_a", F("epilogo", 1) - 0.3, F("epilogo", 2), z0=1.20, z1=1.28, c0=(0.55, 0.60), c1=(0.56, 0.61),
                par=(18, 4), tono=INTERIOR)
snd(F("epilogo", 1) - 0.3, "fuego", 0.30, dur=7.0)


@toma(F("epilogo", 1) - 0.3, ("fundido", 0.8))
def EP2(lz, t):
    PEP2.fondo(lz, t)
    brillo_en(lz, PEP2, t, 0.40, 0.62, 90, inten=0.42, sem=96, chis=8)
    humo_en(lz, PEP2, t, 0.40, 0.55, s=0.6, color=(0.55, 0.50, 0.48), op=0.14, sem=96)
    quieto(lz, PEP2, t, "h18_ollin_viejo/00", 0.58, 0.88, 0.36, tono=INTERIOR)


PEP3 = PF.Plano("e37_sierra_escondite_a", F("epilogo", 2) - 0.3, F("epilogo", 3), z0=1.08, z1=1.18, c0=(0.50, 0.53), c1=(0.56, 0.56),
                par=(28, 6), tono=DORADO)
snd(F("epilogo", 2) + 0.5, "pio", 0.3, tono=1.1)


@toma(F("epilogo", 2) - 0.3, ("fundido", 0.7))
def EP3(lz, t):
    PEP3.fondo(lz, t)
    aves(lz, t, [(F("epilogo", 2) - 0.5, 9.0, 0.18, 0.12, 48, 1, 0.5)])
    quieto(lz, PEP3, t, "h03_citlali/04", 0.40, 0.84, 0.30, tono=DORADO)
    quieto(lz, PEP3, t, "h05_ollin_joven/01", 0.52, 0.86, 0.32, flip=True, tono=DORADO, fase=0.6)


PEP4 = PF.Plano("e39_galeon_a", F("epilogo", 3) - 0.3, t1_("epilogo") + 0.4, z0=1.08, z1=1.20, c0=(0.48, 0.52), c1=(0.38, 0.48),
                par=(26, 6))
snd(F("epilogo", 3) - 0.2, "ola", 0.35, dur=2.0)
snd(F("epilogo", 3) + 4.0, "ola", 0.30, dur=2.0)
snd(T("epilogo", "entregó", 3) - 0.1, "campana", 0.30, tono=0.6)


@toma(F("epilogo", 3) - 0.3, ("fundido", 0.7))
def EP4(lz, t):
    PEP4.fondo(lz, t)
    lluvia(lz, t, n=90, fuerza=0.15, viento=0.25, sem=16)
    te = T("epilogo", "entregó", 3) - 0.2
    pega(lz, "h19_tenamaxtli_espana/02", W * 0.78, H * 0.40, 300, t, te, None, rot=5, tono=(0.85, 0.86, 0.95))
    PF.rotulo(lz, "TENAMAXTLI", W * 0.78, H * 0.16, 60, t, T("epilogo", "tenamaxtli", 3) - 0.1, t1_("epilogo") + 0.3, rot=-1.5)
    PF.rotulo(lz, "casi 10 años más de lucha", W * 0.78, H * 0.26, 38, t, T("epilogo", "siguió", 3) - 0.1, te - 0.2, rot=1.0)


# ------------------------------------------------------------------ bando español: Tenamaxtli ante el Consejo de Indias (1555)
SALA = (0.98, 0.90, 0.82)
PVA1 = PF.Plano("e40_consejo_a", t0_("valladolid") - 0.3, F("valladolid", 1), z0=1.08, z1=1.18, c0=(0.50, 0.53), c1=(0.48, 0.56),
                par=(22, 5), tono=SALA)
snd(t0_("valladolid"), "campana", 0.35, tono=0.7)
snd(T("valladolid", "valladolid", 0) - 0.1, "papel", 0.5)
snd(T("valladolid", "consejo", 0) - 0.1, "papel", 0.5)
snd(T("valladolid", "bartolomé", 0) - 0.1, "papel", 0.5)


@toma(t0_("valladolid") - 0.3, ("fundido", 0.8))
def VA1(lz, t):
    PVA1.fondo(lz, t)
    for k, (pz, x) in enumerate([("h25_oidores/01", 0.42), ("h25_oidores/00", 0.56), ("h25_oidores/04", 0.70)]):
        quieto(lz, PVA1, t, pz, x, 0.78, 0.22, flip=True, tono=SALA, fase=0.4 * k)
    paseo(lz, PVA1, t, "h24_lascasas/03", t0_("valladolid") - 0.3, T("valladolid", "bartolomé", 0) + 1.0, -0.15, 0.20, 0.92, 0.40,
          pasos=1.3, tono=SALA)
    paseo(lz, PVA1, t, "h19_tenamaxtli_espana/00", t0_("valladolid") + 0.2, T("valladolid", "bartolomé", 0) + 1.0, -0.25, 0.30, 0.94,
          0.42, pasos=1.3, tono=SALA)
    PF.rotulo(lz, "VALLADOLID · 1 DE JULIO DE 1555", W * 0.50, H * 0.16, 52, t, T("valladolid", "valladolid", 0) - 0.1,
              F1("valladolid", 0) + 0.2, rot=-1.2)
    PF.rotulo(lz, "CONSEJO DE INDIAS", W * 0.50, H * 0.26, 44, t, T("valladolid", "consejo", 0) - 0.1, F1("valladolid", 0) + 0.2,
              rot=1.0)
    PF.rotulo(lz, "fray Bartolomé de las Casas", W * 0.24, H * 0.40, 38, t, T("valladolid", "bartolomé", 0) - 0.1,
              F1("valladolid", 0) + 0.2, rot=-1.0)


PVA2 = PF.Plano("e40_consejo_a", F("valladolid", 1) - 0.25, F("valladolid", 2), z0=1.45, z1=1.52, c0=(0.30, 0.66), c1=(0.31, 0.66),
                par=(14, 3), tono=SALA)
_t_def = T("valladolid", "defendió", 1)
snd(_t_def - 0.05, "golpe_suave", 0.5)


@toma(F("valladolid", 1) - 0.25, ("corte", 0))
def VA2(lz, t):
    PVA2.fondo(lz, t)
    desenfoca(lz, 1.4)
    quieto(lz, PVA2, t, "h24_lascasas/00", 0.24, 0.94, 0.46, tono=SALA)
    quieto(lz, PVA2, t, "h19_tenamaxtli_espana/00", 0.40, 0.95, 0.47, tono=SALA, fase=0.5)
    PF.rotulo(lz, "NO SE REBELÓ: SE DEFENDIÓ", W * 0.64, H * 0.20, 52, t, _t_def - 0.1, F1("valladolid", 1) + 0.4, rot=-1.2)


PVA3 = PF.Plano("e40_consejo_a", F("valladolid", 2) - 0.25, F("valladolid", 3), z0=1.80, z1=1.86, c0=(0.36, 0.70), c1=(0.36, 0.70),
                par=(12, 2), tono=SALA)
_t_va3 = [T("valladolid", p, 2) for p in ("quemaron", "marcaron", "vendieron")]
for _tv in _t_va3:
    snd(_tv - 0.05, "sello", 0.45)


@toma(F("valladolid", 2) - 0.25, ("corte", 0))
def VA3(lz, t):
    PVA3.fondo(lz, t)
    desenfoca(lz, 1.8)
    quieto(lz, PVA3, t, "h19_tenamaxtli_espana/01", 0.36, 0.95, 0.50, tono=SALA)
    for k, (txt, tp) in enumerate(zip(("QUEMARON", "MARCARON", "VENDIERON"), _t_va3)):
        PF.rotulo(lz, txt, W * 0.72, H * (0.22 + 0.16 * k), 60, t, tp - 0.05, F1("valladolid", 2) + 0.3, rot=(-1) ** k * 2.5,
                  tinta=(120, 24, 14))


PVA4 = PF.Plano("e40_consejo_a", F("valladolid", 3) - 0.25, F("valladolid", 4), z0=1.15, z1=1.22, c0=(0.48, 0.56), c1=(0.48, 0.58),
                par=(20, 4), tono=SALA)
_t_just = T("valladolid", "justicia", 3)
snd(_t_just - 0.1, "tambor", 0.5, tono=0.8)


@toma(F("valladolid", 3) - 0.25, ("fundido", 0.4))
def VA4(lz, t):
    PVA4.fondo(lz, t)
    for k, (pz, x) in enumerate([("h25_oidores/01", 0.42), ("h25_oidores/00", 0.56), ("h25_oidores/04", 0.70)]):
        quieto(lz, PVA4, t, pz, x, 0.78, 0.22, flip=True, tono=SALA, fase=0.4 * k)
    quieto(lz, PVA4, t, "h25_oidores/02", 0.84, 0.86, 0.34, flip=True, tono=SALA, fase=1.2)
    quieto(lz, PVA4, t, "h19_tenamaxtli_espana/00", 0.28, 0.94, 0.44, tono=SALA)
    PF.rotulo(lz, "JUSTICIA NATURAL", W * 0.50, H * 0.18, 86, t, _t_just - 0.1, F1("valladolid", 3) + 0.4, rot=-1.5)


PVA5 = PF.Plano("e40_consejo_a", F("valladolid", 4) - 0.25, F("valladolid", 5), z0=1.95, z1=2.02, c0=(0.34, 0.72), c1=(0.34, 0.72),
                par=(10, 2), tono=SALA)


@toma(F("valladolid", 4) - 0.25, ("corte", 0))
def VA5(lz, t):
    PVA5.fondo(lz, t)
    desenfoca(lz, 2.2)
    quieto(lz, PVA5, t, "h19_tenamaxtli_espana/02", 0.34, 0.95, 0.52, tono=SALA)
    tinte(lz, (0.70, 0.72, 0.85), 0.20 * smooth(prog(t, F("valladolid", 4), F1("valladolid", 4))))


PVA6 = PF.Plano("e39_galeon_b", F("valladolid", 5) - 0.3, t1_("valladolid") + 0.5, z0=1.25, z1=1.08, c0=(0.62, 0.55), c1=(0.55, 0.50),
                par=(26, 6))
snd(F("valladolid", 5) - 0.2, "ola", 0.35, dur=2.0)
snd(T("valladolid", "1556", 5) - 0.1, "papel", 0.5)


@toma(F("valladolid", 5) - 0.3, ("fundido", 0.8))
def VA6(lz, t):
    PVA6.fondo(lz, t)
    tinte(lz, (0.65, 0.70, 0.85), 0.25)
    PF.rotulo(lz, "ÚLTIMO RASTRO · 1556", W * 0.32, H * 0.20, 56, t, T("valladolid", "1556", 5) - 0.1, t1_("valladolid") + 0.3, rot=-1.2)


# ------------------------------------------------------------------ final: orgullo con lágrimas
PFN1 = PF.Plano("e41_casa_vieja_noche_b", t0_("final") - 0.3, F("final", 1), z0=1.12, z1=1.24, c0=(0.42, 0.56), c1=(0.40, 0.60),
                par=(20, 5), tono=INTERIOR)
snd(t0_("final") - 0.2, "fuego", 0.30, dur=16.0)


@toma(t0_("final") - 0.3, ("fundido", 0.8))
def FN1(lz, t):
    PFN1.fondo(lz, t)
    brillo_en(lz, PFN1, t, 0.22, 0.62, 95, inten=0.44, sem=97, chis=8)
    humo_en(lz, PFN1, t, 0.22, 0.50, s=0.6, color=(0.55, 0.50, 0.48), op=0.14, sem=97)
    quieto(lz, PFN1, t, "h18_ollin_viejo/00", 0.40, 0.86, 0.34, tono=INTERIOR)
    tn = T("final", "nietos", 0) - 0.3
    for k, (pz, x, f) in enumerate([("h15_gente/02", 0.56, 0.20), ("h04_ollin_nino/01", 0.68, 0.16), ("h15_gente/05", 0.78, 0.24)]):
        quieto(lz, PFN1, t, pz, x, 0.90, f, flip=True, tono=INTERIOR, t_in=tn + 0.4 * k, fase=0.5 * k)


PFN2 = PF.Plano("e38_mixton_hoy_a", F("final", 1) - 0.3, F("final", 2), z0=1.06, z1=1.18, c0=(0.50, 0.50), c1=(0.52, 0.42),
                par=(30, 7), tono=DORADO)
_t_olv = T("final", "olvidan", 1)
snd(_t_olv - 0.1, "tambor", 0.45, tono=0.7)


@toma(F("final", 1) - 0.3, ("fundido", 1.0))
def FN2(lz, t):
    PFN2.fondo(lz, t)
    aves(lz, t, [(F("final", 1) - 0.5, 9.0, 0.30, 0.22, 52, 1, 0.4)])
    ta = F("final", 1) - 0.3                     # los antepasados, translúcidos, siguen caminando entre los agaves (rigor del MASTER)
    for k, (pz, x0, f) in enumerate([("h15_gente/00", 0.10, 0.20), ("h15_gente/01", 0.20, 0.23), ("h15_gente/03", 0.30, 0.24)]):
        paseo(lz, PFN2, t, pz, ta, F("final", 2) + 0.5, x0, x0 + 0.30, 0.86 + 0.02 * k, f, pasos=1.5, tono=(1.05, 1.0, 0.95),
              op=0.55 * smooth(prog(t, ta + 0.4 * k, ta + 1.4 + 0.4 * k)))
    PF.rotulo(lz, "LOS CERROS NO OLVIDAN", W * 0.50, H * 0.80, 66, t, _t_olv - 0.2, F1("final", 1) + 0.6, rot=-1.0)


PFN3 = PF.Plano("e48_plaza_hoy_a", F("final", 2) - 0.3, F("final", 3), z0=1.08, z1=1.16, c0=(0.50, 0.53), c1=(0.52, 0.55),
                par=(28, 6), tono=DORADO)
snd(T("final", "cuatro", 2) - 0.1, "papel", 0.5)


@toma(F("final", 2) - 0.3, ("fundido", 0.6))
def FN3(lz, t):
    PFN3.fondo(lz, t)
    aves(lz, t, [(F("final", 2), 8.0, 0.20, 0.16, 46, -1, 1.0)])
    for k, (pz, x, f) in enumerate([("h15_gente/01", 0.30, 0.34), ("h15_gente/02", 0.40, 0.22), ("h15_gente/05", 0.70, 0.30)]):
        quieto(lz, PFN3, t, pz, x, 0.92, f, flip=k == 2, tono=(1.05, 1.0, 0.95), op=0.55 * smooth(prog(t, F("final", 2) + 0.5 * k,
               F("final", 2) + 1.5 + 0.5 * k)), fase=0.5 * k)
    PF.rotulo(lz, "HOY", W * 0.30, H * 0.18, 90, t, T("final", "hoy", 2) - 0.1, F1("final", 2) + 0.3, rot=-1.5)
    PF.rotulo(lz, "4 comunidades caxcanas en el sur de Zacatecas", W * 0.36, H * 0.29, 40, t, T("final", "cuatro", 2) - 0.1,
              F1("final", 2) + 0.3, rot=1.0)


PFN4 = PF.Plano("e38_mixton_hoy_b", F("final", 3) - 0.3, F("final", 4), z0=1.20, z1=1.06, c0=(0.55, 0.40), c1=(0.52, 0.50),
                par=(30, 7), tono=DORADO)
snd(F("final", 3) - 0.2, "amanecer", 0.45, dur=4.0)


@toma(F("final", 3) - 0.3, ("fundido", 0.8))
def FN4(lz, t):
    PFN4.fondo(lz, t)
    PF.brillo(lz, *PFN4.P(t, 0.30, 0.10)[:2], 420, color=(1.0, 0.82, 0.55), inten=0.24, t=t, sem=98)
    aves(lz, t, [(F("final", 3) - 0.5, 9.0, 0.16, 0.12, 50, 1, 0.3)])
    plantas(lz, PFN4, t, [("h18_ollin_viejo/02", 0.80, 1.02, 0.52, 1.25, False)], tono=DORADO)


PFN5 = PF.Plano("e41_casa_vieja_noche_a", F("final", 4) - 0.3, t1_("final") + 0.4, z0=1.80, z1=1.95, c0=(0.58, 0.66), c1=(0.58, 0.64),
                par=(12, 2), tono=INTERIOR)
_t_soy = T("final", "soy", 4)
snd(T("final", "piedra", 4) - 0.1, "brillo", 0.45)
snd(_t_soy - 0.05, "tambor", 0.55, tono=0.8)


@toma(F("final", 4) - 0.3, ("fundido", 0.8))
def FN5(lz, t):
    PFN5.fondo(lz, t)
    brillo_en(lz, PFN5, t, 0.40, 0.62, 70, inten=0.34, sem=96)
    desenfoca(lz, 1.6)
    quieto(lz, PFN5, t, "h18_ollin_viejo/03", 0.58, 0.95, 0.52, tono=INTERIOR)
    X, Y, h = PFN5.en(t, 0.58, 0.95 - 0.30, 0.02)
    PF.brillo(lz, X, Y, 70, color=(0.55, 1.0, 0.70), inten=0.35, t=t, sem=99)
    PF.rotulo(lz, "ME LLAMO OLLIN.", W * 0.28, H * 0.30, 64, t, T("final", "llamo", 4) - 0.1, t1_("final") + 0.3, rot=-1.5)
    PF.rotulo(lz, "SOY CAXCÁN.", W * 0.28, H * 0.44, 80, t, _t_soy - 0.05, t1_("final") + 0.3, rot=1.2, tinta=(120, 24, 14))


PCI1 = PF.Plano("e48_plaza_hoy_b", t0_("cierre") - 0.3, TOTAL, z0=1.04, z1=1.16, c0=(0.50, 0.50), c1=(0.40, 0.42), par=(28, 6),
                tono=DORADO)
snd(T("cierre", "compártela", 1) - 0.1, "pop", 0.45)
snd(T("cierre", "gusta", 1) - 0.1, "pop", 0.5, tono=1.2)


@toma(t0_("cierre") - 0.3, ("fundido", 1.0))
def CI1(lz, t):
    PCI1.fondo(lz, t)
    aves(lz, t, [(t0_("cierre"), 10.0, 0.20, 0.14, 48, 1, 0.5)])
    ta = t0_("cierre") - 0.3                     # la familia caxcán, translúcida, en la plaza de hoy (rigor del MASTER)
    for k, (pz, x, f, fl) in enumerate([("h15_gente/01", 0.16, 0.26, False), ("h15_gente/02", 0.26, 0.17, False),
                                         ("h18_ollin_viejo/03", 0.84, 0.30, True)]):
        quieto(lz, PCI1, t, pz, x, 0.94, f, flip=fl, tono=(1.05, 1.0, 0.95), fase=0.5 * k,
               op=0.55 * smooth(prog(t, ta + 0.3 * k, ta + 1.3 + 0.3 * k)) * (1 - smooth(prog(t, TOTAL - 3.0, TOTAL - 1.2))))
    PF.rotulo(lz, "COMPÁRTELA", W * 0.50, H * 0.78, 66, t, T("cierre", "compártela", 1) - 0.1, TOTAL - 2.5, rot=-1.2)
    PF.rotulo(lz, "DALE ME GUSTA", W * 0.50, H * 0.88, 50, t, T("cierre", "gusta", 1) - 0.1, TOTAL - 2.5, rot=1.0,
              tinta=(120, 24, 14))


# ================================================================== (las tomas se insertan aquí, por escena)


# ================================================================== composición
TOMAS.sort(key=lambda d: d["t0"])


def _cuadro(d, t):
    lz = np.zeros((H, W, 3), np.float32)
    d["dib"](lz, t)
    return lz


def render_mundo(t):
    i = 0
    for k, d in enumerate(TOMAS):
        if d["t0"] <= t:
            i = k
    if not TOMAS:
        return np.zeros((H, W, 3), np.float32)
    d = TOMAS[i]
    img = _cuadro(d, t)
    tipo, dur = d["ent"]
    if i > 0 and t < d["t0"] + dur and tipo != "corte":
        img = D.mezcla_tomas(_cuadro(TOMAS[i - 1], t), img, (t - d["t0"]) / dur, tipo)
    img = PF.acabado(img, t)
    franjas(img)
    img = img * smooth(prog(t, 0.0, 1.2)) * (1.0 - smooth(prog(t, TOTAL - 2.0, TOTAL - 0.1)))
    return np.clip(img, 0, 1).astype(np.float32)


class Mundo(Escena):
    def preparar(self):
        if self.idx == 0:
            for t, n, v, kw in SFX:
                self.ev(t, n, v, **kw)

    def render(self, lz, t):
        return render_mundo(t)


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
