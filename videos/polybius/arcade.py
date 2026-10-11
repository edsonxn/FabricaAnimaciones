# -*- coding: utf-8 -*-
"""Mundo arcade de 1981 dibujado por código (pintor `mg.P`, coordenadas 1920x1080): cabinas de frente y de perfil, pantallas
vectoriales propias (formas geométricas «tipo Polybius», asteroides, túnel, tanque de alambre), salón con neones y moqueta,
jugadores. Nada imita la pantalla de un juego comercial concreto: son gráficos vectoriales genéricos de la época."""
import math

import numpy as np

from mg import *  # noqa: F401,F403

NEGRO = (0.012, 0.012, 0.018)
CAB = (0.035, 0.038, 0.050)
CAB2 = (0.070, 0.075, 0.095)
VERDE = (0.25, 1.0, 0.45)
CIAN = (0.25, 0.90, 1.0)
MAG = (1.0, 0.25, 0.75)
AMBAR = (1.0, 0.70, 0.20)
VIOL = (0.62, 0.35, 1.0)
NEON = [CIAN, MAG, AMBAR, VERDE, VIOL, (1.0, 0.30, 0.25)]


def rotp(cx, cy, r, ang):
    return cx + r * math.cos(ang), cy + r * math.sin(ang)


def poligono(p, cx, cy, r, n, ang, w, color, op=1.0, sy=1.0):
    pts = [(cx + r * math.cos(ang + 2 * math.pi * k / n), cy + r * sy * math.sin(ang + 2 * math.pi * k / n)) for k in range(n)]
    p.polilinea(pts, w, color, op, cerrado=True, caps=False)
    return pts


# ------------------------------------------------------------------------------------------------ pantallas vectoriales
def pant_formas(p, x0, y0, x1, y1, t, op=1.0, vel=1.0, fondo=True, detalle=1.0):
    """Formas geométricas que giran sin parar (lo que la leyenda dice que mostraba la máquina). Dibujo propio."""
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    R = min(x1 - x0, y1 - y0) / 2
    if fondo:
        p.rect(x0, y0, x1, y1, (0.0, 0.0, 0.012), op)
    w = max(2.0, R * 0.018)
    n_an = int(5 + 3 * detalle)
    for k in range(n_an):
        u = ((k / n_an + t * 0.11 * vel) % 1.0)
        r = R * (0.08 + 0.92 * u ** 1.5)
        lados = (3, 4, 6, 5, 8)[k % 5]
        col = NEON[k % len(NEON)]
        poligono(p, cx, cy, r, lados, t * (0.9 + 0.25 * k) * vel * (1 if k % 2 else -1), w * (0.6 + u), col, op * min(1.0, 0.25 + u * 1.4) * (1 - u ** 6))
    for k in range(int(10 * detalle)):                     # radios que barren
        a = t * 0.6 * vel + k * math.pi / 5
        r0, r1 = R * 0.10, R * (0.55 + 0.4 * math.sin(t * 1.7 + k))
        p.linea(rotp(cx, cy, r0, a), rotp(cx, cy, r1, a), w * 0.5, NEON[(k + 2) % 6], op * 0.55, caps=False)
    p.glow(cx, cy, R * 0.9, (0.35, 0.25, 0.9), 0.20 * op)
    p.glow(cx, cy, R * 0.25, (1.0, 0.9, 1.0), 0.35 * op * (0.7 + 0.3 * math.sin(t * 5)))


def pant_asteroides(p, x0, y0, x1, y1, t, op=1.0, color=(0.85, 0.92, 1.0)):
    """Nave triangular y rocas de alambre a la deriva (gráfico vectorial genérico)."""
    p.rect(x0, y0, x1, y1, (0.0, 0.0, 0.01), op)
    w_, h_ = x1 - x0, y1 - y0
    lw = max(2.0, h_ * 0.012)
    rng = np.random.default_rng(11)
    for k in range(7):
        bx, by, vx, vy, r, ph = rng.random(), rng.random(), rng.random() - 0.5, rng.random() - 0.5, 0.05 + rng.random() * 0.07, rng.random() * 6
        x = x0 + ((bx + vx * t * 0.12) % 1.0) * w_ * 0.9 + w_ * 0.05
        y = y0 + ((by + vy * t * 0.12) % 1.0) * h_ * 0.86 + h_ * 0.07
        n = 8
        pts = [(x + h_ * r * (0.75 + 0.35 * math.sin(k * 3 + j * 2.1)) * math.cos(ph + t * 0.4 + j * 2 * math.pi / n),
                y + h_ * r * (0.75 + 0.35 * math.sin(k * 3 + j * 2.1)) * math.sin(ph + t * 0.4 + j * 2 * math.pi / n)) for j in range(n)]
        p.polilinea(pts, lw, color, op * 0.9, cerrado=True, caps=False)
    cx, cy = x0 + w_ * 0.5, y0 + h_ * 0.52
    a = t * 1.3
    s = h_ * 0.07
    nave = [rotp(cx, cy, s, a), rotp(cx, cy, s * 0.8, a + 2.5), rotp(cx, cy, s * 0.3, a + math.pi), rotp(cx, cy, s * 0.8, a - 2.5)]
    p.polilinea(nave, lw, color, op, cerrado=True, caps=False)
    u = (t * 1.6) % 1.0
    p.circ(*rotp(cx, cy, s + u * h_ * 0.4, a), lw * 0.9, color, op * (1 - u))
    p.texto(f"{int(t * 137) % 100000:05d}", x0 + w_ * 0.16, y0 + h_ * 0.09, h_ * 0.07, color, "mono", op * 0.9)


