# -*- coding: utf-8 -*-
"""Kit de vector plano (estilo Kurzgesagt) sobre el Lienzo: esferas con sombra de terminador y borde de luz,
halos, Sol, planeta Tierra con continentes que giran, pajarito, microbios, árbol, termómetro, fumarola y
rótulos limpios. Pensado para ESTILO_VISUAL = "kurzgesagt" (sin contornos, sin temblor), pero funciona en
cualquier estilo. Coordenadas en px de 1080p (o locales dentro de lz.grupo).

Reglas de la estética: nada de negro puro (las sombras son azul-violeta), pocas formas grandes con 2 tonos
de sombra + un borde de luz, brillo solo en lo luminoso, texto blanco sin contorno (geo = Poppins)."""
import math

import cv2
import numpy as np

from motor import SS, BLANCO, W as W_, H as H_, catmull, circulo, clamp01, elipse, lerp, rect_red, rellenar_suave

SOMBRA = (22, 18, 64)          # color de sombra por defecto (nunca negro)
TINTA = (30, 26, 62)           # trazos oscuros intencionales (≠ NEGRO, así no los borra "sin_contorno")


def mezcla(c1, c2, u):
    u = clamp01(u)
    return tuple(int(round(a + (b - a) * u)) for a, b in zip(c1[:3], c2[:3]))


def aclarar(c, u):
    return mezcla(c, (255, 255, 255), u)


def oscurecer(c, u):
    return mezcla(c, SOMBRA, u)


def _rotar(P, ang, x, y):
    c, s = math.cos(ang), math.sin(ang)
    return P @ np.array([[c, s], [-s, c]]) + np.array([x, y])


def terminador(x, y, r, ang, e, n=48):
    """Polígono de la zona en sombra de un disco iluminado desde la dirección `ang` (rad, hacia la luz;
    pantalla: 0 = derecha, pi/2 = abajo). e: -1 = sin sombra, 0 = media esfera, 1 = todo en sombra."""
    th = np.linspace(np.pi / 2, 3 * np.pi / 2, n)
    ph = np.linspace(-np.pi / 2, np.pi / 2, n)
    P = np.concatenate([np.stack([np.cos(th), np.sin(th)], 1), np.stack([e * np.cos(ph), np.sin(ph)], 1)]) * r
    return _rotar(P, ang, x, y)


def borde_luz(x, y, r, ang, grosor=0.08, n=40):
    """Media luna fina del lado iluminado (ancho en el ecuador = 2*grosor*r)."""
    th = np.linspace(-np.pi / 2, np.pi / 2, n)
    ph = np.linspace(np.pi / 2, -np.pi / 2, n)
    e = 1 - 2 * grosor
    P = np.concatenate([np.stack([np.cos(th), np.sin(th)], 1), np.stack([e * np.cos(ph), np.sin(ph)], 1)]) * r
    return _rotar(P, ang, x, y)


def esfera(lz, x, y, r, color, ang_luz=math.pi * 1.25, sombra=-0.15, fuerza=0.5, color_sombra=SOMBRA,
           rim=0.07, color_rim=None, contenido=None, alfa=1.0):
    """Disco con 2 tonos de sombra y borde de luz. contenido(): se dibuja recortado dentro del disco."""
    C = circulo(x, y, r, 120)
    lz.relleno(C, color, alfa=alfa)
    if contenido is not None:
        with lz.recorte(C):
            contenido()
    if fuerza > 0:
        lz.relleno(terminador(x, y, r, ang_luz, sombra), color_sombra, alfa=fuerza * 0.55 * alfa)
        lz.relleno(terminador(x, y, r, ang_luz, min(1.0, sombra + 0.45)), color_sombra, alfa=fuerza * 0.6 * alfa)
    if rim > 0:
        lz.relleno(borde_luz(x, y, r, ang_luz, rim), color_rim or aclarar(color, 0.5), alfa=0.75 * alfa)


# ------------------------------------------------------------------ Sol
def sol(lz, x, y, r, t, brillo=1.0, apagado=0.0):
    """Sol con halo, corona ondulante y núcleo claro. apagado 0..1 lo convierte en un disco oscuro sin brillo."""
    u = clamp01(apagado)
    b = brillo * (1 - u)
    if b > 0.01:
        lz.halo(x, y, r * 4.2, (255, 120, 50), alfa=0.22 * b)
        lz.halo(x, y, r * 2.3, (255, 170, 70), alfa=0.45 * b, r0=0.35)
        lz.halo(x, y, r * 1.45, (255, 215, 120), alfa=0.6 * b, r0=0.6)
    muerto = (46, 38, 74)
    # corona: borde que ondula
    n = 160
    th = np.linspace(0, 2 * np.pi, n, endpoint=False)
    rr = r * (1.045 + 0.018 * np.sin(th * 9 + t * 1.3) + 0.012 * np.sin(th * 14 - t * 2.1))
    lz.relleno(np.stack([x + rr * np.cos(th), y + rr * np.sin(th)], 1), mezcla((255, 150, 55), muerto, u),
               alfa=0.85 * (1 - 0.6 * u))
    lz.relleno(circulo(x, y, r, 140), mezcla((255, 168, 60), muerto, u))
    lz.relleno(circulo(x - r * 0.06, y - r * 0.06, r * 0.84, 120), mezcla((255, 196, 84), mezcla(muerto, (60, 50, 92), .5), u))
    lz.relleno(circulo(x - r * 0.13, y - r * 0.13, r * 0.6, 100), mezcla((255, 226, 130), (62, 52, 96), u))
    # manchas de granulación que derivan despacio
    if u < 0.99:
        for k in range(7):
            a = k * 2.4 + t * 0.05
            d = r * (0.25 + 0.55 * ((k * 0.37) % 1))
            lz.relleno(circulo(x + d * math.cos(a), y + d * math.sin(a), r * (0.05 + 0.03 * (k % 3)), 24),
                       (255, 236, 170), alfa=0.35 * (1 - u))
    if u > 0.01:   # borde tenue para que se vea dónde estaba
        lz.relleno(borde_luz(x, y, r, math.pi * 1.25, 0.05), (96, 84, 140), alfa=0.6 * u)


