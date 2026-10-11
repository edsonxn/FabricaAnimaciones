# -*- coding: utf-8 -*-
"""Escena 5 (continuación) · el estandarte guadalupano, la marcha con machetes, palos y piedras, la multitud que crece y el pueblo que quiere sus tierras."""
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
import kz_mapa_dib as MD
import plano as P
from motor import W, H, prog, lerp, smooth, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, h01, catmull
from reg import shot, snd
from util import *  # noqa: F401,F403
import mundos_f as mf
import t01
from t05 import *  # noqa: F401,F403

CAM_MARCHA = mf.CaminoMarcha()
TIE = mf.TierrasPueblo()


def _corazon(lz, x, y, r, col, alfa=1.0):
    lz.relleno(circulo(x - r * 0.5, y - r * 0.2, r * 0.58, 12), col, alfa=alfa, capa=2)
    lz.relleno(circulo(x + r * 0.5, y - r * 0.2, r * 0.58, 12), col, alfa=alfa, capa=2)
    lz.relleno(np.array([[x - r * 1.04, y - r * 0.0], [x + r * 1.04, y - r * 0.0], [x, y + r * 1.1]]), col, alfa=alfa, capa=2)


# ------------------------------------------------------------------------------------------------ 5. EL ESTANDARTE DE LA VIRGEN
def cam_e(t):
    return K(t, [(T_E, (214, 212, 52, 4.3)), (t_virg, (214, 206, 66, 4.9)), (t_pue, (214, 206, 74, 5.2)), (T_F, (214, 206, 78, 5.4))])


@shot(T_E, bg=lambda t: bg_grad((250, 190, 120), (254, 232, 200), mid=(244, 150, 130), ym=0.5), post=[GRAD], ent=("zoom", 0.6))
def g_estandarte(lz, t):
    cx, cy, cz, zm = cam_e(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz(mul=(1.06, 0.98, 0.90), mix=(255, 170, 100), k=0.10)
    DOL.suelo(lz, iso, t, isla=True)
    DOL.ang = 0.0
    m = DOL.objetos(t, gente=0.0)
    kb = e_back(prog(t, t_virg - 0.5, t_virg + 0.2)) if t >= t_virg - 0.5 else 0.0
    # el portaestandarte y su guardia; la multitud detrás con machetes y lanzas
    m.add(206, 196, 224, 214, 80, lambda lz, iso: G.persona(lz, iso, 215, 206, t, "insurgente_lanza", dir=(0, 1), seed=6001, h=46, accion="vitorea", cara="alegre"), fijo=False, clave=421)
    m.add(212, 196, 218, 202, 160, lambda lz, iso: O2.estandarte_virgen(lz, iso, 215, 203, h=46 + 14 * kb, t=t, w=34, alto=46) if kb > 0.01 else None, fijo=False, clave=419)
    for i, (x, y, tp) in enumerate(((190, 210, "insurgente"), (240, 212, "insurgente_lanza"), (176, 230, "indigena"), (254, 232, "campesina"), (200, 240, "honda"), (232, 242, "mestizo"), (160, 214, "campesino"), (270, 214, "indigena_f"), (214, 262, "insurgente"), (186, 270, "campesino"), (246, 268, "indigena"))):
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, tp, i: (lambda lz, iso: G.persona(lz, iso, x, y, t, tp, dir=(0.1 * (x - 215) / 50, -1), seed=6010 + i, h=44, accion="vitorea" if t > t_virg else None, cara="alegre")))(x, y, tp, i), fijo=False, clave=x + y + 3)
    # rayos dorados desde el estandarte
    bx, by = iso.P(215, 203, 120)
    U.haces_luz(lz, float(bx), float(by), t, n=9, largo=1500, color=(255, 230, 150), alfa=0.20 * kb, ancho=0.07, vel=0.08)
    lz.halo(float(bx), float(by), 520 * kb, (255, 224, 130), alfa=0.38 * kb, capa=0)
    m.dibujar(lz, iso)
    U.chispas(lz, t, n=24, seed=44, tam=(6, 14))
    # corazones que suben: «muy querida por el pueblo»
    kq = prog(t, t_quer - 0.2, t_quer + 2.2)
    if 0 < kq < 1:
        for i in range(9):
            u = (kq * 1.1 + i * 0.11) % 1.0
            _corazon(lz, float(bx) - 380 + 760 * h01(45, i), float(by) + 420 - 520 * u, 14 + 10 * h01(46, i), (255, 92, 130), alfa=1 - u)
    k = U.pop(t, t_band - 0.05) * U.salida(t, t_virg - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "la bandera", color=U.COL["naranja"], px=80, k=k, cola=None)
    k = U.pop(t, t_virg - 0.1)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "Virgen de Guadalupe", color=U.COL["verde"], px=74, k=k * U.repop(t, t_guad), cola=None)
    k = U.pop(t, t_quer - 0.1)
    if k > 0.01:
        U.llamada(lz, W / 2, 980, "muy querida por el pueblo", color=U.COL["rojo"], px=60, k=k * U.repop(t, t_pue), cola=None)


