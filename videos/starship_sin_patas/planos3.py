# -*- coding: utf-8 -*-
"""Planos 3: historial de capturas, la nave, los contras, lado a lado y cierre."""
import math

import numpy as np

import linea3d_cohetes as F
from comun import (H, W, L3, R_T, Cam, S, TOTAL, ap, bloque, cabecera, chorro, circulo3d, clamp, e_inout, e_out, etiqueta3d, F0, F1, foto,
                   globo, latlon_xyz, lerp, nrm, pr, rejilla_suelo, smooth, T0, T1, vacio, vent, ww, ancho_texto)
from planos1 import CAPT_X, O, TORRE, X, Y, Z, ZB_SH, cam_orb, con_foto, rp, sh_atrapado, torre
from planos2 import tarjeta

ZB_NAVE = 118.0


def nave_atrapada(lz, op=1.0, dz=0.0):
    b = TORRE + X * CAPT_X + Z * (ZB_NAVE - S.Z_PERNOS_NAVE + dz)
    S.nave(lz, b, Z, 1.0, op=op, ref=X, rot=math.pi / 2, flaps=0.15)
    return b


# ------------------------------------------------------------------ HISTORIAL
INTENTOS = [("5", "13 OCT 2024", "B12", True), ("6", "19 NOV 2024", "B13", False), ("7", "16 ENE 2025", "B14", True),
            ("8", "6 MAR 2025", "B15", True), ("15", "13 NOV 2026", "B22", False)]
MAR = [("9", "B14 · REUTILIZADO", "SE PERDIÓ ANTES DEL AGUA"), ("10", "B16", "AMERIZAJE EN EL GOLFO"), ("11", "B15 · REUTILIZADO", "AMERIZAJE EN EL GOLFO"),
       ("12", "B19 · BLOQUE 3", "CHOCÓ CONTRA EL AGUA"), ("13", "B20 · BLOQUE 3", "CHOCÓ CONTRA EL AGUA"), ("14", "B21 · BLOQUE 3", "AMERIZAJE CONTROLADO")]


def marca(lz, x, y, ok, op, s=22):
    lz.l2([(x - s, y - s), (x + s, y - s), (x + s, y + s), (x - s, y + s)], op, 1.4, cerrada=True)
    if ok:
        lz.l2([(x - s * 0.6, y), (x - s * 0.1, y + s * 0.55), (x + s * 0.65, y - s * 0.6)], op, 2.4)
    else:
        lz.l2([(x - s * 0.55, y - s * 0.55), (x + s * 0.55, y + s * 0.55)], op, 2.4)
        lz.l2([(x - s * 0.55, y + s * 0.55), (x + s * 0.55, y - s * 0.55)], op, 2.4)


def h_tabla(t):
    lz = vacio()
    final = t >= F0("historial", 9) - 0.5
    o = ap(t, T0("historial") + 0.2)
    lz.texto("INTENTOS DE ATRAPAR EL PROPULSOR", 260, 170, 52, "Bold Condensed", o, "lm", esp=0.06)
    for i, (v, fecha, b, ok) in enumerate(INTENTOS):
        y = 300 + i * 105
        oi = ap(t, T0("historial") + 0.5 + 0.25 * i) if not final else 1.0
        lz.texto(f"VUELO {v}", 260, y, 46, "Bold Condensed", oi, "lm", esp=0.06)
        lz.texto(f"{fecha}  ·  {b}", 560, y, 30, "SemiBold Condensed", oi * 0.9, "lm", esp=0.12)
        om = oi if final else ap(t, T0("historial") + 1.2 + 0.25 * i)
        marca(lz, 1010, y, ok, om)
        lz.texto("ATRAPADO" if ok else "CANCELADA", 1060, y, 30, "SemiBold Condensed", om, "lm", esp=0.12)
        lz.l2([(260, y + 48), (1300, y + 48)], oi * 0.25, 0.8)
    if final:
        of = ap(t, ww("historial", 9, "tres") - 0.2)
        lz.texto("3", 1480, 520, 300, "Bold Condensed", of, "mm")
        lz.texto("DE 5 INTENTOS", 1480, 700, 44, "Bold Condensed", ap(t, ww("historial", 9, "cinco") - 0.2), "mm", esp=0.08)
    cabecera(lz, "EL HISTORIAL")
    return lz


