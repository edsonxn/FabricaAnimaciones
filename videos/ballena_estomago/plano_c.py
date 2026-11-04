# -*- coding: utf-8 -*-
"""ESTÓMAGO → CIERRE 31,2-75 s: cae al estómago (oscuridad, linterna y Kuri, 37 °C, paredes que aprietan) → el ácido (charco
verde, vapor en las botas, el dedo asoma por el guante) → el cachalote baja a 1 000 m (regla de profundidad) → presión ×100,
manómetro que se vacía, el O₂ se vuelve veneno → Kuri tiene la idea: ¡que te vomite! (picos de calamar) → atardecer: Kuri
abraza al buzo y la cola se despide; fundido a papel."""
import math

import numpy as np

from acuarela import (H, W, brillo, cinta, curva, degradado, e_back, e_in, e_out, elipse, forma, lavado, lerp, linea, mancha_pts,
                      oscuridad, pr, rgb, rotulo, suave, terminar)
from comun import FIN, INI, T0, T1, corte, desborde, fondo_agua, ww
from personajes import (AMARILLO, BLANCO, OJO_K, buzo, burbuja, cachalote, corazon, destello, exclama, gota, kuri, mareo, pregunta)
from utileria import bombilla, calavera, flecha, manometro, molecula_o2, pico_calamar, termometro, vapor

E, I, C = "estomago", "inmersion", "cierre"
T_INI = T0(E)
aCae, aOsc, a37, aPar, aApr = INI(E, 0), ww(E, 0, "oscuridad"), ww(E, 0, "37"), ww(E, 0, "paredes"), ww(E, 0, "aprietan")
bMas, bAcido, bTraje, bPiel, bNo = INI(E, 1), ww(E, 1, "acido"), ww(E, 1, "traje"), ww(E, 1, "piel"), ww(E, 1, "no")
iPeor, iCach, iBaja, iMil = INI(I, 0), ww(I, 0, "cachalote"), ww(I, 0, "baja"), ww(I, 0, "mil")
pPres, pCien, pTanq, pVac, pMin = ww(I, 1, "presion"), ww(I, 1, "cien"), ww(I, 1, "tanque"), ww(I, 1, "vacia"), ww(I, 1, "minuto")
pOxi, pVen = ww(I, 1, "oxigeno"), ww(I, 1, "veneno")
vSal, vVom, vPicos, vDig = ww(C, 0, "salida"), ww(C, 0, "vomite"), ww(C, 0, "picos"), ww(C, 0, "digerir")
zTu, zBuzo, zEres, zDif, zDig = INI(C, 1), ww(C, 1, "buzo"), ww(C, 1, "eres"), ww(C, 1, "dificil"), ww(C, 1, "digerir")
T_INM = T1(E)                     # afuera: el cachalote baja
T_PRES = pPres - 0.55             # adentro otra vez: la presión
T_FUERA = vVom + 0.35             # el vómito, visto desde fuera
T_ATAR = zTu - 0.25               # atardecer
T_FIN = T1(C)

CARNE, CARNE2, CARNE_OSC = rgb("c76a72"), rgb("9a4352"), rgb("3a0e1a")
ACIDO = rgb("9be05a")
ROJO = rgb("e0574a")


# ------------------------------------------------------------ el estómago (mundo alto con cámara vertical)
def _fondo_estomago():
    return fondo_agua(rgb("6a2236"), rgb("240710"), rgb("8c3a4c"), H + 900, seed=51, n=11, alfa=0.42)


def _paredes(im, t, cam, apr, sacude=0.0):
    """Paredes de músculo con pliegues a ambos lados; apr 0..1 las cierra hacia el centro y respiran."""
    for d in (-1, 1):
        borde = []
        for yw in np.arange(cam - 120, cam + H + 160, 80):
            gap = lerp(430, 175, apr) + 46 * math.sin(yw * 0.0055 + d * 1.3) + 12 * math.sin(t * 2.2 + yw * 0.01)
            gap += sacude * 40 * math.sin(t * 31 + yw * 0.02)
            borde.append((540 + d * gap, yw - cam))
        pared = [(540 + d * 700, borde[0][1]), *borde, (540 + d * 700, borde[-1][1])]
        forma(im, curva(pared, 4, True), CARNE, t, 2100 + d, tinta=6, sombra=(CARNE2, -d * 34, 0, 0.75),
              luz=(BLANCO, d * 10, 0, 0.1), humedo=8)
        for k in range(len(borde) - 1):            # pliegues (arrugas del estómago)
            if k % 2:
                continue
            x0, y0 = borde[k]
            linea(im, curva([(x0 + d * 30, y0 + 20), (x0 + d * 110, y0 + 46), (x0 + d * 210, y0 + 30)], 5), 5, col=CARNE_OSC,
                  seed=2110 + k + 50 * d, t=t, alfa=0.55)


