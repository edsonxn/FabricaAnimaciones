# -*- coding: utf-8 -*-
"""Dibujos de boceto para la historia de España (1/4): sombreros y accesorios nuevos para `persona`, y la Antigüedad:
Atapuerca, Altamira, íberos y celtas (Dama de Elche, falcata), fenicios, griegos, cartagineses (Aníbal y su elefante), Roma
(legionario, Numancia, acueducto de Segovia, teatro de Mérida, Trajano) y visigodos (corona votiva de Guarrazar).
Convenciones de obj_base: origen en los PIES, cabeza en y ≈ -215 (radio 41)."""
import math
from functools import lru_cache

import numpy as np

import boceto as B
import obj_base as OB
from obj_a import colocar
from obj_base import *  # noqa: F401,F403
from obj_base import _rotar

OCRE = (196, 96, 58)
OCRE_CL = (220, 150, 96)
CARBON = (60, 52, 50)
ROCA = (186, 168, 140)
ROCA_OSC = (150, 132, 108)
PIEL_BRONCE = (214, 158, 112)
BRONCE = (190, 140, 70)
HIERRO = (150, 154, 164)
LANA = (196, 176, 140)
ROJO_ROMA = (186, 52, 46)
PURPURA = (120, 60, 110)
VERDE_MAR = (88, 150, 140)
BLANCO_R = (248, 244, 232)
NEGRO_R = (46, 40, 44)

_PELOS = {"negro": (60, 50, 50), "castano": (120, 80, 56), "rubio": (220, 176, 96), "canoso": (200, 196, 190), "pelirrojo": (190, 96, 50)}

# ------------------------------------------------------------------ sombreros nuevos (se enganchan al constructor de personas)
_orig_sombrero = OB.sombrero


def _turbante(cy, col, joya):
    P = curva([(-46, cy - 12), (-58, cy - 40), (-50, cy - 72), (-20, cy - 92), (20, cy - 92), (50, cy - 72), (58, cy - 40), (46, cy - 12), (0, cy - 22)], 6)
    ops = forma(P, col, 4.6, sp=7)
    for k in range(4):
        ops.append(T(curva([(-52 + 8 * k, cy - 22 - 16 * k), (0, cy - 40 - 14 * k), (52 - 10 * k, cy - 58 - 10 * k)], 5), 2.8, peso=0.03))
    return ops + forma(elip(0, cy - 44, 9, 11, 0, 1.0, 12), joya, 3.4, sp=4) + forma(pol((-4, cy - 54), (0, cy - 76), (6, cy - 54)), joya, 2.6, sp=2)


