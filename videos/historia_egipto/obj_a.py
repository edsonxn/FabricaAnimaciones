# -*- coding: utf-8 -*-
"""Objetos del Antiguo Egipto: Orígenes, Dinastías Tempranas y Reino Antiguo (boceto).
Dibuja elementos originales y exclusivos de Egipto: barca de papiro, paleta de Narmer,
escriba sentado, cartucho con jeroglíficos, pirámide escalonada de Saqqara,
Gran Pirámide de Guiza, Gran Esfinge y trineo de construcción.

Todos son `Dib`; origen en la base del objeto (x centrado, y=0 en la base).
"""
import math
from functools import lru_cache

import numpy as np

import boceto as B
from boceto import (AMARILLO, AZUL, AZUL_CL, AZUL_OSC, BLANCO, GRIS, GRIS_CL, MARRON, NARANJA, PIEL, R, ROJO, ROSA, T, VERDE,
                    VERDE_OSC, Dib, arco_, circ, curva, elip, linea, mano_poli, ondas)
from obj_base import (ARENA, ARENA_OSC, AZUL_EGIPTO, BLANCO_LINO, BRONCE, CALIZA, CELESTE_NILO, GRANITO, MADERA, MADERA_OSC,
                      NEGRO_KOHL, ORO, ORO_OSC, PIEL_CL, PIEL_EGIPCIA, ROJO_EGIPTO, ROJO_OSC, TURQUESA, VERDE_PAPIRO,
                      cerrar, colocar, corona_egipcia, elipse, forma, personaje_egipcio, pol, punto, rayita, rect, trap, trazo)


# ------------------------------------------------------------------ 1. Barca de papiro del Nilo
@lru_cache(maxsize=None)
def barca_papiro():
    """Embarcación tradicional de cañas de papiro atadas, con proa y popa curvadas altas."""
    ops = []
    # Casco de juncos de papiro: arco curvado hacia arriba en ambos extremos
    curva_quilla = curva([(-130, -50), (-110, -25), (-60, -5), (0, 0), (60, -5), (110, -25), (130, -50)], 10)
    curva_borda = curva([(130, -50), (95, -20), (50, -12), (0, -10), (-50, -12), (-95, -20), (-130, -50)], 10)
    casco = np.vstack([curva_quilla, curva_borda])
    ops += forma(casco, VERDE_PAPIRO, 5.0, sp=8)

    # Remates florales de papiro / loto en proa y popa
    for x_lado in (-130, 130):
        ops += forma(elip(x_lado, -56, 10, 14, 0, 1.0, 16), ORO, 4.0, sp=5)

    # Ligaduras de cuerda que atan los haces de papiro
    for x_atadura in (-90, -60, -30, 0, 30, 60, 90):
        ops += [rayita(x_atadura, -11, x_atadura, -3, 3.5)]

    # Cabina central ligera de esteras de junco
    P_cabina = trap(-35, 35, -45, -40, 40, -12)
    ops += forma(P_cabina, ARENA, 4.5, sp=6)
    ops += forma(rect(-36, -50, 36, -45, 2), MADERA, 4.0, sp=5) # Techo

    # Remo timonel en popa
    ops += [trazo((100, -20), (145, 15), w=4.5)]
    ops += forma(elip(142, 12, 8, 18, math.radians(35), 1.0, 14), MADERA, 4.0, sp=5)

    # Olas del río Nilo debajo
    ops += [T(ondas(-140, 140, 8, 5, 25), 3.8, peso=0.08)]
    ops += [T(ondas(-110, 110, 16, 4, 22), 3.2, peso=0.06)]
    return Dib(ops)


