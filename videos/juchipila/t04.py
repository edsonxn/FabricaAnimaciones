# -*- coding: utf-8 -*-
"""Escena 4 · los caxcanes (1:55-2:33): quiénes eran (náhuatl), de dónde llegaron (siglos XII-XIII) y su señorío, su cultura (fortalezas, juego de pelota, fiesta de Xochipilli),
el solsticio que trae lluvia y verde, el nombre del pueblo y la fiesta que sobrevive (2015, patrimonio cultural)."""
import math

import numpy as np

import kz_ui as U
import kz_mapa as KM
import kz_mapa_dib as MD
import kz_abstracto as AB
import kz_pers2d as K2
import plano as P
import lugares  # noqa: F401
import paisajes as PA
import mapas as MA_
import mundos_a as MA
import mundos_e as ME
from motor import W, H, prog, lerp, smooth, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, h01, catmull
from reg import shot, snd
from util import *  # noqa: F401,F403
from t01 import acabado, BG_VIOLETA

E4 = "caxcanes"
MP = KM.MAPA
t_ult, t_caxc, t_pueblo, t_habl, t_nah = T(E4, "ultimos", frase=0), T(E4, "caxcanes", frase=0), T(E4, "pueblo", frase=0), T(E4, "hablaba", frase=0), T(E4, "nahuatl", frase=0)
t_lleg, t_norte, t_sig, t_doce, t_trece, t_form, t_sen, t_capital, t_ciudad, t_mont = (T(E4, "llegaron", frase=1), T(E4, "norte", frase=1), T(E4, "siglos", frase=1), T(E4, "doce", frase=1), T(E4, "trece", frase=1), T(E4, "formaron", frase=1),
                                                                                   T(E4, "senorio", frase=1), T(E4, "capital", frase=1), T(E4, "ciudad", frase=1), T(E4, "montana", frase=1))
t_fort, t_cerros, t_juegos, t_pel, t_fiesta, t_xoch, t_dios, t_flores, t_musica, t_danza = (T(E4, "fortalezas", frase=2), T(E4, "cerros", frase=2), T(E4, "juegos", frase=2), T(E4, "pelota", frase=2), T(E4, "fiesta", frase=2),
                                                                                         T(E4, "xochipilli", frase=2), T(E4, "dios", frase=2), T(E4, "flores", frase=2), T(E4, "musica", frase=2), T(E4, "danza", frase=2))
t_solst, t_verano, t_emp, t_lluv, t_canon, t_llena, t_verde = (T(E4, "solsticio", frase=3), T(E4, "verano", frase=3), T(E4, "empiezan", frase=3), T(E4, "lluvias", frase=3), T(E4, "canon", frase=3), T(E4, "llena", frase=3), T(E4, "verde", frase=3))
t_ahi, t_nombre, t_lugar, t_flores2, t_nobles = T(E4, "ahi", frase=4), T(E4, "nombre", frase=4), T(E4, "lugar", frase=4), T(E4, "flores", frase=4), T(E4, "nobles", frase=4)
t_esa, t_perdio, t_junio, t_juch, t_celeb, t_quince, t_patr, t_cult, t_zac = (T(E4, "esa", frase=5), T(E4, "perdio", frase=5), T(E4, "junio", frase=5), T(E4, "juchipila", frase=5), T(E4, "celebrando", frase=5),
                                                                              T(E4, "quince", frase=5), T(E4, "patrimonio", frase=5), T(E4, "cultural", frase=5), T(E4, "zacatecas", frase=5))
T_A, T_B, T_C, T_D, T_E, T_F = T0(E4), INI(E4, 1) - 0.1, INI(E4, 2) - 0.1, INI(E4, 3) - 0.1, INI(E4, 4) - 0.1, INI(E4, 5) - 0.1
TERRITORIO = [(-103.40, 21.98), (-103.05, 22.00), (-102.84, 21.62), (-102.98, 21.18), (-103.30, 21.12), (-103.50, 21.55)]


