# -*- coding: utf-8 -*-
"""BAÚL ESPACIAL Kurzgesagt (12-oct-2026, nacido en `videos/dos_lunas/`): lunas con cráteres, asteroides, lunas que se
deforman y se rompen, planetas gigantes con bandas, anillos (continuos y de escombros), órbitas con estela, esfera de Hill,
puntos de Lagrange, Tierra con abultamientos de marea, flechas/reglas/etiquetas de diagrama, nebulosas y lluvia de rocas.

Todo se dibuja sobre el Lienzo (`lz`) en las coordenadas actuales (px de 1080p, o locales dentro de `lz.grupo`), en el estilo
de `plano.py`: solo rellenos planos, 2 tonos de sombra azul-violeta, borde de luz, nunca negro puro, sin contornos.
Convenciones: `ang_luz` = dirección HACIA la luz (rad; 0 = derecha, pi/2 = abajo, como en `plano.esfera`); `seed` fija los
detalles (cráteres, bandas) para que un cuerpo se vea igual en todos los cuadros; `rot` gira un cuerpo sobre su eje (cráteres
que dan la vuelta con foreshortening). Catálogo y firmas: `python nucleo/api_kz.py` -> docs/api_kz.md.

Fondos: `fondo_espacio(t, ...)` (degradado + nebulosa + estrellas con paralaje) y `nebulosa(lz, ...)` para nubes de color propias.
"""
import math

import numpy as np

import fondos as F
import plano as P
from motor import blob, circulo, clamp01, elipse, h01, lerp
from plano import SOMBRA, aclarar, esfera, mezcla, oscurecer

# ------------------------------------------------------------------ paletas de cuerpos rocosos / helados
# base, color de los «mares»/manchas grandes, tinte de cráter (se oscurece de la base)
CUERPOS = {
    "luna": dict(base=(204, 204, 222), mares=(150, 150, 182), n_mares=4, n_cr=11),
    "ceniza": dict(base=(152, 142, 166), mares=(118, 108, 136), n_mares=3, n_cr=12),
    "rojiza": dict(base=(214, 128, 96), mares=(176, 96, 78), n_mares=3, n_cr=9),
    "hielo": dict(base=(220, 236, 250), mares=(178, 206, 236), n_mares=4, n_cr=5, grietas=True),
    "volcanica": dict(base=(242, 212, 98), mares=(214, 140, 64), n_mares=6, n_cr=0, manchas=(120, 62, 52)),
    "mercurio": dict(base=(178, 160, 150), mares=(140, 124, 124), n_mares=2, n_cr=13),
    "oscura": dict(base=(96, 92, 128), mares=(74, 70, 106), n_mares=3, n_cr=10),
}


def _rot_pts(Pn, ang, x, y):
    c, s = math.cos(ang), math.sin(ang)
    return Pn @ np.array([[c, s], [-s, c]]) + np.array([x, y])


def _proy_esfera(lon, lat, rot):
    """(lon, lat) en la esfera -> (x, y) unitarios en pantalla y profundidad z (>0 = cara visible)."""
    l = lon + rot
    return math.cos(lat) * math.sin(l), -math.sin(lat), math.cos(lat) * math.cos(l)


