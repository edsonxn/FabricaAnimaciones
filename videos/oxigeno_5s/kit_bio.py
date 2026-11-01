# -*- coding: utf-8 -*-
"""Biología y diagramas del video «oxígeno 5 s» (estilo Kurzgesagt): pulmones, cerebro, glóbulo rojo, mitocondria,
glucosa, batería de energía, oído en corte, manómetro, cronómetro, tarta de porcentaje, lupa, ADN, proteína,
cianobacterias y diatomeas. Origen en el centro salvo que se diga otra cosa."""
import math

import numpy as np

import plano as P
from plano import mezcla, aclarar, oscurecer, SOMBRA, TINTA
from motor import circulo, elipse, rect_red, catmull, clamp01, lerp, h01
import kit_oxi as KO

BLANCO = (255, 255, 255)


# ======================================================================== órganos
def pulmones(lz, x, y, s, infla=0.5, col=(240, 120, 140), o2=1.0, t=0.0):
    """Par de pulmones con tráquea; infla 0..1 los hincha; o2 colorea de rojo vivo (1) o violáceo (0)."""
    c = mezcla((150, 110, 170), col, o2)
    k = 0.88 + 0.16 * infla
    with lz.grupo(x, y, s):
        lz.relleno(rect_red(-12, -150, 24, 90, 10), (236, 200, 210))
        for i in range(5):
            lz.relleno(rect_red(-14, -146 + i * 18, 28, 6, 3), (214, 176, 190))
        lz.trazo(np.array([[0, -62], [-40, -30]]), (236, 200, 210), 18, afinar=False)
        lz.trazo(np.array([[0, -62], [40, -30]]), (236, 200, 210), 18, afinar=False)
        for lado in (-1, 1):
            pts = np.array([[8, -70], [60, -96], [104, -40], [118, 60], [92, 118], [30, 120], [10, 60], [22, -10]], float)
            pts[:, 0] *= lado
            pts = pts * k
            lz.relleno(catmull(pts, 8, True), c)
            lz.relleno(catmull(pts * 0.7 + [lado * 22, 22], 8, True), oscurecer(c, 0.18), alfa=0.6)
            lz.relleno(elipse(lado * 70 * k, -40 * k, 16 * k, 26 * k, lado * 0.3, 20), aclarar(c, 0.4), alfa=0.6)
            for j in range(4):   # bronquios
                a = -0.4 + j * 0.35
                lz.trazo(np.array([[lado * 40, -30], [lado * (40 + 50 * math.cos(a)), -30 + 60 * math.sin(a + 0.8)]]) * k,
                         aclarar(c, 0.35), 6, afinar=False)


def cerebro(lz, x, y, s, t=0.0, energia=1.0, falta=0.0, col=(246, 150, 180)):
    """Cerebro de perfil con circunvoluciones; energia 0..1 = brillo de actividad (destellos); falta 0..1 = gris."""
    c = mezcla(col, (150, 140, 170), falta)
    with lz.grupo(x, y, s):
        sil = np.array([[-130, 10], [-138, -40], [-110, -92], [-50, -122], [20, -120], [86, -96], [126, -50], [130, 0],
                        [110, 40], [60, 52], [30, 80], [0, 76], [-20, 56], [-80, 56]], float)
        lz.relleno(catmull(sil, 8, True), c)
        lz.relleno(catmull(np.array([[40, 52], [90, 46], [120, 60], [100, 96], [50, 92]], float), 6, True),
                   oscurecer(c, 0.15))                                  # cerebelo
        lz.relleno(rect_red(-8, 60, 28, 70, 12), oscurecer(c, 0.1))    # tronco
        surcos = [[(-110, -40), (-70, -60), (-40, -40), (-10, -70)], [(-100, 0), (-60, -16), (-20, 4), (20, -26), (60, -10)],
                  [(-30, -100), (0, -76), (40, -96), (80, -70)], [(-70, 30), (-30, 20), (10, 36), (50, 20), (96, 10)],
                  [(30, -50), (70, -40), (100, -60)]]
        for i, sc in enumerate(surcos):
            lz.trazo(catmull(np.array(sc, float), 6), oscurecer(c, 0.32), 7, afinar=True)
        lz.relleno(elipse(-60, -86, 40, 16, -0.3, 20), aclarar(c, 0.35), alfa=0.6)
        if energia > 0.01:
            for i in range(9):
                u = (t * 1.3 + i * 0.37) % 1
                px = -100 + (i * 47) % 200
                py = -90 + (i * 31) % 130
                a = math.sin(u * math.pi)
                lz.halo(px, py, 26, (255, 240, 150), alfa=0.8 * a * energia, capa=2)


