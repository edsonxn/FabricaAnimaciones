# -*- coding: utf-8 -*-
"""ATMÓSFERA + AIRE + PREGUNTA 2 (trampa) + RESPUESTA 2.
atmosfera: la Tierra en el espacio; aparece la CAPA DE GASES, flechas de GRAVEDAD que la sostienen, foto real del cuaderno → la capa
se vuelve una COBIJA de cuadritos → FUNCIONES: regula el clima (termómetro y sol), movimiento del agua (nube con lluvia), el aire
que respiran los seres vivos (personita y planta que respiran).
aire: foto real del cuaderno + cuatro renglones que cuentan solos hasta 78.08 % NITRÓGENO, 20.95 % OXÍGENO, 0.93 % ARGÓN y
0.04 % OTROS GASES (dióxido de carbono) + barra apilada → SALÓN DE 100: 78 azules, 21 rojas, 1 morada y una migajita.
preg2/resp2: «¡OJO, TRAMPA!», NITRÓGENO / OXÍGENO / ARGÓN; gana nitrógeno; la gente dice «¡OXÍGENO!» y se tacha."""
import math

import numpy as np

from acuarela import H, W, TINTA, brillo, degradado, e_out, elipse, forma, lavado, linea, pr, rgb, rotulo, rrect, suave, terminar
from comun import FIN, T0, ww
from comun_ci import cartel, opciones, pantalla_pregunta, titulo
from fondos_amaya import papel, _manchas
from iconos_ia import marca_x, palomita
from personajes import AMARILLO, destello, exclama, nube_lluvia
from personajes_ia import globo
from kit_amaya import AZUL, CREMA, GRIS, MORADO, ROJO, VERDE, cache, chispas, entra, gente, letrero, papa, tarjeta
from piezas_es import ROSA_M, polaroid
from piezas_fj import base
from piezas_ci import AR, CO2, N2, O2, flecha_empuje, tierra
from utileria import termometro

T_INI = T0("atmosfera")
A, AI, P, R = "atmosfera", "aire", "preg2", "resp2"
tAtm, tCapa, tPlan, tFuerza, tGrav = ww(A, 0, "atmosfera"), ww(A, 0, "capa"), ww(A, 0, "planeta"), ww(A, 0, "fuerza"), ww(A, 0, "gravedad")
tCobija, tInvis = ww(A, 1, "cobija"), ww(A, 1, "invisible")
T_FUN = ww(A, 2, "y") - 0.3
tFunc, tClima, tAyuda, tMov, tAireA, tSeres = (ww(A, 2, "funciones"), ww(A, 2, "regula"), ww(A, 2, "ayuda"), ww(A, 2, "movimiento"),
                                              ww(A, 2, "aire"), ww(A, 2, "seres"))
T_AI = T0(AI)
tHecho, tApunt = ww(AI, 0, "hecho"), ww(AI, 0, "apunten")
FILAS = [(78.08, "NITRÓGENO", N2, ww(AI, 0, "setenta"), ww(AI, 0, "nitrogeno")),
         (20.95, "OXÍGENO", O2, ww(AI, 1, "veinte"), ww(AI, 1, "oxigeno")),
         (0.93, "ARGÓN", AR, ww(AI, 2, "cero"), ww(AI, 2, "argon")),
         (0.04, "OTROS GASES", CO2, ww(AI, 2, "cero", 1), ww(AI, 2, "otros"))]
tResp, tMenor, tDiox = ww(AI, 1, "respiramos"), ww(AI, 2, "menor"), ww(AI, 2, "dioxido")
T_SAL = ww(AI, 3, "truco") - 0.3
tSalon, tS78, tS21, tS1, tMiga = ww(AI, 3, "salon"), ww(AI, 3, "setenta"), ww(AI, 3, "veintiuno"), ww(AI, 3, "uno"), ww(AI, 3, "migajita")
T_P2 = T0(P)
tP2, tOjo, tCual, tAireP, tFinP2 = ww(P, 0, "pausa"), ww(P, 0, "ojo"), ww(P, 0, "cual"), ww(P, 0, "aire"), FIN(P)
T_R2 = T0(R)
tNitR, tSetR, tGente, tOxi1, tOxi2, tVeint, tCaigan = (ww(R, 0, "nitrogeno"), ww(R, 0, "setenta"), ww(R, 0, "gente"),
                                                       ww(R, 0, "oxigeno"), ww(R, 0, "oxigeno", 1), ww(R, 0, "veintiuno"),
                                                       ww(R, 0, "caigan"))
