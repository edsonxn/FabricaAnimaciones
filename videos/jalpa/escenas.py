# -*- coding: utf-8 -*-
"""«Jalpa» — PRUEBA de 1 min del estilo PEGATINA FLOW (nucleo/pegaflow.py): escenarios de Flow con cámara y parallax por profundidad,
personajes y utilería recortados de hojas de Flow (ciclos de caminar / correr / galopar en la misma imagen) animados como pegatinas.
11 tomas ancladas a palabras de la voz; ambiente continuo (aves, humo, fogatas, arena, destellos del río) y ≥ 3 planos de profundidad
(escenario con parallax + personajes + primer plano de plantas con capa > 1)."""
import math

import numpy as np

import pegaflow as PF
import docu as D
from escena_base import Escena, TL
from motor import W, H, clamp01, e_inout, lerp, prog, smooth

TOTAL = TL["total"]
_ESC = {e["id"]: e for e in TL["escenas"]}


def T(eid, pref, frase=None, n=0, fin=False):
    return PF.T(TL, eid, pref, frase, n, fin)


G, A, E, R = "gancho", "arena", "encomienda", "rebelion"
t_canon, t_arena0 = T(G, "cañón", 0), T(G, "arena", 0)
t_y, t_gente, t_echar, t_conq = T(G, "y", 1), T(G, "gente", 1), T(G, "echar", 1), T(G, "conquistador", 1)
t_esta, t_jalpa = T(G, "esta", 2), T(G, "jalpa", 2)
t_su, t_nah, t_quiere, t_sobre = T(A, "su", 0), T(A, "náhuatl", 0), T(A, "quiere", 0), T(A, "sobre", 0)
t_aqui, t_caxc, t_seno, t_peta = T(A, "aquí", 1), T(A, "caxcanes", 1), T(A, "señorío", 1), T(A, "petacatl", 1)
t_semb, t_maiz, t_frij, t_cala = T(A, "sembraban", 2), T(A, "maíz", 2), T(A, "frijol", 2), T(A, "calabaza", 2)
t0E = _ESC[E]["t0"]
t_mil, t_esp, t_enc, t_diego = T(E, "mil", 0), T(E, "españoles", 0), T(E, "encomienda", 0), T(E, "diego", 0)
t_los, t_trib, t_trab = T(E, "los", 1), T(E, "tributo", 1), T(E, "trabajar", 1)
t0R = _ESC[R]["t0"]
t_canon2, t_lev = T(R, "cañón", 0), T(R, "levantarse", 0)
t_y2, t_peta2, t_echaron = T(R, "y", 1), T(R, "petacatl", 1), T(R, "echaron", 1)
t_era, t_mixton = T(R, "era", 2), T(R, "mixtón", 2)

NOCHE = (0.60, 0.62, 0.92)       # luz de luna sobre las pegatinas
NUBLADO = (0.93, 0.95, 1.02)
AVES = [f"naturaleza/{i:02d}" for i in (12, 13, 14, 17, 15, 16)]     # ciclo de aleteo (alas arriba → planeo → abajo)

SFX = []


def snd(t, n, v=1.0, **kw):
    SFX.append((t, n, v, kw))


# ------------------------------------------------------------------ ayudantes de la toma
def alto(y, hz, k=0.64):
    """Altura relativa (al escenario) de una persona con los pies en y, con el horizonte en hz (perspectiva)."""
    return max(0.02, k * (y - hz))


# Hacia dónde MIRA cada pieza tal como la pintó Flow (+1 derecha, −1 izquierda). Las que se desplazan y están aquí se voltean
# SOLAS según su rumbo (x0 → x1): nunca caminan de espaldas a donde van (el usuario, 20-oct). Las de frente no están: su `flip` manda.
MIRA = {"caballo_galope": 1, "guerrero_corre": 1, "petacatl_camina": 1, "soldado_marcha": 1, "aliado_marcha": 1,
        "mula_camina": 1, "insurgente_camina": 1, "frances_marcha": 1, "mineros_hoja/01": 1, "insurgentes_hoja/03": 1,
        "gente_hoy/03": 1, "proano_hoja/04": -1, "mendoza_hoja/04": -1, "hidalgo_hoja/04": -1, "hidalgo_hoja/03": -1,
        "gente_hoy/05": -1}


def rumbo(pieza, x0, x1, flip):
    """`flip` que hace que la pieza mire hacia donde avanza (si se sabe hacia dónde mira y de verdad se desplaza)."""
    m = MIRA.get(pieza)
    if m is None or abs(x1 - x0) < 1e-6:
        return flip
    return (x1 - x0) * m < 0


def quieto(lz, pl, t, pieza, x, y, frac, flip=False, op=1.0, tono=None, capa=1.0, fase=0.0, t_in=None, rot=0.0):
    """Personaje u objeto quieto que respira; si `t_in`, se pega con rebote en ese instante."""
    if t_in is not None:
        if t < t_in:
            return
        u = PF.entra(t, t_in, 0.4)
    else:
        u = 1.0
    X, Y, h = pl.en(t, x, y, frac, capa)
    PF.actor(lz, pieza, X, Y, h * (0.6 + 0.4 * u), flip=flip, op=op * clamp01(u * 4), tono=tono,
             sy=PF.respira(t, fase=fase), rot=rot + (1 - u) * 8)


def paseo(lz, pl, t, pieza, ta, tb, x0, x1, y, frac, flip=False, tono=None, pasos=2.2, capa=1.0, op=1.0, y1=None):
    """Títere de papel que camina sin ciclo: avanza con saltitos y balanceo (pieza fija)."""
    flip = rumbo(pieza, x0, x1, flip)
    u = clamp01((t - ta) / max(tb - ta, 1e-3))
    x, yy = lerp(x0, x1, u), lerp(y, y1 if y1 is not None else y, u)
    X, Y, h = pl.en(t, x, yy, frac, capa)
    mov = ta < t < tb
    ph = (t - ta) * pasos * math.pi
    bote = abs(math.sin(ph)) if mov else 0.0
    rot = 3.0 * math.sin(ph) if mov else 0.0
    PF.actor(lz, pieza, X, Y - bote * 0.035 * h, h, flip=flip, tono=tono, rot=rot, op=op, sy=PF.respira(t))


def anda(lz, pl, t, ciclo, ta, tb, x0, x1, y, frac, paso=0.95, flip=False, tono=None, capa=1.0, op=1.0, pose=None,
         pose_frac=None, pose_flip=None, desde_antes=True):
    """Personaje con su CICLO de Flow (caminar/correr/galopar): el cuadro sale de la distancia recorrida (los pies no patinan).
    Antes de ta queda en x0 (cuadro 0 si `desde_antes`, si no, no está); después de tb, en x1 con `pose` (o el cuadro 0)."""
    if t < ta and not desde_antes:
        return
    flip = rumbo(ciclo, x0, x1, flip)
    u = clamp01((t - ta) / max(tb - ta, 1e-3))
    x = lerp(x0, x1, u)
    X, Y, h = pl.en(t, x, y, frac, capa)
    if t >= tb and pose is not None:
        PF.actor(lz, pose, X, Y, h * (pose_frac or 1.0), flip=flip if pose_flip is None else pose_flip, tono=tono, op=op,
                 sy=PF.respira(t))
        return
    n = PF.ciclo_n(ciclo)
    dist = abs(x - x0) * pl.ancho_mundo(t)
    i = PF.cuadro_ciclo(dist, paso * h, n) if ta < t < tb else 0
    PF.actor(lz, f"{ciclo}/ciclo_{i:02d}", X, Y, h, flip=flip, tono=tono, op=op)


def aves(lz, t, vuelos, tono=None):
    """vuelos: [(t_ini, dur, y0, y1, alto px, sentido, fase)] en pantalla; aleteo a 9 cuadros/s."""
    for t_i, dur, y0, y1, hpx, sent, fa in vuelos:
        u = (t - t_i) / dur
        if not 0 <= u <= 1:
            continue
        x = lerp(-0.08, 1.08, u) if sent > 0 else lerp(1.08, -0.08, u)
        y = lerp(y0, y1, u) + 0.012 * math.sin(t * 2.1 + fa)
        k = int((t * 9 + fa * 7)) % len(AVES)
        PF.actor(lz, AVES[k], x * W, y * H, hpx, flip=sent < 0, ancla=(0.5, 0.5), suelo=0, tono=tono)


def plantas(lz, pl, t, lista, tono=None):
    """Primer plano (capa > 1) en coordenadas de pantalla: [(pieza, x, y, frac de alto de pantalla, capa, flip)]; se mece."""
    for k, (pz, x, y, frac, capa, fl) in enumerate(lista):
        X, Y, h = pl.fg(t, x, y, frac, capa)
        PF.actor(lz, pz, X, Y, h, flip=fl, rot=1.6 * math.sin(1.3 * t + k * 1.9), suelo=0, tono=tono)


def rio(lz, pl, t, fondo):
    pts = []
    for x, y, f in PF.puntos_agua(fondo):
        X, Y, s = pl.P(t, x, y)
        if 0 <= X < W and 0 <= Y < H:
            pts.append((X, Y, f))
    PF.destellos(lz, t, pts, s=1.0)


FUEGOS = [(0.24, 0.18), (0.45, 0.34), (0.64, 0.25), (0.81, 0.20)]      # fogatas pintadas en noche_a
ANTORCHA = (0.445, 0.51)


def fuegos(lz, pl, t, extra=(), fuerza=1.0):
    for k, (x, y) in enumerate(list(FUEGOS) + [ANTORCHA]):
        X, Y, s = pl.P(t, x, y)
        PF.brillo(lz, X, Y, 150 * s * 1.4, inten=0.30 * fuerza, t=t, sem=k)
        PF.chispas(lz, t, X, Y, s=s * 1.3, n=6, sem=k)
    for k, (x, y, ti) in enumerate(extra):
        if t < ti:
            continue
        u = PF.entra(t, ti, 0.5)
        X, Y, h = pl.en(t, x, y, 0.05)
        PF.actor(lz, "utileria/16", X, Y, h * u, suelo=0)
        PF.brillo(lz, X, Y - 0.4 * h, 2.6 * h * u, inten=0.42, t=t, sem=10 + k)
        PF.chispas(lz, t, X, Y - 0.5 * h, s=h / 60, n=7, sem=10 + k)


# ------------------------------------------------------------------ tomas
TOMAS = []


def toma(t0, ent=("fundido", 0.5)):
    def deco(f):
        TOMAS.append(dict(t0=t0, ent=ent, dib=f))
        return f
    return deco


VUELO1 = [(0.2, 9.0, 0.16, 0.10, 74, 1, 0.0), (1.4, 10.0, 0.22, 0.17, 54, 1, 1.3), (3.0, 8.5, 0.12, 0.08, 64, 1, 2.1)]
FG_CANON = [("naturaleza/11", 0.05, 1.04, 0.34, 1.30, False), ("naturaleza/06", 0.95, 1.03, 0.26, 1.30, True),
            ("naturaleza/04", 0.82, 1.02, 0.12, 1.25, False)]

