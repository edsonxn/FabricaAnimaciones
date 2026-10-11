# -*- coding: utf-8 -*-
"""Escenas DIBUJADAS del documental (v2): cada función pinta un fondo completo en `lz` para el instante `t` (absoluto) con las anclas de la voz.
Firma de fondo del motor: f(lz, tl, t, dur, ext). Se registran en ESC con @esc(nombre) para poder probarlas con _prueba_mg.py.
Nada de metraje reciclado: todo es procedural (siluetas, objetos, ambientes)."""
import math

import numpy as np

from kit_cp import INI, FIN, ww, we, TL  # anclas de la voz
from mg import *  # noqa: F401,F403
from mg_obj import *  # noqa: F401,F403

ESC = {}


def esc(nombre, ini, fin):
    """Registra una escena dibujada. ini/fin: funciones sin argumentos que devuelven segundos absolutos (para poder probarla)."""
    def deco(fn):
        ESC[nombre] = (fn, ini, fin)
        return fn
    return deco


def F_mg(nombre):
    """Fondo del motor (`shot`) que ejecuta la escena registrada `nombre`."""
    fn = ESC[nombre][0]

    def f(lz, tl, t, dur, ext):
        fn(lz, tl, t, dur, ext)
    return f


def OV(fn):
    """Extra del motor: pinta con P sobre negro y SUMA al cuadro (brillos, líneas, iconos luminosos)."""
    def f(lz, t):
        p = P()
        fn(p, t)
        tmp = np.empty_like(lz)
        p.fin(tmp)
        lz += tmp
    return f


def _cam(p, tl, dur, z0=1.0, z1=1.08, cx=0.5, cy=0.5):
    zoom_p(p, lerp(z0, z1, smooth(tl / max(dur, 1e-3))), cx, cy)


def _lamp(p, x, y, ang, largo, ab, t, amt=0.5):
    fl = 1.0 - 0.06 * (math.sin(t * 31) > 0.92)
    p.haz(x, y, ang, largo, ab, (0.88, 0.94, 1.0), amt * fl)
    p.glow(x, y, 200, (0.9, 0.95, 1.0), 0.8 * fl)
    p.rect(x - 90, y - 26, x + 90, y + 2, (0.22, 0.23, 0.26))


def _sala(p, y_suelo=780, top=(0.012, 0.018, 0.03), bot=(0.045, 0.060, 0.085)):
    p.fondo(top, bot, 0, 0.85)
    for x in range(0, W, 260):
        p.rect(x, 0, x + 4, y_suelo, (0, 0, 0), 0.25)
    suelo(p, y_suelo, (0.03, 0.04, 0.055), (0.008, 0.01, 0.016))


# ====================================================================== GANCHO
@esc("g_camilla", lambda: INI("gancho", 1), lambda: FIN("gancho", 1))
def g_camilla(lz, tl, t, dur, ext):
    p = P()
    _sala(p)
    _lamp(p, 1000, 20, 90, 780, 40, t, 0.55)
    p.elip(1000, 800, 560, 60, 0, LUZ, 0.10)
    camilla(p, 1000, 650, 900)
    (ex, ey), (wx, wy) = acostada(p, 975, 598, 720, (0.04, 0.05, 0.07), t, brazo=1.0)
    bolsa_iv(p, 470, 120, 360, t, tubo_a=(wx - 20, wy))
    p.linea((470, 120), (470, 120), 4, SIL)
    p.rect(463, 120, 477, 790, (0.12, 0.13, 0.15), 0.9)
    polvo(p, t, 60, op=0.5)
    vineta_p(p, 0.5)
    _cam(p, tl, dur, 1.0, 1.10, 0.55, 0.65)
    p.fin(lz)


