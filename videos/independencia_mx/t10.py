# -*- coding: utf-8 -*-
"""Escena 10 · Morelos (5:32-6:17): Hidalgo lo envía al sur, hijo de carpintero y genio militar, un ejército pequeño y disciplinado, el sitio de Cuautla, la salida de noche, Matamoros, Galeana y Leona Vicario, y la conquista de Oaxaca y Acapulco."""
import math

import numpy as np

import kz_iso as I
from kz_iso import tint
import kz_iso_obj as O
import kz_iso_obj2 as O2
import kz_iso_arq as A
import kz_iso_arq2 as B
import kz_iso_int as N
import kz_gente_iso as G
import kz_iso_deco as DC
import kz_retrato as RT
import kz_ui as U
import kz_mapa as KM
import kz_mapa_dib as MD
import plano as P
from motor import W, H, prog, lerp, smooth, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, h01, catmull
from reg import shot, snd
from util import *  # noqa: F401,F403
import mundos_k as mk

E10 = "morelos"
MP = KM.MAPA
GRAD = lambda img, t: U.gradacion(img)
BASE = lambda cam, t: MP.base(cam, t, exag=13.0, rios_umbral=0.7)
CUA = mk.Cuautla()

# ------------------------------------------------------------------ anclas
t_antes, t_mor, t_hid, t_env, t_amigo, t_jose, t_morelos, t_lev, t_sur = [T(E10, w, frase=0) for w in ("antes", "morir", "hidalgo", "enviado", "amigo", "jose", "morelos", "levantar", "sur")]
t_m1, t_cura, t_hijo, t_carp, t_tal, t_nadie, t_genio, t_mil = [T(E10, w, frase=1) for w in ("morelos", "cura", "hijo", "carpintero", "talento", "nadie", "genio", "militar")]
t_ejer, t_peq, t_org, t_disc, t_gano, t_bat = [T(E10, w, frase=2) for w in ("ejercito", "pequeno", "organizado", "disciplinado", "gano", "batalla")]
t_1812, t_res, t_set, t_dias, t_sitio, t_cuautla, t_rod, t_miles, t_sold = [T(E10, w, frase=3) for w in ("doce", "resistio", "setenta", "dias", "sitio", "cuautla", "rodeado", "miles", "soldados")]
t_cuando, t_comida, t_saco, t_hombres, t_noche, t_salvo = [T(E10, w, frase=4) for w in ("cuando", "comida", "saco", "hombres", "noche", "salvo")]
t_junto, t_mat, t_gal, t_capital, t_espia, t_leona, t_vic, t_info, t_dinero = [T(E10, w, frase=5) for w in ("junto", "matamoros", "galeana", "capital", "espia", "leona", "vicario", "informacion", "dinero")]
t_poco, t_tomo, t_oax, t_aca, t_control, t_parte, t_sur2, t_pais = [T(E10, w, frase=6) for w in ("poco", "tomo", "oaxaca", "acapulco", "controlar", "parte", "sur", "pais")]
T_A, T_B1, T_B2, T_C, T_D, T_E, T_F, T_F2, T_G = T0(E10), t_m1 - 0.15, t_tal - 0.2, t_ejer - 0.2, t_1812 - 0.2, t_cuando - 0.2, t_junto - 0.2, t_capital - 1.0, t_poco - 0.2


# ------------------------------------------------------------------------------------------------ 1. HIDALGO ENVÍA A MORELOS AL SUR (mapa)
RUTA_S = [(-101.19, 19.70), (-101.07, 19.01), (-100.60, 18.30), (-99.89, 16.85)]


def cam_a(t):
    return Klog(t, [(T_A, (-100.6, 19.1, 1.9)), (t_morelos, (-100.6, 18.5, 2.2)), (T_B1, (-100.4, 18.2, 2.3))])


