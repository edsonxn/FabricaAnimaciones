# -*- coding: utf-8 -*-
"""Dibujos de boceto para «La historia de Egipto» (v2) 1/3: paleta egipcia, tocados y coronas para `persona`
(nemes, corona blanca, roja y doble, khepresh, corona de Nefertiti, corona de buitre…), accesorios (cayado y flagelo, anj, khopesh,
arco, cetro uas…) y los PERSONAJES de cinco mil años: campesinos, escribas, faraones, reinas, hicsos, hititas, Pueblos del Mar,
nubios, asirios, persas, griegos, romanos, árabes, cruzados, mamelucos, mongoles, franceses, británicos y egipcios de hoy.
Convenciones de obj_base: origen en los PIES, cabeza en y ≈ -215 (radio 41). `pose` 0..3 = ciclo de paso."""
import math
from functools import lru_cache

import numpy as np

import obj_base as OB
from obj_a import colocar
from obj_base import *  # noqa: F401,F403

# ------------------------------------------------------------------ paleta egipcia (pigmentos minerales, apagados como el guache)
ORO_EG = (236, 186, 60)
ORO_OS = (190, 140, 40)
LAPIS = (52, 86, 160)
TURQ = (70, 168, 168)
OCRE_R = (192, 70, 52)
LINO = (246, 242, 228)
KOHL = (46, 40, 46)
PIEL_EG = (206, 140, 96)
PIEL_EG_F = (232, 178, 136)
PIEL_NUB = (122, 80, 58)
PIEL_ASIA = (214, 160, 116)
PIEL_EU = (242, 200, 168)
CALIZA = (238, 230, 210)
ARENISCA = (222, 196, 150)
ARENISCA_OS = (190, 160, 116)
GRANITO = (180, 128, 118)
VERDE_NILO = (110, 160, 96)
LEOPARDO = (222, 170, 90)
BRONCE = (190, 140, 70)
HIERRO = (150, 154, 164)
ROJO_R = (186, 52, 46)
PURPURA = (120, 60, 110)
AZUL_FR = (60, 82, 150)
ROJO_UK = (190, 50, 50)
CAQUI = (190, 172, 120)
NEGRO_EG = (52, 46, 52)
BLANCO_EG = (250, 246, 236)


# ------------------------------------------------------------------ tocados y coronas
_orig_sombrero = OB.sombrero


def _uraeus(cy, x=0.0):
    """Cobra erguida en la frente."""
    return [T(curva([(x, cy - 44), (x - 6, cy - 62), (x + 4, cy - 74), (x + 10, cy - 66)], 5), 4.2, peso=0.04),
            R(elip(x + 6, cy - 70, 7, 6, n=10), ORO_EG, peso=0.02, sp=3)]


