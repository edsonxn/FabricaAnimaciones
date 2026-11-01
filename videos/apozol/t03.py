# -*- coding: utf-8 -*-
"""Escena 3 · conquista y fundación: Oñate baja por el cañón (1530), la encomienda como infografía, San Miguel Atotonilco se levanta junto a la
poza de agua caliente (≈1538), el nombre en náhuatl y las ruinas del primer templo; el cielo se enrojece."""
import math

import numpy as np

import kz_ui as U
import kz_iso as I
import kz_iso_deco as DC
import kz_abstracto as AB
import kz_pers2d as K2
import plano as P
import paisajes as PA
import mundos_1 as M1
import mundos_2 as M2
import mundos_3 as M3
from motor import W, H, prog, lerp, smooth, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, h01
from reg import shot, snd
from util import *  # noqa: F401,F403
from t01 import acabado

E3 = "atotonilco"
CANON = M2.Canon()
ATO = M3.Atotonilco()
t_hacia, t_treinta, t_llego, t_crist, t_onate, t_nuno, t_sold, t_esp, t_aliados = (
    T(E3, "hacia", frase=0), T(E3, "treinta", frase=0), T(E3, "llego", frase=0), T(E3, "cristobal", frase=0), T(E3, "onate", frase=0), T(E3, "nuno", frase=0),
    T(E3, "soldados", frase=0), T(E3, "espanoles", frase=0), T(E3, "aliados", frase=0))
t_pueblos, t_enc, t_pagar, t_trib, t_trab, t_espanol = (T(E3, "pueblos", frase=1), T(E3, "encomiendas", frase=1), T(E3, "pagar", frase=1), T(E3, "tributo", frase=1),
                                                         T(E3, "trabajar", frase=1), T(E3, "espanol", frase=1))
t_unos, t_ocho, t_fundo, t_aqui, t_san, t_ato = (T(E3, "unos", frase=2), T(E3, "ocho", frase=2), T(E3, "fundo", frase=2), T(E3, "aqui", frase=2), T(E3, "san", frase=2),
                                                 T(E3, "atotonilco", frase=2))
t_arc, t_agua, t_cal, t_ato2, t_nah, t_quiere = (T(E3, "arcangel", frase=3), T(E3, "agua", frase=3), T(E3, "caliente", frase=3), T(E3, "atotonilco", frase=3),
                                                 T(E3, "nahuatl", frase=3), T(E3, "quiere", frase=3))
t_cal2 = T(E3, "caliente", frase=3, n=1)
t_primer, t_templo, t_sant, t_hoy, t_ruinas = (T(E3, "primer", frase=4), T(E3, "templo", frase=4), T(E3, "santiago", frase=4), T(E3, "hoy", frase=4), T(E3, "ruinas", frase=4))
t_pero, t_trang, t_poco = T(E3, "pero", frase=5), T(E3, "tranquilidad", frase=5), T(E3, "poco", frase=5)
T_A = T0(E3)
T_B = INI(E3, 1) - 0.12
T_C = INI(E3, 2) - 0.15
T_D = t_arc - 0.35
T_E = INI(E3, 4) - 0.15
T_F = INI(E3, 5) - 0.1


def _pie(lz, iso, x, y, z, texto, color, t, t0, t1, px=40, dy=-70, cola="abajo"):
    k = U.pop(t, t0) * U.salida(t, t1)
    if k > 0.01:
        sx, sy = iso.P(x, y, z)
        U.llamada(lz, float(sx), float(sy) + dy, texto, color=color, px=px, k=k, cola=cola)


# ------------------------------------------------------------------------------------------------ A. Oñate llega al cañón (1530)
def cam_a(t):
    u = max(0.0, t - (T_A + 0.3))
    yc = -300.0 + 26.0 * u + 120
    return (236 + 18 * math.sin((yc + 60) * 0.011) + 40, yc - 10, 0.0, 1.4)