@shot(T_A, bg=lambda t: BASE(cam_a(t), t), post=[GRAD], ent=("fundido", 0.5))
def mo_sur(lz, t):
    cam = cam_a(t)
    I.luz()
    MD.montes(lz, cam, min_alt=2200)
    MD.pais(lz, cam, "Mexico", (255, 96, 70), alfa=0.10, borde=(255, 220, 90), ancho=4.0, t=t, latido=1.0)
    for j, (lug, tp, nm, dx, dy, lado) in enumerate((("valladolid", "ciudad", "Valladolid", -130, 4, "der"), ("caracuaro", "pueblo", "Carácuaro", 130, 4, "izq"), ("acapulco", "puerto", "Acapulco", 130, 4, "izq"), ("mexico", "ciudad", "", 0, 0, "izq"))):
        MD.ciudad(lz, cam, lug, t, T_A + 0.1 * j, tam=1.4, tipo=tp, bando="ins" if j < 3 else "real", semilla=j + 71)
        if nm:
            MD.etiqueta(lz, cam, lug, nm, t, T_A + 0.1 * j + 0.1, px=22, dy=dy, dx=dx, lado=lado)
    f = e_inout(prog(t, t_env, T_B1 - 0.1))
    MD.ruta(lz, cam, RUTA_S, color=(255, 214, 84), frac=f, t=t, ancho=8.0, flecha=True)
    for i in range(4):
        u = max(0.0, min(0.999, f - 0.07 * i))
        if u > 0.01:
            x, y, v = MD.punto_ruta(cam, RUTA_S, u)
            MD.ejercito(lz, float(x), float(y), 6, bando="ins", t=t + i * 0.2, s=1.6, dir=1, semilla=i, bandera=(i == 0), polvo=False)
    kh = U.pop(t, t_hid - 0.1) * U.salida(t, t_jose - 0.2, 0.25)
    if kh > 0.01:
        MD.medallon(lz, 300, 460, 140, "hidalgo", t, emocion="serio", habla=1.0, k=kh, seed=2)
        U.llamada(lz, 300, 630, "Hidalgo", color=U.COL["morado"], px=42, k=kh, cola="arriba")
    km = U.pop(t, t_jose - 0.1)
    if km > 0.01:
        MD.medallon(lz, 1620, 460, 150, "morelos", t, emocion="serio", k=km, seed=3)
        U.llamada(lz, 1620, 640, "José María Morelos", color=U.COL["azul"], px=42, k=km, cola="arriba")
    k = U.pop(t, t_antes - 0.05) * U.salida(t, t_jose - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "antes de morir, Hidalgo lo envió…", color=U.COL["naranja"], px=64, k=k, cola=None)
    k = U.pop(t, t_lev - 0.1)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "a levantar el sur", color=U.COL["rojo"], px=88, k=k * U.repop(t, t_sur + 0.1), cola=None)
    MD.brujula(lz, W - 110, H - 120, 1.0)


# ------------------------------------------------------------------------------------------------ 2. HIJO DE UN CARPINTERO
@shot(T_B1, bg=lambda t: bg_grad((60, 40, 110), (160, 80, 130), mid=(106, 52, 124), ym=0.5), post=[GRAD], ent=("fundido", 0.5))
def mo_carpinteria(lz, t):
    I.luz(mul=(1.0, 0.96, 0.92), mix=(255, 170, 110), k=0.06)
    U.bokeh(lz, t, seed=51, n=12, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.20)
    iso = I.Iso(105, 112, 44, 5.0 + 0.05 * (t - T_B1), sx0=930, sy0=640)
    mk.carpinteria(lz, iso, t)
    m = I.Mundo()
    mk.amueblar_carpinteria(m, t)
    m.add(60, 130, 74, 144, 40, lambda lz, iso: G.persona(lz, iso, 68, 138, t, "campesino", dir=(0.2, -1), seed=9500, h=56, accion="trabaja", cara="serio"), fijo=False, clave=205)
    m.add(100, 124, 112, 136, 40, lambda lz, iso: G.persona(lz, iso, 106, 130, t, "nino", dir=(-0.3, -1), seed=9501, h=34, accion="trabaja", cara="alegre"), fijo=False, clave=240)
    # al decir «cura» el niño crece: aparece de sotana junto al padre
    if t > t_cura:
        k = e_back(prog(t, t_cura, t_cura + 0.5))
        m.add(150, 130, 166, 146, 40, lambda lz, iso: G.persona(lz, iso, 158, 138, t, "cura", dir=(-0.4, -1), seed=9502, h=56 * k, cara="serio"), fijo=False, clave=300)
    m.dibujar(lz, iso)
    for i in range(6):                                       # aserrín
        u = (t * 0.6 + i * 0.17) % 1.0
        qx, qy = iso.P(78 + 22 * i, 100, 30 - 28 * u)
        lz.relleno(circulo(float(qx), float(qy), 2.4 * iso.z / 3, 5), (240, 210, 160), alfa=0.8 * (1 - u), capa=2)
    k = U.pop(t, t_cura - 0.05) * U.salida(t, t_hijo - 0.1, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "Morelos era cura…", color=U.COL["morado"], px=82, k=k, cola=None)
    k = U.pop(t, t_hijo - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "…hijo de un carpintero", color=U.COL["naranja"], px=82, k=k * U.repop(t, t_carp + 0.1), cola=None)


