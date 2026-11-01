# -*- coding: utf-8 -*-
"""Dibujos de boceto para «La historia de Estados Unidos en 6 minutos» (1/3): tocados, sombreros, peinados, accesorios y PERSONAJES
de veinte mil años (de los cazadores de White Sands a Obama). Convenciones de obj_base: origen en los PIES, cabeza en y ≈ -215 (radio 41).
`pose` 0..3 = ciclo de paso. Un sombrero puede combinarse con otro con «+» («peluca_blanca+tricornio»)."""
import math
from functools import lru_cache

import numpy as np

import obj_base as OB
from obj_base import *  # noqa: F401,F403
from pal_us import *  # noqa: F401,F403

CONCHA = (240, 232, 214)
PLUMA_H = (132, 94, 62)          # pluma de halcón
WAMPUM_M = (112, 70, 120)        # wampum morado (conchas de almeja)
NEGRO_V = (40, 36, 40)           # pintura negra de la cerámica pueblo
ARMINIO = (246, 244, 240)
AMARILLO_SUF = (238, 200, 64)
VIOLETA = (142, 92, 158)
ROSA_V = (226, 108, 140)
MORADO_V = (122, 76, 148)
VISERA = (226, 176, 64)

_orig_sombrero = OB.sombrero


# ------------------------------------------------------------------ peinados y sombreros
def _pelo(col, cy):
    """Casquete de pelo que deja libres frente y ojos (igual en todos los peinados cortos)."""
    P = [(-42, cy - 4), (-45, cy - 30), (-30, cy - 47), (0, cy - 53), (30, cy - 47), (45, cy - 30), (42, cy - 4),
         (37, cy - 20), (20, cy - 28), (0, cy - 26), (-20, cy - 28), (-37, cy - 20)]
    return forma(P, col, 4.4, sp=7)


def _tricornio(cy, col=NEGRO_US, ribete=None, escarapela=None):
    ops = forma(rect(-34, cy - 86, 34, cy - 46, 10), col, 4.4, sp=7)
    P = [(-78, cy - 40), (-56, cy - 82), (-22, cy - 72), (0, cy - 76), (22, cy - 72), (56, cy - 82), (78, cy - 40), (40, cy - 38), (0, cy - 26), (-40, cy - 38)]
    ops += forma(P, col, 5.0, sp=8)
    if ribete:
        ops += [R(pol((-78, cy - 40), (-40, cy - 38), (0, cy - 26), (40, cy - 38), (78, cy - 40), (40, cy - 33), (0, cy - 21), (-40, cy - 33)), ribete,
                  peso=0.02, sp=3)]
    if escarapela:
        ops += forma(circ(-40, cy - 54, 9, n=12), escarapela, 3.2, sp=3)
    return ops


