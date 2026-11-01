# -*- coding: utf-8 -*-
"""Escena 5 · la paz y los papeles: el amanecer tras la guerra, los frailes confirman la fundación, «Apozol de Santa María Magdalena» bajo Juchipila,
la cédula de 1597 que devuelve las tierras, el archivo del primer alcalde (1806) y los papeles contra las flechas."""
import math

import numpy as np

import kz_ui as U
import kz_iso as I
import kz_abstracto as AB
import kz_pers2d as K2
import kz_iso_obj2 as O2
import kz_gente_iso as G_
import kz_mapa_dib as MD
import plano as P
import paisajes as PA
import mundos_1 as M1
import mundos_3 as M3
import mundos_5 as M5
from motor import W, H, prog, lerp, smooth, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, h01
from reg import shot, snd
from util import *  # noqa: F401,F403
from t01 import acabado

E5 = "paz"
TIE = M5.Tierras()
ATO = M3.Atotonilco()
t_desp, t_paz, t_pareci = T(E5, "despues", frase=0), T(E5, "paz", frase=0), T(E5, "parecia", frase=0)
t_frailes, t_antonio, t_segovia, t_miguel, t_bolonia, t_cons, t_perd, t_miles, t_conf, t_fund = (
    T(E5, "frailes", frase=1), T(E5, "antonio", frase=1), T(E5, "segovia", frase=1), T(E5, "miguel", frase=1), T(E5, "bolonia", frase=1), T(E5, "consiguieron", frase=1),
    T(E5, "perdon", frase=1), T(E5, "miles", frase=1), T(E5, "confirmaron", frase=1), T(E5, "fundacion", frase=1))
t_virr, t_llamo, t_apozol, t_magd, t_dep, t_juch = (T(E5, "virreinato", frase=2), T(E5, "llamo", frase=2), T(E5, "apozol", frase=2), T(E5, "magdalena", frase=2),
                                                    T(E5, "dependia", frase=2), T(E5, "juchipila", frase=2))
t_siete, t_ced, t_real, t_mando, t_dev, t_tierras, t_cap = (T(E5, "siete", frase=3), T(E5, "cedula", frase=3), T(E5, "real", frase=3), T(E5, "mando", frase=3), T(E5, "devolver", frase=3),
                                                           T(E5, "tierras", frase=3), T(E5, "capitan", frase=3))
t_dosc, t_seis, t_alc, t_joaq, t_gav, t_imp, t_arch, t_recup = (T(E5, "doscientos", frase=4), T(E5, "seis", frase=4), T(E5, "alcalde", frase=4), T(E5, "joaquin", frase=4),
                                                                T(E5, "gavilan", frase=4), T(E5, "impulso", frase=4), T(E5, "archivo", frase=4), T(E5, "recuperaran", frase=4))
t_esta, t_pueblo, t_def, t_pap, t_flech = T(E5, "esta", frase=5), T(E5, "pueblo", frase=5), T(E5, "defendio", frase=5), T(E5, "papeles", frase=5), T(E5, "flechas", frase=5)
T_A = T0(E5)
T_B = INI(E5, 1) - 0.12
T_C = INI(E5, 2) - 0.12
T_D = INI(E5, 3) - 0.12
T_E = INI(E5, 4) - 0.12
T_F = INI(E5, 5) - 0.12


def _pie(lz, iso, x, y, z, texto, color, t, t0, t1, px=40, dy=-70, cola="abajo"):
    k = U.pop(t, t0) * U.salida(t, t1)
    if k > 0.01:
        sx, sy = iso.P(x, y, z)
        U.llamada(lz, float(sx), float(sy) + dy, texto, color=color, px=px, k=k, cola=cola)