def _sombrero(nombre, cy=-215.0):
    if nombre == "nemes":            # paño real a rayas azul y oro con alas sobre los hombros y uraeus
        ops = forma(curva([(-48, cy + 20), (-56, cy - 30), (-40, cy - 66), (0, cy - 78), (40, cy - 66), (56, cy - 30), (48, cy + 20),
                           (36, cy - 18), (0, cy - 40), (-36, cy - 18)], 5), ORO_EG, 4.8, sp=7)
        ops += forma(pol((-48, cy + 4), (-62, cy + 70), (-36, cy + 74), (-36, cy + 2)), ORO_EG, 4.4, sp=6)
        ops += forma(pol((48, cy + 4), (62, cy + 70), (36, cy + 74), (36, cy + 2)), ORO_EG, 4.4, sp=6)
        for k in range(4):
            y = cy - 62 + 14 * k
            ops.append(R(curva([(-44 + 4 * k, y), (0, y - 10 + 2 * k), (44 - 4 * k, y)], 5).tolist() + [(44 - 4 * k, y + 6), (0, y - 4 + 2 * k), (-44 + 4 * k, y + 6)],
                         LAPIS, peso=0.03, sp=4))
        for s_ in (-1, 1):
            for k in range(4):
                y = cy + 14 + 14 * k
                ops.append(R(pol((s_ * 37, y), (s_ * 58, y + 2), (s_ * 59, y + 8), (s_ * 37, y + 6)), LAPIS, peso=0.02, sp=3))
        return ops + _uraeus(cy)
    if nombre == "hedjet":           # corona blanca del Alto Egipto (bolo alto)
        P = curva([(-34, cy - 24), (-30, cy - 70), (-24, cy - 112), (-12, cy - 142), (0, cy - 150), (12, cy - 142), (24, cy - 112), (30, cy - 70),
                   (34, cy - 24)], 6)
        return forma(np.vstack([P, [(0, cy - 30)]]), LINO, 4.8, sp=8) + [R(elip(0, cy - 150, 9, 9, n=10), LINO, peso=0.02, sp=3)] + _uraeus(cy)
    if nombre == "deshret":          # corona roja del Bajo Egipto (con la espiral)
        ops = forma(pol((-38, cy - 20), (-40, cy - 70), (26, cy - 70), (26, cy - 120), (40, cy - 122), (40, cy - 20)), OCRE_R, 4.8, sp=8)
        ops.append(T(curva([(-10, cy - 70), (-30, cy - 96), (-44, cy - 112), (-38, cy - 124), (-26, cy - 118)], 6), 4.6, peso=0.05))
        return ops + _uraeus(cy)
    if nombre == "pschent":          # doble corona: la blanca dentro de la roja
        ops = forma(curva([(-22, cy - 66), (-20, cy - 104), (-10, cy - 132), (0, cy - 140), (10, cy - 132), (20, cy - 104), (22, cy - 66)], 6), LINO, 4.6, sp=7)
        ops += forma(pol((-40, cy - 20), (-42, cy - 72), (-20, cy - 72), (-16, cy - 60), (16, cy - 60), (20, cy - 72), (30, cy - 72), (30, cy - 118),
                         (42, cy - 120), (42, cy - 20)), OCRE_R, 4.8, sp=8)
        ops.append(T(curva([(-22, cy - 64), (-38, cy - 92), (-50, cy - 104), (-44, cy - 116)], 6), 4.4, peso=0.05))
        return ops + _uraeus(cy)
    if nombre == "khepresh":         # corona azul de guerra con discos de oro
        ops = forma(curva([(-46, cy - 6), (-50, cy - 50), (-40, cy - 92), (-10, cy - 116), (28, cy - 112), (50, cy - 86), (50, cy - 40), (46, cy - 6),
                           (30, cy - 20), (-30, cy - 20)], 6), LAPIS, 4.8, sp=8)
        ops += [R(circ(x, y, 4.5, n=8), ORO_EG, peso=0.02, sp=3) for x, y in ((-30, cy - 50), (-14, cy - 70), (6, cy - 86), (24, cy - 66), (-6, cy - 46),
                                                                              (16, cy - 40), (34, cy - 46), (-28, cy - 78), (12, cy - 102))]
        return ops + forma(rect(-48, cy - 26, 48, cy - 16, 4), ORO_EG, 3.8, sp=5) + _uraeus(cy)
    if nombre == "nefertiti":        # corona alta de lados rectos, azul, con cinta dorada
        ops = forma(pol((-36, cy - 22), (-54, cy - 132), (48, cy - 142), (40, cy - 22)), LAPIS, 4.8, sp=8)
        ops += forma(pol((-42, cy - 56), (44, cy - 60), (45, cy - 48), (-40, cy - 44)), ORO_EG, 3.8, sp=5)
        ops += [R(circ(-20 + 20 * k, cy - 52, 4, n=8), (200, 70, 60) if k == 1 else TURQ, peso=0.02, sp=3) for k in range(3)]
        return ops + _uraeus(cy, 0)
    if nombre == "buitre":           # corona de buitre con cuernos y disco solar (reinas, Cleopatra)
        ops = forma(curva([(-48, cy + 24), (-54, cy - 26), (-36, cy - 62), (0, cy - 72), (36, cy - 62), (54, cy - 26), (48, cy + 24), (34, cy - 16),
                           (0, cy - 34), (-34, cy - 16)], 5), ORO_EG, 4.6, sp=7)
        ops += [T(curva([(-46, cy - 20), (-20, cy - 44), (20, cy - 44), (46, cy - 20)], 5), 3.0, peso=0.03)]
        ops += forma(rect(-30, cy - 92, 30, cy - 70, 5), ORO_EG, 4.2, sp=5)
        ops += [T(curva([(-30, cy - 90), (-56, cy - 112), (-50, cy - 150), (-30, cy - 168)], 6), 5.2, peso=0.05),
                T(curva([(30, cy - 90), (56, cy - 112), (50, cy - 150), (30, cy - 168)], 6), 5.2, peso=0.05)]
        ops += forma(elip(0, cy - 128, 30, 30, 0, 1.0, 24), (222, 90, 60), 4.6, sp=6)
        return ops + _uraeus(cy)
    if nombre == "peluca":           # peluca negra corta (nobles, escribas)
        P = curva([(-50, cy + 30), (-54, cy - 20), (-40, cy - 54), (0, cy - 64), (40, cy - 54), (54, cy - 20), (50, cy + 30), (36, cy + 28), (38, cy - 12),
                   (0, cy - 30), (-38, cy - 12), (-36, cy + 28)], 5)
        return forma(P, KOHL, 4.6, sp=7) + [R(rect(-44, cy - 34, 44, cy - 26, 2), ORO_EG, peso=0.02, sp=3)]
    if nombre == "peluca_larga":     # peluca larga de trenzas (damas)
        P = curva([(-52, cy + 70), (-56, cy - 20), (-40, cy - 56), (0, cy - 66), (40, cy - 56), (56, cy - 20), (52, cy + 70), (36, cy + 70), (38, cy - 10),
                   (0, cy - 30), (-38, cy - 10), (-36, cy + 70)], 5)
        return forma(P, KOHL, 4.6, sp=7) + [R(rect(-46, cy - 34, 46, cy - 26, 2), TURQ, peso=0.02, sp=3)]
    if nombre == "gorro_sabio":      # casquete de Imhotep
        return forma(curva([(-42, cy - 14), (-40, cy - 48), (0, cy - 60), (40, cy - 48), (42, cy - 14), (0, cy - 26)], 5), (120, 110, 100), 4.6, sp=7)
    if nombre == "hicso":            # melena de seta con cinta (asiáticos del bronce)
        P = curva([(-50, cy + 16), (-58, cy - 24), (-44, cy - 60), (0, cy - 70), (44, cy - 60), (58, cy - 24), (50, cy + 16), (36, cy - 4), (0, cy - 26),
                   (-36, cy - 4)], 5)
        return forma(P, (60, 44, 40), 4.6, sp=7) + forma(rect(-50, cy - 36, 50, cy - 26, 3), (200, 70, 60), 3.8, sp=5)
    if nombre == "hitita":           # gorro alto y puntiagudo de rey hitita
        return forma(pol((-36, cy - 22), (-20, cy - 120), (0, cy - 146), (16, cy - 122), (36, cy - 22)), (150, 130, 190), 4.8, sp=8) + \
            [T(linea((-30, cy - 48), (30, cy - 48)), 3.6, peso=0.03), T(linea((-24, cy - 80), (24, cy - 80)), 3.2, peso=0.03)]
    if nombre == "casco_hitita":     # casco con cola de crin
        ops = forma(curva([(-44, cy - 8), (-42, cy - 54), (0, cy - 72), (42, cy - 54), (44, cy - 8)], 5), BRONCE, 4.6, sp=8)
        return ops + [T(curva([(0, cy - 72), (-26, cy - 70), (-56, cy - 40), (-66, cy + 6)], 6), 6, peso=0.06)]
    if nombre == "plumas":           # tocado de plumas de los peleset (Pueblos del Mar)
        ops = forma(rect(-46, cy - 40, 46, cy - 24, 4), (90, 120, 170), 4.2, sp=5)
        for k in range(9):
            x = -40 + 10 * k
            ops += forma(pol((x - 5, cy - 38), (x - 2, cy - 104 + abs(k - 4) * 4), (x + 5, cy - 38)), (232, 222, 196), 3.2, sp=3)
        return ops
    if nombre == "cuernos":          # casco con cuernos y disco (sherden)
        ops = forma(curva([(-46, cy - 6), (-44, cy - 54), (0, cy - 70), (44, cy - 54), (46, cy - 6)], 5), BRONCE, 4.6, sp=8)
        ops += [T(curva([(-36, cy - 52), (-64, cy - 70), (-74, cy - 104)], 5), 7, peso=0.05), T(curva([(36, cy - 52), (64, cy - 70), (74, cy - 104)], 5), 7, peso=0.05)]
        return ops + forma(elip(0, cy - 82, 10, 10, 0, 1.0, 12), ORO_EG, 3.6, sp=3)
    if nombre == "kushita":          # casquete ceñido con doble uraeus (faraones nubios)
        ops = forma(curva([(-44, cy - 10), (-42, cy - 50), (0, cy - 62), (42, cy - 50), (44, cy - 10), (0, cy - 24)], 5), KOHL, 4.6, sp=7)
        ops += forma(rect(-46, cy - 26, 46, cy - 16, 3), ORO_EG, 3.6, sp=4)
        return ops + _uraeus(cy, -10) + _uraeus(cy, 12)
    if nombre == "asirio":           # casco cónico
        ops = forma(pol((-42, cy - 14), (-30, cy - 60), (0, cy - 104), (30, cy - 60), (42, cy - 14)), HIERRO, 4.8, sp=8)
        return ops + [T(linea((-38, cy - 26), (38, cy - 26)), 3.6, peso=0.03)]
    if nombre == "laurel_r":         # corona de laurel (Roma)
        ops = []
        for lado in (-1, 1):
            for k in range(5):
                a = math.radians(200 + 32 * k) if lado < 0 else math.radians(-20 - 32 * k)
                x, y = 42 * math.cos(a), cy - 18 + 26 * math.sin(a)
                ops += forma(elip(x, y, 13, 6, a + lado * 1.2, 1.0, 12), (110, 150, 80), 3.4, sp=4)
        return forma(elip(0, cy - 14, 43, 38, math.pi, 0.5, 26), (90, 70, 56), 4.4, cerrada=False, sp=7)[1:] + ops
    if nombre == "galea_r":          # casco de legionario con cresta
        ops = forma([(-46, cy - 6), (-44, cy - 50), (0, cy - 70), (44, cy - 50), (46, cy - 6), (34, cy - 18), (-34, cy - 18)], HIERRO, 4.6, sp=8)
        ops += forma(pol((-46, cy - 14), (-56, cy + 2), (-44, cy + 28), (-32, cy + 6)), HIERRO, 4, sp=6)
        ops += forma(pol((46, cy - 14), (56, cy + 2), (44, cy + 28), (32, cy + 6)), HIERRO, 4, sp=6)
        ops += forma(curva([(-30, cy - 64), (-18, cy - 102), (22, cy - 104), (34, cy - 66)], 6).tolist() + [(0, cy - 72)], ROJO_R, 4.2, sp=6)
        return ops
    if nombre == "macedonio":        # casco frigio con cresta (Alejandro)
        ops = forma(curva([(-44, cy - 6), (-46, cy - 50), (-20, cy - 80), (24, cy - 92), (36, cy - 74), (20, cy - 62), (44, cy - 46), (44, cy - 6),
                           (30, cy - 18), (-30, cy - 18)], 5), ORO_EG, 4.6, sp=8)
        ops += forma(curva([(-36, cy - 70), (-10, cy - 128), (30, cy - 124), (40, cy - 98), (10, cy - 84)], 5), (240, 236, 224), 4, sp=5)
        return ops
    if nombre == "turbante_eg":      # turbante blanco con remate
        P = curva([(-48, cy - 10), (-58, cy - 40), (-48, cy - 72), (-16, cy - 88), (18, cy - 88), (48, cy - 72), (58, cy - 40), (48, cy - 10), (0, cy - 22)], 6)
        ops = forma(P, LINO, 4.6, sp=7)
        for k in range(3):
            ops.append(T(curva([(-52 + 8 * k, cy - 24 - 16 * k), (0, cy - 42 - 14 * k), (52 - 10 * k, cy - 58 - 10 * k)], 5), 2.8, peso=0.03))
        return ops
    if nombre == "turbante_verde":
        P = curva([(-48, cy - 10), (-58, cy - 40), (-48, cy - 72), (-16, cy - 88), (18, cy - 88), (48, cy - 72), (58, cy - 40), (48, cy - 10), (0, cy - 22)], 6)
        ops = forma(P, LINO, 4.6, sp=7) + forma(elip(0, cy - 74, 26, 22, 0, 1.0, 18), (70, 130, 90), 4, sp=5)
        return ops + [T(curva([(-50, cy - 30), (0, cy - 48), (50, cy - 30)], 5), 2.8, peso=0.03)]
    if nombre == "saladino":         # casco con turbante amarillo y punta
        ops = forma(curva([(-50, cy - 10), (-58, cy - 40), (-48, cy - 66), (0, cy - 76), (48, cy - 66), (58, cy - 40), (50, cy - 10), (0, cy - 22)], 6),
                    (232, 196, 90), 4.6, sp=7)
        ops += forma(pol((-22, cy - 70), (0, cy - 120), (22, cy - 70)), HIERRO, 4.2, sp=5)
        return ops + [T(curva([(-52, cy - 30), (0, cy - 48), (52, cy - 30)], 5), 2.8, peso=0.03)]
    if nombre == "mameluco":         # casco con penacho rojo envuelto en tela
        ops = forma(curva([(-46, cy - 8), (-48, cy - 50), (0, cy - 80), (48, cy - 50), (46, cy - 8)], 5), HIERRO, 4.6, sp=8)
        ops += forma(rect(-50, cy - 30, 50, cy - 14, 6), (230, 220, 200), 4, sp=5)
        return ops + [T(linea((0, cy - 80), (0, cy - 110)), 4.4, peso=0.03), R(elip(0, cy - 114, 8, 10, n=10), (200, 60, 50), peso=0.02, sp=3)]
    if nombre == "cruzado":          # yelmo cilíndrico
        ops = forma(rect(-42, cy - 70, 42, cy + 24, 10), HIERRO, 4.8, sp=8)
        return ops + [T(linea((-34, cy - 10), (34, cy - 10)), 4, peso=0.03), T(linea((0, cy - 10), (0, cy + 20)), 4, peso=0.03)] + \
            [R(rect(-36, cy - 14, 36, cy - 6, 2), KOHL, peso=0.02, sp=3)]
    if nombre == "mongol":           # gorro de piel con orejeras
        ops = forma(curva([(-46, cy - 10), (-44, cy - 56), (0, cy - 76), (44, cy - 56), (46, cy - 10)], 5), (150, 70, 60), 4.6, sp=8)
        ops += forma(rect(-52, cy - 30, 52, cy - 10, 8), (180, 150, 110), 4.2, sp=6)
        return ops + [R(circ(0, cy - 80, 6, n=10), (200, 60, 50), peso=0.02, sp=3)]
    if nombre == "bicornio":         # sombrero de Napoleón
        ops = forma(curva([(-80, cy - 30), (-50, cy - 74), (0, cy - 94), (50, cy - 74), (80, cy - 30), (40, cy - 44), (0, cy - 50), (-40, cy - 44)], 6),
                    NEGRO_EG, 4.8, sp=8)
        return ops + forma(elip(30, cy - 60, 9, 9, 0, 1.0, 12), (60, 90, 170), 3.4, sp=3) + [R(elip(30, cy - 60, 4, 4, n=8), (200, 60, 50), peso=0.02, sp=2)]
    if nombre == "chaco":            # chacó de soldado francés
        ops = forma(rect(-34, cy - 104, 34, cy - 30, 4), NEGRO_EG, 4.6, sp=8) + forma(rect(-42, cy - 34, 42, cy - 22, 3), NEGRO_EG, 4, sp=5)
        return ops + forma(elip(0, cy - 114, 8, 14, 0, 1.0, 12), (200, 60, 50), 3.4, sp=3) + [R(rect(-34, cy - 100, 34, cy - 92, 2), (230, 230, 220), peso=0.02, sp=3)]
    if nombre == "salacot":          # casco colonial británico
        ops = forma(curva([(-62, cy - 20), (-46, cy - 62), (0, cy - 82), (46, cy - 62), (62, cy - 20), (0, cy - 30)], 6), (236, 228, 200), 4.6, sp=8)
        return ops + [T(curva([(-56, cy - 26), (0, cy - 40), (56, cy - 26)], 5), 3.2, peso=0.03), R(circ(0, cy - 84, 5, n=8), (200, 190, 160), peso=0.02, sp=3)]
    if nombre == "fez":              # tarbush rojo con borla
        ops = forma(pol((-34, cy - 26), (-28, cy - 86), (28, cy - 86), (34, cy - 26)), (196, 52, 48), 4.6, sp=7)
        return ops + [T(curva([(4, cy - 86), (20, cy - 80), (30, cy - 60), (32, cy - 44)], 5), 3.6, peso=0.03)]
    if nombre == "casco_obra":       # casco de obra
        ops = forma(curva([(-50, cy - 14), (-46, cy - 54), (0, cy - 74), (46, cy - 54), (50, cy - 14)], 5), (240, 196, 60), 4.6, sp=8)
        return ops + forma(rect(-58, cy - 22, 58, cy - 12, 3), (240, 196, 60), 4, sp=5) + [T(linea((0, cy - 74), (0, cy - 22)), 3.2, peso=0.02)]
    if nombre == "gorra_of":         # gorra de oficial (1952)
        ops = forma(rect(-46, cy - 60, 46, cy - 32, 10), (150, 140, 108), 4.6, sp=8)
        ops += forma(rect(-50, cy - 36, 50, cy - 24, 4), (90, 84, 66), 4.2, sp=6)
        return ops + [R(circ(0, cy - 48, 8, n=12), ORO_EG, peso=0.02, sp=4)]
    if nombre == "rizos":            # pelo corto rizado
        ops = []
        for k in range(9):
            a = math.radians(200 + 17.5 * k)
            ops += forma(elip(40 * math.cos(a), cy - 8 + 36 * math.sin(a), 13, 11, 0, 1.0, 12), (70, 50, 40), 3.4, sp=4)
        return ops
    if nombre == "velo":             # pañuelo (mujer de hoy)
        P = curva([(-52, cy + 40), (-56, cy - 20), (-38, cy - 58), (0, cy - 66), (38, cy - 58), (56, cy - 20), (52, cy + 40), (36, cy + 30), (38, cy - 18),
                   (0, cy - 40), (-38, cy - 18), (-36, cy + 30)], 5)
        return forma(P, (110, 150, 180), 4.6, sp=7)
    if nombre == "gorra_beis":
        return forma(curva([(-44, cy - 20), (-42, cy - 56), (0, cy - 66), (42, cy - 56), (44, cy - 20)], 5), (226, 210, 170), 4.4, sp=6) + \
            forma(pol((10, cy - 26), (76, cy - 22), (70, cy - 12), (10, cy - 14)), (226, 210, 170), 4, sp=4)
    if nombre in ("pelo", "pelo_negro", "diadema"):   # casquete de pelo corto (el del kit tapaba los ojos)
        col = (60, 46, 42) if nombre == "pelo_negro" else (104, 74, 54)
        P = arco_(0, cy, 44, 180, 360, 18).tolist() + [(44, cy + 4), (34, cy - 12), (16, cy - 22), (0, cy - 20), (-16, cy - 24), (-34, cy - 12), (-44, cy + 4)]
        ops = forma(np.array(P), col, 4.6, sp=6)
        if nombre == "diadema":
            ops += forma(pol((-44, cy - 24), (44, cy - 24), (44, cy - 14), (-44, cy - 14)), BLANCO_EG, 3.6, sp=4)
            ops += [T(curva([(42, cy - 18), (58, cy + 6), (54, cy + 34)], 4), 4.2, peso=0.03), T(curva([(40, cy - 16), (64, cy + 2), (66, cy + 26)], 4), 3.6, peso=0.03)]
        return ops
    return _orig_sombrero(nombre, cy)


