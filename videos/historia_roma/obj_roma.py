# -*- coding: utf-8 -*-
"""Objetos e ilustraciones propias de «La historia de Roma» (boceto/guache).

Convenciones: origen (0, 0) en la base del objeto. Todo devuelve `Dib` (tinta y crayón)
que se estampa como pegatina con borde blanco y sombra sobre el mapa continuo.
"""
import math
from functools import lru_cache

import numpy as np

from obj_base import *  # noqa: F401,F403

ROJO_ROMA = (196, 48, 48)
ROJO_VINO = (148, 32, 36)
ORO_ROMA = (236, 184, 52)
BRONCE = (184, 136, 68)
HIERRO = (120, 126, 136)
PURPURA_IMP = (124, 44, 98)
MARMOL = (244, 240, 232)
MARMOL_SOMBRA = (208, 202, 192)
LAUREL_VERDE = (72, 140, 78)
MAR = (186, 214, 216)


# ------------------------------------------------------------------ 1. Orígenes: Choza del Lacio
@lru_cache(maxsize=None)
def choza_lacio():
    """Choza de barro y paja de la Roma primitiva (siglo VIII a.C.)."""
    ops = []
    # Paredes circulares de adobe
    ops += forma(pol((-70, 0), (-70, -80), (70, -80), (70, 0)), (180, 140, 96), 5.2, peso=0.8, sp=8)
    # Puerta de madera
    ops += forma(rect(-20, -60, 20, 0, 4), (110, 75, 50), 4.0, sp=5)
    # Techo cónico de paja
    ops += forma(pol((-95, -75), (0, -165), (95, -75)), (210, 180, 100), 5.4, peso=0.9, sp=9)
    # Textura de paja
    for dx in (-60, -30, 0, 30, 60):
        ops.append(T(linea((dx * 0.8, -150), (dx, -80)), 3.2, peso=0.03))
    return Dib(ops)


# ------------------------------------------------------------------ 2. Estandarte SPQR
@lru_cache(maxsize=None)
def estandarte_spqr():
    """Vexillum romano con águila de oro y letras SPQR."""
    ops = []
    # Asta de madera
    ops += forma(rect(-5, -280, 5, 0, 2), MADERA_OSC, 4.0, sp=4)
    # Barra horizontal
    ops += forma(rect(-65, -270, 65, -258, 2), ORO_ROMA, 4.2, sp=4)
    # Estandarte rojo (tela)
    ops += forma(rect(-55, -258, 55, -135, 3), ROJO_ROMA, 5.0, peso=0.85, sp=8)
    # Flecos dorados
    ops += forma(rect(-55, -135, 55, -125, 2), ORO_ROMA, 3.8, sp=4)
    # Letras "SPQR" estilizadas en oro
    for k, let_x in enumerate((-36, -12, 12, 34)):
        ops += forma(elip(let_x, -195, 8, 12, 0, 1.0, 8), ORO_ROMA, 3.2, sp=3)
    # Águila imperial en la punta
    ops += forma(pol((-22, -282), (0, -305), (22, -282), (0, -275)), ORO_ROMA, 4.4, peso=0.9, sp=5)
    ops += forma(circ(0, -302, 6), ORO_ROMA, 3.6, sp=3)
    return Dib(ops)