def _sombrero(nombre, cy=-215.0):
    if nombre == "galea":             # casco de legionario: casquete, guardanucas, carrilleras y cresta roja
        ops = forma([(-46, cy - 6), (-44, cy - 50), (0, cy - 70), (44, cy - 50), (46, cy - 6), (34, cy - 18), (-34, cy - 18)], HIERRO, 4.6, sp=8)
        ops += forma(pol((-46, cy - 14), (-58, cy + 2), (-44, cy + 30), (-32, cy + 6)), HIERRO, 4, sp=6)
        ops += forma(pol((46, cy - 14), (58, cy + 2), (44, cy + 30), (32, cy + 6)), HIERRO, 4, sp=6)
        ops += forma(curva([(-30, cy - 64), (-20, cy - 104), (20, cy - 108), (34, cy - 68)], 6) .tolist() + [(0, cy - 72)], ROJO_ROMA, 4.2, sp=6)
        return ops + [rayita(-40, cy - 30, 40, cy - 30, 3.2)]
    if nombre == "laurel":            # corona de laurel (emperador)
        ops = []
        for lado in (-1, 1):
            for k in range(5):
                a = math.radians(200 + 32 * k) if lado < 0 else math.radians(-20 - 32 * k)
                x, y = 42 * math.cos(a), cy - 18 + 26 * math.sin(a)
                ops += forma(elip(x, y, 13, 6, a + lado * 1.2, 1.0, 12), (110, 150, 80), 3.4, sp=4)
        return forma(elip(0, cy - 14, 43, 38, math.pi, 0.5, 26), (90, 70, 56), 4.4, cerrada=False, sp=7)[1:] + ops
    if nombre == "corona_goda":       # corona de oro con piedras
        ops = forma(pol((-42, cy - 30), (-44, cy - 70), (-24, cy - 50), (0, cy - 80), (24, cy - 50), (44, cy - 70), (42, cy - 30)), ORO, 4.6, sp=7)
        return ops + [R(circ(-22, cy - 40, 5, n=10), ROJO_CH, peso=0.02, sp=3), R(circ(0, cy - 42, 6, n=10), (70, 120, 190), peso=0.02, sp=3),
                      R(circ(22, cy - 40, 5, n=10), JADE, peso=0.02, sp=3)]
    if nombre == "turbante":          # turbante blanco: bulbo enrollado con pliegues en diagonal y joya
        return _turbante(cy, BLANCO_R, (70, 130, 110))
    if nombre == "turbante_verde":
        return _turbante(cy, (110, 160, 120), ORO)
    if nombre == "piel":              # melena despeinada (prehistoria)
        P = [(-46, cy + 20), (-52, cy - 10), (-44, cy - 44), (-20, cy - 58), (6, cy - 54), (30, cy - 60), (48, cy - 36), (52, cy - 4), (46, cy + 24),
             (36, cy - 6), (28, cy - 30), (0, cy - 34), (-26, cy - 30), (-36, cy - 4)]
        return forma(P, (120, 80, 56), 4.4, sp=7)
    if nombre.startswith("pelo_") and nombre[5:] in _PELOS:     # pelo corto por encima de la frente (no tapa los ojos)
        P = [(-42, cy - 4), (-45, cy - 30), (-30, cy - 47), (0, cy - 53), (30, cy - 47), (45, cy - 30), (42, cy - 4), (37, cy - 20), (20, cy - 28),
             (0, cy - 26), (-20, cy - 28), (-37, cy - 20)]
        return forma(P, _PELOS[nombre[5:]], 4.4, sp=7)
    if nombre == "celta":             # pelo largo y bigote rubio
        return forma(pol((-44, cy - 4), (-48, cy - 36), (-24, cy - 56), (20, cy - 56), (46, cy - 36), (44, cy - 4), (52, cy + 50), (36, cy + 46),
                         (34, cy - 14), (-34, cy - 14), (-36, cy + 46), (-52, cy + 50)), (220, 170, 90), 4.4, sp=7)
    if nombre == "gorro_frigio_fen":  # gorro cónico fenicio
        return forma(pol((-40, cy - 24), (-26, cy - 76), (6, cy - 104), (26, cy - 74), (40, cy - 24)), PURPURA, 4.6, sp=7) + [rayita(-40, cy - 28, 40, cy - 28, 3.4)]
    if nombre == "casco_cartago":
        ops = forma([(-46, cy - 10), (-42, cy - 52), (0, cy - 72), (42, cy - 52), (46, cy - 10), (30, cy - 20), (-30, cy - 20)], BRONCE, 4.6, sp=8)
        return ops + forma(pol((-8, cy - 70), (-24, cy - 112), (0, cy - 100), (24, cy - 112), (8, cy - 70)), (230, 220, 200), 3.8, sp=5)
    return _orig_sombrero(nombre, cy)


OB.sombrero = _sombrero


# ------------------------------------------------------------------ accesorios nuevos
def _acc_falcata(m, d):
    x, y = m
    hoja = curva([(x - 4, y - 6), (x + 10, y - 50), (x + 30, y - 96), (x + 22, y - 118), (x + 8, y - 96), (x - 10, y - 48)], 6)
    return forma(hoja, GRIS_CL, 4.2, sp=4) + [T(curva([(x - 14, y - 4), (x - 6, y + 14), (x + 12, y + 8)], 4), 5, peso=0.03)]


def _acc_hacha_piedra(m, d):
    x, y = m
    return forma(pol((x - 10, y - 50), (x + 14, y - 44), (x + 20, y + 6), (x + 2, y + 20), (x - 16, y + 4)), ROCA, 4.4, sp=5)


def _acc_scutum(m, d):
    x, y = m
    ops = forma(rect(x - 40, y - 70, x + 40, y + 60, 10), ROJO_ROMA, 4.8, sp=7)
    ops += forma(elip(x, y - 5, 14, 14, 0, 1.0, 14), ORO, 3.6, sp=4)
    return ops + [rayita(x - 30, y - 5, x - 16, y - 5, 3), rayita(x + 16, y - 5, x + 30, y - 5, 3), rayita(x, y - 60, x, y - 22, 3), rayita(x, y + 12, x, y + 50, 3)]