def _charco(im, t, cam, brillo_f):
    """Charco de ácido verde en el fondo del estómago (mundo y ≈ 2240) que burbujea y brilla."""
    y = 2260 - cam
    if y > H + 200:
        return
    lavado(im, mancha_pts(540, y + 120, 520, 61, 0.12, ry=190), ACIDO * 0.55, 0.85, 61, humedo=14)
    forma(im, curva([(40, y + 10), (300, y - 26 + 6 * math.sin(t * 3)), (540, y - 14), (800, y - 30 + 6 * math.sin(t * 2.6)),
                     (1040, y + 6), (1100, y + 600), (-20, y + 600)], 6, True), ACIDO, t, 62, tinta=5, modo="lavado", alfa=0.75,
          luz=(BLANCO, 0, 16, 0.25))
    brillo(im, 540, y + 40, 420, ACIDO, 0.18 * brillo_f)
    for k in range(9):                             # burbujas que revientan
        u = (t * 0.8 + k * 0.37) % 1
        bx = 140 + 100 * k + 20 * math.sin(k * 5)
        r = 10 + 8 * (k % 3)
        if u < 0.75:
            forma(im, elipse(bx, y + 40 - 70 * u, r * (0.6 + u), r * (0.6 + u)), ACIDO * 1.15, t, 63 + k, tinta=2.6, alfa=0.9)
        else:
            destello(im, bx, y - 30, 0.35 * (1 - u) * 4, t, seed=70 + k, col=ACIDO, f=0.5)


def _pared_frente(im, t, cam):
    """Superficie del charco por delante de las botas."""
    y = 2260 - cam
    if y > H + 200:
        return
    forma(im, curva([(-20, y + 8), (300, y - 6 + 5 * math.sin(t * 3)), (540, y + 2), (800, y - 8 + 5 * math.sin(t * 2.6)),
                     (1100, y + 8), (1100, y + 400), (-20, y + 400)], 6, True), ACIDO * 0.9, t, 64, tinta=4, modo="lavado",
          alfa=0.6)


def _lupa(im, x, y, r, t, u, piel):
    """Círculo de detalle: el dedo asoma por el guante roto y se pone rojo (vapor del ácido)."""
    if u <= 0.02:
        return
    r = r * u
    forma(im, elipse(x, y, r + 12, r + 12), rgb("f6efe0"), t, 2150, tinta=6)
    GU, GU2 = rgb("2c6070"), rgb("163540")
    for k, (dx, L) in enumerate(((-66, 100), (-22, 130), (22, 136), (66, 120))):     # dedos del guante
        tip = (x + dx * u + 6 * k * u, y - L * u)
        forma(im, cinta([(x + dx * u, y + 20 * u), tip], 40 * u, 36 * u), GU, t, 2151 + k, tinta=4, luz=(BLANCO, -6, 6, 0.15))
        if k == 2:                                       # el roto: asoma la yema y se pone roja
            forma(im, elipse(tip[0], tip[1] - 4 * u, 17 * u, 19 * u), rgb("f4cfae") * (1 - piel) + ROJO * piel, t, 2156, tinta=3.4,
                  luz=(BLANCO, -4, 6, 0.3))
            linea(im, [(tip[0] - 20 * u, tip[1] + 12 * u), (tip[0] - 8 * u, tip[1] + 2 * u), (tip[0], tip[1] + 14 * u),
                       (tip[0] + 9 * u, tip[1] + 2 * u), (tip[0] + 20 * u, tip[1] + 12 * u)], 3.4, col=GU2, seed=2157, t=t)
    forma(im, elipse(x, y + 70 * u, 105 * u, 90 * u), GU, t, 2150 + 9, tinta=5, luz=(BLANCO, -10, 12, 0.15))
    forma(im, cinta([(x - 50 * u, y + 30 * u), (x - 140 * u, y - 30 * u)], 38 * u, 32 * u), GU, t, 2160 + 9, tinta=4)   # pulgar
    tip = (x + 34 * u, y - 136 * u)
    vapor(im, tip[0], tip[1] - 20 * u, 0.9 * u, t, n=3, seed=2158, alfa=piel)


