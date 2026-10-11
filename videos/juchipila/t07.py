# -*- coding: utf-8 -*-
"""Escena 7 · la guerra del Mixtón (3:49-4:29): los españoles fracasan ante el peñol, Oñate pide ayuda a México, llega Pedro de Alvarado
(retrato real; el hombre de la matanza del Templo Mayor), ataca en junio de 1541 contra miles de caxcanes de Tenamaxtli, el ataque fracasa,
un caballo le cae encima en la retirada, muere diez días después en Guadalajara, y los caxcanes, confiados, atacan Guadalajara sin tomarla."""
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
import mundos_d as MD_
import mundos_h as MH
from motor import W, H, prog, lerp, smooth, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, h01, catmull
from reg import shot, snd
from util import *  # noqa: F401,F403
from t01 import acabado

E7 = "mixton"
MP = KM.MAPA
PEN = MH.PenolIso()
t_intent, t_aplastar, t_fracas, t_cris, t_pidio, t_ayuda, t_capital = (T(E7, "intentaron", frase=0), T(E7, "aplastar", frase=0), T(E7, "fracasaron", frase=0), T(E7, "cristobal", frase=0),
                                                                        T(E7, "pidio", frase=0), T(E7, "ayuda", frase=0), T(E7, "capital", frase=0))
t_llego, t_temidos, t_america, t_pedro, t_alv, t_matanza, t_templo = (T(E7, "llego", frase=1), T(E7, "temidos", frase=1), T(E7, "america", frase=1), T(E7, "pedro", frase=1),
                                                                      T(E7, "alvarado", frase=1), T(E7, "matanza", frase=1), T(E7, "templo", frase=1))
t_junio, t_ataco, t_cuatroc, t_aliados, t_enfrente, t_miles, t_guerreros, t_dirig, t_jefe, t_tenam = (T(E7, "junio", frase=2), T(E7, "ataco", frase=2), T(E7, "cuatrocientos", frase=2),
                                                                                                       T(E7, "aliados", frase=2), T(E7, "enfrente", frase=2), T(E7, "miles", frase=2),
                                                                                                       T(E7, "guerreros", frase=2), T(E7, "dirigidos", frase=2), T(E7, "jefe", frase=2),
                                                                                                       T(E7, "tenamaxtli", frase=2))
t_ataque, t_fracaso, t_retirada, t_caballo, t_cayo, t_aplasto = (T(E7, "ataque", frase=3), T(E7, "fracaso", frase=3), T(E7, "retirada", frase=3), T(E7, "caballo", frase=3),
                                                                 T(E7, "cayo", frase=3), T(E7, "aplasto", frase=3))
t_murio, t_diez, t_cuatro, t_julio, t_guad = T(E7, "murio", frase=4), T(E7, "diez", frase=4), T(E7, "cuatro", frase=4), T(E7, "julio", frase=4), T(E7, "guadalajara", frase=4)
t_llenaron, t_confianza, t_atacaron, t_incluso, t_guad2, t_lograron, t_tomarla = (T(E7, "llenaron", frase=5), T(E7, "confianza", frase=5), T(E7, "atacaron", frase=5), T(E7, "incluso", frase=5),
                                                                                  T(E7, "guadalajara", frase=5), T(E7, "lograron", frase=5), T(E7, "tomarla", frase=5))
T_A, T_B, T_C, T_D1, T_D2, T_E, T_F, T_G1, T_G2 = (T0(E7), t_cris - 0.25, INI(E7, 1) - 0.15, INI(E7, 2) - 0.15, t_enfrente - 0.2, INI(E7, 3) - 0.15, INI(E7, 4) - 0.15,
                                                   INI(E7, 5) - 0.15, t_atacaron - 0.25)


def peñol_fondo(lz, t, cx, amb):
    PA.sol(lz, 1560, 220, 60, t, amb)
    PA.sierras(lz, t, cx, amb, y0=480, capas=4, semilla=41)
    DC.aves(lz, t, n=6, seed=8)


