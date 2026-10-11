# -*- coding: utf-8 -*-
"""Escena 13 · La guerrilla (7:24-8:06): la insurgencia se esconde en las montañas, Guerrero en la sierra del sur, Victoria solo en la selva, Mina desembarca y cae, el país agotado en 1820 y el costo de la guerra (pueblos quemados, caminos cortados, minas inundadas, campos sin cultivar)."""
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
import mundos_g as mg
import mundos_m as mm
import t12 as T12
import t07 as T07

E13 = "guerrillas"
MP = KM.MAPA
GRAD = lambda img, t: U.gradacion(img)
GRIS = T12.GRIS
BASE = lambda cam, t: MP.base(cam, t, exag=13.0, rios_umbral=0.7)
PURP = lambda t: bg_grad((54, 30, 112), (150, 70, 130), mid=(100, 46, 130), ym=0.5)
SIE = mm.SierraSur()
SEL = mm.Selva()

# ------------------------------------------------------------------ anclas
t_pero, t_term, t_escond, t_mont = [T(E13, w, frase=0) for w in ("pero", "termino", "escondio", "montanas")]
t_guer, t_arr, t_hum, t_mant, t_viva, t_guerra, t_sier, t_sur = [T(E13, w, frase=1) for w in ("guerrero", "arriero", "humilde", "mantuvo", "viva", "guerra", "sierras", "sur")]
t_vic, t_resis, t_anos, t_selva, t_verac, t_solo, t_com, t_enc = [T(E13, w, frase=2) for w in ("victoria", "resistio", "anos", "selva", "veracruz", "solo", "comiendo", "encontraba")]
t_1817, t_desem, t_joven, t_esp, t_mina, t_unirse, t_capt, t_fusi, t_mismo = [T(E13, w, frase=3) for w in ("diecisiete", "desembarco", "joven", "espanol", "mina", "unirse", "capturaron", "fusilaron", "mismo")]
t_1820, t_guerra2, t_diez, t_pais, t_agot, t_insu, t_acor, t_pocos, t_pens, t_ganar = [T(E13, w, frase=4) for w in ("veinte", "guerra", "diez", "pais", "agotado", "insurgentes", "acorralados", "pocos", "pensaban", "ganar")]
t_real, t_quem, t_pueb, t_cort, t_cam, t_minas, t_inund, t_camp, t_sin, t_cult = [T(E13, w, frase=5) for w in ("realistas", "quemaban", "pueblos", "cortaban", "caminos", "minas", "inundaban", "campos", "sin", "cultivar")]
T_A, T_B, T_C, T_D1, T_D2, T_E1, T_E2, T_F = T0(E13), t_guer - 0.2, t_vic - 0.2, t_1817 - 0.2, t_capt - 0.3, t_1820 - 0.15, t_agot - 0.15, t_real - 0.15


# ------------------------------------------------------------------------------------------------ 1. SE ESCONDE EN LAS MONTAÑAS (mapa)
LUCES_SIERRA = [(-99.5, 17.55), (-98.9, 17.75), (-100.2, 17.7), (-99.0, 17.1), (-98.3, 17.5), (-100.8, 18.0), (-97.8, 18.4)]


def cam_a(t):
    return Klog(t, [(T_A, (-99.6, 18.0, 1.4)), (T_B, (-99.3, 17.6, 2.4))])


