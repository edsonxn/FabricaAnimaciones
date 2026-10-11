# -*- coding: utf-8 -*-
"""Figuras planas animadas (estilo Kurzgesagt) para el documental del tesoro de Moctezuma.
Todas: origen en los pies / la base, coordenadas locales en px (persona ~ 118 de alto), `lado` = +1 mira a la derecha, -1 a la izquierda.
soldado, guerrero, tlatoani, caballo, canoa, bergantin, barra_oro, disco, cofre, saco, joya, pluma, jade, moneda, templo_mayor, palacio, brasero."""
import math

import numpy as np

from motor import circulo, elipse, rect_red, blob, catmull, h01, prog, lerp, smooth, e_out, e_back, e_inout
import plano as P

ACERO = (172, 180, 200)
ACERO_S = (112, 120, 150)
ORO = (255, 206, 72)
ORO_S = (214, 150, 40)
ORO_L = (255, 238, 150)
PIELES = [(240, 184, 140), (212, 146, 102), (168, 108, 74), (132, 84, 60)]
PIEL_MEX = (176, 116, 80)


def cap(lz, x0, y0, ang, L, w, col):
    """Cápsula desde (x0,y0) con ángulo ang (0 = hacia abajo, + = hacia +x) y largo L. Devuelve el otro extremo."""
    x1, y1 = x0 + L * math.sin(ang), y0 + L * math.cos(ang)
    dx, dy = math.cos(ang) * w / 2, -math.sin(ang) * w / 2
    lz.relleno(np.array([[x0 - dx, y0 - dy], [x0 + dx, y0 + dy], [x1 + dx, y1 + dy], [x1 - dx, y1 - dy]]), col)
    lz.relleno(circulo(x1, y1, w / 2, 10), col)
    return x1, y1


def _ph(t, paso, seed):
    return t * paso * 6.0 + h01(seed) * 6.28


# ======================================================================== soldado español
def soldado(lz, x, y, s=1.0, t=0.0, paso=0.0, lado=1, carga=0.0, arma=None, seed=0, tunica=(206, 70, 62), brazos=None, inc=0.0):
    """Soldado con coraza y morrión. carga 0..1.5: saco de oro a la espalda (se encorva y pesa). arma: None|'espada'|'lanza'.
    brazos: None (andar) o (ang_izq, ang_der) fijos. inc: inclinación extra del tronco (rad)."""
    ph = _ph(t, paso, seed)
    sw = math.sin(ph) * (0.55 - 0.15 * min(carga, 1.0)) if paso > 0 else 0.0
    bob = abs(math.sin(ph)) * 3 if paso > 0 else 0.0
    lean = 0.16 * min(carga, 1.5) + inc
    pant = (74, 62, 84)
    with lz.grupo(x, y - bob * s, s * lado, 0.0, s):
        cap(lz, -5, -44, -sw, 44, 11, P.oscurecer(pant, 0.25))
        cap(lz, 5, -44, sw, 44, 11, pant)
        lz.relleno(elipse(-5 - 44 * math.sin(-sw) * 0 + 0, 0, 0.1, 0.1, 0, 4), pant)
        with lz.grupo(0, -44, 1.0, lean):
            if carga > 0.02:      # saco a la espalda
                r = 15 + 12 * carga
                lz.relleno(blob(-16 - r * 0.35, -24, r, 3, 0.10, 24, 4), ORO_S)
                lz.relleno(blob(-16 - r * 0.35 - 3, -27, r * 0.82, 3, 0.10, 24, 4), ORO)
                lz.relleno(circulo(-16 - r * 0.6, -32, r * 0.16, 8), ORO_L)
            lz.relleno(rect_red(-13, -44, 26, 46, 9), tunica)
            lz.relleno(rect_red(-13, -44, 26, 34, 8), ACERO)
            lz.relleno(np.array([[-13, -20], [13, -20], [13, -10], [-13, -10]]), ACERO_S)
            lz.relleno(rect_red(-4, -42, 5, 28, 2), (216, 224, 240))
            lz.relleno(rect_red(-13, -12, 26, 5, 2), (110, 76, 54))
            if brazos is None:
                a1, a2 = -0.25 - sw, 0.25 + sw
            else:
                a1, a2 = brazos
            xa, ya = cap(lz, -13, -38, a1, 30, 10, P.oscurecer(tunica, 0.2))
            xb, yb = cap(lz, 13, -38, a2, 30, 10, tunica)
            lz.relleno(circulo(xa, ya + 3, 5, 10), PIELES[0])
            lz.relleno(circulo(xb, yb + 3, 5, 10), PIELES[0])
            if arma == "espada":
                cap(lz, xb, yb, 2.55, 36, 4, (226, 232, 246))
                lz.relleno(rect_red(xb - 6, yb - 2, 12, 4, 1), ORO_S)
            elif arma == "lanza":
                cap(lz, xb, yb + 6, 3.14 + 0.05, 90, 4, (120, 88, 60))
                cap(lz, xb, yb + 6, 0.0 + 0.05, 62, 4, (120, 88, 60))
                lz.relleno(np.array([[xb + 2, yb - 56], [xb + 7, yb - 74], [xb + 12, yb - 56]]), (226, 232, 246))
            # cabeza
            lz.relleno(rect_red(-4, -52, 8, 10, 3), PIELES[0])
            lz.relleno(circulo(0, -60, 12.5, 22), PIELES[0])
            lz.relleno(np.array([[2, -56], [12, -60], [9, -50], [1, -50]]), (66, 46, 40))          # barba
            lz.relleno(circulo(5, -62, 1.8, 8), (40, 28, 40))
            # morrión
            lz.relleno(np.array([[-14, -63], [-11, -76], [0, -84], [11, -76], [14, -63], [8, -66], [-8, -66]]), ACERO)
            lz.relleno(np.array([[-6, -78], [0, -84], [6, -78], [0, -70]]), (216, 224, 240), alfa=0.8)
            lz.relleno(np.array([[-22, -64], [-14, -68], [14, -68], [24, -64], [14, -61], [-14, -61]]), ACERO_S)
            lz.relleno(rect_red(-13, -66, 26, 3, 1), ORO)