def globulo(lz, x, y, s, rot=0.0, oxi=1.0, alfa=1.0):
    """Glóbulo rojo (disco bicóncavo visto en 3/4). oxi 0..1: rojo vivo -> granate oscuro."""
    c = mezcla((150, 50, 90), (232, 60, 70), oxi)
    with lz.grupo(x, y, s, rot):
        lz.relleno(elipse(0, 0, 40, 26, 0, 30), c, alfa=alfa)
        lz.relleno(elipse(2, 2, 24, 13, 0, 24), oscurecer(c, 0.22), alfa=alfa)
        lz.relleno(elipse(-12, -12, 14, 5, -0.2, 14), aclarar(c, 0.4), alfa=0.7 * alfa)


def mitocondria(lz, x, y, s, t=0.0, activo=1.0, rot=0.0):
    c = mezcla((150, 140, 170), (255, 140, 90), activo)
    with lz.grupo(x, y, s, rot):
        lz.relleno(elipse(0, 0, 70, 36, 0, 40), c)
        lz.relleno(elipse(0, 0, 60, 27, 0, 36), aclarar(c, 0.3))
        pts = []
        for i in range(12):
            xx = -50 + i * 9.1
            pts.append([xx, (-22 if i % 2 == 0 else 22) * (1 if i not in (0, 11) else 0.6)])
        lz.trazo(np.array(pts), oscurecer(c, 0.12), 6, afinar=False)
        if activo > 0.05:
            lz.halo(0, 0, 90, (255, 200, 120), alfa=0.35 * activo * (0.8 + 0.2 * math.sin(t * 6)))


def glucosa(lz, x, y, s, rot=0.0, alfa=1.0):
    with lz.grupo(x, y, s, rot):
        hexa = np.array([[22 * math.cos(a), 22 * math.sin(a)] for a in np.linspace(0, 2 * math.pi, 7)[:-1] + math.pi / 6])
        lz.relleno(hexa, (255, 214, 90), alfa=alfa)
        lz.relleno(hexa * 0.55, (255, 240, 170), alfa=alfa)


def bateria(lz, x, y, s, nivel=1.0, alfa=1.0):
    """Pila de energía (ATP) con nivel 0..1."""
    with lz.grupo(x, y, s):
        lz.relleno(rect_red(-44, -80, 88, 160, 16), (60, 54, 96), alfa=alfa)
        lz.relleno(rect_red(-16, -94, 32, 16, 6), (60, 54, 96), alfa=alfa)
        h = 136 * clamp01(nivel)
        c = mezcla((236, 80, 80), (120, 230, 140), clamp01(nivel * 1.5 - 0.2))
        if h > 2:
            lz.relleno(rect_red(-32, 68 - h, 64, h, 10), c, alfa=alfa)
        lz.relleno(np.array([[6, -50], [-18, 6], [0, 6], [-8, 48], [20, -10], [2, -10]]), (255, 250, 220), alfa=alfa)


