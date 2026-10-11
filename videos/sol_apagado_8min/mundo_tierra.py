# -*- coding: utf-8 -*-
"""La superficie (y lo que hay debajo) del plano secuencia: coordenadas planas X (derecha) y H (arriba).
Tierra firme a la izquierda (con corte del suelo: refugio subterráneo, calor profundo), mar a la derecha
(corte con hielo, fuentes hidrotermales) y roca profunda con microbios bajo el fondo marino."""
import math

import numpy as np

import fondos as F
import plano as P
from plano import mezcla, aclarar
from motor import W, H, prog, clamp01, lerp, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, smooth, corazon
from mundo_comun import Sup, smooth_arr, pop, ventana, campana, interp_log, INI, FIN
from anclas import A, D1, B0, BM, B1, D2, TOTAL

C_GLOW = (255, 206, 120)
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
H_MAGMA = -3500.0
MICROBIOS = [(500, -1060, 0, (120, 232, 150)), (566, -1185, 1, (255, 140, 200)), (770, -1010, 2, (120, 200, 255)),
             (835, -1150, 1, (255, 200, 90)), (705, -1215, 0, (190, 150, 255)), (430, -1170, 2, (120, 232, 190)),
             (880, -1065, 0, (255, 150, 120))]
_rng = np.random.default_rng(8)
PROFUNDOS = [(300 + 1500 * _rng.random(), -1400 - 1900 * _rng.random(), int(_rng.integers(0, 3)),
              [(120, 232, 150), (255, 140, 200), (120, 200, 255), (255, 200, 90)][int(_rng.integers(0, 4))])
             for _ in range(46)]


def tinte(c, noche, hielo):
    c = mezcla(c, (214, 228, 248), hielo * 0.7)
    return mezcla(c, mezcla(c, (14, 18, 54), 0.72), noche)


# ======================================================================== estado del mundo
def estado(t):
    if t < BM:
        hielo = (0.05 + 0.35 * e_inout(prog(t, A.semana, A.cero1)) + 0.5 * e_inout(prog(t, A.ano, A.cero2)))
        return dict(
            noche=1.0, hielo=hielo, amanecer=0.0,
            negro=e_inout(prog(t, A.cielo, A.negro + 0.35)),
            flores=1 - e_inout(prog(t, A.plantas - 0.2, A.plantas + 1.8)),
            perdida=e_inout(prog(t, A.millones_f - 0.3, A.nitrogeno + 0.8)),
            mar=e_inout(prog(t, A.oceanos_f - 0.2, A.manta + 0.2)),
            manta=prog(t, A.manta - 0.1, A.manta + 1.4),
            nieve=0.2 + 0.8 * prog(t, A.semana, A.cero2) - 0.2 * prog(t, A.tiempo_atm, A.viento + 1),
            co2=e_inout(prog(t, A.dioxido - 0.3, A.nieve + 1.8)),
            aire_helado=e_inout(prog(t, A.nitrogeno - 0.4, A.suelo_f + 1.0)),
            nubes=1 - e_inout(prog(t, A.viento - 0.8, A.viento + 1.6)),
            viento=1 - e_inout(prog(t, A.tiempo_atm, A.viento)),
        )
    return dict(noche=0.45 * (1 - e_inout(prog(t, D2[1] - 0.4, A.gracias))), hielo=0.0, amanecer=1.0, negro=0.0,
                flores=1.0, perdida=0.0, mar=0.0, manta=0.0, nieve=0.0, co2=0.0, aire_helado=0.0, nubes=0.6,
                viento=1.0)


def temperatura(t):
    if t < A.ano:
        return lerp(15, -18, e_inout(prog(t, A.semana, A.cero1)))
    if t < A.dioxido - 0.4:
        return lerp(-18, -73, e_inout(prog(t, A.ano, A.cero2)))
    if t < A.millones_f:
        return lerp(-73, -78, e_inout(prog(t, A.dioxido - 0.4, A.dioxido + 0.6)))
    return lerp(-78, -240, e_inout(prog(t, A.millones_f, A.nitrogeno)))


def cielo(t, est):
    """Fondo de pantalla del cielo (1080p)."""
    if est["amanecer"] > 0:
        u = e_inout(prog(t, D2[1] - 0.5, A.gracias + 0.5))
        arriba = mezcla((34, 52, 130), (70, 130, 222), u)
        abajo = mezcla((255, 150, 120), (255, 214, 160), u)
        img = F.degradado(t, tuple(v / 255 for v in arriba), tuple(v / 255 for v in abajo))
        return F.estrellas(img, t, 0.5 * (1 - u))
    n = est["negro"]
    arriba = mezcla((26, 40, 104), (5, 7, 24), n)
    abajo = mezcla((70, 92, 168), (20, 18, 50), n)
    abajo = mezcla(abajo, (6, 8, 26), est["aire_helado"])      # sin aire: negro total
    img = F.degradado(t, tuple(v / 255 for v in arriba), tuple(v / 255 for v in abajo))
    return F.estrellas(img, t, 0.25 + 0.75 * n)


