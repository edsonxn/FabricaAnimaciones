# -*- coding: utf-8 -*-
"""Dibujos de boceto para «La historia de Egipto» (v2) 2/3: MONUMENTOS, OBJETOS y DIOSES.
Pirámides (escalonada de Saqqara, Gran Pirámide, las tres de Guiza), Gran Esfinge, templo de Karnak, columna de papiro, obelisco,
coloso sentado, Abu Simbel, tumba del Valle de los Reyes, sarcófago, máscara y tesoro de Tutankamón, disco de Atón, cartucho (y cartucho
borrado), paleta de Narmer, corona doble, jeroglíficos, papiro, ojo de Horus, anj, escarabajo, tratado de Kadesh, piedra de Rosetta,
Faro y Biblioteca de Alejandría, estante de rollos, moneda ptolemaica, ciudadela de Saladino, mezquita, minarete, El Cairo, presa de Asuán,
torre de El Cairo, rascacielos, gavilla, saco de grano, ánfora, sequía, crecida, banderas, águila de Saladino y dioses (Amón, Ra, Anubis,
Osiris, Bastet). Origen en la BASE del objeto (y = 0 abajo, x centrado)."""
import math
from functools import lru_cache

import numpy as np

import obj_eg1 as E1
from obj_a import colocar
from obj_base import *  # noqa: F401,F403
from obj_eg1 import (ARENISCA, ARENISCA_OS, BLANCO_EG, BRONCE, CALIZA, GRANITO, HIERRO, KOHL, LAPIS, LINO, NEGRO_EG, OCRE_R, ORO_EG, ORO_OS, PIEL_EG,
                     TURQ, VERDE_NILO, persona)

SOMBRA_P = (206, 182, 140)
PIEDRA_OS = (150, 132, 108)


def _destello(x, y, r0=12, r1=28, n=8, w=2.8):
    return [T(linea((x + r0 * math.cos(a), y + r0 * math.sin(a)), (x + r1 * math.cos(a), y + r1 * math.sin(a))), w, peso=0.02)
            for a in np.linspace(0, 2 * math.pi, n, endpoint=False)]


# ------------------------------------------------------------------ pirámides
@lru_cache(maxsize=None)
def piramide_escalonada():
    """Pirámide escalonada de Djoser en Saqqara (seis escalones), con su cara en sombra."""
    ops = forma(rect(-150, -10, 150, 0, 3), ARENISCA_OS, 4.0, sp=5)
    pisos = [(126, 100, -10, -44), (104, 82, -44, -76), (86, 66, -76, -106), (70, 52, -106, -132), (56, 40, -132, -156), (44, 28, -156, -178)]
    for wi, ws, yi, ys in pisos:
        ops += forma(trap(-ws, 0, ys, -wi, 0, yi), SOMBRA_P, 4.4, sp=6)
        ops += forma(trap(0, ws, ys, 0, wi, yi), CALIZA, 4.4, sp=6)
        ym = (yi + ys) / 2
        ops += [rayita(-wi * 0.85, ym, wi * 0.85, ym, 2.4)]
        for k in range(-3, 4):
            ops += [rayita(k * wi / 4.2, yi, k * wi / 4.2, ym, 2.0)]
    return Dib(ops + [trazo((0, -178), (0, -10), w=4.4)])


@lru_cache(maxsize=None)
def gran_piramide(brillo=True, bloques=10):
    """La Gran Pirámide de Keops: caliza blanca pulida, cara en sombra y piramidión dorado."""
    ops = forma(curva([(-170, 0), (-80, -7), (0, 0), (80, -6), (170, 0)], 8).tolist() + [(170, 6), (-170, 6)], ARENISCA, 4.4, sp=6)
    ops += forma(pol((-150, 0), (0, -230), (0, 0)), SOMBRA_P, 5.0, sp=7)
    ops += forma(pol((0, -230), (150, 0), (0, 0)), CALIZA, 5.0, sp=7)
    ops += [trazo((0, -230), (0, 0), w=5.0)]
    for yh in np.linspace(-20, -196, bloques):
        f = (230 + yh) / 230
        ops += [rayita(-146 * f, yh, 146 * f, yh, 2.4)]
    ops += forma(pol((-19, -201), (0, -230), (19, -201)), ORO_EG, 4.4, sp=5)
    if brillo:
        ops += _destello(0, -232)
    return Dib(ops)


@lru_cache(maxsize=None)
def piramides_guiza():
    """Las tres pirámides de Guiza (Keops, Kefrén con su remate de caliza, Micerino) y tres pirámides de reinas."""
    ops = forma(curva([(-330, 0), (-160, -8), (0, 0), (160, -6), (330, 0)], 8).tolist() + [(330, 8), (-330, 8)], ARENISCA, 4.4, sp=6)
    for cx, a, h, gorro in ((-150, 120, 190, False), (60, 112, 182, True), (230, 66, 104, False)):
        ops += forma(pol((cx - a, 0), (cx, -h), (cx, 0)), SOMBRA_P, 4.8, sp=7)
        ops += forma(pol((cx, -h), (cx + a, 0), (cx, 0)), ARENISCA if gorro else CALIZA, 4.8, sp=7)
        ops += [trazo((cx, -h), (cx, 0), w=4.6)]
        for yh in np.linspace(-18, -h + 24, 7):
            f = (h + yh) / h
            ops += [rayita(cx - a * f * 0.96, yh, cx + a * f * 0.96, yh, 2.2)]
        if gorro:
            ops += forma(pol((cx - a * 0.2, -h * 0.8), (cx, -h), (cx + a * 0.2, -h * 0.8)), CALIZA, 4.0, sp=4)
    for k in range(3):
        cx = 300 + 0 * k - 36 * (2 - k) - 80
        ops += forma(pol((cx + 60 - 18, 0), (cx + 60, -30), (cx + 60 + 18, 0)), CALIZA, 3.6, sp=4)
    return Dib(ops)


# ------------------------------------------------------------------ la Gran Esfinge
@lru_cache(maxsize=None)
def esfinge():
    """La Gran Esfinge tumbada (de perfil hacia la derecha): cuerpo de león, patas delanteras extendidas y cabeza de rey con nemes."""
    ops = forma(rect(-240, -12, 250, 0, 3), ARENISCA_OS, 4.0, sp=5)
    cuerpo = curva([(-230, -12), (-236, -60), (-210, -104), (-150, -122), (-60, -124), (20, -120), (70, -150), (80, -190), (150, -196), (160, -150),
                    (150, -108), (140, -70), (150, -44), (240, -40), (248, -24), (240, -12)], 6)
    ops += forma(cuerpo, ARENISCA, 5.2, peso=0.6, sp=9)
    ops += forma(curva([(60, -44), (230, -44), (238, -30), (226, -20), (60, -22)], 5), ARENISCA, 4.4, sp=6)       # pata delantera
    for x in (212, 222, 232):
        ops += [rayita(x, -40, x - 2, -24, 2.4)]
    ops += forma(curva([(-150, -40), (-100, -46), (-60, -40), (-60, -20), (-150, -22)], 5), SOMBRA_P, 4.0, sp=5)     # pata trasera
    ops += [T(curva([(-236, -40), (-260, -30), (-250, -12)], 4), 4.4, peso=0.03)]                                         # cola
    ops += [T(curva([(-200, -110), (-120, -96), (-40, -100)], 5), 2.6, peso=0.03), T(curva([(-180, -80), (-110, -70), (-40, -76)], 5), 2.6, peso=0.03)]
    # cabeza con nemes (de frente), grande para que se lea
    cab = forma(curva([(-48, 62), (-58, -2), (-40, -44), (0, -60), (40, -44), (58, -2), (48, 62), (30, 38), (-30, 38)], 6), (214, 186, 120), 5, sp=7)
    cab += [T(curva([(-40, -40), (0, -54), (40, -40)], 5), 2.6, peso=0.02), T(curva([(-34, -32), (0, -46), (34, -32)], 5), 2.6, peso=0.02)]
    for s_ in (-1, 1):
        cab += [T(linea((s_ * 34, y), (s_ * 52, y + 2)), 2.6, peso=0.02) for y in (6, 20, 34, 48)]
    cab += forma(elip(0, 0, 30, 36, 0, 1.0, 24), ARENISCA, 4.8, sp=6)
    cab += [T(curva([(-18, -8), (-10, -12), (-4, -8)], 3), 3.6, peso=0.02), T(curva([(4, -8), (10, -12), (18, -8)], 3), 3.6, peso=0.02)]
    cab += [punto(-11, -7, 6), punto(11, -7, 6), T(linea((0, -4), (-2, 12)), 3, peso=0.02), T(linea((-10, 22), (10, 22)), 3.4, peso=0.02)]
    cab += [T(curva([(-6, -44), (-2, -58), (4, -52)], 3), 3.6, peso=0.02)]
    ops += colocar(cab, 114, -200, 1.4)
    return Dib(ops)


