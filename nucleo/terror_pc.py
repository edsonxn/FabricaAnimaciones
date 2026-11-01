# -*- coding: utf-8 -*-
"""Extensión PC del kit «terror CRT» (Sonic.exe, 13-oct-2026): monitor CRT beige de PC + torre con lector de CD + escritorio + cama,
pantallas de PC dibujadas (escritorio, título de Sonic 1 que se corrompe, wiki, captura retocada, .exe, documento, web/video/blog),
CD-R, nota arrugada, silueta de Sonic (de pie o peluche). Se apoya en `terror.py` (CRT, iluminar, cuarto) y `pix.py`.
Todo lo que lleva marca real (Sega, Windows, GameJolt, YouTube) va SOLO como texto, nunca con logos."""
import math

import cv2
import numpy as np

import terror_crt as T
from terror_pix import Clip, P, ancho_texto, clamp, e_out, lerp, mix, pop, pr, rnd, smooth
from terror_crt import CRT_VERDE, HUESO, SANGRE, SC, SH, SIL, SW, SX0, SX1, SY0, SY1

BEIGE = (0.62, 0.58, 0.46)
MOON = (0.42, 0.52, 0.80)
DESK_Y = 790.0


# ================================================================== encendido / apagado del tubo
def encendido(img, u):
    """El monitor se enciende: una línea blanca que se abre en el centro hasta llenar el tubo."""
    h, w = img.shape[:2]
    ancho, alto = smooth(pr(u, 0.0, 0.3)), smooth(pr(u, 0.28, 1.0))
    y = np.arange(h, dtype=np.float32)[:, None]
    x = np.arange(w, dtype=np.float32)[None, :]
    m = ((np.abs(y - h / 2) < 3 + alto * h / 2) & (np.abs(x - w / 2) < ancho * w / 2)).astype(np.float32)[..., None]
    lin = np.exp(-((np.abs(y - h / 2) / (5 + 40 * alto)) ** 2)) * (ancho > 0) * (1 - alto)
    return img * m + (m * lin[..., None] * 1.6)


def apagado(img, u):
    """El monitor se apaga: se aplasta a una línea y queda un punto que se va."""
    h, w = img.shape[:2]
    alto, ancho = 1 - smooth(pr(u, 0.0, 0.45)), 1 - smooth(pr(u, 0.4, 0.8))
    y = np.arange(h, dtype=np.float32)[:, None]
    x = np.arange(w, dtype=np.float32)[None, :]
    m = ((np.abs(y - h / 2) < 3 + alto * h / 2) & (np.abs(x - w / 2) < 6 + ancho * w / 2)).astype(np.float32)[..., None]
    pt = np.exp(-(((x - w / 2) ** 2 + (y - h / 2) ** 2) / (2 * 22 ** 2)))[..., None] * (1 - smooth(pr(u, 0.75, 1.0))) * 1.2
    return img * m * (1.0 + 1.5 * (1 - alto)) + pt


# ================================================================== cuarto de 2011 (albedo: lo ilumina T.iluminar)
def cuarto_pc(p, t):
    """Cuarto de un chico de 2011: la pared de siempre + cama bajo la ventana + escritorio con torre y teclado."""
    T.cuarto_albedo(p, t)
    # cama (bajo la ventana, a la izquierda)
    p.rect(30, 560, 62, 800, (0.20, 0.12, 0.09))                                      # cabecera
    p.rrect(30, 560, 70, 640, 14, (0.24, 0.15, 0.11))
    p.rrect(46, 690, 540, 806, 10, (0.30, 0.20, 0.25), grad=((0.36, 0.25, 0.30), (0.20, 0.13, 0.17)))    # colcha
    p.rrect(46, 662, 540, 712, 18, (0.46, 0.50, 0.58))                                 # colchón / sábana
    p.elip(150, 656, 90, 30, (0.62, 0.64, 0.70))                                       # almohada
    p.poly([(46, 700), (540, 700), (540, 740), (46, 760)], (0.20, 0.12, 0.16), 0.45)
    for x in (78, 508):
        p.rect(x, 800, x + 14, 836, (0.12, 0.08, 0.06))
    # escritorio
    p.rect(800, DESK_Y, 1920, DESK_Y + 24, (0.34, 0.23, 0.16), grad=((0.40, 0.29, 0.20), (0.27, 0.18, 0.13)))
    p.rect(800, DESK_Y + 24, 1920, DESK_Y + 32, (0.10, 0.07, 0.05))
    p.rect(826, DESK_Y + 32, 866, 1080, (0.20, 0.13, 0.09))
    p.rect(1842, DESK_Y + 32, 1900, 1080, (0.20, 0.13, 0.09))
    p.rect(866, DESK_Y + 32, 1842, 1080, (0.07, 0.05, 0.05))                           # hueco del escritorio
    p.rrect(1650, DESK_Y + 60, 1830, DESK_Y + 170, 6, (0.24, 0.16, 0.12), borde=(0.12, 0.08, 0.06), w=3)   # cajón
    p.rrect(1710, DESK_Y + 104, 1770, DESK_Y + 118, 6, (0.55, 0.50, 0.40))
    # teclado y ratón (sobre el escritorio)
    p.poly([(880, 808), (1400, 808), (1440, 836), (850, 836)], (0.40, 0.38, 0.32), grad=((0.46, 0.44, 0.37), (0.34, 0.32, 0.27)))
    for r in range(4):
        for c in range(22):
            x0 = 892 + c * 22 + r * 6
            p.rect(x0, 812 + r * 6.4, x0 + 17, 816.5 + r * 6.4, (0.14, 0.13, 0.12), 0.9)
    p.elip(1495, 826, 24, 11, (0.45, 0.43, 0.36))
    p.polilinea([(1470, 824), (1445, 806), (1400, 800)], 3, (0.10, 0.10, 0.10))
    # torre
    torre(p, t)


