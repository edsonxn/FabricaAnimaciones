# -*- coding: utf-8 -*-
"""PREGUNTA 1 + RESPUESTA 1 + REGLAS DE LA TILDE.
preg1: botón de PAUSA, tarjeta «MÚSICA» con «?» y tres botones AGUDA / GRAVE / ESDRÚJULA (cada uno cuando lo nombra); cuenta 3-2-1 en
el silencio. resp1: se enciende ESDRÚJULA, MÚ-SI-CA con MÚ encerrada y ANTEPENÚLTIMA, chispas y palomita.
reglas: «¿CUÁNDO LLEVAN TILDE?» y una A gigante a la que se le pinta la rayita → tarjeta AGUDAS (N · S · VOCAL; CAMARÓN ✓, CALOR ✗) y
tarjeta GRAVES (NO N · S · VOCAL; ÁRBOL, FÁCIL, CÉSPED ✓; CAMA, CARA ✗) → dos hermanos peleados jalando la cuerda con N S VOCAL en
medio → «¡SIEMPRE!» ×3 como sellos, mamá con el suéter → TELÉFONO, VERÓNICA, JERÓNIMO «TODAS CON TILDE»."""
import math

import numpy as np

from acuarela import H, W, TINTA, curva, e_out, elipse, forma, lavado, linea, pr, rgb, rotulo, rrect, suave, terminar
from comun import FIN, T0, ww
from fondos_amaya import papel, _manchas
from iconos_ia import marca_x, palomita
from personajes import AMARILLO, destello, pregunta
from personajes_ia import globo
from kit_amaya import (AZUL, CREMA, GRIS, MORADO, ROJO, VERDE, cache, chispas, cuenta, entra, gente, letrero, papa, pausa,
                       tarjeta)
from piezas_es import ROSA_M, TURQ, ficha, palabra
from piezas_fj import base

T_INI = T0("preg1")
P, R, G = "preg1", "resp1", "reglas"
tP1, tMus, tOp, tFinP1 = ww(P, 0, "pausa"), ww(P, 0, "musica"), [ww(P, 0, w) for w in ("aguda", "grave", "esdrujula")], FIN(P)
T_R1 = T0(R)
tEsdR, tMu, tAnte, tEso = ww(R, 0, "esdrujula"), ww(R, 0, "mu"), ww(R, 0, "antepenultima"), ww(R, 0, "eso")
T_G = T0(G)
tCuando, tRayita, tVocal0 = ww(G, 0, "cuando"), ww(G, 0, "rayita"), ww(G, 0, "vocal")
tAgudas, tN1, tS1, tV1, tCam, tCal = (ww(G, 1, "agudas"), ww(G, 1, "ene"), ww(G, 1, "ese"), ww(G, 1, "vocal"), ww(G, 1, "camaron"),
                                      ww(G, 1, "calor"))
tGraves, tContra, tNo2, tArb, tFac, tCes, tCama = (ww(G, 2, "graves"), ww(G, 2, "contrario"), ww(G, 2, "no"), ww(G, 2, "arbol"),
                                                   ww(G, 2, "facil"), ww(G, 2, "cesped"), ww(G, 2, "cama"))
T_HERM = ww(G, 3, "son") - 0.3
tHerm, tOpuesto = ww(G, 3, "hermanos"), ww(G, 3, "opuesto")
T_SIEM = ww(G, 4, "y") - 0.3
tEsd4, tSiem, tMama, tSueter, tTel, tVer, tJer, tTodas = (ww(G, 4, "esdrujulas"), [ww(G, 4, "siempre", k) for k in range(3)],
                                                          ww(G, 4, "lag"), ww(G, 4, "ganar"), ww(G, 4, "telefono"),
                                                          ww(G, 4, "veronica"), ww(G, 4, "jeronimo"), ww(G, 4, "todas"))
OPS = [("AGUDA", rgb("f6a6a0")), ("GRAVE", rgb("b8c7e8")), ("ESDRÚJULA", rgb("a8d8b0"))]


def opciones(im, t, y, t_aps, ok=-1, t_ok=1e9, seed=0, xs=(380, 760, 1140)):
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
        tarjeta(im, x, y, 320 * e * b, 110 * e * b, t, c, seed + k * 5, rot=(k - 1) * 0.02)
        rotulo(im, txt, x, y + 4, (44 if k < 2 else 38) * e * b + 1, CREMA if (k == ok and r > 0.5) else TINTA, t, seed=seed + 1 + k * 5,
               tinta=False)


