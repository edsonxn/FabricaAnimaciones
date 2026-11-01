# -*- coding: utf-8 -*-
"""Objetos de los Sui/Tang a los Ming (boceto)."""
import math
from functools import lru_cache

import numpy as np

from obj_a import colocar
from obj_base import *  # noqa: F401,F403
from obj_base import _rotar


# ------------------------------------------------------------------ Gran Canal y Tang
@lru_cache(maxsize=None)
def barca_arroz(f=0):
    ops = forma(curva([(-100, -40), (-74, 0), (0, 12), (74, 0), (100, -40)], 6), MADERA, 5.5, peso=0.5, sp=9)
    for k in range(3):
        x = -52 + 52 * k
        ops += forma(curva([(x - 26, -38), (x - 30, -80), (x, -96), (x + 30, -80), (x + 26, -38)], 5), (232, 222, 196), 4.6, peso=0.3, sp=7)
        ops.append(T(linea((x - 12, -96), (x + 12, -96)), 4, peso=0.03))
    ops += [T(linea((60, -40), (84, -110)), 5, peso=0.05)]
    return Dib(ops)


@lru_cache(maxsize=None)
def poeta(pose=0):
    return persona((100, 150, 180), PIEL, "letrado", "feliz", (14, 70), pose, barba=None, bigote=True, acc_d="copa", acc_i="pincel", faja=ORO)


@lru_cache(maxsize=None)
def bailarina(pose=0):
    p = pose % 3
    ang = ((50, 150), (130, 40), (80, 110))[p]
    d = persona(ROSA, PIEL, None, "feliz", ang, pose, traje="vestido", pelo_largo=NEGRO, faja=ORO_OSC)
    hx, hy = d.manos[1] if p != 1 else d.manos[0]
    s = 1 if p != 1 else -1
    cinta = colocar([("t", curva([(0, 0), (s * 46, -38 + 16 * p), (s * 96, 10), (s * 150, -36 + 10 * p), (s * 196, -6)], 8))], hx, hy)[0][1]
    return Dib(list(d.ops) + [T(cinta, 6.5, peso=0.3)])


@lru_cache(maxsize=None)
def alquimista(pose=0):
    return persona(AZUL_OSC, PIEL, "letrado", "asombro" if pose else "feliz", (30, 130), pose, barba=(236, 236, 240), acc_d="frasco", faja=MORADO)


@lru_cache(maxsize=None)
def frasco_burbujas(f=0):
    ops = forma(elip(0, -60, 70, 66, 0, 1.0, 26), CELESTE, 5.4, peso=0.6, sp=9) + forma(rect(-22, -190, 22, -110, 4), CELESTE, 5, peso=0.3, sp=7)
    ops += [R(elip(0, -36, 58, 38, n=20), (150, 220, 120), peso=0.04, sp=5)]
    for k in range(4):
        ph = (k * 0.7 + f * 0.6)
        ops.append(T(circ(-22 + 14 * k, -60 - 26 * ((ph % 1.0)), 6 + 2 * (k % 2), n=10), 3.2, peso=0.02))
    return Dib(ops)


@lru_cache(maxsize=None)
def cohete():
    ops = forma(rect(-16, -150, 16, 0, 4), ROJO_CH, 5, peso=0.4, sp=8) + forma(pol((-16, -150), (0, -196), (16, -150)), ORO, 4.6, sp=6)
    ops += [T(linea((0, 0), (0, 40)), 3.6, peso=0.03)]
    return Dib(ops)


@lru_cache(maxsize=None)
def chispas(n=14, r=140):
    rng = np.random.default_rng(5)
    ops = []
    cols = [ROJO_CH, ORO, AZUL, VERDE, NARANJA, ROSA]
    for i in range(n):
        a = i * 2 * math.pi / n + rng.uniform(-0.1, 0.1)
        l0, l1 = r * rng.uniform(0.35, 0.55), r * rng.uniform(0.85, 1.05)
        ops.append(T(linea((l0 * math.cos(a), l0 * math.sin(a)), (l1 * math.cos(a), l1 * math.sin(a))), 6, peso=0.05))
        ops.append(R(circ(l1 * math.cos(a), l1 * math.sin(a), 9, n=10), cols[i % len(cols)], peso=0.02, sp=3))
    return Dib(ops)


