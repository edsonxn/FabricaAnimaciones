# -*- coding: utf-8 -*-
"""Escena 15 · Iturbide y el Plan de Iguala (8:39-9:15): el militar elegido, la misión contra Guerrero, el Plan de Iguala y sus tres garantías, el mensaje para todos, el abrazo y el Ejército Trigarante."""
import math

import numpy as np

import kz_iso as I
from kz_iso import tint
import kz_iso_obj as O
import kz_iso_obj2 as O2
import kz_iso_arq as A
import kz_iso_arq2 as B
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
import mundos_m as mm
import mundos_n as mn

E15 = "iturbide"
MP = KM.MAPA
GRAD = lambda img, t: U.gradacion(img)
BASE = lambda cam, t: MP.base(cam, t, exag=13.0, rios_umbral=0.7)
PURP = lambda t: bg_grad((54, 30, 112), (150, 70, 130), mid=(100, 46, 130), ym=0.5)
IGU = mn.PlazaIguala()
SIE = mm.SierraSur()

# ------------------------------------------------------------------ anclas
t_dir, t_eli, t_mil, t_real, t_comb, t_insu, t_dur, t_agu, t_itu = [T(E15, w, frase=0) for w in ("dirigirla", "eligieron", "militar", "realista", "combatido", "insurgentes", "dureza", "agustin", "iturbide")]
t_env, t_sur, t_acab, t_guer, t_pero, t_itu2, t_plan = [T(E15, w, frase=1) for w in ("enviaron", "sur", "acabar", "guerrero", "pero", "iturbide", "plan")]
t_feb, t_1821, t_lanzo, t_plan2, t_igu, t_tres, t_gar, t_rel, t_ind, t_uni = [T(E15, w, frase=2) for w in ("febrero", "veintiuno", "lanzo", "plan", "iguala", "tres", "garantias", "religion", "independencia", "union")]
t_msj, t_todos, t_cat, t_esp, t_cri, t_ins, t_rea = [T(E15, w, frase=3) for w in ("mensaje", "todos", "catolicos", "espanoles", "criollos", "insurgentes", "realistas")]
t_escr, t_ofre, t_unir, t_acep, t_enem, t_abr = [T(E15, w, frase=4) for w in ("escribio", "ofrecio", "unirse", "acepto", "enemigos", "abrazaron")]
t_nacio, t_ejer, t_tres2, t_col, t_bla, t_ver, t_roj = [T(E15, w, frase=5) for w in ("nacio", "ejercito", "tres", "colores", "blanco", "verde", "rojo")]
T_A, T_A2, T_B, T_C1, T_C2, T_D, T_E1, T_E2, T_F = T0(E15), t_comb - 0.3, t_env - 0.15, t_feb - 0.15, t_tres - 0.25, t_msj - 0.15, t_escr - 0.15, t_acep - 0.25, t_nacio - 0.15


