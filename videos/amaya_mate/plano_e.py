# -*- coding: utf-8 -*-
"""TIPOS DE TRIÁNGULOS (según sus lados) + PREGUNTA 3 + RESPUESTA 3.
e0: «3. TRIÁNGULOS»: tres triángulos distintos; «3 LADOS» y «¿IGUALES?».
e1: EQUILÁTERO con una rayita en cada lado (lados iguales = mismas rayitas); «EQUI = IGUAL» → un equipo: 3 camisetas iguales.
e2: ISÓSCELES con 2 lados marcados y la base distinta → un par de tenis iguales y una chancla.
e3: ESCALENO con 1, 2 y 3 rayitas (todos distintos) → escalera chueca.
e4: FOTO REAL de su cuaderno (equilátero con compás) + la construcción animada: base, el compás se abre del tamaño del lado,
    arco desde cada punta, se cruzan → tercera punta → salen los tres lados iguales.
preg3: triángulo 5 · 5 · 3 cm con opciones EQUILÁTERO / ISÓSCELES / ESCALENO; cuenta 3-2-1.
resp3: ISÓSCELES se enciende; los dos de 5 se marcan iguales y el de 3 distinto; tenis + chancla."""
import math

import numpy as np

from acuarela import H, TINTA, elipse, forma, lavado, linea, pr, rgb, rotulo, suave, terminar
from comun import FIN, INI, T0, ww
from fondos_amaya import papel
from iconos_ia import palomita
from personajes import AMARILLO, destello, pregunta
from kit_amaya import (AZUL, CREMA, GRIS, MORADO, ROJO, VERDE, cache, chispas, cuenta, entra, letrero, papa, pausa, tarjeta)
from piezas_es import ROSA_M, TURQ, polaroid
from piezas_fj import base
from piezas_mt import (AZUL_C, LILA_C, MIEL, ROSA_C, VERDE_C, camiseta, chancla, compas, escalera, marca_lado, tenis,
                       triangulo)

T_INI = T0("triangulos")
G = "triangulos"
tSig, tTres, tNo = ww(G, 0, "siguiente"), ww(G, 0, "tres"), ww(G, 0, "no todos")
T_E1 = INI(G, 1) - 0.3
tEqui, tIg1, tNom, tIgual, tEquipo, tUnif = (ww(G, 1, "equilatero"), ww(G, 1, "iguales"), ww(G, 1, "nombre"), ww(G, 1, "igual", 1),
                                             ww(G, 1, "equipo"), ww(G, 1, "uniforme"))
T_E2 = INI(G, 2) - 0.3
tIso, tDos, tDif, tTen, tChan = ww(G, 2, "isosceles"), ww(G, 2, "dos"), ww(G, 2, "diferente"), ww(G, 2, "tenis"), ww(G, 2, "chancla")
T_E3 = INI(G, 3) - 0.3
tEsc, tTres3, tEscal, tNing = ww(G, 3, "escaleno"), ww(G, 3, "tres"), ww(G, 3, "escalera"), ww(G, 3, "ningun")
T_E4 = INI(G, 4) - 0.3
tCuad, tComp, tAbre, tArco, tCada, tCruz, tTerc, tAsi, tIg4 = (
    ww(G, 4, "cuaderno"), ww(G, 4, "compas"), ww(G, 4, "abre"), ww(G, 4, "arco"), ww(G, 4, "cada"), ww(G, 4, "cruzan"),
    ww(G, 4, "tercera"), ww(G, 4, "asi"), ww(G, 4, "iguales"))
P, R = "preg3", "resp3"
T_P3 = T0(P)
tP3, tMide, tC1, tC2, tT3, tTipo, tFinP3 = (ww(P, 0, "pausa"), ww(P, 0, "mide"), ww(P, 0, "cinco"), ww(P, 0, "cinco", 1),
                                            ww(P, 0, "tres"), ww(P, 0, "tipo"), FIN(P))
T_R3 = T0(R)
tIsoR, tDosR, tCincoR, tTresR, tTenR = ww(R, 0, "isosceles"), ww(R, 0, "dos"), ww(R, 0, "cinco"), ww(R, 0, "tres"), ww(R, 0, "tenis")

OPS = [("EQUILÁTERO", ROSA_C), ("ISÓSCELES", AZUL_C), ("ESCALENO", VERDE_C)]