# ------------------------------------------------------------------ templos y estatuas
@lru_cache(maxsize=None)
def columna_papiro(h=200, col=ARENISCA):
    ops = forma(rect(-24, -h, 24, -18, 4), col, 4.6, sp=6)
    ops += forma(curva([(-24, -h), (-46, -h - 30), (-40, -h - 46), (40, -h - 46), (46, -h - 30), (24, -h)], 5), col, 4.6, sp=6)
    ops += forma(rect(-30, -18, 30, 0, 3), col, 4.2, sp=5)
    for y in (-h + 20, -h + 34, -60, -46):
        ops += [rayita(-23, y, 23, y, 2.2)]
    ops += [R(rect(-20, -h + 60, 20, -h + 120, 3), OCRE_R, peso=0.02, sp=4), R(rect(-20, -h + 130, 20, -h + 150, 3), LAPIS, peso=0.02, sp=4)]
    return Dib(ops)


@lru_cache(maxsize=None)
def templo_karnak():
    """Templo de Karnak: dos pilonos con mástiles y banderolas, la puerta, columnas papiriformes detrás y un obelisco."""
    ops = []
    ops += colocar(list(obelisco(150).ops), -10, -20, 1.0)
    for cx in (-60, 40):
        ops += colocar(list(columna_papiro(150).ops), cx, -18, 0.8)
    for lado in (-1, 1):
        x0, x1 = (-230, -50) if lado < 0 else (50, 230)
        ops += forma(trap(x0 + 18, x1 - 18, -230, x0, x1, 0), ARENISCA, 5.0, sp=8)
        ops += forma(rect(x0 + 14, -242, x1 - 14, -228, 3), ARENISCA_OS, 4.0, sp=5)
        for k in range(2):
            x = x0 + 50 + 70 * k
            ops += [T(linea((x, -6), (x, -280)), 4.2, peso=0.06)] + forma(pol((x, -280), (x + 36, -270), (x, -258)), (200, 70, 60) if k else LAPIS, 3.4, sp=3)
        for y in (-190, -150, -110):
            ops += [rayita(x0 + 30, y, x1 - 30, y, 2.0)]
        ops += forma(rect((x0 + x1) / 2 - 36, -130, (x0 + x1) / 2 + 36, -60, 3), (236, 214, 170), 3.6, sp=4)
        ops += [punto((x0 + x1) / 2 - 12, -100, 7), punto((x0 + x1) / 2 + 12, -100, 7), T(linea(((x0 + x1) / 2 - 20, -80), ((x0 + x1) / 2 + 20, -80)), 2.6, peso=0.02)]
    ops += forma(rect(-50, -190, 50, 0, 3), ARENISCA_OS, 4.6, sp=6)
    ops += forma(rect(-30, -140, 30, 0, 3), (110, 86, 66), 4.4, sp=6)
    ops += forma(elip(0, -170, 24, 10, 0, 1.0, 16), ORO_EG, 3.4, sp=3)
    ops += [T(curva([(-46, -170), (-24, -176)], 2), 3, peso=0.02), T(curva([(46, -170), (24, -176)], 2), 3, peso=0.02)]
    return Dib(ops)


@lru_cache(maxsize=None)
def obelisco(h=280):
    ops = forma(pol((-24, 0), (-16, -h + 30), (0, -h), (16, -h + 30), (24, 0)), GRANITO, 4.8, sp=7)
    ops += forma(pol((-16, -h + 30), (0, -h), (16, -h + 30)), ORO_EG, 4.0, sp=4)
    ops += forma(rect(-34, -12, 34, 0, 3), ARENISCA_OS, 4.0, sp=5)
    for k in range(5):
        y = -40 - k * (h - 90) / 5
        ops += [punto(-4, y, 5), T(linea((-6, y - 14), (6, y - 14)), 2.2, peso=0.02)]
    return Dib(ops + _destello(0, -h, 10, 24, 8, 2.4))


@lru_cache(maxsize=None)
def coloso(corona="pschent", col=ARENISCA, sombra=ARENISCA_OS):
    """Coloso sentado (de frente) de un faraón en su trono de piedra: nemes y doble corona, manos sobre las rodillas."""
    ops = forma(rect(-96, -40, 96, 0, 4), sombra, 4.6, sp=6)                                       # pedestal
    ops += forma(rect(-84, -250, 84, -40, 6), sombra, 4.6, sp=7)                                   # trono detrás
    ops += forma(rect(-46, -150, -8, -40, 4), col, 4.6, sp=6) + forma(rect(8, -150, 46, -40, 4), col, 4.6, sp=6)            # piernas
    ops += forma(rect(-50, -56, -4, -40, 3), col, 4, sp=4) + forma(rect(4, -56, 50, -40, 3), col, 4, sp=4)                  # pies
    ops += forma(rect(-56, -176, 56, -144, 6), col, 4.6, sp=6)                                     # regazo
    ops += forma(pol((-24, -176), (24, -176), (30, -100), (-30, -100)), ORO_EG if col == ARENISCA else col, 3.8, sp=4)      # delantal
    ops += forma(trap(-50, 50, -300, -40, 40, -176), col, 5, sp=7)                                 # torso
    for s_ in (-1, 1):
        ops += forma(pol((s_ * 50, -296), (s_ * 64, -280), (s_ * 56, -180), (s_ * 40, -160), (s_ * 34, -176), (s_ * 44, -200)), col, 4.4, sp=5)   # brazos
        ops += forma(elip(s_ * 40, -166, 12, 9, 0, 1.0, 12), col, 3.6, sp=3)
    ops += [T(arco_(0, -296, 38, 20, 160, 12), 3.6, peso=0.03), R(np.array(arco_(0, -296, 38, 20, 160, 12).tolist() + arco_(0, -296, 26, 160, 20, 12).tolist()), ORO_EG, peso=0.02, sp=3)]
    cy = -340
    ops += forma(curva([(-50, cy + 26), (-56, cy - 26), (-40, cy - 60), (0, cy - 70), (40, cy - 60), (56, cy - 26), (50, cy + 26), (36, cy - 10), (0, cy - 30),
                        (-36, cy - 10)], 5), sombra, 4.6, sp=6)
    ops += forma(pol((-50, cy + 6), (-62, cy + 60), (-38, cy + 64), (-38, cy + 4)), sombra, 4, sp=5) + forma(pol((50, cy + 6), (62, cy + 60), (38, cy + 64), (38, cy + 4)), sombra, 4, sp=5)
    ops += forma(elip(0, cy + 6, 30, 34, 0, 1.0, 22), (240, 222, 180), 4.6, sp=6)
    ops += [punto(-11, cy, 7), punto(11, cy, 7), T(linea((-8, cy + 22), (8, cy + 22)), 3, peso=0.02)]
    ops += forma(pol((-6, cy + 40), (6, cy + 40), (5, cy + 66), (-5, cy + 66)), sombra, 3, sp=2)
    if corona == "pschent":
        ops += forma(curva([(-16, cy - 60), (-14, cy - 96), (0, cy - 116), (14, cy - 96), (16, cy - 60)], 5), col, 4.2, sp=5)
        ops += forma(pol((-30, cy - 40), (-32, cy - 70), (22, cy - 70), (22, cy - 104), (32, cy - 104), (32, cy - 40)), col, 4.4, sp=5)
    for k in range(3):
        ops += [rayita(-60, -120 + 30 * k, -50, -120 + 30 * k, 2)]
    return Dib(ops)


@lru_cache(maxsize=None)
def abu_simbel():
    """Fachada del gran templo de Abu Simbel: la roca tallada con cuatro colosos sentados de Ramsés II y la puerta."""
    ops = forma(pol((-330, 0), (-310, -300), (-150, -330), (150, -334), (310, -300), (330, 0)), ARENISCA, 5.2, peso=0.6, sp=9)
    ops += forma(rect(-280, -310, 280, -286, 3), ARENISCA_OS, 4.0, sp=5)
    for k in range(12):
        ops += forma(elip(-264 + 48 * k, -322, 12, 14, 0, 1.0, 12), (220, 190, 140), 3.0, sp=3)                     # babuinos del friso
    for cx in (-230, -90, 90, 230):
        figura = colocar(list(coloso("pschent").ops), cx, 0, 0.98)
        ops += figura
    ops += forma(rect(-28, -150, 28, 0, 3), (90, 70, 56), 4.4, sp=5)
    ops += forma(elip(0, -190, 14, 22, 0, 1.0, 14), ORO_EG, 3.6, sp=3)                                                # Ra-Horajti
    return Dib(ops)


@lru_cache(maxsize=None)
def tumba_valle():
    """Colina del Valle de los Reyes con la entrada de una tumba excavada en la roca."""
    ops = forma(curva([(-260, 0), (-220, -120), (-140, -200), (-40, -236), (60, -210), (160, -150), (240, -70), (270, 0)], 8), ARENISCA, 5, sp=8)
    ops += [T(curva([(-200, -60), (-120, -80), (-60, -70)], 4), 2.4, peso=0.02), T(curva([(80, -120), (150, -100)], 3), 2.4, peso=0.02)]
    ops += forma(rect(-40, -130, 40, 0, 3), (60, 50, 50), 5, sp=6)
    ops += forma(rect(-56, -146, 56, -128, 3), CALIZA, 4.2, sp=5)
    return Dib(ops + [T(linea((-60, 0), (60, 0)), 4.4, peso=0.03)])


