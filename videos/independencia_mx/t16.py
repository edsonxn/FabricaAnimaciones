# -*- coding: utf-8 -*-
"""Escena 16 · La consumación (9:15-9:45): la noticia corre como pólvora, el tratado de Córdoba, la entrada del Ejército Trigarante a la capital el 27 de septiembre de 1821, el Acta de Independencia y los once años de guerra."""
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
import mundos_d as md
import mundos_n as mn

E16 = "consumacion"
MP = KM.MAPA
GRAD = lambda img, t: U.gradacion(img)
BASE = lambda cam, t: MP.base(cam, t, exag=13.0, rios_umbral=0.7)
PURP = lambda t: bg_grad((54, 30, 112), (150, 70, 130), mid=(100, 46, 130), ym=0.5)
PLZ = md.PlazaMayor()
TRICOLOR = [((250, 250, 246), 1 / 3), ((70, 170, 110), 1 / 3), ((214, 56, 66), 1 / 3)]

# ------------------------------------------------------------------ anclas
t_not, t_corr, t_polv, t_ciu, t_cam, t_band, t_disp = [T(E16, w, frase=0) for w in ("noticia", "corrio", "polvora", "ciudad", "cambiaban", "bando", "disparar")]
t_nuevo, t_repr, t_rey, t_rec, t_esp, t_nada, t_firmo, t_trat, t_itu, t_cord = [T(E16, w, frase=1) for w in ("nuevo", "representante", "rey", "recien", "espana", "nada", "firmo", "tratado", "iturbide", "cordoba")]
t_27, t_sep, t_ejer, t_entro, t_mex, t_itu2, t_frente = [T(E16, w, frase=2) for w in ("veintisiete", "septiembre", "ejercito", "entro", "mexico", "iturbide", "frente")]
t_dia, t_firm, t_acta, t_indep, t_mexico, t_libre = [T(E16, w, frase=3) for w in ("dia", "firmo", "acta", "independencia", "mexico", "libre")]
t_once, t_anos, t_guerra, t_pais, t_dev, t_mom = [T(E16, w, frase=4) for w in ("once", "anos", "guerra", "pais", "devastado", "momento")]
T_A, T_B1, T_B2, T_C, T_D, T_E = T0(E16), t_nuevo - 0.2, t_firmo - 0.3, t_27 - 0.15, t_dia - 0.15, t_once - 0.1


# ------------------------------------------------------------------------------------------------ 1. LA NOTICIA CORRE COMO PÓLVORA
CIUDADES_F = (("puebla", "ciudad", "Puebla"), ("veracruz", "puerto", "Veracruz"), ("oaxaca", "ciudad", "Oaxaca"), ("queretaro", "ciudad", "Querétaro"), ("guanajuato", "ciudad", "Guanajuato"), ("valladolid", "ciudad", "Valladolid"), ("guadalajara", "ciudad", "Guadalajara"), ("san_luis", "ciudad", "San Luis Potosí"), ("zacatecas", "ciudad", "Zacatecas"))


def cam_a(t):
    return Klog(t, [(T_A, (-99.0, 19.6, 1.9)), (T_B1, (-100.2, 21.0, 1.35))])


