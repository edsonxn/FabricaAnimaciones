# -*- coding: utf-8 -*-
"""Escena 6 · las haciendas: el valle se llena de haciendas, La Purísima y la caña (Porfiriato), la casa grande de San José de la Labor (1775),
el piloncillo hecho a mano y los muros que siguen en pie (hotel desde 1997)."""
import math

import numpy as np

import kz_ui as U
import kz_iso as I
import kz_iso_obj2 as O2
import kz_iso_deco as DC
import kz_abstracto as AB
import plano as P
import paisajes as PA
import mundos_6 as M6
from motor import W, H, prog, lerp, smooth, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, h01
from reg import shot, snd
from util import *  # noqa: F401,F403
from t01 import acabado

E6 = "haciendas"
VAL = M6.Valle()
t_siglos, t_valle, t_lleno, t_hac = T(E6, "siglos", frase=0), T(E6, "valle", frase=0), T(E6, "lleno", frase=0), T(E6, "haciendas", frase=0)
t_pur, t_prim, t_constr, t_17, t_18, t_mejor, t_cana, t_porf = (T(E6, "purisima", frase=1), T(E6, "primeras", frase=1), T(E6, "construcciones", frase=1), T(E6, "diecisiete", frase=1),
                                                                T(E6, "dieciocho", frase=1), T(E6, "mejor", frase=1), T(E6, "cana", frase=1), T(E6, "porfiriato", frase=1))
t_san, t_jose, t_labor, t_casa, t_term, t_set, t_cinco = (T(E6, "san", frase=2), T(E6, "jose", frase=2), T(E6, "labor", frase=2), T(E6, "casa", frase=2), T(E6, "terminada", frase=2),
                                                         T(E6, "setecientos", frase=2), T(E6, "cinco", frase=2))
t_jugo, t_cana2, t_herv, t_pilon, t_hoy, t_mano = (T(E6, "jugo", frase=3), T(E6, "cana", frase=3), T(E6, "hervia", frase=3), T(E6, "piloncillo", frase=3), T(E6, "hoy", frase=3), T(E6, "mano", frase=3))
t_muros, t_pie, t_casa2, t_hotel, t_noventa = T(E6, "muros", frase=4), T(E6, "pie", frase=4), T(E6, "casa", frase=4), T(E6, "hotel", frase=4), T(E6, "noventa", frase=4)
T_A = T0(E6)
T_B = INI(E6, 1) - 0.12
T_C = INI(E6, 2) - 0.12
T_D = INI(E6, 3) - 0.12
T_E = INI(E6, 4) - 0.12


def _iso(c):
    return I.Iso(float(c[0]), float(c[1]), float(c[2]), float(c[3]))


def _pie(lz, iso, x, y, z, texto, color, t, t0, t1, px=40, dy=-70, cola="abajo"):
    k = U.pop(t, t0) * U.salida(t, t1)
    if k > 0.01:
        sx, sy = iso.P(x, y, z)
        U.llamada(lz, float(sx), float(sy) + dy, texto, color=color, px=px, k=k, cola=cola)


# ------------------------------------------------------------------------------------------------ A. el valle se llena de haciendas
@shot(T_A, bg=lambda t: PA.cielo(0.0), post=[acabado], ent=("fundido", 0.7))
def a_valle(lz, t):
    c = K(t, [(T_A, (150, 110, 0, 0.62)), (t_hac, (170, 120, 0, 0.8)), (T_B, (180, 120, 0, 0.88))])
    iso = _iso(c)
    PA.sol(lz, 1560, 200, 62, t, 0.0)
    PA.sierras(lz, t, 14 * (t - T_A), 0.0, y0=330, capas=3, semilla=151)
    DC.aves(lz, t, n=5, seed=12)
    VAL.suelo(lz, iso, t)
    n = 5.4 * float(smooth(prog(t, T_A + 0.5, t_hac + 1.2)))
    m = VAL.objetos(t, n=n)
    m.dibujar(lz, iso)
    k = U.pop(t, t_siglos) * U.salida(t, t_lleno - 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 150, "los siglos siguientes", color=U.COL["morado"], px=58, k=k, cola=None)
    k = U.pop(t, t_hac) * U.salida(t, T_B - 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 150, "haciendas", color=U.COL["naranja"], px=70, k=k * U.repop(t, t_hac + 0.3), cola=None)
    snd(t_hac, "obra", 0.4)


