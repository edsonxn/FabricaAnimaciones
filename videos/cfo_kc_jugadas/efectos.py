# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «CFO vs KC: las jugadas clave» (estilo análisis táctico, docs/estilo_analisis_tactico.md), con los helpers
de videos/t1_koi_worlds/efectos.py. Fuentes por partida: medios/_fuente/g<p>_j<k>.mp4 (HUD = t + K). Partida 1: KC AZUL, CFO ROJO;
partida 2: CFO AZUL, KC ROJO (los colores siguen el lado del mapa). Pausas: investigacion/pausas_g1.md (G1) y
previews/cuadros/r_g2_*.jpg (G2, medidas el 29-oct). Tiempos anclados a la voz (T0/T1/W/NX sobre timeline.json).
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
    col = {"KC": COLOR("KC"), "CFO": COLOR("CFO")}
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
                       .replace("Kaisa", "Kai'Sa").replace("XinZhao", "Xin Zhao").replace("MonkeyKing", "Wukong"), dur=T1(k) - e + .35,
                       x=.1 + .2 * i, y=.5, tam=330))
    return out


FX = []
PARTIDA = 1


def COLOR(eq):
    """el color sigue al lado del mapa: partida 1 KC azul, partida 2 CFO azul"""
    return A if (eq == "KC") == (PARTIDA == 1) else R


K = {"g1_j1": 296, "g1_j2": 436, "g1_j3": 556, "g1_j4": 656, "g1_j5": 856, "g1_j6": 986, "g1_j7": 1436, "g1_j8": 1566,
     "g2_j1": 107, "g2_j2": 317, "g2_j3": 568, "g2_j4": 1182, "g2_j5": 1412, "g2_j6": 1659, "g2_j7": 1799, "g2_j8": 2041}


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
    col = COLOR(eq)
    return peg(en, jug, jug, col, eq, sub, dur=(a or en + 3.0) - en, x=x, y=y, tam=tam, gris=True)


def acel(de, a, texto="» ACELERADO"):
    return x2(de, a, texto)



def P_(eq):
    """pegatina del jugador con el color de su lado en esta partida"""
    return COLOR(eq)


def zona(x, y, rx, ry, color, en, etiqueta=None, alfa=.16):
    """zona elíptica (polígono de 16 puntos) sobre el cuadro congelado"""
    import math as _m
    return dict(tipo="zona", pts=[(x + rx * _m.cos(k * _m.pi / 8), y + ry * _m.sin(k * _m.pi / 8)) for k in range(16)], color=color,
                en=en, alfa=alfa)


def an(x, y, jug, sub, eq, en, camp, lado="arriba", r=46):
    """anillo en los PIES medidos de un jugador (nombre en mayúsculas, icono del campeón)"""
    return anillo(x, y, r, COLOR(eq), en, jug.upper(), sub, lado=lado, icono=camp)


# ================================================================== GANCHO (SIN SPOILER)
g = "gancho_"
FX += [
    mg(L.apertura("CFO vs KC", "Worlds 2026 · ronda 4 · el que pierda, a casa"), 0.0, W(g + "0", "CTBC"), x=.5, y=.5,
       nombre="apertura"),
    dict(tipo="destello", en=0.15, fuerza=.7),
    vs(W(g + "0", "CTBC"), T1(g + "0") + .2, "CFO", "KC", "Al mejor de 3", "29 de octubre · a muerte", y=.42),
    tar(W(g + "0", "perdiera"), T1(g + "0") + .2, "El que pierda, se va a casa", None, "oro", x=.5, y=.84, tam=50),
    tar(W(g + "1", "dragon"), W(g + "1", "ventaja"), "Un dragón que terminó en masacre", None, "oro", x=.5, y=.8, tam=50),
    tar(W(g + "1", "ventaja"), W(g + "1", "pausa"), "Casi 5 000 de oro de ventaja", None, "oro", x=.5, y=.8, tam=50),
    tar(W(g + "1", "pausa"), W(g + "1", "ancestral"), "Una pausa de casi media hora", None, "oro", x=.5, y=.8, tam=50),
    tar(W(g + "1", "ancestral"), T1(g + "1") + .2, "Un dragón ancestral", "Que lo decidió todo", "oro", x=.5, y=.8, tam=50),
    mg(L.menu([(ART("Galio"), "Las mejores", "azul"), (JUG("Shad0w"), "Las más inteligentes", "rojo"),
               (ART("Viktor"), "Las predicciones", "amarillo"), (EQ("KC"), "Los errores de cada uno", "oro")]),
       T0(g + "2"), T1(g + "2") + .3,
       [W(g + "2", "mejores"), W(g + "2", "inteligentes"), W(g + "2", "predicciones"), W(g + "2", "errores")], y=.5,
       nombre="menu"),
]
# ================================================================== LO QUE ESTABA EN JUEGO
g = "juego_"
FX += [
    tar(T0(g + "0"), W(g + "0", "fase"), "Lo que estaba en juego", None, "oro", x=.5, y=.2, tam=74),
    mg(L.suiza("Fase suiza · Worlds 2026"), W(g + "0", "fase"), W(g + "0", "llegaban"),
       [W(g + "0", "fase"), W(g + "0", "fase") + .6, W(g + "0", "tres"), W(g + "0", "casa"), W(g + "0", "casa") + .5,
        W(g + "0", "llegaban")], y=.46, nombre="suiza"),
    mg(L.tabla("Antes de hoy", [("1-2 · a muerte", "rojo", [(EQ("CFO"), "CTBC Flying Oyster"), (EQ("KC"), "Karmine Corp")])]),
       W(g + "0", "llegaban"), T1(g + "1") + .3, [W(g + "0", "llegaban")], y=.5, nombre="tabla 1-2"),
    tar(W(g + "1", "ganara"), W(g + "1", "perdiera"), "El que gane: 2-2", "Sigue vivo a la ronda 5", "oro", x=.5, y=.84, tam=52),
    tar(W(g + "1", "perdiera"), T1(g + "1") + .3, "El que pierda: 1-3", "Eliminado del Mundial", R, x=.5, y=.84, tam=52),
    tar(T0(g + "2"), W(g + "2", "Fearless"), "Al mejor de 3", "Gana quien llegue a dos", "oro", x=.5, y=.2, tam=66),
    tar(W(g + "2", "Fearless"), T1(g + "2") + .3, "Fearless Draft", "En la serie, ningún campeón se repite", "oro", x=.5, y=.17,
        tam=66),
]
# ================================================================== DRAFTS
FX += [tar(T0("draft1_0"), W("draft1_0", "Canna"), "Partida 1", "Karmine · lado azul", A, logo="KC", x=.5, y=.2, tam=70)]
FX += draft("draft1_0", "KC", A, [("Canna", "Galio", "Canna"), ("Yike", "MonkeyKing", "Yike"), ("kyeahoo", "Cassiopeia", "kyeahoo"),
                                  ("Caliste", "Tristana", "Caliste"), ("Busio", "Nautilus", "Busio")])