@shot(T_A, bg=lambda t: BASE(cam_a(t), t), post=[GRAD], ent=("fundido", 0.5))
def co_polvora(lz, t):
    cam = cam_a(t)
    I.luz()
    MD.montes(lz, cam, min_alt=2200)
    MD.pais(lz, cam, "Mexico", (255, 96, 70), alfa=0.08, borde=(255, 220, 90), ancho=4.0, t=t, latido=0.0)
    MD.ciudad(lz, cam, "iguala", t, T_A, tam=1.5, tipo="pueblo", bando=(70, 190, 110), semilla=3)
    MD.ciudad(lz, cam, "mexico", t, T_A + 0.1, tam=1.6, tipo="ciudad", bando="real", semilla=9)
    for k in range(5):                                          # ondas de la noticia desde Iguala, una tras otra
        MD.onda(lz, cam, "iguala", t, t_corr + 0.5 * k, dur=3.0, r_deg=9.0, color=(255, 236, 170), n=1, ancho=7.0)
    for i, (lug, tp, nm) in enumerate(CIUDADES_F):
        t_flip = t_ciu + 0.1 + 0.36 * i
        MD.ciudad(lz, cam, lug, t, T_A + 0.2 + 0.05 * i, tam=1.25, tipo=tp, bando="real", semilla=i + 141)
        if t >= t_flip:
            k = U.pop(t, t_flip)
            MD.ciudad(lz, cam, lug, t, t_flip, tam=1.25, tipo=tp, bando=(70, 190, 110), semilla=i + 141)
            sx, sy = MP.proy(cam, *(MD.CIUDADES[lug] if isinstance(lug, str) else lug))
            MD.bandera_mapa(lz, float(sx) + 30, float(sy) - 60, (70, 190, 110), t + i, 2.3 * k, franjas=TRICOLOR)
            lz.trazo(circulo(float(sx), float(sy), 20 + 160 * min(1.0, (t - t_flip) * 1.4), 28), (255, 255, 255), 5, cerrado=True, afinar=False, temblor=0.0, capa=2) if (t - t_flip) < 0.8 else None
            for j in range(5):
                U.chispa4(lz, float(sx) + 90 * math.cos(j * 1.25 + t * 3) * (1 - 0.5 * k), float(sy) - 20 + 60 * math.sin(j * 1.25 + t * 3) * (1 - 0.5 * k), 10 + 5 * (j % 3), alfa=max(0.0, 1.0 - (t - t_flip) * 0.6))
        MD.etiqueta(lz, cam, lug, nm, t, T_A + 0.3 + 0.05 * i, px=20, dy=4, dx=100, lado="izq")
    k = U.pop(t, t_not - 0.05) * U.salida(t, t_ciu - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "la noticia corre como pólvora", color=U.COL["rojo"], px=76, k=k * U.repop(t, t_polv + 0.1), cola=None)
    k = U.pop(t, t_ciu - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "ciudad tras ciudad, cambian de bando", color=U.COL["verde"], px=68, k=k * U.repop(t, t_band + 0.1), cola=None)
        U.llamada(lz, W / 2, 250, "casi sin disparar", color=U.COL["naranja"], px=56, k=U.pop(t, t_disp - 0.5), cola=None)
    MD.brujula(lz, W - 110, H - 120, 1.0)


# ------------------------------------------------------------------------------------------------ 2. EL NUEVO REPRESENTANTE DEL REY LLEGA A VERACRUZ
def cam_b1(t):
    return Klog(t, [(T_B1, (-96.8, 19.2, 2.4)), (T_B2, (-96.9, 19.2, 2.8))])


