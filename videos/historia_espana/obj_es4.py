# -*- coding: utf-8 -*-
"""Dibujos de boceto para la historia de España (4/4): siglos XIX y XX y cierre.
Napoleón y sus soldados, el pueblo del 2 de mayo, guerrillero, Goya y su «3 de mayo», la Constitución de Cádiz, un libertador,
banderas de las repúblicas americanas, Isabel II al exilio, Amadeo que renuncia, calendario de 11 meses, acorazado y buques de 1898,
bandera de la República, miliciano y soldado sublevado, bombardero, Guernica en llamas, general, cartilla de racionamiento,
sello de censura, turistas, sombrilla, SEAT 600, el rey Juan Carlos, urna y Constitución de 1978, tricornio tachado,
estrellas de Europa, aros olímpicos, Sagrada Familia, globo «¡Hola!»."""
import math
from functools import lru_cache

import numpy as np

import obj_base as OB
import obj_es1  # noqa: F401
import obj_es2  # noqa: F401
import obj_es3  # noqa: F401
from obj_a import colocar
from obj_base import *  # noqa: F401,F403
from obj_es1 import BLANCO_R, HIERRO, NEGRO_R, ROCA, ROCA_OSC

AZUL_FR = (50, 70, 140)
GRIS_FR = (130, 130, 140)
CAQUI = (150, 140, 100)
AZUL_MONO = (70, 100, 160)
MORADO_R = (110, 70, 140)
AMARILLO_R = (240, 196, 60)
ROJO_R = (200, 50, 50)

_orig = OB.sombrero


def _sombrero(nombre, cy=-215.0):
    if nombre == "bicornio":
        ops = forma(curva([(-80, cy - 30), (-40, cy - 60), (0, cy - 90), (40, cy - 60), (80, cy - 30), (40, cy - 40), (0, cy - 46), (-40, cy - 40)], 6), NEGRO_R, 4.8, sp=7)
        return ops + [R(circ(0, cy - 62, 9, n=12), (60, 80, 170), peso=0.01, sp=3), R(circ(0, cy - 62, 5, n=10), (220, 60, 60), peso=0.01, sp=3)]
    if nombre == "chaco":             # chacó de soldado francés
        return forma(pol((-36, cy - 20), (-40, cy - 90), (40, cy - 90), (36, cy - 20)), NEGRO_R, 4.6, sp=7) + forma(rect(-40, cy - 30, 40, cy - 20, 2), NEGRO_R, 3.4, sp=3) + \
            forma(elip(0, cy - 100, 9, 12, 0, 1.0, 12), (220, 60, 60), 3, sp=3)
    if nombre == "panuelo":           # pañuelo anudado (guerrillero, majo)
        ops = forma(curva([(-46, cy - 14), (-48, cy - 44), (0, cy - 62), (48, cy - 44), (46, cy - 14)], 5).tolist() + [(0, cy - 26)], (200, 60, 50), 4.4, sp=6)
        return ops + forma(pol((44, cy - 30), (70, cy - 16), (60, cy + 2)), (200, 60, 50), 3.4, sp=3)
    if nombre == "chistera":
        return forma(rect(-30, cy - 100, 30, cy - 34, 4), NEGRO_R, 4.6, sp=7) + forma(rect(-52, cy - 40, 52, cy - 28, 4), NEGRO_R, 4.4, sp=6)
    if nombre == "gorrillo":          # gorrillo cuartelero del miliciano
        return forma(pol((-44, cy - 30), (-36, cy - 58), (36, cy - 64), (46, cy - 30)), (200, 60, 50), 4.4, sp=6) + [rayita(-30, cy - 44, 30, cy - 50, 3)]
    if nombre == "casco_36":
        return forma(curva([(-56, cy - 18), (-46, cy - 56), (0, cy - 74), (46, cy - 56), (56, cy - 18)], 6).tolist() + [(-56, cy - 18)], (110, 112, 90), 4.6, sp=7)
    if nombre == "gorra_general":
        ops = forma(rect(-44, cy - 60, 44, cy - 32, 10), CAQUI, 4.6, sp=8) + forma(rect(-50, cy - 36, 50, cy - 24, 4), (60, 50, 40), 4.2, sp=5)
        return ops + [R(circ(0, cy - 48, 8, n=12), ORO, peso=0.02, sp=4)]
    if nombre == "tricornio":
        return forma(curva([(-70, cy - 26), (-60, cy - 60), (-20, cy - 74), (20, cy - 74), (60, cy - 60), (70, cy - 26), (40, cy - 40), (0, cy - 44), (-40, cy - 40)], 6),
                     NEGRO_R, 4.8, sp=7)
    if nombre == "sombrero_playa":
        return forma(elip(0, cy - 36, 74, 16, 0, 1.0, 30), (240, 220, 160), 4.4, sp=6) + forma(curva([(-36, cy - 40), (-30, cy - 70), (0, cy - 78), (30, cy - 70), (36, cy - 40)], 5),
                                                                                                (240, 220, 160), 4.2, sp=5) + forma(rect(-36, cy - 52, 36, cy - 42, 2), (220, 70, 60), 3, sp=3)
    if nombre == "gafas":
        return forma(elip(-16, cy - 4, 15, 11, 0, 1.0, 14), NEGRO_R, 3.6, sp=3) + forma(elip(16, cy - 4, 15, 11, 0, 1.0, 14), NEGRO_R, 3.6, sp=3) + \
            [T(linea((-2, cy - 6), (2, cy - 6)), 3, peso=0.01)] + forma(elip(0, cy - 10, 43, 36, math.pi, 0.5, 24), (120, 80, 56), 4.2, cerrada=False, sp=6)[1:]
    return _orig(nombre, cy)


