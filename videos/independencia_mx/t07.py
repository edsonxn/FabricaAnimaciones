# -*- coding: utf-8 -*-
"""Escena 7 · La capital a la vista (3:49-4:26): el monte de las Cruces, el valle de México desde la cumbre, la orden de retirarse, las dudas de Hidalgo, el ejército realista que se reorganiza, Aculco y la ruptura entre Allende e Hidalgo."""
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
import mundos_h as mh

E7 = "capital"
MP = KM.MAPA
GRAD = lambda img, t: U.gradacion(img)
BASE = lambda cam, t: MP.base(cam, t, exag=13.0, rios_umbral=0.7)
MON = mh.MonteCruces()
CAMPO = mh.CampoRealista()

# ------------------------------------------------------------------ anclas
t_oct, t_monte, t_cruc, t_puer, t_cdmx, t_derr, t_vir = [T(E7, w, frase=0) for w in ("octubre", "monte", "cruces", "puertas", "ciudad", "derrotaron", "virrey")]
t_cap1, t_vista, t_indef, t_ocho, t_mil, t_hom = [T(E7, w, frase=1) for w in ("capital", "vista", "indefensa", "ochenta", "mil", "hombres")]
t_ent, t_hid, t_algo, t_div, t_hist, t_orden, t_ret = [T(E7, w, frase=2) for w in ("entonces", "hidalgo", "algo", "divide", "historiadores", "ordeno", "retirarse")]
t_quiz, t_temia, t_mat, t_muni, t_nadie, t_sabe = [T(E7, w, frase=3) for w in ("quizas", "temia", "matanza", "municiones", "nadie", "sabe")]
t_quiz2 = T(E7, "quizas", frase=3, n=1)
t_dec, t_camb, t_hist2, t_ejr, t_real, t_reorg, t_pers = [T(E7, w, frase=4) for w in ("decision", "cambio", "historia", "ejercito", "realista", "reorganizo", "perseguirlos")]
t_ins, t_derrot, t_acu, t_all, t_hid2, t_disc, t_sep = [T(E7, w, frase=5) for w in ("insurgentes", "derrotados", "aculco", "allende", "hidalgo", "discutieron", "separaron")]
T_A, T_A2, T_B, T_C, T_D, T_E, T_F, T_G, T_H = T0(E7), t_monte - 0.2, t_cap1 - 0.2, t_ent - 0.3, t_quiz - 0.3, t_dec - 0.3, t_ins - 0.2, t_all - 0.2, t_sep - 0.3


def _pos(path, s):
    p = np.asarray(path, float)
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(p, axis=0).T))]
    s = float(np.clip(s, 0, d[-1] - 1e-3))
    i = int(np.clip(np.searchsorted(d, s, side="right") - 1, 0, len(p) - 2))
    f = (s - d[i]) / (d[i + 1] - d[i])
    q = p[i] + (p[i + 1] - p[i]) * f
    dr = (p[i + 1] - p[i]) / np.hypot(*(p[i + 1] - p[i]))
    return float(q[0]), float(q[1]), dr


# ------------------------------------------------------------------------------------------------ 1. MONTE DE LAS CRUCES (mapa)
RUTA_M = [(-99.66, 19.29), (-99.50, 19.28), (-99.36, 19.30), (-99.25, 19.36)]


def cam_m(t):
    return Klog(t, [(T_A, (-99.75, 19.42, 2.2)), (t_oct, (-99.48, 19.33, 3.8)), (T_A2, (-99.42, 19.32, 4.4))])


@shot(T_A, bg=lambda t: BASE(cam_m(t), t), post=[GRAD], ent=("fundido", 0.5))
def cr_mapa(lz, t):
    cam = cam_m(t)
    I.luz()
    MD.montes(lz, cam, min_alt=2200)
    MD.pais(lz, cam, "Mexico", (255, 96, 70), alfa=0.12, borde=(255, 220, 90), ancho=4.0, t=t, latido=1.0)
    MD.ciudad(lz, cam, "mexico", t, T_A + 0.1, tam=1.6, tipo="ciudad", bando="real", semilla=3)
    MD.etiqueta(lz, cam, "mexico", "Ciudad de México", t, T_A + 0.3, px=26, dy=-110, dx=0, lado="abajo")
    MD.ciudad(lz, cam, (-99.66, 19.29), t, T_A + 0.2, tam=1.1, tipo="ciudad", bando="real", semilla=5)
    MD.etiqueta(lz, cam, (-99.66, 19.29), "Toluca", t, T_A + 0.3, px=22, dy=60, dx=0, lado="arriba")
    f = e_inout(prog(t, T_A + 0.3, t_monte + 0.3))
    MD.ruta(lz, cam, RUTA_M, color=(255, 214, 84), frac=f, t=t, ancho=7.0, flecha=False)
    for i in range(7):
        u = max(0.0, min(0.999, f - 0.06 * i))
        if u > 0.01:
            x, y, v = MD.punto_ruta(cam, RUTA_M, u)
            MD.ejercito(lz, float(x), float(y), 12, bando="ins", t=t + i * 0.2, s=1.5, dir=1, semilla=i, bandera=(i == 0), polvo=(i % 2 == 0))
    MD.insignia_batalla(lz, cam, "monte_cruces", t, t_monte - 0.1, año=1810, s=1.5)
    k = U.pop(t, T_A + 0.2) * U.salida(t, t_monte - 0.15, 0.2)
    if k > 0.01:
        U.fecha_lugar(lz, t, T_A + 0.2, t_monte, "Valle de México", "Octubre de 1810", y=70)
    k = U.pop(t, t_monte - 0.05)
    if k > 0.01:
        sx, sy = MP.proy(cam, -99.35, 19.30)
        U.llamada(lz, float(sx), float(sy) - 150, "Monte de las Cruces", color=U.COL["rojo"], px=60, k=k * U.repop(t, t_cruc + 0.1), cola="abajo")
    MD.brujula(lz, W - 110, H - 120, 1.0)


