# -*- coding: utf-8 -*-
"""Escena 1 · gancho: la carretera 54 en el mapa de relieve real, la lupa entre Juchipila y Jalpa, los dos nombres de agua (agua espumosa /
en el agua caliente), el montaje de la historia (caxcanes, frailes, haciendas, guerra) y el título."""
import math

import numpy as np

import kz_ui as U
import kz_mapa as KM
import kz_mapa_dib as MD
import kz_pers2d as K2
import kz_abstracto as AB
import plano as P
import lugares  # noqa: F401  (registra los lugares del video)
import paisajes as PA
import paisajes as PA_
import mapas as MA_
import mundos_1 as M1
from motor import W, H, prog, lerp, smooth, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, h01
from reg import shot, snd
from util import *  # noqa: F401,F403

E1 = "gancho"
MP = KM.MAPA
t_juch, t_jalpa, t_carr, t_pueblo, t_nombres, t_agua = (T(E1, "juchipila", frase=0), T(E1, "jalpa", frase=0), T(E1, "carretera", frase=0),
                                                         T(E1, "pueblo", frase=0), T(E1, "nombres", frase=0), T(E1, "agua", frase=0))
t_uno, t_esp, t_otro, t_cal = T(E1, "uno", frase=1), T(E1, "espumosa", frase=1), T(E1, "otro", frase=1), T(E1, "caliente", frase=1)
t_agua1 = T(E1, "agua", frase=1)
t_entre, t_caxc, t_frai, t_hac, t_guerra = (T(E1, "entre", frase=2), T(E1, "caxcanes", frase=2), T(E1, "frailes", frase=2), T(E1, "haciendas", frase=2),
                                            T(E1, "guerra", frase=2))
t_esta, t_apozol = T(E1, "esta", frase=3), T(E1, "apozol", frase=3)
T_A = T0(E1)
T_B = t_uno - 0.15
T_C = t_entre - 0.2
T_D = t_esta - 0.2


def acabado(img, t):
    return AB.grano(U.gradacion(img, luces=(1.03, 1.0, 0.95), sombras=(0.96, 0.97, 1.05), contraste=1.05, saturacion=1.08), t)


# ------------------------------------------------------------------------------------------------ A. la carretera y la lupa
def cam_mapa(t):
    return Klog(t, [(T_A, (-101.35, 22.15, 0.95)), (t_juch - 0.3, (-100.9, 21.95, 2.2))])


LENTE = (1390.0, 540.0, 330.0)