# ------------------------------------------------------------------------------------------------ A. la paz, o algo que se le parecía
@shot(T_A, bg=lambda t: PA.cielo(0.0), post=[acabado], ent=("fundido", 0.7))
def a_paz(lz, t):
    M5.paz_amanecer(lz, t, T_A)
    k = U.pop(t, t_paz) * U.salida(t, T_B - 0.2)
    if k > 0.01:
        U.llamada(lz, 960, 220, "la paz", color=U.COL["teal"], px=84, k=k, cola=None)
    k = U.pop(t, t_pareci) * U.salida(t, T_B - 0.2)
    if k > 0.01:
        U.llamada(lz, 960, 340, "o algo parecido", color=U.COL["morado"], px=52, k=k, cola=None)
    snd(t_paz, "amanecer", 0.4)


# ------------------------------------------------------------------------------------------------ B. los frailes y la fundación
@shot(T_B, bg=lambda t: bg_grad((54, 30, 66), (128, 72, 70), mid=(88, 48, 70), ym=0.6), post=[acabado], ent=("fundido", 0.6))
def b_frailes(lz, t):
    M5.mesa_frailes(lz, t, T_B, t_conf, t_conf)
    U.bokeh(lz, t, seed=47, n=8, colores=((255, 190, 110), (255, 150, 90)), alfa=0.25)
    for j, (x, t0, nom, yaw, sd, spec) in enumerate(((430, t_segovia - 0.3, "fray Antonio de Segovia", 0.4, 21, "fraile"),
                                                       (1490, t_bolonia - 0.3, "fray Miguel de Bolonia", -0.4, 22, dict(K2.TIPOS["fraile"], pelo=(190, 186, 196), barba="puntiaguda")))):
        k = pk(t, T_B + 0.25 + 0.3 * j, 0.6)
        if k > 0.01:
            K2.busto(lz, x, 820, 150 * k, spec, t, yaw=yaw, emocion="pensativo", ojos="abiertos", seed=sd, habla=0.5 if t0 < t < t0 + 1.4 else 0.0)
            ka = U.pop(t, t0) * U.salida(t, T_C - 0.2)
            if ka > 0.01:
                U.llamada(lz, x, 230, nom, color=U.COL["naranja"] if j == 0 else U.COL["teal"], px=44, k=ka, cola=None)
    # el perdón de miles y el pergamino de la fundación
    kp = U.pop(t, t_perd) * U.salida(t, t_conf - 0.1)
    if kp > 0.01:
        U.llamada(lz, 960, 160, "el perdón de miles de caxcanes", color=U.COL["morado"], px=50, k=kp, cola=None)
    U.pergamino_grande(lz, 960, 650, 680, 340, t, t_conf - 0.3, lineas=("San Miguel Atotonilco", "pueblo de los caxcanes"), titulo="Fundación del pueblo", sello=True)
    kf = U.pop(t, t_fund) * U.salida(t, T_C - 0.2)
    if kf > 0.01:
        U.llamada(lz, 960, 160, "confirman la fundación", color=U.COL["oscuro"], px=56, k=kf, cola=None) if t > t_conf - 0.1 else None
    snd(t_segovia, "campana", 0.3)
    snd(t_conf, "sello", 0.5)


