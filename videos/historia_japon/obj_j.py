# -*- coding: utf-8 -*-
"""Objetos propios de Japón (boceto): samuráis, castillo, torii, cerezo, barcos, arcabuz, hongo atómico…"""
import math
from functools import lru_cache

import numpy as np

import obj_base as OB
from obj_a import colocar
from obj_base import *  # noqa: F401,F403
from obj_base import _rotar

ROJO_TORII = (206, 70, 50)
BLANCO_ROS = (250, 238, 236)
ROSA_FL = (246, 176, 192)
ROSA_OSC = (226, 130, 156)
AZUL_NOCHE = (60, 70, 110)
TEJA = (84, 92, 110)
MURO = (244, 238, 222)
LACA = (54, 44, 60)

# ------------------------------------------------------------------ sombreros nuevos (se enganchan al constructor de personas)
_orig_sombrero = OB.sombrero


def _sombrero(nombre, cy=-215.0):
    if nombre == "kabuto":            # casco de samurái con cuernos de media luna
        ops = forma([(-46, cy - 14), (-44, cy - 56), (0, cy - 74), (44, cy - 56), (46, cy - 14), (30, cy - 26), (-30, cy - 26)], LACA, 4.6, sp=8)
        ops += forma(pol((-50, cy - 28), (-70, cy - 12), (-44, cy - 8)), LACA, 4, sp=6) + forma(pol((50, cy - 28), (70, cy - 12), (44, cy - 8)), LACA, 4, sp=6)
        ops += [R(pol((-8, cy - 72), (-30, cy - 120), (-2, cy - 96), (0, cy - 76)), ORO, peso=0.03, sp=4), R(pol((8, cy - 72), (30, cy - 120), (2, cy - 96), (0, cy - 76)), ORO, peso=0.03, sp=4)]
        return ops + [T(linea((-10, cy - 70), (-30, cy - 120)), 3.6, peso=0.03), T(linea((10, cy - 70), (30, cy - 120)), 3.6, peso=0.03)]
    if nombre == "eboshi":            # sombrero alto y negro de la corte de Heian
        return forma(pol((-30, cy - 34), (-20, cy - 104), (14, cy - 114), (44, cy - 88), (34, cy - 34)), LACA, 4.6, sp=8)
    if nombre == "chonmage":          # moño de samurái
        ops = forma(elip(0, cy - 8, 43, 36, math.pi, 0.5, 26), LACA, 4.5, cerrada=False, sp=7)[1:]
        return ops + forma(pol((-8, cy - 38), (-6, cy - 62), (12, cy - 78), (16, cy - 60), (8, cy - 40)), LACA, 4, sp=6)
    if nombre == "gorra_meiji":
        ops = forma(rect(-44, cy - 56, 44, cy - 30, 10), (44, 54, 92), 4.6, sp=8) + forma(rect(-48, cy - 36, 48, cy - 24, 4), (30, 38, 70), 4.2, sp=6)
        return ops + [R(circ(0, cy - 44, 8, n=12), ORO, peso=0.02, sp=4)]
    if nombre == "peinado_heian":     # cabello largo liso
        return forma(elip(0, cy - 10, 43, 38, math.pi, 0.5, 26), LACA, 4.5, cerrada=False, sp=7)[1:]
    if nombre == "moño_geisha":
        ops = forma(elip(0, cy - 10, 44, 38, math.pi, 0.5, 26), LACA, 4.5, cerrada=False, sp=7)[1:]
        ops += forma(elip(0, cy - 58, 30, 18, 0, 1.0, 20), LACA, 4.4, sp=6)
        return ops + [R(circ(22, cy - 54, 6, n=10), ROSA_OSC, peso=0.02, sp=3), rayita(-10, cy - 60, -40, cy - 80, 3.4)]
    return _orig_sombrero(nombre, cy)


OB.sombrero = _sombrero


# ------------------------------------------------------------------ accesorios nuevos
def _acc_katana(m, d):
    x, y = m
    return [T(linea((x - 6, y + 30), (x + 18, y - 150)), 4.6, peso=0.04), R(pol((x + 12, y - 142), (x + 20, y - 154), (x + 26, y - 130), (x - 6, y + 10), (x - 10, y + 6)), GRIS_CL, peso=0.04, sp=4),
            R(rect(x - 22, y + 6, x - 2, y + 12, 2), ORO, peso=0.02, sp=3), T(linea((x - 18, y + 8), (x + 2, y + 10)), 5, peso=0.02)]


