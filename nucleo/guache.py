# -*- coding: utf-8 -*-
"""Kit del estilo `guache` (ilustración de libro infantil en gouache; ref. «Economía de la isla», @e_page).

Estética: paleta apagada y cálida (azul verdoso, crema, arena, terracota), formas planas SIN contorno con una
media luna de sombra (dos tonos), cabezas redondas con ojos de punto, mejillas rosadas, grano de papel
(`efectos.acabado` con `papel`). Todo son funciones del tiempo, en px de 1080p (origen de los personajes: los pies).

  personajes : hombre (Don Beto), escorpion, trex, tiburon, platillo, dragon
  armas      : chancla, sarten, pez_espada, extintor, tapa_olla
  efectos    : estrellitas, explosion, ono (onomatopeya), polvo, spray, fuego, salpicadura, brillo
  mundo      : fondo_mundo(X0, t) -> 5 biomas (desierto, selva, oceano, luna, volcan) en un plano continuo
  interfaz   : barra, rotulo, pastilla
"""
import math

import cv2
import numpy as np

from motor import (H, W, catmull, circulo, clamp01, e_back, e_in, e_inout, e_out, elipse, h01, lerp, prog, rect_red,
                   ruido1, smooth)

PI = math.pi
BIOMA_W = 1920.0      # ancho de cada bioma en el mundo continuo


# ------------------------------------------------------------------ color
def mezcla(c1, c2, u):
    u = clamp01(u)
    return tuple(int(round(a + (b - a) * u)) for a, b in zip(c1[:3], c2[:3]))


SOMBRA = (74, 52, 72)
LUZ = (255, 244, 218)
TINTA = (64, 48, 52)


def ton(c, u=0.28):
    return mezcla(c, SOMBRA, u)


def luz(c, u=0.3):
    return mezcla(c, LUZ, u)


C = dict(
    crema=(240, 230, 206), arena=(226, 198, 150), arena_o=(198, 162, 116), duna=(214, 176, 126),
    mar=(112, 158, 158), mar_o=(84, 128, 132), espuma=(238, 242, 230),
    palma=(92, 132, 90), palma_o=(64, 98, 72), selva=(72, 110, 84), selva_c=(128, 160, 106),
    marron=(150, 104, 74), marron_o=(112, 78, 58), rojo=(198, 100, 74), mostaza=(228, 178, 88),
    azul=(98, 128, 166), lila=(156, 134, 166), piel=(238, 186, 144), piel_o=(208, 148, 114),
    lava=(232, 118, 62), lava_c=(248, 192, 96), ceniza=(92, 72, 80), roca=(128, 108, 108),
    luna=(198, 194, 198), noche=(56, 60, 92), alien=(150, 190, 120), acero=(150, 154, 164),
    rosa=(232, 150, 140), blanco=(246, 240, 226),
)


# ------------------------------------------------------------------ primitivas
def capsula(x0, y0, x1, y1, w0, w1=None, n=8):
    ang = math.atan2(y1 - y0, x1 - x0)
    r0, r1_ = w0 / 2, (w1 if w1 is not None else w0) / 2
    a = np.linspace(ang + PI / 2, ang + 3 * PI / 2, n)
    b = np.linspace(ang - PI / 2, ang + PI / 2, n)
    return np.concatenate([np.stack([x0 + r0 * np.cos(a), y0 + r0 * np.sin(a)], 1),
                           np.stack([x1 + r1_ * np.cos(b), y1 + r1_ * np.sin(b)], 1)])


def rot_pts(P, ang, cx=0.0, cy=0.0):
    c, s = math.cos(ang), math.sin(ang)
    P = np.asarray(P, float) - (cx, cy)
    return np.stack([P[:, 0] * c - P[:, 1] * s + cx, P[:, 0] * s + P[:, 1] * c + cy], 1)


def sombreado(lz, P, color, k=0.10, dirx=-0.7, diry=-0.7, u=0.28, alfa=1.0):
    """Relleno con media luna de sombra: forma oscura y encima la misma forma algo menor y corrida hacia la luz."""
    P = np.asarray(P, float)
    c = P.mean(0)
    ext = float(np.abs(P - c).max(0).min())
    lz.relleno(P, ton(color, u), alfa=alfa)
    lz.relleno(c + (P - c) * (1 - k) + np.array([dirx, diry]) * ext * k * 0.9, color, alfa=alfa)


def disco(lz, x, y, r, color, sombra=True, alfa=1.0):
    P = circulo(x, y, r, 40)
    if sombra and r > 7:
        sombreado(lz, P, color, alfa=alfa)
    else:
        lz.relleno(P, color, alfa=alfa)


def elip(lz, x, y, rx, ry, color, rot=0.0, sombra=True, alfa=1.0):
    P = elipse(x, y, rx, ry, rot, 40)
    if sombra and min(rx, ry) > 6:
        sombreado(lz, P, color, alfa=alfa)
    else:
        lz.relleno(P, color, alfa=alfa)


def cap(lz, x0, y0, x1, y1, w0, w1=None, color=(200, 200, 200), sombra=True):
    P = capsula(x0, y0, x1, y1, w0, w1)
    if sombra and min(w0, w1 or w0) > 9:
        sombreado(lz, P, color, k=0.12)
    else:
        lz.relleno(P, color)


def estrella_pts(cx, cy, r1, r2, n=5, rot=-PI / 2):
    a = rot + np.arange(2 * n) * PI / n
    r = np.where(np.arange(2 * n) % 2 == 0, r1, r2)
    return np.stack([cx + r * np.cos(a), cy + r * np.sin(a)], 1)


def ojo_x(lz, x, y, r, col=TINTA, w=None):
    w = w or max(3.0, r * 0.32)
    lz.relleno(capsula(x - r, y - r, x + r, y + r, w), col)
    lz.relleno(capsula(x - r, y + r, x + r, y - r, w), col)


# ------------------------------------------------------------------ personaje: Don Beto
CARAS = ("normal", "brava", "asombro", "grito", "ko", "sonrisa", "miedo", "esfuerzo", "victoria")


def _pierna(lz, cx, hy, fx, fy, col, sandalia=True, alto=1.0):
    cap(lz, cx, hy, fx, fy - 12, 30, 24, col)
    # pie + chancla
    lz.relleno(elipse(fx + 10, fy - 6, 20, 8.5, 0, 24), C["piel_o"])
    if sandalia:
        lz.relleno(elipse(fx + 10, fy - 1.5, 27, 7.5, 0, 24), ton(C["rojo"], 0.1))
        lz.relleno(capsula(fx + 4, fy - 9, fx + 20, fy - 5, 5), C["crema"])