# ------------------------------------------------------------------ 3. Legionario Romano
@lru_cache(maxsize=None)
def legionario(f=0, lanza=True):
    """Soldado romano con galea (casco), lorica segmentata y scutum (escudo rojo)."""
    f = f % 4
    ops = []
    # Piernas con caligae (sandalias)
    ops += forma(rect(-28, -60, -10, 0, 3), PIEL_OSC, 4.0, sp=4)
    ops += forma(rect(10, -60, 28, 0, 3), PIEL_OSC, 4.0, sp=4)
    # Sandalias
    ops += forma(rect(-30, -15, -8, 0, 2), MADERA_OSC, 3.5, sp=3)
    ops += forma(rect(8, -15, 30, 0, 2), MADERA_OSC, 3.5, sp=3)
    # Túnica roja bajo la armadura
    ops += forma(pol((-36, -130), (36, -130), (42, -65), (-42, -65)), ROJO_ROMA, 5.0, sp=7)
    # Coraza metálica (lorica segmentata)
    ops += forma(rect(-34, -145, 34, -85, 6), HIERRO, 5.2, peso=0.85, sp=8)
    for y_banda in (-130, -115, -100):
        ops.append(T(linea((-32, y_banda), (32, y_banda)), 3.6, peso=0.03))
    # Cabeza y rostro
    ops += forma(circ(0, -172, 22), PIEL, 4.6, sp=5)
    # Casco romano (galea) de bronce
    ops += forma(pol((-26, -172), (-24, -200), (0, -208), (24, -200), (26, -172)), BRONCE, 4.8, sp=6)
    # Carrilleras del casco
    ops += forma(rect(-24, -182, -14, -160, 2), BRONCE, 3.5, sp=3)
    ops += forma(rect(14, -182, 24, -160, 2), BRONCE, 3.5, sp=3)
    # Penacho rojo en el casco
    ops += forma(elip(0, -214, 18, 10, 0, 1.0, 8), ROJO_ROMA, 4.0, sp=4)
    # Escudo curvo rectangular (Scutum) al frente
    esc_x = -35 if lanza else 0
    ops += forma(rect(esc_x - 30, -145, esc_x + 30, -35, 10), ROJO_ROMA, 5.4, peso=0.9, sp=9)
    # Umbo metálico en el centro del escudo
    ops += forma(circ(esc_x, -90, 12), ORO_ROMA, 4.2, sp=4)
    ops += forma(circ(esc_x, -90, 6), HIERRO, 3.5, sp=3)
    # Alas de águila pintadas en el escudo
    ops += [T(linea((esc_x - 22, -110), (esc_x - 8, -90)), 3.2, peso=0.04),
            T(linea((esc_x + 22, -110), (esc_x + 8, -90)), 3.2, peso=0.04)]
    # Lanza (pilum) en la mano derecha
    if lanza:
        ops += forma(rect(36, -240, 44, 10, 2), MADERA, 3.8, sp=4)
        ops += forma(pol((36, -240), (40, -270), (44, -240)), HIERRO, 4.0, sp=3)
    return Dib(ops)


# ------------------------------------------------------------------ 4. Senador Romano
@lru_cache(maxsize=None)
def senador(f=0):
    """Senador romano con toga blanca y franja púrpura (toga praetexta)."""
    ops = []
    # Toga blanca amplia
    ops += forma(pol((-45, 0), (-55, -145), (0, -170), (55, -145), (45, 0)), MARMOL, 5.4, peso=0.85, sp=9)
    # Franja púrpura senatorial
    ops += forma(pol((-20, -165), (-8, -165), (15, 0), (0, 0)), PURPURA_IMP, 4.4, sp=6)
    # Pliegues de la toga
    for x1, y1, x2, y2 in ((-35, -130, -10, -50), (20, -125, 35, -30), (-15, -80, 5, 0)):
        ops.append(T(linea((x1, y1), (x2, y2)), 3.4, peso=0.03))
    # Rostro maduro y pelo gris
    ops += forma(circ(0, -190, 20), PIEL, 4.5, sp=5)
    ops += forma(curva([(-18, -200), (0, -212), (18, -200)]), GRIS_CL, 4.0, sp=4)
    # Rollo de papiro en la mano
    ops += forma(rect(28, -100, 48, -85, 3), CREMA, 3.6, sp=3)
    return Dib(ops)


