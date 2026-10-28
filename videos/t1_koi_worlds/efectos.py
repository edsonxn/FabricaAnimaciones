# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «T1 vs KOI» (estilo análisis táctico, docs/estilo_analisis_tactico.md), con los helpers de
videos/cfo_kc_worlds/efectos.py. Fuentes de jugada por partida: medios/_fuente/g<p>_j<k>.mp4 (n = "g1_j1"…).
T1 = AZUL (lado azul en las dos partidas), KOI = ROJO. Tiempos anclados a la voz (T0/T1/W/NX sobre timeline.json).
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
    return os.path.join(_D, "medios", "_fuente", f"{n}.mp4")


def J(n, de, a, desde, vel=1.0, **kw):
    """El tramo de la jugada `n` a cuadro entero desde el segundo `desde`, a velocidad `vel` (0 = congelado).
    kw: zoom=(z, cx, cy), zoom0, zoom_en, zoom_dur (acercamiento animado del FX `video`, 27-oct-2026)."""
    return dict(tipo="video", de=de, a=a, ruta=fuente(n), desde=desde, vel=vel, nombre=f"{n} {desde:.1f} x{vel:g}", **kw)


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


def x2(de, a, texto="» x2"):
    return tar(de, a, texto, None, "oro", x=.09, y=.13, tam=28)



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



# ───────────────────────────────────────── extras de este video (28-oct-2026) ─────────────────────────────────────────────
import rastros_vod as RV  # noqa: E402

_CAMS = {}


def RUTA(n, t_ref, puntos):
    """la RUTA que hizo un jugador, llevada al cuadro congelado t_ref: puntos [(t, x, y)] = sus PIES medidos en cuadros
    anteriores (fracción). La cámara se compensa con investigacion/cam_j<n>.json (rastros_vod.camara_clip)."""
    if n not in _CAMS:
        _CAMS[n] = _json.load(open(os.path.join(_D, "investigacion", f"cam_{n}.json")))
    return RV.ruta_en(_CAMS[n], t_ref, puntos)


def ruta(n, t_ref, puntos, color, en, etiqueta=None, off=(0, -50), dur=1.0):
    """flecha CONTINUA de la ruta hecha (de dónde vino) hasta su posición en el cuadro congelado"""
    pts = RUTA(n, t_ref, puntos)
    if len(pts) < 2:
        print(f"  AVISO ruta {n}@{t_ref}: {puntos} cruza un corte de cámara → sin flecha")
        return None
    return flecha(pts, color, en, etiqueta, off=off, dur=dur)


def intencion(pts, color, en, etiqueta=None, off=(0, -50), dur=.7):
    """flecha DISCONTINUA: a dónde quiere ir (su intención)"""
    return flecha(pts, color, en, etiqueta, off=off, guion=True, dur=dur)


def P2(n, de, a, t, els, reloj, d3=None):
    return P(n, de, a, t, [e for e in els if e], reloj, d3)


def duelo(de, a, ja, jb, titulo, filas, marcas):
    """cara a cara por posición (mg_lol.duelo): ja/jb = (jugador, equipo, sub)"""
    (na, ea, sa), (nb, eb, sb) = ja, jb
    col = {"T1": A, "MKOI": R}
    return mg(L.duelo((JUG(na), na, EQ(ea), col[ea], sa), (JUG(nb), nb, EQ(eb), col[eb], sb), titulo, filas), de, a, marcas,
              y=.5, nombre=f"duelo {na}-{nb}")


def repeticion(de, a, sub="Cámara lenta"):
    return [tar(de, a, "Repetición", sub, R, x=.12, y=.13, tam=34), dict(tipo="destello", en=de, fuerza=.35)]



def CARGA(c):
    return os.path.join(_D, "splash", c + "_carga.jpg")


def draft(k, eq, color, picks):
    """los 5 picks de un equipo, cada uno al nombrarlo la voz: arte de carga del campeón + placa con el jugador"""
    out = []
    for i, (jug, camp, pal) in enumerate(picks):
        e = W(k, pal)
        out.append(peg(e, CARGA(camp), jug, color, eq, camp.replace("LeeSin", "Lee Sin").replace("JarvanIV", "Jarvan IV")
                       .replace("Kaisa", "Kai'Sa").replace("XinZhao", "Xin Zhao"), dur=T1(k) - e + .35,
                       x=.1 + .2 * i, y=.5, tam=330))
    return out


FX = []
# ================================================================== LO QUE ESTABA EN JUEGO
g = "juego_"
FX += [
    tar(T0(g + "0"), W(g + "0", "fase"), "Lo que estaba en juego", None, "oro", x=.5, y=.2, tam=74),
    mg(L.suiza("Fase suiza · Worlds 2026"), W(g + "0", "fase"), T1(g + "0") + .3,
       [W(g + "0", "fase"), W(g + "0", "fase") + .6, W(g + "0", "tres"), W(g + "0", "cuartos"), W(g + "0", "derrotas"),
        T1(g + "0")], y=.46, nombre="suiza"),
    mg(L.resultados("Sus derrotas: el mismo rival", [(EQ("DK"), "Dplus KIA", EQ("T1"), "T1", 0),
                                                      (EQ("DK"), "Dplus KIA", EQ("MKOI"), "Movistar KOI", 0)]),
       T0(g + "1"), W(g + "1", "ganara"), [W(g + "1", "derrotas"), W(g + "1", "Dplus")], y=.45, nombre="resultados DK"),
    mg(L.tabla("Antes de hoy", [("2-1", "oro", [(EQ("T1"), "T1"), (EQ("MKOI"), "Movistar KOI")])]),
       W(g + "1", "ganara"), T1(g + "1") + .3, [W(g + "1", "ganara")], y=.5, nombre="tabla 2-1"),
    tar(W(g + "1", "cuartos"), T1(g + "1") + .3, "El que gane: 3-1", "A cuartos de final", A, x=.5, y=.84, tam=56),
    tar(T0(g + "2"), W(g + "2", "Fearless"), "Al mejor de 3", "Gana quien llegue a dos", "oro", x=.5, y=.2, tam=66),
    tar(W(g + "2", "Fearless"), T1(g + "2") + .3, "Fearless Draft", "En la serie, ningún campeón se repite", "oro", x=.5, y=.17,
        tam=66),
]
# ================================================================== DRAFTS
FX += [tar(T0("draft1_0"), W("draft1_0", "Doran"), "Partida 1", "T1 · lado azul", A, logo="T1", x=.5, y=.2, tam=70)]
FX += draft("draft1_0", "T1", A, [("Doran", "Ambessa", "Doran"), ("Oner", "LeeSin", "Oner"), ("Faker", "Syndra", "Faker"),
                                  ("Peyz", "Xayah", "Peyz"), ("Keria", "Nautilus", "Keria")])
