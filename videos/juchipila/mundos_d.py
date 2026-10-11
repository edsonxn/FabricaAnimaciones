# -*- coding: utf-8 -*-
"""Mundos 2D de la escena 3: excavación arqueológica, el muro de huecos sobre el risco («ventanas» vistas de cerca y de lejos) y el portón que se abre."""
import math

import numpy as np

import plano as P
import kz_pers2d as K2
import paisajes as PA
from motor import circulo, elipse, rect_red, catmull, h01, prog, smooth, e_out, e_back, e_inout, W, H, ruido1


# ------------------------------------------------------------------------------------------------ excavación
ESTRATOS = [(176, 120, 96), (150, 98, 92), (196, 140, 104), (128, 82, 86)]
PIEDRAS = [(1020, 760, 200, 150, 0), (1330, 830, 170, 120, 1), (800, 860, 150, 110, 2), (1180, 905, 190, 90, 0)]     # x, y, w, h, motivo


def _talla(lz, x, y, w, h, motivo, a=1.0):
    """Bloque de piedra tallada (espiral, greca o escalones) en 2 tonos."""
    lz.relleno(rect_red(x - w / 2 + 6, y - h / 2 + 8, w, h, 14), (116, 84, 90), alfa=a, capa=1)
    lz.relleno(rect_red(x - w / 2, y - h / 2, w, h, 14), (214, 190, 166), alfa=a, capa=1)
    lz.relleno(rect_red(x - w / 2, y - h / 2, w, h * 0.18, 10), (232, 212, 190), alfa=a, capa=1)
    col = (150, 112, 104)
    if motivo == 0:                                               # greca escalonada
        pts = []
        for i in range(6):
            pts += [(x - w * 0.36 + i * w * 0.12, y + h * 0.16 - (i % 2) * h * 0.2), (x - w * 0.36 + (i + 1) * w * 0.12, y + h * 0.16 - (i % 2) * h * 0.2)]
        lz.trazo(np.array(pts), col, 7.0, afinar=False, temblor=0.0, capa=1)
    elif motivo == 1:                                             # espiral
        th = np.linspace(0, 5.5 * math.pi, 70)
        r = np.linspace(2, min(w, h) * 0.34, 70)
        lz.trazo(np.stack([x + r * np.cos(th), y + r * np.sin(th)], 1), col, 6.0, afinar=False, temblor=0.0, capa=1)
    else:                                                         # rombos
        for i in range(3):
            cx_ = x - w * 0.26 + i * w * 0.26
            lz.trazo(np.array([(cx_, y - h * 0.26), (cx_ + w * 0.10, y), (cx_, y + h * 0.26), (cx_ - w * 0.10, y), (cx_, y - h * 0.26)]), col, 6.0, afinar=False, temblor=0.0, capa=1)


def excavacion(lz, t, t0, t1, area=(560, 650, 1500, 1010)):
    """Corte de tierra con estratos; los terrones saltan uno a uno (según se «excava») y dejan ver piedra tallada. Devuelve la fracción excavada."""
    x0, y0, x1, y1 = area
    # terreno
    n = len(ESTRATOS)
    for k, c in enumerate(ESTRATOS):
        yy0 = y0 + (y1 - y0) * k / n
        lz.relleno(np.array([(x0, yy0), (x1, yy0), (x1, yy0 + (y1 - y0) / n + 2), (x0, yy0 + (y1 - y0) / n + 2)]), c, capa=0)
    lz.relleno(rect_red(x0, y0 - 24, x1 - x0, 30, 10), (112, 170, 100), capa=0)
    for (px, py, pw, ph, mo) in PIEDRAS:
        _talla(lz, px, py, pw, ph, mo)
    # terrones que cubren las piedras (saltan según su turno)
    f = prog(t, t0, t1)
    cols = 17
    for i in range(cols):
        for j in range(8):
            cx_ = x0 + (x1 - x0) * (i + 0.5) / cols
            cy_ = y0 + 14 + (y1 - y0 - 14) * (j + 0.5) / 8
            # solo hay terrones donde hay piedra detrás (el resto es tierra del corte)
            tapa = any(abs(cx_ - px) < pw / 2 + 30 and abs(cy_ - py) < ph / 2 + 24 for (px, py, pw, ph, mo) in PIEDRAS)
            if not tapa:
                continue
            tr = 0.08 + 0.84 * h01(5, i, j) * 0.6 + 0.4 * (i / cols) * 0.4
            u = prog(f, tr, tr + 0.10)
            if u >= 1:
                continue
            c = ESTRATOS[min(n - 1, int(j * n / 8))]
            dy = -90 * u * (1 - u) * 4 if u > 0 else 0.0
            lz.relleno(circulo(cx_ + 16 * u * (h01(6, i, j) - 0.5), cy_ + dy, (28 + 8 * h01(7, i, j)) * (1 - 0.6 * u), 12), P.oscurecer(c, 0.1), alfa=1 - u * 0.8, capa=1)
    return f


