# -*- coding: utf-8 -*-
"""Capa de EFECTOS: análisis táctico del Barón de Team Liquid (Worlds 2026, TLAW vs AL partida 2).
UN solo clip (medios/_fuente/jugada.mp4, reloj de juego = segundo del clip + 39:40) que el FX `video` controla:
vel=1 juega, vel=0 congela (pausa del telestrador), vel<0 rebobina, vel<1 cámara lenta. Encima, nucleo/mg_tactica.py:
`pizarra` (anillos, flechas, foco sobre el cuadro congelado) y `tablero` (mapa táctico 3D con fichas que se mueven).
Tiempos ABSOLUTOS (segundos del video, de timeline.json). Posiciones de la pizarra: fracción del cuadro, medidas en
previews/cuadros/g*.jpg (rejilla). Posiciones del tablero: fracción del mapa (azul abajo-izquierda), sacadas del
minimapa de la transmisión (previews/minimapas.png).
"""
import os

import mg_tactica as T

_D = os.path.dirname(os.path.abspath(__file__))
FUENTE = os.path.join(_D, "medios", "_fuente", "jugada.mp4")
MAPA = os.path.join(_D, "mapas", "grieta.png")
ICO = os.path.join(_D, "iconos")


def J(de, a, desde, vel=1.0):
    """El clip de la jugada a cuadro entero: desde el segundo `desde` del clip, a velocidad `vel` (0 = congelado)."""
    return dict(tipo="video", de=de, a=a, ruta=FUENTE, desde=desde, vel=vel, nombre=f"clip {desde:.1f} x{vel:g}")


def pizarra(de, a, els, reloj, pausa="PAUSA"):
    return dict(tipo="mg", fn=T.pizarra(de, els, pausa, reloj), de=de, a=a, nombre=f"pizarra {reloj}", ver=1.0)


def chip(de, a, texto, color="amarillo", sub=None, x=.5, y=.2, icono=None, tam=40):
    return dict(tipo="mg", fn=T.chip(texto, color, tam, sub, icono and os.path.join(ICO, icono + ".png")), de=de, a=a, x=x,
                y=y, sale=.25, nombre="chip " + texto, ver=1.0)


def tablero(de, a, els, camara, reloj, hud=None, titulo="MAPA TÁCTICO"):
    return dict(tipo="pantalla", fn=T.tablero(de, MAPA, els, camara, titulo, reloj, hud, ICO), de=de, a=a, entra=.4, sale=.35,
                nombre="tablero " + titulo, ver=2.0)


def ficha(campeon, equipo, ruta, en, nombre=None, sale=None):
    return dict(tipo="ficha", campeon=campeon, equipo=equipo, ruta=ruta, en=en, nombre=nombre, sale=sale)


A, R = "azul", "rojo"

# ------------------------------------------------------------------ tablero 1: contexto (minuto 40:16)
M1 = [ficha("Pantheon", A, [(0, .60, .71)], 18.0), ficha("Xayah", A, [(0, .575, .65)], 18.1),
      ficha("Rakan", A, [(0, .565, .74)], 18.2), ficha("Akali", A, [(0, .62, .62)], 18.3),
      ficha("Kled", A, [(0, .48, .55)], 18.4),
      ficha("Nocturne", R, [(0, .735, .655)], 18.5), ficha("TahmKench", R, [(0, .76, .60)], 18.6),
      ficha("Jinx", R, [(0, .79, .665)], 18.7), ficha("Annie", R, [(0, .755, .72)], 18.8),
      ficha("Olaf", R, [(0, .72, .77)], 18.9),
      dict(tipo="anillo", u=.655, v=.695, r=.045, color="amarillo", en=28.0, etiqueta="DRAGÓN 3", sub="INFERNAL", lado="abajo")]
HUD1 = [(21.3, "11 - 17 EN ASESINATOS", R, "LIQUID VA ABAJO"), (23.7, "+3 000 DE ORO", A, "VENTAJA DE LIQUID"),
        (25.6, "6 - 2 EN TORRES", A, "LIQUID PRESIONA"), (30.5, "¡ALMA EN JUEGO!", R, "SI AL LO TOMA, SE LLEVA EL ALMA")]

# ------------------------------------------------------------------ tablero 2: el tempo (40:20 - 41:05)
# TL: después del dragón suben por el río al medio, presionan el lado de arriba, se retiran del flanco y rodean el Barón
_tl = dict(Pantheon=((.56, .68), (.50, .47), (.57, .32), (.45, .25), (.44, .22)),
           Xayah=((.53, .64), (.47, .50), (.54, .35), (.43, .30), (.47, .31)),
           Rakan=((.55, .73), (.52, .51), (.59, .36), (.47, .28), (.45, .35)),
           Akali=((.59, .63), (.53, .44), (.60, .29), (.48, .24), (.48, .25)))
