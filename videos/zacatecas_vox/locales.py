# -*- coding: utf-8 -*-
"""Escenografía LOCAL de Zacatecas (unidades locales: 1 unidad = 1 px cuando la cámara local vale 1).
Origen (0, 0) = suelo del valle al pie de la Bufa. y crece hacia abajo (el cielo es y < 0).
Todo se dibuja con `lz` ya dentro del grupo de escala local (ver escenas.py)."""
import math

import numpy as np

import vox as V
from motor import prog, e_out, e_back, e_inout, h01, r1, clamp01, lerp, rect_red, smooth

# ------------------------------------------------------------------ terreno
def h(x):
    """Altura del suelo llano (y). Todo el mundo camina sobre este plano; los cerros son telón de fondo."""
    x = np.asarray(x, float)
    return 5 * np.sin(x / 83.0) + 3 * np.sin(x / 31.0 + 1.0)


def montes(x):
    """Perfil de los cerros (y; negativo = hacia arriba): la Bufa a la derecha, el Grillo a la izquierda."""
    x = np.asarray(x, float)
    b = -720 * np.exp(-((x - 900) / 270) ** 2) - 180 * np.exp(-((x - 640) / 190) ** 2)
    g = -430 * np.exp(-((x + 1100) / 300) ** 2) - 130 * np.exp(-((x + 800) / 200) ** 2)
    lejos = -110 * np.exp(-((x - 2600) / 320) ** 2) - 190 * np.exp(-((x - 4000) / 430) ** 2)
    lejos += -150 * np.exp(-((x + 2500) / 380) ** 2) - 90 * np.exp(-((x - 1700) / 300) ** 2)
    return b + g + lejos - 14 * np.sin(x / 61.0) * 0.4


def perfil(x0, x1, paso=24.0):
    xs = np.arange(x0, x1 + paso, paso)
    return xs, montes(xs)


ROJIZO = (190, 122, 86)
ROJIZO_OSC = (150, 92, 68)
OCRE_SUELO = (204, 160, 104)
CIELO = dict(
    alba=((252, 196, 128), (252, 232, 196)),
    dia=((150, 196, 222), (238, 240, 226)),
    tarde=((246, 174, 116), (252, 226, 176)),
    noche=((36, 40, 92), (120, 92, 130)),
    humo=((196, 176, 150), (230, 214, 190)),
)


def cielo(lz, hora, alfa=1.0, y0=-5000, y1=160, x0=-9000, x1=9000):
    """Cielo: rectángulo de papel de color con degradado (capa 0). `hora` = (c_arriba, c_abajo) o clave de CIELO."""
    a, b = CIELO[hora] if isinstance(hora, str) else hora
    with lz.capa(0):
        lz.degradado(np.array([[x0, y0], [x1, y0], [x1, y1], [x0, y1]]), a, b, (0, -1500), (0, 100), alfa=alfa)


def sol(lz, x, y, r, t, alfa=1.0, color=(252, 214, 96)):
    lz.halo(x, y, r * 2.6, (255, 226, 140), alfa=0.45 * alfa, capa=0)
    lz.relleno(V.elipse_pts(x, y, r, r, 0, 48), color, temblor=0.0, capa=0, alfa=alfa)


def nube(lz, x, y, s, color=(252, 248, 240), capa=1, alfa=1.0, seed=0):
    with lz.grupo(x, y, s):
        for dx, dy, rx, ry in ((-60, 8, 52, 30), (0, -6, 70, 42), (62, 8, 50, 30), (0, 14, 110, 26)):
            lz.relleno(V.elipse_pts(dx, dy, rx, ry), color, temblor=0.0, capa=capa, seed=seed, alfa=alfa)


