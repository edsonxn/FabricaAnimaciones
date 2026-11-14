# -*- coding: utf-8 -*-
"""Planos 3: repetición en cámara lenta, por qué importa, qué sigue, cifras y cierre. También los SFX de planos1."""
from comun import *  # noqa: F401,F403
from comun import (H, M, R_T, SB, W, TOTAL, L3, Cam, S, ap, circulo3d, clamp, e_inout, e_out, etiqueta3d, F0, F1, globo, hud_mision,
                   lerp, nrm, pr, real, rejilla_suelo, smooth, T0, T1, vent, ww, ancho_texto)
import math
import numpy as np

import planos1 as P1
import planos2 as P2

E, N, U = SB.E, SB.N, SB.U


def _vacio():
    return L3(Cam((0, -10, 0), (0, 0, 0)))


def bloque(lz, x, y, titulo, sub, op, px=64, anchor="lm"):
    lz.texto(titulo, x, y, px, "Bold Condensed", op, anchor, esp=0.05)
    if sub:
        lz.texto(sub, x + (4 if anchor[0] == "l" else 0), y + px * 0.62 + 6, 24, "SemiBold Condensed", op * 0.9, anchor, esp=0.14)


# ------------------------------------------------------------------ CÁMARA LENTA
def t_lenta(t):
    t0, t1 = T0("lenta"), T1("lenta")
    tc = ww("lenta", 2, "cierran")
    s = smooth(pr(t, t0 + 0.5, tc + 1.2))                     # la nave baja los últimos metros
    base = P2.CAPTURA + U * (22.0 * (1 - s)) * M
    k = pr(t, t0, t1)
    foco = P2.CAPTURA + U * (S.Z_PERNOS_NAVE + 2) * M + E * 2 * M
    az = math.radians(lerp(150, 235, e_inout(k)))
    el = math.radians(lerp(8, 18, k))
    d = math.cos(el) * (math.sin(az) * E + math.cos(az) * N) + math.sin(el) * U
    cam = Cam(foco + d * lerp(0.11, 0.075, e_inout(k)), foco, U, 40, cerca=0.0005, centro=(W * 0.42, H * 0.5))
    lz = L3(cam)
    rejilla_suelo(lz, SB.P, E, N, 0.6, 0.02, op=0.14)
    ab = 0.75 * (1 - smooth(pr(t, tc - 0.2, tc + 1.4)))
    P1.torre(lz, 0.95, ab, w=1.2)
    if t < tc + 1.0:
        P1.llamas_nave(lz, base, U, 0, t * 0.25, 30, 1.4, E, cuales=[0])
    S.nave(lz, base, U, M, op=1.0, ref=E, rot=math.pi / 2, flaps=0.15)
    op_ = ap(t, ww("lenta", 2, "soportes") - 0.2)
    if op_ > 0:
        for lado in (1, -1):
            pp = base + (U * S.Z_PERNOS_NAVE + N * lado * 4.8) * M
            x, y = cam.px(pp)
            lz.c2(x, y, 26 + 8 * math.sin(t * 4), op_, w=1.6)
        x, y = cam.px(base + U * S.Z_PERNOS_NAVE * M + N * 4.8 * M)
        lz.l2([(x + 26, y - 10), (1240, 300)], op_ * 0.6, 1.0)
        bloque(lz, 1250, 290, "2 SOPORTES", "BAJO LOS ALERONES DELANTEROS", op_, 60)
    o3 = ap(t, F0("lenta", 3))
    bloque(lz, 1250, 560, "SIN PATAS", "SIN TOCAR EL SUELO", o3, 72)
    lz.texto("REPETICIÓN  ·  CÁMARA LENTA", 70, 66, 22, "SemiBold Condensed", ap(t, t0), "lm", esp=0.2)
    return lz