# ------------------------------------------------------------------ 2. Paleta de Narmer
@lru_cache(maxsize=None)
def paleta_narmer():
    """Placa ceremonial tallada de limolita que conmemora la unificación de Egipto (c. 3100 a. C.)."""
    ops = []
    # Silueta de escudo con las dos cabezas de la diosa Bat / vaca arriba
    P_placa = [(-65, -180), (-75, -140), (-70, -40), (0, 0), (70, -40), (75, -140), (65, -180), (35, -170), (0, -180), (-35, -170)]
    ops += forma(P_placa, (95, 115, 105), 5.5, sp=8) # Tono piedra limolita verdosa

    # Dos cabezas bovinas de la diosa Hathor / Bat en la parte superior
    for cx in (-45, 45):
        ops += forma(circ(cx, -165, 12, n=14), ORO, 4.0, sp=5)
        # Cuernos curvados de vaca
        ops += [trazo((cx - 8, -172), (cx - 14, -186), (cx - 8, -192), w=3.4)]
        ops += [trazo((cx + 8, -172), (cx + 14, -186), (cx + 8, -192), w=3.4)]

    # Serekh central superior con el pez bagre ('Nar') y cincel ('Mer')
    ops += forma(rect(-16, -176, 16, -152, 2), CALIZA, 3.8, sp=5)
    ops += [trazo((-8, -164), (8, -164), w=3.0)]

    # Relieve central: Rey Narmer con la maza en alto castigando al enemigo
    # Narmer esquemático tallado en relieve blanco/marfil
    ops += forma(trap(-8, 8, -135, -12, 12, -85), CALIZA, 3.5, sp=4) # Torso
    ops += forma(elip(0, -145, 8, 9, 0, 1.0, 12), CALIZA, 3.5, sp=4) # Cabeza
    ops += [trazo((0, -154), (0, -170), w=3.5)] # Corona Blanca Hedjet
    # Brazo levantado con la maza cónica real
    ops += [trazo((8, -132), (20, -145), (28, -155), w=3.6)]
    ops += forma(circ(29, -157, 5, n=8), CALIZA, 3.2, sp=3) # Cabeza de maza piriforme
    # Enemigo arrodillado sumiso
    ops += forma(elip(-22, -90, 7, 7, 0, 1.0, 10), CALIZA, 3.0, sp=3)
    ops += [trazo((-22, -83), (-20, -70), (-30, -68), w=3.2)]

    # Halcón Horus encima de un bloque de papiros
    ops += [trazo((24, -125), (38, -120), (32, -105), w=3.4)]
    ops += [punto(36, -122, w=5.0)]
    return Dib(ops)


# ------------------------------------------------------------------ 3. Escriba sentado con papiro
@lru_cache(maxsize=None)
def escriba_sentado():
    """Escriba egipcio sentado con las piernas cruzadas sosteniendo un rollo de papiro."""
    ops = []
    # Estera tejida sobre el suelo
    ops += forma(rect(-65, -8, 65, 0, 2), ARENA, 4.0, sp=5)

    # Piernas cruzadas estilo oriental
    P_piernas = trap(-55, 55, -45, -60, 60, -8)
    ops += forma(P_piernas, BLANCO_LINO, 5.0, sp=7) # Falda de lino blanco sobre las piernas
    # Rodillas desnudas asomando
    ops += forma(circ(-48, -32, 12, n=12), PIEL_EGIPCIA, 4.0, sp=5)
    ops += forma(circ(48, -32, 12, n=12), PIEL_EGIPCIA, 4.0, sp=5)

    # Rollo de papiro desenrollado sobre las rodillas
    P_papiro = trap(-38, 38, -48, -42, 42, -36)
    ops += forma(P_papiro, CALIZA, 4.2, sp=6)
    # Rollos enrollados a los extremos
    ops += forma(elip(-40, -42, 5, 8, 0, 1.0, 10), ARENA_OSC, 3.5, sp=4)
    ops += forma(elip(40, -42, 5, 8, 0, 1.0, 10), ARENA_OSC, 3.5, sp=4)
    # Líneas de escritura jeroglífica / hierática en tinta negra y roja
    for y_lin in (-44, -40):
        ops += [rayita(-30, y_lin, -10, y_lin, 2.5), rayita(-6, y_lin, 12, y_lin, 2.5), rayita(16, y_lin, 30, y_lin, 2.5)]

    # Torso erguido descubierto
    P_torso = trap(-28, 28, -115, -20, 20, -50)
    ops += forma(P_torso, PIEL_EGIPCIA, 5.0, sp=7)
    # Pecho y costillas sutiles
    ops += [trazo((-14, -85), (0, -82), (14, -85), w=3.0)]

    # Brazos apoyados sobre el papiro
    # Brazo izquierdo sosteniendo el papiro
    ops += forma(pol((-26, -110), (-38, -75), (-25, -50), (-16, -54), (-28, -80), (-18, -108)), PIEL_EGIPCIA, 4.2, sp=5)
    # Brazo derecho sosteniendo el cálamo / pincel
    ops += forma(pol((26, -110), (36, -75), (22, -52), (14, -56), (26, -80), (18, -108)), PIEL_EGIPCIA, 4.2, sp=5)
    # Mano derecha y cálamo
    ops += [R(circ(18, -50, 6, n=8), PIEL_EGIPCIA, peso=0.02, sp=3)]
    ops += [trazo((14, -58), (20, -42), w=3.5)] # Cálamo de caña

    # Cabeza atenta con ojos almendrados de cristal de roca (como el escriba del Louvre)
    cy = -140.0
    ops += forma(rect(-8, -125, 8, -112, 2), PIEL_EGIPCIA, 4.0, sp=5) # Cuello
    ops += forma(elip(0, cy, 24, 26, 0, 1.0, 20), PIEL_EGIPCIA, 4.8, sp=6)

    # Peluca corta negra redonda
    P_peluca = [(-25, cy + 4), (-26, cy - 22), (0, cy - 30), (26, cy - 22), (25, cy + 4), (18, cy + 8), (-18, cy + 8)]
    ops += forma(P_peluca, NEGRO_KOHL, 4.5, sp=6)

    # Ojos penetrantes perfilados de kohl
    for ex in (-10, 10):
        ops += forma(elip(ex, cy - 2, 6, 4, 0, 1.0, 10), BLANCO, 3.2, sp=3)
        ops += [punto(ex, cy - 2, w=5.0)]
        ops += [trazo((ex - 7, cy - 8), (ex + 7, cy - 8), w=2.8)] # Ceja

    # Nariz y labios
    ops += [trazo((0, cy - 5), (2, cy + 4), (-2, cy + 6), w=2.8)]
    ops += [trazo((-6, cy + 12), (6, cy + 12), w=3.0)]
    return Dib(ops)