# ======================================================================== guerrero mexica
def guerrero(lz, x, y, s=1.0, t=0.0, paso=0.0, lado=1, arma="lanza", escudo=True, seed=0, plumas=0, brazos=None, pintura=0):
    """Guerrero mexica con tocado de plumas (plumas=0..2), escudo redondo y lanza / macuahuitl."""
    ph = _ph(t, paso, seed)
    sw = math.sin(ph) * 0.6 if paso > 0 else 0.0
    bob = abs(math.sin(ph)) * 3 if paso > 0 else 0.0
    piel = PIEL_MEX
    paleta = [((60, 200, 130), (255, 210, 80), (230, 80, 90), (90, 160, 240), (60, 200, 130)),
              ((255, 140, 70), (255, 220, 100), (230, 70, 80), (255, 140, 70), (255, 220, 100)),
              ((90, 200, 220), (60, 160, 240), (250, 250, 250), (90, 200, 220), (60, 160, 240))][plumas % 3]
    with lz.grupo(x, y - bob * s, s * lado, 0.0, s):
        cap(lz, -5, -44, -sw, 44, 11, P.oscurecer(piel, 0.3))
        cap(lz, 5, -44, sw, 44, 11, piel)
        lz.relleno(rect_red(-13, -46, 26, 6, 2), (255, 255, 255))           # máxtlatl
        lz.relleno(rect_red(-13, -46, 26, 3, 1), (222, 70, 78))
        lz.relleno(np.array([[-9, -46], [9, -46], [6, -28], [-6, -28]]), (250, 244, 232))
        lz.relleno(rect_red(-13, -90, 26, 46, 9), piel)
        if pintura:
            lz.relleno(rect_red(-13, -74, 26, 6, 1), (230, 76, 80))
            lz.relleno(rect_red(-13, -64, 26, 4, 1), (250, 240, 220))
        if brazos is None:
            a1, a2 = -0.2 - sw, 0.3 + sw
        else:
            a1, a2 = brazos
        xa, ya = cap(lz, -13, -84, a1, 30, 10, P.oscurecer(piel, 0.15))
        xb, yb = cap(lz, 13, -84, a2, 30, 10, piel)
        if escudo:
            cx_, cy_ = xa - 3, ya - 4
            lz.relleno(circulo(cx_, cy_, 21, 26), (200, 64, 60))
            lz.relleno(circulo(cx_, cy_, 15, 24), (252, 226, 150))
            lz.relleno(circulo(cx_, cy_, 8, 20), (60, 170, 190))
            lz.relleno(circulo(cx_, cy_, 3.5, 12), (255, 255, 255))
            for k in range(10):
                a = k / 10 * 6.283
                lz.relleno(elipse(cx_ + math.cos(a) * 23, cy_ + math.sin(a) * 23, 4, 9, a + 1.57, 8), paleta[k % 5])
        if arma == "lanza":
            cap(lz, xb, yb + 4, 3.14 + 0.05, 96, 4, (140, 100, 66))
            cap(lz, xb, yb + 4, 0.0, 60, 4, (140, 100, 66))
            lz.relleno(np.array([[xb, yb - 56], [xb + 5, yb - 78], [xb + 10, yb - 56]]), (60, 60, 76))
        elif arma == "macuahuitl":
            cap(lz, xb, yb + 4, 3.0, 50, 9, (150, 100, 60))
            for k in range(5):
                lz.relleno(np.array([[xb - 6, yb - 8 - k * 9], [xb - 13, yb - 12 - k * 9], [xb - 6, yb - 15 - k * 9]]), (40, 40, 56))
        lz.relleno(rect_red(-4, -100, 8, 10, 3), piel)
        lz.relleno(circulo(0, -108, 12.5, 22), piel)
        lz.relleno(circulo(5, -110, 1.8, 8), (40, 28, 40))
        lz.relleno(np.array([[-13, -110], [0, -128], [13, -110], [11, -116], [0, -120], [-11, -116]]), (40, 30, 50))
        for i, c in enumerate(paleta):
            a = -1.0 + i * 0.5
            lz.relleno(elipse(math.sin(a) * 22 - 4, -122 - math.cos(a) * 22, 6.5, 20, -a, 12), c)
        lz.relleno(rect_red(-13, -122, 26, 6, 2), ORO)


