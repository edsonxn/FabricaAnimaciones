# -*- coding: utf-8 -*-
"""Objetos dibujados para los motion graphics (relojes, calendarios, balanza, mazo, camilla, jeringas, monitor, ambulancia, celdas...).
Todos reciben el pintor `p` (mg.P) y coordenadas del cuadro final 1920x1080; el movimiento sale del tiempo `t` o de un progreso `u` (0..1)."""
import json
import math
import os

import numpy as np

from mg import *  # noqa: F401,F403


def rot(c, ang):
    ca, sa = math.cos(ang), math.sin(ang)
    return lambda q: (c[0] + (q[0] - c[0]) * ca - (q[1] - c[1]) * sa, c[1] + (q[0] - c[0]) * sa + (q[1] - c[1]) * ca)


# ---------------------------------------------------------------- relojes y calendarios
def reloj(p, cx, cy, r, t, h=6.0, m=40.0, segundero=True, cara=CREMA, vel_min=0.0, borde=(0.05, 0.05, 0.06), op=1.0):
    """Reloj de pared. `vel_min`: minutos de reloj que avanzan por segundo de video (para acelerarlo)."""
    p.glow(cx, cy, r * 1.9, (0.35, 0.42, 0.6), 0.22 * op)
    p.circ(cx, cy, r * 1.07, borde, op)
    p.circ(cx, cy, r, cara, op)
    p.circ(cx, cy, r * 0.94, mix(cara, (1, 1, 1), 0.35), op)
    for k in range(60):
        a = k / 60 * 2 * math.pi
        big = k % 5 == 0
        r0, r1 = (r * 0.80, r * 0.92) if big else (r * 0.87, r * 0.92)
        p.linea((cx + r0 * math.sin(a), cy - r0 * math.cos(a)), (cx + r1 * math.sin(a), cy - r1 * math.cos(a)), r * (0.035 if big else 0.015), (0.1, 0.1, 0.12), op, caps=False)
    mm = m + t * vel_min
    ah, am = ((h + mm / 60) % 12) / 12 * 2 * math.pi, (mm % 60) / 60 * 2 * math.pi
    p.linea((cx, cy), (cx + r * 0.50 * math.sin(ah), cy - r * 0.50 * math.cos(ah)), r * 0.065, (0.07, 0.07, 0.09), op)
    p.linea((cx, cy), (cx + r * 0.74 * math.sin(am), cy - r * 0.74 * math.cos(am)), r * 0.045, (0.07, 0.07, 0.09), op)
    if segundero:
        s = int(t) + ease_back(t % 1.0 * 1.6) if (t % 1.0) < 0.625 else int(t) + 1.0
        a = (s % 60) / 60 * 2 * math.pi
        p.linea((cx - r * 0.14 * math.sin(a), cy + r * 0.14 * math.cos(a)), (cx + r * 0.84 * math.sin(a), cy - r * 0.84 * math.cos(a)), r * 0.018, ROJO, op)
    p.circ(cx, cy, r * 0.06, ROJO, op)


def hoja_cal(p, cx, cy, w, h, mes, dia, u=0.0, color=CREMA, tinta=(0.12, 0.10, 0.10), rojo_u=0.0):
    """Hoja de calendario. u 0..1 = la hoja se arranca hacia arriba. `rojo_u` dibuja un círculo rojo alrededor del día."""
    x0, x1, y0 = cx - w / 2, cx + w / 2, cy - h / 2
    p.rect(x0 + 10, y0 + 14, x1 + 10, y0 + h + 14, (0, 0, 0), 0.35)
    p.rect(x0, y0 - h * 0.12, x1, y0 + h, (0.85, 0.12, 0.12), grad=((0.85, 0.12, 0.12), (0.6, 0.06, 0.06)))
    hh = h * max(0.0, math.cos(u * math.pi / 2))
    if hh > 4:
        p.rect(x0, y0, x1, y0 + hh, color, grad=(mix(color, (1, 1, 1), 0.3), mix(color, (0.6, 0.55, 0.45), u)))
        for k in range(6):
            p.circ(x0 + w * (0.12 + k * 0.152), y0 + 6, 7, (0.25, 0.22, 0.2))
        if hh > h * 0.55:
            p.texto(mes, cx, y0 + h * 0.15, h * 0.12, (0.85, 0.12, 0.12), "sans_b", 1 - u)
            p.texto(dia, cx, y0 + h * 0.58, h * 0.46, tinta, "serif", 1 - u)
            if rojo_u > 0:
                p.elip(cx, y0 + h * 0.58, w * 0.30, h * 0.30, -8, ROJO, 0.9 * rojo_u, a0=0, a1=int(360 * rojo_u)) if False else None
                n = int(40 * rojo_u)
                if n > 1:
                    pts = [(cx + w * 0.33 * math.cos(-0.5 + k / 40 * 6.4), y0 + h * 0.58 + h * 0.31 * math.sin(-0.5 + k / 40 * 6.4)) for k in range(n)]
                    p.polilinea(pts, 9, ROJO, 0.95)


def rodillo(p, cx, cy, desde, hasta, u, px, color=ROJO, fnt="abril"):
    """Contador tipo odómetro (cada dígito que cambia se desliza). u 0..1."""
    v = lerp(desde, hasta, ease_out(u))
    iv = int(v)
    fr = v - iv
    a, b = f"{iv}", f"{iv + 1}"
    n = len(a)
    ancho = px * 0.62
    x0 = cx - ancho * n / 2 + ancho / 2
    for i in range(n):
        xi = x0 + i * ancho
        if a[i] == b[i] or fr < 0.001:
            p.texto(a[i], xi, cy, px, color, fnt)
        else:
            p.texto(a[i], xi, cy - fr * px * 0.8, px, color, fnt, 1 - fr)
            p.texto(b[i], xi, cy + (1 - fr) * px * 0.8, px, color, fnt, fr)