FX += [tar(T0("draft1_1"), W("draft1_1", "Rest"), "CTBC Flying Oyster", "Lado rojo", R, logo="CFO", x=.5, y=.2, tam=70)]
FX += draft("draft1_1", "CFO", R, [("Rest", "Rumble", "Rest"), ("Shad0w", "JarvanIV", "Shad0w"), ("POUT", "Syndra", "POUT"),
                                   ("Doggo", "Kaisa", "Doggo"), ("Kino", "Alistar", "Kino")])
FX += [peg(W("draft1_2", "Tristana"), CARGA("Tristana"), "Caliste", A, "KC", "¿Tristana contra Syndra?",
           dur=T1("draft1_2") - W("draft1_2", "Tristana") + .3, x=.3, y=.5, tam=380),
       tar(W("draft1_2", "Guarda"), T1("draft1_2") + .3, "Predicción n.º 1", "Guárdala", "oro", x=.7, y=.62, tam=56)]
FX += [tar(T0("draft2_0"), W("draft2_0", "Rest"), "Partida 2", "CFO · lado azul", A, logo="CFO", x=.5, y=.2, tam=70)]
FX += draft("draft2_0", "CFO", A, [("Rest", "Ambessa", "Rest"), ("Shad0w", "LeeSin", "Shad0w"), ("POUT", "Ryze", "POUT"),
                                   ("Doggo", "Caitlyn", "Doggo"), ("Kino", "Karma", "Kino")])
FX += draft("draft2_1", "KC", R, [("Canna", "Camille", "Canna"), ("Yike", "Pantheon", "Yike"), ("kyeahoo", "Viktor", "kyeahoo"),
                                  ("Caliste", "Yunara", "Caliste"), ("Busio", "Lulu", "Busio")])
FX += [peg(W("draft2_2", "Lee"), CARGA("LeeSin"), "Shad0w", A, "CFO", "Lee Sin", dur=T1("draft2_2") - W("draft2_2", "Lee") + .3,
           x=.3, y=.5, tam=380),
       peg(W("draft2_2", "Yike"), "Yike", "Yike", R, "KC", "Se lo estaba guardando", dur=T1("draft2_2") - W("draft2_2", "Yike") + .3,
           x=.7, y=.5, tam=380, gris=True, sello=("FEARLESS", 0))]

# ================================================================== JUGADA 1 · el dragón de Nube por la 1.ª sangre (g1_j1, g1_j2)
PARTIDA = 1
f = "jugada1_"
e0, e1 = ESC("jugada1")
FX += VIVO("jugada1", "g1_j1", 60 - (T0(f + "0") - e0), "Transmisión oficial · CFO vs KC · partida 1", "KC", "Minuto 5")
a = T0(f + "0")
FX += REB("g1_j1", a, 60, 30)
FX += [CLIP("g1_j1", a + 1.2, NX(f + "0"), 30, 45),
       tar(W(f + "0", "Nube"), NX(f + "0"), "Dragón de Nube", "CFO · 05:35", R, logo="CFO", x=.76, y=.17, tam=40)]
b = T0(f + "1")
FX += [CLIP("g1_j1", NX(f + "0"), b, 45, 51)] if b - NX(f + "0") > .1 else []
FX += PZ("g1_j1", b, NX(f + "2"), 51, [
    dict(tipo="foco", en=b + .2, k=.42),
    an(.554, .327, "POUT", "SIN DESTELLO", "CFO", W(f + "1", "POUT"), "Syndra", lado="der"),
    an(.653, .608, "Busio", None, "KC", W(f + "2", "Busio"), "Nautilus", lado="der"),
    an(.366, .476, "kyeahoo", None, "KC", W(f + "2", "Busio") + .3, "Cassiopeia", lado="izq"),
    intencion([(.653, .59), (.61, .46), (.565, .35)], A, W(f + "2", "arbusto"), None),
    texto("SHAD0W Y KINO", "SE FUERON AL DRAGÓN", .2, .25, W(f + "2", "Shad0w"), color=Y),
    texto("NADIE VA A AYUDAR A POUT", None, .72, .2, W(f + "2", "Nadie"), color=Y),
])
a = T0(f + "3")
FX += [CLIP("g1_j1", a, NX(f + "3"), 51, 60),
       tar(W(f + "3", "sangre"), NX(f + "3"), "Primera sangre", "Yike sobre POUT · 05:53", A, logo="KC", x=.5, y=.84, tam=48),
       gris(W(f + "3", "Yike"), "POUT", "CFO", "Cae a la tercera", .1, NX(f + "3")),
       dict(tipo="destello", en=W(f + "3", "sangre"), fuerza=.5)]
b = T0(f + "4")
FX += PZ("g1_j2", b, NX(f + "4"), 26, [
    an(.395, .569, "Busio", "SOLO EN EL RÍO", "KC", W(f + "4", "Busio"), "Nautilus", lado="izq"),
    an(.557, .371, "Shad0w", None, "CFO", W(f + "4", "Shad0w"), "JarvanIV", lado="der"),
    an(.414, .320, "POUT", None, "CFO", W(f + "4", "Shad0w") + .3, "Syndra", lado="izq"),
    intencion([(.557, .371), (.48, .47), (.41, .55)], R, W(f + "4", "lee"), None),
    texto("SIN GUARDIA", "EN EL RÍO", .76, .62, W(f + "4", "guardia"), color=Y),
])
a = T0(f + "5")
FX += [CLIP("g1_j2", a, e1, 26, 40),
       tar(W(f + "5", "revancha"), e1, "POUT sobre Busio", "07:50 · 1 a 1", R, logo="CFO", x=.5, y=.84, tam=48),
       gris(W(f + "5", "revancha"), "Busio", "KC", "Cazado en el río", .1, e1),
       dict(tipo="destello", en=W(f + "5", "revancha"), fuerza=.45)]

# ================================================================== JUGADA 2 · Caliste castiga a Kino (g1_j3)
f = "jugada2_"
e0, e1 = ESC("jugada2")
FX += VIVO("jugada2", "g1_j3", 34 - (T0(f + "0") - e0), "Transmisión oficial · partida 1", "KC", "Minuto 9")
a = T0(f + "0")
FX += REB("g1_j3", a, 34, 13)
FX += [CLIP("g1_j3", a + 1.2, NX(f + "0"), 13, 25),
       peg(W(f + "0", "Kino"), ICON("Alistar"), "Kino · nivel 5", R, "CFO", dur=NX(f + "0") - W(f + "0", "Kino"), x=.15, y=.5, tam=260),
       peg(W(f + "0", "Busio"), ICON("Nautilus"), "Busio · nivel 6", A, "KC", dur=NX(f + "0") - W(f + "0", "Busio"), x=.85, y=.5,
           tam=260)]
