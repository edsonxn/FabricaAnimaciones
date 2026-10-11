# -*- coding: utf-8 -*-
"""Objetos del video 'El viaje de una semilla' (estilo boceto). Todos son `Dib` en coordenadas locales."""
import math
from functools import lru_cache

import numpy as np

import boceto as B
from boceto import (AMARILLO, AZUL, AZUL_CL, AZUL_OSC, BLANCO, GRIS, GRIS_CL, HIELO, MARRON, NARANJA, PIEL, R, ROJO,
                    ROSA, T, TINTA, VERDE, VERDE_OSC, Dib, arco_, circ, curva, elip, linea, mano_poli, ondas)

# ------------------------------------------------------------------ La Semilla Mascota (Plumita)
def _perfil_semilla():
    """Contorno de una semilla de diente de león: fusiforme, acanalada, con punta abajo y cuello arriba."""
    pts = [
        (0.0, -32.0),     # cuello superior
        (20.0, -18.0),
        (28.0, 18.0),     # cuerpo más ancho y expresivo
        (24.0, 58.0),
        (14.0, 95.0),
        (0.0, 120.0),     # punta inferior
        (-14.0, 95.0),
        (-24.0, 58.0),
        (-28.0, 18.0),
        (-20.0, -18.0),
        (0.0, -32.0)
    ]
    return curva(pts, 8, cerrado=True)


CUERPO_SEMILLA = _perfil_semilla()