def colinas_fondo(lz, cam_x, prof, base, alt, seed, color, x0=-1800, x1=1800, alfa=1.0, capa=0, cam_y=0.0, paso=150.0):
    """Capa de cerros lejanos ANGULOSOS (recortes) con paralaje: prof 0..1 (1 = se mueve con el mundo)."""
    dx = cam_x * (1 - prof)
    dy = cam_y * (1 - prof)
    xs = np.arange(x0, x1 + paso, paso)
    hs = np.array([0.25 + 0.75 * h01(int(seed * 10), i) ** 1.3 for i in range(len(xs))])
    ys = base - alt * hs
    P = np.vstack([np.stack([xs + dx, ys + dy], 1), [[x1 + dx, base + 900 + dy], [x0 + dx, base + 900 + dy]]])
    lz.relleno(P, color, temblor=0.0, capa=capa, alfa=alfa)


BUFA = np.array([(430, 20), (500, -60), (548, -150), (600, -200), (640, -330), (700, -360), (742, -470), (800, -520),
                 (838, -640), (900, -700), (940, -780), (972, -720), (1012, -742), (1060, -660), (1090, -560),
                 (1150, -480), (1190, -360), (1250, -300), (1310, -180), (1380, -110), (1450, 20)], float)
BUFA_SOMBRA = np.array([(940, -780), (972, -720), (1012, -742), (1060, -660), (1090, -560), (1150, -480), (1190, -360),
                        (1250, -300), (1310, -180), (1380, -110), (1450, 20), (1120, 20), (1060, -200), (1000, -460)], float)
BUFA_CRESTA = np.array([(900, -700), (940, -780), (972, -720), (1012, -742), (1030, -690), (980, -672), (930, -676)], float)
GRILLO = np.array([(-1500, 20), (-1430, -90), (-1380, -160), (-1320, -250), (-1260, -300), (-1200, -400), (-1130, -430),
                   (-1090, -360), (-1040, -330), (-980, -240), (-930, -190), (-880, -120), (-820, -70), (-760, 20)], float)
GRILLO_SOMBRA = np.array([(-1130, -430), (-1090, -360), (-1040, -330), (-980, -240), (-930, -190), (-880, -120), (-820, -70),
                          (-760, 20), (-1040, 20), (-1100, -180)], float)


def mesa(lz, x, ancho, alto, seed, alfa=1.0, claro=ROJIZO, capa=1):
    """Mesa/cerro suelto de bordes rectos (para el paisaje del camino)."""
    w = ancho / 2
    P = np.array([[x - w * 1.3, 20], [x - w, -alto * 0.55], [x - w * 0.55, -alto], [x + w * 0.4, -alto * 0.94],
                  [x + w * 0.9, -alto * 0.5], [x + w * 1.3, 20]])
    P = V.corte(P, seed, 6.0, 2)
    lz.relleno(P, claro, temblor=0.0, capa=capa, alfa=alfa)
    lz.relleno(np.array([[x + w * 0.4, -alto * 0.94], [x + w * 0.9, -alto * 0.5], [x + w * 1.3, 20], [x + w * 0.1, 20],
                         [x + w * 0.05, -alto * 0.5]]), ROJIZO_OSC, temblor=0.0, capa=capa, alfa=alfa)


def subsuelo_base(lz, alfa=1.0):
    """Tierra oscura bajo el mundo (y > 420)."""
    lz.relleno(np.array([[-9000, 420], [12000, 420], [12000, 9000], [-9000, 9000]]), (74, 56, 56), temblor=0.0, capa=1, alfa=alfa)


def montaña_bufa(lz, alfa=1.0, capa=1, detalle=1.0):
    """Bufa y cerro del Grillo como recortes angulosos de papel (telón de fondo del valle)."""
    for P, sombra, c_luz, c_som in ((GRILLO, GRILLO_SOMBRA, (206, 142, 104), (170, 108, 82)),
                                    (BUFA, BUFA_SOMBRA, (204, 134, 96), (160, 96, 72))):
        lz.relleno(V.corte(P, 5, 2.5, 2), c_luz, temblor=0.0, capa=capa, alfa=alfa, seed=5)
        lz.relleno(sombra, c_som, temblor=0.0, capa=capa, alfa=alfa)
        if detalle > 0.5:
            V.semitono(lz, sombra, (128, 74, 58), esp=30, r=4.2, ang=0.5, capa=capa)
    lz.relleno(BUFA_CRESTA, (226, 176, 136), temblor=0.0, capa=capa, alfa=alfa)
    lz.relleno(np.array([[972, -720], [1012, -742], [1030, -690], [1000, -684]]), (150, 90, 68), temblor=0.0, capa=capa, alfa=alfa)
    for i in range(60):
        x = -2400 + i * 90 + 40 * h01(4, i)
        lz.relleno(V.elipse_pts(x, 10, 22, 11), (150, 158, 96), temblor=0.0, capa=capa, alfa=alfa * 0.9)


