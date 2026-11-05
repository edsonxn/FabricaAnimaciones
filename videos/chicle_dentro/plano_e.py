# -*- coding: utf-8 -*-
"""INTESTINOS: mapa con el delgado resaltado y cinta métrica de 6 m → dentro del túnel: bilis y jugo del páncreas que
caen, vellosidades al frente que se tragan azúcar, grasa y proteínas; el chicle pasa sin soltar nada (contador de
metros) → intestino grueso: multitud de bacterias que comen fibra y no pueden con el chicle; se junta con lo demás,
el agua se va → mapa: la bolita llega al final, calendario de días, «7 AÑOS» tachado, Kuri dice ADIÓS."""
import math

import cv2
import numpy as np

from acuarela import (H, W, TINTA, brillo, curva, e_back, e_in, e_out, elipse, forma, lavado, lerp, linea, pr, rgb, rotulo,
                      rrect, suave, terminar)
from comun import T0, desborde, ww
from fondos_chicle import papel, tunel
from iconos_ia import marca_x, palomita
from personajes import AMARILLO, BLANCO, mareo, kuri
from piezas_chicle import (ROJO, bacteria, calendario, chicle, gota_agua, mapa_cuerpo, proteina, vellosidad)

T_INI = T0("intestino")
I = "intestino"
tDelgado, tSeis, tPanza = ww(I, 0, "delgado"), ww(I, 0, "seis"), ww(I, 0, "panza")
tBilis, tPancreas, tVello, tAzucar, tGrasas, tProt = (ww(I, 1, "bilis"), ww(I, 1, "pancreas"), ww(I, 1, "vellosidades"),
                                                     ww(I, 1, "azucares"), ww(I, 1, "grasas"), ww(I, 1, "proteinas"))
tNada, tAvanza, tMetro = ww(I, 2, "nada"), ww(I, 2, "avanzando"), ww(I, 2, "metro")
tGrueso, tMedio, tBacterias, tComen = ww(I, 3, "grueso"), ww(I, 3, "medio"), ww(I, 3, "bacterias"), ww(I, 3, "comen")
tTampoco, tJunta, tAgua = ww(I, 4, "tampoco"), ww(I, 4, "junta"), ww(I, 4, "agua")
tDias, tAdios, tNo7 = ww(I, 5, "dias"), ww(I, 5, "adios"), ww(I, 5, "siete")
T_TUNEL = tBilis - 0.6
T_GRUESO = tGrueso - 0.4
T_FINAL = tDias - 0.5


