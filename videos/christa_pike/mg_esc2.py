# -*- coding: utf-8 -*-
"""Escenas dibujadas, parte 2: quien/crimen/juicio/corredor/debate/camino."""
import math

import numpy as np

from mg_esc import *  # noqa: F401,F403
from mg_esc import ESC, esc, _cam, _sala, _lamp


def planta_vapor(p, x, y, esc_, t, color=SIL):
    E = esc_
    p.rect(x - E * 0.55, y - E * 0.50, x + E * 0.30, y, color)
    p.rect(x - E * 0.55, y - E * 0.56, x + E * 0.30, y - E * 0.50, mix(color, (1, 1, 1), 0.06))
    p.rect(x + E * 0.30, y - E * 0.32, x + E * 0.62, y, color)
    p.poly([(x - E * 0.55, y - E * 0.56), (x - E * 0.30, y - E * 0.78), (x + E * 0.30, y - E * 0.78), (x + E * 0.30, y - E * 0.56)], color)
    for k in range(5):                                   # ventanas rotas
        xx = x - E * 0.48 + k * E * 0.16
        p.poly([(xx, y - E * 0.38), (xx + E * 0.08, y - E * 0.38), (xx + E * 0.08 - E * 0.015 * (k % 2), y - E * 0.20), (xx, y - E * 0.20)], (0.05, 0.07, 0.10))
    cx = x + E * 0.40                                    # chimenea
    p.poly([(cx - E * 0.05, y - E * 0.32), (cx + E * 0.05, y - E * 0.32), (cx + E * 0.035, y - E * 1.25), (cx - E * 0.035, y - E * 1.25)], color)
    for k in range(7):                                   # humo/vapor que asciende
        u = ((t * 0.18 + k / 7) % 1.0)
        p.circ(cx + math.sin(u * 6 + k) * E * 0.06 + u * E * 0.2, y - E * 1.25 - u * E * 0.9, E * (0.05 + 0.13 * u), (0.55, 0.6, 0.68), 0.30 * (1 - u))


def calles(p, y, color):
    p.rect(-10, y, W + 10, H + 10, color)


# ====================================================================== CRIMEN
@esc("cr_bosque", lambda: INI("crimen", 1), lambda: ww("crimen", 1, "junto", sep=-0.2))
def cr_bosque(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.012, 0.022, 0.05), (0.08, 0.11, 0.17), 0, 0.82)
    estrellas(p, t, 70, y_max=0.45, brillo=0.8)
    luna(p, 1480, 190, 58, halo=0.9)
    colinas(p, 760, 220, (0.035, 0.055, 0.085), off=t * 7, seed=31)
    planta_vapor(p, lerp(2500, 1560, smooth(tl / max(dur, 1))), 820, 560, t, (0.02, 0.03, 0.045))
    bosque(p, 900, 340, (0.025, 0.035, 0.055), off=t * 38, seed=3, n=16, pelados=True)
    niebla(p, t, 880, 260, (0.45, 0.55, 0.68), 0.45, vel=22, seed=5)
    bosque(p, 1010, 520, (0.008, 0.012, 0.02), off=t * 95, seed=9, n=9, pelados=True)
    p.rect(-10, 990, W + 10, H + 10, (0.006, 0.008, 0.012))
    for k, (x, h, ropa, pelo) in enumerate(((420, 340, "vestido", "largo"), (600, 400, "chaqueta", "corto"), (790, 360, "vestido", "moño"))):
        persona(p, x, 1030, h, pose_caminar(t * 5.6 + k * 1.9, lean=0.07), (0.004, 0.006, 0.01), ropa=ropa, pelo=pelo)
    lluvia(p, t, 0.18, 50)
    vineta_p(p, 0.6)
    _cam(p, tl, dur, 1.0, 1.06, 0.45, 0.7)
    p.fin(lz)


