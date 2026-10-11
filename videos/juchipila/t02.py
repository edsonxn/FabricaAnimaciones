# -*- coding: utf-8 -*-
"""Escena 2 · el cañón (0:24-1:02): paisaje, mapa (160 km de Zacatecas), río Juchipila hacia el Río Grande de Santiago, corte entre dos sierras,
el pueblo en el fondo del cañón (1 249 m, maíz) y el cañón como corredor natural (camino real Guadalajara-Zacatecas)."""
import math

import numpy as np

import kz_ui as U
import kz_mapa as KM
import kz_mapa_dib as MD
import kz_iso as I
import kz_iso_deco as DC
import kz_abstracto as AB
import plano as P
import lugares  # noqa: F401
import paisajes as PA
import mundos_b as MB
import mapas as MA_
from motor import W, H, prog, lerp, smooth, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, h01, catmull
from reg import shot, snd
from util import *  # noqa: F401,F403
from t01 import acabado

E2 = "canon"
t_mirar, t_paisaje, t_suroeste, t_zac, t_km, t_capital = T(E2, "mirar", frase=0), T(E2, "paisaje", frase=0), T(E2, "suroeste", frase=0), T(E2, "zacatecas", frase=0), T(E2, "ciento", frase=0), T(E2, "capital", frase=0)
t_aqui, t_montanas, t_abren, t_rio, t_juch, t_sur, t_sant = T(E2, "aqui", frase=1), T(E2, "montanas", frase=1), T(E2, "abren", frase=1), T(E2, "rio", frase=1), T(E2, "juchipila", frase=1), T(E2, "sur", frase=1), T(E2, "santiago", frase=1)
t_sierra, t_mor, t_otro, t_noch = T(E2, "sierra", frase=2), T(E2, "morones", frase=2), T(E2, "otro", frase=2), T(E2, "nochistlan", frase=2)
t_mil, t_alt, t_fondo, t_canon, t_agua, t_maiz = T(E2, "mil", frase=3), T(E2, "altura", frase=3), T(E2, "fondo", frase=3), T(E2, "canon", frase=3), T(E2, "agua", frase=3), T(E2, "maiz", frase=3)
t_corr, t_pueblos, t_siglos, t_camino, t_guad, t_zac2 = T(E2, "corredor", frase=4), T(E2, "pueblos", frase=4), T(E2, "siglos", frase=4), T(E2, "camino", frase=4), T(E2, "guadalajara", frase=4), T(E2, "zacatecas", frase=4)
MP = KM.MAPA
CP = MB.CanonPueblo()
T_A, T_B, T_C, T_D, T_E, T_F = T0(E2), t_suroeste - 0.1, t_aqui - 0.1, FIN(E2, 1) + 0.0, t_mil - 0.15, t_corr - 0.2
T_D = t_sierra - 0.1
RIO_RUTA = [(-103.33, 21.98), (-103.22, 21.74), (-103.13, 21.55), (-103.1176, 21.41), (-103.17, 21.22), (-103.24, 21.03)]


# ------------------------------------------------------------------------------------------------ A. mirar el paisaje
@shot(T_A, bg=lambda t: PA.cielo(0.0), post=[acabado], ent=("fundido", 0.4))
def a_paisaje(lz, t):
    cx = 150.0 * (t - T_A)
    PA.sol(lz, 1500, 300, 78, t, 0.0)
    PA.sierras(lz, t, cx, 0.0, y0=640)
    PA.rio(lz, t, 0.0)
    PA.aldea(lz, t, 0.0, x0=560, x1=1380, y=716, n=6)
    PA.pared_canon(lz, t, -1, 0.0, ancho=380, seed=2)
    PA.pared_canon(lz, t, 1, 0.0, ancho=380, seed=5)
    PA.aves(lz, t, n=8, seed=3)
    PA.flores_frente(lz, t, cx, amb=0.0)
    k = U.pop(t, t_mirar) * U.salida(t, t_suroeste - 0.5, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 210, "el cañón de Juchipila", color=U.COL["naranja"], px=64, k=k, cola=None)


# ------------------------------------------------------------------------------------------------ B. 160 km de la capital
def cam_b(t):
    return Klog(t, [(T_B, (-103.0, 22.15, 1.45)), (T_C, (-102.95, 22.05, 1.75))])


