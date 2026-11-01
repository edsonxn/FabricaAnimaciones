# -*- coding: utf-8 -*-
"""Utilería PROPIA de «Las 1.200» (noir color). Todo se dibuja por cuadro con h.pieza / h.trazo / h.emitir en el MUNDO.

    candado · llave · llavero · ganzua · regalo · carpeta_tab (carpeta con el NOMBRE escrito en la pestaña) · sobre · reloj ·
    periodico (llega girando) · palanca (interruptor de cuchilla) · enchufe · capsula / tubo · contador (rodillos) · mazo ·
    captcha · portatil + chat · tarjeta (ficha de corcho) + hilo rojo · chincheta · mano (guante / piel) · vaso · servilleta ·
    boton_off · ficha_juego · pieza_ajedrez · busto_ciceron · juez (la máquina que evalúa) · robot_mesa (Bob y Alice) ·
    caja (de almacén) · cinta_policial · silueta_tiza · bombilla · lampara_mesa · telefono
"""
import math

import numpy as np

import noir as N
from motor import clamp01, e_out, smooth
from toon import blob, elipse_, suave, tubo, eje_curvo
from comun import rect, rot, T_obj, IMPACT

TIZA = "C:/Windows/Fonts/segoepr.ttf"         # tiza / letra a mano
TIZA_B = "C:/Windows/Fonts/segoeprb.ttf"


def plano_(h, P, tono, sem, alfa=1.0, rampa=None, grad=None):
    """Relleno liso sin tinta ni sombra."""
    h.pieza(P, tono, sem, w=0, luz=(0, -1), d=1, sombra=0, trama=0, linea=False, jit=0, alfa=alfa, rampa=rampa, grad=grad)


def rrect(x, y, w, hh, r, n=5):
    P = []
    for cx, cy, a0 in ((x + w - r, y + r, -math.pi / 2), (x + w - r, y + hh - r, 0), (x + r, y + hh - r, math.pi / 2),
                       (x + r, y + r, math.pi)):
        for a in np.linspace(a0, a0 + math.pi / 2, n):
            P.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return np.array(P)


def arco(cx, cy, r0, r1, a0, a1, n=24):
    a = np.linspace(a0, a1, n)
    ext = np.stack([cx + r1 * np.cos(a), cy + r1 * np.sin(a)], 1)
    inn = np.stack([cx + r0 * np.cos(a[::-1]), cy + r0 * np.sin(a[::-1])], 1)
    return np.vstack([ext, inn])


# ====================================================================== cerraduras y llaves
def candado(h, x, y, s=1.0, abierto=0.0, sem=0, ang=0.0, luz=(0.3, -1), brillo_ojo=0.0, rampa="laton"):
    """Candado (x, y = centro del cuerpo). abierto 0..1 sube y gira el arco. brillo_ojo: el ojo de la cerradura emite."""
    T = T_obj(x, y, ang, s)
    sube = 46 * e_out(clamp01(abierto))
    giro = 0.5 * clamp01(abierto - 0.4) / 0.6 if abierto > 0.4 else 0.0
    c = np.array([46.0, -60 - sube])
    A = arco(0, -60, 34, 50, math.pi, 2 * math.pi, 22) + (0, -sube)
    A = rot(A, giro, c)
    h.pieza(T(A), 170, sem, w=5 * s, luz=luz, d=6 * s, trama=0.2, rim=0.9, rampa="piedra")
    for sx in (-1, 1):
        if sx > 0 and abierto > 0.4:
            continue
        h.pieza(T(rot(rect(sx * 42 - 8, -64 - sube, 16, 34 + sube * (0 if sx > 0 else 1)), giro if sx < 0 else 0, c)), 160, sem + 5 + sx,
                w=4 * s, luz=luz, d=4 * s, trama=0.1, rim=0.8, rampa="piedra")
    h.pieza(T(rrect(-70, -66, 140, 130, 20)), 150, sem + 1, w=6 * s, luz=luz, d=16 * s, trama=0.5, rim=0.9, rampa=rampa)
    h.pieza(T(rrect(-56, -54, 112, 14, 6)), 200, sem + 2, w=0, luz=luz, d=1, sombra=0, trama=0, rim=0, alfa=0.5, rampa=rampa)
    ojo = suave([(-9, -22), (9, -22), (10, -6), (5, 0), (6, 30), (-6, 30), (-5, 0), (-10, -6)], 3)
    h.pieza(T(ojo), 12, sem + 3, w=2 * s, luz=luz, d=2, sombra=0, trama=0, rim=0, rampa=rampa)
    if brillo_ojo > 0:
        h.emitir(T(ojo), 1.2 * brillo_ojo, col=h.pal["verde"], blur=2)


def llave(h, x, y, s=1.0, ang=0.0, sem=0, luz=(0.3, -1), rampa="laton", tono=170):
    """Llave antigua (x, y = centro del ojo; la paleta apunta a +x)."""
    T = T_obj(x, y, ang, s)
    h.pieza(T(elipse_(0, 0, 34, 34, n=24)), tono, sem, w=4 * s, luz=luz, d=6 * s, trama=0.2, rim=0.9, rampa=rampa)
    h.pieza(T(elipse_(0, 0, 15, 15, n=16)), 14, sem + 1, w=2.5 * s, luz=luz, d=2, sombra=0, trama=0, rim=0, rampa=rampa)
    h.pieza(T(rect(30, -8, 150, 16)), tono - 10, sem + 2, w=4 * s, luz=luz, d=5 * s, trama=0.2, rim=0.9, rampa=rampa)
    h.pieza(T([(140, 6), (182, 6), (182, 44), (170, 44), (170, 30), (158, 30), (158, 40), (146, 40)]), tono - 10, sem + 3, w=4 * s,
            luz=luz, d=5 * s, trama=0.2, rim=0.9, rampa=rampa)


def llavero(h, x, y, s, t, sem=0, etiqueta="HF · ACCESO", n=3, balanceo=0.0, brillo=0.0):
    """Aro con n llaves colgando y una etiqueta de cartón con texto. (x, y) = arriba del aro."""
    a0 = 0.18 * math.sin(t * 2.2 + sem) * balanceo
    T = T_obj(x, y, a0, s)
    h.pieza(T(arco(0, 60, 50, 60, 0, 2 * math.pi, 40)), 180, sem, w=3 * s, luz=(0.3, -1), d=3, trama=0, rim=0.9, rampa="piedra")
    for k in range(n):
        a = math.pi / 2 + (k - (n - 1) / 2) * 0.45
        px, py = T(np.array([[60 * math.cos(a), 60 + 60 * math.sin(a)]]))[0]
        llave(h, px, py, s * 0.8, a0 + a, sem + 10 + k * 7, tono=150 + 20 * k)
    if etiqueta:
        px, py = T(np.array([[-52, 92]]))[0]
        Tt = T_obj(px, py, a0 + 0.5, s)
        h.pieza(Tt([(0, 0), (40, -24), (210, -24), (210, 24), (40, 24)]), 214, sem + 40, w=3 * s, luz=(0.3, -1), d=4, sombra=0.3, trama=0,
                rim=0.3, rampa="papel")
        N.soporte(h, *Tt(np.array([[118, 0]]))[0], 170, 46, a0 + 0.5, s)
        c = Tt(np.array([[118, 0]]))[0]
        N.texto_maquina(h, etiqueta, c[0], c[1], 22 * s, t, -99, cps=1e9, tono=0.05, centro=True, encuadrar=False)
    if brillo > 0:
        h.resplandor(x + 40 * s, y + 120 * s, 120 * s, 0.4 * brillo, col=h.pal["sodio"])


def ganzua(h, x, y, s=1.0, ang=0.0, sem=0, brillo=0.0):
    """Ganzúa de cerrajero (x, y = punta; el mango hacia -x)."""
    T = T_obj(x, y, ang, s)
    h.pieza(T([(0, -3), (-14, -10), (-26, -4), (-200, -5), (-200, 5), (-24, 4), (-12, 0)]), 200, sem, w=2.5 * s, luz=(0.3, -1), d=3,
            trama=0, rim=0.9, rampa="piedra")
    h.pieza(T(rrect(-300, -14, 110, 28, 10)), 60, sem + 1, w=3.5 * s, luz=(0.3, -1), d=5 * s, trama=0.3, rim=0.8, rampa="madera")
    if brillo > 0:
        h.emitir(T(rect(-200, -4, 196, 8)), 0.9 * brillo, col=h.pal["verde"], blur=2)


# ====================================================================== paquetes, carpetas y cartas
def regalo(h, x, y, s=1.0, abre=0.0, sem=0, ang=0.0, rayosx=0.0, t=0.0):
    """Caja de regalo con moño (x, y = base). abre 0..1 levanta la tapa. rayosx 0..1: se ve la ganzúa dentro (escáner)."""
    T = T_obj(x, y, ang, s)
    h.pieza(T(rect(-120, -170, 240, 170)), 170, sem, w=5 * s, luz=(0.3, -1), d=12 * s, trama=0.4, rim=0.7, rampa="papel",
            alfa=1 - 0.6 * rayosx)
    h.pieza(T(rect(-18, -170, 36, 170)), 120, sem + 1, w=3 * s, luz=(0.3, -1), d=4, trama=0.2, rim=0.5, rampa="vino",
            alfa=1 - 0.6 * rayosx)
    ty = -170 - 120 * e_out(clamp01(abre))
    ta = -0.5 * clamp01(abre)
    c = np.array([0.0, ty])
    h.pieza(T(rot(rect(-134, ty - 40, 268, 44), ta, c)), 184, sem + 2, w=5 * s, luz=(0.3, -1), d=8 * s, trama=0.3, rim=0.8,
            rampa="papel", alfa=1 - 0.6 * rayosx)
    for sx in (-1, 1):
        h.pieza(T(rot(suave([(0, ty - 38), (sx * 60, ty - 90), (sx * 90, ty - 60), (sx * 20, ty - 34)], 4), ta, c)), 130, sem + 3 + sx,
                w=4 * s, luz=(0.3, -1), d=5 * s, trama=0.2, rim=0.8, rampa="vino", alfa=1 - 0.6 * rayosx)
    if rayosx > 0:
        ganzua(h, *T(np.array([[60, -80]]))[0], s=0.9 * s, ang=ang + 0.3, sem=sem + 20, brillo=rayosx)