# ------------------------------------------------------------------------------------------------ 1. EL MILITAR ELEGIDO
@shot(T_A, bg=PURP, post=[GRAD], ent=("fundido", 0.5))
def it_elegido(lz, t):
    U.bokeh(lz, t, seed=111, n=14, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.24)
    U.haces_luz(lz, W / 2 + 300, 520, t, n=8, largo=1300, color=(255, 200, 240), alfa=0.10, ancho=0.09)
    # los conservadores le ofrecen el mando (un bastón de oro); su retrato se agranda
    kv = U.pop(t, T_A + 0.05, 1.3)
    RT.retrato(lz, 1130, 1010, 250 * (0.94 + 0.06 * kv), "iturbide", t, emocion="serio", mirar=-0.3, seed=7, alfa=min(1.0, kv))
    for i, (q, x) in enumerate((("garibay", 280), ("yermo", 640))):
        k = U.pop(t, t_eli - 0.1 + 0.2 * i, 1.2)
        if k > 0.01:
            RT.retrato(lz, x, 1030, 125 * (0.94 + 0.06 * k), q, t, emocion="serio", mirar=0.5, seed=12 + i, alfa=min(1.0, k))
    kb = e_out(prog(t, t_eli, t_eli + 0.9))
    if kb > 0.01:
        x0, y0 = 460, 700
        x1, y1 = 900, 600
        bx, by = lerp(x0, x1, kb), lerp(y0, y1, kb) - 80 * math.sin(math.pi * kb)
        lz.trazo(np.array([[bx - 90, by + 40], [bx + 90, by - 40]]), (250, 206, 70), 18, afinar=False, temblor=0.0, capa=2)
        lz.relleno(circulo(bx + 96, by - 44, 22, 14), (250, 236, 150), capa=2)
        lz.halo(bx, by, 200, (255, 224, 130), alfa=0.35, capa=2)
    k = U.pop(t, t_dir - 0.05) * U.salida(t, t_mil - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "para dirigirla, eligieron…", color=U.COL["naranja"], px=76, k=k, cola=None)
    k = U.pop(t, t_mil - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "a un militar realista", color=U.COL["rojo"], px=88, k=k * U.repop(t, t_real + 0.1), cola=None)
    k = U.pop(t, t_agu - 0.05)
    if k > 0.01:
        U.llamada(lz, 1130, 180, "Agustín de Iturbide", color=U.COL["morado"], px=52, k=k * U.repop(t, t_itu + 0.1), cola=None)


RUTA_I = [(-99.13, 19.43), (-99.4, 18.9), (-99.7, 18.35)]


def cam_a2(t):
    return Klog(t, [(T_A2, (-100.2, 19.9, 1.6)), (T_B, (-100.0, 19.6, 1.9))])


@shot(T_A2, bg=lambda t: BASE(cam_a2(t), t), post=[GRAD], ent=("zoom", 0.5))
def it_dureza(lz, t):
    cam = cam_a2(t)
    I.luz()
    MD.montes(lz, cam, min_alt=2200)
    MD.pais(lz, cam, "Mexico", (255, 96, 70), alfa=0.08, borde=(255, 220, 90), ancho=4.0, t=t, latido=0.0)
    for j, (lug, tp, nm, dx, dy, lado, bd) in enumerate((("valladolid", "ciudad", "Valladolid", -130, 4, "der", "real"), ("guanajuato", "ciudad", "Guanajuato", 130, 4, "izq", "real"), ("mexico", "ciudad", "", 0, 0, "izq", "real"))):
        MD.ciudad(lz, cam, lug, t, T_A2 + 0.1 * j, tam=1.4, tipo=tp, bando=bd, semilla=j + 121)
        if nm:
            MD.etiqueta(lz, cam, lug, nm, t, T_A2 + 0.1 * j + 0.1, px=22, dy=dy, dx=dx, lado=lado)
    # sus campañas: columnas realistas que dejan derrotas insurgentes (insignias) y humo
    for j, lug in enumerate((("valladolid"), (-101.0, 20.2), "guanajuato", (-101.4, 20.9), (-100.5, 19.8))):
        k = U.pop(t, t_insu - 0.2 + 0.3 * j)
        if k > 0.01:
            MD.insignia_batalla(lz, cam, lug, t, t_insu - 0.2 + 0.3 * j, s=1.1, color=(226, 70, 70))
            sx, sy = MP.proy(cam, lug[0] if isinstance(lug, tuple) else MD.CIUDADES[lug][0], lug[1] if isinstance(lug, tuple) else MD.CIUDADES[lug][1])
            for q in range(3):
                u = ((t * 0.5 + q / 3.0 + j * 0.2) % 1.0)
                lz.relleno(circulo(float(sx) + 10 * math.sin(q + t), float(sy) - 60 - 90 * u, 14 + 22 * u, 12), (70, 66, 80), alfa=0.6 * (1 - u), capa=2)
    for i in range(5):
        u = (t * 0.2 + i * 0.2) % 1.0
        a = np.array([float(v) for v in MP.proy(cam, -99.13, 19.43)])
        b = np.array([float(v) for v in MP.proy(cam, -101.2, 20.2)])
        p = a + (b - a) * u + np.array([0, 14 * math.sin(u * 8)])
        MD.ejercito(lz, float(p[0]), float(p[1]), 10, bando="real", t=t + i * 0.3, s=1.5, dir=-1, semilla=i, bandera=(i == 0), polvo=True)
    kc = U.pop(t, t_comb - 0.1)
    if kc > 0.01:
        MD.medallon(lz, 300, 470, 140, "iturbide", t, emocion="serio", k=kc, seed=4)
        U.llamada(lz, 300, 640, "Iturbide", color=U.COL["rojo"], px=42, k=kc, cola="arriba")
    k = U.pop(t, t_comb - 0.05) * U.salida(t, t_dur - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "había combatido a los insurgentes…", color=U.COL["naranja"], px=64, k=k, cola=None)
    k = U.pop(t, t_dur - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "con dureza", color=U.COL["rojo"], px=104, k=k * U.repop(t, t_dur + 0.2), cola=None)
    MD.brujula(lz, W - 110, H - 120, 1.0)


