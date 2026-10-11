# -*- coding: utf-8 -*-
"""Escena 4 · la guerra del Mixtón (1540-1542): el cañón estalla (mapa), el peñol y su recuadro entre Juchipila y Apozol, Tenamaxtli y los
guerreros del tope, Alvarado (retrato real), el virrey Mendoza y su ejército, la leyenda de Santiago, la caída del peñol y el borde del vacío."""
import math

import numpy as np

import kz_ui as U
import kz_iso as I
import kz_iso_deco as DC
import kz_mapa as KM
import kz_mapa_dib as MD
import kz_abstracto as AB
import kz_pers2d as K2
import kz_retrato_real as RR
import plano as P
import lugares  # noqa: F401
import paisajes as PA
import mapas as MA_
import mundos_1 as M1
import mundos_4 as M4
from motor import W, H, prog, lerp, smooth, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, h01
from reg import shot, snd
from util import *  # noqa: F401,F403
from t01 import acabado

E4 = "mixton"
MP = KM.MAPA
PEN = M4.Penol()
t_cuar, t_abusos, t_enc, t_estallar, t_canon, t_entero = (T(E4, "cuarenta", frase=0), T(E4, "abusos", frase=0), T(E4, "encomiendas", frase=0), T(E4, "estallar", frase=0),
                                                          T(E4, "canon", frase=0), T(E4, "entero", frase=0))
t_levant, t_armas, t_refug, t_penol, t_mixton, t_cerro, t_paredes, t_vert, t_juch, t_apozol = (
    T(E4, "levantaron", frase=1), T(E4, "armas", frase=1), T(E4, "refugiaron", frase=1), T(E4, "penol", frase=1), T(E4, "mixton", frase=1), T(E4, "cerro", frase=1),
    T(E4, "paredes", frase=1), T(E4, "verticales", frase=1), T(E4, "juchipila", frase=1), T(E4, "apozol", frase=1))
t_miles, t_guerr, t_tena, t_resist = T(E4, "miles", frase=2), T(E4, "guerreros", frase=2), T(E4, "tenamaxtli", frase=2), T(E4, "resistieron", frase=2)
t_hasta, t_conq, t_pedro, t_alv, t_murio = (T(E4, "hasta", frase=3), T(E4, "conquistador", frase=3), T(E4, "pedro", frase=3), T(E4, "alvarado", frase=3), T(E4, "murio", frase=3))
t_tuvo, t_virrey, t_anton, t_mend, t_ejer, t_dec, t_aliad = (T(E4, "tuvo", frase=4), T(E4, "virrey", frase=4), T(E4, "antonio", frase=4), T(E4, "mendoza", frase=4),
                                                           T(E4, "ejercito", frase=4), T(E4, "decenas", frase=4), T(E4, "aliados", frase=4))
t_dice, t_leyenda, t_combate, t_apostol, t_sant, t_apar, t_cab, t_blanco = (T(E4, "dice", frase=5), T(E4, "leyenda", frase=5), T(E4, "combate", frase=5), T(E4, "apostol", frase=5),
                                                                           T(E4, "santiago", frase=5), T(E4, "aparecio", frase=5), T(E4, "caballo", frase=5), T(E4, "blanco", frase=5))
t_princ, t_cuar2, t_dos, t_penol2, t_cayo = (T(E4, "principios", frase=6), T(E4, "cuarenta", frase=6), T(E4, "dos", frase=6), T(E4, "penol", frase=6), T(E4, "cayo", frase=6))
t_cuenta, t_trad, t_muchos, t_pref, t_lanz, t_vacio, t_rend = (T(E4, "cuenta", frase=7), T(E4, "tradicion", frase=7), T(E4, "muchos", frase=7), T(E4, "prefirieron", frase=7),
                                                              T(E4, "lanzarse", frase=7), T(E4, "vacio", frase=7), T(E4, "rendirse", frase=7))
T_A = T0(E4)
T_B = INI(E4, 1) - 0.12
T_C = INI(E4, 2) - 0.12
T_D = INI(E4, 3) - 0.12
T_E = INI(E4, 4) - 0.12
T_F = INI(E4, 5) - 0.12
T_G = INI(E4, 6) - 0.12
T_H = INI(E4, 7) - 0.12
BG_NOCHE = lambda t: bg_grad((14, 8, 40), (70, 26, 70), mid=(36, 16, 70), ym=0.6)


