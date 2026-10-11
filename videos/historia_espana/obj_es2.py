# -*- coding: utf-8 -*-
"""Dibujos de boceto para la historia de España (2/4): al-Ándalus, Reconquista, Reyes Católicos y Colón.
Tariq, califa, mezquita de Córdoba (arcos de herradura bicolores), naranjo, caña de azúcar, azulejo, Pelayo, caballeros, el Cid,
reyes de taifas, Alhambra, Boabdil y la llave, Isabel y Fernando, exiliados, Nebrija y su gramática, Colón, la nao Santa María."""
import math
from functools import lru_cache

import numpy as np

import obj_base as OB
import obj_es1  # noqa: F401  (registra sombreros y accesorios)
from obj_a import colocar
from obj_b import caballo
from obj_base import *  # noqa: F401,F403
from obj_es1 import BLANCO_R, CARBON, HIERRO, NEGRO_R, OCRE, PIEL_BRONCE, ROCA, ROCA_OSC

VERDE_IS = (70, 140, 100)
VERDE_CL2 = (150, 196, 130)
ROJO_ARCO = (196, 76, 60)
TERRACOTA = (204, 120, 84)
ALHAMBRA = (214, 140, 100)
NARANJA_F = (244, 150, 50)
AZUL_TEJA = (60, 100, 170)
MORADO_C = (120, 70, 130)
GRANATE = (150, 40, 50)

# ------------------------------------------------------------------ sombreros y accesorios medievales
_orig = OB.sombrero


def _sombrero(nombre, cy=-215.0):
    if nombre == "yelmo":             # yelmo cilíndrico de caballero con rendija y cruz
        ops = forma(pol((-44, cy + 24), (-46, cy - 50), (-30, cy - 66), (30, cy - 66), (46, cy - 50), (44, cy + 24)), HIERRO, 4.8, sp=8)
        ops += forma(rect(-36, cy - 22, 36, cy - 12, 2), NEGRO_R, 3.4, sp=3)
        return ops + [rayita(0, cy - 4, 0, cy + 20, 3.4), rayita(-12, cy + 6, 12, cy + 6, 3.4)]
    if nombre == "nasal":             # casco cónico con nasal y cota de malla (el Cid)
        ops = forma(pol((-50, cy + 30), (-48, cy - 14), (-40, cy - 46), (0, cy - 80), (40, cy - 46), (48, cy - 14), (50, cy + 30), (36, cy + 30),
                        (34, cy - 8), (-34, cy - 8), (-36, cy + 30)), HIERRO, 4.6, sp=8)
        return ops + forma(rect(-5, cy - 22, 5, cy + 14, 2), HIERRO, 3, sp=3)
    if nombre == "corona_real":
        ops = forma(pol((-44, cy - 26), (-46, cy - 70), (-30, cy - 52), (-15, cy - 78), (0, cy - 56), (15, cy - 78), (30, cy - 52), (46, cy - 70), (44, cy - 26)), ORO, 4.6, sp=7)
        return ops + [R(circ(-15, cy - 40, 5, n=10), ROJO_CH, peso=0.02, sp=3), R(circ(15, cy - 40, 5, n=10), (70, 120, 190), peso=0.02, sp=3)]
    if nombre == "toca_reina":        # toca blanca y corona pequeña (Isabel la Católica)
        ops = forma(pol((-50, cy + 40), (-52, cy - 20), (-40, cy - 50), (0, cy - 60), (40, cy - 50), (52, cy - 20), (50, cy + 40), (38, cy + 30), (38, cy - 20),
                        (-38, cy - 20), (-38, cy + 30)), BLANCO_R, 4.4, sp=7)
        ops += forma(pol((-36, cy - 46), (-38, cy - 76), (-22, cy - 62), (0, cy - 84), (22, cy - 62), (38, cy - 76), (36, cy - 46)), ORO, 4.2, sp=6)
        return ops
    if nombre == "kipa":
        return forma(elip(0, cy - 38, 24, 10, 0, 1.0, 16), (70, 80, 130), 3.6, sp=4)
    if nombre == "panuelo_mujer":
        return forma(pol((-50, cy + 30), (-50, cy - 24), (-30, cy - 52), (30, cy - 52), (50, cy - 24), (50, cy + 30), (38, cy + 20), (38, cy - 18), (-38, cy - 18),
                         (-38, cy + 20)), (150, 110, 160), 4.4, sp=7)
    if nombre == "gorro_colon":       # gorro de terciopelo
        return forma(pol((-46, cy - 20), (-50, cy - 50), (-20, cy - 70), (30, cy - 66), (52, cy - 42), (46, cy - 20)), GRANATE, 4.6, sp=7) + \
            [rayita(-46, cy - 26, 46, cy - 26, 3.4)]
    if nombre == "birrete":           # birrete de letrado
        return forma(pol((-44, cy - 30), (-40, cy - 62), (40, cy - 62), (44, cy - 30)), NEGRO_R, 4.4, sp=7) + forma(elip(0, cy - 66, 10, 6, 0, 1.0, 10), NEGRO_R, 3, sp=3)
    return _orig(nombre, cy)