OB.sombrero = _sombrero


# ------------------------------------------------------------------ accesorios (en la mano)
def _acc_cayado(m, d):
    x, y = m
    return [T(curva([(x, y + 40), (x + 2, y - 70), (x + 4, y - 96), (x + 18, y - 110), (x + 30, y - 98)], 6), 6, peso=0.08),
            R(pol((x - 3, y - 60), (x + 3, y - 60), (x + 4, y - 50), (x - 3, y - 50)), LAPIS, peso=0.02, sp=3)]


def _acc_flagelo(m, d):
    x, y = m
    ops = [T(linea((x, y + 10), (x - 10, y - 50)), 5.4, peso=0.05)]
    for k in range(3):
        ops.append(T(curva([(x - 10, y - 50), (x - 30 - 6 * k, y - 44 + 10 * k), (x - 40 - 6 * k, y - 20 + 12 * k)], 4), 4, peso=0.03))
    return ops + [R(elip(x - 6, y - 26, 6, 10, n=10), ORO_EG, peso=0.02, sp=3)]


def _acc_anj(m, d):
    x, y = m
    ops = forma(elip(x, y - 60, 14, 18, 0, 1.0, 16), None, 6)
    return ops + [T(linea((x, y - 42), (x, y + 20)), 7, peso=0.04), T(linea((x - 24, y - 38), (x + 24, y - 38)), 7, peso=0.04)] + \
        [R(rect(x - 4, y - 42, x + 4, y + 18, 2), ORO_EG, peso=0.02, sp=3)]