# ======================================================================== cámara de la superficie
# claves: (t, Xc, Hc, k): el punto plano (Xc, Hc) cae en el centro de la pantalla con escala k
def _claves_sup():
    return [
        (D1[1], 0, 160, 1.0),
        (A.estrellas + 0.3, 0, 200, 0.95), (A.luna_p - 0.2, 200, 250, 0.9),
        (A.mareas - 0.2, 520, 90, 1.1), (A.frio_p - 0.4, 520, 90, 1.1),
        (A.frio_p + 0.6, 150, -60, 0.62), (A.semana - 0.8, 150, -60, 0.62),
        (A.semana + 0.2, -60, 160, 1.12), (A.cero1 + 0.6, -60, 160, 1.12),
        (A.foto + 0.3, -160, 190, 1.22), (A.cadena + 1.2, -160, 190, 1.22),
        (A.fito - 0.1, 700, -40, 2.1), (A.asfixia - 0.9, 700, -40, 2.1),
        (A.asfixia + 0.1, 150, 290, 0.95), (FIN("vida_sup") + 0.6, 150, 290, 0.95),
        (A.ano - 0.1, -60, 160, 1.12), (A.cero2 + 0.5, -60, 160, 1.12),
        (A.tiempo_atm + 0.4, 200, 300, 0.9), (A.viento + 1.2, 200, 300, 0.9),
        (A.oceanos_f + 0.2, 640, 40, 1.0), (A.manta + 0.8, 640, 40, 1.0),
        (A.debajo + 0.4, 640, -470, 1.0), (A.cientos + 1.4, 640, -470, 1.0),
        (A.dioxido - 0.2, -60, 200, 1.1), (A.nieve + 1.0, -60, 200, 1.1),
        (A.millones_f + 0.4, 0, 230, 0.9), (A.suelo_f + 1.2, 0, 230, 0.9),
        (A.nosotros + 0.8, -440, -330, 0.9), (A.calor_h - 0.4, -440, -330, 0.9),
        (A.calor_h + 1.2, -420, -1650, 0.36), (A.nueve + 1.6, -420, -1650, 0.36),
        (A.paneles - 0.1, -560, -180, 0.82), (A.nucleares + 1.0, -560, -180, 0.82),
        (A.geotermica - 0.2, -430, -650, 1.3), (A.cultivos + 1.8, -430, -650, 1.3),
        (A.oscura - 0.3, -420, -1400, 0.3), (FIN("humanos") + 1.4, -420, -1400, 0.3),
        (A.verdaderos + 0.9, 620, -1020, 0.95), (A.hidro - 0.2, 620, -1020, 0.95),
        (A.hidro + 0.6, 660, -1080, 1.3), (A.gusanos + 2.6, 660, -1080, 1.3),
        (A.pies + 0.6, 700, -2300, 0.62), (A.setenta_p + 2.0, 700, -2300, 0.62),
        (A.noticia - 0.4, 640, -2560, 1.5), (FIN("profundidades") + 0.3, 640, -2560, 1.5),
        (B0, 640, -2800, 1.2), (BM, 640, H_MAGMA - 350, 6.0),
    ]


_CS = _claves_sup()


def cam_superficie(t):
    ts = [c[0] for c in _CS]
    i = int(np.searchsorted(ts, t)) - 1
    if i < 0:
        c = _CS[0]
        Xc, Hc, k = c[1], c[2], c[3]
    elif i >= len(_CS) - 1:
        c = _CS[-1]
        Xc, Hc, k = c[1], c[2], c[3]
    else:
        a, b = _CS[i], _CS[i + 1]
        u = e_inout(prog(t, a[0], b[0]))
        Xc, Hc = lerp(a[1], b[1], u), lerp(a[2], b[2], u)
        k = math.exp(lerp(math.log(a[3]), math.log(b[3]), u))
    kap = 1 / 52000.0 * math.exp(-8 * max(0.0, t - D1[1]))
    return Sup(960 - k * Xc, 540 + k * Hc, k, kap)


def cam_amanecer(t):
    kap = 1 / 52000.0 * math.exp(-8 * max(0.0, t - D2[1]))
    k = 1.0 + 0.05 * prog(t, D2[1], TOTAL)
    return Sup(960.0 - k * 20 * prog(t, D2[1], TOTAL), 700.0 + 60 * (k - 1), k, kap)