def cama_luna(p, k):
    """La cama a la luz de la luna (emisivo, sobre el cuarto apagado): colchón, colcha y almohada con un borde frío."""
    if k <= 0.01:
        return
    mo = tuple(np.array(MOON) * 0.34)
    p.rrect(46, 662, 540, 712, 18, mo, 0.55 * k, borde=MOON, w=3, op_b=0.55 * k)
    p.rrect(46, 690, 540, 806, 10, tuple(np.array(MOON) * 0.20), 0.60 * k, borde=MOON, w=3, op_b=0.40 * k)
    p.elip(150, 656, 90, 30, tuple(np.array(MOON) * 0.55), 0.55 * k)
    p.polilinea([(46, 740), (540, 740)], 3, MOON, 0.22 * k)


def torre(p, t, led=True):
    """Torre beige con lector de CD, disquetera y botón (albedo)."""
    p.rrect(1690, 470, 1862, DESK_Y, 8, BEIGE, grad=((0.66, 0.62, 0.50), (0.50, 0.46, 0.36)), borde=(0.34, 0.31, 0.25), w=3)
    p.rrect(1706, 500, 1846, 540, 4, (0.52, 0.48, 0.38))
    p.rect(1714, 512, 1838, 530, (0.06, 0.06, 0.06))                                    # ranura del CD
    p.rect(1714, 566, 1838, 578, (0.06, 0.06, 0.06))                                    # disquetera
    p.rect(1712, 590, 1750, 600, (0.35, 0.32, 0.26))
    for i in range(9):
        p.rect(1706, 620 + i * 7, 1846, 623 + i * 7, (0.40, 0.37, 0.30), 0.8)           # rejilla
    p.circ(1730, 712, 12, (0.36, 0.33, 0.27))
    p.circ(1730, 712, 7, (0.20, 0.19, 0.16))


def torre_luces(p, t, bandeja=0.0, leyendo=0.0):
    """Luces del lector y bandeja del CD (emisivo, se dibuja DESPUÉS de iluminar)."""
    on = 0.6 + 0.4 * (math.sin(t * 2.0) > -0.3)
    p.circ(1790, 712, 4, (0.35, 1.0, 0.45), 0.9)
    p.glow(1790, 712, 22, (0.35, 1.0, 0.45), 0.5)
    k = leyendo * (0.5 + 0.5 * math.sin(t * 31))
    p.circ(1816, 712, 4, (1.0, 0.7, 0.2), 0.25 + 0.75 * k)
    p.glow(1816, 712, 22, (1.0, 0.7, 0.2), 0.5 * k)
    if bandeja > 0.01:                                                                   # la bandeja sale hacia el frente
        h = 62 * smooth(bandeja)
        p.poly([(1716, 528), (1836, 528), (1846, 528 + h), (1706, 528 + h)], (0.55, 0.53, 0.47), 0.96)
        p.polilinea([(1716, 528), (1836, 528), (1846, 528 + h), (1706, 528 + h)], 2, (0.20, 0.19, 0.16), 0.9, cerrado=True)
        p.elip(1776, 528 + h * 0.55, 46, 16 * smooth(bandeja), (0.28, 0.27, 0.25), 0.9)


# ================================================================== monitor CRT de PC (después de iluminar)
def monitor_pc(p, scr, t, luz, apagado_=False):
    """Monitor CRT beige: pie giratorio, caja, marco hundido y la pantalla `scr` (float32 SHxSW ya con efecto CRT)."""
    a = 0.30 if apagado_ else 1.0
    p.poly([(1060, 790), (1580, 790), (1640, 830), (1000, 830)], (0.02, 0.015, 0.015), 0.35)         # sombra sobre el escritorio
    p.poly([(1240, 742), (1380, 742), (1420, DESK_Y - 2), (1200, DESK_Y - 2)], (0.10, 0.095, 0.08))     # cuello
    p.elip(1310, DESK_Y - 4, 130, 13, (0.12, 0.11, 0.09))
    c0, c1 = mix((0.21, 0.195, 0.16), luz, 0.10), mix((0.11, 0.10, 0.08), luz, 0.06)
    p.rrect(990, 248, 1630, 752, 28, c0, grad=(c0, c1), borde=mix((0.30, 0.28, 0.22), luz, 0.12), w=3)
    p.rrect(1016, 276, 1604, 730, 32, (0.035, 0.035, 0.03))
    p.imagen((np.clip(scr, 0, 1) * 255).astype(np.uint8), SX0, SY0, SX1, SY1, 1.0, 34.0)
    p.poly([(SX0 + 20, SY0 + 10), (SX0 + 150, SY0 + 10), (SX0 + 30, SY0 + 190)], (1, 1, 1), 0.05)    # reflejo
    p.rrect(SX0, SY0, SX1, SY1, 34, None, borde=(0.0, 0.0, 0.0), w=5, op_b=0.6)
    for i in range(5):                                                                               # rejilla de ventilación
        p.rect(1360 + i * 18, 735, 1370 + i * 18, 746, (0.04, 0.04, 0.035))
    for i, x in enumerate((1066, 1092)):                                                             # botones
        p.rrect(x, 738, x + 18, 750, 3, (0.20, 0.19, 0.16))
    on = 0.55 + 0.45 * (math.sin(t * 1.4) > -0.5)
    p.circ(1590, 744, 5, (0.4, 1.0, 0.5) if not apagado_ else (1.0, 0.65, 0.1), 0.9 * on * (a if not apagado_ else 1))
    p.glow(1590, 744, 34, (0.4, 1.0, 0.5) if not apagado_ else (1.0, 0.65, 0.1), 0.35 * on)