def cuerpo_rocoso(lz, x, y, r, tipo="luna", seed=0, ang_luz=math.pi * 1.25, luz=1.0, rot=0.0, sombra=-0.15,
                  alfa=1.0, tinte=None, fase=None):
    """Luna / planeta enano / asteroide grande: disco con mares, cráteres (con borde de luz) que giran con `rot`, y 2 tonos de
    sombra. `sombra` = excentricidad del terminador de `plano.esfera` (-0.15 casi llena; 0 mitad; 0.6 creciente; 1 nueva).
    `luz` 0..1 apaga el cuerpo (0 = solo se intuye, luz cenicienta). `tinte`: color que sustituye a la base de la paleta.
    `fase` (0..1, fracción iluminada: 0 nueva, 0,5 cuarto, 1 llena) dibuja una FASE limpia: cuerpo a plena luz + sombra con
    terminador elíptico (la luz llega desde `ang_luz`) y un poco de luz cenicienta; ignora `sombra`."""
    pal = CUERPOS[tipo]
    base0 = tinte or pal["base"]
    noche = (52, 50, 92)
    base = mezcla(base0, noche, (1 - luz) * 0.82)
    mares = mezcla(pal["mares"], noche, (1 - luz) * 0.82)
    dx_l, dy_l = math.cos(ang_luz), math.sin(ang_luz)

    def contenido():
        # manchas grandes (mares): polígonos irregulares que se desplazan con la rotación
        for i in range(pal["n_mares"]):
            lon = h01(seed, i, 1) * 6.283 - 3.1416
            lat = (h01(seed, i, 2) - 0.5) * 1.5
            px, py, z = _proy_esfera(lon, lat, rot)
            if z < -0.35:
                continue
            tam = r * (0.2 + 0.28 * h01(seed, i, 3))
            B = blob(0, 0, tam, seed=seed * 7 + i, irr=0.32, n=40, lob=4)
            k = max(0.18, z)
            B = B * np.array([k, 1.0])
            ang = math.atan2(py, px)
            lz.relleno(_rot_pts(B, ang, x + px * r, y + py * r), mares, alfa=0.9 * alfa)
        # cráteres: elipse aplastada en la dirección radial (foreshortening)
        for i in range(pal["n_cr"]):
            lon = h01(seed, i, 11) * 6.283 - 3.1416
            lat = (h01(seed, i, 12) - 0.5) * 2.2
            px, py, z = _proy_esfera(lon, lat, rot)
            if z < 0.06:
                continue
            cr = r * (0.075 + 0.15 * h01(seed, i, 13) ** 1.4)
            ang = math.atan2(py, px)
            rx, ry = cr * (0.25 + 0.75 * z), cr
            cx, cy = x + px * r, y + py * r
            lz.relleno(elipse(cx - dx_l * cr * 0.18, cy - dy_l * cr * 0.18, rx, ry, ang, 24), aclarar(base, 0.5), alfa=0.95 * alfa)
            lz.relleno(elipse(cx + dx_l * cr * 0.1, cy + dy_l * cr * 0.1, rx * 0.88, ry * 0.88, ang, 24),
                       oscurecer(base, 0.3), alfa=alfa)
        # hielo: grietas largas; volcánica: manchas oscuras (calderas) con un punto de lava
        if pal.get("grietas"):
            for i in range(5):
                a0 = h01(seed, i, 21) * 6.283
                p0 = np.array([x + math.cos(a0) * r * 0.9, y + math.sin(a0) * r * 0.9])
                a1 = a0 + 2.2 + h01(seed, i, 22) * 1.6
                p1 = np.array([x + math.cos(a1) * r * 0.9, y + math.sin(a1) * r * 0.9])
                m = (p0 + p1) / 2 + np.array([h01(seed, i, 23) - 0.5, h01(seed, i, 24) - 0.5]) * r * 0.5
                lz.trazo(np.array([p0, m, p1]), (150, 112, 100), max(1.5, r * 0.025), afinar=True, temblor=0.0)
        if pal.get("manchas"):
            for i in range(7):
                lon = h01(seed, i, 31) * 6.283 - 3.1416
                lat = (h01(seed, i, 32) - 0.5) * 2.0
                px, py, z = _proy_esfera(lon, lat, rot)
                if z < 0.1:
                    continue
                cr = r * (0.05 + 0.05 * h01(seed, i, 33))
                lz.relleno(elipse(x + px * r, y + py * r, cr * (0.3 + 0.7 * z), cr, math.atan2(py, px), 20),
                           pal["manchas"], alfa=0.95 * alfa)
                lz.relleno(circulo(x + px * r, y + py * r, cr * 0.35, 12), (255, 170, 80), alfa=0.9 * alfa)

    if fase is not None:
        k = clamp01(fase)
        esfera(lz, x, y, r, base, ang_luz, fuerza=0, rim=0, contenido=contenido, alfa=alfa)
        if k < 0.995:
            C = circulo(x, y, r, 120)
            with lz.recorte(C):
                lz.relleno(P.terminador(x, y, r * 1.01, ang_luz, 1 - 2 * k), (24, 20, 66), alfa=0.86 * alfa)
        if k > 0.02:
            lz.relleno(P.borde_luz(x, y, r, ang_luz, 0.05 + 0.03 * k), aclarar(base0, 0.6), alfa=0.6 * alfa)
        return
    esfera(lz, x, y, r, base, ang_luz, sombra=sombra, fuerza=0.55 * luz + 0.3, rim=0.075 * luz, color_rim=aclarar(base0, 0.55),
           contenido=contenido, alfa=alfa)


def roca(lz, x, y, r, seed=0, rot=0.0, tipo="ceniza", ang_luz=math.pi * 1.25, luz=1.0, alargada=1.35):
    """Asteroide / luna-patata (Fobos, el visitante que pasa): polígono irregular con sombra y cráteres. Misma luz que `cuerpo_rocoso`."""
    pal = CUERPOS[tipo]
    base = mezcla(pal["base"], (52, 50, 92), (1 - luz) * 0.8)
    B = blob(0, 0, r, seed=seed, irr=0.26, n=48, lob=5) * np.array([alargada, 1.0])
    pts = _rot_pts(B, rot, x, y)
    lz.relleno(pts, base)
    with lz.recorte(pts):
        lz.relleno(terminador_gran(x, y, r * 1.6, ang_luz), SOMBRA, alfa=0.42 * luz + 0.15)
        for i in range(6):
            a = h01(seed, i, 1) * 6.283
            d = r * 0.65 * h01(seed, i, 2)
            cr = r * (0.1 + 0.16 * h01(seed, i, 3))
            cx, cy = x + math.cos(a) * d, y + math.sin(a) * d
            lz.relleno(elipse(cx - math.cos(ang_luz) * cr * 0.2, cy - math.sin(ang_luz) * cr * 0.2, cr, cr * 0.8, rot, 20),
                       aclarar(base, 0.3), alfa=0.85)
            lz.relleno(elipse(cx, cy, cr * 0.9, cr * 0.72, rot, 20), oscurecer(base, 0.22))