def h_mar(t):
    lz = vacio()
    t5, t7 = F0("historial", 5) - 0.3, ww("historial", 7, "primeros") - 0.4
    o = ap(t, t5 + 0.2)
    lz.texto("SEIS VUELOS SIN INTENTAR LA CAPTURA", 260, 170, 52, "Bold Condensed", o, "lm", esp=0.06)
    for i, (v, b, res) in enumerate(MAR):
        y = 290 + i * 92
        resalta = (i == 0 and t < t7) or (i >= 3 and t >= t7)
        oi = ap(t, t5 + 0.3 + 0.15 * i) * (1.0 if resalta else 0.4)
        lz.texto(f"VUELO {v}", 260, y, 42 if resalta else 36, "Bold Condensed", oi, "lm", esp=0.06)
        lz.texto(b, 520, y, 30, "SemiBold Condensed", oi, "lm", esp=0.1)
        lz.texto(res, 1010, y, 30, "SemiBold Condensed", oi, "lm", esp=0.1)
        lz.l2([(260, y + 40), (1500, y + 40)], oi * 0.25, 0.8)
    lz.texto("PRIMER SUPER HEAVY REUTILIZADO", 1010, 252, 24, "SemiBold Condensed", vent(t, ww("historial", 5, "reutilizado") - 0.3, t7) , "lm", esp=0.16)
    cabecera(lz, "EL HISTORIAL")
    return lz


# ------------------------------------------------------------------ LA NAVE
def n_giro(t):
    t0 = F0("nave", 4) - 0.3
    t1 = F0("nave", 5) - 0.3
    u = pr(t, t0, t1)
    lz = L3(cam_orb(X * 20 + Z * lerp(160, 120, smooth(u)), lerp(280, 220, smooth(u)), 205 + 25 * u, 6, centro=(W * 0.32, H * 0.5)))
    rejilla_suelo(lz, TORRE, X, Y, 200, 10, op=0.15)
    gir = smooth(pr(u, 0.15, 0.4))
    baja = pr(u, 0.15, 1.0)
    b_fin = TORRE + X * CAPT_X + Z * (ZB_NAVE - S.Z_PERNOS_NAVE)
    pos = b_fin + Z * (80 * (1 - smooth(baja)) + 6 * (1 - u)) - X * 60 * (1 - smooth(pr(u, 0, 0.5)))
    eje = nrm(X * (1 - gir) + Z * gir) if gir < 1 else Z
    torre(lz, lerp(0.8, 0.0, smooth(pr(u, 0.85, 1.0))), z=ZB_NAVE, op=0.9)
    S.nave(lz, pos - eje * 0 + (Z * 25 * (1 - gir)), eje, 1.0, op=1.0, ref=X if gir > 0.5 else Z, rot=math.pi / 2, flaps=0.3 * (1 - gir))
    n = 0
    if 0.15 <= u < 0.97:
        n = 3 if u < 0.5 else (2 if u < 0.8 else 1)
        for i, p in enumerate(S.salidas_nave(pos + Z * 25 * (1 - gir), eje, 1.0, X, cuales=list(range(n)))):
            chorro(lz, p, -eje, 22, 1.4, t, n=30, op=0.85, semilla=i * 3)
    bloque(lz, 1150, 300, "LLEGA DE PANZA", None, vent(t, t0 + 0.2, t0 + 2.2), 64)
    bloque(lz, 1150, 300, "GIRA A VERTICAL", None, vent(t, t0 + 2.2, t0 + 4.0), 64)
    if n:
        lz.texto(f"{n} MOTOR{'ES' if n > 1 else ''}", 1150, 420, 72, "Bold Condensed", ap(t, t0 + 1.0), "lm", esp=0.05)
    cabecera(lz, "LA NAVE")
    return lz


def n_puntos(t):
    t0 = F0("nave", 5) - 0.3
    k = pr(t, t0, F0("nave", 6))
    b = TORRE + X * CAPT_X + Z * (ZB_NAVE - S.Z_PERNOS_NAVE)
    foco = b + Z * (S.Z_PERNOS_NAVE + 2)
    lz = L3(cam_orb(foco, lerp(85, 65, e_inout(k)), lerp(215, 250, k), 12, centro=(W * 0.36, H * 0.5)))
    torre(lz, 0.0, z=ZB_NAVE, op=0.85, w=1.1)
    nave_atrapada(lz)
    cam = lz.cam
    o = ap(t, ww("nave", 5, "puntos") - 0.2)
    for lado in (1, -1):
        x, y = cam.px(b + Z * S.Z_PERNOS_NAVE + Y * lado * 4.8)
        lz.c2(x, y, 26 + 6 * math.sin(t * 4), o, w=1.6)
    bloque(lz, 1240, 320, "PUNTOS DE APOYO", "CERCA DE LA PUNTA, JUNTO A LOS ALERONES DELANTEROS", o, 64)
    cabecera(lz, "LA NAVE")
    return lz