P1 = PF.Plano("canon", 0.0, t_y + 0.6, z0=1.02, z1=1.24, c0=(0.5, 0.40), c1=(0.47, 0.64), par=(34, 8))
snd(0.2, "viento", 0.5, dur=4.0)
snd(t_arena0 - 0.3, "viento", 0.7, dur=2.5)
snd(t_canon, "papel", 0.6)


@toma(0.0)
def s1(lz, t):
    P1.fondo(lz, t)
    PF.actor(lz, "naturaleza/00", (0.60 + 0.006 * t) * W, 0.10 * H, 130, ancla=(0.5, 0.5), suelo=0, op=0.85)
    aves(lz, t, VUELO1)
    rio(lz, P1, t, "canon")
    paseo(lz, P1, t, "caxcanes_hoja/01", 0.0, t_y + 0.5, 0.80, 0.50, 0.80, alto(0.80, 0.36, 0.42), flip=True, pasos=1.9)
    paseo(lz, P1, t, "caxcanes_hoja/02", 0.4, t_y + 0.9, 0.88, 0.58, 0.82, alto(0.82, 0.36, 0.42) * 0.72, flip=True, pasos=2.4)
    PF.arena_viento(lz, t, fuerza=smooth(prog(t, t_arena0 - 0.4, t_arena0 + 0.4)) * 0.9, y0=0.72, sem=1)
    plantas(lz, P1, t, FG_CANON)
    PF.rotulo(lz, "CAÑÓN DE JUCHIPILA", W * 0.25, H * 0.15, 46, t, t_canon, t_y - 0.5)


P2 = PF.Plano("noche", t_y - 0.25, t_esta + 0.5, z0=1.18, z1=1.05, c0=(0.58, 0.60), c1=(0.44, 0.60), par=(28, 6))
snd(t_y - 0.1, "fuego", 0.5, dur=4.0)
snd(t_y + 0.3, "galope", 0.8, dur=3.6)
snd(t_echar, "tambor", 0.7)
snd(t_conq, "tambor", 0.8, tono=0.8)


@toma(t_y - 0.25, ("latigo", 0.45))
def s2(lz, t):
    P2.fondo(lz, t)
    fuegos(lz, P2, t)
    ta, tb = t_y + 0.3, t_conq + 1.0          # entra con la frase: sin noche vacía al principio de la toma
    anda(lz, P2, t, "caballo_galope", ta, tb, 1.15, -0.30, 0.86, 0.34, paso=1.7, flip=True, tono=NOCHE, desde_antes=False)
    for k, (dy, dt) in enumerate([(0.0, 0.55), (0.06, 0.85), (-0.04, 1.15)]):
        y = 0.86 + dy
        anda(lz, P2, t, "guerrero_corre", ta + dt, tb + dt, 1.18, -0.15, y, alto(y, 0.38, 0.62), paso=1.35, flip=True,
             tono=NOCHE, desde_antes=False)
    quieto(lz, P2, t, "petacatl_hoja/03", 0.86, 0.99, 0.44, tono=NOCHE, t_in=t_gente, capa=1.08)


P3 = PF.Plano("canon", t_esta - 0.3, t_su + 0.5, z0=1.32, z1=1.18, c0=(0.50, 0.60), c1=(0.5, 0.56), par=(30, 8),
              tono=(1.04, 1.0, 0.94))
VUELO3 = [(t_esta - 1.0, 9.0, 0.14, 0.10, 80, -1, 0.4), (t_esta, 9.5, 0.20, 0.15, 58, -1, 1.7)]
snd(t_jalpa - 0.15, "golpe_grave", 0.7)
snd(t_jalpa + 0.35, "papel", 0.6)


@toma(t_esta - 0.3, ("destello", 0.5))
def s3(lz, t):
    P3.fondo(lz, t)
    rio(lz, P3, t, "canon")
    aves(lz, t, VUELO3)
    plantas(lz, P3, t, FG_CANON)
    PF.rotulo(lz, "JALPA", W * 0.5, H * 0.40, 190, t, t_jalpa - 0.15, rot=-1.5)
    PF.rotulo(lz, "ZACATECAS", W * 0.5, H * 0.58, 50, t, t_jalpa + 0.35, rot=1.0)


P4 = PF.Plano("canon", t_su - 0.3, t_aqui + 0.5, z0=1.75, z1=1.95, c0=(0.36, 0.84), c1=(0.44, 0.84), par=(36, 4))
snd(t_su - 0.2, "viento", 0.6, dur=3.5)
snd(t_nah, "papel", 0.6)
snd(t_quiere, "papel", 0.6)
snd(t_sobre, "pop", 0.8)


@toma(t_su - 0.3, ("desenfoque", 0.5))
def s4(lz, t):
    P4.fondo(lz, t)
    PF.arena_viento(lz, t, fuerza=0.9, y0=0.45, sem=4)
    plantas(lz, P4, t, [("naturaleza/05", 0.22, 1.03, 0.16, 1.35, False), ("naturaleza/06", 0.66, 1.04, 0.20, 1.4, False)])
    PF.rotulo(lz, "XALLI = ARENA", W * 0.29, H * 0.24, 62, t, t_nah, t_aqui - 0.4, rot=-3)
    PF.rotulo(lz, "PAN = SOBRE", W * 0.72, H * 0.24, 62, t, t_quiere, t_aqui - 0.4, rot=2.5)
    PF.rotulo(lz, "SOBRE LA ARENA", W * 0.5, H * 0.55, 120, t, t_sobre, t_aqui - 0.3, rot=-1)


P5 = PF.Plano("senorio", t_aqui - 0.3, t_semb + 0.5, z0=1.0, z1=1.1, c0=(0.48, 0.50), c1=(0.52, 0.55), par=(30, 7))
HZ5 = 0.30
HUMO5 = [(0.21, 0.25), (0.335, 0.19), (0.40, 0.21)]
snd(t_caxc, "papel", 0.6)
snd(t_seno - 0.6, "pasos", 0.5, dur=2.4)
snd(t_peta, "pop", 0.7)


@toma(t_aqui - 0.3, ("fundido", 0.55))
def s5(lz, t):
    P5.fondo(lz, t)
    for k, (x, y) in enumerate(HUMO5):
        X, Y, s = P5.P(t, x, y)
        PF.humo(lz, t, X, Y, s=s * 1.1, sem=k)
    rio(lz, P5, t, "senorio")
    quieto(lz, P5, t, "caxcanes_hoja/05", 0.30, 0.60, alto(0.60, HZ5) * 0.70, rot=2.2 * math.sin(t * 3.8))
    quieto(lz, P5, t, "caxcanes_hoja/04", 0.71, 0.64, alto(0.64, HZ5), flip=True, fase=1.0)
    quieto(lz, P5, t, "caxcanes_hoja/02", 0.55, 0.70, alto(0.70, HZ5) * 0.72, t_in=t_caxc + 0.2)
    paseo(lz, P5, t, "caxcanes_hoja/01", t_aqui, t_peta + 1.0, 0.64, 0.44, 0.66, alto(0.66, HZ5), flip=True)
    anda(lz, P5, t, "petacatl_camina", t_seno - 0.7, t_peta + 0.1, -0.06, 0.38, 0.88, alto(0.88, HZ5),
         pose="petacatl_hoja/01", pose_frac=1.0)
    PF.rotulo(lz, "CAXCANES", W * 0.5, H * 0.13, 64, t, t_caxc, t_semb - 0.4)
    X, Y, h = P5.en(t, 0.38, 0.88, alto(0.88, HZ5))
    PF.rotulo(lz, "PETACATL · señor de Jalpa", X + 0.05 * W, Y - h - 30, 44, t, t_peta, rot=-2)


P6 = PF.Plano("senorio", t_semb - 0.3, t0E + 0.6, z0=1.45, z1=1.55, c0=(0.50, 0.62), c1=(0.55, 0.62), par=(30, 6))
COSECHA = [("utileria/00", 0.30, 0.84, 0.12, t_maiz), ("utileria/01", 0.38, 0.85, 0.12, t_maiz + 0.25),
           ("utileria/05", 0.50, 0.86, 0.07, t_frij), ("utileria/04", 0.62, 0.86, 0.11, t_cala)]
for _p, _x, _y, _f, _t in COSECHA:
    snd(_t, "pop", 0.8)


@toma(t_semb - 0.3, ("desenfoque", 0.5))
def s6(lz, t):
    P6.fondo(lz, t)
    for k, (x, y) in enumerate(HUMO5):
        X, Y, s = P6.P(t, x, y)
        PF.humo(lz, t, X, Y, s=s * 1.1, sem=k)
    quieto(lz, P6, t, "caxcanes_hoja/00", 0.80, 0.92, alto(0.92, HZ5), flip=True, rot=4 * math.sin(t * 3.0))
    for pz, x, y, f, ti in COSECHA:
        quieto(lz, P6, t, pz, x, y, f, t_in=ti)
    plantas(lz, P6, t, [("naturaleza/07", 0.06, 1.04, 0.36, 1.25, False), ("naturaleza/11", 0.97, 1.04, 0.32, 1.25, True)])


P7 = PF.Plano("encomienda", t0E, t_los + 0.5, z0=1.0, z1=1.12, c0=(0.55, 0.50), c1=(0.47, 0.55), par=(28, 6), tono=NUBLADO)
HZ7 = 0.36
snd(t_mil, "golpe_grave", 0.8)
snd(t0E + 0.1, "pasos", 0.6, dur=3.5)
snd(t_enc, "sello", 0.7)
snd(t_diego, "papel", 0.6)


@toma(t0E, ("latigo", 0.45))
def s7(lz, t):
    P7.fondo(lz, t)
    paseo(lz, P7, t, "proano_hoja/04", t0E + 0.1, t_enc + 0.3, 1.02, 0.62, 0.84, alto(0.84, HZ7) * 1.25, pasos=1.6,
          tono=NUBLADO)                     # entra al empezar la toma: la casa no se queda vacía
    plantas(lz, P7, t, [("naturaleza/11", 0.97, 1.04, 0.30, 1.25, True)], tono=NUBLADO)
    PF.rotulo(lz, "1540", W * 0.78, H * 0.22, 150, t, t_mil, t_los - 0.4, rot=2)
    PF.rotulo(lz, "ENCOMIENDA", W * 0.30, H * 0.17, 70, t, t_enc, t_los - 0.4, rot=-2)
    if t >= t_enc:
        X, Y, h = P7.en(t, 0.62, 0.84, alto(0.84, HZ7) * 1.25)
        PF.actor(lz, "utileria/14", X - 0.30 * h, Y - 1.02 * h, 0.20 * h * (0.6 + 0.4 * PF.entra(t, t_enc)), ancla=(0.5, 0.5),
                 suelo=0, rot=-10)
    PF.rotulo(lz, "DIEGO HERNÁNDEZ DE PROAÑO · encomendero", W * 0.50, H * 0.88, 44, t, t_diego, rot=-1)