# ------------------------------------------------------------------ 5. Julio César / Augusto (Emperador)
@lru_cache(maxsize=None)
def cesar_emperador(f=0):
    """Emperador con toga púrpura, coraza imperial y corona de laurel."""
    ops = []
    # Toga púrpura real
    ops += forma(pol((-50, 0), (-60, -150), (0, -175), (60, -150), (50, 0)), PURPURA_IMP, 5.4, peso=0.9, sp=9)
    # Coraza imperial dorada visible al frente
    ops += forma(rect(-25, -155, 25, -85, 5), ORO_ROMA, 5.0, sp=7)
    # Rostro enérgico
    ops += forma(circ(0, -192, 22), PIEL, 4.6, sp=5)
    # Corona de laurel dorada en la cabeza
    ops += forma(curva([(-20, -202), (0, -215), (20, -202)]), ORO_ROMA, 4.4, sp=5)
    ops += [forma(circ(-16, -204, 5), ORO_ROMA, 3.2, sp=2)[0],
            forma(circ(16, -204, 5), ORO_ROMA, 3.2, sp=2)[0]]
    # Brazo alzado en saludo militar (adlocutio)
    ops += forma(pol((25, -145), (65, -185), (78, -175), (35, -135)), PIEL, 4.2, sp=5)
    return Dib(ops)


# ------------------------------------------------------------------ 6. El Coliseo Romano
@lru_cache(maxsize=None)
def coliseo():
    """Anfiteatro Flavio con tres niveles de arcos de medio punto."""
    ops = []
    # Estructura ovalada base
    ops += forma(pol((-170, 0), (-170, -130), (170, -130), (170, 0)), MARMOL_SOMBRA, 5.6, peso=0.9, sp=10)
    # Cornisas horizontales entre pisos
    for y_piso in (-45, -90, -130):
        ops += forma(rect(-175, y_piso - 6, 175, y_piso, 2), MARMOL, 4.0, sp=4)
    # Arcos en cada nivel
    for nivel, y_base in enumerate((-6, -51, -96)):
        for x_arco in range(-145, 150, 36):
            # Interior oscuro del arco
            ops += forma(pol((x_arco - 11, y_base), (x_arco - 11, y_base - 22),
                             (x_arco, y_base - 32), (x_arco + 11, y_base - 22),
                             (x_arco + 11, y_base)), (48, 44, 46), 3.8, sp=4)
    return Dib(ops)


# ------------------------------------------------------------------ 7. Acueducto Romano
@lru_cache(maxsize=None)
def acueducto():
    """Acueducto de doble arcada de piedra clásica."""
    ops = []
    # Canal superior de agua
    ops += forma(rect(-180, -125, 180, -110, 2), MARMOL, 4.4, sp=5)
    ops += forma(rect(-180, -118, 180, -114, 1), (120, 180, 210), 3.2, sp=3)
    # Pilares y arcos superiores
    ops += forma(rect(-175, -110, 175, -60, 2), MARMOL_SOMBRA, 4.8, sp=7)
    for x_a in range(-140, 150, 56):
        ops += forma(pol((x_a - 16, -60), (x_a - 16, -88), (x_a, -102), (x_a + 16, -88), (x_a + 16, -60)), MAR, 4.0, sp=4)
    # Pilares y arcos inferiores
    ops += forma(rect(-175, -60, 175, 0, 2), MARMOL_SOMBRA, 5.0, sp=8)
    for x_a in range(-140, 150, 56):
        ops += forma(pol((x_a - 18, 0), (x_a - 18, -36), (x_a, -52), (x_a + 18, -36), (x_a + 18, 0)), MAR, 4.2, sp=5)
    return Dib(ops)


# ------------------------------------------------------------------ 8. Galera Naval Romana (Trirreme)
@lru_cache(maxsize=None)
def galera_romana(f=0):
    """Trirreme con espolón de proa, vela cuadrada roja y remos."""
    f = f % 4
    ops = []
    # Casco de madera estilizado con espolón (rostrum)
    ops += forma(pol((-130, -35), (110, -35), (145, -20), (125, 0), (-115, 0), (-140, -15)), MADERA, 5.2, peso=0.85, sp=8)
    # Ojo decorativo en la proa
    ops += forma(circ(110, -22, 5), BLANCO, 3.2, sp=2)
    ops += forma(circ(110, -22, 2), NEGRO, 2.5, sp=2)
    # Mástil central
    ops += forma(rect(-8, -170, 8, -35, 2), MADERA_OSC, 4.4, sp=4)
    # Vela cuadrada roja
    ops += forma(rect(-75, -160, 65, -75, 4), ROJO_ROMA, 5.2, peso=0.88, sp=9)
    # Remos inclinados al agua
    oar_ang = -0.3 + 0.1 * math.sin(f * 1.5)
    for x_remo in range(-80, 80, 24):
        x_fin = x_remo + int(35 * math.cos(oar_ang))
        y_fin = int(35 * math.sin(oar_ang)) + 15
        ops.append(T(linea((x_remo, -10), (x_fin, y_fin)), 3.6, peso=0.04))
    return Dib(ops)