def n_viaje(t):
    t0 = F0("nave", 6) - 0.3
    lz = vacio()
    o = ap(t, t0)
    # arco esquemático: suelo -> órbita -> suelo
    cx, cy = 960, 900
    lz.l2([(160, cy), (1760, cy)], o * 0.5, 1.2)
    P = [(cx + 700 * math.cos(a), cy - 560 * math.sin(a)) for a in np.linspace(math.pi, 0, 120)]
    lz.l2(P, o * 0.35, 1.0)
    u = e_inout(pr(t, t0 + 0.4, T1("nave") - 0.4))
    a = math.pi * (1 - u)
    x, y = cx + 700 * math.cos(a), cy - 560 * math.sin(a)
    lz.l2(P[:max(2, int(120 * u))], o, 2.0)
    lz.c2(x, y, 12, o, lleno=True)
    tarjeta(lz, x - 90, y - 110, x + 90, y - 40, o)
    lz.texto("+ PATAS", x, y - 75, 32, "Bold Condensed", o, "mm", esp=0.06)
    for txt, pal, aa in (("AL SUBIR", "subir", 0.85), ("EN ÓRBITA", "orbita", 0.5), ("DE REGRESO", "regreso", 0.15)):
        xx, yy = cx + 760 * math.cos(math.pi * aa), cy - 620 * math.sin(math.pi * aa)
        lz.texto(txt, xx, yy, 34, "SemiBold Condensed", ap(t, ww("nave", 6, pal) - 0.2), "mm", esp=0.12)
    lz.texto("SI LA NAVE TUVIERA PATAS", cx, 150, 52, "Bold Condensed", o, "mm", esp=0.06)
    lz.texto("CARGARÍA ESE PESO TODO EL VIAJE", cx, 210, 28, "SemiBold Condensed", ap(t, ww("nave", 6, "cargaria") - 0.2), "mm", esp=0.14)
    cabecera(lz, "LA NAVE")
    return lz


# ------------------------------------------------------------------ CONTRAS
def k_pregunta(t):
    t0 = T0("contras")
    cam = Cam(np.array([40.0, -270.0, 60]), np.array([40.0, 0, 62]), Z, 40, cerca=0.5, centro=(W * 0.5, H * 0.55))
    lz = L3(cam)
    rejilla_suelo(lz, np.array([40.0, 0, 0]), X, Y, 260, 12, op=0.16)
    F.etapa1(lz, np.array([-80.0, 0, 0]), Z, 1.0, aletas=1.0, patas=1.0, op=0.95, ref=Y)
    torre(lz, 0.0)
    sh_atrapado(lz)
    lz.texto("¿PALILLOS MEJOR QUE PATAS?", W / 2, 150, 72, "Bold Condensed", ap(t, t0 + 0.2), "mm", esp=0.05)
    lz.texto("NO SIEMPRE", W / 2, 240, 48, "SemiBold Condensed", ap(t, ww("contras", 0, "siempre") - 0.2), "mm", esp=0.14)
    return lz


SITIOS = [("STARBASE · PLATAFORMA 2", 25.997, -97.158, True), ("LC-39A", 28.608, -80.604, False), ("SLC-37", 28.531, -80.567, False)]


def k_globo(t):
    t0 = F0("contras", 1) - 0.3
    k = pr(t, t0, F0("contras", 2))
    c = latlon_xyz(27.0, -89.0, 1.0)
    cam = Cam(c * (R_T + lerp(9000, 4200, e_inout(k))), c * R_T * 0.98, (0, 0, 1.0), 40, cerca=1.0, centro=(W * 0.4, H * 0.52))
    lz = L3(cam)
    globo(lz, np.zeros(3), R_T, op=ap(t, t0, 0.6), paso=10)
    for i, (nom, la, lo, ok) in enumerate(SITIOS):
        P = latlon_xyz(la, lo, R_T)
        oi = ap(t, (F0("contras", 1) + 2.0) if ok else ww("contras", 1, "florida") - 0.3)
        x, y = cam.px(P)
        lz.c2(x, y, 10 if ok else 7, oi, w=1.6, lleno=ok)
        if ok:
            lz.c2(x, y, 24 + 6 * math.sin(t * 4), oi, w=1.2)
        etiqueta3d(lz, P, nom, "ATRAPA NAVES HOY" if ok else "EN CONSTRUCCIÓN", dx=-220 if ok else 120, dy=-90 + 120 * (i == 2), op=oi, px=26)
    bloque(lz, 1240, 250, "SIN TORRE", "NO HAY DÓNDE ATERRIZAR", ap(t, t0 + 0.3), 72)
    bloque(lz, 1240, 420, "1 TORRE", "EN TODO EL MUNDO PUEDE ATRAPAR UNA NAVE", ap(t, ww("contras", 1, "solo") - 0.2), 72)
    cabecera(lz, "LO MALO DE LOS PALILLOS")
    return lz