def suelo(lz, x0, x1, grosor=130, alfa=1.0, color=OCRE_SUELO):
    """Plano de tierra: banda clara (donde caminan) + cuerpo de roca hasta el borde inferior del mundo local."""
    xs = np.arange(x0, x1 + 40, 40.0)
    ys = h(xs)
    P = np.vstack([np.stack([xs, ys], 1), [[x1, grosor], [x0, grosor]]])
    lz.relleno(P, color, temblor=0.0, capa=1, alfa=alfa)
    lz.relleno(np.array([[x0, grosor - 2], [x1, grosor - 2], [x1, 424], [x0, 424]]), (168, 106, 80), temblor=0.0, capa=1, alfa=alfa)


# ------------------------------------------------------------------ construcciones
ADOBE = (206, 158, 108)
ADOBE_OSC = (170, 122, 84)
TEJA = (186, 84, 62)
PIEDRA = (218, 206, 184)
PIEDRA_OSC = (176, 162, 140)
MADERA = (120, 84, 56)
PAJA = (222, 184, 92)


def _pop(k):
    return 0.0 if k <= 0 else (e_back(clamp01(k), 1.7) if k < 1 else 1.0)


def tienda(lz, x, y, s=1.0, k=1.0, seed=0, capa=1):
    k = _pop(k)
    if k <= 0.01:
        return
    with lz.grupo(x, y, s, sy=s * k):
        lz.relleno(np.array([[-52, 0], [0, -84], [52, 0]]), (240, 230, 206), temblor=0.0, capa=capa, seed=seed)
        lz.relleno(np.array([[0, -84], [52, 0], [14, 0]]), (206, 190, 160), temblor=0.0, capa=capa)
        lz.relleno(np.array([[-8, 0], [0, -34], [10, 0]]), (60, 44, 40), temblor=0.0, capa=capa)
        lz.trazo(np.array([[0, -84], [0, -104]]), MADERA, 5, afinar=False, temblor=0.0, capa=capa)
        lz.relleno(np.array([[0, -104], [26, -98], [0, -92]]), V.ROJO, temblor=0.0, capa=capa)


def choza(lz, x, y, s=1.0, k=1.0, seed=0, capa=1):
    k = _pop(k)
    if k <= 0.01:
        return
    with lz.grupo(x, y, s, sy=s * k):
        lz.relleno(V.corte([[-46, 0], [46, 0], [46, -52], [-46, -52]], seed, 1.5, 2), (176, 132, 90), temblor=0.0, capa=capa, seed=seed)
        for i in range(-3, 4):
            lz.trazo(np.array([[i * 13, 0], [i * 13, -52]]), MADERA, 3, afinar=False, temblor=0.0, capa=capa)
        lz.relleno(np.array([[-62, -48], [0, -104], [62, -48]]), PAJA, temblor=0.0, capa=capa)
        lz.relleno(np.array([[0, -104], [62, -48], [30, -48]]), V.oscurecer(PAJA, 0.14), temblor=0.0, capa=capa)
        lz.relleno(np.array([[-14, 0], [14, 0], [14, -32], [-14, -32]]), (56, 42, 38), temblor=0.0, capa=capa)