@shot(T_A, bg=lambda t: BASE(cam_a(t), t), post=[lambda img, t: U.gradacion(img, luces=(0.98, 0.98, 1.0), sombras=(0.92, 0.94, 1.04), saturacion=0.7 + 0.3 * smooth(prog(t, t_escond, T_B)))], ent=("fundido", 0.6))
def gu_montanas(lz, t):
    cam = cam_a(t)
    I.luz(mul=(0.92, 0.94, 1.0), mix=(30, 34, 90), k=0.16 * (1 - smooth(prog(t, t_escond, T_B))))
    MD.montes(lz, cam, min_alt=1400)
    MD.pais(lz, cam, "Mexico", (255, 96, 70), alfa=0.06, borde=(255, 220, 90), ancho=4.0, t=t, latido=0.0)
    MD.region(lz, cam, "SIERRA MADRE DEL SUR", (-99.6, 17.2), px=40, alfa=0.7, z_max=3.0)
    for i, (lo, la) in enumerate(T12.FOCOS):
        sx, sy = MP.proy(cam, lo, la)
        lz.relleno(circulo(float(sx), float(sy), 12, 12), (60, 60, 80), alfa=0.7, capa=2)
    for i, (lo, la) in enumerate(LUCES_SIERRA):                     # se encienden de nuevo en la sierra
        ti = t_escond + 0.12 * i
        a = smooth(prog(t, ti, ti + 0.5))
        sx, sy = MP.proy(cam, lo, la)
        if a > 0.01:
            lz.halo(float(sx), float(sy), 220 * a, (140, 255, 170), alfa=0.6 * a, capa=2)
            lz.relleno(circulo(float(sx), float(sy), 20 * a, 14), (210, 255, 220), alfa=a, capa=2)
            MD.bandera_mapa(lz, float(sx), float(sy) - 20, (70, 190, 110), t + i, 1.1 * a)
            U.chispa4(lz, float(sx) + 30, float(sy) - 30, 14 * a, alfa=a)
    k = U.pop(t, t_pero - 0.05) * U.salida(t, t_escond - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "pero no se terminó…", color=U.COL["naranja"], px=90, k=k, cola=None)
    k = U.pop(t, t_escond - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "se escondió en las montañas", color=U.COL["verde"], px=80, k=k * U.repop(t, t_mont + 0.1), cola=None)
    MD.brujula(lz, W - 110, H - 120, 1.0)


# ------------------------------------------------------------------------------------------------ 2. GUERRERO EN LA SIERRA
def cam_b(t):
    return K(t, [(T_B, (120, 250, 30, 2.6)), (t_hum, (250, 150, 40, 2.9)), (t_mant, (300, 140, 44, 3.2)), (T_C, (330, 130, 44, 3.4))])


@shot(T_B, bg=lambda t: bg_grad((120, 180, 230), (252, 230, 196), mid=(190, 210, 238), ym=0.5), post=[GRAD], ent=("fundido", 0.5))
def gu_guerrero(lz, t):
    cx, cy, cz, zm = cam_b(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz(mul=(1.02, 1.0, 0.96), mix=(255, 214, 160), k=0.05)
    mg.cerros(lz, cx, cy, t, tonos=((88, 130, 112), (70, 112, 100), (56, 92, 90)), alturas=(320, 250, 190))
    SIE.suelo(lz, iso, t)
    m = SIE.objetos(t)
    # una recua de arrieros sube por la vereda; Guerrero (arriero) al frente; al decir «mantuvo viva la guerra» sus hombres salen de entre las rocas
    for i in range(7):
        x, y, d = mm.pos_vereda(40 + (t - T_B) * 24.0 - 26 * i)
        if i == 0:
            m.add(x - 8, y - 8, x + 8, y + 8, 50, (lambda x, y: (lambda lz, iso: G.caballo(lz, iso, x, y, t, dir=1, seed=3, vel=1.0, jinete="arriero", s=1.3)))(x, y), fijo=False, clave=x + y + 10)
        else:
            m.add(x - 6, y - 4, x + 6, y + 4, 20, (lambda x, y, i: (lambda lz, iso: G.burro(lz, iso, x, y, t, dir=1, seed=i, carga=True)))(x, y, i), fijo=False, clave=x + y + 3)
    sal = e_out(prog(t, t_mant - 0.1, t_viva + 0.8))
    ROC = ((150, 300), (230, 80), (330, 200), (420, 40), (60, 200), (500, 160), (300, 60))
    for i, (rx, ry) in enumerate(ROC):
        for j in range(3):
            x0, y0 = rx + 10 * (j - 1), ry + 14
            a_ = 2 * math.pi * (i * 3 + j) / 21
            x1, y1 = 320 + 90 * math.cos(a_), 150 + 60 * math.sin(a_)
            x, y = lerp(x0, x1, sal), lerp(y0, y1, sal)
            m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i, j, s_: (lambda lz, iso: G.persona(lz, iso, x, y, t, ("insurgente", "insurgente_lanza", "campesino", "indigena")[(i + j) % 4], dir=(1, 0.2), vel=1.7 if 0 < s_ < 1 else 0.0, seed=10400 + i * 3 + j, h=26 + 18 * s_, cara="enojo", accion="pelea" if s_ >= 1 and j == 0 else None)))(x, y, i, j, sal), fijo=False, clave=x + y + 4)
    m.dibujar(lz, iso)
    DC.aves(lz, t, n=7, seed=101, y0=60, y1=220)
    kg = U.pop(t, t_guer - 0.1, 1.2)
    if kg > 0.01:
        MD.medallon(lz, 1630, 440, 140, "guerrero", t, emocion="serio", k=kg * U.salida(t, T_C - 0.2, 0.25), seed=3)
        U.llamada(lz, 1630, 610, "Vicente Guerrero", color=U.COL["azul"], px=42, k=kg * U.salida(t, T_C - 0.2, 0.25), cola="arriba")
    k = U.pop(t, t_arr - 0.05) * U.salida(t, t_mant - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2 - 200, 130, "un arriero de origen humilde", color=U.COL["naranja"], px=70, k=k * U.repop(t, t_hum + 0.1), cola=None)
    k = U.pop(t, t_mant - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2 - 200, 130, "mantuvo viva la guerra en las sierras del sur", color=U.COL["rojo"], px=58, k=k * U.repop(t, t_sier + 0.1), cola=None)


