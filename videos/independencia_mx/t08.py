# -*- coding: utf-8 -*-
"""Escena 8 · Guadalajara y el puente de Calderón (4:26-4:56): Hidalgo entra a Guadalajara, el decreto contra la esclavitud, El Despertador Americano y los ministros, la batalla del puente de Calderón y la explosión del depósito de pólvora."""
import math

import numpy as np

import kz_iso as I
from kz_iso import tint
import kz_iso_obj as O
import kz_iso_obj2 as O2
import kz_iso_arq as A
import kz_iso_arq2 as B
import kz_iso_int as N
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
import mundos_i as mi

E8 = "guadalajara"
MP = KM.MAPA
GRAD = lambda img, t: U.gradacion(img)
BASE = lambda cam, t: MP.base(cam, t, exag=13.0, rios_umbral=0.7)
GDL = mi.Guadalajara()
CAL = mi.CampoCalderon()

# ------------------------------------------------------------------ anclas
t_hid, t_est, t_gdl, t_ahi, t_pasos, t_imp = [T(E8, w, frase=0) for w in ("hidalgo", "establecio", "guadalajara", "ahi", "pasos", "importantes")]
t_pub, t_decr, t_abol, t_escl, t_pena, t_muerte, t_cumpl = [T(E8, w, frase=1) for w in ("publico", "decreto", "abolir", "esclavitud", "pena", "muerte", "cumpliera")]
t_fund, t_peri, t_insu, t_desp, t_amer, t_nomb, t_min = [T(E8, w, frase=2) for w in ("fundo", "periodico", "insurgente", "despertador", "americano", "nombro", "ministros")]
t_pero, t_enero, t_once, t_puente, t_cald, t_seis, t_sold, t_real, t_arm, t_derr, t_mult, t_enorme, t_mal, t_equi = [T(E8, w, frase=3) for w in ("pero", "enero", "once", "puente", "calderon", "seis", "soldados", "realistas", "armados", "derrotaron", "multitud", "enorme", "mal", "equipada")]
t_proy, t_estal, t_dep, t_pol, t_bat, t_perd, t_min2 = [T(E8, w, frase=4) for w in ("proyectil", "estallar", "deposito", "polvora", "batalla", "perdio", "minutos")]
T_A, T_A2, T_B, T_C, T_D, T_E = T0(E8), t_gdl - 0.1, t_pub - 0.2, t_fund - 0.25, t_pero - 0.2, t_proy - 0.3


# ------------------------------------------------------------------------------------------------ 1. HIDALGO LLEGA A GUADALAJARA
RUTA_G = [(-101.19, 19.70), (-102.0, 19.95), (-103.35, 20.67)]


def cam_g(t):
    return Klog(t, [(T_A, (-102.3, 20.1, 1.8)), (t_est, (-103.0, 20.45, 2.6)), (T_A2, (-103.33, 20.66, 3.2))])


@shot(T_A, bg=lambda t: BASE(cam_g(t), t), post=[GRAD], ent=("fundido", 0.5))
def gd_mapa(lz, t):
    cam = cam_g(t)
    I.luz()
    MD.montes(lz, cam, min_alt=2200)
    MD.pais(lz, cam, "Mexico", (255, 96, 70), alfa=0.12, borde=(255, 220, 90), ancho=4.0, t=t, latido=1.0)
    MD.ciudad(lz, cam, "valladolid", t, T_A, tam=1.2, tipo="ciudad", bando="ins", semilla=3)
    MD.etiqueta(lz, cam, "valladolid", "Valladolid", t, T_A + 0.1, px=22, dy=4, dx=120, lado="izq")
    MD.ciudad(lz, cam, "guadalajara", t, t_est - 0.1, tam=2.4, tipo="ciudad", bando=(255, 206, 70), semilla=5)
    f = e_inout(prog(t, T_A + 0.1, t_gdl))
    MD.ruta(lz, cam, RUTA_G, color=(255, 170, 90), frac=f, t=t, ancho=8.0, flecha=True)
    for i in range(5):
        u = max(0.0, min(0.999, f - 0.07 * i))
        if u > 0.01:
            x, y, v = MD.punto_ruta(cam, RUTA_G, u)
            MD.ejercito(lz, float(x), float(y), 12, bando="ins", t=t + i * 0.2, s=1.7, dir=-1, semilla=i, bandera=(i == 0), polvo=(i % 2 == 0))
    kh = U.pop(t, t_hid - 0.1)
    if kh > 0.01:
        MD.medallon(lz, 300, 480, 150, "hidalgo", t, emocion="neutro", k=kh, seed=2)
        U.llamada(lz, 300, 660, "Hidalgo", color=U.COL["morado"], px=44, k=kh, cola="arriba")
    k = U.pop(t, t_est - 0.05)
    if k > 0.01:
        sx, sy = MP.proy(cam, -103.35, 20.67)
        U.llamada(lz, float(sx), float(sy) - 140, "Guadalajara", color=U.COL["azul"], px=64, k=k * U.repop(t, t_gdl + 0.1), cola="abajo")
    MD.brujula(lz, W - 110, H - 120, 1.0)


