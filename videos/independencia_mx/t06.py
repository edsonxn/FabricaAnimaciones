# -*- coding: utf-8 -*-
"""Escena 6 · Guanajuato (3:13-3:49): la ciudad de la plata, los españoles se encierran en la Alhóndiga, el asedio y el Pípila, la entrada y el saqueo, los criollos ricos cambian de bando y el ejército crece hacia la capital."""
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

E6 = "guanajuato"
MP = KM.MAPA
GRAD = lambda img, t: U.gradacion(img)
BASE = lambda cam, t: MP.base(cam, t, exag=12.0, rios_umbral=0.7)
GTO = mg.GuanajuatoCiudad()
CMP = mg.Campamentos()
PUERTA = (315.0, 121.0)

# ------------------------------------------------------------------ anclas
t_su, t_prim, t_gua, t_cent, t_min, t_pla = T(E6, "su", frase=0), T(E6, "primera", frase=0), T(E6, "guanajuato", frase=0), T(E6, "centro", frase=0), T(E6, "minas", frase=0), T(E6, "plata", frase=0)
t_def, t_esp, t_enc, t_alm, t_gran, t_alh, t_gdit = T(E6, "defensores", frase=1), T(E6, "espanoles", frase=1), T(E6, "encerraron", frase=1), T(E6, "almacen", frase=1), T(E6, "granos", frase=1), T(E6, "alhondiga", frase=1), T(E6, "granaditas", frase=1)
t_ejer, t_rod, t_comb, t_brut, t_ley, t_minero, t_pip, t_cruz, t_puer, t_losa, t_espal, t_prend, t_fue = [T(E6, w, frase=2) for w in ("ejercito", "rodeo", "combate", "brutal", "leyenda", "minero", "pipila", "cruzo", "puerta", "losa", "espalda", "prendio", "fuego")]
t_ins, t_entr, t_mat, t_saq, t_terr = [T(E6, w, frase=3) for w in ("insurgentes", "entraron", "matanza", "saqueo", "terribles")]
t_viol, t_asus, t_crio, t_ric, t_simp, t_caus, t_paso, t_bando, t_rey = [T(E6, w, frase=4) for w in ("violencia", "asusto", "criollos", "ricos", "simpatizaban", "causa", "pasaron", "bando", "rey")]
t_aun, t_ejh, t_crec, t_avan, t_cap = [T(E6, w, frase=5) for w in ("aun", "ejercito", "crecio", "avanzo", "capital")]
T_A, T_A2, T_B, T_C, T_D, T_E, T_F = T0(E6), t_cent - 0.25, t_def - 0.2, t_ejer - 0.1, t_ins - 0.1, t_viol - 0.15, t_aun - 0.1


def _lingotes_mapa(lz, x, y, s, k):
    """Montoncito de barras de plata con destello (icono de las minas) en pantalla."""
    for i, (dx, dy) in enumerate(((-14, 0), (14, 0), (0, -9), (-7, -18), (7, -18))):
        c = (176, 192, 220) if i % 2 else (206, 218, 238)
        lz.relleno(rect_red(x + (dx - 11) * s * k, y + (dy - 8) * s * k, 22 * s * k, 9 * s * k, 2 * s * k), c, capa=2)
        lz.relleno(rect_red(x + (dx - 9) * s * k, y + (dy - 8) * s * k, 12 * s * k, 3 * s * k, 1.5 * s * k), (244, 248, 255), capa=2)


# ------------------------------------------------------------------------------------------------ 1. GUANAJUATO EN EL MAPA
RUTA_A = [(-100.81, 20.52), (-100.95, 20.75), (-101.10, 20.92), (-101.26, 21.02)]


def cam_a(t):
    return Klog(t, [(T_A, (-100.7, 20.8, 1.8)), (t_gua, (-101.05, 20.92, 2.9)), (T_A2, (-101.2, 21.0, 3.4))])