@shot(T_B, bg=lambda t: MP.base(cam_b(t), t, exag=12.0, rios_umbral=0.7), post=[acabado], ent=("tinta", 0.7))
def b_distancia(lz, t):
    cam = cam_b(t)
    MD.mar_vivo(lz, cam, t, seed=2)
    MD.montes(lz, cam)
    MD.region(lz, cam, "SUROESTE DE ZACATECAS", (-103.35, 22.0), px=28, rot=-0.8, alfa=0.7, z_max=3.0)
    MD.ciudad(lz, cam, "zacatecas", t, t_zac, tam=1.1, tipo="ciudad", nombre="capital: Zacatecas", px=30)
    MD.ciudad(lz, cam, "juchipila", t, t_suroeste, tam=1.1, tipo="pueblo", nombre="Juchipila", px=30, semilla=3)
    # línea entre los dos con la distancia
    a = MP.proy(cam, *MD.CIUDADES["juchipila"])
    b = MP.proy(cam, *MD.CIUDADES["zacatecas"])
    f = e_inout(prog(t, t_km - 0.2, t_km + 1.0))
    if f > 0.01:
        MA_.ruta_gruesa(lz, cam, ["juchipila", "zacatecas"], frac=f, t=t, color=(222, 60, 70), ancho=9, dash=True, flecha=False)
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        kk = U.pop(t, t_km + 0.5)
        U.llamada(lz, float(mx) + 270, float(my) - 30, "≈ 160 km", color=U.COL["rojo"], px=64, k=kk * U.repop(t, t_km + 1.2), cola=None)
    MD.brujula(lz, W - 120, H - 130, 1.0)
    MD.escala(lz, 80, H - 70, cam, km=100)
    snd(t_km, "pop", 0.4)


# ------------------------------------------------------------------------------------------------ C. el río Juchipila
def cam_c(t):
    return Klog(t, [(T_C, (-103.12, 21.70, 2.6)), (t_sant, (-103.18, 21.35, 3.1)), (T_D, (-103.19, 21.30, 3.15))])


@shot(T_C, bg=lambda t: MP.base(cam_c(t), t, exag=12.0, rios_umbral=0.7), post=[acabado], ent=("fundido", 0.5))
def c_rio(lz, t):
    cam = cam_c(t)
    MD.montes(lz, cam)
    MD.region(lz, cam, "SIERRA DE MORONES", (-103.62, 21.45), px=24, rot=-1.45, alfa=0.55)
    MD.region(lz, cam, "SIERRA DE NOCHISTLÁN", (-102.80, 21.45), px=24, rot=-1.45, alfa=0.55)
    f = prog(t, t_rio, t_sant + 0.4)
    MA_.ruta_gruesa(lz, cam, RIO_RUTA, frac=e_inout(f), t=t, color=(36, 140, 255), ancho=11, dash=False)
    if f > 0.05:
        pts_r = [MA_.proy(cam, c) for c in RIO_RUTA]
        AB.corriente(lz, t, pts_r, n=30, ancho=9.0, vel=0.10, color=((190, 235, 255), (255, 255, 255)), r=(3.0, 5.5), seed=6, capa=2, alfa=min(1.0, f * 4))
    MD.ciudad(lz, cam, "juchipila", t, t_juch - 0.3, tam=1.0, tipo="pueblo", semilla=3)
    k = U.pop(t, t_juch) * U.salida(t, T_D - 0.1, 0.2)
    p = MP.proy(cam, -103.1176, 21.41)
    if k > 0.01:
        U.llamada(lz, float(p[0]) + 210, float(p[1]) - 16, "río Juchipila", color=U.COL["azul"], px=44, k=k, cola=None)
    k2 = U.pop(t, t_sant) * U.salida(t, T_D - 0.1, 0.2)
    q = MP.proy(cam, *RIO_RUTA[-1])
    if k2 > 0.01:
        U.llamada(lz, float(q[0]) + 40, float(q[1]) + 60, "Río Grande de Santiago", color=U.COL["teal"], px=40, k=k2, cola="arriba")
    k3 = U.pop(t, t_sur - 0.1) * U.salida(t, T_D - 0.1, 0.2)
    if k3 > 0.01:
        U.llamada(lz, W - 330, 150, "hacia el sur", color=U.COL["naranja"], px=46, k=k3, cola=None)
        MA_.flecha_pantalla(lz, W - 330, 200, W - 330, 330, color=(240, 130, 36), ancho=16, alfa=min(1.0, k3))
    MD.escala(lz, 80, H - 70, cam, km=50)
    snd(t_juch, "ola", 0.35)


