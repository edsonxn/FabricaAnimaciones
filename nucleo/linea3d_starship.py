# -*- coding: utf-8 -*-
"""Modelos de alambre de Starship para el kit LÍNEA 3D (14-nov-2026): Super Heavy Block 3 (33 Raptor en 3 anillos, 3 aletas
de rejilla grandes, anillo de hot staging, pernos de captura), nave Starship (3 Raptor de nivel del mar + 3 RVac, 4 flaps,
escudo térmico en el lado de barlovento), pila completa, torre de captura con «palillos» (chopsticks) y mesa de lanzamiento.

Medidas en METROS, esquemáticas (proporciones de Block 3: diámetro 9 m, Super Heavy ~72,3 m, pila ~124,4 m; space.com
«How SpaceX's new Starship V3 differs», 3 aletas de rejilla 50 % más grandes). `esc` = unidades de mundo por metro.
`eje` = hacia dónde apunta la nariz; `ref` fija el giro alrededor del eje (el escudo térmico mira hacia `u` de base_de(eje, ref)).

Pila (z desde la salida de las toberas del Super Heavy): booster 0-72,3 (anillo de hot staging 69,3-72,3) · nave 72,3-124,4.
"""
import math

import numpy as np

from linea3d import base_de, circulo3d, cuerpo_revolucion, nrm

R = 4.5                     # radio del cuerpo (m)
ALTO_SH = 72.3
ALTO_NAVE = 52.1
Z_NAVE = ALTO_SH            # la nave se apoya sobre el anillo de hot staging
Z_PERNOS_SH = 64.5          # pernos de captura del booster (donde lo toman los palillos)
Z_PERNOS_NAVE = 41.5        # pernos de captura de la nave (bajo los flaps delanteros)

# 33 motores del Super Heavy: 3 centrales (vectorizan), 10 en el anillo interior, 20 en el exterior (fijos)
ANILLOS_SH = ((3, 1.05, 0.62, 0.0), (10, 2.45, 0.6, 0.3), (20, 3.85, 0.56, 0.0))   # (n, radio, radio de tobera, desfase)


def _marco(base, eje, ref):
    a = nrm(eje)
    u, v = base_de(a, ref)
    return np.asarray(base, np.float64), a, u, v


def _px(lz, base, esc, largo):
    return lz.cam.escala(base) * largo * esc


def motores_sh():
    """Lista [(anillo, x, y, r_tobera)] de los 33 motores en el plano de las toberas (metros)."""
    out = []
    for k, (n, rr, rt, des) in enumerate(ANILLOS_SH):
        for i in range(n):
            ang = 2 * math.pi * (i + des) / n
            out.append((k, rr * math.cos(ang), rr * math.sin(ang), rt))
    return out


def salidas_sh(base, eje, esc=1.0, ref=(0, 0, 1), rot=0.0, cuales=None):
    b, a, u, v = _marco(base, eje, ref)
    cr, sr = math.cos(rot), math.sin(rot)
    out = []
    for i, (k, x, y, rt) in enumerate(motores_sh()):
        if cuales is not None and i not in cuales:
            continue
        xx, yy = x * cr - y * sr, x * sr + y * cr
        out.append(b + (u * xx + v * yy) * esc)
    return out


def _tobera(lz, c, a, rt, largo, op, w, ref, gen=0):
    cuerpo_revolucion(lz, c, a, [(0, rt), (largo * 0.75, rt * 0.55), (largo, rt * 0.42)], anillos=[0, largo], op=op, w=w,
                      gen=gen, ref=ref, rellenar=True)


def _aleta_rejilla(lz, hinge, a, d, t, L, Wd, ang, op, w, celdas=5):
    """Aleta de rejilla: placa que sale del gozne; ang 0 = pegada hacia arriba, 1 = desplegada horizontal."""
    phi = math.radians(90) * ang
    ex = math.cos(phi) * a + math.sin(phi) * d
    c = [hinge - t * Wd, hinge + t * Wd, hinge + t * Wd + ex * L, hinge - t * Wd + ex * L]
    lz.relleno(np.array(c), 0.0)
    lz.linea(np.array(c), op, w * 0.85, cerrada=True)
    for j in range(1, celdas):
        f = j / celdas
        lz.linea(np.array([hinge - t * Wd + ex * L * f, hinge + t * Wd + ex * L * f]), op * 0.55, w * 0.55)
        lz.linea(np.array([hinge + t * Wd * (2 * f - 1), hinge + t * Wd * (2 * f - 1) + ex * L]), op * 0.55, w * 0.55)