@esc("cr_paz", lambda: ww("crimen", 2, "doce", sep=-0.2), lambda: FIN("crimen", 2))
def cr_paz(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.05, 0.08, 0.14), (0.16, 0.22, 0.28), 0, 0.8)
    colinas(p, 800, 180, (0.05, 0.07, 0.10), off=t * 3, seed=41)
    bosque(p, 980, 520, (0.015, 0.02, 0.03), off=t * 12, seed=7, n=12, pelados=True)
    niebla(p, t, 940, 200, (0.55, 0.62, 0.72), 0.35, vel=10, seed=8)
    p.rect(-10, 980, W + 10, H + 10, (0.01, 0.014, 0.02))
    u = smooth(pr(t, ww("crimen", 2, "paces", sep=-1.2), ww("crimen", 2, "paces", sep=0.6)))
    xa = lerp(1500, 1010, u)
    persona(p, 380, 1040, 380, pose_estar(t, 0.02), (0.01, 0.012, 0.02), ropa="chaqueta", pelo="corto")
    persona(p, 560, 1050, 360, pose_estar(t + 1, 0.0), (0.01, 0.012, 0.02), ropa="vestido", pelo="moño")
    persona(p, xa, 1045, 380, pose_caminar(t * 4.5) if u < 0.98 else pose_señalar(0.6 + 0.4 * math.sin(t)), (0.006, 0.008, 0.012), facing=-1, ropa="vestido", pelo="largo")
    # globo de diálogo con la palabra «paz»
    ap = ease_back(pr(t, ww("crimen", 2, "paces", sep=-0.2), ww("crimen", 2, "paces", sep=0.4)))
    if ap > 0.02:
        p.elip(480, 560, 170 * ap, 105 * ap, 0, CREMA, 0.95)
        p.poly([(420, 640), (450, 700), (500, 640)], CREMA, 0.95)
        p.texto("PAZ", 480, 560, 90 * ap, (0.1, 0.1, 0.12), "sans_b")
    # calendario girando al fondo-derecha
    hoja_cal(p, 1550, 330, 330, 360, "ENERO", "12", u=0.0, rojo_u=pr(t, INI("crimen", 2) + 0.4, INI("crimen", 2) + 1.8))
    polvo(p, t, 30, op=0.3)
    vineta_p(p, 0.55)
    _cam(p, tl, dur, 1.0, 1.06, 0.5, 0.65)
    p.fin(lz)


@esc("cr_reloj", lambda: INI("crimen", 3), lambda: FIN("crimen", 3))
def cr_reloj(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.01, 0.015, 0.04), (0.06, 0.09, 0.14), 0, 0.85)
    estrellas(p, t, 60, y_max=0.5)
    luna(p, 560, 220, 52)
    bosque(p, 980, 560, (0.012, 0.018, 0.028), off=t * 6, seed=4, n=12, pelados=True)
    niebla(p, t, 900, 260, (0.4, 0.5, 0.62), 0.4, vel=8, seed=11)
    p.rect(-10, 990, W + 10, H + 10, (0.005, 0.007, 0.01))
    # reloj gigante: una vuelta completa en el tiempo de la frase (30 minutos -> 1 hora)
    t0, t1 = ww("crimen", 3, "media", sep=-0.3), ww("crimen", 3, "hora", nth=0, sep=0.2)
    vel = 60.0 / max(FIN("crimen", 3) - INI("crimen", 3) - 1.0, 2.0)
    reloj(p, 1330, 470, 300, 0.0, h=0.0, m=(t - INI("crimen", 3)) * vel * 1.0, segundero=False, cara=(0.82, 0.84, 0.88))
    vineta_p(p, 0.6)
    _cam(p, tl, dur, 1.0, 1.05, 0.6, 0.5)
    p.fin(lz)


# ====================================================================== JUICIO
@esc("j_trato", lambda: INI("juicio", 0), lambda: FIN("juicio", 0))
def j_trato(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.10, 0.07, 0.05), (0.03, 0.02, 0.02), 0, 1.0)
    p.rect(-10, 700, W + 10, H + 10, (0.14, 0.09, 0.06), grad=((0.18, 0.11, 0.07), (0.05, 0.03, 0.02)))
    p.glow(960, 700, 900, (1.0, 0.75, 0.4), 0.35)
    t_off = ww("juicio", 0, "ofrecio", sep=-0.2)
    u = ease_out(pr(t, t_off, t_off + 0.7))
    pts = documento(p, lerp(-420, 760, u), 560, 560, 720, ang=lerp(0.25, -0.06, u), lineas=11, titulo=False)
    if u > 0.85:
        p.texto("ACUERDO DE CULPABILIDAD", 760, 330, 34, (0.12, 0.10, 0.10), "sans_b", 0.9 * u)
        p.texto("CADENA PERPETUA", 760, 460, 52, ROJO, "abril", smooth(pr(t, ww("juicio", 0, "cadena", sep=-0.1), ww("juicio", 0, "cadena", sep=0.3))))
    # pluma que se ofrece y se retira
    tr = ww("juicio", 0, "rechazo", sep=-0.1)
    pu = smooth(pr(t, t_off + 0.5, t_off + 1.5)) * (1 - smooth(pr(t, tr, tr + 0.5)))
    px_ = lerp(1500, 1050, pu)
    p.polilinea([(px_, 340 + 20 * math.sin(t * 2)), (px_ + 230, 240)], 18, (0.12, 0.10, 0.12))
    p.poly([(px_ - 8, 340 + 20 * math.sin(t * 2)), (px_ - 54, 366 + 20 * math.sin(t * 2)), (px_ + 8, 350 + 20 * math.sin(t * 2))], (0.85, 0.85, 0.88))
    cruz(p, 760, 560, 280, pr(t, tr, tr + 0.7), ROJO, 40)
    # el documento sale despedido
    vineta_p(p, 0.55)
    _cam(p, tl, dur, 1.0, 1.05)
    p.fin(lz)


