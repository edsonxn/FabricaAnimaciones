# -*- coding: utf-8 -*-
"""Dibujos de boceto para «La historia de México en 5 minutos» (2/3): MONUMENTOS, ARQUITECTURA, CÓDICES y OBJETOS.
Origen en la BASE del objeto (y = 0 abajo, x centrado)."""
import math
from functools import lru_cache

import boceto as B
import numpy as np

from obj_a import colocar
from obj_base import *  # noqa: F401,F403
from obj_mx1 import (AZUL_EEUU, CAL_BL, GRANA, HIERRO_MX, JADE_MX, MANTA, OBSIDIANA, OCRE_MX, ORO_MX, PIEDRA_V, PIEL_MESO,
                     PLATA_MX, ROJO_BAND, TEZONTLE, TURQ_MX, VERDE_BAND)

SOMBRA_P = (182, 168, 146)
PIEDRA_CL = (218, 208, 186)


def _destello(x, y, r0=14, r1=32, n=8, w=3.0):
    return [T(linea((x + r0 * math.cos(a), y + r0 * math.sin(a)), (x + r1 * math.cos(a), y + r1 * math.sin(a))), w, peso=0.02)
            for a in np.linspace(0, 2 * math.pi, n, endpoint=False)]


@lru_cache(maxsize=None)
def planta_maiz():
    """Planta de maíz (milpa) con hojas arqueadas y dos mazorcas doradas."""
    ops = [T(linea((0, 0), (0, -240)), 6.4, peso=0.08)]
    for y, lado in ((-60, -1), (-95, 1), (-135, -1), (-175, 1), (-205, -1)):
        P = curva([(0, y), (lado * 48, y - 24), (lado * 86, y + 8), (lado * 42, y - 6)], 5)
        ops += forma(P, VERDE_BAND, 4.0, sp=5)
    for y, lado in ((-115, 1), (-160, -1)):
        ops += forma(elip(lado * 22, y - 16, 13, 28, lado * 0.35, 1.0, 16), ORO_MX, 4.2, sp=5)
        ops += [rayita(lado * 16, y - 30, lado * 28, y - 4, 2.2)]
    for dx in (-10, 0, 10):
        ops += [T(linea((0, -240), (dx * 2, -276)), 3.4, peso=0.02)]
    return Dib(ops)


@lru_cache(maxsize=None)
def cacao():
    """Mazorca de cacao estriada con hojas verdes."""
    ops = forma(elip(-28, -90, 44, 24, -0.5, 1.0, 18), VERDE_BAND, 4.0, sp=5)
    ops += forma(elip(32, -84, 44, 24, 0.5, 1.0, 18), VERDE_BAND, 4.0, sp=5)
    ops += forma(elip(0, -100, 48, 76, 0.1, 1.0, 28), OCRE_MX, 5.2, peso=0.4, sp=8)
    for x in (-20, 0, 20):
        ops += [T(curva([(x * 0.5, -168), (x, -100), (x * 0.5, -30)], 5), 2.8, peso=0.02)]
    return Dib(ops)


@lru_cache(maxsize=None)
def cabeza_olmeca():
    """Cabeza colosal olmeca de basalto: casco con banda, ceño firme, nariz ancha y labios gruesos."""
    ops = forma(rect(-120, -14, 120, 0, 3), SOMBRA_P, 4.0, sp=5)
    cont = curva([(-104, -12), (-116, -90), (-106, -184), (-64, -236), (0, -248), (64, -236), (106, -184), (116, -90), (104, -12)], 7)
    ops += forma(cont, PIEDRA_V, 5.6, peso=0.6, sp=10)
    ops += forma(curva([(-108, -156), (-98, -214), (0, -246), (98, -214), (108, -156)], 6).tolist() + [(-108, -156)], SOMBRA_P, 4.8, sp=7)
    ops += forma(rect(-110, -172, 110, -148, 4), PIEDRA_CL, 4.4, sp=6)
    for x in (-70, -24, 24, 70):
        ops += forma(rect(x - 12, -206, x + 12, -172, 2), PIEDRA_CL, 3.4, sp=3)
    for sx in (-1, 1):
        ops += forma(elip(sx * 44, -118, 24, 13, 0, 1.0, 16), SOMBRA_P, 4.2, sp=4)
        ops += [punto(sx * 44, -118, 7)]
        ops += forma(rect(sx * 108 - 10, -146, sx * 108 + 10, -78, 3), PIEDRA_CL, 3.8, sp=4)
    ops += forma(pol((-28, -76), (0, -118), (28, -76)), SOMBRA_P, 4.4, sp=4)
    ops += forma(curva([(-52, -46), (-26, -62), (0, -56), (26, -62), (52, -46), (34, -28), (-34, -28)], 5), SOMBRA_P, 4.8, sp=5)
    ops += [T(linea((-44, -46), (44, -46)), 4.0, peso=0.03)]
    return Dib(ops)