def super_heavy(lz, base, eje, esc=1.0, aletas=1.0, op=1.0, ref=(0, 0, 1), rot=0.0, motores=True, w=1.2, pernos=True,
                anillo_hs=True):
    """Super Heavy Block 3. `base` = plano de salida de las toberas. aletas 0..1 (en V3 van fijas: 1)."""
    b, a, u, v = _marco(base, eje, ref)
    s = esc
    tam = _px(lz, b, esc, ALTO_SH)
    if tam < 30:
        lz.linea(np.array([b, b + a * ALTO_SH * s]), op, w * 1.4)
        return
    det = tam > 180
    # faldón y cuerpo
    perfil = [(1.6, R * 0.93), (3.2, R), (ALTO_SH - (3.0 if anillo_hs else 0.0), R)]
    cuerpo_revolucion(lz, b, a, [(z * s, r * s) for z, r in perfil],
                      anillos=[x * s for x in (3.2, 20.0, 33.0, 46.0, 59.0)] if det else None,
                      op=op, w=w, gen=12 if det else 0, rot=rot, ref=ref)
    # anillo de hot staging (rejilla de respiraderos)
    if anillo_hs:
        z0, z1 = ALTO_SH - 3.0, ALTO_SH
        cuerpo_revolucion(lz, b + a * z0 * s, a, [(0, R * s), (3.0 * s, R * s)], anillos=[0, 3.0 * s], op=op, w=w * 0.9,
                          gen=0, rot=rot, ref=ref)
        if det:
            for k in range(28):
                ang = rot + 2 * math.pi * k / 28
                d = math.cos(ang) * u + math.sin(ang) * v
                p0, p1 = b + (a * (z0 + 0.4) + d * R) * s, b + (a * (z1 - 0.4) + d * R) * s
                if (lz.cam.pos - (p0 + p1) / 2) @ d > 0:
                    lz.linea(np.array([p0, p1]), op * 0.5, w * 0.6)
    # chines (carenados laterales de cables) en dos lados
    if det:
        for ang in (rot + math.pi * 0.5, rot + math.pi * 1.5):
            d = math.cos(ang) * u + math.sin(ang) * v
            P = np.array([b + (a * z + d * (R + 0.35)) * s for z in (6.0, ALTO_SH - 6.0)])
            if (lz.cam.pos - P.mean(0)) @ d > 0:
                lz.linea(P, op * 0.6, w * 0.8)
    # aletas de rejilla: 3, grandes (V3)
    for k in range(3):
        ang = rot + math.pi / 6 + k * 2 * math.pi / 3
        d = math.cos(ang) * u + math.sin(ang) * v
        t = np.cross(a, d)
        hinge = b + (a * (ALTO_SH - 5.5) + d * (R + 0.1)) * s
        detras = (lz.cam.pos - hinge) @ d < 0
        _aleta_rejilla(lz, hinge, -a, d, t, 4.6 * s, 1.9 * s, aletas, op * (0.4 if detras else 1.0), w,
                       celdas=6 if det else 3)
    # pernos de captura (dos, a los lados donde llegan los palillos)
    if pernos and det:
        for ang in (rot, rot + math.pi):
            d = math.cos(ang) * u + math.sin(ang) * v
            p = b + (a * Z_PERNOS_SH + d * R) * s
            if (lz.cam.pos - p) @ d > 0:
                lz.linea(np.array([p, p + d * 1.4 * s]), op, w * 1.6)
                lz.linea(np.array([p + d * 1.4 * s - a * 0.5 * s, p + d * 1.4 * s + a * 0.5 * s]), op, w * 1.3)
    # 33 motores
    if motores and tam > 260:
        for c in salidas_sh(b, a, esc, ref, rot):
            _tobera(lz, c, a, 0.58 * s, 2.6 * s, op * 0.8, w * 0.6, ref)


