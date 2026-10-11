# -*- coding: utf-8 -*-
"""Escenas dibujadas, parte 3: la noche del 30 de septiembre (frases 0-9 de la escena «noche»)."""
import math

import numpy as np

from mg_esc import *  # noqa: F401,F403
from mg_esc import ESC, esc, _cam, _sala, _lamp

N_ = "noche"


def A(fr, k, sep=0.0, nth=0):
    return ww(N_, fr, k, nth, sep)


def nota(p, x, y, s, color=CREMA, op=1.0):
    p.elip(x, y, 15 * s, 11 * s, -20, color, op)
    p.linea((x + 13 * s, y - 2 * s), (x + 13 * s, y - 62 * s), 4 * s, color, op, caps=False)
    p.poly([(x + 13 * s, y - 62 * s), (x + 44 * s, y - 46 * s), (x + 36 * s, y - 36 * s), (x + 13 * s, y - 48 * s)], color, op)


def interior(p, t, x0, y0, x1, y1, mover=0.0, brazo=1.0, vena=0.0):
    """Interior de la sala de ejecución visto desde la ventana: pared verdosa, camilla con la mujer, bolsa de suero, luz fría."""
    w, h = x1 - x0, y1 - y0
    p.rect(x0, y0, x1, y1, (0.62, 0.68, 0.60), grad=((0.72, 0.78, 0.70), (0.38, 0.43, 0.37)))
    p.rect(x0, y1 - h * 0.22, x1, y1, (0.30, 0.34, 0.30))
    p.glow(x0 + w * 0.5, y0 + 10, w * 0.8, (0.9, 1.0, 0.95), 0.4)
    camilla(p, x0 + w * 0.52, y1 - h * 0.34, w * 0.78, (0.90, 0.92, 0.95))
    acostada(p, x0 + w * 0.47, y1 - h * 0.44, w * 0.52, (0.07, 0.08, 0.11), t, brazo=brazo, mover=mover)
    p.rect(x0 + w * 0.10, y0 + h * 0.04, x0 + w * 0.104, y1 - h * 0.25, (0.35, 0.37, 0.4))
    bolsa_iv(p, x0 + w * 0.10, y0 + h * 0.06, h * 0.55, t, tubo_a=(x0 + w * 0.30, y1 - h * 0.43))
    p.rect(x1 - w * 0.12, y0 + h * 0.16, x1 - w * 0.04, y0 + h * 0.20, (0.15, 0.16, 0.18))        # teléfono / rótulo en la pared
    p.circ(x1 - w * 0.08, y0 + h * 0.12, 18, (0.12, 0.13, 0.15))


def sala_obs(p, t, abierto, cortinas=False, mover=0.0, rect=(430, 90, 1490, 640), publico=True, t_nube=None):
    x0, y0, x1, y1 = rect
    ventana_obs(p, x0, y0, x1, y1, (0.5, 0.55, 0.5))
    interior(p, t, x0, y0, x1, y1, mover=mover)
    if cortinas:
        cortina(p, x0, y0, x1, y1, abierto, t=t)
    else:
        persianas(p, x0, y0, x1, y1, abierto)
    if publico:
        for fila, (yy, hh, col) in enumerate(((880, 260, (0.006, 0.008, 0.012)), (1020, 340, (0.004, 0.005, 0.008)))):
            for i in range(8 if fila == 0 else 7):
                xx = 130 + i * 240 + (70 if fila else 0) + math.sin(t * 0.9 + i) * 5
                silueta_sentada_vista_trasera(p, xx, yy, hh * (0.85 + 0.25 * ((i * 37 % 10) / 10)), col)