# ======================================================================== tlatoani (Moctezuma)
def tlatoani(lz, x, y, s=1.0, t=0.0, lado=1, brazos=0.0, paso=0.0, seed=0, manto=(70, 190, 200)):
    """Emperador: tilma turquesa hasta las rodillas, collar de oro, diadema triangular de turquesa (xiuhuitzolli)."""
    ph = _ph(t, paso, seed)
    sw = math.sin(ph) * 0.4 if paso > 0 else 0.0
    bob = abs(math.sin(ph)) * 2 if paso > 0 else 0.0
    piel = PIEL_MEX
    with lz.grupo(x, y - bob * s, s * lado, 0.0, s):
        cap(lz, -5, -42, -sw, 42, 10, P.oscurecer(piel, 0.3))
        cap(lz, 5, -42, sw, 42, 10, piel)
        lz.relleno(rect_red(-8, -12, 16, 12, 2), (255, 214, 90))              # sandalias/tiras
        lz.relleno(np.array([[-16, -92], [16, -92], [22, -40], [-22, -40]]), (250, 246, 240))
        lz.relleno(np.array([[-16, -92], [16, -92], [12, -76], [-12, -76]]), manto)
        lz.relleno(np.array([[-22, -40], [22, -40], [22, -46], [-22, -46]]), (222, 70, 78))
        a1 = -0.2 - sw - brazos * 2.4
        a2 = 0.2 + sw + brazos * 2.4
        cap(lz, -15, -86, a1, 30, 9, P.oscurecer(piel, 0.15))
        cap(lz, 15, -86, a2, 30, 9, piel)
        lz.relleno(rect_red(-6, -100, 12, 12, 4), ORO)                             # collar
        lz.relleno(rect_red(-4, -104, 8, 10, 3), piel)
        lz.relleno(circulo(0, -112, 13, 22), piel)
        lz.relleno(circulo(5, -114, 1.8, 8), (40, 28, 40))
        lz.relleno(np.array([[-14, -114], [0, -130], [14, -114], [12, -118], [0, -122], [-12, -118]]), (40, 30, 50))
        lz.relleno(np.array([[-13, -122], [0, -156], [13, -122]]), (60, 200, 200))       # diadema
        lz.relleno(np.array([[-6, -124], [0, -148], [6, -124]]), (140, 236, 226))
        lz.relleno(rect_red(-14, -124, 28, 5, 2), ORO)


