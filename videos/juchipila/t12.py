# -*- coding: utf-8 -*-
"""Escena 12 · la Revolución (7:07-7:47): cuatro siglos después; en 1909 el comerciante Crispín Robles funda en su tienda «El Nuevo Mundo» un
club antirreeleccionista para apoyar a Madero (retrato real); lo arrestan por sedición y va a Lecumberri; asesinado Madero (22 feb 1913),
Robles se alza el 15 de abril de 1913; coronel de caballería con Pánfilo Natera (retrato real); muere en Ocotlán, Jalisco, en marzo de 1914;
tres meses después Villa y Natera (retratos reales) toman Zacatecas."""
import math

import numpy as np

import kz_ui as U
import kz_mapa as KM
import kz_mapa_dib as MD
import kz_abstracto as AB
import kz_pers2d as K2
import kz_retrato as RT
import plano as P
import lugares  # noqa: F401
import paisajes as PA
import mapas as MA_
import mundos_d as MD_
import mundos_h as MH
import mundos_m as MM
from motor import W, H, prog, lerp, smooth, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, h01, catmull
from reg import shot, snd
from util import *  # noqa: F401,F403
from t01 import acabado

E12 = "revolucion"
MP = KM.MAPA
t_cuatro, t_siglos, t_volvio, t_levantarse = T(E12, "cuatro", frase=0), T(E12, "siglos", frase=0), T(E12, "volvio", frase=0), T(E12, "levantarse", frase=0)
t_mil, t_comerc, t_crispin, t_robles, t_fundo, t_club, t_antirr, t_apoyar, t_madero = (T(E12, "mil", frase=1), T(E12, "comerciante", frase=1), T(E12, "crispin", frase=1),
                                                                                     T(E12, "robles", frase=1), T(E12, "fundo", frase=1), T(E12, "club", frase=1),
                                                                                     T(E12, "antirreeleccionista", frase=1), T(E12, "apoyar", frase=1), T(E12, "madero", frase=1))
t_dias, t_revol, t_arrest, t_sedicion, t_penit, t_ciudad = (T(E12, "dias", frase=2), T(E12, "revolucion", frase=2), T(E12, "arrestaron", frase=2), T(E12, "sedicion", frase=2),
                                                            T(E12, "penitenciaria", frase=2), T(E12, "ciudad", frase=2))
t_asesin, t_madero2, t_quince, t_abril, t_robles2, t_armas = (T(E12, "asesinaron", frase=3), T(E12, "madero", frase=3), T(E12, "quince", frase=3), T(E12, "abril", frase=3),
                                                              T(E12, "robles", frase=3), T(E12, "armas", frase=3))
t_coronel, t_caball, t_brigada, t_general, t_panfilo = T(E12, "coronel", frase=4), T(E12, "caballeria", frase=4), T(E12, "brigada", frase=4), T(E12, "general", frase=4), T(E12, "panfilo", frase=4)
t_murio, t_combate, t_marzo, t_ocotlan, t_tres, t_villa, t_natera2, t_zacatecas = (T(E12, "murio", frase=5), T(E12, "combate", frase=5), T(E12, "marzo", frase=5), T(E12, "ocotlan", frase=5),
                                                                                   T(E12, "tres", frase=5), T(E12, "villa", frase=5), T(E12, "natera", frase=5), T(E12, "zacatecas", frase=5))
T_A, T_B, T_C, T_D, T_E, T_F1, T_F2 = T0(E12), INI(E12, 1) - 0.15, INI(E12, 2) - 0.15, INI(E12, 3) - 0.15, INI(E12, 4) - 0.15, INI(E12, 5) - 0.15, t_tres - 0.25


def SEPIA(img, t):
    """Toque de 1910: luces cálidas, algo menos de saturación."""
    return acabado(U.gradacion(img, luces=(1.04, 0.98, 0.88), sombras=(0.98, 0.94, 0.9), contraste=1.03, saturacion=0.88), t)


