# -*- coding: utf-8 -*-
"""Escena 11 · Tenamaxtli (6:24-7:07): hijo del señor de Nochistlán y cacique de Nochistlán y Juchipila; casi diez años de guerrilla en la sierra;
identificado hacia 1552 y enviado a España; en Valladolid conoce a fray Bartolomé de las Casas (retrato real); redacta con él una denuncia
al Consejo de Indias (libertad de su pueblo, fin de la encomienda); la presenta el 1 de julio de 1555; muere en Valladolid hacia 1556."""
import math

import numpy as np

import kz_ui as U
import kz_mapa as KM
import kz_mapa_dib as MD
import kz_abstracto as AB
import kz_pers2d as K2
import kz_retrato as RT
import plano as P
import lugares  # noqa: F401
import paisajes as PA
import mapas as MA_
import mundos_a as MA
import mundos_d as MD_
import mundos_j as MJ
import mundos_l as ML
from motor import W, H, prog, lerp, smooth, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, h01, catmull
from reg import shot, snd
from util import *  # noqa: F401,F403
from t01 import acabado

E11 = "tenamaxtli"
MP = KM.MAPA
MD.CIUDADES.setdefault("sevilla", (-5.98, 37.39))
t_ten, t_hijo, t_senor, t_noch, t_cacique, t_noch2, t_juch = (T(E11, "tenamaxtli", frase=0), T(E11, "hijo", frase=0), T(E11, "senor", frase=0), T(E11, "nochistlan", frase=0),
                                                             T(E11, "cacique", frase=0), T(E11, "nochistlan", frase=0, n=1), T(E11, "juchipila", frase=0))
t_paso, t_diez, t_huyendo, t_guerr, t_sierras = T(E11, "paso", frase=1), T(E11, "diez", frase=1), T(E11, "huyendo", frase=1), T(E11, "guerrillero", frase=1), T(E11, "sierras", frase=1)
t_hacia, t_identif, t_autor, t_enviarlo, t_espana, t_juzgarlo = (T(E11, "hacia", frase=2), T(E11, "identificaron", frase=2), T(E11, "autoridades", frase=2), T(E11, "enviarlo", frase=2),
                                                                 T(E11, "espana", frase=2), T(E11, "juzgarlo", frase=2))
t_valladolid, t_conocio, t_bartolome, t_casas, t_defensor = (T(E11, "valladolid", frase=3), T(E11, "conocio", frase=3), T(E11, "bartolome", frase=3), T(E11, "casas", frase=3),
                                                             T(E11, "defensor", frase=3))
t_ayuda, t_redacto, t_denuncia, t_consejo, t_pedia, t_libertad, t_fin, t_encom = (T(E11, "ayuda", frase=4), T(E11, "redacto", frase=4), T(E11, "denuncia", frase=4), T(E11, "consejo", frase=4),
                                                                                  T(E11, "pedia", frase=4), T(E11, "libertad", frase=4), T(E11, "fin", frase=4), T(E11, "encomienda", frase=4))
t_presento, t_primero, t_julio, t_jefe, t_justicia, t_corona = (T(E11, "presento", frase=5), T(E11, "primero", frase=5), T(E11, "julio", frase=5), T(E11, "jefe", frase=5),
                                                                T(E11, "justicia", frase=5), T(E11, "corona", frase=5))
t_murio, t_valla2, t_cincuenta, t_volver, t_tierra = T(E11, "murio", frase=6), T(E11, "valladolid", frase=6), T(E11, "cincuenta", frase=6), T(E11, "volver", frase=6), T(E11, "tierra", frase=6)
T_A, T_B, T_C1, T_C2, T_D, T_E, T_F, T_G = (T0(E11), INI(E11, 1) - 0.15, INI(E11, 2) - 0.15, t_enviarlo - 0.3, INI(E11, 3) - 0.15, INI(E11, 4) - 0.15, INI(E11, 5) - 0.15,
                                             INI(E11, 6) - 0.15)
HITOS = ("1541", "1550", "1552", "1554", "1555", "1556")


def linea_tiempo(lz, t, actual, alfa=1.0, y=990):
    """Línea de tiempo de su vida al pie del cuadro, con un medallón dorado que se desliza (dibujo compartido por varias tomas)."""
    cx, cy = AB.medallon_tiempo(lz, W / 2, y - 70, 26, t, HITOS, actual=actual, ancho=1100, y_linea=y - 70, alfa=alfa)
    lz.relleno(circulo(cx, cy, 26, 24), (250, 206, 90), alfa=alfa, capa=2)
    lz.relleno(circulo(cx, cy, 18, 20), (60, 150, 180), alfa=alfa, capa=2)