P8 = PF.Plano("encomienda", t_los - 0.3, t0R + 0.6, z0=1.25, z1=1.32, c0=(0.42, 0.62), c1=(0.47, 0.62), par=(28, 6), tono=NUBLADO)
SACOS = [(0.47, 0.585, t_trib), (0.52, 0.59, t_trib + 0.2), (0.43, 0.595, t_trib + 0.4)]
for _x, _y, _t in SACOS:
    snd(_t, "pop", 0.7)
snd(t_los, "pasos", 0.5, dur=3.0)
snd(t_trab, "papel", 0.5)


@toma(t_los - 0.3, ("desenfoque", 0.5))
def s8(lz, t):
    P8.fondo(lz, t)
    for x, y, ti in SACOS:
        quieto(lz, P8, t, "utileria/08", x, y, 0.07, t_in=ti, tono=NUBLADO)
    paseo(lz, P8, t, "caxcanes_hoja/00", t_los - 0.3, t_trab + 0.6, 0.66, 0.50, 0.78, alto(0.78, HZ7), flip=True, tono=NUBLADO)
    paseo(lz, P8, t, "caxcanes_hoja/01", t_los + 0.4, t_trab + 1.4, 0.70, 0.57, 0.82, alto(0.82, HZ7), flip=True, tono=NUBLADO)
    quieto(lz, P8, t, "proano_hoja/01", 0.75, 0.93, alto(0.93, HZ7) * 1.02, flip=True, tono=NUBLADO)
    quieto(lz, P8, t, "petacatl_hoja/04", 0.14, 0.97, alto(0.97, HZ7), tono=NUBLADO, t_in=t_trab, capa=1.05)
    PF.rotulo(lz, "TRIBUTO", W * 0.40, H * 0.16, 70, t, t_trib, rot=-2)


P9 = PF.Plano("noche", t0R, t_y2 + 0.5, z0=1.35, z1=1.08, c0=(0.30, 0.32), c1=(0.60, 0.40), par=(26, 6))
NUEVOS = [(0.10, 0.31, t_canon2), (0.33, 0.28, t_canon2 + 0.4), (0.55, 0.37, t_canon2 + 0.8), (0.71, 0.31, t_lev - 0.2),
          (0.92, 0.33, t_lev + 0.2)]
for _x, _y, _t in NUEVOS:
    snd(_t, "tambor", 0.6)
snd(t0R, "fuego", 0.5, dur=5.0)


@toma(t0R, ("negro", 0.6))
def s9(lz, t):
    P9.fondo(lz, t)
    fuegos(lz, P9, t, extra=NUEVOS, fuerza=0.6 + 0.4 * smooth(prog(t, t_canon2, t_lev + 0.5)))
    for k, (x, y, ti) in enumerate(NUEVOS):         # guerreros a contraluz junto a cada fogata que se enciende
        quieto(lz, P9, t, ("caxcanes_hoja/03", "caxcanes_hoja/04")[k % 2], x + 0.03, y + 0.006, 0.10,
               tono=(0.38, 0.30, 0.40), t_in=ti + 0.15, flip=k % 2 == 1, fase=k)
    aves(lz, t, [(t0R + 0.3, 7.0, 0.12, 0.06, 30, 1, 0.8)], tono=NOCHE)


P10 = PF.Plano("noche", t_y2 - 0.3, t_era + 0.5, z0=1.12, z1=1.2, c0=(0.55, 0.62), c1=(0.47, 0.62), par=(28, 6))
snd(t_peta2, "cuerno", 0.6)
snd(t_echaron - 0.1, "galope", 0.9, dur=2.4)
snd(t_peta2 + 0.3, "pasos", 0.6, dur=2.0)


@toma(t_y2 - 0.3, ("corte", 0.1))
def s10(lz, t):
    P10.fondo(lz, t)
    fuegos(lz, P10, t, extra=[(x, y, -1) for x, y, _ in NUEVOS])
    if t < t_echaron:
        quieto(lz, P10, t, "proano_hoja/03", 0.36, 0.78, alto(0.78, 0.38, 0.62), tono=NOCHE)
    anda(lz, P10, t, "caballo_galope", t_echaron, t_era + 0.6, 0.36, -0.35, 0.80, 0.30, paso=1.7, flip=True, tono=NOCHE,
         desde_antes=False)
    for k, (dy, dt) in enumerate([(0.0, 0.2), (0.07, 0.5), (-0.03, 0.8)]):
        y = 0.86 + dy
        anda(lz, P10, t, "guerrero_corre", t_peta2 + dt, t_era + 0.9 + dt, 1.20, 0.05, y, alto(y, 0.38, 0.62), paso=1.35,
             flip=True, tono=NOCHE, desde_antes=False)
    quieto(lz, P10, t, "petacatl_hoja/03", 0.84, 0.99, 0.46, tono=NOCHE, t_in=t_peta2 - 0.1, capa=1.08)


P11 = PF.Plano("penol", t_era - 0.3, _ESC["mixton"]["t0"] + 0.6, z0=1.0, z1=1.16, c0=(0.52, 0.48), c1=(0.53, 0.40), par=(30, 8))
HUMO11 = [(0.50, 0.26), (0.58, 0.245), (0.635, 0.27)]
snd(t_mixton, "golpe_grave", 0.8)
snd(t_era, "viento", 0.5, dur=5.0)


@toma(t_era - 0.3, ("fundido", 0.7))
def s11(lz, t):
    P11.fondo(lz, t)
    for k, (x, y) in enumerate(HUMO11):
        X, Y, s = P11.P(t, x, y)
        PF.humo(lz, t, X, Y, s=s * 1.6, color=(0.22, 0.17, 0.16), op=0.36, sem=k, alto=320)
    for k in range(3):
        a = t * 0.5 + k * 2.1
        X, Y, s = P11.P(t, 0.56 + 0.10 * math.cos(a), 0.16 + 0.04 * math.sin(a))
        PF.actor(lz, AVES[int(t * 8 + k * 3) % len(AVES)], X, Y, 30, flip=math.sin(a) > 0, ancla=(0.5, 0.5), suelo=0,
                 tono=(0.5, 0.4, 0.4))
    PF.rotulo(lz, "GUERRA DEL MIXTÓN", W * 0.5, H * 0.80, 74, t, t_mixton, rot=-1.5)
    PF.rotulo(lz, "1541 – 1542", W * 0.5, H * 0.90, 46, t, t_mixton + 0.4, rot=1)


# ================================================================== ESCENAS 5-10 (video completo, tramo 3)
def pega(lz, pieza, X, Y, hpx, t, t_in, t_out=None, rot=0.0, tono=None, flip=False, salida=0.35):
    """Pegatina en coordenadas de PANTALLA (centro en X, Y): se pega con rebote en t_in y se despega en t_out; flota un poco."""
    if t < t_in:
        return
    u = PF.entra(t, t_in, 0.45)
    o = 1.0 if t_out is None else 1.0 - smooth(prog(t, t_out, t_out + salida))
    if o <= 0.01:
        return
    PF.actor(lz, pieza, X, Y + 4 * math.sin(1.3 * t + t_in), hpx * (0.6 + 0.4 * u), rot=rot + (1 - u) * 10 + 0.8 * math.sin(1.1 * t),
             op=o * clamp01(u * 4), ancla=(0.5, 0.5), suelo=0, tono=tono, flip=flip)


def retrato(lz, t, quien, X, Y, hpx, t_in, t_out=None, rot=-3.0, tono=None):
    """Retrato REAL (Commons) en su marco, pegado como calcomanía (piezas/retratos, de _retratos.py)."""
    pega(lz, f"retratos/{quien}", X, Y, hpx, t, t_in, t_out, rot=rot, tono=tono)


def columna(lz, pl, t, ciclo, ta, tb, x0, x1, filas, hz, k=0.64, paso=0.95, flip=False, tono=None):
    """Tropa con su ciclo: filas = [(y, retraso, dx)] (de lejos a cerca); dx corre el punto de salida y de llegada."""
    for y, r, dx in sorted(filas):
        anda(lz, pl, t, ciclo, ta + r, tb + r, x0 + dx, x1 + dx, y, alto(y, hz, k), paso=paso, flip=flip, tono=tono)


def baila(lz, pl, t, x, y, frac, fase=0.0, flip=False, tono=None):
    """Tastoán con el ciclo de danza por TIEMPO (9 cuadros/s): baila en su sitio."""
    X, Y, h = pl.en(t, x, y, frac)
    i = int(t * 9 + fase * 8) % PF.ciclo_n("tastoan_danza")
    PF.actor(lz, f"tastoan_danza/ciclo_{i:02d}", X, Y, h, flip=flip, tono=tono)


def desliza(lz, pl, t, pieza, ta, tb, x0, x1, y, frac, flip=False, tono=None):
    """Pieza que se desliza sin saltitos (bicicleta, vagoneta)."""
    flip = rumbo(pieza, x0, x1, flip)
    u = clamp01((t - ta) / max(tb - ta, 1e-3))
    X, Y, h = pl.en(t, lerp(x0, x1, u), y, frac)
    PF.actor(lz, pieza, X, Y + 1.5 * math.sin(t * 17), h, flip=flip, tono=tono)


def humos(lz, pl, t, pts, **kw):
    for k, (x, y) in enumerate(pts):
        X, Y, s = pl.P(t, x, y)
        PF.humo(lz, t, X, Y, s=s * 1.2, sem=k, **kw)


def lumbres(lz, pl, t, pts, inten=0.32, chispas=True):
    for k, (x, y) in enumerate(pts):
        X, Y, s = pl.P(t, x, y)
        PF.brillo(lz, X, Y, 140 * s * 1.4, inten=inten, t=t, sem=20 + k)
        if chispas:
            PF.chispas(lz, t, X, Y, s=s * 1.2, n=5, sem=20 + k)


FG_SECO = [("naturaleza/11", 0.04, 1.04, 0.32, 1.30, False), ("naturaleza/06", 0.96, 1.04, 0.26, 1.30, True)]
GUERRA = (0.22, 0.17, 0.16)

# ------------------------------------------------------------------ 5 · mixton (55,2-88,8)
M = "mixton"
t0M = _ESC[M]["t0"]
m_cax, m_penoles, m_guiados, m_tena = T(M, "caxcanes", 0), T(M, "peñoles", 0), T(M, "guiados", 0), T(M, "tenamaxtli", 0)
m_mil, m_pedro, m_un, m_cayo, m_murio = T(M, "mil", 1), T(M, "pedro", 1), T(M, "un", 1, 1), T(M, "cayó", 1), T(M, "murió", 1)
m_entonces, m_antonio, m_cuat, m_decenas = T(M, "entonces", 2), T(M, "antonio", 2), T(M, "cuatrocientos", 2), T(M, "decenas", 2)
m_penol, m_resis, m_y, m_primer, m_entro = T(M, "peñol", 3), T(M, "resistencia", 3), T(M, "y", 3), T(M, "primer", 3), T(M, "entró", 3)
m_del, m_cron = T(M, "del", 4), T(M, "crónicas", 4)
HZM = 0.42
TOPE = [(0.24, 0.205, 0.0), (0.33, 0.20, 0.3), (0.45, 0.20, 0.6), (0.52, 0.195, 0.9)]     # caxcanes en lo alto del peñol