FX += [tar(T0("draft1_1"), W("draft1_1", "Myrwn"), "Movistar KOI", "Lado rojo", R, logo="MKOI", x=.5, y=.2, tam=70)]
FX += draft("draft1_1", "MKOI", R, [("Myrwn", "Gnar", "Myrwn"), ("Elyoya", "Qiyana", "Elyoya"), ("Jojopyun", "Akali", "Jojopyun"),
                                    ("Supa", "Kaisa", "Supa"), ("Alvaro", "Alistar", "Alvaro")])
FX += [tar(T0("draft2_0"), T1("draft2_0") + .3, "Partida 2", "Fearless: 10 campeones menos", "oro", x=.5, y=.2, tam=70),
       peg(W("draft2_0", "diez") - .2, CARGA("Syndra"), "Syndra", "oro", sub="Ya usado", dur=T1("draft2_0") - W("draft2_0", "diez") + .5,
           x=.3, y=.55, tam=300, gris=True, sello=("YA USADO", 0)),
       peg(W("draft2_0", "diez"), CARGA("Akali"), "Akali", "oro", sub="Ya usado", dur=T1("draft2_0") - W("draft2_0", "diez") + .3,
           x=.7, y=.55, tam=300, gris=True, sello=("YA USADO", 0))]
FX += draft("draft2_1", "T1", A, [("Doran", "Gwen", "Doran"), ("Oner", "JarvanIV", "Oner"), ("Faker", "Orianna", "Faker"),
                                  ("Peyz", "Jhin", "Peyz"), ("Keria", "Karma", "Keria")])
FX += draft("draft2_2", "MKOI", R, [("Myrwn", "Ornn", "Myrwn"), ("Elyoya", "XinZhao", "Elyoya"), ("Jojopyun", "Viktor", "Jojopyun"),
                                    ("Supa", "Ezreal", "Supa"), ("Alvaro", "Seraphine", "Alvaro")])
# ================================================================== LOS NÚMEROS
g = "numeros_"
FX += [
    tar(T0(g + "0"), W(g + "0", "Doran"), "Los números de la serie", None, "oro", x=.5, y=.2, tam=74),
    mg(L.ficha_jugador(JUG("Doran"), "Doran", EQ("T1"), 1, [("Asesinatos", "10", .77), ("Asistencias", "13", 1.0),
                                                            ("Muertes", "0", .02)], color="oro", sub="Top · T1"),
       W(g + "0", "Doran"), T1(g + "0") + .3, [W(g + "0", "diez"), W(g + "0", "trece"), W(g + "0", "cero")], y=.5,
       nombre="ficha Doran"),
    peg(T0(g + "1"), "Keria", "Keria", A, "T1", "30 asistencias", dur=W(g + "1", "Peyz") - T0(g + "1"), x=.3, y=.5, tam=420),
    peg(W(g + "1", "Peyz"), "Peyz", "Peyz", A, "T1", "Jhin · 8/1/5", dur=T1(g + "1") - W(g + "1", "Peyz") + .3, x=.7, y=.5, tam=420),
    mg(L.ranking("Partida 2 · marcador final", [(EQ("T1"), "T1", "22", "asesinatos · 9 torres · 3 dragones", "azul"),
                                                 (EQ("MKOI"), "Movistar KOI", "9", "asesinatos · 0 torres · 0 dragones", "rojo")]),
       T0(g + "2"), T1(g + "2") + .3, [T0(g + "2") + .1, W(g + "2", "KOI")], y=.45, nombre="ranking final g2"),
    tar(W(g + "2", "doce"), T1(g + "2") + .3, "+12 300 de oro", "Para T1 al final", A, logo="T1", dato="57,5K", x=.5, y=.84, tam=52),
]
# ================================================================== QUÉ SIGUE
g = "sigue_"
FX += [
    mg(L.tabla("Tras la ronda 4", [("3-1 · a cuartos", "azul", [(EQ("T1"), "T1")]), ("2-2 · a muerte", "rojo", [(EQ("MKOI"), "Movistar KOI")])]),
       T0(g + "0"), T1(g + "0") + .3, [T0(g + "0") + .1, W(g + "0", "cuartos")], y=.48, nombre="tabla tras r4"),
    mg(L.calendario("Lo que viene", [("31 oct", "Ronda 5\nKOI, a muerte", "rojo"), ("3-6 nov", "Cuartos\nal mejor de 5", "azul"),
                                     ("7-8 nov", "Semifinales", "oro"), ("14 nov", "Final\nNueva York", "amarillo")]),
       T0(g + "1"), T1(g + "2") + .3, [T0(g + "1") + .1, W(g + "1", "cuarto"), T0(g + "2"), W(g + "2", "sabado")], y=.5,
       nombre="calendario"),
    peg(W(g + "1", "cuarto"), "Faker", "Faker", A, "T1", "Por su 4.º Mundial seguido", dur=T1(g + "1") - W(g + "1", "cuarto") + .3,
        x=.18, y=.42, tam=300),
]
# ================================================================== CIERRE
g = "cierre_"
FX += [
    vs(T0(g + "0"), T1(g + "0") + .4, "T1", "MKOI", "T1 2 · KOI 0", "Worlds 2026 · ronda 4", ganador=0, y=.45),
    tar(W(g + "0", "comentarios"), T1(g + "0") + .4, "¿Cuál fue la mejor jugada?", "Déjalo en los comentarios", "oro", x=.5, y=.85,
        tam=54),
]

# ───────────────────────────────────────── relojes del HUD por fuente (datos_g1.md / datos_g2.md: HUD = t + K) ───────────
K = {"g1_j1": 274, "g1_j2": 439, "g1_j3": 1254, "g1_j4": 1970, "g1_j5": 2294, "g2_j1": 474.9, "g2_j2": 1109.9, "g2_j3": 1444.9}


def H(n, t):
    s = int(round(t + K[n]))
    return f"{s // 60:02d}:{s % 60:02d}"


def PZ(n, de, a, t, els, d3=None):
    """pausa con el reloj del HUD de ese cuadro"""
    return P2(n, de, a, t, els, H(n, t), d3)


def REB(n, de, t_desde, t_hasta, dur=1.2):
    """REBOBINANDO rotulado: el clip va hacia atrás de t_desde a t_hasta en `dur` s"""
    return [J(n, de, de + dur, t_desde, -(t_desde - t_hasta) / dur), rebobinar(de, de + dur, H(n, t_hasta)),
            dict(tipo="destello", en=de + dur, fuerza=.4)]