# ------------------------------------------------------------------ Song
@lru_cache(maxsize=None)
def billete():
    ops = forma(rect(-110, -62, 110, 62, 6), (206, 222, 170), 5.2, peso=0.6, sp=9)
    ops += [T(rect(-96, -50, 96, 50, 4), 3.2, peso=0.2)]
    ops += forma(circ(0, 0, 30, n=20), (232, 240, 200), 3.6, sp=5)
    ops += [T(linea((-18, 0), (18, 0)), 3.6, peso=0.02), T(linea((0, -18), (0, 18)), 3.6, peso=0.02)]
    ops += [rayita(-84, -34, -50, -34, 3), rayita(50, 34, 84, 34, 3), rayita(-84, 34, -62, 34, 3), rayita(62, -34, 84, -34, 3)]
    return Dib(ops)


@lru_cache(maxsize=None)
def tipo_movil():
    ops = forma(rect(-40, -120, 40, 0, 4), MADERA, 5, peso=0.4, sp=8)
    ops += [T(linea((-18, -96), (18, -96)), 5, peso=0.03), T(linea((0, -96), (0, -40)), 5, peso=0.03), T(linea((-16, -56), (16, -56)), 4.6, peso=0.02)]
    return Dib(ops)


@lru_cache(maxsize=None)
def brujula(aguja=0.0):
    """aguja = ángulo en radianes (0 = apunta arriba)."""
    ops = forma(circ(0, 0, 92, n=40), ORO, 6, peso=0.7, sp=10) + forma(circ(0, 0, 76, n=36), CREMA, 4.6, peso=0.4, sp=9)
    for i in range(12):
        a = i * math.pi / 6
        ops.append(rayita(66 * math.cos(a), 66 * math.sin(a), 76 * math.cos(a) * 0.97, 76 * math.sin(a) * 0.97, 3.2))
    n = _rotar(pol((-9, 0), (0, -66), (9, 0)), aguja, 0, 0)
    s = _rotar(pol((-9, 0), (0, 58), (9, 0)), aguja, 0, 0)
    ops += forma(n, ROJO_CH, 3.8, sp=5) + forma(s, GRIS_CL, 3.8, sp=5) + [R(circ(0, 0, 7, n=10), NEGRO, peso=0.02, sp=3)]
    return Dib(ops)


@lru_cache(maxsize=None)
def junco(tam=1.0, velas=3):
    """Barco de vela china con velas de listones."""
    casco = forma(curva([(-150, -60), (-120, -6), (0, 8), (130, -4), (170, -70)], 7), MADERA, 5.6, peso=0.6, sp=9)
    ops = casco + [T(linea((-146, -60), (166, -68)), 5, peso=0.1)]
    xs = {1: [0], 2: [-50, 50], 3: [-90, 0, 90], 4: [-110, -36, 36, 110]}[velas]
    for k, x in enumerate(xs):
        h = 250 - 14 * k
        ops += [T(linea((x, -62), (x, -62 - h)), 5.6, peso=0.12)]
        vela = pol((x + 4, -62 - h + 6), (x + 62, -62 - h * 0.86), (x + 66, -62 - 28), (x + 4, -62 - 22))
        ops += forma(vela, ROJO_CH if k % 2 == 0 else (212, 120, 80), 4.6, peso=0.35, sp=8)
        ops += [T(linea((x + 4, -62 - 22 - (h - 28) * j / 4), (x + 64, -62 - 28 - (h - 40) * j / 4)), 2.6, peso=0.02) for j in range(1, 4)]
    return Dib(ops)


@lru_cache(maxsize=None)
def carabela():
    ops = forma(curva([(-110, -50), (-88, 0), (0, 10), (96, 0), (124, -56)], 6), (150, 100, 70), 5.4, peso=0.5, sp=9)
    ops += [T(linea((-10, -50), (-10, -230)), 5, peso=0.1), T(linea((-70, -50), (-70, -190)), 5, peso=0.08), T(linea((56, -50), (56, -180)), 5, peso=0.08)]
    for x, h, w in ((-10, 230, 66), (-70, 190, 52), (56, 180, 50)):
        ops += forma(pol((x - w, -60 - h * 0.4), (x + w, -60 - h * 0.4), (x + w * 0.9, -60), (x - w * 0.9, -60)), CREMA, 4.6, peso=0.3, sp=8)
        ops += [R(pol((x - 6, -60 - h * 0.34), (x + 6, -60 - h * 0.34), (x + 6, -60 - h * 0.16), (x - 6, -60 - h * 0.16)), ROJO_CH, peso=0.02, sp=3)]
    return Dib(ops)