@shot(T_B1, bg=lambda t: BASE(cam_b1(t), t), post=[GRAD], ent=("zoom", 0.5))
def co_odonoju(lz, t):
    cam = cam_b1(t)
    I.luz()
    MD.montes(lz, cam, min_alt=2200)
    MD.mar_vivo(lz, cam, t, seed=21)
    MD.pais(lz, cam, "Mexico", (255, 96, 70), alfa=0.08, borde=(255, 220, 90), ancho=4.0, t=t, latido=0.0)
    MD.ciudad(lz, cam, "veracruz", t, T_B1, tam=2.0, tipo="puerto", bando="real", nombre="Veracruz", px=26, semilla=3)
    MD.ciudad(lz, cam, "cordoba", t, t_firmo - 0.5, tam=1.6, tipo="pueblo", bando=(70, 190, 110), nombre="Córdoba", px=24, semilla=5)
    sx, sy = MP.proy(cam, -96.13, 19.18)
    bx = float(sx) + 700 * (1 - e_out(prog(t, T_B1, t_esp + 0.8)))
    MD.barco_plano(lz, bx, float(sy) - 10, 1.9, t, dir=-1)
    kq = U.pop(t, t_rec - 0.1)
    if kq > 0.01:
        MD.medallon(lz, 1620, 450, 150, "odonoju", t, emocion="serio", k=kq, seed=6)
        U.llamada(lz, 1620, 630, "Juan O'Donojú", color=U.COL["rojo"], px=40, k=kq, cola="arriba")
    k = U.pop(t, t_nuevo - 0.05) * U.salida(t, t_rec - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "el nuevo representante del rey", color=U.COL["rojo"], px=70, k=k * U.repop(t, t_repr + 0.1), cola=None)
    k = U.pop(t, t_rec - 0.05) * U.salida(t, t_nada - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "recién llegado de España", color=U.COL["naranja"], px=74, k=k * U.repop(t, t_esp + 0.1), cola=None)
    k = U.pop(t, t_nada - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "ya no había nada que hacer", color=U.COL["morado"], px=72, k=k * U.repop(t, t_nada + 0.2), cola=None)
    MD.brujula(lz, W - 110, H - 120, 1.0)


@shot(T_B2, bg=PURP, post=[GRAD], ent=("fundido", 0.4))
def co_cordoba(lz, t):
    U.bokeh(lz, t, seed=121, n=14, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.24)
    U.haces_luz(lz, W / 2, 520, t, n=8, largo=1300, color=(255, 200, 240), alfa=0.10, ancho=0.09)
    U.chispas(lz, t, n=18, seed=122, tam=(5, 12))
    k1 = U.pop(t, T_B2 + 0.05, 1.2)
    k2 = U.pop(t, T_B2 + 0.25, 1.2)
    RT.retrato(lz, 320, 1020, 200 * (0.94 + 0.06 * k1), "odonoju", t, emocion="serio", mirar=0.5, seed=6, alfa=min(1.0, k1))
    RT.retrato(lz, 1600, 1020, 200 * (0.94 + 0.06 * k2), "iturbide", t, emocion="serio", mirar=-0.5, seed=7, alfa=min(1.0, k2))
    U.pergamino_grande(lz, W / 2, 520, 720, 520, t, t_firmo - 0.1, lineas=("Se reconoce la independencia", "del Imperio Mexicano", "24 de agosto de 1821"), titulo="TRATADOS DE CÓRDOBA", sello=True, rot=0.0)
    kp = U.pop(t, t_firmo + 0.1)
    if kp > 0.01:                                            # la pluma firma y aparecen los sellos
        px_, py_ = W / 2 + 160 - 60 * math.sin(t * 7), 700
        lz.trazo(np.array([[px_, py_], [px_ + 90, py_ - 150]]), (250, 250, 250), 10, afinar=False, temblor=0.0, capa=2)
        lz.relleno(np.array([[px_ - 8, py_ + 6], [px_ + 4, py_ - 6], [px_ + 12, py_ + 10]]), (60, 50, 70), capa=2)
    U.llamada(lz, 320, 270, "Juan O'Donojú", color=U.COL["rojo"], px=44, k=k1, cola=None)
    U.llamada(lz, 1600, 270, "Agustín de Iturbide", color=U.COL["verde"], px=44, k=k2, cola=None)
    k = U.pop(t, t_firmo - 0.05) * U.salida(t, T_C - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "firma un tratado con Iturbide en Córdoba", color=U.COL["naranja"], px=62, k=k * U.repop(t, t_cord + 0.1), cola=None)


# ------------------------------------------------------------------------------------------------ 3. EL EJÉRCITO ENTRA A LA CAPITAL (27 DE SEPTIEMBRE DE 1821)
def cam_c(t):
    return K(t, [(T_C, (360, 290, 30, 2.1)), (t_ejer, (320, 285, 34, 2.6)), (t_itu2, (290, 285, 34, 2.9)), (T_D, (270, 285, 34, 2.6))])


