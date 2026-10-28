# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «IG vs LYON» (estilo análisis táctico, docs/estilo_analisis_tactico.md), copiada en su forma de
videos/lol_worlds_2026/efectos.py. Editado como Warcraft: pegatina real casi en cada frase, MG de mg_lol por partes con la voz.
Cada jugada: el tramo EN VIVO (beat sin voz, con el audio de la transmisión) y luego el ANÁLISIS con MÁS pausas (el usuario,
27-oct): FX `video` congelado (vel=0) + telestrador (anillos, flechas, rutas, zonas, foco) + capas 3D sobre el video + «mesa».
Tiempos ABSOLUTOS (timeline.json). Posiciones: fracción del cuadro, medidas en previews/cuadros/j*_<t>.jpg (rejilla.py).
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




# ───────────────────────────────────────── anclas a la VOZ (timeline.json): los efectos siguen a las palabras ─────────────
import json as _json
import re as _re
import unicodedata as _ud

_TL = _json.load(open(os.path.join(_D, "timeline.json"), encoding="utf-8"))
_FR = {f["key"]: f for e in _TL["escenas"] for f in e["frases"]}
_ES = {e["id"]: e for e in _TL["escenas"]}


def _n(s):
    s = _ud.normalize("NFD", s.lower())
    return _re.sub(r"[^a-z0-9]", "", "".join(c for c in s if _ud.category(c) != "Mn"))


def T0(k):
    return _FR[k]["t0"]


def T1(k):
    return _FR[k]["t1"]


def W(k, palabra, n=0, fin=False):
    """instante en que la voz dice `palabra` (n-ésima aparición) en la frase k"""
    p = _n(palabra)
    hits = [w for w in _FR[k]["words"] if _n(w["w"]).startswith(p)]
    if len(hits) <= n:
        raise KeyError(f"{k}: no encuentro «{palabra}» ({n}) en: {' '.join(w['w'] for w in _FR[k]['words'])}")
    return hits[n]["e" if fin else "s"]


def ESC(i):
    return _ES[i]["t0"], _ES[i]["t1"]


def SEQ(n, tramos):
    """tramos [(de, a, desde_clip, vel)] → FX video encadenados del clip de la jugada n"""
    return [J(n, de, a, desde, vel, **({"zoom": z} if z else {})) for de, a, desde, vel, *z_ in tramos
            for z in [z_[0] if z_ else None]]


def ICON(c):
    return os.path.join(ICO, c + ".png")


def x2(de, a, texto="▶▶ x2"):
    return tar(de, a, texto, None, "oro", x=.09, y=.13, tam=28)