# ------------------------------------------------------------------------------------------------ 2. EL ENCARGO: ACABAR CON GUERRERO (mapa)
def cam_b(t):
    return Klog(t, [(T_B, (-99.3, 18.9, 2.6)), (T_C1, (-99.3, 18.6, 3.0))])


def _flecha(lz, a, b, ancho, color, frac=1.0, alfa=1.0):
    d = b - a
    L = float(np.hypot(*d))
    if L < 1 or frac < 0.01:
        return
    u = d / L
    n = np.array([-u[1], u[0]])
    f = min(1.0, frac)
    p1 = a + d * f
    cab = min(ancho * 1.5, L * f)
    base = p1 - u * cab
    w = ancho / 2
    pts = np.array([a + n * w * 0.55, base + n * w * 0.55, base + n * w * 1.5, p1, base - n * w * 1.5, base - n * w * 0.55, a - n * w * 0.55])
    lz.relleno(pts + np.array([6.0, 8.0]), (20, 10, 50), alfa=0.25 * alfa, capa=2)
    lz.relleno(pts, color, alfa=alfa, capa=2)


@shot(T_B, bg=lambda t: BASE(cam_b(t), t), post=[GRAD], ent=("fundido", 0.5))
def it_encargo(lz, t):
    cam = cam_b(t)
    I.luz()
    MD.montes(lz, cam, min_alt=2200)
    MD.pais(lz, cam, "Mexico", (255, 96, 70), alfa=0.08, borde=(255, 220, 90), ancho=4.0, t=t, latido=0.0)
    c0 = np.array([float(v) for v in MP.proy(cam, -99.5, 17.9)])
    sx, sy = c0
    lz.halo(float(sx), float(sy), 360, (140, 255, 170), alfa=0.28, capa=2)
    for j, (lug, tp, nm, dx, dy, lado, bd) in enumerate((("mexico", "ciudad", "Ciudad de México", 0, -100, "abajo", "real"), ("iguala", "pueblo", "Iguala", 110, 4, "izq", "real"), ("chilpancingo", "ciudad", "Chilpancingo", -130, 4, "der", "ins"))):
        MD.ciudad(lz, cam, lug, t, T_B + 0.1 * j, tam=1.5, tipo=tp, bando=bd, semilla=j + 131)
        MD.etiqueta(lz, cam, lug, nm, t, T_B + 0.1 * j + 0.1, px=22, dy=dy, dx=dx, lado=lado)
    pm = np.array([float(v) for v in MP.proy(cam, -99.13, 19.43)])
    pg = np.array([float(v) for v in MP.proy(cam, -99.54, 18.35)])
    f = e_inout(prog(t, t_env, t_acab + 1.0))
    _flecha(lz, pm + np.array([-40.0, 70.0]), pg + np.array([60.0, -40.0]), 64, (232, 70, 80), f)
    for i in range(5):
        u = max(0.0, min(0.999, f - 0.07 * i))
        if u > 0.01:
            p = (pm + np.array([-40.0, 70.0])) + ((pg + np.array([60.0, -40.0])) - (pm + np.array([-40.0, 70.0]))) * u
            MD.ejercito(lz, float(p[0]), float(p[1]), 10, bando="real", t=t + i * 0.2, s=1.5, dir=-1, semilla=i, bandera=(i == 0), polvo=True)
    kg = U.pop(t, t_guer - 0.1)
    if kg > 0.01:
        MD.medallon(lz, 1620, 450, 140, "guerrero", t, emocion="serio", k=kg, seed=5)
        U.llamada(lz, 1620, 620, "Guerrero", color=U.COL["verde"], px=44, k=kg, cola="arriba")
    kp = U.pop(t, t_plan - 0.15)
    if kp > 0.01:                                           # el «otro plan»: un pergamino que Iturbide esconde
        px_, py_ = float(pm[0]) - 40, float(pm[1]) + 70
        U.pergamino_grande(lz, 420, 800, 420, 240, t, t_plan - 0.15, lineas=("…", "otro plan"), titulo="¡un plan!", sello=True, rot=-0.06)
    k = U.pop(t, t_env - 0.05) * U.salida(t, t_acab - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "lo enviaron al sur", color=U.COL["naranja"], px=82, k=k, cola=None)
    k = U.pop(t, t_acab - 0.05) * U.salida(t, t_pero - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "para acabar con Guerrero", color=U.COL["rojo"], px=78, k=k * U.repop(t, t_guer + 0.1), cola=None)
    k = U.pop(t, t_pero - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "pero Iturbide tenía otro plan", color=U.COL["morado"], px=72, k=k * U.repop(t, t_plan + 0.1), cola=None)
    MD.brujula(lz, W - 110, H - 120, 1.0)