# ======================================================================== el paisaje
def paisaje(lz, t, S, est, alfa=1.0, corte=1.0):
    noche, hielo = est["noche"], est["hielo"]

    def tn(c):
        return tinte(c, noche, hielo)

    X = XS
    tp = _taper(X)
    if est["amanecer"] > 0:
        hs = lerp(-40, 330, e_out(prog(t, D2[1] - 0.9, A.gracias + 0.4)))
        x, y = S.pt(-620, hs)
        P.sol(lz, x, y, 88 * S.k, t, brillo=1.0)
    elif est["nubes"] > 0.01 and S.visible_y(700, 200):
        for i in range(5):   # nubes oscuras que se detienen y se disuelven
            v = est["viento"]
            cx_ = -900 + i * 520 + ((A.tiempo_atm - D1[1]) * 22 * (1 - v) + (t - D1[1]) * 22 * v)
            ch = 430 + 60 * (i % 3)
            with S.en(lz, cx_, ch):
                for j in range(3):
                    lz.relleno(elipse((j - 1) * 70, (5 if j != 1 else -20), 90, 42, 0, 30), tn((70, 76, 110)),
                               alfa=0.8 * est["nubes"] * alfa)
    if S.visible_y(260, -120):
        Hf = (80 + 40 * np.sin(X / 260 + 1) + 22 * np.sin(X / 130 + 2.3)) * tp
        lz.relleno(S.poly(np.concatenate([np.stack([X, Hf], 1), [[X[-1], -80], [X[0], -80]]])), tn((120, 190, 182)),
                   alfa=alfa)
        Xm = X[X < 160]
        Hm = (38 + 22 * np.sin(Xm / 200 + 0.4) + 14 * np.sin(Xm / 90)) * _taper(Xm) * (1 - smooth_arr(Xm / 160))
        lz.relleno(S.poly(np.concatenate([np.stack([Xm, Hm], 1), [[160, -80], [Xm[0], -80]]])), tn((88, 174, 136)),
                   alfa=alfa)
    # ---- mar en corte
    marea = 0.0
    if A.mareas - 1.0 < t < A.frio_p + 2.0:
        amp = 22 * (1 - 0.6 * e_inout(prog(t, A.mareas + 0.6, A.mareas + 3.2)))
        marea = amp * math.sin((t - A.mareas) * 1.8) * ventana(t, A.mareas - 0.6, A.frio_p + 1.0, 0.6, 1.0)
    Xa = X[X > 100]
    sup = -8 + marea + (2.5 * np.sin(Xa / 60 + t * 1.6)) * (1 - est["mar"])
    agua = np.concatenate([np.stack([Xa, sup], 1), np.stack([Xa[::-1], fondo_mar(Xa[::-1]) - 40], 1)])
    x0, y0 = S.pt(VENT_X, 0)
    x1, y1 = S.pt(VENT_X, -1250)
    lz.degradado(S.poly(agua), tinte((60, 150, 226), noche * 0.8, 0), (10, 22, 62), (x0, y0), (x1, y1), alfa=corte)
    # fitoplancton
    af = ventana(t, A.fito - 0.3, A.asfixia - 0.6, 0.5, 0.6)
    if af > 0.01:
        vivo = 1 - e_inout(prog(t, A.fito + 1.2, A.fito + 3.8))
        for i in range(60):
            fx = 180 + (i * 97.3) % 1300 + 8 * math.sin(t + i)
            fh = -20 - (i * 53.7) % 170
            with S.en(lz, fx, fh):
                c = mezcla((90, 110, 120), (120, 240, 140), vivo)
                lz.relleno(circulo(0, 0, 5.5, 14), c, alfa=af)
                if vivo > 0.2:
                    lz.halo(0, 0, 14, (120, 255, 150), alfa=0.5 * vivo * af)
    # fondo del mar y roca profunda
    Xf = X[X > 240]
    fm = np.concatenate([np.stack([Xf, fondo_mar(Xf)], 1), [[Xf[-1], -4400], [Xf[0], -4400]]])
    lz.relleno(S.poly(fm), (48, 40, 82), alfa=corte)
    if corte > 0.5 and S.visible_y(-1250, -4400):
        roca_profunda(lz, t, S)
    for i, (rx, rr) in enumerate(((330, 50), (470, 34), (1120, 60), (1260, 40), (1500, 70))):
        with S.en(lz, rx, float(fondo_mar(rx)) - 6):
            lz.relleno(elipse(0, 0, rr * 1.4, rr * 0.8, 0, 32), (66, 54, 100), alfa=corte)
    # ---- suelo en corte (izquierda)
    Xs = X[X < 110]
    tope = suelo_h(Xs)
    suelo = np.concatenate([np.stack([Xs, tope], 1), [[150, -120], [220, -520], [270, -1000], [300, -1300],
                                                      [320, -4400], [Xs[0], -4400]]])
    Ps = S.poly(suelo)
    if corte > 0.004:
        lz.relleno(Ps, tn((118, 84, 76)), alfa=corte)
        with lz.recorte(Ps):
            for h0, h1, c in ((-260, -330, (132, 96, 84)), (-560, -700, (100, 72, 78)), (-900, -960, (124, 90, 86)),
                              (-1150, -1800, (82, 62, 80)), (-1800, -2600, (70, 52, 74)), (-2600, -4400, (60, 44, 66))):
                if S.visible_y(h0, h1):
                    lz.relleno(S.poly([[-4200, h0], [400, h0 - 20], [400, h1], [-4200, h1]]), tn(c), alfa=corte)
            if S.visible_y(-300, -700):
                for i in range(9):
                    px_, ph = -1500 + i * 190 + 40 * math.sin(i * 7.1), -380 - 90 * (i % 4) - 170 * (i % 2)
                    with S.en(lz, px_, ph):
                        lz.relleno(elipse(0, 0, 26 + 8 * (i % 3), 15, 0.3 * i, 20), tn((150, 116, 100)), alfa=corte)
            refugio(lz, t, S, est)
            calor_profundo(lz, t, S)
    pasto = np.concatenate([np.stack([Xs, tope + 4], 1), np.stack([Xs[::-1], tope[::-1] - 30], 1)])
    lz.relleno(S.poly(pasto), tn((70, 158, 102)), alfa=alfa)
    capa_nieve = max(hielo - 0.2, 0) / 0.7 * 16 + est["co2"] * 14
    if capa_nieve > 0.5:
        nv = np.concatenate([np.stack([Xs, tope + 4 + capa_nieve], 1), np.stack([Xs[::-1], tope[::-1] + 2], 1)])
        lz.relleno(S.poly(nv), tinte((236, 244, 255), noche * 0.55, 0), alfa=alfa)
    if est["aire_helado"] > 0.01:   # nitrógeno y oxígeno congelados sobre todo
        g = 34 * est["aire_helado"]
        base = tope + 4 + capa_nieve
        ah = np.concatenate([np.stack([Xs, base + g], 1), np.stack([Xs[::-1], base[::-1]], 1)])
        lz.relleno(S.poly(ah), tinte((170, 196, 255), noche * 0.4, 0), alfa=alfa * 0.95)
    # ---- hielo del mar
    if est["mar"] > 0.005:
        g = 78 * est["mar"]
        hx = np.concatenate([np.stack([Xa, np.full_like(Xa, 6.0)], 1), np.stack([Xa[::-1], np.full_like(Xa, -8 - g)], 1)])
        xa0, ya0 = S.pt(VENT_X, 6)
        xa1, ya1 = S.pt(VENT_X, -8 - g)
        lz.degradado(S.poly(hx), tinte((236, 246, 255), noche * 0.5, 0), tinte((160, 204, 240), noche * 0.5, 0),
                     (xa0, ya0), (xa1, ya1), alfa=corte)
        if est["manta"] > 0:
            col_c = (70, 104, 176)
            for hh in (-8 - g * 0.28, -8 - g * 0.74):
                xs_, ys_ = S.p(np.linspace(150, 1700, 80), np.full(80, hh))
                P.discontinua(lz, np.stack([xs_, ys_], 1), col_c, 5 * S.k, 18 * S.k, 12 * S.k, frac=est["manta"])
            for gx in range(330, 1700, 190):
                P.discontinua(lz, [S.pt(gx, 2), S.pt(gx, -6 - g)], col_c, 5 * S.k, 12 * S.k, 10 * S.k,
                              frac=clamp01(est["manta"] * 1.6 - (gx - 330) / 2600))
    # ---- fumarolas, gusanos, microbios
    if corte > 0.5 and S.visible_y(-600, -1300):
        with S.en(lz, VENT2_X, float(fondo_mar(VENT2_X)) + 4, 0.58):
            P.fumarola(lz, 0, 0, 1.0, t + 3.1, agua=(14, 28, 70))
        with S.en(lz, VENT_X, float(fondo_mar(VENT_X)) + 4, 1.0):
            P.fumarola(lz, 0, 0, 1.0, t, agua=(14, 28, 70))
        ag = pop(t, A.gusanos - 0.5, 0.6)
        if ag > 0.01 and t < B0 + 1:
            for i, gx in enumerate((520, 560, 595, 700, 735, 780, 870, 990)):
                with S.en(lz, gx, float(fondo_mar(gx)) + 2, 0.9 * ag):
                    P.gusano_tubo(lz, 0, 0, 1.0, t, seed=i, alto=0.7 + 0.35 * ((i * 7) % 3) / 2)
        if A.verdaderos - 0.5 < t < B0 + 1.2:
            for i, (mx, mh, forma, col) in enumerate(MICROBIOS):
                k = e_back(prog(t, A.verdaderos + 0.12 * i, A.verdaderos + 0.12 * i + 0.4))
                if k <= 0.01:
                    continue
                with S.en(lz, mx + 12 * math.sin(t * 0.8 + i), mh + 10 * math.sin(t * 1.1 + i * 2), k):
                    P.microbio(lz, 0, 0, 1.1, t, col, seed=i, forma=forma, mirar=(math.sin(t + i), 0.3), brillo=0.55)
    # ---- árboles, flores, animales, pajarito, cosas de la superficie
    if S.visible_y(420, -60):
        for tx, ts in ((-270, 1.05), (-20, 0.8)):
            with S.en(lz, tx, float(suelo_h(tx)) - 2):
                P.arbol(lz, 0, 0, ts, t, perdida=est["perdida"], escarcha=hielo * 0.8, oscuro=noche * 0.62)
        for i, fx in enumerate((-470, -430, -385, -150, -115, 60, 95)):
            with S.en(lz, fx, float(suelo_h(fx)) - 1, 0.8):
                P.planta(lz, 0, 0, 1.0, t, vida=est["flores"], col=tinte((96, 196, 110), noche * 0.5, hielo * 0.5))
        animales(lz, t, S, est)
        pajaro(lz, t, S, est)
        superficie_humana(lz, t, S, est)
        if A.semana - 1.0 < t < A.nosotros + 1.5 and vis_termo(t) > 0.01:
            termometro(lz, t, S, est)
        if est["amanecer"] > 0:
            iconos_amanecer(lz, t, S)
    # ---- nieve (y copos de CO2)
    if est["nieve"] > 0.01 or est["co2"] > 0.01:
        n = int(90 * est["nieve"] + 60 * est["co2"])
        for i in range(n):
            u = (t * (40 + 25 * ((i * 7) % 5)) / 1000 + (i * 0.618) % 1) % 1
            nx = -1000 + (i * 263.7) % 2200 + 30 * math.sin(t * 0.9 + i)
            nh = 1000 - u * 1000
            if nh < suelo_h(nx) + 4 and nx < 120:
                continue
            x, y = S.pt(nx, nh)
            if i % 9 == 0 and est["co2"] > 0.3:
                P.molecula(lz, x, y, 0.35 * S.k, "CO2", rot=t + i)
            else:
                lz.puntos([[x, y]], (2.2 + 1.8 * ((i * 3) % 4) / 3) * S.k, (236, 244, 255))
    # ---- detalles del primer día (Luna fantasma, calor que se escapa, O2)
    extras_primer_dia(lz, t, S, est)


