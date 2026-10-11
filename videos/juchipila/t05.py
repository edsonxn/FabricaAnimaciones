# -*- coding: utf-8 -*-
"""Escena 5 · la llegada (2:33-3:07): «todo cambió» (la flor se marchita), Nuño de Guzmán y su ejército cruzan el occidente, pueblos quemados y cautivos, Oñate toma la capital caxcana
y el reparto en encomienda (la Corona entrega pueblos; la gente paga tributo y trabaja)."""
import math

import numpy as np

import kz_ui as U
import kz_iso as I
import kz_iso_deco as DC
import kz_mapa as KM
import kz_mapa_dib as MD
import kz_abstracto as AB
import kz_pers2d as K2
import plano as P
import lugares  # noqa: F401
import paisajes as PA
import mapas as MA_
import mundos_a as MA
import mundos_c as MC
import mundos_f as MF
from motor import W, H, prog, lerp, smooth, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, h01, catmull
from reg import shot, snd
from util import *  # noqa: F401,F403
from t01 import acabado, paisaje

E5 = "llegada"
MP = KM.MAPA
CV = MC.CerroVentanas()
t_pero, t_alr, t_mil, t_quin, t_trein, t_todo, t_camb = (T(E5, "pero", frase=0), T(E5, "alrededor", frase=0), T(E5, "mil", frase=0), T(E5, "quinientos", frase=0), T(E5, "treinta", frase=0), T(E5, "todo", frase=0), T(E5, "cambio", frase=0))
t_nuno, t_guz, t_gob, t_fama, t_cruel, t_cruzo, t_occ, t_cientos, t_miles, t_alia = (T(E5, "nuno", frase=1), T(E5, "guzman", frase=1), T(E5, "gobernador", frase=1), T(E5, "fama", frase=1), T(E5, "cruel", frase=1), T(E5, "cruzo", frase=1),
                                                                                  T(E5, "occidente", frase=1), T(E5, "cientos", frase=1), T(E5, "miles", frase=1), T(E5, "aliados", frase=1))
t_dejo, t_queim, t_miles2, t_pers, t_escl = T(E5, "dejo", frase=2), T(E5, "quemados", frase=2), T(E5, "miles", frase=2), T(E5, "personas", frase=2), T(E5, "esclavizadas", frase=2)
t_uno, t_cap, t_cris, t_onate, t_llego, t_canon, t_derr, t_defens, t_capital = (T(E5, "uno", frase=3), T(E5, "capitanes", frase=3), T(E5, "cristobal", frase=3), T(E5, "onate", frase=3), T(E5, "llego", frase=3),
                                                                                T(E5, "canon", frase=3), T(E5, "derroto", frase=3), T(E5, "defensores", frase=3), T(E5, "capital", frase=3))
t_desp, t_vino, t_rep, t_esp2, t_rec, t_pueblos, t_enter, t_enc, t_corona, t_entreg, t_gente, t_pagara, t_trib, t_trab = (T(E5, "despues", frase=4), T(E5, "vino", frase=4), T(E5, "reparto", frase=4), T(E5, "espanoles", frase=4), T(E5, "recibieron", frase=4),
                                                                                                                         T(E5, "pueblos", frase=4), T(E5, "enteros", frase=4), T(E5, "encomienda", frase=4), T(E5, "corona", frase=4), T(E5, "entregaba", frase=4),
                                                                                                                         T(E5, "gente", frase=4), T(E5, "pagara", frase=4), T(E5, "tributo", frase=4), T(E5, "trabajara", frase=4))
T_A, T_B, T_C, T_D1, T_D2, T_E = T0(E5), INI(E5, 1) - 0.1, INI(E5, 2) - 0.1, INI(E5, 3) - 0.1, t_derr - 0.5, INI(E5, 4) - 0.1
RUTA_NUNO = ["mexico", "patzcuaro", "guadalajara", "compostela", "culiacan"]


# ------------------------------------------------------------------------------------------------ A. todo cambió
def amb_a(t):
    return float(smooth(prog(t, t_todo - 0.2, t_camb + 0.5)))