def carpeta_tab(h, cx, cy, s, titulo, t, t0=-99, ang=0.0, sem=0, cps=16.0, tono=150, vacia=True, px=30, brillo=0.0):
    """Carpeta de archivo con pestaña: el TÍTULO se escribe en la pestaña (el «nombre de carpeta» con el que se hablan)."""
    T = T_obj(cx, cy, ang, s)
    h.pieza(T([(-200, -130), (-200, 140), (200, 140), (200, -130)]), tono - 30, sem, w=4 * s, luz=(0.2, -1), d=8 * s, trama=0.3,
            rim=0.5, rampa="papel")
    tab = [(-190, -130), (-180, -180), (150, -180), (165, -130)]
    h.pieza(T(tab), tono + 30, sem + 1, w=4 * s, luz=(0.2, -1), d=6 * s, trama=0, rim=0.5, rampa="papel")
    h.pieza(T([(-200, -120), (200, -120), (210, 150), (-210, 150)]), tono, sem + 2, w=4 * s, luz=(0.2, -1), d=10 * s, trama=0.3,
            rim=0.6, rampa="papel")
    c = T(np.array([[-15, -155]]))[0]
    N.soporte(h, c[0], c[1], 330, 46, ang, s, margen=8)
    if t >= t0:
        N.texto_maquina(h, titulo, c[0], c[1], px * s, t, t0, cps=cps, tono=0.05, centro=True, encuadrar=False)
    if brillo > 0:
        h.resplandor(cx, cy, 260 * s, 0.25 * brillo, col=h.pal["verde"])


def sobre(h, cx, cy, s=1.0, ang=0.0, sem=0, abierto=0.0, texto="", lacre=False, tono=212, t=0.0):
    T = T_obj(cx, cy, ang, s)
    h.pieza(T(rect(-180, -110, 360, 220)), tono, sem, w=4 * s, luz=(0.2, -1), d=8 * s, trama=0.2, rim=0.4, rampa="papel")
    h.trazo(T(np.array([[-180, 110], [0, -10], [180, 110]])), 2.5 * s, sem + 1, alfa=0.5)
    sol = -110 - 150 * clamp01(abierto)
    h.pieza(T([(-180, -110), (180, -110), (0, sol + 150 + (0 if abierto <= 0 else -150 * abierto))]), tono - 20, sem + 2, w=3.5 * s,
            luz=(0.2, -1), d=4, trama=0.1, rim=0.4, rampa="papel")
    if lacre:
        h.pieza(T(blob(0, 26, 30, 28, n=10)), 110, sem + 3, w=3 * s, luz=(0.3, -1), d=4, trama=0, rim=0.7, rampa="vino")
    if texto:
        c = T(np.array([[0, 60]]))[0]
        N.soporte(h, c[0], c[1], 320, 60, ang, s)
        N.texto_maquina(h, texto, c[0], c[1], 24 * s, t, -99, cps=1e9, tono=0.06, centro=True, encuadrar=False)


def caja(h, x, y, s=1.0, sem=0, rotulo="", t=0.0, tono=120, ang=0.0, ancho=220, alto=160, candado_=False, abierto=0.0,
         rampa="madera"):
    """Caja de madera de almacén (x, y = base). Rótulo estarcido."""
    T = T_obj(x, y, ang, s)
    h.pieza(T(rect(-ancho / 2, -alto, ancho, alto)), tono, sem, w=4.5 * s, luz=(0.3, -1), d=10 * s, trama=0.4, rim=0.6, rampa=rampa)
    for k in range(1, 4):
        h.trazo(T(np.array([[-ancho / 2, -alto * k / 4], [ancho / 2, -alto * k / 4]])), 2 * s, sem + k, alfa=0.4)
    h.trazo(T(np.array([[-ancho / 2 + 8, -8], [ancho / 2 - 8, -alto + 8]])), 6 * s, sem + 5, alfa=0.55)
    if rotulo:
        c = T(np.array([[0, -alto * 0.55]]))[0]
        N.soporte(h, c[0], c[1], ancho * 0.9, 50, ang, s)
        N.texto_maquina(h, rotulo, c[0], c[1], 26 * s, t, -99, cps=1e9, tono=0.04, centro=True, fuente="C:/Windows/Fonts/STENCIL.TTF",
                        encuadrar=False)
    if candado_:
        p = T(np.array([[0, -alto * 0.18]]))[0]
        candado(h, p[0], p[1], 0.32 * s, abierto=abierto, sem=sem + 40, ang=ang)


# ====================================================================== tiempo
def reloj(h, cx, cy, r, hora, minuto, sem=0, t=0.0, luz=(0.3, -1), marco=60, esfera=226, segundero=True, numeros=True):
    """Reloj de pared. hora/minuto pueden ser decimales (las agujas giran continuas)."""
    h.pieza(elipse_(cx, cy, r * 1.12, r * 1.12, n=60), marco, sem, w=6, luz=luz, d=r * 0.08, trama=0.4, rim=0.9, rampa="madera")
    h.pieza(elipse_(cx, cy, r, r, n=60), esfera, sem + 1, w=4, luz=luz, d=r * 0.05, trama=0, rim=0, sombra=0.25, rampa="papel")
    for k in range(60):
        a = k / 60 * 2 * math.pi - math.pi / 2
        r0 = r * (0.84 if k % 5 == 0 else 0.92)
        h.trazo(np.array([[cx + r0 * math.cos(a), cy + r0 * math.sin(a)], [cx + r * 0.96 * math.cos(a), cy + r * 0.96 * math.sin(a)]]),
                (r * 0.035 if k % 5 == 0 else r * 0.012), sem + 2 + k, jit=0.1, taper=(0, 0))
    if numeros:
        for k in (12, 3, 6, 9):
            a = (k % 12) / 12 * 2 * math.pi - math.pi / 2
            N.texto_maquina(h, str(k), cx + r * 0.68 * math.cos(a), cy + r * 0.68 * math.sin(a), r * 0.2, t, -99, cps=1e9, tono=0.06,
                            centro=True, fuente="C:/Windows/Fonts/BOD_B.TTF", encuadrar=False)
    ah = ((hora % 12) + minuto / 60.0) / 12 * 2 * math.pi - math.pi / 2
    am = (minuto % 60) / 60 * 2 * math.pi - math.pi / 2
    for a, L, w_ in ((ah, r * 0.52, r * 0.07), (am, r * 0.8, r * 0.045)):
        P = np.array([[cx - math.cos(a) * r * 0.12, cy - math.sin(a) * r * 0.12], [cx + math.cos(a) * L, cy + math.sin(a) * L]])
        h.pieza(tubo(P, w_, w_ * 0.4), 18, sem + 70 + int(L), w=2, luz=luz, d=2, sombra=0, trama=0, rim=0.4, rampa="piedra")
    if segundero:
        a = (t % 60) / 60 * 2 * math.pi - math.pi / 2
        h.trazo(np.array([[cx, cy], [cx + math.cos(a) * r * 0.86, cy + math.sin(a) * r * 0.86]]), r * 0.012, sem + 90, color=(150, 30, 30),
                jit=0.1, taper=(0, 0))
    h.pieza(elipse_(cx, cy, r * 0.05, r * 0.05, n=12), 30, sem + 91, w=2, luz=luz, d=2, sombra=0, trama=0, rim=0.6, rampa="laton")


def periodico(h, t, t0, cx, cy, s, titular, sub="", sem=0, ang_fin=-0.06, dur=0.9, fecha="", lineas=10):
    """Periódico que llega girando desde el fondo (cine clásico) y se asienta. titular a toda la página."""
    u = clamp01((t - t0) / dur)
    if u <= 0:
        return
    e = e_out(u)
    z = 0.05 + 0.95 * e
    a = ang_fin + (1 - e) * 4 * math.pi
    T = T_obj(cx, cy, a, s * z)
    h.pieza(T(rect(-560, -380, 1120, 760)), 214, sem, w=5, luz=(0.2, -1), d=14, trama=0, rim=0.2, sombra=0.4, rampa="papel")
    h.pieza(T(rect(-530, -350, 1060, 70)), 212, sem + 1, w=0, d=0, sombra=0, trama=0, rim=0, rampa="papel")
    if z > 0.5:
        c0 = T(np.array([[0, -315]]))[0]
        N.soporte(h, cx, cy, 1120, 760, a, s * z)
        N.texto_maquina(h, "EL DIARIO DE LA BAHÍA" + (f"   ·   {fecha}" if fecha else ""), c0[0], c0[1], 40 * s * z, t, -99, cps=1e9,
                        tono=0.06, centro=True, fuente="C:/Windows/Fonts/OLDENGL.TTF", encuadrar=False)
        h.trazo(T(np.array([[-530, -272], [530, -272]])), 4 * s * z, sem + 2, alfa=0.9)
        c1 = T(np.array([[0, -180]]))[0]
        N.texto_maquina(h, titular, c1[0], c1[1], 110 * s * z, t, -99, cps=1e9, tono=0.04, centro=True, fuente=IMPACT, track=2,
                        encuadrar=False)
        if sub:
            c2 = T(np.array([[0, -80]]))[0]
            N.texto_maquina(h, sub, c2[0], c2[1], 36 * s * z, t, -99, cps=1e9, tono=0.08, centro=True, fuente="C:/Windows/Fonts/BOD_B.TTF",
                            encuadrar=False)
        r = np.random.default_rng(sem)
        for col in range(3):
            for k in range(lineas):
                y = -20 + k * 32
                L = 300 * r.uniform(0.7, 1.0)
                plano_(h, T(rect(-510 + col * 350, y, L, 8)), 110, sem + 10 + col * 20 + k, alfa=0.55, rampa="papel")
        plano_(h, T(rect(180, -20, 330, 300)), 90, sem + 90, alfa=0.85, rampa="papel")      # la «foto» de portada