OB.sombrero = _sombrero


def _acc_fusil(m, d):
    x, y = m
    return [T(linea((x - 20, y + 60), (x + 20, y - 150)), 5.4, peso=0.08), R(pol((x - 26, y + 66), (x - 8, y + 70), (x + 4, y + 10), (x - 10, y + 6)), (140, 96, 60), peso=0.03, sp=4),
            T(linea((x + 18, y - 140), (x + 24, y - 178)), 3, peso=0.02)]


def _acc_trabuco(m, d):
    x, y = m
    return [T(linea((x - 10, y + 30), (x + 80, y - 40)), 6, peso=0.05)] + forma(pol((x + 76, y - 50), (x + 100, y - 58), (x + 92, y - 32)), (120, 110, 100), 3.6, sp=3)


def _acc_maleta(m, d):
    x, y = m
    return forma(rect(x - 34, y + 4, x + 34, y + 54, 4), (150, 100, 60), 4.4, sp=5) + [T(arco_(x, y + 4, 12, 180, 360, 8), 4, peso=0.02)]


def _acc_bandera_rep(m, d):
    x, y = m
    ops = [T(linea((x, y + 40), (x + 4, y - 190)), 5, peso=0.12)]
    for k, c in enumerate((ROJO_R, AMARILLO_R, MORADO_R)):
        ops += [R(pol((x + 4, y - 188 + 26 * k), (x + 110, y - 184 + 26 * k), (x + 110, y - 158 + 26 * k), (x + 4, y - 162 + 26 * k)), c, peso=0.03, sp=5)]
    return ops + [T(pol((x + 4, y - 188), (x + 110, y - 184), (x + 110, y - 106), (x + 4, y - 110), (x + 4, y - 188)), 3.6, peso=0.04)]


def _acc_papeleta(m, d):
    x, y = m
    return forma(rect(x - 20, y - 50, x + 20, y + 4, 2), BLANCO_R, 3.6, sp=4) + [rayita(x - 12, y - 38 + 10 * k, x + 12, y - 38 + 10 * k, 2.2) for k in range(3)]


def _acc_camara(m, d):
    x, y = m
    return forma(rect(x - 26, y - 22, x + 26, y + 14, 4), NEGRO_R, 4, sp=4) + forma(elip(x, y - 4, 11, 11, 0, 1.0, 12), (150, 180, 210), 3, sp=3)


def _acc_constitucion(m, d):
    x, y = m
    return forma(rect(x - 30, y - 56, x + 30, y + 20, 4), (190, 60, 50), 4.2, sp=5) + forma(rect(x - 20, y - 44, x + 20, y - 26, 2), ORO, 3, sp=3)


OB.ACC.update({"fusil": _acc_fusil, "trabuco": _acc_trabuco, "maleta": _acc_maleta, "bandera_rep": _acc_bandera_rep, "papeleta": _acc_papeleta,
               "camara": _acc_camara, "constitucion": _acc_constitucion})


# ------------------------------------------------------------------ 1808-1898
@lru_cache(maxsize=None)
def napoleon(pose=0, cara="enojo"):
    return persona(GRIS_FR, PIEL_ROSA, "bicornio", cara, (16, 26), pose, traje="armadura", faja=(240, 236, 220), cuello=AZUL_FR, acc_d="espada")


@lru_cache(maxsize=None)
def soldado_frances(pose=0, cara="serio"):
    return persona(AZUL_FR, PIEL_ROSA, "chaco", cara, (12, 26), pose, traje="armadura", faja=BLANCO_R, acc_d="fusil")


@lru_cache(maxsize=None)
def jose_bonaparte(pose=0, cara="feliz"):
    return persona((90, 60, 120), PIEL_ROSA, "corona_real", cara, (16, 40), pose, traje="tunica", faja=ORO, cuello=BLANCO_R, acc_d="cetro")


