# -*- coding: utf-8 -*-
"""Escena 17 · Después de la independencia (9:45-10:21): los problemas que quedaron, el imperio de Iturbide, la República de Victoria, Guerrero y el fin de la esclavitud, su fusilamiento, los héroes caídos y un país por construir."""
import math

import numpy as np

import kz_iso as I
from kz_iso import tint
import kz_iso_obj2 as O2
import kz_gente_iso as G
import kz_retrato as RT
import kz_ui as U
import kz_mapa as KM
import kz_mapa_dib as MD
import plano as P
from motor import W, H, prog, lerp, smooth, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, h01, catmull
from reg import shot, snd
from util import *  # noqa: F401,F403
import mundos_l as ml
import t01
import t09 as T9

E17 = "despues"
MP = KM.MAPA
GRAD = lambda img, t: U.gradacion(img)
GRIS = T9.GRIS
BASE = lambda cam, t: MP.base(cam, t, exag=13.0, rios_umbral=0.7)
PURP = lambda t: bg_grad((54, 30, 112), (150, 70, 130), mid=(100, 46, 130), ym=0.5)
PURPG = lambda t: bg_grad((40, 34, 70), (96, 70, 100), mid=(64, 50, 84), ym=0.55)

# ------------------------------------------------------------------ anclas
t_pero, t_indep, t_resol, t_todos, t_probl = [T(E17, w, frase=0) for w in ("pero", "independencia", "resolvio", "todos", "problemas")]
t_itu, t_coron, t_emp, t_dur, t_menos, t_ano, t_1824, t_nacio, t_rep, t_vic, t_pres = [T(E17, w, frase=1) for w in ("iturbide", "corono", "emperador", "duro", "menos", "ano", "veinticuatro", "nacio", "republica", "victoria", "presidente")]
t_guer, t_lleg, t_presid, t_1829, t_abol, t_defin, t_escl = [T(E17, w, frase=2) for w in ("guerrero", "llego", "presidencia", "veintinueve", "abolio", "definitivamente", "esclavitud")]
t_dos, t_desp, t_enem, t_capt, t_trai, t_fus = [T(E17, w, frase=3) for w in ("dos", "despues", "enemigos", "capturaron", "traicion", "fusilaron")]
t_hero, t_cas, t_term, t_misma, t_man = [T(E17, w, frase=4) for w in ("heroes", "casi", "terminaron", "misma", "manera")]
t_mex, t_emp2, t_pais, t_terr, t_enor, t_sin, t_din, t_ideas, t_dist, t_gob = [T(E17, w, frase=5) for w in ("mexico", "empezaba", "pais", "territorio", "enorme", "sin", "dinero", "ideas", "distintas", "gobernarse")]
T_A, T_B1, T_B2, T_C, T_D1, T_D2, T_E, T_F1, T_F2 = T0(E17), t_itu - 0.2, t_1824 - 0.2, t_guer - 0.2, t_dos - 0.15, t_fus - 0.3, t_hero - 0.15, t_mex - 0.2, t_sin - 0.2


# ------------------------------------------------------------------------------------------------ 1. LOS PROBLEMAS QUE QUEDARON
def cam_a(t):
    return Klog(t, [(T_A, (-102.0, 23.0, 1.1)), (T_B1, (-102.0, 22.5, 1.25))])