# ------------------------------------------------------------------------------------------------ A-B. 1909: la tienda «El Nuevo Mundo» y el club antirreeleccionista
def cam_ab(t):
    return K(t, [(T_A, (0.0, 1.0)), (T_B + 0.4, (0.0, 1.0)), (t_club, (60.0, 1.18)), (T_C, (90.0, 1.25))])


@shot(T_A, bg=lambda t: PA.cielo(0.1), post=[SEPIA], ent=("tinta", 0.6))
def a_calle(lz, t):
    cx, z = cam_ab(t)
    with lz.grupo(960 * (1 - z), 760 * (1 - z), z):
        MM.calle_1909(lz, t, cx=cx)
        MM.manta_club(lz, 960 - cx * 0.6, 300, pk(t, t_club - 0.1, 0.5), t)
        # vecinos que se juntan a escuchar
        for i in range(9):
            x = 480 + 120 * i - cx * 0.6 + (40 * math.sin(t * 0.6 + i) if t < t_fundo else 0)
            if abs(x - 960) < 120:
                continue
            K2.cuerpo(lz, x, 980 + 16 * (i % 2), 30, MM.VECINO(2100 + i), t, piernas="idle" if t > T_B else "camina", brazos="arriba" if (t > t_madero and i % 3 == 0) else "idle",
                      mirar=1 if x < 960 else -1, vista="perfil", seed=2100 + i, emocion="alegre" if t > t_madero else "neutro", ph=t * 4 + i)
        if t > T_B - 0.2:
            K2.cuerpo(lz, 960 - cx * 0.6 + 40, 990, 36, MM.ROBLES, t, piernas="idle", brazos="señala" if t_fundo < t < t_apoyar else ("arriba" if t > t_madero else "idle"),
                      mirar=-1, vista="tres", seed=2150, emocion="alegre", objetivo=(700, 300))
    # Madero en un cartel de la pared (retrato real)
    km = pk(t, t_madero - 0.2, 0.5)
    if km > 0.01:
        RT.retrato(lz, 1600, 760, 120 * (0.9 + 0.1 * km), "madero", t, emocion="serio", alfa=min(1.0, km * 1.3), seed=2)
        U.llamada(lz, 1600, 230, "Francisco I. Madero", color=U.COL["azul"], px=38, k=U.pop(t, t_madero), cola=None)
    c = int(lerp(1556, 1909, e_inout(prog(t, t_cuatro - 0.1, t_mil + 0.3))))
    k = U.pop(t, t_cuatro - 0.1) * U.salida(t, t_crispin - 0.1)
    if k > 0.01:
        AB.contador_atras(lz, W / 2, 190, c, px=150, k=k)
    k = U.pop(t, t_levantarse) * U.salida(t, t_mil - 0.1)
    if k > 0.01:
        U.llamada(lz, W / 2, 310, "volvió a levantarse", color=U.COL["rojo"], px=48, k=k, cola=None)
    k = U.pop(t, t_crispin)
    if k > 0.01:
        U.llamada(lz, 330, 100, "Crispín Robles", color=U.COL["naranja"], px=60, k=k, cola=None)
        U.llamada(lz, 330, 185, "comerciante · 1909", color=U.COL["oscuro"], px=36, k=k, cola=None)
    snd(t_cuatro, "reloj_rapido", 0.35)
    snd(t_club, "pop", 0.4)
    snd(t_madero, "campana", 0.35)