# ================================================================== GANCHO: portada y MG cada 3-5 s
g = "gancho_"
FX = [
    mg(L.apertura("IG vs LYON", "Worlds 2026 · fase suiza · ronda 4"), 0.0, W(g + "0", "uno"), x=.5, y=.5, nombre="apertura"),
    dict(tipo="destello", en=0.15, fuerza=.7),
    vs(W(g + "0", "uno"), T1(g + "0") + .2, "IG", "LYON", "Hoy · al mejor de 3", "28 de octubre · Allen, Texas", y=.42),
    tar(W(g + "0", "cuartos"), T1(g + "0") + .2, "Uno pasa a cuartos", "El otro, a una derrota de casa", "oro", x=.5, y=.84, tam=50),
    gran(T0(g + "1"), EQ("IG"), "Invictus Gaming", R, sub="China · LPL", dur=W(g + "1", "todavia") - T0(g + "1"), x=.22, tam=430),
    tar(W(g + "1", "primer"), T1(g + "1") + .2, "Campeón del mundo 2018", "El primer título de China", R, logo="IG", dato="2018",
        x=.66, y=.78, tam=52),
    peg(W(g + "1", "todavia"), "TheShy", "TheShy", R, "IG", "Campeón 2018", dur=T1(g + "1") - W(g + "1", "todavia") + .2, x=.2,
        y=.45, tam=360),
    peg(W(g + "1", "dos"), "Rookie", "Rookie", R, "IG", "Campeón 2018", dur=T1(g + "1") - W(g + "1", "dos") + .2, x=.42, y=.42,
        tam=360),
    gran(T0(g + "2"), EQ("LYON"), "LYON", A, sub="Norteamérica · LCS", dur=W(g + "2", "hoy") - T0(g + "2"), x=.78, tam=430),
    tar(W(g + "2", "Mexico"), W(g + "2", "hoy"), "Nacida en México", "2013 · Lyon Gaming", A, logo="LYON", x=.32, y=.78, tam=52),
    tar(W(g + "2", "2017"), W(g + "2", "hoy"), "2017: cambio de nombre", "Por orden de Riot", R, x=.32, y=.2, tam=48),
    peg(W(g + "2", "hoy"), "Inspired", "Inspired", A, "LYON", "Capitán · jungla", dur=T1(g + "2") - W(g + "2", "hoy") + .2, x=.24,
        y=.47, tam=400),
    tar(W(g + "2", "esperanza"), T1(g + "2") + .2, "La esperanza de Norteamérica", None, A, x=.66, y=.78, tam=50),
    tar(T0(g + "3"), W(g + "3", "historia"), "¿Nunca los has visto?", "Te los presento en 12 minutos", "oro", x=.5, y=.2, tam=66),
    mg(L.menu([(EQ("IG"), "La historia", "rojo"), (EQ("LYON"), "El camino", "azul"), (JUG("Rookie"), "Los jugadores", "oro"),
               (ART("Annie"), "Las jugadas", "amarillo")]),
       W(g + "3", "historia") - .3, T1(g + "3") + .3,
       [W(g + "3", "historia"), W(g + "3", "camino"), W(g + "3", "jugadores"), W(g + "3", "jugadas")], y=.5, nombre="menu"),
]
# ================================================================== LO QUE ESTÁ EN JUEGO
g = "juego_"
FX += [
    tar(T0(g + "0"), W(g + "0", "fase"), "Lo que está en juego", None, "oro", x=.5, y=.2, tam=74),
    mg(L.suiza("Fase suiza · Allen, Texas"), W(g + "0", "fase"), T1(g + "0") + .3,
       [W(g + "0", "fase"), W(g + "0", "fase") + .6, W(g + "0", "regla"), W(g + "0", "victorias"), W(g + "0", "derrotas"),
        T1(g + "0")], y=.46, nombre="suiza"),
    tar(W(g + "0", "victorias"), W(g + "0", "derrotas"), "3 victorias", "Cuartos de final", A, x=.5, y=.88, tam=46),
    tar(W(g + "0", "derrotas"), T1(g + "0") + .3, "3 derrotas", "A casa", R, x=.5, y=.88, tam=46),
    mg(L.tabla("Tras tres rondas", [("3-0 · ya en cuartos", "azul", [(EQ("GEN"), "Gen.G"), (EQ("DK"), "Dplus KIA")]),
                                    ("2-1 · se juegan el pase", "oro", [(EQ("IG"), "Invictus Gaming"), (EQ("LYON"), "LYON"),
                                                                        (EQ("T1"), "T1"), (EQ("MKOI"), "Movistar KOI")])]),
       T0(g + "1"), W(g + "1", "gane"), [T0(g + "1") + .1, T0(g + "1") + .6], y=.5, nombre="tabla"),
    vs(W(g + "1", "gane"), T1(g + "1") + .2, "IG", "LYON", "El que gane: 3-1", "Directo a cuartos", y=.4),
    tar(W(g + "1", "pierda"), T1(g + "1") + .2, "El que pierda: 2-2", "Serie a muerte el sábado 31", R, x=.5, y=.84, tam=48),
    tar(T0(g + "2"), W(g + "2", "Fearless"), "Al mejor de 3", "Gana quien llegue a dos", "oro", x=.5, y=.2, tam=66),
    tar(W(g + "2", "Fearless"), T1(g + "2") + .2, "Fearless Draft", "En la serie, ningún campeón se repite", "oro", x=.5, y=.17,
        tam=66),
    peg(W(g + "2", "campeon"), ICON("Annie"), "Annie", "oro", sub="Partida 1", dur=T1(g + "2") - W(g + "2", "campeon"), x=.24,
        y=.55, tam=240),
    peg(W(g + "2", "elegir") - .8, ICON("Annie"), "Annie", R, sub="Partida 2", dur=T1(g + "2") - W(g + "2", "elegir") + .8, x=.76,
        y=.55, tam=240, gris=True, sello=("YA USADO", 0), marcas=[W(g + "2", "elegir")]),
    tar(W(g + "2", "planes"), T1(g + "2") + .2, "Tres planes distintos", None, "oro", x=.5, y=.86, tam=48),
]
# ================================================================== IG: HISTORIA
g = "ig_historia_"
FX += [
    gran(T0(g + "0"), EQ("IG"), "Invictus Gaming", R, sub="Fundado en 2011 · China", dur=T1(g + "0") - T0(g + "0") + .2, x=.27,
         tam=520),
    tar(W(g + "0", "2018"), T1(g + "0") + .2, "2018", "Volvamos atrás", "oro", x=.72, y=.5, tam=110),
    tar(T0(g + "1"), W(g + "1", "IG"), "Incheon · 3 de noviembre de 2018", "Final del Mundial", "oro", x=.5, y=.2, tam=56),
    vs(W(g + "1", "IG"), W(g + "1", "primer"), "IG", "FNC", "IG 3 · Fnatic 0", "Final del Mundial 2018", ganador=0,
       marca=W(g + "1", "cero"), y=.42),
    tar(W(g + "1", "primer"), W(g + "1", "ochenta"), "El primer título de China", None, R, logo="IG", x=.5, y=.8, tam=56),
    tar(W(g + "1", "ochenta"), T1(g + "1") + .2, "85 minutos", "La final más corta de la historia", "oro", dato="85", x=.5, y=.8,
        tam=56),
    gran(W(g + "2", "TheShy") - .2, "TheShy", "TheShy", R, "IG", "Top · campeón 2018", dur=T1(g + "2") - W(g + "2", "TheShy") + .4,
         x=.25, tam=520),
    gran(W(g + "2", "Rookie") - .2, "Rookie", "Rookie", R, "IG", "Medio · campeón 2018", dur=T1(g + "2") - W(g + "2", "Rookie") + .4,
         x=.75, tam=520),
    tar(W(g + "2", "Ocho"), T1(g + "2") + .2, "8 años después… siguen ahí", "Juntos de nuevo desde diciembre de 2024", "oro",
        x=.5, y=.17, tam=54),
    gran(T0(g + "3"), "Meiko", "Meiko", R, "IG", "Soporte · capitán", dur=W(g + "3", "Tres") - T0(g + "3"), x=.25, tam=540),
    tar(W(g + "3", "campeon"), W(g + "3", "primer"), "Campeón del mundo 2021", "Con EDG", "oro", logo="EDG", x=.7, y=.62, tam=52),
    tar(W(g + "3", "primer"), W(g + "3", "Tres"), "1.000 partidas en el LPL", "El primero en lograrlo", "oro", dato="1000", x=.7,
        y=.62, tam=52),
    peg(W(g + "3", "Tres"), "TheShy", "TheShy", R, "IG", "2018", dur=T1(g + "3") - W(g + "3", "Tres") + .2, x=.2, y=.47, tam=330),
    peg(W(g + "3", "Tres") + .25, "Rookie", "Rookie", R, "IG", "2018", dur=T1(g + "3") - W(g + "3", "Tres"), x=.5, y=.47, tam=330),
    peg(W(g + "3", "Tres") + .5, "Meiko", "Meiko", R, "IG", "2021", dur=T1(g + "3") - W(g + "3", "Tres") - .25, x=.8, y=.47,
        tam=330),
    tar(W(g + "3", "Tres") + .6, T1(g + "3") + .2, "3 campeones del mundo", None, "oro", dato="3", x=.5, y=.86, tam=48),
    peg(W(g + "4", "Wei"), "Wei", "Wei", R, "IG", "Jungla · MVP del MSI 2022", dur=T1(g + "4") - W(g + "4", "Wei") + .2, x=.24,
        y=.48, tam=430),
    peg(W(g + "4", "JiaQi"), "JiaQi", "JiaQi", R, "IG", "Tirador", dur=T1(g + "4") - W(g + "4", "JiaQi") + .2, x=.76, y=.48,
        tam=430),
    tar(W(g + "4", "entrenador"), T1(g + "4") + .2, "Helper", "Entrenador · Corea del Sur", R, logo="IG", x=.5, y=.86, tam=48),
]
# ================================================================== IG: CAMINO
g = "ig_camino_"
FX += [
    mg(L.calendario("Invictus Gaming en 2026", [("Split 2", "Fuera de\nplayoffs", "rojo"), ("Split 3", "3.º", "oro"),
                                                ("Regional", "1-3 TES\n3-1 JDG", "azul"), ("Mundial", "LPL n.º 4", "amarillo")]),
       T0(g + "0"), T1(g + "1") + .3,
       [W(g + "0", "segunda"), W(g + "1", "tercera"), W(g + "1", "clasificacion"), W(g + "1", "ultimo")], y=.5,
       nombre="calendario IG"),
    tar(W(g + "1", "ganaron"), T1(g + "1") + .3, "3-1 a JD Gaming", "El último boleto de China", R, logo="IG", x=.5, y=.86, tam=48),
    mg(L.resultados("IG en el Mundial", [(EQ("GEN"), "Gen.G", EQ("IG"), "Invictus Gaming", 0),
                                          (EQ("IG"), "Invictus Gaming", EQ("TSW"), "Secret Whales", 0),
                                          (EQ("IG"), "Invictus Gaming", EQ("HLE"), "Hanwha Life", 0)]),
       T0(g + "2"), W(g + "3", "veintinueve"), [T0(g + "2") + .2, W(g + "3", "remontaron"), W(g + "3", "aplastaron")], y=.45,
       nombre="resultados IG"),
    tar(W(g + "2", "cuatro"), T1(g + "2") + .2, "China, 0-4 en el primer día", None, R, x=.5, y=.86, tam=46),
    tar(W(g + "3", "veintinueve"), T1(g + "3") + .3, "29 a 9", "IG aplasta al campeón del MSI", R, logo="IG", dato="29-9", x=.5,
        y=.5, tam=70),
    gran(T0(g + "4"), "Rookie", "Rookie", R, "IG", "Annie", dur=T1(g + "4") - T0(g + "4") + .3, x=.75, tam=500),
    tar(T0(g + "4") + .4, T1(g + "4") + .3, "La pelea que explica a IG", "IG vs Hanwha Life · minuto 24", R, x=.33, y=.8, tam=48),
]