@lru_cache(maxsize=None)
def madrileno(pose=0, cara="enojo"):
    return persona((230, 222, 200), PIEL_ROSA, "panuelo", cara, (120, 150), pose, traje="corta", faja=(200, 60, 50))


@lru_cache(maxsize=None)
def guerrillero(pose=0, cara="enojo"):
    return persona((120, 96, 70), PIEL_ROSA, "panuelo", cara, (16, 60), pose, traje="corta", faja=(200, 60, 50), barba=(110, 80, 60), acc_d="trabuco")


@lru_cache(maxsize=None)
def goya(pose=0, cara="serio"):
    return persona((70, 60, 70), PIEL_ROSA, "chistera", cara, (16, 80), pose, traje="tunica", cuello=BLANCO_R, acc_d="pincel", acc_i="paleta")


@lru_cache(maxsize=None)
def cuadro_3mayo():
    """Evocación de «El 3 de mayo de 1808» (Goya, 1814, dominio público): de noche, el hombre de camisa blanca y pantalón amarillo,
    de rodillas y con los brazos en cruz, iluminado por un gran farol en el suelo, frente al pelotón de fusilamiento."""
    ops = forma(rect(-220, -320, 220, 0, 4), (160, 120, 60), 6, peso=0.4, sp=9)
    ops += forma(rect(-200, -300, 200, -20, 3), (54, 50, 60), 4, peso=0.3, sp=9)                                      # noche
    ops += forma(pol((-200, -160), (-120, -230), (-40, -190), (-40, -20), (-200, -20)), (100, 88, 76), 3.4, sp=8)   # el cerro
    ops += forma(pol((-14, -100), (34, -100), (40, -40), (-20, -40)), (240, 210, 110), 4, sp=5)                      # farol
    ops += forma(pol((-150, -40), (-20, -40), (10, -110), (-180, -110)), (220, 190, 120), 3, sp=7)                  # la luz en el suelo
    ops += forma(pol((-118, -40), (-128, -86), (-94, -92), (-80, -40)), (230, 196, 70), 4, sp=4)                    # pantalón
    ops += forma(pol((-132, -84), (-128, -150), (-90, -150), (-90, -88)), BLANCO_R, 4.2, sp=5)                      # camisa
    ops += forma(pol((-128, -146), (-182, -214), (-170, -224), (-116, -158)), BLANCO_R, 3.6, sp=3)                  # brazos en cruz
    ops += forma(pol((-92, -146), (-40, -214), (-30, -204), (-86, -136)), BLANCO_R, 3.6, sp=3)
    ops += forma(elip(-108, -168, 15, 16, 0, 1.0, 16), (220, 180, 140), 3.6, sp=3) + forma(elip(-108, -180, 15, 8, math.pi, 0.5, 10), NEGRO_R, 3, cerrada=False, sp=3)[1:]
    ops += [punto(-114, -168, 4), punto(-102, -168, 4), T(elip(-108, -158, 4, 5, 0, 1.0, 8), 2.4, peso=0.01)]
    for k in range(5):                                                                                                 # pelotón, de espaldas
        x = 90 + 24 * k
        ops += forma(pol((x - 14, -40), (x - 20, -130), (x + 4, -150), (x + 14, -40)), (70, 66, 74), 3.4, sp=4)
        ops += forma(pol((x - 22, -150), (x + 8, -160), (x + 10, -142), (x - 16, -136)), (40, 38, 44), 3, sp=3)
        ops += [T(linea((x - 10, -118), (x - 96, -126)), 4.4, peso=0.02)]
    return Dib(ops)


@lru_cache(maxsize=None)
def constitucion_1812():
    ops = forma(rect(-120, -280, 120, 0, 8), (190, 60, 50), 5.4, peso=0.5, sp=9)
    ops += forma(rect(-90, -250, 90, -170, 4), (240, 226, 190), 4, sp=6)
    ops += [rayita(-70, -228 + 18 * k, 70, -228 + 18 * k, 3) for k in range(3)]
    ops += forma(elip(0, -100, 40, 40, 0, 1.0, 24), ORO, 4.2, sp=5)
    return Dib(ops)


@lru_cache(maxsize=None)
def diputado(pose=0, cara="feliz"):
    return persona((60, 70, 90), PIEL_ROSA, "pelo_castano", cara, (16, 130), pose, traje="tunica", cuello=BLANCO_R, acc_d="constitucion")


@lru_cache(maxsize=None)
def libertador(pose=0, cara="serio"):
    return persona((40, 60, 110), PIEL_ROSA, "bicornio", cara, (16, 150), pose, traje="armadura", faja=(220, 60, 60), cuello=ORO, acc_d="espada")