# ======================================================================== caballo
def caballo(lz, x, y, s=1.0, t=0.0, paso=0.0, lado=1, carga=0, col=(150, 98, 68), seed=0, cabeza=0.0):
    """Caballo de perfil (origen entre los cascos). carga: 0 nada, 1 arcones con oro. paso: velocidad del trote/galope."""
    ph = _ph(t, paso, seed)
    bob = abs(math.sin(ph)) * 4 if paso > 0 else 0.0
    osc = math.sin(ph * 2) * 0.03 if paso > 0 else 0.0
    oscuro = P.oscurecer(col, 0.28)
    claro = P.aclarar(col, 0.12)
    crin = (58, 40, 40)
    with lz.grupo(x, y - bob * s, s * lado, osc, s):
        # patas traseras / delanteras (trote diagonal)
        for (hx, fase, tono) in ((-38, 0.0, oscuro), (36, math.pi, oscuro), (-30, math.pi, col), (44, 0.0, col)):
            a = math.sin(ph + fase) * 0.62 if paso > 0 else 0.0
            b = -abs(math.sin(ph + fase + 0.9)) * 0.7 if paso > 0 else 0.0
            kx, ky = cap(lz, hx, -60, a * 0.8, 34, 14, tono)
            fx, fy = cap(lz, kx, ky, a * 0.5 + b + (0.15 if hx < 0 else -0.05), 34, 10, tono)
            lz.relleno(rect_red(fx - 6, fy - 2, 13, 9, 3), (52, 40, 44))
        lz.relleno(catmull([(-58, -90), (-30, -102), (20, -100), (50, -96), (62, -78), (52, -56), (20, -50), (-20, -50), (-52, -58), (-66, -76)], 8, True), col)
        lz.relleno(catmull([(-46, -66), (-10, -58), (30, -60), (48, -66), (34, -52), (-10, -48), (-46, -56)], 8, True), claro, alfa=0.55)
        lz.relleno(catmull([(-62, -94), (-40, -104), (-38, -84), (-64, -80)], 8, True), P.aclarar(col, 0.08))
        # cuello y cabeza
        cb = math.sin(ph * 2) * 4 * cabeza if paso > 0 else 0
        lz.relleno(np.array([[38, -98], [58, -136 + cb], [80, -142 + cb], [84, -120 + cb], [62, -92]]), col)
        lz.relleno(np.array([[74, -144 + cb], [104, -120 + cb], [112, -108 + cb], [104, -101 + cb], [90, -110 + cb], [72, -124 + cb]]), claro)
        lz.relleno(np.array([[76, -144 + cb], [82, -158 + cb], [88, -142 + cb]]), oscuro)
        lz.relleno(circulo(88, -126 + cb, 2.4, 8), (30, 24, 36))
        lz.relleno(circulo(108, -108 + cb, 1.8, 6), (60, 40, 44))
        for k in range(6):          # crin
            px, py = 44 + k * 7, -102 - k * 6
            lz.relleno(np.array([[px, py + cb * k / 6], [px - 12, py - 4 + cb * k / 6], [px - 6, py + 14]]), crin)
        # cola
        w = math.sin(ph * 1.3) * 8 if paso > 0 else 0
        lz.relleno(catmull([(-62, -88), (-84, -84 + w), (-96, -60 + w * 1.5), (-90, -34 + w), (-80, -56), (-72, -78)], 8, True), crin)
        # silla / carga
        lz.relleno(rect_red(-16, -106, 48, 12, 4), (196, 70, 70))
        if carga:
            for (cx, cy) in ((-24, -92), (12, -92)):
                lz.relleno(rect_red(cx - 2, cy - 10, 26, 28, 4), (140, 92, 58))
                lz.relleno(rect_red(cx, cy - 8, 22, 6, 2), (172, 122, 78))
                lz.relleno(np.array([[cx + 2, cy - 12], [cx + 22, cy - 12], [cx + 18, cy - 20], [cx + 6, cy - 20]]), ORO)
                lz.relleno(circulo(cx + 10, cy - 15, 3, 8), ORO_L)


# ======================================================================== canoa y bergantín
def canoa(lz, x, y, s=1.0, t=0.0, lado=1, guerreros=2, remo=1.0, seed=0, plumas=0):
    """Canoa mexica con remeros/guerreros (origen en la línea de flotación, centro)."""
    ph = t * 3.2 * remo + h01(seed) * 6.28
    bob = math.sin(ph * 0.7) * 3
    with lz.grupo(x, y + bob * s, s * lado, math.sin(ph * 0.5) * 0.03, s):
        for k in range(guerreros):
            bx = -34 + k * 60
            g = math.sin(ph + k * 1.6)
            piel = PIEL_MEX
            lz.relleno(rect_red(bx - 10, -66, 20, 40, 8), piel)
            lz.relleno(circulo(bx, -78, 11, 18), piel)
            for i, c in enumerate(((60, 200, 130), (255, 210, 80), (230, 80, 90), (60, 200, 130))):
                a = -0.8 + i * 0.5
                lz.relleno(elipse(bx + math.sin(a) * 16, -90 - math.cos(a) * 14, 5, 14, -a, 10), c)
            xb, yb = cap(lz, bx + 8, -58, -0.5 + g * 0.5, 34, 8, piel)
            lz.relleno(np.array([[xb - 1, yb], [xb + 22 + g * 8, yb + 26], [xb + 30 + g * 8, yb + 22], [xb + 6, yb - 6]]), (150, 100, 60))
            cap(lz, bx - 6, -60, 0.2 - g * 0.3, 30, 8, P.oscurecer(piel, 0.15))
        lz.relleno(catmull([(-92, -22), (-60, -8), (0, 0), (60, -8), (96, -30), (84, -18), (60, -2), (0, 8), (-60, 2)], 8, True), (140, 88, 58))
        lz.relleno(np.array([[-92, -22], [96, -30], [92, -24], [-88, -16]]), (196, 138, 88))
        lz.relleno(np.array([[-88, -14], [90, -22], [70, -2], [-60, 4]]), (110, 68, 50), alfa=0.6)


def bergantin(lz, x, y, s=1.0, t=0.0, lado=1, seed=0, vela=1.0):
    """Bergantín español de vela cuadrada (origen en la línea de flotación)."""
    ph = t * 1.6 + h01(seed) * 6.28
    bob = math.sin(ph) * 3
    with lz.grupo(x, y + bob * s, s * lado, math.sin(ph * 0.8) * 0.025, s):
        lz.relleno(np.array([[-70, -30], [70, -30], [54, 4], [-54, 4]]), (120, 78, 58))
        lz.relleno(np.array([[-70, -30], [70, -30], [66, -22], [-66, -22]]), (196, 140, 90))
        lz.relleno(rect_red(-3, -140, 6, 110, 2), (98, 66, 50))
        lz.relleno(np.array([[-46, -134], [46, -134], [42 * vela, -66], [-42 * vela, -66]]), (250, 244, 232))
        lz.relleno(np.array([[-10, -134], [10, -134], [10, -66], [-10, -66]]), (216, 60, 60))
        lz.relleno(np.array([[-4, -66], [4, -66], [4, -134], [-4, -134]]), (216, 60, 60), alfa=0.0)
        lz.relleno(np.array([[3, -140], [22, -134 + math.sin(ph * 3) * 3], [3, -128]]), (216, 60, 60))
        lz.relleno(np.array([[-60, -30], [-90, -50], [-60, -50]]), (250, 244, 232), alfa=0.9)