# ------------------------------------------------------------------------------------------------ B. La Purísima y la caña
@shot(T_B, bg=lambda t: PA.cielo(0.0), post=[acabado], ent=("fundido", 0.6))
def b_purisima(lz, t):
    c = K(t, [(T_B, (80, -110, 20, 1.45)), (T_C - 0.4, (90, -100, 20, 1.65))])
    iso = _iso(c)
    PA.sol(lz, 1560, 200, 62, t, 0.0)
    PA.sierras(lz, t, 14 * (t - T_B), 0.0, y0=330, capas=3, semilla=153)
    VAL.suelo(lz, iso, t)
    m = VAL.objetos(t, n=5.0)
    m.dibujar(lz, iso)
    _pie(lz, iso, 85, -115, 90, "La Purísima", U.COL["rojo"], t, t_pur, T_C - 0.2, px=58, dy=-60)
    k = U.pop(t, t_constr) * U.salida(t, t_mejor - 0.1)
    if k > 0.01:
        U.llamada(lz, 400, 220, "siglos XVII y XVIII", color=U.COL["morado"], px=54, k=k, cola=None)
    k = U.pop(t, t_cana) * U.salida(t, T_C - 0.2)
    if k > 0.01:
        sx, sy = iso.P(-60, -150, 0)
        U.llamada(lz, float(sx), float(sy) - 20, "caña de azúcar", color=U.COL["verde"], px=52, k=k, cola="abajo")
    k = U.pop(t, t_porf) * U.salida(t, T_C - 0.2)
    if k > 0.01:
        U.llamada(lz, 1480, 200, "Porfiriato", color=U.COL["naranja"], px=60, k=k, cola=None)
        U.llamada(lz, 1480, 300, "1876 – 1911", color=U.COL["oscuro"], px=46, k=k, cola=None)
    snd(t_pur, "pop", 0.35)
    snd(t_cana, "pop", 0.3)


# ------------------------------------------------------------------------------------------------ C. San José de la Labor: la casa grande de 1775
@shot(T_C, bg=lambda t: PA.cielo(0.0), post=[acabado], ent=("fundido", 0.6))
def c_casa_grande(lz, t):
    u = float(smooth(prog(t, T_C + 0.4, t_term + 1.0)))
    c = K(t, [(T_C, (360, 210, 20, 1.5)), (T_D - 0.4, (370, 220, 30, 1.8))])
    iso = _iso(c)
    PA.sol(lz, 1560, 200, 62, t, 0.0)
    PA.sierras(lz, t, 14 * (t - T_C), 0.0, y0=330, capas=3, semilla=157)
    VAL.suelo(lz, iso, t)
    # las demás haciendas ya están; esta se levanta (n = 3 + u)
    m = VAL.objetos(t, n=3.0 + u)
    m.dibujar(lz, iso)
    _pie(lz, iso, 375, 225, 70, "San José de la Labor", U.COL["morado"], t, t_san, T_D - 0.2, px=54, dy=-80)
    yr = int(lerp(1700, 1775, e_inout(prog(t, t_set - 0.2, t_cinco + 0.5))))
    k = U.pop(t, t_set - 0.2) * U.salida(t, T_D - 0.2)
    if k > 0.01:
        AB.contador_atras(lz, 1560, 170, yr, px=160, k=k)
        U.llamada(lz, 1560, 290, "casa grande terminada", color=U.COL["naranja"], px=46, k=U.pop(t, t_term) * U.salida(t, T_D - 0.2), cola=None)
    snd(t_casa, "obra", 0.4)
    snd(t_cinco, "campana", 0.4)