@esc("j_tribunal", lambda: ww("juicio", 2, "treinta", sep=-0.3), lambda: ww("juicio", 2, "silla", sep=-0.3))
def j_tribunal(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.05, 0.04, 0.05), (0.14, 0.09, 0.07), 0, 0.9)
    p.rect(-10, 800, W + 10, H + 10, (0.07, 0.045, 0.035))
    # estrado del juez
    p.rect(480, 560, 1440, 900, (0.22, 0.12, 0.07), grad=((0.30, 0.17, 0.10), (0.13, 0.07, 0.04)))
    p.rect(450, 535, 1470, 570, (0.36, 0.21, 0.12))
    persona(p, 880, 560, 420, pose_estar(t), (0.02, 0.015, 0.02), ropa="vestido", pelo="corto")      # juez con toga
    p.glow(900, 300, 700, (1.0, 0.8, 0.5), 0.3)
    th = ww("juicio", 2, "condenada", sep=0.0)
    u = pr(t, th - 0.6, th)
    mazo(p, 1230, 535, 420, ease_out(u) if t < th else 1.0)
    onda_choque(p, 1230, 560, pr(t, th, th + 0.5), 460)
    p.glow(1230, 540, 420 * (1 - pr(t, th, th + 0.4)), (1, 0.9, 0.7), 0.8 * (t > th))
    # público al fondo
    for i in range(10):
        silueta_sentada_vista_trasera(p, 90 + i * 190 + (i % 2) * 40, 960 + (i % 2) * 40, 230, (0.008, 0.006, 0.008))
    p.texto("30 · 03 · 1996", 960, 140, 120, ROJO, "abril", smooth(pr(t, INI("juicio", 2) + 0.2, INI("juicio", 2) + 0.8)))
    vineta_p(p, 0.55)
    _cam(p, tl, dur, 1.0, 1.06, 0.6, 0.55)
    p.fin(lz)


@esc("j_silla", lambda: ww("juicio", 2, "silla", sep=-0.3), lambda: FIN("juicio", 2))
def j_silla(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.02, 0.02, 0.03), (0.10, 0.09, 0.10), 0, 0.9)
    p.glow(960, 330, 800, (0.9, 0.95, 1.0), 0.5)
    p.haz(960, 0, 90, 1000, 38, (0.9, 0.95, 1.0), 0.6)
    suelo(p, 860, (0.07, 0.07, 0.08), (0.02, 0.02, 0.03))
    u = ease_out(pr(t, ww("juicio", 2, "silla", sep=-0.1), ww("juicio", 2, "silla", sep=0.8)))
    silla_electrica(p, 960, 860, 560 * (0.8 + 0.2 * u), (0.01, 0.01, 0.015), u)
    p.elip(960, 868, 320, 28, 0, (0, 0, 0), 0.6)
    vineta_p(p, 0.6)
    _cam(p, tl, dur, 1.0, 1.1, 0.5, 0.5)
    p.fin(lz)