# ───────────────────────────────────────── piezas de las jugadas ─────────────────────────────────────────────────────────
TIEMPOS_MESAS = {}


def CLIP(n, de, a, t0, t1, **kw):
    """el tramo t0→t1 del clip de la jugada n, estirado o acelerado para llenar [de, a)"""
    return J(n, de, a, t0, (t1 - t0) / (a - de), **kw)


def P(n, de, a, t, els, reloj, d3=None):
    """PAUSA: el cuadro t congelado + telestrador 2D (o capa 3D sobre el video si d3 = nombre de la capa)"""
    if d3:
        return [J(n, de, a, t, 0), *pizarra3d(d3, de, a, els, reloj, (fuente(n), t))]
    return [J(n, de, a, t, 0), pizarra(de, a, els, reloj)]


def MESA2(k, de, a, reloj):
    TIEMPOS_MESAS[k] = (round(de, 2), round(a, 2))
    return MESA(k, de, a, reloj)


def NX(k):
    """inicio de la frase siguiente (o fin de escena): los tramos de video cubren también el silencio entre frases"""
    esc, i = k.rsplit("_", 1)
    sig = f"{esc}_{int(i) + 1}"
    return T0(sig) if sig in _FR else _ES[esc]["t1"]


def texto(t, sub, x, y, en, color=Y, tam=36, icono=None):
    d = dict(tipo="texto", texto=t, sub=sub, x=x, y=y, en=en, color=color, tam=tam)
    if icono:
        d["icono"] = ICON(icono)
    return d


# ================================================================== JUGADA 1 · IG vs HLE (j1: reloj = t + 23:...; t=86 → 24:23)
f = "jugada1_"
e0, e1 = ESC("jugada1")
FX += [en_vivo(e0 + .3, "Transmisión oficial · IG vs Hanwha Life", "IG"),
       tar(e0 + .3, e0 + 5.5, "Minuto 24", "Mira primero la pelea entera", "oro", x=.76, y=.17, tam=40)]
a = T0(f + "0")
FX += [J(1, a, a + 1.2, 120, -30), rebobinar(a, a + 1.2, "24:21"), dict(tipo="destello", en=a + 1.2, fuerza=.4)]
FX += P(1, a + 1.2, NX(f + "0"), 84, [
    anillo(.43, .075, 40, A, W(f + "0", "cuatro"), "+3.800 DE ORO", "IG", lado="abajo"),
    texto("ALMA INFERNAL", "IG · CUATRO DRAGONES", .26, .55, W(f + "0", "alma"), color=A),
    texto("BARÓN", "LO ACABA DE ROBAR HANWHA", .74, .55, W(f + "0", "Baron"), color=R),
    texto("HANWHA NECESITA PELEAR", None, .5, .78, W(f + "0", "necesita"), color=R, tam=40),
], "24:21")
b = W(f + "1", "Rookie")
FX += P(1, T0(f + "1"), b, 86, [
    dict(tipo="foco", en=T0(f + "1") + .2, k=.4),
    anillo(.43, .39, 62, R, W(f + "1", "Nearsighted"), "NEARSIGHTED", "SIN VISIÓN", lado="der"),
    anillo(.557, .245, 54, R, W(f + "1", "Nearsighted") + .3),
    anillo(.115, .135, 50, R, W(f + "1", "Nearsighted") + .5),
    texto("PARANOIA", "LA DEFINITIVA DE WEI · NOCTURNE", .5, .82, W(f + "1", "definitiva"), color=A, icono="Nocturne"),
], "24:23", d3="j1_paranoia")
FX += [CLIP(1, b, NX(f + "1"), 86, 92),
       peg(b + .3, "Kanavi", "Kanavi", R, "HLE", "Cae la jungla de Hanwha", dur=NX(f + "1") - b - .3, x=.1, y=.62, tam=210,
           gris=True)]
b = W(f + "2", "directo")
FX += P(1, T0(f + "2"), b, 92, [
    anillo(.307, .30, 58, R, T0(f + "2") + .3, "ZEKA", "LISSANDRA", lado="izq", icono="Lissandra"),
    anillo(.432, .65, 58, A, W(f + "2", "Destello"), "JIAQI", "EL TIRADOR", lado="der", icono="Yunara"),
    flecha([(.31, .31), (.35, .48), (.42, .62)], R, W(f + "2", "Destello"), "DESTELLO", off=(-120, 0)),
], "24:29")
FX += [CLIP(1, b, NX(f + "2"), 92, 99),
       peg(b + 1.2, "JiaQi", "JiaQi", A, "IG", "Cae el tirador", dur=NX(f + "2") - b - 1.2, x=.1, y=.62, tam=210, gris=True)]