# ------------------------------------------------------------------------------------------------ 2. LA BATALLA EN EL MONTE
def cam_b1(t):
    return K(t, [(T_A2, (150, 260, 34, 2.4)), (t_puer, (240, 200, 40, 2.8)), (t_derr, (290, 160, 44, 3.0)), (T_B, (330, 130, 44, 3.0))])


def _canon_t(t, ph):
    return ((t * 1.0 + ph) % 1.3)


@shot(T_A2, bg=lambda t: bg_grad((120, 170, 230), (254, 226, 196), mid=(196, 200, 232), ym=0.5), post=[GRAD], ent=("zoom", 0.5))
def cr_batalla(lz, t):
    cx, cy, cz, zm = cam_b1(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz(mul=(1.02, 0.98, 0.94), mix=(255, 214, 160), k=0.05)
    MON.suelo(lz, iso, t)
    m = MON.objetos(t)
    # los cañones del virrey disparan; la infantería realista se pliega y huye cuando son derrotados
    for i, (x, y) in enumerate(((330, 110), (352, 128), (308, 94))):
        td = _canon_t(t, 0.4 * i) if t < t_derr + 0.5 else -1.0
        B.canon(m, x, y, dir=-1, t_fn=lambda: t, disparo=td, escala=1.1)
    huye = e_inout(prog(t, t_derr, t_derr + 2.2))
    for i in range(34):
        r_, c_ = i // 12, i % 12
        x0, y0 = 360 + 10 * r_ + 14 * (c_ % 3), 70 + 10 * c_ + 4 * r_
        x, y = lerp(x0, 560 + 20 * h01(141, i), huye), lerp(y0, 10 - 50 * h01(142, i), huye)
        tp = ("realista", "granadero", "dragon", "oficial")[i % 4] if i % 7 else "granadero"
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i, tp, hu: (lambda lz, iso: G.persona(lz, iso, x, y, t, tp, dir=(-1, 0.5) if hu <= 0 else (1, -0.5), vel=1.8 if 0 < hu < 1 else (0.0 if hu <= 0 else 0.0), seed=8000 + i, h=44, cara="miedo" if hu > 0 else "enojo", accion="pelea" if (hu <= 0 and i % 2 == 0 and t > T_A2 + 1.0) else None)))(x, y, i, tp, huye), fijo=False, clave=x + y + 4)
    if huye < 0.7:
        m.add(344, 66, 354, 76, 120, lambda lz, iso: O2.faro_bandera(lz, iso, 350, 74, color=(206, 56, 70), t=t, h=80), fijo=False, clave=424)
    # los insurgentes cargan monte arriba por el camino
    tipos = ("insurgente", "honda", "campesino", "minero", "indigena", "insurgente_lanza", "mestizo", "indigena_f")
    for i in range(96):
        s0 = -420 + 540 * h01(143, i)
        s = s0 + (t - T_A2) * 70.0
        s = max(-40.0, min(s, 520 + 120 * h01(144, i)))
        x, y, d = _pos(MON.CAMINO, max(0.0, s))
        ox, oy = 26 * (h01(145, i) - 0.5), 26 * (h01(146, i) - 0.5)
        mov = 0.0 < s < 500
        m.add(x + ox - 4, y + oy - 4, x + ox + 4, y + oy + 4, 40, (lambda x, y, i, mov, d: (lambda lz, iso: G.persona(lz, iso, x, y, t, tipos[i % 8], dir=(d[0], d[1]), vel=1.8 if mov else 0.0, seed=8100 + i, h=42, accion="vitorea" if (not mov and t > t_derr) else ("pelea" if (not mov and i % 3 == 0) else None), cara="enojo")))(x + ox, y + oy, i, mov, d), fijo=False, clave=x + y + ox + oy + 4)
    m.dibujar(lz, iso)
    # fogonazos y humo de los cañones y de los fusiles
    for i, (x, y) in enumerate(((330, 110), (352, 128), (308, 94))):
        td = _canon_t(t, 0.4 * i)
        if td < 0.25 and t < t_derr + 0.5:
            qx, qy = iso.P(x - 12, y + 6, 18)
            U.chispa4(lz, float(qx), float(qy), 26 * (1 - td * 3), color=(255, 226, 140), alfa=0.95)
            lz.halo(float(qx), float(qy), 90 * iso.z / 3.0, (255, 190, 90), alfa=0.35, capa=2)
        O.humo(lz, iso, x - 14, y + 6, 24, t + i, n=4, s=1.4, color=(214, 210, 222), alfa=0.6, seed=i) if t < t_derr + 1.5 else None
    k = U.pop(t, T_A2 + 0.2) * U.salida(t, t_puer - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "Monte de las Cruces", color=U.COL["rojo"], px=80, k=k, cola=None)
    k = U.pop(t, t_puer - 0.05) * U.salida(t, t_derr - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "a las puertas de la capital", color=U.COL["naranja"], px=68, k=k * U.repop(t, t_cdmx + 0.1), cola=None)
    k = U.pop(t, t_derr - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "¡derrotan al ejército del virrey!", color=U.COL["verde"], px=72, k=k * U.repop(t, t_vir + 0.1), cola=None)