def _acc_uas(m, d):
    x, y = m
    return [T(linea((x, y + 90), (x + 2, y - 120)), 5.4, peso=0.1), T(curva([(x + 2, y - 120), (x + 16, y - 128), (x + 24, y - 118)], 4), 5.4, peso=0.03),
            T(curva([(x, y + 90), (x - 8, y + 100), (x + 8, y + 104)], 3), 4.4, peso=0.02)]


def _acc_khopesh(m, d):
    x, y = m
    hoja = curva([(x + 4, y - 18), (x + 8, y - 60), (x + 30, y - 92), (x + 58, y - 98), (x + 50, y - 84), (x + 26, y - 74), (x + 16, y - 46), (x + 12, y - 18)], 6)
    return forma(hoja, (176, 180, 186), 4.4, sp=4) + [T(linea((x, y + 12), (x + 6, y - 20)), 7, peso=0.04)]


def _acc_arco_eg(m, d):
    x, y = m
    return [T(curva([(x - 6, y - 120), (x + 30, y - 60), (x + 34, y), (x + 30, y + 60), (x - 6, y + 120)], 7), 5.6, peso=0.08),
            T(linea((x - 6, y - 120), (x - 6, y + 120)), 2.4, peso=0.02)]


def _acc_escudo_eg(m, d):
    x, y = m
    P = curva([(x - 30, y + 46), (x - 34, y - 20), (x - 20, y - 64), (x, y - 72), (x + 20, y - 64), (x + 34, y - 20), (x + 30, y + 46)], 6)
    ops = forma(P, (232, 220, 196), 4.6, sp=7)
    return ops + [R(elip(x - 10, y - 24, 10, 8, n=10), (120, 80, 60), peso=0.02, sp=3), R(elip(x + 12, y + 8, 9, 7, n=10), (120, 80, 60), peso=0.02, sp=3)]


def _acc_hacha(m, d):
    x, y = m
    return [T(linea((x, y + 40), (x + 6, y - 96)), 5.6, peso=0.06)] + forma(curva([(x + 4, y - 90), (x + 40, y - 106), (x + 50, y - 80), (x + 42, y - 62),
                                                                                    (x + 6, y - 70)], 5), (176, 150, 110), 4, sp=4)


def _acc_maza(m, d):
    x, y = m
    return [T(linea((x, y + 30), (x + 4, y - 80)), 6, peso=0.05)] + forma(elip(x + 4, y - 96, 20, 22, 0, 1.0, 18), (220, 214, 200), 4.6, sp=5)


def _acc_cuerda(m, d):
    x, y = m
    return [T(curva([(x, y), (x + 60, y - 10), (x + 140, y - 30), (x + 220, y - 46)], 6), 5.2, peso=0.04)]


def _acc_hoz(m, d):
    x, y = m
    return [T(linea((x, y + 14), (x + 4, y - 24)), 6, peso=0.03), T(curva([(x + 4, y - 24), (x + 30, y - 50), (x + 60, y - 40), (x + 66, y - 14)], 6), 5.2, peso=0.04)]


def _acc_cesta(m, d):
    x, y = m
    ops = forma(curva([(x - 40, y - 30), (x - 32, y + 20), (x + 32, y + 20), (x + 40, y - 30)], 5).tolist() + [(x, y - 36)], (196, 150, 90), 4.6, sp=6)
    ops += [T(linea((x - 36, y - 10), (x + 36, y - 10)), 2.8, peso=0.02), T(linea((x - 34, y + 6), (x + 34, y + 6)), 2.8, peso=0.02)]
    return ops + [R(elip(x - 12, y - 36, 12, 10, n=10), (236, 196, 80), peso=0.02, sp=3), R(elip(x + 14, y - 38, 12, 10, n=10), (200, 80, 70), peso=0.02, sp=3)]


def _acc_jarra(m, d):
    x, y = m
    return forma(curva([(x - 12, y - 56), (x - 16, y - 44), (x - 30, y - 10), (x - 22, y + 24), (x + 22, y + 24), (x + 30, y - 10), (x + 16, y - 44), (x + 12, y - 56)], 6),
                 (200, 120, 80), 4.6, sp=6)


def _acc_papiro(m, d):
    x, y = m
    ops = forma(rect(x - 44, y - 22, x + 44, y + 16, 4), (240, 226, 186), 4.2, sp=6)
    ops += [R(elip(x - 44, y - 3, 8, 20, n=12), (210, 190, 140), peso=0.02, sp=3), R(elip(x + 44, y - 3, 8, 20, n=12), (210, 190, 140), peso=0.02, sp=3)]
    for k in range(4):
        ops.append(T(linea((x - 30 + 16 * k, y - 12), (x - 30 + 16 * k, y + 6)), 2.6, peso=0.02))
    return ops