def cam_p(t):
    return K(t, [(T_A2, (-40, 300, 30, 2.2)), (t_ahi, (120, 280, 34, 2.7)), (t_pasos, (200, 270, 34, 2.9)), (T_B, (220, 250, 34, 2.9))])


@shot(T_A2, bg=lambda t: bg_grad((130, 190, 240), (254, 232, 200), mid=(200, 218, 238), ym=0.5), post=[GRAD], ent=("zoom", 0.5))
def gd_plaza(lz, t):
    cx, cy, cz, zm = cam_p(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz(mul=(1.03, 1.0, 0.96), mix=(255, 220, 160), k=0.05)
    GDL.suelo(lz, iso, t)
    m = GDL.objetos(t)
    # desfile de entrada: Hidalgo a caballo con Allende, estandarte guadalupano y tropa; el pueblo vitorea
    u = e_inout(prog(t, T_A2 - 0.2, t_pasos + 1.4))
    px = lerp(-120, 215, u)
    m.add(px - 8, 288, px + 8, 306, 50, lambda lz, iso: G.caballo(lz, iso, px, 298, t, dir=1, seed=3, vel=1.0 if 0 < u < 1 else 0.0, jinete="cura", s=1.3), fijo=False, clave=px + 298 + 10)
    m.add(px - 40, 280, px - 28, 292, 50, lambda lz, iso: G.caballo(lz, iso, px - 36, 292, t, dir=1, seed=4, vel=1.0 if 0 < u < 1 else 0.0, jinete="oficial", s=1.3), fijo=False, clave=px + 292 - 26)
    m.add(px - 70, 300, px - 60, 310, 160, lambda lz, iso: O2.estandarte_virgen(lz, iso, px - 66, 308, h=48, t=t, w=30, alto=40), fijo=False, clave=px + 308 - 56)
    tipos = ("insurgente", "insurgente_lanza", "campesino", "indigena", "honda", "mestizo")
    for i in range(18):
        x = px - 90 - 20 * (i // 3) + 8 * h01(171, i)
        y = 290 + 8 * (i % 3) + 4 * h01(172, i)
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i: (lambda lz, iso: G.persona(lz, iso, x, y, t, tipos[i % 6], dir=(1, 0), vel=1.2 if 0 < u < 1 else 0.0, seed=8300 + i, h=42, accion="vitorea" if u >= 1 else None, cara="alegre")))(x, y, i), fijo=False, clave=x + y + 3)
    m.dibujar(lz, iso)
    DC.aves(lz, t, n=8, seed=71, y0=70, y1=260)
    for i in range(18):                                          # pétalos y confeti que lanzan los vecinos
        uu = ((t * 0.5 + h01(173, i)) % 1.0)
        qx, qy = iso.P(px - 60 + 140 * h01(174, i), 280 + 40 * h01(175, i), 70 - 60 * uu)
        lz.relleno(circulo(float(qx), float(qy), (3 + 2 * h01(176, i)) * iso.z / 3, 6), [(255, 92, 130), (255, 214, 72), (110, 200, 130), (255, 255, 255)][i % 4], alfa=0.9 * (1 - uu * 0.5), capa=2)
    U.fecha_lugar(lz, t, T_A2 + 0.2, T_B - 0.2, "Guadalajara", "Noviembre de 1810", y=70)
    k = U.pop(t, t_pasos - 0.1) * U.salida(t, T_B - 0.25, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "pasos muy importantes", color=U.COL["naranja"], px=80, k=k * U.repop(t, t_imp + 0.1), cola=None)


# ------------------------------------------------------------------------------------------------ 2. EL DECRETO CONTRA LA ESCLAVITUD
def cam_d(t):
    return K(t, [(T_B, (190, 235, 30, 3.1)), (t_abol, (190, 245, 30, 3.6)), (t_pena, (190, 245, 30, 3.8)), (T_C, (190, 245, 30, 3.6))])