# ------------------------------------------------------------------ 4. Cartucho real con jeroglíficos
@lru_cache(maxsize=None)
def cartucho_real():
    """Cartucho ovalado con cuerda dorada anudada en la base, conteniendo jeroglíficos protectores:
    el Ankh (vida), el Escarabajo Khepri (renacimiento) y el Ojo de Horus (protección)."""
    ops = []
    # Borde de soga ovalada
    curva_izq = list(arco_(-25, -80, 20, 90, 270, 14))
    curva_der = list(arco_(25, -80, 20, -90, 90, 14))
    P_ovalo = curva_izq + [(-25, -160)] + list(arco_(-25, -160, 20, 180, 360, 14)) + [(45, -80)] + curva_der + [(-25, -60)]
    ops += forma(rect(-38, -185, 38, -15, r=22), (248, 238, 205), 5.5, sp=8) # Fondo papiro claro
    # Doble línea de cuerda dorada
    ops += [T(rect(-38, -185, 38, -15, r=22), 4.5, peso=0.08)]
    ops += [R(rect(-38, -185, 38, -15, r=22), ORO, peso=0.05, sp=5)]
    # Nudo inferior de la cuerda
    ops += forma(rect(-32, -15, 32, -5, 2), ORO, 4.8, sp=5)
    ops += [rayita(-20, -10, 20, -10, 3.2)]

    # JEROGLÍFICO 1: Ojo de Horus / Wedjat (arriba)
    cy_ojo = -150.0
    ops += [trazo((-18, cy_ojo), (0, cy_ojo - 8), (14, cy_ojo), (18, cy_ojo - 2), w=3.8)]
    ops += [trazo((-18, cy_ojo), (0, cy_ojo + 8), (14, cy_ojo), w=3.8)]
    ops += [punto(0, cy_ojo, w=7.0)]
    ops += [trazo((2, cy_ojo + 8), (2, cy_ojo + 18), w=3.2)] # Lágrima
    ops += [trazo((-6, cy_ojo + 8), (-12, cy_ojo + 16), (-4, cy_ojo + 20), w=3.0)] # Espiral

    # JEROGLÍFICO 2: Escarabajo pelotero / Khepri (centro)
    cy_esc = -100.0
    ops += forma(elip(0, cy_esc, 12, 16, 0, 1.0, 16), TURQUESA, 4.0, sp=5)
    ops += forma(elip(0, cy_esc - 18, 8, 6, 0, 1.0, 12), ORO, 3.5, sp=4) # Cabeza
    # Patas del escarabajo
    for lado in (-1, 1):
        ops += [trazo((lado * 10, cy_esc - 12), (lado * 22, cy_esc - 18), (lado * 20, cy_esc - 26), w=3.0)]
        ops += [trazo((lado * 12, cy_esc), (lado * 24, cy_esc), (lado * 22, cy_esc + 8), w=3.0)]
        ops += [trazo((lado * 10, cy_esc + 12), (lado * 22, cy_esc + 18), (lado * 18, cy_esc + 26), w=3.0)]

    # JEROGLÍFICO 3: Ankh / Llave de la Vida (abajo)
    cy_ankh = -50.0
    ops += [T(elip(0, cy_ankh - 14, 8, 12, 0, 1.0, 16), 4.0, peso=0.06)] # Bucle
    ops += [R(elip(0, cy_ankh - 14, 8, 12, 0, 1.0, 16), ORO, peso=0.04, sp=4)]
    ops += [trazo((-15, cy_ankh), (15, cy_ankh), w=4.5)] # Barra horizontal
    ops += [trazo((0, cy_ankh), (0, cy_ankh + 24), w=4.5)] # Tallo vertical
    return Dib(ops)


