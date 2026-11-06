# -*- coding: utf-8 -*-
"""euphoria_robots — vertical, estilo «Disección en vivo» (kit nucleo/diseccion.py, doc docs/estilo_diseccion.md).
Plano secuencia: todas las escenas usan `Mundo`, que dibuja el cuadro entero por tiempo global.
Cada MOMENTO es una función (lz, u, ctx) con u = segundos desde que empieza; PLAN (más abajo) los ancla a las palabras de la voz.
Grabaciones reales del Robotaller: capturas/*.mp4 (se graban cuando el motor tipo Euphoria esté en main; ver ESTADO.md).
Mientras no existan, `clip()` usa un respaldo SOLO para las hojas de prueba (nunca para el render: `RESPALDO_OK`)."""
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "nucleo"))
from escena_base import Escena  # noqa: E402  (activa el estilo de guion.py)
from motor import W, H, componer  # noqa: E402
from montaje_real import _Clip  # noqa: E402

import diseccion as D  # noqa: E402
import plano as PL  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
RESPALDO = os.path.join(AQUI, "..", "robotaller_n64", "medios", "token.mp4")
RESPALDO_OK = os.environ.get("FAB_RESPALDO") == "1"
_CLIPS = {}


def clip(nombre, seg, recorte=None):
    """Cuadro BGR de capturas/<nombre>.mp4 en el segundo `seg`; recorte = (x0, y0, x1, y1) en fracciones."""
    ruta = os.path.join(AQUI, "capturas", nombre + ".mp4")
    if not os.path.exists(ruta):
        if not RESPALDO_OK:
            raise FileNotFoundError(f"falta la grabación real {ruta}")
        ruta = RESPALDO
    if ruta not in _CLIPS:
        _CLIPS[ruta] = _Clip(ruta)
    f = _CLIPS[ruta].leer(seg)
    if recorte:
        h, w = f.shape[:2]
        x0, y0, x1, y1 = recorte
        f = f[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)]
    return f


# ------------------------------------------------------------------ momentos
SUELO = 1560


def suelo(lz, y=SUELO, col=(34, 24, 78), alfa=1.0):
    """Piso del laboratorio: losa de 2 tonos con borde de luz; llega a H+60 por los zooms."""
    with lz.capa(0):
        lz.relleno(np.array([[-60, y], [W + 60, y], [W + 60, H + 60], [-60, H + 60]]), col, alfa=alfa)
        lz.relleno(np.array([[-60, y], [W + 60, y], [W + 60, y + 8], [-60, y + 8]]), PL.aclarar(col, 0.35), alfa=alfa)
        for i in range(-2, 14):
            x = i * 110 + 40
            lz.relleno(np.array([[x, y + 8], [x + 4, y + 8], [x - 60, H + 60], [x - 64, H + 60]]), PL.aclarar(col, 0.12), alfa=0.5 * alfa)


def pip(lz, nombre, seg, u, t0=0.3, cy=770, w=880, h=500, rayos=0.0, barrido=None, recorte=None, etiqueta="GRABACIÓN REAL"):
    """La grabación real del taller en el centro de cada paso: lo que el diagrama explica, pasando de verdad."""
    k = D.rebote(D.pr(u, t0, t0 + 0.45))
    if k > 0.01:
        D.monitor(lz, clip(nombre, seg, recorte), W / 2, cy, w, h, u, rayos=rayos, barrido=barrido, k=k, etiqueta=etiqueta)


def tarjeta(lz, lineas, x, y, u, t0, w=860, px=40, fondo=(30, 22, 70)):
    """Tarjeta de fórmula: fondo oscuro de 2 tonos y líneas que aparecen una a una."""
    a = D.suave(D.pr(u, t0, t0 + 0.3))
    if a <= 0.01:
        return
    h = len(lineas) * px * 1.5 + px
    with lz.capa(2):
        lz.relleno(D.rrect(x, y + 10, w, h, 28), (6, 4, 24), alfa=0.4 * a)
        lz.relleno(D.rrect(x, y, w, h, 28), fondo, alfa=0.92 * a)
        lz.relleno(D.rrect(x - w / 2 + 8, y, 8, h - 40, 4), D.AMAR, alfa=a)
    for i, (txt, col) in enumerate(lineas):
        b = D.rebote(D.pr(u, t0 + 0.25 + 0.35 * i, t0 + 0.6 + 0.35 * i))
        PL.rotulo(lz, x, y - h / 2 + px * (1.2 + 1.5 * i), txt, px=px, k=b, color=col, sombra=0.3)


