# -*- coding: utf-8 -*-
"""Objetos de los orígenes a los Han (boceto). Todos son `Dib`; el origen está en la base del objeto."""
import math
from functools import lru_cache

import numpy as np

from obj_base import *  # noqa: F401,F403
from obj_base import _rotar


def colocar(ops, dx=0.0, dy=0.0, s=1.0, rot=0.0, flip=False):
    """Copia las operaciones `ops` (listas de T/R) desplazadas/escaladas/giradas: sirve para componer un Dib con varios."""
    out = []
    for op in ops:
        P = np.asarray(op[1], float) * (-s if flip else s, s)
        if flip:
            P = P * (1, 1)
        if rot:
            P = _rotar(P, rot, 0, 0)
        P = P + (dx, dy)
        out.append((op[0], P) + tuple(op[2:]))
    return out


def ops_de(d):
    return list(d.ops)


# ------------------------------------------------------------------ aldea, agricultura
@lru_cache(maxsize=None)
def casa():
    ops = forma(rect(-62, -72, 62, 0, 4), (206, 170, 120), 5.2, peso=0.5, sp=9)
    ops += forma(pol((-92, -68), (0, -158), (92, -68)), MIJO, 5.5, peso=0.6, sp=8)
    ops += forma(rect(-16, -46, 16, 0, 4), MADERA_OSC, 4, sp=6)
    ops += [rayita(-50 + 14 * k, -88 - 6 * abs(k - 3), -40 + 14 * k, -68, 2.6) for k in range(7)]
    return Dib(ops)


@lru_cache(maxsize=None)
def arrozal():
    """Parcela de arroz inundada con brotes (en boceto)."""
    P = pol((-120, -30), (110, -44), (138, 10), (-96, 26))
    ops = forma(P, (146, 196, 120), 5, peso=0.5, sp=9)
    for i in range(3):
        for k in range(7):
            x, y = -96 + 30 * k + 6 * i, -18 - 6 * k * 0 + 14 * i - 4 * k
            ops += [trazo((x, y + 10), (x - 4, y - 6), w=3.4), trazo((x, y + 10), (x + 5, y - 8), w=3.4)]
    return Dib(ops)


@lru_cache(maxsize=None)
def mijo_planta():
    ops = [T(linea((0, 0), (2, -150)), 4.5, peso=0.05)]
    for k in range(7):
        ops.append(R(elip(5 * (k % 2) - 2, -40 - 16 * k, 8, 13, math.radians(16 * (1 if k % 2 else -1)), 1.0, 10), MIJO, peso=0.03, sp=3))
    ops += [trazo((2, -20), (-30, -44), w=3.6), trazo((2, -30), (34, -58), w=3.6)]
    return Dib(ops)


# ------------------------------------------------------------------ Shang
@lru_cache(maxsize=None)
def ding():
    """Vasija ritual de bronce de tres patas."""
    bronce = (178, 140, 76)
    cuerpo = curva([(-70, -150), (-84, -96), (-70, -56), (0, -40), (70, -56), (84, -96), (70, -150)], 6)
    ops = forma(np.vstack([cuerpo, [(-70, -150)]]), bronce, 5.5, peso=0.8, sp=9)
    ops += forma(elip(0, -152, 72, 14, 0, 1.0, 26), (150, 118, 62), 5, sp=7)
    for lado in (-1, 1):
        ops += forma(pol((lado * 70, -150), (lado * 96, -196), (lado * 110, -190), (lado * 92, -146)), bronce, 4.5, sp=7)
        ops += forma(pol((lado * 56, -56), (lado * 68, 0), (lado * 44, 0), (lado * 40, -50)), bronce, 4.5, sp=7)
    ops += forma(pol((-14, -46), (-18, 0), (18, 0), (14, -46)), bronce, 4.5, sp=7)
    ops += [T(ondas(-56, 56, -116, 6, 28), 3.2, peso=0.08), T(ondas(-56, 56, -92, 6, 28, 1.6), 3.2, peso=0.08)]
    ops += [T(arco_(0, -80, 14, 180, 360, 10), 3.4, peso=0.05)]
    return Dib(ops)