# ------------------------------------------------------------------ 5. Pirámide escalonada de Saqqara
@lru_cache(maxsize=None)
def piramide_escalonada():
    """Pirámide escalonada del faraón Djoser en Saqqara, diseñada por Imhotep (6 escalones)."""
    ops = []
    # Arena de base
    ops += forma(rect(-140, -10, 140, 0, 3), ARENA_OSC, 4.0, sp=5)

    # 6 escalones decrecientes de piedra caliza
    anchos = [(125, 95, -10, -40),
              (100, 75, -40, -70),
              (80, 60, -70, -100),
              (65, 48, -100, -125),
              (52, 36, -125, -148),
              (40, 25, -148, -170)]

    col_cara_luz = CALIZA
    col_cara_som = (205, 185, 145)

    for w_inf, w_sup, y_inf, y_sup in anchos:
        # Cara en sombra (izquierda)
        P_izq = trap(-w_inf, 0, y_inf, -w_sup, 0, y_sup)
        ops += forma(P_izq, col_cara_som, 4.5, sp=6)
        # Cara iluminada por el sol egipcio (derecha)
        P_der = trap(0, w_inf, y_inf, 0, w_sup, y_sup)
        ops += forma(P_der, col_cara_luz, 4.5, sp=6)
        # Hiladas de bloques de piedra
        y_mid = (y_inf + y_sup) / 2
        ops += [rayita(-w_inf * 0.8, y_mid, w_inf * 0.8, y_mid, 2.5)]

    # Arista central vertical que separa luz y sombra
    ops += [trazo((0, -170), (0, -10), w=4.5)]
    return Dib(ops)


# ------------------------------------------------------------------ 6. Gran Pirámide de Guiza (Keops)
@lru_cache(maxsize=None)
def gran_piramide_guiza():
    """La Gran Pirámide de Keops: revestimiento de caliza pulida blanca y piramidión dorado que brilla."""
    ops = []
    # Duna de arena en la base
    ops += forma(curva([(-160, 0), (-80, -6), (0, 0), (80, -5), (160, 0)], 8), ARENA, 4.5, sp=6)

    # Cara izquierda (en sombra cálida dorada)
    P_izq = pol((-145, 0), (0, -220), (0, 0))
    ops += forma(P_izq, (215, 190, 148), 5.0, sp=7)

    # Cara derecha (en luz radiante de caliza pura)
    P_der = pol((0, -220), (145, 0), (0, 0))
    ops += forma(P_der, CALIZA, 5.0, sp=7)

    # Arista central impecable
    ops += [trazo((0, -220), (0, 0), w=5.0)]

    # Hiladas de bloques horizontales grabadas finamente
    for y_h in np.linspace(-20, -190, 10):
        factor = (220 + y_h) / 220
        ops += [rayita(-140 * factor, y_h, 140 * factor, y_h, 2.6)]

    # Piramidión superior de oro (electrum) que refleja el sol
    P_oro = pol((-18, -192), (0, -220), (18, -192))
    ops += forma(P_oro, ORO, 4.5, sp=5)
    ops += [rayita(0, -220, 0, -192, 3.8)] # Arista del piramidión

    # Destello solar sobre la cúspide
    for rad_a in (0, 45, 90, 135, 180, 225, 270, 315):
        ra = math.radians(rad_a)
        r0, r1 = 12, 28
        ops += [rayita(r0 * math.cos(ra), -220 + r0 * math.sin(ra),
                       r1 * math.cos(ra), -220 + r1 * math.sin(ra), 2.8)]
    return Dib(ops)


