# -*- coding: utf-8 -*-
"""GARGANTA 10,8-31,2 s: casi ninguna ballena puede (tres ballenas con barbas tachadas) → garganta estrecha (el buzo se atora,
el pez pasa) → 2021: la jorobada atrapa a un buzo y lo escupe → el cachalote sí: se traga un calamar gigante entero."""
import math

import numpy as np

from acuarela import (H, W, brillo, curva, degradado, e_back, e_in, e_out, elipse, forma, lavado, lerp, linea, mancha_pts, oscuridad,
                      pr, rayos, rgb, rotulo, suave, terminar)
from comun import FIN, INI, T0, T1, corte, desborde, fondo_agua, ww
from personajes import (BLANCO, buzo, burbuja, cachalote, calamar, destello, exclama, gota, kuri, mareo, nube_lluvia, pez, pregunta)
from utileria import jorobada

E = "garganta"
gNot, gNing, gTrag = ww(E, 0, "buena"), ww(E, 0, "ninguna"), ww(E, 0, "tragarte")
gGar, gEstr = ww(E, 0, "garganta"), ww(E, 0, "estrecha")
j2021, jJor, jAtr, jBoca, jEsc = ww(E, 1, "2021"), ww(E, 1, "jorobada"), ww(E, 1, "atrapó"), ww(E, 1, "boca"), ww(E, 1, "escupió")
cPero, cPuede, cCach = INI(E, 2), ww(E, 2, "puede"), ww(E, 2, "cachalote")
cTraga, cCalam, cEnt = ww(E, 2, "traga"), ww(E, 2, "calamares"), ww(E, 2, "enteros")
T_INI = T0(E)
T_GARG = gGar - 0.35                 # pasa a la garganta (corte por desborde)
T_JOR = INI(E, 1) - 0.25             # 2021
T_CACH = cPero - 0.2                 # el cachalote
T_FIN = T1(E)

ROJO = rgb("d84a3a")
CARNE, CARNE2, CARNE_OSC = rgb("e79a96"), rgb("c9676d"), rgb("4a1420")


# ------------------------------------------------------------ casi ninguna ballena
def ninguna(t):
    im = corte(fondo_agua(rgb("c6ece6"), rgb("3a7fa0"), rgb("4f93b2"), H + 400, seed=21), 120 + 30 * (t - T_INI))
    rayos(im, 560, -150, [1.7, 1.85, 2.0, 2.2], 1600, 120, rgb("fff4d0"), 0.18)
    filas = ((700, 0.55, rgb("3d4656"), 1), (1090, 0.48, rgb("566174"), -1), (1450, 0.6, rgb("45505f"), 1))
    for k, (y, s, c, d) in enumerate(filas):
        x = 540 + d * (60 - 50 * (t - T_INI)) + 20 * math.sin(t + k)
        jorobada(im, x, y + 12 * math.sin(t * 1.3 + k), s, t, sx=d, col=c, seed=1200 + 40 * k)
        tx = gNing + 0.25 + 0.3 * k            # tachadas una tras otra hasta «tragarte»
        if t > tx:
            u = pr(t, tx, tx + 0.18)
            u2 = pr(t, tx + 0.12, tx + 0.3)
            linea(im, [(x - 150, y - 110), (lerp(x - 150, x + 150, u), lerp(y - 110, y + 110, u))], 18, col=ROJO, seed=60 + k, t=t)
            if u2 > 0:
                linea(im, [(x + 150, y - 110), (lerp(x + 150, x - 150, u2), lerp(y - 110, y + 110, u2))], 18, col=ROJO, seed=70 + k, t=t)
    # el buzo y Kuri arriba, aliviados
    bx, by = 330 + 15 * math.sin(t), 330 + 12 * math.sin(t * 1.4)
    feliz = t > gNot + 0.2
    buzo(im, bx, by, 0.85, t, rot=-0.1, cara="feliz" if feliz else "normal", brazos=(1.2, 2.3 if feliz else 1.2), codos=(0.5, -0.3))
    kuri(im, 760, 300 + 15 * math.sin(t * 1.7), 0.9, t, cara="feliz" if feliz else "normal", brazos=(0.5, 1.8 if feliz else 0.5))
    if t > gNot:
        for k, (dx, dy) in enumerate(((-160, -150), (150, -60), (520, -120))):
            u = e_back(pr(t, gNot + 0.1 * k, gNot + 0.1 * k + 0.3))
            destello(im, bx + dx, by + dy, 0.8 * u * (1 - pr(t, gGar - 0.6, gGar - 0.3)), t, seed=1100 + k)
    return terminar(im, t)