@shot(T_A, bg=lambda t: BASE(cam_a(t), t), post=[GRAD], ent=("fundido", 0.5))
def gt_mapa(lz, t):
    cam = cam_a(t)
    I.luz()
    MD.montes(lz, cam, min_alt=2200)
    MD.pais(lz, cam, "Mexico", (255, 96, 70), alfa=0.12, borde=(255, 220, 90), ancho=4.0, t=t, latido=1.0)
    for j, (lug, tp, nm, dx, dy, lado) in enumerate((("dolores", "pueblo", "Dolores", 100, 4, "izq"), ((-100.81, 20.52), "ciudad", "Celaya", 100, 4, "izq"), ((-100.74, 20.91), "pueblo", "San Miguel", 120, 4, "izq"))):
        MD.ciudad(lz, cam, lug, t, T_A + 0.1 * j, tam=1.1, tipo=tp, bando="real", semilla=j + 31)
        MD.etiqueta(lz, cam, lug, nm, t, T_A + 0.1 * j + 0.1, px=22, dy=dy, dx=dx, lado=lado)
    MD.ciudad(lz, cam, "guanajuato", t, t_gua - 0.1, tam=2.6, tipo="ciudad", bando=(255, 206, 70), semilla=5)
    f = e_inout(prog(t, T_A + 0.2, t_gua + 0.4))
    MD.ruta(lz, cam, RUTA_A, color=(255, 214, 84), frac=f, t=t, ancho=7.0, flecha=False)
    for i in range(6):
        u = max(0.0, min(0.999, f - 0.045 * i))
        if u > 0.01:
            x, y, v = MD.punto_ruta(cam, RUTA_A, u)
            MD.ejercito(lz, float(x), float(y), 12, bando="ins", t=t + i * 0.2, s=1.5, dir=-1, semilla=i, bandera=(i == 0), polvo=(i % 2 == 0))
    k = U.pop(t, t_gua - 0.05) * U.salida(t, t_cent - 0.3, 0.2)
    if k > 0.01:
        sx, sy = MP.proy(cam, -101.26, 21.02)
        U.llamada(lz, float(sx), float(sy) - 120, "Guanajuato", color=U.COL["morado"], px=76, k=k * U.repop(t, t_gua + 0.4), cola="abajo")
    k = U.pop(t, t_prim - 0.05) * U.salida(t, t_gua - 0.1, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "su primera gran ciudad", color=U.COL["naranja"], px=70, k=k, cola=None)
    MD.brujula(lz, W - 110, H - 120, 1.0)


# ------------------------------------------------------------------------------------------------ 2. LA CIUDAD DE LAS MINAS
def cam_gt(t):
    return K(t, [(T_A2, (160, 190, 44, 1.5)), (t_min, (-5, 40, 44, 2.7)), (t_pla, (-10, 36, 40, 3.0)), (T_B, (150, 150, 44, 2.4))])


