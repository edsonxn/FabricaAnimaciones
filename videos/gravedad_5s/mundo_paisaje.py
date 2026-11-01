# -*- coding: utf-8 -*-
"""El paisaje continuo de «gravedad 5 s» (X a la derecha, H hacia arriba; 1 unidad ≈ 1 px a k = 1):
  - Izquierda (X ≈ -1250): casa en corte transversal (KG.casa_corte) con jardín y cerca; en Segundo 0 flota todo a ras del piso.
  - Centro-izq (X ≈ -850..-200): parque con gran árbol (altura ~295 u = 5 metros), banca, farolas, mesa con taza de café y bicicleta.
  - Centro-der (X ≈ -150..1150): avenida urbana con edificios coloridos estilo Kurzgesagt, carretera, charcos y coches que flotan en viento_mar.
  - Derecha (X ≈ 1150..3200): malecón con faro y playa; mar en corte donde las olas se despegan en grandes burbujas flotantes.
  - Capas lejanas con paralaje: Sol (0,04), nubes (0,3), cordillera (0,2), cerros con pinos y aerogeneradores (0,45), lomas y skyline (0,75).
"""
import math

import numpy as np

import plano as P
from plano import mezcla, aclarar, oscurecer
from motor import W, H, prog, clamp01, lerp, e_in, e_out, e_inout, circulo, elipse, rect_red, h01
from mundo_comun import Sup, pop, ventana, campana, smooth_arr
from anclas import A
import kit_grav as KG

XS = np.arange(-4800, 4800, 40.0)
X_CASA = -1250.0
X_ARBOL_5M = -490.0
X_BANCO = -720.0
X_MESA_CAFE = -395.0
X_BICI = -265.0
X_COSTA = 1420.0
X_MONTE = -3100.0
H_MONTE = 1250.0

C_CIELO = ((66, 134, 226), (174, 216, 252))
C_CIELO_VIENTO = ((52, 108, 198), (144, 196, 240))

DELGADO = [False]


# ======================================================================== relieve y suelo
def _mont(X, relieve=1.0):
    X = np.asarray(X, float)
    m = (H_MONTE * np.exp(-((X - X_MONTE) / 540) ** 2)
         + 740 * np.exp(-((X + 4100) / 460) ** 2)
         + 310 * np.exp(-((X + 2350) / 290) ** 2))
    return m * relieve


def suelo_h(X, relieve=1.0):
    """Altura del suelo firme (y fondo del mar a la derecha de X_COSTA)."""
    X = np.asarray(X, float)
    parque = (5 * np.sin(X / 160) + 3 * np.sin(X / 65 + 1)) * np.clip((-220 - X) / 200, 0, 1)
    playa = -24 * smooth_arr((X - 1220) / 210)
    hondo = -1150 * smooth_arr((X - X_COSTA) / 920) + 32 * np.sin(X / 210) * smooth_arr((X - 1900) / 500)
    return _mont(X, relieve) + parque + playa + hondo


# ======================================================================== cielo y capas con paralaje
def cielo(t, est):
    import fondos as F
    v = est.get("viento", 0.0)
    arr = mezcla(C_CIELO[0], C_CIELO_VIENTO[0], v * 0.65)
    aba = mezcla(C_CIELO[1], C_CIELO_VIENTO[1], v * 0.65)
    return F.degradado(t, tuple(c / 255 for c in arr), tuple(c / 255 for c in aba))


SOL_X, SOL_H = 850.0, 22000.0


def sol_paisaje(lz, t, S):
    Ss = S.par(0.04)
    x, y = Ss.pt(SOL_X, SOL_H)
    r = 2150 * Ss.k
    if -r * 4 < x < W + r * 4 and -r * 4 < y < H + r * 4:
        P.sol(lz, x, y, r, t)


_NUBES = [(-5600, 2100, 1.25), (-3800, 2450, 1.0), (-2100, 1980, 1.4), (-600, 2320, 1.15),
          (900, 2080, 1.35), (2400, 2420, 1.05), (4100, 2150, 1.25), (5800, 2380, 1.1)]