b = W(f + "3", "clave")
FX += P(1, T0(f + "3"), b, 99, [
    dict(tipo="foco", en=T0(f + "3") + .2, k=.42),
    anillo(.344, .57, 74, R, W(f + "3", "Olaf"), "ZEUS · OLAF", "INMUNE AL CONTROL", lado="izq", icono="Olaf"),
], "24:36", d3="j1_olaf")
FX += MESA2("j1", b, NX(f + "3"), "24:36")
b = W(f + "4", "todo")
FX += [CLIP(1, T0(f + "4"), b, 99, 107),
       peg(T0(f + "4") + .8, "Gumayusi", "Gumayusi", R, "HLE", "Atrapado por Rookie", dur=b - T0(f + "4") - .8, x=.1, y=.62,
           tam=210, gris=True)]
FX += P(1, b, NX(f + "4"), 107, [
    anillo(.41, .56, 70, R, b + .1, "ZEUS", "SE ACABÓ SU DEFINITIVA", lado="izq"),
    texto("ATURDIMIENTO", "ANNIE · ROOKIE", .78, .3, W(f + "4", "aturdimiento"), color=A, icono="Annie"),
    texto("MIEDO", "NOCTURNE · WEI", .78, .45, W(f + "4", "miedo"), color=A, icono="Nocturne"),
    texto("POLIMORFO", "LULU · MEIKO", .78, .6, W(f + "4", "polimorfo"), color=A, icono="Lulu"),
], "24:44")
a = T0(f + "5")
FX += [CLIP(1, a, NX(f + "5"), 107, 123), x2(a, NX(f + "5"), "▶▶ ACELERADO"),
       dict(tipo="destello", en=W(f + "5", "cuadruple"), fuerza=.6),
       tar(W(f + "5", "cuadruple"), NX(f + "5"), "¡Cuádruple!", "Rookie · Annie", A, logo="IG", dato="4", x=.16, y=.14, tam=40),
       tar(W(f + "5", "veinticuatro"), NX(f + "5"), "24 a 9", None, A, x=.5, y=.86, tam=46)]
a = T0(f + "6")
FX += [CLIP(1, a, e1, 112, 123), tar(a, a + 2.5, "Repetición", "Cámara lenta", R, x=.1, y=.14, tam=30),
       tar(W(f + "6", "leccion"), W(f + "6", "Si"), "La lección de IG", "Pelear en el momento justo", "oro", x=.5, y=.18, tam=56),
       tar(W(f + "6", "Si"), e1, "Si IG retrocede…", "…está esperando", "oro", x=.5, y=.18, tam=56)]

# ================================================================== IG: JUGADORES
g = "ig_jugadores_"
FX += [
    mg(L.ficha_jugador(JUG("Wei"), "Wei", EQ("IG"), 1, [("Muertes en 3 partidas", "5", .2), ("KDA", "9,4", .94),
                                                        ("Participación", "78 %", .78)], R, sub="Jungla · Nocturne"),
       T0(g + "0"), T1(g + "0") + .2, [W(g + "0", "muertes"), W(g + "0", "KDA"), W(g + "0", "mejor")], y=.5, nombre="ficha Wei"),
    mg(L.ficha_jugador(JUG("Rookie"), "Rookie", EQ("IG"), 2, [("Asesinatos", "17", .68), ("Edad", "29 años", .5)], R,
                       sub="Medio · Annie"),
       T0(g + "1"), W(g + "1", "JiaQi"), [W(g + "1", "diecisiete"), W(g + "1", "veintinueve")], y=.5, nombre="ficha Rookie"),
    mg(L.ficha_jugador(JUG("JiaQi"), "JiaQi", EQ("IG"), 3, [("Asesinatos", "20", .8), ("Récord ante HLE", "12/4/6", .6)], R,
                       sub="Tirador · el que remata"),
       W(g + "1", "JiaQi"), T1(g + "1") + .2, [W(g + "1", "veinte"), W(g + "1", "remata")], y=.5, nombre="ficha JiaQi"),
    mg(L.ficha_jugador(JUG("Meiko"), "Meiko", EQ("IG"), 4, [("Participación", "82 %", .82), ("Asistencias", "45", .9)], R,
                       sub="Soporte · el capitán"),
       T0(g + "2"), T1(g + "2") + .2, [W(g + "2", "ochenta"), W(g + "2", "capitan")], y=.5, nombre="ficha Meiko"),
    vs(T0(g + "3"), T1(g + "3") + .3, "TSW", "IG", "IG iba perdiendo", "Ronda 2 · contra Team Secret Whales",
       marca=W(g + "3", "hasta"), ganador=1, y=.42),
]

# ================================================================== JUGADA 2 · TSW vs IG (j2: t=100 → 22:34)
f = "jugada2_"
e0, e1 = ESC("jugada2")
FX += [en_vivo(e0 + .3, "Transmisión oficial · Secret Whales vs IG", "IG"),
       tar(e0 + .3, e0 + 5.5, "Minuto 22", "IG va abajo en asesinatos", "oro", x=.76, y=.17, tam=40)]
a = T0(f + "0")
FX += [J(2, a, a + 1.2, 124, -20), rebobinar(a, a + 1.2, "22:34"), dict(tipo="destello", en=a + 1.2, fuerza=.4)]
FX += P(2, a + 1.2, NX(f + "0"), 100, [
    anillo(.47, .035, 44, R, W(f + "0", "diez"), "10 A 8", "SECRET WHALES ARRIBA", lado="abajo"),
    texto("ORO: EMPATE", "42,1K CONTRA 41,9K", .26, .5, W(f + "0", "oro"), color=Y),
    texto("IG · 3 DRAGONES", "CON EL CUARTO, EL ALMA", .74, .5, W(f + "0", "tres"), color=A),
], "22:34")
FX += P(2, T0(f + "1"), NX(f + "1"), 100, [
    anillo(.40, .425, 60, A, W(f + "1", "Ashe") - .6, "ROOKIE", "ORIANNA · A PROTEGER", lado="der", icono="Orianna"),
    anillo(.505, .66, 60, A, W(f + "1", "Ashe"), "JIAQI", "ASHE · A PROTEGER", lado="der", icono="Ashe"),
    dict(tipo="zona", pts=[(.0, .38), (.22, .38), (.24, .82), (.0, .82)], color=R, en=W(f + "1", "sorprender"), alfa=.16),
    texto("EL PELIGRO", "QIYANA Y LOCKE POR EL FLANCO", .14, .3, W(f + "1", "sorprender"), color=R),
    texto("PELEAR DE FRENTE", "EL PLAN DE IG", .62, .86, W(f + "1", "frente"), color=A),
], "22:34")
b = W(f + "2", "Wei")
FX += [CLIP(2, T0(f + "2"), b, 100, 104),
       peg(T0(f + "2") + .4, ICON("Qiyana"), "Hizto", R, sub="Qiyana · se queda corto", dur=b - T0(f + "2") - .4, x=.1, y=.62,
           tam=180)]