def estomago(t):
    cam = 700 * suave(pr(t, bMas - 0.15, bAcido))
    im = corte(_fondo_estomago(), cam)
    apr = suave(pr(t, aPar, aApr + 0.2)) * (1 - suave(pr(t, bMas - 0.2, bMas + 0.6)) * 0.8)
    _paredes(im, t, cam, apr)
    _charco(im, t, cam, 1.0 + 0.5 * pr(t, bAcido, bAcido + 0.3))
    for k in range(3):                         # picos de calamar flotando en el ácido (lo que no digiere)
        pico_calamar(im, 190 + 330 * k + 20 * math.sin(t + k), 2330 - cam + 10 * math.sin(t * 1.5 + k), 0.9, t, rot=0.6 * k - 0.5 +
                     0.1 * math.sin(t + k), seed=1350 + 10 * k)
    # el buzo cae (gira un poco), rebota y luego resbala hasta el charco
    s = 1.35
    cae = pr(t, aCae - 0.2, aCae + 0.9)
    ywb = lerp(-400, 960, e_out(cae)) + 30 * math.sin(math.pi * pr(t, aCae + 0.9, aCae + 1.3))
    ywb = lerp(ywb, 2050, e_in(pr(t, bMas - 0.15, bMas + 0.9)))
    bx = 470 + 10 * math.sin(t * 1.1)
    by = ywb - cam + (0 if t > bMas else 8 * math.sin(t * 1.6))
    rot = 0.6 * (1 - cae) + 0.04 * math.sin(t * 1.4)
    acido = t > bMas + 0.9
    piel = pr(t, bPiel - 0.1, bPiel + 0.5)
    if t < aOsc:
        cara = "susto"
    elif t < aPar:
        cara = "abiertos"
    elif t < bMas:
        cara = "apretados"
    elif t < bPiel - 0.1:
        cara = "susto" if t < bTraje else "normal"
    else:
        cara = "susto"
    brazos = (2.4, 2.4) if t < aCae + 1.0 else ((1.3, 1.3) if t < aPar else (2.0, 2.0))
    if t > bPiel - 0.3:
        brazos = (0.6, lerp(1.0, 2.6, e_out(pr(t, bPiel - 0.3, bPiel))))
    buzo(im, bx, by, s, t, rot=rot, cara=cara, brazos=brazos, codos=(0.5, -1.2 if t > bPiel - 0.3 else -0.4), lampara=True,
         apretado=apr, patada=0.4 if acido else 1.0, guante_roto=piel)
    kx, ky = bx + 330 * (1 - 0.4 * apr), by - 260 + 18 * math.sin(t * 2)
    kc = "susto" if t < aPar else ("apretados" if t < bMas else ("triste" if t < bPiel else "susto"))
    ks = 1.0 * (1 - 0.2 * apr)
    kuri(im, kx, ky, ks, t, cara=kc, brazos=(1.2, 1.2))
    if acido:
        _pared_frente(im, t, cam)
        vapor(im, bx - 50, by + 270, 1.3, t, n=4, seed=2010)
        vapor(im, bx + 60, by + 270, 1.2, t + 0.4, n=3, seed=2020)
    # luz: la linterna del buzo, Kuri y el brillo del ácido
    nivel = 0.5 + 0.36 * pr(t, aOsc - 0.1, aOsc + 0.2)
    lx, ly = bx, by - 230 * s
    barrido = -0.4 + 0.8 * math.sin(t * 0.8) if t < aPar else (math.pi / 2 if t > bMas else 0.0)
    luces = [(kx, ky, 300, 0.95), (bx, by, 380, 0.55)]
    if t > bMas:
        luces.append((540, 2300 - cam, 750, 0.9))
    oscuridad(im, nivel, luces=luces, conos=[(lx, ly, barrido, 0.34, 1000, 0.9 * pr(t, aOsc + 0.15, aOsc + 0.3))])
    kuri(im, kx, ky, ks, t, cara=kc, brazos=(1.2, 1.2), aura=False)     # Kuri brilla sobre la oscuridad
    # rótulos y utilería por encima de la oscuridad
    if a37 - 0.15 < t < aPar + 0.4:
        u = e_back(pr(t, a37 - 0.15, a37 + 0.15)) * (1 - pr(t, aPar, aPar + 0.4))
        termometro(im, 200, 560, 1.6 * u, t, 0.85 * suave(pr(t, a37, a37 + 0.7)))
        rotulo(im, "37°C", 420, 430, 140, rgb("f7e3b5"), t, seed=21, rot=-0.06, esc=u)
        for k in range(2):
            gota(im, bx - 110 + 220 * k, by - 330 - 20 * math.sin(t * 4 + k), 0.5 * u, t, 2140 + k)
    if aPar < t < bMas:
        u = e_back(pr(t, aPar, aPar + 0.25)) * (1 - pr(t, bMas - 0.3, bMas))
        for k, d in enumerate((-1, 1)):
            flecha(im, 540 + d * 560, 640, 540 + d * 330, 640, 80 * u + 1, t, CARNE * 1.15, seed=2160 + k)
        rotulo(im, "¡APRIETA!", 540, 430, 110, rgb("f7e3b5"), t, seed=27, rot=0.05, esc=u)
    if bAcido - 0.05 < t < bPiel - 0.2:
        u = e_back(pr(t, bAcido - 0.05, bAcido + 0.25)) * (1 - pr(t, bPiel - 0.6, bPiel - 0.2))
        rotulo(im, "¡ÁCIDO!", 540, 640, 150, ACIDO, t, seed=22, rot=0.05, esc=u)
    if t > bPiel - 0.2:
        _lupa(im, 720, 620, 230, t, e_back(pr(t, bPiel - 0.2, bPiel + 0.15)), piel)
        exclama(im, 960, 400, 1.1 * e_back(pr(t, bPiel, bPiel + 0.25)), t)
    return terminar(im, t)