# ------------------------------------------------------------------------------------------------ 3. EL PLAN DE IGUALA Y LAS TRES GARANTÍAS
def cam_c1(t):
    return Klog(t, [(T_C1, (-99.7, 18.6, 2.2)), (T_C2, (-99.54, 18.35, 3.4))])


@shot(T_C1, bg=lambda t: BASE(cam_c1(t), t), post=[GRAD], ent=("zoom", 0.5))
def it_iguala_mapa(lz, t):
    cam = cam_c1(t)
    I.luz()
    MD.montes(lz, cam, min_alt=2200)
    MD.pais(lz, cam, "Mexico", (255, 96, 70), alfa=0.08, borde=(255, 220, 90), ancho=4.0, t=t, latido=0.0)
    MD.ciudad(lz, cam, "iguala", t, T_C1, tam=2.6, tipo="pueblo", bando=(70, 190, 110), semilla=5, llama=False)
    MD.onda(lz, cam, "iguala", t, t_lanzo, dur=2.4, r_deg=0.8, color=(255, 255, 255), n=3, ancho=6.0)
    k = U.pop(t, t_feb - 0.05)
    if k > 0.01:
        U.fecha_lugar(lz, t, T_C1 + 0.1, T_C2 - 0.1, "Iguala", "24 de febrero de 1821", y=70)
        sx, sy = MP.proy(cam, -99.54, 18.35)
        U.llamada(lz, float(sx), float(sy) - 140, "Iguala", color=U.COL["morado"], px=70, k=k * U.repop(t, t_igu + 0.1) * U.salida(t, t_lanzo - 0.15, 0.2), cola="abajo")
    k = U.pop(t, t_lanzo - 0.05) * U.salida(t, T_C2 - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "lanza el Plan de Iguala", color=U.COL["verde"], px=86, k=k * U.repop(t, t_plan2 + 0.1), cola=None)
    MD.brujula(lz, W - 110, H - 120, 1.0)


