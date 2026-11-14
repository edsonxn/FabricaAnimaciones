# -*- coding: utf-8 -*-
"""Planos 1: gancho, presentación, plan, despegue, Max Q y separación en caliente."""
from comun import *  # noqa: F401,F403
from comun import (ASC, CA, DH, H, M, SA, SB, W, L3, Cam, R_T, S, ap, base_de, chorro, circulo3d, clamp, cuerpo_revolucion,
                   e_inout, e_out, etiqueta3d, F0, F1, globo, hud, hud_mision, latlon_xyz, lerp, mapa_sb, marco, mision, motores_nave,
                   motores_sh, nrm, p_asc, pr, prog, real, rejilla_suelo, rnd, slerp, smooth, T0, T1, trayecto, vent, ww, fmt_t)
import math
import numpy as np

E, N, U = SB.E, SB.N, SB.U
Z_BRAZOS = 118.0                     # altura (m) de los palillos al atrapar la nave
TORRE_F = -E                          # la torre queda al oeste de la mesa: los brazos apuntan al este
P_TORRE = SB.P + E * (-22 * M)        # pie de la torre
P_MESA = SB.P + E * (14 * M)          # centro de la mesa de lanzamiento


# ------------------------------------------------------------------ piezas
def llamas_sh(lz, base, a, m, t, largo, ancho, ref, op=0.85):
    enc = motores_sh(m)
    if not enc or largo <= 0:
        return
    if len(enc) > 6:                                   # muchos motores: una pluma grande + algunas individuales
        chorro(lz, base, -a, largo * M, 7.5 * M * ancho / 6, t, n=110, op=op, semilla=3, w=1.0, abre=1.4)
        for i, p in enumerate(S.salidas_sh(base, a, M, ref, cuales=enc[::5])):
            chorro(lz, p, -a, largo * 0.5 * M, ancho * 0.25 * M, t, n=14, op=op * 0.7, semilla=i * 5, w=0.8)
    else:
        for i, p in enumerate(S.salidas_sh(base, a, M, ref, cuales=enc)):
            chorro(lz, p, -a, largo * M, ancho * 0.3 * M, t, n=40, op=op, semilla=i * 7, w=0.9)


def llamas_nave(lz, base, a, m, t, largo, ancho, ref, op=0.85, cuales=None):
    enc = motores_nave(m) if cuales is None else cuales
    for i, p in enumerate(S.salidas_nave(base, a, M, ref, cuales=enc)):
        chorro(lz, p, -a, largo * M, ancho * M * (1.4 if i >= 3 else 1.0), t, n=40, op=op, semilla=20 + i * 7, w=0.9)


def torre(lz, op=0.8, apertura=0.6, z=Z_BRAZOS, w=1.0):
    return S.torre_captura(lz, P_TORRE, U, E, M, alto=146.0, z_brazos=z, apertura=apertura, op=op, w=w, z_qd=None)


def nave_atrapada(lz, op=1.0, w=1.2, dz=0.0, flaps=0.15):
    """Nave colgada de los palillos (los pernos de captura sobre los brazos)."""
    base = P_TORRE + E * (22 * M + 13.5 * M) + U * (Z_BRAZOS - S.Z_PERNOS_NAVE + dz) * M
    S.nave(lz, base, U, M, op=op, ref=E, rot=math.pi / 2, flaps=flaps, w=w)
    return base


def boton_titulo(lz, txt, sub, x, y, op, px=96):
    lz.texto(txt, x, y, px, "Bold Condensed", op, "lm", esp=0.04)
    tw = ancho_texto(txt, px, "Bold Condensed", 0.04)
    lz.l2([(x + 4, y + px * 0.62), (x + 4 + tw * e_out(op), y + px * 0.62)], op * 0.8, 1.2)
    if sub:
        lz.texto(sub, x + 4, y + px * 0.62 + 34, 24, "SemiBold Condensed", op * 0.9, "lm", esp=0.16)


# ------------------------------------------------------------------ GANCHO
def g_real1(t):
    lz = L3(Cam((0, -10, 0), (0, 0, 0)))
    o14 = vent(t, ww("gancho", 0, "catorce") - 0.1, F1("gancho", 1) + 0.4)
    if o14 > 0:
        lz.texto("14 VUELTAS", 90, 470, 120, "Bold Condensed", o14, "lm", esp=0.04)
        lz.texto("A LA TIERRA EN 22 HORAS", 96, 560, 26, "SemiBold Condensed", o14 * 0.9, "lm", esp=0.16)
    ov = ap(t, ww("gancho", 1, "veintiseis") - 0.1)
    if ov > 0:
        lz.texto("26 400 KM/H", 96, 640, 64, "Bold Condensed", ov, "lm", esp=0.06)
    return real(t, "o5790", 1.0 + t, lz, tmision=5124 + t)


def g_real2(t):
    t0 = F0("gancho", 2) - 0.4
    lz = L3(Cam((0, -10, 0), (0, 0, 0)))
    return real(t, "reg", 225 + (t - t0), lz, rotulo="PLASMA", sub="ATRAVIESA LA ATMÓSFERA", tmision=80525 + (t - t0))