@lru_cache(maxsize=None)
def trono(ancho=1.0):
    mad = (172, 92, 70)
    ops = forma(rect(-74, -230, 74, -96, 10), mad, 5.5, peso=0.7, sp=9)
    ops += forma(rect(-54, -208, 54, -120, 8), (206, 130, 92), 4, sp=8)
    ops += forma(rect(-92, -102, 92, -58, 6), mad, 5.5, peso=0.5, sp=9)
    ops += forma(rect(-84, -58, 84, 0, 4), (142, 70, 56), 5, peso=0.5, sp=9)
    ops += [R(circ(0, -166, 18, n=16), ORO, peso=0.05, sp=5), T(circ(0, -166, 18, n=16), 3.6, peso=0.05)]
    return Dib(ops)


@lru_cache(maxsize=None)
def hueso():
    """Caparazón de tortuga con signos grabados."""
    P = elip(0, 0, 120, 160, 0.0, 1.0, 34)
    ops = forma(P, (224, 204, 156), 6, peso=0.8, sp=9)
    ops += [T(linea((0, -150), (0, 150)), 3.6, peso=0.1), T(linea((-110, -40), (110, -40)), 3.6, peso=0.1), T(linea((-100, 60), (100, 60)), 3.6, peso=0.1)]
    g = [((-60, -100), (-40, -80), (-70, -60)), ((40, -110), (70, -96), (50, -76), (74, -62)), ((-74, -10), (-50, 6), (-66, 20), (-40, 24)),
         ((46, -20), (74, -6), (52, 8)), ((-60, 100), (-36, 118), (-56, 128)), ((40, 96), (62, 110), (44, 126), (68, 132))]
    ops += [T(linea(*q), 3.8, peso=0.06) for q in g]
    return Dib(ops)


@lru_cache(maxsize=None)
def grietas_hueso():
    ops = [T(linea((0, -40), (22, -22), (10, 6), (34, 28), (26, 60)), 4.2, peso=0.1), T(linea((10, 6), (-26, 18), (-40, 46)), 3.6, peso=0.08),
           T(linea((22, -22), (56, -30), (70, -52)), 3.6, peso=0.08), T(linea((-2, -80), (-18, -58), (0, -40)), 3.6, peso=0.06)]
    return Dib(ops)


@lru_cache(maxsize=None)
def llama(f=0):
    f = f % 3
    a = (0, 10, -8)[f]
    b = (0, -12, 8)[f]
    P = curva([(-60, 0), (-70 + a, -70), (-36, -140 + b), (-28, -96), (4, -230 + a * 2), (30, -130), (52, -170 + b), (70, -80), (64, 0)], 6)
    Q = curva([(-30, 0), (-34, -40), (-8, -84 + b), (8, -150 + a), (30, -70), (38, 0)], 6)
    return Dib(forma(np.vstack([P, P[:1]]), NARANJA, 5, peso=0.6, sp=8) + forma(np.vstack([Q, Q[:1]]), AMARILLO, 4, peso=0.4, sp=7))


# ------------------------------------------------------------------ cielo y Zhou
@lru_cache(maxsize=None)
def nube_cielo():
    from boceto import union_circulos
    circ_ = [(-120, -10, 62, 50), (-40, -50, 78, 50), (54, -60, 84, 50), (130, -12, 62, 50)]
    pts, _ = union_circulos(circ_, 50, (0, -20))
    th = np.arctan2(-(pts[:, 1] + 20), pts[:, 0])
    th = np.where(th < -math.pi / 2, th + 2 * math.pi, th)
    pts = pts[np.argsort(th)]
    base = np.stack([np.linspace(pts[-1, 0], pts[0, 0], 18), 50 + 3 * np.sin(np.linspace(0, 9, 18))], 1)
    P = np.vstack([pts, base, pts[:1]])
    return Dib(forma(P, CREMA, 5.5, peso=0.8, sp=11) + [T(arco_(-50, -50, 34, 200, 290, 8), 3.5, peso=0.05)])


@lru_cache(maxsize=None)
def sol_brillo(r=56):
    ops = forma(circ(0, 0, r, n=36), AMARILLO, 5.5, peso=0.4, sp=9)
    for i in range(14):
        a = i * 2 * math.pi / 14
        l0, l1 = r * 1.3, r * (1.8 if i % 2 == 0 else 1.55)
        ops.append(rayita(l0 * math.cos(a), l0 * math.sin(a), l1 * math.cos(a), l1 * math.sin(a), 5))
    return Dib(ops)