# ======================================================================== tesoros y utilería
def barra_oro(lz, x, y, s=1.0, rot=0.0, brillo=0.0, alfa=1.0):
    """Lingote de oro (origen en el centro)."""
    with lz.grupo(x, y, s, rot):
        lz.relleno(np.array([[-46, 6], [46, 6], [40, 26], [-40, 26]]), ORO_S, alfa=alfa)
        lz.relleno(np.array([[-46, 6], [46, 6], [32, -14], [-32, -14]]), ORO_L, alfa=alfa)
        lz.relleno(np.array([[-46, 6], [46, 6], [46, 8], [-46, 8]]), (255, 250, 210), alfa=alfa)
        lz.relleno(np.array([[-30, 10], [-16, 10], [-19, 24], [-31, 24]]), (255, 240, 170), alfa=0.8 * alfa)
        if brillo > 0.01:
            lz.halo(0, 0, 70 * brillo, ORO, alfa=0.55 * alfa)
            lz.relleno(np.array([[22, -8], [25, -2], [31, 0], [25, 2], [22, 8], [19, 2], [13, 0], [19, -2]]), (255, 255, 255), alfa=brillo * alfa)


def disco(lz, x, y, r, t=0.0, tipo="oro", rot=0.0):
    """Disco de oro (sol con rayos) o de plata (luna con cráteres)."""
    oro = tipo == "oro"
    c1, c2, c3 = ((255, 214, 90), (232, 160, 44), (255, 246, 190)) if oro else ((226, 232, 246), (150, 162, 190), (250, 252, 255))
    with lz.grupo(x, y, 1.0, rot):
        if oro:
            pts = []
            for k in range(32):
                a = k / 32 * 6.283
                rr = r if k % 2 == 0 else r * 0.8
                pts.append((math.cos(a) * rr, math.sin(a) * rr))
            lz.relleno(np.array(pts), c2)
        lz.relleno(circulo(0, 0, r * 0.72, 40), c1)
        lz.relleno(circulo(-r * 0.10, -r * 0.10, r * 0.62, 40), P.aclarar(c1, 0.25))
        if oro:
            for rr in (0.5, 0.32, 0.16):
                lz.relleno(circulo(0, 0, r * rr, 30), c2 if rr != 0.32 else c1)
            lz.relleno(circulo(0, 0, r * 0.1, 20), c3)
        else:
            for (dx, dy, rr) in ((-0.25, -0.15, 0.13), (0.22, 0.10, 0.18), (-0.05, 0.36, 0.1), (0.3, -0.3, 0.08)):
                lz.relleno(circulo(r * dx, r * dy, r * rr, 20), c2, alfa=0.55)


def cofre(lz, x, y, s=1.0, abierto=0.0, brillo=1.0):
    with lz.grupo(x, y, s):
        lz.relleno(rect_red(-38, -38, 76, 38, 5), (140, 92, 58))
        lz.relleno(rect_red(-38, -20, 76, 6, 1), (94, 60, 44))
        lz.relleno(rect_red(-6, -24, 12, 14, 2), ORO)
        if abierto > 0.02:
            lz.halo(0, -44, 60 * abierto, ORO, alfa=0.7 * abierto * brillo)
            lz.relleno(np.array([[-36, -38], [36, -38], [30 + 10 * abierto, -38 - 34 * abierto], [-30 - 10 * abierto, -38 - 34 * abierto]]), (172, 122, 78))
            lz.relleno(rect_red(-30, -44, 60, 8, 3), ORO)
            for i in range(6):
                lz.relleno(circulo(-24 + i * 10, -46 - (i % 2) * 4, 6, 10), ORO_L if i % 2 else ORO)
        else:
            lz.relleno(np.array([[-38, -38], [38, -38], [34, -52], [-34, -52]]), (172, 122, 78))


def saco(lz, x, y, s=1.0, col=ORO, brillo=0.0):
    with lz.grupo(x, y, s):
        lz.relleno(blob(0, -22, 26, 4, 0.10, 26, 4), P.oscurecer(col, 0.25))
        lz.relleno(blob(-3, -25, 22, 4, 0.10, 26, 4), col)
        lz.relleno(rect_red(-8, -52, 16, 8, 3), (150, 100, 60))
        if brillo > 0.01:
            lz.halo(0, -22, 46, col, alfa=0.5 * brillo)