b = T0(f + "1")
FX += PZ("g1_j3", b, NX(f + "1"), 25, [
    an(.468, .486, "Kino", "NIVEL 5", "CFO", W(f + "1", "Pausa") + .3, "Alistar", lado="der"),
    an(.416, .620, "Busio", "NIVEL 6 · DEFINITIVA", "KC", W(f + "1", "Nautilus"), "Nautilus", lado="izq"),
    an(.433, .704, "Caliste", None, "KC", W(f + "1", "adelante"), "Tristana", lado="der", r=40),
    intencion([(.416, .60), (.44, .55), (.465, .50)], A, W(f + "1", "adelante"), None),
    texto("NO LE PUEDE RESPONDER", None, .74, .3, W(f + "1", "responder"), color=Y),
])
a = T0(f + "2")
FX += [CLIP("g1_j3", a, e1, 25, 40),
       gris(W(f + "2", "Kino"), "Kino", "CFO", "Un nivel abajo", .1, W(f + "2", "narradores")),
       dict(tipo="destello", en=W(f + "2", "Kino"), fuerza=.45),
       tar(W(f + "2", "narradores"), e1, "«Si Caliste se alimenta…»", "Los narradores, minuto 9", "oro", x=.5, y=.2, tam=50),
       peg(W(f + "2", "asegurado"), "Caliste", "Caliste", A, "KC", "Predicción n.º 2", dur=e1 - W(f + "2", "asegurado"), x=.82,
           y=.52, tam=360)]

# ================================================================== JUGADA 3 · el dragón Químico (g1_j4) ★ 3D
f = "jugada3_"
e0, e1 = ESC("jugada3")
FX += VIVO("jugada3", "g1_j4", 52 - (T0(f + "0") - e0), "Transmisión oficial · partida 1", "KC", "Minuto 11")
a = T0(f + "0")
FX += REB("g1_j4", a, 52, 14)
FX += [CLIP("g1_j4", a + 1.2, NX(f + "0"), 14, 25),
       tar(W(f + "0", "mil"), NX(f + "0"), "Karmine +1 000", "Feed oficial · 11:00", A, logo="KC", x=.76, y=.17, tam=40),
       tar(W(f + "0", "Quimico"), NX(f + "0"), "Dragón Químico", "Yike lo empieza", A, icono="MonkeyKing", x=.24, y=.17, tam=40)]
b = T0(f + "1")
FX += PZ("g1_j4", b, NX(f + "1"), 25, [
    dict(tipo="foco", en=b + .2, k=.35),
    zona(x=.25, y=.24, rx=.09, ry=.10, color=A, en=W(f + "1", "foso"), etiqueta="FOSO"),
    an(.247, .313, "Yike", "EN EL DRAGÓN", "KC", W(f + "1", "vision"), "MonkeyKing", lado="der"),
    an(.512, .153, "Guardia", "DE KC", "KC", W(f + "1", "guardias"), "SummonerFlash", lado="der", r=30),
    an(.273, .692, "Busio", None, "KC", W(f + "1", "entrada"), "Nautilus", lado="izq", r=40),
    an(.423, .698, "Caliste", None, "KC", W(f + "1", "entrada") + .2, "Tristana", lado="der", r=40),
    an(.747, .437, "Kino", "LLEGANDO", "CFO", W(f + "1", "CFO"), "Alistar", lado="izq"),
    texto("LOS VEN LLEGAR", None, .72, .25, W(f + "1", "vean"), color=Y),
], d3="j3a")
a = T0(f + "2")
FX += [CLIP("g1_j4", a, NX(f + "2"), 27.4, 30), x2(a, NX(f + "2"), "CÁMARA LENTA"),
       tar(W(f + "2", "Kino"), W(f + "2", "Rest"), "Kino: definitiva", "Antes del dragón", R, icono="Alistar", x=.24, y=.17, tam=40),
       tar(W(f + "2", "Rest"), NX(f + "2"), "Rest: Teleportación", "Posición comprometida", R, icono="SummonerTeleport",
           x=.24, y=.17, tam=40)]
b = T0(f + "3")
FX += PZ("g1_j4", b, NX(f + "3"), 30, [
    an(.600, .408, "Doggo", "SIN SU PRIMER OBJETO", "CFO", W(f + "3", "Doggo"), "Kaisa", lado="der"),
    an(.537, .372, "Shad0w", None, "CFO", W(f + "3", "Doggo") + .4, "JarvanIV", lado="izq", r=40),
    an(.553, .218, "Kino", "DEFINITIVA GASTADA", "CFO", W(f + "3", "Doggo") + .7, "Alistar", lado="der", r=40),
    intencion([(.537, .372), (.49, .29), (.44, .21)], R, W(f + "3", "regresado"), None),
    texto("NO PEGA", None, .78, .55, W(f + "3", "pega"), color=Y),
], d3="j3b")
a = T0(f + "4")
FX += [CLIP("g1_j4", a, NX(f + "4"), 30, 45),
       tar(W(f + "4", "asegura"), W(f + "4", "Canna"), "Dragón para Karmine", "11:31", A, logo="KC", x=.5, y=.84, tam=48),
       peg(W(f + "4", "Canna"), "Canna", "Canna", A, "KC", "Galio cae del cielo", dur=NX(f + "4") - W(f + "4", "Canna"), x=.85,
           y=.5, tam=360),
       gris(W(f + "4", "Shad0w"), "Shad0w", "CFO", "11:41", .1, NX(f + "4")),
       dict(tipo="destello", en=W(f + "4", "cae"), fuerza=.5)]
a = T0(f + "5")
FX += [CLIP("g1_j4", a, e1, 45, 56),
       gris(W(f + "5", "Kino"), "Kino", "CFO", "11:43", .26, e1),
       gris(W(f + "5", "Doggo"), "Doggo", "CFO", "11:46", .42, e1),
       dict(tipo="destello", en=W(f + "5", "Doggo"), fuerza=.55),
       tar(W(f + "5", "Tres"), e1, "3 por 0 y el dragón", "kyeahoo: doble asesinato", A, logo="KC", dato="3-0", x=.75, y=.84, tam=48)]
e0, e1 = ESC("jugada3_rep")
FX += LENTA("g1_j4", e0, e1, 47, .45, zoom=(1.35, .40, .32))
FX += [tar(W("jugada3_rep_0", "definitiva"), W("jugada3_rep_0", "Kai"), "Error 1", "Definitiva de Kino, ya gastada", R, x=.5, y=.84,
           tam=46),
       tar(W("jugada3_rep_0", "Kai"), W("jugada3_rep_0", "Teleportacion"), "Error 2", "Kai'Sa sin objeto", R, x=.5, y=.84, tam=46),
       tar(W("jugada3_rep_0", "Teleportacion"), e1, "Error 3", "La Teleportación de Rest", R, x=.5, y=.84, tam=46)]