def hombre(lz, x, y, s=1.0, t=0.0, *, mirar=1, ph=0.0, paso=0.0, inc=0.0, agach=0.0, sq=1.0, cara="normal",
           brazo_f=(1.2, 1.5), brazo_b=(1.7, 1.9), arma_f=None, arma_b=None, casco=0.0, sudor=0.0, alfa=1.0,
           parpadeo=True, flotar=0.0, camisa=None, ret=False):
    """Don Beto: hombre común (tirantes, bigote, chanclas). Origen = pies. Ángulos de brazo en rad (0 = derecha, pi/2
    = abajo); brazo_f = (hombro, antebrazo) del brazo delantero. arma_f/arma_b: fn(lz, x, y, ang) dibujada en la mano.
    Devuelve las posiciones locales de la mano delantera y trasera (para colocar objetos)."""
    camisa = camisa or C["blanco"]
    pan = (52, 78, 116)
    piel, pielo = C["piel"], C["piel_o"]
    respira = math.sin(t * 3.1) * 2.0 * (1 - min(1, paso))
    bob = abs(math.sin(ph)) * 9 * paso - flotar
    cadera_y = -90 + 30 * agach
    hombro_y = cadera_y - 100 + 12 * agach + respira * 0.5
    cab_y = hombro_y - 55 + respira
    hands = {}
    with lz.grupo(x, y - bob, s * mirar, rot=inc * mirar, sy=s * sq):
        # --- piernas
        sw = math.sin(ph) * 0.62 * paso
        sep = 16 + 26 * agach
        L = 92 - 30 * agach
        for k, (cx0, sgn) in enumerate(((-sep * 0.5, -1), (sep * 0.5, 1))):
            a = sw * sgn
            fx = cx0 + math.sin(a) * L * 1.0 + (sgn * 4)
            fy = -max(0.0, math.cos(ph + (0 if sgn > 0 else PI))) * 12 * paso + (0 if paso > 0.01 else 0) + (
                -(L - math.cos(a) * L) * 0.0)
            fy = min(0.0, fy - 0.0)
            _pierna(lz, cx0, cadera_y - 6, fx, fy, ton(pan, 0.1 if sgn > 0 else 0.3))
        # --- brazo trasero (detrás del torso)
        sh_b = (-30.0, hombro_y + 8)
        p1 = (sh_b[0] + math.cos(brazo_b[0]) * 54, sh_b[1] + math.sin(brazo_b[0]) * 54)
        p2 = (p1[0] + math.cos(brazo_b[1]) * 52, p1[1] + math.sin(brazo_b[1]) * 52)
        cap(lz, sh_b[0], sh_b[1], p1[0], p1[1], 22, 20, ton(piel, 0.16))
        cap(lz, p1[0], p1[1], p2[0], p2[1], 19, 17, ton(piel, 0.16))
        disco(lz, p2[0], p2[1], 12, ton(piel, 0.16), sombra=False)
        hands["b"] = (p2[0], p2[1], brazo_b[1])
        if arma_b:
            arma_b(lz, p2[0], p2[1], brazo_b[1])
        # --- torso
        lz.relleno(elipse(0, cadera_y - 2, 45, 32, 0, 30), pan)         # pantalón (bajo la camiseta)
        tor = elipse(0, hombro_y + 48 - 7 * agach, 47, 60 - 7 * agach, 0, 44)
        sombreado(lz, tor, camisa, k=0.10, u=0.22)
        lz.relleno(rect_red(-9, cadera_y - 14, 18, 8, 3), C["mostaza"], alfa=0.0)
        # escote y tirantes
        lz.relleno(elipse(0, hombro_y - 7, 21, 15, 0, 24), piel)
        # --- cabeza
        cx, cy = 0.0, cab_y
        lz.relleno(capsula(0, hombro_y - 4, 0, cy + 20, 26), pielo)        # cuello
        for sg in (-1, 1):
            disco(lz, cx + sg * 47, cy + 4, 11, piel, sombra=False)          # orejas
        cab = circulo(cx, cy, 50, 48)
        sombreado(lz, cab, piel, k=0.09, u=0.20)
        # pelo (mechón oscuro arriba)
        arco = np.linspace(PI * 1.06, PI * 1.94, 22)
        pelo = np.concatenate([np.stack([cx + 51 * np.cos(arco), cy + 51 * np.sin(arco)], 1),
                               np.stack([cx + 40 * np.cos(arco[::-1]), cy - 8 + 42 * np.sin(arco[::-1])], 1)])
        lz.relleno(pelo, (58, 44, 46))
        lz.relleno(elipse(cx - 36, cy - 30, 9, 13, 0.5, 14), (58, 44, 46))
        lz.relleno(elipse(cx + 36, cy - 30, 9, 13, -0.5, 14), (58, 44, 46))
        _cara(lz, cx + 7, cy, cara, t, parpadeo, sudor)
        # casco-pecera (translúcido)
        if casco > 0.01:
            lz.relleno(circulo(cx, cy + 2, 64 * casco, 44), (200, 226, 232), alfa=0.26)
            lz.relleno(capsula(cx - 66 * casco, cy + 32, cx + 66 * casco, cy + 32, 12 * casco), C["acero"], alfa=0.95)
            lz.relleno(elipse(cx - 24 * casco, cy - 30 * casco, 15 * casco, 8 * casco, -0.6, 16), (255, 255, 255), alfa=0.55)
        # --- brazo delantero
        sh_f = (30.0, hombro_y + 8)
        p1 = (sh_f[0] + math.cos(brazo_f[0]) * 54, sh_f[1] + math.sin(brazo_f[0]) * 54)
        p2 = (p1[0] + math.cos(brazo_f[1]) * 52, p1[1] + math.sin(brazo_f[1]) * 52)
        cap(lz, sh_f[0], sh_f[1], p1[0], p1[1], 23, 21, piel)
        cap(lz, p1[0], p1[1], p2[0], p2[1], 20, 18, piel)
        disco(lz, p2[0], p2[1], 13, piel, sombra=False)
        hands["f"] = (p2[0], p2[1], brazo_f[1])
        if arma_f:
            arma_f(lz, p2[0], p2[1], brazo_f[1])
    return hands


def _cara(lz, x, y, cara, t, parpadeo, sudor):
    ojos_y = y - 4
    cerrado = parpadeo and (t % 3.7) < 0.12
    ceja = {"normal": (0.0, 0.0), "brava": (0.55, 0.55), "asombro": (-0.25, -0.25), "grito": (0.5, 0.5),
            "ko": (0.0, 0.0), "sonrisa": (-0.12, -0.12), "miedo": (-0.45, -0.45), "esfuerzo": (0.65, 0.65),
            "victoria": (-0.1, -0.1)}[cara]
    for sg, ex in ((-1, x - 19), (1, x + 17)):
        if cara == "ko":
            ojo_x(lz, ex, ojos_y, 8)
        elif cara == "asombro" or cara == "miedo":
            disco(lz, ex, ojos_y, 12, C["blanco"], sombra=False)
            disco(lz, ex + 2, ojos_y, 4.6, TINTA, sombra=False)
        elif cerrado or cara in ("victoria", "esfuerzo"):
            lz.relleno(capsula(ex - 8, ojos_y + 2, ex + 8, ojos_y + (0 if cara != "victoria" else -3), 4.5), TINTA)
        else:
            disco(lz, ex, ojos_y, 6.2, TINTA, sombra=False)
            disco(lz, ex + 2, ojos_y - 2.4, 2.1, C["blanco"], sombra=False)
        dy = -18 - (7 if cara in ("asombro", "miedo") else 0)
        a = ceja[0] * (1 if sg == -1 else -1)
        lz.relleno(capsula(ex - 11 * math.cos(a), y + dy - 11 * math.sin(a), ex + 11 * math.cos(a),
                           y + dy + 11 * math.sin(a), 5.5), (58, 44, 46))
    # mejillas y nariz
    for ex in (x - 33, x + 33):
        lz.relleno(elipse(ex, y + 14, 12, 8, 0, 20), C["rosa"], alfa=0.55)
    disco(lz, x + 2, y + 8, 9.5, C["piel_o"], sombra=False)
    # bigote
    lz.relleno(elipse(x - 12, y + 21, 15, 8, 0.22, 20), (58, 44, 46))
    lz.relleno(elipse(x + 14, y + 21, 15, 8, -0.22, 20), (58, 44, 46))
    # boca
    if cara in ("grito", "asombro", "miedo"):
        lz.relleno(elipse(x + 1, y + 35, 11 if cara != "asombro" else 8, 13 if cara != "asombro" else 10, 0, 20), (110, 52, 58))
        lz.relleno(elipse(x + 1, y + 41, 7, 5, 0, 12), C["rosa"])
    elif cara in ("sonrisa", "victoria"):
        arco = np.linspace(0.15, PI - 0.15, 14)
        lz.relleno(np.concatenate([np.stack([x + 1 + 15 * np.cos(arco), y + 30 + 13 * np.sin(arco)], 1),
                                   np.stack([x + 1 + 15 * np.cos(arco[::-1]), y + 30 + 5 * np.sin(arco[::-1])], 1)]), (110, 52, 58))
    elif cara == "esfuerzo":
        lz.relleno(rect_red(x - 12, y + 30, 26, 11, 4), C["blanco"])
        lz.relleno(capsula(x - 10, y + 35, x + 12, y + 35, 2.2), (110, 52, 58))
    elif cara == "ko":
        lz.relleno(capsula(x - 8, y + 36, x + 10, y + 34, 5), TINTA)
        lz.relleno(elipse(x + 6, y + 42, 6, 8, 0, 12), C["rosa"])
    else:
        lz.relleno(capsula(x - 8, y + 36, x + 10, y + 37, 4.5), TINTA)
    if sudor > 0.01:
        gy = y - 40 + 24 * ((t * 1.7) % 1.0)
        lz.relleno(np.concatenate([[[x + 46, gy - 14 * sudor]], elipse(x + 46, gy + 2, 6 * sudor, 8 * sudor, 0, 16)]),
                   (190, 222, 230))