# ------------------------------------------------------------ afuera: el cachalote baja a 1 000 m
def _regla(im, t, prof):
    """Regla de profundidad pintada a la izquierda: 0 → 1 000 m con un marcador que baja."""
    x, y0, y1 = 120, 360, 1640
    linea(im, [(x, y0), (x, y1)], 8, col=BLANCO, seed=2200, t=t, punta=False, alfa=0.9)
    for k in range(5):
        y = lerp(y0, y1, k / 4)
        linea(im, [(x - 22, y), (x + 22, y)], 6, col=BLANCO, seed=2201 + k, t=t, punta=False, alfa=0.9)
        rotulo(im, f"{250 * k} m" if k in (0, 4) else str(250 * k), x + 90 if k in (0, 4) else x + 70, y, 40, BLANCO, t,
               seed=2210 + k, tinta=True)
    ym = lerp(y0, y1, prof)
    forma(im, np.array([(x - 14, ym), (x - 62, ym - 26), (x - 62, ym + 26)], np.float32), ROJO, t, 2220, tinta=3.6)
    brillo(im, x - 40, ym, 30, ROJO, 0.3)


def inmersion(t):
    prof = suave(pr(t, iBaja - 0.1, iMil + 0.7)) * 0.86 + 0.14 * pr(t, iMil + 0.7, T_PRES + 0.5)
    fondo = fondo_agua(rgb("8fd3e0"), rgb("02060d"), rgb("2c6688"), H + 2200, seed=52, n=14, alfa=0.4)
    im = corte(fondo, 2200 * prof)
    rg = np.random.default_rng(5)
    for k in range(46):                            # nieve marina que sube: se nota el descenso
        x = (rg.uniform(0, W) + 10 * math.sin(t * 0.6 + k)) % W
        y = (rg.uniform(0, H) - 1500 * prof - 15 * t) % H
        brillo(im, x, y, 3 + 2 * (k % 3), rgb("d8eef4"), 0.3)
    gira = suave(pr(t, iCach - 0.2, iBaja + 0.3))
    s = 0.95
    wx = 600 + 30 * math.sin(t * 0.7)
    wy = lerp(980, 1000, gira) + 14 * math.sin(t * 1.3)
    T = cachalote(im, wx, wy, s, t, rot=lerp(0.0, math.pi / 2 - 0.12, gira), col=rgb("5d6c88"), bulto=(0.55, 0.9))
    gx, gy = T(np.array([(-110, 100)], np.float32))[0]
    pul = 0.6 + 0.4 * math.sin(t * 4)
    oscuridad(im, 0.78 * prof, luces=[(gx, gy, 170, 0.8 * pul)])
    brillo(im, gx, gy, 80, OJO_K, 0.4 * pul * (0.4 + 0.6 * prof))     # Kuri brilla dentro de la panza
    _regla(im, t, prof)
    if t > iMil - 0.1:
        rotulo(im, "1 000 m", 640, 330, 150, rgb("f6efe0"), t, seed=23, rot=-0.04, esc=e_back(pr(t, iMil - 0.1, iMil + 0.2)))
    return terminar(im, t)


