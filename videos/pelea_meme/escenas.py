# -*- coding: utf-8 -*-
"""UN HOMBRE CONTRA CINCO CRIATURAS — estilo `guache`, plano secuencia.

Un solo mundo continuo (desierto -> selva -> océano -> Luna -> volcán): la cámara corre con Don Beto de una ronda a
la siguiente (`X0(t)`), sin cortes. Cada golpe está anclado a una palabra de la narración (`T(id, palabra)`).
Coordenadas: mundo en px de 1080p; el bioma k ocupa x en [1920k, 1920(k+1)]; el héroe va fijo en pantalla (x=HX)
y el suelo está en GY. Todo es función del tiempo global `t`.
"""
import math
import types

import cv2
import numpy as np

import guache as G
from escena_base import *  # noqa: F401,F403
from motor import (H, W, Lienzo, componer, e_back, e_in, e_inout, e_out, h01, lerp, mat_r, mat_s, mat_t, prog,
                   smooth)

_ESC = {e["id"]: e for e in TL["escenas"]}
TOTAL = TL["total"]
C = G.C
GY = 812.0            # suelo
HX = 520.0            # x del héroe en pantalla
HS = 1.45             # escala del héroe
BASE = [G.BIOMA_W * k for k in range(5)]
RONDAS = ["r1", "r2", "r3", "r4", "r5"]


def T(eid, texto, **kw):
    return Escena.w(types.SimpleNamespace(fr=_ESC[eid]["frases"], id=eid), texto, **kw)


def INI(eid, i=0):
    return _ESC[eid]["frases"][i]["t0"]


def FIN(eid, i=-1):
    return _ESC[eid]["frases"][i]["t1"]


def kf(t, pts, f=smooth):
    """Interpolación por claves [(t0, v0), (t1, v1), ...] con suavizado f (v puede ser número)."""
    if t <= pts[0][0]:
        return pts[0][1]
    for (ta, va), (tb, vb) in zip(pts, pts[1:]):
        if t < tb:
            return va + (vb - va) * f(prog(t, ta, tb))
    return pts[-1][1]


def bal(t, t0, t1, p0, p1, alto=0.0):
    """Trayectoria parabólica de p0 a p1 entre t0 y t1 (alto = altura extra del arco). Devuelve (x, y, u)."""
    u = min(1.0, max(0.0, (t - t0) / (t1 - t0)))
    return (p0[0] + (p1[0] - p0[0]) * u, p0[1] + (p1[1] - p0[1]) * u - 4 * alto * u * (1 - u), u)


# ------------------------------------------------------------------ anclas
# intro
t_hombre, t_normal, t_cinco, t_crias, t_una = (T("intro", "hombre"), T("intro", "normal"), T("intro", "cinco"),
                                                T("intro", "criaturas"), T("intro", "una"))
# ronda 1
t1_esc, t1_gig = T("r1", "escorpion"), T("r1", "gigante")
t1_saca, t1_secreta, t1_chancla = T("r1", "saca"), T("r1", "secreta"), T("r1", "chancla", frase=2)
t1_chanclazo, t1_nocaut = T("r1", "chanclazo", frase=3), T("r1", "nocaut", frase=3)
# ronda 2
t2_trex, t2_brac, t2_ridi = T("r2", "tiranosaurio"), T("r2", "bracitos"), T("r2", "ridiculos")
t2_resp, t2_sar = T("r2", "responde"), T("r2", "sarten", frase=2)
t2_sartenazo, t2_nocaut = T("r2", "sartenazo", frase=3), T("r2", "nocaut", frase=3)
# ronda 3
t3_tib, t3_gig = T("r3", "tiburon"), T("r3", "gigante")
t3_contra, t3_pez, t3_esp = T("r3", "contraataca"), T("r3", "pez"), T("r3", "espada", frase=2)
t3_esgr, t3_mar, t3_nocaut = T("r3", "duelo", frase=3), T("r3", "espadas", frase=3), T("r3", "nocaut", frase=3)
# ronda 4
t4_alien, t4_plat = T("r4", "extraterrestre"), T("r4", "platillo")
t4_solo, t4_ext, t4_cohete = T("r4", "solo"), T("r4", "extintor", frase=2), T("r4", "cohete")
t4_adios, t4_nocaut = T("r4", "adios"), T("r4", "nocaut", frase=3)
# ronda 5
t5_dragon, t5_cubre, t5_tapa = T("r5", "dragon"), T("r5", "cubre"), T("r5", "tapa")
t5_y, t5_chancla, t5_regresa, t5_nocaut = T("r5", "entonces"), T("r5", "chancla", frase=3), T("r5", "regresa"), T("r5", "nocaut", frase=3)
# cierre
tc_marcador, tc_hombre, tc_cinco, tc_crias, tc_cero = (T("cierre", "marcador"), T("cierre", "hombre"), T("cierre", "cinco"),
                                                        T("cierre", "criaturas"), T("cierre", "cero"))
tc_nunca, tc_chancla = T("cierre", "nunca"), T("cierre", "chancla", frase=1)

PAN_DUR = 1.9
PAN0 = [None] + [INI(RONDAS[i], 0) - 0.35 for i in range(1, 5)]      # inicio de la carrera hacia la ronda i+1


def X0_de(t):
    x = 0.0
    for i in range(1, 5):
        x += G.BIOMA_W * e_inout(prog(t, PAN0[i], PAN0[i] + PAN_DUR))
    return x


def panning(t):
    return any(PAN0[i] <= t < PAN0[i] + PAN_DUR for i in range(1, 5))


T_PELEA = {r: FIN(r, 1) - 0.1 for r in RONDAS}

# momentos de impacto (cámara: sacudida y "golpe" de zoom) y tiempos derivados
IMP1 = t1_chanclazo + 0.30
IMP2 = t2_sartenazo + 0.06
IMP3 = t3_nocaut - 0.32
IMP4 = t4_adios
IMP5 = t5_regresa + 0.05
GOLPES = [(IMP1, 22, 0.35), (IMP2, 30, 0.45), (IMP3, 20, 0.35), (IMP4, 26, 0.4), (IMP5, 34, 0.55),
          (t1_nocaut, 12, 0.3), (t2_nocaut, 26, 0.5), (t4_nocaut, 16, 0.4), (t5_nocaut + 0.35, 24, 0.6)]
KOS = [t1_nocaut, t2_nocaut, t3_nocaut, t4_nocaut, t5_nocaut]


def camara(t):
    z, dx, dy = 1.0, 0.0, 0.0
    for t0, amp, dur in GOLPES:
        u = t - t0
        if 0 <= u < dur:
            q = u / dur
            dx += amp * math.exp(-q * 4) * math.sin(u * 95)
            dy += amp * 0.7 * math.exp(-q * 4) * math.sin(u * 83 + 1)
            z += 0.045 * math.exp(-q * 5) * (1 if amp < 30 else 1.4)
    # pasos del tiranosaurio (temblor del suelo)
    if t2_trex - 0.6 < t < t2_brac:
        dy += 5 * abs(math.sin((t - t2_trex) * 7.2))
    if t5_dragon - 0.5 < t < t5_dragon + 1.6:
        dx += 6 * math.sin(t * 55)
        dy += 5 * math.sin(t * 47)
    # empujón hacia el héroe en momentos dramáticos
    z += 0.05 * smooth(prog(t, t1_saca, t1_chancla)) * (1 - prog(t, t1_chancla, t1_chancla + 0.3))
    z += 0.05 * smooth(prog(t, t5_y - 0.2, t5_chancla)) * (1 - prog(t, t5_chancla, t5_chancla + 0.3))
    return z, dx, dy


# ------------------------------------------------------------------ héroe
def _idle_brazos(t):
    b = math.sin(t * 3.1)
    return (1.42 + 0.03 * b, 1.55 + 0.04 * b), (1.68 - 0.03 * b, 1.6)


