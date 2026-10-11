# -*- coding: utf-8 -*-
"""Escena 3 · Las Ventanas (1:02-1:55): el cerro se construye, el apogeo 700-1200, la visita guiada (ciudadela, terrazas, pirámide, juego de pelota, 25 monolitos),
116 hectáreas, la excavación, el muro de huecos sobre el risco y el portón que se abre en 2019."""
import math

import numpy as np

import kz_ui as U
import kz_iso as I
import kz_iso_deco as DC
import kz_abstracto as AB
import kz_pers2d as K2
import plano as P
import paisajes as PA
import mundos_c as MC
import mundos_d as MD2
from motor import W, H, prog, lerp, smooth, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, h01
from reg import shot, snd
from util import *  # noqa: F401,F403
from t01 import acabado

E3 = "ventanas"
t_mucho, t_esp, t_eligio, t_cerro, t_constr, t_ciudad, t_vent = (T(E3, "mucho", frase=0), T(E3, "espanoles", frase=0), T(E3, "eligio", frase=0), T(E3, "cerro", frase=0), T(E3, "construir", frase=0), T(E3, "ciudad", frase=0), T(E3, "ventanas", frase=0))
t_arq, t_setec, t_mil, t_docs, t_era = T(E3, "arqueologos", frase=1), T(E3, "setecientos", frase=1), T(E3, "mil", frase=1), T(E3, "doscientos", frase=1), T(E3, "era", frase=1)
t_arriba, t_ciudadela, t_terrazas, t_pir, t_juego, t_25, t_mono = T(E3, "arriba", frase=2), T(E3, "ciudadela", frase=2), T(E3, "terrazas", frase=2), T(E3, "piramide", frase=2), T(E3, "juego", frase=2), T(E3, "veinticinco", frase=2), T(E3, "monolitos", frase=2)
t_todo, t_ciento, t_hect, t_desarr, t_grande, t_conoce = T(E3, "todo", frase=3), T(E3, "ciento", frase=3), T(E3, "hectareas", frase=3), T(E3, "desarrollo", frase=3), T(E3, "grande", frase=3), T(E3, "conoce", frase=3)
t_prim, t_estud, t_extr, t_finales, t_siglo, t_desde, t_excav, t_revela, t_piedra = (T(E3, "primeros", frase=4), T(E3, "estudiarlo", frase=4), T(E3, "investigadores", frase=4), T(E3, "finales", frase=4), T(E3, "siglo", frase=4),
                                                                                      T(E3, "desde", frase=4), T(E3, "excavacion", frase=4), T(E3, "revela", frase=4), T(E3, "piedra", frase=4))
t_nombre, t_muro, t_huecos, t_risco, t_lejos, t_parecen, t_vent2 = T(E3, "nombre", frase=5), T(E3, "muro", frase=5), T(E3, "huecos", frase=5), T(E3, "risco", frase=5), T(E3, "lejos", frase=5), T(E3, "parecen", frase=5), T(E3, "ventanas", frase=5)
t_siglos, t_nadie, t_visit, t_zona, t_abrio, t_pub, t_dos, t_ago, t_2019 = (T(E3, "siglos", frase=6), T(E3, "nadie", frase=6), T(E3, "visitarlo", frase=6), T(E3, "zona", frase=6), T(E3, "abrio", frase=6),
                                                                              T(E3, "publico", frase=6), T(E3, "dos", frase=6), T(E3, "agosto", frase=6), T(E3, "diecinueve", frase=6))
CV = MC.CerroVentanas()
T_A, T_B, T_C, T_D, T_E, T_F, T_G = T0(E3), FIN(E3, 0) + 0.1, INI(E3, 2) - 0.1, INI(E3, 3) - 0.1, INI(E3, 4) - 0.1, INI(E3, 5) - 0.1, INI(E3, 6) - 0.1