def _acc_caetra(m, d):                 # escudo redondo íbero
    x, y = m
    return forma(elip(x, y, 36, 36, 0, 1.0, 26), (170, 120, 80), 4.6, sp=7) + forma(elip(x, y, 10, 10, 0, 1.0, 12), BRONCE, 3.4, sp=4)


def _acc_pilum(m, d):
    x, y = m
    return [T(linea((x, y + 70), (x + 6, y - 170)), 5, peso=0.12), T(linea((x + 6, y - 170), (x + 9, y - 230)), 3.4, peso=0.05),
            R(pol((x + 3, y - 228), (x + 10, y - 252), (x + 16, y - 228)), GRIS_CL, peso=0.03, sp=3)]


def _acc_aquila(m, d):                 # estandarte del águila
    x, y = m
    ops = [T(linea((x, y + 80), (x + 2, y - 190)), 5, peso=0.12)]
    ops += forma(pol((x - 34, y - 196), (x - 10, y - 206), (x + 2, y - 222), (x + 14, y - 206), (x + 38, y - 196), (x + 14, y - 192), (x + 2, y - 184),
                     (x - 10, y - 192)), ORO, 4, sp=4)
    return ops + forma(rect(x - 26, y - 176, x + 30, y - 140, 3), ROJO_ROMA, 3.6, sp=5)


def _acc_cetro(m, d):
    x, y = m
    return [T(linea((x, y + 40), (x + 4, y - 110)), 6, peso=0.08)] + forma(elip(x + 4, y - 118, 12, 12, 0, 1.0, 12), ORO, 3.6, sp=4)


def _acc_rollo_ley(m, d):
    x, y = m
    return forma(rect(x - 24, y - 50, x + 24, y + 10, 4), CREMA, 3.8, sp=5) + [rayita(x - 14, y - 36 + 11 * k, x + 14, y - 36 + 11 * k, 2.4) for k in range(4)]


def _acc_anfora(m, d):
    x, y = m
    P = curva([(x - 8, y - 70), (x - 10, y - 56), (x - 26, y - 30), (x - 22, y + 10), (x, y + 40), (x + 22, y + 10), (x + 26, y - 30), (x + 10, y - 56),
               (x + 8, y - 70)], 5)
    return forma(P, OCRE_CL, 4.2, sp=6) + [T(arco_(x - 16, y - 54, 10, 90, 270, 8), 3.4, peso=0.02), T(arco_(x + 16, y - 54, 10, -90, 90, 8), 3.4, peso=0.02)]


def _acc_antorcha2(m, d):
    x, y = m
    return [T(linea((x, y + 14), (x + 4, y - 70)), 6, peso=0.05)] + forma(pol((x - 16, y - 70), (x - 6, y - 104), (x + 4, y - 92), (x + 10, y - 128), (x + 24, y - 70)),
                                                                           NARANJA, 3.6, sp=4)


def _acc_pincel_ocre(m, d):
    x, y = m
    return [T(linea((x, y + 8), (x + 30, y - 50)), 4.4, peso=0.04), R(circ(x + 32, y - 54, 7, n=10), OCRE, peso=0.02, sp=3)]


OB.ACC.update({"falcata": _acc_falcata, "hacha_piedra": _acc_hacha_piedra, "scutum": _acc_scutum, "caetra": _acc_caetra, "pilum": _acc_pilum,
               "aquila": _acc_aquila, "cetro": _acc_cetro, "rollo_ley": _acc_rollo_ley, "anfora": _acc_anfora, "antorcha2": _acc_antorcha2,
               "pincel_ocre": _acc_pincel_ocre})


# ------------------------------------------------------------------ prehistoria
@lru_cache(maxsize=None)
def humano_atapuerca(pose=0, cara="serio"):
    return persona((140, 100, 70), PIEL_BRONCE, "piel", cara, (14, 34), pose, traje="corta", acc_d="hacha_piedra")


