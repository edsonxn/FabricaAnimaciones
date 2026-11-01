# -*- coding: utf-8 -*-
"""Dibujos de boceto para «La historia de México en 5 minutos» (1/3): tocados, sombreros, accesorios y PERSONAJES de tres mil años.
Convenciones de obj_base: origen en los PIES, cabeza en y ≈ -215 (radio 41). `pose` 0..3 = ciclo de paso."""
import math
from functools import lru_cache

import numpy as np

import obj_base as OB
from obj_a import colocar
from obj_base import *  # noqa: F401,F403

# ------------------------------------------------------------------ paleta mexicana (pigmentos de códice, jade, grana cochinilla, oro, talavera)
ORO_MX = (236, 186, 58)
JADE_MX = (64, 158, 126)
TURQ_MX = (68, 172, 168)
GRANA = (198, 56, 52)
OCRE_MX = (212, 146, 72)
MANTA = (244, 240, 226)
OBSIDIANA = (44, 42, 48)
PIEL_MESO = (198, 134, 92)
PIEL_MESO_F = (216, 154, 112)
PIEL_CL = (240, 198, 166)
PIEDRA_V = (158, 152, 142)
TEZONTLE = (164, 72, 62)
CAL_BL = (238, 232, 216)
HIERRO_MX = (148, 154, 164)
PLATA_MX = (212, 218, 226)
VERDE_BAND = (56, 138, 84)
ROJO_BAND = (202, 54, 50)
AZUL_EEUU = (58, 84, 146)
AZUL_FR = (56, 78, 144)
CAQUI_REV = (188, 166, 118)
CHARRO_OS = (58, 50, 46)

_orig_sombrero = OB.sombrero


