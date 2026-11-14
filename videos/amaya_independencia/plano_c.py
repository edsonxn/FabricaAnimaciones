# -*- coding: utf-8 -*-
"""GRITO: junta secreta de noche en Querétaro (vela y cuatro camafeos: Allende, Aldama, Hidalgo, Josefa) → «¡LOS DESCUBRIERON!»,
Josefa encerrada tras la reja manda un recado volando → amanecer en Dolores: iglesia, campana que suena, gente que llega,
calendario 16 SEP 1810, Hidalgo y «¡EL GRITO DE DOLORES!» → estandarte de la Virgen de Guadalupe y Hidalgo «el Zorro» →
PREGUNTA 1 (botón de pausa, cuenta regresiva) → RESPUESTA (calendario gigante, chispas, «¡ESO!»)."""
import math

import numpy as np

from acuarela import (H, W, TINTA, brillo, curva, degradado, e_back, e_in, e_out, elipse, forma, lavado, linea, pr, rgb, rotulo,
                      rrect, suave, terminar)
from comun import T0, ww, FIN
from fondos_amaya import papel, _manchas
from iconos_ia import palomita, estrella
from personajes import AMARILLO, destello, exclama, pregunta
from kit_amaya import (AZUL, CAFE, CREMA, DORADO, GRIS, ROJO, VERDE, cache, cam, chispas, cuenta, entra, fecha, gente, letrero,
                       papa, pausa, tarjeta)

T_INI = T0("grito")
C = "grito"
tQro, tEsc, tAll, tAld, tHid, tJos, tCorr = (ww(C, 0, "queretaro"), ww(C, 0, "escondidas"), ww(C, 0, "allende"),
                                             ww(C, 0, "aldama"), ww(C, 0, "hidalgo"), ww(C, 0, "josefa"), ww(C, 0, "corregidora"))
tDesc, tEnc, tAvisar, tSalvo = ww(C, 1, "descubrieron"), ww(C, 1, "encerraron"), ww(C, 1, "avisar"), ww(C, 1, "salvo")
tMadr, tDiec, tDolores, tGuana, tCampana, tGente, tGrito = (ww(C, 2, "madrugada"), ww(C, 2, "dieciseis"), ww(C, 2, "dolores"),
                                                            ww(C, 2, "guanajuato"), ww(C, 2, "campana"), ww(C, 2, "gente"),
                                                            ww(C, 2, "grito"))
tBand, tVirgen, tDato, tZorro, tListo = (ww(C, 3, "bandera"), ww(C, 3, "virgen"), ww(C, 3, "dato"), ww(C, 3, "zorro"),
                                         ww(C, 3, "listo"))
tPreg, tQue, tFinP = ww("preg1", 0, "pausa"), ww("preg1", 0, "que"), FIN("preg1")
T_RESP = T0("resp1")
tR16, tEso = ww("resp1", 0, "dieciseis"), ww("resp1", 0, "eso")

T_DESC = tDesc - 0.6
T_DOL = tMadr - 0.6
T_BAN = tBand - 0.5
T_PREG = T0("preg1")


def vela(im, x, y, t, s=1.0):
    forma(im, rrect(x, y, 40 * s, 120 * s, 8), CREMA, t, 11001, tinta=3)
    fl = 1 + 0.12 * math.sin(t * 13) + 0.06 * math.sin(t * 29)
    forma(im, curva([(x, y - 60 * s - 70 * s * fl), (x + 18 * s, y - 75 * s), (x, y - 60 * s), (x - 18 * s, y - 75 * s)], 6, True),
          rgb("ffb84a"), t, 11002, tinta=2)
    brillo(im, x, y - 100 * s, 420 * s * fl, rgb("ffcf7a"), 0.55)


def junta(t):
    def f():
        im = papel("frio")
        degradado(im, np.array([0.16, 0.2, 0.32], np.float32), np.array([0.22, 0.24, 0.36], np.float32))
        forma(im, rrect(960, 860, 1100, 120, 20), rgb("6a4a2a"), 0, 11010, tinta=5)            # mesa
        return im
    im = cache("junta", f).copy()
    vela(im, 960, 760, t)
    letrero(im, "QUERÉTARO · 1810", 960, 110, 60, t, col=CREMA, seed=11020, esc=entra(t, tQro - 0.2))
    for k, (n, nom, x, tk) in enumerate((("allende", "ALLENDE", 300, tAll), ("aldama", "ALDAMA", 660, tAld),
                                         ("hidalgo", "HIDALGO", 1120, tHid), ("josefa", "JOSEFA", 1470, tJos))):
        cam(im, n, x, 430 + 10 * math.sin(t * 2 + k), 0.78 * entra(t, tk - 0.25), t, nom, seed=10 + k)
    if t > tEsc - 0.2:
        rotulo(im, "¡SHHH!", 960, 330, 84, rgb("f4f1e6"), t, seed=11030, esc=entra(t, tEsc - 0.2), alfa=1 - pr(t, tAll, tAll + 0.5))
    if t > tCorr - 0.2:
        letrero(im, "LA CORREGIDORA", 1420, 150, 44, t, col=AMARILLO, seed=11040, esc=entra(t, tCorr - 0.2))
    return im