@lru_cache(maxsize=None)
def pintor_altamira(pose=0):
    return persona((150, 110, 76), PIEL_BRONCE, "piel", "feliz", (20, 120), pose, traje="corta", acc_d="pincel_ocre", acc_i="antorcha2")


@lru_cache(maxsize=None)
def bisonte(color=OCRE, tam=1.0):
    """Bisonte al estilo del techo de Altamira: cuerpo rojo ocre, giba alta sobre los hombros, cabeza baja negra con barba y cuernos."""
    cuerpo = curva([(-146, -72), (-118, -104), (-60, -116), (-6, -134), (36, -170), (76, -166), (100, -138), (96, -96), (88, -60), (40, -48),
                    (-50, -52), (-120, -46)], 7)
    ops = forma(cuerpo, color, 6.4, peso=0.6, sp=10)
    ops += [R(curva([(-6, -134), (36, -170), (76, -166), (98, -136), (60, -128), (20, -122)], 5), CARBON, peso=0.08, sp=6)]      # giba oscura
    cabeza = curva([(94, -136), (122, -128), (146, -100), (152, -66), (140, -50), (122, -48), (108, -30), (96, -44), (90, -80)], 6)
    ops += forma(cabeza, CARBON, 5.4, sp=6)
    ops += [T(curva([(124, -124), (142, -146), (130, -160)], 4), 5, peso=0.04), punto(132, -96, 8)]
    ops += [R(circ(132, -96, 5, n=10), (240, 220, 190), peso=0.01, sp=3)]
    for x0, dx in ((-120, -14), (-88, 8), (50, -8), (78, 10)):
        ops += forma(pol((x0 - 11, -54), (x0 + 11, -54), (x0 + dx + 6, -6), (x0 + dx - 6, -6)), color, 4.8, sp=5)
        ops += forma(pol((x0 + dx - 9, -10), (x0 + dx + 9, -10), (x0 + dx + 7, 0), (x0 + dx - 7, 0)), CARBON, 3.6, sp=3)
    ops += [T(curva([(-144, -74), (-162, -52), (-158, -26)], 4), 4.6, peso=0.04)]
    ops += [T(curva([(-110, -96), (-70, -84), (-30, -90)], 4), 3.2, peso=0.04, v=180), T(curva([(-40, -70), (0, -64), (40, -74)], 4), 3.2, peso=0.04, v=180)]
    return Dib(colocar(ops, 0, 0, tam) if tam != 1.0 else ops)


@lru_cache(maxsize=None)
def cueva():
    """Boca de cueva: roca con hueco oscuro."""
    ops = forma(curva([(-200, 0), (-210, -110), (-150, -200), (-40, -236), (80, -226), (180, -170), (214, -70), (206, 0)], 7), ROCA, 6, peso=0.6, sp=11)
    ops += forma(curva([(-110, 0), (-120, -80), (-70, -140), (10, -156), (90, -132), (126, -70), (118, 0)], 7), (90, 74, 70), 5, peso=0.5, sp=9)
    ops += [T(curva([(-160, -120), (-120, -150)], 3), 3.4, peso=0.04), T(curva([(140, -160), (176, -120)], 3), 3.4, peso=0.04),
            T(curva([(-190, -40), (-170, -60)], 3), 3.4, peso=0.04)]
    return Dib(ops)


@lru_cache(maxsize=None)
def techo_cueva():
    """Techo de la cueva de Altamira: gran roca clara y abombada, con grietas y relieves (sobre ella se pinta el bisonte)."""
    ops = forma(curva([(-330, -30), (-350, -150), (-300, -260), (-160, -320), (0, -330), (170, -320), (310, -250), (350, -140), (330, -20), (200, 10),
                       (0, 20), (-200, 10)], 8), (222, 196, 160), 6, peso=0.6, sp=12)
    ops += [T(curva([(-260, -230), (-200, -180), (-210, -120)], 4), 3, peso=0.03, v=150), T(curva([(220, -270), (250, -200), (290, -170)], 4), 3, peso=0.03, v=150),
            T(curva([(-120, -40), (-60, -20), (10, -40)], 4), 3, peso=0.03, v=150), T(curva([(120, -60), (180, -30), (260, -50)], 4), 3, peso=0.03, v=150)]
    for x, y, r in ((-240, -80, 50), (230, -110, 46), (-30, -270, 40)):
        ops += [R(B.elip(x, y, r, r * 0.6, 0, 1.0, 20), (206, 176, 140), peso=0.02, sp=8)]
    return Dib(ops)