def arqueologo(lz, x, y, s, t, ph=0.0, seed=0):
    spec = dict(piel="clara", pelo=(110, 70, 50), peinado="corto", cejas_g=1.2, torso="camiseta", ropa=(186, 150, 106), ropa2=(120, 88, 60), tocado="sombrero_palma", bigote=True, pantalon=(96, 84, 76))
    K2.cuerpo(lz, x, y, s, spec, t, piernas="idle", brazos="labra", mirar=1, vista="perfil", ph=ph, seed=seed, cara="minima")


def props_excavacion(lz, t, area):
    """Carpa, cajones, cubeta, pala y cuerdas de cuadrícula alrededor de la excavación."""
    x0, y0, x1, y1 = area
    for i in range(1, 6):
        xx = x0 + (x1 - x0) * i / 6
        lz.relleno(np.array([(xx - 1.5, y0 - 30), (xx + 1.5, y0 - 30), (xx + 1.5, y0 - 4), (xx - 1.5, y0 - 4)]), (255, 255, 255), alfa=0.8, capa=1)
        lz.relleno(circulo(xx, y0 - 34, 5, 8), (222, 60, 70), capa=1)
    cx, cy = x1 + 150, y0 + 30
    lz.relleno(np.array([(cx - 130, cy + 150), (cx, cy - 90), (cx + 130, cy + 150)]), (236, 228, 214), capa=0)
    lz.relleno(np.array([(cx - 130, cy + 150), (cx, cy - 90), (cx, cy + 150)]), (214, 204, 190), capa=0)
    for k in range(4):
        lz.relleno(np.array([(cx - 100 + k * 50, cy + 150), (cx - 40 + k * 20, cy - 30 + 0.2 * k), (cx - 30 + k * 20, cy - 30), (cx - 70 + k * 50, cy + 150)]), (222, 60, 70), alfa=0.35, capa=0)
    lz.relleno(np.array([(cx - 30, cy + 150), (cx + 30, cy + 150), (cx + 30, cy + 40), (cx - 30, cy + 40)]), (96, 60, 70), capa=0)
    for (bx, by, bw, bh) in ((x0 - 210, y1 + 30, 90, 62), (x0 - 140, y1 + 42, 70, 50)):
        lz.relleno(rect_red(bx, by - bh, bw, bh, 5), (190, 140, 90), capa=1)
        lz.relleno(rect_red(bx, by - bh, bw, bh * 0.2, 5), (214, 168, 112), capa=1)
        lz.relleno(rect_red(bx, by - bh * 0.55, bw, 6, 2), (150, 106, 70), capa=1)
    bx, by = x0 - 60, y1 + 26
    lz.relleno(np.array([(bx - 26, by - 52), (bx + 26, by - 52), (bx + 20, by), (bx - 20, by)]), (110, 130, 170), capa=1)
    lz.relleno(elipse(bx, by - 52, 26, 7, 0, 16), (70, 84, 120), capa=1)
    px = x1 + 40
    lz.relleno(np.array([(px - 4, y1 - 210), (px + 4, y1 - 210), (px + 4, y1 + 20), (px - 4, y1 + 20)]), (140, 100, 70), capa=1)
    lz.relleno(np.array([(px - 24, y1 + 20), (px + 24, y1 + 20), (px + 16, y1 + 76), (px, y1 + 90), (px - 16, y1 + 76)]), (170, 176, 196), capa=1)


