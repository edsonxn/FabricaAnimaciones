# -*- coding: utf-8 -*-
"""Escena 8 · el virrey Mendoza (4:29-5:07): Antonio de Mendoza (retrato real) ve en peligro todo el occidente y sale de México al frente
del ejército; cientos de españoles y decenas de miles de aliados (tlaxcaltecas, mexicas, tarascos) convergen; cae Nochistlán el 9 de
noviembre de 1541 y Tenamaxtli escapa; quedan dos peñoles; el ejército rodea y asedia el Mixtón, que cae a principios de 1542."""
import math

import numpy as np

import kz_ui as U
import kz_iso as I
import kz_iso_obj as O
import kz_iso_deco as DC
import kz_mapa as KM
import kz_mapa_dib as MD
import kz_abstracto as AB
import kz_pers2d as K2
import kz_retrato as RT
import plano as P
import lugares  # noqa: F401
import paisajes as PA
import mapas as MA_
import mundos_g as MG
import mundos_h as MH
import mundos_i as MI
from mundos_b import iso_en
from motor import W, H, prog, lerp, smooth, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, h01, catmull
from reg import shot, snd
from util import *  # noqa: F401,F403
from t01 import acabado

E8 = "mendoza"
MP = KM.MAPA
PEN = MH.PenolIso()
t_virrey, t_antonio, t_mendoza, t_compr, t_todo, t_occ, t_salio, t_frente, t_ejercito = (T(E8, "virrey", frase=0), T(E8, "antonio", frase=0), T(E8, "mendoza", frase=0),
                                                                                       T(E8, "comprendio", frase=0), T(E8, "todo", frase=0), T(E8, "occidente", frase=0),
                                                                                       T(E8, "salio", frase=0), T(E8, "frente", frase=0), T(E8, "ejercito", frase=0))
t_reunio, t_cientos, t_decenas, t_aliados, t_tlax, t_mexicas, t_tarascos = (T(E8, "reunio", frase=1), T(E8, "cientos", frase=1), T(E8, "decenas", frase=1), T(E8, "aliados", frase=1),
                                                                            T(E8, "tlaxcaltecas", frase=1), T(E8, "mexicas", frase=1), T(E8, "tarascos", frase=1))
t_nueve, t_noviembre, t_cayo, t_noch, t_pero, t_tenam, t_escapar = (T(E8, "nueve", frase=2), T(E8, "noviembre", frase=2), T(E8, "cayo", frase=2), T(E8, "nochistlan", frase=2),
                                                                     T(E8, "pero", frase=2), T(E8, "tenamaxtli", frase=2), T(E8, "escapar", frase=2))
t_rebeldes, t_dos, t_penoles, t_noch2, t_mixton = (T(E8, "rebeldes", frase=3), T(E8, "dos", frase=3), T(E8, "penoles", frase=3), T(E8, "nochistlan", frase=3), T(E8, "mixton", frase=3))
t_entonces, t_dirigio, t_rodeo, t_asedio, t_principios, t_penol, t_cayo2 = (T(E8, "entonces", frase=4), T(E8, "dirigio", frase=4), T(E8, "rodeo", frase=4), T(E8, "asedio", frase=4),
                                                                            T(E8, "principios", frase=4), T(E8, "penol", frase=4), T(E8, "cayo", frase=4))
t_rebelion, t_terminado = T(E8, "rebelion", frase=5), T(E8, "terminado", frase=5)
T_A, T_B, T_C, T_D, T_E, T_F = T0(E8), t_salio - 0.2, INI(E8, 1) - 0.15, INI(E8, 2) - 0.15, INI(E8, 3) - 0.15, INI(E8, 4) - 0.15


# ------------------------------------------------------------------------------------------------ A. el virrey Mendoza: se juega todo el occidente
def cam_a(t):
    return Klog(t, [(T_A, (-100.5, 21.6, 0.95)), (T_B, (-101.6, 21.6, 1.1))])


def _occ_poly(cam):
    pts = [(-106.0, 24.5), (-101.5, 25.0), (-100.6, 22.6), (-101.2, 20.4), (-103.0, 19.4), (-105.6, 20.2), (-106.8, 22.4)]
    ll = np.array(pts)
    x, y = MP.proy(cam, ll[:, 0], ll[:, 1])
    return np.array(catmull(np.stack([x, y], 1), 8, True))