# ---------------------------------------------------------------- justicia
def balanza(p, cx, cy, esc, tilt=0.0, color=CREMA, op=1.0, t=0.0):
    """Balanza de la justicia (cy = pivote superior). tilt en radianes (+ = baja la derecha)."""
    p.poly([(cx - esc * 0.18, cy + esc * 0.92), (cx + esc * 0.18, cy + esc * 0.92), (cx + esc * 0.10, cy + esc * 0.82), (cx - esc * 0.10, cy + esc * 0.82)], color, op)
    p.rect(cx - esc * 0.025, cy, cx + esc * 0.025, cy + esc * 0.84, color, op)
    p.circ(cx, cy, esc * 0.05, color, op)
    L = esc * 0.50
    el = (cx - L * math.cos(tilt), cy - L * math.sin(tilt))
    er = (cx + L * math.cos(tilt), cy + L * math.sin(tilt))
    p.linea(el, er, esc * 0.02, color, op)
    for e in (el, er):
        pan = (e[0], e[1] + esc * 0.42)
        p.linea(e, (pan[0] - esc * 0.17, pan[1]), esc * 0.008, color, op, caps=False)
        p.linea(e, (pan[0] + esc * 0.17, pan[1]), esc * 0.008, color, op, caps=False)
        pts = [(pan[0] + esc * 0.19 * math.cos(a), pan[1] + esc * 0.07 * math.sin(a)) for a in np.linspace(0, math.pi, 14)]
        p.poly(pts, color, op)


def mazo(p, x, y, esc, u, color=(0.34, 0.19, 0.10), bloque=(0.24, 0.13, 0.07), op=1.0):
    """Mazo de juez; u: 0 = en alto, 1 = golpe. (x, y) = parte superior del bloque, centro."""
    E = esc
    p.rrect(x - E * 0.34, y, x + E * 0.34, y + E * 0.11, E * 0.03, bloque, op)
    p.rect(x - E * 0.26, y - E * 0.03, x + E * 0.26, y, mix(bloque, (1, 1, 1), 0.14), op)
    hand = (x + E * 0.60, y - E * 0.17)
    ang = lerp(1.15, 0.0, ease_out(u))
    R = rot(hand, ang)
    hd = R((hand[0] - E * 0.60, hand[1]))
    p.polilinea([R((hand[0] + E * 0.12, hand[1])), hd], E * 0.045, (0.48, 0.30, 0.16), op)
    ca = R((hand[0] - E * 0.60 - E * 0.10, hand[1] - E * 0.20)), R((hand[0] - E * 0.60 + E * 0.10, hand[1] - E * 0.20)), R((hand[0] - E * 0.60 + E * 0.10, hand[1] + E * 0.20)), R((hand[0] - E * 0.60 - E * 0.10, hand[1] + E * 0.20))
    p.poly(ca, color, op)
    for dd in (-0.16, 0.16):
        p.poly([R((hand[0] - E * 0.60 - E * 0.105, hand[1] + E * (dd - 0.015))), R((hand[0] - E * 0.60 + E * 0.105, hand[1] + E * (dd - 0.015))),
                R((hand[0] - E * 0.60 + E * 0.105, hand[1] + E * (dd + 0.015))), R((hand[0] - E * 0.60 - E * 0.105, hand[1] + E * (dd + 0.015)))], (0.78, 0.60, 0.22), op)


def onda_choque(p, x, y, u, r=300, color=LUZ, op=0.7):
    if 0 < u < 1:
        p.polilinea([(x + r * u * math.cos(a) * 1.6, y + r * u * math.sin(a) * 0.5) for a in np.linspace(0, 2 * math.pi, 40)], 8 * (1 - u) + 1, color, op * (1 - u), cerrado=True)


def barrotes(p, x0, x1, y0, y1, n, grosor, color=SIL, u=1.0, escalonado=0.5, travesaños=(0.2, 0.8)):
    """Rejas verticales que caen desde arriba (u 0..1)."""
    for i in range(n):
        x = lerp(x0, x1, i / max(n - 1, 1))
        ui = ease_out((u - escalonado * (i / max(n - 1, 1))) / max(1 - escalonado, 1e-3))
        if ui > 0.001:
            p.rect(x - grosor / 2, y0 - (1 - ui) * (y1 - y0), x + grosor / 2, y0 + (y1 - y0) * ui * 0 + (y1 - y0) - (1 - ui) * (y1 - y0), color)
    if u > 0.6:
        for tr in travesaños:
            yy = lerp(y0, y1, tr)
            p.rect(x0 - grosor, yy - grosor * 0.6, x1 + grosor, yy + grosor * 0.6, color, smooth((u - 0.6) / 0.4))


def silla_electrica(p, x, y, esc, color=SIL, op=1.0):
    """Silueta de silla (solo contorno general): asiento, respaldo alto, brazos y patas."""
    p.rect(x - esc * 0.20, y - esc * 0.40, x + esc * 0.20, y - esc * 0.30, color, op)
    p.rect(x - esc * 0.20, y - esc * 1.05, x - esc * 0.10, y - esc * 0.30, color, op)
    p.rect(x - esc * 0.30, y - esc * 1.08, x - esc * 0.04, y - esc * 1.0, color, op)
    p.rect(x - esc * 0.26, y - esc * 0.62, x + esc * 0.24, y - esc * 0.57, color, op)
    for dx in (-0.18, 0.16):
        p.rect(x + esc * dx - esc * 0.025, y - esc * 0.30, x + esc * dx + esc * 0.025, y, color, op)
    p.rect(x + esc * 0.20, y - esc * 0.62, x + esc * 0.25, y - esc * 0.30, color, op)
    p.linea((x - esc * 0.08, y - esc * 1.0), (x + esc * 0.05, y - esc * 1.35), esc * 0.012, color, op)


