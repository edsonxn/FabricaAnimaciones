# -*- coding: utf-8 -*-
"""Escena 4 · La conspiración (1:45-2:28): la tertulia secreta, Querétaro y la casa del corregidor, los oficiales, el líder que falta (Dolores), los oficios del cura, la delación y Josefa Ortiz que avisa desde su encierro."""
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
import mundos_e as me

E4 = "conspiracion"
MP = KM.MAPA
GRAD = lambda img, t: U.gradacion(img)
BASE = lambda cam, t: MP.base(cam, t, exag=12.0, rios_umbral=0.7)
CAL = me.CalleQueretaro()
TAL = me.TalleresDolores()

# ------------------------------------------------------------------ anclas
t_cri, t_sec, t_tert, t_lit = T(E4, "criollos", frase=0), T(E4, "secreto", frase=0), T(E4, "tertulias", frase=0), T(E4, "literarias", frase=0)
t_quer, t_casa, t_corr, t_mig, t_jos1 = T(E4, "queretaro", frase=1), T(E4, "casa", frase=1), T(E4, "corregidor", frase=1), T(E4, "miguel", frase=1), T(E4, "josefa", frase=1)
t_ahi, t_ofi, t_all, t_ald, t_plan, t_arm = T(E4, "ahi", frase=2), T(E4, "oficiales", frase=2), T(E4, "ignacio", frase=2), T(E4, "juan", frase=2), T(E4, "plan", frase=2), T(E4, "armas", frase=2)
t_falt, t_lid, t_pue, t_enc, t_dol, t_cur, t_hid = T(E4, "faltaba", frase=3), T(E4, "lider", frase=3), T(E4, "pueblo", frase=3), T(E4, "encontraron", frase=3), T(E4, "dolores", frase=3), T(E4, "cura", frase=3), T(E4, "hidalgo", frase=3)
t_cul, t_len, t_ind, t_ens, t_cam, t_ofc, t_pob = T(E4, "culto", frase=4), T(E4, "lenguas", frase=4), T(E4, "indigenas", frase=4), T(E4, "ensenaba", frase=4), T(E4, "campesinos", frase=4), T(E4, "oficios", frase=4), T(E4, "pobreza", frase=4)
t_fec, t_lev, t_oct, t_per, t_alg, t_del = T(E4, "fecha", frase=5), T(E4, "levantamiento", frase=5), T(E4, "octubre", frase=5), T(E4, "pero", frase=5), T(E4, "alguien", frase=5), T(E4, "delato", frase=5)
t_jos, t_cerr, t_cas6, t_avi, t_cons, t_desc = T(E4, "josefa", frase=6), T(E4, "encerrada", frase=6), T(E4, "casa", frase=6), T(E4, "avisar", frase=6), T(E4, "conspiradores", frase=6), T(E4, "descubiertos", frase=6)
T_A, T_B1, T_B2, T_C, T_D, T_E, T_F, T_G = T0(E4), t_quer - 0.9, t_casa - 0.4, t_ahi - 0.25, t_falt - 0.2, T(E4, "hidalgo", frase=4) - 0.35, t_fec - 0.3, t_jos - 0.3
PURPURA = lambda t: bg_grad((40, 22, 92), (130, 58, 124), mid=(84, 38, 112), ym=0.5)


# ------------------------------------------------------------------------------------------------ 1. LA TERTULIA SECRETA
def _criollos(m, t, T0_, posiciones, tipos, accion=None, h=50):
    """Criollos que entran por la puerta de la pared derecha (x=0) y toman sus sitios alrededor de la mesa."""
    for i, (px, py) in enumerate(posiciones):
        ti = T0_ + 0.42 * i
        u = e_inout(prog(t, ti, ti + 1.5))
        x = lerp(2.0, px, u)
        y = lerp(176.0, py, u)
        caminando = 0.0 < u < 1.0
        d = (px - 2.0, py - 176.0) if caminando else ((140 - px), (118 - py))
        n = math.hypot(*d) or 1.0
        if u <= 0.0:
            continue
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, d, n, i, caminando: (lambda lz, iso: G.persona(lz, iso, x, y, t, tipos[i % len(tipos)], dir=(d[0] / n, d[1] / n), vel=1.0 if caminando else 0.0, seed=4100 + i, h=h, accion=(None if caminando else accion), cara=("habla" if (not caminando and i % 2 == 0 and accion == "habla") else None))))(x, y, d, n, i, caminando), fijo=False, clave=x + y + 3)