def roca_profunda(lz, t, S):
    """Grietas con microbios bajo el fondo marino y regla de profundidad."""
    for i in range(14):
        x0 = 380 + (i * 131) % 1300
        h0 = -1450 - (i * 347) % 1700
        pts = [(x0, h0)]
        for j in range(6):
            pts.append((pts[-1][0] + 40 * math.sin(i + j * 1.7), pts[-1][1] - 50))
        Pp = np.array([S.pt(a, b) for a, b in pts])
        lz.trazo(Pp, (30, 24, 54), 5 * S.k, afinar=True)
    a = ventana(t, A.pies - 0.3, B0 + 0.8, 0.8, 0.4)
    if a > 0.01:
        for i, (mx, mh, forma, col) in enumerate(PROFUNDOS):
            k = e_back(prog(t, A.pies + 0.05 * i, A.pies + 0.05 * i + 0.4)) * a
            if k <= 0.01:
                continue
            with S.en(lz, mx + 6 * math.sin(t + i), mh, 0.55 * k):
                P.microbio(lz, 0, 0, 1.0, t, col, seed=i + 10, forma=forma, brillo=0.7)
        for j, km in enumerate(("1 km", "2 km", "3 km")):
            h = -1250 - 700 * (j + 1)
            x, y = S.pt(330, h)
            lz.relleno(rect_red(x - 30 * S.k, y - 3, 30 * S.k, 6, 3), (220, 220, 240), alfa=a)
            P.rotulo(lz, x - 40 * S.k, y, km, 34, ancla=(1, 0.5), alfa=a, fuente="geo_n")