PM1 = PF.Plano("penoles_dia", t0M, m_guiados, z0=1.0, z1=1.12, c0=(0.5, 0.5), c1=(0.42, 0.42), par=(30, 8))
snd(t0M + 0.1, "viento", 0.6, dur=4.0)
snd(m_cax, "tambor", 0.5)
snd(m_penoles, "papel", 0.6)


@toma(t0M, ("fundido", 0.6))
def m1(lz, t):
    PM1.fondo(lz, t)
    humos(lz, PM1, t, [(0.26, 0.19), (0.50, 0.18)], op=0.25, alto=200)
    for k, (x, y, dt) in enumerate(TOPE):
        quieto(lz, PM1, t, ("caxcanes_hoja/03", "caxcanes_hoja/04", "tenamaxtli_hoja/02")[k % 3], x, y + 0.01, 0.075,
               t_in=m_cax + dt, flip=k % 2 == 1, fase=k)
    paseo(lz, PM1, t, "caxcanes_hoja/04", t0M - 0.3, m_guiados, 0.84, 0.62, 0.88, alto(0.88, HZM), flip=True, pasos=1.9)
    paseo(lz, PM1, t, "caxcanes_hoja/03", t0M + 0.2, m_guiados + 0.3, 0.97, 0.74, 0.94, alto(0.94, HZM), flip=True, pasos=2.1)
    aves(lz, t, [(t0M - 0.5, 9.0, 0.30, 0.22, 60, 1, 0.3), (t0M + 1.0, 9.5, 0.36, 0.30, 44, 1, 1.1)])
    plantas(lz, PM1, t, FG_SECO)
    PF.rotulo(lz, "LOS PEÑOLES", W * 0.74, H * 0.16, 64, t, m_penoles, m_guiados - 0.4, rot=2)


PM2 = PF.Plano("penoles_dia", m_guiados - 0.3, m_mil, z0=1.45, z1=1.55, c0=(0.62, 0.70), c1=(0.58, 0.70), par=(34, 6))
snd(m_guiados, "cuerno", 0.6)
snd(m_tena, "papel", 0.6)


@toma(m_guiados - 0.3, ("desenfoque", 0.5))
def m2(lz, t):
    PM2.fondo(lz, t)
    quieto(lz, PM2, t, "caxcanes_hoja/03", 0.44, 0.80, alto(0.80, HZM), fase=0.5)
    quieto(lz, PM2, t, "caxcanes_hoja/04", 0.80, 0.82, alto(0.82, HZM), flip=True, fase=1.4)
    quieto(lz, PM2, t, "tenamaxtli_hoja/01", 0.60, 0.99, alto(0.99, HZM) * 1.05, t_in=m_guiados - 0.25)
    X, Y, h = PM2.en(t, 0.60, 0.99, alto(0.99, HZM) * 1.05)
    PF.rotulo(lz, "TENAMAXTLI · caudillo caxcán", W * 0.27, H * 0.16, 50, t, m_tena, rot=-2)
    plantas(lz, PM2, t, [("naturaleza/05", 0.10, 1.04, 0.18, 1.35, False)])


HZP = 0.45
PM3 = PF.Plano("penol", m_mil - 0.2, m_un, z0=1.15, z1=1.28, c0=(0.40, 0.66), c1=(0.48, 0.62), par=(30, 8))
snd(m_mil, "tambor", 0.7)
snd(m_mil + 0.2, "pasos", 0.6, dur=4.2)
snd(m_pedro, "papel", 0.6)


@toma(m_mil - 0.2, ("latigo", 0.45))
def m3(lz, t):
    PM3.fondo(lz, t)
    humos(lz, PM3, t, HUMO11, color=GUERRA, op=0.34, alto=300)
    columna(lz, PM3, t, "soldado_marcha", m_mil - 0.4, m_un + 0.6, -0.12, 0.40, [(0.78, 0.0, 0.0), (0.78, 0.0, -0.10),
            (0.83, 0.3, -0.04), (0.83, 0.3, -0.15), (0.88, 0.6, -0.08)], HZP)
    paseo(lz, PM3, t, "alvarado_hoja/00", m_mil - 0.3, m_un + 0.4, 0.06, 0.34, 0.94, alto(0.94, HZP) * 1.05, pasos=1.8)
    PF.rotulo(lz, "1541", W * 0.20, H * 0.16, 120, t, m_mil, m_un - 0.3, rot=-2)
    retrato(lz, t, "alvarado", W * 0.80, H * 0.38, H * 0.44, m_pedro - 0.1, m_un - 0.3)
    PF.rotulo(lz, "PEDRO DE ALVARADO", W * 0.80, H * 0.67, 44, t, m_pedro + 0.2, m_un - 0.3, rot=1.5)


PM4 = PF.Plano("penol", m_un - 0.3, m_entonces, z0=1.6, z1=1.75, c0=(0.62, 0.70), c1=(0.60, 0.72), par=(30, 6))
snd(m_un - 0.2, "galope", 0.8, dur=1.6)
snd(m_cayo + 0.15, "golpe_grave", 0.9)
snd(m_murio, "campana", 0.4, tono=0.6)


@toma(m_un - 0.3, ("desenfoque", 0.45))
def m4(lz, t):
    PM4.fondo(lz, t)
    tc = m_cayo
    if t < tc + 1.3:                                 # a caballo por la ladera… y el caballo se le viene encima
        u = smooth(prog(t, tc, tc + 0.6))
        x = lerp(0.50, 0.60, clamp01((t - (m_un - 0.3)) / (tc - m_un + 0.3)))
        X, Y, h = PM4.en(t, x + 0.03 * u, 0.76 + 0.07 * u, alto(0.76, HZP) * 1.15)
        bote = 0 if u > 0 else abs(math.sin(t * 7)) * 0.03 * h
        PF.actor(lz, "alvarado_hoja/04", X, Y - bote, h, rot=-78 * u, op=1 - smooth(prog(t, tc + 0.9, tc + 1.3)),
                 suelo=0.3 * (1 - u))
    if t > tc + 0.3:
        X, Y, s = PM4.P(t, 0.64, 0.84)
        PF.humo(lz, t - tc, X, Y, s=s * 1.6, color=(0.80, 0.66, 0.50), op=0.45 * (1 - smooth(prog(t, tc + 1.5, tc + 2.5))),
                sem=7, alto=120)
    quieto(lz, PM4, t, "alvarado_hoja/03", 0.62, 0.86, alto(0.86, HZP) * 0.55, t_in=tc + 0.6)
    PF.rotulo(lz, "† 1541", W * 0.76, H * 0.22, 90, t, m_murio, rot=2)


HZC = 0.42
FUEGO_C = [(0.725, 0.665), (0.87, 0.745)]
PM5 = PF.Plano("campamento", m_entonces - 0.2, m_cuat, z0=1.05, z1=1.15, c0=(0.52, 0.56), c1=(0.58, 0.56), par=(30, 7))
snd(m_entonces, "cuerno", 0.7)
snd(m_entonces + 0.2, "pasos", 0.5, dur=2.5)
snd(m_antonio, "papel", 0.6)


@toma(m_entonces - 0.2, ("latigo", 0.45))
def m5(lz, t):
    PM5.fondo(lz, t)
    humos(lz, PM5, t, [(0.725, 0.63), (0.87, 0.72)], op=0.25, alto=220)
    lumbres(lz, PM5, t, FUEGO_C, inten=0.22)
    for k, (x, y) in enumerate([(0.56, 0.66), (0.64, 0.665), (0.95, 0.70)]):
        quieto(lz, PM5, t, "soldado_marcha/ciclo_00", x, y, alto(y, HZC), flip=k == 1, fase=k)
    quieto(lz, PM5, t, "aliado_marcha/ciclo_00", 0.48, 0.69, alto(0.69, HZC), fase=2.0)
    paseo(lz, PM5, t, "mendoza_hoja/04", m_entonces - 0.3, m_antonio + 0.4, 0.04, 0.32, 0.88, alto(0.88, HZC) * 1.2, pasos=1.5)
    plantas(lz, PM5, t, [("naturaleza/07", 0.97, 1.04, 0.30, 1.25, True)])
    retrato(lz, t, "mendoza", W * 0.74, H * 0.38, H * 0.46, m_antonio - 0.1, m_cuat - 0.3, rot=2.5)
    PF.rotulo(lz, "ANTONIO DE MENDOZA · virrey", W * 0.74, H * 0.69, 44, t, m_antonio + 0.3, m_cuat - 0.3, rot=-1.5)


PM6 = PF.Plano("campamento", m_cuat - 0.3, m_penol, z0=1.35, z1=1.25, c0=(0.30, 0.74), c1=(0.40, 0.72), par=(34, 6))
snd(m_cuat - 0.2, "pasos", 0.8, dur=4.4)
snd(m_cuat, "tambor", 0.7)
snd(m_decenas, "tambor", 0.8, tono=0.8)


@toma(m_cuat - 0.3, ("desenfoque", 0.45))
def m6(lz, t):
    PM6.fondo(lz, t)
    ta, tb = m_cuat - 0.6, m_penol + 0.6
    ali = [(0.66, 0.05 * j, 0.12 - 0.06 * j) for j in range(10)] + [(0.70, 0.3, 0.09 - 0.06 * j) for j in range(10)]
    columna(lz, PM6, t, "aliado_marcha", ta, tb, 0.05, 0.40, ali, HZC)          # detrás: muchos y chicos
    esp = [(0.86, 0.0, -0.12 * j) for j in range(4)] + [(0.93, 0.25, 0.05 - 0.12 * j) for j in range(4)]
    columna(lz, PM6, t, "soldado_marcha", ta, tb, 0.05, 0.40, esp, HZC)
    PF.rotulo(lz, "450 ESPAÑOLES", W * 0.30, H * 0.14, 62, t, m_cuat, rot=-2)
    PF.rotulo(lz, "DECENAS DE MILES DE ALIADOS", W * 0.64, H * 0.27, 52, t, m_decenas, rot=1.5)


PM7 = PF.Plano("penoles_dia", m_penol - 0.2, m_y, z0=1.0, z1=1.08, c0=(0.56, 0.50), c1=(0.60, 0.50), par=(28, 6),
               tono=(0.86, 0.78, 0.76))
snd(m_penol, "fuego", 0.6, dur=3.0)
snd(T(M, "peñol", 3, 1), "fuego", 0.5, dur=1.5)
snd(m_resis + 0.6, "golpe_grave", 0.8)
FUEGOS7 = [(0.24, 0.19, m_penol), (0.40, 0.19, m_penol + 0.25), (0.53, 0.18, m_penol + 0.5), (0.80, 0.20, m_penol + 0.7)]