@shot(T_A2, bg=lambda t: bg_grad((130, 190, 240), (254, 236, 206), mid=(196, 220, 238), ym=0.5), post=[GRAD], ent=("zoom", 0.6))
def gt_minas(lz, t):
    cx, cy, cz, zm = cam_gt(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz(mul=(1.03, 1.0, 0.96), mix=(255, 220, 160), k=0.05)
    mg.cerros(lz, cx, cy, t)
    GTO.suelo(lz, iso, t)
    m = GTO.objetos(t)
    m.dibujar(lz, iso)
    DC.aves(lz, t, n=7, seed=61, y0=70, y1=260)
    DC.polvo_luz(lz, t, n=20, seed=62, color=(255, 230, 190), alfa=0.35)
    k = U.pop(t, t_cent - 0.1) * U.salida(t, t_min - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "el centro minero", color=U.COL["naranja"], px=72, k=k, cola=None)
    k = U.pop(t, t_min - 0.05)
    if k > 0.01:
        qx, qy = iso.P(-30, 50, 60)
        U.llamada(lz, float(qx) + 20, float(qy) - 70, "minas de plata", color=U.COL["azul"], px=64, k=k * U.repop(t, t_pla + 0.1), cola="abajo")
        for i in range(6):
            U.chispa4(lz, float(qx) + 160 * math.cos(i * 1.05 + t * 1.3) * 0.7, float(qy) + 90 * math.sin(i * 1.05 + t * 1.3) * 0.5, 12 + 6 * (i % 3), alfa=0.9 * k)


# ------------------------------------------------------------------------------------------------ 3. LOS ESPAÑOLES SE ENCIERRAN EN LA ALHÓNDIGA
def cam_b(t):
    return K(t, [(T_B, (310, 160, 44, 2.4)), (t_enc, (312, 110, 52, 3.0)), (t_alh, (315, 80, 56, 3.2)), (T_C, (315, 80, 56, 3.1))])


def _defensores(m, t, desde, n=14, z=84.0):
    for i in range(n):
        x = 244 + 142 * i / (n - 1)
        ti = desde + 0.12 * i
        k = e_back(prog(t, ti, ti + 0.4)) if t >= ti else 0.0
        if k > 0.01:
            m.add(x - 3, 104, x + 3, 110, 120, (lambda x, i, k: (lambda lz, iso: G.persona(lz, iso, x, 108, t, "realista", dir=(0, 1), seed=7000 + i, h=40 * k, z=z, cara="miedo" if i % 3 else "enojo", accion="pelea" if (t > t_comb and i % 2) else None)))(x, i, k), fijo=False, clave=x + 108 + 40)


@shot(T_B, bg=lambda t: bg_grad((130, 190, 240), (254, 236, 206), mid=(196, 220, 238), ym=0.5), post=[GRAD], ent=("fundido", 0.5))
def gt_alhondiga(lz, t):
    cx, cy, cz, zm = cam_b(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz(mul=(1.03, 1.0, 0.96), mix=(255, 220, 160), k=0.05)
    mg.cerros(lz, cx, cy, t)
    GTO.suelo(lz, iso, t)
    m = GTO.objetos(t, gente=0.0)
    # los españoles y sus familias llegan corriendo con costales de grano y cofres y se meten por el portón
    tipos = ("peninsular", "noble", "dama", "regidor", "dama", "nino", "noble", "escribano", "realista", "dama")
    for i in range(16):
        ti = T_B + 0.1 + 0.28 * i
        u = prog(t, ti, ti + 2.0)
        if 0 < u < 1:
            x0, y0 = 120 + 330 * h01(91, i), 270 + 40 * h01(92, i)
            x, y = lerp(x0, PUERTA[0] + 2 * (i % 5 - 2), e_in(u)), lerp(y0, PUERTA[1] + 10, e_in(u))
            a = 1.0 - max(0.0, (u - 0.85) / 0.15)
            m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i, a: (lambda lz, iso: G.persona(lz, iso, x, y, t, tipos[i % 10], dir=(PUERTA[0] - x, PUERTA[1] - y), vel=1.6, seed=7100 + i, h=44 if tipos[i % 10] != "nino" else 30, cara="miedo", alfa=a, accion="carga" if i % 3 == 0 else None)))(x, y, i, a), fijo=False, clave=x + y + 5)
    _defensores(m, t, t_enc + 0.1)
    # costales de grano apilados junto a la fachada
    for i, (x, y) in enumerate(((258, 128), (266, 132), (262, 138), (362, 130), (370, 134), (366, 140), (340, 136), (292, 138))):
        m.add(x - 4, y - 4, x + 4, y + 4, 12, (lambda x, y: (lambda lz, iso: O.costal(lz, iso, x, y, 1.1)))(x, y), fijo=False, clave=x + y + 2)
    m.dibujar(lz, iso)
    DC.aves(lz, t, n=7, seed=63, y0=70, y1=240)
    k = U.pop(t, t_def - 0.05) * U.salida(t, t_alm - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "los defensores españoles", color=U.COL["rojo"], px=68, k=k, cola=None)
    k = U.pop(t, t_alm - 0.05) * U.salida(t, t_alh - 0.15, 0.2)
    if k > 0.01:
        qx, qy = iso.P(300, 130, 24)
        U.llamada(lz, float(qx) - 40, float(qy) + 80, "un enorme almacén de granos", color=U.COL["naranja"], px=54, k=k * U.repop(t, t_gran + 0.1), cola=None)
    k = U.pop(t, t_alh - 0.05)
    if k > 0.01:
        qx, qy = iso.P(315, 40, 110)
        U.llamada(lz, float(qx), float(qy) - 10, "Alhóndiga de Granaditas", color=U.COL["morado"], px=58, k=k * U.repop(t, t_gdit + 0.1), cola="abajo")


# ------------------------------------------------------------------------------------------------ 4. EL ASEDIO Y EL PÍPILA
def cam_c(t):
    return K(t, [(T_C, (310, 210, 30, 2.2)), (t_comb, (312, 190, 40, 2.6)), (t_pip - 0.4, (312, 172, 46, 3.0)), (t_puer, (314, 150, 50, 3.6)), (t_prend, (314, 134, 50, 4.2)), (T_D, (314, 134, 50, 4.2))])