def _sombrero(nombre, cy=-215.0):
    if "+" in nombre:
        ops = []
        for n in nombre.split("+"):
            ops += _sombrero(n, cy)
        return ops
    if nombre in ("pelo_neg", "pelo_cas", "pelo_roj", "pelo_cano", "pelo_rubio"):
        col = {"pelo_neg": PELO_NEG, "pelo_cas": PELO_CAS, "pelo_roj": PELO_ROJ, "pelo_cano": PELO_CANO, "pelo_rubio": (222, 186, 110)}[nombre]
        return _pelo(col, cy)
    if nombre == "pelo_largo":            # pelo largo suelto (paleoindios)
        return _pelo(PELO_NEG, cy) + forma(pol((-42, cy - 10), (-54, cy + 70), (-36, cy + 80), (-34, cy + 6)), PELO_NEG, 4, sp=6) + \
            forma(pol((42, cy - 10), (54, cy + 70), (36, cy + 80), (34, cy + 6)), PELO_NEG, 4, sp=6)
    if nombre == "cinta_pieles":         # cinta de cuero con una pluma
        return forma(rect(-44, cy - 30, 44, cy - 20, 3), CUERO, 3.6, sp=4) + forma(elip(30, cy - 62, 8, 26, 0.3, 1.0, 12), PLUMA_H, 3.2, sp=3)
    if nombre == "plumas_halcon":        # tocado de plumas de halcón (cultura del Misisipi)
        ops = []
        for k in range(7):
            a = math.radians(-150 + 20 * k)
            cx, cyy = 66 * math.cos(a), cy - 44 + 56 * math.sin(a)
            col = PLUMA_H if k % 2 == 0 else CONCHA
            ops += forma(elip(cx, cyy, 13, 40, a + math.pi / 2, 1.0, 18), col, 3.6, sp=4)
            ops += [T(linea((cx * 0.55, cy - 44 + (cyy - cy + 44) * 0.55), (cx * 1.35, cy - 44 + (cyy - cy + 44) * 1.35)), 2.2, peso=0.01)]
            ops += [R(elip(cx * 1.42, cy - 44 + (cyy - cy + 44) * 1.42, 9, 10, a, 1.0, 10), CUERO_OSC, peso=0.01, sp=2)]
        ops += _pelo(PELO_NEG, cy)
        ops += forma(rect(-46, cy - 34, 46, cy - 20, 4), ROJO_US, 3.8, sp=4)
        ops += [R(circ(-24 + 24 * k, cy - 27, 5, n=10), CONCHA, peso=0.02, sp=3) for k in range(3)]
        return ops
    if nombre == "rodetes":              # peinado hopi «flor de calabaza»
        ops = _pelo(PELO_NEG, cy)
        for lado in (-1, 1):
            ops += forma(circ(lado * 56, cy - 18, 22, n=20), PELO_NEG, 4.2, sp=6)
            ops += [T(arco_(lado * 56, cy - 18, 11, 0, 300, 12), 2.6, peso=0.02)]
        return ops
    if nombre == "gustoweh":             # gorro iroqués con plumas erguidas
        ops = forma(curva([(-44, cy - 16), (-42, cy - 50), (0, cy - 64), (42, cy - 50), (44, cy - 16)], 5).tolist() + [(0, cy - 26)], CUERO, 4.4, sp=6)
        ops += forma(rect(-46, cy - 30, 46, cy - 18, 3), CONCHA, 3.6, sp=4)
        ops += [R(pol((-40 + 14 * k, cy - 28), (-34 + 14 * k, cy - 20), (-28 + 14 * k, cy - 28)), WAMPUM_M, peso=0.01, sp=2) for k in range(6)]
        for dx, h in ((-10, 64), (8, 80), (24, 56)):
            ops += forma(elip(dx, cy - 64 - h / 2, 8, h / 2, 0.08 * dx / 10, 1.0, 14), CONCHA, 3.4, sp=3)
            ops += [R(elip(dx, cy - 64 - h + 10, 6, 10, 0, 1.0, 10), NEGRO_US, peso=0.01, sp=2)]
        return ops
    if nombre == "morrion":
        ops = forma(curva([(-70, cy - 22), (-48, cy - 32), (-36, cy - 66), (0, cy - 80), (36, cy - 66), (48, cy - 32), (70, cy - 22),
                           (40, cy - 38), (-40, cy - 38)], 6), ACERO, 4.8, sp=8)
        ops += forma(curva([(-26, cy - 70), (-6, cy - 104), (18, cy - 104), (30, cy - 70)], 5).tolist() + [(0, cy - 78)], ACERO, 4.2, sp=5)
        return ops + forma(pol((-2, cy - 104), (8, cy - 132), (16, cy - 102)), ROJO_US, 3.0, sp=3)
    if nombre == "tonsura":              # corona de pelo del fraile
        return forma(curva([(-44, cy - 2), (-46, cy - 26), (-36, cy - 40), (-30, cy - 30), (-36, cy - 16), (-38, cy - 2)], 4), PELO_CAS, 3.8, sp=4) + \
            forma(curva([(44, cy - 2), (46, cy - 26), (36, cy - 40), (30, cy - 30), (36, cy - 16), (38, cy - 2)], 4), PELO_CAS, 3.8, sp=4)
    if nombre == "ala_ancha":            # sombrero de colono de Jamestown
        ops = forma(curva([(-36, cy - 36), (-30, cy - 82), (0, cy - 90), (30, cy - 82), (36, cy - 36)], 5), CUERO_OSC, 4.6, sp=7)
        ops += forma(elip(0, cy - 36, 84, 15, 0, 1.0, 26), CUERO_OSC, 4.6, sp=7)
        return ops + [R(pol((-34, cy - 52), (34, cy - 52), (34, cy - 42), (-34, cy - 42)), BEIGE_US, peso=0.01, sp=3)]
    if nombre == "capotain":             # sombrero alto del peregrino, con hebilla
        ops = forma(pol((-34, cy - 36), (-26, cy - 118), (26, cy - 118), (34, cy - 36)), NEGRO_US, 4.8, sp=8)
        ops += forma(elip(0, cy - 36, 66, 12, 0, 1.0, 24), NEGRO_US, 4.6, sp=7)
        ops += [R(pol((-33, cy - 58), (33, cy - 58), (34, cy - 46), (-34, cy - 46)), CUERO, peso=0.02, sp=3)]
        return ops + forma(rect(-12, cy - 62, 12, cy - 42, 2), LATON, 3.6, sp=3) + forma(rect(-5, cy - 56, 5, cy - 48, 1), CUERO, 2.6, sp=2)
    if nombre == "cofia":                # cofia blanca de peregrina
        ops = _pelo(PELO_CAS, cy)
        return ops + forma(curva([(-50, cy + 6), (-52, cy - 34), (-30, cy - 58), (0, cy - 64), (30, cy - 58), (52, cy - 34), (50, cy + 6),
                                  (40, cy - 8), (38, cy - 28), (0, cy - 40), (-38, cy - 28), (-40, cy - 8)], 5), BLANCO_US, 4.2, sp=6)
    if nombre == "corona_jorge":         # corona británica
        ops = _sombrero("peluca_blanca", cy)
        ops += forma(pol((-42, cy - 32), (-46, cy - 82), (-24, cy - 66), (0, cy - 96), (24, cy - 66), (46, cy - 82), (42, cy - 32)), ORO_US, 4.6, sp=7)
        ops += forma(rect(-44, cy - 42, 44, cy - 28, 3), ARMINIO, 3.8, sp=4)
        ops += [R(circ(-20 + 20 * k, cy - 35, 4, n=8), NEGRO_US, peso=0.01, sp=2) for k in range(3)]
        ops += [T(linea((0, cy - 96), (0, cy - 114)), 4, peso=0.02), T(linea((-8, cy - 106), (8, cy - 106)), 4, peso=0.02)]
        return ops + [R(circ(0, cy - 58, 6, n=10), ROJO_US, peso=0.02, sp=3)]
    if nombre == "tricornio":
        return _tricornio(cy)
    if nombre == "tricornio_oro":        # oficial: ribete dorado y escarapela
        return _tricornio(cy, NEGRO_US, LATON, BLANCO_US)
    if nombre == "tricornio_esp":        # Gálvez: ribete dorado y escarapela roja
        return _tricornio(cy, NEGRO_US, LATON, ROJO_US)
    if nombre == "tricornio_cont":       # Ejército Continental
        return _tricornio(cy, NEGRO_US, BLANCO_US, NEGRO_US)
    if nombre == "peluca_blanca":
        ops = forma(curva([(-46, cy - 4), (-50, cy - 32), (-32, cy - 54), (0, cy - 60), (32, cy - 54), (50, cy - 32), (46, cy - 4),
                           (36, cy - 22), (0, cy - 32), (-36, cy - 22)], 6), PELUCA, 4.4, sp=7)
        for lado in (-1, 1):
            ops += forma(elip(lado * 48, cy - 4, 13, 10, 0, 1.0, 12), PELUCA, 3.6, sp=4)
            ops += forma(elip(lado * 48, cy + 16, 13, 10, 0, 1.0, 12), PELUCA, 3.6, sp=4)
        return ops
    if nombre == "pelo_jefferson":       # pelo rojizo recogido con rizos a los lados
        ops = _pelo(PELO_ROJ, cy)
        for lado in (-1, 1):
            ops += forma(elip(lado * 48, cy - 2, 12, 11, 0, 1.0, 12), PELO_ROJ, 3.6, sp=4)
        return ops
    if nombre == "bicornio_lado":        # bicornio de Napoleón, puesto de lado
        ops = _pelo(PELO_CAS, cy)
        P = [(-104, cy - 34), (-70, cy - 58), (-30, cy - 90), (0, cy - 96), (30, cy - 90), (70, cy - 58), (104, cy - 34), (60, cy - 42), (0, cy - 40), (-60, cy - 42)]
        ops += forma(P, NEGRO_US, 5.0, sp=8)
        ops += forma(circ(18, cy - 66, 10, n=14), BLANCO_US, 3.2, sp=3) + [R(circ(18, cy - 66, 5, n=10), ROJO_US, peso=0.01, sp=2)]
        return ops
    if nombre == "mapache":              # gorro de piel de mapache con cola
        ops = forma(curva([(-46, cy - 12), (-44, cy - 52), (0, cy - 70), (44, cy - 52), (46, cy - 12), (0, cy - 26)], 6), (140, 112, 84), 4.8, sp=7)
        ops += [T(ondas(-40, 40, cy - 30, 3, 14), 2.6, peso=0.02)]
        for k in range(5):
            col = (140, 112, 84) if k % 2 == 0 else NEGRO_US
            ops += forma(elip(54 + 4 * k, cy - 14 + 18 * k, 11, 11, 0, 1.0, 12), col, 3.2, sp=3)
        return ops
    if nombre == "sombrero_clark":
        ops = _pelo(PELO_ROJ, cy)
        ops += forma(curva([(-34, cy - 38), (-28, cy - 80), (0, cy - 86), (28, cy - 80), (34, cy - 38)], 5), CUERO, 4.6, sp=7)
        return ops + forma(elip(0, cy - 38, 66, 12, -0.06, 1.0, 22), CUERO, 4.4, sp=6)
    if nombre == "trenzas":
        ops = _pelo(PELO_NEG, cy)
        for lado in (-1, 1):
            ops += forma(pol((lado * 38, cy - 6), (lado * 50, cy + 10), (lado * 46, cy + 96), (lado * 34, cy + 96), (lado * 36, cy + 10)), PELO_NEG, 3.8, sp=4)
            ops += [rayita(lado * 36, cy + 30 + 18 * k, lado * 48, cy + 38 + 18 * k, 2.4) for k in range(3)]
            ops += forma(rect(lado * 40 - 7, cy + 92, lado * 40 + 7, cy + 102, 2), ROJO_US, 2.8, sp=2)
        return ops + forma(rect(-44, cy - 30, 44, cy - 20, 3), TURQUESA, 3.4, sp=3)
    if nombre == "turbante_cherokee":
        ops = forma(curva([(-48, cy - 16), (-50, cy - 50), (-26, cy - 72), (0, cy - 76), (26, cy - 72), (50, cy - 50), (48, cy - 16), (0, cy - 28)], 6),
                    (196, 84, 68), 4.8, sp=7)
        ops += [T(curva([(-46, cy - 34), (0, cy - 52), (46, cy - 38)], 5), 3.0, peso=0.03), T(curva([(-44, cy - 52), (0, cy - 68), (42, cy - 56)], 5), 3.0, peso=0.03)]
        return ops + forma(elip(30, cy - 92, 7, 22, 0.4, 1.0, 12), CONCHA, 3.0, sp=3)
    if nombre == "chaco_us":             # chacó azul del ejército de EE. UU. (1846)
        ops = forma(rect(-34, cy - 92, 34, cy - 34, 4), AZUL_OSC_US, 4.6, sp=7)
        ops += forma(rect(-46, cy - 40, 46, cy - 28, 3), NEGRO_US, 3.8, sp=4)
        return ops + forma(circ(0, cy - 66, 9, n=12), LATON, 3.0, sp=3) + forma(elip(0, cy - 100, 8, 10, 0, 1.0, 12), BLANCO_US, 3.0, sp=3)
    if nombre == "chaco_mx":             # chacó mexicano con pompón rojo
        ops = forma(pol((-32, cy - 34), (-38, cy - 96), (38, cy - 96), (32, cy - 34)), NEGRO_US, 4.6, sp=7)
        ops += forma(rect(-44, cy - 40, 44, cy - 28, 3), NEGRO_US, 3.8, sp=4)
        ops += [R(pol((-36, cy - 80), (36, cy - 80), (37, cy - 72), (-37, cy - 72)), ROJO_US, peso=0.01, sp=2)]
        return ops + forma(circ(0, cy - 108, 13, n=14), ROJO_US, 3.4, sp=4) + forma(circ(0, cy - 58, 8, n=12), LATON, 3.0, sp=3)
    if nombre == "sombrero_minero":      # sombrero aplastado del buscador de oro
        ops = _pelo(PELO_CAS, cy)
        ops += forma(curva([(-38, cy - 34), (-34, cy - 70), (-10, cy - 64), (8, cy - 76), (34, cy - 68), (38, cy - 34)], 5), (128, 110, 86), 4.6, sp=7)
        return ops + forma(curva([(-74, cy - 30), (-40, cy - 42), (0, cy - 38), (40, cy - 44), (76, cy - 34), (40, cy - 26), (0, cy - 28), (-40, cy - 24)], 5),
                           (128, 110, 86), 4.4, sp=6)
    if nombre == "chistera_alta":        # chistera altísima de Lincoln
        ops = forma(elip(-42, cy - 18, 8, 16, 0, 1.0, 12), PELO_NEG, 3.2, sp=3) + forma(elip(42, cy - 18, 8, 16, 0, 1.0, 12), PELO_NEG, 3.2, sp=3)
        ops += forma(pol((-30, cy - 38), (-32, cy - 148), (32, cy - 148), (30, cy - 38)), NEGRO_US, 5.0, sp=8)
        ops += forma(rect(-52, cy - 44, 52, cy - 32, 4), NEGRO_US, 4.4, sp=6)
        return ops + [R(pol((-31, cy - 66), (31, cy - 66), (31, cy - 54), (-31, cy - 54)), GRIS_OSC_US, peso=0.02, sp=3)]
    if nombre == "chistera":
        ops = forma(rect(-30, cy - 104, 30, cy - 36, 4), NEGRO_US, 4.6, sp=7)
        return ops + forma(rect(-52, cy - 42, 52, cy - 30, 4), NEGRO_US, 4.4, sp=6)
    if nombre in ("kepi_azul", "kepi_gris"):
        col = AZUL_OSC_US if nombre == "kepi_azul" else GRIS_CONF
        ops = _pelo(PELO_CAS, cy)
        ops += forma(pol((-38, cy - 30), (-28, cy - 78), (34, cy - 70), (40, cy - 30)), col, 4.6, sp=7)
        ops += forma(pol((-44, cy - 32), (44, cy - 32), (52, cy - 20), (-20, cy - 22)), NEGRO_US, 3.8, sp=4)
        return ops + forma(circ(0, cy - 50, 6, n=10), LATON, 2.8, sp=2)
    if nombre == "panuelo":              # pañuelo atado en la cabeza
        ops = forma(curva([(-46, cy - 8), (-48, cy - 44), (-24, cy - 64), (0, cy - 68), (24, cy - 64), (48, cy - 44), (46, cy - 8), (0, cy - 26)], 6),
                    (210, 120, 66), 4.6, sp=7)
        ops += forma(pol((30, cy - 60), (62, cy - 82), (56, cy - 54)), (210, 120, 66), 3.6, sp=3)
        return ops + [R(circ(-16 + 16 * k, cy - 46, 4, n=8), CREMA_US, peso=0.01, sp=2) for k in range(3)]
    if nombre in ("gorra_obrero", "gorra_gris"):
        col = (104, 96, 88) if nombre == "gorra_obrero" else (150, 146, 136)
        ops = forma(curva([(-46, cy - 24), (-44, cy - 56), (0, cy - 66), (44, cy - 56), (50, cy - 30)], 5).tolist() + [(0, cy - 30)], col, 4.6, sp=7)
        return ops + forma(pol((-46, cy - 28), (50, cy - 30), (64, cy - 18), (-30, cy - 20)), col, 4.0, sp=5)
    if nombre == "calva_lados":          # calvo con pelo a los lados
        return forma(elip(-42, cy - 14, 9, 16, 0, 1.0, 12), PELO_CANO, 3.4, sp=3) + forma(elip(42, cy - 14, 9, 16, 0, 1.0, 12), PELO_CANO, 3.4, sp=3)
    if nombre == "sombrero_campana":     # sombrero de campaña de los Rough Riders
        ops = _pelo(PELO_CAS, cy)
        ops += forma(curva([(-36, cy - 34), (-30, cy - 78), (-8, cy - 70), (0, cy - 84), (8, cy - 70), (30, cy - 78), (36, cy - 34)], 5), CAQUI_US, 4.6, sp=7)
        return ops + forma(elip(0, cy - 34, 82, 14, 0, 1.0, 24), CAQUI_US, 4.4, sp=6) + [R(pol((-34, cy - 50), (34, cy - 50), (35, cy - 42), (-35, cy - 42)),
                                                                                             CUERO_OSC, peso=0.01, sp=2)]
    if nombre in ("fedora", "fedora_gris"):
        col = (110, 100, 92) if nombre == "fedora" else (134, 136, 140)
        ops = forma(curva([(-36, cy - 36), (-32, cy - 80), (-8, cy - 72), (0, cy - 82), (8, cy - 72), (32, cy - 80), (36, cy - 36)], 5), col, 4.6, sp=7)
        ops += forma(curva([(-70, cy - 30), (-36, cy - 40), (36, cy - 40), (70, cy - 32), (36, cy - 28), (-36, cy - 28)], 5), col, 4.4, sp=6)
        return ops + [R(pol((-35, cy - 52), (35, cy - 52), (36, cy - 42), (-36, cy - 42)), NEGRO_US, peso=0.01, sp=2)]
    if nombre == "casco_plato":          # casco Brodie de la Primera Guerra Mundial
        ops = forma(curva([(-30, cy - 36), (-24, cy - 66), (0, cy - 74), (24, cy - 66), (30, cy - 36)], 5), VERDE_OLIVA, 4.6, sp=7)
        return ops + forma(elip(0, cy - 36, 78, 14, 0, 1.0, 24), VERDE_OLIVA, 4.6, sp=7)
    if nombre == "melena":               # melena corta «bob» con cinta
        ops = forma(curva([(-48, cy + 22), (-52, cy - 30), (-30, cy - 54), (0, cy - 58), (30, cy - 54), (52, cy - 30), (48, cy + 22),
                           (38, cy + 18), (36, cy - 18), (14, cy - 30), (-24, cy - 18), (-38, cy + 18)], 6), PELO_NEG, 4.4, sp=7)
        ops += forma(rect(-46, cy - 38, 46, cy - 28, 3), (196, 70, 90), 3.2, sp=3)
        return ops + forma(elip(34, cy - 52, 8, 18, 0.5, 1.0, 12), BLANCO_US, 3.0, sp=3)
    if nombre == "sombrero_sufragista":
        ops = _pelo(PELO_CAS, cy)
        ops += forma(curva([(-36, cy - 36), (-30, cy - 72), (0, cy - 80), (30, cy - 72), (36, cy - 36)], 5), VIOLETA, 4.6, sp=7)
        ops += forma(elip(0, cy - 38, 80, 13, 0, 1.0, 24), VIOLETA, 4.4, sp=6)
        return ops + forma(circ(28, cy - 58, 11, n=12), AMARILLO_SUF, 3.0, sp=3) + forma(circ(12, cy - 62, 9, n=12), BLANCO_US, 3.0, sp=3)
    if nombre == "casco_m1":
        ops = forma(curva([(-48, cy - 16), (-46, cy - 54), (-24, cy - 74), (0, cy - 78), (24, cy - 74), (46, cy - 54), (48, cy - 16),
                           (40, cy - 22), (0, cy - 30), (-40, cy - 22)], 6), VERDE_OLIVA, 4.8, sp=7)
        return ops + [T(linea((-30, cy - 40), (-18, cy + 30)), 3, peso=0.02), T(linea((30, cy - 40), (18, cy + 30)), 3, peso=0.02)]
    if nombre == "gorro_marinero":
        ops = _pelo(PELO_CAS, cy)
        return ops + forma(curva([(-44, cy - 36), (-46, cy - 60), (0, cy - 70), (46, cy - 60), (44, cy - 36), (0, cy - 42)], 5), BLANCO_US, 4.4, sp=6)
    if nombre == "ushanka":              # gorro soviético de orejeras
        ops = forma(curva([(-46, cy - 20), (-42, cy - 62), (0, cy - 76), (42, cy - 62), (46, cy - 20)], 5).tolist() + [(0, cy - 32)], (128, 104, 80), 4.8, sp=7)
        for lado in (-1, 1):
            ops += forma(pol((lado * 40, cy - 30), (lado * 58, cy - 26), (lado * 56, cy + 22), (lado * 40, cy + 18)), (128, 104, 80), 4.0, sp=5)
        ops += forma(rect(-48, cy - 40, 48, cy - 26, 4), (150, 124, 96), 3.8, sp=4)
        return ops + [R(pol(*[(11 * math.cos(math.radians(-90 + 72 * k * 2)), cy - 54 + 11 * math.sin(math.radians(-90 + 72 * k * 2))) for k in range(5)]),
                        ROJO_US, peso=0.01, sp=2)] + forma(pol(*[(11 * math.cos(math.radians(-90 + 72 * k * 2)), cy - 54 + 11 * math.sin(math.radians(-90 + 72 * k * 2)))
                                                                 for k in range(5)]), ROJO_US, 2.6, sp=2)
    if nombre in ("tupe", "tupe_negro"):  # tupé (Kennedy castaño, rockero negro)
        col = PELO_CAS if nombre == "tupe" else PELO_NEG
        return forma([(-42, cy - 4), (-46, cy - 34), (-34, cy - 54), (-4, cy - 66), (30, cy - 64), (50, cy - 40), (44, cy - 4), (38, cy - 22),
                      (14, cy - 34), (-12, cy - 30), (-36, cy - 20)], col, 4.4, sp=7)
    if nombre == "casco_astronauta":     # escafandra con visera dorada (tapa la cara)
        ops = forma(circ(0, cy - 4, 62, n=40), BLANCO_US, 5.2, sp=8)
        ops += forma(elip(0, cy + 2, 44, 36, 0, 1.0, 30), VISERA, 4.4, sp=6)
        ops += [R(elip(-16, cy - 12, 12, 8, -0.5, 1.0, 12), (250, 236, 190), peso=0.01, sp=2)]
        return ops + forma(rect(-34, cy + 56, 34, cy + 70, 4), GRIS_OSC_US, 3.6, sp=3)
    if nombre == "sombrerito":           # sombrero pequeño de Rosa Parks
        ops = _pelo(PELO_NEG, cy)
        return ops + forma(curva([(-38, cy - 38), (-30, cy - 64), (0, cy - 70), (30, cy - 64), (38, cy - 38)], 5).tolist() + [(0, cy - 44)], (84, 70, 76),
                           4.4, sp=6)
    if nombre == "casco_bombero":
        ops = forma(curva([(-40, cy - 34), (-36, cy - 70), (0, cy - 84), (36, cy - 70), (40, cy - 34)], 5), (190, 160, 70), 4.8, sp=7)
        ops += forma(curva([(-62, cy - 30), (-40, cy - 40), (40, cy - 40), (70, cy - 20), (40, cy - 28), (-40, cy - 28)], 5), (190, 160, 70), 4.4, sp=6)
        return ops + forma(pol((-14, cy - 78), (14, cy - 78), (16, cy - 46), (-16, cy - 46)), BLANCO_US, 3.2, sp=3)
    if nombre == "rizos_flor":           # pelo ondulado con una flor
        ops = forma(curva([(-46, cy + 34), (-50, cy - 30), (-30, cy - 54), (0, cy - 58), (30, cy - 54), (50, cy - 30), (46, cy + 34),
                           (38, cy + 30), (38, cy - 20), (0, cy - 30), (-38, cy - 20), (-38, cy + 30)], 6), PELO_NEG, 4.4, sp=7)
        ops += [T(ondas(-44, -36, cy + 20, 3, 8), 2.4, peso=0.02), T(ondas(36, 44, cy + 20, 3, 8), 2.4, peso=0.02)]
        for k in range(5):
            a = math.radians(72 * k)
            ops += forma(circ(36 + 10 * math.cos(a), cy - 50 + 10 * math.sin(a), 8, n=10), ROSA_V, 2.6, sp=2)
        return ops + [R(circ(36, cy - 50, 5, n=8), ORO_US, peso=0.01, sp=2)]
    return _orig_sombrero(nombre, cy)


