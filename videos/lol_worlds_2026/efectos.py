# -*- coding: utf-8 -*-
"""Capa de EFECTOS del resumen de la Worlds 2026 (estilo análisis táctico, docs/estilo_analisis_tactico.md).
Editado como Warcraft/Tamriel/Runa (el usuario, 27-oct-2026): pegatina real casi en cada frase, MG propios del guion que
entran por partes con la voz y tarjetas de transmisión (kit nucleo/mg_lol.py; plan por escena en PLAN_EFECTOS.md).
En cada jugada analizada, el FX `video` toma el cuadro entero con el tramo de la jugada (medios/_fuente/jN.mp4: vel=1 juega,
0 congela, <0 rebobina, <1 cámara lenta) y nucleo/mg_tactica.py dibuja el telestrador encima. El tramo EN VIVO previo de
cada jugada (beat largo sin voz) va casi sin FX: es el clip del beat con el audio de la transmisión (ambiente_por).
Tiempos ABSOLUTOS (timeline.json). Posiciones de la pizarra: fracción del cuadro, medidas en previews/cuadros/g*.jpg.
"""
import os

import sys

import mg_lol as L
import mg_tactica as T

_D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_D, "..", "..", "nucleo", "tactica3d"))
import sobre_video as SV  # noqa: E402
from capa import capa3d  # noqa: E402
ICO = os.path.join(_D, "iconos")
A, R, Y = "azul", "rojo", "amarillo"


def EQ(cod):
    return os.path.join(ICO, "equipos", cod + ".png")


def JUG(n):
    return os.path.join(_D, "pegatinas", "jugadores", n + ".png")


def ART(c):
    return os.path.join(_D, "splash", c + ".jpg")


def fuente(n):
    if n == 6:                      # el Barón de Liquid: el corte de la prueba (VOD wjoQ0ze5bJ4 desde 2833 s; reloj = s + 39:40)
        return os.path.join(_D, "..", "lol_worlds_tl_al", "medios", "_fuente", "jugada.mp4")
    return os.path.join(_D, "medios", "_fuente", f"j{n}.mp4")


def J(n, de, a, desde, vel=1.0, **kw):
    """El tramo de la jugada `n` a cuadro entero desde el segundo `desde`, a velocidad `vel` (0 = congelado).
    kw: zoom=(z, cx, cy), zoom0, zoom_en, zoom_dur (acercamiento animado del FX `video`, 27-oct-2026)."""
    return dict(tipo="video", de=de, a=a, ruta=fuente(n), desde=desde, vel=vel, nombre=f"j{n} {desde:.1f} x{vel:g}", **kw)


def pizarra(de, a, els, reloj, pausa="PAUSA"):
    return dict(tipo="mg", fn=T.pizarra(de, els, pausa, reloj), de=de, a=a, nombre=f"pizarra {reloj}", ver=1.0)


CAPAS = os.path.join(_D, "tactica3d", "capas")


def pizarra3d(nombre, de, a, els, reloj, fondo, pausa="PAUSA", extra=None):
    """La pausa con elementos 3D SOBRE EL VIDEO REAL (27-oct-2026): la pizarra 2D solo pone el chip «PAUSA · reloj» y los
    anillos/flechas/zonas medidos en el cuadro van como capa 3D (nucleo/tactica3d/sobre_video.py). fondo = (ruta, s) del
    cuadro congelado, para revisar. extra = dict de elementos 3D añadidos (pilares, proyectiles, etiquetas…)."""
    spec = SV.de_pizarra(de, a, els)
    for k, v in (extra or {}).items():
        spec.setdefault(k, []).extend(v)
    base = SV.registrar(CAPAS, nombre, spec, fondo)
    return [pizarra(de, a, [], reloj, pausa),
            dict(tipo="mg", fn=capa3d(base), de=de, a=a, nombre=f"3D {nombre}", ver=1.0)]


def rebobinar(de, a, sub=None, texto="REBOBINANDO"):
    return dict(tipo="mg", fn=T.rebobinar(texto, sub), de=de, a=a, nombre="rebobinar")


J3D = os.path.join(_D, "medios", "_fuente", "j6_3d.mp4")


def V3(de, a, mp4=J3D, t0=975.0):
    """tramo del clip 3D (render3d.py) que corresponde a [de, a) del video; el clip empieza en t0"""
    return dict(tipo="video", de=de, a=a, ruta=mp4, desde=de - t0, vel=1.0, nombre=f"3D {de:.1f}")

def MESA(k, de, a, reloj):
    """la pausa se vuelve 3D: medios/_fuente/mesa_<k>.mp4 (mesas_3d.py) + el chip «PAUSA · reloj» encima"""
    return [V3(de, a, os.path.join(_D, "medios", "_fuente", f"mesa_{k}.mp4"), de), pizarra(de, a, [], reloj)]

MAPA = os.path.join(_D, "mapas", "grieta.png")


def tablero(de, a, els, camara, reloj, hud=None, titulo="MAPA TÁCTICO"):
    return dict(tipo="pantalla", fn=T.tablero(de, MAPA, els, camara, titulo, reloj, hud, ICO), de=de, a=a, entra=.4, sale=.35,
                nombre="tablero " + titulo, ver=2.0)


def ficha(campeon, equipo, ruta, en, nombre=None, sale=None):
    return dict(tipo="ficha", campeon=campeon, equipo=equipo, ruta=ruta, en=en, nombre=nombre, sale=sale)


def anillo(x, y, r, color, en, etiqueta=None, sub=None, lado="arriba", icono=None, **kw):
    d = dict(tipo="anillo", x=x, y=y, r=r, color=color, en=en, lado=lado, **kw)
    if etiqueta:
        d.update(etiqueta=etiqueta, sub=sub)
    if icono:
        d["icono"] = os.path.join(ICO, icono + ".png")
    return d


def flecha(pts, color, en, etiqueta=None, off=(0, -50), guion=False, dur=.6, **kw):
    d = dict(tipo="flecha", pts=pts, color=color, en=en, dur=dur, guion=guion, off=off, **kw)
    if etiqueta:
        d["etiqueta"] = etiqueta
    return d


def en_vivo(de, sub, logo):
    return tar(de, de + 5.2, "En vivo", sub, R, logo=logo, x=.24, y=.17, tam=46)


def mg(fn, de, a, marcas=(), x=.5, y=.45, nombre="MG"):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.3, nombre=nombre, ver=2.0)


def tar(de, a, titulo, sub=None, color="oro", logo=None, icono=None, dato=None, x=.72, y=.74, tam=60):
    """Tarjeta de transmisión (tercio inferior); logo = código del equipo, icono = cuadro de campeón."""
    return mg(L.tarjeta(titulo, sub, color, logo=logo and EQ(logo), icono=icono and os.path.join(ICO, icono + ".png"), dato=dato,
                        tam=tam), de, a, x=x, y=y, nombre="tarjeta " + titulo)


def peg(en, img, nombre=None, color="oro", logo=None, sub=None, dur=4.0, x=.17, y=.52, tam=420, gris=False, sello=None,
        marcas=()):
    """Pegatina: img = jugador (pegatinas/jugadores) o ruta completa; con placa de su equipo debajo."""
    ruta = img if os.path.sep in img or "/" in img else JUG(img)
    return mg(L.pegatina(ruta, nombre, color, logo=logo and EQ(logo), sub=sub, tam=tam, gris=gris, sello=sello), en, en + dur,
              marcas, x=x, y=y, nombre="pegatina " + (nombre or os.path.basename(ruta)))


def gran(en, img, nombre=None, color="oro", logo=None, sub=None, dur=4.5, x=.25, tam=580, **kw):
    return peg(en, img, nombre, color, logo, sub, dur, x=x, y=.47, tam=tam, **kw)


def vs(de, a, ea, eb, titulo, sub=None, ganador=None, marca=None, y=.45):
    return mg(L.versus((EQ(ea), ea), (EQ(eb), eb), titulo, sub, ganador=ganador), de, a, [marca] if marca else [], y=y,
              nombre=f"versus {ea}-{eb}")