def VIVO(sid, n, t, sub, logo, minuto):
    """tramo EN VIVO (beat sin voz con la narración original): de e0 a la primera frase, desde el segundo t de la fuente"""
    e0, _ = ESC(sid)
    f0 = T0(sid + "_0")
    return [J(n, e0, f0, t), en_vivo(e0 + .3, sub, logo),
            tar(e0 + .3, e0 + 5.5, minuto, "Mírala primero en vivo", "oro", x=.76, y=.17, tam=40)]


def LENTA(n, de, a, t_fin, vel=.45, zoom=None, sub="Cámara lenta"):
    """repetición en cámara lenta que TERMINA en el cuadro t_fin"""
    kw = dict(zoom=zoom, zoom0=(1.0, .5, .5), zoom_dur=1.2) if zoom else {}
    return [J(n, de, a, t_fin - vel * (a - de), vel, **kw), *repeticion(de, de + 3.5, sub)]


def gris(en, jug, eq, sub, x, a=None, y=.62, tam=190):
    col = A if eq == "T1" else R
    return peg(en, jug, jug, col, eq, sub, dur=(a or en + 3.0) - en, x=x, y=y, tam=tam, gris=True)


def acel(de, a, texto="» ACELERADO"):
    return x2(de, a, texto)


# ================================================================== GANCHO (sin spoiler: el 28-oct el usuario lo pidió)
g = "gancho_"
FX += [
    mg(L.apertura("T1 vs KOI", "Worlds 2026 · ronda 4 · un boleto a cuartos"), 0.0, W(g + "0", "Movistar"), x=.5, y=.5,
       nombre="apertura"),
    dict(tipo="destello", en=0.15, fuerza=.7),
    vs(W(g + "0", "Movistar"), T1(g + "0") + .2, "T1", "MKOI", "Al mejor de 3", "28 de octubre · fase suiza", y=.42),
    tar(W(g + "0", "boleto"), T1(g + "0") + .2, "El que gane, a cuartos", None, "oro", x=.5, y=.84, tam=50),
    tar(W(g + "1", "arranque"), W(g + "1", "dragon"), "Un arranque que nadie esperaba", None, R, logo="MKOI", x=.5, y=.8, tam=50),
    tar(W(g + "1", "dragon"), W(g + "1", "pelea"), "Un dragón robado", "En el peor momento", R, x=.5, y=.8, tam=50),
    tar(W(g + "1", "pelea"), T1(g + "1") + .2, "Una pelea que lo decidió todo", None, "oro", x=.5, y=.8, tam=50),
    mg(L.menu([(ART("Ambessa"), "Las jugadas", "rojo"), (JUG("Faker"), "Pausa por pausa", "azul"),
               (ART("Gnar"), "Dónde estaba cada uno", "amarillo"), (EQ("T1"), "Por qué salió así", "oro")]),
       T0(g + "2"), T1(g + "2") + .3,
       [W(g + "2", "jugadas"), W(g + "2", "pausa"), W(g + "2", "donde"), W(g + "2", "salio")], y=.5, nombre="menu"),
]
# ================================================================== CÓMO LLEGARON
g = "camino_"
FX += [
    peg(T0(g + "0"), "Faker", "Faker", A, "T1", "Campeón 2023 · 2024 · 2025", dur=W(g + "0", "Debuto") - T0(g + "0"), x=.24, y=.47,
        tam=430),
    tar(W(g + "0", "cuarto"), W(g + "0", "Debuto"), "¿El 4.º seguido?", "Nadie lo ha hecho", "oro", logo="T1", x=.68, y=.6, tam=54),
    tar(W(g + "0", "Debuto"), T1(g + "0") + .2, "Ronda 1: T1 gana", "A Los Grandes · 24 minutos", A, logo="T1", x=.5, y=.8, tam=54),
    mg(L.resultados("T1 en el Mundial", [(EQ("DK"), "Dplus KIA", EQ("T1"), "T1", 0), (EQ("T1"), "T1", EQ("CFO"), "CFO", 0)]),
       T0(g + "1"), T1(g + "1") + .3, [T0(g + "1") + .2, W(g + "1", "recupero")], y=.45, nombre="resultados T1"),
    tar(T0(g + "2"), W(g + "2", "arranco"), "Movistar KOI", "El equipo de Ibai y Piqué", R, logo="MKOI", x=.5, y=.2, tam=62),
    mg(L.resultados("KOI en el Mundial", [(EQ("MKOI"), "Movistar KOI", EQ("BLG"), "Bilibili Gaming", 0),
                                          (EQ("MKOI"), "Movistar KOI", EQ("CFO"), "CFO", 0)]),
       W(g + "2", "arranco"), T1(g + "2") + .3, [W(g + "2", "Bilibili"), W(g + "2", "despues")], y=.5, nombre="resultados KOI"),
    mg(L.resultados("Ronda 3", [(EQ("DK"), "Dplus KIA", EQ("MKOI"), "Movistar KOI", 0)]),
       T0(g + "3"), T1(g + "3") + .3, [T0(g + "3") + .3], y=.42, nombre="resultados DK-KOI"),
    tar(W(g + "3", "pentakill"), T1(g + "3") + .3, "Pentakill de Smash", "DK 2 · KOI 0", R, logo="DK", x=.5, y=.82, tam=50),
]

# ================================================================== JUGADA 1 · el arranque de KOI (g1_j1 + g1_j2)
f = "jugada1_"
e0, e1 = ESC("jugada1")
FX += VIVO("jugada1", "g1_j2", 48, "Transmisión oficial · KOI vs T1 · partida 1", "MKOI", "Minuto 8")
a = T0(f + "0")
FX += REB("g1_j2", a, 65.2, 50)
FX += [CLIP("g1_j1", a + 1.2, NX(f + "0"), 40, 65), acel(a + 1.2, NX(f + "0")),
       tar(W(f + "0", "Destello"), NX(f + "0"), "Faker, sin Destello", "Se lo quemó Jojopyun", A, icono="SummonerFlash", x=.24,
           y=.17, tam=40)]