# ------------------------------------------------------------------------------------------------ A. los últimos en habitar la ciudad
@shot(T_A, bg=lambda t: bg_grad((70, 28, 130), (18, 8, 46), mid=(44, 18, 96), ym=0.55), post=[acabado], ent=("tinta", 0.5))
def a_caxcanes(lz, t):
    U.bokeh(lz, t, seed=14, n=14, colores=((255, 150, 44), (236, 70, 140), (122, 90, 255), (255, 214, 90)), alfa=0.40)
    U.chispas(lz, t, n=12, seed=5)
    PA.sierras(lz, t, 0.0, 1.0, y0=830, capas=3, semilla=41)
    kb = pk(t, t_ult, 0.5)
    K2.busto(lz, 520, 1110, 215 * kb, "caxcan", t, yaw=0.55, emocion="serio", ojos="abiertos", seed=2)
    kb2 = pk(t, t_ult + 0.25, 0.5)
    K2.busto(lz, 1400, 1110, 215 * kb2, "caxcana", t, yaw=-0.55, emocion="neutro", ojos="abiertos", seed=7, habla=0.7 if t_habl - 0.2 < t < t_nah + 0.9 else 0.0)
    k = U.pop(t, t_ult) * U.salida(t, t_caxc - 0.1, 0.25)
    if k > 0.01:
        U.llamada(lz, W / 2, 150, "los últimos en habitar la ciudad", color=U.COL["morado"], px=60, k=k, cola=None)
    k = U.pop(t, t_caxc)
    if k > 0.01:
        U.llamada(lz, W / 2, 150, "los caxcanes", color=U.COL["naranja"], px=76, k=k * U.repop(t, t_caxc + 0.8), cola=None)
    k = U.pop(t, t_nah)
    if k > 0.01:
        U.globo(lz, 1230, 520, "Nāhuatl", px=64, k=k, cola="abajo", lado=1, color_texto=U.COL["morado"])
    snd(t_caxc, "pop", 0.4)


# ------------------------------------------------------------------------------------------------ B. llegaron desde el norte; el señorío
def cam_b(t):
    return Klog(t, [(T_B, (-102.95, 22.25, 1.9)), (t_form, (-103.05, 21.95, 2.4)), (T_C, (-103.12, 21.62, 2.9))])


@shot(T_B, bg=lambda t: MP.base(cam_b(t), t, exag=12.0, rios_umbral=0.7), post=[acabado], ent=("tinta", 0.6))
def b_llegada(lz, t):
    cam = cam_b(t)
    MD.montes(lz, cam)
    MD.region(lz, cam, "SIERRA MADRE OCCIDENTAL", (-104.3, 22.6), px=24, rot=-1.1, alfa=0.55, z_max=2.6)
    # el señorío: territorio que se llena de color
    kt = U.pop(t, t_form + 0.1)
    if kt > 0.01:
        q = np.array([MA_.proy(cam, c) for c in TERRITORIO])
        cen = q.mean(0)
        q2 = cen + (q - cen) * float(min(1.0, kt))
        lz.relleno(np.array(catmull(q2, 8, True)), (255, 150, 44), alfa=0.30, capa=2)
        lz.trazo(np.array(catmull(q2, 8, True)), (255, 150, 44, 230), 8.0, cerrado=True, afinar=False, temblor=0.0, capa=2)
    f = prog(t, t_lleg, t_norte + 1.4)
    MA_.ruta_gruesa(lz, cam, ["la_quemada", (-103.0, 22.0), "juchipila"], frac=e_inout(f), t=t, color=(240, 130, 36), ancho=13, dash=True)
    if t_lleg + 0.3 < t < T_C:
        ptsm = [MA_.proy(cam, c) for c in ("la_quemada", (-103.0, 22.0), "juchipila")]
        AB.corriente(lz, t, ptsm, n=26, ancho=16.0, vel=0.18, color=((255, 130, 90), (255, 206, 90), (236, 70, 140)), r=(5.0, 8.0), seed=11, capa=2, alfa=min(1.0, (t - t_lleg - 0.3) * 2), estela=1.0)
    MD.ciudad(lz, cam, "la_quemada", t, t_lleg, tam=0.9, tipo="fuerte", nombre="La Quemada", px=26, semilla=5)
    MD.ciudad(lz, cam, "las_ventanas", t, t_capital - 0.1, tam=1.2, tipo="fuerte", semilla=2)
    MD.ciudad(lz, cam, "juchipila", t, t_lleg + 0.2, tam=0.9, tipo="pueblo", semilla=3)
    k = U.pop(t, t_norte) * U.salida(t, t_sig - 0.15, 0.25)
    if k > 0.01:
        U.llamada(lz, W / 2, 140, "desde el norte", color=U.COL["naranja"], px=64, k=k, cola=None)
    k = U.pop(t, t_sig) * U.salida(t, t_form - 0.1, 0.25)
    if k > 0.01:
        lz.texto("siglos XII y XIII", W / 2, 150, 96, "geo_x", color=(255, 255, 255), borde=None, k=k, alfa=1.0, capa=2, temblor=0.0)
        U.llamada(lz, W / 2, 250, "años 1100 a 1300", color=U.COL["azul"], px=42, k=pk(t, t_doce, 0.4), cola=None)
    k = U.pop(t, t_sen)
    if k > 0.01:
        p = MA_.proy(cam, (-103.1, 21.86))
        U.llamada(lz, p[0], p[1], "señorío", color=U.COL["naranja"], px=70, k=k * U.repop(t, t_sen + 0.7), cola=None)
    k = U.pop(t, t_capital) * U.salida(t, T_C - 0.1, 0.25)
    if k > 0.01:
        p = MA_.proy(cam, "las_ventanas")
        U.llamada(lz, p[0] + 150, p[1] - 60, "capital", color=U.COL["magenta"], px=54, k=k, cola=None)
    MD.escala(lz, 80, H - 70, cam, km=100)
    snd(t_lleg, "whoosh", 0.4)