@lru_cache(maxsize=None)
def semilla(ojos="abiertos", boca="sonrisa", paracaidas="abierto", mejillas=True, brazos=False, mira=0):
    """Mascota protagonista: semilla con carita tierna y paracaídas plumoso (vilano)."""
    ops = []
    # 1. Contorno y relleno de la semilla (el primer trazo T es el contorno principal para morfosis)
    ops.append(T(CUERPO_SEMILLA, 5.5, peso=0.4))
    ops.append(R(CUERPO_SEMILLA, MARRON, peso=0.35, sp=8, ang=-45, off=(3, -3)))

    # Ranuras longitudinales de la semilla (textura botánica real de Taraxacum)
    c1 = curva([(0, -28), (-10, 15), (-7, 68), (0, 115)], 6)
    c2 = curva([(0, -28), (10, 15), (7, 68), (0, 115)], 6)
    ops.append(T(c1, 3.5, peso=0.06, v=180))
    ops.append(T(c2, 3.5, peso=0.06, v=180))

    # 2. Rostro expresivo
    ex = 12
    ox = 5 * mira
    yo = 20
    if ojos == "abiertos":
        ops += [T(linea((-ex + ox, yo - 8), (-ex + ox, yo + 8)), 9, peso=0.03),
                T(linea((ex + ox, yo - 8), (ex + ox, yo + 8)), 9, peso=0.03)]
    elif ojos == "feliz":
        ops += [T(arco_(-ex + ox, yo + 6, 9, 200, 340, 8), 5.0, peso=0.04),
                T(arco_(ex + ox, yo + 6, 9, 200, 340, 8), 5.0, peso=0.04)]
    elif ojos == "cerrados":
        ops += [T(arco_(-ex + ox, yo, 9, 20, 160, 8), 4.5, peso=0.04),
                T(arco_(ex + ox, yo, 9, 20, 160, 8), 4.5, peso=0.04)]
    elif ojos == "miedo":
        ops += [T(circ(-ex + ox, yo, 9, n=14), 4.5, peso=0.05),
                T(circ(ex + ox, yo, 9, n=14), 4.5, peso=0.05),
                T(linea((-ex + ox, yo - 2), (-ex + ox, yo + 3)), 6, peso=0.02),
                T(linea((ex + ox, yo - 2), (ex + ox, yo + 3)), 6, peso=0.02)]
    elif ojos == "dormido":
        ops += [T(linea((-ex + ox - 7, yo + 1), (-ex + ox + 7, yo + 1)), 4.5, peso=0.03),
                T(linea((ex + ox - 7, yo + 1), (ex + ox + 7, yo + 1)), 4.5, peso=0.03)]

    # Boquita
    yb = 42
    if boca == "sonrisa":
        ops.append(T(arco_(ox, yb, 14, 25, 155, 10), 4.8, peso=0.05))
    elif boca == "o":
        ops.append(T(circ(ox, yb + 2, 7, n=14), 4.5, peso=0.04))
    elif boca == "temblor":
        ops.append(T(linea((-14 + ox, yb + 4), (-7 + ox, yb - 3), (0 + ox, yb + 5), (7 + ox, yb - 3), (14 + ox, yb + 4)), 4.2, peso=0.05))
    elif boca == "abierta":
        ops += [T(arco_(ox, yb - 2, 14, 10, 170, 12), 4.8, peso=0.05),
                R(arco_(ox, yb - 2, 14, 10, 170, 12), ROSA, peso=0.04, sp=4)]
    elif boca == "ronca":
        ops.append(T(elip(ox, yb + 4, 8, 5, n=12), 4.0, peso=0.04))

    # Mejillas rosadas
    if mejillas:
        ops += [R(elip(-28, 30, 9, 6, n=14), ROSA, peso=0.03, sp=4, off=(1, -1)),
                R(elip(28, 30, 9, 6, n=14), ROSA, peso=0.03, sp=4, off=(1, -1))]

    # Bracitos
    if brazos == "saludo":
        ops.append(T(curva([(22, 24), (40, 6), (54, -16), (46, -30)], 6), 4.5, peso=0.05))
    elif brazos == "agarrar":
        ops += [T(curva([(-20, 24), (-30, -5), (-14, -45), (-2, -55)], 6), 4.5, peso=0.04),
                T(curva([(20, 24), (30, -5), (14, -45), (2, -55)], 6), 4.5, peso=0.04)]

    # 3. Pedicelo (el tallo que sube al paracaídas)
    y_nudo = -140.0
    ped = linea((0.0, -32.0), (0.0, y_nudo))
    ops.append(T(ped, 4.5, peso=0.15))

    # 4. Paracaídas / Vilano (pappus)
    if paracaidas == "abierto":
        # Sombrilla abierta y curvada hacia arriba con 20 radios plumosos
        n_radios = 20
        for i in range(n_radios):
            ang_deg = -162 + (144.0 * i) / (n_radios - 1)
            ang = math.radians(ang_deg)
            L = 120.0 + 16.0 * math.sin(i * 1.7)
            c_pt = (0.5 * L * math.cos(ang), y_nudo + 0.4 * L * math.sin(ang) - 10)
            e_pt = (L * math.cos(ang), y_nudo + L * math.sin(ang))
            radio = curva([(0.0, y_nudo), c_pt, e_pt], 6)
            ops.append(T(radio, 3.4, peso=0.03, v=220))
            for sg in (-1, 1):
                an_sub = ang + sg * 0.45
                ops.append(T(linea(e_pt, (e_pt[0] + 20 * math.cos(an_sub), e_pt[1] + 20 * math.sin(an_sub))), 2.4, peso=0.01, v=190))
        disco = circ(0.0, y_nudo - 45, 105, vuelta=1.0, n=28, ry=50)
        ops.append(R(disco, BLANCO, peso=0.3, sp=14, ang=30))
    elif paracaidas == "plegado":
        # Radios plegados hacia arriba (picada veloz en tormenta)
        for i in range(14):
            ang = math.radians(-105 + (30.0 * i) / 13)
            L = 130.0 + 10.0 * (i % 3)
            ops.append(T(linea((0.0, y_nudo), (L * math.cos(ang), y_nudo + L * math.sin(ang))), 3.6, peso=0.03, v=220))
    elif paracaidas == "pequeno":
        for i in range(12):
            ang = math.radians(-150 + (120.0 * i) / 11)
            L = 65.0
            ops.append(T(linea((0.0, y_nudo), (L * math.cos(ang), y_nudo + L * math.sin(ang))), 3.2, peso=0.03, v=200))

    return Dib(ops)


# ------------------------------------------------------------------ Pompón de Diente de León Maduro (C0)
def _contorno_pompon_base():
    """Tallo y receptáculo del pompón."""
    tallo = np.array([(-14, 40), (-10, 420), (10, 420), (14, 40)], float)
    return tallo