@shot(T_A, bg=lambda t: MP.base(cam_a(t), t, exag=12.0, rios_umbral=0.7), post=[acabado], ent=("tinta", 0.6))
def a_mendoza(lz, t):
    cam = cam_a(t)
    MD.montes(lz, cam)
    MD.ciudad(lz, cam, "mexico", t, T_A + 0.2, tam=1.1, tipo="ciudad", nombre="México", px=26, semilla=2)
    MD.ciudad(lz, cam, "guadalajara", t, T_A + 0.3, tam=0.9, tipo="ciudad", nombre="Guadalajara", px=24, semilla=3)
    MD.ciudad(lz, cam, "mixton", t, T_A + 0.4, tam=0.9, tipo="fuerte", nombre="Mixtón", px=24, semilla=5, llama=True)
    a = smooth(prog(t, t_todo - 0.2, t_occ + 0.4))
    if a > 0.01:                                                         # todo el occidente en juego: zona que late en rojo
        q = _occ_poly(cam)
        lz.relleno(q, (226, 60, 70), alfa=(0.22 + 0.08 * math.sin(t * 6)) * a, capa=1)
        lz.trazo(q, (255, 120, 120), 6.0, cerrado=True, temblor=0.0, capa=1)
        k = U.pop(t, t_occ)
        if k > 0.01:
            cx_, cy_ = q.mean(axis=0)
            U.llamada(lz, cx_, cy_ - 40, "todo el occidente", color=U.COL["rojo"], px=50, k=k * U.repop(t, t_occ + 0.6), cola=None)
    # retrato real del virrey
    lz.relleno(rect_red(0, 0, 700, H, 0), (20, 8, 40), alfa=0.35, capa=1)
    kr = pk(t, T_A + 0.15, 0.55)
    if kr > 0.01:
        RT.retrato(lz, 360, 930, 190 * (0.9 + 0.1 * kr), "mendoza", t, emocion="serio", alfa=min(1.0, kr * 1.3), seed=4)
    k = U.pop(t, t_virrey)
    if k > 0.01:
        U.llamada(lz, 360, 150, "el virrey", color=U.COL["morado"], px=44, k=k, cola=None)
    k = U.pop(t, t_antonio)
    if k > 0.01:
        U.llamada(lz, 360, 230, "Antonio de Mendoza", color=U.COL["rojo"], px=56, k=k, cola=None)
    snd(t_antonio, "gong", 0.5)
    snd(t_occ, "tambor", 0.4)


# ------------------------------------------------------------------------------------------------ B. sale él mismo al frente del ejército (Ciudad de México)
@shot(T_B, bg=lambda t: PA.cielo(0.05), post=[acabado], ent=("tinta", 0.6))
def b_salida(lz, t):
    cx = 90.0 * (t - T_B)
    PA.sol(lz, 1660, 230, 56, t, 0.05)
    MI.volcanes(lz, t, cx, y=650)
    MI.ciudad_mexico(lz, t, cx, y=760)
    lz.relleno(np.array([(0, 760), (W, 752), (W, 820), (0, 830)]), (110, 170, 200), capa=1)            # orilla del lago
    lz.relleno(np.array([(0, 820), (W, 812), (W, H), (0, H)]), (170, 170, 100), capa=1)
    lz.trazo(np.array([(x, 930) for x in np.linspace(-40, W + 40, 12)]), (226, 206, 160), 110.0, afinar=False, temblor=0.0, capa=1)     # calzada
    # columna: el virrey a la cabeza, con abanderado; detrás soldados y aliados
    xv = 1080 + 80 * (t - T_B)
    MI.virrey_a_caballo(lz, xv, 975, 22, t)
    for i in range(10):
        x = xv - 330 - 130 * i
        spec = "soldado" if i < 5 else dict(K2.variar("caxcan", 960 + i), tocado="cinta", ropa=(240, 236, 222))
        K2.cuerpo(lz, x, 960 + 12 * (i % 2), 26, spec, t, piernas="camina", brazos="balanceo", mirar=1, vista="perfil", seed=40 + i, ph=t * 5 + i)
    PA.flores_frente(lz, t, cx * 1.8, n=8, amb=0.05, y0=1010, seed=19)
    k = U.pop(t, t_frente - 0.2)
    if k > 0.01:
        U.llamada(lz, xv, 470, "él mismo, al frente", color=U.COL["naranja"], px=48, k=k, cola="abajo")
    snd(t_salio, "galope", 0.5)
    snd(t_ejercito, "tambor", 0.4)


# ------------------------------------------------------------------------------------------------ C. cientos de españoles, decenas de miles de aliados
def cam_c(t):
    return Klog(t, [(T_C, (-100.9, 20.4, 1.45)), (T_D, (-101.6, 20.7, 1.6))])


ORIGENES = [("tlaxcala", "tlaxcaltecas", (255, 150, 60)), ("mexico", "mexicas", (90, 200, 200)), ("patzcuaro", "tarascos", (200, 110, 220))]