@shot(T_C, bg=lambda t: bg_grad((120, 190, 245), (254, 232, 200), mid=(200, 220, 240), ym=0.5), post=[GRAD], ent=("fundido", 0.5))
def co_entrada(lz, t):
    cx, cy, cz, zm = cam_c(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz(mul=(1.05, 1.0, 0.95), mix=(255, 214, 150), k=0.07)
    PLZ.suelo(lz, iso, t)
    m = PLZ.objetos(t)
    # el ejército trigarante entra por la calle del este: Iturbide a caballo al frente, columnas mixtas y banderas trigarantes
    u = e_inout(prog(t, T_C + 0.3, t_frente + 0.5))
    xi = lerp(700, 300, u)
    m.add(xi - 8, 276, xi + 8, 296, 50, lambda lz, iso: G.caballo(lz, iso, xi, 286, t, dir=-1, seed=11, color=(244, 240, 232), vel=1.0 if 0 < u < 1 else 0.0, jinete="oficial", s=1.4), fijo=False, clave=xi + 286 + 10)
    tipos = ("oficial", "insurgente", "realista", "insurgente_lanza", "dragon", "campesino")
    for i in range(60):
        r_, c_ = i // 5, i % 5
        x = xi + 26 + 15 * r_
        y = 270 + 10 * c_
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i: (lambda lz, iso: G.persona(lz, iso, x, y, t, tipos[i % 6], dir=(-1, 0), vel=1.4 if 0 < u < 1 else 0.0, seed=11000 + i, h=44, accion="vitorea" if u >= 1 else None, cara="alegre")))(x, y, i), fijo=False, clave=x + y + 3)
    for j in range(4):
        bx = xi + 40 + 70 * j
        m.add(bx - 4, 262, bx + 4, 270, 150, (lambda bx: (lambda lz, iso: O2.bandera_trigarante(lz, iso, bx, 266, h=90, t=t, w=42, alto=26)))(bx), fijo=False, clave=bx + 266 + 6)
    # el pueblo vitorea en los portales y la plaza
    for i in range(24):
        x, y = 140 + 280 * h01(301, i), 150 + 90 * h01(302, i) + 240 * (i % 2)
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i: (lambda lz, iso: G.persona(lz, iso, x, y, t, ("campesino", "campesina", "mestizo", "indigena", "indigena_f", "dama", "comerciante", "nino")[i % 8], dir=(1, 0.3), seed=11100 + i, h=40 if i % 8 != 7 else 28, accion="vitorea", cara="alegre")))(x, y, i), fijo=False, clave=x + y + 3)
    m.dibujar(lz, iso)
    mn.guirnaldas(lz, iso, t, k=prog(t, T_C, T_C + 2.0), postes=[(100, 140), (420, 140), (420, 430), (100, 430)], z=64)
    DC.aves(lz, t, n=10, seed=131, y0=60, y1=260)
    for i in range(40):                                            # confeti tricolor
        uu = ((t * 0.45 + h01(311, i)) % 1.0)
        lz.relleno(circulo(100 + 1700 * h01(312, i) + 30 * math.sin(t * 2 + i), 60 + 1000 * uu, 4 + 3 * h01(313, i), 6), [(250, 250, 246), (70, 190, 110), (226, 70, 80)][i % 3], alfa=0.9, capa=2)
    k = U.pop(t, t_27 - 0.05) * U.salida(t, t_ejer - 0.2, 0.2)
    if k > 0.01:
        P.rotulo(lz, W / 2, 180, "27 de septiembre de 1821", px=int(110 * (0.94 + 0.06 * k)), k=k, color=(255, 255, 255))
    k = U.pop(t, t_ejer - 0.05) * U.salida(t, t_itu2 - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "el ejército entra a la Ciudad de México", color=U.COL["verde"], px=68, k=k * U.repop(t, t_entro + 0.1), cola=None)
    k = U.pop(t, t_itu2 - 0.05)
    if k > 0.01:
        qx, qy = iso.P(xi, 286, 90)
        U.llamada(lz, float(qx), float(qy) - 10, "Iturbide al frente", color=U.COL["naranja"], px=54, k=k * U.repop(t, t_frente + 0.1), cola="abajo")