# ------------------------------------------------------------------ Yuan
@lru_cache(maxsize=None)
def caballo(pose=0):
    """Caballo en galope (4 poses)."""
    p = pose % 4
    col = (166, 112, 76)
    ops = forma(elip(0, -130, 92, 42, 0, 1.0, 30), col, 5.4, peso=0.6, sp=9)
    ops += forma(curva([(74, -150), (104, -206), (118, -252), (144, -262), (154, -236), (130, -214), (120, -168), (100, -110)], 6), col, 5.2, peso=0.5, sp=9)
    ops += forma(elip(152, -250, 26, 18, -0.5, 1.0, 18), col, 4.6, sp=7) + [punto(158, -258, 8)]
    ops += forma(pol((112, -262), (104, -300), (122, -270)), col, 3.6, sp=4)
    ops += forma(curva([(100, -262), (84, -236), (90, -206), (100, -180)], 5), NEGRO, 4.6, sp=6)
    # patas: 4 fases del galope
    offs = [((-50, -22), (-8, 10), (46, 28), (72, 6)), ((-30, 10), (-54, -26), (60, -14), (40, 26)), ((-8, 24), (-66, 4), (28, 6), (74, -18)), ((-46, 0), (-20, 30), (54, 20), (88, 10))][p]
    xs = (-64, -34, 40, 72)
    for x, (dx, dy) in zip(xs, offs):
        ops += forma(pol((x - 10, -100), (x + 10, -100), (x + dx + 8, dy * 0 - 4 + dy * 0), (x + dx - 8, -4)), col, 4.4, sp=6)
    ops += forma(curva([(-88, -148), (-130, -150), (-150, -120), (-140, -90)], 5), NEGRO, 4.6, sp=6)
    return Dib(ops)


@lru_cache(maxsize=None)
def jinete(pose=0, ropa=ROJO_OSC, sombrero_="gorro", arco=True, trenza=False, cara="enojo"):
    h = caballo(pose)
    r = persona(ropa, PIEL, sombrero_, cara, (40, 140) if arco else (40, 40), pose, traje="corta", trenza=trenza, acc_i="lanza" if not arco else None)
    ops = list(h.ops) + colocar(list(r.ops), 6, -150, 0.56)
    if arco:
        ops += [T(arco_(86, -270, 52, -80, 80, 12), 5, peso=0.1), T(linea((86 + 52 * math.cos(math.radians(-80)), -270 + 52 * math.sin(math.radians(-80))),
                                                                    (86 + 52 * math.cos(math.radians(80)), -270 + 52 * math.sin(math.radians(80)))), 2.6, peso=0.04)]
    return Dib(ops)


@lru_cache(maxsize=None)
def flecha():
    ops = [T(linea((-70, 0), (60, 0)), 5, peso=0.1)] + forma(pol((60, -10), (92, 0), (60, 10)), GRIS_CL, 3.6, sp=4)
    ops += [T(linea((-70, 0), (-84, -10)), 3.6, peso=0.02), T(linea((-70, 0), (-84, 10)), 3.6, peso=0.02), T(linea((-56, 0), (-70, -10)), 3.6, peso=0.02), T(linea((-56, 0), (-70, 10)), 3.6, peso=0.02)]
    return Dib(ops)


@lru_cache(maxsize=None)
def tormenta():
    from boceto import union_circulos
    circ_ = [(-130, -10, 70, 50), (-50, -60, 88, 50), (50, -70, 92, 50), (140, -14, 70, 50)]
    pts, _ = union_circulos(circ_, 50, (0, -20))
    th = np.arctan2(-(pts[:, 1] + 20), pts[:, 0])
    th = np.where(th < -math.pi / 2, th + 2 * math.pi, th)
    pts = pts[np.argsort(th)]
    base = np.stack([np.linspace(pts[-1, 0], pts[0, 0], 18), 50 + 3 * np.sin(np.linspace(0, 9, 18))], 1)
    P = np.vstack([pts, base, pts[:1]])
    ops = forma(P, (104, 110, 136), 5.6, peso=0.8, sp=11)
    ops += forma(pol((10, 50), (48, 50), (24, 100), (54, 100), (-6, 190), (8, 120), (-16, 120)), AMARILLO, 4.4, sp=6)
    ops += [T(linea((-90 + 40 * k, 62), (-98 + 40 * k, 100)), 4, peso=0.02) for k in range(6)]
    return Dib(ops)


@lru_cache(maxsize=None)
def yurta():
    ops = forma(pol((-90, 0), (-90, -70), (0, -150), (90, -70), (90, 0)), CREMA, 5.4, peso=0.6, sp=9)
    ops += forma(pol((-90, -70), (0, -150), (90, -70), (86, -60), (0, -130), (-86, -60)), (196, 150, 110), 4.4, sp=7)
    ops += forma(rect(-18, -58, 18, 0, 3), ROJO_CH, 4.2, sp=6)
    return Dib(ops)


