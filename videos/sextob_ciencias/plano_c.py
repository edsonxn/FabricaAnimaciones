# -*- coding: utf-8 -*-
"""JERINGA + PREGUNTA 1 + RESPUESTA 1.
jeringa: foto real de su cuaderno + «EL EXPERIMENTO DE LA JERINGA»; el dedo tapa la punta; el émbolo baja cada vez más lento
(«CUESTA MÁS») hasta que «¡YA NO BAJA!»; al soltarlo regresa de golpe («¡ZAS!») y el dedo se pone rojo («¡AY!», PRESIÓN) → jalar:
cuesta subirlo y al soltarlo se regresa rápido → acercamiento: «ADENTRO HAY AIRE», las partículas se aprietan, «¡YA NO SE PUEDEN
JUNTAR MÁS!» y flechas rojas que empujan de regreso.
preg1: PAUSA + «¿CÓMO PODEMOS SABER QUE LOS GASES SON MATERIA?» + jeringa con «?» + cuenta 3-2-1.
resp1: «¡OCUPAN UN LUGAR!» + jeringa que no baja hasta el fondo + OCUPA LUGAR ✓ TIENE MASA ✓ = MATERIA."""
import math

import numpy as np

from acuarela import H, W, TINTA, e_out, elipse, forma, lavado, linea, pr, rgb, rotulo, rrect, suave, terminar
from comun import FIN, T0, ww
from comun_ci import cartel, pantalla_pregunta, titulo
from fondos_amaya import papel
from iconos_ia import marca_x, palomita
from personajes import AMARILLO, destello, exclama, pregunta
from kit_amaya import AZUL, CREMA, GRIS, MORADO, ROJO, VERDE, cache, chispas, entra, letrero, papa, tarjeta
from piezas_es import ROSA_M, polaroid
from piezas_fj import base
from piezas_ci import flecha_empuje, jeringa

T_INI = T0("jeringa")
J, P, R = "jeringa", "preg1", "resp1"
tExp, tDedo, tEmp = ww(J, 0, "experimento"), ww(J, 0, "dedo"), ww(J, 0, "empujan")
tCuesta, tYa, tNo, tSuelt, tReg, tDuele, tPres = (ww(J, 1, "cuesta"), ww(J, 1, "ya"), ww(J, 1, "no"), ww(J, 1, "sueltan"),
                                                 ww(J, 1, "regresa"), ww(J, 1, "duele"), ww(J, 1, "presion"))
T_JALA = ww(J, 2, "y") - 0.3
tJalan, tCuesta2, tSubir, tSoltar, tReg2 = (ww(J, 2, "jalan"), ww(J, 2, "cuesta"), ww(J, 2, "subirlo"), ww(J, 2, "soltarlo"),
                                           ww(J, 2, "regresa"))
T_ZOOM = ww(J, 3, "por") - 0.3
tAdentro, tAire, tApri, tJuntar, tEmpuj = (ww(J, 3, "adentro"), ww(J, 3, "aire"), ww(J, 3, "aprietan"), ww(J, 3, "juntar"),
                                           ww(J, 3, "empujan"))
T_P1 = T0(P)
tP1, tComo, tGasesP, tFinP1 = ww(P, 0, "pausa"), ww(P, 0, "como"), ww(P, 0, "gases"), FIN(P)
T_R1 = T0(R)
tOcupan, tJerR, tFondo, tOcupaR, tMasaR, tMatR, tEso = (ww(R, 0, "ocupan"), ww(R, 0, "jeringa"), ww(R, 0, "fondo"), ww(R, 0, "ocupa"),
                                                        ww(R, 0, "tiene"), ww(R, 0, "materia"), ww(R, 0, "eso"))
JX, JY, JS = 620, 580, 1.4


def _emb(t):
    """Émbolo en el experimento de empujar: baja cada vez más lento, se queda, y al soltarlo regresa de golpe."""
    u = pr(t, tEmp + 0.2, tNo)
    e = 1 - (1 - u) ** 2.6
    if t > tSuelt:
        r = pr(t, tSuelt + 0.05, tSuelt + 0.4)
        e = (1 - e_out(r)) - 0.08 * math.sin(r * math.pi) * (r < 1)
    return e