def _pie(lz, iso, x, y, z, texto, color, t, t0, t1, px=40, dy=-70, cola="abajo"):
    k = U.pop(t, t0) * U.salida(t, t1)
    if k > 0.01:
        sx, sy = iso.P(x, y, z)
        U.llamada(lz, float(sx), float(sy) + dy, texto, color=color, px=px, k=k, cola=cola)


# ------------------------------------------------------------------------------------------------ A. el cañón estalla (1540)
def cam_a(t):
    return Klog(t, [(T_A, (-102.2, 22.0, 1.5)), (T1(E4) - 38.0, (-103.05, 21.58, 3.3))])


@shot(T_A, bg=lambda t: MP.base(cam_a(t), t, exag=12.0, rios_umbral=0.7), post=[acabado], ent=("fundido", 0.6))
def a_estalla(lz, t):
    cam = cam_a(t)
    MD.mar_vivo(lz, cam, t, seed=7)
    MD.montes(lz, cam)
    MD.region(lz, cam, "ZACATECAS", (-102.4, 22.9), px=40, alfa=0.7, z_max=2.4)
    MD.ciudad(lz, cam, "juchipila", t, T_A + 0.2, tam=1.1, tipo="pueblo", nombre=None, semilla=2)
    MD.ciudad(lz, cam, "nochistlan", t, T_A + 0.4, tam=1.0, tipo="pueblo", nombre=None, semilla=3)
    MD.ciudad(lz, cam, "tlaltenango", t, T_A + 0.6, tam=1.0, tipo="pueblo", nombre=None, semilla=4)
    MD.etiqueta(lz, cam, "juchipila", "Juchipila", t, T_A + 0.3, px=30, dy=36, dx=-86)
    MD.etiqueta(lz, cam, "nochistlan", "Nochistlán", t, T_A + 0.5, px=30, dy=34, dx=70)
    MD.etiqueta(lz, cam, "tlaltenango", "Tlaltenango", t, T_A + 0.7, px=30, dy=-56, dx=0)
    for k, (lug, dt) in enumerate((("juchipila", 0.0), ("nochistlan", 0.35), ("tlaltenango", 0.7), ("apozol", 0.15))):
        MD.onda(lz, cam, lug, t, t_estallar + dt, dur=2.6, r_deg=0.9, n=3, ancho=6.0, periodo=0.45, alfa=0.9, color=(255, 90, 80))
    k = U.pop(t, T_A + 0.2)
    if k > 0.01:
        U.fecha_lugar(lz, t, T_A + 0.2, T_B - 0.2, "Cañón de Juchipila", "1540")
    k = U.pop(t, t_abusos) * U.salida(t, t_estallar - 0.1)
    if k > 0.01:
        U.llamada(lz, 1500, 250, "abusos de las encomiendas", color=U.COL["naranja"], px=52, k=k, cola=None)
    k = U.pop(t, t_estallar) * U.salida(t, T_B - 0.15)
    if k > 0.01:
        U.llamada(lz, 1500, 380, "el cañón entero estalla", color=U.COL["rojo"], px=58, k=k * U.repop(t, t_entero), cola=None)
    snd(t_estallar, "estallido", 0.5)
    snd(t_abusos, "tambor", 0.4)


# ------------------------------------------------------------------------------------------------ B. el peñol del Mixtón entre Juchipila y Apozol
def _iso_pen(c):
    return I.Iso(float(c[0]), float(c[1]), float(c[2]), float(c[3]))


@shot(T_B, bg=lambda t: PA.cielo(0.35), post=[acabado], ent=("fundido", 0.6))
def b_penol(lz, t):
    c = K(t, [(T_B, (170, 180, 40, 0.8)), (t_cerro, (180, 190, 60, 0.92)), (T_C, (180, 190, 80, 1.0))])
    iso = _iso_pen(c)
    PA.sol(lz, 1560, 220, 60, t, 0.35)
    PA.sierras(lz, t, 10 * (t - T_B), 0.35, y0=360, capas=3, semilla=91)
    PEN.suelo(lz, iso, t)
    g = float(smooth(prog(t, T_B, t_refug + 1.0)))
    m = PEN.objetos(t, guerreros=g, cerco=0.0, gente_cerco=0.0, fuego=g)
    m.dibujar(lz, iso)
    k = U.pop(t, t_penol) * U.salida(t, T_C - 0.2)
    if k > 0.01:
        sx, sy = iso.P(180, 180, 180)
        U.llamada(lz, float(sx), float(sy) - 130, "peñol del Mixtón", color=U.COL["rojo"], px=58, k=k * U.repop(t, t_mixton + 0.3), cola="abajo")
    kp = U.pop(t, t_paredes) * U.salida(t, T_C - 0.2)
    if kp > 0.01:
        U.llamada(lz, 1500, 840, "paredes casi verticales", color=U.COL["morado"], px=48, k=kp, cola=None)
    # recuadro con el mapa: entre Juchipila y Apozol
    ki = pk(t, t_juch - 0.5, 0.6) * (1 - smooth(prog(t, T_C - 0.3, T_C - 0.05)))
    if ki > 0.01:
        M4.inset_tres(lz, 330, 380, 260, t, t_juch - 0.1, t_juch - 0.5, t_apozol - 0.1, k=ki)
    snd(t_levant, "tambor", 0.4)
    snd(t_penol, "pop", 0.4)