# ------------------------------------------------------------------------------------------------ 3. UN GENIO MILITAR (mesa de guerra)
def _mapa_guerra(lz, t, k, x, y, w, h):
    with lz.capa(2):
        lz.relleno(rect_red(x - w / 2 + 12, y - h / 2 + 16, w, h, 14), (20, 10, 50), alfa=0.30)
        lz.relleno(rect_red(x - w / 2, y - h / 2, w, h, 12), (240, 224, 186))
        lz.relleno(rect_red(x - w / 2 + 16, y - h / 2 + 16, w - 32, h - 32, 8), (212, 226, 190))
        costa = np.array([[x - w / 2 + 16, y - 40], [x - w / 4, y - 70], [x, y - 20], [x + w / 4, y - 60], [x + w / 2 - 16, y - 20], [x + w / 2 - 16, y + h / 2 - 16], [x - w / 2 + 16, y + h / 2 - 16]])
        lz.relleno(costa, (150, 200, 232))
        for i in range(5):                                                       # montes dibujados
            mx, my = x - w / 2 + 120 + 150 * i, y - 100 + 40 * math.sin(i * 1.7)
            lz.relleno(np.array([[mx - 24, my + 14], [mx, my - 22], [mx + 24, my + 14]]), (176, 150, 120))
        # movimientos de tropas: flechas que avanzan y envuelven al enemigo (rojo) con el ejército (azul)
        for j, (a, b, col) in enumerate((((x - 260, y + 90), (x - 20, y + 20), (60, 110, 220)), ((x - 120, y + 140), (x + 120, y + 60), (60, 110, 220)), ((x + 300, y - 20), (x + 90, y + 20), (206, 70, 70)))):
            u = prog(t, t_genio + 0.2 * j, t_genio + 1.6 + 0.2 * j)
            p = np.array(a) + (np.array(b) - np.array(a)) * u
            lz.trazo(np.array([a, p]), col, 14, afinar=False, temblor=0.0, capa=2)
            d = np.array(b) - np.array(a)
            d = d / np.hypot(*d)
            n = np.array([-d[1], d[0]])
            lz.relleno(np.array([p + d * 26, p + n * 20, p - n * 20]), col)
        for j in range(8):
            lz.relleno(rect_red(x - 280 + 20 * (j % 4), y + 60 + 18 * (j // 4), 14, 14, 3), (60, 110, 220))
        for j in range(6):
            lz.relleno(rect_red(x + 220 + 20 * (j % 3), y - 40 + 18 * (j // 3), 14, 14, 3), (206, 70, 70))


@shot(T_B2, bg=lambda t: bg_grad((54, 30, 112), (150, 70, 130), mid=(100, 46, 130), ym=0.5), post=[GRAD], ent=("fundido", 0.4))
def mo_genio(lz, t):
    U.bokeh(lz, t, seed=52, n=14, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.24)
    U.haces_luz(lz, 560, 560, t, n=8, largo=1300, color=(255, 200, 240), alfa=0.10, ancho=0.09)
    U.chispas(lz, t, n=18, seed=53, tam=(5, 12))
    kv = U.pop(t, T_B2 + 0.05, 1.3)
    RT.retrato(lz, 480, 1010, 250 * (0.94 + 0.06 * kv), "morelos", t, emocion="serio", habla=0.0, mirar=0.4, seed=7, alfa=min(1.0, kv))
    km = U.pop(t, t_genio - 0.2, 1.2)
    if km > 0.01:
        _mapa_guerra(lz, t, km, 1240, 520, 1000, 560)
    k = U.pop(t, t_tal - 0.05) * U.salida(t, t_genio - 0.1, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2 + 200, 130, "un talento que nadie esperaba", color=U.COL["naranja"], px=62, k=k, cola=None)
    k = U.pop(t, t_genio - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2 + 200, 130, "¡un genio militar!", color=U.COL["rojo"], px=92, k=k * U.repop(t, t_mil + 0.1), cola=None)


# ------------------------------------------------------------------------------------------------ 4. BATALLA TRAS BATALLA (mapa)
RUTA_V = [(-99.50, 17.55), (-99.17, 17.60), (-98.47, 18.60), (-98.94, 18.81)]


def cam_c(t):
    return Klog(t, [(T_C, (-99.2, 18.2, 2.9)), (T_D, (-99.15, 18.2, 3.2))])


@shot(T_C, bg=lambda t: BASE(cam_c(t), t), post=[GRAD], ent=("zoom", 0.5))
def mo_batallas(lz, t):
    cam = cam_c(t)
    I.luz()
    MD.montes(lz, cam, min_alt=2200)
    MD.pais(lz, cam, "Mexico", (255, 96, 70), alfa=0.10, borde=(255, 220, 90), ancho=4.0, t=t, latido=1.0)
    for j, (lug, tp, nm, dx, dy, lado) in enumerate((("chilpancingo", "ciudad", "Chilpancingo", -130, 4, "der"), ((-99.17, 17.60), "pueblo", "Chilapa", 110, 40, "izq"), ((-98.47, 18.60), "pueblo", "Izúcar", 100, 4, "izq"), ("cuautla", "pueblo", "Cuautla", 100, 4, "izq"))):
        MD.ciudad(lz, cam, lug, t, T_C + 0.1 * j, tam=1.3, tipo=tp, bando="ins", semilla=j + 81)
        MD.etiqueta(lz, cam, lug, nm, t, T_C + 0.2 + 0.1 * j, px=22, dy=dy, dx=dx, lado=lado)
    f = e_inout(prog(t, T_C + 0.3, T_D - 0.3))
    MD.ruta(lz, cam, RUTA_V, color=(255, 214, 84), frac=f, t=t, ancho=8.0, flecha=True)
    for i in range(3):                                           # un ejército chico, en filas parejas
        u = max(0.0, min(0.999, f - 0.05 * i))
        if u > 0.01:
            x, y, v = MD.punto_ruta(cam, RUTA_V, u)
            MD.ejercito(lz, float(x), float(y), 8, bando="ins", t=t + i * 0.2, s=1.9, dir=1, semilla=i, bandera=(i == 0), polvo=(i == 0))
    # victorias: una insignia de batalla gana cada plaza
    for j, lug in enumerate(("chilpancingo", (-99.17, 17.60), (-98.47, 18.60), "cuautla")):
        MD.insignia_batalla(lz, cam, lug, t, T_C + 1.0 + 0.9 * j, s=1.1, color=(70, 190, 110))
    for (txt, col, tt_, dx, dy) in (("pequeño", U.COL["naranja"], t_peq, -330, 0), ("organizado", U.COL["azul"], t_org, 0, -80), ("disciplinado", U.COL["verde"], t_disc, 330, 0)):
        k = U.pop(t, tt_ - 0.05) * U.salida(t, t_gano - 0.2, 0.2)
        if k > 0.01:
            U.llamada(lz, W / 2 + dx, 780 + dy, txt, color=col, px=62, k=k * U.repop(t, tt_ + 0.3), cola=None)
    k = U.pop(t, t_ejer - 0.05) * U.salida(t, t_gano - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "un ejército…", color=U.COL["morado"], px=82, k=k, cola=None)
    k = U.pop(t, t_gano - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "batalla tras batalla", color=U.COL["verde"], px=92, k=k * U.repop(t, t_bat + 0.2), cola=None)
    MD.brujula(lz, W - 110, H - 120, 1.0)


# ------------------------------------------------------------------------------------------------ 5. EL SITIO DE CUAUTLA
def cam_d(t):
    return K(t, [(T_D, (200, 200, 40, 1.5)), (t_set, (200, 200, 40, 1.9)), (t_sitio, (200, 190, 40, 2.1)), (t_miles, (200, 190, 40, 2.3)), (T_E, (200, 190, 40, 2.4))])


@shot(T_D, bg=lambda t: bg_grad((130, 190, 240), (254, 232, 196), mid=(200, 218, 238), ym=0.5), post=[GRAD], ent=("fundido", 0.5))
def mo_cuautla(lz, t):
    cx, cy, cz, zm = cam_d(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz(mul=(1.03, 1.0, 0.96), mix=(255, 220, 160), k=0.05)
    CUA.suelo(lz, iso, t)
    m = CUA.objetos(t)
    # defensores tras las trincheras y la plaza; el anillo de soldados realistas en círculo
    for i in range(36):
        x, y = 70 + 260 * h01(211, i), 100 + 200 * h01(212, i)
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i: (lambda lz, iso: G.persona(lz, iso, x, y, t, ("insurgente", "campesino", "indigena", "insurgente_lanza", "mestizo", "honda")[i % 6], dir=(h01(213, i) - 0.5, h01(214, i) - 0.5), vel=0.5, seed=9600 + i, h=40, cara="enojo", accion="pelea" if i % 4 == 0 else None)))(x, y, i), fijo=False, clave=x + y + 3)
    for i in range(130):
        a = 2 * math.pi * (i / 130) + 0.03 * math.sin(t + i)
        r_x, r_y = 300 + 22 * h01(215, i), 250 + 20 * h01(216, i)
        x, y = 200 + r_x * math.cos(a), 200 + r_y * math.sin(a)
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i, a: (lambda lz, iso: G.persona(lz, iso, x, y, t, ("realista", "granadero", "dragon", "oficial")[i % 4], dir=(-math.cos(a), -math.sin(a)), vel=0.0, seed=9700 + i, h=42, cara="serio", accion="pelea" if i % 9 == 0 else None)))(x, y, i, a), fijo=False, clave=x + y + 3)
    m.dibujar(lz, iso)
    for i in range(8):                                       # cañonazos hacia la plaza: fogonazos y humo
        a = 2 * math.pi * (i + 0.5) / 8
        td = (t * 0.9 + 0.17 * i) % 1.3
        qx, qy = iso.P(200 + 290 * math.cos(a), 200 + 236 * math.sin(a), 18)
        if td < 0.22:
            U.chispa4(lz, float(qx), float(qy), 20 * (1 - td * 4), color=(255, 226, 140), alfa=0.9)
        O.humo(lz, iso, 200 + 290 * math.cos(a), 200 + 236 * math.sin(a), 24, t + i, n=3, s=1.2, color=(214, 210, 222), alfa=0.5, seed=i)
    DC.aves(lz, t, n=6, seed=91, y0=50, y1=200)
    # el reloj de los días: contador de 0 a 72 con la luz del día que pasa rápido
    kd = U.pop(t, t_res - 0.05) * U.salida(t, T_E - 0.25, 0.25)
    if kd > 0.01:
        dias = int(72 * smooth(prog(t, t_set - 0.1, t_dias + 0.6)))
        P.rotulo(lz, 330, 320, f"{dias}", px=200, k=kd, color=(255, 255, 255))
        U.llamada(lz, 330, 470, "días de sitio", color=U.COL["rojo"], px=58, k=kd * U.repop(t, t_dias + 0.1), cola=None)
    k = U.pop(t, t_1812 - 0.05) * U.salida(t, t_res - 0.15, 0.2)
    if k > 0.01:
        U.fecha_lugar(lz, t, T_D + 0.1, t_res, "Cuautla, Morelos", "1812", y=70)
    k = U.pop(t, t_rod - 0.05) * U.salida(t, T_E - 0.25, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2 + 280, 130, "rodeado por miles de soldados", color=U.COL["naranja"], px=60, k=k * U.repop(t, t_miles + 0.1), cola=None)
    k = U.pop(t, t_sitio - 0.05) * U.salida(t, t_rod - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2 + 280, 130, "el sitio de Cuautla", color=U.COL["morado"], px=72, k=k * U.repop(t, t_cuautla + 0.1), cola=None)


# ------------------------------------------------------------------------------------------------ 6. LA SALIDA DE NOCHE
def cam_e(t):
    return K(t, [(T_E, (200, 200, 40, 2.5)), (t_noche, (240, 240, 40, 2.4)), (t_salvo, (280, 300, 40, 2.1)), (T_F, (290, 310, 40, 2.1))])


@shot(T_E, bg=lambda t: bg_grad((10, 12, 52), (58, 46, 112), mid=(28, 28, 90), ym=0.45), post=[lambda img, t: U.gradacion(img, luces=(1.0, 0.98, 1.04), sombras=(0.92, 0.94, 1.08), saturacion=1.04)], ent=("fundido", 0.6))
def mo_noche(lz, t):
    cx, cy, cz, zm = cam_e(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz(mul=(0.70, 0.76, 1.0), mix=(30, 34, 100), k=0.28)
    for i in range(70):
        x, y = (h01(14, i, 1) * 2000) % 1920, (h01(14, i, 2) * 560)
        lz.relleno(circulo(x, y, 1.6 + 2.0 * h01(14, i, 3), 6), (255, 244, 210), alfa=0.4 + 0.4 * math.sin(t * 2 + i), capa=0)
    lz.halo(1500, 160, 260, (150, 170, 255), alfa=0.35, capa=0)
    lz.relleno(circulo(1500, 160, 62, 28), (242, 246, 255), capa=0)
    CUA.suelo(lz, iso, t)
    m = CUA.objetos(t)
    # los realistas vigilan (algunos dormitan: zZz); los insurgentes salen en fila por un hueco del cerco hacia el sureste
    RUTA = [(200, 230), (240, 290), (300, 350), (350, 410), (420, 470)]
    p = np.asarray(RUTA, float)
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(p, axis=0).T))]
    for i in range(64):
        s = (t - (t_noche - 0.8)) * 34 - 9.0 * i
        if s <= 0:
            x, y = 130 + 140 * h01(221, i), 150 + 100 * h01(222, i)
            dr, run = (0.5, 1), 0.0
        else:
            s2 = min(s, d[-1] - 1)
            j = int(np.clip(np.searchsorted(d, s2, side="right") - 1, 0, len(p) - 2))
            f = (s2 - d[j]) / (d[j + 1] - d[j])
            q = p[j] + (p[j + 1] - p[j]) * f
            x, y = float(q[0]) + 6 * (h01(223, i) - 0.5), float(q[1]) + 6 * (h01(224, i) - 0.5)
            dr, run = (p[j + 1] - p[j]) / np.hypot(*(p[j + 1] - p[j])), 1.2
        al = 1.0
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i, dr, run: (lambda lz, iso: G.persona(lz, iso, x, y, t, ("insurgente", "campesino", "indigena", "mestizo", "indigena_f", "insurgente_lanza")[i % 6], dir=(float(dr[0]), float(dr[1])), vel=run, seed=9800 + i, h=40, cara="miedo" if run else "normal")))(x, y, i, dr, run), fijo=False, clave=x + y + 3)
    for i in range(22):                                     # guardias del cerco (centinelas con antorcha)
        a = 2 * math.pi * i / 22
        x, y = 200 + 290 * math.cos(a), 200 + 240 * math.sin(a)
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i, a: (lambda lz, iso: (G.persona(lz, iso, x, y, t, "realista", dir=(math.sin(a), -math.cos(a)), vel=0.0, seed=9900 + i, h=42, cara="normal"), O.antorcha(lz, iso, x + 5, y + 2, t, h=26, seed=i))))(x, y, i, a), fijo=False, clave=x + y + 3)
    m.dibujar(lz, iso)
    for i in range(0, 22, 3):
        a = 2 * math.pi * i / 22
        qx, qy = iso.P(200 + 290 * math.cos(a), 200 + 240 * math.sin(a), 40)
        U.globo(lz, float(qx), float(qy) - 30, "zZz", px=26, k=U.pop(t, t_comida + 0.1 * (i % 3)) * U.salida(t, t_saco + 0.6, 0.2)) if (i % 6 == 0) else None
        lz.halo(float(qx), float(qy), 70 * iso.z / 3.0, (255, 168, 84), alfa=0.20, capa=2)
    k = U.pop(t, t_cuando - 0.05) * U.salida(t, t_saco - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "ya no quedaba comida", color=U.COL["rojo"], px=78, k=k, cola=None)
        qx, qy = iso.P(200, 200, 0)
        lz.relleno(circulo(float(qx), 900, 70 * k, 20), (60, 50, 60), alfa=0.9, capa=2)
        lz.relleno(circulo(float(qx), 900, 54 * k, 20), (30, 26, 36), alfa=0.9, capa=2)
    k = U.pop(t, t_saco - 0.05) * U.salida(t, t_noche - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "saca a todos sus hombres", color=U.COL["naranja"], px=76, k=k, cola=None)
    k = U.pop(t, t_noche - 0.05) * U.salida(t, t_salvo - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "en plena noche", color=U.COL["morado"], px=86, k=k * U.repop(t, t_noche + 0.2), cola=None)
    k = U.pop(t, t_salvo - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "¡y los salva!", color=U.COL["verde"], px=96, k=k * U.repop(t, t_salvo + 0.2), cola=None)


