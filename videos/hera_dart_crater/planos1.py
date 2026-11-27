# -*- coding: utf-8 -*-
"""Planos 1: gancho, el sistema doble, la nave DART. Mundo LOCAL en metros (Didymos en el origen)."""
import math

import numpy as np

from comun import (H, W, L3, Cam, E, ap, bloque, cabecera, clamp, contador, e_inout, e_out, etiqueta3d, F0, F1, foto, lerp, pr,
                   real, smooth, T0, T1, vacio, vent, ww, a_img, _Img, circulo3d, nrm)
from p3d import (O, X, Y, Z, SOL, R_DID, R_DIM, R_ORB, P_ANTES, cam_orb, pos_dim, didymos, dimorphos, orbita, flecha3d, reloj)
from _seg import SEG


def rp(clip, s0, ta, rot=None, sub=None, top=None, vel=1.0, zoom=1.0, cy=0.5, cx=0.5, extra=None, tfin=None, sat=0.8, credito=True):
    """Plano de video real: segundo s0 del clip al empezar el plano (ta)."""
    def f(t):
        lz = vacio()
        seg = s0 + (t - ta) * vel
        if tfin is not None:
            seg = min(seg, tfin)
        if extra:
            extra(lz, t)
        return real(t, clip, seg, lz, zoom=zoom, cy=cy, cx=cx, rotulo=rot, sub=sub, tmision=top, sat=sat, credito=credito)
    f.ta = ta
    return f


def con_foto(plano, *fotos):
    def f(t):
        img = a_img(plano(t), t)
        for k in fotos:
            img = foto(img, t, **k)
        return _Img(img)
    return f


def ang_dim(t):
    """Ángulo de Dimorphos en su órbita (en pantalla da una vuelta cada ~40 s)."""
    return 200.0 + t * 9.0


# ------------------------------------------------------------------ GANCHO
def g_duda(t):
    """Dimorphos de alambre con signos de pregunta: nadie había visto cómo quedó."""
    t0 = F0("gancho", 2) - 0.3
    k = pr(t, t0, F0("gancho", 4))
    lz = L3(cam_orb(O, lerp(520, 430, k), 25 + 20 * k, 12))
    E.estrellas(lz)
    dimorphos(lz, O, yaw=30 + 12 * k)
    o = ap(t, t0 + 0.4)
    for i, (x, y, px) in enumerate(((1350, 330, 150), (560, 760, 110), (1420, 760, 80))):
        lz.texto("?", x, y + 8 * math.sin(t * 1.3 + i), px, "Light Condensed", o * (0.9 - 0.2 * i), "mm")
    lz.texto("¿CÓMO QUEDÓ?", W / 2, 960, 44, "Bold Condensed", vent(t, t0 + 0.3, F0("gancho", 3) - 0.45), "mm", esp=0.08)
    o2 = ap(t, F0("gancho", 3) - 0.1)
    lz.texto("HASTA ESTA SEMANA", W / 2, 960, 52, "Bold Condensed", o2, "mm", esp=0.08)
    cabecera(lz, "DIMORPHOS · 2022")
    return lz


def g_titulo(t):
    """El sistema doble con Hera llegando: título del video."""
    t0 = F0("gancho", 6) - 0.3
    k = pr(t, t0, T1("gancho") + 0.5)
    foco = np.array([R_ORB * 0.45, 0, 0])
    lz = L3(cam_orb(foco, lerp(4200, 3600, k), lerp(-20, -5, k), 18, centro=(W * 0.36, H * 0.52)))
    E.estrellas(lz)
    orbita(lz, 0.35)
    didymos(lz, t)
    P = pos_dim(ang_dim(t))
    dimorphos(lz, P, despues=True, yaw=t * 20)
    hp = P + np.array([-350, -900, 260]) * (1.3 - 0.3 * k)
    E.hera(lz, hp, E.rot_ypr(70, 0, 0), esc=22)
    o = ap(t, t0 + 0.2)
    lz.texto("EL CRÁTER", 1150, 420, 120, "Bold Condensed", o, "lm", esp=0.03)
    lz.texto("DE DART", 1150, 530, 120, "Bold Condensed", ap(t, t0 + 0.5), "lm", esp=0.03)
    lz.texto("EXPLICADO EN 3D", 1156, 612, 30, "SemiBold Condensed", ap(t, t0 + 0.9) * 0.9, "lm", esp=0.22)
    cabecera(lz, "HERA · DIDYMOS · DIMORPHOS")
    return lz