# ------------------------------------------------------------------ armas (origen en la mano, +x = a lo largo del antebrazo)
def _en(lz, x, y, ang, s=1.0):
    return lz.grupo(x, y, s, rot=ang)


def chancla(lz, x, y, ang=0.0, s=1.0):
    with _en(lz, x, y, ang, s):
        suela = elipse(30, 0, 50, 21, 0, 34)
        sombreado(lz, suela, C["rojo"], k=0.12)
        lz.relleno(elipse(32, -1, 40, 15, 0, 30), luz(C["rojo"], 0.22))
        lz.relleno(elipse(-6, 0, 16, 13, 0, 20), ton(C["rojo"], 0.25))
        lz.relleno(capsula(20, 0, 4, -13, 6.5), C["crema"])
        lz.relleno(capsula(20, 0, 4, 13, 6.5), C["crema"])
        lz.relleno(capsula(20, 0, 50, 0, 6.5), C["crema"])
        disco(lz, 52, 0, 4.8, ton(C["crema"], 0.15), sombra=False)


def sarten(lz, x, y, ang=0.0, s=1.0):
    with _en(lz, x, y, ang, s):
        cap(lz, -12, 0, 86, 0, 16, 12, (74, 62, 62), sombra=False)
        disco(lz, 136, 0, 58, (66, 64, 74))
        disco(lz, 136, 0, 46, (98, 98, 110), sombra=False)
        lz.relleno(elipse(120, -20, 16, 6, -0.7, 16), (200, 200, 210), alfa=0.6)
        disco(lz, 84, 0, 5, (200, 180, 120), sombra=False)


def pez_espada(lz, x, y, ang=0.0, s=1.0, boca=0.0):
    with _en(lz, x, y, ang, s):
        cuerpo = np.array([(-10, 0), (30, -24), (86, -26), (130, -12), (150, 0), (130, 12), (86, 22), (30, 20)], float)
        sombreado(lz, catmull(cuerpo, 8, True), C["azul"], k=0.12)
        lz.relleno(catmull(np.array([(40, 8), (86, 8), (126, 6), (86, 20), (40, 16)], float), 8, True), luz(C["azul"], 0.5))
        lz.relleno(np.array([(-10, 0), (-46, -30), (-30, 0), (-46, 30)], float), ton(C["azul"], 0.2))            # cola
        lz.relleno(np.array([(60, -24), (84, -52), (104, -22)], float), ton(C["azul"], 0.2))                       # aleta
        lz.relleno(np.array([(148, -5), (330, -1.5), (148, 5)], float), C["acero"])                               # espada
        lz.relleno(np.array([(148, -5), (330, -1.5), (300, -1)], float), luz(C["acero"], 0.5))
        disco(lz, 122, -5, 6.5, C["blanco"], sombra=False)
        disco(lz, 123.5, -5, 3, TINTA, sombra=False)


def extintor(lz, x, y, ang=0.0, s=1.0):
    with _en(lz, x, y, ang, s):
        cuerpo = rect_red(-6, -18, 92, 36, 14)
        sombreado(lz, cuerpo, (196, 84, 70), k=0.1)
        lz.relleno(rect_red(30, -19, 16, 38, 2), C["crema"])
        lz.relleno(rect_red(80, -9, 18, 18, 4), (62, 54, 60))
        lz.relleno(capsula(96, 0, 118, 8, 8), (62, 54, 60))
        lz.relleno(capsula(-4, -18, -20, -30, 8), (62, 54, 60))
        lz.relleno(capsula(-4, -18, -4, -29, 6), (62, 54, 60))


def tapa_olla(lz, x, y, ang=0.0, s=1.0):
    with _en(lz, x, y, ang, s):
        disco(lz, 20, 0, 92, C["acero"])
        disco(lz, 20, 0, 76, luz(C["acero"], 0.16), sombra=False)
        lz.relleno(elipse(-14, -40, 30, 9, -0.6, 16), (255, 255, 255), alfa=0.5)
        disco(lz, 22, 0, 16, (86, 78, 82))
        disco(lz, 22, 0, 8, (120, 112, 116), sombra=False)


# ------------------------------------------------------------------ criaturas (nativas mirando a la DERECHA; origen = suelo)
def _ojo_c(lz, x, y, r, mira=(2, 0), col=C["blanco"], ko=False, ceja=0.0):
    if ko:
        ojo_x(lz, x, y, r * 0.7)
        return
    disco(lz, x, y, r, col, sombra=False)
    disco(lz, x + mira[0], y + mira[1], r * 0.45, TINTA, sombra=False)
    if ceja:
        lz.relleno(capsula(x - r * 1.0, y - r * (1.05 + ceja * 0.35), x + r * 1.0, y - r * (1.05 - ceja * 0.35), r * 0.5),
                   TINTA)


def escorpion(lz, x, y, s=1.0, t=0.0, *, mirar=1, ph=0.0, paso=0.0, cola=0.0, pinza=0.0, ko=False, sq=1.0, ceja=0.5,
              rot=0.0, larga=1.0):
    """cola: 0 = enroscada sobre el cuerpo, 1 = picotazo hacia adelante. pinza: 0 cerrada, 1 abierta."""
    col = (186, 108, 76)
    with lz.grupo(x, y, s * mirar, rot=rot, sy=s * sq):
        # patas
        for i, px in enumerate((-58, -22, 14, 48)):
            for sg in (0, 1):
                a = math.sin(ph * 1.0 + i * 1.7 + sg * PI) * 14 * paso
                cap(lz, px, -38, px + 26 + a, 0 - max(0, math.sin(ph + i * 1.7 + sg * PI)) * 8 * paso, 13, 9,
                    ton(col, 0.25 if sg else 0.05), sombra=False)
        # cola
        base = (-84.0, -66.0)
        ang0 = math.radians(lerp(232, 292, cola))
        giro = lerp(0.56, 0.24, cola)
        pts = [base]
        ang = ang0
        for i in range(7):
            ang += giro
            pts.append((pts[-1][0] + math.cos(ang) * 40 * larga, pts[-1][1] + math.sin(ang) * 40 * larga))
        for i in range(len(pts) - 1, -1, -1):
            r = 24 - i * 1.7
            disco(lz, pts[i][0], pts[i][1], r, ton(col, 0.1 + 0.03 * (i % 2)))
        ex, ey = pts[-1]
        aa = ang + 0.2
        lz.relleno(np.array([(ex + math.cos(aa - 1.5) * 12, ey + math.sin(aa - 1.5) * 12),
                             (ex + math.cos(aa) * 42, ey + math.sin(aa) * 42),
                             (ex + math.cos(aa + 1.5) * 12, ey + math.sin(aa + 1.5) * 12)], float), C["mostaza"])
        # cuerpo
        cuerpo = elipse(0, -58, 100, 50, 0, 48)
        sombreado(lz, cuerpo, col, k=0.10)
        lz.relleno(elipse(-30, -72, 24, 8, 0.1, 16), luz(col, 0.3), alfa=0.8)
        lz.relleno(elipse(10, -80, 24, 7, 0.1, 16), luz(col, 0.3), alfa=0.8)
        # brazos con pinzas
        for k, (sy_, of) in enumerate(((-38, 0.0), (-48, 0.6))):
            cx0, cy0 = 78.0, sy_
            ex_, ey_ = 126.0 + 6 * math.sin(t * 4 + k), sy_ - 22 - 16 * pinza
            cap(lz, cx0, cy0, ex_, ey_, 18, 15, ton(col, 0.12 + 0.12 * k), sombra=False)
            for sg in (-1, 1):
                a = sg * (0.12 + 0.42 * pinza)
                lz.relleno(rot_pts(elipse(ex_ + 26, ey_, 30, 15, 0, 26), a, ex_, ey_), ton(col, 0.05 + 0.15 * k))
        # cara
        _ojo_c(lz, 74, -100, 13, (3, 1), ko=ko, ceja=ceja)
        _ojo_c(lz, 44, -106, 12, (3, 1), ko=ko, ceja=ceja)
        if ko:
            lz.relleno(capsula(62, -66, 84, -62, 5), TINTA)
        else:
            lz.relleno(capsula(60, -64, 86, -68 + 4 * pinza, 5), TINTA)