def fondo_iso(lz, t, cx, amb=0.0):
    PA.sol(lz, 1600, 240, 66, t, amb)
    PA.sierras(lz, t, cx, amb, y0=470, capas=4, semilla=17)


def vida(lz, t):
    DC.aves(lz, t, n=6, seed=3)
    DC.polvo_luz(lz, t, n=14, seed=4)


# ------------------------------------------------------------------------------------------------ A. el cerro se construye
def cam_a(t):
    return K(t, [(T_A, (95, 100, 80, 1.40)), (t_ciudad + 0.5, (92, 92, 90, 1.58)), (T_B, (92, 90, 100, 1.62))])


@shot(T_A, bg=lambda t: PA.cielo(0.0), post=[acabado], ent=("fundido", 0.5))
def a_construye(lz, t):
    cx, cy, cz, zm = cam_a(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz(mul=(1.03, 1.0, 0.95), mix=(255, 170, 110), k=0.05)
    fondo_iso(lz, t, 0.0)
    CV.suelo(lz, iso, t)
    u = prog(t, t_constr - 0.1, t_ciudad + 1.7)
    CV.objetos(t, u).dibujar(lz, iso)
    vida(lz, t)
    # el tiempo retrocede: 1530 -> 700
    c = lerp(1530, 700, e_inout(prog(t, t_mucho, t_cerro - 0.1)))
    kc = U.pop(t, t_mucho) * U.salida(t, t_eligio + 0.1, 0.25)
    if kc > 0.01:
        lz.texto(str(int(c)), 330, 200, 170, "geo_x", color=(255, 255, 255), borde=None, k=kc, alfa=1.0, capa=2, temblor=0.0)
        U.llamada(lz, 330, 320, "antes de los españoles", color=U.COL["naranja"], px=42, k=kc, cola="arriba")
    k = U.pop(t, t_eligio) * U.salida(t, t_constr - 0.05, 0.25)
    if k > 0.01:
        sx, sy = iso.P(90, 90, 100)
        lz.halo(float(sx), float(sy), 360 * k, (255, 230, 150), alfa=0.35, dureza=1.1, capa=2)
        U.llamada(lz, float(sx), float(sy) - 330, "alguien eligió un cerro", color=U.COL["magenta"], px=50, k=k, cola="abajo")
    k = U.pop(t, t_constr) * U.salida(t, t_vent - 0.1, 0.25)
    if k > 0.01:
        U.llamada(lz, W - 430, 170, "construir una ciudad", color=U.COL["teal"], px=50, k=k, cola=None)
    k = U.pop(t, t_vent)
    if k > 0.01:
        U.llamada(lz, W - 430, 170, "Cerro de las Ventanas", color=U.COL["morado"], px=58, k=k * U.repop(t, t_vent + 0.8), cola=None)
    for tt in (t_constr + 0.3, t_constr + 1.0, t_constr + 1.7):
        snd(tt, "pop", 0.4)


# ------------------------------------------------------------------------------------------------ B. el apogeo (700-1200)
@shot(T_B, bg=lambda t: PA.cielo(0.0), post=[acabado], ent=("fundido", 0.4))
def b_apogeo(lz, t):
    iso = I.Iso(92.0, 92.0, 100.0, 1.55 + 0.03 * (t - T_B))
    ciclo = 0.5 + 0.5 * math.sin((t - T_B) * 1.7)
    I.luz(mul=(1.0 - 0.28 * ciclo, 1.0 - 0.22 * ciclo, 1.0 - 0.05 * ciclo), mix=(60, 40, 130), k=0.35 * ciclo)
    fondo_iso(lz, t, 0.0)
    CV.suelo(lz, iso, t)
    CV.objetos(t).dibujar(lz, iso)
    vida(lz, t)
    I.luz()
    # línea del tiempo 600-1300 con el tramo 700-1200 iluminado
    xa, xb, yb = 280, 1640, 930
    lz.relleno(rect_red(xa, yb - 5, xb - xa, 10, 5), (255, 255, 255), alfa=0.5, capa=2)
    for yr in range(600, 1301, 100):
        xx = lerp(xa, xb, (yr - 600) / 700)
        lz.relleno(rect_red(xx - 2, yb - 16, 4, 32, 2), (255, 255, 255), alfa=0.7, capa=2)
        P.rotulo(lz, xx, yb + 44, str(yr), px=30, alfa=0.85)
    f = e_inout(prog(t, t_setec - 0.3, t_docs + 0.9))
    if f > 0.001:
        x0 = lerp(xa, xb, 100 / 700)
        x1 = x0 + (lerp(xa, xb, 600 / 700) - x0) * f
        lz.relleno(rect_red(x0, yb - 14, x1 - x0, 28, 14), (255, 190, 60), capa=2)
        lz.halo((x0 + x1) / 2, yb, (x1 - x0) / 2 + 60, (255, 200, 90), alfa=0.35, capa=2)
    k = U.pop(t, t_arq) * U.salida(t, t_setec - 0.1, 0.25)
    if k > 0.01:
        U.llamada(lz, W / 2, 140, "los arqueólogos calculan…", color=U.COL["morado"], px=56, k=k, cola=None)
    k = U.pop(t, t_setec) * U.salida(t, T_C - 0.1, 0.25)
    if k > 0.01:
        U.llamada(lz, W / 2, 140, "su mejor momento", color=U.COL["naranja"], px=60, k=k, cola=None)
        lz.texto("700", lerp(xa, xb, 100 / 700), yb - 110, 100, "geo_x", color=(255, 255, 255), borde=None, k=k, alfa=1.0, capa=2, temblor=0.0)
    k = U.pop(t, t_mil) * U.salida(t, T_C - 0.1, 0.25)
    if k > 0.01:
        lz.texto("1200", lerp(xa, xb, 600 / 700), yb - 110, 100, "geo_x", color=(255, 255, 255), borde=None, k=k, alfa=1.0, capa=2, temblor=0.0)
        U.llamada(lz, W / 2 + 330, 250, "d. C.", color=U.COL["azul"], px=44, k=k, cola=None)


# ------------------------------------------------------------------------------------------------ C. visita guiada
def cam_c(t):
    return K(t, [(T_C, (50, 60, 150, 2.4)), (t_terrazas - 0.5, (60, 70, 150, 2.4)), (t_terrazas + 0.3, (150, 110, 100, 1.8)), (t_pir - 0.4, (200, 130, 70, 1.8)), (t_pir + 0.4, (378, 60, 70, 2.5)),
                     (t_juego - 0.4, (370, 70, 60, 2.5)), (t_juego + 0.3, (170, 335, 40, 2.3)), (t_25 - 0.5, (170, 335, 40, 2.3)), (t_25 + 0.4, (90, 262, 80, 2.8)), (T_D, (90, 262, 80, 2.8))])


@shot(T_C, bg=lambda t: PA.cielo(0.0), post=[acabado], ent=("tinta", 0.6))
def c_visita(lz, t):
    cx, cy, cz, zm = cam_c(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz(mul=(1.03, 1.0, 0.95), mix=(255, 170, 110), k=0.05)
    fondo_iso(lz, t, cx * 0.4)
    CV.suelo(lz, iso, t)
    n_m = int(np.clip((t - t_25) / 0.045, 0, 25)) if t < t_mono + 1.6 else 25
    CV.objetos(t, 1.0, n_m if t < t_mono + 1.3 else 25).dibujar(lz, iso)
    vida(lz, t)
    def rot(t0, t1, texto, col, p, dy=-60, px=52):
        k = U.pop(t, t0) * U.salida(t, t1, 0.25)
        if k > 0.01:
            sx, sy = iso.P(*p)
            U.llamada(lz, float(sx), float(sy) + dy, texto, color=col, px=px, k=k, cola="abajo")
    rot(t_arriba + 0.4, t_terrazas - 0.2, "ciudadela fortificada", U.COL["morado"], (55, 40, 190), -70)
    rot(t_terrazas, t_pir - 0.3, "terrazas con casas", U.COL["naranja"], (150, 120, 90), -80)
    rot(t_pir, t_juego - 0.25, "pirámide monumental", U.COL["magenta"], (376, 60, 100), -70)
    rot(t_juego, t_25 - 0.2, "juego de pelota", U.COL["teal"], (170, 338, 60), -100)
    k = U.pop(t, t_25) * U.salida(t, T_D - 0.1, 0.25)
    if k > 0.01:
        sx, sy = iso.P(90, 262, 150)
        lz.texto(str(n_m), float(sx), float(sy) - 20, 150, "geo_x", color=(255, 255, 255), borde=None, k=k, alfa=1.0, capa=2, temblor=0.0)
        U.llamada(lz, float(sx), float(sy) + 90, "monolitos circulares", color=U.COL["oro"], px=48, k=k, cola="arriba", color_texto=(60, 36, 20))
    for i in range(0, 25, 2):
        snd(t_25 + 0.045 * i, "pop", 0.2)


# ------------------------------------------------------------------------------------------------ D. 116 hectáreas
@shot(T_D, bg=lambda t: bg_grad((64, 28, 120), (20, 8, 52), mid=(44, 18, 96), ym=0.55), post=[acabado], ent=("tinta", 0.6))
def d_hectareas(lz, t):
    U.bokeh(lz, t, seed=11, n=12, colores=((255, 150, 44), (236, 70, 140), (122, 90, 255)), alfa=0.35)
    cols, filas = 14, 9
    n_tot = 116
    paso = 78
    x0, y0 = W / 2 - cols * paso / 2 + 400, 150
    f = prog(t, t_ciento, t_hect + 0.7)
    n_vis = int(f * n_tot)
    for i in range(n_tot):
        r, c = divmod(i, cols)
        ti = i / n_tot
        k = pk(t, t_ciento + ti * (t_hect + 0.6 - t_ciento), 0.25)
        if k <= 0.01:
            continue
        xx, yy = x0 + c * paso, y0 + r * paso
        col = P.mezcla((255, 190, 60), (236, 80, 120), (c / cols) * 0.5 + (r / filas) * 0.5)
        lz.relleno(rect_red(xx - 30 * k + 4, yy - 30 * k + 5, 60 * k, 60 * k, 10), P.oscurecer(col, 0.35), alfa=0.55, capa=1)
        lz.relleno(rect_red(xx - 30 * k, yy - 30 * k, 60 * k, 60 * k, 10), col, capa=1)
    kc = U.pop(t, t_ciento) * U.salida(t, T_E - 0.1, 0.25)
    if kc > 0.01:
        lz.texto(str(n_vis), 400, 390, 230, "geo_x", color=(255, 255, 255), borde=None, k=kc, alfa=1.0, capa=2, temblor=0.0)
        U.llamada(lz, 400, 530, "hectáreas", color=U.COL["naranja"], px=64, k=kc, cola=None)
        U.llamada(lz, 400, 630, "1 ha = 100 m × 100 m", color=U.COL["azul"], px=36, k=pk(t, t_hect, 0.4), cola=None)
    k = U.pop(t, t_desarr) * U.salida(t, T_E - 0.1, 0.25)
    if k > 0.01:
        U.llamada(lz, 360, 790, "el desarrollo cultural más grande", color=U.COL["magenta"], px=38, k=k, cola=None)
    k2 = U.pop(t, t_conoce) * U.salida(t, T_E - 0.1, 0.25)
    if k2 > 0.01:
        U.llamada(lz, 360, 860, "que se conoce en el cañón", color=U.COL["morado"], px=38, k=k2, cola=None)
    snd(t_hect, "bling", 0.4)


# ------------------------------------------------------------------------------------------------ E. la excavación
@shot(T_E, bg=lambda t: bg_grad((255, 214, 150), (255, 240, 200), mid=(250, 170, 150), ym=0.5), post=[acabado], ent=("tinta", 0.6))
def e_excava(lz, t):
    PA.sol(lz, 1500, 220, 70, t, 0.0)
    PA.sierras(lz, t, 0.0, 0.0, y0=520, capas=3, semilla=23)
    AREA = (380, 500, 1540, 1000)
    MD2.props_excavacion(lz, t, AREA)
    f = MD2.excavacion(lz, t, t_excav - 0.3, t_piedra + 1.0, area=AREA)
    # arqueólogos: uno cava a la izquierda y otro observa a la derecha
    MD2.arqueologo(lz, 250, 1010, 46, t, ph=t * 6.0, seed=1)
    K2.cuerpo(lz, 1700, 1020, 44, dict(piel="trigueña", pelo=(70, 50, 40), peinado="corto", cejas_g=1.2, torso="levita", ropa=(210, 200, 176), ropa2=(120, 88, 60), tocado="sombrero_ala", bigote=True), t,
              piernas="idle", brazos="señala", mirar=-1, vista="perfil", objetivo=(1330, 800), seed=4, cara="minima")
    k = U.pop(t, t_prim) * U.salida(t, t_finales - 0.1, 0.25)
    if k > 0.01:
        U.llamada(lz, 700, 250, "primeros estudios", color=U.COL["morado"], px=50, k=k, cola=None)
    k = U.pop(t, t_extr) * U.salida(t, t_finales - 0.1, 0.25)
    if k > 0.01:
        U.llamada(lz, 700, 330, "investigadores extranjeros", color=U.COL["azul"], px=46, k=k, cola=None)
    k = U.pop(t, t_finales) * U.salida(t, t_desde - 0.1, 0.25)
    if k > 0.01:
        U.llamada(lz, 1300, 280, "fines del siglo XIX", color=U.COL["naranja"], px=60, k=k, cola=None)
    k = U.pop(t, t_desde) * U.salida(t, T_F - 0.15, 0.25)
    if k > 0.01:
        U.llamada(lz, 1100, 300, "cada excavación revela más", color=U.COL["magenta"], px=54, k=k, cola=None)
    k = U.pop(t, t_piedra) * U.salida(t, T_F - 0.15, 0.25)
    if k > 0.01:
        U.llamada(lz, 1100, 380, "piedra tallada", color=U.COL["teal"], px=60, k=k * U.repop(t, t_piedra + 0.6), cola=None)
    for tt in (t_excav, t_excav + 0.5, t_revela, t_piedra):
        snd(tt, "crujido", 0.35)


# ------------------------------------------------------------------------------------------------ F. un muro con huecos
def esc_f(t):
    return K(t, [(T_F, 1.55), (t_lejos - 0.2, 1.5), (t_lejos + 1.4, 0.55), (T_G, 0.52)])


@shot(T_F, bg=lambda t: PA.cielo(0.0), post=[acabado], ent=("tinta", 0.6))
def f_muro(lz, t):
    s = float(esc_f(t))
    PA.sol(lz, 1560, 240, 70, t, 0.0)
    PA.sierras(lz, t, 0.0, 0.0, y0=500, capas=3, semilla=29)
    PA.aves(lz, t, n=5, seed=8)
    MD2.risco(lz, t, k=s, cx=960, cy=lerp(760, 640, smooth(prog(s, 1.5, 0.55))), brillo=0.9)
    k = U.pop(t, t_nombre) * U.salida(t, t_muro - 0.1, 0.25)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "el nombre viene de…", color=U.COL["morado"], px=56, k=k, cola=None)
    k = U.pop(t, t_muro) * U.salida(t, t_lejos - 0.1, 0.25)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "un muro de piedra con huecos", color=U.COL["naranja"], px=56, k=k, cola=None)
    k = U.pop(t, t_risco) * U.salida(t, t_lejos - 0.1, 0.25)
    if k > 0.01:
        U.llamada(lz, W / 2, 210, "sobre el risco más alto", color=U.COL["magenta"], px=50, k=k, cola=None)
    k = U.pop(t, t_lejos) * U.salida(t, t_parecen - 0.1, 0.25)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "desde lejos…", color=U.COL["azul"], px=60, k=k, cola=None)
    k = U.pop(t, t_parecen)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "parecen ventanas abiertas en la montaña", color=U.COL["oro"], px=54, k=k * U.repop(t, t_vent2 + 0.2), cola=None, color_texto=(60, 36, 20))
    snd(t_huecos, "pop", 0.4)