@shot(T_A, bg=PURPURA, post=[GRAD], ent=("fundido", 0.5))
def q_tertulia(lz, t):
    I.luz(mul=(1.0, 0.96, 0.92), mix=(255, 170, 110), k=0.06)
    U.bokeh(lz, t, seed=11, n=12, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.20)
    iso = I.Iso(150, 125, 40, 3.3 + 0.05 * (t - T_A), sx0=930, sy0=650)
    me.sala_criolla(lz, iso, t)
    m = I.Mundo()
    me.mueble_sala(m, t, plan=prog(t, t_lit - 0.2, t_lit + 0.8))
    pos = ((60, 108), (60, 134), (200, 108), (200, 134), (98, 174), (144, 174), (98, 72), (150, 72))
    _criollos(m, t, T_A + 0.2, pos, ("noble", "comerciante", "regidor", "escribano", "noble", "comerciante", "regidor", "escribano"), accion="habla")
    # un criollo vigila la puerta (alto, junto al marco) y la tertulia se «apaga» con el secreto
    m.add(0, 192, 10, 204, 40, lambda lz, iso: G.persona(lz, iso, 6, 206, t, "regidor", dir=(0.8, -0.6), seed=4200, h=52, cara="miedo"), fijo=False, clave=215)
    m.dibujar(lz, iso)
    N.araña(lz, iso, 130, 118, 130, t, velas=5, s=1.25)
    U.fecha_lugar(lz, t, T_A + 0.3, t_quer - 0.2, "Nueva España", "1809")
    # rótulos y globos
    ks = U.pop(t, t_sec - 0.15) * U.salida(t, t_tert - 0.1, 0.2)
    if ks > 0.01:
        qx, qy = iso.P(130, 100, 100)
        U.llamada(lz, float(qx), float(qy) - 40, "en secreto", color=U.COL["rojo"], px=62, k=ks * U.repop(t, t_sec + 0.3), cola="abajo")
        for i, (gx, gy, tx) in enumerate(((60, 108, "shh…"), (200, 134, "…"), (144, 174, "psst"))):
            kg = U.pop(t, t_sec + 0.2 + 0.3 * i)
            if kg > 0.01:
                sx, sy = iso.P(gx, gy, 62)
                U.globo(lz, float(sx), float(sy) - 4, tx, px=30, k=kg * ks)
    kt = U.pop(t, t_tert - 0.1)
    if kt > 0.01:
        qx, qy = iso.P(130, 120, 90)
        U.llamada(lz, W / 2 + 40, 960, "tertulias literarias", color=U.COL["azul"], px=64, k=kt * U.repop(t, t_lit + 0.2), cola=None)


# ------------------------------------------------------------------------------------------------ 2. QUERÉTARO Y LA CASA DEL CORREGIDOR
def cam_q(t):
    return Klog(t, [(T_B1, (-100.9, 21.7, 1.5)), (t_quer, (-100.45, 20.75, 3.0)), (T_B2 + 0.2, (-100.40, 20.62, 3.4))])