def nubes(lz, t, S, est):
    Sn = S.par(0.3)
    v = est.get("viento", 0.0)
    desp_v = est.get("deriva", 0.0) * 420.0
    sube_v = v * 180.0
    for i, (nx, nh, s) in enumerate(_NUBES):
        X = nx + 28 * t + desp_v * (0.7 + 0.2 * (i % 3))
        Hh = nh + sube_v * (0.6 + 0.3 * (i % 2))
        x, y = Sn.pt(X, Hh)
        if -500 < x < W + 500 and -300 < y < H + 200:
            with Sn.en(lz, X, Hh, s * 3.0):
                KG.nube(lz, 0, 0, 1.0, (255, 255, 255), alfa=0.92, seed=i)


_XL = np.arange(-12000, 12000, 110.0)
_CORD = 1380 + 480 * np.sin(_XL / 860) + 340 * np.sin(_XL / 390 + 1.2) + 190 * np.sin(_XL / 180 + 0.5)
_CERROS = 640 + 210 * np.sin(_XL / 520 + 0.7) + 130 * np.sin(_XL / 240 + 2.1)
_LOMAS = 290 + 95 * np.sin(_XL / 410 + 1.5) + 55 * np.sin(_XL / 170 + 0.3)


def capas_lejanas(lz, t, S, est):
    v = est.get("viento", 0.0)
    # 1. Cordillera azulada lejana (paralaje 0.20)
    Sc = S.par(0.20)
    x0, x1 = Sc.rango_x(400)
    m = (_XL >= x0 - 200) & (_XL <= x1 + 200)
    if m.sum() > 2:
        Xc, Hc = _XL[m], _CORD[m]
        base = np.full_like(Xc, -200.0)
        lz.relleno(Sc.poly(np.concatenate([np.stack([Xc, Hc], 1), np.stack([Xc[::-1], base[::-1]], 1)])),
                   (132, 166, 224))
    # 2. Cerros medios con pinos y aerogeneradores (paralaje 0.45)
    Sm = S.par(0.45)
    x0, x1 = Sm.rango_x(350)
    m = (_XL >= x0 - 200) & (_XL <= x1 + 200)
    if m.sum() > 2:
        Xc, Hc = _XL[m], _CERROS[m]
        base = np.full_like(Xc, -200.0)
        lz.relleno(Sm.poly(np.concatenate([np.stack([Xc, Hc], 1), np.stack([Xc[::-1], base[::-1]], 1)])),
                   (96, 162, 154))
        for xp in range(-2800, 2600, 260):
            if x0 - 100 < xp < x1 + 100:
                hp = float(640 + 210 * math.sin(xp / 520 + 0.7) + 130 * math.sin(xp / 240 + 2.1))
                with Sm.en(lz, xp, hp - 10, 1.05):
                    KG.pino(lz, 0, 0, 1.0, (68, 138, 122), incl=0.14 * v + 0.03 * math.sin(t * 2 + xp))
        for xa in (-1550, -980, 1180, 1680):
            if x0 - 150 < xa < x1 + 150:
                ha = float(640 + 210 * math.sin(xa / 520 + 0.7) + 130 * math.sin(xa / 240 + 2.1))
                with Sm.en(lz, xa, ha - 8, 1.2):
                    KG.aerogenerador(lz, 0, 0, 1.0, t, vel=1.4 + 3.5 * v)
    # 3. Lomas verdes cercanas y silueta de edificios (paralaje 0.72)
    Sl = S.par(0.72)
    x0, x1 = Sl.rango_x(300)
    m = (_XL >= x0 - 200) & (_XL <= x1 + 200)
    if m.sum() > 2:
        Xc, Hc = _XL[m], _LOMAS[m]
        base = np.full_like(Xc, -200.0)
        lz.relleno(Sl.poly(np.concatenate([np.stack([Xc, Hc], 1), np.stack([Xc[::-1], base[::-1]], 1)])),
                   (78, 168, 118))
        # Skyline urbano detrás de la avenida
        for xb, wb, hb, col in ((-180, 130, 320, (108, 132, 192)), (10, 150, 410, (94, 118, 182)),
                                (210, 120, 290, (116, 140, 198)), (460, 160, 380, (88, 112, 176)),
                                (720, 140, 340, (104, 128, 188)), (960, 130, 270, (118, 142, 202))):
            if x0 - 200 < xb < x1 + 200:
                with Sl.en(lz, xb, 180, 1.0):
                    lz.relleno(rect_red(-wb / 2, -hb, wb, hb + 120, 8), col)
                    for r in range(4):
                        for c in range(3):
                            wx = -wb / 2 + 22 + c * ((wb - 44) / 2.2)
                            wy = -hb + 28 + r * 58
                            lz.relleno(rect_red(wx, wy, 18, 28, 3), (196, 226, 255), alfa=0.65)