def pant_tunel(p, x0, y0, x1, y1, t, op=1.0, color=CIAN):
    """Túnel geométrico de alambre con figuras que suben por los carriles (gráfico vectorial genérico)."""
    p.rect(x0, y0, x1, y1, (0.0, 0.0, 0.012), op)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    R = min(x1 - x0, y1 - y0) / 2 * 0.92
    lw = max(2.0, R * 0.016)
    n = 14
    a0 = 0.12 * math.sin(t * 0.7)
    ext = [rotp(cx, cy, R * (0.92 + 0.08 * math.cos(3 * (a0 + k * 2 * math.pi / n))), a0 + k * 2 * math.pi / n) for k in range(n)]
    inn = [rotp(cx + R * 0.05 * math.sin(t), cy + R * 0.12, R * 0.16, a0 + k * 2 * math.pi / n) for k in range(n)]
    p.polilinea(ext, lw, color, op, cerrado=True, caps=False)
    p.polilinea(inn, lw * 0.7, color, op * 0.8, cerrado=True, caps=False)
    for k in range(n):
        p.linea(ext[k], inn[k], lw * 0.6, color, op * 0.6, caps=False)
    for k in range(5):                                     # figuras que suben
        c = (k * 3 + int(t * 0.3)) % n
        u = (t * 0.35 + k * 0.23) % 1.0
        a_, b_ = inn[c], ext[c]
        a2, b2 = inn[(c + 1) % n], ext[(c + 1) % n]
        q0 = (a_[0] + (b_[0] - a_[0]) * u, a_[1] + (b_[1] - a_[1]) * u)
        q1 = (a2[0] + (b2[0] - a2[0]) * u, a2[1] + (b2[1] - a2[1]) * u)
        m = ((q0[0] + q1[0]) / 2, (q0[1] + q1[1]) / 2)
        d = R * 0.06 * (0.4 + u)
        p.polilinea([q0, (m[0], m[1] - d), q1, (m[0], m[1] + d)], lw, (1.0, 0.25, 0.25), op, cerrado=True, caps=False)
    c = int(t * 2.2) % n                                   # el jugador en el borde
    m = ((ext[c][0] + ext[(c + 1) % n][0]) / 2, (ext[c][1] + ext[(c + 1) % n][1]) / 2)
    p.polilinea([ext[c], (m[0] + (m[0] - cx) * 0.10, m[1] + (m[1] - cy) * 0.10), ext[(c + 1) % n]], lw * 1.6, AMBAR, op, caps=False)