# ------------------------------------------------------------------------------------------------ 6. LA MARCHA: MACHETES, PALOS Y PIEDRAS
def _pos_agente(s0, ox, oy, vel, t):
    x, y = mf.pos_camino(s0 + (t - T_F) * vel)
    return x + ox, y + oy


def cam_f(t):
    sc = 120 + (t - T_F) * 20
    x, y = mf.pos_camino(sc)
    return (x + 10, y - 4, 24, 4.3)


@shot(T_F, bg=lambda t: bg_grad((130, 180, 240), (254, 232, 200), mid=(200, 214, 238), ym=0.5), post=[GRAD], ent=("fundido", 0.5))
def g_marcha(lz, t):
    cx, cy, cz, zm = cam_f(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz(mul=(1.04, 1.0, 0.94), mix=(255, 214, 160), k=0.06)
    CAM_MARCHA.suelo(lz, iso, t)
    m = CAM_MARCHA.objetos(t)
    # la columna: tres hileras de hombres a pie con machetes, lanzas/palos y hondas, y el estandarte al frente
    heroes = ((t_mach, "insurgente", 0.0, 12, "machetes", U.COL["rojo"], 1.0), (t_palos, "insurgente_lanza", 18.0, -14, "palos", U.COL["naranja"], 0.5), (t_pied, "honda", 36.0, 10, "piedras", U.COL["morado"], 1.4))
    tipos = ("insurgente", "insurgente_lanza", "campesino", "indigena", "honda", "mestizo", "campesina", "indigena_f")
    for i in range(64):
        s0 = 90 + 110 * h01(51, i)
        ox, oy = -18 + 36 * h01(52, i), -14 + 28 * h01(53, i)
        x, y = _pos_agente(s0, ox, oy, 20.0, t)
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i: (lambda lz, iso: G.persona(lz, iso, x, y, t, tipos[i % 8], dir=(1, -0.35), vel=1.1, seed=6100 + i, h=46, accion=None, cara="alegre" if i % 3 == 0 else None)))(x, y, i), fijo=False, clave=x + y + 3)
    xf, yf = _pos_agente(210.0, 0.0, 0.0, 20.0, t)
    m.add(xf - 4, yf - 4, xf + 4, yf + 4, 40, lambda lz, iso: G.persona(lz, iso, xf, yf, t, "insurgente_lanza", dir=(1, -0.35), vel=1.1, seed=6199, h=46, accion="vitorea", cara="alegre"), fijo=False, clave=xf + yf + 3)
    m.add(xf - 4, yf - 4, xf + 4, yf + 4, 160, lambda lz, iso: O2.estandarte_virgen(lz, iso, xf, yf, h=46, t=t, w=32, alto=44), fijo=False, clave=xf + yf + 4)
    # burros con cargas y mujeres que acompañan
    for i in range(3):
        x, y = _pos_agente(60 + 40 * i, 20, 18, 20.0, t)
        m.add(x - 6, y - 4, x + 6, y + 4, 20, (lambda x, y, i: (lambda lz, iso: G.burro(lz, iso, x, y, t, dir=1, seed=i, carga=True)))(x, y, i), fijo=False, clave=x + y + 3)
    m.dibujar(lz, iso)
    DC.aves(lz, t, n=8, seed=47, y0=60, y1=260)
    DC.polvo_luz(lz, t, n=24, seed=48, color=(240, 214, 160), alfa=0.45)
    # etiquetas de las armas: cada una señala a un hombre con esa arma
    for (tt_, tp, s0, oy, lab, col, dur_) in heroes:
        x, y = _pos_agente(150 + s0, 0.0, oy, 20.0, t)
        k = U.pop(t, tt_ - 0.1) * U.salida(t, tt_ + dur_, 0.2)
        if k > 0.01:
            m2 = I.Mundo()
            m2.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, tp: (lambda lz, iso: G.persona(lz, iso, x, y, t, tp, dir=(1, -0.35), vel=1.1, seed=6300 + int(s0), h=54, accion=None, cara="alegre")))(x, y, tp), fijo=False, clave=x + y + 9)
            m2.dibujar(lz, iso)
            qx, qy = iso.P(x, y, 70)
            U.llamada(lz, float(qx), float(qy) - 6, lab, color=col, px=50, k=k * U.repop(t, tt_ + 0.3), cola="abajo")
    k = U.pop(t, t_sal - 0.1) * U.salida(t, t_cien - 0.1, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "salen de Dolores", color=U.COL["azul"], px=68, k=k, cola=None)
    k = U.pop(t, t_cien - 0.05) * U.salida(t, t_arm5 - 0.25, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "unos cientos de hombres", color=U.COL["naranja"], px=68, k=k * U.repop(t, t_hom), cola=None)
    k = U.pop(t, t_arm5 - 0.05) * U.salida(t, t_mach - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "mal armados", color=U.COL["rojo"], px=66, k=k * U.repop(t, t_arm5 + 0.3), cola=None)


