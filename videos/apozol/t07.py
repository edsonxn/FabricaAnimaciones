# -*- coding: utf-8 -*-
"""Escena 7 · hoy: municipalidad (1863) y municipio libre (1918) en una línea de tiempo a escala, el ministro nacido aquí, la plaza de hoy con su
laurel y su monumento, la fiesta de la Ascensión, los tastoanes, los dos nombres de agua y la carretera que sigue hacia el norte."""
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
import mundos_1 as M1
import mundos_2 as M2
import mundos_4 as M4
import mundos_7 as M7
from motor import W, H, prog, lerp, smooth, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, h01
from reg import shot, snd
from util import *  # noqa: F401,F403
from t01 import acabado

E7 = "hoy"
MP = KM.MAPA
PLAZA = M7.Plaza()
CANON = M2.Canon()
t_1863, t_gob, t_jesus, t_gonz, t_apoz, t_cat, t_munic = (T(E7, "ochocientos", frase=0), T(E7, "gobierno", frase=0), T(E7, "jesus", frase=0), T(E7, "gonzalez", frase=0),
                                                          T(E7, "apozol", frase=0), T(E7, "categoria", frase=0), T(E7, "municipalidad", frase=0))
t_novec, t_diec, t_term, t_rev, t_const, t_libre = (T(E7, "novecientos", frase=1), T(E7, "dieciocho", frase=1), T(E7, "terminar", frase=1), T(E7, "revolucion", frase=1),
                                                    T(E7, "constituido", frase=1), T(E7, "libre", frase=1))
t_hoy, t_cab, t_viven, t_dos, t_pers, t_munic2, t_seis = (T(E7, "hoy", frase=2), T(E7, "cabecera", frase=2), T(E7, "viven", frase=2), T(E7, "dos", frase=2), T(E7, "personas", frase=2),
                                                         T(E7, "municipio", frase=2), T(E7, "seis", frase=2))
t_jard, t_templo, t_laurel, t_sombra, t_monum, t_juarez = (T(E7, "jardin", frase=3), T(E7, "templo", frase=3), T(E7, "laurel", frase=3), T(E7, "sombra", frase=3),
                                                           T(E7, "monumento", frase=3), T(E7, "juarez", frase=3))
t_cada, t_fiesta, t_senor, t_asc, t_musica, t_cab2, t_fuegos = (T(E7, "cada", frase=4), T(E7, "fiesta", frase=4), T(E7, "senor", frase=4), T(E7, "ascension", frase=4),
                                                               T(E7, "musica", frase=4), T(E7, "caballos", frase=4), T(E7, "fuegos", frase=4))
t_julio, t_bailan, t_tasto, t_danza, t_recu, t_guerra = (T(E7, "julio", frase=5), T(E7, "bailan", frase=5), T(E7, "tastoanes", frase=5), T(E7, "danza", frase=5), T(E7, "recuerda", frase=5),
                                                         T(E7, "guerra", frase=5))
t_apoz2, t_peq, t_dosn, t_nom, t_agua, t_hist, t_corr = (T(E7, "apozol", frase=6), T(E7, "pequeno", frase=6), T(E7, "dos", frase=6), T(E7, "nombres", frase=6), T(E7, "agua", frase=6),
                                                         T(E7, "historia", frase=6), T(E7, "corriendo", frase=6))
t_carr, t_sigue, t_norte, t_sig, t_pueb, t_espera = (T(E7, "carretera", frase=7), T(E7, "sigue", frase=7), T(E7, "norte", frase=7), T(E7, "siguiente", frase=7), T(E7, "pueblo", frase=7),
                                                     T(E7, "espera", frase=7))
T_A = T0(E7)
T_B = INI(E7, 1) - 0.12
T_D = INI(E7, 2) - 0.12
T_E = INI(E7, 3) - 0.12
T_F = INI(E7, 4) - 0.12
T_G = INI(E7, 5) - 0.12
T_H = INI(E7, 6) - 0.12
T_I = INI(E7, 7) - 0.12


def _iso(c):
    return I.Iso(float(c[0]), float(c[1]), float(c[2]), float(c[3]))


def _pie(lz, iso, x, y, z, texto, color, t, t0, t1, px=40, dy=-70, cola="abajo"):
    k = U.pop(t, t0) * U.salida(t, t1)
    if k > 0.01:
        sx, sy = iso.P(x, y, z)
        U.llamada(lz, float(sx), float(sy) + dy, texto, color=color, px=px, k=k, cola=cola)


