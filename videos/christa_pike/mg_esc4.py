# -*- coding: utf-8 -*-
"""Escenas dibujadas, parte 4: después, historial, precedente, cierre."""
import math

import numpy as np

from mg_esc import *  # noqa: F401,F403
from mg_esc import ESC, esc, _cam, _sala, _lamp


# ====================================================================== DESPUÉS
def habitacion(p, t, z=1.0):
    """Habitación de hospital de noche: ventana con ciudad y lluvia, paciente en cama con respirador y monitor."""
    p.fondo((0.03, 0.05, 0.08), (0.10, 0.14, 0.18))
    # ventana con ciudad
    p.rect(1180, 120, 1780, 560, (0.02, 0.03, 0.06))
    ciudad(p, t, 560, (0.01, 0.015, 0.03), off=t * 6, seed=21, h_max=240, ancho_med=70)
    p.rect(1170, 110, 1790, 128, (0.2, 0.22, 0.26)); p.rect(1170, 552, 1790, 570, (0.2, 0.22, 0.26)); p.rect(1470, 110, 1480, 570, (0.2, 0.22, 0.26))
    lluvia(p, t, 0.25, 40, seed=3)
    suelo(p, 820, (0.07, 0.09, 0.12), (0.02, 0.03, 0.05))
    p.glow(560, 90, 800, (0.7, 0.9, 1.0), 0.28)
    # cama de hospital con paciente
    camilla(p, 640, 690, 980, (0.80, 0.86, 0.92), correas=False)
    acostada(p, 600, 640, 760, (0.12, 0.14, 0.2), t, brazo=0.3, resp=1.6)
    # respirador: fuelle que sube y baja + tubo a la boca
    br = 0.5 + 0.5 * math.sin(t * 2.0)
    p.rrect(150, 520, 300, 760, 16, (0.16, 0.2, 0.26))
    p.rrect(172, 560 + 90 * (1 - br), 278, 740, 10, (0.55, 0.78, 0.88), 0.9)
    p.rect(172, 540, 278, 556, (0.3, 0.34, 0.4))
    p.polilinea([(300, 600), (360, 560), (400, 620), (470, 640)], 10, (0.65, 0.85, 0.92), 0.8)
    # monitor cardiaco
    p.rect(1010, 480, 1020, 820, (0.3, 0.32, 0.36))
    monitor_marco(p, 800, 400, 1080, 520)
    ecg(p, 810, 470, 260, 38, t, vel=210, ritmo=1.0, grosor=4)
    p.texto("SpO2 89", 940, 420, 22, (0.4, 0.95, 0.9), "mono")
    bolsa_iv(p, 1150, 200, 300, t, tubo_a=(780, 640))
    polvo(p, t, 30, op=0.25, color=(0.6, 0.9, 1.0))


@esc("de_hospital", lambda: INI("despues", 0), lambda: INI("despues", 1))
def de_hospital(lz, tl, t, dur, ext):
    p = P()
    habitacion(p, t)
    vineta_p(p, 0.55)
    _cam(p, tl, dur, 1.0, 1.12, 0.35, 0.65)
    p.fin(lz)


@esc("de_monitor", lambda: INI("despues", 1), lambda: INI("despues", 2))
def de_monitor(lz, tl, t, dur, ext):
    p = P()
    habitacion(p, t)
    vineta_p(p, 0.55)
    z = lerp(1.0, 1.55, smooth(tl / max(dur, 1)))
    zoom_p(p, z, 0.17, 0.75)
    p.fin(lz)