@shot(T_C, bg=lambda t: MP.base(cam_c(t), t, exag=12.0, rios_umbral=0.7), post=[acabado], ent=("tinta", 0.6))
def c_aliados(lz, t):
    cam = cam_c(t)
    MD.montes(lz, cam)
    MD.ciudad(lz, cam, "guadalajara", t, T_C, tam=0.9, tipo="ciudad", nombre="Guadalajara", px=24, semilla=3)
    MD.ciudad(lz, cam, "mixton", t, T_C, tam=0.9, tipo="fuerte", nombre="Mixtón", px=24, semilla=5)
    for j, (lug, nom, col) in enumerate(ORIGENES):
        t0 = {"tlaxcaltecas": t_tlax, "mexicas": t_mexicas, "tarascos": t_tarascos}[nom]
        MD.ciudad(lz, cam, lug, t, T_C + 0.1 * j, tam=0.9, tipo="ciudad", nombre=None, px=22, semilla=6 + j)
        a = smooth(prog(t, t_decenas - 0.3 + 0.2 * j, t_decenas + 0.5 + 0.2 * j))
        if a > 0.01:
            q = MA_._pts(cam, [lug, (-101.9, 20.45), "guadalajara", "mixton"])
            AB.corriente(lz, t, q, n=110, ancho=34.0, vel=0.16, color=(col, P.aclarar(col, 0.3)), r=(8.0, 14.0), seed=40 + j, capa=2, alfa=a)
        k = U.pop(t, t0)
        if k > 0.01:
            x, y = MA_.proy(cam, lug)
            dx, dy = {"tlaxcaltecas": (150, 70), "mexicas": (-60, 110), "tarascos": (0, 100)}[nom]
            U.llamada(lz, x + dx, y + dy, nom, color=col, px=42, k=k * U.repop(t, t0 + 0.3), cola=None)
    # proporción: cientos frente a decenas de miles (cada punto = muchos)
    k = pk(t, t_cientos - 0.1, 0.5)
    if k > 0.01:
        bx, by = 90, 640
        lz.relleno(rect_red(bx - 20, by - 70, 560 * k, 400 * k, 24), (20, 8, 50), alfa=0.65, capa=2)
        for i in range(4):
            lz.relleno(circulo(bx + 30 + 34 * i, by, 13 * k, 12), (226, 70, 70), capa=2)
        U.llamada(lz, bx + 380, by, "cientos de españoles", color=U.COL["rojo"], px=30, k=k, cola=None)
        kd = smooth(prog(t, t_decenas - 0.1, t_aliados + 0.4))
        n = int(220 * kd)
        for i in range(n):
            x = bx + 30 + 19 * (i % 26)
            y = by + 70 + 19 * (i // 26)
            lz.relleno(circulo(x, y, 7 * k, 8), ORIGENES[i % 3][2], capa=2)
        if kd > 0.05:
            U.llamada(lz, bx + 270, by + 270, "decenas de miles de aliados", color=U.COL["teal"], px=30, k=U.pop(t, t_decenas), cola=None)
    snd(t_reunio, "tambor", 0.4)
    for tt in (t_tlax, t_mexicas, t_tarascos):
        snd(tt, "pop", 0.35)


# ------------------------------------------------------------------------------------------------ D. 9 de noviembre de 1541: cae Nochistlán; Tenamaxtli escapa
def cam_d(t):
    return Klog(t, [(T_D, (-102.95, 21.45, 3.6)), (T_E, (-103.05, 21.5, 4.2))])


@shot(T_D, bg=lambda t: MP.base(cam_d(t), t, exag=12.0, rios_umbral=0.7), post=[acabado], ent=("tinta", 0.6))
def d_nochistlan(lz, t):
    cam = cam_d(t)
    MD.montes(lz, cam)
    MD.ciudad(lz, cam, "juchipila", t, T_D, tam=0.8, tipo="pueblo", nombre="Juchipila", px=22, semilla=2)
    MD.ciudad(lz, cam, "mixton", t, T_D, tam=0.9, tipo="fuerte", nombre="Mixtón", px=22, semilla=5)
    MD.ciudad(lz, cam, "nochistlan", t, T_D + 0.1, tam=1.3, tipo="fuerte", nombre=None, px=24, semilla=4, llama=t > t_cayo)
    # el ejército llega desde el sur y rodea Nochistlán
    nx, ny = MA_.proy(cam, "nochistlan")
    for j in range(5):
        a = 2 * math.pi * j / 5 + 0.6
        f = e_inout(prog(t, T_D + 0.1 * j, t_cayo))
        r = lerp(380, 110, f)
        MD.ejercito(lz, nx + r * math.cos(a), ny + 0.6 * r * math.sin(a), 6, bando=(222, 60, 70), t=t, s=1.2, dir=-1 if math.cos(a) > 0 else 1, marcha=f < 0.99, bandera=j == 0, semilla=10 + j)
    MD.insignia_batalla(lz, cam, "nochistlan", t, t_cayo, año=None, s=1.2)
    U.fecha_lugar(lz, t, t_nueve - 0.1, T_E - 0.1, "Nochistlán", "9 nov. 1541")
    # Tenamaxtli escapa: punto de luz que sale hacia la sierra con línea discontinua
    f = e_inout(prog(t, t_escapar - 0.4, T_E + 0.2))
    if f > 0.01:
        cab = MA_.ruta_gruesa(lz, cam, ["nochistlan", (-102.95, 21.6), (-103.1, 21.75), (-103.35, 21.9)], frac=f, t=t, color=(70, 200, 200), ancho=8, dash=True, flecha=False)
        if cab is not None:
            AB.halo_punto(lz, cab[0], cab[1], 16, t, color=(70, 220, 210), nucleo=(250, 255, 250))
            U.llamada(lz, cab[0] + 20, cab[1] - 60, "Tenamaxtli escapa", color=U.COL["teal"], px=38, k=U.pop(t, t_tenam), cola="abajo")
    k = U.pop(t, t_cayo)
    if k > 0.01:
        U.llamada(lz, nx, ny + 120, "cae Nochistlán", color=U.COL["rojo"], px=46, k=k, cola=None)
    snd(t_cayo, "canonazo", 0.5)
    snd(t_escapar, "whoosh", 0.4)


# ------------------------------------------------------------------------------------------------ E. dos peñoles: Nochistlán y el Mixtón (pantalla dividida)
def _mitad(sd):
    m = 18
    if sd < 0:
        return np.array([(0, 0), (W / 2 - m, 0), (W / 2 - m, H / 2 - 40), (W / 2 - m - 26, H / 2), (W / 2 - m, H / 2 + 40), (W / 2 - m, H), (0, H)])
    return np.array([(W / 2 + m, 0), (W, 0), (W, H), (W / 2 + m, H), (W / 2 + m, H / 2 + 40), (W / 2 + m - 26, H / 2), (W / 2 + m, H / 2 - 40)])


@shot(T_E, bg=lambda t: bg_grad((30, 14, 50), (10, 4, 20)), post=[acabado], ent=("tinta", 0.6))
def e_dos_penoles(lz, t):
    for sd, nombre, t0, amb in ((-1, "peñol de Nochistlán", t_noch2, 0.65), (1, "peñol del Mixtón", t_mixton, 0.3)):
        k = smooth(prog(t, T_E + (0.0 if sd < 0 else 0.25), T_E + (0.5 if sd < 0 else 0.75)))
        if k < 0.01:
            continue
        with lz.recorte(_mitad(sd)):
            p = PA.pal(amb)
            degradado_v(lz, 0 if sd < 0 else W / 2, W / 2 if sd < 0 else W, 0, H, p["cielo"][0], p["cielo"][2], 0, H)
            cx0 = W / 4 if sd < 0 else 3 * W / 4
            PA.sierras(lz, t, 10 * (t - T_E) + (0 if sd < 0 else 900), amb, y0=720, capas=3, semilla=70 + sd)
            caido = sd < 0
            MG.penol(lz, t, cx=cx0, y_base=960, ancho=470 if caido else 520, alto=430 if caido else 520, sube=1.0 if not caido else 0.0,
                     fogatas=0.0 if caido else 1.0, gente=not caido)
            lz.relleno(np.array([(cx0 - 600, 950), (cx0 + 600, 940), (cx0 + 600, H), (cx0 - 600, H)]), p["pasto"][1], capa=1)
            if caido:                                                    # Nochistlán ya cayó: humo y fuego en la cumbre, gris
                for j in range(4):
                    llama(lz, cx0 - 150 + 100 * j, 960 - 430 - 4, 0.4, t, seed=j)
                    humo(lz, cx0 - 150 + 100 * j, 960 - 470, t, 0.0, n=6, s=0.7, alfa=0.5, seed=j, col=(80, 70, 90))
            lz.relleno(rect_red(0 if sd < 0 else W / 2, 0, W / 2, H, 0), (20, 10, 40), alfa=0.0, capa=2)
        U.llamada(lz, W / 4 if sd < 0 else 3 * W / 4, 150, nombre, color=U.COL["rojo"] if sd < 0 else U.COL["teal"], px=50, k=U.pop(t, t0), cola=None)
        if sd < 0 and t > t_noch2 + 0.6:
            U.llamada(lz, W / 4, 240, "ya cayó", color=U.COL["oscuro"], px=36, k=U.pop(t, t_noch2 + 0.6), cola=None)
    k = U.pop(t, t_dos)
    if k > 0.01:
        U.globo(lz, W / 2, 120, "dos peñoles", px=44, k=k, cola=None)
    snd(t_noch2, "pop", 0.35)
    snd(t_mixton, "pop", 0.35)


# ------------------------------------------------------------------------------------------------ F. rodean, asedian y toman el Mixtón; la rebelión termina
def cam_f(t):
    return K(t, [(T_F, (-20, 120, 150, 1.05)), (t_asedio, (-20, 60, 180, 1.2)), (t_cayo2, (-20, 20, 230, 1.45)), (T1(E8), (-20, 0, 250, 1.5))])


def _post_f(img, t):
    g = smooth(prog(t, t_rebelion - 0.4, t_terminado + 0.3))
    img = U.gradacion(img, luces=(1.0 - 0.1 * g, 1.0 - 0.12 * g, 1.0 - 0.02 * g), sombras=(1.0 - 0.12 * g, 1.0 - 0.14 * g, 1.0), contraste=1.0 + 0.04 * g, saturacion=1.0 - 0.45 * g)
    return acabado(img, t)


@shot(T_F, bg=lambda t: PA.cielo(round(0.3 + 0.4 * smooth(prog(t, t_rodeo, t_cayo2)), 1)), post=[_post_f], ent=("tinta", 0.6))
def f_cerco(lz, t):
    cx, cy, cz, zm = cam_f(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    amb = 0.3 + 0.4 * smooth(prog(t, t_rodeo, t_cayo2))
    PA.sol(lz, 1600, 240, 56, t, amb)
    PA.sierras(lz, t, 15 * (t - T_F), amb, y0=470, capas=4, semilla=81)
    PEN.suelo(lz, iso, t)
    R = lerp(470, 300, e_inout(prog(t, t_rodeo - 0.3, t_asedio + 1.2)))
    llegada = smooth(prog(t, T_F, t_rodeo))
    if llegada > 0.01:
        MI.cerco(lz, iso, t, R + 300 * (1 - llegada), frente=False)
    PEN.penol(lz, iso, t)
    cae = smooth(prog(t, t_cayo2 - 0.2, t_cayo2 + 0.5))
    if cae < 0.99:
        PEN.defensores(lz, iso, t, n=18, piedras=0.6 * (1 - cae))
        PEN.lluvia_piedras(lz, iso, t, 0.5 * smooth(prog(t, t_asedio - 0.3, t_asedio + 0.5)) * (1 - cae))
    if cae > 0.01:                                                       # la bandera de los vencedores en la cumbre y humo
        O.bandera(lz, iso_en(iso, MH.ZT), -20, -20, h=70 * cae, w=40, alto=26, color=(240, 236, 226), t=t, seed=2)
        for j, (x, y) in enumerate(MH.FOGATAS):
            O.humo(lz, iso, x, y, MH.ZT + 30, t, n=8, s=1.4, color=(110, 100, 120), seed=j, alfa=0.6 * cae)
    if llegada > 0.01:
        MI.cerco(lz, iso, t, R + 300 * (1 - llegada), frente=True)
    k = U.pop(t, t_rodeo) * U.salida(t, t_asedio - 0.1)
    if k > 0.01:
        U.llamada(lz, 520, 150, "lo rodearon", color=U.COL["rojo"], px=60, k=k, cola=None)
    k = U.pop(t, t_asedio) * U.salida(t, t_principios - 0.1)
    if k > 0.01:
        U.llamada(lz, 520, 150, "lo asediaron", color=U.COL["rojo"], px=60, k=k, cola=None)
    U.fecha_lugar(lz, t, t_principios - 0.1, T1(E8) + 1.0, "el Mixtón", "principios de 1542")
    k = U.pop(t, t_cayo2)
    if k > 0.01:
        U.llamada(lz, W / 2, 150, "el peñol cayó", color=U.COL["oscuro"], px=64, k=k * U.salida(t, t_rebelion - 0.1), cola=None)
    k = U.pop(t, t_rebelion)
    if k > 0.01:
        U.llamada(lz, W / 2, 150, "fin de la rebelión", color=U.COL["oscuro"], px=64, k=k, cola=None)
    snd(t_rodeo, "tambor", 0.45)
    snd(t_asedio, "canonazo", 0.4)
    snd(t_cayo2, "gong", 0.55)