# ------------------------------------------------------------------------------------------------ 3. LA CAPITAL A LA VISTA
@shot(T_B, bg=lambda t: bg_grad((90, 150, 230), (252, 226, 200), mid=(190, 200, 240), ym=0.62), post=[GRAD], ent=("fundido", 0.5))
def cr_vista(lz, t):
    dx = (t - T_B) * 12.0
    mh.vista_capital(lz, t, dx=-dx)
    kk = e_inout(prog(t, t_ocho - 0.2, t_hom + 0.4))
    mh.multitud_espalda(lz, t, n=420, y0=770.0, y1=1110.0, seed=7, alzar=kk, banderas=3, escala=1.3)
    for i in range(3):
        U.chispa4(lz, 300 + 600 * h01(151, i), 200 + 160 * h01(152, i), 10 + 6 * i, alfa=0.7)
    k = U.pop(t, t_cap1 - 0.05) * U.salida(t, t_indef - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "la capital a la vista", color=U.COL["azul"], px=84, k=k * U.repop(t, t_vista + 0.1), cola=None)
    k = U.pop(t, t_indef - 0.05) * U.salida(t, t_ocho - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, 780, 560, "casi indefensa", color=U.COL["rojo"], px=64, k=k * U.repop(t, t_indef + 0.3), cola="abajo")
    k = U.pop(t, t_ocho - 0.1)
    if k > 0.01:
        v = 80000 * smooth(prog(t, t_ocho - 0.1, t_hom + 0.2))
        U.contador(lz, W / 2, 170, v, px=150, color=(255, 255, 255), k=k)
        U.llamada(lz, W / 2, 290, "hombres", color=U.COL["naranja"], px=64, k=k * U.repop(t, t_hom + 0.1), cola=None)


# ------------------------------------------------------------------------------------------------ 4. LA ORDEN DE RETIRARSE (mapa)
RUTA_AV = [(-99.66, 19.29), (-99.46, 19.29), (-99.30, 19.33), (-99.20, 19.40)]
RUTA_RE = [(-99.20, 19.40), (-99.46, 19.29), (-99.82, 19.34), (-100.0, 19.45)]


def _flecha(lz, a, b, ancho, color, frac=1.0, alfa=1.0):
    """Flecha gruesa de mapa de guerra (cuerpo + punta) de a a b, dibujada hasta `frac` del recorrido (coordenadas de pantalla)."""
    d = b - a
    L = float(np.hypot(*d))
    if L < 1 or frac < 0.01:
        return
    u = d / L
    n = np.array([-u[1], u[0]])
    f = min(1.0, frac)
    p1 = a + d * f
    cab = min(ancho * 1.5, L * f)
    base = p1 - u * cab
    w = ancho / 2
    pts = np.array([a + n * w * 0.55, base + n * w * 0.55, base + n * w * 1.5, p1, base - n * w * 1.5, base - n * w * 0.55, a - n * w * 0.55])
    lz.relleno(pts + np.array([6.0, 8.0]), (20, 10, 50), alfa=0.25 * alfa, capa=2)
    lz.relleno(pts, color, alfa=alfa, capa=2)
    lz.relleno(np.array([a + n * w * 0.2, base + n * w * 0.2, base + n * w * 0.55, a + n * w * 0.55]), (255, 255, 255), alfa=0.25 * alfa, capa=2)