def opciones(im, t, y, t_aps, ok=-1, t_ok=1e9, seed=0, xs=(330, 730, 1130)):
    """Tres botones de opción; desde t_ok el correcto se pone verde y brinca, los otros se apagan."""
    for k, ((txt, col), x) in enumerate(zip(OPS, xs)):
        e = entra(t, t_aps[k] - 0.2)
        if e <= 0.01:
            continue
        r = pr(t, t_ok - 0.1, t_ok + 0.3)
        if k == ok:
            c, b = (VERDE if r > 0.5 else col), 1 + 0.15 * r
        else:
            c, b = col * (1 - 0.5 * r) + np.array([0.85, 0.85, 0.85], np.float32) * 0.5 * r, 1 - 0.1 * r
        tarjeta(im, x, y, 360 * e * b, 110 * e * b, t, c, seed + k * 5, rot=(k - 1) * 0.02)
        rotulo(im, txt, x, y + 4, 42 * e * b + 1, CREMA if (k == ok and r > 0.5) else TINTA, t, seed=seed + 1 + k * 5, tinta=False)


def equi(x, y, L):
    h = L * math.sqrt(3) / 2
    return [(x - L / 2, y + h / 3), (x + L / 2, y + h / 3), (x, y - 2 * h / 3)]


def iso(x, y, base_, lado):
    h = math.sqrt(lado ** 2 - (base_ / 2) ** 2)
    return [(x - base_ / 2, y + h / 2), (x + base_ / 2, y + h / 2), (x, y - h / 2)]


def esca(x, y, s=1.0):
    return [(x - 190 * s, y + 110 * s), (x + 150 * s, y + 110 * s), (x + 70 * s, y - 150 * s)]


def e0(t):
    im = cache("e_e0", lambda: papel("frio")).copy()
    letrero(im, "3. TRIÁNGULOS", 300, 110, 56, t, col=VERDE_C, seed=24000, esc=entra(t, tSig - 0.2), rot=-0.04)
    for k, (pts, col) in enumerate(((equi(330, 480, 300), ROSA_C), (iso(760, 470, 190, 320), AZUL_C), (esca(1190, 470, 1.0), VERDE_C))):
        triangulo(im, pts, t, col, seed=24010 + k * 40, e=entra(t, tSig + 0.3 + 0.25 * k))
    if t > tTres - 0.3:
        e = entra(t, tTres - 0.3)
        rotulo(im, "TODOS: 3 LADOS", 760, 720, 64 * e + 1, MORADO, t, seed=24150)
        for k in range(3):
            linea(im, [(240 + 430 * k, 655), (420 + 430 * k, 655)], 6, MORADO, seed=24155 + k, t=t, alfa=0.6 * e)
    if t > tNo - 0.3:
        e = entra(t, tNo - 0.3)
        letrero(im, "PERO ¿IGUALES?", 760, 850, 50, t, col=AMARILLO, seed=24160, esc=e, rot=0.03)
        pregunta(im, 1110, 830, 1.2 * e + 0.01, t, seed=24165)
    return im


def e1(t):
    im = cache("e_e1", lambda: papel("calido")).copy()
    e = entra(t, tEqui - 0.3)
    letrero(im, "EQUILÁTERO", 420, 120, 60, t, col=ROSA_C, seed=24200, esc=e, rot=-0.04)
    triangulo(im, equi(420, 520, 440), t, ROSA_C, seed=24210, e=e,
              marcas=(1, 1, 1) if t > tIg1 - 0.2 else (0, 0, 0))
    if t > tIg1 - 0.3:
        rotulo(im, "3 LADOS IGUALES", 420, 760, 56 * entra(t, tIg1 - 0.3) + 1, ROJO, t, seed=24220)
    if t > tIgual - 0.4:
        ee = entra(t, tIgual - 0.4)
        rotulo(im, "EQUI = IGUAL", 1150, 240, 70 * ee + 1, MORADO, t, seed=24230, rot=0.03)
    for k in range(3):
        ek = entra(t, tEquipo - 0.3 + 0.18 * k)
        if ek > 0.01:
            camiseta(im, 930 + 220 * k, 520 + 8 * math.sin(t * 5 + k), 1.7 * ek, t, rgb("3f78c8"), num="10", seed=24240 + k * 3)
    if t > tEquipo - 0.3:
        rotulo(im, "UN EQUIPO", 1150, 380, 52 * entra(t, tEquipo - 0.3) + 1, AZUL, t, seed=24260, tinta=False)
    if t > tUnif - 0.4:
        letrero(im, "¡MISMO UNIFORME!", 1150, 720, 50, t, col=AMARILLO, seed=24265, esc=entra(t, tUnif - 0.4), rot=-0.03)
    return im


