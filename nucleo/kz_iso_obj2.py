# -*- coding: utf-8 -*-
"""Más utilería para dioramas isométricos de historia de México: lingotes y monedas, pergaminos, carteles, cofres, lluvia, brotes, banderas históricas, estandarte guadalupano,
tambores, libros, cadenas, escaleras, trincheras. Todas son fn(lz, iso, x, y, ...) con (x, y) en el suelo del mundo (z opcional)."""
import math

import numpy as np

import kz_iso as I
import kz_iso_obj as O
import plano as P
from kz_iso import tint, caja, cara_rect, sombra_elipse, sombra_suelo, Caja
from motor import circulo, elipse, rect_red, h01, catmull


def lingote(lz, iso, x, y, z=0.0, s=1.0, rot=0, brillo=0.0):
    """Barra de plata (prisma gris azulado con filo claro)."""
    w, d, h = 12 * s, 5 * s, 3.4 * s
    if rot:
        w, d = d, w
    caja(lz, iso, x - w / 2, y - d / 2, w, d, h, (170, 184, 212), z0=z)
    if brillo > 0.02:
        sx, sy = iso.P(x, y, z + h)
        lz.halo(sx, sy, 14 * iso.z * s, (255, 255, 255), alfa=0.5 * brillo, capa=2)


def pila_lingotes(lz, iso, x, y, n=6, s=1.0, z=0.0, t=0.0):
    k = 0
    fila = 0
    while k < n:
        for i in range(min(3 - fila, n - k)):
            lingote(lz, iso, x + (i - (2 - fila) / 2) * 13 * s, y, z + fila * 3.6 * s, s, brillo=0.5 + 0.5 * math.sin(t * 3 + k))
            k += 1
        fila += 1
        if fila >= 3:
            fila = 0
            z += 11 * s


def moneda(lz, iso, x, y, z=0.0, r=4.0, t=0.0, giro=True, color=(250, 200, 60)):
    """Moneda de oro/plata en pie que gira (ancho oscila con cos) con destello."""
    sx, sy = iso.P(x, y, z)
    k = iso.z
    w = abs(math.cos(t * 5 + x)) if giro else 1.0
    lz.relleno(elipse(sx, sy, max(0.6, r * w) * k, r * k, 0, 14), tint(P.oscurecer(color, 0.25)))
    lz.relleno(elipse(sx - 0.5 * k, sy, max(0.5, r * w * 0.82) * k, r * 0.82 * k, 0, 14), tint(color))
    lz.relleno(elipse(sx - r * 0.2 * k, sy - r * 0.2 * k, max(0.3, r * w * 0.3) * k, r * 0.28 * k, 0, 8), tint(P.aclarar(color, 0.55)))


def cofre(lz, iso, x, y, s=1.0, abierto=0.0, brillo=1.0, oro=True):
    sombra_elipse(lz, iso, x + 4 * s, y + 2 * s, 11 * s, 6 * s, 0.2)
    c = caja(lz, iso, x - 9 * s, y - 6 * s, 18 * s, 12 * s, 9 * s, (150, 98, 66))
    cara_rect(lz, iso, c, "y", 0, c.w, 3.2 * s, 5 * s, (250, 206, 90))
    cara_rect(lz, iso, c, "x", 0, c.d, 3.2 * s, 5 * s, (250, 206, 90))
    sx, sy = iso.P(x, y, 9 * s)
    k = iso.z * s
    if abierto > 0.3:
        lz.relleno(rect_red(sx - 9 * k, sy - 4 * k - 7 * k * abierto, 18 * k, 3 * k, 1.0 * k), tint((120, 78, 56)))
        if oro:
            lz.relleno(elipse(sx, sy - 1 * k, 8 * k, 3.4 * k, 0, 12), tint((250, 206, 90)))
            lz.halo(sx, sy - 6 * k, 30 * k * brillo, (255, 226, 130), alfa=0.6 * brillo, capa=2)
    else:
        lz.relleno(elipse(sx, sy - 0.5 * k, 9 * k, 4.4 * k, 0, 14), tint((176, 120, 82)))