def joya(lz, x, y, s=1.0, tipo="anillo", t=0.0, brillo=0.6):
    with lz.grupo(x, y, s):
        if tipo == "anillo":
            lz.relleno(circulo(0, 0, 16, 24), ORO)
            lz.relleno(circulo(0, 0, 9, 20), (60, 40, 84), alfa=1.0)
            lz.relleno(np.array([[-8, -14], [8, -14], [12, -24], [0, -32], [-12, -24]]), (110, 220, 240))
            lz.relleno(np.array([[-4, -20], [4, -20], [0, -30]]), (220, 250, 255))
        elif tipo == "collar":
            pts = [(-30 + i * 6, -10 + 0.032 * (-30 + i * 6) ** 2 * 0.2 + 18 - 0.03 * (-30 + i * 6) ** 2) for i in range(11)]
            for (px, py) in pts:
                lz.relleno(circulo(px, py, 4, 8), ORO)
            lz.relleno(np.array([[-6, 18], [6, 18], [10, 30], [0, 40], [-10, 30]]), (90, 210, 150))
        elif tipo == "reloj":
            lz.relleno(circulo(0, 0, 16, 24), (210, 214, 226))
            lz.relleno(circulo(0, 0, 12, 20), (250, 250, 252))
            lz.relleno(rect_red(-1, -9, 2, 9, 1), (60, 60, 80))
            lz.relleno(rect_red(0, -1, 7, 2, 1), (60, 60, 80))
            lz.relleno(rect_red(-6, -34, 12, 18, 3), (120, 90, 64))
            lz.relleno(rect_red(-6, 16, 12, 18, 3), (120, 90, 64))
        if brillo > 0.01:
            a = 0.5 + 0.5 * math.sin(t * 4 + x * 0.05)
            lz.halo(0, 0, 30, (255, 240, 180), alfa=0.25 * brillo * a)


def pluma(lz, x, y, s=1.0, rot=0.0, col=(60, 200, 130), t=0.0):
    """Pluma de quetzal (curva larga con nervadura)."""
    with lz.grupo(x, y, s, rot):
        pts = []
        for i in range(21):
            v = i / 20
            cx = math.sin(v * 2.6 + t * 0.8) * 16 * v
            pts.append((cx, -v * 120))
        izq = [(px - 12 * math.sin(math.pi * min(1, i / 20 * 1.1)) ** 0.7, py) for i, (px, py) in enumerate(pts)]
        der = [(px + 12 * math.sin(math.pi * min(1, i / 20 * 1.1)) ** 0.7, py) for i, (px, py) in list(enumerate(pts))[::-1]]
        lz.relleno(np.array(izq + der), col)
        lz.relleno(np.array([(px, py) for px, py in pts] + [(px + 2, py) for px, py in pts[::-1]]), P.aclarar(col, 0.4))


def jade(lz, x, y, s=1.0, t=0.0):
    """Piedra de jade facetada."""
    with lz.grupo(x, y, s):
        lz.relleno(np.array([[-30, -6], [-16, -32], [16, -32], [30, -6], [0, 26]]), (44, 170, 120))
        lz.relleno(np.array([[-16, -32], [16, -32], [6, -6], [-6, -6]]), (110, 226, 170))
        lz.relleno(np.array([[-30, -6], [-16, -32], [-6, -6]]), (70, 200, 140))
        lz.relleno(np.array([[30, -6], [16, -32], [6, -6]]), (30, 130, 96))
        lz.relleno(np.array([[-6, -6], [6, -6], [0, 26]]), (36, 150, 108))


def moneda(lz, x, y, r=12, brillo=0.0):
    lz.relleno(circulo(x, y, r, 18), ORO_S)
    lz.relleno(circulo(x - 1, y - 1, r * 0.82, 18), ORO)
    lz.relleno(circulo(x - r * 0.2, y - r * 0.2, r * 0.3, 10), ORO_L)


def brasero(lz, x, y, s=1.0, t=0.0):
    """Brasero de piedra con fuego."""
    from mundo import llama
    with lz.grupo(x, y, s):
        lz.relleno(np.array([[-26, -28], [26, -28], [20, 0], [-20, 0]]), (110, 80, 96))
        lz.relleno(rect_red(-30, -34, 60, 10, 3), (150, 112, 120))
        llama(lz, 0, -32, 0.55, t, seed=int(x))
        lz.halo(0, -50, 90, (255, 150, 60), alfa=0.35)