# ---------------------------------------------------------------- camilla, jeringas, suero, monitor
def camilla(p, x, y, esc, color=(0.80, 0.82, 0.86), op=1.0, correas=True):
    """Camilla de lado (x, y = centro de la superficie)."""
    L = esc
    p.rrect(x - L * 0.5, y - L * 0.035, x + L * 0.5, y + L * 0.035, L * 0.03, color, op)
    p.rrect(x - L * 0.49, y - L * 0.075, x - L * 0.30, y - L * 0.03, L * 0.025, mix(color, (1, 1, 1), 0.2), op)
    p.rect(x - L * 0.46, y + L * 0.035, x - L * 0.43, y + L * 0.20, (0.2, 0.22, 0.25), op)
    p.rect(x + L * 0.43, y + L * 0.035, x + L * 0.46, y + L * 0.20, (0.2, 0.22, 0.25), op)
    p.rect(x - L * 0.46, y + L * 0.20, x + L * 0.46, y + L * 0.215, (0.2, 0.22, 0.25), op)
    for dx in (-0.42, 0.42):
        p.circ(x + L * dx, y + L * 0.245, L * 0.03, (0.08, 0.09, 0.1), op)
    if correas:
        for dx in (-0.12, 0.12, 0.34):
            p.rect(x + L * dx - L * 0.012, y - L * 0.085, x + L * dx + L * 0.012, y + L * 0.045, (0.55, 0.28, 0.12), op)


def jeringa(p, cx, cy, ang, esc, u=0.0, liquido=(0.95, 0.9, 0.35), op=1.0):
    """Jeringa en (cx, cy) apuntando a `ang` (rad; 0 = aguja a la derecha). u: 0 llena, 1 vacía (el émbolo avanza)."""
    R = rot((cx, cy), ang)
    L = esc
    barril = [R((cx - L * 0.30, cy - L * 0.06)), R((cx + L * 0.25, cy - L * 0.06)), R((cx + L * 0.25, cy + L * 0.06)), R((cx - L * 0.30, cy + L * 0.06))]
    p.poly(barril, (0.86, 0.9, 0.95), 0.9 * op)
    ll = lerp(0.55, 0.0, u)
    p.poly([R((cx - L * 0.30 + L * 0.55 * u, cy - L * 0.045)), R((cx + L * 0.25, cy - L * 0.045)), R((cx + L * 0.25, cy + L * 0.045)), R((cx - L * 0.30 + L * 0.55 * u, cy + L * 0.045))], liquido, 0.85 * op) if ll > 0.01 else None
    for k in range(8):
        xx = cx - L * 0.22 + k * L * 0.065
        p.linea(R((xx, cy - L * 0.06)), R((xx, cy - L * (0.03 if k % 2 else 0.0))), 2, (0.2, 0.25, 0.3), op, caps=False)
    p.linea(R((cx + L * 0.25, cy)), R((cx + L * 0.46, cy)), L * 0.012, (0.8, 0.82, 0.85), op)
    p.rect(*R((cx + L * 0.25, cy - L * 0.025)), *R((cx + L * 0.29, cy + L * 0.025)), (0.7, 0.72, 0.75), op) if False else None
    ex = L * 0.55 * u
    p.linea(R((cx - L * 0.30 + ex, cy)), R((cx - L * 0.50 + ex, cy)), L * 0.02, (0.55, 0.58, 0.62), op)
    p.linea(R((cx - L * 0.50 + ex, cy - L * 0.07)), R((cx - L * 0.50 + ex, cy + L * 0.07)), L * 0.025, (0.7, 0.72, 0.75), op)
    p.linea(R((cx - L * 0.30, cy - L * 0.075)), R((cx - L * 0.30, cy + L * 0.075)), L * 0.022, (0.7, 0.72, 0.75), op)


def bolsa_iv(p, x, y, esc, t, color=(0.85, 0.92, 0.95), liquido=(0.8, 0.85, 0.5), tubo_a=None, op=1.0):
    """Bolsa de suero colgada con tubo y goteo. (x, y) = gancho superior. tubo_a = punto final del tubo."""
    p.linea((x, y - esc * 0.30), (x, y), esc * 0.01, (0.6, 0.62, 0.65), op)
    p.rrect(x - esc * 0.10, y, x + esc * 0.10, y + esc * 0.36, esc * 0.04, color, 0.55 * op)
    p.rrect(x - esc * 0.085, y + esc * 0.10, x + esc * 0.085, y + esc * 0.35, esc * 0.035, liquido, 0.8 * op)
    cam = (x, y + esc * 0.50)
    p.rrect(cam[0] - esc * 0.025, cam[1] - esc * 0.05, cam[0] + esc * 0.025, cam[1] + esc * 0.07, esc * 0.015, color, 0.6 * op)
    gy = ((t * 0.9) % 1.0)
    p.circ(cam[0], cam[1] - esc * 0.03 + gy * esc * 0.09, esc * 0.01, liquido, op * (1 - gy * 0.3))
    fin = tubo_a or (x + esc * 0.25, y + esc * 1.4)
    pts = [(x, y + esc * 0.36), (x, y + esc * 0.46)] + [(x + (fin[0] - x) * s * s * (3 - 2 * s) * 0.9, y + esc * 0.58 + (fin[1] - y - esc * 0.58) * s) for s in np.linspace(0, 1, 14)]
    p.polilinea(pts, esc * 0.012, (0.75, 0.82, 0.85), 0.8 * op)
    return fin