@shot(T_C2, bg=PURP, post=[GRAD], ent=("fundido", 0.4))
def it_garantias(lz, t):
    U.bokeh(lz, t, seed=112, n=14, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.24)
    U.haces_luz(lz, W / 2, 520, t, n=8, largo=1300, color=(255, 200, 240), alfa=0.10, ancho=0.09)
    U.chispas(lz, t, n=18, seed=113, tam=(5, 12))
    U.pergamino_grande(lz, 470, 540, 620, 480, t, T_C2 + 0.05, lineas=("Plan de Iguala", "24 de febrero de 1821", "tres garantías"), titulo="PLAN DE IGUALA", sello=True, rot=-0.03)
    # tres insignias grandes: religión, independencia, unión
    for (x, tt_, lab, col, ic) in ((1130, t_rel, "religión", (236, 196, 90), "c"), (1440, t_ind, "independencia", (70, 190, 110), "b"), (1750, t_uni, "unión", (214, 56, 66), "u")):
        k = U.pop(t, tt_ - 0.15, 1.2)
        if k > 0.01:
            y = 560
            lz.relleno(np.array([[x - 110 * k, y - 190 * k], [x + 110 * k, y - 190 * k], [x + 100 * k, y + 110 * k], [x, y + 220 * k], [x - 100 * k, y + 110 * k]]), col, capa=2)
            lz.relleno(np.array([[x - 92 * k, y - 170 * k], [x + 92 * k, y - 170 * k], [x + 84 * k, y + 96 * k], [x, y + 196 * k], [x - 84 * k, y + 96 * k]]), tuple(min(255, c + 40) for c in col), capa=2)
            if ic == "c":
                lz.relleno(rect_red(x - 12 * k, y - 110 * k, 24 * k, 150 * k, 6), (255, 255, 255), capa=2)
                lz.relleno(rect_red(x - 54 * k, y - 66 * k, 108 * k, 24 * k, 6), (255, 255, 255), capa=2)
            elif ic == "b":
                lz.trazo(np.array([[x - 40 * k, y + 60 * k], [x - 40 * k, y - 120 * k]]), (255, 255, 255), 8 * k, afinar=False, temblor=0.0, capa=2)
                lz.relleno(np.array([[x - 40 * k, y - 120 * k], [x + 70 * k, y - 100 * k], [x + 70 * k, y - 20 * k], [x - 40 * k, y - 40 * k]]), (255, 255, 255), capa=2)
            else:
                for sg in (-1, 1):
                    lz.trazo(circulo(x + sg * 30 * k, y - 20 * k, 52 * k, 24), (255, 255, 255), 12 * k, cerrado=True, afinar=False, temblor=0.0, capa=2)
            U.llamada(lz, x, y + 280 * k, lab, color=col, px=42, k=k * U.repop(t, tt_ + 0.2), cola=None)
    k = U.pop(t, t_tres - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2 + 330, 130, "tres garantías", color=U.COL["morado"], px=86, k=k * U.repop(t, t_gar + 0.1), cola=None)