OB.sombrero = _sombrero


def _acc_cimitarra(m, d):
    x, y = m
    return forma(curva([(x - 2, y - 6), (x + 12, y - 60), (x + 40, y - 110), (x + 30, y - 116), (x + 4, y - 74), (x - 10, y - 10)], 6), GRIS_CL, 4, sp=4) + \
        [T(linea((x - 18, y - 8), (x + 14, y - 2)), 5, peso=0.02)]


def _acc_escudo_cruz(m, d):
    x, y = m
    ops = forma(curva([(x - 34, y - 54), (x + 34, y - 54), (x + 34, y - 6), (x, y + 44), (x - 34, y - 6)], 5), BLANCO_R, 4.6, sp=6)
    return ops + forma(pol((x - 6, y - 50), (x + 6, y - 50), (x + 6, y - 22), (x + 30, y - 22), (x + 30, y - 10), (x + 6, y - 10), (x + 6, y + 30), (x - 6, y + 30),
                           (x - 6, y - 10), (x - 30, y - 10), (x - 30, y - 22), (x - 6, y - 22)), ROJO_CH, 3.4, sp=3)


def _acc_escudo_redondo_v(m, d):
    x, y = m
    return forma(elip(x, y, 36, 36, 0, 1.0, 26), VERDE_IS, 4.6, sp=7) + [T(elip(x, y, 24, 24, 0, 1.0, 22), 3, peso=0.03)] + forma(elip(x, y, 8, 8, 0, 1.0, 10), ORO, 3, sp=3)


def _acc_cruz(m, d):
    x, y = m
    return [T(linea((x, y + 20), (x + 2, y - 130)), 5.4, peso=0.06)] + forma(pol((x - 4, y - 150), (x + 6, y - 150), (x + 6, y - 116), (x + 30, y - 116), (x + 30, y - 104),
                                                                                 (x + 6, y - 104), (x + 6, y - 70), (x - 4, y - 70), (x - 4, y - 104), (x - 28, y - 104),
                                                                                 (x - 28, y - 116), (x - 4, y - 116)), ORO, 3.6, sp=3)


def _acc_tizona(m, d):
    x, y = m
    return [T(linea((x, y + 10), (x + 10, y - 150)), 5.4, peso=0.06), R(pol((x - 5, y - 14), (x + 5, y - 156), (x + 15, y - 14)), GRIS_CL, peso=0.04, sp=4),
            T(linea((x - 22, y - 12), (x + 30, y - 16)), 7, peso=0.03)] + forma(elip(x - 2, y + 18, 8, 8, 0, 1.0, 10), ORO, 3, sp=3)


def _acc_llave(m, d):
    x, y = m
    return forma(elip(x, y - 70, 18, 18, 0, 1.0, 16), ORO, 4.4, sp=4) + [T(linea((x, y - 52), (x, y + 30)), 6, peso=0.04),
                                                                       T(linea((x, y + 18), (x + 18, y + 18)), 5, peso=0.02), T(linea((x, y + 30), (x + 14, y + 30)), 5, peso=0.02)]


def _acc_fardo(m, d):
    x, y = m
    return forma(curva([(x - 30, y - 20), (x - 36, y + 26), (x, y + 40), (x + 36, y + 26), (x + 30, y - 20), (x, y - 30)], 6), (180, 150, 110), 4.4, sp=6) + \
        [T(linea((x - 10, y - 30), (x + 10, y - 30)), 4, peso=0.02)]


def _acc_libro_g(m, d):
    x, y = m
    return forma(rect(x - 30, y - 50, x + 30, y + 26, 4), (150, 60, 50), 4.4, sp=5) + forma(rect(x - 22, y - 38, x + 22, y - 18, 2), ORO, 3, sp=3)


def _acc_catalejo(m, d):
    x, y = m
    return forma(pol((x - 10, y - 4), (x + 60, y - 50), (x + 68, y - 38), (x - 2, y + 8)), (176, 126, 70), 4.2, sp=4) + [T(linea((x + 30, y - 26), (x + 38, y - 14)), 3, peso=0.02)]