@shot(T_A, bg=lambda t: MP.base(cam_mapa(t), t, exag=12.0, rios_umbral=0.7), post=[acabado], ent=("fundido", 0.01))
def a_mapa(lz, t):
    cam = cam_mapa(t)
    MD.mar_vivo(lz, cam, t, seed=5)
    MD.montes(lz, cam)
    MD.region(lz, cam, "ZACATECAS", (-102.5, 23.35), px=44, alfa=0.80, z_max=2.6)
    MD.region(lz, cam, "JALISCO", (-103.2, 20.25), px=34, alfa=0.55, z_max=2.6)
    MD.ciudad(lz, cam, "zacatecas", t, T_A + 0.4, tam=0.8, tipo="ciudad", nombre="Zacatecas", px=26)
    MD.ciudad(lz, cam, "guadalajara", t, T_A + 0.7, tam=0.8, tipo="ciudad", nombre="Guadalajara", px=26)
    # la carretera federal 54 se dibuja de Zacatecas a Guadalajara
    f = smooth(prog(t, t_juch - 1.2, t_carr + 1.8))
    if f > 0.01:
        MA_.ruta_gruesa(lz, cam, ["zacatecas", "villanueva", "tabasco", "jalpa", "apozol", "juchipila", "moyahua", "mezquital", (-103.30, 21.00), "guadalajara"],
                        frac=f, t=t, color=(255, 214, 72), ancho=9.0, dash=True, flecha=False)
    sx, sy = MA_.proy(cam, "apozol")
    # la lupa crece desde el cañón
    kl = pk(t, t_juch - 0.25, 0.55)
    if kl > 0.01:
        MD.onda(lz, cam, "apozol", t, t_juch - 0.2, dur=2.4, r_deg=0.35, n=3, ancho=5.0, periodo=0.5, alfa=0.9, color=(255, 214, 90))
        cx, cy, R = LENTE
        lz.trazo(np.array([(sx + 40, sy - 16), (cx - R * 0.96, cy - 40)]), (255, 244, 200, 190), 4.0, afinar=False, temblor=0.0, capa=2)
        lz.trazo(np.array([(sx + 40, sy + 22), (cx - R * 0.94, cy + 150)]), (255, 244, 200, 190), 4.0, afinar=False, temblor=0.0, capa=2)
        M1.lupa_carretera(lz, cx, cy, R, t, k=kl, t_juch=t_juch, t_jalpa=t_jalpa, t_carr=t_carr, t_apozol=t_pueblo, t_nombres=t_nombres)
    k = U.pop(t, t_carr) * U.salida(t, T_B - 0.1)
    if k > 0.01:
        U.llamada(lz, 430, 760, "carretera federal 54", color=U.COL["oscuro"], px=44, k=k, cola=None)
    k = U.pop(t, t_nombres) * U.salida(t, T_B - 0.1)
    if k > 0.01:
        U.llamada(lz, 1390, 940, "un pueblo, dos nombres", color=U.COL["morado"], px=48, k=k * U.repop(t, t_agua + 0.1), cola=None)
    k = pk(t, t_agua, 0.5) * (1 - smooth(prog(t, T_B - 0.25, T_B)))
    if k > 0.01:
        M1.gota(lz, 1390, 500, 54, t, k=k)
    snd(t_juch, "pop", 0.4)
    snd(t_jalpa, "pop", 0.4)
    snd(t_pueblo, "bling", 0.4)


# ------------------------------------------------------------------------------------------------ B. dos nombres de agua
def _xm(t):
    return lerp(W + 140, 960, e_inout(prog(t, t_otro - 0.25, t_otro + 0.55)))


@shot(T_B, bg=lambda t: bg_grad((250, 150, 90), (160, 40, 90), mid=(236, 110, 90), ym=0.55), post=[acabado], ent=("zoom", 0.5))
def b_nombres(lz, t):
    xm = _xm(t)
    izq = [(-10, -10), (xm + 70, -10), (xm - 70, H + 10), (-10, H + 10)]
    # mitad izquierda: agua espumosa (frío)
    with lz.recorte(izq):
        lz.degradado(izq, (60, 150, 230), (18, 52, 140), (0, 0), (0, H), capa=0)
        U.bokeh(lz, t, seed=11, n=12, colores=((130, 226, 240), (255, 255, 255), (90, 160, 255)), alfa=0.30, area=(0, 0, xm, H))
        U.chispas(lz, t, n=12, seed=4, area=(0, 0, 1100, H))
        M1.agua_con_espuma(lz, -20, W + 40, 700, t, k=pk(t, T_B + 0.25, 0.6), seed=3)
        k = pk(t, t_uno + 0.1, 0.5)
        M1.gota(lz, 470, 460, 120, t, k=k)
    for i in range(7):                                                  # gotas flotando en toda la pantalla antes de la mitad cálida
        ka = pk(t, T_B + 0.1 + 0.12 * i, 0.5) * (1 - smooth(prog(t, t_otro - 0.3, t_otro + 0.5)))
        M1.gota(lz, 1080 + 130 * i + 30 * math.sin(i * 1.9), 380 + 90 * (i % 3) + 24 * math.sin(t * 1.3 + i), 20 + 12 * h01(5, i), t, k=ka, alfa=0.85, seed=i)
    # mitad derecha: en el agua caliente (cálido), se destapa al decir «el otro»
    der = [(xm + 70, -10), (W + 10, -10), (W + 10, H + 10), (xm - 70, H + 10)]
    with lz.recorte(der):
        U.bokeh(lz, t, seed=13, n=5, colores=((255, 214, 120), (255, 150, 90)), alfa=0.18, area=(xm, 700, W, H))
        kp = pk(t, t_cal - 0.4, 0.6)
        M1.poza(lz, 1440, 730, 330, 130, t, k=kp, seed=2)
    # rótulos
    k = U.pop(t, t_esp - 0.2) * U.salida(t, T_C - 0.25)
    if k > 0.01:
        AB.titulo_textura(lz, "APOZOL", 480, 175, 150, t, paleta=((40, 110, 230), (30, 170, 170), (110, 226, 236), (255, 255, 255), (240, 130, 36)), k=1.0, alfa=min(1.0, k * 1.5))
        U.llamada(lz, 480, 300, "atl (agua) + pozolli (espuma)", color=U.COL["azul"], px=36, k=k, cola=None)
    k = U.pop(t, t_esp) * U.salida(t, T_C - 0.25)
    if k > 0.01:
        U.llamada(lz, 480, 930, "agua espumosa", color=U.COL["teal"], px=54, k=k * U.repop(t, t_esp + 0.4), cola=None)
    k = U.pop(t, t_cal - 0.15) * U.salida(t, T_C - 0.25)
    if k > 0.01:
        AB.titulo_textura(lz, "ATOTONILCO", 1450, 175, 128, t, paleta=((250, 130, 36), (255, 200, 70), (236, 70, 120), (255, 255, 255), (255, 150, 90)), k=1.0, alfa=min(1.0, k * 1.5))
        U.llamada(lz, 1450, 300, "en náhuatl", color=U.COL["magenta"], px=34, k=k, cola=None)
    k = U.pop(t, t_cal) * U.salida(t, T_C - 0.25)
    if k > 0.01:
        U.llamada(lz, 1450, 940, "en el agua caliente", color=U.COL["rojo"], px=54, k=k * U.repop(t, t_cal + 0.4), cola=None)
    snd(t_esp, "burbujas", 0.4)
    snd(t_cal, "siseo", 0.4)