def casa_adobe(lz, x, y, s=1.0, k=1.0, seed=0, capa=1, humo=False, t=0.0):
    k = _pop(k)
    if k <= 0.01:
        return
    w = 58 + 8 * h01(seed, 1)
    hh = 78 + 12 * h01(seed, 2)
    with lz.grupo(x, y, s, sy=s * k):
        lz.relleno(V.corte([[-w, 0], [w, 0], [w, -hh], [-w, -hh]], seed, 1.8, 3), ADOBE, temblor=0.0, capa=capa, seed=seed)
        lz.relleno(np.array([[w, 0], [w, -hh], [w - 16, -hh], [w - 16, 0]]), ADOBE_OSC, temblor=0.0, capa=capa)
        for i in range(4):     # vigas que sobresalen
            lz.relleno(rect_red(-w + 8 + i * (2 * w - 16) / 3.6, -hh - 3, 12, 8, 3), MADERA, temblor=0.0, capa=capa)
        lz.relleno(np.array([[-w - 4, -hh], [w + 4, -hh], [w + 4, -hh - 9], [-w - 4, -hh - 9]]), ADOBE_OSC, temblor=0.0, capa=capa)
        lz.relleno(rect_red(-16, -46, 32, 46, 8), (54, 40, 38), temblor=0.0, capa=capa)
        lz.relleno(rect_red(w * 0.42, -hh * 0.72, 22, 22, 4), (54, 40, 38), temblor=0.0, capa=capa)


def casa_piedra(lz, x, y, s=1.0, k=1.0, seed=0, capa=1, pisos=1):
    k = _pop(k)
    if k <= 0.01:
        return
    w = 74 + 10 * h01(seed, 1)
    hh = 96 * pisos + 16
    with lz.grupo(x, y, s, sy=s * k):
        lz.relleno(V.corte([[-w, 0], [w, 0], [w, -hh], [-w, -hh]], seed, 1.6, 3), PIEDRA, temblor=0.0, capa=capa, seed=seed)
        lz.relleno(np.array([[w, 0], [w, -hh], [w - 18, -hh], [w - 18, 0]]), PIEDRA_OSC, temblor=0.0, capa=capa)
        lz.relleno(np.array([[-w - 8, -hh], [w + 8, -hh], [w - 8, -hh - 26], [-w + 8, -hh - 26]]), TEJA, temblor=0.0, capa=capa)
        for p in range(pisos):
            yy = -p * 96
            lz.relleno(rect_red(-w * 0.58, yy - 70, 24, 38, 10), (70, 52, 48), temblor=0.0, capa=capa)
            lz.relleno(rect_red(w * 0.22, yy - 70, 24, 38, 10), (70, 52, 48), temblor=0.0, capa=capa)
            if p == 0:
                lz.relleno(rect_red(-18, yy - 56, 36, 56, 16), (60, 44, 40), temblor=0.0, capa=capa)
            else:
                lz.relleno(rect_red(-w, yy - 4, 2 * w, 6, 2), (60, 44, 40), temblor=0.0, capa=capa)


def iglesia(lz, x, y, s=1.0, k=1.0, seed=0, capa=1):
    """Templo franciscano sencillo: nave, espadaña con campana y cruz."""
    k = _pop(k)
    if k <= 0.01:
        return
    with lz.grupo(x, y, s, sy=s * k):
        lz.relleno(V.corte([[-120, 0], [120, 0], [120, -170], [-120, -170]], seed, 1.5, 3), (232, 220, 196), temblor=0.0, capa=capa, seed=seed)
        lz.relleno(np.array([[120, 0], [120, -170], [98, -170], [98, 0]]), PIEDRA_OSC, temblor=0.0, capa=capa)
        lz.relleno(np.array([[-132, -170], [132, -170], [120, -196], [-120, -196]]), TEJA, temblor=0.0, capa=capa)
        # espadaña
        lz.relleno(np.array([[-46, -196], [46, -196], [46, -290], [0, -330], [-46, -290]]), (240, 230, 208), temblor=0.0, capa=capa)
        lz.relleno(rect_red(-16, -290, 32, 54, 14), (60, 44, 40), temblor=0.0, capa=capa)
        lz.relleno(V.elipse_pts(0, -262, 11, 13), (216, 170, 70), temblor=0.0, capa=capa)
        lz.trazo(np.array([[0, -330], [0, -368]]), MADERA, 6, afinar=False, temblor=0.0, capa=capa)
        lz.trazo(np.array([[-13, -352], [13, -352]]), MADERA, 6, afinar=False, temblor=0.0, capa=capa)
        lz.relleno(rect_red(-32, -110, 64, 110, 30), (62, 46, 42), temblor=0.0, capa=capa)
        lz.relleno(V.elipse_pts(-84, -110, 12, 22), (62, 46, 42), temblor=0.0, capa=capa)
        lz.relleno(V.elipse_pts(84, -110, 12, 22), (62, 46, 42), temblor=0.0, capa=capa)