def m_gancho(lz, u, ctx):
    """Grabación real arriba con el barrido de rayos X; abajo el mismo muñeco cayendo, simulado."""
    sim = D.escenario("fuerte")
    D.manchas(lz, u, D.TONOS["gancho"])
    f = clip("caida", 3.0 + u, recorte=(0.2, 0.05, 0.8, 0.95))
    bar = D.suave(D.pr(u, 1.2, 3.4)) if u > 1.2 else None
    D.monitor(lz, f, W / 2, 560, 960, 860, u, barrido=bar, k=D.rebote(D.pr(u, 0, 0.45)))
    D.titular(lz, "NADIE LA DIBUJÓ", 1150, u, 0.5, px=104)
    D.kicker(lz, "0 ANIMACIONES", W / 2, 1262, u, 0.9, fondo=D.CORAL)
    suelo(lz)
    P = sim.en(max(0.0, u - 0.3))
    D.muneco(lz, P, W / 2 - 90, SUELO, s=4.2, rayos=D.suave(D.pr(u, 1.4, 2.4)) * 0.8, t=u, cara="x" if sim.dato(u - 0.3)["cae"] else "normal")


def m_verlet(lz, u, ctx):
    """El muñeco abierto: 7 puntos con nombre; la «memoria» de cada punto (dónde estaba) y la velocidad que sale sola."""
    D.manchas(lz, u, D.TONOS["verlet"])
    D.kicker(lz, "PASO 1", W / 2, 250, u, 0.0, fondo=D.TURQ)
    D.titular(lz, "VERLET", 380, u, 0.15, px=150)
    suelo(lz)
    t1, t2 = ctx["k"]("verlet_1"), ctx["k"]("verlet_2", "trapo") - 0.6
    sim = D.escenario("trapo", 6.0)
    tt = max(0.0, u - t2)
    P = sim.en(tt) if u > t2 else D.escenario("leve").en(0.0)
    ox, oy, s = W / 2, SUELO, 9.5
    if u < t1 or u > t2:
        pip(lz, "verlet", u, u, 0.5, rayos=D.suave(D.pr(u, 1.2, 2.0)) * 0.6)
    else:
        tarjeta(lz, [("x nuevo = x + (x − x antes)", D.PAPEL), ("+ gravedad · dt²", D.AMAR)], W / 2, 780, u, t1 + 0.1)
    if t1 < u < t2:                               # fantasma: dónde estaba hace un instante
        fant = D.escenario("leve").en(0.0) + [0, 0]
        dx = 9 * math.sin(u * 2.4)
        P = P + [[dx * 0.2, 0]]
        D.muneco(lz, fant + [[-dx * 0.25, 0]], ox, oy, s=s, rayos=1.0, alfa=0.25 * D.suave(D.pr(u, t1, t1 + 0.4)), t=u)
    Q = D.muneco(lz, P, ox, oy, s=s, rayos=D.suave(D.pr(u, 0.3, 1.0)), etiquetas=D.pr(u, 0.6, 2.0) * (u < t2 - 0.2), t=u)
    if t1 + 0.2 < u < t2:
        cab = Q[D.CAB]
        D.flecha(lz, cab + [-40, -150], cab + [90, -150], D.AMAR, 20, D.suave(D.pr(u, t1 + 0.4, t1 + 0.9)))
        D.kicker(lz, "velocidad = ahora − antes", W / 2, 1010, u, t1 + 0.6, fondo=D.PAPEL, px=30)