# ------------------------------------------------------------------------------------------------ A. ¿Y Tenamaxtli? Linaje
@shot(T_A, bg=lambda t: bg_grad((40, 92, 120), (12, 20, 46), mid=(24, 50, 84), ym=0.55), post=[acabado], ent=("tinta", 0.6))
def a_tenamaxtli(lz, t):
    U.bokeh(lz, t, seed=111, n=10, colores=((70, 200, 210), (255, 206, 80), (122, 90, 255)), alfa=0.3)
    U.chispas(lz, t, n=14, seed=11)
    k = pk(t, T_A + 0.1, 0.6)
    K2.busto(lz, 1220, 960, 150 * k, "jefe_caxcan", t, yaw=-0.35, emocion="pensativo" if t < t_hijo else "serio", ojos="abiertos", seed=31)
    kq = U.pop(t, T_A + 0.2) * U.salida(t, t_hijo - 0.1)
    if kq > 0.01:
        P.rotulo(lz, 1530, 300, "?", px=200, k=0.7 + 0.3 * kq, color=(255, 214, 90), alfa=kq)
    k = U.pop(t, t_ten)
    if k > 0.01:
        U.llamada(lz, 1220, 170, "Tenamaxtli", color=U.COL["teal"], px=72, k=k, cola=None)
    # su padre, el señor de Nochistlán, en un medallón con una línea hacia él
    kp = pk(t, t_hijo - 0.1, 0.5)
    if kp > 0.01:
        spec = dict(K2.TIPOS["anciano_caxcan"], tocado="plumas", ropa=(72, 150, 190))
        lz.relleno(circulo(430, 420, 170 * kp, 44), (20, 40, 70), alfa=0.8, capa=1)
        lz.trazo(circulo(430, 420, 170 * kp, 44), (250, 206, 90), 8.0, cerrado=True, temblor=0.0, capa=2)
        with lz.recorte(circulo(430, 420, 166 * kp, 44)):
            K2.busto(lz, 430, 570, 80 * kp, spec, t, yaw=0.35, emocion="serio", ojos="abiertos", seed=33)
        U.llamada(lz, 430, 640, "su padre: señor de Nochistlán", color=U.COL["naranja"], px=36, k=U.pop(t, t_senor), cola=None)
        P.discontinua(lz, [(600, 420), (980, 560)], (255, 255, 255), ancho=5.0, largo=16, hueco=12, fase=-t * 30, capa=2)
    kc = U.pop(t, t_cacique)
    if kc > 0.01:
        for j, (lug, t0, x) in enumerate((("Nochistlán", t_noch2, 330), ("Juchipila", t_juch, 640))):
            kk = pk(t, t0, 0.45)
            if kk > 0.01:
                MA.flor_xuchitl(lz, x, 830, 34 * kk, t, u=1.0, sombra=False) if j == 1 else MD.corona(lz, x, 830, 2.4 * kk, 1.0, t)
                U.llamada(lz, x, 900, lug, color=U.COL["teal"], px=36, k=kk, cola=None)
        U.llamada(lz, 480, 750, "cacique de", color=U.COL["morado"], px=38, k=kc, cola=None)
    linea_tiempo(lz, t, 0.0, alfa=0.0)
    snd(t_ten, "gong", 0.45)


# ------------------------------------------------------------------------------------------------ B. casi diez años de guerrilla en la sierra (lluvia)
def _lluvia(img, t):
    return acabado(post_lluvia(img, t, dens=1.2, alfa=0.35), t)