def _sombrero(nombre, cy=-215.0):
    if nombre == "casco_olmeca":
        ops = forma(curva([(-48, cy + 4), (-50, cy - 42), (-32, cy - 68), (0, cy - 74), (32, cy - 68), (50, cy - 42), (48, cy + 4)], 6),
                    (172, 148, 112), 4.8, sp=7)
        ops += forma(rect(-48, cy - 34, 48, cy - 20, 3), OCRE_MX, 4.0, sp=5)
        ops += [R(circ(0, cy - 46, 10, n=12), JADE_MX, peso=0.02, sp=3)]
        return ops
    if nombre == "penacho":
        ops = []
        for k in range(11):
            a = math.radians(-160 + 14 * k)
            x0, y0 = 32 * math.cos(a), cy - 36 + 22 * math.sin(a)
            x1, y1 = 108 * math.cos(a), cy - 42 + 88 * math.sin(a)
            col = JADE_MX if k % 2 == 0 else (76, 176, 112)
            ops += forma(pol((x0 - 5, y0), (x1, y1), (x0 + 5, y0)), col, 3.4, sp=4)
        ops += forma(curva([(-44, cy - 18), (-42, cy - 54), (0, cy - 68), (42, cy - 54), (44, cy - 18)], 5), ORO_MX, 4.6, sp=6)
        ops += forma(rect(-44, cy - 28, 44, cy - 16, 3), GRANA, 3.8, sp=4)
        ops += [R(circ(-18 + 18 * k, cy - 38, 5, n=10), TURQ_MX, peso=0.02, sp=3) for k in range(3)]
        return ops
    if nombre == "aguila":
        ops = forma(curva([(-48, cy + 6), (-52, cy - 40), (-30, cy - 74), (14, cy - 80), (44, cy - 60), (56, cy - 30), (54, cy + 6)], 6),
                    (168, 122, 74), 4.8, sp=7)
        ops += forma(pol((42, cy - 50), (88, cy - 42), (72, cy - 24), (50, cy - 24)), ORO_MX, 4.0, sp=4)
        ops += [punto(28, cy - 52, 8)]
        for k in range(4):
            ops += forma(elip(-38 + 8 * k, cy - 90 - 5 * k, 8, 22, -0.45 + 0.18 * k, 1.0, 12), JADE_MX if k % 2 else GRANA, 3.0, sp=3)
        return ops
    if nombre == "jaguar":
        ops = forma(curva([(-48, cy + 8), (-52, cy - 42), (-28, cy - 72), (16, cy - 74), (46, cy - 54), (54, cy + 6)], 6), ORO_MX, 4.8, sp=7)
        for sx in (-24, 16):
            ops += forma(elip(sx, cy - 74, 11, 11, 0, 1.0, 10), ORO_MX, 3.6, sp=3)
        for x, y in ((-26, cy - 46), (0, cy - 56), (22, cy - 44), (-16, cy - 28)):
            ops += [R(circ(x, y, 5, n=8), OBSIDIANA, peso=0.02, sp=2)]
        return ops
    if nombre == "tlaxcala":
        ops = forma(elip(0, cy - 18, 43, 30, math.pi, 0.5, 20), OBSIDIANA, 4.2, cerrada=False, sp=6)[1:]
        ops += forma(rect(-44, cy - 38, 44, cy - 24, 4), GRANA, 3.8, sp=4)
        ops += forma(rect(-20, cy - 38, 20, cy - 24, 2), MANTA, 3.4, sp=3)
        for k in range(3):
            ops += forma(elip(-10 + 10 * k, cy - 72, 7, 26, 0.18 * (k - 1), 1.0, 12), MANTA if k != 1 else GRANA, 3.2, sp=3)
        return ops
    if nombre == "morrion":
        ops = forma(curva([(-68, cy - 20), (-48, cy - 30), (-36, cy - 66), (0, cy - 78), (36, cy - 66), (48, cy - 30), (68, cy - 20),
                           (40, cy - 36), (-40, cy - 36)], 6), HIERRO_MX, 4.8, sp=8)
        ops += forma(curva([(-28, cy - 70), (-10, cy - 100), (16, cy - 102), (30, cy - 70)], 5).tolist() + [(0, cy - 76)], HIERRO_MX, 4.2, sp=5)
        return ops + forma(pol((-4, cy - 102), (4, cy - 128), (14, cy - 102)), GRANA, 3.0, sp=3)
    if nombre == "peluca_virrey":
        ops = forma(curva([(-46, cy - 6), (-50, cy - 34), (-30, cy - 58), (0, cy - 64), (30, cy - 58), (50, cy - 34), (46, cy - 6),
                           (34, cy - 26), (0, cy - 36), (-34, cy - 26)], 6), (238, 234, 224), 4.4, sp=7)
        for lado in (-1, 1):
            for k in range(2):
                ops += forma(elip(lado * 48, cy - 4 + 20 * k, 12, 10, 0, 1.0, 12), (238, 234, 224), 3.6, sp=4)
        return ops
    if nombre == "monja":
        ops = forma(curva([(-56, cy + 56), (-60, cy - 18), (-42, cy - 64), (0, cy - 74), (42, cy - 64), (60, cy - 18), (56, cy + 56),
                           (38, cy + 44), (38, cy - 18), (0, cy - 34), (-38, cy - 18), (-38, cy + 44)], 6), OBSIDIANA, 4.6, sp=7)
        ops += forma(rect(-40, cy - 44, 40, cy - 28, 3), MANTA, 3.8, sp=4)
        return ops
    if nombre == "cura_hidalgo":
        ops = []
        for lado in (-1, 1):
            ops += forma(elip(lado * 44, cy - 6, 14, 20, 0, 1.0, 14), (242, 240, 236), 3.8, sp=4)
        return ops
    if nombre == "paliacate_morelos":
        ops = forma(curva([(-46, cy - 12), (-48, cy - 44), (0, cy - 62), (48, cy - 44), (46, cy - 12)], 5).tolist() + [(0, cy - 24)],
                    GRANA, 4.6, sp=6)
        ops += forma(pol((-44, cy - 24), (-72, cy - 8), (-60, cy + 10)), GRANA, 3.6, sp=3)
        return ops
    if nombre == "bicornio_iturbide":
        ops = forma(curva([(-78, cy - 28), (-44, cy - 66), (0, cy - 92), (44, cy - 66), (78, cy - 28), (40, cy - 40), (0, cy - 46), (-40, cy - 40)], 6),
                    OBSIDIANA, 4.8, sp=7)
        ops += [R(circ(-10, cy - 96, 9, n=10), VERDE_BAND, peso=0.02, sp=3), R(circ(0, cy - 102, 9, n=10), MANTA, peso=0.02, sp=3),
                R(circ(10, cy - 96, 9, n=10), ROJO_BAND, peso=0.02, sp=3)]
        return ops + forma(rect(-50, cy - 44, 50, cy - 34, 2), ORO_MX, 3.4, sp=3)
    if nombre == "chaco_eeuu":
        ops = forma(rect(-36, cy - 72, 36, cy - 26, 4), AZUL_EEUU, 4.6, sp=7)
        return ops + forma(rect(-44, cy - 30, 44, cy - 20, 3), OBSIDIANA, 3.8, sp=4)
    if nombre == "chaco_fr":
        ops = forma(pol((-34, cy - 22), (-38, cy - 88), (38, cy - 88), (34, cy - 22)), ROJO_BAND, 4.6, sp=7)
        ops += forma(rect(-40, cy - 30, 40, cy - 20, 2), OBSIDIANA, 3.6, sp=3)
        return ops + forma(elip(0, cy - 98, 8, 12, 0, 1.0, 12), ORO_MX, 3.0, sp=3)
    if nombre == "chistera":
        return forma(rect(-32, cy - 104, 32, cy - 32, 4), OBSIDIANA, 4.6, sp=7) + forma(rect(-54, cy - 38, 54, cy - 26, 4), OBSIDIANA, 4.4, sp=6)
    if nombre == "corona_imp":
        ops = forma(pol((-42, cy - 26), (-46, cy - 72), (-22, cy - 54), (0, cy - 84), (22, cy - 54), (46, cy - 72), (42, cy - 26)), ORO_MX, 4.6, sp=7)
        return ops + [R(circ(0, cy - 44, 6, n=10), GRANA, peso=0.02, sp=3)]
    if nombre == "bicornio_porfirio":
        ops = forma(curva([(-76, cy - 28), (-42, cy - 64), (0, cy - 88), (42, cy - 64), (76, cy - 28), (38, cy - 40), (-38, cy - 40)], 6),
                    OBSIDIANA, 4.8, sp=7)
        ops += forma(curva([(-48, cy - 66), (0, cy - 96), (48, cy - 66)], 5), MANTA, 4.0, sp=5)
        return ops + forma(rect(-46, cy - 42, 46, cy - 32, 2), ORO_MX, 3.4, sp=3)
    if nombre == "charro_zapata":
        ops = forma(pol((-36, cy - 36), (-22, cy - 98), (0, cy - 108), (22, cy - 98), (36, cy - 36)), CHARRO_OS, 4.8, sp=7)
        ops += forma(curva([(-96, cy - 26), (-50, cy - 46), (0, cy - 42), (50, cy - 46), (96, cy - 26), (56, cy - 16), (-56, cy - 16)], 6),
                     CHARRO_OS, 4.8, sp=8)
        return ops + forma(rect(-34, cy - 48, 34, cy - 38, 2), ORO_MX, 3.4, sp=3)
    if nombre == "charro_blanco":
        ops = forma(pol((-34, cy - 34), (-20, cy - 90), (0, cy - 98), (20, cy - 90), (34, cy - 34)), (236, 224, 188), 4.6, sp=7)
        return ops + forma(curva([(-84, cy - 24), (-44, cy - 42), (0, cy - 38), (44, cy - 42), (84, cy - 24), (48, cy - 16), (-48, cy - 16)], 6),
                           (236, 224, 188), 4.6, sp=7)
    if nombre == "stetson_villa":
        ops = forma(curva([(-38, cy - 32), (-30, cy - 78), (0, cy - 86), (30, cy - 78), (38, cy - 32)], 5), CAQUI_REV, 4.6, sp=7)
        return ops + forma(elip(0, cy - 30, 68, 12, 0, 1.0, 24), CAQUI_REV, 4.4, sp=6)
    if nombre == "flores_frida":
        P = [(-44, cy - 2), (-46, cy - 34), (-28, cy - 54), (0, cy - 58), (28, cy - 54), (46, cy - 34), (44, cy - 2), (34, cy - 20), (-34, cy - 20)]
        ops = forma(P, OBSIDIANA, 4.6, sp=7)
        for x, col in ((-22, GRANA), (0, ORO_MX), (22, (212, 92, 152))):
            ops += forma(circ(x, cy - 54, 12, n=12), col, 3.6, sp=3)
        return ops
    if nombre == "casco_petrolero":
        ops = forma(curva([(-48, cy - 18), (-44, cy - 56), (0, cy - 72), (44, cy - 56), (48, cy - 18)], 5), ORO_MX, 4.6, sp=7)
        return ops + forma(rect(-56, cy - 24, 56, cy - 14, 3), ORO_MX, 4.0, sp=5)
    if nombre in ("pelo_negro", "pelo_castano", "pelo_canoso"):
        col = {"pelo_negro": OBSIDIANA, "pelo_castano": (112, 76, 52), "pelo_canoso": (208, 206, 200)}[nombre]
        P = [(-42, cy - 4), (-45, cy - 30), (-30, cy - 47), (0, cy - 53), (30, cy - 47), (45, cy - 30), (42, cy - 4),
             (37, cy - 20), (20, cy - 28), (0, cy - 26), (-20, cy - 28), (-37, cy - 20)]
        return forma(P, col, 4.4, sp=7)
    if nombre == "trenza_indigena":
        P = [(-44, cy + 28), (-48, cy - 24), (-32, cy - 52), (0, cy - 56), (32, cy - 52), (48, cy - 24), (44, cy + 28),
             (34, cy + 20), (34, cy - 18), (0, cy - 28), (-34, cy - 18), (-34, cy + 20)]
        return forma(P, OBSIDIANA, 4.4, sp=7) + forma(rect(-44, cy - 32, 44, cy - 22, 2), GRANA, 3.4, sp=3)
    return _orig_sombrero(nombre, cy)