# ------------------------------------------------------------------ POR QUÉ IMPORTA
def _transbordador(lz, cx, cy, s, op):
    pts = [(-1.0, 0.0), (-0.55, -0.12), (0.35, -0.12), (0.55, -0.05), (0.62, 0.0), (0.55, 0.05), (0.35, 0.12), (-0.55, 0.12), (-1.0, 0.0)]
    lz.l2([(cx + x * s, cy + y * s) for x, y in pts], op, 1.6)
    ala = [(-0.35, 0.12), (0.2, 0.12), (-0.55, 0.42), (-0.75, 0.42), (-0.35, 0.12)]
    lz.l2([(cx + x * s, cy + y * s) for x, y in ala], op, 1.4)
    lz.l2([(cx - 0.85 * s, cy - 0.05 * s), (cx - 1.0 * s, cy - 0.35 * s), (cx - 0.8 * s, cy - 0.12 * s)], op, 1.4)


def _nave2d(lz, cx, cy, s, op):
    """Silueta de Starship en vertical (cy = base)."""
    pts = [(-0.09, 0.0), (-0.09, -0.62), (-0.07, -0.8), (-0.03, -0.95), (0.0, -1.0), (0.03, -0.95), (0.07, -0.8), (0.09, -0.62), (0.09, 0.0)]
    lz.l2([(cx + x * s, cy + y * s) for x, y in pts], op, 1.6, cerrada=True)
    for lado in (1, -1):
        lz.l2([(cx + 0.09 * lado * s, cy - 0.05 * s), (cx + 0.2 * lado * s, cy - 0.02 * s), (cx + 0.2 * lado * s, cy - 0.25 * s),
               (cx + 0.09 * lado * s, cy - 0.3 * s)], op, 1.3)
        lz.l2([(cx + 0.08 * lado * s, cy - 0.72 * s), (cx + 0.15 * lado * s, cy - 0.7 * s), (cx + 0.13 * lado * s, cy - 0.84 * s),
               (cx + 0.06 * lado * s, cy - 0.86 * s)], op, 1.3)


def i_comparar(t):
    lz = _vacio()
    o1 = ap(t, F0("importa", 1) - 0.1)
    lz.texto("¿POR QUÉ IMPORTA?", W / 2, 140, 64, "Bold Condensed", ap(t, T0("importa") + 0.3) * (1 - o1), "mm", esp=0.05)
    # transbordador: planea como avión
    cx1, cy1 = 520, 560
    if o1 > 0:
        P = [(cx1 - 380 + 760 * q, cy1 - 160 + 230 * q ** 1.6) for q in np.linspace(0, e_out(pr(t, F0("importa", 1), F1("importa", 1))), 40)]
        lz.l2(P, o1 * 0.5, 1.2) if len(P) > 1 else None
        x, y = P[-1] if P else (cx1 - 380, cy1 - 160)
        _transbordador(lz, x, y - 10, 90, o1)
        lz.l2([(cx1 - 420, cy1 + 90), (cx1 + 440, cy1 + 90)], o1 * 0.6, 1.2)
        bloque(lz, cx1, 760, "TRANSBORDADOR", "VOLVÍA PLANEANDO, COMO AVIÓN", o1, 54, "mm")
    o2 = ap(t, F0("importa", 2) - 0.1)
    cx2, cy2 = 1400, 650
    if o2 > 0:
        lz.l2([(cx2 - 260, cy2), (cx2 + 260, cy2)], o2 * 0.6, 1.2)
        lz.l2([(cx2 - 120, cy2), (cx2 - 120, cy2 - 420), (cx2 - 96, cy2 - 420), (cx2 - 96, cy2)], o2 * 0.7, 1.2)       # torre
        lz.l2([(cx2 - 96, cy2 - 330), (cx2 - 20, cy2 - 330)], o2, 1.6)
        _nave2d(lz, cx2, cy2 - 200, 250, o2)
        bloque(lz, cx2, 760, "STARSHIP · NAVE 42", "VUELVE DE ÓRBITA Y ATERRIZA DE PIE", o2, 54, "mm")
        lz.texto("PRIMERA VEZ", cx2, 150, 44, "Bold Condensed", ap(t, ww("importa", 2, "ninguna")), "mm", esp=0.1)
    hud_mision(lz, 0.8)
    return lz