def terminador_gran(x, y, r, ang_luz):
    """Media luna de sombra (lado opuesto a la luz) para recortar sobre formas irregulares."""
    return P.terminador(x, y, r, ang_luz, 0.0)


# ------------------------------------------------------------------ luna que se deforma y se rompe (límite de Roche)
def luna_rota(lz, x, y, r, estira, ang, t, seed=0, tipo="luna", rompe=0.0, ang_luz=math.pi * 1.25):
    """Luna estirada por la marea hacia el planeta (`ang` = dirección del planeta). estira 0..1: elipse alargada con grietas de
    lava; rompe 0..1: se parte en pedazos que se separan en una cola hacia el planeta y se esparcen."""
    k = 1 + 0.9 * estira
    sy = 1 / (1 + 0.45 * estira)
    cuerpo_alfa = 1 - 0.65 * clamp01(rompe * 1.4)
    with lz.grupo(x, y, k, ang, sy):
        cuerpo_rocoso(lz, 0, 0, r, tipo, seed, ang_luz=ang_luz - ang, alfa=cuerpo_alfa, sombra=-0.1)
        if estira > 0.25:
            u = clamp01((estira - 0.25) / 0.75)
            for i in range(7):
                a0 = h01(seed, i, 41) * 6.283
                p0 = np.array([math.cos(a0), math.sin(a0)]) * r * (0.1 + 0.5 * h01(seed, i, 42))
                a1 = a0 + (h01(seed, i, 43) - 0.5) * 1.8
                p1 = p0 + np.array([math.cos(a1), math.sin(a1)]) * r * (0.35 + 0.5 * h01(seed, i, 44))
                with lz.recorte(circulo(0, 0, r, 64)):
                    m = (p0 + p1) / 2 + np.array([h01(seed, i, 45) - 0.5, h01(seed, i, 46) - 0.5]) * r * 0.35
                    lz.halo(m[0], m[1], r * 0.45, (255, 140, 60), alfa=0.30 * u, r0=0.1)
                    lz.trazo(np.array([p0, m, p1]), (255, 120, 50), max(2.0, r * 0.05 / k), afinar=True, temblor=0.0)
                    lz.trazo(np.array([p0, m, p1]), (255, 214, 130), max(1.0, r * 0.022 / k), afinar=True, temblor=0.0)
    if rompe > 0.01:
        u = clamp01(rompe)
        c, s = math.cos(ang), math.sin(ang)
        for i in range(16):
            d = r * (0.4 + (0.6 + 3.4 * h01(seed, i, 51)) * u)            # a lo largo del eje (hacia el planeta)
            lado = (h01(seed, i, 52) - 0.5) * r * 1.8 * (0.3 + u)
            px, py = x + c * d - s * lado, y + s * d + c * lado
            roca(lz, px, py, r * (0.1 + 0.18 * h01(seed, i, 53)) * (1 - 0.3 * u), seed=seed + i, rot=t * (0.5 + h01(seed, i, 54)) + i,
                 tipo="ceniza" if tipo == "luna" else tipo)
            lz.halo(px, py, r * 0.35, (255, 150, 70), alfa=0.25 * u * (1 - u) * 3, r0=0.1)


# ------------------------------------------------------------------ la Luna con sus dos caras
_MARES_VIS = [(-0.85, 0.38, 0.30), (-0.30, 0.50, 0.22), (0.25, 0.32, 0.30), (0.62, 0.08, 0.20), (-0.55, -0.12, 0.27),
              (0.05, -0.30, 0.24), (0.75, -0.35, 0.16), (-1.0, -0.2, 0.15), (0.35, 0.62, 0.14)]