# ------------------------------------------------------------ garganta estrecha
def _paredes(im, t, apr):
    """Garganta en corte: paredes de carne que se estrechan hasta un tubo de ~70 px."""
    degradado(im, rgb("6d2434"), rgb("1c0710"), 0, H)
    lavado(im, mancha_pts(540, 380, 420, 5, 0.3, ry=260), rgb("b85864"), 0.4, 5, humedo=18)
    a = 6 * apr * math.sin(t * 9)
    for d in (-1, 1):
        def X(v):
            return 540 + d * v
        pared = [(X(560), 300), (X(560), 1920), (X(36 - a), 1920), (X(36 - a), 1360), (X(80 - a), 1150), (X(250), 700), (X(560), 480)]
        forma(im, curva(pared, 6, True), CARNE, t, 400 + d, tinta=6, sombra=(CARNE2, -d * 26, 0, 0.7), luz=(BLANCO, d * 10, 0, 0.12),
              humedo=8)
        for k in range(6):                     # pliegues
            yk = 760 + 160 * k
            xk = X(280 + 30 * (k % 2)) if yk < 1150 else X(200)
            linea(im, curva([(xk, yk), (X(150 + 40 * (k % 3)), yk + 30), (X(90 + 20 * (k % 2)), yk + 90)], 5), 4, col=CARNE_OSC,
                  seed=410 + 10 * k + d, t=t, alfa=0.6)


def garganta(t):
    im = np.zeros((H, W, 3), np.float32)
    apr = pr(t, gEstr - 0.05, gEstr + 0.1)
    # el pez baja y cabe sin problema
    up = pr(t, T_GARG + 0.1, gEstr - 0.2)
    if 0 < up < 1:
        pass
    _paredes(im, t, apr)
    if 0 < up < 1:
        fx = 540 + 30 * math.sin(up * 9)
        fy = lerp(560, 1900, e_in(up))
        pez(im, fx, fy, 0.9 * (1 - 0.35 * pr(up, 0.5, 0.7)), t, rgb("f2b544"), seed=870)
        # se dibuja bajo las paredes en el tubo: tapa con paredes otra vez si está en el tubo
        if fy > 1340:
            _paredes_frente(im, t, apr)
    # el buzo baja de cabeza y se atora donde la garganta mide lo que su cabeza
    ub = pr(t, gGar - 0.1, gEstr)
    hy = lerp(250, 1110, e_out(ub)) + 10 * apr * math.sin(t * 30)
    atorado = t > gEstr - 0.05
    buzo(im, 540 + 6 * apr * math.sin(t * 27), hy - 134 * 1.1, 1.1, t, rot=math.pi, cara="apretados" if atorado else "susto",
         brazos=(2.6, 2.6), codos=(0.2, -0.2), patada=2.2 if atorado else 1.0, vel=18 if atorado else 7, apretado=0.7 * apr)
    _paredes_frente(im, t, apr)
    if atorado:
        for k in range(3):
            gota(im, 540 + (-150 + 150 * k), hy - 260 - 30 * math.sin(t * 5 + k), 0.45, t, 1060 + k)
        rotulo(im, "¡ATORADO!", 540, 520, 96, rgb("f7e3b5"), t, seed=9, rot=-0.06, esc=e_back(pr(t, gEstr, gEstr + 0.25)))
    kuri(im, 830, 380 + 20 * math.sin(t * 2), 0.95, t, cara="susto" if atorado else "normal", brazos=(1.0, 1.0))
    return terminar(im, t)


def _paredes_frente(im, t, apr):
    """Labios de las paredes por delante (tapan los bordes de lo que entra en el tubo)."""
    a = 6 * apr * math.sin(t * 9)
    for d in (-1, 1):
        def X(v):
            return 540 + d * v
        labio = [(X(36 - a), 1920), (X(36 - a), 1360), (X(80 - a), 1150), (X(130), 1000), (X(150), 1000), (X(105), 1150),
                 (X(62), 1360), (X(62), 1920)]
        forma(im, curva(labio, 5, True), CARNE * 0.96, t, 430 + d, tinta=5, humedo=4)


# ------------------------------------------------------------ 2021: la jorobada
BUZO2 = dict(traje=rgb("b8443a"), traje_osc=rgb("6f2722"), franja=rgb("f2d16a"), pelo=rgb("1f1a18"))