# ================================================================== GANCHO (0-50 s): portada y MG cada 3-5 s
FX = [
    mg(L.apertura("WORLDS 2026", "Todo lo que ha pasado · al 27 de octubre"), 0.0, 3.3, x=.5, y=.5, nombre="apertura"),
    dict(tipo="destello", en=0.15, fuerza=.7),
    # «Llegaron a Texas como campeones de China… y se fueron sin ganar una sola partida.»
    mg(L.eliminado(EQ("AL"), "Anyone's Legend", "Campeón de China 2026"), 3.3, 9.0, [6.0, 7.8], y=.45, nombre="AL eliminado"),
    # «Anyone's Legend, el primer sembrado del LPL, eliminado cero a tres en la fase suiza del Mundial 2026.»
    peg(9.3, "Tarzan", "Tarzan", R, "AL", "Jungla", dur=6.9, x=.17, y=.47, tam=400, gris=True),
    peg(10.3, "Shanks", "Shanks", R, "AL", "Medio", dur=5.9, x=.83, y=.47, tam=400, gris=True),
    peg(11.2, "Hope", "Hope", R, "AL", "Tirador", dur=5.0, x=.5, y=.36, tam=340, gris=True, sello=("0-3", 0), marcas=[13.2]),
    tar(11.5, 16.2, "Primer sembrado del LPL", "Fuera en la fase suiza", R, logo="AL", dato="0-3", x=.5, y=.82),
    # «Y el último golpe se lo dio un equipo de Norteamérica.»
    vs(16.3, 20.1, "TLAW", "AL", "Team Liquid elimina a AL", "Día 4 · ronda 3", ganador=0, marca=18.0),
    dict(tipo="destello", en=16.65, fuerza=.5),
    # «Pero esa no fue la única sorpresa.»
    tar(20.2, 22.4, "Y no fue la única sorpresa", None, "oro", x=.5, y=.45, tam=84),
    # «En cuatro días vimos a China perder sus cuatro partidas del arranque,»
    mg(L.caida("China en el día 1", [(EQ(c), n) for c, n in (("AL", "AL"), ("BLG", "BLG"), ("TES", "TES"), ("IG", "IG"))], "0-4"),
       22.4, 26.7, [22.5, 23.3, 24.2, 24.7, 25.4, 25.9], y=.45, nombre="caida China"),
    # «el primer pentakill del torneo,»
    gran(26.7, "Smash", "Smash", A, "DK", "Tirador · Kai'Sa", dur=1.85, x=.27, tam=520),
    peg(26.9, ART("Kaisa_carga"), dur=1.65, x=.74, y=.46, tam=470),
    tar(27.1, 28.5, "Pentakill", "El primero del Mundial", A, logo="DK", dato="5", x=.5, y=.84, tam=54),
    # «una remontada imposible contra T1…»
    vs(28.5, 30.85, "DK", "T1", "DK remonta a T1", "Día 2 · una sola pelea", ganador=0, marca=30.2),
    dict(tipo="destello", en=28.85, fuerza=.5),
    # «y a un equipo de Estados Unidos quitándole una partida al mejor de Corea.»
    vs(30.9, 35.6, "LYON", "GEN", "LYON le quita una partida a Gen.G", "Día 3 · partida 1", ganador=0, marca=33.8, y=.42),
    peg(32.3, "Inspired", "Inspired", A, "LYON", "Jungla", dur=3.3, x=.13, y=.55, tam=330),
    # «Si no has visto nada, tranquilo. En los próximos veinte minutos te pongo al día con todo:»
    tar(36.0, 41.3, "¿No viste nada?", "Te pongo al día en 20 minutos", "oro", x=.5, y=.2, tam=70),
    # «las mejores jugadas, analizadas pausa por pausa, los mejores jugadores, los mejores equipos… y lo que viene esta semana.»
    mg(L.menu([(ART("Kaisa"), "Las jugadas", "oro"), (JUG("Smash"), "Los jugadores", "azul"), (EQ("GEN"), "Los equipos", "oro"),
               (EQ("T1"), "Lo que viene", "rojo")]), 40.8, 49.8, [41.5, 44.9, 46.3, 47.7], y=.5, nombre="menu"),
]

# ================================================================== FORMATO (50-135 s)
FX += [
    tar(50.8, 55.9, "El formato", "Lo explica casi todo", "oro", x=.5, y=.2, tam=74),
    # «Son diecinueve equipos. Cuatro empezaron en Los Ángeles, en el play-in, y solo uno sobrevivió.»
    tar(56.1, 58.3, "19 equipos", "Mundial 2026", "oro", x=.5, y=.2, tam=64),
    mg(L.caida("Play-in · Los Ángeles", [(EQ("KC"), "Karmine Corp", True), (EQ("C9"), "Cloud9 KIA"), (EQ("FUR"), "FURIA"),
                                          (EQ("MVK"), "MVK")], sello="FUERA"),
       58.3, 63.2, [58.4, 61.2, 61.5, 61.8], y=.47, nombre="caida play-in"),
    # «Los otros dieciséis se juegan todo en la fase suiza, en Allen, Texas. La regla es simple: tres victorias… tres derrotas…»
    mg(L.suiza("Fase suiza · Allen, Texas"), 63.4, 88.0, [64.0, 66.9, 68.5, 69.5, 72.2, 85.0], y=.46, nombre="suiza"),
    tar(69.5, 72.1, "3 victorias", "Cuartos de final", A, x=.5, y=.86, tam=50),
    tar(72.2, 74.9, "3 derrotas", "A casa", R, x=.5, y=.86, tam=50),
    tar(79.2, 82.6, "Al mejor de 1", "Sin margen de error", "oro", x=.5, y=.86, tam=50),
    # «Y hay una regla que lo cambia todo: el Fearless Draft. Dentro de una serie, un campeón que ya se usó no se puede…»
    tar(89.6, 99.7, "Fearless Draft", "En una serie, ningún campeón se repite", "oro", x=.5, y=.17, tam=74),
    peg(93.6, os.path.join(ICO, "LeeSin.png"), "Lee Sin", "oro", sub="Partida 1", dur=6.0, x=.2, y=.5, tam=240),
    peg(94.4, os.path.join(ICO, "LeeSin.png"), "Lee Sin", R, sub="Partida 2", dur=5.2, x=.8, y=.5, tam=240, gris=True,
        sello=("YA USADO", 0), marcas=[95.6]),
    # «Ocho equipos pasan a cuartos. La final es el 14 de noviembre, en el Barclays Center de Nueva York.»
    tar(100.0, 106.5, "8 equipos a cuartos", "Del 3 al 6 de noviembre", A, x=.28, y=.2, tam=52),
    tar(102.2, 106.5, "Final · 14 de noviembre", "Barclays Center · Nueva York", "oro", x=.72, y=.8, tam=56),
    # lema, himno (el clip es el video oficial de «Know My Name») y Cyanide
    tar(108.0, 115.8, "«Este es nuestro momento»", "El lema de 2026", "oro", x=.5, y=.17, tam=58),
    tar(110.9, 115.8, "Know My Name", "Himno · True Damage", "oro", x=.72, y=.84, tam=52),
    tar(118.4, 123.4, "Cyanide", "Campeón del primer Mundial · 2011 · Fnatic", "oro", x=.5, y=.8, tam=58),
    # «Y ahí quiere llegar T1, el campeón de 2023, 2024 y 2025, que va por algo que nadie ha hecho jamás: su cuarto título seguido.»
    gran(124.2, "Faker", "Faker", R, "T1", "Medio · T1", dur=10.2, x=.24, tam=600),
    tar(125.6, 134.6, "T1 · 2023 · 2024 · 2025", "Tricampeón", R, logo="T1", dato="3", x=.7, y=.78, tam=56),
    tar(131.9, 134.6, "¿El cuarto seguido?", "Nadie lo ha hecho", "oro", x=.7, y=.2, tam=60),
]

# ================================================================== PLAY-IN (135-172 s)
FX += [
    tar(135.9, 139.2, "Play-in", "Los Ángeles · 15-18 de octubre", "oro", x=.5, y=.2, tam=70),
    tar(139.4, 146.2, "Karmine Corp", "3.º de Europa · su primer Mundial", A, logo="KC", x=.68, y=.78),
    gran(139.8, "Canna", "Canna", A, "KC", "Top", dur=6.4, x=.22, tam=520),
    vs(146.4, 151.4, "KC", "C9", "3-2 a Cloud9 KIA", "Necesitó las cinco partidas", ganador=0, marca=149.0),
    vs(151.5, 160.3, "KC", "MVK", "3-0 y 3-0 a MVK", "Serie final por el boleto", ganador=0, marca=154.3),
    peg(155.9, "Caliste", "Caliste", A, "KC", "Tirador", dur=4.3, x=.13, y=.55, tam=330),
    mg(L.caida("Fuera en el play-in", [(EQ("C9"), "Cloud9 KIA"), (EQ("FUR"), "FURIA"), (EQ("MVK"), "MVK")], sello="FUERA"),
       160.4, 164.9, [160.5, 161.0, 161.6, 162.4], y=.45, nombre="caida play-in 2"),
    vs(165.0, 172.3, "KC", "AL", "Su estreno: el campeón de China", "Día 1 · ronda 1", y=.43),
]

# ================================================================== DÍA 1 (172-212 s)
FX += [
    tar(175.1, 181.9, "Día 1 · 23 de octubre", "Fase suiza · ronda 1", "oro", x=.5, y=.2, tam=74),
    peg(178.6, "Knight", None, dur=3.4, x=.83, y=.52, tam=360, gris=True),
    mg(L.resultados("Día 1 · ronda 1", [(EQ("GEN"), "Gen.G", EQ("IG"), "Invictus", 0), (EQ("HLE"), "Hanwha Life", EQ("TES"), "Top Esports", 0),
                                         (EQ("MKOI"), "Movistar KOI", EQ("BLG"), "Bilibili", 0), (EQ("KC"), "Karmine Corp", EQ("AL"), "Anyone's Legend", 0)]),
       182.2, 196.4, [182.3, 184.5, 187.8, 193.4], y=.42, nombre="resultados día 1"),
    # «Cuatro equipos chinos, cuatro derrotas. Nunca había pasado…»
    peg(196.6, "Knight", "Knight", R, "BLG", None, dur=8.1, x=.14, y=.5, tam=330, gris=True),
    peg(197.0, "Rookie", "Rookie", R, "IG", None, dur=7.7, x=.38, y=.5, tam=330, gris=True),
    peg(197.4, "Tarzan", "Tarzan", R, "AL", None, dur=7.3, x=.62, y=.5, tam=330, gris=True),
    peg(197.8, "TheShy", "TheShy", R, "IG", None, dur=6.9, x=.86, y=.5, tam=330, gris=True),
    tar(199.6, 204.8, "Nunca había pasado", "El LPL sin ganar en la primera ronda", R, dato="0-4", x=.5, y=.17, tam=62),
    # «Y la pelea que lo resume todo está en esa última partida. Vamos a verla de cerca.»
    gran(205.3, "Canna", "Canna", A, "KC", "Jax", dur=5.0, x=.24, tam=520),
    gran(205.7, "Busio", "Busio", A, "KC", "Renata", dur=4.6, x=.76, tam=520),
    # el tramo EN VIVO (scene-026, 209.7-263.8) va solo con su rótulo: se oye la transmisión
    tar(212.3, 217.5, "En vivo", "Transmisión oficial · KC vs AL", R, logo="KC", x=.24, y=.17, tam=46),
]