OB.sombrero = _sombrero


# ------------------------------------------------------------------ accesorios en mano
def _acc_lanza_piedra(m, d):
    x, y = m
    return [T(linea((x - 2, y + 90), (x + 6, y - 196)), 5.2, peso=0.12)] + forma(pol((x - 8, y - 190), (x + 8, y - 252), (x + 22, y - 190), (x + 7, y - 180)),
                                                                                 (156, 140, 120), 4.0, sp=4) + [rayita(x - 2, y - 186, x + 16, y - 184, 3.4)]


def _acc_maza_cahokia(m, d):
    x, y = m
    ops = [T(linea((x, y + 40), (x + 6, y - 150)), 5.4, peso=0.08)]
    return ops + forma(curva([(x - 30, y - 140), (x - 18, y - 172), (x + 12, y - 182), (x + 6, y - 158), (x + 28, y - 150), (x - 6, y - 140)], 4),
                       (88, 96, 108), 4.2, sp=4) + forma(elip(x + 2, y - 120, 9, 16, 0, 1.0, 12), CONCHA, 3, sp=2)


def _acc_vasija(m, d):
    x, y = m
    ops = forma(curva([(x - 16, y - 66), (x - 36, y - 40), (x - 32, y - 6), (x, y + 8), (x + 32, y - 6), (x + 36, y - 40), (x + 16, y - 66)], 5).tolist()
                + [(x - 16, y - 66)], BLANCO_US, 4.4, sp=6)
    ops += [T(linea((x - 32, y - 40), (x - 20, y - 26), (x - 8, y - 40), (x + 4, y - 26), (x + 16, y - 40), (x + 30, y - 26)), 3.4, peso=0.02)]
    ops += [R(pol((x - 30, y - 18), (x + 30, y - 18), (x + 26, y - 10), (x - 26, y - 10)), NEGRO_V, peso=0.01, sp=2)]
    return ops + [R(pol((x - 16, y - 62), (x + 16, y - 62), (x + 20, y - 54), (x - 20, y - 54)), NEGRO_V, peso=0.01, sp=2)]


def _acc_wampum(m, d):
    x, y = m
    ops = forma(rect(x - 16, y - 8, x + 16, y + 104, 3), WAMPUM_M, 4.0, sp=5)
    for k in range(3):
        cy = y + 14 + 32 * k
        ops += forma(pol((x, cy - 12), (x + 11, cy), (x, cy + 12), (x - 11, cy)), BLANCO_US, 2.6, sp=2)
    return ops + [rayita(x - 10 + 7 * k, y + 104, x - 10 + 7 * k, y + 120, 2.2) for k in range(4)]