# ------------------------------------------------------------------ SISTEMA
def s_par(t):
    """Los dos asteroides: tamaño de cada uno y la órbita (con su reloj)."""
    t0 = T0("sistema")
    k = smooth(pr(t, t0, F0("sistema", 6)))
    foco = lerp(np.zeros(3), np.array([R_ORB * 0.35, 0, 0]), smooth(pr(t, F0("sistema", 3) - 0.5, F0("sistema", 3) + 1.5)))
    lz = L3(cam_orb(foco, lerp(1900, 3700, smooth(pr(t, F0("sistema", 3) - 0.5, F0("sistema", 3) + 1.5))), -30 + 25 * k, 20,
                    centro=(W * 0.42, H * 0.5)))
    E.estrellas(lz)
    oo = ap(t, F0("sistema", 3) + 0.4)
    if oo > 0:
        orbita(lz, 0.45 * oo)
    didymos(lz, t)
    P = pos_dim(ang_dim(t))
    o_dim = ap(t, ww("sistema", 3, "luna") - 0.3)
    if o_dim > 0:
        dimorphos(lz, P, op=o_dim, yaw=t * 9)
    etiqueta3d(lz, np.array([0, 0, R_DID * 0.8]), "DIDYMOS", "730 M · FORMA DE TROMPO", dx=-260, dy=-150,
               op=ap(t, ww("sistema", 1, "didymos") - 0.1), px=34)
    etiqueta3d(lz, P + np.array([0, 0, R_DIM * 0.6]), "DIMORPHOS", "UNOS 150 M · SU LUNA", dx=200, dy=-140,
               op=o_dim * ap(t, ww("sistema", 3, "dimorphos") - 0.1), px=34)
    o_rel = ap(t, F0("sistema", 5) - 0.2)
    if o_rel > 0:
        reloj(lz, 1500, 820, P_ANTES, o_rel, 84, "UNA VUELTA ALREDEDOR DE DIDYMOS")
    o_seg = vent(t, F0("sistema", 6) - 0.1, T1("sistema") + 0.5)
    o_gir = vent(t, F0("sistema", 2) - 0.1, F0("sistema", 3) - 0.3)
    lz.texto("GIRA CADA 2 H 15 MIN", 1500, 220, 40, "Bold Condensed", o_gir, "mm", esp=0.08)
    o_nom = vent(t, F0("sistema", 4) - 0.1, F0("sistema", 5) - 0.3)
    lz.texto("DIMORPHOS = «EL DE DOS FORMAS»", 1500, 220, 40, "Bold Condensed", o_nom, "mm", esp=0.06)
    lz.texto("SIN PELIGRO PARA LA TIERRA", 1500, 220, 34, "Bold Condensed", o_seg, "mm", esp=0.1)
    cabecera(lz, "EL BLANCO · UN ASTEROIDE DOBLE")
    return lz