@shot(T_A, bg=lambda t: PA.cielo(round(amb_a(t), 1)), post=[acabado], ent=("fundido", 0.5))
def a_cambio(lz, t):
    amb = amb_a(t)
    paisaje(lz, t, 24.0 * (t - T_A), amb)
    # el año
    c = lerp(1500, 1530, e_inout(prog(t, t_mil, t_trein + 0.2)))
    kc = U.pop(t, t_alr)
    if kc > 0.01:
        lz.texto(str(int(c)), W / 2, 210, 190, "geo_x", color=(255, 255, 255), borde=None, k=kc, alfa=1.0, capa=2, temblor=0.0)
        U.llamada(lz, W / 2, 330, "hacia 1530", color=U.COL["naranja"], px=44, k=kc, cola="arriba") if kc > 0.5 else None
    # la flor del hook, que se marchita al decir «todo cambió»
    marchit = e_inout(prog(t, t_todo, t_camb + 0.9))
    k = pk(t, t_pero, 0.6) * (1 - smooth(prog(t, t_camb + 0.8, t_camb + 1.2)))
    if k > 0.01:
        MA.flor_xuchitl(lz, W / 2, 650, 170 * k, t, u=1.0 - 0.75 * marchit, seed=2, alfa=1.0 - 0.3 * marchit)
    AB.petalos(lz, t, t_camb, (W / 2, 650), n=22, dur=2.6, spread=(-math.pi * 1.0, math.pi * 0.2), seed=31, tam=(18, 34), vel=(140, 380), g=60.0)
    snd(t_camb, "trueno", 0.5)


# ------------------------------------------------------------------------------------------------ B. Nuño de Guzmán cruza el occidente
def cam_b(t):
    return Klog(t, [(T_B, (-101.4, 20.9, 1.15)), (t_cientos, (-102.6, 21.1, 1.35)), (T_C, (-103.1, 21.5, 1.5))])


@shot(T_B, bg=lambda t: MP.base(cam_b(t), t, exag=12.0, rios_umbral=0.7), post=[acabado], ent=("tinta", 0.6))
def b_nuno(lz, t):
    cam = cam_b(t)
    MD.mar_vivo(lz, cam, t, seed=2)
    MD.montes(lz, cam)
    f = prog(t, t_nuno + 0.3, t_occ + 2.3)
    cab = MA_.ruta_gruesa(lz, cam, RUTA_NUNO, frac=e_inout(f), t=t, color=(222, 60, 70), ancho=11, dash=True, flecha=False)
    for lug, t0, nom in (("mexico", T_B, "México"), ("guadalajara", t_cruzo + 0.4, "Guadalajara"), ("culiacan", t_occ + 1.5, "Culiacán")):
        MD.ciudad(lz, cam, lug, t, t0, tam=0.8, tipo="ciudad", nombre=nom, px=24, semilla=3)
    if cab is not None:
        MD.ejercito(lz, cab[0], cab[1], 24, bando=(222, 60, 70), t=t, s=1.3, dir=1, marcha=True, bandera=True, semilla=3)
    kb = pk(t, t_nuno, 0.5)
    if kb > 0.01:
        lz.relleno(circulo(300, 760, 270 * kb, 48), (30, 12, 60), alfa=0.55, capa=1)
        with lz.recorte(circulo(300, 760, 270 * kb, 48)):
            K2.busto(lz, 300, 960, 140 * kb, "capitan", t, yaw=0.45, emocion="enojo" if t > t_fama else "serio", ojos="abiertos", seed=9, habla=0.6 if t_nuno < t < t_cruel + 0.5 else 0.0)
        U.llamada(lz, 300, 1030, "Nuño de Guzmán", color=U.COL["rojo"], px=48, k=kb, cola=None)
    k = U.pop(t, t_gob) * U.salida(t, t_cruzo - 0.1, 0.25)
    if k > 0.01:
        U.llamada(lz, W / 2 + 200, 150, "gobernador español de fama cruel", color=U.COL["rojo"], px=60, k=k * U.repop(t, t_cruel + 0.2), cola=None)
    k = U.pop(t, t_cruzo) * U.salida(t, t_cientos - 0.1, 0.25)
    if k > 0.01:
        U.llamada(lz, W / 2 + 200, 150, "cruzó el occidente de México", color=U.COL["naranja"], px=60, k=k, cola=None)
    k = U.pop(t, t_cientos)
    if k > 0.01:
        U.llamada(lz, W - 520, 880, "cientos de soldados", color=U.COL["azul"], px=48, k=k, cola=None)
        for i in range(10):
            K2.cuerpo(lz, W - 760 + 52 * i, 1010, 14, "soldado", t, piernas="camina", brazos="balanceo", mirar=-1, vista="perfil", seed=i, cara="ninguna", sombra=False, ph=t * 5 + i)
    k = U.pop(t, t_miles)
    if k > 0.01:
        U.llamada(lz, W - 520, 770, "miles de aliados indígenas", color=U.COL["magenta"], px=48, k=k, cola=None)
        for i in range(22):
            K2.cuerpo(lz, W - 760 + 24 * i, 750 + 0, 8, "caxcan", t, piernas="camina", brazos="balanceo", mirar=-1, vista="perfil", seed=i + 40, cara="ninguna", sombra=False, ph=t * 5 + i * 0.4)
    snd(t_nuno, "gong", 0.4)