# ------------------------------------------------------------------------------------------------ muro de huecos en el risco
def risco(lz, t, k=1.0, cx=960, cy=700, brillo=0.8):
    """Risco irregular con estratos, árboles y cactus y, en lo alto, el muro de piedra con seis huecos (luz cálida dentro). k = escala; (cx, cy) = base del muro."""
    s = k
    base = [(-1100, 1300), (-960, 330), (-780, 250), (-640, 120), (-470, 90), (-380, 10), (-210, -10), (210, -10), (300, 20), (420, 80), (540, 70), (700, 190), (860, 260), (1000, 380), (1100, 1300)]
    per = [(cx + x * s + 22 * s * ruido1(i * 1.7, 7, 1), cy + y * s + 14 * s * ruido1(i * 2.3, 8, 2)) for i, (x, y) in enumerate(base)]
    lz.relleno(np.array(catmull(np.array(per, float), 6, False)), (112, 64, 108), capa=0)
    lz.relleno(np.array(catmull(np.array([(x + 26 * s, y + 6 * s) for x, y in per[:-2]] + [per[-2], per[-1]], float), 6, False)), (146, 88, 120), capa=0)
    for q in range(9):
        qx = cx + (-700 + 170 * q) * s
        qy = cy + (190 + 60 * ((q * 7) % 5)) * s
        lz.relleno(np.array([(qx - 70 * s, qy + 40 * s), (qx - 30 * s, qy - 28 * s), (qx + 40 * s, qy - 34 * s), (qx + 80 * s, qy + 40 * s)]), (170, 108, 124), alfa=0.55, capa=0)
        lz.relleno(np.array([(qx - 30 * s, qy - 28 * s), (qx + 40 * s, qy - 34 * s), (qx + 10 * s, qy + 6 * s)]), (210, 140, 124), alfa=0.5, capa=0)
    for q in range(7):
        yq = cy + (110 + 85 * q) * s
        lz.relleno(np.array([(cx - 1000 * s, yq), (cx + 1000 * s, yq - 24 * s), (cx + 1000 * s, yq - 8 * s), (cx - 1000 * s, yq + 10 * s)]), (86, 46, 88), alfa=0.30, capa=0)
    for q in range(14):
        if q % 3 == 0:
            continue
        vx = cx + (-820 + 125 * q + 30 * ruido1(q, 3, 3)) * s
        vy = cy + (180 + 55 * ((q * 5) % 6)) * s
        PA.arbol(lz, vx, vy, 0.9 * s, 0.0, seed=q, t=t, capa=0)
    mw, mh = 620 * s, 120 * s
    x0, y0 = cx - mw / 2, cy - mh - 8 * s
    lz.relleno(rect_red(x0 + 8 * s, y0 + 8 * s, mw, mh, 6 * s), (60, 36, 80), alfa=0.35, capa=1)
    lz.relleno(rect_red(x0, y0, mw, mh, 6 * s), (214, 190, 166), capa=1)
    lz.relleno(rect_red(x0, y0, mw, mh * 0.14, 5 * s), (232, 212, 190), capa=1)
    for r in range(4):
        yy = y0 + mh * (0.22 + 0.2 * r)
        lz.relleno(rect_red(x0, yy, mw, 3 * s, 1), (170, 142, 130), alfa=0.7, capa=1)
        for c_ in range(10):
            xx = x0 + mw * (c_ + 0.5 * (r % 2)) / 10
            lz.relleno(rect_red(xx, yy, 2.4 * s, mh * 0.2, 1), (170, 142, 130), alfa=0.6, capa=1)
    n = 6
    for i in range(n):
        wx = x0 + mw * (0.07 + 0.155 * i)
        ww = mw * 0.085
        arc = [(wx, y0 + mh * 0.88)] + [(wx + ww / 2 + ww / 2 * math.cos(a), y0 + mh * 0.34 - ww / 2 * math.sin(a)) for a in np.linspace(math.pi, 0, 14)] + [(wx + ww, y0 + mh * 0.88)]
        lz.relleno(np.array(arc), (70, 40, 80), capa=1)
        lz.relleno(np.array(arc[:1] + [(px, py + (y0 + mh * 0.88 - py) * 0.12) for px, py in arc[1:-1]] + arc[-1:]), (255, 206, 110), alfa=0.65 * brillo, capa=1)
        lz.halo(wx + ww / 2, y0 + mh * 0.62, ww * 2.2, (255, 190, 100), alfa=0.40 * brillo, capa=1)