# ================================================================== JUGADA 4 · lo mejor de CFO (g1_j5) y las dos peleas 3 por 0 (g1_j6)
f = "jugada4_"
e0, e1 = ESC("jugada4")
FX += VIVO("jugada4", "g1_j6", 64 - (T0(f + "0") - e0), "Transmisión oficial · partida 1", "KC", "Minuto 17")
a = T0(f + "0")
FX += REB("g1_j6", a, 64, 40)
FX += [CLIP("g1_j5", a + 1.2, NX(f + "0"), 24, 36),
       tar(a + 1.3, W(f + "0", "POUT"), "Minuto 14", "Lo mejor de CFO", R, logo="CFO", x=.76, y=.17, tam=40),
       gris(W(f + "0", "remata"), "kyeahoo", "KC", "14:48", .1, NX(f + "0")),
       dict(tipo="destello", en=W(f + "0", "remata"), fuerza=.45)]
a = T0(f + "1")
FX += [J("g1_j5", a, NX(f + "1"), 36, .5), x2(a, NX(f + "1"), "CÁMARA LENTA"),
       gran(W(f + "1", "unica"), "kyeahoo", "kyeahoo", A, "KC", "Su única muerte en la serie", dur=NX(f + "1") - W(f + "1", "unica"))]
a = T0(f + "2")
FX += [CLIP("g1_j6", a, NX(f + "2"), 40, 47.5),
       tar(W(f + "2", "Rest"), NX(f + "2"), "Rest: TP + definitiva", "17:11", R, icono="Rumble", x=.24, y=.17, tam=40)]
b = T0(f + "3")
FX += PZ("g1_j6", b, NX(f + "3"), 47.5, [
    zona(x=.574, y=.443, rx=.07, ry=.08, color=A, en=W(f + "3", "provocacion"), etiqueta="PROVOCACIÓN"),
    an(.575, .47, "Canna", "GALIO", "KC", W(f + "3", "Canna"), "Galio", lado="der"),
    an(.398, .472, "Rest", "ATRAPADO", "CFO", W(f + "3", "atrapa"), "Rumble", lado="izq"),
    an(.268, .369, "kyeahoo", "MIRADA PETRIFICANTE", "KC", W(f + "3", "kyeahoo"), "Cassiopeia", lado="izq", r=40),
    an(.216, .551, "Caliste", None, "KC", W(f + "3", "petrifica"), "Tristana", lado="izq", r=38),
    an(.345, .718, "Yike", None, "KC", W(f + "3", "petrifica") + .2, "MonkeyKing", lado="der", r=38),
])
a = T0(f + "4")
w = W(f + "4", "minuto")
FX += [CLIP("g1_j6", a, w, 47.5, 64),
       gris(W(f + "4", "Kino"), "Kino", "CFO", "17:19", .1, w), gris(W(f + "4", "Rest"), "Rest", "CFO", "17:20", .26, w),
       gris(W(f + "4", "Shad0w"), "Shad0w", "CFO", "17:28", .42, w),
       dict(tipo="destello", en=W(f + "4", "Tres"), fuerza=.5),
       tar(W(f + "4", "Tres"), w, "3 por 0", "17:19-17:28", A, logo="KC", dato="3-0", x=.75, y=.84, tam=48),
       CLIP("g1_j6", w, NX(f + "4"), 64, 131), acel(w, NX(f + "4"), "» x8"),
       tar(W(f + "4", "otra"), NX(f + "4"), "Otra vez 3 por 0", "18:31-18:36", A, logo="KC", dato="3-0", x=.75, y=.84, tam=48),
       dict(tipo="destello", en=W(f + "4", "otra"), fuerza=.5)]
a = T0(f + "5")
FX += [J("g1_j6", a, e1, 131),
       tar(a + .1, e1, "«CFO no había hecho un solo combo»", "Los narradores, minuto 19", "oro", x=.5, y=.2, tam=48)]
e0, e1 = ESC("jugada4_rep")
FX += LENTA("g1_j6", e0, e1, 62, .45, zoom=(1.3, .45, .5))
FX += [mg(L.barras("Ventaja de Karmine", [(ICON("Galio"), "Antes de las peleas", 2.9), (ICON("Galio"), "Dos minutos después", 6.5)],
                   7.0), W("jugada4_rep_0", "ventaja"), e1, [W("jugada4_rep_0", "casi"), W("jugada4_rep_0", "seis")], y=.5,
          nombre="barras oro g1")]

# ================================================================== JUGADA 5 · el pick a Shad0w + Barón (g1_j7) y el cierre (g1_j8)
f = "jugada5_"
e0, e1 = ESC("jugada5")
FX += VIVO("jugada5", "g1_j7", 40 - (T0(f + "0") - e0), "Transmisión oficial · partida 1", "KC", "Minuto 24")
a = T0(f + "0")
FX += REB("g1_j7", a, 40, 31)
w = W(f + "0", "provocacion")
FX += [CLIP("g1_j7", a + 1.2, w, 31, 33.6)]
FX += PZ("g1_j7", w, W(f + "0", "Yike"), 33.6, [
    an(.443, .707, "Shad0w", "ATRAPADO", "CFO", w + .2, "JarvanIV", lado="der"),
    an(.308, .675, "Canna", "PROVOCACIÓN", "KC", w + .5, "Galio", lado="izq"),
    zona(x=.31, y=.62, rx=.08, ry=.07, color=Y, en=w + .8, etiqueta="BARÓN"),
])
b = W(f + "0", "Yike")
FX += [CLIP("g1_j7", b, NX(f + "0"), 33.6, 37),
       gris(b, "Shad0w", "CFO", "24:32", .1, NX(f + "0")), dict(tipo="destello", en=b, fuerza=.45)]
a = T0(f + "1")
FX += [CLIP("g1_j7", a, NX(f + "1"), 37, 62), acel(a, NX(f + "1")),
       gris(W(f + "1", "Busio"), "Busio", "KC", "24:35", .1, W(f + "1", "jungla")),
       tar(W(f + "1", "Baron", 1), NX(f + "1"), "Barón para Karmine", "24:56", A, logo="KC", x=.5, y=.84, tam=48)]
a = T0(f + "2")
w = W(f + "2", "nexo")
FX += [CLIP("g1_j8", a, w, 72, 93),
       tar(W(f + "2", "exterminio"), w, "Exterminio", "Los cinco de CFO en siete segundos", A, logo="KC", x=.5, y=.84, tam=48),
       dict(tipo="destello", en=W(f + "2", "exterminio"), fuerza=.5),
       J("g1_j8", w, e1, 93),
       mg(L.versus((EQ("KC"), "KC"), (EQ("CFO"), "CFO"), "Partida 1", "27:39 · 19 a 3", ganador=0), W(f + "2", "Uno"), e1,
          [W(f + "2", "Uno")], y=.45, nombre="versus 1-0")]
e0, e1 = ESC("jugada5_rep")
FX += LENTA("g1_j8", e0, e1, 82, .45, zoom=(1.25, .5, .5))
FX += [tar(W("jugada5_rep_0", "Diecinueve"), e1, "19 a 3 · 0 torres de CFO", "Una partida perfecta", A, logo="KC", x=.5, y=.84,
           tam=48)]