b = T0(f + "1")
FX += PZ("g1_j1", b, NX(f + "1"), 65, [
    dict(tipo="foco", en=b + .2, k=.42),
    anillo(.44, .49, 52, A, W(f + "1", "Faker"), "FAKER", "SIN DESTELLO", lado="der", icono="Syndra"),
    anillo(.31, .43, 44, R, W(f + "1", "Faker") + .3, "JOJOPYUN", "AKALI", lado="izq", icono="Akali"),
    anillo(.565, .71, 48, R, W(f + "1", "Alvaro"), "ALVARO", "VIENE DE LA JUNGLA", lado="der", icono="Alistar"),
    intencion([(.565, .69), (.52, .60), (.465, .52)], R, W(f + "1", "jungla"), None),
    texto("NADIE EN T1 LO VE", None, .74, .32, W(f + "1", "Nadie"), color=Y),
])
a = T0(f + "2")
FX += [CLIP("g1_j1", a, NX(f + "2"), 65, 73),
       tar(W(f + "2", "sangre"), NX(f + "2"), "Primera sangre", "Jojopyun sobre Faker · 05:44", R, logo="MKOI", x=.5, y=.84, tam=48),
       gris(W(f + "2", "Faker"), "Faker", "T1", "Cae primero", .1, NX(f + "2")),
       dict(tipo="destello", en=W(f + "2", "sangre"), fuerza=.5)]
a = T0(f + "3")
FX += [CLIP("g1_j2", a, W(f + "3", "Pausa"), 40, 54), acel(a, W(f + "3", "Pausa"))]
b = W(f + "3", "Pausa")
FX += PZ("g1_j2", b, NX(f + "3"), 54, [
    intencion([(.46, .76), (.42, .71), (.385, .67)], R, W(f + "3", "Elyoya"), "ELYOYA · QIYANA", off=(150, 0)),
    anillo(.365, .65, 46, A, W(f + "3", "jungla"), "ONER", None, lado="izq", icono="LeeSin"),
    anillo(.32, .53, 40, A, W(f + "3", "jungla") + .2, "KERIA", None, lado="izq", icono="Nautilus"),
    anillo(.595, .53, 42, R, W(f + "3", "jungla") + .4, "SUPA", None, lado="der", icono="Kaisa"),
    anillo(.57, .72, 42, R, W(f + "3", "jungla") + .6, "ALVARO", None, lado="der", icono="Alistar"),
    texto("JUNGLA DE T1", "NI UNA GUARDIA", .16, .3, W(f + "3", "guardia"), color=Y),
])
a = T0(f + "4")
FX += [CLIP("g1_j2", a, NX(f + "4"), 54, 66),
       gris(W(f + "4", "Oner"), "Oner", "T1", "Lo derriten", .1, NX(f + "4")),
       gris(W(f + "4", "Peyz"), "Peyz", "T1", "Seis segundos después", .26, NX(f + "4")),
       dict(tipo="destello", en=W(f + "4", "Oner"), fuerza=.45),
       tar(W(f + "4", "Tres"), NX(f + "4"), "3-0 para KOI", "+1 700 de oro", R, logo="MKOI", dato="3-0", x=.7, y=.84, tam=48)]
a = T0(f + "5")
FX += [J("g1_j2", a, e1, 66),
       tar(a + .1, e1, "El plan de KOI", "Castigar el mapa sin visión", R, logo="MKOI", x=.5, y=.2, tam=56)]

# ================================================================== JUGADA 2 · la pelea de T1 (g1_j3, HUD = t + 1254)
f = "jugada2_"
e0, e1 = ESC("jugada2")
FX += VIVO("jugada2", "g1_j3", 42, "Transmisión oficial · partida 1", "T1", "Minuto 21")
a = T0(f + "0")
FX += REB("g1_j3", a, 62.25, 30)
FX += [CLIP("g1_j3", a + 1.2, NX(f + "0"), 30, 43),
       tar(W(f + "0", "siete"), NX(f + "0"), "7-6 en asesinatos", "Pero KOI +0,2K de oro", "oro", x=.5, y=.84, tam=46)]
b = T0(f + "1")
FX += PZ("g1_j3", b, NX(f + "2"), 43, [
    dict(tipo="foco", en=b + .2, k=.4),
    anillo(.455, .47, 52, A, W(f + "1", "Doran"), "DORAN", "AMBESSA", lado="izq", icono="Ambessa"),
    anillo(.51, .23, 40, R, W(f + "1", "Alvaro"), "ALVARO", "SOPORTE DE KOI", lado="der", icono="Alistar"),
    intencion([(.455, .45), (.48, .34), (.505, .26)], A, W(f + "1", "lanza"), "ENTRA", off=(-110, 0)),
    anillo(.46, .55, 36, A, W(f + "2", "equipo"), "FAKER", None, lado="izq", icono="Syndra"),
    anillo(.565, .66, 36, A, W(f + "2", "equipo") + .2, "KERIA", None, lado="der", icono="Nautilus"),
    anillo(.575, .74, 36, A, W(f + "2", "equipo") + .4, "PEYZ", None, lado="der", icono="Xayah"),
], d3="j2a")
FX += [tar(W(f + "2", "entra"), NX(f + "2"), "Entra, aguanta, sale", "Ambessa", A, icono="Ambessa", x=.76, y=.17, tam=40)]
a = T0(f + "3")
FX += [CLIP("g1_j3", a, NX(f + "3"), 43, 50),
       gris(W(f + "3", "remata"), "Alvaro", "MKOI", "Lo remata Faker", .1, NX(f + "3")),
       tar(W(f + "3", "Teleportacion"), NX(f + "3"), "Teleportación", "Jojopyun entra a la pelea", R, icono="SummonerTeleport",
           x=.7, y=.84, tam=44)]
b = T0(f + "4")
FX += PZ("g1_j3", b, NX(f + "4"), 50, [
    dict(tipo="foco", en=b + .2, k=.42),
    anillo(.46, .66, 50, A, W(f + "4", "Faker"), "FAKER", "LO ATRAPAN", lado="der", icono="Syndra"),
    texto("JOJOPYUN Y MYRWN", "KOI", .62, .3, W(f + "4", "Myrwn"), color=R),
    anillo(.41, .52, 46, A, W(f + "4", "Doran"), "DORAN", "VA POR JOJOPYUN", lado="izq", icono="Ambessa"),
])
a = T0(f + "5")
FX += [CLIP("g1_j3", a, NX(f + "5"), 50, 64), acel(a, NX(f + "5")),
       gris(a + .1, "Faker", "T1", "Cae Faker", .1, W(f + "5", "Oner")),
       gris(a + .4, "Jojopyun", "MKOI", "Y Jojopyun", .26, W(f + "5", "Oner")),
       gris(W(f + "5", "Elyoya"), "Elyoya", "MKOI", "Llegó tarde", .1, NX(f + "5")),
       gris(W(f + "5", "Supa"), "Supa", "MKOI", "Lo caza Doran", .26, NX(f + "5")),
       tar(W(f + "5", "Cinco"), NX(f + "5"), "5 por 1", "Para T1", A, logo="T1", dato="5-1", x=.7, y=.84, tam=48)]