@shot(T_A, bg=lambda t: BASE(cam_a(t), t), post=[lambda img, t: U.gradacion(img, luces=(0.98, 0.98, 1.0), sombras=(0.92, 0.94, 1.04), saturacion=0.85)], ent=("fundido", 0.5))
def de_problemas(lz, t):
    cam = cam_a(t)
    I.luz(mul=(0.95, 0.96, 1.0), mix=(40, 44, 100), k=0.12 * smooth(prog(t, t_resol, T_B1)))
    MD.montes(lz, cam, min_alt=2200)
    MD.pais(lz, cam, "Mexico", (70, 200, 120), alfa=0.22, borde=(150, 255, 180), ancho=6.0, t=t, latido=1.0)
    for lug, nm, dx in (("mexico", "Ciudad de México", 0), ("guadalajara", "Guadalajara", 130), ("veracruz", "Veracruz", 120), ("zacatecas", "Zacatecas", 120)):
        MD.ciudad(lz, cam, lug, t, T_A + 0.1, tam=1.5, tipo="ciudad", bando=(70, 190, 110), semilla=3)
    # nubes de tormenta sobre varias regiones: los problemas por resolver
    for j, ((lo, la), s) in enumerate((((-99.1, 19.4), 2.2), ((-103.3, 20.7), 1.8), ((-101.0, 25.0), 2.0), ((-96.5, 17.5), 1.7), ((-90.5, 20.0), 1.5))):
        k = U.pop(t, t_resol - 0.3 + 0.18 * j)
        if k > 0.01:
            sx, sy = MP.proy(cam, lo, la)
            O2.nube_tormenta(lz, float(sx), float(sy) - 110, s * k, t + j * 1.3, relampago=max(0.0, 1.0 - ((t - t_resol + 0.25 * j) % 2.0) * 5))
    k = U.pop(t, t_pero - 0.05) * U.salida(t, t_resol - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "pero la independencia…", color=U.COL["azul"], px=84, k=k, cola=None)
    k = U.pop(t, t_resol - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "no resolvió todos los problemas", color=U.COL["rojo"], px=72, k=k * U.repop(t, t_probl + 0.1), cola=None)
    MD.brujula(lz, W - 110, H - 120, 1.0)