# ------------------------------------------------------------------------------------------------ A. 1863: categoría de municipalidad
@shot(T_A, bg=lambda t: bg_grad((60, 40, 110), (200, 120, 110), mid=(120, 70, 120), ym=0.6), post=[acabado], ent=("fundido", 0.7))
def a_municipalidad(lz, t):
    U.bokeh(lz, t, seed=61, n=10, colores=((255, 200, 120), (255, 120, 140), (180, 140, 255)), alfa=0.28)
    U.pergamino_grande(lz, 620, 560, 760, 430, t, T_A + 0.3, lineas=("El pueblo de Apozol", "alcanza la categoría", "de municipalidad"), titulo="Decreto", sello=True)
    ky = U.pop(t, t_1863 - 0.1)
    if ky > 0.01:
        P.rotulo(lz, 1440, 380, "1863", px=220, k=ky, color=(255, 255, 255), alfa=min(1.0, ky * 1.4))
        U._registrar(lz, 1440, 380, 640, 240)
    kg = U.pop(t, t_gob)
    if kg > 0.01:
        U.llamada(lz, 1440, 560, "gobierno de Jesús González Ortega", color=U.COL["morado"], px=44, k=kg, cola=None)
    km = U.pop(t, t_cat)
    if km > 0.01:
        U.llamada(lz, 1440, 680, "MUNICIPALIDAD", color=U.COL["naranja"], px=70, k=km * U.repop(t, t_munic + 0.1), cola=None)
    snd(t_1863, "campana", 0.3)
    snd(t_cat, "sello", 0.5)


# ------------------------------------------------------------------------------------------------ B. 1918: municipio libre
@shot(T_B, bg=lambda t: bg_grad((30, 20, 70), (120, 60, 110), mid=(70, 36, 96), ym=0.6), post=[acabado], ent=("fundido", 0.6))
def b_libre(lz, t):
    U.bokeh(lz, t, seed=63, n=8, colores=((255, 200, 120), (255, 120, 140)), alfa=0.25)
    M7.linea_tiempo(lz, t, 1850, 1930, 600, 160, 1760, [(1863, "1863 · municipalidad", U.COL["naranja"], T_B + 0.4), (1918, "1918 · municipio libre", U.COL["teal"], t_diec)], T_B + 0.1,
                    banda=(1910, 1920, "Revolución", (214, 60, 70)))
    k = U.pop(t, t_libre)
    if k > 0.01:
        U.llamada(lz, W / 2, 250, "MUNICIPIO LIBRE", color=U.COL["teal"], px=84, k=k * U.repop(t, t_libre + 0.2), cola=None)
    snd(t_diec, "pop", 0.4)
    snd(t_libre, "bling", 0.4)


# ------------------------------------------------------------------------------------------------ D. hoy: unas dos mil seiscientas personas
@shot(T_D, bg=lambda t: PA.cielo(0.0), post=[acabado], ent=("fundido", 0.6))
def d_hoy(lz, t):
    c = K(t, [(T_D, (200, 150, 0, 0.95)), (T_E - 0.4, (180, 160, 0, 1.15))])
    iso = _iso(c)
    PA.sol(lz, 1560, 200, 62, t, 0.0)
    PA.sierras(lz, t, 14 * (t - T_D), 0.0, y0=330, capas=3, semilla=173)
    DC.aves(lz, t, n=5, seed=13)
    CANON.suelo(lz, iso, t)
    CANON.camino(lz, iso)
    m = CANON.objetos(t, "hoy")
    m.dibujar(lz, iso)
    k = U.pop(t, t_cab) * U.salida(t, T_E - 0.2)
    if k > 0.01:
        n = int(lerp(0, 2600, e_out(prog(t, t_dos - 0.1, t_pers + 0.4))) / 100) * 100
        lz.texto(f"{n:,}".replace(",", " "), 480, 190, 150, "geo_x", color=(255, 255, 255), borde=None, k=k, alfa=1.0, capa=2, temblor=0.0)
        U.llamada(lz, 480, 300, "en la cabecera", color=U.COL["naranja"], px=52, k=k, cola=None)
        U._registrar(lz, 480, 210, 440, 180)
    k = U.pop(t, t_munic2) * U.salida(t, T_E - 0.2)
    if k > 0.01:
        n = int(lerp(0, 6000, e_out(prog(t, t_seis - 0.1, t_seis + 1.0))) / 100) * 100
        lz.texto(f"{n:,}".replace(",", " "), 1500, 190, 150, "geo_x", color=(255, 255, 255), borde=None, k=k, alfa=1.0, capa=2, temblor=0.0)
        U.llamada(lz, 1500, 300, "en todo el municipio", color=U.COL["teal"], px=52, k=k, cola=None)
        U._registrar(lz, 1500, 210, 440, 180)
    snd(t_hoy, "pop", 0.3)