@shot(T_B, bg=lambda t: PA.cielo(0.95), post=[_lluvia], ent=("tinta", 0.6))
def b_guerrilla(lz, t):
    cx = 220.0 * (t - T_B)
    PA.sierras(lz, t, cx * 0.4, 0.95, y0=560, capas=5, semilla=121)
    p = PA.pal(0.95)
    xs = np.linspace(-40, W + 40, 50)
    cresta = [(x, 860 - 90 * math.sin((x + cx) * 0.003) - 40 * math.sin((x + cx) * 0.009 + 1)) for x in xs]
    lz.relleno(np.array(cresta + [(W + 40, H), (-40, H)]), p["sierras"][4], capa=1)
    for i, (spec, dx, sc) in enumerate((("jefe_caxcan", 0, 30), ("caxcan", -170, 26), ("caxcan", -320, 26), ("caxcana", -460, 25))):
        x = 1060 + dx
        y = 860 - 90 * math.sin((x + cx) * 0.003) - 40 * math.sin((x + cx) * 0.009 + 1)
        K2.cuerpo(lz, x, y + 4, sc, spec, t, piernas="corre", brazos="balanceo", mirar=1, vista="perfil", seed=2000 + i, ph=t * 8.5 + i * 0.9, emocion="serio", lean=0.15)
    for k in range(5):                                                   # matorral en silueta delante (paralaje rápido)
        x = ((k * 470 - cx * 1.6) % (W + 400)) - 200
        lz.relleno(np.array([(x - 90, H + 10), (x - 20, H - 170), (x + 30, H - 120), (x + 90, H + 10)]), (24, 18, 40), capa=2)
    c = int(lerp(1541, 1550, e_inout(prog(t, t_diez - 0.2, T_C1))))
    k = U.pop(t, t_diez - 0.2)
    if k > 0.01:
        lz.texto(str(c), 300, 170, 120, "geo_x", color=(255, 255, 255), borde=None, k=k, alfa=1.0, capa=2, temblor=0.0)
        U.llamada(lz, 300, 270, "casi diez años", color=U.COL["naranja"], px=40, k=k, cola=None)
    k = U.pop(t, t_guerr)
    if k > 0.01:
        U.llamada(lz, 1300, 190, "guerrillero en la sierra", color=U.COL["teal"], px=52, k=k, cola=None)
    linea_tiempo(lz, t, lerp(0.0, 1.0, prog(t, T_B, T_C1)))
    snd(t_huyendo, "galope", 0.3)


# ------------------------------------------------------------------------------------------------ C1. 1552: lo identifican
@shot(T_C1, bg=lambda t: bg_grad((96, 70, 60), (36, 24, 30), mid=(70, 50, 48), ym=0.5), post=[acabado], ent=("tinta", 0.6))
def c1_identificado(lz, t):
    U.bokeh(lz, t, seed=131, n=8, colores=((255, 190, 120), (200, 120, 90)), alfa=0.25)
    ML.orden_busqueda(lz, 760, 520, 1.0, t, pk(t, T_C1 + 0.05, 0.5), sello_k=e_back(prog(t, t_identif, t_identif + 0.35)))
    k = U.pop(t, t_hacia - 0.1)
    if k > 0.01:
        lz.texto("1552", 1450, 360, 150, "geo_x", color=(255, 255, 255), borde=None, k=k, alfa=1.0, capa=2, temblor=0.0)
    k = U.pop(t, t_identif)
    if k > 0.01:
        U.llamada(lz, 1450, 480, "lo identifican", color=U.COL["rojo"], px=50, k=k, cola=None)
    linea_tiempo(lz, t, lerp(1.0, 2.0, prog(t, T_C1, T_C2)))
    snd(t_identif, "bonk", 0.45)


# ------------------------------------------------------------------------------------------------ C2. lo envían a España (mapa del Atlántico)
def cam_c2(t):
    return Klog(t, [(T_C2, (-52.0, 29.0, 0.18)), (T_D, (-46.0, 31.0, 0.19))])


@shot(T_C2, bg=lambda t: MP.base(cam_c2(t), t, exag=12.0, rios_umbral=0.7), post=[acabado], ent=("tinta", 0.6))
def c2_barco(lz, t):
    cam = cam_c2(t)
    MD.mar_vivo(lz, cam, t, seed=12, densidad=0.7)
    MD.ciudad(lz, cam, "veracruz", t, T_C2, tam=0.8, tipo="puerto", nombre="Veracruz", px=24, semilla=3)
    MD.ciudad(lz, cam, "sevilla", t, T_C2 + 0.2, tam=0.8, tipo="puerto", nombre="Sevilla", px=24, semilla=4)
    MD.ciudad(lz, cam, "valladolid_esp", t, T_C2 + 0.3, tam=0.8, tipo="ciudad", nombre="Valladolid", px=24, semilla=5)
    f = e_inout(prog(t, T_C2 + 0.2, T_D + 0.2))
    cab = MA_.ruta_gruesa(lz, cam, ["veracruz", (-80.0, 23.5), (-60.0, 30.0), (-30.0, 36.5), "sevilla", "valladolid_esp"], frac=f, t=t, color=(240, 170, 50), ancho=8, dash=True, flecha=False)
    if cab is not None:
        MD.barco_plano(lz, cab[0], cab[1] - 20, s=1.6, t=t, dir=1)
    k = U.pop(t, t_espana)
    if k > 0.01:
        U.llamada(lz, W / 2, 150, "enviado a España, para juzgarlo", color=U.COL["naranja"], px=56, k=k, cola=None)
    linea_tiempo(lz, t, lerp(2.0, 3.0, prog(t, T_C2, T_D)))
    snd(T_C2 + 0.3, "ola", 0.4)


