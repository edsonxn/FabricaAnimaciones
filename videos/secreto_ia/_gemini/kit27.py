# -*- coding: utf-8 -*-
"""Utilería propia de «El informante que le puso fecha al final» (estilo noir). Todo se dibuja con h.pieza / h.trazo (mundo).

    pared(h, tono, grad, ladrillo)            fondo de pared a pantalla completa
    hoja(h, cx, cy, w, hh, ang, renglones)    hoja de papel con renglones impresos -> función T (local -> mundo)
    calendario(h, t, t0, mes, num, anio, ...) hoja de calendario que cae y se clava
    carpeta(h, cx, cy, s, titulo, t, ...)     el EXPEDIENTE (carpeta de cartón con pestaña y título)
    billetes / casa / balanza / pluma / garabato / chip / interruptor / reloj_arena / puerta / flecha / barra
    mano_alzada(h, x, y, s, sube)             brazo que se levanta desde abajo (votación)
    multitud(h, t, x0, x1, y, n, ...)         siluetas con ritmo propio y pancartas
    robot(h, x, y, s, t)                      humanoide de fábrica (visor que emite)
    pantalla_codigo(h, caja, t)               renglones de código que corren dentro de una pantalla
    cajas(h, t, n, ...)                       rejilla de «copias» (monolitos con su luz) que se encienden en oleada
"""
import math

import numpy as np

import noir as N
import props as PR
from motor import H, W, clamp01, e_out, smooth
from noir import gris
from noir_pers import avance_paso, cadera_paso, pierna_paso
from toon import elipse_, suave, tubo

rect, rot = PR.rect, PR.rot
IMPACT = "C:/Windows/Fonts/impact.ttf"
DAN = dict(pelo="oscuro", barba=True, traje=66)          # Daniel (Frontal(sem=77)): el mismo en todo el video


def plano_(h, P, tono, sem, alfa=1.0, grad=None):
    """Relleno liso sin tinta ni sombra (pantallas, huecos, fondos)."""
    h.pieza(P, tono, sem, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False, jit=0, alfa=alfa, grad=grad)


def pared(h, tono=56, grad=22, ladrillo=False, sem=5, paneles=0):
    plano_(h, rect(-400, -400, W + 800, H + 800), tono, sem, grad=(grad, 0, H))
    if ladrillo:
        for k in range(10):
            for j in range(13):
                xx = -80 + j * 170 + (85 if k % 2 else 0)
                h.anillo(h.tf(rect(xx, -40 + k * 120, 164, 114)), 2.5 * h.zoom, sem + 100 + k * 13 + j, alfa=0.3, jit=0.6)
    for k in range(paneles):                                  # paneles de madera verticales
        x = -200 + k * (W + 400) / paneles
        h.trazo(np.array([[x, -200], [x + 4, H + 200]]), 5, sem + 300 + k, alfa=0.45, jit=0.5)


def hoja(h, cx, cy, w=620, hh=820, ang=0.0, sem=0, tono=226, renglones=0, y0=0.24, sep=44, margen=70, s=1.0):
    """Hoja de papel. Devuelve T(P) para colocar cosas encima en coordenadas locales (0,0 = centro; px sin escalar)."""
    c = np.array([cx, cy], float)

    def T(P):
        return rot(np.asarray(P, float).reshape(-1, 2) * s + c, ang, c)
    h.pieza(T(rect(-w / 2, -hh / 2, w, hh)), tono, sem, w=4, luz=(0.2, -1), d=10, trama=0, rim=0)
    N.soporte(h, cx, cy, w, hh, ang, s)                     # el texto que se escriba encima sale paralelo a la hoja y dentro de ella
    r = np.random.default_rng(sem + 7)
    for k in range(renglones):
        y = -hh / 2 + hh * y0 + k * sep
        if y > hh / 2 - margen * 0.6:
            break
        L = (w - 2 * margen) * r.uniform(0.62, 1.0)
        plano_(h, T(rect(-w / 2 + margen, y, L, 7)), 118, sem + 20 + k, alfa=0.75)
    return T


def calendario(h, t, t0, mes, num, anio="", cx=520, cy=520, s=1.0, sem=20, ang=-0.05, px_num=None):
    """Hoja de calendario de taco: cae desde arriba y se clava. num = texto grande (día o año)."""
    cae = e_out(clamp01((t - t0 + 0.3) / 0.45))
    hy = cy - 900 * (1 - cae)
    c = np.array([cx, hy])
    a = ang + 0.25 * (1 - cae)
    h.pieza(rot(rect(cx - 290 * s, hy - 360 * s, 580 * s, 720 * s), a, c), 226, sem, w=5, luz=(0.2, -1), d=12, trama=0, rim=0)
    plano_(h, rot(rect(cx - 290 * s, hy - 360 * s, 580 * s, 150 * s), a, c), 28, sem + 1)
    for q in (-1, 1):                                          # anillas
        h.pieza(elipse_(cx + q * 170 * s, hy - 372 * s, 16 * s, 26 * s, n=16), 150, sem + 2 + q, w=4, luz=(0, -1), d=4, trama=0, rim=0.8)
    if cae > 0.97:
        N.texto_maquina(h, mes, cx + 10 * s, hy - 285 * s, 92 * s, t, -99, cps=1e9, tono=0.96, centro=True, fuente=N.FUENTE_SELLO,
                        encuadrar=False)
        px = px_num or (400 if len(num) <= 2 else 250)
        N.texto_maquina(h, num, cx - 4 * s, hy + (10 if anio else 60) * s, px * s, t, -99, cps=1e9, tono=0.04, centro=True,
                        fuente=N.FUENTE_SELLO, encuadrar=False)
        if anio:
            N.texto_maquina(h, anio, cx - 10 * s, hy + 280 * s, 80 * s, t, -99, cps=1e9, tono=0.10, centro=True, fuente=N.FUENTE_SELLO,
                            encuadrar=False)
    return cae