FX += P(2, b, NX(f + "2"), 104, [
    dict(tipo="foco", en=b + .1, k=.4),
    anillo(.10, .45, 46, R, b + .3, "A CIEGAS", "NEARSIGHTED", lado="der"),
    anillo(.20, .53, 46, R, b + .5),
    anillo(.08, .61, 46, R, b + .7),
    anillo(.344, .20, 52, A, W(f + "2", "definitiva"), "WEI", "PARANOIA", lado="der", icono="Nocturne"),
], "22:38", d3="j2_paranoia")
b = W(f + "3", "TheShy")
FX += [CLIP(2, T0(f + "3"), b, 104, 112)]
FX += P(2, b, NX(f + "3"), 112, [
    flecha([(.12, .99), (.2, .86), (.29, .72)], A, b + .1, "TELETRANSPORTE", off=(140, 10)),
    anillo(.297, .70, 58, A, b + .5, "THESHY", "K'SANTE · CIERRA EL FLANCO", lado="der", icono="KSante"),
], "22:46")
b = W(f + "4", "cuatro")
FX += P(2, T0(f + "4"), b, 112.6, [dict(tipo="foco", en=T0(f + "4") + .1, k=.35)], "22:47")
FX += MESA2("j2", b, NX(f + "4"), "22:47")
a, b = T0(f + "5"), W(f + "5", "Baron")
FX += [J(2, a, a + 4.0, 112.6, .55), CLIP(2, a + 4.0, b, 114.8, 128), x2(a + 4.0, b, "▶▶ ACELERADO"),
       dict(tipo="destello", en=a + .4, fuerza=.6),
       tar(a + .3, a + 4.0, "Onda de choque", "Rookie · Orianna", A, icono="Orianna", x=.16, y=.14, tam=40),
       tar(W(f + "5", "cuatro"), b, "4 por 0", "Para IG", A, logo="IG", dato="4-0", x=.5, y=.86, tam=46),
       CLIP(2, b, NX(f + "5"), 162, 162 + (NX(f + "5") - b)),
       tar(b, NX(f + "5"), "Barón para IG", None, A, logo="IG", x=.5, y=.2, tam=56),
       tar(W(f + "5", "directo"), NX(f + "5"), "El patrón de IG", "Deja entrar al rival… y castiga", "oro", x=.5, y=.86, tam=50)]

# ================================================================== LYON: HISTORIA
g = "lyon_historia_"
FX += [
    mg(L.apertura("LYON", "Una historia que empieza en México"), T0(g + "0") - .2, T1(g + "0") + .3, x=.5, y=.5,
       nombre="apertura LYON"),
    mg(L.calendario("La historia de LYON", [("2013", "Lyon Gaming\nnace en México", "oro"), ("2017", "Multa y\ncambio de nombre", "rojo"),
                                            ("2018-2024", "Rainbow7", "azul"), ("2024", "Fusión con\nSix Karma", "oro"),
                                            ("2026", "Salta\nal LCS", "amarillo")]),
       T0(g + "1"), T1(g + "2") + .3,
       [W(g + "1", "2013"), W(g + "1", "2017"), W(g + "2", "Rainbow7"), W(g + "2", "2024"), W(g + "2", "2026")], y=.42,
       nombre="calendario LYON"),
    tar(W(g + "1", "multa"), T1(g + "1") + .2, "Multa de 12.500 dólares", "Y cambio de nombre obligatorio", R, x=.5, y=.84,
        tam=46),
    tar(W(g + "2", "LCS"), T1(g + "2") + .3, "LCS 2026", "La liga norteamericana", A, logo="LYON", x=.5, y=.84, tam=46),
    mg(L.ranking("LYON en 2026", [(EQ("LYON"), "LCS Lock-In", "1.º", "3-1 a Cloud9", "oro"),
                                  (EQ("LYON"), "LCS Primavera", "1.º", "3-0 a Team Liquid", "oro"),
                                  (EQ("LYON"), "MSI", "3.º", "Cayó 2-3 con Hanwha Life", "azul"),
                                  (EQ("LYON"), "LCS Verano", "2.º", "1-3 con Team Liquid", "azul")]),
       T0(g + "3"), W(g + "3", "Hasta"),
       [W(g + "3", "Lock"), W(g + "3", "primavera"), W(g + "3", "tercero"), W(g + "3", "subcampeon")], y=.5, nombre="ranking LYON"),
    tar(W(g + "3", "Hasta"), T1(g + "3") + .3, "De local en la Ciudad de México", "29-30 de agosto · 2-0 a Cloud9 y a Team Liquid",
        A, logo="LYON", x=.5, y=.8, tam=48),
    gran(W(g + "4", "Inspired") - .2, "Inspired", "Inspired", A, "LYON", "Jungla · capitán · Polonia",
         dur=T1(g + "4") - W(g + "4", "Inspired") + .4, x=.25, tam=540),
    tar(T0(g + "4"), W(g + "4", "Inspired"), "Una plantilla internacional", None, "oro", x=.5, y=.2, tam=60),
    tar(W(g + "4", "campeon"), W(g + "4", "2024"), "Campeón de Norteamérica", "Con Evil Geniuses y con FlyQuest", A, x=.7, y=.62,
        tam=48),
    vs(W(g + "4", "2024"), T1(g + "4") + .3, "FLY", "GEN", "FlyQuest 2 · Gen.G 3", "Cuartos del Mundial 2024", ganador=1,
       marca=W(g + "4", "cinco"), y=.42),
    peg(W(g + "5", "Saint"), "Saint", "Saint", A, "LYON", "Medio · MVP final de primavera", dur=W(g + "5", "Dhokla") - W(g + "5", "Saint"),
        x=.24, y=.48, tam=400),
    peg(W(g + "5", "Berserker"), "Berserker", "Berserker", A, "LYON", "Tirador · MVP del verano",
        dur=W(g + "5", "Dhokla") - W(g + "5", "Berserker"), x=.76, y=.48, tam=400),
    peg(W(g + "5", "Dhokla"), "Dhokla", "Dhokla", A, "LYON", "Top · EE. UU.", dur=T1(g + "5") - W(g + "5", "Dhokla") + .3, x=.2,
        y=.45, tam=340),
    peg(W(g + "5", "Isles"), "Isles", "Isles", A, "LYON", "Soporte · Australia", dur=T1(g + "5") - W(g + "5", "Isles") + .3, x=.5,
        y=.45, tam=340),
    tar(W(g + "5", "dirige"), T1(g + "5") + .3, "Reignover", "Entrenador · exjungla de Fnatic", A, logo="LYON", x=.78, y=.8,
        tam=44),
]
# ================================================================== LYON: CAMINO + JUGADORES
g = "lyon_camino_"
FX += [
    mg(L.resultados("LYON en el Mundial", [(EQ("LYON"), "LYON", EQ("TSW"), "Secret Whales", 0),
                                            (EQ("LYON"), "LYON", EQ("KC"), "Karmine Corp", 0),
                                            (EQ("GEN"), "Gen.G", EQ("LYON"), "LYON (1-2)", 0)]),
       T0(g + "0"), W(g + "1", "reacciono"), [T0(g + "0") + .2, W(g + "0", "Despues"), W(g + "1", "tercera")], y=.45,
       nombre="resultados LYON"),
    tar(W(g + "0", "primera"), W(g + "0", "Despues"), "1.ª victoria de Norteamérica", "En este Mundial", A, x=.5, y=.86, tam=46),
    tar(W(g + "1", "gano"), W(g + "1", "reacciono"), "Partida 1: LYON", "Le gana al n.º 1 de Corea", A, logo="LYON", x=.5, y=.86,
        tam=46),
    tar(W(g + "1", "reacciono"), T1(g + "1") + .2, "Gen.G gana 2-1", "Pero LYON tumbó a un gigante", "oro", x=.5, y=.5, tam=64),
    mg(L.ficha_jugador(JUG("Berserker"), "Berserker", EQ("LYON"), 1, [("Asesinatos", "25", 1.0), ("Con Ezreal ante TSW", "13/1/5", .52)],
                       A, sub="Tirador · el más letal"),
       T0(g + "2"), W(g + "2", "Saint"), [W(g + "2", "Veinticinco"), W(g + "2", "trece")], y=.5, nombre="ficha Berserker"),
    peg(W(g + "2", "Saint"), "Saint", "Saint", A, "LYON", "El mejor KDA de LYON · 6,57", dur=W(g + "2", "Isles") - W(g + "2", "Saint"),
        x=.25, y=.47, tam=430),
    peg(W(g + "2", "Isles"), "Isles", "Isles", A, "LYON", "En el 90 % de los asesinatos", dur=T1(g + "2") - W(g + "2", "Isles") + .3,
        x=.75, y=.47, tam=430),
    vs(T0(g + "3"), T1(g + "3") + .3, "LYON", "TSW", "La pelea que explica a LYON", "Ronda 1 · minuto 15", y=.42),
]