def empujar(t):
    im = cache("c_emp", lambda: papel("frio")).copy()
    titulo(im, "EL EXPERIMENTO DE LA JERINGA", t, tExp, 21000, col=AZUL, x=640, y=110, px=66)
    if t > tExp - 0.3:
        polaroid(im, "jeringa", 1400, 230, 1.0 * entra(t, tExp - 0.3), t, rot=0.05, seed=21010, alto=190)
    em = _emb(t)
    ay = pr(t, tDuele - 0.2, tDuele + 0.2) * (1 - pr(t, tPres + 1.0, tPres + 1.6))
    sacude = 6 * math.sin(t * 40) * (pr(t, tCuesta, tNo) - pr(t, tNo, tNo + 0.3))
    pos, mango = jeringa(im, JX, JY + sacude, JS, t, emb=em, dedo=suave(pr(t, tDedo - 0.4, tDedo + 0.2)), seed=21020, ay=ay)
    if tEmp - 0.2 < t < tSuelt:
        flecha_empuje(im, mango + 200, JY - 140, mango + 40, JY - 60, t, col=ROJO, seed=21040, u=pr(t, tEmp - 0.2, tEmp + 0.3))
    if t > tDedo - 0.2 and t < tEmp:
        letrero(im, "PUNTA TAPADA", 240, 330, 40, t, seed=21045, esc=entra(t, tDedo - 0.2), rot=-0.04)
    if tCuesta - 0.2 < t < tSuelt:
        rotulo(im, "CUESTA MÁS...", 640, 820, 60, MORADO, t, seed=21050, esc=entra(t, tCuesta - 0.2))
    if tYa - 0.3 < t < tSuelt:
        letrero(im, "¡YA NO BAJA!", 640, 930, 58, t, col=ROJO, txt=CREMA, seed=21055, esc=entra(t, tYa - 0.3), rot=0.03)
    if tSuelt < t < tDuele - 0.3:
        rotulo(im, "¡ZAS!", 1300, 620, 110, ROJO, t, seed=21060, esc=entra(t, tReg - 0.3), rot=0.1)
        for k in range(3):
            destello(im, 1180 + 120 * k, 470 + 60 * (k % 2), entra(t, tReg - 0.2 + 0.1 * k), t, seed=21062 + k)
    if t > tDuele - 0.3:
        rotulo(im, "¡AY!", 200, 330, 120, ROJO, t, seed=21070, esc=entra(t, tDuele - 0.3), rot=-0.1)
        exclama(im, 330, 330, 1.2 * entra(t, tDuele - 0.2), t, seed=21072, col=ROJO)
    if t > tPres - 0.3:
        letrero(im, "POR LA PRESIÓN", 640, 860, 58, t, col=AMARILLO, seed=21075, esc=entra(t, tPres - 0.3), rot=-0.03)
    return im


def jalar(t):
    im = cache("c_jal", lambda: papel("calido")).copy()
    titulo(im, "AHORA: JALAR EL ÉMBOLO", t, T_JALA + 0.3, 21100, col=MORADO, x=640, y=110, px=66)
    u = pr(t, tJalan, tSubir + 0.4)
    j = 1 - (1 - u) ** 2.2
    if t > tSoltar:
        j *= 1 - e_out(pr(t, tSoltar + 0.05, tSoltar + 0.35))
    pos, mango = jeringa(im, JX - 60, JY, JS, t, jala=j, dedo=1.0, seed=21020)
    if tJalan - 0.2 < t < tSoltar:
        flecha_empuje(im, mango + 30, JY - 110, mango + 220, JY - 170, t, col=AZUL, seed=21110, u=pr(t, tJalan - 0.2, tJalan + 0.3))
    if tCuesta2 - 0.2 < t < tSoltar:
        rotulo(im, "¡CUESTA MUCHO!", 640, 760, 60, MORADO, t, seed=21120, esc=entra(t, tCuesta2 - 0.2))
    if t > tReg2 - 0.3:
        letrero(im, "¡SE REGRESA RÁPIDO!", 640, 840, 58, t, col=ROJO, txt=CREMA, seed=21125, esc=entra(t, tReg2 - 0.3), rot=0.03)
    return im