@shot(T_B1, bg=lambda t: BASE(cam_q(t), t), post=[GRAD], ent=("zoom", 0.7))
def q_mapa(lz, t):
    cam = cam_q(t)
    I.luz()
    MD.mar_vivo(lz, cam, t, seed=12)
    MD.montes(lz, cam, min_alt=2200)
    MD.pais(lz, cam, "Mexico", (255, 96, 70), alfa=0.20, borde=(255, 220, 90), ancho=4.0, t=t, latido=1.0)
    for j, (lug, tp) in enumerate((("mexico", "ciudad"), ("guanajuato", "ciudad"), ("dolores", "pueblo"), ("san_luis", "ciudad"), ("zitacuaro", "pueblo"))):
        MD.ciudad(lz, cam, lug, t, T_B1 + 0.05 * j, tam=1.4, tipo=tp, bando="real", semilla=j + 31)
    MD.ciudad(lz, cam, "queretaro", t, t_quer - 0.2, tam=3.0, tipo="ciudad", bando=(255, 206, 70), nombre="Querétaro", px=40, llama=True)
    MD.onda(lz, cam, "queretaro", t, t_quer, dur=2.2, r_deg=0.6, color=(255, 236, 170), n=3, ancho=5.0)
    k = U.pop(t, t_quer) * U.salida(t, T_B2 - 0.1, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "Querétaro", color=U.COL["morado"], px=80, k=k * U.repop(t, t_quer + 0.5), cola=None)
    MD.brujula(lz, W - 110, H - 120, 1.0)


def cam_calle(t):
    return K(t, [(T_B2, (210, 200, 30, 2.1)), (t_corr, (250, 150, 56, 3.4)), (t_jos1, (250, 130, 60, 3.8)), (T_C, (250, 140, 56, 3.5))])


@shot(T_B2, bg=lambda t: bg_grad((250, 160, 100), (252, 226, 200), mid=(238, 130, 120), ym=0.45), post=[GRAD], ent=("fundido", 0.5))
def q_calle(lz, t):
    cx, cy, cz, zm = cam_calle(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz(mul=(1.04, 0.96, 0.90), mix=(255, 150, 90), k=0.10)
    CAL.suelo(lz, iso, t)
    m = CAL.objetos(t)
    # los conspiradores entran en fila a la casa del corregidor (zaguán en y≈178)
    for i in range(5):
        u = prog(t, T_B2 + 0.3 + 0.55 * i, T_B2 + 3.4 + 0.5 * i)
        if 0 < u < 1:
            x, y = lerp(130 + 22 * i, 252, e_inout(u)), lerp(236, 184, e_inout(u))
            m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i: (lambda lz, iso: G.persona(lz, iso, x, y, t, ["noble", "regidor", "comerciante", "escribano", "dama"][i], dir=(0.7, -0.7), vel=1.0, seed=4300 + i, h=44, alfa=1.0 - 0.8 * max(0.0, (y - 184) / 52 if False else 0))))(x, y, i), fijo=False, clave=x + y + 1)
    m.dibujar(lz, iso)
    DC.aves(lz, t, n=7, seed=21, y0=90, y1=300)
    DC.polvo_luz(lz, t, n=20, seed=5, color=(255, 214, 150), alfa=0.4)
    # medallones: corregidor y esposa
    kc = U.pop(t, t_corr + 0.1) * U.salida(t, T_C - 0.15, 0.2)
    if kc > 0.01:
        MD.medallon(lz, 330, 520, 125, "criollo", t, emocion="serio", k=kc, seed=7)
        U.llamada(lz, 330, 690, "Miguel Domínguez", color=U.COL["azul"], px=44, k=kc, cola="arriba")
        U.llamada(lz, 330, 830, "corregidor", color=U.COL["morado"], px=40, k=kc * U.repop(t, t_corr + 0.4), cola=None)
    kj = U.pop(t, t_jos1 - 0.1) * U.salida(t, T_C - 0.15, 0.2)
    if kj > 0.01:
        MD.medallon(lz, 1590, 520, 125, "josefa", t, emocion="neutro", k=kj, seed=8)
        U.llamada(lz, 1590, 690, "Josefa Ortiz", color=U.COL["rojo"], px=44, k=kj, cola="arriba")
    kl = U.pop(t, t_quer - 0.2) * U.salida(t, t_casa - 0.1, 0.2)
    if kl > 0.01:
        U.fecha_lugar(lz, t, T_B2, T_C - 0.2, "Querétaro", "1810", y=70)