@esc("de_protocolo", lambda: INI("despues", 5), lambda: FIN("despues", 5))
def de_protocolo(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.10, 0.075, 0.06), (0.025, 0.02, 0.02))
    p.glow(960, 500, 1000, (1.0, 0.8, 0.5), 0.3)
    documento(p, 700, 560, 760, 860, ang=-0.04, lineas=0, titulo=False)
    p.texto("PROTOCOLO", 700, 220, 62, (0.12, 0.10, 0.10), "sans_b")
    pasos = ["Vía intravenosa", "Primera dosis", "Cinco minutos", "Segunda dosis", "Traslado médico"]
    T0 = INI("despues", 5)
    for k, s in enumerate(pasos):
        y = 340 + k * 100
        p.texto(s, 420, y, 44, (0.18, 0.16, 0.16), "sans_l", anchor="lm")
        check(p, 960, y, 26, smooth(pr(t, T0 + 0.5 + k * 0.45, T0 + 0.9 + k * 0.45)), (0.2, 0.7, 0.35), 9)
    ts = ww("despues", 5, "conforme", sep=-0.2)
    ap = ease_back(pr(t, ts, ts + 0.5))
    if ap > 0.02:
        p.polilinea([(1300 + 100 * math.cos(a) * ap, 540 + 100 * math.sin(a) * ap) for a in np.linspace(0, 6.28, 30)], 10, (0.2, 0.7, 0.35), 0.9, cerrado=True)
        check(p, 1300, 540, 90 * ap, pr(t, ts + 0.1, ts + 0.7), (0.2, 0.8, 0.4), 22)
        p.texto("CONFORME", 1300, 720, 50 * ap, (0.3, 0.9, 0.5), "sans_b", clamp(ap))
    vineta_p(p, 0.55)
    _cam(p, tl, dur, 1.0, 1.05)
    p.fin(lz)


@esc("de_sistema", lambda: INI("despues", 6), lambda: FIN("despues", 6))
def de_sistema(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.03, 0.03, 0.05), (0.07, 0.07, 0.10))
    T0 = INI("despues", 6)
    falla = smooth(pr(t, ww("despues", 6, "falla", sep=-0.2), ww("despues", 6, "persona", sep=0.2)))
    disp = [(300, 360, 150, 1), (600, 280, 100, -1), (800, 560, 190, 1), (1120, 420, 120, -1), (1420, 300, 150, 1), (1560, 640, 100, -1), (1020, 780, 150, -1),
            (560, 760, 110, 1), (1800, 480, 90, 1)]
    w = 1.0 - 0.95 * falla
    for k, (x, y, r, d) in enumerate(disp):
        rojo = clamp(falla * 1.8 - 0.14 * k) if k else clamp(falla * 3)
        col = mix((0.40, 0.44, 0.50), (0.80, 0.12, 0.12), rojo)
        engranaje(p, x, y, r, t * 0.55 * w * d * (150 / r), col, dientes=max(8, int(r / 9)))
    # grieta que se abre en el engranaje central
    if falla > 0.05:
        pts = [(800, 560)] + [(800 + 70 * math.sin(s * 5) + s * 60, 560 + s * 190) for s in np.linspace(0.1, 1, 8)]
        p.polilinea(pts[:max(2, int(len(pts) * falla))], 9, (0.05, 0.01, 0.01), 1.0)
        p.glow(800, 560, 420 * falla, (1.0, 0.15, 0.1), 0.6)
    p.texto("FALLA SISTÉMICA", 960, 960, 76, CREMA, "sans_b", smooth(pr(t, ww("despues", 6, "falla", sep=-0.1), ww("despues", 6, "falla", sep=0.5))))
    vineta_p(p, 0.55)
    _cam(p, tl, dur, 1.0, 1.05)
    p.fin(lz)


# ====================================================================== HISTORIAL
@esc("hs_prision", lambda: INI("historial", 1), lambda: INI("historial", 3))
def hs_prision(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.006, 0.01, 0.025), (0.06, 0.08, 0.13), 0, 0.85)
    estrellas(p, t, 80, y_max=0.5, brillo=0.7)
    luna(p, 1560, 160, 46, halo=0.8)
    colinas(p, 860, 130, (0.02, 0.03, 0.05), off=t * 2, seed=75)
    niebla(p, t, 900, 140, (0.35, 0.45, 0.6), 0.3, vel=7, seed=7)
    prision(p, 960, 960, 1100, t)
    p.rect(-10, 960, W + 10, H + 10, (0.012, 0.016, 0.024))
    p.glow(960, 940, 800, (1.0, 0.8, 0.45), 0.25)
    lluvia(p, t, 0.15, 50)
    vineta_p(p, 0.6)
    _cam(p, tl, dur, 1.0, 1.07, 0.5, 0.7)
    p.fin(lz)