@lru_cache(maxsize=None)
def monte_alban():
    """Plataforma escalonada zapoteca de Monte Albán con estela calendárica."""
    ops = forma(trap(-200, 200, -48, -230, 230, 0), PIEDRA_CL, 4.8, sp=8)
    ops += forma(trap(-146, 146, -96, -170, 170, -48), SOMBRA_P, 4.8, sp=7)
    ops += forma(rect(-96, -156, 96, -96, 3), PIEDRA_CL, 4.6, sp=6)
    ops += forma(pol((-42, 0), (-30, -96), (30, -96), (42, 0)), PIEDRA_V, 4.2, sp=5)
    for y in np.linspace(-12, -88, 6):
        ops += [rayita(-34, y, 34, y, 2.4)]
    ops += forma(rect(-48, -156, 48, -116, 2), OBSIDIANA, 3.6, sp=3)
    ops += forma(rect(-22, -196, 22, -156, 3), GRANA, 4.0, sp=4)
    return Dib(ops)


@lru_cache(maxsize=None)
def piramide_sol():
    """Pirámide del Sol en Teotihuacán: cinco cuerpos escalonados en talud-tablero, escalinata central y sol radiante encima."""
    ops = forma(rect(-250, -10, 250, 0, 3), SOMBRA_P, 4.0, sp=5)
    cuerpos = [(226, 196, 0, -44), (190, 162, -44, -86), (154, 128, -86, -126), (118, 94, -126, -162), (84, 62, -162, -194)]
    for wi, ws, yi, ys in cuerpos:
        ops += forma(trap(-ws, 0, ys, -wi, 0, yi), SOMBRA_P, 4.6, sp=7)
        ops += forma(trap(0, ws, ys, 0, wi, yi), PIEDRA_CL, 4.6, sp=7)
        ops += forma(rect(-ws * 0.92, ys + 4, ws * 0.92, ys + 15, 2), TEZONTLE, 3.6, sp=4)
    ops += forma(pol((-40, 0), (-22, -194), (22, -194), (40, 0)), CAL_BL, 4.4, sp=6)
    for y in np.linspace(-14, -184, 11):
        ops += [rayita(-28, y, 28, y, 2.2)]
    ops += forma(circ(0, -252, 34, n=24), ORO_MX, 4.6, sp=6) + _destello(0, -252, 40, 62, 10, 3.2)
    return Dib(ops)


@lru_cache(maxsize=None)
def piramide_kukulcan():
    """El Castillo de Chichén Itzá: pirámide maya de nueve plataformas escalonadas y templo superior con crestería."""
    ops = forma(rect(-210, -10, 210, 0, 3), SOMBRA_P, 4.0, sp=5)
    for k in range(7):
        wi = 188 - 22 * k
        ws = wi - 14
        yi = -24 * k
        ys = -24 * (k + 1)
        ops += forma(trap(-ws, 0, ys, -wi, 0, yi), SOMBRA_P, 4.2, sp=6)
        ops += forma(trap(0, ws, ys, 0, wi, yi), CAL_BL, 4.2, sp=6)
    ops += forma(pol((-38, 0), (-18, -168), (18, -168), (38, 0)), PIEDRA_CL, 4.4, sp=6)
    for y in np.linspace(-12, -158, 9):
        ops += [rayita(-24, y, 24, y, 2.2)]
    ops += forma(rect(-48, -222, 48, -168, 3), CAL_BL, 4.6, sp=6)
    ops += forma(rect(-36, -242, 36, -222, 2), PIEDRA_CL, 4.0, sp=4)
    for x in (-22, 0, 22):
        ops += forma(rect(x - 6, -206, x + 6, -168, 1), OBSIDIANA, 3.0, sp=2)
    return Dib(ops)