OPS = [("NITRÓGENO", rgb("b8c7e8")), ("OXÍGENO", rgb("f6a6a0")), ("ARGÓN", rgb("d8b8e8"))]


def _espacio():
    im = np.zeros((H, W, 3), np.float32)
    degradado(im, rgb("2c3a6a"), rgb("1c2448"))
    _manchas(im, rgb("4a3a8a"), 8, 77, r=(260, 460), alfa=0.35)
    rg = np.random.default_rng(3)
    for k in range(90):
        x, y, r = rg.uniform(0, W), rg.uniform(0, H), rg.uniform(1.5, 4)
        forma(im, elipse(x, y, r, r), rgb("fbf3df"), 0, 22000 + k, tinta=0)
    return im


def atmosfera(t):
    im = cache("d_esp", _espacio).copy()
    for k in range(5):
        a = (t * 0.7 + k * 1.7) % 6
        brillo(im, 120 + 300 * k, 120 + 160 * (k % 3), 30, rgb("fff3c0"), 0.25 * (0.5 + 0.5 * math.sin(t * 3 + k)))
    titulo(im, "LA ATMÓSFERA", t, tAtm, 22100, col=rgb("a9d4f2"), x=640, y=100, px=86)
    if t > tAtm - 0.3:
        polaroid(im, "atmosfera", 1400, 250, entra(t, tAtm - 0.3), t, rot=0.05, seed=22105, alto=210)
    atm = suave(pr(t, tCapa - 0.2, tCapa + 0.8))
    tierra(im, 640, 560, 250, t, seed=22110, atm=atm, cobija=suave(pr(t, tCobija - 0.2, tCobija + 0.6)))
    if t > tCapa - 0.2 and t < tCobija - 0.3:
        letrero(im, "CAPA DE GASES", 1130, 430, 50, t, col=rgb("a9d4f2"), seed=22120, esc=entra(t, tCapa - 0.2), rot=-0.03)
        linea(im, [(950, 440), (900, 450)], 6, rgb("a9d4f2"), seed=22122, t=t)
    if t > tPlan - 0.2 and t < tCobija - 0.3:
        letrero(im, "PLANETA", 1130, 600, 46, t, col=CREMA, txt=VERDE, seed=22125, esc=entra(t, tPlan - 0.2), rot=0.03)
    if t > tFuerza - 0.3 and t < tCobija - 0.3:
        u = pr(t, tFuerza - 0.3, tFuerza + 0.3)
        for k in range(8):
            a = 2 * math.pi * k / 8 + 0.2
            r0, r1 = 400, 300
            flecha_empuje(im, 640 + r0 * math.cos(a), 560 + r0 * math.sin(a), 640 + r1 * math.cos(a), 560 + r1 * math.sin(a), t,
                          col=rgb("e9b949"), ancho=8, seed=22130 + k * 3, u=u)
        letrero(im, "GRAVEDAD", 1130, 760, 52, t, col=rgb("e9b949"), seed=22160, esc=entra(t, tGrav - 0.3), rot=-0.02)
    if t > tCobija - 0.3:
        letrero(im, "UNA COBIJA INVISIBLE", 1130, 560, 48, t, col=CREMA, txt=ROSA_M, seed=22170, esc=entra(t, tCobija - 0.3), rot=0.03)
    return im