def carpeta(h, cx, cy, s=1.0, titulo="2027", t=0.0, t0=-99, ang=-0.04, sem=0, abre=0.0, sub="EXPEDIENTE", px=230):
    """Carpeta de cartón manila con pestaña, cinta y título estampado. abre 0..1 levanta la tapa (se ve el papel)."""
    c = np.array([cx, cy], float)

    def T(P):
        return rot(np.asarray(P, float).reshape(-1, 2) * s + c, ang, c)
    h.pieza(T([(-420, -300), (-150, -300), (-110, -350), (140, -350), (180, -300), (420, -300), (420, 300), (-420, 300)]), 96, sem,
            w=6, luz=(0.25, -1), d=18, trama=0.5, rim=0.6)
    if abre > 0:
        h.pieza(T(rect(-380, -270 - 40 * abre, 760, 540)), 228, sem + 1, w=4, luz=(0.2, -1), d=8, trama=0, rim=0)
        for k in range(9):
            plano_(h, T(rect(-320, -200 + k * 46, 640 * (0.7 + 0.3 * math.sin(k * 2.3) ** 2), 7)), 120, sem + 30 + k, alfa=0.7)
    y_t = 300 - 600 * (1 - 0.82 * abre)
    tapa = [(-420, y_t), (420, y_t), (420 + 30 * abre, 300), (-420 - 30 * abre, 300)]
    h.pieza(T(tapa), 132 - 30 * abre, sem + 2, w=6, luz=(0.25, -1), d=16, trama=0.4, rim=0.7)
    if abre < 0.25:
        plano_(h, T(rect(-420, -40, 840, 26)), 40, sem + 3, alfa=0.85)                           # cinta
        N.soporte(h, cx, cy, 840, 600, ang, s)
        P = T([(0, -150)])[0]
        N.texto_maquina(h, sub, P[0], P[1], 50 * s, t, -99, cps=1e9, tono=0.10, centro=True, fuente=N.FUENTE_SELLO, encuadrar=False)
        if t >= t0:                                             # el título cae como un golpe de tampón (tinta sólida: se lee siempre)
            k = 1.0 + 0.35 * (1 - clamp01((t - t0) / 0.14)) ** 2
            P = T([(0, 140)])[0]
            N.texto_maquina(h, titulo, P[0], P[1], px * s * k, t, -99, cps=1e9, tono=0.03, centro=True, fuente=IMPACT, track=4.0,
                            encuadrar=False)


def billetes(h, x, y, n=5, s=1.0, sem=0):
    """Pila de fajos de billetes con su faja (y = base)."""
    for k in range(n):
        yy = y - (k + 1) * 34 * s
        dx = 8 * math.sin(k * 2.1 + sem) * s
        h.pieza(rect(x - 130 * s + dx, yy, 260 * s, 32 * s), 150 + 12 * (k % 2), sem + k, w=3.5 * s, luz=(0.2, -1), d=5 * s, trama=0.2,
                rim=0.5)
        h.pieza(rect(x - 26 * s + dx, yy, 52 * s, 32 * s), 222, sem + 40 + k, w=2.5 * s, luz=(0, -1), d=2, trama=0, sombra=0.2)
        for q in range(4):
            h.trazo(np.array([[x - 122 * s + dx, yy + (6 + q * 7) * s], [x - 34 * s + dx, yy + (6 + q * 7) * s]]), 1.2 * s,
                    sem + 80 + k * 4 + q, alfa=0.35, jit=0.2)


def casa(h, x, y, s=1.0, frac=0.0, sem=0, luz_v=1.0):
    """Casa familiar de frente (y = suelo). frac 0..1: la parte que «se pierde» se oscurece de abajo arriba."""
    def T(P):
        return np.asarray(P, float) * s + (x, y)
    h.pieza(T([(-230, 0), (-230, -260), (230, -260), (230, 0)]), 150, sem, w=6 * s, luz=(0.3, -1), d=16 * s, trama=0.5, rim=0.6)
    h.pieza(T([(-280, -250), (0, -460), (280, -250)]), 70, sem + 1, w=6 * s, luz=(0.3, -1), d=16 * s, trama=0.6, rim=0.7)
    h.pieza(T(rect(120, -440, 50, 130)), 90, sem + 2, w=4 * s, luz=(0.3, -1), d=8 * s, trama=0.4, rim=0.5)   # chimenea
    h.pieza(T(rect(-40, -150, 80, 150)), 60, sem + 3, w=4 * s, luz=(0.3, -1), d=6 * s, trama=0.3, rim=0.5)   # puerta
    for q in (-1, 1):
        v = T(rect(q * 140 - 45, -200, 90, 90))
        h.pieza(v, 200, sem + 4 + q, w=4 * s, luz=(0, -1), d=4, trama=0, sombra=0.2)
        if luz_v > 0:
            h.emitir(v, 0.5 * luz_v)
        h.trazo(T([(q * 140, -200), (q * 140, -110)]), 3 * s, sem + 7 + q)
        h.trazo(T([(q * 140 - 45, -155), (q * 140 + 45, -155)]), 3 * s, sem + 10 + q)
    if frac > 0:
        alto = 470 * frac
        plano_(h, T(rect(-300, -alto, 600, alto)), 8, sem + 20, alfa=0.86)
        h.trazo(T([(-300, -alto), (300, -alto)]), 5 * s, sem + 21, color=(240, 240, 240), jit=0.4, taper=(0, 0))