# ------------------------------------------------------------------------------------------------ 4. UN MENSAJE PARA TODOS
@shot(T_D, bg=lambda t: bg_grad((110, 150, 230), (252, 226, 200), mid=(196, 190, 236), ym=0.55), post=[GRAD], ent=("fundido", 0.4))
def it_mensaje(lz, t):
    U.chispas(lz, t, n=16, seed=114, tam=(5, 12))
    # una carta en el centro; de ella salen rayos hacia seis grupos: católicos, españoles, criollos, insurgentes y realistas
    kc = U.pop(t, t_msj - 0.05, 1.3)
    if kc > 0.01:
        cx, cy = W / 2, 470
        lz.relleno(rect_red(cx - 150 * kc, cy - 100 * kc, 300 * kc, 200 * kc, 12), (252, 246, 232), capa=2)
        lz.relleno(np.array([[cx - 150 * kc, cy - 100 * kc], [cx, cy + 20 * kc], [cx + 150 * kc, cy - 100 * kc]]), (226, 214, 190), capa=2)
        lz.relleno(circulo(cx, cy + 10 * kc, 26 * kc, 16), (206, 60, 70), capa=2)
        lz.halo(cx, cy, 340 * kc, (255, 236, 170), alfa=0.30, capa=0)
    grupos = (("campesina", "católicos", t_cat, 220, U.COL["morado"]), ("peninsular", "españoles", t_esp, 620, U.COL["rojo"]), ("criollo", "criollos", t_cri, 1020, U.COL["naranja"]), ("guerrero", "insurgentes", t_ins, 1400, U.COL["verde"]), ("yermo", "realistas", t_rea, 1740, U.COL["azul"]))
    for q, lab, tt_, x, col in grupos:
        k = U.pop(t, tt_ - 0.15, 1.2)
        if k > 0.01:
            RT.retrato(lz, x, 1030, 120 * (0.94 + 0.06 * k), q, t, emocion="neutro", mirar=0.0, seed=int(x), alfa=min(1.0, k))
            u = prog(t, tt_ - 0.15, tt_ + 0.5)
            lz.trazo(np.array([[W / 2, 470], [W / 2 + (x - W / 2) * u, 470 + (700 - 470) * u]]), (255, 236, 170), 6, afinar=False, temblor=0.0, capa=2)
            U.llamada(lz, x, 760, lab, color=col, px=40, k=k, cola=None)
    k = U.pop(t, t_msj - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "un mensaje para todos", color=U.COL["naranja"], px=88, k=k * U.repop(t, t_todos + 0.1), cola=None)


# ------------------------------------------------------------------------------------------------ 5. LA CARTA Y EL ABRAZO
@shot(T_E1, bg=lambda t: bg_grad((130, 190, 240), (254, 232, 200), mid=(200, 218, 238), ym=0.5), post=[GRAD], ent=("fundido", 0.4))
def it_carta(lz, t):
    # mapa esquemático: carta que vuela de Iturbide a Guerrero; respuesta que vuelve
    U.bokeh(lz, t, seed=115, n=8, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.16)
    RT.retrato(lz, 380, 1010, 160, "iturbide", t, emocion="serio", mirar=0.4, seed=7, alfa=U.pop(t, T_E1 + 0.05))
    RT.retrato(lz, 1540, 1010, 160, "guerrero", t, emocion="serio", mirar=-0.4, seed=8, alfa=U.pop(t, T_E1 + 0.15))
    u1 = e_inout(prog(t, t_escr, t_unir + 0.4))
    u2 = e_inout(prog(t, t_acep - 0.2, t_acep + 0.9))
    for (u, x0, x1, ret, ok) in ((u1, 560, 1380, False, False), (u2, 1380, 560, True, True)):
        if 0 < u < 1:
            x, y = lerp(x0, x1, u), 520 - 160 * math.sin(math.pi * u)
            lz.relleno(rect_red(x - 52, y - 34, 104, 68, 8), (252, 246, 232), capa=2)
            lz.relleno(np.array([[x - 52, y - 34], [x, y + 8], [x + 52, y - 34]]), (226, 214, 190), capa=2)
            lz.relleno(circulo(x, y + 4, 12, 10), (70, 190, 110) if ok else (206, 60, 70), capa=2)
    k = U.pop(t, t_escr - 0.05) * U.salida(t, t_acep - 0.25, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "le escribió a Guerrero y le ofreció unirse", color=U.COL["naranja"], px=66, k=k * U.repop(t, t_ofre + 0.1), cola=None)
    k = U.pop(t, t_acep - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "Guerrero aceptó", color=U.COL["verde"], px=96, k=k * U.repop(t, t_acep + 0.2), cola=None)