@toma(m_penol - 0.2, ("fundido", 0.5))
def m7(lz, t):
    PM7.fondo(lz, t)
    for k, (x, y, ti) in enumerate(FUEGOS7):
        if t > ti:
            X, Y, s = PM7.P(t, x, y)
            PF.humo(lz, t, X, Y, s=s * 1.6 * smooth(prog(t, ti, ti + 1.0)), color=GUERRA, op=0.36, sem=k, alto=240)
            PF.brillo(lz, X, Y, 90 * s, inten=0.35, t=t, sem=30 + k)
    quieto(lz, PM7, t, "tenamaxtli_hoja/04", 0.33, 0.92, alto(0.92, HZM) * 0.95, t_in=m_resis - 0.2, tono=(0.86, 0.78, 0.76))
    plantas(lz, PM7, t, [("naturaleza/06", 0.95, 1.04, 0.26, 1.30, True)], tono=(0.86, 0.78, 0.76))


PM8 = PF.Plano("senorio", m_y - 0.2, m_del, z0=1.25, z1=1.15, c0=(0.62, 0.62), c1=(0.56, 0.60), par=(30, 7), tono=(0.90, 0.88, 0.92))
snd(m_y, "pasos", 0.7, dur=3.6)
snd(m_primer, "sello", 0.7)
snd(m_entro - 0.3, "galope", 0.5, dur=1.4)


@toma(m_y - 0.2, ("desenfoque", 0.45))
def m8(lz, t):
    PM8.fondo(lz, t)
    tn = (0.90, 0.88, 0.92)
    humos(lz, PM8, t, HUMO5, color=(0.40, 0.36, 0.34), op=0.34, alto=300)
    for k, (x, y) in enumerate([(0.43, 0.62), (0.56, 0.60)]):
        quieto(lz, PM8, t, "caxcanes_hoja/0%d" % (4 + k), x, y, alto(y, HZ5) * (0.9, 0.7)[k], tono=tn, fase=k, flip=k == 0)
    columna(lz, PM8, t, "soldado_marcha", m_y - 0.3, m_del + 0.4, 1.10, 0.66, [(0.74, 0.0, 0.0), (0.74, 0.2, 0.09),
            (0.79, 0.4, 0.05)], HZ5, flip=True, tono=tn)
    paseo(lz, PM8, t, "mendoza_hoja/04", m_y - 0.3, m_entro + 0.5, 1.02, 0.56, 0.90, alto(0.90, HZ5) * 1.2, flip=True, tono=tn,
          pasos=1.5)
    PF.rotulo(lz, "1 DE ENERO DE 1542", W * 0.30, H * 0.16, 62, t, m_primer, rot=-2)


PM9 = PF.Plano("penol", m_del - 0.3, _ESC["santiago"]["t0"] + 0.6, z0=1.3, z1=1.4, c0=(0.50, 0.64), c1=(0.50, 0.60),
               par=(30, 6), tono=(0.55, 0.52, 0.72))
snd(m_del, "viento", 0.6, dur=3.5)
snd(m_cron, "papel", 0.6)
snd(m_cron + 0.6, "papel", 0.6)


@toma(m_del - 0.3, ("negro", 0.5))
def m9(lz, t):
    PM9.fondo(lz, t)
    tn = (0.55, 0.52, 0.72)
    sep = smooth(prog(t, m_cron - 0.2, m_cron + 1.2))          # las crónicas no coinciden: dos versiones que se separan
    for k, s in enumerate((-1, 1)):
        quieto(lz, PM9, t, "petacatl_hoja/00", 0.50 + s * 0.13 * sep, 0.97, alto(0.97, HZP) * 0.95, tono=tn,
               op=1.0 - 0.45 * sep, fase=k, flip=s > 0 and sep > 0.5)
        if t > m_cron:
            X, Y, h = PM9.en(t, 0.50 + s * 0.24 * sep, 0.80, 0.10)
            PF.actor(lz, "utileria/14", X, Y, h * PF.entra(t, m_cron + 0.6 * k), ancla=(0.5, 0.5), suelo=0, rot=s * 8)
    PF.rotulo(lz, "¿PETACATL?", W * 0.5, H * 0.15, 80, t, m_del + 0.3, rot=-1.5)


# ------------------------------------------------------------------ 6 · santiago (88,8-108,0)
S = "santiago"
t0S = _ESC[S]["t0"]
s_guerra, s_fundar = T(S, "guerra", 0), T(S, "fundar", 0)
s_le, s_santiago, s_santo, s_durante, s_xalpa = T(S, "le", 1), T(S, "santiago", 1), T(S, "santo", 1), T(S, "durante", 1), \
    T(S, "xalpa", 1)
s_santiago2 = T(S, "santiago", 1, 1)
s_cax, s_mezcl, s_y, s_arena = T(S, "caxcanes", 2), T(S, "mezclaron", 2), T(S, "y", 2), T(S, "arena", 2)
HZS = 0.35
PS1 = PF.Plano("iglesia_obra", t0S, s_le, z0=1.0, z1=1.1, c0=(0.50, 0.50), c1=(0.56, 0.52), par=(28, 7))
snd(t0S + 0.2, "viento", 0.4, dur=3.0)
snd(s_guerra + 0.3, "golpe_suave", 0.6)
snd(s_fundar, "golpe_suave", 0.5)
snd(s_guerra, "papel", 0.5)


@toma(t0S, ("fundido", 0.6))
def sa1(lz, t):
    PS1.fondo(lz, t)
    quieto(lz, PS1, t, "colonia_hoja/00", 0.40, 0.62, alto(0.62, HZS), fase=0.4)
    quieto(lz, PS1, t, "colonia_hoja/02", 0.82, 0.86, alto(0.86, HZS), flip=True, rot=4 * math.sin(t * 3.0))
    paseo(lz, PS1, t, "colonia_hoja/01", t0S, s_le + 0.5, 0.12, 0.52, 0.78, alto(0.78, HZS), pasos=1.8)
    aves(lz, t, [(t0S - 1.0, 9.0, 0.12, 0.08, 56, 1, 0.2)])
    plantas(lz, PS1, t, [("naturaleza/05", 0.05, 1.04, 0.20, 1.35, False)])
    PF.rotulo(lz, "1542", W * 0.20, H * 0.17, 110, t, s_guerra, s_le - 0.3, rot=-2)


PS2 = PF.Plano("iglesia_obra", s_le - 0.3, s_durante, z0=1.55, z1=1.65, c0=(0.60, 0.50), c1=(0.62, 0.47), par=(30, 6))
snd(s_santiago, "campana", 0.6)
snd(s_santo, "papel", 0.6)


@toma(s_le - 0.3, ("desenfoque", 0.45))
def sa2(lz, t):
    PS2.fondo(lz, t)
    quieto(lz, PS2, t, "colonia_hoja/01", 0.50, 0.63, alto(0.63, HZS), fase=0.8, rot=2 * math.sin(t * 2.2))
    quieto(lz, PS2, t, "colonia_hoja/00", 0.72, 0.66, alto(0.66, HZS), flip=True, fase=0.2)
    pega(lz, "gente_hoy/05", W * 0.13, H * 0.42, H * 0.44, t, s_santiago - 0.1, s_durante - 0.3, rot=-4)
    PF.rotulo(lz, "SANTIAGO · el santo de los conquistadores", W * 0.42, H * 0.80, 44, t, s_santo, s_durante - 0.3, rot=-1)


HZX = 0.42
PS3 = PF.Plano("santiago_xalpa", s_durante - 0.3, s_cax, z0=1.15, z1=1.05, c0=(0.62, 0.58), c1=(0.55, 0.56), par=(28, 7))
snd(s_santiago2, "campana", 0.7, tono=1.2)
snd(s_santiago2 + 0.3, "papel", 0.6)


@toma(s_durante - 0.3, ("latigo", 0.45))
def sa3(lz, t):
    PS3.fondo(lz, t)
    paseo(lz, PS3, t, "colonia_hoja/00", s_durante - 0.4, s_cax + 0.3, 0.55, 0.74, 0.70, alto(0.70, HZX), pasos=1.6)
    paseo(lz, PS3, t, "colonia_hoja/04", s_durante - 0.4, s_cax + 0.3, 0.98, 0.70, 0.86, alto(0.86, HZX), flip=True, pasos=1.9)
    quieto(lz, PS3, t, "colonia_hoja/05", 0.66, 0.74, alto(0.74, HZX), fase=1.2)
    aves(lz, t, [(s_durante - 1.0, 8.0, 0.14, 0.10, 52, -1, 0.6)])
    PF.rotulo(lz, "SANTIAGO DE XALPA", W * 0.42, H * 0.20, 76, t, s_santiago2, rot=-2)


PS4 = PF.Plano("santiago_xalpa", s_cax - 0.3, s_y + 2.0, z0=1.55, z1=1.0, c0=(0.50, 0.76), c1=(0.50, 0.52), par=(32, 8))
snd(s_cax, "pasos", 0.5, dur=2.5)
snd(s_mezcl, "pop", 0.7)
snd(s_arena - 0.2, "viento", 0.7, dur=3.0)


@toma(s_cax - 0.3, ("desenfoque", 0.45))
def sa4(lz, t):
    PS4.fondo(lz, t)
    PF.arena_viento(lz, t, fuerza=smooth(prog(t, s_arena - 0.4, s_arena + 0.4)) * 0.8, y0=0.70, sem=6)
    quieto(lz, PS4, t, "colonia_hoja/04", 0.36, 0.80, alto(0.80, HZX), fase=0.3)
    paseo(lz, PS4, t, "caxcanes_hoja/01", s_cax - 0.3, s_mezcl + 0.3, 0.18, 0.40, 0.90, alto(0.90, HZX), pasos=1.8)
    paseo(lz, PS4, t, "colonia_hoja/02", s_cax - 0.3, s_mezcl + 0.3, 0.86, 0.62, 0.90, alto(0.90, HZX), flip=True, pasos=1.8)
    quieto(lz, PS4, t, "colonia_hoja/03", 0.51, 0.93, alto(0.93, HZX), t_in=s_mezcl)
    quieto(lz, PS4, t, "caxcanes_hoja/02", 0.74, 0.78, alto(0.78, HZX) * 0.72, t_in=s_mezcl + 0.4, flip=True)
    plantas(lz, PS4, t, [("naturaleza/06", 0.03, 1.04, 0.24, 1.3, False)])
    PF.rotulo(lz, "MESTIZAJE", W * 0.5, H * 0.14, 76, t, s_mezcl, s_y + 1.0, rot=-1.5)


# ------------------------------------------------------------------ 7 · mineral (108,0-122,4)
X_ = "mineral"
t0X = _ESC[X_]["t0"]
x_debajo, x_plata = T(X_, "debajo", 0), T(X_, "plata", 0)
x_las, x_leonera, x_monroy, x_jalpa = T(X_, "las", 1), T(X_, "leonera", 1), T(X_, "monroy", 1), T(X_, "jalpa", 1)
x_por, x_mulas = T(X_, "por", 2), T(X_, "mulas", 2)
HZN = 0.45
PX1 = PF.Plano("mina_dia", t0X, x_las, z0=1.1, z1=1.6, c0=(0.40, 0.50), c1=(0.20, 0.56), par=(30, 6))
snd(t0X + 0.6, "clink", 0.5, tono=0.8)
snd(t0X + 1.6, "clink", 0.5, tono=0.7)
snd(x_plata, "bling", 0.8)


