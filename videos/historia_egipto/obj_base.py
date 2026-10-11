# -*- coding: utf-8 -*-
"""Piezas comunes de dibujo (boceto) para «La historia de Egipto en 5 minutos»:
geometría, paleta egipcia auténtica y generador de personajes dinásticos y epocales.

Convenciones: coordenadas locales (x derecha, y abajo), origen en los PIES del personaje
(la cabeza queda en y ≈ -215). Todo devuelve `Dib` (tinta T y crayón R).
"""
import math
from functools import lru_cache

import numpy as np

import boceto as B
from boceto import (AMARILLO, AZUL, AZUL_CL, AZUL_OSC, BLANCO, GRIS, GRIS_CL, MARRON, NARANJA, PIEL, R, ROJO, ROSA, T, VERDE,
                    VERDE_OSC, Dib, arco_, circ, curva, elip, linea, mano_poli, ondas)

# Paleta egipcia tradicional (pigmentos minerales sobre papiro y piedra caliza)
ORO = (238, 188, 56)
ORO_OSC = (196, 142, 38)
AZUL_EGIPTO = (45, 82, 155)      # Azul lapislázuli / azul egipcio
CELESTE_NILO = (130, 185, 225)
TURQUESA = (64, 168, 172)        # Malaquita / turquesa del Sinaí
ROJO_EGIPTO = (195, 62, 50)      # Ocre rojo / jaspe
ROJO_OSC = (145, 42, 36)
BLANCO_LINO = (248, 244, 232)    # Lino blanco plisado
NEGRO_KOHL = (44, 40, 46)        # Kohl / galena negra
PIEL_EGIPCIA = (212, 136, 92)    # Ocre cálido de frescos tebanos
PIEL_CL = (242, 202, 168)        # Tono claro (reinas, escribas, griegos)
VERDE_PAPIRO = (118, 172, 108)   # Tallo de papiro fresco
ARENA = (228, 206, 164)          # Arena del desierto líbico
ARENA_OSC = (196, 170, 128)
CALIZA = (242, 236, 220)         # Piedra caliza blanca de Tura
GRANITO = (174, 126, 118)        # Granito rosa de Asuán
BRONCE = (180, 138, 72)
MADERA = (168, 114, 74)
MADERA_OSC = (118, 76, 50)


# ------------------------------------------------------------------ atajos de geometría
def cerrar(P):
    P = np.asarray(P, float)
    return np.vstack([P, P[:1]])


def pol(*pts):
    return np.asarray(pts, float)