def i_torre(t):
    t0 = F0("importa", 3) - 0.3
    k = pr(t, t0, F0("importa", 6))
    foco = P1.P_TORRE + U * 75 * M + E * 25 * M
    az = math.radians(lerp(210, 250, k))
    d = math.cos(0.15) * (math.sin(az) * E + math.cos(az) * N) + math.sin(0.15) * U
    cam = Cam(foco + d * 0.30, foco, U, 40, cerca=0.001, centro=(W * 0.36, H * 0.52))
    lz = L3(cam)
    rejilla_suelo(lz, SB.P, E, N, 0.6, 0.02, op=0.16)
    S.mesa_lanzamiento(lz, P1.P_MESA, U, M, op=0.55 + 0.4 * vent(t, ww("importa", 3, "cargar") - 0.3, F0("importa", 4)), ref=N)
    P1.torre(lz, 0.9, 0.0)
    P1.nave_atrapada(lz)
    o3 = vent(t, ww("importa", 3, "patas"), F0("importa", 4))
    bloque(lz, 1200, 300, "SIN PATAS", "MENOS PESO, MÁS CARGA ÚTIL", o3, 64)
    etiqueta3d(lz, P1.P_MESA + U * 20 * M, "SE VUELVE A CARGAR AQUÍ", None, dx=200, dy=60,
               op=vent(t, ww("importa", 3, "cargar") - 0.2, F0("importa", 4)), px=26)
    o4 = ap(t, F0("importa", 4))
    if o4 > 0:
        bloque(lz, 1200, 300, "REUTILIZABLE", "ENTERO, COMO UN AVIÓN", o4, 70)
        for i, (txt, ok, tt) in enumerate((("NAVE", True, F0("importa", 4) + 1.0), ("PROPULSOR", False, F0("importa", 5)))):
            oi = ap(t, tt)
            y = 470 + i * 80
            lz.l2([(1210, y - 24), (1258, y - 24), (1258, y + 24), (1210, y + 24)], oi, 1.4, cerrada=True)
            if ok:
                lz.l2([(1218, y), (1230, y + 14), (1252, y - 16)], oi, 2.2)
            else:
                lz.l2([(1220, y - 14), (1248, y + 14)], oi, 2.2)
                lz.l2([(1220, y + 14), (1248, y - 14)], oi, 2.2)
            lz.texto(txt + ("  ·  LOGRADO" if ok else "  ·  ESTA VEZ NO"), 1280, y, 34, "SemiBold Condensed", oi, "lm", esp=0.1)
    hud_mision(lz, 0.8)
    return lz


def i_luna(t):
    t0 = F0("importa", 6) - 0.3
    k = pr(t, t0, T1("importa"))
    luna = np.array([0.0, 0.0, 0.0])
    Rl = 1737.0
    ang = 0.5 + 0.4 * k
    cam = Cam(np.array([math.cos(ang), math.sin(ang), 0.25]) * 6200, luna, (0, 0, 1.0), 40, cerca=1.0, centro=(W * 0.36, H * 0.5))
    lz = L3(cam)
    globo(lz, luna, Rl, paso=15, costas=False, op_rej=0.3, op=ap(t, t0, 0.6))
    for i in range(14):                                        # cráteres
        la, lo = math.radians(-50 + (i * 37) % 100), math.radians(i * 53)
        c = np.array([math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la)]) * Rl
        if (cam.pos - c) @ c > 0:
            lz.linea(circulo3d(c * 1.001, c, 60 + 90 * ((i * 7) % 5) / 5, 40), ap(t, t0) * 0.6, 1.0, cerrada=True)
    cd = nrm(np.array([math.cos(ang), math.sin(ang), 0.25]))
    sitio = nrm(cd * 0.7 + np.array([0, 0, 0.75]) + nrm(np.cross(cd, [0, 0, 1.0])) * 0.25) * Rl
    S.nave(lz, sitio, nrm(sitio), 9.0, op=ap(t, ww("importa", 6, "luna") - 0.3), ref=np.array([0, 0, 1.0]), rot=0.0)
    o = ap(t, ww("importa", 6, "nasa"))
    bloque(lz, 1240, 330, "LA LUNA", "LA NASA CUENTA CON UNA VERSIÓN DE ESTA NAVE", o * (1 - ap(t, F0("importa", 7))), 80)
    o7 = ap(t, F0("importa", 7))
    bloque(lz, 1240, 330, "22 H 32 MIN", "LA MISIÓN MÁS LARGA DE STARSHIP", o7, 80)
    hud_mision(lz, 0.8)
    return lz


