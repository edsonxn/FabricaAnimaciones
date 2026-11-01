# -*- coding: utf-8 -*-
"""El paisaje continuo (coordenadas planas X a la derecha, H hacia arriba; 1 unidad ≈ 1 px a k = 1):
montaña de 2 000 m (izq.) · parque con estanque, asador y gente · pueblo con carretera, semáforos y edificios ·
torres de luz y central térmica · costa con muelle · mar en corte hasta el fondo. Bajo el suelo, estratos de roca.
Capas lejanas con paralaje: Sol, nubes, cordillera, cerros con bosque (incendio) y lomas.
El estado (est) dice qué está encendido, qué se ha destruido (versión B) y qué ha desaparecido."""
import math

import numpy as np

import plano as P
from plano import mezcla, aclarar, oscurecer
from motor import W, H, prog, clamp01, lerp, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, smooth, catmull, h01
from mundo_comun import Sup, pop, ventana, campana, smooth_arr
from anclas import A
from estado import T_FUEGO, T_RED, T_B
import kit_oxi as KO

XS = np.arange(-5400, 5800, 40.0)
X_COSTA = 2330.0
X_MONTE = -3350.0
H_MONTE = 1500.0
C_CIELO = ((70, 138, 228), (176, 216, 250))
C_CIELO_B = ((92, 64, 110), (214, 150, 140))


# ======================================================================== relieve
def _mont(X, relieve=1.0, hundir=0.0):
    X = np.asarray(X, float)
    m = (H_MONTE * np.exp(-((X - X_MONTE) / 560) ** 2) + 820 * np.exp(-((X + 4350) / 480) ** 2)
         + 360 * np.exp(-((X + 2650) / 300) ** 2))
    return m * relieve * (1 - 0.45 * hundir)


def suelo_h(X, relieve=1.0, hundir=0.0):
    """Altura del suelo firme (también bajo el mar, donde es el fondo)."""
    X = np.asarray(X, float)
    parque = (7 * np.sin(X / 150) + 4 * np.sin(X / 61 + 1)) * np.clip((-350 - X) / 200, 0, 1)
    playa = -26 * smooth_arr((X - 2130) / 220)
    hondo = -1474 * smooth_arr((X - X_COSTA) / 1050) + 40 * np.sin(X / 230) * smooth_arr((X - 2800) / 600)
    base = _mont(X, relieve, hundir) + parque + playa + hondo
    tierra = X < X_COSTA + 300
    if hundir > 0:
        base = base - np.where(tierra, hundir * (70 + 22 * np.sin(X / 97) + 12 * np.sin(X / 37)), 0.0)
    return base


def fondo_mar(X):
    return suelo_h(X)


# ======================================================================== cielo y capas lejanas
def cielo(t, est):
    import fondos as F
    b = est.get("cielo_b", 0.0)
    arr = mezcla(C_CIELO[0], C_CIELO_B[0], b)
    aba = mezcla(C_CIELO[1], C_CIELO_B[1], b)
    vb = est.get("vuelta_b", 0.0)
    if vb > 0:
        f = vb * (0.6 + 0.4 * math.sin(t * 9))
        aba = mezcla(aba, (255, 170, 110), 0.5 * f)
    return F.degradado(t, tuple(v / 255 for v in arr), tuple(v / 255 for v in aba))


def sol_paisaje(lz, t, S):
    Ss = S.par(0.04)
    x, y = Ss.pt(SOL_X, SOL_H)
    r = 2250 * Ss.k
    if -r * 4 < x < W + r * 4 and -r * 4 < y < H + r * 4:
        P.sol(lz, x, y, r, t)
    return x, y, r


SOL_X, SOL_H = 900.0, 24000.0
_NUBES = [(-7000, 2300, 1.3), (-4800, 2700, 1.0), (-2600, 2200, 1.5), (-300, 2600, 1.1), (2000, 2350, 1.4),
          (4300, 2750, 1.0), (6500, 2250, 1.2), (8600, 2600, 1.1), (11000, 2400, 1.3)]


def nubes(lz, t, S, est):
    a = 1 - est.get("hidro", 0.0) * 0.85
    if a <= 0.02:
        return
    Sn = S.par(0.3)
    colb = mezcla((255, 255, 255), (236, 200, 210), est.get("cielo_b", 0.0))
    for i, (nx, nh, s) in enumerate(_NUBES):
        X = nx + 26 * t
        x, y = Sn.pt(X, nh)
        if -500 < x < W + 500 and -300 < y < H + 200:
            with Sn.en(lz, X, nh, s * 3.2):
                KO.nube(lz, 0, 0, 1.0, colb, alfa=a, seed=i)


_XL = np.arange(-14000, 14000, 120.0)
_CORD = (1500 + 520 * np.sin(_XL / 900) + 380 * np.sin(_XL / 410 + 1.3) + 220 * np.sin(_XL / 190 + 0.4))