def _piedra(lz, iso, t, x0, y0, xt, yt, ph, per=1.3):
    u = ((t * 1.0 + ph) % per) / per
    z0, z1 = 26.0, 90.0
    z = z0 + (z1 - z0) * u + 70 * math.sin(math.pi * u)
    sx, sy = iso.P(lerp(x0, xt, u), lerp(y0, yt, u), z)
    lz.relleno(circulo(float(sx), float(sy), 3.2 * iso.z, 8), (96, 92, 104), capa=2)
    lz.relleno(circulo(float(sx) - 0.8 * iso.z, float(sy) - 0.8 * iso.z, 1.4 * iso.z, 6), (176, 172, 184), capa=2)


@shot(T_C, bg=lambda t: bg_grad((120, 160, 230), (252, 214, 190), mid=(214, 168, 210), ym=0.5), post=[GRAD], ent=("fundido", 0.4))
def gt_asedio(lz, t):
    cx, cy, cz, zm = cam_c(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz(mul=(1.04, 0.97, 0.92), mix=(255, 170, 120), k=0.10)
    mg.cerros(lz, cx, cy, t)
    GTO.suelo(lz, iso, t)
    m = GTO.objetos(t, gente=0.0)
    _defensores(m, t, T_C - 9.0)
    # el ejército insurgente rodea la Alhóndiga: llega desde las calles y se abre en arco frente al portón
    tipos = ("insurgente", "honda", "campesino", "minero", "indigena", "insurgente_lanza", "mestizo", "indigena_f")
    for i in range(78):
        a = -1.25 + 2.5 * h01(95, i)
        r = 70 + 120 * h01(96, i)
        xt, yt = 315 + r * math.sin(a) * 1.5, 120 + r * math.cos(a) * 0.9 + 22
        if abs(xt - PUERTA[0]) < 18 and yt < 175:
            xt += 36 * (1 if xt >= PUERTA[0] else -1)
        sx_, sy_ = (60, 260) if i % 2 else (560, 260)
        u = e_out(prog(t, T_C - 3.0 + 3.6 * h01(97, i), T_C + 1.4 + 3.6 * h01(97, i)))
        x, y = lerp(sx_, xt, u), lerp(sy_, yt, u)
        lanza = t > t_comb
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i, u: (lambda lz, iso: G.persona(lz, iso, x, y, t, tipos[i % 8], dir=(PUERTA[0] - x, PUERTA[1] - y), vel=1.5 if 0 < u < 0.99 else 0.0, seed=7200 + i, h=42, accion=("pelea" if (u >= 0.99 and i % 3 == 0) else ("vitorea" if u >= 0.99 and i % 3 == 1 else None)), cara="enojo")))(x, y, i, u), fijo=False, clave=x + y + 4)
    # el Pípila: se agacha bajo una losa y avanza hasta el portón
    up = e_inout(prog(t, t_pip, t_puer + 0.8))
    px_, py_ = lerp(300, PUERTA[0], up), lerp(232, PUERTA[1] + 6, up)
    if t > t_pip - 0.3:
        m.add(px_ - 4, py_ - 4, px_ + 4, py_ + 4, 60, lambda lz, iso: _pipila(lz, iso, t, px_, py_, up), fijo=False, clave=px_ + py_ + 20)
    m.dibujar(lz, iso)
    # humo y destellos de mosquetes desde la azotea; piedras de las hondas
    for i in range(12):
        x = 252 + 130 * i / 11
        fl = max(0.0, math.sin(t * 9 + i * 2.3))
        if t > T_C and fl > 0.8:
            qx, qy = iso.P(x, 110, 100)
            U.chispa4(lz, float(qx), float(qy), 12 + 8 * fl, color=(255, 230, 150), alfa=0.9)
        if t > T_C and i % 2 == 0:
            O.humo(lz, iso, x, 108, 96, t + i, n=3, s=1.0, color=(236, 232, 240), alfa=0.55, seed=i) if False else None
    for i in range(9):
        x0, y0 = 230 + 170 * h01(98, i), 190 + 60 * h01(99, i)
        if t > t_comb - 0.3:
            _piedra(lz, iso, t, x0, y0, 250 + 130 * h01(100, i), 118, i * 0.37)
    fuego = e_out(prog(t, t_prend, t_prend + 0.9))
    if fuego > 0.01:
        for j in range(4):
            O.fuego(lz, iso, 304 + 7 * j, 122, 1.0 * fuego, t, seed=j, halo=(j == 0))
        qx, qy = iso.P(PUERTA[0], PUERTA[1], 20)
        lz.halo(float(qx), float(qy), 330 * fuego, (255, 170, 80), alfa=0.35, capa=2)
        O.humo(lz, iso, 315, 122, 40, t, n=6, s=1.6 * fuego, color=(60, 56, 70), alfa=0.8)
    # rótulos
    k = U.pop(t, t_ejer - 0.05) * U.salida(t, t_comb - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "el ejército insurgente la rodea", color=U.COL["naranja"], px=64, k=k, cola=None)
    k = U.pop(t, t_comb - 0.05) * U.salida(t, t_ley - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "un combate brutal", color=U.COL["rojo"], px=86, k=k * U.repop(t, t_brut + 0.1), cola=None)
    k = U.pop(t, t_ley - 0.05) * U.salida(t, t_pip - 0.3, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "cuenta la leyenda…", color=U.COL["morado"], px=68, k=k, cola=None)
    if t > t_pip - 0.2:
        qx, qy = iso.P(px_, py_, 60)
        k = U.pop(t, t_pip - 0.1) * U.salida(t, t_losa - 0.1, 0.2)
        if k > 0.01:
            U.llamada(lz, float(qx), float(qy) - 20, "el Pípila", color=U.COL["azul"], px=56, k=k * U.repop(t, t_pip + 0.2), cola="abajo")
        k = U.pop(t, t_losa - 0.05) * U.salida(t, t_prend - 0.1, 0.2)
        if k > 0.01:
            U.llamada(lz, float(qx) + 150, float(qy) - 20, "una losa a la espalda", color=U.COL["naranja"], px=44, k=k, cola="abajo")
    k = U.pop(t, t_prend - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "¡le prendió fuego!", color=U.COL["rojo"], px=92, k=k * U.repop(t, t_fue + 0.1), cola=None)


