# -*- coding: utf-8 -*-
"""Modelos de alambre para el kit LÍNEA 3D (13-nov-2026): Falcon 9 por partes (etapa 1 con 9 motores, aletas de rejilla y
patas; etapa 2 con tobera MVac; cápsula Dragon con morro que se abre), Estación Espacial, torre de servicio, zona de aterrizaje.
Medidas en METROS (proporciones del Falcon 9: 3,66 m de diámetro, ~70 m con Dragon); `esc` = unidades de mundo por metro
(el mundo de cohete_crs30 va en km: esc = 0.001). `eje` = hacia dónde apunta la nariz; `ref` fija el giro alrededor del eje.

Pila (z desde la salida de las toberas de la etapa 1): etapa 1 0-41 + interetapa 41-47,5 · etapa 2 base (salida MVac) en 41,3 ·
Dragon (tronco) en 60,5.  `Z_S2`, `Z_DRAGON` para colocar las piezas sueltas tras la separación.
"""
import math

import numpy as np

from linea3d import base_de, circulo3d, cuerpo_revolucion, nrm, rot_eje

R = 1.83                    # radio del cuerpo (m)
Z_S2 = 41.3                 # salida de la tobera MVac dentro de la interetapa
Z_DRAGON = 60.5             # base del tronco de la Dragon
ALTO_S1 = 47.5


def _marco(base, eje, ref):
    a = nrm(eje)
    u, v = base_de(a, ref)
    return np.asarray(base, np.float64), a, u, v


def _px(lz, base, esc, largo):
    return lz.cam.escala(base) * largo * esc


def etapa1(lz, base, eje, esc=0.001, aletas=0.0, patas=0.0, op=1.0, ref=(0, 0, 1), rot=0.0, motores=True, w=1.2):
    """Primera etapa. aletas 0..1 = aletas de rejilla plegadas -> desplegadas; patas 0..1 = patas plegadas -> abiertas."""
    b, a, u, v = _marco(base, eje, ref)
    tam = _px(lz, b, esc, ALTO_S1)
    if tam < 30:                                           # muy lejos: una raya
        lz.linea(np.array([b, b + a * ALTO_S1 * esc]), op, w * 1.4)
        return
    det = tam > 160
    perfil = [(1.3, 1.55), (1.9, R), (41.0, R), (47.5, R)]
    s = esc
    # patas (detrás del cuerpo se tapan con el relleno del cuerpo)
    if det:
        for k in range(4):
            ang = rot + math.pi / 4 + k * math.pi / 2
            d = math.cos(ang) * u + math.sin(ang) * v
            phi = math.radians(118) * patas
            hinge = b + (a * 1.6 + d * (R + 0.08)) * s
            L = 8.6
            dirp = math.cos(phi) * a + math.sin(phi) * d
            pie = hinge + dirp * L * s
            t = np.cross(a, d)
            anch = 0.45 * s
            lz.linea(np.array([hinge + t * anch, pie + t * anch * 0.5]), op, w * 0.9)
            lz.linea(np.array([hinge - t * anch, pie - t * anch * 0.5]), op, w * 0.9)
            if patas > 0.02:
                anc = b + (a * 7.0 + d * R) * s                    # pistón hasta media pata
                lz.linea(np.array([anc, hinge + dirp * L * 0.55 * s]), op * 0.7, w * 0.7)
                lz.linea(circulo3d(pie, a, 0.7 * s, 16, ref=ref), op * 0.8, w * 0.8, cerrada=True)
    cuerpo_revolucion(lz, b, a, [(z * s, r * s) for z, r in perfil], anillos=[x * s for x in (1.9, 14.0, 41.0, 44.2, 47.5)],
                      op=op, w=w, gen=10 if det else 0, rot=rot, ref=ref)
    # interetapa: banda rayada (en el real es negra)
    if det:
        for k in range(16):
            ang = rot + 2 * math.pi * k / 16
            d = math.cos(ang) * u + math.sin(ang) * v
            p0, p1 = b + (a * 41.0 + d * R) * s, b + (a * 47.5 + d * R) * s
            vis = (lz.cam.pos - (p0 + p1) / 2) @ d > 0
            if vis:
                lz.linea(np.array([p0, p1]), op * 0.45, w * 0.7)
    # aletas de rejilla
    if det:
        for k in range(4):
            ang = rot + k * math.pi / 2
            d = math.cos(ang) * u + math.sin(ang) * v
            t = np.cross(a, d)
            hinge = b + (a * 46.9 + d * (R + 0.05)) * s
            phi = math.radians(90) * aletas
            ex = (math.cos(phi) * (-a) + math.sin(phi) * d)        # sale del gozne
            fondo = (lz.cam.pos - hinge) @ d < 0 and aletas < 0.3
            o = op * (0.35 if fondo else 1.0)
            Lg, Wg = 1.5 * s, 0.62 * s
            c = [hinge - t * Wg, hinge + t * Wg, hinge + t * Wg + ex * Lg, hinge - t * Wg + ex * Lg]
            lz.linea(np.array(c), o, w * 0.8, cerrada=True)
            for j in range(1, 4):
                f = j / 4
                lz.linea(np.array([hinge - t * Wg + ex * Lg * f, hinge + t * Wg + ex * Lg * f]), o * 0.6, w * 0.6)
                lz.linea(np.array([hinge + t * Wg * (2 * f - 1), hinge + t * Wg * (2 * f - 1) + ex * Lg]), o * 0.6, w * 0.6)
    # motores: 1 al centro + 8 en anillo
    if motores and det:
        for k in range(9):
            if k == 0:
                c = b
            else:
                ang = rot + 2 * math.pi * (k - 1) / 8
                c = b + (math.cos(ang) * u + math.sin(ang) * v) * 1.22 * s
            cuerpo_revolucion(lz, c, a, [(0, 0.46 * s), (1.35 * s, 0.2 * s)], anillos=[0, 1.35 * s], op=op * 0.85, w=w * 0.75,
                              gen=0, ref=ref, rellenar=True)