def pergamino(lz, iso, x, y, z=0.0, w=12.0, h=16.0, rot=0.0, lineas=True, sello=(206, 60, 60), abre=1.0, billboard=True):
    """Pergamino enrollado en los extremos (cartel en pantalla)."""
    sx, sy = iso.P(x, y, z)
    k = iso.z
    hh = h * abre
    lz.relleno(rect_red(sx - w * k / 2, sy - hh * k, w * k, hh * k, 1.2 * k), tint((252, 240, 210)))
    for dy, col in ((0, (206, 170, 120)), (hh, (206, 170, 120))):
        lz.relleno(rect_red(sx - w * k / 2 - 1.6 * k, sy - (dy + 1.6) * k, w * k + 3.2 * k, 3.2 * k, 1.6 * k), tint(col))
    if lineas:
        for i in range(4):
            lz.relleno(rect_red(sx - w * 0.36 * k, sy - (hh * 0.8 - i * hh * 0.18) * k, w * 0.72 * k * (0.7 + 0.3 * h01(i, 3)), 0.9 * k, 0.3 * k), tint((150, 120, 100)), alfa=0.7)
    if sello:
        lz.relleno(circulo(sx + w * 0.28 * k, sy - hh * 0.12 * k, 2.0 * k, 8), tint(sello))


def cartel(lz, iso, x, y, texto, h=26, w=30, color=(250, 240, 220), tinta=(150, 40, 40), px=9, poste=(130, 90, 66), t=0.0):
    """Cartel de madera con texto sobre un poste (SE VENDE, REMATE…)."""
    sx, sy = iso.P(x, y, 0)
    k = iso.z
    sombra_elipse(lz, iso, x + 2, y + 1, 5, 3, 0.18)
    lz.relleno(rect_red(sx - 1.2 * k, sy - h * k, 2.4 * k, h * k, 0.6 * k), tint(poste))
    sw = 0.8 * math.sin(t * 1.7 + x)
    lz.relleno(rect_red(sx - w / 2 * k, sy - (h + 13) * k + sw * k, w * k, 13 * k, 1.6 * k), tint(color))
    lz.relleno(rect_red(sx - w / 2 * k, sy - (h + 13) * k + sw * k, w * k, 2.0 * k, 1.0 * k), tint(P.oscurecer(color, 0.12)))
    lz.texto(texto, sx, sy - (h + 6.4) * k + sw * k, max(6, int(px * k)), "geo", color=tinta, borde=None, temblor=0.0, capa=2)


def lluvia(lz, t, dens=1.0, alfa=0.5, ang=0.28, largo=42, seed=1):
    """Lluvia en pantalla (capa superior)."""
    n = int(180 * dens)
    for i in range(n):
        x0 = (h01(seed, i) * 2300 - 200)
        ciclo = (t * 1.5 + h01(seed, i, 3)) % 1.0
        y0 = ciclo * 1300 - 120
        xx = x0 + math.sin(ang) * ciclo * 1300
        lz.relleno(np.array([[xx, y0], [xx + 2.2, y0], [xx + 2.2 + math.sin(ang) * largo, y0 + largo], [xx + math.sin(ang) * largo, y0 + largo]]), (200, 220, 255), alfa=alfa * 0.8, capa=2)


def nube_tormenta(lz, x, y, s=1.0, t=0.0, relampago=0.0):
    k = s
    for (dx, dy, r, c) in ((-70, 10, 58, (70, 56, 104)), (0, -6, 74, (86, 70, 122)), (74, 10, 56, (70, 56, 104)), (-30, 22, 52, (60, 48, 92)), (36, 24, 52, (60, 48, 92)),
                           (-20, -24, 40, (110, 92, 146)), (30, -26, 36, (110, 92, 146))):
        lz.relleno(circulo(x + dx * k + 4 * math.sin(t * 0.5 + dx), y + dy * k, r * k, 20), c, capa=2)
    if relampago > 0.02:
        lz.halo(x, y + 10 * k, 220 * k, (255, 250, 200), alfa=0.6 * relampago, capa=2)
        pts = [(x - 8 * k, y + 50 * k), (x + 14 * k, y + 110 * k), (x - 4 * k, y + 112 * k), (x + 18 * k, y + 190 * k), (x - 20 * k, y + 120 * k), (x - 2 * k, y + 118 * k)]
        lz.relleno(np.array(pts), (255, 244, 170), capa=2)