@lru_cache(maxsize=None)
def sarcofago():
    """Sarcófago antropomorfo dorado (de pie)."""
    P = curva([(-40, 0), (-52, -80), (-56, -170), (-62, -230), (-58, -290), (-30, -330), (30, -330), (58, -290), (62, -230), (56, -170), (52, -80), (40, 0)], 8)
    ops = forma(P, ORO_EG, 5.4, peso=0.6, sp=9)
    ops += forma(curva([(-50, -250), (-56, -300), (-28, -328), (28, -328), (56, -300), (50, -250), (30, -236), (-30, -236)], 6), LAPIS, 4.6, sp=6)
    ops += forma(elip(0, -270, 26, 32, 0, 1.0, 22), ORO_EG, 4.4, sp=6)
    ops += [punto(-10, -276, 7), punto(10, -276, 7), T(linea((-6, -256), (6, -256)), 3, peso=0.02)]
    ops += forma(pol((-6, -238), (6, -238), (5, -214), (-5, -214)), (90, 70, 60), 3, sp=2)
    for k in range(3):
        ops.append(R(curva([(-50, -200 + 14 * k), (0, -186 + 14 * k), (50, -200 + 14 * k)], 5).tolist() + [(50, -192 + 14 * k), (0, -178 + 14 * k), (-50, -192 + 14 * k)],
                     (TURQ, LAPIS, OCRE_R)[k], peso=0.03, sp=4))
    ops += [T(linea((-20, -150), (20, -150)), 4.4, peso=0.03), T(curva([(-40, -150), (0, -120), (40, -150)], 5), 3.4, peso=0.02)]
    ops += [T(linea((0, -110), (0, -10)), 3, peso=0.02)] + [rayita(-30, -90 + 30 * k, 30, -90 + 30 * k, 2.2) for k in range(3)]
    return Dib(ops)


@lru_cache(maxsize=None)
def mascara_tut():
    """Máscara funeraria de oro de Tutankamón (nemes a rayas de lapislázuli, collar, barba)."""
    ops = forma(curva([(-130, 0), (-128, -60), (-110, -120), (-118, -200), (-100, -270), (-50, -312), (0, -320), (50, -312), (100, -270), (118, -200),
                       (110, -120), (128, -60), (130, 0)], 8), ORO_EG, 5.6, peso=0.6, sp=9)
    for k in range(7):
        y = -290 + 26 * k
        ops.append(R(curva([(-104 + 4 * k, y), (0, y - 14), (104 - 4 * k, y)], 5).tolist() + [(104 - 4 * k, y + 10), (0, y - 4), (-104 + 4 * k, y + 10)],
                     LAPIS, peso=0.03, sp=4))
    for lado in (-1, 1):
        for k in range(5):
            y = -150 + 26 * k
            ops.append(R(pol((lado * 80, y), (lado * 126, y + 4), (lado * 128, y + 14), (lado * 80, y + 10)), LAPIS, peso=0.02, sp=3))
    ops += forma(elip(0, -190, 62, 78, 0, 1.0, 30), ORO_EG, 5.0, sp=7)
    for s_ in (-1, 1):
        ops += forma(curva([(s_ * 40, -206), (s_ * 22, -218), (s_ * 6, -208), (s_ * 22, -198)], 5, cerrado=True), BLANCO_EG, 3.8, sp=3)
        ops += [punto(s_ * 22, -208, 9), T(curva([(s_ * 6, -208), (s_ * 2, -200)], 2), 3.6, peso=0.02)]
        ops += [T(curva([(s_ * 44, -226), (s_ * 22, -236), (s_ * 4, -228)], 4), 5, peso=0.04)]
    ops += [T(curva([(-4, -200), (-8, -168), (6, -164)], 4), 3.4, peso=0.02), T(linea((-18, -146), (18, -146)), 4, peso=0.02)]
    ops += forma(pol((-12, -114), (12, -114), (10, -60), (-10, -60)), LAPIS, 3.8, sp=3)
    for k in range(4):
        ops.append(R(curva([(-120, -50 + 14 * k), (0, -30 + 14 * k), (120, -50 + 14 * k)], 5).tolist() + [(120, -42 + 14 * k), (0, -22 + 14 * k),
                                                                                                        (-120, -42 + 14 * k)], (TURQ, OCRE_R, LAPIS, ORO_OS)[k],
                     peso=0.03, sp=4))
    ops += [T(curva([(-14, -316), (-8, -346), (6, -350), (10, -332)], 4), 5, peso=0.03), T(curva([(14, -316), (30, -340), (44, -338)], 4), 4, peso=0.03)]
    return Dib(ops + _destello(-110, -300, 10, 26, 6, 2.6) + _destello(120, -80, 10, 22, 6, 2.4))


@lru_cache(maxsize=None)
def tesoro():
    """Cofre abierto del tesoro de Tutankamón: oro, joyas, escarabajos y un anj."""
    ops = []
    for k, (x, y, r) in enumerate(((-70, -96, 26), (-30, -112, 28), (16, -110, 26), (58, -98, 24), (-50, -80, 22), (40, -80, 22))):
        ops += forma(elip(x, y, r, r * 0.8, 0, 1.0, 16), ORO_EG, 3.8, sp=4)
    ops += colocar(list(anj().ops), -18, -100, 0.42) + colocar(list(escarabajo().ops), 46, -128, 0.32)
    ops += forma(rect(-110, -84, 110, 0, 6), (176, 120, 70), 5.2, sp=8)
    ops += forma(rect(-110, -84, 110, -64, 4), ORO_EG, 4.4, sp=5)
    ops += forma(pol((-110, -84), (-120, -168), (110, -176), (110, -84)), (150, 100, 60), 4.6, sp=6)
    ops += [R(rect(-80, -50, -40, -20, 3), LAPIS, peso=0.02, sp=3), R(rect(40, -50, 80, -20, 3), LAPIS, peso=0.02, sp=3)]
    return Dib(ops + _destello(-90, -140, 8, 20, 6, 2.4) + _destello(70, -150, 8, 22, 6, 2.4))


@lru_cache(maxsize=None)
def disco_aton(manos=True, n=11):
    """Atón: el disco solar con uraeus y rayos que terminan en manitas (algunas con el anj)."""
    ops = []
    for k in range(n):
        a = math.radians(30 + 120 * k / (n - 1))
        x0, y0 = 70 * math.cos(a), -200 + 70 * math.sin(a)
        x1, y1 = 210 * math.cos(a), -200 + 210 * math.sin(a)
        ops += [T(linea((x0, y0), (x1, y1)), 3.6, peso=0.03)]
        if manos:
            ops += forma(elip(x1, y1, 9, 9, 0, 1.0, 10), (232, 170, 120), 3.0, sp=2)
            if k % 3 == 1:
                ops += colocar(list(anj().ops), x1 + 14, y1 + 30, 0.18)
    ops += forma(elip(0, -200, 70, 70, 0, 1.0, 36), (246, 196, 70), 5.6, peso=0.5, sp=8)
    ops += forma(elip(0, -200, 50, 50, 0, 1.0, 30), (250, 214, 110), 3.4, sp=6)
    ops += [T(curva([(0, -128), (-8, -112), (4, -100), (10, -110)], 4), 4.2, peso=0.03)]
    return Dib(ops)


# ------------------------------------------------------------------ escritura y símbolos
@lru_cache(maxsize=None)
def anj():
    ops = forma(elip(0, -180, 34, 44, 0, 1.0, 24), None, 9)
    ops += [R(elip(0, -180, 34, 44, 0, 1.0, 24), ORO_EG, peso=0.03, sp=5)]
    ops += forma(rect(-60, -140, 60, -116, 6), ORO_EG, 5.6, sp=5) + forma(rect(-13, -120, 13, 0, 5), ORO_EG, 5.6, sp=5)
    return Dib(ops)


@lru_cache(maxsize=None)
def ojo_horus():
    ops = forma(curva([(-90, -110), (-40, -146), (20, -150), (80, -116), (20, -88), (-40, -86)], 6, cerrado=True), BLANCO_EG, 5.6, sp=6)
    ops += forma(elip(-6, -116, 26, 26, 0, 1.0, 20), LAPIS, 5, sp=5) + [punto(-6, -116, 14)]
    ops += [T(curva([(-96, -150), (-30, -176), (40, -170), (96, -136)], 6), 9, peso=0.05)]
    ops += [T(linea((-20, -88), (-24, -20)), 8, peso=0.04), T(curva([(10, -90), (30, -50), (60, -40), (70, -60), (56, -70)], 6), 7, peso=0.04)]
    ops += [T(linea((80, -116), (140, -114)), 7, peso=0.03)]
    return Dib(ops)


@lru_cache(maxsize=None)
def escarabajo():
    ops = forma(elip(0, -100, 64, 80, 0, 1.0, 30), TURQ, 5.4, sp=7) + [T(linea((0, -170), (0, -30)), 4, peso=0.03)]
    ops += forma(elip(0, -190, 34, 22, 0, 1.0, 18), (60, 120, 120), 4.6, sp=5)
    for s_ in (-1, 1):
        for k, (a, b) in enumerate((((-40, -140), (-90, -170)), ((-60, -100), (-110, -100)), ((-44, -50), (-90, -20)))):
            ops += [T(linea((s_ * -a[0], a[1]), (s_ * -b[0], b[1])), 5, peso=0.03)]
    ops += forma(elip(0, -250, 34, 34, 0, 1.0, 24), (232, 130, 70), 4.8, sp=5)
    return Dib(ops)