# ------------------------------------------------------------------------------------------------ C. el montaje: caxcanes, frailes, haciendas, guerra
MEDS = [(330, "caxcanes", t_caxc, (96, 52, 160), (40, 24, 90)), (790, "frailes", t_frai, (60, 130, 190), (20, 50, 110)),
        (1250, "haciendas", t_hac, (255, 214, 140), (236, 150, 110)), (1710, "una guerra", t_guerra, (236, 104, 84), (62, 24, 76))]


def _medallon(lz, t, i, x, y, r, t0, bg0, bg1, k):
    if k <= 0.01:
        return
    rr = r * k
    ring = circulo(x, y, rr, 48)
    lz.relleno(circulo(x + 8, y + 12, rr + 6, 48), (10, 6, 30), alfa=0.35, capa=1)
    with lz.recorte(ring):
        lz.degradado(ring, bg0, bg1, (x, y - rr), (x, y + rr), capa=1)
        if i == 0:
            U.bokeh(lz, t, seed=21, n=5, colores=((255, 206, 90), (236, 70, 140)), alfa=0.3, area=(x - r, y - r, x + r, y + r))
            K2.busto(lz, x + 4, y + rr * 0.92, 118 * k, "caxcan", t, yaw=-0.45, emocion="serio", ojos="abiertos", seed=7)
        elif i == 1:
            lz.halo(x, y - 40, 200, (255, 230, 170), alfa=0.35, dureza=1.1, capa=1)
            K2.busto(lz, x - 2, y + rr * 0.92, 118 * k, "fraile", t, yaw=0.4, emocion="pensativo", ojos="abiertos", seed=9)
        elif i == 2:
            lz.halo(x + 110, y - 100, 130, (255, 246, 190), alfa=0.6, dureza=1.2, capa=1)
            lz.relleno(rect_red(x - rr, y + 70, 2 * rr, rr, 0), (112, 170, 92), capa=1)
            lz.relleno(rect_red(x - rr, y + 70, 2 * rr, 10, 0), (146, 200, 110), capa=1)
            M1.hacienda2d(lz, x - 4, y + 96, 0.74 * k, capa=1)
            for j, (ox, sc) in enumerate(((-150, 0.9), (150, 1.0))):
                PA_.arbol(lz, x + ox * k, y + 116, 0.9 * sc * k, 0.0, seed=j + 3, t=t, capa=1)
        else:
            lz.halo(x, y - 10, 220, (255, 170, 90), alfa=0.35, dureza=1.0, capa=1)
            lz.relleno(rect_red(x - rr, y + 120, 2 * rr, rr, 0), (54, 24, 66), capa=1)
            M1.penol_fuego(lz, x, y + 140, 0.62 * k, t, capa=1)
    lz.trazo(ring, (255, 206, 72), 9.0, cerrado=True, afinar=False, temblor=0.0, capa=2)


