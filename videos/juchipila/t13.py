# -*- coding: utf-8 -*-
"""Escena 13 · el cierre (7:47-8:18): Juchipila hoy (12 251 habitantes, censo 2020), la migración a Estados Unidos y las remesas, junio lleno
de flores como hace mil años, los tastoanes en las fiestas de Santiago, el título final y la pregunta a quien mira."""
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
import mundos_e as ME
import mundos_n as MN
from motor import W, H, prog, lerp, smooth, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, h01, catmull
from reg import shot, snd
from util import *  # noqa: F401,F403
from t01 import acabado

E13 = "cierre"
MP = KM.MAPA
JH = MN.JuchipilaHoy()
for k_, v_ in {"los_angeles": (-118.24, 34.05), "chicago": (-87.63, 41.88), "dallas": (-96.80, 32.78)}.items():
    MD.CIUDADES.setdefault(k_, v_)
t_hoy, t_doce, t_habit, t_hijos, t_ido, t_eeuu, t_dinero, t_mandan, t_sostiene = (T(E13, "hoy", frase=0), T(E13, "doce", frase=0), T(E13, "habitantes", frase=0), T(E13, "hijos", frase=0),
                                                                                T(E13, "ido", frase=0), T(E13, "estados", frase=0), T(E13, "dinero", frase=0), T(E13, "mandan", frase=0),
                                                                                T(E13, "sostiene", frase=0))
t_junio, t_flores, t_mil, t_julio, t_santiago, t_tastoanes, t_recuerdan, t_invasores = (T(E13, "junio", frase=1), T(E13, "flores", frase=1), T(E13, "mil", frase=1), T(E13, "julio", frase=1),
                                                                                       T(E13, "santiago", frase=1), T(E13, "tastoanes", frase=1), T(E13, "recuerdan", frase=1),
                                                                                       T(E13, "invasores", frase=1))
t_juch, t_nobles, t_hermoso, t_sobrevivio, t_guerra = T(E13, "juchipila", frase=2), T(E13, "nobles", frase=2), T(E13, "hermoso", frase=2), T(E13, "sobrevivio", frase=2), T(E13, "guerra", frase=2)
t_que, t_otro, t_contemos, t_comentarios = T(E13, "que", frase=3), T(E13, "otro", frase=3), T(E13, "contemos", frase=3), T(E13, "comentarios", frase=3)
T_A, T_B, T_C, T_D, T_E, T_F = T0(E13), t_hijos - 0.3, INI(E13, 1) - 0.15, t_julio - 0.25, INI(E13, 2) - 0.15, INI(E13, 3) - 0.15


# ------------------------------------------------------------------------------------------------ A. Juchipila hoy: 12 251 habitantes
def cam_a(t):
    return K(t, [(T_A, (200, 0, 30, 1.25)), (T_B, (190, 30, 20, 1.05))])