def balanza(h, cx, cy, incl=0.0, s=1.0, sem=0):
    """Balanza de dos platillos. incl > 0 baja el platillo derecho. Devuelve (centro platillo izq, centro platillo der)."""
    h.pieza(np.array([[cx - 90 * s, cy + 420 * s], [cx + 90 * s, cy + 420 * s], [cx + 40 * s, cy + 380 * s], [cx - 40 * s, cy + 380 * s]]),
            40, sem, w=5 * s, luz=(0.2, -1), d=8 * s, trama=0.4, rim=0.8)
    h.pieza(rect(cx - 9 * s, cy - 20 * s, 18 * s, 400 * s), 46, sem + 1, w=4 * s, luz=(0.3, -1), d=5 * s, trama=0.3, rim=0.9)
    a = 0.30 * incl
    L = 430 * s
    pl = np.array([cx - L * math.cos(a), cy + L * math.sin(-a)])
    pr = np.array([cx + L * math.cos(a), cy + L * math.sin(a)])
    h.trazo(np.array([pl, [cx, cy - 6 * s], pr]), 12 * s, sem + 2, color=gris(60), jit=0.3, taper=(0.1, 0.1))
    h.pieza(elipse_(cx, cy - 6 * s, 22 * s, 22 * s, n=20), 70, sem + 3, w=4 * s, luz=(0.3, -1), d=5 * s, trama=0.2, rim=0.9)
    out = []
    for k, p in enumerate((pl, pr)):
        py = p[1] + 250 * s
        for q in (-1, 1):
            h.trazo(np.array([p, [p[0] + q * 130 * s, py]]), 2.5 * s, sem + 10 + k * 3 + q, color=gris(150), jit=0.3, taper=(0, 0))
        h.pieza(suave([(p[0] - 150 * s, py), (p[0] + 150 * s, py), (p[0] + 100 * s, py + 46 * s), (p[0] - 100 * s, py + 46 * s)], 4), 60,
                sem + 20 + k, w=5 * s, luz=(0.3, -1), d=8 * s, trama=0.4, rim=0.9)
        out.append(np.array([p[0], py]))
    return out


def pluma(h, x, y, ang=-0.9, s=1.0, sem=0):
    """Pluma estilográfica; (x, y) = punta."""
    c = np.array([x, y], float)

    def T(P):
        return rot(np.asarray(P, float) * s + c, ang, c)
    h.pieza(T([(0, 0), (34, -9), (44, 0), (34, 9)]), 200, sem, w=2.5 * s, luz=(0.2, -1), d=3, trama=0, rim=0.6)
    h.pieza(T(suave([(42, -13), (300, -17), (330, 0), (300, 17), (42, 13)], 4)), 26, sem + 1, w=4 * s, luz=(0.2, -1), d=7 * s,
            trama=0.3, rim=0.95, rim_tono=220)
    plano_(h, T(rect(150, -17, 14, 34)), 190, sem + 2)


def garabato(h, x, y, u, s=1.0, sem=0, ancho=260, color=(14, 14, 14), w=5.0):
    """Firma que se va escribiendo (u 0..1)."""
    if u <= 0:
        return np.array([x, y])
    r = np.random.default_rng(sem)
    n = 60
    xs = np.linspace(0, ancho * s, n)
    f1, f2, p1 = r.uniform(5, 8), r.uniform(11, 15), r.uniform(0, 6)
    ys = (26 * np.sin(xs / (ancho * s) * f1 * math.pi + p1) + 12 * np.sin(xs / (ancho * s) * f2 * math.pi)) * s * np.linspace(1, 0.4, n)
    m = max(2, int(n * clamp01(u)))
    P = np.stack([x + xs[:m], y + ys[:m] - xs[:m] * 0.08], 1)
    h.trazo(P, w * s, sem, color=color, jit=0.4, taper=(0.3, 0.6))
    return P[-1]


def chip(h, cx, cy, s=1.0, sem=0, brillo=0.0):
    h.pieza(rect(cx - 110 * s, cy - 110 * s, 220 * s, 220 * s), 36, sem, w=5 * s, luz=(0.3, -1), d=10 * s, trama=0.4, rim=0.9)
    h.pieza(rect(cx - 62 * s, cy - 62 * s, 124 * s, 124 * s), 90, sem + 1, w=3 * s, luz=(0.3, -1), d=5 * s, trama=0.2, rim=0.8)
    for k in range(7):
        o = (-90 + k * 30) * s
        for (a, b) in (((cx + o, cy - 110 * s), (cx + o, cy - 150 * s)), ((cx + o, cy + 110 * s), (cx + o, cy + 150 * s)),
                       ((cx - 110 * s, cy + o), (cx - 150 * s, cy + o)), ((cx + 110 * s, cy + o), (cx + 150 * s, cy + o))):
            h.trazo(np.array([a, b]), 7 * s, sem + 5 + k, color=gris(170), jit=0.2, taper=(0, 0))
    if brillo > 0:
        h.emitir(rect(cx - 40 * s, cy - 40 * s, 80 * s, 80 * s), 0.7 * brillo, blur=4)