@esc("hs_cuatro", lambda: INI("historial", 3), lambda: FIN("historial", 3))
def hs_cuatro(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.03, 0.03, 0.05), (0.09, 0.09, 0.12), 0, 0.9)
    p.haz(960, -40, 90, 1100, 70, (0.95, 0.97, 1.0), 0.35)
    suelo(p, 900, (0.08, 0.08, 0.1), (0.02, 0.02, 0.03))
    T0 = ww("historial", 3, "cuatro", sep=-0.2)
    for k in range(4):
        tk = T0 + k * 0.5
        a = smooth(pr(t, tk, tk + 0.4))
        x = 560 + k * 270
        gris = mix((0.02, 0.025, 0.04), (0.16, 0.17, 0.2), a)
        persona(p, x, 960, 520, pose_estar(t + k, 0.0), gris, ropa="chaqueta" if k % 2 else "pantalon", pelo="corto")
        p.texto(str(k + 1), x, 330, 120 * ease_back(pr(t, tk, tk + 0.4)), ROJO, "abril", clamp(a * 2))
    vineta_p(p, 0.6)
    _cam(p, tl, dur, 1.0, 1.06)
    p.fin(lz)


@esc("hs_dos", lambda: INI("historial", 4), lambda: FIN("historial", 4))
def hs_dos(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.04, 0.04, 0.06), (0.10, 0.10, 0.13), 0, 1.0)
    p.glow(960, 700, 1000, (0.6, 0.7, 0.9), 0.25)
    T0 = INI("historial", 4)
    for k, (x, tt) in enumerate(((620, ww("historial", 4, "segunda", sep=-0.2)), (1300, ww("historial", 4, "fallida", sep=-0.1)))):
        u = ease_out(pr(t, T0 + 0.1 + k * 0.5, T0 + 0.9 + k * 0.5))
        documento(p, x, lerp(1300, 700, u), 560, 700, ang=lerp(0.2, -0.04 + 0.08 * k, u), lineas=8, titulo=True)
        p.texto("EJECUCIÓN" , x, lerp(1300, 700, u) - 40, 40, (0.12, 0.10, 0.10), "sans_b", u)
        ap = ease_back(pr(t, tt, tt + 0.35))
        if ap > 0.03:
            p.texto("FALLIDA", x, 760 - 20 * ap, 100 * ap, ROJO, "abril", clamp(ap), stroke=0)
            cruz(p, x, 720, 190 * ap, pr(t, tt + 0.1, tt + 0.5), ROJO, 22)
    vineta_p(p, 0.55)
    _cam(p, tl, dur, 1.0, 1.05)
    p.fin(lz)


@esc("hs_vial", lambda: INI("historial", 5), lambda: FIN("historial", 5))
def hs_vial(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.03, 0.04, 0.07), (0.09, 0.11, 0.16), 0, 1.0)
    p.glow(700, 560, 900, (0.5, 0.7, 0.9), 0.3)
    # frasco con etiqueta
    p.rrect(540, 320, 880, 880, 40, (0.85, 0.92, 0.96), 0.35)
    p.rrect(556, 520, 864, 868, 30, (0.95, 0.88, 0.45), 0.75)
    p.rrect(540, 250, 880, 330, 22, (0.15, 0.2, 0.3))
    p.rect(580, 560, 840, 780, CREMA)
    p.texto("PENTOBARBITAL", 710, 620, 36, (0.12, 0.10, 0.10), "sans_b")
    p.texto("1 dosis", 710, 690, 34, (0.3, 0.28, 0.26), "sans_l")
    # jeringa que se llena
    u = smooth(pr(t, INI("historial", 5) + 0.8, FIN("historial", 5) - 0.6))
    jeringa(p, 1360, 600, math.pi + 0.5, 760, 1 - u, (0.95, 0.88, 0.45))
    # burbujas dentro del frasco
    for k in range(8):
        s = (t * 0.25 + k / 8) % 1.0
        p.circ(620 + (k * 41) % 240, 840 - s * 300, 7 + (k % 3) * 3, (1, 1, 0.8), 0.5 * (1 - s))
    p.texto("desde 2024 · único fármaco", 1100, 960, 40, CREMA, "sans_l", smooth(pr(t, INI("historial", 5) + 2.5, INI("historial", 5) + 3.2)))
    vineta_p(p, 0.55)
    _cam(p, tl, dur, 1.0, 1.06)
    p.fin(lz)