_BANDERAS = {   # colores de las banderas actuales (franjas simplificadas): (orientación, [colores], extra)
    "Mexico": ("v", [(0, 120, 70), (250, 250, 250), (206, 40, 50)]), "Guatemala": ("v", [(80, 160, 220), (250, 250, 250), (80, 160, 220)]),
    "Honduras": ("h", [(20, 90, 170), (250, 250, 250), (20, 90, 170)]), "El Salvador": ("h", [(20, 70, 160), (250, 250, 250), (20, 70, 160)]),
    "Nicaragua": ("h", [(30, 110, 200), (250, 250, 250), (30, 110, 200)]), "Costa Rica": ("h", [(20, 40, 120), (250, 250, 250), (206, 30, 40), (250, 250, 250), (20, 40, 120)]),
    "Panama": ("q", [(250, 250, 250), (210, 30, 40), (20, 60, 150), (250, 250, 250)]), "Colombia": ("h", [(250, 210, 30), (250, 210, 30), (20, 60, 150), (206, 20, 40)]),
    "Venezuela": ("h", [(250, 210, 30), (20, 50, 150), (206, 20, 40)]), "Ecuador": ("h", [(250, 210, 30), (250, 210, 30), (20, 60, 150), (206, 20, 40)]),
    "Peru": ("v", [(206, 20, 40), (250, 250, 250), (206, 20, 40)]), "Bolivia": ("h", [(206, 30, 40), (250, 210, 30), (0, 120, 60)]),
    "Chile": ("c", [(250, 250, 250), (210, 20, 40), (20, 50, 150)]), "Argentina": ("h", [(120, 180, 230), (250, 250, 250), (120, 180, 230)]),
    "Paraguay": ("h", [(206, 20, 40), (250, 250, 250), (20, 50, 150)]), "Uruguay": ("h", [(250, 250, 250), (20, 60, 160), (250, 250, 250), (20, 60, 160), (250, 250, 250)]),
    "Dominican Rep.": ("q", [(20, 50, 130), (206, 20, 40), (206, 20, 40), (20, 50, 130)]),
}