def luna_dos_caras(lz, x, y, r, rot=0.0, ang_luz=math.pi * 1.25, alfa=1.0, panqueque=0.0, seed=1, sombra=-0.55):
    """La Luna con sus DOS caras: `rot`=0 enseña la visible (lisa, con grandes mares oscuros) y `rot`=pi la oculta (llena de cráteres,
    montañas y tierras altas claras = corteza gruesa). `panqueque` 0..1 resalta en la cara oculta la meseta que dejaría una luna
    pequeña aplastada (hipótesis de Jutzi y Asphaug, 2011). Misma luz y paleta que `cuerpo_rocoso(tipo='luna')`."""
    base = (204, 204, 222)
    mares = (146, 146, 180)
    alta = (226, 224, 236)
    dx_l, dy_l = math.cos(ang_luz), math.sin(ang_luz)

    def contenido():
        for lon, lat, tam in _MARES_VIS:
            px, py, z = _proy_esfera(lon, lat, rot)
            if z < -0.3:
                continue
            B = blob(0, 0, r * tam, seed=seed * 13 + int(lon * 10), irr=0.30, n=40, lob=4) * np.array([max(0.18, z), 1.0])
            lz.relleno(_rot_pts(B, math.atan2(py, px), x + px * r, y + py * r), mares, alfa=0.95 * alfa)
        # tierras altas de la cara oculta
        for lon, lat, tam in ((math.pi, 0.05, 0.62), (math.pi + 0.8, -0.35, 0.40), (math.pi - 0.8, 0.40, 0.42), (math.pi + 0.3, 0.7, 0.30)):
            px, py, z = _proy_esfera(lon, lat, rot)
            if z < -0.3:
                continue
            B = blob(0, 0, r * tam, seed=seed * 7 + int(lon * 10), irr=0.22, n=44, lob=3) * np.array([max(0.18, z), 1.0])
            lz.relleno(_rot_pts(B, math.atan2(py, px), x + px * r, y + py * r), alta, alfa=0.9 * alfa)
        # cráteres: pocos en la visible, muchísimos en la oculta
        for i in range(46):
            lonb = 0.0 if i < 8 else math.pi
            ancho = 2.6 if i < 8 else 3.1
            lon = lonb + (h01(seed, i, 61) - 0.5) * ancho
            lat = (h01(seed, i, 62) - 0.5) * 2.3
            px, py, z = _proy_esfera(lon, lat, rot)
            if z < 0.06:
                continue
            cr = r * (0.035 + 0.15 * h01(seed, i, 63) ** 1.7) * (0.7 if i < 8 else 1.0)
            ang = math.atan2(py, px)
            rx, ry = cr * (0.25 + 0.75 * z), cr
            cx, cy = x + px * r, y + py * r
            lz.relleno(elipse(cx - dx_l * cr * 0.18, cy - dy_l * cr * 0.18, rx, ry, ang, 24), aclarar(base, 0.5), alfa=0.95 * alfa)
            lz.relleno(elipse(cx + dx_l * cr * 0.1, cy + dy_l * cr * 0.1, rx * 0.88, ry * 0.88, ang, 24), oscurecer(base, 0.3),
                       alfa=alfa)
        # montañas de la cara oculta: lomos con lado de luz y lado de sombra
        for i in range(16):
            lon = math.pi + (h01(seed, i, 81) - 0.5) * 2.6
            lat = (h01(seed, i, 82) - 0.5) * 2.0
            px, py, z = _proy_esfera(lon, lat, rot)
            if z < 0.15:
                continue
            w = r * (0.05 + 0.06 * h01(seed, i, 83))
            cx, cy = x + px * r, y + py * r
            pts = np.array([[-w, w * 0.6], [0.0, -w * 1.1], [w, w * 0.6]])
            Q = _rot_pts(pts * np.array([max(0.3, z), 1.0]), 0.0, cx, cy)
            lz.relleno(Q, (238, 236, 246), alfa=0.95 * alfa)
            lz.relleno(np.array([[cx, cy - w * 1.1], [cx + w * max(0.3, z), cy + w * 0.6], [cx + w * 0.1, cy + w * 0.6]]),
                       oscurecer(base, 0.35), alfa=0.9 * alfa)
        if panqueque > 0.01:
            px, py, z = _proy_esfera(math.pi + 0.25, 0.12, rot)
            if z > -0.2:
                B = blob(0, 0, r * 0.52, seed=seed * 5, irr=0.14, n=48, lob=3) * np.array([max(0.18, z), 1.0])
                Q = _rot_pts(B, math.atan2(py, px), x + px * r, y + py * r)
                lz.relleno(Q, (255, 250, 236), alfa=0.97 * panqueque * alfa)
                lz.relleno((Q - [x + px * r, y + py * r]) * 0.72 + [x + px * r, y + py * r], (240, 226, 206),
                           alfa=0.85 * panqueque * alfa)
                lz.trazo(np.vstack([Q, Q[:1]]), (255, 214, 90), max(3.0, r * 0.018), afinar=False, temblor=0.0)

    esfera(lz, x, y, r, base, ang_luz, sombra=sombra, fuerza=0.85, rim=0.075, color_rim=aclarar(base, 0.55), contenido=contenido,
           alfa=alfa)


# ------------------------------------------------------------------ planetas gigantes y anillos
GIGANTES = {
    "jupiter": [(222, 176, 128), (236, 214, 178), (186, 120, 92), (206, 152, 112)],
    "saturno": [(230, 208, 156), (212, 186, 134), (240, 226, 190), (196, 168, 120)],
    "hielo": [(110, 196, 226), (140, 214, 240), (86, 168, 210), (160, 224, 244)],
    "violeta": [(150, 110, 220), (186, 150, 240), (120, 84, 190), (206, 176, 250)],
    "rojizo": [(214, 100, 92), (240, 150, 120), (172, 70, 84), (250, 190, 150)],
}