def calor_profundo(lz, t, S):
    """Resplandor del interior caliente de la Tierra (abajo del todo) y la bolsa de roca caliente."""
    if S.visible_y(-2300, -4400):
        x0, y0 = S.pt(0, H_MAGMA + 500)
        x1, y1 = S.pt(0, -4400)
        lz.degradado(S.poly([[-4200, H_MAGMA + 500], [4200, H_MAGMA + 500], [4200, -4400], [-4200, -4400]]),
                     (70, 44, 66), (255, 120, 50), (x0, y0), (x1, y1))
        for i in range(10):
            xx = -1400 + i * 300 + 60 * math.sin(t * 0.5 + i)
            x, y = S.pt(xx, H_MAGMA - 200)
            lz.halo(x, y, 260 * S.k, (255, 140, 60), alfa=0.35)
    # roca caliente bajo el refugio (energía geotérmica)
    if S.visible_y(-2300, -3000):
        x, y = S.pt(-430, -2650)
        lz.halo(x, y, 420 * S.k, (255, 120, 60), alfa=0.55)
        lz.relleno(elipse(x, y, 260 * S.k, 110 * S.k, 0, 40), (255, 130, 70))
        lz.relleno(elipse(x - 40 * S.k, y - 20 * S.k, 150 * S.k, 55 * S.k, 0, 30), (255, 190, 110))
    a = ventana(t, A.calor_h - 0.2, A.poquisimo + 0.6, 0.5, 0.6)
    if a > 0.01:   # flechas de calor que suben
        for i in range(7):
            xx = -1200 + i * 360
            f = ((t * 0.3 + i * 0.37) % 1)
            x0_, y0_ = S.pt(xx, H_MAGMA + 300 + f * 2600)
            lz.trazo(np.array([[x0_, y0_ + 120 * S.k], [x0_, y0_]]), (255, 150, 80), 8 * S.k, afinar=False)
            lz.relleno(np.array([[x0_ - 16 * S.k, y0_ + 6], [x0_ + 16 * S.k, y0_ + 6], [x0_, y0_ - 22 * S.k]]),
                       (255, 150, 80), alfa=a)


def refugio(lz, t, S, est):
    """Refugio subterráneo: sala con personas, invernadero con luz artificial, reactor y tubo geotérmico."""
    a = ventana(t, A.nosotros - 0.6, B0, 0.9, 0.3)
    if a <= 0.01 or not S.visible_y(0, -2700):
        return
    # pozo de acceso desde la superficie
    lz.relleno(S.poly([[-470, 0], [-420, 0], [-420, -520], [-470, -520]]), (36, 28, 44), alfa=a)
    salas = [(-780, -540, -520, -760, (255, 196, 120)),     # vivienda
             (-500, -540, -250, -760, (255, 120, 200)),     # invernadero (LED)
             (-760, -800, -300, -960, (130, 200, 255))]     # reactor
    for x0, h0, x1, h1, luz in salas:
        Pp = S.poly([[x0, h0], [x1, h0], [x1, h1], [x0, h1]])
        lz.relleno(Pp, (30, 24, 40), alfa=a)
        cx, cy = S.pt((x0 + x1) / 2, (h0 + h1) / 2)
        with lz.recorte(Pp):
            lz.halo(cx, cy, 260 * S.k, luz, alfa=0.55 * a)
    # personas en la vivienda
    for i, px_ in enumerate((-730, -660, -590)):
        with S.en(lz, px_ + 20 * math.sin(t * 0.4 + i), -760, 0.62):
            P.humano(lz, 0, 0, 1.0, t, ropa=[(92, 142, 232), (236, 120, 90), (120, 200, 140)][i], paso=0.4,
                     voltear=i == 1)
    # invernadero
    with S.en(lz, -375, -560):
        lz.relleno(rect_red(-110, -6, 220, 12, 4), (255, 150, 220), alfa=a)
    for i, px_ in enumerate((-470, -430, -390, -350, -310, -270)):
        with S.en(lz, px_, -760, 0.9):
            P.planta(lz, 0, 0, 1.0, t, vida=1.0, col=(120, 220, 130))
    # reactor
    x, y = S.pt(-530, -880)
    lz.halo(x, y, 120 * S.k, (130, 220, 255), alfa=0.8 * a)
    lz.relleno(circulo(x, y, 30 * S.k, 30), (220, 245, 255), alfa=a)
    # tubo geotérmico hasta la roca caliente
    tubo = S.poly([[-450, -960], [-410, -960], [-410, -2600], [-450, -2600]])
    lz.relleno(tubo, (150, 150, 170), alfa=a)
    ag = ventana(t, A.geotermica - 0.3, B0, 0.4, 0.3)
    if ag > 0.01:
        for i in range(8):
            f = ((t * 0.45 + i / 8) % 1)
            x, y = S.pt(-430, -2600 + f * 1640)
            lz.relleno(circulo(x, y, 9 * S.k, 16), (255, 150, 80), alfa=ag)
    ar = ventana(t, A.geotermica - 0.2, A.oscura - 0.4, 0.3, 0.4)
    if ar > 0.01:
        for txt, (X0, H0) in (("geotérmica", (-430, -1300)), ("reactor", (-530, -1000)),
                              ("luz artificial", (-375, -500))):
            x, y = S.pt(X0, H0)
            P.pastilla(lz, x, y, txt, 30, k=ar)