# ------------------------------------------------------------------------------------------------ C. su cultura: fortalezas, juego de pelota, fiesta y Xochipilli
@shot(T_C, bg=lambda t: bg_grad((255, 200, 132), (255, 236, 190), mid=(246, 150, 150), ym=0.58), post=[acabado], ent=("tinta", 0.6))
def c_cultura(lz, t):
    PA.sol(lz, 1640, 200, 64, t, 0.0)
    PA.sierras(lz, t, 0.0, 0.0, y0=640, capas=4, semilla=47)
    oc = 1 - smooth(prog(t, t_xoch - 0.2, t_xoch + 0.5))
    xs = (400, 960, 1520)
    for i, (t0, fn) in enumerate(((t_fort, ME.fortaleza), (t_juegos, ME.cancha_pelota), (t_fiesta, None))):
        k = pk(t, t0 - 0.12, 0.4) * oc
        if k <= 0.01:
            continue
        ME.tarjeta(lz, xs[i], 520, 480, 580, k=k, color=(255, 246, 232), borde=(122, 52, 200))
        with lz.grupo(xs[i], 520, k):
            if fn is ME.fortaleza:
                ME.fortaleza(lz, 0, 60, 0.9, t)
            elif fn is ME.cancha_pelota:
                ME.cancha_pelota(lz, 0, 40, 0.86, t)
            else:
                MA.flor_xuchitl(lz, 0, 20, 150, t, u=1.0, sombra=False, seed=3)
        rot = ("fortalezas en los cerros", "juegos de pelota", "una fiesta al año")[i]
        U.llamada(lz, xs[i], 880, rot, color=(U.COL["morado"], U.COL["teal"], U.COL["naranja"])[i], px=40, k=k, cola=None)
    # Xochipilli
    kx = pk(t, t_xoch - 0.1, 0.6)
    if kx > 0.01:
        lz.halo(960, 760, 520 * kx, (255, 214, 110), alfa=0.40, capa=1)
        for q in range(14):
            a = q * 2 * math.pi / 14 + t * 0.2
            MA.flor_xuchitl(lz, 960 + 640 * math.cos(a) * kx, 640 + 380 * math.sin(a) * kx, 30 * kx, t, u=1.0, sombra=False, seed=q)
        K2.busto(lz, 960, 1130, 165 * kx, "xochipilli", t, yaw=-0.3, emocion="serio", ojos="abiertos", seed=4)
        U.llamada(lz, 960, 120, "Xochipilli", color=U.COL["naranja"], px=80, k=kx * U.repop(t, t_xoch + 0.6), cola=None)
    # lo que preside: flores, música, danza
    for t0, x, fn, txt, col in ((t_flores, 300, "flor", "las flores", U.COL["naranja"]), (t_musica, 1620, "nota", "la música", U.COL["azul"]), (t_danza, 300, "baile", "la danza", U.COL["magenta"])):
        k = pk(t, t0 - 0.05, 0.45)
        if k <= 0.01:
            continue
        y = 330 if fn != "baile" else 700
        if fn == "nota" and x > 1000:
            y = 330
        lz.relleno(circulo(x, y, 130 * k, 40), (255, 255, 255), alfa=0.85, capa=2)
        with lz.grupo(x, y, k):
            if fn == "flor":
                MA.flor_xuchitl(lz, 0, 0, 90, t, u=1.0, sombra=False, seed=2)
            elif fn == "nota":
                ME.notas_musicales(lz, 0, 60, 0.9, t)
            else:
                K2.cuerpo(lz, 0, 90, 20, "danzante", t, piernas="baila", brazos="baila", mirar=1, vista="frente", seed=5, cara="minima", sombra=False)
        U.llamada(lz, x, y + 175, txt, color=col, px=44, k=k, cola=None)
    for tt in (t_fort, t_juegos, t_fiesta, t_xoch, t_flores, t_musica, t_danza):
        snd(tt, "pop", 0.35)