# ====================================================================== PRECEDENTE
@esc("pr_busqueda", lambda: INI("precedente", 0), lambda: FIN("precedente", 0))
def pr_busqueda(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.06, 0.05, 0.05), (0.02, 0.02, 0.025), 0, 1.0)
    p.glow(960, 540, 1100, (1.0, 0.85, 0.55), 0.25)
    T0 = INI("precedente", 0)
    cols, filas = 7, 3
    for r in range(filas):
        for c in range(cols):
            x = 340 + c * 200
            y = 300 + r * 250
            u = ease_out(pr(t, T0 + 0.1 + (r * cols + c) * 0.05, T0 + 0.5 + (r * cols + c) * 0.05))
            documento(p, x, lerp(y + 400, y, u), 150, 190, ang=(((r * 5 + c * 3) % 7) - 3) * 0.03, lineas=5, titulo=False, op=u)
    # lupa que recorre la pared
    lx = 340 + 1200 * smooth((math.sin(tl * 0.8 - 0.8) + 1) / 2)
    ly = 300 + 500 * smooth((math.sin(tl * 0.55) + 1) / 2)
    lupa(p, lx, ly, 120, ang=-0.8)
    ap = ease_back(pr(t, ww("precedente", 0, "conoce", sep=-0.2), ww("precedente", 0, "conoce", sep=0.5)))
    if ap > 0.02:
        p.texto("NINGÚN CASO IGUAL", 960, 940, 72 * ap, ROJO, "abril", clamp(ap))
    vineta_p(p, 0.55)
    _cam(p, tl, dur, 1.0, 1.05)
    p.fin(lz)


@esc("pr_luisiana", lambda: INI("precedente", 1), lambda: FIN("precedente", 1))
def pr_luisiana(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.03, 0.05, 0.09), (0.05, 0.08, 0.13))
    z = lerp(1.0, 5.5, ease_out(pr(t, INI("precedente", 1), INI("precedente", 1) + 2.4)))
    mapa_us(p, resaltar=("Louisiana",), zoom=(-91.8, 31.0, z), color=(0.08, 0.13, 0.21), color_res=(0.42, 0.34, 0.14))
    ox, oy = proy_us(-91.1, 30.5)
    cxz, cyz = proy_us(-91.8, 31.0)
    x, y = 960 + (ox - cxz) * z, 540 + (oy - cyz) * z
    if t > INI("precedente", 1) + 1.6:
        pin(p, x, y, 22, ROJO, t)
        p.texto("Luisiana", x + 60, y - 80, 58, CREMA, "sans_b", smooth(pr(t, INI("precedente", 1) + 1.8, INI("precedente", 1) + 2.4)), anchor="lm")
    vineta_p(p, 0.55)
    p.fin(lz)