def interruptor(h, cx, cy, s=1.0, pos=0.0, sem=0, rot_txt=True, t=0.0):
    """Interruptor de palanca industrial. pos 0 = arriba (ENCENDIDO) .. 1 = abajo (APAGADO). Devuelve la punta de la palanca."""
    h.pieza(rect(cx - 150 * s, cy - 260 * s, 300 * s, 520 * s), 60, sem, w=7 * s, luz=(0.3, -1), d=16 * s, trama=0.5, rim=0.8)
    for q in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        h.pieza(elipse_(cx + q[0] * 118 * s, cy + q[1] * 228 * s, 12 * s, 12 * s, n=10), 130, sem + 1 + q[0] + 2 * q[1], w=2.5 * s,
                luz=(0.3, -1), d=3, trama=0, rim=0.8)
    plano_(h, rect(cx - 26 * s, cy - 150 * s, 52 * s, 300 * s), 8, sem + 6)
    a = -1.0 + 2.0 * pos
    tip = np.array([cx, cy + 150 * s * a])
    h.pieza(tubo(np.array([[cx, cy], [cx, (cy + tip[1]) / 2], tip]), 34 * s, 26 * s), 150, sem + 7, w=5 * s, luz=(0.3, -1), d=8 * s,
            trama=0.2, rim=0.9)
    h.pieza(elipse_(tip[0], tip[1], 44 * s, 44 * s, n=24), 30, sem + 8, w=5 * s, luz=(0.3, -1), d=10 * s, trama=0.3, rim=0.95)
    if rot_txt:
        N.texto_maquina(h, "ON", cx, cy - 215 * s, 36 * s, t, -99, cps=1e9, tono=0.95 if pos < 0.5 else 0.4, centro=True, fuente=IMPACT,
                        encuadrar=False)
        N.texto_maquina(h, "OFF", cx, cy + 205 * s, 36 * s, t, -99, cps=1e9, tono=0.95 if pos >= 0.5 else 0.4, centro=True, fuente=IMPACT,
                        encuadrar=False)
    return tip


def reloj_arena(h, cx, cy, s=1.0, u=0.0, t=0.0, sem=0):
    """Reloj de arena: u 0..1 = fracción ya caída."""
    for q in (-1, 1):
        h.pieza(rect(cx - 170 * s, cy + q * 330 * s - 20 * s, 340 * s, 40 * s), 50, sem + q, w=5 * s, luz=(0.3, -1), d=8 * s, trama=0.4,
                rim=0.9)
        h.trazo(np.array([[cx + q * 150 * s, cy - 310 * s], [cx + q * 150 * s, cy + 310 * s]]), 9 * s, sem + 3 + q, color=gris(60), jit=0.2,
                taper=(0, 0))
    cristal = suave([(-120, -310), (120, -310), (110, -150), (16, 0), (110, 150), (120, 310), (-120, 310), (-110, 150), (-16, 0),
                     (-110, -150)], 5)
    h.pieza(np.asarray(cristal) * s + (cx, cy), 120, sem + 6, w=5 * s, luz=(0.4, -1), d=10 * s, trama=0.1, rim=0.9, alfa=0.55)
    a = 150 * (1 - u)                                           # arena de arriba
    if a > 4:
        wa = 16 + 94 * (a / 150)
        h.pieza(np.array([(-wa, -a), (wa, -a), (10, -4), (-10, -4)]) * s + (cx, cy), 226, sem + 7, w=3 * s, luz=(0.3, -1), d=4, trama=0)
    b = 150 * u
    if b > 4:
        wb = 110 - 60 * (1 - b / 150)
        h.pieza(np.array(suave([(-108, 300), (108, 300), (wb * 0.5, 300 - b), (-wb * 0.5, 300 - b)], 3)) * s + (cx, cy), 226, sem + 8,
                w=3 * s, luz=(0.3, -1), d=4, trama=0)
    if 0 < u < 1:
        h.trazo(np.array([[cx, cy], [cx + 2 * math.sin(t * 20) * s, cy + 290 * s]]), 4 * s, sem + 9, color=(230, 230, 230), jit=0.6,
                taper=(0, 0))


def puerta(h, x, y, w=380, hh=720, sem=0, rendija=0.0, tono=30, vidrio="", t=0.0, abre=0.0):
    """Puerta cerrada (x, y = esquina sup-izq). rendija 0..1 = luz que sale por debajo. vidrio = rótulo en el cristal esmerilado."""
    h.pieza(rect(x - 22, y - 22, w + 44, hh + 22), tono - 12, sem, w=6, luz=(0, -1), d=10, trama=0.5, rim=0.4)
    an = w * (1 - 0.8 * abre)
    if abre > 0:
        plano_(h, rect(x, y, w, hh), 236, sem + 1)
        h.emitir(rect(x, y, w, hh), 0.9 * abre)
        h.luz_radial(x + w / 2, y + hh / 2, 900, (1.0, 1.0, 1.0), k=1.2 * abre)
    h.pieza(rect(x, y, an, hh), tono, sem + 2, w=6, luz=(0, -1), d=12, trama=0.5, rim=0.5)
    if abre < 0.3:
        v = rect(x + 40, y + 50, w - 80, hh * 0.36)
        h.pieza(v, 96, sem + 3, w=4, luz=(0, -1), d=6, trama=0.3)
        if vidrio:
            N.texto_maquina(h, vidrio, x + w / 2, y + 50 + hh * 0.18, 34, t, -99, cps=1e9, tono=0.05, centro=True, fuente=N.FUENTE_SELLO,
                            encuadrar=False)
        h.pieza(elipse_(x + w - 46, y + hh * 0.56, 16, 16, n=14), 160, sem + 4, w=3, luz=(0.3, -1), d=4, trama=0, rim=0.9)
    if rendija > 0:
        r = rect(x + 6, y + hh - 4, w - 12, 12)
        h.emitir(r, 1.3 * rendija, blur=3)
        h.luz_cono(x + w / 2, y + hh - 10, math.pi / 2, 1.2, 420, (1.4, 1.4, 1.4), k=0.9 * rendija, suave=0.7)