def ecg(p, x0, y0, w, h, t, color=(0.35, 0.95, 0.60), vel=260.0, ritmo=1.1, irregular=0.0, grosor=5, op=1.0, plana=0.0):
    """Monitor cardiaco: línea que avanza con latidos; `plana` 0..1 la va aplanando."""
    n = 150
    xs = np.linspace(0, w, n)
    pts = []
    per = vel / max(ritmo, 0.1)
    for x in xs:
        ph = ((x - t * vel) / per) % 1.0
        # complejo PQRST
        y = 0.0
        y += 0.10 * math.exp(-((ph - 0.18) / 0.035) ** 2)
        y -= 0.12 * math.exp(-((ph - 0.36) / 0.012) ** 2)
        y += 1.00 * math.exp(-((ph - 0.40) / 0.012) ** 2)
        y -= 0.25 * math.exp(-((ph - 0.44) / 0.014) ** 2)
        y += 0.22 * math.exp(-((ph - 0.62) / 0.05) ** 2)
        y += irregular * 0.05 * math.sin(x * 0.2 + t * 13)
        pts.append((x0 + x, y0 - y * h * (1 - plana)))
    p.polilinea(pts, grosor * 2.2, color, 0.15 * op)
    p.polilinea(pts, grosor, color, op)
    p.glow(pts[-1][0], pts[-1][1], 60, color, 0.8 * op)


def monitor_marco(p, x0, y0, x1, y1, op=1.0):
    p.rrect(x0 - 18, y0 - 18, x1 + 18, y1 + 18, 26, (0.07, 0.08, 0.10), op)
    p.rrect(x0, y0, x1, y1, 14, (0.02, 0.05, 0.05), op)
    for k in range(1, 5):
        p.linea((x0, lerp(y0, y1, k / 5)), (x1, lerp(y0, y1, k / 5)), 1.5, (0.1, 0.25, 0.2), 0.5 * op, caps=False)


def ambulancia(p, x, y, esc, t, op=1.0, luces=True, dir=1):
    """Ambulancia de lado, (x, y) = suelo bajo el centro; esc = largo. dir=1 mira a la derecha."""
    L = esc
    f = dir

    def X(dx):
        return x + f * dx * L

    p.rrect(X(-0.5), y - L * 0.34, X(0.5) if f > 0 else X(0.5), y - L * 0.03, L * 0.03, (0.85, 0.87, 0.9), op) if f > 0 else p.rrect(X(0.5), y - L * 0.34, X(-0.5), y - L * 0.03, L * 0.03, (0.85, 0.87, 0.9), op)
    # cabina
    p.poly([(X(0.22), y - L * 0.34), (X(0.38), y - L * 0.34), (X(0.50), y - L * 0.19), (X(0.50), y - L * 0.03), (X(0.22), y - L * 0.03)], (0.80, 0.82, 0.86), op)
    p.poly([(X(0.26), y - L * 0.31), (X(0.36), y - L * 0.31), (X(0.45), y - L * 0.20), (X(0.26), y - L * 0.20)], (0.15, 0.22, 0.30), op)
    p.rect(min(X(-0.5), X(0.2)), y - L * 0.17, max(X(-0.5), X(0.2)), y - L * 0.12, (0.80, 0.12, 0.12), op)
    p.linea((X(-0.28), y - L * 0.29), (X(-0.28), y - L * 0.20), L * 0.03, (0.80, 0.12, 0.12), op)
    p.linea((X(-0.33), y - L * 0.245), (X(-0.23), y - L * 0.245), L * 0.03, (0.80, 0.12, 0.12), op)
    for dx in (-0.30, 0.33):
        p.circ(X(dx), y - L * 0.03, L * 0.07, (0.04, 0.04, 0.05), op)
        p.circ(X(dx), y - L * 0.03, L * 0.035, (0.5, 0.5, 0.55), op)
    if luces:
        a = (math.sin(t * 14) > 0)
        cr, ca = (1.0, 0.1, 0.1), (0.2, 0.4, 1.0)
        p.rect(X(0.0) - L * 0.12, y - L * 0.375, X(0.0) + L * 0.12, y - L * 0.34, (0.1, 0.1, 0.12), op) if f > 0 else None
        p.glow(X(-0.08), y - L * 0.36, L * 0.9, cr if a else ca, 0.9 * op)
        p.glow(X(0.08), y - L * 0.36, L * 0.9, ca if a else cr, 0.9 * op)
        p.circ(X(-0.08), y - L * 0.36, L * 0.022, cr if a else ca, op)
        p.circ(X(0.08), y - L * 0.36, L * 0.022, ca if a else cr, op)


# ---------------------------------------------------------------- persianas y cortinas (ventana de observación)
def persianas(p, x0, y0, x1, y1, abierto, n=18, color=(0.10, 0.11, 0.13)):
    """Láminas horizontales: abierto 0 = cerradas, 1 = abiertas (giran y quedan finas)."""
    hh = (y1 - y0) / n
    for i in range(n):
        ui = clamp((abierto * 1.25 - 0.25 * i / n))
        alto = hh * lerp(1.0, 0.10, smooth(ui))
        yy = y0 + i * hh
        p.rect(x0, yy, x1, yy + alto, color, 1.0, grad=(mix(color, (1, 1, 1), 0.10), color))