def sol(im, x, y, r, t, seed):
    brillo(im, x, y, r * 2.2, rgb("fff0a0"), 0.5)
    for k in range(10):
        a = 2 * math.pi * k / 10 + t * 0.4
        linea(im, [(x + r * 1.2 * math.cos(a), y + r * 1.2 * math.sin(a)), (x + r * 1.55 * math.cos(a), y + r * 1.55 * math.sin(a))], 6,
              rgb("f2a93e"), seed=seed + k, t=t)
    forma(im, elipse(x, y, r, r), rgb("f7c84e"), t, seed + 20, tinta=4)


def planta(im, x, y, s, t, seed):
    linea(im, [(x, y), (x + 6 * s * math.sin(t * 1.3), y - 120 * s)], 7 * s, VERDE, seed=seed, t=t)
    for k, d in enumerate((-1, 1, -1)):
        yy = y - (40 + 35 * k) * s
        forma(im, elipse(x + d * 34 * s, yy, 34 * s, 16 * s, d * 0.5), rgb("6fb35f"), t, seed + 2 + k, tinta=2.5 * s)
    forma(im, np.array([(x - 50 * s, y), (x + 50 * s, y), (x + 38 * s, y + 70 * s), (x - 38 * s, y + 70 * s)], np.float32),
          rgb("c8754a"), t, seed + 9, tinta=3 * s)


def funciones(t):
    im = cache("d_fun", lambda: papel("frio")).copy()
    titulo(im, "SUS FUNCIONES", t, tFunc, 22200, col=MORADO, x=640, y=100, px=80)
    cols = [(260, "REGULA EL CLIMA", tClima, rgb("f4d38a")), (700, "MOVIMIENTO DEL AGUA", tMov, rgb("b8c7e8")),
            (1140, "EL AIRE QUE RESPIRAN", tAireA, rgb("a8d8b0"))]
    for k, (x, txt, tk, col) in enumerate(cols):
        if t <= tk - 0.3:
            continue
        e = entra(t, tk - 0.3)
        tarjeta(im, x, 520, 400 * e, 520 * e, t, col, 22210 + k * 7, rot=(k - 1) * 0.02)
        rotulo(im, txt, x, 330, (36 if len(txt) > 16 else 42) * e + 1, TINTA, t, seed=22211 + k * 7, tinta=False)
        if e < 0.6:
            continue
        if k == 0:
            sol(im, x - 70, 500, 60, t, 22220)
            termometro(im, x + 100, 560, 1.0, t, 0.45 + 0.1 * math.sin(t * 1.5), seed=22230)
        elif k == 1:
            nube_lluvia(im, x, 470, 1.2, t, seed=22240)
            lavado(im, elipse(x, 690, 140, 26), rgb("8fc3e8"), 0.8, 22245)
        else:
            gente(im, x - 80, 560, 2.4, t, seed=22250)
            planta(im, x + 100, 690, 1.0, t, 22255)
            for j in range(3):
                a = (t * 0.8 + j / 3) % 1
                lavado(im, elipse(x - 20 + 90 * a, 540 - 20 * a, 12 + 14 * a, 10 + 10 * a), rgb("cfe4f4"), 0.7 * (1 - a), 22260 + j)
            if t > tSeres - 0.3:
                rotulo(im, "SERES VIVOS", x, 740, 40, VERDE, t, seed=22265, esc=entra(t, tSeres - 0.3))
    if t > tAyuda - 0.3:
        e = entra(t, tAyuda - 0.3)
        forma(im, rrect(920, 860, 760 * e + 1, 100 * e + 1, 20, 0.02), VERDE, t, 22270, tinta=5)
        rotulo(im, "AYUDA A LA VIDA", 920, 866, 56 * e + 1, CREMA, t, seed=22271, rot=0.02)
    return im