def flecha(h, a, b, w=10.0, sem=0, color=(236, 236, 236), u=1.0, punta=34.0, curva=0.0):
    """Flecha de a hacia b (se dibuja hasta la fracción u). curva = panza lateral en px."""
    if u <= 0:
        return
    a, b = np.asarray(a, float), np.asarray(b, float)
    d = b - a
    n_ = np.array([-d[1], d[0]]) / (np.hypot(*d) + 1e-9)
    ts = np.linspace(0, clamp01(u), 24)
    P = a[None] + d[None] * ts[:, None] + n_[None] * (curva * np.sin(ts * math.pi))[:, None]
    h.trazo(P, w, sem, color=color, jit=0.4, taper=(0.2, 0.0))
    if len(P) > 2:
        v = P[-1] - P[-3]
        v /= (np.hypot(*v) + 1e-9)
        q = np.array([-v[1], v[0]])
        tip = P[-1] + v * punta * 0.6
        h.pieza(np.array([tip, P[-1] - v * punta * 0.5 + q * punta * 0.55, P[-1] - v * punta * 0.5 - q * punta * 0.55]),
                color[0], sem + 1, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False, jit=0.5)


def barra(h, x, y, w, hh, frac, sem=0, tono_f=20, tono_r=230, vertical=False):
    """Barra de progreso con marco (frac 0..1)."""
    h.pieza(rect(x - 6, y - 6, w + 12, hh + 12), 14, sem, w=4, luz=(0, -1), d=3, trama=0, sombra=0, rim=0.4)
    plano_(h, rect(x, y, w, hh), tono_f, sem + 1)
    f = clamp01(frac)
    if f > 0:
        P = rect(x, y + hh * (1 - f), w, hh * f) if vertical else rect(x, y, w * f, hh)
        plano_(h, P, tono_r, sem + 2)
        h.luz_fija(P, 0.92)


def mano_alzada(h, x, y, s=1.0, sube=1.0, sem=0, d=1, manga=60, bal=0.0):
    """Brazo que se levanta desde el borde inferior (x = eje del brazo, y = altura de la mano ya alzada)."""
    yy = y + 700 * s * (1 - e_out(clamp01(sube)))
    x = x + bal
    h.pieza(tubo(np.array([[x - 30 * d * s, yy + 760 * s], [x - 10 * d * s, yy + 380 * s], [x, yy + 110 * s]]), 150 * s, 104 * s), manga,
            sem, w=7 * s, luz=(0.2, -1), d=22 * s, trama=0.6, rim=0.8)
    h.pieza(rect(x - 60 * s, yy + 96 * s, 120 * s, 30 * s), 215, sem + 1, w=4 * s, luz=(0.2, -1), d=5 * s, trama=0.1, rim=0.5)   # puño
    h.pieza(suave([(x - 56 * s, yy + 100 * s), (x - 62 * s, yy + 10 * s), (x - 30 * s, yy - 30 * s), (x + 36 * s, yy - 30 * s),
                   (x + 58 * s, yy + 14 * s), (x + 52 * s, yy + 100 * s)], 4), 122, sem + 2, w=6 * s, luz=(0.2, -1), d=16 * s, trama=0.4,
            rim=0.85)
    for k in range(4):
        fx = x + (-44 + k * 29) * s
        L = (96 + 14 * math.sin(k * 1.3 + 1)) * s
        h.pieza(tubo(np.array([[fx, yy - 16 * s], [fx - 2 * s, yy - 16 * s - L * 0.6], [fx - 3 * s, yy - 16 * s - L]]), 26 * s, 22 * s), 126,
                sem + 3 + k, w=5 * s, luz=(0.2, -1), d=6 * s, trama=0.2, rim=0.8)
    h.pieza(tubo(np.array([[x + d * 50 * s, yy + 60 * s], [x + d * 86 * s, yy + 20 * s], [x + d * 100 * s, yy - 20 * s]]), 30 * s, 24 * s),
            124, sem + 8, w=5 * s, luz=(0.2, -1), d=6 * s, trama=0.2, rim=0.8)


def persona(h, x, y, s=1.0, sem=0, tono=24, bal=0.0, brazo=0.0, sombrero=False, rim=0.5, luz=(0.2, -1)):
    """Silueta barata de cuerpo entero (multitudes): cabeza, hombros, abrigo. y = pies. brazo 0..1 levanta el puño."""
    def T(P):
        return np.asarray(P, float) * s + (x + bal, y)
    h.pieza(T(suave([(-52, -330), (-22, -356), (22, -356), (52, -330), (60, -150), (48, 0), (-48, 0), (-60, -150)], 4)), tono, sem,
            w=4 * s, luz=luz, d=10 * s, trama=0.3, rim=rim)
    h.pieza(T(elipse_(0, -394, 32, 38, n=18)), tono + 14, sem + 1, w=3.5 * s, luz=luz, d=7 * s, trama=0.2, rim=rim)
    if sombrero:
        h.pieza(T([(-50, -412), (50, -412), (30, -420), (26, -452), (-26, -452), (-30, -420)]), tono - 8, sem + 2, w=3 * s, luz=luz,
                d=5 * s, trama=0.2, rim=rim)
    if brazo > 0:
        h.pieza(T(tubo(np.array([[40, -320], [70, -380 - 40 * brazo], [62, -440 - 90 * brazo]]), 30, 24)), tono + 4, sem + 3, w=3.5 * s,
                luz=luz, d=6 * s, trama=0.2, rim=rim)