def g_real3(t):
    t0 = F0("gancho", 3) - 0.3
    s = 842.0 + (t - t0) * 1.2
    lz = L3(Cam((0, -10, 0), (0, 0, 0)))
    if s >= 848.0:
        lz.texto("ATRAPADA", 70, H - 120, 56, "Bold Condensed", ap(s, 848.0, 0.4), "lm", esp=0.06)
    return real(t, "reg", s, lz, zoom=1.15, tmision=80300 + s)


def g_captura3d(t):
    t0 = F0("gancho", 4) - 0.3
    k = pr(t, t0, F0("gancho", 5))
    foco = P_TORRE + U * 92 * M + E * 22 * M
    az = math.radians(200 + 40 * k)
    d = math.cos(math.radians(12)) * (math.sin(az) * E + math.cos(az) * N) + math.sin(math.radians(12)) * U
    cam = Cam(foco + d * lerp(0.19, 0.16, e_inout(k)), foco, U, 40, cerca=0.001, centro=(W * 0.36, H * 0.52))
    lz = L3(cam)
    rejilla_suelo(lz, SB.P, E, N, 0.6, 0.02, op=0.2)
    S.mesa_lanzamiento(lz, P_MESA, U, M, op=0.5, ref=N)
    torre(lz, 0.85, 0.0)
    nave_atrapada(lz)
    o = ap(t, ww("gancho", 4, "nunca"))
    lz.texto("PRIMERA VEZ", 1150, 420, 88, "Bold Condensed", o, "lm", esp=0.04)
    lz.texto("UNA ETAPA QUE LLEGÓ A ÓRBITA", 1154, 500, 26, "SemiBold Condensed", o * 0.9, "lm", esp=0.14)
    lz.texto("VUELVE Y ATERRIZA DE PIE", 1154, 536, 26, "SemiBold Condensed", ap(t, ww("gancho", 4, "pie")) * 0.9, "lm", esp=0.14)
    hud_mision(lz, 0.8)
    return lz


def g_booster(t):
    t0 = F0("gancho", 5) - 0.4
    tb = ww("gancho", 5, "suerte")                      # se rompe al decir «suerte»
    k = pr(t, t0, T0("gancho") + 29.2)
    mar = SB.a_mundo(30.0, -6.0, 0.0)
    alt = lerp(1.6, 0.25, smooth(pr(t, t0, tb)))
    a = nrm(U * math.cos(0.25 * math.sin(t * 1.3)) + E * 0.35 * math.sin(t * 0.9))
    base = mar + U * alt
    cam = Cam(base + (N * -0.17 + E * 0.05 + U * 0.02), base + U * 0.035, U, 40, cerca=0.001, centro=(W * 0.40, H * 0.5))
    lz = L3(cam)
    rejilla_suelo(lz, mar, E, N, 3.0, 0.12, op=0.22)
    if t < tb:
        S.super_heavy(lz, base, a, M, 1.0, 1.0, ref=N)
        llamas_sh(lz, base, a, 375, t, 40, 6, N)
    else:
        g = pr(t, tb, tb + 2.2)
        for i in range(90):                              # fragmentos
            d = nrm(np.array([rnd(i, 1) - 0.5, rnd(i, 2) - 0.5, rnd(i, 3) - 0.3]))
            d = d[0] * E + d[1] * N + d[2] * U
            c = base + a * (rnd(i, 4) * 70 * M) + d * (g * (20 + 60 * rnd(i, 5)) * M) - U * g * g * 20 * M
            q = nrm(np.cross(d, a)) * (3 + 6 * rnd(i, 6)) * M
            lz.linea(np.array([c - q, c + q]), (1 - g * 0.7) * (0.5 + 0.5 * rnd(i, 7)), 1.0)
        for j in range(3):
            cuerpo_revolucion(lz, base + a * 30 * M, U, [(0, (20 + 70 * g + 30 * j) * M), (2 * M, (18 + 70 * g + 30 * j) * M)],
                              anillos=[0], op=(1 - g) * 0.6, w=1.2, gen=0, ref=N, rellenar=False)
    o = ap(t, ww("gancho", 5, "propulsor"))
    lz.texto("SUPER HEAVY B22", 1210, 430, 64, "Bold Condensed", o, "lm", esp=0.05)
    lz.texto("NO VOLVIÓ A LA TORRE", 1214, 490, 26, "SemiBold Condensed", o * 0.9, "lm", esp=0.16)
    hud_mision(lz, 0.8)
    return lz