def brote(lz, iso, x, y, u=1.0, t=0.0, enojo=True, s=1.0, color=(110, 200, 100)):
    """Planta que crece (u 0..1) con una carita enojada en la flor: «el descontento sembrado»."""
    if u <= 0.01:
        return
    sx, sy = iso.P(x, y, 0)
    k = iso.z * s
    sombra_elipse(lz, iso, x + 2, y + 1, 5 * u, 3 * u, 0.2)
    h = 28 * u
    sw = 2.0 * math.sin(t * 2.2 + x) * u
    lz.relleno(np.array([[sx - 1.6 * k, sy], [sx + 1.6 * k, sy], [sx + (1.0 + sw) * k, sy - h * k], [sx + (-1.0 + sw) * k, sy - h * k]]), tint(color))
    for sg, ang in ((-1, -0.7), (1, 0.7)):
        lz.relleno(elipse(sx + sg * 8 * k * u + sw * 0.5 * k, sy - h * 0.55 * k, 9 * k * u, 4 * k * u, ang * sg, 12), tint(P.aclarar(color, 0.12)))
    r = 7.5 * k * u
    fx, fy = sx + sw * k, sy - h * k - r * 0.6
    for a in range(8):
        th = a * math.pi / 4
        lz.relleno(circulo(fx + math.cos(th) * r * 1.2, fy + math.sin(th) * r * 1.2, r * 0.62, 8), tint((226, 70, 90)))
    lz.relleno(circulo(fx, fy, r * 0.95, 14), tint((250, 200, 70)))
    if enojo and u > 0.5:
        for sg in (-1, 1):
            lz.relleno(circulo(fx + sg * r * 0.36, fy - r * 0.08, r * 0.14, 6), tint((50, 30, 40)))
            lz.relleno(np.array([[fx + sg * r * 0.7, fy - r * 0.40], [fx + sg * r * 0.1, fy - r * 0.18], [fx + sg * r * 0.1, fy - r * 0.30], [fx + sg * r * 0.7, fy - r * 0.52]]), tint((90, 30, 40)))
        lz.relleno(np.array([[fx - r * 0.35, fy + r * 0.42], [fx, fy + r * 0.28], [fx + r * 0.35, fy + r * 0.42], [fx, fy + r * 0.34]]), tint((90, 30, 40)))


def tambor(lz, iso, x, y, s=1.0, golpe=0.0):
    I.cilindro(lz, iso, x, y, 6 * s, 8 * s, (206, 66, 66))
    sx, sy = iso.P(x, y, 8 * s)
    k = iso.z * s
    lz.relleno(elipse(sx, sy, 6 * k * 1.22, 6 * k * 0.7, 0, 14), tint((246, 230, 190)))
    for dx in (-3, 3):
        lz.relleno(rect_red(sx + dx * k - 0.4 * k, sy - 8 * k - golpe * 3 * k, 0.8 * k, 8 * k, 0.3 * k), tint((130, 90, 66)))