# ------------------------------------------------------------------ Tierra
_CONT = {   # contornos (lon, lat) muy simplificados
    "namerica": [(-165, 65), (-140, 70), (-95, 72), (-75, 62), (-58, 50), (-78, 32), (-82, 25), (-97, 18),
                 (-105, 22), (-118, 33), (-125, 48), (-140, 60), (-160, 58)],
    "samerica": [(-80, 10), (-60, 9), (-35, -7), (-40, -22), (-58, -38), (-70, -54), (-75, -40), (-72, -18),
                 (-81, -5)],
    "groenlandia": [(-55, 60), (-42, 60), (-20, 70), (-25, 82), (-50, 82), (-62, 76)],
    "africa": [(-17, 21), (-6, 35), (10, 37), (32, 31), (43, 12), (51, 11), (40, -15), (20, -35), (12, -18),
               (9, 4), (-8, 5), (-17, 14)],
    "eurasia": [(-10, 36), (-9, 43), (0, 50), (6, 58), (12, 64), (25, 70), (40, 67), (70, 73), (110, 77),
                (140, 72), (170, 66), (160, 60), (140, 50), (130, 40), (122, 30), (108, 20), (100, 8),
                (80, 9), (72, 20), (58, 25), (48, 30), (36, 36), (26, 38), (18, 40), (10, 44), (0, 40)],
    "australia": [(114, -22), (130, -12), (142, -11), (153, -25), (150, -37), (140, -38), (130, -32), (115, -34)],
}
_CONT_S = {k: catmull(np.array(v, float), 6, cerrado=True) for k, v in _CONT.items()}
_NUBES = [(-150, 30, 1.0), (-100, -10, 0.8), (-40, 45, 1.1), (0, -30, 0.9), (30, 10, 0.7), (80, 40, 1.0),
          (120, -15, 0.9), (170, 20, 0.8), (-120, -45, 0.9), (60, -45, 0.8), (-10, 60, 0.7), (150, 55, 0.7)]
_CIUDADES = [(-74, 41), (-118, 34), (-87, 42), (-99, 19), (-46, -23), (-58, -34), (0, 51), (2, 49), (13, 52),
             (37, 56), (31, 30), (3, 6), (28, -26), (77, 29), (72, 19), (121, 31), (116, 40), (139, 36),
             (127, 37), (151, -34), (103, 1), (106, -6), (-43, -23), (-80, 26), (-122, 47)]


def _proy(lonlat, rot, tilt):
    lam = np.radians(lonlat[..., 0]) + rot
    phi = np.radians(lonlat[..., 1])
    X = np.cos(phi) * np.sin(lam)
    Y = -np.sin(phi)
    Z = np.cos(phi) * np.cos(lam)
    atras = Z < 0
    if np.any(atras):   # lo que queda detrás se pega al borde (el recorte al disco hace el resto)
        L = np.sqrt(X * X + Y * Y) + 1e-9
        X = np.where(atras, X / L, X)
        Y = np.where(atras, Y / L, Y)
    c, s = math.cos(tilt), math.sin(tilt)
    return np.stack([X * c - Y * s, X * s + Y * c], -1), Z