@shot(T_A, bg=lambda t: PA.cielo(0.0), post=[acabado], ent=("tinta", 0.6))
def a_hoy(lz, t):
    cx, cy, cz, zm = cam_a(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    PA.sol(lz, 1600, 220, 60, t, 0.0)
    PA.sierras(lz, t, 15 * (t - T_A), 0.0, y0=440, capas=4, semilla=131)
    DC.aves(lz, t, n=7, seed=13)
    JH.suelo(lz, iso, t)
    JH.objetos_hoy(t).dibujar(lz, iso)
    c = int(lerp(0, 12251, e_out(prog(t, t_doce - 0.1, t_habit + 0.6))))
    k = U.pop(t, t_hoy - 0.1)
    if k > 0.01:
        U.llamada(lz, 330, 140, "hoy", color=U.COL["naranja"], px=56, k=k, cola=None)
    k = U.pop(t, t_doce - 0.1)
    if k > 0.01:
        lz.texto(f"{c:,}".replace(",", " "), 1500, 170, 130, "geo_x", color=(255, 255, 255), borde=None, k=k, alfa=1.0, capa=2, temblor=0.0)
        U.llamada(lz, 1500, 270, "habitantes (censo 2020)", color=U.COL["teal"], px=36, k=k, cola=None)
        U._registrar(lz, 1500, 210, 520, 200)
    snd(t_doce, "pop", 0.4)


# ------------------------------------------------------------------------------------------------ B. se van a Estados Unidos y mandan dinero
def cam_b(t):
    return Klog(t, [(T_B, (-104.0, 27.5, 0.42)), (T_C, (-102.5, 29.0, 0.45))])


DESTINOS = ["los_angeles", "dallas", "chicago"]


@shot(T_B, bg=lambda t: MP.base(cam_b(t), t, exag=12.0, rios_umbral=0.7), post=[acabado], ent=("tinta", 0.6))
def b_migracion(lz, t):
    cam = cam_b(t)
    MD.mar_vivo(lz, cam, t, seed=14, densidad=0.6)
    MD.ciudad(lz, cam, "juchipila", t, T_B, tam=1.1, tipo="pueblo", nombre="Juchipila", px=26, semilla=2)
    for j, d in enumerate(DESTINOS):
        MD.ciudad(lz, cam, d, t, T_B + 0.2 + 0.15 * j, tam=0.8, tipo="ciudad", nombre=None, px=22, semilla=7 + j)
        a = smooth(prog(t, t_ido - 0.3 + 0.2 * j, t_ido + 0.5 + 0.2 * j))
        if a > 0.01:                                                    # gente que se va
            q = MA_._pts(cam, ["juchipila", (lerp(-103.0, MD.CIUDADES[d][0], 0.5) - 1.5, lerp(21.4, MD.CIUDADES[d][1], 0.5)), d])
            AB.corriente(lz, t, q, n=40, ancho=20.0, vel=0.14, color=((90, 200, 220), (160, 230, 240)), r=(6.0, 10.0), seed=60 + j, capa=2, alfa=a)
        b = smooth(prog(t, t_dinero - 0.2 + 0.15 * j, t_mandan + 0.3 + 0.15 * j))
        if b > 0.01:                                                    # remesas que vuelven
            q = MA_._pts(cam, [d, (lerp(-103.0, MD.CIUDADES[d][0], 0.5) + 1.5, lerp(21.4, MD.CIUDADES[d][1], 0.5) - 0.8), "juchipila"])
            AB.corriente(lz, t, q, n=30, ancho=16.0, vel=0.16, color=((255, 206, 70), (255, 236, 150)), r=(7.0, 11.0), seed=70 + j, capa=2, alfa=b)
    k = U.pop(t, t_eeuu)
    if k > 0.01:
        U.llamada(lz, 860, 150, "a Estados Unidos", color=U.COL["teal"], px=56, k=k, cola=None)
    k = U.pop(t, t_dinero)
    if k > 0.01:
        U.llamada(lz, 1420, 860, "el dinero que mandan", color=U.COL["oro"], px=46, k=k, cola=None, color_texto=(60, 36, 20))
    snd(t_ido, "whoosh", 0.35)
    snd(t_dinero, "monedas", 0.4)


# ------------------------------------------------------------------------------------------------ C. cada junio el pueblo se llena de flores
def cam_c(t):
    return K(t, [(T_C, (200, 60, 20, 0.95)), (T_D, (200, 80, 30, 1.3))])


@shot(T_C, bg=lambda t: PA.cielo(0.0), post=[acabado], ent=("tinta", 0.6))
def c_flores(lz, t):
    cx, cy, cz, zm = cam_c(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    PA.sol(lz, 1600, 220, 60, t, 0.0)
    PA.sierras(lz, t, 15 * (t - T_C), 0.0, y0=440, capas=4, semilla=131, verde=1.0)
    JH.suelo(lz, iso, t)
    JH.objetos_hoy(t, flores=smooth(prog(t, t_junio - 0.3, t_mil + 0.5))).dibujar(lz, iso)
    ME.papel_picado(lz, t, y=70, n=14)
    for j in range(3):
        AB.petalos(lz, t, t_flores + 0.3 * j, (500 + 460 * j, 300), n=26, dur=2.6, seed=20 + j)
    k = U.pop(t, t_junio)
    if k > 0.01:
        U.llamada(lz, 960, 210, "cada junio: Fiesta de Xúchitl", color=U.COL["naranja"], px=54, k=k, cola=None)
    k = U.pop(t, t_mil)
    if k > 0.01:
        U.llamada(lz, 960, 310, "como hace mil años", color=U.COL["magenta"], px=44, k=k, cola=None)
    snd(t_flores, "bling", 0.4)


# ------------------------------------------------------------------------------------------------ D. cada julio: los tastoanes en las fiestas de Santiago
@shot(T_D, bg=lambda t: PA.cielo(0.2), post=[acabado], ent=("tinta", 0.6))
def d_tastoanes(lz, t):
    PA.sol(lz, 1500, 240, 60, t, 0.2)
    PA.sierras(lz, t, 20 * (t - T_D), 0.2, y0=640, capas=3, semilla=141)
    ME.fachada_iglesia(lz, 960, 820, 1.25, capa=0)
    lz.relleno(rect_red(0, 820, W, 260, 0), (214, 190, 150), capa=0)
    ME.papel_picado(lz, t, y=110, n=14)
    MN.tastoanes(lz, t)
    k = U.pop(t, t_julio)
    if k > 0.01:
        U.llamada(lz, 460, 230, "cada julio: fiestas de Santiago", color=U.COL["azul"], px=44, k=k, cola=None)
    k = U.pop(t, t_tastoanes)
    if k > 0.01:
        U.llamada(lz, 1460, 230, "los tastoanes", color=U.COL["rojo"], px=56, k=k * U.repop(t, t_tastoanes + 0.4), cola=None)
    k = U.pop(t, t_recuerdan)
    if k > 0.01:
        U.llamada(lz, 1460, 330, "memoria de la guerra", color=U.COL["oscuro"], px=40, k=k, cola=None)
    snd(t_tastoanes, "tambor", 0.5)


# ------------------------------------------------------------------------------------------------ E. Juchipila: el lugar de las flores nobles
@shot(T_E, bg=lambda t: bg_grad((78, 32, 140), (18, 8, 46), mid=(44, 18, 96), ym=0.5), post=[acabado], ent=("zoom", 0.55))
def e_titulo(lz, t):
    U.bokeh(lz, t, seed=151, n=16, colores=((255, 150, 44), (236, 70, 140), (122, 90, 255), (255, 214, 90)), alfa=0.45)
    U.chispas(lz, t, n=16, seed=15)
    u = prog(t, T_E, T_E + 1.4)
    MA.flor_xuchitl(lz, 960, 440, 260, t, u=u, seed=7)
    AB.petalos(lz, t, T_E + 0.3, (960, 440), n=28, dur=2.6, spread=(-math.pi, 0.0), seed=31)
    a = U.pop(t, t_juch)
    AB.titulo_textura(lz, "JUCHIPILA", 960, 800, 170, t, k=1.0, alfa=min(1.0, a * 1.5))
    k = U.pop(t, t_nobles)
    if k > 0.01:
        U.llamada(lz, 960, 930, "el lugar de las flores nobles", color=U.COL["morado"], px=52, k=k, cola=None)
    k = U.pop(t, t_sobrevivio)
    if k > 0.01:
        U.llamada(lz, 960, 140, "un pueblo que sobrevivió a una guerra", color=U.COL["naranja"], px=46, k=k, cola=None)
    snd(t_juch, "gong", 0.45)


# ------------------------------------------------------------------------------------------------ F. ¿Qué otro pueblo quieres que contemos?
def cam_f(t):
    return Klog(t, [(T_F, (-101.8, 22.0, 0.75)), (T1(E13), (-101.6, 21.6, 0.85))])


PUEBLOS_Q = [(-99.9, 20.4), (-96.7, 17.06), (-103.75, 19.6), (-98.2, 18.9), (-105.2, 20.6), (-101.0, 22.2), (-92.6, 16.7), (-100.4, 19.4), (-97.0, 19.5), (-104.3, 24.0),
             (-106.4, 23.2), (-99.5, 27.0), (-89.6, 20.9)]


@shot(T_F, bg=lambda t: MP.base(cam_f(t), t, exag=12.0, rios_umbral=0.7), post=[acabado], ent=("tinta", 0.6))
def f_pregunta(lz, t):
    cam = cam_f(t)
    MD.mar_vivo(lz, cam, t, seed=16)
    MD.montes(lz, cam)
    MD.ciudad(lz, cam, "juchipila", t, T_F, tam=1.1, tipo="pueblo", nombre="Juchipila", px=26, semilla=2)
    for i, ll in enumerate(PUEBLOS_Q):                                 # signos de pregunta que brotan sobre otros pueblos
        k = pk(t, t_otro - 0.2 + 0.12 * i, 0.4)
        if k > 0.01:
            x, y = MP.proy(cam, *ll)
            lz.relleno(circulo(float(x), float(y) - 40 * k, 30 * k, 22), U.COL["morado"], capa=2)
            P.rotulo(lz, float(x), float(y) - 40 * k, "?", px=int(40 * k) + 1, color=(255, 255, 255), alfa=1.0, sombra=0.0)
            lz.relleno(np.array([(float(x) - 10 * k, float(y) - 18 * k), (float(x), float(y)), (float(x) + 10 * k, float(y) - 18 * k)]), U.COL["morado"], capa=2)
    k = U.pop(t, t_que)
    if k > 0.01:
        U.llamada(lz, 960, 150, "¿Qué otro pueblo contamos?", color=U.COL["naranja"], px=62, k=k, cola=None)
    MN.icono_comentarios(lz, 1620, 860, 1.0, t, k=pk(t, t_comentarios - 0.2, 0.45))
    for i in range(6):
        snd(t_otro - 0.2 + 0.24 * i, "pop", 0.25)