OB.sombrero = _sombrero


# ------------------------------------------------------------------ accesorios en mano
def _acc_maiz(m, d):
    x, y = m
    ops = forma(pol((x - 10, y + 18), (x - 16, y - 48), (x + 16, y - 48), (x + 10, y + 18)), JADE_MX, 3.8, sp=4)
    return ops + forma(elip(x, y - 44, 12, 28, 0, 1.0, 16), ORO_MX, 4.2, sp=5)


def _acc_macuahuitl(m, d):
    x, y = m
    ops = forma(pol((x - 8, y + 20), (x + 8, y + 20), (x + 12, y - 118), (x - 4, y - 118)), (166, 114, 70), 4.2, sp=4)
    for k in range(5):
        yy = y - 12 - 22 * k
        ops += forma(pol((x - 6, yy), (x - 18, yy - 6), (x - 6, yy - 12)), OBSIDIANA, 2.8, sp=2)
        ops += forma(pol((x + 10, yy), (x + 22, yy - 6), (x + 10, yy - 12)), OBSIDIANA, 2.8, sp=2)
    return ops


def _acc_chimalli(m, d):
    x, y = m
    ops = forma(elip(x, y, 38, 38, 0, 1.0, 24), ORO_MX, 4.6, sp=7) + forma(elip(x, y, 18, 18, 0, 1.0, 16), TURQ_MX, 3.4, sp=4)
    for k in range(5):
        ops += forma(elip(x - 24 + 12 * k, y + 44, 5, 14, 0, 1.0, 10), JADE_MX if k % 2 else GRANA, 2.6, sp=2)
    return ops