# ------------------------------------------------------------------ 9. Elefante de Aníbal
@lru_cache(maxsize=None)
def elefante_anibal(f=0):
    """Elefante cartaginés de guerra con manta y colmillos."""
    ops = []
    # Cuerpo del elefante
    ops += forma(elip(0, -90, 75, 55, 0, 1.0, 12), GRIS_OSC, 5.6, peso=0.9, sp=10)
    # Patas robustas
    for x_pata in (-45, -15, 25, 55):
        ops += forma(rect(x_pata - 12, -50, x_pata + 12, 0, 4), GRIS_OSC, 4.6, sp=6)
    # Cabeza y oreja grande
    ops += forma(circ(-75, -115, 32), GRIS_OSC, 5.0, sp=7)
    ops += forma(elip(-60, -115, 18, 28, 0.2, 1.0, 8), (95, 95, 110), 4.2, sp=5)
    # Trompa curvada
    ops += forma(pol((-95, -120), (-125, -95), (-115, -65), (-100, -75), (-85, -105)), GRIS_OSC, 4.4, sp=6)
    # Colmillos de marfil
    ops += forma(pol((-90, -100), (-125, -102), (-120, -112)), BLANCO, 3.8, sp=4)
    # Manta cartaginesa sobre el lomo
    ops += forma(rect(-35, -140, 35, -90, 4), PURPURA_IMP, 4.8, sp=6)
    return Dib(ops)


# ------------------------------------------------------------------ 10. Corona de Laurel
@lru_cache(maxsize=None)
def corona_laurel():
    """Corona triunfal de laurel clásica."""
    ops = []
    # Dos ramas curvas
    ops += forma(elip(0, -70, 60, 45, 0, 0.8, 14), LAUREL_VERDE, 4.8, peso=0.6, sp=6)
    # Hojas doradas/verdes
    for ang in np.linspace(0.4, 2.7, 9):
        x = int(60 * math.cos(ang))
        y = int(45 * math.sin(ang)) - 70
        ops += forma(circ(x, y, 9), LAUREL_VERDE, 3.6, sp=3)
        ops += forma(circ(-x, y, 9), LAUREL_VERDE, 3.6, sp=3)
    # Lazo rojo en la base
    ops += forma(circ(0, -25, 12), ROJO_ROMA, 4.0, sp=4)
    return Dib(ops)


# ------------------------------------------------------------------ 11. Templo Romano Clásico
@lru_cache(maxsize=None)
def templo_romano():
    """Templo romano de mármol con escalinata, columnas corintias y frontón triangular."""
    ops = []
    # Escalinata / Podio
    ops += forma(rect(-140, -20, 140, 0, 2), MARMOL_SOMBRA, 5.0, sp=6)
    ops += forma(rect(-130, -35, 130, -20, 2), MARMOL, 4.8, sp=6)
    # Columnas frontales (6 columnas)
    for xc in (-110, -66, -22, 22, 66, 110):
        ops += forma(rect(xc - 7, -135, xc + 7, -35, 2), MARMOL, 4.2, sp=4)
        ops += forma(rect(xc - 9, -142, xc + 9, -135, 1), ORO_ROMA, 3.4, sp=2) # Capitel corintio
    # Entablamento horizontal
    ops += forma(rect(-135, -160, 135, -142, 2), MARMOL, 5.0, sp=6)
    # Frontón triangular (pedimento)
    ops += forma(pol((-140, -160), (0, -220), (140, -160)), MARMOL, 5.4, peso=0.9, sp=8)
    # Relieve escultórico dentro del frontón
    ops += forma(circ(0, -180, 14), ORO_ROMA, 3.8, sp=3)
    return Dib(ops)