# ------------------------------------------------------------------------------------------------ C. miles de guerreros y Tenamaxtli
@shot(T_C, bg=lambda t: PA.cielo(0.4), post=[acabado], ent=("zoom", 0.55))
def c_guerreros(lz, t):
    c = K(t, [(T_C, (180, 180, 170, 1.9)), (T_D - 0.5, (176, 176, 170, 2.25))])
    iso = _iso_pen(c)
    PA.sol(lz, 1560, 220, 60, t, 0.4)
    PA.sierras(lz, t, 10 * (t - T_C), 0.4, y0=360, capas=3, semilla=93)
    PEN.suelo(lz, iso, t)
    m = PEN.objetos(t, guerreros=1.0, cerco=0.25 * float(smooth(prog(t, T_C, T_D))), gente_cerco=1.0)
    m.dibujar(lz, iso)
    # el contador sube: «miles»
    k = U.pop(t, t_miles) * U.salida(t, T_D - 0.2)
    if k > 0.01:
        lz.texto("MILES", 360, 170, 140, "geo_x", color=(255, 255, 255), borde=None, k=k, alfa=1.0, capa=2, temblor=0.0)
        U.llamada(lz, 360, 280, "de guerreros caxcanes", color=U.COL["teal"], px=46, k=k, cola=None)
        U._registrar(lz, 360, 200, 460, 170)
    # Tenamaxtli en medallón
    kb = pk(t, t_tena - 0.3, 0.5) * U.salida(t, T_D - 0.2)
    if kb > 0.01:
        ring = circulo(1560, 560, 200 * kb, 44)
        lz.relleno(circulo(1568, 572, 206 * kb, 44), (14, 8, 40), alfa=0.35, capa=1)
        lz.relleno(ring, (60, 36, 120), capa=1)
        with lz.recorte(ring):
            lz.degradado(ring, (120, 70, 170), (40, 20, 90), (1560, 360), (1560, 760), capa=1)
            K2.busto(lz, 1566, 760, 150 * kb, "jefe_caxcan", t, yaw=-0.5, emocion="serio", ojos="abiertos", seed=12, habla=0.4 if t_tena < t < t_tena + 1.4 else 0.0)
        lz.trazo(ring, (255, 206, 72), 10.0, cerrado=True, afinar=False, temblor=0.0, capa=2)
        U.llamada(lz, 1560, 810, "Tenamaxtli", color=U.COL["naranja"], px=56, k=U.pop(t, t_tena), cola=None)
    snd(t_miles, "tambor", 0.5)
    snd(t_resist, "gong", 0.4)


# ------------------------------------------------------------------------------------------------ D. Pedro de Alvarado (1541)
@shot(T_D, bg=lambda t: bg_grad((60, 38, 86), (24, 16, 56), mid=(40, 24, 78), ym=0.55), post=[acabado], ent=("fundido", 0.6))
def d_alvarado(lz, t):
    U.bokeh(lz, t, seed=33, n=10, colores=((120, 90, 200), (200, 80, 120), (255, 170, 90)), alfa=0.3)
    k = pk(t, t_conq - 0.1, 0.6)
    if k > 0.01:
        RR.retrato(lz, 760, 900, 260 * k, "alvarado", t, emocion="serio")
        U.llamada(lz, 760, 130, "Pedro de Alvarado", color=U.COL["rojo"], px=64, k=U.pop(t, t_alv), cola=None)
    # lo que se sabe: 1541, campaña del Mixtón, murió
    kf = U.pop(t, t_hasta)
    if kf > 0.01:
        U.llamada(lz, 1450, 330, "conquistador", color=U.COL["oscuro"], px=52, k=kf * U.salida(t, T_E - 0.2), cola=None)
        U.llamada(lz, 1450, 450, "campaña del Mixtón", color=U.COL["morado"], px=52, k=kf * U.salida(t, T_E - 0.2), cola=None)
    km = U.pop(t, t_murio)
    if km > 0.01:
        # crespón negro en diagonal sobre el marco (violencia sin mostrar el momento)
        lz.relleno(np.array([(392, 250), (392, 350), (700, 105), (590, 105)]), (10, 6, 16), alfa=0.92 * km, capa=2)
        P.rotulo(lz, 1450, 640, "1541", px=190, k=km, color=(255, 255, 255), alfa=min(1.0, km * 1.4))
        U.llamada(lz, 1450, 780, "murió en la campaña", color=U.COL["rojo"], px=50, k=km, cola=None)
        U._registrar(lz, 1450, 640, 520, 220)
    snd(t_alv, "campana", 0.35)
    snd(t_murio, "golpe_grave", 0.4)


