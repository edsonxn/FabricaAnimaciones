# -*- coding: utf-8 -*-
"""¿Qué pasaría si el Sol se apagara? — PLANO SECUENCIA estilo Kurzgesagt (sin cortes).

Las 6 "escenas" del guion solo marcan narración y música: TODAS usan la clase Mundo, que dibuja un único
mundo continuo en función del tiempo global t. Cada cosa se transforma en la siguiente:
  1. Espacio: el Sol se apaga y su última luz (frente de onda) viaja 8 min 20 s hacia la Tierra.
  2. La onda alcanza la Tierra: se oscurece y sale disparada por la tangente (la órbita sigue sin ella).
  3. INMERSIÓN: la cámara cae hacia la Tierra; su borde curvo se aplana y se vuelve el horizonte del
     paisaje (el paisaje se dibuja doblado sobre el planeta con curvatura kappa = 1/radio en pantalla).
  4. Superficie: el cielo se apaga, frío, termómetro, las hojas caen, el mar se congela desde arriba.
  5. La cámara baja por el corte del mar, bajo el hielo (una manta), hasta la fumarola con microbios.
  6. El brillo de la fumarola crece hasta llenar la pantalla y se encoge convertido en el Sol.
  7. Vida del Sol; nueva inmersión por la línea del amanecer; el pajarito da las gracias.
"""
import math
import types
from contextlib import contextmanager

import numpy as np

from escena_base import *  # noqa: F401,F403
from escena_base import TL, Escena, F
import plano as P
from plano import mezcla, aclarar
from motor import (W, H, Lienzo, componer, mat_t, mat_s, prog, clamp01, lerp, e_in, e_out, e_inout, e_back, smooth,
                   circulo, elipse, rect_red, remuestrear, corazon)


# ======================================================================== anclas (tiempo global)
_ESC = {e["id"]: e for e in TL["escenas"]}


def T(eid, texto, **kw):
    return Escena.w(types.SimpleNamespace(fr=_ESC[eid]["frases"], id=eid), texto, **kw)


def INI(eid, i=0):
    return _ESC[eid]["frases"][i]["t0"]


TOTAL = TL["total"]
A = types.SimpleNamespace(
    apaga=T("intro", "apaga"), tierra=T("intro", "Tierra"),
    luz0=INI("luz"), ocho=T("luz", "ocho"), nada=T("luz", "nada"), ultima=T("luz", "última"),
    grav=T("luz", "gravedad"),
    alcanza=T("deriva", "alcanza"), disp=T("deriva", "disparada"), treinta=T("deriva", "treinta"),
    aqui=T("deriva", "aquí"), cielo=T("deriva", "cielo"), negro=T("deriva", "negro"),
    semana=T("frio", "semana"), cero1=T("frio", "cero", frase=0, fin=True),
    ano=T("frio", "año"), cero2=T("frio", "cero", frase=1, fin=True),
    foto=T("frio", "fotosíntesis"), oceanos=T("frio", "océanos"), arriba=T("frio", "arriba", fin=True),
    pero=T("vida", "Pero"), manta=T("vida", "manta"), liquida=T("vida", "líquida"),
    fondo=T("vida", "fondo"), hidro=T("vida", "hidrotermales"), microbios=T("vida", "microbios"),
    vivos=T("vida", "vivos"), vivos_f=T("vida", "vivos", fin=True),
    suerte=T("cierre", "suerte"), sol=T("cierre", "Sol"), cinco=T("cierre", "cinco"),
    manana=T("cierre", "mañana"), salga=T("cierre", "salga"), gracias=T("cierre", "gracias"),
    fin=_ESC["cierre"]["frases"][-1]["t1"],
)
# fases del plano secuencia
LLEGA = A.alcanza + 0.1                        # la última luz (y el fin de la gravedad) pasa por la Tierra
D1 = (A.aqui - 0.95, A.cielo + 0.2)           # inmersión 1: espacio -> superficie de noche
BAJA1 = (A.pero - 0.3, A.pero + 2.1)          # la cámara baja bajo el hielo
BAJA2 = (A.fondo - 0.35, A.fondo + 2.3)       # ... hasta el fondo del mar
B0 = A.vivos_f + 0.2                           # brillo de la fumarola...
BM = B0 + 0.9                                  # ... llena la pantalla -> es el Sol
B1 = BM + 1.5                                  # el Sol ya se ve entero
D2 = (A.manana - 0.6, A.salga + 0.3)           # inmersión 2: espacio -> amanecer
C_GLOW = (255, 206, 120)

# ======================================================================== espacio
SOL = np.array([230.0, 560.0])
SOL_R = 300.0
ORB = 1250.0
ER = 100.0
OMEGA = 0.03
TH0 = 0.2


def pos_orbita(th):
    return SOL + ORB * np.array([math.cos(th), math.sin(th)])


def tangente(th):
    return np.array([math.sin(th), -math.cos(th)])


def tierra_pos(t):
    """Primera parte: en órbita; tras 'disparada', en línea recta (con un leve acelerón de cámara rápida)."""
    if t <= A.disp:
        return pos_orbita(TH0 - OMEGA * t)
    th = TH0 - OMEGA * A.disp
    tau = t - A.disp
    s = ORB * OMEGA * tau + 60.0 * (tau - 0.5 * (1 - math.exp(-tau / 0.5)))
    return pos_orbita(th) + tangente(th) * s


def tierra2_pos(t):
    return pos_orbita(-0.14 - OMEGA * (t - B0))


def radio_luz(t):
    return SOL_R + (ORB - SOL_R) * (t - A.apaga) / (LLEGA - A.apaga)


def luz_tierra(t):
    return 1.0 - e_inout(prog(t, LLEGA, LLEGA + 0.8))