def oido(lz, x, y, s, t=0.0, bombeo=0.0, alfa=1.0, rotura=0.0):
    """Oído en corte: conducto auditivo, tímpano (se abomba hacia fuera con bombeo>0, hacia dentro con <0),
    huesecillos y caracol. Las flechas de presión las dibuja quien llama."""
    with lz.grupo(x, y, s):
        piel = (236, 170, 130)
        lz.relleno(catmull(np.array([[-260, -170], [-120, -190], [-60, -120], [-60, -40], [-120, -20], [-140, 40],
                                     [-60, 50], [-60, 130], [-150, 190], [-260, 170]], float), 8, True), piel, alfa=alfa)
        lz.relleno(rect_red(-260, -40, 210, 80, 30), (130, 70, 80), alfa=alfa)     # conducto
        lz.relleno(rect_red(-60, -170, 280, 340, 40), (250, 214, 196), alfa=alfa)  # hueso / oído medio
        lz.relleno(rect_red(-50, -90, 120, 180, 30), (255, 236, 226), alfa=alfa)   # cavidad
        # tímpano
        b = 34 * bombeo
        mem = np.array([[-50, -60], [-50 - b * 0.6, -30], [-50 - b, 0], [-50 - b * 0.6, 30], [-50, 60]], float)
        lz.trazo(catmull(mem, 6), (236, 90, 110), 10, afinar=False)
        if rotura > 0.05:
            lz.trazo(np.array([[-50 - b, -8], [-44 - b, 0], [-56 - b, 8], [-48 - b, 16]]), (255, 255, 255, int(255 * rotura)), 4,
                     afinar=False)
        # huesecillos
        lz.trazo(np.array([[-46 - b * 0.8, 0], [0, -20], [30, 10], [60, -10]]), (240, 220, 180), 9, afinar=False)
        # caracol
        lz.relleno(circulo(150, 0, 60, 30), (255, 190, 170), alfa=alfa)
        lz.trazo(P.arco_pts(150, 0, 40, 0, 4.5, 30), (230, 140, 140), 8, afinar=False)
        lz.trazo(P.arco_pts(150, 0, 20, 0, 5.0, 24), (230, 140, 140), 7, afinar=False)


# ======================================================================== instrumentos y gráficos
def manometro(lz, x, y, r, valor, vmin=0.0, vmax=120.0, t=0.0, marcas=(0, 20, 40, 60, 80, 100, 120), rojo=None,
              texto=None, alfa=1.0, k=1.0):
    """Manómetro (presión) de radio r: escala de 225° y aguja en `valor`."""
    if k <= 0.01 or alfa <= 0.01:
        return
    a0, a1 = math.radians(135), math.radians(405)

    def ang(v):
        return a0 + (a1 - a0) * clamp01((v - vmin) / (vmax - vmin))
    with lz.capa(2):
        with lz.grupo(x, y, k):
            lz.relleno(circulo(6, 10, r * 1.08, 60), (20, 16, 50), alfa=0.25 * alfa)
            lz.relleno(circulo(0, 0, r * 1.08, 60), (196, 202, 226), alfa=alfa)
            lz.relleno(circulo(0, 0, r, 60), (250, 250, 255), alfa=alfa)
            if rojo is not None:
                th = np.linspace(ang(rojo[0]), ang(rojo[1]), 30)
                ext = np.stack([np.cos(th), np.sin(th)], 1) * r * 0.93
                inn = (np.stack([np.cos(th), np.sin(th)], 1) * r * 0.80)[::-1]
                lz.relleno(np.concatenate([ext, inn]), (255, 120, 110), alfa=0.8 * alfa)
            for m in marcas:
                a = ang(m)
                lz.trazo(np.array([[math.cos(a) * r * 0.8, math.sin(a) * r * 0.8], [math.cos(a) * r * 0.93, math.sin(a) * r * 0.93]]),
                         (60, 54, 96, int(255 * alfa)), 5, afinar=False)
                P.rotulo(lz, math.cos(a) * r * 0.64, math.sin(a) * r * 0.64, str(m), r * 0.16, color=(60, 54, 96), sombra=0,
                         alfa=alfa, capa=2)
            a = ang(valor) + 0.01 * math.sin(t * 30)
            lz.relleno(np.array([[math.cos(a + 1.57) * 6, math.sin(a + 1.57) * 6], [math.cos(a) * r * 0.86, math.sin(a) * r * 0.86],
                                 [math.cos(a - 1.57) * 6, math.sin(a - 1.57) * 6]]), (236, 72, 84), alfa=alfa)
            lz.relleno(circulo(0, 0, r * 0.08, 20), (60, 54, 96), alfa=alfa)
            if texto:
                P.rotulo(lz, 0, r * 0.5, texto, r * 0.17, color=(60, 54, 96), sombra=0, alfa=alfa, capa=2)


