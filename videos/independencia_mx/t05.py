# -*- coding: utf-8 -*-
"""Escena 5 · El Grito de Dolores (2:28-3:13): Allende llega de madrugada, «ya no hay remedio», la campana convoca al pueblo, el Grito, el estandarte guadalupano, la marcha, la multitud que crece y el pueblo que quiere sus tierras."""
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
import mundos
import mundos_e as me
import mundos_f as mf
import t01

E5 = "grito"
MP = KM.MAPA
GRAD = lambda img, t: U.gradacion(img)
BASE = lambda cam, t: MP.base(cam, t, exag=12.0, rios_umbral=0.7)
DOL = mundos.Dolores()

# ------------------------------------------------------------------ anclas
t_alle, t_lleg, t_dol, t_mad, t_dies, t_sep, t_not = T(E5, "allende", frase=0), T(E5, "llego", frase=0), T(E5, "dolores", frase=0), T(E5, "madrugada", frase=0), T(E5, "dieciseis", frase=0), T(E5, "septiembre", frase=0), T(E5, "noticia", frase=0)
t_trad, t_hid, t_resp, t_rem, t_act, t_inm = T(E5, "tradicion", frase=1), T(E5, "hidalgo", frase=1), T(E5, "respondio", frase=1), T(E5, "remedio", frase=1), T(E5, "actuar", frase=1), T(E5, "inmediato", frase=1)
t_mand, t_toc, t_camp, t_par, t_llam, t_todos, t_unir = T(E5, "mando", frase=2), T(E5, "tocar", frase=2), T(E5, "campana", frase=2), T(E5, "parroquia", frase=2), T(E5, "llamo", frase=2), T(E5, "todos", frase=2), T(E5, "unirse", frase=2)
t_ese, t_grito, t_dolg, t_disc, t_escr, t_llm, t_arm = T(E5, "ese", frase=3), T(E5, "grito", frase=3), T(E5, "dolores", frase=3), T(E5, "discurso", frase=3), T(E5, "escrito", frase=3), T(E5, "llamada", frase=3), T(E5, "armas", frase=3)
t_tom, t_band, t_virg, t_guad, t_quer, t_pue = T(E5, "tomaron", frase=4), T(E5, "bandera", frase=4), T(E5, "virgen", frase=4), T(E5, "guadalupe", frase=4), T(E5, "querida", frase=4), T(E5, "pueblo", frase=4)
t_sal, t_cien, t_hom, t_arm5, t_mach, t_palos, t_pied = T(E5, "salieron", frase=5), T(E5, "cientos", frase=5), T(E5, "hombres", frase=5), T(E5, "armados", frase=5), T(E5, "machetes", frase=5), T(E5, "palos", frase=5), T(E5, "piedras", frase=5)
t_pocos, t_dias, t_miles, t_pocas, t_sem, t_dec, t_miles2 = T(E5, "pocos", frase=6), T(E5, "dias", frase=6), T(E5, "miles", frase=6), T(E5, "pocas", frase=6), T(E5, "semanas", frase=6), T(E5, "decenas", frase=6), T(E5, "miles", frase=6, n=1)
t_mayo, t_indi, t_mest, t_vier, t_esp, t_recu, t_tier, t_acab, t_trib = T(E5, "mayoria", frase=7), T(E5, "indigenas", frase=7), T(E5, "mestizos", frase=7), T(E5, "vieron", frase=7), T(E5, "esperanza", frase=7), T(E5, "recuperar", frase=7), T(E5, "tierras", frase=7), T(E5, "acabar", frase=7), T(E5, "tributos", frase=7)
T_A, T_B, T_C, T_D, T_E, T_F, T_G, T_H = T0(E5), t_trad - 0.25, t_mand - 0.3, t_ese - 0.25, t_tom - 0.3, t_sal - 0.25, t_pocos - 0.25, t_mayo - 0.3


def alba(t):
    return prog(t, t_dies + 0.2, t_not + 1.0)


def bg_madrugada(t):
    a = alba(t)
    c = lambda x0, x1: int(x0 + (x1 - x0) * a)
    return bg_grad((c(14, 110), c(16, 70), c(66, 150)), (c(48, 252), c(42, 176), c(112, 150)), mid=(c(30, 190), c(30, 110), c(96, 156)), ym=0.55)