@esc("pr_abogados", lambda: INI("precedente", 5), lambda: FIN("precedente", 5))
def pr_abogados(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.06, 0.09, 0.16), (0.30, 0.34, 0.44), 0, 0.8)
    p.glow(300, 700, 900, (1.0, 0.8, 0.55), 0.35)
    columnas(p, 1330, 930, 880, 720, (0.74, 0.74, 0.72), n=7)
    p.rect(-10, 930, W + 10, H + 10, (0.05, 0.06, 0.08))
    for k in range(4):
        x = lerp(-250 - k * 230, 980 + k * 70, smooth(pr(t, INI("precedente", 5) - 0.2 + k * 0.1, FIN("precedente", 5) + 0.5)) ** 0.9)
        persona(p, x, 1020 + (k % 2) * 20, 420, pose_caminar(t * 5.0 + k), (0.01, 0.012, 0.02), ropa="chaqueta", pelo="largo" if k == 2 else "corto", bolso=True)
    vineta_p(p, 0.5)
    _cam(p, tl, dur, 1.0, 1.05, 0.6, 0.6)
    p.fin(lz)


# ====================================================================== CIERRE
@esc("ci_ciudad", lambda: INI("cierre", 0), lambda: FIN("cierre", 0))
def ci_ciudad(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.006, 0.012, 0.03), (0.07, 0.10, 0.17), 0, 0.85)
    estrellas(p, t, 100, y_max=0.55, brillo=0.8)
    luna(p, 1480, 200, 60, halo=0.9)
    ciudad(p, t, 880, (0.015, 0.02, 0.04), off=t * 6, seed=31, h_max=520)
    ciudad(p, t, 960, (0.006, 0.01, 0.02), off=t * 14, seed=32, h_max=380, ancho_med=160)
    # edificio del hospital con una ventana que late
    hx = 560
    p.rect(hx - 150, 560, hx + 150, 960, (0.02, 0.03, 0.05))
    p.rect(hx - 20, 500, hx + 20, 560, (0.7, 0.12, 0.12)); p.rect(hx - 8, 510, hx + 8, 550, (1, 1, 1)); p.rect(hx - 18, 522, hx + 18, 538, (1, 1, 1))
    for r in range(4):
        for c in range(5):
            p.rect(hx - 120 + c * 52, 600 + r * 80, hx - 90 + c * 52, 640 + r * 80, (0.9, 0.8, 0.5), 0.5)
    pul = 0.5 + 0.5 * math.sin(t * 2.2)
    p.rect(hx - 68, 680, hx - 38, 720, (1.0, 0.45, 0.35), 0.6 + 0.4 * pul)
    p.glow(hx - 53, 700, 300 + 120 * pul, (1.0, 0.35, 0.25), 0.8)
    p.rect(-10, 960, W + 10, H + 10, (0.008, 0.01, 0.015))
    lluvia(p, t, 0.15, 40)
    vineta_p(p, 0.6)
    _cam(p, tl, dur, 1.0, 1.1, 0.3, 0.65)
    p.fin(lz)


@esc("ci_sala", lambda: INI("cierre", 1), lambda: FIN("cierre", 1))
def ci_sala(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.01, 0.015, 0.025), (0.04, 0.05, 0.07))
    x0, y0, x1, y1 = 470, 90, 1450, 650
    ventana_obs(p, x0, y0, x1, y1, (0.45, 0.50, 0.46))
    p.rect(x0, y1 - 120, x1, y1, (0.28, 0.32, 0.28))
    camilla(p, 960, y1 - 190, 700, (0.88, 0.9, 0.93))
    p.glow(960, y0 + 20, 700, (0.85, 1.0, 0.95), 0.35)
    p.rect(x0 + 90, y0 + 40, x0 + 94, y1 - 100, (0.35, 0.37, 0.4))
    # polvo flotando en la luz de la sala vacía
    polvo(p, t, 40, op=0.5, color=(0.9, 1.0, 0.95))
    for k in range(2):
        p.haz(960, y0 + 4, 90, 520, 28, (0.9, 1.0, 0.95), 0.2)
    persianas(p, x0, y0, x1, y1, 0.9 - 0.05 * math.sin(t))
    for fila, (yy, hh, col) in enumerate(((900, 260, (0.006, 0.008, 0.012)), (1030, 340, (0.004, 0.005, 0.008)))):
        for i in range(8 if fila == 0 else 7):
            xx = 130 + i * 240 + (70 if fila else 0)
            silueta_sentada_vista_trasera(p, xx, yy, hh * (0.85 + 0.25 * ((i * 37 % 10) / 10)), col)
    vineta_p(p, 0.6)
    _cam(p, tl, dur, 1.0, 1.08, 0.5, 0.4)
    p.fin(lz)