def estandarte_virgen(lz, iso, x, y, h=64, t=0.0, w=34, alto=46):
    """Estandarte de la Virgen de Guadalupe (fondo azul-verde, mandorla dorada, silueta de la Virgen con manto), que ondea. Diseño estilizado propio."""
    sx, sy = iso.P(x, y, 0)
    k = iso.z
    lz.relleno(rect_red(sx - 1.2 * k, sy - (h + alto) * k, 2.4 * k, (h + alto) * k, 0.6 * k), tint((130, 96, 70)))
    lz.relleno(rect_red(sx - w * 0.6 * k, sy - (h + alto) * k - 1.6 * k, w * 1.2 * k, 2.4 * k, 1.0 * k), tint((130, 96, 70)))
    top = sy - (h + alto - 2) * k
    n = 12
    up, dn = [], []
    for i in range(n + 1):
        u = i / n
        off = 2.4 * math.sin(t * 3.4 - u * 4.0) * u
        up.append((sx + 1.2 * k + u * w * k, top + off * k))
        dn.append((sx + 1.2 * k + u * w * k, top + (alto + off) * k))
    lz.relleno(np.array(up + dn[::-1]), tint((60, 138, 150)))
    off = 2.4 * math.sin(t * 3.4 - 0.5 * 4.0) * 0.5
    cx, cy = sx + 1.2 * k + w * 0.5 * k, top + (alto * 0.5 + off) * k
    # mandorla de rayos dorados
    for i in range(16):
        a = i * math.pi / 8
        lz.relleno(np.array([[cx + math.cos(a - 0.08) * 10 * k, cy + math.sin(a - 0.08) * 14 * k], [cx + math.cos(a) * 20 * k, cy + math.sin(a) * 25 * k], [cx + math.cos(a + 0.08) * 10 * k, cy + math.sin(a + 0.08) * 14 * k]]), tint((250, 210, 100)))
    lz.relleno(elipse(cx, cy, 9 * k, 14 * k, 0, 18), tint((252, 226, 150)))
    # figura: manto verde-azul, túnica rosa, rostro
    lz.relleno(np.array([[cx, cy - 11 * k], [cx + 8 * k, cy + 12 * k], [cx - 8 * k, cy + 12 * k]]), tint((70, 150, 150)))
    lz.relleno(np.array([[cx, cy - 6 * k], [cx + 5 * k, cy + 12 * k], [cx - 5 * k, cy + 12 * k]]), tint((236, 130, 150)))
    lz.relleno(circulo(cx, cy - 9 * k, 3 * k, 8), tint((240, 190, 150)))
    lz.relleno(rect_red(cx - 7 * k, cy + 12 * k, 14 * k, 2.4 * k, 1.0 * k), tint((250, 206, 90)))


def bandera_trigarante(lz, iso, x, y, h=64, t=0.0, w=40, alto=24):
    """Bandera del Ejército Trigarante: tres franjas diagonales blanco, verde y rojo con estrellas (diseño de época)."""
    sx, sy = iso.P(x, y, 0)
    k = iso.z
    lz.relleno(rect_red(sx - 1.2 * k, sy - h * k, 2.4 * k, h * k, 0.6 * k), tint((130, 96, 70)))
    top = sy - h * k + 2 * k
    n = 12
    for fr, col in (((0, 1 / 3), (250, 250, 246)), ((1 / 3, 2 / 3), (46, 160, 80)), ((2 / 3, 1), (210, 50, 62))):
        up, dn = [], []
        for i in range(n + 1):
            u = i / n
            off = 2.6 * math.sin(t * 5.0 - u * 4.6) * u
            ya = (fr[0] * alto) + (u - 0.5) * alto * 0.55 * 1.0
            yb = (fr[1] * alto) + (u - 0.5) * alto * 0.55 * 1.0
            up.append((sx + 1.2 * k + u * w * k, top + (ya + off) * k))
            dn.append((sx + 1.2 * k + u * w * k, top + (yb + off) * k))
        lz.relleno(np.array(up + dn[::-1]), tint(col))
    for (u, v_) in ((0.28, 0.7), (0.5, 0.5), (0.72, 0.3)):
        off = 2.6 * math.sin(t * 5.0 - u * 4.6) * u
        P_.chispa(lz, sx + 1.2 * k + u * w * k, top + (v_ * alto + (u - 0.5) * alto * 0.55 + off) * k, 3.2 * k) if False else lz.relleno(circulo(sx + 1.2 * k + u * w * k, top + (v_ * alto + (u - 0.5) * alto * 0.55 + off) * k, 1.8 * k, 6), tint((250, 206, 90)))
    lz.relleno(circulo(sx, sy - h * k, 2.2 * k, 8), tint((250, 208, 90)))