# ====================================================================== 0: PRISIÓN
@esc("n_prision", lambda: INI(N_, 0), lambda: FIN(N_, 0))
def n_prision(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.006, 0.01, 0.025), (0.06, 0.08, 0.13), 0, 0.82)
    estrellas(p, t, 80, y_max=0.5, brillo=0.7)
    luna(p, 280, 170, 48, halo=0.8)
    colinas(p, 900, 160, (0.02, 0.03, 0.05), off=t * 2, seed=71)
    niebla(p, t, 960, 160, (0.35, 0.45, 0.6), 0.35, vel=8, seed=6)
    prision(p, 1150, 960, 1000, t)
    p.glow(1150, 940, 700, (1.0, 0.8, 0.45), 0.35)
    p.rect(-10, 960, W + 10, H + 10, (0.012, 0.016, 0.024))
    # testigos que caminan en fila hacia la puerta
    t0 = A(0, "testigos", -0.6)
    for k in range(7):
        x = lerp(-160 - k * 150, 1100, smooth(pr(t, t0 + 0.0, FIN(N_, 0) + 0.4)) ** 0.9)
        persona(p, x, 1030 + (k % 2) * 14, 380, pose_caminar(t * 5.0 + k * 0.9), (0.10, 0.11, 0.15), ropa="chaqueta" if k % 2 else "vestido", pelo="largo" if k % 3 == 0 else "corto")
    lluvia(p, t, 0.18, 60)
    vineta_p(p, 0.6)
    _cam(p, tl, dur, 1.0, 1.06, 0.6, 0.65)
    p.fin(lz)


# ====================================================================== 1: PERSIANAS SE ABREN (7:26)
@esc("n_persianas", lambda: INI(N_, 1), lambda: FIN(N_, 1))
def n_persianas(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.008, 0.012, 0.02), (0.03, 0.04, 0.06))
    ab = smooth(pr(t, A(1, "persianas", -0.2), A(1, "persianas", 0.9)))
    sala_obs(p, t, ab)
    p.glow(960, 360, 800, (0.7, 0.85, 0.75), 0.25 * ab)
    vineta_p(p, 0.6)
    _cam(p, tl, dur, 1.0, 1.09, 0.5, 0.35)
    p.fin(lz)


# ====================================================================== 2: ÚLTIMAS PALABRAS Y CANCIÓN
@esc("n_cancion", lambda: INI(N_, 2), lambda: FIN(N_, 2))
def n_cancion(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.02, 0.03, 0.05), (0.08, 0.10, 0.14), 0, 0.9)
    p.glow(900, 300, 900, (0.7, 0.85, 0.8), 0.35)
    suelo(p, 860, (0.05, 0.06, 0.08), (0.015, 0.02, 0.03))
    camilla(p, 860, 700, 1000, (0.88, 0.9, 0.93))
    acostada(p, 840, 640, 800, (0.06, 0.07, 0.10), t, brazo=0.7, resp=2.0)
    # consejero espiritual a su lado, con la mano apoyada
    persona(p, 1380, 900, 640, pose_señalar(0.12) | dict(br=(0.55, 0.55), bl=(0.1, 0.3)), (0.02, 0.025, 0.04), facing=-1, ropa="chaqueta", pelo="corto")
    # notas musicales que suben desde ella
    ts = A(2, "canto", -0.1)
    for k in range(9):
        u = ((t - ts) * 0.34 + k / 9) % 1.0 if t > ts else 2.0
        if u <= 1.0:
            nota(p, 700 + k * 60 + 30 * math.sin(u * 7 + k), 560 - u * 420, 1.1 + (k % 3) * 0.3, mix(CREMA, CALIDO, k / 9), 1 - u)
    p.glow(840, 630, 360, (1.0, 0.8, 0.5), 0.35 * smooth(pr(t, ts, ts + 1.0)))
    polvo(p, t, 40, op=0.35)
    vineta_p(p, 0.6)
    _cam(p, tl, dur, 1.0, 1.08, 0.5, 0.65)
    p.fin(lz)