def e2(t):
    im = cache("e_e2", lambda: papel("rosa")).copy()
    e = entra(t, tIso - 0.3)
    letrero(im, "ISÓSCELES", 420, 120, 60, t, col=AZUL_C, seed=24300, esc=e, rot=-0.04)
    pts = iso(420, 500, 260, 430)
    triangulo(im, pts, t, AZUL_C, seed=24310, e=e, marcas=(0, 1, 1) if t > tDos - 0.2 else (0, 0, 0))
    if t > tDos - 0.3:
        rotulo(im, "2 LADOS IGUALES", 420, 790, 52 * entra(t, tDos - 0.3) + 1, ROJO, t, seed=24320)
    if t > tDif - 0.3:
        ed = entra(t, tDif - 0.3)
        (x0, y0), (x1, y1) = pts[0], pts[1]
        linea(im, [(x0, y0 + 2), (x1, y1 + 2)], 12, AMARILLO, seed=24325, t=t, alfa=ed)
        rotulo(im, "1 DIFERENTE", 420, 860, 44 * ed + 1, MORADO, t, seed=24326, tinta=False)
    for k in range(2):
        ek = entra(t, tTen - 0.3 + 0.2 * k)
        if ek > 0.01:
            tenis(im, 950 + 240 * k, 480 - 10 * abs(math.sin(t * 6 + k)), 1.6 * ek, t, seed=24330 + k * 6)
    if t > tTen - 0.3:
        rotulo(im, "IGUALES", 1070, 610, 50 * entra(t, tTen - 0.3) + 1, ROSA_M, t, seed=24345)
    if t > tChan - 0.4:
        ec = entra(t, tChan - 0.4)
        chancla(im, 1420, 480, 1.6 * ec + 0.01, t, seed=24350)
        rotulo(im, "DIFERENTE", 1400, 610, 46 * ec + 1, AZUL, t, seed=24355)
        rotulo(im, "+", 1300, 480, 70 * ec + 1, TINTA, t, seed=24356)
    return im


def e3(t):
    im = cache("e_e3", lambda: papel("frio")).copy()
    e = entra(t, tEsc - 0.3)
    letrero(im, "ESCALENO", 420, 120, 60, t, col=VERDE_C, seed=24400, esc=e, rot=-0.04)
    triangulo(im, esca(430, 500, 1.35), t, VERDE_C, seed=24410, e=e, marcas=(1, 2, 3) if t > tTres3 - 0.2 else (0, 0, 0))
    if t > tTres3 - 0.3:
        rotulo(im, "3 LADOS DIFERENTES", 430, 790, 50 * entra(t, tTres3 - 0.3) + 1, ROJO, t, seed=24420)
    if t > tEscal - 0.4:
        es = entra(t, tEscal - 0.4)
        escalera(im, 920, 640, 1.7 * es + 0.01, t, seed=24430, alturas=(60, 150, 90, 210))
        rotulo(im, "ESCALENO = ESCALERA CHUECA", 1110, 250, 46 * es + 1, MORADO, t, seed=24440, tinta=False)
    if t > tNing - 0.3:
        letrero(im, "NINGÚN ESCALÓN IGUAL", 1110, 760, 46, t, col=AMARILLO, seed=24450, esc=entra(t, tNing - 0.3), rot=0.03)
    return im


# construcción con compás: base A-B y la tercera punta C
CA, CB, L = (1010.0, 720.0), (1410.0, 720.0), 400.0
CC = (1210.0, 720.0 - L * math.sqrt(3) / 2)
LAPIZ = rgb("7a7a86")


def arco(im, c, a0, a1, u, t, seed):
    if u <= 0:
        return
    a = np.linspace(a0, a0 + (a1 - a0) * u, 40)
    linea(im, np.stack([c[0] + L * np.cos(a), c[1] + L * np.sin(a)], 1), 4, LAPIZ, seed=seed, t=t, punta=False)