# ================================================================== JUGADA 3 · LYON vs TSW (j3: t=70 → 15:51)
f = "jugada3_"
e0, e1 = ESC("jugada3")
FX += [en_vivo(e0 + .3, "Transmisión oficial · LYON vs Secret Whales", "LYON"),
       tar(e0 + .3, e0 + 5.5, "Minuto 15", "Mira primero la pelea entera", "oro", x=.76, y=.17, tam=40)]
a, b = T0(f + "0"), W(f + "0", "Secret")
FX += [J(3, a, a + 1.2, 92, -75), rebobinar(a, a + 1.2, "14:00"), dict(tipo="destello", en=a + 1.2, fuerza=.4),
       CLIP(3, a + 1.2, b, 2, 2 + (b - a - 1.2)),
       tar(a + 1.4, b, "Dos minutos antes", "LYON persigue de más y pierde a tres", R, x=.5, y=.86, tam=44)]
FX += P(3, b, NX(f + "0"), 70, [
    anillo(.585, .045, 40, R, b + .2, "+600 DE ORO", "SECRET WHALES", lado="abajo"),
], "15:51")
b = W(f + "1", "Secret")
FX += P(3, T0(f + "1"), b, 70, [
    anillo(.38, .30, 66, Y, W(f + "1", "Heraldo"), "HERALDO", "LYON LO ESTÁ HACIENDO", lado="izq"),
], "15:51")
FX += MESA2("j3", b, NX(f + "1"), "15:51")
FX += [peg(W(f + "1", "Bie") - .2, "Bie", "Bie", R, "TSW", "Nautilus · listo para iniciar", dur=NX(f + "1") - W(f + "1", "Bie") + .2,
           x=.1, y=.62, tam=200)]
b = W(f + "2", "Todo")
FX += [CLIP(3, T0(f + "2"), b, 70, 74)]
FX += P(3, b, NX(f + "2"), 74, [
    dict(tipo="foco", en=b + .1, k=.42),
    anillo(.677, .35, 46, R, b + .2, "A OSCURAS", "NEARSIGHTED", lado="der"),
    anillo(.47, .43, 46, R, b + .35),
    anillo(.677, .65, 46, R, b + .5),
    anillo(.693, .77, 46, R, b + .65),
    anillo(.411, .37, 54, A, b + .8, "INSPIRED", "PARANOIA", lado="izq", icono="Nocturne"),
], "15:55", d3="j3_paranoia")
a = T0(f + "3")
FX += [CLIP(3, a, NX(f + "3"), 74, 79),
       peg(W(f + "3", "primero"), "Bie", "Bie", R, "TSW", "El primero en caer", dur=NX(f + "3") - W(f + "3", "primero"), x=.1, y=.62,
           tam=200, gris=True)]
b = W(f + "4", "Teletransporte")
FX += [CLIP(3, T0(f + "4"), b, 79, 84)]
FX += P(3, b, NX(f + "4"), 84, [
    flecha([(.12, .99), (.22, .86), (.33, .70)], R, b + .1, "TELETRANSPORTE", off=(-150, 10)),
    anillo(.344, .67, 56, R, b + .5, "PUN", "RUMBLE · LA ÚLTIMA CARTA", lado="der", icono="Rumble"),
    anillo(.328, .59, 50, A, b + .9, "BERSERKER", None, lado="izq", icono="Ezreal"),
], "16:05")
a = T0(f + "5")
FX += [CLIP(3, a, NX(f + "5"), 84, 100), x2(a, NX(f + "5"), "▶▶ ACELERADO"),
       dict(tipo="destello", en=W(f + "5", "Cuatro"), fuerza=.55),
       tar(W(f + "5", "Cuatro"), NX(f + "5"), "4 por 0", "Para LYON", A, logo="LYON", dato="4-0", x=.5, y=.86, tam=46)]
a = T0(f + "6")
FX += [CLIP(3, a, e1, 126, 126 + (e1 - a) * .8), tar(a, a + 2.5, "Repetición", None, R, x=.1, y=.14, tam=30),
       tar(W(f + "6", "marca"), W(f + "6", "Gen"), "La marca de LYON", "Se equivoca, se reagrupa y vuelve", "oro", x=.5, y=.18, tam=54),
       vs(W(f + "6", "Gen"), e1 + .2, "LYON", "GEN", "La partida 1 contra Gen.G", "Ronda 3 · minuto 34", y=.42)]