@shot(T_B, bg=lambda t: bg_grad((130, 190, 240), (254, 232, 200), mid=(200, 218, 238), ym=0.5), post=[GRAD], ent=("fundido", 0.4))
def gd_decreto(lz, t):
    cx, cy, cz, zm = cam_d(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz(mul=(1.03, 1.0, 0.96), mix=(255, 220, 160), k=0.05)
    GDL.suelo(lz, iso, t)
    m = GDL.objetos(t, gente=0.3)
    # Hidalgo firma el decreto en una mesa bajo los portales; el escribano lo sostiene
    m.add(150, 150, 230, 190, 30, lambda lz, iso: mi.me.B.mesa(lz, iso, 150, 150, 80, 36, 20, color=(122, 82, 60), mantel=(150, 40, 60)) if False else B.mesa(lz, iso, 150, 150, 80, 36, 20, color=(122, 82, 60), mantel=(150, 40, 60)), fijo=False, clave=380)
    m.add(170, 182, 182, 194, 40, lambda lz, iso: G.persona(lz, iso, 176, 190, t, "cura", dir=(0, -1), seed=8400, h=52, accion="trabaja", cara="serio"), fijo=False, clave=380 + 9)
    m.add(204, 182, 216, 194, 40, lambda lz, iso: G.persona(lz, iso, 210, 190, t, "escribano", dir=(0, -1), seed=8401, h=50, cara="normal"), fijo=False, clave=380 + 20)
    # personas esclavizadas con grilletes: las cadenas se rompen al decir «esclavitud» y se van libres
    libre = prog(t, t_escl, t_escl + 0.5)
    for i in range(9):
        x, y = 90 + 28 * i, 262 + 10 * (i % 3)
        xx = x + (40 * (h01(177, i) - 0.5) * 2 * prog(t, t_escl + 0.6, t_cumpl))
        m.add(xx - 4, y - 4, xx + 4, y + 4, 40, (lambda xx, y, i: (lambda lz, iso: G.persona(lz, iso, xx, y, t, "esclavo", dir=(0, -1), seed=8410 + i, h=44, accion=("vitorea" if libre >= 1.0 else None), cara=("alegre" if libre >= 1.0 else "triste"))))(xx, y, i), fijo=False, clave=xx + y + 3)
        if libre < 1.0:
            m.add(xx - 5, y - 2, xx + 5, y + 4, 10, (lambda xx, y, i: (lambda lz, iso: (O2.grillete(lz, iso, xx - 3, y + 2, 3, t), O2.grillete(lz, iso, xx + 3, y + 2, 3, t + 0.3))))(xx, y, i), fijo=False, clave=xx + y + 4)
        else:
            for sg in (-1, 1):
                ux = (t - t_escl - 0.5)
                m.add(xx - 5, y - 2, xx + 5, y + 6, 10, (lambda xx, y, sg, ux: (lambda lz, iso: lz.relleno(circulo(*[float(v) for v in iso.P(xx + sg * (4 + 14 * ux), y + 2, max(0.0, 18 * ux - 22 * ux * ux) + 2)], 3.2 * iso.z / 3, 8), (150, 150, 170), alfa=max(0.0, 1 - ux * 0.7), capa=2)))(xx, y, sg, ux), fijo=False, clave=xx + y + 5)
    m.dibujar(lz, iso)
    DC.aves(lz, t, n=7, seed=72, y0=70, y1=240)
    for i in range(10):                                          # destellos de libertad
        if t > t_escl + 0.3:
            qx, qy = iso.P(90 + 28 * (i % 9), 262, 56)
            U.chispa4(lz, float(qx), float(qy) - 20 * h01(178, i), 10 + 6 * h01(179, i), alfa=0.9 * prog(t, t_escl + 0.3, t_escl + 0.8) * (0.6 + 0.4 * math.sin(t * 6 + i)))
    ks = U.pop(t, t_decr - 0.1)
    if ks > 0.01:
        U.pergamino_grande(lz, 520, 470, 520, 320, t, t_decr - 0.1, lineas=("Los dueños de esclavos", "deberán liberarlos", "so pena de muerte"), titulo="DECRETO", sello=True, rot=-0.05, alfa=min(1.0, ks) * U.salida(t, T_C - 0.3, 0.25))
    k = U.pop(t, t_abol - 0.05) * U.salida(t, t_pena - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2 + 280, 150, "abolir la esclavitud", color=U.COL["verde"], px=76, k=k * U.repop(t, t_escl + 0.1), cola=None)
    k = U.pop(t, t_pena - 0.05) * U.salida(t, T_C - 0.25, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2 + 280, 150, "pena de muerte", color=U.COL["rojo"], px=80, k=k * U.repop(t, t_muerte + 0.1), cola=None)
        for sg in (-1, 1):
            _espada(lz, W / 2 + 280 + sg * 380, 150, 0.6 * k, sg)


def _espada(lz, x, y, s, sg):
    lz.trazo(np.array([[x - 40 * s, y + 40 * s * sg], [x + 40 * s, y - 40 * s * sg]]), (238, 240, 250), 10 * s, afinar=False, temblor=0.0, capa=2)
    lz.trazo(np.array([[x - 14 * s, y - 14 * s * sg - 10 * s], [x + 2 * s, y - 14 * s * sg + 16 * s]]), (250, 206, 70), 8 * s, afinar=False, temblor=0.0, capa=2)


# ------------------------------------------------------------------------------------------------ 3. EL DESPERTADOR AMERICANO Y LOS MINISTROS
def cam_i(t):
    return K(t, [(T_C, (100, 115, 44, 3.9)), (t_desp, (90, 105, 44, 4.2)), (t_nomb - 0.2, (150, 130, 44, 3.9)), (t_nomb + 0.6, (205, 160, 44, 3.9)), (T_D, (210, 165, 44, 3.9))])


def _periodico_card(lz, x, y, s, k, t):
    w, h = 460 * s, 600 * s
    with lz.capa(2):
        with lz.grupo(x, y, k, 0.05 * math.sin(t * 1.4)):
            lz.relleno(rect_red(-w / 2 + 14, -h / 2 + 18, w, h, 10), (20, 10, 50), alfa=0.3)
            lz.relleno(rect_red(-w / 2, -h / 2, w, h, 8), (246, 238, 214))
            lz.relleno(np.array([[-w / 2 + 18, -h / 2 + 150 * s], [w / 2 - 18, -h / 2 + 150 * s], [w / 2 - 18, -h / 2 + 156 * s], [-w / 2 + 18, -h / 2 + 156 * s]]), (60, 46, 70))
            lz.texto("EL DESPERTADOR", 0, -h / 2 + 56 * s, int(54 * s), "geo", color=(50, 36, 60), borde=None, temblor=0.0)
            lz.texto("AMERICANO", 0, -h / 2 + 116 * s, int(54 * s), "geo", color=(50, 36, 60), borde=None, temblor=0.0)
            lz.texto("Guadalajara · diciembre de 1810", 0, -h / 2 + 184 * s, int(24 * s), "geo_n", color=(90, 70, 90), borde=None, temblor=0.0)
            for j in range(11):
                a = 0.5 + 0.5 * h01(181, j)
                lz.relleno(rect_red(-w / 2 + 22 * s, -h / 2 + (220 + 28 * j) * s, (w / 2 - 22 * s) * 0.9 * a * 2 / 2 + 60 * s, 6 * s, 2 * s), (90, 80, 100), alfa=0.8)
            lz.relleno(rect_red(w / 2 - 170 * s, -h / 2 + 232 * s, 140 * s, 110 * s, 6 * s), (150, 170, 200))
            lz.relleno(circulo(w / 2 - 100 * s, -h / 2 + 275 * s, 26 * s, 14), (250, 206, 70))


@shot(T_C, bg=lambda t: bg_grad((60, 40, 110), (160, 80, 130), mid=(106, 52, 124), ym=0.5), post=[GRAD], ent=("fundido", 0.5))
def gd_imprenta(lz, t):
    cx, cy, cz, zm = cam_i(t)
    I.luz(mul=(1.0, 0.96, 0.92), mix=(255, 170, 110), k=0.06)
    U.bokeh(lz, t, seed=41, n=12, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.20)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm), sx0=900, sy0=640)
    mi.imprenta(lz, iso, t)
    m = I.Mundo()
    kp = prog(t, t_fund, t_fund + 0.5)
    mi.amueblar_imprenta(m, t, kp)
    m.add(60, 130, 74, 144, 40, lambda lz, iso: G.persona(lz, iso, 68, 140, t, "escribano", dir=(0, -1), seed=8500, h=56, accion="trabaja", cara="serio"), fijo=False, clave=200)
    m.add(122, 100, 134, 112, 40, lambda lz, iso: G.persona(lz, iso, 128, 108, t, "comerciante", dir=(-1, 0.2), seed=8501, h=50, accion="carga"), fijo=False, clave=232)
    # mesa de los ministros (aparece al nombrarlos): tres personajes con pergamino
    mm = e_back(prog(t, t_nomb - 0.2, t_nomb + 0.4)) if t > t_nomb - 0.2 else 0.0
    if mm > 0.01:
        m.add(180, 140, 260, 180, 30, lambda lz, iso: B.mesa(lz, iso, 180, 140, 80, 36, 20, color=(122, 82, 60), mantel=(60, 90, 150)), fijo=False, clave=330)
        for i, (x, y, tp) in enumerate(((196, 190, "regidor"), (222, 192, "noble"), (248, 190, "escribano"))):
            m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, tp, i: (lambda lz, iso: G.persona(lz, iso, x, y, t, tp, dir=(0, -1), seed=8510 + i, h=50 * mm, cara="serio", accion="saluda" if (t > t_min and i == 1) else None)))(x, y, tp, i), fijo=False, clave=330 + 15 + i)
    m.dibujar(lz, iso)
    # los periódicos salen volando de la prensa
    if t > t_peri:
        for i in range(10):
            u = ((t - t_peri) * 0.7 + i * 0.1) % 1.0
            qx, qy = iso.P(80, 90, 40)
            xx = float(qx) + 60 * i - 150 + 400 * u
            yy = float(qy) - 40 - 380 * math.sin(math.pi * u) + 40 * i
            lz.relleno(rect_red(xx - 20, yy - 26, 40, 52, 3), (250, 246, 232), alfa=0.95 * (1 - u * 0.6), capa=2)
            lz.relleno(np.array([[xx - 14, yy - 16], [xx + 14, yy - 16], [xx + 14, yy - 12], [xx - 14, yy - 12]]), (60, 46, 70), alfa=0.8, capa=2)
    kc = U.pop(t, t_desp - 0.1, 1.3) * U.salida(t, t_nomb - 0.3, 0.25)
    if kc > 0.01:
        _periodico_card(lz, 1480, 520, 1.0, kc, t)
    k = U.pop(t, t_peri - 0.05) * U.salida(t, t_desp - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "un periódico insurgente", color=U.COL["naranja"], px=76, k=k * U.repop(t, t_insu + 0.1), cola=None)
    k = U.pop(t, t_min - 0.5) * U.salida(t, T_D - 0.2, 0.2)
    if k > 0.01:
        qx, qy = iso.P(222, 192, 66)
        U.llamada(lz, float(qx), float(qy) - 4, "ministros", color=U.COL["azul"], px=64, k=k * U.repop(t, t_min + 0.1), cola="abajo")