@lru_cache(maxsize=None)
def glifo_cero():
    """Estela maya con la concha del cero y barras y puntos vigesimales."""
    ops = forma(rect(-78, -210, 78, 0, 12), PIEDRA_CL, 5.0, sp=8)
    ops += forma(elip(0, -68, 48, 28, 0, 1.0, 24), JADE_MX, 4.6, sp=6)
    ops += [T(linea((-38, -68), (38, -68)), 3.2, peso=0.02)]
    for x in (-20, 0, 20):
        ops += [T(linea((x, -94), (x, -42)), 2.8, peso=0.02)]
    ops += forma(rect(-48, -132, 48, -114, 4), GRANA, 4.0, sp=4)
    for x in (-32, 0, 32):
        ops += forma(circ(x, -162, 12, n=12), ORO_MX, 3.8, sp=3)
    return Dib(ops)


@lru_cache(maxsize=None)
def atlante_tula():
    """Guerrero colosal tolteca de Tula tallado en piedra."""
    ops = forma(rect(-48, -60, 48, 0, 3), PIEDRA_V, 4.6, sp=6)
    ops += forma(rect(-56, -148, 56, -60, 4), PIEDRA_CL, 4.8, sp=7)
    ops += forma(pol((-34, -132), (0, -114), (34, -132), (24, -100), (-24, -100)), TURQ_MX, 3.8, sp=4)
    ops += forma(rect(-42, -204, 42, -148, 4), PIEDRA_V, 4.6, sp=6)
    ops += forma(rect(-48, -252, 48, -204, 3), OCRE_MX, 4.6, sp=6)
    ops += [punto(-16, -180, 6), punto(16, -180, 6), T(linea((-18, -162), (18, -162)), 3.4, peso=0.02)]
    return Dib(ops)


@lru_cache(maxsize=None)
def aguila_nopal():
    """Señal de Tenochtitlan: islote sobre el lago, nopal con tunas rojas y el águila real devorando la serpiente."""
    ops = forma(elip(0, -12, 120, 24, 0, 1.0, 28), (118, 178, 208), 4.2, sp=6)
    ops += forma(curva([(-76, -12), (-54, -44), (0, -52), (54, -44), (76, -12)], 5), OCRE_MX, 4.4, sp=6)
    for cx, cy, rx, ry, ang in ((0, -76, 22, 34, 0), (-36, -98, 18, 28, -0.45), (36, -98, 18, 28, 0.45), (0, -124, 18, 26, 0)):
        ops += forma(elip(cx, cy, rx, ry, ang, 1.0, 16), VERDE_BAND, 4.2, sp=5)
    for x, y in ((-46, -124), (46, -124), (0, -150)):
        ops += forma(circ(x, y, 7, n=10), GRANA, 3.2, sp=3)
    alas = [(-118, -234), (-52, -198), (-18, -154), (18, -154), (52, -198), (118, -234), (78, -150), (0, -142), (-78, -150)]
    ops += forma(curva(alas, 5, cerrado=True), (154, 102, 58), 4.8, sp=8)
    ops += forma(elip(0, -214, 22, 24, 0, 1.0, 16), (154, 102, 58), 4.4, sp=5)
    ops += forma(pol((18, -218), (44, -212), (22, -202)), ORO_MX, 3.8, sp=3)
    ops += [T(curva([(32, -210), (66, -228), (84, -196), (108, -212)], 5), 5.6, peso=0.04),
            R(curva([(32, -210), (66, -228), (84, -196)], 4), JADE_MX, peso=0.02, sp=3)]
    return Dib(ops)


@lru_cache(maxsize=None)
def templo_mayor():
    """Templo Mayor de México-Tenochtitlan: pirámide escalonada con doble escalinata y los templos de Tláloc (azul) y Huitzilopochtli (rojo)."""
    ops = forma(pol((-240, 0), (-220, 18), (220, 18), (240, 0)), (118, 178, 208), 3.8, sp=6)
    for k in range(5):
        w = 192 - 28 * k
        ops += forma(rect(-w, -46 * (k + 1), w, -46 * k, 3), PIEDRA_CL if k % 2 == 0 else SOMBRA_P, 4.8, peso=0.3, sp=8)
    ops += forma(pol((-48, 0), (-10, 0), (-6, -230), (-34, -230)), CAL_BL, 4.0, sp=5)
    ops += forma(pol((10, 0), (48, 0), (34, -230), (6, -230)), CAL_BL, 4.0, sp=5)
    ops += forma(rect(-86, -306, -8, -230, 3), (78, 136, 198), 4.6, sp=6)
    ops += forma(rect(8, -306, 86, -230, 3), GRANA, 4.6, sp=6)
    ops += forma(pol((-92, -306), (-47, -342), (-4, -306)), (78, 136, 198), 4.0, sp=5)
    ops += forma(pol((4, -306), (47, -342), (92, -306)), GRANA, 4.0, sp=5)
    return Dib(ops)