# ================================================================== silueta del jugador en silla
def jugador_pc(p, t, luz, giro=0.0, k=1.0):
    """Tom sentado en una silla giratoria, de espaldas (silueta con luz de borde); `giro` 0..1 = se da la vuelta hacia la cama."""
    x0 = 640.0
    resp = 4 * math.sin(t * 1.5)
    hx = x0 + 4 - 62 * giro
    hy = 690 + resp * 0.5

    def forma(dx, col, op):
        x = x0 + dx
        p.rrect(x - 125, 760, x + 125, 960, 30, col, op)                                  # respaldo
        p.rect(x - 14, 990, x + 14, 1050, col, op)                                        # pistón
        for s_ in (-1, 0, 1):
            p.polilinea([(x, 1046), (x + s_ * 120, 1066)], 12, col, op)
            p.circ(x + s_ * 124, 1070, 12, col, op)
        p.elip(x, 990, 150, 40, col, op)                                                  # asiento
        p.elip(x, 905, 140, 130, col, op)                                                 # torso (sudadera)
        p.elip(x, 818 + resp, 158, 70, col, op)                                           # hombros
        p.polilinea([(x + 140, 805), (x + 205, 880), (x + 300, 905)], 46, col, op)       # brazo hacia el teclado
        p.polilinea([(x - 140, 805), (x - 192, 892), (x - 70, 962)], 46, col, op)
        p.elip(x + 3, 770 + resp * 0.5, 92, 40, col, op)                                  # capucha caída
        p.rect(x - 30, hy + 40, x + 30, 780, col, op)                                     # cuello
        p.circ(hx + dx, hy, 64, col, op)                                                  # cabeza
        for s_ in (-1, 1):
            p.elip(hx + dx + s_ * 62, hy + 6, 11, 18, col, op)
        for i in range(9):                                                                # pelo desordenado
            a = math.pi + (i - 4) * 0.34
            p.poly([(hx + dx + 50 * math.cos(a), hy + 50 * math.sin(a)), (hx + dx + 86 * math.cos(a + 0.15) + 4 * math.sin(t + i), hy + 86 * math.sin(a + 0.15)),
                    (hx + dx + 50 * math.cos(a + 0.4), hy + 50 * math.sin(a + 0.4))], col, op)
        if giro > 0.35:                                                                   # perfil: nariz hacia la cama
            p.poly([(hx + dx - 58, hy - 4), (hx + dx - 92, hy + 16), (hx + dx - 56, hy + 26)], col, op)
    forma(7, mix(luz, (1, 1, 1), 0.1), 0.50 * k)
    forma(0, SIL, k)


# ================================================================== Sonic: silueta de pie o peluche
def sonic_sil(p, x, y, s, luz, t, ojos=0.0, sangre=0.0, peluche=False, k=1.0):
    """Silueta de Sonic (propia, casi negra, con luz de borde). y = suelo. `peluche`: sentado, cabezón. `ojos` 0..1 brillo rojo;
    `sangre` 0..1 largo de los chorros que bajan de los ojos."""
    if k <= 0.01:
        return

    def forma(dx, col, op):
        with p.grupo(x + dx * s, y, s):
            if peluche:
                p.elip(0, -34, 54, 36, col, op)                                           # cuerpo redondo sentado
                for sg in (-1, 1):
                    p.elip(sg * 44, -12, 26, 14, col, op)                                 # patas
                    p.polilinea([(sg * 40, -52), (sg * 76, -30)], 18, col, op)           # brazos cortos
                hy_, hr = -108, 62
            else:
                for sg in (-1, 1):
                    p.polilinea([(sg * 13, -52), (sg * 17, -6)], 15, col, op)             # piernas largas
                    p.elip(sg * 24, -6, 25, 11, col, op)
                    p.polilinea([(sg * 24, -118), (sg * 52, -86), (sg * 58, -58)], 14, col, op)   # brazos
                p.elip(0, -92, 28, 44, col, op)                                           # torso
                hy_, hr = -162, 50
            # púas hacia atrás (a la izquierda)
            p.poly([(-hr * 0.7, hy_ - hr * 0.5), (-hr * 2.5, hy_ - hr * 0.2), (-hr * 0.85, hy_ + hr * 0.15)], col, op)
            p.poly([(-hr * 0.8, hy_ + hr * 0.05), (-hr * 2.6, hy_ + hr * 0.7), (-hr * 0.8, hy_ + hr * 0.6)], col, op)
            p.poly([(-hr * 0.3, hy_ - hr * 0.9), (-hr * 1.7, hy_ - hr * 1.5), (hr * 0.1, hy_ - hr * 0.95)], col, op)
            p.poly([(hr * 0.1, hy_ - hr * 0.95), (-hr * 0.2, hy_ - hr * 1.7), (hr * 0.5, hy_ - hr * 0.85)], col, op)   # púa frontal
            p.circ(0, hy_, hr, col, op)                                                   # cabeza
            p.elip(hr * 0.62, hy_ + hr * 0.28, hr * 0.62, hr * 0.46, col, op)            # hocico
            p.circ(hr * 1.12, hy_ + hr * 0.12, hr * 0.12, col, op)                        # nariz
    forma(7, mix(luz, (1, 1, 1), 0.12), 0.55 * k * k)
    forma(0, SIL, k)
    if ojos > 0.01:
        hy_, hr = (-108, 62) if peluche else (-162, 50)
        with p.grupo(x, y, s):
            for ex in (hr * 0.18, hr * 0.62):
                cx_, cy_ = ex, hy_ - hr * 0.08
                p.glow(cx_, cy_, hr * 0.8, SANGRE, 0.9 * ojos * k, 2.0)
                p.elip(cx_, cy_, hr * 0.17, hr * 0.26, (0.02, 0.0, 0.0), ojos * k)
                p.circ(cx_, cy_ + hr * 0.02, hr * 0.07, (1.0, 0.18, 0.12), ojos * k)
                if sangre > 0.01:                                                         # chorro que baja del ojo
                    l = hr * (0.4 + 2.2 * smooth(sangre)) * (0.8 + 0.2 * math.sin(t * 2 + ex))
                    p.polilinea([(cx_, cy_ + hr * 0.2), (cx_ + 3, cy_ + hr * 0.2 + l * 0.5), (cx_ - 1, cy_ + hr * 0.2 + l)], max(3, hr * 0.07), SANGRE, 0.9 * k)
                    p.circ(cx_ - 1, cy_ + hr * 0.2 + l, max(4, hr * 0.065), SANGRE, 0.9 * k)