# ------------------------------------------------------------------------------------------------ E. el jardín: laurel y monumento
@shot(T_E, bg=lambda t: PA.cielo(0.0), post=[acabado], ent=("fundido", 0.6))
def e_jardin(lz, t):
    c = K(t, [(T_E, (120, 40, 20, 1.45)), (t_laurel, (150, 70, 30, 1.8)), (T_F - 0.4, (125, 110, 30, 1.95))])
    iso = _iso(c)
    PA.sol(lz, 1560, 200, 62, t, 0.0)
    PA.sierras(lz, t, 14 * (t - T_E), 0.0, y0=330, capas=3, semilla=177)
    PLAZA.suelo(lz, iso, t)
    m = PLAZA.objetos(t)
    m.dibujar(lz, iso)
    _pie(lz, iso, 190, 80, 130, "laurel de la India", U.COL["verde"], t, t_laurel, t_monum - 0.1, px=48, dy=-60)
    _pie(lz, iso, 120, 140, 60, "monumento a Benito Juárez", U.COL["morado"], t, t_monum, T_F - 0.2, px=46, dy=-70)
    k = U.pop(t, t_jard) * U.salida(t, t_laurel - 0.1)
    if k > 0.01:
        U.llamada(lz, 960, 150, "jardín principal", color=U.COL["naranja"], px=62, k=k, cola=None)
    snd(t_jard, "pop", 0.3)


# ------------------------------------------------------------------------------------------------ F. la fiesta del Señor de la Ascensión
@shot(T_F, bg=lambda t: bg_grad((8, 6, 30), (70, 30, 80), mid=(30, 14, 60), ym=0.65), post=[acabado], ent=("fundido", 0.7))
def f_fiesta(lz, t):
    coh = [((300 + 330 * i + 140 * h01(7, i)) % (W - 300) + 150, 250 + 170 * h01(8, i), 200 + 90 * h01(9, i), T_F + 0.5 + 1.3 * i) for i in range(16)]
    M7.fiesta_noche(lz, t, T_F, coh)
    # charros al galope por la calle
    for i, (x0, v, y, col) in enumerate(((-300, 380.0, 1010, (120, 76, 52)), (-900, 340.0, 1035, (60, 42, 40)))):
        x = ((t - T_F) * v + x0) % (W + 1200) - 300
        M4.caballo2d(lz, x, y, 26, t, ph=t * 11.0 + i, galope=1.0, color=col,
                     jinete=dict(K2.TIPOS["revolucionario"], tocado="sombrero_palma", ropa=(240, 232, 208), ropa2=(150, 90, 60)), jinete_seed=40 + i, capa=2, mirar=1)
    k = U.pop(t, t_fiesta) * U.salida(t, T_G - 0.2)
    if k > 0.01:
        U.llamada(lz, 480, 330, "fiesta del Señor de la Ascensión", color=U.COL["oro"], px=54, k=k, cola=None, color_texto=(40, 24, 70))
        U.llamada(lz, 480, 430, "cada año, un jueves de mayo", color=U.COL["blanco"], px=40, k=k, cola=None, color_texto=(60, 20, 70))
    k = U.pop(t, t_musica) * U.salida(t, T_G - 0.2)
    if k > 0.01:
        U.llamada(lz, 1480, 700, "música · caballos · fuegos artificiales", color=U.COL["magenta"], px=46, k=k, cola=None)
    snd(t_fuegos, "estallido", 0.4)
    snd(t_musica, "fanfarria", 0.3)