# ------------------------------------------------------------------ QUÉ SIGUE
def s_pregunta(t):
    t0 = T0("sigue")
    lz = L3(Cam(np.array([0.0, -150.0, 40.0]), np.array([0.0, 0.0, 36.0]), (0, 0, 1.0), 40, cerca=0.5, centro=(W * 0.32, H * 0.52)))
    a = nrm(np.array([0.15, 0.0, 1.0]))
    S.super_heavy(lz, np.array([0.0, 0.0, 0.0]), a, 1.0, 1.0, op=0.45 * ap(t, t0, 0.6), ref=np.array([0, 1.0, 0]))
    o = ap(t, F0("sigue", 1))
    lz.texto("?", 600, 520, 260, "Bold Condensed", o * (0.7 + 0.3 * math.sin(t * 3)), "mm")
    lz.texto("¿Y AHORA QUÉ SIGUE?", W * 0.62, 300, 60, "Bold Condensed", ap(t, t0 + 0.3), "mm", esp=0.05)
    bloque(lz, 1100, 480, "B22: ¿QUÉ FALLÓ?", "SPACEX LO INVESTIGA ANTES DEL PRÓXIMO VUELO", o, 60)
    hud_mision(lz, 0.8)
    return lz


def s_real(t):
    t0 = F0("sigue", 2) - 0.3
    lz = _vacio()
    if t < F0("sigue", 3):
        rot, sub = "NAVE 42, EN LA TORRE", "LA PRIMERA STARSHIP QUE VUELVE DE ÓRBITA ENTERA"
    else:
        rot, sub = "LOSETAS · ALERONES · MOTORES", "REVISIÓN PIEZA POR PIEZA"
    return real(t, "reg", 990 + (t - t0) * 0.8, lz, rotulo=rot, sub=sub)


# ------------------------------------------------------------------ CIFRAS
CIFRAS = [("22 H 32 MIN", "DE MISIÓN", 1, "veintidos"), ("14", "VUELTAS A LA TIERRA", 2, "catorce"),
          ("26", "SATÉLITES EN ÓRBITA", 3, "veintiseis"), ("33 A 1", "MOTORES: PARA DESPEGAR Y PARA DETENERSE", 4, "treinta"),
          ("1 DE 2", "CAPTURAS LOGRADAS", 5, "una")]


def c_cifras(t):
    t0 = T0("cifras")
    ang = 0.5 + 0.3 * pr(t, t0, T1("cifras"))
    eje = np.array([0, 0, 1.0])
    lz = L3(Cam(np.array([math.cos(ang), math.sin(ang), 0.15]) * 230, eje * 62, eje, 40, cerca=0.5, centro=(W * 0.22, H * 0.5)))
    S.pila(lz, np.zeros(3), eje, 1.0, op=0.7 * ap(t, t0, 0.6), ref=np.array([1.0, 0, 0]))
    lz.texto("EL VUELO 15 EN CIFRAS", 780, 150, 46, "Bold Condensed", ap(t, t0 + 0.2), "lm", esp=0.08)
    for i, (big, sub, fr, pal) in enumerate(CIFRAS):
        oi = ap(t, ww("cifras", fr, pal) - 0.15)
        y = 270 + i * 135
        lz.l2([(780, y + 52), (780 + 900 * e_out(oi), y + 52)], oi * 0.35, 1.0)
        lz.texto(big, 780, y, 80, "Bold Condensed", oi, "lm", esp=0.04)
        lz.texto(sub, 1180, y + 6, 26, "SemiBold Condensed", oi * 0.9, "lm", esp=0.14)
    return lz