@lru_cache(maxsize=None)
def chinampa():
    """Chinampa: isla agrícola sobre el lago rodeada de ahuehuetes y milpas de maíz."""
    ops = forma(elip(0, -14, 150, 34, 0, 1.0, 28), (112, 176, 208), 4.2, sp=6)
    ops += forma(rect(-116, -42, 116, -12, 8), (146, 108, 74), 4.6, sp=6)
    ops += forma(rect(-112, -56, 112, -36, 6), VERDE_BAND, 4.4, sp=6)
    for x in (-88, 88):
        ops += [T(linea((x, -46), (x, -126)), 5.4, peso=0.04)]
        ops += forma(elip(x, -138, 24, 38, 0, 1.0, 18), (64, 134, 82), 4.2, sp=5)
    for x in (-42, 0, 42):
        ops += [T(linea((x, -50), (x, -104)), 4.0, peso=0.03)]
        ops += forma(elip(x + 6, -82, 7, 14, 0.3, 1.0, 10), ORO_MX, 3.4, sp=3)
    return Dib(ops)


@lru_cache(maxsize=None)
def epidemia_nube(f=0):
    """Nube oscura de la epidemia de viruela (1520)."""
    circs = [(-86, -96, 56), (-18, -134, 68), (56, -106, 58), (104, -68, 44), (-122, -58, 42), (10, -68, 56)]
    P, _ = B.union_circulos(circs, -18, centro=(0.0, -96.0))
    ops = forma(P, (148, 138, 152), 5.0, peso=0.4, sp=8)
    for x, y in ((-70, -95), (-15, -120), (45, -95), (-30, -65), (30, -65), (75, -70)):
        ops += forma(circ(x, y, 8, n=10), GRANA, 3.0, sp=2)
    return Dib(ops)


@lru_cache(maxsize=None)
def catedral_virreinal():
    """Catedral barroca de la Nueva España: dos torres campanario, fachada de cantera y gran cúpula."""
    ops = forma(rect(-168, -164, 168, 0, 4), PIEDRA_CL, 5.0, sp=8)
    ops += forma(curva([(-82, -164), (-64, -228), (0, -252), (64, -228), (82, -164)], 6), ORO_MX, 4.8, sp=7)
    for sx in (-1, 1):
        cx = sx * 124
        ops += forma(rect(cx - 38, -264, cx + 38, 0, 3), PIEDRA_CL, 4.8, sp=7)
        ops += forma(curva([(cx - 34, -264), (cx, -304), (cx + 34, -264)], 5), TEZONTLE, 4.4, sp=5)
        ops += [T(linea((cx, -304), (cx, -332)), 4.0, peso=0.02), T(linea((cx - 10, -320), (cx + 10, -320)), 4.0, peso=0.02)]
        ops += forma(rect(cx - 14, -232, cx + 14, -188, 6), OBSIDIANA, 3.6, sp=3)
    ops += forma(curva([(-42, 0), (-42, -96), (0, -118), (42, -96), (42, 0)], 5), (124, 84, 56), 4.6, sp=6)
    ops += forma(circ(0, -142, 20, n=16), TURQ_MX, 3.8, sp=4)
    return Dib(ops)


@lru_cache(maxsize=None)
def cerro_mina_plata():
    """Cerro minero de Zacatecas / Guanajuato con bocamina y vetas brillantes de plata."""
    ops = forma(curva([(-230, 0), (-140, -116), (-56, -236), (0, -268), (56, -236), (140, -116), (230, 0)], 7), (184, 112, 78), 5.6, peso=0.6, sp=10)
    ops += forma(curva([(-38, 0), (-38, -68), (0, -88), (38, -68), (38, 0)], 5), OBSIDIANA, 4.4, sp=5)
    for x, y in ((-68, -124), (0, -168), (64, -118), (-34, -192), (42, -186)):
        ops += forma(pol((x - 16, y), (x, y - 22), (x + 16, y), (x, y + 12)), PLATA_MX, 3.6, sp=3)
    return Dib(ops)


