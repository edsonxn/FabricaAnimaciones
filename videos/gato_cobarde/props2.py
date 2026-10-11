# -*- coding: utf-8 -*-
"""Props de la cocina animados con tinta: puerta del refri (gira sobre las bisagras), ojo gigante del monstruo, lámpara colgante que se
balancea, reloj de gato con ojos y cola, gota que cae del grifo, grietas del techo, polvo de yeso."""
import math

import numpy as np

import toon as TN
from toon import blob, elipse_, suave, bezier2, tubo
from motor import clamp01, prog

MENTA = (140, 202, 172)
MENTA_S = (92, 148, 128)
CROMO = (222, 230, 232)
CROMO_S = (150, 162, 170)


def puerta_refri(h, th, F, sem=0):
    """Puerta del refri con la bisagra a la izquierda (x = F['bx']); th = ángulo de apertura en rad (0 cerrada). Devuelve (x_asa, y_asa)."""
    bx, y0, y1 = F["bx"], F["y0"], F["y1"]
    ancho = 460.0
    xf = bx + ancho * math.cos(th)
    k = 0.11 * math.sin(th)                       # el borde libre se acerca a la cámara: se ve más alto
    ym = (y0 + y1) / 2
    ya0, ya1 = ym - (ym - y0) * (1 + k), ym + (y1 - ym) * (1 + k)
    r = 70
    pts = [(bx, y0 + r), (bx + 16, y0 + 18), (bx + r, y0), (xf - r * 0.6 * abs(math.cos(th)) - 4, ya0),
           (xf, ya0 + r * 0.5), (xf, ya1 - 20), (xf - 10 * abs(math.cos(th)), ya1), (bx + 10, y1), (bx, y1 - 10)]
    P = suave(np.array(pts, float), 5, True)
    dentro = th > math.pi / 2
    col, sh = ((226, 238, 232), (176, 196, 192)) if dentro else (MENTA, MENTA_S)
    h.forma(P, col, sh, w=10, sem=sem + 1, d_sombra=(16 * (1 if not dentro else -1), 14), jit=2.0)
    if abs(math.cos(th)) > 0.12 and not dentro:
        # franja del congelador y letrerito
        a = np.array([[bx + 14, y0 + 330], [xf - 8, ya0 + 330 + (330 * k)]])
        h.trazo(a, 8, sem + 2, taper=(0.1, 0.1), jit=0.8, color=MENTA_S)
        # asa cromada vertical cerca del borde libre
        xa = bx + 0.9 * (xf - bx)
        asa = np.array([(xa - 11, 1080), (xa + 11, 1080), (xa + 11, 1290), (xa - 11, 1290)])
        asa = suave(asa, 4, True)
        h.forma(asa, CROMO, CROMO_S, w=7, sem=sem + 3, jit=0.8, d_sombra=(5, 6), tex=0.0)
        return xa, 1190.0
    xa = bx + 0.9 * (xf - bx)
    return xa, 1190.0