def preg1(t):
    im = cache("c_p1", lambda: papel("frio")).copy()
    pausa(im, 260, 210, 0.7 * entra(t, tP1 - 0.3), t, seed=13000, texto=False)
    rotulo(im, "PAUSA Y CONTESTA", 820, 200, 72, ROJO, t, seed=13005, esc=entra(t, tP1 - 0.1))
    if t > tMus - 0.3:
        e = entra(t, tMus - 0.3)
        tarjeta(im, 760, 470, 620 * e, 230 * e, t, CREMA, 13010, rot=-0.02)
        rotulo(im, "MÚSICA", 700, 478, 110 * e + 1, MORADO, t, seed=13011, rot=-0.02)
        pregunta(im, 1000, 470, 1.6 * e + 0.01, t, seed=13012)
    opciones(im, t, 760, tOp, seed=13020)
    cuenta(im, 1640, 250, t, tFinP1 + 0.15, T_R1 + 0.1, s=0.75, seed=13030)
    return im


def resp1(t):
    im = cache("c_r1", lambda: papel("frio")).copy()
    letrero(im, "RESPUESTA", 300, 140, 56, t, col=VERDE, txt=CREMA, seed=13100, esc=entra(t, T_R1), rot=-0.04)
    opciones(im, t, 760, [T_R1 - 2] * 3, ok=2, t_ok=tEsdR, seed=13020)
    palabra(im, ["MÚ", "SI", "CA"], 760, 430, 100, t, tonica=0, t_ap=[tMu - 0.2, tMu + 0.3, tMu + 0.8], t_ton=tMu + 0.1, seed=13110,
            etiquetas=["ANTEPENÚLTIMA", "PENÚLTIMA", "ÚLTIMA"], t_eti=tAnte - 0.5)
    chispas(im, 1140, 760, 200, t, tEsdR, seed=13120, col=AMARILLO)
    if t > tEso - 0.3:
        palomita(im, 1500, 330, 1.6 * entra(t, tEso - 0.3), t, seed=13130, col=VERDE)
    return im


def palabra_fin(im, txt, x, y, px, t, e, ok, seed, ancho_fin=1):
    """Palabra + la ficha de su última letra (o «vocal») + palomita o tache."""
    if e <= 0.01:
        return
    rotulo(im, txt, x, y, px * e + 1, TINTA, t, seed=seed, tinta=False)
    fin = txt[-ancho_fin:]
    xf = x + len(txt) * px * 0.3 + 70
    linea(im, [(xf - 52, y), (xf - 30, y)], 4, GRIS, seed=seed + 1, t=t)
    ficha(im, fin, xf + 8, y, px * 0.8, t, rgb("fff2c0"), seed + 2, esc=e)
    if ok:
        palomita(im, xf + 105, y, 0.9 * e, t, seed=seed + 3, col=VERDE)
    else:
        marca_x(im, xf + 105, y, 0.8 * e, t, seed=seed + 4)