# ------------------------------------------------------------------------------------------------ 4. EL PUENTE DE CALDERÓN
def cam_c(t):
    return K(t, [(T_D, (270, 210, 30, 2.0)), (t_puente, (270, 200, 30, 2.7)), (t_seis, (440, 190, 34, 2.7)), (t_derr, (300, 200, 34, 2.2)), (t_mult, (70, 220, 34, 2.4)), (t_mal, (50, 240, 40, 3.4)), (T_E, (80, 232, 40, 3.2))])


T_ESTAL = t_estal
CANONES = ((408, 150), (408, 190), (408, 230), (408, 270), (408, 310))


def _batalla_gente(m, t, avance, seed=0):
    tipos_i = ("insurgente", "honda", "campesino", "indigena", "insurgente_lanza", "mestizo", "indigena_f", "campesina")
    for i in range(170):
        x = -190 + 400 * h01(190, i) ** 0.9
        y = 130 + 190 * h01(191, i)
        x += avance * 40 * h01(192, i)
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i: (lambda lz, iso: G.persona(lz, iso, x + 3 * math.sin(t * 2 + i), y + 2 * math.cos(t * 2.3 + i), t, tipos_i[i % 8], dir=(1, 0.1), vel=0.5, seed=8600 + i, h=42, accion=("pelea" if i % 3 == 0 and t > t_derr - 0.5 else ("vitorea" if i % 5 == 0 else None)), cara="enojo")))(x, y, i), fijo=False, clave=x + y + 3)
    tipos_r = ("realista", "granadero", "dragon", "oficial")
    for i in range(96):
        r_, c_ = i // 16, i % 16
        x0 = 430 + 16 * r_
        y0 = 130 + 11.5 * c_
        x = x0 - 220 * avance
        m.add(x - 4, y0 - 4, x + 4, y0 + 4, 40, (lambda x, y0, i: (lambda lz, iso: G.persona(lz, iso, x, y0, t, tipos_r[i % 4], dir=(-1, 0), vel=1.2 if 0.0 < avance < 1.0 else 0.0, seed=8700 + i, h=44, cara="serio", accion=None)))(x, y0, i), fijo=False, clave=x + y0 + 3)