@lru_cache(maxsize=None)
def craneo():
    ops = forma(curva([(-70, -40), (-80, -100), (-50, -150), (10, -166), (66, -140), (84, -90), (74, -40), (40, -24), (20, 0), (-30, 0), (-50, -24)], 6),
                (236, 226, 200), 5.4, peso=0.5, sp=9)
    ops += forma(elip(-26, -86, 18, 16, 0, 1.0, 16), NEGRO_R, 4, sp=5) + forma(elip(28, -86, 18, 16, 0, 1.0, 16), NEGRO_R, 4, sp=5)
    ops += forma(pol((-2, -64), (-10, -44), (6, -44)), NEGRO_R, 3.4, sp=3)
    ops += [rayita(-24 + 12 * k, -22, -24 + 12 * k, -6, 3) for k in range(5)] + [T(linea((-60, -110), (70, -112)), 3.6, peso=0.04)]
    return Dib(ops)


# ------------------------------------------------------------------ íberos y celtas
@lru_cache(maxsize=None)
def ibero(pose=0, cara="serio"):
    return persona((200, 190, 170), PIEL_BRONCE, "pelo_negro", cara, (16, 40), pose, traje="corta", faja=OCRE, acc_d="falcata", acc_i="caetra")


@lru_cache(maxsize=None)
def celta(pose=0, cara="feliz"):
    return persona((90, 130, 90), PIEL_ROSA, "celta", cara, (14, 30), pose, traje="corta", faja=(150, 100, 60), bigote=True, acc_d="lanza")


@lru_cache(maxsize=None)
def dama_elche():
    """La Dama de Elche (s. V-IV a. C.): busto con los grandes rodetes a los lados de la cara, mitra y collares."""
    ops = forma(curva([(-110, 0), (-96, -70), (-60, -110), (60, -110), (96, -70), (110, 0)], 6), (200, 160, 120), 5.4, peso=0.5, sp=9)     # hombros y manto
    ops += forma(elip(0, -168, 40, 52, 0, 1.0, 30), (222, 184, 146), 5.2, peso=0.4, sp=8)                                                    # cara
    ops += forma(curva([(-46, -200), (-40, -248), (0, -270), (40, -248), (46, -200)], 6).tolist() + [(0, -214)], (188, 140, 100), 4.8, sp=7)   # mitra
    for lado in (-1, 1):                                                                                                                     # rodetes
        cx = lado * 74
        ops += forma(elip(cx, -168, 34, 40, 0, 1.0, 26), (196, 150, 108), 5, sp=7)
        ops += [T(elip(cx, -168, 22, 27, 0, 1.0, 22), 3.4, peso=0.04), T(elip(cx, -168, 10, 12, 0, 1.0, 14), 3.2, peso=0.03)]
    ops += [T(curva([(-20, -176), (-12, -180), (-4, -176)], 3), 3.2, peso=0.02), T(curva([(4, -176), (12, -180), (20, -176)], 3), 3.2, peso=0.02),
            T(linea((0, -170), (-4, -150), (4, -148)), 3, peso=0.02), T(linea((-10, -134), (10, -134)), 3.2, peso=0.02)]
    for k in range(3):                                                                                                                      # collares
        ops += [T(arco_(0, -120 + 14 * k, 54 - 4 * k, 20, 160, 14), 3.6, peso=0.04)]
        ops += [R(circ(-30 + 30 * j, -84 + 14 * k, 6, n=10), ORO, peso=0.01, sp=3) for j in range(3)]
    return Dib(ops)


# ------------------------------------------------------------------ fenicios, griegos, cartagineses
@lru_cache(maxsize=None)
def fenicio(pose=0, cara="feliz"):
    return persona(PURPURA, PIEL_BRONCE, "gorro_frigio_fen", cara, (18, 30), pose, barba=(130, 96, 70), faja=ORO, acc_d="anfora")


