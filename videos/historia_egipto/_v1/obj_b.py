# -*- coding: utf-8 -*-
"""Objetos del Reino Medio y Reino Nuevo de Egipto (boceto).
Dibuja monumentos y símbolos icónicos: el templo y obelisco de Karnak, el carro de guerra real,
el barco de la expedición a Punt de Hatshepsut, el sol radiante de Atón con manos de vida,
la máscara funeraria de oro de Tutankamón, la fachada colosal de Abu Simbel y el Tratado de Kadesh.

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
                      cerrar, colocar, elipse, forma, pol, punto, rayita, rect, trap, trazo)


# ------------------------------------------------------------------ 1. Pilono monumental de Karnak
@lru_cache(maxsize=None)
def templo_karnak():
    """Entrada monumental al templo de Amón en Karnak: pilono doble con muros inclinados,
    mástiles con estandartes y columnas papiriformes."""
    ops = []
    # Explanada de piedra arenisca
    ops += forma(rect(-160, -8, 160, 0, 2), ARENA_OSC, 4.5, sp=6)

    # 1. Torre izquierda del pilono (talud egipcio característico)
    P_torre_izq = trap(-150, -45, -165, -158, -35, -8)
    ops += forma(P_torre_izq, (225, 198, 155), 5.2, sp=8)
    # Cornisa de gola egipcia decorada en lo alto
    ops += forma(trap(-154, -41, -175, -150, -45, -165), (200, 165, 120), 4.5, sp=6)

    # 2. Torre derecha del pilono
    P_torre_der = trap(45, 150, -165, 35, 158, -8)
    ops += forma(P_torre_der, (235, 208, 165), 5.2, sp=8)
    # Cornisa de gola derecha
    ops += forma(trap(41, 154, -175, 45, 150, -165), (200, 165, 120), 4.5, sp=6)

    # 3. Puerta central de granito
    P_portal = trap(-35, 35, -135, -35, 35, -8)
    ops += forma(P_portal, GRANITO, 5.0, sp=7)
    # Vano oscuro de paso hacia la sala hipóstila
    ops += forma(rect(-18, -115, 18, -8, 2), (50, 42, 45), 4.5, sp=6)
    # Disco solar alado sobre el dintel de la puerta
    ops += forma(circ(0, -125, 7, n=12), ORO, 3.8, sp=4)
    ops += [trazo((-26, -123), (-8, -125), w=3.4), trazo((8, -125), (26, -123), w=3.4)] # Alas desplegadas

    # 4. Mástiles de cedro del Líbano con banderolas rojas y doradas
    for mx in (-110, -75, 75, 110):
        ops += [trazo((mx, -195), (mx, -8), w=4.5)] # Mástil alto
        # Banderola ondeando al viento
        P_bandera = [(mx, -195), (mx + 28, -185), (mx, -175)]
        ops += forma(P_bandera, ROJO_EGIPTO, 3.6, sp=4)

    # 5. Columnas con capiteles de papiro abierto detrás del portal
    for cx in (-18, 18):
        ops += forma(rect(cx - 5, -155, cx + 5, -135, 2), ARENA, 3.8, sp=4)
        ops += forma(trap(cx - 10, cx + 10, -165, cx - 6, cx + 6, -155), VERDE_PAPIRO, 3.8, sp=4)
    return Dib(ops)


# ------------------------------------------------------------------ 2. Obelisco de granito rosa
@lru_cache(maxsize=None)
def obelisco():
    """Obelisco monolítico de granito rosa de Asuán con piramidión de electro dorado y jeroglíficos."""
    ops = []
    # Pedestal cúbico de granito
    ops += forma(trap(-30, 30, -32, -36, 36, 0), GRANITO, 5.0, sp=7)
    ops += forma(rect(-26, -42, 26, -32, 2), (150, 105, 98), 4.5, sp=6)

    # Fuste cuadrangular que se estrecha suavemente hacia arriba
    # Mitad izquierda en sombra
    P_fuste_izq = trap(-18, 0, -210, -22, 0, -42)
    ops += forma(P_fuste_izq, (160, 112, 105), 4.8, sp=7)
    # Mitad derecha en luz
    P_fuste_der = trap(0, 18, -210, 0, 22, -42)
    ops += forma(P_fuste_der, GRANITO, 4.8, sp=7)
    # Arista central vertical perfecta
    ops += [trazo((0, -210), (0, -42), w=4.5)]

    # Columna central de jeroglíficos tallados
    for yh in np.linspace(-60, -190, 8):
        ops += [R(circ(0, yh, 4, n=8), ORO, peso=0.03, sp=3)]
        ops += [rayita(-6, yh + 8, 6, yh + 8, 2.5)]

    # Piramidión de oro / electrum en la cúspide
    P_piramidion = pol((-18, -210), (0, -245), (18, -210))
    ops += forma(P_piramidion, ORO, 4.5, sp=5)
    ops += [rayita(0, -245, 0, -210, 3.8)] # Arista del piramidión

    # Destello de luz divina en la punta
    for ang in (30, 90, 150):
        rad = math.radians(ang)
        ops += [rayita(10 * math.cos(rad), -245 - 10 * math.sin(rad),
                       24 * math.cos(rad), -245 - 24 * math.sin(rad), 2.8)]
    return Dib(ops)


# ------------------------------------------------------------------ 3. Carro de guerra egipcio / faraónico
@lru_cache(maxsize=None)
def carro_faraon():
    """Carro de guerra real ligero: caja dorada con relieves, rueda de 6 radios,
    carcaj con flechas y lanza, y tiro de caballos veloces."""
    ops = []
    # 1. Rueda de 6 radios de madera doblada
    cx_r, cy_r = -45.0, -32.0
    r_ext = 30.0
    ops += forma(circ(cx_r, cy_r, r_ext, n=24), MADERA_OSC, 5.0, sp=7)
    ops += [T(circ(cx_r, cy_r, r_ext - 4, n=20), 3.8)] # Llanta
    ops += forma(circ(cx_r, cy_r, 7, n=12), BRONCE, 4.0, sp=4) # Cubo central
    # 6 radios
    for i in range(6):
        a = math.radians(60 * i)
        ops += [rayita(cx_r + 6 * math.cos(a), cy_r + 6 * math.sin(a),
                       cx_r + (r_ext - 4) * math.cos(a), cy_r + (r_ext - 4) * math.sin(a), 3.2)]

    # 2. Caja del carro (madera dorada repujada con barandilla curvada)
    P_caja = [(-65, -80), (-20, -92), (10, -78), (15, -35), (-65, -35)]
    ops += forma(P_caja, ORO, 5.0, sp=8)
    ops += forma(rect(-60, -75, 5, -40, 4), (200, 50, 45), 4.0, sp=6) # Panel rojo decorado

    # 3. Carcajes dobles cruzados con flechas y arcos compuestos
    ops += forma(trap(-30, -18, -115, -45, -35, -45), ORO, 4.0, sp=5)
    # Flechas asomando
    for fx in (-28, -24, -20):
        ops += [rayita(fx, -115, fx + 5, -132, 2.8)]
        ops += [punto(fx + 5, -132, w=5.0)]

    # 4. Lanza de guerra fijada al carro
    ops += [trazo((-40, -45), (-10, -145), w=4.0)]
    ops += forma(pol((-12, -145), (-8, -162), (-4, -145)), BRONCE, 3.5, sp=3)

    # 5. Lanza de enganche y yugo hacia los caballos
    ops += [trazo((10, -40), (85, -55), (105, -70), w=4.8)] # Timón curvado
    ops += forma(rect(80, -78, 100, -70, 2), MADERA, 4.0, sp=4) # Yugo

    # 6. Silueta estilizada del corcel de guerra egipcio
    # Pecho y grupa del caballo
    curva_caballo = curva([(60, -45), (85, -80), (120, -85), (135, -60), (125, -20), (115, 0)], 8)
    ops += forma(curva_caballo, (185, 125, 80), 4.8, sp=7) # Caballo castaño
    # Cuello y cabeza orgullosa
    P_cuello = trap(105, 125, -125, 85, 120, -85)
    ops += forma(P_cuello, (185, 125, 80), 4.8, sp=6)
    ops += forma(elip(125, -135, 12, 18, math.radians(-30), 1.0, 16), (185, 125, 80), 4.5, sp=5)
    # Penacho de plumas de avestruz de color azul y rojo sobre la cabeza del caballo
    P_penacho = [(120, -148), (115, -178), (135, -175), (130, -148)]
    ops += forma(P_penacho, CELESTE_NILO, 4.0, sp=5)
    ops += forma([(122, -148), (120, -172), (132, -170), (128, -148)], ROJO_EGIPTO, 3.5, sp=4)

    # Riendas doradas tensadas desde el carro hasta la boca del corcel
    ops += [trazo((-25, -80), (60, -95), (128, -130), w=3.4)]
    return Dib(ops)


# ------------------------------------------------------------------ 4. Barco de expedición a Punt (Hatshepsut)
@lru_cache(maxsize=None)
def barco_punt():
    """Gran navío egipcio de la reina Hatshepsut para la legendaria expedición comercial al país de Punt.
    Casco con soga tensora (hogging truss), vela cuadrada izada y árboles de mirra en cubierta."""
    ops = []
    # Casco marinero de cedro con proa y popa curvadas altas sobre las olas del Mar Rojo
    curva_quilla = curva([(-140, -45), (-110, -20), (-50, -5), (0, 0), (60, -5), (110, -20), (145, -45)], 10)
    curva_borda = curva([(145, -45), (100, -22), (50, -16), (0, -15), (-50, -16), (-100, -22), (-140, -45)], 10)
    casco = np.vstack([curva_quilla, curva_borda])
    ops += forma(casco, MADERA, 5.2, sp=8)

    # Mástil doble (bípode) izado en el centro
    ops += [trazo((-6, 0), (0, -180), w=4.5), trazo((6, 0), (0, -180), w=4.5)]

    # Vergas superior e inferior de la gran vela cuadrada
    ops += [trazo((-95, -165), (95, -165), w=4.5)] # Verga alta
    ops += [trazo((-85, -60), (85, -60), w=4.5)]   # Verga baja

    # Gran vela de lino blanco hinchada por el viento
    curva_vela_izq = [(-95, -165), (-105, -115), (-85, -60)]
    curva_vela_der = [(95, -165), (105, -115), (85, -60)]
    P_vela = np.vstack([curva_vela_izq, [(85, -60)], curva_vela_der[::-1], [(-95, -165)]])
    ops += forma(P_vela, BLANCO_LINO, 4.8, sp=7)
    # Costuras de la vela
    for xv in (-50, 0, 50):
        ops += [rayita(xv, -162, xv, -63, 2.5)]

    # Cable de tensión (truss) que recorre el barco de proa a popa sostenido por horquillas
    ops += [trazo((-120, -38), (-40, -55), (40, -55), (120, -38), w=3.8)]

    # Carga de valiosos árboles de mirra e incienso en cestas de mimbre sobre cubierta
    for xc in (-60, -35, 35, 60):
        ops += forma(trap(xc - 10, xc + 10, -30, xc - 12, xc + 12, -16), ARENA_OSC, 3.8, sp=4) # Cesta
        # Follaje verde fresco del árbol de mirra
        ops += forma(circ(xc, -40, 11, n=12), VERDE_PAPIRO, 3.8, sp=5)
        ops += [R(circ(xc, -40, 7, n=10), (90, 145, 80), peso=0.03, sp=3)]

    # Dos grandes remos de gobierno en la popa
    ops += [trazo((115, -20), (155, 15), w=4.5)]
    ops += forma(elip(152, 12, 7, 18, math.radians(35), 1.0, 12), MADERA_OSC, 4.0, sp=4)

    # Olas turquesas del Mar Rojo
    ops += [T(ondas(-150, 150, 8, 5, 26), 4.0, peso=0.08)]
    ops += [T(ondas(-120, 120, 16, 4, 22), 3.4, peso=0.06)]
    return Dib(ops)


# ------------------------------------------------------------------ 5. Disco solar de Atón (Akenatón y Nefertiti)
@lru_cache(maxsize=None)
def disco_aton():
    """El disco solar de Atón: esfera de oro de la que descienden rayos que terminan
    en manos humanas benevolentes que ofrecen la llave de la vida (Ankh)."""
    ops = []
    cx, cy = 0.0, -180.0
    r_sol = 36.0

    # 1. Disco solar central radiante
    ops += forma(circ(cx, cy, r_sol, n=32), ORO, 5.5, sp=8)
    ops += [R(circ(cx, cy, r_sol - 6, n=24), (255, 215, 90), peso=0.06, sp=6)]
    # Uraeus sagrado enrollado alrededor del disco solar
    ops += [T(arco_(cx, cy + r_sol - 4, 14, 0, 180, 12), 4.0)]
    ops += [trazo((cx, cy + r_sol + 8), (cx + 4, cy + r_sol + 16), w=3.4)]

    # 2. Rayos solares que se abren hacia abajo cubriendo todo Egipto
    angulos = [-75, -60, -45, -30, -15, 0, 15, 30, 45, 60, 75]
    for a_deg in angulos:
        rad = math.radians(a_deg)
        x0 = cx + r_sol * math.sin(rad)
        y0 = cy + r_sol * math.cos(rad)
        largo = 130 + 20 * math.cos(rad * 2)
        x1 = cx + largo * math.sin(rad)
        y1 = cy + largo * math.cos(rad)

        # Trazo del rayo dorado
        ops += [trazo((x0, y0), (x1, y1), w=3.5)]

        # Mano en el extremo del rayo
        ops += forma(circ(x1, y1, 5, n=8), ORO, 3.0, sp=3)
        # Dedos extendidos
        ops += [trazo((x1, y1), (x1 + 4 * math.sin(rad), y1 + 4 * math.cos(rad)), w=2.8)]

        # Los rayos centrales portan la llave de la vida (Ankh)
        if abs(a_deg) <= 30:
            ya = y1 + 10
            ops += forma(elip(x1, ya, 4, 6, 0, 1.0, 10), ORO, 2.8, sp=2) # Bucle
            ops += [trazo((x1 - 5, ya + 6), (x1 + 5, ya + 6), w=2.8)]     # Barra
            ops += [trazo((x1, ya + 6), (x1, ya + 15), w=2.8)]            # Tallo
    return Dib(ops)


# ------------------------------------------------------------------ 6. Máscara de oro de Tutankamón
@lru_cache(maxsize=None)
def mascara_tutankamon():
    """La máscara funeraria de oro macizo de Tutankamón (tumba KV62):
    oro pulido, bandas de lapislázuli, Uraeus y Buitre en la frente, ojos de obsidiana y barba divina."""
    ops = []
    cy = -140.0

    # 1. Alas del tocado Nemes que caen a los lados
    P_ala_izq = [(-45, cy - 20), (-70, cy + 30), (-45, cy + 65), (-25, cy + 65), (-30, cy + 20)]
    P_ala_der = [(45, cy - 20), (70, cy + 30), (45, cy + 65), (25, cy + 65), (30, cy + 20)]
    ops += forma(P_ala_izq, ORO, 5.0, sp=7)
    ops += forma(P_ala_der, ORO, 5.0, sp=7)
    # Franjas alternadas de oro y lapislázuli en las alas del nemes
    for y_f in range(int(cy - 10), int(cy + 60), 12):
        ops += forma(rect(-65, y_f, -32, y_f + 6, 1), AZUL_EGIPTO, 3.2, sp=4)
        ops += forma(rect(32, y_f, 65, y_f + 6, 1), AZUL_EGIPTO, 3.2, sp=4)

    # 2. Cabeza y tocado superior
    P_tocado = [(-46, cy - 20), (-42, cy - 65), (0, cy - 78), (42, cy - 65), (46, cy - 20)]
    ops += forma(P_tocado, ORO, 5.2, sp=8)
    # Franjas concéntricas de lapislázuli sobre la frente
    for i, a_r in enumerate(range(int(cy - 65), int(cy - 25), 10)):
        if i % 2 == 0:
            ops += [T(arco_(0, a_r, 40 - i * 3, 200, 340, 14), 4.0)]
            ops += [R(arco_(0, a_r, 40 - i * 3, 205, 335, 12), AZUL_EGIPTO, peso=0.04, sp=4)]

    # 3. Emblemas reales sobre la frente: Buitre Nekhbet y Cobra Wadjet
    # Buitre a la izquierda
    ops += forma(elip(-10, cy - 65, 5, 8, math.radians(-15), 1.0, 10), ORO, 3.2, sp=3)
    ops += [trazo((-10, cy - 73), (-14, cy - 80), w=2.8)] # Pico
    # Cobra a la derecha
    ops += [trazo((10, cy - 60), (10, cy - 75), (6, cy - 80), (12, cy - 84), w=3.4)]
    ops += forma(circ(10, cy - 84, 4, n=8), ORO, 3.0, sp=2)

    # 4. Rostro del joven rey de oro puro
    ops += forma(elip(0, cy, 30, 34, 0, 1.0, 26), (255, 218, 95), 5.2, sp=8)

    # 5. Ojos de cuarzo y obsidiana con delineado largo de lapislázuli
    for ex, sx in ((-14, -1), (14, 1)):
        # Contorno alargado de kohl / lapislázuli
        ops += [trazo((ex - 10 * sx, cy - 4), (ex + 12 * sx, cy - 4), (ex + 18 * sx, cy - 2), w=3.8)]
        ops += [trazo((ex - 10 * sx, cy - 4), (ex + 2 * sx, cy + 4), (ex + 12 * sx, cy - 4), w=3.4)]
        # Globo ocular blanco y pupila negra
        ops += forma(elip(ex, cy - 1, 6, 4, 0, 1.0, 10), BLANCO, 3.0, sp=3)
        ops += [punto(ex, cy - 1, w=6.0)]
        # Ceja curva de lapislázuli
        ops += [trazo((ex - 12 * sx, cy - 12), (ex + 2 * sx, cy - 15), (ex + 16 * sx, cy - 10), w=3.8)]

    # 6. Nariz recta y labios carnosos jóvenes
    ops += [trazo((0, cy - 6), (3, cy + 6), (-3, cy + 8), (0, cy + 9), w=3.2)]
    ops += forma(rect(-8, cy + 14, 8, cy + 22, 2), (230, 165, 80), 3.5, sp=4) # Labios
    ops += [trazo((-8, cy + 18), (8, cy + 18), w=3.0)]

    # 7. Barba divina tubular con patrón trenzado azul y oro
    P_barba = trap(-7, 7, cy + 34, -9, 9, cy + 85)
    ops += forma(P_barba, AZUL_EGIPTO, 4.5, sp=6)
    for y_b in range(int(cy + 42), int(cy + 80), 8):
        ops += [rayita(-8, y_b, 8, y_b, 3.2)] # Rayas doradas
    # Punta curvada hacia afuera típica de las divinidades
    ops += [trazo((0, cy + 85), (6, cy + 92), (12, cy + 90), w=4.0)]

    # 8. Collar usekh en la base de la máscara
    P_collar = trap(-55, 55, cy + 65, -60, 60, cy + 115)
    ops += forma(P_collar, ORO, 5.0, sp=7)
    # Hileras de cuentas incrustadas de cornalina, turquesa y lapislázuli
    for yc, col_c in ((cy + 75, TURQUESA), (cy + 87, ROJO_EGIPTO), (cy + 99, AZUL_EGIPTO)):
        ops += [T(arco_(0, yc, 52, 10, 170, 14), 3.8)]
        ops += [R(arco_(0, yc, 50, 15, 165, 12), col_c, peso=0.04, sp=4)]
    return Dib(ops)


# ------------------------------------------------------------------ 7. Fachada colosal de Abu Simbel (Ramsés II)
@lru_cache(maxsize=None)
def abu_simbel_fachada():
    """El gran templo rupestre de Abu Simbel excavado en la roca viva:
    cuatro colosos sedentes de Ramsés II con la doble corona contemplando el Nilo."""
    ops = []
    # Acantilado de arenisca nubia que enmarca el templo
    P_risco = trap(-165, 165, -170, -170, 170, 0)
    ops += forma(P_risco, (215, 180, 135), 5.5, sp=8)

    # Friso de babuinos sagrados saludando al sol en la cornisa superior
    ops += forma(rect(-145, -175, 145, -165, 2), ARENA_OSC, 4.0, sp=5)
    for bx in np.linspace(-130, 130, 12):
        ops += [punto(bx, -170, w=6.0)]

    # Hornacina central con el dios Ra-Horakhty con cabeza de halcón
    ops += forma(rect(-18, -135, 18, -95, 3), (160, 120, 85), 4.2, sp=5) # Niche
    ops += forma(circ(0, -120, 8, n=12), ORO, 3.8, sp=4)                  # Disco solar del dios
    ops += [trazo((0, -112), (0, -100), w=3.4)]

    # Puerta de entrada oscura en la base
    ops += forma(rect(-16, -55, 16, 0, 2), (40, 32, 35), 4.5, sp=6)

    # CUATRO COLOSOS SEDENTES DE RAMSÉS II
    # Posiciones X de los 4 reyes colosales: dos a la izquierda, dos a la derecha de la puerta
    pos_x = [-115, -60, 60, 115]

    for i, rx in enumerate(pos_x):
        # Trono de piedra masivo
        P_trono = trap(rx - 22, rx + 22, -90, rx - 26, rx + 26, 0)
        ops += forma(P_trono, (200, 165, 120), 4.5, sp=6)

        # Piernas y rodillas monumentales
        ops += forma(rect(rx - 16, -65, rx - 3, 0, 4), (220, 185, 140), 4.2, sp=5)
        ops += forma(rect(rx + 3, -65, rx + 16, 0, 4), (220, 185, 140), 4.2, sp=5)
        # Manos gigantescas apoyadas serenamente sobre los muslos
        ops += [R(circ(rx - 9, -58, 6, n=8), ORO_OSC, peso=0.02, sp=3)]
        ops += [R(circ(rx + 9, -58, 6, n=8), ORO_OSC, peso=0.02, sp=3)]

        # Torso atlético desnudo con el collar ceremonial
        P_torso = trap(rx - 20, rx + 20, -120, rx - 16, rx + 16, -65)
        ops += forma(P_torso, (225, 190, 145), 4.5, sp=6)

        # Cabeza colosal con el rostro sereno y eterno de Ramsés
        cy_rey = -135.0
        # El segundo coloso (i=1) tiene la cabeza caída por un terremoto antiguo en época dinástica
        if i == 1:
            # Torso decapitado
            ops += forma(trap(rx - 14, rx + 14, -125, rx - 16, rx + 16, -118), (190, 155, 110), 4.0, sp=4)
            # Cabeza caída en el suelo a los pies del trono
            ops += forma(elip(rx + 15, -15, 14, 12, math.radians(20), 1.0, 14), (210, 175, 130), 4.0, sp=4)
        else:
            ops += forma(elip(rx, cy_rey, 14, 16, 0, 1.0, 18), (230, 195, 150), 4.8, sp=6)
            # Tocado Nemes que cae sobre los hombros
            P_nem = [(rx - 18, cy_rey - 10), (rx - 22, cy_rey + 20), (rx + 22, cy_rey + 20), (rx + 18, cy_rey - 10)]
            ops += forma(P_nem, (200, 165, 120), 4.0, sp=5)
            # Doble corona Pschent colosal sobre la cabeza
            P_cor = [(rx - 12, cy_rey - 14), (rx - 10, cy_rey - 45), (rx + 10, cy_rey - 45), (rx + 12, cy_rey - 14)]
            ops += forma(P_cor, CALIZA, 4.2, sp=5)
            # Barba postiza real
            ops += forma(rect(rx - 3, cy_rey + 14, rx + 3, cy_rey + 32, 1), (180, 145, 100), 3.5, sp=3)
    return Dib(ops)


# ------------------------------------------------------------------ 8. Tratado de paz de Kadesh
@lru_cache(maxsize=None)
def tratado_paz_kadesh():
    """Tablilla de arcilla y plata del Tratado de Kadesh (1274 a. C.):
    el primer tratado de paz documentado entre el faraón Ramsés II y el rey hitita Hattusili III."""
    ops = []
    # Tablilla rectangular de arcilla cocida con esquinas desgastadas
    P_tablilla = rect(-75, -155, 75, 0, r=10)
    ops += forma(P_tablilla, (212, 168, 122), 5.2, sp=8)

    # Sello real circular en la parte superior (el sello de plata del tratado)
    ops += forma(circ(0, -125, 20, n=20), (220, 224, 230), 4.5, sp=6) # Plata pulida
    # Grabado interior del sello: Ramsés y el dios de la tormenta Teshub abrazados
    ops += [T(circ(0, -125, 15, n=16), 3.2)]
    ops += [R(circ(0, -125, 14, n=14), ORO, peso=0.03, sp=3)]
    ops += [trazo((-6, -125), (6, -125), w=2.8), punto(0, -125, w=5.0)]

    # Líneas horizontales divisorias del texto cuneiforme y jeroglífico
    for yh in range(-95, -10, 12):
        ops += [rayita(-65, yh, 65, yh, 3.2)]
        # Símbolos cuneiformes en cuña
        for x_c in range(-55, 60, 16):
            ops += [trazo((x_c, yh - 6), (x_c + 4, yh - 2), (x_c + 8, yh - 6), w=2.4)]
            ops += [rayita(x_c + 4, yh - 8, x_c + 4, yh - 2, 2.4)]
    return Dib(ops)