# ======================================================================== edificios
def templo_mayor(lz, x, y, s=1.0, luz=1.0):
    """Templo Mayor visto de frente: pirámide escalonada con dos adoratorios (Tláloc azul, Huitzilopochtli rojo)."""
    with lz.grupo(x, y, s):
        for i in range(5):
            w = 250 - i * 38
            h = 44
            yy = -i * h
            lz.relleno(rect_red(-w, yy - h, 2 * w, h, 0), (232, 210, 180) if i % 2 == 0 else (214, 186, 160))
            lz.relleno(rect_red(-w, yy - h, 2 * w, 6, 0), (250, 236, 212))
        lz.relleno(np.array([[-30, 0], [30, 0], [30, -220], [-30, -220]]), (176, 140, 128))          # escalinata doble
        for k in range(10):
            lz.relleno(rect_red(-30, -k * 22 - 6, 60, 3, 0), (232, 212, 196))
        lz.relleno(np.array([[-2, 0], [2, 0], [2, -220], [-2, -220]]), (120, 90, 96))
        top = -5 * 44
        for (cx, col, col2) in ((-105, (70, 150, 220), (30, 90, 170)), (105, (222, 70, 78), (150, 40, 60))):
            lz.relleno(rect_red(cx - 46, top - 70, 92, 70, 2), col)
            lz.relleno(rect_red(cx - 52, top - 82, 104, 14, 2), col2)
            lz.relleno(rect_red(cx - 16, top - 50, 32, 50, 2), (40, 24, 50))
            lz.relleno(rect_red(cx - 10, top - 106, 20, 26, 2), (250, 236, 212))


def palacio(lz, x, y, s=1.0, ruina=0.0, luz=0.0):
    """Palacio mexica de una planta, techo plano, con entrada, columnas y franjas rojas."""
    with lz.grupo(x, y, s):
        lz.relleno(rect_red(-260, -150, 520, 150, 2), (246, 230, 204))
        lz.relleno(rect_red(-260, -150, 520, 16, 0), (222, 70, 78))
        lz.relleno(rect_red(-260, -168, 520, 18, 0), (204, 180, 150))
        for i in range(6):
            lz.relleno(rect_red(-224 + i * 84, -120, 30, 120, 3), (218, 196, 172))
        lz.relleno(rect_red(-44, -104, 88, 104, 4), (52, 34, 58))
        if luz > 0.01:
            lz.halo(0, -50, 90 * luz, ORO, alfa=0.6 * luz)
        for i in range(3):
            lz.relleno(rect_red(-236 + i * 178, -100, 56, 30, 3), (120, 150, 190))
        if ruina > 0.01:
            lz.relleno(np.array([[-260, -170], [260, -170], [260, -170 + 170 * ruina], [-260, -170 + 170 * ruina]]), (30, 24, 44), alfa=0.0)


# ======================================================================== Durero y otros
def durero(lz, x, y, s=1.0, t=0.0, lado=1, escribe=0.0, sorpresa=0.0):
    """Alberto Durero: melena castaña, boina oscura, jubón verde oscuro y un cuaderno donde escribe con pluma (escribe 0..1)."""
    piel = (238, 190, 150)
    with lz.grupo(x, y, s * lado, 0.0, s):
        cap(lz, -6, -44, 0.04, 44, 12, (50, 44, 60))
        cap(lz, 6, -44, -0.04, 44, 12, (60, 54, 70))
        lz.relleno(rect_red(-15, -46, 30, 10, 3), (40, 30, 40))
        lz.relleno(np.array([[-16, -92], [16, -92], [20, -40], [-20, -40]]), (48, 92, 84))
        lz.relleno(np.array([[-16, -92], [16, -92], [12, -78], [-12, -78]]), (236, 228, 214))
        lz.relleno(rect_red(-16, -56, 32, 6, 1), (60, 40, 40))
        w = math.sin(t * 10) * 0.25 * escribe
        cap(lz, -14, -84, -0.5, 30, 10, (40, 76, 70))
        xb, yb = cap(lz, 14, -84, 0.9 + w, 32, 10, (48, 92, 84))
        lz.relleno(rect_red(xb - 6, yb - 22, 30, 38, 3), (250, 240, 214))
        lz.relleno(np.array([[xb + 6, yb - 6], [xb + 30, yb - 34], [xb + 34, yb - 30], [xb + 10, yb - 2]]), (230, 220, 200))
        lz.relleno(rect_red(-5, -104, 10, 12, 3), piel)
        lz.relleno(np.array([[-16, -114], [-22, -84], [-10, -86], [-8, -100], [8, -100], [10, -86], [22, -84], [16, -114]]), (128, 84, 52))   # melena
        lz.relleno(circulo(0, -112, 13.5, 22), piel)
        lz.relleno(np.array([[-2, -104], [10, -106], [7, -95], [0, -96]]), (150, 100, 64))                                              # barba
        lz.relleno(circulo(5, -114, 2.2 + 1.2 * sorpresa, 8), (40, 30, 40))
        lz.relleno(elipse(0, -128, 17, 8, 0.0, 16), (50, 40, 60))
        lz.relleno(elipse(-3, -134, 12, 8, 0.0, 16), (66, 54, 78))