def trinchera(lz, iso, x, y, w, d, h=7.0, tierra=(150, 112, 84)):
    """Trinchera con parapeto de tierra y sacos."""
    I.suelo_rect(lz, iso, x, y, w, d, P.oscurecer(tierra, 0.3))
    caja(lz, iso, x - 3, y - 3, w + 6, 4, h, tierra)
    caja(lz, iso, x - 3, y + d - 1, w + 6, 4, h, tierra)
    for i in range(int(w / 7)):
        caja(lz, iso, x + i * 7, y + d - 1, 5, 4, h + 2, (214, 190, 140))


def barricada(lz, iso, x, y, w=40, s=1.0):
    caja(lz, iso, x, y, w, 6, 8 * s, (150, 108, 76))
    for i in range(int(w / 9)):
        O.barril(lz, iso, x + 5 + i * 9, y + 10, s * 0.9)


def escalera(lz, iso, x, y, z0, z1, ancho=6.0):
    """Escalera de mano apoyada en un muro (de (x,y,z0) a (x,y+off,z1))."""
    a = iso.P(x, y, z0)
    b = iso.P(x, y - 4, z1)
    k = iso.z
    for off in (-ancho / 2, ancho / 2):
        lz.relleno(np.array([[a[0] + off * k - 0.8 * k, a[1]], [a[0] + off * k + 0.8 * k, a[1]], [b[0] + off * k + 0.8 * k, b[1]], [b[0] + off * k - 0.8 * k, b[1]]]), tint((150, 106, 76)))
    n = 7
    for i in range(n + 1):
        u = i / n
        yy = a[1] + (b[1] - a[1]) * u
        xx = a[0] + (b[0] - a[0]) * u
        lz.relleno(rect_red(xx - ancho * k / 2, yy - 0.7 * k, ancho * k, 1.4 * k, 0.4 * k), tint((176, 128, 92)))


def carruaje(lz, iso, x, y, t=0.0, mov=0.0, color=(206, 60, 70), s=1.0, caballos=2, dir=1):
    """Carruaje de gala (cabina con ventanillas, techo con farol, 4 ruedas) tirado por caballos."""
    import kz_gente_iso as G
    sx, sy = iso.P(x, y, 0)
    k = iso.z * s
    I.sombra_elipse(lz, iso, x + 6 * s, y + 2 * s, 30 * s, 10 * s, 0.22)
    rot = t * mov * 3.0
    for dx in (-17, 13):
        for off in (0, -4):
            lz.relleno(circulo(sx + dx * k, sy - 8 * k + off * 0.4 * k, 8.2 * k, 16), tint((120, 82, 60)))
            lz.relleno(circulo(sx + dx * k, sy - 8 * k + off * 0.4 * k, 5.6 * k, 14), tint((176, 128, 92)))
            for j in range(4):
                a = rot + j * math.pi / 4
                lz.relleno(np.array([[sx + dx * k + math.cos(a) * 5.4 * k, sy - 8 * k + math.sin(a) * 5.4 * k], [sx + dx * k - math.cos(a) * 5.4 * k, sy - 8 * k - math.sin(a) * 5.4 * k],
                                     [sx + dx * k - math.cos(a) * 5.4 * k + 1.0 * k, sy - 8 * k - math.sin(a) * 5.4 * k], [sx + dx * k + math.cos(a) * 5.4 * k + 1.0 * k, sy - 8 * k + math.sin(a) * 5.4 * k]]), tint((120, 82, 60)))
            break
    lz.relleno(rect_red(sx - 24 * k, sy - 34 * k, 48 * k, 22 * k, 3 * k), tint(P.oscurecer(color, 0.25)))
    lz.relleno(rect_red(sx - 24 * k, sy - 34 * k, 30 * k, 22 * k, 3 * k), tint(color))
    lz.relleno(rect_red(sx - 22 * k, sy - 30 * k, 12 * k, 12 * k, 2 * k), tint((250, 226, 150)))
    lz.relleno(rect_red(sx - 6 * k, sy - 30 * k, 12 * k, 12 * k, 2 * k), tint((250, 226, 150)))
    lz.relleno(np.array([[sx - 28 * k, sy - 34 * k], [sx + 26 * k, sy - 34 * k], [sx + 20 * k, sy - 44 * k], [sx - 22 * k, sy - 44 * k]]), tint((60, 44, 72)))
    lz.relleno(circulo(sx - 18 * k, sy - 48 * k, 2.6 * k, 8), tint((255, 220, 120)))
    lz.relleno(rect_red(sx - 26 * k, sy - 12 * k, 52 * k, 3 * k, 1), tint((250, 206, 90)))
    cabs = [(30 + 26 * i) * dir for i in range(caballos)]
    for i, cx_ in enumerate(cabs):
        G.caballo(lz, iso, x + cx_ * 0.0, y, t, dir=dir, seed=i + 3, vel=mov) if False else None