@toma(t0X, ("fundido", 0.5))
def x1(lz, t):
    PX1.fondo(lz, t)
    quieto(lz, PX1, t, "mineros_hoja/00", 0.22, 0.64, alto(0.64, HZN) * 1.2, rot=5 * math.sin(t * 4.0))
    quieto(lz, PX1, t, "mineros_hoja/05", 0.30, 0.66, alto(0.66, HZN) * 0.85, flip=True, fase=0.6)
    if t > x_plata - 0.1:
        u = PF.entra(t, x_plata - 0.1, 0.5)
        PF.brillo(lz, W * 0.5, H * 0.50, H * 0.40 * u, color=(1.0, 0.95, 0.80), inten=0.45, t=t, sem=40)
    pega(lz, "utileria_2/01", W * 0.5, H * 0.50, H * 0.30, t, x_plata - 0.1, rot=-6)
    PF.rotulo(lz, "PLATA", W * 0.5, H * 0.80, 96, t, x_plata + 0.1, rot=-1.5)


PX2 = PF.Plano("mina_dia", x_las - 0.3, x_por, z0=1.0, z1=1.08, c0=(0.50, 0.50), c1=(0.56, 0.52), par=(30, 7))
snd(x_las, "clink", 0.4, tono=0.9)
snd(x_leonera, "papel", 0.6)
snd(x_monroy, "papel", 0.6)
snd(x_jalpa, "sello", 0.8)


@toma(x_las - 0.3, ("latigo", 0.45))
def x2(lz, t):
    PX2.fondo(lz, t)
    humos(lz, PX2, t, [(0.60, 0.52)], op=0.18, alto=160)
    quieto(lz, PX2, t, "mineros_hoja/00", 0.13, 0.66, alto(0.66, HZN) * 1.2, rot=5 * math.sin(t * 4.0))
    desliza(lz, PX2, t, "utileria_2/07", x_las - 0.3, x_monroy + 0.8, 0.12, 0.30, 0.66, 0.07)
    paseo(lz, PX2, t, "mineros_hoja/01", x_las - 0.3, x_jalpa, 0.30, 0.62, 0.80, alto(0.80, HZN) * 1.2, pasos=1.6)
    quieto(lz, PX2, t, "mineros_hoja/02", 0.80, 0.84, alto(0.84, HZN) * 1.2, flip=True, fase=0.7)
    quieto(lz, PX2, t, "mineros_hoja/05", 0.70, 0.90, alto(0.90, HZN) * 0.85, fase=1.4)
    plantas(lz, PX2, t, [("naturaleza/07", 0.97, 1.04, 0.30, 1.25, True)])
    PF.rotulo(lz, "LA LEONERA", W * 0.24, H * 0.14, 58, t, x_leonera, x_jalpa - 0.3, rot=-2)
    PF.rotulo(lz, "MONROY", W * 0.62, H * 0.14, 58, t, x_monroy, x_jalpa - 0.3, rot=2)
    PF.rotulo(lz, "JALPA MINERAL", W * 0.5, H * 0.42, 120, t, x_jalpa, rot=-1.5)


PX3 = PF.Plano("mina_dia", x_por - 0.3, _ESC["hidalgo"]["t0"] + 0.6, z0=1.45, z1=1.55, c0=(0.42, 0.70), c1=(0.48, 0.70),
               par=(34, 6))
snd(x_por, "pasos", 0.6, dur=4.0)
snd(x_mulas, "galope", 0.3, dur=2.0, tono=0.6)


@toma(x_por - 0.3, ("desenfoque", 0.45))
def x3(lz, t):
    PX3.fondo(lz, t)
    ta, tb = x_por - 0.8, x_por + 5.4
    anda(lz, PX3, t, "mula_camina", ta, tb, 0.70, 0.46, 0.70, alto(0.70, HZN) * 0.92, paso=1.25, flip=True)   # la lejana, primero
    for k in range(3):
        y = 0.86 + 0.02 * (k % 2)
        anda(lz, PX3, t, "mula_camina", ta + 0.25 * k, tb + 0.25 * k, 0.24 - 0.13 * k, 0.56 - 0.13 * k, y, alto(y, HZN) * 0.92,
             paso=1.25)
    paseo(lz, PX3, t, "mineros_hoja/04", ta, tb, 0.34, 0.66, 0.90, alto(0.90, HZN) * 1.15, pasos=1.7)
    plantas(lz, PX3, t, [("naturaleza/05", 0.93, 1.04, 0.22, 1.35, True)])


# ------------------------------------------------------------------ 8 · hidalgo (122,4-148,8)
Hd = "hidalgo"
t0H = _ESC[Hd]["t0"]
h_enero, h_miguel, h_acababa, h_puente = T(Hd, "enero", 0), T(Hd, "miguel", 0), T(Hd, "acababa", 0), T(Hd, "puente", 0)
h_subio, h_y, h_dieciocho, h_jalpa = T(Hd, "subió", 1), T(Hd, "y", 1), T(Hd, "dieciocho", 1), T(Hd, "jalpa", 1)
h_segun, h_hablo, h_balcon, h_tienda = T(Hd, "según", 2), T(Hd, "habló", 2), T(Hd, "balcón", 2), T(Hd, "tienda", 2)
h_durmio, h_siguio, h_norte, h_dos, h_capt = T(Hd, "durmió", 3), T(Hd, "siguió", 3), T(Hd, "norte", 3), T(Hd, "dos", 3), \
    T(Hd, "capturaron", 3)
HZH = 0.42
TARDE = (1.03, 0.95, 0.88)
PH1 = PF.Plano("camino_tarde", t0H, h_acababa, z0=1.05, z1=1.15, c0=(0.50, 0.56), c1=(0.55, 0.60), par=(30, 7), tono=TARDE)
snd(t0H + 0.2, "pasos", 0.6, dur=4.0)
snd(h_enero, "papel", 0.6)
snd(h_miguel, "papel", 0.7)


@toma(t0H, ("fundido", 0.6))
def h1(lz, t):
    PH1.fondo(lz, t)
    columna(lz, PH1, t, "insurgente_camina", t0H - 0.5, h_acababa + 0.5, 0.00, 0.30,
            [(0.70, 0.0, 0.0), (0.70, 0.2, -0.08), (0.73, 0.4, -0.04), (0.73, 0.5, -0.13)], HZH, tono=TARDE)
    paseo(lz, PH1, t, "hidalgo_hoja/04", t0H - 0.3, h_acababa + 0.3, 0.22, 0.48, 0.82, alto(0.82, HZH) * 1.2, pasos=1.4,
          tono=TARDE)
    plantas(lz, PH1, t, FG_SECO, tono=TARDE)
    PF.rotulo(lz, "ENERO DE 1811", W * 0.24, H * 0.15, 66, t, h_enero, h_acababa - 0.3, rot=-2)
    retrato(lz, t, "hidalgo", W * 0.79, H * 0.38, H * 0.46, h_miguel - 0.1, h_acababa - 0.2)
    PF.rotulo(lz, "MIGUEL HIDALGO", W * 0.79, H * 0.69, 48, t, h_miguel + 0.2, h_acababa - 0.2, rot=1.5)


PH2 = PF.Plano("camino_tarde", h_acababa - 0.3, h_subio, z0=1.6, z1=1.7, c0=(0.40, 0.76), c1=(0.45, 0.76), par=(34, 6),
               tono=TARDE)
snd(h_acababa, "tambor", 0.4, tono=0.7)
snd(h_puente, "golpe_grave", 0.7)


@toma(h_acababa - 0.3, ("desenfoque", 0.45))
def h2(lz, t):
    PH2.fondo(lz, t)
    ta, tb = h_acababa - 0.4, h_subio + 0.6
    paseo(lz, PH2, t, "insurgentes_hoja/02", ta, tb, 0.16, 0.30, 0.84, alto(0.84, HZH), pasos=1.5, tono=TARDE)
    paseo(lz, PH2, t, "insurgentes_hoja/05", ta, tb, 0.06, 0.20, 0.86, alto(0.86, HZH) * 0.75, pasos=1.9, tono=TARDE)
    paseo(lz, PH2, t, "insurgentes_hoja/01", ta, tb, 0.30, 0.44, 0.93, alto(0.93, HZH), pasos=1.2, tono=TARDE)
    PF.rotulo(lz, "PUENTE DE CALDERÓN", W * 0.64, H * 0.16, 62, t, h_puente, rot=-2)
    PF.rotulo(lz, "derrota · 17 de enero de 1811", W * 0.64, H * 0.27, 40, t, h_puente + 0.4, rot=1)


TARDE2 = (1.0, 0.86, 0.80)
PH3 = PF.Plano("camino_tarde", h_subio - 0.3, h_dieciocho - 0.2, z0=1.25, z1=1.30, c0=(0.62, 0.66), c1=(0.58, 0.62), par=(30, 7),
               tono=TARDE2)
snd(h_subio, "pasos", 0.7, dur=3.0)


@toma(h_subio - 0.3, ("latigo", 0.45))
def h3(lz, t):
    PH3.fondo(lz, t)
    ta, tb = h_subio - 0.8, h_dieciocho + 0.5
    filas = [(0.80, 0.0, 0.0), (0.80, 0.2, -0.09), (0.80, 0.4, -0.18), (0.88, 0.1, 0.04), (0.88, 0.3, -0.05),
             (0.88, 0.5, -0.14), (0.96, 0.25, -0.02), (0.96, 0.45, -0.11)]
    columna(lz, PH3, t, "insurgente_camina", ta, tb, 0.40, 0.72, filas, HZH, tono=TARDE2)
    paseo(lz, PH3, t, "insurgentes_hoja/03", ta, tb, 0.50, 0.80, 0.74, alto(0.74, HZH) * 1.15, pasos=1.6, tono=TARDE2)


HZT = 0.44
DUSK = (0.95, 0.84, 0.82)
LUZ_T = [(0.31, 0.75), (0.55, 0.72)]
FAROL_T = [(0.265, 0.36), (0.41, 0.36)]
PH4 = PF.Plano("mina_tarde", h_dieciocho - 0.3, h_segun, z0=1.05, z1=1.15, c0=(0.45, 0.56), c1=(0.40, 0.53), par=(30, 7))
snd(h_dieciocho - 0.2, "fuego", 0.5, dur=3.0)
snd(h_dieciocho, "papel", 0.6)
snd(h_jalpa - 0.6, "galope", 0.4, dur=1.4, tono=0.7)