# ------------------------------------------------------------------------------------------------ D. del jugo al piloncillo, a mano
@shot(T_D, bg=lambda t: bg_grad((255, 220, 170), (236, 150, 110), mid=(250, 186, 130), ym=0.55), post=[acabado], ent=("fundido", 0.6))
def d_piloncillo(lz, t):
    up = float(smooth(prog(t, t_jugo - 0.3, t_jugo + 1.0)))
    uo = float(smooth(prog(t, t_herv - 0.4, t_herv + 0.8)))
    uc = float(smooth(prog(t, t_pilon - 0.2, t_pilon + 2.2)))
    M6.trapiche(lz, t, up, uo, uc, T_D)
    k = U.pop(t, t_jugo) * U.salida(t, t_herv - 0.2)
    if k > 0.01:
        U.llamada(lz, 600, 240, "jugo de caña", color=U.COL["verde"], px=56, k=k, cola=None)
    k = U.pop(t, t_herv) * U.salida(t, t_pilon - 0.2)
    if k > 0.01:
        U.llamada(lz, 1040, 240, "hervir", color=U.COL["rojo"], px=60, k=k, cola=None)
    k = U.pop(t, t_pilon)
    if k > 0.01:
        U.llamada(lz, 1660, 560, "piloncillo", color=U.COL["naranja"], px=64, k=k * U.repop(t, t_pilon + 0.4), cola=None)
    k = U.pop(t, t_mano) * U.salida(t, T1(E6) - 6.0)
    if k > 0.01:
        U.llamada(lz, 1200, 130, "hoy, todavía a mano", color=U.COL["oscuro"], px=62, k=k, cola=None)
    snd(t_jugo, "chorro", 0.35)
    snd(t_herv, "fuego", 0.3)
    snd(t_pilon, "pop", 0.35)


# ------------------------------------------------------------------------------------------------ E. los muros siguen en pie: hotel desde 1997
@shot(T_E, bg=lambda t: bg_grad((60, 40, 110), (250, 150, 100), mid=(170, 80, 120), ym=0.55), post=[acabado], ent=("fundido", 0.7))
def e_hotel(lz, t):
    c = K(t, [(T_E, (360, 210, 40, 1.7)), (T1(E6) - 2.0, (372, 222, 40, 1.95))])
    iso = _iso(c)
    I.luz(mul=(0.92, 0.9, 1.0), mix=(255, 150, 90), k=0.22)
    PA.sol(lz, 1400, 340, 80, t, 0.55)
    PA.sierras(lz, t, 8 * (t - T_E), 0.5, y0=520, capas=4, semilla=161)
    VAL.suelo(lz, iso, t)
    m = VAL.objetos(t, n=5.0, noche=0.6)
    m.dibujar(lz, iso)
    I.luz()
    # luces cálidas en las ventanas y cartel
    sx, sy = iso.P(375, 280, 20)
    lz.halo(float(sx), float(sy) - 30, 150, (255, 214, 140), alfa=0.35 * smooth(prog(t, t_hotel - 0.3, t_hotel + 0.6)), dureza=1.2, capa=2)
    _pie(lz, iso, 375, 225, 70, "casa grande de San José de la Labor", U.COL["morado"], t, t_casa2, t_hotel - 0.1, px=46, dy=-80)
    k = U.pop(t, t_hotel) * U.salida(t, T1(E6) - 0.2)
    if k > 0.01:
        U.llamada(lz, float(sx), float(sy) - 200, "HOTEL", color=U.COL["oro"], px=80, k=k * U.repop(t, t_hotel + 0.3), cola="abajo", color_texto=(60, 28, 70))
    yr = int(lerp(1775, 1997, e_inout(prog(t, t_hotel - 0.5, t_noventa + 1.4))))
    kk = U.pop(t, t_hotel - 0.5) * U.salida(t, T1(E6) - 0.2)
    if kk > 0.01:
        AB.contador_atras(lz, 360, 170, yr, px=150, k=kk)
    snd(t_muros, "viento", 0.25)
    snd(t_hotel, "bling", 0.4)