@lru_cache(maxsize=None)
def real_de_a_ocho():
    """Moneda de plata novohispana (Real de a ocho columnario) y lingotes de plata."""
    ops = forma(elip(0, -104, 96, 96, 0, 1.0, 36), PLATA_MX, 5.4, peso=0.5, sp=8)
    ops += [T(elip(0, -104, 80, 80, 0, 1.0, 32), 3.0, peso=0.04)]
    for cx in (-34, 34):
        ops += forma(rect(cx - 9, -150, cx + 9, -62, 2), HIERRO_MX, 3.6, sp=3)
        ops += forma(rect(cx - 14, -160, cx + 14, -150, 2), ORO_MX, 3.2, sp=3)
    ops += forma(pol((-118, 0), (-54, 0), (-64, -32), (-108, -32)), PLATA_MX, 4.2, sp=4)
    ops += forma(pol((54, 0), (118, 0), (108, -32), (64, -32)), PLATA_MX, 4.2, sp=4)
    return Dib(ops)


@lru_cache(maxsize=None)
def campana_dolores(f=0):
    """La Campana de Dolores repicando con ondas sonoras."""
    ops = forma(rect(-64, -238, 64, -208, 4), (132, 88, 56), 4.6, sp=6)
    ops += forma(pol((-48, -208), (48, -208), (82, -84), (108, -42), (-108, -42), (-82, -84)), ORO_MX, 5.4, sp=8)
    ops += forma(elip(0, -24, 22, 22, 0, 1.0, 16), ORO_MX, 4.4, sp=4)
    for lado in (-1, 1):
        for r in (128, 156):
            a0, a1 = (150, 210) if lado < 0 else (-30, 30)
            ops += [T(arco_(0, -110, r, a0, a1, 10), 4.0, peso=0.03)]
    return Dib(ops)


@lru_cache(maxsize=None)
def libro_constitucion(anio="1917"):
    """Libro abierto de la Constitución (1857 o 1917) con listón tricolor."""
    ops = forma(pol((-146, -18), (-8, -6), (-8, -188), (-146, -202)), MANTA, 5.0, sp=8)
    ops += forma(pol((146, -18), (8, -6), (8, -188), (146, -202)), MANTA, 5.0, sp=8)
    ops += forma(rect(-10, -192, 10, -4, 2), GRANA, 4.2, sp=4)
    for k in range(5):
        y = -164 + 28 * k
        ops += [rayita(-122, y, -28, y + 6, 2.8), rayita(28, y + 6, 122, y, 2.8)]
    ops += forma(pol((-18, -6), (-6, 36), (6, -6)), VERDE_BAND, 3.6, sp=3)
    ops += forma(pol((0, -6), (12, 36), (22, -6)), ROJO_BAND, 3.6, sp=3)
    return Dib(ops)


@lru_cache(maxsize=None)
def fuerte_puebla():
    """Fuerte de Loreto y Guadalupe en Puebla (5 de mayo de 1862) con bandera mexicana."""
    ops = forma(trap(-180, 180, -120, -210, 210, 0), PIEDRA_CL, 5.0, sp=8)
    for k in range(5):
        x = -156 + 78 * k - 18
        ops += forma(rect(x, -148, x + 36, -120, 2), PIEDRA_CL, 4.2, sp=4)
    ops += forma(curva([(-36, 0), (-36, -64), (0, -82), (36, -64), (36, 0)], 5), (112, 78, 52), 4.4, sp=5)
    ops += [T(linea((0, -148), (0, -256)), 5.0, peso=0.05)]
    ops += forma(rect(0, -254, 32, -202, 1), VERDE_BAND, 3.6, sp=4)
    ops += forma(rect(32, -254, 64, -202, 1), MANTA, 3.6, sp=4)
    ops += forma(rect(64, -254, 96, -202, 1), ROJO_BAND, 3.6, sp=4)
    return Dib(ops)


@lru_cache(maxsize=None)
def palacio_bellas_artes():
    """Palacio de Bellas Artes: fachada de mármol blanco y gran cúpula naranja y dorada."""
    ops = forma(rect(-190, -142, 190, 0, 4), CAL_BL, 5.0, sp=8)
    ops += forma(curva([(-96, -142), (-78, -220), (0, -248), (78, -220), (96, -142)], 6), ORO_MX, 5.0, sp=7)
    ops += forma(curva([(-64, -142), (-48, -208), (0, -232), (48, -208), (64, -142)], 5), GRANA, 4.2, sp=5)
    for x in np.linspace(-152, 152, 7):
        ops += forma(rect(x - 8, -132, x + 8, -12, 2), PIEDRA_CL, 3.6, sp=4)
    ops += forma(curva([(-42, 0), (-42, -78), (0, -98), (42, -78), (42, 0)], 5), OBSIDIANA, 4.2, sp=4)
    return Dib(ops)