# ================================================================== PARTIDA 1 EN ORO + PREDICCIONES
g = "curva1_"
FX += [mg(L.calendario("La partida 1 en oro", [("Min 1", "Último minuto\nde CFO arriba", "rojo"), ("Min 11", "Dragón\nQuímico", "azul"),
                                                ("Min 18", "Dos 3 por 0", "azul"), ("Min 27", "KC\n+15K", "azul")]),
          T0(g + "0"), T1(g + "0") + .3, [T0(g + "0") + .3, W(g + "0", "primero"), W(g + "0", "Quince") - .8, W(g + "0", "Quince")],
          y=.5, nombre="calendario g1"),
       peg(W(g + "1", "Tristana"), "Caliste", "Caliste", A, "KC", "7/0/5", dur=W(g + "1", "otra") - W(g + "1", "Tristana"), x=.3,
           y=.5, tam=400, sello=("FALLÓ", 0)),
       peg(W(g + "1", "otra"), "Doggo", "Doggo", R, "CFO", "0/3/0 · 0 %", dur=T1(g + "1") + .3 - W(g + "1", "otra"), x=.7, y=.5,
           tam=400, gris=True, sello=("SE CUMPLIÓ", 0))]

# ================================================================== JUGADA 6 · el arranque de CFO (g2_j1, g2_j2, g2_j3)
PARTIDA = 2
f = "jugada6_"
e0, e1 = ESC("jugada6")
FX += VIVO("jugada6", "g2_j2", 70 - (T0(f + "0") - e0), "Transmisión oficial · CFO vs KC · partida 2", "CFO", "Minuto 6")
a = T0(f + "0")
FX += REB("g2_j2", a, 70, 40)
FX += [CLIP("g2_j1", a + 1.2, NX(f + "0"), 12, 28),
       tar(W(f + "0", "sangre"), NX(f + "0"), "Primera sangre", "Doggo sobre Caliste · 02:11", A, logo="CFO", x=.5, y=.84, tam=48),
       gris(W(f + "0", "Caliste"), "Caliste", "KC", "02:11", .1, NX(f + "0")),
       dict(tipo="destello", en=W(f + "0", "sangre"), fuerza=.45)]
a = T0(f + "1")
w = W(f + "1", "Pausa")
FX += [CLIP("g2_j2", a, w, 40, 49)] if w - a > .2 else []
FX += PZ("g2_j2", w, NX(f + "1"), 49, [
    an(.47, .47, "Busio", "LULU", "KC", W(f + "1", "Busio"), "Lulu", lado="der"),
    an(.42, .68, "Doggo", None, "CFO", W(f + "1", "Doggo"), "Caitlyn", lado="der"),
    an(.39, .33, "Yike", None, "KC", W(f + "1", "Doggo") + .3, "Pantheon", lado="izq", r=40),
    an(.57, .31, "Caliste", None, "KC", W(f + "1", "Doggo") + .5, "Yunara", lado="der", r=40),
    texto("YA VIENEN", "SHAD0W Y POUT", .18, .6, W(f + "1", "llega"), color=Y),
])
a = T0(f + "2")
FX += [CLIP("g2_j2", a, NX(f + "2"), 49, 70),
       gris(W(f + "2", "Busio"), "Busio", "KC", "06:14", .1, NX(f + "2")), gris(W(f + "2", "Yike"), "Yike", "KC", "06:24", .26, NX(f + "2")),
       tar(W(f + "2", "Dos"), NX(f + "2"), "2 por 1 en la pelea", "3 a 1 en el marcador · dragón Hextech", A, logo="CFO", x=.72,
           y=.84, tam=44)]
a = T0(f + "3")
w = W(f + "3", "torres")
FX += [CLIP("g2_j3", a, NX(f + "3"), 12, 60), acel(a, NX(f + "3")),
       gris(W(f + "3", "Busio"), "Busio", "KC", "09:48", .1, W(f + "3", "desde")),
       tar(w, NX(f + "3"), "4 torres a 0", "10:23 · 12:19 · 15:21 · 16:44", A, logo="CFO", dato="4-0", x=.72, y=.84, tam=44)]
a = T0(f + "4")
FX += [J("g2_j4", a, e1, 0),
       mg(L.ficha_jugador(EQ("CFO"), "CFO", EQ("CFO"), 20, [("Ventaja de oro", "+4,8K", .96), ("Torres", "4 a 0", .8),
                                                           ("Dragones", "2", .5)], color="azul", sub="Minuto 20"),
          W(f + "4", "veinte"), e1, [W(f + "4", "cinco"), W(f + "4", "cinco") + .4, W(f + "4", "cinco") + .8], y=.5,
          nombre="ficha CFO min 20")]

# ================================================================== JUGADA 7 · la pelea de mitad de partida (g2_j4) ★ 3D
f = "jugada7_"
e0, e1 = ESC("jugada7")
FX += VIVO("jugada7", "g2_j4", 35 - (T0(f + "0") - e0), "Transmisión oficial · partida 2", "KC", "Minuto 20")
a = T0(f + "0")
FX += REB("g2_j4", a, 35, 2)
FX += [CLIP("g2_j4", a + 1.2, NX(f + "0"), 2, 15),
       tar(W(f + "0", "previa"), W(f + "0", "aqui"), "La clave de la previa", "La pelea de mitad de partida", "oro", x=.5, y=.2, tam=50),
       tar(W(f + "0", "Baron"), NX(f + "0"), "Barón · 20:00", "Acaba de aparecer", "oro", x=.24, y=.17, tam=40)]
b = T0(f + "1")
FX += PZ("g2_j4", b, NX(f + "1"), 15, [
    dict(tipo="foco", en=b + .2, k=.35),
    an(.175, .56, "Doggo", "Y KINO", "CFO", W(f + "1", "cada"), "Caitlyn", lado="der"),
    an(.43, .57, "Busio", "SE ADELANTA", "KC", W(f + "1", "cada") + .3, "Lulu", lado="der"),
    an(.43, .39, "kyeahoo", None, "KC", W(f + "1", "cada") + .6, "Viktor", lado="der", r=40),
    texto("CFO: +4,8K", None, .2, .3, W(f + "1", "oro"), color=Y),
    texto("CANNA LLEGA", "POR LA RETAGUARDIA", .74, .62, W(f + "1", "cuatro"), color=Y),
    intencion([(.95, .70), (.80, .66), (.62, .60)], R, W(f + "1", "cuatro"), None),
], d3="j7a")
a = T0(f + "2")
FX += [CLIP("g2_j4", a, NX(f + "2"), 15, 28),
       peg(W(f + "2", "Canna"), "Canna", "Canna", R, "KC", "Camille", dur=NX(f + "2") - W(f + "2", "Canna"), x=.85, y=.5, tam=360),
       gris(W(f + "2", "cae"), "Doggo", "CFO", "20:04", .1, NX(f + "2")),
       dict(tipo="destello", en=W(f + "2", "cae"), fuerza=.45)]