def canon(lz, x, y, s=1.0, rot=0.0):
    """Cañón de bronce sobre ruedas (origen en el suelo, apunta a la derecha)."""
    with lz.grupo(x, y, s):
        with lz.grupo(0, -34, 1.0, rot):
            lz.relleno(rect_red(-50, -16, 120, 30, 8), (120, 86, 60))
            lz.relleno(rect_red(58, -20, 24, 38, 5), (150, 108, 72))
            lz.relleno(rect_red(-56, -12, 14, 22, 4), (98, 70, 50))
            lz.relleno(circulo(-52, 0, 9, 12), (150, 108, 72))
        lz.relleno(rect_red(-40, -30, 80, 16, 4), (110, 78, 56))
        lz.relleno(circulo(-6, -20, 22, 20), (140, 100, 66))
        lz.relleno(circulo(-6, -20, 12, 20), (96, 68, 48))
        lz.relleno(circulo(-6, -20, 4, 10), (60, 44, 40))


def soldado_triste(lz, x, y, s=1.0, t=0.0, lado=1, seed=0, tunica=(150, 40, 60)):
    """Soldado sentado, cabeza baja y una mano en la cara (llora); el morrión queda a su lado en el suelo."""
    with lz.grupo(x, y, s * lado, 0.0, s):
        pant = (74, 62, 84)
        cap(lz, 4, -22, 1.5, 44, 12, pant)           # piernas estiradas hacia delante
        cap(lz, -2, -22, 1.42, 44, 12, P.oscurecer(pant, 0.2))
        lz.relleno(rect_red(46, -10, 12, 12, 3), (52, 40, 44))
        with lz.grupo(-8, -22, 1.0, 0.35):
            lz.relleno(rect_red(-13, -66, 26, 66, 9), tunica)
            lz.relleno(rect_red(-13, -66, 26, 46, 8), ACERO)
            lz.relleno(rect_red(-13, -14, 26, 6, 2), (110, 76, 54))
            cap(lz, 6, -60, 2.6, 34, 10, tunica)
            lz.relleno(circulo(14, -94, 5, 10), PIELES[0])
            lz.relleno(rect_red(-4, -76, 8, 10, 3), PIELES[0])
            lz.relleno(circulo(6, -82, 12.5, 22), PIELES[0])
            lz.relleno(np.array([[8, -78], [18, -82], [15, -72], [7, -72]]), (66, 46, 40))
        # lágrimas
        for k in range(3):
            ph = (t * 1.2 + k * 0.33 + h01(seed, k)) % 1.0
            lz.relleno(circulo(30, -96 + ph * 60, 2.6, 6), (150, 210, 255), alfa=1 - ph)
        lz.relleno(np.array([[64, -6], [72, -22], [88, -22], [96, -6]]), ACERO)        # morrión en el suelo
        lz.relleno(np.array([[58, -6], [102, -6], [98, -1], [62, -1]]), ACERO_S)


def obrero(lz, x, y, s=1.0, t=0.0, lado=1, pico=0.0, paso=0.0, seed=0, chaleco=(255, 150, 40)):
    """Obrero/electricista con casco amarillo y chaleco naranja; pico 0..1 = balanceo de la herramienta."""
    ph = _ph(t, paso, seed)
    sw = math.sin(ph) * 0.5 if paso > 0 else 0.0
    with lz.grupo(x, y, s * lado, 0.0, s):
        cap(lz, -5, -44, -sw, 44, 11, (60, 80, 140))
        cap(lz, 5, -44, sw, 44, 11, (70, 92, 156))
        lz.relleno(rect_red(-8, -6, 14, 8, 3), (60, 44, 40))
        lz.relleno(rect_red(-13, -90, 26, 48, 9), (240, 240, 250))
        lz.relleno(rect_red(-13, -90, 26, 34, 8), chaleco)
        lz.relleno(rect_red(-13, -70, 26, 5, 1), (255, 250, 200))
        g = math.sin(t * 9 + seed) * pico
        xa, ya = cap(lz, -13, -84, -0.3 + 0.2 * g, 30, 9, (240, 190, 150))
        xb, yb = cap(lz, 13, -84, 0.6 + 1.9 * abs(g) - 0.4 * pico, 32, 9, (240, 190, 150))
        if pico > 0:
            cap(lz, xb, yb, 3.14 - 0.2 * g, 54, 5, (120, 90, 60))
            lz.relleno(np.array([[xb - 12, yb + 46], [xb + 14, yb + 52], [xb + 6, yb + 60], [xb - 16, yb + 54]]) * np.array([1, -1]) + np.array([0, 2 * yb]) * 0 + np.array([0, -100]), (120, 120, 140), alfa=0.0)
        lz.relleno(rect_red(-4, -100, 8, 10, 3), (240, 190, 150))
        lz.relleno(circulo(0, -108, 12.5, 22), (240, 190, 150))
        lz.relleno(circulo(5, -110, 1.8, 8), (40, 28, 40))
        lz.relleno(np.array([[-14, -110], [-12, -122], [0, -130], [12, -122], [14, -110], [16, -108], [-16, -108]]), (255, 214, 60))