# ------------------------------------------------------------ adentro: presión ×100, el tanque se vacía, O₂ veneno
def presion(t, sacude=0.0):
    im = corte(_fondo_estomago(), 200)
    apr = 0.55 + 0.12 * math.sin(t * 5) * pr(t, pPres, pPres + 0.3) + 0.4 * sacude
    _paredes(im, t, 200, min(apr, 1), sacude)
    bx, by = 520, 1050
    ven = pr(t, pVen - 0.1, pVen + 0.3)
    cara = "apretados" if t < pVen else "mareo"
    if t < T_FUERA and t > vSal - 0.3:
        cara = "abiertos"
    if sacude > 0:
        cara = "susto"
    buzo(im, bx, by, 1.25, t, cara=cara, brazos=(2.5, 2.5) if t < vSal - 0.3 else (1.1, 1.1), codos=(-0.6, 0.6), lampara=True,
         apretado=min(1, 0.4 + 0.5 * pr(t, pPres, pCien) + 0.15 * math.sin(t * 8)), patada=0.5, rot=0.05 * math.sin(t * 20) * sacude)
    # burbujas que escapan mientras el tanque se vacía
    vac = pr(t, pVac - 0.3, pMin + 0.2)
    if 0 < vac < 1.05:
        for k in range(8):
            u = (t * 1.6 + k / 8) % 1
            burbuja(im, bx + 20 + 40 * math.sin(k * 3 + u * 6), by - 260 - 500 * u, 8 + 5 * (k % 3), t, seed=2300 + k)
    kx, ky = 840, 800 + 20 * math.sin(t * 2)
    idea = t > vSal - 0.1
    kc = "feliz" if idea else ("susto" if t > pVen else "apretados")
    kb = (1.8, 1.8) if idea else (1.0, 1.0)
    lu = [(kx, ky, 260, 0.95), (bx, by, 360, 0.6)]
    if t > pOxi:
        lu.append((780, 440, 220, 0.7))
    if t > vSal - 0.1:
        lu.append((kx, ky - 230, 280, 0.9))
    if pTanq - 0.25 < t < pVen + 0.8:
        lu.append((280, 400, 280, 0.9))
    conos = [(bx, by - 290, -math.pi / 2 + 0.5 * math.sin(t * 0.9), 0.3, 800, 0.8)]
    oscuridad(im, 0.82, luces=lu, conos=conos)
    kuri(im, kx, ky, 0.95, t, cara=kc, brazos=kb)
    # por encima de la oscuridad: flechas de presión, ×100, manómetro, O2 → veneno, bombilla
    f = e_back(pr(t, pPres - 0.1, pPres + 0.25)) * (1 - pr(t, pVen + 0.4, pVen + 0.8))
    if f > 0:
        p = 30 * math.sin(t * 7)
        for k, (x0, y0, x1, y1) in enumerate(((-20, 1050, 250 + p, 1050), (1100, 1050, 800 - p, 1050), (520, 560, 520, 700 + p),
                                              (520, 1760, 520, 1420 - p))):
            flecha(im, x0, y0, lerp(x0, x1, f), lerp(y0, y1, f), 70, t, rgb("f2a33a"), seed=2400 + k)
    if pCien - 0.05 < t < pTanq:
        u = e_back(pr(t, pCien - 0.05, pCien + 0.2)) * (1 - pr(t, pTanq - 0.3, pTanq))
        rotulo(im, "×100", 540, 300, 230, rgb("f4cf5a"), t, seed=24, rot=-0.05, esc=u)
    if pTanq - 0.25 < t < pVen + 0.8:
        u = e_back(pr(t, pTanq - 0.25, pTanq + 0.1)) * (1 - pr(t, pVen + 0.4, pVen + 0.8))
        val = 1 - e_in(pr(t, pVac, pMin + 0.1)) + 0.03 * math.sin(t * 40) * pr(t, pVac, pMin)
        manometro(im, 280, 400, 160 * u, t, val)
        if val < 0.15:
            brillo(im, 280, 400, 240, ROJO, 0.35 * (0.5 + 0.5 * math.sin(t * 14)) * u)
            exclama(im, 470, 230, 0.9 * u, t, seed=1001, col=ROJO)
    if pOxi - 0.1 < t < vSal - 0.2:
        u = e_back(pr(t, pOxi - 0.1, pOxi + 0.2)) * (1 - pr(t, vSal - 0.6, vSal - 0.2))
        ox, oy = 790, 440 + 12 * math.sin(t * 2)
        molecula_o2(im, ox, oy, 1.2 * u, t, veneno=ven)
        rotulo(im, "OXÍGENO" if ven < 0.5 else "¡VENENO!", ox, oy + 110, 64, rgb("c9f2a8") if ven >= 0.5 else BLANCO, t, seed=28,
               esc=u)
        if ven > 0:
            calavera(im, ox, oy - 150, 1.4 * e_back(ven) * u, t, col=rgb("c9f2a8"))
    if t > pVen:
        mareo(im, bx, by - 340, 1.0, t)
    if idea and sacude == 0:
        bombilla(im, kx, ky - 230, 1.3 * e_back(pr(t, vSal - 0.1, vSal + 0.2)), t)
    if sacude > 0:
        rotulo(im, "¡BLAAAGH!", 540, 300, 150, ACIDO, t, seed=25, rot=0.08 * math.sin(t * 20), esc=e_back(pr(t, vVom - 0.1, vVom + 0.2)))
        dx = int(26 * sacude * math.sin(t * 47))
        dy = int(18 * sacude * math.sin(t * 39))
        im = np.roll(im, (dy, dx), (0, 1))
    return terminar(im, t)