def pose_heroe(t):
    """Devuelve (dict de parámetros de G.hombre, dx_mundo, dy_salto)."""
    p = dict(cara="normal", paso=0.0, inc=0.0, agach=0.0, sq=1.0, sudor=0.0, casco=0.0, arma_f=None, arma_b=None)
    bf, bb = _idle_brazos(t)
    p["brazo_f"], p["brazo_b"] = bf, bb
    dx, dy = 0.0, 0.0
    X0 = X0_de(t)
    # ---- intro + ronda 1
    if t < PAN0[1]:
        p["cara"] = "sonrisa" if t < t1_esc else "normal"
        if t < 1.15:                                                  # entra corriendo desde la izquierda
            kk = 1 - smooth(prog(t, 0.9, 1.15))
            dx = -760 * (1 - e_out(prog(t, 0.0, 1.15)))
            ph_ = (dx * 2 * math.pi / 330.0)
            p["paso"] = kk
            p["inc"] = 0.14 * kk
            p["brazo_f"] = (0.9 + 0.9 * math.sin(ph_), 1.2 + 0.6 * math.sin(ph_))
            p["brazo_b"] = (0.9 - 0.9 * math.sin(ph_), 1.2 - 0.6 * math.sin(ph_))
        if max(1.15, t_hombre - 0.1) < t < max(1.15, t_normal) + 0.6:   # saluda
            w = math.sin(t * 9)
            p["brazo_f"] = (-0.9 + 0.25 * w, -1.5 + 0.55 * w)
            p["cara"] = "sonrisa"
        if INI("r1", 0) < t < t1_esc - 0.4:
            p["cara"] = "brava"
        if t1_gig - 0.3 < t < t1_saca:
            p["cara"] = "miedo"
            p["sudor"] = 1.0
        # el picotazo: salta hacia atrás
        if t >= t1_secreta - 0.15:
            dx = kf(t, [(t1_secreta - 0.15, 0), (t1_secreta + 0.35, -190), (t1_nocaut + 0.6, -190), (PAN0[1] - 0.05, 0)])
        salto = bal(t, t1_secreta - 0.1, t1_secreta + 0.55, (0, 0), (0, 0), 150)
        dy = salto[1]
        if t1_secreta - 0.1 < t < t1_secreta + 0.55:
            p["cara"] = "grito"
            p["brazo_f"] = (-1.0, -1.6)
            p["brazo_b"] = (-2.2, -1.9)
            p["inc"] = -0.12
        # saca la chancla
        if t1_saca < t < t1_chanclazo - 0.25:
            u = prog(t, t1_saca, t1_chancla)
            p["agach"] = 0.5 * (1 - prog(t, t1_chancla - 0.2, t1_chancla))
            p["brazo_f"] = (lerp(1.4, -0.7, e_back(u)), lerp(1.5, -1.25, e_back(u)))
            p["arma_f"] = G.chancla if t >= t1_chancla - 0.12 else None
            p["cara"] = "brava"
        # lanzamiento
        if t1_chanclazo - 0.28 <= t < t1_chanclazo + 0.6:
            u = prog(t, t1_chanclazo - 0.28, t1_chanclazo)
            v = prog(t, t1_chanclazo, t1_chanclazo + 0.12)
            a1 = lerp(-0.7, -2.5, smooth(u)) if v <= 0 else lerp(-2.5, 0.05, e_out(v))
            a2 = lerp(-1.25, -3.0, smooth(u)) if v <= 0 else lerp(-3.0, -0.1, e_out(v))
            p["brazo_f"] = (a1, a2)
            p["arma_f"] = G.chancla if t < t1_chanclazo else None
            p["inc"] = -0.16 * smooth(u) + 0.3 * e_out(v) * (1 - prog(t, t1_chanclazo + 0.15, t1_chanclazo + 0.5))
            p["agach"] = 0.3 * smooth(u) * (1 - v)
            p["cara"] = "esfuerzo" if t < t1_chanclazo + 0.15 else "grito"
        if t >= t1_nocaut - 0.1 and t < PAN0[1] - 0.05:
            p["cara"] = "victoria"
            p["brazo_f"] = (-1.2 + 0.15 * math.sin(t * 8), -1.45)
            p["brazo_b"] = (1.6, 1.7)
    else:
        pass
    # ---- carreras (paneo)
    for i in range(1, 5):
        if PAN0[i] <= t < PAN0[i] + PAN_DUR + 0.25:
            k = smooth(prog(t, PAN0[i], PAN0[i] + 0.25)) * (1 - smooth(prog(t, PAN0[i] + PAN_DUR - 0.2, PAN0[i] + PAN_DUR + 0.25)))
            p["paso"] = k
            p["inc"] = 0.16 * k
            p["cara"] = "esfuerzo" if k > 0.5 else p["cara"]
            p["brazo_f"] = (lerp(p["brazo_f"][0], 0.9 + 0.9 * math.sin(X0 * 2 * math.pi / 330), k), lerp(p["brazo_f"][1], 1.2 + 0.6 * math.sin(X0 * 2 * math.pi / 330), k))
            p["brazo_b"] = (lerp(p["brazo_b"][0], 0.9 - 0.9 * math.sin(X0 * 2 * math.pi / 330), k), lerp(p["brazo_b"][1], 1.2 - 0.6 * math.sin(X0 * 2 * math.pi / 330), k))
            p["arma_f"] = None
    # ---- ronda 2
    if PAN0[1] + PAN_DUR <= t < PAN0[2]:
        p["cara"] = "normal"
        if t2_ridi - 0.3 < t < t2_resp - 0.35:
            p["cara"] = "sonrisa"                                   # no le teme a los bracitos
        if t2_brac - 0.1 < t < t2_ridi:
            p["cara"] = "asombro"
        dx = kf(t, [(t2_sartenazo - 0.4, 0), (IMP2 - 0.02, 170), (t2_nocaut + 0.5, 170), (PAN0[2] - 0.05, 0)])
        if t >= t2_nocaut + 0.5:
            p["cara"] = "victoria"
            p["arma_f"] = G.sarten
            p["brazo_f"] = (-1.2 + 0.1 * math.sin(t * 8), -1.4)
        if t2_resp - 0.35 < t < t2_sar:
            u = smooth(prog(t, t2_resp - 0.35, t2_resp - 0.1))
            p["agach"] = 0.95 * u
            p["cara"] = "miedo"
            p["sudor"] = 1.0
            p["brazo_f"] = (lerp(p["brazo_f"][0], 0.2, u), lerp(p["brazo_f"][1], -0.8, u))
            p["brazo_b"] = (lerp(p["brazo_b"][0], 0.1, u), lerp(p["brazo_b"][1], -0.7, u))
        if t2_sar <= t < t2_sartenazo - 0.32:
            u = e_back(prog(t, t2_sar, t2_sar + 0.35))
            p["brazo_f"] = (lerp(0.2, -0.5, u), lerp(-0.8, -1.0, u))
            p["arma_f"] = G.sarten
            p["cara"] = "brava"
            p["agach"] = 0.5 * (1 - prog(t, t2_sar, t2_sar + 0.3))
        if t2_sartenazo - 0.32 <= t < t2_nocaut + 0.5 and t < PAN0[2]:
            u = prog(t, t2_sartenazo - 0.32, t2_sartenazo - 0.02)            # subida
            v = prog(t, t2_sartenazo - 0.02, IMP2)                          # golpe
            arriba = bal(t, t2_sartenazo - 0.34, IMP2 + 0.4, (0, 0), (0, 0), 260)
            dy = arriba[1] if t < IMP2 + 0.4 else 0.0
            p["arma_f"] = G.sarten
            p["brazo_f"] = (lerp(-0.5, -2.7, smooth(u)) if v <= 0 else lerp(-2.7, 1.0, e_out(v)),
                            lerp(-1.0, -3.0, smooth(u)) if v <= 0 else lerp(-3.0, 0.4, e_out(v)))
            p["cara"] = "grito"
            p["inc"] = 0.1 + 0.15 * v
            if t > IMP2 + 0.45:
                p["cara"] = "victoria"
                p["arma_f"] = G.sarten
                p["brazo_f"] = (-1.2 + 0.1 * math.sin(t * 8), -1.4)
                p["inc"] = 0.0
    # ---- ronda 3 (balsa)
    if PAN0[2] + PAN_DUR <= t < PAN0[3]:
        p["cara"] = "normal"
        if t3_tib - 0.05 < t < t3_contra:
            p["cara"] = "miedo"
            p["sudor"] = 1.0
        if t3_contra - 0.1 < t < t3_pez:
            p["cara"] = "grito"
            p["agach"] = 0.5
            p["brazo_f"] = (0.6, -0.6)
            p["brazo_b"] = (0.4, -0.5)
        if t3_pez <= t < t3_nocaut + 0.9:
            catch = t3_pez + 0.5
            u = e_back(prog(t, t3_pez + 0.15, catch))
            p["arma_f"] = G.pez_espada if t >= catch - 0.1 else None
            p["brazo_f"] = (lerp(0.6, -0.1, u), lerp(-0.6, -0.05, u))
            p["cara"] = "brava"
            p["agach"] = 0.3
            p["brazo_b"] = (2.0, 1.8)
            # esgrima: estocadas
            if t >= t3_esp - 0.05:
                p["agach"] = 0.35
                ests = [t3_esp + 0.1, t3_esgr + 0.0, t3_esgr + 0.32, t3_mar + 0.05, IMP3 - 0.02]
                lim = 0.0
                for te in ests:
                    lim = max(lim, math.exp(-abs(t - (te + 0.05)) * 9) * 1.0) if te - 0.25 < t < te + 0.3 else lim
                p["brazo_f"] = (lerp(-0.25, 0.05, lim), lerp(-0.15, -0.08, lim))
                dx = 70 * lim
                p["inc"] = 0.2 * lim
                p["cara"] = "esfuerzo"
        if t >= t3_nocaut + 0.2:
            p["cara"] = "victoria"
            p["arma_f"] = G.pez_espada
            p["brazo_f"] = (-1.15, -1.5)
            p["agach"] = 0.0
            dx = 0.0
    # ---- ronda 4 (Luna)
    if PAN0[3] + PAN_DUR <= t < PAN0[4]:
        p["casco"] = e_back(prog(t, PAN0[3] + PAN_DUR - 0.2, PAN0[3] + PAN_DUR + 0.35))
        p["cara"] = "asombro" if t < t4_alien + 0.4 else "normal"
        if t4_alien + 0.4 <= t < t4_solo:
            p["cara"] = "brava"
        elif t >= t4_solo:
            # rayo tractor y cohete
            levit = kf(t, [(t4_solo, 0), (t4_solo + 0.9, 120), (t4_cohete, 120), (t4_cohete + 0.5, 185)], smooth)
            dy = -levit
            if t < t4_cohete:
                p["cara"] = "miedo"
                p["sudor"] = 1.0
                w = math.sin(t * 14)
                p["brazo_f"] = (-0.6 + 0.4 * w, -1.0 + 0.5 * w)
                p["brazo_b"] = (-2.0 - 0.4 * w, -2.4 - 0.4 * w)
                p["paso"] = 0.0
            if t4_ext <= t < t4_adios + 0.2:
                u = e_back(prog(t, t4_ext, t4_ext + 0.3))
                p["arma_f"] = G.extintor
                p["brazo_f"] = (lerp(-0.6, 1.9, u), lerp(-1.0, 1.75, u))          # apunta hacia abajo
                p["cara"] = "brava" if t < t4_cohete else "esfuerzo"
                p["brazo_b"] = (2.0, 1.9)
                p["inc"] = 0.0
            if t >= t4_adios + 0.15:
                p["arma_f"] = G.extintor
                p["brazo_f"] = (-0.2, -0.3)
                p["cara"] = "grito" if t < t4_nocaut else "victoria"
            if t >= t4_adios + 0.2:                                   # cae despacio (poca gravedad)
                dy = -kf(t, [(t4_adios + 0.2, 185), (t4_adios + 1.2, 0)], e_in)
                if t > t4_adios + 1.2:
                    dy = 0.0
                    p["brazo_f"] = (-1.2 + 0.1 * math.sin(t * 8), -1.45)
    # ---- ronda 5 (volcán)
    if PAN0[4] + PAN_DUR <= t:
        p["casco"] = 1.0 - e_in(prog(t, PAN0[4] + 0.15, PAN0[4] + 0.6)) if t < PAN0[4] + 0.6 else 0.0
        p["cara"] = "normal"
        if t < t5_dragon + 0.3:
            p["cara"] = "miedo" if t > t5_dragon - 0.3 else "normal"
            p["sudor"] = 1.0 if t > t5_dragon - 0.3 else 0.0
        if t5_cubre - 0.5 <= t < t5_y:
            p["cara"] = "miedo"
            p["sudor"] = 1.0
            p["agach"] = 0.35
            dx = -70 * smooth(prog(t, t5_cubre - 0.2, t5_cubre + 0.4)) + 3 * math.sin(t * 45)
            u = e_back(prog(t, t5_tapa - 0.05, t5_tapa + 0.3))
            p["brazo_f"] = (lerp(0.4, 0.05, u), lerp(-0.2, 0.0, u)) if t >= t5_tapa - 0.05 else (0.4, -0.2)
            p["arma_f"] = G.tapa_olla if t >= t5_tapa - 0.05 else None
        if t5_y <= t < t5_regresa - 0.2:
            p["cara"] = "asombro" if t > t5_chancla else "esfuerzo"
            p["agach"] = 0.3
            dx = -70
            p["arma_f"] = G.tapa_olla
            p["brazo_f"] = (0.05, 0.0)
            p["sudor"] = 1.0
        if t >= t5_regresa - 0.2:
            dx = kf(t, [(t5_regresa - 0.2, -70), (t5_regresa + 0.5, 0)])
            p["cara"] = "victoria" if t > t5_regresa + 0.5 else "asombro"
            p["brazo_f"] = (-1.2 + 0.1 * math.sin(t * 8), -1.4)
            if t >= t_chancla_mano():
                p["arma_f"] = G.chancla
    return p, dx, dy