def _acc_estandarte_castilla(m, d):
    x, y = m
    ops = [T(linea((x, y + 60), (x + 4, y - 190)), 5, peso=0.12)]
    ops += forma(pol((x + 4, y - 188), (x + 104, y - 188), (x + 104, y - 108), (x + 4, y - 108)), BLANCO_R, 4, sp=6)
    for (dx, dy, c) in ((0, 0, ROJO_CH), (50, 40, MORADO_C), (50, 0, BLANCO_R), (0, 40, BLANCO_R)):
        ops += [R(rect(x + 6 + dx, y - 186 + dy, x + 54 + dx, y - 150 + dy, 1), c, peso=0.02, sp=4)]
    return ops


OB.ACC.update({"cimitarra": _acc_cimitarra, "escudo_cruz": _acc_escudo_cruz, "escudo_v": _acc_escudo_redondo_v, "cruz": _acc_cruz, "tizona": _acc_tizona,
               "llave": _acc_llave, "fardo": _acc_fardo, "libro_g": _acc_libro_g, "catalejo": _acc_catalejo, "estandarte": _acc_estandarte_castilla})


# ------------------------------------------------------------------ al-Ándalus
@lru_cache(maxsize=None)
def tariq(pose=0, cara="serio"):
    return persona((70, 110, 90), PIEL_BRONCE, "turbante", cara, (16, 60), pose, traje="armadura", faja=ORO, barba=(130, 100, 80), acc_d="cimitarra", acc_i="escudo_v")


@lru_cache(maxsize=None)
def soldado_omeya(pose=0, cara="enojo", color=(80, 120, 100)):
    return persona(color, PIEL_BRONCE, "turbante", cara, (16, 40), pose, traje="corta", faja=(200, 170, 100), acc_d="lanza", acc_i="escudo_v")


@lru_cache(maxsize=None)
def califa(pose=0, cara="feliz"):
    return persona((236, 230, 214), PIEL_BRONCE, "turbante_verde", cara, (16, 50), pose, traje="tunica", faja=VERDE_IS, cuello=ORO, barba=(140, 110, 90), acc_d="cetro")


@lru_cache(maxsize=None)
def sabio_andalusi(pose=0):
    return persona((120, 110, 170), PIEL_BRONCE, "turbante", "feliz", (16, 70), pose, traje="tunica", faja=ORO, barba=(200, 196, 190), acc_d="libro_g")


@lru_cache(maxsize=None)
def mezquita(arcos=4):
    """Mezquita de Córdoba: columnas y arcos de herradura de dovelas rojas y blancas, en dos alturas."""
    ops = []
    w = 92
    x0 = -arcos * w / 2
    ops += forma(rect(x0 - 10, -268, x0 + arcos * w + 10, -246, 3), ALHAMBRA, 4.6, sp=7)
    ops += forma(rect(x0 - 6, -246, x0 + arcos * w + 6, -150, 2), (236, 220, 190), 4.4, peso=0.3, sp=9)
    for k in range(arcos + 1):
        x = x0 + k * w
        ops += forma(rect(x - 9, -150, x + 9, -6, 3), (210, 196, 170), 4, sp=4)
        ops += forma(rect(x - 14, -12, x + 14, 0, 2), ROCA, 3.4, sp=3)
        ops += forma(rect(x - 14, -158, x + 14, -146, 2), ROCA, 3.4, sp=3)
    for k in range(arcos):
        cx = x0 + k * w + w / 2
        for nivel, (cy, r) in enumerate(((-120, 38), (-200, 34))):
            for j in range(10):                                                     # dovelas alternas
                a0 = math.radians(196 + j * 14.8)
                a1 = math.radians(196 + (j + 1) * 14.8)
                pts = [(cx + r * math.cos(a0), cy + r * math.sin(a0)), (cx + (r + 18) * math.cos(a0), cy + (r + 18) * math.sin(a0)),
                       (cx + (r + 18) * math.cos(a1), cy + (r + 18) * math.sin(a1)), (cx + r * math.cos(a1), cy + r * math.sin(a1))]
                ops += [R(pol(*pts), ROJO_ARCO if j % 2 == 0 else BLANCO_R, peso=0.01, sp=3)]
            ops += [T(arco_(cx, cy, r + 18, 196, 344, 16), 3.6, peso=0.03), T(arco_(cx, cy, r, 196, 344, 16), 3.2, peso=0.03)]
    return Dib(ops)