def reglas_txt(t):
    im = cache("c_rg", lambda: papel("calido")).copy()
    if t < tAgudas - 0.4:
        letrero(im, "¿CUÁNDO LLEVAN TILDE?", 760, 140, 64, t, col=AMARILLO, seed=13200, esc=entra(t, tCuando - 0.3), rot=-0.02)
        e = entra(t, tRayita - 0.6)
        rotulo(im, "A", 760, 600, 360 * e + 1, MORADO, t, seed=13205)
        u = suave(pr(t, tRayita - 0.1, tRayita + 0.5))
        if u > 0:
            forma(im, np.array([(700, 395), (712, 410), (712 + 150 * u, 410 - 95 * u), (700 + 150 * u, 395 - 95 * u)], np.float32) + np.array([[0, 0], [0, 0], [0, 0], [0, 0]], np.float32), ROJO, t, 13206, tinta=3)
        if t > tRayita + 0.3:
            letrero(im, "LA TILDE", 1150, 330, 54, t, col=rgb("fde0dc"), txt=ROJO, seed=13207, esc=entra(t, tRayita + 0.3), rot=0.05)
        return im
    # tarjeta AGUDAS
    e = entra(t, tAgudas - 0.4)
    tarjeta(im, 420, 520, 620 * e, 820 * e, t, rgb("f6a6a0"), 13210, rot=-0.015)
    rotulo(im, "AGUDAS", 420, 165, 66 * e + 1, TINTA, t, seed=13211, tinta=False)
    rotulo(im, "LLEVAN TILDE SI TERMINAN EN:", 420, 240, 30 * e + 1, TINTA, t, seed=13212, tinta=False)
    for k, (txt, tk, x) in enumerate((("N", tN1, 270), ("S", tS1 + 0.2, 380), ("VOCAL", tV1, 520))):
        ficha(im, txt, x, 330, 52, t, rgb("fff2c0"), 13215 + k * 4, esc=entra(t, tk - 0.2))
    palabra_fin(im, "CAMARÓN", 330, 500, 66, t, entra(t, tCam - 0.3), True, 13230)
    palabra_fin(im, "CALOR", 300, 650, 66, t, entra(t, tCal - 0.3), False, 13240)
    # tarjeta GRAVES
    if t > tGraves - 0.4:
        e2 = entra(t, tGraves - 0.4)
        tarjeta(im, 1080, 520, 620 * e2, 820 * e2, t, rgb("b8c7e8"), 13250, rot=0.015)
        rotulo(im, "GRAVES", 1080, 165, 66 * e2 + 1, TINTA, t, seed=13251, tinta=False)
        if t > tContra - 0.3:
            letrero(im, "¡AL REVÉS!", 1080, 95, 44, t, col=ROJO, txt=CREMA, seed=13252, esc=entra(t, tContra - 0.3), rot=0.04)
        rotulo(im, "LLEVAN TILDE SI", 1080, 230, 30 * e2 + 1, TINTA, t, seed=13253, tinta=False)
        en = entra(t, tNo2 - 0.2)
        rotulo(im, "NO", 925, 268, 44 * en + 1, ROJO, t, seed=13254)
        rotulo(im, "TERMINAN EN:", 1110, 268, 30 * e2 + 1, TINTA, t, seed=13255, tinta=False)
        for k, (txt, x) in enumerate((("N", 930), ("S", 1040), ("VOCAL", 1180))):
            ficha(im, txt, x, 340, 52, t, rgb("fff2c0"), 13256 + k * 4, esc=entra(t, tNo2 + 0.6 + 0.2 * k))
            if t > tNo2 + 0.9:
                linea(im, [(x - 45, 365), (x + 45, 315)], 6, ROJO, seed=13270 + k, t=t)
        for k, (w_, tk) in enumerate((("ÁRBOL", tArb), ("FÁCIL", tFac), ("CÉSPED", tCes))):
            palabra_fin(im, w_, 960, 450 + k * 92, 54, t, entra(t, tk - 0.3), True, 13280 + k * 6)
        if t > tCama - 0.3:
            palabra_fin(im, "CAMA", 960, 740, 54, t, entra(t, tCama - 0.3), False, 13300)
            palabra_fin(im, "CARA", 960, 832, 54, t, entra(t, tCama + 0.4), False, 13306)
    return im


def hermanos(t):
    im = cache("c_he", lambda: papel("rosa")).copy()
    letrero(im, "HERMANOS PELEADOS", 760, 130, 62, t, col=AMARILLO, seed=13400, esc=entra(t, tHerm - 0.3), rot=-0.02)
    jala = 18 * math.sin(t * 4)
    y = 560
    linea(im, [(380 + jala, y + 10), (1140 + jala, y + 10)], 12, rgb("b98352"), seed=13405, t=t)
    for k, (txt, x) in enumerate((("N", 640), ("S", 760), ("VOCAL", 900))):
        ficha(im, txt, x + jala, y - 60, 52, t, rgb("fff2c0"), 13410 + k * 4, esc=entra(t, tHerm + 0.4 + 0.15 * k))
    for k, (txt, x, col, lado) in enumerate((("AGUDAS", 330, rgb("e35d4a"), -1), ("GRAVES", 1190, AZUL, 1))):
        e = entra(t, tHerm - 0.2 + 0.2 * k)
        gente(im, x + jala, y + 20, 4.2 * e + 0.01, t, seed=13420 + k, cara="enojo", col=col)
        letrero(im, txt, x + jala, y + 300, 50, t, col=CREMA, txt=col, seed=13430 + k * 3, esc=e, rot=0.03 * lado)
    if t > tOpuesto - 0.4:
        rotulo(im, "¡HACEN LO OPUESTO!", 760, 900, 72, ROJO, t, seed=13440, esc=entra(t, tOpuesto - 0.4))
    return im