_GLIFOS = ("ojo", "pajaro", "agua", "cana", "anj", "buho", "sol", "pan", "serpiente", "mano", "pie", "loto")


def _glifo(nombre, x, y, s=1.0):
    """Jeroglífico simple centrado en (x, y), unos 40 px * s."""
    k = s
    if nombre == "ojo":
        return [T(curva([(x - 18 * k, y), (x, y - 9 * k), (x + 18 * k, y), (x, y + 8 * k), (x - 18 * k, y)], 4), 3.4, peso=0.02), punto(x, y, 6 * k)]
    if nombre == "pajaro":
        return [T(curva([(x - 16 * k, y + 14 * k), (x - 6 * k, y), (x + 8 * k, y - 4 * k), (x + 12 * k, y - 16 * k), (x + 20 * k, y - 14 * k),
                         (x + 14 * k, y - 8 * k), (x + 12 * k, y + 8 * k), (x, y + 14 * k), (x - 16 * k, y + 14 * k)], 3), 3.4, peso=0.02),
                T(linea((x - 2 * k, y + 14 * k), (x - 4 * k, y + 22 * k)), 3, peso=0.01)]
    if nombre == "agua":
        return [T(np.array([(x - 20 * k + 5 * k * i, y + (4 * k if i % 2 else -4 * k)) for i in range(9)]), 3.2, peso=0.02)]
    if nombre == "cana":
        return [T(linea((x, y + 18 * k), (x, y - 14 * k)), 3.2, peso=0.02), T(curva([(x, y - 14 * k), (x + 10 * k, y - 20 * k), (x + 6 * k, y - 6 * k)], 3), 3, peso=0.02)]
    if nombre == "anj":
        return [T(elip(x, y - 10 * k, 7 * k, 9 * k, 0, 1.0, 12), 3, peso=0.02), T(linea((x - 12 * k, y), (x + 12 * k, y)), 3.2, peso=0.02),
                T(linea((x, y), (x, y + 18 * k)), 3.2, peso=0.02)]
    if nombre == "buho":
        return [T(curva([(x - 10 * k, y + 18 * k), (x - 12 * k, y - 4 * k), (x - 6 * k, y - 16 * k), (x + 6 * k, y - 16 * k), (x + 12 * k, y - 4 * k),
                         (x + 10 * k, y + 18 * k)], 3), 3.2, peso=0.02), punto(x - 4 * k, y - 8 * k, 4 * k), punto(x + 4 * k, y - 8 * k, 4 * k)]
    if nombre == "sol":
        return [T(circ(x, y, 12 * k, n=16), 3.2, peso=0.02), punto(x, y, 5 * k)]
    if nombre == "pan":
        return [T(arco_(x, y + 8 * k, 16 * k, 180, 360, 10), 3.2, peso=0.02), T(linea((x - 16 * k, y + 8 * k), (x + 16 * k, y + 8 * k)), 3, peso=0.02)]
    if nombre == "serpiente":
        return [T(ondas(x - 18 * k, x + 18 * k, y, 5 * k, 14 * k), 3.2, peso=0.02), punto(x + 18 * k, y - 2 * k, 5 * k)]
    if nombre == "mano":
        return [T(curva([(x - 18 * k, y + 4 * k), (x + 10 * k, y + 2 * k), (x + 18 * k, y - 4 * k), (x + 8 * k, y - 6 * k), (x - 18 * k, y - 4 * k)], 3), 3, peso=0.02)]
    if nombre == "pie":
        return [T(curva([(x - 4 * k, y - 18 * k), (x - 4 * k, y + 10 * k), (x + 18 * k, y + 12 * k), (x + 16 * k, y + 4 * k), (x + 4 * k, y + 2 * k),
                         (x + 4 * k, y - 18 * k)], 3), 3, peso=0.02)]
    return [T(curva([(x, y + 18 * k), (x, y - 4 * k), (x - 12 * k, y - 16 * k), (x, y - 10 * k), (x + 12 * k, y - 16 * k), (x, y - 4 * k)], 3), 3, peso=0.02)]


@lru_cache(maxsize=None)
def tablilla_jeroglificos(filas=4, cols=5, col=CALIZA):
    """Losa de piedra con columnas de jeroglíficos pintados."""
    w, h = cols * 50 + 40, filas * 56 + 40
    ops = forma(rect(-w / 2, -h, w / 2, 0, 8), col, 5, sp=8)
    k = 0
    for c in range(cols):
        for f in range(filas):
            x = -w / 2 + 45 + 50 * c
            y = -h + 48 + 56 * f
            ops += _glifo(_GLIFOS[(k * 7 + c) % len(_GLIFOS)], x, y, 0.9)
            k += 1
        if c:
            ops += [T(linea((-w / 2 + 20 + 50 * c, -h + 16), (-w / 2 + 20 + 50 * c, -16)), 2, peso=0.02, v=150)]
    ops += [R(rect(-w / 2 + 10, -h + 10, w / 2 - 10, -h + 20, 2), OCRE_R, peso=0.02, sp=3)]
    return Dib(ops)


@lru_cache(maxsize=None)
def papiro_escrito():
    """Rollo de papiro desplegado con columnas de jeroglíficos y una viñeta."""
    ops = forma(pol((-170, -200), (170, -206), (174, -6), (-166, 0)), (240, 224, 180), 4.8, sp=8)
    ops += forma(elip(-170, -100, 18, 104, 0, 1.0, 20), (214, 190, 140), 4.4, sp=5) + forma(elip(172, -104, 18, 104, 0, 1.0, 20), (214, 190, 140), 4.4, sp=5)
    for c in range(4):
        for f in range(4):
            ops += _glifo(_GLIFOS[(c * 5 + f * 3) % len(_GLIFOS)], -120 + 40 * c, -170 + 42 * f, 0.75)
    ops += colocar(list(E1.escriba(0, "feliz").ops), 90, -16, 0.6)
    return Dib(ops)


@lru_cache(maxsize=None)
def cartucho(nombre=("sol", "pajaro", "anj"), borrado=False):
    """Cartucho real (óvalo con cuerda dorada) con tres jeroglíficos; `borrado` = picado a cincel (Akenatón)."""
    ops = forma(rect(-46, -230, 46, -20, 30), (248, 238, 205), 5.6, sp=8)
    ops += [T(rect(-38, -222, 38, -28, 24), 3, peso=0.04)]
    ops += forma(rect(-40, -20, 40, -4, 3), ORO_EG, 4.6, sp=5)
    for k, g in enumerate(nombre):
        ops += _glifo(g, 0, -184 + 56 * k, 1.1)
    if borrado:
        for k in range(14):
            x = -30 + (k * 37) % 60
            y = -200 + (k * 53) % 170
            ops += [T(curva([(x - 10, y - 4), (x, y + 6), (x + 12, y - 2)], 3), 4.4, peso=0.02)]
        ops += forma(pol((-46, -150), (40, -170), (46, -120), (-40, -100)), (200, 186, 160), 3, sp=5)
        ops += [T(linea((-50, -230), (50, -10)), 9, peso=0.04), T(linea((50, -230), (-50, -10)), 9, peso=0.04)]
    return Dib(ops)


@lru_cache(maxsize=None)
def paleta_narmer():
    """La paleta de Narmer (pizarra en forma de escudo): cabezas de Bat, el serej con el nombre y el rey golpeando a un enemigo."""
    P = curva([(-90, 0), (-104, -80), (-110, -180), (-100, -250), (-60, -290), (0, -300), (60, -290), (100, -250), (110, -180), (104, -80), (90, 0)], 8)
    ops = forma(P, (130, 140, 128), 5.6, peso=0.6, sp=9)
    for s_ in (-1, 1):
        ops += forma(elip(s_ * 64, -262, 20, 20, 0, 1.0, 16), (170, 176, 160), 4, sp=4)
        ops += [T(curva([(s_ * 50, -276), (s_ * 40, -300), (s_ * 54, -310)], 3), 4, peso=0.02), T(curva([(s_ * 78, -276), (s_ * 90, -298), (s_ * 78, -310)], 3), 4, peso=0.02)]
    ops += forma(rect(-28, -284, 28, -232, 3), (170, 176, 160), 4, sp=4) + _glifo("pez" if False else "serpiente", 0, -262, 0.7)
    ops += [T(linea((-100, -224), (100, -224)), 3, peso=0.02)]
    rey = E1.narmer(0, "hedjet", "enojo")
    ops += colocar(list(rey.ops), -16, -40, 0.62)
    ops += colocar(list(persona((180, 170, 150), PIEL_EG, "calvo", "miedo", (60, 80), 0, traje="corta").ops), 60, -40, 0.42, rot=0.5)
    return Dib(ops)