def ojo_gigante(h, x, y, r, abre, mira=(0.0, 0.0), miedo=0.0, sem=0, alfa=1.0):
    """Ojo enorme (esclerótica amarillenta con venas, iris naranja con pupila rasgada) que se abre bajo un párpado grueso."""
    if abre <= 0.03 or alfa <= 0.01:
        return
    rx, ry = r, r * 0.86
    a = np.linspace(0, 2 * math.pi, 40, endpoint=False)
    xs, ys = rx * np.cos(a), ry * np.sin(a)
    ytop = -ry * (2 * abre - 1)
    ys = np.clip(ys, ytop + 0.0 * xs, ry)
    P = np.stack([x + xs, y + ys], 1)
    # sombra de la cuenca
    h.forma(elipse_(x, y, r * 1.28, r * 1.06, n=24), (20, 16, 26), None, w=0, jit=2.0, alfa=0.85 * alfa, tex=0, sem=sem + 9)
    rr_ = h.forma(P, (244, 234, 160), (206, 186, 110), w=12, sem=sem + 10, jit=1.6, tex=0.0, d_sombra=(10, 14), alfa=alfa)
    if rr_ is None:
        return
    pr = r * (0.52 - 0.12 * miedo)
    ix, iy = x + mira[0] * (rx - pr) * 0.9, y + mira[1] * (ry - pr) * 0.9
    h.relleno(h.tf(np.stack([ix + pr * np.cos(a), iy + pr * np.sin(a)], 1)), (236, 104, 40), grad=((160, 40, 30), h.tf(np.array([[0, iy - pr]]))[0][1], h.tf(np.array([[0, iy + pr]]))[0][1]),
              clip=rr_, tex=0.0)
    pw = pr * (0.22 - 0.1 * miedo)
    h.relleno(h.tf(np.stack([ix + pw * np.cos(a), iy + pr * 0.96 * np.sin(a)], 1)), (20, 12, 16), clip=rr_, tex=0.0)
    rng = np.random.default_rng(sem + 3)
    for k in range(9):
        ang = rng.uniform(0, 2 * math.pi)
        ln = rx * rng.uniform(0.35, 0.7)
        a0 = np.array([x + math.cos(ang) * rx * 0.98, y + math.sin(ang) * ry * 0.98])
        a1 = np.array([x + math.cos(ang) * (rx * 0.98 - ln), y + math.sin(ang) * (ry * 0.98 - ln * 0.86)])
        h.trazo(np.array([a0, (a0 + a1) / 2 + rng.uniform(-8, 8, 2), a1]), 4, sem + 20 + k, color=(200, 40, 56), alfa=alfa, taper=(0.0, 0.8), jit=0.6)
    h.anillo(h.tf(P), 12.0, sem + 11, jit=0.0)
    if abre < 0.95:
        xs2 = np.linspace(-rx, rx, 14)
        h.trazo(np.stack([x + xs2, np.full(14, y + ytop)], 1), 16, sem + 12, taper=(0.1, 0.1), jit=0.8)


def lampara(h, x, y_techo, largo, ang, enciende=0.0, sem=0):
    """Lámpara colgante (cordón + pantalla cónica + foco) que se balancea con el ángulo `ang` (rad) desde el punto del techo."""
    p0 = np.array([x, y_techo])
    d = np.array([math.sin(ang), math.cos(ang)])
    p1 = p0 + d * largo
    h.trazo(np.array([p0, p1]), 6, sem, color=(24, 18, 26), taper=(0.1, 0.1), jit=0.5)
    n = np.array([d[1], -d[0]])
    pan = np.array([p1 - n * 20, p1 + n * 20, p1 + d * 80 + n * 90, p1 + d * 80 - n * 90])
    h.forma(suave(pan, 3, True), (96, 130, 96), (60, 90, 66), w=9, sem=sem + 1, jit=1.0, d_sombra=(10, 12))
    bulbo = elipse_(*(p1 + d * 86), 28, 22, n=16)
    col = (255, 238, 150) if enciende > 0.05 else (150, 150, 130)
    h.forma(bulbo, col, None, w=6, sem=sem + 2, jit=0.5, tex=0.0)
    return p1 + d * 86


def reloj_gato(h, x, y, r, t, sem=0):
    """Reloj de gato: cabeza negra con ojos que van de lado a lado y una cola que hace de péndulo."""
    sw = math.sin(2 * math.pi * 0.5 * t)
    cola = np.array([(x, y + r * 0.9), (x + 30 * sw, y + r * 1.9), (x + 50 * sw, y + r * 2.6)])
    h.trazo(cola, 12, sem, color=(20, 16, 22), taper=(0.0, 0.0), jit=0.6)
    h.disco(x + 54 * sw, y + r * 2.7, 20, (20, 16, 22), sem=sem + 1, w=0)
    cab = blob(x, y, r, r * 0.95, rad=[1, 1, 1, 1, 1, 1], n=6, sub=8)
    h.forma(cab, (34, 30, 40), (20, 16, 24), w=7, sem=sem + 2, jit=1.0, d_sombra=(8, 10))
    for s in (-1, 1):
        h.forma(np.array([(x + s * r * 0.5, y - r * 0.7), (x + s * r * 0.95, y - r * 1.25), (x + s * r * 0.95, y - r * 0.35)]), (34, 30, 40), None, w=7, sem=sem + 3 + s, jit=0.8)
        h.forma(elipse_(x + s * r * 0.36, y - r * 0.12, r * 0.28, r * 0.34, n=14), (250, 246, 226), None, w=4, sem=sem + 5 + s, jit=0.4, tex=0)
        h.disco(x + s * r * 0.36 + 9 * sw * 1.0, y - r * 0.08, r * 0.1, (16, 12, 18), sem=sem + 7 + s, w=0)
    h.trazo(np.array([[x - r * 0.3, y + r * 0.45], [x, y + r * 0.58], [x + r * 0.3, y + r * 0.45]]), 5, sem + 9, color=(240, 240, 230), taper=(0.2, 0.2), jit=0.5)