# ------------------------------------------------------------------------------------------------ 7. MATAMOROS Y GALEANA
@shot(T_F, bg=lambda t: bg_grad((54, 30, 112), (150, 70, 130), mid=(100, 46, 130), ym=0.5), post=[GRAD], ent=("fundido", 0.5))
def mo_aliados(lz, t):
    U.bokeh(lz, t, seed=55, n=14, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.24)
    U.haces_luz(lz, W / 2, 500, t, n=8, largo=1300, color=(255, 200, 240), alfa=0.10, ancho=0.09)
    for (q, lab, tt_, x, col) in (("morelos", "Morelos", T_F, 960, U.COL["azul"]), ("matamoros", "Mariano Matamoros", t_mat, 400, U.COL["naranja"]), ("galeana", "Hermenegildo Galeana", t_gal, 1520, U.COL["verde"])):
        k = U.pop(t, tt_ - 0.05 if tt_ != T_F else T_F + 0.05, 1.2) * U.salida(t, T_F2 - 0.1, 0.25)
        if k > 0.01:
            s = 210 if q == "morelos" else 165
            RT.retrato(lz, x, 1020 if q == "morelos" else 990, s * (0.94 + 0.06 * k), q, t, emocion="serio", mirar=0.0 if q == "morelos" else (0.5 if x < 960 else -0.5), seed=5, alfa=min(1.0, k))
            U.llamada(lz, x, 190, lab, color=col, px=46, k=k, cola=None)
    k = U.pop(t, t_junto - 0.05) * U.salida(t, T_F2 - 0.1, 0.25)
    if k > 0.01:
        U.llamada(lz, W / 2, 980, "peleaban junto a él", color=U.COL["rojo"], px=64, k=k, cola=None)