def _pipila(lz, iso, t, x, y, up):
    G.persona(lz, iso, x, y, t, "minero", dir=(0, -1), vel=1.2 if 0 < up < 1 else 0.0, seed=7300, h=36, cara="esfuerzo" if False else "enojo")
    # losa grande de piedra sobre la espalda (cartel plano), la cabeza queda debajo
    lz.relleno(iso.pts([(x - 12, y + 6, 8), (x + 12, y + 6, 8), (x + 12, y + 6, 46), (x - 12, y + 6, 46)]), tint((150, 146, 160)))
    lz.relleno(iso.pts([(x - 12, y + 6, 40), (x + 12, y + 6, 40), (x + 12, y + 6, 46), (x - 12, y + 6, 46)]), tint((190, 186, 198)))
    lz.relleno(iso.pts([(x - 12, y + 6, 8), (x - 9, y + 6, 8), (x - 9, y + 6, 46), (x - 12, y + 6, 46)]), tint((120, 116, 132)))


# ------------------------------------------------------------------------------------------------ 5. ENTRAN Y SAQUEAN
def cam_d(t):
    return K(t, [(T_D, (314, 136, 50, 4.0)), (t_mat, (314, 150, 46, 3.2)), (t_saq, (314, 164, 46, 2.9)), (T_E, (314, 180, 46, 2.6))])