def _mix_cam(c1, c2, u):
    if u <= 0:
        return c1
    if u >= 1:
        return c2
    (a1, s1, z1), (a2, s2, z2) = c1, c2
    return (a1 + (a2 - a1) * u, s1 + (s2 - s1) * u, math.exp(lerp(math.log(z1), math.log(z2), u)))


def cam_espacio1(t):
    """(punto del mundo, dónde cae en pantalla, zoom)."""
    E = tierra_pos(t)
    c = (np.array([800.0, 560 + 0.5 * (E[1] - 560)]), np.array([960.0, 540.0]), 0.9 - 0.05 * prog(t, 0, A.apaga))
    c = _mix_cam(c, (E, np.array([1180.0, 560.0]), 1.3), e_inout(prog(t, A.tierra - 0.4, A.tierra + 1.3)))
    c = _mix_cam(c, (np.array([760.0, 0.5 * (560 + E[1])]), np.array([960.0, 560.0]), 0.8),
                 e_inout(prog(t, A.luz0 - 0.2, A.luz0 + 2.2)))
    c = _mix_cam(c, (E, np.array([1010.0, 590.0]), 1.4), e_inout(prog(t, LLEGA - 0.9, LLEGA + 1.4)))
    return c


def cam_espacio2(t):
    base = (np.array([840.0, 520.0]), np.array([960.0, 540.0]), 0.88 + 0.03 * prog(t, B1, D2[0]))
    if t < B1:     # sale del núcleo del Sol
        u = e_out(prog(t, BM, B1))
        z = math.exp(lerp(math.log(6.5), math.log(base[2]), u))
        fin = base[1] + base[2] * (SOL - base[0])
        return (SOL, np.array([960.0, 540.0]) + (fin - np.array([960.0, 540.0])) * u, z)
    return base


def cam_inmersion(t, d, cam_fn, pos_fn):
    """Cámara que cae hacia el borde superior de la Tierra: devuelve (cam, r_pantalla, u)."""
    u = prog(t, *d)
    ancla0, pant0, z0 = cam_fn(d[0])
    L = pos_fn(t) + np.array([0.0, -ER])
    L0 = pos_fn(d[0]) + np.array([0.0, -ER])
    p0 = pant0 + z0 * (L0 - ancla0)
    ue = e_inout(u)
    z = math.exp(lerp(math.log(z0), math.log(520.0), e_in(u) * 0.35 + ue * 0.65))
    p = p0 + (np.array([960.0, 700.0]) - p0) * ue
    return (L, p, z), ER * z, u


def matriz(cam):
    ancla, pant, z = cam
    return mat_t(pant[0], pant[1]) @ mat_s(z) @ mat_t(-ancla[0], -ancla[1])


def aplicar(cam, pt):
    ancla, pant, z = cam
    return pant + z * (np.asarray(pt) - ancla)


# ======================================================================== superficie (coords planas X, H↑)
class Sup:
    """Plano de la superficie -> pantalla: escala k y curvatura kappa (1/radio del planeta en px).
    Con kappa > 0 el paisaje se dobla sobre un planeta cuyo punto más alto está en (hx, hy)."""

    def __init__(self, hx, hy, k=1.0, kappa=0.0):
        self.hx, self.hy, self.k, self.kappa = hx, hy, k, kappa

    def p(self, X, Hh):
        a = self.k * np.asarray(X, float)
        h = self.k * np.asarray(Hh, float)
        kap = self.kappa
        if kap < 1e-9:
            return self.hx + a, self.hy - h
        phi = kap * a
        return (self.hx + np.sin(phi) / kap + h * np.sin(phi),
                self.hy + (1 - np.cos(phi)) / kap - h * np.cos(phi))

    def ang(self, X):
        return self.kappa * self.k * X

    def poly(self, pts):
        Q = np.asarray(pts, float)
        if self.kappa > 1e-9:
            Q = remuestrear(Q, 40.0, True)
        x, y = self.p(Q[:, 0], Q[:, 1])
        return np.stack([x, y], 1)

    @contextmanager
    def en(self, lz, X, Hh, s=1.0):
        x, y = self.p(X, Hh)
        with lz.grupo(float(x), float(y), s * self.k, self.ang(X)):
            yield


XS = np.arange(-4200, 4201, 40.0)


def _taper(X):
    return np.clip((4000 - np.abs(X)) / 900, 0, 1)


def suelo_h(X):
    X = np.asarray(X, float)
    return 5 * np.sin(X / 170) + 3 * np.sin(X / 70 + 1)


def fondo_mar(X):
    return -1250 + 30 * np.sin(np.asarray(X, float) / 170)


VENT_X, VENT2_X = 640.0, 930.0
VENT_TOP = float(fondo_mar(VENT_X)) + 305
MICROBIOS = [(500, -1060, 0, (120, 232, 150)), (566, -1185, 1, (255, 140, 200)), (770, -1010, 2, (120, 200, 255)),
             (835, -1150, 1, (255, 200, 90)), (705, -1215, 0, (190, 150, 255)), (430, -1170, 2, (120, 232, 190)),
             (880, -1065, 0, (255, 150, 120))]


def tinte(c, noche, hielo):
    c = mezcla(c, (214, 228, 248), hielo * 0.7)
    return mezcla(c, mezcla(c, (14, 18, 54), 0.72), noche)