# ------------------------------------------------------------------------------------------------ C. arrestado por sedición: Lecumberri
@shot(T_C, bg=lambda t: bg_grad((84, 76, 90), (30, 26, 40), mid=(56, 50, 66), ym=0.55), post=[SEPIA], ent=("tinta", 0.6))
def c_carcel(lz, t):
    a0 = 1.0 - smooth(prog(t, t_penit - 0.2, t_penit + 0.3))
    if a0 > 0.01:                                                        # la calle del pueblo, de noche, donde lo detienen
        MM.calle_1909(lz, t, cx=40.0, noche=1.0)
        lz.relleno(rect_red(0, 0, W, H, 0), (20, 16, 50), alfa=0.55 * a0, capa=0)
    U.bokeh(lz, t, seed=141, n=8, colores=((170, 160, 190), (120, 110, 150)), alfa=0.22)
    k = U.pop(t, t_revol - 0.1) * U.salida(t, t_arrest + 0.4)
    if k > 0.01:
        U.llamada(lz, W / 2, 150, "noviembre de 1910: empieza la Revolución", color=U.COL["rojo"], px=48, k=k, cola=None)
    # el arresto: dos rurales flanquean a Robles
    a = 1.0 - smooth(prog(t, t_penit - 0.2, t_penit + 0.3))
    if a > 0.01:
        K2.cuerpo(lz, 760, 980, 40, MM.RURAL, t, piernas="idle", brazos="defensa", mirar=1, vista="perfil", seed=2201, emocion="enojo", alfa=a)
        K2.cuerpo(lz, 960, 990, 42, MM.ROBLES, t, piernas="idle", brazos="pecho", mirar=-1, vista="perfil", seed=2150, emocion="serio", alfa=a)
        K2.cuerpo(lz, 1160, 980, 40, MM.RURAL, t, piernas="idle", brazos="defensa", mirar=-1, vista="perfil", seed=2202, emocion="enojo", alfa=a)
        k = U.pop(t, t_sedicion)
        if k > 0.01:
            U.llamada(lz, 960, 330, "acusado de sedición", color=U.COL["oscuro"], px=50, k=k * a, cola=None)
    b = smooth(prog(t, t_penit - 0.2, t_penit + 0.4))
    if b > 0.01:
        MM.lecumberri(lz, 520, 560, 300, t, k=e_back(prog(t, t_penit - 0.2, t_penit + 0.4)))
        U.llamada(lz, 520, 960, "Lecumberri, Ciudad de México", color=U.COL["morado"], px=38, k=U.pop(t, t_penit), cola=None)
        lz.relleno(rect_red(1100, 260, 640, 620, 20), (60, 50, 70), alfa=b, capa=1)
        K2.cuerpo(lz, 1420, 820, 34, MM.ROBLES, t, piernas="sentado", brazos="idle", mirar=-1, vista="perfil", seed=2150, emocion="triste", alfa=b)
        MM.barrotes(lz, 1110, 270, 1730, 870, n=8)
    snd(t_arrest, "bonk", 0.45)
    snd(t_penit, "crujido", 0.35)


# ------------------------------------------------------------------------------------------------ D. asesinan a Madero (22 feb 1913); Robles se alza (15 abr 1913)
@shot(T_D, bg=lambda t: bg_grad((90, 40, 50), (30, 12, 24), mid=(60, 24, 40), ym=0.55), post=[SEPIA], ent=("tinta", 0.6))
def d_alzamiento(lz, t):
    U.bokeh(lz, t, seed=151, n=8, colores=((236, 90, 90), (255, 170, 90)), alfa=0.25)
    RT.retrato(lz, 420, 900, 150, "madero", t, emocion="serio", seed=2)
    c = smooth(prog(t, t_asesin, t_asesin + 0.5))
    if c > 0.01:
        lz.relleno(np.array([(520, 340), (590, 340), (610, 340 + 160 * c), (610, 420 + 160 * c)]), (16, 12, 24), alfa=0.95, capa=2)
    k = U.pop(t, t_asesin)
    if k > 0.01:
        U.llamada(lz, 420, 200, "Madero, asesinado · 22 feb 1913", color=U.COL["oscuro"], px=38, k=k, cola=None)
    kc = pk(t, t_quince - 0.15, 0.45)
    if kc > 0.01:
        MD_.calendario(lz, 1060, 420, 0.9 * kc, t, dia="15", mes="ABRIL", anio="1913")
    ka = pk(t, t_robles2 - 0.2, 0.5)
    if ka > 0.01:
        for i, dx in enumerate((-170, 170)):
            K2.cuerpo(lz, 1560 + dx, 1000, 30, dict(MM.VECINO(2300 + i), torso="bandolera", tocado="sombrero_palma"), t, piernas="idle", brazos="arriba" if t > t_armas else "idle",
                      mirar=-1 if dx > 0 else 1, vista="perfil", seed=2300 + i, emocion="enojo", alfa=min(1.0, ka * 1.4))
        K2.cuerpo(lz, 1560, 1010, 38, MM.ROBLES_REV, t, piernas="idle", brazos="arriba" if t > t_armas - 0.1 else "pecho", mirar=-1, vista="frente", seed=2150, emocion="enojo",
                  alfa=min(1.0, ka * 1.4))
        U.llamada(lz, 1560, 330, "Robles se levanta en armas", color=U.COL["rojo"], px=44, k=U.pop(t, t_armas - 0.1), cola=None)
    snd(t_asesin, "gong", 0.45)
    snd(t_armas, "tambor", 0.5)