# ------------------------------------------------------------------------------------------------ portón y calendario
def porton(lz, t, abre, cx=960, cy=900, s=1.0):
    """Portón de la zona arqueológica: dos hojas que giran al abrir (abre 0..1), cartel y piedras a los lados."""
    ang = abre * 1.15
    for sd in (-1, 1):
        w = 210 * s * math.cos(ang)
        x_in = cx + sd * 12 * s
        x_out = x_in + sd * w
        for k, col in enumerate(((120, 80, 70), (168, 118, 90))):
            off = 0 if k == 0 else 7 * s
            lz.relleno(np.array([(x_in, cy - 380 * s + off), (x_out, cy - 360 * s + off), (x_out, cy - 14 * s), (x_in, cy)]), col, capa=1)
        for q in range(6):                                          # tablones
            yq = cy - 350 * s + q * 58 * s
            lz.relleno(np.array([(x_in, yq), (x_out, yq + 6 * s), (x_out, yq + 12 * s), (x_in, yq + 6 * s)]), (96, 62, 60), alfa=0.55, capa=1)
    for sd in (-1, 1):                                              # columnas de piedra
        px = cx + sd * 262 * s
        lz.relleno(rect_red(px - 36 * s, cy - 430 * s, 72 * s, 440 * s, 8 * s), (206, 186, 164), capa=1)
        lz.relleno(rect_red(px - 36 * s, cy - 430 * s, 72 * s, 440 * s * 0.12, 8 * s), (226, 208, 188), capa=1)


def entorno_porton(lz, t, s=1.0, cx=960, cy=900):
    """Muros bajos de piedra a los lados del portón, árboles y el cartel de la zona arqueológica."""
    for sd in (-1, 1):
        x_in = cx + sd * 300 * s
        for q in range(6):
            xx = x_in + sd * (q * 130 * s)
            lz.relleno(rect_red(xx - 62 * s, cy - 70 * s - 6 * q, 124 * s, 70 * s + 6 * q, 6), (200, 180, 160), capa=1)
            lz.relleno(rect_red(xx - 62 * s, cy - 70 * s - 6 * q, 124 * s, 18 * s, 6), (228, 210, 190), capa=1)
            lz.relleno(rect_red(xx - 62 * s, cy - 40 * s - 6 * q, 124 * s, 3 * s, 1), (160, 138, 126), alfa=0.6, capa=1)
        for q in range(3):
            PA.arbol(lz, x_in + sd * (150 + 330 * q) * s, cy - 70 * s - 24 - 14 * q, (1.6 - 0.25 * q) * s, 0.0, seed=q + (5 if sd > 0 else 0), t=t, capa=1)
    bx = cx - 520 * s
    lz.relleno(rect_red(bx - 6, cy - 300 * s, 12, 300 * s, 3), (120, 84, 70), capa=1)
    lz.relleno(rect_red(bx - 150, cy - 400 * s, 300, 130 * s, 12), (250, 244, 232), capa=1)
    lz.relleno(rect_red(bx - 150, cy - 400 * s, 300, 36 * s, 12), (222, 60, 70), capa=1)
    P.rotulo(lz, bx, cy - 382 * s, "ZONA ARQUEOLÓGICA", px=22, color=(255, 255, 255), alfa=1.0, sombra=0.0)
    P.rotulo(lz, bx, cy - 318 * s, "Las Ventanas", px=34, color=(34, 28, 80), alfa=1.0, sombra=0.0)


def calendario(lz, x, y, s, t, dia="2", mes="AGOSTO", anio="2019", alfa=1.0):
    """Hoja de calendario: cabecera roja con anillas, día enorme, mes y año."""
    lz.relleno(rect_red(x - 170 * s + 8 * s, y - 200 * s + 10 * s, 340 * s, 400 * s, 22 * s), (20, 8, 50), alfa=0.30 * alfa, capa=2)
    lz.relleno(rect_red(x - 170 * s, y - 200 * s, 340 * s, 400 * s, 22 * s), (252, 248, 240), alfa=alfa, capa=2)
    lz.relleno(rect_red(x - 170 * s, y - 200 * s, 340 * s, 96 * s, 22 * s), (222, 60, 70), alfa=alfa, capa=2)
    lz.relleno(rect_red(x - 170 * s, y - 130 * s, 340 * s, 26 * s, 0), (222, 60, 70), alfa=alfa, capa=2)
    for sd in (-1, 1):
        lz.relleno(rect_red(x + sd * 90 * s - 8 * s, y - 220 * s, 16 * s, 44 * s, 8 * s), (90, 84, 110), alfa=alfa, capa=2)
    P.rotulo(lz, x, y - 154 * s, mes, px=62 * s, color=(255, 255, 255), alfa=alfa, sombra=0.0)
    P.rotulo(lz, x, y + 10 * s, dia, px=230 * s, color=(34, 28, 80), alfa=alfa, sombra=0.0)
    P.rotulo(lz, x, y + 148 * s, anio, px=74 * s, color=(222, 60, 70), alfa=alfa, sombra=0.0)