# ======================================================================== terreno, estratos y mar
ESTRATOS = [(-38, -145, (148, 102, 82)), (-145, -170, (168, 118, 94)), (-170, -410, (130, 90, 80)),
            (-410, -860, (110, 78, 82)), (-860, -1800, (88, 62, 78))]


def terreno(lz, t, S, est, rel=1.0):
    x0, x1 = S.rango_x(300)
    m = (XS >= x0 - 80) & (XS <= x1 + 80)
    X = XS[m] if m.sum() > 2 else XS
    top = suelo_h(X, rel)
    fondo = -2200.0
    if DELGADO[0]:
        base = np.minimum(top, 0.0) - 70
        lz.relleno(S.poly(np.concatenate([np.stack([X, top], 1), np.stack([X[::-1], base[::-1]], 1)])), (92, 182, 110))
        mm = top > 120
        if mm.sum() > 2:
            Xm, Tm = X[mm], top[mm]
            lz.relleno(S.poly(np.concatenate([np.stack([Xm, Tm], 1), np.stack([Xm[::-1], np.full(mm.sum(), 60.0)], 1)])),
                       (148, 134, 170))
        return
    Pt = S.poly(np.concatenate([np.stack([X, top], 1), [[X[-1], fondo], [X[0], fondo]]]))
    lz.relleno(Pt, (120, 86, 78))
    with lz.recorte(Pt):
        ref = np.minimum(top, 0.0)
        ond = 22 * np.sin(X / 290)
        for h0, h1, c in ESTRATOS:
            if S.vis(x0, x1, float(ref.min()) + h1 - 40, h0 + 60):
                lz.relleno(S.poly(np.concatenate([np.stack([X, ref + h0 + ond], 1), np.stack([X[::-1], (ref + h1 + ond)[::-1]], 1)])), c)
        # Piel de pasto sobre tierra firme
        mt = (X < X_COSTA - 120) & (top < 380)
        cortes = np.flatnonzero(np.diff(mt.astype(int)) != 0) + 1
        for seg in np.split(np.arange(len(X)), cortes):
            if len(seg) < 3 or not mt[seg[0]]:
                continue
            Xt, Tt = X[seg], top[seg]
            lz.relleno(S.poly(np.concatenate([np.stack([Xt, Tt + 4], 1), np.stack([Xt[::-1], (Tt - 36)[::-1]], 1)])), (92, 184, 110))
            lz.relleno(S.poly(np.concatenate([np.stack([Xt, Tt + 4], 1), np.stack([Xt[::-1], (Tt - 14)[::-1]], 1)])), (118, 206, 126))
        # Arena de la playa junto a la costa
        mp = (X >= X_COSTA - 260) & (X <= X_COSTA + 220)
        if mp.sum() > 2:
            Xp, Tp = X[mp], top[mp]
            lz.relleno(S.poly(np.concatenate([np.stack([Xp, Tp + 4], 1), np.stack([Xp[::-1], (Tp - 42)[::-1]], 1)])), (242, 212, 152))