@shot(T_D, bg=lambda t: bg_grad((90, 60, 100), (210, 120, 100), mid=(150, 80, 100), ym=0.5), post=[lambda img, t: U.gradacion(img, luces=(1.04, 0.96, 0.92), sombras=(0.96, 0.94, 1.04), saturacion=1.02)], ent=("destello", 0.4))
def gt_saqueo(lz, t):
    cx, cy, cz, zm = cam_d(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz(mul=(1.02, 0.92, 0.88), mix=(255, 130, 80), k=0.14)
    mg.cerros(lz, cx, cy, t, tonos=((130, 110, 120), (108, 92, 108), (88, 76, 98)))
    GTO.suelo(lz, iso, t)
    m = GTO.objetos(t, gente=0.0)
    _defensores(m, t, T_D - 9.0, n=6)
    # la multitud entra por el portón; salen con costales y monedas; nadie queda quieto
    tipos = ("insurgente", "honda", "campesino", "minero", "indigena", "insurgente_lanza", "mestizo", "indigena_f")
    for i in range(60):
        ti = T_D + 3.2 * h01(110, i) - 1.0
        u = (t - ti) / 2.4
        if 0 < u < 1:
            x0 = 315 + 200 * (h01(111, i) - 0.5)
            x, y = lerp(x0, PUERTA[0] + 14 * (h01(112, i) - 0.5), e_in(u)), lerp(250, PUERTA[1] + 8, e_in(u))
            a = 1.0 - max(0.0, (u - 0.88) / 0.12)
            m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i, a: (lambda lz, iso: G.persona(lz, iso, x, y, t, tipos[i % 8], dir=(0, -1), vel=1.8, seed=7400 + i, h=42, accion="pelea" if i % 3 == 0 else None, cara="enojo", alfa=a)))(x, y, i, a), fijo=False, clave=x + y + 4)
    for i in range(14):                                         # los que salen cargados
        ti = t_saq - 0.6 + 0.3 * i
        u = (t - ti) / 2.0
        if 0 < u < 1:
            x, y = lerp(PUERTA[0] + 4 * (i % 3 - 1), 120 + 400 * h01(113, i), e_out(u)), lerp(PUERTA[1] + 10, 290, e_out(u))
            m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i: (lambda lz, iso: G.persona(lz, iso, x, y, t, tipos[i % 8], dir=(x - PUERTA[0], 1), vel=1.8, seed=7500 + i, h=42, accion="carga")))(x, y, i), fijo=False, clave=x + y + 4)
    for i in range(10):                                         # costales y monedas que vuelan
        u = ((t - t_mat) * 0.9 + i * 0.13) % 1.0
        if t > t_mat - 0.2:
            bx = PUERTA[0] + 170 * (h01(114, i) - 0.5) * u * 2
            by = PUERTA[1] + 12 + 80 * u
            bz = 8 + 40 * math.sin(math.pi * u)
            m.add(bx - 3, by - 3, bx + 3, by + 3, 20, (lambda bx, by, bz, i: (lambda lz, iso: O2.moneda(lz, iso, bx, by, bz, r=3.4, t=t + i * 0.3) if i % 2 else O.costal(lz, iso, bx, by, 1.0)))(bx, by, bz, i), fijo=False, clave=bx + by + 6)
    m.dibujar(lz, iso)
    fuego = e_out(prog(t, T_D - 0.2, T_D + 0.5))
    for j in range(4):
        O.fuego(lz, iso, 304 + 7 * j, 122, 1.1, t, seed=j, halo=(j == 0))
    qx, qy = iso.P(PUERTA[0], PUERTA[1], 20)
    lz.halo(float(qx), float(qy), 420, (255, 160, 70), alfa=0.35, capa=2)
    for (hx, hy) in ((260, 106), (370, 106), (300, 100)):
        O.humo(lz, iso, hx, hy, 70, t + hx, n=5, s=1.8, color=(60, 56, 70), alfa=0.75)
    U.viñeta_color(lz, (60, 10, 20), 0.0) if False else None
    k = U.pop(t, t_ins - 0.05) * U.salida(t, t_mat - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "los insurgentes entran", color=U.COL["naranja"], px=70, k=k, cola=None)
    k = U.pop(t, t_mat - 0.05) * U.salida(t, t_saq - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "una matanza", color=U.COL["rojo"], px=96, k=k * U.repop(t, t_mat + 0.2), cola=None)
    k = U.pop(t, t_saq - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "y un saqueo terribles", color=U.COL["rojo"], px=84, k=k * U.repop(t, t_terr + 0.1), cola=None)


# ------------------------------------------------------------------------------------------------ 6. LOS CRIOLLOS RICOS CAMBIAN DE BANDO
def cam_e(t):
    return K(t, [(T_E, (225, 190, 34, 2.7)), (t_crio, (225, 190, 34, 3.0)), (t_paso, (235, 190, 34, 3.3)), (T_F, (245, 190, 34, 3.1))])