# ------------------------------------------------------------------ CIERRE
def c_cierre(t):
    t0 = T0("cierre")
    k = pr(t, t0, TOTAL)
    foco = P1.P_TORRE + U * 85 * M + E * 22 * M
    az = math.radians(lerp(200, 250, k))
    d = math.cos(0.2) * (math.sin(az) * E + math.cos(az) * N) + math.sin(0.2) * U
    cam = Cam(foco + d * lerp(0.22, 0.30, k), foco, U, 40, cerca=0.001, centro=(W * 0.30, H * 0.5))
    lz = L3(cam)
    rejilla_suelo(lz, SB.P, E, N, 0.6, 0.02, op=0.16)
    S.mesa_lanzamiento(lz, P1.P_MESA, U, M, op=0.5, ref=N)
    P1.torre(lz, 0.9, 0.0)
    P1.nave_atrapada(lz)
    for i, (txt, pal) in enumerate((("1 NAVE ATRAPADA", "nave"), ("1 PROPULSOR PERDIDO", "propulsor"), ("26 SATÉLITES EN ÓRBITA", "veintiseis"))):
        oi = vent(t, ww("cierre", 0, pal) - 0.1, F0("cierre", 2))
        lz.texto(txt, 1060, 300 + i * 70, 44, "Bold Condensed", oi, "lm", esp=0.06)
    oh = vent(t, F0("cierre", 1), F0("cierre", 2))
    lz.texto("NO FUE PERFECTO.", 1060, 560, 40, "SemiBold Condensed", oh, "lm", esp=0.1)
    lz.texto("FUE HISTÓRICO.", 1060, 620, 64, "Bold Condensed", ap(t, ww("cierre", 1, "historico") - 0.1) * oh, "lm", esp=0.05)
    ol = ap(t, F0("cierre", 2))
    if ol > 0:
        lz.texto("T MENOS CERO", 1060, 330, 84, "Bold Condensed", ol, "lm", esp=0.08)
        lz.texto("CADA LANZAMIENTO, EXPLICADO EN 3D", 1064, 400, 24, "SemiBold Condensed", ol * 0.9, "lm", esp=0.16)
    os_ = ap(t, ww("cierre", 3, "suscribete")) * (1 - smooth(pr(t, TOTAL - 0.6, TOTAL - 0.1)))
    if os_ > 0:
        cx, cy = 1340, 560
        tw = ancho_texto("SUSCRÍBETE", 40, "Bold Condensed", 0.12)
        x0b, x1b = cx - tw / 2 - 70, cx + tw / 2 + 30
        lz.r2(x0b, cy - 38, x1b, cy + 38, 0.0)
        lz.l2([(x0b, cy - 38), (x1b, cy - 38), (x1b, cy + 38), (x0b, cy + 38)], os_, 1.6, cerrada=True)
        bx = x0b + 36
        th = np.linspace(math.pi, 2 * math.pi, 20)
        campana = [(bx - 11, cy + 10)] + [(bx + 11 * math.cos(a), cy - 2 + 13 * math.sin(a)) for a in th] + [(bx + 11, cy + 10)]
        lz.l2(campana + [(bx - 11, cy + 10)], os_, 1.4)
        lz.c2(bx, cy + 14, 3, os_, lleno=True)
        lz.texto("SUSCRÍBETE", bx + 28, cy, 40, "Bold Condensed", os_, "lm", esp=0.12)
        lz.texto("NOS VEMOS EN EL PRÓXIMO DESPEGUE", cx, cy + 66, 22, "SemiBold Condensed", os_ * 0.85, "mm", esp=0.18)
    hud_mision(lz, 0.8)
    return lz


PLANOS = [(T0("lenta"), t_lenta), (T0("importa"), i_comparar), (F0("importa", 3) - 0.3, i_torre), (F0("importa", 6) - 0.3, i_luna),
          (T0("sigue"), s_pregunta), (F0("sigue", 2) - 0.3, s_real), (T0("cifras"), c_cifras), (T0("cierre"), c_cierre)]