# ====================================================================== electricidad
def palanca(h, cx, cy, s=1.0, pos=0.0, sem=0, rotulo="MAESTRO", t=0.0, luz=(0.3, -1)):
    """Interruptor de cuchilla en su tablero (pos 0 = arriba conectado .. 1 = abajo, cortado). Devuelve el puño de la palanca."""
    h.pieza(rect(cx - 220 * s, cy - 320 * s, 440 * s, 640 * s), 70, sem, w=7 * s, luz=luz, d=18 * s, trama=0.5, rim=0.8, rampa="piedra")
    for q in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        h.pieza(elipse_(cx + q[0] * 190 * s, cy + q[1] * 290 * s, 12 * s, 12 * s, n=10), 140, sem + 3 + q[0] + 2 * q[1], w=2.5 * s,
                luz=luz, d=3, trama=0, rim=0.8, rampa="piedra")
    for sx in (-1, 1):                                           # bornes de cobre arriba y bisagras abajo
        h.pieza(rect(cx + sx * 70 * s - 22 * s, cy - 250 * s, 44 * s, 80 * s), 150, sem + 10 + sx, w=4 * s, luz=luz, d=6 * s, trama=0.2,
                rim=0.9, rampa="laton")
        h.pieza(rect(cx + sx * 70 * s - 18 * s, cy + 120 * s, 36 * s, 70 * s), 130, sem + 14 + sx, w=4 * s, luz=luz, d=6 * s, trama=0.2,
                rim=0.9, rampa="laton")
    piv = np.array([cx, cy + 150 * s])
    a = -math.pi / 2 + math.pi * 0.62 * clamp01(pos)          # arriba = -90°, abajo ~ +22°
    L = 380 * s
    tip = piv + L * np.array([math.cos(a), math.sin(a)])
    for sx in (-1, 1):
        q = np.array([sx * 70 * s, 0])
        h.pieza(tubo(np.array([piv + q, tip + q]), 16 * s, 14 * s), 160, sem + 20 + sx, w=4 * s, luz=luz, d=5 * s, trama=0.2, rim=0.9,
                rampa="laton")
    h.pieza(tubo(np.array([tip - (90 * s, 0), tip + (90 * s, 0)]), 26 * s, 26 * s), 30, sem + 30, w=5 * s, luz=luz, d=8 * s, trama=0.3,
            rim=0.9, rampa="madera")
    if rotulo:
        c = np.array([cx, cy + 260 * s])
        h.pieza(rect(c[0] - 150 * s, c[1] - 26 * s, 300 * s, 52 * s), 200, sem + 40, w=3 * s, luz=luz, d=3, trama=0, rim=0, rampa="papel")
        N.texto_maquina(h, rotulo, c[0], c[1], 34 * s, t, -99, cps=1e9, tono=0.05, centro=True, fuente=IMPACT, encuadrar=False)
    return tip


def enchufe(h, x, y, s=1.0, fuera=0.0, ang=0.0, sem=0, cable_a=None, chispa=0.0):
    """Clavija de dos patas que sale (fuera 0..1) de un toma de pared (x, y = centro del toma; la clavija sale hacia -y local
    girado ang). cable_a = punto del mundo hacia donde va el cable."""
    T = T_obj(x, y, ang, s)
    h.pieza(T(rrect(-90, -110, 180, 220, 24)), 196, sem, w=5 * s, luz=(0.3, -1), d=8 * s, trama=0.2, rim=0.6, rampa="papel")
    for sx in (-1, 1):
        plano_(h, T(rect(sx * 30 - 7, -26, 14, 40)), 16, sem + 1 + sx)
    off = 260 * e_out(clamp01(fuera))
    for sx in (-1, 1):
        h.pieza(T(rect(sx * 30 - 6, -30 - off - 50, 12, 64)), 180, sem + 4 + sx, w=2.5 * s, luz=(0.3, -1), d=2, trama=0, rim=0.9,
                rampa="laton")
    h.pieza(T(rrect(-70, -150 - off - 60, 140, 110, 22)), 40, sem + 7, w=5 * s, luz=(0.3, -1), d=8 * s, trama=0.4, rim=0.9,
            rampa="piedra")
    base = T(np.array([[0, -170 - off - 60]]))[0]
    fin = np.asarray(cable_a, float) if cable_a is not None else T(np.array([[0, -900 - off]]))[0]
    mid = (base + fin) / 2 + np.array([120 * s, 0])
    h.pieza(tubo(np.vstack([eje_curvo(base, mid, 40, 10), eje_curvo(mid, fin, -40, 10)[1:]]), 22 * s, 22 * s), 34, sem + 8, w=4 * s,
            luz=(0.3, -1), d=5 * s, trama=0.2, rim=0.8, rampa="piedra")
    return T(np.array([[0, -30 - off]]))[0]


def capsula(h, x, y, s=1.0, ang=0.0, sem=0, rotulo="", t=0.0, brillo=0.0):
    """Cápsula de correo neumático (eje a lo largo de +x local)."""
    T = T_obj(x, y, ang, s)
    h.pieza(T(rrect(-90, -34, 180, 68, 30)), 150, sem, w=4 * s, luz=(0.3, -1), d=8 * s, trama=0.3, rim=0.9, rampa="laton")
    for xx in (-60, 60):
        plano_(h, T(rect(xx - 6, -34, 12, 68)), 60, sem + 1 + (xx > 0), rampa="laton")
    if rotulo:
        c = T(np.array([[0, 0]]))[0]
        N.texto_maquina(h, rotulo, c[0], c[1], 20 * s, t, -99, cps=1e9, tono=0.06, centro=True, encuadrar=False, ang=ang)
    if brillo > 0:
        h.resplandor(x, y, 120 * s, 0.35 * brillo, col=h.pal["verde"])


def tubo_neumatico(h, P, r=36, sem=0, vidrio=True, tono=90):
    """Tubo de correo neumático por la polilínea P (mundo): metal con abrazaderas, o vidrio (se ve la cápsula)."""
    P = np.asarray(P, float)
    if vidrio:
        h.pieza(tubo(P, r * 2, r * 2), 120, sem, w=3, luz=(0.3, -1), d=6, sombra=0.2, trama=0, rim=0.9, alfa=0.35, rampa="vidrio_verde")
    else:
        h.pieza(tubo(P, r * 2, r * 2), tono, sem, w=4, luz=(0.3, -1), d=10, trama=0.4, rim=0.85, rampa="laton")
    L = np.cumsum(np.r_[0, np.hypot(*np.diff(P, axis=0).T)])
    for k, d in enumerate(np.arange(60, L[-1], 220)):
        i = np.searchsorted(L, d) - 1
        i = max(0, min(len(P) - 2, i))
        u = (d - L[i]) / max(1e-6, L[i + 1] - L[i])
        c = P[i] + (P[i + 1] - P[i]) * u
        v = (P[i + 1] - P[i]) / (np.hypot(*(P[i + 1] - P[i])) + 1e-9)
        n = np.array([-v[1], v[0]])
        h.pieza(np.array([c - n * (r + 6) - v * 9, c + n * (r + 6) - v * 9, c + n * (r + 6) + v * 9, c - n * (r + 6) + v * 9]), 150,
                sem + 10 + k, w=2.5, luz=(0.3, -1), d=3, trama=0, rim=0.9, rampa="laton")


def punto_en(P, f):
    """Punto a la fracción f (0..1) de la longitud de la polilínea P, y su ángulo."""
    P = np.asarray(P, float)
    L = np.cumsum(np.r_[0, np.hypot(*np.diff(P, axis=0).T)])
    d = clamp01(f) * L[-1]
    i = max(0, min(len(P) - 2, int(np.searchsorted(L, d) - 1)))
    u = (d - L[i]) / max(1e-6, L[i + 1] - L[i])
    v = P[i + 1] - P[i]
    return P[i] + v * u, math.atan2(v[1], v[0])


# ====================================================================== números y juzgado
def contador(h, cx, cy, s, valor, t, sem=0, dig=6, rampa="laton"):
    """Contador mecánico de rodillos: los dígitos ruedan (valor puede ser decimal -> el último rodillo gira suave)."""
    w_, hh = 92 * s, 140 * s
    an = dig * w_ + 40 * s
    h.pieza(rrect(cx - an / 2 - 20 * s, cy - hh / 2 - 30 * s, an + 40 * s, hh + 60 * s, 18 * s), 60, sem, w=6 * s, luz=(0.3, -1),
            d=14 * s, trama=0.4, rim=0.9, rampa=rampa)
    v = max(0.0, valor)
    for k in range(dig):
        p = 10 ** (dig - 1 - k)
        x = cx - an / 2 + 20 * s + k * w_
        h.pieza(rect(x + 4 * s, cy - hh / 2, w_ - 8 * s, hh), 222, sem + 1 + k, w=3 * s, luz=(0.3, -1), d=3, sombra=0.4, trama=0, rim=0,
                rampa="papel")
        d = (v / p) % 10
        frac = d - math.floor(d)
        if p > 1:
            frac = max(0.0, (frac - 0.9) / 0.1) if frac > 0.9 else 0.0
        base = int(math.floor(d))
        for j, nn in enumerate((base, (base + 1) % 10)):
            yy = cy - (frac + (-j)) * hh * 0.9
            if abs(yy - cy) < hh * 0.7:
                N.texto_maquina(h, str(nn), x + w_ / 2, yy, 112 * s, t, -99, cps=1e9, tono=0.05, centro=True, fuente=IMPACT,
                                encuadrar=False)
        plano_(h, rect(x + 4 * s, cy - hh / 2 - 40 * s, w_ - 8 * s, 40 * s), 60, sem + 30 + k, rampa=rampa)
        plano_(h, rect(x + 4 * s, cy + hh / 2, w_ - 8 * s, 40 * s), 60, sem + 50 + k, rampa=rampa)
    h.luz_fija(rect(cx - an / 2, cy - hh / 2, an, hh), 0.9)