@lru_cache(maxsize=None)
def pompon_maduro():
    """Gran flor madura de diente de león antes de dispersarse: tallo verde, cúpula y esfera de vilanos."""
    r_globo = 210.0
    globo = circ(0, 20, r_globo, vuelta=1.02, n=48)
    ops = [
        # Primer T: contorno principal emparejado para morfosis
        T(globo, 5.0, peso=0.5, v=180),
        R(globo, BLANCO, peso=0.8, sp=14, ang=45),
        R(globo, (228, 242, 252), peso=0.4, sp=22, ang=-45)
    ]
    # Tallo verde principal
    tallo = _contorno_pompon_base()
    ops.append(T(tallo, 6.0, peso=0.6))
    ops.append(R(tallo, VERDE, peso=0.5, sp=10, ang=80))

    # Brácteas/sépalos curvados hacia abajo bajo el receptáculo
    for lado in (-1, 1):
        for k in range(4):
            x0 = lado * (4 + k * 8)
            b = curva([(x0, 36), (lado * (22 + k * 12), 55 + k * 6), (lado * (32 + k * 14), 85 + k * 8)], 6)
            ops.append(T(b, 4.5, peso=0.05))
            ops.append(R(np.vstack([b, [(x0, 50)], b[:1]]), VERDE_OSC, peso=0.04, sp=6))

    # Receptáculo central (botón carnoso marrón claro / crema)
    rec = elip(0, 32, 44, 22, n=24)
    ops.append(T(rec, 5.0, peso=0.3))
    ops.append(R(rec, (210, 195, 160), peso=0.3, sp=8))

    # Esfera de vilanos: decenas de radios radiales con plumitas en la punta
    n_radios = 32
    for i in range(n_radios):
        a = -math.pi + (2 * math.pi * i) / n_radios
        x0, y0 = 32 * math.cos(a), 28 + 16 * math.sin(a)
        x1, y1 = r_globo * math.cos(a), 20 + r_globo * math.sin(a)
        ops.append(T(linea((x0, y0), (x1, y1)), 3.0, peso=0.03, v=200))
        for sg in (-1, 1):
            aa = a + sg * 0.5
            ops.append(T(linea((x1, y1), (x1 + 14 * math.cos(aa), y1 + 14 * math.sin(aa))), 2.2, peso=0.01, v=180))

    return Dib(ops)


def pompon_din(t):
    """Pompón con vida: los filamentos ondean sutilmente con la brisa periódica."""
    w = B.OMEGA
    base_dib = pompon_maduro()
    return base_dib


# ------------------------------------------------------------------ Mariposa Voladora (Acompañante de vuelo)
@lru_cache(maxsize=None)
def mariposa(aleteo=0.0):
    """Mariposa colorida con alas articuladas (aleteo controla la proyección horizontal de las alas)."""
    ops = []
    cos_al = max(0.18, math.cos(aleteo))

    # Alas superiores (naranja y amarillo)
    ala_sup_izq = curva([(0, -10), (-60 * cos_al, -75), (-110 * cos_al, -50), (-85 * cos_al, 0), (0, 0)], 8, cerrado=True)
    ala_sup_der = curva([(0, -10), (60 * cos_al, -75), (110 * cos_al, -50), (85 * cos_al, 0), (0, 0)], 8, cerrado=True)
    ops.append(T(ala_sup_izq, 4.8, peso=0.25))
    ops.append(R(ala_sup_izq, NARANJA, peso=0.2, sp=8, ang=-30))
    ops.append(T(ala_sup_der, 4.8, peso=0.25))
    ops.append(R(ala_sup_der, NARANJA, peso=0.2, sp=8, ang=30))

    # Detalles interiores de alas superiores
    mancha_izq = elip(-55 * cos_al, -45, 22 * cos_al, 14, rot=-0.4, n=16)
    mancha_der = elip(55 * cos_al, -45, 22 * cos_al, 14, rot=0.4, n=16)
    ops.append(R(mancha_izq, AMARILLO, peso=0.1, sp=6))
    ops.append(R(mancha_der, AMARILLO, peso=0.1, sp=6))

    # Alas inferiores (más redondeadas)
    ala_inf_izq = curva([(0, 0), (-75 * cos_al, 15), (-60 * cos_al, 65), (-20 * cos_al, 55), (0, 10)], 8, cerrado=True)
    ala_inf_der = curva([(0, 0), (75 * cos_al, 15), (60 * cos_al, 65), (20 * cos_al, 55), (0, 10)], 8, cerrado=True)
    ops.append(T(ala_inf_izq, 4.2, peso=0.2))
    ops.append(R(ala_inf_izq, (230, 95, 60), peso=0.15, sp=8, ang=-60))
    ops.append(T(ala_inf_der, 4.2, peso=0.2))
    ops.append(R(ala_inf_der, (230, 95, 60), peso=0.15, sp=8, ang=60))

    # Cuerpo central (tórax y abdomen oscuro)
    cuerpo = elip(0, 12, 9, 32, n=20)
    cabeza = circ(0, -22, 10, n=14)
    ops.append(T(cuerpo, 5.0, peso=0.15))
    ops.append(R(cuerpo, (50, 42, 40), peso=0.15, sp=6))
    ops.append(T(cabeza, 4.5, peso=0.1))
    ops.append(R(cabeza, (50, 42, 40), peso=0.1, sp=5))

    # Rayitas del abdomen
    for y in (-2, 8, 18, 28):
        ops.append(T(linea((-6, y), (6, y)), 3.2, peso=0.02, v=230))

    # Antenitas curvas
    ant_izq = curva([(0, -28), (-12, -48), (-24, -56)], 6)
    ant_der = curva([(0, -28), (12, -48), (24, -56)], 6)
    ops.append(T(ant_izq, 3.5, peso=0.04))
    ops.append(T(ant_der, 3.5, peso=0.04))
    ops.append(T(circ(-25, -58, 3, n=8), 3.0, peso=0.01))
    ops.append(T(circ(25, -58, 3, n=8), 3.0, peso=0.01))

    return Dib(ops)