# ------------------------------------------------------------------------------------------------ 7. LA MULTITUD CRECE
RUTA_G = [(-100.93, 21.16), (-100.85, 21.03), (-100.74, 20.91), (-100.78, 20.70), (-100.81, 20.52)]


def cam_g(t):
    return Klog(t, [(T_G, (-100.90, 21.10, 4.4)), (t_miles, (-100.86, 20.98, 3.4)), (t_pocas, (-100.82, 20.86, 2.6)), (t_miles2, (-100.84, 20.84, 1.9)), (T_H, (-100.9, 20.9, 1.6))])


@shot(T_G, bg=lambda t: BASE(cam_g(t), t), post=[GRAD], ent=("zoom", 0.6))
def g_crece(lz, t):
    cam = cam_g(t)
    I.luz()
    MD.montes(lz, cam, min_alt=2200)
    MD.pais(lz, cam, "Mexico", (255, 96, 70), alfa=0.12, borde=(255, 220, 90), ancho=4.0, t=t, latido=1.0)
    for j, (lug, tp, nm, dx, dy, lado) in enumerate((("dolores", "pueblo", "Dolores", -120, -6, "der"), ((-100.74, 20.91), "pueblo", "San Miguel", 130, -6, "izq"), ((-100.81, 20.52), "ciudad", "Celaya", 120, -6, "izq"), ("guanajuato", "ciudad", "Guanajuato", -140, -6, "der"))):
        MD.ciudad(lz, cam, lug, t, T_G + 0.1 * j, tam=1.1, tipo=tp, bando="real", semilla=j + 17)
        MD.etiqueta(lz, cam, lug, nm, t, T_G + 0.1 * j + 0.1, px=22, dy=dy, dx=dx, lado=lado)
    # la columna insurgente crece: cada grupo es un puñado de hombres; llegan más de los pueblos cercanos (flechas de afluencia)
    ng = int(3 + 12 * smooth(prog(t, T_G, t_miles + 0.4)) + 60 * smooth(prog(t, t_pocas, t_miles2 + 0.6)))
    f = e_inout(prog(t, T_G, t_miles2 + 0.4))
    rutas = ((-100.93, 21.16), (-100.85, 21.03), (-100.74, 20.91), (-100.78, 20.70), (-100.81, 20.52))
    for i in range(ng):
        u = min(1.0, 0.04 * i + 0.1) * f * 0.0 + (i / max(1, ng - 1)) * f
        k_ = U.pop(t, T_G + 0.05 * i if i < 12 else (t_pocas + 0.07 * (i - 12)))
        if k_ <= 0.01:
            continue
        x, y, v = MD.punto_ruta(cam, list(rutas), min(0.999, max(0.0, u)))
        ox, oy = 200 * (h01(61, i) - 0.5) * (1 + 3 * smooth(prog(t, t_pocas, t_miles2))) * (cam[2] / 2.4), 120 * (h01(62, i) - 0.5) * (1 + 2.5 * smooth(prog(t, t_pocas, t_miles2))) * (cam[2] / 2.4)
        MD.ejercito(lz, float(x) + ox, float(y) + oy, 12, bando="ins", t=t + i * 0.3, s=2.2 * k_, dir=1, semilla=i, bandera=(i % 5 == 0), polvo=(i % 3 == 0))
    k = U.pop(t, t_pocos - 0.05) * U.salida(t, t_miles - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 140, "en pocos días…", color=U.COL["azul"], px=74, k=k, cola=None)
    k = U.pop(t, t_miles - 0.05) * U.salida(t, t_pocas - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 140, "¡eran miles!", color=U.COL["naranja"], px=96, k=k * U.repop(t, t_miles + 0.3), cola=None)
    k = U.pop(t, t_pocas - 0.05) * U.salida(t, t_dec - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 140, "en pocas semanas…", color=U.COL["azul"], px=74, k=k, cola=None)
    k = U.pop(t, t_dec - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 140, "¡decenas de miles!", color=U.COL["rojo"], px=106, k=k * U.repop(t, t_miles2 + 0.2), cola=None)
    MD.brujula(lz, W - 110, H - 120, 1.0)