a = T0(f + "6")
w = W(f + "6", "asegura")
FX += [CLIP("g1_j3", a, w, 64, 93), acel(a, w, "» x4"),
       J("g1_j3", w, e1, 93),
       tar(w, e1, "Barón para T1", "22:29 · con 1 400 de vida", A, logo="T1", x=.5, y=.84, tam=48),
       dict(tipo="destello", en=w + 1.0, fuerza=.5),
       tar(W(f + "6", "regalo"), e1, "+3,2K", "T1 pasa delante", A, dato="+3,2K", x=.76, y=.17, tam=40)]
f = "jugada2_rep_"
e0, e1 = ESC("jugada2_rep")
FX += LENTA("g1_j3", e0, T1(f + "0") + .2, 54, .5, zoom=(1.3, .45, .45))
FX += [peg(T0(f + "0") + .3, "Doran", "Doran", A, "T1", "Entra primero · no muere", dur=T1(f + "0") - T0(f + "0"), x=.12, y=.55,
           tam=230),
       J("g1_j3", T1(f + "0") + .2, e1, 101),
       mg(L.barras("Oro de T1 en la partida 1", [(ICON("Ambessa"), "Minuto 21", 0), (ICON("Ambessa"), "Minuto 23", 3.3),
                                                  (ICON("Ambessa"), "Minuto 26", 5.8)], 6.0),
          T0(f + "1"), e1, [T0(f + "1"), W(f + "1", "seis") - .4, W(f + "1", "seis")], y=.5, nombre="barras oro")]

# ================================================================== JUGADA 3 · el robo del dragón (g1_j4, HUD = t + 1970)
f = "jugada3_"
e0, e1 = ESC("jugada3")
FX += VIVO("jugada3", "g1_j4", 54, "Transmisión oficial · partida 1", "MKOI", "Minuto 33")
a = T0(f + "0")
FX += REB("g1_j4", a, 71.25, 44)
FX += [CLIP("g1_j4", a + 1.2, NX(f + "0"), 44, 60),
       tar(W(f + "0", "tres"), NX(f + "0"), "T1 +3,4K", "3 dragones · el 4.º es el alma", A, logo="T1", x=.5, y=.84, tam=46)]
b = T0(f + "1")
FX += PZ("g1_j4", b, NX(f + "1"), 60, [
    dict(tipo="zona", pts=[(.27, .53), (.46, .53), (.46, .71), (.27, .71)], color=Y, en=W(f + "1", "foso"), alfa=.14),
    texto("DRAGÓN INFERNAL", "3 162 DE VIDA", .37, .47, W(f + "1", "dragon"), color=Y),
    anillo(.48, .62, 40, R, W(f + "1", "foso") + .3, "ALVARO", None, lado="abajo", icono="Alistar"),
    anillo(.585, .60, 40, R, W(f + "1", "foso") + .5, "SUPA", None, lado="der", icono="Kaisa"),
    texto("MYRWN · GNAR", "ESPERA EL ÚLTIMO GOLPE", .66, .73, W(f + "1", "Myrwn"), color=R),
    intencion([(.53, .74), (.46, .70), (.40, .64)], R, W(f + "1", "robarlo"), None),
])
a = T0(f + "2")
FX += [J("g1_j4", a, NX(f + "2"), 60, (62.6 - 60) / (NX(f + "2") - a)), x2(a, NX(f + "2"), "CÁMARA LENTA"),
       dict(tipo="destello", en=W(f + "2", "roba"), fuerza=.6),
       tar(W(f + "2", "roba"), NX(f + "2"), "¡Dragón robado!", "Myrwn · 33:51", R, logo="MKOI", x=.5, y=.84, tam=50)]
b = T0(f + "3")
FX += PZ("g1_j4", b, NX(f + "4"), 64, [
    dict(tipo="foco", en=b + .2, k=.4),
    anillo(.49, .52, 46, R, W(f + "3", "Alvaro"), "ALVARO", "CONTROL SOBRE FAKER", lado="der", icono="Alistar"),
    anillo(.35, .39, 40, A, W(f + "3", "Faker"), "FAKER", None, lado="izq", icono="Syndra"),
    anillo(.41, .72, 46, R, W(f + "3", "Myrwn"), "MYRWN", "MEGA GNAR", lado="izq", icono="Gnar"),
    texto("SUPA · KAI'SA", "LIBRE, ATRÁS", .56, .73, W(f + "4", "Supa"), color=R),
    intencion([(.52, .74), (.45, .55), (.38, .44)], R, W(f + "4", "libre"), "NADIE LLEGA", off=(140, 0)),
])
a = T0(f + "5")
FX += [CLIP("g1_j4", a, NX(f + "5"), 64, 72),
       gris(W(f + "5", "Oner"), "Oner", "T1", "Doble de Supa", .1, NX(f + "5")),
       gris(W(f + "5", "Peyz"), "Peyz", "T1", "Doble de Supa", .26, NX(f + "5")),
       gris(W(f + "5", "Keria"), "Keria", "T1", "Lo remata Myrwn", .42, NX(f + "5")),
       tar(W(f + "5", "Tres"), NX(f + "5"), "3 por 1", "Para KOI", R, logo="MKOI", dato="3-1", x=.72, y=.84, tam=48)]
a = T0(f + "6")
FX += [CLIP("g1_j4", a, e1, 72, 113), acel(a, e1, "» x4"),
       tar(W(f + "6", "Baron"), e1, "Barón para KOI", "34:42", R, logo="MKOI", x=.5, y=.84, tam=48),
       tar(W(f + "6", "esfuma"), e1, "KOI +2,1K", "Minuto 37", R, dato="+2,1K", x=.76, y=.17, tam=40)]
f = "jugada3_rep_"
e0, e1 = ESC("jugada3_rep")
FX += LENTA("g1_j4", e0, e1, 62.2, .4, zoom=(1.4, .40, .62))

# ================================================================== JUGADA 4 · la pelea del alma (g1_j5, HUD = t + 2294)
f = "jugada4_"
e0, e1 = ESC("jugada4")
FX += VIVO("jugada4", "g1_j5", 52, "Transmisión oficial · partida 1", "T1", "Minuto 39")
a = T0(f + "0")
FX += REB("g1_j5", a, 73.25, 38)
FX += [CLIP("g1_j5", a + 1.2, NX(f + "0"), 38, 48),
       tar(W(f + "0", "mil"), NX(f + "0"), "KOI +1,5K", "15-10 en asesinatos para T1", R, logo="MKOI", x=.5, y=.84, tam=46),
       tar(W(f + "0", "alma"), NX(f + "0"), "4.º dragón de T1 = alma", None, A, x=.5, y=.17, tam=46)]