# ================================================================== utilería: CD-R y nota
def cd_disco(p, x, y, s=1.0, tilt=0.6, u_texto=1.0, brillo=1.0):
    """CD-R sin carátula (visto en perspectiva: elipse). Lleva «SONIC.EXE» a rotulador (u_texto 0..1 lo va escribiendo)."""
    with p.grupo(x, y, s):
        p.elip(6, 10, 72, 72 * tilt, (0, 0, 0), 0.35)
        p.elip(0, 0, 70, 70 * tilt, (0.70 * brillo, 0.72 * brillo, 0.76 * brillo))
        p.elip(0, 0, 66, 66 * tilt, (0.82 * brillo, 0.83 * brillo, 0.85 * brillo))
        p.elip(0, 0, 24, 24 * tilt, (0.74 * brillo, 0.75 * brillo, 0.78 * brillo))
        p.elip(0, 0, 22, 22 * tilt, (0.80 * brillo, 0.81 * brillo, 0.83 * brillo), 1.0, w=0)
        p.elip(0, 0, 8, 8 * tilt, (0.07, 0.08, 0.10))
        for a in range(0, 360, 60):                                                       # destello del plástico
            p.elip(0, 0, 60, 60 * tilt, (1, 1, 1), 0.07, a0=a, a1=a + 24, w=0)
        if u_texto > 0.02:
            n = int(clamp(u_texto) * 9 + 0.999)                                           # el punto se dibuja a mano (la fuente lo trae como cuadro)
            w1 = ancho_texto("SONIC", 19, "mano")
            yy = 38 * tilt
            p.texto("SONIC"[:min(n, 5)], -(w1 + 8), yy, 19, (0.07, 0.07, 0.09), "mano", 0.95, "lm")
            if n > 5:
                p.circ(-2, yy + 6, 3.2, (0.07, 0.07, 0.09), 0.95)
            if n > 6:
                p.texto("EXE"[:n - 6], 3, yy, 19, (0.07, 0.07, 0.09), "mano", 0.95, "lm")


def nota_arrugada(p, x, y, s, t, u1=0.0, u2=0.0):
    """Nota amarilla arrugada con letra apurada (u1: «NO LO JUEGUES», u2: «DESTRÚYELO»)."""
    a = -0.06 + 0.01 * math.sin(t * 1.1)
    ca, sa = math.cos(a), math.sin(a)

    def rot(px_, py_):
        return (x + (px_ * ca - py_ * sa) * s, y + (px_ * sa + py_ * ca) * s)
    pts = [rot(-120, -78), rot(-30, -86), rot(60, -76), rot(124, -84), rot(130, -10), rot(122, 80), rot(30, 88), rot(-60, 78), rot(-126, 84), rot(-132, 0)]
    p.poly(pts, (0.80, 0.72, 0.38), grad=((0.88, 0.80, 0.44), (0.66, 0.58, 0.28)))
    p.polilinea(pts, 2, (0.40, 0.33, 0.14), 0.9, cerrado=True)
    for (a0, a1) in (((-90, -20), (30, 30)), ((20, -60), (-70, 60)), ((-30, 78), (90, 20))):   # arrugas
        p.linea(rot(*a0), rot(*a1), 2, (0.45, 0.38, 0.17), 0.45)
    cx_, cy_ = rot(0, -26)
    p.texto("NO LO JUEGUES"[:int(clamp(u1) * 13 + 0.999)], cx_, cy_, 26 * s, (0.10, 0.08, 0.06), "mano", 0.95 if u1 > 0.01 else 0.0)
    cx_, cy_ = rot(0, 26)
    p.texto("DESTRÚYELO"[:int(clamp(u2) * 10 + 0.999)], cx_, cy_, 30 * s, (0.45, 0.04, 0.04), "mano", 0.95 if u2 > 0.01 else 0.0)


# ================================================================== pantallas de PC (búfer SWxSH, 4:3)
def _cursor(q, x, y, op=1.0):
    pts = [(x, y), (x, y + 32), (x + 8, y + 25), (x + 14, y + 38), (x + 20, y + 35), (x + 14, y + 22), (x + 24, y + 22)]
    q.poly(pts, (1, 1, 1), op)
    q.polilinea(pts, 2, (0, 0, 0), op, cerrado=True)


def _ventana(q, x0, y0, x1, y1, titulo, u=1.0, cuerpo=(0.55, 0.57, 0.62)):
    q.rect(x0 + 8, y0 + 8, x1 + 8, y1 + 8, (0, 0, 0), 0.35 * u)
    q.rect(x0, y0, x1, y1, (0.50, 0.50, 0.52), u)
    q.rect(x0, y0, x1, y0 + 3, (0.8, 0.8, 0.8), 0.8 * u)
    q.rect(x0 + 4, y0 + 4, x1 - 4, y0 + 44, (0.02, 0.05, 0.50), u, grad=((0.02, 0.05, 0.36), (0.14, 0.32, 0.58)))
    q.texto(titulo, x0 + 16, y0 + 24, 22, (1, 1, 1), "bold", u, "lm")
    for i in range(3):
        q.rect(x1 - 44 - i * 34, y0 + 10, x1 - 14 - i * 34, y0 + 38, (0.78, 0.78, 0.78), u)
    q.rect(x0 + 8, y0 + 56, x1 - 8, y1 - 8, cuerpo, u)


def _barra_tareas(q, hora="23:47"):
    q.rect(0, SH - 64, SW, SH, (0.76, 0.76, 0.76))
    q.rect(0, SH - 64, SW, SH - 61, (1, 1, 1), 0.8)
    q.rect(10, SH - 54, 150, SH - 10, (0.74, 0.74, 0.74))
    q.rect(10, SH - 54, 150, SH - 52, (1, 1, 1), 0.9)
    q.texto("Inicio", 80, SH - 32, 24, (0.05, 0.05, 0.05), "bold")
    q.rect(SW - 150, SH - 54, SW - 10, SH - 10, (0.70, 0.70, 0.70))
    q.texto(hora, SW - 80, SH - 32, 22, (0.05, 0.05, 0.05), "semi")


