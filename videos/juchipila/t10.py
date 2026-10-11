# -*- coding: utf-8 -*-
"""Escena 10 · la refundación (5:42-6:24): fray Antonio de Segovia y fray Miguel de Bolonia; el virrey perdona a unos seis mil caxcanes que bajan
de paz; Juchipila se refunda en 1542-1543 (diorama que se construye); el convento y el templo de San Francisco de Asís (1627); alcaldía mayor
de la Nueva Galicia (1548-1786) en el mapa; pasan los siglos y en 1810 sus descendientes se suman a los insurgentes."""
import math

import numpy as np

import kz_ui as U
import kz_iso as I
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
import mundos_k as MK
from motor import W, H, prog, lerp, smooth, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, h01, catmull
from reg import shot, snd
from util import *  # noqa: F401,F403
from t01 import acabado

E10 = "refundacion"
MP = KM.MAPA
PN = MK.PuebloNuevo()
t_interv, t_frailes, t_franc, t_antonio, t_segovia, t_miguel, t_bolonia = (T(E10, "intervinieron", frase=0), T(E10, "frailes", frase=0), T(E10, "franciscanos", frase=0),
                                                                           T(E10, "antonio", frase=0), T(E10, "segovia", frase=0), T(E10, "miguel", frase=0), T(E10, "bolonia", frase=0))
t_consig, t_virrey, t_perdon, t_seis, t_bajaron, t_paz, t_penol = (T(E10, "consiguieron", frase=1), T(E10, "virrey", frase=1), T(E10, "perdonara", frase=1), T(E10, "seis", frase=1),
                                                                    T(E10, "bajaron", frase=1), T(E10, "paz", frase=1), T(E10, "penol", frase=1))
t_refundo, t_juch, t_entre, t_cuarenta_y_dos = T(E10, "refundo", frase=2), T(E10, "juchipila", frase=2), T(E10, "entre", frase=2), T(E10, "cuarenta", frase=2)
t_conv, t_templo, t_sanfr, t_asis, t_mil = T(E10, "convento", frase=3), T(E10, "templo", frase=3), T(E10, "francisco", frase=3), T(E10, "asis", frase=3), T(E10, "mil", frase=3)
t_colonia, t_cabeza, t_alcaldia, t_nueva, t_mil2, t_ochenta = (T(E10, "colonia", frase=4), T(E10, "cabeza", frase=4), T(E10, "alcaldia", frase=4), T(E10, "nueva", frase=4),
                                                               T(E10, "mil", frase=4), T(E10, "ochenta", frase=4))
t_pasaron, t_siglos, t_indep, t_desc, t_caxc, t_espan, t_sumaron, t_insurg = (T(E10, "pasaron", frase=5), T(E10, "siglos", frase=5), T(E10, "independencia", frase=5),
                                                                              T(E10, "descendientes", frase=5), T(E10, "caxcanes", frase=5), T(E10, "espanoles", frase=5),
                                                                              T(E10, "sumaron", frase=5), T(E10, "insurgentes", frase=5))
T_A, T_B, T_C, T_D, T_E, T_F = T0(E10), INI(E10, 1) - 0.15, INI(E10, 2) - 0.15, INI(E10, 3) - 0.15, INI(E10, 4) - 0.15, INI(E10, 5) - 0.15