def nave(lz, base, eje, esc=1.0, op=1.0, ref=(0, 0, 1), rot=0.0, flaps=0.0, flaps_del=None, escudo=True, motores=True, w=1.2,
         pernos=True):
    """Nave Starship. `base` = plano de salida de las toberas. flaps 0..1 = plegados -> abiertos 90° (flaps_del = delanteros,
    por defecto igual). El escudo térmico (losetas) mira hacia +u (barlovento en la reentrada)."""
    b, a, u, v = _marco(base, eje, ref)
    s = esc
    tam = _px(lz, b, esc, ALTO_NAVE)
    if tam < 25:
        lz.linea(np.array([b, b + a * ALTO_NAVE * s]), op, w * 1.4)
        return
    det = tam > 160
    fd = flaps if flaps_del is None else flaps_del
    nariz = [(36.0, R), (40.0, R * 0.96), (44.0, R * 0.82), (47.5, R * 0.6), (50.3, R * 0.32), (51.6, R * 0.12), (ALTO_NAVE, 0.0)]
    perfil = [(0.8, R * 0.95), (2.0, R), (30.0, R)] + nariz
    cuerpo_revolucion(lz, b, a, [(z * s, r * s) for z, r in perfil],
                      anillos=[x * s for x in (2.0, 14.0, 26.0, 36.0, 44.0)] if det else None,
                      op=op, w=w, gen=12 if det else 0, rot=rot, ref=ref)
    cu, su = math.cos(rot), math.sin(rot)
    uu = cu * u + su * v                                   # lado del escudo térmico
    vv = -su * u + cu * v
    # escudo térmico: losetas (rejilla en la mitad de barlovento, solo si se ve)
    if escudo and det:
        zs_esc = np.linspace(3.0, 47.0, 23)
        for k in np.linspace(-1, 1, 13):
            ang = k * math.pi / 2 * 0.98
            d = math.cos(ang) * uu + math.sin(ang) * vv
            P = np.array([b + (a * z + d * float(np.interp(z, [p[0] for p in perfil], [p[1] for p in perfil]))) * s
                          for z in zs_esc])
            frente = np.array([(lz.cam.pos - p) @ d for p in P]) > 0
            lz.linea(P, np.where(frente, op * 0.3, 0.0), w * 0.5)
        for z in zs_esc[::2]:
            r = float(np.interp(z, [p[0] for p in perfil], [p[1] for p in perfil]))
            angs = np.linspace(-math.pi / 2, math.pi / 2, 40)
            P = np.array([b + (a * z + (math.cos(t) * uu + math.sin(t) * vv) * r) * s for t in angs])
            frente = np.array([(lz.cam.pos - p) @ (math.cos(t) * uu + math.sin(t) * vv) for p, t in zip(P, angs)]) > 0
            lz.linea(P, np.where(frente, op * 0.3, 0.0), w * 0.5)
    # flaps: traseros (grandes) y delanteros (chicos), a ±90° del escudo; gozne a lo largo del eje
    for lado in (1, -1):
        d = vv * lado                                     # radial hacia el costado
        tng = uu * -1.0                                   # plegado: hacia sotavento (pegado al cuerpo)
        for (z0, z1, an0, an1, ff) in ((4.0, 17.0, 6.2, 4.2, flaps), (39.0, 46.5, 4.0, 2.2, fd)):
            phi = math.radians(90) * ff
            ex = math.cos(phi) * tng + math.sin(phi) * d
            r0 = float(np.interp(z0, [p[0] for p in perfil], [p[1] for p in perfil]))
            r1 = float(np.interp(z1, [p[0] for p in perfil], [p[1] for p in perfil]))
            h0 = b + (a * z0 + d * r0) * s
            h1 = b + (a * z1 + d * r1) * s
            P = np.array([h0, h1, h1 + ex * an1 * s, h0 + ex * an0 * s])
            detras = (lz.cam.pos - (h0 + h1) / 2) @ (ex + d) < 0 and ff < 0.2
            lz.relleno(P, 0.0)
            lz.linea(P, op * (0.4 if detras else 1.0), w * 0.9, cerrada=True)
            if det:
                lz.linea(np.array([(P[0] + P[3]) / 2, (P[1] + P[2]) / 2]), op * 0.35, w * 0.6)
    # pernos de captura
    if pernos and det:
        for lado in (1, -1):
            d = vv * lado
            p = b + (a * Z_PERNOS_NAVE + d * R) * s
            if (lz.cam.pos - p) @ d > 0:
                lz.linea(np.array([p, p + d * 1.1 * s]), op, w * 1.5)
    # 6 motores: 3 de nivel del mar al centro + 3 RVac (toberas grandes) por fuera
    if motores and tam > 220:
        for i in range(3):
            ang = rot + 2 * math.pi * i / 3
            c = b + (math.cos(ang) * u + math.sin(ang) * v) * 1.15 * s + a * 0.6 * s
            _tobera(lz, c, a, 0.6 * s, 2.4 * s, op * 0.8, w * 0.6, ref)
            ang2 = ang + math.pi / 3
            c2 = b + (math.cos(ang2) * u + math.sin(ang2) * v) * 3.05 * s
            _tobera(lz, c2, a, 1.2 * s, 3.4 * s, op * 0.85, w * 0.7, ref, gen=6 if det else 0)