def pant_tanque(p, x0, y0, x1, y1, t, op=1.0, color=VERDE, mira=True):
    """Campo de batalla de alambre visto desde un tanque: horizonte, montañas, volcán, un tanque enemigo y la mira (dibujo propio)."""
    p.rect(x0, y0, x1, y1, (0.0, 0.012, 0.004), op)
    w_, h_ = x1 - x0, y1 - y0
    lw = max(2.0, h_ * 0.010)
    hy = y0 + h_ * 0.52
    off = (t * 0.05) % 1.0
    p.linea((x0, hy), (x1, hy), lw, color, op, caps=False)
    for k in range(-1, 6):                                 # montañas que se desplazan al girar
        bx = x0 + ((k / 5 - off) % 1.2 - 0.1) * w_
        pts = [(bx, hy), (bx + w_ * 0.07, hy - h_ * (0.10 + 0.05 * (k % 3))), (bx + w_ * 0.12, hy - h_ * 0.04), (bx + w_ * 0.18, hy - h_ * (0.14 - 0.03 * (k % 2))),
               (bx + w_ * 0.25, hy)]
        pts = [(min(max(x, x0), x1), y) for x, y in pts]
        p.polilinea(pts, lw * 0.8, color, op * 0.8, caps=False)
    # tanque enemigo de alambre (caja + torreta + cañón), se acerca y se aleja
    s = h_ * (0.10 + 0.05 * math.sin(t * 0.5))
    tx = x0 + w_ * (0.5 + 0.22 * math.sin(t * 0.33))
    ty = hy + h_ * 0.12
    casco = [(tx - s * 1.5, ty), (tx + s * 1.5, ty), (tx + s * 1.9, ty - s * 0.45), (tx - s * 1.9, ty - s * 0.45)]
    p.polilinea(casco, lw, color, op, cerrado=True, caps=False)
    p.polilinea([(tx - s * 1.9, ty - s * 0.45), (tx - s * 1.3, ty - s * 0.75), (tx + s * 1.3, ty - s * 0.75), (tx + s * 1.9, ty - s * 0.45)], lw, color, op, caps=False)
    p.polilinea([(tx - s * 0.6, ty - s * 0.75), (tx - s * 0.4, ty - s * 1.15), (tx + s * 0.6, ty - s * 1.15), (tx + s * 0.8, ty - s * 0.75)], lw, color, op, caps=False)
    p.linea((tx + s * 0.5, ty - s * 0.95), (tx + s * 2.4, ty - s * 1.0), lw, color, op, caps=False)
    for k in range(5):                                     # líneas del suelo en perspectiva
        u = ((k / 5 + t * 0.25) % 1.0) ** 2
        yy = hy + (y1 - hy) * u
        p.linea((x0 + w_ * 0.5 - w_ * 0.5 * u, yy), (x0 + w_ * 0.5 + w_ * 0.5 * u, yy), lw * 0.5, color, op * 0.35, caps=False)
    if mira:
        mx, my = x0 + w_ * 0.5, hy + h_ * 0.02
        g = h_ * 0.07
        col = (1.0, 0.3, 0.2) if abs(tx - mx) < w_ * 0.05 else color
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p.linea((mx + dx * g * 0.4, my + dy * g * 0.4), (mx + dx * g, my + dy * g), lw, col, op, caps=False)


# ------------------------------------------------------------------------------------------------ cabinas
def cabina(p, x, y, h, t=0.0, pantalla=None, color=CAB, borde=CAB2, marq=None, luz=CIAN, op=1.0, encendida=True, rotulo=None):
    """Cabina de frente. (x, y) = centro del suelo. Devuelve el rectángulo de la pantalla."""
    w = h * 0.40
    p.elip(x, y + h * 0.01, w * 0.75, h * 0.035, 0, (0, 0, 0), 0.55 * op)                       # sombra en el suelo
    p.poly([(x - w * 0.50, y), (x + w * 0.50, y), (x + w * 0.50, y - h * 0.42), (x + w * 0.56, y - h * 0.50), (x + w * 0.50, y - h * 0.58),
            (x + w * 0.50, y - h), (x - w * 0.50, y - h), (x - w * 0.50, y - h * 0.58), (x - w * 0.56, y - h * 0.50), (x - w * 0.50, y - h * 0.42)], color, op)
    p.rect(x - w * 0.50, y - h, x - w * 0.44, y, borde, 0.9 * op)                                 # cantos
    p.rect(x + w * 0.44, y - h, x + w * 0.50, y, borde, 0.9 * op)
    # marquesina
    mq = marq if marq is not None else mix(luz, (0, 0, 0), 0.25)
    p.rect(x - w * 0.42, y - h * 0.975, x + w * 0.42, y - h * 0.875, mq if encendida else mix(mq, (0, 0, 0), 0.85), op)
    if rotulo:
        p.texto(rotulo, x, y - h * 0.925, h * 0.050, (0.02, 0.02, 0.03) if encendida else (0.2, 0.2, 0.22), "sans_b", op)
    if encendida:
        p.glow(x, y - h * 0.925, w * 0.9, mq, 0.35 * op)
    # pantalla (bisel)
    sx0, sy0, sx1, sy1 = x - w * 0.36, y - h * 0.83, x + w * 0.36, y - h * 0.54
    p.rect(sx0 - w * 0.05, sy0 - h * 0.02, sx1 + w * 0.05, sy1 + h * 0.02, (0.0, 0.0, 0.0), op)
    if encendida and pantalla:
        pantalla(p, sx0, sy0, sx1, sy1, t, op)
    elif encendida:
        p.rect(sx0, sy0, sx1, sy1, mix(luz, (0, 0, 0), 0.82), op)
    else:
        p.rect(sx0, sy0, sx1, sy1, (0.02, 0.022, 0.03), op)
        p.poly([(sx0, sy0), (sx0 + (sx1 - sx0) * 0.5, sy0), (sx0, sy0 + (sy1 - sy0) * 0.6)], (0.5, 0.55, 0.65), 0.06 * op)   # reflejo
    # panel de mandos
    p.poly([(x - w * 0.56, y - h * 0.50), (x + w * 0.56, y - h * 0.50), (x + w * 0.50, y - h * 0.42), (x - w * 0.50, y - h * 0.42)], borde, op)
    p.linea((x - w * 0.22, y - h * 0.47), (x - w * 0.22 + w * 0.03 * math.sin(t * 6), y - h * 0.515), h * 0.012, (0.6, 0.6, 0.65), op)
    p.circ(x - w * 0.22 + w * 0.03 * math.sin(t * 6), y - h * 0.52, h * 0.016, (0.9, 0.15, 0.15), op)
    for k, c in enumerate(((0.95, 0.2, 0.2), (0.95, 0.85, 0.2), (0.3, 0.6, 1.0))):
        p.circ(x + w * (0.08 + 0.13 * k), y - h * 0.465, h * 0.013, c if encendida else mix(c, (0, 0, 0), 0.7), op)
    # puerta de monedas
    p.rect(x - w * 0.16, y - h * 0.34, x + w * 0.16, y - h * 0.16, (0.09, 0.09, 0.11), op)
    for dx in (-0.07, 0.07):
        p.rect(x + w * (dx - 0.035), y - h * 0.30, x + w * (dx + 0.035), y - h * 0.22, (0.75, 0.25, 0.1) if encendida else (0.2, 0.1, 0.08), op)
    if encendida:
        p.glow((sx0 + sx1) / 2, (sy0 + sy1) / 2, w * 1.5, luz, 0.22 * op)
    return sx0, sy0, sx1, sy1