def compas_en(im, aguja, lapiz, t, seed, alto=300):
    """Compás con la aguja en `aguja` y la punta de lápiz en `lapiz` (bisagra arriba)."""
    ax, ay = aguja
    px, py = lapiz
    d = math.hypot(px - ax, py - ay)
    mx, my = (ax + px) / 2, (ay + py) / 2
    h = math.sqrt(max(1.0, alto ** 2 - (d / 2) ** 2))
    nx, ny = -(py - ay) / (d + 1e-6), (px - ax) / (d + 1e-6)
    if ny > 0:
        nx, ny = -nx, -ny
    bx, by = mx + nx * h, my + ny * h
    th = math.atan2(my - by, mx - bx)
    ang = th - math.pi / 2
    # el compás pinta la pierna «θ+half» con la punta amarilla; si esa queda en la aguja, se refleja el ángulo
    half = math.asin(min(1.0, d / 2 / alto))
    ex, ey = bx + alto * math.cos(th + half), by + alto * math.sin(th + half)
    if math.hypot(ex - ax, ey - ay) < math.hypot(ex - px, ey - py):
        # dibujar a mano con las piernas cambiadas
        for q, col in ((lapiz, rgb("6f7a8a")), (aguja, GRIS)):
            linea(im, [(bx, by), q], 11, col, seed=seed + (1 if q is lapiz else 2), t=t)
        dx, dy = (px - bx) / alto, (py - by) / alto
        linea(im, [(px, py), (px + dx * 26, py + dy * 26)], 6, AMARILLO, seed=seed + 3, t=t)
        forma(im, elipse(bx, by, 18, 18), ROJO, t, seed + 4, tinta=3)
        linea(im, [(bx, by - 18), (bx, by - 50)], 9, rgb("8a5a34"), seed=seed + 5, t=t)
        return
    compas(im, bx, by, alto, d, ang, t, seed=seed)


def e4(t):
    im = cache("e_e4", lambda: papel("calido")).copy()
    letrero(im, "EN SU CUADERNO", 300, 100, 52, t, col=CREMA, txt=TURQ, seed=24500, esc=entra(t, T_E4 + 0.1), rot=-0.04)
    e = entra(t, tCuad - 0.4, 0.5)
    polaroid(im, "tri_hoja", 420, 500, 0.9 * e, t, rot=-0.025, seed=24510, alto=460)
    if t > tComp - 0.4:
        rotulo(im, "CON COMPÁS", 1210, 120, 56 * entra(t, tComp - 0.4) + 1, MORADO, t, seed=24520)
    # base
    ub = suave(pr(t, tAbre - 0.3, tAbre + 0.5))
    if ub > 0:
        linea(im, [CA, (CA[0] + (CB[0] - CA[0]) * ub, CB[1])], 9, ROSA_M, seed=24530, t=t)
        for q, n in ((CA, "A"), (CB, "B")):
            forma(im, elipse(q[0], q[1], 11, 11), TINTA, t, 24531 + ord(n), tinta=2)
        rotulo(im, "TAMAÑO DEL LADO", 1210, 790, 40 * entra(t, tAbre) + 1, ROSA_M, t, seed=24535, tinta=False)
    a0A, a1A = -math.radians(35), -math.radians(85)
    a0B, a1B = -math.radians(145), -math.radians(95)
    uA = suave(pr(t, tArco - 0.2, tArco + 0.6))
    uB = suave(pr(t, tCada + 0.1, tCada + 0.9))
    arco(im, CA, a0A, a1A, uA, t, 24540)
    arco(im, CB, a0B, a1B, uB, t, 24541)
    # el compás: primero se abre sobre la base, luego gira en A, luego en B
    if tComp - 0.4 < t < tAsi:
        if t < tArco - 0.2:
            ab = 120 + (L - 120) * ub
            compas_en(im, CA, (CA[0] + ab, CA[1]), t, 24550)
        elif t < tCada + 0.1:
            a = a0A + (a1A - a0A) * uA
            compas_en(im, CA, (CA[0] + L * math.cos(a), CA[1] + L * math.sin(a)), t, 24550)
        else:
            a = a0B + (a1B - a0B) * uB
            compas_en(im, CB, (CB[0] + L * math.cos(a), CB[1] + L * math.sin(a)), t, 24550)
    if t > tCruz - 0.2:
        ec = entra(t, tCruz - 0.2)
        destello(im, CC[0], CC[1], 1.2 * ec, t, seed=24560)
        forma(im, elipse(CC[0], CC[1], 14 * ec + 1, 14 * ec + 1), ROJO, t, 24561, tinta=2)
        if t > tTerc - 0.3:
            rotulo(im, "3.ª PUNTA", CC[0] + 150, CC[1] - 30, 42 * entra(t, tTerc - 0.3) + 1, ROJO, t, seed=24562)
    us = suave(pr(t, tAsi - 0.2, tAsi + 0.6))
    if us > 0:
        for k, q in enumerate((CA, CB)):
            linea(im, [q, (q[0] + (CC[0] - q[0]) * us, q[1] + (CC[1] - q[1]) * us)], 9, ROSA_M, seed=24570 + k, t=t)
    if t > tIg4 - 0.3:
        for k, (a, b) in enumerate(((CA, CB), (CB, CC), (CC, CA))):
            marca_lado(im, a, b, 1, t, 24580 + k * 3, s=1.6)
        letrero(im, "¡3 LADOS IGUALES!", 1210, 880, 46, t, col=AMARILLO, seed=24590, esc=entra(t, tIg4 - 0.3), rot=0.03)
    return im