def mazo(h, x, y, s=1.0, ang=0.0, sem=0):
    """Mazo de juez (x, y = centro de la cabeza; el mango hacia +x local)."""
    T = T_obj(x, y, ang, s)
    h.pieza(T(rrect(-60, -44, 120, 88, 18)), 90, sem, w=5 * s, luz=(0.3, -1), d=10 * s, trama=0.4, rim=0.9, rampa="madera")
    for xx in (-44, 44):
        plano_(h, T(rect(xx - 6, -44, 12, 88)), 150, sem + 1 + (xx > 0), rampa="laton")
    h.pieza(T(tubo(np.array([[40, 0], [330, 0]]), 26, 20)), 110, sem + 3, w=4 * s, luz=(0.3, -1), d=6 * s, trama=0.3, rim=0.9,
            rampa="madera")


# ====================================================================== pantallas
def portatil(h, cx, cy, s=1.0, sem=0, abre=1.0, brillo=1.0, col=None):
    """Portátil visto de 3/4 frontal (cx, cy = centro de la pantalla). Devuelve la caja de la pantalla (x, y, w, hh)."""
    w_, hh = 520 * s, 330 * s
    x0, y0 = cx - w_ / 2, cy - hh / 2
    h.pieza(rrect(x0 - 24 * s, y0 - 24 * s, w_ + 48 * s, hh + 48 * s, 18 * s), 40, sem, w=5 * s, luz=(0.3, -1), d=10 * s, trama=0.3,
            rim=0.8, rampa="piedra")
    h.pieza(np.array([[x0 - 60 * s, y0 + hh + 30 * s], [x0 + w_ + 60 * s, y0 + hh + 30 * s], [x0 + w_ + 130 * s, y0 + hh + 150 * s],
                      [x0 - 130 * s, y0 + hh + 150 * s]]), 60, sem + 1, w=5 * s, luz=(0.3, -1), d=8 * s, trama=0.3, rim=0.8, rampa="piedra")
    for k in range(4):
        for j in range(12):
            xx = x0 - 40 * s + j * (w_ + 80 * s) / 12 + k * 14 * s - 20 * s
            yy = y0 + hh + 46 * s + k * 22 * s
            plano_(h, rect(xx, yy, (w_ + 80 * s) / 12 - 8 * s, 16 * s), 90, sem + 10 + k * 12 + j, rampa="piedra")
    plano_(h, rect(x0, y0, w_, hh), 30, sem + 70, rampa="papel")
    h.emitir(rect(x0, y0, w_, hh), 0.18 * brillo, col=col or h.pal["luna"], blur=4)
    return (x0, y0, w_, hh)


def chat(h, caja, mensajes, t, px=26, sem=0, fondo=200):
    """Ventana de chat dentro de caja=(x, y, w, hh) del mundo. mensajes = [(t0, 'yo'|'otro', texto), ...]: cada burbuja aparece en t0
    y su texto se escribe; las viejas suben."""
    x, y, w_, hh = caja
    plano_(h, rect(x, y, w_, hh), fondo, sem, rampa="papel")
    plano_(h, rect(x, y, w_, px * 1.8), 70, sem + 1, rampa="piedra")
    h.luz_fija(rect(x, y, w_, hh), 0.95)
    vis = [m for m in mensajes if t >= m[0]]
    yb = y + hh - px * 0.8
    for k, (t0, quien, txt) in enumerate(reversed(vis)):
        lineas = _partir(txt, int(w_ * 0.62 / (px * 0.6)))
        bh = len(lineas) * px * 1.25 + px * 0.8
        ent = e_out(clamp01((t - t0) / 0.25))
        yb -= bh * ent + px * 0.5
        if yb < y + px * 2:
            break
        bw = max(len(l_) for l_ in lineas) * px * 0.62 + px * 1.2
        bx = x + w_ - bw - px * 0.6 if quien == "yo" else x + px * 0.6
        tono = 150 if quien == "yo" else 228
        h.pieza(rrect(bx, yb, bw, bh, px * 0.5), tono, sem + 10 + k, w=2.5, luz=(0.2, -1), d=2, sombra=0.2, trama=0, rim=0,
                rampa="tela_verde" if quien == "yo" else "papel")
        tt = t0
        for j, l_ in enumerate(lineas):
            N.texto_maquina(h, l_, bx + px * 0.6, yb + px * 0.4 + j * px * 1.25, px, t, tt, cps=30, tono=0.05, encuadrar=False, ang=0.0)
            tt += len(l_) / 30


def _partir(s, n):
    pal = s.split()
    out, cur = [], ""
    for p in pal:
        if len(cur) + len(p) + 1 > n and cur:
            out.append(cur)
            cur = p
        else:
            cur = (cur + " " + p).strip()
    if cur:
        out.append(cur)
    return out


def captcha(h, cx, cy, s, t, sem=0, sel=(), ondula=1.0, rotulo=True, marcas=None):
    """Rejilla 3x3 de CAPTCHA: mosaicos dibujados (semáforos, pasos de peatones, coches, farolas) que ondulan. sel = índices
    marcados en verde (palomita). marcas = dict índice -> 0..1 (aparición de la palomita)."""
    lado = 190 * s
    g = 10 * s
    tot = 3 * lado + 2 * g
    x0, y0 = cx - tot / 2, cy - tot / 2
    h.pieza(rect(x0 - 30 * s, y0 - 150 * s, tot + 60 * s, tot + 190 * s), 214, sem, w=5 * s, luz=(0.2, -1), d=8 * s, trama=0, rim=0.3,
            rampa="papel")
    plano_(h, rect(x0, y0 - 128 * s, tot, 104 * s), 70, sem + 1, rampa="tela_verde")
    h.luz_fija(rect(x0 - 30 * s, y0 - 150 * s, tot + 60 * s, tot + 190 * s), 0.92)
    if rotulo:
        N.texto_maquina(h, "Seleccione todos los", x0 + 20 * s, y0 - 116 * s, 26 * s, t, -99, cps=1e9, tono=0.93, encuadrar=False)
        N.texto_maquina(h, "SEMÁFOROS", x0 + 20 * s, y0 - 80 * s, 44 * s, t, -99, cps=1e9, tono=0.97, fuente=IMPACT, encuadrar=False)
    tipos = ["semaforo", "paso", "coche", "semaforo", "farola", "paso", "coche", "semaforo", "paso"]
    for i in range(9):
        r_, c_ = divmod(i, 3)
        x = x0 + c_ * (lado + g)
        y = y0 + r_ * (lado + g)
        _mosaico(h, x, y, lado, tipos[i], t, sem + 20 + i * 13, ondula)
        m = (marcas or {}).get(i, 1.0 if i in sel else 0.0)
        if m > 0:
            h.pieza(rect(x, y, lado, lado), 120, sem + 200 + i, w=6 * s, luz=(0, -1), d=1, sombra=0, trama=0, rim=0, alfa=0.35 * m,
                    rampa="tela_verde")
            k = e_out(m)
            h.pieza(elipse_(x + 30 * s, y + 30 * s, 24 * s * k, 24 * s * k, n=16), 150, sem + 220 + i, w=3 * s, luz=(0, -1), d=2,
                    sombra=0, trama=0, rim=0, rampa="tela_verde")
            h.trazo(np.array([[x + 18 * s, y + 30 * s], [x + 27 * s, y + 40 * s], [x + 43 * s, y + 20 * s]]) if k > 0.6 else
                    np.array([[x + 30 * s, y + 30 * s], [x + 31 * s, y + 31 * s]]), 5 * s, sem + 240 + i, color=(240, 240, 230), jit=0.1,
                    taper=(0, 0))


def _mosaico(h, x, y, lado, tipo, t, sem, ondula):
    """Un mosaico de foto granulosa (dibujado), con onda de distorsión."""
    def W_(P):
        P = np.asarray(P, float).reshape(-1, 2)
        dx = 4 * ondula * np.sin(P[:, 1] * 0.06 + t * 3 + sem)
        dy = 3 * ondula * np.sin(P[:, 0] * 0.05 + t * 2.3 + sem * 0.7)
        return np.stack([x + P[:, 0] + dx, y + P[:, 1] + dy], 1)
    L = lado
    plano_(h, W_(rect(0, 0, L, L * 0.55)), 140, sem, rampa="lejos")
    plano_(h, W_(rect(0, L * 0.55, L, L * 0.45)), 80, sem + 1, rampa="asfalto")
    if tipo == "semaforo":
        h.pieza(W_(rect(L * 0.46, L * 0.25, L * 0.08, L * 0.75)), 30, sem + 2, w=2, d=2, sombra=0, trama=0, rim=0, rampa="piedra")
        h.pieza(W_(rrect(L * 0.36, L * 0.08, L * 0.28, L * 0.5, 8)), 26, sem + 3, w=2.5, d=3, sombra=0, trama=0, rim=0.5, rampa="piedra")
        for k, cc in enumerate(("neon", "sodio", "verde")):
            c = W_(np.array([[L * 0.5, L * (0.17 + k * 0.15)]]))[0]
            h.pieza(elipse_(c[0], c[1], L * 0.06, L * 0.06, n=12), 60, sem + 4 + k, w=0, d=0, sombra=0, trama=0, rim=0, rampa="piedra")
            if k == int(t * 0.7 + sem) % 3:
                h.emitir(elipse_(c[0], c[1], L * 0.055, L * 0.055, n=12), 1.1, col=h.pal[cc], blur=1.5)
    elif tipo == "paso":
        for k in range(6):
            h.pieza(W_([(L * (0.05 + k * 0.16), L * 0.62), (L * (0.13 + k * 0.16), L * 0.62), (L * (0.16 + k * 0.16), L * 0.98),
                        (L * (0.02 + k * 0.16), L * 0.98)]), 210, sem + 2 + k, w=0, d=0, sombra=0, trama=0, rim=0, rampa="papel")
    elif tipo == "coche":
        h.pieza(W_(suave([(L * 0.1, L * 0.78), (L * 0.18, L * 0.58), (L * 0.38, L * 0.46), (L * 0.66, L * 0.46), (L * 0.84, L * 0.6),
                          (L * 0.92, L * 0.78)], 4)), 60, sem + 2, w=2.5, d=4, sombra=0.3, trama=0, rim=0.6, rampa="vino")
        for xx in (0.26, 0.74):
            c = W_(np.array([[L * xx, L * 0.8]]))[0]
            h.pieza(elipse_(c[0], c[1], L * 0.08, L * 0.08, n=12), 14, sem + 5 + int(xx * 10), w=2, d=0, sombra=0, trama=0, rim=0,
                    rampa="piedra")
    elif tipo == "farola":
        h.pieza(W_(rect(L * 0.3, L * 0.2, L * 0.05, L * 0.8)), 30, sem + 2, w=2, d=0, sombra=0, trama=0, rim=0, rampa="piedra")
        c = W_(np.array([[L * 0.4, L * 0.2]]))[0]
        h.emitir(elipse_(c[0], c[1], L * 0.06, L * 0.04, n=12), 1.0, col=h.pal["sodio"], blur=2)
    rng = np.random.default_rng(sem)
    for k in range(10):                                            # grano de foto mala
        px, py = rng.uniform(0, L, 2)
        plano_(h, W_(rect(px, py, 6, 6)), rng.uniform(40, 200), sem + 50 + k, alfa=0.35, rampa="neutro")