def planeta_gas(lz, x, y, r, t=0.0, paleta="jupiter", seed=0, luz=1.0, ang_luz=math.pi * 1.25, tormenta=True, tilt=-0.2):
    """Gigante gaseoso genérico con bandas que ondulan. paleta: clave de GIGANTES o lista de 4 colores."""
    cols = GIGANTES[paleta] if isinstance(paleta, str) else paleta
    noche = (38, 36, 72)
    base = mezcla(cols[0], noche, (1 - luz) * 0.82)

    def contenido():
        n = 9
        for i in range(n):
            hh = -0.95 + 1.9 * (i + 0.5 * h01(seed, i, 1)) / n
            gr = 0.1 + 0.1 * h01(seed, i, 2)
            col = mezcla(cols[1 + i % 3], noche, (1 - luz) * 0.82)
            xs = np.linspace(-1.2 * r, 1.2 * r, 30)
            ond = r * 0.03 * np.sin(xs / (r * 0.35) + i * 1.7 + t * (0.25 + 0.1 * (i % 3)))
            top = np.stack([xs, hh * r - gr * r / 2 + ond], 1)
            bot = np.stack([xs[::-1], hh * r + gr * r / 2 + ond[::-1]], 1)
            lz.relleno(_rot_pts(np.concatenate([top, bot]), tilt, x, y), col, alfa=0.78)
        if tormenta:
            lz.relleno(elipse(x + r * 0.28, y + r * 0.33, r * 0.2, r * 0.11, tilt, 28), mezcla(cols[2], noche, (1 - luz) * 0.8))

    esfera(lz, x, y, r, base, ang_luz, sombra=-0.05, fuerza=0.55 * luz + 0.15, rim=0.07 * luz, color_rim=aclarar(cols[0], 0.5),
           contenido=contenido)


def anillo(lz, x, y, r_in, r_out, tilt=-0.25, incl=0.3, mitad=1, col=(226, 204, 150), alfa=1.0, bandas=3):
    """Anillo continuo de un planeta. mitad=0: la mitad de ATRÁS (dibújala antes del planeta); mitad=1: la de ADELANTE (después).
    incl = cociente eje menor/mayor (0 = visto de canto, 1 = de frente); tilt = giro en el plano de la imagen."""
    th = np.linspace(np.pi, 2 * np.pi, 56) if mitad == 0 else np.linspace(0, np.pi, 56)
    if incl > 0.97:
        th = np.linspace(0, 2 * np.pi, 96)

    def franja(a0, a1, col_, al):
        ext = np.stack([a1 * np.cos(th), a1 * incl * np.sin(th)], 1)
        inn = np.stack([a0 * np.cos(th[::-1]), a0 * incl * np.sin(th[::-1])], 1)
        lz.relleno(_rot_pts(np.concatenate([ext, inn]), tilt, x, y), col_, alfa=al * alfa)

    franja(r_in, r_out, col, 0.92)
    for b in range(bandas):
        f0 = r_in + (r_out - r_in) * (0.12 + 0.3 * b)
        franja(f0, f0 + (r_out - r_in) * (0.07 + 0.03 * (b % 2)), oscurecer(col, 0.35), 0.8)


def anillo_escombros(lz, x, y, r_in, r_out, t, n=120, seed=0, incl=0.3, tilt=-0.25, mitad=1, col=(176, 168, 190), tam=7.0,
                     vel=1.0, brillo=0.0):
    """Anillo de pedazos de roca que giran (ω ∝ ρ^-1,5, Kepler). mitad=0 atrás / 1 adelante (como `anillo`). brillo 0..1 añade
    un resplandor cálido (recién formado). Cada pedazo se ve distinto (tamaño, tono)."""
    for i in range(n):
        rho = r_in + (r_out - r_in) * h01(seed, i, 1)
        th = h01(seed, i, 2) * 6.283 + vel * 0.35 * (r_in / rho) ** 1.5 * t * 2.0
        sin_ = math.sin(th)
        if (sin_ >= 0) != (mitad == 1):
            continue
        px, py = rho * math.cos(th), rho * sin_ * incl
        q = _rot_pts(np.array([[px, py]]), tilt, x, y)[0]
        s = tam * (0.35 + 1.1 * h01(seed, i, 3) ** 2)
        c = mezcla(col, aclarar(col, 0.5), h01(seed, i, 4))
        if brillo > 0.01:
            lz.halo(q[0], q[1], s * 3.2, (255, 150, 70), alfa=0.28 * brillo, r0=0.1)
        lz.relleno(blob(q[0], q[1], s, seed=seed + i, irr=0.3, n=14, lob=4), c)


def lluvia_rocas(lz, t, cx, cy, R, n=26, seed=0, ciclo=1.6, largo=1.0):
    """Rocas que caen en línea recta hacia el centro del planeta (cx, cy, radio R) con cola incandescente al entrar."""
    for i in range(n):
        a = h01(seed, i, 1) * 6.283
        ph = (t / (ciclo * (0.7 + 0.6 * h01(seed, i, 2))) + h01(seed, i, 3)) % 1.0
        d0 = R * (2.6 + 2.0 * h01(seed, i, 4))
        d = lerp(d0, R * 1.0, ph ** 1.4)
        px, py = cx + math.cos(a) * d, cy + math.sin(a) * d
        cola = R * 0.45 * largo * (0.4 + ph)
        qx, qy = cx + math.cos(a) * (d + cola), cy + math.sin(a) * (d + cola)
        caliente = clamp01((ph - 0.55) / 0.4)
        col = mezcla((200, 190, 210), (255, 170, 80), caliente)
        lz.trazo(np.array([[qx, qy], [px, py]]), mezcla(col, (255, 110, 60), 0.4), 2 + 2 * h01(seed, i, 5), afinar=True,
                 temblor=0.0, capa=2)
        lz.halo(px, py, 9 + 12 * caliente, (255, 170, 80), alfa=0.35 + 0.4 * caliente, r0=0.1, capa=2)
        lz.relleno(circulo(px, py, 2.5 + 2.5 * h01(seed, i, 6), 10), aclarar(col, 0.4), capa=2)