def _deslizador(lz, x0, x1, y, val, u, t0):
    a = D.suave(D.pr(u, t0, t0 + 0.4))
    with lz.capa(2):
        lz.relleno(D.rrect((x0 + x1) / 2, y, x1 - x0, 18, 9), (60, 48, 120), alfa=a)
        lz.degradado(D.rrect(x0 + (x1 - x0) * val / 2, y, (x1 - x0) * val, 18, 9), D.CORAL, D.AMAR, (x0, y), (x1, y), alfa=a)
        xk = x0 + (x1 - x0) * val
        lz.halo(xk, y, 70, D.AMAR, alfa=0.5 * a)
        lz.relleno(D.circulo(xk, y, 26), D.PAPEL, alfa=a)
    PL.rotulo(lz, x0, y + 58, "0 · TRAPO", px=34, alfa=a)
    PL.rotulo(lz, x1, y + 58, "1 · ANIMACIÓN", px=34, alfa=a)


def m_musculos(lz, u, ctx):
    """Un deslizador de fuerza muscular de 0 a 1; el muñeco cambia de trapo a estatua y se queda en medio."""
    D.manchas(lz, u, D.TONOS["musculos"])
    D.kicker(lz, "PASO 2", W / 2, 250, u, 0.0, fondo=D.AMAR)
    D.titular(lz, "MÚSCULOS", 380, u, 0.15, px=140)
    suelo(lz)
    val = 0.5 + 0.5 * math.sin(u * 1.1 - 1.2) if u < 5.5 else 0.5 + 0.5 * (1 - D.suave(D.pr(u, 5.5, 6.3)))
    pip(lz, "musculos", u, u, 0.5, h=460)
    for i, (n, x) in enumerate((("trapo", 220), ("leve", 540), ("rigido", 860))):
        peso = (1 - val) if n == "trapo" else val if n == "rigido" else 1 - abs(val - 0.5) * 2
        sim = D.escenario(n)
        P = sim.en((u * 0.9) % 4.0)
        D.muneco(lz, P, x, SUELO, s=6.2, rayos=0.35, alfa=0.25 + 0.75 * peso, t=u + i)
    _deslizador(lz, 170, 910, 1720, val, u, 0.4)
    # resortes: líneas en zigzag del punto a su pose
    if u > 1.0:
        Q = D.escenario("leve").en(0.95) * 6.2 + [540, SUELO]
        T = (D.PARADO + [D.escenario("leve").en(0.95)[D.CAD, 0], 0]) * 6.2 + [540, SUELO]
        for i in (D.CAB, D.MI, D.MD):
            p0, p1 = Q[i], T[i]
            n = 9
            pts = [p0 + (p1 - p0) * k / n + (np.array([-(p1 - p0)[1], (p1 - p0)[0]]) / (np.linalg.norm(p1 - p0) + 1e-6)) * (7 if k % 2 else -7) * (0 < k < n)
                   for k in range(n + 1)]
            with lz.capa(2):
                lz.trazo(np.array(pts), D.AMAR + (200,), 3, afinar=False)


def m_equilibrio(lz, u, ctx):
    """Centro de masa, plomada y base de apoyo; empujón leve con paso de captura."""
    D.manchas(lz, u, D.TONOS["equilibrio"])
    D.kicker(lz, "PASO 3", W / 2, 250, u, 0.0, fondo=D.VERDE)
    D.titular(lz, "EQUILIBRIO", 380, u, 0.15, px=130)
    suelo(lz)
    sim = D.escenario("leve")
    tt = (u * 0.75) % 3.6
    P, d = sim.en(tt), sim.dato(tt)
    pip(lz, "equilibrio", u, u, 0.5, h=460, barrido=D.suave(D.pr(u, 1.5, 3.0)) if u > 1.5 else None)
    ox, s = W / 2 - 60, 8.6
    Q = D.muneco(lz, P, ox, SUELO, s=s, rayos=0.55, t=u)
    c = d["com"] * s + [ox, SUELO]
    D.punteada(lz, c, (c[0], SUELO - 6), fase=u * 40)
    dentro = abs(d["fuera"]) < 3
    D.base(lz, d["base"][0] * s + ox, d["base"][1] * s + ox, SUELO + 2, dentro)
    D.centro_masa(lz, c[0], c[1], 24, giro=u * 2)
    if 0.66 < tt < 1.15:
        D.flecha(lz, Q[D.PEC] + [-330, 0], Q[D.PEC] + [-120, 0], D.CORAL, 34, D.suave((tt - 0.66) / 0.12))
    PL.pastilla(lz, W / 2, 1740, "dentro: de pie" if dentro else "fuera: ¡un paso!", px=36, fondo=D.VERDE if dentro else D.CORAL, color=D.TINTA)