# ====================================================================== corcho, hilo rojo y fichas
def chincheta(h, x, y, s=1.0, sem=0, rampa="vino"):
    h.pieza(elipse_(x + 3 * s, y + 4 * s, 13 * s, 11 * s, n=12), 8, sem + 1, w=0, d=0, sombra=0, trama=0, rim=0, alfa=0.5, rampa="piedra")
    h.pieza(elipse_(x, y, 12 * s, 12 * s, n=14), 120, sem, w=2.5 * s, luz=(0.3, -1), d=3, trama=0, rim=0.9, rampa=rampa)


def tarjeta(h, cx, cy, s, titulo, t, t0=-99, sub="", ang=0.0, sem=0, dibujo=None, w_=420, hh=300, entra=0.25, pin=True,
            tono=218):
    """Ficha de cartulina clavada en el corcho: un dibujo (fn(h, T) en coordenadas locales de la ficha) y el título a máquina.
    Entra con un golpe (escala) en t0. Devuelve el punto de la chincheta (para el hilo)."""
    if t < t0:
        return None
    k = 1.0 + 0.3 * (1 - e_out(clamp01((t - t0) / entra)))
    T = T_obj(cx, cy, ang, s * k)
    h.pieza(T(rect(-w_ / 2, -hh / 2, w_, hh)), tono, sem, w=4, luz=(0.2, -1), d=8, sombra=0.5, trama=0, rim=0.2, rampa="papel")
    if dibujo is not None:
        dibujo(h, T)
    c = T(np.array([[0, hh / 2 - 40]]))[0]
    N.soporte(h, cx, cy, w_, hh, ang, s * k, margen=14)
    N.texto_maquina(h, titulo, c[0], c[1], 30 * s * k, t, t0 + 0.15, cps=40, tono=0.05, centro=True, fuente=IMPACT, encuadrar=False)
    if sub:
        c2 = T(np.array([[0, hh / 2 - 12]]))[0]
        N.texto_maquina(h, sub, c2[0], c2[1], 18 * s * k, t, t0 + 0.3, cps=40, tono=0.12, centro=True, encuadrar=False)
    p = T(np.array([[0, -hh / 2 + 18]]))[0]
    if pin:
        chincheta(h, p[0], p[1], s * k, sem + 90)
    return p


def hilo(h, a, b, t, t0, dur=0.6, sem=0, comba=40.0, w=4.0):
    """Hilo de lana roja que se tiende de a hacia b (empieza en t0, tarda dur s), con su comba."""
    u = clamp01((t - t0) / dur)
    if u <= 0:
        return
    a, b = np.asarray(a, float), np.asarray(b, float)
    e = e_out(u)
    q = a + (b - a) * e
    n = 20
    s_ = np.linspace(0, 1, n)
    P = a[None] + (q - a)[None] * s_[:, None] + np.array([0, 1.0])[None] * (comba * e * np.sin(s_ * math.pi))[:, None]
    c = np.asarray(h.c(150, "vino"))
    h.trazo(P, w * h.zoom ** 0, sem, color=tuple(c), jit=0.3, taper=(0, 0))


# ====================================================================== manos
def mano(h, x, y, s=1.0, ang=0.0, pose="abierta", sem=0, rampa="piel", tono=140, manga=None, manga_tono=60, largo_brazo=0,
         luz=(0.3, -1), cierra=0.0):
    """Mano humana vista de lado/arriba (x, y = muñeca; los dedos apuntan a +x local). poses: abierta · agarra (puño sobre un mango
    horizontal) · dedo (índice estirado) · pellizco. manga = rampa de la manga (brazo que entra desde -x, largo_brazo px)."""
    T = T_obj(x, y, ang, s)
    if manga is not None and largo_brazo > 0:
        h.pieza(T(tubo(np.array([[-largo_brazo, 0], [-largo_brazo * 0.5, 2], [10, 0]]), 92, 80)), manga_tono, sem + 30, w=5 * s, luz=luz,
                d=12 * s, trama=0.5, rim=0.8, rampa=manga)
        h.pieza(T(rect(-6, -42, 20, 84)), manga_tono + 30, sem + 31, w=3 * s, luz=luz, d=3, trama=0.2, rim=0.6, rampa=manga)
    palma = suave([(0, -34), (70, -40), (96, -30), (100, 26), (70, 40), (0, 34)], 4)
    h.pieza(T(palma), tono, sem, w=4.5 * s, luz=luz, d=10 * s, trama=0.3, rim=0.85, rampa=rampa)
    if pose in ("abierta", "dedo", "pellizco"):
        for k in range(4):
            yy = -28 + k * 18
            L = 92 - abs(k - 1.2) * 12
            if pose == "dedo" and k > 0:
                P = np.array([[92, yy], [112, yy + 4], [118, yy + 18]])
            elif pose == "pellizco" and k > 1:
                P = np.array([[92, yy], [110, yy + 6], [112, yy + 16]])
            else:
                c = cierra
                P = np.array([[90, yy], [90 + L * 0.55, yy - 2 + 10 * c], [90 + L * (1 - 0.5 * c), yy + 26 * c]])
            h.pieza(T(tubo(P, 19, 15)), tono + 6, sem + 1 + k, w=3.5 * s, luz=luz, d=5 * s, trama=0.2, rim=0.85, rampa=rampa)
        h.pieza(T(tubo(np.array([[40, 30], [78, 52], [104, 48 if pose != "pellizco" else 34]]), 22, 17)), tono, sem + 6, w=3.5 * s,
                luz=luz, d=5 * s, trama=0.2, rim=0.85, rampa=rampa)
    elif pose == "agarra":
        for k in range(4):
            yy = -28 + k * 18
            h.pieza(T(suave([(88, yy - 9), (118, yy - 7), (124, yy + 9), (92, yy + 10)], 3)), tono + 6, sem + 1 + k, w=3.5 * s, luz=luz,
                    d=5 * s, trama=0.2, rim=0.85, rampa=rampa)
        h.pieza(T(tubo(np.array([[40, -30], [80, -48], [104, -40]]), 22, 17)), tono, sem + 6, w=3.5 * s, luz=luz, d=5 * s, trama=0.2,
                rim=0.85, rampa=rampa)
    return T(np.array([[118, 0]]))[0]


# ====================================================================== bar
def vaso(h, x, y, s=1.0, sem=0, nivel=0.5, hielo=True, t=0.0, lado=True):
    """Vaso de whisky visto de lado (x, y = base)."""
    T = T_obj(x, y, 0, s)
    if nivel > 0:
        h.pieza(T(rect(-46, -110 * nivel - 8, 92, 110 * nivel)), 150, sem, w=0, luz=(0.3, -1), d=4, sombra=0.3, trama=0, rim=0.6,
                rampa="whisky")
        if hielo:
            for k, (dx, a) in enumerate(((-14, 0.3), (16, -0.4))):
                c = T(np.array([[dx, -110 * nivel - 2]]))[0]
                h.pieza(rot(rect(c[0] - 18 * s, c[1] - 16 * s, 36 * s, 32 * s), a + 0.05 * math.sin(t + k), c), 220, sem + 2 + k,
                        w=2 * s, luz=(0.3, -1), d=2, sombra=0, trama=0, rim=0.9, alfa=0.7, rampa="piedra")
    h.pieza(T([(-56, -130), (56, -130), (50, 0), (-50, 0)]), 200, sem + 5, w=4 * s, luz=(0.3, -1), d=6 * s, sombra=0.2, trama=0, rim=0.9,
            alfa=0.35, rampa="piedra")
    h.pieza(T(rect(-50, -14, 100, 14)), 210, sem + 6, w=2 * s, luz=(0.3, -1), d=2, sombra=0, trama=0, rim=0.9, alfa=0.6, rampa="piedra")
    h.pieza(T(rect(-44, -124, 10, 100)), 240, sem + 7, w=0, d=0, sombra=0, trama=0, rim=0, alfa=0.35, rampa="piedra")


def servilleta(h, cx, cy, s=1.0, ang=0.0, sem=0):
    """Servilleta de papel de bar (cuadrada, con el borde dentado y un doblez). Declara soporte para escribir encima."""
    T = T_obj(cx, cy, ang, s)
    n = 18
    borde = []
    for k in range(4):
        a0 = [(-300, -300), (300, -300), (300, 300), (-300, 300)][k]
        a1 = [(-300, -300), (300, -300), (300, 300), (-300, 300)][(k + 1) % 4]
        for j in range(n):
            u = j / n
            p = np.array(a0) + (np.array(a1) - np.array(a0)) * u
            nrm = np.array([0, -1]) if k == 0 else (np.array([1, 0]) if k == 1 else (np.array([0, 1]) if k == 2 else np.array([-1, 0])))
            borde.append(p + nrm * (5 if j % 2 else 0))
    h.pieza(T(np.array(borde)), 222, sem, w=3 * s, luz=(0.2, -1), d=6 * s, sombra=0.3, trama=0, rim=0.2, rampa="papel")
    h.trazo(T(np.array([[-300, 0], [300, 0]])), 2.5 * s, sem + 1, alfa=0.25)
    h.trazo(T(np.array([[0, -300], [0, 300]])), 2.5 * s, sem + 2, alfa=0.25)
    for k in range(4):
        a = k * math.pi / 2 + math.pi / 4
        c = T(np.array([[230 * math.cos(a), 230 * math.sin(a)]]))[0]
        h.anillo(h.tf(elipse_(c[0], c[1], 22 * s, 22 * s, n=16)), 1.8 * h.zoom, sem + 10 + k, alfa=0.3)
    N.soporte(h, cx, cy, 600, 600, ang, s, margen=40)
    return T