def pant_escritorio(t, u_win=0.0, u_sel=0.0, u_err=0.0):
    """Escritorio de PC de 2011: iconos, ventana de la unidad D: con el icono SONIC.EXE, o un aviso de «inserte un disco»."""
    q = P(SW, SH)
    q.fondo((0.02, 0.36, 0.42), (0.02, 0.30, 0.38))
    for i, (nom, col) in enumerate((("Mi PC", (0.82, 0.82, 0.86)), ("Documentos", (0.92, 0.82, 0.34)), ("Papelera", (0.62, 0.72, 0.66)))):
        x, y = 86, 100 + i * 160
        q.rrect(x - 36, y - 30, x + 36, y + 30, 6, col, 0.95, borde=(0.08, 0.08, 0.1), w=2)
        q.texto(nom, x, y + 66, 22, (1, 1, 1), "semi", 0.95, "mm", 0, 0.8)
    if u_win > 0.01:
        k = e_out(u_win)
        x0, y0, x1, y1 = 260, 130, 960, 660
        _ventana(q, x0, y0, x1, y1, "Disco compacto (D:)", k)
        q.rect(x0 + 8, y0 + 56, x1 - 8, y0 + 92, (0.86, 0.86, 0.86), k)
        for j, m in enumerate(("Archivo", "Edición", "Ver", "Ayuda")):
            q.texto(m, x0 + 24 + j * 110, y0 + 74, 20, (0.1, 0.1, 0.1), "med", k, "lm")
        ix, iy = 420, 320
        if u_sel > 0.01:
            q.rect(ix - 82, iy - 52, ix + 82, iy + 92, (0.05, 0.12, 0.62), 0.28 * u_sel)
        q.rrect(ix - 34, iy - 40, ix + 34, iy + 30, 6, (0.88, 0.88, 0.9), k, borde=(0.3, 0.3, 0.35), w=3)
        q.circ(ix, iy - 4, 24, (0.75, 0.78, 0.82), k)
        q.circ(ix, iy - 4, 6, (0.9, 0.9, 0.92), k)
        q.rect(ix - 80, iy + 46, ix + 80, iy + 80, (0.05, 0.12, 0.62) if u_sel > 0.5 else (0.97, 0.97, 0.97), k)
        q.texto("SONIC.EXE", ix, iy + 63, 22, (1, 1, 1) if u_sel > 0.5 else (0.05, 0.05, 0.05), "bold", k)
        q.texto("1 objeto", x0 + 24, y1 - 24, 18, (0.3, 0.3, 0.3), "med", k, "lm")
        if u_sel > 0.01:
            _cursor(q, ix + 20, iy + 40 + 20 * (1 - u_sel))
    if u_err > 0.01:
        k = e_out(u_err)
        x0, y0, x1, y1 = 300, 270, 920, 560
        _ventana(q, x0, y0, x1, y1, "D:\\", k, (0.52, 0.52, 0.54))
        q.circ(x0 + 80, y0 + 150, 34, SANGRE, k)
        q.texto("X", x0 + 80, y0 + 150, 40, (1, 1, 1), "xbold", k)
        q.texto("No hay ningún disco en la unidad.", x0 + 140, y0 + 138, 24, (0.05, 0.05, 0.05), "semi", k, "lm")
        q.texto("Inserte un disco e intente de nuevo.", x0 + 140, y0 + 176, 24, (0.05, 0.05, 0.05), "semi", k, "lm")
        q.rect(x0 + 250, y1 - 74, x0 + 370, y1 - 30, (0.74, 0.74, 0.74))
        q.texto("Aceptar", x0 + 310, y1 - 52, 22, (0.05, 0.05, 0.05), "bold")
    _barra_tareas(q)
    return q


def _titulo_base(q, seg, brillo=1.0):
    fr = Clip.cuadro("titulo_real", 2.0 + (seg % 5.0))
    q.imagen(fr, 0, 30, SW, SH - 30, 1.0, 0.0, brillo)
    return fr


def pant_titulo(t, seg, p_cielo=0.0, p_oxid=0.0, p_666=0.0, p_roja=0.0, brillo=1.0, press=0.0):
    """Pantalla de título real de Sonic 1 (320x224) que se corrompe: cielo oscuro, emblema oxidado, ©SEGA 1991 -> 666, agua roja."""
    q = P(SW, SH)
    q.fondo((0, 0, 0), (0, 0, 0))
    _titulo_base(q, seg, brillo)
    im, y0, hh = q.im, 30, SH - 60
    f = lambda a, b: slice(y0 + int(a * hh), y0 + int(b * hh))
    if p_cielo > 0.01:                                                                    # el cielo (y el lago lejano) se vuelven ceniza
        n = int(0.66 * hh)
        sk = im[y0:y0 + n]
        wy = np.clip((0.64 - (np.arange(n, dtype=np.float32) / hh)) / 0.14, 0, 1)[:, None, None]
        lum = sk.mean(2, keepdims=True)
        im[y0:y0 + n] = mix_arr(sk, lum * np.float32((0.55, 0.40, 0.45)) * 0.50, 0.88 * p_cielo * wy)
    if p_oxid > 0.01:                                                                     # el emblema se oxida
        yy, xx = np.mgrid[0:SH, 0:SW].astype(np.float32)
        m = np.clip(1 - (((xx - SW * 0.5) / (SW * 0.40)) ** 2 + ((yy - (y0 + hh * 0.42)) / (hh * 0.46)) ** 2), 0, 1)[..., None]
        rng = np.random.default_rng(7)
        ru = cv2.resize(rng.random((38, 50)).astype(np.float32), (SW, SH), interpolation=cv2.INTER_CUBIC)[..., None]
        ox = im.mean(2, keepdims=True) * np.float32((1.25, 0.62, 0.28)) * (0.55 + 0.6 * ru)
        im[:] = mix_arr(im, ox, 0.62 * p_oxid * np.clip(m * 1.4, 0, 1))
    if p_roja > 0.01:                                                                     # el agua se vuelve roja
        w = im[f(0.47, 1.0)]
        lum = w.mean(2, keepdims=True)
        im[f(0.47, 1.0)] = mix_arr(w, lum * np.float32((1.55, 0.12, 0.10)) * 0.85, 0.90 * p_roja)
    if p_666 > 0.01 or p_roja > 0.01:                                                     # «1991» -> «666»
        x0, x1 = int(SW * 0.829), int(SW * 0.932)
        yc = y0 + int(hh * 0.912)
        reg = im[yc - 24:yc + 22, x0 - 6:x1 + 10]
        base = reg.copy()
        if p_666 > 0.01:
            patch = np.float32(mix((0.05, 0.08, 0.40), (0.38, 0.03, 0.04), p_roja)) * (0.9 + 0.2 * rnd(int(t * 12), 3))
            reg[:] = mix_arr(base, np.broadcast_to(patch, base.shape), clamp(p_666 * 3))
            q.texto("666", (x0 + x1) / 2 + 4, yc, 32, mix((1.0, 0.92, 0.9), SANGRE, 0.75 * p_666), "pixel", clamp(p_666 * 3))
    if press > 0.01 and int(t * 2) % 2 == 0:
        q.texto("PRESS START", SW / 2, y0 + hh * 0.80, 34, (1, 1, 1), "pixel", press, "mm", 0.0, 0.8)
    return q