# ================================================================== JUGADA 4 · LYON vs Gen.G partida 1 (j4: t=104 → 34:03)
f = "jugada4_"
e0, e1 = ESC("jugada4")
FX += [en_vivo(e0 + .3, "Transmisión oficial · LYON vs Gen.G · partida 1", "LYON"),
       tar(e0 + .3, e0 + 5.5, "Minuto 34", "Mira primero la pelea entera", "oro", x=.76, y=.17, tam=40)]
a = T0(f + "0")
FX += [J(4, a, a + 1.2, 160, -46), rebobinar(a, a + 1.2, "34:03"), dict(tipo="destello", en=a + 1.2, fuerza=.4)]
FX += P(4, a + 1.2, NX(f + "0"), 104, [
    anillo(.415, .075, 40, A, W(f + "0", "tres"), "+3.000 DE ORO", "LYON", lado="abajo"),
    texto("LYON · 3 DRAGONES", "EL PRÓXIMO LE DA EL ALMA", .5, .8, W(f + "0", "dragones"), color=A),
], "34:03")
b = T0(f + "1")
FX += P(4, b, NX(f + "1"), 104, [dict(tipo="foco", en=b + .1, k=.45)], "34:03")
for i, (j, x) in enumerate((("Berserker", .08), ("Dhokla", .19), ("Saint", .30))):
    e = W(f + "1", "Berserker") + .25 * i
    FX.append(peg(e, j, None, dur=NX(f + "1") - e, x=x, y=.62, tam=190, gris=True))
for i, (j, x) in enumerate((("Chovy", .81), ("Ruler", .92))):
    e = W(f + "1", "Chovy") + .25 * i
    FX.append(peg(e, j, None, dur=NX(f + "1") - e, x=x, y=.62, tam=190, gris=True))
FX += [tar(W(f + "1", "Berserker"), NX(f + "1"), "Berserker · Dhokla · Saint", "LYON · sin Destello", A, logo="LYON", x=.2, y=.84, tam=34),
       tar(W(f + "1", "Chovy"), NX(f + "1"), "Chovy · Ruler", "Gen.G · sin Destello", R, logo="GEN", x=.86, y=.84, tam=34)]
FX += [tar(W(f + "1", "Destello"), NX(f + "1"), "Destello", "El hechizo para escapar o entrar", "oro", icono="SummonerFlash", x=.5,
           y=.2, tam=44)]
a = T0(f + "2")
FX += [CLIP(4, a, NX(f + "2"), 112, 124), tar(a + .3, NX(f + "2"), "Saint · Ahri", "Entra, conecta… y sale", A, icono="Ahri",
                                               x=.16, y=.14, tam=36)]
b = W(f + "3", "posiciones")
FX += [CLIP(4, T0(f + "3"), b, 124, 138)]
FX += P(4, b, NX(f + "3"), 138, [
    dict(tipo="zona", pts=[(.33, .16), (.53, .16), (.53, .42), (.33, .42)], color=R, en=W(f + "3", "Gen"), alfa=.16),
    texto("GEN.G", "LOS CINCO, SOBRE EL DRAGÓN", .43, .1, W(f + "3", "Gen"), color=R),
    anillo(.396, .60, 50, A, W(f + "3", "LYON"), "LYON", "ENFRENTE", lado="izq"),
    anillo(.604, .59, 44, A, W(f + "3", "LYON") + .2),
    anillo(.635, .74, 44, A, W(f + "3", "LYON") + .4),
    anillo(.068, .43, 54, A, W(f + "3", "Dhokla"), "DHOKLA", "OLAF · EN UN ARBUSTO", lado="der", icono="Olaf"),
], "34:37")
FX += MESA2("j4", T0(f + "4"), NX(f + "4"), "34:37")
FX += [tar(T0(f + "4") + .3, NX(f + "4"), "Castigo 50/50", "Inspired contra Canyon", Y, icono="SummonerSmite", x=.5, y=.88, tam=40)]
b = W(f + "5", "definitiva")
FX += [J(4, T0(f + "5"), b, 138, (145 - 138) / (b - T0(f + "5"))),
       tar(T0(f + "5") + .2, b, "Destello + Xin Zhao", "Al centro de los cinco", A, icono="XinZhao", x=.16, y=.14, tam=36)]
FX += P(4, b, NX(f + "5"), 145, [
    dict(tipo="foco", en=b + .1, k=.38),
    anillo(.36, .54, 78, A, b + .2, "INSPIRED", "GUARDIA CRECIENTE", lado="der", icono="XinZhao"),
    flecha([(.36, .54), (.31, .40), (.27, .27)], A, W(f + "5", "empuja"), None, dur=.4),
    flecha([(.36, .54), (.41, .48), (.44, .42)], A, W(f + "5", "empuja") + .15, None, dur=.4),
    flecha([(.36, .54), (.29, .52), (.23, .48)], A, W(f + "5", "empuja") + .3, None, dur=.4),
    anillo(.198, .57, 50, A, W(f + "5", "intocable"), "DHOKLA", "INMUNE AL CONTROL", lado="izq", icono="Olaf"),
], "34:44", d3="j4_guardia")
a = T0(f + "6")
FX += [CLIP(4, a, NX(f + "6"), 145, 157), dict(tipo="destello", en=W(f + "6", "Chovy"), fuerza=.6),
       peg(W(f + "6", "Chovy"), "Chovy", "Chovy", R, "GEN", "Cae", dur=NX(f + "6") - W(f + "6", "Chovy"), x=.1, y=.62, tam=200, gris=True),
       tar(W(f + "6", "gana"), NX(f + "6"), "LYON gana la pelea", None, A, logo="LYON", x=.5, y=.86, tam=46)]
a = T0(f + "7")
FX += [CLIP(4, a, NX(f + "7"), 182, 206), x2(a, NX(f + "7"), "▶▶ ACELERADO"),
       tar(W(f + "7", "partida"), NX(f + "7"), "LYON gana la partida 1", "Al primer sembrado de Corea", A, logo="LYON", x=.5, y=.86,
           tam=48),
       tar(W(f + "7", "imposible") - .8, NX(f + "7"), "«Se suponía que era imposible»", "El narrador oficial", "oro", x=.5, y=.18,
           tam=46)]