def trex(lz, x, y, s=1.0, t=0.0, *, mirar=1, ph=0.0, paso=0.0, boca=0.0, brazos=0.0, ko=False, sq=1.0, cabeza=0.0,
         ceja=0.6, estrellas=False, rot=0.0):
    """boca 0..1; brazos: 0 = quietos, >0 = agitándolos; cabeza: giro/inclinación del cuello (rad)."""
    verde = (112, 148, 112)
    vientre = (226, 208, 152)
    with lz.grupo(x, y, s * mirar, rot=rot, sy=s * sq):
        bob = abs(math.sin(ph)) * 8 * paso
        # cola
        cola = [(-90, -230 + bob), (-170, -216), (-250, -186 + 8 * math.sin(t * 2.4)), (-340, -150 + 12 * math.sin(t * 2.4 + 0.6)),
                (-410, -132 + 16 * math.sin(t * 2.4 + 1.2)), (-340, -140 + 12 * math.sin(t * 2.4 + 0.6)),
                (-250, -160 + 8 * math.sin(t * 2.4)), (-170, -140), (-90, -140 + bob)]
        sombreado(lz, catmull(np.array(cola, float), 8, True), verde, k=0.06)
        # patas (dos)
        for k, sg in enumerate((1, -1)):
            a = math.sin(ph + (0 if sg > 0 else PI)) * 0.55 * paso
            cx0 = 10 + sg * 20
            fx, fy = cx0 + math.sin(a) * 100, -max(0, math.cos(ph + (0 if sg > 0 else PI))) * 14 * paso
            col = ton(verde, 0.06 if sg > 0 else 0.2)
            elip(lz, cx0 - 4, -118 + bob, 52, 68, col, 0.3, sombra=False)
            cap(lz, cx0, -100 + bob, fx, fy - 12, 46, 34, col, sombra=False)
            lz.relleno(elipse(fx + 22, fy - 8, 40, 14, 0, 20), ton(col, 0.15))
            for g in (0, 1, 2):
                lz.relleno(np.array([(fx + 46 + g * 2 - g * 4, fy - 12 + g * 5), (fx + 62, fy - 8 + g * 5), (fx + 46, fy - 3 + g * 5)], float),
                           C["blanco"])
        # torso
        cuerpo = elipse(20, -204 + bob, 140, 100, -0.16, 48)
        sombreado(lz, cuerpo, verde, k=0.09)
        lz.relleno(elipse(60, -172 + bob, 92, 58, -0.16, 40), vientre)
        for i, (mx, my, mr) in enumerate(((-40, -270, 20), (0, -290, 16), (-84, -252, 14), (40, -298, 14))):
            disco(lz, mx, my + bob, mr, ton(verde, 0.28), sombra=False)
        # cuello + cabeza
        hx, hy = 150 + 24 * math.sin(cabeza), -310 + bob + 34 * math.sin(cabeza) * -0.5
        cap(lz, 96, -250 + bob, hx, hy, 92, 130, verde, sombra=False)
        with lz.grupo(hx, hy, 1.0, rot=cabeza * 0.6):
            # mandíbula inferior
            mand = elipse(38, 44 + 34 * boca, 100, 30, 0.12 * boca, 32)
            sombreado(lz, mand, ton(verde, 0.05), k=0.08)
            lz.relleno(elipse(46, 44 + 34 * boca + 2, 82, 15, 0.12 * boca, 24), (130, 60, 64) if boca > 0.15 else vientre)
            if boca > 0.15:
                lz.relleno(elipse(46, 26 + 12 * boca, 66, 12 + 16 * boca, 0, 24), (150, 70, 72))
                lz.relleno(elipse(60, 60 + 34 * boca - 4, 24, 9 + 4 * boca, 0, 16), C["rosa"], alfa=0.9)
            # cráneo/hocico
            cr = elipse(34, -4, 108, 62, 0.0, 44)
            sombreado(lz, cr, verde, k=0.09)
            # dientes
            for i in range(6):
                px = -8 + i * 22
                lz.relleno(np.array([(px, 30), (px + 15, 30), (px + 7, 30 + 13 + 7 * boca)], float), C["blanco"])
            for i in range(5):
                px = 4 + i * 22
                lz.relleno(np.array([(px, 44 + 34 * boca), (px + 15, 44 + 34 * boca), (px + 7, 44 + 34 * boca - 14)], float), C["blanco"])
            disco(lz, 128, -14, 7, ton(verde, 0.5), sombra=False)          # fosa nasal
            _ojo_c(lz, 40, -26, 15, (3, 1), ko=ko, ceja=ceja)
            if estrellas:
                for i in range(3):
                    a = t * 5 + i * 2.09
                    lz.relleno(estrella_pts(40 + 46 * math.cos(a), -84 + 12 * math.sin(a), 11, 5), C["mostaza"])
        # bracitos
        for k in range(2):
            ax, ay = 118 + k * 14, -226 + bob + k * 6
            w = brazos * 0.9
            a1 = 0.9 + 0.7 * math.sin(t * 17 + k * 2.0) * w
            a2 = 1.2 + 0.9 * math.sin(t * 17 + 1.5 + k * 2.0) * w
            p1 = (ax + math.cos(a1) * 24, ay + math.sin(a1) * 24)
            p2 = (p1[0] + math.cos(a2) * 22, p1[1] + math.sin(a2) * 22)
            cap(lz, ax, ay, p1[0], p1[1], 17, 14, ton(verde, 0.05 + 0.15 * k), sombra=False)
            cap(lz, p1[0], p1[1], p2[0], p2[1], 14, 10, ton(verde, 0.05 + 0.15 * k), sombra=False)
            for g in (-0.5, 0.5):
                lz.relleno(capsula(p2[0], p2[1], p2[0] + math.cos(a2 + g) * 14, p2[1] + math.sin(a2 + g) * 14, 5), C["blanco"])


def tiburon(lz, x, y, s=1.0, t=0.0, *, mirar=1, boca=0.0, ko=False, sq=1.0, ceja=0.6, rot=0.0):
    """Tiburón gigante, mirando a la derecha; origen = centro del cuerpo."""
    az = (112, 140, 158)
    with lz.grupo(x, y, s * mirar, rot=rot, sy=s * sq):
        # cola
        cola_y = 8 * math.sin(t * 9)
        lz.relleno(np.array([(-130, -6), (-230, -100 + cola_y), (-200, -8 + cola_y * 0.5), (-238, 84 + cola_y), (-130, 12)], float), ton(az, 0.18))
        # aleta dorsal
        lz.relleno(np.array([(-30, -78), (20, -170), (58, -74)], float), ton(az, 0.12))
        # cuerpo
        cuerpo = catmull(np.array([(-170, 0), (-100, -72), (10, -96), (120, -76), (196, -18), (200, 4), (120, 78), (0, 96), (-100, 60)], float), 8, True)
        sombreado(lz, cuerpo, az, k=0.09)
        vientre = catmull(np.array([(-100, 34), (10, 60), (120, 44), (190, 8), (120, 76), (10, 96), (-80, 66)], float), 8, True)
        lz.relleno(vientre, (226, 224, 214))
        # aleta pectoral
        lz.relleno(np.array([(10, 40), (-40, 130), (50, 66)], float), ton(az, 0.2))
        # boca
        my = 26 + 28 * boca
        if boca > 0.1:
            lz.relleno(np.array([(80, 18), (206, 6), (168, 24 + 46 * boca), (86, 40 + 30 * boca)], float), (130, 60, 66))
            for i in range(6):
                px = 96 + i * 17
                lz.relleno(np.array([(px, 18 - i * 2), (px + 12, 16 - i * 2), (px + 6, 32 + 8 * boca - i)], float), C["blanco"])
        else:
            lz.relleno(capsula(96, 22, 190, 16, 5.5), ton(az, 0.6))
        # branquias
        for i in range(3):
            lz.relleno(capsula(30 - i * 16, -10, 24 - i * 16, 22, 4.5), ton(az, 0.4))
        _ojo_c(lz, 128, -28, 13, (3, 1), ko=ko, ceja=ceja)