@lru_cache(maxsize=None)
def arbol_familia():
    """Árbol genealógico de dos generaciones (abuelo -> nieto)."""
    ops = [T(linea((0, -20), (0, 40)), 5, peso=0.06), T(linea((-90, 40), (90, 40)), 5, peso=0.06), T(linea((-90, 40), (-90, 80)), 5, peso=0.04), T(linea((90, 40), (90, 80)), 5, peso=0.04),
           T(linea((0, -20), (0, -64)), 5, peso=0.04)]
    return Dib(ops)


# ------------------------------------------------------------------ Ming
@lru_cache(maxsize=None)
def huerfano(pose=0):
    return persona((190, 168, 130), PIEL_OSC, "pelo", "lloron", (30, 130), pose, traje="corta", acc_d="cuenco", alto=0.8)


@lru_cache(maxsize=None)
def emperador(pose=0, cara="feliz"):
    return persona(ORO, PIEL, "corona", cara, (20 + 20 * (pose % 2), 100), pose, traje="tunica", faja=ROJO_CH, cuello=ROJO_CH, bigote=True)


@lru_cache(maxsize=None)
def palacio():
    """Ciudad Prohibida: muro rojo y dos tejados dorados."""
    ops = forma(rect(-230, -70, 230, 0, 4), ROJO_CH, 5.6, peso=0.7, sp=10)
    ops += forma(rect(-180, -150, 180, -70, 4), (214, 120, 90), 5, peso=0.5, sp=9)
    for xx, w, y in ((0, 210, -150), (0, 150, -230)):
        ops += forma(pol((xx - w - 26, y + 10), (xx - w * 0.6, y - 50), (xx + w * 0.6, y - 50), (xx + w + 26, y + 10)), ORO, 5.4, peso=0.5, sp=8)
    ops += forma(rect(-110, -226, 110, -150, 3), (214, 120, 90), 4.8, peso=0.4, sp=9)
    ops += [T(linea((-200, -150), (-150, -210), (-110, -226)), 3, peso=0.05)]
    ops += forma(rect(-30, -70, 30, 0, 14), (120, 40, 40), 4.4, sp=6)
    ops += [R(circ(-110 + 44 * k, -34, 10, n=10), (240, 210, 130), peso=0.02, sp=3) for k in range(6)]
    return Dib(ops)


@lru_cache(maxsize=None)
def nave_tesoro():
    """Barco del tesoro: casco enorme con nueve mástiles (seis visibles)."""
    ops = forma(curva([(-210, -90), (-170, -10), (0, 14), (180, -6), (236, -110)], 8), MADERA, 6, peso=0.9, sp=10)
    ops += forma(rect(-180, -130, 210, -90, 6), (196, 130, 90), 5, peso=0.4, sp=9)
    xs = [-150, -90, -30, 30, 90, 150]
    for k, x in enumerate(xs):
        h = 300 - 22 * abs(k - 2.5)
        ops += [T(linea((x, -130), (x, -130 - h)), 5.6, peso=0.12)]
        vela = pol((x + 4, -130 - h + 8), (x + 56, -130 - h * 0.88), (x + 58, -130 - 34), (x + 4, -130 - 30))
        ops += forma(vela, ROJO_CH if k % 2 == 0 else (224, 140, 70), 4.6, peso=0.4, sp=8)
    ops += [R(circ(-186 + 26 * k, -108, 7, n=8), ORO, peso=0.02, sp=3) for k in range(10)]
    return Dib(ops)


def gran_puerta_cerrada(cierre=1.0):
    """La puerta se cierra (cierre 0..1) y al final lleva candado."""
    from obj_a import puerta
    return puerta(round(1 - cierre, 2), cierre > 0.95)


@lru_cache(maxsize=None)
def ladrillo_muro():
    ops = forma(rect(-90, -50, 90, 0, 3), (196, 150, 120), 5, peso=0.3, sp=8)
    ops += [T(linea((-90, -25), (90, -25)), 3, peso=0.03), T(linea((-45, -50), (-45, -25)), 3, peso=0.02), T(linea((15, -50), (15, -25)), 3, peso=0.02), T(linea((-15, -25), (-15, 0)), 3, peso=0.02), T(linea((55, -25), (55, 0)), 3, peso=0.02)]
    return Dib(ops)


@lru_cache(maxsize=None)
def pajaro(f=0):
    """Pajarito de dos trazos que bate las alas (2 poses)."""
    a = 26 if f % 2 == 0 else -6
    return Dib([T(curva([(-46, -a * 0.2), (-22, -a), (0, 0)], 6), 5, peso=0.05), T(curva([(0, 0), (22, -a), (46, -a * 0.2)], 6), 5, peso=0.05)])