def boton_off(h, x, y, s=1.0, pulsado=0.0, sem=0, t=0.0, brillo=1.0):
    """Botón rojo de apagado en su caja amarilla con rayas (x, y = centro)."""
    h.pieza(rect(x - 170 * s, y - 170 * s, 340 * s, 340 * s), 150, sem, w=6 * s, luz=(0.3, -1), d=16 * s, trama=0.4, rim=0.8, rampa="whisky")
    for k in range(-4, 5):
        P = np.array([[x - 170 * s + (k * 70 - 40) * s, y + 170 * s], [x - 170 * s + (k * 70) * s, y + 170 * s],
                      [x - 170 * s + (k * 70 + 340) * s, y - 170 * s], [x - 170 * s + (k * 70 + 300) * s, y - 170 * s]])
        P[:, 0] = np.clip(P[:, 0], x - 170 * s, x + 170 * s)
        plano_(h, P, 20, sem + 10 + k, alfa=0.7, rampa="piedra")
    h.pieza(elipse_(x, y, 120 * s, 120 * s, n=40), 40, sem + 1, w=5 * s, luz=(0.3, -1), d=8 * s, trama=0.3, rim=0.8, rampa="piedra")
    hun = 14 * s * clamp01(pulsado)
    h.pieza(elipse_(x, y - 10 * s + hun, 96 * s, 90 * s, n=40), 120, sem + 2, w=5 * s, luz=(0.3, -1), d=16 * s - hun, trama=0.2, rim=0.9,
            rampa="vino")
    h.emitir(elipse_(x - 20 * s, y - 34 * s + hun, 40 * s, 20 * s, n=16), 0.25 * brillo, col=h.pal["neon"], blur=4)
    N.texto_maquina(h, "OFF", x, y - 4 * s + hun, 60 * s, t, -99, cps=1e9, tono=0.93, centro=True, fuente=IMPACT, encuadrar=False)


# ====================================================================== juegos
def ficha_juego(h, x, y, s=1.0, tipo="ejercito", rampa="vino", sem=0, tono=130, ang=0.0, caida=0.0):
    """Ficha de Diplomacy: ejército (bloque con estrella) o flota (casco). caida 0..1: volcada."""
    T = T_obj(x, y, ang + 1.3 * caida, s)
    if tipo == "ejercito":
        h.pieza(T(rrect(-34, -30, 68, 60, 10)), tono, sem, w=4 * s, luz=(0.3, -1), d=8 * s, trama=0.3, rim=0.9, rampa=rampa)
        h.pieza(T(np.array([(math.cos(a) * (16 if k % 2 == 0 else 7), math.sin(a) * (16 if k % 2 == 0 else 7))
                            for k, a in enumerate(np.linspace(-math.pi / 2, 1.5 * math.pi, 10, endpoint=False))])), 220, sem + 1,
                w=1.5 * s, luz=(0.3, -1), d=1, sombra=0, trama=0, rim=0, rampa="papel")
    else:
        h.pieza(T(suave([(-46, -6), (46, -6), (32, 22), (-32, 22)], 3)), tono, sem, w=4 * s, luz=(0.3, -1), d=6 * s, trama=0.3, rim=0.9,
                rampa=rampa)
        h.pieza(T(rect(-4, -40, 8, 36)), tono - 30, sem + 1, w=2 * s, luz=(0.3, -1), d=2, trama=0, rim=0.6, rampa=rampa)
        h.pieza(T([(4, -38), (30, -18), (4, -12)]), 210, sem + 2, w=2 * s, luz=(0.3, -1), d=2, trama=0, rim=0.4, rampa="papel")


def pieza_ajedrez(h, x, y, s=1.0, tipo="peon", blanca=True, ang=0.0, sem=0):
    """Pieza de ajedrez de perfil (x, y = base)."""
    T = T_obj(x, y, ang, s)
    tono = 210 if blanca else 40
    rp = "papel" if blanca else "madera"
    h.pieza(T(suave([(-46, 0), (46, 0), (40, -24), (-40, -24)], 3)), tono, sem, w=4 * s, luz=(0.3, -1), d=6 * s, trama=0.2, rim=0.9,
            rampa=rp)
    cuerpo = {"peon": [(-30, -24), (30, -24), (14, -90), (-14, -90)], "torre": [(-34, -24), (34, -24), (30, -130), (-30, -130)],
              "alfil": [(-32, -24), (32, -24), (14, -120), (-14, -120)], "rey": [(-34, -24), (34, -24), (18, -140), (-18, -140)],
              "caballo": [(-34, -24), (34, -24), (20, -90), (34, -130), (0, -160), (-30, -120), (-20, -90)]}[tipo]
    h.pieza(T(suave(cuerpo, 3)), tono, sem + 1, w=4 * s, luz=(0.3, -1), d=8 * s, trama=0.3, rim=0.9, rampa=rp)
    if tipo == "peon":
        h.pieza(T(elipse_(0, -110, 26, 26, n=18)), tono, sem + 2, w=4 * s, luz=(0.3, -1), d=6 * s, trama=0.2, rim=0.9, rampa=rp)
    elif tipo == "torre":
        for k in range(3):
            h.pieza(T(rect(-34 + k * 26, -158, 16, 30)), tono, sem + 3 + k, w=3 * s, luz=(0.3, -1), d=4, trama=0.2, rim=0.9, rampa=rp)
    elif tipo == "rey":
        h.pieza(T(rect(-6, -190, 12, 52)), tono, sem + 2, w=3 * s, luz=(0.3, -1), d=4, trama=0, rim=0.9, rampa=rp)
        h.pieza(T(rect(-20, -176, 40, 12)), tono, sem + 3, w=3 * s, luz=(0.3, -1), d=4, trama=0, rim=0.9, rampa=rp)
    elif tipo == "alfil":
        h.pieza(T(elipse_(0, -138, 22, 30, n=18)), tono, sem + 2, w=4 * s, luz=(0.3, -1), d=6 * s, trama=0.2, rim=0.9, rampa=rp)


# ====================================================================== personajes-objeto
def busto_ciceron(h, x, y, s, t, sem=0, sonrisa=0.0, ojo=1.0, mira=0.0, luz=(0.4, -1.0), gira=0.0):
    """Busto romano de mármol (Cicerón) con un OJO de circuito que brilla rojo: así se presenta la máquina que juega Diplomacy.
    (x, y) = base del pedestal; ~760 px a s = 1. sonrisa 0..1. mira desplaza la pupila."""
    T = T_obj(x, y, 0, s)
    rp = "piedra"
    h.pieza(T(rect(-150, -150, 300, 150)), 120, sem, w=6 * s, luz=luz, d=16 * s, trama=0.5, rim=0.8, rampa="laton")      # pedestal
    h.pieza(T(rect(-170, -170, 340, 30)), 150, sem + 1, w=5 * s, luz=luz, d=8 * s, trama=0.3, rim=0.8, rampa="laton")
    N.texto_maquina(h, "CICERO", *T(np.array([[0, -80]]))[0], 52 * s, t, -99, cps=1e9, tono=0.06, centro=True,
                    fuente="C:/Windows/Fonts/BOD_B.TTF", track=6, encuadrar=False)
    # hombros con toga
    h.pieza(T(suave([(-230, -170), (-200, -300), (-110, -350), (110, -350), (200, -300), (230, -170)], 5)), 200, sem + 2, w=6 * s,
            luz=luz, d=20 * s, trama=0.6, rim=0.9, rampa=rp)
    for k in range(4):
        h.trazo(T(np.array([[-150 + k * 50, -330 + k * 6], [-60 + k * 60, -180]])), 3 * s, sem + 10 + k, alfa=0.45)
    h.pieza(T(rect(-50, -400, 100, 80)), 196, sem + 3, w=5 * s, luz=luz, d=10 * s, trama=0.4, rim=0.9, rampa=rp)       # cuello
    gx = 18 * gira
    cab = suave([(-100 + gx, -520), (-96 + gx, -610), (-50 + gx, -660), (30 + gx, -664), (86 + gx, -620), (100 + gx, -560), (118 + gx, -540),
                 (104 + gx, -520), (110 + gx, -500), (96 + gx, -470), (60 + gx, -440), (0 + gx, -410), (-60 + gx, -420), (-96 + gx, -460)], 5)
    h.pieza(T(cab), 205, sem + 4, w=6 * s, luz=luz, d=22 * s, trama=0.5, rim=0.9, rampa=rp)
    for k in range(9):                                        # cabello corto romano (mechones)
        a = math.pi * (1.05 + 0.85 * k / 8)
        c = (gx + 70 * math.cos(a) * 1.3, -600 + 60 * math.sin(a))
        h.pieza(T(elipse_(c[0], c[1], 26, 16, rot=a + 1.4, n=10)), 175, sem + 20 + k, w=3 * s, luz=luz, d=4 * s, trama=0.2, rim=0.7,
                rampa=rp)
    h.trazo(T(np.array([[30 + gx, -578], [72 + gx, -586]])), 5 * s, sem + 30, alfa=0.85)                                 # ceja
    h.pieza(T([(84 + gx, -560), (118 + gx, -520), (94 + gx, -512)]), 190, sem + 31, w=3.5 * s, luz=luz, d=4 * s, trama=0.2, rim=0.9,
            rampa=rp)                                                                                                     # nariz
    # el ojo de circuito
    oc = T(np.array([[56 + gx, -556]]))[0]
    h.pieza(elipse_(oc[0], oc[1], 24 * s, 15 * s, n=18), 30, sem + 32, w=3 * s, luz=luz, d=2, sombra=0, trama=0, rim=0, rampa=rp)
    if ojo > 0:
        h.emitir(elipse_(oc[0] + mira * 8 * s, oc[1], 9 * s, 9 * s, n=12), 1.6 * ojo, col=h.pal["neon"], blur=1.5)
        h.resplandor(oc[0], oc[1], 90 * s, 0.25 * ojo, col=h.pal["neon"])
        for k in range(3):                                    # trazas de circuito que salen del ojo
            P = T(np.array([[56 + gx - 20, -556 + k * 10 - 10], [10 + gx - 30 * k, -556 + k * 14], [-20 + gx - 30 * k, -500 + k * 20]]))
            h.trazo(P, 2.5 * s, sem + 40 + k, color=(200, 60, 50), alfa=0.8 * ojo, jit=0.1, taper=(0, 0))
    # boca: la sonrisa se curva
    b = sonrisa
    P = T(np.array([[60 + gx, -480 + 6 * b], [80 + gx, -476 - 4 * b], [100 + gx, -486 - 12 * b]]))
    h.trazo(P, 4.5 * s, sem + 50, alfa=0.9)
    h.trazo(T(np.array([[-40 + gx, -560], [-30 + gx, -520], [-44 + gx, -500]])), 4 * s, sem + 51, alfa=0.6)          # oreja
    return T(np.array([[56 + gx, -556]]))[0]