def _acc_pluma_cana(m, d):
    x, y = m
    return [T(linea((x, y + 8), (x + 22, y - 74)), 4.4, peso=0.04)]


def _acc_estandarte(m, d):
    x, y = m
    return [T(linea((x, y + 100), (x + 4, y - 170)), 5.4, peso=0.12)] + forma(elip(x + 6, y - 186, 26, 20, 0, 1.0, 16), ORO_EG, 4.2, sp=5) + \
        [T(curva([(x + 4, y - 160), (x + 30, y - 150), (x + 50, y - 160)], 4), 4, peso=0.03)]


def _acc_abanico_pl(m, d):
    x, y = m
    ops = [T(linea((x, y + 60), (x + 4, y - 120)), 5, peso=0.08)]
    return ops + forma(curva([(x + 4, y - 120), (x - 46, y - 150), (x - 30, y - 196), (x + 4, y - 210), (x + 38, y - 196), (x + 54, y - 150)], 6),
                       (236, 214, 150), 4.2, sp=6)


def _acc_aspid(m, d):
    x, y = m
    return [T(curva([(x - 20, y + 20), (x, y + 6), (x - 10, y - 14), (x + 6, y - 30), (x + 2, y - 50)], 6), 7, peso=0.05), R(elip(x + 4, y - 54, 9, 7, n=10), (110, 140, 80), peso=0.02, sp=3)]


def _acc_copa_eg(m, d):
    x, y = m
    return forma(pol((x - 20, y - 36), (x + 20, y - 36), (x + 12, y), (x - 12, y)), ORO_EG, 4.2, sp=5) + [T(linea((x, y), (x, y + 18)), 4.4, peso=0.02)]


def _acc_gladius(m, d):
    x, y = m
    return [T(linea((x, y + 14), (x + 4, y - 80)), 5.4, peso=0.06), R(pol((x - 5, y - 14), (x + 3, y - 84), (x + 11, y - 14)), (200, 204, 210), peso=0.03, sp=3),
            T(linea((x - 14, y - 12), (x + 20, y - 14)), 6, peso=0.03)]


def _acc_scutum(m, d):
    x, y = m
    ops = forma(rect(x - 34, y - 70, x + 34, y + 60, 10), ROJO_R, 5, sp=7)
    return ops + forma(elip(x, y - 4, 13, 13, 0, 1.0, 14), ORO_EG, 3.6, sp=3) + [T(linea((x, y - 62), (x, y + 52)), 3, peso=0.03)]


def _acc_cimitarra(m, d):
    x, y = m
    return [T(linea((x, y + 14), (x + 4, y - 12)), 7, peso=0.03)] + forma(curva([(x + 2, y - 12), (x + 18, y - 70), (x + 52, y - 108), (x + 40, y - 74),
                                                                                (x + 14, y - 12)], 6), (200, 204, 212), 4, sp=4)


def _acc_escudo_r(m, d):
    x, y = m
    return forma(elip(x, y, 38, 38, 0, 1.0, 26), (150, 100, 60), 4.8, sp=7) + forma(elip(x, y, 12, 12, 0, 1.0, 12), ORO_EG, 3.6, sp=3)


def _acc_escudo_cruz(m, d):
    x, y = m
    P = curva([(x - 34, y - 54), (x + 34, y - 54), (x + 32, y + 4), (x, y + 56), (x - 32, y + 4)], 6)
    return forma(P, BLANCO_EG, 4.6, sp=6) + [R(rect(x - 6, y - 50, x + 6, y + 44, 2), (200, 50, 46), peso=0.02, sp=3),
                                             R(rect(x - 28, y - 18, x + 28, y - 6, 2), (200, 50, 46), peso=0.02, sp=3)]


def _acc_arco_c(m, d):
    x, y = m
    return [T(curva([(x - 4, y - 100), (x + 26, y - 70), (x + 10, y - 40), (x + 30, y), (x + 10, y + 40), (x + 26, y + 70), (x - 4, y + 100)], 8), 5.4, peso=0.06),
            T(linea((x - 4, y - 100), (x - 4, y + 100)), 2.2, peso=0.02)]


def _acc_fusil(m, d):
    x, y = m
    return [T(linea((x - 10, y + 50), (x + 14, y - 140)), 7, peso=0.06), R(pol((x - 16, y + 50), (x - 4, y + 50), (x + 2, y), (x - 10, y)), (150, 100, 60), peso=0.02, sp=3),
            T(linea((x + 14, y - 140), (x + 18, y - 176)), 3, peso=0.02)]


def _acc_libreta(m, d):
    x, y = m
    return forma(rect(x - 30, y - 40, x + 30, y + 10, 3), (236, 226, 196), 4.2, sp=5) + [T(linea((x - 20, y - 26 + 10 * k), (x + 20, y - 26 + 10 * k)), 2.2, peso=0.02)
                                                                                         for k in range(4)]


def _acc_lupa(m, d):
    x, y = m
    return [T(linea((x, y + 10), (x + 22, y - 30)), 7, peso=0.03)] + forma(circ(x + 36, y - 54, 26, n=24), (210, 236, 246), 5, sp=5)


def _acc_pala(m, d):
    x, y = m
    return [T(linea((x, y - 90), (x + 4, y + 70)), 6, peso=0.1)] + forma(pol((x - 18, y + 66), (x + 26, y + 66), (x + 22, y + 116), (x + 4, y + 130), (x - 14, y + 116)),
                                                                         HIERRO, 4.4, sp=4)


def _acc_plano(m, d):
    x, y = m
    ops = forma(rect(x - 50, y - 40, x + 50, y + 20, 3), (170, 206, 236), 4.2, sp=6)
    return ops + [T(linea((x - 40, y - 10), (x + 40, y - 10)), 2.4, peso=0.02), T(linea((x - 20, y - 34), (x - 20, y + 14)), 2.4, peso=0.02),
                  T(curva([(x - 40, y + 10), (x, y - 26), (x + 40, y + 10)], 5), 2.4, peso=0.02)]


def _acc_bandera_eg(m, d):
    x, y = m
    ops = [T(linea((x, y + 40), (x + 4, y - 180)), 5, peso=0.12)]
    ops += forma(rect(x + 4, y - 180, x + 120, y - 160, 2), (200, 50, 46), 4, sp=5) + forma(rect(x + 4, y - 160, x + 120, y - 140, 2), BLANCO_EG, 4, sp=5)
    ops += forma(rect(x + 4, y - 140, x + 120, y - 120, 2), NEGRO_EG, 4, sp=5)
    return ops + [R(elip(x + 62, y - 150, 8, 8, n=10), ORO_EG, peso=0.02, sp=3)]


def _acc_bandera_fr(m, d):
    x, y = m
    ops = [T(linea((x, y + 40), (x + 4, y - 180)), 5, peso=0.12)]
    ops += forma(rect(x + 4, y - 180, x + 40, y - 120, 2), AZUL_FR, 4, sp=5) + forma(rect(x + 40, y - 180, x + 76, y - 120, 2), BLANCO_EG, 4, sp=5)
    return ops + forma(rect(x + 76, y - 180, x + 112, y - 120, 2), (200, 50, 46), 4, sp=5)


def _acc_libro(m, d):
    x, y = m
    ops = forma(pol((x - 40, y - 30), (x, y - 22), (x + 40, y - 30), (x + 40, y + 16), (x, y + 24), (x - 40, y + 16)), (60, 110, 80), 4.4, sp=5)
    return ops + [T(linea((x, y - 22), (x, y + 24)), 3, peso=0.02), R(pol((x - 34, y - 24), (x - 4, y - 18), (x - 4, y + 16), (x - 34, y + 10)), (240, 230, 200), peso=0.02, sp=3)]