# ------------------------------------------------------------------ 12. Arco de Triunfo Romano
@lru_cache(maxsize=None)
def arco_triunfo():
    """Arco de triunfo monumental de tres bóvedas y cuadriga superior."""
    ops = []
    # Estructura masiva
    ops += forma(rect(-120, -160, 120, 0, 4), MARMOL_SOMBRA, 5.4, peso=0.88, sp=8)
    # Bóveda central grande
    ops += forma(pol((-35, 0), (-35, -75), (0, -105), (35, -75), (35, 0)), (44, 40, 42), 4.6, sp=5)
    # Bóvedas laterales menores
    for xl in (-85, 85):
        ops += forma(pol((xl - 18, 0), (xl - 18, -48), (xl, -66), (xl + 18, -48), (xl + 18, 0)), (44, 40, 42), 3.8, sp=4)
    # Columnas adosadas decorativas
    for xc in (-115, -45, 45, 115):
        ops += forma(rect(xc - 5, -150, xc + 5, -10, 2), MARMOL, 3.8, sp=3)
    # Ático superior con inscripción dorada
    ops += forma(rect(-125, -205, 125, -160, 3), MARMOL, 5.0, sp=6)
    for y_linea in (-190, -175):
        ops += forma(rect(-85, y_linea - 3, 85, y_linea + 3, 1), ORO_ROMA, 3.2, sp=3)
    # Estatuas / cuadriga de bronce en la cima
    ops += forma(pol((-30, -205), (0, -240), (30, -205)), ORO_ROMA, 4.4, sp=5)
    return Dib(ops)


# ------------------------------------------------------------------ 13. Guerrero Bárbaro Germano
@lru_cache(maxsize=None)
def barbaro_german(f=0):
    """Guerrero de las tribus germánicas con hacha, escudo redondo y pieles."""
    ops = []
    # Piernas con calzas de cuero
    ops += forma(rect(-25, -55, -8, 0, 3), (120, 85, 55), 4.0, sp=4)
    ops += forma(rect(8, -55, 25, 0, 3), (120, 85, 55), 4.0, sp=4)
    # Túnica y manto de piel de lobo/oso
    ops += forma(pol((-38, -135), (38, -135), (42, -55), (-42, -55)), (88, 70, 56), 5.0, sp=7)
    # Pecho y manto con textura
    ops += forma(rect(-35, -135, 35, -75, 4), (135, 110, 85), 4.8, sp=6)
    # Cabeza y rostro fiero con bigote y barba rubia/pelirroja
    ops += forma(circ(0, -168, 20), PIEL, 4.5, sp=5)
    ops += forma(pol((-22, -160), (0, -135), (22, -160)), (196, 125, 45), 4.4, sp=5) # Barba
    ops += forma(curva([(-22, -178), (0, -195), (22, -178)]), (196, 125, 45), 4.6, sp=5) # Pelo
    # Casco con cuernos estilizados
    ops += forma(pol((-22, -178), (0, -190), (22, -178)), HIERRO, 4.0, sp=4)
    ops += forma(curva([(-18, -185), (-35, -205), (-32, -220)]), BLANCO, 3.8, sp=3)
    ops += forma(curva([(18, -185), (35, -205), (32, -220)]), BLANCO, 3.8, sp=3)
    # Escudo redondo de madera con umbo de hierro
    ops += forma(circ(-35, -95, 28), (145, 75, 50), 5.2, peso=0.85, sp=7)
    ops += forma(circ(-35, -95, 9), HIERRO, 3.8, sp=3)
    # Hacha de combate en la mano alzada
    ops += forma(rect(32, -200, 40, -30, 2), MADERA, 3.8, sp=4)
    ops += forma(pol((30, -200), (62, -215), (58, -180), (30, -190)), HIERRO, 4.5, sp=4)
    return Dib(ops)