# ------------------------------------------------------------------ órbitas, esfera de Hill, Lagrange
def pos_orbita(cx, cy, rx, ry=None, tilt=0.0, ang=0.0):
    """Punto de una órbita elíptica (centro, semiejes, giro) para el ángulo `ang` (rad). ry=None -> círculo."""
    ry = rx if ry is None else ry
    px, py = rx * math.cos(ang), ry * math.sin(ang)
    c, s = math.cos(tilt), math.sin(tilt)
    return cx + px * c - py * s, cy + px * s + py * c


def orbita(lz, cx, cy, rx, ry=None, tilt=0.0, color=(150, 170, 235), ancho=3.0, alfa=0.7, dash=True, frac=1.0, fase=0.0,
           capa=None):
    """Órbita elíptica. dash: línea discontinua que 'corre' con `fase` (px); frac<1 la dibuja solo en parte (se traza)."""
    ry = rx if ry is None else ry
    th = np.linspace(0, 2 * np.pi, 220)
    pts = np.stack([rx * np.cos(th), ry * np.sin(th)], 1)
    pts = _rot_pts(pts, -tilt, cx, cy)
    if dash:
        P.discontinua(lz, pts, mezcla(color, (255, 255, 255), 0.1), ancho, largo=max(10, ancho * 5), hueco=max(8, ancho * 4),
                      fase=fase, frac=frac, capa=capa)
    else:
        n = max(2, int(len(pts) * clamp01(frac)))
        lz.trazo(pts[:n], color, ancho, afinar=False, temblor=0.0, capa=capa)


def estela(lz, cx, cy, rx, ry, tilt, ang, color=(190, 205, 255), largo=1.1, ancho=11.0, sentido=1, n=22):
    """Cola luminosa que se desvanece detrás de un cuerpo que va por la órbita (en `ang`), hacia atrás `largo` rad."""
    ry = rx if ry is None else ry
    for k in range(n):
        u0, u1 = k / n, (k + 1) / n
        a0, a1 = ang - sentido * largo * u0, ang - sentido * largo * u1
        p0, p1 = pos_orbita(cx, cy, rx, ry, tilt, a0), pos_orbita(cx, cy, rx, ry, tilt, a1)
        lz.trazo(np.array([p0, p1]), mezcla(color, (20, 20, 60), u0 * 0.85), max(1.0, ancho * (1 - u0 * 0.9)),
                 afinar=False, temblor=0.0)


def esfera_hill(lz, x, y, r, t, color=(120, 160, 255), alfa=1.0):
    """Esfera de Hill / zona de influencia: disco translúcido con borde discontinuo que respira y destellos en el borde."""
    resp = 1 + 0.012 * math.sin(t * 1.6)
    lz.halo(x, y, r * 1.08 * resp, color, alfa=0.22 * alfa, r0=0.82)
    lz.relleno(circulo(x, y, r * resp, 140), color, alfa=0.09 * alfa)
    th = np.linspace(0, 2 * np.pi, 200)
    P.discontinua(lz, np.stack([x + r * resp * np.cos(th), y + r * resp * np.sin(th)], 1), aclarar(color, 0.35), 4.0, largo=26,
                  hueco=18, fase=t * 30)


def punto_lagrange(lz, x, y, nombre, t, s=1.0, color=(255, 214, 90), alfa=1.0, rotulo=True, lado=1):
    """Marca de punto de equilibrio (L4/L5...): rombo que pulsa con halo y su nombre."""
    pul = 0.75 + 0.25 * math.sin(t * 3.0)
    lz.halo(x, y, 34 * s * pul, color, alfa=0.45 * alfa, r0=0.2)
    d = 12 * s
    lz.relleno(np.array([[x, y - d], [x + d, y], [x, y + d], [x - d, y]]), color, alfa=alfa)
    lz.relleno(np.array([[x, y - d * 0.45], [x + d * 0.45, y], [x, y + d * 0.45], [x - d * 0.45, y]]), (255, 250, 220), alfa=alfa)
    if rotulo:
        P.rotulo(lz, x + lado * 30 * s, y - 22 * s, nombre, px=int(36 * s), color=aclarar(color, 0.25), alfa=alfa)


def triangulo_equilibrio(lz, a, b, c, t, color=(255, 214, 90), alfa=1.0, frac=1.0):
    """Triángulo equilátero punteado Tierra–Luna–L4/L5 (a, b, c son puntos (x, y))."""
    ptsl = [np.array(a), np.array(b), np.array(c), np.array(a)]
    seg = []
    for p, q in zip(ptsl[:-1], ptsl[1:]):
        seg.append((p, q))
    tot = sum(np.linalg.norm(q - p) for p, q in seg)
    rec = tot * clamp01(frac)
    for p, q in seg:
        L = np.linalg.norm(q - p)
        u = clamp01(rec / max(L, 1e-6))
        rec = max(0.0, rec - L)
        if u > 0.001:
            P.discontinua(lz, np.array([p, p + (q - p) * u]), color, 3.0, largo=16, hueco=12, fase=t * 20)