# ================================================================== JUGADA 1: el cuádruple de Canna (263.8-322.9 s)
# j1.mp4 = resumen oficial del día 1 (_9iVitbeCio) desde 1000 s. Pelea: 75.0 = 24:36 (KC bajo la definitiva de Nocturne),
# 77 = 24:38 (definitivas de KC), 86.8 doble, 89 triple, 91.5 CUÁDRUPLE de Canna; 126 Barón de KC; 145-149 torre de la base.
FX += [
    J(1, 263.8, 265.1, 112.0, -32.0), rebobinar(263.8, 265.1, "24:36"),
    J(1, 265.1, 273.3, 70.5, .55),
    tar(265.1, 273.2, "Anyone's Legend", "Una composición para entrar de frente", R, logo="AL", x=.5, y=.86, tam=42),
    peg(266.8, ART("Olaf_carga"), "Olaf", R, sub="Breathe", dur=6.4, x=.07, y=.62, tam=210),
    peg(267.6, ART("Nocturne_carga"), "Nocturne", R, sub="Tarzan", dur=5.6, x=.18, y=.62, tam=210),
    peg(268.3, ART("Akali_carga"), "Akali", R, sub="Shanks", dur=4.9, x=.82, y=.62, tam=210),
    peg(269.1, ART("MissFortune_carga"), "Miss Fortune", R, sub="Hope", dur=4.1, x=.93, y=.62, tam=210),
    dict(tipo="destello", en=273.3, fuerza=.45),
    J(1, 273.3, 277.4, 75.0, 0),
    *pizarra3d("j1_pausa", 273.3, 277.4, [
        dict(tipo="foco", en=273.4, k=.42),
        dict(tipo="anillo", x=.715, y=.36, r=70, color=R, en=273.5, etiqueta="TARZAN", sub="NOCTURNE · KC A CIEGAS",
             lado="izq"),
        dict(tipo="anillo", x=.21, y=.27, r=60, color=R, en=273.7, etiqueta="SHANKS", sub="AKALI", lado="der"),
        dict(tipo="anillo", x=.385, y=.43, r=72, color=A, en=274.7, etiqueta="BUSIO", sub="RENATA",
             icono=os.path.join(ICO, "Renata.png"), lado="abajo"),
    ], "24:36", (fuente(1), 75.0)),
    # «…y su definitiva hace algo cruel: los enemigos que toca… se atacan entre ellos.» — la pausa en 3D (mesas_3d.py)
    *MESA("j1", 277.4, 282.27, "24:36"),
    peg(275.2, ART("Renata_carga"), "Renata", A, sub="Busio · KC", dur=7.0, x=.93, y=.42, tam=220),
    J(1, 282.27, 294.09, 75.0, .42),
    tar(282.4, 285.6, "Cámara lenta", "24:36 → 24:41", R, x=.1, y=.14, tam=30),
    tar(282.9, 294.2, "Definitiva de Renata", "Busio", A, icono="Renata", x=.87, y=.13, tam=30),
    tar(285.9, 294.2, "Onda de choque", "Kyeahoo · Orianna", A, icono="Orianna", x=.87, y=.21, tam=30),
    tar(288.8, 294.2, "Cataclismo", "Yike · Jarvan IV", A, icono="JarvanIV", x=.87, y=.29, tam=30),
    tar(290.9, 294.2, "AL, atrapado", "Peleándose consigo mismo", R, logo="AL", x=.5, y=.86, tam=40),
    J(1, 294.09, 300.0, 80.0, 1.79),
    peg(294.5, "Canna", "Canna", A, "KC", "Top", dur=5.4, x=.08, y=.55, tam=240),
    peg(295.5, ART("Jax_carga"), "Jax", A, sub="A la línea de atrás", dur=4.4, x=.93, y=.42, tam=220),
    dict(tipo="destello", en=300.0, fuerza=.6),
    J(1, 300.0, 305.24, 90.6, .55),
    tar(300.0, 305.2, "¡Cuádruple!", "Canna · Jax", A, logo="KC", dato="4", x=.16, y=.14, tam=44),
    tar(303.3, 305.2, "KC gana la pelea", "Cuatro por uno", A, x=.5, y=.86, tam=40),
    J(1, 305.24, 309.5, 126.0), J(1, 309.5, 313.21, 145.5),
    tar(306.1, 309.4, "Barón para KC", None, A, logo="KC", x=.5, y=.2, tam=60),
    mg(L.caida("Día 1: el LPL", [(EQ(c), n) for c, n in (("IG", "IG"), ("TES", "TES"), ("BLG", "BLG"), ("AL", "AL"))], "0-4"),
       308.4, 313.2, [308.5, 308.8, 309.2, 309.7, 310.2, 311.5], y=.42, nombre="caida China 2"),
    J(1, 313.21, 322.9, 149.2, 0),
    pizarra(313.21, 322.9, [dict(tipo="foco", en=313.3, k=.5)], "FIN", "LA LECCIÓN"),
    tar(313.3, 322.4, "La lección", None, "oro", x=.5, y=.3, tam=70),
    tar(314.8, 322.4, "AL no perdió por nivel", None, R, logo="AL", x=.5, y=.47, tam=58),
    tar(316.7, 322.4, "Peleó donde KC lo esperaba", None, A, logo="KC", x=.5, y=.64, tam=58),
    dict(tipo="cierra", en=322.2, dur=.45, a=322.91), dict(tipo="abre", en=322.91, dur=.45),
]

# ================================================================== DÍA 1 (resto) y DÍA 2 (323-381.8 s)
FX += [
    # «Ese mismo día, CTBC Flying Oyster, de Taiwán, sorprende a Team Liquid con una gran partida de Shadow en la jungla.»
    vs(323.4, 331.5, "CFO", "TLAW", "CTBC sorprende a Team Liquid", "Día 1 · de Taiwán", ganador=0, marca=327.1, y=.42),
    peg(329.6, "Shad0w", "Shadow", A, "CFO", "Jungla", dur=1.9, x=.88, y=.55, tam=300),
    # «LYON le da a Norteamérica su primera victoria, y el estadio de Allen explota.»
    peg(331.8, "Saint", "Saint", A, "LYON", "Medio", dur=5.4, x=.2, y=.5, tam=400),
    tar(332.6, 337.2, "LYON gana", "Primera victoria de Norteamérica", A, logo="LYON", x=.68, y=.78),
    dict(tipo="destello", en=335.8, fuerza=.45),
    # «T1 debuta con Faker en LeBlanc y despacha a Los Grandes, de Brasil, en veinticuatro minutos.»
    gran(337.4, "Faker", "Faker", R, "T1", "Medio · LeBlanc", dur=6.5, x=.24, tam=540),
    peg(338.9, ART("LeBlanc_carga"), "LeBlanc", R, sub="Faker", dur=5.0, x=.62, y=.45, tam=380),
    tar(341.4, 343.9, "T1 vence a Los Grandes", "De Brasil", R, logo="T1", dato="24'", x=.78, y=.84, tam=46),
    # «Y Dplus KIA voltea una partida que iba perdiendo contra G2. Guarda ese nombre: Dplus KIA. Va a aparecer mucho…»
    vs(344.2, 348.3, "DK", "G2", "DK remonta a G2", "Día 1 · 32 minutos", ganador=0, marca=345.0),
    peg(348.4, EQ("DK"), "Dplus KIA", A, sub="Guarda este nombre", dur=4.7, x=.5, y=.42, tam=380),
    # «24 de octubre. Día dos. Y el partido que todos marcaron en el calendario: Dplus KIA contra T1, los dos con una victoria.»
    tar(356.2, 361.2, "Día 2 · 24 de octubre", "Fase suiza · ronda 2", "oro", x=.5, y=.2, tam=74),
    vs(361.4, 366.7, "DK", "T1", "El duelo del día", "Los dos con 1-0", y=.47),
    # «Durante buena parte de la partida, T1 parecía tener la medida de DK: Faker con Anivia…, Peyz… con Caitlyn.»
    peg(367.4, "Faker", "Faker", R, "T1", "Anivia", dur=9.9, x=.15, y=.52, tam=380),
    peg(372.5, ART("Anivia_carga"), dur=4.9, x=.36, y=.48, tam=320),
    peg(373.9, "Peyz", "Peyz", R, "T1", "Caitlyn", dur=3.5, x=.64, y=.52, tam=380),
    peg(376.0, ART("Caitlyn_carga"), dur=1.4, x=.85, y=.48, tam=320),
    # «Hasta el dragón Anciano. Míralo primero en vivo.» → tramo EN VIVO (beat 045, 377.4-433.9, con el audio de la transmisión)
    tar(377.6, 381.2, "El dragón Anciano", "Míralo en vivo", "oro", x=.5, y=.2, tam=66),
    en_vivo(381.4, "Transmisión oficial · DK vs T1", "DK"),
]