def mix_arr(a, b, u):
    return a * (1 - u) + b * u


def pant_clip43(nombre, seg, ini, fin, brillo=1.0, recorte=0.03):
    """Video real en 4:3 a pantalla completa; recorta el borde inferior (marca de agua del canal de origen)."""
    q = P(SW, SH)
    d = max(0.1, fin - ini)
    fr = Clip.cuadro(nombre, ini + (seg % d) if d > 0.5 else ini)
    h = fr.shape[0]
    q.imagen(np.ascontiguousarray(fr[:int(h * (1 - recorte))]), 0, 0, SW, SH, 1.0, 0.0, brillo)
    return q


def pant_wiki(t, t0, u_elim=0.0, u_s1=0.0, u_s2=0.0):
    """Página de una wiki de creepypastas (solo texto, sin logo). u_elim 0..1: el relato se borra y queda el sello ELIMINADO;
    u_s1 / u_s2 0..1: los sellos «MAL ESCRITO» y «CLICHÉS» (los motivos que dio el autor del borrado) caen debajo."""
    q = P(SW, SH)
    q.fondo((0.10, 0.09, 0.14), (0.07, 0.06, 0.10))
    q.rect(0, 0, SW, 80, (0.20, 0.16, 0.30), 0.95)
    q.texto("CREEPYPASTA WIKI", 36, 40, 34, (0.88, 0.84, 1.0), "xbold", 1.0, "lm")
    q.rect(SW - 340, 22, SW - 30, 58, (0.10, 0.09, 0.16), 0.9)
    q.texto("buscar…", SW - 320, 40, 20, (0.55, 0.52, 0.7), "med", 1.0, "lm")
    q.rrect(40, 110, SW - 40, SH - 40, 12, (0.15, 0.14, 0.20), 0.96, borde=(0.30, 0.27, 0.40), w=3)
    ku = pr(t, t0, t0 + 0.4)
    q.texto("Sonic.exe", 80, 176, 74, (0.96, 0.94, 1.0), "xbold", ku, "lm")
    q.texto("por JC-the-Hyena", 84, 246, 32, (0.78, 0.74, 0.96), "semi", pr(t, t0 + 0.5, t0 + 0.9), "lm")
    q.texto("9 AGO 2011", SW - 80, 246, 32, HUESO, "semi", pr(t, t0 + 1.0, t0 + 1.4), "rm")
    q.rect(80, 280, SW - 80, 284, (0.40, 0.34, 0.60), 0.8)
    n_lin = 13
    for i in range(n_lin):
        u = pr(t, t0 + 0.8 + i * 0.07, t0 + 1.1 + i * 0.07)
        gone = clamp(pr(u_elim, 0.0, 1.0) * 1.6 - rnd(i, 31) * 0.6)
        ancho = (480 + 560 * rnd(i, 4)) * (0.55 if i % 5 == 4 else 1.0)
        y = 322 + i * 40
        q.rect(80, y - 9, 80 + ancho * u * (1 - gone), y + 9, (0.62, 0.58, 0.80), 0.50 + 0.2 * rnd(i, 7))
    if u_elim > 0.01:
        k = clamp(u_elim * 3)
        q.rect(210, 400, SW - 210, 700, (0.0, 0.0, 0.0), 0.65 * k)
        q.rrect(250, 430, SW - 250, 670, 14, None, borde=SANGRE, w=8, op_b=k)
        q.texto("ELIMINADO", SW / 2, 520, 92, SANGRE, "xbold", k, "mm", 0.03, 0.9)
        q.texto("14 ENE 2014", SW / 2, 620, 56, HUESO, "bold", k, "mm", 0.02, 0.9)
    for u_s, x0_, txt in ((u_s1, 90, "MAL ESCRITO"), (u_s2, 650, "CLICHÉS")):
        if u_s > 0.01:
            k = clamp(u_s * 3)
            with q.grupo(x0_ + 240, 790, lerp(1.35, 1.0, e_out(k))):
                q.rrect(-240, -52, 240, 52, 10, (0.0, 0.0, 0.0), 0.62 * k, borde=SANGRE, w=5, op_b=k)
                q.texto(txt, 0, 0, 54, SANGRE, "xbold", k, "mm", 0.02, 0.9)
    return q