def gota_agua(h, x, y0, t, per=1.35, ph=0.0, sem=0):
    """Gota que se forma en la punta del grifo y cae (devuelve el instante del último impacto relativo)."""
    q = ((t + ph) % per) / per
    if q < 0.55:
        r = 4 + 12 * (q / 0.55)
        h.forma(elipse_(x, y0 + r * 0.8, r * 0.8, r * 1.0, n=14), (190, 226, 255), (140, 190, 235), w=4, sem=sem, jit=0.3, tex=0, d_sombra=(3, 4))
    elif q < 0.92:
        u = (q - 0.55) / 0.37
        yy = y0 + 14 + (1170 - y0) * u * u
        G = TN.gota(x, yy, 12 - 4 * u, ang=math.pi)
        h.forma(G, (190, 226, 255), (140, 190, 235), w=4, sem=sem + 1, jit=0.3, tex=0, d_sombra=(3, 4))
    else:
        u = (q - 0.92) / 0.08
        for s in (-1, 1):
            h.trazo(np.array([[x + s * 6, 1166], [x + s * (22 + 18 * u), 1146 - 12 * u]]), 4, sem + 2 + s, color=(190, 226, 255), taper=(0.1, 0.6), jit=0.3, alfa=1 - u)


def grieta(h, x, y, t0, t, largo=240, sem=0):
    """Grieta de yeso que se abre desde (x, y) con ramas."""
    k = clamp01((t - t0) / 0.18)
    if k <= 0:
        return
    rng = np.random.default_rng(sem + 11)
    for i in range(6):
        a = math.radians(rng.uniform(20, 160))
        L = largo * rng.uniform(0.4, 1.0) * k
        pts = [(x, y)]
        for j in range(5):
            a += rng.normal(0, 0.35)
            pts.append((pts[-1][0] + math.cos(a) * L / 5, pts[-1][1] + math.sin(a) * L / 5))
        h.trazo(np.array(pts), 5, sem + i, taper=(0.0, 0.8), jit=0.8)


def polvo_yeso(h, x, y, t0, t, n=14, sem=0):
    u = (t - t0) / 1.3
    if not 0 <= u < 1:
        return
    rng = np.random.default_rng(sem + 5)
    for i in range(n):
        a = rng.uniform(0, math.pi)
        d = (40 + 140 * rng.uniform()) * math.sqrt(u)
        px, py = x + math.cos(a) * d * 1.3, y + math.sin(a) * d * 0.9 + 180 * u * u * rng.uniform(0.3, 1.0)
        r = 14 + 24 * rng.uniform() * (1 - 0.4 * u)
        h.forma(elipse_(px, py, r, r * 0.9, n=10), (226, 220, 206), None, w=0, jit=1.2, alfa=(1 - u) * 0.8, tex=0, sem=sem + i)


# ------------------------------------------------------------------ comida del refri (props animables)
def tarta(h, x, y, s=1.0, ang=0.0, sem=0, rebanada=False):
    """Pastel con cerezas sobre su plato; (x, y) = centro de la base del plato. Se puede girar y mover (lo lleva el monstruo)."""
    c, sn = math.cos(ang), math.sin(ang)

    def T(P):
        P = np.asarray(P, float) * s
        return np.stack([x + P[:, 0] * c - P[:, 1] * sn, y + P[:, 0] * sn + P[:, 1] * c], 1)
    h.forma(T(elipse_(0, -10, 140, 24, n=24)), (250, 250, 252), (206, 212, 220), w=6, sem=sem, jit=0.6, d_sombra=(8, 8), tex=0)
    cuerpo = np.array([(-120, -22), (120, -22), (104, -100), (-104, -100)])
    h.forma(T(suave(cuerpo, 5, True)), (216, 152, 66), (166, 98, 40), w=8, sem=sem + 1, jit=1.0, d_sombra=(14, 12))
    tapa = np.array([(-104, -100), (104, -100), (86, -122), (-86, -122)])
    h.forma(T(suave(tapa, 5, True)), (248, 224, 158), (214, 178, 110), w=7, sem=sem + 2, jit=0.8, d_sombra=(10, 8))
    for k in range(5):
        cx = -60 + k * 30
        h.disco(*T(np.array([[cx, -128]]))[0], 12 * s, (206, 36, 60), sem=sem + 3 + k, w=5)
    if rebanada:
        h.forma(T(np.array([(10, -22), (60, -22), (46, -118), (10, -100)])), (250, 250, 252), None, w=0, sem=sem + 9, jit=0.2, tex=0)