# ================================================================== JUGADA 2: DK le voltea el Anciano a T1 (433.9-482.18 s)
# j2.mp4 = resumen del día 2 (Fbxau2uQc_E) desde 1960 s. 72.6 = 37:08 (Oner mata a Lucid: NO es la pelea); 73.9 = 40:24 la pelea
# del Anciano (Lucid vivo); pausa 74.6 = 40:25; 76-81 Destello de Career + Definitiva de Kalista; 85 «rampage» de Smash;
# 92.6 «Blue team has slain the Elder Dragon» (DK es azul); 106-112 nexo. Vivo (beat 045) termina en j2 102.5.
FX += [
    J(2, 433.9, 435.1, 102.5, -23.8), rebobinar(433.9, 435.1, "40:24"),
    J(2, 435.1, 438.79, 73.9, .19),
    tar(435.2, 438.7, "Alma de Nube", "Ya es de T1", R, logo="T1", x=.13, y=.14, tam=30),
    dict(tipo="destello", en=438.79, fuerza=.4),
    J(2, 438.79, 446.6, 74.6, 0),
    *pizarra3d("j2_pausa", 438.79, 446.6, [
        dict(tipo="foco", en=438.85, k=.4),
        anillo(.84, .27, 85, Y, 438.9, "ANCIANO", "T1 LO ESTÁ TIRANDO", "izq"),
        anillo(.665, .31, 46, R, 439.3), anillo(.71, .52, 46, R, 440.5, "T1", "+1,8K DE ORO", "der"), anillo(.62, .76, 64, R, 439.6),
        dict(tipo="zona", pts=[(.74, .12), (.95, .12), (.95, .42), (.74, .42)], color=R, en=443.3, alfa=.2),
        dict(tipo="texto", x=.84, y=.48, texto="CON SU BUFO, SE ACABA", color=R, en=444.4, tam=32),
    ], "40:25", (fuente(2), 74.6)),
    # «DK tiene una sola salida: pelear. Ya. Antes de que caiga el dragón.» — la pausa en 3D
    *MESA("j2", 446.6, 453.31, "40:25"),
    tar(440.6, 446.8, "T1 · +1,8K de oro", "Y ya tiene el alma de Nube", R, logo="T1", x=.5, y=.88, tam=34),
    # «Keria se lanza con Destello y la definitiva de Neeko sobre DK. Pero Smash usa la definitiva de Kalista para sacar a
    # Career de ahí… y Career responde con la definitiva de Renata.» (cuadros 78.0-79.6 y VOD 47:08) — cámara lenta con zoom
    J(2, 453.31, 461.1, 74.6, .64, zoom=(1.35, .45, .55), zoom_en=.15, zoom_dur=1.0),
    J(2, 461.1, 464.36, 79.6, .45, zoom0=(1.35, .45, .55), zoom=(1.35, .45, .55)),
    tar(453.4, 457.2, "Cámara lenta", "40:25 → 40:31", "oro", x=.1, y=.14, tam=30),
    peg(453.4, ART("Neeko_carga"), "Neeko", R, sub="Keria · Destello", dur=4.2, x=.07, y=.6, tam=210),
    tar(454.2, 463.9, "Destello y definitiva de Neeko", "Keria · T1", R, icono="Neeko", x=.87, y=.13, tam=30),
    peg(457.4, ART("Kalista_carga"), "Kalista", A, sub="Smash · definitiva", dur=6.8, x=.93, y=.6, tam=210),
    tar(458.3, 463.9, "Smash saca a Career", "Definitiva de Kalista", A, icono="Kalista", x=.87, y=.21, tam=30),
    peg(461.1, ART("Renata_carga"), "Renata", A, sub="Career responde", dur=3.2, x=.07, y=.6, tam=210),
    tar(462.3, 464.3, "Definitiva de Renata", "Career · DK", A, icono="Renata", x=.5, y=.86, tam=40),
    # «¡Y DK voltea la pelea entera! ¡De la nada, DK reduce a cenizas a T1… y se queda con el Anciano!»
    dict(tipo="destello", en=464.4, fuerza=.55),
    J(2, 464.36, 471.7, 81.07, 1.6, zoom0=(1.35, .45, .55), zoom=(1.0, .5, .5), zoom_dur=.8),
    peg(464.6, "Smash", "Smash", A, "DK", "Kalista", dur=6.9, x=.08, y=.55, tam=240),
    tar(466.9, 471.6, "DK voltea la pelea", "De la nada", A, logo="DK", x=.5, y=.86, tam=40),
    tar(470.6, 473.6, "Anciano para DK", None, A, logo="DK", x=.5, y=.2, tam=56),
    J(2, 471.7, 475.4, 92.8), J(2, 475.4, 482.18, 106.0),
    # «Una pelea. Eso fue todo. DK se pone dos a cero… y T1, el tricampeón, conoce su primera derrota del Mundial.»
    vs(473.7, 478.4, "DK", "T1", "DK se pone 2-0", "Una sola pelea", ganador=0, marca=474.7),
    tar(476.1, 481.9, "T1 · primera derrota", "El tricampeón cae a 1-1", R, logo="T1", x=.5, y=.84, tam=46),
    dict(tipo="cierra", en=481.5, dur=.45, a=482.18), dict(tipo="abre", en=482.18, dur=.45),
]

# ================================================================== DÍA 2 (resto) y DÍA 3 (482.2-554.2 s)
FX += [
    vs(483.4, 487.6, "GEN", "HLE", "Gen.G vence a Hanwha Life", "El clásico coreano", ganador=0, marca=484.8),
    gran(487.7, "Canyon", "Canyon", "oro", "GEN", "Jungla · imparable", dur=2.7, x=.75, tam=520),
    peg(490.4, "SkewMond", "SkewMond", A, "G2", "Jungla · Lee Sin", dur=6.6, x=.17, y=.5, tam=400),
    peg(492.7, ART("LeeSin_carga"), dur=4.3, x=.42, y=.46, tam=330),
    tar(494.0, 497.1, "G2 aplasta a Los Grandes", None, A, logo="G2", dato="21-9", x=.74, y=.8, tam=50),
    peg(497.4, "Rookie", "Rookie", A, "IG", "Medio", dur=7.1, x=.2, y=.5, tam=400),
    peg(497.9, "TheShy", "TheShy", A, "IG", "Top", dur=6.6, x=.8, y=.5, tam=400),
    tar(500.0, 504.5, "Campeones del mundo en 2018", "Invictus vence a Team Secret Whales", "oro", logo="IG", x=.5, y=.86, tam=44),
    vs(504.8, 509.3, "LYON", "KC", "LYON vence a Karmine Corp", "Norteamérica, 2-0", ganador=0, marca=505.2),
    vs(509.4, 513.7, "TES", "AL", "Top Esports vence a AL", "Día 2", ganador=0, marca=510.3),
    peg(513.8, "Tarzan", "Tarzan", R, "AL", "Jungla", dur=4.3, x=.17, y=.52, tam=360, gris=True),
    tar(513.9, 518.1, "Anyone's Legend", "Contra la pared", R, logo="AL", dato="0-2", x=.62, y=.5, tam=60),
    # «Así queda la tabla tras dos días…»
    mg(L.tabla("Tras dos días", [("2-0", "azul", [(EQ("GEN"), "Gen.G"), (EQ("DK"), "Dplus KIA"), (EQ("MKOI"), "Movistar KOI"),
                                                   (EQ("LYON"), "LYON")]),
                                  ("0-2 · a una derrota", "rojo", [(EQ("AL"), "Anyone's Legend"), (EQ("TLAW"), "Team Liquid"),
                                                                    (EQ("LOS"), "Los Grandes"), (EQ("TSW"), "Team Secret Whales")])]),
       518.2, 534.1, [520.9, 526.3], y=.5, nombre="tabla 2 días"),
    tar(537.3, 542.0, "Día 3 · 25 de octubre", "Fase suiza · ronda 3", "oro", x=.5, y=.2, tam=74),
    tar(542.0, 546.5, "Al mejor de 3", "Los 2-0 juegan por cuartos", A, x=.5, y=.84, tam=52),
    vs(547.1, 553.1, "DK", "MKOI", "Dplus KIA vs Movistar KOI", "Al mejor de 3 · partida 1", y=.46),
    en_vivo(553.4, "DK vs Movistar KOI · partida 1", "DK"),
]