def jorobada_2021(t):
    im = corte(fondo_agua(rgb("e1f4ee"), rgb("4b97ad"), rgb("6aa9bf"), H + 300, seed=31), 60)
    # superficie con luz
    lavado(im, curva([(0, 0), (1080, 0), (1080, 210 + 10 * math.sin(t * 2)), (540, 230), (0, 205)], 6, True), rgb("fbfaf2"), 0.6, 33,
           humedo=12)
    linea(im, [(x, 214 + 10 * math.sin(t * 2 + x * 0.01)) for x in range(-20, 1110, 40)], 5, seed=34, t=t, punta=False, alfa=0.7)
    rayos(im, 600, 200, [1.75, 1.9, 2.05, 2.2], 1600, 110, rgb("fff4d0"), 0.2)
    # el «2021» pintado
    if t > j2021 - 0.05:
        u = e_back(pr(t, j2021 - 0.05, j2021 + 0.25))
        sale = 1 - pr(t, jEsc - 0.6, jEsc - 0.3)
        rotulo(im, "2021", 540, 420, 190, rgb("f4cf5a"), t, seed=12, rot=-0.04, esc=u * sale)
        if sale > 0:
            destello(im, 820, 330, 0.7 * u * sale, t, seed=1120)
    # el buzo (otro: traje rojo)
    dentro_boca = jAtr - 0.05 < t < jEsc
    escupido = t >= jEsc
    bx, by = 540 + 20 * math.sin(t), 900 + 12 * math.sin(t * 1.5)
    # la jorobada sube con la boca abierta
    rise = e_out(pr(t, jJor - 0.5, jAtr))
    baja = e_in(pr(t, jEsc + 0.3, T_CACH))
    s = 1.3
    r = -math.pi / 2 + 0.15
    wx = 446
    wy = lerp(H + 900, 1517, rise) + 900 * baja
    abre = suave(pr(t, jJor - 0.2, jJor + 0.4)) * (1 - suave(pr(t, jAtr + 0.05, jAtr + 0.5)) * 0.9)
    if t > jEsc - 0.05:
        abre = 0.1 + 0.7 * math.sin(math.pi * pr(t, jEsc - 0.05, jEsc + 0.7))

    def dentro(img, T):
        if dentro_boca:
            buzo(img, bx, by, 0.9, t, cara="susto", brazos=(2.2, 2.2), patada=1.8, vel=14, seed=150, **BUZO2)

    if not dentro_boca and not escupido:
        buzo(im, bx, by, 0.9, t, cara="susto" if t > jJor else "normal", brazos=(1.0, 1.0), seed=150, **BUZO2)
    if t > jJor - 0.6:
        T = jorobada(im, wx, wy, s, t, rot=r, abre=abre, dentro=dentro, ojo="cerrado" if jBoca < t < jBoca + 0.2 else "abierto")
        if dentro_boca and abre < 0.3:                 # aletas que asoman entre las mandíbulas
            for k, d in enumerate((-1, 1)):
                px, py = T(np.array([(500, 4)], np.float32))[0]
                pts = np.array([(0, 0), (20, -60), (44, -50), (34, 0)], np.float32)
                ang = 0.3 * math.sin(t * 14 + k * 3)
                c, si = math.cos(ang + d * 0.4), math.sin(ang + d * 0.4)
                q = np.stack([pts[:, 0] * c - pts[:, 1] * si, pts[:, 0] * si + pts[:, 1] * c], 1) + (px - 10 + 26 * d, py + 4)
                forma(im, q, rgb("ef7b3c"), t, 160 + k, tinta=3.6)
    if jBoca + 0.3 < t < jEsc:
        pregunta(im, 820, 760, 1.2 * e_back(pr(t, jBoca + 0.3, jBoca + 0.6)), t)
    if escupido:                                         # sale disparado, girando, mareado
        u = pr(t, jEsc, jEsc + 1.0)
        ex, ey = lerp(bx, 700, e_out(u)), lerp(by, 380, e_out(u))
        buzo(im, ex, ey, 0.9, t, rot=t * 9 * (1 - u) + 0.3, cara="mareo", brazos=(2.0, 2.0), seed=150, **BUZO2)
        mareo(im, ex, ey - 200, 0.9, t)
        for k in range(10):
            e = t - jEsc
            if e < 1.5:
                burbuja(im, bx + 60 * math.cos(k) * e * 3, by - e * 260 + 40 * math.sin(k * 2), 8 + 4 * (k % 3), t, seed=170 + k)
    return terminar(im, t)