# ------------------------------------------------------------------------------------------------ C. Apozol de Santa María Magdalena
@shot(T_C, bg=lambda t: PA.cielo(0.0), post=[acabado], ent=("fundido", 0.6))
def c_nombre(lz, t):
    c = K(t, [(T_C, (230, 90, 0, 1.45)), (T_D - 0.5, (240, 110, 0, 1.6))])
    iso = I.Iso(float(c[0]), float(c[1]), float(c[2]), float(c[3]))
    PA.sol(lz, 1560, 200, 62, t, 0.0)
    PA.sierras(lz, t, 14 * (t - T_C), 0.0, y0=330, capas=3, semilla=131)
    ATO.suelo(lz, iso, t)
    m = ATO.objetos(t, obra=1.0, templo=1.0)
    m.dibujar(lz, iso)
    # rótulo que cambia de nombre
    k = U.pop(t, T_C + 0.2) * U.salida(t, t_llamo - 0.1)
    if k > 0.01:
        U.llamada(lz, 960, 140, "San Miguel Atotonilco", color=U.COL["morado"], px=58, k=k, cola=None)
    k = U.pop(t, t_llamo) * U.salida(t, T_D - 0.2)
    if k > 0.01:
        U.llamada(lz, 960, 140, "Apozol de Santa María Magdalena", color=U.COL["naranja"], px=60, k=k * U.repop(t, t_magd + 0.1), cola=None)
    kd = U.pop(t, t_dep) * U.salida(t, T_D - 0.2)
    if kd > 0.01:
        # cadena de dependencia hacia el sur
        sx, sy = iso.P(130, 300, 0)
        U.llamada(lz, 1500, 860, "dependía de Juchipila", color=U.COL["rojo"], px=54, k=kd, cola=None)
        lz.trazo(np.array([(1180, 800), (1500, 830)]), (255, 255, 255, 200), 5.0, afinar=False, temblor=0.0, capa=2)
        for i in range(5):
            u = ((t - t_dep) * 0.5 + i / 5.0) % 1.0
            lz.relleno(circulo(1180 + 320 * u, 800 + 30 * u, 8, 10), (255, 214, 90), alfa=0.9, capa=2)
    snd(t_llamo, "pop", 0.35)
    snd(t_dep, "pop", 0.3)


# ------------------------------------------------------------------------------------------------ D. la cédula de 1597
@shot(T_D, bg=lambda t: PA.cielo(0.0), post=[acabado], ent=("fundido", 0.6))
def d_cedula(lz, t):
    u = float(smooth(prog(t, t_mando - 0.1, t_dev + 1.4)))
    c = K(t, [(T_D, (130, 100, 0, 1.35)), (t_dev, (170, 130, 0, 1.55))])
    iso = I.Iso(float(c[0]), float(c[1]), float(c[2]), float(c[3]))
    PA.sol(lz, 1560, 200, 62, t, 0.0)
    PA.sierras(lz, t, 14 * (t - T_D), 0.0, y0=330, capas=3, semilla=137)
    TIE.suelo(lz, iso, t)
    m = TIE.objetos(t, u=u)
    m.dibujar(lz, iso)
    ky = U.pop(t, t_siete - 0.4) * U.salida(t, T_E - 0.2)
    if ky > 0.01:
        AB.contador_atras(lz, 360, 160, 1597, px=140, k=ky)
    kc = pk(t, t_ced - 0.1, 0.6) * U.salida(t, T_E - 0.2)
    if kc > 0.01:
        U.pergamino_grande(lz, 1560, 330, 520, 300, t, t_ced - 0.1, lineas=("Cédula real", "se devuelven las tierras"), titulo="Año de 1597", sello=True)
        MD.corona(lz, 1560, 130, 2.2 * kc, 1.0, t)
    k = U.pop(t, t_tierras) * U.salida(t, T_E - 0.2)
    if k > 0.01:
        sx, sy = iso.P(300, 120, 0)
        U.llamada(lz, float(sx) - 40, float(sy) - 80, "las tierras del pueblo", color=U.COL["teal"], px=50, k=k, cola="abajo")
    kq = U.pop(t, t_cap) * U.salida(t, T_E - 0.2)
    if kq > 0.01:
        U.llamada(lz, 520, 860, "un capitán se las había quedado", color=U.COL["rojo"], px=46, k=kq, cola=None)
    snd(t_ced, "sello", 0.45)
    snd(t_dev, "bling", 0.4)