def salidas_motores(base, eje, esc=0.001, ref=(0, 0, 1), rot=0.0, cuales=range(9)):
    b, a, u, v = _marco(base, eje, ref)
    out = []
    for k in cuales:
        if k == 0:
            out.append(b)
        else:
            ang = rot + 2 * math.pi * (k - 1) / 8
            out.append(b + (math.cos(ang) * u + math.sin(ang) * v) * 1.22 * esc)
    return out


def etapa2(lz, base, eje, esc=0.001, op=1.0, ref=(0, 0, 1), rot=0.0, w=1.2):
    """Segunda etapa; `base` = salida de la tobera MVac."""
    b, a, u, v = _marco(base, eje, ref)
    tam = _px(lz, b, esc, 19.2)
    s = esc
    if tam < 25:
        lz.linea(np.array([b, b + a * 19.2 * s]), op, w * 1.4)
        return
    cuerpo_revolucion(lz, b, a, [(0, 1.5 * s), (2.2 * s, 0.75 * s), (3.3 * s, 0.42 * s), (3.4 * s, 0.7 * s), (6.0 * s, 0.9 * s)],
                      anillos=[0, 1.1 * s, 2.2 * s, 3.3 * s], op=op * 0.9, w=w * 0.85, gen=8, rot=rot, ref=ref)
    cuerpo_revolucion(lz, b + a * 6.2 * s, a, [(0, R * s), (13.0 * s, R * s)], anillos=[0, 6.5 * s, 13.0 * s], op=op, w=w,
                      gen=10, rot=rot, ref=ref)


def dragon(lz, base, eje, esc=0.001, op=1.0, ref=(0, 0, 1), rot=0.0, morro=0.0, tronco=True, w=1.2):
    """Dragon de carga: tronco (4,4 m) + cápsula; morro 0..1 = cerrado -> abierto (gira sobre su gozne)."""
    b, a, u, v = _marco(base, eje, ref)
    s = esc
    if _px(lz, b, esc, 8.8) < 20:
        lz.linea(np.array([b, b + a * 8.8 * s]), op, w * 1.4)
        return
    if tronco:
        cuerpo_revolucion(lz, b, a, [(0, R * s), (4.4 * s, R * s)], anillos=[0, 2.2 * s, 4.4 * s], op=op, w=w, gen=12, rot=rot,
                          ref=ref)
    c0 = b + a * 4.4 * s
    cuerpo_revolucion(lz, c0, a, [(0, 1.95 * s), (0.35 * s, 2.0 * s), (3.4 * s, 1.18 * s), (3.55 * s, 1.0 * s)],
                      anillos=[0, 0.35 * s, 1.6 * s, 3.4 * s], op=op, w=w, gen=12, rot=rot, ref=ref)
    # ventanillas (marcas) y morro con gozne
    gozne = c0 + a * 3.55 * s + u * 1.0 * s
    Rm = rot_eje(np.cross(a, u), -math.radians(105) * morro)
    perfil = [(0, 1.0), (0.35, 0.9), (0.6, 0.6), (0.75, 0.0)]
    centro = c0 + a * 3.55 * s
    pts_izq, pts_der = [], []
    for z, r in perfil:
        anillo = circulo3d(centro + a * z * s, a, r * s, 40, ref=ref) if r > 0 else (centro + a * z * s)[None]
        anillo = (anillo - gozne) @ Rm.T + gozne
        if r > 0:
            lz.linea(anillo, op * 0.9, w * 0.8, cerrada=True)
    for ang in np.linspace(0, 2 * math.pi, 8, endpoint=False):
        d = math.cos(ang + rot) * u + math.sin(ang + rot) * v
        P = np.array([centro + (a * z + d * r) * s for z, r in perfil])
        P = (P - gozne) @ Rm.T + gozne
        lz.linea(P, op * 0.5, w * 0.6)