# ------------------------------------------------------------------------------------------------ E. coronel de caballería con Pánfilo Natera
@shot(T_E, bg=lambda t: PA.cielo(0.35), post=[SEPIA], ent=("tinta", 0.6))
def e_caballeria(lz, t):
    cx = 420.0 * (t - T_E)
    PA.sol(lz, 300, 220, 60, t, 0.35)
    PA.sierras(lz, t, cx * 0.4, 0.35, y0=620, capas=4, semilla=161)
    p = PA.pal(0.35)
    degradado_v(lz, 0, W, 760, H, p["pasto"][0], p["pasto"][1], 760, H)
    for k in range(8):                                                   # nopales y magueyes que pasan rápido
        x = ((k * 330 - cx * 1.2) % (W + 400)) - 200
        lz.relleno(elipse(x, 800, 26, 40, 0, 16), (90, 150, 100), capa=1)
        lz.relleno(elipse(x - 22, 752, 18, 28, -0.3, 14), (100, 160, 110), capa=1)
    for i in range(6):                                                   # la caballería al galope (Robles al frente)
        x = 1350 - 230 * i + 30 * math.sin(t * 2 + i)
        y = 930 + 30 * (i % 2)
        MH.caballo2d(lz, x, y, 15 if i else 17, t, ph=t * 12 + i * 1.3, galope=1.0, color=((120, 76, 52), (60, 44, 40), (170, 120, 80), (226, 220, 210), (90, 60, 50), (140, 100, 70))[i],
                     jinete=MM.ROBLES_REV if i == 0 else dict(MM.VECINO(2400 + i), torso="bandolera", tocado="sombrero_palma"), jinete_seed=2400 + i)
        MH.polvo2d(lz, x - 120, y, t, t - ((t * 0.9 + i * 0.3) % 1.2), dur=1.2, n=6, s=0.7, seed=i)
    k = U.pop(t, t_coronel)
    if k > 0.01:
        U.llamada(lz, 1350, 620, "coronel Robles", color=U.COL["naranja"], px=44, k=k, cola="abajo")
    kn = pk(t, t_general - 0.2, 0.5)
    if kn > 0.01:
        MD.medallon(lz, 300, 300, 150, "natera", t, k=kn)
        U.llamada(lz, 300, 490, "gral. Pánfilo Natera", color=U.COL["rojo"], px=38, k=U.pop(t, t_panfilo), cola=None)
    k = U.pop(t, t_caball)
    if k > 0.01:
        U.llamada(lz, 1200, 150, "caballería", color=U.COL["oscuro"], px=56, k=k, cola=None)
    snd(t_caball, "galope", 0.55)


# ------------------------------------------------------------------------------------------------ F1. muere en combate: Ocotlán, Jalisco, marzo de 1914
def cam_f(t):
    return Klog(t, [(T_F1, (-102.9, 20.5, 2.4)), (T_F2, (-102.7, 21.2, 2.0)), (T1(E12), (-102.6, 22.2, 2.4))])