b = T0(f + "3")
FX += PZ("g2_j4", b, NX(f + "3"), 28, [
    an(.56, .56, "Yike", "MATÓ A REST", "KC", W(f + "3", "Yike"), "Pantheon", lado="der"),
    an(.31, .55, "Canna", "SOBRE KINO", "KC", W(f + "3", "Canna"), "Camille", lado="izq"),
    an(.70, .59, "Busio", None, "KC", W(f + "3", "Canna") + .3, "Lulu", lado="der", r=38),
    texto("REST CAE", "20:10", .5, .27, W(f + "3", "Rest"), color=Y),
], d3="j7b")
a = T0(f + "4")
FX += [CLIP("g2_j4", a, e1, 28, 66), acel(a, e1),
       gris(a + .2, "Kino", "CFO", "20:14", .1, e1), gris(W(f + "4", "POUT"), "POUT", "CFO", "20:44", .26, e1),
       dict(tipo="destello", en=W(f + "4", "Cuatro"), fuerza=.5),
       tar(W(f + "4", "Cuatro"), e1, "4 por 0 para Karmine", "De +4,8K a menos de +3K", R, logo="KC", dato="4-0", x=.72, y=.84, tam=46)]
e0, e1 = ESC("jugada7_rep")
FX += LENTA("g2_j4", e0, e1, 23, .45, zoom=(1.35, .3, .5))
FX += [tar(W("jugada7_rep_0", "menos"), e1, "En menos de un minuto", "+4,8K → +2,2K", R, logo="KC", x=.5, y=.84, tam=48)]

# ================================================================== JUGADA 8 · el Barón de CFO, la pelea 4 por 4 y la pausa (g2_j5)
f = "jugada8_"
e0, e1 = ESC("jugada8")
FX += VIVO("jugada8", "g2_j5", 48 - (T0(f + "0") - e0), "Transmisión oficial · partida 2", "CFO", "Minuto 24")
a = T0(f + "0")
FX += REB("g2_j5", a, 48, 5)
FX += [CLIP("g2_j5", a + 1.2, NX(f + "0"), 5, 50), acel(a + 1.2, NX(f + "0")),
       tar(W(f + "0", "dragones"), W(f + "0", "Doggo"), "CFO: 3 dragones", None, A, logo="CFO", x=.24, y=.17, tam=40),
       gris(W(f + "0", "Canna"), "Canna", "KC", "23:44", .1, W(f + "0", "asegura")),
       tar(W(f + "0", "asegura"), NX(f + "0"), "Barón para CFO", "24:17", A, logo="CFO", x=.5, y=.84, tam=48)]
b = T0(f + "1")
FX += PZ("g2_j5", b, NX(f + "1"), 50, [
    an(.18, .60, "kyeahoo", None, "KC", W(f + "1", "salida"), "Viktor", lado="der"),
    an(.40, .57, "Caliste", None, "KC", W(f + "1", "salida") + .3, "Yunara", lado="izq"),
    an(.58, .73, "POUT", None, "CFO", W(f + "1", "caos"), "Ryze", lado="der", r=40),
    texto("7 MUERTES", "EN 35 SEGUNDOS", .78, .3, W(f + "1", "siete"), color=Y),
])
a = T0(f + "2")
FX += [CLIP("g2_j5", a, NX(f + "2"), 50, 84),
       mg(L.versus((EQ("CFO"), "CFO"), (EQ("KC"), "KC"), "La pelea del Barón", "4 muertes por lado"), W(f + "2", "cuatro"),
          NX(f + "2"), [W(f + "2", "cuatro")], y=.42, nombre="versus 4-4")]
a = T0(f + "3")
FX += [J("g2_j5", a, e1, 84),
       tar(W(f + "3", "detiene"), e1, "Pausa · 25:02", "Problemas técnicos de Doggo · ~29 min", "oro", x=.5, y=.2, tam=52),
       peg(W(f + "3", "Doggo"), "Doggo", "Doggo", A, "CFO", "Problemas técnicos", dur=e1 - W(f + "3", "Doggo"), x=.83, y=.5, tam=340)]

# ================================================================== JUGADA 9 · alma, inhibidor y la pelea 3 por 1 (g2_j6, g2_j7)
f = "jugada9_"
e0, e1 = ESC("jugada9")
FX += VIVO("jugada9", "g2_j7", 27 - (T0(f + "0") - e0), "Transmisión oficial · partida 2", "KC", "Minuto 30")
a = T0(f + "0")
FX += REB("g2_j7", a, 27, 13)
FX += [CLIP("g2_j6", a + 1.2, NX(f + "0"), 4, 25),
       tar(W(f + "0", "alma"), NX(f + "0"), "Alma del Océano", "CFO · 27:57", A, logo="CFO", x=.5, y=.84, tam=48)]
a = T0(f + "1")
FX += [CLIP("g2_j6", a, NX(f + "1"), 25, 96), acel(a, NX(f + "1"), "» x7"),
       gris(W(f + "1", "Canna"), "Canna", "KC", "28:34", .1, W(f + "1", "inhibidor")),
       tar(W(f + "1", "inhibidor"), NX(f + "1"), "CFO +3,7K", "Alma · inhibidor · 6 torres a 2", A, logo="CFO", x=.72, y=.84, tam=46)]
b = T0(f + "2")
FX += PZ("g2_j7", b, NX(f + "2"), 19, [
    an(.37, .27, "Rest", None, "CFO", W(f + "2", "Rest"), "Ambessa", lado="izq"),
    an(.58, .52, "kyeahoo", None, "KC", W(f + "2", "voltea"), "Viktor", lado="der"),
    an(.63, .42, "Busio", None, "KC", W(f + "2", "voltea") + .3, "Lulu", lado="der", r=38),
    texto("CALISTE SE LANZA", None, .2, .6, W(f + "2", "Caliste"), color=Y),
    texto("EL BARÓN", "ACABA DE REAPARECER", .8, .2, W(f + "2", "Baron"), color=Y),
])
a = T0(f + "3")
FX += [J("g2_j7", a, NX(f + "3"), 19, (26 - 19) / (NX(f + "3") - a)), x2(a, NX(f + "3"), "CÁMARA LENTA"),
       gris(W(f + "3", "Doggo"), "Doggo", "CFO", "30:20", .1, NX(f + "3")), gris(W(f + "3", "Kino"), "Kino", "CFO", "30:21", .26, NX(f + "3")),
       gris(W(f + "3", "Rest"), "Rest", "CFO", "30:22", .42, NX(f + "3")),
       dict(tipo="destello", en=W(f + "3", "Tres"), fuerza=.5),
       tar(W(f + "3", "Tres"), NX(f + "3"), "3 por 1 para Karmine", None, R, logo="KC", dato="3-1", x=.75, y=.84, tam=46)]
a = T0(f + "4")
FX += [CLIP("g2_j7", a, e1, 26, 88), acel(a, e1),
       tar(W(f + "4", "Baron"), W(f + "4", "minuto"), "Barón para Karmine", "≈ 30:56", R, logo="KC", x=.5, y=.84, tam=48),
       tar(W(f + "4", "minuto"), e1, "Oro empatado", "Minuto 31", "oro", x=.5, y=.84, tam=48)]