def pescado(h, x, y, s=1.0, ang=0.0, sem=0):
    """Espinas de pescado sobre un plato (la cena del gato)."""
    c, sn = math.cos(ang), math.sin(ang)

    def T(P):
        P = np.asarray(P, float) * s
        return np.stack([x + P[:, 0] * c - P[:, 1] * sn, y + P[:, 0] * sn + P[:, 1] * c], 1)
    h.forma(T(elipse_(0, -8, 130, 20, n=24)), (250, 250, 252), (206, 212, 220), w=6, sem=sem, jit=0.6, d_sombra=(8, 8), tex=0)
    h.trazo(T(np.array([[-70, -30], [70, -30]])), 7, sem + 1, color=(236, 230, 214), taper=(0.1, 0.1), jit=0.6)
    for k in range(7):
        xx = -56 + k * 17
        h.trazo(T(np.array([[xx, -30], [xx + 4, -58 + 4 * abs(k - 3)]])), 5, sem + 2 + k, color=(236, 230, 214), taper=(0.1, 0.4), jit=0.5)
        h.trazo(T(np.array([[xx, -30], [xx + 4, -4 - 4 * abs(k - 3) * 0 - 2]])), 4, sem + 12 + k, color=(236, 230, 214), taper=(0.1, 0.4), jit=0.5)
    cab = np.array([(-110, -30), (-72, -58), (-70, -4)])
    h.forma(T(cab), (240, 236, 222), (200, 196, 180), w=5, sem=sem + 20, jit=0.5, d_sombra=(4, 4), tex=0)
    h.disco(*T(np.array([[-92, -34]]))[0], 4 * s, (24, 18, 26), sem=sem + 21, w=0)
    cola = np.array([(70, -30), (112, -62), (112, -2)])
    h.forma(T(cola), (240, 236, 222), (200, 196, 180), w=5, sem=sem + 22, jit=0.5, d_sombra=(4, 4), tex=0)


def hielo(h, x, y, ang, s=1.0, sem=0, alfa=1.0):
    """Cubito de hielo (sale disparado cuando revienta el refri)."""
    c, sn = math.cos(ang), math.sin(ang)
    P = np.array([(-26, -26), (26, -26), (26, 26), (-26, 26)], float) * s
    Q = np.stack([x + P[:, 0] * c - P[:, 1] * sn, y + P[:, 0] * sn + P[:, 1] * c], 1)
    h.forma(Q, (200, 238, 252), (150, 200, 230), w=5, sem=sem, jit=0.5, d_sombra=(6, 6), tex=0, alfa=alfa)
    h.trazo(np.array([Q[0] * 0.7 + Q[2] * 0.3, Q[0] * 0.5 + Q[1] * 0.2 + Q[2] * 0.3]), 3, sem + 1, color=(255, 255, 255), taper=(0.1, 0.3), jit=0.3, alfa=alfa)


def nube_escarcha(h, x, y, r, k, sem=0, color=(226, 244, 250)):
    """Bocanada de vapor/escarcha que sube y se disuelve (k 0..1 = edad)."""
    rng = np.random.default_rng(sem + 2)
    for i in range(7):
        a = rng.uniform(0, 2 * math.pi)
        d = r * rng.uniform(0.2, 0.9) * (0.4 + k)
        rr_ = r * rng.uniform(0.35, 0.6) * (0.5 + 0.8 * k)
        h.forma(elipse_(x + math.cos(a) * d, y + math.sin(a) * d * 0.7 - 60 * k, rr_, rr_ * 0.9, n=10), color, None, w=0, jit=2.0, alfa=(1 - k) * 0.75, tex=0, sem=sem + i)