def cronometro(lz, x, y, r, frac=0.0, numero=None, alfa=1.0, k=1.0, col=(236, 72, 84), t=0.0):
    """Cronómetro: esfera clara con un sector que se llena (frac 0..1) y una cifra grande."""
    if k <= 0.01 or alfa <= 0.01:
        return
    with lz.capa(2):
        with lz.grupo(x, y, k):
            lz.relleno(circulo(6, 10, r * 1.1, 60), (20, 16, 50), alfa=0.25 * alfa)
            lz.relleno(rect_red(-r * 0.18, -r * 1.36, r * 0.36, r * 0.3, r * 0.06), (196, 202, 226), alfa=alfa)
            lz.relleno(circulo(0, 0, r * 1.1, 60), (196, 202, 226), alfa=alfa)
            lz.relleno(circulo(0, 0, r, 60), (250, 250, 255), alfa=alfa)
            if frac > 0.002:
                th = np.linspace(-math.pi / 2, -math.pi / 2 + 2 * math.pi * clamp01(frac), 64)
                lz.relleno(np.concatenate([[[0, 0]], np.stack([np.cos(th), np.sin(th)], 1) * r * 0.9]), aclarar(col, 0.55),
                           alfa=alfa)
                a = th[-1]
                lz.trazo(np.array([[0, 0], [math.cos(a) * r * 0.9, math.sin(a) * r * 0.9]]), col + (int(255 * alfa),), 6,
                         afinar=False)
            for i in range(12):
                a = i / 12 * 2 * math.pi
                lz.relleno(circulo(math.cos(a) * r * 0.94, math.sin(a) * r * 0.94, r * 0.025, 10), (120, 116, 150), alfa=alfa)
            if numero is not None:
                P.rotulo(lz, 0, r * 0.05, str(numero), r * 0.75, color=(60, 54, 96), fuente="geo_x", sombra=0, alfa=alfa,
                         capa=2)


def tarta(lz, x, y, r, frac, col=(236, 72, 84), resto=(230, 226, 240), texto=None, sub=None, k=1.0, alfa=1.0, crece=1.0,
          px=None, a0=-math.pi / 2):
    """Gráfico de tarta: porción `frac` en `col` (que se dibuja hasta crece*frac), con cifra en el centro."""
    if k <= 0.01 or alfa <= 0.01:
        return
    with lz.capa(2):
        with lz.grupo(x, y, k):
            lz.relleno(circulo(5, 9, r * 1.04, 64), (20, 16, 50), alfa=0.22 * alfa)
            lz.relleno(circulo(0, 0, r, 64), resto, alfa=alfa)
            f = clamp01(frac * crece)
            if f > 0.002:
                th = np.linspace(a0, a0 + 2 * math.pi * f, max(8, int(80 * f)))
                lz.relleno(np.concatenate([[[0, 0]], np.stack([np.cos(th), np.sin(th)], 1) * r]), col, alfa=alfa)
            lz.relleno(circulo(0, 0, r * 0.58, 50), (250, 250, 255), alfa=alfa)
            if texto:
                P.rotulo(lz, 0, -r * 0.04 if sub else 0, texto, px or r * 0.36, color=oscurecer(col, 0.25), fuente="geo_x", sombra=0,
                         alfa=alfa, capa=2)
            if sub:
                P.rotulo(lz, 0, r * 0.28, sub, r * 0.15, color=(90, 84, 120), sombra=0, alfa=alfa, capa=2)