e0, e1 = ESC("jugada9_rep")
FX += LENTA("g2_j7", e0, e1, 25, .45, zoom=(1.3, .45, .45))
FX += [peg(W("jugada9_rep_0", "Rest"), "Rest", "Rest", A, "CFO", "1 asesinato · 3 muertes y un Barón",
           dur=e1 - W("jugada9_rep_0", "Rest"), x=.83, y=.5, tam=340)]

# ================================================================== JUGADA 10 · el dragón ancestral (g2_j8) ★ 3D
f = "jugada10_"
e0, e1 = ESC("jugada10")
FX += VIVO("jugada10", "g2_j8", 123 - (T0(f + "0") - e0), "Transmisión oficial · partida 2", "KC", "Minuto 35")
a = T0(f + "0")
FX += REB("g2_j8", a, 123, 60)
FX += [CLIP("g2_j8", a + 1.2, NX(f + "0"), 60, 84),
       tar(W(f + "0", "oro"), W(f + "0", "ancestral"), "Karmine, arriba en oro", "Por primera vez desde el minuto 2", R, logo="KC",
           x=.76, y=.17, tam=40),
       tar(W(f + "0", "ancestral"), NX(f + "0"), "Dragón ancestral", "En el mapa desde el 33:55", "oro", x=.76, y=.17, tam=40)]
b = T0(f + "1")
FX += PZ("g2_j8", b, NX(f + "1"), 84, [
    dict(tipo="foco", en=b + .2, k=.38),
    an(.54, .40, "Shad0w", "SOLO EN EL RÍO", "CFO", W(f + "1", "Shad0w"), "LeeSin", lado="der"),
    an(.13, .63, "POUT", "LEJOS", "CFO", W(f + "1", "Lee") + .2, "Ryze", lado="der", r=38),
    texto("UN CENTINELA LO DELATA", None, .74, .62, W(f + "1", "encuentra"), color=Y),
], d3="j10a")
a = T0(f + "2")
FX += [CLIP("g2_j8", a, NX(f + "2"), 84, 108),
       gris(W(f + "2", "Shad0w"), "Shad0w", "CFO", "35:32", .1, NX(f + "2")),
       dict(tipo="destello", en=W(f + "2", "Shad0w"), fuerza=.45),
       tar(W(f + "2", "cuatro"), NX(f + "2"), "4 contra 5", "Sin jungla, por el ancestral", R, logo="KC", x=.72, y=.84, tam=46)]
b = T0(f + "3")
FX += PZ("g2_j8", b, NX(f + "3"), 108, [
    an(.38, .31, "Caliste", "ENTRA", "KC", W(f + "3", "Caliste"), "Yunara", lado="izq"),
    an(.43, .36, "POUT", None, "CFO", W(f + "3", "Yunara"), "Ryze", lado="der", r=38),
    an(.31, .49, "Yike", None, "KC", W(f + "3", "Yunara") + .3, "Pantheon", lado="izq", r=38),
], d3="j10b")
a = T0(f + "4")
FX += [CLIP("g2_j8", a, NX(f + "4"), 108, 118),
       gris(W(f + "4", "Rest"), "Rest", "CFO", "35:53", .1, NX(f + "4")), gris(W(f + "4", "POUT"), "POUT", "CFO", "35:55", .26, NX(f + "4")),
       gris(W(f + "4", "Canna"), "Canna", "KC", "35:56", .42, NX(f + "4")),
       tar(W(f + "4", "ancestral"), NX(f + "4"), "Ancestral para Karmine", "35:57", R, logo="KC", x=.5, y=.84, tam=48),
       dict(tipo="destello", en=W(f + "4", "ancestral"), fuerza=.55)]
a = T0(f + "5")
w = W(f + "5", "nexo")
FX += [CLIP("g2_j8", a, w, 118, 176), acel(W(f + "5", "base"), w),
       gris(W(f + "5", "Doggo"), "Doggo", "CFO", "35:57", .1, W(f + "5", "base")),
       gris(W(f + "5", "Kino"), "Kino", "CFO", "35:59", .26, W(f + "5", "base")),
       tar(W(f + "5", "cinco"), W(f + "5", "base"), "5 por 1 y el ancestral", None, R, logo="KC", dato="5-1", x=.72, y=.84, tam=46),
       dict(tipo="destello", en=w, fuerza=.6),
       J("g2_j8", w, e1, 176),
       mg(L.versus((EQ("KC"), "KC"), (EQ("CFO"), "CFO"), "Karmine 2 · CFO 0", "36:58 · KC sigue vivo", ganador=0), W(f + "5", "Dos"),
          e1, [W(f + "5", "Dos")], y=.45, nombre="versus 2-0")]
e0, e1 = ESC("jugada10_rep")
FX += LENTA("g2_j8", e0, e1, 117, .45, zoom=(1.3, .45, .45))
FX += [mg(L.calendario("Lo que tuvo CFO", [("Min 20", "+4,8K", "azul"), ("24:17", "Barón", "azul"), ("27:57", "Alma", "azul"),
                                            ("29:07", "Inhibidor", "azul")]),
          W("jugada10_rep_0", "llego"), W("jugada10_rep_0", "perdio"),
          [W("jugada10_rep_0", "cinco"), W("jugada10_rep_0", "Baron"), W("jugada10_rep_0", "alma"), W("jugada10_rep_0", "inhibidor")],
          y=.5, nombre="calendario CFO"),
       tar(W("jugada10_rep_0", "perdio"), e1, "Y perdió en tres peleas", "20:04 · 30:20 · 35:32", R, logo="KC", x=.5, y=.84, tam=48)]

# ================================================================== PARTIDA 2 EN ORO
g = "curva2_"
FX += [mg(L.calendario("La partida 2 en oro", [("Min 20", "CFO\n+4,8K", "azul"), ("Min 29", "CFO\n+3,7K", "azul"),
                                                ("Min 30", "La pelea\n3 por 1", "rojo"), ("Min 33", "KC arriba", "rojo"),
                                                ("Final", "KC\n+7K", "rojo")]),
          T0(g + "0"), T1(g + "0") + .3,
          [W(g + "0", "veinte"), W(g + "0", "inhibidor"), W(g + "0", "treinta"), W(g + "0", "Karmine"), W(g + "0", "Siete")],
          y=.5, nombre="calendario g2")]