def capas_lejanas(lz, t, S, est):
    b = est.get("b", 0.0)
    hund = est.get("hundir", 0.0)
    # cordillera (paralaje 0.2)
    Sc = S.par(0.2)
    alt = _CORD * (1 - 0.35 * hund)
    col = mezcla((168, 198, 236), (170, 130, 150), b)
    lz.relleno(Sc.poly(np.concatenate([np.stack([_XL, alt], 1), [[_XL[-1], -600], [_XL[0], -600]]])), col)
    nieve = np.stack([_XL, np.maximum(alt - 230, 1650)], 1)
    top = np.stack([_XL[::-1], alt[::-1]], 1)
    msk = alt > 1880
    if msk.any() and hund < 0.5:
        lz.relleno(Sc.poly(np.concatenate([nieve, top])), mezcla((236, 244, 255), (200, 170, 190), b),
                   alfa=0.0)   # (se deja la cumbre lisa: la nieve se pinta abajo)
    for i in range(-30, 30):
        xi = i * 470 + 120 * math.sin(i * 1.7)
        hi = 1500 + 520 * math.sin(xi / 900) + 380 * math.sin(xi / 410 + 1.3) + 220 * math.sin(xi / 190 + 0.4)
        if hi > 1900 and hund < 0.6:
            hi *= (1 - 0.35 * hund)
            lz.relleno(Sc.poly([[xi - 170, hi - 210], [xi, hi + 6], [xi + 170, hi - 210], [xi + 60, hi - 170], [xi - 50, hi - 230]]),
                       mezcla((240, 246, 255), (210, 180, 200), b))
    # cerros con bosque (paralaje 0.42) y el incendio forestal
    Sb = S.par(0.42)
    hb = (560 + 200 * np.sin(_XL / 520 + 2) + 120 * np.sin(_XL / 230)) * (1 - 0.4 * hund)
    colb = mezcla((128, 186, 196), (160, 120, 140), b)
    lz.relleno(Sb.poly(np.concatenate([np.stack([_XL, hb], 1), [[_XL[-1], -600], [_XL[0], -600]]])), colb)
    x0, x1 = Sb.rango_x(300)
    vida = est.get("vida_resto", 1.0)
    for i in range(int(max(x0, -14000) // 90), int(min(x1, 14000) // 90)):
        xi = i * 90 + 30 * math.sin(i * 2.3)
        hi = 560 + 200 * math.sin(xi / 520 + 2) + 120 * math.sin(xi / 230)
        hi *= (1 - 0.4 * hund)
        s = 0.9 + 0.4 * h01(i, 3)
        if vida > 0.02:
            with Sb.en(lz, xi, hi - 30 - 60 * h01(i, 5), s * 2.2):
                lz.relleno(np.array([[-22, 0], [0, -70], [22, 0]]), mezcla(mezcla((96, 160, 160), (150, 110, 130), b), colb, 0.2),
                           alfa=vida)
    incendio(lz, t, Sb, est)
    # lomas cercanas (paralaje 0.68)
    Sl = S.par(0.68)
    hl = (190 + 80 * np.sin(_XL / 340 + 0.7) + 40 * np.sin(_XL / 140)) * (1 - 0.5 * hund)
    lz.relleno(Sl.poly(np.concatenate([np.stack([_XL, hl], 1), [[_XL[-1], -600], [_XL[0], -600]]])),
               mezcla((112, 190, 160), (150, 116, 130), b))
    x0, x1 = Sl.rango_x(200)
    for i in range(int(max(x0, -14000) // 160), int(min(x1, 14000) // 160)):
        xi = i * 160 + 50 * math.sin(i * 1.3)
        hi = (190 + 80 * math.sin(xi / 340 + 0.7) + 40 * math.sin(xi / 140)) * (1 - 0.5 * hund)
        if vida > 0.02:
            with Sl.en(lz, xi, hi - 12, 1.25 + 0.3 * h01(i, 7)):
                lz.relleno(circulo(0, -40, 34, 20), mezcla(mezcla((86, 168, 130), (140, 104, 120), b), (112, 190, 160), 0.1), alfa=vida)
                lz.relleno(rect_red(-4, -14, 8, 16, 3), (96, 120, 120), alfa=vida)


INC_X = 260.0


def incendio(lz, t, Sb, est):
    """Incendio forestal en los cerros (capa 0.42): llamas que se apagan en T_FUEGO y humo que se disipa."""
    if not (-1e9 < Sb.pt(INC_X, 0)[0] < 1e9):
        return
    x, _ = Sb.pt(INC_X, 0)
    if x < -600 or x > W + 600:
        return
    hb = lambda X: (560 + 200 * math.sin(X / 520 + 2) + 120 * math.sin(X / 230)) * (1 - 0.4 * est.get("hundir", 0.0))
    f = est["fuego"] if not est.get("normal") else 0.0   # en el cierre no hay incendio
    if est.get("normal"):
        return
    # mancha quemada
    with Sb.en(lz, INC_X, hb(INC_X) - 40, 1.2):
        lz.relleno(elipse(0, 0, 150, 40, 0.05, 30), (90, 80, 96), alfa=0.6)
    # humo oscuro
    if f > 0.02:
        with Sb.en(lz, INC_X, hb(INC_X), 1.2):
            KO.columna_humo(lz, 0, -60, 1.0, t, col=(120, 110, 124), n=9, vel=0.18, ancho=0.8, alfa=0.55 * f, viento=60,
                            alto=330)
    with Sb.en(lz, INC_X, hb(INC_X), 1.2):
        KO.humo(lz, 0, -60, 1.4, t, T_FUEGO, dur=3.4, col=(150, 140, 150), n=7, alfa=0.6, sube=200)
    for k in range(9):
        Xk = INC_X - 200 + k * 50
        with Sb.en(lz, Xk, hb(Xk) - 20 - 18 * (k % 3), 1.2):
            KO.llama(lz, 0, 0, 0.6 + 0.25 * (k % 2), t, k, f)


# ======================================================================== suelo, estratos, mar
ESTRATOS = [(-40, -150, (150, 104, 84)), (-150, -170, (170, 120, 96)), (-170, -420, (132, 92, 82)),
            (-420, -450, (156, 112, 94)), (-450, -900, (112, 80, 84)), (-900, -1500, (96, 70, 84)),
            (-1500, -2600, (80, 58, 78))]


def terreno(lz, t, S, est, rel=1.0):
    b, hund, polvo = est.get("b", 0.0), est.get("hundir", 0.0), est.get("polvo", 0.0)
    x0, x1 = S.rango_x(300)
    m = (XS >= x0 - 80) & (XS <= x1 + 80)
    X = XS[m] if m.sum() > 2 else XS
    top = suelo_h(X, rel, hund)
    fondo = -2600.0
    if DELGADO[0]:   # zoom hacia el planeta: solo una franja fina de superficie (sin el corte del subsuelo)
        base = np.minimum(top, 0.0) - 70
        lz.relleno(S.poly(np.concatenate([np.stack([X, top], 1), np.stack([X[::-1], base[::-1]], 1)])),
                   mezcla((96, 184, 112), (150, 126, 120), b))
        mm = top > 120   # la montaña, de roca
        if mm.sum() > 2:
            Xm, Tm = X[mm], top[mm]
            lz.relleno(S.poly(np.concatenate([np.stack([Xm, Tm], 1), np.stack([Xm[::-1], np.full(mm.sum(), 60.0)], 1)])),
                       mezcla((150, 136, 172), (170, 130, 140), b))
        return
    Pt = S.poly(np.concatenate([np.stack([X, top], 1), [[X[-1], fondo], [X[0], fondo]]]))
    lz.relleno(Pt, mezcla((122, 88, 80), (110, 80, 90), b))
    with lz.recorte(Pt):
        ref = np.minimum(top, 0.0)
        ond = 24 * np.sin(X / 300)
        for h0, h1, c in ESTRATOS:
            if S.vis(x0, x1, float(ref.min()) + h1 - 40, h0 + 60):
                lz.relleno(S.poly(np.concatenate([np.stack([X, ref + h0 + ond], 1), np.stack([X[::-1], (ref + h1 + ond)[::-1]], 1)])),
                           mezcla(c, (150, 120, 120), 0.25 * b))
        # la montaña: roca violácea con cara iluminada, bosque abajo y nieve arriba
        if S.vis(-4900, -2200, 0, 1600):
            mm = (X > -5000) & (X < -2150)
            if mm.sum() > 2:
                Xm, Tm = X[mm], top[mm]
                lz.relleno(S.poly(np.concatenate([np.stack([Xm, Tm + 2], 1), np.stack([Xm[::-1], np.full(mm.sum(), 30.0)], 1)])),
                           mezcla((150, 136, 172), (170, 130, 140), b))
                cara = np.where(np.gradient(Tm) > 0, Tm + 2, np.maximum(30, Tm - 260))
                lz.relleno(S.poly(np.concatenate([np.stack([Xm, Tm + 2], 1), np.stack([Xm[::-1], cara[::-1]], 1)])),
                           mezcla((176, 164, 200), (190, 150, 160), b), alfa=0.8)
                for i in range(9):   # aristas de roca
                    xr = X_MONTE - 900 + i * 230
                    hr = float(suelo_h(xr, rel, hund))
                    if hr > 200:
                        lz.relleno(S.poly([[xr, hr], [xr + 50, hr - 20], [xr + 140, hr - 420], [xr + 60, hr - 380]]),
                                   mezcla((128, 116, 156), (150, 116, 130), b), alfa=0.55)
                nieve_h = 1060 - 400 * hund
                Ns = np.maximum(Tm + 3, nieve_h)
                if (Tm > nieve_h).any() and hund < 0.8:
                    zig = nieve_h + 40 * np.abs(np.sin(Xm / 60))
                    lz.relleno(S.poly(np.concatenate([np.stack([Xm, Ns], 1), np.stack([Xm[::-1], np.minimum(Ns, zig)[::-1]], 1)])),
                               mezcla((246, 250, 255), (220, 196, 206), b))
        # piel de pasto sobre la tierra firme
        mt = (X < X_COSTA - 160) & (top < 420)
        cortes = np.flatnonzero(np.diff(mt.astype(int)) != 0) + 1
        for seg in np.split(np.arange(len(X)), cortes):
            if len(seg) < 3 or not mt[seg[0]]:
                continue
            Xt, Tt = X[seg], top[seg]
            lz.relleno(S.poly(np.concatenate([np.stack([Xt, Tt + 2], 1), np.stack([Xt[::-1], Tt[::-1] - 22], 1)])),
                       mezcla((96, 184, 112), (150, 126, 120), b))
        # piedras
        if S.vis(x0, x1, -1500, -150):
            for i in range(int(max(x0, -5400) // 110), int(min(x1, 5800) // 110)):
                px = i * 110 + 40 * math.sin(i * 7.1)
                tp = float(suelo_h(px, rel, hund))
                ph = min(tp, 0.0) - 200 - 130 * ((i * 37) % 7) - 90 * (i % 2)
                if not S.vis(px - 40, px + 40, ph - 30, ph + 30):
                    continue
                with S.en(lz, px, ph):
                    lz.relleno(elipse(0, 0, 26 + 10 * (i % 3), 15, 0.3 * i, 20), mezcla((166, 128, 112), (170, 140, 140), b),
                               alfa=1 - 0.6 * polvo)
        tunel_metro(lz, t, S, est)
        if polvo > 0.01 and S.vis(x0, min(x1, 2600), -1200, 1600):   # la roca se vuelve polvo: grano
            for i in range(int(max(x0, -5400) // 60), int(min(x1, 2600) // 60)):
                for j in range(5):
                    px = i * 60 + 50 * h01(i, j)
                    ph = float(suelo_h(px, rel, hund)) - 30 - 900 * h01(i, j + 9)
                    if not S.vis(px - 10, px + 10, ph - 10, ph + 10):
                        continue
                    with S.en(lz, px, ph - 30 * polvo * math.sin(t * 2 + i + j)):
                        lz.relleno(circulo(0, 0, 5 + 4 * h01(j, i), 8), (214, 190, 170), alfa=0.6 * polvo)

    vida = est.get("vida_resto", 1.0)
    if vida > 0.02 and S.vis(-4900, -2200, 0, 800):
        for i in range(int(max(x0, -4900) // 70), int(min(x1, -2200) // 70)):
            xi = i * 70 + 25 * math.sin(i * 3.3)
            hi = float(suelo_h(xi, rel, hund))
            if 40 < hi < 680:
                with S.en(lz, xi, hi - 10, 0.55 + 0.25 * h01(i, 2)):
                    KO.pino(lz, 0, 0, 1.0, mezcla((70, 150, 120), (140, 110, 120), b), oscuro=0.1)


def tunel_metro(lz, t, S, est):
    """Túnel del metro bajo el pueblo (detalle del corte: un tren que pasa; se detiene con el apagón)."""
    if not S.vis(-700, 1700, -380, -220):
        return
    pol = est.get("polvo", 0.0)
    lz.relleno(S.poly([[-700, -230], [1700, -230], [1700, -360], [-700, -360]]), (64, 56, 82))
    lz.relleno(S.poly([[-700, -350], [1700, -350], [1700, -362], [-700, -362]]), (110, 100, 130))
    red = 1.0 if est.get("normal") else est.get("red", 1.0)
    tt = t if red > 0.5 else T_RED
    tx = -1400 + ((tt * 260) % 3600)
    for k in range(3):
        xx = tx - k * 250
        if not S.vis(xx - 130, xx + 130, -360, -240):
            continue
        with S.en(lz, xx, -350):
            lz.relleno(rect_red(-118, -100, 236, 96, 26), mezcla((236, 200, 90), (150, 140, 150), pol))
            for w_ in range(5):
                lz.relleno(rect_red(-100 + w_ * 42, -86, 30, 30, 6), mezcla((255, 244, 200), (80, 90, 120), 1 - red))
            lz.relleno(rect_red(-118, -30, 236, 12, 4), (220, 90, 80))


def mar(lz, t, S, est):
    if not S.vis(X_COSTA - 400, 6000, -1700, 60):
        return
    hid = est.get("hidro", 0.0)
    b = est.get("b", 0.0)
    X = XS[XS >= X_COSTA - 300]
    ola = 5 * np.sin(X / 70 + t * 1.8) + 3 * np.sin(X / 31 - t * 2.6)
    sup = ola * (1 - hid) + hid * (18 * np.sin(X / 25 + t * 9) * 0.4)
    fondo = suelo_h(X)
    if DELGADO[0]:
        fondo = np.maximum(fondo, -70.0)
    agua = np.concatenate([np.stack([X, sup], 1), np.stack([X[::-1], fondo[::-1] - 2], 1)])
    c0 = mezcla((92, 176, 236), (236, 226, 250), hid)
    c1 = mezcla((16, 34, 92), (190, 176, 230), hid)
    xa, ya = S.pt(3400, 0)
    xb, yb = S.pt(3400, -1500)
    lz.degradado(S.poly(agua), c0, c1, (xa, ya), (xb, yb), alfa=1 - 0.55 * hid)
    # rayos de luz bajo el agua
    if hid < 0.9:
        for i in range(6):
            x_ = 2700 + i * 420 + 60 * math.sin(t * 0.4 + i)
            lz.relleno(S.poly([[x_, -5], [x_ + 90, -5], [x_ - 120, -700], [x_ - 260, -700]]), (190, 230, 255),
                       alfa=0.08 * (1 - hid))
    # espuma en la superficie
    if hid < 0.95:
        xs_, ys_ = S.p(X, sup + 2)
        lz.trazo(np.stack([xs_, ys_], 1), (236, 248, 255, int(220 * (1 - hid))), 5 * S.k, afinar=False)
    if DELGADO[0]:
        return
    vida_mar(lz, t, S, est)
    algas(lz, t, S, est)
    if hid > 0.01:
        burbujas_h(lz, t, S, est)


def algas(lz, t, S, est):
    vida = est.get("vida_resto", 1.0)
    if vida <= 0.02 or not S.vis(2500, 5800, -1600, -100):
        return
    for i in range(26):
        x_ = 2450 + i * 130 + 40 * math.sin(i * 3.1)
        f = float(suelo_h(x_))
        alto = 60 + 70 * ((i * 7) % 4) / 3
        pts = np.array([[x_ + 14 * math.sin(t * 1.2 + i + k * 0.6) * k / 5, f + alto * k / 5] for k in range(6)])
        xs_, ys_ = S.p(pts[:, 0], pts[:, 1])
        lz.trazo(np.stack([xs_, ys_], 1), (60 + 40 * (i % 2), 170, 120, int(255 * vida)), 9 * S.k, afinar=False)
    for i in range(12):
        x_ = 2600 + i * 270
        with S.en(lz, x_, float(suelo_h(x_)) + 6):
            lz.relleno(elipse(0, 0, 50 + 20 * (i % 3), 22, 0, 24), (110, 84, 120))


def vida_mar(lz, t, S, est):
    vida = est.get("vida_resto", 1.0)
    if vida <= 0.02:
        return
    for j, (cx, ch, n, col) in enumerate(((2900, -260, 9, (255, 176, 80)), (3500, -560, 11, (255, 120, 150)),
                                          (4200, -380, 8, (120, 220, 230)), (3100, -900, 7, (255, 220, 110)))):
        if not S.vis(cx - 400, cx + 400, ch - 200, ch + 200):
            continue
        for i in range(n):
            px = cx + 150 * math.sin(t * 0.35 + i * 0.9 + j) + (i % 3) * 40
            ph = ch + 60 * math.sin(i * 1.7) + 10 * math.sin(t + i)
            d = 1 if math.cos(t * 0.35 + i * 0.9 + j) > 0 else -1
            with S.en(lz, px, ph, 0.9):
                KO.pez(lz, 0, 0, 1.0, t, col, dir=d, seed=i)
    # ballena lejana
    if S.vis(3600, 4800, -900, -500):
        xw = 4300 - 40 * t % 1200
        with S.en(lz, 4300 - 30 * math.sin(t * 0.05), -720, 1.0):
            lz.relleno(elipse(0, 0, 260, 70, 0.02, 40), (70, 96, 160), alfa=vida)
            lz.relleno(elipse(20, 26, 200, 34, 0, 30), (150, 180, 220), alfa=vida)
            lz.relleno(np.array([[-250, 0], [-330, -50 + 20 * math.sin(t)], [-320, 40 + 20 * math.sin(t)]]), (70, 96, 160),
                       alfa=vida)
            lz.relleno(circulo(170, -10, 6, 10), (30, 30, 60), alfa=vida)


def burbujas_h(lz, t, S, est):
    """El agua convertida en hidrógeno: burbujas pálidas que suben por todo el mar."""
    hid = est["hidro"]
    for i in range(int(120 * hid)):
        x_ = 2400 + (i * 97.3) % 3300
        prof = float(suelo_h(x_))
        u = (t * (0.25 + 0.15 * (i % 4)) + (i * 0.618) % 1) % 1
        ph = prof + (-prof + 120) * u
        if not S.vis(x_ - 30, x_ + 30, ph - 30, ph + 30):
            continue
        with S.en(lz, x_ + 18 * math.sin(t * 2 + i), ph):
            lz.relleno(circulo(0, 0, 7 + 9 * ((i * 7) % 5) / 4, 14), (250, 248, 255), alfa=0.75 * hid)


# ======================================================================== pueblo
# (X centro, ancho, alto, color, techo, tipo)
EDIFICIOS = [
    (-250, 170, 200, (244, 204, 160), "dos_aguas", "velas"),
    (-40, 150, 340, (150, 172, 226), "plano", "pisos"),
    (170, 190, 170, (246, 236, 220), "toldo", "cafe"),
    (400, 160, 230, (180, 226, 196), "dos_aguas", "cocina"),
    (640, 210, 440, (232, 178, 196), "plano", "torre"),
    (890, 170, 190, (250, 222, 160), "dos_aguas", "casa"),
    (1110, 150, 290, (170, 200, 240), "plano", "pisos"),
]


def skyline(lz, t, S, est):
    """Fila de edificios lejanos detrás del pueblo (paralaje 0.86)."""
    Sk = S.par(0.86)
    if not Sk.vis(-500, 1400, 0, 700):
        return
    pol = est.get("polvo", 0.0)
    for i in range(13):
        x_ = -480 + i * 140
        h_ = (260 + 180 * h01(i, 2)) * (1 - 0.85 * clamp01(pol * 1.4 - 0.2 * h01(i, 4)))
        col = mezcla((176, 186, 226), (170, 140, 160), est.get("b", 0.0))
        lz.relleno(Sk.poly([[x_ - 60, -10], [x_ + 60, -10], [x_ + 60, h_], [x_ - 60, h_]]), col)
        for j in range(int(h_ // 60)):
            for c in (-25, 15):
                lz.relleno(Sk.poly([[x_ + c, 30 + j * 60], [x_ + c + 14, 30 + j * 60], [x_ + c + 14, 48 + j * 60],
                                    [x_ + c, 48 + j * 60]]), mezcla((150, 160, 210), (255, 236, 170), 0.5 * est.get("red", 1.0)))


def _ventana(lz, x, y, w, h, red, b=0.0):
    luz = mezcla((96, 110, 160), (255, 232, 150), red * 0.85)
    lz.relleno(rect_red(x, y, w, h, 3), mezcla(luz, (140, 120, 140), b * 0.5))
    lz.relleno(rect_red(x + 2, y + 2, w * 0.35, h - 4, 2), (255, 255, 255), alfa=0.25)


def edificio(lz, t, S, est, i, X, w, h, col, techo, tipo):
    pol = est.get("polvo", 0.0)
    b = est.get("b", 0.0)
    red = est.get("red", 1.0)
    d = clamp01(pol * 1.5 - 0.25 * h01(i, 1))           # cuánto se ha deshecho este edificio
    hund = est.get("hundir", 0.0)
    base = float(suelo_h(X, 1.0, hund))
    colb = mezcla(col, (190, 160, 160), 0.3 * b)
    with S.en(lz, X, base):
        # esqueleto de acero (lo que queda de los metales)
        if d > 0.02:
            ac = (150, 156, 186)
            for c in np.linspace(-w / 2 + 8, w / 2 - 8, 4):
                lz.trazo(np.array([[c, 0], [c, -h * (0.96 - 0.1 * h01(i, int(c)))]]), ac + (int(255 * min(1, d * 2)),), 5,
                         afinar=False)
            for j in range(1, int(h // 70) + 1):
                yy = -j * 70
                lz.trazo(np.array([[-w / 2 + 8, yy], [w / 2 - 8, yy + 6 * math.sin(j + i)]]), ac + (int(255 * min(1, d * 2)),), 4,
                         afinar=False)
        # cuerpo: recortado por una línea irregular que baja (se deshace en polvo)
        hv = h * (1 - d) + 30
        corte = np.array([[-w / 2 - 50, 10]] + [[xx, -hv + 26 * d * math.sin(xx / 13 + i + t * 3)] for xx in
                                              np.linspace(-w / 2 - 50, w / 2 + 50, 14)] + [[w / 2 + 50, 10]])
        cl = corte
        with lz.recorte(cl):
            _cuerpo_edificio(lz, t, est, i, w, h, colb, techo, tipo, red, b)
        if d > 0.01:
            # polvo que cae del borde y nube en la base
            for k in range(14):
                u = (t * 0.9 + k / 14 + h01(i, k)) % 1
                px = -w / 2 + w * h01(k, i)
                py = -hv + u * hv
                lz.relleno(circulo(px + 10 * math.sin(u * 7 + k), py, 4 + 5 * u, 10), (226, 206, 186),
                           alfa=0.8 * min(1.0, d * 3) * (1 - d ** 4) * (1 - u * 0.4))
            for k in range(5):
                lz.relleno(circulo(-w / 2 + k * w / 4, -10, (30 + 40 * d) * (1 + 0.1 * math.sin(t * 2 + k)), 20),
                           (220, 196, 176), alfa=0.55 * min(1.0, d * 2))
            lz.relleno(catmull(np.array([[-w / 2 - 40, 4], [-w / 4, -38 * d], [0, -60 * d], [w / 3, -30 * d],
                                         [w / 2 + 40, 4]]), 6), (206, 180, 160), alfa=min(1.0, d * 2))


def _cuerpo_edificio(lz, t, est, i, w, h, col, techo, tipo, red, b):
    lz.relleno(rect_red(-w / 2, -h, w, h, 4), col)
    lz.relleno(rect_red(-w / 2, -h, w * 0.18, h, 3), aclarar(col, 0.25))
    lz.relleno(rect_red(w / 2 - w * 0.12, -h, w * 0.12, h, 3), oscurecer(col, 0.12))
    if techo == "dos_aguas":
        lz.relleno(np.array([[-w / 2 - 16, -h + 4], [0, -h - 74], [w / 2 + 16, -h + 4]]), mezcla((206, 90, 80), (150, 110, 120), b))
        lz.relleno(np.array([[0, -h - 74], [w / 2 + 16, -h + 4], [w / 4, -h + 4]]), mezcla((176, 70, 70), (130, 96, 110), b))
        lz.relleno(rect_red(w * 0.18, -h - 66, 22, 50, 3), oscurecer(col, 0.2))
    elif techo == "plano":
        lz.relleno(rect_red(-w / 2 - 6, -h - 12, w + 12, 14, 3), oscurecer(col, 0.25))
        lz.relleno(rect_red(-w * 0.25, -h - 52, 46, 40, 6), (140, 140, 170))
        lz.relleno(rect_red(-w * 0.25 + 6, -h - 58, 34, 10, 4), (170, 170, 196))
    elif techo == "toldo":
        for k in range(6):
            c = (230, 80, 90) if k % 2 == 0 else (250, 246, 240)
            x_ = -w / 2 - 10 + k * (w + 20) / 6
            lz.relleno(np.array([[x_, -h * 0.55], [x_ + (w + 20) / 6, -h * 0.55], [x_ + (w + 20) / 6, -h * 0.55 + 34],
                                 [x_, -h * 0.55 + 34]]), c)
    if tipo == "pisos" or tipo == "torre":
        cols = 3 if tipo == "pisos" else 4
        filas = int((h - 40) // 62)
        for f in range(filas):
            for c in range(cols):
                wx = -w / 2 + 18 + c * (w - 36) / cols
                on = red * (1.0 if h01(i * 7 + f, c) > 0.25 else 0.15)
                _ventana(lz, wx, -h + 26 + f * 62, (w - 36) / cols - 14, 38, on, b)
        lz.relleno(rect_red(-18, -54, 36, 54, 4), oscurecer(col, 0.45))
    elif tipo == "velas":
        # gran ventana con mesa y velas encendidas
        lz.relleno(rect_red(-62, -150, 124, 96, 6), (70, 60, 96))
        lz.relleno(rect_red(-58, -146, 116, 88, 4), mezcla((120, 100, 130), (255, 214, 150), 0.35 * est.get("fuego", 1.0)))
        lz.relleno(rect_red(-50, -80, 100, 10, 3), (150, 96, 80))
        for k, vx in enumerate((-26, 0, 26)):
            KO.vela(lz, vx, -80, 0.62, t, est.get("fuego", 1.0) if not est.get("normal") else 1.0, seed=k,
                    t_apaga=T_FUEGO if not est.get("normal") else None)
        lz.relleno(rect_red(-62, -100, 124, 4, 2), (250, 244, 236), alfa=0.0)
        lz.relleno(rect_red(30, -54, 36, 54, 4), (150, 96, 80))
    elif tipo == "cocina":
        lz.relleno(rect_red(-60, -150, 100, 86, 6), (70, 60, 96))
        lz.relleno(rect_red(-56, -146, 92, 78, 4), (226, 220, 236))
        lz.relleno(rect_red(-50, -96, 80, 28, 3), (90, 90, 110))          # fogón
        fu = est.get("fuego", 1.0) if not est.get("normal") else 1.0
        for k, vx in enumerate((-30, 10)):
            KO.llama(lz, vx, -96, 0.38, t, k + 5, fu)
            lz.relleno(rect_red(vx - 22, -122, 44, 22, 6), (110, 120, 150))   # ollas
        if not est.get("normal"):
            KO.humo(lz, -10, -130, 0.6, t, T_FUEGO, dur=2.4, n=5, alfa=0.7)
        lz.relleno(rect_red(52, -64, 32, 64, 4), (120, 84, 70))
        _ventana(lz, 52, -150, 30, 40, red, b)
    elif tipo == "cafe":
        lz.relleno(rect_red(-w / 2 + 14, -h * 0.55 + 40, w - 28, h * 0.55 - 40, 4), (90, 70, 96))
        lz.relleno(rect_red(-w / 2 + 18, -h * 0.55 + 44, w - 36, h * 0.55 - 60, 3), mezcla((110, 100, 140), (255, 220, 160), 0.6 * red))
        # letrero de neón
        neon = red
        col_n = mezcla((120, 80, 110), (255, 90, 150), neon)
        if neon > 0.05:
            lz.halo(0, -h + 20, 110, (255, 90, 150), alfa=0.45 * neon)
        P.rotulo(lz, 0, -h + 22, "CAFÉ", 40, color=col_n, sombra=0.0, capa=None)
        for k in range(3):
            _ventana(lz, -w / 2 + 20 + k * 54, -h + 52, 40, 36, red, b)
    else:
        _ventana(lz, -w / 2 + 20, -h + 40, 46, 44, red, b)
        _ventana(lz, w / 2 - 66, -h + 40, 46, 44, red, b)
        lz.relleno(rect_red(-20, -60, 40, 60, 4), (140, 90, 80))


def pueblo(lz, t, S, est):
    if not S.vis(-500, 1300, -100, 700):
        return
    for i, e in enumerate(EDIFICIOS):
        if S.vis(e[0] - e[1], e[0] + e[1], 0, e[2] + 100):
            edificio(lz, t, S, est, i, *e)


# ======================================================================== red eléctrica y central
TORRES = [(1380.0, 1.0), (1000.0, 0.92), (620.0, 0.86)]
X_CENTRAL = 1820.0


def red_electrica(lz, t, S, est):
    if not S.vis(-400, 2000, 0, 500):
        return
    red = est.get("red", 1.0)
    pol = est.get("polvo", 0.0)
    hund = est.get("hundir", 0.0)
    pts_cable = [(X_CENTRAL - 200, 300)]
    for X, s in TORRES:
        base = float(suelo_h(X, 1.0, hund))
        if S.vis(X - 80, X + 80, base, base + 340 * s):
            with S.en(lz, X, base, s):
                KO.torre_luz(lz, 0, 0, 1.0, col=mezcla((120, 126, 160), (150, 120, 130), est.get("b", 0.0)))
        pts_cable.append((X, base + 290 * s))
    pts_cable.append((80, 250))
    for (xa, ha), (xb, hb) in zip(pts_cable[:-1], pts_cable[1:]):
        xs_ = np.linspace(xa, xb, 24)
        u = np.linspace(0, 1, 24)
        hs_ = ha + (hb - ha) * u - 40 * np.sin(u * math.pi)
        for dh in (0, -48):
            xx, yy = S.p(xs_, hs_ + dh)
            lz.trazo(np.stack([xx, yy], 1), (70, 70, 100, 230), 2.5 * S.k, afinar=False)
        # pulsos de energía que viajan hacia el pueblo
        if red > 0.05:
            for k in range(3):
                uu = (t * 0.6 + k / 3) % 1
                j = int(uu * 23)
                x_, y_ = S.pt(xs_[::-1][j], hs_[::-1][j])
                lz.halo(x_, y_, 22 * S.k, (255, 240, 150), alfa=0.8 * red)
    _ = pol


def central_electrica(lz, t, S, est):
    if not S.vis(X_CENTRAL - 600, X_CENTRAL + 400, 0, 1300):
        return
    normal = est.get("normal", False)
    fu = 1.0 if normal else est.get("fuego", 1.0)
    alarma = 0.0 if normal else ventana(t, A.seguridad - 0.3, B_FIN_ALARMA, 0.3, 0.6)
    d = clamp01(est.get("polvo", 0.0) * 1.5 - 0.3)
    base = float(suelo_h(X_CENTRAL, 1.0, est.get("hundir", 0.0)))
    with S.en(lz, X_CENTRAL, base, 0.92):
        corte = np.array([[-520, 10]] + [[xx, -700 * (1 - d) - 20 + 30 * d * math.sin(xx / 17)] for xx in np.linspace(-520, 320, 16)]
                         + [[320, 10]])
        with lz.recorte(corte):
            KO.central(lz, 0, 0, 1.0, t, llama_f=fu, humo_f=fu, alarma=alarma, t_apaga=None if normal else T_FUEGO)


B_FIN_ALARMA = A.cero_a + 300   # se redefine abajo


# ======================================================================== carretera, semáforos, coches
X_CARR = (-2440.0, 2150.0)
H_ACERA, H_CARR = -14.0, -92.0


def carretera(lz, t, S, est):
    if not S.vis(X_CARR[0], X_CARR[1], H_CARR - 40, 20):
        return
    pol, hund = est.get("polvo", 0.0), est.get("hundir", 0.0)
    rot_c = clamp01((t - A.carreteras + 0.3) / 1.6) if not est.get("normal") and pol > 0 else 0.0
    n = 30
    L = (X_CARR[1] - X_CARR[0]) / n
    for k in range(n):
        xa = X_CARR[0] + k * L
        caida = rot_c * (0.3 + 0.7 * h01(k, 3))
        dy = -hund * (70 + 22 * math.sin((xa + L / 2) / 97)) - 60 * caida ** 2
        ang = (h01(k, 5) - 0.5) * 0.25 * caida
        with S.en(lz, xa + L / 2, dy, 1.0, ang):
            lz.relleno(np.array([[-L / 2 - 1, 0], [L / 2 + 1, 0], [L / 2 + 1, H_ACERA], [-L / 2 - 1, H_ACERA]]) * [1, -1],
                       mezcla((214, 212, 226), (190, 170, 170), est.get("b", 0.0)))
            lz.relleno(np.array([[-L / 2 - 1, -H_ACERA], [L / 2 + 1, -H_ACERA], [L / 2 + 1, -H_CARR], [-L / 2 - 1, -H_CARR]]),
                       mezcla((78, 76, 104), (110, 96, 110), est.get("b", 0.0)))
            lz.relleno(np.array([[-L / 2 + 20, 50], [-L / 2 + 80, 50], [-L / 2 + 80, 56], [-L / 2 + 20, 56]]), (250, 236, 170))
            if caida > 0.05:
                lz.relleno(np.array([[-L / 2, 14], [L / 2, 92], [L / 2, 96], [-L / 2, 18]]), (40, 34, 50), alfa=0.0)
            if pol > 0.05:   # grietas
                lz.trazo(np.array([[-L / 2 + 30, 16], [-L / 2 + 50, 40], [-L / 2 + 40, 70], [-L / 2 + 64, 92]]),
                         (40, 34, 60, int(255 * min(1, pol * 2))), 3, afinar=False)


def tunel_carretera(lz, t, S, est):
    """Boca del túnel por el que la carretera entra en la montaña (de ahí salen los coches)."""
    if not S.vis(X_CARR[0] - 160, X_CARR[0] + 160, -100, 200):
        return
    with S.en(lz, X_CARR[0] - 10, 0):
        lz.relleno(np.array([[-150, 96], [-150, -110], [-70, -170], [70, -170], [130, -110], [130, 96]], float),
                   mezcla((150, 136, 172), (170, 130, 140), est.get("b", 0.0)))
        lz.relleno(np.array([[-110, 94], [-110, -60], [-60, -110], [40, -110], [90, -60], [90, 94]], float), (40, 34, 60))
        lz.relleno(np.array([[-110, 94], [-110, -60], [-60, -110], [-40, -110], [-80, -60], [-80, 94]], float), (60, 52, 84))


def mobiliario(lz, t, S, est):
    red = est.get("red", 1.0)
    hund = est.get("hundir", 0.0)
    d = est.get("polvo", 0.0)
    if d > 0.6:
        return
    for X, f in ((300.0, 0.0), (790.0, 0.4)):
        if S.vis(X - 40, X + 40, 0, 240):
            with S.en(lz, X, -6 - hund * 70):
                KO.semaforo(lz, 0, 0, 0.9, t, on=red, fase=f)
    for X in (-120.0, 520.0, 1010.0):
        if S.vis(X - 40, X + 60, 0, 240):
            with S.en(lz, X, -6 - hund * 70):
                KO.farola(lz, 0, 0, 0.95, on=0.0)


# coches: (color, X donde se paran, velocidad, fase)
COCHES = [((236, 90, 90), 360.0, 230.0, 0.0), ((90, 150, 236), 760.0, 200.0, 0.3), ((250, 196, 70), 1180.0, 250.0, 0.6),
          ((120, 200, 160), 1560.0, 210.0, 0.1)]
TAU_C = 2.2


def pos_coche(t, i):
    col, xs, v, f = COCHES[i]
    t_off = A.coches - 0.2
    if t <= t_off:
        return xs - v * TAU_C - v * (t_off - t), v
    u = t - t_off
    x = xs - v * TAU_C * math.exp(-u / TAU_C)
    vel = v * math.exp(-u / TAU_C)
    if i == 1:   # el azul choca suavemente con el rojo cuando el apagón deja los semáforos negros
        x += 0.0
    return x, vel


def coches(lz, t, S, est):
    if est.get("normal"):
        return
    hund = est.get("hundir", 0.0)
    for i, (col, xs, v, f) in enumerate(COCHES):
        x, vel = pos_coche(t, i)
        extra = 0.0
        if i == 1 and t > A.choques - 0.6:      # choque leve contra el rojo (adelantado)
            extra = -0.0
        if x < X_CARR[0] + 40 or not S.vis(x - 140, x + 140, -100, 120):
            continue
        rueda = (x / 20.0)
        with S.en(lz, x + extra, -64 - hund * 75, 1.0):
            KO.coche(lz, 0, 0, 1.0, t, col, rueda=rueda, motor=est.get("motores", 1.0) if t < A.pilotos else 0.0, dir=1, seed=i)
    # choque en el cruce durante el apagón (dos coches, estrellitas)
    ch = est.get("choques", 0.0)
    if ch > 0.01 and S.vis(820, 1100, -100, 120):
        with S.en(lz, 960, -64, 1.0):
            KO.coche(lz, 0, 0, 1.0, t, (200, 120, 230), rueda=0, motor=0, dir=-1, seed=7)
        x_, y_ = S.pt(860, 40)
        for k in range(5):
            a = k / 5 * 2 * math.pi + t * 3
            lz.relleno(KO.circulo(x_ + 34 * math.cos(a) * S.k, y_ + 16 * math.sin(a) * S.k, 7 * S.k, 10), (255, 236, 120),
                       alfa=ch, capa=2)


# ======================================================================== costa
def costa(lz, t, S, est):
    if not S.vis(1900, 3200, -200, 400):
        return
    b = est.get("b", 0.0)
    hund = est.get("hundir", 0.0)
    X = np.arange(2050, 2460, 20.0)
    top = suelo_h(X, 1.0, hund)
    lz.relleno(S.poly(np.concatenate([np.stack([X, top + 3], 1), np.stack([X[::-1], top[::-1] - 26], 1)])),
               mezcla((246, 222, 160), (220, 190, 170), b))
    # faro
    with S.en(lz, 2140, float(suelo_h(2140, 1.0, hund))):
        lz.relleno(np.array([[-30, 0], [-20, -260], [20, -260], [30, 0]]), (250, 246, 240))
        for k in range(3):
            lz.relleno(np.array([[-29 + 3 * k, -40 - 80 * k], [29 - 3 * k, -40 - 80 * k], [28 - 3 * k, -76 - 80 * k],
                                 [-28 + 3 * k, -76 - 80 * k]]), (226, 80, 80))
        lz.relleno(rect_red(-22, -300, 44, 40, 6), (90, 100, 140))
        lz.relleno(np.array([[-28, -300], [0, -330], [28, -300]]), (226, 80, 80))
        on = est.get("red", 1.0) if not est.get("normal") else 1.0
        if on > 0.05:
            ang = t * 1.6
            for sgn in (1, -1):
                lz.relleno(np.array([[0, -280], [sgn * 380 * math.cos(ang), -280 - 50], [sgn * 380 * math.cos(ang), -280 + 50]]),
                           (255, 250, 200), alfa=0.18 * on * abs(math.cos(ang)), capa=2)
            lz.halo(0, -280, 50, (255, 240, 170), alfa=0.8 * on)
    # muelle
    if S.vis(2380, 2800, -80, 80):
        for k in range(6):
            xx = 2400 + k * 70
            lz.relleno(S.poly([[xx - 6, 30], [xx + 6, 30], [xx + 6, -110], [xx - 6, -110]]), (120, 84, 70))
        lz.relleno(S.poly([[2380, 30], [2780, 30], [2780, 46], [2380, 46]]), (176, 120, 90))
    # barca
    bob = 5 * math.sin(t * 1.4)
    if S.vis(2780, 3080, -60, 200):
        with S.en(lz, 2930, bob - 4, 1.0, 0.04 * math.sin(t * 1.1)):
            lz.relleno(np.array([[-110, -30], [110, -30], [80, 10], [-90, 10]]), mezcla((240, 120, 90), (200, 140, 150), b))
            lz.relleno(np.array([[-110, -30], [110, -30], [104, -20], [-106, -20]]), (250, 246, 240))
            lz.relleno(rect_red(-30, -90, 70, 60, 6), (250, 246, 240))
            lz.relleno(rect_red(-22, -80, 22, 20, 3), (150, 200, 240))
            lz.trazo(np.array([[60, -30], [60, -150]]), (120, 84, 70), 5, afinar=False)


# ======================================================================== parque
ARBOLES = [(-2050, 1.05, 0), (-1880, 0.85, 1), (-1520, 1.15, 2), (-1060, 0.95, 3), (-560, 1.1, 4), (-380, 0.8, 5)]
PINOS = [(-2220, 1.1), (-1700, 1.3), (-1330, 1.0)]
X_BANCO = -930.0
X_ASADOR = -470.0
ESTANQUE = (-1680.0, -1380.0)


def parque(lz, t, S, est):
    if not S.vis(-2400, -250, -60, 500):
        return
    b = est.get("b", 0.0)
    vida = est.get("vida_resto", 1.0)
    hund = est.get("hundir", 0.0)
    hid = est.get("hidro", 0.0)
    # estanque
    if False and S.vis(ESTANQUE[0], ESTANQUE[1], -60, 20):
        x0, x1 = ESTANQUE
        X = np.linspace(x0, x1, 30)
        fondo = -40 * np.sin(np.linspace(0, math.pi, 30)) - 2
        lz.relleno(S.poly(np.concatenate([np.stack([X, np.zeros(30) - 1], 1), np.stack([X[::-1], fondo[::-1]], 1)])),
                   mezcla((80, 170, 230), (236, 226, 250), hid), alfa=1 - 0.6 * hid)
        for k in range(3):
            xx = x0 + 60 + k * 90 + 20 * math.sin(t * 0.7 + k)
            xx_, yy_ = S.pt(xx, -3)
            lz.relleno(elipse(xx_, yy_, 26 * S.k, 4 * S.k, 0, 16), (200, 236, 255), alfa=0.6 * (1 - hid))
    # pasto alto (borde)
    X = XS[(XS > -2400) & (XS < -300)]
    top = suelo_h(X, 1.0, hund)
    lz.relleno(S.poly(np.concatenate([np.stack([X, top + 2], 1), np.stack([X[::-1], top[::-1] - 26], 1)])),
               mezcla((92, 184, 108), (150, 130, 120), b))
    for X_, s, sd in ARBOLES:
        if S.vis(X_ - 160, X_ + 160, 0, 360):
            _arbol_vivo(lz, t, S, est, X_, s, sd, vida)
    for X_, s in PINOS:
        if S.vis(X_ - 100, X_ + 100, 0, 300):
            if vida > 0.02:
                with S.en(lz, X_, float(suelo_h(X_, 1.0, hund)) - 4, s):
                    KO.pino(lz, 0, 0, 1.0, mezcla((60, 150, 110), (130, 110, 120), b))
            if vida < 0.98:
                _fantasma_arbol(lz, S, X_, float(suelo_h(X_, 1.0, hund)), s * 0.9, 1 - vida, t)
    for i in range(16):   # flores y arbustos
        X_ = -2250 + i * 120 + 30 * math.sin(i * 2.7)
        if not S.vis(X_ - 60, X_ + 60, -20, 100):
            continue
        if i % 3 == 0 and vida > 0.02:
            with S.en(lz, X_, float(suelo_h(X_, 1.0, hund)) - 6, 0.8):
                KO.arbusto(lz, 0, 0, 1.0, mezcla((80, 170, 100), (140, 110, 120), b), seed=i)
        elif vida > 0.02:
            with S.en(lz, X_, float(suelo_h(X_, 1.0, hund)) - 4, 0.75):
                P.planta(lz, 0, 0, 1.0, t, vida=vida, col=(96, 196, 110))
    # banco
    if S.vis(X_BANCO - 120, X_BANCO + 120, 0, 120):
        with S.en(lz, X_BANCO, float(suelo_h(X_BANCO, 1.0, hund)) - 4):
            for xx in (-70, 70):
                lz.relleno(rect_red(xx - 5, -46, 10, 46, 3), (80, 76, 100))
            lz.relleno(rect_red(-90, -54, 180, 12, 4), (176, 112, 80))
            lz.relleno(rect_red(-90, -100, 180, 12, 4), (176, 112, 80))
            lz.relleno(rect_red(-90, -82, 180, 12, 4), (196, 128, 92))
    # farolas del parque
    for X_ in (-1950.0, -1200.0):
        if S.vis(X_ - 40, X_ + 60, 0, 240):
            with S.en(lz, X_, float(suelo_h(X_, 1.0, hund)) - 4):
                KO.farola(lz, 0, 0, 0.95, on=0.0)


def _arbol_vivo(lz, t, S, est, X_, s, sd, vida):
    base = float(suelo_h(X_, 1.0, est.get("hundir", 0.0))) - 4
    if vida > 0.02:
        with S.en(lz, X_, base, s, 0.02 * math.sin(t * 0.8 + sd)):
            P.arbol(lz, 0, 0, 1.0, t, hojas=mezcla((80, 176, 100), (150, 120, 120), est.get("b", 0.0)), seed=sd)
    if vida < 0.98:
        _fantasma_arbol(lz, S, X_, base, s, 1 - vida, t)


def _fantasma_arbol(lz, S, X_, base, s, a, t):
    with S.en(lz, X_, base, s):
        col = (255, 255, 255)
        for dx, dy, r in ((-62, -150, 44), (60, -160, 44), (-50, -200, 62), (40, -210, 68), (-5, -262, 72)):
            KO.fantasma(lz, dx, dy, r * 0.9, col, alfa=0.55 * a, fase=t * 10, ancho=3)
        P.discontinua(lz, [[0, 0], [0, -150]], col + (int(140 * a),), 3, 12, 10, fase=t * 10)


def asador(lz, t, S, est):
    if not S.vis(X_ASADOR - 120, X_ASADOR + 120, 0, 200):
        return
    normal = est.get("normal", False)
    fu = 1.0 if normal else max(est.get("fuego", 1.0), 0.0)
    br = 1.0 if normal else max(est.get("fuego", 1.0), 0.6 * est.get("fuego_vuelve", 0.0) + 0.25)
    if not normal and t > A.brasas:
        fu = max(fu, 0.7 * est.get("fuego_vuelve", 0.0))
    if not normal and est.get("b", 0.0) > 0.5:
        fu = br = 0.0
    with S.en(lz, X_ASADOR, float(suelo_h(X_ASADOR, 1.0, est.get("hundir", 0.0))) - 4, 0.95):
        KO.parrilla(lz, 0, 0, 1.0, t, fuego=fu, brasas=br, t_apaga=None if normal else T_FUEGO)


def motas_o(lz, t, S, x0, x1, h0, h1, n, alfa, seed=0, r=7.0):
    """Átomos de oxígeno (puntos rojos que titilan) repartidos en un rectángulo del mundo."""
    if alfa <= 0.01 or not S.vis(x0, x1, h0, h1):
        return
    for i in range(n):
        X = x0 + (x1 - x0) * h01(i, seed)
        Hh = h0 + (h1 - h0) * h01(i, seed + 7)
        tw = 0.6 + 0.4 * math.sin(t * 4 + i * 1.3)
        x, y = S.pt(X, Hh)
        rr = r * max(S.k, 1.0) * tw
        lz.relleno(circulo(x, y, rr + 2.5, 12), (255, 236, 236), alfa=alfa * 0.8, capa=2)
        lz.relleno(circulo(x, y, rr, 12), (240, 60, 76), alfa=alfa, capa=2)


DELGADO = [False]


def dibujar(lz, t, S, est, rel=1.0, sin_gente=False, tapa=None, delgado=False):
    """Dibuja todo el paisaje (sin cielo, que es el fondo). delgado: solo la piel de la superficie (zoom al planeta)."""
    DELGADO[0] = delgado
    import gente as G
    sol_paisaje(lz, t, S)
    nubes(lz, t, S, est)
    capas_lejanas(lz, t, S, est)
    G.aviones_lejanos(lz, t, S, est)
    skyline(lz, t, S, est)
    red_electrica(lz, t, S, est)
    central_electrica(lz, t, S, est)
    terreno(lz, t, S, est, rel)
    mar(lz, t, S, est)
    costa(lz, t, S, est)
    if tapa is not None:
        tapa()
    parque(lz, t, S, est)
    pueblo(lz, t, S, est)
    carretera(lz, t, S, est)
    tunel_carretera(lz, t, S, est)
    mobiliario(lz, t, S, est)
    asador(lz, t, S, est)
    coches(lz, t, S, est)
    if not sin_gente:
        G.gente(lz, t, S, est)
    G.avion_grande(lz, t, S, est)
    DELGADO[0] = False


B_FIN_ALARMA = A.version_facil