@lru_cache(maxsize=None)
def barco_fenicio(f=0, vela=PURPURA):
    """Galera fenicia: proa con cabeza de caballo, vela a rayas, remos."""
    ops = forma(curva([(-150, -60), (-120, -10), (0, 6), (120, -10), (150, -70)], 6).tolist() + [(130, -62), (0, -44), (-130, -50)], (150, 100, 66), 5.4, peso=0.5, sp=9)
    ops += forma(curva([(150, -70), (176, -110), (200, -112), (196, -92), (178, -88)], 5), (150, 100, 66), 4.6, sp=6) + [punto(188, -102, 7)]   # caballo
    ops += forma(curva([(-150, -60), (-176, -96), (-170, -120)], 4).tolist() + [(-156, -90)], (150, 100, 66), 4.4, sp=5)
    ops += [T(linea((0, -44), (0, -250)), 5.4, peso=0.1)]
    vela_P = [(-80, -236), (80, -236), (70, -86), (-70, -86)]
    ops += forma(vela_P, CREMA, 4.6, peso=0.3, sp=8)
    for k in range(4):
        ops += [R(pol((-76 + 38 * k, -232), (-58 + 38 * k, -232), (-52 + 35 * k, -90), (-68 + 35 * k, -90)), vela, peso=0.03, sp=5)]
    for k in range(7):
        a = 0.25 * math.sin(f * 1.3 + k * 0.7)
        x = -100 + 33 * k
        ops += [T(linea((x, -30), (x - 18 + 30 * a, 36)), 3.6, peso=0.02)]
    for k in range(5):
        ops += forma(elip(-80 + 40 * k, -46, 14, 14, 0, 1.0, 12), (176, 70, 60) if k % 2 else (70, 110, 160), 3.4, sp=4)          # escudos
    return Dib(ops)


@lru_cache(maxsize=None)
def griego(pose=0):
    return persona((236, 232, 220), PIEL_ROSA, "casco_griego", "feliz", (18, 30), pose, traje="corta", faja=(70, 110, 170), acc_d="lanza", barba=(120, 90, 60))


@lru_cache(maxsize=None)
def cartagines(pose=0, cara="enojo"):
    return persona((150, 70, 110), PIEL_BRONCE, "casco_cartago", cara, (16, 30), pose, traje="armadura", faja=BRONCE, acc_d="lanza", barba=(120, 86, 64))


@lru_cache(maxsize=None)
def elefante(pose=0, jinete=True):
    """Elefante de guerra de Aníbal (4 poses de paso): cabeza grande, oreja, trompa gruesa, colmillos; torrecilla y conductor."""
    p = pose % 4
    col = (160, 156, 160)
    col_cl = (186, 180, 184)
    offs = [(-16, 10, 14, -10), (0, -14, -12, 14), (16, -10, -14, 10), (0, 14, 12, -14)][p]
    ops = []
    for x, dx, lejos in zip((-104, -54, 46, 96), offs, (True, False, True, False)):          # patas (las de atrás, más oscuras)
        ops += forma(pol((x - 24, -110), (x + 24, -110), (x + 23 + dx, -6), (x - 23 + dx, -6)), (140, 134, 140) if lejos else col, 5, sp=7)
        ops += [T(linea((x - 16 + dx, -6), (x + 16 + dx, -6)), 4, peso=0.02)]
    ops += forma(elip(-20, -160, 136, 82, -0.04, 1.0, 40), col, 6.2, peso=0.7, sp=11)                                  # cuerpo
    sw = [0.0, 0.18, 0.0, -0.18][p]
    tr = []
    for k in range(9):                                                                                                 # trompa (gruesa, se curva)
        u = k / 8
        a = -1.2 + 1.9 * u + sw * u
        tr.append((150 + 46 * math.sin(a * 0.6) + 34 * u, -150 + 120 * u))
    tr = np.array(tr)
    w = np.linspace(22, 9, len(tr))
    izq = tr + np.stack([-w, np.zeros_like(w)], 1)
    der = tr + np.stack([w, np.zeros_like(w)], 1)
    ops += forma(np.vstack([izq, der[::-1]]), col, 5, sp=7)
    ops += forma(elip(118, -184, 62, 58, 0, 1.0, 30), col, 5.6, peso=0.4, sp=9)                                        # cabeza
    ops += forma(curva([(96, -230), (40, -226), (22, -170), (46, -116), (92, -126), (100, -170)], 6), col_cl, 5, sp=8)   # oreja
    ops += [T(curva([(56, -206), (44, -170), (60, -136)], 4), 3, peso=0.03)]
    ops += forma(curva([(148, -146), (176, -138), (204, -150), (196, -132), (166, -124), (146, -130)], 5), BLANCO_R, 4.2, sp=4)   # colmillo
    ops += [punto(136, -196, 9), T(arco_(136, -200, 14, 200, 330, 6), 3.4, peso=0.02)]
    ops += [T(curva([(-150, -170), (-176, -140), (-180, -100)], 4), 4.4, peso=0.03), R(elip(-180, -96, 6, 10, n=10), CARBON, peso=0.01, sp=3)]
    ops += forma(curva([(-110, -226), (-60, -238), (10, -236), (60, -222), (50, -170), (-100, -170)], 6), ROJO_CH, 4.8, sp=7)     # manta
    ops += [T(curva([(-104, -194), (-30, -200), (52, -190)], 4), 3.4, peso=0.03)]
    ops += forma(rect(-76, -312, 20, -236, 6), (176, 120, 60), 5, sp=7)                                               # torrecilla
    ops += [rayita(-60, -300, -60, -246, 3.4), rayita(-28, -300, -28, -246, 3.4), rayita(4, -300, 4, -246, 3.4)]
    if jinete:
        r = persona((150, 70, 110), PIEL_BRONCE, "casco_cartago", "enojo", (30, 110), pose, traje="corta", acc_d="lanza")
        ops += colocar(list(r.ops), -28, -296, 0.5)
    return Dib(ops)