@esc("ci_discuten", lambda: INI("cierre", 2), lambda: FIN("cierre", 2))
def ci_discuten(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.05, 0.07, 0.12), (0.12, 0.15, 0.22), 0, 0.85)
    colinas(p, 820, 160, (0.04, 0.06, 0.09), off=t * 3, seed=88)
    p.rect(-10, 940, W + 10, H + 10, (0.015, 0.02, 0.03))
    grupos = [(460, "?", ROJO), (960, "!", CALIDO), (1460, "…", CREMA)]
    for g, (x, sym, col) in enumerate(grupos):
        for k in range(3):
            xx = x + (k - 1) * 150
            persona(p, xx, 1030 + (k % 2) * 16, 430 - (k % 2) * 30, pose_señalar(0.5 + 0.5 * math.sin(t * 2.2 + k + g)) if k != 1 else pose_estar(t + g),
                    (0.01, 0.012, 0.02), facing=1 if k < 1 else -1, ropa="vestido" if (g + k) % 3 == 0 else "chaqueta", pelo="largo" if (g + k) % 3 == 0 else "corto")
        tb = INI("cierre", 2) + 1.0 + g * 1.4
        for j in range(3):
            tj = tb + j * 0.5
            ap = ease_back(pr(t, tj, tj + 0.35))
            if ap > 0.02:
                bx, by = x - 110 + j * 110, 330 - j * 50 + 10 * math.sin(t * 2 + j)
                p.elip(bx, by, 78 * ap, 56 * ap, 0, CREMA, 0.92)
                p.poly([(bx - 20, by + 40), (bx - 40, by + 92), (bx + 8, by + 50)], CREMA, 0.92)
                p.texto(sym, bx, by - 2, 80 * ap, mix(col, (0, 0, 0), 0.0) if sym != "…" else (0.1, 0.1, 0.12), "abril" if sym != "…" else "sans_b", clamp(ap * 1.5))
    vineta_p(p, 0.5)
    _cam(p, tl, dur, 1.0, 1.05)
    p.fin(lz)


@esc("ci_vela", lambda: INI("cierre", 3), lambda: FIN("cierre", 3))
def ci_vela(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.006, 0.006, 0.01), (0.03, 0.025, 0.03), 0, 1.0)
    p.glow(1450, 560, 1100, (1.0, 0.6, 0.25), 0.35)
    vela(p, 1450, 920, 340, t)
    polvo(p, t, 50, op=0.5, color=(1.0, 0.8, 0.5))
    vineta_p(p, 0.7)
    _cam(p, tl, dur, 1.0, 1.05, 0.7, 0.6)
    p.fin(lz)


# ====================================================================== escenas extra
@esc("q_atras", lambda: INI("quien", 0), lambda: FIN("quien", 0))
def q_atras(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.02, 0.025, 0.05), (0.08, 0.10, 0.16))
    estrellas(p, t, 70, y_max=0.9, brillo=0.5)
    T0, T1 = INI("quien", 0), FIN("quien", 0)
    u = pr(t, T0 + 0.6, T1 - 0.2)
    p.glow(960, 540, 1000, (0.35, 0.45, 0.7), 0.35)
    reloj(p, 960, 520, 430, 0.0, h=6.0, m=-(t - T0) * 260.0, segundero=False, cara=(0.55, 0.60, 0.72), op=0.38)
    # hojas de calendario que se desprenden hacia atrás (vuelan a la cámara y se alejan)
    for k in range(10):
        s = ((t - T0) * 0.55 + k / 10) % 1.0
        z = 0.35 + 1.6 * s
        a = 1.0 - abs(2 * s - 1) ** 2
        ang = (k * 0.7) + s * 1.8
        R = rot((960, 540), ang)
        cx_, cy_ = R((960 + (k % 5 - 2) * 330 * z, 540 + ((k * 3) % 4 - 1.5) * 190 * z))
        if -250 < cx_ < W + 250 and -250 < cy_ < H + 250:
            documento(p, cx_, cy_, 190 * z, 230 * z, ang=ang * 0.4, lineas=3, titulo=False, sombra=False, op=0.28 * a)
    rodillo(p, 960, 560, 2026, 1995, u, 330, ROJO)
    p.texto("HACE MÁS DE 30 AÑOS", 960, 860, 56, CREMA, "sans_b", smooth(pr(t, T0 + 1.5, T0 + 2.2)))
    vineta_p(p, 0.55)
    p.fin(lz)