def cielo_estrellas(lz, t, a, luna=True):
    for i in range(70):
        x, y = (h01(24, i, 1) * 2000) % 1920, (h01(24, i, 2) * 620)
        lz.relleno(circulo(x, y, 1.6 + 2.0 * h01(24, i, 3), 6), (255, 244, 210), alfa=(0.4 + 0.4 * math.sin(t * 2 + i)) * (1 - a), capa=0)
    if luna:
        lz.halo(300, 170 + 120 * a, 260, (170, 190, 255), alfa=0.30 * (1 - a), capa=0)
        lz.relleno(circulo(300, 170 + 120 * a, 56, 28), (244, 246, 255), alfa=1 - a, capa=0)


# ------------------------------------------------------------------------------------------------ 1. ALLENDE LLEGA A DOLORES (madrugada)
RUTA_A = [(30, 372), (120, 372), (200, 352), (252, 300), (292, 232), (312, 150)]
_dA = np.r_[0, np.cumsum(np.hypot(*np.diff(np.asarray(RUTA_A, float), axis=0).T))]


def _en_ruta(s):
    p = np.asarray(RUTA_A, float)
    s = float(np.clip(s, 0, _dA[-1] - 1e-3))
    i = int(np.clip(np.searchsorted(_dA, s, side="right") - 1, 0, len(p) - 2))
    f = (s - _dA[i]) / (_dA[i + 1] - _dA[i])
    q = p[i] + (p[i + 1] - p[i]) * f
    d = (p[i + 1] - p[i]) / np.hypot(*(p[i + 1] - p[i]))
    return float(q[0]), float(q[1]), d


T_LLEGA = t_dol + 0.9
T_GALOPE = T_A + 0.3


def cam_a(t):
    return K(t, [(T_A, (70, 360, 22, 1.7)), (T_A + 1.8, (190, 320, 26, 2.0)), (T_LLEGA - 0.2, (290, 200, 34, 2.8)), (t_dies, (300, 150, 40, 3.2)), (t_not, (300, 130, 44, 3.6)), (T_B, (300, 126, 44, 3.7))])