# ------------------------------------------------------------------ 14. Jinete de Caballería Romana
@lru_cache(maxsize=None)
def jinete_romano(f=0):
    """Jinete de los equites romanos sobre caballo al galope con capa roja ondeante."""
    f = f % 4
    ops = []
    # Caballo castaño en carrera
    bob = int(6 * math.sin(f * 1.5))
    # Cuerpo del caballo
    ops += forma(elip(0, -90 + bob, 85, 42, 0, 1.0, 14), (110, 68, 42), 5.6, peso=0.9, sp=9)
    # Cuello y cabeza
    ops += forma(pol((50, -105 + bob), (95, -155 + bob), (120, -145 + bob), (85, -85 + bob)), (110, 68, 42), 5.2, sp=7)
    ops += forma(pol((95, -165 + bob), (98, -150 + bob), (90, -150 + bob)), (110, 68, 42), 3.5, sp=2) # Oreja
    # Crin y cola negra
    ops += forma(curva([(55, -100 + bob), (75, -135 + bob), (95, -155 + bob)]), NEGRO, 4.0, sp=4)
    ops += forma(curva([(-80, -95 + bob), (-115, -90 + bob), (-135, -65 + bob)]), NEGRO, 4.5, sp=5)
    # Patas delanteras y traseras extendidas
    ops += forma(pol((45, -75 + bob), (95, -35), (85, -25), (40, -65 + bob)), (110, 68, 42), 4.2, sp=5)
    ops += forma(pol((-55, -75 + bob), (-105, -35), (-95, -25), (-45, -65 + bob)), (110, 68, 42), 4.2, sp=5)
    # Jinete romano montado
    # Capa roja al viento
    ops += forma(pol((-15, -165 + bob), (-75, -150 + bob), (-90, -120 + bob), (-25, -125 + bob)), ROJO_ROMA, 5.0, sp=7)
    # Torso con lorica
    ops += forma(rect(-15, -165 + bob, 15, -110 + bob, 4), HIERRO, 4.8, sp=6)
    # Cabeza y casco
    ops += forma(circ(0, -185 + bob, 16), PIEL, 4.2, sp=4)
    ops += forma(pol((-18, -185 + bob), (0, -205 + bob), (18, -185 + bob)), BRONCE, 4.2, sp=4)
    # Lanza de caballería (hasta) inclinada al frente
    ops += forma(rect(-60, -210 + bob, 130, -204 + bob, 2), MADERA, 3.8, sp=4)
    ops += forma(pol((130, -212 + bob), (155, -207 + bob), (130, -202 + bob)), HIERRO, 3.8, sp=3)
    return Dib(ops)


# ------------------------------------------------------------------ 15. Barco Mercante Romano (Corbita)
@lru_cache(maxsize=None)
def barco_mercante(f=0):
    """Barco de carga romano con casco redondeado, vela beige y ánforas."""
    f = f % 4
    ops = []
    # Casco redondeado y pesado
    ops += forma(pol((-105, -30), (95, -30), (80, 5), (-80, 5)), (140, 95, 60), 5.2, peso=0.88, sp=8)
    # Cubierta y ánforas visibles
    for xa in (-45, -20, 5, 30):
        ops += forma(elip(xa, -38, 10, 16, 0, 1.0, 8), ARCILLA, 3.6, sp=3)
    # Mástil y vela curvada por el viento
    ops += forma(rect(-6, -160, 6, -30, 2), MADERA_OSC, 4.2, sp=4)
    ops += forma(curva([(-65, -150), (15, -135), (65, -150), (50, -60), (-15, -55), (-55, -60)]), CREMA, 5.0, peso=0.85, sp=8)
    # Cola de cisne tradicional en la popa
    ops += forma(curva([(-105, -30), (-120, -55), (-110, -70)]), ORO_ROMA, 4.0, sp=3)
    return Dib(ops)


# ------------------------------------------------------------------ 16. Ánfora de Vino / Aceite
@lru_cache(maxsize=None)
def anfora_vino():
    """Ánfora de terracota clásica con dos asas y sello de cera."""
    ops = []
    # Cuerpo ovalado estilizado
    ops += forma(elip(0, -75, 42, 60, 0, 1.0, 16), ARCILLA, 5.2, peso=0.9, sp=8)
    # Cuello estrecho y boca
    ops += forma(rect(-14, -145, 14, -120, 2), ARCILLA, 4.0, sp=4)
    ops += forma(elip(0, -145, 18, 6, 0, 1.0, 8), ARCILLA, 3.8, sp=3)
    # Pie cónico
    ops += forma(pol((-12, -18), (0, 0), (12, -18)), ARCILLA, 3.8, sp=3)
    # Dos asas laterales
    ops += [T(curva([(-14, -130), (-38, -115), (-28, -85)]), 4.0, peso=0.04),
            T(curva([(14, -130), (38, -115), (28, -85)]), 4.0, peso=0.04)]
    # Sello romano grabado
    ops += forma(circ(0, -75, 12), ROJO_ROMA, 3.5, sp=3)
    return Dib(ops)