# ------------------------------------------------------------------------------------------------ 8. TIERRAS Y TRIBUTOS
def cam_h(t):
    return K(t, [(T_H, (200, 250, 30, 2.5)), (t_recu, (150, 250, 26, 2.7)), (t_acab - 0.4, (170, 230, 26, 2.8)), (T1(E5), (220, 200, 40, 2.4))])


@shot(T_H, bg=lambda t: bg_grad((130, 190, 240), (252, 236, 206), mid=(196, 220, 238), ym=0.5), post=[GRAD], ent=("fundido", 0.5))
def g_tierras(lz, t):
    cx, cy, cz, zm = cam_h(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz(mul=(1.03, 1.0, 0.96), mix=(255, 220, 160), k=0.05)
    cae = prog(t, t_recu, t_tier + 1.0)
    verde = smooth(prog(t, t_tier + 0.2, t_tier + 2.0))
    trib = 1.0 - e_in(prog(t, t_acab - 0.1, t_acab + 1.0))
    TIE.suelo(lz, iso, t, verde=verde)
    m = TIE.objetos(t, fence=1.0 - cae, tributo=trib)
    # el pueblo (indígenas y mestizos) frente a la cerca; cuando cae, entra a sembrar su milpa; el cobrador y el escribano huyen
    tipos = ("indigena", "mestizo", "indigena_f", "campesina", "campesino", "indigena", "mestizo", "nino")
    entra = e_inout(prog(t, t_recu + 0.6, t_tier + 1.6))
    for i in range(18):
        x0, y0 = 262 + 60 * h01(71, i), 180 + 120 * h01(72, i)
        x1, y1 = 40 + 190 * h01(73, i), 176 + 190 * h01(74, i)
        x, y = lerp(x0, x1, entra), lerp(y0, y1, entra)
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i: (lambda lz, iso: G.persona(lz, iso, x, y, t, tipos[i % 8], dir=(-1, 0.1) if entra < 0.99 and entra > 0 else (0.2, 1), vel=1.0 if 0.0 < entra < 1.0 else 0.0, seed=6400 + i, h=44 if i % 8 != 7 else 30, accion=("trabaja" if entra >= 0.99 and i % 2 == 0 else ("vitorea" if t > t_esp and entra < 0.01 else None)), cara="alegre" if t > t_esp else None)))(x, y, i), fijo=False, clave=x + y + 3)
    huye = e_inout(prog(t, t_acab + 0.1, t_trib + 1.2))
    for i, (tp, ax, ay) in enumerate((("peninsular", 330, 196), ("escribano", 350, 206))):
        x, y = lerp(ax, ax + 160, huye), lerp(ay, ay + 90, huye)
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, tp, i: (lambda lz, iso: G.persona(lz, iso, x, y, t, tp, dir=(1, 0.5) if huye > 0 else (-1, 0.2), vel=1.6 if 0 < huye < 1 else 0.0, seed=6500 + i, h=48, cara="miedo" if huye > 0 else "enojo", alfa=1.0 - 0.9 * e_in(huye))))(x, y, tp, i), fijo=False, clave=x + y + 8)
    m.dibujar(lz, iso)
    DC.aves(lz, t, n=6, seed=49, y0=70, y1=240)
    DC.mariposas(lz, iso, 20, 150, 250, 370, n=int(2 + 8 * verde), t=t)
    # retratos de quiénes eran
    for (nm, lab, tt_, px_, col) in (("campesino", "indígenas", t_indi, 280, U.COL["naranja"]), ("criollo", "mestizos", t_mest, 1640, U.COL["azul"])):
        k = U.pop(t, tt_ - 0.05) * U.salida(t, t_esp - 0.2, 0.25)
        if k > 0.01:
            MD.medallon(lz, px_, 440, 120, nm, t, emocion="neutro", k=k, seed=11)
            U.llamada(lz, px_, 608, lab, color=col, px=44, k=k, cola="arriba")
    k = U.pop(t, t_mayo - 0.1) * U.salida(t, t_indi - 0.1, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "la mayoría del ejército", color=U.COL["morado"], px=66, k=k, cola=None)
    k = U.pop(t, t_esp - 0.1) * U.salida(t, t_recu - 0.15, 0.25)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "una esperanza", color=U.COL["verde"], px=80, k=k * U.repop(t, t_esp + 0.3), cola=None)
        for i in range(10):
            U.chispa4(lz, 300 + 1300 * h01(8, i), 200 + 700 * h01(9, i), 10 + 8 * h01(7, i), alfa=0.8 * k)
    k = U.pop(t, t_recu - 0.05) * U.salida(t, t_acab - 0.2, 0.25)
    if k > 0.01:
        qx, qy = iso.P(130, 270, 20)
        U.llamada(lz, float(qx), float(qy) - 20, "recuperar sus tierras", color=U.COL["verde"], px=58, k=k * U.repop(t, t_tier + 0.2), cola="abajo")
    k = U.pop(t, t_acab - 0.05)
    if k > 0.01:
        qx, qy = iso.P(340, 190, 36)
        U.llamada(lz, float(qx), float(qy) - 20, "tributos", color=U.COL["rojo"], px=64, k=k * U.repop(t, t_trib + 0.1), cola="abajo")
        ux = prog(t, t_trib - 0.1, t_trib + 0.35)
        if ux > 0:
            lz.trazo(np.array([[float(qx) - 130, float(qy) - 52 + 26], [float(qx) - 130 + 260 * ux, float(qy) - 52 + 26 - 52 * ux]]), (226, 40, 60), 16, afinar=False, temblor=0.0, capa=2)