# ------------------------------------------------------------------------------------------------ 2a. ITURBIDE EMPERADOR (menos de un año)
@shot(T_B1, bg=PURP, post=[GRAD], ent=("fundido", 0.5))
def de_imperio(lz, t):
    U.bokeh(lz, t, seed=131, n=14, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.24)
    U.haces_luz(lz, 560, 560, t, n=8, largo=1300, color=(255, 200, 240), alfa=0.10, ancho=0.09)
    kv = U.pop(t, T_B1 + 0.05, 1.3)
    RT.retrato(lz, 520, 1010, 235 * (0.94 + 0.06 * kv), "iturbide", t, emocion="serio", mirar=0.2, seed=7, alfa=min(1.0, kv))
    kc = e_out(prog(t, t_coron - 0.3, t_coron + 0.5))
    if kc > 0.01:                                           # la corona baja sobre su cabeza
        import kz_mapa_dib as MD2
        MD2.corona(lz, 520, lerp(130, 320, kc), 5.0, 1.0, t)
        lz.halo(520, lerp(130, 320, kc), 320, (255, 224, 130), alfa=0.35, capa=2)
    # doce meses: el reinado cubre apenas diez y se rompe
    for i in range(12):
        k = U.pop(t, t_dur - 0.1 + 0.05 * i)
        if k > 0.01:
            x = 960 + 150 * (i % 6)
            y = 520 + 170 * (i // 6)
            vivo = i < 10
            caido = t > t_ano + 0.2 and i >= 9
            col = (255, 214, 72) if vivo else (80, 70, 110)
            lz.relleno(rect_red(x - 60 * k, y - 60 * k + (60 * (t - t_ano - 0.2) ** 2 if caido else 0), 120 * k, 120 * k, 16), col, alfa=0.35 if caido else 1.0, capa=2)
            P.rotulo(lz, x, y + (60 * (t - t_ano - 0.2) ** 2 if caido else 0), "ENE FEB MAR ABR MAY JUN JUL AGO SEP OCT NOV DIC".split()[i], px=40, k=k, color=(60, 40, 90), sombra=0.0)
    k = U.pop(t, t_coron - 0.05) * U.salida(t, t_dur - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2 + 300, 130, "se coronó emperador", color=U.COL["naranja"], px=78, k=k * U.repop(t, t_emp + 0.1), cola=None)
    k = U.pop(t, t_dur - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2 + 300, 130, "duró menos de un año", color=U.COL["rojo"], px=78, k=k * U.repop(t, t_ano + 0.1), cola=None)
    U.llamada(lz, 520, 190, "Agustín de Iturbide", color=U.COL["morado"], px=44, k=kv, cola=None)


# ------------------------------------------------------------------------------------------------ 2b. LA REPÚBLICA (1824)
@shot(T_B2, bg=lambda t: bg_grad((110, 150, 230), (252, 226, 200), mid=(196, 190, 236), ym=0.55), post=[GRAD], ent=("fundido", 0.5))
def de_republica(lz, t):
    U.chispas(lz, t, n=16, seed=132, tam=(5, 12))
    k = U.pop(t, t_nacio - 0.2, 1.3)
    if k > 0.01:
        t01.emblema(lz, 520, 700, 3.0 * k, t)
    kv = U.pop(t, t_vic - 0.1, 1.3)
    if kv > 0.01:
        RT.retrato(lz, 1460, 1010, 215 * (0.94 + 0.06 * kv), "victoria", t, emocion="serio", mirar=-0.2, seed=8, alfa=min(1.0, kv))
        U.llamada(lz, 1460, 250, "Guadalupe Victoria", color=U.COL["verde"], px=48, k=kv, cola=None)
    P.rotulo(lz, 520, 230, "1824", px=int(190 * (0.9 + 0.1 * U.pop(t, T_B2 + 0.1))), k=U.pop(t, T_B2 + 0.1), color=(255, 214, 72))
    k = U.pop(t, t_nacio - 0.05) * U.salida(t, t_vic - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 960, "nace la República", color=U.COL["naranja"], px=84, k=k * U.repop(t, t_rep + 0.1), cola=None)
    k = U.pop(t, t_vic - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 960, "su primer presidente", color=U.COL["verde"], px=80, k=k * U.repop(t, t_pres + 0.1), cola=None)


# ------------------------------------------------------------------------------------------------ 3. GUERRERO ABOLE LA ESCLAVITUD (1829)
@shot(T_C, bg=lambda t: bg_grad((54, 30, 112), (150, 70, 130), mid=(100, 46, 130), ym=0.5), post=[GRAD], ent=("fundido", 0.5))
def de_guerrero(lz, t):
    U.bokeh(lz, t, seed=133, n=12, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.22)
    kv = U.pop(t, T_C + 0.05, 1.3)
    RT.retrato(lz, 470, 1010, 235 * (0.94 + 0.06 * kv), "guerrero", t, emocion="serio", mirar=0.3, seed=9, alfa=min(1.0, kv))
    U.llamada(lz, 470, 190, "Vicente Guerrero", color=U.COL["azul"], px=46, k=kv, cola=None)
    rota = e_out(prog(t, t_abol, t_abol + 0.9))
    ml.cadena(lz, 1330, 560, n=7, t=t, rota=rota, ancho=96)
    if rota > 0.3:
        U.chispas(lz, t, n=24, seed=134, tam=(6, 14))
        lz.halo(1330, 560, 420 * rota, (255, 226, 150), alfa=0.35 * rota, capa=0)
    kd = U.pop(t, t_1829 - 0.1)
    if kd > 0.01:
        P.rotulo(lz, 1330, 260, "1829", px=int(170 * (0.9 + 0.1 * kd)), k=kd, color=(255, 214, 72))
    k = U.pop(t, t_guer - 0.05) * U.salida(t, t_abol - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2 + 300, 960, "llega a la presidencia", color=U.COL["naranja"], px=76, k=k * U.repop(t, t_presid + 0.1), cola=None)
    k = U.pop(t, t_abol - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2 + 300, 960, "abole definitivamente la esclavitud", color=U.COL["verde"], px=62, k=k * U.repop(t, t_escl + 0.1), cola=None)


# ------------------------------------------------------------------------------------------------ 4. TRAICIÓN Y FUSILAMIENTO (sobrio)
RUTA_G = [(-99.89, 16.85), (-98.0, 16.0), (-96.9, 16.4), (-96.8, 17.0)]


def cam_d1(t):
    return Klog(t, [(T_D1, (-98.6, 16.8, 2.4)), (T_D2, (-98.4, 16.7, 2.7))])


@shot(T_D1, bg=lambda t: BASE(cam_d1(t), t), post=[GRIS], ent=("fundido", 0.5))
def de_traicion(lz, t):
    cam = cam_d1(t)
    I.luz(mul=(0.94, 0.95, 1.0), mix=(40, 44, 100), k=0.12)
    MD.montes(lz, cam, min_alt=2200)
    MD.mar_vivo(lz, cam, t, seed=23)
    MD.pais(lz, cam, "Mexico", (255, 96, 70), alfa=0.06, borde=(255, 220, 90), ancho=4.0, t=t, latido=0.0)
    MD.ciudad(lz, cam, "acapulco", t, T_D1, tam=1.6, tipo="puerto", bando="real", nombre="Acapulco", px=24, semilla=3)
    MD.ciudad(lz, cam, "oaxaca", t, T_D1 + 0.1, tam=1.6, tipo="ciudad", bando="real", nombre="Oaxaca", px=24, semilla=5)
    f = e_inout(prog(t, t_capt - 0.3, T_D2 - 0.1))
    MD.ruta(lz, cam, RUTA_G, color=(210, 210, 226), frac=f, t=t, ancho=7.0, flecha=False)
    x, y, v = MD.punto_ruta(cam, RUTA_G, max(0.01, f))
    MD.barco_plano(lz, float(x), float(y) - 10, 1.5, t, dir=1)
    kv = U.pop(t, t_dos - 0.1) * U.salida(t, T_D2 - 0.2, 0.25)
    if kv > 0.01:
        MD.medallon(lz, 1620, 450, 140, "guerrero", t, emocion="serio", k=kv, seed=5)
        P.rotulo(lz, 330, 200, "1831", px=int(190 * (0.9 + 0.1 * kv)), k=kv, color=(255, 214, 72))
    k = U.pop(t, t_enem - 0.05) * U.salida(t, t_trai - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "sus enemigos lo capturan…", color=U.COL["rojo"], px=76, k=k, cola=None)
    k = U.pop(t, t_trai - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "por traición", color=U.COL["rojo"], px=104, k=k * U.repop(t, t_trai + 0.2), cola=None)
    MD.brujula(lz, W - 110, H - 120, 1.0)


@shot(T_D2, bg=PURPG, post=[GRIS], ent=("fundido", 0.5))
def de_guerrero_fin(lz, t):
    U.haces_luz(lz, W / 2, 380, t, n=7, largo=1300, color=(220, 200, 255), alfa=0.08, ancho=0.09)
    k = U.pop(t, T_D2 + 0.05, 1.2)
    fus = e_out(prog(t, t_fus, t_fus + 0.6))
    RT.retrato(lz, W / 2, 1000, 230 * (0.94 + 0.06 * k), "guerrero", t, emocion="serio", alfa=min(1.0, k) * (1 - 0.5 * fus), luz_borde=(220, 200, 255))
    if fus > 0.01:
        lz.relleno(np.array([[W / 2 - 220, 520], [W / 2 - 170, 480], [W / 2 + 230, 880], [W / 2 + 180, 930]]), (14, 12, 22), alfa=0.85 * fus, capa=2)
    U.llamada(lz, W / 2, 140, "Vicente Guerrero", color=U.COL["azul"], px=56, k=k, cola=None)
    kk = U.pop(t, t_fus - 0.05)
    if kk > 0.01:
        U.llamada(lz, W / 2, 250, "fusilado en 1831", color=U.COL["rojo"], px=78, k=kk * U.repop(t, t_fus + 0.2), cola=None)


# ------------------------------------------------------------------------------------------------ 5. LOS HÉROES CAEN, CASI TODOS IGUAL
@shot(T_E, bg=PURPG, post=[GRIS], ent=("fundido", 0.6))
def de_heroes(lz, t):
    U.haces_luz(lz, W / 2, 360, t, n=8, largo=1300, color=(220, 200, 255), alfa=0.08, ancho=0.09)
    heroes = (("hidalgo", "Hidalgo"), ("allende", "Allende"), ("aldama", "Aldama"), ("morelos", "Morelos"), ("matamoros", "Matamoros"), ("mina", "Mina"), ("guerrero", "Guerrero"))
    for i, (q, lab) in enumerate(heroes):
        x = 150 + 270 * i
        k = U.pop(t, t_hero - 0.1 + 0.2 * i, 1.2)
        if k > 0.01:
            cae = e_out(prog(t, t_term - 0.2 + 0.18 * i, t_term + 0.5 + 0.18 * i))
            RT.retrato(lz, x, 800, 78 * (0.94 + 0.06 * k), q, t, emocion="serio", alfa=min(1.0, k) * (1 - 0.5 * cae), seed=i + 2, luz_borde=(220, 200, 255))
            U.llamada(lz, x, 520, lab, color=U.COL["morado"], px=34, k=k, cola=None)
            if cae > 0.01:
                lz.relleno(np.array([[x - 100, 650], [x - 70, 625], [x + 110, 800], [x + 80, 830]]), (14, 12, 22), alfa=0.85 * cae, capa=2)
    k = U.pop(t, t_hero - 0.05) * U.salida(t, t_term - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 200, "los héroes de la independencia…", color=U.COL["naranja"], px=70, k=k, cola=None)
    k = U.pop(t, t_term - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 200, "casi todos terminaron de la misma manera", color=U.COL["rojo"], px=66, k=k * U.repop(t, t_man + 0.1), cola=None)


# ------------------------------------------------------------------------------------------------ 6. UN PAÍS POR CONSTRUIR
TERRITORIO_N = [(-117.1, 32.5), (-114.7, 32.7), (-109.0, 31.3), (-106.5, 31.8), (-104.0, 29.5), (-99.5, 27.0), (-97.2, 26.0), (-94.0, 29.7), (-94.0, 33.0), (-100.0, 36.5), (-103.0, 37.0), (-109.0, 37.0), (-114.0, 37.0), (-120.0, 39.0), (-124.4, 42.0), (-124.0, 38.0), (-120.6, 34.5)]


def cam_f1(t):
    return Klog(t, [(T_F1, (-104.0, 27.0, 0.62)), (T_F2, (-104.0, 27.0, 0.7))])


@shot(T_F1, bg=lambda t: MP.base(cam_f1(t), t, exag=9.0, rios_umbral=2.0), post=[GRAD], ent=("fundido", 0.5))
def de_pais(lz, t):
    cam = cam_f1(t)
    I.luz()
    MD.pais(lz, cam, "Mexico", (70, 200, 120), alfa=0.30, borde=(150, 255, 180), ancho=6.0, t=t, latido=1.0)
    g = e_out(prog(t, t_terr - 0.1, t_enor + 0.8))
    if g > 0.02:
        pts = np.array([[float(v) for v in MP.proy(cam, lo, la)] for lo, la in TERRITORIO_N])
        c = pts.mean(axis=0)
        pts = c + (pts - c) * g
        lz.relleno(pts, (70, 200, 120), alfa=0.22, capa=2)
        lz.trazo(np.vstack([pts, pts[:1]]), (150, 255, 180), 6.0, afinar=False, temblor=0.0, capa=2)
    for lug, nm in (("mexico", "Ciudad de México"),):
        MD.ciudad(lz, cam, lug, t, T_F1, tam=1.4, tipo="ciudad", bando=(70, 190, 110), nombre=nm, px=22, semilla=3)
    k = U.pop(t, t_mex - 0.05) * U.salida(t, t_terr - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "México empezaba a ser un país…", color=U.COL["naranja"], px=70, k=k, cola=None)
    k = U.pop(t, t_terr - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "con un territorio enorme", color=U.COL["verde"], px=82, k=k * U.repop(t, t_enor + 0.1), cola=None)
    MD.brujula(lz, W - 110, H - 120, 1.0)


@shot(T_F2, bg=lambda t: bg_grad((54, 30, 112), (150, 70, 130), mid=(100, 46, 130), ym=0.5), post=[GRAD], ent=("fundido", 0.4))
def de_ideas(lz, t):
    U.bokeh(lz, t, seed=135, n=12, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.22)
    # bolsa de dinero vacía: caen las últimas monedas y queda en cero
    kb = U.pop(t, t_sin - 0.1, 1.2)
    if kb > 0.01:
        cx, cy = 480, 600 + 7 * math.sin(t * 2.2)
        lz.relleno(elipse(cx, cy + 40, 150 * kb, 140 * kb, 0, 30), (190, 150, 90), capa=2)
        lz.relleno(np.array([[cx - 60 * kb, cy - 80 * kb], [cx + 60 * kb, cy - 80 * kb], [cx + 36 * kb, cy - 140 * kb], [cx - 36 * kb, cy - 140 * kb]]), (190, 150, 90), capa=2)
        lz.relleno(rect_red(cx - 70 * kb, cy - 100 * kb, 140 * kb, 24 * kb, 8), (226, 70, 80), capa=2)
        P.rotulo(lz, cx, cy + 40, "0", px=int(120 * kb), k=1.0, color=(250, 244, 220), sombra=0.0)
        for j in range(4):
            u = ((t - t_din) * 0.8 + j * 0.25) % 1.0 if t > t_din else 0.0
            if u > 0:
                lz.relleno(circulo(cx + 40 * (j - 1.5), cy + 140 + 250 * u, 18, 12), (250, 206, 70), alfa=1 - u, capa=2)
    k = U.pop(t, t_din - 0.05)
    if k > 0.01:
        U.llamada(lz, 480, 880, "sin dinero", color=U.COL["rojo"], px=64, k=k * U.repop(t, t_din + 0.2), cola=None)
    # ideas distintas: una caja «gobierno» de la que parten flechas en direcciones opuestas
    ki = U.pop(t, t_ideas - 0.15, 1.2)
    if ki > 0.01:
        cx, cy = 1300, 560 + 6 * math.sin(t * 2.0 + 1.0)
        lz.relleno(rect_red(cx - 190 * ki, cy - 62 * ki, 380 * ki, 124 * ki, 22), (250, 244, 232), capa=2)
        P.rotulo(lz, cx, cy, "¿cómo gobernar?", px=int(44 * ki), k=1.0, color=(60, 40, 90), sombra=0.0)
        for j, (ang, col) in enumerate(((-2.5, (226, 70, 80)), (-1.57, (70, 150, 230)), (-0.64, (250, 206, 70)), (0.8, (70, 190, 110)), (2.3, (176, 110, 220)))):
            u = e_out(prog(t, t_ideas - 0.1 + 0.12 * j, t_ideas + 0.9 + 0.12 * j))
            a = np.array([cx + math.cos(ang) * 150, cy + math.sin(ang) * 90])
            b = np.array([cx + math.cos(ang) * (440 + 22 * math.sin(t * 3.0 + j)), cy + math.sin(ang) * (270 + 14 * math.sin(t * 3.0 + j))])
            d = b - a
            p1 = a + d * u
            lz.trazo(np.array([a, p1]), col, 18, afinar=False, temblor=0.0, capa=2)
            if u > 0.1:
                dd = d / np.hypot(*d)
                n = np.array([-dd[1], dd[0]])
                lz.relleno(np.array([p1 + dd * 34, p1 + n * 24, p1 - n * 24]), col, capa=2)
    k = U.pop(t, t_ideas - 0.05)
    if k > 0.01:
        U.llamada(lz, 1300, 920, "ideas muy distintas de cómo gobernarse", color=U.COL["morado"], px=48, k=k * U.repop(t, t_dist + 0.1), cola=None)


# ------------------------------------------------------------------------------------------------ sonido
snd(T_A + 0.2, "trueno", 0.4)
snd(t_resol, "gong", 0.4)
snd(T_B1, "pop", 0.3)
snd(t_coron, "bling", 0.5)
snd(t_ano + 0.2, "crujido", 0.5)
snd(T_B2, "bling", 0.4)
snd(t_nacio, "gong", 0.4)
snd(t_vic, "pop", 0.4)
snd(T_C, "pop", 0.3)
snd(t_abol, "crujido", 0.6)
snd(T_D1, "whoosh", 0.3, dur=0.9)
snd(t_trai, "gong", 0.5)
snd(T_D2, "pluck", 0.4)
snd(t_fus + 0.1, "canonazo", 0.4)
snd(T_E, "gong", 0.4)
snd(T_F1, "whoosh", 0.3, dur=1.0)
snd(t_enor, "pop", 0.4)
snd(t_din, "monedas", 0.4)
snd(t_ideas, "pluck", 0.4)