# ------------------------------------------------------------------------------------------------ C. pueblos quemados y cautivos
def cam_c(t):
    return Klog(t, [(T_C, (-103.1, 21.55, 2.4)), (T1(E5) - 6.5, (-103.05, 21.5, 2.7))])


PUEBLOS_Q = [("juchipila", "Juchipila"), ("apozol", "Apozol"), ("nochistlan", "Nochistlán"), ("jalpa", "Jalpa"), ("tlaltenango", "Tlaltenango"), ("teul", "Teúl"), ("moyahua", "Moyahua")]


@shot(T_C, bg=lambda t: MP.base(cam_c(t), t, exag=12.0, rios_umbral=0.7), post=[acabado, lambda img, t: U.gradacion(img, luces=(0.9, 0.86, 0.9), sombras=(0.9, 0.9, 1.0), contraste=1.05, saturacion=0.8)], ent=("tinta", 0.6))
def c_quemados(lz, t):
    cam = cam_c(t)
    MD.montes(lz, cam)
    for i, (lug, nom) in enumerate(PUEBLOS_Q):
        MD.ciudad(lz, cam, lug, t, t_dejo + 0.2 * i, tam=0.9, tipo="pueblo", nombre=nom if t < t_queim else None, px=24, llama=(t > t_queim + 0.15 * i), semilla=i + 2)
    k = U.pop(t, t_dejo) * U.salida(t, t_miles2 - 0.1, 0.25)
    if k > 0.01:
        U.llamada(lz, W / 2, 140, "pueblos quemados", color=U.COL["rojo"], px=70, k=k * U.repop(t, t_queim + 0.2), cola=None)
    # franja oscura inferior con la fila de cautivos
    a = smooth(prog(t, t_miles2 - 0.2, t_miles2 + 0.5))
    if a > 0.01:
        lz.relleno(np.array([(0, 700), (W, 640), (W, H), (0, H)]), (24, 10, 52), alfa=0.80 * a, capa=2)
        MF.fila_encadenada(lz, t, t_miles2 - 0.2, y=1010, n=9, s=36, x_ini=-250, vel=110, alfa=a)
        k = U.pop(t, t_pers)
        U.llamada(lz, W / 2, 780, "miles de personas esclavizadas", color=U.COL["morado"], px=62, k=k, cola=None) if k > 0.01 else None
    snd(t_queim, "crujido", 0.5)


# ------------------------------------------------------------------------------------------------ D1. Oñate llega al cañón
def cam_d1(t):
    return Klog(t, [(T_D1, (-103.1, 21.2, 2.2)), (T_D2, (-103.1, 21.4, 2.8))])


@shot(T_D1, bg=lambda t: MP.base(cam_d1(t), t, exag=12.0, rios_umbral=0.7), post=[acabado], ent=("tinta", 0.6))
def d1_onate(lz, t):
    cam = cam_d1(t)
    MD.montes(lz, cam)
    f = prog(t, t_llego - 0.2, t_llego + 1.4)
    cab = MA_.ruta_gruesa(lz, cam, ["guadalajara", (-103.25, 20.95), "las_ventanas"], frac=e_inout(f), t=t, color=(222, 60, 70), ancho=11, dash=True, flecha=False)
    MD.ciudad(lz, cam, "guadalajara", t, T_D1, tam=0.8, tipo="ciudad", nombre="Guadalajara", px=24, semilla=3)
    MD.ciudad(lz, cam, "las_ventanas", t, t_llego, tam=1.2, tipo="fuerte", nombre="capital caxcana", px=26, semilla=2)
    if cab is not None:
        MD.ejercito(lz, cab[0], cab[1], 16, bando=(222, 60, 70), t=t, s=1.3, dir=1, marcha=True, bandera=True, semilla=5)
    kb = pk(t, t_uno, 0.5)
    if kb > 0.01:
        lz.relleno(circulo(1560, 740, 270 * kb, 48), (30, 12, 60), alfa=0.55, capa=1)
        with lz.recorte(circulo(1560, 740, 270 * kb, 48)):
            K2.busto(lz, 1560, 940, 140 * kb, "capitan", t, yaw=-0.45, emocion="serio", ojos="abiertos", seed=13, habla=0.6 if t_cris < t < t_onate + 0.8 else 0.0)
        U.llamada(lz, 1560, 1010, "Cristóbal de Oñate", color=U.COL["rojo"], px=48, k=kb, cola=None)
    k = U.pop(t, t_uno) * U.salida(t, t_llego - 0.1, 0.25)
    if k > 0.01:
        U.llamada(lz, 760, 150, "uno de sus capitanes", color=U.COL["morado"], px=60, k=k, cola=None)
    k = U.pop(t, t_llego)
    if k > 0.01:
        U.llamada(lz, 760, 150, "llegó al cañón", color=U.COL["naranja"], px=64, k=k, cola=None)
    MD.escala(lz, 80, H - 70, cam, km=50)