def _acc_estandarte(m, d):
    x, y = m
    ops = [T(linea((x, y + 40), (x + 2, y - 188)), 5.4, peso=0.08), T(linea((x - 42, y - 176), (x + 46, y - 176)), 4.6, peso=0.04)]
    ops += forma(rect(x - 38, y - 174, x + 42, y - 78, 4), MANTA, 4.2, sp=6)
    ops += forma(elip(x + 2, y - 126, 18, 30, 0, 1.0, 16), JADE_MX, 3.6, sp=4)
    return ops + forma(elip(x + 2, y - 144, 8, 8, 0, 1.0, 10), PIEL_MESO_F, 3.0, sp=2)


def _acc_campana_mano(m, d):
    x, y = m
    return forma(pol((x - 16, y - 34), (x + 16, y - 34), (x + 28, y + 10), (x - 28, y + 10)), ORO_MX, 4.4, sp=5) + \
        forma(elip(x, y + 16, 7, 7, 0, 1.0, 10), ORO_MX, 3.0, sp=2)


def _acc_bandera_mx(m, d):
    x, y = m
    ops = [T(linea((x, y + 44), (x + 4, y - 188)), 5.2, peso=0.10)]
    for k, c in enumerate((VERDE_BAND, MANTA, ROJO_BAND)):
        x0 = x + 4 + 34 * k
        ops += [R(pol((x0, y - 186), (x0 + 34, y - 184), (x0 + 34, y - 110), (x0, y - 112)), c, peso=0.03, sp=5)]
    ops += [R(circ(x + 55, y - 148, 9, n=10), (150, 104, 60), peso=0.02, sp=3)]
    return ops + [T(pol((x + 4, y - 186), (x + 106, y - 182), (x + 106, y - 110), (x + 4, y - 112), (x + 4, y - 186)), 3.8, peso=0.04)]