def descubiertos(t):
    im = cache("desc", lambda: papel("rosa")).copy()
    rotulo(im, "¡LOS DESCUBRIERON!", 960, 120, 92, ROJO, t, seed=11100, esc=entra(t, tDesc - 0.2))
    exclama(im, 1500, 120, 1.4 * entra(t, tDesc), t, seed=11101)
    # casa con ventana enrejada; Josefa adentro
    forma(im, rrect(560, 620, 640, 600, 16), rgb("e8c49a"), t, 11110, tinta=5)
    forma(im, np.array([(200, 340), (560, 170), (920, 340)], np.float32), rgb("b5533f"), t, 11111, tinta=5)
    forma(im, rrect(560, 600, 380, 420, 12), rgb("3a3040"), t, 11112, tinta=4)
    cam(im, "josefa", 560, 590, 0.62, t, "", seed=20)
    ej = entra(t, tEnc - 0.2)
    for k in range(5):
        linea(im, [(410 + 75 * k, 390), (410 + 75 * k, 390 + 420 * ej)], 9, rgb("4a4a52"), seed=11120 + k, t=t)
    if ej > 0.5:
        rotulo(im, "ENCERRADA", 560, 880, 56, TINTA, t, seed=11125, tinta=False)
    # el recado vuela hacia los demás
    if t > tAvisar - 0.3:
        u = e_out(pr(t, tAvisar - 0.3, tAvisar + 1.0))
        x, y = 760 + 760 * u, 560 - 260 * math.sin(math.pi * u)
        tarjeta(im, x, y, 150, 100, t, CREMA, 11130, rot=0.3 * math.sin(t * 6))
        linea(im, [(x - 60, y - 20), (x, y + 15), (x + 60, y - 20)], 4, seed=11131, t=t)
        cam(im, "allende", 1560, 560, 0.5 * entra(t, tAvisar + 0.6), t, "", seed=21)
        if u > 0.95:
            exclama(im, 1660, 360, 1.0, t, seed=11132)
    if t > tSalvo - 0.3:
        letrero(im, "¡ELLA SALVÓ EL PLAN!", 960, 990, 60, t, col=AMARILLO, seed=11140, esc=entra(t, tSalvo - 0.3))
    return im


def iglesia(im, x, y, s, t, campana=0.0):
    forma(im, rrect(x, y, 520 * s, 360 * s, 10), rgb("f0dcb4"), t, 11200, tinta=5, sombra=(rgb("c9a77a"), 24, 0, 0.5))
    forma(im, np.array([(x - 290 * s, y - 180 * s), (x, y - 330 * s), (x + 290 * s, y - 180 * s)], np.float32), rgb("d9b98a"), t, 11201,
          tinta=5)
    forma(im, rrect(x, y + 70 * s, 130 * s, 220 * s, 60 * s), rgb("6a4a2a"), t, 11202, tinta=4)       # puerta
    tx = x + 330 * s                                                                                     # torre
    forma(im, rrect(tx, y - 120 * s, 170 * s, 600 * s, 10), rgb("efd8ae"), t, 11203, tinta=5)
    forma(im, rrect(tx, y - 330 * s, 110 * s, 130 * s, 50 * s), rgb("3a3040"), t, 11204, tinta=3.5)
    ang = 0.6 * math.sin(t * 9) * campana
    bx, by = tx + math.sin(ang) * 30 * s, y - 320 * s
    forma(im, curva([(bx - 40 * s, by + 40 * s), (bx - 30 * s, by - 30 * s), (bx, by - 45 * s), (bx + 30 * s, by - 30 * s),
                     (bx + 40 * s, by + 40 * s)], 6, True), DORADO, t, 11205, tinta=3)
    linea(im, [(tx, y - 470 * s), (tx, y - 560 * s)], 7 * s, seed=11206, t=t)
    linea(im, [(tx - 30 * s, y - 530 * s), (tx + 30 * s, y - 530 * s)], 7 * s, seed=11207, t=t)
    if campana > 0.1:
        for k in range(3):
            a = (t * 1.6 + k / 3) % 1
            linea(im, curva([(tx + 120 * s + 120 * a * s, by - 80 * s), (tx + 150 * s + 120 * a * s, by),
                             (tx + 120 * s + 120 * a * s, by + 80 * s)], 6), 8 * (1 - a) + 1, AMARILLO, seed=11210 + k, t=t,
                  alfa=campana * (1 - a))