def estado(t):
    """Estado del paisaje: primera visita (noche que se congela) o amanecer final."""
    if t < BM:
        hielo = 0.05 + 0.4 * e_inout(prog(t, A.semana, A.cero1)) + 0.45 * e_inout(prog(t, A.ano, A.cero2))
        return dict(noche=1.0, hielo=hielo, perdida=e_inout(prog(t, A.foto, A.foto + 1.8)),
                    mar=e_inout(prog(t, A.oceanos, A.arriba + 0.4)), nieve=0.25 + 0.75 * prog(t, A.semana, A.cero2),
                    manta=prog(t, A.manta - 0.1, A.manta + 1.3), amanecer=0.0,
                    negro=e_inout(prog(t, A.cielo, A.negro + 0.35)))
    return dict(noche=0.45 * (1 - e_inout(prog(t, D2[1] - 0.4, A.gracias))), hielo=0.0, perdida=0.0, mar=0.0,
                nieve=0.0, manta=0.0, amanecer=1.0, negro=0.0)


def temperatura(t):
    if t < A.ano:
        return lerp(15, -18, e_inout(prog(t, A.semana, A.cero1)))
    return lerp(-18, -73, e_inout(prog(t, A.ano, A.cero2)))


def cielo(t, est):
    """Fondo (1080p) del cielo de la superficie."""
    if est["amanecer"] > 0:
        u = e_inout(prog(t, D2[1] - 0.5, A.gracias + 0.5))
        arriba = mezcla((34, 52, 130), (70, 130, 222), u)
        abajo = mezcla((255, 150, 120), (255, 214, 160), u)
        img = F.degradado(t, tuple(v / 255 for v in arriba), tuple(v / 255 for v in abajo))
        return F.estrellas(img, t, 0.5 * (1 - u))
    n = est["negro"]
    arriba = mezcla((26, 40, 104), (5, 7, 24), n)
    abajo = mezcla((70, 92, 168), (20, 18, 50), n)
    img = F.degradado(t, tuple(v / 255 for v in arriba), tuple(v / 255 for v in abajo))
    return F.estrellas(img, t, 0.25 + 0.75 * n)