# ------------------------------------------------------------------------------------------------ D. dos sierras (corte)
@shot(T_D, bg=lambda t: bg_grad((255, 190, 120), (255, 232, 176), mid=(246, 140, 150), ym=0.55), post=[acabado], ent=("tinta", 0.6))
def d_corte(lz, t):
    u = prog(t, T_D + 0.1, T_D + 1.3)
    PA.sol(lz, 960, 300, 70, t, 0.0)
    PA.sierras(lz, t, 0.0, 0.0, y0=640, capas=3, semilla=11)
    pts = MB.corte_canon(lz, t, u)
    PA.aves(lz, t, n=5, seed=9, y0=120, y1=300)
    k = U.pop(t, t_mor) * U.salida(t, T_E - 0.1, 0.2)
    if k > 0.01:
        U.llamada(lz, float(pts["izq"][0]), float(pts["izq"][1]) - 40, "sierra de Morones", color=U.COL["morado"], px=52, k=k, cola="abajo")
    k = U.pop(t, t_noch) * U.salida(t, T_E - 0.1, 0.2)
    if k > 0.01:
        U.llamada(lz, float(pts["der"][0]), float(pts["der"][1]) - 40, "sierra de Nochistlán", color=U.COL["magenta"], px=52, k=k, cola="abajo")
    k = U.pop(t, t_otro) * U.salida(t, T_E - 0.1, 0.2)
    if k > 0.01:
        U.llamada(lz, 960, 580, "el cañón", color=U.COL["teal"], px=46, k=k, cola=None)


# ------------------------------------------------------------------------------------------------ E. el pueblo en el fondo del cañón
def cam_e(t):
    return K(t, [(T_E, (230, -120, 20, 1.05)), (t_canon, (205, 120, 20, 1.20)), (t_maiz - 0.4, (240, 340, 20, 1.40)), (T_F, (280, 400, 20, 1.55))])