@lru_cache(maxsize=None)
def pulgar(arriba=True):
    """Gesto de aprobación / desaprobación dentro de un círculo."""
    ops = forma(circ(0, 0, 84, n=36), CREMA, 5.5, peso=0.6, sp=10)
    s = 1 if arriba else -1
    mano = pol((-34, 10 * s), (-34, 44 * s), (36, 44 * s), (44, 18 * s), (30, 6 * s), (14, 6 * s), (22, -26 * s), (8, -40 * s), (-8, -14 * s), (-18, 10 * s))
    ops += forma(mano, PIEL, 4.6, peso=0.4, sp=8)
    ops += [R(circ(0, 0, 80, n=30), (150, 210, 140) if arriba else (230, 130, 120), peso=0.05, sp=14, ang=25)]
    return Dib(ops)


@lru_cache(maxsize=None)
def rayo():
    P = pol((-20, 0), (30, -150), (4, -150), (52, -300), (-34, -120), (-6, -120), (-50, 0))
    return Dib(forma(P, AMARILLO, 5, peso=0.5, sp=7))


@lru_cache(maxsize=None)
def espadas():
    ops = []
    for s in (-1, 1):
        ang = s * 0.6
        hoja = _rotar(pol((-7, 0), (-7, -150), (0, -172), (7, -150), (7, 0)), ang, 0, 0)
        ops += forma(hoja, GRIS_CL, 4.5, peso=0.3, sp=7)
        guarda = _rotar(pol((-22, 0), (22, 0), (22, 8), (-22, 8)), ang, 0, 0)
        ops += forma(guarda, ORO_OSC, 4, sp=5)
        ops += [T(_rotar(linea((0, 8), (0, 38)), ang, 0, 0), 7, peso=0.04)]
    ops += [T(circ(0, -60, 7, n=10), 3, peso=0.02)]
    return Dib(ops)


# ------------------------------------------------------------------ Qin
@lru_cache(maxsize=None)
def moneda(r=62):
    ops = forma(circ(0, 0, r, n=36), ORO, 5.5, peso=0.6, sp=9)
    ops += [T(circ(0, 0, r * 0.82, n=30), 3.4, peso=0.25)]
    ops += forma(rect(-r * 0.28, -r * 0.28, r * 0.28, r * 0.28, 2), (226, 214, 180), 4.2, sp=5)
    ops += [rayita(-r * 0.55, -r * 0.58, -r * 0.35, -r * 0.4, 3.2), rayita(r * 0.45, r * 0.55, r * 0.6, r * 0.4, 3.2), rayita(r * 0.55, -r * 0.5, r * 0.4, -r * 0.6, 3.2)]
    return Dib(ops)


@lru_cache(maxsize=None)
def rueda():
    """Rueda de carro con eje y regla: los ejes de todos los carros con el mismo ancho."""
    ops = forma(circ(0, -100, 96, n=44), (196, 150, 100), 6, peso=0.8, sp=12)
    ops += [T(circ(0, -100, 70, n=38), 4, peso=0.3)]
    for i in range(8):
        a = i * math.pi / 4
        ops.append(rayita(0, -100, 70 * math.cos(a), -100 + 70 * math.sin(a), 5))
    ops += forma(circ(0, -100, 18, n=16), MADERA_OSC, 4.5, sp=5)
    ops += forma(rect(-170, -92, 170, -74, 3), (220, 190, 110), 4.5, sp=6)        # eje/regla
    ops += [rayita(x, -92, x, -84 if k % 2 else -80, 3) for k, x in enumerate(range(-150, 160, 25))]
    return Dib(ops)