def mar(lz, t, S, est):
    if not S.vis(X_COSTA - 120, 4600, -1300, 520):
        return
    b_mar = est.get("burbujas_mar", 0.0)
    imp = est.get("impacto_a", 0.0)
    Xm = np.arange(X_COSTA - 40, 4400, 36.0)
    # Cuando las olas se levantan sin gravedad, el nivel del mar baja un poco y se ondula fuerte
    ola = (12 + 28 * b_mar + 22 * imp) * np.sin(Xm / 95 - t * 2.8) + 8 * np.cos(Xm / 48 + t * 3.6)
    nivel = -14.0 - 42.0 * b_mar + ola
    fondo = np.full_like(Xm, -80.0) if DELGADO[0] else suelo_h(Xm) - 20
    P_mar = S.poly(np.concatenate([np.stack([Xm, nivel], 1), np.stack([Xm[::-1], fondo[::-1]], 1)]))
    lz.relleno(P_mar, (36, 128, 212), alfa=0.90)
    # Franja superficial clara de espuma
    esp = nivel - 18
    lz.relleno(S.poly(np.concatenate([np.stack([Xm, nivel + 2], 1), np.stack([Xm[::-1], esp[::-1]], 1)])), (132, 212, 252), alfa=0.85)
    if DELGADO[0]:
        return
    # Grandes burbujas flotantes que se despegan del mar y de los charcos en viento_mar
    if b_mar > 0.01:
        der = est.get("deriva", 0.0) * 160.0
        datos_b = [
            (X_COSTA + 120, 160, 46, 1),
            (X_COSTA + 260, 290, 64, 2),
            (X_COSTA + 420, 210, 52, 3),
            (X_COSTA + 580, 350, 72, 4),
            (X_COSTA + 760, 250, 48, 5),
            (X_COSTA + 190, 85, 28, 6),
            (X_COSTA + 350, 125, 34, 7),
            (X_COSTA + 510, 140, 30, 8),
        ]
        for bx, bh, br, sd in datos_b:
            Xb = bx + der * (0.6 + 0.1 * sd) + 14 * math.sin(t * 1.8 + sd)
            Hb = -10 + bh * b_mar + 12 * math.cos(t * 2.3 + sd) * b_mar
            x, y = S.pt(Xb, Hb)
            KG.burbuja_agua(lz, x, y, br * S.k * min(1.0, b_mar * 1.35), t, seed=sd, col=(58, 166, 238), alfa=0.88)
    # Salpicaduras gigantes al caer el agua en caida_a
    if imp > 0.02:
        for k in range(10):
            xs = X_COSTA + 110 + k * 75
            hs = (120 + 60 * (k % 3)) * math.sin(imp * math.pi)
            x, y = S.pt(xs, hs)
            KG.burbuja_agua(lz, x, y, (16 + 6 * (k % 3)) * S.k, t, seed=20 + k, col=(168, 226, 255), alfa=0.8 * imp)


# ======================================================================== zonas del paisaje: casa, parque, avenida, costa
def zona_casa(lz, t, S, est):
    if DELGADO[0] or not S.vis(X_CASA - 350, X_CASA + 350, -40, 420):
        return
    base = float(suelo_h(X_CASA))
    # Cerca blanca de jardín a los lados
    for xc in range(int(X_CASA - 310), int(X_CASA - 215), 26):
        with S.en(lz, xc, float(suelo_h(xc)), 1.0):
            lz.relleno(rect_red(-5, -52, 10, 52, 3), (242, 244, 252))
    with S.en(lz, X_CASA, base, 1.0):
        KG.casa_corte(lz, 0, 0, 1.0, t, alt_casa=est.get("alt_casa", 0.0))