def composicion(t):
    im = cache("d_comp", lambda: papel("calido")).copy()
    titulo(im, "¿DE QUÉ ESTÁ HECHO EL AIRE?", t, tHecho, 22300, col=AZUL, x=740, y=100, px=70)
    if t > tApunt - 0.4:
        polaroid(im, "aire", 300, 470, entra(t, tApunt - 0.4), t, rot=-0.05, seed=22305, alto=380)
        rotulo(im, "SU CUADERNO", 300, 720, 36, ROSA_M, t, seed=22307, esc=entra(t, tApunt - 0.2), rot=-0.05)
    for k, (val, nom, col, t0, t1) in enumerate(FILAS):
        if t <= t0 - 0.3:
            continue
        e = entra(t, t0 - 0.3)
        y = 260 + 135 * k
        tarjeta(im, 1030, y, 860 * e, 112 * e, t, CREMA, 22310 + k * 7, rot=(k % 2 - 0.5) * 0.02)
        forma(im, elipse(650, y, 30 * e + 1, 30 * e + 1), col, t, 22311 + k * 7, tinta=3)
        v = val * suave(pr(t, t0, t1))
        rotulo(im, f"{v:.2f} %", 830, y + 4, 62 * e + 1, col * 0.8, t, seed=22312 + k * 7, tinta=False)
        if t > t1 - 0.3:
            rotulo(im, nom, 1230, y + 4, (46 if len(nom) > 9 else 54), TINTA, t, seed=22313 + k * 7, esc=entra(t, t1 - 0.3),
                   tinta=False)
    if t > tResp - 0.3:
        letrero(im, "¡EL QUE RESPIRAMOS!", 1300, 330, 30, t, col=AMARILLO, seed=22340, esc=entra(t, tResp - 0.3), rot=0.06)
    if t > tDiox - 0.3:
        letrero(im, "COMO EL DIÓXIDO DE CARBONO", 1050, 800, 38, t, col=CREMA, txt=GRIS, seed=22345, esc=entra(t, tDiox - 0.3), rot=-0.02)
    elif t > tMenor - 0.3:
        rotulo(im, "EN MENOR CONCENTRACIÓN", 1050, 800, 40, GRIS, t, seed=22346, esc=entra(t, tMenor - 0.3))
    # barra apilada que crece con cada renglón
    x0, x1, yb = 160, 1460, 930
    if t > FILAS[0][3] - 0.3:
        linea(im, rrect((x0 + x1) / 2, yb, x1 - x0, 60, 10), 4, seed=22350, t=t, cerrado=True, punta=False)
        xa = x0
        for k, (val, nom, col, t0, t1) in enumerate(FILAS):
            w = (x1 - x0) * val / 100 * suave(pr(t, t0, t1))
            if w > 3:
                forma(im, rrect(xa + w / 2, yb, w, 52, 6), col, t, 22355 + k, tinta=1.5)
            xa += (x1 - x0) * val / 100
    return im


def salon(t):
    im = cache("d_sal", lambda: papel("frio")).copy()
    titulo(im, "TRUCO: UN SALÓN DE 100", t, tSalon, 22400, col=MORADO, x=640, y=100, px=72)
    gx, gy, lado = 560, 560, 66
    if t > tSalon - 0.3:
        e = entra(t, tSalon - 0.3)
        tarjeta(im, gx, gy, 700 * e, 700 * e, t, rgb("eef2ea"), 22405)
    grupos = [(78, N2, tS78 - 0.1), (21, O2, tS21 - 0.1), (1, AR, tS1 - 0.1)]
    k = 0
    for (n, col, t0) in grupos:
        for j in range(n):
            ti = t0 + j * 0.012
            if t > ti:
                i_, j_ = k % 10, k // 10
                cx, cy = gx + (i_ - 4.5) * lado, gy + (j_ - 4.5) * lado
                ee = entra(t, ti, 0.25)
                forma(im, elipse(cx, cy, lado * 0.38 * ee, lado * 0.38 * ee), col, t, 22410 + k, tinta=2)
                if ee > 0.8:
                    for d in (-1, 1):
                        forma(im, elipse(cx + d * 7, cy - 3, 2.5, 3.5), TINTA, t, 22520 + k * 2 + d, tinta=0)
            k += 1
    for k, (txt, col, tk) in enumerate((("78 NITRÓGENO", N2, tS78), ("21 OXÍGENO", O2, tS21), ("1 ARGÓN", AR, tS1))):
        if t > tk - 0.3:
            e = entra(t, tk - 0.3)
            tarjeta(im, 1260, 330 + 150 * k, 440 * e, 110 * e, t, CREMA, 22600 + k * 5, rot=(k - 1) * 0.02)
            forma(im, elipse(1090, 330 + 150 * k, 26 * e + 1, 26 * e + 1), col, t, 22601 + k * 5, tinta=2.5)
            rotulo(im, txt, 1290, 335 + 150 * k, 46 * e + 1, col * 0.8, t, seed=22602 + k * 5, tinta=False)
    if t > tMiga - 0.4:
        e = entra(t, tMiga - 0.4)
        forma(im, elipse(1090, 790, 7 * e + 1, 6 * e + 1), CO2, t, 22620, tinta=1.5)
        linea(im, elipse(1090, 790, 46, 46), 6, rgb("6a5a4a"), seed=22621, t=t, cerrado=True, punta=False, alfa=e)
        linea(im, [(1123, 823), (1170, 870)], 10, rgb("6a5a4a"), seed=22622, t=t, alfa=e)
        rotulo(im, "+ UNA MIGAJITA", 1320, 795, 44, GRIS, t, seed=22625, esc=e)
    return im