def dolores(t):
    def f():
        im = papel("calido")
        degradado(im, rgb("f6b98a"), rgb("fbe7c6"), 0, 700)
        forma(im, elipse(300, 640, 160, 160), rgb("ffd27a"), 0, 11220, tinta=0, alfa=0.9)          # sol que sale
        forma(im, np.array([(0, 760), (W, 740), (W, H), (0, H)], np.float32), rgb("d9c08e"), 0, 11221, tinta=0)
        linea(im, [(0, 760), (W, 740)], 5, seed=11222)
        return im
    im = cache("dolores", f).copy()
    camp = pr(t, tCampana - 0.2, tCampana + 0.3) * (1 - pr(t, tGrito + 1.5, tGrito + 2.5))
    iglesia(im, 820, 560, 1.0, t, camp)
    fecha(im, 1560, 300, 0.75 * entra(t, tDiec - 0.3), t, "16", "SEP", "1810", seed=11230)
    if tDolores - 0.2 < t < tGrito - 0.2:
        letrero(im, "DOLORES, GUANAJUATO", 760, 110, 54, t, col=CREMA, seed=11240, esc=entra(t, tDolores - 0.2))
    cam(im, "hidalgo", 380, 520, 0.55 * entra(t, tDolores + 1.0), t, "HIDALGO", seed=30)
    if t > tGente - 0.5:
        for k in range(9):
            u = e_out(pr(t, tGente - 0.5 + 0.12 * k, tGente + 1.0 + 0.12 * k))
            x = (W + 80 if k % 2 else -80) + ((560 + 80 * k) - (W + 80 if k % 2 else -80)) * u
            gente(im, x, 900 + 30 * (k % 3) + 6 * abs(math.sin(t * 8 + k)) * (u < 1), 2.0, t, seed=70 + k,
                  cara="grito" if t > tGrito else "normal")
    if t > tGrito - 0.2:
        rotulo(im, "¡EL GRITO DE DOLORES!", 820, 110, 92, ROJO, t, seed=11250, esc=entra(t, tGrito - 0.2))
    return im


def estandarte(im, x, y, s, t, seed=11300):
    linea(im, [(x - 200 * s, y - 330 * s), (x - 200 * s, y + 420 * s)], 12 * s, CAFE, seed=seed, t=t)
    on = 10 * math.sin(t * 2.5)
    forma(im, curva([(x - 190 * s, y - 300 * s), (x + 200 * s, y - 290 * s + on), (x + 210 * s, y + 230 * s - on),
                     (x - 190 * s, y + 220 * s)], 6, True), CREMA, t, seed + 1, tinta=4)
    # la Virgen pintada a la manera de los estandartes: aura de rayos, manto verde azulado con estrellas, túnica rosa
    for k in range(16):
        a = 2 * math.pi * k / 16
        linea(im, [(x + math.cos(a) * 95 * s, y - 20 * s + math.sin(a) * 150 * s), (x + math.cos(a) * 130 * s, y - 20 * s + math.sin(a) * 195 * s)],
              5 * s, DORADO, seed=seed + 10 + k, t=t)
    forma(im, elipse(x, y - 20 * s, 90 * s, 150 * s), rgb("f2c27a"), t, seed + 2, tinta=2.5)
    forma(im, curva([(x - 15 * s, y - 120 * s), (x + 60 * s, y - 60 * s), (x + 55 * s, y + 110 * s), (x - 55 * s, y + 110 * s),
                     (x - 60 * s, y - 60 * s)], 6, True), rgb("e7a0a6"), t, seed + 3, tinta=2.5)
    forma(im, curva([(x, y - 150 * s), (x + 80 * s, y - 70 * s), (x + 70 * s, y + 120 * s), (x + 25 * s, y + 120 * s),
                     (x + 35 * s, y - 60 * s), (x, y - 110 * s), (x - 35 * s, y - 60 * s), (x - 25 * s, y + 120 * s),
                     (x - 70 * s, y + 120 * s), (x - 80 * s, y - 70 * s)], 6, True), rgb("3f8f84"), t, seed + 4, tinta=2.5)
    forma(im, elipse(x, y - 115 * s, 22 * s, 26 * s), rgb("d9a07a"), t, seed + 5, tinta=2)
    for k in range(6):
        forma(im, elipse(x + (-50 + 20 * k) * s, y + (-40 + 25 * (k % 3)) * s, 4 * s, 4 * s), DORADO, t, seed + 20 + k, tinta=0)
    forma(im, curva([(x - 50 * s, y + 130 * s), (x, y + 155 * s), (x + 50 * s, y + 130 * s), (x, y + 145 * s)], 6, True), rgb("6aa0c8"),
          t, seed + 6, tinta=2)