@shot(T_E, bg=lambda t: PA.cielo(0.0), post=[acabado], ent=("fundido", 0.5))
def e_pueblo(lz, t):
    cx, cy, cz, zm = cam_e(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz(mul=(1.03, 1.0, 0.95), mix=(255, 170, 110), k=0.06)
    PA.sol(lz, 1560, 260, 70, t, 0.0)
    PA.sierras(lz, t, cy * 0.5, 0.0, y0=560, capas=4, semilla=7)
    CP.suelo(lz, iso, t)
    m = CP.objetos(t)
    m.dibujar(lz, iso)
    DC.aves(lz, t, n=7, seed=3)
    DC.polvo_luz(lz, t, n=18, seed=2)
    # altitud que sube hasta 1 249 m
    v = lerp(0, 1249, e_out(prog(t, t_mil, t_mil + 1.3)))
    k = U.pop(t, t_mil) * U.salida(t, t_fondo - 0.05, 0.25)
    if k > 0.01:
        lz.texto(f"{int(v):,}".replace(",", " ") + " m", 330, 190, 130, "geo_x", color=(255, 255, 255), borde=None, k=k, alfa=1.0, capa=2, temblor=0.0)
        U.llamada(lz, 330, 290, "sobre el nivel del mar", color=U.COL["naranja"], px=36, k=k, cola="arriba")
    k = U.pop(t, t_canon) * U.salida(t, t_agua - 0.1, 0.25)
    if k > 0.01:
        U.llamada(lz, 360, 190, "largo y estrecho", color=U.COL["morado"], px=54, k=k, cola=None)
    k = U.pop(t, t_agua) * U.salida(t, t_maiz - 0.05, 0.2)
    if k > 0.01:
        q = iso.P(262, 200, 14)
        U.llamada(lz, float(q[0]) + 150, float(q[1]) - 40, "agua", color=U.COL["azul"], px=44, k=k, cola="abajo")
    k = U.pop(t, t_maiz) * U.salida(t, T_F - 0.1, 0.25)
    if k > 0.01:
        q = iso.P(395, 392, 22)
        U.llamada(lz, float(q[0]), float(q[1]) - 40, "maíz", color=U.COL["oro"], px=50, k=k, cola="abajo", color_texto=(60, 36, 20))
    snd(t_mil, "bling", 0.4)


# ------------------------------------------------------------------------------------------------ F. un corredor natural
CORREDOR = [(-103.30, 22.25), (-103.20, 21.90), (-103.14, 21.62), (-103.1176, 21.41), (-103.16, 21.15), (-103.24, 20.90)]
CAMINO = ["guadalajara", (-103.24, 20.95), (-103.1176, 21.41), (-103.14, 21.80), (-102.9, 22.3), "zacatecas"]


def cam_f(t):
    return Klog(t, [(T_F, (-103.16, 21.75, 3.4)), (t_siglos - 0.3, (-103.17, 21.7, 3.4)), (t_camino - 0.1, (-102.95, 21.85, 1.85)), (T1(E2), (-102.95, 21.85, 1.85))])


@shot(T_F, bg=lambda t: MP.base(cam_f(t), t, exag=12.0, rios_umbral=0.7), post=[acabado], ent=("tinta", 0.7))
def f_corredor(lz, t):
    cam = cam_f(t)
    MD.montes(lz, cam)
    MD.ciudad(lz, cam, "juchipila", t, T_F, tam=1.0, tipo="pueblo", semilla=3)
    # personas (puntos de colores) que van y vienen por el cañón: pueblos enteros
    pts = [tuple(MP.proy(cam, *c)) for c in CORREDOR]
    ga = U.pop(t, t_corr) * (1 - smooth(prog(t, t_siglos + 0.2, t_siglos + 1.0)))
    if ga > 0.01:
        lz.trazo(np.array(catmull(np.array(pts, float), 10, False)), (255, 255, 255, int(70 * ga)), 90.0 * float(np.clip(cam[2] / 3.4, 0.5, 1.0)), afinar=False, temblor=0.0, capa=1)
    a = U.pop(t, t_corr) * (1 - smooth(prog(t, t_siglos + 0.2, t_siglos + 1.0)))
    if a > 0.01:
        sc = float(np.clip(cam[2] / 3.4, 0.5, 1.0))
        AB.corriente(lz, t, pts, n=54, ancho=34.0 * sc, vel=0.11, color=((255, 130, 90), (255, 206, 90), (236, 70, 140), (120, 220, 200)), r=(7.0 * sc, 12.0 * sc), seed=3, capa=2, alfa=min(1.0, a), estela=1.0)
        AB.corriente(lz, t, pts[::-1], n=34, ancho=34.0 * sc, vel=0.08, color=((255, 255, 255), (255, 214, 120), (190, 150, 255)), r=(6.0 * sc, 10.0 * sc), seed=8, capa=2, alfa=min(1.0, a), estela=1.0)
    k = U.pop(t, t_corr) * U.salida(t, t_siglos - 0.1, 0.25)
    if k > 0.01:
        U.llamada(lz, W / 2, 150, "un corredor natural", color=U.COL["naranja"], px=64, k=k, cola=None)
    k = U.pop(t, t_pueblos) * U.salida(t, t_siglos - 0.1, 0.25)
    p0 = MP.proy(cam, -103.2, 21.95)
    if k > 0.01:
        U.llamada(lz, float(p0[0]) + 200, float(p0[1]), "pueblos enteros", color=U.COL["magenta"], px=44, k=k, cola=None)
    # siglos después: el camino real
    ks = U.pop(t, t_siglos) * U.salida(t, t_camino - 0.1, 0.25)
    if ks > 0.01:
        U.llamada(lz, W / 2, 150, "siglos después…", color=U.COL["morado"], px=60, k=ks, cola=None)
    f = prog(t, t_camino, t_zac2 + 0.6)
    if f > 0.001:
        MA_.ruta_gruesa(lz, cam, CAMINO, frac=e_inout(f), t=t, color=(240, 150, 30), ancho=10, dash=True)
    MD.ciudad(lz, cam, "guadalajara", t, t_guad - 0.1, tam=0.9, tipo="ciudad", nombre="Guadalajara", px=30, semilla=2)
    MD.ciudad(lz, cam, "zacatecas", t, t_zac2 - 0.1, tam=0.9, tipo="ciudad", nombre="Zacatecas", px=30, semilla=4)
    kc = U.pop(t, t_camino + 0.2)
    if kc > 0.01:
        U.llamada(lz, W / 2, 150, "el primer camino real", color=U.COL["oro"], px=64, k=kc, cola=None, color_texto=(60, 36, 20))
    MD.escala(lz, 80, H - 70, cam, km=100)