def superficie_humana(lz, t, S, est):
    """Paneles solares apagados y central nuclear (sección humanos)."""
    a = ventana(t, A.nosotros - 0.5, B0, 0.6, 0.3)
    if a <= 0.01:
        return
    with S.en(lz, -900, float(suelo_h(-900)), 0.9):
        P.panel_solar(lz, 0, 0, 1.0, activo=0.0)
        k = pop(t, A.paneles + 0.2)
        if k > 0.01:
            lz.trazo(np.array([[-70, -140], [70, 0]]), (255, 90, 90), 14 * k, afinar=False)
            lz.trazo(np.array([[70, -140], [-70, 0]]), (255, 90, 90), 14 * k, afinar=False)
    with S.en(lz, -620, float(suelo_h(-620)), 0.7):
        P.central_nuclear(lz, 0, 0, 1.0, t, activa=pop(t, A.nucleares - 0.2))
    with S.en(lz, -445, float(suelo_h(-445)), 0.8):   # caseta del pozo
        lz.relleno(rect_red(-40, -60, 80, 60, 6), (120, 116, 140))
        lz.relleno(rect_red(-16, -44, 32, 44, 4), (255, 196, 120) if t > A.nosotros else (60, 60, 80))


def animales(lz, t, S, est):
    if est["amanecer"] > 0 or t > A.oxigeno + 2:
        return
    a = ventana(t, A.plantas - 1.5, A.cadena + 1.0, 0.6, 0.6)
    if a <= 0.01:
        return
    # el conejo busca comida; el zorro lo sigue
    xc = lerp(-480, -360, e_inout(prog(t, A.animales, A.animales + 2.0)))
    salto = 18 * abs(math.sin((t - A.animales) * 6)) * ventana(t, A.animales, A.animales + 2.0, 0.1, 0.1)
    triste = prog(t, A.animales + 1.0, A.animales + 1.6)
    with S.en(lz, xc, float(suelo_h(xc)), 0.85):
        P.conejo(lz, 0, 0, 1.0, t, col=tinte((196, 184, 178), est["noche"] * 0.45, est["hielo"] * 0.4), salto=salto)
    kz = pop(t, A.despues - 0.2)
    if kz > 0.01:
        with S.en(lz, -610, float(suelo_h(-610)), 0.8 * kz):
            P.zorro(lz, 0, 0, 1.0, t)


def pajaro(lz, t, S, est):
    X0 = -145.0
    if est["amanecer"] > 0:
        feliz = 1.0 if t > A.gracias - 0.05 else 0.0
        aleteo = 0.5 + 0.5 * math.sin((t - A.gracias) * 14) if A.gracias < t < A.gracias + 1.4 else 0.0
        salto = 16 * abs(math.sin((t - A.gracias) * 7)) * (1 - prog(t, A.gracias, A.gracias + 1.2)) if t > A.gracias else 0
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
    if t > A.millones_f + 1.0:      # millones de años después ya no hay pajarito
        return
    col = tinte((128, 90, 216), est["noche"] * 0.45, 0)
    mirar = (0.3, -1.0) if t < A.semana else (0.2, 0.2)
    tiritar = prog(t, A.semana, A.semana + 0.6)
    salida = e_in(prog(t, A.nieve, A.millones_f + 0.8))
    with S.en(lz, X0 - 400 * salida, float(suelo_h(X0))):
        P.pajaro(lz, 0, 0, 0.95, t, color=col, mirar=mirar, tiritar=tiritar, escarcha=est["hielo"])


def termometro(lz, t, S, est):
    temp = temperatura(t)
    a = vis_termo(t)
    if a <= 0.01:
        return
    nivel = clamp01((temp + 90) / 170)
    with S.en(lz, -640, -118, 0.72 * (0.7 + 0.3 * a)):
        P.termometro(lz, 0, 0, 1.0, nivel, col=mezcla((255, 110, 90), (120, 190, 255), prog(-temp, -5, 60)))
    x, y = S.pt(-585, 380)
    txt = f"{int(round(temp))} °C".replace("-", "−")
    P.rotulo(lz, x, y, txt, 72 * S.k, k=a, ancla=(0, 0.5), capa=1)
    if t < A.ano - 0.6:
        etiqueta, t0 = "1 SEMANA", A.semana
    elif t < A.dioxido - 0.4:
        etiqueta, t0 = "1 AÑO", A.ano
    elif t < A.millones_f:
        etiqueta, t0 = "MÁS TARDE", A.dioxido - 0.4
    else:
        etiqueta, t0 = "MILLONES DE AÑOS", A.millones_f
    ae = prog(t, t0, t0 + 0.3)
    P.rotulo(lz, x + 4, y + 62 * S.k, etiqueta, 34 * S.k, k=a * (0.6 + 0.4 * ae), ancla=(0, 0.5), fuente="geo_n",
             alfa=ae, capa=1)