def cortina(p, x0, y0, x1, y1, abierto, color=(0.38, 0.06, 0.08), t=0.0):
    """Cortina con pliegues que se corre a los lados."""
    w = x1 - x0
    mitad = w / 2
    ancho = mitad * (1 - smooth(abierto)) + w * 0.035
    for lado in (-1, 1):
        xe = x0 + mitad + lado * (mitad - ancho) if lado < 0 else x0 + mitad + (mitad - ancho)
        xa, xb = (x0, x0 + ancho) if lado < 0 else (x1 - ancho, x1)
        p.rect(xa, y0, xb, y1, color)
        nf = max(2, int(ancho / 38))
        for k in range(nf):
            xx = lerp(xa, xb, (k + 0.5) / nf)
            p.rect(xx - 6, y0, xx + 6, y1, mix(color, (0, 0, 0), 0.5), 0.8)
            p.rect(xx + 6, y0, xx + 16, y1, mix(color, (1, 1, 1), 0.12), 0.7)
    p.rect(x0 - 20, y0 - 18, x1 + 20, y0 + 6, (0.2, 0.2, 0.22))


def ventana_obs(p, x0, y0, x1, y1, luz=(0.78, 0.84, 0.74), marco=(0.04, 0.05, 0.06)):
    p.rect(x0 - 28, y0 - 28, x1 + 28, y1 + 28, marco)
    p.rect(x0, y0, x1, y1, luz, grad=(mix(luz, (1, 1, 1), 0.15), mix(luz, (0, 0, 0), 0.25)))


# ---------------------------------------------------------------- oficina, vela, papeles
def escritorio_pc(p, x, y, esc, t, escribe=True, color_pantalla=(0.15, 0.85, 0.55)):
    """Escritorio con monitor CRT encendido y teclado. (x, y) = suelo bajo el centro del escritorio."""
    E = esc
    p.rect(x - E * 0.55, y - E * 0.42, x + E * 0.55, y - E * 0.38, (0.12, 0.08, 0.06))
    p.rect(x - E * 0.50, y - E * 0.38, x - E * 0.47, y, (0.12, 0.08, 0.06))
    p.rect(x + E * 0.47, y - E * 0.38, x + E * 0.50, y, (0.12, 0.08, 0.06))
    mx0, my0, mx1, my1 = x - E * 0.20, y - E * 0.92, x + E * 0.20, y - E * 0.50
    p.rrect(mx0 - 14, my0 - 14, mx1 + 14, my1 + 14, 16, (0.55, 0.55, 0.50))
    p.rect(x - E * 0.05, y - E * 0.50, x + E * 0.05, y - E * 0.42, (0.5, 0.5, 0.46))
    p.rect(mx0, my0, mx1, my1, (0.02, 0.07, 0.05))
    p.glow(x, (my0 + my1) / 2, E * 0.9, color_pantalla, 0.45)
    if escribe:
        for k in range(9):
            largo = (E * 0.34) * (0.35 + 0.65 * ((math.sin(k * 2.7) + 1) / 2))
            prog_ = clamp((t * 2.2 - k) * 0.8)
            if prog_ > 0:
                p.rect(mx0 + 20, my0 + 24 + k * (E * 0.038), mx0 + 20 + largo * prog_, my0 + 24 + k * (E * 0.038) + 9, color_pantalla, 0.85)
        if int(t * 2.5) % 2 == 0:
            p.rect(mx0 + 22, my0 + 24 + 9 * E * 0.038, mx0 + 46, my0 + 24 + 9 * E * 0.038 + 12, color_pantalla, 0.9)
    p.rrect(x - E * 0.20, y - E * 0.41, x + E * 0.20, y - E * 0.385, 6, (0.5, 0.5, 0.47))


def vela(p, x, y, esc, t, color_cera=(0.92, 0.86, 0.72), amt=1.0):
    """Vela encendida: cuerpo, mecha y llama que oscila. (x, y) = base."""
    E = esc
    p.glow(x, y - E * 1.05, E * 3.2, (1.0, 0.62, 0.22), 0.55 * amt)
    p.glow(x, y - E * 1.05, E * 1.4, (1.0, 0.8, 0.45), 0.55 * amt)
    p.rrect(x - E * 0.16, y - E * 0.9, x + E * 0.16, y, E * 0.03, color_cera, 1.0)
    p.rect(x - E * 0.16, y - E * 0.9, x + E * 0.16, y - E * 0.86, mix(color_cera, (1, 1, 1), 0.3))
    p.linea((x, y - E * 0.9), (x, y - E * 0.97), E * 0.018, (0.1, 0.08, 0.06))
    fl = math.sin(t * 9.0) * 0.06 + math.sin(t * 17.0 + 1) * 0.03
    tip = (x + E * fl, y - E * (1.38 + 0.04 * math.sin(t * 11)))
    p.poly([(x - E * 0.07, y - E * 0.98), (x - E * 0.05, y - E * 1.15), tip, (x + E * 0.05, y - E * 1.15), (x + E * 0.07, y - E * 0.98)], (1.0, 0.62, 0.15), 0.95)
    p.poly([(x - E * 0.035, y - E * 0.99), (x - E * 0.025, y - E * 1.08), (x + E * fl * 0.6, y - E * 1.24), (x + E * 0.025, y - E * 1.08), (x + E * 0.035, y - E * 0.99)], (1.0, 0.92, 0.6), 1.0)