OB.ACC.update({"libro": _acc_libro, "cayado": _acc_cayado, "flagelo": _acc_flagelo, "anj": _acc_anj, "uas": _acc_uas, "khopesh": _acc_khopesh, "arco_eg": _acc_arco_eg,
               "escudo_eg": _acc_escudo_eg, "hacha": _acc_hacha, "maza": _acc_maza, "cuerda": _acc_cuerda, "hoz": _acc_hoz, "cesta": _acc_cesta,
               "jarra": _acc_jarra, "papiro": _acc_papiro, "pluma_cana": _acc_pluma_cana, "estandarte": _acc_estandarte, "abanico_pl": _acc_abanico_pl,
               "aspid": _acc_aspid, "copa_eg": _acc_copa_eg, "gladius": _acc_gladius, "scutum": _acc_scutum, "cimitarra": _acc_cimitarra,
               "escudo_r": _acc_escudo_r, "escudo_cruz": _acc_escudo_cruz, "arco_c": _acc_arco_c, "fusil": _acc_fusil, "libreta": _acc_libreta,
               "lupa": _acc_lupa, "pala": _acc_pala, "plano": _acc_plano, "bandera_eg": _acc_bandera_eg, "bandera_fr": _acc_bandera_fr})


# ------------------------------------------------------------------ añadidos al cuerpo
def _usekh(y=-176.0, ancho=44):
    """Collar ancho de cuentas (oro, turquesa, lapislázuli)."""
    ops = []
    for k, col in enumerate((ORO_EG, TURQ, LAPIS)):
        r0 = ancho - 10 * k
        P = arco_(0, y - 2, r0, 15, 165, 14).tolist() + arco_(0, y - 2, r0 - 9, 165, 15, 14).tolist()
        ops.append(R(np.array(P), col, peso=0.03, sp=4))
    return ops + [T(arco_(0, y - 2, ancho, 12, 168, 16), 3.6, peso=0.04)]


def _barba_real(cy=-215.0):
    """Barba postiza trenzada de los faraones."""
    return forma(pol((-9, cy + 34), (9, cy + 34), (8, cy + 74), (-8, cy + 74)), (90, 70, 60), 3.8, sp=3) + [T(linea((-8, cy + 48), (8, cy + 48)), 2.4, peso=0.02),
                                                                                                             T(linea((-8, cy + 61), (8, cy + 61)), 2.4, peso=0.02)]


def _falda_shendyt(oro=True):
    """Delantal triangular dorado sobre la falda de lino."""
    ops = forma(pol((-16, -106), (16, -106), (24, -40), (-24, -40)), ORO_EG if oro else LINO, 4, sp=5)
    return ops + [T(linea((-14, -86), (14, -86)), 2.6, peso=0.02), T(linea((-18, -66), (18, -66)), 2.6, peso=0.02)]


def _barba(col=(96, 70, 56), cy=-215.0, rizos=False):
    P = [(-39, cy + 2), (-37, cy + 44), (-22, cy + 78), (0, cy + 92), (22, cy + 78), (37, cy + 44), (39, cy + 2), (30, cy + 20), (15, cy + 36), (0, cy + 40),
         (-15, cy + 36), (-30, cy + 20)]
    ops = forma(curva(P, 4, cerrado=True), col, 4.4, sp=6)
    ops += [T(curva([(-20, cy + 14), (-8, cy + 10), (0, cy + 13), (8, cy + 10), (20, cy + 14)], 4), 4.2, peso=0.04)]
    if rizos:
        ops += [T(arco_(x, y, 6, 0, 300, 8), 2.6, peso=0.02) for x, y in ((-24, cy + 46), (0, cy + 58), (24, cy + 46), (-12, cy + 74), (12, cy + 74))]
    return ops


def pers(*a, barba=None, rizos=False, **k):
    """persona() con la barba propia (la del kit tapaba la boca)."""
    p = persona(*a, **k)
    if barba is None:
        return p
    d = Dib(list(p.ops) + _barba(barba, rizos=rizos))
    d.manos = getattr(p, "manos", [])
    return d


def _mas(p, *extra):
    """Persona + piezas extra (encima)."""
    ops = list(p.ops)
    for e in extra:
        ops += e
    d = Dib(ops)
    d.manos = getattr(p, "manos", [])
    return d


# ------------------------------------------------------------------ PERSONAJES: Egipto faraónico
@lru_cache(maxsize=None)
def campesino(pose=0, cara="feliz", acc="azada"):
    return _mas(persona(LINO, PIEL_EG, "peluca" if pose % 2 else "calvo", cara, (16, 34), pose, traje="corta", faja=(200, 180, 140), acc_d=acc))


@lru_cache(maxsize=None)
def campesina(pose=0, cara="feliz"):
    return _mas(persona(LINO, PIEL_EG_F, "peluca_larga", cara, (20, 120), pose, traje="vestido", acc_d="cesta"), _usekh(-174, 36))


@lru_cache(maxsize=None)
def segador(pose=0, cara="feliz"):
    return _mas(persona(LINO, PIEL_EG, "peluca", cara, (40, 90), pose, traje="corta", faja=(200, 180, 140), acc_d="hoz"))


@lru_cache(maxsize=None)
def escriba(pose=0, cara="feliz"):
    return _mas(persona(LINO, PIEL_EG, "peluca", cara, (40, 60), pose, traje="tunica", acc_i="papiro", acc_d="pluma_cana"), _usekh(-174, 34))


@lru_cache(maxsize=None)
def sacerdote(pose=0, cara="serio", acc="anj"):
    p = persona(LINO, PIEL_EG, "calvo", cara, (18, 40), pose, traje="tunica", acc_d=acc)
    piel = forma(pol((-46, -170), (40, -100), (46, -60), (10, -70), (-44, -130)), LEOPARDO, 4.2, sp=6)
    manchas = [R(elip(x, y, 6, 5, n=8), (120, 80, 50), peso=0.02, sp=2) for x, y in ((-30, -150), (-10, -128), (10, -110), (28, -92), (-20, -140), (20, -100))]
    return _mas(p, piel, manchas)


@lru_cache(maxsize=None)
def faraon(pose=0, corona="nemes", cara="serio", ropa=LINO, acc_d="cayado", acc_i="flagelo", brazos=(30, 34), piel=PIEL_EG, barba=True):
    p = persona(ropa, piel, corona, cara, brazos, pose, traje="corta", faja=ORO_EG, acc_d=acc_d, acc_i=acc_i)
    ex = [_usekh(), _falda_shendyt()]
    if barba:
        ex.append(_barba_real())
    return _mas(p, *ex)


def narmer(pose=0, corona="pschent", cara="serio"):
    return faraon(pose, corona, cara, acc_d="maza", acc_i="cayado", brazos=(20, 70))


def rey_alto(pose=0, cara="serio"):
    return faraon(pose, "hedjet", cara, acc_d="maza", acc_i=None, brazos=(16, 60))


def rey_bajo(pose=0, cara="serio"):
    return faraon(pose, "deshret", cara, ropa=(236, 214, 200), acc_d="maza", acc_i=None, brazos=(16, 60))


@lru_cache(maxsize=None)
def imhotep(pose=0, cara="feliz"):
    return _mas(persona(LINO, PIEL_EG, "gorro_sabio", cara, (20, 70), pose, traje="tunica", acc_d="plano", acc_i="papiro"), _usekh(-174, 34))