# ================================================================== JUGADA 3: el pentakill de Smash (606.3-652.36 s)
# j3.mp4 = resumen del día 3 (Oix7cBcGmgM) desde 830 s. 32:30 (j ~50) KOI a +0,8K; pausa 59.5 = 38:23 (Jojopyun adelantado,
# Career encima); 60.4 el ancla conecta; 63.6 «Smash killing spree»; 67.8 doble; 72.5 triple; ~75 cuádruple; 79 PENTAKILL.
FX += [
    J(3, 606.3, 607.4, 92.0, -33.6), rebobinar(606.3, 607.4, "38:15"),
    J(3, 607.4, 613.68, 55.3, .67),
    tar(606.9, 612.9, "KOI se había acercado", "A menos de mil de oro · 32:30", R, logo="MKOI", x=.13, y=.14, tam=30),
    peg(610.1, ART("Anivia_carga"), "Anivia", R, sub="Jojopyun", dur=3.5, x=.07, y=.6, tam=210),
    dict(tipo="destello", en=613.68, fuerza=.4),
    J(3, 613.68, 617.3, 59.5, 0),
    *pizarra3d("j3_pausa", 613.68, 617.3, [
        dict(tipo="foco", en=613.75, k=.4),
        anillo(.385, .19, 55, R, 615.5, "JOJOPYUN", "ANIVIA · ADELANTADO", "izq"),
    ], "38:23", (fuente(3), 59.5)),
    # «…lejos de su equipo… y Career, con Nautilus, tiene el ancla lista.» — la pausa en 3D
    *MESA("j3", 617.3, 622.32, "38:23"),
    J(3, 622.32, 630.02, 59.5, .58),
    tar(622.6, 629.9, "El ancla atrapa a la Anivia", "Career · Nautilus", A, icono="Nautilus", x=.87, y=.13, tam=30),
    tar(624.6, 629.9, "Cae primero Myrwn", "Jayce · KOI", R, icono="Jayce", x=.87, y=.21, tam=30),
    peg(625.6, ART("Jayce_carga"), "Jayce", R, sub="Myrwn · el primero", dur=3.9, x=.93, y=.6, tam=210, gris=True),
    # «Ahora mira a Smash, con Kai'Sa. Entra a la pelea… y Supa cae. El Agotamiento que le lanzan no sirve de nada.»
    J(3, 630.02, 638.61, 64.0, .99, zoom=(1.28, .40, .48), zoom_dur=1.0),
    peg(630.7, "Smash", "Smash", A, "DK", "Kai'Sa", dur=7.8, x=.08, y=.55, tam=240),
    peg(631.5, ART("Kaisa_carga"), "Kai'Sa", A, sub="Smash · DK", dur=2.3, x=.93, y=.42, tam=220),
    tar(632.3, 633.8, "Entra a la pelea", None, A, icono="Kaisa", x=.5, y=.86, tam=36),
    peg(634.0, "Supa", "Supa", R, "MKOI", "Ezreal", dur=4.4, x=.93, y=.45, tam=220, gris=True),
    tar(634.8, 638.4, "El Agotamiento no basta", "Supa cae", R, icono="Ezreal", x=.5, y=.86, tam=36),
    # «¡Triple! ¡Cuádruple! ¡Y pentakill para Smash!»
    J(3, 638.61, 642.69, 72.5, 1.6, zoom0=(1.28, .40, .48), zoom=(1.0, .5, .5), zoom_dur=.6),
    dict(tipo="destello", en=638.6, fuerza=.4), dict(tipo="destello", en=639.0, fuerza=.45),
    dict(tipo="destello", en=640.4, fuerza=.7),
    tar(640.4, 645.3, "¡Pentakill!", "Smash · Kai'Sa", A, logo="DK", dato="5", x=.5, y=.84, tam=58),
    J(3, 642.69, 645.7, 79.0),
    gran(642.6, "Smash", "Smash", A, "DK", "El único pentakill", dur=3.1, x=.24, tam=520),
    peg(643.0, ART("Kaisa"), dur=2.7, x=.72, y=.45, tam=560),
    vs(645.7, 652.0, "DK", "MKOI", "DK gana la serie 2-0", "Primer clasificado a cuartos", ganador=0, marca=647.0),
    tar(648.9, 652.2, "Primero en cuartos", None, A, logo="DK", dato="3-0", x=.5, y=.86, tam=46),
    # «Y en la otra serie… LYON le hace a Gen.G lo que nadie esperaba.»
    vs(653.0, 657.6, "LYON", "GEN", "LYON vs Gen.G", "Al mejor de 3", y=.46),
    en_vivo(657.6, "LYON vs Gen.G · partida 1", "LYON"),
]

# ================================================================== JUGADA 4: Inspired y la caída de Chovy (711.0-752.7 s)
# j4.mp4 = resumen del día 3 desde 1230 s. 29.0 = 20:24 «Blue team has slain Baron Nashor» (LYON es azul); 84.0 = 34:41
# Inspired (Xin Zhao) dentro de Gen.G junto a Chovy; 90.5 = 34:48 cae Chovy. Vivo (beat 078) termina en j4 114.3.
FX += [
    J(4, 711.0, 712.0, 114.3, -90.0), rebobinar(711.0, 712.0, "20:15"),
    J(4, 712.0, 715.75, 24.3),
    tar(712.1, 715.6, "Gen.G acumula dragones", "Ese era su plan", R, logo="GEN", x=.87, y=.13, tam=30),
    dict(tipo="destello", en=715.75, fuerza=.4),
    J(4, 715.75, 722.3, 29.0, 0),
    *pizarra3d("j4_baron", 715.75, 722.3, [
        dict(tipo="foco", en=715.8, k=.4),
        anillo(.38, .33, 110, Y, 716.9, "BARÓN", "PARA LYON · 20:24", "abajo"),
        anillo(.27, .5, 85, A, 717.7, "LYON", None, "izq"),
        anillo(.57, .34, 44, R, 718.9), anillo(.785, .53, 44, R, 719.05), anillo(.555, .76, 44, R, 719.2),
        flecha([(.77, .50), (.63, .43), (.50, .37)], R, 719.4, "GEN.G LLEGA TARDE", off=(80, 50), guion=True),
        flecha([(.55, .72), (.50, .56), (.45, .44)], R, 719.55, guion=True),
    ], "20:24", (fuente(4), 29.0)),
    tar(718.9, 722.2, "Barón para LYON", "Minuto 20", A, logo="LYON", x=.5, y=.86, tam=40),
    J(4, 722.3, 723.9, 29.0, 34.4), rebobinar(722.3, 723.9, "34:41", "AVANCE RÁPIDO · +14 MIN"),
    # «Mira a Inspired, con Xin Zhao. / Inspired se mete con Xin Zhao al centro…» — la pausa 34:41 en 3D
    *MESA("j4", 723.9, 729.3, "34:41"),
    # «Inspired se mete con Xin Zhao al centro del equipo coreano, sin dudar.» (narración: «he jumped into the center»)
    J(4, 729.3, 732.41, 84.0, 1.3, zoom=(1.45, .40, .36), zoom_dur=1.0),
    peg(727.1, "Inspired", "Inspired", A, "LYON", "Jungla · Xin Zhao", dur=5.3, x=.08, y=.55, tam=240),
    peg(728.2, ART("XinZhao_carga"), "Xin Zhao", A, sub="Inspired", dur=4.2, x=.93, y=.45, tam=220),
    tar(728.9, 732.3, "Al centro de Gen.G", "Sin dudar", A, icono="XinZhao", x=.87, y=.13, tam=30),
    # «¡Chovy cae! ¡Y LYON gana la pelea!…» (kill feed 34:48: «LYON Dhokla has slain GEN Chovy»)
    dict(tipo="destello", en=732.41, fuerza=.6),
    J(4, 732.41, 741.88, 90.5, zoom0=(1.45, .40, .36), zoom=(1.0, .5, .5), zoom_dur=.8),
    tar(732.4, 736.9, "¡Chovy cae!", "Lo remata Dhokla · Olaf", A, logo="LYON", x=.16, y=.14, tam=44),
    peg(732.6, "Chovy", "Chovy", R, "GEN", "Medio · Anivia", dur=4.4, x=.93, y=.5, tam=230, gris=True),
    tar(734.0, 741.7, "LYON gana la pelea", "Norteamérica le quita una partida a Gen.G", A, logo="LYON", x=.5, y=.86, tam=40),
    peg(737.9, "Berserker", "Berserker", A, "LYON", "Tirador", dur=3.9, x=.93, y=.5, tam=230),
    # «Pero Gen.G es Gen.G. Ajusta, gana la segunda y la tercera, y se clasifica tres a cero. LYON cae…»
    vs(741.9, 748.6, "GEN", "LYON", "Gen.G gana la serie 2-1", "Y se clasifica 3-0 a cuartos", ganador=0, marca=745.4),
    tar(748.8, 752.6, "LYON cae", "Con la cabeza en alto", A, logo="LYON", x=.5, y=.84, tam=50),
    # «Los que iban uno a uno se jugaron todo a una sola partida. Y ahí apareció un viejo conocido.»
    tar(753.4, 757.2, "Récord 1-1", "Todo a una sola partida", "oro", x=.5, y=.2, tam=64),
    gran(757.4, "Rookie", "Rookie", A, "IG", "Campeón del mundo en 2018", dur=4.1, x=.5, tam=520),
    en_vivo(761.6, "Invictus vs Hanwha Life", "IG"),
]