def documento(p, cx, cy, w, h, ang=0.0, lineas=8, color=CREMA, tinta=(0.35, 0.33, 0.30), titulo=True, sombra=True, op=1.0):
    R = rot((cx, cy), ang)
    pts = [R((cx - w / 2, cy - h / 2)), R((cx + w / 2, cy - h / 2)), R((cx + w / 2, cy + h / 2)), R((cx - w / 2, cy + h / 2))]
    if sombra:
        p.poly([(q[0] + 14, q[1] + 18) for q in pts], (0, 0, 0), 0.35 * op)
    p.poly(pts, color, op)
    if titulo:
        p.poly([R((cx - w * 0.36, cy - h * 0.40)), R((cx + w * 0.10, cy - h * 0.40)), R((cx + w * 0.10, cy - h * 0.34)), R((cx - w * 0.36, cy - h * 0.34))], (0.15, 0.13, 0.12), op)
    for k in range(lineas):
        yy = cy - h * 0.26 + k * h * 0.70 / max(lineas - 1, 1)
        l = w * (0.78 if k % 4 != 3 else 0.5)
        p.poly([R((cx - w * 0.39, yy)), R((cx - w * 0.39 + l, yy)), R((cx - w * 0.39 + l, yy + h * 0.022)), R((cx - w * 0.39, yy + h * 0.022))], tinta, 0.8 * op)
    return pts


def lupa(p, x, y, r, ang=-0.8, color=(0.85, 0.88, 0.92), op=1.0):
    p.circ(x, y, r * 1.0, color, op)
    p.circ(x, y, r * 0.86, (0.10, 0.14, 0.2), 0.0)
    p.circ(x, y, r * 0.84, (0.65, 0.78, 0.9), 0.28 * op)
    ex, ey = x + r * 1.0 * math.cos(ang + math.pi), y + r * 1.0 * math.sin(ang + math.pi)
    p.linea((ex, ey), (ex + r * 1.0 * math.cos(ang + math.pi), ey + r * 1.0 * math.sin(ang + math.pi)), r * 0.28, (0.35, 0.22, 0.12), op)


def signo(p, x, y, txt, px, color=ROJO, t=0.0, u=1.0, fnt="abril"):
    """Signo grande que aparece con rebote (¿?, ✓...)."""
    s = ease_back(u)
    if s > 0.02:
        p.texto(txt, x, y + 8 * math.sin(t * 3), px * s, color, fnt, clamp(u * 3))


def check(p, x, y, r, u, color=(0.3, 0.95, 0.5), w=18):
    if u <= 0:
        return
    pts = [(x - r * 0.6, y), (x - r * 0.2, y + r * 0.5), (x + r * 0.7, y - r * 0.55)]
    n = u * 2.0
    if n < 1:
        q = [pts[0], (lerp(pts[0][0], pts[1][0], n), lerp(pts[0][1], pts[1][1], n))]
    else:
        q = [pts[0], pts[1], (lerp(pts[1][0], pts[2][0], n - 1), lerp(pts[1][1], pts[2][1], n - 1))]
    p.polilinea(q, w, color, 1.0)


def cruz(p, x, y, r, u, color=ROJO, w=18):
    if u <= 0:
        return
    a = min(1, u * 2)
    p.linea((x - r, y - r), (lerp(x - r, x + r, a), lerp(y - r, y + r, a)), w, color)
    if u > 0.5:
        b = (u - 0.5) * 2
        p.linea((x + r, y - r), (lerp(x + r, x - r, b), lerp(y - r, y + r, b)), w, color)


def cerebro(p, cx, cy, r, color=(0.85, 0.55, 0.60), grieta=0.0, t=0.0):
    p.elip(cx - r * 0.30, cy, r * 0.62, r * 0.78, 0, color)
    p.elip(cx + r * 0.30, cy, r * 0.62, r * 0.78, 0, mix(color, (1, 1, 1), 0.07))
    oscuro = mix(color, (0, 0, 0), 0.45)
    for s_ in (-1, 1):
        for k in range(4):
            yy = cy - r * 0.5 + k * r * 0.33
            pts = [(cx + s_ * (r * 0.1 + j * r * 0.14), yy + math.sin(j * 1.7 + k) * r * 0.08) for j in range(5)]
            p.polilinea(pts, r * 0.035, oscuro, 0.8)
    p.linea((cx, cy - r * 0.75), (cx, cy + r * 0.65), r * 0.03, oscuro, 0.9)
    p.rrect(cx - r * 0.09, cy + r * 0.6, cx + r * 0.09, cy + r * 1.05, r * 0.04, mix(color, (0, 0, 0), 0.2))
    if grieta > 0:
        rng = np.random.default_rng(4)
        pts = [(cx - r * 0.15, cy - r * 0.8)]
        for k in range(1, 9):
            pts.append((cx + (rng.random() - 0.5) * r * 0.5, cy - r * 0.8 + k * r * 0.2))
        n = max(2, int(len(pts) * grieta))
        p.polilinea(pts[:n], r * 0.045, (0.12, 0.02, 0.03), 1.0)


def nube(p, cx, cy, esc, color=(0.35, 0.38, 0.45), t=0.0, lluvia_=True, op=1.0):
    for dx, dy, rr in ((-0.5, 0.05, 0.38), (-0.15, -0.15, 0.5), (0.25, -0.05, 0.44), (0.6, 0.08, 0.34), (0.05, 0.12, 0.5)):
        p.circ(cx + dx * esc, cy + dy * esc, rr * esc, color, op)
    if lluvia_:
        for k in range(10):
            x = cx - esc * 0.8 + k * esc * 0.18
            y0 = cy + esc * 0.5 + ((t * 700 + k * 97) % (esc * 0.9))
            p.linea((x, y0), (x - 8, y0 + 34), 4, (0.55, 0.7, 0.95), 0.8 * op, caps=False)


def engranaje(p, cx, cy, r, ang, color=(0.40, 0.44, 0.50), dientes=10, op=1.0):
    pts = []
    for k in range(dientes * 2):
        a = ang + k / (dientes * 2) * 2 * math.pi
        rr = r if k % 2 == 0 else r * 0.80
        pts += [(cx + rr * math.cos(a - 0.08), cy + rr * math.sin(a - 0.08)), (cx + rr * math.cos(a + 0.08), cy + rr * math.sin(a + 0.08))]
    p.poly(pts, color, op)
    p.circ(cx, cy, r * 0.38, (0.05, 0.06, 0.08), op)