@toma(h_dieciocho - 0.3, ("fundido", 0.5))
def h4(lz, t):
    PH4.fondo(lz, t)
    lumbres(lz, PH4, t, LUZ_T, inten=0.30)
    lumbres(lz, PH4, t, FAROL_T, inten=0.22, chispas=False)
    quieto(lz, PH4, t, "mineros_hoja/03", 0.64, 0.80, alto(0.80, HZT), flip=True, tono=DUSK)
    quieto(lz, PH4, t, "mineros_hoja/05", 0.72, 0.82, alto(0.82, HZT) * 0.8, flip=True, tono=DUSK, fase=1.0)
    paseo(lz, PH4, t, "hidalgo_hoja/04", h_dieciocho - 0.4, h_jalpa + 0.6, 0.02, 0.36, 0.88, alto(0.88, HZT) * 1.2, pasos=1.4,
          tono=DUSK)
    plantas(lz, PH4, t, [("naturaleza/07", 0.03, 1.04, 0.30, 1.25, False)], tono=DUSK)
    PF.rotulo(lz, "18 DE ENERO DE 1811 · JALPA", W * 0.5, H * 0.12, 56, t, h_dieciocho, rot=-1.5)


PH5 = PF.Plano("mina_tarde", h_segun - 0.3, h_durmio, z0=1.62, z1=1.78, c0=(0.36, 0.53), c1=(0.36, 0.50), par=(30, 6))
snd(h_segun, "papel", 0.5)
snd(h_hablo, "eco", 0.4)
snd(h_tienda, "papel", 0.6)


@toma(h_segun - 0.3, ("desenfoque", 0.45))
def h5(lz, t):
    PH5.fondo(lz, t)
    lumbres(lz, PH5, t, FAROL_T, inten=0.26, chispas=False)
    lumbres(lz, PH5, t, LUZ_T, inten=0.26)
    quieto(lz, PH5, t, "hidalgo_hoja/01", 0.36, 0.465, 0.21, tono=DUSK, t_in=h_segun + 0.3,
           rot=1.5 * math.sin(t * 2.4) if t > h_hablo else 0.0)
    for k, (pz, x, y, f) in enumerate([("insurgentes_hoja/02", 0.20, 0.84, 1.0), ("mineros_hoja/01", 0.30, 0.86, 1.05),
                                       ("insurgentes_hoja/04", 0.47, 0.85, 1.0), ("mineros_hoja/03", 0.58, 0.87, 1.0)]):
        quieto(lz, PH5, t, pz, x, y, alto(y, HZT) * f, tono=DUSK, fase=k * 0.7, flip=x > 0.4)
    PF.rotulo(lz, "según los cronistas del cañón", W * 0.24, H * 0.10, 40, t, h_segun, h_balcon, rot=-1.5)
    PF.rotulo(lz, "TIENDA DE RAYA · MINA LA LEONERA", W * 0.70, H * 0.12, 46, t, h_tienda, rot=1.5)


AMANECER = (0.92, 0.88, 1.0)
PH6 = PF.Plano("camino_tarde", h_durmio - 0.3, h_dos, z0=1.3, z1=1.4, c0=(0.55, 0.64), c1=(0.60, 0.62), par=(30, 7),
               tono=AMANECER)
snd(h_durmio, "amanecer", 0.5, dur=2.5)
snd(h_siguio, "pasos", 0.6, dur=1.6)
snd(h_norte, "papel", 0.6)


@toma(h_durmio - 0.3, ("negro", 0.6))
def h6(lz, t):
    PH6.fondo(lz, t)
    if t < h_siguio:
        quieto(lz, PH6, t, "hidalgo_hoja/02", 0.42, 0.88, alto(0.88, HZH) * 1.15, tono=AMANECER)
    else:
        paseo(lz, PH6, t, "hidalgo_hoja/03", h_siguio, h_dos + 0.8, 0.42, 0.62, 0.88, alto(0.88, HZH) * 1.15, pasos=1.4,
              tono=AMANECER)
    aves(lz, t, [(h_durmio - 0.5, 7.0, 0.16, 0.10, 46, 1, 0.9)])
    plantas(lz, PH6, t, FG_SECO, tono=AMANECER)
    PF.rotulo(lz, "RUMBO AL NORTE", W * 0.74, H * 0.18, 62, t, h_norte, rot=2)


PH7 = PF.Plano("camino_tarde", h_dos - 0.3, _ESC["franceses"]["t0"] + 0.6, z0=1.0, z1=1.05, c0=(0.5, 0.5), c1=(0.5, 0.48),
               par=(20, 4), tono=(0.42, 0.40, 0.52))
snd(h_dos, "papel", 0.5)
snd(h_capt, "golpe_grave", 0.9)


@toma(h_dos - 0.3, ("desenfoque", 0.45))
def h7(lz, t):
    PH7.fondo(lz, t)
    gris = 1.0 - 0.35 * smooth(prog(t, h_capt - 0.2, h_capt + 0.6))
    retrato(lz, t, "hidalgo", W * 0.5, H * 0.43, H * 0.62, h_dos - 0.2, rot=-2,
            tono=(gris, gris, gris * 1.05) if gris < 0.999 else None)
    PF.rotulo(lz, "CAPTURADO · MARZO DE 1811", W * 0.5, H * 0.86, 56, t, h_capt, rot=-1)


# ------------------------------------------------------------------ 9 · franceses (148,8-168,0)
F = "franceses"
t0F = _ESC[F]["t0"]
f_mil, f_aleman, f_piedra, f_leonera, f_plata = T(F, "mil", 0), T(F, "alemán", 0), T(F, "piedra", 0), T(F, "leonera", 0), \
    T(F, "plata", 0)
f_la, f_jalpaita, f_libros = T(F, "la", 1), T(F, "jalpaíta", 1), T(F, "libros", 1)
f_seis, f_unos, f_franc, f_plaza = T(F, "seis", 2), T(F, "unos", 2), T(F, "franceses", 2), T(F, "plaza", 2)
LAMPARA = [(0.83, 0.47)]
PF1 = PF.Plano("gabinete", t0F, f_piedra - 0.2, z0=1.0, z1=1.1, c0=(0.50, 0.50), c1=(0.56, 0.55), par=(24, 6))
snd(t0F + 0.2, "tick", 0.3)
snd(f_mil, "papel", 0.6)
snd(f_aleman, "papel", 0.5)


@toma(t0F, ("fundido", 0.6))
def f1(lz, t):
    PF1.fondo(lz, t)
    lumbres(lz, PF1, t, LAMPARA, inten=0.25, chispas=False)
    quieto(lz, PF1, t, "siglo19_hoja/00", 0.30, 0.98, 0.56)
    PF.rotulo(lz, "1858", W * 0.20, H * 0.16, 120, t, f_mil, rot=-2)
    PF.rotulo(lz, "mineralogista alemán", W * 0.26, H * 0.30, 42, t, f_aleman, rot=1.5)


PF2 = PF.Plano("gabinete", f_piedra - 0.3, f_la, z0=1.8, z1=1.9, c0=(0.66, 0.78), c1=(0.68, 0.78), par=(24, 4))
snd(f_piedra, "pop", 0.8)
snd(f_plata, "bling", 0.6)
snd(f_leonera, "papel", 0.5)


@toma(f_piedra - 0.3, ("desenfoque", 0.45))
def f2(lz, t):
    PF2.fondo(lz, t)
    lumbres(lz, PF2, t, LAMPARA, inten=0.25, chispas=False)
    pega(lz, "utileria_2/00", W * 0.48, H * 0.56, H * 0.40, t, f_piedra, rot=-3)
    if t > f_piedra + 0.3:
        a = (t - f_piedra) * 1.3
        pega(lz, "utileria_2/04", W * (0.50 + 0.10 * math.cos(a)), H * (0.50 + 0.07 * math.sin(a)), H * 0.30, t, f_piedra + 0.3,
             rot=-20)
    PF.rotulo(lz, "de La Leonera", W * 0.22, H * 0.82, 46, t, f_leonera, rot=-2)
    PF.rotulo(lz, "PLATA + COBRE", W * 0.5, H * 0.13, 66, t, f_plata, rot=1.5)


PF3 = PF.Plano("gabinete", f_la - 0.3, f_seis, z0=1.25, z1=1.2, c0=(0.45, 0.62), c1=(0.50, 0.60), par=(24, 6))
snd(f_jalpaita, "sello", 0.8)
snd(f_libros - 0.6, "escribir", 0.5, dur=1.5)


@toma(f_la - 0.3, ("latigo", 0.45))
def f3(lz, t):
    PF3.fondo(lz, t)
    lumbres(lz, PF3, t, LAMPARA, inten=0.25, chispas=False)
    quieto(lz, PF3, t, "siglo19_hoja/01", 0.40, 0.98, 0.56, rot=0.8 * math.sin(t * 5))
    PF.rotulo(lz, "JALPAÍTA", W * 0.66, H * 0.30, 130, t, f_jalpaita, rot=-2)
    PF.rotulo(lz, "en los libros de mineralogía", W * 0.66, H * 0.48, 44, t, f_libros, rot=1)


HZF = 0.43
PF4 = PF.Plano("plaza_1864", f_seis - 0.3, _ESC["hoy"]["t0"] + 0.6, z0=1.12, z1=1.0, c0=(0.55, 0.62), c1=(0.50, 0.55), par=(30, 7),
               tono=NUBLADO)
snd(f_seis, "tambor", 0.7)
snd(f_seis + 0.6, "pasos", 0.8, dur=5.0)
snd(f_unos, "tambor", 0.8, tono=0.8)
snd(f_plaza, "golpe_grave", 0.6)


@toma(f_seis - 0.3, ("fundido", 0.5))
def f4(lz, t):
    PF4.fondo(lz, t)
    quieto(lz, PF4, t, "siglo19_hoja/05", 0.10, 0.72, alto(0.72, HZF), tono=NUBLADO)
    quieto(lz, PF4, t, "siglo19_hoja/04", 0.80, 0.72, alto(0.72, HZF), tono=NUBLADO, fase=0.5)
    quieto(lz, PF4, t, "siglo19_hoja/03", 0.88, 0.75, alto(0.75, HZF), flip=True, tono=NUBLADO, fase=1.1)
    ta, tb = f_seis + 0.4, f_plaza + 0.8
    filas = [(0.82, 0.10 * j, -0.09 * j) for j in range(5)] + [(0.90, 0.2 + 0.1 * j, -0.04 - 0.09 * j) for j in range(5)]
    columna(lz, PF4, t, "frances_marcha", ta, tb, 0.10, 0.52, filas, HZF, tono=NUBLADO)
    quieto(lz, PF4, t, "siglo19_hoja/02", 0.62, 0.96, alto(0.96, HZF), tono=NUBLADO, t_in=f_unos - 0.3)
    PF.rotulo(lz, "1864", W * 0.20, H * 0.16, 110, t, f_seis, rot=-2)
    PF.rotulo(lz, "UNOS 300 SOLDADOS FRANCESES", W * 0.58, H * 0.14, 54, t, f_unos, rot=1.5)