def _acc_estandarte_borgona(m, d):
    x, y = m
    ops = [T(linea((x, y + 44), (x + 4, y - 196)), 5.4, peso=0.1)]
    ops += forma(pol((x + 4, y - 196), (x + 104, y - 190), (x + 100, y - 112), (x + 4, y - 116)), BLANCO_US, 4.2, sp=6)
    ops += [R(pol((x + 8, y - 192), (x + 22, y - 192), (x + 98, y - 118), (x + 84, y - 116)), ROJO_US, peso=0.02, sp=3),
            R(pol((x + 84, y - 192), (x + 100, y - 190), (x + 22, y - 118), (x + 6, y - 120)), ROJO_US, peso=0.02, sp=3)]
    return ops


def _acc_cruz(m, d):
    x, y = m
    return forma(rect(x - 5, y - 70, x + 5, y + 10, 1), MADERA_OSC_US, 3.4, sp=2) + forma(rect(x - 22, y - 52, x + 22, y - 42, 1), MADERA_OSC_US, 3.4, sp=2)


def _acc_mosquete(m, d):
    x, y = m
    ops = [R(pol((x - 26, y + 56), (x - 8, y + 62), (x + 2, y + 14), (x - 12, y + 8)), MADERA_US, peso=0.03, sp=4),
           T(pol((x - 26, y + 56), (x - 8, y + 62), (x + 2, y + 14), (x - 12, y + 8), (x - 26, y + 56)), 3.6, peso=0.03)]
    return ops + [T(linea((x - 6, y + 14), (x + 26, y - 168)), 5.0, peso=0.06)]


def _acc_fusil_bay(m, d):
    x, y = m
    return _acc_mosquete(m, d) + [T(linea((x + 26, y - 168), (x + 33, y - 210)), 3.2, peso=0.03)]


def _acc_hojas_tabaco(m, d):
    x, y = m
    ops = []
    for k, a in enumerate((-0.5, 0.0, 0.5)):
        ops += forma(elip(x + 34 * math.sin(a), y - 44 - 4 * k, 15, 46, a, 1.0, 18), TABACO, 3.8, sp=4)
        ops += [T(linea((x, y), (x + 70 * math.sin(a), y - 86)), 2.4, peso=0.02)]
    return ops


def _acc_libro(m, d, col=NEGRO_US):
    x, y = m
    return forma(rect(x - 26, y - 40, x + 26, y + 16, 4), col, 4.2, sp=5) + [rayita(x - 20, y - 36, x - 20, y + 12, 2.4)]


def _acc_diario(m, d):
    return _acc_libro(m, d, CUERO)


def _acc_cetro(m, d):
    x, y = m
    ops = [T(linea((x, y + 56), (x + 4, y - 130)), 5.4, peso=0.08), R(pol((x - 3, y + 56), (x + 3, y + 56), (x + 7, y - 130), (x + 1, y - 130)), ORO_US, peso=0.02, sp=2)]
    return ops + forma(circ(x + 4, y - 144, 14, n=14), ORO_US, 4.2, sp=4) + [rayita(x + 4, y - 158, x + 4, y - 176, 3.4), rayita(x - 4, y - 168, x + 12, y - 168, 3.4)]


def _acc_pluma(m, d):
    x, y = m
    ops = forma(curva([(x, y + 6), (x + 10, y - 50), (x + 34, y - 92), (x + 18, y - 36)], 5), BLANCO_US, 3.8, sp=4)
    return ops + [T(linea((x - 4, y + 16), (x + 30, y - 84)), 3.4, peso=0.03)]


def _acc_pergamino(m, d):
    x, y = m
    ops = forma(rect(x - 30, y - 70, x + 30, y + 14, 3), CREMA_US, 4.0, sp=5)
    ops += [R(elip(x, y - 70, 32, 7, 0, 1.0, 14), BEIGE_US, peso=0.02, sp=3), T(elip(x, y - 70, 32, 7, 0, 1.0, 14), 3.4, peso=0.03)]
    return ops + [rayita(x - 20, y - 52 + 12 * k, x + (20 if k < 4 else 4), y - 52 + 12 * k, 2.2) for k in range(5)] + \
        [T(curva([(x - 2, y + 2), (x + 8, y - 6), (x + 16, y + 2), (x + 24, y - 4)], 4), 2.6, peso=0.02)]


def _acc_espada(m, d):
    x, y = m
    ops = [T(linea((x, y + 14), (x + 10, y - 116)), 4.6, peso=0.06), R(pol((x - 3, y - 14), (x + 6, y - 118), (x + 10, y - 14)), ACERO, peso=0.04, sp=3)]
    return ops + forma(rect(x - 18, y - 22, x + 22, y - 12, 2), LATON, 3.4, sp=2)


def _acc_brujula(m, d):
    x, y = m
    ops = forma(circ(x, y - 14, 24, n=22), LATON, 4.2, sp=4) + forma(circ(x, y - 14, 17, n=18), CREMA_US, 3.0, sp=3)
    return ops + [R(pol((x - 4, y - 14), (x + 8, y - 28), (x + 4, y - 10)), ROJO_US, peso=0.01, sp=2), T(linea((x - 8, y), (x + 8, y - 28)), 2.6, peso=0.02)]


def _acc_batea(m, d):
    x, y = m
    ops = forma(curva([(x - 48, y - 18), (x - 36, y + 4), (x, y + 10), (x + 36, y + 4), (x + 48, y - 18)], 5).tolist() + [(x - 48, y - 18)], ACERO, 4.2, sp=5)
    return ops + [R(circ(x - 18 + 14 * k, y - 10 + 3 * (k % 2), 5, n=8), ORO_US, peso=0.01, sp=2) for k in range(4)] + [T(ondas(x - 34, x + 34, y - 4, 2, 12), 2.4, peso=0.02)]


def _acc_saco_algodon(m, d):
    x, y = m
    ops = forma(curva([(x - 30, y - 30), (x - 44, y + 30), (x - 30, y + 70), (x + 30, y + 70), (x + 44, y + 30), (x + 30, y - 30)], 6), (222, 210, 182), 4.4, sp=6)
    for dx, dy in ((-16, -40), (2, -48), (18, -38)):
        ops += forma(circ(x + dx, y + dy, 13, n=14), ALGODON, 3.4, sp=3)
    return ops


def _acc_cadena(m, d):
    x, y = m
    ops = forma(rect(x - 18, y - 12, x + 18, y + 4, 4), ACERO_OSC, 3.8, sp=3)
    for k in range(3):
        ops += [T(elip(x + 4 * (k % 2), y + 18 + 16 * k, 7, 10, 0.3 * (1 if k % 2 else -1), 1.05, 14), 3.4, peso=0.03)]
    return ops + [T(linea((x + 2, y + 66), (x - 6, y + 74)), 3.2, peso=0.02), T(linea((x + 4, y + 66), (x + 12, y + 72)), 3.2, peso=0.02)]


def _acc_mazo(m, d):
    x, y = m
    return [T(linea((x - 4, y + 30), (x + 8, y - 130)), 6, peso=0.08)] + forma(rect(x - 26, y - 160, x + 42, y - 126, 4), ACERO_OSC, 4.4, sp=5)


def _acc_baston(m, d):
    x, y = m
    return [T(linea((x, y - 10), (x + 4, y + 120)), 5, peso=0.08)] + forma(circ(x, y - 14, 10, n=12), LATON, 3.2, sp=3)


def _acc_bolsa_dinero(m, d):
    x, y = m
    ops = forma(curva([(x - 14, y - 14), (x - 44, y + 20), (x - 38, y + 64), (x, y + 74), (x + 38, y + 64), (x + 44, y + 20), (x + 14, y - 14)], 6),
                (176, 168, 120), 4.4, sp=6)
    ops += [T(linea((x - 16, y - 10), (x + 16, y - 10)), 4, peso=0.02)]
    return ops + forma(circ(x, y + 34, 16, n=16), ORO_US, 3.4, sp=3) + [T(arco_(x, y + 34, 8, 200, 520, 10), 2.4, peso=0.02)]


def _acc_bombilla(m, d):
    x, y = m
    ops = [T(linea((x - 30 * math.cos(a) * 1.0 + 0, y - 56 + 30 * math.sin(a)), (x - 48 * math.cos(a), y - 56 + 48 * math.sin(a))), 3.2, peso=0.02)
           for a in np.linspace(math.radians(200), math.radians(340), 5)]
    ops += forma(circ(x, y - 56, 24, n=24), (252, 230, 120), 4.2, sp=4)
    ops += [T(arco_(x, y - 52, 7, 180, 540, 14), 2.4, peso=0.02), T(linea((x - 6, y - 36), (x - 6, y - 50)), 2.2, peso=0.01),
            T(linea((x + 6, y - 36), (x + 6, y - 50)), 2.2, peso=0.01)]
    return ops + forma(rect(x - 12, y - 34, x + 12, y - 14, 2), ACERO, 3.4, sp=2) + [rayita(x - 12, y - 27, x + 12, y - 27, 2.2)]


def _acc_maleta(m, d):
    x, y = m
    ops = [T(arco_(x, y + 4, 12, 180, 360, 8), 3.6, peso=0.02)]
    ops += forma(rect(x - 44, y + 4, x + 44, y + 64, 6), CUERO, 4.4, sp=6)
    return ops + [R(pol((x - 44, y + 22), (x + 44, y + 22), (x + 44, y + 30), (x - 44, y + 30)), CUERO_OSC, peso=0.01, sp=2)] + \
        forma(rect(x - 8, y + 18, x + 8, y + 32, 2), LATON, 2.6, sp=2)


def _acc_hatillo(m, d):
    x, y = m
    return [T(linea((x, y + 10), (x + 40, y - 110)), 4.6, peso=0.06)] + forma(circ(x + 44, y - 124, 26, n=20), (190, 98, 84), 4.2, sp=5) + \
        [R(circ(x + 36 + 10 * k, y - 126 + 6 * (k % 2), 3, n=6), BLANCO_US, peso=0.01, sp=1) for k in range(3)]


def _acc_trompeta(m, d):
    x, y = m
    ops = forma(pol((x - 10, y - 6), (x + 70, y - 12), (x + 70, y + 2), (x - 10, y + 2)), LATON, 3.6, sp=3)
    ops += forma(pol((x + 66, y - 14), (x + 100, y - 30), (x + 100, y + 20), (x + 66, y + 4)), LATON, 4.0, sp=4)
    return ops + [R(circ(x + 18 + 12 * k, y - 16, 5, n=8), LATON, peso=0.01, sp=2) for k in range(3)]