def zona_parque(lz, t, S, est):
    if DELGADO[0] or not S.vis(-980, -160, -40, 460):
        return
    v = est.get("viento", 0.0)
    alt_c = est.get("alt_cosas", 0.0)
    der = est.get("deriva", 0.0)
    # Sendero del parque
    Xp = np.linspace(-960, -180, 30)
    Tp = suelo_h(Xp)
    lz.relleno(S.poly(np.concatenate([np.stack([Xp, Tp + 3], 1), np.stack([Xp[::-1], (Tp - 10)[::-1]], 1)])), (226, 198, 156))

    # Árboles del parque (el de X_ARBOL_5M mide ~290 u = 5 metros de referencia)
    for xa, sa, sd in ((-880.0, 1.05, 1), (X_ARBOL_5M, 1.22, 2), (-210.0, 0.95, 3)):
        if S.vis(xa - 160, xa + 160, 0, 360):
            incl = 0.14 * v + 0.025 * math.sin(t * 1.4 + sd)
            with S.en(lz, xa, float(suelo_h(xa)) - 4, sa, incl):
                P.arbol(lz, 0, 0, 1.0, t, hojas=(76, 178, 104), seed=sd)

    # Arbustos y flores
    for xb, sd in ((-810, 1), (-580, 2), (-330, 3)):
        with S.en(lz, xb, float(suelo_h(xb)) - 3, 0.85):
            KG.arbusto(lz, 0, 0, 1.0, (68, 166, 98), seed=sd)

    # Banca del parque
    if S.vis(X_BANCO - 100, X_BANCO + 100, 0, 120):
        with S.en(lz, X_BANCO, float(suelo_h(X_BANCO)) - 2, 0.95):
            for xx in (-56, 56):
                lz.relleno(rect_red(xx - 5, -42, 10, 42, 3), (74, 70, 98))
            lz.relleno(rect_red(-74, -48, 148, 11, 4), (186, 118, 82))
            lz.relleno(rect_red(-74, -76, 148, 11, 4), (204, 134, 94))
            lz.relleno(rect_red(-74, -92, 148, 11, 4), (186, 118, 82))

    # Farolas
    for xf in (-790.0, -350.0):
        with S.en(lz, xf, float(suelo_h(xf)) - 2, 0.95):
            KG.farola(lz, 0, 0, 1.0, on=0.25)

    # Mesa pequeña de terraza y taza de café (sube en cámara lenta en version_a; en cierre se cae al piso)
    hm = float(suelo_h(X_MESA_CAFE)) - 2
    with S.en(lz, X_MESA_CAFE, hm, 1.0):
        lz.relleno(rect_red(-28, -6, 56, 6, 3), (78, 74, 104))
        lz.relleno(rect_red(-4, -64, 8, 60, 3), (96, 92, 124))
        lz.relleno(rect_red(-42, -70, 84, 8, 4), (238, 224, 204))
    caida_taza = est.get("caida_taza", 0.0)
    if caida_taza > 0.01:
        # En el cierre: la taza cae de la mesa al piso
        xt = X_MESA_CAFE + 26 * min(1.0, caida_taza * 1.2)
        ht = hm + 70 * (1.0 - caida_taza) + 8 * abs(math.sin(caida_taza * math.pi * 2)) * (1.0 - caida_taza)
        rot_t = caida_taza * 1.45
        with S.en(lz, xt, ht, 0.95, rot_t):
            KG.taza_cafe(lz, 0, 0, 1.0, t, ingravidez=0.0)
    else:
        xt = X_MESA_CAFE + der * 95.0 + 8 * math.sin(t * 1.9) * alt_c
        ht = hm + 70 + alt_c * 175.0
        rot_t = 0.28 * math.sin(t * 1.6) * alt_c
        with S.en(lz, xt, ht, 0.95, rot_t):
            KG.taza_cafe(lz, 0, 0, 1.0, t, ingravidez=alt_c)

    # Bicicleta que sube en cámara lenta con las ruedas girando
    xb = X_BICI + der * 115.0
    hb = float(suelo_h(X_BICI)) + alt_c * 210.0 + 10 * math.sin(t * 2.1 + 1.0) * alt_c
    rot_b = -0.22 * alt_c + 0.08 * math.cos(t * 1.5) * alt_c
    with S.en(lz, xb, hb, 0.95, rot_b):
        KG.bicicleta(lz, 0, 0, 1.0, t, giro=1.0 + 1.5 * alt_c)