# ------------------------------------------------------------------ Paisaje Aéreo (Colinas, Casas, Techos)
@lru_cache(maxsize=None)
def paisaje_colinas():
    """Paisaje de colinas verdes y lejanas para la escena de vuelo."""
    # Colina trasera
    c1 = ondas(-540, 540, 120, 35, 420)
    p1 = np.vstack([[(-540, 350)], c1, [(540, 350)]])
    # Colina delantera
    c2 = ondas(-540, 540, 220, 25, 300, ph=1.5)
    p2 = np.vstack([[(-540, 450)], c2, [(540, 450)]])

    ops = [
        T(c1, 5.0, peso=0.4),
        R(p1, (160, 204, 150), peso=0.5, sp=14, ang=25),
        T(c2, 5.5, peso=0.5),
        R(p2, VERDE, peso=0.6, sp=12, ang=-20)
    ]
    # Pequeños arbolitos redondos en las lomas
    for (ax, ay, ar) in [(-320, 95, 26), (-120, 85, 34), (220, 110, 28), (380, 200, 36)]:
        copa = circ(ax, ay, ar, n=24)
        ops.append(T(linea((ax, ay + ar), (ax, ay + ar + 22)), 4.5, peso=0.04))
        ops.append(T(copa, 4.2, peso=0.1))
        ops.append(R(copa, VERDE_OSC, peso=0.1, sp=6))

    return Dib(ops)


@lru_cache(maxsize=None)
def casa_aldea():
    """Casita con techo de tejas rojas y chimenea para la vista aérea."""
    fachada = np.array([(-90, -30), (90, -30), (90, 80), (-90, 80), (-90, -30)], float)
    techo = np.array([(-115, -30), (0, -115), (115, -30), (-115, -30)], float)
    chimenea = np.array([(45, -95), (45, -135), (75, -135), (75, -60)], float)
    puerta = np.array([(-22, 80), (-22, 25), (22, 25), (22, 80)], float)
    ventana = np.array([(40, 0), (75, 0), (75, 35), (40, 35), (40, 0)], float)

    ops = [
        T(fachada, 5.5, peso=0.4),
        R(fachada, (244, 236, 218), peso=0.4, sp=9),
        T(techo, 6.0, peso=0.4),
        R(techo, ROJO, peso=0.5, sp=8, ang=-45),
        T(chimenea, 4.5, peso=0.15),
        R(chimenea, MARRON, peso=0.1, sp=6),
        T(puerta, 4.5, peso=0.1),
        R(puerta, MARRON, peso=0.1, sp=6),
        T(ventana, 4.0, peso=0.1),
        R(ventana, AZUL_CL, peso=0.08, sp=5),
        T(linea((57, 0), (57, 35)), 3.2, peso=0.02),
        T(linea((40, 17), (75, 17)), 3.2, peso=0.02)
    ]
    return Dib(ops)


# ------------------------------------------------------------------ Tormenta (Nubes oscuras, Rayo, Gotas)
@lru_cache(maxsize=None)
def nube_tormenta():
    """Gran nube de tormenta gris oscura e imponente."""
    circulos = [(-220, 20, 95, 75), (-110, -45, 115, -15), (35, -65, 130, -15), (185, -10, 105, 45), (275, 45, 65, 75)]
    pts, _ = B.union_circulos(circulos, 110, (20, 20))
    th = np.arctan2(-(pts[:, 1] - 20), pts[:, 0] - 20)
    th = np.where(th < -math.pi / 2, th + 2 * math.pi, th)
    pts = pts[np.argsort(th)]
    xs = np.linspace(pts[-1, 0], pts[0, 0], 28)
    base_l = np.stack([xs, 110 + 6 * np.sin(xs / 50)], 1)
    contorno = np.vstack([pts, base_l, pts[:1]])

    detalles = [arco_(-150, 15, 45, 190, 300, 10), arco_(15, -20, 60, 200, 310, 10), arco_(205, 25, 40, 190, 300, 10)]

    ops = [
        T(contorno, 6.5, peso=1.0),
        R(contorno, GRIS, peso=0.9, sp=10, ang=35),
        R(contorno, AZUL_OSC, peso=0.6, sp=18, ang=-35)
    ]
    for d in detalles:
        ops.append(T(d, 4.0, peso=0.08))

    return Dib(ops)