M2 = [ficha(c, A, [(50.2,) + p[0], (56.5,) + p[1], (69.0,) + p[2], (76.6,) + p[2], (80.2,) + p[3], (87.0,) + p[4]], 50.4)
      for c, p in _tl.items()]
M2.append(ficha("Kled", A, [(50.2, .46, .55), (68.05, .46, .55), (68.2, .71, .12), (76.6, .71, .12), (80.5, .52, .16),
                            (87.0, .40, .19)], 50.4, "Morgan"))
_al = dict(Nocturne=((.74, .66), (.84, .53), (.83, .40), (.69, .30)), TahmKench=((.77, .61), (.87, .50), (.86, .37), (.72, .25)),
           Jinx=((.79, .67), (.88, .56), (.88, .43), (.73, .33)))
for c, p in _al.items():
    M2.append(ficha(c, R, [(50.2,) + p[0], (60.0,) + p[1], (70.0,) + p[2], (82.0,) + p[3]], 50.6))
M2.append(ficha("Annie", R, [(50.2, .755, .72), (60.0, .85, .58), (73.4, .85, .49), (76.0, .81, .33), (78.0, .69, .25),
                             (82.0, .66, .27)], 50.6, "Annie"))
M2.append(ficha("Olaf", R, [(50.2, .72, .77), (60.0, .82, .60), (73.4, .82, .52), (76.0, .78, .35), (78.0, .67, .29),
                            (82.0, .64, .31)], 50.6, "Olaf"))
M2 += [
    dict(tipo="anillo", u=.655, v=.695, r=.05, color="amarillo", en=52.6, sale=55.5, etiqueta="TODOS ABAJO", lado="abajo"),
    dict(tipo="oleada", ruta=[(.30, .085), (.50, .085), (.74, .092)], de=53.8, en=53.8, a=58.0, color=A, n=7, sale=66.5),
    dict(tipo="anillo", u=.755, v=.095, r=.035, color=R, en=57.6, sale=66.5, etiqueta="TORRE DEL INHIBIDOR", lado="der"),
    dict(tipo="flecha", pts=[(.86, .48), (.87, .32), (.79, .15)], color=R, en=60.9, sale=66.5, guion=True,
         etiqueta="¿DEFENDER LA BASE?", off=(190, 0)),
    dict(tipo="flecha", pts=[(.82, .56), (.68, .56), (.56, .51)], color=R, en=62.6, sale=66.5, guion=True,
         etiqueta="¿SEGUIR A LIQUID?", off=(0, 70)),
    dict(tipo="tp", desde=(.46, .55), a=(.71, .12), en=67.0, dur=1.1, color=A, sale=72.0),
    dict(tipo="flecha", pts=[(.86, .46), (.83, .32), (.70, .25)], color=R, en=72.6, sale=80.5, etiqueta="FLANCO",
         sub="ANNIE + OLAF", off=(150, 30)),
    dict(tipo="flecha", pts=[(.56, .32), (.51, .29), (.45, .26)], color=A, en=76.6, sale=81.0, etiqueta="SE RETIRA",
         off=(-40, 75)),
    dict(tipo="niebla", pts=[(0, 0), (1, 0), (0, 1)], en=84.0, k=.6),
    dict(tipo="ward", u=.25, v=.17, en=84.6, color=A), dict(tipo="ward", u=.38, v=.12, en=84.8, color=A),
    dict(tipo="ward", u=.40, v=.40, en=85.0, color=A), dict(tipo="ward", u=.20, v=.38, en=85.2, color=A),
    dict(tipo="ward", u=.55, v=.20, en=85.4, color=A),
    dict(tipo="anillo", u=.325, v=.295, r=.05, color="amarillo", en=86.8, etiqueta="BARÓN", lado="izq"),
]
CAM2 = [(50.2, .60, .60, 1.15), (53.6, .54, .40, 1.0), (57.8, .66, .20, 1.45), (60.2, .70, .40, 1.2), (66.8, .60, .32, 1.15),
        (72.0, .70, .34, 1.30), (77.0, .62, .30, 1.30), (80.8, .48, .34, 1.0), (88.0, .40, .27, 1.35)]
HUD2 = [(64.0, "NO PUEDE CON LAS DOS", R, None, 66.8), (68.6, "TP DE MORGAN", A, "KLED PRESIONA EL INHIBIDOR", 72.2),
        (81.4, "BARÓN EN 0:40", "amarillo", None), (84.2, "AL ESTÁ A CIEGAS", R, "LIQUID TIENE LA VISIÓN ARRIBA")]