# ------------------------------------------------------------------ 17. Moneda Denario de Oro / Plata
@lru_cache(maxsize=None)
def moneda_denario():
    """Denario romano con perfil de emperador con corona de laurel y gráfila perlada."""
    ops = []
    # Disco dorado
    ops += forma(circ(0, -60, 60), ORO_ROMA, 5.6, peso=0.9, sp=10)
    # Borde perlado
    for ang in np.linspace(0, 2 * math.pi, 24, endpoint=False):
        xp = int(52 * math.cos(ang))
        yp = int(52 * math.sin(ang)) - 60
        ops += forma(circ(xp, yp, 3), (190, 140, 35), 2.5, sp=2)
    # Perfil imperial grabado
    ops += forma(pol((-15, -80), (15, -80), (22, -65), (10, -55), (18, -45), (5, -35), (-15, -45)), (190, 140, 35), 4.2, sp=5)
    # Laurel sobre la cabeza del perfil
    ops += forma(curva([(-10, -85), (5, -95), (20, -85)]), LAUREL_VERDE, 3.5, sp=3)
    return Dib(ops)


# ------------------------------------------------------------------ 18. Villa Romana / Insula (Pueblo)
@lru_cache(maxsize=None)
def villa_romana():
    """Villa romana de campo con tejado de terracota rojo y pórtico."""
    ops = []
    # Muros de estuco blanco
    ops += forma(rect(-85, -60, 85, 0, 3), MARMOL, 5.0, peso=0.85, sp=7)
    # Puerta de arco y ventanas
    ops += forma(pol((-15, 0), (-15, -32), (0, -42), (15, -32), (15, 0)), MADERA_OSC, 4.0, sp=4)
    for xw in (-55, 55):
        ops += forma(rect(xw - 12, -45, xw + 12, -25, 2), (48, 44, 46), 3.5, sp=3)
    # Techo a dos aguas de tejas rojas (tegulae)
    ops += forma(pol((-105, -58), (0, -115), (105, -58)), ROJO_ROMA, 5.4, peso=0.9, sp=9)
    # Líneas de tejas
    for xt in (-75, -45, -15, 15, 45, 75):
        ops.append(T(linea((xt * 0.6, -105), (xt, -60)), 3.2, peso=0.03))
    return Dib(ops)


# ------------------------------------------------------------------ 19. Campamento Castrum (Fuerte)
@lru_cache(maxsize=None)
def castrum_fort():
    """Fuerte militar romano con empalizada de madera y torre de vigilancia."""
    ops = []
    # Muralla / empalizada de madera con troncos
    ops += forma(rect(-130, -55, 130, 0, 2), MADERA, 5.2, peso=0.88, sp=8)
    for xt in range(-125, 130, 16):
        ops.append(T(linea((xt, -55), (xt, 0)), 3.6, peso=0.03))
    # Torre de guardia central
    ops += forma(rect(-40, -135, 40, -55, 3), MADERA_OSC, 5.0, sp=7)
    # Techo de la torre
    ops += forma(pol((-52, -135), (0, -175), (52, -135)), ROJO_ROMA, 4.8, sp=6)
    # Ventana saetera
    ops += forma(rect(-8, -115, 8, -90, 1), (30, 25, 25), 3.2, sp=2)
    # Estandarte pequeño en la torre
    ops += forma(rect(0, -210, 3, -175, 1), MADERA, 3.0, sp=2)
    ops += forma(pol((3, -210), (32, -198), (3, -186)), ROJO_ROMA, 3.8, sp=3)
    return Dib(ops)