@lru_cache(maxsize=None)
def corona_doble():
    """La doble corona (pschent) como objeto, sobre un cojín."""
    ops = forma(rect(-90, -30, 90, 0, 12), (200, 70, 60), 4.6, sp=6)
    ops += forma(curva([(-36, -110), (-34, -170), (-20, -230), (0, -246), (20, -230), (34, -170), (36, -110)], 6), LINO, 5, sp=7)
    ops += forma(pol((-70, -30), (-74, -120), (-36, -120), (-30, -100), (30, -100), (36, -120), (50, -120), (50, -200), (72, -204), (72, -30)), OCRE_R, 5.2, sp=8)
    ops += [T(curva([(-36, -110), (-62, -150), (-84, -170), (-74, -190)], 5), 5, peso=0.04)]
    return Dib(ops + _destello(0, -260, 12, 30, 8, 2.6))


@lru_cache(maxsize=None)
def tratado():
    """El tratado de paz de Kadesh: tablilla de plata con escritura cuneiforme y, encima, dos manos que se estrechan."""
    ops = forma(rect(-110, -220, 110, 0, 10), (210, 214, 222), 5.2, sp=8)
    for f in range(7):
        for c in range(9):
            x = -88 + 22 * c
            y = -190 + 26 * f
            ops += [T(pol((x, y), (x + 8, y + 4), (x, y + 8)), 2.6, peso=0.02), T(linea((x + 4, y + 4), (x + 14, y + 4)), 2.2, peso=0.01)]
    ops += colocar(list(E1.ramses(0, "feliz").ops), -170, 0, 0.62)
    ops += colocar(list(E1.rey_hitita(0, "feliz").ops), 170, 0, 0.62, flip=True)
    return Dib(ops)


@lru_cache(maxsize=None)
def piedra_rosetta():
    """La Piedra de Rosetta: granodiorita oscura rota arriba, con tres textos (jeroglífico, demótico y griego)."""
    P = [(-120, 0), (-124, -200), (-110, -250), (-60, -262), (-20, -300), (60, -306), (110, -280), (124, -220), (120, 0)]
    ops = forma(pol(*P), (84, 86, 96), 5.6, peso=0.6, sp=9)
    for k in range(4):
        for c in range(6):
            ops += _glifo(_GLIFOS[(k * 5 + c) % len(_GLIFOS)], -80 + 32 * c, -250 + 20 * k + (6 if c % 2 else 0), 0.5)
    ops += [T(linea((-110, -176), (112, -178)), 2.4, peso=0.02, v=200)]
    for k in range(5):
        ops += [T(ondas(-100, 100, -158 + 18 * k, 3, 9), 2.4, peso=0.02, v=220)]
    ops += [T(linea((-112, -64), (114, -66)), 2.4, peso=0.02, v=200)]
    for k in range(5):
        y = -50 + 10 * k
        ops += [T(np.array([(-100 + 10 * i, y + (2 if i % 3 == 0 else 0)) for i in range(21)]), 2.2, peso=0.01, v=230)]
    ops += [R(pol((-110, -192), (-104, -200), (-80, -196)), (130, 132, 140), peso=0.02, sp=3)]
    return Dib(ops)


# ------------------------------------------------------------------ Alejandría
@lru_cache(maxsize=None)
def faro():
    """El Faro de Alejandría: tres cuerpos (cuadrado, octogonal, cilíndrico), estatua y haz de luz."""
    ops = forma(pol((180, -330), (420, -380), (420, -280)), (250, 230, 150), 3.0, sp=8)
    ops += forma(rect(-90, -20, 90, 0, 3), ARENISCA_OS, 4.0, sp=5)
    ops += forma(trap(-60, 60, -230, -76, 76, -20), CALIZA, 5, sp=8)
    for y in (-190, -150, -110, -70):
        ops += [rayita(-60, y, 60, y, 2.2)]
    ops += [punto(-30, -120, 9), punto(30, -120, 9), punto(0, -170, 9)]
    ops += forma(trap(-38, 38, -330, -50, 50, -230), CALIZA, 4.8, sp=7)
    ops += forma(rect(-28, -380, 28, -330, 6), CALIZA, 4.6, sp=6)
    ops += forma(elip(0, -356, 18, 14, 0, 1.0, 14), (250, 200, 80), 4, sp=5)
    ops += [T(linea((0, -380), (0, -420)), 4.4, peso=0.03)] + forma(elip(0, -428, 10, 10, 0, 1.0, 12), ORO_EG, 3.6, sp=3)
    ops += [T(linea((-6, -416), (-26, -440)), 3.6, peso=0.02)]
    return Dib(ops)


@lru_cache(maxsize=None)
def biblioteca():
    """La Biblioteca de Alejandría: pórtico griego con columnas y frontón, y rollos asomando."""
    ops = forma(rect(-210, -26, 210, 0, 3), CALIZA, 4.6, sp=6) + forma(rect(-190, -40, 190, -26, 3), CALIZA, 4.2, sp=5)
    ops += forma(rect(-180, -220, 180, -40, 4), (226, 214, 190), 4.4, sp=7)
    for k in range(6):
        x = -150 + 60 * k
        ops += forma(rect(x - 14, -214, x + 14, -40, 4), BLANCO_EG, 4.2, sp=5) + [rayita(x - 4, -200, x - 4, -54, 2), rayita(x + 5, -200, x + 5, -54, 2)]
        if k < 5:
            for j in range(3):
                ops += forma(elip(x + 30, -80 - 40 * j, 9, 9, 0, 1.0, 10), (232, 214, 170), 3, sp=2)
    ops += forma(rect(-196, -240, 196, -216, 3), CALIZA, 4.4, sp=5)
    ops += forma(pol((-206, -240), (0, -320), (206, -240)), CALIZA, 5, sp=7)
    ops += forma(elip(0, -268, 24, 18, 0, 1.0, 16), ORO_EG, 3.6, sp=4)
    return Dib(ops)


@lru_cache(maxsize=None)
def estante_rollos():
    """Estantería con rollos de papiro (los libros de la Biblioteca)."""
    ops = forma(rect(-150, -280, 150, 0, 4), (150, 100, 66), 5, sp=8)
    for f in range(4):
        y = -270 + 68 * f
        ops += [T(linea((-146, y + 62), (146, y + 62)), 4, peso=0.03)]
        for c in range(9):
            x = -126 + 31 * c
            ops += forma(elip(x, y + 44, 13, 13, 0, 1.0, 12), (240, 226, 186), 3, sp=3) + [punto(x, y + 44, 5)]
            if (c + f) % 4 == 0:
                ops += [T(linea((x, y + 30), (x + 8, y + 18)), 2.4, peso=0.01), R(pol((x + 6, y + 18), (x + 16, y + 16), (x + 14, y + 24)), (200, 70, 60), peso=0.01, sp=2)]
    return Dib(ops)


@lru_cache(maxsize=None)
def moneda_ptolemaica():
    ops = forma(elip(0, -90, 90, 90, 0, 1.0, 36), (210, 214, 222), 5.4, sp=7)
    ops += [T(elip(0, -90, 76, 76, 0, 1.0, 36), 2.6, peso=0.02)]
    ops += forma(curva([(-40, -60), (-30, -110), (0, -136), (20, -126), (10, -110), (30, -90), (44, -50), (10, -40)], 5), (150, 154, 164), 4.4, sp=5)
    ops += [T(linea((-30, -40), (44, -40)), 3.6, peso=0.02), T(curva([(-6, -132), (4, -144), (14, -138)], 3), 3, peso=0.02)]
    return Dib(ops)


# ------------------------------------------------------------------ El Cairo
@lru_cache(maxsize=None)
def minarete(h=300, col=CALIZA):
    ops = forma(rect(-26, -h * 0.55, 26, 0, 3), col, 4.6, sp=6)
    ops += forma(rect(-36, -h * 0.58, 36, -h * 0.52, 3), col, 4, sp=4)
    ops += forma(trap(-18, 18, -h * 0.85, -22, 22, -h * 0.58), col, 4.4, sp=5)
    ops += forma(rect(-28, -h * 0.88, 28, -h * 0.83, 3), col, 4, sp=4)
    ops += forma(curva([(-16, -h * 0.88), (-18, -h * 0.94), (0, -h), (18, -h * 0.94), (16, -h * 0.88)], 5), (150, 180, 150), 4.2, sp=4)
    ops += [T(linea((0, -h), (0, -h - 26)), 3.6, peso=0.02), T(arco_(4, -h - 34, 8, 120, 400, 8), 3.4, peso=0.02)]
    ops += [T(arco_(0, -h * 0.3, 10, 180, 360, 8), 3, peso=0.02), T(linea((-10, -h * 0.3), (-10, -h * 0.22)), 3, peso=0.02), T(linea((10, -h * 0.3), (10, -h * 0.22)), 3, peso=0.02)]
    return Dib(ops)