@shot(T_D, bg=lambda t: bg_grad((120, 170, 230), (254, 222, 188), mid=(206, 196, 230), ym=0.5), post=[GRAD], ent=("fundido", 0.5))
def gd_calderon(lz, t):
    cx, cy, cz, zm = cam_c(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz(mul=(1.02, 0.98, 0.94), mix=(255, 214, 160), k=0.05)
    CAL.suelo(lz, iso, t)
    m = CAL.objetos(t)
    avance = e_inout(prog(t, t_derr, t_derr + 2.2)) * 0.5
    _batalla_gente(m, t, avance)
    for i, (x, y) in enumerate(CANONES):
        td = ((t * 1.0 + 0.3 * i) % 1.4) if t > t_seis - 0.3 else -1.0
        B.canon(m, x - 220 * avance, y, dir=-1, t_fn=lambda: t, disparo=td, escala=1.1)
    for (x, y) in ((420, 140), (420, 300)):
        m.add(x - 4, y - 4, x + 4, y + 4, 120, (lambda x, y: (lambda lz, iso: O2.faro_bandera(lz, iso, x - 220 * avance, y, color=(206, 56, 70), t=t, h=80)))(x, y), fijo=False, clave=x + y + 6)
    m.add(-20, 180, -10, 190, 120, lambda lz, iso: O2.estandarte_virgen(lz, iso, -14, 186, h=56, t=t, w=34, alto=46), fijo=False, clave=170)
    m.dibujar(lz, iso)
    for i, (x, y) in enumerate(CANONES):
        td = ((t * 1.0 + 0.3 * i) % 1.4) if t > t_seis - 0.3 else -1.0
        if 0 <= td < 0.25:
            qx, qy = iso.P(x - 220 * avance - 12, y + 6, 18)
            U.chispa4(lz, float(qx), float(qy), 20 * (1 - td * 3), color=(255, 226, 140), alfa=0.9)
            lz.halo(float(qx), float(qy), 80 * iso.z / 3.0, (255, 190, 90), alfa=0.30, capa=2)
        if t > t_seis - 0.3:
            O.humo(lz, iso, x - 220 * avance - 14, y + 6, 24, t + i, n=3, s=1.3, color=(214, 210, 222), alfa=0.55, seed=i)
    DC.aves(lz, t, n=6, seed=73, y0=60, y1=220)
    k = U.pop(t, t_enero - 0.05) * U.salida(t, t_puente - 0.15, 0.2)
    if k > 0.01:
        U.fecha_lugar(lz, t, T_D, t_seis - 0.2, "Calderón, Jalisco", "17 de enero de 1811", y=70)
    k = U.pop(t, t_puente - 0.05) * U.salida(t, t_seis - 0.15, 0.2)
    if k > 0.01:
        qx, qy = iso.P(310, 200, 70)
        U.llamada(lz, float(qx), float(qy) - 10, "puente de Calderón", color=U.COL["morado"], px=60, k=k * U.repop(t, t_cald + 0.1), cola="abajo")
    k = U.pop(t, t_seis - 0.1) * U.salida(t, t_derr - 0.2, 0.2)
    if k > 0.01:
        v = 6000 * smooth(prog(t, t_seis - 0.1, t_sold + 0.2))
        U.contador(lz, W / 2 + 330, 170, v, px=130, color=(255, 255, 255), k=k)
        U.llamada(lz, W / 2 + 330, 290, "soldados bien armados", color=U.COL["rojo"], px=52, k=k * U.repop(t, t_arm + 0.1), cola=None)
    k = U.pop(t, t_derr - 0.05) * U.salida(t, t_mult - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "¡derrotaron!", color=U.COL["rojo"], px=96, k=k * U.repop(t, t_derr + 0.2), cola=None)
    k = U.pop(t, t_mult - 0.05) * U.salida(t, t_mal - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "una multitud enorme…", color=U.COL["naranja"], px=82, k=k * U.repop(t, t_enorme + 0.1), cola=None)
    k = U.pop(t, t_mal - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "…pero mal equipada", color=U.COL["rojo"], px=82, k=k * U.repop(t, t_equi + 0.1), cola=None)
        for j, (lab, dx) in enumerate((("machetes", -380), ("hondas", 0), ("palos", 380))):
            kk = U.pop(t, t_mal + 0.15 + 0.3 * j)
            if kk > 0.01:
                U.llamada(lz, W / 2 + dx, 900, lab, color=U.COL["morado"], px=44, k=kk, cola="abajo")


# ------------------------------------------------------------------------------------------------ 5. EXPLOTA EL DEPÓSITO DE PÓLVORA
def cam_e(t):
    return K(t, [(T_E, (90, 232, 36, 3.0)), (t_estal, (110, 226, 34, 3.2)), (t_perd, (140, 220, 34, 2.4)), (T1(E8), (180, 210, 34, 2.2))])


def _explosion(lz, iso, x, y, z, t, t0):
    u = t - t0
    if u < 0:
        return
    sx, sy = iso.P(x, y, z)
    sx, sy = float(sx), float(sy)
    r = 330 * smooth(prog(t, t0, t0 + 0.8)) * (1.0 - 0.3 * prog(t, t0 + 0.8, t0 + 2.4))
    a = max(0.0, 1.0 - u / 2.6)
    lz.halo(sx, sy - 40, r * 2.0, (255, 150, 60), alfa=0.55 * a, capa=2)
    for rr, col in ((1.0, (240, 90, 40)), (0.78, (255, 150, 56)), (0.54, (255, 206, 90)), (0.28, (255, 250, 226))):
        lz.relleno(circulo(sx, sy - 70 * smooth(prog(t, t0, t0 + 1.2)), r * rr * 0.72, 30), col, alfa=min(1.0, a * 1.5), capa=2)
    for i in range(12):                                      # humo negro que sube
        uu = prog(t, t0 + 0.2 + 0.05 * i, t0 + 3.0)
        lz.relleno(circulo(sx + 40 * math.sin(i * 1.7) * uu, sy - 120 - 420 * uu, (30 + 70 * uu) * (0.8 + 0.2 * h01(201, i)), 14), (54, 50, 62), alfa=0.8 * (1 - uu), capa=2)
    for i in range(14):                                      # escombros que salen disparados
        ang = i * 0.45 + 0.4
        uu = prog(t, t0, t0 + 1.6)
        dx = math.cos(ang) * 520 * smooth(uu)
        dy = -math.sin(ang * 1.3) * 300 * smooth(uu) + 420 * uu * uu
        lz.relleno(circulo(sx + dx, sy - 60 + dy, 7 + 6 * h01(202, i), 8), [(120, 80, 60), (60, 60, 70), (250, 214, 90)][i % 3], alfa=1 - uu * 0.8, capa=2)
    ring = prog(t, t0, t0 + 1.4)
    if 0 < ring < 1:
        U.onda_iso(lz, iso, x, y, t, t0, dur=1.4, r1=420, n=2, color=(255, 236, 170), periodo=0.2, ancho=4.0)


@shot(T_E, bg=lambda t: bg_grad((110, 150, 220), (252, 214, 180), mid=(196, 176, 216), ym=0.5), post=[GRAD], ent=("destello", 0.4))
def gd_explosion(lz, t):
    cx, cy, cz, zm = cam_e(t)
    sh = 10 * max(0.0, 1 - (t - t_estal) / 0.8) if t_estal < t < t_estal + 0.8 else 0.0
    with lz.grupo(sh * math.sin(t * 90), sh * math.cos(t * 77), 1.0):
        iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
        I.luz(mul=(1.02, 0.96, 0.92), mix=(255, 190, 120), k=0.08)
        CAL.suelo(lz, iso, t)
        m = CAL.objetos(t)
        WX, WY = 120.0, 228.0
        boom = t >= t_estal
        if not boom:
            m.add(WX - 12, WY - 8, WX + 12, WY + 8, 30, lambda lz, iso: O.carreta(lz, iso, WX, WY, t, mov=0.0, carga=(70, 66, 76), s=1.2, bultos=True), fijo=False, clave=WX + WY)
            for j, (bx, by) in enumerate(((WX - 22, WY + 12), (WX + 24, WY + 10), (WX - 4, WY - 16), (WX + 16, WY - 12))):
                m.add(bx - 4, by - 4, bx + 4, by + 4, 20, (lambda bx, by: (lambda lz, iso: O.barril(lz, iso, bx, by, 1.1, (50, 50, 64))))(bx, by), fijo=False, clave=bx + by)
        # la multitud en pánico: al estallar todos huyen del centro de la explosión
        tipos = ("insurgente", "honda", "campesino", "indigena", "insurgente_lanza", "mestizo", "indigena_f", "campesina")
        for i in range(120):
            x0 = -120 + 330 * h01(190, i) ** 0.9
            y0 = 140 + 180 * h01(191, i)
            if boom:
                d = np.array([x0 - WX, y0 - WY])
                n = float(np.hypot(*d)) or 1.0
                d = d / n
                v = (160 + 120 * h01(203, i)) / (1 + n * 0.012)
                uu = min(2.2, t - t_estal)
                x, y = x0 + d[0] * v * uu * 1.2, y0 + d[1] * v * uu * 0.9 - 40 * (h01(204, i) - 0.5) * uu
                run = 1.9 if uu < 2.2 else 0.0
                dr = (d[0], d[1])
            else:
                x, y, run, dr = x0, y0, 0.5, (1, 0.1)
            m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i, run, dr: (lambda lz, iso: G.persona(lz, iso, x, y, t, tipos[i % 8], dir=dr, vel=run, seed=8800 + i, h=42, cara="miedo" if boom else "enojo", accion=None)))(x, y, i, run, dr), fijo=False, clave=x + y + 3)
        # los realistas avanzan por el puente tras la explosión
        for i in range(60):
            r_, c_ = i // 12, i % 12
            x = 330 + 20 * r_ - (160 * e_inout(prog(t, t_estal + 0.8, t_perd + 1.0)) if boom else 0)
            y = 150 + 13 * c_
            m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i: (lambda lz, iso: G.persona(lz, iso, x, y, t, ("realista", "granadero", "dragon")[i % 3], dir=(-1, 0), vel=1.2 if (boom and t > t_estal + 0.8) else 0.0, seed=8900 + i, h=44, cara="serio")))(x, y, i), fijo=False, clave=x + y + 3)
        m.dibujar(lz, iso)
        # el proyectil cruza el cielo y cae sobre el depósito de pólvora
        up = prog(t, t_proy, t_estal - 0.05)
        if 0 < up < 1 and not boom:
            bx, by = iso.P(lerp(380, WX, up), lerp(228, WY, up), 20 + 150 * math.sin(math.pi * up) * (1 - up * 0.3) + 20 * (1 - up))
            lz.relleno(circulo(float(bx), float(by), 7 * iso.z / 3, 10), (50, 50, 60), capa=2)
            lz.relleno(circulo(float(bx) - 2, float(by) - 2, 3 * iso.z / 3, 8), (150, 150, 166), capa=2)
            for j in range(6):
                lz.relleno(circulo(float(bx) + 18 * j, float(by) - 6 * j, (6 - j) * iso.z / 3, 8), (230, 226, 240), alfa=0.4 * (1 - j / 6), capa=2)
        if boom:
            _explosion(lz, iso, WX, WY, 14, t, t_estal)
    k = U.pop(t, t_proy - 0.05) * U.salida(t, t_estal - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "¡un proyectil!", color=U.COL["rojo"], px=88, k=k * U.repop(t, t_proy + 0.2), cola=None)
    k = U.pop(t, t_dep - 0.05) * U.salida(t, t_estal + 0.5, 0.2)
    if k > 0.01:
        qx, qy = iso.P(120, 228, 40)
        U.llamada(lz, float(qx), float(qy) - 60, "depósito de pólvora", color=U.COL["naranja"], px=54, k=k * U.repop(t, t_pol + 0.1), cola="abajo")
    k = U.pop(t, t_estal - 0.05) * U.salida(t, t_bat - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "¡estalla!", color=U.COL["rojo"], px=110, k=k * U.repop(t, t_estal + 0.2), cola=None)
    k = U.pop(t, t_bat - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "la batalla se pierde en minutos", color=U.COL["rojo"], px=70, k=k * U.repop(t, t_min2 + 0.1), cola=None)
        # reloj que corre rápido
        ck = U.pop(t, t_perd - 0.1)
        if ck > 0.01:
            cxr, cyr, rr = 1700, 300, 90 * ck
            lz.relleno(circulo(cxr, cyr, rr, 28), (255, 255, 255), capa=2)
            lz.relleno(circulo(cxr, cyr, rr * 0.9, 28), (250, 244, 232), capa=2)
            ang = (t - t_perd) * 9.0 - math.pi / 2
            lz.trazo(np.array([[cxr, cyr], [cxr + rr * 0.7 * math.cos(ang), cyr + rr * 0.7 * math.sin(ang)]]), (60, 40, 90), 7, afinar=False, temblor=0.0, capa=2)
            lz.trazo(np.array([[cxr, cyr], [cxr + rr * 0.45 * math.cos(ang / 12), cyr + rr * 0.45 * math.sin(ang / 12)]]), (60, 40, 90), 10, afinar=False, temblor=0.0, capa=2)


# ------------------------------------------------------------------------------------------------ sonido
snd(T_A + 0.2, "whoosh", 0.3, dur=1.0)
snd(t_est, "pop", 0.4)
snd(T_A2, "tambor", 0.4)
snd(t_pasos, "bling", 0.4)
snd(t_decr, "pop", 0.4)
snd(t_escl + 0.1, "crujido", 0.5)
snd(t_escl + 0.3, "bling", 0.5)
snd(t_pena, "gong", 0.5)
snd(T_C, "pop", 0.3)
for _i in range(6):
    snd(t_fund + 0.3 + 0.5 * _i, "bonk", 0.25)
snd(t_desp, "bling", 0.5)
snd(t_min, "pop", 0.4)
snd(T_D, "whoosh", 0.3, dur=0.9)
for _i in range(8):
    snd(t_seis + 0.5 * _i, "canonazo", 0.35)
snd(t_derr, "gong", 0.5)
snd(t_mult, "tambor", 0.5)
snd(t_proy, "whoosh", 0.5, dur=0.9)
snd(t_estal, "explosion", 0.8)
snd(t_estal + 0.2, "explosion", 0.5)
snd(t_perd, "gong", 0.5)