# ------------------------------------------------------------------------------------------------ G. los tastoanes
@shot(T_G, bg=lambda t: PA.cielo(0.45), post=[acabado], ent=("fundido", 0.7))
def g_tastoanes(lz, t):
    PA.sol(lz, 1500, 380, 80, t, 0.45)
    PA.sierras(lz, t, 8 * (t - T_G), 0.45, y0=600, capas=4, semilla=181)
    p = PA.pal(0.45)
    degradado_v(lz, 0, W, 700, H, (110, 130, 90), (70, 84, 80), 700, H)
    M7.multitud_silueta(lz, 760, t, n=40, x0=-20, x1=W + 20, esc=0.8, color=(40, 30, 60), seed=7, sombreros=0.5)
    lz.relleno(elipse(960, 950, 700, 130, 0, 40), (176, 140, 108), alfa=0.95, capa=0)           # el círculo de baile
    for i in range(26):
        a_ = i * 2 * math.pi / 26
        lz.relleno(elipse(960 + 700 * math.cos(a_), 950 + 130 * math.sin(a_), 20, 12, 0, 10), (120, 100, 90), capa=0)
    # hoguera central
    for j, (col, sc) in enumerate((((236, 60, 48), 1.0), ((255, 138, 40), 0.72), ((255, 224, 96), 0.42))):
        a = 110 * sc * (1 + 0.16 * math.sin(t * 9 + j))
        lz.relleno(np.array([(960 - 36 * sc, 940), (960 + 36 * sc, 940), (960 + 8 * math.sin(t * 7), 940 - a)]), col, capa=1)
    lz.halo(960, 900, 360, (255, 160, 80), alfa=0.35, dureza=1.1, capa=0)
    # el estandarte con el caballo blanco de Santiago
    lz.relleno(rect_red(1420, 330, 14, 560, 0), (120, 84, 60), capa=1)
    lz.relleno(rect_red(1434, 340, 250, 190, 10), (250, 244, 230), capa=1)
    M4.caballo2d(lz, 1560, 480, 9, t, ph=t * 2.0, galope=0.2, color=(240, 236, 228), crin=(200, 196, 196), mirar=1, capa=1)
    # los tastoanes bailan alrededor
    for i in range(11):
        a = t * 0.8 + i * 2 * math.pi / 11
        x = 960 + 500 * math.cos(a)
        yy = 990 + 70 * math.sin(a)
        K2.cuerpo(lz, x, yy, 36 + 7 * math.sin(a), dict(K2.variar("tastoan", 4500 + i), tocado="mascara_tastoan"), t, piernas="baila", brazos="baila",
                  mirar=1 if math.cos(a) < 0 else -1, vista="frente", seed=4500 + i, ph=t * 6 + i)
    k = U.pop(t, t_julio) * U.salida(t, t_tasto - 0.1)
    if k > 0.01:
        U.llamada(lz, 480, 200, "julio", color=U.COL["naranja"], px=80, k=k, cola=None)
    k = U.pop(t, t_tasto) * U.salida(t, T_H - 0.2)
    if k > 0.01:
        U.llamada(lz, 480, 200, "los tastoanes", color=U.COL["morado"], px=70, k=k * U.repop(t, t_danza + 0.1), cola=None)
        U.llamada(lz, 480, 310, "25 de julio, Santiago", color=U.COL["oscuro"], px=44, k=k, cola=None)
    snd(t_tasto, "tambor", 0.45)
    snd(t_bailan, "pasos", 0.35)