# ================================================================== PREDICCIONES DE LA PREVIA
g = "predicciones_"
FX += [tar(T0(g + "0"), W(g + "0", "Uno"), "Las 3 claves de la previa", "¿Se cumplieron?", "oro", x=.5, y=.2, tam=66),
       tar(W(g + "0", "Uno"), T1(g + "0") + .3, "1 · La pelea de mitad de partida", "SE CUMPLIÓ · minuto 20", "oro", x=.5, y=.8, tam=50),
       tar(T0(g + "1"), T1(g + "1") + .3, "2 · Los objetivos", "Alma para CFO… ancestral para KC", "oro", x=.5, y=.8, tam=50),
       peg(W(g + "1", "alma", 1), CARGA("Karma"), "CFO", A, "CFO", "Alma del Océano", dur=W(g + "1", "Otra") - W(g + "1", "alma", 1),
           x=.25, y=.45, tam=340),
       peg(W(g + "1", "ancestral", 2), CARGA("Viktor"), "Karmine", R, "KC", "Dragón ancestral", dur=T1(g + "1") - W(g + "1", "ancestral", 2) + .3,
           x=.75, y=.45, tam=340, sello=("OTRA VEZ", 0)),
       tar(T0(g + "2"), T1(g + "2") + .3, "3 · El Fearless", None, "oro", x=.5, y=.8, tam=50),
       peg(W(g + "2", "Rest"), CARGA("Rumble"), "Rest", R, "CFO", "Rumble · gastado en la 1", dur=W(g + "2", "Shad0w") - W(g + "2", "Rest"),
           x=.3, y=.45, tam=340, gris=True),
       peg(W(g + "2", "Pantheon"), CARGA("Pantheon"), "Yike", R, "KC", "4/2/12", dur=T1(g + "2") - W(g + "2", "Pantheon") + .3,
           x=.7, y=.45, tam=340)]


# ================================================================== LA BOLETA (MG nuevo: aciertos ✓ / errores ✗)
def BOL(k0, k1, jug, eq, sub, filas, marcas):
    col = "azul" if eq == "KC" else "rojo"
    return mg(L.boleta(JUG(jug), jug, EQ(eq), col, sub, filas), k0, k1, marcas, y=.5, nombre="boleta " + jug)


g = "boleta_kc_"
FX += [tar(T0(g + "0"), W(g + "0", "kyeahoo"), "La boleta", "Karmine Corp", A, logo="KC", x=.5, y=.2, tam=70),
       BOL(W(g + "0", "kyeahoo"), T1(g + "0") + .3, "kyeahoo", "KC", "Mid · 12/1/19 en la serie",
           [(True, "12 asesinatos, 1 sola muerte"), (True, "0 muertes en la partida 2"), (None, "La figura de la serie")],
           [W(g + "0", "doce"), W(g + "0", "Cero"), W(g + "0", "figura")]),
       BOL(T0(g + "1"), T1(g + "1") + .3, "Caliste", "KC", "Tirador",
           [(True, "Partida 1 sin morir con Tristana"), (False, "Primera sangre de la partida 2")],
           [W(g + "1", "terminó"), W(g + "1", "error")]),
       BOL(T0(g + "2"), W(g + "2", "Yike"), "Canna", "KC", "Top",
           [(True, "La entrada al dragón Químico"), (True, "La pelea del minuto 20")], [W(g + "2", "entrada"), W(g + "2", "veinte")]),
       BOL(W(g + "2", "Yike"), T1(g + "2") + .3, "Yike", "KC", "Jungla",
           [(True, "Primera sangre de la serie"), (True, "Cazó a Shad0w antes del ancestral")],
           [W(g + "2", "sangre"), W(g + "2", "cazo")]),
       BOL(T0(g + "3"), T1(g + "3") + .3, "Busio", "KC", "Soporte",
           [(True, "17 asistencias en la partida 2"), (False, "3 muertes antes del minuto 10")],
           [W(g + "3", "diecisiete"), W(g + "3", "tres")])]
g = "boleta_cfo_"
FX += [tar(T0(g + "0") - .1, W(g + "0", "Shad0w"), "La boleta", "CTBC Flying Oyster", R, logo="CFO", x=.5, y=.2, tam=70),
       BOL(W(g + "0", "Shad0w"), T1(g + "0") + .3, "Shad0w", "CFO", "Jungla",
           [(True, "La mejor lectura: la cacería de Busio"), (True, "5 asesinatos en la partida 2"), (False, "6 muertes en la partida 1")],
           [W(g + "0", "lectura"), W(g + "0", "cinco"), W(g + "0", "seis")]),
       BOL(T0(g + "1"), T1(g + "1") + .3, "Doggo", "CFO", "Tirador",
           [(False, "0 % de participación en la partida 1"), (True, "Primera sangre y 40 % del daño en la 2")],
           [W(g + "1", "cero"), W(g + "1", "primera")]),
       BOL(T0(g + "2"), W(g + "2", "Kino"), "POUT", "CFO", "Mid",
           [(True, "Los 3 asesinatos de CFO en la partida 1")], [W(g + "2", "tres")]),
       BOL(W(g + "2", "Kino"), T1(g + "2") + .3, "Kino", "CFO", "Soporte",
           [(False, "Un nivel abajo en el minuto 9"), (False, "Definitiva gastada antes del dragón")],
           [W(g + "2", "nivel"), W(g + "2", "definitiva")]),
       BOL(T0(g + "3"), T1(g + "3") + .3, "Rest", "CFO", "Top",
           [(False, "La Teleportación del dragón Químico"), (False, "La entrada del minuto 30"), (False, "7 muertes y 1 asesinato")],
           [W(g + "3", "Teleportacion"), W(g + "3", "entrada"), W(g + "3", "siete")])]

# ================================================================== LOS NÚMEROS
g = "numeros_"
FX += [tar(T0(g + "0"), W(g + "0", "treinta"), "Los números de la serie", None, "oro", x=.5, y=.2, tam=74),
       mg(L.ranking("La serie · asesinatos", [(EQ("KC"), "Karmine Corp", "39", "asesinatos · 2 partidas", "azul"),
                                              (EQ("CFO"), "CTBC Flying Oyster", "15", "asesinatos · 7 torres, todas en la partida 2", "rojo")]),
          W(g + "0", "treinta"), T1(g + "0") + .3, [W(g + "0", "treinta"), W(g + "0", "quince")], y=.5, nombre="ranking serie")]

# ================================================================== QUÉ SIGUE
g = "sigue_"
FX += [mg(L.eliminado(EQ("CFO"), "CTBC Flying Oyster", "1-3 · fuera del Mundial"), T0(g + "0"), T1(g + "0") + .3,
          [W(g + "0", "derrotas"), W(g + "0", "eliminado")], y=.47, nombre="eliminado CFO"),
       mg(L.calendario("Lo que viene", [("29 oct", "KC 2-2", "azul"), ("31 oct", "Ronda 5\na muerte", "rojo"),
                                        ("Si gana", "Cuartos\nde final", "oro")]),
          T0(g + "1"), T1(g + "1") + .3, [W(g + "1", "dos"), W(g + "1", "sabado"), W(g + "1", "cuartos")], y=.5, nombre="calendario KC")]

# ================================================================== CIERRE
g = "cierre_"
FX += [tar(T0(g + "0"), W(g + "0", "alcanza"), "¿Cuál fue la jugada clave?", "Déjalo en los comentarios", "oro", x=.5, y=.2, tam=62),
       tar(W(g + "0", "alcanza"), T1(g + "0") + .5, "¿Le alcanza a Karmine?", "Nos vemos el sábado", R, logo="KC", x=.5, y=.8, tam=56)]
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