def m_error_vuela(lz, u, ctx):
    """El error real: la meta de las manos a 32 sobre el pecho con un brazo de 21; viaja con el cuerpo y lo saca volando."""
    D.manchas(lz, u, D.TONOS["errores"])
    if not ctx.get("teaser"):
        D.kicker(lz, "ERROR REAL · 5-NOV", W / 2, 250, u, 0.0, fondo=D.CORAL)
    sim = D.escenario("vuela")
    tt = max(0.0, u - 0.6)
    P = sim.en(tt)
    s = 9.0
    sube = -(P[D.PEC, 1] + 25)                    # unidades que ha subido
    rel = P - [0, P[D.PEC, 1] + 25] + [0, -min(sube, 30)]
    with lz.capa(0):                              # marcas de altura que bajan: el robot sube
        for i in range(-2, 22):
            y = (1600 - i * 120 + (sube * s) % 120)
            lz.relleno(np.array([[60, y], [130, y], [130, y + 6], [60, y + 6]]), D.PAPEL, alfa=0.3)
            lz.relleno(np.array([[W - 130, y], [W - 60, y], [W - 60, y + 6], [W - 130, y + 6]]), D.PAPEL, alfa=0.3)
    PL.pastilla(lz, W - 150, 470, f"altura +{max(0, int(sube))}", px=30, fondo=D.CORAL, color=D.TINTA, k=D.suave(D.pr(u, 1.0, 1.3)))
    Q = D.muneco(lz, rel, W / 2, 1380, s=s, rayos=0.7, t=u, cara="x")
    for m, sx in ((D.MI, -7), (D.MD, 7)):
        meta = Q[D.PEC] + np.array([sx, -32]) * s
        D.punteada(lz, Q[m], meta, col=D.CORAL, ancho=4, fase=u * 60)
        with lz.capa(2):
            lz.halo(meta[0], meta[1], 60, D.CORAL, alfa=0.6)
            lz.relleno(D.circulo(meta[0], meta[1], 16), D.CORAL)
    if ctx.get("teaser"):
        D.titular(lz, "¿¿NADIE LO TOCÓ??", 1660, u, 0.9, px=96, col=D.CORAL)
        return
    D.titular(lz, "32 > 21", 1660, u, 0.3, px=150, col=D.CORAL)
    PL.pastilla(lz, W / 2, 1790, "la meta viaja con el cuerpo", px=34, fondo=D.PAPEL, color=D.TINTA, k=D.rebote(D.pr(u, 1.4, 1.8)))


from esc_cola import MOMENTOS, PLAN, T, momento_en, pinta  # noqa: E402,F401


class Mundo(Escena):
    def preparar(self):
        if self.idx != 0:
            return
        from esc_cola import T as TT
        for i, (t0, nom) in enumerate(PLAN[1:]):          # cada cambio de momento: barrido de aire
            self.ev(t0, "zas", 0.5, pan=(-0.3, 0.3)[i % 2])
        for clave, pal, nombre, vol in (("gancho_0", "caída", "plaf", .8), ("gancho_1", "volando", "boing", .6),
                                        ("verlet_2", "trapo", "plaf", .7), ("equilibrio_1", "paso", "paso", .7),
                                        ("equilibrio_3", "agarro", "clang", .6), ("mundo_0", "trampillas", "clang", .7),
                                        ("mundo_1", "chancla", "chanclazo", .8), ("errores_1", "llegar", "error", .6),
                                        ("errores_2", "orden", "acierto", .6), ("cierre_1", "tú", "acierto", .5)):
            self.ev(TT(clave, pal), nombre, vol)
        self.ev(0.2, "escaneo", 0.5)

    def render(self, lz, t):
        t0, nombre = momento_en(t)
        img = pinta(lz, nombre, t - t0, t)
        u = t - t0                                   # destello corto en cada cambio de momento
        if u < 0.12 and t > 0.5:
            img = np.clip(img + (0.12 - u) / 0.12 * 0.35, 0, 1)
        return img


from escena_base import TL  # noqa: E402

CLASES = {e["id"]: Mundo for e in TL["escenas"]}