def sfx():
    v = []
    # gancho y presentación
    v += [(0.3, "pulso", 0.5, 0.0, None), (ww("gancho", 0, "catorce"), "hud", 0.5, -0.3, None), (ww("gancho", 1, "veintiseis"), "tic", 0.45, -0.3, None),
          (F0("gancho", 2) - 0.3, "plasma", 0.55, 0.0, 4.0), (F0("gancho", 3) - 0.2, "brazos", 0.7, 0.0, None),
          (ww("gancho", 5, "suerte"), "explosion", 0.8, 0.0, 3.0), (F0("gancho", 6) - 0.3, "pulso", 0.8, 0.0, None),
          (ww("presenta", 0, "starbase"), "hud", 0.5, 0.3, None), (F0("presenta", 1) - 0.3, "whoosh", 0.5, 0.0, None)]
    v += [(ww("presenta", 2, "veintidos"), "hud", 0.45, 0.3, None), (ww("presenta", 3, "cuarenta"), "hud", 0.45, 0.3, None),
          (F0("presenta", 4), "tic", 0.4, 0.3, None), (ww("presenta", 5, "ciento"), "tic", 0.4, -0.3, None),
          (ww("presenta", 6, "brazos"), "brazos", 0.5, -0.3, None), (ww("presenta", 7, "veintiseis"), "tic", 0.4, 0.3, None),
          (ww("presenta", 8, "atrapar"), "hud", 0.5, 0.0, None)]
    v += [(ww("plan", 1, "primero"), "tic", 0.45, -0.2, None), (ww("plan", 2, "segundo"), "tic", 0.45, 0.0, None),
          (ww("plan", 3, "tercero"), "tic", 0.45, 0.2, None), (F0("plan", 4), "hud", 0.5, 0.0, None)]
    # despegue, Max Q, separación
    te, td = ww("despegue", 0, "encienden"), ww("despegue", 1, "despega")
    v += [(te, "ignicion", 0.9, 0.0, 4.0), (td - 0.3, "despegue", 1.0, 0.0, 6.0), (F0("despegue", 3) - 0.3, "whoosh", 0.4, 0.0, None),
          (ww("despegue", 4, "trece"), "hud", 0.4, 0.3, None), (ww("despegue", 4, "veinte"), "hud", 0.4, 0.3, None)]
    v += [(T0("maxq") + 0.2, "viento", 0.75, 0.0, 3.0), (ww("maxq", 1, "max"), "hud", 0.45, 0.3, None)]
    v += [(ww("separa", 0, "apaga"), "corte", 0.85, 0.0, 1.5), (ww("separa", 1, "enciende"), "caliente", 0.95, 0.0, 3.0),
          (ww("separa", 3, "anillo"), "hud", 0.45, 0.3, None), (F0("separa", 4) - 0.3, "whoosh", 0.4, 0.0, None)]
    # cámara lenta → cierre
    v += [(T0("lenta") + 0.2, "whoosh", 0.5, 0.0, None), (ww("lenta", 2, "cierran"), "brazos", 0.8, 0.0, None),
          (ww("lenta", 2, "cierran") + 1.3, "toque", 0.7, 0.0, None), (ww("lenta", 2, "soportes"), "hud", 0.4, 0.3, None)]
    v += [(F0("importa", 1), "whoosh", 0.4, -0.3, None), (F0("importa", 2), "whoosh", 0.4, 0.3, None),
          (ww("importa", 3, "patas"), "hud", 0.4, 0.3, None), (F0("importa", 4) + 1.0, "tic", 0.5, 0.3, None),
          (F0("importa", 5), "falla", 0.5, 0.3, None), (ww("importa", 6, "luna"), "whoosh", 0.5, 0.0, None),
          (F0("importa", 7), "hud", 0.45, 0.3, None)]
    v += [(F0("sigue", 1), "hud", 0.45, 0.0, None), (F0("sigue", 2) - 0.3, "whoosh", 0.4, 0.0, None)]
    v += [(ww("cifras", fr, pal) - 0.1, "tic", 0.5, 0.3, None) for _, _, fr, pal in CIFRAS]
    v += [(F0("cierre", 1), "pulso", 0.5, 0.0, None), (F0("cierre", 2), "whoosh", 0.45, 0.0, None),
          (ww("cierre", 3, "suscribete"), "campana", 0.6, 0.0, None)]
    return v