def k_riesgo(t):
    t0 = F0("contras", 2) - 0.3
    u = pr(t, t0, F0("contras", 3))
    lz = L3(cam_orb(X * 20 + Z * 80, 260, 215 + 15 * u, 6, centro=(W * 0.32, H * 0.5)))
    rejilla_suelo(lz, TORRE, X, Y, 200, 10, op=0.15)
    torre(lz, 0.8, op=0.9)
    tilt = 0.25 * math.sin(t * 2.2)
    b = X * (CAPT_X + 14) + Z * (ZB_SH - S.Z_PERNOS_SH + 30 * (1 - u))
    S.super_heavy(lz, b, nrm(Z + X * tilt * 0.4 - X * 0.12), 1.0, 1.0, op=0.9, ref=Y)
    cam = lz.cam
    x, y = cam.px(TORRE + Z * 100)
    o = ap(t, ww("contras", 2, "torre") - 0.3)
    lz.c2(x, y, 120, o * (0.6 + 0.4 * math.sin(t * 6)), w=1.6)
    bloque(lz, 1150, 320, "SI SALE MAL", "NO SOLO SE ARRIESGA EL COHETE", ap(t, t0 + 0.2), 70)
    bloque(lz, 1150, 500, "TAMBIÉN LA TORRE", "MUCHO MÁS DIFÍCIL DE REEMPLAZAR", o, 64)
    cabecera(lz, "LO MALO DE LOS PALILLOS")
    return lz


def k_luna(t):
    t0 = F0("contras", 3) - 0.3
    k = pr(t, t0, F0("contras", 5))
    lz = L3(cam_orb(Z * 22, lerp(150, 120, k), 200 + 40 * k, 8, centro=(W * 0.62, H * 0.56)))
    rejilla_suelo(lz, O, X, Y, 140, 8, op=0.2)
    for i in range(10):                                 # cráteres
        c = np.array([((i * 37) % 200) - 100.0, ((i * 59) % 160) - 60.0, 0.0])
        lz.linea(circulo3d(c, Z, 5 + (i * 7) % 12), 0.4, 1.0, cerrada=True)
    S.nave(lz, Z * 3.5, Z, 1.0, op=1.0, ref=Y, flaps=0.0)
    for j in range(4):                                  # 4 patas
        a = math.pi / 4 + j * math.pi / 2
        d = X * math.cos(a) + Y * math.sin(a)
        lz.linea(np.array([d * 4.4 + Z * 9, d * 8.5 + Z * 0.0]), 1.0, 1.6)
        lz.linea(np.array([d * 7.5, d * 9.5]), 1.0, 1.6)
    o = ap(t, t0 + 0.3)
    etiqueta3d(lz, X * 8.5 + Z * 0.5, "4 PATAS", "VERSIÓN LUNAR (HLS)", dx=-260, dy=60, op=ap(t, ww("contras", 3, "patas") - 0.3), px=28)
    bloque(lz, 1240, 220, "EN LA LUNA", "NO HAY TORRES", o, 72)
    bloque(lz, 1240, 400, "1/6", "DE LA GRAVEDAD DE LA TIERRA", ap(t, F0("contras", 4)), 110)
    cabecera(lz, "LO MALO DE LOS PALILLOS")
    return lz


# ------------------------------------------------------------------ LADO A LADO
FILAS = [("PESO EXTRA EN CADA VUELO", "EN TIERRA, EN LA TORRE"), ("TIERRA O MAR", "SOLO DONDE HAY TORRE"),
         ("LEJOS: HAY QUE TRAERLO", "YA ESTÁ EN CASA"), ("SE PIERDE EL COHETE", "SE ARRIESGA LA TORRE")]
ETQ = ["PESO", "DÓNDE ATERRIZA", "DESPUÉS", "SI FALLA"]