# ------------------------------------------------------------------------------------------------ H. dos nombres de agua, una historia que corre
@shot(T_H, bg=lambda t: PA.cielo(0.0), post=[acabado], ent=("fundido", 0.7))
def h_agua(lz, t):
    PA.sol(lz, 1500, 250, 70, t, 0.0)
    U.haces_luz(lz, 1500, 250, t, n=9, largo=1400, color=(255, 236, 190), alfa=0.10)
    PA.sierras(lz, t, 14 * (t - T_H), 0.0, y0=600, capas=5, semilla=191)
    PA.aldea(lz, t, 0.0, y=660, x0=500, x1=1500, n=5, seed=15, rio_h=None)
    M1.agua_con_espuma(lz, -20, W + 40, 780, t, k=1.0, seed=5)
    k = pk(t, t_agua - 0.1, 0.6)
    M1.poza(lz, 420, 940, 260, 90, t, k=pk(t, t_agua + 0.4, 0.6), seed=3)
    a = U.pop(t, t_apoz2 - 0.1)
    AB.titulo_textura(lz, "APOZOL", W / 2, 190, 170, t, paleta=((40, 110, 230), (30, 170, 170), (110, 226, 236), (240, 130, 36), (255, 204, 70)), k=1.0, alfa=min(1.0, a * 1.5))
    ka = U.pop(t, t_nom) * U.salida(t, t_corr + 3.0)
    if ka > 0.01:
        U.llamada(lz, 1320, 880, "agua espumosa", color=U.COL["teal"], px=50, k=ka, cola=None)
        U.llamada(lz, 420, 1040, "en el agua caliente", color=U.COL["rojo"], px=50, k=ka, cola=None)
    kh = U.pop(t, t_hist)
    if kh > 0.01:
        U.llamada(lz, W / 2, 340, "una historia que sigue corriendo", color=U.COL["morado"], px=52, k=kh, cola=None)
    for i in range(7):
        u = ((t - T_H) * 0.15 + i / 7) % 1.0
        M1.gota(lz, 300 + 220 * i, 840 - u * 460, 14 + 8 * h01(4, i), t, k=min(1.0, u * 6) * (1 - u), alfa=0.9, seed=i)
    snd(t_agua, "burbujas", 0.35)


# ------------------------------------------------------------------------------------------------ I. la carretera sigue hacia el norte
def cam_i(t):
    return Klog(t, [(T_I, (-101.3, 21.7, 2.0)), (T1(E7) - 3.0, (-102.1, 22.0, 2.9))])


@shot(T_I, bg=lambda t: MP.base(cam_i(t), t, exag=12.0, rios_umbral=0.7), post=[acabado, lambda img, t: post_fundido_negro(img, t, T1(E7) - 1.0, T1(E7) - 0.02)], ent=("fundido", 0.7))
def i_carretera(lz, t):
    cam = cam_i(t)
    MD.mar_vivo(lz, cam, t, seed=9)
    MD.montes(lz, cam)
    MD.region(lz, cam, "ZACATECAS", (-102.3, 22.9), px=40, alfa=0.7, z_max=3.2)
    MA_.ruta_gruesa(lz, cam, ["guadalajara", (-103.30, 21.00), "mezquital", "moyahua", "juchipila", "apozol"], frac=1.0, t=t, color=(255, 214, 72), ancho=9.0, dash=True, flecha=False, alfa=0.8)
    f = float(smooth(prog(t, t_sigue - 0.1, t_norte + 1.4)))
    head = MA_.ruta_gruesa(lz, cam, ["apozol", "jalpa", "tabasco", "villanueva", "zacatecas"], frac=f, t=t, color=(255, 90, 80), ancho=12.0, dash=True, flecha=True)
    MD.ciudad(lz, cam, "zacatecas", t, T_I, tam=0.8, tipo="ciudad", nombre="Zacatecas", px=24)
    MD.ciudad(lz, cam, "guadalajara", t, T_I + 0.2, tam=0.8, tipo="ciudad", nombre="Guadalajara", px=24)
    MD.ciudad(lz, cam, "apozol", t, T_I + 0.4, tam=1.2, tipo="pueblo", nombre=None, semilla=3)
    MD.onda(lz, cam, "apozol", t, T_I + 0.4, dur=2.4, r_deg=0.3, n=3, ancho=5.0, periodo=0.5, alfa=0.9, color=(255, 214, 90))
    sx, sy = MA_.proy(cam, "apozol")
    k = U.pop(t, T_I + 0.5)
    if k > 0.01:
        U.llamada(lz, float(sx), float(sy) + 70, "Apozol", color=U.COL["naranja"], px=40, k=k, cola="arriba")
    k = U.pop(t, t_carr) * U.salida(t, T1(E7) - 1.0)
    if k > 0.01:
        U.llamada(lz, 500, 220, "carretera federal 54", color=U.COL["oscuro"], px=48, k=k, cola=None)
    k = U.pop(t, t_sig) * U.salida(t, T1(E7) - 1.0)
    if k > 0.01 and head is not None:
        U.llamada(lz, float(head[0]) + 120, float(head[1]) - 40, "¿qué pueblo sigue?", color=U.COL["rojo"], px=54, k=k * U.repop(t, t_pueb + 0.2), cola=None)
    snd(t_sigue, "whoosh", 0.4)
    snd(t_espera, "bling", 0.4)