def paisaje(lz, t, S, est, alfa=1.0, corte=1.0):
    """Todo el mundo de la superficie (colinas, mar en corte, suelo en corte, fumarolas, árboles, pajarito).
    alfa: opacidad de lo que está sobre el suelo; corte: opacidad del corte transversal (mar, suelo, fondo)."""
    noche, hielo = est["noche"], est["hielo"]

    def tn(c):
        return tinte(c, noche, hielo)

    X = XS
    tp = _taper(X)
    # sol del amanecer (detrás de las colinas)
    if est["amanecer"] > 0:
        hs = lerp(-40, 330, e_out(prog(t, D2[1] - 0.9, A.gracias + 0.4)))
        x, y = S.p(-620, hs)
        P.sol(lz, float(x), float(y), 88 * S.k, t, brillo=1.0)
    # colinas lejanas y medias
    Hf = (80 + 40 * np.sin(X / 260 + 1) + 22 * np.sin(X / 130 + 2.3)) * tp
    lz.relleno(S.poly(np.concatenate([np.stack([X, Hf], 1), [[X[-1], -80], [X[0], -80]]])), tn((120, 190, 182)),
               alfa=alfa)
    Xm = X[X < 160]
    Hm = (38 + 22 * np.sin(Xm / 200 + 0.4) + 14 * np.sin(Xm / 90)) * _taper(Xm) * (1 - smooth_arr((Xm - 0) / 160))
    lz.relleno(S.poly(np.concatenate([np.stack([Xm, Hm], 1), [[160, -80], [Xm[0], -80]]])), tn((88, 174, 136)),
               alfa=alfa)
    # mar en corte (degradado por profundidad)
    Xa = X[X > 100]
    sup = -8 + (2.5 * np.sin(Xa / 60 + t * 1.6)) * (1 - est["mar"])
    agua = np.concatenate([np.stack([Xa, sup], 1), np.stack([Xa[::-1], fondo_mar(Xa[::-1]) - 40], 1)])
    x0, y0 = S.p(VENT_X, 0)
    x1, y1 = S.p(VENT_X, -1250)
    lz.degradado(S.poly(agua), tinte((60, 150, 226), noche * 0.8, 0), (10, 22, 62), (float(x0), float(y0)),
                 (float(x1), float(y1)), alfa=corte)
    # fondo del mar
    Xf = X[X > 240]
    fm = np.concatenate([np.stack([Xf, fondo_mar(Xf)], 1), [[Xf[-1], -2700], [Xf[0], -2700]]])
    lz.relleno(S.poly(fm), (48, 40, 82), alfa=corte)
    for i, (rx, rr) in enumerate(((330, 50), (470, 34), (1120, 60), (1260, 40), (1500, 70))):
        with S.en(lz, rx, float(fondo_mar(rx)) - 6):
            lz.relleno(elipse(0, 0, rr * 1.4, rr * 0.8, 0, 32), (66, 54, 100), alfa=corte)
    # suelo en corte (izquierda) con estratos
    Xs = X[X < 110]
    tope = suelo_h(Xs)
    suelo = np.concatenate([np.stack([Xs, tope], 1), [[150, -120], [220, -520], [270, -1000], [300, -1300],
                                                      [320, -2700], [Xs[0], -2700]]])
    Ps = S.poly(suelo)
    if corte > 0.004:
        lz.relleno(Ps, tn((118, 84, 76)), alfa=corte)
        with lz.recorte(Ps):
            for h0, h1, c in ((-260, -330, (132, 96, 84)), (-560, -700, (100, 72, 78)), (-900, -960, (124, 90, 86)),
                              (-1150, -2700, (78, 60, 80))):
                lz.relleno(S.poly([[-4200, h0], [400, h0 - 20], [400, h1], [-4200, h1]]), tn(c), alfa=corte)
            for i in range(9):   # piedritas
                px_, ph = -900 + i * 190 + 40 * math.sin(i * 7.1), -380 - 90 * (i % 4) - 170 * (i % 2)
                with S.en(lz, px_, ph):
                    lz.relleno(elipse(0, 0, 26 + 8 * (i % 3), 15, 0.3 * i, 20), tn((150, 116, 100)), alfa=corte)
            for i in range(14):  # raíces bajo el pasto
                rx = -1100 + i * 90
                with S.en(lz, rx, float(suelo_h(rx)) - 28):
                    lz.trazo(np.array([[0, 0], [8 * math.sin(i), 30], [-6, 60 + 20 * (i % 3)]]), tn((96, 70, 64)),
                             5, afinar=True)
    pasto = np.concatenate([np.stack([Xs, tope + 4], 1), np.stack([Xs[::-1], tope[::-1] - 30], 1)])
    lz.relleno(S.poly(pasto), tn((70, 158, 102)), alfa=alfa)
    if hielo > 0.2:   # nieve que se acumula sobre el pasto
        g = 16 * clamp01((hielo - 0.2) / 0.7)
        nv = np.concatenate([np.stack([Xs, tope + 4 + g], 1), np.stack([Xs[::-1], tope[::-1] + 2], 1)])
        lz.relleno(S.poly(nv), tinte((236, 244, 255), noche * 0.55, 0), alfa=alfa)
    # hielo sobre el mar (crece desde arriba)
    if est["mar"] > 0.005:
        g = 78 * est["mar"]
        hx = np.concatenate([np.stack([Xa, np.full_like(Xa, 6.0)], 1), np.stack([Xa[::-1], np.full_like(Xa, -8 - g)], 1)])
        xa0, ya0 = S.p(VENT_X, 6)
        xa1, ya1 = S.p(VENT_X, -8 - g)
        lz.degradado(S.poly(hx), tinte((236, 246, 255), noche * 0.5, 0), tinte((160, 204, 240), noche * 0.5, 0),
                     (float(xa0), float(ya0)), (float(xa1), float(ya1)), alfa=corte)
        brillo_h = np.concatenate([np.stack([Xa, np.full_like(Xa, 6.0)], 1),
                                   np.stack([Xa[::-1], np.full_like(Xa, 0.0)], 1)])
        lz.relleno(S.poly(brillo_h), (250, 253, 255), alfa=0.8 * corte)
        if est["manta"] > 0:   # costuras de "manta"
            col_c = (70, 104, 176)
            for hh in (-8 - g * 0.28, -8 - g * 0.74):
                xs_, ys_ = S.p(np.linspace(150, 1700, 80), np.full(80, hh))
                P.discontinua(lz, np.stack([xs_, ys_], 1), col_c, 5 * S.k, 18 * S.k, 12 * S.k, frac=est["manta"])
            for gx in range(330, 1700, 190):
                x0_, y0_ = S.p(gx, 2)
                x1_, y1_ = S.p(gx, -6 - g)
                P.discontinua(lz, [[float(x0_), float(y0_)], [float(x1_), float(y1_)]], col_c, 5 * S.k,
                              12 * S.k, 10 * S.k, frac=clamp01(est["manta"] * 1.6 - (gx - 330) / 2600))
    # fumarolas y microbios
    if corte > 0.5:
        with S.en(lz, VENT2_X, float(fondo_mar(VENT2_X)) + 4, 0.58):
            P.fumarola(lz, 0, 0, 1.0, t + 3.1, agua=(14, 28, 70))
        with S.en(lz, VENT_X, float(fondo_mar(VENT_X)) + 4, 1.0):
            P.fumarola(lz, 0, 0, 1.0, t, agua=(14, 28, 70))
    if t > A.microbios - 0.2 and t < D2[0]:
        for i, (mx, mh, forma, col) in enumerate(MICROBIOS):
            t0 = A.microbios + 0.13 * i
            k = e_back(prog(t, t0, t0 + 0.4))
            if k <= 0.01:
                continue
            salto = 14 * math.sin(math.pi * prog(t, A.vivos + 0.06 * i, A.vivos + 0.06 * i + 0.45))
            mx, mh = mx + 12 * math.sin(t * 0.8 + i), mh + 10 * math.sin(t * 1.1 + i * 2) + salto
            if t > B0:   # se apartan nadando cuando la cámara entra en el brillo
                f = 1 + 2.5 * e_in(prog(t, B0, BM))
                mx, mh = VENT_X + (mx - VENT_X) * f, VENT_TOP + (mh - VENT_TOP) * f
            with S.en(lz, mx, mh, k):
                P.microbio(lz, 0, 0, 1.15, t, col, seed=i, forma=forma,
                           mirar=(math.sin(t + i), 0.3 * math.cos(t * 1.3 + i)), brillo=0.55)
    # árboles, pajarito, termómetro
    for tx, ts in ((-270, 1.05), (-20, 0.8)):
        with S.en(lz, tx, float(suelo_h(tx)) - 2):
            P.arbol(lz, 0, 0, ts, t, perdida=est["perdida"], escarcha=hielo * 0.8, oscuro=noche * 0.62)
            if est["perdida"] > 0:
                P.hojas_cayendo(lz, 0, -200 * ts, t, A.foto, n=9, col=tinte((190, 150, 100), noche * 0.5, 0))
    pajaro(lz, t, S, est)
    if A.semana - 1.0 < t < BAJA2[1]:
        termometro(lz, t, S, est)
    # nieve (en coords planas: cae sobre el paisaje y se va con la cámara)
    if est["nieve"] > 0.01:
        n = int(90 * est["nieve"])
        for i in range(n):
            u = (t * (40 + 25 * ((i * 7) % 5)) / 1000 + (i * 0.618) % 1) % 1
            nx = -1000 + (i * 263.7) % 2000 + 30 * math.sin(t * 0.9 + i)
            nh = 1000 - u * 1000
            if nh < suelo_h(nx) + 4 and nx < 120:
                continue
            x, y = S.p(nx, nh)
            lz.puntos([[float(x), float(y)]], (2.2 + 1.8 * ((i * 3) % 4) / 3) * S.k, (236, 244, 255))