def s_brillo(t):
    """Curva de luz: desde la Tierra, cuando una pasa por delante de la otra el brillo baja; tras el empujón, llega antes."""
    t0 = F0("sistema", 7) - 0.3
    lz = L3(cam_orb(np.array([0, 0, 0]), 5200, 0, 4, centro=(W * 0.5, H * 0.3)))
    E.estrellas(lz, op=0.35)
    orbita(lz, 0.3)
    # Dimorphos pasa por delante de Didymos (vista casi de canto)
    fase = (t - t0) * 0.10
    ang = -90 + math.degrees(math.sin(fase * 2 * math.pi) * 0.0) + ((t - t0) * 24) % 360 - 180
    didymos(lz, t, rocas=60)
    P = pos_dim(ang)
    dimorphos(lz, P, rocas=60)
    lz.texto("DESDE LA TIERRA", 960, 80, 22, "SemiBold Condensed", ap(t, t0) * 0.85, "mm", esp=0.22)
    # gráfica de brillo
    x0, x1, yb = 260, 1600, 940
    o = ap(t, t0 + 0.3)
    lz.l2([(x0, yb - 260), (x0, yb), (x1, yb)], o * 0.7, 1.2)
    lz.texto("BRILLO", x0 - 16, yb - 250, 20, "SemiBold Condensed", o * 0.8, "rm", esp=0.16)
    lz.texto("TIEMPO", x1, yb + 28, 20, "SemiBold Condensed", o * 0.8, "rm", esp=0.16)
    xs = np.linspace(x0, x1, 400)

    def curva(per, des=0.0):
        u = (xs - x0) / (x1 - x0) * 3.2 + des
        ph = (u % 1.0)
        dip = np.exp(-((ph - 0.5) / 0.035) ** 2) * 70 + np.exp(-((ph - 0.0) / 0.035) ** 2) * 40 + np.exp(-((ph - 1.0) / 0.035) ** 2) * 40
        return yb - 200 + dip * per

    kd = e_out(pr(t, t0 + 0.4, t0 + 3.4))
    n = int(len(xs) * kd)
    if n > 2:
        lz.l2(np.stack([xs[:n], curva(1.0)[:n]], -1), o, 1.8)
    o2 = ap(t, ww("sistema", 8, "empujas") - 0.1)
    if o2 > 0:
        u = (xs - x0) / (x1 - x0) * 3.2 * 1.12
        ph = u % 1.0
        dip = np.exp(-((ph - 0.5) / 0.035) ** 2) * 70 + np.exp(-(ph / 0.035) ** 2) * 40 + np.exp(-((ph - 1.0) / 0.035) ** 2) * 40
        ys = yb - 200 + dip + 110
        k2 = e_out(pr(t, ww("sistema", 8, "empujas"), ww("sistema", 8, "empujas") + 2.5))
        m = int(len(xs) * k2)
        for jj in range(0, max(0, m - 3), 6):
            lz.l2([(xs[jj], ys[jj]), (xs[jj + 3], ys[jj + 3])], o2, 1.6)
        lz.texto("ANTES", x1 + 20, yb - 200, 20, "SemiBold Condensed", o2 * 0.8, "lm", esp=0.14)
        lz.texto("DESPUÉS", x1 + 20, yb - 90, 20, "SemiBold Condensed", o2, "lm", esp=0.14)
        lz.texto("TRAS EL EMPUJÓN: LAS BAJADAS LLEGAN ANTES", x1, yb - 300, 26, "SemiBold Condensed", o2, "rm", esp=0.12)
    lz.texto("CADA BAJADA = UNA PASA POR DELANTE DE LA OTRA", x0, yb + 60, 22, "SemiBold Condensed", ap(t, t0 + 2.0) * 0.85, "lm", esp=0.12)
    cabecera(lz, "CÓMO SE MIDE DESDE AQUÍ")
    return lz


def s_prueba(t):
    t0 = F0("sistema", 9) - 0.3
    k = pr(t, t0, T1("sistema") + 1.0)
    lz = L3(cam_orb(np.array([R_ORB, 0, 0]), lerp(900, 700, k), 60 - 30 * k, 10, centro=(W * 0.62, H * 0.5)))
    E.estrellas(lz)
    P = np.array([R_ORB, 0, 0])
    dimorphos(lz, P, yaw=20 + 10 * k)
    o = ap(t, t0 + 0.2)
    lz.texto("¿PODEMOS MOVER", 120, 440, 84, "Bold Condensed", o, "lm", esp=0.04)
    lz.texto("UN ASTEROIDE?", 120, 530, 84, "Bold Condensed", ap(t, t0 + 0.5), "lm", esp=0.04)
    cabecera(lz, "LA PRUEBA")
    return lz


# ------------------------------------------------------------------ DART
def d_modelo(t):
    """La nave DART: cuerpo y los dos paneles ROSA que se desenrollan."""
    t0 = F0("dart", 2) - 0.3
    k = pr(t, t0, F0("dart", 4))
    rosa = e_inout(pr(t, ww("dart", 2, "desenrollaban") - 0.8, ww("dart", 2, "desenrollaban") + 1.8))
    rosa = max(rosa, 0.04)
    lz = L3(cam_orb(O, lerp(16, 24, k) + 10 * rosa, lerp(30, 70, k), 22, centro=(W * 0.46, H * 0.52), cerca=0.1))
    E.estrellas(lz)
    E.dart(lz, O, E.rot_ypr(0, 0, 0), rosa=rosa)
    etiqueta3d(lz, np.array([0, 0, 0.7]), "CUERPO", "UNOS 570 KG", dx=-150, dy=-200,
               op=ap(t, ww("dart", 2, "caja") - 0.1), px=30)
    etiqueta3d(lz, np.array([0, 1.0 + 8.5 * rosa * 0.7, 0]), "PANELES SOLARES", "SE DESENROLLAN", dx=150, dy=-150,
               op=ap(t, ww("dart", 2, "paneles") - 0.1) * smooth(pr(rosa, 0.3, 0.6)), px=30)
    o = ap(t, F0("dart", 3) - 0.1)
    lz.texto("SIN EXPLOSIVOS", 1500, 860, 48, "Bold Condensed", o, "mm", esp=0.06)
    lz.texto("SU ARMA: LA VELOCIDAD", 1500, 912, 24, "SemiBold Condensed", o * 0.9, "mm", esp=0.18)
    cabecera(lz, "DART · DOUBLE ASTEROID REDIRECTION TEST")
    return lz