def _acc_fusil_mx(m, d):
    x, y = m
    return [T(linea((x - 18, y + 54), (x + 22, y - 142)), 5.6, peso=0.08),
            R(pol((x - 24, y + 60), (x - 8, y + 64), (x + 4, y + 10), (x - 10, y + 6)), (140, 96, 60), peso=0.03, sp=4)]


def _acc_libro_mx(m, d):
    x, y = m
    return forma(rect(x - 28, y - 44, x + 28, y + 18, 4), GRANA, 4.2, sp=5) + [rayita(x - 16, y - 24, x + 16, y - 24, 3.0)]


def _acc_pincel_mx(m, d):
    x, y = m
    return [T(linea((x - 6, y + 26), (x + 18, y - 74)), 5.2, peso=0.04)] + forma(pol((x + 14, y - 72), (x + 24, y - 98), (x + 30, y - 70)), GRANA, 3.4, sp=3)


def _acc_paleta_mx(m, d):
    x, y = m
    ops = forma(elip(x, y - 14, 34, 24, 0.2, 1.0, 18), (212, 174, 124), 4.0, sp=5)
    for dx, dy, col in ((-14, -18, GRANA), (0, -24, ORO_MX), (14, -16, JADE_MX)):
        ops += [R(circ(x + dx, y + dy, 6, n=8), col, peso=0.01, sp=2)]
    return ops


def _acc_cetro(m, d):
    x, y = m
    ops = [T(linea((x, y + 60), (x + 4, y - 140)), 5.4, peso=0.08)]
    ops += forma(circ(x + 4, y - 154, 14, n=14), ORO_MX, 4.2, sp=4)
    return ops + [R(circ(x + 4, y - 154, 6, n=10), JADE_MX, peso=0.02, sp=2)]


def _acc_maza(m, d):
    x, y = m
    ops = [T(linea((x - 4, y + 24), (x + 10, y - 68)), 5.2, peso=0.06)]
    return ops + forma(rect(x - 16, y - 92, x + 36, y - 62, 4), PIEDRA_V, 4.4, sp=5)


def _acc_pluma(m, d):
    x, y = m
    ops = forma(curva([(x, y + 8), (x + 12, y - 48), (x + 36, y - 86), (x + 18, y - 34)], 5), MANTA, 3.8, sp=4)
    return ops + [T(linea((x - 4, y + 18), (x + 32, y - 80)), 3.6, peso=0.03)]


OB.ACC.update({
    "maiz_mano": _acc_maiz, "macuahuitl": _acc_macuahuitl, "chimalli": _acc_chimalli,
    "estandarte": _acc_estandarte, "campana_mano": _acc_campana_mano, "bandera_mx": _acc_bandera_mx,
    "fusil_mx": _acc_fusil_mx, "libro_mx": _acc_libro_mx, "pincel_mx": _acc_pincel_mx, "paleta_mx": _acc_paleta_mx,
    "cetro": _acc_cetro, "maza": _acc_maza, "pluma": _acc_pluma,
})


def _barba(col=(96, 70, 56), cy=-215.0):
    P = [(-38, cy + 2), (-36, cy + 42), (-20, cy + 74), (0, cy + 86), (20, cy + 74), (36, cy + 42), (38, cy + 2),
         (28, cy + 20), (14, cy + 34), (0, cy + 38), (-14, cy + 34), (-28, cy + 20)]
    return forma(curva(P, 4, cerrado=True), col, 4.4, sp=6)


def _bigote_charro(col=OBSIDIANA, cy=-215.0):
    return forma(curva([(-34, cy + 26), (-16, cy + 12), (0, cy + 16), (16, cy + 12), (34, cy + 26), (16, cy + 24), (0, cy + 22), (-16, cy + 24)], 4),
                 col, 3.8, sp=4)