b = T0(f + "1")
FX += PZ("g1_j5", b, NX(f + "2"), 48, [
    dict(tipo="zona", pts=[(.6, .36), (.8, .36), (.82, .58), (.6, .58)], color=Y, en=b + .3, alfa=.14),
    texto("DRAGÓN · 5 514", None, .70, .30, b + .4, color=Y),
    anillo(.775, .38, 38, R, W(f + "1", "cada"), "ALVARO", None, lado="der", icono="Alistar"),
    anillo(.88, .46, 38, R, W(f + "1", "cada") + .15, "SUPA", None, lado="izq", icono="Kaisa"),
    anillo(.83, .52, 38, R, W(f + "1", "cada") + .3, "ELYOYA", None, lado="izq", icono="Qiyana"),
    anillo(.43, .51, 40, R, W(f + "1", "cada") + .45, "MYRWN", None, lado="izq", icono="Gnar"),
    anillo(.42, .28, 38, A, W(f + "1", "cada") + .6, "ONER", None, lado="izq", icono="LeeSin"),
    anillo(.62, .21, 38, A, W(f + "1", "cada") + .75, "DORAN", None, lado="izq", icono="Ambessa"),
    texto("EXTERMINIO = FIN", "LOS NARRADORES", .2, .7, W(f + "1", "exterminio"), color=Y),
    texto("BARÓN DE KOI", "YA TERMINADO", .2, .6, W(f + "2", "Baron"), color=R),
], d3="j4a")
a = T0(f + "3")
b = W(f + "3", "Doran")
FX += [CLIP("g1_j5", a, b, 48, 52), acel(a, b)]
FX += PZ("g1_j5", b, NX(f + "3"), 52, [
    dict(tipo="foco", en=b + .2, k=.4),
    anillo(.625, .77, 52, A, b + .1, "DORAN", "SE LANZA CON TODO", lado="der", icono="Ambessa"),
    flecha([(.62, .75), (.53, .67), (.45, .60)], A, W(f + "3", "todo"), None, dur=.7),
    anillo(.44, .58, 40, R, W(f + "3", "KOI"), "ALVARO", None, lado="izq", icono="Alistar"),
    anillo(.23, .74, 40, R, W(f + "3", "KOI") + .2, "ELYOYA", None, lado="der", icono="Qiyana"),
    anillo(.37, .51, 36, A, W(f + "3", "acomode"), "KERIA", None, lado="izq", icono="Nautilus"),
    anillo(.34, .45, 36, A, W(f + "3", "acomode") + .2, "PEYZ", None, lado="izq", icono="Xayah"),
    dict(tipo="zona", pts=[(.12, .52), (.32, .52), (.32, .68), (.12, .68)], color=Y, en=W(f + "3", "mismo"), alfa=.12),
], d3="j4b")
a = T0(f + "4")
FX += [CLIP("g1_j5", a, NX(f + "4"), 52, 57.5),
       gris(W(f + "4", "Supa"), "Supa", "MKOI", "Lo mata Doran", .1, NX(f + "4")),
       dict(tipo="destello", en=W(f + "4", "Alma"), fuerza=.6),
       tar(W(f + "4", "Alma"), NX(f + "4"), "¡Alma para T1!", "Dragón · 39:10", A, logo="T1", x=.5, y=.84, tam=52)]
a = T0(f + "5")
FX += [CLIP("g1_j5", a, NX(f + "5"), 57.5, 88), acel(a, NX(f + "5"), "» x3"),
       gris(W(f + "5", "Jojopyun"), "Jojopyun", "MKOI", "Faker", .1, NX(f + "5"), y=.55, tam=170),
       gris(W(f + "5", "Alvaro"), "Alvaro", "MKOI", "Peyz", .24, NX(f + "5"), y=.55, tam=170),
       gris(W(f + "5", "Elyoya"), "Elyoya", "MKOI", "Doran", .38, NX(f + "5"), y=.55, tam=170),
       gris(W(f + "5", "Myrwn"), "Myrwn", "MKOI", "Oner", .52, NX(f + "5"), y=.55, tam=170),
       tar(W(f + "5", "Cinco"), NX(f + "5"), "5 por 0", "Exterminio", A, logo="T1", dato="5-0", x=.76, y=.84, tam=48)]
a = T0(f + "6")
FX += [CLIP("g1_j5", a, W(f + "6", "nexo"), 88, 101), acel(a, W(f + "6", "nexo")),
       J("g1_j5", W(f + "6", "nexo"), e1, 101),
       dict(tipo="destello", en=W(f + "6", "nexo"), fuerza=.7),
       vs(W(f + "6", "nexo") + .3, e1, "T1", "MKOI", "Partida 1 para T1", "39:55 · 20-10", ganador=0, y=.42)]
f = "jugada4_rep_"
e0, e1 = ESC("jugada4_rep")
FX += LENTA("g1_j5", e0, T1(f + "0") + .2, 56, .45, zoom=(1.3, .5, .62))
FX += [peg(T0(f + "0") + .3, "Doran", "Doran", A, "T1", "6/0/6 · cero muertes", dur=T1(f + "0") - T0(f + "0"), x=.12, y=.55,
           tam=230),
       J("g1_j5", T1(f + "0") + .2, e1, 101.5, .4),
       mg(L.calendario("Lo que KOI hizo bien", [("05:44", "Primera\nsangre", "rojo"), ("08:23", "3-0", "rojo"),
                                                ("33:51", "Dragón\nrobado", "rojo"), ("34:42", "Barón", "rojo")]),
          T0(f + "1"), W(f + "1", "perdio"), [W(f + "1", "arranque"), W(f + "1", "arranque") + .4, W(f + "1", "robo"),
                                              W(f + "1", "Baron")], y=.5, nombre="calendario KOI"),
       tar(W(f + "1", "perdio"), e1, "Pero perdió las 2 peleas grandes", "21:42 y 39:09", R, x=.5, y=.5, tam=56)]
# ── la partida 1 en oro
g = "curva1_"
FX += [mg(L.calendario("La partida 1 en oro", [("Min 9", "KOI\n+1,7K", "rojo"), ("Min 26", "T1\n+5,8K", "azul"),
                                               ("Min 37", "KOI\n+2,1K", "rojo"), ("Min 40", "T1\ngana", "azul")]),
          T0(g + "0"), T1(g + "1") + .3, [W(g + "0", "nueve"), W(g + "0", "veintiseis"), W(g + "0", "treinta"), W(g + "1", "pelea")],
          y=.5, nombre="curva oro"),
       tar(W(g + "1", "Tres"), T1(g + "1") + .3, "3 vueltas de marcador", None, "oro", x=.5, y=.86, tam=50)]