def pant_captura(t, u):
    """Editor de imágenes: a la izquierda la captura original del título de Sonic 1; a la derecha, la misma captura retocada."""
    q = P(SW, SH)
    q.fondo((0.20, 0.20, 0.22), (0.16, 0.16, 0.18))
    _ventana(q, 40, 70, SW - 40, SH - 110, "Editor de imágenes", 1.0, (0.30, 0.30, 0.33))
    q.rect(60, 140, 130, SH - 130, (0.60, 0.60, 0.62))
    for i in range(6):
        q.rrect(72, 156 + i * 78, 118, 198 + i * 78, 6, (0.80, 0.80, 0.82), borde=(0.3, 0.3, 0.3), w=2)
    a = _frame_titulo(3.0)
    q_ret = pant_titulo(t, 3.0, 1.0, 1.0, 1.0, 0.0)
    ret = (np.clip(q_ret.im, 0, 1) * 255).astype(np.uint8)[30:SH - 30]
    ancho = 520
    for j, (img, lab) in enumerate(((a, "ORIGINAL"), (ret, "RETOCADA"))):
        x0 = 150 + j * (ancho + 14)
        k = pr(u, j * 0.4, j * 0.4 + 0.4)
        q.rect(x0 - 3, 210 - 3, x0 + ancho + 3, 210 + ancho * 0.7 + 3, (0.05, 0.05, 0.06), k)
        q.imagen(img, x0, 210, x0 + ancho, 210 + ancho * 0.7, k, 0.0)
        q.texto(lab, x0 + ancho / 2, 170, 28, HUESO if j == 0 else SANGRE, "bold", k)
    for i, nom in enumerate(("Brillo", "Contraste", "Tono")):                          # panel de ajustes del editor
        y = 630 + i * 48
        k = pr(u, 0.6 + i * 0.15, 0.9 + i * 0.15)
        q.texto(nom, 160, y, 22, (0.78, 0.78, 0.8), "med", k, "lm")
        q.rect(300, y - 4, 1000, y + 4, (0.12, 0.12, 0.14), k)
        q.circ(300 + 700 * (0.62 - 0.4 * (i != 2) * pr(u, 0.8, 1.0)), y, 11, (0.8, 0.8, 0.85), k)
    return q


def _frame_titulo(seg):
    return Clip.cuadro("titulo_real", 2.0 + (seg % 5.0))


def pant_exe(t, u_prop=0.0, u_corre=0.0, t0=None):
    """Propiedades de un archivo .exe: «Aplicación»; al final el botón Ejecutar y un reloj de arena que gira.
    `t0` (inicio de la ventana): el cursor recorre el icono, el tipo y la acción hasta quedar sobre «Ejecutar»."""
    q = P(SW, SH)
    q.fondo((0.02, 0.36, 0.42), (0.02, 0.30, 0.38))
    _barra_tareas(q)
    k = e_out(u_prop)
    _ventana(q, 190, 100, 1030, 760, "Propiedades de sonic.exe", k)
    q.rrect(260, 220, 380, 340, 10, (0.86, 0.86, 0.90), k, borde=(0.3, 0.3, 0.35), w=3)
    q.rect(272, 232, 368, 256, (0.05, 0.12, 0.62), k)
    q.texto(".EXE", 640, 280, 120, (0.05, 0.05, 0.08), "black", k)
    q.texto("sonic.exe", 640, 396, 36, (0.05, 0.05, 0.08), "bold", k)
    for i, (a, b) in enumerate((("Tipo:", "Aplicación (.exe)"), ("Se ejecuta:", "en esta computadora"), ("Acción:", "ejecutar el programa"))):
        y = 470 + i * 58
        q.texto(a, 260, y, 24, (0.30, 0.30, 0.34), "med", k, "lm")
        q.texto(b, 460, y, 24, (0.05, 0.05, 0.08), "semi", k, "lm")
    pul = 0.5 + 0.5 * math.sin(t * 6)
    q.rect(730, 664, 990, 730, (0.74, 0.74, 0.74), k)
    if t0 is not None and u_corre <= 0.01 and u_prop > 0.3:
        ruta = ((0.4, 560, 160), (2.8, 320, 290), (5.2, 680, 480), (7.4, 700, 600), (8.9, 848, 720))
        s_ = t - t0
        x_, y_ = ruta[0][1:] if s_ <= ruta[0][0] else ruta[-1][1:]
        for (ta, xa, ya), (tb, xb, yb) in zip(ruta, ruta[1:]):
            if ta < s_ <= tb:
                u_ = smooth((s_ - ta) / (tb - ta))
                x_, y_ = lerp(xa, xb, u_), lerp(ya, yb, u_)
        _cursor(q, x_, y_, k)
    if u_corre > 0.01:
        q.rect(730, 664, 990, 730, SANGRE, 0.35 * u_corre * (0.6 + 0.4 * pul))
        _cursor(q, 840 + 8 * (1 - u_corre), 690 + 30 * (1 - u_corre))
        for i in range(8):                                                                  # reloj de carga
            a = t * 7 + i * math.pi / 4
            q.circ(640 + 44 * math.cos(a), 690 + 44 * math.sin(a), 6, (0.1, 0.1, 0.1), 0.2 + 0.8 * (i / 8) * u_corre)
    q.texto("Ejecutar", 860, 697, 28, (0.05, 0.05, 0.08), "bold", k)
    return q


def pant_doc(t, t0, u_marca=0.0):
    """Documento de texto: un relato amateur lleno de tópicos (barras de texto con subrayados rojos y sellos «CLICHÉ»)."""
    q = P(SW, SH)
    q.fondo((0.02, 0.36, 0.42), (0.02, 0.30, 0.38))
    _barra_tareas(q)
    _ventana(q, 70, 70, SW - 70, SH - 100, "Sonic.exe.txt - Bloc de notas", 1.0, (0.52, 0.52, 0.49))
    for i in range(15):
        u = pr(t, t0 + i * 0.06, t0 + 0.3 + i * 0.06)
        ancho = (560 + 380 * rnd(i, 9)) * (0.6 if i % 6 == 5 else 1.0)
        y = 188 + i * 40
        q.rect(110, y - 7, 110 + ancho * u, y + 7, (0.30, 0.30, 0.34), 0.75)
    for j, (x, y, w) in enumerate(((140, 228, 420), (300, 388, 300), (180, 548, 460), (430, 668, 330))):
        m = pr(u_marca, j * 0.22, j * 0.22 + 0.25)
        if m > 0.01:
            q.polilinea([(x + w * m * (i / 12), y + 10 + 4 * (i % 2)) for i in range(13)], 4, SANGRE, 0.9)
            q.rrect(x + w + 14, y - 26, x + w + 176, y + 4, 6, None, borde=SANGRE, w=3, op_b=m)
            q.texto("CLICHÉ", x + w + 95, y - 11, 22, SANGRE, "bold", m)
    return q