@lru_cache(maxsize=None)
def mezquita():
    """Mezquita cairota: muro con almenas, gran cúpula y dos minaretes."""
    ops = colocar(list(minarete(300).ops), -170, 0, 1.0) + colocar(list(minarete(260).ops), 170, 0, 1.0)
    ops += forma(rect(-140, -150, 140, 0, 3), (232, 218, 190), 5, sp=8)
    for k in range(9):
        x = -130 + 32.5 * k
        ops += forma(pol((x - 8, -150), (x, -166), (x + 8, -150)), (232, 218, 190), 3.2, sp=3)
    ops += forma(curva([(-80, -150), (-82, -200), (-50, -250), (0, -268), (50, -250), (82, -200), (80, -150)], 6), (130, 176, 150), 5, sp=7)
    ops += [T(linea((0, -268), (0, -296)), 3.6, peso=0.02), T(arco_(4, -304, 8, 120, 400, 8), 3.4, peso=0.02)]
    for x in (-90, -30, 30, 90):
        ops += forma(curva([(x - 16, -40), (x - 16, -90), (x, -110), (x + 16, -90), (x + 16, -40)], 5), (110, 90, 70), 3.8, sp=4)
    return Dib(ops)


@lru_cache(maxsize=None)
def ciudadela():
    """La Ciudadela de Saladino: murallas y torres sobre la colina (y la mezquita otomana posterior no: aún no existía)."""
    ops = forma(curva([(-260, 0), (-200, -50), (-100, -70), (100, -70), (200, -50), (260, 0)], 6), ARENISCA, 4.6, sp=7)
    ops += forma(rect(-200, -190, 200, -60, 3), (214, 196, 160), 5, sp=8)
    for x in (-210, -70, 70, 210):
        ops += forma(curva([(x - 34, -50), (x - 34, -230), (x + 34, -230), (x + 34, -50)], 4), (200, 180, 144), 5, sp=7)
        for k in range(3):
            ops += forma(rect(x - 34 + 24 * k, -250, x - 22 + 24 * k, -228, 2), (200, 180, 144), 3.6, sp=3)
        ops += forma(rect(x - 8, -190, x + 8, -160, 3), (80, 60, 50), 3, sp=3)
    for k in range(10):
        ops += forma(rect(-196 + 40 * k, -206, -180 + 40 * k, -188, 2), (214, 196, 160), 3.4, sp=3)
    ops += forma(curva([(-30, -60), (-30, -120), (0, -144), (30, -120), (30, -60)], 5), (80, 60, 50), 4, sp=4)
    ops += [T(linea((70, -230), (70, -300)), 4, peso=0.04)] + forma(pol((70, -300), (130, -290), (70, -270)), (232, 196, 90), 3.6, sp=3)
    return Dib(ops)


@lru_cache(maxsize=None)
def el_cairo():
    """Silueta de El Cairo medieval: casas, cúpulas y minaretes."""
    ops = []
    for k, (x, w, h) in enumerate(((-240, 70, 110), (-160, 80, 150), (-70, 90, 120), (20, 70, 170), (100, 90, 130), (190, 80, 100))):
        ops += forma(rect(x - w / 2, -h, x + w / 2, 0, 3), ((226, 206, 170), (214, 190, 150), (236, 220, 190))[k % 3], 4.6, sp=6)
        for j in range(2):
            ops += [T(arco_(x - w / 4 + j * w / 2, -h + 34, 8, 180, 360, 6), 2.8, peso=0.02), T(linea((x - w / 4 + j * w / 2 - 8, -h + 34), (x - w / 4 + j * w / 2 - 8, -h + 50)), 2.6, peso=0.01),
                    T(linea((x - w / 4 + j * w / 2 + 8, -h + 34), (x - w / 4 + j * w / 2 + 8, -h + 50)), 2.6, peso=0.01)]
    ops += colocar(list(minarete(320).ops), -110, -150, 0.72) + colocar(list(minarete(280).ops), 140, -130, 0.72)
    ops += forma(curva([(-30, -170), (-28, -210), (20, -232), (68, -210), (70, -170)], 5), (130, 176, 150), 4.6, sp=5)
    return Dib(ops)


# ------------------------------------------------------------------ siglos XIX y XX
@lru_cache(maxsize=None)
def presa_asuan():
    """La Gran Presa de Asuán: el muro de tierra y roca, el lago detrás, las turbinas y las torres eléctricas."""
    ops = forma(pol((-330, -110), (-330, -160), (-120, -170), (120, -170), (330, -160), (330, -110)), (120, 170, 210), 4.4, sp=7)
    ops += [T(ondas(-320, 320, -150, 4, 30), 2.6, peso=0.02, v=200)]
    ops += forma(pol((-340, 0), (-300, -120), (300, -120), (340, 0)), (196, 176, 140), 5.2, sp=8)
    ops += forma(rect(-310, -132, 310, -116, 3), (150, 150, 156), 4.2, sp=5)
    for k in range(6):
        x = -150 + 60 * k
        ops += forma(rect(x - 16, -90, x + 16, -30, 3), (80, 84, 96), 4, sp=4)
        ops += [T(ondas(x - 14, x + 14, -18, 3, 10), 2.4, peso=0.02)]
    for x in (-260, 270):
        ops += [T(linea((x - 30, -120), (x, -280)), 4, peso=0.04), T(linea((x + 30, -120), (x, -280)), 4, peso=0.04), T(linea((x - 40, -240), (x + 40, -240)), 4, peso=0.02),
                T(linea((x - 22, -170), (x + 22, -170)), 3, peso=0.02), T(linea((x - 26, -170), (x + 20, -240)), 2.4, peso=0.01)]
    ops += [T(curva([(-220, -240), (0, -210), (230, -240)], 6), 2.4, peso=0.01)]
    return Dib(ops)


@lru_cache(maxsize=None)
def torre_cairo():
    """La Torre de El Cairo (1961): fuste en celosía de flor de loto."""
    ops = forma(trap(-22, 22, -360, -34, 34, 0), (200, 190, 176), 5, sp=7)
    for k in range(12):
        y = -30 - 28 * k
        ops += [T(linea((-30 + k * 0.7, y), (30 - k * 0.7, y - 20)), 2.2, peso=0.01), T(linea((30 - k * 0.7, y), (-30 + k * 0.7, y - 20)), 2.2, peso=0.01)]
    ops += forma(curva([(-60, -380), (-40, -410), (0, -420), (40, -410), (60, -380), (0, -360)], 5), (110, 160, 140), 4.6, sp=6)
    return Dib(ops + [T(linea((0, -420), (0, -470)), 3.6, peso=0.02)])


@lru_cache(maxsize=None)
def rascacielos_eg(n=5):
    ops = []
    for k in range(n):
        x = -160 + 80 * k
        h = 180 + 70 * ((k * 3) % 4)
        ops += forma(rect(x - 30, -h, x + 30, 0, 3), ((150, 180, 210), (200, 196, 186), (170, 190, 180))[k % 3], 4.6, sp=6)
        for f in range(int(h / 34)):
            ops += [T(linea((x - 20, -20 - 34 * f), (x + 20, -20 - 34 * f)), 2, peso=0.01, v=160)]
    return Dib(ops)


@lru_cache(maxsize=None)
def gavilla():
    ops = []
    for k in range(9):
        a = (k - 4) * 0.09
        x1, y1 = 120 * math.sin(a), -200 * math.cos(a)
        ops += [T(linea((0, -10), (x1, y1)), 3.4, peso=0.03)]
        ops += forma(elip(x1, y1 - 20, 10, 30, a, 1.0, 14), (236, 190, 80), 3.4, sp=3)
    ops += forma(rect(-26, -90, 26, -70, 4), (176, 120, 70), 4, sp=4)
    return Dib(ops)


@lru_cache(maxsize=None)
def saco_grano():
    ops = forma(curva([(-60, 0), (-76, -60), (-60, -130), (-30, -150), (30, -150), (60, -130), (76, -60), (60, 0)], 6), (214, 186, 130), 5, sp=7)
    ops += [T(curva([(-30, -150), (0, -138), (30, -150)], 4), 4, peso=0.03), T(linea((0, -150), (0, -176)), 4, peso=0.02)]
    for k in range(5):
        ops += forma(elip(-14 + 7 * k, -180 + (k % 2) * 6, 7, 5, 0, 1.0, 10), (236, 196, 90), 2.6, sp=2)
    return Dib(ops)


@lru_cache(maxsize=None)
def anfora():
    P = curva([(-14, -230), (-20, -210), (-56, -160), (-60, -90), (-30, -20), (0, 0), (30, -20), (60, -90), (56, -160), (20, -210), (14, -230)], 8)
    ops = forma(P, (200, 120, 80), 5, sp=7)
    ops += [T(curva([(-18, -210), (-46, -214), (-50, -170)], 4), 4.6, peso=0.03), T(curva([(18, -210), (46, -214), (50, -170)], 4), 4.6, peso=0.03)]
    return Dib(ops + [T(linea((-50, -130), (50, -130)), 2.4, peso=0.02)])


@lru_cache(maxsize=None)
def sequia():
    """Tierra agrietada, una planta seca y un sol que quema."""
    ops = forma(pol((-200, -40), (200, -40), (220, 0), (-220, 0)), (206, 170, 120), 4.6, sp=7)
    for k in range(9):
        x = -180 + 45 * k
        ops += [T(np.array([(x, -38), (x + 10, -26), (x + 4, -14), (x + 14, -2)]), 3, peso=0.02)]
    ops += [T(curva([(-60, -40), (-58, -90), (-70, -120)], 4), 4, peso=0.02), T(curva([(-58, -80), (-40, -96)], 2), 3, peso=0.02), T(curva([(-62, -100), (-80, -104)], 2), 3, peso=0.02)]
    ops += forma(elip(110, -200, 46, 46, 0, 1.0, 24), (240, 150, 60), 5, sp=6) + _destello(110, -200, 56, 86, 10, 3.6)
    return Dib(ops)