# ------------------------------------------------------------------------------------------------ 4. EL ACTA DE INDEPENDENCIA: MÉXICO ERA LIBRE
def _cohete(lz, x, y, u, col):
    if u <= 0:
        return
    for i in range(20):
        a = i * 0.314
        r = 260 * smooth(u)
        lz.relleno(circulo(x + math.cos(a) * r, y + math.sin(a) * r + 120 * u * u, 7 * (1 - u * 0.7), 8), col, alfa=max(0.0, 1 - u), capa=2)
        lz.relleno(circulo(x + math.cos(a) * r * 0.7, y + math.sin(a) * r * 0.7 + 90 * u * u, 4 * (1 - u * 0.7), 6), (255, 255, 255), alfa=max(0.0, 1 - u), capa=2)
    lz.halo(x, y, 300 * u, col, alfa=0.25 * (1 - u), capa=0)


@shot(T_D, bg=lambda t: bg_grad((40, 24, 100), (160, 70, 130), mid=(90, 40, 120), ym=0.5), post=[GRAD], ent=("destello", 0.4))
def co_acta(lz, t):
    U.bokeh(lz, t, seed=123, n=14, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.26)
    U.haces_luz(lz, W / 2, 560, t, n=10, largo=1400, color=(255, 214, 240), alfa=0.14, ancho=0.08)
    U.pergamino_grande(lz, W / 2, 560, 900, 640, t, T_D + 0.1, lineas=("La Nación Mexicana,", "que por trescientos años", "ni ha tenido voluntad propia,", "recobra hoy su libertad", "28 de septiembre de 1821"), titulo="ACTA DE INDEPENDENCIA", sello=True, rot=-0.02)
    kb = U.pop(t, t_libre - 0.2)
    if kb > 0.01:
        for j, (x, y, col, dt) in enumerate(((330, 380, (255, 214, 90), 0.0), (1590, 360, (110, 220, 150), 0.25), (960, 220, (255, 120, 140), 0.5), (520, 760, (120, 180, 255), 0.7), (1400, 780, (255, 214, 90), 0.9))):
            _cohete(lz, x, y, prog(t, t_libre - 0.1 + dt, t_libre + 1.6 + dt), col)
        U.chispas(lz, t, n=30, seed=124, tam=(6, 15))
        # bandera trigarante sube a un asta a la derecha
        h = 460 * e_out(prog(t, t_libre - 0.1, t_libre + 1.0))
        lz.trazo(np.array([[1700, 1000], [1700, 1000 - 460]]), (130, 96, 70), 8, afinar=False, temblor=0.0, capa=2)
        pts = [(1700 + k * 11, 1000 - h + 6 * math.sin(t * 5 - k * 0.5) + 0.3 * k) for k in range(0, 21)]
        pts += [(1700 + k * 11, 1000 - h + 130 + 6 * math.sin(t * 5 - k * 0.5) + 0.3 * k) for k in range(20, -1, -1)]
        lz.relleno(np.array(pts), (70, 170, 110), capa=2)
    k = U.pop(t, t_dia - 0.05) * U.salida(t, t_mexico - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "al día siguiente se firma el Acta de Independencia", color=U.COL["naranja"], px=60, k=k * U.repop(t, t_acta + 0.1), cola=None)
    k = U.pop(t, t_mexico - 0.05)
    if k > 0.01:
        P.rotulo(lz, W / 2, 140, "¡MÉXICO ERA LIBRE!", px=int(150 * (0.94 + 0.06 * k)), k=k * U.repop(t, t_libre + 0.1), color=(255, 255, 255))