def juez(h, x, y, s, t, sem=0, barrido=0.0, ojo=1.0, golpe=0.0, luz=(0.2, -1.0)):
    """EL JUEZ: el algoritmo evaluador como una máquina enorme con toga sobre el estrado: cabeza de lente (un ojo que barre),
    peluca de rodillos de papel, brazo con sello. (x, y) = base del estrado (centro). barrido -1..1 mueve el haz del ojo.
    golpe 0..1 baja el sello. Devuelve (centro del ojo, ángulo del haz)."""
    T = T_obj(x, y, 0, s)
    # estrado de madera
    h.pieza(T(rect(-520, -420, 1040, 420)), 70, sem, w=7 * s, luz=luz, d=20 * s, trama=0.6, rim=0.7, rampa="madera")
    for k in range(5):
        h.pieza(T(rect(-480 + k * 196, -380, 160, 320)), 86, sem + 1 + k, w=4 * s, luz=luz, d=6 * s, trama=0.3, rim=0.5, rampa="madera")
    h.pieza(T(rect(-560, -450, 1120, 40)), 110, sem + 8, w=5 * s, luz=luz, d=8 * s, trama=0.3, rim=0.8, rampa="madera")
    # cuerpo con toga
    h.pieza(T(suave([(-330, -450), (-300, -820), (-180, -900), (180, -900), (300, -820), (330, -450)], 5)), 26, sem + 10, w=7 * s,
            luz=luz, d=22 * s, trama=0.6, rim=0.9, rampa="piedra")
    h.pieza(T([(-60, -900), (60, -900), (20, -720), (-20, -720)]), 210, sem + 11, w=4 * s, luz=luz, d=4, trama=0, rim=0.4, rampa="papel")
    # cabeza: carcasa de metal con lente
    h.pieza(T(rrect(-170, -1180, 340, 290, 60)), 120, sem + 12, w=7 * s, luz=luz, d=22 * s, trama=0.5, rim=0.9, rampa="piedra")
    for sx in (-1, 1):                                       # peluca: rodillos de papel continuo
        for k in range(4):
            h.pieza(T(elipse_(sx * (190 + 6 * k), -1120 + k * 64, 48, 34, n=18)), 220, sem + 20 + k + (sx > 0) * 5, w=4 * s, luz=luz,
                    d=8 * s, trama=0.3, rim=0.6, rampa="papel")
    oc = T(np.array([[0, -1040]]))[0]
    h.pieza(elipse_(oc[0], oc[1], 100 * s, 100 * s, n=40), 40, sem + 30, w=6 * s, luz=luz, d=10 * s, trama=0.3, rim=0.95, rampa="laton")
    h.pieza(elipse_(oc[0], oc[1], 76 * s, 76 * s, n=40), 20, sem + 31, w=4 * s, luz=luz, d=2, sombra=0, trama=0, rim=0,
            rampa="vidrio_verde")
    ang = math.pi / 2 + 0.55 * barrido
    if ojo > 0:
        h.emitir(elipse_(oc[0], oc[1], 46 * s, 46 * s, n=24), 1.2 * ojo, col=h.pal["neon"], blur=3)
        h.emitir(elipse_(oc[0] - 14 * s, oc[1] - 16 * s, 12 * s, 10 * s, n=10), 1.8 * ojo, col=(1, 1, 1), blur=1)
    # brazo con el sello
    sh = T(np.array([[300, -820]]))[0]
    g = e_out(clamp01(golpe))
    mn = sh + np.array([170 * s, (-80 + 380 * g) * s])
    h.pieza(tubo(np.array([sh, sh + (120 * s, -30 * s), mn]), 70 * s, 54 * s), 34, sem + 40, w=6 * s, luz=luz, d=12 * s, trama=0.5, rim=0.9,
            rampa="piedra")
    h.pieza(rect(mn[0] - 70 * s, mn[1], 140 * s, 60 * s), 90, sem + 41, w=5 * s, luz=luz, d=8 * s, trama=0.3, rim=0.9, rampa="madera")
    h.pieza(rect(mn[0] - 80 * s, mn[1] + 60 * s, 160 * s, 40 * s), 120, sem + 42, w=5 * s, luz=luz, d=6 * s, trama=0.2, rim=0.9,
            rampa="vino")
    return oc, ang


def robot_mesa(h, x, y, s, t, sem=0, nombre="BOB", visor=1.0, d=1, brazo=0.0, habla=0.0, tono=150, rampa="laton"):
    """Agente de 2017 (Bob o Alice): robot de mesa de lata, cuerpo de caja, cabeza redonda con rejilla de altavoz y antena;
    placa con el nombre. (x, y) = base. brazo 0..1 extiende el brazo hacia d. habla 0..1 hace vibrar la rejilla."""
    T = T_obj(x, y, 0, s, sx=d)
    h.pieza(T(rect(-80, -40, 160, 40)), tono - 70, sem, w=4 * s, luz=(0.3, -1), d=6 * s, trama=0.4, rim=0.8, rampa=rampa)
    h.pieza(T(rrect(-90, -260, 180, 220, 20)), tono, sem + 1, w=5 * s, luz=(0.3, -1), d=14 * s, trama=0.5, rim=0.9, rampa=rampa)
    for k in range(3):
        h.pieza(T(elipse_(-40 + k * 40, -200, 12, 12, n=10)), 60 + 40 * (k == int(t * 3 + sem) % 3), sem + 2 + k, w=2.5 * s, luz=(0.3, -1),
                d=2, trama=0, rim=0.6, rampa="piedra")
        if k == int(t * 3 + sem) % 3:
            h.emitir(T(elipse_(-40 + k * 40, -200, 9, 9, n=10)), 0.9 * visor, col=h.pal["sodio"], blur=1)
    c = T(np.array([[0, -110]]))[0]
    h.pieza(T(rect(-60, -136, 120, 50)), 214, sem + 6, w=3 * s, luz=(0.3, -1), d=2, sombra=0, trama=0, rim=0, rampa="papel")
    N.texto_maquina(h, nombre, c[0], c[1], 36 * s, t, -99, cps=1e9, tono=0.05, centro=True, fuente=IMPACT, encuadrar=False)
    # brazo extensible (pinza) hacia d
    b = clamp01(brazo)
    base = np.array([90.0, -170])
    fin = base + np.array([40 + 200 * b, 30 + 40 * b])
    h.pieza(T(tubo(np.array([base, (base + fin) / 2 + (0, -20), fin]), 26, 22)), tono - 30, sem + 7, w=3.5 * s, luz=(0.3, -1), d=5 * s,
            trama=0.3, rim=0.8, rampa=rampa)
    for q in (-1, 1):
        h.pieza(T([(fin[0], fin[1] - 4), (fin[0] + 34, fin[1] + q * 18 - 4), (fin[0] + 30, fin[1] + q * 8)]), tono - 40, sem + 8 + q,
                w=3 * s, luz=(0.3, -1), d=3, trama=0, rim=0.8, rampa=rampa)
    # cabeza redonda
    hc = np.array([0.0, -340 + 3 * math.sin(t * 2 + sem)])
    h.pieza(T(elipse_(hc[0], hc[1], 92, 86, n=36)), tono + 20, sem + 10, w=5 * s, luz=(0.3, -1), d=14 * s, trama=0.4, rim=0.9, rampa=rampa)
    h.pieza(T(rrect(-60, hc[1] - 36, 120, 44, 18)), 20, sem + 11, w=3 * s, luz=(0.3, -1), d=2, sombra=0, trama=0, rim=0, rampa="piedra")
    if visor > 0:
        ex = 22 * math.sin(t * 1.3 + sem)
        h.emitir(T(rrect(-40 + ex, hc[1] - 26, 30, 22, 8)), 1.1 * visor, col=h.pal["sodio"], blur=1.2)
        h.emitir(T(rrect(14 + ex, hc[1] - 26, 30, 22, 8)), 1.1 * visor, col=h.pal["sodio"], blur=1.2)
    for k in range(4):
        yy = hc[1] + 24 + k * 9
        amp = 4 * habla * math.sin(t * 30 + k)
        h.trazo(T(np.array([[-30, yy + amp], [30, yy - amp]])), 3 * s, sem + 20 + k, alfa=0.7)
    h.trazo(T(np.array([[0, hc[1] - 86], [10, hc[1] - 150]])), 4 * s, sem + 30)
    h.pieza(T(elipse_(10, hc[1] - 156, 12, 12, n=10)), 150, sem + 31, w=2.5 * s, luz=(0.3, -1), d=2, trama=0, rim=0.8, rampa="vino")
    if visor > 0:
        h.emitir(T(elipse_(10, hc[1] - 156, 7, 7, n=10)), 0.8 * visor * (0.5 + 0.5 * math.sin(t * 4 + sem)), col=h.pal["neon"], blur=1)
    return T(fin + (34, 0))[0] if np.ndim(T(fin)) > 1 else T(fin)