@lru_cache(maxsize=None)
def rollo_escritura(n=1):
    rng = np.random.default_rng(3 + n)
    ops = forma(rect(-110, -70, 110, 70, 10), CREMA, 5.2, peso=0.6, sp=9)
    ops += [R(elip(-110, 0, 18, 72, n=16), MADERA, peso=0.05, sp=5), R(elip(110, 0, 18, 72, n=16), MADERA, peso=0.05, sp=5), T(elip(-110, 0, 18, 72, n=16), 4.5, peso=0.1), T(elip(110, 0, 18, 72, n=16), 4.5, peso=0.1)]
    for i in range(4):
        for j in range(2):
            x0, y0 = -76 + i * 46, -38 + j * 44
            ops.append(T(linea((x0, y0), (x0 + 18 + rng.uniform(-4, 4), y0 + rng.uniform(-6, 6))), 3.6, peso=0.03))
            ops.append(T(linea((x0 + 8, y0 - 8), (x0 + 8 + rng.uniform(-6, 6), y0 + 16)), 3.6, peso=0.03))
            ops.append(T(linea((x0 - 4, y0 + 12), (x0 + 22, y0 + 14)), 3.4, peso=0.03))
    return Dib(ops)


@lru_cache(maxsize=None)
def torre_muralla(s=1.0):
    ops = forma(rect(-56, -130, 56, 0, 4), (186, 174, 154), 5.5, peso=0.6, sp=10)
    ops += forma(rect(-66, -166, 66, -130, 4), (170, 156, 136), 5, peso=0.3, sp=9)
    ops += [R(rect(-62 + 25 * k, -196, -36 + 25 * k, -166, 2), (186, 174, 154), peso=0.03, sp=5) for k in range(5)]
    ops += [T(rect(-62 + 25 * k, -196, -36 + 25 * k, -166, 2), 3.6, peso=0.03) for k in range(5)]
    ops += forma(rect(-16, -78, 16, -34, 10), NEGRO, 4, sp=5)
    ops += [T(linea((-56, -96 + 22 * k), (56, -96 + 22 * k)), 2.6, peso=0.03) for k in range(4)]
    return Dib(ops)


@lru_cache(maxsize=None)
def soldado_barro(pose=0):
    return persona(ARCILLA, (206, 146, 116), "moño", "serio", (12, 20 + 6 * (pose % 2)), pose, traje="armadura", acc_d="lanza")


@lru_cache(maxsize=None)
def foso_guerreros():
    """Fosa del mausoleo: rectángulo hundido."""
    P = rect(-300, -60, 300, 60, 14)
    return Dib(forma(P, (170, 140, 104), 6, peso=0.8, sp=12) + [T(linea((-280, -36), (280, -36)), 3, peso=0.2)])


@lru_cache(maxsize=None)
def calavera_calendario():
    return Dib([])


@lru_cache(maxsize=None)
def arena_reloj():
    """Reloj de arena (los cuatro años)."""
    ops = forma(pol((-60, -190), (60, -190), (8, -100), (60, -10), (-60, -10), (-8, -100)), (236, 226, 198), 5.4, peso=0.6, sp=9)
    ops += forma(pol((-40, -176), (40, -176), (6, -112)), (214, 160, 80), 3.6, sp=5)
    ops += forma(pol((-50, -22), (50, -22), (20, -60), (-20, -60)), (214, 160, 80), 3.6, sp=5)
    ops += [rayita(-70, -198, 70, -198, 7), rayita(-70, -4, 70, -4, 7)]
    return Dib(ops)


# ------------------------------------------------------------------ Han
@lru_cache(maxsize=None)
def puerta(abierta=0.0, candado=False):
    """Puerta monumental: pilares y tejado; las dos hojas giran (abierta 0..1) y detrás aparece la luz del mundo."""
    ops = forma(pol((-150, -212), (-96, -268), (96, -268), (150, -212)), ROJO_OSC, 5.6, peso=0.6, sp=9)
    ops += forma(rect(-126, -214, 126, -186, 4), (196, 150, 100), 5, peso=0.3, sp=8)
    ops += forma(rect(-126, -190, -96, 0, 3), ROJO_CH, 5, peso=0.4, sp=8) + forma(rect(96, -190, 126, 0, 3), ROJO_CH, 5, peso=0.4, sp=8)
    luz = (255, 232, 160) if abierta > 0.15 else (64, 54, 60)
    ops += forma(rect(-96, -188, 96, 0, 2), luz, 4.5, peso=0.3, sp=10)
    if abierta > 0.3:
        ops += [R(circ(0, -110, 26, n=16), AMARILLO, peso=0.02, sp=5)]
    wl = 96 * (1 - 0.86 * abierta)
    for lado in (-1, 1):
        x_ext = lado * 96
        x_int = lado * (96 - wl)
        h_int = 188 - 34 * abierta
        P = pol((x_ext, -186), (x_int, -186 + (188 - h_int) * 0.5), (x_int, -2 - (188 - h_int) * 0.5), (x_ext, -2))
        ops += forma(P, (184, 72, 62), 5, peso=0.3, sp=8)
        if abierta < 0.3:
            ops += [R(circ(x_int - lado * 12, -92, 7, n=10), ORO, peso=0.02, sp=3)]
    if candado:
        ops += forma(rect(-18, -108, 18, -68, 8), ORO, 4.6, peso=0.3, sp=6) + [T(arco_(0, -108, 13, 180, 360, 10), 5.5, peso=0.1)]
    return Dib(ops)