def platillo(lz, x, y, s=1.0, t=0.0, *, haz=0.0, alien="normal", rot=0.0, luces=1.0):
    """Platillo volador con un alienígena en la cúpula. haz 0..1 = rayo tractor hacia abajo. Origen = centro."""
    with lz.grupo(x, y, s, rot=rot):
        if haz > 0.01:
            for i, a in enumerate((0.34, 0.24)):
                lz.relleno(np.array([(-40, 20), (40, 20), (140 * (1 + i * 0.1), 540), (-140 * (1 + i * 0.1), 540)], float),
                           C["lava_c"] if i else LUZ, alfa=0.16 * haz)
        # cúpula + alien
        lz.relleno(circulo(0, -20, 62, 40), (196, 226, 226), alfa=0.85)
        cab = elipse(0, -34, 32, 38, 0, 32)
        sombreado(lz, cab, C["alien"], k=0.1)
        lz.relleno(elipse(-14, -34, 10, 15, 0.5, 16), (30, 30, 46))
        lz.relleno(elipse(14, -34, 10, 15, -0.5, 16), (30, 30, 46))
        if alien == "grito":
            lz.relleno(elipse(0, -8, 8, 11, 0, 16), (60, 30, 50))
        elif alien == "ko":
            lz.relleno(capsula(-8, -8, 8, -6, 4), (60, 30, 50))
        else:
            lz.relleno(capsula(-7, -10, 7, -10, 3.5), (60, 30, 50))
        lz.relleno(elipse(-22, -46, 12, 5, -0.5, 12), (255, 255, 255), alfa=0.45)
        # plato
        plato = elipse(0, 8, 150, 38, 0, 48)
        sombreado(lz, plato, C["lila"], k=0.10)
        lz.relleno(elipse(0, 2, 118, 22, 0, 40), luz(C["lila"], 0.28))
        for i in range(7):
            u = i / 6.0
            px = -108 + 216 * u
            on = 0.5 + 0.5 * math.sin(t * 8 * luces - i * 0.9)
            disco(lz, px, 14 + 9 * math.sin(u * PI) * 0.0 + 4 * math.sin(u * PI), 7.5, mezcla(C["mostaza"], C["blanco"], on), sombra=False)
        lz.relleno(elipse(0, 40, 60, 12, 0, 24), ton(C["lila"], 0.4))


def dragon(lz, x, y, s=1.0, t=0.0, *, mirar=1, boca=0.0, ko=False, alto=1.0, cab=0.0, ceja=0.7, cuello_ang=0.0, estrellas=False):
    """Dragón que asoma desde el suelo (origen en la base del cuello). alto 0..1 = cuánto se ha levantado."""
    rojo = (192, 96, 84)
    with lz.grupo(x, y, s * mirar, sy=s):
        # ala
        ala = [(30, -280 * alto), (-150, -520 * alto - 70 * math.sin(t * 5)), (-250, -300 * alto), (-190, -230 * alto),
               (-120, -160 * alto), (-60, -60 * alto)]
        lz.relleno(np.array(ala, float), ton(C["lila"], 0.05))
        for a in ala[1:4]:
            lz.relleno(capsula(30, -280 * alto, a[0], a[1], 9), ton(C["lila"], 0.35))
        # cuello (cadena de discos siguiendo una S)
        n = 14
        pts = []
        for i in range(n + 1):
            u = i / n
            px = 20 * math.sin(u * 3.2 + t * 1.6 + cuello_ang) * (0.4 + u) + 60 * u * u + cuello_ang * 60 * u
            py = -u * 420 * alto
            pts.append((px, py))
        Pn = np.array(pts, float)
        wd = np.array([78 - 26 * (i / n) for i in range(n + 1)])
        izq = np.stack([Pn[:, 0] - wd, Pn[:, 1]], 1)
        der = np.stack([Pn[:, 0] + wd, Pn[:, 1]], 1)
        cuello = np.concatenate([catmull(izq, 6), catmull(der[::-1], 6)])
        sombreado(lz, cuello, rojo, k=0.07, dirx=-1.0, diry=0.0)
        for i, (px, py) in enumerate(pts):
            u = i / n
            if i % 2 == 0 and i > 0:
                lz.relleno(np.array([(px - 60 * (1 - u * 0.4), py - 10), (px - 84 * (1 - u * 0.3), py - 30), (px - 56, py - 36)], float), C["mostaza"])
        # vientre (placas)
        for i, (px, py) in enumerate(pts[:-1]):
            u = i / n
            lz.relleno(elipse(px + 26, py, 24 - 8 * u, 12, 0, 12), C["mostaza"])
        hx, hy = pts[-1]
        with lz.grupo(hx + 10, hy - 6, 1.0, rot=cab):
            mand = elipse(56, 40 + 40 * boca, 108, 26, 0.16 * boca, 32)
            sombreado(lz, mand, ton(rojo, 0.1), k=0.08)
            if boca > 0.12:
                lz.relleno(elipse(56, 30 + 20 * boca, 88, 8 + 26 * boca, 0, 24), (250, 150, 90))
            cr = catmull(np.array([(-46, -34), (20, -74), (120, -56), (176, -16), (168, 22), (60, 34), (-40, 30)], float), 8, True)
            sombreado(lz, cr, rojo, k=0.09)
            for i in range(5):
                px = 70 + i * 22
                lz.relleno(np.array([(px, 24), (px + 12, 24), (px + 6, 38 + 8 * boca)], float), C["blanco"])
            # cuernos
            lz.relleno(np.array([(-14, -60), (-70, -132), (12, -80)], float), C["crema"])
            lz.relleno(np.array([(24, -68), (0, -150), (52, -76)], float), C["crema"])
            disco(lz, 158, -12, 8, ton(rojo, 0.5), sombra=False)
            disco(lz, 152, -34 if boca < 0.1 else -40, 0.1, rojo, sombra=False)
            _ojo_c(lz, 84, -34, 17, (3, 2), col=(250, 226, 150), ko=ko, ceja=ceja)
            if estrellas:
                for i in range(3):
                    a = t * 5 + i * 2.09
                    lz.relleno(estrella_pts(70 + 60 * math.cos(a), -110 + 14 * math.sin(a), 12, 5), C["mostaza"])
        return hx + 10, hy - 6


# ------------------------------------------------------------------ efectos
def estrellitas(lz, x, y, t, r=60.0, n=4, s=1.0, alfa=1.0):
    for i in range(n):
        a = t * 5.5 + i * 2 * PI / n
        px, py = x + r * math.cos(a), y + r * 0.32 * math.sin(a)
        lz.relleno(estrella_pts(px, py, 13 * s, 5.5 * s, 5, a), C["mostaza"], alfa=alfa)