def cuentas(t):
    t0 = T0("cuentas")
    lz = vacio()
    o = ap(t, t0 + 0.2)
    lz.texto("PATAS", 820, 170, 70, "Bold Condensed", o, "mm", esp=0.08)
    lz.texto("PALILLOS", 1460, 170, 70, "Bold Condensed", o, "mm", esp=0.08)
    lz.l2([(1140, 140), (1140, 900)], o * 0.4, 1.0)
    for i, (a, b) in enumerate(FILAS):
        y = 330 + i * 150
        ta = F0("cuentas", i + 1)
        oa = max(0.3 * o, ap(t, ta - 0.1))
        ob = ap(t, ww("cuentas", i + 1, "palillos") - 0.1)
        lz.texto(ETQ[i], 180, y, 26, "SemiBold Condensed", oa * 0.8, "lm", esp=0.18)
        lz.texto(a, 820, y, 36, "Bold Condensed", oa, "mm", esp=0.05)
        lz.texto(b, 1460, y, 36, "Bold Condensed", ob, "mm", esp=0.05)
        lz.l2([(180, y + 52), (1760, y + 52)], oa * 0.25, 0.8)
    cabecera(lz, "LADO A LADO")
    return lz


# ------------------------------------------------------------------ CIERRE
def c_cierre(t):
    t0 = T0("cierre")
    k = pr(t, t0, TOTAL)
    cam = Cam(np.array([10 + 30 * k, -300.0, 70]), np.array([10.0 + 30 * k, 0, 65]), Z, 40, cerca=0.5, centro=(W * 0.3, H * 0.55))
    lz = L3(cam)
    rejilla_suelo(lz, np.array([10.0, 0, 0]), X, Y, 260, 12, op=0.16)
    F.etapa1(lz, np.array([-80.0, 0, 0]), Z, 1.0, aletas=1.0, patas=1.0, op=0.9, ref=Y)
    torre(lz, 0.0)
    sh_atrapado(lz)
    o0 = vent(t, t0 + 0.2, F0("cierre", 2))
    lz.texto("PATAS O PALILLOS", 1060, 330, 70, "Bold Condensed", o0, "lm", esp=0.05)
    lz.texto("UN COHETE QUE VUELVA Y VUELE OTRA VEZ", 1064, 400, 26, "SemiBold Condensed", ap(t, ww("cierre", 0, "vuelva") - 0.2) * o0, "lm", esp=0.14)
    lz.texto("FALCON 9: ATERRIZA CASI DONDE SEA", 1064, 480, 28, "SemiBold Condensed", ap(t, F0("cierre", 1)) * o0, "lm", esp=0.1)
    lz.texto("STARSHIP: LO ATRAPAN DONDE DESPEGA", 1064, 530, 28, "SemiBold Condensed", ap(t, ww("cierre", 1, "starship") - 0.1) * o0, "lm", esp=0.1)
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
    cabecera(lz, "STARSHIP SIN PATAS")
    return lz