def cabina_lado(p, x, y, h, f=1, t=0.0, color=CAB, luz=CIAN, op=1.0, encendida=True, amt=1.0):
    """Cabina de PERFIL; f = +1 la pantalla mira a la derecha. (x, y) = suelo bajo el centro. Devuelve el punto de la pantalla (foco de luz)."""
    d = h * 0.36
    xb, xf = x - f * d * 0.5, x + f * d * 0.5
    p.elip(x, y + h * 0.01, d * 0.8, h * 0.03, 0, (0, 0, 0), 0.5 * op)
    p.poly([(xb, y), (xf - f * d * 0.10, y), (xf - f * d * 0.10, y - h * 0.44), (xf + f * d * 0.22, y - h * 0.50), (xf + f * d * 0.22, y - h * 0.545),
            (xf - f * d * 0.22, y - h * 0.58), (xf - f * d * 0.40, y - h * 0.84), (xf + f * d * 0.10, y - h * 0.88), (xf + f * d * 0.10, y - h),
            (xb, y - h)], color, op)
    p.linea((xb + f * 4, y - h + 4), (xb + f * 4, y - 4), 4, mix(color, (0.3, 0.32, 0.4), 0.5), 0.8 * op)       # canto trasero
    sx, sy = xf - f * d * 0.31, y - h * 0.71
    if encendida:
        p.polilinea([(xf - f * d * 0.24, y - h * 0.60), (xf - f * d * 0.38, y - h * 0.82)], h * 0.018, luz, op)
        p.rect(min(xf - f * d * 0.38, xf + f * d * 0.08), y - h * 0.975, max(xf - f * d * 0.38, xf + f * d * 0.08), y - h * 0.895, mix(luz, (1, 1, 1), 0.2), 0.9 * op)
        p.haz(sx, sy, 0 if f > 0 else 180, h * 0.95, 70, luz, 0.30 * amt * op)
        p.glow(sx, sy, h * 0.42, luz, 0.38 * amt * op)
    return sx, sy


def jugador(p, x, y, h, t, f=1, color=SIL, pelo="corto", ritmo=1.0, alpha=1.0, lean=0.10):
    """Chico de pie jugando: brazos al panel, cabeza que sigue la pantalla, peso que cambia de pierna."""
    b = math.sin(t * 7.0 * ritmo)
    pose = dict(ll=(0.10 + 0.03 * math.sin(t * 1.3), 0.05), lr=(-0.12, 0.02), bl=(0.95 + 0.06 * b, 0.75), br=(1.05 - 0.07 * b, 0.60),
                lean=lean + 0.015 * math.sin(t * 2.1), head=0.18 + 0.04 * math.sin(t * 3.0), drop=0.004 * abs(b))
    return persona(p, x, y, h, pose, color, f, pelo=pelo, alpha=alpha)