def smooth_arr(x):
    x = np.clip(x, 0, 1)
    return x * x * (3 - 2 * x)


def pajaro(lz, t, S, est):
    X0 = -145.0
    if est["amanecer"] > 0:
        feliz = 1.0 if t > A.gracias - 0.05 else 0.0
        aleteo = 0.5 + 0.5 * math.sin((t - A.gracias) * 14) if A.gracias < t < A.gracias + 1.4 else 0.0
        salto = 16 * abs(math.sin((t - A.gracias) * 7)) * (1 - prog(t, A.gracias, A.gracias + 1.2)) \
            if t > A.gracias else 0.0
        with S.en(lz, X0, float(suelo_h(X0)) + salto):
            P.pajaro(lz, 0, 0, 0.95, t, color=(128, 90, 216), mirar=(-0.8, -0.5), aleteo=aleteo, feliz=feliz,
                     voltear=True, boca=0.6 * feliz * (1 - prog(t, A.gracias + 0.6, A.gracias + 1.0)))
            if t > A.gracias:
                for j in range(3):
                    u = prog(t, A.gracias + 0.15 * j, A.gracias + 0.15 * j + 1.6)
                    if 0 < u < 1:
                        s_ = e_back(min(1, u * 3)) * (1 - e_in(prog(u, 0.7, 1.0)))
                        lz.relleno(corazon(-70 + 50 * j, -180 - 130 * u, 28 * s_), (255, 110, 150))
        return
    noche = est["noche"]
    col = tinte((128, 90, 216), noche * 0.45, 0)
    mirar = (0.3, -1.0) if t < A.semana else (0.2, 0.2)
    tiritar = prog(t, A.semana, A.semana + 0.6)
    with S.en(lz, X0, float(suelo_h(X0))):
        P.pajaro(lz, 0, 0, 0.95, t, color=col, mirar=mirar, tiritar=tiritar, escarcha=est["hielo"])


def termometro(lz, t, S, est):
    temp = temperatura(t)
    a = e_out(prog(t, A.semana - 0.9, A.semana - 0.3))
    nivel = (temp + 90) / 170
    with S.en(lz, -640, -118, 0.72 * (0.7 + 0.3 * a)):
        P.termometro(lz, 0, 0, 1.0, nivel, col=mezcla((255, 110, 90), (120, 190, 255), prog(temp, 5, -60)))
    x, y = S.p(-585, 380)
    txt = f"{int(round(temp))} °C".replace("-", "−")
    P.rotulo(lz, float(x), float(y), txt, 72 * S.k, k=a, ancla=(0, 0.5), capa=1)
    etiqueta = "1 SEMANA" if t < A.ano else "1 AÑO"
    ae = prog(t, A.semana, A.semana + 0.3) if t < A.ano else prog(t, A.ano, A.ano + 0.3)
    P.rotulo(lz, float(x) + 4, float(y) + 62 * S.k, etiqueta, 34 * S.k, k=a * (0.6 + 0.4 * ae), ancla=(0, 0.5),
             fuente="geo_n", alfa=ae, capa=1)


def cam_superficie(t):
    """Sup para la superficie después de la inmersión 1 (frío -> bajo el hielo -> fondo -> brillo)."""
    kap = 1 / (520.0 * ER) * math.exp(-8 * max(0.0, t - D1[1]))
    u1, u2 = e_inout(prog(t, *BAJA1)), e_inout(prog(t, *BAJA2))
    k = lerp(1.0 + 0.16 * e_inout(prog(t, D1[1] - 0.2, A.semana + 0.8)), 1.0, u1)
    hx, hy = 960.0 - 25 * prog(t, D1[1], BAJA1[0]), 700.0 + 60 * (k - 1)
    hx = lerp(hx, 960 - VENT_X, u1)
    hy = lerp(hy, 150.0, u1)
    hy = lerp(hy, 420 + VENT_TOP, u2)       # la boca de la fumarola a y=420
    if t > B0:   # zoom a la boca de la fumarola
        u = prog(t, B0, BM)
        k = math.exp(lerp(0, math.log(16), e_in(u)))
        px, py = lerp(960.0, 960.0, u), lerp(420.0, 540.0, e_inout(u))
        hx = px - k * VENT_X
        hy = py + k * VENT_TOP
    return Sup(hx, hy, k, kap)


def cam_amanecer(t):
    kap = 1 / (520.0 * ER) * math.exp(-8 * max(0.0, t - D2[1]))
    return Sup(960.0 + 18 * prog(t, D2[1], TOTAL), 700.0, 1.0 + 0.04 * prog(t, D2[1], TOTAL), kap)