def rect(x0, y0, x1, y1, r=8.0, n=5):
    """Rectángulo con esquinas redondeadas."""
    r = min(r, (x1 - x0) / 2, (y1 - y0) / 2)
    P = []
    for cx, cy, a0 in ((x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):
        P += list(arco_(cx, cy, r, a0, a0 + 90, n))
    return cerrar(P)


def trap(xa0, xa1, ya, xb0, xb1, yb):
    """Trapecio: arriba [xa0, xa1] en ya, abajo [xb0, xb1] en yb."""
    return cerrar([(xa0, ya), (xa1, ya), (xb1, yb), (xb0, yb)])


def forma(P, color, w=5.0, peso=None, sp=10.0, ang=-55.0, tinta=True, cerrada=True):
    """Contorno de tinta + relleno de crayón."""
    P = cerrar(P) if cerrada else np.asarray(P, float)
    ops = []
    if tinta:
        ops.append(T(P, w, peso=peso))
    if color is not None:
        ops.append(R(P, color, peso=(peso * 0.7 if peso else None), sp=sp, ang=ang))
    return ops


def elipse(cx, cy, rx, ry, color, w=5.0, rot=0.0, peso=None, sp=9.0, tinta=True):
    P = elip(cx, cy, rx, ry, rot, 1.0, 36)
    return forma(P, color, w, peso, sp, tinta=tinta, cerrada=False)


def trazo(*pts, w=4.5, peso=0.05):
    return T(np.asarray(pts, float), w, peso=peso)


def rayita(x0, y0, x1, y1, w=4.0):
    return T(linea((x0, y0), (x1, y1)), w, peso=0.04)


def punto(x, y, w=11.0):
    return T(linea((x, y), (x + 0.6, y + 0.4)), w, peso=0.02)


def _rotar(P, rad, cx=0.0, cy=0.0):
    c, s = math.cos(rad), math.sin(rad)
    X, Y = P[:, 0] - cx, P[:, 1] - cy
    return np.stack([cx + c * X - s * Y, cy + s * X + c * Y], 1)


def colocar(ops, dx=0.0, dy=0.0, s=1.0, rot=0.0, flip=False):
    """Compone elementos gráficos escalando, rotando y trasladando."""
    out = []
    for op in ops:
        P = np.asarray(op[1], float) * (-s if flip else s, s)
        if rot:
            P = _rotar(P, rot, 0, 0)
        P = P + (dx, dy)
        out.append((op[0], P) + tuple(op[2:]))
    return out


# ------------------------------------------------------------------ tocados y coronas de Egipto
def corona_egipcia(tipo, cy=-215.0):
    """Devuelve las ops del tocado/corona para la cabeza centrada en (0, cy)."""
    ops = []
    if tipo == "hedjet":          # Corona Blanca del Alto Egipto (cónica / bulbo)
        P = [( -24, cy - 20), (-26, cy - 80), (-16, cy - 120), (0, cy - 138), (16, cy - 120), (26, cy - 80), (24, cy - 20)]
        ops += forma(P, BLANCO_LINO, 4.8, sp=7)
        ops += [T(linea((0, cy - 138), (0, cy - 146)), 4.0)]
        return ops

    if tipo == "deshret":         # Corona Roja del Bajo Egipto (plana con espiral frontal)
        P = [(-26, cy - 20), (-30, cy - 70), (28, cy - 70), (26, cy - 20)]
        ops += forma(P, ROJO_EGIPTO, 4.8, sp=7)
        # parte trasera levantada
        P_alta = [(20, cy - 70), (24, cy - 135), (32, cy - 135), (28, cy - 70)]
        ops += forma(P_alta, ROJO_EGIPTO, 4.5, sp=6)
        # espiral frontal hacia adelante
        ops += [trazo((-26, cy - 65), (-42, cy - 90), (-30, cy - 105), (-20, cy - 95), w=3.8)]
        return ops

    if tipo == "pschent":         # Doble Corona unificada (Blanca dentro de la Roja)
        ops += corona_egipcia("deshret", cy=cy)
        # Corona blanca insertada
        P_blanca = [(-16, cy - 60), (-18, cy - 110), (0, cy - 130), (14, cy - 110), (12, cy - 60)]
        ops += forma(P_blanca, BLANCO_LINO, 4.5, sp=6)
        return ops

    if tipo == "nemes":           # Tocado real a rayas azul y oro con ureaus
        # Paño que envuelve la cabeza y cae en dos alas
        P_cabeza = [(-38, cy - 15), (-34, cy - 65), (0, cy - 72), (34, cy - 65), (38, cy - 15)]
        ops += forma(P_cabeza, AZUL_EGIPTO, 4.8, sp=7)
        # Alas que caen a los lados de los hombros
        P_ala_izq = [(-36, cy - 15), (-46, cy + 35), (-26, cy + 38), (-24, cy - 10)]
        P_ala_der = [(36, cy - 15), (46, cy + 35), (26, cy + 38), (24, cy - 10)]
        ops += forma(P_ala_izq, ORO, 4.5, sp=6)
        ops += forma(P_ala_der, ORO, 4.5, sp=6)
        # Rayas de lino azul y oro
        for k in range(5):
            y_r = cy - 55 + 10 * k
            ops += [rayita(-32 + 2 * k, y_r, 32 - 2 * k, y_r, 3.2)]
        # Uraeus (cobra erguida en la frente)
        ops += [trazo((0, cy - 50), (-2, cy - 68), (4, cy - 72), (0, cy - 76), w=3.5)]
        ops += [R(circ(0, cy - 76, 4, n=8), ORO, peso=0.03, sp=3)]
        return ops

    if tipo == "khepresh":        # Casco o corona azul de guerra
        P = [(-34, cy - 20), (-32, cy - 75), (-12, cy - 90), (22, cy - 85), (34, cy - 55), (32, cy - 20)]
        ops += forma(P, AZUL_EGIPTO, 4.8, sp=7)
        # Discos dorados decorativos
        for px, py in ((-16, cy - 50), (0, cy - 60), (16, cy - 50), (-8, cy - 35), (10, cy - 35)):
            ops += [R(circ(px, py, 3.5, n=8), ORO, peso=0.02, sp=3)]
        ops += [trazo((-32, cy - 35), (-40, cy - 50), (-34, cy - 56), w=3.4)] # Uraeus
        return ops

    if tipo == "nefertiti":       # Tocado alto azul de Nefertiti
        P = [(-28, cy - 25), (-42, cy - 105), (42, cy - 105), (28, cy - 25)]
        ops += forma(P, AZUL_EGIPTO, 4.8, sp=7)
        # Cinta dorada frontal con joyel
        ops += forma(rect(-36, cy - 45, 36, cy - 35, 2), ORO, 4.0, sp=5)
        ops += [R(circ(0, cy - 40, 5, n=10), ROJO_EGIPTO, peso=0.03, sp=3)]
        return ops

    if tipo == "turbante":        # Turbante islámico medieval
        ops += forma(elip(0, cy - 35, 42, 28, 0, 1.0, 24), BLANCO_LINO, 4.8, sp=7)
        ops += forma(elip(0, cy - 50, 26, 20, 0, 1.0, 18), VERDE_OSC, 4.2, sp=6)
        return ops

    if tipo == "casco_romano":    # Casco de legionario con penacho
        P = [(-38, cy - 15), (-34, cy - 60), (0, cy - 68), (34, cy - 60), (38, cy - 15), (20, cy - 22), (-20, cy - 22)]
        ops += forma(P, BRONCE, 4.6, sp=7)
        # Cresta roja
        P_cresta = [(-10, cy - 68), (-8, cy - 95), (8, cy - 95), (10, cy - 68)]
        ops += forma(P_cresta, ROJO_EGIPTO, 4.2, sp=6)
        return ops

    if tipo == "casco_griego":    # Casco macedonio de Alejandro
        P = [(-36, cy - 18), (-30, cy - 70), (0, cy - 78), (30, cy - 70), (36, cy - 18), (14, cy - 28), (-14, cy - 28)]
        ops += forma(P, ORO, 4.8, sp=7)
        ops += forma(arco_(0, cy - 78, 22, 160, 380, 12), ROJO_EGIPTO, 4.2, sp=6)
        return ops

    # Pelo natural o peluca egipcia negra
    P_pelo = [(-36, cy - 10), (-32, cy - 60), (0, cy - 66), (32, cy - 60), (36, cy - 10)]
    ops += forma(P_pelo, NEGRO_KOHL, 4.5, sp=7)
    return ops


# ------------------------------------------------------------------ personaje egipcio
def personaje_egipcio(tipo="faraon", corona="nemes", piel=PIEL_EGIPCIA, falda_col=BLANCO_LINO,
                      pose="real", mirada=1.0, cetro=True, cara="serio"):
    """Construye un personaje egipcio con proporciones dinásticas y canon parietal.
    Origen (0, 0) en los pies. Cabeza en y ≈ -215.
    """
    ops = []
    cy = -215.0

    # 1. PIES Y PIERNAS (estilo perfil clásico: una pierna adelantada)
    # Pierna trasera
    ops += forma(rect(-22, -100, -8, 0, 4), piel, 4.5, sp=6)
    ops += forma(rect(-26, -10, 4, 0, 4), piel, 4.2, sp=5)
    # Pierna delantera adelantada hacia la mirada
    dx_pie = 18.0 * mirada
    ops += forma(rect(dx_pie - 8, -100, dx_pie + 8, 0, 4), piel, 4.5, sp=6)
    ops += forma(rect(dx_pie - 6, -10, dx_pie + 24 * (1.0 if mirada > 0 else -1.0), 0, 4), piel, 4.2, sp=5)

    # 2. FALDA / SHENDYT (falda de lino blanco con pliegues dorados)
    P_falda = trap(-30, 30, -115, -40, 40, -75)
    ops += forma(P_falda, falda_col, 5.0, sp=8)
    # Cinturón dorado real con hebilla
    ops += forma(rect(-32, -122, 32, -112, 3), ORO, 4.5, sp=6)
    if tipo in ("faraon", "reina"):
        # Colgante central del cinturón con rayas verticales
        ops += forma(trap(-10, 10, -112, -14, 14, -65), ORO, 4.0, sp=5)
        for y_r in (-100, -88, -76):
            ops += [rayita(-11, y_r, 11, y_r, 2.8)]

    # 3. TORSO (visto casi de frente como en el canon egipcio)
    P_torso = trap(-34, 34, -185, -24, 24, -118)
    ops += forma(P_torso, piel, 5.0, sp=8)

    # 4. COLLAR USEKH (collar ancho ceremonial de cuentas concéntricas)
    P_usekh = arco_(0, -185, 34, 0, 180, 16)
    ops += [T(P_usekh, 5.0, peso=0.08)]
    ops += [R(arco_(0, -185, 30, 10, 170, 14), ORO, peso=0.05, sp=5)]
    ops += [R(arco_(0, -185, 22, 15, 165, 12), TURQUESA, peso=0.04, sp=4)]
    ops += [R(arco_(0, -185, 14, 20, 160, 10), ROJO_EGIPTO, peso=0.03, sp=3)]

    # 5. BRAZOS Y MANOS
    if pose == "real":           # Un brazo doblado al pecho sosteniendo cayado/cetro, otro al costado
        # Brazo izquierdo caído con cayado o suelto
        ops += forma(pol((-32, -180), (-46, -130), (-34, -130), (-24, -178)), piel, 4.2, sp=5)
        # Brazo derecho cruzado al pecho
        ops += forma(pol((30, -180), (10, -145), (18, -135), (36, -175)), piel, 4.2, sp=5)
        # Manos
        ops += [R(circ(-40, -125, 7, n=10), piel, peso=0.02, sp=4), R(circ(12, -140, 7, n=10), piel, peso=0.02, sp=4)]
        if cetro:
            # Heka (cayado de pastor) y Nekhakha (flagelo) dorados
            ops += [trazo((14, -140), (14, -80), w=4.0)]
            ops += [T(arco_(14, -150, 10, -90, 120, 10), 3.8)]
            # Flagelo cruzado
            ops += [trazo((-38, -125), (-52, -90), w=3.8)]
            ops += [trazo((-52, -90), (-60, -75), w=3.2), trazo((-52, -90), (-54, -72), w=3.2)]
    elif pose == "ofrenda":      # Ambos brazos extendidos hacia adelante
        ops += forma(pol((-30, -180), (-10, -150), (25, -150), (25, -162), (-8, -162), (-24, -180)), piel, 4.2, sp=6)
        ops += [R(circ(28, -156, 7, n=10), piel, peso=0.02, sp=4)]
    else:                        # Guerrero con lanza o arco
        ops += forma(pol((-30, -180), (-55, -130), (-45, -130), (-22, -178)), piel, 4.2, sp=5)
        ops += forma(pol((30, -180), (55, -140), (45, -145), (24, -178)), piel, 4.2, sp=5)
        # Lanza larga
        ops += [trazo((55, -230), (55, 0), w=4.5)]
        # Punta de bronce
        ops += forma(pol((51, -230), (55, -255), (59, -230)), BRONCE, 3.8, sp=4)

    # 6. CUELLO Y CABEZA (en perfil)
    ops += forma(rect(-10, -200, 10, -180, 3), piel, 4.5, sp=5)
    ops += forma(elip(0, cy, 32, 34, 0, 1.0, 24), piel, 5.0, sp=7)

    # 7. RASGOS FACIALES EGIPCIOS
    ox = 8.0 * mirada
    if cara == "asombro":
        # Ojo de Horus bien abierto
        ops += [trazo((-4 + ox, cy - 8), (8 + ox, cy - 8), (14 + ox, cy - 4), w=3.6)]
        ops += [trazo((-4 + ox, cy + 2), (8 + ox, cy + 4), (14 + ox, cy), w=3.4)]
        ops += [T(circ(4 + ox, cy - 2, 6, n=12), 3.5, peso=0.03)]
        ops += [punto(4 + ox, cy - 2, w=4.5)]
        # Ceja levantada
        ops += [trazo((-6 + ox, cy - 18), (8 + ox, cy - 20), (16 + ox, cy - 14), w=3.6)]
        # Nariz recta
        ops += [trazo((24 * mirada, cy - 8), (32 * mirada, cy + 2), (24 * mirada, cy + 8), w=3.4)]
        # Boca abierta en O de asombro
        ops += [T(elip(22 * mirada, cy + 18, 5, 8, 0, 1.0, 12), 3.6, peso=0.03)]
    else:
        # Ojo almendrado con línea de kohl
        ops += [trazo((-4 + ox, cy - 4), (10 + ox, cy - 4), (16 + ox, cy - 2), w=3.6)]
        ops += [trazo((-4 + ox, cy - 4), (6 + ox, cy + 2), (12 + ox, cy - 2), w=3.2)]
        ops += [punto(4 + ox, cy - 3, w=6.0)] # Pupila
        # Ceja arqueada marcada
        ops += [trazo((-6 + ox, cy - 12), (8 + ox, cy - 14), (16 + ox, cy - 8), w=3.5)]
        # Perfil: nariz recta y boca serena
        ops += [trazo((24 * mirada, cy - 8), (32 * mirada, cy + 2), (24 * mirada, cy + 8), w=3.4)]
        ops += [trazo((20 * mirada, cy + 16), (28 * mirada, cy + 16), w=3.2)]

    # 8. BARBA DIVINA / POSTIZA (faraones)
    if tipo == "faraon":
        P_barba = trap(16 * mirada, 24 * mirada, cy + 24, 20 * mirada, 28 * mirada, cy + 60)
        ops += forma(P_barba, ORO, 3.8, sp=4)
        ops += [trazo((24 * mirada, cy + 60), (30 * mirada, cy + 56), w=3.2)] # Curva hacia afuera

    # 9. CORONA / TOCADO
    if corona:
        ops += corona_egipcia(corona, cy=cy)

    return Dib(ops)