def _acc_arcabuz(m, d):
    x, y = m
    return [T(linea((x - 30, y + 26), (x + 120, y - 30)), 7, peso=0.05), R(pol((x - 34, y + 18), (x - 12, y + 34), (x + 20, y + 6), (x + 8, y - 2)), MADERA, peso=0.04, sp=5)]


def _acc_pincel_tinta(m, d):
    x, y = m
    return [T(linea((x, y + 10), (x + 20, y - 56)), 5, peso=0.04), R(pol((x + 14, y - 52), (x + 26, y - 82), (x + 32, y - 54)), NEGRO, peso=0.03, sp=4)]


OB.ACC["katana"] = _acc_katana
OB.ACC["arcabuz"] = _acc_arcabuz
OB.ACC["pincel_tinta"] = _acc_pincel_tinta


# ------------------------------------------------------------------ personajes
@lru_cache(maxsize=None)
def samurai(pose=0, brazos=(14, 28), cara="serio", color=(150, 48, 48)):
    return persona(color, PIEL, "kabuto", cara, brazos, pose, traje="armadura", faja=ORO, acc_d="katana", bigote=True)


@lru_cache(maxsize=None)
def samurai_paz(pose=0, cara="normal"):
    return persona((84, 100, 140), PIEL, "chonmage", cara, (16, 16), pose, traje="tunica", faja=ORO, acc_d="katana")


@lru_cache(maxsize=None)
def ashigaru(pose=0, cara="enojo"):
    return persona((120, 100, 80), PIEL, "paja", cara, (40, 50), pose, traje="corta", acc_d="arcabuz")


@lru_cache(maxsize=None)
def emperador_jp(pose=0, cara="serio"):
    return persona(CREMA, PIEL_CL, "eboshi", cara, (16, 16), pose, traje="vestido", faja=ROJO_TORII, cuello=ROJO_TORII)


@lru_cache(maxsize=None)
def dama_heian(pose=0):
    return persona(ROSA_OSC, PIEL_CL, "peinado_heian", "feliz", (14, 40), pose, traje="vestido", faja=ROSA_FL, acc_d="pincel_tinta", pelo_largo=LACA)


@lru_cache(maxsize=None)
def emperador_meiji(pose=0, cara="serio"):
    return persona((44, 54, 92), PIEL, "gorra_meiji", cara, (16, 16), pose, traje="armadura", faja=ORO, bigote=True)


@lru_cache(maxsize=None)
def oficial_naval(pose=0):
    return persona((230, 230, 236), PIEL, "gorra_oficial", "serio", (16, 16), pose, traje="corta", bigote=True, acc_d="espada")


@lru_cache(maxsize=None)
def marino_yanqui(pose=0):
    return persona((60, 80, 130), PIEL_ROSA, "bombin", "serio", (16, 40), pose, traje="corta", acc_d="bandera")


@lru_cache(maxsize=None)
def comerciante(pose=0):
    return persona((176, 120, 78), PIEL, "chonmage", "feliz", (20, 50), pose, traje="corta", acc_d="saco")


@lru_cache(maxsize=None)
def obrero_jp(pose=0):
    return persona((94, 130, 170), PIEL, "gorra", "feliz", (20, 40), pose, traje="corta", acc_d="azada")


@lru_cache(maxsize=None)
def geisha(pose=0):
    return persona(ROJO_TORII, PIEL_CL, "moño_geisha", "feliz", (14, 30), pose, traje="vestido", faja=ORO, acc_d="abanico")


@lru_cache(maxsize=None)
def campesino_jp(pose=0):
    return persona((176, 160, 112), PIEL, "paja", "feliz", (14, 46), pose, traje="corta", acc_d="mijo")


@lru_cache(maxsize=None)
def nino_jp(pose=0):
    d = persona(ROJO_TORII, PIEL, "chonmage", "feliz", (20, 20), pose, traje="corta")
    return Dib(colocar(list(d.ops), 0, 0, 0.7))