@lru_cache(maxsize=None)
def bandera_pais(pais, f=0):
    """Banderita en su mástil con los colores de cada república (simplificada, sin escudos)."""
    tipo, cols = _BANDERAS[pais]
    ops = [T(linea((0, 0), (0, -170)), 4.4, peso=0.06)]
    x0, y0, w, h = 2, -168, 110, 70
    ond = lambda x: 5 * math.sin(f * 2 + x / 30)
    if tipo == "v":
        n = len(cols)
        for k, c in enumerate(cols):
            xa, xb = x0 + w * k / n, x0 + w * (k + 1) / n
            ops += [R(pol((xa, y0 + ond(xa)), (xb, y0 + ond(xb)), (xb, y0 + h + ond(xb)), (xa, y0 + h + ond(xa))), c, peso=0.02, sp=4)]
    elif tipo == "h":
        n = len(cols)
        for k, c in enumerate(cols):
            ya, yb = y0 + h * k / n, y0 + h * (k + 1) / n
            ops += [R(pol((x0, ya + ond(x0)), (x0 + w, ya + ond(x0 + w)), (x0 + w, yb + ond(x0 + w)), (x0, yb + ond(x0))), c, peso=0.02, sp=4)]
    elif tipo == "q":
        for k, c in enumerate(cols):
            xa, ya = x0 + w / 2 * (k % 2), y0 + h / 2 * (k // 2)
            ops += [R(pol((xa, ya + ond(xa)), (xa + w / 2, ya + ond(xa + w / 2)), (xa + w / 2, ya + h / 2 + ond(xa + w / 2)), (xa, ya + h / 2 + ond(xa))), c, peso=0.02, sp=4)]
    elif tipo == "c":                     # Chile: franja blanca y roja con el cuadro azul
        ops += [R(pol((x0, y0 + ond(x0)), (x0 + w, y0 + ond(x0 + w)), (x0 + w, y0 + h / 2 + ond(x0 + w)), (x0, y0 + h / 2 + ond(x0))), cols[0], peso=0.02, sp=4),
                R(pol((x0, y0 + h / 2 + ond(x0)), (x0 + w, y0 + h / 2 + ond(x0 + w)), (x0 + w, y0 + h + ond(x0 + w)), (x0, y0 + h + ond(x0))), cols[1], peso=0.02, sp=4),
                R(pol((x0, y0 + ond(x0)), (x0 + w / 3, y0 + ond(x0 + w / 3)), (x0 + w / 3, y0 + h / 2 + ond(x0 + w / 3)), (x0, y0 + h / 2 + ond(x0))), cols[2], peso=0.01, sp=3)]
    borde = [(x0, y0 + ond(x0)), (x0 + w, y0 + ond(x0 + w)), (x0 + w, y0 + h + ond(x0 + w)), (x0, y0 + h + ond(x0)), (x0, y0 + ond(x0))]
    ops += [T(np.array(borde), 3.4, peso=0.04)]
    return Dib(ops)


@lru_cache(maxsize=None)
def isabel2(pose=0, cara="lloron"):
    return persona((70, 110, 170), PIEL_ROSA, "corona_real", cara, (16, 20), pose, traje="vestido", faja=ORO, cuello=BLANCO_R, acc_d="maleta")


@lru_cache(maxsize=None)
def amadeo(pose=0, cara="lloron"):
    return persona((40, 70, 120), PIEL_ROSA, "pelo_castano", cara, (16, 20), pose, traje="armadura", faja=ROJO_CH, barba=(130, 96, 70), bigote=True, acc_d="maleta")


@lru_cache(maxsize=None)
def calendario(hojas=11):
    """Taco de calendario con el número de meses."""
    ops = forma(rect(-90, -200, 90, 0, 6), BLANCO_R, 5, sp=8) + forma(rect(-90, -200, 90, -150, 6), (200, 60, 50), 4.6, sp=6)
    ops += [T(circ(-50, -200, 10, n=12), 4, peso=0.02), T(circ(50, -200, 10, n=12), 4, peso=0.02)]
    for k in range(3):
        for j in range(4):
            ops += [R(rect(-70 + 38 * j, -134 + 40 * k, -46 + 38 * j, -112 + 40 * k, 2), (220, 214, 200), peso=0.01, sp=3)]
    return Dib(ops)


@lru_cache(maxsize=None)
def acorazado(f=0, color=(130, 140, 150), bandera="eeuu"):
    """Acorazado/crucero de 1898: casco gris, dos chimeneas humeantes, torretas."""
    ops = forma(curva([(-230, -70), (-210, -10), (200, -10), (250, -70), (200, -64), (-200, -64)], 5), color, 5.4, peso=0.5, sp=9)
    ops += forma(rect(-120, -130, 80, -64, 4), (170, 176, 184), 4.6, sp=7)
    for x in (-60, 10):
        ops += forma(rect(x - 16, -210, x + 16, -130, 3), (190, 170, 120), 4.4, sp=5)
        for k in range(3):
            r = 18 + 8 * k
            ops += forma(elip(x + 20 * k + 6 * math.sin(f + k), -240 - 34 * k, r, r * 0.8, 0, 1.0, 14), (200, 200, 205), 3, sp=4)
    for x in (-180, 150):
        ops += forma(rect(x - 30, -100, x + 30, -64, 6), (150, 156, 164), 4, sp=5) + [T(linea((x, -86), (x + (80 if x > 0 else -80), -94)), 6, peso=0.02)]
    x, y = -200, -110
    ops += [T(linea((x, y), (x, y - 90)), 3.6, peso=0.04)]
    if bandera == "eeuu":
        for k in range(5):
            ops += [R(rect(x, y - 90 + 10 * k, x + 70, y - 85 + 10 * k, 1), (200, 40, 50) if k % 2 == 0 else BLANCO_R, peso=0.01, sp=3)]
        ops += [R(rect(x, y - 90, x + 28, y - 70, 1), (40, 60, 130), peso=0.01, sp=3), T(pol((x, y - 90), (x + 70, y - 90), (x + 70, y - 40), (x, y - 40), (x, y - 90)), 3, peso=0.02)]
    else:
        ops += [R(rect(x, y - 90, x + 70, y - 78, 1), (200, 40, 50), peso=0.01, sp=3), R(rect(x, y - 78, x + 70, y - 54, 1), (240, 196, 60), peso=0.01, sp=3),
                R(rect(x, y - 54, x + 70, y - 42, 1), (200, 40, 50), peso=0.01, sp=3), T(pol((x, y - 90), (x + 70, y - 90), (x + 70, y - 42), (x, y - 42), (x, y - 90)), 3, peso=0.02)]
    return Dib(ops)


# ------------------------------------------------------------------ siglo XX
@lru_cache(maxsize=None)
def bandera_republica(f=0):
    ops = [T(linea((0, 0), (0, -300)), 5, peso=0.1)]
    for k, c in enumerate((ROJO_R, AMARILLO_R, MORADO_R)):
        P = [(0, -298 + 40 * k), (180, -294 + 40 * k + 8 * math.sin(f)), (180, -254 + 40 * k + 8 * math.sin(f)), (0, -258 + 40 * k)]
        ops += [R(pol(*P), c, peso=0.04, sp=6)]
    ops += [T(np.array([(0, -298), (180, -294 + 8 * math.sin(f)), (180, -174 + 8 * math.sin(f)), (0, -178), (0, -298)]), 4, peso=0.05)]
    return Dib(ops)


@lru_cache(maxsize=None)
def ciudadano_1931(pose=0, cara="feliz", mujer=False):
    if mujer:
        return persona((200, 90, 90), PIEL_ROSA, "pelo_castano", cara, (150, 40), pose, traje="vestido", faja=(240, 200, 80))
    return persona((110, 100, 90), PIEL_ROSA, "gorra", cara, (150, 150), pose, traje="corta", faja=(80, 70, 60))


@lru_cache(maxsize=None)
def miliciano(pose=0, cara="enojo"):
    return persona(AZUL_MONO, PIEL_ROSA, "gorrillo", cara, (12, 30), pose, traje="corta", faja=(80, 70, 60), acc_d="fusil")


@lru_cache(maxsize=None)
def soldado_nacional(pose=0, cara="enojo"):
    return persona(CAQUI, PIEL_ROSA, "casco_36", cara, (12, 30), pose, traje="armadura", faja=(90, 80, 60), acc_d="fusil")


@lru_cache(maxsize=None)
def bombardero(f=0):
    """Bombardero bimotor de los años treinta, de lado: fuselaje grueso, cabina acristalada, motor con hélice y cola alta."""
    ops = forma(curva([(-210, -66), (-170, -88), (-40, -100), (110, -96), (196, -78), (214, -60), (190, -44), (80, -36), (-170, -46)], 6), (124, 130, 120), 5.2, peso=0.5, sp=9)
    ops += forma(pol((-196, -70), (-236, -146), (-206, -150), (-160, -86)), (124, 130, 120), 4.4, sp=5)                # timón
    ops += forma(pol((-60, -66), (70, -66), (40, -18), (-90, -18)), (104, 110, 100), 4.4, sp=6)                         # ala
    ops += forma(curva([(0, -76), (20, -96), (70, -100), (90, -80), (60, -64), (10, -62)], 5), (104, 110, 100), 4.2, sp=5)   # motor
    ops += forma(curva([(150, -94), (186, -84), (204, -66), (172, -66), (150, -76)], 4), (190, 214, 230), 3.6, sp=3)     # cabina
    for k in range(3):
        ops += [R(rect(-110 + 50 * k, -84, -84 + 50 * k, -68, 2), (190, 214, 230), peso=0.01, sp=3)]
    a = f * 11
    ops += [T(linea((96, -82 + 34 * math.cos(a)), (96, -82 - 34 * math.cos(a))), 4, peso=0.01)]
    ops += forma(elip(98, -82, 7, 7, 0, 1.0, 10), (60, 60, 64), 2.6, sp=2)
    return Dib(ops)


@lru_cache(maxsize=None)
def bomba():
    return Dib(forma(elip(0, -40, 14, 34, 0, 1.0, 16), (60, 60, 64), 3.6, sp=3) + forma(pol((-14, -76), (14, -76), (6, -64), (-6, -64)), (60, 60, 64), 3, sp=3))


@lru_cache(maxsize=None)
def pueblo_llamas(f=0):
    """Casas de un pueblo vasco (tejados a dos aguas) con llamas y humo."""
    ops = []
    for k, (x, w, h) in enumerate(((-150, 90, 90), (-40, 110, 120), (80, 90, 100), (170, 70, 80))):
        ops += forma(rect(x - w / 2, -h, x + w / 2, 0, 3), BLANCO_R, 4.6, sp=7)
        ops += forma(pol((x - w / 2 - 10, -h), (x, -h - 50), (x + w / 2 + 10, -h)), (190, 80, 60), 4.4, sp=6)
        ops += forma(rect(x - 10, -40, x + 10, 0, 2), (120, 80, 60), 3, sp=3)
        a = 0.3 * math.sin(f * 3 + k)
        ops += forma(pol((x - 26, -h - 20), (x - 6 + 10 * a, -h - 90), (x + 4, -h - 50), (x + 18 - 8 * a, -h - 110), (x + 30, -h - 20)), (250, 150, 50), 3.6, sp=4)
    return Dib(ops)


@lru_cache(maxsize=None)
def cuadro_gris():
    """Lienzo enorme en gris, blanco y negro (homenaje al «Guernica», sin copiar su composición): formas rotas y una bombilla."""
    ops = forma(rect(-260, -260, 260, 0, 4), (90, 90, 96), 6, peso=0.4, sp=10)
    ops += forma(pol((-240, -20), (-200, -200), (-120, -140), (-60, -230), (0, -120), (60, -200), (140, -110), (240, -180), (240, -20)), (170, 170, 176), 3.6, sp=8)
    ops += forma(pol((-150, -40), (-110, -120), (-60, -80), (-80, -40)), BLANCO_R, 3.4, sp=4)
    ops += forma(pol((60, -40), (90, -150), (140, -60)), (220, 220, 226), 3.4, sp=4)
    ops += forma(elip(0, -200, 40, 18, 0, 1.0, 20), BLANCO_R, 3.6, sp=4) + forma(elip(0, -200, 10, 12, 0, 1.0, 12), (240, 230, 160), 3, sp=3)
    ops += [T(linea((0, -218), (0, -250)), 3, peso=0.02)]
    return Dib(ops)


@lru_cache(maxsize=None)
def general(pose=0, cara="serio"):
    return persona(CAQUI, PIEL_ROSA, "gorra_general", cara, (16, 20), pose, traje="armadura", faja=(200, 60, 50), cuello=ORO, bigote=True)


@lru_cache(maxsize=None)
def cartilla():
    ops = forma(rect(-80, -200, 80, 0, 4), (230, 214, 180), 5, sp=8) + forma(rect(-80, -200, 80, -160, 4), (150, 120, 90), 4, sp=5)
    for k in range(4):
        for j in range(3):
            ops += [T(rect(-64 + 44 * j, -146 + 36 * k, -30 + 44 * j, -120 + 36 * k, 2), 2.6, peso=0.01)]
    ops += [T(linea((-50, -140), (-40, -126)), 3, peso=0.01), T(linea((-6, -140), (4, -126)), 3, peso=0.01)]
    return Dib(ops)


@lru_cache(maxsize=None)
def turista(pose=0, mujer=False):
    if mujer:
        return persona((240, 120, 140), (246, 200, 170), "sombrero_playa", "feliz", (20, 140), pose, traje="corta", faja=(250, 220, 90), acc_i="camara")
    return persona((250, 230, 120), (246, 200, 170), "gafas", "feliz", (20, 120), pose, traje="corta", faja=(80, 160, 200), acc_d="camara")


@lru_cache(maxsize=None)
def sombrilla(f=0):
    ops = [T(linea((0, 0), (6, -200)), 5, peso=0.06)]
    for k in range(6):
        a0, a1 = math.pi + k * math.pi / 6, math.pi + (k + 1) * math.pi / 6
        P = [(6, -200)] + [(6 + 130 * math.cos(a), -170 + 60 * math.sin(a)) for a in np.linspace(a0, a1, 6)]
        ops += forma(P, (230, 70, 60) if k % 2 == 0 else BLANCO_R, 3.6, sp=6)
    ops += forma(pol((-160, 10), (-150, -10), (160, -10), (170, 10)), (240, 220, 160), 3.4, sp=5)
    return Dib(ops)


@lru_cache(maxsize=None)
def seat600(f=0, color=(110, 160, 200)):
    """El SEAT 600 (1957), símbolo del desarrollo de los sesenta."""
    ops = forma(curva([(-150, -40), (-146, -80), (-110, -100), (-80, -150), (40, -156), (100, -110), (150, -90), (156, -40)], 6).tolist() + [(-150, -40)], color, 5.6, peso=0.5, sp=9)
    ops += forma(curva([(-74, -104), (-60, -140), (-6, -144), (-6, -104)], 4), (200, 226, 240), 3.8, sp=4)
    ops += forma(curva([(6, -104), (6, -144), (36, -142), (72, -108)], 4), (200, 226, 240), 3.8, sp=4)
    ops += forma(elip(140, -70, 10, 9, 0, 1.0, 10), (250, 240, 180), 3, sp=3)
    for x in (-90, 90):
        ops += forma(elip(x, -36, 30, 30, 0, 1.0, 20), NEGRO_R, 4.6, sp=5) + forma(elip(x, -36, 12, 12, 0, 1.0, 12), (200, 200, 205), 3, sp=3)
        ops += [T(linea((x, -36), (x + 12 * math.cos(f * 6), -36 + 12 * math.sin(f * 6))), 2.6, peso=0.01)]
    return Dib(ops)


@lru_cache(maxsize=None)
def juan_carlos(pose=0, cara="feliz"):
    return persona((60, 70, 100), PIEL_ROSA, "pelo_castano", cara, (16, 140), pose, traje="tunica", faja=(200, 60, 50), cuello=BLANCO_R)


@lru_cache(maxsize=None)
def votante(pose=0, cara="feliz", mujer=False, color=(200, 120, 80)):
    return persona(color, PIEL_ROSA, "pelo_castano" if not mujer else "pelo_rubio", cara, (16, 100), pose, traje="vestido" if mujer else "tunica", acc_d="papeleta")


@lru_cache(maxsize=None)
def urna():
    ops = forma(pol((-110, -200), (110, -200), (96, 0), (-96, 0)), (200, 226, 236), 5.2, peso=0.4, sp=9)
    ops += forma(rect(-60, -210, 60, -192, 3), NEGRO_R, 3.6, sp=3)
    ops += forma(rect(-36, -250, 36, -200, 2), BLANCO_R, 3.6, sp=4) + [rayita(-24, -236 + 10 * k, 24, -236 + 10 * k, 2.4) for k in range(3)]
    return Dib(ops)


@lru_cache(maxsize=None)
def constitucion_1978():
    ops = forma(rect(-120, -280, 120, 0, 8), (200, 60, 50), 5.4, peso=0.5, sp=9)
    ops += forma(rect(-96, -256, 96, -160, 4), (250, 210, 70), 4, sp=6)
    ops += forma(elip(0, -90, 40, 40, 0, 1.0, 24), ORO, 4.2, sp=5)
    return Dib(ops)


@lru_cache(maxsize=None)
def tricornio_tachado():
    ops = OB.sombrero("tricornio", 0.0)
    ops = colocar(ops, 0, 40, 2.6)
    ops += [T(linea((-150, -180), (150, 60)), 12, peso=0.06), T(linea((150, -180), (-150, 60)), 12, peso=0.06)]
    return Dib(ops)


@lru_cache(maxsize=None)
def estrellas_europa(f=0):
    """Círculo de doce estrellas amarillas sobre azul."""
    ops = forma(rect(-180, -330, 180, 0, 6), (40, 70, 160), 5, peso=0.4, sp=9)
    for k in range(12):
        a = k * math.pi / 6
        cx, cy = 110 * math.cos(a), -165 + 110 * math.sin(a)
        P = []
        for j in range(10):
            r = 18 if j % 2 == 0 else 7
            b = -math.pi / 2 + j * math.pi / 5
            P.append((cx + r * math.cos(b), cy + r * math.sin(b)))
        ops += forma(P, (250, 210, 60), 2.8, sp=3)
    return Dib(ops)


@lru_cache(maxsize=None)
def aros_olimpicos():
    ops = []
    for (x, y, c) in ((-110, -140, (40, 110, 200)), (0, -140, (40, 40, 44)), (110, -140, (220, 50, 50)), (-55, -90, (240, 190, 40)), (55, -90, (40, 150, 70))):
        ops += [T(circ(x, y, 50, n=40), 9, peso=0.1)]
        ops += [R(np.vstack([circ(x, y, 54, n=30), circ(x, y, 44, n=30)[::-1]]), c, peso=0.03, sp=4)]
    return Dib(ops)


@lru_cache(maxsize=None)
def sagrada_familia():
    """Las torres de la Sagrada Familia (Gaudí), con grúas: el templo sin terminar."""
    ops = []
    for k, (x, h, w) in enumerate(((-120, 230, 26), (-70, 270, 28), (70, 270, 28), (120, 230, 26), (0, 330, 34))):
        P = [(x - w, 0), (x - w * 0.8, -h * 0.6), (x - w * 0.4, -h * 0.9), (x, -h), (x + w * 0.4, -h * 0.9), (x + w * 0.8, -h * 0.6), (x + w, 0)]
        ops += forma(curva(P, 5), (226, 206, 170), 4.6, peso=0.3, sp=7)
        ops += forma(elip(x, -h - 10, 10, 12, 0, 1.0, 12), (230, 170, 70), 3, sp=3)
        ops += [T(linea((x - w * 0.5, -h * 0.3 - 20 * j), (x + w * 0.5, -h * 0.3 - 20 * j)), 2.2, peso=0.01, v=150) for j in range(4)]
    ops += forma(rect(-160, -110, 160, 0, 3), (214, 194, 160), 4.6, sp=8)
    ops += forma(curva([(-40, 0), (-40, -60), (0, -90), (40, -60), (40, 0)], 4), (150, 110, 80), 4, sp=5)
    ops += [T(linea((180, 0), (180, -340)), 4, peso=0.05), T(linea((120, -330), (260, -330)), 4, peso=0.04)]
    return Dib(ops)


@lru_cache(maxsize=None)
def globo_hola(txt="¡HOLA!"):
    """Globo de diálogo (el texto lo pone la escena)."""
    ops = forma(curva([(-110, -60), (-116, -130), (-60, -170), (60, -170), (116, -130), (110, -60), (60, -36), (-10, -36), (-40, 0), (-40, -38), (-80, -44)], 6),
                BLANCO_R, 4.6, sp=8)
    return Dib(ops)


@lru_cache(maxsize=None)
def multitud_mezcla(pose=0):
    """Fila de personajes de todas las épocas (cierre)."""
    import obj_es1 as E1
    import obj_es2 as E2
    import obj_es3 as E3
    figs = [E1.ibero(pose, "feliz"), E1.legionario(pose, "feliz"), E1.rey_godo(pose, "feliz"), E2.califa(pose, "feliz"), E2.exiliado(pose), E2.isabel(pose, "feliz"),
            E3.cervantes(pose, "feliz"), goya(pose, "feliz"), turista(pose, True)]
    ops = []
    for k, d in enumerate(figs):
        ops += colocar(list(d.ops), -400 + 100 * k, (k % 2) * 16, 0.62)
    return Dib(ops)