# ------------------------------------------------------------------------------------------------ 8. LEONA VICARIO (mapa)
RUTA_L = [(-99.13, 19.43), (-99.05, 19.20), (-98.94, 18.81)]


def cam_f2(t):
    return Klog(t, [(T_F2, (-99.05, 19.1, 3.6)), (T_G, (-99.05, 19.1, 4.0))])


@shot(T_F2, bg=lambda t: BASE(cam_f2(t), t), post=[GRAD], ent=("zoom", 0.5))
def mo_leona(lz, t):
    cam = cam_f2(t)
    I.luz()
    MD.montes(lz, cam, min_alt=2200)
    MD.pais(lz, cam, "Mexico", (255, 96, 70), alfa=0.10, borde=(255, 220, 90), ancho=4.0, t=t, latido=1.0)
    MD.ciudad(lz, cam, "mexico", t, T_F2, tam=1.7, tipo="ciudad", bando="real", nombre="Ciudad de México", px=24, semilla=3)
    MD.ciudad(lz, cam, "cuautla", t, T_F2 + 0.1, tam=1.5, tipo="pueblo", bando="ins", nombre="Cuautla", px=24, semilla=5)
    pm = np.array([float(v) for v in MP.proy(cam, -99.13, 19.43)])
    pc = np.array([float(v) for v in MP.proy(cam, -98.94, 18.81)])
    f = e_inout(prog(t, t_info - 0.3, t_dinero + 1.0))
    # la espía manda cartas y bolsas de dinero por mensajeros a caballo que cruzan el cerco
    for j in range(4):
        u = ((t - t_info) * 0.35 + j * 0.25) % 1.0 if t > t_info - 0.3 else -1
        if u >= 0:
            p = pm + (pc - pm) * u + np.array([0.0, 14.0 * math.sin(u * 6)])
            mi_ = ((j % 2) == 0)
            lz.trazo(np.array([pm, pc]), (255, 255, 255), 4, afinar=False, temblor=0.0, capa=2) if j == 0 else None
            if mi_:
                lz.relleno(rect_red(p[0] - 16, p[1] - 12, 32, 22, 3), (252, 246, 232), capa=2)
                lz.relleno(np.array([[p[0] - 16, p[1] - 12], [p[0], p[1]], [p[0] + 16, p[1] - 12]]), (222, 210, 190), capa=2)
                lz.relleno(circulo(p[0], p[1] - 2, 5, 8), (206, 60, 70), capa=2)
            else:
                lz.relleno(circulo(p[0], p[1] - 6, 14, 14), (222, 196, 120), capa=2)
                lz.relleno(rect_red(p[0] - 5, p[1] - 22, 10, 8, 3), (190, 150, 80), capa=2)
                P.rotulo(lz, p[0], p[1] - 6, "$", px=18, k=1.0, color=(110, 80, 40), sombra=0.0)
    kl = U.pop(t, t_leona - 0.2)
    if kl > 0.01:
        MD.medallon(lz, 330, 470, 150, "leona", t, emocion="neutro", k=kl, seed=6)
        U.llamada(lz, 330, 650, "Leona Vicario", color=U.COL["rojo"], px=46, k=kl, cola="arriba")
    k = U.pop(t, t_capital - 0.1) * U.salida(t, t_espia - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "…desde la capital", color=U.COL["azul"], px=80, k=k, cola=None)
    k = U.pop(t, t_espia - 0.05) * U.salida(t, t_info - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "la espía", color=U.COL["rojo"], px=96, k=k * U.repop(t, t_espia + 0.2), cola=None)
    k = U.pop(t, t_info - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2 - 260, 130, "información", color=U.COL["naranja"], px=72, k=k, cola=None)
        U.llamada(lz, W / 2 + 260, 130, "y dinero", color=U.COL["verde"], px=72, k=U.pop(t, t_dinero - 0.05), cola=None)
    MD.brujula(lz, W - 110, H - 120, 1.0)


