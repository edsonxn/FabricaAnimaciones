# -*- coding: utf-8 -*-
"""Planos 2: el propulsor (aborto y pérdida), la nave a órbita, Starlink, las 14 vueltas, la reentrada y la llegada."""
from comun import *  # noqa: F401,F403
from comun import (BOO, DH, H, M, R_T, SB, W, L3, Cam, S, ap, base_de, chorro, circulo3d, clamp, cuerpo_revolucion, e_inout, e_out,
                   etiqueta3d, F0, F1, globo, hud, hud_mision, latlon_xyz, lerp, mapa_sb, marco, mision, motores_nave, motores_sh, nrm,
                   orbita_eci, oculto_tierra, p_asc, p_boo, pr, prog, real, rejilla_suelo, rnd, slerp, smooth, T0, T1, trayecto, vent,
                   ww, fmt_t, ancho_texto, PERIODO, R_ORB, INC, W_T, FALLA)
import math
import numpy as np

import planos1 as P1

E, N, U = SB.E, SB.N, SB.U


def _vacio():
    return L3(Cam((0, -10, 0), (0, 0, 0)))


def texto_bloque(lz, x, y, titulo, sub, op, px=64):
    lz.texto(titulo, x, y, px, "Bold Condensed", op, "lm", esp=0.05)
    if sub:
        lz.texto(sub, x + 4, y + px * 0.62 + 6, 24, "SemiBold Condensed", op * 0.9, "lm", esp=0.14)


# ------------------------------------------------------------------ PROPULSOR
def eje_boo(m):
    pro = prog(p_asc, 139.0)
    p = p_boo(m)
    up = nrm(p)
    atras = nrm(-DH * 0.9 + up * 0.45)
    if m < 141.5:
        return pro
    if m < 182:
        return slerp(pro, atras, e_inout(pr(m, 141.5, 146.0)))
    return slerp(atras, up, e_inout(pr(m, 182, 230)))


def b_vuelta(t):
    m = mision(t)
    p = p_boo(m)
    a = eje_boo(m)
    e, n, u = marco(p)
    side = nrm(np.cross(DH, u))
    foco = p + a * 36 * M
    cam = Cam(foco + (side * 0.15 + u * 0.03 - DH * 0.03), foco, u, 40, cerca=0.0005, centro=(W * 0.42, H * 0.5))
    lz = L3(cam)
    P1.llamas_sh(lz, p, a, m, t, 90, 9, N)
    S.super_heavy(lz, p, a, M, 1.0, 1.0, ref=N)
    og = vent(t, F0("propulsor", 1), ww("propulsor", 1, "enciende"))
    if og > 0:
        c = p + a * 36 * M
        arc = circulo3d(c, side, 48 * M, 50, 0.4, 2.7, ref=a)
        lz.linea(arc, og * 0.8, 1.4, guion=2)
    etiqueta3d(lz, p + a * 60 * M, "MEDIA VUELTA", "EN EL VACÍO", dx=200, dy=-90, op=vent(t, ww("propulsor", 1, "media"), ww("propulsor", 1, "enciende")), px=28)
    etiqueta3d(lz, p + a * 4 * M, "QUEMA DE REGRESO", "T+ 00:02:26", dx=200, dy=90, op=ap(t, ww("propulsor", 1, "enciende")), px=28)
    hud(lz, t)
    return lz


def b_falla(t):
    t0 = F0("propulsor", 2) - 0.3
    lz = _vacio()
    m = mision(t)
    cx, cy, k = 700, 470, 62.0
    lz.c2(cx, cy, 4.6 * k, 0.8, w=1.6)
    enc = set(motores_sh(m))
    for i, (kk, mx, my, rt) in enumerate(S.motores_sh()):
        x, y = cx + mx * k, cy + my * k
        on = i in enc
        lz.c2(x, y, 0.5 * k, 1.0 if on else 0.5, w=1.4)
        if on:
            lz.c2(x, y, 0.28 * k * (0.85 + 0.15 * math.sin(t * 30 + i)), 0.8, lleno=True)
        if i == FALLA:
            bl = 0.6 + 0.4 * (math.sin(t * 8) > 0)
            r = 0.55 * k
            lz.l2([(x - r, y - r), (x + r, y + r)], bl, 2.4)
            lz.l2([(x - r, y + r), (x + r, y - r)], bl, 2.4)
            lz.c2(x, y, 0.95 * k, bl * 0.8, w=1.6)
            lz.l2([(x + 0.95 * k, y - 0.3 * k), (1180, 380)], 0.7, 1.0)
    lz.texto("VISTA DESDE ABAJO · QUEMA DE REGRESO", cx, 120, 24, "SemiBold Condensed", ap(t, t0), "mm", esp=0.25)
    o = ap(t, ww("propulsor", 2, "uno"))
    texto_bloque(lz, 1190, 360, "UN MOTOR", "NO VUELVE A ENCENDER", o, 80)
    lz.texto("32 DE 33 ENCENDIDOS", 1194, 470, 30, "SemiBold Condensed", o * 0.85, "lm", esp=0.12)
    hud(lz, t, sh=1.0)
    return lz