@shot(T_A, bg=bg_madrugada, post=[lambda img, t: U.gradacion(img, luces=(1.02, 1.0, 0.98), sombras=(0.94, 0.95, 1.06), saturacion=1.05)], ent=("fundido", 0.5))
def g_allende(lz, t):
    a = alba(t)
    cx, cy, cz, zm = cam_a(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz(mul=(0.72 + 0.32 * a, 0.78 + 0.22 * a, 1.0 - 0.08 * a), mix=(40, 50, 120), k=0.26 * (1 - a))
    cielo_estrellas(lz, t, a)
    DOL.suelo(lz, iso, t, isla=True)
    m = DOL.objetos(t, gente=0.0)
    A.casa_colonial(m, 276, 52, 64, 56, 46, muro=A.OCRE, techo=A.TEJA, eje="x", ventanas=2, puerta=True, seed=909)       # la casa del cura junto a la parroquia
    # Allende cabalga hasta la casa del cura, desmonta y entrega la noticia; Hidalgo sale a la puerta
    s = max(0.0, (t - T_GALOPE) * 215.0)
    x, y, d = _en_ruta(s)
    llegado = s >= _dA[-1] - 2
    if not llegado:
        m.add(x - 6, y - 6, x + 6, y + 6, 40, lambda lz, iso: G.caballo(lz, iso, x, y, t, dir=1 if d[0] >= 0 else -1, seed=5, vel=1.0, jinete="oficial", s=1.2), fijo=False, clave=x + y + 3)
    else:
        m.add(300, 140, 312, 152, 40, lambda lz, iso: G.caballo(lz, iso, 316, 160, t, dir=-1, seed=5, vel=0.0, jinete=None, s=1.2), fijo=False, clave=478)
        m.add(300, 130, 312, 142, 40, lambda lz, iso: G.persona(lz, iso, 300, 136, t, "oficial", dir=(0.6, -0.8), seed=5701, h=52, cara="serio", accion="habla"), fijo=False, clave=440)
        kh = e_inout(prog(t, t_dies + 0.5, t_dies + 1.5))
        m.add(300, 112, 312, 124, 40, lambda lz, iso: G.persona(lz, iso, 310, lerp(104, 122, kh), t, "cura", dir=(-0.2, 1), seed=5702, h=52, cara="normal" if t < t_not else "miedo"), fijo=False, clave=435)
        if prog(t, t_not - 0.4, t_not + 0.6) > 0:
            u = prog(t, t_not - 0.4, t_not + 0.6)
            m.add(300, 120, 312, 132, 40, lambda lz, iso: O2.pergamino(lz, iso, lerp(302, 308, u), lerp(134, 124, u), 36 + 6 * math.sin(u * math.pi), w=8, h=11, abre=1.0), fijo=False, clave=470)
    m.dibujar(lz, iso)
    for (wx, wy) in ((290, 112), (328, 112)):                                      # ventanas de la casa del cura: se encienden en la madrugada
        qx, qy = iso.P(wx, wy, 26)
        lz.halo(float(qx), float(qy), 44 * iso.z / 3.0, (255, 214, 130), alfa=0.30 * (1 - 0.5 * a), capa=2)
    DC.polvo_luz(lz, t, n=18, seed=25, color=(255, 214, 150), alfa=0.35)
    t1 = t01
    t1.aves(lz, t, t_dies, (900, 300), 6, 0.9) if t > t_dies else None
    # rótulos
    U.fecha_lugar(lz, t, T_A + 0.2, t_not + 0.3, "Dolores, Guanajuato", "16 de septiembre de 1810", y=70)
    k = U.pop(t, t_mad - 0.1) * U.salida(t, t_dies - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, 330, 330, "madrugada", color=U.COL["morado"], px=62, k=k * U.repop(t, t_mad + 0.3), cola=None)
    if llegado:
        qx, qy = iso.P(300, 136, 66)
        k = U.pop(t, T_LLEGA) * U.salida(t, t_not - 0.4, 0.2)
        if k > 0.01:
            U.llamada(lz, float(qx), float(qy) - 6, "Ignacio Allende", color=U.COL["azul"], px=40, k=k, cola="abajo")
        k = U.pop(t, t_not)
        if k > 0.01:
            U.llamada(lz, float(qx) + 130, float(qy) - 90, "¡la noticia!", color=U.COL["rojo"], px=60, k=k * U.repop(t, t_not + 0.4), cola="abajo")


# ------------------------------------------------------------------------------------------------ 2. «YA NO HAY REMEDIO»
@shot(T_B, bg=lambda t: bg_grad((60, 40, 120), (170, 90, 130), mid=(110, 56, 128), ym=0.5), post=[GRAD], ent=("fundido", 0.5))
def g_remedio(lz, t):
    I.luz(mul=(1.0, 0.96, 0.92), mix=(255, 170, 110), k=0.06)
    U.bokeh(lz, t, seed=26, n=12, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.20)
    iso = I.Iso(145, 120, 44, 3.3 + 0.05 * (t - T_B), sx0=930, sy0=650)
    mf.casa_cural(lz, iso, t, alba=1.0)
    m = I.Mundo()
    mf.amueblar_casa_cural(m, t)
    habla_h = t > t_resp
    m.add(210, 120, 226, 136, 40, lambda lz, iso: G.persona(lz, iso, 216, 128, t, "cura", dir=(-1, 0.1), seed=5710, h=60, cara="habla" if habla_h and (t % 0.8) < 0.5 else "serio", accion="habla" if habla_h else None), fijo=False, clave=345)
    m.add(60, 100, 76, 116, 40, lambda lz, iso: G.persona(lz, iso, 66, 108, t, "oficial", dir=(1, 0.2), seed=5711, h=58, cara="serio", accion="habla" if t < t_resp else None), fijo=False, clave=170)
    m.add(70, 150, 86, 166, 40, lambda lz, iso: G.persona(lz, iso, 76, 158, t, "dragon", dir=(1, -0.2), seed=5712, h=58, cara="miedo"), fijo=False, clave=235)
    m.dibujar(lz, iso)
    N.araña(lz, iso, 140, 120, 128, t, velas=4, s=1.1)
    # retratos con su frase («según la tradición»)
    k = U.pop(t, T_B + 0.1) * U.salida(t, t_resp - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "según la tradición…", color=U.COL["morado"], px=72, k=k, cola=None)
    kh = U.pop(t, t_hid)
    if kh > 0.01:
        MD.medallon(lz, 1700, 340, 150, "hidalgo", t, emocion="serio", habla=1.0 if t_resp < t < t_act else 0.0, k=kh, seed=2)
        U.llamada(lz, 1700, 520, "Hidalgo", color=U.COL["morado"], px=44, k=kh, cola="arriba")
    ka = U.pop(t, T_B + 0.3)
    if ka > 0.01:
        MD.medallon(lz, 230, 340, 120, "allende", t, emocion="serio", k=ka, seed=3)
    kr = U.pop(t, t_rem - 0.25) * U.salida(t, t_act - 0.1, 0.2)
    if kr > 0.01:
        U.globo(lz, 1470, 330, "¡Ya no hay remedio!", px=46, k=kr * U.repop(t, t_rem + 0.2), cola="der", lado=1)
    ki = U.pop(t, t_act - 0.1)
    if ki > 0.01:
        U.globo(lz, 1470, 330, "¡Hay que actuar ya!", px=46, k=ki * U.repop(t, t_inm + 0.1), cola="der", lado=1)


# ------------------------------------------------------------------------------------------------ 3. LA CAMPANA CONVOCA AL PUEBLO
def ang_c(t):
    if t < t_camp - 0.6:
        return 0.0
    u = t - (t_camp - 0.6)
    return 0.62 * math.sin(u * 6.98) * math.exp(-u * 0.10)


GOLPES_C = [t_camp - 0.6 + 0.45 * k for k in range(10)]


def cam_c(t):
    return K(t, [(T_C, (240, 150, 40, 2.1)), (t_camp, (236, 190, 60, 2.7)), (t_llam, (230, 230, 28, 2.3)), (T_D, (230, 240, 24, 2.2))])


@shot(T_C, bg=lambda t: bg_grad((120, 150, 230), (252, 214, 190), mid=(214, 168, 210), ym=0.55), post=[GRAD], ent=("fundido", 0.5))
def g_campana(lz, t):
    cx, cy, cz, zm = cam_c(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz(mul=(1.04, 0.97, 0.92), mix=(255, 170, 120), k=0.10)
    t01.nubes(lz, t)
    DOL.suelo(lz, iso, t, isla=True)
    DOL.ang = ang_c(t)
    m = DOL.objetos(t, gente=0.0)
    A.casa_colonial(m, 276, 52, 64, 56, 46, muro=A.OCRE, techo=A.TEJA, eje="x", ventanas=2, puerta=True, seed=909)
    px, py = 264.0, 188.0
    m.add(px - 5, py - 5, px + 5, py + 5, 40, lambda lz, iso: G.persona(lz, iso, px, py, t, "cura", dir=(0, 1), seed=21, accion="trabaja" if t >= t_camp - 0.6 else "habla", h=40), fijo=False)
    # el pueblo acude de todas las calles a la plaza
    mu = G.Multitud()
    tipos = ("campesino", "campesina", "mestizo", "indigena", "indigena_f", "arriero", "comerciante", "nino")
    entradas = (((-60, 372), (120, 372)), ((520, 372), (340, 372)), ((96, 520), (98, 372)), ((364, 520), (362, 372)), ((96, -60), (98, 150)), ((362, -60), (360, 150)))
    for i in range(44):
        (p0, p1) = entradas[i % 6]
        fx, fy = 140 + 190 * h01(31, i), 200 + 140 * h01(32, i)
        mu.camina([p0, p1, (fx, fy)], tipos[i % 8], vel=26 + 8 * h01(33, i), fase=0.0, seed=5800 + i, h=40 if i % 8 != 7 else 28, bucle=False, t0=T_C - 22.0 * h01(34, i) - 2.0)
    mu.dibujar(m, t)
    m.dibujar(lz, iso)
    sx0, sy0 = iso.P(264, 162, 130)
    sx1, sy1 = iso.P(px, py, 24)
    sw = math.sin(max(0.0, t - t_camp + 0.6) * 6.98 + 0.4) * 5 * zm
    P_ = np.array([[sx0, sy0], [(sx0 + sx1) / 2 + sw, (sy0 + sy1) / 2], [sx1, sy1]])
    lz.trazo(np.array(t01.catmull_(P_)), (232, 216, 180), 2.2 * zm, afinar=False, temblor=0.0, capa=2)
    bx, by = iso.P(264, 162, 140)
    for g in GOLPES_C:
        if g - 0.05 < t < g + 2.0:
            U.onda_iso(lz, iso, 264, 162, t, g, dur=1.8, r1=260, n=1, color=(255, 230, 170), periodo=0.3, ancho=2.4)
        if g <= t < g + 1.2:
            U.ondas_sonoras(lz, float(bx), float(by), t, g, dur=1.1, r1=210 * zm / 3.0, n=1, color=(255, 238, 180), ancho=3.0, periodo=0.28, alfa=0.55)
    t01.aves(lz, t, GOLPES_C[0] + 0.1, (float(bx), float(by) - 20), 10)
    t01.aves(lz, t, GOLPES_C[4] + 0.1, (float(bx) + 40, float(by) - 10), 8, vel=0.9)
    k = U.pop(t, t_camp - 0.05) * U.salida(t, t_llam - 0.1, 0.2)
    if k > 0.01:
        U.llamada(lz, float(bx), float(by) - 70, "la campana de la parroquia", color=U.COL["naranja"], px=48, k=k * U.repop(t, t_camp + 0.4), cola="abajo")
    k = U.pop(t, t_llam - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "¡a todos los que quieran unirse!", color=U.COL["verde"], px=64, k=k * U.repop(t, t_unir - 0.3), cola=None)


# ------------------------------------------------------------------------------------------------ 4. EL GRITO
def cam_d(t):
    return K(t, [(T_D, (236, 230, 28, 2.5)), (t_grito, (220, 186, 40, 3.5)), (t_disc, (220, 190, 38, 3.8)), (t_arm, (222, 210, 32, 3.4)), (T_E, (224, 226, 30, 3.0))])


@shot(T_D, bg=lambda t: bg_grad((250, 160, 120), (254, 226, 190), mid=(240, 130, 140), ym=0.5), post=[GRAD], ent=("destello", 0.5))
def g_grito(lz, t):
    cx, cy, cz, zm = cam_d(t)
    sh = 6 * max(0.0, 1 - (t - t_grito) / 0.5) if t_grito < t < t_grito + 0.5 else 0.0
    with lz.grupo(sh * math.sin(t * 90), sh * math.cos(t * 77), 1.0):
        iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
        I.luz(mul=(1.06, 0.96, 0.90), mix=(255, 150, 90), k=0.14)
        DOL.suelo(lz, iso, t, isla=True)
        DOL.ang = ang_c(t)
        m = DOL.objetos(t, gente=0.0)
        A.casa_colonial(m, 276, 52, 64, 56, 46, muro=A.OCRE, techo=A.TEJA, eje="x", ventanas=2, puerta=True, seed=909)
        # Hidalgo en el atrio, brazo en alto; a su lado Allende y Aldama; el pueblo abajo vitoreando con machetes y palos
        m.add(200, 150, 232, 180, 40, lambda lz, iso: _tarima_atrio(lz, iso), fijo=False, clave=365)
        m.add(212, 160, 222, 170, 60, lambda lz, iso: G.persona(lz, iso, 215, 165, t, "cura", dir=(0, 1), seed=5720, h=60, z=10, accion="vitorea", cara="habla" if (t_grito < t < t_arm + 0.3) else "serio"), fijo=False, clave=380)
        m.add(180, 160, 190, 170, 60, lambda lz, iso: G.persona(lz, iso, 186, 168, t, "oficial", dir=(0.3, 1), seed=5721, h=54, accion="vitorea"), fijo=False, clave=355)
        m.add(240, 160, 250, 170, 60, lambda lz, iso: G.persona(lz, iso, 246, 168, t, "dragon", dir=(-0.3, 1), seed=5722, h=54, accion="vitorea"), fijo=False, clave=415)
        mu = G.Multitud()
        tipos = ("insurgente", "campesino", "indigena", "insurgente_lanza", "campesina", "mestizo", "honda", "indigena_f")
        for i in range(52):
            ang = 3.14 * h01(41, i)
            rad = 40 + 120 * h01(42, i)
            x, y = 215 + rad * math.cos(ang) * 1.3, 205 + rad * math.sin(ang) * 0.9
            mu.quieto((x, y), tipos[i % 8], dir=(215 - x, 165 - y), seed=5900 + i, h=40, accion=("vitorea" if t > t_grito + (0.1 * h01(43, i)) and i % 2 == 0 else ("pelea" if i % 3 == 0 and t > t_arm - 0.3 else None)))
        mu.dibujar(m, t)
        m.dibujar(lz, iso)
        hx, hy = iso.P(215, 165, 74)
        for g in range(5):
            tg = t_grito + 0.15 + 0.5 * g
            if tg < t < tg + 1.1 and t < t_arm + 0.4:
                U.ondas_sonoras(lz, float(hx), float(hy), t, tg, dur=1.0, r1=330, n=1, color=(255, 236, 170), ancho=5.0, periodo=0.25, alfa=0.7)
        t01.aves(lz, t, t_grito + 0.1, (float(hx), float(hy) - 30), 12)
    # rótulos
    k = U.pop(t, t_grito - 0.1, 1.2) * U.salida(t, t_disc - 0.2, 0.3)
    if k > 0.01:
        P.rotulo(lz, W / 2, 170, "EL GRITO DE DOLORES", px=int(124 * (0.94 + 0.06 * k)), k=k, color=(255, 255, 255))
    kmh = U.pop(t, t_grito - 0.1) * U.salida(t, t_arm + 0.6, 0.25)
    if kmh > 0.01:
        MD.medallon(lz, 1690, 330, 150, "hidalgo", t, emocion="enojo", habla=1.0, k=kmh, seed=2)
        U.llamada(lz, 1690, 510, "Miguel Hidalgo", color=U.COL["morado"], px=44, k=kmh, cola="arriba")
    ks = U.pop(t, t_disc - 0.1) * U.salida(t, t_llm - 0.15, 0.25)
    if ks > 0.01:
        U.pergamino_grande(lz, 560, 520, 520, 280, t, t_disc - 0.1, lineas=("Señores, el día...", "de hoy llegó", "—"), titulo="DISCURSO", sello=False, rot=-0.06)
        if t > t_escr_x():
            u = prog(t, t_escr_x(), t_escr_x() + 0.35)
            lz.trazo(np.array([[400, 400], [400 + 320 * u, 400 + 240 * u]]), (226, 40, 60), 20, afinar=False, temblor=0.0, capa=2)
            lz.trazo(np.array([[720, 400], [720 - 320 * u, 400 + 240 * u]]), (226, 40, 60), 20, afinar=False, temblor=0.0, capa=2)
        U.llamada(lz, 560, 690, "no fue un discurso escrito", color=U.COL["morado"], px=44, k=ks, cola="arriba")
    ka = U.pop(t, t_llm - 0.1)
    if ka > 0.01:
        U.llamada(lz, W / 2, 960, "¡una llamada a las armas!", color=U.COL["rojo"], px=84, k=ka * U.repop(t, t_arm + 0.1), cola=None)
        _espadas2(lz, 330, 400, 1.3, ka)


def _tarima_atrio(lz, iso):
    I.caja(lz, iso, 200, 152, 30, 26, 8, (206, 170, 130))
    I.caja(lz, iso, 202, 154, 26, 22, 2, (232, 204, 160), z0=8)


def t_escr_x():
    return t_escr + 0.2


def _espadas2(lz, x, y, s=1.0, k=1.0, col=(238, 240, 250)):
    for sg in (-1, 1):
        p0 = np.array([x - sg * 70 * s * k, y - 70 * s * k])
        p1 = np.array([x + sg * 70 * s * k, y + 70 * s * k])
        lz.trazo(np.array([p0, p1]), col, 12 * s * k, afinar=False, temblor=0.0, capa=2)
        gx, gy = x - sg * 30 * s * k, y - 30 * s * k
        lz.trazo(np.array([[gx - 22 * s * k, gy + sg * 22 * s * k], [gx + 22 * s * k, gy - sg * 22 * s * k]]), (250, 206, 70), 9 * s * k, afinar=False, temblor=0.0, capa=2)
    lz.halo(x, y, 200 * s * k, (255, 220, 120), alfa=0.28 * k, capa=0)