def _cananas():
    return [T(linea((-36, -172), (36, -104)), 6.2, peso=0.04), T(linea((36, -172), (-36, -104)), 6.2, peso=0.04),
            R(pol((-38, -174), (38, -102), (32, -96), (-42, -168)), ORO_MX, peso=0.02, sp=3),
            R(pol((38, -174), (-38, -102), (-32, -96), (42, -168)), ORO_MX, peso=0.02, sp=3)]


def _mas(p, *extra):
    ops = list(p.ops)
    for e in extra:
        ops += e
    d = Dib(ops)
    d.manos = getattr(p, "manos", [])
    return d


# ------------------------------------------------------------------ PERSONAJES: Mesoamérica
@lru_cache(maxsize=None)
def campesino_pre(pose=0, cara="feliz"):
    return persona(MANTA, PIEL_MESO, "pelo_negro", cara, (20, 60), pose, traje="corta", faja=GRANA, acc_d="maiz_mano")


@lru_cache(maxsize=None)
def campesina_pre(pose=0, cara="feliz"):
    return persona(MANTA, PIEL_MESO_F, "trenza_indigena", cara, (24, 70), pose, traje="vestido", faja=JADE_MX, acc_d="maiz_mano")


@lru_cache(maxsize=None)
def escultor_olmeca(pose=0, cara="serio"):
    return persona(OCRE_MX, PIEL_MESO, "casco_olmeca", cara, (24, 65), pose, traje="corta", faja=JADE_MX, acc_d="maza")


@lru_cache(maxsize=None)
def sabio_zapoteca(pose=0, cara="feliz"):
    return persona(MANTA, PIEL_MESO, "penacho", cara, (20, 75), pose, traje="tunica", faja=GRANA, cuello=JADE_MX, acc_d="cetro")


@lru_cache(maxsize=None)
def sacerdote_teotihuacan(pose=0, cara="serio"):
    return persona(GRANA, PIEL_MESO, "penacho", cara, (28, 70), pose, traje="tunica", faja=ORO_MX, cuello=JADE_MX, acc_d="cetro")


@lru_cache(maxsize=None)
def rey_maya(pose=0, cara="serio"):
    return persona(MANTA, PIEL_MESO, "penacho", cara, (24, 80), pose, traje="corta", faja=JADE_MX, cuello=TURQ_MX, acc_d="cetro", acc_i="chimalli")


@lru_cache(maxsize=None)
def astronomo_maya(pose=0, cara="feliz"):
    return persona(MANTA, PIEL_MESO, "pelo_negro", cara, (30, 85), pose, traje="tunica", faja=TURQ_MX, acc_d="libro_mx")


@lru_cache(maxsize=None)
def guerrero_tolteca(pose=0, cara="enojo"):
    return persona(OCRE_MX, PIEL_MESO, "tlaxcala", cara, (24, 60), pose, traje="armadura", faja=TURQ_MX, acc_d="lanza", acc_i="chimalli")


@lru_cache(maxsize=None)
def guerrero_aguila(pose=0, cara="enojo"):
    return persona(ORO_MX, PIEL_MESO, "aguila", cara, (22, 65), pose, traje="armadura", faja=GRANA, acc_d="macuahuitl", acc_i="chimalli")


@lru_cache(maxsize=None)
def guerrero_jaguar(pose=0, cara="enojo"):
    return persona(ORO_MX, PIEL_MESO, "jaguar", cara, (24, 65), pose, traje="armadura", faja=JADE_MX, acc_d="macuahuitl", acc_i="chimalli")


@lru_cache(maxsize=None)
def moctezuma(pose=0, cara="serio"):
    return persona(MANTA, PIEL_MESO, "penacho", cara, (24, 80), pose, traje="tunica", faja=ORO_MX, cuello=JADE_MX, acc_d="cetro", acc_i="chimalli")


# ------------------------------------------------------------------ Conquista y Virreinato
@lru_cache(maxsize=None)
def cortes(pose=0, cara="serio"):
    p = persona((168, 54, 48), PIEL_CL, "morrion", cara, (22, 70), pose, traje="armadura", faja=ORO_MX, acc_d="espada")
    return _mas(p, _barba((96, 68, 48)))


@lru_cache(maxsize=None)
def soldado_esp(pose=0, cara="enojo"):
    return persona(HIERRO_MX, PIEL_CL, "morrion", cara, (24, 55), pose, traje="armadura", faja=GRANA, acc_d="lanza")