@lru_cache(maxsize=None)
def camello(pose=0):
    p = pose % 2
    cuerpo = forma(elip(0, -140, 100, 44, 0, 1.0, 30), (212, 170, 110), 5.5, peso=0.6, sp=10)
    joroba1 = forma(curva([(-70, -170), (-58, -224), (-20, -214), (-10, -172)], 5), (212, 170, 110), 5, peso=0.3, sp=8, cerrada=True)
    joroba2 = forma(curva([(10, -176), (24, -232), (62, -222), (72, -172)], 5), (212, 170, 110), 5, peso=0.3, sp=8, cerrada=True)
    cuello = forma(curva([(84, -160), (118, -210), (130, -262), (148, -276), (158, -250), (142, -236), (128, -184), (108, -130)], 6), (212, 170, 110), 5.2, peso=0.5, sp=9)
    cabeza = forma(elip(164, -268, 26, 17, -0.3, 1.0, 20), (212, 170, 110), 4.5, sp=7)
    ops = cuerpo + joroba1 + joroba2 + cuello + cabeza + [punto(168, -274, 8), T(linea((150, -290), (146, -304)), 4, peso=0.02)]
    for k, x in enumerate((-66, -34, 40, 72)):
        dx = (10 if (k + p) % 2 else -10)
        ops += forma(pol((x - 10, -108), (x + 10, -108), (x + 6 + dx, 0), (x - 8 + dx, 0)), (196, 150, 96), 4.5, sp=6)
    ops += forma(elip(-96, -150, 10, 26, 0.3, 1.0, 12), (196, 150, 96), 4, sp=5)
    # fardos de seda
    ops += forma(rect(-68, -236, -12, -196, 8), ROJO_CH, 4.2, sp=6) + forma(rect(14, -240, 70, -198, 8), AZUL_IMP, 4.2, sp=6)
    return Dib(ops)


@lru_cache(maxsize=None)
def rollo_seda():
    ops = forma(rect(-70, -56, 70, 0, 6), ROJO_CH, 5, peso=0.5, sp=8) + forma(elip(70, -28, 16, 28, 0, 1.0, 14), (230, 100, 90), 4.4, sp=5)
    ops += [T(ondas(-60, 60, -36, 4, 26), 3, peso=0.05), T(ondas(-60, 60, -18, 4, 26, 1.2), 3, peso=0.05)]
    return Dib(ops)


@lru_cache(maxsize=None)
def papel_hoja():
    ops = forma(pol((-80, -110), (52, -110), (80, -82), (80, 70), (-80, 70)), BLANCO, 5, peso=0.6, sp=9)
    ops += [T(linea((52, -110), (52, -82), (80, -82)), 3.6, peso=0.05)]
    ops += [trazo((-56 + 6 * (k % 2), -62 + 22 * k), (30, -62 + 22 * k + 5 * math.sin(k)), w=3.4) for k in range(5)]
    return Dib(ops)


@lru_cache(maxsize=None)
def mesa_papel():
    ops = forma(rect(-130, -60, 130, -40, 5), MADERA, 5.2, peso=0.3, sp=8)
    ops += [T(linea((-110, -40), (-116, 0)), 6, peso=0.05), T(linea((110, -40), (116, 0)), 6, peso=0.05)]
    return Dib(ops)