def salidas_nave(base, eje, esc=1.0, ref=(0, 0, 1), rot=0.0, cuales=range(6)):
    """0-2 nivel del mar (centro), 3-5 RVac."""
    b, a, u, v = _marco(base, eje, ref)
    out = []
    for i in cuales:
        if i < 3:
            ang = rot + 2 * math.pi * i / 3
            out.append(b + (math.cos(ang) * u + math.sin(ang) * v) * 1.15 * esc + a * 0.6 * esc)
        else:
            ang = rot + 2 * math.pi * (i - 3) / 3 + math.pi / 3
            out.append(b + (math.cos(ang) * u + math.sin(ang) * v) * 3.05 * esc)
    return out


def pila(lz, base, eje, esc=1.0, op=1.0, ref=(0, 0, 1), rot=0.0, w=1.2, motores=True):
    a = nrm(eje)
    super_heavy(lz, base, a, esc, 1.0, op, ref, rot, motores, w)
    nave(lz, np.asarray(base, np.float64) + a * Z_NAVE * esc, a, esc, op, ref, rot, 0.0, None, True, False, w)


def mesa_lanzamiento(lz, centro, arriba, esc=1.0, alto=20.0, op=0.8, w=1.0, ref=(0, 0, 1)):
    """Mesa de lanzamiento: anillo a `alto` m sobre patas, foso de llamas debajo. `centro` = punto del suelo."""
    c = np.asarray(centro, np.float64)
    U = nrm(arriba)
    u, v = base_de(U, ref)
    s = esc
    top = c + U * alto * s
    for rr in (R + 1.2, R + 4.5):
        lz.linea(circulo3d(top, U, rr * s, 72, ref=ref), op, w, cerrada=True)
    lz.linea(circulo3d(top - U * 2.0 * s, U, (R + 4.5) * s, 72, ref=ref), op * 0.6, w * 0.8, cerrada=True)
    for k in range(6):
        ang = 2 * math.pi * k / 6 + math.pi / 6
        d = math.cos(ang) * u + math.sin(ang) * v
        p_top = top + d * (R + 4.5) * s
        p_pie = c + d * (R + 8.0) * s
        lz.linea(np.array([p_top - U * 2.0 * s, p_pie]), op, w)
        lz.linea(np.array([p_top, p_top - U * 2.0 * s]), op * 0.8, w * 0.8)
    # foso de llamas
    for rr, o in ((R + 9.0, 0.5), (R + 14.0, 0.3)):
        lz.linea(circulo3d(c, U, rr * s, 72, ref=ref), op * o, w * 0.8, cerrada=True)