# ------------------------------------------------------------------------------------------------ E. 1806: el primer alcalde y el archivo
@shot(T_E, bg=lambda t: bg_grad((90, 56, 86), (200, 140, 110), mid=(140, 90, 100), ym=0.6), post=[acabado], ent=("fundido", 0.6))
def e_archivo(lz, t):
    c = K(t, [(T_E, (130, 90, 40, 1.9)), (T_F, (140, 100, 40, 2.15))])
    iso = I.Iso(float(c[0]), float(c[1]), float(c[2]), float(c[3]))
    M5.archivo(lz, iso, t, legajos=float(smooth(prog(t, t_arch - 0.6, t_arch + 1.2))))
    # el alcalde en su escritorio
    G_.persona(lz, iso, 190, 150, t, tipo="regidor", dir=(0.0, 1.0), seed=61, h=60, accion="trabaja")
    yr = int(lerp(1597, 1806, e_inout(prog(t, T_E + 0.1, t_seis + 0.3))))
    k = U.pop(t, T_E + 0.1) * U.salida(t, T_F - 0.2)
    if k > 0.01:
        AB.contador_atras(lz, 340, 170, yr, px=150, k=k)
        U.llamada(lz, 340, 290, "más de 200 años después", color=U.COL["naranja"], px=44, k=U.pop(t, t_dosc) * U.salida(t, T_F - 0.2), cola=None)
    k = U.pop(t, t_alc) * U.salida(t, T_F - 0.2)
    if k > 0.01:
        sx, sy = iso.P(190, 150, 70)
        U.llamada(lz, float(sx), float(sy) - 60, "Joaquín Pérez Gavilán, primer alcalde", color=U.COL["morado"], px=44, k=k, cola="abajo")
    k = U.pop(t, t_arch) * U.salida(t, T_F - 0.2)
    if k > 0.01:
        sx, sy = iso.P(40, 30, 100)
        U.llamada(lz, float(sx) + 150, float(sy) - 20, "el archivo del pueblo", color=U.COL["teal"], px=46, k=k, cola=None)
    snd(t_alc, "pop", 0.3)
    snd(t_arch, "paginas", 0.4)


# ------------------------------------------------------------------------------------------------ F. papeles, no flechas
@shot(T_F, bg=lambda t: bg_grad((70, 40, 120), (250, 170, 110), mid=(160, 80, 130), ym=0.6), post=[acabado], ent=("fundido", 0.6))
def f_papeles(lz, t):
    U.bokeh(lz, t, seed=55, n=10, colores=((255, 200, 120), (255, 120, 140), (180, 140, 255)), alfa=0.3)
    lz.relleno(np.array([(-40, 880), (W + 40, 860), (W + 40, H + 20), (-40, H + 20)]), (74, 40, 80), capa=0)
    # a la izquierda, las flechas se rompen y se apagan
    kf = pk(t, T_F + 0.2, 0.6)
    for i in range(7):
        a = -1.2 + 0.18 * i
        x = 300 + 40 * math.cos(i * 1.7)
        fade = 1 - smooth(prog(t, t_flech, t_flech + 1.4))
        if kf > 0.01 and fade > 0.02:
            M5.flecha(lz, x + 46 * i, 980 - 10 * i, a, 560 * kf, alfa=fade, color=(150, 112, 80) if i % 2 else (176, 130, 90), g=1.5)
    # a la derecha, los papeles suben
    for i in range(8):
        k = pk(t, min(t_pap - 0.2, T_F + 0.5) + 0.15 * i, 0.5)
        if k > 0.01:
            x = 1300 + 170 * (i % 3) - 60
            y = 960 - 120 * (i // 3) * 1.0 - 30 * (i % 2)
            M5.papel(lz, x + 60, y - 30, 2.0 * k, rot=-0.14 + 0.1 * (i % 4), sello=(i % 2 == 0), capa=2)
    k = U.pop(t, t_def)
    if k > 0.01:
        U.llamada(lz, 960, 150, "defendió lo suyo", color=U.COL["oscuro"], px=64, k=k * U.salida(t, T1(E5) - 0.4), cola=None)
    k = U.pop(t, t_pap)
    if k > 0.01:
        U.llamada(lz, 1450, 330, "papeles", color=U.COL["teal"], px=70, k=k * U.repop(t, t_pap + 0.2), cola=None)
    k = U.pop(t, t_flech)
    if k > 0.01:
        U.llamada(lz, 480, 330, "no flechas", color=U.COL["rojo"], px=70, k=k, cola=None)
    snd(t_pap, "papel", 0.4)
    snd(t_flech, "dardo", 0.35)