def b_cae(t):
    m = mision(t)
    t4, t5 = F0("propulsor", 4), F0("propulsor", 5)
    p = p_boo(m)
    a = eje_boo(m)
    e, n, u = marco(p)
    side = nrm(np.cross(DH, u))
    foco = p + a * 40 * M
    cam = Cam(foco + (side * 0.26 - DH * 0.06 - u * 0.02), foco, u, 40, cerca=0.0005, centro=(W * 0.40, H * 0.5))
    lz = L3(cam)
    vel = 1 - 0.6 * smooth(pr(m, 365, 372))
    for i in range(44):
        ang = rnd(i, 1) * 2 * math.pi
        rr = (8 + 50 * rnd(i, 2)) * M
        d = math.cos(ang) * e + math.sin(ang) * n
        z = ((rnd(i, 3) + t * 1.4) % 1.0) * 170 - 40
        q = p + d * rr + u * z * M
        lz.linea(np.array([q, q + u * (10 + 12 * rnd(i, 4)) * M]), vel * 0.35 * rnd(i, 5), 0.8)
    P1.llamas_sh(lz, p, a, m, t, 45, 6, N)
    S.super_heavy(lz, p, a, M, 1.0, 1.0, ref=N)
    etiqueta3d(lz, p + a * 8 * M, "CAE DE COLA", "MÁS DE 3 MINUTOS SIN MOTORES", dx=210, dy=80,
               op=vent(t, ww("propulsor", 3, "cae"), t4), px=28)
    etiqueta3d(lz, p + a * 67 * M, "3 ALETAS DE REJILLA", "LO GUÍAN EN LA CAÍDA", dx=-230, dy=-60,
               op=vent(t, ww("propulsor", 3, "aletas") - 0.2, t4 + 0.5), px=28)
    etiqueta3d(lz, p + a * 4 * M, "QUEMA DE ATERRIZAJE", "T+ 00:06:10 · RUMBO A LA TORRE", dx=210, dy=80, op=ap(t, ww("propulsor", 4, "enciende")), px=28)
    o5 = ap(t, t5)
    if o5 > 0:
        lz.texto("ANTES YA LO HABÍAN LOGRADO", 1210, 300, 40, "Bold Condensed", o5, "lm", esp=0.05)
        lz.texto("CAPTURAS DE PROPULSOR EN VUELOS ANTERIORES", 1214, 346, 20, "SemiBold Condensed", o5 * 0.85, "lm", esp=0.14)
    hud(lz, t)
    return lz


def p_boo_plan(m):
    """Ruta prevista: de la quema de aterrizaje a la torre."""
    s, h = BOO(min(m, 370.0))
    q = clamp((m - 370.0) / 30.0)
    return SB.gran_circulo(97.0, s * (1 - q) ** 1.5, h * (1 - q) ** 2 + 0.06 * q)


def b_mapa(t):
    m = mision(t)
    t_ab = ww("propulsor", 7, "aborta")
    k = pr(t, F0("propulsor", 6) - 0.3, F0("propulsor", 9))
    foco = SB.a_mundo(5.0, -1.0, 0.0)
    cam = Cam(foco + (-N * 14.0 + U * 40.0 - E * 2.0) * lerp(1.0, 0.85, k), foco, N, 40, cerca=0.01, centro=(W * 0.40, H * 0.52))
    lz = L3(cam)
    rejilla_suelo(lz, foco, E, N, 30.0, 1.0, op=0.12)
    mapa_sb(lz, 1.0)
    P1.torre(lz, 0.9, 0.7)
    lz.linea(circulo3d(SB.P, U, 0.5, 64), 0.7, 1.2, cerrada=True)
    etiqueta3d(lz, SB.P, "TORRE · PLATAFORMA 2", None, dx=-200, dy=-70, op=ap(t, F0("propulsor", 6)), px=26)
    trayecto(lz, p_boo_plan, 330, 400, 0.5 * (1 - ap(t, t_ab)), 1.2, guion=4, n=100)
    trayecto(lz, p_boo, 300, max(m, 300.5), 1.0, 1.8, n=120)
    p = p_boo(m)
    lz.puntos(p, 5.0, 1.0)
    S.super_heavy(lz, p, nrm(p), M * 6, 1.0, 0.9, ref=N, motores=False)
    oa = ap(t, t_ab)
    etiqueta3d(lz, p, "ABORTO AUTOMÁTICO", "NO ESTABA DONDE DEBÍA ESTAR", dx=180, dy=-120, op=oa * (1 - ap(t, F0("propulsor", 9))), px=30)
    x, y = cam.px(SB.a_mundo(16.0, -6.0, 0.0))
    lz.texto("GOLFO DE MÉXICO", x, y, 28, "SemiBold Condensed", ap(t, ww("propulsor", 7, "golfo")) * 0.9, "mm", esp=0.3)
    om = ap(t, F0("propulsor", 8))
    if om > 0:
        lz.texto("ELON MUSK", 1250, 600, 24, "SemiBold Condensed", om * 0.8, "lm", esp=0.3)
        lz.texto("«BAJO RENDIMIENTO»", 1250, 650, 48, "Bold Condensed", om, "lm", esp=0.04)
        lz.texto("Y POCO COMBUSTIBLE", 1254, 698, 24, "SemiBold Condensed", om * 0.9, "lm", esp=0.14)
        os_ = ap(t, ww("propulsor", 8, "spacex"))
        lz.texto("SPACEX: AÚN INVESTIGA LA CAUSA", 1254, 760, 26, "SemiBold Condensed", os_, "lm", esp=0.12)
    hud(lz, t)
    return lz