def g_titulo(t):
    t0 = F0("gancho", 6) - 0.4
    k = pr(t, t0, T1("gancho"))
    c = np.array([0.0, 0.0, 0.0])
    ang = 0.4 + k * 0.9
    eje = np.array([0, 0, 1.0])
    cam = Cam(np.array([math.cos(ang), math.sin(ang), 0.18]) * 210, c + eje * 62, eje, 40, cerca=0.5, centro=(W * 0.3, H * 0.5))
    lz = L3(cam)
    S.pila(lz, c, eje, 1.0, op=ap(t, t0, 0.6), ref=np.array([1.0, 0, 0]))
    o = ap(t, ww("gancho", 6, "quince") - 0.2, 0.5)
    lz.texto("STARSHIP", 1040, 420, 150, "Bold Condensed", o, "lm", esp=0.04)
    lz.texto("VUELO 15", 1046, 560, 96, "Bold Condensed", ap(t, ww("gancho", 6, "quince"), 0.5), "lm", esp=0.08)
    lz.l2([(1050, 640), (1050 + 640 * e_out(ap(t, ww("gancho", 6, "minuto"), 0.8)), 640)], o * 0.8, 1.2)
    lz.texto("MINUTO A MINUTO  ·  EN 3D", 1050, 676, 28, "SemiBold Condensed", ap(t, ww("gancho", 6, "minuto")), "lm", esp=0.2)
    lz.texto("T MENOS CERO", 1050, 760, 22, "Light Condensed", ap(t, ww("gancho", 6, "tres")) * 0.8, "lm", esp=0.4)
    return lz


# ------------------------------------------------------------------ PRESENTACIÓN
def p_mapa(t):
    t0 = T0("presenta")
    u = e_inout(pr(t, t0, F0("presenta", 1) + 0.2))
    pos0 = latlon_xyz(16.0, -86.0, R_T + 9000.0)
    pos1 = SB.a_mundo(60.0, -150.0, 70.0)
    r0, r1 = np.linalg.norm(pos0) - R_T, np.linalg.norm(pos1) - R_T
    pos = slerp(pos0, pos1, u) * (R_T + math.exp(lerp(math.log(r0), math.log(r1), u)))
    mira = SB.P * (0.55 + 0.45 * smooth(pr(u, 0.0, 0.6)))
    uc = smooth(pr(u, 0.3, 1.0))
    cam = Cam(pos, mira, nrm(np.array([0, 0, 1.0]) * (1 - uc) + U * uc), 40, cerca=0.3)
    lz = L3(cam)
    globo(lz, (0, 0, 0), R_T, op=ap(t, t0, 0.8), paso=10, op_costa=0.8 * (1 - 0.7 * uc))
    if u > 0.4:
        mapa_sb(lz, smooth(pr(u, 0.4, 0.9)))
    lz.puntos(SB.P, 4.0, 1.0)
    o = ap(t, ww("presenta", 0, "starbase")) * (1 - u * 0.0)
    etiqueta3d(lz, SB.P, "STARBASE, TEXAS", "JUNTO A LA FRONTERA CON MÉXICO", dx=150, dy=-90, op=o, px=28)
    om = ap(t, ww("presenta", 0, "mexico")) * (1 - smooth(pr(u, 0.75, 0.95)))
    for lat, lon, txt in ((31.0, -100.5, "ESTADOS UNIDOS"), (23.0, -101.0, "MÉXICO"), (25.0, -91.0, "GOLFO DE MÉXICO")):
        x, y = cam.px(latlon_xyz(lat, lon, R_T))
        if 0 < x < W and 0 < y < H:
            lz.texto(txt, x, y, 24, "SemiBold Condensed", om * 0.85, "mm", esp=0.3)
    of = vent(t, ww("presenta", 0, "viernes"), F1("presenta", 0) + 0.6)
    lz.texto("VIERNES 13 DE NOVIEMBRE", 90, 470, 60, "Bold Condensed", of, "lm", esp=0.05)
    lz.texto("16:47 HORA DEL CENTRO DE MÉXICO", 94, 530, 26, "SemiBold Condensed", of * 0.9, "lm", esp=0.14)
    hud(lz, t, reloj=ap(t, t0 + 1.0), sh=0.0, nave=0.0)
    return lz