@shot(T_C, bg=lambda t: bg_grad((70, 40, 120), (24, 14, 60), mid=(44, 24, 96), ym=0.5), post=[acabado], ent=("tinta", 0.55))
def c_montaje(lz, t):
    U.bokeh(lz, t, seed=15, n=12, colores=((255, 150, 44), (236, 70, 140), (122, 90, 255), (90, 210, 190)), alfa=0.35)
    for i, (x, nom, t0, c0, c1) in enumerate(MEDS):
        k = pk(t, min(t0 - 0.25, T_C + 0.3 + 0.55 * i), 0.5)
        _medallon(lz, t, i, x, 520, 190, t0, c0, c1, k)
        ka = U.pop(t, t0) * U.salida(t, T_D - 0.2)
        if ka > 0.01:
            U.llamada(lz, x, 800, nom, color=U.COL["naranja"] if i != 3 else U.COL["rojo"], px=48, k=ka, cola=None)
    kt = U.pop(t, T_C + 0.1) * U.salida(t, T_D - 0.2)
    if kt > 0.01:
        U.llamada(lz, W / 2, 180, "entre esos dos nombres", color=U.COL["morado"], px=56, k=kt, cola=None)
    snd(t_caxc, "pop", 0.4)
    snd(t_frai, "pop", 0.4)
    snd(t_hac, "pop", 0.4)
    snd(t_guerra, "tambor", 0.5)


# ------------------------------------------------------------------------------------------------ D. título
@shot(T_D, bg=lambda t: PA.cielo(0.0), post=[acabado], ent=("fundido", 0.6))
def d_titulo(lz, t):
    cx = 22.0 * (t - T_D)
    PA.sol(lz, 1500, 250, 70, t, 0.0)
    U.haces_luz(lz, 1500, 250, t, n=9, largo=1400, color=(255, 236, 190), alfa=0.10)
    PA.sierras(lz, t, cx, 0.0, y0=700, capas=5, semilla=31, verde=0.0)
    PA.rio(lz, t, 0.0)
    PA.aldea(lz, t, 0.0, n=5, seed=9)
    PA.pared_canon(lz, t, -1, 0.0, ancho=380, seed=3)
    PA.pared_canon(lz, t, 1, 0.0, ancho=380, seed=6)
    PA.aves(lz, t, n=6, seed=4)
    PA.flores_frente(lz, t, cx, n=14, amb=0.0, seed=8)
    a = U.pop(t, t_apozol - 0.1)
    AB.titulo_textura(lz, "APOZOL", W / 2, 250, 190, t, paleta=((40, 110, 230), (30, 170, 170), (110, 226, 236), (240, 130, 36), (255, 204, 70)), k=1.0, alfa=min(1.0, a * 1.5))
    k = U.pop(t, t_apozol + 0.5)
    if k > 0.01:
        U.llamada(lz, W / 2, 410, "la historia de un pueblo de agua", color=U.COL["morado"], px=44, k=k, cola=None)
    for i in range(6):                                                        # gotitas que suben
        u = ((t - T_D) * 0.18 + i / 6) % 1.0
        M1.gota(lz, 380 + 230 * i + 40 * math.sin(i * 2.0), 900 - u * 520, 12 + 8 * h01(3, i), t, k=min(1.0, u * 6) * (1 - u), alfa=0.9, seed=i)
    snd(t_apozol, "bling", 0.5)