# ================================================================== JUGADA 5: el cuádruple de Rookie (813.5-853.09 s)
# j5.mp4 = resumen del día 3 desde 215 s. 56.5 = 24:21 (IG +3,7K y sus 4 dragones: alma del Infernal); pausa 61.0 = 24:25
# (Rookie detrás); 64 «Rookie killing spree» (Gumayusi); 89 triple; 92 = 24:57 CUÁDRUPLE. Vivo (beat 090) termina en j5 91.
FX += [
    J(5, 813.5, 814.6, 91.0, -34.2), rebobinar(813.5, 814.6, "24:16"),
    J(5, 814.6, 823.03, 53.4, .9),
    tar(815.9, 822.9, "+3,7K de oro", "Invictus · 24:21", A, logo="IG", x=.13, y=.14, tam=30),
    tar(818.8, 822.9, "Alma del Infernal", "Cuatro dragones para IG", A, x=.13, y=.22, tam=30),
    tar(820.3, 822.9, "Hanwha sigue viva", None, R, logo="HLE", x=.5, y=.86, tam=40),
    dict(tipo="destello", en=823.03, fuerza=.4),
    # «Pausa. Mira dónde está Rookie: con Annie, detrás de su equipo.» — la pausa 24:25 en 3D
    *MESA("j5", 823.03, 827.82, "24:25"),
    # «Gumayusi se queda sin salida. Rookie lo remata. Y en el tres contra tres… la transformación de Lulu deja a Olaf…»
    # (24:40 «Rookie is on a rampage» y Gumayusi muere; 3 contra 3: Wei, Rookie, Meiko · Zeus, Zeka, Delight)
    J(5, 827.82, 837.29, 61.0, 1.5, zoom=(1.3, .45, .45), zoom_dur=1.0),
    peg(827.85, "Gumayusi", "Gumayusi", R, "HLE", "Kalista", dur=3.4, x=.93, y=.45, tam=220, gris=True),
    peg(829.5, "Rookie", "Rookie", A, "IG", "Annie", dur=9.6, x=.08, y=.55, tam=240),
    tar(830.2, 832.9, "Rookie lo remata", None, A, icono="Annie", x=.5, y=.86, tam=36),
    peg(833.1, ART("Lulu_carga"), "Lulu", A, sub="Meiko · polimorfo", dur=4.0, x=.93, y=.45, tam=220),
    tar(834.7, 837.2, "Olaf, sin poder hacer nada", "Zeus · Hanwha Life", R, icono="Olaf", x=.5, y=.86, tam=36),
    # «¡Triple para Rookie… y cuádruple!»
    J(5, 837.29, 840.44, 88.8, 1.3, zoom0=(1.3, .45, .45), zoom=(1.0, .5, .5), zoom_dur=.6),
    dict(tipo="destello", en=837.3, fuerza=.5), dict(tipo="destello", en=838.7, fuerza=.65),
    tar(837.3, 842.4, "¡Cuádruple!", "Rookie · Annie", A, logo="IG", dato="4", x=.16, y=.14, tam=44),
    vs(840.5, 846.4, "IG", "HLE", "Invictus gana", "Ahora va 2-1, a una serie de cuartos", ganador=0, marca=844.1),
    vs(846.5, 853.0, "TES", "G2", "Top Esports también gana", "Día 3", ganador=0, marca=848.3),
]

# ================================================================== DÍA 4 (853.1-922.9 s)
FX += [
    tar(855.8, 860.0, "Día 4 · 26 de octubre", "El más cruel", R, x=.5, y=.2, tam=74),
    tar(860.2, 862.8, "Los 0-2 se juegan la vida", None, R, x=.5, y=.84, tam=50),
    vs(863.2, 867.5, "T1", "CFO", "T1 vence a CTBC", "La pelea perfecta", ganador=0, marca=866.5),
    peg(867.6, "Doggo", "Doggo", R, "CFO", "Tirador", dur=5.0, x=.2, y=.5, tam=380, gris=True),
    tar(869.0, 872.6, "Atrapan a Doggo", "El que cargaba a CTBC", R, logo="T1", x=.68, y=.78, tam=46),
    tar(872.8, 875.9, "Partida terminada", "T1 vence a CTBC", R, logo="T1", dato="27'", x=.68, y=.78, tam=50),
    gran(876.1, "Knight", "Knight", "oro", "BLG", "Medio · en gran forma", dur=6.0, x=.25, tam=520),
    tar(878.7, 882.0, "Bilibili vence a Karmine Corp", "Una pelea de cinco por cero", "oro", logo="BLG", dato="5-0", x=.7, y=.8, tam=44),
    vs(882.3, 886.0, "LOS", "TSW", "Los Grandes remonta otra vez", "2-0", ganador=0, marca=882.9),
    mg(L.caida("Fuera en la fase suiza", [(EQ("TSW"), "Team Secret Whales")], sello="FUERA"), 886.1, 890.0, [886.2, 888.4],
       y=.45, nombre="caida TSW"),
    tar(890.1, 893.8, "La última serie", "La que da título a este video", "oro", x=.5, y=.2, tam=64),
    vs(893.9, 900.4, "TLAW", "AL", "Team Liquid vs Anyone's Legend", "Los dos 0-2 · el que pierda se va", y=.47),
    # «Recuerda quién es AL: en septiembre ganó la liga china, 3 a 1 a Bilibili en la final…»
    vs(900.6, 906.5, "AL", "BLG", "Final de la liga china", "Septiembre · AL campeón 3-1", ganador=0, marca=903.2),
    gran(906.6, "Tarzan", "Tarzan", R, "AL", "Jungla", dur=5.3, x=.25, tam=520),
    tar(908.4, 911.8, "«Uno de los mejores del mundo»", "Así lo llamó la transmisión", "oro", logo="AL", x=.68, y=.8, tam=42),
    tar(911.9, 913.9, "Nadie los veía caer", None, R, x=.5, y=.2, tam=60),
    # «Liquid gana la primera con una Camille de Morgan… Y en la segunda, llega el Barón que lo decide todo.»
    peg(914.1, "Morgan", "Morgan", A, "TLAW", "Top · Camille", dur=4.5, x=.17, y=.5, tam=380),
    peg(915.8, ART("Camille_carga"), dur=2.8, x=.42, y=.46, tam=320),
    tar(915.0, 918.6, "Partida 1 para Liquid", None, A, logo="TLAW", x=.72, y=.8, tam=48),
    tar(919.3, 922.7, "Partida 2", "El Barón que lo decide todo", "oro", x=.5, y=.2, tam=60),
    en_vivo(922.9, "Team Liquid vs AL · partida 2", "TLAW"),
]

# ================================================================== JUGADA 6: el Barón de Liquid (974.8-1028.3 s)
# jugada.mp4 = VOD wjoQ0ze5bJ4 desde 2833 s (reloj = s + 39:40). Vivo (beat 108) = VOD 2909 → termina en jugada.mp4 132.
# El análisis (40:14 → 41:46) es una JUGADA EN 3D (nucleo/tactica3d, 27-oct-2026): j6_3d.py escribe tactica3d/j6.json con
# las posiciones medidas en el minimapa y los datos de la narración oficial; render3d.py → medios/_fuente/j6_3d.mp4
# (empieza en t = 975.0 del video: desde = t - 975.0). Al grito del castigo vuelve el VOD real.
J6 = fuente(6)

FX += [
    J(6, 974.8, 975.7, 132.0, -105.0), rebobinar(974.8, 975.7, "40:16"),
    # «Minuto 40. Liquid pierde en asesinatos, 11 a 17… pero va arriba en oro y en torres.» — el mapa en 3D
    V3(975.7, 982.4), dict(tipo="destello", en=975.7, fuerza=.45),
    # «Toma el tercer dragón y le quita a AL el alma.» — VOD: el dragón cae a las 40:20-40:21 (40:21 = buff «3 %»)
    dict(tipo="destello", en=982.4, fuerza=.35),
    J(6, 982.4, 984.6, 38.2), J(6, 984.6, 986.4, 41.0, 0),
    *pizarra3d("j6_dragon", 984.6, 986.4, [
        dict(tipo="foco", en=984.6, k=.3),
        anillo(.285, .45, 50, A, 984.65, "YEON", "REMATA EL DRAGÓN", "izq", icono="Xayah"),
        dict(tipo="zona", pts=[(.40, .50), (.66, .44), (.70, .62), (.50, .78), (.30, .74)], color=R, en=984.9, alfa=.16),
        dict(tipo="texto", x=.5, y=.86, texto="AL SE QUEDA SIN ALMA", color=R, en=985.0, tam=42),
    ], "40:21", (J6, 41.0)),
    # «Pausa. Mira arriba: una oleada de Liquid empuja sola hacia el inhibidor, y Morgan se teletransporta…» — 3D
    V3(986.4, 994.6), dict(tipo="destello", en=986.4, fuerza=.3),
    # «AL tiene que soltar el dragón y volver a su base.» — VOD 40:38: Morgan pega al inhibidor, Tarzan, Hope y Kael llegan
    dict(tipo="destello", en=994.6, fuerza=.35),
    J(6, 994.6, 998.2, 58.0, 0),
    *pizarra3d("j6_inhib", 994.6, 998.2, [
        dict(tipo="foco", en=994.65, k=.3),
        anillo(.27, .37, 46, A, 994.7, "MORGAN", "LLEGÓ CON TP", "izq", icono="Kled"),
        anillo(.36, .34, 70, Y, 995.0, "INHIBIDOR DE AL", None, "arriba"),
        anillo(.45, .41, 40, R, 995.6), anillo(.70, .36, 40, R, 995.75), anillo(.79, .26, 40, R, 995.9),
        flecha([(.45, .41), (.40, .39), (.33, .37)], R, 996.1, dur=.5),
        flecha([(.70, .36), (.56, .35), (.42, .34)], R, 996.3, dur=.6, etiqueta="AL VUELVE A DEFENDER", off=(150, 70)),
        flecha([(.79, .26), (.66, .27), (.50, .31)], R, 996.5, dur=.6),
    ], "40:38", (J6, 58.0)),
    # «Intenta encerrar a Liquid por un flanco… pero Liquid se retira a tiempo, y AL se queda a oscuras.» + «Liquid empieza
    # el Barón. Y Hope…» — 3D
    V3(998.2, 1007.2), dict(tipo="destello", en=998.2, fuerza=.3),
    # «…dispara el cohete de Jinx buscando el robo…» — VOD 41:44,8 congelado: el cohete sale de Hope, al este del foso
    dict(tipo="destello", en=1007.2, fuerza=.4),
    J(6, 1007.2, 1010.27, 124.8, 0),
    *pizarra3d("j6_cohete", 1007.2, 1010.27, [
        dict(tipo="foco", en=1007.25, k=.32),
        anillo(.34, .36, 120, Y, 1007.3, "BARÓN · 3 634 PV", "LIQUID LO ESTÁ TIRANDO", "abajo"),
        anillo(.28, .34, 34, A, 1007.4), anillo(.28, .42, 34, A, 1007.5), anillo(.26, .50, 34, A, 1007.6),
        anillo(.87, .37, 46, R, 1007.5, "HOPE · JINX", "COHETE PARA ROBARLO", "izq", icono="Jinx"),
    ], "41:45", (J6, 124.8),
        extra=dict(proyectiles=[dict(desde=(.86, .38), a=(.36, .36), de=1008.1, llega=1009.6, color="#ff4fc3", alto=4)])),
    # «¡Pero Josedeodo no falla el castigo! ¡Barón para Liquid!»: el VOD desde 41:44.4 (el cohete y el castigo)
    J(6, 1010.27, 1012.2, 124.4), J(6, 1012.2, 1013.2, 126.3, 0),
    dict(tipo="destello", en=1012.2, fuerza=.6),
    *pizarra3d("j6_castigo", 1012.2, 1013.2, [dict(tipo="anillo", x=.39, y=.30, r=70, color=A, en=1012.2, etiqueta="¡CASTIGO!",
                                                    sub="JOSEDEODO", lado="der", icono=os.path.join(ICO, "SummonerSmite.png"))],
               "41:46", (J6, 126.3)),
    J(6, 1013.2, 1014.66, 126.3, .4),
    peg(1010.4, "Josedeodo", "Josedeodo", A, "TLAW", "Jungla · Pantheon", dur=4.2, x=.08, y=.55, tam=240),
    tar(1012.7, 1014.6, "Barón para Liquid", None, A, logo="TLAW", x=.5, y=.84, tam=48),
    # «Minutos después, Liquid termina la partida. Anyone's Legend, campeón de China, se despide cero a tres…» — clips 119-120
    tar(1015.8, 1018.3, "Liquid termina la partida", "2-0 en la serie", A, logo="TLAW", x=.5, y=.84, tam=48),
    mg(L.eliminado(EQ("AL"), "Anyone's Legend", "Campeón de China · fuera 0-3"), 1018.4, 1025.2, [1021.7, 1022.5], y=.45,
       nombre="AL eliminado 2"),
    dict(tipo="destello", en=1025.8, fuerza=.6),
    tar(1025.4, 1028.2, "El favorito cayó", None, R, x=.5, y=.45, tam=96),
]