def estrellitas(h, x, y, t, r=120, n=5, sem=0):
    """Estrellitas que giran sobre una cabeza (mareo)."""
    for k in range(n):
        a = t * 4.2 + k * 2 * math.pi / n
        h.forma(TN.estrella(x + r * math.cos(a), y + r * 0.28 * math.sin(a), 26, 11, 5, rot=a), (255, 226, 90), None, w=5, sem=sem + k, jit=0.5, tex=0)


def sombra_cuernos(h, xc, yb, k, a, u, punta, sem=400, col=(8, 6, 18), ojos=True):
    """Sombra gigante con cuernos, un brazo largo con garras que alcanza `punta` y ojos que brillan. a = opacidad 0..1, k = escala."""
    if a <= 0.01:
        return
    cuerpo = blob(xc, yb - 520 * k, 250 * k, 360 * k, rad=[1, 1.08, 0.94, 1.05, 1.0, 0.92, 1.06, 1.0], n=8, sub=8)
    h.forma(cuerpo, col, None, w=0, jit=2.0, alfa=0.80 * a, tex=0, sem=sem)
    cab = blob(xc - 60 * k, yb - 900 * k, 118 * k, 104 * k, rad=[1, 1.1, 0.95, 1.05, 1, 0.92], n=6, sub=8)
    h.forma(cab, col, None, w=0, jit=2.0, alfa=0.80 * a, tex=0, sem=sem + 1)
    for sg in (-1, 1):
        c0 = np.array([xc - 60 * k + sg * 70 * k, yb - 960 * k])
        h.forma(np.array([c0, c0 + np.array([sg * 40 * k, -150 * k]), c0 + np.array([-sg * 20 * k, -10 * k])]), col, None, w=0, jit=1.0,
                alfa=0.80 * a, tex=0, sem=sem + 2 + sg)
    base = np.array([xc - 190 * k, yb - 620 * k])
    punta = np.asarray(punta, float)
    eje = TN.eje_curvo(base, punta, -140 * k, 20)
    h.forma(tubo(eje, 70 * k, 30 * k), col, None, w=0, jit=2.0, alfa=0.80 * a, tex=0, sem=sem + 4)
    d = punta - eje[-3]
    d = d / (np.hypot(*d) + 1e-9)
    n_ = np.array([-d[1], d[0]])
    for i in (-1, 0, 1):
        b0 = punta + n_ * i * 16 * k
        h.forma(np.array([b0 - n_ * 7 * k, b0 + d * 70 * k + n_ * i * 10 * k, b0 + n_ * 7 * k]), col, None, w=0, jit=0.8, alfa=0.80 * a, tex=0, sem=sem + 10 + i)
    if ojos:
        ea = clamp01((a - 0.4) / 0.4)
        for sg in (-1, 1):
            h.forma(np.array([(xc - 60 * k + sg * 44 * k - 24 * k, yb - 900 * k - 8 * k), (xc - 60 * k + sg * 44 * k + 24 * k, yb - 900 * k + 8 * k * sg),
                              (xc - 60 * k + sg * 44 * k + 20 * k, yb - 900 * k + 22 * k)]), (255, 214, 70), None, w=0, jit=0.5, alfa=ea, tex=0, sem=sem + 20 + sg)


def llama(h, x, y, t, k=1.0, sem=0):
    """Llama de vela que baila (k = tamaño; 0 la apaga)."""
    if k <= 0.02:
        return
    w = 1.0 + 0.12 * math.sin(t * 17 + sem) + 0.07 * math.sin(t * 29)
    P = np.array([(x, y - 74 * k * w), (x + 17 * k, y - 28 * k), (x + 12 * k, y + 6 * k), (x, y + 12 * k), (x - 12 * k, y + 6 * k), (x - 17 * k, y - 28 * k)], float)
    P[0, 0] += 6 * k * math.sin(t * 13 + sem)
    h.forma(suave(P, 4, True), (255, 176, 60), None, w=0, jit=0.6, tex=0, sem=sem)
    Q = np.array([(x, y - 40 * k * w), (x + 8 * k, y - 12 * k), (x, y + 6 * k), (x - 8 * k, y - 12 * k)], float)
    h.forma(suave(Q, 4, True), (255, 240, 160), None, w=0, jit=0.4, tex=0, sem=sem + 1)