def faro_bandera(lz, iso, x, y, color=(206, 56, 70), t=0.0, h=60):
    """Mástil con la bandera de la Corona (rojo y oro con castillo/león estilizado)."""
    O.bandera(lz, iso, x, y, h=h, w=36, alto=24, color=color, t=t, franjas=[(color, 0.25), ((250, 206, 90), 0.5), (color, 0.25)])


def corona(lz, iso, x, y, z=0.0, s=1.0, rot=0.0, brillo=1.0):
    """Corona real de oro con joyas (cartel en pantalla, con giro opcional y halo)."""
    sx, sy = iso.P(x, y, z)
    k = iso.z * s
    c, sn = math.cos(rot), math.sin(rot)

    def R(pts):
        a = np.asarray(pts, float) * k
        return np.stack([sx + a[:, 0] * c - a[:, 1] * sn, sy + a[:, 0] * sn + a[:, 1] * c], 1)
    if brillo > 0.02:
        lz.halo(sx, sy - 6 * k, 26 * k, (255, 230, 140), alfa=0.5 * brillo, capa=2)
    lz.relleno(R([(-10, 0), (-12, -14), (-5, -7), (0, -17), (5, -7), (12, -14), (10, 0)]), tint((226, 160, 40)))
    lz.relleno(R([(-10, 0), (-12, -14), (-5, -7), (-2, -6), (-2, 0)]), tint((250, 206, 70)))
    lz.relleno(R([(-10, 0), (10, 0), (10, 4), (-10, 4)]), tint((226, 160, 40)))
    for dx, col in ((-6, (214, 52, 70)), (0, (60, 150, 230)), (6, (214, 52, 70))):
        lz.relleno(circulo(sx + (dx * c) * k, sy + (dx * sn + 2) * k, 1.6 * k, 8), tint(col))


def barrotes(lz, iso, x, y, w, h, n=7, z=0.0, color=(70, 66, 84)):
    """Reja de barrotes verticales a lo largo de x (prisión)."""
    for i in range(n + 1):
        px = x + w * i / n
        a = iso.P(px, y, z)
        b = iso.P(px, y, z + h)
        k = iso.z
        lz.relleno(rect_red(a[0] - 1.4 * k, b[1], 2.8 * k, a[1] - b[1], 0.8 * k), tint(color))
    for zz in (z + 3, z + h - 3):
        a = iso.P(x, y, zz)
        b = iso.P(x + w, y, zz)
        k = iso.z
        lz.relleno(np.array([[a[0], a[1] - 1.6 * k], [b[0], b[1] - 1.6 * k], [b[0], b[1] + 1.6 * k], [a[0], a[1] + 1.6 * k]]), tint(color))


def grillete(lz, iso, x, y, z, t=0.0):
    sx, sy = iso.P(x, y, z)
    k = iso.z
    for dx in (-5, 5):
        lz.trazo(np.stack([sx + dx * k + 2.6 * k * np.cos(np.linspace(0, 6.28, 14)), sy + 2.2 * k * np.sin(np.linspace(0, 6.28, 14))], 1), (150, 150, 170), 1.8 * k, cerrado=True, afinar=False, temblor=0.0, capa=2)
    lz.trazo(np.array([[sx - 5 * k, sy], [sx - 2 * k, sy + 4 * k + 1.2 * k * math.sin(t * 2)], [sx + 2 * k, sy + 4 * k], [sx + 5 * k, sy]]), (150, 150, 170), 1.6 * k, afinar=False, temblor=0.0, capa=2)