@lru_cache(maxsize=None)
def crecida():
    """La crecida del Nilo: olas que suben y flechas hacia arriba."""
    ops = []
    for k in range(3):
        y = -30 - 34 * k
        ops += forma(np.vstack([ondas(-180, 180, y, 10, 70, k * 1.3), [(180, 0), (-180, 0)]]), (120, 170, 210) if k == 0 else (150, 196, 224), 4, sp=6)
    for x in (-120, 0, 120):
        ops += [T(linea((x, -150), (x, -230)), 5, peso=0.03), T(linea((x - 18, -210), (x, -232)), 5, peso=0.02), T(linea((x + 18, -210), (x, -232)), 5, peso=0.02)]
    return Dib(ops)


@lru_cache(maxsize=None)
def bandera(cual="egipto"):
    """Bandera grande en su mástil: egipto | uk | francia | otomana | republica_arabe."""
    ops = [T(linea((-120, 0), (-120, -340)), 6, peso=0.12)]
    x0, x1, y0, y1 = -116, 150, -330, -160
    if cual in ("egipto", "republica_arabe"):
        for k, c in enumerate(((200, 50, 46), BLANCO_EG, NEGRO_EG)):
            ops += forma(rect(x0, y0 + 57 * k, x1, y0 + 57 * (k + 1), 2), c, 4.4, sp=6)
        ops += colocar(list(aguila_saladino().ops), (x0 + x1) / 2, y0 + 108, 0.24)
    elif cual == "francia":
        for k, c in enumerate(((60, 82, 150), BLANCO_EG, (200, 50, 46))):
            ops += forma(rect(x0 + 89 * k, y0, x0 + 89 * (k + 1), y1, 2), c, 4.4, sp=6)
    elif cual == "uk":
        ops += forma(rect(x0, y0, x1, y1, 2), (40, 60, 120), 4.4, sp=6)
        for a, b in (((x0, y0), (x1, y1)), ((x0, y1), (x1, y0))):
            ops += [T(linea(a, b), 18, peso=0.02, v=255)]
        ops += [R(rect((x0 + x1) / 2 - 16, y0, (x0 + x1) / 2 + 16, y1, 1), (200, 50, 46), peso=0.02, sp=3),
                R(rect(x0, (y0 + y1) / 2 - 14, x1, (y0 + y1) / 2 + 14, 1), (200, 50, 46), peso=0.02, sp=3)]
    elif cual == "otomana":
        ops += forma(rect(x0, y0, x1, y1, 2), (190, 40, 50), 4.4, sp=6)
        ops += [T(arco_(0, (y0 + y1) / 2, 46, 40, 320, 16), 9, peso=0.03), R(elip(54, (y0 + y1) / 2, 12, 12, n=10), BLANCO_EG, peso=0.02, sp=3)]
    return Dib(ops)


@lru_cache(maxsize=None)
def aguila_saladino():
    """El águila de Saladino (escudo de Egipto)."""
    ops = forma(curva([(-150, -200), (-110, -150), (-60, -140), (-40, -100), (-46, -40), (0, 0), (46, -40), (40, -100), (60, -140), (110, -150), (150, -200),
                       (100, -200), (60, -180), (30, -190), (20, -230), (0, -250), (-20, -230), (-30, -190), (-60, -180), (-100, -200)], 6), ORO_EG, 5, sp=7)
    ops += forma(rect(-30, -130, 30, -60, 6), BLANCO_EG, 4, sp=4) + [R(rect(-30, -130, -10, -60, 2), (200, 50, 46), peso=0.02, sp=3),
                                                                      R(rect(10, -130, 30, -60, 2), NEGRO_EG, peso=0.02, sp=3)]
    ops += [punto(10, -232, 7), T(linea((16, -226), (30, -222)), 3, peso=0.02)]
    return Dib(ops)


# ------------------------------------------------------------------ dioses (cabeza animal: se quita la cabeza redonda de la persona)
def _sin_cabeza(d):
    """Quita de una persona las piezas de la cara/cabeza redonda (para ponerle cabeza de animal)."""
    ops = []
    for op in d.ops:
        P = op[1]
        cx, cy = P[:, 0].mean(), P[:, 1].mean()
        if abs(cx) < 30 and -262 < cy < -170 and np.ptp(P[:, 1]) < 100:
            continue
        ops.append(op)
    return ops


def _cabeza_animal(tipo):
    cy = -215
    if tipo == "chacal":           # Anubis
        ops = forma(curva([(-34, cy + 30), (-40, cy - 10), (-20, cy - 40), (10, cy - 40), (50, cy - 20), (90, cy - 4), (84, cy + 10), (40, cy + 14), (20, cy + 34)], 5),
                    NEGRO_EG, 4.6, sp=7)
        ops += forma(pol((-24, cy - 36), (-30, cy - 92), (-4, cy - 44)), NEGRO_EG, 4.2, sp=4) + forma(pol((2, cy - 40), (8, cy - 96), (22, cy - 38)), NEGRO_EG, 4.2, sp=4)
        ops += [R(elip(18, cy - 16, 8, 5, n=10), ORO_EG, peso=0.02, sp=3)]
        return ops
    if tipo == "halcon":           # Ra / Horus
        ops = forma(curva([(-36, cy + 30), (-42, cy - 10), (-20, cy - 44), (20, cy - 44), (42, cy - 20), (60, cy - 6), (50, cy + 14), (34, cy + 4), (30, cy + 34)], 5),
                    (150, 110, 70), 4.6, sp=7)
        ops += forma(pol((42, cy - 20), (66, cy - 2), (46, cy + 6)), (240, 196, 70), 3.6, sp=3)
        ops += [punto(14, cy - 18, 9), T(curva([(10, cy - 8), (6, cy + 14)], 2), 3.6, peso=0.02)]
        return ops
    if tipo == "gato":             # Bastet
        ops = forma(elip(0, cy, 40, 36, 0, 1.0, 26), (60, 56, 60), 4.6, sp=7)
        ops += forma(pol((-36, cy - 14), (-34, cy - 66), (-10, cy - 34)), (60, 56, 60), 4.2, sp=4) + forma(pol((36, cy - 14), (34, cy - 66), (10, cy - 34)), (60, 56, 60), 4.2, sp=4)
        ops += [R(elip(-14, cy - 4, 8, 6, n=10), (220, 200, 90), peso=0.02, sp=3), R(elip(14, cy - 4, 8, 6, n=10), (220, 200, 90), peso=0.02, sp=3)]
        return ops + [T(linea((-34, cy + 12), (-60, cy + 6)), 2.4, peso=0.01), T(linea((34, cy + 12), (60, cy + 6)), 2.4, peso=0.01)]
    return []


@lru_cache(maxsize=None)
def dios(quien="amon", pose=0):
    """Dioses: amon (plumas altas, piel azul), ra (halcón con disco solar), anubis (chacal), osiris (piel verde, corona atef), bastet (gata)."""
    if quien == "amon":
        p = persona(LINO, (90, 120, 190), "calvo", "serio", (20, 30), pose, traje="corta", faja=ORO_EG, acc_d="uas")
        ops = list(p.ops) + forma(rect(-30, -270, 30, -244, 4), (200, 70, 60), 4.2, sp=4)
        ops += forma(pol((-24, -270), (-20, -400), (-2, -400), (-4, -270)), ORO_EG, 4.2, sp=5) + forma(pol((4, -270), (2, -400), (20, -400), (24, -270)), ORO_EG, 4.2, sp=5)
        return Dib(ops + E1._usekh() + E1._barba_real())
    if quien == "osiris":
        p = persona(LINO, (110, 170, 120), "calvo", "serio", (40, 40), pose, traje="tunica", acc_d="cayado", acc_i="flagelo")
        ops = list(p.ops) + forma(curva([(-30, -246), (-26, -300), (-16, -340), (0, -352), (16, -340), (26, -300), (30, -246)], 5), LINO, 4.6, sp=6)
        ops += forma(pol((-30, -250), (-50, -330), (-34, -330), (-26, -260)), (240, 230, 210), 3.6, sp=3) + forma(pol((30, -250), (50, -330), (34, -330), (26, -260)), (240, 230, 210), 3.6, sp=3)
        return Dib(ops + E1._usekh() + E1._barba_real())
    tipo = {"ra": "halcon", "horus": "halcon", "anubis": "chacal", "bastet": "gato"}[quien]
    p = persona(LINO, PIEL_EG, "calvo", "serio", (20, 30), pose, traje="corta" if quien != "bastet" else "vestido", faja=ORO_EG,
                acc_d="uas" if quien != "bastet" else "anj")
    ops = _sin_cabeza(p) + forma(curva([(-46, -196), (-56, -150), (56, -150), (46, -196)], 4), (60, 60, 70) if quien == "anubis" else (90, 110, 170), 4, sp=5)
    ops += _cabeza_animal(tipo)
    if quien == "ra":
        ops += forma(elip(0, -296, 34, 34, 0, 1.0, 24), (232, 90, 60), 4.6, sp=5) + [T(curva([(0, -262), (-6, -252), (4, -246)], 3), 3.6, peso=0.02)]
    ops += E1._usekh()
    return Dib(ops)