def zorro(im, x, y, s, t, seed=11400):
    nar = rgb("e07a32")
    for d in (-1, 1):
        forma(im, np.array([(x + d * 40 * s, y - 40 * s), (x + d * 95 * s, y - 140 * s), (x + d * 110 * s, y - 20 * s)], np.float32),
              nar, t, seed + d, tinta=3)
    forma(im, curva([(x - 120 * s, y - 30 * s), (x, y - 70 * s), (x + 120 * s, y - 30 * s), (x + 30 * s, y + 90 * s),
                     (x, y + 110 * s), (x - 30 * s, y + 90 * s)], 6, True), nar, t, seed + 2, tinta=4)
    for d in (-1, 1):
        forma(im, curva([(x + d * 115 * s, y - 25 * s), (x + d * 30 * s, y + 10 * s), (x + d * 10 * s, y + 90 * s)], 4, True), CREMA, t,
              seed + 4 + d, tinta=0)
        forma(im, elipse(x + d * 40 * s, y - 10 * s, 9 * s, 12 * s), TINTA, t, seed + 7 + d, tinta=0)
    forma(im, elipse(x, y + 100 * s, 14 * s, 11 * s), TINTA, t, seed + 9, tinta=0)


def bandera_y_zorro(t):
    im = cache("banz", lambda: papel("sepia")).copy()
    estandarte(im, 520, 560, 1.35 * entra(t, tBand - 0.3) + 0.01, t)
    if t > tVirgen - 0.2:
        letrero(im, "VIRGEN DE GUADALUPE", 520, 1000, 46, t, col=CREMA, seed=11500, esc=entra(t, tVirgen - 0.2))
    if t > tDato - 0.3:
        letrero(im, "DATO CHIDO", 1250, 120, 60, t, col=AMARILLO, seed=11510, esc=entra(t, tDato - 0.3), rot=0.04)
        cam(im, "hidalgo", 1080, 500, 0.7 * entra(t, tDato), t, "HIDALGO", seed=31)
    if t > tZorro - 0.3:
        ez = entra(t, tZorro - 0.3)
        zorro(im, 1420, 560, 1.2 * ez + 0.01, t)
        rotulo(im, "EL ZORRO", 1300, 880, 90, rgb("c45a1e"), t, seed=11520, esc=ez)
    return im


def pregunta1(t):
    im = cache("preg", lambda: papel("calido")).copy()
    pausa(im, 960, 330, 1.2 * entra(t, tPreg - 0.3), t, seed=11600)
    if t > tQue - 0.3:
        letrero(im, "¿QUÉ DÍA EMPEZÓ LA INDEPENDENCIA?", 960, 700, 58, t, col=CREMA, seed=11610, esc=entra(t, tQue - 0.3))
    cuenta(im, 960, 900, t, tFinP + 0.15, T_RESP + 0.1, s=0.8, seed=11620)
    for k in range(2):
        pregunta(im, 300 + 1300 * k, 400, 1.6 * entra(t, tQue + 0.2 * k), t, seed=1012 + k)
    return im


def respuesta1(t):
    im = cache("resp1", lambda: papel("calido")).copy()
    e = entra(t, tR16 - 0.2, 0.45)
    fecha(im, 960, 520, 1.4 * e, t, "16", "SEP", "1810", seed=11700)
    chispas(im, 960, 520, 360, t, tR16, seed=11710, col=AMARILLO)
    if t > tEso - 0.3:
        palomita(im, 1400, 420, 2.6 * entra(t, tEso - 0.3), t, seed=11720, col=VERDE)
        rotulo(im, "¡ESO!", 520, 420, 130, VERDE, t, seed=11730, esc=entra(t, tEso - 0.3))
    return im


TRAMOS = [(T_INI, junta), (T_DESC, descubiertos), (T_DOL, dolores), (T_BAN, bandera_y_zorro), (T_PREG, pregunta1),
          (T_RESP, respuesta1)]


def _base(t):
    from comun import desborde
    i = max(k for k, (t0, _) in enumerate(TRAMOS) if t >= t0 or k == 0)
    t0, f = TRAMOS[i]
    if i > 0 and t < t0 + 0.6:
        return desborde(TRAMOS[i - 1][1](t), f(t), pr(t, t0, t0 + 0.6), W / 2, H / 2)
    return f(t)


def cuadro_crudo(t):
    im = _base(t)
    papa(im, t, 1770, H + 30, alto=330)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