# ------------------------------------------------------------ afuera: lo vomita con los picos de calamar
def vomito(t):
    im = corte(fondo_agua(rgb("4c8fb0"), rgb("0b2238"), rgb("2c6688"), H + 300, seed=53, alfa=0.42), 150)
    rg = np.random.default_rng(9)
    for k in range(30):
        x = (rg.uniform(0, W) + 10 * math.sin(t * 0.6 + k)) % W
        y = (rg.uniform(0, H) - 18 * t) % H
        brillo(im, x, y, 3 + 2 * (k % 3), rgb("d8eef4"), 0.3)
    s = 1.05
    wx, wy = 980, 1250 + 16 * math.sin(t * 1.2)
    t0 = T_FUERA + 0.1
    boca = suave(pr(t, t0 - 0.1, t0 + 0.25)) * (1 - 0.6 * suave(pr(t, vDig - 0.2, T_ATAR)))
    sac = math.sin(t * 25) * 0.05 * (1 - pr(t, t0, t0 + 1.0))
    T = cachalote(im, wx, wy, s, t, sx=-1, rot=sac, boca=boca, col=rgb("5d6c88"), ojo="cerrado" if t < t0 + 1.4 else "abierto")
    mx, my = T(np.array([(470, 110)], np.float32))[0]
    # chorro de vómito (lavado verdoso) en la dirección del disparo
    ch = pr(t, t0, t0 + 0.35) * (1 - pr(t, t0 + 1.2, t0 + 2.2))
    if ch > 0:
        lavado(im, mancha_pts(mx - 260, my - 160, 260 * ch, 81, 0.35, ry=150 * ch), rgb("b7c77a"), 0.45 * ch, 81, humedo=16)
    # los picos de calamar salen en abanico en «picos»
    for k in range(7):
        ts = vPicos - 0.5 + 0.12 * k
        if t > ts:
            u = pr(t, ts, ts + 3.2)
            ang = math.radians(150 + 22 * k)
            d = 620 * e_out(u)
            px = mx + d * math.cos(ang) * 1.0
            py = my - d * math.sin(ang) * 0.9 + 260 * u * u
            pico_calamar(im, px, py, 1.25 + 0.25 * (k % 2), t, rot=t * (3 + k), seed=1300 + 10 * k)
    if vPicos < t < vDig + 0.6:
        u = e_back(pr(t, vPicos, vPicos + 0.25)) * (1 - pr(t, vDig + 0.2, vDig + 0.6))
        rotulo(im, "PICOS DE CALAMAR", 540, 1720, 92, rgb("f6efe0"), t, seed=26, rot=-0.03, esc=u)
    # el buzo sale disparado girando, Kuri detrás
    u = pr(t, t0 + 0.05, t0 + 1.6)
    ex = lerp(mx - 30, 330, e_out(u)) + 12 * math.sin(t * 1.3)
    ey = lerp(my, 560, e_out(u)) + 10 * math.sin(t * 1.7)
    buzo(im, ex, ey, 1.0, t, rot=(1 - e_out(u)) * 9 + 0.15 * math.sin(t), cara="mareo", brazos=(2.2, 2.2), codos=(0.6, -0.6),
         patada=0.6)
    mareo(im, ex, ey - 220, 1.0, t)
    uk = pr(t, t0 + 0.35, t0 + 1.9)
    kx, ky = lerp(mx, 700, e_out(uk)), lerp(my, 420, e_out(uk)) + 14 * math.sin(t * 2.2)
    kuri(im, kx, ky, 0.85, t, cara="feliz", brazos=(2.0, 2.0))
    for k in range(10):
        e = t - t0
        if 0 < e < 1.6:
            burbuja(im, mx - 120 * e * (1 + k % 3) + 20 * math.sin(k), my - 220 * e + 30 * math.cos(k * 2), 8 + 4 * (k % 3), t, seed=2500 + k)
    return terminar(im, t)