# ------------------------------------------------------------------------------------------------ D. en Valladolid conoce a fray Bartolomé de las Casas
@shot(T_D, bg=lambda t: bg_plano((150, 126, 118)), post=[acabado], ent=("tinta", 0.6))
def d_lascasas(lz, t):
    ML.sala_valladolid(lz, t)
    kr = pk(t, t_conocio - 0.3, 0.55)
    if kr > 0.01:
        RT.retrato(lz, 480, 900, 175 * (0.9 + 0.1 * kr), "lascasas", t, emocion="serio", alfa=min(1.0, kr * 1.3), seed=6)
    K2.busto(lz, 1440, 980, 135, "jefe_caxcan", t, yaw=-0.45, emocion="pensativo" if t < t_bartolome else "neutro", ojos="abiertos", seed=31, mirar=(-0.5, 0.0))
    U.fecha_lugar(lz, t, T_D + 0.1, T_E - 0.1, "Valladolid", "1554")
    k = U.pop(t, t_bartolome)
    if k > 0.01:
        U.llamada(lz, 480, 230, "fray Bartolomé de las Casas", color=U.COL["morado"], px=46, k=k, cola=None)
    k = U.pop(t, t_defensor)
    if k > 0.01:
        U.llamada(lz, 480, 320, "defensor de los indígenas", color=U.COL["teal"], px=38, k=k, cola=None)
    snd(t_bartolome, "pluck", 0.4)


# ------------------------------------------------------------------------------------------------ E. la denuncia: libertad para su pueblo, fin de la encomienda
@shot(T_E, bg=lambda t: bg_plano((110, 70, 54)), post=[acabado], ent=("tinta", 0.6))
def e_denuncia(lz, t):
    lz.relleno(rect_red(0, 0, W, H, 0), (96, 62, 50), capa=0)
    for i in range(9):
        lz.relleno(rect_red(0, 120 * i + 20, W, 8, 0), (86, 54, 44), capa=0)
    U.pergamino_grande(lz, 900, 540, 980, 760, t, t_redacto - 0.4, lineas=(), titulo="Memorial al Consejo de Indias", sello=False)
    escrito = prog(t, t_redacto, t_pedia)
    for i in range(6):                                                  # renglones que se escriben
        f = np.clip(escrito * 6 - i, 0, 1)
        if f > 0:
            lz.relleno(rect_red(520, 330 + 46 * i, 720 * f * (0.8 + 0.2 * h01(5, i)), 12, 6), (120, 80, 60), alfa=0.75, capa=2)
    px_ = 520 + 720 * (np.clip(escrito * 6, 0, 5.999) % 1.0)
    py_ = 330 + 46 * int(np.clip(escrito * 6, 0, 5.999))
    if t < t_libertad:
        ML.pluma(lz, px_, py_, 40, t)
    for j, (t0, txt, col) in enumerate(((t_libertad, "libertad para su pueblo", U.COL["teal"]), (t_fin, "fin de la encomienda", U.COL["rojo"]))):
        k = pk(t, t0 - 0.1, 0.45)
        if k > 0.01:
            y = 680 + 110 * j
            lz.relleno(circulo(560, y, 34 * k, 22), col, capa=2)
            lz.trazo(np.array([(542, y), (556, y + 14), (582, y - 16)]), (255, 255, 255), 7.0, afinar=False, temblor=0.0, capa=2)
            P.rotulo(lz, 620 + 230, y, txt, px=46, color=(90, 60, 50), alfa=min(1.0, k * 1.4), sombra=0.0)
    if t > t_fin + 0.3:                                                 # cadena que se rompe
        u = prog(t, t_fin + 0.3, t_fin + 1.0)
        for sd in (-1, 1):
            for k_ in range(4):
                lz.relleno(elipse(1500 + sd * (30 + 40 * k_ + 60 * u), 760 + 30 * u * k_, 22, 13, 0.4 * sd, 14), (190, 186, 200), capa=2)
    k = U.pop(t, t_ayuda - 0.1) * U.salida(t, t_libertad - 0.1)
    if k > 0.01:
        U.llamada(lz, 1600, 220, "con ayuda de Las Casas", color=U.COL["morado"], px=40, k=k, cola=None)
    linea_tiempo(lz, t, lerp(3.0, 4.0, prog(t, T_E, T_F)))
    snd(t_redacto, "garabato", 0.35)
    snd(t_libertad, "bling", 0.4)
    snd(t_fin, "crujido", 0.4)