@shot(T_E2, bg=lambda t: bg_grad((250, 190, 120), (254, 232, 190), mid=(246, 150, 130), ym=0.5), post=[GRAD], ent=("fundido", 0.4))
def it_abrazo(lz, t):
    u = e_inout(prog(t, t_enem - 0.2, t_abr + 0.1))
    cx, cy, cz, zm = 150, 140, 36, 3.5
    iso = I.Iso(cx, cy, cz, zm)
    I.luz(mul=(1.05, 0.98, 0.92), mix=(255, 170, 100), k=0.10)
    SIE.suelo(lz, iso, t)
    m = SIE.objetos(t)
    # dos tropas (realistas e insurgentes) llegan desde lados opuestos del camino; los jefes se encuentran y se abrazan
    for i in range(10):
        x = lerp(20 - 14 * i, 110 - 8 * (i % 3), e_out(prog(t, T_E2, t_abr)))
        y = 150 + 10 * (i % 3) - 12 * (i // 3)
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i: (lambda lz, iso: G.persona(lz, iso, x, y, t, ("realista", "dragon", "granadero")[i % 3], dir=(1, 0), vel=1.3 if t < t_abr else 0.0, seed=10700 + i, h=44, accion="vitorea" if t > t_abr + 0.4 else None)))(x, y, i), fijo=False, clave=x + y + 3)
        x2 = lerp(300 + 14 * i, 190 + 8 * (i % 3), e_out(prog(t, T_E2, t_abr)))
        m.add(x2 - 4, y - 4, x2 + 4, y + 4, 40, (lambda x2, y, i: (lambda lz, iso: G.persona(lz, iso, x2, y, t, ("insurgente", "insurgente_lanza", "campesino")[i % 3], dir=(-1, 0), vel=1.3 if t < t_abr else 0.0, seed=10750 + i, h=44, accion="vitorea" if t > t_abr + 0.4 else None)))(x2, y, i), fijo=False, clave=x2 + y + 3)
    xa, xb = lerp(110, 144, u), lerp(190, 156, u)
    m.add(xa - 4, 140, xa + 4, 148, 50, lambda lz, iso: G.persona(lz, iso, xa, 144, t, "oficial", dir=(1, 0), vel=0.0, seed=10800, h=58, cara="alegre" if t > t_abr else "serio", accion="saluda" if t > t_abr else None), fijo=False, clave=xa + 144)
    m.add(xb - 4, 140, xb + 4, 148, 50, lambda lz, iso: G.persona(lz, iso, xb, 144, t, "insurgente", dir=(-1, 0), vel=0.0, seed=10801, h=58, cara="alegre" if t > t_abr else "serio", accion="saluda" if t > t_abr else None), fijo=False, clave=xb + 144)
    m.dibujar(lz, iso)
    if t > t_abr:
        k = prog(t, t_abr, t_abr + 1.2)
        qx, qy = iso.P(150, 144, 70)
        for j in range(8):
            a = j * 0.8 + t * 2
            U.chispa4(lz, float(qx) + 150 * math.cos(a) * k, float(qy) - 40 + 90 * math.sin(a) * k, 14 + 6 * (j % 3), alfa=0.9 * (1 - 0.4 * k))
        lz.halo(float(qx), float(qy), 300 * k, (255, 224, 130), alfa=0.35 * k, capa=2)
    k = U.pop(t, t_enem - 0.05) * U.salida(t, t_abr - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "los dos enemigos…", color=U.COL["rojo"], px=88, k=k, cola=None)
    k = U.pop(t, t_abr - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "¡se abrazaron!", color=U.COL["verde"], px=104, k=k * U.repop(t, t_abr + 0.2), cola=None)


# ------------------------------------------------------------------------------------------------ 6. NACE EL EJÉRCITO DE LAS TRES GARANTÍAS
def cam_f(t):
    return K(t, [(T_F, (200, 260, 30, 2.4)), (t_col, (200, 240, 36, 2.8)), (T1(E15), (200, 230, 40, 2.9))])