# ====================================================================== 3: LA VENA A PUNTO DE REVENTAR
@esc("n_vena", lambda: INI(N_, 3), lambda: FIN(N_, 3))
def n_vena(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.04, 0.02, 0.03), (0.12, 0.05, 0.07), 0, 1.0)
    skin = (0.60, 0.40, 0.33)
    ph = pr(t, A(3, "vena", -0.4), A(3, "reventar", 0.2))
    lat = 1.0 + 0.04 * math.sin(t * 7.5) * (0.4 + ph)
    # antebrazo en primer plano, correa y vía
    p.poly([(-20, 400), (1950, 330), (1950, 890), (-20, 900)], skin, grad=((0.66, 0.45, 0.37), (0.34, 0.21, 0.17)))
    p.polilinea([(60, 640), (700, 620), (1300, 600), (1960, 590)], 56 * lat * (1 + 0.5 * ph), (0.22, 0.24, 0.45), 0.9)
    p.polilinea([(60, 640), (700, 620), (1300, 600), (1960, 590)], 20 * lat * (1 + 0.5 * ph), (0.40, 0.42, 0.72), 0.7)
    p.polilinea([(700, 620), (1180, 140)], 12, (0.82, 0.85, 0.9))                  # catéter entrando
    p.circ(1180, 140, 28, (0.75, 0.78, 0.84))
    p.rect(1130, 90, 1230, 130, (0.7, 0.72, 0.76))
    # dolor: ondas rojas desde el punto de punción
    for k in range(4):
        u = (t * 0.9 + k * 0.25) % 1.0
        if t > A(3, "quejo"):
            p.elip(700, 620, 40 + 380 * u, 28 + 180 * u, 0, ROJO, 0.45 * (1 - u) * (0.4 + ph))
    p.glow(700, 620, 520 * (0.4 + ph), (1.0, 0.25, 0.15), 0.6 * ph)
    # correa de la camilla y barras de latido
    p.rect(300, 780, 520, 880, (0.55, 0.28, 0.12), 0.95)
    ecg(p, 120, 980, 1100, 90, t, vel=300, ritmo=1.4 + ph, irregular=0.4, op=0.8)
    vineta_p(p, 0.65)
    _cam(p, tl, dur, 1.0, 1.1, 0.4, 0.55)
    p.fin(lz)


# ====================================================================== 4b: PRIMERA DOSIS (jeringa que se vacía hacia la vía)
@esc("n_jeringa", lambda: A(4, "pentobarbital", -0.8), lambda: FIN(N_, 4))
def n_jeringa(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.02, 0.03, 0.05), (0.07, 0.09, 0.13), 0, 1.0)
    p.glow(760, 540, 900, (0.5, 0.65, 0.9), 0.3)
    T0 = A(4, "pentobarbital", -0.8)
    u = smooth(pr(t, T0 + 0.4, FIN(N_, 4) - 0.6))
    jeringa(p, 560, 360, 0.0, 1100, u, (0.95, 0.9, 0.35))
    # tubo hacia el brazo + gotas que viajan
    pts = [(1120 + 140 * math.sin(s * 3), 360 + s * 420 + 20 * math.sin(s * 5)) for s in np.linspace(0, 1, 14)]
    pts = [(1140, 360)] + [(1140 + (1420 - 1140) * s + 90 * math.sin(s * 6), 360 + (700 - 360) * s) for s in np.linspace(0.05, 1, 14)]
    p.polilinea(pts, 14, (0.75, 0.82, 0.88), 0.7)
    for k in range(9):
        s = ((t * 0.35 + k / 9) % 1.0) * u
        if u > 0.02:
            i = min(len(pts) - 2, int(s * (len(pts) - 1)))
            f = s * (len(pts) - 1) - i
            q = (lerp(pts[i][0], pts[i + 1][0], f), lerp(pts[i][1], pts[i + 1][1], f))
            p.circ(q[0], q[1], 9, (0.95, 0.9, 0.35), 0.9)
    # brazo en el que entra
    p.poly([(1250, 760), (1920, 700), (1920, 960), (1250, 990)], (0.55, 0.37, 0.30), grad=((0.62, 0.42, 0.34), (0.30, 0.19, 0.15)))
    p.polilinea([(1300, 850), (1920, 800)], 26, (0.25, 0.27, 0.48), 0.9)
    p.circ(1420, 700, 16, (0.9, 0.9, 0.95))
    p.glow(1560, 840, 320, (0.95, 0.9, 0.35), 0.5 * u)
    p.texto("1.ª DOSIS · PENTOBARBITAL", 760, 880, 52, CREMA, "sans_b", smooth(pr(t, T0 + 0.2, T0 + 0.8)))
    polvo(p, t, 30, op=0.3)
    vineta_p(p, 0.6)
    _cam(p, tl, dur, 1.0, 1.06, 0.6, 0.5)
    p.fin(lz)