def lupa(lz, x, y, r, contenido, fondo=(20, 24, 60), borde=(255, 255, 255), k=1.0, alfa=1.0, objetivo=None, capa=2):
    """Círculo de aumento: contenido(lz) se dibuja recortado (origen en el centro). objetivo=(x, y): cola hacia ese punto."""
    if k <= 0.01 or alfa <= 0.01:
        return
    with lz.capa(capa):
        if objetivo is not None:
            ox, oy = objetivo
            d = math.hypot(ox - x, oy - y)
            if d > r * k + 10:
                ux, uy = (ox - x) / d, (oy - y) / d
                lz.relleno(np.array([[x + uy * r * 0.25 * k, y - ux * r * 0.25 * k], [ox, oy],
                                     [x - uy * r * 0.25 * k, y + ux * r * 0.25 * k]]), borde, alfa=0.85 * alfa * min(1, k))
                lz.relleno(circulo(ox, oy, 8, 14), borde, alfa=alfa * min(1, k))
        with lz.grupo(x, y, k):
            lz.relleno(circulo(6, 10, r * 1.06, 70), (20, 16, 50), alfa=0.25 * alfa)
            lz.relleno(circulo(0, 0, r * 1.06, 70), borde, alfa=alfa)
            C = circulo(0, 0, r, 90)
            lz.relleno(C, fondo, alfa=alfa)
            with lz.recorte(C):
                contenido(lz)
            lz.relleno(P.borde_luz(0, 0, r, -math.pi * 0.75, 0.05), (255, 255, 255), alfa=0.25 * alfa)


def flecha(lz, p0, p1, col=(255, 255, 255), ancho=10.0, punta=26.0, alfa=1.0, frac=1.0):
    p0, p1 = np.array(p0, float), np.array(p1, float)
    if frac <= 0.01 or alfa <= 0.01:
        return
    p1 = p0 + (p1 - p0) * clamp01(frac)
    d = p1 - p0
    L = float(np.hypot(*d)) + 1e-6
    u = d / L
    n = np.array([-u[1], u[0]])
    base = p1 - u * punta
    lz.trazo(np.array([p0, base + u * 2]), col + (int(255 * alfa),), ancho, afinar=False)
    lz.relleno(np.array([p1, base + n * punta * 0.6, base - n * punta * 0.6]), col, alfa=alfa)


# ======================================================================== moléculas de la vida
def adn(lz, x, y, s, t=0.0, largo=360, falta_o=0.0, alfa=1.0):
    """Doble hélice horizontal con peldaños; los átomos de O (puntos rojos) se apagan con falta_o."""
    with lz.grupo(x, y, s):
        xs = np.linspace(-largo / 2, largo / 2, 60)
        f = xs / 38 + t * 1.2
        y1, y2 = 46 * np.sin(f), 46 * np.sin(f + math.pi)
        for i in range(0, 60, 4):
            lz.trazo(np.array([[xs[i], y1[i]], [xs[i], y2[i]]]), ((255, 200, 90) if i % 8 else (110, 210, 190)) + (int(255 * alfa),),
                     7, afinar=False)
        lz.trazo(np.stack([xs, y1], 1), (120, 140, 240, int(255 * alfa)), 11, afinar=False)
        lz.trazo(np.stack([xs, y2], 1), (90, 110, 220, int(255 * alfa)), 11, afinar=False)
        for i in range(2, 60, 8):
            KO.atomo(lz, xs[i], y1[i], 7, KO.COL_AT["O"], alfa * (1 - falta_o))