# ------------------------------------------------------------------ tablero 3: la lección
M3 = [
    dict(tipo="num", u=.655, v=.695, n=1, color="amarillo", en=119.1, etiqueta="DRAGÓN"),
    dict(tipo="flecha", pts=[(.63, .64), (.55, .42), (.60, .14)], color=A, en=119.5, dur=.6),
    dict(tipo="oleada", ruta=[(.36, .085), (.60, .088)], de=119.7, en=119.7, a=121.5, color=A, n=6),
    dict(tipo="num", u=.64, v=.09, n=2, color="amarillo", en=120.1, etiqueta="OLEADA + TP"),
    dict(tipo="flecha", pts=[(.60, .13), (.47, .19), (.38, .26)], color=A, en=120.5, dur=.5),
    dict(tipo="num", u=.325, v=.295, n=3, color="amarillo", en=120.9, etiqueta="PACIENCIA = BARÓN"),
]
HUD3 = [(122.2, "¿QUÉ JUGADA ANALIZAMOS?", "amarillo", "DÉJALO EN LOS COMENTARIOS")]

FX = [
    # --- gancho: el castigo al Barón, pausa en el foso y rebobinado de 90 s
    J(0.0, 4.6, 123.3), J(4.6, 9.8, 127.9),
    chip(0.5, 8.6, "WORLDS 2026 · FASE SUIZA", "amarillo", "TEAM LIQUID vs ANYONE'S LEGEND · PARTIDA 2", x=.24, y=.2, tam=34),
    dict(tipo="destello", en=9.8, fuerza=.6),
    J(9.8, 14.5, 126.3, 0),
    pizarra(9.8, 14.5, [dict(tipo="foco", en=10.0, k=.45),
                        dict(tipo="anillo", x=.52, y=.42, r=190, color="amarillo", en=10.1, etiqueta="EL BARÓN", lado="izq"),
                        dict(tipo="texto", x=.5, y=.70, texto="NO SE GANÓ AQUÍ", color=R, en=10.6, tam=56),
                        dict(tipo="texto", x=.5, y=.80, texto="SE GANÓ 90 SEGUNDOS ANTES", color="amarillo", en=12.9, tam=46)],
            "41:46"),
    J(14.5, 16.4, 126.3, -48.6),
    dict(tipo="mg", fn=T.rebobinar("REBOBINANDO", "90 SEGUNDOS"), de=14.5, a=16.4, nombre="rebobinar"),
    J(16.4, 17.8, 34.0, 0.4),
    # --- contexto: tablero
    tablero(17.45, 34.95, M1, [(17.45, .52, .54, .92), (24.0, .56, .58, 1.0), (28.0, .63, .66, 1.32)], [(17.45, "40:16")], HUD1),
    # --- el dragón: llegada, pausa con telestrador y repetición en cámara lenta
    J(34.9, 36.7, 34.2), J(36.7, 43.3, 36.0, 0),
    pizarra(36.7, 43.3, [
        dict(tipo="foco", en=36.7, k=.42),
        dict(tipo="anillo", x=.27, y=.48, r=80, color=A, en=36.7, etiqueta="JOSEDEODO", sub="PANTHEON · CASTIGO LISTO", lado="izq"),
        dict(tipo="anillo", x=.33, y=.37, r=95, color="amarillo", en=37.9, etiqueta="DRAGÓN", sub="INFERNAL", lado="der"),
        dict(tipo="anillo", x=.345, y=.27, r=62, color=A, en=38.5, etiqueta="YEON", sub="XAYAH PEGA DESDE ATRÁS", lado="arriba"),
        dict(tipo="anillo", x=.485, y=.56, r=58, color=R, en=40.4), dict(tipo="anillo", x=.605, y=.44, r=58, color=R, en=40.5),
        dict(tipo="anillo", x=.64, y=.53, r=58, color=R, en=40.6),
        dict(tipo="flecha", pts=[(.60, .47), (.51, .46), (.43, .43)], color=R, en=40.8, guion=True, etiqueta="AL LLEGA TARDE",
             off=(30, 70)),
    ], "40:16"),
    J(43.3, 50.2, 36.0, .72),
    chip(43.3, 50.2, "REPETICIÓN", R, None, x=.12, y=.16, tam=36),
    chip(44.9, 50.2, "TRES DRAGONES PARA LIQUID", A, None, x=.5, y=.70, tam=40),
    chip(46.7, 50.2, "EL ALMA SE LE ESCAPA A AL", R, None, x=.5, y=.79, tam=40),
    # --- el tempo y la visión: tablero
    tablero(50.2, 89.6, M2, CAM2, [(50.2, "40:20"), (66.8, "40:35"), (72.2, "40:45"), (81.0, "41:05")], HUD2,
            "EL TEMPO"),
    # --- el Barón: pausa con Nocturne buscando el robo, castigo y cámara lenta
    J(89.45, 94.95, 115.5), J(94.95, 102.5, 121.0, 0),
    pizarra(94.95, 102.5, [
        dict(tipo="foco", en=94.95, k=.42),
        dict(tipo="anillo", x=.25, y=.36, r=125, color="amarillo", en=94.95, etiqueta="BARÓN · 11 166 PV", lado="arriba"),
        dict(tipo="anillo", x=.20, y=.45, r=46, color=A, en=95.2), dict(tipo="anillo", x=.285, y=.47, r=46, color=A, en=95.3),
        dict(tipo="anillo", x=.18, y=.55, r=46, color=A, en=95.4),
        dict(tipo="anillo", x=.46, y=.28, r=58, color=R, en=95.84, etiqueta="NOCTURNE", sub="TARZAN", lado="der"),
        dict(tipo="flecha", pts=[(.44, .25), (.40, .15), (.30, .14)], color=R, en=96.4, dur=.8, etiqueta="BUSCA EL ROBO",
             off=(0, -55)),
        dict(tipo="anillo", x=.56, y=.50, r=52, color=R, en=98.7), dict(tipo="anillo", x=.59, y=.73, r=52, color=R, en=98.8),
        dict(tipo="anillo", x=.73, y=.23, r=52, color=R, en=98.9),
        dict(tipo="flecha", pts=[(.55, .50), (.45, .46), (.37, .43)], color=R, en=99.4, guion=True),
        dict(tipo="flecha", pts=[(.58, .71), (.48, .62), (.38, .50)], color=R, en=99.5, guion=True),
        dict(tipo="flecha", pts=[(.71, .26), (.58, .34), (.42, .38)], color=R, en=99.6, guion=True),
        dict(tipo="texto", x=.68, y=.60, texto="VIENEN DE LEJOS", color=R, en=100.2, tam=44),
    ], "41:41"),
    dict(tipo="destello", en=102.5, fuerza=.5),
    J(102.5, 104.2, 124.6), J(104.2, 105.4, 126.3, 0),
    pizarra(104.2, 105.4, [dict(tipo="anillo", x=.39, y=.30, r=70, color=A, en=104.2, etiqueta="¡CASTIGO!",
                                sub="JOSEDEODO", lado="der", icono=os.path.join(ICO, "SummonerSmite.png"))], "41:46"),
    J(105.4, 106.95, 126.3, .4),
    chip(104.7, 106.95, "BARÓN PARA LIQUID", A, None, x=.5, y=.78, tam=48),
    # --- remate: AL sin definitivas, el costo, y la lección en el tablero
    J(106.9, 116.6, 128.0),
    chip(109.4, 112.4, "SIN DEFINITIVAS", R, "AL NO PUEDE FORZAR LA PELEA", x=.5, y=.2),
    chip(113.9, 116.6, "-2 DESTELLO", A, None, x=.41, y=.2, icono="SummonerFlash"),
    chip(115.1, 116.6, "-1 CURAR", A, None, x=.61, y=.2, icono="SummonerHeal"),
    tablero(116.4, 129.4, M3, [(116.4, .50, .50, .90), (129.4, .48, .45, .98)], [(116.4, "41:46")], HUD3, "LA LECCIÓN"),
    dict(tipo="cierra", en=128.4, dur=.9),
]