@lru_cache(maxsize=None)
def tlaxcalteca(pose=0, cara="enojo"):
    return persona(MANTA, PIEL_MESO, "tlaxcala", cara, (22, 60), pose, traje="armadura", faja=GRANA, acc_d="lanza", acc_i="chimalli")


@lru_cache(maxsize=None)
def malinche(pose=0, cara="serio"):
    return persona((236, 224, 204), PIEL_MESO_F, "trenza_indigena", cara, (24, 70), pose, traje="vestido", faja=GRANA, cuello=JADE_MX)


@lru_cache(maxsize=None)
def virrey(pose=0, cara="serio"):
    return persona((62, 84, 152), PIEL_CL, "peluca_virrey", cara, (20, 65), pose, traje="tunica", faja=ORO_MX, cuello=MANTA, acc_d="cetro")


@lru_cache(maxsize=None)
def minero_plata(pose=0, cara="serio"):
    return persona((180, 154, 118), PIEL_MESO, "pelo_negro", cara, (30, 75), pose, traje="corta", faja=(120, 90, 64), acc_d="azada")


@lru_cache(maxsize=None)
def sor_juana(pose=0, cara="feliz"):
    p = persona(MANTA, PIEL_CL, "monja", cara, (24, 80), pose, traje="tunica", faja=OBSIDIANA, acc_d="pluma", acc_i="libro_mx")
    medallon = forma(elip(0, -152, 20, 16, 0, 1.0, 16), ORO_MX, 3.8, sp=4)
    return _mas(p, medallon)


# ------------------------------------------------------------------ Independencia y siglo XIX
@lru_cache(maxsize=None)
def hidalgo(pose=0, cara="enojo"):
    p = persona(OBSIDIANA, PIEL_CL, "cura_hidalgo", cara, (26, 110), pose, traje="tunica", cuello=MANTA, acc_d="estandarte", acc_i="campana_mano")
    return p


@lru_cache(maxsize=None)
def morelos(pose=0, cara="serio"):
    return persona((54, 74, 132), PIEL_MESO, "paliacate_morelos", cara, (24, 80), pose, traje="tunica", faja=ORO_MX, acc_d="espada", acc_i="libro_mx")


@lru_cache(maxsize=None)
def vicente_guerrero(pose=0, cara="serio"):
    return persona((64, 112, 86), PIEL_MESO, "pelo_negro", cara, (24, 75), pose, traje="tunica", faja=ORO_MX, acc_d="espada")


@lru_cache(maxsize=None)
def iturbide(pose=0, cara="serio", imperial=False):
    som = "corona_imp" if imperial else "bicornio_iturbide"
    return persona((52, 76, 136), PIEL_CL, som, cara, (22, 75), pose, traje="tunica", faja=ORO_MX, cuello=GRANA if imperial else None, acc_d="espada")


@lru_cache(maxsize=None)
def soldado_mx_xix(pose=0, cara="serio"):
    return persona((68, 124, 92), PIEL_MESO, "chaco_eeuu", cara, (24, 60), pose, traje="tunica", faja=MANTA, acc_d="fusil_mx")


@lru_cache(maxsize=None)
def soldado_eeuu(pose=0, cara="enojo"):
    return persona(AZUL_EEUU, PIEL_CL, "chaco_eeuu", cara, (24, 60), pose, traje="tunica", faja=MANTA, acc_d="fusil_mx")


@lru_cache(maxsize=None)
def juarez(pose=0, cara="serio"):
    return persona(OBSIDIANA, PIEL_MESO, "chistera", cara, (24, 75), pose, traje="tunica", cuello=MANTA, acc_d="bandera_mx", acc_i="libro_mx")


@lru_cache(maxsize=None)
def zaragoza(pose=0, cara="enojo"):
    return persona((56, 82, 138), PIEL_CL, "pelo_castano", cara, (24, 85), pose, traje="tunica", faja=ORO_MX, acc_d="espada")


@lru_cache(maxsize=None)
def soldado_frances(pose=0, cara="enojo"):
    return persona(AZUL_FR, PIEL_CL, "chaco_fr", cara, (24, 60), pose, traje="tunica", faja=MANTA, acc_d="fusil_mx")


