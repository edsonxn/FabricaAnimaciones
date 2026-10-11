# -*- coding: utf-8 -*-
"""Mundos y utilería PROPIOS de «¿Puede una IA guardar un secreto?» (LogIA, noir). Ningún elemento viene de otro video: solo se
reutilizan primitivas del kit (K.pared, K.plano_, K.puerta, K.hoja, K.robot, K.medidor, K.barra, K.flecha, C.banda, N.*)."""
import math

import numpy as np

import comun as C
import kit27 as K
import noir as N
from motor import H, W
from toon import elipse_


def rect(x0, y0, x1, y1):
    return np.array([[x0, y0], [x1, y0], [x1, y1], [x0, y1]], float)


def lerp(a, b, s):
    return (a[0] + (b[0] - a[0]) * s, a[1] + (b[1] - a[1]) * s)


# ================================================================== MUNDOS
def oficina_noche(h, t, sem=200):
    """Despacho de noche: pared de ladrillo, ventana con persiana y lluvia fuera, escritorio con flexo encendido."""
    K.pared(h, 56, 10, ladrillo=True, sem=sem)
    V = rect(1180, 110, 1720, 640)
    K.plano_(h, V, 120, sem + 1)
    h.luz_fija(V, 0.95)
    h.luz_persiana(V, k=0.75, tipo="persiana", n=14, abierto=0.45)
    h.trazo(np.array([[1180, 110], [1720, 110], [1720, 640], [1180, 640], [1180, 110]], float), 10, sem + 2, jit=0.5)
    N.lluvia(h, t, n=240, caja=(1180, 110, 1720, 640), k=0.9)
    D = rect(120, 760, 1500, 1080)
    h.pieza(D, 84, sem + 3, w=6, luz=(-0.4, -1), d=24, sombra=0.6, trama=0.7)
    h.trazo(np.array([[120, 760], [1500, 760]], float), 8, sem + 4, jit=0.4)
    # flexo: pantalla, brazo y la luz que cae sobre el escritorio
    h.pieza(np.array([[420, 470], [560, 470], [520, 560], [460, 560]], float), 232, sem + 5, w=5, luz=(0, -1), d=8, sombra=0.3)
    h.trazo(np.array([[490, 560], [490, 760]], float), 9, sem + 5, jit=0.4)
    h.luz_cono(490, 580, math.pi / 2, 0.55, 1200, (1.6, 1.5, 1.35), k=1.0, suave=0.5)
    h.luz_radial(490, 720, 520, (1.0, 0.95, 0.85), k=0.9)
    N.motas(h, t, n=60, k=0.5, sem=sem + 50)
    h.ambiente[:] = 0.22
    return h