def p_pila(t):
    t0 = F0("presenta", 1) - 0.3
    k = pr(t, t0, F0("presenta", 7))
    a5, a6 = F0("presenta", 5), F0("presenta", 6)
    foco = P_MESA + U * lerp(62, 70, smooth(pr(t, a5 - 0.5, a5 + 0.5))) * M
    az = math.radians(lerp(130, 215, k))
    el = math.radians(lerp(14, 8, k))
    dist = lerp(0.30, 0.25, e_inout(k)) + 0.06 * smooth(pr(t, a5 - 0.5, a5 + 0.5)) * (1 - smooth(pr(t, a6, a6 + 1.0)))
    cx = W * lerp(0.5, 0.38, smooth(pr(t, F0("presenta", 2) - 0.6, F0("presenta", 2))))
    d = math.cos(el) * (math.sin(az) * E + math.cos(az) * N) + math.sin(el) * U
    cam = Cam(foco + d * dist, foco, U, 40, cerca=0.001, centro=(cx, H * 0.52))
    lz = L3(cam)
    rejilla_suelo(lz, SB.P, E, N, 0.8, 0.02, op=0.18)
    S.mesa_lanzamiento(lz, P_MESA, U, M, op=0.6, ref=N)
    ab = 0.75 - 0.6 * smooth(pr(t, a6 + 0.4, a6 + 2.0)) + 0.6 * smooth(pr(t, a6 + 3.0, a6 + 4.5))
    torre(lz, 0.75 + 0.25 * vent(t, a6, F0("presenta", 7)), ab, z=95.0)
    base = P_MESA + U * 20 * M
    hb = vent(t, F0("presenta", 2), F0("presenta", 3)) * 0.0
    S.super_heavy(lz, base, U, M, 1.0, 1.0, ref=N, w=1.2 + hb)
    S.nave(lz, base + U * S.Z_NAVE * M, U, M, op=1.0, ref=N, rot=math.pi / 2, flaps=0.0)
    etiqueta3d(lz, P_MESA + U * 4 * M, "PLATAFORMA 2", "STARBASE", dx=-190, dy=60, op=vent(t, F0("presenta", 1), F0("presenta", 2) + 0.5), px=26)
    etiqueta3d(lz, base + U * 36 * M, "SUPER HEAVY B22", "33 MOTORES RAPTOR", dx=200, dy=40,
               op=vent(t, F0("presenta", 2), F0("presenta", 4)), px=28)
    etiqueta3d(lz, base + U * (S.Z_NAVE + 26) * M, "NAVE 42", "«DON'T PANIC»", dx=200, dy=-30,
               op=vent(t, F0("presenta", 3), F0("presenta", 4)), px=28)
    ob = vent(t, F0("presenta", 4), F0("presenta", 5))
    if ob > 0:
        lz.texto("BLOQUE 3", 1240, 360, 80, "Bold Condensed", ob, "lm", esp=0.05)
        for i, (txt, pal) in enumerate((("MÁS ALTA", "alta"), ("MÁS COMBUSTIBLE", "combustible"), ("RAPTOR DE 3.ª GENERACIÓN", "raptor"))):
            oi = ob * ap(t, ww("presenta", 4, pal) - 0.1)
            lz.c2(1250, 450 + i * 46, 5, oi, lleno=True)
            lz.texto(txt, 1270, 450 + i * 46, 28, "SemiBold Condensed", oi, "lm", esp=0.1)
    orr = vent(t, a5 - 0.2, a6 + 0.4)
    if orr > 0:                                        # regla de altura + edificio de 40 pisos
        lado = N * -1.0
        x0 = P_MESA + lado * 24 * M
        uu = e_out(pr(t, a5 - 0.2, a5 + 1.4))
        lz.linea(np.array([x0, x0 + U * (20 + 104.4 * uu) * M]), orr, 1.6)
        for z in range(0, 125, 10):
            if z <= 20 + 104.4 * uu:
                lz.linea(np.array([x0 + U * z * M, x0 + U * z * M + E * 3 * M]), orr * 0.7, 1.0)
        x, y = cam.px(x0 + U * 126 * M)
        lz.texto("124 M", x, y - 20, 46, "Bold Condensed", orr * uu, "mm", esp=0.06, fondo=True)
        ed = ap(t, ww("presenta", 5, "edificio"))
        if ed > 0:
            b0 = P_MESA + lado * 50 * M - E * 10 * M
            for p in range(40):
                z = p * 3.0
                q = [b0 + U * z * M, b0 + U * z * M + E * 20 * M, b0 + U * z * M + E * 20 * M + lado * 14 * M, b0 + U * z * M + lado * 14 * M]
                lz.linea(np.array(q), ed * (0.5 if p % 5 else 0.8) * ap(t, ww("presenta", 5, "edificio") + p * 0.02, 0.2), 0.8, cerrada=True)
            x, y = cam.px(b0 + U * 125 * M + E * 10 * M)
            lz.texto("40 PISOS", x, y - 12, 26, "SemiBold Condensed", ed, "mm", esp=0.16)
    etiqueta3d(lz, P_TORRE + U * 95 * M + E * 30 * M, "LOS PALILLOS", "BRAZOS DE CAPTURA", dx=-220, dy=-80,
               op=vent(t, ww("presenta", 6, "brazos"), F0("presenta", 7) + 0.3), px=28)
    hud(lz, t, sh=0.0, nave=0.0)
    return lz