# ------------------------------------------------------------------------------------------------ A. dos frailes franciscanos
@shot(T_A, bg=lambda t: PA.cielo(0.0), post=[acabado], ent=("fundido", 0.6))
def a_frailes(lz, t):
    PA.sol(lz, 960, 640, 120, t, 0.0)
    U.haces_luz(lz, 960, 640, t, n=10, largo=1300, color=(255, 236, 190), alfa=0.12)
    PA.sierras(lz, t, 20 * (t - T_A), 0.0, y0=760, capas=3, semilla=101)
    U.bokeh(lz, t, seed=103, n=8, colores=((255, 214, 140), (255, 160, 120)), alfa=0.25)
    for j, (x, t0, nom, yaw, sd, spec) in enumerate(((600, t_antonio - 0.2, "fray Antonio de Segovia", 0.4, 21, "fraile"),
                                                       (1320, t_miguel - 0.2, "fray Miguel de Bolonia", -0.4, 22, dict(K2.TIPOS["fraile"], pelo=(190, 186, 196), barba="puntiaguda")))):
        k = pk(t, T_A + 0.3 + 0.35 * j, 0.6)
        if k > 0.01:
            K2.busto(lz, x, 930, 150 * k, spec, t, yaw=yaw, emocion="pensativo" if t < t0 + 0.4 else "neutro", ojos="abiertos", seed=sd, habla=0.5 if t0 < t < t0 + 1.4 else 0.0)
            ka = U.pop(t, t0)
            if ka > 0.01:
                U.llamada(lz, x, 290, nom, color=U.COL["naranja"] if j == 0 else U.COL["teal"], px=44, k=ka, cola=None)
    k = U.pop(t, t_franc) * U.salida(t, t_antonio - 0.1)
    if k > 0.01:
        U.llamada(lz, W / 2, 150, "dos frailes franciscanos", color=U.COL["morado"], px=56, k=k, cola=None)
    snd(t_frailes, "campana", 0.4)


# ------------------------------------------------------------------------------------------------ B. el perdón: seis mil bajan de paz
@shot(T_B, bg=lambda t: PA.cielo(0.05), post=[acabado], ent=("tinta", 0.6))
def b_paz(lz, t):
    PA.sol(lz, 1600, 180, 60, t, 0.05)
    MK.bajada_paz(lz, t, smooth(prog(t, T_B, t_paz + 0.6)) * 0.95 + 0.05)
    km = pk(t, t_virrey - 0.2, 0.5)
    if km > 0.01:
        MD.medallon(lz, 250, 260, 150, "mendoza", t, k=km)
        k = U.pop(t, t_perdon)
        if k > 0.01:
            U.llamada(lz, 250, 450, "perdón del virrey", color=U.COL["morado"], px=40, k=k, cola=None)
    c = int(round(lerp(0, 6000, e_out(prog(t, t_seis - 0.1, t_bajaron + 0.4))) / 10.0)) * 10
    k = U.pop(t, t_seis - 0.1)
    if k > 0.01:
        lz.texto(f"{c:,}".replace(",", " "), 1560, 400, 150, "geo_x", color=(255, 255, 255), borde=None, k=k, alfa=1.0, capa=2, temblor=0.0)
        U.llamada(lz, 1560, 510, "caxcanes", color=U.COL["teal"], px=48, k=k, cola=None)
    k = U.pop(t, t_paz)
    if k > 0.01:
        U.llamada(lz, 1560, 600, "bajan de paz", color=U.COL["blanco"], px=44, k=k, cola=None, color_texto=(60, 40, 90))
    snd(t_perdon, "campana", 0.4)
    snd(t_seis, "pop", 0.4)


# ------------------------------------------------------------------------------------------------ C-D. el pueblo se refunda (1542-1543) y llega el templo (1627)
def cam_cd(t):
    return K(t, [(T_C, (110, 60, 0, 0.85)), (t_cuarenta_y_dos, (120, 40, 20, 0.95)), (T_D + 1.2, (160, -60, 40, 1.35)), (T1(E10) - 9.5, (170, -80, 50, 1.55))])


def _obra(t):
    return smooth(prog(t, T_C + 0.2, T_D - 0.3))


def _templo(t):
    return 1.0 if t > t_templo - 0.3 else 0.0