def pasillo_puerta(h, t, sem=300):
    """Pasillo largo de servidores que se pierde al fondo. Al final, una puerta de acero con una rendija de luz: la puerta trasera."""
    fuga = (960.0, 540.0)
    h.luz_radial(960, 540, 900, (0.9, 0.9, 0.9), k=0.7)
    K.plano_(h, np.array([[-400, -400], [W + 400, -400], [1140, 380], [780, 380]], float), 34, sem)            # techo
    K.plano_(h, np.array([[-400, H + 400], [W + 400, H + 400], [1140, 600], [780, 600]], float), 64, sem + 1)  # suelo
    K.plano_(h, np.array([[-400, -400], [780, 380], [780, 600], [-400, H + 400]], float), 50, sem + 2)        # pared izquierda
    K.plano_(h, np.array([[W + 400, -400], [1140, 380], [1140, 600], [W + 400, H + 400]], float), 50, sem + 3)  # derecha
    # armarios de servidor: paneles en perspectiva sobre las dos paredes
    for k in range(7):
        s0, s1 = 0.08 + k * 0.12, 0.08 + k * 0.12 + 0.055
        a0, a1 = lerp((-400, -400), (780, 380), s0), lerp((-400, -400), (780, 380), s1)
        b0, b1 = lerp((-400, H + 400), (780, 600), s0), lerp((-400, H + 400), (780, 600), s1)
        Q = np.array([a0, a1, b1, b0], float)
        h.pieza(Q, 62 + 4 * (k % 2), sem + 10 + k, w=3, luz=(0.6, -0.2), d=6, sombra=0.4, trama=0.3)
        c0, c1 = lerp((W + 400, -400), (1140, 380), s0), lerp((W + 400, -400), (1140, 380), s1)
        d0, d1 = lerp((W + 400, H + 400), (1140, 600), s0), lerp((W + 400, H + 400), (1140, 600), s1)
        h.pieza(np.array([c0, c1, d1, d0], float), 62 + 4 * ((k + 1) % 2), sem + 20 + k, w=3, luz=(-0.6, -0.2), d=6, sombra=0.4, trama=0.3)
    # la puerta del fondo
    K.plano_(h, rect(780, 380, 1140, 600), 60, sem + 4)
    K.puerta(h, 880, 380, 160, 220, sem=sem + 5, rendija=0.0, tono=30, t=t, abre=0.0)
    h.luz_radial(960, 430, 180, (1.0, 1.0, 1.0), k=0.6)
    N.motas(h, t, n=80, k=0.6, sem=sem + 60)
    h.ambiente[:] = 0.2
    return h


def sala_interrogatorio(h, t, sem=400):
    """Sala de interrogatorio: pared de ladrillo, espejo de dos caras en el fondo, mesa de metal y una bombilla colgante."""
    K.pared(h, 36, 10, ladrillo=True, sem=sem)
    espejo_unidireccional(h, 1200, 150, 520, 420, sem=sem + 1)
    K.plano_(h, rect(-300, 930, W + 300, H + 300), 28, sem + 2)
    # mesa: tablero en perspectiva y frente
    h.pieza(np.array([[520, 800], [1400, 800], [1480, 860], [440, 860]], float), 74, sem + 3, w=6, luz=(-0.2, -1), d=18, sombra=0.5, trama=0.6)
    h.pieza(rect(440, 860, 1480, 900), 42, sem + 4, w=5, luz=(-0.2, -1), d=10, sombra=0.4, trama=0.4)
    # bombilla colgante: cable, pantalla y foco de luz sobre la mesa
    h.trazo(np.array([[960, -60], [960, 120]], float), 6, sem + 5, jit=0.3)
    K.plano_(h, elipse_(960, 150, 34, 22, n=24), 236, sem + 6)
    h.luz_cono(960, 150, math.pi / 2, 0.62, 1300, (1.8, 1.7, 1.5), k=1.0, suave=0.5)
    h.luz_radial(960, 820, 620, (1.0, 0.95, 0.9), k=0.8)
    N.motas(h, t, n=70, k=0.5, sem=sem + 60)
    h.ambiente[:] = 0.16
    return h


def dos_cuartos(h, t, sem=500):
    """Dos habitaciones separadas por una pared: a la izquierda, una sala iluminada con cámara; a la derecha, una sala a oscuras."""
    # sala vigilada (izquierda): más clara, cámara en el techo
    K.plano_(h, rect(-100, -100, 960, H + 100), 70, sem)
    K.plano_(h, rect(-100, 820, 960, H + 100), 96, sem + 1)
    h.luz_cono(480, -220, math.pi / 2, 0.78, 1700, (1.35, 1.35, 1.35), k=1.0, suave=0.5)
    # sala privada (derecha): casi negra, un foco lejano
    K.plano_(h, rect(960, -100, W + 100, H + 100), 14, sem + 2)
    K.plano_(h, rect(960, 840, W + 100, H + 100), 20, sem + 3)
    h.luz_cono(1440, -160, math.pi / 2, 0.22, 1000, (0.8, 0.8, 0.8), k=1.0, suave=0.5)
    # un haz que se desplaza despacio por la sala vigilada
    h.luz_cono(480 + 140 * math.sin(t * 0.35), -220, math.pi / 2 + 0.06 * math.sin(t * 0.3), 0.5, 1500, (0.7, 0.7, 0.7), k=1.0, suave=0.5)
    N.motas(h, t, n=90, k=0.6, sem=sem + 60)
    # tabique entre las dos
    K.plano_(h, rect(944, -100, 976, H + 100), 8, sem + 4)
    h.ambiente[:] = 0.18
    return h