def _acc_papeles(m, d):
    x, y = m
    ops = []
    for k, (dx, dy, a) in enumerate(((0, -30, 0.2), (30, -70, -0.4), (-24, -84, 0.5))):
        c, s = math.cos(a), math.sin(a)
        P = [(x + dx + c * px - s * py, y + dy + s * px + c * py) for px, py in ((-20, -26), (20, -26), (20, 26), (-20, 26))]
        ops += forma(P, BLANCO_US, 3.4, sp=3)
        ops += [T(linea(((P[0][0] * 3 + P[3][0]) / 4 + 4, (P[0][1] * 3 + P[3][1]) / 4), ((P[1][0] * 3 + P[2][0]) / 4 - 4, (P[1][1] * 3 + P[2][1]) / 4)), 2, peso=0.01)]
    return ops


def _acc_cartel(m, d):
    x, y = m
    return [T(linea((x, y + 30), (x + 2, y - 150)), 5.2, peso=0.08)] + forma(rect(x - 64, y - 236, x + 66, y - 140, 4), BLANCO_US, 4.4, sp=6)


def _acc_fusil_moderno(m, d):
    x, y = m
    ops = [R(pol((x - 24, y + 50), (x - 6, y + 56), (x + 4, y + 18), (x - 10, y + 12)), CUERO, peso=0.03, sp=4),
           T(pol((x - 24, y + 50), (x - 6, y + 56), (x + 4, y + 18), (x - 10, y + 12), (x - 24, y + 50)), 3.6, peso=0.03)]
    ops += [T(linea((x - 4, y + 18), (x + 24, y - 140)), 5.6, peso=0.06)]
    return ops + forma(rect(x - 4, y - 30, x + 14, y - 4, 2), NEGRO_US, 3, sp=2)


def _acc_guitarra(m, d):
    x, y = m
    ops = forma(curva([(x - 30, y - 6), (x - 52, y + 18), (x - 42, y + 56), (x - 6, y + 62), (x + 18, y + 40), (x + 10, y + 14), (x + 22, y - 4), (x - 6, y - 16)],
                      6), ROJO_US, 4.6, sp=6)
    ops += [T(linea((x - 6, y + 10), (x + 66, y - 96)), 6, peso=0.04)]
    ops += forma(rect(x + 60, y - 118, x + 80, y - 92, 3), NEGRO_US, 3.2, sp=2)
    return ops + forma(rect(x - 26, y + 18, x - 6, y + 30, 2), BLANCO_US, 2.6, sp=2)


def _acc_bolso(m, d):
    x, y = m
    return [T(arco_(x, y + 12, 16, 180, 360, 10), 3.6, peso=0.02)] + forma(rect(x - 30, y + 12, x + 30, y + 52, 6), (110, 70, 54), 4.2, sp=5)


def _acc_portatil(m, d):
    x, y = m
    ops = forma(pol((x - 50, y - 64), (x + 40, y - 70), (x + 46, y - 4), (x - 44, y)), ACERO_OSC, 4.2, sp=5)
    ops += forma(pol((x - 40, y - 56), (x + 32, y - 60), (x + 37, y - 12), (x - 36, y - 8)), CIELO_US, 3.2, sp=3)
    return ops + forma(pol((x - 52, y), (x + 48, y - 4), (x + 60, y + 10), (x - 46, y + 14)), ACERO, 3.6, sp=3)


def _acc_hacha(m, d):
    x, y = m
    ops = [T(linea((x - 4, y + 30), (x + 8, y - 130)), 6.4, peso=0.08)]
    ops += forma(curva([(x + 6, y - 132), (x + 40, y - 150), (x + 66, y - 140), (x + 58, y - 112), (x + 62, y - 88), (x + 30, y - 100), (x + 4, y - 106)], 4),
                 ACERO, 4.4, sp=4)
    return ops + forma(pol((x + 4, y - 128), (x - 30, y - 132), (x + 2, y - 112)), ACERO_OSC, 3.6, sp=3)