# ------------------------------------------------------------------------------------------------ E. el virrey Mendoza y su ejército
@shot(T_E, bg=lambda t: PA.cielo(0.3), post=[acabado], ent=("fundido", 0.6))
def e_virrey(lz, t):
    PA.sol(lz, 1500, 230, 60, t, 0.3)
    PA.sierras(lz, t, 24 * (t - T_E), 0.3, y0=620, capas=5, semilla=97)
    # el peñol lejano a la derecha
    M4.penol_fuego(lz, 1620, 700, 0.7, t, capa=0, fuego=0.8)
    p = PA.pal(0.3)
    degradado_v(lz, 0, W, 700, H, p["pasto"][0], p["pasto"][1], 700, H)
    # camino y ejército que avanza (corriente de miles)
    cam = [(-80, 960), (360, 900), (760, 930), (1180, 860), (1500, 790), (1640, 720)]
    q = np.array(catmull(np.array(cam, float), 12, False))
    lz.trazo(q, (226, 206, 168), 120.0, afinar=False, temblor=0.0, capa=1)
    AB.corriente(lz, t, cam, n=420, ancho=96.0, vel=0.07, color=((255, 130, 90), (255, 214, 120), (120, 200, 255), (250, 250, 250)), r=(3.5, 7.0), seed=5, capa=1)
    for i, (x, y, s) in enumerate(((120, 1010, 1.1), (520, 1040, 0.9), (1000, 1020, 1.2), (1500, 1040, 1.0), (1780, 1000, 0.9), (760, 780, 0.7), (1320, 760, 0.8))):
        PA.arbol(lz, x, y, s * 1.4, 0.3, seed=i + 2, t=t, capa=1)
    for i in range(10):
        u = ((t - T_E) * 0.05 + i * 0.1) % 1.0
        j = int(u * (len(q) - 1))
        MD.ejercito(lz, float(q[j][0]), float(q[j][1]) - 10, 8, bando="real", t=t, s=1.9, dir=1, marcha=True, bandera=(i % 2 == 0), semilla=i)
    kv = pk(t, t_virrey - 0.2, 0.6)
    if kv > 0.01:
        MD.medallon(lz, 300, 330, 190, "mendoza", t, k=kv)
        U.llamada(lz, 300, 560, "virrey Antonio de Mendoza", color=U.COL["morado"], px=44, k=U.pop(t, t_mend), cola=None)
    k = U.pop(t, t_dec)
    if k > 0.01:
        lz.texto("decenas de miles", 1250, 250, 96, "geo_x", color=(255, 255, 255), borde=None, k=k * U.salida(t, T_F - 0.2), alfa=1.0, capa=2, temblor=0.0)
        U.llamada(lz, 1250, 340, "de aliados indígenas", color=U.COL["teal"], px=48, k=k * U.salida(t, T_F - 0.2), cola=None)
        U._registrar(lz, 1250, 270, 800, 180)
    snd(t_ejer, "pasos", 0.4)
    snd(t_dec, "tambor", 0.4)