def multitud(h, t, x0, x1, y, n=24, s=1.0, sem=0, carteles=(), tono=22, ritmo=1.0, filas=2, px=30):
    """Multitud de siluetas con ritmo propio (cada una se balancea y sube el puño a su tiempo) y pancartas con texto."""
    r = np.random.default_rng(sem)
    orden = []
    for f in range(filas):
        for k in range(n // filas):
            xx = x0 + (x1 - x0) * (k + r.uniform(0.1, 0.9)) / (n // filas)
            orden.append((f, xx, r.uniform(0.86, 1.1), r.uniform(0, 6.28), r.uniform(0.8, 1.5), r.uniform() < 0.3, k))
    orden.sort(key=lambda o: o[0])
    ci = 0
    for i, (f, xx, ss, ph, vel, somb, k) in enumerate(orden):
        yy = y - (filas - 1 - f) * 46 * s
        sc = s * ss * (0.86 + 0.14 * f / max(1, filas - 1))
        bal = 7 * math.sin(t * vel * ritmo * 2.2 + ph) * sc
        bz = max(0.0, math.sin(t * vel * ritmo * 1.6 + ph * 2)) if (i % 3 == 0) else 0.0
        persona(h, xx, yy + 3 * abs(math.sin(t * vel * ritmo * 2.2 + ph)) * sc, sc, sem + 10 + i * 5, tono=tono + 8 * f, bal=bal, brazo=bz,
                sombrero=somb)
        if carteles and i % max(2, (len(orden) // max(1, len(carteles)))) == 1 and ci < len(carteles):
            cx = xx + bal * 2 + 40 * sc
            cy = yy - 560 * sc + 10 * math.sin(t * vel * 2 + ph)
            h.trazo(np.array([[cx, yy - 300 * sc], [cx, cy + 50 * sc]]), 7 * sc, sem + 500 + i, color=gris(40), jit=0.2, taper=(0, 0))
            aw = (len(carteles[ci]) * px * 0.56 + 40) * sc
            c = np.array([cx, cy])
            a = 0.06 * math.sin(t * vel * 2 + ph)
            h.pieza(rot(rect(cx - aw / 2, cy - 44 * sc, aw, 88 * sc), a, c), 226, sem + 600 + i, w=3.5, luz=(0, -1), d=4, trama=0, rim=0)
            N.texto_maquina(h, carteles[ci], cx, cy, px * sc, t, -99, cps=1e9, tono=0.04, centro=True, fuente=IMPACT, encuadrar=False)
            ci += 1


def robot(h, x, y, s=1.0, t=0.0, sem=0, visor=1.0, brazo=0.0, tono=150, luz=(0.2, -1)):
    """Humanoide de fábrica de frente (y = pies): casco con visor que emite, torso con placa, brazos y piernas articulados."""
    def T(P):
        return np.asarray(P, float) * s + (x, y)
    for q in (-1, 1):                                             # piernas
        h.pieza(T(tubo(np.array([[q * 34, -210], [q * 38, -110], [q * 36, -10]]), 40, 32)), tono - 40, sem + 1 + q, w=4 * s, luz=luz,
                d=8 * s, trama=0.4, rim=0.8)
        h.pieza(T(rect(q * 36 - 30, -14, 60, 16)), tono - 70, sem + 4 + q, w=3 * s, luz=luz, d=3, trama=0, rim=0.6)
        h.pieza(T(elipse_(q * 37, -112, 17, 17, n=12)), tono - 80, sem + 7 + q, w=3 * s, luz=luz, d=3, trama=0, rim=0.8)
    h.pieza(T(suave([(-78, -400), (78, -400), (64, -214), (-64, -214)], 3)), tono, sem + 10, w=5 * s, luz=luz, d=14 * s, trama=0.5, rim=0.9)
    h.pieza(T(rect(-36, -370, 72, 60)), tono - 70, sem + 11, w=3 * s, luz=luz, d=4, trama=0.2, rim=0.5)
    for q in (-1, 1):                                             # brazos
        sube = brazo if q == 1 else 0.0
        hom = np.array([q * 92, -384])
        codo = hom + (q * 16, 96 - 150 * sube)
        mano_ = codo + (q * (6 + 40 * sube), 96 - 180 * sube)
        h.pieza(T(tubo(np.array([hom, codo, mano_]), 34, 26)), tono - 30, sem + 14 + q, w=4 * s, luz=luz, d=7 * s, trama=0.4, rim=0.8)
        h.pieza(T(elipse_(hom[0], hom[1], 24, 24, n=14)), tono - 60, sem + 17 + q, w=3.5 * s, luz=luz, d=5 * s, trama=0.2, rim=0.9)
        h.pieza(T(elipse_(mano_[0], mano_[1], 18, 20, n=12)), tono - 70, sem + 20 + q, w=3 * s, luz=luz, d=4, trama=0, rim=0.8)
    h.pieza(T(rect(-14, -424, 28, 30)), tono - 80, sem + 23, w=3 * s, luz=luz, d=3, trama=0)
    h.pieza(T(suave([(-54, -426), (-58, -500), (-30, -540), (30, -540), (58, -500), (54, -426)], 4)), tono + 20, sem + 24, w=5 * s,
            luz=luz, d=12 * s, trama=0.4, rim=0.9)
    vis = T(rect(-40, -500, 80, 26))
    plano_(h, vis, 10, sem + 25)
    if visor > 0:
        e = T(rect(-34 + 20 * math.sin(t * 1.7 + sem), -496, 28, 18))
        h.emitir(e, 1.1 * visor, blur=2)


def pantalla_codigo(h, caja, t, sem=0, vel=3.0, tono=220, filas=14, enc=1.0):
    """Renglones de código (sangrías distintas) que suben dentro de caja=(x, y, w, hh) y emiten."""
    x, y, w, hh = caja
    plano_(h, rect(x, y, w, hh), 12, sem)
    paso = hh / filas
    off = (t * vel) % 1.0
    k0 = int(t * vel)
    for j in range(filas + 1):
        r = np.random.default_rng(sem * 977 + k0 + j)
        yy = y + (j - off) * paso + paso * 0.3
        if yy < y + 4 or yy > y + hh - paso * 0.5:
            continue
        xi = x + w * (0.04 + 0.06 * int(r.integers(0, 4)))
        for q in range(int(r.integers(1, 4))):
            L = w * r.uniform(0.08, 0.3)
            if xi + L > x + w * 0.96:
                break
            P = rect(xi, yy, L, paso * 0.36)
            plano_(h, P, tono * r.uniform(0.5, 1.0), sem + 3 + j * 4 + q)
            xi += L + w * 0.03
    h.emitir(rect(x, y, w, hh), 0.22 * enc, blur=6)


def cajas(h, t, t0, cols, filas, x0, y0, dx, dy, s=0.2, sem=0, ola=0.02, led=1.0):
    """Rejilla de copias de la IA (monolitos con una luz): se encienden en oleada desde t0 (ola = s entre vecinos)."""
    n_on = 0
    for j in range(filas):
        for i in range(cols):
            tk = t0 + (i + j * 1.7) * ola
            if t < tk:
                continue
            n_on += 1
            a = clamp01((t - tk) / 0.25)
            x, y = x0 + i * dx, y0 + j * dy
            w_, a_ = 230 * s, 520 * s
            h.pieza(rect(x - w_ / 2, y - a_, w_, a_), 22, sem + (i * 31 + j * 7) % 900, w=2.5, luz=(0.3, -1), d=6 * s * 4, trama=0.3,
                    rim=0.9, rim_tono=190, alfa=a, jit=0.6)
            v = led * a * (0.5 + 0.5 * math.sin(t * 3.1 + i * 1.3 + j * 2.1) ** 2)
            h.emitir(elipse_(x + w_ / 2 - 36 * s, y - a_ + 34 * s, max(2.0, 9 * s), max(2.0, 9 * s), n=8), 1.3 * v, blur=1.5)
    return n_on


def taza_arriba(h, x, y, s=1.0, sem=0, t=None):
    """Taza de café vista desde arriba (para los escritorios cenitales), con su vapor."""
    h.pieza(elipse_(x, y, 104 * s, 104 * s, n=40), 205, sem, w=4 * s, luz=(0.3, -1), d=8 * s, trama=0.2, rim=0.5)
    h.pieza(tubo(np.array([[x + 60 * s, y - 10 * s], [x + 108 * s, y - 30 * s], [x + 122 * s, y]]), 22 * s, 18 * s), 225, sem + 1,
            w=4 * s, luz=(0.3, -1), d=4 * s, trama=0, rim=0.6)
    h.pieza(elipse_(x, y, 68 * s, 68 * s, n=36), 232, sem + 2, w=4 * s, luz=(0.3, -1), d=8 * s, trama=0.2, rim=0.6)
    h.pieza(elipse_(x, y, 54 * s, 54 * s, n=32), 22, sem + 3, w=3 * s, luz=(0.3, -1), d=5 * s, sombra=0.3, trama=0, rim=0.5, rim_tono=120)
    if t is not None:
        N.humo(h, t, x, y, k=0.7, ancho=1.3, viento=(10, -46), vida=2.4, hebras=2, sem=sem)


ZANCADA = 72.0                                    # del caminante, px locales (medio paso)


def fase_paso(dist, s=1.0):
    """Fase del caminante que ha recorrido dist px del mundo a escala s: así el pie apoyado no patina."""
    return dist / avance_paso(ZANCADA, s)


def caminante(h, x, y, s=1.0, fase=0.0, sem=0, tono=34, d=1, luz=(0.5, -1.0), rim=0.85, carga=False, barba=True, piel=124,
              pelo=24, andar=1.0):
    """Daniel de cuerpo entero, de perfil, CAMINANDO (ciclo de piernas con rodilla, braceo contrario, cabeceo): y = suelo,
    ~580 px de alto a s = 1. carga=True lleva los dos brazos al frente (sujeta una caja). Devuelve la posición de las manos.
    fase = fase_paso(distancia recorrida, s) para que los pies no patinen (no `t * algo` suelto)."""
    def T(P):
        P = np.asarray(P, float)
        return np.stack([x + d * s * P[..., 0], y + s * P[..., 1]], -1)
    kw = dict(luz=(luz[0] * d, luz[1]), rim=rim)
    alt_cad = cadera_paso(fase, 250.0, ZANCADA * andar)             # la pierna apoyada va estirada: el cuerpo sube y baja con ella
    bob = 250.0 - alt_cad

    def brazo(k, sm):
        a = 0.55 * math.sin(fase + math.pi * (1 - k)) * andar
        hom = np.array([2.0, -452 + bob])
        if carga:
            codo, man = hom + (34, 92), hom + (104, 120)
        else:
            codo = hom + 100 * np.array([math.sin(a), math.cos(a)])
            man = codo + 92 * np.array([math.sin(a + 0.4), math.cos(a + 0.4)])
        h.pieza(T(tubo(np.array([hom, codo, man]), 40, 30)), tono - 8 + 10 * k, sem + sm, w=5 * s, d=10 * s, trama=0.4, **kw)
        h.pieza(T(elipse_(man[0], man[1], 15, 17, n=12)), piel, sem + sm + 1, w=3.5 * s, d=5 * s, trama=0.1, **kw)
        return T(man)
    brazo(0, 20)
    for k in (0, 1):
        ph = fase + math.pi * k
        cad = np.array([0.0, -alt_cad])
        rod, pie = pierna_paso(ph, cad, 126, 126, ZANCADA * andar, 30 * andar * andar)     # dobla la rodilla al llevar el pie adelante
        h.pieza(T(tubo(np.array([cad, rod, pie]), 48, 32)), tono - 12 + 8 * k, sem + k, w=5 * s, d=10 * s, trama=0.5, **kw)
        h.pieza(T(suave([(pie[0] - 16, pie[1] - 12), (pie[0] + 30, pie[1] - 8), (pie[0] + 42, pie[1] + 6), (pie[0] - 16, pie[1] + 8)], 3)),
                12, sem + 4 + k, w=3.5 * s, d=4 * s, trama=0, **kw)
    tor = suave([(-42, -468 + bob), (-8, -486 + bob), (28, -478 + bob), (46, -436 + bob), (46, -330 + bob), (38, -236 + bob),
                 (-38, -236 + bob), (-48, -330 + bob)], 4)
    h.pieza(T(tor), tono, sem + 8, w=6 * s, d=16 * s, trama=0.6, **kw)
    h.pieza(T([(22, -478 + bob), (40, -474 + bob), (36, -400 + bob), (26, -420 + bob)]), 205, sem + 9, w=3 * s, d=4 * s, trama=0, **kw)
    h.pieza(T(rect(-8, -500 + bob, 30, 30)), piel - 14, sem + 10, w=3 * s, d=4 * s, trama=0.2, **kw)                  # cuello
    cab = suave([(-30, -540), (-26, -580), (0, -596), (30, -586), (40, -560), (42, -548), (52, -536), (42, -528), (42, -514),
                 (30, -500), (4, -496), (-20, -508)], 4)
    h.pieza(T(np.asarray(cab) + (0, bob)), piel, sem + 11, w=5 * s, d=14 * s, trama=0.35, **kw)
    if barba:
        h.pieza(T(np.asarray(suave([(8, -530), (42, -524), (42, -512), (30, -496), (4, -494), (-8, -510)], 3)) + (0, bob)), pelo + 14,
                sem + 12, w=3.5 * s, d=5 * s, trama=0.3, **kw)
    h.pieza(T(np.asarray(suave([(-32, -540), (-30, -584), (0, -602), (32, -592), (40, -572), (24, -578), (-4, -574), (-16, -548)], 4))
              + (0, bob)), pelo, sem + 13, w=4.5 * s, d=8 * s, trama=0.4, **kw)
    ojo = T(np.array([[30.0, -552 + bob]]))[0]
    h.trazo(T(np.array([[20.0, -560 + bob], [38, -562 + bob]])), 3.2 * s, sem + 14, alfa=0.9)
    h.pieza(elipse_(ojo[0], ojo[1], 3.2 * s, 3.2 * s, n=8), 16, sem + 15, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False)
    return brazo(1, 16)


def medidor(h, cx, cy, r, v, t=0.0, sem=0, rojo=0.6):
    """Indicador de aguja de 0 a 100 % (semicírculo). v 0..1; la zona desde `rojo` va rayada (peligro)."""
    h.pieza(elipse_(cx, cy, r * 1.08, r * 1.08, n=64), 30, sem, w=8, luz=(0.3, -1), d=r * 0.06, trama=0.4, rim=0.95, rim_tono=220)
    h.pieza(elipse_(cx, cy, r, r, n=64), 214, sem + 1, w=4, luz=(0.3, -1), d=r * 0.04, trama=0.1, rim=0.0, sombra=0.3)
    ang = lambda f: math.pi * (1.0 + f)                              # 0 % a la izquierda, 100 % a la derecha
    for k in range(51):
        f = k / 50
        a = ang(f)
        r0 = r * (0.80 if k % 5 == 0 else 0.88)
        h.trazo(np.array([[cx + r0 * math.cos(a), cy + r0 * math.sin(a)], [cx + r * 0.95 * math.cos(a), cy + r * 0.95 * math.sin(a)]]),
                (7 if k % 5 == 0 else 3) * (2.2 if f >= rojo else 1.0), sem + 2 + k, jit=0.2, taper=(0, 0))
    for k in range(0, 101, 20):
        a = ang(k / 100)
        N.texto_maquina(h, str(k), cx + r * 0.64 * math.cos(a), cy + r * 0.64 * math.sin(a), r * 0.13, t, -99, cps=1e9, tono=0.05, centro=True,
                        fuente=IMPACT, encuadrar=False)
    N.texto_maquina(h, "%", cx, cy + r * 0.42, r * 0.2, t, -99, cps=1e9, tono=0.08, centro=True, fuente=IMPACT, encuadrar=False)
    a = ang(clamp01(v)) + (0.02 * math.sin(t * 31) if v > rojo else 0.0)
    tip = np.array([cx + r * 0.84 * math.cos(a), cy + r * 0.84 * math.sin(a)])
    n_ = np.array([-math.sin(a), math.cos(a)]) * r * 0.035
    h.pieza(np.array([tip, [cx + n_[0], cy + n_[1]], [cx - n_[0], cy - n_[1]]]), 14, sem + 60, w=3, luz=(0.3, -1), d=3, trama=0, rim=0)
    h.pieza(elipse_(cx, cy, r * 0.08, r * 0.08, n=20), 40, sem + 61, w=4, luz=(0.3, -1), d=4, trama=0, rim=0.9)