@shot(T_A, bg=lambda t: PA.cielo(0.05), post=[acabado], ent=("fundido", 0.5))
def a_onate(lz, t):
    cx, cy, cz, zm = cam_a(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    PA.sol(lz, 1560, 200, 62, t, 0.05)
    PA.sierras(lz, t, 14 * (t - T_A), 0.05, y0=330, capas=3, semilla=61)
    DC.aves(lz, t, n=5, seed=9)
    CANON.suelo(lz, iso, t)
    CANON.camino(lz, iso)
    m = CANON.objetos(t, "caxcan", contorno=False)
    yc = M3.columna(m, t, T_A + 0.3, vel=26.0, y_ini=-300.0)
    m.dibujar(lz, iso)
    U.fecha_lugar(lz, t, t_treinta - 0.2, t_llego + 6.0, "Cañón de Juchipila", "≈ 1530")
    _pie(lz, iso, 236 + 18 * math.sin((yc + 60) * 0.011), yc, 60, "Cristóbal de Oñate", U.COL["rojo"], t, t_crist, t_nuno + 1.2, px=44, dy=-90)
    k = U.pop(t, t_sold) * U.salida(t, T_B - 0.1)
    if k > 0.01:
        U.llamada(lz, 1180, 520, "soldados españoles", color=U.COL["rojo"], px=48, k=k, cola=None)
    k = U.pop(t, t_aliados) * U.salida(t, T_B - 0.1)
    if k > 0.01:
        U.llamada(lz, 1600, 440, "aliados indígenas", color=U.COL["teal"], px=48, k=k, cola=None)
    snd(t_llego, "cuerno", 0.4)
    snd(t_sold, "pasos", 0.35)
    snd(t_aliados, "pasos", 0.3)


# ------------------------------------------------------------------------------------------------ B. la encomienda
@shot(T_B, bg=lambda t: bg_grad((255, 226, 170), (210, 120, 96), mid=(246, 176, 120), ym=0.62), post=[acabado], ent=("fundido", 0.5))
def b_encomienda(lz, t):
    PA.sol(lz, 1000, 300, 90, t, 0.25)
    for i, (x, y, s) in enumerate(((300, 330, 1.0), (1180, 280, 0.8), (1700, 360, 0.9))):          # nubes
        for dx, dy, r in ((-60, 10, 40), (0, -14, 52), (64, 8, 42)):
            lz.relleno(circulo(x + dx * s + 14 * math.sin(t * 0.3 + i), y + dy * s, r * s, 18), (255, 246, 232), alfa=0.8, capa=0)
    lz.relleno(np.array([(-40, 760), (W + 40, 720), (W + 40, H + 20), (-40, H + 20)]), (176, 128, 92), capa=0)
    lz.relleno(np.array([(-40, 830), (W + 40, 800), (W + 40, 900), (-40, 930)]), (230, 200, 152), capa=0)
    for i in range(14):
        lz.relleno(elipse(60 + 140 * i, 990 + 10 * (i % 3), 44, 8, 0, 12), (150, 108, 80), alfa=0.35, capa=0)
    # el pueblo (izquierda): casas grandes y gente
    for i, (x, y, s) in enumerate(((150, 790, 2.0), (420, 780, 1.7), (680, 800, 1.9))):
        PA.casita(lz, x, y, s, 0.0, muro=[(236, 200, 150), (240, 214, 170), (226, 176, 140)][i], techo=[(190, 84, 70), (170, 92, 96), (200, 110, 70)][i], chimenea=(i == 1), t=t, seed=i)
    kp = pk(t, t_pueblos - 0.1, 0.5)
    if kp > 0.01:
        for i, (x, tipo) in enumerate(((250, "caxcan"), (410, "caxcana"), (600, "caxcan"))):
            K2.cuerpo(lz, x, 950, 46 * kp, tipo, t, piernas="camina" if t > t_pagar else "idle", brazos="balanceo", mirar=1, vista="perfil", seed=i + 5)
        U.llamada(lz, 400, 440, "los pueblos", color=U.COL["teal"], px=54, k=U.pop(t, t_pueblos) * U.salida(t, t_enc - 0.1), cola=None)
    # el encomendero (derecha)
    ke = pk(t, t_enc - 0.1, 0.6)
    if ke > 0.01:
        lz.halo(1620, 640, 340, (255, 214, 150), alfa=0.35, dureza=1.1, capa=0)
        K2.busto(lz, 1640, 1040, 175 * ke, "encomendero", t, yaw=0.45, emocion="serio", ojos="abiertos", seed=4, habla=0.0)
        U.llamada(lz, 1600, 330, "el encomendero", color=U.COL["rojo"], px=54, k=U.pop(t, t_espanol - 0.2) * U.salida(t, T1(E3) - 8.0), cola=None)
    # flujo de tributo (maíz y mantas) hacia el encomendero + el trabajo
    f = prog(t, t_pagar - 0.2, T_C)
    if f > 0.01:
        lz.relleno(np.array([(760, 640), (1180, 640), (1180, 600), (1290, 690), (1180, 780), (1180, 740), (760, 740)]), (255, 150, 50), alfa=0.6, capa=1)
        for i in range(6):
            u = (((t - t_pagar) * 0.2) + i / 6.0) % 1.0
            x = 770 + 520 * u
            y = 735 - 24 * math.sin(u * math.pi)
            (M3.saco if i % 2 == 0 else M3.manta)(lz, x, y, 1.25, capa=2)
        k = U.pop(t, t_pagar) * U.salida(t, T_C - 0.2)
        if k > 0.01:
            U.llamada(lz, 1030, 560, "tributo", color=U.COL["naranja"], px=62, k=k * U.repop(t, t_trib + 0.1), cola=None)
    kt = U.pop(t, t_trab) * U.salida(t, T_C - 0.2)
    if kt > 0.01:
        U.llamada(lz, 1030, 880, "trabajo gratis", color=U.COL["morado"], px=58, k=kt, cola=None)
        K2.cuerpo(lz, 1030, 990, 40, "caxcana", t, piernas="arrodillado", brazos="balanceo", mirar=1, vista="perfil", seed=21)
    k0 = U.pop(t, t_enc) * U.salida(t, T_C - 0.2)
    if k0 > 0.01:
        U.llamada(lz, W / 2, 130, "ENCOMIENDA", color=U.COL["oscuro"], px=84, k=k0, cola=None)
    snd(t_enc, "pop", 0.45)
    snd(t_pagar, "monedas", 0.3)


# ------------------------------------------------------------------------------------------------ C. San Miguel Atotonilco
def cam_c(t):
    return K(t, [(T_C, (160, 70, 0, 1.35)), (t_fundo, (210, 90, 0, 1.5)), (T_D, (250, 130, 0, 1.6))])


def _obra(t):
    return float(smooth(prog(t, T_C + 0.5, t_san + 0.8)))


@shot(T_C, bg=lambda t: PA.cielo(0.0), post=[acabado], ent=("fundido", 0.6))
def c_fundacion(lz, t):
    cx, cy, cz, zm = cam_c(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    PA.sol(lz, 1560, 200, 62, t, 0.0)
    PA.sierras(lz, t, 14 * (t - T_C), 0.0, y0=330, capas=3, semilla=67)
    DC.aves(lz, t, n=5, seed=10)
    ATO.suelo(lz, iso, t)
    templo = float(smooth(prog(t, t_fundo, t_san + 1.2)))
    m = ATO.objetos(t, obra=_obra(t), templo=templo)
    m.dibujar(lz, iso)
    # el reloj: 1530 -> 1538
    yr = int(round(lerp(1530, 1538, e_inout(prog(t, t_unos, t_ocho + 0.9)))))
    k = U.pop(t, t_unos - 0.05) * U.salida(t, T_D - 0.2)
    if k > 0.01:
        AB.contador_atras(lz, 1560, 160, yr, px=140, k=k)
        U.llamada(lz, 1560, 280, "ocho años después", color=U.COL["naranja"], px=44, k=U.pop(t, t_ocho) * U.salida(t, T_D - 0.2), cola=None)
    k = U.pop(t, t_san) * U.salida(t, T_D - 0.2)
    if k > 0.01:
        sx, sy = iso.P(160, -50, 90)
        U.llamada(lz, float(sx), float(sy) - 90, "San Miguel Atotonilco", color=U.COL["morado"], px=52, k=k * U.repop(t, t_ato + 0.1), cola="abajo")
    snd(t_fundo, "obra", 0.4)
    snd(t_san, "campana", 0.4)


# ------------------------------------------------------------------------------------------------ D. nombre de arcángel y de agua caliente
@shot(T_D, bg=lambda t: PA.cielo(0.0), post=[acabado], ent=("zoom", 0.55))
def d_nombre(lz, t):
    k = K(t, [(T_D, (290, 150, 0, 1.7)), (T_E, (292, 150, 0, 2.1))])
    iso = I.Iso(float(k[0]), float(k[1]), float(k[2]), float(k[3]))
    PA.sol(lz, 1560, 200, 62, t, 0.0)
    PA.sierras(lz, t, 14 * (t - T_D), 0.0, y0=330, capas=3, semilla=67)
    ATO.suelo(lz, iso, t)
    m = ATO.objetos(t, obra=1.0, templo=1.0, vapor=1.6)
    m.dibujar(lz, iso)
    # el arcángel en un medallón con estandarte
    ka = pk(t, t_arc - 0.1, 0.6) * (1 - smooth(prog(t, t_agua + 0.3, t_agua + 0.8)))
    if ka > 0.01:
        lz.relleno(circulo(430, 400, 250 * ka, 40), (50, 40, 120), alfa=0.9, capa=2)
        lz.trazo(circulo(430, 400, 250 * ka, 40), (255, 206, 72), 10.0, cerrado=True, afinar=False, temblor=0.0, capa=2)
        with lz.recorte(circulo(430, 400, 240 * ka, 40)):
            lz.degradado(circulo(430, 400, 240 * ka, 40), (130, 160, 255), (60, 40, 140), (430, 160), (430, 640), capa=2)
        M3.san_miguel(lz, 430, 600, 1.9 * ka, t, capa=2)
        U.llamada(lz, 430, 690, "arcángel", color=U.COL["azul"], px=54, k=U.pop(t, t_arc), cola=None)
    # ecuación: atl + totonilli + co = en el agua caliente
    items = (("atl", "agua", t_agua, U.COL["azul"]), ("totonilli", "caliente", t_cal, U.COL["rojo"]), ("-co", "en", t_ato2, U.COL["morado"]))
    for i, (a, b, t0, col) in enumerate(items):
        kk = U.pop(t, t0 - 0.1) * U.salida(t, T_E - 0.2)
        if kk > 0.01:
            U.llamada(lz, 1520, 250 + 120 * i, f"{a} = {b}", color=col, px=52, k=kk, cola=None)
    kr = U.pop(t, t_quiere) * U.salida(t, T_E - 0.2)
    if kr > 0.01:
        U.llamada(lz, 1520, 640, "ATOTONILCO", color=U.COL["oscuro"], px=64, k=kr, cola=None)
        U.llamada(lz, 1520, 740, "en el agua caliente", color=U.COL["rojo"], px=50, k=kr * U.repop(t, t_cal2 + 0.1), cola=None)
    snd(t_arc, "bling", 0.4)
    snd(t_agua, "pop", 0.35)
    snd(t_cal, "siseo", 0.4)


# ------------------------------------------------------------------------------------------------ E. las ruinas del primer templo
@shot(T_E, bg=lambda t: bg_grad((90, 60, 130), (236, 140, 100), mid=(190, 96, 120), ym=0.55), post=[acabado], ent=("fundido", 0.6))
def e_ruinas(lz, t):
    c = K(t, [(T_E, (150, 90, 0, 1.7)), (T_F, (140, 90, 0, 2.05))])
    iso = I.Iso(float(c[0]), float(c[1]), float(c[2]), float(c[3]))
    I.luz(mul=(0.92, 0.88, 1.0), mix=(255, 140, 90), k=0.22)
    PA.sol(lz, 1400, 330, 80, t, 0.6)
    PA.sierras(lz, t, 8 * (t - T_E), 0.5, y0=520, capas=3, semilla=71)
    DC.aves(lz, t, n=4, seed=14, color=(40, 20, 50))
    I.isla(lz, iso, 0, 0, 300, 260, color_top=(172, 170, 104), t=t, seed=71, esp=36)
    DC.parches(lz, iso, 0, 0, 300, 260, (172, 170, 104), n=14, var=18, seed=72, alfa=0.5, tam=(30, 70))
    DC.hierba(lz, iso, 0, 0, 300, 260, n=90, seed=73, t=t, color=(156, 160, 92), flores=0.04)
    M3.ruinas_mundo(t).dibujar(lz, iso)
    I.luz()
    _pie(lz, iso, 130, 80, 100, "templo de Santiago", U.COL["morado"], t, t_sant - 0.1, T_F - 0.2, px=52, dy=-60)
    k = U.pop(t, t_ruinas) * U.salida(t, T_F - 0.2)
    if k > 0.01:
        U.llamada(lz, 1500, 860, "hoy: ruinas", color=U.COL["oscuro"], px=56, k=k, cola=None)
    snd(t_primer, "viento", 0.3)
    snd(t_ruinas, "golpe_grave", 0.3)


# ------------------------------------------------------------------------------------------------ F. la tranquilidad duró poco
def amb_f(t):
    return float(smooth(prog(t, T_F, T1(E3) - 0.2)))


def _humos(lz, t, amb):
    for i, x in enumerate((420, 900, 1420)):
        a = amb * min(1.0, prog(t, T_F + 0.2 * i, T_F + 1.0 + 0.2 * i))
        if a <= 0.01:
            continue
        for q in range(7):
            u = ((t * 0.18 + q / 7 + i * 0.3) % 1.0)
            lz.relleno(circulo(x + 40 * math.sin(u * 4 + i) + u * 80, 640 - u * 380, 22 + 60 * u, 18), (60, 36, 70), alfa=0.55 * (1 - u) * a, capa=0)


@shot(T_F, bg=lambda t: PA.cielo(round(amb_f(t), 1)), post=[acabado], ent=("fundido", 0.7))
def f_poco(lz, t):
    amb = amb_f(t)
    cx = 30.0 * (t - T_F)
    PA.sol(lz, 1500, 280, 66, t, amb)
    PA.sierras(lz, t, cx, amb, y0=640, capas=5, semilla=81)
    _humos(lz, t, amb)
    PA.rio(lz, t, amb)
    PA.aldea(lz, t, amb, n=5, seed=12)
    PA.pared_canon(lz, t, -1, amb, ancho=380, seed=3)
    PA.pared_canon(lz, t, 1, amb, ancho=380, seed=6)
    PA.aves(lz, t, n=5, seed=5)
    PA.flores_frente(lz, t, cx, n=10, amb=amb, seed=9)
    snd(t_pero, "grave_inquietante", 0.35)