@lru_cache(maxsize=None)
def anibal(pose=0, cara="serio"):
    return persona((140, 60, 70), PIEL_BRONCE, "casco_cartago", cara, (20, 70), pose, traje="armadura", faja=ORO, barba=(110, 80, 60), acc_d="espada")


# ------------------------------------------------------------------ Roma
@lru_cache(maxsize=None)
def legionario(pose=0, cara="serio", estandarte=False):
    return persona(ROJO_ROMA, PIEL_ROSA, "galea", cara, (12, 40 if estandarte else 26), pose, traje="armadura", faja=BRONCE,
                   acc_d="aquila" if estandarte else "pilum", acc_i="scutum")


@lru_cache(maxsize=None)
def numantino(pose=0, cara="enojo"):
    return persona((150, 120, 90), PIEL_BRONCE, "celta", cara, (40, 60), pose, traje="corta", bigote=True, acc_d="falcata", acc_i="caetra")


@lru_cache(maxsize=None)
def emperador_romano(pose=0, cara="serio"):
    return persona(BLANCO_R, PIEL_ROSA, "laurel", cara, (16, 40), pose, traje="tunica", faja=PURPURA, cuello=PURPURA, acc_d="rollo_ley")


@lru_cache(maxsize=None)
def acueducto(arcos=6, pisos=2):
    """Acueducto de Segovia: dos pisos de arcos de granito."""
    ops = []
    w = 60
    x0 = -arcos * w / 2
    alto1, alto2 = 170, 90
    ops += forma(rect(x0 - 8, -alto1 - alto2 - 26, x0 + arcos * w + 8, -alto1 - alto2 - 4, 3), ROCA, 4.6, sp=8)
    for piso, (yb, h) in enumerate(((0, alto1), (-alto1, alto2))):
        n = arcos if piso == 0 else arcos * 2
        ww = arcos * w / n
        for k in range(n):
            xa = x0 + k * ww
            P = [(xa, yb), (xa, yb - h), (xa + ww, yb - h), (xa + ww, yb)]
            ops += [R(pol(*P), ROCA if piso == 0 else (196, 180, 150), peso=0.04, sp=7)]
            r = ww * 0.32
            arco = [(xa + ww / 2 - r, yb)] + list(arco_(xa + ww / 2, yb - h * 0.62, r, 180, 360, 10)) + [(xa + ww / 2 + r, yb)]
            ops += forma(arco, PAPEL_HUECO, 3.6, sp=5)
        ops += [T(linea((x0, yb - h), (x0 + arcos * w, yb - h)), 4.4, peso=0.05)]
        ops += [T(linea((x0, yb), (x0, yb - h)), 4.4, peso=0.04), T(linea((x0 + arcos * w, yb), (x0 + arcos * w, yb - h)), 4.4, peso=0.04)]
    return Dib(ops)