# ------------------------------------------------------------------------------------------------ G. el portón se abre en 2019
@shot(T_G, bg=lambda t: bg_grad((120, 80, 170), (255, 214, 150), mid=(240, 140, 150), ym=0.62), post=[acabado], ent=("tinta", 0.6))
def g_porton(lz, t):
    PA.sierras(lz, t, 0.0, 0.0, y0=560, capas=3, semilla=31)
    PA.sol(lz, 1560, 240, 66, t, 0.0)
    abre = e_inout(prog(t, t_ago + 0.2, t_2019 + 0.2))
    MD2.porton(lz, t, abre, cx=960, cy=900, s=1.0)
    lz.relleno(rect_red(0, 890, W, 200, 0), (150, 190, 112), capa=0)
    MD2.entorno_porton(lz, t)
    PA.flores_frente(lz, t, 0.0, n=18, amb=0.0, y0=960, seed=9, escala=0.8)
    # visitantes que entran cuando se abre
    if abre > 0.25:
        for i, (tipo, x0, v) in enumerate((("mujer", 330, 1.0), ("hombre", 120, 0.95), ("nino", 520, 0.9), ("senora", -40, 0.85), ("mujer", -220, 1.05))):
            x = x0 + (abre - 0.25) * 0 + max(0.0, t - (t_ago + 0.7)) * v * 135
            K2.cuerpo(lz, x, 985 + 8 * (i % 3), 40 if tipo != "nino" else 30, tipo, t, piernas="camina", brazos="balanceo", mirar=1, vista="perfil", seed=i + 5, cara="minima")
    # cartel y tiempo
    cer = U.pop(t, t_siglos) * U.salida(t, t_zona - 0.1, 0.25)
    if cer > 0.01:
        U.llamada(lz, 960, 200, "durante siglos…", color=U.COL["morado"], px=62, k=cer, cola=None)
    k = U.pop(t, t_nadie) * U.salida(t, t_zona - 0.1, 0.25)
    if k > 0.01:
        U.llamada(lz, 960, 290, "casi nadie pudo visitarlo", color=U.COL["rojo"], px=56, k=k, cola=None)
    k = U.pop(t, t_zona) * U.salida(t, t_dos - 0.1, 0.25)
    if k > 0.01:
        U.llamada(lz, 960, 200, "zona arqueológica", color=U.COL["naranja"], px=62, k=k, cola=None)
    k = U.pop(t, t_abrio) * U.salida(t, t_dos - 0.1, 0.25)
    if k > 0.01:
        U.llamada(lz, 960, 290, "se abrió al público", color=U.COL["teal"], px=56, k=k, cola=None)
    kc = pk(t, t_dos - 0.1, 0.5)
    if kc > 0.01:
        MD2.calendario(lz, 1560, 420, 0.7 * kc, t, dia="2", mes="AGOSTO", anio="2019", alfa=min(1.0, kc * 1.5))
    snd(t_dos, "bling", 0.5)
    snd(t_ago + 0.3, "crujido", 0.5)