@esc("g_testigos", lambda: INI("gancho", 2), lambda: FIN("gancho", 2))
def g_testigos(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.01, 0.014, 0.022), (0.03, 0.04, 0.06))
    x0, y0, x1, y1 = 500, 110, 1420, 590
    ventana_obs(p, x0, y0, x1, y1, (0.70, 0.76, 0.70))
    # interior iluminado: pared, camilla, bolsa
    p.rect(x0, y1 - 120, x1, y1, (0.40, 0.44, 0.40))
    camilla(p, 960, y1 - 150, 560, (0.88, 0.9, 0.92))
    p.rect(x0 + 120, y0, x0 + 128, y1 - 110, (0.35, 0.37, 0.4))
    p.rect(x0 + 70, y0 + 40, x0 + 180, y0 + 150, (0.88, 0.9, 0.85), 0.9)
    p.circ(x1 - 140, y0 + 90, 26, (0.15, 0.15, 0.17))
    abierto = smooth(pr(t, INI("gancho", 2) + 0.9, INI("gancho", 2) + 3.4))
    cortina(p, x0, y0, x1, y1, abierto, t=t)
    # testigos de espaldas (cabezas que giran levemente)
    rng = np.random.default_rng(5)
    for fila, (yy, hh, col) in enumerate(((880, 250, (0.006, 0.008, 0.012)), (1010, 330, (0.004, 0.005, 0.008)))):
        n = 8 if fila == 0 else 7
        for i in range(n):
            xx = 150 + i * 235 + (60 if fila else 0) + math.sin(t * 0.9 + i) * 5
            silueta_sentada_vista_trasera(p, xx, yy, hh * (0.85 + 0.3 * rng.random()), col)
    p.glow(960, 330, 700, (0.55, 0.62, 0.55), 0.25 * abierto)
    vineta_p(p, 0.55)
    _cam(p, tl, dur, 1.0, 1.07, 0.5, 0.4)
    p.fin(lz)


@esc("g_dosis", lambda: INI("gancho", 3), lambda: FIN("gancho", 3))
def g_dosis(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.02, 0.03, 0.05), (0.06, 0.08, 0.12))
    p.glow(560, 540, 700, (0.3, 0.38, 0.55), 0.35)
    reloj(p, 560, 540, 320, tl, h=7.0, m=0.0, vel_min=3.2)
    for k, (yy, clave) in enumerate(((360, "una"), (740, "otra"))):
        t0 = ww("gancho", 3, clave)
        u = smooth(pr(t, t0, t0 + 1.4))
        p.glow(1380, yy, 300 + 200 * smooth(pr(t, t0, t0 + 0.3)) * (1 - u), (1.0, 0.85, 0.4), 0.5 * smooth(pr(t, t0 - 0.2, t0 + 0.2)))
        jeringa(p, 1340, yy, -0.25, 640, u)
        ap = ease_back(pr(t, t0 - 0.5, t0 - 0.1))
        p.texto(f"DOSIS {k + 1}", 1340, yy + 120, 54 * ap, CREMA, "sans_b", clamp(ap))
    # minuteros que pasan: puntitos de tiempo
    polvo(p, t, 40, seed=2, op=0.35)
    vineta_p(p, 0.55)
    _cam(p, tl, dur, 1.0, 1.06)
    p.fin(lz)


@esc("g_nadie", lambda: INI("gancho", 4), lambda: FIN("gancho", 4))
def g_nadie(lz, tl, t, dur, ext):
    p = P()
    _sala(p)
    _lamp(p, 960, 20, 90, 800, 34, t, 0.5)
    camilla(p, 960, 700, 760)
    p.elip(960, 820, 480, 50, 0, LUZ, 0.09)
    pos = [(330, 980, 640, 1), (560, 1000, 700, 1), (1370, 1000, 700, -1), (1600, 980, 640, -1)]
    for k, (x, y, h, f) in enumerate(pos):
        persona(p, x, y, h, pose_estar(t + k, lean=0.04 * math.sin(t * 0.7 + k)), SIL, facing=f, ropa="chaqueta" if k % 2 == 0 else "pantalon", pelo="corto")
    # signos de pregunta que brotan sobre las cabezas
    base = ww("gancho", 4, "nadie")
    for k, (x, y, h, f) in enumerate(pos):
        t0 = base + k * 0.55
        u = pr(t, t0, t0 + 1.8)
        if u > 0:
            ap = ease_back(min(1, u * 3))
            p.texto("?", x + 20 * math.sin(t * 2 + k), y - h - 70 - 90 * u, 150 * ap, ROJO, "abril", clamp(1.6 - u * 1.2))
    polvo(p, t, 40, op=0.4)
    vineta_p(p, 0.55)
    _cam(p, tl, dur, 1.0, 1.08)
    p.fin(lz)


def ecg_pulso(p, t):
    """Overlay del 'sigue respirando': línea de monitor y anillo de latido bajo la ficha."""
    ecg(p, 330, 960, 1260, 120, t, vel=360, ritmo=0.9, irregular=0.6, op=0.9)
    u = (t * 1.1) % 1.0
    p.polilinea([(960 + 260 * u * math.cos(a) * 1.9, 540 + 260 * u * math.sin(a)) for a in np.linspace(0, 6.28, 40)], 6 * (1 - u) + 1, (0.9, 0.2, 0.2), 0.5 * (1 - u), cerrado=True)