def pant_web(t, tipo, t0, u_a=0.0, u_b=0.0, u_c=0.0):
    """Páginas web dibujadas (solo texto, sin logos): 'gj' (juego fan), 'video' (partida), 'blog' (furioso), 'broma'."""
    q = P(SW, SH)
    if tipo == "gj":
        q.fondo((0.07, 0.07, 0.10), (0.05, 0.05, 0.08))
        q.rect(0, 0, SW, 76, (0.11, 0.11, 0.16), 0.95)
        q.texto("GAME JOLT", 36, 38, 32, (0.60, 1.0, 0.74), "xbold", 1.0, "lm")
        k = pr(t, t0, t0 + 0.5)
        q.rrect(50, 120, 760, 640, 12, (0.02, 0.02, 0.03), k, borde=(0.25, 0.25, 0.32), w=3)
        q.imagen(Clip.cuadro("fuego", 1.0 + (t % 5) * 0.2), 56, 126, 754, 634, k, 8.0, 0.9)
        q.texto("Sonic.exe", 800, 180, 56, (0.97, 0.97, 1.0), "xbold", k, "lm")
        q.texto("por MY5TCrimson", 802, 250, 30, (0.70, 1.0, 0.82), "semi", pr(u_b, 0, 1), "lm")
        q.rrect(800, 300, 1080, 360, 28, (0.30, 0.10, 0.12), pr(u_a, 0, 1), borde=SANGRE, w=3, op_b=pr(u_a, 0, 1))
        q.texto("AGO 2012", 940, 330, 32, HUESO, "bold", pr(u_a, 0, 1))
        for i in range(5):
            q.rect(800, 420 + i * 44, 800 + 260 + 60 * rnd(i, 4), 432 + i * 44, (0.5, 0.5, 0.62), 0.35 * k)
        pul = 0.75 + 0.25 * math.sin(t * 6) * u_c
        q.rrect(800, 650, 1130, 730, 16, (0.20 * pul, 0.80 * pul, 0.50 * pul), pr(u_c, 0, 1) if u_c > 0 else 0.35, borde=(0.7, 1.0, 0.8), w=3)
        q.texto("DESCARGAR", 965, 690, 36, (0.02, 0.10, 0.06), "xbold", 1.0 if u_c > 0 else 0.5)
        for i in range(4):
            q.rect(60 + i * 180, 680, 60 + i * 180 + 150, 720, (0.5, 0.5, 0.62), 0.25 * k)
    elif tipo == "video":
        q.fondo((0.05, 0.05, 0.06), (0.03, 0.03, 0.04))
        q.rect(0, 0, SW, 70, (0.09, 0.09, 0.10), 0.95)
        q.texto("VIDEO", 36, 35, 30, (0.95, 0.95, 0.95), "xbold", 1.0, "lm")
        q.rrect(60, 100, SW - 60, 690, 10, (0, 0, 0), 1.0, borde=(0.25, 0.25, 0.28), w=3)
        q.imagen(Clip.cuadro("eggman", 0.5 + (t % 6)), 66, 106, SW - 66, 684, 1.0, 6.0, 0.85)
        q.poly([(SW / 2 - 40, 330), (SW / 2 - 40, 450), (SW / 2 + 52, 390)], (1, 1, 1), 0.85 * (1 - u_b))
        q.rect(60, 700, SW - 60, 708, (0.25, 0.25, 0.28))
        q.rect(60, 700, 60 + (SW - 120) * (0.1 + 0.75 * clamp(pr(t, t0, t0 + 6))), 708, (0.95, 0.15, 0.15))
        q.circ(100, 770, 34, (0.4, 0.4, 0.5), pr(u_a, 0, 1))
        q.texto("PEWDIEPIE", 160, 770, 54, (1, 1, 1), "xbold", pr(u_a, 0, 1), "lm", 0.01, 0.9)
        q.texto("su partida", 164, 826, 28, (0.7, 0.7, 0.78), "semi", pr(u_a, 0.3, 1), "lm")
    elif tipo == "blog":
        q.fondo((0.16, 0.05, 0.05), (0.08, 0.02, 0.03))
        q.rect(0, 0, SW, 76, (0.30, 0.06, 0.07), 0.95)
        q.texto("BLOG", 36, 38, 34, HUESO, "xbold", 1.0, "lm")
        for i in range(11):
            u = pr(t, t0 + 0.2 + i * 0.12, t0 + 0.5 + i * 0.12)
            sh = (3 + 6 * u_a) * math.sin(t * 25 + i * 3)
            ancho = 700 + 360 * rnd(i, 3)
            y = 150 + i * 62
            q.rect(70 + sh, y - 15, 70 + ancho * u + sh, y + 15, (0.92, 0.25, 0.22), 0.65 + 0.3 * rnd(i, 8))
        for j in range(3):
            q.texto("!" * (3 + j), 1080 - j * 120, 220 + j * 260, 160 + 40 * u_a, SANGRE, "black", pr(u_a, 0, 0.5) * (0.5 + 0.3 * math.sin(t * 9 + j)), "mm")
    else:                                                                                # 'broma': una carita sonriente cansada
        q.fondo((0.06, 0.06, 0.08), (0.03, 0.03, 0.05))
        k = pop(t, t0, 0.5)
        with q.grupo(SW / 2, SH / 2, clamp(k, 0, 1.2)):
            q.circ(0, 0, 250, (0.98, 0.82, 0.22), 1.0)
            q.circ(0, 0, 250, (0.5, 0.35, 0.05), 1.0, w=8)
            for s_ in (-1, 1):
                q.elip(s_ * 90, -60, 26, 38, (0.1, 0.07, 0.03), 1.0)
            q.elip(0, 70, 120, 78, (0.1, 0.07, 0.03), 1.0, a0=10, a1=170, w=14)
            q.texto("JAJA", 0, 330, 70, HUESO, "xbold", 0.9, "mm", 0.03, 0.9)
    return q