# ================================================================== JUGADA 5 · la caza en la jungla de T1 (g2_j1, HUD = t + 474,9)
f = "jugada5_"
e0, e1 = ESC("jugada5")
FX += VIVO("jugada5", "g2_j1", 66, "Transmisión oficial · KOI vs T1 · partida 2", "T1", "Minuto 9")
a = T0(f + "0")
FX += REB("g2_j1", a, 83.3, 25)
FX += [CLIP("g2_j1", a + 1.2, NX(f + "0"), 25, 57), acel(a + 1.2, NX(f + "0")),
       tar(W(f + "0", "Doran"), W(f + "0", "Peyz"), "Doran: +30 súbditos", "Y un nivel sobre Myrwn", A, logo="T1", x=.5, y=.84,
           tam=46),
       gris(W(f + "0", "Peyz"), "Myrwn", "MKOI", "Lo mata Peyz bajo su torre", .1, NX(f + "0"))]
b = T0(f + "1")
FX += [tar(W(f + "1", "larvas"), NX(f + "1"), "KOI tomó las larvas", "08:36", R, logo="MKOI", x=.76, y=.17, tam=38)]
FX += PZ("g2_j1", b, NX(f + "1"), 57, [
    anillo(.46, .64, 50, R, W(f + "1", "Elyoya"), "ELYOYA", "XIN ZHAO · ROBANDO", lado="der", icono="XinZhao"),
    texto("JUNGLA DE T1", None, .2, .3, W(f + "1", "jungla"), color=Y),
    anillo(.415, .27, 40, A, W(f + "1", "confian"), "DORAN", None, lado="izq", icono="Gwen"),
    anillo(.42, .39, 40, A, W(f + "1", "confian") + .2, "KERIA", None, lado="izq", icono="Karma"),
    intencion([(.42, .41), (.44, .52), (.455, .61)], A, W(f + "1", "confian") + .5, None),
])
a = T0(f + "2")
FX += [CLIP("g2_j1", a, NX(f + "2"), 57, 70), acel(a, NX(f + "2")),
       gris(W(f + "2", "remata"), "Elyoya", "MKOI", "Lo remata Doran", .1, NX(f + "2"))]
b = T0(f + "3")
FX += PZ("g2_j1", b, NX(f + "3"), 70, [
    anillo(.49, .60, 48, R, W(f + "3", "Alvaro"), "ALVARO", "HUYE POR EL RÍO", lado="der", icono="Seraphine"),
    texto("KERIA · KARMA", "ENCIMA", .64, .43, W(f + "3", "Keria"), color=A),
    anillo(.41, .28, 40, R, W(f + "3", "Segundo"), "SUPA", None, lado="der", icono="Ezreal"),
    anillo(.22, .62, 40, A, W(f + "3", "Segundo") + .2, "DORAN", None, lado="izq", icono="Gwen"),
    intencion([(.23, .60), (.31, .44), (.39, .31)], A, W(f + "3", "Segundo") + .5, None),
])
a = T0(f + "4")
FX += [CLIP("g2_j1", a, NX(f + "4"), 70, 85),
       gris(a + .1, "Alvaro", "MKOI", "Lo alcanza Keria", .1, NX(f + "4")),
       tar(W(f + "4", "Destello"), W(f + "4", "caza"), "Supa usa Destello", None, R, icono="SummonerFlash", x=.76, y=.17, tam=38),
       gris(W(f + "4", "caza"), "Supa", "MKOI", "Lo caza Doran", .26, NX(f + "4")),
       tar(W(f + "4", "Tres"), NX(f + "4"), "3 por 0", "+3K antes del minuto 10", A, logo="T1", dato="3-0", x=.72, y=.84, tam=46)]
a = T0(f + "5")
FX += [J("g2_j1", a, e1, 85), tar(a + .1, e1, "«Cocinada para T1»", "Los narradores, minuto 9", "oro", x=.5, y=.2, tam=52)]
f = "jugada5_rep_"
e0, e1 = ESC("jugada5_rep")
FX += LENTA("g2_j1", e0, e1, 75, .5, zoom=(1.25, .45, .5))

# ================================================================== JUGADA 6 · el exterminio en el dragón (g2_j2, HUD = t + 1109,9)
f = "jugada6_"
e0, e1 = ESC("jugada6")
FX += VIVO("jugada6", "g2_j2", 40, "Transmisión oficial · partida 2", "T1", "Minuto 19")
a = T0(f + "0")
FX += REB("g2_j2", a, 60, 27)
FX += [CLIP("g2_j2", a + 1.2, NX(f + "0"), 27, 42),
       tar(W(f + "0", "cinco"), W(f + "0", "dragon"), "T1 +5,6K", None, A, logo="T1", x=.76, y=.17, tam=40),
       tar(W(f + "0", "dragon"), NX(f + "0"), "Dragón infernal", "T1 lo empieza", "oro", x=.5, y=.84, tam=46),
       tar(W(f + "0", "Teleportacion"), NX(f + "0"), "TP de Myrwn", "KOI lo espera", R, icono="SummonerTeleport", x=.76, y=.3, tam=38)]
b = T0(f + "1")
FX += PZ("g2_j2", b, NX(f + "1"), 42, [
    anillo(.30, .44, 50, A, W(f + "1", "Oner"), "ONER", "JARVAN IV", lado="izq", icono="JarvanIV"),
    intencion([(.31, .44), (.37, .48), (.42, .54)], A, W(f + "1", "lanza"), "SOLO", off=(0, 50)),
    anillo(.43, .52, 38, R, W(f + "1", "mala"), "MYRWN", None, lado="der", icono="Ornn"),
    anillo(.53, .51, 38, R, W(f + "1", "mala") + .15, "ALVARO", None, lado="der", icono="Seraphine"),
    anillo(.50, .60, 38, R, W(f + "1", "mala") + .3, "SUPA", None, lado="der", icono="Ezreal"),
    anillo(.42, .66, 38, R, W(f + "1", "mala") + .45, "ELYOYA", None, lado="izq", icono="XinZhao"),
    texto("LA CARNADA", None, .18, .28, W(f + "1", "carnada"), color=Y, tam=44),
])
a = T0(f + "2")
FX += [J("g2_j2", a, NX(f + "2"), 42, (46 - 42) / (NX(f + "2") - a)), x2(a, NX(f + "2"), "CÁMARA LENTA"),
       tar(W(f + "2", "definitiva"), NX(f + "2"), "Definitiva de Alvaro", "Seraphine", R, icono="Seraphine", x=.24, y=.17, tam=38),
       tar(W(f + "2", "todos"), NX(f + "2"), "Todos van por Oner", None, R, logo="MKOI", x=.5, y=.84, tam=48)]