@lru_cache(maxsize=None)
def pagoda(niveles=5):
    ops = []
    y = 0.0
    w = 92.0
    for k in range(niveles):
        h = 54
        ops += forma(rect(-w * 0.72, y - h, w * 0.72, y, 3), (214, 176, 134), 4.8, peso=0.3, sp=8)
        ops += forma(pol((-w * 1.15, y - h + 4), (-w * 0.6, y - h - 28), (w * 0.6, y - h - 28), (w * 1.15, y - h + 4)), ROJO_CH if k % 2 == 0 else ROJO_OSC, 5, peso=0.35, sp=8)
        ops += [R(rect(-10, y - 38, 10, y - 4, 3), MADERA_OSC, peso=0.02, sp=4)]
        y -= h + 26
        w *= 0.86
    ops += [T(linea((0, y), (0, y - 50)), 5, peso=0.05), R(circ(0, y - 56, 8, n=10), ORO, peso=0.02, sp=3)]
    return Dib(ops)


@lru_cache(maxsize=None)
def multitud(n=8, seed=1):
    """Grupito de personas diminutas (cabeza + cuerpo) para rebeliones/multitudes."""
    rng = np.random.default_rng(seed)
    ops = []
    cols = [ROJO_CH, AZUL_IMP, JADE, ORO, MORADO, NARANJA]
    for k in range(n):
        x, y = rng.uniform(-110, 110), rng.uniform(-40, 40)
        ops += forma(pol((x - 14, y), (x - 10, y - 50), (x + 10, y - 50), (x + 14, y)), cols[k % len(cols)], 3.6, peso=0.12, sp=5)
        ops += forma(circ(x, y - 64, 14, n=14), PIEL, 3.6, peso=0.1, sp=5)
        ops += [T(linea((x + 10, y - 44), (x + 26, y - 80 - 10 * (k % 2))), 3.4, peso=0.03)]
    return Dib(ops)


@lru_cache(maxsize=None)
def horquilla():
    return Dib([T(linea((0, 0), (0, -190)), 5.5, peso=0.1), T(linea((-22, -190), (-22, -230)), 4.5, peso=0.03), T(linea((0, -190), (0, -240)), 4.5, peso=0.03),
                T(linea((22, -190), (22, -230)), 4.5, peso=0.03), T(linea((-22, -190), (22, -190)), 4.5, peso=0.04)])


@lru_cache(maxsize=None)
def bolsa_dinero():
    ops = forma(curva([(-46, -90), (-68, -40), (-44, 0), (44, 0), (68, -40), (46, -90)], 6), (214, 170, 100), 5, peso=0.5, sp=8)
    ops += [T(linea((-24, -94), (24, -94)), 5, peso=0.04)] + forma(circ(0, -44, 22, n=18), ORO, 4, sp=5) + [T(linea((-8, -44), (8, -44)), 4, peso=0.02)]
    return Dib(ops)


@lru_cache(maxsize=None)
def cetro_corona(tam=1.0):
    ops = forma(pol((-56, 0), (-70, -70), (-34, -40), (0, -96), (34, -40), (70, -70), (56, 0)), ORO, 5.2, peso=0.5, sp=8)
    ops += [R(circ(0, -30, 10, n=10), ROJO_CH, peso=0.02, sp=3), R(circ(-34, -24, 7, n=10), JADE, peso=0.02, sp=3), R(circ(34, -24, 7, n=10), JADE, peso=0.02, sp=3)]
    return Dib(ops)


@lru_cache(maxsize=None)
def signo_pregunta():
    P = np.vstack([arco_(0, -110, 44, 170, 400, 20), [(8, -60), (8, -38)]])
    return Dib([T(P, 14, peso=0.4), T(linea((8, -10), (8.6, -9.4)), 18, peso=0.03)])


@lru_cache(maxsize=None)
def estallido(n=12, r0=40, r1=110):
    """Destello radial (impactos, pólvora, sellos)."""
    ops = []
    for i in range(n):
        a = i * 2 * math.pi / n + 0.12
        l1 = r1 * (1.0 if i % 2 == 0 else 0.68)
        ops.append(T(linea((r0 * math.cos(a), r0 * math.sin(a)), (l1 * math.cos(a), l1 * math.sin(a))), 7, peso=0.04))
    ops += [R(circ(0, 0, r0 * 0.9, n=18), AMARILLO, peso=0.06, sp=7)]
    return Dib(ops)


@lru_cache(maxsize=None)
def estrella5(r=40):
    P = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        P.append((rr * math.cos(a), rr * math.sin(a)))
    return Dib(forma(pol(*P), ORO, 4.4, peso=0.3, sp=6))