# ------------------------------------------------------------------------------------------------ 9. OAXACA, ACAPULCO Y MEDIO SUR (mapa)
SUR_POLI = [(-102.2, 17.9), (-100.6, 18.6), (-99.2, 19.0), (-98.0, 19.0), (-96.9, 18.4), (-95.6, 17.4), (-96.4, 15.9), (-98.4, 16.4), (-100.8, 16.9)]


def cam_g(t):
    return Klog(t, [(T_G, (-99.2, 18.0, 2.2)), (t_aca, (-99.0, 17.6, 2.1)), (t_control, (-98.8, 17.6, 1.8)), (T1(E10), (-98.6, 17.6, 1.6))])


@shot(T_G, bg=lambda t: BASE(cam_g(t), t), post=[GRAD], ent=("zoom", 0.5))
def mo_conquistas(lz, t):
    cam = cam_g(t)
    I.luz()
    MD.montes(lz, cam, min_alt=2200)
    MD.pais(lz, cam, "Mexico", (255, 96, 70), alfa=0.08, borde=(255, 220, 90), ancho=4.0, t=t, latido=0.0)
    # territorio insurgente del sur: un polígono verde translúcido que crece desde Cuautla
    g = smooth(prog(t, t_tomo, t_pais + 0.6))
    cxm, cym = (np.array([float(v) for v in MP.proy(cam, -98.94, 18.81)]))
    pts = np.array([[float(v) for v in MP.proy(cam, lo, la)] for lo, la in SUR_POLI])
    pts = np.array([cxm, cym]) + (pts - np.array([cxm, cym])) * g
    if g > 0.02:
        lz.relleno(pts, (70, 200, 120), alfa=0.28 * min(1.0, g * 1.5), capa=2)
        lz.trazo(np.vstack([pts, pts[:1]]), (140, 255, 170), 6.0, afinar=False, temblor=0.0, capa=2)
    for j, (lug, tp, nm, dx, dy, lado, tt_) in enumerate((("cuautla", "pueblo", "Cuautla", 110, 4, "izq", T_G), ("oaxaca", "ciudad", "Oaxaca", 120, 4, "izq", t_oax), ("acapulco", "puerto", "Acapulco", 130, 4, "izq", t_aca), ("chilpancingo", "ciudad", "Chilpancingo", -130, 4, "der", T_G))):
        MD.ciudad(lz, cam, lug, t, T_G + 0.1 * j, tam=1.4, tipo=tp, bando=(255, 206, 70) if tt_ > T_G + 0.5 else "ins", semilla=j + 91)
        MD.etiqueta(lz, cam, lug, nm, t, T_G + 0.2 + 0.1 * j, px=22, dy=dy, dx=dx, lado=lado)
        if tt_ > T_G + 0.5:
            MD.insignia_batalla(lz, cam, lug, t, tt_ - 0.1, s=1.1, color=(70, 190, 110))
    for (a, b, tt_) in (((-98.94, 18.81), (-96.7, 17.06), t_oax), ((-98.94, 18.81), (-99.89, 16.85), t_aca)):
        MD.ruta(lz, cam, [a, b], color=(255, 214, 84), frac=e_inout(prog(t, tt_ - 0.7, tt_ + 0.2)), t=t, ancho=8.0, flecha=True)
    k = U.pop(t, t_poco - 0.05) * U.salida(t, t_tomo - 0.1, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "en poco tiempo…", color=U.COL["azul"], px=84, k=k, cola=None)
    k = U.pop(t, t_tomo - 0.05) * U.salida(t, t_control - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "toma Oaxaca y Acapulco", color=U.COL["naranja"], px=78, k=k * U.repop(t, t_aca + 0.1), cola=None)
    k = U.pop(t, t_control - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "controla buena parte del sur", color=U.COL["verde"], px=76, k=k * U.repop(t, t_sur2 + 0.1), cola=None)
    MD.brujula(lz, W - 110, H - 120, 1.0)