# ------------------------------------------------------------------------------------------------ A. intentaron aplastar la rebelión... y fracasaron
def cam_a(t):
    return K(t, [(T_A, (-30, 150, 110, 1.45)), (t_fracas, (-30, 120, 150, 1.65)), (T_B, (-30, 110, 160, 1.72))])


@shot(T_A, bg=lambda t: PA.cielo(0.3), post=[acabado], ent=("tinta", 0.6))
def a_fracaso(lz, t):
    cx, cy, cz, zm = cam_a(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    peñol_fondo(lz, t, 20 * (t - T_A), 0.3)
    PEN.suelo(lz, iso, t)
    PEN.penol(lz, iso, t)
    piedras = smooth(prog(t, t_aplastar, t_fracas))
    PEN.defensores(lz, iso, t, piedras=piedras)
    PEN.atacantes(lz, iso, t, asalto=smooth(prog(t, T_A, t_aplastar + 0.6)), retirada=smooth(prog(t, t_fracas - 0.2, T_B + 0.4)))
    PEN.lluvia_piedras(lz, iso, t, piedras)
    PEN.flechas(lz, iso, t, piedras)
    k = U.pop(t, t_intent) * U.salida(t, t_fracas - 0.15)
    if k > 0.01:
        U.llamada(lz, 520, 150, "intentaron aplastarla...", color=U.COL["rojo"], px=58, k=k, cola=None)
    k = U.pop(t, t_fracas)
    if k > 0.01:
        U.llamada(lz, 520, 150, "...y fracasaron", color=U.COL["teal"], px=64, k=k * U.repop(t, t_fracas + 0.5), cola=None)
    snd(t_aplastar, "tambor", 0.45)
    snd(t_fracas, "whoosh", 0.4)


# ------------------------------------------------------------------------------------------------ B. Oñate pide ayuda a la capital (mapa)
def cam_b(t):
    return Klog(t, [(T_B, (-101.4, 20.6, 1.25)), (T_C, (-101.2, 20.4, 1.35))])


@shot(T_B, bg=lambda t: MP.base(cam_b(t), t, exag=12.0, rios_umbral=0.7), post=[acabado], ent=("tinta", 0.6))
def b_ayuda(lz, t):
    cam = cam_b(t)
    MD.mar_vivo(lz, cam, t, seed=7)
    MD.montes(lz, cam)
    MD.ciudad(lz, cam, "mexico", t, T_B + 0.1, tam=1.1, tipo="ciudad", nombre="México", px=28, semilla=2)
    MD.ciudad(lz, cam, "guadalajara", t, T_B + 0.2, tam=0.9, tipo="ciudad", nombre="Guadalajara", px=24, semilla=3)
    MD.ciudad(lz, cam, "mixton", t, T_B, tam=0.9, tipo="fuerte", nombre="Mixtón", px=24, semilla=5, llama=True)
    f = e_inout(prog(t, t_pidio - 0.1, t_capital + 0.5))
    cab = MA_.ruta_gruesa(lz, cam, ["guadalajara", (-101.6, 20.0), "mexico"], frac=f, t=t, color=(240, 170, 50), ancho=9, dash=True, flecha=False)
    if cab is not None:
        MH.sobre(lz, cab[0], cab[1] - 40, 22, rot=0.15 * math.sin(t * 6))
    kb = pk(t, t_cris, 0.5)
    if kb > 0.01:
        lz.relleno(circulo(300, 760, 240 * kb, 48), (30, 12, 60), alfa=0.55, capa=1)
        with lz.recorte(circulo(300, 760, 240 * kb, 48)):
            K2.busto(lz, 300, 940, 125 * kb, "capitan", t, yaw=0.45, emocion="preocupado", ojos="abiertos", seed=13, habla=0.6 if t_cris < t < t_ayuda + 0.6 else 0.0)
        U.llamada(lz, 300, 1010, "Cristóbal de Oñate", color=U.COL["rojo"], px=44, k=kb, cola=None)
    k = U.pop(t, t_ayuda)
    if k > 0.01:
        U.llamada(lz, 1320, 160, "pide ayuda a México", color=U.COL["naranja"], px=58, k=k, cola=None)
    snd(t_pidio, "whoosh", 0.35)
    snd(t_capital, "pop", 0.35)


# ------------------------------------------------------------------------------------------------ C. llega Pedro de Alvarado (retrato real)
@shot(T_C, bg=lambda t: bg_grad((84, 22, 60), (20, 6, 30), mid=(54, 14, 52), ym=0.55), post=[acabado], ent=("tinta", 0.6))
def c_alvarado(lz, t):
    U.bokeh(lz, t, seed=61, n=10, colores=((236, 70, 90), (122, 90, 255), (255, 150, 44)), alfa=0.30)
    U.haces_luz(lz, 620, 560, t, n=8, largo=1300, color=(255, 200, 200), alfa=0.10)
    ka = pk(t, T_C + 0.1, 0.55)
    if ka > 0.01:
        RT.retrato(lz, 620, 980, 200 * (0.9 + 0.1 * ka), "alvarado", t, emocion="serio", alfa=min(1.0, ka * 1.3), seed=7)
    k = U.pop(t, T_C + 0.3) * U.salida(t, t_pedro - 0.1)
    if k > 0.01:
        U.llamada(lz, 1360, 300, "uno de los más temidos", color=U.COL["rojo"], px=56, k=k, cola=None)
    k = U.pop(t, t_pedro)
    if k > 0.01:
        U.llamada(lz, 1360, 300, "Pedro de Alvarado", color=U.COL["rojo"], px=72, k=k * U.repop(t, t_alv + 0.3), cola=None)
    # la matanza del Templo Mayor (1520): el templo con un velo rojo, sin mostrar violencia
    kt = pk(t, t_matanza - 0.2, 0.5)
    if kt > 0.01:
        cx, cy = 1360, 820
        lz.relleno(rect_red(cx - 330 * kt, cy - 280 * kt, 660 * kt, 400 * kt, 26), (250, 240, 230), alfa=0.95, capa=1)
        with lz.recorte(rect_red(cx - 316 * kt, cy - 266 * kt, 632 * kt, 372 * kt, 18)):
            degradado_v(lz, cx - 330, cx + 330, cy - 280, cy + 140, (255, 196, 160), (196, 80, 90), cy - 280, cy + 120)
            MH.templo_mayor(lz, cx, cy + 80, 52 * kt)
            lz.relleno(rect_red(cx - 330, cy - 280, 660, 420, 0), (200, 30, 50), alfa=0.25 * smooth(prog(t, t_templo, t_templo + 0.8)), capa=1)
        U.llamada(lz, cx, cy + 190 * kt, "matanza del Templo Mayor, 1520", color=U.COL["oscuro"], px=36, k=kt, cola=None)
    snd(t_pedro, "gong", 0.55)
    snd(t_matanza, "trueno", 0.35)


# ------------------------------------------------------------------------------------------------ D1. junio de 1541: cuatrocientos españoles y sus aliados
@shot(T_D1, bg=lambda t: PA.cielo(0.25), post=[acabado], ent=("tinta", 0.6))
def d1_ejercito(lz, t):
    cx = 160.0 * (t - T_D1)
    PA.sol(lz, 1500, 230, 64, t, 0.25)
    PA.sierras(lz, t, cx * 0.5, 0.25, y0=600, capas=4, semilla=47)
    p = PA.pal(0.25)
    degradado_v(lz, 0, W, 760, H, p["pasto"][0], p["pasto"][1], 760, H)
    lz.trazo(np.array([(x, 950 + 6 * math.sin((x + cx) * 0.005)) for x in np.linspace(-40, W + 40, 30)]), (226, 206, 160), 90.0, afinar=False, temblor=0.0, capa=1)
    # columna en marcha: jinetes delante, infantería, aliados detrás (avanzan hacia la derecha)
    v = K2.v_marcha(20)
    for i in range(16):
        x = 1560 - i * 150 + (t - T_D1) * v * 0.6 - 80 * (i > 2)
        y = 960 + 14 * (i % 2)
        if i < 3:
            MH.caballo2d(lz, x, y, 15, t, ph=t * 9 + i, galope=1.0, color=((120, 76, 52), (226, 220, 210), (90, 60, 50))[i], jinete="capitan" if i == 0 else "soldado", jinete_seed=i)
        else:
            spec = "soldado" if i < 9 else K2.variar("caxcan", 900 + i)
            if i >= 9:
                spec = dict(spec, tocado="cinta", ropa=(240, 236, 222), ropa2=(214, 70, 70))
            K2.cuerpo(lz, x, y, 27, spec, t, piernas="camina", brazos="balanceo", mirar=1, vista="perfil", seed=i + 20, ph=t * 5.5 + i)
    PA.flores_frente(lz, t, cx * 1.6, n=10, amb=0.25, y0=1000, seed=14)
    # calendario y cifras
    U.fecha_lugar(lz, t, t_junio - 0.2, T_D2 - 0.1, "rumbo al Mixtón", "junio de 1541")
    k = U.pop(t, t_cuatroc)
    if k > 0.01:
        lz.texto("400", 1060, 210, 150, "geo_x", color=(255, 255, 255), borde=None, k=k, alfa=1.0, capa=2, temblor=0.0)
        U.llamada(lz, 1060, 320, "españoles", color=U.COL["rojo"], px=48, k=k, cola=None)
    k = U.pop(t, t_aliados)
    if k > 0.01:
        U.llamada(lz, 1560, 320, "+ aliados indígenas", color=U.COL["magenta"], px=48, k=k, cola=None)
    snd(t_ataco, "galope", 0.5)


# ------------------------------------------------------------------------------------------------ D2. enfrente: miles de caxcanes con Tenamaxtli
def cam_d2(t):
    return K(t, [(T_D2, (-20, 140, 150, 1.4)), (T_E, (-20, 110, 190, 1.6))])


@shot(T_D2, bg=lambda t: PA.cielo(0.4), post=[acabado], ent=("tinta", 0.6))
def d2_tenamaxtli(lz, t):
    cx, cy, cz, zm = cam_d2(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    peñol_fondo(lz, t, 20 * (t - T_D2), 0.4)
    PEN.suelo(lz, iso, t)
    PEN.penol(lz, iso, t)
    PEN.defensores(lz, iso, t, n=22, piedras=smooth(prog(t, t_guerreros, t_guerreros + 0.5)))
    PEN.atacantes(lz, iso, t, asalto=smooth(prog(t, T_D2, T_E)), retirada=0.0)
    # corrientes de guerreros que bajan de la cumbre (abstracción de «miles»)
    a = smooth(prog(t, t_miles - 0.1, t_miles + 0.6))
    if a > 0.01:
        for j, x0 in enumerate((-120, -40, 40)):
            p0 = iso.P(x0, 90, MH.ZT)
            p1 = iso.P(x0 - 30, 150, MH.ZT * 0.5)
            p2 = iso.P(x0 - 20, 220, 0)
            AB.corriente(lz, t, [p0, p1, p2], n=26, ancho=34.0, vel=0.25, color=((72, 200, 200), (90, 150, 240)), r=(5.0, 9.0), seed=30 + j, capa=2, alfa=a)
    k = U.pop(t, t_miles)
    if k > 0.01:
        U.llamada(lz, 480, 150, "miles de guerreros caxcanes", color=U.COL["teal"], px=54, k=k, cola=None)
    # Tenamaxtli (no hay retrato de época: dibujado)
    kt = pk(t, t_jefe - 0.1, 0.5)
    if kt > 0.01:
        lz.relleno(circulo(1560, 700, 250 * kt, 48), (30, 12, 60), alfa=0.6, capa=1)
        lz.trazo(circulo(1560, 700, 250 * kt, 48), (250, 206, 90), 10.0, cerrado=True, temblor=0.0, capa=2)
        with lz.recorte(circulo(1560, 700, 245 * kt, 48)):
            K2.busto(lz, 1560, 900, 120 * kt, "jefe_caxcan", t, yaw=-0.4, emocion="serio", ojos="abiertos", seed=31)
        U.llamada(lz, 1560, 990, "Tenamaxtli", color=U.COL["teal"], px=54, k=kt * U.repop(t, t_tenam + 0.3), cola=None)
    snd(t_miles, "tambor", 0.5)
    snd(t_tenam, "gong", 0.45)


# ------------------------------------------------------------------------------------------------ E. el ataque fracasa; en la retirada el caballo cae sobre Alvarado
def _ladera_y(x):
    return 560 + 0.36 * x + 30 * math.sin(x * 0.006)


@shot(T_E, bg=lambda t: PA.cielo(0.55), post=[acabado], ent=("tinta", 0.6))
def e_caida(lz, t):
    cxp = 26.0 * (t - T_E)
    PA.sol(lz, 300, 220, 58, t, 0.55)
    PA.sierras(lz, t, cxp, 0.55, y0=560, capas=4, semilla=52)
    # ladera empinada del peñol (de arriba a la izquierda hacia abajo a la derecha)
    xs = np.linspace(-60, W + 60, 40)
    lz.relleno(np.array([(x, _ladera_y(x)) for x in xs] + [(W + 60, H + 40), (-60, H + 40)]), (176, 120, 110), capa=1)
    lz.relleno(np.array([(x, _ladera_y(x) + 26) for x in xs] + [(W + 60, H + 40), (-60, H + 40)]), (150, 100, 104), capa=1)
    for k in range(18):
        x = 60 + 105 * k
        y = _ladera_y(x) + 70 + 120 * h01(4, k)
        lz.relleno(elipse(x, y, 30 + 20 * h01(5, k), 14, -0.3, 14), (130, 90, 100), alfa=0.8, capa=1)
    # piedras y polvo que bajan por la ladera
    for k in range(10):
        u = ((t * 0.6 + h01(9, k)) % 1.0)
        x = 100 + 1700 * u
        lz.relleno(circulo(x, _ladera_y(x) - 14, 12 + 8 * h01(9, k, 2), 10), (110, 90, 96), capa=2)
    # retirada: soldados que bajan corriendo (hacia la derecha) y el caballo de Alvarado que resbala y cae
    for i in range(6):
        x = 520 + 230 * i + 200 * (t - T_E)
        K2.cuerpo(lz, x, _ladera_y(x), 24, "soldado", t, piernas="corre", brazos="balanceo", mirar=1, vista="perfil", seed=80 + i, emocion="miedo", ph=t * 8 + i,
                  lean=0.15)
    u_c = prog(t, t_caballo - 0.1, t_aplasto + 0.2)                     # 0..1 la caída
    xh = 420 + 260 * prog(t, T_E, t_caballo) + 280 * e_out(u_c)
    yh = _ladera_y(xh)
    rot = 0.36 + 1.9 * e_in(min(1.0, u_c * 1.15))
    with lz.grupo(xh, yh - 40 * math.sin(math.pi * min(1.0, u_c)), 1.0, rot):
        MH.caballo2d(lz, 0, 0, 19, t, ph=t * 12, galope=1.0 - u_c, color=(120, 76, 52), mirar=1, jinete="capitan" if u_c < 0.35 else None, jinete_seed=2, patas_caida=smooth(u_c))
    if u_c > 0.3:                                                        # el jinete sale despedido detrás del caballo (sin mostrar el golpe)
        jx = xh - 120 + 160 * e_out(prog(t, t_cayo, t_aplasto))
        K2.cuerpo(lz, jx, _ladera_y(jx) + 8, 21, "capitan", t, piernas="sentado", brazos="defensa", mirar=1, vista="perfil", seed=2, emocion="miedo", alfa=1.0 - smooth(prog(t, t_aplasto, t_aplasto + 0.3)))
    MH.polvo2d(lz, xh + 60, yh, t, t_aplasto - 0.1, dur=1.6, n=18, s=1.4, seed=4)
    k = U.pop(t, t_fracaso - 0.1) * U.salida(t, t_retirada - 0.1)
    if k > 0.01:
        U.llamada(lz, 1300, 150, "el ataque fracasó", color=U.COL["teal"], px=60, k=k, cola=None)
    k = U.pop(t, t_retirada) * U.salida(t, t_aplasto - 0.1)
    if k > 0.01:
        U.llamada(lz, 1300, 150, "en la retirada...", color=U.COL["naranja"], px=60, k=k, cola=None)
    k = U.pop(t, t_aplasto + 0.2)
    if k > 0.01:
        U.llamada(lz, 1300, 150, "un caballo cayó sobre Alvarado", color=U.COL["rojo"], px=56, k=k, cola=None)
    snd(t_caballo, "galope", 0.5)
    snd(t_aplasto, "bonk", 0.55)
    snd(t_aplasto + 0.05, "crujido", 0.4)


# ------------------------------------------------------------------------------------------------ F. murió diez días después, el 4 de julio, en Guadalajara
GRIS = lambda img, t: acabado(U.gradacion(img, luces=(0.92, 0.88, 0.95), sombras=(0.86, 0.84, 0.95), contraste=1.0, saturacion=0.6), t)


@shot(T_F, bg=lambda t: bg_grad((62, 48, 86), (20, 14, 34), mid=(40, 30, 60), ym=0.55), post=[GRIS], ent=("fundido", 0.5))
def f_muerte(lz, t):
    U.bokeh(lz, t, seed=71, n=8, colores=((160, 150, 200), (110, 90, 160)), alfa=0.25)
    RT.retrato(lz, 560, 960, 190, "alvarado", t, emocion="serio", seed=7)
    c = smooth(prog(t, t_murio, t_murio + 0.5))
    if c > 0.01:                                                         # crespón negro
        lz.relleno(np.array([(700, 330), (780, 330), (800, 330 + 200 * c), (800, 430 + 200 * c)]), (16, 12, 24), alfa=0.95, capa=2)
    # calendario: del 24 de junio al 4 de julio (diez días)
    d = int(lerp(24, 34, e_inout(prog(t, t_diez - 0.2, t_julio + 0.2))))
    dia, mes = (str(d), "JUNIO") if d <= 30 else (str(d - 30), "JULIO")
    MD_.calendario(lz, 1360, 540, 1.5, t, dia=dia, mes=mes, anio="1541")
    k = U.pop(t, t_diez)
    if k > 0.01:
        U.llamada(lz, 1360, 120, "diez días después", color=U.COL["oscuro"], px=56, k=k, cola=None)
    k = U.pop(t, t_guad)
    if k > 0.01:
        U.llamada(lz, 1360, 880, "en Guadalajara", color=U.COL["morado"], px=52, k=k, cola=None)
    snd(t_murio, "campana", 0.4)


# ------------------------------------------------------------------------------------------------ G1. los caxcanes se llenan de confianza
@shot(T_G1, bg=lambda t: PA.cielo(0.1), post=[acabado], ent=("fundido", 0.5))
def g1_confianza(lz, t):
    cx = 40.0 * (t - T_G1)
    PA.sol(lz, 960, 520, 110, t, 0.1)
    U.haces_luz(lz, 960, 520, t, n=10, largo=1300, color=(255, 230, 170), alfa=0.12)
    PA.sierras(lz, t, cx, 0.1, y0=700, capas=3, semilla=61)
    lz.relleno(np.array([(0, 820), (W, 790), (W, H), (0, H)]), (132, 100, 110), capa=1)
    lz.relleno(np.array([(0, 840), (W, 812), (W, H), (0, H)]), (110, 84, 100), capa=1)
    # guerreros en la cumbre que celebran (siluetas al contraluz y personajes delante)
    for i in range(14):
        x = 120 + 130 * i + 30 * h01(3, i)
        K2.cuerpo(lz, x, 830 - 10 * h01(4, i), 17, K2.variar("caxcan", 950 + i), t, piernas="baila" if i % 3 == 0 else "idle", brazos="arriba", mirar=1 if i % 2 else -1,
                  vista="frente" if i % 4 == 0 else "perfil", seed=950 + i, emocion="alegre")
    K2.busto(lz, 1480, 1080, 112, "jefe_caxcan", t, yaw=-0.35, emocion="alegre", ojos="abiertos", seed=31)
    AB.petalos(lz, t, t_confianza, (960, 500), n=30, dur=2.4, seed=12)
    k = U.pop(t, t_confianza - 0.2)
    if k > 0.01:
        U.llamada(lz, 960, 150, "confianza", color=U.COL["oro"], px=72, k=k * U.repop(t, t_confianza + 0.4), cola=None, color_texto=(60, 36, 20))
    snd(t_confianza, "tambor", 0.5)


# ------------------------------------------------------------------------------------------------ G2. atacan Guadalajara y no logran tomarla
def cam_g2(t):
    return Klog(t, [(T_G2, (-103.2, 21.05, 3.6)), (T1(E7), (-103.25, 20.95, 4.0))])


@shot(T_G2, bg=lambda t: MP.base(cam_g2(t), t, exag=12.0, rios_umbral=0.7), post=[acabado], ent=("tinta", 0.6))
def g2_guadalajara(lz, t):
    cam = cam_g2(t)
    MD.montes(lz, cam)
    MD.ciudad(lz, cam, "mixton", t, T_G2, tam=1.0, tipo="fuerte", nombre="Mixtón", px=26, semilla=5)
    MD.ciudad(lz, cam, "guadalajara", t, T_G2, tam=1.3, tipo="fuerte", nombre="Guadalajara", px=30, semilla=3)
    # tres flechas de ataque que llegan a la ciudad y rebotan
    gx, gy = MA_.proy(cam, "guadalajara")
    mx, my = MA_.proy(cam, "mixton")
    for j, dy in enumerate((-60, 0, 60)):
        f = e_inout(prog(t, t_atacaron + 0.15 * j, t_guad2 + 0.6 + 0.15 * j))
        reb = e_out(prog(t, t_lograron + 0.1 * j, t_tomarla + 0.6))
        if f > 0.01:
            x1 = mx + (gx - mx) * f * (1 - 0.35 * reb)
            y1 = my + dy * 0.5 + (gy - 40 + dy * 0.4 - my - dy * 0.5) * f * (1 - 0.35 * reb)
            MA_.flecha_pantalla(lz, mx, my + dy * 0.5, x1, y1, color=(60, 190, 190), ancho=22, alfa=1.0 - 0.5 * reb)
    if t > t_lograron:                                                   # el muro aguanta: escudo y destello
        k = pk(t, t_lograron, 0.4)
        lz.relleno(circulo(gx, gy - 30, 90 * k, 36), (255, 255, 255), alfa=0.25, capa=2)
        lz.trazo(circulo(gx, gy - 30, 90 * k, 36), (255, 255, 255), 6.0, cerrado=True, temblor=0.0, capa=2)
    k = U.pop(t, t_incluso)
    if k > 0.01:
        U.llamada(lz, 1360, 150, "atacan Guadalajara", color=U.COL["teal"], px=60, k=k, cola=None)
    k = U.pop(t, t_lograron)
    if k > 0.01:
        U.llamada(lz, 1360, 250, "pero no la toman", color=U.COL["rojo"], px=56, k=k, cola=None)
    MD.escala(lz, 80, H - 70, cam, km=50)
    snd(t_atacaron, "tambor", 0.5)
    snd(t_lograron, "bonk", 0.4)