# ------------------------------------------------------------------------------------------------ D2. asalto a la capital caxcana
def cam_d2(t):
    return K(t, [(T_D2, (60, 280, 70, 1.35)), (t_defens, (70, 160, 100, 1.55)), (T_E, (70, 90, 130, 1.65))])


@shot(T_D2, bg=lambda t: PA.cielo(0.35), post=[acabado], ent=("tinta", 0.6))
def d2_asalto(lz, t):
    cx, cy, cz, zm = cam_d2(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    a = float(smooth(prog(t, T_D2 + 0.3, t_defens + 1.0)))
    I.luz(mul=(1.0 - 0.18 * a, 1.0 - 0.22 * a, 1.0 - 0.10 * a), mix=(160, 60, 80), k=0.18 * a)
    PA.sol(lz, 1600, 240, 62, t, 0.4)
    PA.sierras(lz, t, cx * 0.4, 0.4, y0=470, capas=4, semilla=17)
    CV.suelo(lz, iso, t)
    CV.objetos(t, 1.0, 25, a).dibujar(lz, iso)
    DC.aves(lz, t, n=6, seed=3)
    I.luz()
    k = U.pop(t, t_derr) * U.salida(t, t_capital - 0.1, 0.25)
    if k > 0.01:
        U.llamada(lz, 450, 160, "derrotó a los defensores", color=U.COL["rojo"], px=58, k=k, cola=None)
    k = U.pop(t, t_capital)
    if k > 0.01:
        U.llamada(lz, 450, 160, "de la capital caxcana", color=U.COL["naranja"], px=58, k=k, cola=None)
    snd(t_derr, "canonazo", 0.5)


# ------------------------------------------------------------------------------------------------ E. el reparto: encomienda
@shot(T_E, bg=lambda t: bg_grad((64, 28, 110), (18, 8, 46), mid=(46, 20, 90), ym=0.55), post=[acabado], ent=("tinta", 0.6))
def e_encomienda(lz, t):
    U.bokeh(lz, t, seed=21, n=10, colores=((255, 190, 60), (236, 70, 140), (122, 90, 255)), alfa=0.30)
    MF.reparto(lz, t, T_E + 0.05, t_rep, t_esp2 - 0.1)
    MF.diagrama_encomienda(lz, t, t_corona - 0.2, t_pueblos, t_esp2, t_gente, t_pagara, t_trib, t_trab)
    k = U.pop(t, t_vino) * U.salida(t, t_esp2 - 0.1, 0.25)
    if k > 0.01:
        U.llamada(lz, 330, 200, "el reparto", color=U.COL["naranja"], px=72, k=k, cola=None)
    k = U.pop(t, t_enc)
    if k > 0.01:
        U.llamada(lz, 330, 200, "encomienda", color=U.COL["magenta"], px=76, k=k * U.repop(t, t_enc + 0.8), cola=None)
    k = U.pop(t, t_corona) * U.salida(t, t_gente - 0.1, 0.25)
    if k > 0.01:
        U.llamada(lz, 1560, 200, "la Corona", color=U.COL["oro"], px=64, k=k, cola=None, color_texto=(60, 36, 20))
    k = U.pop(t, t_trib)
    if k > 0.01:
        U.llamada(lz, 480, 640, "tributo", color=U.COL["oro"], px=60, k=k, cola=None, color_texto=(60, 36, 20))
    k = U.pop(t, t_trab)
    if k > 0.01:
        U.llamada(lz, 1440, 640, "trabajo", color=U.COL["naranja"], px=60, k=k, cola=None)
    snd(t_corona, "bling", 0.4)