def b_rompe(t):
    t0 = F0("propulsor", 9) - 0.3
    tb = ww("propulsor", 9, "desintegra")
    mar = SB.a_mundo(8.0, -1.0, 0.0)
    alt = lerp(0.5, 0.08, smooth(pr(t, t0, tb)))
    a = nrm(U + E * 0.15 * math.sin(t * 0.8))
    base = mar + U * alt
    cam = Cam(base + (-N * 0.20 + E * 0.06 + U * 0.03), base + U * 0.03, U, 40, cerca=0.001, centro=(W * 0.40, H * 0.5))
    lz = L3(cam)
    rejilla_suelo(lz, mar, E, N, 3.0, 0.08, op=0.2)
    if t < tb:
        S.super_heavy(lz, base, a, M, 1.0, 1.0, ref=N)
    else:
        g = pr(t, tb, tb + 2.6)
        for i in range(110):
            d = nrm(np.array([rnd(i, 1) - 0.5, rnd(i, 2) - 0.5, rnd(i, 3) - 0.3]))
            d = d[0] * E + d[1] * N + d[2] * U
            c = base + a * (rnd(i, 4) * 70 * M) + d * (g * (20 + 70 * rnd(i, 5)) * M) - U * g * g * 25 * M
            q = nrm(np.cross(d, a)) * (3 + 6 * rnd(i, 6)) * M
            lz.linea(np.array([c - q, c + q]), (1 - g * 0.7) * (0.5 + 0.5 * rnd(i, 7)), 1.0)
        for j in range(3):
            cuerpo_revolucion(lz, base + a * 30 * M, U, [(0, (20 + 80 * g + 30 * j) * M), (2 * M, (18 + 80 * g + 30 * j) * M)],
                              anillos=[0], op=(1 - g) * 0.6, w=1.2, gen=0, ref=N, rellenar=False)
    o = ap(t, tb)
    texto_bloque(lz, 1200, 420, "SE DESINTEGRA", "ANTES DE TOCAR EL AGUA", o, 70)
    hud(lz, t)
    return lz


def b_torre(t):
    t0 = F0("propulsor", 10) - 0.3
    k = pr(t, t0, T1("propulsor"))
    foco = P1.P_TORRE + U * 80 * M + E * 15 * M
    cam = Cam(foco + (E * 0.20 - N * 0.16 + U * 0.02), foco, U, 40, cerca=0.001, centro=(W * 0.38, H * 0.5))
    lz = L3(cam)
    rejilla_suelo(lz, SB.P, E, N, 0.6, 0.02, op=0.18)
    S.mesa_lanzamiento(lz, P1.P_MESA, U, M, op=0.5, ref=N)
    P1.torre(lz, 0.9, 0.85, z=90.0)
    o = ap(t, t0 + 0.2)
    texto_bloque(lz, 1180, 420, "CAPTURA DOBLE", "PENDIENTE", o, 76)
    hud(lz, t, reloj=1 - k * 0.0)
    return lz


# ------------------------------------------------------------------ ÓRBITA
def o_nave(t):
    m = mision(t)
    t0 = T0("orbita")
    p = p_asc(m)
    a = prog(p_asc, m)
    e, n, u = marco(p)
    side = nrm(np.cross(a, u))
    foco = p + a * 10 * M
    cam = Cam(foco - a * 0.075 + side * 0.035 - u * 0.012, foco + a * 0.01, u, 40, cerca=0.0003, centro=(W * 0.40, H * 0.5))
    lz = L3(cam)
    globo(lz, (0, 0, 0), R_T, paso=5, op_rej=0.12, op_costa=0.5, limbo=0.6)
    P1.llamas_nave(lz, p, a, m, t, 60, 1.8, N)
    S.nave(lz, p, a, M, op=1.0, ref=u, rot=0.0, flaps=0.0)
    o3 = ap(t, ww("orbita", 0, "tres"))
    sal = S.salidas_nave(p, a, M, ref=u)
    if o3 > 0:
        x, y = cam.px(sal[0])
        lz.l2([(x, y), (1180, 330)], o3 * 0.6, 1.0)
        texto_bloque(lz, 1190, 320, "3 PARA EL AIRE", "RAPTOR DE NIVEL DEL MAR · AL CENTRO", o3, 48)
    o4 = ap(t, ww("orbita", 0, "vacio"))
    if o4 > 0:
        x, y = cam.px(sal[4])
        lz.l2([(x, y), (1180, 520)], o4 * 0.6, 1.0)
        texto_bloque(lz, 1190, 510, "3 PARA EL VACÍO", "RAPTOR DE VACÍO · TOBERAS GRANDES", o4, 48)
    hud(lz, t)
    return lz


def o_real(t):
    ta = ww("orbita", 1, "apaga")
    s = 3.0 + (t - ta)
    lz = _vacio()
    if t < F0("orbita", 2) - 0.2:
        rot, sub = "SECO", "T+ 00:08:09 · APAGA SUS 6 MOTORES"
    else:
        rot, sub = "26 400 KM/H", "CASI EN ÓRBITA"
    return real(t, "o1150", max(0.0, s), lz, rotulo=rot, sub=sub, tmision=486 + max(0.0, s))


def ecuador(n=240):
    a = np.linspace(0, 2 * math.pi, n)
    return np.stack([np.cos(a), np.sin(a), np.zeros(n)], 1) * (R_T * 1.003)


def anillo_orbita(m, n=300):
    return np.array([orbita_eci(x) for x in np.linspace(m, m + PERIODO, n)])