TRI_P = iso(560, 500, 240, 400)


def preg3(t):
    im = cache("e_p3", lambda: papel("frio")).copy()
    pausa(im, 260, 210, 0.7 * entra(t, tP3 - 0.3), t, seed=24700, texto=False)
    rotulo(im, "PAUSA Y CONTESTA", 820, 200, 72, ROJO, t, seed=24705, esc=entra(t, tP3 - 0.1))
    e = entra(t, tMide - 0.4)
    triangulo(im, TRI_P, t, rgb("f7e8c8"), seed=24710, e=e)
    if e > 0.5:
        c = np.mean(np.asarray(TRI_P), 0)
        for k, (i, txt, tk) in enumerate(((2, "5 cm", tC1), (1, "5 cm", tC2), (0, "3 cm", tT3))):
            ek = entra(t, tk - 0.2)
            if ek > 0.01:
                a, b = np.asarray(TRI_P[i]), np.asarray(TRI_P[(i + 1) % 3])
                m = (a + b) / 2
                d = m - c
                d = d / (np.linalg.norm(d) + 1e-6)
                rotulo(im, txt, m[0] + d[0] * 90, m[1] + d[1] * 70, 50 * ek + 1, MORADO, t, seed=24720 + k)
    if t > tTipo - 0.3:
        ee = entra(t, tTipo - 0.3)
        letrero(im, "¿QUÉ TIPO ES?", 1110, 450, 56, t, col=AMARILLO, seed=24730, esc=ee, rot=0.03)
        pregunta(im, 1110, 590, 1.3 * ee + 0.01, t, seed=24735)
    opciones(im, t, 860, [tTipo + 0.1 * k for k in range(3)], seed=24740)
    cuenta(im, 1640, 250, t, tFinP3 + 0.15, T_R3 + 0.1, s=0.75, seed=24760)
    return im


def resp3(t):
    im = cache("e_r3", lambda: papel("frio")).copy()
    letrero(im, "RESPUESTA", 300, 120, 56, t, col=VERDE, txt=CREMA, seed=24800, esc=entra(t, T_R3), rot=-0.04)
    opciones(im, t, 860, [T_R3 - 2] * 3, ok=1, t_ok=tIsoR, seed=24740)
    chispas(im, 730, 860, 200, t, tIsoR, seed=24805, col=AMARILLO)
    triangulo(im, TRI_P, t, AZUL_C if t > tIsoR else rgb("f7e8c8"), seed=24710, marcas=(0, 1, 1) if t > tDosR - 0.2 else (0, 0, 0))
    c = np.mean(np.asarray(TRI_P), 0)
    for k, (i, txt) in enumerate(((2, "5 cm"), (1, "5 cm"), (0, "3 cm"))):
        a, b = np.asarray(TRI_P[i]), np.asarray(TRI_P[(i + 1) % 3])
        m = (a + b) / 2
        d = (m - c) / (np.linalg.norm(m - c) + 1e-6)
        brilla = (tCincoR - 0.2 < t < tCincoR + 1.2 and k < 2) or (tTresR - 0.2 < t < tTresR + 1.2 and k == 2)
        if brilla:
            lavado(im, elipse(m[0] + d[0] * 90, m[1] + d[1] * 70, 80, 40), AMARILLO, 0.5, 24820 + k, humedo=4)
        rotulo(im, txt, m[0] + d[0] * 90, m[1] + d[1] * 70, 50, ROJO if brilla else MORADO, t, seed=24720 + k)
    if t > tDosR - 0.3:
        rotulo(im, "2 IGUALES + 1 DIFERENTE", 1110, 300, 48 * entra(t, tDosR - 0.3) + 1, ROJO, t, seed=24830, tinta=False)
    if t > tTenR - 0.4:
        et = entra(t, tTenR - 0.4)
        for k in range(2):
            tenis(im, 960 + 190 * k, 520, 1.2 * et + 0.01, t, seed=24840 + k * 6)
        chancla(im, 1380, 520, 1.2 * et + 0.01, t, seed=24855)
        palomita(im, 1380, 650, 1.0 * entra(t, tTenR + 0.4), t, seed=24860, col=VERDE)
    return im


TRAMOS = [(T_INI, e0), (T_E1, e1), (T_E2, e2), (T_E3, e3), (T_E4, e4), (T_P3, preg3), (T_R3, resp3)]


def cuadro_crudo(t):
    im = base(TRAMOS, t)
    papa(im, t, 1770, H + 30, alto=330)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