def vela(h, x, y, sem=0):
    h.forma(suave(np.array([(x - 15, y), (x + 15, y), (x + 13, y + 100), (x - 13, y + 100)], float), 3, True), (244, 236, 214), (206, 196, 170), w=6, sem=sem,
            jit=0.6, d_sombra=(5, 6), tex=0)
    h.forma(elipse_(x, y + 104, 46, 10, n=18), (170, 130, 70), (120, 90, 50), w=5, sem=sem + 1, jit=0.5, tex=0)
    h.trazo(np.array([[x, y], [x, y - 12]]), 3, sem + 2, taper=(0.1, 0.1), jit=0.2)


def sombra_techo(h, a, u, sem=500, col=(6, 4, 14)):
    """La sombra que se asoma por ENCIMA de la cámara: cabezota con cuernos y ojos que brillan, y dos brazos largos con garras que abrazan la mesa.
    a = 0..1 (cuánto ha bajado; 1 = de lleno). Todo en coordenadas de mundo de la cocina (pantalla sin cámara)."""
    if a <= 0.01:
        return
    dy = -820 * (1 - smooth_(a))
    al = 0.93 * min(1.0, a * 2.0)
    cab = blob(540, 330 + dy, 360, 270, rad=[1, 1.06, 0.96, 1.04, 1.0, 0.94, 1.05, 0.98], n=8, sub=8)
    h.forma(cab, col, None, w=0, jit=3.0, alfa=al, tex=0, sem=sem)
    for sg in (-1, 1):
        c0 = np.array([540 + sg * 250, 160 + dy])
        P = np.array([c0 + np.array([-sg * 60, 40]), c0 + np.array([sg * 20, -120]), c0 + np.array([sg * 120, -330]), c0 + np.array([sg * 190, -520]),
                      c0 + np.array([sg * 150, -300]), c0 + np.array([sg * 110, -120]), c0 + np.array([sg * 60, 70])])
        h.forma(suave(P, 5, True), col, None, w=0, jit=2.0, alfa=al, tex=0, sem=sem + 1 + sg)
        base = np.array([540 + sg * 330, 420 + dy])
        punta = np.array([540 + sg * 470 + sg * 30 * math.sin(u * 3), 1290 + dy * 0.3])
        eje = TN.eje_curvo(base, punta, sg * 120, 22)
        h.forma(tubo(eje, 150, 60), col, None, w=0, jit=2.5, alfa=al, tex=0, sem=sem + 4 + sg)
        d = punta - eje[-3]
        d = d / (np.hypot(*d) + 1e-9)
        n_ = np.array([-d[1], d[0]])
        for i in (-1, 0, 1):
            b0 = punta + n_ * i * 30
            h.forma(np.array([b0 - n_ * 12, b0 + d * 150 + n_ * i * 18, b0 + n_ * 12]), col, None, w=0, jit=1.0, alfa=al, tex=0, sem=sem + 10 + i + 3 * sg)
    ea = clamp01((a - 0.55) / 0.35)
    for sg in (-1, 1):
        ex, ey = 540 + sg * 140, 320 + dy
        h.forma(np.array([(ex - 70 * sg * 0.0 - 62, ey - 22 * sg), (ex + 62, ey + 22 * sg), (ex + 52, ey + 46), (ex - 52, ey + 30)]), (255, 214, 60), None, w=0, jit=0.8,
                alfa=ea, tex=0, sem=sem + 30 + sg)
        h.forma(np.array([(ex - 14, ey - 4), (ex + 14, ey + 4), (ex + 6, ey + 40), (ex - 8, ey + 34)]), (40, 10, 10), None, w=0, jit=0.4, alfa=ea, tex=0, sem=sem + 33 + sg)
    if ea > 0:
        h.luz_radial(540, 340 + dy, 900, (1.0, 0.7, 0.2), 0.5 * ea, mundo=False)


def smooth_(x):
    x = 0.0 if x < 0 else 1.0 if x > 1 else x
    return x * x * (3 - 2 * x)