# ------------------------------------------------------------------ mareas
def abultamiento_marea(lz, x, y, r, lunas, amp=0.22, color=(76, 164, 246), alfa=0.95):
    """Capa de agua de la Tierra deformada por una o varias lunas: lunas = [(ang, fuerza)] (ang = dirección a la luna, fuerza 0..1+).
    Dibujar ANTES de la Tierra (`plano.tierra`/`tierra_marea`). Las fuerzas se suman como tirones semidiurnos (cos 2θ), así que dos
    lunas a 90° se anulan y a 0°/180° se suman."""
    th = np.linspace(0, 2 * np.pi, 180, endpoint=False)
    f = np.zeros_like(th)
    for ang, fz in lunas:
        f += fz * np.cos(2 * (th - ang))
    R = r * (1.0 + amp * f)
    pts = np.stack([x + R * np.cos(th), y + R * np.sin(th)], 1)
    lz.halo(x, y, r * 1.6, color, alfa=0.25 * alfa, r0=0.62)
    lz.relleno(pts, color, alfa=alfa)
    lz.relleno((pts - [x, y]) * 0.985 + [x, y], mezcla(color, (40, 122, 226), 0.55), alfa=alfa)


def tierra_marea(lz, x, y, r, t, lunas, rot=0.0, luz=1.0, ang_luz=math.pi, amp=0.2):
    """La Tierra con su agua deformada hacia/contra cada luna (ver `abultamiento_marea`)."""
    lz.halo(x, y, r * 1.45, (110, 190, 255), alfa=0.32 * luz, r0=0.7)
    abultamiento_marea(lz, x, y, r, lunas, amp)
    P.tierra(lz, x, y, r * 0.985, t, rot=rot, ang_luz=ang_luz, luz=luz, atmosfera=0.0)


def flecha(lz, p0, p1, color=(255, 255, 255), ancho=5.0, frac=1.0, alfa=1.0, cabeza=None, capa=None):
    """Flecha de p0 a p1 (se dibuja hasta `frac`). La cabeza mide `cabeza` px (por defecto 3.2×ancho)."""
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    q = p0 + (p1 - p0) * clamp01(frac)
    L = np.linalg.norm(q - p0)
    if L < 2:
        return
    u = (q - p0) / L
    ch = (cabeza or ancho * 3.2)
    ch = min(ch, L * 0.7)
    base = q - u * ch
    lz.trazo(np.array([p0, base + u * 1.0]), color, ancho, afinar=False, temblor=0.0, capa=capa)
    nv = np.array([-u[1], u[0]])
    lz.relleno(np.array([q, base + nv * ch * 0.55, base - nv * ch * 0.55]), color, alfa=alfa, capa=capa)


def flechas_marea(lz, x, y, r, ang, fuerza=1.0, color=(255, 214, 90), t=0.0):
    """Par de flechas del tirón de marea (lado cercano más fuerte, lado lejano más débil) hacia la luna en la dirección `ang`."""
    c, s = math.cos(ang), math.sin(ang)
    pul = 0.9 + 0.1 * math.sin(t * 4)
    for lado, fz in ((1, 1.0), (-1, 0.55)):
        a = np.array([x + lado * c * r * 1.08, y + lado * s * r * 1.08])
        b = a + np.array([lado * c, lado * s]) * r * 0.55 * fuerza * fz * pul
        flecha(lz, a, b, color, ancho=6.0 * (0.6 + 0.4 * fuerza), capa=2)


# ------------------------------------------------------------------ diagramas
def regla(lz, p0, p1, texto, color=(255, 255, 255), px=34, alfa=1.0, frac=1.0, lado=1, fondo=None):
    """Cota de distancia con topes en los extremos y pastilla con el texto a la mitad (ej. «384 400 km»)."""
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    q = p0 + (p1 - p0) * clamp01(frac)
    d = q - p0
    L = np.linalg.norm(d)
    if L < 4:
        return
    n = np.array([-d[1], d[0]]) / L
    lz.trazo(np.array([p0, q]), color, 3.5, afinar=False, temblor=0.0)
    for p in (p0, q):
        lz.trazo(np.array([p - n * 12, p + n * 12]), color, 3.5, afinar=False, temblor=0.0)
    if frac > 0.55:
        m = (p0 + q) / 2 + n * 30 * lado
        P.pastilla(lz, m[0], m[1], texto, px=px, fondo=fondo or (255, 255, 255), alfa=alfa * clamp01((frac - 0.55) * 4))


def etiqueta(lz, x, y, texto, dx=80.0, dy=-70.0, px=34, color=(255, 255, 255), fondo=None, alfa=1.0, frac=1.0):
    """Rótulo con línea de llamada desde un cuerpo en (x, y): pastilla en (x+dx, y+dy)."""
    P.linea_llamada(lz, (x, y), (x + dx, y + dy), frac=frac, col=color, ancho=3.0, alfa=0.9 * alfa)
    if frac > 0.6:
        P.pastilla(lz, x + dx, y + dy, texto, px=px, fondo=fondo or (255, 255, 255),
                   alfa=alfa * clamp01((frac - 0.6) * 4))