# ---------------------------------------------------------------- edificios
def columnas(p, cx, y, w, h, color=(0.80, 0.80, 0.78), sombra=SIL, n=6, op=1.0):
    """Frente de tribunal con frontón y columnas (y = base de las columnas)."""
    ch = h * 0.62
    p.poly([(cx - w * 0.52, y - ch - h * 0.06), (cx + w * 0.52, y - ch - h * 0.06), (cx, y - h)], color, op)
    p.rect(cx - w * 0.52, y - ch - h * 0.06, cx + w * 0.52, y - ch, mix(color, (0, 0, 0), 0.15), op)
    for i in range(n):
        xx = cx - w * 0.42 + i * w * 0.84 / (n - 1)
        p.rect(xx - w * 0.026, y - ch, xx + w * 0.026, y, color, op, grad=(mix(color, (1, 1, 1), 0.1), mix(color, (0, 0, 0), 0.25)))
        p.rect(xx - w * 0.036, y - ch, xx + w * 0.036, y - ch + h * 0.025, mix(color, (0, 0, 0), 0.1), op)
    for k in range(3):
        p.rect(cx - w * (0.55 + k * 0.03), y + k * h * 0.035, cx + w * (0.55 + k * 0.03), y + (k + 1) * h * 0.035, mix(color, (0, 0, 0), 0.25 + k * 0.1), op)


def prision(p, x, y, esc, t, color=SIL, ventanas=True, reflector=True, valla=True, amb=None):
    """Prisión de máxima seguridad en silueta: bloque con ventanas con barrotes, torre de vigilancia, alambre y haz de reflector. (x, y)=suelo, centro."""
    E = esc
    p.rect(x - E * 0.55, y - E * 0.42, x + E * 0.55, y, color)
    p.rect(x - E * 0.62, y - E * 0.30, x - E * 0.55, y, color)
    p.rect(x + E * 0.55, y - E * 0.30, x + E * 0.62, y, color)
    # torre
    tx = x + E * 0.32
    p.rect(tx - E * 0.035, y - E * 0.80, tx + E * 0.035, y - E * 0.42, color)
    p.poly([(tx - E * 0.09, y - E * 0.80), (tx + E * 0.09, y - E * 0.80), (tx + E * 0.07, y - E * 0.90), (tx - E * 0.07, y - E * 0.90)], color)
    p.poly([(tx - E * 0.10, y - E * 0.90), (tx + E * 0.10, y - E * 0.90), (tx, y - E * 0.96)], color)
    if ventanas:
        rng = np.random.default_rng(11)
        for r_ in range(2):
            for c in range(16):
                xx = x - E * 0.50 + c * E * 0.0675
                yy = y - E * 0.34 + r_ * E * 0.15
                if rng.random() < 0.28:
                    p.rect(xx, yy, xx + E * 0.034, yy + E * 0.07, (1.0, 0.82, 0.45), 0.75 + 0.2 * math.sin(t * 2 + c))
                else:
                    p.rect(xx, yy, xx + E * 0.034, yy + E * 0.07, (0.08, 0.10, 0.14), 0.9)
    if valla:
        for k in range(26):
            xx = x - E * 0.75 + k * E * 0.06
            p.rect(xx - 2, y - E * 0.13, xx + 2, y + E * 0.02, color)
        p.rect(x - E * 0.77, y - E * 0.13, x + E * 0.76, y - E * 0.115, color)
        pts = [(x - E * 0.77 + k * E * 0.03, y - E * (0.15 if k % 2 else 0.18)) for k in range(52)]
        p.polilinea(pts, 3, color, 0.9, caps=False)
    if reflector:
        ang = 90 + 55 * math.sin(t * 0.7)
        p.haz(tx, y - E * 0.85, ang, E * 1.3, 22, (1.0, 0.97, 0.85), 0.75)
        p.glow(tx, y - E * 0.85, E * 0.25, (1.0, 0.97, 0.85), 0.9)