# ------------------------------------------------------------------ añadidos (ciudad antigua, trineo, busto de Nefertiti, trono, bandera de 1922, león)
@lru_cache(maxsize=None)
def ciudad_antigua():
    """Ciudad del Egipto antiguo (Menfis, Ajetatón): muralla blanca, casas de adobe con azotea, un pilono y palmeras."""
    ops = []
    for x in (-230, 230):
        ops += colocar(list(E3_palmera(220).ops), x, 0, 0.8)
    ops += forma(rect(-210, -70, 210, 0, 4), (244, 240, 228), 5, sp=7)
    for k in range(14):
        ops += forma(rect(-206 + 30 * k, -84, -192 + 30 * k, -68, 2), (244, 240, 228), 3, sp=2)
    for k, (x, w, h) in enumerate(((-150, 70, 120), (-70, 60, 150), (60, 70, 130), (140, 60, 110))):
        ops += forma(rect(x - w / 2, -h, x + w / 2, -60, 3), ((214, 176, 130), (196, 156, 112), (222, 190, 146))[k % 3], 4.4, sp=6)
        ops += forma(rect(x - 10, -h + 20, x + 10, -h + 44, 2), (90, 70, 56), 3, sp=2)
    ops += forma(trap(-30, 30, -190, -44, 44, -60), ARENISCA, 4.6, sp=6) + forma(rect(-14, -110, 14, -60, 2), (100, 76, 60), 3.4, sp=3)
    ops += [T(linea((-20, -186), (-20, -230)), 3.4, peso=0.03)] + forma(pol((-20, -230), (8, -222), (-20, -212)), LAPIS, 3, sp=2)
    return Dib(ops)


def E3_palmera(h):
    import obj_eg3
    return obj_eg3.palmera(h)


@lru_cache(maxsize=None)
def trineo():
    """Bloque de piedra sobre un trineo de madera, con la cuerda tensa hacia delante (a la derecha)."""
    ops = forma(rect(-90, -130, 90, -34, 4), CALIZA, 5, sp=8)
    ops += [T(linea((-80, -100), (80, -100)), 2.4, peso=0.02), T(linea((-30, -130), (-30, -100)), 2.4, peso=0.02), T(linea((40, -100), (40, -34)), 2.4, peso=0.02)]
    ops += forma(pol((-120, -34), (110, -34), (130, -20), (110, -10), (-120, -10)), (176, 124, 78), 4.6, sp=6)
    ops += [T(curva([(110, -24), (200, -40), (300, -54)], 4), 5, peso=0.03)]
    for x in (-80, -30, 20, 70):
        ops += forma(elip(x, -4, 12, 6, 0, 1.0, 12), (150, 110, 70), 3, sp=2)
    return Dib(ops)


@lru_cache(maxsize=None)
def busto_nefertiti():
    """El busto de Nefertiti (Neues Museum): cuello largo, corona azul de lados rectos con cinta de oro, collar ancho."""
    ops = forma(curva([(-110, 0), (-100, -50), (-60, -80), (60, -80), (100, -50), (110, 0)], 6), (222, 160, 110), 5, sp=7)
    for k, col in enumerate((ORO_EG, TURQ, OCRE_R, LAPIS)):
        ops.append(R(curva([(-96, -40 + 10 * k), (0, -68 + 10 * k), (96, -40 + 10 * k)], 5).tolist() + [(96, -30 + 10 * k), (0, -58 + 10 * k), (-96, -30 + 10 * k)],
                     col, peso=0.03, sp=4))
    ops += forma(pol((-26, -80), (-24, -150), (24, -150), (26, -80)), (222, 160, 110), 4.6, sp=5)
    ops += forma(elip(0, -196, 42, 56, 0, 1.0, 26), (226, 166, 116), 5, sp=6)
    ops += [T(curva([(-26, -206), (-14, -212), (-4, -206)], 3), 4, peso=0.02), T(curva([(4, -206), (14, -212), (26, -206)], 3), 4, peso=0.02)]
    ops += [punto(-14, -204, 7), T(linea((0, -200), (-2, -178)), 3, peso=0.02), T(curva([(-12, -162), (0, -158), (12, -162)], 3), 3.6, peso=0.02)]
    ops += [R(elip(-12, -160, 10, 4, n=10), (200, 80, 80), peso=0.02, sp=2)]
    ops += forma(pol((-40, -222), (-62, -330), (58, -340), (40, -222)), LAPIS, 5, sp=7)
    ops += forma(pol((-46, -262), (50, -268), (52, -254), (-44, -248)), ORO_EG, 3.8, sp=4)
    ops += [R(circ(-20 + 20 * k, -258, 4, n=8), (200, 70, 60) if k == 1 else TURQ, peso=0.02, sp=3) for k in range(3)]
    return Dib(ops)


@lru_cache(maxsize=None)
def trono_eg():
    """Trono dorado egipcio con patas de león y respaldo alto."""
    ops = forma(rect(-80, -260, 70, -120, 6), ORO_EG, 5, sp=7)
    ops += forma(rect(-90, -130, 90, -100, 4), ORO_EG, 4.6, sp=6)
    for x in (-70, 70):
        ops += forma(curva([(x - 14, -100), (x - 14, -30), (x - 20, -10), (x + 14, -6), (x + 10, -30), (x + 12, -100)], 4), ORO_OS, 4.4, sp=5)
    ops += forma(elip(-4, -190, 34, 34, 0, 1.0, 20), LAPIS, 3.6, sp=4) + colocar(list(anj().ops), -4, -170, 0.2)
    ops += forma(rect(-60, -100, 60, -80, 3), (200, 70, 60), 3.6, sp=4)
    return Dib(ops)


@lru_cache(maxsize=None)
def bandera_reino():
    """Bandera del Reino de Egipto (1922): verde con media luna y tres estrellas blancas."""
    ops = [T(linea((-120, 0), (-120, -340)), 6, peso=0.12)]
    ops += forma(rect(-116, -330, 150, -160, 2), (60, 140, 80), 4.4, sp=6)
    ops += [T(arco_(0, -245, 48, 50, 310, 16), 10, peso=0.03)]
    for k in range(3):
        a = math.radians(-40 + 40 * k)
        ops += [R(circ(20 + 40 * math.cos(a), -245 + 40 * math.sin(a), 9, n=10), BLANCO_EG, peso=0.02, sp=3)]
    return Dib(ops)


@lru_cache(maxsize=None)
def leon(pose=0):
    """León de perfil (para «cuerpo de león»)."""
    col = (220, 170, 90)
    ops = forma(curva([(-150, -60), (-140, -120), (-60, -140), (60, -136), (110, -120), (120, -60), (100, -40), (-130, -40)], 6), col, 5.2, sp=8)
    for x, dx in ((-120, -8), (-90, 8), (70, -8), (100, 8)):
        ops += forma(rect(x - 14 + dx * (pose % 2), -60, x + 14 + dx * (pose % 2), 0, 6), col, 4.4, sp=5)
    ops += forma(elip(140, -150, 66, 66, 0, 1.0, 28), (190, 120, 60), 5, sp=7)
    ops += forma(elip(152, -146, 40, 38, 0, 1.0, 22), col, 4.6, sp=6)
    ops += [punto(162, -156, 8), T(linea((178, -140), (190, -138)), 3.4, peso=0.02), T(curva([(166, -126), (180, -122), (192, -128)], 3), 3.4, peso=0.02)]
    ops += [T(curva([(-150, -90), (-190, -110), (-196, -150)], 4), 5, peso=0.03)] + forma(elip(-196, -156, 12, 14, 0, 1.0, 10), (190, 120, 60), 3.4, sp=3)
    return Dib(ops)


@lru_cache(maxsize=None)
def corazon():
    P = curva([(0, -10), (-70, -80), (-80, -140), (-44, -172), (0, -140), (44, -172), (80, -140), (70, -80)], 6, cerrado=True)
    return Dib(forma(P, (220, 80, 90), 5, sp=6))


@lru_cache(maxsize=None)
def tachar():
    """Gran X roja de tachado."""
    return Dib([T(linea((-110, -230), (110, 0)), 14, peso=0.04), T(linea((110, -230), (-110, 0)), 14, peso=0.04),
                R(pol((-120, -226), (-100, -234), (120, -4), (100, 4)), (210, 50, 46), peso=0.02, sp=4),
                R(pol((120, -226), (100, -234), (-120, -4), (-100, 4)), (210, 50, 46), peso=0.02, sp=4)])


@lru_cache(maxsize=None)
def regla(alto=300, marcas=6):
    """Regla vertical de medir (para los 146 m de la Gran Pirámide)."""
    ops = forma(rect(-16, -alto, 16, 0, 3), (240, 214, 120), 4.4, sp=5)
    for k in range(marcas * 2 + 1):
        y = -alto * k / (marcas * 2)
        ops += [T(linea((-16, y), (-16 + (22 if k % 2 == 0 else 12), y)), 3, peso=0.01)]
    return Dib(ops)