# ====================================================================== QUIEN
@esc("q_montanas", lambda: INI("quien", 1), lambda: ww("quien", 1, "virginia", sep=-0.25))
def q_montanas(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.05, 0.08, 0.20), (0.95, 0.55, 0.30), 0.0, 0.78)            # anochecer en los Apalaches
    estrellas(p, t, 60, y_max=0.4, brillo=0.7)
    p.glow(1500, 700, 520, (1.0, 0.62, 0.30), 0.9)
    p.circ(1500, 700, 70, (1.0, 0.8, 0.5))
    colinas(p, 760, 330, (0.30, 0.22, 0.34), off=t * 5, seed=11, escala=0.6)
    niebla(p, t, 720, 200, (0.95, 0.7, 0.6), 0.35, vel=9, seed=3)
    colinas(p, 860, 300, (0.15, 0.12, 0.22), off=t * 11 + 400, seed=12, escala=0.9)
    niebla(p, t, 820, 180, (0.7, 0.55, 0.6), 0.35, vel=16, seed=4)
    colinas(p, 960, 260, (0.05, 0.06, 0.10), off=t * 20 + 900, seed=13, escala=1.2)
    bosque(p, 990, 260, (0.02, 0.025, 0.04), off=t * 30, seed=6, n=16)
    # cabaña con ventana encendida y una niña que camina por el camino
    p.poly([(250, 1010), (250, 900), (330, 840), (410, 900), (410, 1010)], (0.015, 0.02, 0.03))
    p.rect(300, 930, 345, 975, (1.0, 0.78, 0.4), 0.9 + 0.1 * math.sin(t * 3))
    p.glow(322, 952, 160, (1.0, 0.7, 0.3), 0.55)
    xn = lerp(520, 1250, (tl * 0.09) % 1.0)
    persona(p, xn, 1050, 330, pose_caminar(tl * 6.0), (0.03, 0.035, 0.055), ropa="vestido", pelo="largo")
    p.rect(-10, 1030, W + 10, H + 10, (0.012, 0.016, 0.025))
    # aves
    for k in range(6):
        xa = (W + 200 - (t * 90 + k * 140)) % (W + 400) - 100
        ya = 230 + 60 * math.sin(t * 0.8 + k) + k * 25
        al = 22 * math.sin(t * 9 + k)
        p.polilinea([(xa - 26, ya + al), (xa, ya), (xa + 26, ya + al)], 4, SIL, 0.85, caps=False)
    vineta_p(p, 0.5)
    _cam(p, tl, dur, 1.0, 1.07, 0.5, 0.7)
    p.fin(lz)


@esc("q_campus", lambda: ww("quien", 3, "programa", sep=-0.3), lambda: FIN("quien", 3))
def q_campus(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.10, 0.20, 0.34), (0.98, 0.62, 0.35), 0.0, 0.7)
    p.glow(300, 700, 700, (1.0, 0.7, 0.4), 0.8)
    p.circ(300, 700, 90, (1.0, 0.85, 0.6))
    colinas(p, 820, 160, (0.16, 0.13, 0.22), off=t * 4, seed=21, escala=0.5)
    # edificio dormitorio con ventanas
    bx0, bx1, by1, bh = 760, 1700, 930, 420
    p.rect(bx0, by1 - bh, bx1, by1, (0.05, 0.06, 0.10))
    p.rect(bx0 - 20, by1 - bh - 26, bx1 + 20, by1 - bh, (0.09, 0.10, 0.15))
    rng = np.random.default_rng(3)
    for r in range(4):
        for c in range(14):
            lit = rng.random() < 0.45
            xx = bx0 + 34 + c * 66
            yy = by1 - bh + 34 + r * 96
            p.rect(xx, yy, xx + 38, yy + 58, (1.0, 0.8, 0.45) if lit else (0.14, 0.17, 0.25), 0.9 if lit else 1.0)
            if lit and rng.random() < 0.3:
                p.circ(xx + 19, yy + 40, 11, SIL, 0.9)
    p.rect(bx0 + 410, by1 - 120, bx0 + 520, by1, (0.02, 0.02, 0.03))
    p.rect(bx0 + 380, by1 - 150, bx0 + 550, by1 - 120, (0.55, 0.12, 0.12))
    p.texto("JOB CORPS", bx0 + 465, by1 - 135, 24, CREMA, "sans_b")
    # bandera
    p.rect(1790, 420, 1798, 930, (0.5, 0.5, 0.52))
    onda = math.sin(t * 3)
    p.poly([(1798, 430), (1920, 430 + 6 * onda), (1920, 500 + 10 * onda), (1798, 490)], (0.7, 0.12, 0.14))
    # suelo + árboles
    p.rect(-10, 930, W + 10, H + 10, (0.04, 0.05, 0.07))
    for k in range(5):
        pino(p, 120 + k * 150 + (k % 2) * 40, 940, 330 - k * 20, (0.02, 0.03, 0.04))
    # jóvenes que llegan con mochilas desde la izquierda
    for k in range(6):
        x = -150 + ((tl * 150 + k * 190) % (W * 0.62 + 300))
        if x < bx0 + 480:
            persona(p, x, 1050 + (k % 2) * 25, 330 - (k % 3) * 16, pose_caminar(tl * 5.5 + k * 1.3), SIL, ropa="chaqueta" if k % 2 else "pantalon", pelo="largo" if k % 3 == 0 else "corto", bolso=(k % 2 == 0))
    vineta_p(p, 0.45)
    _cam(p, tl, dur, 1.0, 1.06, 0.4, 0.6)
    p.fin(lz)