def cam_c(t):
    return Klog(t, [(T_C, (-99.55, 19.36, 3.0)), (t_orden, (-99.55, 19.36, 3.0)), (T_D, (-99.55, 19.37, 3.0))])


@shot(T_C, bg=lambda t: BASE(cam_c(t), t), post=[GRAD], ent=("zoom", 0.5))
def cr_retirada(lz, t):
    cam = cam_c(t)
    I.luz()
    MD.montes(lz, cam, min_alt=2200)
    MD.pais(lz, cam, "Mexico", (255, 96, 70), alfa=0.12, borde=(255, 220, 90), ancho=4.0, t=t, latido=1.0)
    MD.ciudad(lz, cam, "mexico", t, T_C, tam=1.7, tipo="ciudad", bando="real", nombre="Ciudad de México", px=26, semilla=3)
    MD.ciudad(lz, cam, (-99.66, 19.29), t, T_C + 0.1, tam=1.1, tipo="ciudad", bando="real", semilla=5)
    MD.etiqueta(lz, cam, (-99.66, 19.29), "Toluca", t, T_C + 0.2, px=22, dy=60, dx=0, lado="arriba")
    av = e_inout(prog(t, T_C, t_algo + 0.6))
    re_ = e_inout(prog(t, t_orden, t_ret + 1.4))
    pm = np.array([float(v) for v in MP.proy(cam, -99.13, 19.43)])
    pt = np.array([float(v) for v in MP.proy(cam, -99.66, 19.29)])
    A0, A1 = pt + np.array([-330.0, 40.0]), pm + np.array([-70.0, 20.0])
    if re_ <= 0.01:
        _flecha(lz, A0, A1, 70, (255, 214, 84), av)
        for i in range(8):
            u = max(0.0, min(0.999, av - 0.06 * i))
            if u > 0.01:
                p = A0 + (A1 - A0) * u
                MD.ejercito(lz, float(p[0]), float(p[1]) + 4, 12, bando="ins", t=t + i * 0.2, s=1.6, dir=1, semilla=i, bandera=(i == 0), polvo=(i % 2 == 0))
    else:
        B0, B1 = A1 + np.array([-10.0, 40.0]), A0 + np.array([-170.0, 90.0])
        _flecha(lz, A0, A1, 70, (255, 214, 84), 1.0, alfa=0.35)
        _flecha(lz, B0, B1, 80, (232, 70, 80), re_)
        for i in range(8):
            u = max(0.0, min(0.999, re_ - 0.06 * i))
            if u > 0.01:
                p = B0 + (B1 - B0) * u
                MD.ejercito(lz, float(p[0]), float(p[1]) + 4, 12, bando="ins", t=t + i * 0.2, s=1.6, dir=-1, semilla=i, bandera=(i == 0), polvo=(i % 2 == 0))
    k = U.pop(t, t_ent - 0.05) * U.salida(t, t_algo - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "…y entonces Hidalgo hizo algo", color=U.COL["morado"], px=70, k=k, cola=None)
    k = U.pop(t, t_algo + 0.1) * U.salida(t, t_orden - 0.1, 0.2)
    if k > 0.01:
        sx, sy = MP.proy(cam, -99.2, 19.4)
        P.rotulo(lz, float(sx) - 200, float(sy) - 160, "?", px=int(240 * k) + 10, k=k, color=(255, 214, 72))
    for (txt, col, dx, tt_) in (("¿un error?", U.COL["rojo"], -260, t_div), ("¿prudencia?", U.COL["verde"], 260, t_div + 0.35)):
        k = U.pop(t, tt_) * U.salida(t, t_orden - 0.1, 0.2)
        if k > 0.01:
            U.globo(lz, W / 2 + dx, 330, txt, px=44, k=k)
    kh = U.pop(t, t_orden - 0.1)
    if kh > 0.01:
        MD.medallon(lz, 300, 480, 150, "hidalgo", t, emocion="serio", habla=1.0 if t < t_ret + 0.6 else 0.0, k=kh, seed=2)
        U.llamada(lz, 300, 660, "Hidalgo", color=U.COL["morado"], px=44, k=kh, cola="arriba")
        U.llamada(lz, W / 2, 130, "¡ordenó retirarse!", color=U.COL["rojo"], px=92, k=kh * U.repop(t, t_ret + 0.1), cola=None)
    MD.brujula(lz, W - 110, H - 120, 1.0)