# ====================================================================== 5: CIERRAN Y VUELVEN A ABRIR — SIGUE MOVIÉNDOSE
@esc("n_reabre", lambda: INI(N_, 5), lambda: FIN(N_, 5))
def n_reabre(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.008, 0.012, 0.02), (0.03, 0.04, 0.06))
    c, a = A(5, "cerraron", -0.1), A(5, "abrieron", 0.1)
    ab = 1.0 - smooth(pr(t, c, c + 0.8)) + smooth(pr(t, a, a + 0.9))
    ab = clamp(ab)
    sala_obs(p, t, ab, mover=smooth(pr(t, a + 0.4, a + 1.2)) * 1.6)
    p.glow(960, 360, 800, (0.7, 0.85, 0.75), 0.25 * ab)
    vineta_p(p, 0.6)
    _cam(p, tl, dur, 1.0, 1.08, 0.5, 0.35)
    p.fin(lz)


# ====================================================================== 6: SEGUNDA DOSIS, CINCO MINUTOS
@esc("n_cuenta", lambda: INI(N_, 6), lambda: FIN(N_, 6))
def n_cuenta(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.015, 0.02, 0.04), (0.07, 0.09, 0.14))
    p.glow(560, 560, 900, (0.45, 0.55, 0.85), 0.35)
    T0 = A(6, "cinco", -0.1)
    segs = (t - T0) * 60.0 / 5.0 * (5.0 / max(A(6, "viva", 0.2) - T0, 1.0)) if t > T0 else 0.0
    reloj(p, 560, 560, 340, 0.0, h=7.0, m=segs / 6.0, segundero=True, cara=(0.86, 0.88, 0.92))
    tu = A(6, "segunda", -0.1)
    ya = ease_out(pr(t, tu, tu + 0.8))
    jeringa(p, lerp(2400, 1380, ya), 640, math.pi, 780, smooth(pr(t, A(6, "hizo", -1.2), A(6, "hizo", 0.2))), (0.95, 0.9, 0.35))
    vineta_p(p, 0.55)
    _cam(p, tl, dur, 1.0, 1.06)
    p.fin(lz)


# ====================================================================== 7: CORTINAS, RONQUIDOS, PERIODISTAS
@esc("n_ronca", lambda: INI(N_, 7), lambda: FIN(N_, 7))
def n_ronca(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.008, 0.012, 0.02), (0.03, 0.04, 0.06))
    c = A(7, "cortinas", 0.0)
    ab = 1.0 - smooth(pr(t, c - 0.2, c + 1.0))
    sala_obs(p, t, ab, cortinas=True, publico=False, rect=(330, 90, 1130, 590))
    # periodistas fuera tomando notas
    for k, (x, h) in enumerate(((1260, 520), (1520, 560), (1760, 500))):
        persona(p, x, 1040, h, pose_escribir(t + k * 0.8), (0.025, 0.03, 0.045), ropa="chaqueta", pelo="largo" if k == 1 else "corto")
    for k in range(5):
        p.rect(1200 + k * 120, 960, 1262 + k * 120, 1000, (0.75, 0.72, 0.62), 0.0)
    # onda de ronquido (se oye aunque la cortina esté cerrada)
    tr = A(7, "roncaba", -0.4)
    a = smooth(pr(t, tr, tr + 0.5))
    pts = [(240 + i * 12, 760 + math.sin(i * 0.35 + t * 7) * (40 + 60 * abs(math.sin(t * 1.5 + i * 0.05))) * a * math.exp(-((i - 60) / 52) ** 2)) for i in range(120)]
    p.polilinea(pts, 8, (0.35, 0.95, 0.60), 0.9 * a)
    for k in range(4):
        u = (t * 0.45 + k * 0.25) % 1.0
        p.texto("Z", 760 + k * 80 + u * 90, 700 - u * 300, 70 + 30 * k, CREMA, "sans_b", 0.7 * (1 - u) * a)
    p.texto("RESPIRACIÓN RUIDOSA", 740, 880, 40, (0.6, 0.95, 0.75), "sans_b", 0.8 * a)
    vineta_p(p, 0.6)
    _cam(p, tl, dur, 1.0, 1.06, 0.45, 0.5)
    p.fin(lz)