def pasillo(p, t, cam=0.0, color_luz=(0.9, 0.95, 0.8), celdas=True, un_celda_luz=None, f=900.0):
    """Pasillo de celdas en perspectiva; la cámara avanza (cam = metros recorridos). Devuelve el centro del punto de fuga."""
    cx, cy = 960, 470
    a, b0, b1 = 1.6, 1.3, 1.6          # semiancho, suelo, techo
    p.fondo((0.02, 0.025, 0.03))

    def S(X, Y, Z):
        return (cx + X * f / Z, cy - Y * f / Z)
    # paredes/suelo/techo en tiras para dar degradado
    zs = np.arange(1.0, 40.0, 1.0)
    base = cam % 2.0
    for i in range(len(zs) - 1):
        z0, z1 = zs[i] - base, zs[i + 1] - base
        if z0 < 0.4:
            z0 = 0.4
        if z1 <= z0:
            continue
        sh = clamp(1.15 - (z0) / 22)
        luz = sh * (0.10 + 0.05 * math.sin(i * 1.3 + t * 0.9 * 0))
        for lado in (-1, 1):
            p.poly([S(lado * a, -b0, z0), S(lado * a, b1, z0), S(lado * a, b1, z1), S(lado * a, -b0, z1)], (luz * 0.9, luz, luz * 0.95))
        p.poly([S(-a, -b0, z0), S(a, -b0, z0), S(a, -b0, z1), S(-a, -b0, z1)], (luz * 0.7, luz * 0.75, luz * 0.8))
        p.poly([S(-a, b1, z0), S(a, b1, z0), S(a, b1, z1), S(-a, b1, z1)], (luz * 0.5, luz * 0.55, luz * 0.6))
    if celdas:
        for k in range(14):
            z = 2.0 + k * 2.0 - base
            if z < 0.6:
                continue
            sh = clamp(1.1 - z / 24)
            for lado in (-1, 1):
                z0, z1 = z, z + 1.3
                p.poly([S(lado * a, -b0, z0), S(lado * a, 0.8, z0), S(lado * a, 0.8, z1), S(lado * a, -b0, z1)], (0.03 * sh, 0.035 * sh, 0.04 * sh))
                # barrotes
                for q in range(5):
                    zz = z0 + (z1 - z0) * (q + 0.5) / 5
                    p.linea(S(lado * a, -b0, zz), S(lado * a, 0.8, zz), max(2, 11 / z), (0.32 * sh, 0.36 * sh, 0.38 * sh), 0.9, caps=False)
                p.linea(S(lado * a, 0.0, z0), S(lado * a, 0.0, z1), max(2, 10 / z), (0.32 * sh, 0.36 * sh, 0.38 * sh), 0.9, caps=False)
            # lámpara de techo
            zl = z + 0.6
            pl = S(0, b1 - 0.02, zl)
            flick = 0.55 + 0.45 * (math.sin(t * 7 + k * 3.1) > -0.7)
            p.glow(pl[0], pl[1] + 12 / zl * 6, 520 / zl, color_luz, 0.55 * sh * flick)
            p.rect(pl[0] - 120 / zl, pl[1] - 4, pl[0] + 120 / zl, pl[1] + 10 / zl * 3, (0.95 * sh * flick, 0.97 * sh * flick, 0.85 * sh * flick))
    if un_celda_luz is not None:
        z, lado = un_celda_luz
        zc = z - base if z - base > 0.6 else None
    p.glow(cx, cy, 180, (0.3, 0.38, 0.45), 0.4)
    return cx, cy


# ---------------------------------------------------------------- mapa de EE. UU. con arcos
_ESTADOS = {}


def _estados():
    if not _ESTADOS:
        ruta = os.path.join(os.getcwd(), "mapas", "ne_admin1.geojson")
        gj = json.load(open(ruta, encoding="utf-8"))
        for ft in gj["features"]:
            pr_ = ft["properties"]
            if pr_.get("adm0_a3") != "USA":
                continue
            g = ft["geometry"]
            polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
            _ESTADOS[pr_["name"]] = [np.array(poly[0], np.float32) for poly in polys]
    return _ESTADOS


def proy_us(lon, lat, caja=(160, 140, 1760, 940)):
    """Proyección sencilla (equirectangular corregida) del EE. UU. continental a una caja del cuadro."""
    x = (lon + 125.0) * math.cos(math.radians(38.0))
    y = (50.0 - lat)
    X = (24.5 * math.cos(math.radians(38.0)))
    Y = 26.0
    s = min((caja[2] - caja[0]) / X, (caja[3] - caja[1]) / Y)
    return caja[0] + x * s, caja[1] + y * s


def mapa_us(p, resaltar=(), color=(0.10, 0.17, 0.26), color_res=(0.35, 0.28, 0.12), borde=(0.28, 0.40, 0.55), caja=(160, 140, 1760, 940), op=1.0, zoom=None):
    """Dibuja los estados continentales; `resaltar` = nombres de estados en color destacado. zoom=(lon, lat, factor) acerca la vista."""
    for nombre, polys in _estados().items():
        if nombre in ("Alaska", "Hawaii"):
            continue
        res = nombre in resaltar
        for poly in polys:
            pts = [proy_us(lon, lat, caja) for lon, lat in poly]
            if zoom:
                cxz, cyz = proy_us(zoom[0], zoom[1], caja)
                pts = [(960 + (x - cxz) * zoom[2], 540 + (y - cyz) * zoom[2]) for x, y in pts]
            if max(q[0] for q in pts) < -50 or min(q[0] for q in pts) > W + 50:
                continue
            p.poly(pts, color_res if res else color, op)
            p.polilinea(pts, 3 if res else 2, mix(borde, ROJO, 0.0) if not res else CALIDO, op, cerrado=True, caps=False)


def arco(p, a, b, u, altura=260, color=CALIDO, w=6, punteado=True, op=1.0):
    """Arco punteado de a a b dibujado hasta u (0..1) con un punto brillante en la punta."""
    n = 40
    pts = []
    for k in range(int(n * u) + 1):
        s = k / n
        pts.append((lerp(a[0], b[0], s), lerp(a[1], b[1], s) - 4 * altura * s * (1 - s)))
    if len(pts) < 2:
        return
    if punteado:
        for i in range(0, len(pts) - 1, 2):
            p.linea(pts[i], pts[i + 1], w, color, op, caps=False)
    else:
        p.polilinea(pts, w, color, op)
    p.glow(pts[-1][0], pts[-1][1], 50, color, 0.9 * op)
    p.circ(pts[-1][0], pts[-1][1], w * 1.4, (1, 1, 1), op)


def pin(p, x, y, r, color=ROJO, t=0.0, pulso=True):
    if pulso:
        u = (t * 0.9) % 1.0
        p.elip(x, y, r * (1 + 3 * u), r * (1 + 3 * u) * 0.45, 0, color, 0.5 * (1 - u))
    p.poly([(x - r * 0.55, y - r * 1.9), (x + r * 0.55, y - r * 1.9), (x, y)], color)
    p.circ(x, y - r * 2.1, r * 0.95, color)
    p.circ(x, y - r * 2.1, r * 0.38, (0.1, 0.05, 0.05))