# ------------------------------------------------------------------ edificios y lugares
@lru_cache(maxsize=None)
def torii():
    ops = forma(rect(-110, -300, 110, -270, 4), ROJO_TORII, 5.4, peso=0.5, sp=9)
    ops += forma(pol((-140, -312), (-110, -290), (110, -290), (140, -312), (150, -330), (-150, -330)), LACA, 5.4, sp=8)
    ops += forma(rect(-84, -262, 84, -246, 3), ROJO_TORII, 4.6, sp=7)
    ops += forma(rect(-92, -270, -68, 0, 3), ROJO_TORII, 5, peso=0.3, sp=8) + forma(rect(68, -270, 92, 0, 3), ROJO_TORII, 5, peso=0.3, sp=8)
    ops += forma(rect(-16, -300, 16, -262, 2), LACA, 4, sp=6)
    return Dib(ops)


def _techo(ancho, y, alto, col=TEJA):
    """Techo de teja curvado con aleros levantados."""
    P = [(-ancho - 26, y - alto * 0.35), (-ancho * 0.6, y - alto * 0.05), (0, y), (ancho * 0.6, y - alto * 0.05), (ancho + 26, y - alto * 0.35),
         (ancho, y - alto), (0, y - alto * 1.25), (-ancho, y - alto)]
    return forma(P, col, 5, peso=0.5, sp=8)