@shot(T_E, bg=lambda t: bg_grad((60, 40, 120), (170, 90, 130), mid=(110, 56, 128), ym=0.5), post=[GRAD], ent=("fundido", 0.5))
def gt_criollos(lz, t):
    cx, cy, cz, zm = cam_e(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz(mul=(0.96, 0.94, 1.02), mix=(120, 80, 160), k=0.08)
    U.bokeh(lz, t, seed=28, n=10, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.18)
    CMP.suelo(lz, iso, t)
    m = CMP.objetos(t)
    # soldados de cada bando en sus campamentos
    for i, (x, y) in enumerate(((50, 90), (70, 160), (100, 230), (140, 130), (36, 250), (110, 100))):
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i: (lambda lz, iso: G.persona(lz, iso, x, y, t, ["insurgente", "campesino", "insurgente_lanza", "indigena", "honda", "mestizo"][i], dir=(1, 0.2), seed=7600 + i, h=42, accion="vitorea" if i % 2 == 0 and t > t_simp else None)))(x, y, i), fijo=False, clave=x + y + 3)
    for i, (x, y) in enumerate(((330, 100), (380, 170), (350, 240), (420, 120), (310, 200), (410, 230))):
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i: (lambda lz, iso: G.persona(lz, iso, x, y, t, ["realista", "dragon", "oficial", "granadero", "realista", "dragon"][i], dir=(-1, 0.2), seed=7700 + i, h=46, accion="vitorea" if t > t_paso + 1.0 and i % 2 == 0 else None)))(x, y, i), fijo=False, clave=x + y + 3)
    # los criollos ricos (de levita, con bolsas de dinero) cruzan del campamento insurgente al realista
    ric = ("noble", "dama", "regidor", "comerciante", "noble", "dama", "regidor", "noble")
    for i in range(10):
        ti = t_asus + 0.2 + 0.32 * i
        u = e_inout(prog(t, ti + 1.0, ti + 3.2 + 0.2 * i))
        y0, y1 = 120 + 110 * h01(121, i), 130 + 100 * h01(122, i)
        x, y = lerp(130 + 20 * h01(123, i), 330 + 20 * h01(124, i), u), lerp(y0, y1, u)
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i, u: (lambda lz, iso: G.persona(lz, iso, x, y, t, ric[i % 8], dir=(1, 0.1) if 0 < u < 1 else ((-1, 0.1) if u <= 0 else (1, 0.2)), vel=1.2 if 0 < u < 1 else 0.0, seed=7800 + i, h=46, accion=("carga" if 0 < u < 1 and i % 3 == 0 else ("vitorea" if u >= 1 and t > t_rey - 1.0 else None)), cara="miedo" if u <= 0 else ("alegre" if u >= 1 else None))))(x, y, i, u), fijo=False, clave=x + y + 6)
    m.dibujar(lz, iso)
    DC.polvo_luz(lz, t, n=18, seed=64, color=(255, 214, 170), alfa=0.3)
    k = U.pop(t, t_viol - 0.05) * U.salida(t, t_crio - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "la violencia los asusta", color=U.COL["rojo"], px=70, k=k, cola=None)
    k = U.pop(t, t_crio - 0.05) * U.salida(t, t_simp - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "criollos ricos", color=U.COL["morado"], px=82, k=k * U.repop(t, t_ric + 0.1), cola=None)
    k = U.pop(t, t_simp - 0.05) * U.salida(t, t_paso - 0.15, 0.2)
    if k > 0.01:
        qx, qy = iso.P(120, 180, 90)
        U.llamada(lz, float(qx), float(qy) - 40, "simpatizaban con la causa", color=U.COL["verde"], px=48, k=k * U.repop(t, t_caus + 0.1), cola="abajo")
    k = U.pop(t, t_paso - 0.05)
    if k > 0.01:
        qx, qy = iso.P(316, 140, 110)
        U.llamada(lz, float(qx), float(qy) - 20, "se pasan al bando del rey", color=U.COL["rojo"], px=56, k=k * U.repop(t, t_rey + 0.1), cola="abajo")


# ------------------------------------------------------------------------------------------------ 7. HACIA LA CAPITAL
RUTA_F = [(-101.26, 21.02), (-101.19, 20.20), (-101.19, 19.70), (-100.2, 19.45), (-99.66, 19.29), (-99.13, 19.43)]