@lru_cache(maxsize=None)
def naranjo(f=0):
    ops = forma(pol((-10, 0), (-8, -90), (8, -90), (12, 0)), (130, 90, 60), 4.4, sp=5)
    ops += forma(curva([(-80, -100), (-90, -150), (-50, -196), (0, -210), (56, -192), (88, -150), (80, -100), (40, -84), (-40, -84)], 7), (90, 150, 80), 5.2, peso=0.5, sp=9)
    for k, (x, y) in enumerate(((-50, -130), (-10, -170), (30, -130), (56, -160), (-36, -170), (10, -110), (60, -110))):
        ops += forma(elip(x, y + 3 * math.sin(f + k), 13, 13, 0, 1.0, 14), NARANJA_F, 3.4, sp=4)
    return Dib(ops)


@lru_cache(maxsize=None)
def cana_azucar():
    ops = []
    for k, (x, h) in enumerate(((-30, 210), (0, 240), (30, 200))):
        ops += forma(rect(x - 7, -h, x + 7, 0, 3), (170, 190, 110), 3.8, sp=4)
        ops += [rayita(x - 8, -h + 40 * j, x + 8, -h + 40 * j, 2.6) for j in range(1, h // 40)]
        ops += forma(curva([(x, -h), (x + 30 * (1 if k % 2 else -1), -h - 30), (x + 50 * (1 if k % 2 else -1), -h - 20)], 4).tolist() + [(x + 6, -h + 10)], VERDE, 3.4, sp=4)
    return Dib(ops)


@lru_cache(maxsize=None)
def azulejo():
    ops = forma(rect(-80, -160, 80, 0, 4), BLANCO_R, 5, sp=8)
    ops += forma(pol((0, -150), (70, -80), (0, -10), (-70, -80)), AZUL_TEJA, 4, sp=5)
    ops += forma(elip(0, -80, 28, 28, 0, 1.0, 20), (240, 200, 80), 3.6, sp=4)
    for cx, cy in ((-66, -146), (66, -146), (-66, -14), (66, -14)):
        ops += [R(circ(cx, cy, 10, n=10), (60, 150, 110), peso=0.01, sp=3)]
    return Dib(ops)


@lru_cache(maxsize=None)
def noria(f=0):
    """Noria de riego: rueda con cangilones (agricultura andalusí)."""
    ops = []
    r = 110
    ops += [T(circ(0, -130, r, n=60), 6, peso=0.3), T(circ(0, -130, r - 22, n=50), 4, peso=0.2)]
    for k in range(8):
        a = f * 0.5 + k * math.pi / 4
        ops += [T(linea((0, -130), (r * math.cos(a), -130 + r * math.sin(a))), 4, peso=0.03)]
        ops += forma(rect(r * math.cos(a) - 12, -130 + r * math.sin(a) - 10, r * math.cos(a) + 12, -130 + r * math.sin(a) + 10, 3), TERRACOTA, 3.4, sp=3)
    ops += forma(elip(0, -130, 14, 14, 0, 1.0, 12), (130, 90, 60), 3.6, sp=4)
    ops += forma(pol((-130, 0), (-120, -30), (120, -30), (130, 0)), (140, 190, 210), 4, sp=6)
    return Dib(ops)


# ------------------------------------------------------------------ Reconquista
@lru_cache(maxsize=None)
def pelayo(pose=0, cara="serio"):
    return persona((110, 90, 150), PIEL_ROSA, "pelo_castano", cara, (16, 120), pose, traje="armadura", faja=(150, 110, 70), barba=(110, 76, 50), acc_d="cruz")


def _pata(x0, y0, a1, a2, col, l1=58, l2=56, w1=17, w2=11):
    """Pata de caballo en dos tramos (muslo y caña) con casco oscuro; ángulos en grados desde la vertical (positivo = hacia delante)."""
    r1, r2 = math.radians(a1), math.radians(a2)
    kx, ky = x0 + l1 * math.sin(r1), y0 + l1 * math.cos(r1)
    fx, fy = kx + l2 * math.sin(r2), ky + l2 * math.cos(r2)
    def seg(ax, ay, bx, by, wa, wb):
        dx, dy = bx - ax, by - ay
        n = math.hypot(dx, dy) + 1e-6
        nx, ny = -dy / n, dx / n
        return [(ax + nx * wa, ay + ny * wa), (bx + nx * wb, by + ny * wb), (bx - nx * wb, by - ny * wb), (ax - nx * wa, ay - ny * wa)]
    ops = forma(seg(x0, y0, kx, ky, w1, w2 * 1.1), col, 4.4, sp=6) + forma(seg(kx, ky, fx, fy, w2, w2 * 0.85), col, 4.2, sp=5)
    ops += forma(pol((fx - 12, fy - 6), (fx + 13, fy - 6), (fx + 15, fy + 8), (fx - 13, fy + 8)), NEGRO_R, 3.4, sp=3)
    return ops


# ciclo de paso/galope: (muslo, caña) de las patas trasera lejana, trasera cercana, delantera lejana, delantera cercana
_PASOS = [((-24, 4), (18, -2), (34, 20), (-8, -30)), ((-8, -24), (30, 6), (8, -28), (26, 10)),
          ((20, -6), (-24, 4), (-12, -30), (34, 20)), ((30, 6), (-8, -24), (26, 10), (8, -28))]


@lru_cache(maxsize=None)
def caballo2(pose=0, col=(150, 100, 66), crin=(70, 50, 40)):
    """Caballo de perfil (hacia la derecha) con 4 poses de galope: cuello, cabeza, crin, cola y patas articuladas."""
    p = _PASOS[pose % 4]
    osc = tuple(int(c * 0.82) for c in col)
    ops = []
    for (x, y), (a1, a2), lejos in zip(((-76, -112), (-94, -112), (70, -112), (88, -112)), p, (True, False, True, False)):
        if lejos:
            ops += _pata(x, y, a1, a2, osc)
    ops += forma(curva([(-104, -142), (-130, -150), (-160, -126), (-170, -90), (-150, -100), (-140, -126)], 5), crin, 4.4, sp=5)           # cola
    ops += forma(elip(-4, -138, 112, 44, 0.0, 1.0, 36), col, 5.8, peso=0.6, sp=10)                                                       # cuerpo
    cuello = [(58, -166), (88, -206), (116, -244), (146, -262), (170, -250), (190, -214), (186, -196), (166, -200), (146, -214), (126, -186), (104, -128)]
    ops += forma(curva(cuello, 6), col, 5.4, peso=0.4, sp=8)
    ops += forma(curva([(110, -236), (88, -214), (66, -180), (54, -160), (76, -170), (100, -200), (124, -236)], 5), crin, 4, sp=5)        # crin
    ops += forma(pol((140, -258), (146, -286), (156, -260)), col, 3.6, sp=3)                                                            # oreja
    ops += [punto(158, -236, 8), punto(184, -206, 5)]
    for (x, y), (a1, a2), lejos in zip(((-76, -112), (-94, -112), (70, -112), (88, -112)), p, (True, False, True, False)):
        if not lejos:
            ops += _pata(x, y, a1, a2, col)
    ops += [T(curva([(30, -170), (40, -150), (36, -120)], 4), 3, peso=0.03, v=170)]
    return Dib(ops)


def _montado(h, r, dx=4, dy=-118, s=0.6, color=None):
    ops = list(h.ops) + colocar(list(r.ops), dx, dy, s)
    if color is not None:
        ops += forma(curva([(-70, -176), (-56, -116), (44, -112), (66, -176), (0, -188)], 5), color, 4.2, sp=6)          # gualdrapa
    return ops


@lru_cache(maxsize=None)
def caballero(pose=0, color=(150, 80, 150), lanza=True):
    """Caballero cristiano a caballo con yelmo, escudo con cruz y lanza."""
    r = persona(color, PIEL_ROSA, "yelmo", "serio", (40, 70), pose, traje="armadura", faja=ORO, acc_i="escudo_cruz", acc_d="lanza" if lanza else "espada")
    return Dib(_montado(caballo2(pose), r, color=color))


@lru_cache(maxsize=None)
def cid(pose=0):
    """El Cid sobre Babieca (blanco), con la Tizona en alto."""
    r = persona((200, 60, 50), PIEL_ROSA, "nasal", "serio", (40, 150), pose, traje="armadura", faja=ORO, barba=(150, 110, 80), acc_d="tizona", acc_i="escudo_cruz")
    return Dib(_montado(caballo2(pose, (236, 232, 222), (170, 160, 150)), r, color=(200, 60, 50)))


@lru_cache(maxsize=None)
def jinete_moro(pose=0, color=(80, 130, 100)):
    r = persona(color, PIEL_BRONCE, "turbante", "enojo", (40, 60), pose, traje="armadura", faja=ORO, barba=(120, 90, 70), acc_d="cimitarra", acc_i="escudo_v")
    return Dib(_montado(caballo2(pose, (110, 80, 60)), r, color=color))


@lru_cache(maxsize=None)
def rey_cristiano(pose=0, cara="serio", color=(150, 60, 120)):
    return persona(color, PIEL_ROSA, "corona_real", cara, (16, 44), pose, traje="tunica", faja=ORO, cuello=BLANCO_R, barba=(140, 100, 70), acc_d="espada")


@lru_cache(maxsize=None)
def rey_taifa(pose=0, cara="enojo", color=(80, 130, 100)):
    return persona(color, PIEL_BRONCE, "turbante", cara, (40, 60), pose, traje="tunica", faja=ORO, barba=(140, 104, 80), acc_d="cimitarra")


@lru_cache(maxsize=None)
def castillo():
    """Castillo de tres torres (Castilla)."""
    ops = forma(rect(-120, -150, 120, 0, 3), (226, 200, 150), 5.2, peso=0.5, sp=9)
    for x0, x1, top in ((-130, -70, -230), (-36, 36, -290), (70, 130, -230)):
        ops += forma(rect(x0, top, x1, 0, 3), (214, 186, 136), 5, peso=0.3, sp=8)
        w = (x1 - x0) / 5
        for j in (0, 2, 4):
            ops += forma(rect(x0 + j * w, top - 26, x0 + (j + 1) * w, top, 2), (214, 186, 136), 4, sp=4)
        ops += forma(rect((x0 + x1) / 2 - 8, top + 40, (x0 + x1) / 2 + 8, top + 76, 3), NEGRO_R, 3.4, sp=3)
    ops += forma(curva([(-30, 0), (-30, -60), (0, -86), (30, -60), (30, 0)], 5), (110, 76, 56), 4.4, sp=5)
    ops += [T(linea((-120, -150 + 24 * k), (120, -150 + 24 * k)), 2.4, peso=0.03, v=150) for k in range(1, 6)]
    return Dib(ops)


@lru_cache(maxsize=None)
def alhambra():
    """La Alhambra sobre su colina: murallas rojizas, torres (Comares y la Vela) y Sierra Nevada nevada detrás."""
    ops = forma(pol((-260, 0), (-230, -150), (-160, -210), (-90, -170), (-10, -250), (70, -196), (150, -240), (240, -150), (270, 0)), (200, 206, 220), 4.4, sp=9)
    ops += forma(pol((-120, -190), (-90, -170), (-10, -250), (70, -196), (100, -210), (60, -230), (-10, -270), (-70, -210)), BLANCO_R, 3.6, sp=6)
    ops += forma(curva([(-280, 0), (-240, -70), (-120, -100), (80, -104), (220, -80), (280, 0)], 6), (150, 170, 100), 5, peso=0.4, sp=10)       # colina
    ops += forma(rect(-210, -150, 200, -86, 3), ALHAMBRA, 5, peso=0.4, sp=9)                                                                    # muralla
    for x0, x1, top in ((-200, -140, -210), (-40, 30, -230), (120, 176, -196), (-110, -70, -180)):
        ops += forma(rect(x0, top, x1, -100, 3), ALHAMBRA, 4.6, sp=7)
        w = (x1 - x0) / 5
        for j in (0, 2, 4):
            ops += forma(rect(x0 + j * w, top - 16, x0 + (j + 1) * w, top, 2), ALHAMBRA, 3.6, sp=3)
        ops += forma(curva([((x0 + x1) / 2 - 7, top + 50), ((x0 + x1) / 2 - 7, top + 32), ((x0 + x1) / 2, top + 24), ((x0 + x1) / 2 + 7, top + 32),
                            ((x0 + x1) / 2 + 7, top + 50)], 4), NEGRO_R, 3, sp=3)
    for k in range(6):
        x = -220 + 80 * k
        ops += forma(pol((x - 8, -86), (x - 4, -130), (x + 4, -130), (x + 8, -86)), (60, 110, 70), 3.4, sp=3)              # cipreses
        ops += forma(elip(x, -140, 10, 22, 0, 1.0, 12), (60, 110, 70), 3.4, sp=3)
    return Dib(ops)


@lru_cache(maxsize=None)
def boabdil(pose=0, cara="lloron"):
    return persona((70, 120, 90), PIEL_BRONCE, "turbante", cara, (16, 70), pose, traje="tunica", faja=ORO, barba=(130, 100, 80), acc_d="llave")


# ------------------------------------------------------------------ Reyes Católicos
@lru_cache(maxsize=None)
def isabel(pose=0, cara="serio"):
    return persona((150, 40, 60), PIEL_ROSA, "toca_reina", cara, (16, 46), pose, traje="vestido", faja=ORO, cuello=ORO, acc_d="cetro")


@lru_cache(maxsize=None)
def fernando(pose=0, cara="serio"):
    return persona((200, 150, 60), PIEL_ROSA, "corona_real", cara, (16, 50), pose, traje="tunica", faja=ROJO_CH, cuello=NEGRO_R, acc_d="espada")


@lru_cache(maxsize=None)
def anillos():
    ops = forma(elip(-26, -70, 44, 44, 0, 1.0, 30), ORO, 6, sp=5) + [T(elip(-26, -70, 30, 30, 0, 1.0, 26), 4, peso=0.03)]
    ops += forma(elip(26, -70, 44, 44, 0, 1.0, 30), ORO, 6, sp=5) + [T(elip(26, -70, 30, 30, 0, 1.0, 26), 4, peso=0.03)]
    ops += forma(pol((-10, -126), (0, -140), (10, -126), (0, -112)), (180, 220, 240), 3.4, sp=3)
    return Dib(ops)


@lru_cache(maxsize=None)
def yugo_flechas():
    """Divisa de los Reyes Católicos: el haz de flechas (de Fernando) atado, cruzado por el yugo (de Isabel) con sus dos colleras."""
    ops = []
    for k in range(5):                                                                     # flechas en abanico, atadas abajo
        a = math.radians(-90 + (k - 2) * 13)
        x0, y0 = -70 * math.cos(a), -40 - 70 * math.sin(a)
        x1, y1 = 190 * math.cos(a), -40 + 190 * math.sin(a)
        ops += [T(linea((x0, y0 + 10), (x1, y1)), 5, peso=0.04)]
        ops += forma(pol((x1 + 18 * math.cos(a), y1 + 18 * math.sin(a)), (x1 + 10 * math.sin(a), y1 - 10 * math.cos(a)), (x1 - 10 * math.sin(a), y1 + 10 * math.cos(a))),
                     GRIS_CL, 3.4, sp=3)
        ops += forma(pol((x0, y0 + 10), (x0 - 10, y0 + 30), (x0 + 10, y0 + 30)), ROJO_CH, 3, sp=3)
    ops += forma(rect(-16, -66, 16, -40, 4), ROJO_CH, 3.6, sp=3)                         # lazo
    ops += forma(curva([(-170, -150), (-90, -166), (0, -158), (90, -166), (170, -150), (170, -128), (90, -142), (0, -134), (-90, -142), (-170, -128)], 5),
                 (176, 120, 66), 5, peso=0.3, sp=7)                                        # yugo
    for cx in (-96, 96):                                                                   # colleras
        ops += [T(arco_(cx, -140, 34, 10, 170, 14), 6, peso=0.05)]
    return Dib(ops)


@lru_cache(maxsize=None)
def exiliado(pose=0, mujer=False):
    if mujer:
        return persona((120, 100, 150), PIEL_ROSA, "panuelo_mujer", "lloron", (14, 20), pose, traje="vestido", acc_d="fardo")
    return persona((90, 90, 120), PIEL_ROSA, "kipa", "lloron", (14, 20), pose, traje="tunica", barba=(170, 160, 150), acc_d="fardo")


@lru_cache(maxsize=None)
def nebrija(pose=0):
    return persona(NEGRO_R, PIEL_ROSA, "birrete", "feliz", (16, 80), pose, traje="tunica", cuello=BLANCO_R, acc_d="libro_g")


@lru_cache(maxsize=None)
def gramatica():
    ops = forma(rect(-110, -260, 110, 0, 8), (150, 60, 50), 5.4, peso=0.5, sp=9)
    ops += forma(rect(-92, -244, 92, -16, 6), (170, 76, 62), 3.6, sp=8)
    ops += forma(rect(-70, -210, 70, -150, 4), (240, 226, 190), 4, sp=6)
    ops += [rayita(-56, -194 + 16 * k, 56, -194 + 16 * k, 2.8) for k in range(3)]
    ops += forma(elip(0, -90, 30, 30, 0, 1.0, 20), ORO, 4, sp=4)
    return Dib(ops)


# ------------------------------------------------------------------ Colón
@lru_cache(maxsize=None)
def colon(pose=0, cara="feliz"):
    return persona((60, 80, 120), PIEL_ROSA, "gorro_colon", cara, (16, 120), pose, traje="tunica", faja=ORO, cuello=BLANCO_R, acc_d="catalejo", pelo_largo=(200, 196, 190))


@lru_cache(maxsize=None)
def marinero(pose=0, cara="feliz"):
    return persona((150, 120, 90), PIEL_ROSA, "pelo_castano", cara, (16, 130), pose, traje="corta", faja=(120, 60, 50))


@lru_cache(maxsize=None)
def nao(f=0, tam=1.0, cruz=True):
    """Nao (la Santa María): casco alto con castillos, tres palos, velas cuadradas con la cruz roja."""
    ops = forma(curva([(-170, -90), (-150, -20), (-60, 8), (90, 8), (160, -30), (196, -96), (150, -84), (110, -70), (-100, -70), (-130, -110)], 6),
                (150, 100, 66), 5.6, peso=0.6, sp=10)
    ops += forma(rect(-170, -130, -100, -84, 3), (166, 112, 72), 4.6, sp=6) + forma(rect(110, -112, 168, -80, 3), (166, 112, 72), 4.6, sp=6)
    ops += [T(linea((-150, -40), (150, -40)), 3.2, peso=0.04)]
    for k in range(6):
        ops += forma(elip(-100 + 36 * k, -46, 6, 6, 0, 1.0, 10), NEGRO_R, 2.6, sp=2)
    for x, h, w in ((-20, 300, 80), (-110, 220, 50), (80, 230, 56)):
        ops += [T(linea((x, -70), (x, -70 - h)), 5.4, peso=0.12)]
        sw = 6 * math.sin(f * 1.4 + x)
        vela = [(x - w, -70 - h * 0.88), (x + w, -70 - h * 0.88), (x + w * 0.92 + sw, -70 - h * 0.30), (x - w * 0.92 + sw, -70 - h * 0.30)]
        ops += forma(curva(vela + [vela[0]], 4), BLANCO_R, 4.6, peso=0.3, sp=8)
        if cruz and w > 60:
            cy = -70 - h * 0.6
            ops += forma(pol((x - 8, cy - 40), (x + 8, cy - 40), (x + 8, cy - 8), (x + 34, cy - 8), (x + 34, cy + 8), (x + 8, cy + 8), (x + 8, cy + 36), (x - 8, cy + 36),
                             (x - 8, cy + 8), (x - 34, cy + 8), (x - 34, cy - 8), (x - 8, cy - 8)), ROJO_CH, 3.2, sp=3)
    ops += forma(pol((-20, -370), (30, -360), (-20, -350)), ROJO_CH, 3.2, sp=3)
    return Dib(colocar(ops, 0, 0, tam) if tam != 1.0 else ops)


@lru_cache(maxsize=None)
def isla_palmera(f=0):
    ops = forma(curva([(-150, 0), (-120, -36), (-40, -56), (60, -50), (140, -26), (160, 0)], 6), (238, 214, 150), 5, peso=0.4, sp=9)
    ops += forma(curva([(10, -50), (18, -130), (34, -210), (46, -250)], 5).tolist() + [(56, -246), (44, -200), (30, -130), (26, -50)], (150, 110, 70), 4.4, sp=5)
    for k in range(5):
        a = math.radians(-160 + 36 * k) + 0.06 * math.sin(f + k)
        ops += forma(curva([(46, -250), (46 + 60 * math.cos(a), -250 + 40 * math.sin(a) - 20), (46 + 110 * math.cos(a), -250 + 70 * math.sin(a) + 20)], 5).tolist() +
                     [(46 + 60 * math.cos(a), -250 + 40 * math.sin(a))], (90, 160, 80), 3.6, sp=4)
    return Dib(ops)


@lru_cache(maxsize=None)
def taino(pose=0, cara="asombro"):
    return persona((196, 150, 90), (200, 140, 100), "pelo_negro", cara, (16, 30), pose, traje="corta", faja=(220, 80, 60), pelo_largo=(60, 50, 50))


@lru_cache(maxsize=None)
def balanza(incl=0.0):
    """Balanza de dos platillos; incl (rad) inclina el brazo (positivo = baja el platillo izquierdo)."""
    ops = forma(pol((-60, 0), (60, 0), (40, -24), (-40, -24)), (150, 110, 70), 4.6, sp=6)
    ops += forma(rect(-8, -250, 8, -24, 3), (170, 126, 80), 4.4, sp=4)
    c, s = math.cos(incl), math.sin(incl)
    L = 170
    xa, ya = -L * c, -250 + L * s
    xb, yb = L * c, -250 - L * s
    ops += [T(linea((xa, ya), (xb, yb)), 7, peso=0.05)] + forma(elip(0, -250, 14, 14, 0, 1.0, 12), ORO, 3.6, sp=3)
    for (x, y, col) in ((xa, ya, (150, 80, 150)), (xb, yb, VERDE_IS)):
        ops += [T(linea((x, y), (x - 50, y + 90)), 3, peso=0.02), T(linea((x, y), (x + 50, y + 90)), 3, peso=0.02)]
        ops += forma(curva([(x - 64, y + 90), (x - 40, y + 116), (x + 40, y + 116), (x + 64, y + 90)], 5).tolist() + [(x - 64, y + 90)], (200, 170, 110), 4.4, sp=5)
        ops += forma(elip(x, y + 70, 30, 22, 0, 1.0, 16), col, 3.6, sp=4)
    return Dib(ops)