def preg2(t):
    im = cache("d_p2", lambda: papel("frio")).copy()
    pantalla_pregunta(im, t, tP2, tFinP2, T_R2, 22700, ["¿CUÁL ES EL GAS QUE", "MÁS HAY EN EL AIRE?"], [tCual, tCual + 0.8], y0=400)
    if t > tOjo - 0.3:
        letrero(im, "¡OJO: HAY TRAMPA!", 1280, 330, 44, t, col=AMARILLO, seed=22720, esc=entra(t, tOjo - 0.3), rot=0.06)
        exclama(im, 1480, 300, 1.2 * entra(t, tOjo - 0.2), t, seed=22725, col=ROJO)
    opciones(im, t, 820, OPS, [tAireP + 0.1, tAireP + 0.4, tAireP + 0.7], seed=22730, xs=(320, 720, 1120))
    return im


def resp2(t):
    im = cache("d_r2", lambda: papel("frio")).copy()
    letrero(im, "RESPUESTA", 260, 120, 56, t, col=VERDE, txt=CREMA, seed=22800, esc=entra(t, T_R2), rot=-0.04)
    opciones(im, t, 300, OPS, [T_R2 - 2] * 3, ok=0, t_ok=tNitR, seed=22730, xs=(320, 720, 1120))
    chispas(im, 320, 300, 200, t, tNitR, seed=22810, col=AMARILLO)
    if t > tSetR - 0.3:
        rotulo(im, "78 %", 320, 470, 110, N2 * 0.8, t, seed=22815, esc=entra(t, tSetR - 0.3))
    if t > tGente - 0.3:
        e = entra(t, tGente - 0.3)
        for k in range(4):
            gente(im, 700 + 110 * k, 820 - 18 * (k % 2), 2.4 * e + 0.01, t, seed=22820 + k * 3)
        if t > tOxi1 - 0.2:
            globo(im, 900, 580, 380, 110, "¡OXÍGENO!", t, px=50, seed=22840, cola=(-0.4, 1), alfa=min(1, (t - tOxi1 + 0.2) * 4))
        if t > tOxi2:
            marca_x(im, 900, 580, 1.3 * entra(t, tOxi2), t, seed=22850)
    if t > tVeint - 0.3:
        letrero(im, "OXÍGENO: SOLO ~21 %", 1180, 450, 40, t, col=CREMA, txt=O2 * 0.8, seed=22860, esc=entra(t, tVeint - 0.3), rot=0.04)
    if t > tCaigan - 0.5:
        rotulo(im, "¡NO CAIGAN!", 380, 680, 88, ROJO, t, seed=22870, esc=entra(t, tCaigan - 0.5), rot=-0.05)
    return im


TRAMOS = [(T_INI, atmosfera), (T_FUN, funciones), (T_AI, composicion), (T_SAL, salon), (T_P2, preg2), (T_R2, resp2)]


def cuadro_crudo(t):
    im = base(TRAMOS, t)
    papa(im, t, 1770, H + 30, alto=330)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