b = T0(f + "3")
FX += PZ("g2_j2", b, NX(f + "4"), 46, [
    dict(tipo="foco", en=b + .2, k=.4),
    texto("FAKER · ORIANNA", "POR EL FLANCO", .64, .72, W(f + "3", "Faker"), color=A),
    flecha([(.505, .80), (.49, .66), (.46, .52)], A, W(f + "3", "flanco"), None, dur=.8),
    anillo(.58, .64, 42, R, W(f + "3", "espera"), "JOJOPYUN", None, lado="der", icono="Viktor"),
    anillo(.33, .41, 40, R, W(f + "3", "espera") + .2, "ELYOYA", None, lado="izq", icono="XinZhao"),
    texto("SUPA · EZREAL", "SIN PEGAR LIBRE", .78, .13, W(f + "4", "Supa"), color=R),
], d3="j6a")
a = T0(f + "5")
FX += [CLIP("g2_j2", a, NX(f + "5"), 46, 60),
       gris(W(f + "5", "Jojopyun"), "Jojopyun", "MKOI", "Oner", .08, NX(f + "5"), y=.55, tam=160),
       gris(W(f + "5", "Supa"), "Supa", "MKOI", "Doran", .2, NX(f + "5"), y=.55, tam=160),
       gris(W(f + "5", "Alvaro"), "Alvaro", "MKOI", "Keria", .32, NX(f + "5"), y=.55, tam=160),
       gris(W(f + "5", "Elyoya"), "Elyoya", "MKOI", "Peyz", .44, NX(f + "5"), y=.55, tam=160),
       gris(W(f + "5", "Myrwn"), "Myrwn", "MKOI", "Faker", .56, NX(f + "5"), y=.55, tam=160),
       dict(tipo="destello", en=W(f + "5", "Exterminio"), fuerza=.6),
       peg(W(f + "5", "sobrevive"), "Oner", "Oner", A, "T1", "Sobrevive", dur=NX(f + "5") - W(f + "5", "sobrevive"), x=.85, y=.5,
           tam=240)]
a = T0(f + "6")
FX += [CLIP("g2_j2", a, e1, 60, 72),
       tar(a + .1, W(f + "6", "minuto"), "Dragón infernal", "19:41 · para T1", A, logo="T1", x=.5, y=.84, tam=46),
       tar(W(f + "6", "diez"), e1, "+10,3K", "Minuto 20", A, dato="+10K", x=.76, y=.17, tam=40)]
f = "jugada6_rep_"
e0, e1 = ESC("jugada6_rep")
FX += LENTA("g2_j2", e0, e1, 50, .45, zoom=(1.3, .48, .55))

# ================================================================== JUGADA 7 · el final (g2_j3, HUD = t + 1444,9)
f = "jugada7_"
e0, e1 = ESC("jugada7")
FX += VIVO("jugada7", "g2_j3", 44, "Transmisión oficial · partida 2", "T1", "Minuto 25")
a = T0(f + "0")
FX += REB("g2_j3", a, 60.1, 30)
FX += [CLIP("g2_j3", a + 1.2, NX(f + "0"), 30, 50), acel(a + 1.2, NX(f + "0")),
       tar(W(f + "0", "tres"), W(f + "0", "Faker"), "3 dragones", "El alma, en 20 segundos", A, logo="T1", x=.76, y=.17, tam=38),
       tar(W(f + "0", "Onda"), NX(f + "0"), "Onda de choque", "Faker · Orianna", A, icono="Orianna", x=.24, y=.17, tam=38),
       tar(W(f + "0", "cinco"), NX(f + "0"), "5 por 1", None, A, logo="T1", dato="5-1", x=.72, y=.84, tam=46)]
a = T0(f + "1")
FX += [CLIP("g2_j3", a, NX(f + "1"), 50, 60),
       gris(W(f + "1", "Oner"), "Oner", "T1", "La única baja de T1", .1, NX(f + "1"))]
a = T0(f + "2")
w = W(f + "2", "nexo")
FX += [CLIP("g2_j3", a, w, 60, 95), acel(a, w, "» x4"), J("g2_j3", w, e1, 95),
       dict(tipo="destello", en=w, fuerza=.7),
       vs(w + .2, e1, "T1", "MKOI", "T1 2 · KOI 0", "A cuartos de final", ganador=0, y=.42)]
f = "jugada7_rep_"
e0, e1 = ESC("jugada7_rep")
FX += LENTA("g2_j3", e0, e1, 59, .4, zoom=(1.25, .5, .5))

# ================================================================== LAS CLAVES
g = "claves_"
FX += [
    tar(T0(g + "0"), T1(g + "0") + .3, "Tres claves", "¿Qué decidió la serie?", "oro", x=.5, y=.45, tam=90),
    tar(T0(g + "1"), T1(g + "1") + .3, "1 · Doran", None, "oro", x=.5, y=.17, tam=60),
    gran(T0(g + "1") + .2, "Doran", "Doran", A, "T1", "0 muertes en la serie", dur=T1(g + "1") - T0(g + "1"), x=.5, tam=520),
    tar(T0(g + "2"), T1(g + "2") + .3, "2 · Las peleas grandes", None, "oro", x=.5, y=.17, tam=60),
    mg(L.resultados("Las peleas que valían algo", [(EQ("T1"), "Barón · 22:29", EQ("MKOI"), "KOI", 0),
                                                   (EQ("T1"), "Alma · 39:10", EQ("MKOI"), "KOI", 0),
                                                   (EQ("T1"), "Dragón · 19:41", EQ("MKOI"), "KOI", 0)]),
       W(g + "2", "pero"), T1(g + "2") + .3, [W(g + "2", "Baron"), W(g + "2", "alma"), W(g + "2", "partida")], y=.5,
       nombre="resultados peleas"),
    tar(T0(g + "3"), T1(g + "3") + .3, "3 · La jungla", None, "oro", x=.5, y=.17, tam=60),
    peg(W(g + "3", "primera"), "Elyoya", "Elyoya", R, "MKOI", "Partida 1: castiga", dur=W(g + "3", "segunda") - W(g + "3", "primera"),
        x=.3, y=.5, tam=380),
    peg(W(g + "3", "segunda"), "Elyoya", "Elyoya", R, "MKOI", "Partida 2: lo cazan", dur=T1(g + "3") - W(g + "3", "segunda") + .3,
        x=.7, y=.5, tam=380, gris=True),
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