def t_chancla_mano():
    return IMP5 + 0.95


def hero_hands_world(hx, hy, s, hands, key="f"):
    lx, ly, ang = hands[key]
    return hx + lx * s, hy + ly * s, ang


# ------------------------------------------------------------------ criaturas y escenario por ronda
def raft_y(t):
    return 8 * math.sin(t * 2.2)


def dibujar_r1(lz, t, X0):
    """Desierto: cactus + escorpión; devuelve nada (el héroe se dibuja aparte)."""
    b = BASE[0]
    if X0 > b + 2300:
        return
    # cactus de primer plano (se mueven con el mundo)
    for i, (cx, s) in enumerate(((240, 1.0), (1000, 0.8), (1650, 1.15))):
        x = b + cx
        cactus(lz, x, GY + 46 + 14 * i, s)
    # escorpión
    esc = t1_esc
    if t < esc - 0.9:
        return
    hitv = t >= IMP1
    if not hitv:
        xin = kf(t, [(esc - 0.9, b + 2250), (t1_gig + 0.1, b + 1390), (t1_secreta - 0.7, b + 1390), (t1_secreta - 0.05, b + 850)], smooth)
        moving = (esc - 0.9 < t < t1_gig + 0.1) or (t1_secreta - 0.7 < t < t1_secreta - 0.05)
        cola = kf(t, [(t1_gig + 0.1, 0.0), (t1_secreta - 0.35, 0.05), (t1_secreta + 0.02, 1.0), (t1_secreta + 0.55, 1.0), (t1_secreta + 0.95, 0.3),
                      (t1_chanclazo, 0.5)])
        cola += 0.06 * math.sin(t * 5)
        G.escorpion(lz, xin, GY + 6, 1.6, t, mirar=-1, ph=t * 16, paso=1.0 if moving else 0.25, cola=cola,
                    pinza=0.4 + 0.4 * math.sin(t * 6), larga=1.35 if cola > 0.5 else 1.0, sq=1.0)
        if 0 <= t - (t1_secreta + 0.02) < 0.35:
            G.polvo(lz, b + 850 - 300, GY + 20, t, t1_secreta + 0.04, n=7, r=44)
        if moving and int(t * 8) % 2 == 0:
            pass
        if esc - 0.9 < t < t1_gig + 0.1:
            G.polvo(lz, xin + 100, GY + 10, t, math.floor(t * 5) / 5.0, n=4, r=30, dur=0.5, alcance=60)
    else:
        # lanzado por la chancla, cae boca arriba lejos
        p0 = (b + 850 - 105, GY - 135)
        p1 = (b + 1560, GY - 20)
        x, y, u = bal(t, IMP1, t1_nocaut, p0, p1, 260)
        rot = -2 * math.pi * 2 * e_out(u) - math.pi * 1.0 * (1 - 0) if False else -(2 * math.pi * 1.5) * u
        if t >= t1_nocaut:
            rot = -math.pi * 3
            y = GY - 20 - 14 * abs(math.sin((t - t1_nocaut) * 9)) * math.exp(-(t - t1_nocaut) * 5)
        # al girar 1,5 vueltas queda boca abajo (pi)
        G.escorpion(lz, x, y, 1.6, t, mirar=-1, ph=0, paso=0.0, cola=0.35, pinza=0.7,
                    ko=t > IMP1 + 0.25, rot=rot, ceja=0.0)
        if t >= t1_nocaut:
            G.estrellitas(lz, x + 10, y - 100, t, 90, 4, 1.4)
            G.polvo(lz, x - 40, GY + 8, t, t1_nocaut, n=8, r=50, alcance=130)
    # chancla en vuelo / rebote
    ch = None
    if t1_chanclazo <= t < IMP1:
        hx = b + HX - 190 + 110
        x, y, u = bal(t, t1_chanclazo, IMP1, (hx + 60, GY - 330), (b + 850 - 105, GY - 135), 60)
        ch = (x, y, t * 26)
    elif IMP1 <= t < IMP1 + 1.0:
        x, y, u = bal(t, IMP1, IMP1 + 1.0, (b + 850 - 105, GY - 135), (b + 1500, -260), 260)
        ch = (x, y, t * 22)
    if ch:
        G.chancla(lz, ch[0], ch[1], ch[2], 1.1)
        if t1_chanclazo <= t < IMP1:
            G.lineas_vel(lz, ch[0], ch[1], math.atan2(-90, 500), 160, 3, t, 0.5)
    if IMP1 - 0.03 <= t < IMP1 + 0.55:
        u = (t - (IMP1 - 0.03)) / 0.55
        G.explosion(lz, b + 850 - 120, GY - 140, u, 170, seed=3)
        G.ono(lz, "¡CHANCLAZO!", b + 850 + 30, GY - 470, t, IMP1, dur=1.2, px=132, col=C["rojo"])