# ------------------------------------------------------------------ 7. Gran Esfinge de Guiza
@lru_cache(maxsize=None)
def gran_esfinge():
    """La Gran Esfinge con cuerpo de león recostado sobre la roca viva y rostro de faraón con nemes."""
    ops = []
    # 1. Cuerpo de león
    # Espalda y grupa del león
    curva_lomo = curva([(-130, -50), (-90, -75), (-30, -70), (20, -60), (45, -55)], 8)
    curva_base = curva([(45, 0), (-30, 0), (-90, -5), (-130, 0)], 8)
    P_cuerpo = np.vstack([curva_lomo, [(45, 0)], curva_base[::-1], [(-130, -50)]])
    ops += forma(P_cuerpo, ARENA_OSC, 5.0, sp=8)

    # Cola de león enroscada sobre el muslo
    ops += [trazo((-130, -40), (-145, -25), (-135, -8), (-120, -12), w=4.5)]

    # Garras delanteras extendidas en la arena
    P_pata1 = trap(45, 75, -25, 45, 120, 0)
    P_pata2 = trap(35, 65, -35, 35, 105, -10)
    ops += forma(P_pata2, (185, 155, 115), 4.5, sp=6) # Pata del fondo en sombra
    ops += forma(P_pata1, ARENA_OSC, 4.8, sp=7)       # Pata en primer plano
    # Uñas / dedos de león
    for x_dedo in (95, 105, 115):
        ops += [trazo((x_dedo, -12), (x_dedo + 4, 0), w=3.4)]

    # Pecho ancho del león
    P_pecho = trap(20, 55, -110, 20, 55, -55)
    ops += forma(P_pecho, ARENA_OSC, 5.0, sp=7)

    # 2. Cabeza humana real
    cy = -145.0
    cx = 38.0
    # Cuello de roca sólida
    ops += forma(rect(cx - 15, -120, cx + 15, -105, 4), ARENA_OSC, 4.8, sp=6)
    # Rostro de rey Kefrén
    ops += forma(elip(cx, cy, 22, 25, 0, 1.0, 20), (218, 185, 142), 5.0, sp=7)

    # Tocado Nemes que se abre a los lados
    P_nemes_izq = [(cx - 20, cy - 25), (cx - 40, cy + 15), (cx - 22, cy + 20), (cx - 15, cy - 10)]
    P_nemes_der = [(cx + 20, cy - 25), (cx + 40, cy + 15), (cx + 22, cy + 20), (cx + 15, cy - 10)]
    ops += forma(P_nemes_izq, (180, 150, 110), 4.5, sp=6)
    ops += forma(P_nemes_der, (210, 180, 138), 4.5, sp=6)
    # Rayas del nemes desgastadas por el milenario viento del desierto
    for y_r in (-155, -145, -135):
        ops += [rayita(cx - 30, y_r, cx + 30, y_r, 3.0)]

    # Barba ceremonial rota
    ops += forma(trap(cx - 4, cx + 4, cy + 25, cx - 6, cx + 6, cy + 42), (180, 150, 110), 3.8, sp=4)

    # Ojos y cejas nobles que miran al horizonte oriental hacia el sol naciente
    ops += [trazo((cx - 12, cy - 4), (cx - 3, cy - 4), (cx + 2, cy - 2), w=3.4)]
    ops += [trazo((cx + 6, cy - 4), (cx + 15, cy - 4), (cx + 20, cy - 2), w=3.4)]
    ops += [punto(cx - 6, cy - 4, w=5.0), punto(cx + 11, cy - 4, w=5.0)]
    # Nariz ancha (erosionada por los siglos)
    ops += [trazo((cx, cy - 6), (cx + 3, cy + 5), (cx - 3, cy + 5), w=3.4)]
    # Sonrisa majestuosa y enigmática
    ops += [trazo((cx - 8, cy + 14), (cx + 8, cy + 14), w=3.6)]
    return Dib(ops)


# ------------------------------------------------------------------ 8. Trineo de transporte de bloques
@lru_cache(maxsize=None)
def trineo_bloque():
    """Trineo de madera con un gigantesco bloque de caliza arrastrado sobre rodillos."""
    ops = []
    # Rodillos de troncos de madera en la arena
    for xr in (-60, -30, 0, 30, 60):
        ops += forma(circ(xr, -8, 8, n=12), MADERA_OSC, 4.0, sp=5)
        ops += [R(circ(xr, -8, 4, n=8), MADERA, peso=0.03, sp=3)]

    # Patines del trineo de madera con proa levantada
    curva_patin = curva([(-85, -16), (-80, -16), (75, -16), (90, -28), (95, -38)], 8)
    ops += [T(curva_patin, 6.0, peso=0.1)]
    # Travesaños de unión
    ops += forma(rect(-80, -26, 80, -16, 2), MADERA, 4.5, sp=6)

    # Bloque monumental de caliza blanca de varias toneladas
    P_bloque = trap(-65, 65, -85, -70, 70, -26)
    ops += forma(P_bloque, CALIZA, 5.2, sp=8)
    # Marcas de cantero en ocre rojo
    ops += [trazo((-20, -55), (0, -45), (20, -55), w=3.0), rayita(0, -65, 0, -40, 3.0)]

    # Cuerdas gruesas atadas para arrastre
    ops += [trazo((-70, -22), (-110, -35), w=4.5)]
    ops += [trazo((70, -22), (120, -35), w=4.5)]
    return Dib(ops)