# ====================================================================== escena del crimen
def cinta_policial(h, a, b, t, sem=0, texto="NO PASAR · ESCENA DEL CRIMEN", px=26):
    a, b = np.asarray(a, float), np.asarray(b, float)
    d = b - a
    L = float(np.hypot(*d))
    ang = math.atan2(d[1], d[0])
    n = np.array([-d[1], d[0]]) / (L + 1e-9)
    ond = 6 * math.sin(t * 2.0 + sem)
    P = np.array([a - n * 22, b - n * 22 + n * ond, b + n * 22 + n * ond, a + n * 22])
    h.pieza(P, 180, sem, w=3, luz=(0.3, -1), d=3, sombra=0.3, trama=0, rim=0.4, rampa="whisky")
    paso = len(texto) * px * 0.62 + 60
    k = 0
    while (k + 0.5) * paso < L:
        c = a + d / L * (k + 0.5) * paso + n * ond * (k + 0.5) * paso / L
        N.texto_maquina(h, texto, c[0], c[1], px, t, -99, cps=1e9, tono=0.05, centro=True, fuente=IMPACT, encuadrar=False, ang=ang)
        k += 1


def silueta_tiza(h, x, y, s=1.0, u=1.0, sem=0, ang=0.0):
    """Contorno de tiza en el suelo de una COPIA caída (cabeza de monitor), que se dibuja hasta u."""
    T = T_obj(x, y, ang, s)
    P = [(-260, 30), (-160, 60), (-40, 50), (60, 90), (140, 70), (180, 120), (240, 100), (220, 40), (300, 10), (330, -70),
         (420, -60), (470, -130), (420, -210), (330, -200), (300, -130), (230, -150), (170, -100), (60, -120), (-40, -150),
         (-140, -120), (-250, -170), (-300, -110), (-230, -60), (-300, -10)]
    Q = np.array(suave(P, 6))
    m = max(2, int(len(Q) * clamp01(u)))
    h.trazo(T(np.vstack([Q[:m]])), 7 * s, sem, color=tuple(h.c(235, "papel")), jit=0.6, taper=(0.1, 0.1))


# ====================================================================== luces de mesa
def lampara_mesa(h, x, y, s=1.0, sem=0, enc=1.0, col=None, ang=0.0):
    """Flexo de despacho (x, y = base) con pantalla cónica; devuelve el punto de la bombilla."""
    T = T_obj(x, y, 0, s)
    h.pieza(T(elipse_(0, -10, 90, 22, n=30)), 40, sem, w=4 * s, luz=(0.3, -1), d=6 * s, trama=0.3, rim=0.8, rampa="piedra")
    h.pieza(T(tubo(np.array([[0, -20], [-30, -200], [60, -330]]), 14, 12)), 60, sem + 1, w=3 * s, luz=(0.3, -1), d=4, trama=0.2, rim=0.8,
            rampa="piedra")
    c = np.array([60.0, -330])
    P = rot(np.array([(-30, -40), (40, -40), (110, 60), (-70, 60)]), 0.5 + ang, (0, 0)) + c
    h.pieza(T(P), 40, sem + 2, w=4 * s, luz=(0.3, -1), d=8 * s, trama=0.4, rim=0.9, rampa="tela_verde")
    b = T(rot(np.array([[20.0, 60]]), 0.5 + ang, (0, 0)) + c)[0]
    if enc > 0:
        h.emitir(elipse_(b[0], b[1], 30 * s, 12 * s, n=16), 1.3 * enc, col=col or h.pal["lampara"], blur=3)
    return b


def telefono(h, x, y, s=1.0, sem=0, descolgado=0.0, t=0.0):
    """Teléfono de baquelita de disco (x, y = base)."""
    T = T_obj(x, y, 0, s)
    h.pieza(T(suave([(-120, 0), (120, 0), (90, -110), (-90, -110)], 4)), 26, sem, w=5 * s, luz=(0.3, -1), d=10 * s, trama=0.4, rim=0.9,
            rampa="piedra")
    h.pieza(T(elipse_(0, -60, 54, 30, n=30)), 200, sem + 1, w=3 * s, luz=(0.3, -1), d=3, trama=0, rim=0.6, rampa="papel")
    u = e_out(clamp01(descolgado))
    c = np.array([0.0, -150 - 160 * u])
    a = -0.6 * u
    h.pieza(T(rot(suave([(-150, 0), (-120, -40), (120, -40), (150, 0), (110, 10), (-110, 10)], 4) + c, a, c)), 30, sem + 2, w=5 * s,
            luz=(0.3, -1), d=10 * s, trama=0.4, rim=0.9, rampa="piedra")


def cadena(h, a, b, sem=0, eslabon=34, grosor=7, tono=150, comba=0.0, t=0.0):
    """Cadena de eslabones alternos (de frente y de canto) de a hasta b, con comba opcional."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    L = float(np.hypot(*(b - a)))
    n = max(2, int(L / (eslabon * 0.8)))
    d = (b - a) / (L + 1e-9)
    nrm = np.array([-d[1], d[0]])
    ang = math.atan2(d[1], d[0])
    for k in range(n):
        u = (k + 0.5) / n
        c = a + (b - a) * u + nrm * comba * math.sin(math.pi * u) + np.array([0, 2 * math.sin(t * 2 + k)])
        if k % 2 == 0:
            P = elipse_(c[0], c[1], eslabon * 0.6, eslabon * 0.36, rot=ang, n=16)
            h.pieza(P, tono, sem + k, w=grosor * 0.5, luz=(0.3, -1), d=3, sombra=0.3, trama=0, rim=0.9, rampa="piedra")
            h.pieza(elipse_(c[0], c[1], eslabon * 0.32, eslabon * 0.12, rot=ang, n=12), 10, sem + 500 + k, w=0, d=0, sombra=0, trama=0,
                    rim=0, rampa="piedra")
        else:
            P = np.array([c - d * eslabon * 0.6 - nrm * grosor * 0.6, c + d * eslabon * 0.6 - nrm * grosor * 0.6,
                          c + d * eslabon * 0.6 + nrm * grosor * 0.6, c - d * eslabon * 0.6 + nrm * grosor * 0.6])
            h.pieza(P, tono - 20, sem + k, w=grosor * 0.4, luz=(0.3, -1), d=2, sombra=0, trama=0, rim=0.9, rampa="piedra")


def papeles(h, t, t0, x, y, n=12, sem=0, dirx=1, vel=900.0, alcance=900.0, cada=0.12, s=1.0, suelo=None):
    """Hojas que salen disparadas de (x, y) una tras otra (cada `cada` s), giran en el aire y caen."""
    rng = np.random.default_rng(sem)
    for k in range(n):
        u = t - t0 - k * cada
        if u < 0:
            continue
        a = -0.6 - rng.uniform(0, 0.7)
        v = vel * rng.uniform(0.7, 1.2)
        px = x + dirx * math.cos(a) * v * u * (1 / (1 + u * 1.5))
        py = y + math.sin(a) * v * u * (1 / (1 + u * 1.5)) + 520 * u * u
        if suelo is not None and py > suelo:
            py = suelo
        rr = rng.uniform(-1, 1) * (3 + u * 4)
        c = np.array([px, py])
        P = rot(rect(px - 60 * s, py - 42 * s, 120 * s, 84 * s), rr, c)
        if py > 3000:
            continue
        h.pieza(P, 222, sem + k, w=2.5, luz=(0.2, -1), d=3, sombra=0.25, trama=0, rim=0.3, rampa="papel")
        for j in range(3):
            q = rot(rect(px - 44 * s, py - 24 * s + j * 18 * s, 80 * s, 4 * s), rr, c)
            plano_(h, q, 110, sem + 100 + k * 3 + j, alfa=0.6, rampa="papel")


# ====================================================================== objetos de trueque (Bob y Alice)
def objeto_trato(h, tipo, x, y, s=1.0, sem=0, ang=0.0):
    """Objeto de las negociaciones de 2017 apoyado en (x, y): sombrero · libro · balon."""
    if tipo == "sombrero":
        h.pieza(elipse_(x, y, 72 * s, 20 * s, n=24), 60, sem, w=4 * s, luz=(0.3, -1), d=6 * s, trama=0.3, rim=0.8, rampa="vino")
        h.pieza(rot(rect(x - 38 * s, y - 70 * s, 76 * s, 70 * s), ang * 0.3, (x, y)), 56, sem + 1, w=4 * s, luz=(0.3, -1), d=8 * s,
                trama=0.3, rim=0.8, rampa="vino")
        h.pieza(rect(x - 38 * s, y - 24 * s, 76 * s, 12 * s), 190, sem + 2, w=0, luz=(0.3, -1), d=2, sombra=0, trama=0, rim=0,
                rampa="laton")
    elif tipo == "libro":
        h.pieza(rot(rect(x - 56 * s, y - 70 * s, 112 * s, 70 * s), ang, (x, y)), 80, sem, w=4 * s, luz=(0.3, -1), d=8 * s, trama=0.3,
                rim=0.8, rampa="tela_verde")
        h.pieza(rot(rect(x - 50 * s, y - 62 * s, 100 * s, 10 * s), ang, (x, y)), 215, sem + 1, w=0, luz=(0.3, -1), d=1, sombra=0,
                trama=0, rim=0, rampa="papel")
    else:
        h.pieza(elipse_(x, y - 48 * s, 48 * s, 48 * s, n=28), 120, sem, w=4 * s, luz=(0.3, -1), d=10 * s, trama=0.3, rim=0.9, rampa="laton")
        for q in (-1, 1):
            h.trazo(np.array([[x - 46 * s, y - 48 * s + q * 14 * s], [x, y - 48 * s + q * 20 * s], [x + 46 * s, y - 48 * s + q * 14 * s]]),
                    3 * s, sem + 3, alfa=0.7)
        h.trazo(np.array([[x, y - 96 * s], [x, y]]), 3 * s, sem + 5, alfa=0.7)