# ------------------------------------------------------------------------------------------------ 3. VICTORIA SOLO EN LA SELVA
def cam_c(t):
    return K(t, [(T_C, (190, 170, 30, 2.6)), (t_selva, (190, 175, 30, 3.4)), (t_solo, (190, 175, 30, 3.8)), (T_D1, (190, 178, 30, 3.9))])


def _fruta(lz, x, y, tipo, s, a=1.0):
    if tipo == 0:                                              # plátano
        lz.relleno(np.array([[x - 24 * s, y], [x, y + 14 * s], [x + 24 * s, y - 6 * s], [x, y + 4 * s]]), (250, 214, 70), alfa=a, capa=2)
    elif tipo == 1:                                            # raíz
        lz.relleno(np.array([[x - 22 * s, y - 6 * s], [x + 20 * s, y - 2 * s], [x + 28 * s, y + 6 * s], [x - 20 * s, y + 8 * s]]), (176, 120, 80), alfa=a, capa=2)
    else:                                                      # pez
        lz.relleno(elipse(x, y, 24 * s, 11 * s, 0, 16), (130, 190, 230), alfa=a, capa=2)
        lz.relleno(np.array([[x + 20 * s, y], [x + 38 * s, y - 12 * s], [x + 38 * s, y + 12 * s]]), (110, 170, 214), alfa=a, capa=2)