# ================================================================== META, JUGADORES, EQUIPOS (1027.6-1215.3 s)
FX += [
    tar(1028.4, 1030.5, "Un dato del juego", None, "oro", x=.5, y=.2, tam=64),
    tar(1030.6, 1036.1, "Fearless Draft", "Ningún campeón se repite en una serie", "oro", x=.5, y=.2, tam=64),
    peg(1036.3, ART("LeeSin_carga"), "Lee Sin", "oro", sub="El que nadie suelta", dur=2.8, x=.5, y=.48, tam=430),
    mg(L.barras("Los más elegidos · fase suiza", [(os.path.join(ICO, c + ".png"), n, v) for c, n, v in
                                                   (("LeeSin", "Lee Sin", 12), ("Orianna", "Orianna", 10), ("Renata", "Renata", 10),
                                                    ("Alistar", "Alistar", 10), ("Nocturne", "Nocturne", 10))], 29),
       1039.1, 1049.0, [1039.2, 1044.0, 1044.8, 1045.6, 1046.6], y=.5, nombre="barras picks"),
    peg(1049.6, ART("Renata"), "Renata", "oro", sub="En las dos peleas", dur=5.4, x=.5, y=.45, tam=560),
    peg(1053.2, EQ("KC"), dur=1.8, x=.15, y=.5, tam=240), peg(1054.3, EQ("DK"), dur=.9, x=.85, y=.5, tam=240),
    tar(1055.4, 1060.2, "Peleas en equipo", "No duelos", "oro", x=.5, y=.2, tam=70),
    # Los cinco mejores jugadores (números de gol.gg; docstring de guion.py)
    tar(1061.2, 1066.9, "Los 5 mejores jugadores", "Números de gol.gg", "oro", x=.5, y=.2, tam=74),
    mg(L.ficha_jugador(JUG("Knight"), "Knight", EQ("BLG"), 5, [("Participación en asesinatos", "89 %", .89),
                                                              ("Daño de su equipo", "35 %", .35)], "oro", "Medio · Bilibili"),
       1067.2, 1081.2, [1072.0, 1076.0], y=.5, nombre="ficha Knight"),
    mg(L.ficha_jugador(JUG("Rookie"), "Rookie", EQ("IG"), 4, [("Campeón del mundo", "2018", 1.0),
                                                             ("Cuádruple con Annie", "4", .8)], "azul", "Medio · Invictus"),
       1081.4, 1092.4, [1086.0, 1089.3], y=.5, nombre="ficha Rookie"),
    peg(1089.4, ART("Annie_carga"), dur=2.9, x=.91, y=.55, tam=260),
    mg(L.ficha_jugador(JUG("Canyon"), "Canyon", EQ("GEN"), 3, [("KDA", "10,5", .85), ("Participación en asesinatos", "80 %", .8)],
                       "oro", "Jungla · Gen.G"), 1092.6, 1105.4, [1097.1, 1099.4], y=.5, nombre="ficha Canyon"),
    mg(L.ficha_jugador(JUG("ShowMaker"), "ShowMaker", EQ("DK"), 2, [("Daño de su equipo", "30 %", .3),
                                                                   ("Muertes por partida", "1", .12)], "azul", "Medio · DK"),
       1105.6, 1117.0, [1111.2, 1114.0], y=.5, nombre="ficha ShowMaker"),
    dict(tipo="destello", en=1118.2, fuerza=.55),
    mg(L.ficha_jugador(JUG("Smash"), "Smash", EQ("DK"), 1, [("Partidas ganadas", "4 de 4", 1.0), ("KDA", "10,7", .9),
                                                           ("Pentakills", "1 · el único", .6)], "azul", "Tirador · DK"),
       1117.1, 1128.0, [1120.2, 1121.6, 1124.4], y=.5, nombre="ficha Smash"),
    peg(1124.4, ART("Kaisa_carga"), dur=3.5, x=.91, y=.55, tam=260),
    tar(1128.2, 1138.1, "Menciones honoríficas", None, "oro", x=.5, y=.17, tam=60),
    peg(1129.8, "Keria", "Keria", R, "T1", "Soporte", dur=8.3, x=.17, y=.55, tam=360),
    peg(1130.4, "Faker", "Faker", R, "T1", "Medio", dur=7.7, x=.42, y=.55, tam=360),
    peg(1134.1, "SkewMond", "SkewMond", A, "G2", "Jungla · Lee Sin", dur=4.0, x=.72, y=.55, tam=360),
    # Ranking de equipos
    tar(1139.8, 1144.0, "Mi ranking", "Después de cuatro días", "oro", x=.5, y=.2, tam=74),
    mg(L.ranking("Mi ranking · tras 4 días", [(EQ("GEN"), "Gen.G", "3-0", "+313 de oro por minuto · 8 de cada 10 dragones", "oro"),
                                             (EQ("DK"), "Dplus KIA", "3-0", "4 de 4 partidas", "azul"),
                                             (EQ("T1"), "T1", "2-1", "Solo perdió contra DK", "rojo"),
                                             (EQ("IG"), "Invictus Gaming", "2-1", "Dos seguidas tras perder", "oro"),
                                             (EQ("LYON"), "LYON", "2-1", "La sorpresa", "azul")]),
       1144.2, 1199.1, [1144.3, 1158.3, 1171.8, 1181.4, 1190.2], y=.5, nombre="ranking equipos"),
    peg(1146.0, "Canyon", None, dur=4.0, x=.08, y=.6, tam=220), peg(1150.6, "Chovy", None, dur=4.2, x=.92, y=.6, tam=220),
    peg(1154.8, "Ruler", None, dur=3.2, x=.08, y=.6, tam=220),
    peg(1164.6, "ShowMaker", None, dur=4.0, x=.08, y=.6, tam=220), peg(1168.8, "Smash", None, dur=3.0, x=.92, y=.6, tam=220),
    peg(1175.9, "Faker", None, dur=4.5, x=.08, y=.6, tam=220), peg(1177.5, "Keria", None, dur=3.5, x=.92, y=.6, tam=220),
    peg(1186.4, "Rookie", None, dur=3.5, x=.08, y=.6, tam=220), peg(1187.0, "TheShy", None, dur=3.0, x=.92, y=.6, tam=220),
    peg(1192.0, "Inspired", None, dur=4.0, x=.08, y=.6, tam=220), peg(1194.6, "Berserker", None, dur=4.2, x=.92, y=.6, tam=220),
    mg(L.tabla("Los demás", [("China · 2-1", "rojo", [(EQ("IG"), "Invictus"), (EQ("TES"), "Top Esports"), (EQ("BLG"), "Bilibili")]),
                             ("Europa", "azul", [(EQ("MKOI"), "Movistar KOI · 2-1"), (EQ("G2"), "G2 · 1-2"),
                                                 (EQ("KC"), "Karmine Corp · 1-2")])]),
       1199.4, 1214.1, [1199.9, 1207.4], y=.5, nombre="tabla China Europa"),
    peg(1205.2, EQ("AL"), "Anyone's Legend", R, sub="Fuera", dur=2.2, x=.9, y=.5, tam=220, gris=True),
]