@shot(T_C, bg=lambda t: PA.cielo(0.0), post=[acabado], ent=("tinta", 0.6))
def c_refundacion(lz, t):
    cx, cy, cz, zm = cam_cd(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    PA.sol(lz, 1600, 220, 60, t, 0.0)
    PA.sierras(lz, t, 15 * (t - T_C), 0.0, y0=440, capas=4, semilla=107)
    DC.aves(lz, t, n=7, seed=4)
    PN.suelo(lz, iso, t)
    m = PN.objetos(t, _obra(t), _templo(t), convento=smooth(prog(t, t_conv - 0.2, t_conv + 0.6)))
    m.dibujar(lz, iso)
    if t < T_D:
        k = U.pop(t, t_refundo)
        if k > 0.01:
            U.llamada(lz, W / 2, 150, "se refunda Juchipila", color=U.COL["naranja"], px=60, k=k * U.repop(t, t_juch + 0.2), cola=None)
        U.fecha_lugar(lz, t, t_entre, T_D - 0.1, "Juchipila", "1542 – 1543")
    else:
        # convento y templo: el reloj corre de 1542 a 1627
        y = int(lerp(1543, 1627, e_inout(prog(t, t_conv, t_templo + 0.3))))
        k = U.pop(t, t_conv - 0.1)
        if k > 0.01:
            U.llamada(lz, 480, 150, "el convento franciscano", color=U.COL["morado"], px=52, k=k * U.salida(t, t_templo - 0.1), cola=None)
        k = U.pop(t, t_templo)
        if k > 0.01:
            sx, sy = iso.P(167, -20, 120)
            U.llamada(lz, sx, sy - 40, "Templo de San Francisco de Asís", color=U.COL["naranja"], px=44, k=k, cola="abajo")
        k = U.pop(t, t_conv)
        if k > 0.01:
            lz.texto(str(y), 1640, 170, 120, "geo_x", color=(255, 255, 255), borde=None, k=k, alfa=1.0, capa=2, temblor=0.0)
            U._registrar(lz, 1640, 170, 320, 130)
    snd(t_refundo, "amanecer", 0.4)
    snd(t_templo, "campana", 0.5)


# ------------------------------------------------------------------------------------------------ E. alcaldía mayor de la Nueva Galicia (1548-1786)
def cam_e(t):
    return Klog(t, [(T_E, (-103.6, 22.4, 1.25)), (T_F, (-103.4, 22.0, 1.45))])


NG = [(-106.2, 23.6), (-103.0, 24.4), (-101.2, 23.6), (-101.0, 21.6), (-102.2, 20.4), (-103.8, 19.9), (-105.4, 20.4), (-106.6, 21.6)]


@shot(T_E, bg=lambda t: MP.base(cam_e(t), t, exag=12.0, rios_umbral=0.7), post=[acabado], ent=("tinta", 0.6))
def e_alcaldia(lz, t):
    cam = cam_e(t)
    MD.mar_vivo(lz, cam, t, seed=10)
    MD.montes(lz, cam)
    a = smooth(prog(t, t_nueva - 0.3, t_nueva + 0.5))
    if a > 0.01:
        ll = np.array(NG)
        x, y = MP.proy(cam, ll[:, 0], ll[:, 1])
        q = np.array(catmull(np.stack([x, y], 1), 8, True))
        lz.relleno(q, (122, 90, 220), alfa=0.18 * a, capa=1)
        P.discontinua(lz, np.vstack([q, q[:1]]), (255, 255, 255), ancho=4.0, largo=18.0, hueco=12.0, fase=-t * 20, capa=1)
        MD.region(lz, cam, "NUEVA GALICIA", (-105.2, 23.3), px=46, alfa=0.85 * a)
    MD.ciudad(lz, cam, "guadalajara", t, T_E + 0.2, tam=0.9, tipo="ciudad", nombre="Guadalajara", px=24, semilla=3)
    MD.ciudad(lz, cam, "zacatecas", t, T_E + 0.3, tam=0.9, tipo="ciudad", nombre="Zacatecas", px=24, semilla=4)
    MD.ciudad(lz, cam, "juchipila", t, t_cabeza - 0.2, tam=1.25, tipo="pueblo", nombre=None, px=26, semilla=2)
    x, y = MA_.proy(cam, "juchipila")
    k = pk(t, t_cabeza, 0.45)
    if k > 0.01:
        MD.corona(lz, x, y - 70, 2.2 * k, 1.0, t)
        U.llamada(lz, x + 230, y + 10, "Juchipila: alcaldía mayor", color=U.COL["naranja"], px=38, k=U.pop(t, t_alcaldia), cola=None)
    # línea de tiempo 1548 -> 1786
    kl = U.pop(t, t_mil2 - 0.2)
    if kl > 0.01:
        f = e_inout(prog(t, t_mil2, t_ochenta + 0.5))
        x0, x1, yl = 360, 1560, 960
        lz.relleno(rect_red(x0 - 20, yl - 50, (x1 - x0 + 40) * kl, 100, 50), (30, 14, 60), alfa=0.7, capa=2)
        lz.relleno(rect_red(x0, yl - 6, (x1 - x0) * f, 12, 6), (255, 196, 70), capa=2)
        lz.relleno(circulo(x0 + (x1 - x0) * f, yl, 16, 16), (255, 230, 150), capa=2)
        P.rotulo(lz, x0 + 10, yl - 30, "1548", px=36, color=(255, 255, 255), alfa=kl, sombra=0.0)
        if f > 0.95:
            P.rotulo(lz, x1 - 10, yl - 30, "1786", px=36, color=(255, 255, 255), alfa=1.0, sombra=0.0)
        U._registrar(lz, (x0 + x1) / 2, yl, x1 - x0 + 40, 100)
    snd(t_cabeza, "bling", 0.4)


# ------------------------------------------------------------------------------------------------ F. pasan los siglos: 1810, se suman a los insurgentes
@shot(T_F, bg=lambda t: PA.cielo(round(0.15 + 0.3 * smooth(prog(t, t_indep - 0.3, t_indep + 0.5)), 1)), post=[acabado], ent=("tinta", 0.6))
def f_insurgentes(lz, t):
    amb = 0.15 + 0.3 * smooth(prog(t, t_indep - 0.3, t_indep + 0.5))
    cx = 60.0 * (t - T_F)
    PA.sol(lz, 1500, 260, 64, t, amb)
    PA.sierras(lz, t, cx * 0.5, amb, y0=640, capas=4, semilla=113)
    p = PA.pal(amb)
    degradado_v(lz, 0, W, 760, H, p["pasto"][0], p["pasto"][1], 760, H)
    lz.trazo(np.array([(x, 940 + 6 * math.sin((x + cx) * 0.004)) for x in np.linspace(-40, W + 40, 30)]), (226, 206, 160), 110.0, afinar=False, temblor=0.0, capa=1)
    y_ = int(lerp(1786, 1810, e_inout(prog(t, t_pasaron, t_indep + 0.2))))
    k = U.pop(t, t_pasaron - 0.1)
    if k > 0.01:
        AB.contador_atras(lz, W / 2, 200, y_, px=150, k=k)
    k = U.pop(t, t_indep)
    if k > 0.01:
        U.llamada(lz, W / 2, 320, "la Independencia", color=U.COL["verde"] if "verde" in U.COL else U.COL["teal"], px=50, k=k, cola=None)
    # columna que se forma: descendientes de caxcanes y de españoles juntos tras el estandarte
    a = smooth(prog(t, T_F + 0.2, T_F + 1.0))
    if a > 0.01:
        v = K2.v_marcha(26)
        x0 = 700 + (t - T_F) * v * 0.7
        MK.estandarte_guadalupano(lz, x0 + 30, 950, 30, t)
        for i in range(10):
            caxc = i % 2 == 0
            spec = dict(K2.variar("caxcan" if caxc else "hombre", 1900 + i), tocado="sombrero_palma", torso="camiseta")
            if not caxc:
                spec["piel"] = "clara"
            K2.cuerpo(lz, x0 - 140 * (i + 1), 960 + 10 * (i % 2), 26, spec, t, piernas="camina", brazos="arriba" if i % 4 == 1 else "balanceo", mirar=1, vista="perfil",
                      seed=1900 + i, emocion="alegre", ph=t * 5 + i, alfa=a)
        k = U.pop(t, t_caxc)
        if k > 0.01:
            U.llamada(lz, 700, 600, "caxcanes", color=U.COL["teal"], px=40, k=k, cola=None)
        k = U.pop(t, t_espan)
        if k > 0.01:
            U.llamada(lz, 1000, 600, "+ españoles", color=U.COL["rojo"], px=40, k=k, cola=None)
    k = U.pop(t, t_insurg)
    if k > 0.01:
        U.llamada(lz, 1400, 470, "con los insurgentes", color=U.COL["naranja"], px=48, k=k, cola="abajo")
    PA.flores_frente(lz, t, cx * 1.8, n=8, amb=amb, y0=1020, seed=23)
    snd(t_indep, "campana", 0.5)
    snd(t_sumaron, "tambor", 0.4)