# ======================================================================== espacio: dibujo
def dibujar_espacio(lz, t, cam, fase, atm=1.0):
    """fase 1: Sol apagándose, onda, Tierra que se va. fase 2: Sol vivo, Tierra en órbita."""
    lz.M = matriz(cam)
    z = cam[2]
    lineas = z < 2.2          # en la inmersión, órbitas y rótulos quedan atrás
    if fase == 1:
        E = tierra_pos(t)
        luz = luz_tierra(t)
        apagado = e_out(prog(t, A.apaga, A.apaga + 0.75))
    else:
        E = tierra2_pos(t)
        luz, apagado = 1.0, 0.0
    # órbita
    fase_o = t * 8
    alfa_orb = 0.55 if fase == 1 else 0.45
    col_orb = mezcla((20, 20, 60), (150, 160, 230), alfa_orb)
    if lineas:
        P.discontinua(lz, P.arco_pts(SOL[0], SOL[1], ORB, -1.5, 1.1, 400), col_orb, 3.0, 20, 18, fase=fase_o)
    # Sol
    P.sol(lz, SOL[0], SOL[1], SOL_R, t, brillo=1.0 + (0.25 * campana(t, A.suerte, A.suerte + 1.2) if fase == 2 else 0),
          apagado=apagado)
    if fase == 1 and t > A.apaga:
        r = radio_luz(t)
        a_on = e_out(prog(t, A.apaga, A.apaga + 0.4)) * (1 - prog(t, LLEGA + 2.5, LLEGA + 4.0))
        P.onda(lz, SOL[0], SOL[1], r, 34, (255, 196, 110), alfa=0.95 * a_on)
        if t > A.grav - 0.3:
            ag = e_out(prog(t, A.grav - 0.3, A.grav + 0.5)) * a_on
            for j in range(3):
                P.onda(lz, SOL[0], SOL[1], r - 40 - 34 * j, 7, (170, 130, 255), alfa=0.7 * ag * (1 - 0.25 * j),
                       frente=0.6, estela=0.6)
        # rótulos que viajan con la onda
        if t > A.ultima - 0.2:
            k = e_back(prog(t, A.ultima - 0.2, A.ultima + 0.2)) * (1 - prog(t, LLEGA - 0.6, LLEGA))
            q = SOL + (r + 30) * np.array([math.cos(-0.36), math.sin(-0.36)])
            P.rotulo(lz, q[0], q[1], "ÚLTIMA LUZ", 60, k=k, ancla=(0, 0.5), color=(255, 226, 160), capa=1)
        if t > A.grav - 0.2:
            k = e_back(prog(t, A.grav - 0.2, A.grav + 0.2)) * (1 - prog(t, LLEGA - 0.6, LLEGA))
            q = SOL + (r - 150) * np.array([math.cos(-0.1), math.sin(-0.1)])
            P.rotulo(lz, q[0], q[1], "GRAVEDAD", 60, k=k, ancla=(1, 0.5), color=(206, 180, 255), capa=1)
    # trayectoria libre + fantasma que sigue la órbita
    if fase == 1 and t > A.disp - 0.1 and lineas:
        th = TH0 - OMEGA * A.disp
        p0 = pos_orbita(th)
        frac = e_out(prog(t, A.disp - 0.1, A.disp + 1.0))
        P.discontinua(lz, [p0, p0 + tangente(th) * 1600], (236, 240, 255), 4.0, 26, 16, fase=-t * 30, frac=frac)
        g = pos_orbita(TH0 - OMEGA * t)
        ag = 0.35 * prog(t, A.disp, A.disp + 0.6)
        lz.relleno(circulo(g[0], g[1], ER, 80), (140, 160, 230), alfa=ag)
        P.rotulo(lz, g[0] + ER + 24, g[1], "órbita", 30, k=1.0, ancla=(0, 0.5), fuente="geo_n",
                 color=(170, 180, 240), alfa=ag / 0.35 * (1 - prog(t, D1[0], D1[0] + 0.5)), capa=1)
    # Luna
    am = 0.25 * t + 2.0
    lpos = E + 175 * np.array([math.cos(am), 0.45 * math.sin(am)])
    if math.sin(am) < 0:   # detrás de la Tierra
        P.luna(lz, lpos[0], lpos[1], 26, math.atan2(SOL[1] - lpos[1], SOL[0] - lpos[0]), luz)
    P.tierra(lz, E[0], E[1], ER, t, rot=0.6 + 0.1 * t, ang_luz=math.atan2(SOL[1] - E[1], SOL[0] - E[0]), luz=luz,
             ciudades=(prog(t, LLEGA + 0.2, LLEGA + 1.2) * (1 - prog(z, 2.5, 6.0))) if fase == 1 else 0.0,
             atmosfera=atm, nubes=1 - prog(z, 3.0, 9.0))
    if math.sin(am) >= 0:
        P.luna(lz, lpos[0], lpos[1], 26, math.atan2(SOL[1] - lpos[1], SOL[0] - lpos[0]), luz)
    if fase == 1 and lineas:
        # "¿Qué le pasaría a la Tierra?": pulso
        u = prog(t, A.tierra - 0.1, A.tierra + 0.9)
        if 0 < u < 1:
            P.onda(lz, E[0], E[1], ER * (1.05 + 0.6 * e_out(u)), 6, (255, 255, 255), alfa=0.8 * (1 - u), frente=0.5,
                   estela=0.5)
        k = e_back(prog(t, A.nada - 0.15, A.nada + 0.2)) * (1 - e_in(prog(t, A.ultima - 0.3, A.ultima)))
        P.pastilla(lz, E[0], E[1] + ER + 70, "todo normal", 40, k=k)
        k = e_back(prog(t, A.treinta - 0.1, A.treinta + 0.25)) * (1 - prog(t, D1[0] - 0.4, D1[0]))
        P.pastilla(lz, E[0] + ER + 160, E[1] + 40, "30 km/s", 44, k=k)
    lz.M = np.eye(3)


def fondo_espacio(t, cam):
    ancla, pant, z = cam
    return F.espacio(t, dx=-ancla[0] * 0.05 * min(z, 3), dy=-ancla[1] * 0.05 * min(z, 3))


# ======================================================================== interfaz (pantalla)
def ui_titulo(lz, t, a):
    if a > 0.01:
        P.rotulo(lz, 960, 96, "¿QUÉ PASARÍA SI EL SOL SE APAGARA?", 60, k=0.94 + 0.06 * a, alfa=a)