# ====================================================================== 8: EL PROTOCOLO NO DICE QUÉ HACER
@esc("n_protocolo", lambda: INI(N_, 8), lambda: FIN(N_, 8))
def n_protocolo(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.10, 0.075, 0.06), (0.025, 0.02, 0.02))
    p.glow(960, 500, 1000, (1.0, 0.8, 0.5), 0.3)
    T0 = INI(N_, 8)
    u = ease_out(pr(t, T0, T0 + 0.8))
    cy = lerp(1300, 540, u)
    documento(p, 840, cy, 900, 880, ang=-0.03, lineas=0, titulo=False)
    p.texto("PROTOCOLO", 840, cy - 330, 66, (0.12, 0.10, 0.10), "sans_b", u)
    pasos = ["1. Se inserta la vía", "2. Primera dosis", "3. Cinco minutos de espera", "4. Segunda dosis"]
    for k, s in enumerate(pasos):
        ap = smooth(pr(t, T0 + 0.8 + k * 0.5, T0 + 1.2 + k * 0.5))
        p.texto(s, 500, cy - 200 + k * 85, 44, (0.18, 0.16, 0.16), "sans_l", ap, anchor="lm")
        if ap > 0.9:
            check(p, 1130, cy - 200 + k * 85, 24, smooth(pr(t, T0 + 1.2 + k * 0.5, T0 + 1.6 + k * 0.5)), (0.2, 0.7, 0.35), 8)
    td = A(8, "dice", -0.4)
    p.texto("5.", 500, cy + 140, 44, (0.18, 0.16, 0.16), "sans_l", smooth(pr(t, td, td + 0.4)), anchor="lm")
    for k in range(3):
        if t > td:
            p.rect(540, cy + 140 + 6 + k * 0, 540 + 560 * clamp((t - td - 0.2) * 1.6), cy + 150, (0.5, 0.48, 0.45), 0.7 * (1 if k == 0 else 0))
    # un espacio en blanco subrayado en rojo y un gran signo de pregunta
    ap = ease_back(pr(t, A(8, "hacer", -0.2), A(8, "hacer", 0.5)))
    if ap > 0.02:
        p.polilinea([(520, cy + 175), (1110, cy + 175)], 10, ROJO, ap)
        p.texto("?", 1560, 520, 520 * ap, ROJO, "abril", clamp(ap))
    vineta_p(p, 0.55)
    _cam(p, tl, dur, 1.0, 1.05)
    p.fin(lz)


# ====================================================================== 9: AMBULANCIA
@esc("n_ambulancia", lambda: INI(N_, 9), lambda: FIN(N_, 9))
def n_ambulancia(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.01, 0.015, 0.035), (0.07, 0.09, 0.14), 0, 0.8)
    estrellas(p, t, 60, y_max=0.45, brillo=0.7)
    ciudad(p, t, 800, (0.02, 0.03, 0.05), off=t * 40, seed=8, h_max=420)
    ciudad(p, t, 880, (0.008, 0.012, 0.02), off=t * 90, seed=9, h_max=320, ancho_med=150)
    # hospital que se acerca al final
    hx = lerp(3000, 1500, smooth(pr(t, INI(N_, 9), FIN(N_, 9))))
    p.rect(hx - 380, 440, hx + 380, 900, (0.05, 0.07, 0.10))
    rng = np.random.default_rng(2)
    for r in range(6):
        for c in range(12):
            if rng.random() < 0.65:
                p.rect(hx - 340 + c * 58, 480 + r * 62, hx - 300 + c * 58, 520 + r * 62, (1.0, 0.9, 0.6), 0.8)
    p.rect(hx - 60, 380, hx + 60, 440, (0.7, 0.1, 0.1))
    p.rect(hx - 14, 392, hx + 14, 428, (1, 1, 1)); p.rect(hx - 28, 404, hx + 28, 416, (1, 1, 1))
    # carretera con rayas que pasan
    p.rect(-10, 900, W + 10, H + 10, (0.03, 0.04, 0.05))
    for k in range(10):
        x = (k * 260 - t * 700) % (W + 260) - 130
        p.rect(x, 1000, x + 140, 1016, (0.7, 0.7, 0.6), 0.8)
    amb_x = 640 + 30 * math.sin(t * 2)
    p.glow(amb_x + 380, 960, 520, (1.0, 0.95, 0.8), 0.5)
    p.haz(amb_x + 420, 940, 0, 900, 22, (1.0, 0.97, 0.85), 0.55)
    ambulancia(p, amb_x, 960, 640, t)
    lluvia(p, t, 0.25, 70)
    vineta_p(p, 0.6)
    p.fin(lz)