# ------------------------------------------------------------------ 10 · hoy (168,0-203,4)
Y_ = "hoy"
t0Y = _ESC[Y_]["t0"]
y_hoy, y_veinti, y_carretera = T(Y_, "hoy", 0), T(Y_, "veinticinco", 0), T(Y_, "carretera", 0)
y_sus, y_senor, y_san = T(Y_, "sus", 1), T(Y_, "señor", 1), T(Y_, "antonio", 1) - 0.25
y_julio, y_tasto, y_mascaras, y_guerra = T(Y_, "julio", 2), T(Y_, "tastoanes", 2), T(Y_, "máscaras", 2), T(Y_, "guerra", 2)
y_el, y_guayabos, y_hoy2, y_agave = T(Y_, "el", 3), T(Y_, "guayabos", 3), T(Y_, "hoy", 3), T(Y_, "agave", 3)
y_y, y_arena = T(Y_, "y", 4), T(Y_, "arena", 4)
y_esto, y_bitac, y_sigue, y_que = T(Y_, "esto", 5), T(Y_, "bitácora", 5), T(Y_, "sigue", 5), T(Y_, "qué", 5)
HZJ = 0.50
PY1 = PF.Plano("jalpa_hoy", t0Y, y_carretera, z0=1.0, z1=1.12, c0=(0.50, 0.50), c1=(0.45, 0.52), par=(28, 7))
snd(y_hoy, "campana", 0.6)
snd(y_hoy + 0.8, "campana", 0.4, tono=0.8)
snd(y_veinti, "papel", 0.6)


@toma(t0Y, ("destello", 0.5))
def y1(lz, t):
    PY1.fondo(lz, t)
    aves(lz, t, [(t0Y - 0.5, 8.0, 0.16, 0.10, 54, 1, 0.4), (t0Y + 1.5, 9.0, 0.22, 0.17, 40, -1, 1.5)])
    quieto(lz, PY1, t, "gente_hoy/02", 0.58, 0.80, alto(0.80, HZJ) * 1.1, fase=0.3)
    quieto(lz, PY1, t, "gente_hoy/00", 0.32, 0.86, alto(0.86, HZJ) * 1.1, fase=1.1)
    paseo(lz, PY1, t, "gente_hoy/01", t0Y, y_carretera, 0.92, 0.70, 0.92, alto(0.92, HZJ) * 1.1, flip=True, pasos=1.7)
    desliza(lz, PY1, t, "gente_hoy/03", y_veinti - 1.0, y_carretera + 0.2, -0.10, 1.10, 0.96, alto(0.96, HZJ) * 1.05)
    PF.rotulo(lz, "HOY", W * 0.5, H * 0.13, 100, t, y_hoy, y_veinti - 0.3, rot=-2)
    PF.rotulo(lz, "MUNICIPIO DE ~25 000 HABITANTES", W * 0.5, H * 0.13, 52, t, y_veinti, rot=1)


PY2 = PF.Plano("canon_hoy", y_carretera - 0.3, y_sus, z0=1.35, z1=1.45, c0=(0.72, 0.55), c1=(0.76, 0.55), par=(30, 6))
snd(y_carretera, "whoosh", 0.6)
snd(y_carretera + 0.2, "papel", 0.6)


@toma(y_carretera - 0.3, ("latigo", 0.45))
def y2(lz, t):
    PY2.fondo(lz, t)
    rio(lz, PY2, t, "canon_hoy")
    aves(lz, t, [(y_carretera - 1.0, 6.0, 0.18, 0.12, 48, 1, 0.7)])
    PF.rotulo(lz, "CARRETERA 54", W * 0.40, H * 0.20, 72, t, y_carretera, rot=-2)


PY3 = PF.Plano("jalpa_hoy", y_sus - 0.3, y_julio, z0=1.45, z1=1.6, c0=(0.62, 0.62), c1=(0.60, 0.50), par=(30, 6))
snd(y_senor, "campana", 0.7)
snd(y_san, "campana", 0.5, tono=1.2)


@toma(y_sus - 0.3, ("desenfoque", 0.45))
def y3(lz, t):
    PY3.fondo(lz, t)
    paseo(lz, PY3, t, "gente_hoy/04", y_sus - 0.3, y_julio, 0.52, 0.64, 0.84, alto(0.84, HZJ) * 1.1, pasos=1.3)
    quieto(lz, PY3, t, "gente_hoy/01", 0.80, 0.86, alto(0.86, HZJ) * 1.1, flip=True, fase=0.4)
    PF.rotulo(lz, "SEÑOR DE JALPA", W * 0.28, H * 0.22, 60, t, y_senor, rot=-2)
    PF.rotulo(lz, "SAN ANTONIO", W * 0.74, H * 0.32, 56, t, y_san, rot=2)


HZY = 0.45
PY4 = PF.Plano("fiesta_calle", y_julio - 0.3, y_mascaras - 0.2, z0=1.05, z1=1.15, c0=(0.50, 0.60), c1=(0.50, 0.63), par=(30, 7))
snd(y_julio, "tambor", 0.6)
snd(y_tasto, "tambor", 0.7, tono=1.2)
snd(y_tasto + 0.6, "tambor", 0.6, tono=0.9)


@toma(y_julio - 0.3, ("latigo", 0.45))
def y4(lz, t):
    PY4.fondo(lz, t)
    for k, (x, y) in enumerate([(0.50, 0.74), (0.32, 0.82), (0.68, 0.84)]):
        baila(lz, PY4, t, x, y, alto(y, HZY) * 1.7, fase=k * 0.37, flip=k == 2)
    paseo(lz, PY4, t, "gente_hoy/05", y_julio - 0.4, y_mascaras, 0.92, 0.80, 0.93, alto(0.93, HZY) * 1.2, flip=True, pasos=1.6)
    quieto(lz, PY4, t, "gente_hoy/00", 0.12, 0.76, alto(0.76, HZY) * 1.05, fase=0.7)
    PF.rotulo(lz, "JULIO", W * 0.20, H * 0.24, 54, t, y_julio, rot=-2)
    PF.rotulo(lz, "TASTOANES", W * 0.5, H * 0.13, 90, t, y_tasto, rot=1.5)


PY5 = PF.Plano("fiesta_calle", y_mascaras - 0.2, y_el, z0=1.6, z1=1.7, c0=(0.42, 0.72), c1=(0.48, 0.72), par=(32, 6))
snd(y_mascaras, "pop", 0.8)
snd(y_guerra, "golpe_grave", 0.6)


@toma(y_mascaras - 0.2, ("desenfoque", 0.45))
def y5(lz, t):
    PY5.fondo(lz, t)
    baila(lz, PY5, t, 0.36, 0.97, alto(0.97, HZY) * 1.05, fase=0.2)
    baila(lz, PY5, t, 0.47, 0.86, alto(0.86, HZY), fase=0.6, flip=True)     # a 0.56 la máscara le tapaba el cuerpo
    pega(lz, "utileria_2/17", W * 0.74, H * 0.42, H * 0.46, t, y_mascaras, rot=5)
    PF.rotulo(lz, "MÁSCARAS DE MADERA", W * 0.74, H * 0.80, 50, t, y_mascaras + 0.3, rot=-1.5)
    PF.rotulo(lz, "DE 1541 A HOY", W * 0.30, H * 0.16, 70, t, y_guerra, rot=-2)


PY6 = PF.Plano("canon_hoy", y_el - 0.3, y_y, z0=1.25, z1=1.35, c0=(0.40, 0.70), c1=(0.45, 0.70), par=(32, 6))
snd(y_guayabos, "pop", 0.7)
snd(y_agave, "pop", 0.8, tono=0.8)
snd(y_el, "viento", 0.4, dur=3.0)


@toma(y_el - 0.3, ("fundido", 0.5))
def y6(lz, t):
    PY6.fondo(lz, t)
    rio(lz, PY6, t, "canon_hoy")
    pega(lz, "utileria_2/15", W * 0.28, H * 0.40, H * 0.30, t, y_guayabos, y_hoy2 - 0.1, rot=-4)
    pega(lz, "utileria_2/14", W * 0.46, H * 0.30, H * 0.20, t, y_guayabos + 0.3, y_hoy2 - 0.1, rot=5)
    pega(lz, "utileria_2/16", W * 0.66, H * 0.40, H * 0.42, t, y_hoy2, rot=3)
    PF.rotulo(lz, "AGAVE", W * 0.66, H * 0.74, 70, t, y_agave, rot=-2)


PY7 = PF.Plano("canon_hoy", y_y - 0.3, y_esto, z0=1.0, z1=1.08, c0=(0.45, 0.55), c1=(0.50, 0.58), par=(30, 7))
snd(y_arena - 0.2, "viento", 0.7, dur=3.0)


@toma(y_y - 0.3, ("desenfoque", 0.5))
def y7(lz, t):
    PY7.fondo(lz, t)
    rio(lz, PY7, t, "canon_hoy")
    PF.arena_viento(lz, t, fuerza=0.4 + 0.5 * smooth(prog(t, y_arena - 0.4, y_arena + 0.4)), y0=0.70, sem=8)
    aves(lz, t, [(y_y - 1.0, 9.0, 0.14, 0.10, 64, 1, 0.1), (y_y, 9.5, 0.20, 0.16, 46, 1, 1.4)])
    PF.rotulo(lz, "XALLI = ARENA", W * 0.30, H * 0.20, 62, t, y_arena, rot=-2)


PY8 = PF.Plano("canon_hoy", y_esto - 0.3, TOTAL, z0=1.1, z1=1.5, c0=(0.62, 0.55), c1=(0.74, 0.52), par=(30, 7))
snd(y_bitac, "sello", 0.7)
snd(y_que, "papel", 0.6)


@toma(y_esto - 0.3, ("fundido", 0.6))
def y8(lz, t):
    PY8.fondo(lz, t)
    rio(lz, PY8, t, "canon_hoy")
    aves(lz, t, [(y_esto - 0.5, 8.0, 0.16, 0.10, 56, 1, 0.5)])
    PF.rotulo(lz, "BITÁCORA PERDIDA", W * 0.5, H * 0.38, 110, t, y_bitac, rot=-2)
    PF.rotulo(lz, "¿QUÉ PUEBLO SIGUE?", W * 0.5, H * 0.58, 64, t, y_que, rot=1.5)


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
    d = TOMAS[i]
    img = _cuadro(d, t)
    tipo, dur = d["ent"]
    if i > 0 and t < d["t0"] + dur and tipo != "corte":
        img = D.mezcla_tomas(_cuadro(TOMAS[i - 1], t), img, (t - d["t0"]) / dur, tipo)
    img = PF.acabado(img, t)
    img = img * smooth(prog(t, 0.0, 0.6)) * (1.0 - smooth(prog(t, TOTAL - 1.4, TOTAL - 0.1)))
    return np.clip(img, 0, 1).astype(np.float32)


class Mundo(Escena):
    def preparar(self):
        if self.idx == 0:
            for t, n, v, kw in SFX:
                self.ev(t, n, v, **kw)

    def render(self, lz, t):
        return render_mundo(t)


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