# ------------------------------------------------------------------------------------------------ sonido
snd(T_A + 0.2, "whoosh", 0.3, dur=1.0)
snd(t_hid, "pop", 0.4)
snd(t_jose, "pop", 0.4)
snd(t_env, "galope", 0.4, dur=1.8)
snd(t_lev, "gong", 0.4)
snd(T_B1, "pop", 0.3)
for _i in range(6):
    snd(T_B1 + 0.4 + 0.45 * _i, "bonk", 0.2)
snd(t_cura, "bling", 0.4)
snd(T_B2, "whoosh", 0.3, dur=0.9)
snd(t_genio, "bling", 0.5)
snd(T_C, "whoosh", 0.3, dur=0.9)
for _j in range(4):
    snd(T_C + 1.0 + 0.9 * _j, "pluck", 0.4)
snd(T_D, "pop", 0.3)
for _k in range(8):
    snd(T_D + 0.8 + 1.0 * _k, "canonazo", 0.3)
snd(t_set, "gong", 0.4)
snd(T_E, "amanecer", 0.2, dur=2.0)
snd(t_noche, "pluck", 0.4)
snd(t_salvo, "bling", 0.5)
snd(T_F, "pop", 0.3)
snd(t_mat, "pop", 0.3)
snd(t_gal, "pop", 0.3)
snd(T_F2, "whoosh", 0.3, dur=0.9)
snd(t_leona, "pop", 0.4)
snd(t_dinero, "monedas", 0.4)
snd(T_G, "whoosh", 0.3, dur=0.9)
snd(t_oax, "gong", 0.4)
snd(t_aca, "gong", 0.4)
snd(t_control, "bling", 0.5)