def pasillo_alfombra(h, t, sem=600):
    """Pasillo de madera con una alfombra vieja en el centro; la alfombra se levanta en una esquina."""
    K.plano_(h, np.array([[-400, -400], [W + 400, -400], [W + 400, 500], [-400, 500]], float), 44, sem)          # pared del fondo
    K.plano_(h, np.array([[-400, H + 400], [W + 400, H + 400], [W + 400, 480], [-400, 480]], float), 72, sem + 1)  # suelo
    for k in range(9):                                                                                       # tablas del suelo
        y = 520 + k * 62
        h.trazo(np.array([[-200, y], [W + 200, y]], float), 4, sem + 2 + k, jit=0.2, alfa=0.55)
    h.luz_radial(960, 380, 900, (1.0, 1.0, 1.0), k=0.5)
    N.motas(h, t, n=60, k=0.5, sem=sem + 60)
    h.ambiente[:] = 0.24
    return h


# ================================================================== UTILERÍA
def columna_ia(h, x, y, s=1.0, luz=1.0, sem=900):
    """La IA del caso: una columna de cristal oscuro y alta, con un núcleo de luz que late dentro. La careta se pone en la cara
    (zona alta). Base en (x, y); mide 520·s hacia arriba. `luz` 0..1 apaga el núcleo (sala privada)."""
    h.pieza(rect(x - 110 * s, y - 520 * s, x + 110 * s, y), 46, sem, w=7, luz=(-0.3, -1), d=16, sombra=0.5, trama=0.4, rim=0.6)
    h.pieza(elipse_(x, y - 520 * s, 110 * s, 34 * s, n=32), 84, sem + 1, w=6, luz=(0, -1), d=6, sombra=0.3, trama=0.2)
    h.pieza(elipse_(x, y, 110 * s, 22 * s, n=32), 30, sem + 2, w=6, luz=(0, -1), d=4, sombra=0.2, trama=0.2)
    K.plano_(h, rect(x - 56 * s, y - 470 * s, x + 56 * s, y - 70 * s), int(120 + 110 * luz), sem + 3)
    for k in range(1, 9):
        yy = y - 470 * s + k * 50 * s
        h.trazo(np.array([[x - 56 * s, yy], [x + 56 * s, yy]], float), 3, sem + 4, color=(60, 60, 60), alfa=0.5, jit=0.1)
    h.luz_radial(x, y - 280 * s, 340 * s, (1.0, 1.0, 1.0), k=0.9 * luz)
    return h


def espejo_unidireccional(h, x, y, w, hh, sem=700):
    """Espejo de dos caras: marco de madera oscura y vidrio con un reflejo que se corre despacio."""
    h.pieza(rect(x - 16, y - 16, x + w + 16, y + hh + 16), 26, sem, w=6, luz=(-0.3, -1), d=10, sombra=0.5, trama=0.4)
    K.plano_(h, rect(x, y, x + w, y + hh), 64, sem + 1)
    h.trazo(np.array([[x + w * 0.22, y + hh * 0.08], [x + w * 0.44, y + hh * 0.92]], float), 26, sem + 2, color=(70, 70, 70), alfa=0.35, jit=0.2)
    h.trazo(np.array([[x + w * 0.58, y + hh * 0.05], [x + w * 0.66, y + hh * 0.85]], float), 10, sem + 3, color=(70, 70, 70), alfa=0.25, jit=0.2)
    return h