# ------------------------------------------------------------------------------------------------ 5. ONCE AÑOS DE GUERRA PARA LLEGAR AQUÍ
HITOS = ((1810, "el Grito", 0.0), (1811, "Calderón y la captura", 0.14), (1812, "Cuautla", 0.26), (1813, "el Congreso", 0.38), (1815, "cae Morelos", 0.55), (1820, "el giro", 0.82), (1821, "independencia", 1.0))


@shot(T_E, bg=lambda t: bg_grad((54, 30, 112), (150, 70, 130), mid=(100, 46, 130), ym=0.5), post=[lambda img, t: U.gradacion(img, luces=(1.0, 0.98, 1.0), sombras=(0.94, 0.95, 1.04), saturacion=1.0 - 0.18 * smooth(prog(t, t_dev - 0.3, t_dev + 0.8)))], ent=("fundido", 0.5))
def co_once(lz, t):
    U.bokeh(lz, t, seed=125, n=12, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.20)
    x0, x1, y = 200, 1720, 640
    lz.relleno(rect_red(x0 - 20, y - 10, x1 - x0 + 40, 20, 10), (255, 255, 255), alfa=0.25, capa=2)
    u = prog(t, T_E + 0.1, t_mom + 0.2)
    lz.relleno(rect_red(x0 - 20, y - 10, (x1 - x0 + 40) * u, 20, 10), (255, 214, 72), capa=2)
    for i, (anio, lab, f) in enumerate(HITOS):
        x = x0 + (x1 - x0) * f
        k = U.pop(t, T_E + 0.1 + (t_mom + 0.2 - T_E - 0.1) * f) if f < 1 else U.pop(t, t_mom - 0.1)
        if k > 0.01:
            lz.relleno(circulo(x, y, 30 * k, 20), (255, 214, 72) if i < 6 else (110, 220, 150), capa=2)
            lz.relleno(circulo(x, y, 18 * k, 16), (60, 40, 90), capa=2)
            up = (i % 2 == 0)
            P.rotulo(lz, x, y + (-110 if up else 110), str(anio), px=int(56 * k), k=1.0, color=(255, 255, 255))
            U.llamada(lz, x, y + (-190 if up else 190), lab, color=U.COL["morado"] if i < 6 else U.COL["verde"], px=32, k=k, cola=None)
    k = U.pop(t, t_once - 0.05)
    if k > 0.01:
        P.rotulo(lz, W / 2, 190, "11 años", px=int(190 * (0.94 + 0.06 * k)), k=k * U.repop(t, t_anos + 0.1), color=(255, 214, 72))
    k = U.pop(t, t_pais - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 960, "…y un país devastado", color=U.COL["rojo"], px=70, k=k * U.repop(t, t_dev + 0.1), cola=None)


# ------------------------------------------------------------------------------------------------ sonido
snd(T_A + 0.2, "whoosh", 0.3, dur=1.0)
snd(t_corr, "explosion", 0.4)
for _i in range(len(CIUDADES_F)):
    snd(t_ciu + 0.1 + 0.36 * _i, "pop", 0.3)
snd(T_B1, "whoosh", 0.3, dur=0.9)
snd(t_nada, "pluck", 0.4)
snd(T_B2, "bling", 0.4)
snd(t_firmo + 0.2, "bonk", 0.4)
snd(T_C, "tambor", 0.4)
for _k in range(8):
    snd(T_C + 0.5 * _k, "tambor", 0.25)
snd(t_entro, "campana", 0.5)
snd(t_itu2, "bling", 0.5)
snd(T_D, "pop", 0.3)
snd(t_acta, "gong", 0.5)
snd(t_libre, "explosion", 0.6)
snd(t_libre + 0.3, "bling", 0.6)
snd(T_E, "pluck", 0.4)
snd(t_mom, "gong", 0.5)