def p_carga(t):
    t0 = F0("presenta", 7) - 0.3
    k = pr(t, t0, F0("presenta", 8))
    base = P_MESA + U * (20 + S.Z_NAVE) * M
    foco = base + U * 26 * M
    az = math.radians(lerp(250, 280, k))
    d = math.cos(0.1) * (math.sin(az) * E + math.cos(az) * N) + math.sin(0.1) * U
    cam = Cam(foco + d * lerp(0.11, 0.095, k), foco, U, 40, cerca=0.0005, centro=(W * 0.4, H * 0.5))
    lz = L3(cam)
    S.nave(lz, base, U, M, op=0.45, ref=N, rot=math.pi / 2, flaps=0.0, escudo=False)
    n = int(26 * e_out(pr(t, ww("presenta", 7, "veintiseis") - 0.2, ww("presenta", 7, "veintiseis") + 1.6)))
    for i in range(n):
        z = 15.0 + i * 0.75
        c = base + U * z * M
        q = [c + (E * sx * 3.2 + N * sy * 1.4) * M for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        lz.relleno(np.array(q), 0.0)
        lz.linea(np.array(q), 0.9, 1.0, cerrada=True)
    o = ap(t, ww("presenta", 7, "veintiseis"))
    lz.texto(f"{n}", 1200, 420, 140, "Bold Condensed", o, "lm", esp=0.04)
    lz.texto("SATÉLITES STARLINK", 1206, 520, 30, "SemiBold Condensed", o, "lm", esp=0.14)
    lz.texto("DE NUEVA GENERACIÓN (V3)", 1206, 560, 24, "SemiBold Condensed", o * 0.85, "lm", esp=0.14)
    hud(lz, t, sh=0.0, nave=0.0)
    return lz


def p_meta(t):
    t0 = F0("presenta", 8) - 0.3
    k = pr(t, t0, T1("presenta"))
    foco = P_TORRE + U * 70 * M + N * 0.0
    cam = Cam(foco + (E * 0.36 - N * 0.10 + U * 0.02), foco + E * 0.03, U, 40, cerca=0.001)
    lz = L3(cam)
    rejilla_suelo(lz, SB.P, E, N, 0.7, 0.02, op=0.16)
    for j, (dn, tipo) in enumerate(((0.06, "sh"), (-0.06, "nave"))):
        sh = N * dn
        ab = 0.0
        S.torre_captura(lz, P_TORRE + sh, U, E, M, alto=146.0, z_brazos=Z_BRAZOS if tipo == "nave" else 90.0, apertura=ab, op=0.7)
        oj = ap(t, F0("presenta", 8) + j * 0.5)
        if tipo == "sh":
            b = P_TORRE + sh + E * 35.5 * M + U * (90.0 - S.Z_PERNOS_SH) * M
            S.super_heavy(lz, b, U, M, 1.0, oj, ref=E)
        else:
            b = P_TORRE + sh + E * 35.5 * M + U * (Z_BRAZOS - S.Z_PERNOS_NAVE) * M
            S.nave(lz, b, U, M, op=oj, ref=E, rot=math.pi / 2, flaps=0.15)
        x, y = cam.px(P_TORRE + sh + U * 160 * M)
        lz.texto("PROPULSOR" if tipo == "sh" else "NAVE", x, y - 10, 30, "SemiBold Condensed", oj, "mm", esp=0.2)
    o = ap(t, ww("presenta", 8, "meta"))
    lz.texto("LA META", W / 2, 760, 34, "SemiBold Condensed", o * 0.85, "mm", esp=0.3)
    lz.texto("ATRAPAR LAS DOS ETAPAS", W / 2, 830, 72, "Bold Condensed", ap(t, ww("presenta", 8, "atrapar")), "mm", esp=0.05)
    hud(lz, t, sh=0.0, nave=0.0)
    return lz


# ------------------------------------------------------------------ PLAN (diagrama)
def pl_plan(t):
    lz = L3(Cam((0, -10, 0), (0, 0, 0)))
    o = ap(t, T0("plan") + 0.1, 0.5)
    cx, cy, R = W / 2, 2600.0, 1900.0                      # arco de la Tierra
    A = np.linspace(-0.55, 0.55, 200)
    tierra = np.stack([cx + R * np.sin(A), cy - R * np.cos(A)], 1)
    lz.l2(tierra, o * 0.8, 1.6)
    Ro = R + 420
    orb = np.stack([cx + Ro * np.sin(A), cy - Ro * np.cos(A)], 1)
    lz.l2(orb, o * 0.35, 1.0)
    lz.texto("ÓRBITA · ~275 KM", cx + Ro * math.sin(0.42), cy - Ro * math.cos(0.42) - 26, 20, "SemiBold Condensed", o * 0.6, "mm", esp=0.2)

    def pt(a, r):
        return cx + r * math.sin(a), cy - r * math.cos(a)
    a_sb = -0.32
    xs, ys = pt(a_sb, R)
    lz.l2([(xs - 6, ys), (xs - 6, ys - 60), (xs + 6, ys - 60), (xs + 6, ys)], o, 1.4)        # torre
    lz.l2([(xs + 6, ys - 52), (xs + 26, ys - 52)], o, 1.4)
    lz.texto("STARBASE", xs, ys + 36, 24, "SemiBold Condensed", o, "mm", esp=0.2)
    # 1: ascenso y regreso del propulsor
    k1 = e_out(pr(t, ww("plan", 1, "propulsor"), F1("plan", 1)))
    asc = [pt(a_sb + 0.11 * q ** 1.2, R + 190 * (1 - (1 - q) ** 2)) for q in np.linspace(0, 1, 60)]
    lz.l2(asc[:max(2, int(60 * min(1, k1 * 2)))], o, 2.0)
    if k1 > 0.5:
        q2 = (k1 - 0.5) * 2
        xa, ya = asc[-1]
        ret = [(lerp(xa, xs + 14, q) + 60 * math.sin(math.pi * q), lerp(ya, ys - 60, q ** 1.4) - 50 * math.sin(math.pi * q))
               for q in np.linspace(0, 1, 60)]
        lz.l2(ret[:max(2, int(60 * q2))], o, 1.6)
    o1 = ap(t, ww("plan", 1, "primero"))
    xa, ya = asc[-1]
    lz.c2(xa + 70, ya - 40, 26, o1, w=1.4)
    lz.texto("1", xa + 70, ya - 40, 32, "Bold Condensed", o1, "mm")
    # 2: la nave sigue a la órbita, x14
    k2 = e_out(pr(t, ww("plan", 2, "nave"), F1("plan", 2)))
    if k2 > 0:
        up = [(lerp(xa, pt(0.0, Ro)[0], q), lerp(ya, pt(0.0, Ro)[1], q ** 0.7)) for q in np.linspace(0, 1, 40)]
        lz.l2(up[:max(2, int(40 * min(1, k2 * 1.6)))], o, 2.0)
        if k2 > 0.6:
            q3 = (k2 - 0.6) / 0.4
            arc = [pt(a, Ro) for a in np.linspace(0.0, 0.0 + 0.5 * q3, 40)]
            lz.l2(arc, o, 2.0)
    o2 = ap(t, ww("plan", 2, "segundo"))
    x2, y2 = pt(0.05, Ro + 90)
    lz.c2(x2, y2, 26, o2, w=1.4)
    lz.texto("2", x2, y2, 32, "Bold Condensed", o2, "mm")
    lz.texto("× 14 VUELTAS", x2 + 44, y2, 30, "SemiBold Condensed", ap(t, ww("plan", 2, "catorce")), "lm", esp=0.12)
    # 3: regreso de la nave
    k3 = e_out(pr(t, ww("plan", 3, "regresa"), F1("plan", 3)))
    if k3 > 0:
        ret = [(lerp(pt(-0.5, Ro)[0], xs + 14, q) - 40 * math.sin(math.pi * q), lerp(pt(-0.5, Ro)[1], ys - 64, q ** 1.6))
               for q in np.linspace(0, 1, 60)]
        lz.l2(ret[:max(2, int(60 * k3))], o, 2.0, )
    o3 = ap(t, ww("plan", 3, "tercero"))
    x3, y3 = pt(-0.47, Ro - 40)
    lz.c2(x3, y3, 26, o3, w=1.4)
    lz.texto("3", x3, y3, 32, "Bold Condensed", o3, "mm")
    o4 = ap(t, F0("plan", 4))
    lz.texto("NINGUNA TOCA EL SUELO", W / 2, 150, 64, "Bold Condensed", o4, "mm", esp=0.05)
    lz.texto("NI EL MAR", W / 2, 214, 30, "SemiBold Condensed", ap(t, ww("plan", 4, "mar")) * 0.9, "mm", esp=0.3)
    lz.texto("EL PLAN", 90, 150, 30, "SemiBold Condensed", o * (1 - o4), "lm", esp=0.3)
    hud_mision(lz, 0.8)
    return lz


# ------------------------------------------------------------------ DESPEGUE
def d_real(t):
    te, td = ww("despegue", 0, "encienden"), ww("despegue", 1, "despega")
    s = float(np.interp(t, [T0("despegue"), te, td, td + 20], [69.0, 73.5, 76.5, 96.5]))
    m = s - 76.5
    lz = L3(Cam((0, -10, 0), (0, 0, 0)))
    rot, sub = None, None
    if t > te - 0.1 and t < td - 0.2:
        rot, sub = "IGNICIÓN", "T- 3 S · 33 RAPTOR"
    elif td - 0.2 <= t < F0("despegue", 2):
        rot, sub = "DESPEGUE", "16:47:36 HORA DEL CENTRO"
    elif t >= F0("despegue", 2):
        rot, sub = "EL COHETE MÁS POTENTE", "DE LA HISTORIA"
    return real(t, "lanz", s, lz, zoom=1.2, cy=0.40, rotulo=rot, sub=sub, tmision=m)


def d_abajo(t):
    t0 = F0("despegue", 3) - 0.3
    m = mision(t)
    k = pr(t, t0, T1("despegue"))
    base = SB.P + U * 0.6 * (t - t0) * M
    ang = 0.3 * k
    ci = Cam(base - U * 0.034 + E * 0.004 * math.cos(ang) + N * 0.004 * math.sin(ang), base + U * 0.02, N, 40, cerca=0.0005,
             centro=(W * 0.40, H * 0.5))
    lz = L3(ci)
    S.super_heavy(lz, base, U, M, 1.0, 0.8, ref=E, motores=False)
    lz.linea(circulo3d(base + U * 1.6 * M, U, 4.5 * M, 120), 0.9, 1.6, cerrada=True)
    t13 = ww("despegue", 4, "trece")
    t20 = ww("despegue", 4, "veinte")
    for i, (kk, mx, my, rt) in enumerate(S.motores_sh()):
        c = base + (E * mx + N * my) * M
        x, y = ci.px(c)
        r = ci.escala(c) * 0.62 * M
        fl = 0.75 + 0.25 * math.sin(t * 37 + i * 2.3)
        centro = kk < 2
        hi = vent(t, t13, t20) if centro else ap(t, t20)
        dim = 1.0 - 0.6 * vent(t, t13, t20) * (0.0 if centro else 1.0)
        lz.c2(x, y, r * 0.8, dim, w=1.2 + 1.2 * hi)
        lz.c2(x, y, r * 0.42 * fl, (0.55 + 0.35 * fl) * dim, lleno=True)
        if centro and hi > 0:                          # flechas de giro en los 13 centrales
            a0 = t * 2.0 + i
            lz.l2([(x + r * 1.5 * math.cos(a0 + q), y + r * 1.5 * math.sin(a0 + q)) for q in np.linspace(0, 1.4, 10)], hi * 0.8, 1.2)
    xc, yc = ci.px(base)
    lz.texto("VISTA DESDE ABAJO", xc, 120, 26, "SemiBold Condensed", ap(t, t0), "mm", esp=0.3)
    o13 = ap(t, t13)
    lz.texto("13 CENTRALES", 1300, 420, 56, "Bold Condensed", o13, "lm", esp=0.05)
    lz.texto("GIRAN PARA DIRIGIR EL COHETE", 1304, 474, 24, "SemiBold Condensed", o13 * 0.9, "lm", esp=0.14)
    o20 = ap(t, t20)
    lz.texto("20 EXTERIORES", 1300, 580, 56, "Bold Condensed", o20, "lm", esp=0.05)
    lz.texto("FIJOS: SOLO EMPUJAN", 1304, 634, 24, "SemiBold Condensed", o20 * 0.9, "lm", esp=0.14)
    hud(lz, t)
    return lz


# ------------------------------------------------------------------ MAX Q
def q_maxq(t):
    m = mision(t)
    tq = ww("maxq", 0, "potencia")
    p = p_asc(m)
    a = prog(p_asc, m) if m > 5 else U
    e, n, u = marco(p)
    side = nrm(np.cross(DH, u))
    k = pr(t, T0("maxq"), T1("maxq"))
    ctr = p + a * 62 * M
    cam = Cam(ctr + side * lerp(0.30, 0.26, k) - u * 0.03 + DH * 0.05, ctr, u, 40, cerca=0.0005, centro=(W * 0.36, H * 0.5))
    lz = L3(cam)
    q = math.exp(-((m - 58) / 16) ** 2)
    nose = p + a * 124.4 * M
    oq = ap(t, T0("maxq")) * (0.35 + 0.65 * q)
    for j in range(4):
        fase = (t * 1.5 + j / 4) % 1.0
        largo = (16 + 40 * fase) * M
        ancho = (4.5 + (8 + 14 * q) * fase) * M
        cuerpo_revolucion(lz, nose - a * largo, a, [(0, ancho), (largo, 0.4 * M)], anillos=[], op=oq * (1 - fase), w=1.4, gen=0,
                          ref=N, rellenar=False)
    uu, vv = base_de(a, u)
    for i in range(26):
        ang = 2 * math.pi * i / 26
        d = math.cos(ang) * uu + math.sin(ang) * vv
        if (cam.pos - p) @ d < 0:
            continue
        z = ((rnd(i, 1) - t * (1.2 + q)) % 1.0) * 140 - 15
        q0 = p + a * z * M + d * (5 + 5 * rnd(i, 2) + 6 * q) * M
        lz.linea(np.array([q0, q0 - a * (8 + 10 * rnd(i, 3)) * M]), oq * 0.6 * rnd(i, 4), 0.8)
    emp = 1.0 - 0.3 * smooth(pr(m, 52, 58)) * (1 - smooth(pr(m, 66, 75)))
    llamas_sh(lz, p, a, m, t, 140 * emp, 10 * emp, N)
    S.pila(lz, p, a, M, ref=N)
    gx, gy, gw, gh = 1260, 280, 520, 220
    og = ap(t, F0("maxq", 1) - 0.4)
    if og > 0:
        lz.texto("PRESIÓN DEL AIRE SOBRE EL COHETE", gx, gy - 24, 20, "SemiBold Condensed", og * 0.85, "lb", esp=0.2)
        lz.l2([(gx, gy), (gx, gy + gh), (gx + gw, gy + gh)], og * 0.6, 1.0)
        xs = np.linspace(0, 140, 120)
        ys = np.exp(-((xs - 58) / 26) ** 2) * (xs / 58) ** 0.5
        pts = np.stack([gx + xs / 140 * gw, gy + gh - ys / ys.max() * gh * 0.9], 1)
        hasta = int(np.clip(m / 140 * 120, 2, 120))
        lz.l2(pts[:hasta], og, 1.8)
        if m >= 57:
            x58 = gx + 58 / 140 * gw
            lz.l2([(x58, gy + gh), (x58, gy + gh * 0.1)], og * 0.5, 1.0)
            lz.texto("MAX-Q  ·  T+ 00:00:58", x58 + 14, gy + gh * 0.1, 24, "SemiBold Condensed", og, "lm", esp=0.1)
    oe = ap(t, tq - 0.3)
    if oe > 0:                                         # barra de empuje que baja y vuelve
        bx, by = 1160, 620
        lz.texto("EMPUJE", bx, by - 18, 20, "SemiBold Condensed", oe * 0.85, "lb", esp=0.2)
        lz.l2([(bx, by), (bx + 420, by), (bx + 420, by + 26), (bx, by + 26)], oe * 0.6, 1.0, cerrada=True)
        lz.r2(bx + 3, by + 3, bx + 3 + 414 * emp, by + 23, 0.85 * oe)
        lz.texto("BAJA" if emp < 0.97 and m < 62 else ("VUELVE A ACELERAR" if m >= 62 else ""), bx + 436, by + 13, 24,
                 "SemiBold Condensed", oe, "lm", esp=0.12)
    hud(lz, t)
    return lz


# ------------------------------------------------------------------ SEPARACIÓN EN CALIENTE
def s_caliente(t):
    m = mision(t)
    t_ap, t_enc = ww("separa", 0, "apaga"), ww("separa", 1, "enciende")
    t_ani = ww("separa", 3, "anillo")
    p = p_asc(min(m, 139.0)) + prog(p_asc, 139.0) * 0.0
    a = prog(p_asc, 139.0)
    e, n, u = marco(p)
    side = nrm(np.cross(a, u))
    sep = 0.0 if m < 142.0 else (m - 142.0) ** 1.7 * 6.0             # metros que se aleja la nave
    zi = S.ALTO_SH                                                   # anillo de separación
    k1 = smooth(pr(t, t_enc - 0.5, t_enc + 1.0))
    k2 = smooth(pr(t, t_ani - 0.6, t_ani + 0.8))
    foco = p + a * lerp(lerp(62, 74, k1), 72, k2) * M
    dist = lerp(lerp(0.30, 0.16, k1), 0.07, k2)
    cam = Cam(foco + nrm(side + a * 0.2 - u * 0.15) * dist, foco, u, 40, cerca=0.0003, centro=(W * 0.42, H * 0.5))
    lz = L3(cam)
    pl = 1 - smooth(pr(t, t_ap, t_ap + 0.4))
    llamas_sh(lz, p, a, m, t, 150 * pl + 40, 10 * pl + 3, N)
    S.super_heavy(lz, p, a, M, 1.0, 1.0, ref=N)
    bn = p + a * (S.Z_NAVE + sep) * M
    if m >= 141.0:
        g = ap(m, 141.0, 0.6)
        llamas_nave(lz, bn, a, m, t, 18 + 30 * pr(m, 141, 146), 1.6, N, op=0.9)
        uu, vv = base_de(a, N)
        for i in range(48):                                          # fuego que escapa por las rejillas del anillo
            ang = 2 * math.pi * i / 48 + t * 0.6
            d = math.cos(ang) * uu + math.sin(ang) * vv
            z0 = zi - 1.5 + rnd(i, 3) * 1.5
            q0 = p + (a * z0 + d * 4.6) * M
            ll = (4 + 9 * rnd(i, 4)) * (0.6 + 0.4 * math.sin(t * 20 + i)) * g * (1 - pr(m, 142, 145))
            if ll > 0.2:
                lz.linea(np.array([q0, q0 + (d * ll - a * ll * 0.4) * M]), 0.85 * rnd(i, 5) + 0.15, 1.0)
    S.nave(lz, bn, a, M, op=1.0, ref=N, rot=math.pi / 2, flaps=0.0)
    etiqueta3d(lz, p + a * 30 * M, "MECO", "T+ 00:02:19 · QUEDAN 3 MOTORES", dx=-240, dy=120,
               op=vent(t, t_ap, t_enc - 0.2), px=26)
    etiqueta3d(lz, p + a * zi * M, "SEPARACIÓN EN CALIENTE", "T+ 00:02:21", dx=210, dy=-120,
               op=vent(t, ww("separa", 2, "separacion"), t_ani), px=28)
    etiqueta3d(lz, p + a * (zi - 1.5) * M, "ANILLO DE REJILLAS", "POR AQUÍ SALE EL FUEGO", dx=200, dy=-110,
               op=vent(t, t_ani, F0("separa", 4) + 0.2), px=28)
    hud(lz, t)
    return lz


def s_real(t):
    t0 = F0("separa", 4) - 0.3
    s = 214.0 + (t - t0)
    lz = L3(Cam((0, -10, 0), (0, 0, 0)))
    rot = "LA NAVE YA EMPUJA SOLA" if t < F0("separa", 5) else "CADA ETAPA, SU CAMINO"
    return real(t, "lanz", s, lz, rotulo=rot, sub="CÁMARA A BORDO DE LA NAVE", tmision=s - 76.5)