@shot(T_C, bg=lambda t: bg_grad((90, 150, 150), (200, 232, 190), mid=(140, 190, 170), ym=0.5), post=[GRAD], ent=("fundido", 0.5))
def gu_selva(lz, t):
    cx, cy, cz, zm = cam_c(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz(mul=(0.94, 1.0, 0.96), mix=(60, 140, 100), k=0.10)
    SEL.suelo(lz, iso, t)
    m = SEL.objetos(t)
    m.add(190, 170, 206, 186, 40, lambda lz, iso: G.persona(lz, iso, 198, 178, t, "insurgente", dir=(0.3, 1), seed=10500, h=52, accion="trabaja" if t > t_com else None, cara="serio"), fijo=False, clave=370)
    m.add(214, 190, 226, 200, 20, lambda lz, iso: O.fuego(lz, iso, 220, 196, 1.0, t, seed=2, halo=True), fijo=False, clave=420)
    m.add(214, 186, 226, 198, 80, lambda lz, iso: O.humo(lz, iso, 220, 192, 20, t, n=5, s=1.0, seed=3), fijo=False, clave=421)
    m.dibujar(lz, iso)
    DC.mariposas(lz, iso, 100, 100, 300, 260, n=5, t=t)
    DC.aves(lz, t, n=6, seed=102, y0=60, y1=200, color=(40, 90, 70))
    DC.polvo_luz(lz, t, n=18, seed=103, color=(200, 255, 210), alfa=0.35)
    kv = U.pop(t, t_vic - 0.1) * U.salida(t, T_D1 - 0.25, 0.25)
    if kv > 0.01:
        MD.medallon(lz, 300, 440, 140, "victoria", t, emocion="serio", k=kv, seed=2)
        U.llamada(lz, 300, 610, "Guadalupe Victoria", color=U.COL["verde"], px=42, k=kv, cola="arriba")
    k = U.pop(t, t_resis - 0.05) * U.salida(t, t_selva - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "resistió durante años", color=U.COL["naranja"], px=80, k=k * U.repop(t, t_anos + 0.1), cola=None)
    k = U.pop(t, t_selva - 0.05) * U.salida(t, t_solo - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "en la selva de Veracruz", color=U.COL["verde"], px=76, k=k, cola=None)
    k = U.pop(t, t_solo - 0.05) * U.salida(t, t_com - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "casi solo", color=U.COL["rojo"], px=100, k=k * U.repop(t, t_solo + 0.2), cola=None)
    k = U.pop(t, t_com - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "comiendo lo que encontraba", color=U.COL["morado"], px=70, k=k * U.repop(t, t_enc + 0.1), cola=None)
        for j in range(3):
            u = prog(t, t_com + 0.35 * j, t_com + 0.35 * j + 1.4)
            if 0 < u < 1:
                qx, qy = iso.P(198, 178, 50)
                _fruta(lz, float(qx) + 140 * (j - 1) * u, float(qy) - 30 - 150 * u, j, 1.6, 1.0 - u * 0.6)


# ------------------------------------------------------------------------------------------------ 4. MINA DESEMBARCA (mapa) Y CAE
RUTA_M = [(-97.77, 23.77), (-99.0, 22.5), (-100.5, 21.6), (-101.7, 21.2)]


def cam_d1(t):
    return Klog(t, [(T_D1, (-99.8, 22.6, 1.7)), (t_unirse, (-99.9, 22.4, 2.0)), (T_D2, (-100.0, 22.4, 2.0))])


@shot(T_D1, bg=lambda t: BASE(cam_d1(t), t), post=[GRAD], ent=("zoom", 0.5))
def gu_mina(lz, t):
    cam = cam_d1(t)
    I.luz()
    MD.montes(lz, cam, min_alt=2200)
    MD.mar_vivo(lz, cam, t, seed=17)
    MD.pais(lz, cam, "Mexico", (255, 96, 70), alfa=0.08, borde=(255, 220, 90), ancho=4.0, t=t, latido=0.0)
    MD.ciudad(lz, cam, "soto_marina", t, T_D1 + 0.1, tam=1.5, tipo="puerto", bando="ins", nombre="Soto la Marina", px=24, semilla=3)
    MD.ciudad(lz, cam, (-101.7, 21.2), t, T_D1 + 0.2, tam=1.5, tipo="fuerte", bando="ins", nombre="Fuerte del Sombrero", px=24, semilla=5)
    # el barco llega por el golfo y la tropa avanza hacia el interior
    f = e_inout(prog(t, t_desem - 0.2, t_unirse + 0.6))
    sx, sy = MP.proy(cam, -97.77, 23.77)
    bx = float(sx) + 520 * (1 - e_out(prog(t, T_D1, t_desem + 0.2)))
    MD.barco_plano(lz, bx, float(sy) - 20, 1.6, t, dir=-1)
    if t > t_desem:
        MD.ruta(lz, cam, RUTA_M, color=(255, 214, 84), frac=f, t=t, ancho=8.0, flecha=True)
        for i in range(4):
            u = max(0.0, min(0.999, f - 0.07 * i))
            if u > 0.01:
                x, y, v = MD.punto_ruta(cam, RUTA_M, u)
                MD.ejercito(lz, float(x), float(y), 6, bando="ins", t=t + i * 0.2, s=1.6, dir=-1, semilla=i, bandera=(i == 0), polvo=(i % 2 == 0))
    k = U.pop(t, t_1817 - 0.05)
    if k > 0.01:
        U._registrar(lz, 300, 200, 440, 190)
        P.rotulo(lz, 300, 200, "1817", px=int(200 * (0.9 + 0.1 * k)), k=k * U.salida(t, T_D2 - 0.2, 0.25), color=(255, 214, 72))
    km = U.pop(t, t_mina - 0.1) * U.salida(t, T_D2 - 0.2, 0.25)
    if km > 0.01:
        MD.medallon(lz, 1620, 450, 150, "mina", t, emocion="serio", k=km, seed=4)
        U.llamada(lz, 1620, 630, "Francisco Xavier Mina", color=U.COL["azul"], px=40, k=km, cola="arriba")
    k = U.pop(t, t_desem - 0.05) * U.salida(t, t_unirse - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "desembarca un joven español", color=U.COL["naranja"], px=72, k=k * U.repop(t, t_joven + 0.1), cola=None)
    k = U.pop(t, t_unirse - 0.05) * U.salida(t, T_D2 - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "para unirse a la lucha", color=U.COL["verde"], px=76, k=k, cola=None)
    MD.brujula(lz, W - 110, H - 120, 1.0)


@shot(T_D2, bg=lambda t: bg_grad((40, 34, 70), (96, 70, 100), mid=(64, 50, 84), ym=0.55), post=[GRIS], ent=("fundido", 0.6))
def gu_mina_fin(lz, t):
    U.haces_luz(lz, W / 2, 380, t, n=7, largo=1300, color=(220, 200, 255), alfa=0.08, ancho=0.09)
    k = U.pop(t, T_D2 + 0.05, 1.2)
    fus = e_out(prog(t, t_fusi, t_fusi + 0.6))
    if k > 0.01:
        RT.retrato(lz, W / 2, 1000, 230 * (0.94 + 0.06 * k), "mina", t, emocion="serio", alfa=min(1.0, k) * (1 - 0.5 * fus), luz_borde=(220, 200, 255))
        U.llamada(lz, W / 2, 140, "Francisco Xavier Mina", color=U.COL["azul"], px=56, k=k, cola=None)
    kc = U.pop(t, t_capt - 0.05)
    if kc > 0.01:
        ml_cadena(lz, W / 2, 940, t, kc)
    if fus > 0.01:
        lz.relleno(np.array([[W / 2 - 220, 520], [W / 2 - 170, 480], [W / 2 + 230, 880], [W / 2 + 180, 930]]), (14, 12, 22), alfa=0.85 * fus, capa=2)
    k = U.pop(t, t_capt - 0.05) * U.salida(t, t_fusi - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 250, "capturado", color=U.COL["rojo"], px=90, k=k * U.repop(t, t_capt + 0.1), cola=None)
    k = U.pop(t, t_fusi - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 250, "fusilado ese mismo año", color=U.COL["rojo"], px=76, k=k * U.repop(t, t_fusi + 0.2), cola=None)


def ml_cadena(lz, x, y, t, k):
    import mundos_l as ml
    ml.cadena(lz, x, y, n=7, t=t, rota=0.0, ancho=100 * k)


# ------------------------------------------------------------------------------------------------ 5. 1820: DIEZ AÑOS DE GUERRA
def _vela(lz, x, y, alto, t, k=1.0):
    lz.relleno(rect_red(x - 18, y - alto, 36, alto, 6), (250, 240, 214), alfa=k, capa=2)
    lz.relleno(rect_red(x - 18, y - alto, 12, alto, 4), (255, 252, 240), alfa=k, capa=2)
    h = 36 + 8 * math.sin(t * 9 + x)
    lz.relleno(np.array([[x - 10, y - alto], [x, y - alto - h], [x + 10, y - alto]]), (255, 170, 60), alfa=k, capa=2)
    lz.relleno(np.array([[x - 5, y - alto], [x, y - alto - h * 0.6], [x + 5, y - alto]]), (255, 236, 150), alfa=k, capa=2)
    lz.halo(x, y - alto - 12, 80, (255, 190, 90), alfa=0.30 * k, capa=2)


@shot(T_E1, bg=lambda t: bg_grad((54, 30, 112), (150, 70, 130), mid=(100, 46, 130), ym=0.5), post=[GRAD], ent=("fundido", 0.5))
def gu_diez(lz, t):
    U.bokeh(lz, t, seed=81, n=12, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.20)
    u = prog(t, t_1820 - 0.1, t_diez + 0.9)
    anio = int(1810 + 10 * smooth(u))
    P.rotulo(lz, W / 2, 250, str(anio), px=260, k=U.pop(t, T_E1 + 0.05), color=(255, 255, 255))
    for i in range(10):                                      # diez velas que se van consumiendo
        k = U.pop(t, T_E1 + 0.1 + 0.07 * i)
        if k > 0.01:
            alto = 260 - 190 * smooth(prog(t, t_diez - 0.4 + 0.12 * i, t_diez + 1.2 + 0.1 * i))
            _vela(lz, 270 + 150 * i, 840, alto * k, t, k)
    k = U.pop(t, t_guerra2 - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 470, "la guerra llevaba diez años", color=U.COL["rojo"], px=76, k=k * U.repop(t, t_diez + 0.1), cola=None)


def cam_e2(t):
    return Klog(t, [(T_E2, (-100.0, 20.0, 1.3)), (T1(E13) - 8.5, (-100.0, 20.0, 1.45))]) if False else Klog(t, [(T_E2, (-100.0, 20.0, 1.3)), (t_ganar, (-100.0, 20.0, 1.45))])


@shot(T_E2, bg=lambda t: BASE(cam_e2(t), t), post=[lambda img, t: U.gradacion(img, luces=(0.96, 0.96, 1.0), sombras=(0.9, 0.92, 1.05), saturacion=0.62)], ent=("fundido", 0.5))
def gu_agotado(lz, t):
    cam = cam_e2(t)
    I.luz(mul=(0.92, 0.94, 1.0), mix=(40, 44, 100), k=0.14)
    MD.montes(lz, cam, min_alt=2200)
    MD.pais(lz, cam, "Mexico", (255, 96, 70), alfa=0.06, borde=(255, 220, 90), ancho=4.0, t=t, latido=0.0)
    for i, (lo, la) in enumerate(T12.FOCOS[:8]):
        sx, sy = MP.proy(cam, lo, la)
        a = smooth(prog(t, T_E2 + 0.1 * i, T_E2 + 0.5 + 0.1 * i))
        lz.halo(float(sx), float(sy), 130, (140, 255, 170), alfa=0.45 * a, capa=2)
        lz.relleno(circulo(float(sx), float(sy), 16, 14), (210, 255, 220), alfa=a, capa=2)
        # cercos realistas que se cierran: anillos rojos que se encogen
        if t > t_insu:
            r_ = 120 - 60 * smooth(prog(t, t_insu, t_acor + 0.8))
            lz.trazo(circulo(float(sx), float(sy), r_, 28), (232, 70, 80), 6, cerrado=True, afinar=False, temblor=0.0, capa=2)
    # «pocos pensaban que se pudiera ganar»: diez siluetas, solo una con esperanza
    kp = U.pop(t, t_pocos - 0.1) * U.salida(t, T1(E13) - 8.45, 0.25) if False else U.pop(t, t_pocos - 0.1)
    if kp > 0.01:
        for i in range(10):
            x = 420 + 120 * i
            col = (255, 214, 90) if i == 4 else (84, 84, 110)
            lz.relleno(rect_red(x - 26, 860 - 70, 52, 90, 20), col, alfa=min(1.0, kp), capa=2)
            lz.relleno(circulo(x, 860 - 94, 22, 14), col, alfa=min(1.0, kp), capa=2)
            if i != 4:
                P.rotulo(lz, x, 860 - 60, "?", px=44, k=min(1.0, kp), color=(210, 210, 230), sombra=0.0)
        lz.halo(420 + 480, 780, 120, (255, 214, 90), alfa=0.4 * min(1.0, kp), capa=2)
    k = U.pop(t, t_pais - 0.05) * U.salida(t, t_insu - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "el país estaba agotado", color=U.COL["rojo"], px=80, k=k * U.repop(t, t_agot + 0.1), cola=None)
    k = U.pop(t, t_insu - 0.05) * U.salida(t, t_pocos - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "los insurgentes, acorralados", color=U.COL["naranja"], px=76, k=k * U.repop(t, t_acor + 0.1), cola=None)
    k = U.pop(t, t_pocos - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "pocos pensaban que se pudiera ganar", color=U.COL["morado"], px=62, k=k * U.repop(t, t_ganar + 0.1), cola=None)
    MD.brujula(lz, W - 110, H - 120, 1.0)


# ------------------------------------------------------------------------------------------------ 6. EL COSTO DE LA GUERRA (cuatro paneles)
def _panel(lz, cx, cy, w, h, k, col):
    with lz.grupo(cx, cy, k, 0.0):
        lz.relleno(rect_red(-w / 2 + 12, -h / 2 + 16, w, h, 26), (20, 10, 50), alfa=0.30, capa=1)
        lz.relleno(rect_red(-w / 2, -h / 2, w, h, 24), col, capa=1)


def _ic_pueblo(lz, cx, cy, t):
    for j, (dx, s) in enumerate(((-150, 0.8), (0, 1.0), (150, 0.8))):
        with lz.grupo(cx + dx * 1.5, cy + 40, 1.0, 0.0):
            T07._icono_matanza(lz, 0, 0, 1.45 * s, t + j)


def _ic_camino(lz, cx, cy, t, u):
    lz.relleno(np.array([[cx - 380, cy + 120], [cx - 300, cy + 60], [cx + 380, cy + 40], [cx + 380, cy + 140]]), (214, 186, 136), capa=2)
    ang = -1.2 * (1 - e_out(u))
    with lz.grupo(cx + 40, cy + 70, 1.0, ang):
        lz.relleno(rect_red(-30, -250, 60, 280, 14), (120, 82, 58), capa=2)
        lz.relleno(circulo(0, -250, 30, 14), (186, 140, 100), capa=2)
        for j in range(3):
            lz.relleno(np.array([[-40 + 30 * j, -230], [-10 + 30 * j, -300], [10 + 30 * j, -230]]), (60, 140, 80), capa=2)
    lz.trazo(np.array([[cx - 250, cy + 40], [cx - 150, cy - 60]]), (90, 60, 40), 10, afinar=False, temblor=0.0, capa=2)       # hacha
    lz.relleno(np.array([[cx - 160, cy - 90], [cx - 100, cy - 70], [cx - 150, cy - 30]]), (176, 182, 196), capa=2)


def _ic_mina(lz, cx, cy, t, u):
    lz.relleno(np.array([[cx - 260, cy + 140], [cx - 260, cy - 30], [cx - 130, cy - 130], [cx + 130, cy - 130], [cx + 260, cy - 30], [cx + 260, cy + 140]]), (140, 120, 140), capa=2)
    lz.relleno(np.array([[cx - 150, cy + 140], [cx - 150, cy - 30], [cx - 80, cy - 90], [cx + 80, cy - 90], [cx + 150, cy - 30], [cx + 150, cy + 140]]), (40, 34, 52), capa=2)
    nivel = cy + 140 - 200 * smooth(u)
    pts = [(cx - 150 + k * 15, nivel + 6 * math.sin(t * 4 + k)) for k in range(0, 21)] + [(cx + 150, cy + 140), (cx - 150, cy + 140)]
    lz.relleno(np.array(pts), (70, 150, 220), alfa=0.9, capa=2)
    for sg in (-1, 1):
        lz.relleno(rect_red(cx + sg * 160 - 10, cy - 100, 20, 240, 4), (150, 106, 70), capa=2)
    lz.relleno(rect_red(cx - 170, cy - 130, 340, 24, 4), (150, 106, 70), capa=2)


def _ic_campos(lz, cx, cy, t, u):
    lz.relleno(rect_red(cx - 380, cy - 80, 760, 240, 20), (176, 138, 98), capa=2)
    for r in range(4):
        for c in range(14):
            x, y = cx - 340 + 52 * c, cy - 50 + 52 * r
            seca = smooth(u)
            col = tuple(int(a + (b - a) * seca) for a, b in zip((96, 170, 90), (160, 130, 80)))
            lz.trazo(np.array([[x, y + 20], [x + 14 * seca * (1 if (r + c) % 2 else -1), y - 26 + 14 * seca]]), col, 6, afinar=False, temblor=0.0, capa=2)
    for k in range(6):
        lz.trazo(np.array([[cx - 320 + 120 * k, cy + 130], [cx - 290 + 120 * k, cy + 100], [cx - 330 + 120 * k + 40, cy + 70]]), (120, 90, 64), 4, afinar=False, temblor=0.0, capa=2)


@shot(T_F, bg=lambda t: bg_grad((40, 24, 80), (110, 54, 110), mid=(70, 36, 100), ym=0.5), post=[GRAD], ent=("fundido", 0.5))
def gu_costo(lz, t):
    U.bokeh(lz, t, seed=82, n=10, colores=((255, 170, 90), (255, 80, 120), (120, 100, 255)), r=(50, 150), alfa=0.16)
    paneles = ((480, 330, t_quem, (176, 96, 80)), (1440, 330, t_cort, (100, 150, 110)), (480, 810, t_minas, (96, 120, 170)), (1440, 810, t_camp, (170, 150, 100)))
    for i, (cx, cy, tt_, col) in enumerate(paneles):
        k = U.pop(t, tt_ - 0.2, 1.2)
        if k > 0.01:
            _panel(lz, cx, cy, 860, 420, k, col)
            with lz.grupo(cx, cy, k, 0.0):
                if i == 0:
                    _ic_pueblo(lz, 0, 0, t)
                elif i == 1:
                    _ic_camino(lz, 0, 20, t, prog(t, tt_, tt_ + 1.2))
                elif i == 2:
                    _ic_mina(lz, 0, 20, t, prog(t, tt_, tt_ + 1.6))
                else:
                    _ic_campos(lz, 0, 20, t, prog(t, tt_, tt_ + 1.8))
    for (txt, col, tt_, x, y) in (("pueblos quemados", U.COL["rojo"], t_quem, 480, 160), ("caminos cortados", U.COL["verde"], t_cort, 1440, 160), ("minas inundadas", U.COL["azul"], t_inund, 480, 640), ("campos sin cultivar", U.COL["naranja"], t_cult - 0.9, 1440, 640)):
        k = U.pop(t, tt_ - 0.05)
        if k > 0.01:
            U.llamada(lz, x, y, txt, color=col, px=40, k=k * U.repop(t, tt_ + 0.2), cola=None)


# ------------------------------------------------------------------------------------------------ sonido
snd(T_A + 0.2, "amanecer", 0.3, dur=2.0)
snd(t_escond, "bling", 0.5)
snd(T_B, "pop", 0.3)
snd(t_mant, "tambor", 0.5)
snd(T_C, "amanecer", 0.2, dur=1.8)
snd(t_solo, "pluck", 0.4)
snd(t_com, "pop", 0.3)
snd(T_D1, "whoosh", 0.3, dur=1.0)
snd(t_desem, "pop", 0.4)
snd(T_D2, "gong", 0.4)
snd(t_fusi, "canonazo", 0.4)
snd(T_E1, "pop", 0.3)
snd(t_diez, "gong", 0.4)
snd(T_E2, "whoosh", 0.3, dur=0.9)
snd(t_acor, "tambor", 0.4)
snd(T_F, "pop", 0.3)
snd(t_quem, "explosion", 0.4)
snd(t_cort, "crujido", 0.5)
snd(t_inund, "ola", 0.4, dur=1.5)
snd(t_camp, "pluck", 0.4)