def cam_f(t):
    return Klog(t, [(T_F, (-101.0, 20.6, 2.2)), (t_crec, (-100.4, 20.2, 1.7)), (t_cap, (-100.2, 20.1, 1.45)), (T1(E6), (-100.0, 19.9, 1.5))])


@shot(T_F, bg=lambda t: BASE(cam_f(t), t), post=[GRAD], ent=("zoom", 0.6))
def gt_capital(lz, t):
    cam = cam_f(t)
    I.luz()
    MD.montes(lz, cam, min_alt=2200)
    MD.pais(lz, cam, "Mexico", (255, 96, 70), alfa=0.12, borde=(255, 220, 90), ancho=4.0, t=t, latido=1.0)
    for j, (lug, tp, nm, dx, dy, lado) in enumerate((("guanajuato", "ciudad", "Guanajuato", 130, 4, "izq"), ((-101.19, 19.70), "ciudad", "Valladolid", -110, 4, "der"), ((-99.66, 19.29), "ciudad", "", 110, 4, "izq"))):
        MD.ciudad(lz, cam, lug, t, T_F + 0.1 * j, tam=1.3, tipo=tp, bando="ins" if j == 0 else "real", semilla=j + 41)
        if nm:
            MD.etiqueta(lz, cam, lug, nm, t, T_F + 0.1 * j + 0.1, px=22, dy=dy, dx=dx, lado=lado)
    MD.ciudad(lz, cam, "mexico", t, T_F + 0.4, tam=2.2, tipo="ciudad", bando="real", nombre="Ciudad de México", px=30, semilla=7)
    f = e_inout(prog(t, T_F + 0.2, T1(E6) - 0.3))
    MD.ruta(lz, cam, RUTA_F, color=(255, 214, 84), frac=f, t=t, ancho=8.0, flecha=True)
    ng = int(3 + 40 * smooth(prog(t, t_ejh, t_crec + 1.2)))
    for i in range(ng):
        u = max(0.0, min(0.999, f - 0.03 * (i % 20) - 0.02 * h01(131, i)))
        if u <= 0.01:
            continue
        x, y, v = MD.punto_ruta(cam, RUTA_F, u)
        ox, oy = 60 * (h01(132, i) - 0.5), 40 * (h01(133, i) - 0.5)
        MD.ejercito(lz, float(x) + ox, float(y) + oy, 12, bando="ins", t=t + i * 0.3, s=1.6, dir=1, semilla=i, bandera=(i == 0), polvo=(i % 4 == 0))
    k = U.pop(t, t_aun - 0.05) * U.salida(t, t_crec - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "aun así…", color=U.COL["azul"], px=84, k=k, cola=None)
    k = U.pop(t, t_crec - 0.05) * U.salida(t, t_avan - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "el ejército crece y crece", color=U.COL["naranja"], px=72, k=k * U.repop(t, t_crec + 0.5), cola=None)
    k = U.pop(t, t_avan - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "avanza hacia la capital", color=U.COL["rojo"], px=78, k=k * U.repop(t, t_cap + 0.1), cola=None)
    MD.brujula(lz, W - 110, H - 120, 1.0)


# ------------------------------------------------------------------------------------------------ sonido
snd(T_A + 0.2, "whoosh", 0.3, dur=1.0)
snd(t_gua, "pop", 0.4)
snd(T_A2, "whoosh", 0.3, dur=0.9)
snd(t_min, "pluck", 0.4)
snd(t_pla, "bling", 0.5)
snd(T_B, "pop", 0.3)
snd(t_enc, "gong", 0.4)
snd(t_alh, "pop", 0.4)
for _k in range(6):
    snd(T_C + 0.5 + 0.6 * _k, "tambor", 0.3)
snd(t_comb, "canonazo", 0.5)
snd(t_brut, "canonazo", 0.5)
snd(t_pip, "pop", 0.4)
snd(t_prend, "explosion", 0.6)
snd(T_D, "explosion", 0.5)
snd(t_mat, "gong", 0.5)
snd(t_saq, "monedas", 0.5)
snd(T_E, "whoosh", 0.3, dur=0.9)
snd(t_crio, "pop", 0.4)
snd(t_paso, "pluck", 0.5)
snd(T_F, "whoosh", 0.3, dur=0.9)
snd(t_crec, "tambor", 0.5)
snd(t_cap, "gong", 0.5)