def _acc_banderita(m, d):
    x, y = m
    ops = [T(linea((x, y + 30), (x + 3, y - 150)), 4.6, peso=0.08)]
    x0, y0, x1, y1 = x + 3, y - 150, x + 93, y - 92
    for k in range(7):
        ya = y0 + (y1 - y0) * k / 7
        ops += [R(pol((x0, ya), (x1, ya), (x1, ya + (y1 - y0) / 7), (x0, ya + (y1 - y0) / 7)), ROJO_US if k % 2 == 0 else BLANCO_US, peso=0.01, sp=2)]
    ops += [R(pol((x0, y0), (x0 + 38, y0), (x0 + 38, y0 + 30), (x0, y0 + 30)), AZUL_US, peso=0.01, sp=2)]
    ops += [R(circ(x0 + 9 + 10 * (k % 3), y0 + 9 + 11 * (k // 3), 2.6, n=6), BLANCO_US, peso=0.01, sp=1) for k in range(6)]
    return ops + [T(pol((x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)), 3.4, peso=0.03)]


def _acc_libro_rojo(m, d):
    return _acc_libro(m, d, ROJO_US)


OB.ACC.update({
    "lanza_piedra": _acc_lanza_piedra, "maza_cahokia": _acc_maza_cahokia, "vasija": _acc_vasija, "wampum": _acc_wampum,
    "estandarte_borgona": _acc_estandarte_borgona, "cruz": _acc_cruz, "mosquete": _acc_mosquete, "fusil_bay": _acc_fusil_bay,
    "hojas_tabaco": _acc_hojas_tabaco, "libro_us": _acc_libro, "diario": _acc_diario, "libro_rojo": _acc_libro_rojo, "cetro_us": _acc_cetro,
    "pluma_us": _acc_pluma, "pergamino": _acc_pergamino, "espada_us": _acc_espada, "brujula_mano": _acc_brujula, "batea": _acc_batea,
    "saco_algodon": _acc_saco_algodon, "cadena": _acc_cadena, "mazo": _acc_mazo, "baston": _acc_baston, "bolsa_dinero_us": _acc_bolsa_dinero,
    "bombilla_mano": _acc_bombilla, "maleta": _acc_maleta, "hatillo": _acc_hatillo, "trompeta": _acc_trompeta, "papeles": _acc_papeles,
    "cartel": _acc_cartel, "fusil_moderno": _acc_fusil_moderno, "guitarra": _acc_guitarra, "bolso": _acc_bolso, "portatil": _acc_portatil,
    "hacha": _acc_hacha, "banderita": _acc_banderita,
})


# ------------------------------------------------------------------ piezas de cara y ropa (encima del personaje)
CY = -215.0


def _mas(p, *extra):
    ops = list(p.ops)
    for e in extra:
        ops += e
    d = Dib(ops)
    d.manos = getattr(p, "manos", [])
    return d


def _antes(p, *extra):
    """Piezas DETRÁS del personaje (mochilas, bebé a la espalda, mantos)."""
    ops = []
    for e in extra:
        ops += e
    d = Dib(ops + list(p.ops))
    d.manos = getattr(p, "manos", [])
    return d


def _barba(col=PELO_CAS, largo=74):
    """Barba bajo la boca (no la tapa): arranca en las patillas y deja libre todo lo que hay por encima de cy+30."""
    P = [(-41, CY - 2), (-40, CY + 36), (-22, CY + largo - 8), (0, CY + largo), (22, CY + largo - 8), (40, CY + 36), (41, CY - 2),
         (34, CY + 16), (20, CY + 30), (0, CY + 34), (-20, CY + 30), (-34, CY + 16)]
    return forma(curva(P, 4, cerrado=True), col, 4.2, sp=6)


def _bigote(col=PELO_CAS, ancho=22):
    return forma(curva([(-ancho, CY + 13), (-8, CY + 7), (0, CY + 10), (8, CY + 7), (ancho, CY + 13), (8, CY + 14), (0, CY + 13), (-8, CY + 14)], 4),
                 col, 3.4, sp=3)


def _gafas(redondas=True, col=None):
    ops = []
    for x in (-15, 15):
        P = circ(x, CY - 4, 12, n=18) if redondas else rect(x - 13, CY - 14, x + 13, CY + 6, 4)
        ops += [T(P, 3.2, peso=0.02)]
        if col:
            ops += [R(P, col, peso=0.01, sp=2)]
    return ops + [T(linea((-3, CY - 6), (3, CY - 6)), 3, peso=0.01), T(linea((-27, CY - 6), (-40, CY - 10)), 2.6, peso=0.01),
                  T(linea((27, CY - 6), (40, CY - 10)), 2.6, peso=0.01)]


def _solapas(col, bot=LATON):
    ops = [R(pol((-46, -172), (-14, -172), (-20, -70), (-40, -70)), col, peso=0.02, sp=4), R(pol((46, -172), (14, -172), (20, -70), (40, -70)), col, peso=0.02, sp=4)]
    ops += [T(linea((-14, -172), (-20, -70)), 3, peso=0.02), T(linea((14, -172), (20, -70)), 3, peso=0.02)]
    return ops + [R(circ(sx * 30, -150 + 26 * k, 4.5, n=8), bot, peso=0.01, sp=2) for k in range(3) for sx in (-1, 1)]


def _charreteras(col=ORO_US):
    ops = []
    for lado in (-1, 1):
        ops += forma(elip(lado * 46, -170, 20, 9, 0, 1.0, 14), col, 3.4, sp=3)
        ops += [rayita(lado * 46 + k * 6, -162, lado * 46 + k * 6, -148, 2.2) for k in (-2, -1, 0, 1, 2)]
    return ops


def _correaje():
    return [R(pol((-40, -170), (-26, -170), (40, -74), (26, -70)), BLANCO_US, peso=0.02, sp=3),
            R(pol((40, -170), (26, -170), (-40, -74), (-26, -70)), BLANCO_US, peso=0.02, sp=3),
            T(pol((-40, -170), (-26, -170), (40, -74), (26, -70), (-40, -170)), 2.6, peso=0.02),
            T(pol((40, -170), (26, -170), (-40, -74), (-26, -70), (40, -170)), 2.6, peso=0.02)]


def _botones(col=LATON, x=0, n=4, y0=-150, paso=22):
    return [R(circ(x, y0 + paso * k, 4.5, n=8), col, peso=0.01, sp=2) for k in range(n)]


def _corbata(col=ROJO_US):
    return forma(pol((-6, -170), (6, -170), (10, -110), (0, -96), (-10, -110)), col, 3, sp=3)


def _camisa_traje(camisa=BLANCO_US, corbata=None):
    """Pechera de camisa en V bajo la chaqueta (+ corbata)."""
    ops = [R(pol((-18, -174), (18, -174), (0, -112)), camisa, peso=0.02, sp=3), T(linea((-18, -174), (0, -112), (18, -174)), 3.4, peso=0.02)]
    return ops + (_corbata(corbata) if corbata else [])


def _flecos(y0=-14, x0=-50, x1=50, n=9):
    return [rayita(x0 + (x1 - x0) * k / (n - 1), y0, x0 + (x1 - x0) * k / (n - 1) + 2, y0 + 16, 2.6) for k in range(n)]


def _collar(col=CONCHA, n=7, r=5):
    return [R(circ(-24 + 48 * k / (n - 1), -166 + 8 * math.sin(math.pi * k / (n - 1)), r, n=8), col, peso=0.01, sp=2) for k in range(n)] + \
        [T(curva([(-26, -168), (0, -156), (26, -168)], 5), 2.2, peso=0.01)]


def _delantal(col=BLANCO_US):
    return forma(pol((-36, -110), (36, -110), (44, -14), (-44, -14)), col, 3.6, sp=5)


def _cinturon(col=CUERO_OSC, hebilla=LATON):
    return forma(rect(-54, -100, 54, -86, 3), col, 3.6, sp=3) + forma(rect(-10, -102, 10, -84, 2), hebilla, 3, sp=2)


_persona_kit = persona


def persona(ropa, piel=PIEL_A, sombrero_=None, cara="feliz", *a, **k):
    """persona() del kit + ojos reforzados en pieles morenas y oscuras (los puntos finos se perdían bajo el crayón)."""
    p = _persona_kit(ropa, piel, sombrero_, cara, *a, **k)
    if sum(piel) < 560 and cara in ("feliz", "normal", "serio", "enojo", "lloron"):
        ojos = []
        for x in (-15, 15):
            ojos += [R(circ(x, CY - 4, 6.0, n=12), BLANCO_US, peso=0.01, sp=2), R(circ(x, CY - 3, 3.8, n=10), (24, 20, 24), peso=0.01, sp=1.5),
                     T(circ(x, CY - 4, 6.0, n=12), 1.4, peso=0.01)]
        return _mas(p, ojos)
    return p


# ------------------------------------------------------------------ PERSONAJES: primeros pueblos
@lru_cache(maxsize=None)
def cazador_paleo(pose=0, cara="serio"):
    p = persona(GAMUZA, PIEL_NAT, "pelo_largo", cara, (20, 55), pose, traje="corta", faja=CUERO_OSC, acc_d="lanza_piedra")
    return _mas(p, [T(curva([(-46, -170), (-20, -120), (10, -170)], 5), 3, peso=0.02)], _flecos(-16, -46, 46, 8))


@lru_cache(maxsize=None)
def mujer_paleo(pose=0, cara="feliz"):
    p = persona((176, 136, 92), PIEL_NAT, "pelo_largo+cinta_pieles", cara, (24, 40), pose, traje="vestido", faja=CUERO_OSC)
    return _mas(p, _flecos(-16, -80, 80, 10), _collar((214, 196, 160), 5, 5))


@lru_cache(maxsize=None)
def jefe_cahokia(pose=0, cara="serio"):
    p = persona((168, 82, 58), PIEL_NAT, "plumas_halcon", cara, (24, 75), pose, traje="tunica", faja=CONCHA, acc_d="maza_cahokia")
    return _mas(p, _collar(CONCHA, 9, 6), [R(circ(0, -120, 14, n=14), CONCHA, peso=0.02, sp=3), T(circ(0, -120, 14, n=14), 3, peso=0.02)])


@lru_cache(maxsize=None)
def alfarero_pueblo(pose=0, cara="feliz"):
    p = persona((228, 214, 186), PIEL_NAT, "pelo_neg+cinta_pieles", cara, (22, 40), pose, traje="corta", faja=TERRACOTA, acc_d="vasija")
    return _mas(p, _collar(TURQUESA, 5, 5))


@lru_cache(maxsize=None)
def mujer_pueblo(pose=0, cara="feliz"):
    p = persona((48, 46, 54), PIEL_NAT, "rodetes", cara, (24, 50), pose, traje="vestido", faja=ROJO_US, cuello=(48, 46, 54))
    return _mas(p, _collar(TURQUESA, 5, 5), [R(pol((-56, -100), (56, -100), (60, -90), (-60, -90)), TURQUESA, peso=0.01, sp=2)])


@lru_cache(maxsize=None)
def sachem_iroques(pose=0, cara="serio"):
    p = persona((92, 128, 104), PIEL_NAT, "gustoweh", cara, (22, 70), pose, traje="tunica", faja=CUERO, acc_d="wampum")
    return _mas(p, _collar(CONCHA, 7, 5), _flecos(-14, -66, 66, 10))


# ------------------------------------------------------------------ colonias
@lru_cache(maxsize=None)
def menendez(pose=0, cara="serio"):
    p = persona((172, 60, 54), PIEL_A, "morrion", cara, (22, 80), pose, traje="armadura", faja=ORO_US, acc_d="estandarte_borgona", acc_i="espada_us")
    return _mas(p, _barba(PELO_NEG, 62), _bigote(PELO_NEG))


@lru_cache(maxsize=None)
def fraile_franciscano(pose=0, cara="feliz"):
    p = persona((132, 98, 70), PIEL_A, "tonsura", cara, (22, 60), pose, traje="tunica", acc_d="cruz")
    capucha = forma(curva([(-48, -172), (-30, -150), (0, -144), (30, -150), (48, -172)], 5), (118, 86, 60), 3.6, sp=4)
    return _mas(p, capucha, [T(curva([(-50, -96), (0, -88), (50, -96)], 5), 4.4, peso=0.02), T(linea((24, -92), (28, -40)), 3.6, peso=0.02)])


@lru_cache(maxsize=None)
def colono_jamestown(pose=0, cara="serio"):
    p = persona((112, 120, 96), PIEL_A, "pelo_cas+ala_ancha", cara, (22, 60), pose, traje="corta", faja=CUERO_OSC, cuello=BLANCO_US, acc_d="mosquete")
    return _mas(p, _barba(PELO_CAS, 54), _botones(LATON, 0, 3, -140, 20))


@lru_cache(maxsize=None)
def plantador_tabaco(pose=0, cara="feliz"):
    p = persona((150, 106, 72), PIEL_A, "pelo_cas+ala_ancha", cara, (22, 75), pose, traje="corta", faja=CUERO_OSC, cuello=BLANCO_US, acc_d="hojas_tabaco")
    return _mas(p, _botones(LATON, 0, 3, -140, 20))


@lru_cache(maxsize=None)
def africano_esclavizado(pose=0, cara="serio"):
    return persona((200, 186, 160), PIEL_C, "pelo_neg", cara, (18, 22), pose, traje="corta", faja=CUERO)


@lru_cache(maxsize=None)
def peregrino(pose=0, cara="serio"):
    p = persona(NEGRO_US, PIEL_A, "pelo_cas+capotain", cara, (22, 70), pose, traje="tunica", acc_d="libro_us")
    cuello = forma(pol((-44, -176), (44, -176), (36, -148), (0, -140), (-36, -148)), BLANCO_US, 3.6, sp=4)
    return _mas(p, cuello, _cinturon())


@lru_cache(maxsize=None)
def peregrina(pose=0, cara="feliz"):
    p = persona((92, 88, 96), PIEL_A, "cofia", cara, (24, 40), pose, traje="vestido")
    cuello = forma(pol((-44, -176), (44, -176), (36, -146), (0, -138), (-36, -146)), BLANCO_US, 3.6, sp=4)
    return _mas(p, _delantal(), cuello)


# ------------------------------------------------------------------ Revolución
@lru_cache(maxsize=None)
def rey_jorge(pose=0, cara="enojo"):
    manto = forma(pol((-62, -176), (62, -176), (96, -6), (-96, -6)), ROJO_US, 5, sp=8) + [R(pol((-96, -24), (96, -24), (98, -6), (-98, -6)), ARMINIO, peso=0.02, sp=3)]
    manto += [R(circ(-80 + 26 * k, -15, 3.5, n=6), NEGRO_US, peso=0.01, sp=1) for k in range(7)]
    p = persona((214, 196, 150), PIEL_A, "corona_jorge", cara, (22, 75), pose, traje="tunica", faja=AZUL_US, acc_d="cetro_us")
    armino = forma(pol((-50, -178), (50, -178), (44, -156), (-44, -156)), ARMINIO, 3.6, sp=4) + [R(circ(-30 + 20 * k, -167, 3.5, n=6), NEGRO_US, peso=0.01,
                                                                                                    sp=1) for k in range(4)]
    return _mas(_antes(p, manto), armino)


@lru_cache(maxsize=None)
def casaca_roja(pose=0, cara="enojo"):
    p = persona(ROJO_US, PIEL_A, "pelo_cas+tricornio", cara, (22, 55), pose, traje="corta", faja=BLANCO_US, acc_d="fusil_bay")
    return _mas(p, _correaje(), _botones(LATON, 0, 3, -150, 20))


@lru_cache(maxsize=None)
def miliciano(pose=0, cara="enojo"):
    p = persona(BLANCO_US, PIEL_A, "pelo_cas+tricornio", cara, (22, 55), pose, traje="corta", faja=CUERO_OSC, acc_d="mosquete")
    chaleco = [R(pol((-46, -170), (-12, -170), (-14, -40), (-50, -40)), CUERO, peso=0.02, sp=4), R(pol((46, -170), (12, -170), (14, -40), (50, -40)), CUERO, peso=0.02, sp=4)]
    return _mas(p, chaleco, [T(linea((-40, -172), (40, -60)), 4, peso=0.02)], forma(elip(40, -62, 14, 12, 0, 1.0, 12), (220, 206, 170), 3, sp=2))


@lru_cache(maxsize=None)
def soldado_continental(pose=0, cara="serio"):
    p = persona(AZUL_US, PIEL_A, "pelo_cas+tricornio_cont", cara, (22, 55), pose, traje="corta", faja=BEIGE_US, acc_d="fusil_bay")
    return _mas(p, _solapas(BEIGE_US), [T(linea((-40, -170), (40, -76)), 4, peso=0.02)])


@lru_cache(maxsize=None)
def jefferson(pose=0, cara="feliz"):
    p = persona((118, 74, 56), PIEL_A, "pelo_jefferson", cara, (26, 80), pose, traje="tunica", faja=None, cuello=BLANCO_US, acc_d="pluma_us", acc_i="pergamino")
    return _mas(p, _solapas((96, 58, 44)), forma(pol((-14, -176), (14, -176), (8, -150), (-8, -150)), BLANCO_US, 3, sp=3))


@lru_cache(maxsize=None)
def washington(pose=0, cara="serio"):
    p = persona(AZUL_US, PIEL_A, "peluca_blanca", cara, (22, 75), pose, traje="tunica", faja=BEIGE_US, cuello=BEIGE_US, acc_d="espada_us")
    return _mas(p, _solapas(BEIGE_US), _charreteras())


@lru_cache(maxsize=None)
def galvez(pose=0, cara="serio"):
    p = persona(BLANCO_US, PIEL_A, "peluca_blanca+tricornio_esp", cara, (22, 80), pose, traje="tunica", faja=ROJO_US, acc_d="espada_us")
    return _mas(p, _solapas(ROJO_US), _charreteras())


@lru_cache(maxsize=None)
def soldado_frances_rev(pose=0, cara="serio"):
    p = persona(BLANCO_US, PIEL_A, "peluca_blanca+tricornio_oro", cara, (22, 55), pose, traje="corta", faja=AZUL_US, acc_d="fusil_bay")
    return _mas(p, _solapas(AZUL_US))


# ------------------------------------------------------------------ república y oeste
@lru_cache(maxsize=None)
def napoleon(pose=0, cara="serio"):
    p = persona(AZUL_US, PIEL_A, "bicornio_lado", cara, (40, 18), pose, traje="tunica", faja=BLANCO_US, cuello=BLANCO_US)
    mano = forma(elip(8, -124, 14, 12, 0, 1.0, 12), PIEL_A, 3.6, sp=3)
    return _mas(p, _solapas(ROJO_US), _charreteras(), [T(linea((-16, -130), (20, -118)), 3, peso=0.02)], mano)


@lru_cache(maxsize=None)
def lewis(pose=0, cara="serio"):
    p = persona(GAMUZA, PIEL_A, "pelo_cas+mapache", cara, (22, 55), pose, traje="corta", faja=CUERO_OSC, acc_d="mosquete")
    return _mas(p, _flecos(-12, -48, 48, 8), [rayita(-46 + 4 * k, -150 + 14 * k, -56 + 4 * k, -146 + 14 * k, 2.2) for k in range(5)])


@lru_cache(maxsize=None)
def clark(pose=0, cara="feliz"):
    p = persona((118, 104, 72), PIEL_A, "sombrero_clark", cara, (26, 70), pose, traje="corta", faja=CUERO_OSC, acc_d="diario", acc_i="brujula_mano")
    return _mas(p, _flecos(-12, -48, 48, 8))


@lru_cache(maxsize=None)
def sacagawea(pose=0, cara="feliz"):
    cuna = forma(rect(40, -268, 98, -150, 10), MADERA_US, 4.2, sp=5) + forma(circ(69, -238, 20, n=18), PIEL_NAT, 3.8, sp=4)
    cuna += [punto(63, -240, 6), punto(75, -240, 6), T(arco_(69, -234, 7, 25, 155, 6), 2.6, peso=0.02)]
    cuna += forma(rect(46, -216, 92, -160, 6), (196, 84, 68), 3.4, sp=3)
    p = persona(GAMUZA, PIEL_NAT, "trenzas", cara, (24, 50), pose, traje="vestido", faja=TURQUESA)
    return _mas(_antes(p, cuna), _flecos(-14, -80, 80, 11), _collar(TURQUESA, 5, 4))


@lru_cache(maxsize=None)
def cherokee(pose=0, cara="serio"):
    chal = forma(pol((-56, -176), (56, -176), (64, -92), (0, -70), (-64, -92)), (196, 84, 68), 4.2, sp=6)
    chal += [T(ondas(-56, 56, -100, 4, 18), 2.4, peso=0.02)]
    p = persona((214, 196, 150), PIEL_NAT, "pelo_neg+turbante_cherokee", cara, (20, 26), pose, traje="tunica", faja=(56, 92, 140))
    return _mas(p, chal)


@lru_cache(maxsize=None)
def soldado_eeuu_1846(pose=0, cara="enojo"):
    p = persona(AZUL_OSC_US, PIEL_A, "chaco_us", cara, (22, 55), pose, traje="corta", faja=BLANCO_US, acc_d="fusil_bay")
    return _mas(p, _correaje(), _botones(LATON, 0, 3, -150, 20))


@lru_cache(maxsize=None)
def soldado_mexicano_1846(pose=0, cara="serio"):
    p = persona((48, 58, 104), PIEL_B, "chaco_mx", cara, (22, 55), pose, traje="corta", faja=ROJO_US, acc_d="fusil_bay")
    vivos = [R(pol((-46, -172), (-38, -172), (-38, -30), (-46, -30)), ROJO_US, peso=0.01, sp=2), R(pol((38, -172), (46, -172), (46, -30), (38, -30)), ROJO_US, peso=0.01, sp=2)]
    return _mas(p, vivos, _botones(LATON, 0, 3, -150, 20))


@lru_cache(maxsize=None)
def buscador_oro(pose=0, cara="feliz"):
    p = persona((176, 70, 60), PIEL_A, "sombrero_minero", cara, (22, 50), pose, traje="corta", faja=CUERO_OSC, acc_d="batea")
    tirantes = [T(linea((-24, -174), (-28, -14)), 4.4, peso=0.02), T(linea((24, -174), (28, -14)), 4.4, peso=0.02)]
    return _mas(p, tirantes, _barba(PELO_CAS, 66))


# ------------------------------------------------------------------ Guerra Civil
@lru_cache(maxsize=None)
def lincoln(pose=0, cara="serio"):
    p = persona(NEGRO_US, PIEL_A, "chistera_alta", cara, (18, 22), pose, traje="corta", alto=1.0)
    return _mas(p, _camisa_traje(BLANCO_US, NEGRO_US), _barba((92, 70, 58), 60))


@lru_cache(maxsize=None)
def soldado_union(pose=0, cara="serio"):
    p = persona(AZUL_US, PIEL_A, "kepi_azul", cara, (22, 55), pose, traje="corta", faja=NEGRO_US, acc_d="fusil_bay")
    return _mas(p, _botones(LATON, 0, 4, -152, 20), [T(linea((-40, -170), (40, -84)), 3.6, peso=0.02)])


@lru_cache(maxsize=None)
def soldado_confederado(pose=0, cara="serio"):
    p = persona(GRIS_CONF, PIEL_A, "kepi_gris", cara, (22, 55), pose, traje="corta", faja=NEGRO_US, acc_d="fusil_bay")
    return _mas(p, _botones(LATON, 0, 4, -152, 20), [T(linea((-40, -170), (40, -84)), 3.6, peso=0.02)], _barba(PELO_CAS, 54))


@lru_cache(maxsize=None)
def esclava_algodon(pose=0, cara="serio"):
    p = persona((196, 172, 140), PIEL_C, "panuelo", cara, (20, 40), pose, traje="vestido", faja=None, acc_d="saco_algodon")
    return _mas(p, _delantal((232, 224, 204)))


@lru_cache(maxsize=None)
def liberto(pose=0, cara="feliz"):
    return persona((206, 192, 160), PIEL_C, "pelo_neg", cara, (100, 100), pose, traje="corta", faja=CUERO, acc_d="cadena", acc_i="cadena")


# ------------------------------------------------------------------ industria
@lru_cache(maxsize=None)
def obrero_ferrocarril(pose=0, cara="feliz"):
    p = persona((92, 112, 150), PIEL_B, "gorra_obrero", cara, (22, 70), pose, traje="corta", faja=CUERO_OSC, acc_d="mazo")
    return _mas(p, [T(linea((-24, -174), (-28, -14)), 4.4, peso=0.02), T(linea((24, -174), (28, -14)), 4.4, peso=0.02)], _bigote(PELO_NEG))


@lru_cache(maxsize=None)
def carnegie(pose=0, cara="feliz"):
    p = persona(NEGRO_US, PIEL_A, "pelo_cano+chistera", cara, (22, 40), pose, traje="tunica", acc_d="baston")
    return _mas(p, _camisa_traje(BLANCO_US, NEGRO_US), _barba(PELO_CANO, 50), _bigote(PELO_CANO))


@lru_cache(maxsize=None)
def rockefeller(pose=0, cara="serio"):
    p = persona((60, 60, 70), PIEL_A, "calva_lados", cara, (22, 55), pose, traje="tunica", acc_d="bolsa_dinero_us")
    return _mas(p, _camisa_traje(BLANCO_US, GRIS_OSC_US), [T(arco_(34, -150, 10, 90, 270, 8), 2.6, peso=0.02)])


@lru_cache(maxsize=None)
def edison(pose=0, cara="feliz"):
    p = persona((70, 66, 74), PIEL_A, "pelo_cano", cara, (22, 100), pose, traje="tunica", acc_d="bombilla_mano")
    return _mas(p, _camisa_traje(BLANCO_US, NEGRO_US))


@lru_cache(maxsize=None)
def inmigrante(pose=0, cara="feliz"):
    p = persona((132, 112, 92), PIEL_A, "pelo_cas+gorra_gris", cara, (20, 18), pose, traje="corta", faja=CUERO_OSC, acc_d="maleta")
    return _mas(p, _bigote(PELO_CAS), _botones(GRIS_OSC_US, 0, 3, -140, 22))


@lru_cache(maxsize=None)
def inmigrante_mujer(pose=0, cara="feliz"):
    p = persona((112, 120, 140), PIEL_A, "panuelo", cara, (22, 55), pose, traje="vestido", acc_d="hatillo")
    return _mas(p, _delantal((220, 210, 190)))


@lru_cache(maxsize=None)
def rough_rider(pose=0, cara="feliz"):
    p = persona(CAQUI_US, PIEL_A, "sombrero_campana", cara, (22, 80), pose, traje="corta", faja=CUERO_OSC, cuello=AZUL_US, acc_d="espada_us")
    pañuelo = forma(pol((-20, -176), (20, -176), (0, -146)), AZUL_US, 3, sp=2)
    return _mas(p, pañuelo, _gafas(True), _bigote(PELO_CAS, 26), _botones(LATON, 0, 3, -140, 22))


@lru_cache(maxsize=None)
def hermano_wright(pose=0, cara="feliz"):
    p = persona((94, 84, 76), PIEL_A, "gorra_gris", cara, (22, 40), pose, traje="corta", faja=None)
    return _mas(p, _camisa_traje(BLANCO_US, NEGRO_US), _bigote(PELO_CAS, 20))


# ------------------------------------------------------------------ siglo XX
@lru_cache(maxsize=None)
def henry_ford(pose=0, cara="feliz"):
    p = persona((84, 86, 96), PIEL_A, "pelo_cano+fedora_gris", cara, (22, 70), pose, traje="tunica")
    return _mas(p, _camisa_traje(BLANCO_US, AZUL_OSC_US))


@lru_cache(maxsize=None)
def doughboy(pose=0, cara="serio"):
    p = persona(VERDE_OLIVA, PIEL_A, "casco_plato", cara, (22, 55), pose, traje="corta", faja=CUERO, acc_d="fusil_moderno")
    return _mas(p, _botones(LATON, 0, 3, -150, 22), [R(pol((-56, -40), (-44, -40), (-44, -6), (-56, -6)), VERDE_OLIVA, peso=0.01, sp=2)])


@lru_cache(maxsize=None)
def flapper(pose=0, cara="feliz"):
    p = persona((200, 92, 112), PIEL_A, "melena", cara, (60, 110), pose, traje="corta", faja=None)
    perlas = [R(circ(-22 + 44 * k / 8, -168 + 18 * math.sin(math.pi * k / 8), 4, n=8), BLANCO_US, peso=0.01, sp=2) for k in range(9)]
    perlas += [R(circ(0, -150 + 14 * k, 4, n=8), BLANCO_US, peso=0.01, sp=2) for k in range(4)]
    return _mas(p, [T(ondas(-50, 50, -30, 4, 16), 3, peso=0.02), T(ondas(-50, 50, -54, 4, 16), 3, peso=0.02)], perlas)


@lru_cache(maxsize=None)
def sufragista(pose=0, cara="feliz"):
    p = persona(BLANCO_US, PIEL_A, "sombrero_sufragista", cara, (22, 120), pose, traje="vestido", faja=VIOLETA, acc_d="cartel")
    banda = [R(pol((-46, -174), (-28, -174), (52, -70), (38, -60)), AMARILLO_SUF, peso=0.02, sp=3),
             T(pol((-46, -174), (-28, -174), (52, -70), (38, -60), (-46, -174)), 2.8, peso=0.02)]
    return _mas(p, banda)


@lru_cache(maxsize=None)
def musico_jazz(pose=0, cara="feliz"):
    p = persona((200, 188, 150), PIEL_C, "pelo_neg", cara, (40, 76), pose, traje="tunica", acc_d="trompeta")
    pajarita = forma(pol((-20, -176), (0, -168), (20, -176), (20, -160), (0, -168), (-20, -160)), ROJO_US, 3, sp=2)
    return _mas(p, _camisa_traje(BLANCO_US), pajarita)


@lru_cache(maxsize=None)
def corredor_bolsa(pose=0, cara="miedo"):
    p = persona((70, 72, 84), PIEL_A, "pelo_neg", cara, (120, 125), pose, traje="tunica", acc_d="papeles", acc_i="papeles")
    return _mas(p, _camisa_traje(BLANCO_US, ROJO_US))


@lru_cache(maxsize=None)
def desempleado(pose=0, cara="lloron"):
    p = persona((120, 110, 96), PIEL_A, "pelo_cas+gorra_obrero", cara, (18, 30), pose, traje="corta", faja=None, acc_d="cartel")
    remiendo = forma(rect(-30, -90, -10, -66, 2), (168, 140, 100), 2.8, sp=2)
    return _mas(p, remiendo, [T(linea((-24, -174), (-28, -14)), 4, peso=0.02), T(linea((24, -174), (28, -14)), 4, peso=0.02)])


@lru_cache(maxsize=None)
def fdr(pose=0, cara="feliz"):
    p = persona((90, 92, 104), PIEL_A, "pelo_cano+fedora_gris", cara, (22, 60), pose, traje="tunica")
    boquilla = [T(linea((10, CY + 18), (58, CY - 6)), 3.4, peso=0.02), R(pol((54, CY - 4), (72, CY - 13), (74, CY - 8), (56, CY + 1)), BLANCO_US, peso=0.01, sp=2),
                T(curva([(76, CY - 16), (80, CY - 30), (74, CY - 44), (80, CY - 58)], 4), 2.2, peso=0.01)]
    return _mas(p, _camisa_traje(BLANCO_US, AZUL_OSC_US), _gafas(False), boquilla)


@lru_cache(maxsize=None)
def soldado_ww2(pose=0, cara="serio"):
    p = persona(VERDE_OLIVA, PIEL_A, "casco_m1", cara, (22, 55), pose, traje="corta", faja=(150, 134, 92), acc_d="fusil_moderno")
    return _mas(p, _botones(CUERO_OSC, 0, 3, -150, 22), [R(rect(-44, -150, -20, -126, 2), (104, 108, 66), peso=0.01, sp=2)])


@lru_cache(maxsize=None)
def marinero(pose=0, cara="feliz"):
    p = persona(BLANCO_US, PIEL_A, "gorro_marinero", cara, (22, 40), pose, traje="corta", faja=None)
    cuello = forma(pol((-46, -176), (46, -176), (40, -136), (0, -124), (-40, -136)), AZUL_OSC_US, 3.6, sp=4)
    return _mas(p, cuello, forma(pol((-10, -130), (10, -130), (0, -100)), NEGRO_US, 2.8, sp=2))


@lru_cache(maxsize=None)
def soldado_sovietico(pose=0, cara="serio"):
    p = persona((126, 122, 96), PIEL_A, "ushanka", cara, (22, 55), pose, traje="corta", faja=CUERO_OSC, acc_d="fusil_moderno")
    return _mas(p, _botones(LATON, 0, 3, -150, 22))


@lru_cache(maxsize=None)
def kennedy(pose=0, cara="feliz"):
    p = persona((64, 70, 92), PIEL_A, "tupe", cara, (22, 40), pose, traje="tunica")
    return _mas(p, _camisa_traje(BLANCO_US, AZUL_OSC_US))


@lru_cache(maxsize=None)
def lider_sovietico(pose=0, cara="enojo"):
    p = persona((70, 70, 76), PIEL_A, "calva_lados", cara, (22, 60), pose, traje="tunica")
    medallas = [R(circ(-30 + 10 * k, -144, 5, n=8), (ORO_US if k % 2 == 0 else ROJO_US), peso=0.01, sp=2) for k in range(3)]
    return _mas(p, _camisa_traje(BLANCO_US, GRIS_OSC_US), medallas)


@lru_cache(maxsize=None)
def astronauta(pose=0, cara="feliz"):
    mochila = forma(rect(-66, -196, 66, -66, 12), (214, 214, 210), 4.6, sp=6)
    p = persona(BLANCO_US, PIEL_A, "casco_astronauta", cara, (26, 70), pose, traje="corta", faja=GRIS_OSC_US, acc_d="banderita")
    parche = [R(pol((-38, -150), (-18, -150), (-18, -136), (-38, -136)), AZUL_US, peso=0.01, sp=2), R(pol((-38, -136), (-18, -136), (-18, -128), (-38, -128)),
                                                                                                      ROJO_US, peso=0.01, sp=2)]
    return _mas(_antes(p, mochila), parche, forma(rect(-14, -146, 22, -116, 3), GRIS_OSC_US, 3, sp=2))


@lru_cache(maxsize=None)
def rockero(pose=0, cara="guiño"):
    p = persona((60, 56, 64), PIEL_A, "tupe_negro", cara, (30, 50), pose, traje="corta", faja=None, acc_d="guitarra")
    return _mas(p, [R(pol((-18, -176), (18, -176), (0, -150)), BLANCO_US, peso=0.02, sp=2)])


@lru_cache(maxsize=None)
def rosa_parks(pose=0, cara="serio"):
    p = persona((96, 116, 104), PIEL_C, "sombrerito", cara, (20, 26), pose, traje="vestido", cuello=BLANCO_US, acc_d="bolso")
    return _mas(p, _gafas(True), _botones(NEGRO_US, 0, 4, -150, 22))


@lru_cache(maxsize=None)
def mlk(pose=0, cara="feliz"):
    p = persona((58, 60, 70), PIEL_C, "pelo_neg", cara, (20, 165), pose, traje="tunica")
    return _mas(p, _camisa_traje(BLANCO_US, NEGRO_US), _bigote(PELO_NEG, 18))


@lru_cache(maxsize=None)
def manifestante(pose=0, cara="feliz"):
    return persona((208, 196, 172), PIEL_B, "pelo_neg", cara, (22, 125), pose, traje="corta", faja=CUERO, acc_d="cartel")


@lru_cache(maxsize=None)
def programador(pose=0, cara="feliz"):
    p = persona((96, 120, 150), PIEL_B, "pelo_neg", cara, (60, 64), pose, traje="corta", acc_d="portatil")
    capucha = forma(curva([(-46, -176), (-30, -158), (0, -152), (30, -158), (46, -176)], 5), (80, 102, 130), 3.6, sp=4)
    return _mas(p, capucha, [T(linea((-10, -158), (-12, -126)), 2.6, peso=0.02), T(linea((10, -158), (12, -126)), 2.6, peso=0.02)],
                forma(rect(-30, -70, 30, -40, 4), (80, 102, 130), 3, sp=2))


@lru_cache(maxsize=None)
def bombero(pose=0, cara="serio"):
    p = persona((70, 66, 58), PIEL_A, "casco_bombero", cara, (22, 60), pose, traje="corta", faja=None, acc_d="hacha")
    bandas = [R(pol((-52, -60), (52, -60), (52, -48), (-52, -48)), (230, 210, 90), peso=0.01, sp=2), R(pol((-50, -130), (50, -130), (50, -118), (-50, -118)),
                                                                                                         (230, 210, 90), peso=0.01, sp=2)]
    return _mas(p, bandas)


@lru_cache(maxsize=None)
def obama(pose=0, cara="feliz"):
    p = persona((52, 58, 76), PIEL_C, "pelo_neg", cara, (22, 95), pose, traje="tunica")
    pin = [R(circ(-30, -146, 5, n=8), ROJO_US, peso=0.01, sp=2)]
    return _mas(p, _camisa_traje(BLANCO_US, AZUL_US), pin)


@lru_cache(maxsize=None)
def ciudadana_hispana(pose=0, cara="feliz"):
    p = persona((228, 120, 70), PIEL_B, "rizos_flor", cara, (24, 120), pose, traje="vestido", faja=TURQUESA)
    return _mas(p, [T(ondas(-80, 80, -30, 4, 18), 3, peso=0.02)], _collar(ORO_US, 5, 4))


@lru_cache(maxsize=None)
def ciudadano_hoy(pose=0, cara="feliz"):
    p = persona((96, 132, 176), PIEL_B, "pelo_neg", cara, (22, 80), pose, traje="corta", faja=None, acc_d="banderita")
    return _mas(p, [R(pol((-18, -176), (18, -176), (0, -152)), BLANCO_US, peso=0.02, sp=2)])