def camara_vigilancia(h, x, y, s=1.0, encendida=1.0, sem=720):
    """Cámara de vigilancia de pared: cuerpo, objetivo y un piloto que se apaga cuando la cámara deja de mirar."""
    h.pieza(rect(x - 70 * s, y - 36 * s, x + 50 * s, y + 36 * s), 60, sem, w=5, luz=(-0.4, -1), d=12, sombra=0.5, trama=0.4)
    h.pieza(elipse_(x + 80 * s, y, 40 * s, 40 * s, n=24), 36, sem + 1, w=5, luz=(-0.4, -1), d=8, sombra=0.5, trama=0.3)
    K.plano_(h, elipse_(x + 92 * s, y, 18 * s, 18 * s, n=16), 14 + int(200 * encendida), sem + 2)
    if encendida > 0.5:
        h.luz_radial(x + 92 * s, y, 60 * s, (1.0, 1.0, 1.0), k=0.8 * encendida)
    return h


def careta(h, x, y, s=1.0, sem=760):
    """Careta blanca de sonrisa fija, con dos cuencas oscuras. Se pega sobre el visor del robot en la sala vigilada."""
    h.pieza(elipse_(x, y, 150 * s, 186 * s, n=40), 236, sem, w=7, luz=(-0.3, -1), d=12, sombra=0.5, trama=0.2)
    for dx in (-58, 58):
        K.plano_(h, elipse_(x + dx * s, y - 22 * s, 30 * s, 22 * s, n=18), 12, sem + 1)
    sonrisa = np.array([[x - 90 * s, y + 60 * s], [x - 40 * s, y + 96 * s], [x + 40 * s, y + 96 * s], [x + 90 * s, y + 60 * s]], float)
    h.trazo(sonrisa, 9 * s, sem + 2, jit=0.3, taper=(0.2, 0.2))
    return h


def burbuja(h, x, y, w, hh, sem=780):
    """Globo de diálogo: rectángulo redondeado claro con su colita hacia abajo. El texto se escribe dentro con N.texto_maquina."""
    h.pieza(rect(x - w / 2, y - hh / 2, x + w / 2, y + hh / 2), 236, sem, w=6, luz=(0, -1), d=10, sombra=0.35, trama=0.3)
    h.pieza(np.array([[x - 40, y + hh / 2 - 6], [x - 110, y + hh / 2 + 70], [x + 10, y + hh / 2 - 6]], float), 236, sem + 1,
            w=6, luz=(0, -1), d=6, sombra=0.3, trama=0.2)
    return h


def alfombra(h, x0, x1, y0, y1, levanta=0.0, sem=800):
    """Alfombra gastada. Con levanta > 0 se dobla una esquina y deja ver el suelo oscuro debajo, con dos luces que miran."""
    K.plano_(h, rect(x0, y0, x1, y1), 124, sem)
    K.plano_(h, rect(x0 + 60, y0 + 50, x1 - 60, y1 - 50), 100, sem + 1)
    h.trazo(np.array([[x0 + 60, y0 + 50], [x1 - 60, y0 + 50], [x1 - 60, y1 - 50], [x0 + 60, y1 - 50], [x0 + 60, y0 + 50]], float),
            5, sem + 2, jit=0.4, alfa=0.7)
    if levanta > 0:
        doblez = np.array([[x0, y0], [x0 + 380 * levanta, y0 + 60 * levanta], [x0 + 300 * levanta, y0 + 240 * levanta], [x0, y0 + 200]], float)
        K.plano_(h, doblez, 10, sem + 3)                                  # hueco negro bajo la alfombra
        h.pieza(doblez, 110, sem + 4, w=6, luz=(0.3, -1), d=18, sombra=0.5, trama=0.6)
        for k in range(2):
            ex = x0 + 120 + 80 * levanta * k
            K.plano_(h, elipse_(ex, y0 + 110, 10, 7, n=14), 250, sem + 5)
            h.luz_radial(ex, y0 + 110, 56, (1.0, 1.0, 1.0), k=0.9 * levanta)
    return h