@shot(T_F, bg=lambda t: bg_grad((130, 190, 240), (254, 232, 200), mid=(200, 218, 238), ym=0.5), post=[GRAD], ent=("fundido", 0.4))
def it_trigarante(lz, t):
    cx, cy, cz, zm = cam_f(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz(mul=(1.04, 1.0, 0.96), mix=(255, 220, 160), k=0.06)
    IGU.suelo(lz, iso, t)
    m = IGU.objetos(t, gente=0.5)
    # el ejército mixto (realistas, insurgentes) en columnas bajo banderas trigarantes que suben
    tb = e_back(prog(t, t_nacio - 0.2, t_nacio + 0.6))
    for i in range(48):
        r_, c_ = i // 12, i % 12
        x, y = 110 + 15 * c_, 270 + 14 * r_
        tp = ("oficial", "insurgente", "realista", "insurgente_lanza", "dragon", "campesino")[i % 6]
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i, tp: (lambda lz, iso: G.persona(lz, iso, x, y, t, tp, dir=(0, -1), vel=0.0, seed=10900 + i, h=44, accion="vitorea" if (t > t_nacio + 0.5 and i % 3 == 0) else None, cara="alegre")))(x, y, i, tp), fijo=False, clave=x + y + 3)
    for (x, y) in ((100, 240), (200, 232), (300, 240)):
        m.add(x - 4, y - 4, x + 4, y + 4, 140, (lambda x, y: (lambda lz, iso: O2.bandera_trigarante(lz, iso, x, y, h=int(90 * tb) + 4, t=t, w=44, alto=28)))(x, y), fijo=False, clave=x + y + 6)
    m.dibujar(lz, iso)
    mn.guirnaldas(lz, iso, t, k=prog(t, t_nacio, t_nacio + 2.0))
    DC.aves(lz, t, n=8, seed=121, y0=70, y1=240)
    for (txt, col, tt_, sw, x) in (("blanco", (255, 255, 255), t_bla, (250, 250, 246), 560), ("verde", (70, 190, 110), t_ver, (70, 190, 110), 960), ("rojo", (226, 70, 80), t_roj, (214, 56, 66), 1360)):
        k = U.pop(t, tt_ - 0.1)
        if k > 0.01:
            lz.relleno(circulo(x, 930, 64 * k, 28), sw, capa=2)
            lz.trazo(circulo(x, 930, 68 * k, 28), (255, 255, 255), 6, cerrado=True, afinar=False, temblor=0.0, capa=2)
            U.llamada(lz, x, 1030, txt, color=U.COL["morado"] if txt == "blanco" else (U.COL["verde"] if txt == "verde" else U.COL["rojo"]), px=44, k=k, cola=None)
    k = U.pop(t, t_nacio - 0.05) * U.salida(t, t_col - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "nace el Ejército de las Tres Garantías", color=U.COL["verde"], px=68, k=k * U.repop(t, t_ejer + 0.1), cola=None)
    k = U.pop(t, t_col - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "con sus colores", color=U.COL["naranja"], px=88, k=k * U.repop(t, t_col + 0.1), cola=None)


# ------------------------------------------------------------------------------------------------ sonido
snd(T_A + 0.2, "pop", 0.3)
snd(t_eli, "bling", 0.5)
snd(T_A2, "whoosh", 0.3, dur=0.9)
snd(t_dur, "gong", 0.5)
snd(T_B, "whoosh", 0.3, dur=0.9)
snd(t_plan, "pluck", 0.5)
snd(T_C1, "campana", 0.4)
snd(T_C2, "bling", 0.5)
snd(t_rel, "pop", 0.4)
snd(t_ind, "pop", 0.4)
snd(t_uni, "bling", 0.5)
snd(T_D, "pop", 0.3)
for _t in (t_cat, t_esp, t_cri, t_ins, t_rea):
    snd(_t, "pop", 0.3)
snd(t_escr, "whoosh", 0.3, dur=0.8)
snd(t_acep, "bling", 0.5)
snd(T_E2, "tambor", 0.3)
snd(t_abr, "bling", 0.6)
snd(T_F, "tambor", 0.4)
snd(t_nacio, "gong", 0.5)
snd(t_bla, "pop", 0.3)
snd(t_ver, "pop", 0.3)
snd(t_roj, "pop", 0.3)