def torre_captura(lz, base, arriba, frente, esc=1.0, alto=146.0, ancho=11.0, z_brazos=80.0, apertura=0.0, largo_brazo=36.0,
                  op=0.8, w=1.0, z_qd=None):
    """Torre de lanzamiento y captura con «palillos». `base` = pie de la torre, `frente` = dirección horizontal hacia el
    cohete. z_brazos = altura del carro de los brazos (m); apertura 0 = cerrados (pinza a 9 m), 1 = abiertos (~65°).
    Devuelve las puntas de los brazos (para anclar la cámara o el cohete)."""
    b = np.asarray(base, np.float64)
    U, F = nrm(arriba), nrm(frente)
    T = np.cross(U, F)
    s = esc
    h = ancho / 2
    esq = [b + (F * i + T * j) * h * s for i, j in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    for p in esq:
        lz.linea(np.array([p, p + U * alto * s]), op, w)
    paso = 9.0
    n = int(alto / paso)
    for k in range(n):
        z0, z1 = k * paso, (k + 1) * paso
        anillo = [p + U * z1 * s for p in esq]
        lz.linea(np.array(anillo), op * 0.75, w * 0.75, cerrada=True)
        for i in range(4):
            j = (i + 1) % 4
            if k % 2:
                lz.linea(np.array([esq[i] + U * z0 * s, esq[j] + U * z1 * s]), op * 0.4, w * 0.55)
            else:
                lz.linea(np.array([esq[j] + U * z0 * s, esq[i] + U * z1 * s]), op * 0.4, w * 0.55)
    # remate (grúa y pararrayos)
    topc = b + U * alto * s
    lz.linea(np.array([topc, topc + U * 14 * s]), op * 0.7, w * 0.8)
    lz.linea(np.array([topc + U * 9 * s - F * 3 * s, topc + U * 9 * s + F * 10 * s]), op * 0.55, w * 0.7)
    # carro de los brazos
    zc = z_brazos
    car = [p + U * zc * s for p in esq]
    for dz in (-4.0, 4.0):
        lz.linea(np.array([p + U * dz * s for p in car]), op, w * 1.1, cerrada=True)
    # brazos: pivotan en las esquinas delanteras, se abren en el plano horizontal
    puntas = []
    ab = math.radians(65) * apertura
    sep = R + 0.6                                         # medio hueco entre brazos cerrados (deja pasar 9 m)
    for lado in (1, -1):
        piv = b + (F * h + T * lado * h) * s + U * zc * s
        # dirección del brazo: cerrado = paralelo a F con desfase lateral hacia el centro; abierto gira hacia fuera
        dir_c = nrm(F * largo_brazo + T * (-lado) * (h - sep))
        ang = ab * lado
        dir_ = nrm(dir_c * math.cos(ang) + np.cross(U, dir_c) * math.sin(ang))
        tip = piv + dir_ * largo_brazo * s
        puntas.append(tip)
        lado_n = nrm(np.cross(U, dir_))
        for dz in (-2.2, 2.2):
            lz.linea(np.array([piv + U * dz * s, tip + U * dz * s * 0.6]), op, w * 1.1)
        for f in np.linspace(0, 1, 9)[:-1]:
            p0 = piv + dir_ * largo_brazo * f * s
            p1 = piv + dir_ * largo_brazo * (f + 1 / 8) * s
            lz.linea(np.array([p0 - U * 2.2 * s * (1 - 0.4 * f), p1 + U * 2.2 * s * (1 - 0.4 * (f + 1 / 8))]), op * 0.45, w * 0.55)
        # riel superior donde se apoyan los pernos
        lz.linea(np.array([piv + U * 2.6 * s + lado_n * 0.4 * s * lado, tip + U * 1.6 * s]), op * 0.6, w * 0.7)
    # brazo de conexión rápida (QD) de la nave
    if z_qd:
        p = b + F * h * s + U * z_qd * s
        lz.linea(np.array([p, p + F * 12 * s]), op * 0.8, w)
        lz.linea(np.array([p + U * 3 * s, p + F * 12 * s + U * 3 * s]), op * 0.6, w * 0.8)
    return puntas