def explosion(lz, x, y, u, r=130.0, col=None, seed=0):
    """Estallido de cómic: estrella puntiaguda que crece rápido y se desvanece (u = 0..1)."""
    if u <= 0 or u >= 1:
        return
    col = col or C["mostaza"]
    k = e_out(min(1, u * 2.4)) * (1 - 0.35 * prog(u, 0.5, 1.0))
    a = 1 - prog(u, 0.55, 1.0)
    n = 9
    P = []
    for i in range(2 * n):
        rr = r * k * (1.0 if i % 2 == 0 else 0.55 + 0.1 * h01(seed, i))
        rr *= 0.85 + 0.3 * h01(seed, i + 40)
        ang = i * PI / n + seed
        P.append((x + rr * math.cos(ang), y + rr * math.sin(ang)))
    lz.relleno(np.array(P), luz(col, 0.5), alfa=a)
    lz.relleno(np.array([(x + (px - x) * 0.62, y + (py - y) * 0.62) for px, py in P]), col, alfa=a)
    lz.relleno(circulo(x, y, r * 0.22 * k, 20), C["blanco"], alfa=a)


def ono(lz, texto, x, y, t, t0, dur=1.1, px=120, col=None, rot=-0.07, fuente="show"):
    """Onomatopeya de cómic: aparece con rebote, tiembla un poco, se desvanece."""
    u = t - t0
    if u < 0 or u > dur:
        return
    k = e_back(clamp01(u / 0.22))
    a = 1 - prog(u, dur - 0.25, dur)
    col = col or C["mostaza"]
    for dx_, dy_, cc in ((5, 6, ton(TINTA, 0.0)), (0, 0, col)):
        lz.texto(texto, x + dx_ + 2 * math.sin(u * 40), y + dy_, px, fuente, color=cc, borde=TINTA if cc == col else None,
                 borde_px=max(4, px * 0.09), k=k, rot=rot + 0.03 * math.sin(u * 30), alfa=a, temblor=0)


def polvo(lz, x, y, t, t0, n=6, r=46.0, dur=0.9, col=None, dir=(1.0, 0.0), alcance=90.0):
    u = t - t0
    if u < 0 or u > dur:
        return
    col = col or C["arena"]
    q = u / dur
    for i in range(n):
        ang = -PI * 0.5 + (i / max(1, n - 1) - 0.5) * 2.6 + 0.3 * h01(i, 3)
        d = alcance * e_out(q) * (0.6 + 0.6 * h01(i, 5))
        px = x + math.cos(ang) * d * (dir[0] if abs(dir[0]) > 0.01 else 1) + dir[0] * 20 * q
        py = y + math.sin(ang) * d * 0.5 - 20 * q
        disco(lz, px, py, r * (0.5 + 0.6 * e_out(q)) * (0.6 + 0.5 * h01(i, 7)), luz(col, 0.15), sombra=False, alfa=0.85 * (1 - q))


def spray(lz, x, y, ang, t, t0, t1, largo=380.0, col=None):
    """Nube de extintor: círculos que salen de (x,y) en la dirección ang y se ensanchan."""
    if t < t0 or t > t1 + 0.7:
        return
    col = col or C["blanco"]
    for i in range(26):
        u0 = t0 + (t1 - t0) * (i / 26.0)
        age = (t - u0)
        if age < 0 or age > 0.7:
            continue
        q = age / 0.7
        d = largo * e_out(q)
        px = x + math.cos(ang) * d + 26 * (h01(i, 1) - 0.5) * q * 3
        py = y + math.sin(ang) * d + 26 * (h01(i, 2) - 0.5) * q * 3
        disco(lz, px, py, 12 + 46 * q, col, sombra=False, alfa=0.85 * (1 - q * 0.9))


def fuego(lz, x, y, ang, t, largo=560.0, ancho=0.34, dens=1.0, seed=0):
    """Chorro de fuego (llamas circulares que se apagan a lo largo del chorro)."""
    if dens <= 0.01:
        return
    n = int(38 * dens) + 4
    for i in range(n):
        u = ((i / n) + t * 2.6 + h01(seed, i) * 0.5) % 1.0
        d = largo * e_out(u) * dens
        spread = ancho * d * (h01(seed, i + 9) - 0.5) * 2
        px = x + math.cos(ang) * d - math.sin(ang) * spread
        py = y + math.sin(ang) * d + math.cos(ang) * spread
        r = 18 + 58 * u
        c = mezcla(C["lava_c"], C["lava"], u * 1.4) if u < 0.72 else mezcla(C["lava"], C["ceniza"], (u - 0.72) / 0.28)
        disco(lz, px, py, r, c, sombra=False, alfa=(1 - u ** 3) * 0.95)


def salpicadura(lz, x, y, t, t0, n=9, alto=170.0, dur=1.0, col=None):
    u = t - t0
    if u < 0 or u > dur:
        return
    col = col or C["espuma"]
    for i in range(n):
        ang = -PI / 2 + (i / (n - 1) - 0.5) * 2.2
        v = 300 + 220 * h01(i, 4)
        px = x + math.cos(ang) * v * u * 0.6
        py = y + math.sin(ang) * v * u + 520 * u * u
        disco(lz, px, py, 12 * (1 - u * 0.5) * (0.6 + 0.6 * h01(i, 8)), col, sombra=False, alfa=1 - prog(u, 0.6, 1.0))


def brillo(lz, x, y, t, t0, r=60.0, dur=0.6):
    u = t - t0
    if u < 0 or u > dur:
        return
    q = u / dur
    k = math.sin(q * PI)
    lz.relleno(estrella_pts(x, y, r * k, r * 0.16 * k, 4, PI / 4), C["blanco"])
    lz.relleno(estrella_pts(x, y, r * 0.55 * k, r * 0.1 * k, 4, 0), luz(C["mostaza"], 0.4))


def lineas_vel(lz, x, y, ang, largo=240.0, n=5, t=0.0, alfa=0.5, col=None):
    col = col or C["blanco"]
    for i in range(n):
        o = (i - (n - 1) / 2) * 34
        ph = (t * 5 + i * 0.37) % 1.0
        d0 = largo * (0.2 + 0.8 * ph)
        px = x - math.sin(ang) * o
        py = y + math.cos(ang) * o
        lz.relleno(capsula(px - math.cos(ang) * d0, py - math.sin(ang) * d0, px - math.cos(ang) * (d0 + largo * 0.5),
                           py - math.sin(ang) * (d0 + largo * 0.5), 6), col, alfa=alfa * (1 - ph))


# ------------------------------------------------------------------ interfaz
def pastilla(lz, x, y, w, h, color, alfa=1.0):
    P = rect_red(x - w / 2, y - h / 2, w, h, h / 2)
    lz.relleno(P, ton(color, 0.3), alfa=alfa)
    lz.relleno(rect_red(x - w / 2, y - h / 2 - 3, w, h - 1, h / 2), color, alfa=alfa)


def barra(lz, x0, y, w, frac, nombre, color, lado=1, t=0.0, agita=0.0):
    """Barra de vida al estilo juego de pelea (lado=1 rellena de izquierda a derecha; -1 al revés)."""
    h = 34
    ox = agita * 6 * math.sin(t * 60)
    cx = x0 + w / 2 * lado + ox
    lz.relleno(rect_red(cx - w / 2 - 8, y - h / 2 - 8 + 5, w + 16, h + 16, 16), ton(C["marron_o"], 0.4))
    lz.relleno(rect_red(cx - w / 2 - 8, y - h / 2 - 8, w + 16, h + 16, 16), C["crema"])
    lz.relleno(rect_red(cx - w / 2, y - h / 2, w, h, 11), ton(C["marron"], 0.3), alfa=0.35)
    fw = max(0.0, w * clamp01(frac))
    if fw > 6:
        xx = cx - w / 2 if lado > 0 else cx + w / 2 - fw
        lz.relleno(rect_red(xx, y - h / 2, fw, h, 11), color)
        lz.relleno(rect_red(xx + 6, y - h / 2 + 4, max(1, fw - 12), 8, 4), luz(color, 0.4), alfa=0.8)
    tx = cx - w / 2 + 12 if lado > 0 else cx + w / 2 - 12
    lz.texto(nombre, tx, y + h / 2 + 30, 34, "vox_b", color=C["crema"], borde=ton(C["marron_o"], 0.3), borde_px=6,
             ancla=(0.0 if lado > 0 else 1.0, 0.5), temblor=0)