# ------------------------------------------------------------------------------------------------ 5. LAS DUDAS (burbujas de pensamiento)
def _nube(lz, x, y, r, k, col=(255, 255, 255)):
    for (dx, dy, rr) in ((0, 0, 1.0), (-0.9, 0.2, 0.7), (0.9, 0.2, 0.74), (-0.4, -0.5, 0.7), (0.5, -0.45, 0.66)):
        lz.relleno(circulo(x + dx * r * k, y + dy * r * k, r * rr * k, 16), col, capa=2)


def _icono_matanza(lz, x, y, s, t):
    lz.relleno(rect_red(x - 60 * s, y - 20 * s, 120 * s, 80 * s, 6 * s), (214, 150, 110), capa=2)
    lz.relleno(np.array([[x - 74 * s, y - 20 * s], [x + 74 * s, y - 20 * s], [x, y - 80 * s]]), (190, 70, 70), capa=2)
    for j, (dx, c) in enumerate(((-28, (255, 214, 72)), (0, (255, 140, 60)), (28, (255, 214, 72)))):
        h = (60 + 20 * math.sin(t * 9 + j * 2)) * s
        lz.relleno(np.array([[x + dx * s - 16 * s, y + 60 * s], [x + dx * s, y + 60 * s - h], [x + dx * s + 16 * s, y + 60 * s]]), c, capa=2)
    for j in range(3):
        u = ((t * 0.6 + j / 3) % 1.0)
        lz.relleno(circulo(x + 30 * s + 20 * s * u, y - 90 * s - 90 * s * u, (14 + 18 * u) * s, 12), (80, 76, 92), alfa=0.8 * (1 - u), capa=2)


def _icono_municion(lz, x, y, s, t):
    lz.relleno(rect_red(x - 70 * s, y + 10 * s, 140 * s, 56 * s, 6 * s), (160, 110, 76), capa=2)
    lz.relleno(rect_red(x - 62 * s, y + 18 * s, 124 * s, 40 * s, 4 * s), (60, 42, 40), capa=2)
    P.rotulo(lz, x, y + 38 * s, "0", px=int(54 * s), k=1.0, color=(255, 214, 72), sombra=0.0)
    for (dx, dy) in ((-24, -14), (24, -14), (0, -14), (-12, -34), (12, -34), (0, -54)):
        lz.relleno(circulo(x + dx * s - 80 * s, y + dy * s + 30 * s, 12 * s, 12), (70, 70, 82), capa=2)
        lz.relleno(circulo(x + dx * s - 83 * s, y + dy * s + 27 * s, 4.6 * s, 8), (170, 170, 186), capa=2)


@shot(T_D, bg=lambda t: bg_grad((54, 30, 112), (150, 70, 130), mid=(100, 46, 130), ym=0.5), post=[GRAD], ent=("fundido", 0.5))
def cr_dudas(lz, t):
    U.bokeh(lz, t, seed=31, n=14, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.24)
    U.haces_luz(lz, 560, 600, t, n=8, largo=1300, color=(255, 200, 240), alfa=0.10, ancho=0.09)
    U.chispas(lz, t, n=18, seed=32, tam=(5, 12))
    kv = U.pop(t, T_D + 0.05, 1.3)
    RT.retrato(lz, 540, 1010, 240 * (0.94 + 0.06 * kv), "hidalgo", t, emocion="pensativo", habla=0.0, mirar=0.35, seed=5, alfa=min(1.0, kv))
    # tres burbujas: matanza, municiones, ¿?
    for (tt_, x, y, ico, lab, col) in ((t_temia - 0.1, 1100, 330, "m", "¿temía una matanza?", U.COL["rojo"]), (t_quiz2 - 0.1, 1560, 560, "u", "¿sin municiones?", U.COL["naranja"]), (t_nadie - 0.1, 1130, 760, "?", "nadie lo sabe", U.COL["morado"])):
        k = U.pop(t, tt_, 1.2)
        if k > 0.01:
            for j, (px_, py_, rr) in enumerate(((820 + (x - 820) * 0.14, 760 + (y - 760) * 0.14, 12), (820 + (x - 820) * 0.28, 760 + (y - 760) * 0.28, 20))):
                lz.relleno(circulo(px_, py_, rr * k, 12), (255, 255, 255), capa=2)
            _nube(lz, x, y, 150, k)
            with lz.grupo(x, y, 1.0):
                if ico == "m":
                    _icono_matanza(lz, 0, 10, 0.95 * k, t)
                elif ico == "u":
                    _icono_municion(lz, 20, 0, 0.95 * k, t)
                else:
                    P.rotulo(lz, 0, 10, "?", px=int(220 * k) + 10, k=1.0, color=(150, 80, 200), sombra=0.0)
            U.llamada(lz, x, y + 190, lab, color=col, px=42, k=k * U.repop(t, tt_ + 0.4), cola="arriba")
    k = U.pop(t, T_D + 0.1) * U.salida(t, t_temia - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "¿por qué se retiró?", color=U.COL["azul"], px=80, k=k, cola=None)