def o_globo(t):
    m = mision(t)
    t3, t4 = F0("orbita", 3), F0("orbita", 4)
    k = pr(t, t3 - 0.3, T1("orbita"))
    p = orbita_eci(m)
    u0 = math.pi - math.asin(math.sin(math.radians(25.997)) / math.sin(INC))
    lonn = math.radians(-97.16) - math.atan2(math.cos(INC) * math.sin(u0), math.cos(u0)) - W_T * (m - 600.0)
    vista = nrm(np.array([math.cos(lonn), math.sin(lonn), 0]) * 0.85 + np.array([-math.sin(lonn), math.cos(lonn), 0]) * 0.45 + np.array([0, 0, 0.3]))
    cam = Cam(vista * lerp(18000, 21000, e_inout(k)), (0, 0, 0), (0, 0, 1.0), 40, cerca=1.0, centro=(W * 0.36, H * 0.5))
    lz = L3(cam)
    globo(lz, (0, 0, 0), R_T, paso=15, op_rej=0.18, op_costa=0.7)
    oe = ap(t, ww("orbita", 4, "ecuador") - 0.3)
    Q = ecuador()
    lz.linea(Q, oe * (1 - oculto_tierra(cam.pos, Q)) * 0.9, 1.6, guion=3)
    A = anillo_orbita(m)
    lz.linea(A, (1 - oculto_tierra(cam.pos, A)) * 0.9, 1.6)
    lz.puntos(p, 5.0, 1.0)
    if 1565 <= m < 1600:
        d = nrm(orbita_eci(m + 1) - p)
        chorro(lz, p, -d, 500, 60, t, n=40, op=0.9, w=1.0)
    etiqueta3d(lz, p, "QUEMA DE INSERCIÓN", "1 MOTOR · 20 S", dx=170, dy=-80, op=vent(t, ww("orbita", 3, "veintiseis"), t4 + 0.3), px=28)
    oo = ap(t, ww("orbita", 4, "doscientos"))
    lz.texto("~275 KM", 1300, 300, 76, "Bold Condensed", oo, "lm", esp=0.05)
    lz.texto("DE ALTURA", 1304, 362, 24, "SemiBold Condensed", oo * 0.9, "lm", esp=0.16)
    oi = ap(t, ww("orbita", 4, "treinta"))
    lz.texto("30,5°", 1300, 470, 76, "Bold Condensed", oi, "lm", esp=0.05)
    lz.texto("SOBRE EL ECUADOR", 1304, 532, 24, "SemiBold Condensed", oi * 0.9, "lm", esp=0.16)
    if oi > 0:                                              # arco del ángulo en el nodo ascendente
        u_nodo = 0.0
        nodo = np.array([1.0, 0, 0])
        lonn = math.radians(-97.16) - math.atan2(math.cos(INC) * math.sin(math.pi - math.asin(math.sin(math.radians(25.997)) / math.sin(INC))),
                                                 math.cos(math.pi - math.asin(math.sin(math.radians(25.997)) / math.sin(INC))))
        lonn -= W_T * (m - 600.0)
        c, s = math.cos(lonn), math.sin(lonn)
        nodo = np.array([c, s, 0.0]) * R_ORB
        de = nrm(np.array([-s, c, 0.0]))
        do = nrm(np.array([-s * math.cos(INC), c * math.cos(INC), math.sin(INC)]))
        arc = np.array([nodo + nrm(de * math.cos(f * INC / INC * 1) + 0 * do) * 0 for f in [0]])
        P = np.array([nodo + (de * math.cos(f) + np.cross(np.cross(de, do), de) / max(1e-9, np.linalg.norm(np.cross(de, do))) * math.sin(f)) * 1400
                      for f in np.linspace(0, INC, 20)])
        vis = 1 - oculto_tierra(cam.pos, P)
        lz.linea(P, oi * vis, 1.6)
        lz.linea(np.array([nodo, nodo + de * 1800]), oi * vis[0] * 0.8, 1.2)
        lz.linea(np.array([nodo, nodo + do * 1800]), oi * vis[0] * 0.8, 1.2)
        del arc, u_nodo
    hud(lz, t)
    return lz


# ------------------------------------------------------------------ STARLINK
def _nave_orbita(t, m, dist, centro=(W * 0.42, H * 0.5), az=0.0):
    p = orbita_eci(min(max(m, 2000), 4800))
    v = nrm(orbita_eci(min(max(m, 2000), 4800) + 1) - p)
    up = nrm(p)
    side = nrm(np.cross(v, up))
    foco = p + v * 26 * M
    cam = Cam(foco + (side * math.cos(az) - v * 0.5 * math.sin(az)) * dist + up * dist * 0.25, foco, up, 40, cerca=dist * 0.003, centro=centro)
    return p, v, up, side, cam