def rotulo(lz, texto, x, y, px, col, k=1.0, rot=0.0, fuente="vox_x", alfa=1.0, borde_col=None):
    if k <= 0.01:
        return
    bc = borde_col or TINTA
    lz.texto(texto, x + 6 * k, y + 8 * k, px, fuente, color=ton(bc, 0.0), borde=bc, borde_px=px * 0.16, k=k, rot=rot,
             alfa=alfa * 0.5, temblor=0)
    lz.texto(texto, x, y, px, fuente, color=col, borde=bc, borde_px=px * 0.11, k=k, rot=rot, alfa=alfa, temblor=0)


# ------------------------------------------------------------------ mundo: fondos
_XX, _YY = np.meshgrid(np.arange(W // 2, dtype=np.float32), np.arange(H // 2, dtype=np.float32))
_X1 = np.arange(W // 2, dtype=np.float32)


def _c(c):
    return np.array(c, np.float32) / 255.0


def _grad(top, bot, y0=0, y1=None, mid=None):
    y1 = y1 or H // 2
    u = np.clip((_YY[:, :1] - y0) / max(1, y1 - y0), 0, 1)
    if mid is None:
        col = _c(top) * (1 - u[..., None]) + _c(bot) * u[..., None]
    else:
        a = np.clip(u * 2, 0, 1)[..., None]
        b = np.clip(u * 2 - 1, 0, 1)[..., None]
        col = _c(top) * (1 - a) + _c(mid) * (a - b) + _c(bot) * b
    return np.broadcast_to(col, (H // 2, W // 2, 3)).copy()


def _capa(img, base_y, amp, frec, semilla, color, dx=0.0, nube=0.0, sup=None, alfa=1.0, agudo=0.0):
    """Silueta de colinas/dunas por suma de senos (coordenada de mundo = x + dx). Pinta de esa altura hacia abajo."""
    xw = _X1 + dx
    h = base_y - amp * (0.55 * np.sin(xw * frec + semilla * 7.3) + 0.3 * np.sin(xw * frec * 2.3 + semilla * 3.1 + 1.0)
                        + 0.15 * np.sin(xw * frec * 5.1 + semilla * 1.7))
    if agudo:
        h = h - agudo * np.abs(np.sin(xw * frec * 0.7 + semilla)) ** 3 * amp
    a = np.clip((_YY - h[None, :]) / 1.4 + 0.5, 0, 1)[..., None] * alfa
    col = _c(color)
    if sup is not None:                     # bruma: aclara hacia el horizonte
        col = col + (_c(sup) - col) * np.clip(1 - (_YY - h[None, :]) / 140.0, 0, 1)[..., None] * 0.35
    img[:] = img * (1 - a) + col * a
    return h


def _disco_bg(img, cx, cy, r, color, halo=0.0, alfa=1.0, cshalo=None):
    d = np.sqrt((_XX - cx) ** 2 + (_YY - cy) ** 2)
    if halo > 0:
        g = np.clip(1 - (d - r) / (r * 3.0), 0, 1) ** 2.4 * halo
        img[:] = img * (1 - g[..., None]) + _c(cshalo or color) * g[..., None]
    a = np.clip((r - d) / 1.3 + 0.5, 0, 1)[..., None] * alfa
    img[:] = img * (1 - a) + _c(color) * a


def _nubes(img, t, dx, y, n, col, alfa=0.85, vel=6.0, esc=1.0, sem=0):
    for i in range(n):
        cx = ((i * 197.0 + 130 * h01(sem, i) + t * vel - dx * 0.06) % (W // 2 + 240)) - 120
        cy = y + 34 * h01(sem, i + 5)
        r = (20 + 16 * h01(sem, i + 9)) * esc
        for ox, oy, rr in ((0, 0, r), (r * 1.1, r * 0.2, r * 0.8), (-r * 1.05, r * 0.25, r * 0.7), (r * 0.3, -r * 0.35, r * 0.75)):
            _disco_bg(img, cx + ox, cy + oy, rr, col, alfa=alfa)
        # base plana
        y0 = int(cy + r * 0.55)
        x0, x1 = int(max(0, cx - r * 1.6)), int(min(W // 2, cx + r * 1.8))
        if x1 > x0 and 0 <= y0 < H // 2 - 1:
            img[y0:y0 + 1, x0:x1] = img[y0:y0 + 1, x0:x1] * (1 - alfa * 0.0) + 0.0


def _estrellas_bg(img, dx, t, n=90, sem=3):
    for i in range(n):
        px = (h01(sem, i) * (W // 2 + 200) - dx * (0.03 + 0.05 * h01(sem, i + 60))) % (W // 2)
        py = h01(sem, i + 30) * (H // 2 - 100)
        b = 0.55 + 0.45 * math.sin(t * (1.2 + 2 * h01(sem, i + 8)) + i)
        x0, y0 = int(px), int(py)
        r = 1 + int(h01(sem, i + 3) * 1.5)
        img[max(0, y0 - r + 1):y0 + r, max(0, x0 - r + 1):x0 + r] = _c(C["blanco"]) * b + img[y0, x0] * (1 - b)


def _bioma_desierto(t, dx):
    img = _grad((216, 200, 166), (246, 226, 190), 0, 210)
    _disco_bg(img, 690 - dx * 0.02, 96, 40, (252, 240, 208), halo=0.5, cshalo=(255, 232, 190))
    _nubes(img, t, dx, 70, 3, (250, 240, 216), 0.55, 4.0, 1.2, 1)
    _capa(img, 262, 40, 0.0035, 1, (212, 168, 140), dx * 0.05, sup=(246, 226, 190), agudo=0.5)       # mesas
    _capa(img, 292, 30, 0.0048, 2, (222, 180, 134), dx * 0.12, sup=(246, 226, 190))
    _capa(img, 334, 20, 0.0062, 3, (226, 190, 140), dx * 0.3)
    img[345:] = img[345:] * 0.0 + _c((226, 196, 148))
    yy = np.clip((_YY[345:] - 345) / 195.0, 0, 1)[..., None]
    img[345:] = _c((228, 200, 152)) * (1 - yy) + _c((206, 168, 120)) * yy
    return img


def _bioma_selva(t, dx):
    img = _grad((186, 208, 188), (226, 232, 206), 0, 230)
    _disco_bg(img, 250 - dx * 0.02, 90, 54, (240, 240, 214), halo=0.35, cshalo=(240, 240, 214))
    _nubes(img, t, dx, 60, 3, (238, 240, 224), 0.5, 3.0, 1.1, 2)
    _capa(img, 250, 46, 0.0042, 4, (138, 172, 150), dx * 0.05, sup=(226, 232, 206))
    _capa(img, 288, 40, 0.0055, 5, (98, 142, 112), dx * 0.14, sup=(226, 232, 206))
    # copas de árboles lejanas
    for i in range(14):
        cx = ((i * 92.0 - dx * 0.24) % (W // 2 + 200)) - 60
        _disco_bg(img, cx, 290 + 18 * h01(6, i), 44 + 16 * h01(6, i + 3), (76, 120, 90), alfa=0.95)
    _capa(img, 330, 20, 0.007, 6, (72, 112, 82), dx * 0.34)
    yy = np.clip((_YY[350:] - 350) / 190.0, 0, 1)[..., None]
    img[350:] = _c((88, 118, 78)) * (1 - yy) + _c((58, 84, 62)) * yy
    return img


def _bioma_oceano(t, dx):
    img = _grad((222, 230, 222), (232, 232, 214), 0, 240)
    _disco_bg(img, 470 - dx * 0.02, 130, 34, (250, 240, 208), halo=0.6, cshalo=(252, 226, 176))
    _nubes(img, t, dx, 60, 4, (248, 246, 232), 0.7, 5.0, 1.15, 3)
    # isla lejana con palmera (guiño a la referencia)
    ix = 760 - dx * 0.10
    _capa_isla = np.clip((_YY - (250 - 26 * np.exp(-((_XX - ix) / 60.0) ** 2))) / 1.4 + 0.5, 0, 1)[..., None]
    img[:] = img * (1 - _capa_isla) + _c((118, 150, 132)) * _capa_isla
    yy = np.clip((_YY - 250) / 290.0, 0, 1)[..., None]
    mar = _c((146, 190, 184)) * (1 - yy) + _c((78, 124, 130)) * yy
    m = np.clip((_YY - 250) / 1.4 + 0.5, 0, 1)[..., None]
    img[:] = img * (1 - m) + mar * m
    # oleaje: bandas claras que ondulan
    for k in range(9):
        by = 262 + k * k * 3.6 + 12 * k
        amp = 3 + 1.5 * k
        h = by + amp * np.sin((_X1 + dx * (0.2 + 0.05 * k)) * (0.03 - 0.002 * k) + t * (0.8 + 0.1 * k) + k * 2)
        a = np.clip(1 - np.abs(_YY - h[None, :]) / (1.6 + 0.4 * k), 0, 1)[..., None] * 0.34
        img[:] = img * (1 - a) + _c((238, 244, 232)) * a
    return img


def _bioma_luna(t, dx):
    img = _grad((36, 40, 70), (82, 78, 112), 0, 300)
    _estrellas_bg(img, dx, t)
    _disco_bg(img, 660 - dx * 0.03, 116, 50, (110, 156, 194), halo=0.35, cshalo=(120, 160, 200))
    # Tierra: manchas verdes y nubes
    d = np.sqrt((_XX - (660 - dx * 0.03)) ** 2 + (_YY - 116) ** 2)
    for ox, oy, rr, cc in ((-16, -8, 17, (110, 156, 112)), (12, 16, 15, (110, 156, 112)), (10, -20, 12, (236, 240, 240))):
        dd = np.sqrt((_XX - (660 - dx * 0.03 + ox)) ** 2 + (_YY - (116 + oy)) ** 2)
        m = (np.clip((rr - dd) / 1.3 + 0.5, 0, 1) * np.clip((49 - d) / 1.3 + 0.5, 0, 1))[..., None]
        img[:] = img * (1 - m) + _c(cc) * m
    m = (np.clip((d - 20) / 30, 0, 1) * np.clip((52 - d) / 1.3 + 0.5, 0, 1) * (((_XX - 660 + dx * 0.03) > 6) * 0.35))[..., None]
    img[:] = img * (1 - m) + _c((40, 44, 84)) * m
    _capa(img, 268, 34, 0.004, 7, (116, 108, 138), dx * 0.05, agudo=0.6)
    _capa(img, 312, 22, 0.0055, 8, (150, 146, 164), dx * 0.14)
    yy = np.clip((_YY[338:] - 338) / 200.0, 0, 1)[..., None]
    img[338:] = _c((188, 184, 192)) * (1 - yy) + _c((146, 142, 156)) * yy
    for i in range(8):        # cráteres
        cx = ((i * 143.0 + 60 - dx * 0.5) % (W // 2 + 300)) - 100
        cy = 380 + 24 * h01(9, i) + 16 * (i % 3)
        rx = 44 + 26 * h01(9, i + 4)
        d2 = ((_XX - cx) / rx) ** 2 + ((_YY - cy) / (rx * 0.26)) ** 2
        m = np.clip((1 - d2) * 6, 0, 1)[..., None]
        img[:] = img * (1 - m * 0.45) + _c((122, 118, 136)) * m * 0.45
        m2 = np.clip((1 - ((_XX - cx - 5) / (rx * 0.9)) ** 2 - ((_YY - cy - 3) / (rx * 0.2)) ** 2) * 6, 0, 1)[..., None]
        img[:] = img * (1 - m2 * 0.5) + _c((160, 156, 170)) * m2 * 0.5
    return img


def _bioma_volcan(t, dx):
    img = _grad((112, 62, 66), (238, 152, 96), 0, 300, mid=(190, 96, 80))
    _nubes(img, t, dx, 60, 3, (150, 96, 96), 0.55, 4.0, 1.5, 4)
    # volcán central con lava
    vx = 500 - dx * 0.10
    alt = 250 - 150 * np.exp(-np.abs((_X1 - vx) / 190.0) ** 1.25)
    m = np.clip((_YY - alt[None, :]) / 1.4 + 0.5, 0, 1)[..., None]
    img[:] = img * (1 - m) + _c((92, 64, 74)) * m
    glow = np.clip(1 - np.sqrt((_XX - vx) ** 2 + ((_YY - 110) * 1.3) ** 2) / 120.0, 0, 1)[..., None] ** 2 * 0.65
    img[:] = img * (1 - glow) + _c(C["lava_c"]) * glow
    for k in range(3):        # ríos de lava por la ladera
        lx = vx + (k - 1) * 22 + 10 * np.sin(_YY[:, 0] * 0.06 + k * 2 + t * 0.5)
        yy_ = _YY[:, 0]
        w = 4 + 2 * (yy_ - 110) / 80
        a = np.clip(1 - np.abs(_XX - lx[:, None]) / w[:, None], 0, 1) * ((_YY > 112 + 6 * k) * (_YY < 290))
        img[:] = img * (1 - a[..., None] * 0.9) + _c(C["lava"]) * a[..., None] * 0.9
    _capa(img, 300, 26, 0.0055, 10, (96, 68, 78), dx * 0.16, sup=(238, 152, 96))
    _capa(img, 336, 18, 0.008, 11, (74, 54, 64), dx * 0.32)
    yy = np.clip((_YY[350:] - 350) / 190.0, 0, 1)[..., None]
    img[350:] = _c((84, 62, 70)) * (1 - yy) + _c((58, 44, 54)) * yy
    # grietas de lava en el suelo
    for i in range(5):
        cx = ((i * 220.0 - dx * 0.5 + 40) % (W // 2 + 300)) - 100
        cy = 410 + 30 * (i % 3)
        d2 = np.abs((_XX - cx) / 90.0) ** 2 + np.abs((_YY - cy - 6 * np.sin(_XX * 0.05 + i)) / 3.5) ** 2
        a = np.clip(1.2 - d2, 0, 1)[..., None] * (0.75 + 0.25 * math.sin(t * 3 + i))
        img[:] = img * (1 - a) + _c(C["lava"]) * a
    return img


_BIOMAS = [_bioma_desierto, _bioma_selva, _bioma_oceano, _bioma_luna, _bioma_volcan]
NOMBRES_BIOMA = ["desierto", "selva", "oceano", "luna", "volcan"]


def bioma_img(k, X0, t):
    k = int(np.clip(k, 0, len(_BIOMAS) - 1))
    img = _BIOMAS[k](t, X0 - BIOMA_W * k)
    img = cv2.GaussianBlur(img, (0, 0), 0.9)
    return cv2.resize(img, (W, H), interpolation=cv2.INTER_CUBIC)


def fondo_mundo(X0, t):
    """Fondo continuo: mezcla el bioma actual con el siguiente a lo largo de un borde de pincel que se desplaza."""
    k = int(math.floor(X0 / BIOMA_W + 1e-6))
    k = max(0, min(k, len(_BIOMAS) - 1))
    A = bioma_img(k, X0, t)
    bx = BIOMA_W * (k + 1) - X0                 # posición en pantalla del borde con el siguiente bioma
    if k + 1 >= len(_BIOMAS) or bx >= W + 120:
        return A
    B = bioma_img(k + 1, X0, t)
    ys = np.arange(H, dtype=np.float32)
    env = min(1.0, max(0.0, (W - bx) / 300.0))            # el borde solo ondula mientras se desplaza
    borde = bx + 40 + env * (46 * np.sin(ys * 0.011 + 1.0) + 24 * np.sin(ys * 0.031) + 12 * np.sin(ys * 0.09 + 2.0))
    return _mezcla_borde(A, B, borde)


def _mezcla_borde(A, B, borde):
    xs = np.arange(W, dtype=np.float32)[None, :]
    m = np.clip((borde[:, None] - xs) / 70.0 + 0.5, 0, 1)      # 1 a la izquierda del borde (bioma A)
    m = (m * m * (3 - 2 * m))[..., None]
    return A * m + B * (1 - m)