# ------------------------------------------------------------------------------------------------ 6. EL EJÉRCITO REALISTA SE REORGANIZA
def cam_e(t):
    return K(t, [(T_E, (230, 250, 36, 2.1)), (t_reorg, (240, 250, 36, 2.5)), (t_pers, (300, 240, 36, 2.4)), (T_F, (360, 230, 36, 2.2))])


@shot(T_E, bg=lambda t: bg_grad((130, 180, 240), (254, 232, 204), mid=(200, 216, 240), ym=0.5), post=[GRAD], ent=("fundido", 0.5))
def cr_realistas(lz, t):
    cx, cy, cz, zm = cam_e(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz(mul=(1.03, 1.0, 0.96), mix=(255, 220, 160), k=0.05)
    CAMPO.suelo(lz, iso, t)
    m = CAMPO.objetos(t)
    orden = e_inout(prog(t, t_ejr, t_reorg + 1.4))
    marcha = prog(t, t_pers - 0.1, t_pers + 3.0)
    tipos = ("realista", "granadero", "dragon", "realista", "oficial", "granadero")
    for i in range(72):
        r_, c_ = i // 12, i % 12
        # desorden: puntos al azar en el campo; orden: cuadro de 6 hileras x 12 filas
        xd, yd = 40 + 400 * h01(161, i), 120 + 220 * h01(162, i)
        xo, yo = 90 + 22 * c_, 140 + 24 * r_ * 1.0
        x, y = lerp(xd, xo, orden), lerp(yd, yo, orden)
        if marcha > 0:
            x, y = lerp(x, 560 + 120 * marcha, e_in(marcha)) + 10 * h01(163, i) * 0, lerp(y, 230 - 50 * marcha + 20 * (r_ - 3), e_in(marcha))
        mov = (0.02 < orden < 0.98) or (0.0 < marcha < 1.0)
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i, mov, orden: (lambda lz, iso: G.persona(lz, iso, x, y, t, tipos[i % 6], dir=(1, 0.2) if mov else ((0, 1) if orden >= 0.98 else (h01(164, i) - 0.5, 1)), vel=1.7 if mov else 0.0, seed=8200 + i, h=44, cara="serio", accion=("vitorea" if orden >= 0.98 and marcha <= 0 and i % 5 == 0 and t > t_reorg + 1.5 else None))))(x, y, i, mov, orden), fijo=False, clave=x + y + 4)
    # Calleja a caballo al frente
    cxp = lerp(100, 580, e_in(marcha)) if marcha > 0 else 100
    m.add(cxp - 8, 210, cxp + 8, 226, 50, lambda lz, iso: G.caballo(lz, iso, cxp, 218, t, dir=1, seed=9, vel=1.0 if marcha > 0 else 0.0, jinete="dragon", s=1.3), fijo=False, clave=cxp + 218 + 10)
    m.dibujar(lz, iso)
    DC.polvo_luz(lz, t, n=20, seed=33, color=(240, 214, 170), alfa=0.4)
    k = U.pop(t, T_E + 0.05, 1.2) * U.salida(t, t_ejr - 0.15, 0.3)
    if k > 0.01:
        P.rotulo(lz, W / 2, 190, "Esa decisión cambió la historia", px=int(86 * (0.94 + 0.06 * k)), k=k, color=(255, 255, 255))
    k = U.pop(t, t_ejr - 0.05) * U.salida(t, t_reorg - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "el ejército realista", color=U.COL["rojo"], px=76, k=k * U.repop(t, t_real + 0.1), cola=None)
    k = U.pop(t, t_reorg - 0.05) * U.salida(t, t_pers - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "se reorganiza", color=U.COL["azul"], px=84, k=k * U.repop(t, t_reorg + 0.4), cola=None)
    k = U.pop(t, t_pers - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "y los persigue", color=U.COL["naranja"], px=88, k=k * U.repop(t, t_pers + 0.2), cola=None)
    kc = U.pop(t, t_real - 0.05) * U.salida(t, t_reorg + 0.6, 0.25)
    if kc > 0.01:
        MD.medallon(lz, 1640, 420, 130, "calleja", t, emocion="serio", k=kc, seed=9)
        U.llamada(lz, 1640, 588, "Calleja", color=U.COL["rojo"], px=42, k=kc, cola="arriba")


# ------------------------------------------------------------------------------------------------ 7. ACULCO (mapa)
RUTA_AC = [(-99.55, 19.85), (-99.70, 20.00), (-99.83, 20.10)]


def cam_f(t):
    return Klog(t, [(T_F, (-99.55, 19.95, 2.0)), (t_acu, (-99.78, 20.06, 3.0)), (T_G, (-99.80, 20.08, 3.4))])