def keops(pose=0, cara="serio"):
    return faraon(pose, "nemes", cara)


@lru_cache(maxsize=None)
def obrero(pose=0, cara="enojo"):
    return persona((236, 226, 200), PIEL_EG, "calvo" if pose % 2 == 0 else "peluca", cara, (60, 70), pose, traje="corta", faja=(200, 180, 140))


@lru_cache(maxsize=None)
def nomarca(pose=0, cara="enojo", ropa=(200, 140, 90)):
    return _mas(persona(ropa, PIEL_EG, "peluca", cara, (16, 50), pose, traje="tunica", faja=ORO_EG, acc_d="uas"), _usekh(-174, 34))


def mentuhotep(pose=0, cara="feliz"):
    return faraon(pose, "pschent", cara, acc_d="uas", acc_i=None, brazos=(18, 30))


@lru_cache(maxsize=None)
def hicso(pose=0, cara="enojo", ropa=(150, 92, 150)):
    p = pers(ropa, PIEL_ASIA, "hicso", cara, (20, 60), pose, traje="tunica", faja=(232, 196, 90), barba=(80, 56, 46), acc_d="hacha")
    rayas = [R(pol((-56, -60 - 24 * k), (56, -60 - 24 * k), (56, -50 - 24 * k), (-56, -50 - 24 * k)), (220, 170, 70), peso=0.02, sp=3) for k in range(3)]
    return _mas(p, rayas)


@lru_cache(maxsize=None)
def soldado_eg(pose=0, cara="serio", acc="lanza"):
    return persona(LINO, PIEL_EG, "peluca", cara, (24, 30), pose, traje="corta", faja=(170, 120, 80), acc_d=acc, acc_i="escudo_eg")


@lru_cache(maxsize=None)
def arquero_eg(pose=0, cara="serio"):
    return persona(LINO, PIEL_EG, "peluca", cara, (40, 70), pose, traje="corta", faja=(170, 120, 80), acc_i="arco_eg")


def ahmose(pose=0, cara="enojo"):
    return faraon(pose, "khepresh", cara, acc_d="khopesh", acc_i="escudo_eg", brazos=(30, 110))


def hatshepsut(pose=0, cara="feliz"):
    p = faraon(pose, "nemes", cara, piel=PIEL_EG_F)
    return _mas(p, [R(elip(-28, -205, 8, 5, n=12), ROSA, peso=0.03, sp=4), R(elip(28, -205, 8, 5, n=12), ROSA, peso=0.03, sp=4),
                    T(linea((-24, -226), (-12, -222)), 3, peso=0.02), T(linea((24, -226), (12, -222)), 3, peso=0.02)])


def tutmosis(pose=0, cara="serio"):
    return faraon(pose, "khepresh", cara, acc_d="khopesh", acc_i="arco_eg", brazos=(24, 60))


@lru_cache(maxsize=None)
def akenaton(pose=0, cara="feliz", brazos=(30, 150)):
    p = persona(LINO, PIEL_EG, "khepresh", cara, brazos, pose, traje="tunica", faja=ORO_EG, alto=1.1)
    return _mas(p, _usekh(), _barba_real())


@lru_cache(maxsize=None)
def nefertiti(pose=0, cara="feliz", brazos=(20, 40)):
    p = persona(LINO, PIEL_EG_F, "nefertiti", cara, brazos, pose, traje="vestido", faja=(200, 70, 60))
    return _mas(p, _usekh(-174, 40))


def tutankamon(pose=0, cara="feliz"):
    return faraon(pose, "nemes", cara)


def ramses(pose=0, cara="serio", corona="khepresh"):
    return faraon(pose, corona, cara, acc_d="khopesh", acc_i="cayado", brazos=(24, 90))


@lru_cache(maxsize=None)
def rey_hitita(pose=0, cara="enojo"):
    return persona((110, 120, 170), PIEL_ASIA, "hitita", cara, (16, 60), pose, traje="tunica", faja=ORO_EG, acc_d="lanza")


@lru_cache(maxsize=None)
def soldado_hitita(pose=0, cara="enojo"):
    return persona((130, 140, 190), PIEL_ASIA, "casco_hitita", cara, (24, 40), pose, traje="armadura", faja=BRONCE, acc_d="lanza", acc_i="escudo_r")


@lru_cache(maxsize=None)
def pueblo_mar(pose=0, cara="enojo", tipo="plumas"):
    return persona((90, 120, 170) if tipo == "plumas" else (170, 110, 80), PIEL_EU, tipo, cara, (30, 70), pose, traje="corta", faja=BRONCE,
                   acc_d="espada", acc_i="escudo_r")


@lru_cache(maxsize=None)
def faraon_nubio(pose=0, cara="serio"):
    p = persona(LINO, PIEL_NUB, "kushita", cara, (24, 60), pose, traje="corta", faja=ORO_EG, acc_d="uas")
    return _mas(p, _usekh(), _falda_shendyt(), [R(circ(-42, -196, 7, n=10), ORO_EG, peso=0.02, sp=3), R(circ(42, -196, 7, n=10), ORO_EG, peso=0.02, sp=3)])


@lru_cache(maxsize=None)
def asirio(pose=0, cara="enojo"):
    p = pers((140, 110, 90), PIEL_ASIA, "asirio", cara, (24, 40), pose, traje="armadura", faja=BRONCE, acc_d="lanza", acc_i="escudo_r",
             barba=(70, 50, 46), rizos=True)
    return p


@lru_cache(maxsize=None)
def persa(pose=0, cara="serio", rey=False):
    if rey:
        return pers((110, 96, 170), PIEL_ASIA, "tiara", cara, (16, 60), pose, traje="tunica", faja=ORO_EG, barba=(86, 64, 52), acc_d="lanza")
    return pers((120, 150, 190), PIEL_ASIA, "turbante_blanco", cara, (24, 40), pose, traje="tunica", faja=(200, 160, 70), barba=(86, 64, 52),
                   acc_d="lanza", acc_i="escudo_r")


@lru_cache(maxsize=None)
def alejandro(pose=0, cara="feliz"):
    return persona((200, 60, 54), PIEL_EU, "macedonio", cara, (20, 120), pose, traje="armadura", faja=ORO_EG, acc_d="espada")


@lru_cache(maxsize=None)
def ptolomeo(pose=0, cara="serio", egipcio=False):
    if egipcio:
        return faraon(pose, "pschent", cara, piel=PIEL_EU, acc_d="uas", acc_i=None, brazos=(18, 30))
    return pers((236, 232, 220), PIEL_EU, "diadema", cara, (16, 40), pose, traje="tunica", faja=(70, 110, 170), barba=(150, 110, 80), acc_d="rollo")


@lru_cache(maxsize=None)
def griego(pose=0, cara="feliz", acc="rollo"):
    return pers((236, 232, 220), PIEL_EU, "pelo", cara, (16, 60), pose, traje="tunica", faja=(70, 110, 170), barba=(120, 90, 70), acc_d=acc)


@lru_cache(maxsize=None)
def cleopatra(pose=0, cara="feliz", corona="buitre", acc_d="copa_eg"):
    p = persona((236, 232, 220), PIEL_EG_F, corona, cara, (20, 50), pose, traje="vestido", faja=ORO_EG, acc_d=acc_d)
    return _mas(p, _usekh(-174, 40), [T(linea((-24, -226), (-12, -222)), 3, peso=0.02), T(linea((24, -226), (12, -222)), 3, peso=0.02)])


@lru_cache(maxsize=None)
def cesar(pose=0, cara="serio"):
    return persona(BLANCO_EG, PIEL_EU, "laurel_r", cara, (16, 50), pose, traje="tunica", faja=PURPURA, cuello=PURPURA, acc_d="rollo")