# ====================================================================== COLLEEN
@esc("c_florida", lambda: INI("colleen", 1), lambda: FIN("colleen", 1))
def c_florida(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.03, 0.06, 0.12), (0.06, 0.12, 0.20))
    mapa_us(p, resaltar=("Florida",), zoom=(-82.9, 28.4, 4.0), color=(0.08, 0.14, 0.23), color_res=(0.45, 0.36, 0.16))
    ox, oy = proy_us(-81.77, 30.17)
    cxz, cyz = proy_us(-82.9, 28.4)
    x, y = 960 + (ox - cxz) * 4.0, 540 + (oy - cyz) * 4.0
    pin(p, x, y, 26, ROJO, t)
    p.texto("Orange Park", x + 70, y - 70, 54, CREMA, "sans_b", smooth(pr(tl, 0.5, 1.2)), anchor="lm")
    # palmeras mecidas
    for px_, hh in ((130, 700), (1790, 760)):
        sway = math.sin(t * 1.2 + px_) * 14
        p.polilinea([(px_, 1100), (px_ + sway * 0.5, 1100 - hh * 0.5), (px_ + sway, 1100 - hh)], 20, SIL)
        for k in range(7):
            a = -math.pi / 2 + (k - 3) * 0.42 + math.sin(t * 1.5 + k) * 0.05
            p.poly([(px_ + sway, 1100 - hh), (px_ + sway + 230 * math.cos(a - 0.1), 1100 - hh + 230 * math.sin(a - 0.1) + 60),
                    (px_ + sway + 280 * math.cos(a), 1100 - hh + 280 * math.sin(a) + 120), (px_ + sway + 230 * math.cos(a + 0.1), 1100 - hh + 230 * math.sin(a + 0.1) + 60)], SIL)
    vineta_p(p, 0.5)
    p.fin(lz)


@esc("c_pc", lambda: INI("colleen", 2), lambda: FIN("colleen", 2))
def c_pc(lz, tl, t, dur, ext):
    p = P()
    _sala(p, 800, (0.03, 0.025, 0.04), (0.08, 0.06, 0.07))
    p.glow(1100, 500, 900, (0.15, 0.7, 0.5), 0.35)
    escritorio_pc(p, 1150, 800, 760, tl)
    # silla y la joven escribiendo
    p.rect(660, 700, 790, 730, (0.05, 0.05, 0.07))
    p.rect(650, 520, 676, 730, (0.05, 0.05, 0.07))
    p.rect(700, 730, 716, 800, (0.05, 0.05, 0.07))
    persona(p, 740, 800, 560, pose_escribir(tl), SIL, facing=1, ropa="vestido", pelo="largo")
    # el abuelo detrás, con la mano en el hombro (pose señalar)
    persona(p, 480, 805, 640, pose_señalar(0.9 + 0.1 * math.sin(tl)), SIL, facing=1, ropa="chaqueta", pelo="corto")
    # flotan símbolos de computación
    for k in range(10):
        x = (k * 211 + tl * 30) % W
        y = 100 + ((k * 97 + tl * 40) % 320)
        p.texto(("01" if k % 2 else "10"), x, y, 40, (0.2, 0.9, 0.6), "mono", 0.18)
    polvo(p, t, 30, op=0.3, color=(0.4, 1.0, 0.7))
    vineta_p(p, 0.55)
    _cam(p, tl, dur, 1.0, 1.08, 0.55, 0.55)
    p.fin(lz)