# ------------------------------------------------------------------------------------------------ D. solsticio, lluvia y verde
def verde_t(t):
    return float(smooth(prog(t, t_canon + 0.1, t_llena + 0.9)))


def lluvia_t(t):
    return float(smooth(prog(t, t_emp - 0.1, t_lluv + 0.7)) * (1 - 0.5 * smooth(prog(t, t_verde, t_verde + 1.0))))


@shot(T_D, bg=lambda t: PA.cielo(round(0.30 * lluvia_t(t), 1)), post=[acabado], ent=("tinta", 0.6))
def d_solsticio(lz, t):
    v, ll = verde_t(t), lluvia_t(t)
    u = prog(t, T_D, t_verano + 0.8)
    amb = 0.30 * ll
    if t < t_emp:
        sx, sy = ME.arco_solar(lz, t, 0.15 + 0.35 * u, cx=960, cy=830, rx=760, ry=640)
    PA.sierras(lz, t, 30 * (t - T_D), amb, y0=660, verde=v)
    PA.rio(lz, t, amb, y_h=660)
    PA.aldea(lz, t, amb, x0=560, x1=1380, y=740, n=6, rio_h=660)
    PA.pared_canon(lz, t, -1, amb, ancho=360, seed=2, verde=v)
    PA.pared_canon(lz, t, 1, amb, ancho=360, seed=5, verde=v)
    PA.flores_frente(lz, t, 0.0, n=int(8 + 22 * v), amb=amb)
    # nubes y lluvia
    for i, (x, y, s) in enumerate(((420, 210, 1.0), (940, 150, 1.3), (1480, 230, 1.0))):
        nk = ll
        if nk > 0.02:
            ME.nube(lz, x + 20 * math.sin(t * 0.3 + i), y, s * nk, color=P.mezcla((236, 232, 248), (120, 110, 160), 0.4), alfa=nk)
    if ll > 0.05:
        ME.lluvia(lz, t, a=ll, y0=260, y1=900, n=150)
    k = U.pop(t, t_solst) * U.salida(t, t_emp - 0.1, 0.25)
    if k > 0.01:
        U.llamada(lz, W / 2, 150, "solsticio de verano", color=U.COL["naranja"], px=70, k=k, cola=None)
    k = U.pop(t, t_verano) * U.salida(t, t_emp - 0.1, 0.25)
    if k > 0.01:
        U.llamada(lz, W / 2, 268, "junio", color=U.COL["rojo"], px=54, k=k, cola=None)
    k = U.pop(t, t_emp) * U.salida(t, t_llena - 0.1, 0.25)
    if k > 0.01:
        U.llamada(lz, W / 2, 150, "empiezan las lluvias", color=U.COL["azul"], px=66, k=k, cola=None)
    k = U.pop(t, t_llena)
    if k > 0.01:
        U.llamada(lz, W / 2, 150, "el cañón se llena de verde", color=U.COL["verde"], px=66, k=k * U.repop(t, t_verde + 0.3), cola=None)
    snd(t_lluv, "ola", 0.4)