PAPEL_HUECO = (226, 236, 236)


@lru_cache(maxsize=None)
def teatro_romano():
    """Teatro romano de Mérida: graderío semicircular (cávea) delante del frente escénico de dos órdenes de columnas."""
    ops = forma(rect(-170, -230, 170, -110, 3), (226, 206, 170), 5, peso=0.4, sp=9)                 # frente escénico
    for piso, (yb, h) in enumerate(((-110, 70), (-180, 50))):
        for k in range(6):
            x = -140 + 56 * k
            ops += forma(rect(x - 11, yb - h, x + 11, yb, 2), BLANCO_R, 3.8, sp=4)
            ops += forma(rect(x - 16, yb - h - 8, x + 16, yb - h, 2), BLANCO_R, 3.4, sp=4)
        ops += forma(rect(-176, yb - h - 18, 176, yb - h - 6, 2), ROCA, 3.8, sp=5)
    ops += forma(curva([(-30, -110), (-30, -150), (0, -168), (30, -150), (30, -110)], 5), (120, 90, 70), 4, sp=5)
    for k in range(5):                                                                                # gradas
        r = 230 - 26 * k
        ops += forma(np.vstack([arco_(0, -110, r, 0, 180, 30), arco_(0, -110, r - 22, 180, 0, 30)]) * (1, 0.42) + (0, -64),
                     ROCA if k % 2 else (210, 192, 160), 3.6, sp=6)
    return Dib(ops)


@lru_cache(maxsize=None)
def calzada_hito():
    """Miliario romano (columna con inscripción)."""
    ops = forma(rect(-30, -150, 30, 0, 8), ROCA, 5, sp=7) + forma(rect(-40, -20, 40, 0, 3), ROCA_OSC, 4.4, sp=6)
    return Dib(ops + [rayita(-18, -120 + 16 * k, 18, -120 + 16 * k, 3) for k in range(4)])


# ------------------------------------------------------------------ visigodos
@lru_cache(maxsize=None)
def rey_godo(pose=0, cara="serio"):
    return persona((70, 90, 150), PIEL_ROSA, "corona_goda", cara, (16, 40), pose, traje="tunica", faja=ORO, barba=(160, 110, 60), cuello=ORO, acc_d="cetro")


@lru_cache(maxsize=None)
def noble_godo(pose=0, cara="enojo", color=(130, 60, 60)):
    return persona(color, PIEL_ROSA, "pelo_rubio", cara, (16, 60), pose, traje="tunica", faja=ORO, barba=(200, 150, 80), acc_d="espada")


@lru_cache(maxsize=None)
def corona_votiva():
    """Corona votiva de Recesvinto (tesoro de Guarrazar): aro de oro con piedras, cadenas, letras colgantes y una cruz."""
    ops = []
    for k in range(4):                                                                                                   # cadenas
        x = -60 + 40 * k
        ops += [T(linea((x * 0.5, -250), (x, -160)), 3, peso=0.04)]
    ops += forma(elip(0, -250, 14, 10, 0, 1.0, 12), ORO, 3.4, sp=4)
    ops += forma(curva([(-90, -150), (-86, -100), (0, -90), (86, -100), (90, -150), (0, -164)], 6), ORO, 5.4, peso=0.4, sp=8)
    for k in range(7):
        x = -72 + 24 * k
        ops += forma(elip(x, -126, 7, 9, 0, 1.0, 10), (ROJO_CH, (70, 120, 190), JADE)[k % 3], 3, sp=3)
    for k in range(7):                                                                                                   # pinjantes
        x = -72 + 24 * k
        ops += [T(linea((x, -96), (x, -60)), 2.6, peso=0.03)] + forma(elip(x, -52, 6, 9, 0, 1.0, 10), ORO, 3, sp=3)
    ops += [T(linea((0, -96), (0, -30)), 3, peso=0.03)] + forma(pol((-6, -36), (6, -36), (6, -24), (20, -24), (20, -12), (6, -12), (6, 14), (-6, 14), (-6, -12),
                                                                     (-20, -12), (-20, -24), (-6, -24)), ORO, 3.6, sp=3)
    return Dib(ops)