# ------------------------------------------------------------------------------------------------ sonido
snd(T_A + 0.2, "amanecer", 0.3, dur=2.4)
snd(T_GALOPE, "galope", 0.5, dur=2.4)
snd(T_LLEGA, "pop", 0.4)
snd(t_not, "pluck", 0.5)
snd(T_B, "pop", 0.3)
snd(t_rem, "gong", 0.5)
for _k in range(8):
    snd(GOLPES_C[_k], "campana", 0.6)
snd(t_llam, "tambor", 0.4)
snd(T_D, "whoosh", 0.4, dur=0.8)
snd(t_grito, "gong", 0.6)
snd(t_arm, "tambor", 0.5)
snd(t_virg, "bling", 0.5)
snd(t_quer, "pop", 0.3)
snd(T_F, "tambor", 0.4)
snd(t_mach, "pop", 0.3)
snd(t_palos, "pop", 0.3)
snd(t_pied, "pop", 0.3)
snd(T_G, "whoosh", 0.3, dur=0.9)
snd(t_miles, "pop", 0.5)
snd(t_miles2, "gong", 0.5)
snd(t_mest, "pop", 0.3)
snd(t_recu, "crujido", 0.5)
snd(t_tier + 0.3, "bling", 0.5)
snd(t_trib, "bonk", 0.5)