# ------------------------------------------------------------------------------------------------ F. la leyenda: Santiago en un caballo blanco
@shot(T_F, bg=BG_NOCHE, post=[acabado], ent=("fundido", 0.7))
def f_santiago(lz, t):
    M4.noche_penol(lz, t, glow=1.0)
    k = pk(t, t_apostol - 0.2, 0.9)
    if k > 0.01:
        U.haces_luz(lz, 960, 330, t, n=7, largo=1500, color=(255, 236, 170), alfa=0.09 * k, ancho=0.05)
        lz.halo(960, 330, 340 * k, (255, 240, 190), alfa=0.55 * k, dureza=1.1, capa=0)
        yb = 400 + 16 * math.sin(t * 1.4)
        M4.caballo2d(lz, 960, yb, 34 * k, t, ph=t * 3.2, galope=0.3, color=(246, 242, 236), crin=(214, 210, 214), mirar=-1,
                     jinete=dict(K2.TIPOS["capitan"], tocado="sombrero_ala", ropa=(60, 90, 160), ropa2=(240, 220, 120)), jinete_seed=77, capa=2)
    kl = U.pop(t, t_leyenda) * U.salida(t, T_G - 0.2)
    if kl > 0.01:
        U.llamada(lz, 400, 200, "leyenda", color=U.COL["morado"], px=64, k=kl, cola=None)
    ks = U.pop(t, t_sant) * U.salida(t, T_G - 0.2)
    if ks > 0.01:
        U.llamada(lz, 1500, 180, "el apóstol Santiago", color=U.COL["oro"], px=54, k=ks, cola=None, color_texto=(40, 24, 70))
    snd(t_apostol, "amanecer", 0.4)
    snd(t_cab, "galope", 0.35)


# ------------------------------------------------------------------------------------------------ G. el peñol cae (1542)
@shot(T_G, bg=lambda t: PA.cielo(0.75), post=[acabado], ent=("fundido", 0.6))
def g_cae(lz, t):
    f = float(smooth(prog(t, T_G, t_cayo + 0.4)))
    c = K(t, [(T_G, (180, 190, 70, 0.9)), (t_cayo, (180, 186, 90, 1.0))])
    iso = _iso_pen(c)
    PA.sol(lz, 1560, 220, 60, t, 0.75)
    PA.sierras(lz, t, 10 * (t - T_G), 0.75, y0=360, capas=3, semilla=99)
    PEN.suelo(lz, iso, t)
    m = PEN.objetos(t, guerreros=1.0 - 0.9 * f, cerco=f, fuego=1.0, bandera=float(smooth(prog(t, t_cayo - 0.1, t_cayo + 0.8))), caido=0.5 * f, gente_cerco=1.0)
    m.dibujar(lz, iso)
    yr = int(lerp(1541, 1542, e_inout(prog(t, t_princ, t_dos + 0.5))))
    k = U.pop(t, t_princ) * U.salida(t, T_H - 0.2)
    if k > 0.01:
        AB.contador_atras(lz, 1560, 170, yr, px=150, k=k)
        U.llamada(lz, 1560, 290, "principios de 1542", color=U.COL["naranja"], px=48, k=U.pop(t, t_cuar2), cola=None)
    kc = U.pop(t, t_cayo) * U.salida(t, T_H - 0.2)
    if kc > 0.01:
        sx, sy = iso.P(180, 180, 190)
        U.llamada(lz, float(sx), float(sy) - 140, "el peñol cae", color=U.COL["rojo"], px=64, k=kc * U.repop(t, t_cayo + 0.2), cola="abajo")
    snd(t_cayo, "impacto", 0.5)
    snd(t_princ, "campana", 0.3)


# ------------------------------------------------------------------------------------------------ H. la tradición: el vacío
@shot(T_H, bg=lambda t: bg_grad((60, 22, 70), (236, 120, 92), mid=(170, 60, 96), ym=0.6), post=[acabado, lambda img, t: post_fundido_negro(img, t, T1(E4) - 0.6, T1(E4) - 0.02)], ent=("fundido", 0.7))
def h_vacio(lz, t):
    lz.halo(1500, 700, 520, (255, 190, 120), alfa=0.35, dureza=1.1, capa=0)
    M4.borde_vacio(lz, t)
    AB.petalos(lz, t, t_lanz - 0.1, (900, 760), n=26, dur=3.4, spread=(0.2, 1.2), g=60.0, seed=8, vel=(40, 140), color=((255, 150, 44), (255, 204, 70), (236, 70, 140)))
    k = U.pop(t, t_trad) * U.salida(t, t_lanz + 1.4)
    if k > 0.01:
        U.llamada(lz, 1330, 250, "cuenta la tradición", color=U.COL["blanco"], px=56, k=k, cola=None, color_texto=(60, 20, 70))
    kv = U.pop(t, t_vacio)
    if kv > 0.01:
        U.llamada(lz, 1330, 360, "antes que rendirse", color=U.COL["oscuro"], px=52, k=kv, cola=None)
    snd(t_trad, "viento", 0.3)
    snd(t_lanz, "suspiro", 0.3)