def avanza(im, t, vel=0.35):
    """Sensación de avanzar por el túnel: zoom cíclico hacia el punto de fuga."""
    z = 1 + 0.12 * ((t * vel) % 1)
    cx, cy = 980, 520
    M = np.array([[z, 0, cx - z * cx], [0, z, cy - z * cy]], np.float32)
    return cv2.warpAffine(im, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def mapa1(t):
    im = papel("rosa")
    mapa_cuerpo(im, 620, 600, 1.45, t, u=lerp(0.22, 0.3, pr(t, T_INI, T_TUNEL)), resalta="delgado")
    rotulo(im, "INTESTINO DELGADO", 1300, 260, 78, rgb("2f4f86"), t, seed=9800, esc=e_back(pr(t, min(tDelgado, T_INI + 0.9) - 0.2, min(tDelgado, T_INI + 0.9) + 0.1)))
    if t > tSeis - 0.3:
        u = e_out(pr(t, tSeis - 0.3, tPanza))
        forma(im, rrect(1000 + 450 * u, 560, 900 * u + 4, 70, 8), rgb("f2d36a"), t, 9801, tinta=3.4)
        for k in range(int(6 * u) + 1):
            x = 1000 + k * 150
            linea(im, [(x, 525), (x, 560)], 3, seed=9802 + k, t=t, punta=False)
            rotulo(im, f"{k} m", x, 610, 34, TINTA, t, seed=9810 + k, tinta=False)
        rotulo(im, "≈ 6 METROS", 1450, 760, 96, ROJO, t, seed=9820, esc=e_back(pr(t, tSeis, tSeis + 0.25)))
    return im


def delgado(t):
    im = avanza(tunel("delgado"), t)
    # bilis y páncreas que caen
    for k, (tt, col, txt, x) in enumerate([(tBilis, rgb("8fbf4a"), "BILIS", 600), (tPancreas, rgb("f2d36a"), "PÁNCREAS", 1380)]):
        if t > tt - 0.3 and t < tAvanza:
            e = e_back(pr(t, tt - 0.3, tt))
            for j in range(5):
                y = 80 + ((t * 260 + j * 90) % 450)
                forma(im, curva([(0, -24), (13, 0), (9, 13), (0, 17), (-9, 13), (-13, 0)], 5, True) * 1.4 + np.array([x + j * 20 - 40, y], np.float32),
                      col, t, 9830 + 10 * k + j, tinta=2.4, alfa=e)
            rotulo(im, txt, x, 120, 66, col * 0.8, t, seed=9840 + k, esc=e)
    # partículas que las vellosidades se tragan
    if tAzucar - 0.5 < t < tNada + 0.8:
        for k in range(9):
            kind = k % 3
            tk = [tAzucar, tGrasas, tProt][kind] + 0.15 * (k // 3)
            v = pr(t, tk - 0.4, tk + 0.9)
            if 0 < v < 1:
                x = 300 + k * 160
                y = lerp(560, 930, e_in(v))
                a = 1 - pr(v, 0.75, 1.0)
                if kind == 0:
                    forma(im, rrect(x, y, 34, 34, 5, t), BLANCO, t, 9850 + k, tinta=2.4, alfa=a)
                elif kind == 1:
                    forma(im, elipse(x, y, 22, 22), rgb("f2d36a"), t, 9850 + k, tinta=2.4, alfa=a)
                else:
                    proteina(im, x, y, 0.6, t, n=3, seed=9850 + k)
        for k, (txt, x, y, tt) in enumerate([("AZÚCARES", 360, 470, tAzucar), ("GRASAS", 1330, 360, tGrasas),
                                             ("PROTEÍNAS", 1660, 540, tProt)]):
            if tt - 0.2 < t < tNada:
                rotulo(im, txt, x, y, 64, BLANCO, t, seed=9870 + k, esc=e_back(pr(t, tt - 0.2, tt + 0.1)))
    # vellosidades al frente
    for k in range(13):
        vellosidad(im, -40 + k * 165, H + 30, 230 + 40 * math.sin(k * 1.7), t, seed=9880 + k, ancho=58)
    if tVello - 0.2 < t < tAzucar:
        rotulo(im, "VELLOSIDADES", 960, 760, 80, AMARILLO, t, seed=9900, esc=e_back(pr(t, tVello - 0.2, tVello + 0.1)))
    # el chicle con Kuri
    gx, gy = 960 + 40 * math.sin(t * 0.9), 610 + 14 * math.sin(t * 2.1)
    chicle(im, gx, gy, 120, t, seed=9910, cara="normal" if t < tNada else "feliz")
    kuri(im, gx, gy - 205, 1.4, t, aura=False)
    if tNada - 0.2 < t < tAvanza:
        rotulo(im, "NADA QUE SACAR", gx, gy - 400, 84, AMARILLO, t, seed=9920, esc=e_back(pr(t, tNada - 0.2, tNada + 0.1)))
    if t > tAvanza - 0.2:
        m = 1 + int(5.99 * pr(t, tAvanza, tMetro + 1.0))
        forma(im, rrect(1640, 160, 300, 120, 20), BLANCO, t, 9930, tinta=4)
        rotulo(im, f"{m} m", 1640, 160, 80, ROJO, t, seed=9931, tinta=False)
    return im


def grueso(t):
    im = avanza(tunel("grueso"), t, vel=0.2)
    rotulo(im, "INTESTINO GRUESO", 960, 120, 78, AMARILLO, t, seed=9940, esc=e_back(pr(t, tGrueso - 0.2, tGrueso + 0.1)),
           alfa=1 - pr(t, tBacterias - 0.3, tBacterias))
    if tMedio - 0.2 < t < tBacterias:
        rotulo(im, "≈ 1,5 METROS", 960, 240, 64, BLANCO, t, seed=9941, esc=e_back(pr(t, tMedio - 0.2, tMedio + 0.1)))
    gx, gy = 960, 600
    junta = pr(t, tJunta - 0.2, tJunta + 1.0)
    if junta > 0:                                                         # lo demás que se le junta
        for k in range(9):
            a = k * 0.7
            r = lerp(560, 160, e_out(junta))
            forma(im, mancha_pts_(gx + r * math.cos(a), gy + r * 0.7 * math.sin(a), 46, 9950 + k), rgb("8a6040"), t, 9950 + k,
                  tinta=2.6)
    if t > tAgua - 0.2:                                                   # el agua se va
        for k in range(7):
            v = ((t - tAgua) * 0.7 + k / 7) % 1
            gota_agua(im, gx - 300 + k * 100, lerp(gy - 60, 230, v), 1.8, t, seed=9960 + k)
    chicle(im, gx, gy, 125, t, seed=9970, cara="normal" if t < tTampoco else "feliz")
    kuri(im, gx + 250, gy - 220, 1.35, t, aura=False, cara="normal" if t < tTampoco else "feliz")
    n = int(18 * e_out(pr(t, tBacterias - 0.4, tBacterias + 0.8)))
    rg = np.random.default_rng(9980)
    pos = [(rg.uniform(80, W - 80), rg.uniform(250, H - 80)) for _ in range(18)]
    for k in range(n):
        x, y = pos[k]
        if abs(x - gx) < 380 and abs(y - gy) < 300:
            x += 420 * (1 if x > gx else -1)
        ataca = pr(t, tTampoco - 0.2, tTampoco + 0.6) * (k < 5)
        if ataca > 0:
            a = k * 1.25
            x, y = lerp(x, gx + 170 * math.cos(a), ataca), lerp(y, gy + 140 * math.sin(a), ataca)
        cara = "mareo" if ataca > 0.9 and t > tTampoco + 0.6 else "normal"
        bacteria(im, x, y, 1.5, t, seed=7300 + k, cara=cara, boca="o" if t > tComen and k % 2 else "sonrisa")
        if tComen < t < tTampoco and k % 3 == 0:                          # comen fibra
            linea(im, [(x + 40, y + 10), (x + 80, y + 30)], 6, col=rgb("7fae5a"), seed=9990 + k, t=t)
    if tBacterias - 0.2 < t < tTampoco:
        rotulo(im, "BILLONES DE BACTERIAS", 960, 140, 76, AMARILLO, t, seed=9995, esc=e_back(pr(t, tBacterias - 0.2, tBacterias + 0.1)))
    if t > tTampoco + 0.4 and t < tJunta:
        rotulo(im, "¡NO SE PUEDE!", gx - 60, gy - 330, 90, BLANCO, t, seed=9996, esc=e_back(pr(t, tTampoco + 0.4, tTampoco + 0.6)))
    if t > tAgua - 0.2:
        rotulo(im, "SE VA EL AGUA", 960, 140, 70, rgb("8cc8ee"), t, seed=9997, esc=e_back(pr(t, tAgua - 0.2, tAgua + 0.1)))
    return im


def mancha_pts_(x, y, r, seed):
    from acuarela import mancha_pts
    return mancha_pts(x, y, r, seed, 0.25)


def final(t):
    im = papel("calido")
    u = lerp(0.85, 1.0, suave(pr(t, T_FINAL, tAdios)))
    gx, gy = mapa_cuerpo(im, 520, 600, 1.4, t, u=u, resalta="grueso")
    if t > tDias - 0.3:
        d = 1 + int(2.99 * pr(t, tDias, tAdios))
        calendario(im, 1080, 340, 1.7 * e_back(pr(t, tDias - 0.3, tDias)), t, "DÍAS", str(d), col=rgb("4f86c6"))
    if t > tAdios - 0.3:
        e = e_back(pr(t, tAdios - 0.3, tAdios))
        rotulo(im, "¡ADIÓS!", 1560, 200, 130, AMARILLO, t, seed=10000, rot=0.05, esc=e)
        kuri(im, 1600, 540, 2.1, t, cara="feliz", brazos=(0.5, 1.9 + 0.5 * math.sin(t * 10)))
    if t > tNo7 - 0.4:
        e = e_back(pr(t, tNo7 - 0.4, tNo7))
        calendario(im, 1100, 790, 1.4 * e, t, "AÑOS", "7")
        marca_x(im, 1100, 790, 2.0 * e_back(pr(t, tNo7, tNo7 + 0.25)), t, seed=10010)
        palomita(im, 1250, 340, 1.4 * e, t, seed=10011)
        rotulo(im, "¡DÍAS, NO AÑOS!", 1540, 900, 82, ROJO, t, seed=10012, rot=-0.04, esc=e_back(pr(t, tNo7, tNo7 + 0.3)))
    return im


def cuadro_crudo(t):
    pasos = [(T_INI, mapa1), (T_TUNEL, delgado), (T_GRUESO, grueso), (T_FINAL, final)]
    for i in range(len(pasos) - 1, -1, -1):
        t0, f = pasos[i]
        if t >= t0:
            if i > 0 and t < t0 + 0.8:
                return desborde(pasos[i - 1][1](t), f(t), pr(t, t0, t0 + 0.8), W / 2, H / 2)
            return f(t)
    return mapa1(t)


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