def l_compuerta(t):
    m = mision(t)
    p, v, up, side, cam = _nave_orbita(t, m, 0.085)
    lz = L3(cam)
    globo(lz, (0, 0, 0), R_T, paso=5, op_rej=0.10, op_costa=0.45, limbo=0.7)
    S.nave(lz, p, v, M, op=1.0, ref=-up, rot=0.0, flaps=0.0)
    ab = smooth(pr(t, ww("starlink", 0, "abre") - 0.2, ww("starlink", 0, "abre") + 1.2))
    z0, z1 = 22.0, 30.0
    hinge0, hinge1 = p + (v * z0 + side * 4.5) * M, p + (v * z1 + side * 4.5) * M
    dd = nrm(side * math.cos(ab * 1.4) + up * math.sin(ab * 1.4))
    door = [hinge0, hinge1, hinge1 + dd * 3.0 * M, hinge0 + dd * 3.0 * M]
    lz.relleno(np.array(door), 0.0)
    lz.linea(np.array(door), 1.0, 1.4, cerrada=True)
    n = int(clamp((m - 2101) / (4660 - 2101)) * 26)
    t_sal = ww("starlink", 1, "salen")
    for i in range(min(n, 26)):
        edad = (m - (2101 + i * (4660 - 2101) / 26)) / 100.0
        if edad < 0:
            continue
        c = p + (v * (26 - edad * 3 - i * 0.6) + side * (6 + edad * 10 + i * 0.4) - up * (i % 3) * 1.2) * M
        q = [c + (v * sx * 3.0 + up * sy * 1.3) * M for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        lz.relleno(np.array(q), 0.0)
        lz.linea(np.array(q), 0.95, 1.1, cerrada=True)
    etiqueta3d(lz, (hinge0 + hinge1) / 2, "COMPUERTA DE CARGA", "T+ 00:35:01", dx=-230, dy=-90, op=vent(t, ww("starlink", 0, "abre"), t_sal + 0.6), px=28)
    oc = ap(t, t_sal)
    lz.texto(f"{n:02d} / 26", 1290, 330, 90, "Bold Condensed", oc, "lm", esp=0.05)
    lz.texto("STARLINK V3 DESPLEGADOS", 1294, 410, 24, "SemiBold Condensed", oc * 0.9, "lm", esp=0.14)
    lz.texto("≈ 42 MINUTOS", 1294, 460, 34, "SemiBold Condensed", ap(t, ww("starlink", 2, "cuarenta")), "lm", esp=0.1)
    hud(lz, t)
    return lz


def l_rejilla(t):
    t0 = F0("starlink", 3) - 0.3
    lz = _vacio()
    o = ap(t, t0)
    x0, y0, cw, ch = 560, 260, 76, 46
    for i in range(60):
        r, c = divmod(i, 10)
        x, y = x0 + c * (cw + 8), y0 + r * (ch + 14)
        lleno = i < 26 and t > ww("starlink", 3, "veintiseis") - 0.2 + i * 0.03
        oi = o * ap(t, t0 + i * 0.012, 0.2)
        lz.l2([(x, y), (x + cw, y), (x + cw, y + ch), (x, y + ch)], oi * (1.0 if lleno else 0.45), 1.2, cerrada=True)
        if lleno:
            lz.r2(x + 6, y + 6, x + cw - 6, y + ch - 6, 0.75 * oi)
    lz.texto("HASTA 60 POR NAVE", W / 2, 170, 64, "Bold Condensed", o, "mm", esp=0.05)
    lz.texto("EN ESTE VUELO: 26", W / 2, 720, 44, "Bold Condensed", ap(t, ww("starlink", 3, "veintiseis")), "mm", esp=0.08)
    hud_mision(lz, 0.8)
    return lz


def l_camaras(t):
    m = mision(t)
    t0 = F0("starlink", 4) - 0.3
    p, v, up, side, cam = _nave_orbita(t, m, 0.10, az=0.35 + 0.15 * pr(t, t0, F0("starlink", 5)))
    lz = L3(cam)
    globo(lz, (0, 0, 0), R_T, paso=5, op_rej=0.10, op_costa=0.45, limbo=0.7)
    S.nave(lz, p, v, M, op=1.0, ref=-up, rot=0.0, flaps=0.0)
    for j in range(3):
        ang = -0.9 + j * 0.9
        c = p + (v * (14 + j * 12) + (side * math.cos(ang) - up * math.sin(ang) * 0.8) * 16) * M
        q = [c + (v * sx * 3.0 + side * sy * 1.3) * M for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        oj = ap(t, ww("starlink", 4, "camaras") + j * 0.3)
        lz.relleno(np.array(q), 0.0)
        lz.linea(np.array(q), oj, 1.2, cerrada=True)
        blanco = p + (v * (10 + j * 12) - up * 4.5) * M
        for dd in (-1, 1):
            lz.linea(np.array([c, blanco + v * dd * 5 * M]), oj * 0.5, 1.0, guion=2)
    o = ap(t, ww("starlink", 4, "tres"))
    texto_bloque(lz, 1250, 300, "3 CON CÁMARA", "FOTOGRAFÍAN EL ESCUDO TÉRMICO", o, 64)
    hud(lz, t)
    return lz


def l_real(t):
    t0 = F0("starlink", 5) - 0.3
    lz = _vacio()
    return real(t, "o4395", 2.0 + (t - t0), lz, rotulo="VIDEO EN DIRECTO", sub="LLEGA A LA TIERRA POR LA RED STARLINK", tmision=3722 + (t - t0))


# ------------------------------------------------------------------ 14 VUELTAS
CONTROLES = [(5266, "CONTROL «HAWÁI»", "hawai", 0), (26135, "CONTROL «CHILE»", "chile", 0), (74515, "CONTROL «HAWÁI»", "otra", 0)]


def v_globo(t):
    m = mision(t)
    t0 = T0("vueltas")
    k = pr(t, t0, T1("vueltas"))
    ang = math.radians(-100 + 40 * k)
    cam = Cam(np.array([math.cos(ang), math.sin(ang), 0.42]) * 19500, (0, 0, 0), (0, 0, 1.0), 40, cerca=1.0, centro=(W * 0.38, H * 0.52))
    lz = L3(cam)
    globo(lz, (0, 0, 0), R_T, paso=15, op_rej=0.16, op_costa=0.75)
    ms = np.linspace(600, max(m, 601), int(min(2400, 60 + (m - 600) / 30)))
    G = np.array([nrm(orbita_eci(x)) * R_T * 1.004 for x in ms])
    vis = 1 - oculto_tierra(cam.pos, G)
    lz.linea(G, vis * 0.55, 1.0)
    A = anillo_orbita(m)
    lz.linea(A, (1 - oculto_tierra(cam.pos, A)) * 0.85, 1.4)
    p = orbita_eci(m)
    lz.puntos(p, 5.0, 1 - float(oculto_tierra(cam.pos, p[None])[0]))
    nv = int(clamp((m - 600) / PERIODO + 1, 1, 14))
    lz.texto(f"VUELTA {nv:02d} / 14", 90, 260, 56, "Bold Condensed", ap(t, t0), "lm", esp=0.05)
    o1 = vent(t, F0("vueltas", 1), F0("vueltas", 3))
    lz.texto("1 VUELTA ≈ 90 MIN", 94, 330, 30, "SemiBold Condensed", o1, "lm", esp=0.12)
    lz.texto("45 DE DÍA · 45 DE NOCHE", 94, 370, 24, "SemiBold Condensed", o1 * 0.85, "lm", esp=0.14)
    o2 = vent(t, F0("vueltas", 2), F0("vueltas", 3))
    lz.texto("LA TIERRA GIRA DEBAJO", 94, 430, 30, "SemiBold Condensed", o2, "lm", esp=0.12)
    for i, (mm, nom, pal, _) in enumerate(CONTROLES):
        oi = ap(t, ww("vueltas", 3, pal) - 0.1)
        y = 300 + i * 120
        x = 1340
        lz.l2([(x, y - 40), (x + 470, y - 40), (x + 470, y + 50), (x, y + 50)], oi * 0.7, 1.2, cerrada=True)
        lz.texto(nom, x + 22, y - 6, 30, "Bold Condensed", oi, "lm", esp=0.06)
        lz.texto(fmt_t(mm), x + 22, y + 28, 22, "SemiBold Condensed", oi * 0.85, "lm", esp=0.1)
        osi = ap(t, ww("vueltas", 5, "si") + i * 0.25)
        if osi > 0:
            lz.texto("SÍ", x + 440, y + 4, 44, "Bold Condensed", osi, "rm", esp=0.05)
    op = vent(t, F0("vueltas", 4), F0("vueltas", 5) + 0.2)
    lz.texto("¿INTENTAR LA TORRE, O CAER AL OCÉANO?", 1340, 680, 26, "SemiBold Condensed", op, "lm", esp=0.08)
    hud(lz, t, sh=0.0)
    return lz


# ------------------------------------------------------------------ REENTRADA
def _pose_entrada(m):
    p = orbita_eci(m)
    v = nrm(orbita_eci(m + 1) - p)
    up = nrm(p)
    side = nrm(np.cross(v, up))
    return p, v, up, side


def r_deorbit(t):
    m = mision(t)
    p, v, up, side = _pose_entrada(m)
    a = -v                                                   # cola hacia delante: frena
    foco = p
    cam = Cam(foco + (side * 0.12 + up * 0.03 + v * 0.02), foco - v * 0.012, up, 40, cerca=0.0005, centro=(W * 0.42, H * 0.5))
    lz = L3(cam)
    globo(lz, (0, 0, 0), R_T, paso=5, op_rej=0.10, op_costa=0.45, limbo=0.7)
    if motores_nave(m):
        P1.llamas_nave(lz, p - v * 25 * M, a, m, t, 50, 1.8, up)
    S.nave(lz, p - v * 25 * M, a, M, op=1.0, ref=-up, rot=0.0, flaps=0.0)
    etiqueta3d(lz, p - v * 25 * M, "SALIDA DE ÓRBITA", "T+ 21:35:57 · 10 S DE FRENADO", dx=200, dy=90, op=ap(t, ww("reentrada", 0, "enciende")), px=28)
    oc = ap(t, F0("reentrada", 1))
    if oc > 0:
        P = np.array([p - v * 25 * M + (v * s * 0.8 - up * (s / 0.9) ** 2 * 0.06) for s in np.linspace(0, 0.9 * e_out(oc), 40)])
        lz.linea(P, oc * 0.8, 1.4, guion=3)
        etiqueta3d(lz, P[-1], "EMPIEZA A CAER", None, dx=80, dy=60, op=oc, px=26)
    hud(lz, t)
    return lz


def _nave_panza(lz, base, v, up, t, flaps=0.25, aleteo=0.0):
    fl = flaps + aleteo * 0.12 * math.sin(t * 2.6)
    fd = flaps + aleteo * 0.12 * math.sin(t * 2.6 + 1.7)
    S.nave(lz, base, v, M, op=1.0, ref=-up, rot=0.0, flaps=fl, flaps_del=fd)


def r_plasma(t):
    m = mision(t)
    t3 = F0("reentrada", 3)
    up = U
    v = nrm(E + U * -0.05)
    base = SB.P + U * 0.0
    k = pr(t, F0("reentrada", 2) - 0.3, F0("reentrada", 4))
    foco = base + v * 26 * M
    cam = Cam(foco + (N * -0.12 + up * -0.01 + v * 0.015) * lerp(1.0, 0.8, k), foco, up, 40, cerca=0.0003, centro=(W * 0.40, H * 0.46))
    lz = L3(cam)
    pl = ap(t, ww("reentrada", 2, "toca"), 1.5)
    for j in range(8):                                        # capa de choque: arcos que fluyen bajo la panza
        fase = (t * 1.2 + j / 8) % 1.0
        rr = (6 + 10 * fase)
        arc = [base + v * (26 + rr * math.sin(a) * 2.0) * M - up * (5.0 + rr * (1 - math.cos(a)) * 0.15 + 1.5 * fase) * M
               + N * rr * math.cos(a) * 0.0 for a in np.linspace(-1.3, 1.3, 40)]
        lz.linea(np.array(arc), pl * (1 - fase), 2.2)
    for i in range(40):                                       # estela de plasma hacia atrás
        z = ((rnd(i, 1) - t * 1.6) % 1.0)
        q = base + v * (50 - z * 120) * M - up * (4.5 + rnd(i, 2) * 3 + z * 6) * M + N * (rnd(i, 3) - 0.5) * 9 * M
        lz.linea(np.array([q, q - v * (6 + 8 * rnd(i, 4)) * M]), pl * 0.8 * (1 - z), 1.2)
    _nave_panza(lz, base, v, up, t, 0.3)
    etiqueta3d(lz, base + v * 30 * M - up * 4.6 * M, "ENTRA DE PANZA", "EL ESCUDO TÉRMICO POR DELANTE", dx=-220, dy=110,
               op=vent(t, ww("reentrada", 3, "panza"), F0("reentrada", 4)), px=28)
    oh = ap(t, ww("reentrada", 3, "losetas") - 0.2)
    if oh > 0:                                                # recuadro con losetas hexagonales
        cx, cy, r = 1500, 330, 34
        for i in range(-3, 4):
            for j in range(-2, 3):
                x = cx + i * r * 1.5
                y = cy + j * r * 1.732 + (r * 0.866 if i % 2 else 0)
                hexa = [(x + r * 0.92 * math.cos(a), y + r * 0.92 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 7)]
                lz.l2(hexa, oh * 0.85 * ap(t, ww("reentrada", 3, "losetas") + (i + j) * 0.04), 1.2)
        lz.texto("LOSETAS HEXAGONALES", cx, cy + 190, 30, "Bold Condensed", oh, "mm", esp=0.08)
    lz.texto("ENTRADA · T+ 22:10:46", 90, 260, 34, "SemiBold Condensed", ap(t, ww("reentrada", 2, "toca")), "lm", esp=0.1)
    hud(lz, t)
    return lz


def r_real(t):
    t0 = F0("reentrada", 4) - 0.3
    lz = _vacio()
    return real(t, "reg", 228 + (t - t0), lz, rotulo="PLASMA", sub="CÁMARA A BORDO, SOBRE UN ALERÓN", tmision=80528 + (t - t0))


def r_alerones(t):
    t0 = F0("reentrada", 5) - 0.3
    k = pr(t, t0, T1("reentrada"))
    up = U
    v = E
    base = SB.P
    foco = base + v * 26 * M
    az = lerp(0.6, 1.1, k)
    cam = Cam(foco + (N * -math.cos(az) + v * math.sin(az) * 0.6 + up * 0.35) * 0.12, foco, up, 40, cerca=0.0003, centro=(W * 0.40, H * 0.5))
    lz = L3(cam)
    _nave_panza(lz, base, v, up, t, 0.35, aleteo=1.0)
    for z, txt, dy in ((10.5, "ALERONES TRASEROS", 90), (43.0, "ALERONES DELANTEROS", -90)):
        etiqueta3d(lz, base + v * z * M - N * 6 * M, txt, None, dx=-180 if dy > 0 else 180, dy=dy,
                   op=vent(t, ww("reentrada", 5, "alerones"), F0("reentrada", 6)), px=26)
    o = ap(t, ww("reentrada", 5, "paracaidista") - 0.2) * (1 - ap(t, F0("reentrada", 6)))
    texto_bloque(lz, 1240, 330, "4 ALERONES", "LA MANTIENEN ESTABLE", o, 64)
    o6 = ap(t, F0("reentrada", 6))
    texto_bloque(lz, 1240, 330, "LO MÁS PELIGROSO", "EN VUELOS ANTERIORES, EL CALOR DAÑÓ UN ALERÓN", o6, 56)
    hud(lz, t)
    return lz


# ------------------------------------------------------------------ LLEGADA
CAPTURA = P1.P_TORRE + E * (22 * M + 13.5 * M) + U * (P1.Z_BRAZOS - S.Z_PERNOS_NAVE) * M


def pose_llegada(m):
    """Base de la nave, eje y referencia del escudo: planeo de panza hacia la torre, giro y bajada vertical."""
    q = clamp((81148.0 - m) / 12.0)
    pos = CAPTURA + U * (0.62 * q ** 1.6) - E * (0.30 * q ** 2.2)
    if m < 81136:
        r = clamp((81136.0 - m) / 200.0)
        pos = CAPTURA + U * (0.62 + 11.0 * r ** 1.3) - E * (0.30 + 26.0 * r ** 1.1)
    f = e_inout(pr(m, 81137.0, 81139.0))
    a = slerp(E, U, f)
    ref = nrm(-U * (1 - f) + N * f + E * 0.001)
    return pos, a, ref


def ll_mapa(t):
    m = mision(t)
    pos, a, ref = pose_llegada(m)
    k = pr(t, T0("llegada"), F0("llegada", 2))
    foco = pos * 0.55 + SB.P * 0.45
    dist = np.linalg.norm(pos - SB.P) * 0.9 + 1.0
    cam = Cam(foco + (-N * 0.9 + U * 0.3 - E * 0.1) * dist, foco, U, 40, cerca=0.005, centro=(W * 0.42, H * 0.52))
    lz = L3(cam)
    rejilla_suelo(lz, SB.P, E, N, 40.0, 1.0, op=0.12)
    mapa_sb(lz, 1.0)
    P1.torre(lz, 0.9, 0.7)
    trayecto(lz, lambda x: pose_llegada(x)[0], 80940, m, 0.9, 1.6, n=120)
    trayecto(lz, lambda x: pose_llegada(x)[0], m, 81148, 0.4, 1.0, guion=4, n=80)
    lz.puntos(pos, 5.0, 1.0)
    _ = S.nave(lz, pos, a, M * max(1.0, dist * 1.2), op=1.0, ref=ref, rot=0.0, flaps=0.3)
    etiqueta3d(lz, pos, "PLANEO DE PANZA", "SUBSÓNICA · T+ 22:30:13", dx=170, dy=-90, op=vent(t, ww("llegada", 0, "baja"), F0("llegada", 2)), px=28)
    etiqueta3d(lz, SB.P, "STARBASE", None, dx=-180, dy=70, op=ap(t, ww("llegada", 1, "starbase")), px=26)
    hud(lz, t, sh=0.0)
    return lz


def ll_giro(t):
    m = mision(t)
    pos, a, ref = pose_llegada(m)
    bb = smooth(pr(m, 81142.0, 81146.5))
    foco = (pos + a * 26 * M) * (1 - bb) + ((pos + CAPTURA) / 2 + U * 0.02) * bb
    dist = lerp(0.17, 0.30, bb)
    cam = Cam(foco + (-N * 0.92 + E * 0.30 + U * 0.05) * dist, foco, U, 40, cerca=0.001, centro=(W * 0.40, H * 0.5))
    lz = L3(cam)
    rejilla_suelo(lz, SB.P, E, N, 0.8, 0.02, op=0.16)
    S.mesa_lanzamiento(lz, P1.P_MESA, U, M, op=0.45, ref=N)
    ab = 0.7 * (1 - smooth(pr(m, 81147.6, 81148.4)))
    P1.torre(lz, 0.9, ab)
    if motores_nave(m):
        P1.llamas_nave(lz, pos, a, m, t, 35, 1.4, ref)
    S.nave(lz, pos, a, M, op=1.0, ref=ref, rot=0.0, flaps=0.3 * (1 - smooth(pr(m, 81139, 81145))) + 0.1)
    etiqueta3d(lz, pos + a * 20 * M, "QUEMA DE ATERRIZAJE", "T+ 22:32:16", dx=200, dy=-80, op=vent(t, ww("llegada", 2, "enciende"), F0("llegada", 3)), px=28)
    etiqueta3d(lz, pos + a * 30 * M, "GIRO", "DE HORIZONTAL A VERTICAL", dx=200, dy=-80, op=vent(t, ww("llegada", 3, "gira"), F0("llegada", 4)), px=28)
    n = len(motores_nave(m))
    on = ap(t, F0("llegada", 4))
    if on > 0:
        lz.texto(f"{n}", 1420, 400, 160, "Bold Condensed", on, "mm", esp=0.0)
        lz.texto("MOTOR" if n == 1 else "MOTORES", 1420, 500, 30, "SemiBold Condensed", on, "mm", esp=0.2)
    hud(lz, t, sh=0.0)
    return lz


def ll_real(t):
    ta = ww("llegada", 6, "atrapan")
    s = 848.0 + (t - ta)
    lz = _vacio()
    rot, sub = (None, None)
    if s >= 848.0:
        rot, sub = "ATRAPADA", "T+ 22:32:28 · 14 NOV 2026"
    return real(t, "reg", s, lz, zoom=1.15, rotulo=rot, sub=sub, tmision=80300 + s)


# ------------------------------------------------------------------ montaje y sonido
PLANOS = [(T0("propulsor"), b_vuelta), (F0("propulsor", 2) - 0.3, b_falla), (F0("propulsor", 3) - 0.3, b_cae),
          (F0("propulsor", 6) - 0.3, b_mapa), (F0("propulsor", 9) - 0.3, b_rompe), (F0("propulsor", 10) - 0.3, b_torre),
          (T0("orbita"), o_nave), (F0("orbita", 1) - 0.3, o_real), (F0("orbita", 3) - 0.3, o_globo),
          (T0("starlink"), l_compuerta), (F0("starlink", 3) - 0.3, l_rejilla), (F0("starlink", 4) - 0.3, l_camaras),
          (F0("starlink", 5) - 0.3, l_real), (T0("vueltas"), v_globo),
          (T0("reentrada"), r_deorbit), (F0("reentrada", 2) - 0.3, r_plasma), (F0("reentrada", 4) - 0.3, r_real),
          (F0("reentrada", 5) - 0.3, r_alerones), (T0("llegada"), ll_mapa), (F0("llegada", 2) - 0.3, ll_giro),
          (F0("llegada", 5) - 0.3, ll_real)]


def sfx():
    v = []
    v += [(ww("propulsor", 1, "media"), "rcs", 0.7, -0.2, None), (ww("propulsor", 1, "enciende"), "encendido", 0.85, 0.0, 2.0),
          (ww("propulsor", 2, "uno"), "falla", 0.8, 0.2, None), (ww("propulsor", 3, "cae") - 0.2, "caida", 0.7, 0.0, 3.0),
          (ww("propulsor", 4, "enciende"), "encendido", 0.85, 0.0, 2.0), (ww("propulsor", 6, "decide"), "alarma", 0.7, 0.0, None),
          (ww("propulsor", 7, "aborta"), "hud", 0.5, 0.3, None), (ww("propulsor", 8, "musk"), "hud", 0.45, -0.3, None),
          (ww("propulsor", 9, "desintegra"), "explosion", 0.95, 0.0, 3.0), (F0("propulsor", 10), "whoosh", 0.5, 0.0, None)]
    v += [(T0("orbita") + 0.3, "encendido", 0.6, 0.0, 2.5), (ww("orbita", 0, "tres"), "hud", 0.45, 0.3, None),
          (ww("orbita", 1, "apaga"), "apagado", 0.8, 0.0, None), (ww("orbita", 3, "motor"), "encendido", 0.7, 0.0, 2.0),
          (ww("orbita", 4, "doscientos"), "hud", 0.45, 0.3, None), (ww("orbita", 4, "treinta"), "tic", 0.4, 0.3, None)]
    v += [(ww("starlink", 0, "abre"), "compuerta", 0.8, 0.0, None)]
    v += [(ww("starlink", 1, "salen") + i * 0.45, "satelite", 0.55, 0.3, None) for i in range(6)]
    v += [(F0("starlink", 3), "whoosh", 0.4, 0.0, None), (ww("starlink", 3, "veintiseis"), "tic", 0.4, 0.0, None),
          (ww("starlink", 4, "camaras"), "hud", 0.45, -0.3, None), (F0("starlink", 5) - 0.3, "whoosh", 0.45, 0.0, None)]
    v += [(T0("vueltas") + 0.3, "whoosh", 0.5, 0.0, None)]
    v += [(ww("vueltas", 3, p), "hud", 0.5, 0.3, None) for p in ("hawai", "chile", "otra")]
    v += [(ww("vueltas", 5, "si") + i * 0.25, "tic", 0.5, 0.3, None) for i in range(3)]
    v += [(ww("reentrada", 0, "enciende"), "encendido", 0.75, 0.0, 2.0), (ww("reentrada", 2, "toca"), "plasma", 0.85, 0.0, 6.0),
          (ww("reentrada", 4, "plasma"), "plasma", 0.7, 0.0, 6.0), (ww("reentrada", 5, "alerones"), "rcs", 0.5, 0.0, None)]
    v += [(ww("llegada", 0, "baja"), "estampido", 0.8, 0.0, None), (ww("llegada", 1, "cayendo"), "caida", 0.6, 0.0, 3.0),
          (ww("llegada", 2, "enciende"), "encendido", 0.95, 0.0, 2.5), (ww("llegada", 3, "gira"), "rcs", 0.7, 0.0, None),
          (ww("llegada", 5, "detiene"), "brazos", 0.85, 0.0, None), (ww("llegada", 6, "atrapan"), "toque", 0.95, 0.0, None)]
    return v