ROTULOS = []
SFX = {}          # todos de la biblioteca (sfx usar): rebobina, whoosh, whoosh2, golpe, clic, pop, pop2, subida, scratch
_pop = [21.3, 23.7, 25.6, 30.5, 44.9, 46.7, 57.6, 64.0, 68.6, 84.2, 86.8, 109.4, 113.9, 115.1, 119.1, 120.1, 120.9, 122.2]
_dib = [10.1, 37.9, 38.5, 40.4, 60.9, 62.6, 72.6, 76.6, 95.84, 96.4, 98.7]       # anillos y flechas que entran
PISTAS = ([dict(sfx="golpe", en=9.8, vol=.55), dict(sfx="clic", en=9.82, vol=.5),
           dict(sfx="rebobina", en=14.5, vol=.5), dict(sfx="rebobina", en=15.4, vol=.4),
           dict(sfx="whoosh", en=17.4, vol=.5), dict(sfx="clic", en=36.7, vol=.55), dict(sfx="golpe", en=36.72, vol=.3),
           dict(sfx="whoosh2", en=43.25, vol=.35), dict(sfx="whoosh", en=50.1, vol=.5), dict(sfx="whoosh2", en=67.0, vol=.45),
           dict(sfx="clic", en=94.95, vol=.55), dict(sfx="golpe", en=94.97, vol=.3), dict(sfx="subida", en=102.2, vol=.45),
           dict(sfx="golpe", en=104.2, vol=.7), dict(sfx="scratch", en=104.25, vol=.25), dict(sfx="whoosh", en=116.3, vol=.5)]
          + [dict(sfx="pop2", en=t, vol=.32) for t in _pop] + [dict(sfx="pop", en=t, vol=.3) for t in _dib])