@lru_cache(maxsize=None)
def castillo():
    """Castillo japonés de cinco pisos sobre una base de piedra (estilo Himeji)."""
    ops = forma(pol((-170, 0), (-130, -110), (130, -110), (170, 0)), PIEDRA, 5.6, peso=0.6, sp=9)
    niveles = [(120, -110, 78), (96, -196, 70), (74, -272, 62), (52, -338, 54)]
    for ancho, y, alto in niveles:
        ops += forma(rect(-ancho + 8, y - alto + 10, ancho - 8, y, 2), MURO, 5, sp=9)
        ops += [R(rect(-ancho + 26 + 34 * k, y - alto + 30, -ancho + 44 + 34 * k, y - alto + 48, 2), LACA, peso=0.02, sp=3) for k in range(int((ancho - 26) // 17))][:5]
        ops += _techo(ancho, y - alto + 14, 40)
    ops += forma(rect(-30, -398, 30, -358, 2), MURO, 4.6, sp=8) + _techo(40, -352, 30, TEJA)
    ops += [R(pol((-14, -434), (0, -452), (14, -434)), ORO, peso=0.02, sp=3)]
    return Dib(ops)


@lru_cache(maxsize=None)
def templo():
    ops = forma(rect(-110, -96, 110, 0, 3), MURO, 5, sp=9) + [R(rect(-14, -76, 14, 0, 2), LACA, peso=0.02, sp=3)]
    ops += [T(linea((-80 + 40 * k, -96), (-80 + 40 * k, 0)), 3, peso=0.03) for k in range(5)]
    ops += _techo(120, -92, 70)
    ops += forma(rect(-24, -180, 24, -150, 2), MURO, 4.4, sp=8) + _techo(40, -150, 36)
    return Dib(ops)


@lru_cache(maxsize=None)
def kofun():
    """Tumba en forma de ojo de cerradura, vista desde el aire (foso azul y montículo verde)."""
    P = pol((-150, 0), (-100, -46), (-40, -50), (-10, -34), (40, -20), (130, -24), (160, 0), (130, 24), (40, 20), (-10, 34), (-40, 50), (-100, 46))
    ops = forma(P, (150, 196, 224), 5.4, peso=0.7, sp=8)
    Q = pol((-110, 0), (-76, -28), (-36, -30), (-6, -16), (40, -8), (110, -10), (126, 0), (110, 10), (40, 8), (-6, 16), (-36, 30), (-76, 28))
    ops += forma(Q, (122, 160, 104), 4.8, peso=0.6, sp=8)
    ops += forma(elip(-58, 0, 24, 16, 0, 1.0, 18), (98, 136, 84), 3.8, sp=6)
    return Dib(ops)


@lru_cache(maxsize=None)
def cerezo(f=0, flor=1.0):
    ops = forma(curva([(-18, 0), (-10, -70), (-30, -150), (-46, -210)], 7), MADERA_OSC, 5.6, peso=0.5, sp=9, cerrada=False)
    ops += [T(curva([(-10, -70), (14, -120), (40, -170)], 7), 6, peso=0.1), T(curva([(-30, -150), (-70, -176), (-96, -214)], 7), 5, peso=0.1), T(curva([(14, -120), (64, -130), (92, -160)], 6), 4.6, peso=0.1)]
    if flor > 0:
        rng = np.random.default_rng(3)
        for k in range(int(30 * flor)):
            a = rng.uniform(0, 6.283)
            r = rng.uniform(20, 120)
            cx, cy = -10 + 1.25 * r * math.cos(a), -200 + 0.85 * r * math.sin(a)
            ops += [R(circ(cx, cy, rng.uniform(16, 26), n=10), ROSA_FL if k % 3 else ROSA_OSC, peso=0.02, sp=4)]
    return Dib(ops)


@lru_cache(maxsize=None)
def monte_fuji():
    ops = forma(pol((-220, 0), (-70, -200), (-30, -236), (30, -236), (70, -200), (220, 0)), (104, 130, 184), 5.6, peso=0.7, sp=9)
    ops += forma(pol((-74, -196), (-34, -232), (34, -232), (74, -196), (44, -178), (20, -200), (0, -172), (-24, -202), (-48, -176)), BLANCO, 4.8, sp=7)
    return Dib(ops)


@lru_cache(maxsize=None)
def gran_ola():
    """La gran ola (estilo grabado): cresta con garras de espuma y el Fuji al fondo."""
    ops = colocar(list(monte_fuji().ops), 60, 0, 0.45)
    ops += forma(curva([(-180, 0), (-176, -80), (-130, -160), (-60, -190), (0, -150), (-30, -110), (-60, -130), (-80, -90), (-50, -30), (40, 0)], 8), (70, 100, 160), 5.6, peso=0.7, sp=8)
    ops += [R(pol((-60, -190), (-20, -200), (10, -160), (0, -150), (-30, -170)), BLANCO, peso=0.02, sp=4)]
    for k in range(5):
        ops += [R(circ(-70 + 16 * k, -198 - 6 * (k % 2), 7, n=8), BLANCO, peso=0.02, sp=3)]
    ops += [T(ondas(-200, 200, -2, 6, 60), 4.4, peso=0.1)]
    return Dib(ops)


# ------------------------------------------------------------------ barcos, armas y máquinas
@lru_cache(maxsize=None)
def barco_mongol():
    ops = forma(curva([(-150, -60), (-120, -6), (0, 10), (130, -4), (170, -76)], 7), (92, 110, 150), 5.6, peso=0.6, sp=9)
    for k, x in enumerate((-70, 30, 110)):
        h = 200 - 20 * k
        ops += [T(linea((x, -62), (x, -62 - h)), 5.4, peso=0.12)]
        ops += forma(pol((x + 4, -62 - h + 6), (x + 54, -62 - h * 0.86), (x + 58, -62 - 28), (x + 4, -62 - 22)), (236, 226, 196), 4.6, peso=0.35, sp=8)
    ops += [R(pol((-150, -62), (-176, -116), (-150, -96)), ROJO_CH, peso=0.04, sp=4)]
    return Dib(ops)


@lru_cache(maxsize=None)
def barco_negro(f=0):
    """Buque de vapor negro con ruedas de paletas (el de Perry)."""
    ops = forma(pol((-200, -84), (-160, -8), (170, -8), (220, -96)), (44, 44, 52), 5.8, peso=0.8, sp=10)
    ops += forma(rect(-130, -138, 130, -84, 6), (70, 70, 84), 5, peso=0.5, sp=9)
    ops += [R(circ(-120 + 40 * k, -70, 8, n=10), (20, 20, 26), peso=0.02, sp=3) for k in range(7)]
    ops += forma(rect(-30, -244, 14, -138, 4), (34, 34, 40), 5, peso=0.3, sp=8)
    for ph in ((f * 0.33) % 1.0, (f * 0.33 + 0.5) % 1.0):
        ops += [T(circ(-8 + 30 * ph, -262 - 90 * ph, 18 + 30 * ph, n=16), 4 * (1 - 0.4 * ph), peso=0.06)]
    ops += [T(linea((60, -138), (60, -270)), 5, peso=0.1)] + forma(pol((60, -270), (120, -256), (60, -236)), (200, 60, 60), 3.8, sp=6)
    ops += [T(ondas(-190, 210, -4, 5, 52, f * 0.9), 4.4, peso=0.12)]
    return Dib(ops)


@lru_cache(maxsize=None)
def locomotora(f=0):
    ops = forma(rect(-110, -110, 70, -40, 8), (60, 70, 84), 5.4, peso=0.5, sp=9)
    ops += forma(rect(70, -150, 130, -40, 6), (60, 70, 84), 5, sp=8) + forma(rect(-80, -160, -44, -110, 4), (34, 34, 40), 4.8, sp=7)
    for x in (-80, -30, 30, 94):
        ops += forma(circ(x, -34, 26, n=20), GRIS_OSC, 4.8, sp=7) + [T(linea((x, -34), (x + 24 * math.cos(f * 0.9 + x), -34 + 24 * math.sin(f * 0.9 + x))), 3.6, peso=0.02)]
    ph = (f * 0.3) % 1.0
    ops += [T(circ(-60 + 10 * ph, -186 - 70 * ph, 16 + 26 * ph, n=14), 4 * (1 - 0.4 * ph), peso=0.06)]
    ops += [T(linea((-130, -8), (170, -8)), 4.4, peso=0.05)]
    return Dib(ops)


@lru_cache(maxsize=None)
def bandera_japon():
    ops = [T(linea((0, 40), (4, -200)), 5.4, peso=0.12)]
    ops += forma(rect(4, -200, 170, -90, 3), BLANCO, 4.6, sp=8)
    ops += [R(circ(87, -145, 28, n=24), (204, 50, 50), peso=0.02, sp=4), T(circ(87, -145, 28, n=24), 3.4, peso=0.05)]
    return Dib(ops)


@lru_cache(maxsize=None)
def sol_naciente():
    ops = forma(circ(0, 0, 70, n=30), (204, 50, 50), 5, peso=0.3, sp=8)
    for k in range(16):
        a = k * 6.2832 / 16
        c = (236, 168, 70) if k % 2 == 0 else (236, 210, 120)
        ops += [R(pol((80 * math.cos(a - 0.1), 80 * math.sin(a - 0.1)), (170 * math.cos(a), 170 * math.sin(a)), (80 * math.cos(a + 0.1), 80 * math.sin(a + 0.1))), c, peso=0.02, sp=4)]
    return Dib(ops)


@lru_cache(maxsize=None)
def hongo(f=0):
    """Nube de hongo (estilo boceto, sin nada gráfico)."""
    P = [(-34, 0), (-30, -90), (-48, -140), (-112, -160), (-134, -214), (-96, -268), (-34, -290), (34, -290), (96, -268), (134, -214), (112, -160), (48, -140), (30, -90), (34, 0)]
    ops = forma(curva(P, 8), (214, 120, 70), 5.6, peso=0.7, sp=9)
    ops += forma(curva([(-70, -190), (-60, -240), (0, -262), (60, -240), (70, -190), (20, -170), (-20, -170)], 8), (238, 176, 96), 4.4, sp=7)
    ops += [T(ondas(-150, 150, -2, 4, 40, f * 0.6), 4.2, peso=0.1)]
    return Dib(ops)


@lru_cache(maxsize=None)
def humo_bomba(f=0):
    ops = forma(elip(0, 0, 90, 50, 0, 1.0, 26), (150, 140, 140), 5, peso=0.6, sp=9)
    ops += forma(elip(-50, -34, 60, 40, 0, 1.0, 24), (180, 170, 170), 4.6, sp=8) + forma(elip(40, -40, 70, 44, 0, 1.0, 24), (190, 180, 180), 4.6, sp=8)
    return Dib(ops)


@lru_cache(maxsize=None)
def avion_zero(f=0):
    ops = forma(elip(0, -40, 120, 22, 0, 1.0, 26), (130, 160, 130), 5.2, peso=0.5, sp=9)
    ops += forma(pol((-20, -44), (30, -44), (10, -110), (-30, -110)), (130, 160, 130), 4.8, sp=8) + forma(pol((-20, -32), (30, -32), (10, 30), (-30, 30)), (130, 160, 130), 4.8, sp=8)
    ops += forma(pol((-112, -48), (-140, -96), (-116, -96), (-92, -56)), (130, 160, 130), 4.2, sp=6)
    ops += [R(circ(-8, -42, 12, n=12), (204, 50, 50), peso=0.02, sp=3)]
    ops += [T(linea((124, -62), (124, -18)), 4.4, peso=0.02 + 0.02 * math.sin(f)), T(linea((112, -40), (136, -40)), 4.4, peso=0.02)]
    return Dib(ops)


@lru_cache(maxsize=None)
def radio():
    ops = forma(rect(-60, -80, 60, 0, 8), (176, 120, 78), 5.4, peso=0.5, sp=9)
    ops += forma(circ(-24, -40, 26, n=20), CREMA, 4.6, sp=7) + [T(linea((-24, -40), (-10, -52)), 3.6, peso=0.02)]
    ops += [R(rect(14, -66, 50, -14, 4), (90, 70, 60), peso=0.02, sp=4)] + [rayita(18, -58 + 10 * k, 46, -58 + 10 * k, 3) for k in range(5)]
    ops += [T(linea((0, -80), (-40, -150)), 4, peso=0.04)]
    return Dib(ops)


@lru_cache(maxsize=None)
def aros_olimpicos():
    cols = [(60, 110, 190), (40, 40, 50), (204, 50, 50), (238, 190, 60), (60, 160, 90)]
    pos = [(-70, -30), (0, -30), (70, -30), (-35, 6), (35, 6)]
    ops = []
    for c, (x, y) in zip(cols, pos):
        ops += [T(circ(x, y, 30, n=22), 8, peso=0.05), R(circ(x, y, 28, n=22, vuelta=1.0), c, peso=0.0, sp=5)]
    return Dib(ops)


@lru_cache(maxsize=None)
def mascara_kabuki():
    ops = forma(elip(0, 0, 54, 66, 0, 1.0, 30), BLANCO, 5, peso=0.5, sp=9)
    ops += [R(pol((-40, -20), (-14, -8), (-16, -24)), (204, 50, 50), peso=0.02, sp=3), R(pol((40, -20), (14, -8), (16, -24)), (204, 50, 50), peso=0.02, sp=3)]
    ops += [T(linea((-42, -30), (-16, -14)), 5, peso=0.04), T(linea((42, -30), (16, -14)), 5, peso=0.04), T(linea((-26, 30), (0, 38), (26, 30)), 4.4, peso=0.04)]
    ops += [R(elip(0, 34, 12, 6, n=12), (204, 50, 50), peso=0.02, sp=3), punto(-20, -6, 7), punto(20, -6, 7)]
    ops += [T(linea((-30, 6), (-50, 40)), 3.4, peso=0.03), T(linea((30, 6), (50, 40)), 3.4, peso=0.03)]
    return Dib(ops)


@lru_cache(maxsize=None)
def vasija_jomon():
    ops = forma(curva([(-48, -130), (-70, -80), (-50, -20), (-30, 0), (30, 0), (50, -20), (70, -80), (48, -130)], 8), ARCILLA, 5.4, peso=0.6, sp=9)
    ops += forma(pol((-62, -130), (-74, -150), (-40, -136), (-20, -154), (0, -136), (22, -154), (40, -136), (74, -150), (62, -130)), ARCILLA, 4.6, sp=7)
    ops += [T(ondas(-56 + 4 * k, 56 - 4 * k, -100 + 26 * k, 5, 28), 3, peso=0.04) for k in range(4)]
    return Dib(ops)


@lru_cache(maxsize=None)
def tablilla_ley():
    ops = forma(rect(-80, -120, 80, 0, 4), CREMA, 4.6, sp=8)
    ops += [rayita(-56, -96 + 18 * k, 56, -96 + 18 * k, 3) for k in range(6)]
    ops += [R(circ(0, -138, 14, n=12), ROJO_TORII, peso=0.02, sp=3)]
    return Dib(ops)


@lru_cache(maxsize=None)
def arroz_planta(f=0):
    ops = []
    for k in range(7):
        x = -36 + 12 * k
        ops += [T(curva([(x, 0), (x + 2 * math.sin(f * 0.4 + k), -60), (x + 16, -110 - 6 * (k % 3))], 6), 4.4, peso=0.06)]
        ops += [R(elip(x + 14, -108 - 6 * (k % 3), 4, 12, 0.6, 1.0, 8), MIJO, peso=0.02, sp=3)]
    return Dib(ops)


@lru_cache(maxsize=None)
def tren_vapor():
    return locomotora(0)


@lru_cache(maxsize=None)
def nube_petalos(n=8):
    rng = np.random.default_rng(5)
    ops = []
    for k in range(n):
        x, y = rng.uniform(-90, 90), rng.uniform(-90, 90)
        ops += [R(elip(x, y, 10, 6, rng.uniform(0, 3), 1.0, 8), ROSA_FL, peso=0.02, sp=3)]
    return Dib(ops)


@lru_cache(maxsize=None)
def sacerdote(pose=0):
    """Misionero europeo (sotana negra)."""
    return persona((46, 42, 50), PIEL_ROSA, "calvo", "serio", (16, 50), pose, traje="tunica", cuello=BLANCO, acc_d="rollo")