def luz_cara(p, j, x, y, f, luz, h, amt=0.5):
    """Borde de luz de pantalla sobre cabeza y pecho de un jugador (j = articulaciones devueltas por persona)."""
    hx, hy = x + f * j["hd"][0], y - j["hd"][1]
    p.elip(hx + f * j["rc"] * 0.55, hy, j["rc"] * 0.42, j["rc"] * 0.95, 0, luz, amt)
    cx, cy = x + f * j["cu"][0], y - j["cu"][1]
    p.linea((cx + f * h * 0.085, cy + h * 0.03), (cx + f * h * 0.065, cy + h * 0.20), h * 0.014, luz, amt * 0.7)


def moqueta(p, y, t=0.0, col_a=(0.110, 0.060, 0.150), col_b=(0.060, 0.110, 0.190), f=700.0, cam=0.0):
    """Suelo de salón recreativo: moqueta de rombos en perspectiva."""
    p.rect(-10, y, W + 10, H + 10, col_a, grad=(mix(col_a, (0, 0, 0), 0.3), col_a))
    for k in range(1, 9):
        yy = y + (H - y) * (k / 8) ** 1.7
        p.linea((0, yy), (W, yy), 2 + k * 0.4, col_b, 0.7, caps=False)
    for k in range(-14, 15):
        xs = W / 2 + k * 190 - cam
        p.linea((W / 2 + (xs - W / 2) * 0.35, y), (W / 2 + (xs - W / 2) * 2.4, H + 10), 3, col_b, 0.6, caps=False)


def neon(p, txt, x, y, px, color, t, fase=0.0, fnt="sans_b", parpadea=True):
    k = 1.0
    if parpadea:
        s = math.sin(t * 2.3 + fase) + math.sin(t * 7.1 + fase * 2)
        k = 0.35 if s > 1.72 else 1.0
    p.texto(txt, x, y, px, mix(color, (1, 1, 1), 0.55), fnt, k)
    p.glow(x, y, px * 0.6 * max(2, len(txt)) * 0.5, color, 0.30 * k)


def salon(p, t, y_suelo=780, cam=0.0, n=7, luz=1.0, hueco=None, neones=True, vivas=True):
    """Fondo de salón recreativo: pared oscura con neones, fila de cabinas al fondo con sus pantallas y moqueta. `hueco` = índice sin cabina."""
    p.fondo((0.045, 0.028, 0.085), (0.120, 0.070, 0.170))
    for k in range(0, W + 1, 240):                                                       # paneles de la pared
        p.rect(k - cam * 0.3 % 240, 0, k - cam * 0.3 % 240 + 4, y_suelo, (0.0, 0.0, 0.0), 0.25)
    p.rect(0, y_suelo - 470, W, y_suelo - 460, (0.75, 0.25, 0.95), 0.55 * luz)          # tira de neón
    p.glow(W / 2, y_suelo - 465, 1500, (0.45, 0.15, 0.65), 0.16 * luz)
    if neones:
        neon(p, "ARCADE", 380 - cam * 0.3, 150, 120, MAG, t, 0.0)
        neon(p, "GAMES", 1500 - cam * 0.3, 190, 100, CIAN, t, 2.0)
        neon(p, "25¢", 960 - cam * 0.3, 110, 70, AMBAR, t, 4.0)
    moqueta(p, y_suelo, t, cam=cam)
    pant = (pant_asteroides, pant_tunel, pant_tanque, None, pant_asteroides, pant_tunel, None, pant_tanque)
    for k in range(n):
        if hueco is not None and k == hueco:
            continue
        x = (k + 0.5) / n * (W + 300) - 150 - cam * 0.6
        col = NEON[(k * 2 + 1) % 6]
        cabina(p, x, y_suelo + 6, 430, t + k, pant[k % 8] if vivas else None, color=(0.060, 0.062, 0.085), borde=(0.11, 0.115, 0.15), luz=col, op=1.0)
        p.elip(x, y_suelo + 70, 150, 34, 0, col, 0.10 * luz)                            # charco de luz en la moqueta
    p.rect(0, 0, W, H, (0.0, 0.0, 0.02), 0.10 + 0.30 * (1 - luz))                     # el fondo queda en penumbra