@shot(T_F, bg=lambda t: BASE(cam_f(t), t), post=[GRAD], ent=("zoom", 0.5))
def cr_aculco(lz, t):
    cam = cam_f(t)
    I.luz()
    MD.montes(lz, cam, min_alt=2200)
    MD.pais(lz, cam, "Mexico", (255, 96, 70), alfa=0.12, borde=(255, 220, 90), ancho=4.0, t=t, latido=1.0)
    MD.ciudad(lz, cam, "aculco", t, T_F + 0.1, tam=2.0, tipo="pueblo", bando="real", semilla=3)
    MD.ciudad(lz, cam, "mexico", t, T_F, tam=1.6, tipo="ciudad", bando="real", semilla=7)
    # los realistas (rojos) persiguen; los insurgentes (verdes) se dispersan hacia el norte
    f = e_inout(prog(t, T_F + 0.2, t_acu + 0.6))
    for i in range(6):
        u = max(0.0, min(0.999, f - 0.05 * i))
        if u > 0.01:
            x, y, v = MD.punto_ruta(cam, RUTA_AC, u)
            MD.ejercito(lz, float(x), float(y), 12, bando="real", t=t + i * 0.2, s=1.6, dir=1, semilla=i, bandera=(i == 0), polvo=(i % 2 == 0))
    sx, sy = MP.proy(cam, -99.83, 20.10)
    d = e_out(prog(t, t_acu + 0.4, t_all + 0.2))
    for i in range(10):
        ang = -2.4 + 1.6 * h01(171, i)
        r_ = (60 + 220 * h01(172, i)) * d
        MD.ejercito(lz, float(sx) + math.cos(ang) * r_ + 20 * h01(173, i), float(sy) + math.sin(ang) * r_ * 0.7, 6, bando="ins", t=t + i * 0.3, s=1.4, dir=-1 if math.cos(ang) < 0 else 1, semilla=i, bandera=False, polvo=False)
    MD.insignia_batalla(lz, cam, "aculco", t, t_acu - 0.1, año=1810, s=1.5)
    k = U.pop(t, t_ins - 0.05) * U.salida(t, t_acu - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "los insurgentes son derrotados", color=U.COL["rojo"], px=70, k=k, cola=None)
    k = U.pop(t, t_acu - 0.05)
    if k > 0.01:
        U.llamada(lz, float(sx), float(sy) - 150, "Aculco", color=U.COL["morado"], px=72, k=k * U.repop(t, t_acu + 0.4), cola="abajo")
    MD.brujula(lz, W - 110, H - 120, 1.0)


# ------------------------------------------------------------------------------------------------ 8. ALLENDE E HIDALGO DISCUTEN
@shot(T_G, bg=lambda t: bg_grad((70, 32, 100), (160, 60, 100), mid=(112, 44, 100), ym=0.5), post=[GRAD], ent=("fundido", 0.4))
def cr_discusion(lz, t):
    U.bokeh(lz, t, seed=35, n=14, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.22)
    U.chispas(lz, t, n=14, seed=36, tam=(5, 12))
    xdiv = W / 2
    k1 = U.pop(t, T_G + 0.05, 1.2)
    k2 = U.pop(t, T_G + 0.35, 1.2)
    gesto = 0.5 + 0.5 * math.sin(t * 7)
    RT.retrato(lz, 480, 1000, 250 * (0.94 + 0.06 * k1), "allende", t, emocion="enojo", habla=gesto if t < t_disc + 1.2 else 0.0, mirar=0.5, seed=4, flip=1, alfa=min(1.0, k1), luz_borde=(255, 120, 90))
    RT.retrato(lz, 1440, 1000, 250 * (0.94 + 0.06 * k2), "hidalgo", t, emocion="enojo", habla=(1 - gesto) if t < t_disc + 1.2 else 0.0, mirar=-0.5, seed=5, flip=-1, alfa=min(1.0, k2), luz_borde=(255, 120, 90))
    lz.trazo(np.array([[xdiv - 8, 80], [xdiv + 16, 360], [xdiv - 14, 600], [xdiv + 10, 860], [xdiv - 6, 1100]]), (255, 214, 72), 7.0, afinar=False, temblor=0.0, capa=2)
    for (x, y, tx, tt_) in ((560, 330, "¡¡hay que seguir!!", t_all), (1380, 330, "¡¡no, es mejor esperar!!", t_hid2 + 0.2)):
        kk = U.pop(t, tt_)
        if kk > 0.01:
            U.globo(lz, x, y + 120, tx, px=36, k=kk, cola="abajo")
    U.llamada(lz, 480, 190, "Ignacio Allende", color=U.COL["azul"], px=48, k=k1, cola=None)
    U.llamada(lz, 1440, 190, "Miguel Hidalgo", color=U.COL["morado"], px=48, k=k2, cola=None)
    kd = U.pop(t, t_disc - 0.05)
    if kd > 0.01:
        U.llamada(lz, W / 2, 130, "discuten", color=U.COL["rojo"], px=84, k=kd * U.repop(t, t_disc + 0.2), cola=None)