def d_draco(t):
    """La cámara DRACO al frente y el piloto automático."""
    t0 = F0("dart", 4) - 0.3
    k = pr(t, t0, F0("dart", 6))
    lz = L3(cam_orb(np.array([1.0, 0, 0.2]), lerp(9, 6.5, k), lerp(130, 110, k), 14, centro=(W * 0.4, H * 0.5), cerca=0.1))
    E.estrellas(lz)
    E.dart(lz, O, E.rot_ypr(0, 0, 0), rosa=1.0)
    # cono de visión de la cámara
    o = ap(t, ww("dart", 4, "draco") - 0.2)
    tip = np.array([1.1, 0, 0.25])
    for a in range(8):
        u = 2 * math.pi * a / 8
        lz.linea(np.array([tip, tip + np.array([12, 2.0 * math.cos(u), 2.0 * math.sin(u)])]), o * 0.35, 1.0)
    lz.linea(circulo3d(tip + np.array([12, 0, 0]), X, 2.0, 48), o * 0.5, 1.0, cerrada=True)
    etiqueta3d(lz, tip, "DRACO", "LA CÁMARA", dx=160, dy=-170, op=o, px=34)
    o2 = ap(t, ww("dart", 5, "programa") - 0.1)
    lz.texto("PILOTO AUTOMÁTICO", 1460, 800, 50, "Bold Condensed", o2, "mm", esp=0.05)
    lz.texto("SE GUÍA SOLA EN LAS ÚLTIMAS 4 HORAS", 1460, 852, 22, "SemiBold Condensed", o2 * 0.9, "mm", esp=0.16)
    cabecera(lz, "DART · DRACO")
    return lz


def d_licia(t):
    """LICIACube se separa y se queda atrás."""
    t0 = ww("dart", 6, "quince") - 0.3
    ks = e_out(pr(t, ww("dart", 6, "soltó") - 0.2, ww("dart", 6, "soltó") + 5.0))
    lz = L3(cam_orb(np.array([-3 - 4 * ks, -1, 0.5]), 18, 120, 22, centro=(W * 0.5, H * 0.5), cerca=0.1))
    E.estrellas(lz)
    E.dart(lz, O, E.rot_ypr(0, 0, 0), rosa=1.0)
    ks = e_out(pr(t, ww("dart", 6, "soltó") - 0.2, ww("dart", 6, "soltó") + 5.0))
    P = np.array([-0.8 - 7 * ks, -1.0 - 1.5 * ks, 0.3 + 1.0 * ks])
    E.caja(lz, P, E.rot_ypr(t * 20, 10, 0), (0.37, 0.23, 0.11))
    etiqueta3d(lz, P, "LICIACUBE", "AGENCIA ESPACIAL ITALIANA", dx=-150, dy=-160, op=ap(t, ww("dart", 6, "liciacube") - 0.1), px=32)
    o = ap(t, F0("dart", 7) - 0.1)
    lz.texto("SU TRABAJO: FOTOGRAFIAR EL CHOQUE", W / 2, 960, 36, "Bold Condensed", o, "mm", esp=0.08)
    o0 = ap(t, t0)
    lz.texto("15 DÍAS ANTES", 1560, 240, 54, "Bold Condensed", o0, "mm", esp=0.05)
    cabecera(lz, "DART · LICIACUBE")
    return lz


def S(k, d=0.0):
    return SEG.get(k, d)