@lru_cache(maxsize=None)
def rayo():
    """Rayo eléctrico zigzagueante de tormenta."""
    pts = [(-20, -180), (35, -70), (-15, -20), (45, 70), (-5, 90), (30, 190)]
    ancho_pts = []
    for i in range(len(pts) - 1):
        ancho_pts.append(pts[i])
        ancho_pts.append((pts[i][0] + 12, pts[i][1] + 5))
    poly = np.array([(-20, -180), (35, -70), (-15, -20), (45, 70), (30, 190), (10, 85), (-30, 20), (15, -60), (-20, -180)], float)

    ops = [
        T(poly, 5.0, peso=0.35),
        R(poly, AMARILLO, peso=0.3, sp=6),
        T(curva(pts, 4), 3.5, peso=0.2, v=240)
    ]
    return Dib(ops)


@lru_cache(maxsize=None)
def gota_gigante():
    """Gota de lluvia pesada que cae como un meteorito contra la semilla."""
    tip = (0.0, -90.0)
    C = (0.0, 25.0)
    r = 50.0
    d = C[1] - tip[1]
    phi = math.degrees(math.acos(r / d))
    arc = arco_(C[0], C[1], r, -90 + phi, 270 - phi, 32)
    poly = np.vstack([[tip], arc, [tip]])

    brillo = arco_(-18, 15, 26, 120, 220, 8)

    return Dib([
        T(poly, 6.0, peso=0.6),
        R(poly, AZUL_OSC, peso=0.5, sp=9, ang=60),
        R(poly, AZUL, peso=0.4, sp=14, ang=-30),
        T(brillo, 3.8, peso=0.08, v=150)
    ])


# ------------------------------------------------------------------ Grieta y Suelo de Piedra
@lru_cache(maxsize=None)
def suelo_grieta():
    """Grandes adoquines de piedra con una profunda grieta en V donde caerá la semilla."""
    # Adoquín izquierdo
    izq = mano_poli(np.array([(-540, -120), (-60, -120), (-25, -20), (-80, 80), (-35, 200), (-15, 380), (-540, 380)]), 3.5, seed=7)
    # Adoquín derecho
    der = mano_poli(np.array([(540, -120), (60, -120), (25, -20), (80, 80), (35, 200), (15, 380), (540, 380)]), 3.5, seed=11)

    # Grieta oscura central
    grieta_poly = np.vstack([
        [(-60, -120), (-25, -20), (-80, 80), (-35, 200), (-15, 380)],
        [(15, 380), (35, 200), (80, 80), (25, -20), (60, -120)]
    ])

    ops = [
        # Piedra izquierda
        T(izq, 6.0, peso=0.8),
        R(izq, (185, 185, 192), peso=0.7, sp=12, ang=-45),
        # Piedra derecha
        T(der, 6.0, peso=0.8),
        R(der, (170, 172, 180), peso=0.7, sp=12, ang=45),
        # Fondo oscuro de la grieta
        T(grieta_poly, 5.0, peso=0.5),
        R(grieta_poly, (80, 75, 75), peso=0.6, sp=8, ang=85)
    ]
    # Grietas secundarias y textura de piedra (hatching)
    ops.append(T(linea((-240, -120), (-200, -30), (-270, 40)), 3.8, peso=0.08))
    ops.append(T(linea((210, -120), (260, -20), (220, 60)), 3.8, peso=0.08))
    ops.append(T(linea((-35, 200), (35, 200)), 4.0, peso=0.05))

    return Dib(ops)


@lru_cache(maxsize=None)
def bufanda():
    """Bufandita de lana roja para la semilla que inverna."""
    cuello = curva([(-28, -8), (-12, 12), (12, 12), (28, -8)], 6)
    cola = curva([(12, 12), (18, 45), (14, 80)], 6)
    flecos = [linea((14, 80), (10, 95)), linea((14, 80), (14, 98)), linea((14, 80), (18, 95))]

    poly_c = np.vstack([cuello, [(24, 6), (10, 24), (-10, 24), (-24, 6)]])
    poly_col = np.array([(8, 12), (24, 12), (20, 80), (8, 80)], float)

    ops = [
        T(poly_c, 5.0, peso=0.2),
        R(poly_c, ROJO, peso=0.2, sp=6),
        T(poly_col, 5.0, peso=0.2),
        R(poly_col, ROJO, peso=0.2, sp=6)
    ]
    for f in flecos:
        ops.append(T(f, 3.5, peso=0.03))

    return Dib(ops)