# ------------------------------------------------------------ cierre: atardecer
def _cola(im, x, y, s, t, alza):
    """Aleta caudal que sale del agua y se despide."""
    if alza <= 0:
        return
    ang = 0.25 * math.sin(t * 2.4)
    pts = np.array([(-16, 40), (-14, -100), (-130, -150), (-170, -200), (-60, -180), (0, -140), (60, -180), (170, -200),
                    (130, -150), (14, -100), (16, 40)], np.float32)
    c, si = math.cos(ang), math.sin(ang)
    q = np.stack([pts[:, 0] * c - pts[:, 1] * si, pts[:, 0] * si + pts[:, 1] * c], 1) * s
    q[:, 1] += 260 * s * (1 - alza)
    forma(im, curva(q + (x, y), 5, True), rgb("4c5774"), t, 2600, tinta=5 * s, sombra=(rgb("343c55"), 0, -14, 0.6),
          luz=(rgb("f6b49a"), -10, 0, 0.25))
    for k in range(5):                             # gotas que caen de la aleta
        u = (t * 1.3 + k / 5) % 1
        gota(im, x + (-150 + 75 * k) * s, y - 170 * s + 220 * s * u, 0.25 * alza, t, 2610 + k, alfa=1 - u)


def atardecer(t):
    im = np.zeros((H, W, 3), np.float32)
    hz = 700
    degradado(im, rgb("d97ea0"), rgb("fbc98c"), 0, hz)
    sub = im[hz:]
    u = np.linspace(0, 1, H - hz, dtype=np.float32)[:, None, None]
    sub[:] = rgb("f0a37e") * (1 - u) + rgb("2f4f7e") * u
    lavado(im, mancha_pts(260, 250, 260, 91, 0.25, ry=70), rgb("f3b7c4"), 0.55, 91, humedo=14)
    lavado(im, mancha_pts(860, 170, 300, 92, 0.25, ry=60), rgb("f6c1a4"), 0.5, 92, humedo=14)
    sol_y = hz - 40 + 30 * pr(t, T_ATAR, T_FIN)
    brillo(im, 600, sol_y, 300, rgb("fff0c8"), 0.35)
    forma(im, elipse(600, sol_y, 120, 120), rgb("ffd98a"), t, 93, tinta=0, alfa=1.0)
    for k in range(7):                             # reflejos del sol en el agua
        y = hz + 30 + 34 * k
        w = 220 - 24 * k + 20 * math.sin(t * 2 + k)
        linea(im, [(600 - w, y), (600 + w, y)], 8 - k * 0.6, col=rgb("fff1c4"), seed=95 + k, t=t, alfa=0.7, punta=True)
    linea(im, [(x, hz + 6 * math.sin(t * 2 + x * 0.012)) for x in range(-20, 1110, 40)], 5, seed=96, t=t, punta=False, alfa=0.8)
    # la cola se despide a lo lejos
    alza = e_out(pr(t, zDif - 0.5, zDif + 0.6))
    _cola(im, 900, hz + 10, 0.75, t, alza)
    linea(im, [(x, hz + 6 * math.sin(t * 2 + x * 0.012)) for x in range(700, 1110, 40)], 5, seed=97, t=t, punta=False, alfa=0.8)
    # el buzo flota mareado; Kuri lo abraza
    bx, by = 320, 880 + 14 * math.sin(t * 1.6)
    feliz = t > zDig - 0.1
    buzo(im, bx, by, 1.15, t, rot=0.08 * math.sin(t * 1.2), cara="feliz" if feliz else "mareo",
         brazos=(2.5, 2.5) if feliz else (1.4, 0.9), codos=(0.3, -0.3), patada=0.5, vel=3)
    pico_calamar(im, bx + 40, by - 250, 0.9, t, rot=0.5)        # un pico se le quedó en la cabeza
    if not feliz:
        mareo(im, bx, by - 300, 1.0, t)
    abr = e_out(pr(t, zBuzo - 0.2, zEres))
    kx, ky = lerp(820, bx + 150, abr), lerp(500, by - 70, abr) + 10 * math.sin(t * 2)
    kuri(im, kx, ky, 0.9, t, cara="corazon" if abr > 0.6 else "feliz", brazos=(2.7, 2.7) if abr > 0.6 else (1.8, 1.8))
    # agua por delante del cuerpo
    forma(im, curva([(-20, 900), (300, 905 + 8 * math.sin(t * 2)), (600, 898), (1100, 905), (1100, H + 20), (-20, H + 20)], 6, True),
          rgb("3f6e9a"), t, 98, tinta=4, modo="lavado", alfa=0.55, luz=(rgb("f6b49a"), 0, 14, 0.3))
    if abr > 0.6:
        for k in range(4):
            u = (t * 0.5 + k / 4) % 1
            corazon(im, bx + 90 + 90 * math.sin(k * 2 + u * 3), by - 280 - 420 * u, 1.1 * (1 - u * 0.5), t, seed=1040 + k)
    for k, (dx, dy) in enumerate(((-260, -360), (260, -420), (330, -120))):
        if t > zDig:
            destello(im, bx + dx, by + dy, 0.8 * e_back(pr(t, zDig + 0.1 * k, zDig + 0.1 * k + 0.3)), t, seed=1150 + k)
    im = terminar(im, t)
    f = suave(pr(t, T_FIN - 0.9, T_FIN - 0.1))     # fundido a papel
    if f > 0:
        im = im * (1 - f) + BLANCO * f
    return im