def cactus(lz, x, y, s=1.0):
    col = (104, 140, 92)
    with lz.grupo(x, y, s):
        G.cap(lz, 0, 0, 0, -230, 60, 54, col)
        G.cap(lz, -8, -110, -70, -110, 26, 26, col, sombra=False)
        G.cap(lz, -70, -110, -70, -170, 26, 26, col, sombra=False)
        G.cap(lz, 8, -140, 66, -140, 26, 26, col, sombra=False)
        G.cap(lz, 66, -140, 66, -200, 26, 26, col, sombra=False)
        for k in range(5):
            G.disco(lz, -10 + 5 * k, -40 - 42 * k, 2.8, C["crema"], sombra=False)
        G.disco(lz, 0, -238, 14, C["rosa"], sombra=False)


def arbusto(lz, x, y, s=1.0, col=(70, 108, 76), t=0.0):
    with lz.grupo(x, y, s):
        for i, (ox, oy, r) in enumerate(((-60, -30, 42), (0, -46, 56), (58, -30, 44))):
            G.disco(lz, ox + 2 * math.sin(t * 2 + i), oy, r, col)


def hoja_grande(lz, x, y, s, ang, t, col=(60, 104, 76), fase=0.0):
    a = ang + 0.05 * math.sin(t * 1.7 + fase)
    with lz.grupo(x, y, s, rot=a):
        P = np.array([(0, 0), (60, -50), (170, -60), (280, -10), (170, 40), (60, 40)], float)
        G.sombreado(lz, G.catmull(P, 8, True), col, k=0.08)
        lz.relleno(G.capsula(0, -2, 250, -12, 6), G.ton(col, 0.35))


def dibujar_r2(lz, t, X0):
    b = BASE[1]
    if not (b - 2100 < X0 < b + 2300):
        return
    for i, (cx, s) in enumerate(((320, 1.2), (980, 1.0), (1700, 1.3))):
        arbusto(lz, b + cx, GY + 60 + 10 * i, s, (62, 100, 70), t)
    for i, (cx, a) in enumerate(((60, -0.4), (1260, -2.6), (1560, -0.6))):
        hoja_grande(lz, b + cx, GY + 140, 1.3, a, t, fase=i)
    tr = t2_trex
    if t < tr - 0.9:
        return
    ph = t * 7.2
    if t < IMP2:
        xin = kf(t, [(tr - 0.9, b + 2350), (t2_brac - 0.25, b + 1480), (t2_ridi + 0.15, b + 1250), (t2_resp - 0.05, b + 1250),
                     (t2_resp + 0.3, b + 1010)], smooth)
        caminando = (tr - 0.9 < t < t2_brac - 0.25) or (t2_resp - 0.05 < t < t2_resp + 0.3) or (t2_ridi - 0.4 < t < t2_ridi + 0.15)
        boca = 0.0
        if t2_resp - 0.25 < t < t2_sar + 0.2:
            boca = 0.5 + 0.5 * abs(math.sin(t * 16))
        if tr - 0.05 < t < tr + 0.7:
            boca = 1.0
        brazos = 1.0 if t2_brac - 0.1 <= t < t2_sar else 0.0
        cabeza = 0.25 * math.sin(t * 5) * (1 if t2_ridi - 0.3 < t < t2_resp else 0.0)
        cabeza += 0.5 * smooth(prog(t, t2_resp - 0.3, t2_resp + 0.1)) * (1 - smooth(prog(t, t2_resp + 0.1, t2_resp + 0.6)))
        G.trex(lz, xin, GY + 4, 1.5, t, mirar=-1, ph=ph, paso=1.0 if caminando else 0.0, boca=boca, brazos=brazos,
               cabeza=cabeza)
        if t2_brac <= t < t2_ridi + 0.5:
            # nota señalando los bracitos
            u = G.e_back(min(1, (t - t2_brac) / 0.3)) if hasattr(G, "e_back") else 1
            chip(lz, xin - 300, GY - 200, "BRAZOS DE JUGUETE", u, 34, C["crema"], G.TINTA)
    else:
        u = t - IMP2
        base_x = b + 1010
        cab = 0.9 * smooth(prog(t, IMP2, IMP2 + 0.3))
        caida = e_in(prog(t, IMP2 + 0.25, t2_nocaut)) * 1.45
        rot = caida
        sq = 1.0 - 0.18 * math.exp(-u * 9) * math.cos(u * 40) if u < 0.5 else 1.0
        G.trex(lz, base_x, GY + 4, 1.5, t, mirar=-1, ph=0, paso=0.0, boca=0.35, brazos=0.0, cabeza=cab, ko=True, sq=sq,
               rot=rot, estrellas=(t > t2_nocaut - 0.05), ceja=0.0)
        if t >= t2_nocaut:
            G.polvo(lz, base_x + 320, GY + 10, t, t2_nocaut, n=9, r=56, alcance=180)
    if IMP2 - 0.02 <= t < IMP2 + 0.55:
        G.explosion(lz, b + 880, GY - 330, (t - (IMP2 - 0.02)) / 0.55, 180, seed=5)
        G.ono(lz, "¡BONK!", b + 1010, GY - 640, t, IMP2, dur=1.2, px=150, col=C["mostaza"])
        G.estrellitas(lz, b + 880, GY - 400, t, 90, 4, 1.4, alfa=prog(t, IMP2 + 0.1, IMP2 + 0.2))


def dibujar_r3(lz, t, X0):
    b = BASE[2]
    if not (b - 2100 < X0 < b + 2300):
        return
    # muelle de madera que cruza todo el océano (la carrera continúa sobre él)
    muelle(lz, b, b + G.BIOMA_W - 70)
    # aleta de tiburón acercándose
    tib = t3_tib
    sea_y = GY + 20
    if tib - 1.0 < t < t3_contra - 0.1:
        x = kf(t, [(tib - 1.0, b + 2100), (t3_gig + 0.3, b + 1200), (t3_contra - 0.1, b + 1010)], smooth)
        aleta(lz, x, sea_y, t, 1.0)
        estela(lz, x + 40, sea_y + 6, t)
    # salto del tiburón y esgrima
    if t3_contra - 0.1 <= t < IMP3:
        if t < t3_esp - 0.05:
            x, y, u = bal(t, t3_contra - 0.1, t3_esp - 0.05, (b + 1010, sea_y + 20), (b + 830, GY - 260), 380)
            rot = -0.9 * math.sin(u * math.pi) * 0.9 + 0.0
            boca = 0.9
        else:
            # rebote de la primera estocada y luego combate cuerpo a cuerpo
            ests = [t3_esp + 0.1, t3_esgr + 0.0, t3_esgr + 0.32, t3_mar + 0.05]
            ph_ = t - t3_esp
            x, y, u = bal(t, t3_esp - 0.05, t3_esp + 0.5, (b + 830, GY - 260), (b + 1040, sea_y - 60), 120)
            if t >= t3_esp + 0.5:
                x = b + 1040 - 40 * abs(math.sin((t - t3_esp) * 5))
                y = sea_y - 90 - 40 * abs(math.sin((t - t3_esp) * 6.2))
            rot = -0.3 + 0.35 * math.sin((t - t3_esp) * 7)
            boca = 0.4 + 0.6 * abs(math.sin((t - t3_esp) * 9))
        G.tiburon(lz, x, y, 1.3, t, mirar=-1, boca=boca, rot=rot)
        if t3_esp - 0.04 <= t < t3_esp + 0.6:
            G.salpicadura(lz, b + 1040, sea_y, t, t3_esp + 0.3, n=8, alto=170)
    if t >= IMP3:
        xf, yf = b + 1360, sea_y - 40
        x, y, u = bal(t, IMP3, t3_nocaut + 0.4, (b + 1040 - 40, sea_y - 90), (xf, yf), 380)
        if t < t3_nocaut + 0.4:
            rot = -(2 * math.pi * 1.5) * u
            G.tiburon(lz, x, y, 1.3, t, mirar=-1, boca=0.8, rot=rot, ko=u > 0.2, ceja=0.0)
        else:
            flot = 6 * math.sin(t * 2.5)
            G.tiburon(lz, xf, yf + flot, 1.3, t, mirar=-1, boca=0.3, rot=-math.pi * 3, ko=True, ceja=0.0)
            G.estrellitas(lz, xf, yf - 150, t, 100, 4, 1.4)
    if t3_nocaut + 0.38 <= t < t3_nocaut + 1.4:
        G.salpicadura(lz, b + 1360, sea_y - 30, t, t3_nocaut + 0.4, n=12, alto=260)
    # pez espada saltando hacia la mano
    if t3_pez <= t < t3_pez + 0.5:
        hx = b + HX + 100
        x, y, u = bal(t, t3_pez, t3_pez + 0.5, (b + 700, sea_y + 30), (hx + 110, GY - 260), 200)
        G.pez_espada(lz, x, y, -0.3 + 0.9 * u - 0.0, 1.0)
        if t < t3_pez + 0.12:
            G.salpicadura(lz, b + 700, sea_y + 20, t, t3_pez, n=6, alto=100, dur=0.7)
    # destellos de las estocadas
    for te in (t3_esp + 0.1, t3_esgr + 0.0, t3_esgr + 0.32, t3_mar + 0.05):
        if te <= t < te + 0.35:
            G.brillo(lz, b + 880, GY - 300, t, te, 80, 0.35)
    # ola de primer plano (tapa el borde inferior de la balsa)
    ola_frente(lz, t, X0)