@lru_cache(maxsize=None)
def copo_nieve(r=55):
    """Copo de nieve hexagonal para el invierno."""
    ops = []
    for i in range(6):
        a = i * math.pi / 3
        c, s = math.cos(a), math.sin(a)
        ops.append(T(linea((0, 0), (r * c, r * s)), 4.2, peso=0.08))
        # Ramificaciones del copo
        for f, l in ((0.5, 0.35), (0.78, 0.22)):
            bx, by = r * f * c, r * f * s
            for sg in (-1, 1):
                aa = a + sg * 0.75
                ops.append(T(linea((bx, by), (bx + r * l * math.cos(aa), by + r * l * math.sin(aa))), 3.2, peso=0.04))
    return Dib(ops)


# ------------------------------------------------------------------ Despertar, Raíces y Brote Verde
@lru_cache(maxsize=None)
def raices():
    """Sistema de raíces fuertes que rompen la piedra y se ramifican bajo el suelo."""
    ops = []
    # Raíz principal pivotante (gruesa en el arranque)
    p_ppal = curva([(0, 0), (15, 60), (-12, 140), (8, 240), (-4, 340), (0, 430)], 10)
    ops.append(T(p_ppal, 6.0, peso=0.5))

    # Raíces laterales secundarias
    r1 = curva([(10, 50), (65, 90), (120, 150), (160, 230)], 8)
    r2 = curva([(-8, 90), (-70, 140), (-130, 200), (-175, 290)], 8)
    r3 = curva([(5, 170), (55, 230), (95, 320)], 8)
    r4 = curva([(-5, 210), (-60, 270), (-110, 360)], 8)
    r5 = curva([(2, 280), (35, 340), (50, 420)], 8)

    for r in (r1, r2, r3, r4, r5):
        ops.append(T(r, 4.5, peso=0.15))

    # Pequeños pelos radiculares
    for k, (px, py, ang) in enumerate([(45, 75, 0.8), (95, 120, 0.5), (-45, 120, -0.6), (-100, 170, -0.8), (30, 200, 0.7)]):
        ops.append(T(linea((px, py), (px + 22 * math.cos(ang), py + 22 * math.sin(ang))), 3.0, peso=0.02))

    return Dib(ops)


@lru_cache(maxsize=None)
def brote_verde():
    """Brote verde elástico que surge de la semilla: tallo y dos hojitas cotiledones redondeadas."""
    tallo = curva([(0, 80), (-8, 40), (4, 0), (0, -40)], 8)

    # Hoja cotiledón izquierda
    hoja_izq = curva([(0, -40), (-35, -55), (-60, -45), (-65, -30), (-40, -25), (0, -35)], 6, cerrado=True)
    # Hoja cotiledón derecha
    hoja_der = curva([(0, -40), (35, -55), (60, -45), (65, -30), (40, -25), (0, -35)], 6, cerrado=True)

    ops = [
        T(tallo, 6.0, peso=0.3),
        T(hoja_izq, 4.8, peso=0.2),
        R(hoja_izq, VERDE, peso=0.2, sp=7),
        T(hoja_der, 4.8, peso=0.2),
        R(hoja_der, VERDE, peso=0.2, sp=7),
        # Nervaduras de las hojitas
        T(linea((0, -35), (-45, -38)), 3.0, peso=0.03),
        T(linea((0, -35), (45, -38)), 3.0, peso=0.03)
    ]
    return Dib(ops)


# ------------------------------------------------------------------ Flor de Diente de León
@lru_cache(maxsize=None)
def hoja_diente_leon():
    """Hoja basal aserrada clásica con 'dientes de león' triangulares."""
    # Lóbulo apical y lóbulos laterales que apuntan hacia atrás
    pts_izq = [(0, -220), (-25, -180), (-12, -170), (-45, -125), (-18, -115), (-55, -60), (-22, -50), (-45, 10), (-16, 20), (0, 70)]
    pts_der = [(0, 70), (16, 20), (45, 10), (22, -50), (55, -60), (18, -115), (45, -125), (12, -170), (25, -180), (0, -220)]
    poly = np.array(pts_izq + pts_der, float)
    nerv = linea((0, -210), (0, 65))

    return Dib([
        T(poly, 5.5, peso=0.7),
        R(poly, VERDE_OSC, peso=0.6, sp=10, ang=75),
        T(nerv, 4.0, peso=0.15)
    ])