# ------------------------------------------------------------ montaje
def cuadro(t):
    if t < T_INM:
        return estomago(t)
    if t < T_INM + 0.5:
        return desborde(estomago(t), inmersion(t), pr(t, T_INM, T_INM + 0.5), cx=540, cy=1000, borde=(0.1, 0.15, 0.25))
    if t < T_PRES:
        return inmersion(t)
    if t < T_PRES + 0.5:
        return desborde(inmersion(t), presion(t), pr(t, T_PRES, T_PRES + 0.5), cx=600, cy=1000, borde=(0.15, 0.05, 0.08))
    if t < vVom - 0.05:
        return presion(t)
    if t < T_FUERA:
        return presion(t, sacude=pr(t, vVom - 0.1, vVom + 0.1))
    if t < T_FUERA + 0.4:
        return desborde(presion(t, 1.0), vomito(t), pr(t, T_FUERA, T_FUERA + 0.4), cx=880, cy=1300, borde=(0.3, 0.35, 0.15))
    if t < T_ATAR:
        return vomito(t)
    if t < T_ATAR + 0.6:
        return desborde(vomito(t), atardecer(t), pr(t, T_ATAR, T_ATAR + 0.6), cx=540, cy=700, borde=(0.4, 0.2, 0.2))
    return atardecer(t)