def ui_reloj(lz, t):
    a = e_out(prog(t, A.apaga + 0.6, A.apaga + 1.2)) * (1 - prog(t, A.disp, A.disp + 0.5))
    if a <= 0.01:
        return
    seg = int(500 * clamp01((t - A.apaga) / (LLEGA - A.apaga)))
    pulso = 1 + 0.12 * campana(t, A.ocho - 0.05, A.ocho + 0.5) + 0.12 * campana(t, LLEGA - 0.05, LLEGA + 0.5)
    col = mezcla((255, 255, 255), (255, 214, 120), prog(t, LLEGA - 0.2, LLEGA))
    P.rotulo(lz, 960, 92, f"{seg // 60}:{seg % 60:02d}", 76, k=pulso, alfa=a, fuente="geo_x", color=col)
    P.rotulo(lz, 960, 150, "desde el apagón", 28, alfa=a * 0.85, fuente="geo_n", color=(200, 205, 240))


def ui_barra(lz, t):
    a = e_out(prog(t, A.cinco - 0.35, A.cinco + 0.1)) * (1 - prog(t, D2[0], D2[0] + 0.4))
    if a <= 0.01:
        return
    x0, x1, y, h = 440.0, 1240.0, 150.0, 26.0
    w = x1 - x0
    hoy = 0.46
    with lz.capa(2):
        lz.relleno(rect_red(x0, y - h / 2, w, h, h / 2), (255, 255, 255), alfa=0.16 * a)
        lz.relleno(rect_red(x0, y - h / 2, w * hoy, h, h / 2), (255, 160, 70), alfa=a)
        f = e_inout(prog(t, A.cinco + 0.1, A.cinco + 1.3))
        if f > 0:
            lz.relleno(rect_red(x0 + w * hoy - h / 2, y - h / 2, w * (1 - hoy) * f + h / 2, h, h / 2), (255, 222, 120),
                       alfa=a)
        xh = x0 + w * hoy
        lz.relleno(np.array([[xh - 12, y - h / 2 - 20], [xh + 12, y - h / 2 - 20], [xh, y - h / 2 - 4]]),
                   (255, 255, 255), alfa=a)
    P.rotulo(lz, xh, y - 64, "HOY", 42, alfa=a)
    P.rotulo(lz, x0 - 24, y, "vida del Sol", 36, fuente="geo_n", ancla=(1, 0.5), alfa=a * 0.9, color=(210, 214, 245))
    P.rotulo(lz, x0 + w * (hoy + (1 - hoy) / 2), y + 58, "≈ 5 000 millones de años más", 38, fuente="geo_n",
             alfa=a * prog(t, A.cinco + 0.4, A.cinco + 0.9), color=(255, 232, 170))


def ui_etiquetas_mar(lz, t, S):
    a = e_out(prog(t, A.liquida - 0.2, A.liquida + 0.3)) * (1 - prog(t, A.fondo, A.fondo + 0.8))
    if a > 0.01:
        x, y = S.p(VENT_X, -420)
        P.rotulo(lz, float(x), float(y), "AGUA LÍQUIDA", 56 * S.k, k=0.9 + 0.1 * a, alfa=a)
    a = e_out(prog(t, A.hidro - 0.2, A.hidro + 0.3)) * (1 - prog(t, B0, B0 + 0.4))
    if a > 0.01:
        xv, yv = S.p(VENT_X - 20, VENT_TOP + 10)
        xl, yl = S.p(VENT_X - 400, VENT_TOP + 150)
        P.linea_llamada(lz, (float(xv), float(yv)), (float(xl) + 150, float(yl) + 10), frac=a)
        P.rotulo(lz, float(xl), float(yl), "FUENTE HIDROTERMAL", 46 * S.k, alfa=a, ancla=(0.5, 1.0))
    a = e_out(prog(t, A.vivos - 0.1, A.vivos + 0.3)) * (1 - prog(t, B0, B0 + 0.4))
    if a > 0.01:
        x, y = S.p(VENT_X + 330, -1330)
        P.rotulo(lz, float(x), float(y), "¡seguimos aquí!", 42 * S.k, fuente="geo_n", alfa=a, color=(200, 255, 210))