def estacion(lz, centro, ejes, esc=0.001, op=1.0, w=1.0, ref=(0, 0, 1)):
    """Estación Espacial esquemática: armazón de 109 m, 8 alas de paneles y módulos presurizados. ejes = (x armazón, y módulos)."""
    c = np.asarray(centro, np.float64)
    x, y = nrm(ejes[0]), nrm(ejes[1])
    z = np.cross(x, y)
    s = esc
    # módulos (cilindros a lo largo de y)
    cuerpo_revolucion(lz, c - y * 22 * s, y, [(0, 2.1 * s), (52 * s, 2.1 * s)], anillos=[k * s for k in (0, 10, 20, 32, 42, 52)],
                      op=op, w=w, gen=0, ref=x)
    cuerpo_revolucion(lz, c - x * 9 * s + y * 4 * s, x, [(0, 2.1 * s), (18 * s, 2.1 * s)], anillos=[0, 9 * s, 18 * s],
                      op=op * 0.9, w=w, gen=0, ref=y)
    # armazón
    for k in (-1, 1):
        lz.linea(np.array([c - x * 54 * s + z * 1.5 * k * s, c + x * 54 * s + z * 1.5 * k * s]), op, w)
    for xx in np.linspace(-54, 54, 13):
        lz.linea(np.array([c + x * xx * s - z * 1.5 * s, c + x * xx * s + z * 1.5 * s]), op * 0.6, w * 0.7)
    # paneles: 4 grupos (2 alas cada uno) en los extremos
    for xx in (-46, -37, 37, 46):
        for k in (-1, 1):
            p0 = c + x * xx * s + y * 2 * k * s
            p1 = p0 + y * 34 * k * s
            e = x * 5.8 * s
            lz.relleno(np.array([p0 - e, p0 + e, p1 + e, p1 - e]), 0.0)
            lz.linea(np.array([p0 - e, p0 + e, p1 + e, p1 - e]), op, w * 0.9, cerrada=True)
            for f in np.linspace(0, 1, 7)[1:-1]:
                q = p0 + (p1 - p0) * f
                lz.linea(np.array([q - e, q + e]), op * 0.45, w * 0.6)
            lz.linea(np.array([p0, p1]), op * 0.45, w * 0.6)
    # radiadores
    for xx in (-14, 14):
        p0 = c + x * xx * s
        lz.linea(np.array([p0, p0 - z * 15 * s, p0 - z * 15 * s + x * 4 * s, p0 + x * 4 * s]), op * 0.7, w * 0.8)


def torre(lz, base, arriba, lado, esc=0.001, alto=80.0, ancho=5.0, op=0.7, w=0.9):
    """Torre de servicio de celosía; `lado` = dirección horizontal en la que está respecto al cohete."""
    b = np.asarray(base, np.float64)
    U, L = nrm(arriba), nrm(lado)
    T = np.cross(U, L)
    s = esc
    esq = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
    P = [b + (L * i + T * j) * ancho / 2 * s for i, j in esq]
    for p in P:
        lz.linea(np.array([p, p + U * alto * s]), op, w)
    paso = 6.0
    for k in range(int(alto / paso)):
        z0, z1 = k * paso, (k + 1) * paso
        anillo = [p + U * z1 * s for p in P]
        lz.linea(np.array(anillo), op * 0.8, w * 0.8, cerrada=True)
        for i in range(4):
            lz.linea(np.array([P[i] + U * z0 * s, P[(i + 1) % 4] + U * z1 * s]), op * 0.45, w * 0.6)
    # brazo de acceso hacia el cohete (a 2/3 de altura) y el de arriba
    for zz in (alto * 0.66, alto * 0.9):
        p = b + U * zz * s
        lz.linea(np.array([p - L * ancho / 2 * s, p - L * (ancho / 2 + 6.5) * s]), op, w)
        lz.linea(np.array([p - L * ancho / 2 * s + U * 2.4 * s, p - L * (ancho / 2 + 6.5) * s + U * 2.4 * s]), op * 0.7, w * 0.8)


def zona_aterrizaje(lz, centro, arriba, esc=0.001, op=0.8, w=1.0, r=43.0):
    """Plataforma circular de aterrizaje (LZ-1) con anillos y cruz."""
    c = np.asarray(centro, np.float64)
    U = nrm(arriba)
    for k, rr in enumerate((r, r * 0.62)):
        lz.linea(circulo3d(c, U, rr * esc, 96), op * (1.0 if k == 0 else 0.6), w, cerrada=True)
    u, v = base_de(U)
    for d in (u, v):
        lz.linea(np.array([c - d * r * 0.5 * esc, c + d * r * 0.5 * esc]), op * 0.55, w * 0.8)