@lru_cache(maxsize=None)
def flor_amarilla(apertura=1.0):
    """Flor dorada radiante de diente de león: capas de pétalos en corona circular."""
    r_ext = max(10.0, 165.0 * apertura)
    corona_ext = circ(0, 0, r_ext, vuelta=1.02, n=48)
    ops = [
        # Primer T: contorno principal circular emparejado con el pompón
        T(corona_ext, 5.5, peso=0.5),
        R(corona_ext, AMARILLO, peso=0.7, sp=10, ang=45)
    ]
    # Tallo verde abajo
    tallo = np.array([(-12, 35), (-10, 320), (10, 320), (12, 35)], float)
    ops.append(T(tallo, 6.0, peso=0.5))
    ops.append(R(tallo, VERDE, peso=0.4, sp=9, ang=85))

    # Receptáculo y brácteas verdes
    rec = elip(0, 35, 48, 22, n=24)
    ops.append(T(rec, 5.0, peso=0.25))
    ops.append(R(rec, VERDE_OSC, peso=0.2, sp=7))

    # Capas de pétalos dorados (ligulados con puntas dentadas)
    # Capa 1: exterior (24 pétalos)
    n1 = 24
    r_ext = 165.0 * apertura
    r_int = 45.0
    for i in range(n1):
        a = (2 * math.pi * i) / n1
        c, s = math.cos(a), math.sin(a)
        # Cada pétalo es una tira fina
        w_pet = 14.0 * apertura
        tang = np.array([-s, c])
        p0 = np.array([r_int * c, r_int * s])
        p1 = np.array([r_ext * c, r_ext * s])
        p_pet = np.array([p0 - tang * (w_pet * 0.5), p1 - tang * (w_pet * 0.7), p1 + tang * (w_pet * 0.7), p0 + tang * (w_pet * 0.5)], float)
        ops.append(T(p_pet, 3.8, peso=0.03))
        ops.append(R(p_pet, AMARILLO, peso=0.03, sp=5))

    # Capa 2: intermedia (18 pétalos más cortos)
    n2 = 18
    r_med = 115.0 * apertura
    for i in range(n2):
        a = (2 * math.pi * i) / n2 + 0.15
        c, s = math.cos(a), math.sin(a)
        w_pet = 12.0 * apertura
        tang = np.array([-s, c])
        p0 = np.array([(r_int - 10) * c, (r_int - 10) * s])
        p1 = np.array([r_med * c, r_med * s])
        p_pet = np.array([p0 - tang * (w_pet * 0.5), p1 - tang * (w_pet * 0.6), p1 + tang * (w_pet * 0.6), p0 + tang * (w_pet * 0.5)], float)
        ops.append(T(p_pet, 3.5, peso=0.02))
        ops.append(R(p_pet, NARANJA, peso=0.02, sp=5))

    # Centro floral (botón denso naranja / dorado)
    centro = circ(0, 0, max(12, int(42 * apertura)), n=28)
    ops.append(T(centro, 5.0, peso=0.3))
    ops.append(R(centro, (245, 175, 45), peso=0.3, sp=7))

    return Dib(ops)


# ------------------------------------------------------------------ Abeja Polinizadora
@lru_cache(maxsize=None)
def abeja(aleteo=0.0):
    """Abejita simpática y regordeta que visita la flor."""
    ops = []
    # Alas vibrantes
    cos_w = max(0.2, math.cos(aleteo * 2.5))
    ala_izq = elip(-18 * cos_w, -35, 16 * cos_w, 32, rot=-0.4, n=16)
    ala_der = elip(18 * cos_w, -35, 16 * cos_w, 32, rot=0.4, n=16)
    ops.append(T(ala_izq, 4.0, peso=0.15))
    ops.append(R(ala_izq, (230, 245, 255), peso=0.1, sp=6))
    ops.append(T(ala_der, 4.0, peso=0.15))
    ops.append(R(ala_der, (230, 245, 255), peso=0.1, sp=6))

    # Cuerpo redondeado a rayas
    cuerpo = elip(0, 0, 36, 28, n=24)
    ops.append(T(cuerpo, 5.5, peso=0.3))
    ops.append(R(cuerpo, AMARILLO, peso=0.25, sp=7))

    # Franjas negras
    f1 = np.array([(-15, -26), (0, -28), (0, 28), (-15, 26)], float)
    f2 = np.array([(10, -26), (25, -20), (25, 20), (10, 26)], float)
    ops.append(R(f1, TINTA, peso=0.1, sp=5))
    ops.append(R(f2, TINTA, peso=0.1, sp=5))

    # Ojito tierno y sonrisa
    ops.append(T(circ(-18, -6, 5, n=10), 4.0, peso=0.04))
    ops.append(T(arco_(-24, 6, 7, 20, 160, 6), 3.5, peso=0.03))

    # Antenitas
    ops.append(T(curva([(-28, -15), (-42, -28), (-38, -36)], 6), 3.2, peso=0.03))
    ops.append(T(curva([(-24, -18), (-34, -34), (-28, -42)], 6), 3.2, peso=0.03))

    return Dib(ops)