# ------------------------------------------------------------------------------------------------ E. el nombre del pueblo
@shot(T_E, bg=BG_VIOLETA, post=[acabado], ent=("tinta", 0.5))
def e_nombre(lz, t):
    U.bokeh(lz, t, seed=4, n=16, colores=((255, 150, 44), (236, 70, 140), (122, 90, 255), (255, 214, 90)), alfa=0.45)
    U.chispas(lz, t, n=14, seed=2)
    k = pk(t, t_ahi, 0.7)
    MA.flor_xuchitl(lz, 470, 560, 240 * min(1.0, k), t, u=min(1.0, k), seed=1)
    AB.petalos(lz, t, t_ahi + 0.3, (470, 560), n=14, dur=2.2, seed=9)
    a = U.pop(t, t_nombre)
    AB.titulo_textura(lz, "XOCHIPILLAN", 1330, 430, 150, t, k=0.78, alfa=min(1.0, a * 1.5))
    k = U.pop(t, t_lugar)
    if k > 0.01:
        U.llamada(lz, 1330, 640, "lugar de las flores nobles", color=U.COL["morado"], px=62, k=k * U.repop(t, t_nobles + 0.2), cola=None)
    k = U.pop(t, t_flores2) * 1.0
    if k > 0.01:
        MD.corona(lz, 1330, 820, 3.0 * U.pop(t, t_nobles), 1.0, t)


# ------------------------------------------------------------------------------------------------ F. la fiesta de hoy
DANZ = [("danzante", 420, 820), ("danzante_h", 640, 880), ("danzante", 860, 830), ("danzante_h", 1080, 890), ("danzante", 1300, 830), ("danzante_h", 1520, 880), ("danzante", 1730, 820)]


@shot(T_F, bg=lambda t: bg_grad((90, 60, 160), (255, 190, 130), mid=(240, 120, 150), ym=0.55), post=[acabado], ent=("tinta", 0.6))
def f_fiesta(lz, t):
    PA.sierras(lz, t, 0.0, 0.0, y0=560, capas=3, semilla=53)
    ME.fachada_iglesia(lz, 960, 770, 1.05, capa=0)
    lz.relleno(rect_red(0, 760, W, 400, 0), (214, 170, 130), capa=0)
    lz.relleno(rect_red(0, 760, W, 28, 0), (186, 140, 110), capa=0)
    ME.papel_picado(lz, t, y=110)
    ME.papel_picado(lz, t, y=240, n=11)
    # flores en el suelo y bailarines
    for i in range(18):
        x = 80 + 105 * i + 20 * (h01(3, i, 1) - 0.5)
        y = 800 + 140 * h01(3, i, 2)
        MA.flor_xuchitl(lz, x, y, 20 + 8 * h01(3, i, 3), t, u=1.0, sombra=False, seed=i)
    for i, (tipo, x, y) in enumerate(DANZ):
        K2.cuerpo(lz, x, y + 160, 48, tipo, t + 0.13 * i, piernas="baila", brazos="baila", mirar=1 if i % 2 else -1, vista="frente", seed=i + 20, cara="minima")
    k = U.pop(t, t_esa) * U.salida(t, t_junio - 0.1, 0.25)
    if k > 0.01:
        U.llamada(lz, W / 2, 380, "esa fiesta no se perdió", color=U.COL["magenta"], px=66, k=k, cola=None)
    k = U.pop(t, t_junio) * U.salida(t, t_quince - 0.2, 0.25)
    if k > 0.01:
        U.llamada(lz, W / 2, 380, "cada junio: la Fiesta de Xúchitl", color=U.COL["naranja"], px=62, k=k, cola=None)
    k = U.pop(t, t_quince - 0.1)
    if k > 0.01:
        lz.relleno(rect_red(0, 0, W, H, 0), (20, 8, 50), alfa=0.35 * min(1.0, k), capa=2)
        lz.texto("2015", 560, 430, 230, "geo_x", color=(255, 255, 255), borde=None, k=k, alfa=1.0, capa=2, temblor=0.0)
        U.llamada(lz, 560, 600, "patrimonio cultural", color=U.COL["oro"], px=62, k=pk(t, t_patr, 0.4), cola=None, color_texto=(60, 36, 20))
        ME.sello(lz, 1330, 470, 190, "PATRIMONIO", t, k=pk(t, t_patr - 0.1, 0.6))
        U.llamada(lz, 1330, 800, "de Zacatecas", color=U.COL["morado"], px=58, k=pk(t, t_zac, 0.4), cola=None)
    snd(t_junio, "pluck", 0.4)
    snd(t_quince, "bling", 0.5)