def sueter(im, x, y, s, t, seed):
    col, osc = rgb("d9534f"), rgb("a83a36")
    forma(im, np.array([(x - 120 * s, y - 120 * s), (x + 120 * s, y - 120 * s), (x + 230 * s, y + 10 * s), (x + 180 * s, y + 60 * s),
                        (x + 120 * s, y + 10 * s), (x + 120 * s, y + 170 * s), (x - 120 * s, y + 170 * s), (x - 120 * s, y + 10 * s),
                        (x - 180 * s, y + 60 * s), (x - 230 * s, y + 10 * s)], np.float32), col, t, seed, tinta=4 * s)
    for k in range(3):
        linea(im, [(x - 115 * s, y + (30 + 45 * k) * s), (x + 115 * s, y + (30 + 45 * k) * s)], 10 * s, CREMA, seed=seed + 1 + k, t=t)
    forma(im, elipse(x, y - 118 * s, 50 * s, 22 * s), osc, t, seed + 5, tinta=3 * s)


def pantalla_lag(im, x, y, e, t, gana, seed=13520):
    """Pantalla de videojuego congelada: barra al 99 % y el circulito de carga que gira («LAG»)."""
    if e <= 0.01:
        return
    tarjeta(im, x, y, 760 * e, 380 * e, t, rgb("2b2f45"), seed, rot=-0.01, tinta=5)
    forma(im, rrect(x, y + 90 * e, 600 * e, 46 * e, 12), rgb("4a4f6a"), t, seed + 1, tinta=3)
    forma(im, rrect(x - 6 * e, y + 90 * e, 588 * e, 34 * e, 10), rgb("5fd38a"), t, seed + 2, tinta=0)
    rotulo(im, "99 %", x + 230 * e, y + 30 * e, 44 * e + 1, CREMA, t, seed=seed + 3)
    ang = t * 6
    for k in range(8):
        a = ang + k * math.pi / 4
        forma(im, elipse(x + 60 * e * math.cos(a), y - 50 * e + 60 * e * math.sin(a), (4 + 2 * k) * e, (4 + 2 * k) * e), CREMA,
              t, seed + 4 + k, tinta=0, alfa=0.25 + 0.09 * k)
    rotulo(im, "LAG", x - 250 * e, y - 60 * e, 90 * e + 1, rgb("ff6b6b"), t, seed=seed + 13, rot=-0.08)
    if gana:
        rotulo(im, "¡YA IBA A GANAR!", x, y + 250 * e, 54, ROJO, t, seed=seed + 14, rot=0.03)


def siempre(t):
    im = cache("c_si", lambda: papel("frio")).copy()
    letrero(im, "ESDRÚJULAS", 420, 130, 62, t, col=rgb("a8d8b0"), seed=13500, esc=entra(t, tEsd4 - 0.3), rot=-0.03)
    if t < tTel - 0.4:
        for k, tk in enumerate(tSiem):
            e = entra(t, tk - 0.1, 0.25)
            if e > 0.01:
                rotulo(im, "¡SIEMPRE!", 330 + 430 * k, 300 + 120 * (k % 2), 96 * e + 1, ROJO, t, seed=13505 + k, rot=(k - 1) * 0.12)
        if t > tMama - 0.4:
            e = entra(t, tMama - 0.4)
            pantalla_lag(im, 760, 690, e, t, t > tSueter - 0.3)
        return im
    for k, (w_, tk) in enumerate((("TELÉFONO", tTel), ("VERÓNICA", tVer), ("JERÓNIMO", tJer))):
        e = entra(t, tk - 0.3)
        if e > 0.01:
            tarjeta(im, 760, 330 + 170 * k, 640 * e, 140 * e, t, CREMA, 13540 + k * 5, rot=(k - 1) * 0.02)
            rotulo(im, w_, 720, 336 + 170 * k, 76 * e + 1, MORADO, t, seed=13541 + k * 5, tinta=False)
            palomita(im, 1010, 330 + 170 * k, 0.9 * e, t, seed=13543 + k * 5, col=VERDE)
    if t > tTodas - 0.3:
        rotulo(im, "¡TODAS CON TILDE!", 760, 900, 80, ROJO, t, seed=13560, esc=entra(t, tTodas - 0.3))
    return im


TRAMOS = [(T_INI, preg1), (T_R1, resp1), (T_G, reglas_txt), (T_HERM, hermanos), (T_SIEM, siempre)]


def cuadro_crudo(t):
    im = base(TRAMOS, t)
    papa(im, t, 1770, H + 30, alto=330)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