# ------------------------------------------------------------------------------------------------ F. 1 de julio de 1555: un jefe rebelde pide justicia ante la Corona
@shot(T_F, bg=lambda t: bg_plano((64, 46, 70)), post=[acabado], ent=("tinta", 0.6))
def f_presenta(lz, t):
    MJ.sala_consejo(lz, t, 10 * (t - T_F))
    lz.halo(960, 300, 500, (255, 220, 160), alfa=0.25, capa=0)
    MD.corona(lz, 960, 200, 4.0, 1.0, t)
    for i, x in enumerate((420, 640, 1280, 1500)):                    # el Consejo escucha
        spec = dict(K2.TIPOS["encomendero"], ropa=(36, 30, 44), ropa2=(240, 236, 226), tocado=None, pelo=((200, 196, 204), (60, 44, 40), (120, 100, 90), (190, 186, 196))[i])
        K2.busto(lz, x, 735, 64, spec, t, yaw=(0.4, 0.3, -0.3, -0.4)[i], emocion="sorpresa" if t > t_jefe else "serio", ojos="abiertos", seed=1600 + i, brazo=False)
    lz.relleno(rect_red(-20, 760, W + 40, 60, 6), (60, 110, 80), capa=1)
    lz.relleno(rect_red(-20, 800, W + 40, 300, 0), (40, 80, 60), capa=1)
    K2.cuerpo(lz, 960, 1070, 38, "jefe_caxcan", t, piernas="idle", brazos="carga", mirar=1, vista="frente", seed=31, emocion="serio")
    MD_.calendario(lz, 1640, 420, 0.9 * pk(t, t_primero - 0.1, 0.45), t, dia="1", mes="JULIO", anio="1555")
    k = U.pop(t, t_jefe)
    if k > 0.01:
        U.llamada(lz, 600, 140, "un jefe rebelde", color=U.COL["teal"], px=52, k=k, cola=None)
    k = U.pop(t, t_justicia)
    if k > 0.01:
        U.llamada(lz, 600, 230, "pidiendo justicia ante la Corona", color=U.COL["oro"], px=44, k=k, cola=None, color_texto=(60, 36, 20))
    snd(t_presento, "pop", 0.4)
    snd(t_justicia, "campana", 0.4)


# ------------------------------------------------------------------------------------------------ G. murió en Valladolid hacia 1556, sin volver a su tierra
@shot(T_G, bg=lambda t: bg_plano((52, 44, 70)), post=[lambda img, t: acabado(U.gradacion(img, saturacion=0.7), t)], ent=("fundido", 0.6))
def g_muerte(lz, t):
    ML.ventana_lluvia(lz, t)
    MA.flor_xuchitl(lz, 1180, 845, 46, t, u=1.0 - 0.6 * smooth(prog(t, t_murio, t_tierra + 0.5)), seed=6, alfa=0.95, sombra=False)
    U.fecha_lugar(lz, t, t_valla2 - 0.1, T1(E11) + 1.0, "Valladolid", "hacia 1556")
    k = U.pop(t, t_volver)
    if k > 0.01:
        U.llamada(lz, 620, 300, "sin volver a su tierra", color=U.COL["oscuro"], px=50, k=k, cola=None)
    linea_tiempo(lz, t, lerp(4.0, 5.0, prog(t, T_G, t_cincuenta + 0.3)))
    snd(t_murio, "campana", 0.35)