# ====================================================================== CORREDOR
@esc("co_pasillo", lambda: INI("corredor", 0), lambda: FIN("corredor", 3))
def co_pasillo(lz, tl, t, dur, ext):
    p = P()
    T0 = INI("corredor", 0)
    cam = (t - T0) * 0.55
    pasillo(p, t, cam=cam)
    # calendarios que vuelan hacia la cámara marcando el paso de los años
    for k in range(14):
        u = ((t - T0) * 0.16 + k / 14) % 1.0
        z = 1.0 + 6.0 * (1 - u)
        sx = 960 + math.sin(k * 2.3) * 520 / z
        sy = 470 + math.cos(k * 1.7) * 220 / z
        hoja_cal(p, sx, sy, 150 / z * 2.2, 170 / z * 2.2, "AÑO", str(1996 + int((t - T0) * 30 / max(dur, 1) + k)) if False else "", u=0.0) if False else None
    # figura sentada en una celda lejana
    persona(p, 930, 706, 120, pose_sentado(t, 0.2), (0.012, 0.014, 0.02), ropa="vestido", pelo="largo")
    vineta_p(p, 0.6)
    p.fin(lz)


@esc("co_anos", lambda: INI("corredor", 0), lambda: INI("corredor", 1))
def co_anos(lz, tl, t, dur, ext):
    co_pasillo(lz, tl, t, dur, ext)
    p = P()
    T0 = INI("corredor", 0)
    # contador de años 1996 -> 2026 a lo largo de la frase
    rodillo(p, 1330, 420, 1996, 2026, pr(t, T0 + 0.8, FIN("corredor", 0) - 0.4), 250, ROJO)
    tmp = np.empty_like(lz)
    p.fin(tmp)
    lz += tmp


# ====================================================================== DEBATE
@esc("d_balanza", lambda: INI("debate", 0), lambda: FIN("debate", 0))
def d_balanza(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.05, 0.06, 0.10), (0.16, 0.14, 0.15), 0, 0.9)
    p.glow(960, 360, 900, (1.0, 0.85, 0.55), 0.35)
    for k in range(2):                                       # cortinas de luz
        p.haz(300 + k * 1320, -40, 90, 1000, 30, (1.0, 0.9, 0.7), 0.18)
    tilt = 0.42 * math.sin(tl * 1.5) * math.exp(-tl * 0.15)
    balanza(p, 960, 250, 760, tilt, (0.86, 0.80, 0.62), t=t)
    p.texto("CONDENA", 560, 900, 60, CREMA, "sans_b", smooth(pr(tl, 0.3, 0.9)))
    p.texto("PERDÓN", 1360, 900, 60, CREMA, "sans_b", smooth(pr(tl, 0.9, 1.5)))
    polvo(p, t, 40, op=0.4)
    vineta_p(p, 0.55)
    _cam(p, tl, dur, 1.0, 1.06)
    p.fin(lz)


# ====================================================================== CAMINO
_MESES = ["OCT", "NOV", "DIC", "ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO"]


def OV_calendario(t0, t1, cx=420, cy=600):
    """Hojas de calendario que se arrancan una tras otra, de «30 sep 2025» a «30 sep 2026» (12 saltos)."""
    hojas = [("SEP 2025", "30")] + [(f"{m} {2025 if k < 3 else 2026}", "1") for k, m in enumerate(_MESES)] + [("SEP 2026", "30")]

    def f(p, t):
        x = pr(t, t0, t1) * 12
        k = min(11, int(x))
        fr = x - k
        if x >= 12:
            hoja_cal(p, cx, cy, 340, 390, *hojas[12], u=0.0, rojo_u=pr(t, t1, t1 + 0.8))
            return
        hoja_cal(p, cx, cy, 340, 390, *hojas[k + 1], u=0.0)
        hoja_cal(p, cx, cy, 340, 390, *hojas[k], u=smooth(clamp(fr * 1.5)))
    return lambda lz, t: _ov(f, lz, t)


def _ov(f, lz, t):
    p = P()
    f(p, t)
    tmp = np.empty_like(lz)
    p.fin(tmp)
    lz += tmp