# ------------------------------------------------------------ el cachalote sí puede
def cachalote_si(t):
    im = corte(fondo_agua(rgb("2e5d7e"), rgb("08182c"), rgb("16344f"), H + 300, seed=41, alfa=0.45), 100)
    rg = np.random.default_rng(3)
    for k in range(40):                                  # nieve marina
        x = (rg.uniform(0, W) + 12 * math.sin(t * 0.5 + k)) % W
        y = (rg.uniform(0, H) + 25 * t) % H
        brillo(im, x, y, 3 + 2 * (k % 3), rgb("cfe8f0"), 0.35)
    ent = e_out(pr(t, T_CACH, cCach))
    s = 1.25
    wx, wy = lerp(1750, 860, ent), 1260 + 14 * math.sin(t * 1.2)
    boca = suave(pr(t, cCalam - 0.1, cCalam + 0.4)) * (1 - suave(pr(t, cEnt + 0.2, cEnt + 0.6)))
    trago = pr(t, cEnt + 0.4, T_FIN + 0.5)
    # el calamar llega por arriba y la boca lo aspira entero (encima del cachalote hasta entrar en la boca)
    mx, my = wx - 470 * s, wy + 70 * s
    cal = None
    if cTraga - 0.4 < t < cEnt + 0.5:
        a = e_back(pr(t, cTraga - 0.4, cTraga))
        u = e_in(pr(t, cCalam + 0.3, cEnt + 0.4))
        qx = lerp(230, mx - 40, u) + 20 * math.sin(t * 2) * (1 - u)
        qy = lerp(820, my + 20, u)
        cal = (qx, qy, 0.9 * a * (1 - 0.85 * u), lerp(-0.3, -1.5, u), 1 + 2 * u)
    cachalote(im, wx, wy, s, t, sx=-1, boca=boca, bulto=(0.05 + 0.5 * suave(trago), 1.0) if trago > 0 else None,
              col=rgb("566582"), ojo="cerrado" if cEnt + 0.5 < t < cEnt + 1.1 else "abierto")
    if cal is not None:
        calamar(im, cal[0], cal[1], cal[2], t, rot=cal[3], ondas=cal[4])
    bx_, by_ = wx - 330 * s, wy + 40 * s
    brillo(im, bx_, by_, 40, rgb("cfe8f0"), 0.25 * (0.6 + 0.4 * math.sin(t * 3)))
    if t > cCach - 0.1:
        rotulo(im, "CACHALOTE", 620, 640, 128, rgb("f6efe0"), t, seed=14, rot=-0.03, esc=e_back(pr(t, cCach - 0.1, cCach + 0.2)))
    # el buzo y Kuri miran desde arriba
    bx, by = 300 + 10 * math.sin(t), 380 + 10 * math.sin(t * 1.3)
    preoc = t > cEnt - 0.2
    buzo(im, bx, by, 0.75, t, cara="triste" if preoc else "susto", brazos=(0.4, 0.4), codos=(1.4, -1.4))
    kuri(im, 520, 330 + 12 * math.sin(t * 1.8), 0.75, t, cara="triste" if preoc else "susto")
    if t > cPuede:
        exclama(im, 520, 200, 0.9 * e_back(pr(t, cPuede, cPuede + 0.25)) * (1 - pr(t, cEnt - 0.4, cEnt - 0.2)), t)
    if preoc:
        nube_lluvia(im, bx, by - 250, 0.75 * e_back(pr(t, cEnt - 0.2, cEnt + 0.1)), t)
    return terminar(im, t)


def cuadro(t):
    if t < T_GARG:
        return ninguna(t)
    if t < T_GARG + 0.5:
        return desborde(ninguna(t), garganta(t), pr(t, T_GARG, T_GARG + 0.5), cx=540, cy=1150)
    if t < T_JOR:
        return garganta(t)
    if t < T_JOR + 0.5:
        return desborde(garganta(t), jorobada_2021(t), pr(t, T_JOR, T_JOR + 0.5), cx=540, cy=300)
    if t < T_CACH:
        return jorobada_2021(t)
    if t < T_CACH + 0.6:
        return desborde(jorobada_2021(t), cachalote_si(t), pr(t, T_CACH, T_CACH + 0.6), cx=1000, cy=1200, borde=(0.1, 0.1, 0.2))
    return cachalote_si(t)


def entrada(t, G):
    """Del plano de fuera del gancho a «casi ninguna ballena»."""
    return desborde(G.cuadro(t), ninguna(t), pr(t, T_INI, T_INI + 0.55), cx=300, cy=400)