def vis_termo(t):
    return max(ventana(t, A.semana - 0.6, A.foto - 0.8, 0.5, 0.5), ventana(t, A.ano - 0.7, A.nosotros + 0.2, 0.5, 0.8))


def extras_primer_dia(lz, t, S, est):
    # reloj de mediodía en el cielo
    a = ventana(t, A.mediodia - 0.3, A.luna_p - 0.4, 0.3, 0.4)
    if a > 0.01:
        x, y = S.pt(-60, 520)
        P.pastilla(lz, x, y, "12:00 · mediodía", 40, k=a)
    # Luna fantasma
    a = ventana(t, A.luna_p - 0.2, A.mareas - 0.6, 0.4, 0.5)
    if a > 0.01:
        x, y = S.pt(420, 470)
        P.discontinua(lz, P.arco_pts(x, y, 70 * S.k, 0, 2 * np.pi, 120), mezcla((10, 10, 30), (170, 170, 220), a), 4, 14,
                      12, fase=t * 10)
        P.rotulo(lz, x, y + 110 * S.k, "Luna: sin luz que reflejar", 32, fuente="geo_n", alfa=a, color=(200, 200, 240))
    # mareas
    a = ventana(t, A.mareas - 0.2, A.frio_p - 0.6, 0.3, 0.4)
    if a > 0.01:
        x, y = S.pt(900, 150)
        P.rotulo(lz, x, y, "mareas más débiles", 40, alfa=a)
    # calor guardado que se escapa
    a = ventana(t, A.frio_p - 0.3, A.semana - 0.4, 0.5, 0.6)
    if a > 0.01:
        u = prog(t, A.frio_p, A.semana)
        for txt, (X0, H0), (Xl, Hl) in (("suelo", (-400, -300), (-400, -300)), ("aire", (-200, 240), (-200, 240)),
                                        ("océanos", (700, -500), (700, -500))):
            x, y = S.pt(X0, H0)
            lz.halo(x, y, 360 * S.k, (255, 140, 70), alfa=0.55 * a * (1 - 0.6 * u))
            P.rotulo(lz, x, y, txt, 40, alfa=a, color=(255, 214, 170))
    # árboles: aguantan décadas; fitoplancton
    a = ventana(t, A.decadas - 0.2, A.animales - 0.4, 0.3, 0.4)
    if a > 0.01:
        x, y = S.pt(-270, 400)
        P.pastilla(lz, x, y, "décadas", 38, k=a)
    a = ventana(t, A.fito - 0.1, A.asfixia - 0.8, 0.3, 0.4)
    if a > 0.01:
        x, y = S.pt(700, 60)
        P.pastilla(lz, x, y, "fitoplancton", 38, k=a, fondo=(150, 250, 170))
    # oxígeno para miles de años
    a = ventana(t, A.asfixia - 0.2, FIN("vida_sup") + 1.2, 0.4, 0.5)
    if a > 0.01:
        for i in range(12):
            ox = -700 + (i * 173) % 1600 + 30 * math.sin(t * 0.7 + i)
            oh = 250 + (i * 71) % 300 + 20 * math.sin(t * 0.9 + i * 2)
            x, y = S.pt(ox, oh)
            P.molecula(lz, x, y, 0.55 * S.k * pop(t, A.asfixia + 0.05 * i), "O2", rot=0.3 * math.sin(t + i))
        x, y = S.pt(150, 620)
        P.pastilla(lz, x, y, "oxígeno para miles de años", 36, k=pop(t, A.oxigeno - 0.1))
    # "líquida durante cientos de miles de años"
    a = ventana(t, A.debajo - 0.1, A.dioxido - 1.0, 0.4, 0.5)
    if a > 0.01:
        x, y = S.pt(VENT_X, -420)
        P.rotulo(lz, x, y, "AGUA LÍQUIDA", 56 * S.k, alfa=a)
        x, y = S.pt(VENT_X, -520)
        P.rotulo(lz, x, y, "cientos de miles de años", 34 * S.k, alfa=a * prog(t, A.cientos - 0.2, A.cientos + 0.4),
                 fuente="geo_n", color=(190, 220, 255))
    # rótulos del aire congelado
    a = ventana(t, A.dioxido - 0.1, A.millones_f - 0.4, 0.3, 0.4)
    if a > 0.01:
        x, y = S.pt(200, 520)
        P.rotulo(lz, x, y, "nieve de CO2 · −78 °C", 42, alfa=a)
    a = ventana(t, A.nitrogeno - 0.2, FIN("frio") + 1.5, 0.4, 0.6)
    if a > 0.01:
        x, y = S.pt(200, 520)
        P.rotulo(lz, x, y, "nitrógeno y oxígeno congelados", 42, alfa=a, color=(200, 220, 255))
    # vida muy oscura
    # (el zoom hacia fuera lo cuenta; sin rótulo)


def iconos_amanecer(lz, t, S):
    """Comida, aire y clima: todo funciona con luz del Sol."""
    xs, ys = S.pt(-620, lerp(-40, 330, e_out(prog(t, D2[1] - 0.9, A.gracias + 0.4))))
    for i, (tt, txt, (X0, H0)) in enumerate(((A.comida, "comida", (-40, 520)), (A.aire_c, "aire", (220, 600)),
                                             (A.clima, "clima", (480, 520)))):
        k = pop(t, tt - 0.1) * (1 - e_in(prog(t, A.manana - 0.4, A.manana + 0.1)))
        if k <= 0.01:
            continue
        x, y = S.pt(X0, H0)
        P.discontinua(lz, [(xs, ys), (x, y)], (255, 226, 160), 3, 14, 10, fase=-t * 40, frac=min(1, k))
        with lz.grupo(x, y, k):
            lz.relleno(circulo(0, 0, 58, 40), (255, 255, 255), alfa=0.9)
            if i == 0:
                P.planta(lz, 0, 34, 0.9, t, vida=1.0, col=(110, 190, 90))
            elif i == 1:
                P.molecula(lz, 0, 0, 0.9, "O2")
            else:
                for j in range(3):
                    lz.relleno(elipse((j - 1) * 20, 6 if j != 1 else -4, 22, 14, 0, 20), (130, 170, 230))
        P.rotulo(lz, x, y + 86 * k, txt, 34, alfa=min(1, k))