a = T0(f + "8")
FX += [CLIP(4, a, e1, 206, 206 + (e1 - a)),
       tar(a, e1, "La amenaza de LYON", "Paciencia, posición… y un jungla que sabe cuándo entrar", "oro", x=.5, y=.18, tam=50)]

# ================================================================== CLAVES DEL DUELO
g = "claves_"
FX += [
    tar(T0(g + "0"), T1(g + "0") + .3, "3 claves para hoy", "Para verlo como un experto", "oro", x=.5, y=.45, tam=80),
    tar(T0(g + "1"), T1(g + "1") + .2, "1 · La jungla", "Wei contra Inspired", "oro", x=.5, y=.17, tam=60),
    gran(W(g + "1", "Wei") - .2, "Wei", "Wei", R, "IG", "Casi no muere", dur=T1(g + "1") - W(g + "1", "Wei") + .4, x=.25, tam=500),
    gran(W(g + "1", "Inspired") - .2, "Inspired", "Inspired", A, "LYON", "Da las órdenes", dur=T1(g + "1") - W(g + "1", "Inspired") + .4,
         x=.75, tam=500),
    tar(T0(g + "2"), T1(g + "2") + .2, "2 · El medio", "Rookie contra Saint", "oro", x=.5, y=.17, tam=60),
    gran(W(g + "2", "Rookie") - .2, "Rookie", "Rookie", R, "IG", "Campeón del mundo", dur=T1(g + "2") - W(g + "2", "Rookie") + .4,
         x=.25, tam=500),
    gran(W(g + "2", "Saint") - .2, "Saint", "Saint", A, "LYON", "El más fino de LYON", dur=T1(g + "2") - W(g + "2", "Saint") + .4,
         x=.75, tam=500),
    tar(T0(g + "3"), W(g + "3", "elige"), "3 · Experiencia contra hambre", "3 títulos mundiales contra 0", "oro", x=.5, y=.17, tam=58),
    peg(W(g + "3", "IG"), "TheShy", None, dur=W(g + "3", "elige") - W(g + "3", "IG"), x=.15, y=.55, tam=260),
    peg(W(g + "3", "IG") + .2, "Rookie", None, dur=W(g + "3", "elige") - W(g + "3", "IG") - .2, x=.32, y=.55, tam=260),
    peg(W(g + "3", "IG") + .4, "Meiko", None, dur=W(g + "3", "elige") - W(g + "3", "IG") - .4, x=.49, y=.55, tam=260),
    peg(W(g + "3", "ninguno"), EQ("LYON"), "LYON", A, sub="0 títulos", dur=W(g + "3", "elige") - W(g + "3", "ninguno"), x=.78,
        y=.55, tam=300),
    tar(W(g + "3", "elige"), T1(g + "3") + .2, "Primera selección: LYON", "En la partida 1", A, logo="LYON", x=.5, y=.5, tam=64),
    vs(T0(g + "4"), T1(g + "4") + .3, "IG", "LYON", "Primer enfrentamiento oficial", "Hasta donde hay registro", y=.42),
]
# ================================================================== CIERRE: HORARIOS
g = "cierre_"
FX += [
    mg(L.calendario("Miércoles 28 de octubre · hora del centro de México", [("14:00", "T1 vs\nMovistar KOI", "rojo"),
                                                                             ("17:00", "IG vs LYON", "amarillo")]),
       T0(g + "0"), W(g + "0", "juegan"), [W(g + "0", "dos"), W(g + "0", "dos") + .8], y=.45, nombre="horarios"),
    vs(W(g + "0", "juegan"), T1(g + "0") + .2, "T1", "MKOI", "14:00 · T1 vs Movistar KOI", "También se juegan el pase", y=.4),
    peg(W(g + "0", "tricampeon"), "Faker", "Faker", R, "T1", "Tricampeón del mundo", dur=T1(g + "0") - W(g + "0", "tricampeon") + .2,
        x=.15, y=.55, tam=300),
    vs(T0(g + "1"), T1(g + "1") + .3, "IG", "LYON", "17:00 · IG vs LYON", "O en cuanto termine T1-KOI", y=.42),
    peg(T0(g + "2"), EQ("IG"), "¿La experiencia?", R, dur=W(g + "2", "comentarios") - T0(g + "2"), x=.27, y=.47, tam=380),
    peg(W(g + "2", "sueno") - .3, EQ("LYON"), "¿El sueño?", A, dur=W(g + "2", "comentarios") - W(g + "2", "sueno") + .3, x=.73,
        y=.47, tam=380),
    tar(W(g + "2", "comentarios"), W(g + "2", "Nos"), "¿Con quién vas?", "Déjalo en los comentarios", "oro", x=.5, y=.45, tam=76),
    mg(L.apertura("¡NOS VEMOS!", "IG vs LYON · miércoles 28 de octubre"), W(g + "2", "Nos"), _TL["total"], x=.5, y=.5,
       nombre="cierre"),
]

# mesas 3D: sus tiempos para mesas_3d.py
with open(os.path.join(_D, "tiempos_mesas.py"), "w", encoding="utf-8") as _f:
    _f.write("# lo escribe efectos.py: (de, a) de cada mesa 3D en el video\nTIEMPOS = " + repr(TIEMPOS_MESAS) + "\n")

ROTULOS = []
SFX = {}
_entra = sorted({e.get("de", 0) for e in FX if e.get("tipo") == "mg" and not e.get("nombre", "").startswith(("pizarra", "rebobinar", "3D"))})
_rebob = [d["de"] for d in FX if d.get("nombre") == "rebobinar"]
_pausas = sorted({d["de"] for d in FX if d.get("tipo") == "video" and d.get("vel") == 0})
_golpes = [d["en"] for d in FX if d.get("tipo") == "destello"]
_dibujo = sorted({e["en"] for d in FX if d.get("nombre", "").startswith("pizarra") for e in getattr(d["fn"], "_els", [])})
_mesas = [v[0] for v in TIEMPOS_MESAS.values()]
PISTAS = ([dict(sfx="whoosh", en=0.1, vol=.6), dict(sfx="golpe", en=0.3, vol=.7)]
          + [dict(sfx="whoosh2", en=t, vol=.22) for t in _entra]
          + [dict(sfx="rebobina", en=t, vol=.5) for t in _rebob]
          + [dict(sfx="clic", en=t, vol=.5) for t in _pausas] + [dict(sfx="golpe", en=t + .02, vol=.28) for t in _pausas]
          + [dict(sfx="golpe", en=t, vol=.55) for t in _golpes]
          + [dict(sfx="pop", en=t, vol=.26) for t in _dibujo]
          + [dict(sfx="whoosh", en=t, vol=.4) for t in _mesas])
