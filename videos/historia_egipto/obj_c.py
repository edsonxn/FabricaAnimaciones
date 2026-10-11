# -*- coding: utf-8 -*-
"""Objetos del Periodo Helenístico, Islámico y Moderno de Egipto (boceto).
Dibuja monumentos y piezas históricas: el Faro y la Biblioteca de Alejandría, Cleopatra VII,
galera naval de Accio, Ciudadela de Saladino, jinete mameluco, la Piedra de Rosetta,
el Canal de Suez con barco de vapor y la Presa de Asuán.

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


# ------------------------------------------------------------------ 1. Faro de Alejandría
@lru_cache(maxsize=None)
def faro_alejandria():
    """El Faro de Alejandría (isla de Faros), una de las Siete Maravillas del Mundo Antiguo:
    tres cuerpos superpuestos (cuadrado, octagonal y cilíndrico) con la hoguera perpetua y estatua de Poseidón."""
    ops = []
    # Escollera de piedra marina en la base
    ops += forma(rect(-80, -12, 80, 0, 3), (170, 165, 160), 4.8, sp=6)

    # CUERPO 1: Torre inferior cuadrangular con muros en talud
    P_base_izq = trap(-62, 0, -115, -68, 0, -12)
    P_base_der = trap(0, 62, -115, 0, 68, -12)
    ops += forma(P_base_izq, (215, 210, 202), 5.0, sp=7) # Cara en sombra
    ops += forma(P_base_der, CALIZA, 5.0, sp=7)          # Cara en luz de mármol blanco
    ops += [trazo((0, -115), (0, -12), w=4.5)]           # Arista vertical
    # Ventanas saeteras verticales
    for yv in (-35, -65, -95):
        ops += [rayita(-30, yv - 6, -30, yv + 6, 3.2), rayita(30, yv - 6, 30, yv + 6, 3.2)]
    # Cornisa superior con almenas y estatuas de tritones
    ops += forma(rect(-65, -122, 65, -115, 2), CALIZA, 4.5, sp=6)

    # CUERPO 2: Torre media octagonal
    P_oct_izq = trap(-34, 0, -185, -38, 0, -122)
    P_oct_der = trap(0, 34, -185, 0, 38, -122)
    ops += forma(P_oct_izq, (205, 200, 192), 4.8, sp=6)
    ops += forma(P_oct_der, CALIZA, 4.8, sp=6)
    ops += [trazo((0, -185), (0, -122), w=4.0)]
    ops += forma(rect(-36, -192, 36, -185, 2), CALIZA, 4.2, sp=5) # Cornisa

    # CUERPO 3: Linterna cilíndrica con columnas
    ops += forma(rect(-20, -225, 20, -192, 2), (220, 215, 205), 4.2, sp=5)
    # Columnas de la linterna
    for xc in (-16, -6, 6, 16):
        ops += [rayita(xc, -225, xc, -192, 3.0)]

    # HOGUERA PERPETUA Y ESPEJO DE BRONCE
    # Fuego resplandeciente en la linterna
    P_fuego = [(-14, -225), (-6, -242), (0, -236), (6, -248), (14, -225)]
    ops += forma(P_fuego, (245, 140, 40), 4.0, sp=5)
    ops += forma([(-8, -225), (0, -238), (8, -225)], ORO, 3.5, sp=4) # Núcleo ardiente
    # Humo que sube
    ops += [T(ondas(-10, 15, -252, 4, 12), 3.0, peso=0.04)]

    # Cúpula y estatua colosal de Poseidón en la cúspide
    ops += forma(elip(0, -228, 22, 6, 0, 1.0, 14), BRONCE, 4.0, sp=4)
    # Estatua con tridente
    ops += [trazo((0, -228), (0, -260), w=3.6)]
    ops += [trazo((5, -265), (5, -245), w=2.8)] # Tridente

    # Haz de luz que cruza el mar Mediterráneo
    P_haz = [(14, -230), (160, -265), (160, -215), (14, -225)]
    ops += [R(P_haz, (255, 245, 160), peso=0.03, sp=8)]
    return Dib(ops)


# ------------------------------------------------------------------ 2. Biblioteca de Alejandría
@lru_cache(maxsize=None)
def biblioteca_alejandria():
    """La Gran Biblioteca de Alejandría: columnata griega jónica con frontón clásico,
    estanterías llenas de rollos de papiro y sabios debatiendo."""
    ops = []
    # Estilóbato de tres peldaños de mármol blanco
    ops += forma(rect(-145, -8, 145, 0, 2), CALIZA, 4.5, sp=6)
    ops += forma(rect(-135, -16, 135, -8, 2), (230, 225, 215), 4.2, sp=5)
    ops += forma(rect(-125, -24, 125, -16, 2), CALIZA, 4.2, sp=5)

    # Sala interior sombría con estanterías (armaria) de rollos de papiro
    ops += forma(rect(-110, -125, 110, -24, 2), (75, 55, 45), 4.5, sp=6) # Interior madera
    # Estantes repletos de rollos de papiro con etiquetas
    for y_est in (-45, -70, -95, -115):
        ops += [rayita(-100, y_est, 100, y_est, 3.2)]
        for xr in range(-90, 95, 16):
            ops += forma(rect(xr - 5, y_est - 16, xr + 5, y_est, 1), ARENA, 2.5, sp=3)

    # Columnata monumental de mármol blanco (6 columnas jónicas)
    col_x = [-105, -63, -21, 21, 63, 105]
    for cx in col_x:
        # Fuste estriado
        ops += forma(rect(cx - 7, -135, cx + 7, -24, 2), CALIZA, 4.5, sp=6)
        ops += [rayita(cx - 3, -132, cx - 3, -26, 2.4), rayita(cx + 3, -132, cx + 3, -26, 2.4)]
        # Capitel con volutas
        ops += forma(rect(cx - 12, -145, cx + 12, -135, 2), (220, 215, 205), 4.0, sp=4)
        ops += [T(circ(cx - 9, -140, 4, n=8), 2.8), T(circ(cx + 9, -140, 4, n=8), 2.8)]

    # Arquitrabe y entablamento
    ops += forma(rect(-125, -160, 125, -145, 2), CALIZA, 4.8, sp=6)

    # Frontón triangular clásico con relieve alegórico de las Musas
    P_fronton = pol((-125, -160), (0, -205), (125, -160))
    ops += forma(P_fronton, CALIZA, 5.0, sp=7)
    # Tímpano interior con relieve en dorado
    P_timpano = pol((-105, -164), (0, -198), (105, -164))
    ops += forma(P_timpano, (215, 205, 190), 4.0, sp=5)
    ops += [R(circ(0, -178, 9, n=12), ORO, peso=0.03, sp=3)] # Sol del saber
    return Dib(ops)


# ------------------------------------------------------------------ 3. Cleopatra VII en su trono
@lru_cache(maxsize=None)
def cleopatra_trono():
    """Cleopatra VII Filopátor en su trono dorado: diadema real ptolemaica,
    túnica de lino plisado, brazalete de serpiente y mirada inteligente."""
    ops = []
    # 1. Trono helenístico-egipcio de madera dorada con patas de león
    P_respaldo = rect(-35, -155, 35, -50, r=6)
    ops += forma(P_respaldo, ORO, 4.8, sp=7)
    ops += forma(rect(-28, -145, 28, -60, 4), (195, 45, 45), 4.0, sp=5) # Cojín de terciopelo rojo
    # Asiento y brazos con esfinges
    ops += forma(rect(-45, -60, 45, -45, 3), ORO, 4.8, sp=6)
    # Patas de león del trono
    for px in (-35, 35):
        ops += forma(trap(px - 5, px + 5, -45, px - 8, px + 8, 0), ORO, 4.2, sp=5)

    # 2. Vestido de lino diáfano y túnica azul marino / púrpura real
    P_falda = trap(-30, 30, -50, -38, 38, -5)
    ops += forma(P_falda, BLANCO_LINO, 4.8, sp=7)
    # Pliegues finos de la tela griega (himation)
    for xf in (-20, -10, 0, 10, 20):
        ops += [rayita(xf, -48, xf * 1.2, -6, 2.5)]

    # 3. Torso y brazos elegantes
    P_torso = trap(-20, 20, -110, -16, 16, -50)
    ops += forma(P_torso, PIEL_CL, 4.6, sp=6)
    # Collar dorado griego con piedras turquesas
    ops += [T(arco_(0, -110, 18, 0, 180, 12), 4.0)]
    ops += [R(arco_(0, -110, 16, 10, 170, 10), TURQUESA, peso=0.03, sp=3)]

    # Brazos apoyados en los reposabrazos del trono
    # Brazo derecho con el áspid / serpiente de oro enroscado
    ops += forma(pol((-20, -105), (-38, -75), (-30, -55), (-22, -60), (-14, -100)), PIEL_CL, 4.0, sp=5)
    ops += forma(pol((20, -105), (38, -75), (30, -55), (22, -60), (14, -100)), PIEL_CL, 4.0, sp=5)
    # Brazalete de serpiente en el antebrazo
    ops += [T(arco_(-30, -68, 6, -90, 180, 8), 3.8)]
    ops += [R(circ(-30, -68, 6, n=8), ORO, peso=0.03, sp=3)]

    # 4. Rostro noble y cabello rizado helenístico con diadema real
    cy = -135.0
    ops += forma(rect(-6, -118, 6, -108, 2), PIEL_CL, 4.0, sp=4) # Cuello
    ops += forma(elip(0, cy, 18, 22, 0, 1.0, 20), PIEL_CL, 4.8, sp=6)

    # Cabello recogido en moño melón (estilo ptolemaico)
    P_pelo = [(-22, cy + 4), (-22, cy - 16), (0, cy - 25), (22, cy - 16), (22, cy + 4), (16, cy + 12), (-16, cy + 12)]
    ops += forma(P_pelo, (55, 38, 30), 4.5, sp=6) # Cabello castaño oscuro

    # Diadema de oro real con triple Uraeus
    ops += forma(rect(-20, cy - 14, 20, cy - 8, 2), ORO, 4.2, sp=4)
    ops += [trazo((0, cy - 14), (0, cy - 24), (3, cy - 28), w=3.0)] # Cobra frontal

    # Ojos penetrantes e inteligentes
    ops += [trazo((-10, cy - 2), (0, cy - 2), (3, cy), w=3.2)]
    ops += [trazo((2, cy - 2), (12, cy - 2), (15, cy), w=3.2)]
    ops += [punto(-5, cy - 2, w=5.0), punto(7, cy - 2, w=5.0)]
    # Nariz aguileña característica de las monedas de Cleopatra
    ops += [trazo((0, cy - 4), (4, cy + 5), (0, cy + 6), w=3.0)]
    ops += [trazo((-4, cy + 11), (4, cy + 11), w=3.0)]
    return Dib(ops)


# ------------------------------------------------------------------ 4. Galera de guerra romana (Accio)
@lru_cache(maxsize=None)
def galera_romana():
    """Birreme / trirreme de guerra romano: espolón de proa (rostrum),
    dos filas de remos, escudos scuta rojos en la borda y estandarte legionario."""
    ops = []
    # Casco de guerra robusto de roble
    curva_quilla = curva([(-135, -25), (-80, -10), (0, -5), (80, -8), (145, -30)], 10)
    curva_borda = curva([(145, -30), (80, -22), (0, -20), (-80, -22), (-135, -25)], 10)
    casco = np.vstack([curva_quilla, curva_borda])
    ops += forma(casco, (140, 85, 55), 5.2, sp=8)

    # Espolón de bronce naval (rostrum) en la proa para embestir
    P_espolon = pol((-135, -25), (-165, -15), (-135, -8))
    ops += forma(P_espolon, BRONCE, 4.8, sp=6)

    # Popa en voluta decorativa (aplustre)
    ops += [trazo((140, -28), (160, -55), (150, -68), (142, -62), w=4.5)]

    # Torreta de madera para arqueros y legionarios
    ops += forma(rect(-40, -55, -10, -22, 2), MADERA_OSC, 4.2, sp=5)
    # Estandarte imperial con águila romana
    ops += [trazo((-25, -55), (-25, -105), w=4.0)]
    ops += forma(rect(-25, -100, 5, -82, 1), ROJO_EGIPTO, 3.8, sp=4)
    ops += [T(linea((-25, -100), (5, -82)), 2.8)]
    ops += [punto(-10, -91, w=6.0)] # Emblema SPQR / Águila

    # Escudos romanos (scuta) rojos y dorados alineados a lo largo de la borda
    for xs in range(-90, 110, 22):
        ops += forma(rect(xs - 8, -32, xs + 8, -16, 3), ROJO_EGIPTO, 3.5, sp=4)
        ops += [R(circ(xs, -24, 3, n=8), ORO, peso=0.02, sp=2)] # Umbo dorado

    # Dos bancos de remos batiendo el agua simultáneamente
    for xr in range(-105, 120, 24):
        # Fila superior de remos
        ops += [trazo((xr, -20), (xr - 22, 18), w=3.4)]
        # Fila inferior de remos
        ops += [trazo((xr + 10, -12), (xr - 12, 24), w=3.0)]

    # Espuma blanca de las olas del mar
    ops += [T(ondas(-150, 150, 15, 6, 26), 4.2, peso=0.08)]
    return Dib(ops)


# ------------------------------------------------------------------ 5. Ciudadela de Saladino (El Cairo)
@lru_cache(maxsize=None)
def ciudadela_saladino():
    """La inexpugnable Ciudadela de Saladino en las colinas de Mokattam:
    murallas almenadas con torres redondas, y mezquita con cúpulas y minaretes esbeltos."""
    ops = []
    # Risco rocoso de colina
    P_risco = trap(-155, 155, -35, -165, 165, 0)
    ops += forma(P_risco, ARENA_OSC, 5.0, sp=7)

    # Muralla medieval masiva de piedra dorada
    P_muro = rect(-140, -95, 140, -35, r=4)
    ops += forma(P_muro, (220, 192, 148), 5.2, sp=8)
    # Almenas de la muralla
    for xa in range(-135, 140, 18):
        ops += forma(rect(xa - 6, -105, xa + 6, -95, 1), (220, 192, 148), 3.5, sp=4)

    # Dos grandes torres cilíndricas de vigilancia
    for xt in (-105, 105):
        P_torre = trap(xt - 26, xt + 26, -125, xt - 28, xt + 28, -35)
        ops += forma(P_torre, (210, 180, 138), 5.0, sp=7)
        # Almenas de la torre
        for xat in (-18, 0, 18):
            ops += forma(rect(xt + xat - 5, -135, xt + xat + 5, -125, 1), (210, 180, 138), 3.2, sp=3)
        # Aspilleras
        ops += [rayita(xt, -85, xt, -65, 3.2)]

    # Gran cúpula central otomana / mameluca de cobre verde
    ops += forma(elip(0, -115, 36, 32, 0, 1.0, 26), (110, 160, 135), 5.0, sp=7)
    ops += [trazo((0, -147), (0, -162), w=3.8)] # Aguja de la cúpula con media luna
    ops += forma(circ(0, -162, 5, n=10), ORO, 3.2, sp=3)

    # Minaretes esbeltos que se elevan hacia el cielo
    for xm in (-45, 45):
        ops += forma(trap(xm - 7, xm + 7, -185, xm - 9, xm + 9, -95), CALIZA, 4.2, sp=6)
        # Balcones del almuédano
        ops += forma(rect(xm - 11, -145, xm + 11, -138, 1), (180, 150, 110), 3.4, sp=3)
        ops += forma(rect(xm - 10, -188, xm + 10, -182, 1), (180, 150, 110), 3.4, sp=3)
        # Cúspide cónica del minarete con media luna
        P_cono = pol((xm - 7, -188), (xm, -215), (xm + 7, -188))
        ops += forma(P_cono, (110, 160, 135), 3.8, sp=4)
        ops += forma(circ(xm, -218, 4, n=8), ORO, 2.8, sp=2)
    return Dib(ops)


# ------------------------------------------------------------------ 6. Piedra de Rosetta y descifrado
@lru_cache(maxsize=None)
def piedra_rosetta():
    """La Piedra de Rosetta (1798 / 1822): estela de granodiorita oscura con tres escrituras
    (jeroglífico, demótico y griego clásico) y la lupa de Champollion descifrando un cartucho."""
    ops = []
    # Losa de piedra granodiorita negra con la esquina superior rota
    P_piedra = [(-70, -155), (-60, -170), (45, -165), (70, -140), (70, 0), (-70, 0)]
    ops += forma(P_piedra, (58, 56, 62), 5.5, sp=8) # Granodiorita oscura

    # REGISTRO 1: Jeroglíficos egipcios (arriba, 14 líneas fragmentadas)
    for y1 in range(-145, -105, 10):
        ops += [rayita(-55, y1, 55, y1, 2.2)]
        for xj in range(-45, 50, 15):
            ops += [punto(xj, y1 - 3, w=4.5)]

    # REGISTRO 2: Escritura demótica cotidiana (centro, 32 líneas)
    for y2 in range(-100, -55, 8):
        ops += [rayita(-62, y2, 62, y2, 2.0)]

    # REGISTRO 3: Griego clásico (abajo, 54 líneas)
    for y3 in range(-50, -10, 8):
        ops += [rayita(-62, y3, 62, y3, 2.0)]

    # Lupa de Champollion enfocando el cartucho de 'Ptolomeo'
    cx_lupa, cy_lupa = 25.0, -125.0
    r_lupa = 26.0
    # Mango de latón de la lupa
    ops += [trazo((cx_lupa + 18, cy_lupa + 18), (cx_lupa + 55, cy_lupa + 55), w=6.5)]
    # Marco circular dorado y lente de aumento clara
    ops += forma(circ(cx_lupa, cy_lupa, r_lupa, n=24), (220, 235, 245), 4.8, sp=6)
    ops += [T(circ(cx_lupa, cy_lupa, r_lupa, n=24), 5.0, peso=0.08)]
    ops += [R(circ(cx_lupa, cy_lupa, r_lupa, n=24), ORO, peso=0.04, sp=4)]

    # Cartucho magnificado dentro de la lupa con los signos P-T-O-L-M-Y-S
    ops += forma(rect(cx_lupa - 18, cy_lupa - 12, cx_lupa + 18, cy_lupa + 12, r=10), ORO, 3.2, sp=4)
    ops += [punto(cx_lupa - 8, cy_lupa, w=5.0), punto(cx_lupa, cy_lupa, w=5.0), punto(cx_lupa + 8, cy_lupa, w=5.0)]
    return Dib(ops)


# ------------------------------------------------------------------ 7. Canal de Suez y barco de vapor (1869)
@lru_cache(maxsize=None)
def barco_vapor_suez():
    """El Canal de Suez recién inaugurado: canal recto entre dunas arenosas
    y un barco de vapor del siglo XIX con chimenea humeante y rueda de paletas."""
    ops = []
    # Riberas arenosas del canal a ambos lados
    P_duna_izq = trap(-150, -75, -60, -150, -95, 0)
    P_duna_der = trap(75, 150, -60, 95, 150, 0)
    ops += forma(P_duna_izq, ARENA, 4.8, sp=7)
    ops += forma(P_duna_der, ARENA, 4.8, sp=7)

    # Agua azul del canal uniendo el Mediterráneo y el Mar Rojo
    P_canal = trap(-85, 85, -55, -100, 100, 0)
    ops += forma(P_canal, CELESTE_NILO, 4.8, sp=7)

    # BARCO DE VAPOR DEL SIGLO XIX
    # Casco de hierro negro
    curva_casco = [(-65, -35), (-55, -18), (55, -18), (65, -35)]
    P_casco = np.vstack([curva_casco, [(55, -35)], [(-65, -35)]])
    ops += forma(curva_casco, (45, 45, 52), 5.0, sp=7)
    # Franja blanca en la borda
    ops += [rayita(-60, -32, 60, -32, 3.0)]

    # Cubierta y camarotes de madera
    ops += forma(rect(-40, -48, 40, -35, 2), CALIZA, 4.2, sp=5)

    # Chimenea central alta inclinada
    P_chimenea = trap(-6, 6, -85, -8, 8, -48)
    ops += forma(P_chimenea, (215, 60, 45), 4.2, sp=5)     # Chimenea roja
    ops += forma(rect(-6, -85, 6, -75, 1), NEGRO_KOHL, 4.0, sp=4) # Banda negra superior
    # Penacho de humo blanco y gris
    for yh, rad, r_h in ((-95, 0, 8), (-108, 6, 12), (-122, 16, 16)):
        ops += forma(circ(rad, yh, r_h, n=14), (220, 222, 228), 3.2, sp=4)

    # Rueda de paletas central (paddlewheel)
    ops += forma(circ(0, -26, 15, n=16), (80, 80, 90), 4.0, sp=5)
    ops += [R(circ(0, -26, 8, n=10), ORO_OSC, peso=0.03, sp=3)]
    for ap in range(0, 360, 45):
        rad_p = math.radians(ap)
        ops += [rayita(0, -26, 14 * math.cos(rad_p), -26 + 14 * math.sin(rad_p), 2.8)]

    # Mástiles de proa y popa con jarcias
    ops += [trazo((-35, -48), (-35, -95), w=3.4), trazo((35, -48), (35, -95), w=3.4)]
    ops += [trazo((-35, -85), (-60, -35), w=2.4), trazo((35, -85), (60, -35), w=2.4)]
    return Dib(ops)


# ------------------------------------------------------------------ 8. Presa de Asuán (siglo XX)
@lru_cache(maxsize=None)
def presa_asuan():
    """La Gran Presa de Asuán (Sadd el-Aali): dique colosal de granito y hormigón,
    aliviaderos con cascadas de agua blanca y el Lago Nasser al fondo."""
    ops = []
    # Lago Nasser azul profundo al fondo
    P_lago = trap(-155, 155, -115, -160, 160, -75)
    ops += forma(P_lago, (55, 110, 175), 4.8, sp=7)

    # Corona superior del dique (carretera y vía de servicio)
    ops += forma(rect(-160, -85, 160, -75, 2), CALIZA, 4.5, sp=6)
    ops += [rayita(-155, -80, 155, -80, 2.6)]

    # Cara curva de hormigón y escollera de granito de la presa
    P_presa = trap(-160, 160, -75, -170, 170, -20)
    ops += forma(P_presa, (185, 180, 175), 5.2, sp=8)

    # 4 Compuertas y aliviaderos rugientes con cascadas de agua blanca
    for xg in (-90, -30, 30, 90):
        # Boca de la compuerta
        ops += forma(rect(xg - 14, -65, xg + 14, -40, 2), (40, 42, 48), 4.0, sp=5)
        # Chorro potente de agua espumosa que se precipita al Nilo
        P_cascada = trap(xg - 12, xg + 12, -40, xg - 18, xg + 18, 0)
        ops += forma(P_cascada, (240, 248, 255), 4.2, sp=6)
        # Espuma turbulenta en la base
        for xs in (-15, 0, 15):
            ops += [R(circ(xg + xs, 2, 7, n=10), BLANCO, peso=0.04, sp=3)]

    # Torres de alta tensión eléctrica a los lados
    for xt in (-140, 140):
        ops += [trazo((xt, -85), (xt, -145), w=3.8)]
        ops += [trazo((xt - 12, -130), (xt + 12, -130), w=3.0)]
        ops += [trazo((xt - 10, -115), (xt + 10, -115), w=3.0)]
        ops += [trazo((xt - 12, -85), (xt, -145), (xt + 12, -85), w=2.6)] # Celosía
    return Dib(ops)