@esc("ca_intentos", lambda: INI("camino", 1), lambda: FIN("camino", 1))
def ca_intentos(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.02, 0.03, 0.05), (0.07, 0.09, 0.13), 0, 0.9)
    p.glow(1000, 560, 800, (0.9, 0.95, 1.0), 0.3)
    # antebrazo horizontal (primer plano) con la vena marcada
    skin = (0.45, 0.30, 0.25)
    p.poly([(200, 640), (1700, 560), (1700, 840), (200, 860)], skin, grad=((0.55, 0.38, 0.31), (0.32, 0.20, 0.16)))
    p.polilinea([(260, 735), (700, 722), (1200, 710), (1660, 700)], 22, (0.28, 0.30, 0.52), 0.8)
    p.polilinea([(260, 735), (700, 722), (1200, 710), (1660, 700)], 8, (0.45, 0.46, 0.75), 0.6)
    # agujas que intentan y fallan; cada intento tiene su cruz
    n = 7
    t0 = INI("camino", 1) + 0.6
    per = (FIN("camino", 1) - t0 - 0.4) / n
    for k in range(n):
        tk = t0 + k * per
        u = pr(t, tk, tk + per * 0.5)
        if 0 < u:
            x = 400 + k * 190
            gy = lerp(120, 700 + 16 * math.sin(k * 1.9), ease_out(min(1.0, u * 1.8)) if u < 0.6 else 1.0)
            ret = pr(t, tk + per * 0.45, tk + per * 0.78)
            gy = lerp(gy, 120, ease_out(ret))
            p.linea((x, gy - 360), (x + 18, gy), 7, (0.85, 0.88, 0.92))
            p.linea((x, gy - 360), (x, gy - 420), 26, (0.7, 0.72, 0.76))
            cruz(p, x + 10, 905, 34, pr(t, tk + per * 0.3, tk + per * 0.55), ROJO, 14)
    p.glow(1000, 700, 200, (1, 0.2, 0.2), 0.0)
    # reloj de 'más de una hora'
    reloj(p, 1650, 270, 150, 0.0, h=8.0, m=(t - INI("camino", 1)) * 6.0, segundero=False)
    vineta_p(p, 0.55)
    _cam(p, tl, dur, 1.0, 1.06, 0.5, 0.7)
    p.fin(lz)


@esc("ca_sangre", lambda: INI("camino", 2), lambda: FIN("camino", 2))
def ca_sangre(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.05, 0.01, 0.02), (0.14, 0.03, 0.05), 0, 1.0)
    # vaso sanguíneo (tubo) con glóbulos que fluyen y un coágulo que lo va tapando
    y0 = 560
    p.rect(-10, y0 - 190, W + 10, y0 + 190, (0.30, 0.04, 0.07), grad=((0.46, 0.08, 0.10), (0.22, 0.02, 0.05)))
    p.rect(-10, y0 - 210, W + 10, y0 - 190, (0.55, 0.20, 0.18), 0.7)
    p.rect(-10, y0 + 190, W + 10, y0 + 210, (0.2, 0.05, 0.08), 0.8)
    obst = smooth(pr(t, INI("camino", 2) + 0.8, FIN("camino", 2) - 0.5))
    rng = np.random.default_rng(3)
    for k in range(70):
        fila = (k * 53) % 330 - 165
        vel = 380 * (1 - 0.88 * obst * (abs(fila) < 120))
        x = ((k * 211) + t * vel * (0.7 + (k % 5) * 0.12)) % (W + 200) - 100
        y = y0 + fila * (0.7 if x < 1000 else 0.7) + 14 * math.sin(t * 2 + k)
        p.elip(x, y, 40, 22, 20 * math.sin(k), (0.82, 0.10, 0.12), 0.95)
        p.elip(x, y, 14, 8, 20 * math.sin(k), (0.5, 0.04, 0.07), 0.9)
    # coágulo amarillento que crece en el centro
    r = 40 + 190 * obst
    p.elip(1100, y0 + 40, r * 1.3, r * 0.9, 12, (0.90, 0.74, 0.28), 0.9 * min(1, obst * 3))
    p.elip(1080, y0 + 20, r * 0.8, r * 0.5, 12, (1.0, 0.9, 0.5), 0.6 * min(1, obst * 3))
    # aguja que se acerca
    ag = ease_out(pr(t, INI("camino", 2) + 1.4, INI("camino", 2) + 2.4))
    p.linea((520 - 420 * (1 - ag), 60 - 120 * (1 - ag)), (1000, y0 - 140), 9, (0.85, 0.88, 0.92))
    p.texto("HISTORIAL MÉDICO", 960, 960, 64, CREMA, "sans_b", smooth(pr(t, ww("camino", 2, "historial", sep=-0.1), ww("camino", 2, "historial", sep=0.3))))
    vineta_p(p, 0.6)
    _cam(p, tl, dur, 1.0, 1.07, 0.55, 0.5)
    p.fin(lz)