def humo(lz, x, y, t, n=5, col=(214, 206, 196), esc=1.0, capa=2, alfa=0.7):
    for i in range(n):
        u = ((t * 0.35 + i / n) % 1.0)
        r = (10 + 30 * u) * esc
        lz.relleno(V.elipse_pts(x + 24 * math.sin(u * 6 + i) * u * esc, y - 130 * u * esc, r, r), col, temblor=0.0, capa=capa,
                   alfa=alfa * (1 - u) ** 0.8)


def fogata(lz, x, y, s=1.0, t=0.0, capa=1):
    with lz.grupo(x, y, s):
        lz.relleno(V.capsula([-24, 0], [24, -6], 9), MADERA, temblor=0.0, capa=capa)
        lz.relleno(V.capsula([-22, -6], [22, 0], 9), V.oscurecer(MADERA, 0.2), temblor=0.0, capa=capa)
        f = 1 + 0.12 * math.sin(t * 17) + 0.06 * math.sin(t * 29)
        lz.relleno(np.array([[-20, -6], [0, -52 * f], [20, -6]]), V.NARANJA, temblor=0.0, capa=capa)
        lz.relleno(np.array([[-10, -6], [2, -34 * f], [12, -6]]), V.AMARILLO, temblor=0.0, capa=capa)


def arroyo(lz, alfa=1.0, t=0.0, x0=-330, x1=-120, y0=-4, y1=340):
    """Arroyo (cinta azul que baja por el valle hacia el observador)."""
    xs = np.linspace(0, 1, 16)
    izq = [(lerp(x0, x1, u) - 26 - 16 * math.sin(u * 5), lerp(y0, y1, u)) for u in xs]
    der = [(lerp(x0, x1, u) + 26 + 16 * math.sin(u * 5), lerp(y0, y1, u)) for u in xs][::-1]
    lz.relleno(np.array(izq + der), (120, 176, 196), temblor=0.0, capa=1, alfa=alfa)


def barra_plata(lz, x, y, s=1.0, rot=0.0, capa=1, brillo=0.0, seed=0):
    with lz.grupo(x, y, s, rot):
        lz.relleno(np.array([[-46, -14], [46, -14], [58, 16], [-58, 16]]), V.PLATA, temblor=0.0, capa=capa, seed=seed)
        lz.relleno(np.array([[-46, -14], [46, -14], [42, -6], [-42, -6]]), V.aclarar(V.PLATA, 0.6), temblor=0.0, capa=capa)
        lz.relleno(np.array([[58, 16], [46, -14], [40, -14], [50, 16]]), V.PLATA_OSC, temblor=0.0, capa=capa)


def chispa(lz, x, y, r, t, seed=0, capa=2, color=(255, 255, 230), alfa=1.0):
    """Destello de 4 puntas (brillo de la plata)."""
    a = r * (0.7 + 0.3 * math.sin(t * 9 + seed))
    P = np.array([[0, -a], [a * 0.18, -a * 0.18], [a, 0], [a * 0.18, a * 0.18], [0, a], [-a * 0.18, a * 0.18], [-a, 0],
                  [-a * 0.18, -a * 0.18]])
    lz.relleno(P + [x, y], color, temblor=0.0, capa=capa, alfa=alfa)