def muelle(lz, x0, x1):
    madera = C["marron"]
    n = int((x1 - x0) // 120)
    for i in range(n + 1):
        x = x0 + i * 120
        lz.relleno(G.rect_red(x + 4, GY + 14, 20, 90, 4), G.ton(C["marron_o"], 0.3))            # postes
    G.sombreado(lz, G.rect_red(x0, GY - 2, x1 - x0, 34, 6), madera, k=0.16, dirx=0.0, diry=-1.0)
    for i in range(n + 1):
        lz.relleno(G.capsula(x0 + i * 120 + 60, GY + 1, x0 + i * 120 + 60, GY + 28, 4), G.ton(madera, 0.45), alfa=0.7)


def aleta(lz, x, y, t, s):
    az = (112, 140, 158)
    with lz.grupo(x, y, s):
        lz.relleno(np.array([(-58, 4), (-8 + 4 * math.sin(t * 6), -120), (52, 4)], float), G.ton(az, 0.15))
        lz.relleno(np.array([(-30, 2), (-8 + 4 * math.sin(t * 6), -112), (16, 2)], float), az)


def estela(lz, x, y, t):
    for i in range(4):
        u = (t * 1.4 + i * 0.25) % 1.0
        lz.relleno(G.capsula(x + 60 + u * 120, y + 4, x + 60 + u * 120 + 60 * (1 - u), y + 4, 6), C["espuma"], alfa=0.7 * (1 - u))


def ola_frente(lz, t, X0):
    """Franja de agua por delante del muelle (solo mientras el océano está en pantalla)."""
    b = BASE[2]
    if not (X0 + W > b and X0 < b + G.BIOMA_W):
        return
    x0, x1 = b + 40, b + G.BIOMA_W - 40
    xs = np.arange(x0, x1 + 1, 80.0)
    ys = GY + 52 + 8 * np.sin(xs * 0.02 + t * 2.4) + 6 * np.sin(xs * 0.043 - t * 1.7)
    pts = [(x0, GY + 240)] + list(zip(xs, ys)) + [(x1, GY + 240)]
    lz.relleno(np.array(pts, float), (88, 132, 136), alfa=0.92)
    for i in range(0, len(xs) - 1, 2):
        lz.relleno(G.capsula(xs[i], ys[i] + 6, xs[i + 1], ys[i + 1] + 6, 6), C["espuma"], alfa=0.5)


def dibujar_r4(lz, t, X0):
    b = BASE[3]
    if not (b - 2100 < X0 < b + 2300):
        return
    # rocas lunares de primer plano
    for i, (cx, s) in enumerate(((300, 1.0), (1080, 0.7), (1720, 1.2))):
        roca(lz, b + cx, GY + 40 + 16 * i, s)
    al = t4_alien
    if t < al - 1.0:
        return
    if t < IMP4:
        # platillo: baja, se coloca sobre el héroe y lo levanta
        x = kf(t, [(al - 1.0, b + 1900), (t4_plat + 0.3, b + 1350), (t4_solo - 0.1, b + 1350), (t4_solo + 0.5, b + 560)], smooth)
        y = kf(t, [(al - 1.0, -120), (t4_plat + 0.3, 200), (t4_cohete, 200)], smooth) + 10 * math.sin(t * 3.3)
        haz = kf(t, [(t4_solo + 0.4, 0.0), (t4_solo + 0.7, 1.0), (t4_cohete + 0.1, 1.0), (t4_cohete + 0.3, 0.0)])
        haz = max(0.0, haz)
        alien = "normal"
        if t4_cohete < t < IMP4:
            alien = "grito"
        G.platillo(lz, x, y, 1.3, t, haz=haz, alien=alien, rot=0.04 * math.sin(t * 3))
        if t4_plat - 0.4 < t < t4_plat + 0.6:
            G.brillo(lz, x + 80, y - 20, t, t4_plat, 60, 0.5)
    else:
        p0 = (b + 560, 200)
        p1 = (b + 1620, GY - 30)
        x, y, u = bal(t, IMP4, t4_nocaut, p0, p1, 260)
        if t < t4_nocaut:
            G.platillo(lz, x, y, 1.3, t, haz=0.0, alien="grito", rot=-(2 * math.pi * 2.5) * u, luces=2.0)
        else:
            G.platillo(lz, p1[0], p1[1], 1.3, t, haz=0.0, alien="ko", rot=math.pi * 1.0 * -1 - 0.15, luces=0.0)
            G.polvo(lz, p1[0] - 20, GY + 6, t, t4_nocaut, n=8, r=50, col=C["luna"], alcance=140)
            humo(lz, p1[0] - 20, p1[1] - 40, t, t4_nocaut)
    # spray del extintor
    hxw = b + HX
    if IMP4 - 0.02 <= t < IMP4 + 0.55:
        G.explosion(lz, b + 590, 340, (t - (IMP4 - 0.02)) / 0.55, 190, seed=9)
        G.ono(lz, "¡CLANG!", b + 800, 150, t, IMP4, dur=1.2, px=150, col=C["mostaza"])


def humo(lz, x, y, t, t0):
    for i in range(5):
        u = ((t - t0) * 0.6 + i * 0.2) % 1.0
        G.disco(lz, x + 14 * math.sin(u * 6 + i), y - 220 * u, 16 + 40 * u, (110, 100, 110), sombra=False, alfa=0.7 * (1 - u))


def roca(lz, x, y, s=1.0):
    with lz.grupo(x, y, s):
        P = np.array([(-90, 0), (-70, -50), (-20, -78), (40, -66), (90, -20), (110, 0)], float)
        G.sombreado(lz, G.catmull(P, 8, True), (150, 146, 158), k=0.09)


def dibujar_r5(lz, t, X0):
    b = BASE[4]
    if not (b - 2100 < X0 < b + 2300):
        return
    for i, (cx, s) in enumerate(((260, 1.0), (1000, 0.8), (1720, 1.1))):
        roca_v(lz, b + cx, GY + 44 + 14 * i, s)
    # ceniza / brasas
    for i in range(16):
        u = ((t * (0.12 + 0.05 * h01(1, i)) + h01(2, i)) % 1.0)
        px = b + (h01(3, i) * 2100 - 100) - (0 if X0 == 0 else 0)
        py = 950 - u * 1000
        G.disco(lz, px + 30 * math.sin(t * 2 + i), py, 5 + 4 * h01(4, i), C["lava_c"], sombra=False, alfa=0.85 * (1 - u))
    dg = t5_dragon
    if t < dg - 0.7:
        return
    dx0 = b + 1520
    alto = kf(t, [(dg - 0.7, 0.0), (dg + 0.35, 1.0)], e_out)
    hundido = 1.0 - e_in(prog(t, t5_nocaut + 0.05, t5_nocaut + 0.9))
    if t >= IMP5:
        alto = alto * hundido
    boca = 0.0
    ko = t >= IMP5 + 0.02
    cab = 0.0
    if dg + 0.2 <= t < dg + 1.0:
        boca = 1.0
    fuego_on = t5_cubre - 0.45 <= t < t5_y + 0.7
    if fuego_on:
        boca = 1.0
    if t5_y + 0.7 <= t < t5_chancla:
        cab = -0.1
        boca = 0.0
    if t >= IMP5:
        boca = 0.2
        cab = 0.6 * smooth(prog(t, IMP5, IMP5 + 0.5))
    shake = 4 * math.sin(t * 50) if (t >= IMP5 and t < IMP5 + 0.5) else 0.0
    hx, hy = G.dragon(lz, dx0 + shake, GY + 60 + 40 * (1 - alto), 1.2, t, mirar=-1, boca=boca, ko=ko, alto=max(0.02, alto), cab=cab,
                      cuello_ang=0.0, estrellas=(t > IMP5 + 0.3 and t < t5_nocaut + 0.9))
    # coordenadas de la boca en el mundo
    mx, my = dx0 - 1.1 * (hx + 120), GY + 60 + 40 * (1 - alto) + 1.1 * (hy - 0)
    if dg + 0.25 <= t < dg + 0.95:                 # llamarada al cielo
        G.fuego(lz, mx, my - 30, -math.pi / 2 - 0.5, t, 520, 0.3, kf(t, [(dg + 0.25, 0.0), (dg + 0.45, 1.0), (dg + 0.8, 1.0), (dg + 0.95, 0.0)]), seed=2)
    if fuego_on:
        dens = kf(t, [(t5_cubre - 0.45, 0.0), (t5_cubre - 0.15, 1.0), (t5_y + 0.45, 1.0), (t5_y + 0.7, 0.0)])
        escudo_x = b + HX - 70 + 190
        largo = max(120.0, (mx - escudo_x) * (1.0 if t < t5_tapa else 1.0))
        G.fuego(lz, mx - 20, my + 10, math.pi - 0.05, t, largo, 0.16, dens, seed=4)
        if t >= t5_tapa:
            # las llamas chocan con la tapa y se abren
            for i in range(10):
                u = ((t * 3 + i * 0.1) % 1.0)
                a = -math.pi / 2 + (i % 2) * math.pi
                G.disco(lz, escudo_x + 30 * u, GY - 190 + math.sin(a) * 210 * u * (1 if i % 2 else 1) * 0.9 * (1 if i % 2 else 1),
                        18 + 16 * u, C["lava_c"] if u < 0.5 else C["lava"], sombra=False, alfa=(1 - u) * dens)
    # chancla que cae del cielo
    if t5_chancla - 0.1 <= t < IMP5:
        x, y, u = bal(t, t5_chancla - 0.1, IMP5, (dx0 - 380, -240), (mx + 20, my - 60), 0)
        G.chancla(lz, x, y, t * 30, 1.5)
        G.lineas_vel(lz, x, y - 60, math.pi / 2 - 0.35, 300, 4, t, 0.55)
        G.brillo(lz, x, y, t, t5_chancla - 0.1, 70, 0.5)
    if IMP5 - 0.03 <= t < IMP5 + 0.6:
        G.explosion(lz, mx + 10, my - 60, (t - (IMP5 - 0.03)) / 0.6, 230, seed=6)
        G.ono(lz, "¡CHANCLAZO!", mx - 330, my - 150, t, IMP5, dur=1.3, px=140, col=C["rojo"])
    if IMP5 <= t < IMP5 + 0.95:
        x, y, u = bal(t, IMP5, IMP5 + 0.95, (mx + 10, my - 60), (b + HX + 120, GY - 330 + 30), 380)
        G.chancla(lz, x, y, t * 18, 1.4)
    if t5_nocaut + 0.3 <= t < t5_nocaut + 1.3:
        G.salpicadura(lz, dx0 - 60, GY + 100, t, t5_nocaut + 0.32, n=14, alto=300, dur=1.1, col=C["lava_c"])


def roca_v(lz, x, y, s=1.0):
    with lz.grupo(x, y, s):
        P = np.array([(-100, 0), (-80, -50), (-20, -86), (50, -70), (100, -20), (120, 0)], float)
        G.sombreado(lz, G.catmull(P, 8, True), (88, 68, 80), k=0.09)
        lz.relleno(G.capsula(-30, -60, 20, -20, 5), C["lava"], alfa=0.9)


def chip(lz, x, y, texto, k, px, fondo, col):
    if k <= 0.02:
        return
    w = 22 + len(texto) * px * 0.62
    with lz.grupo(x, y, k):
        G.pastilla(lz, 0, 0, w, px * 1.7, fondo)
        lz.texto(texto, 0, 0, px, "vox_b", color=col, borde=None, temblor=0)


# ------------------------------------------------------------------ interfaz (coordenadas de pantalla)
CRIA = [("ESCORPIÓN GIGANTE", (t1_esc - 0.3), IMP1, t1_nocaut),
        ("TIRANOSAURIO", t2_trex - 0.2, IMP2, t2_nocaut),
        ("TIBURÓN GIGANTE", t3_tib - 0.2, IMP3, t3_nocaut),
        ("EXTRATERRESTRE", t4_alien - 0.2, IMP4, t4_nocaut),
        ("DRAGÓN", t5_dragon - 0.3, IMP5, t5_nocaut)]
BANNER = ["EL DESIERTO", "LA SELVA", "EL OCÉANO", "LA LUNA", "EL VOLCÁN"]


def icono_cria(lz, i, x, y, k):
    """Dibujo pequeño de cada criatura para las medallas (k = radio/92: 1.0 = medalla grande)."""
    if i == 0:
        with lz.grupo(x, y + 40 * k, 0.42 * k):
            G.escorpion(lz, 0, 0, 1.0, 1.0, mirar=1, cola=0.0, pinza=0.3, ph=0)
    elif i == 1:
        with lz.grupo(x + 22 * k, y + 41 * k, 0.22 * k):
            G.trex(lz, 0, 0, 1.0, 1.0, mirar=1, boca=0.4)
    elif i == 2:
        with lz.grupo(x + 6 * k, y + 6 * k, 0.30 * k):
            G.tiburon(lz, 0, 0, 1.0, 1.0, mirar=1, boca=0.5)
    elif i == 3:
        with lz.grupo(x, y + 8 * k, 0.5 * k):
            G.platillo(lz, 0, 0, 1.0, 1.0, luces=0.0)
    else:
        with lz.grupo(x - 10 * k, y + 52 * k, 0.36 * k):
            G.dragon(lz, 0, 0, 1.0, 1.0, mirar=1, boca=0.3, alto=0.32)


def medalla(lz, i, x, y, r, ko_u, activa, t):
    G.disco(lz, x, y, r + 7, G.ton(C["marron_o"], 0.2), sombra=False)
    G.disco(lz, x, y, r, C["crema"] if not activa else G.luz(C["mostaza"], 0.55), sombra=False)
    lz.relleno(G.circulo(x, y, r * 0.86, 40), G.ton(C["arena"], 0.05), alfa=0.55)
    icono_cria(lz, i, x, y, r / 92.0)
    if ko_u > 0:
        k = e_back(ko_u)
        lz.relleno(G.circulo(x, y, r * 0.9, 40), C["blanco"], alfa=0.5 * min(1, ko_u * 2))
        G.ojo_x(lz, x, y, r * 0.5 * k, C["rojo"], w=r * 0.2 * k)


def ui(lz, t):
    dibujo = False
    # --- medallas (arriba en el centro)
    u_med = e_inout(prog(t, t_una - 0.15, t_una + 0.55))
    u_fin = e_inout(prog(t, tc_marcador - 0.1, tc_marcador + 0.6)) * (1 - e_inout(prog(t, tc_nunca - 0.3, tc_nunca + 0.3)))
    for i in range(5):
        aparece = G.e_back(min(1, max(0.0, (t - (t_cinco + 0.16 * i)) / 0.3))) if hasattr(G, "e_back") else 1
        gx, gy, gr = 1230 + (i - 2) * 200, 300, 82
        px_, py_, pr_ = 960 + (i - 2) * 84, 72, 36
        u = u_med
        # el marcador final vuelve a agrandarlas
        x = lerp(px_, gx, max(0.0, u_fin)) if t > tc_marcador - 1 else lerp(gx, px_, u)
        y = lerp(py_, gy, max(0.0, u_fin)) if t > tc_marcador - 1 else lerp(gy, py_, u)
        r = lerp(pr_, gr, max(0.0, u_fin)) if t > tc_marcador - 1 else lerp(gr, pr_, u)
        activa = CRIA[i][1] <= t < CRIA[i][3] + 1.0
        ko_u = (t - CRIA[i][3]) / 0.4 if t >= CRIA[i][3] else 0.0
        if t > tc_marcador - 1:
            ko_u = 1.0
        if aparece > 0.02:
            medalla(lz, i, x, y, r * aparece, min(1, max(0.0, ko_u)), activa, t)
            dibujo = True
    # --- barras de vida
    if t > t_una:
        a = e_out(prog(t, t_una, t_una + 0.4))
        bx = -700 + 760 * a
        G.barra(lz, 60 - 800 * (1 - a), 66, 640, 1.0, "DON BETO", C["palma"], 1, t)
        for i, (nom, t_in, t_hit, t_ko) in enumerate(CRIA):
            if t_in - 0.1 <= t < t_ko + 1.4:
                ent = e_out(prog(t, t_in, t_in + 0.4))
                sal = e_in(prog(t, t_ko + 0.9, t_ko + 1.4))
                frac = 1.0 if t < t_hit else max(0.0, 1.0 - (t - t_hit) / 0.35)
                if i == 4 and t < IMP5:
                    frac = 1.0
                off = 800 * ((1 - ent) + sal)
                ag = 1.0 * math.exp(-(t - t_hit) * 6) if t_hit <= t < t_hit + 0.6 else 0.0
                G.barra(lz, 1860 + off, 66, 640, frac, nom, C["rojo"], -1, t, agita=ag)
        dibujo = True
    # --- rótulos de ronda
    for i, r in enumerate(RONDAS):
        t0 = INI(r, 0)
        if t0 - 0.05 <= t < T_PELEA[r] + 1.0:
            if t < INI(r, 1) - 0.05 or True:
                k_in = G.e_back(min(1, (t - t0) / 0.32)) if hasattr(G, "e_back") else 1
                sal = e_in(prog(t, INI(r, 1) + 0.15, INI(r, 1) + 0.5))
                k = k_in * (1 - sal)
                if k > 0.02:
                    G.rotulo(lz, f"RONDA {i + 1}", 960, 262, 190, C["crema"], k, -0.03)
                    G.rotulo(lz, BANNER[i], 960, 384, 74, C["mostaza"], k, -0.03, "vox_serif")
                    dibujo = True
            # ¡PELEA!
            tp = T_PELEA[r]
            if tp <= t < tp + 0.9:
                kk = G.e_back(min(1, (t - tp) / 0.22)) * (1 - prog(t, tp + 0.65, tp + 0.9))
                G.rotulo(lz, "¡PELEA!", 960, 340, 210, C["rojo"], kk, 0.05)
                dibujo = True
    # --- ¡NOCAUT!
    for i, tk in enumerate(KOS):
        if tk <= t < tk + 1.5:
            kk = G.e_back(min(1, (t - tk) / 0.25)) * (1 - prog(t, tk + 1.1, tk + 1.5))
            G.rotulo(lz, "¡NOCAUT!" if i < 4 else "¡NOCAUT FINAL!", 1080 if i < 4 else 960, 300, 190 if i < 4 else 150, C["rojo"], kk, -0.06)
            dibujo = True
    # --- presentación del héroe
    if t_hombre - 0.05 <= t < t_una + 0.2:
        kk = G.e_back(min(1, (t - max(t_hombre, 0.9)) / 0.3)) * (1 - prog(t, t_una - 0.1, t_una + 0.2)) if t > 0.85 else 0.0
        chip(lz, 440, 336, "DON BETO · HOMBRE NORMAL", kk, 38, C["crema"], G.TINTA)
        dibujo = True
    # --- chips de arma
    armas = [(t1_chancla, "ARMA: LA CHANCLA", t1_chanclazo - 0.25), (t2_sar, "ARMA: SARTÉN", t2_sartenazo - 0.35),
             (t3_pez + 0.45, "ARMA: PEZ ESPADA", t3_esgr), (t4_ext, "ARMA: EXTINTOR", t4_cohete + 0.5),
             (t5_tapa, "ARMA: TAPA DE OLLA", t5_y + 0.7)]
    for ta, txt, tb in armas:
        if ta <= t < tb + 0.4:
            kk = G.e_back(min(1, (t - ta) / 0.28)) * (1 - prog(t, tb, tb + 0.4))
            chip(lz, 560, 372, txt, kk, 42, C["crema"], G.TINTA)
            dibujo = True
    # --- marcador final y cierre
    if t >= tc_marcador - 0.1:
        if tc_hombre - 0.05 <= t < tc_nunca - 0.05:
            k1 = G.e_back(min(1, (t - tc_hombre) / 0.3)) * (1 - prog(t, tc_nunca - 0.3, tc_nunca - 0.05))
            G.rotulo(lz, "HOMBRE", 1030, 530, 92, C["crema"], k1, -0.02)
            if t >= tc_cinco:
                G.rotulo(lz, "5", 1030, 660, 200, C["mostaza"], G.e_back(min(1, (t - tc_cinco) / 0.3)) * (1 - prog(t, tc_nunca - 0.3, tc_nunca - 0.05)), -0.02)
            if t >= tc_crias - 0.05:
                k2 = G.e_back(min(1, (t - tc_crias) / 0.3)) * (1 - prog(t, tc_nunca - 0.3, tc_nunca - 0.05))
                G.rotulo(lz, "CRIATURAS", 1450, 530, 92, C["crema"], k2, 0.02)
            if t >= tc_cero:
                G.rotulo(lz, "0", 1450, 660, 200, C["rojo"], G.e_back(min(1, (t - tc_cero) / 0.3)) * (1 - prog(t, tc_nunca - 0.3, tc_nunca - 0.05)), 0.02)
            dibujo = True
        if t >= tc_nunca:
            k = G.e_back(min(1, (t - tc_nunca) / 0.35))
            fin = prog(t, TOTAL - 0.9, TOTAL - 0.05)
            G.rotulo(lz, "NUNCA SUBESTIMES", 1240, 300, 84, C["crema"], k, -0.02, alfa=1 - fin)
            G.rotulo(lz, "A UNA CHANCLA", 1240, 410, 116, C["mostaza"], G.e_back(min(1, max(0.0, (t - tc_chancla + 0.25) / 0.35))), -0.02, alfa=1 - fin)
            dibujo = True
    return dibujo


# ------------------------------------------------------------------ render
def render_mundo(lz, t):
    X0 = X0_de(t)
    bg = G.fondo_mundo(X0, t)
    z, dx, dy = camara(t)
    Mc = mat_t(W / 2 + dx, H / 2 + dy) @ mat_r(0.0) @ mat_s(z) @ mat_t(-W / 2, -H / 2)
    if abs(z - 1) > 1e-4 or abs(dx) > 1e-3 or abs(dy) > 1e-3:
        bg = cv2.warpAffine(bg, Mc[:2].astype(np.float32), (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    lz.nuevo(t, wob=0.0)
    lz.M = Mc @ mat_t(-X0, 0)
    dibujar_todo(lz, t, X0)
    img = componer(bg, lz.resolver(), boil=lz.boil)
    lz.nuevo(t)
    if ui(lz, t):
        img = componer(img, lz.resolver(), boil=lz.boil)
    neg = prog(t, TOTAL - 0.8, TOTAL - 0.05)
    if neg > 0:
        img = img * (1 - smooth(neg)) + np.array([0.93, 0.89, 0.79], np.float32) * smooth(neg)
    return np.clip(img, 0, 1)


def dibujar_todo(lz, t, X0):
    # escenarios y criaturas (detrás del héroe)
    dibujar_r1(lz, t, X0)
    dibujar_r2(lz, t, X0)
    dibujar_r3(lz, t, X0)
    dibujar_r4(lz, t, X0)
    dibujar_r5(lz, t, X0)
    # héroe
    p, ddx, ddy = pose_heroe(t)
    x = X0 + HX + ddx
    y = GY + ddy
    ph = ((X0 + ddx) * 2 * math.pi / 330.0) if p["paso"] > 0.01 else 0.0
    inc = p.pop("inc")
    hands = G.hombre(lz, x, y, HS, t, mirar=1, ph=ph, inc=inc, **p)
    # objetos que dependen de la mano
    _extras_heroe(lz, t, X0, x, y, p, hands)
    # capas de primer plano por bioma (después del héroe)
    if X0 + W > BASE[2] - 200 and X0 < BASE[3] + 60:
        ola_frente(lz, t, X0)
    # rayas de velocidad durante las carreras
    for i in range(1, 5):
        if PAN0[i] + 0.15 <= t < PAN0[i] + PAN_DUR - 0.15:
            k = math.sin(math.pi * prog(t, PAN0[i], PAN0[i] + PAN_DUR))
            G.lineas_vel(lz, X0 + 760, GY - 170, 0.0, 460, 6, t, 0.5 * k)
            G.lineas_vel(lz, X0 + 300, GY - 300, 0.0, 300, 4, t + 0.3, 0.35 * k)
            G.polvo(lz, x - 80, GY + 20, t, math.floor(t * 6) / 6.0, n=5, r=30, dur=0.4, dir=(-1.0, 0.0), alcance=70)


def _extras_heroe(lz, t, X0, x, y, p, hands):
    s = HS
    if "f" not in hands:
        return
    hx_, hy_, ang = hero_hands_world(x, y, s, hands)
    # chispas de las estocadas y llamas de la tapa se dibujan en cada ronda; aquí: brillo al sacar el arma
    for ta in (t1_chancla, t2_sar, t3_pez + 0.5, t4_ext, t5_tapa, tc_chancla):
        if ta <= t < ta + 0.5:
            G.brillo(lz, hx_ + 30, hy_ - 40, t, ta, 90, 0.5)
    # extintor: nube saliendo de la boquilla mientras vuela
    if t4_cohete <= t < t4_cohete + 1.4:
        nx = hx_ + (118 * math.cos(ang) - 8 * math.sin(ang)) * s
        ny = hy_ + (118 * math.sin(ang) + 8 * math.cos(ang)) * s
        G.spray(lz, nx, ny, ang, t, t4_cohete, t4_cohete + 0.6, 330)


# ------------------------------------------------------------------ sonido
def sonidos(e):
    ev = e.ev
    ev(0.1, "aparicion", 0.5)
    # intro
    ev(t_hombre, "pop", 0.6, tono=0.9)
    for i in range(5):
        ev(t_cinco + 0.16 * i, "pop", 0.55, tono=1.0 + 0.12 * i)
    ev(t_una - 0.1, "whoosh", 0.5, dur=0.6)
    # marcadores de ronda
    for i, r in enumerate(RONDAS):
        ev(INI(r, 0), "gong", 0.75)
        ev(T_PELEA[r], "impacto", 0.4, tono=1.6)
        ev(T_PELEA[r] + 0.02, "aparicion", 0.4, tono=1.3)
    for tk in KOS:
        ev(tk, "ko", 0.9)
        ev(tk + 0.05, "estrellitas", 0.5)
    # carreras
    for i in range(1, 5):
        ev(PAN0[i], "whoosh", 0.55, dur=1.6, tono=0.8)
        ev(PAN0[i], "pasos", 0.6, dur=PAN_DUR)
        ev(PAN0[i] + PAN_DUR - 0.3, "puf", 0.4)
    # ronda 1
    ev(t1_esc - 0.85, "pasos", 0.5, dur=1.3, tono=1.4)
    ev(t1_esc - 0.5, "arena", 0.4, dur=1.0)
    ev(t1_gig, "comic", 0.5)
    ev(t1_secreta + 0.02, "impacto", 0.5, tono=1.5)
    ev(t1_secreta - 0.05, "whoosh", 0.5, dur=0.3, tono=1.6)
    ev(t1_saca, "hmm", 0.5)
    ev(t1_chancla - 0.1, "ding", 0.6)
    ev(t1_chancla - 0.05, "brillo", 0.5)
    ev(t1_chanclazo - 0.15, "whoosh", 0.5, dur=0.3, tono=1.2)
    ev(IMP1, "chancla", 1.0)
    ev(IMP1, "comic", 0.6)
    ev(IMP1 + 0.05, "boing", 0.6, tono=1.4)
    ev(t1_nocaut, "impacto", 0.7, tono=1.3)
    ev(t1_nocaut + 0.05, "bocinazo", 0.4)
    # ronda 2
    for k in range(6):
        ev(t2_trex - 0.9 + 0.35 * k + 0.05, "impacto", 0.45, tono=1.8 - 0.08 * k)
    ev(t2_trex, "rugido", 0.8)
    ev(t2_brac, "boing", 0.6, tono=1.4)
    ev(t2_ridi, "comic", 0.5)
    ev(t2_resp - 0.05, "rugido", 0.9)
    ev(t2_resp + 0.25, "impacto", 0.5, tono=1.5)
    ev(t2_sar - 0.05, "ding", 0.6)
    ev(t2_sar, "brillo", 0.5)
    ev(t2_sartenazo - 0.34, "whoosh", 0.6, dur=0.35, tono=1.0)
    ev(IMP2, "bonk", 1.0)
    ev(IMP2 + 0.02, "comic", 0.5)
    ev(t2_nocaut - 0.1, "impacto", 0.8, tono=1.2)
    ev(t2_nocaut + 0.2, "bocinazo", 0.4, tono=0.9)
    # ronda 3
    ev(t3_tib - 0.8, "latido", 0.7)
    ev(t3_tib + 0.5, "latido", 0.7)
    ev(t3_gig + 0.3, "latido", 0.8)
    ev(t3_tib - 0.5, "ola", 0.35, dur=1.4)
    ev(t3_contra - 0.1, "chapuzon", 0.9)
    ev(t3_contra - 0.05, "rugido", 0.5, tono=1.4)
    ev(t3_pez, "chapuzon", 0.5, tono=1.5)
    ev(t3_pez + 0.4, "ding", 0.6)
    for te in (t3_esp + 0.1, t3_esgr + 0.0, t3_esgr + 0.32, t3_mar + 0.05):
        ev(te, "clink", 0.9, tono=1.0 + 0.1 * (te % 3))
        ev(te, "zap", 0.35, tono=1.3)
    ev(IMP3, "comic", 0.7)
    ev(IMP3 + 0.02, "boing", 0.6, tono=1.3)
    ev(t3_nocaut + 0.36, "chapuzon", 1.0)
    ev(t3_nocaut + 0.5, "bocinazo", 0.4, tono=0.8)
    # ronda 4
    ev(t4_alien - 0.9, "whoosh", 0.4, dur=1.0, tono=0.7)
    ev(t4_alien, "zap", 0.5, tono=0.8)
    ev(t4_plat, "aparicion", 0.6, tono=1.4)
    ev(t4_solo + 0.5, "zap", 0.7, tono=0.6)
    ev(t4_solo + 0.55, "espiral_zap", 0.5, dur=0.85)
    ev(t4_ext, "ding", 0.6)
    ev(t4_cohete, "spray", 1.0, dur=0.6)
    ev(t4_cohete, "whoosh", 0.7, dur=0.7, tono=1.4)
    ev(IMP4, "bonk", 1.0)
    ev(IMP4 + 0.02, "clink", 0.7)
    ev(IMP4 + 0.1, "whoosh", 0.5, dur=0.9, tono=0.9)
    ev(t4_nocaut - 0.05, "impacto", 0.7, tono=1.3)
    ev(t4_nocaut + 0.2, "bocinazo", 0.4, tono=1.1)
    # ronda 5
    ev(t5_dragon - 0.6, "impacto", 0.6, tono=0.6)
    ev(t5_dragon - 0.4, "rugido", 1.0, tono=0.75)
    ev(t5_dragon + 0.25, "fuego", 0.7, dur=0.9)
    ev(t5_cubre - 0.45, "rugido", 0.7, tono=0.9)
    ev(t5_cubre - 0.35, "fuego", 1.0, dur=t5_y + 0.7 - (t5_cubre - 0.35))
    ev(t5_tapa - 0.05, "ding", 0.6)
    ev(t5_tapa + 0.05, "clink", 0.8, tono=0.7)
    ev(t5_chancla - 0.1, "whoosh", 0.7, dur=t5_regresa - t5_chancla + 0.15, tono=1.5)
    ev(t5_chancla - 0.05, "brillo", 0.5)
    ev(IMP5, "chancla", 1.0)
    ev(IMP5, "bonk", 0.7, tono=0.9)
    ev(IMP5 + 0.03, "comic", 0.6)
    ev(t5_nocaut + 0.3, "chapuzon", 1.0, tono=0.6)
    ev(t5_nocaut + 0.35, "fuego", 0.4, dur=0.8)
    ev(t_chancla_mano(), "ding", 0.7, tono=1.2)
    ev(t_chancla_mano(), "brillo", 0.6)
    # cierre
    ev(tc_marcador, "whoosh", 0.5, dur=0.7)
    ev(tc_hombre, "pop", 0.6, tono=1.0)
    ev(tc_cinco, "ding", 0.7)
    ev(tc_crias, "pop", 0.6, tono=0.8)
    ev(tc_cero, "bocinazo", 0.5, tono=1.2)
    ev(tc_nunca, "whoosh", 0.4, dur=0.5)
    ev(tc_chancla, "ding", 0.7, tono=1.3)
    ev(tc_chancla + 0.05, "campana", 0.5, tono=1.1)


class Mundo(Escena):
    def preparar(self):
        if self.idx == 0:
            sonidos(self)

    def render(self, lz, t):
        return render_mundo(lz, t)


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