def _planos():
    p = [(T0("historial"), h_tabla)]
    a = F0("historial", 1) - 0.3
    p.append((a, rp("f5", 141.5, a, rot="VUELO 5 · 13 OCT 2024", sub="ATRAPADO AL PRIMER INTENTO", tfin=152.0)))
    a = F0("historial", 2) - 0.3
    p.append((a, rp("f6", 36.0, a, rot="VUELO 6 · 19 NOV 2024", sub="CAPTURA CANCELADA · AL GOLFO DE MÉXICO", vel=0.9, tfin=45.0)))
    a = F0("historial", 3) - 0.3
    p.append((a, rp("f7", 130.0, a, rot="VUELO 7 · 16 ENE 2025", sub="ATRAPADO", tfin=141.0)))
    a = F0("historial", 4) - 0.3
    p.append((a, rp("f8", 452.0, a, rot="VUELO 8 · 6 MAR 2025", sub="ATRAPADO · AUNQUE 2 MOTORES NO REENCENDIERON", vel=1.5, tfin=482.0)))
    p.append((F0("historial", 5) - 0.3, h_mar))
    a = F0("historial", 6) - 0.3
    p.append((a, rp("f11", 399.0, a, rot="PRUEBAS EN EL MAR", sub="VUELO 11 · 13 OCT 2025 · PROPULSOR REUTILIZADO", tfin=412.0)))
    a = F0("historial", 7) - 0.3
    p.append((a, rp("lanz", 74.0, a, rot="TERCERA VERSIÓN", sub="MÁS ALTA Y CON MOTORES NUEVOS", vel=0.8)))
    p.append((ww("historial", 7, "primeros") - 0.4, h_mar))
    a = F0("historial", 8) - 0.3
    p.append((a, rp("cnn", 156.0, a, rot="VUELO 15 · 13 NOV 2026 · B22", sub="DETECTÓ UN PROBLEMA Y ABORTÓ SOLO", tfin=169.0)))
    a = ww("historial", 8, "perdio") - 0.5
    p.append((a, rp("cnn", 185.2, a, rot="SE PERDIÓ SOBRE EL GOLFO", sub="VUELO 15 · PROPULSOR B22", vel=0.7, tfin=188.6)))
    p.append((F0("historial", 9) - 0.5, h_tabla))
    # la nave
    a = T0("nave")
    p.append((a, rp("reg", 835.5, a, rot="NAVE 42 · VUELO 15", sub="VUELVE DE ÓRBITA TRAS 14 VUELTAS", tfin=847.0)))
    a = F0("nave", 2) - 0.4
    p.append((a, rp("reg", 847.6, a, rot="LA PRIMERA NAVE ATRAPADA", sub="14 NOV 2026 · STARBASE, TEXAS", vel=0.9, tfin=853.5)))
    a = F0("nave", 3) - 0.3
    p.append((a, rp("cnn", 222.0, a, rot="T+ 22:32:28", sub="CON UN SOLO MOTOR, ENTRE LOS BRAZOS", tfin=240.0)))
    p.append((F0("nave", 4) - 0.3, n_giro))
    p.append((F0("nave", 5) - 0.3, n_puntos))
    p.append((F0("nave", 6) - 0.3, n_viaje))
    # contras
    p.append((T0("contras"), k_pregunta))
    p.append((F0("contras", 1) - 0.3, k_globo))
    p.append((F0("contras", 2) - 0.3, k_riesgo))
    a = F0("contras", 3) - 0.3
    p.append((a, con_foto(k_luna, dict(nombre="hls", cx=430, cy=520, ancho=380, asp=0.62, foco=(0.5, 0.55), t0=a + 0.6, t1=F0("contras", 5) - 0.3,
                                       rotulo="STARSHIP LUNAR (HLS)", sub="ILUSTRACIÓN: SPACEX / NASA", estilo=0))))
    a = F0("contras", 5) - 0.3
    p.append((a, rp("crs8", 10.0, a, rot="FALCON 9 · SEGUIRÁ CON PATAS", sub="ATERRIZA EN BARCAZAS EN MEDIO DEL MAR", tfin=38.0)))
    p.append((T0("cuentas"), cuentas))
    p.append((T0("cierre"), c_cierre))
    return p


PLANOS = _planos()


def sfx():
    v = [(T0("historial") + 0.3, "hud", 0.45, 0.0, None)]
    v += [(T0("historial") + 1.2 + 0.25 * i, "tic", 0.4, 0.3, None) for i in range(5)]
    v += [(F0("historial", 5) - 0.1, "whoosh", 0.35, 0.0, None), (ww("historial", 8, "perdio") - 0.4, "explosion", 0.5, 0.0, None),
          (ww("historial", 9, "tres") - 0.2, "pulso", 0.6, 0.0, None)]
    v += [(F0("nave", 4) - 0.2, "whoosh", 0.4, 0.0, None), (F0("nave", 4) + 1.0, "encendido", 0.5, 0.0, None),
          (F1("nave", 4) - 0.6, "toque", 0.5, 0.0, None), (ww("nave", 5, "puntos"), "hud", 0.45, 0.3, None), (F0("nave", 6), "tic", 0.4, 0.0, None)]
    v += [(T0("contras") + 0.2, "whoosh", 0.4, 0.0, None), (F0("contras", 1) + 2.0, "hud", 0.45, 0.3, None),
          (ww("contras", 2, "torre") - 0.3, "alarma", 0.4, 0.0, None), (F0("contras", 3) - 0.2, "whoosh", 0.4, 0.0, None),
          (F0("contras", 4), "tic", 0.45, 0.3, None)]
    v += [(F0("cuentas", i + 1) - 0.1, "tic", 0.45, -0.3, None) for i in range(4)]
    v += [(ww("cuentas", i + 1, "palillos") - 0.1, "tic", 0.45, 0.3, None) for i in range(4)]
    v += [(F0("cierre", 2), "whoosh", 0.45, 0.0, None), (ww("cierre", 3, "suscribete"), "campana", 0.6, 0.0, None)]
    return v