@lru_cache(maxsize=None)
def torre_petroleo():
    """Torre petrolera de 1938 con chorro de petróleo brotando en lo alto."""
    ops = [T(linea((-78, 0), (-22, -240)), 6.0, peso=0.08), T(linea((78, 0), (22, -240)), 6.0, peso=0.08)]
    for y0, y1, w0, w1 in ((0, -60, 78, 64), (-60, -120, 64, 50), (-120, -180, 50, 36), (-180, -240, 36, 22)):
        ops += [T(linea((-w1, y1), (w1, y1)), 4.6, peso=0.03), T(linea((-w0, y0), (w1, y1)), 3.6, peso=0.03),
                T(linea((w0, y0), (-w1, y1)), 3.6, peso=0.03)]
    ops += forma(curva([(-12, -240), (-58, -304), (0, -326), (58, -304), (12, -240)], 6), OBSIDIANA, 4.6, sp=6)
    return Dib(ops)


@lru_cache(maxsize=None)
def fabrica_moderna():
    """Planta industrial moderna con techo en diente de sierra, engrane y torre corporativa."""
    ops = forma(rect(-190, -120, 80, 0, 3), PIEDRA_CL, 4.8, sp=7)
    for x in (-190, -100, -10):
        ops += forma(pol((x, -120), (x + 45, -168), (x + 90, -120)), GRANA, 4.4, sp=5)
    ops += forma(rect(80, -256, 176, 0, 3), (96, 148, 188), 4.8, sp=7)
    for y in (-220, -180, -140, -100, -60):
        ops += [rayita(96, y, 160, y, 2.8)]
    ops += forma(circ(-56, -62, 32, n=20), ORO_MX, 4.4, sp=5) + forma(circ(-56, -62, 12, n=12), OBSIDIANA, 3.6, sp=3)
    return Dib(ops)


@lru_cache(maxsize=None)
def paloma_68():
    """Paloma blanca de la paz y aros olímpicos de México 68."""
    ops = []
    cols = ((58, 118, 188), OBSIDIANA, ROJO_BAND, ORO_MX, VERDE_BAND)
    pos = ((-88, -64), (0, -64), (88, -64), (-44, -26), (44, -26))
    for (x, y), c in zip(pos, cols):
        ops += [T(circ(x, y, 34, n=24), 5.2, peso=0.04), R(elip(x, y, 34, 34, n=20), c, peso=0.01, sp=3)]
    P = [(-92, -168), (-34, -158), (0, -218), (44, -168), (98, -186), (52, -128), (-22, -122)]
    ops += forma(curva(P, 5, cerrado=True), MANTA, 4.8, sp=7)
    return Dib(ops)


@lru_cache(maxsize=None)
def urna_voto():
    """Urna electoral con boleta entrando por la ranura."""
    ops = forma(rect(-84, -128, 84, 0, 6), (218, 228, 236), 4.8, sp=7)
    ops += forma(rect(-92, -142, 92, -124, 4), OBSIDIANA, 4.4, sp=5)
    ops += forma(pol((-34, -134), (-26, -212), (34, -204), (26, -134)), MANTA, 4.4, sp=5)
    ops += [T(linea((-22, -64), (22, -20)), 5.0, peso=0.03), T(linea((22, -64), (-22, -20)), 5.0, peso=0.03)]
    return Dib(ops)


@lru_cache(maxsize=None)
def angel_independencia():
    """El Ángel de la Independencia: pedestal de cantera, alta columna corintia y la Victoria Alada de oro."""
    ops = forma(rect(-74, -68, 74, 0, 3), PIEDRA_CL, 4.8, sp=6)
    ops += forma(rect(-22, -242, 22, -68, 2), CAL_BL, 4.8, sp=6)
    ops += forma(rect(-34, -256, 34, -240, 2), PIEDRA_CL, 4.2, sp=4)
    ops += forma(pol((-46, -312), (-12, -288), (12, -288), (46, -312), (24, -268), (-24, -268)), ORO_MX, 4.4, sp=5)
    ops += forma(elip(0, -282, 14, 28, 0, 1.0, 16), ORO_MX, 4.4, sp=5)
    ops += forma(circ(0, -318, 10, n=12), ORO_MX, 4.0, sp=3)
    ops += [T(circ(22, -316, 10, n=12), 3.6, peso=0.02)]
    return Dib(ops + _destello(0, -304, 34, 54, 8, 2.8))