# ------------------------------------------------------------------ Brisa y Viento Dinámico
@lru_cache(maxsize=None)
def espiral_viento():
    """Línea de viento con espiral en el extremo."""
    th = np.linspace(0, 3.5 * math.pi, 36)
    r = 5.0 + 8.0 * th
    xs = r * np.cos(th)
    ys = r * np.sin(th)
    cola_x = np.linspace(-300, xs[0], 24)
    cola_y = 12 * np.sin(cola_x / 40)
    P = np.vstack([np.stack([cola_x, cola_y], 1), np.stack([xs, ys], 1)])
    return Dib([T(P, 4.5, peso=0.6)])


@lru_cache(maxsize=None)
def chispa_polen():
    """Motitas doradas de polen flotando."""
    ops = []
    for a, l in ((0, 24), (math.pi / 2, 24), (math.pi / 4, 15), (3 * math.pi / 4, 15)):
        ops.append(T(linea((-l * math.cos(a), -l * math.sin(a)), (l * math.cos(a), l * math.sin(a))), 3.8, peso=0.05))
    return Dib(ops)


@lru_cache(maxsize=None)
def planeta_mini(r=75):
    """Pequeño globo terráqueo giratorio con continentes."""
    circ_p = circ(0, 0, r, vuelta=1.03, n=40)
    c1 = curva([(-35, -25), (-12, -45), (15, -20), (-5, 10), (-30, 5)], 6, cerrado=True)
    c2 = curva([(15, 12), (45, 5), (55, 35), (35, 55), (10, 40)], 6, cerrado=True)
    ops = [
        T(circ_p, 5.5, peso=0.4),
        R(circ(0, 0, r, vuelta=1.0, n=36), AZUL, peso=0.5, sp=9),
        T(c1, 3.8, peso=0.15),
        R(c1, VERDE, peso=0.15, sp=6),
        T(c2, 3.8, peso=0.15),
        R(c2, VERDE, peso=0.15, sp=6)
    ]
    return Dib(ops)


@lru_cache(maxsize=None)
def termometro_frio():
    """Termómetro de vidrio con mercurio azul bajo cero y rayitas de frío."""
    tubo = np.array([(-14, -120), (14, -120), (14, 50), (-14, 50)], float)
    bulbo = circ(0, 80, 36, vuelta=1.02, n=28)
    merc_tubo = np.array([(-8, -20), (8, -20), (8, 55), (-8, 55)], float)
    merc_bulbo = circ(0, 80, 28, vuelta=1.0, n=24)

    ops = [
        T(bulbo, 5.0, peso=0.3),
        T(tubo, 5.0, peso=0.3),
        R(merc_bulbo, AZUL_OSC, peso=0.3, sp=6),
        T(merc_tubo, 4.0, peso=0.1),
        R(merc_tubo, AZUL_OSC, peso=0.2, sp=5)
    ]
    # Marcas de temperatura y copito de nieve
    for y in (-90, -60, -30, 0, 30):
        ops.append(T(linea((14, y), (26, y)), 3.2, peso=0.02))
    # Líneas de tiritar brrr
    ops.append(T(curva([(-35, -40), (-45, -30), (-35, -20)], 4), 3.2, peso=0.03))
    ops.append(T(curva([(35, 40), (45, 50), (35, 60)], 4), 3.2, peso=0.03))
    return Dib(ops)


@lru_cache(maxsize=None)
def rayos_sol():
    """Ráfaga de rayos solares cálidos descendiendo diagonalmente desde el cielo."""
    ops = []
    for k in range(5):
        x = -250 + k * 130
        p0 = (x, -220)
        p1 = (x + 180, 220)
        ops.append(T(linea(p0, p1), 4.5, peso=0.12, v=200))
    return Dib(ops)


@lru_cache(maxsize=None)
def hierba_base():
    """Mancha de césped y hierba fresca al pie de la planta."""
    ops = []
    suelo = ondas(-240, 240, 0, 6, 80)
    ops.append(T(suelo, 4.5, peso=0.3))
    for k in range(9):
        x = -200 + k * 48
        h = 24 + 14 * math.sin(k * 1.6)
        inclin = 10 * math.sin(k * 2.1)
        ops.append(T(curva([(x, 0), (x + inclin * 0.5, -h * 0.6), (x + inclin, -h)], 5), 4.0, peso=0.05))
    return Dib(ops)


@lru_cache(maxsize=None)
def pajaros_lejanos():
    """Siluetas de aves volando en formación lejana."""
    ops = []
    for (px, py, sc) in [(-60, -20, 1.0), (0, 0, 1.2), (70, -35, 0.9)]:
        ala = curva([(px - 22 * sc, py + 8 * sc), (px - 10 * sc, py - 12 * sc), (px, py), (px + 10 * sc, py - 12 * sc), (px + 22 * sc, py + 8 * sc)], 6)
        ops.append(T(ala, 4.0 * sc, peso=0.1))
    return Dib(ops)