@lru_cache(maxsize=None)
def marco_antonio(pose=0, cara="feliz"):
    return pers(ROJO_R, PIEL_EU, "pelo", cara, (16, 60), pose, traje="armadura", faja=ORO_EG, barba=(110, 80, 60), acc_d="gladius")


@lru_cache(maxsize=None)
def octavio(pose=0, cara="serio"):
    return persona(BLANCO_EG, PIEL_EU, "pelo", cara, (16, 50), pose, traje="tunica", faja=PURPURA, cuello=PURPURA, acc_d="gladius")


@lru_cache(maxsize=None)
def legionario(pose=0, cara="serio"):
    return persona(ROJO_R, PIEL_EU, "galea_r", cara, (12, 26), pose, traje="armadura", faja=BRONCE, acc_d="lanza", acc_i="scutum")


# ------------------------------------------------------------------ Edad Media y moderna
@lru_cache(maxsize=None)
def amr(pose=0, cara="serio"):
    return pers((90, 140, 100), PIEL_ASIA, "kufiya", cara, (20, 100), pose, traje="tunica", faja=(200, 160, 70), barba=(80, 60, 50), acc_d="cimitarra")


@lru_cache(maxsize=None)
def califa(pose=0, cara="feliz"):
    return pers((70, 130, 90), PIEL_ASIA, "turbante_verde", cara, (16, 40), pose, traje="tunica", faja=ORO_EG, barba=(86, 64, 52), acc_d="libro")


@lru_cache(maxsize=None)
def saladino(pose=0, cara="serio"):
    return pers((214, 160, 60), PIEL_ASIA, "saladino", cara, (24, 100), pose, traje="armadura", faja=(150, 60, 50), barba=(80, 58, 48),
                   acc_d="cimitarra", acc_i="escudo_r")


@lru_cache(maxsize=None)
def cruzado(pose=0, cara="enojo"):
    p = persona(BLANCO_EG, PIEL_EU, "cruzado", cara, (24, 40), pose, traje="armadura", faja=(150, 140, 130), acc_d="espada", acc_i="escudo_cruz")
    return _mas(p, [R(rect(-8, -164, 8, -60, 2), (200, 50, 46), peso=0.02, sp=3), R(rect(-36, -132, 36, -118, 2), (200, 50, 46), peso=0.02, sp=3)])


@lru_cache(maxsize=None)
def mameluco(pose=0, cara="serio"):
    return persona((200, 120, 60), PIEL_ASIA, "mameluco", cara, (30, 80), pose, traje="armadura", faja=(240, 220, 170), bigote=True, acc_i="arco_c",
                   acc_d="cimitarra")


@lru_cache(maxsize=None)
def mongol(pose=0, cara="enojo"):
    return persona((110, 104, 92), PIEL_ASIA, "mongol", cara, (40, 70), pose, traje="armadura", faja=(170, 60, 50), bigote=True, acc_i="arco_c")


@lru_cache(maxsize=None)
def napoleon(pose=0, cara="serio"):
    return persona(AZUL_FR, PIEL_EU, "bicornio", cara, (14, 150), pose, traje="armadura", faja=BLANCO_EG, cuello=BLANCO_EG, acc_d=None)


@lru_cache(maxsize=None)
def soldado_fr(pose=0, cara="serio"):
    return persona(AZUL_FR, PIEL_EU, "chaco", cara, (20, 30), pose, traje="armadura", faja=BLANCO_EG, bigote=True, acc_d="fusil")


@lru_cache(maxsize=None)
def sabio_fr(pose=0, cara="asombro", acc="libreta"):
    return persona((90, 80, 70), PIEL_EU, "pelo", cara, (20, 70), pose, traje="corta", faja=(236, 226, 196), cuello=BLANCO_EG, acc_d=acc)


@lru_cache(maxsize=None)
def champollion(pose=0, cara="asombro"):
    return persona((60, 70, 100), PIEL_EU, "pelo", cara, (30, 90), pose, traje="corta", faja=(236, 226, 196), cuello=BLANCO_EG, acc_d="lupa", acc_i="papiro")


@lru_cache(maxsize=None)
def mehmet_ali(pose=0, cara="serio"):
    return pers((150, 60, 60), PIEL_ASIA, "turbante_eg", cara, (16, 50), pose, traje="tunica", faja=ORO_EG, barba=(240, 236, 228), acc_d="plano")


@lru_cache(maxsize=None)
def lesseps(pose=0, cara="feliz"):
    return persona((60, 60, 70), PIEL_EU, "bombin", cara, (16, 60), pose, traje="corta", faja=(120, 110, 100), cuello=BLANCO_EG, bigote=True, acc_d="plano")


@lru_cache(maxsize=None)
def obrero_canal(pose=0, cara="enojo"):
    return persona((214, 200, 170), PIEL_EG, "fez" if pose % 2 else "turbante_eg", cara, (30, 60), pose, traje="tunica", faja=(160, 120, 80), acc_d="pala")


@lru_cache(maxsize=None)
def soldado_brit(pose=0, cara="serio"):
    return persona(ROJO_UK, PIEL_EU, "salacot", cara, (20, 30), pose, traje="armadura", faja=BLANCO_EG, bigote=True, acc_d="fusil")


@lru_cache(maxsize=None)
def nasser(pose=0, cara="feliz", brazos=(16, 150)):
    return persona((150, 140, 108), PIEL_EG, "gorra_of", cara, brazos, pose, traje="armadura", faja=(110, 100, 80), bigote=True)


@lru_cache(maxsize=None)
def ingeniero(pose=0, cara="feliz"):
    return persona((90, 120, 160), PIEL_EG, "casco_obra", cara, (20, 60), pose, traje="corta", faja=(70, 80, 100), acc_d="plano")


_HOY = [((200, 70, 60), PIEL_EG, "rizos", "feliz", "corta", None), ((110, 150, 180), PIEL_EG_F, "velo", "feliz", "vestido", None),
        ((90, 140, 100), PIEL_EG, "gorra_beis", "feliz", "corta", None), ((236, 180, 70), PIEL_EG_F, "peluca_larga", "guiño", "vestido", None),
        ((150, 110, 160), PIEL_EG, "pelo", "feliz", "corta", "bandera_eg"), ((240, 236, 226), PIEL_EG, "fez", "feliz", "tunica", None)]


@lru_cache(maxsize=None)
def egipcio_hoy(k=0, pose=0):
    ropa, piel, som, cara, traje, acc = _HOY[k % len(_HOY)]
    return persona(ropa, piel, som, cara, (20, 120 if acc else 40), pose, traje=traje, acc_d=acc)


@lru_cache(maxsize=None)
def pintor(pose=0, cara="feliz"):
    return _mas(persona(LINO, PIEL_EG, "peluca", cara, (30, 120), pose, traje="corta", faja=(200, 180, 140), acc_d="pincel", acc_i="jarra"))


@lru_cache(maxsize=None)
def alejandro_faraon(pose=0, cara="feliz"):
    return faraon(pose, "pschent", cara, piel=PIEL_EU, acc_d="uas", acc_i=None, brazos=(18, 30), barba=False)


@lru_cache(maxsize=None)
def cleopatra_aspid(pose=0):
    return cleopatra(pose, "lloron", "buitre", "aspid")


@lru_cache(maxsize=None)
def turista(pose=0, cara="feliz"):
    return persona((236, 120, 80), PIEL_EU, "gorra_beis", cara, (20, 110), pose, traje="corta", faja=(80, 110, 150), acc_d="libreta")