# ------------------------------------------------------------------------------------------------ 3. LOS OFICIALES EN LA SALA
@shot(T_C, bg=PURPURA, post=[GRAD], ent=("tinta", 0.7))
def q_oficiales(lz, t):
    I.luz(mul=(1.0, 0.96, 0.92), mix=(255, 170, 110), k=0.06)
    U.bokeh(lz, t, seed=12, n=12, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.20)
    iso = I.Iso(135, 120, 42, 4.2 - 0.12 * (t - T_C), sx0=960, sy0=640)
    me.sala_criolla(lz, iso, t)
    m = I.Mundo()
    plan = prog(t, t_plan - 0.1, t_plan + 0.8)
    me.mueble_sala(m, t, plan=plan)
    # los oficiales entran a caballo... no: a pie, de uniforme, y se inclinan sobre la mesa
    pos = ((60, 108), (60, 134), (200, 108), (200, 134), (98, 174), (144, 174), (98, 72), (150, 72))
    _criollos(m, t, T_C - 9.0, pos, ("noble", "comerciante", "regidor", "escribano", "noble", "comerciante", "regidor", "escribano"), accion="habla", h=52)
    ua = e_inout(prog(t, t_all - 0.8, t_all + 0.6))
    ub = e_inout(prog(t, t_ald - 0.8, t_ald + 0.6))
    for (nm, tp, x0, x1, y0, y1, sd, tt_) in (("allende", "oficial", 2, 120, 176, 76, 4400, ua), ("aldama", "dragon", 2, 150, 176, 76, 4401, ub)):
        x, y = lerp(x0, x1, tt_), lerp(y0, y1, tt_)
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, tp, sd, tt_: (lambda lz, iso: G.persona(lz, iso, x, y, t, tp, dir=(0.4, -1) if tt_ > 0.98 else (1, -0.6), vel=0.0 if tt_ in (0.0, 1.0) else 1.0, seed=sd, h=58, cara="serio")))(x, y, tp, sd, tt_), fijo=False, clave=x + y + 8)
    m.dibujar(lz, iso)
    N.araña(lz, iso, 130, 118, 130, t, velas=5, s=1.25)
    # retratos de los oficiales con su nombre
    for (nm, lab, tt_, px_, col) in (("allende", "Ignacio Allende", t_all, 300, U.COL["azul"]), ("aldama", "Juan Aldama", t_ald, 1620, U.COL["naranja"])):
        k = U.pop(t, tt_ - 0.05) * U.salida(t, t_plan - 0.25, 0.2)
        if k > 0.01:
            MD.medallon(lz, px_, 500, 120, nm, t, emocion="serio", k=k, seed=3)
            U.llamada(lz, px_, 668, lab, color=col, px=42, k=k, cola="arriba")
    ko = U.pop(t, t_ofi - 0.1) * U.salida(t, t_all - 0.3, 0.2)
    if ko > 0.01:
        U.llamada(lz, W / 2, 130, "oficiales del ejército", color=U.COL["morado"], px=64, k=ko, cola=None)
    kp = U.pop(t, t_plan)
    if kp > 0.01:
        U.llamada(lz, W / 2, 130, "levantarse en armas", color=U.COL["rojo"], px=70, k=kp * U.repop(t, t_arm), cola=None)
        sx, sy = iso.P(124, 116, 34)
        for i in range(3):
            U.chispa4(lz, float(sx) + 70 * math.cos(t * 1.4 + i * 2.1), float(sy) - 40 + 40 * math.sin(t * 1.4 + i * 2.1), 12 + 5 * i, alfa=0.9 * kp)


# ------------------------------------------------------------------------------------------------ sonido
snd(T_A + 0.2, "pop", 0.3)
snd(t_sec, "pluck", 0.4)
snd(T_B1 + 0.1, "whoosh", 0.3, dur=1.0)
snd(t_quer, "campana", 0.35)
snd(T_B2, "amanecer", 0.2, dur=1.6)
snd(t_corr + 0.2, "pop", 0.3)
snd(t_jos1 + 0.1, "pop", 0.3)
snd(T_C, "whoosh", 0.3, dur=0.9)
snd(t_all, "pop", 0.35)
snd(t_ald, "pop", 0.35)
snd(t_plan, "bling", 0.4)