def zona_avenida(lz, t, S, est):
    if DELGADO[0] or not S.vis(-180, 1450, -50, 560):
        return
    v = est.get("viento", 0.0)
    b_mar = est.get("burbujas_mar", 0.0)
    der = est.get("deriva", 0.0)
    imp = est.get("impacto_a", 0.0)

    # Asfalto y líneas de carril
    Xa = np.linspace(-160, 1280, 40)
    Ta = suelo_h(Xa)
    lz.relleno(S.poly(np.concatenate([np.stack([Xa, Ta + 4], 1), np.stack([Xa[::-1], (Ta - 18)[::-1]], 1)])), (58, 56, 86))
    for xl in range(-120, 1220, 90):
        hl = float(suelo_h(xl))
        lz.relleno(S.poly([[xl, hl - 2], [xl + 46, hl - 2], [xl + 46, hl - 8], [xl, hl - 8]]), (248, 214, 92))

    # Edificios de fachada colorida estilo Kurzgesagt
    edificios = [
        (-40.0, 165, 310, (232, 118, 108), (255, 224, 152)),
        (210.0, 185, 380, (88, 164, 224), (218, 242, 255)),
        (490.0, 170, 330, (242, 178, 78), (255, 240, 190)),
        (770.0, 190, 410, (142, 106, 208), (228, 216, 255)),
    ]
    for xe, we, he, col, c_vent in edificios:
        if S.vis(xe - we, xe + we, 0, he + 40):
            he_s = float(suelo_h(xe))
            with S.en(lz, xe, he_s - 4, 1.0):
                lz.relleno(rect_red(-we / 2, -he, we, he, 10), col)
                lz.relleno(rect_red(we * 0.18, -he, we * 0.32, he, 6), oscurecer(col, 0.18))
                lz.relleno(rect_red(-we / 2 - 8, -he - 12, we + 16, 16, 6), oscurecer(col, 0.25))
                pisos = int(he // 68)
                for r in range(1, pisos):
                    for c in range(3):
                        wx = -we / 2 + 22 + c * ((we - 44) / 2.2)
                        wy = -he + r * 64 - 22
                        lz.relleno(rect_red(wx, wy, 26, 36, 5), c_vent)
                # Puerta en planta baja
                lz.relleno(rect_red(-22, -54, 44, 54, 6), oscurecer(col, 0.35))

    # Farolas de la avenida y foleo
    for xf in (90.0, 360.0, 640.0, 940.0):
        with S.en(lz, xf, float(suelo_h(xf)) - 2, 0.95):
            KG.farola(lz, 0, 0, 1.0, on=0.3)

    # Faro costero en X = 1230
    if S.vis(1120, 1380, 0, 420):
        with S.en(lz, 1230.0, float(suelo_h(1230.0)) - 4, 1.05):
            lz.relleno(np.array([[-38, 0], [38, 0], [24, -260], [-24, -260]], float), (244, 246, 255))
            for k, (y0, y1) in enumerate(((-65, -110), (-155, -200))):
                w0 = 38 - 14 * (-y0 / 260)
                w1 = 38 - 14 * (-y1 / 260)
                lz.relleno(np.array([[-w0, y0], [w0, y0], [w1, y1], [-w1, y1]], float), (232, 78, 86))
            lz.relleno(rect_red(-30, -274, 60, 16, 5), (56, 52, 84))
            lz.relleno(rect_red(-20, -304, 40, 30, 4), (255, 232, 128))
            lz.relleno(np.array([[-28, -304], [28, -304], [0, -334]], float), (232, 78, 86))
            lz.halo(0, -290, 95, (255, 232, 130), alfa=0.45)

    # Charcos de la calle que se convierten en burbujas flotantes en viento_mar
    for k, xp in enumerate((160.0, 560.0, 980.0)):
        hp = float(suelo_h(xp))
        if b_mar < 0.85:
            with S.en(lz, xp, hp + 2, 1.0 - 0.7 * b_mar):
                lz.relleno(elipse(0, 0, 48, 7, 0, 24), (72, 174, 242), alfa=0.8 * (1 - b_mar))
        if b_mar > 0.02:
            for j in range(3):
                xb = xp + der * 130 + (j - 1) * 34 + 10 * math.sin(t * 2.5 + k + j)
                hb = hp + (85 + 55 * j + 30 * k) * b_mar
                x, y = S.pt(xb, hb)
                KG.burbuja_agua(lz, x, y, (18 + 6 * j) * S.k * min(1.0, b_mar * 1.4), t, seed=30 + k * 3 + j)

    # Coches que se levantan y derivan de lado con el viento y la rotación terrestre
    coches_cfg = [
        (75.0, (238, 84, 96), False, 1.0, 0.95),
        (430.0, (64, 186, 172), True, 1.22, 1.15),
        (820.0, (248, 186, 64), False, 0.88, 1.05),
    ]
    for idx, (xc0, col, volt, f_alt, f_der) in enumerate(coches_cfg):
        sube_c = b_mar * 195.0 * f_alt
        xc = xc0 + der * 155.0 * f_der
        hc = float(suelo_h(xc0)) + sube_c + (10 * math.sin(t * 2.2 + idx) if b_mar > 0.05 else 0.0)
        rot_c = (0.26 * (1 if idx % 2 == 0 else -1) * b_mar
                 + 0.08 * math.sin(t * 1.9 + idx) * b_mar
                 + 0.06 * math.sin(imp * math.pi * 3) * imp)
        with S.en(lz, xc, hc, 0.92, rot_c):
            KG.coche_urbano(lz, 0, 0, 1.0, t, col=col, voltear=volt)
        # Polvo de impacto al caer en Segundo 5
        if imp > 0.02:
            with S.en(lz, xc, float(suelo_h(xc0)), 1.0):
                for d in (-75, -35, 35, 75):
                    r_p = (18 + abs(d) * 0.15) * math.sin(imp * math.pi)
                    lz.relleno(circulo(d * (1 + 0.4 * imp), -10 - 20 * imp, max(2.0, r_p), 16),
                               (224, 210, 196), alfa=0.65 * imp)


def rafagas_viento(lz, t, S, est):
    """Líneas de flujo de aire subiendo y derivando de lado durante viento_mar."""
    v = est.get("viento", 0.0)
    if DELGADO[0] or v <= 0.02:
        return
    x0, x1 = S.rango_x(100)
    for i in range(18):
        u = ((t * 0.85 + i * 0.17) % 1.0)
        Xb = x0 + (x1 - x0) * ((i * 0.37 + 0.13) % 1.0) + u * 220.0
        Hb = 40.0 + 360.0 * h01(i, 4) + u * 190.0
        pts = []
        for k in range(8):
            s = k / 7.0
            xx = Xb + s * 130.0
            hh = Hb + s * 65.0 + 12.0 * math.sin(s * math.pi * 2 + t * 5 + i)
            pts.append(S.pt(xx, hh))
        alfa = v * math.sin(u * math.pi) * 0.65
        if alfa > 0.02:
            lz.trazo(np.array(pts, float), (225, 244, 255, int(255 * alfa)), 4.0, afinar=True)


def dibujar(lz, t, S, est, rel=1.0, sin_gente=False, tapa=None, delgado=False):
    """Dibuja todo el paisaje continuo. Si delgado=True, solo la piel superficial para el zoom al planeta."""
    DELGADO[0] = delgado
    import gente as G
    sol_paisaje(lz, t, S)
    nubes(lz, t, S, est)
    capas_lejanas(lz, t, S, est)
    terreno(lz, t, S, est, rel)
    mar(lz, t, S, est)
    if tapa is not None:
        tapa()
    zona_casa(lz, t, S, est)
    zona_parque(lz, t, S, est)
    zona_avenida(lz, t, S, est)
    if not sin_gente:
        G.gente(lz, t, S, est)
    rafagas_viento(lz, t, S, est)
    DELGADO[0] = False