# ======================================================================== render del plano secuencia
def render_mundo(lz, t):
    lz.nuevo(t, wob=0.0)
    ui = []
    if t < D1[0]:                                   # 1. espacio
        cam = cam_espacio1(t)
        bg = fondo_espacio(t, cam)
        dibujar_espacio(lz, t, cam, 1)
        ui_titulo(lz, t, e_out(prog(t, 0.15, 0.8)) * (1 - prog(t, A.apaga - 0.9, A.apaga - 0.3)))
        ui_reloj(lz, t)
    elif t < D1[1]:                                 # 3. inmersión en la Tierra oscura
        cam, rs, u = cam_inmersion(t, D1, cam_espacio1, tierra_pos)
        est = estado(t)
        s_cielo = prog(math.log(rs), math.log(1300), math.log(12000))
        bg = fondo_espacio(t, cam) * (1 - s_cielo) + cielo(t, est) * s_cielo
        dibujar_espacio(lz, t, cam, 1, atm=1 - prog(rs, 6000, 30000))
        S = Sup(cam[1][0], cam[1][1], min(1.0, rs / 9000), 1 / rs)
        paisaje(lz, t, S, est, alfa=prog(rs, 260, 800), corte=e_inout(prog(S.k, 0.35, 0.9)))
    elif t < BM:                                    # 4-6. superficie, bajo el hielo, fumarola
        S = cam_superficie(t)
        est = estado(t)
        bg = cielo(t, est)
        paisaje(lz, t, S, est)
        ui_etiquetas_mar(lz, t, S)
        if t > B0:
            u = prog(t, B0, BM)
            xv, yv = S.p(VENT_X, VENT_TOP)
            with lz.capa(2):
                lz.halo(float(xv), float(yv), lerp(260, 3200, e_in(u)), C_GLOW, alfa=min(1.0, 0.5 + u),
                        r0=lerp(0.1, 0.55, u), dureza=1.3)
                if u > 0.85:
                    lz.relleno(rect_red(-10, -10, W + 20, H + 20, 0), C_GLOW, alfa=smooth(prog(u, 0.85, 1.0)))
    elif t < D2[0]:                                 # 6-7. el brillo es el Sol
        cam = cam_espacio2(t)
        bg = fondo_espacio(t, cam)
        dibujar_espacio(lz, t, cam, 2)
        a = 1 - e_out(prog(t, BM, BM + 0.55))
        if a > 0.003:
            with lz.capa(2):
                lz.relleno(rect_red(-10, -10, W + 20, H + 20, 0), C_GLOW, alfa=a)
        ui_barra(lz, t)
    elif t < D2[1]:                                 # 8. inmersión por el amanecer
        cam, rs, u = cam_inmersion(t, D2, cam_espacio2, tierra2_pos)
        est = estado(t)
        s_cielo = prog(math.log(rs), math.log(1300), math.log(12000))
        bg = fondo_espacio(t, cam) * (1 - s_cielo) + cielo(t, est) * s_cielo
        dibujar_espacio(lz, t, cam, 2, atm=1 - prog(rs, 6000, 30000))
        ui_barra(lz, t)
        S = Sup(cam[1][0], cam[1][1], min(1.0, rs / 9000), 1 / rs)
        paisaje(lz, t, S, est, alfa=prog(rs, 260, 800), corte=e_inout(prog(S.k, 0.35, 0.9)))
    else:                                           # 9. amanecer y final
        S = cam_amanecer(t)
        est = estado(t)
        bg = cielo(t, est)
        paisaje(lz, t, S, est)
        ui_titulo(lz, t, e_out(prog(t, A.fin + 0.15, A.fin + 0.8)))
    img = componer(bg, lz.resolver(), boil=lz.boil)
    negro = prog(t, TOTAL - 0.9, TOTAL - 0.1)
    if negro > 0:
        img = img * (1 - smooth(negro))
    return np.clip(img, 0, 1)


# ======================================================================== sonido
def registrar_sfx(e):
    ev = e.ev
    ev(0.3, "brillo", 0.3, 0.0)
    ev(A.apaga, "apagon", 0.9)
    ev(A.tierra, "pop", 0.35, 0.3, tono=0.9)
    ev(A.ocho, "ding", 0.3, 0.0, tono=0.9)
    ev(A.nada, "pop", 0.45, 0.4)
    ev(A.ultima - 0.15, "whoosh", 0.3, 0.3)
    ev(A.grav - 0.2, "morph", 0.35, -0.2)
    ev(LLEGA, "ding", 0.4, 0.3, tono=0.75)
    ev(LLEGA + 0.1, "golpe_suave", 0.5, 0.3)
    ev(A.disp - 0.1, "zoom_whoosh", 0.55, 0.4)
    ev(A.treinta, "pop", 0.4, 0.5)
    ev(D1[0], "suspiro", 0.8, 0.0, dur=round(D1[1] - D1[0] + 0.4, 2))
    ev(A.negro - 0.2, "viento", 0.3, 0.0, dur=2.5)
    ev(A.semana, "viento", 0.25, -0.3, dur=3.0)
    ev(A.semana + 0.3, "brr", 0.35, -0.2)
    ev(A.ano, "tick", 0.3, -0.5)
    ev(A.foto + 0.1, "puf", 0.25, -0.2)
    ev(A.oceanos, "hielo", 0.7, 0.4, dur=1.6)
    ev(BAJA1[0], "suspiro", 0.6, 0.0, dur=round(BAJA1[1] - BAJA1[0], 2))
    ev(A.manta, "puntada", 0.45, 0.2)
    for j in range(3):
        ev(A.liquida + 0.15 * j, "burbuja", 0.3, 0.2 * j - 0.2, tono=1 + 0.2 * j)
    ev(BAJA2[0], "suspiro", 0.6, 0.0, dur=round(BAJA2[1] - BAJA2[0], 2))
    ev(A.hidro, "revelar", 0.45, -0.2)
    for i in range(len(MICROBIOS)):
        ev(A.microbios + 0.13 * i, "pop", 0.28, -0.5 + 0.16 * i, tono=1.0 + 0.1 * i)
    ev(A.vivos, "brillo", 0.4, 0.3)
    ev(B0, "zoom_whoosh", 0.5, 0.0)
    ev(BM - 0.2, "amanecer", 0.5, 0.0, dur=1.2)
    ev(A.cinco, "ding", 0.35, 0.2)
    ev(D2[0], "suspiro", 0.7, 0.0, dur=round(D2[1] - D2[0] + 0.4, 2))
    ev(A.manana, "amanecer", 0.5, 0.0, dur=2.2)
    ev(A.gracias, "pio", 0.7, -0.3)
    ev(A.gracias + 0.4, "pio", 0.6, -0.3, tono=1.12)
    ev(A.fin + 0.2, "brillo", 0.3, 0.0)


class Mundo(Escena):
    """Plano secuencia: todas las escenas del guion comparten este mismo mundo continuo."""

    def preparar(self):
        if self.idx == 0:        # los efectos se registran una sola vez
            registrar_sfx(self)

    def render(self, lz, t):
        return render_mundo(lz, t)


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