FN = "FOTO: NASA / JOHNS HOPKINS APL"
PLANOS = [
    # ---------------- GANCHO
    (0.0, rp("draco", S("draco_gancho", 26.0), 0.0, "LO ÚLTIMO QUE VIO DART", "CÁMARA DRACO · 26-SEP-2022", tfin=S("draco_ultimo", 38.5))),
    (F0("gancho", 1) - 0.3, rp("hubble_x3", 0.0, F0("gancho", 1) - 0.3, "EL CHOQUE, VISTO POR HUBBLE", "26-SEP-2022", vel=0.5,
                              tfin=S("x3_fin", 2.95))),
    (F0("gancho", 2) - 0.3, g_duda),
    (F0("gancho", 4) - 0.3, rp("hera_llegada", S("llegada_gancho", 30.0), F0("gancho", 4) - 0.3, "HERA · AGENCIA ESPACIAL EUROPEA",
                              "LLEGA A LOS ASTEROIDES · NOV-2026", vel=2.0)),
    (F0("gancho", 5) - 0.3, rp("hera_sur", S("sur", 0.0), F0("gancho", 5) - 0.3, "DIMORPHOS · NOVIEMBRE 2026",
                              "EL CRÁTER Y LOS TUMBOS · VIDEO DE HERA")),
    (F0("gancho", 6) - 0.3, g_titulo),
    # ---------------- SISTEMA
    (T0("sistema"), con_foto(s_par,
                             dict(nombre="hera_afc", cx=1450, cy=560, ancho=520, t0=ww("sistema", 1, "didymos") + 0.4,
                                  t1=F0("sistema", 2) - 0.2, rotulo="DIDYMOS VISTO POR HERA", sub="FOTO: ESA · CC BY-SA 3.0 IGO",
                                  estilo=0, asp=1.0),
                             dict(nombre="dart_ultima1", cx=1450, cy=560, ancho=520, t0=ww("sistema", 3, "dimorphos") + 0.4,
                                  t1=F0("sistema", 4) + 1.5, rotulo="DIMORPHOS · ÚLTIMA FOTO DE DART", sub=FN, estilo=1, asp=1.0))),
    (F0("sistema", 2) - 0.3, rp("hera_llegada", S("didymos_cerca", 60.0), F0("sistema", 2) - 0.3, "DIDYMOS",
                                "GIRA CADA 2 H 15 MIN · FOTOS DE HERA", vel=0.5)),
    (F0("sistema", 3) - 0.3, con_foto(s_par,
                                      dict(nombre="dart_ultima1", cx=1450, cy=560, ancho=520, t0=ww("sistema", 3, "dimorphos") + 0.4,
                                           t1=F0("sistema", 4) + 1.5, rotulo="DIMORPHOS · ÚLTIMA FOTO DE DART", sub=FN, estilo=1,
                                           asp=1.0))),
    (F0("sistema", 7) - 0.3, s_brillo),
    (F0("sistema", 9) - 0.3, s_prueba),
    # ---------------- DART
    (T0("dart"), con_foto(d_modelo, dict(nombre="dart_vandenberg", cx=1420, cy=520, ancho=700, t0=T0("dart") + 0.3,
                                         t1=F0("dart", 1) - 0.4, rotulo="LA NAVE DART REAL", sub="FOTO: NASA · VANDENBERG 2021",
                                         estilo=2, asp=1.52))),
    (F0("dart", 1) - 0.3, rp("dart_lanz", S("lanz", 15.0), F0("dart", 1) - 0.3, "FALCON 9 · VANDENBERG, CALIFORNIA", "24-NOV-2021")),
    (F0("dart", 2) - 0.3, d_modelo),
    (F0("dart", 4) - 0.3, d_draco),
    (F0("dart", 6) - 0.3, rp("dart_despl", S("despl", 10.0), F0("dart", 6) - 0.3, "DART SE SEPARA DEL COHETE", "EMPIEZAN 10 MESES DE VIAJE")),
    (ww("dart", 6, "quince") - 0.3, d_licia),
]


def sfx():
    return [(0.3, "foto", 0.5, 0.0, None), (1.6, "foto", 0.5, 0.0, None), (F0("gancho", 1) - 0.4, "senal", 0.7, 0.0, None),
            (F0("gancho", 3), "pulso", 0.9, 0.0, None), (F0("gancho", 4) - 0.3, "whoosh", 0.6, 0.0, None),
            (F0("gancho", 5), "rocas", 0.5, 0.0, None), (F0("gancho", 6) - 0.2, "pulso", 0.9, 0.0, None),
            (T0("sistema"), "whoosh", 0.6, 0.0, None), (ww("sistema", 1, "didymos"), "hud", 0.6, -0.2, None),
            (ww("sistema", 3, "dimorphos"), "hud", 0.6, 0.2, None), (F0("sistema", 5), "tic", 0.5, 0.0, None),
            (F0("sistema", 7) - 0.3, "whoosh", 0.5, 0.0, None), (ww("sistema", 8, "empujas"), "hud", 0.6, 0.0, None),
            (F0("sistema", 9) - 0.2, "pulso", 0.8, 0.0, None), (F0("dart", 1) - 0.3, "rugido", 0.8, 0.0, None),
            (ww("dart", 2, "desenrollaban") - 0.6, "despliegue", 0.7, 0.0, None), (F0("dart", 3), "sello", 0.6, 0.0, None),
            (ww("dart", 4, "draco"), "foto", 0.6, 0.0, None), (ww("dart", 6, "soltó"), "despliegue", 0.5, 0.0, None)]