def acerca(t):
    im = cache("c_zoom", lambda: papel("frio")).copy()
    em = 0.9 * suave(pr(t, tApri - 0.2, tJuntar))
    pos, mango = jeringa(im, 640, 470, 1.6, t, emb=em, dedo=1.0, seed=21200, n=22)
    if t > tAdentro - 0.3:
        letrero(im, "ADENTRO HAY AIRE", 640, 140, 62, t, col=CREMA, txt=AZUL, seed=21210, esc=entra(t, tAdentro - 0.3), rot=-0.03)
    if t > tApri - 0.3 and t < tJuntar - 0.3:
        rotulo(im, "SE APRIETAN...", 640, 760, 66, MORADO, t, seed=21220, esc=entra(t, tApri - 0.3))
    if t > tJuntar - 0.3:
        letrero(im, "¡YA NO SE PUEDEN JUNTAR MÁS!", 640, 760, 52, t, col=AMARILLO, seed=21225, esc=entra(t, tJuntar - 0.3), rot=0.02)
    if t > tEmpuj - 0.3:
        u = pr(t, tEmpuj - 0.3, tEmpuj + 0.3)
        lat = 14 * math.sin(t * 9)
        flecha_empuje(im, pos + 10, 470, pos + 170 + lat, 470, t, col=ROJO, ancho=18, seed=21230, u=u)
        flecha_empuje(im, 640 - 448 + 20, 470, 640 - 448 - 160 - lat, 470, t, col=ROJO, ancho=18, seed=21235, u=u)
        rotulo(im, "¡Y EMPUJAN DE REGRESO!", 640, 900, 60, ROJO, t, seed=21240, esc=entra(t, tEmpuj - 0.3))
    return im


def preg1(t):
    im = cache("c_p1", lambda: papel("frio")).copy()
    pantalla_pregunta(im, t, tP1, tFinP1, T_R1, 21300, ["¿CÓMO PODEMOS SABER", "QUE LOS GASES SON MATERIA?"], [tComo, tGasesP],
                      y0=430)
    if t > tGasesP:
        jeringa(im, 700, 790, 0.7, t, emb=0.4 + 0.3 * math.sin(t * 2), seed=21320)
        pregunta(im, 1100, 780, 1.6 * entra(t, tGasesP), t, seed=21330)
    return im


def resp1(t):
    im = cache("c_r1", lambda: papel("frio")).copy()
    letrero(im, "RESPUESTA", 260, 120, 56, t, col=VERDE, txt=CREMA, seed=21400, esc=entra(t, T_R1), rot=-0.04)
    if t > tOcupan - 0.3:
        rotulo(im, "¡OCUPAN UN LUGAR!", 900, 130, 84, VERDE, t, seed=21405, esc=entra(t, tOcupan - 0.3))
    if t > tJerR - 0.4:
        e = entra(t, tJerR - 0.4)
        pos, _ = jeringa(im, 560, 420, 1.15 * e + 0.01, t, emb=1.0, seed=21410, n=16)
        if t > tFondo - 0.4:
            x0 = 560 - 322 * 1.15 * e
            linea(im, [(x0 + 40, 420), (pos - 30, 420)], 6, ROJO, seed=21420, t=t, alfa=0.0)
            letrero(im, "NO BAJÓ HASTA EL FONDO", 560, 600, 44, t, col=AMARILLO, seed=21425, esc=entra(t, tFondo - 0.4), rot=-0.02)
    for k, (txt, tk) in enumerate((("OCUPA LUGAR", tOcupaR), ("TIENE MASA", tMasaR))):
        cartel(im, txt, 420 + 520 * k, 760, 50, t, tk, 21440 + k * 7, ok=True, t_ok=tk + 0.3)
    if t > tMatR - 0.4:
        e = entra(t, tMatR - 0.4)
        forma(im, rrect(700, 910, 640 * e + 1, 110 * e + 1, 22, -0.02), VERDE, t, 21460, tinta=5)
        rotulo(im, "= MATERIA", 700, 916, 66 * e + 1, CREMA, t, seed=21461, rot=-0.02)
    chispas(im, 700, 910, 240, t, tEso, seed=21470, col=AMARILLO)
    if t > tEso - 0.3:
        palomita(im, 1320, 380, 1.6 * entra(t, tEso - 0.3), t, seed=21480, col=VERDE)
    return im


TRAMOS = [(T_INI, empujar), (T_JALA, jalar), (T_ZOOM, acerca), (T_P1, preg1), (T_R1, resp1)]


def cuadro_crudo(t):
    im = base(TRAMOS, t)
    papa(im, t, 1770, H + 30, alto=330)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