def proteina(lz, x, y, s, t=0.0, falta_o=0.0, alfa=1.0, seed=3):
    """Cadena plegada (proteína) de cuentas de colores con algunos O rojos."""
    rng = np.random.default_rng(seed)
    pts = [np.array([0.0, 0.0])]
    ang = 0.0
    for i in range(34):
        ang += rng.normal(0, 0.9)
        p = pts[-1] + 22 * np.array([math.cos(ang), math.sin(ang)])
        p = np.clip(p, -110, 110)
        pts.append(p)
    pts = np.array(pts)
    pts = pts - pts.mean(0)
    with lz.grupo(x, y, s, 0.1 * math.sin(t * 0.7)):
        lz.trazo(catmull(pts, 4), (180, 170, 230, int(255 * alfa)), 9, afinar=False)
        cols = [(255, 200, 90), (110, 210, 190), (150, 130, 230), (255, 150, 120)]
        for i, p in enumerate(pts):
            if i % 5 == 2:
                KO.atomo(lz, p[0], p[1], 9, KO.COL_AT["O"], alfa * (1 - falta_o))
            else:
                lz.relleno(circulo(p[0], p[1], 8, 14), cols[i % 4], alfa=alfa)


def cianobacteria(lz, x, y, s, t=0.0, n=7, seed=0, burbujas=1.0, col=(80, 200, 140)):
    """Filamento de cianobacteria (cadena de células verdes que ondula) que suelta burbujitas de O2."""
    with lz.grupo(x, y, s):
        for i in range(n):
            px = (i - n / 2) * 30
            py = 12 * math.sin(t * 1.6 + i * 0.7 + seed)
            lz.relleno(elipse(px, py, 17, 14, 0.3 * math.sin(i + t), 22), col)
            lz.relleno(elipse(px - 4, py - 4, 7, 5, 0, 12), aclarar(col, 0.4), alfa=0.8)
            lz.relleno(circulo(px + 3, py + 3, 4, 10), oscurecer(col, 0.3), alfa=0.6)
        if burbujas > 0.01:
            for i in range(5):
                u = (t * 0.5 + i / 5 + seed * 0.13) % 1
                bx = (i - 2) * 40 + 10 * math.sin(u * 8 + i)
                by = -20 - u * 160
                KO.molecula(lz, bx, by, 0.45, "O2", rot=u * 3 + i, alfa=burbujas * (1 - u ** 3))


def diatomea(lz, x, y, s, t=0.0, seed=0, col=(140, 220, 200)):
    """Fitoplancton: diatomea (caja de vidrio con patrón radial) o cocolito, girando despacio."""
    tipo = seed % 3
    with lz.grupo(x, y, s, t * 0.3 + seed):
        lz.halo(0, 0, 60, col, alfa=0.35, r0=0.3)
        if tipo == 0:
            lz.relleno(circulo(0, 0, 30, 30), col)
            for i in range(12):
                a = i / 12 * 2 * math.pi
                lz.trazo(np.array([[math.cos(a) * 8, math.sin(a) * 8], [math.cos(a) * 26, math.sin(a) * 26]]),
                         aclarar(col, 0.4), 3, afinar=False)
            lz.relleno(circulo(0, 0, 8, 14), aclarar(col, 0.5))
        elif tipo == 1:
            lz.relleno(rect_red(-40, -14, 80, 28, 14), col)
            for i in range(9):
                lz.trazo(np.array([[-32 + i * 8, -10], [-32 + i * 8, 10]]), aclarar(col, 0.35), 2.5, afinar=False)
        else:
            for i in range(8):
                a = i / 8 * 2 * math.pi
                lz.relleno(elipse(math.cos(a) * 18, math.sin(a) * 18, 12, 7, a, 14), aclarar(col, 0.2))
            lz.relleno(circulo(0, 0, 16, 20), col)