@shot(T_F1, bg=lambda t: MP.base(cam_f(t), t, exag=12.0, rios_umbral=0.7), post=[SEPIA], ent=("tinta", 0.6))
def f_final(lz, t):
    cam = cam_f(t)
    MD.montes(lz, cam)
    MD.ciudad(lz, cam, "ocotlan", t, T_F1 + 0.1, tam=0.9, tipo="pueblo", nombre="Ocotlán", px=24, semilla=6)
    MD.ciudad(lz, cam, "guadalajara", t, T_F1 + 0.2, tam=0.9, tipo="ciudad", nombre="Guadalajara", px=24, semilla=3)
    MD.ciudad(lz, cam, "juchipila", t, T_F1 + 0.3, tam=0.9, tipo="pueblo", nombre="Juchipila", px=24, semilla=2)
    MD.ciudad(lz, cam, "zacatecas", t, T_F1 + 0.4, tam=1.2, tipo="ciudad", nombre=None, px=26, semilla=4)
    MD.insignia_batalla(lz, cam, "ocotlan", t, t_combate, año=None, s=1.1)
    if t < T_F2 + 0.4:
        U.fecha_lugar(lz, t, t_marzo - 0.1, T_F2 + 0.2, "Ocotlán, Jalisco", "marzo de 1914")
        kr = pk(t, t_murio - 0.2, 0.5) * (1 - smooth(prog(t, T_F2, T_F2 + 0.4)))
        if kr > 0.01:
            lz.relleno(circulo(1560, 640, 210 * kr, 48), (60, 40, 50), alfa=0.85, capa=1)
            lz.trazo(circulo(1560, 640, 210 * kr, 48), (250, 206, 90), 9.0, cerrado=True, temblor=0.0, capa=2)
            with lz.recorte(circulo(1560, 640, 205 * kr, 48)):
                K2.busto(lz, 1560, 800, 100 * kr, MM.ROBLES_REV, t, yaw=-0.35, emocion="serio", ojos="cerrados", seed=2150)
            lz.relleno(np.array([(1660, 450), (1720, 470), (1700, 620), (1650, 600)]), (16, 12, 24), alfa=0.95 * kr, capa=2)
            U.llamada(lz, 1560, 900, "Crispín Robles, muere en combate", color=U.COL["oscuro"], px=36, k=kr, cola=None)
    else:
        # tres meses después: Villa y Natera toman Zacatecas
        zx, zy = MA_.proy(cam, "zacatecas")
        for j, (a, col) in enumerate(((-2.6, (226, 70, 70)), (-1.9, (240, 150, 50)), (-0.9, (226, 70, 70)), (-0.2, (240, 150, 50)))):
            f = e_inout(prog(t, t_villa - 0.2 + 0.12 * j, t_zacatecas + 0.6))
            r0 = 420
            x0, y0 = zx + math.cos(a) * r0, zy - math.sin(a) * r0 * 0.7
            if f > 0.01:
                MA_.flecha_pantalla(lz, x0, y0, x0 + (zx - x0) * f * 0.85, y0 + (zy - y0) * f * 0.85, color=col, ancho=24, alfa=1.0)
        for j, (quien, x, t0) in enumerate((("villa", 300, t_villa), ("natera", 1620, t_natera2))):
            km = pk(t, t0 - 0.2, 0.5)
            if km > 0.01:
                MD.medallon(lz, x, 330, 150, quien, t, k=km)
                U.llamada(lz, x, 520, ("Francisco Villa", "Pánfilo Natera")[j], color=U.COL["rojo"], px=38, k=km, cola=None)
        k = U.pop(t, t_zacatecas)
        if k > 0.01:
            U.llamada(lz, zx, zy + 110, "Toma de Zacatecas · 23 jun 1914", color=U.COL["naranja"], px=40, k=k, cola=None)
        k = U.pop(t, t_tres - 0.1)
        if k > 0.01:
            U.llamada(lz, W / 2, 140, "tres meses después", color=U.COL["oscuro"], px=50, k=k, cola=None)
    MD.escala(lz, 80, H - 70, cam, km=50)
    snd(t_combate, "canonazo", 0.45)
    snd(t_zacatecas, "tambor", 0.5)