# ================================================================== LO QUE VIENE, LECCIONES, CIERRE (1215.3-1321.1 s)
FX += [
    tar(1216.1, 1221.8, "¿Qué viene?", "Ronda 4 · desde el 28 de octubre · al mejor de 3", "oro", x=.5, y=.2, tam=74),
    mg(L.resultados("Por el pase a cuartos · 2-1", [(EQ("MKOI"), "Movistar KOI", EQ("T1"), "T1", None, "28 OCT"),
                                                    (EQ("IG"), "Invictus", EQ("LYON"), "LYON", None, "28 OCT"),
                                                    (EQ("TES"), "Top Esports", EQ("BLG"), "Bilibili", None, "29 OCT")]),
       1222.0, 1232.9, [1225.2, 1227.2, 1229.4], y=.5, nombre="cruces 2-1"),
    mg(L.resultados("Para no irse a casa · 1-2", [(EQ("KC"), "Karmine Corp", EQ("CFO"), "CTBC", None, "29 OCT"),
                                                  (EQ("TLAW"), "Team Liquid", EQ("LOS"), "Los Grandes", None, "30 OCT"),
                                                  (EQ("HLE"), "Hanwha Life", EQ("G2"), "G2", None, "30 OCT")]),
       1233.1, 1242.8, [1235.8, 1238.3, 1240.7], y=.5, nombre="cruces 1-2"),
    mg(L.calendario("Lo que viene", [("31 oct", "Ronda 5", "oro"), ("3-6 nov", "Cuartos", "azul"),
                                     ("7-8 nov", "Semifinales\nTexas", "azul"), ("14 nov", "Final\nNueva York", "amarillo")]),
       1242.9, 1256.4, [1244.1, 1248.1, 1250.9, 1253.7], y=.5, nombre="calendario"),
    vs(1256.6, 1260.2, "T1", "MKOI", "La serie que no te puedes perder", "28 de octubre"),
    gran(1260.3, "Faker", "Faker", R, "T1", "¿El cuarto título?", dur=3.8, x=.25, tam=520),
    tar(1261.2, 1264.0, "Si T1 cae…", "El cuarto título se complica", R, logo="T1", x=.7, y=.8, tam=46),
    peg(1264.2, EQ("HLE"), "Hanwha Life", R, sub="1-2 · podría irse", dur=5.1, x=.7, y=.45, tam=340),
    peg(1264.9, "Zeus", None, dur=4.4, x=.25, y=.5, tam=360),
    tar(1270.7, 1273.9, "Tres lecciones", None, "oro", x=.5, y=.2, tam=80),
    tar(1274.1, 1281.3, "1 · Corea manda", "Gen.G y DK, invictos · T1 sigue vivo", A, x=.5, y=.2, tam=64),
    peg(1275.7, EQ("GEN"), dur=5.6, x=.25, y=.55, tam=300), peg(1276.9, EQ("DK"), dur=4.4, x=.5, y=.55, tam=300),
    peg(1279.5, EQ("T1"), dur=1.8, x=.75, y=.55, tam=300),
    tar(1281.6, 1290.6, "2 · China, en crisis", "0-4 el primer día y su campeón fuera", R, x=.5, y=.2, tam=64),
    mg(L.caida("China", [(EQ("AL"), "AL"), (EQ("IG"), "IG", True), (EQ("TES"), "TES", True), (EQ("BLG"), "BLG", True)],
               sello="FUERA"), 1283.4, 1290.6, [1283.5, 1287.0], y=.56, nombre="caida China 3"),
    tar(1290.9, 1301.7, "3 · Occidente llegó con hambre", None, A, x=.5, y=.17, tam=60),
    mg(L.resultados("Occidente", [(EQ("LYON"), "LYON", EQ("GEN"), "Gen.G", 0), (EQ("MKOI"), "Movistar KOI", EQ("BLG"), "Bilibili", 0),
                                  (EQ("TLAW"), "Team Liquid", EQ("AL"), "Anyone's Legend", 0)]),
       1293.4, 1301.8, [1293.6, 1296.7, 1298.9], y=.56, nombre="occidente"),
    # «Así va el Mundial. El campeón de China, fuera. Corea, con dos equipos invictos. Y T1, a una serie de seguir soñando.»
    peg(1304.5, EQ("AL"), "AL", R, sub="Fuera", dur=7.3, x=.17, y=.5, tam=300, gris=True),
    peg(1306.4, EQ("GEN"), "Gen.G", A, sub="Invicto", dur=5.4, x=.39, y=.5, tam=300),
    peg(1307.2, EQ("DK"), "Dplus KIA", A, sub="Invicto", dur=4.6, x=.61, y=.5, tam=300),
    peg(1309.0, EQ("T1"), "T1", R, sub="A una serie", dur=2.8, x=.83, y=.5, tam=300),
    tar(1312.1, 1316.7, "¿Quién levanta la copa?", "Déjalo en los comentarios", "oro", x=.5, y=.45, tam=80),
    mg(L.apertura("NOS VEMOS EN CUARTOS", "Worlds 2026 · desde el 3 de noviembre"), 1316.8, 1321.09, x=.5, y=.5, nombre="cierre"),
]

ROTULOS = []
SFX = {}
_entra = sorted({e.get("de", 0) for e in FX if e.get("tipo") == "mg" and not e.get("nombre", "").startswith(("pizarra", "rebobinar"))})
PISTAS = ([dict(sfx="whoosh", en=0.1, vol=.6), dict(sfx="golpe", en=0.3, vol=.7), dict(sfx="subida", en=5.0, vol=.4),
           dict(sfx="golpe", en=6.0, vol=.75), dict(sfx="scratch", en=6.05, vol=.3), dict(sfx="golpe", en=7.8, vol=.6),
           dict(sfx="golpe", en=13.2, vol=.6), dict(sfx="golpe", en=16.65, vol=.6),
           dict(sfx="golpe", en=26.0, vol=.6), dict(sfx="golpe", en=28.85, vol=.55), dict(sfx="golpe", en=31.25, vol=.55),
           dict(sfx="rebobina", en=263.8, vol=.5), dict(sfx="clic", en=273.3, vol=.55), dict(sfx="golpe", en=273.32, vol=.3),
           dict(sfx="whoosh2", en=282.4, vol=.35), dict(sfx="subida", en=298.0, vol=.45), dict(sfx="golpe", en=300.0, vol=.7),
           dict(sfx="clic", en=313.21, vol=.5), dict(sfx="whoosh", en=322.0, vol=.45)]
          + [dict(sfx="whoosh2", en=t, vol=.22) for t in _entra]
          + [dict(sfx="golpe", en=t, vol=.35) for t in (23.3, 24.2, 24.7, 25.4, 61.2, 61.5, 61.8, 160.5, 161.0, 161.6, 95.6)]
          + [dict(sfx="pop", en=t, vol=.3) for t in (273.5, 273.7, 274.7)])
# tramo 3 (27-oct): rebobinados, pausas (clic + golpe suave), destellos y lo que se dibuja en cada pizarra
_rebob = (433.9, 606.3, 711.0, 722.3, 813.5, 974.8)
_pausas = (438.79, 613.68, 715.75, 723.9, 823.03, 986.45)
_golpes = [d["en"] for d in FX if d.get("tipo") == "destello" and d["en"] > 323]
_dibujo = sorted({e["en"] for d in FX if d.get("nombre", "").startswith("pizarra") and d["de"] > 323
                  for e in getattr(d["fn"], "_els", [])})
PISTAS += ([dict(sfx="rebobina", en=t, vol=.5) for t in _rebob] + [dict(sfx="clic", en=t, vol=.55) for t in _pausas]
           + [dict(sfx="golpe", en=t + .02, vol=.3) for t in _pausas] + [dict(sfx="golpe", en=t, vol=.55) for t in _golpes]
           + [dict(sfx="subida", en=t, vol=.42) for t in (462.0, 636.6, 730.9, 835.5, 1009.6, 1023.6)]
           + [dict(sfx="pop", en=t, vol=.28) for t in (438.9, 440.5, 447.25, 449.3, 615.5, 617.6, 619.0, 716.9, 717.7, 719.4,
                                                        724.8, 725.3, 824.9, 826.0)]
           + [dict(sfx="whoosh", en=t, vol=.45) for t in (975.7, 990.6, 1004.55, 1008.1)]
           + [dict(sfx="whoosh2", en=t, vol=.28) for t in (277.4, 446.6, 617.3, 723.9, 982.4, 986.4, 994.6, 998.2, 1007.2)]
           + [dict(sfx="whoosh2", en=t, vol=.3) for t in (998.25, 1000.2)]
           + [dict(sfx="golpe", en=t, vol=.45) for t in (984.6, 990.96, 993.43, 1009.6)]
           + [dict(sfx="golpe", en=t, vol=.35) for t in (886.2, 888.4, 1287.0, 1021.7, 1022.5)])