# ------------------------------------------------------------------------------------------------ 9. SE SEPARAN (mapa)
RUTA_AL = [(-99.83, 20.10), (-100.20, 20.55), (-100.8, 21.0), (-101.26, 21.02)]
RUTA_HI = [(-99.83, 20.10), (-100.30, 19.90), (-101.19, 19.70), (-102.0, 19.9), (-103.35, 20.67)]


def cam_h(t):
    return Klog(t, [(T_H, (-100.5, 20.3, 1.7)), (T1(E7), (-101.3, 20.4, 1.4))])


@shot(T_H, bg=lambda t: BASE(cam_h(t), t), post=[GRAD], ent=("zoom", 0.5))
def cr_separan(lz, t):
    cam = cam_h(t)
    I.luz()
    MD.montes(lz, cam, min_alt=2200)
    MD.pais(lz, cam, "Mexico", (255, 96, 70), alfa=0.12, borde=(255, 220, 90), ancho=4.0, t=t, latido=1.0)
    MD.ciudad(lz, cam, "aculco", t, T_H, tam=1.6, tipo="pueblo", bando="real", semilla=3)
    for j, (lug, tp, nm, dx, dy, lado) in enumerate((("guanajuato", "ciudad", "Guanajuato", 130, 4, "izq"), ("valladolid", "ciudad", "Valladolid", -130, 4, "der"), ("guadalajara", "ciudad", "Guadalajara", -140, 4, "der"))):
        MD.ciudad(lz, cam, lug, t, T_H + 0.2 + 0.1 * j, tam=1.5, tipo=tp, bando="ins", semilla=j + 51)
        MD.etiqueta(lz, cam, lug, nm, t, T_H + 0.3 + 0.1 * j, px=22, dy=dy, dx=dx, lado=lado)
    f = e_inout(prog(t, T_H + 0.2, T1(E7) - 0.2))
    MD.ruta(lz, cam, RUTA_AL, color=(110, 200, 255), frac=f, t=t, ancho=9.0, flecha=True)
    MD.ruta(lz, cam, RUTA_HI, color=(255, 170, 90), frac=f, t=t, ancho=9.0, flecha=True)
    for (pts, col, nm, k_) in ((RUTA_AL, "ins", "allende", 0), (RUTA_HI, "ins", "hidalgo", 1)):
        x, y, v = MD.punto_ruta(cam, pts, max(0.01, min(0.999, f)))
        MD.ejercito(lz, float(x), float(y), 12, bando="ins" if k_ == 0 else (255, 170, 90), t=t + k_, s=1.8, dir=1, semilla=k_, bandera=True, polvo=True)
        kk = U.pop(t, T_H + 0.6)
        if kk > 0.01:
            MD.medallon(lz, float(x) + (-150 if k_ else 150), float(y) - 140, 90, nm, t, emocion="serio", k=kk, seed=k_ + 2)
    k = U.pop(t, t_sep - 0.1)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "y se separan", color=U.COL["rojo"], px=92, k=k * U.repop(t, t_sep + 0.2), cola=None)
    MD.brujula(lz, W - 110, H - 120, 1.0)


# ------------------------------------------------------------------------------------------------ sonido
snd(T_A + 0.2, "whoosh", 0.3, dur=1.0)
snd(t_monte, "gong", 0.4)
snd(T_A2, "tambor", 0.4)
for _i in range(5):
    snd(T_A2 + 0.5 + 1.3 * _i, "canonazo", 0.4)
snd(t_derr, "gong", 0.5)
snd(T_B, "whoosh", 0.3, dur=1.0)
snd(t_ocho, "tambor", 0.5)
snd(t_hom, "pop", 0.4)
snd(T_C, "whoosh", 0.3, dur=0.9)
snd(t_algo, "pluck", 0.5)
snd(t_orden, "gong", 0.5)
snd(T_D, "pop", 0.3)
snd(t_temia, "pop", 0.4)
snd(t_quiz2, "pop", 0.4)
snd(t_nadie, "pluck", 0.5)
snd(T_E, "gong", 0.4)
snd(t_reorg, "tambor", 0.5)
snd(t_pers, "galope", 0.5, dur=2.5)
snd(T_F, "whoosh", 0.3, dur=0.9)
snd(t_acu, "canonazo", 0.5)
snd(T_G, "pop", 0.3)
snd(t_disc, "bonk", 0.4)
snd(T_H, "whoosh", 0.3, dur=0.9)
snd(t_sep, "gong", 0.5)