# ======================================================================== interfaz de la superficie
def ui_superficie(lz, t):
    # cadena alimentaria que se derrumba
    a = ventana(t, A.animales - 0.3, A.fito - 0.6, 0.4, 0.5)
    if a > 0.01:
        cx, cy = 960, 190
        cae = e_in(prog(t, A.cadena, A.cadena + 1.2))
        for i, nom in enumerate(("planta", "conejo", "zorro")):
            x = cx + (i - 1) * 260
            rot = cae * (0.9 + 0.2 * i) * (1 if i % 2 else -1)
            dy = cae * 220 * (0.6 + 0.3 * i)
            with lz.capa(2):
                with lz.grupo(x, cy + dy, 1.0, rot):
                    lz.relleno(circulo(0, 0, 74, 40), (255, 255, 255), alfa=a * 0.92)
                    if nom == "planta":
                        P.planta(lz, 0, 40, 1.0, t, vida=1 - 0.8 * prog(t, A.plantas, A.plantas + 1.5))
                    elif nom == "conejo":
                        P.conejo(lz, 4, 42, 0.8, t)
                    else:
                        P.zorro(lz, 0, 40, 0.62, t)
            if i < 2 and cae < 0.5:
                with lz.capa(2):
                    aa = a * (1 - 2 * cae)
                    lz.relleno(rect_red(x + 96, cy - 5, 44, 10, 5), (255, 255, 255), alfa=aa)
                    lz.relleno(np.array([[x + 136, cy - 18], [x + 164, cy], [x + 136, cy + 18]]), (255, 255, 255), alfa=aa)
    # 3 700 veces más energía
    a = ventana(t, A.poquisimo - 0.2, A.islandia - 0.5, 0.4, 0.4)
    if a > 0.01:
        k = pop(t, A.tres - 0.3)
        with lz.capa(2):
            lz.relleno(rect_red(300, 200, 1320, 660, 40), (12, 12, 36), alfa=0.78 * a)
            lz.halo(700, 470, 330 * k, (255, 200, 90), alfa=0.6 * a)
            lz.relleno(circulo(700, 470, 230 * k, 90), (255, 206, 96), alfa=a)
            lz.halo(1300, 470, 30, (255, 130, 60), alfa=a)
            lz.relleno(circulo(1300, 470, 3.8, 12), (255, 150, 80), alfa=a)
        P.rotulo(lz, 700, 470, "energía del Sol", 40, alfa=a * k, color=(90, 40, 10), sombra=0)
        P.rotulo(lz, 1300, 520, "calor interno de la Tierra", 34, alfa=a, fuente="geo_n")
        P.rotulo(lz, 1000, 780, "≈ 3 700 veces más", 48, alfa=a * k)
    # Islandia: 9 de cada 10 casas
    a = ventana(t, A.islandia - 0.2, A.paneles - 0.4, 0.4, 0.4)
    if a > 0.01:
        with lz.capa(2):
            lz.relleno(rect_red(150, 270, 1620, 360, 40), (12, 12, 36), alfa=0.78 * a)
        for i in range(10):
            x = 960 + (i - 4.5) * 150
            k = pop(t, A.nueve - 0.4 + 0.06 * i)
            if k <= 0.01:
                continue
            with lz.capa(2):
                P.casa(lz, x, 560, 0.95 * k, calor=1.0 if i < 9 else 0.0, oscuro=0.0 if i < 9 else 0.4)
        P.rotulo(lz, 960, 330, "Islandia: 9 de cada 10 casas", 48, alfa=a)
        P.rotulo(lz, 960, 390, "se calientan con el calor de la Tierra", 34, fuente="geo_n", alfa=a)
    # 70 % de las bacterias y arqueas
    a = ventana(t, A.setenta_p - 0.3, A.noticia - 0.4, 0.4, 0.4)
    if a > 0.01:
        P.pastilla(lz, 960, 170, "≈ 70 % de las bacterias y arqueas viven bajo tierra", 36, k=a)


def ui_noticia(lz, t, S):
    a = ventana(t, A.noticia - 0.2, B0 + 0.3, 0.3, 0.3)
    if a <= 0.01:
        return
    mx, mh = PROFUNDOS[0][0], PROFUNDOS[0][1]
    x, y = S.pt(640, -2560)
    k = pop(t, A.noticia - 0.1)
    with lz.capa(2):
        with lz.grupo(x, y, S.k / 1.5):
            P.microbio(lz, 0, 0, 1.6, t, (120, 232, 150), seed=3, forma=1, brillo=0.8)
            with lz.grupo(90, -120, k):
                lz.relleno(elipse(0, 0, 120, 58, 0, 40), (255, 255, 255))
                lz.relleno(np.array([[-40, 40], [-70, 80], [-10, 48]]), (255, 255, 255))
                lz.texto("¿el Sol?", 0, 0, 40, "geo", color=(40, 30, 80), borde=None, temblor=0.0)