# ------------------------------------------------------------------ fondos
def fondo_espacio(t, brillo=1.0, dx=0.0, dy=0.0, tono=0):
    """Fondo de espacio (degradado noche->violeta + nebulosa + estrellas titilantes con paralaje dx/dy en px)."""
    return F.espacio(t, tono=tono, brillo_est=brillo, dx=dx, dy=dy)


def nebulosa(lz, x, y, r, color=(160, 90, 220), seed=0, alfa=0.5, capa=0):
    """Nube de gas de color propia (varios halos desplazados). Úsala sobre el fondo, antes de los cuerpos."""
    for i in range(6):
        a = h01(seed, i, 1) * 6.283
        d = r * 0.5 * h01(seed, i, 2)
        c = mezcla(color, (90, 200, 230) if i % 2 else (230, 120, 190), 0.35 * h01(seed, i, 3))
        lz.halo(x + math.cos(a) * d, y + math.sin(a) * d, r * (0.6 + 0.5 * h01(seed, i, 4)), c, alfa=alfa * 0.6, r0=0.0,
                dureza=1.4, capa=capa)


def destello(lz, x, y, r, t, color=(255, 255, 255), alfa=1.0, capa=2):
    """Estrella de 4 puntas que centellea (para brillos, descubrimientos, remates)."""
    k = 0.75 + 0.25 * math.sin(t * 6)
    R = r * k
    lz.halo(x, y, R * 1.6, color, alfa=0.45 * alfa, r0=0.1, capa=capa)
    pts = []
    for i in range(8):
        rr = R if i % 2 == 0 else R * 0.16
        a = i * math.pi / 4 - math.pi / 2
        pts.append([x + rr * math.cos(a), y + rr * math.sin(a)])
    lz.relleno(np.array(pts), color, alfa=alfa, capa=capa)


# ---------------------------------------------------------------- utilidades de trayectoria y marcas (de videos/dos_lunas, 13-oct-2026)
def fantasma(lz, x, y, r, t, alfa=1.0):
    """Cuerpo hipotético: disco translúcido con contorno punteado que corre."""
    lz.relleno(circulo(x, y, r, 48), (255, 255, 255), alfa=0.14 * alfa)
    th_ = np.linspace(0, 2 * np.pi, 72)
    P.discontinua(lz, np.stack([x + r * np.cos(th_), y + r * np.sin(th_)], 1), (255, 255, 255), 3.0, 12, 10, fase=t * 25)


def marca_x(lz, x, y, s=1.0, k=1.0, color=(255, 90, 110)):
    """✗ roja (entra con rebote: k es la escala)."""
    if k <= 0.01:
        return
    d = 22 * s * k
    for a, b in (((-d, -d), (d, d)), ((-d, d), (d, -d))):
        lz.trazo(np.array([[x + a[0], y + a[1]], [x + b[0], y + b[1]]]), color, 9 * s * min(k, 1.0), afinar=False, temblor=0.0)


def bez2(p0, p1, p2, u):
    """Bézier cuadrática (p. ej. aproximación de un asteroide hasta el periapsis antes de pasar a `kepler`)."""
    return (1 - u) ** 2 * np.asarray(p0, float) + 2 * (1 - u) * u * np.asarray(p1, float) + u * u * np.asarray(p2, float)


def kepler(a, e, w, M):
    """Posición relativa al foco para la anomalía media M (periapsis en el ángulo w; sentido horario en pantalla)."""
    E_ = M
    for _ in range(7):
        E_ = E_ - (E_ - e * math.sin(E_) - M) / (1 - e * math.cos(E_))
    x = a * (math.cos(E_) - e)
    y = a * math.sqrt(1 - e * e) * math.sin(E_)
    c, s_ = math.cos(w), math.sin(w)
    return np.array([x * c - y * s_, x * s_ + y * c])


def trail(lz, f, t, dur=0.5, n=12, color=(255, 255, 255), ancho=7.0):
    """Estela de un objeto cuya posición en pantalla es f(tt), afinándose hacia atrás. f debe valer también para tiempos
    anteriores (si no, salen tramos rectos raros)."""
    pts = [np.asarray(f(t - dur * k / n), float) for k in range(n + 1)]
    for k in range(n):
        u = k / n
        lz.trazo(np.array([pts[k], pts[k + 1]]), mezcla(color, (30, 30, 80), u * 0.8), max(1.0, ancho * (1 - u)),
                 afinar=False, temblor=0.0)


__all__ = ["CUERPOS", "GIGANTES", "cuerpo_rocoso", "roca", "luna_rota", "luna_dos_caras", "planeta_gas", "anillo", "anillo_escombros",
           "lluvia_rocas", "pos_orbita", "orbita", "estela", "esfera_hill", "punto_lagrange", "triangulo_equilibrio",
           "abultamiento_marea", "tierra_marea", "flecha", "flechas_marea", "regla", "etiqueta", "fondo_espacio", "nebulosa", "destello",
           "fantasma", "marca_x", "bez2", "kepler", "trail"]