@lru_cache(maxsize=None)
def maximiliano(pose=0, cara="serio"):
    p = persona((56, 78, 138), PIEL_CL, "corona_imp", cara, (20, 65), pose, traje="tunica", faja=GRANA, acc_d="cetro")
    return _mas(p, _barba((206, 162, 96)))


# ------------------------------------------------------------------ Porfiriato, Revolución y siglo XX
@lru_cache(maxsize=None)
def porfirio_diaz(pose=0, cara="serio"):
    p = persona(OBSIDIANA, PIEL_MESO, "bicornio_porfirio", cara, (20, 60), pose, traje="tunica", faja=ORO_MX, acc_d="espada")
    medallas = [R(circ(-18 + 12 * k, -146, 5, n=8), ORO_MX, peso=0.02, sp=2) for k in range(3)]
    return _mas(p, _bigote_charro((220, 218, 212)), medallas)


@lru_cache(maxsize=None)
def madero(pose=0, cara="feliz"):
    p = persona(OBSIDIANA, PIEL_CL, "chistera", cara, (24, 90), pose, traje="tunica", cuello=MANTA, acc_d="bandera_mx")
    return _mas(p, _barba((96, 68, 48)))


@lru_cache(maxsize=None)
def zapata(pose=0, cara="enojo"):
    p = persona(CHARRO_OS, PIEL_MESO, "charro_zapata", cara, (24, 75), pose, traje="tunica", faja=ORO_MX, acc_d="fusil_mx")
    return _mas(p, _bigote_charro(), _cananas())


@lru_cache(maxsize=None)
def pancho_villa(pose=0, cara="enojo"):
    p = persona(CAQUI_REV, PIEL_MESO, "stetson_villa", cara, (24, 80), pose, traje="tunica", faja=(130, 90, 56), acc_d="fusil_mx")
    return _mas(p, _bigote_charro((112, 74, 48)), _cananas())


@lru_cache(maxsize=None)
def adelita(pose=0, cara="serio"):
    p = persona(MANTA, PIEL_MESO_F, "charro_blanco", cara, (24, 70), pose, traje="vestido", faja=GRANA, acc_d="fusil_mx")
    return _mas(p, _cananas())


@lru_cache(maxsize=None)
def carranza(pose=0, cara="serio"):
    p = persona(CAQUI_REV, PIEL_CL, "stetson_villa", cara, (20, 80), pose, traje="tunica", acc_d="libro_mx")
    return _mas(p, _barba((224, 220, 212)))


@lru_cache(maxsize=None)
def diego_rivera(pose=0, cara="feliz"):
    return persona((74, 106, 158), PIEL_MESO, "pelo_negro", cara, (26, 85), pose, traje="tunica", faja=(140, 100, 68), acc_d="pincel_mx", acc_i="paleta_mx")


@lru_cache(maxsize=None)
def frida_kahlo(pose=0, cara="serio"):
    p = persona(GRANA, PIEL_MESO_F, "flores_frida", cara, (22, 75), pose, traje="vestido", faja=ORO_MX, cuello=JADE_MX, acc_d="pincel_mx")
    ceja = [T(curva([(-22, -226), (0, -221), (22, -226)], 4), 3.8, peso=0.02)]
    return _mas(p, ceja)


@lru_cache(maxsize=None)
def lazaro_cardenas(pose=0, cara="serio"):
    p = persona((70, 84, 98), PIEL_MESO, "pelo_negro", cara, (22, 85), pose, traje="tunica", cuello=MANTA, acc_d="bandera_mx")
    return _mas(p, _bigote_charro())


@lru_cache(maxsize=None)
def obrero_petroleo(pose=0, cara="feliz"):
    return persona((68, 104, 152), PIEL_MESO, "casco_petrolero", cara, (26, 75), pose, traje="tunica", faja=(90, 70, 52), acc_d="azada")


@lru_cache(maxsize=None)
def ciudadano_hoy(pose=0, cara="feliz"):
    return persona(VERDE_BAND, PIEL_MESO, "pelo_negro", cara, (24, 85), pose, traje="tunica", acc_d="bandera_mx")


@lru_cache(maxsize=None)
def ingeniera_hoy(pose=0, cara="feliz"):
    return persona((236, 232, 220), PIEL_MESO_F, "casco_petrolero", cara, (24, 75), pose, traje="tunica", faja=VERDE_BAND, acc_d="libro_mx")