@esc("cr_luto", lambda: INI("crimen", 4), lambda: FIN("crimen", 4))
def cr_luto(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.006, 0.01, 0.025), (0.05, 0.07, 0.11), 0, 0.85)
    estrellas(p, t, 80, y_max=0.5, brillo=0.7)
    luna(p, 1400, 200, 56, halo=1.0)
    bosque(p, 960, 560, (0.012, 0.018, 0.03), off=t * 3, seed=6, n=12, pelados=True)
    niebla(p, t, 920, 260, (0.4, 0.5, 0.62), 0.4, vel=7, seed=14)
    p.rect(-10, 990, W + 10, H + 10, (0.004, 0.006, 0.01))
    vela(p, 960, 1000, 120, t)
    polvo(p, t, 30, op=0.4, color=(1.0, 0.8, 0.5))
    vineta_p(p, 0.7)
    _cam(p, tl, dur, 1.0, 1.1, 0.5, 0.8)
    p.fin(lz)


@esc("j_testigo", lambda: ww("juicio", 1, "amiga", sep=-0.3), lambda: FIN("juicio", 1))
def j_testigo(lz, tl, t, dur, ext):
    p = P()
    p.fondo((0.05, 0.04, 0.05), (0.14, 0.09, 0.07), 0, 0.9)
    p.rect(-10, 820, W + 10, H + 10, (0.07, 0.045, 0.035))
    p.glow(560, 300, 700, (1.0, 0.8, 0.5), 0.3)
    # estrado del juez al fondo, bandera, banco del testigo en primer plano
    p.rect(900, 520, 1800, 700, (0.20, 0.11, 0.07), grad=((0.28, 0.16, 0.09), (0.12, 0.07, 0.04)))
    persona(p, 1350, 530, 300, pose_estar(t), (0.02, 0.015, 0.02), ropa="vestido", pelo="corto")
    p.rect(1880, 260, 1888, 700, (0.5, 0.5, 0.52))
    p.poly([(1888, 270), (1920, 270 + 6 * math.sin(t * 3)), (1920, 360 + 8 * math.sin(t * 3)), (1888, 340)], (0.7, 0.12, 0.14))
    p.rect(300, 600, 780, 900, (0.24, 0.13, 0.08), grad=((0.32, 0.18, 0.10), (0.14, 0.08, 0.05)))
    p.rect(280, 580, 800, 620, (0.40, 0.24, 0.14))
    persona(p, 540, 600, 520, pose_estar(t * 1.2 + 1.0) | dict(bl=(0.2, 0.2), br=(0.9 + 0.1 * math.sin(t * 2), 0.3)), (0.02, 0.015, 0.02), ropa="vestido", pelo="moño")
    p.linea((650, 590), (700, 520), 6, (0.1, 0.1, 0.12)); p.circ(704, 512, 18, (0.12, 0.12, 0.14))       # micrófono
    for i in range(7):
        silueta_sentada_vista_trasera(p, 150 + i * 280 + (i % 2) * 40, 960 + (i % 2) * 40, 250, (0.008, 0.006, 0.008))
    vineta_p(p, 0.55)
    _cam(p, tl, dur, 1.0, 1.06, 0.4, 0.55)
    p.fin(lz)