def tierra(lz, x, y, r, t, rot=0.0, ang_luz=math.pi, luz=1.0, hielo=0.0, nubes=1.0, ciudades=0.0, tilt=-0.35,
           atmosfera=1.0):
    """Planeta Tierra. rot: giro (rad); luz 0..1 (0 = sin Sol: todo en noche); hielo 0..1 congela océanos."""
    oce = mezcla((40, 122, 226), (196, 222, 244), hielo * 0.85)
    tierra_c = mezcla((96, 196, 108), (232, 240, 250), hielo)
    tierra_c2 = mezcla((70, 162, 92), (205, 222, 240), hielo)
    atm = atmosfera * (0.2 + 0.8 * luz)
    if atm > 0.01:
        lz.halo(x, y, r * 1.28, (110, 190, 255), alfa=0.55 * atm, r0=0.76)

    def contenido():
        lz.relleno(circulo(x + r * 0.35, y + r * 0.35, r * 0.95, 80), mezcla(oce, (26, 84, 180), 0.6), alfa=0.6)
        for k, P in _CONT_S.items():
            Q, Z = _proy(P, rot, tilt)
            if Z.max() <= 0:
                continue
            lz.relleno(Q * r + [x, y], tierra_c)
            # sombra interior del continente (da volumen)
            lz.relleno(Q * r * 0.95 + [x, y] + np.array([r * 0.015, r * 0.02]), tierra_c2, alfa=0.4)
        # casquetes polares
        for lat in (78, -80):
            anillo = np.stack([np.linspace(-180, 180, 60), np.full(60, lat)], 1)
            Q, Z = _proy(anillo, rot, tilt)
            polo, _ = _proy(np.array([[0.0, 90.0 if lat > 0 else -90.0]]), 0.0, tilt)
            cx, cy = polo[0] * r + [x, y]
            lz.relleno(elipse(cx, cy, r * 0.42, r * 0.13, tilt, 48), (238, 246, 255))
        if nubes > 0.01:
            for i, (lo, la, s) in enumerate(_NUBES):
                p, Z = _proy(np.array([[lo, la]], float), rot * 1.25 + t * 0.03, tilt)
                if Z[0] < 0.08:
                    continue
                cx, cy = p[0] * r + [x, y]
                k = math.sqrt(Z[0])
                for j in range(3):
                    lz.relleno(elipse(cx + (j - 1) * r * 0.1 * k * s, cy + (0.02 if j != 1 else -0.03) * r,
                                      r * 0.12 * s * k, r * 0.06 * s, tilt, 28), (248, 252, 255), alfa=0.85 * nubes)

    ang = ang_luz
    n = int(np.clip(r * lz.escala() / 3, 120, 3000))     # círculo fino aunque la cámara se acerque mucho
    lz.relleno(circulo(x, y, r, n), oce)
    with lz.recorte(circulo(x, y, r, n)):
        contenido()
        # día: 2 tonos de sombra en el lado opuesto al Sol; noche: todo cubierto
        if luz > 0.01:
            lz.relleno(terminador(x, y, r, ang, 0.05, n // 2), SOMBRA, alfa=0.36 * luz)
            lz.relleno(terminador(x, y, r, ang, 0.55, n // 2), SOMBRA, alfa=0.4 * luz)
        if luz < 0.99:
            lz.relleno(circulo(x, y, r * 1.01, n), (12, 14, 46), alfa=0.8 * (1 - luz))
            if ciudades > 0.01:
                pts, Z = _proy(np.array(_CIUDADES, float), rot, tilt)
                vis = Z > 0.15
                if np.any(vis):
                    P = pts[vis] * r + [x, y]
                    lz.puntos(P, r * 0.022, (255, 214, 120))
                    for p in P:
                        lz.halo(p[0], p[1], r * 0.07, (255, 190, 90), alfa=0.5 * ciudades * (1 - luz))
    if luz > 0.01:
        lz.relleno(borde_luz(x, y, r, ang, 0.05, n // 2), (190, 235, 255), alfa=0.7 * luz)


def luna(lz, x, y, r, ang_luz=math.pi, luz=1.0):
    def cr():
        for dx, dy, s in ((-0.3, -0.2, 0.22), (0.25, 0.1, 0.16), (-0.05, 0.4, 0.13), (0.35, -0.35, 0.1)):
            lz.relleno(circulo(x + dx * r, y + dy * r, s * r, 24), (170, 170, 196))
    esfera(lz, x, y, r, mezcla((200, 200, 220), (60, 58, 96), 1 - luz), ang_luz, -0.1, 0.55 * luz + 0.3,
           rim=0.08 * luz, contenido=cr)


# ------------------------------------------------------------------ seres
def pajaro(lz, x, y, s=1.0, t=0.0, color=(126, 88, 214), mirar=(0.0, 0.0), aleteo=0.0, tiritar=0.0,
           feliz=0.0, escarcha=0.0, voltear=False, boca=0.0):
    """Pajarito redondo tipo Kurzgesagt (origen en las patas). mirar (-1..1), aleteo 0..1, tiritar 0..1."""
    sx = -1 if voltear else 1
    dx = math.sin(t * 55) * 3.2 * tiritar
    col = mezcla(color, (205, 225, 250), escarcha * 0.55)
    oscuro = oscurecer(col, 0.35)
    panza = aclarar(col, 0.45)
    with lz.grupo(x + dx, y, s):
        # patas
        for px_ in (-12, 12):
            lz.relleno(rect_red(px_ * sx - 3, -16, 6, 18, 3), (255, 150, 60))
        # cola
        lz.relleno(np.array([[-52 * sx, -58], [-86 * sx, -80], [-78 * sx, -44]]), oscuro)
        # cuerpo
        lz.relleno(elipse(0, -62, 58, 52, 0, 72), col)
        lz.relleno(elipse(10 * sx, -44, 38, 30, 0, 56), panza)
        lz.relleno(terminador(0, -62, 57, -math.pi / 2 - 0.5 * sx, 0.55), SOMBRA, alfa=0.22)
        # ala
        a = -0.35 - 1.1 * aleteo
        with lz.grupo(-12 * sx, -60, 1.0, a * sx):
            lz.relleno(elipse(-20 * sx, 4, 30, 17, 0, 40), oscuro)
        # pico
        pb = 0.5 + 5 * boca
        lz.relleno(np.array([[50 * sx, -74 + pb * 0.2], [74 * sx, -66], [50 * sx, -58 + pb]]), (255, 168, 54))
        # ojo
        ex, ey = 22 * sx, -82
        if feliz > 0.5:
            lz.trazo(np.stack([ex + 12 * np.cos(np.linspace(np.pi * 1.1, np.pi * 1.9, 12)),
                               ey + 4 + 12 * np.sin(np.linspace(np.pi * 1.1, np.pi * 1.9, 12))], 1), TINTA, 6,
                     afinar=False)
        else:
            lz.relleno(circulo(ex, ey, 17, 36), (255, 255, 255))
            px_, py_ = ex + 6 * mirar[0], ey + 5 * mirar[1]
            lz.relleno(circulo(px_, py_, 9, 28), TINTA)
            lz.relleno(circulo(px_ + 3, py_ - 3, 3, 12), (255, 255, 255))
        if escarcha > 0.05:
            for i in range(9):
                a_ = i * 0.7 + 1.0
                lz.relleno(circulo(math.cos(a_) * 50, -62 + math.sin(a_) * 44 - 8, 4 + 2 * (i % 3), 10),
                           (235, 245, 255), alfa=escarcha * 0.9)


def kuri(lz, x, y, s=1.0, t=0.0, color=(64, 196, 190), mirar=(0.0, 0.0), aleteo=0.0, tiritar=0.0,
         feliz=0.0, escarcha=0.0, voltear=False, boca=0.0):
    """Kuri, mascota de Kuriox: robot explorador redondo con pantalla de cara y antena (origen en los pies).
    Misma firma que `pajaro`: mirar (-1..1), aleteo 0..1 (saluda con los brazos), tiritar 0..1, feliz, boca 0..1."""
    sx = -1 if voltear else 1
    dx = math.sin(t * 55) * 3.2 * tiritar
    col = mezcla(color, (205, 225, 250), escarcha * 0.55)
    oscuro = oscurecer(col, 0.35)
    claro = aclarar(col, 0.4)
    ojo = (150, 255, 236)
    with lz.grupo(x + dx, y, s):
        # patas
        for px_ in (-20, 20):
            lz.relleno(rect_red(px_ - 10, -20, 20, 22, 8), oscuro)
        # antena con foco que parpadea
        lz.trazo(np.array([[0, -108], [8 * sx, -138]]), oscuro, 6, afinar=False)
        pul = 0.6 + 0.4 * math.sin(t * 5)
        lz.halo(8 * sx, -144, 24, (255, 214, 64), alfa=0.5 * pul, r0=0.2)
        lz.relleno(circulo(8 * sx, -144, 9, 20), (255, 214, 64))
        # brazos
        for k in (-1, 1):
            a = (0.5 + 1.6 * aleteo * (1 if k * sx > 0 else 0.4)) * -k * sx if aleteo else 0.35 * k
            with lz.grupo(52 * k, -68, 1.0, a):
                lz.relleno(elipse(6 * k, 14, 12, 26, 0, 24), oscuro)
                lz.relleno(circulo(6 * k, 36, 11, 18), claro)
        # cuerpo
        lz.relleno(rect_red(-52, -116, 104, 100, 40), col)
        lz.relleno(elipse(0, -36, 30, 14, 0, 28), claro, alfa=0.8)
        lz.relleno(terminador(0, -66, 52, -math.pi / 2 - 0.5 * sx, 0.55), SOMBRA, alfa=0.22)
        # pantalla-cara
        lz.relleno(rect_red(-38, -104, 76, 52, 22), (28, 32, 70))
        for ex in (-16, 16):
            ox, oy = ex + 5 * mirar[0], -80 + 4 * mirar[1]
            if feliz > 0.5:
                arc = np.linspace(np.pi * 1.1, np.pi * 1.9, 12)
                lz.trazo(np.stack([ox + 9 * np.cos(arc), oy + 5 + 9 * np.sin(arc)], 1), ojo, 5, afinar=False)
            else:
                lz.relleno(elipse(ox, oy, 8, 11, 0, 24), ojo)
                lz.relleno(circulo(ox + 2, oy - 4, 3, 10), (255, 255, 255))
        m = 7 + 6 * boca
        lz.trazo(np.stack([5 * mirar[0] + np.linspace(-m, m, 10),
                           -62 + 2 * np.sin(np.linspace(0, np.pi, 10)) * (1 + 2 * boca)], 1), ojo, 4, afinar=False)
        if escarcha > 0.05:
            for i in range(9):
                a_ = i * 0.7 + 1.0
                lz.relleno(circulo(math.cos(a_) * 46, -66 + math.sin(a_) * 46, 4 + 2 * (i % 3), 10),
                           (235, 245, 255), alfa=escarcha * 0.9)


mascota = kuri      # mascota de Kuriox (NO usar `pajaro`: es la mascota de otro canal)


def microbio(lz, x, y, s, t, color=(120, 230, 150), seed=0, forma=0, mirar=(0.0, 0.0), brillo=0.4):
    """Microbio blandito con ojos y cilios. forma 0 = píldora, 1 = redondo, 2 = alargado."""
    rx, ry = [(42, 26), (32, 30), (58, 20)][forma % 3]
    fase = seed * 1.7
    rot = 0.3 * math.sin(t * 0.9 + fase) + seed * 0.8
    with lz.grupo(x, y, s, rot):
        if brillo > 0:
            lz.halo(0, 0, rx * 2.1, color, alfa=0.35 * brillo, r0=0.3)
        n = 64
        th = np.linspace(0, 2 * np.pi, n, endpoint=False)
        wob = 1 + 0.06 * np.sin(th * 3 + t * 4 + fase) + 0.04 * np.sin(th * 5 - t * 3 + fase)
        # cilios
        cil = aclarar(color, 0.3)
        for k in range(14):
            a = k / 14 * 2 * np.pi
            bx, by = rx * math.cos(a), ry * math.sin(a)
            nx, ny = math.cos(a) * ry, math.sin(a) * rx
            L = 1.0 / max(1e-6, math.hypot(nx, ny)) * 12
            ond = 0.5 * math.sin(t * 9 + k * 1.3 + fase)
            lz.trazo(np.array([[bx, by], [bx + nx * L + ny * L * ond * 0.4, by + ny * L - nx * L * ond * 0.4]]),
                     cil, 3.2, afinar=False)
        P = np.stack([rx * wob * np.cos(th), ry * wob * np.sin(th)], 1)
        lz.relleno(P, color)
        lz.relleno(P * [0.8, 0.6] + [rx * 0.08, ry * 0.25], oscurecer(color, 0.25), alfa=0.5)
        lz.relleno(elipse(-rx * 0.35, -ry * 0.45, rx * 0.3, ry * 0.18, 0, 20), aclarar(color, 0.55), alfa=0.8)
        for ex in (-9, 9):
            lz.relleno(circulo(ex + rx * 0.15, -3, 7, 18), (255, 255, 255))
            lz.relleno(circulo(ex + rx * 0.15 + 2.5 * mirar[0], -3 + 2.5 * mirar[1], 3.6, 12), TINTA)


def arbol(lz, x, y, s=1.0, t=0.0, hojas=(80, 176, 100), perdida=0.0, seed=0, escarcha=0.0, oscuro=0.0):
    """Árbol de copa redonda (origen en la base). perdida 0..1: las hojas se secan y caen. oscuro: noche."""
    col = mezcla(hojas, (150, 130, 110), clamp01(perdida * 1.6))
    col = mezcla(col, (220, 232, 248), escarcha)
    col = mezcla(col, (16, 20, 56), oscuro)
    with lz.grupo(x, y, s):
        tronco = mezcla(mezcla((122, 84, 76), (150, 150, 175), escarcha * 0.6), (16, 20, 56), oscuro)
        lz.relleno(rect_red(-14, -170, 28, 172, 8), tronco)
        lz.relleno(np.array([[0, -110], [52, -150], [58, -142], [6, -96]]), tronco)
        vis = 1 - clamp01((perdida - 0.35) / 0.65)
        if vis > 0.02:
            a = min(1.0, vis * 1.4)
            for dx, dy, r in ((-62, -150, 44), (60, -160, 44), (-50, -200, 62), (40, -210, 68), (-5, -262, 72)):
                rr = r * (0.6 + 0.4 * vis)
                lz.relleno(circulo(dx, dy, rr, 48), col, alfa=a)
                lz.relleno(terminador(dx, dy, rr, -math.pi * 0.72, 0.1), SOMBRA, alfa=0.22 * a)
            lz.relleno(circulo(-22, -282, 30 * (0.6 + 0.4 * vis), 32), aclarar(col, 0.3), alfa=0.7 * vis)


def hojas_cayendo(lz, x, y, t, t0, n=10, col=(170, 140, 100), seed=3):
    """Hojas que caen desde (x, y) a partir de t0."""
    if t < t0:
        return
    for i in range(n):
        u = t - t0 - i * 0.12
        if u <= 0:
            continue
        hx = x + (i * 37 % 140 - 70) + 30 * math.sin(u * 2.5 + i)
        hy = y + (i * 23 % 60) + u * 120
        lz.relleno(elipse(hx, hy, 9, 5, u * 2 + i, 12), col, alfa=clamp01(1.6 - u * 0.5))


# ------------------------------------------------------------------ objetos
def termometro(lz, x, y, s, nivel, col=(255, 90, 90), marcas=6):
    """Termómetro vertical (origen = centro del bulbo). nivel 0..1."""
    with lz.grupo(x, y, s):
        lz.relleno(rect_red(-26, -420, 52, 420, 26), (228, 236, 255))
        lz.relleno(circulo(0, 0, 48, 48), (228, 236, 255))
        lz.relleno(circulo(0, 0, 34, 40), col)
        h = 20 + 360 * clamp01(nivel)
        lz.relleno(rect_red(-12, -h, 24, h + 4, 12), col)
        lz.relleno(rect_red(-18, -410, 8, 380, 4), (255, 255, 255), alfa=0.5)
        for i in range(marcas + 1):
            yy = -60 - i * (330 / marcas)
            lz.relleno(rect_red(26, yy - 3, 22 if i % 2 == 0 else 14, 6, 3), (228, 236, 255), alfa=0.9)


def fumarola(lz, x, y, s, t, calor=1.0, agua=(14, 30, 72)):
    """Chimenea hidrotermal del fondo del mar (origen en la base) con penacho y brillo.
    agua: color del fondo (el humo se funde con él al subir)."""
    with lz.grupo(x, y, s):
        roca, roca_c = (58, 44, 74), (92, 70, 108)
        lz.relleno(np.array([[-110, 0], [-70, -120], [-48, -230], [-30, -300], [30, -300], [44, -220],
                             [66, -110], [100, 0]]), roca)
        lz.relleno(np.array([[-70, -120], [-48, -230], [-30, -300], [-8, -300], [-20, -220], [-36, -110], [-60, 0],
                             [-110, 0]]), roca_c)
        for yy, w in ((-80, 150), (-170, 110), (-250, 80)):
            lz.relleno(elipse(0, yy, w * 0.55, 14, 0, 30), oscurecer(roca, 0.3), alfa=0.6)
        for bx, by, br in ((-60, -60, 26), (50, -140, 20), (-30, -200, 16), (20, -260, 13)):
            lz.relleno(circulo(bx, by, br, 20), roca_c if bx < 0 else oscurecer(roca, 0.2))
        lz.halo(0, -300, 190, (255, 110, 40), alfa=0.6 * calor, r0=0.08)
        # penacho: bocanadas opacas (las viejas arriba), que se funden con el agua al subir
        n = 12
        us = sorted(((t * 0.3 + i / n) % 1.0, i) for i in range(n))
        for u, i in reversed(us):
            py = -300 - u * 400
            px = 16 * math.sin(u * 5 + i * 0.7) + u * 50
            r = 24 + 48 * u
            c = mezcla(mezcla((110, 96, 120), (255, 150, 90), 0.35 * (1 - u) ** 4 * calor), agua, u ** 0.6)
            lz.relleno(circulo(px, py, r, 32), c)
        lz.relleno(elipse(0, -300, 30, 9, 0, 24), (255, 176, 80))


# ------------------------------------------------------------------ ondas y líneas
def onda(lz, x, y, r, ancho, color, alfa=1.0, capa=None, frente=0.45, estela=1.8):
    """Frente de onda luminoso (anillo) de radio r: borde delantero nítido y estela suave hacia dentro."""
    if alfa <= 0.003 or r <= 0:
        return
    c = lz.a_px([[x, y]])[0] * SS
    esc = lz.escala() * SS
    R, A = r * esc, max(1.0, ancho * esc)
    col = np.array(lz._col(color)[:3], np.float32)
    ext = R + A * 3 * max(frente, estela)

    def dibuja(dst, off):
        h, w = dst.shape[:2]
        f = 4
        hs, ws = max(2, h // f + 1), max(2, w // f + 1)
        ox, oy = off / 16
        xs = (np.arange(ws, dtype=np.float32) * f + ox - c[0])[None, :]
        ys = (np.arange(hs, dtype=np.float32) * f + oy - c[1])[:, None]
        d = np.sqrt(xs * xs + ys * ys) - R
        k = np.where(d > 0, 1.0 / (A * frente), 1.0 / (A * estela)).astype(np.float32)
        aa = np.exp(-(d * k) ** 2)
        rellenar_suave(dst, aa, f, col)

    lz._dibujar_en(lz._buf(capa), (c[0] - ext, c[1] - ext, c[0] + ext, c[1] + ext), dibuja, alfa)


def discontinua(lz, pts, color, ancho=4.0, largo=22.0, hueco=16.0, fase=0.0, frac=1.0, capa=None):
    """Línea discontinua a lo largo de la polilínea pts (coords locales). frac: porción dibujada."""
    Pp = np.asarray(pts, float)
    seg = np.hypot(*np.diff(Pp, axis=0).T)
    d = np.concatenate([[0.0], np.cumsum(seg)])
    total = d[-1] * clamp01(frac)
    per = largo + hueco
    s0 = -(fase % per)
    ini = np.arange(s0, total, per)
    a = np.maximum(ini, 0.0)
    b = np.minimum(ini + largo, total)
    ok = b > a + 0.5
    a, b = a[ok], b[ok]
    if not len(a):
        return
    if lz.recortes:   # con recorte: trazo a trazo (lento pero exacto)
        for aa, bb in zip(a, b):
            xs = np.interp([aa, (aa + bb) / 2, bb], d, Pp[:, 0])
            ys = np.interp([aa, (aa + bb) / 2, bb], d, Pp[:, 1])
            lz.trazo(np.stack([xs, ys], 1), color, ancho, afinar=False, capa=capa, paso=4.0)
        return
    # rápido: todos los trazos en una sola llamada de OpenCV (sin temblor: vector plano)
    m = (a + b) / 2
    trozos = np.stack([np.stack([np.interp(v, d, Pp[:, 0]), np.interp(v, d, Pp[:, 1])], -1) for v in (a, m, b)], 1)
    Q = lz.a_px(trozos.reshape(-1, 2)).reshape(-1, 3, 2)
    w = ancho * lz.escala()
    if w <= 0.05:
        return
    en_pant = ((Q[:, :, 0] > -50) & (Q[:, :, 0] < W_ + 50) & (Q[:, :, 1] > -50) & (Q[:, :, 1] < H_ + 50)).any(1)
    Q = Q[en_pant]
    if not len(Q):
        return
    Qi = np.round(Q * SS * 16).astype(np.int32)
    cv2.polylines(lz._buf(capa), list(Qi), False, lz._col(color), max(1, int(round(w * SS))), cv2.LINE_AA, 4)


def arco_pts(x, y, r, a0, a1, n=240):
    th = np.linspace(a0, a1, n)
    return np.stack([x + r * np.cos(th), y + r * np.sin(th)], 1)


# ------------------------------------------------------------------ texto
def rotulo(lz, x, y, texto, px=46, k=1.0, color=BLANCO, fuente="geo", ancla=(0.5, 0.5), alfa=1.0, sombra=0.45,
           capa=2, rot=0.0):
    """Texto blanco limpio con sombra suave (sin contorno)."""
    if k <= 0.01 or alfa <= 0.01:
        return
    if sombra > 0:
        lz.texto(texto, x + 3, y + 4, px, fuente, color=(12, 10, 40), borde=None, k=k, ancla=ancla,
                 alfa=alfa * sombra, capa=capa, temblor=0.0, rot=rot)
    lz.texto(texto, x, y, px, fuente, color=color, borde=None, k=k, ancla=ancla, alfa=alfa, capa=capa,
             temblor=0.0, rot=rot)


def pastilla(lz, x, y, texto, px=40, k=1.0, fondo=(255, 255, 255), color=(34, 28, 80), fuente="geo", alfa=1.0,
             capa=2):
    """Etiqueta en cápsula redondeada (fondo claro, texto oscuro)."""
    if k <= 0.01 or alfa <= 0.01:
        return
    from motor import ancho_texto
    w = ancho_texto(texto, fuente, px) + px * 1.1
    h = px * 1.55
    with lz.capa(capa):
        with lz.grupo(x, y, k):
            lz.relleno(rect_red(-w / 2, -h / 2, w, h, h / 2), fondo, alfa=alfa)
            lz.texto(texto, 0, px * 0.05, px, fuente, color=color, borde=None, alfa=alfa, temblor=0.0)


def linea_llamada(lz, p0, p1, frac=1.0, col=(255, 255, 255), ancho=3.0, alfa=0.9):
    """Línea fina de llamada (del objeto al rótulo) con punto en el origen."""
    if frac <= 0.01:
        return
    p0, p1 = np.array(p0, float), np.array(p1, float)
    lz.puntos([p0], 6, col)
    lz.trazo(np.array([p0, p0 + (p1 - p0) * clamp01(frac)]), col, ancho, afinar=False)


# ------------------------------------------------------------------ planetas y estrellas
PLANETAS = {   # color base, color de bandas
    "mercurio": ((168, 158, 172), None),
    "venus": ((242, 212, 150), (226, 192, 128)),
    "marte": ((222, 108, 74), None),
    "jupiter": ((234, 188, 140), (200, 140, 98)),
    "saturno": ((238, 214, 158), (214, 184, 122)),
    "urano": ((156, 222, 232), None),
    "neptuno": ((86, 126, 232), (66, 100, 206)),
}


def _anillo_saturno(lz, x, y, r, tilt, mitad, col, alfa=1.0):
    """Mitad trasera (mitad=0) o delantera (mitad=1) de los anillos."""
    th = np.linspace(np.pi, 2 * np.pi, 48) if mitad == 0 else np.linspace(0, np.pi, 48)
    a, b = r * 2.25, r * 0.62
    ext = np.stack([a * np.cos(th), b * np.sin(th)], 1)
    inn = np.stack([a * 0.62 * np.cos(th[::-1]), b * 0.62 * np.sin(th[::-1])], 1)
    P = _rotar(np.concatenate([ext, inn]), tilt, x, y)
    lz.relleno(P, col, alfa=alfa)
    th2 = th
    ext2 = np.stack([a * 0.86 * np.cos(th2), b * 0.86 * np.sin(th2)], 1)
    inn2 = np.stack([a * 0.8 * np.cos(th2[::-1]), b * 0.8 * np.sin(th2[::-1])], 1)
    lz.relleno(_rotar(np.concatenate([ext2, inn2]), tilt, x, y), oscurecer(col, 0.35), alfa=alfa)


def planeta(lz, x, y, r, tipo, t=0.0, luz=1.0, ang_luz=math.pi, seed=0):
    """Planeta del sistema solar (no la Tierra: usa tierra()). luz 0..1 (0 = sin Sol)."""
    base, bandas = PLANETAS[tipo]
    noche = (38, 36, 72)
    col = mezcla(base, noche, (1 - luz) * 0.85)
    colb = mezcla(bandas, noche, (1 - luz) * 0.85) if bandas else None
    tilt = -0.25
    if tipo == "saturno":
        _anillo_saturno(lz, x, y, r, tilt, 0, mezcla((226, 204, 150), noche, (1 - luz) * 0.85))

    def contenido():
        if colb is not None:
            for i, (hh, gros) in enumerate(((-0.62, 0.1), (-0.3, 0.14), (0.05, 0.1), (0.35, 0.16), (0.68, 0.09))):
                yy = y + hh * r
                xs = np.linspace(x - r * 1.1, x + r * 1.1, 24)
                ond = r * 0.025 * np.sin(xs / (r * 0.3) + i + t * 0.2)
                top = np.stack([xs, yy - gros * r / 2 + ond], 1)
                bot = np.stack([xs[::-1], yy + gros * r / 2 + ond[::-1]], 1)
                lz.relleno(_rotar(np.concatenate([top, bot]) - [x, y], tilt, x, y), colb, alfa=0.8)
        if tipo == "jupiter":
            lz.relleno(elipse(x + r * 0.3, y + r * 0.34, r * 0.2, r * 0.11, tilt, 28),
                       mezcla((214, 110, 84), noche, (1 - luz) * 0.85))
        if tipo in ("mercurio", "marte"):
            for dx, dy, s in ((-0.3, -0.25, 0.2), (0.3, 0.15, 0.14), (-0.05, 0.45, 0.12), (0.4, -0.4, 0.09)):
                lz.relleno(circulo(x + dx * r, y + dy * r, s * r, 24), oscurecer(col, 0.18))
        if tipo == "marte":
            lz.relleno(elipse(x, y - r * 0.9, r * 0.4, r * 0.14, tilt, 24), mezcla((250, 244, 240), noche, 1 - luz))

    esfera(lz, x, y, r, col, ang_luz, sombra=-0.05, fuerza=0.55 * luz + 0.15, rim=0.07 * luz,
           color_rim=aclarar(base, 0.5), contenido=contenido)
    if tipo == "saturno":
        _anillo_saturno(lz, x, y, r, tilt, 1, mezcla((226, 204, 150), noche, (1 - luz) * 0.85))


def sol_corte(lz, x, y, r, t, apertura=1.0, nucleo=1.0, ang=-0.55, brillo=1.0):
    """Sol con una cuña recortada que muestra núcleo, zona radiativa y zona convectiva.
    apertura 0..1 (ancho de la cuña); nucleo 0..1 (0 = núcleo apagado, gris)."""
    sol(lz, x, y, r, t, brillo=brillo)
    if apertura <= 0.01:
        return
    w = 1.7 * apertura
    if w >= 2 * np.pi * 0.995:     # corte completo: todo el disco (sin costura)
        cuna = circulo(x, y, r * 1.2, 160)
    else:
        th = np.linspace(ang - w / 2, ang + w / 2, 60)
        cuna = np.concatenate([[[x, y]], np.stack([x + r * 1.2 * np.cos(th), y + r * 1.2 * np.sin(th)], 1)])
    with lz.recorte(cuna):
        lz.relleno(circulo(x, y, r * 1.001, 160), (236, 96, 48))
        for i in range(22):   # celdas de convección
            a = ang - w / 2 + (i + 0.5) / 22 * w
            rr = r * (0.84 + 0.06 * math.sin(t * 1.5 + i * 2.1))
            lz.relleno(circulo(x + rr * math.cos(a), y + rr * math.sin(a), r * 0.07, 24), (255, 140, 66), alfa=0.8)
        lz.relleno(circulo(x, y, r * 0.7, 140), (255, 176, 70))
        for k in range(1, 5):   # zona radiativa: anillos concéntricos
            lz.relleno(circulo(x, y, r * (0.7 - k * 0.09), 120), (255, 176, 70) if k % 2 == 0 else (255, 194, 92))
        cn = mezcla((140, 132, 164), (255, 252, 226), nucleo)
        lz.relleno(circulo(x, y, r * 0.29, 90), mezcla((110, 100, 136), (255, 226, 150), nucleo))
        lz.halo(x, y, r * 0.36, mezcla((110, 100, 136), (255, 244, 200), nucleo), alfa=0.9 * nucleo, r0=0.55)
        lz.relleno(circulo(x, y, r * 0.24, 90), cn)
    for a in ((ang - w / 2, ang + w / 2) if apertura < 1.25 else ()):   # bordes del corte
        lz.trazo(np.array([[x, y], [x + r * math.cos(a), y + r * math.sin(a)]]), (255, 226, 170), 3 * max(1, r / 300),
                 afinar=False)


_GAL_RNG = np.random.default_rng(77)
_N_GAL = 5200


def _puntos_galaxia():
    rng = _GAL_RNG
    brazos = rng.integers(0, 2, _N_GAL)
    u = rng.random(_N_GAL) ** 0.8
    rho = 0.1 + 0.9 * u
    phi = brazos * np.pi + 5.2 * np.log(rho + 0.05) + rng.normal(0, 0.28 + 0.2 * (1 - u), _N_GAL)
    rho = rho + rng.normal(0, 0.03, _N_GAL)
    nb = 1600
    rb = np.abs(rng.normal(0, 0.12, nb))
    pb = rng.random(nb) * 2 * np.pi
    rho = np.concatenate([rho, rb])
    phi = np.concatenate([phi, pb])
    tipo = np.concatenate([np.where(rng.random(_N_GAL) < 0.12, 2, 1), np.zeros(nb, int)])
    tam = np.concatenate([0.7 + 1.6 * rng.random(_N_GAL) ** 4, 0.8 + 1.2 * rng.random(nb) ** 3])
    return rho, phi, tipo, tam


_GAL = _puntos_galaxia()


def galaxia(lz, x, y, R, t=0.0, rot=0.0, inclin=0.5, alfa=1.0, fondo=(12, 12, 34)):
    """Galaxia espiral (Vía Láctea estilizada) de radio R; alfa mezcla hacia el color de fondo."""
    if alfa <= 0.01 or R < 2:
        return
    lz.halo(x, y, R * 1.25, (90, 90, 190), alfa=0.35 * alfa)
    lz.halo(x, y, R * 0.42, (255, 214, 170), alfa=0.8 * alfa, r0=0.2)
    rho, phi, tipo, tam = _GAL
    ph = phi + rot
    X = x + R * rho * np.cos(ph)
    Y = y + R * rho * np.sin(ph) * inclin
    esc = max(0.6, min(3.0, R / 500))
    for k, col in enumerate(((255, 226, 186), (190, 206, 255), (255, 150, 206))):
        m = tipo == k
        lz.puntos(np.stack([X[m], Y[m]], 1), tam[m] * esc, mezcla(fondo, col, alfa))


def estrella_neutrones(lz, x, y, r, col=(170, 210, 255), brillo=1.0):
    lz.halo(x, y, r * 5, col, alfa=0.6 * brillo)
    lz.relleno(circulo(x, y, r, 32), aclarar(col, 0.6))


# ------------------------------------------------------------------ personas, casas, animales, iconos
def humano(lz, x, y, s=1.0, t=0.0, ropa=(92, 142, 232), piel=(250, 202, 164), pelo=(64, 44, 44), paso=0.0,
           brazo=0.0, voltear=False):
    """Persona simple estilo Kurzgesagt (origen en los pies, altura ~170*s)."""
    sx = -1 if voltear else 1
    with lz.grupo(x, y, s):
        pierna = oscurecer(ropa, 0.35)
        for k, lado in enumerate((-1, 1)):
            a = 0.35 * math.sin(t * 7 + k * math.pi) * paso
            with lz.grupo(lado * 9, -62, 1.0, a):
                lz.relleno(rect_red(-8, 0, 16, 62, 8), pierna)
        lz.relleno(rect_red(-24, -122, 48, 70, 20), ropa)
        with lz.grupo(22 * sx, -112, 1.0, (-0.3 - 1.6 * brazo) * sx):
            lz.relleno(rect_red(-7, 0, 14, 52, 7), oscurecer(ropa, 0.12))
        lz.relleno(circulo(0, -146, 24, 36), piel)
        lz.relleno(np.concatenate([P for P in [np.stack([24 * np.cos(np.linspace(np.pi, 2 * np.pi, 20)),
                                                        -146 + 24 * np.sin(np.linspace(np.pi, 2 * np.pi, 20))], 1)]]),
                   pelo)
        lz.relleno(circulo(9 * sx, -144, 3.2, 10), TINTA)


def casa(lz, x, y, s=1.0, calor=0.0, oscuro=0.0):
    """Casita (origen en la base). calor 0..1: ventana encendida con luz cálida."""
    pared = mezcla((226, 214, 204), (40, 40, 70), oscuro)
    techo = mezcla((190, 86, 76), (40, 30, 60), oscuro)
    with lz.grupo(x, y, s):
        lz.relleno(rect_red(-50, -80, 100, 80, 4), pared)
        lz.relleno(np.array([[-62, -76], [0, -128], [62, -76]]), techo)
        lz.relleno(rect_red(22, -122, 16, 34, 2), techo)
        v = mezcla((70, 80, 110), (255, 186, 96), calor)
        if calor > 0.05:
            lz.halo(-18, -46, 60, (255, 170, 80), alfa=0.6 * calor)
        lz.relleno(rect_red(-34, -60, 32, 28, 3), v)
        lz.relleno(rect_red(12, -48, 22, 48, 3), mezcla((120, 84, 70), (40, 30, 60), oscuro))


def planta(lz, x, y, s=1.0, t=0.0, vida=1.0, col=(96, 196, 110)):
    """Plantita/flor (origen en la base). vida 0..1: 0 = seca y caída."""
    c = mezcla((150, 120, 90), col, vida)
    inc = (1 - vida) * 0.9
    with lz.grupo(x, y, s, inc):
        lz.relleno(rect_red(-3, -60, 6, 60, 3), c)
        for lado in (-1, 1):
            with lz.grupo(0, -30, 1.0, lado * (0.9 - 0.5 * (1 - vida))):
                lz.relleno(elipse(0, -16, 9, 18, 0, 20), c)
        lz.relleno(circulo(0, -66, 11 * (0.5 + 0.5 * vida), 20), mezcla((150, 120, 90), (255, 200, 90), vida))


def conejo(lz, x, y, s=1.0, t=0.0, col=(196, 184, 178), voltear=False, salto=0.0):
    sx = -1 if voltear else 1
    with lz.grupo(x, y - salto, s):
        lz.relleno(elipse(-6 * sx, -34, 40, 30, 0, 36), col)
        lz.relleno(circulo(-44 * sx, -40, 12, 18), (250, 248, 246))
        lz.relleno(circulo(26 * sx, -56, 22, 30), col)
        for k, a in enumerate((-0.25, 0.05)):
            with lz.grupo((20 + 8 * k) * sx, -72, 1.0, a * sx):
                lz.relleno(elipse(0, -24, 7, 26, 0, 20), col)
                lz.relleno(elipse(0, -24, 3.5, 18, 0, 14), (240, 190, 196))
        lz.relleno(circulo(34 * sx, -60, 4, 10), TINTA)
        for px_ in (-24, 12):
            lz.relleno(elipse(px_ * sx, -4, 14, 6, 0, 16), oscurecer(col, 0.15))


def zorro(lz, x, y, s=1.0, t=0.0, voltear=False):
    sx = -1 if voltear else 1
    nar, bla = (236, 128, 60), (250, 246, 240)
    with lz.grupo(x, y, s):
        with lz.grupo(-50 * sx, -40, 1.0, (0.5 + 0.15 * math.sin(t * 3)) * sx):
            lz.relleno(elipse(-30 * sx, 0, 38, 16, 0, 30), nar)
            lz.relleno(elipse(-58 * sx, 0, 12, 10, 0, 16), bla)
        lz.relleno(elipse(0, -40, 46, 24, 0, 36), nar)
        for px_ in (-28, -12, 18, 32):
            lz.relleno(rect_red(px_ * sx - 4, -24, 8, 24, 4), oscurecer(nar, 0.45))
        lz.relleno(np.array([[30 * sx, -46], [78 * sx, -58], [38 * sx, -78]]), nar)
        lz.relleno(np.array([[62 * sx, -54], [80 * sx, -58], [66 * sx, -64]]), bla)
        for ex in (34, 50):
            lz.relleno(np.array([[ex * sx, -70], [(ex + 4) * sx, -96], [(ex + 14) * sx, -72]]), nar)
        lz.relleno(circulo(52 * sx, -64, 3.5, 10), TINTA)


def gusano_tubo(lz, x, y, s=1.0, t=0.0, seed=0, alto=1.0):
    """Gusano de tubo gigante (Riftia): tubo blanco y penacho rojo que se mece (origen en la base)."""
    oscil = 0.12 * math.sin(t * 1.3 + seed * 1.7)
    with lz.grupo(x, y, s, oscil):
        h = 150 * alto
        lz.relleno(rect_red(-9, -h, 18, h, 9), (226, 222, 214))
        lz.relleno(rect_red(-9, -h, 7, h, 4), (250, 248, 244), alfa=0.7)
        for k in range(5):
            a = -0.7 + k * 0.35 + 0.1 * math.sin(t * 2 + k + seed)
            with lz.grupo(0, -h + 4, 1.0, a):
                lz.relleno(elipse(0, -20, 7, 22, 0, 20), (230, 52, 68))
        lz.relleno(circulo(0, -h - 6, 12, 20), (246, 80, 90))


def panel_solar(lz, x, y, s=1.0, activo=1.0):
    with lz.grupo(x, y, s):
        lz.relleno(rect_red(-6, -60, 12, 60, 3), (150, 156, 176))
        P = np.array([[-80, -60], [80, -60], [60, -130], [-60, -130]])
        lz.relleno(P, mezcla((60, 64, 90), (60, 120, 220), activo))
        for i in range(1, 4):
            u = i / 4
            lz.trazo(np.array([[-80 + 20 * u, -60 - 70 * u], [80 - 20 * u, -60 - 70 * u]]), (40, 60, 120), 3,
                     afinar=False)
        for i in range(1, 4):
            xx = -80 + 160 * i / 4
            lz.trazo(np.array([[xx, -60], [xx * 0.75, -130]]), (40, 60, 120), 3, afinar=False)


def central_nuclear(lz, x, y, s=1.0, t=0.0, activa=1.0):
    """Torre de refrigeración con vapor (origen en la base)."""
    with lz.grupo(x, y, s):
        yy = np.linspace(0, -170, 20)
        ancho = 70 - 40 * np.sin(np.linspace(0, np.pi * 0.8, 20))
        P = np.concatenate([np.stack([-ancho, yy], 1), np.stack([ancho[::-1], yy[::-1]], 1)])
        lz.relleno(P, (214, 214, 226))
        lz.relleno(P * [0.45, 1] - [ancho.max() * 0.45, 0], (240, 240, 248), alfa=0.6)
        if activa > 0:
            for i in range(6):
                u = (t * 0.25 + i / 6) % 1
                lz.relleno(circulo(10 * math.sin(i * 2 + u * 3), -190 - u * 160, 30 + 40 * u, 28), (236, 238, 248),
                           alfa=0.75 * (1 - u) * activa)


def interruptor(lz, x, y, s=1.0, encendido=1.0):
    with lz.grupo(x, y, s):
        lz.relleno(rect_red(-60, -90, 120, 180, 20), (236, 236, 244))
        lz.relleno(rect_red(-24, -54, 48, 108, 12), (196, 198, 214))
        yy = lerp(22, -22, encendido)
        lz.relleno(rect_red(-18, yy - 26, 36, 52, 10), (255, 255, 255))


def molecula(lz, x, y, s=1.0, tipo="O2", rot=0.0):
    """O2 (dos esferas rojas) o CO2 (carbono gris entre dos oxígenos)."""
    with lz.grupo(x, y, s, rot):
        if tipo == "CO2":
            for dx in (-34, 34):
                lz.relleno(circulo(dx, 0, 20, 24), (236, 84, 84))
            lz.relleno(circulo(0, 0, 22, 24), (90, 90, 104))
        else:
            for dx in (-15, 15):
                lz.relleno(circulo(dx, 0, 20, 24), (236, 84, 84))
        lz.relleno(circulo(-6, -8, 7, 12), (255, 255, 255), alfa=0.5)


__all__ = ["mezcla", "aclarar", "oscurecer", "terminador", "borde_luz", "esfera", "sol", "tierra", "luna", "pajaro", "kuri", "mascota",
           "microbio", "arbol", "hojas_cayendo", "termometro", "fumarola", "rotulo", "pastilla", "linea_llamada",
           "onda", "discontinua", "arco_pts", "SOMBRA", "TINTA", "lerp", "PLANETAS", "planeta", "sol_corte",
           "galaxia", "estrella_neutrones", "humano", "casa", "planta", "conejo", "zorro", "gusano_tubo",
           "panel_solar", "central_nuclear", "interruptor", "molecula"]
