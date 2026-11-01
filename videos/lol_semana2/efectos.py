# -*- coding: utf-8 -*-
"""Capa de EFECTOS del resumen semanal de la Worlds 2026 (estilo análisis táctico, docs/estilo_analisis_tactico.md), formato de
videos/cfo_kc_jugadas/efectos.py. Fuentes: medios/_fuente/<n>.mp4 y, para T1-KOI y KC-CFO, las de sus videos (EXT, ruta absoluta).
Coordenadas y relojes: investigacion/datos_{t1ko,lyig,kccf,blte,lotl,g2hl}.md (nada inventado: sin coordenada = texto). Colores = lado
del mapa de cada partida (AZUL). Tiempos anclados a la voz (T0/T1/W/NX). SIN SPOILER en el gancho. ACTO B: se añade tras `tabla4`.
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


EXT = {"t1_g1j4": ("t1_koi_worlds", "g1_j4"), "t1_g1j5": ("t1_koi_worlds", "g1_j5"), "t1_g2j1": ("t1_koi_worlds", "g2_j1"),
       "t1_g2j2": ("t1_koi_worlds", "g2_j2"), "kc_g1j4": ("cfo_kc_jugadas", "g1_j4"), "kc_g1j8": ("cfo_kc_jugadas", "g1_j8"),
       "kc_g2j4": ("cfo_kc_jugadas", "g2_j4"), "kc_g2j5": ("cfo_kc_jugadas", "g2_j5"), "kc_g2j8": ("cfo_kc_jugadas", "g2_j8")}


def fuente(n):
    if n in EXT:
        return os.path.abspath(os.path.join(_D, "..", EXT[n][0], "medios", "_fuente", EXT[n][1] + ".mp4"))
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


def x2(de, a, texto="» x2", x=.09):
    return tar(de, a, texto, None, "oro", x=x, y=.13, tam=28)



# ───────────────────────────────────────── piezas de las jugadas ─────────────────────────────────────────────────────────
TIEMPOS_MESAS = {}


def CLIP(n, de, a, t0, t1, **kw):
    """llena [de, a) con el tramo t0→t1 SIN pasar de x1 (31-oct-2026, nunca cámara rápida): si no cabe, lo que se ve es el FINAL a x1,
    y así sigue cuadrando con la pausa que viene detrás"""
    v = (t1 - t0) / (a - de)
    return J(n, de, a, t0, v, **kw) if v <= 1.05 else J(n, de, a, t1 - (a - de), 1.0, **kw)


def TRAMO(n, a, b, t0, t1):
    """tramo del VOD que arranca donde quedó el anterior: x1 como máximo; si t1 no llega a tiempo, salto por CORTE a mitad del tramo
    (lo que sigue al momento anterior + lo que lleva al siguiente). t1 = None: x1 sin más."""
    dur = b - a
    if t1 is None:
        return [J(n, a, b, t0, 1.0)]
    v = (t1 - t0) / dur
    if v <= 1.05:
        return [J(n, a, b, t0, v)]
    if dur < 1.5:
        return [J(n, a, b, t1 - dur, 1.0)]
    m = a + dur / 2
    return [J(n, a, m, t0, 1.0), J(n, m, b, t1 - (b - m), 1.0)]


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


def repeticion(de, a, sub="Cámara lenta"):
    return [tar(de, a, "Repetición", sub, R, x=.3, y=.13, tam=34), dict(tipo="destello", en=de, fuerza=.35)]



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
AZUL = set()          # equipos del lado azul en la partida en curso: el color sigue al lado del mapa


def COLOR(eq):
    return A if eq in AZUL else R


K = {"t1_g1j4": 1970, "t1_g1j5": 2294, "t1_g2j1": 474.9, "t1_g2j2": 1109.9, "kc_g1j4": 656, "kc_g1j8": 1566, "kc_g2j4": 1182,
     "kc_g2j5": 1412, "kc_g2j8": 2041, "lyig_j1": 1659, "lyig_j2": 130, "lyig_j3": 718.5, "lyig_ace": 1487.5, "blte_j1": 1519,
     "blte_j2": 2152, "blte_j3": 1706, "blte_g3": 1392, "lotl_j1": 2063, "lotl_j2": 2364.5, "lotl_j3": 2289, "lotl_g1": 723,
     "lotl_g2": 2158, "lotl_zest": 2767, "g2hl_j1": 1279.7, "g2hl_j2": 906.7, "g2hl_j3": 822.7}


def H(n, t):
    s = int(t + K[n])
    return f"{s // 60:02d}:{s % 60:02d}"


def PZ(n, de, a, t, els, d3=None):
    """pausa con el reloj del HUD de ese cuadro"""
    return P2(n, de, a, t, els, H(n, t), d3)


def REB(n, de, t_desde, t_hasta, dur=1.2):
    """REBOBINANDO rotulado: el clip va hacia atrás de t_desde a t_hasta en `dur` s"""
    return [J(n, de, de + dur, t_desde, -(t_desde - t_hasta) / dur), rebobinar(de, de + dur, H(n, t_hasta)),
            dict(tipo="destello", en=de + dur, fuerza=.4)]


def REBX(n, a, t_desde, b, t_fin):
    """REBOBINANDO + VOD a x1 que llega al cuadro t_fin en el instante b: rebobina justo hasta lo que cabe, sin acelerar"""
    t = t_fin - (b - a - 1.2)
    return [*REB(n, a, t_desde, t), J(n, a + 1.2, b, t, 1.0)]


AUD_VIVOS = []          # (id de escena, fuente, segundo inicial, e0, f0): vivos_audio.py corta de aquí la narración original


def VIVO(sid, n, t, sub, logo, minuto):
    """tramo EN VIVO (beat sin voz con la narración original): de e0 a la primera frase, desde el segundo t de la fuente"""
    e0, _ = ESC(sid)
    f0 = T0(sid + "_0")
    AUD_VIVOS.append((sid, fuente(n), t, round(e0, 3), round(f0, 3)))
    return [J(n, e0, f0, t), en_vivo(e0 + .3, sub, logo),
            tar(e0 + .3, e0 + 5.5, minuto, "Mírala primero en vivo", "oro", x=.76, y=.17, tam=40)]


def LENTA(n, de, a, t_fin, vel=.45, zoom=None, sub="Cámara lenta"):
    """repetición en cámara lenta que TERMINA en el cuadro t_fin"""
    kw = dict(zoom=zoom, zoom0=(1.0, .5, .5), zoom_dur=1.2) if zoom else {}
    return [J(n, de, a, t_fin - vel * (a - de), vel, **kw), *repeticion(de, de + 3.5, sub)]


def gris(en, jug, eq, sub, x, a=None, y=.62, tam=190):
    col = COLOR(eq)
    return peg(en, jug, jug, col, eq, sub, dur=(a or en + 3.0) - en, x=x, y=y, tam=tam, gris=True)


def LEN(n, de, a, t0, t1):
    """t0→t1 en [de, a): rotula «CÁMARA LENTA» solo si de verdad lo es"""
    return [*TRAMO(n, de, a, t0, t1), *([x2(de, a, "CÁMARA LENTA")] if (t1 - t0) / (a - de) < .8 else [])]



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




def SYNC(n, pares):
    """pares [(instante, t_fuente)]: tramos encadenados del VOD para que cada muerte caiga cuando la voz la dice. Nada pasa de x1: el
    hueco lo dan ESPACIOS_VOZ y `post` (guion.py); lo que aun así no cabe salta por corte. t_fuente = None al final: x1 hasta ahí."""
    return [f for (a, t0), (b, t1) in zip(pares, pares[1:]) if b - a > .03 for f in TRAMO(n, a, b, t0, t1)]


def COM(cid):
    return os.path.join(_D, "pegatinas", f"com_{cid}.png")


def com(en, cid, dur, x=.5, y=.42, tam=980, giro_marcas=()):
    """captura del comentario REAL (texto exacto, nucleo/comentarios.py)"""
    return mg(L.pegatina(COM(cid), None, "oro", tam=tam), en, en + dur, giro_marcas, x=x, y=y, nombre="comentario " + cid[:8])


# ---- estilos de pegatina variados (REGLA DE ORO, nucleo/peg_estilos.py, tema gaming)
import peg_estilos as PE  # noqa: E402


def sil(en, jug, nombre=None, sub=None, dur=4.5, lado="izq", alto=640):
    """jugador SIN FONDO saliendo del borde, a media pantalla (fuera del análisis)"""
    fn = PE.silueta(JUG(jug), nombre, sub, alto=alto, encuadre=(0, 1), lado=lado, tema="gaming")
    x, y = PE.pos_silueta(fn, lado)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.35, nombre="pegatina " + jug, ver=1.2)


def cam(en, jug, nombre=None, dur=3.0, x=.09, y=.3, tam=210, ruta=None):
    """medallón para menciones rápidas: chico y en el borde durante el análisis"""
    return dict(tipo="mg", fn=PE.camafeo(ruta or JUG(jug), nombre or jug, tam, (.5, .3, 1.5), tema="gaming"), en=en, dur=dur, x=x, y=y,
                sale=.3, nombre="pegatina " + (nombre or jug), ver=1.0)


def banda(en, jug, nombre, sub, dur=4.0, y=.5, lado="der"):
    """tira de cine con la cara del jugador"""
    return dict(tipo="mg", fn=PE.banda(JUG(jug), nombre, sub, (.5, .36, 1.3), lado=lado, tema="gaming"), en=en, dur=dur, x=.5, y=y, sale=.35,
                nombre="pegatina " + jug, ver=1.2)


def abanico(de, a, fotos, marcas, x=.5, y=.5, tam=300, nombre="abanico"):
    """cartas que se abren cuando la voz enumera: fotos = [(ruta, etiqueta)]"""
    return dict(tipo="mg", fn=PE.abanico(fotos, tam, tema="gaming"), de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.35, nombre=nombre, ver=1.2)


def peor(de, a, categoria, jug, eq, datos, marcas, sub=None, sello="LO PEOR"):
    """MG «lo peor» (rojo y en gris, con sello)"""
    return mg(L.premio(categoria, JUG(jug), jug, EQ(eq), datos, color="rojo", sub=sub, sello=sello, gris=True), de, a, marcas, y=.5,
              nombre="premio " + jug)


def elim(de, a, eq, nombre, sub, marcas):
    return mg(L.eliminado(EQ(eq), nombre, sub), de, a, marcas, y=.47, nombre="eliminado " + eq)


def muro_2d(pts, en, color=Y):
    """el muro de Taliyah medido: línea gruesa sin punta sobre el cuadro congelado"""
    return dict(tipo="flecha", pts=pts, color=color, en=en, dur=.9, guion=False, ancho=15, punta=False)


TODOS = "DK GEN T1 MKOI LYON IG BLG TES KC CFO HLE G2 LOS TLAW TSW AL".split()
LOG = {c: EQ(c) for c in TODOS}
COLS = [("A cuartos", "verde"), ("2-1", "oro"), ("2-2", "oro"), ("1-2", "oro"), ("Eliminados", "rojo")]
R3 = [["DK", "GEN"], ["T1", "MKOI", "LYON", "IG", "BLG", "TES"], [], ["KC", "CFO", "HLE", "G2", "LOS", "TLAW"], ["TSW", "AL"]]
_N = None
R4a = [["DK", "GEN", "T1", "IG", "TES"], [_N, "MKOI", "LYON", _N, "BLG", _N], [], ["KC", "CFO", "HLE", "G2", "LOS", "TLAW"], ["TSW", "AL"]]
R4b = [R4a[0], R4a[1], [], ["KC", _N, "HLE", _N, "LOS", _N], ["TSW", "AL", "CFO", "TLAW", "G2"]]
R4c = [R4a[0], [], ["KC", "MKOI", "LOS", "LYON", "HLE", "BLG"], [], R4b[4]]      # los 3 cruces, cada uno en su fila

# ================================================================== GANCHO (SIN SPOILER: ni equipos ganadores ni nombres en los rótulos)
g = "gancho_"
a0 = T0(g + "1")
FX += [J("lotl_j3", 0.0, a0, 6.0),
       mg(L.apertura("LA SEMANA DECISIVA", "Worlds 2026 · rondas 4 y 5 de la fase suiza"), 0.0, T0(g + "0"), x=.5, y=.5, nombre="apertura"),
       dict(tipo="destello", en=0.15, fuerza=.7),
       tar(W(g + "0", "Seis"), T1(g + "0") + .2, "6 plazas", "Para cuartos de final", "oro", x=.2, y=.84, tam=54),
       tar(W(g + "0", "Catorce"), T1(g + "0") + .2, "14 equipos", "Todavía vivos", "oro", x=.5, y=.84, tam=54),
       tar(W(g + "0", "Nueve"), T1(g + "0") + .2, "9 series", "Todas a muerte o por el pase", "oro", x=.8, y=.84, tam=54)]
m, p, q = W(g + "1", "muro"), W(g + "1", "pausa"), W(g + "1", "jugada")
FX += [CLIP("blte_j3", a0, m, 23, 34), CLIP("lotl_j1", m, p, 14.0, 19.0), J("kc_g2j5", p, q, 84),
       CLIP("lyig_j2", q, T0(g + "2"), 22, 27),
       tar(W(g + "1", "cinco"), W(g + "1", "perder"), "+5 000 de oro", None, "oro", x=.5, y=.84, tam=56),
       tar(W(g + "1", "perder"), m, "En un minuto", "4 muertos y el Barón", R, x=.5, y=.84, tam=56),
       tar(m, p, "Un muro", "Parte a un equipo por la mitad", "oro", x=.5, y=.84, tam=56),
       tar(p, q, "29 minutos de pausa", "En plena serie", "oro", x=.5, y=.84, tam=56),
       tar(q, T0(g + "2"), "Minuto 2", "La jugada que decidió quién pasaba", "oro", x=.5, y=.84, tam=56),
       dict(tipo="destello", en=m, fuerza=.45), dict(tipo="destello", en=p, fuerza=.35), dict(tipo="destello", en=q, fuerza=.35)]
b = T0(g + "2")
c = W(g + "2", "Aqui")
FX += [CLIP("t1_g1j4", b, T0(g + "3"), 0, 28),
       com(W(g + "2", "Julio"), "UgwypMnI-accuZuSYMJ4AaABAg", T1(g + "2") - W(g + "2", "Julio") + .2, x=.5, y=.38, tam=1060),
       tar(W(g + "2", "Todos"), T1(g + "2") + .2, "Todos los comentarios se leen", "Este video se hizo con ellos", "oro", x=.5, y=.84, tam=54)]
b = T0(g + "3")
FX += [CLIP("g2hl_j2", b, ESC("gancho")[1], 15, 28),
       mg(L.menu([(ART("Orianna"), "Las mejores jugadas", "azul"), (ART("Olaf"), "Lo mejor y lo peor", "rojo"),
                  (ART("Taliyah"), "Los jugadores", "amarillo"), (ART("Swain"), "Los cuartos de final", "oro")]),
          b, ESC("gancho")[1], [W(g + "3", "mejores"), W(g + "3", "mejor", 1), W(g + "3", "jugadores"), W(g + "3", "cuartos")], y=.5,
          nombre="menu")]

# ================================================================== CORRECCIONES
g = "correcciones_"
e0, e1 = ESC("correcciones")
b = T0(g + "1")
FX += [J("lyig_j1", e0, b, 37.0), J("lyig_j3", b, e1, 40.0, .5),
       com(W(g + "0", "Rodolfo"), "UgyZTKk5Cq0R2nYl7zN4AaABAg", T1(g + "0") - W(g + "0", "Rodolfo") + .2, x=.5, y=.3, tam=900),
       tar(W(g + "0", "organizacion"), T1(g + "0") + .2, "LYON", "Organización mexicana · juega en la LCS", "oro", logo="LYON", x=.5, y=.84, tam=56),
       com(W(g + "1", "comentario"), "Ugykg5d4Nn9MJAorVLd4AaABAg", e1 - W(g + "1", "comentario") - .2, x=.5, y=.3, tam=820),
       tar(W(g + "1", "Mensaje"), e1 - .1, "Mensaje recibido", "Esa palabra se queda en el campo", "oro", x=.5, y=.84, tam=56)]

# ================================================================== DÓNDE ESTÁBAMOS (tabla tras la ronda 3)
g = "donde_"
e0, e1 = ESC("donde")
b = T0(g + "2")
FX += [CLIP("kc_g1j4", e0, b, 0, 22), J("t1_g2j2", b, e1, 8.0),
       mg(L.tablero_suizo("Así llegamos a esta semana", COLS, LOG, [R3]), e0 + .1, b, [], y=.5, nombre="tablero R3"),
       tar(W(g + "2", "Todo"), W(g + "2", "Fearless"), "Al mejor de 3", "Gana quien llegue a dos", "oro", x=.5, y=.84, tam=56),
       tar(W(g + "2", "Fearless"), e1, "Fearless", "Campeón usado en la serie, no se repite", "oro", x=.5, y=.84, tam=56),
       peg(W(g + "2", "Fearless") + .2, CARGA("Orianna"), "Orianna", "oro", None, "Ya usada", dur=e1 - W(g + "2", "Fearless") - .3, x=.14, y=.42,
           tam=380, gris=True, sello=("NO SE REPITE", 0))]

# ================================================================== MIÉRCOLES · T1 vs MOVISTAR KOI
AZUL = {"T1"}
g = "t1ko_res_"
e0, e1 = ESC("t1ko_res")
b = T0(g + "1")
FX += [J("t1_g1j4", e0, b, 30.0), CLIP("t1_g1j5", b, e1, 0, 25),
       tar(e0 + .15, W(g + "0", "Abre"), "Miércoles", "28 de octubre", "oro", x=.5, y=.17, tam=66),
       vs(W(g + "0", "Abre"), T1(g + "0") + .2, "T1", "MKOI", "Por el pase", "El que gana, a cuartos", y=.42),
       sil(W(g + "0", "cuarto"), "Faker", "Faker", None, dur=T1(g + "0") - W(g + "0", "cuarto") + .2, lado="izq", alto=560),
       tar(W(g + "0", "cuarto"), T1(g + "0") + .2, "Busca su 4.º título seguido", None, A, logo="T1", x=.76, y=.17, tam=40),
       mg(L.calendario("Partida 1: el oro, tres vueltas", [("Min 9", "KOI\n+1,7K", "rojo"), ("Min 26", "T1\n+5,8K", "azul"), ("Min 37", "KOI\n+2,1K", "rojo")]),
          b + .1, e1, [W(g + "1", "KOI"), W(g + "1", "T1"), W(g + "1", "otra")], y=.5, nombre="calendario oro t1ko")]

g = "t1ko_g1_"
n = "t1_g1j5"
e0, e1 = ESC("t1ko_g1")
FX += VIVO("t1ko_g1", n, 52, "Transmisión oficial · T1 vs KOI · partida 1", "T1", "Minuto 39")
a = T0(g + "0")
ta = 52 + (a - e0)
b, c = W(g + "0", "minuto"), W(g + "0", "Cinco")
p = W(g + "0", "todo", fin=True) + .1          # acaba «se lanzó con todo»: ahí sigue el VOD, a x1, con la narración original
FX += REBX(n, a, ta, b, 52)
FX += [peg(a + 1.3, "Doran", "Doran", A, "T1", "10/0/13 · no murió en la serie", dur=b - a - 1.0, x=.13, y=.56, tam=250)]
FX += PZ(n, b, p, 52, [
    dict(tipo="foco", en=b + .1, k=.4),
    texto("DORAN", "SE LANZA CON TODO", .68, .66, b + .3, color=A, icono="Ambessa"),
    flecha([(.62, .75), (.53, .67), (.45, .60)], A, b + .5, None, dur=.7),
    an(.44, .58, "Alvaro", None, "MKOI", W(g + "0", "abajo"), "Alistar", lado="izq", r=40),
    an(.23, .74, "Elyoya", None, "MKOI", W(g + "0", "abajo") + .3, "Qiyana", lado="der", r=40),
])
FX += [tar(W(g + "0", "mil"), p, "KOI +1,5K", "39:04", R, logo="MKOI", x=.76, y=.17, tam=40)]
FX += SYNC(n, [(p, 52), (W(g + "0", "alma"), 61.6), (W(g + "0", "nexo"), 96), (e1, 101)])
FX += [gris(c + .1, "Supa", "MKOI", "39:09", .08, W(g + "0", "nexo")),
       gris(c + .5, "Jojopyun", "MKOI", None, .21, W(g + "0", "nexo")), gris(c + .9, "Alvaro", "MKOI", None, .34, W(g + "0", "nexo")),
       dict(tipo="destello", en=c, fuerza=.5),
       tar(W(g + "0", "alma"), e1, "5 por 0", "Alma y nexo", A, logo="T1", dato="5-0", x=.72, y=.84, tam=46)]

g = "t1ko_j_"
n = "t1_g2j2"
e0, e1 = ESC("t1ko_j")
FX += VIVO("t1ko_j", n, 40, "Transmisión oficial · T1 vs KOI · partida 2", "T1", "Minuto 19")
a = T0(g + "0")
FX += REBX(n, a, 40 + (a - e0), NX(g + "0"), 42)
FX += [tar(W(g + "0", "cinco"), NX(g + "0"), "T1 +5,6K", "Empieza el dragón", A, logo="T1", x=.76, y=.17, tam=40)]
b = T0(g + "1")
p, q = W(g + "1", "pero"), W(g + "1", "van")
FX += PZ(n, b, p, 42, [
    an(.30, .425, "Oner", "JARVAN IV", "T1", W(g + "1", "Oner"), "JarvanIV", lado="izq", r=50),
    intencion([(.31, .425), (.37, .48), (.42, .54)], A, W(g + "1", "adelanta"), "SOLO", off=(0, 50)),
    an(.53, .51, "Alvaro", None, "MKOI", W(g + "1", "queda"), "Seraphine", lado="der", r=38),
    an(.50, .60, "Supa", None, "MKOI", W(g + "1", "queda") + .2, "Ezreal", lado="der", r=38),
    an(.42, .66, "Elyoya", None, "MKOI", W(g + "1", "queda") + .4, "XinZhao", lado="izq", r=38),
    texto("LA CARNADA", "ASÍ LA LLAMARON LOS NARRADORES", .18, .28, W(g + "1", "carnada"), color=Y, tam=40),
], d3="t1ko_a")
FX += LEN(n, p, q, 42, 46)
FX += MESA2("t1ko", q, NX(g + "2"), H(n, 46))
FX += [peg(q + .4, "Oner", "Oner", A, "T1", "Jarvan IV · sigue vivo", dur=T0(g + "2") - q - .3, x=.1, y=.42, tam=190),
       tar(W(g + "2", "Faker"), NX(g + "2"), "Faker", "Orianna · por el flanco", A, icono="Orianna", x=.76, y=.17, tam=40)]
b = T0(g + "3")
FX += SYNC(n, [(b, 46), (W(g + "3", "Jojopyun"), 49.1), (W(g + "3", "Supa"), 51.1), (W(g + "3", "Alvaro"), 53.1), (W(g + "3", "Elyoya"), 55.1),
               (W(g + "3", "Myrwn"), 59.1), (W(g + "3", "Cinco"), 60), (e1, None)])
ks = [("Jojopyun", .08), ("Supa", .21), ("Alvaro", .34), ("Elyoya", .47), ("Myrwn", .60)]
FX += [gris(W(g + "3", v_), v_, "MKOI", None, x_, W(g + "3", "Cinco") + 3) for v_, x_ in ks]
FX += [dict(tipo="destello", en=W(g + "3", "Cinco"), fuerza=.5),
       tar(W(g + "3", "Cinco"), e1, "5 por 0", "Ace · Oner sigue vivo", A, logo="T1", dato="5-0", x=.72, y=.84, tam=46)]

g = "t1ko_rep_"
e0, e1 = ESC("t1ko_rep")
f0 = T0(g + "0")
FX += LENTA(n, e0, f0, 50, .45, zoom=(1.3, .48, .55))
FX += [CLIP(n, f0, e1, 73, 88),
       vs(f0 + .1, e1, "T1", "MKOI", "T1 gana 2 a 0", "T1 a cuartos · KOI 2-2", ganador=0, y=.42)]

g = "t1ko_peor_"
n = "t1_g2j1"
e0, e1 = ESC("t1ko_peor")
b = T0(g + "1")
c = W(g + "0", "Elyoya")
d = W(g + "0", "Keria")
FX += [CLIP(n, e0, c, 25, 57)]
FX += [peor(e0 + .1, c, "Lo peor de KOI", "Elyoya", "MKOI", ["Se mete a robar a la jungla de T1", "Minuto 8"], [W(g + "0", "peor"), W(g + "0", "minutos")], "Jungla · Xin Zhao")]
FX += PZ(n, c, b, 57, [
    an(.46, .64, "Elyoya", "XIN ZHAO · ROBANDO", "MKOI", c + .1, "XinZhao", lado="der", r=50),
    texto("JUNGLA DE T1", None, .2, .3, c + .3, color=Y),
    an(.415, .27, "Doran", None, "T1", d, "Gwen", lado="izq", r=40),
    an(.42, .39, "Keria", None, "T1", d + .3, "Karma", lado="izq", r=40),
    intencion([(.42, .41), (.44, .52), (.455, .61)], A, d + .5),
])
u, v = W(g + "1", "Keria"), W(g + "1", "Doran", 1)
w = W(g + "1", "Tres")
FX += SYNC(n, [(b, 57), (W(g + "1", "mata"), 66.1), (W(g + "1", "rio"), 75.1), (W(g + "1", "Supa"), 83.1), (w, 85), (e1, None)])
FX += [gris(W(g + "1", "mata"), "Elyoya", "MKOI", None, .08, w + 2), gris(W(g + "1", "rio"), "Alvaro", "MKOI", None, .21, w + 2),
       gris(W(g + "1", "Supa"), "Supa", "MKOI", None, .34, w + 2),
       dict(tipo="destello", en=w, fuerza=.45),
       tar(w, W(g + "1", "KOI"), "3 por 0, gratis", "De +1,4K a +3,0K", A, logo="T1", dato="3-0", x=.72, y=.84, tam=46),
       tar(W(g + "1", "KOI"), e1, "KOI: 0 torres", "Partida 2 · 9 a 0", R, logo="MKOI", x=.72, y=.84, tam=46)]

# ================================================================== MIÉRCOLES · LYON vs INVICTUS
AZUL = {"LYON"}
g = "lyig_res_"
n = "lyig_ace"
e0, e1 = ESC("lyig_res")
c = W(g + "0", "primera")
FX += [J("lyig_j3", e0, c, 2.0),
       vs(e0 + .15, c, "LYON", "IG", "Esa misma tarde", "También por el pase", y=.42)]
FX += SYNC(n, [(c, 3), (e1, None)])
FX += [sil(W(g + "0", "Rookie"), "Rookie", "Rookie", None, dur=e1 - W(g + "0", "Rookie"), lado="der", alto=560),
       tar(W(g + "0", "Rookie"), e1, "Rookie · Aurora", "8/1/8 en la partida 1", R, logo="IG", x=.4, y=.17, tam=40),
       tar(W(g + "0", "cuadruple"), W(g + "0", "Diecinueve"), "Cuádruple y ace", "25:02", R, logo="IG", x=.28, y=.84, tam=46),
       tar(W(g + "0", "Diecinueve"), e1, "19 a 4", "Partida 1 para Invictus", R, logo="IG", x=.28, y=.84, tam=46),
       dict(tipo="destello", en=W(g + "0", "ace"), fuerza=.5)]

g = "lyig_j1_"
n = "lyig_j1"
AZUL = {"IG"}
e0, e1 = ESC("lyig_j1")
FX += VIVO("lyig_j1", n, 21, "Transmisión oficial · LYON vs IG · partida 2", "LYON", "Minuto 28")
a = T0(g + "0")
FX += REBX(n, a, 21 + (a - e0), NX(g + "0"), 22)
FX += [tar(W(g + "0", "Barón"), NX(g + "0"), "LYON +1,4K", "Invictus tiene el Barón", R, logo="LYON", x=.76, y=.17, tam=40)]
b = T0(g + "1")
FX += MESA2("lyig1", b, NX(g + "1"), H(n, 22))
FX += [cam(W(g + "1", "Dhokla"), "Dhokla", "Dhokla", dur=3.0, x=.09, y=.42), cam(W(g + "1", "Isles"), "Isles", "Isles", dur=NX(g + "1") - W(g + "1", "Isles"), x=.91, y=.3)]
b = T0(g + "2")
c = W(g + "2", "Meiko")
FX += LEN(n, b, c, 22, 24)
FX += [tar(W(g + "2", "Destello"), c, "Destello de Isles", "28:02", R, icono="SummonerFlash", x=.76, y=.17, tam=40)]
FX += PZ(n, c, NX(g + "2"), 24, [
    an(.26, .44, "Meiko", "STUNNED", "IG", c + .1, "Nautilus", lado="izq"),
    zona(x=.39, y=.56, rx=.09, ry=.09, color=R, en=W(g + "2", "JiaQi") - .2),
    an(.665, .66, "Rookie", None, "IG", W(g + "2", "JiaQi"), "Annie", lado="der", r=38),
], d3="lyig1b")
FX += [tar(W(g + "2", "JiaQi"), NX(g + "2"), "JiaQi, en el aire", "Con Isles encima", R, icono="Alistar", x=.5, y=.17, tam=40)]
b = T0(g + "3")
u = W(g + "3", "Tres")
FX += SYNC(n, [(b, 24), (W(g + "3", "De"), 40), (e1, None)])
FX += [gris(W(g + "3", "JiaQi"), "JiaQi", "IG", "28:05", .08, u + 2), gris(W(g + "3", "Rookie"), "Rookie", "IG", "28:08", .21, u + 2),
       gris(W(g + "3", "Wei"), "Wei", "IG", "28:14", .34, u + 2),
       dict(tipo="destello", en=W(g + "3", "JiaQi"), fuerza=.45),
       tar(u, W(g + "3", "De"), "3 por 0", None, R, logo="LYON", dato="3-0", x=.72, y=.84, tam=46),
       tar(W(g + "3", "De"), e1, "LYON: de +1,4K a +4,7K", "28:40 · 2.º Infernal", R, logo="LYON", x=.72, y=.84, tam=46),
       vs(W(g + "3", "LYON"), e1, "LYON", "IG", "Empate", "1 a 1 en la serie", y=.4)]

g = "lyig_j2_"
n = "lyig_j2"
AZUL = {"LYON"}
e0, e1 = ESC("lyig_j2")
FX += VIVO("lyig_j2", n, 20, "Transmisión oficial · LYON vs IG · partida 3", "IG", "Minuto 2")
a = T0(g + "0")
FX += REBX(n, a, 20 + (a - e0), NX(g + "0"), 22)
FX += [tar(W(g + "0", "tercera"), NX(g + "0"), "Partida 3", "La que decide la serie", "oro", x=.76, y=.17, tam=40)]
b = T0(g + "1")
c = W(g + "1", "Meiko")
d = W(g + "1", "va")
FX += PZ(n, b, c, 22, [
    an(.30, .275, "Inspired", "XIN ZHAO", "LYON", W(g + "1", "Inspired"), "XinZhao", lado="der"),
    intencion(RUTA(n, 22, [(22.0, .30, .275), (23.0, .37, .30), (24.0, .39, .39), (25.0, .37, .43)]), A, W(g + "1", "baja"), None),
    an(.41, .63, "Meiko y JiaQi", None, "IG", W(g + "1", "pareja"), "Lux", lado="der"),
    an(.25, .535, "Berserker", None, "LYON", W(g + "1", "emboscada"), "Lucian", lado="izq", r=40),
    an(.20, .745, "Isles", None, "LYON", W(g + "1", "emboscada") + .3, "Milio", lado="izq", r=38),
], d3="lyig2a")
FX += LEN(n, c, d, 22, 24)
FX += [cam(c, "Meiko", "Meiko · Lux", dur=d - c + .2, x=.91, y=.3)]
u = W(g + "2", "Primera")
FX += MESA2("lyig2", d, u, H(n, 24))
FX += [tar(W(g + "2", "prision"), u, "Prisión de luz", "Sobre Berserker", R, icono="Lux", x=.76, y=.17, tam=40)]
FX += SYNC(n, [(u, 24), (T0(g + "3"), 26)])
FX += [tar(u, T0(g + "3"), "Primera sangre", "JiaQi sobre Berserker · 02:36", R, logo="IG", x=.5, y=.84, tam=48),
       gris(u + .2, "Berserker", "LYON", "02:36", .08, T1(g + "3")),
       dict(tipo="destello", en=T0(g + "3") - .1, fuerza=.45)]
b = T0(g + "3")
v = W(g + "3", "Pero")
FX += SYNC(n, [(b, 26), (W(g + "3", "Queda"), 41), (v, 42)])
FX += [J(n, v, NX(g + "3"), 42, .4),
       gris(W(g + "3", "Meiko"), "Meiko", "IG", "02:40", .21, T1(g + "3")), gris(W(g + "3", "Inspired", 1), "Inspired", "LYON", "02:48", .34, T1(g + "3")),
       gris(W(g + "3", "JiaQi", 1), "JiaQi", "IG", "02:50", .47, T1(g + "3")),
       tar(W(g + "3", "Queda"), NX(g + "3"), "2 por 2", "Los 2 de Invictus son del tirador", R, logo="IG", dato="2-2", x=.72, y=.84, tam=44)]
b = T0(g + "4")
FX += [CLIP(n, b, e1, 81, 112), x2(b, b + 3.5, "REPETICIÓN", x=.3),
       tar(W(g + "4", "narradores"), W(g + "4", "Invictus"), "«Una bola de nieve»", "Los narradores", "oro", x=.5, y=.17, tam=50),
       tar(W(g + "4", "Invictus"), W(g + "4", "JiaQi"), "Invictus, arriba en oro", "De ahí al final", R, logo="IG", x=.5, y=.17, tam=50),
       mg(L.barras("Partida 3 · asesinatos de Invictus", [(ICON("Caitlyn"), "JiaQi", 5), (EQ("IG"), "El resto del equipo", 2)], 7),
          W(g + "4", "JiaQi"), W(g + "4", "Invictus", 1), [W(g + "4", "cinco"), W(g + "4", "siete")], y=.5, nombre="barras JiaQi"),
       vs(W(g + "4", "Invictus", 1), e1, "LYON", "IG", "Invictus gana 2 a 1", "Invictus a cuartos · LYON 2-2", ganador=1, y=.42)]

g = "lyig_peor_"
n = "lyig_j3"
AZUL = {"LYON"}
e0, e1 = ESC("lyig_peor")
c = W(g + "0", "minuto")
d = W(g + "0", "Wei")
FX += [CLIP(n, e0, c, 3, 15.2),
       peor(e0 + .1, c, "Lo peor de esa serie", "Inspired", "LYON", ["Partida 1 · 1/6/1"], [W(g + "0", "peor"), W(g + "0", "partida")], "Jungla · Nocturne")]
FX += [J(n, c, W(g + "0", "pegandole"), 15.2, .6)]
_t = 15.2 + .6 * (W(g + "0", "pegandole") - c)
FX += SYNC(n, [(W(g + "0", "pegandole"), _t), (d, 18)])
FX += [tar(W(g + "0", "pegandole"), d, "En la jungla de Invictus", "12:16", R, logo="IG", x=.76, y=.17, tam=40)]
u = T0(g + "1")
FX += PZ(n, d, u, 20, [
    an(.385, .46, "Inspired", "NOCTURNE", "LYON", d, "Nocturne", lado="der"),
    an(.38, .32, "Wei", None, "IG", W(g + "0", "encima") - .1, "Vi", lado="der", r=40),
    an(.34, .20, "Rookie", None, "IG", W(g + "0", "Rookie"), "Aurora", lado="izq", r=40),
    an(.53, .74, "Meiko", None, "IG", W(g + "0", "Meiko"), "Lulu", lado="der", r=38),
    texto("JIAQI, POR ABAJO", None, .74, .55, W(g + "0", "JiaQi"), color=R),
], d3="lyig3")
FX += SYNC(n, [(u, 20), (W(g + "1", "asesinato"), 24), (e1, None)])
FX += [gris(W(g + "1", "asesinato"), "Inspired", "LYON", "12:22 · 1/6/1", .08, e1),
       dict(tipo="destello", en=W(g + "1", "asesinato"), fuerza=.45),
       tar(W(g + "1", "narrador"), e1, "«No está muy inspirado el día de hoy»", "Un narrador", "oro", x=.5, y=.17, tam=48)]

# ================================================================== JUEVES · KARMINE vs CFO
AZUL = {"KC"}
g = "kccf_res_"
e0, e1 = ESC("kccf_res")
b, c = T0(g + "1"), T0(g + "2")
FX += [J("kc_g1j4", e0, b, 0), CLIP("kc_g1j8", b, c, 62, 93), J("kc_g2j5", c, e1, 84.5, .55),
       tar(e0 + .15, W(g + "0", "Karmine"), "Jueves", "29 de octubre", "oro", x=.5, y=.17, tam=66),
       vs(W(g + "0", "Karmine"), T1(g + "0") + .2, "KC", "CFO", "A muerte", "Los dos con dos derrotas · el que pierde se va", y=.42),
       tar(W(g + "1", "diecinueve"), W(g + "1", "Doggo"), "19 a 3", "Partida 1 · CFO sin una sola torre", A, logo="KC", dato="10-0", x=.72, y=.84, tam=46),
       peg(W(g + "1", "Doggo"), "Doggo", "Doggo", R, "CFO", "0/3/0", dur=c - W(g + "1", "Doggo"), x=.8, y=.48, tam=420, gris=True, sello=("0 / 3 / 0", 0)),
       mg(L.calendario("Partida 2: dos pausas", [("17:03", "7 minutos", "oro"), ("25:02", "29 minutos", "rojo")]), c + .1, e1,
          [W(g + "2", "siete"), W(g + "2", "veintinueve")], y=.5, nombre="calendario pausas"),
       tar(W(g + "2", "comprar"), e1, "No podía comprar un objeto", "El equipo de Doggo", R, logo="CFO", x=.5, y=.84, tam=52)]

g = "kccf_j_"
n = "kc_g2j4"
AZUL = {"CFO"}
e0, e1 = ESC("kccf_j")
tv = 35 - (T0(g + "0") - e0)
FX += VIVO("kccf_j", n, tv, "Transmisión oficial · KC vs CFO · partida 2", "KC", "Minuto 20")
a = T0(g + "0")
FX += REBX(n, a, 35, NX(g + "0"), 15)
FX += [tar(W(g + "0", "CFO"), NX(g + "0"), "CFO +4,5K", "19:47", A, logo="CFO", x=.76, y=.17, tam=40),
       tar(W(g + "0", "Baron"), NX(g + "0"), "El Barón, en el mapa", None, "oro", x=.24, y=.17, tam=40)]
b = T0(g + "1")
FX += MESA2("kccf", b, NX(g + "1"), H(n, 15))
FX += [cam(W(g + "1", "Busio"), "Busio", "Busio · Lulu", dur=3.0, x=.09, y=.42),
       cam(W(g + "1", "Canna"), "Canna", "Canna · Camille", dur=NX(g + "1") - W(g + "1", "Canna"), x=.91, y=.3)]
b = T0(g + "2")
FX += SYNC(n, [(b, 15), (W(g + "2", "Doggo"), 22), (W(g + "2", "Rest"), 28), (W(g + "2", "Kino"), 32), (W(g + "2", "POUT"), 62), (W(g + "2", "Cuatro"), 64), (e1, 66)])
FX += [gris(W(g + "2", "Doggo"), "Doggo", "CFO", "20:04", .08, e1), gris(W(g + "2", "Rest"), "Rest", "CFO", "20:10", .21, e1),
       gris(W(g + "2", "Kino"), "Kino", "CFO", "20:14", .34, e1), gris(W(g + "2", "POUT"), "POUT", "CFO", "20:44", .47, e1),
       dict(tipo="destello", en=W(g + "2", "Doggo"), fuerza=.45),
       tar(W(g + "2", "Cuatro"), e1, "4 por 0", "Junto al Barón", R, logo="KC", dato="4-0", x=.74, y=.84, tam=46)]

g = "kccf_peor_"
n = "kc_g2j8"
e0, e1 = ESC("kccf_peor")
tv = 123 - (T0(g + "0") - e0)
FX += VIVO("kccf_peor", n, tv, "Transmisión oficial · KC vs CFO · partida 2", "KC", "Minuto 35")
a = T0(g + "0")
c = W(g + "0", "Shad0w")
FX += REBX(n, a, 123, c, 84)
FX += [peor(a + .1, c, "Lo peor de CFO", "Shad0w", "CFO", ["Minuto 35 · va solo al río"], [W(g + "0", "peor"), W(g + "0", "minuto")], "Jungla · Lee Sin")]
b = T0(g + "1")
FX += PZ(n, c, b, 84, [
    dict(tipo="foco", en=c + .1, k=.38),
    an(.54, .40, "Shad0w", "SOLO EN EL RÍO", "CFO", c + .1, "LeeSin", lado="der"),
    an(.13, .63, "POUT", "LEJOS", "CFO", W(g + "0", "centinela") - .2, "Ryze", lado="der", r=38),
    texto("UN CENTINELA LO DELATA", None, .74, .62, W(g + "0", "centinela"), color=Y),
], d3="kc_e1")
u, v = W(g + "1", "cuatro"), W(g + "1", "Cinco", 1)
w = W(g + "1", "CFO", 1)
FX += SYNC(n, [(b, 84), (W(g + "1", "mata"), 91), (u, 112), (v, 123), (W(g + "1", "nexo"), 176), (e1, 180)])
FX += [gris(W(g + "1", "mata"), "Shad0w", "CFO", "35:32", .08, v), dict(tipo="destello", en=W(g + "1", "mata"), fuerza=.45),
       tar(u, v, "4 contra 5", "Sin su jungla", R, logo="KC", x=.72, y=.84, tam=46),
       tar(v, w, "5 por 1, ancestral y nexo", None, R, logo="KC", dato="5-1", x=.72, y=.84, tam=46),
       dict(tipo="destello", en=W(g + "1", "nexo"), fuerza=.55),
       elim(w, e1, "CFO", "CTBC Flying Oyster", "1-3 · y con ellos, la LCP entera", [W(g + "1", "Mundial"), W(g + "1", "LCP")])]

# ================================================================== JUEVES · BLG vs TES
AZUL = {"BLG"}
g = "blte_res_"
n = "blte_j1"
e0, e1 = ESC("blte_res")
FX += VIVO("blte_res", n, 22, "Transmisión oficial · BLG vs TES · partida 1", "BLG", "Minuto 25")
a = T0(g + "0")
ta = 22 + (a - e0)
u = W(g + "0", "Knight")
FX += REBX(n, a, ta, u, 25)
FX += [vs(a + 1.3, u, "BLG", "TES", "La mejor serie de la semana", "Por el pase · al mejor de 3", y=.42)]
v = W(g + "0", "dos")
FX += LEN(n, u, e1, 27, 32.4)
FX += [sil(u, "Knight", "Knight", None, dur=W(g + "0", "veintiuno") - u, lado="der", alto=520),
       tar(u, W(g + "0", "veintiuno"), "Knight · Orianna", None, A, logo="BLG", x=.4, y=.17, tam=40),
       tar(W(g + "0", "triple"), W(g + "0", "veintiuno"), "Triple en 2 segundos", "25:48-25:51", A, logo="BLG", x=.3, y=.84, tam=46),
       tar(W(g + "0", "veintiuno"), e1, "21 a 6", "Partida 1 para Bilibili", A, logo="BLG", dato="21-6", x=.3, y=.84, tam=46)]

g = "blte_peor_"
n = "blte_j3"
e0, e1 = ESC("blte_peor")
FX += VIVO("blte_peor", n, 24, "Transmisión oficial · BLG vs TES · partida 2", "TES", "Minuto 28")
a = T0(g + "0")
_t = 19 - (W(g + "0", "Creme") - a - 1.2)
FX += REB(n, a, 24 + (a - e0), _t)
FX += SYNC(n, [(a + 1.2, _t), (W(g + "0", "Creme"), 19), (NX(g + "0"), 23)])
FX += [tar(W(g + "0", "tres"), W(g + "0", "Creme"), "Bilibili +5,2K", "3 dragones · 28:49", A, logo="BLG", x=.76, y=.17, tam=40),
       gris(W(g + "0", "Creme"), "Creme", "TES", "28:45", .08, NX(g + "0")),
       tar(W(g + "0", "Ya"), NX(g + "0"), "Ya ganó la pelea", "6 a 3", A, logo="BLG", x=.72, y=.84, tam=46)]
b = T0(g + "1")
c = W(g + "1", "cuatro")
FX += PZ(n, b, c, 23, [
    dict(tipo="foco", en=b + .1, k=.3),
    an(.485, .44, "Tian", None, "TES", W(g + "1", "jungla"), "JarvanIV", lado="der", r=38),
    an(.394, .207, "JackeyLove", None, "TES", W(g + "1", "jungla") + .2, "Lucian", lado="izq", r=38),
    an(.439, .20, "Zhuo", None, "TES", W(g + "1", "jungla") + .4, "Milio", lado="der", r=36),
], d3="blte3a")
FX += [tar(W(g + "1", "jungla"), c, "Dentro de la jungla de TES", "28:49", R, logo="TES", x=.5, y=.84, tam=46)]
FX += MESA2("blte3", c, NX(g + "1"), H(n, 23))
FX += [cam(W(g + "1", "Xun"), "Xun", "Xun · casi muerto", dur=2.4, x=.09, y=.38),
       cam(W(g + "1", "Knight"), "Knight", "Knight · solo", dur=2.4, x=.09, y=.66),
       cam(W(g + "1", "Bin"), "Bin", "Bin · centro", dur=NX(g + "1") - W(g + "1", "Bin"), x=.91, y=.28),
       cam(W(g + "1", "Viper"), "Viper", "Viper y ON", dur=NX(g + "1") - W(g + "1", "Viper"), x=.91, y=.62)]
b = T0(g + "2")
FX += SYNC(n, [(b, 23), (W(g + "2", "Viper"), 30), (W(g + "2", "ON"), 33), (W(g + "2", "Bin"), 41), (W(g + "2", "Xun"), 47.5), (NX(g + "2"), 48.5)])
FX += [gris(W(g + "2", "Viper"), "Viper", "BLG", "28:56", .08, T1(g + "3") - 4), gris(W(g + "2", "ON"), "ON", "BLG", "28:59", .21, T1(g + "3") - 4),
       gris(W(g + "2", "Bin"), "Bin", "BLG", "29:07", .34, T1(g + "3") - 4), gris(W(g + "2", "Xun"), "Xun", "BLG", "≈ 29:24", .47, T1(g + "3") - 4),
       dict(tipo="destello", en=W(g + "2", "Viper"), fuerza=.45)]
b = T0(g + "3")
FX += SYNC(n, [(b, 48.5), (W(g + "3", "Baron"), 82), (e1, None)])
FX += [mg(L.calendario("Un minuto y medio que voltea la partida", [("28:49", "Bilibili\n+5,2K", "azul"), ("29:24", "4 muertos", "rojo"), ("29:48", "Barón\npara TES", "rojo"),
                                                                    ("Min 31", "TES\n+1K", "rojo"), ("Min 32", "Le quita\nel alma", "rojo")]),
          b + .1, e1,
          [b + .4, W(g + "3", "jugadores"), W(g + "3", "Baron"), W(g + "3", "delante"), W(g + "3", "alma")], y=.5, nombre="calendario blte")]

g = "blte_j_"
n = "blte_j2"
e0, e1 = ESC("blte_j")
FX += VIVO("blte_j", n, 26, "Transmisión oficial · BLG vs TES · partida 2", "TES", "Minuto 36")
a = T0(g + "0")
c = W(g + "1", "Los")
FX += REBX(n, a, 26 + (a - e0), c, 26)         # contexto seguido, a x1, hasta la pausa
FX += [tar(W(g + "0", "dos"), NX(g + "0"), "Bilibili +2K", "36:00", A, logo="BLG", x=.76, y=.17, tam=40),
       tar(W(g + "0", "Entonces"), NX(g + "0"), "TES empieza el Barón", "10 231 de vida · 36:12", R, logo="TES", x=.24, y=.17, tam=40)]
b = T0(g + "1")
FX += PZ(n, c, NX(g + "1"), 26, [
    an(.387, .411, "Bin", None, "BLG", c, "KSante", lado="der", r=38),
    an(.408, .538, "Xun", None, "BLG", c + .2, "MonkeyKing", lado="izq", r=38),
    an(.513, .48, "ON y Knight", None, "BLG", c + .4, "Leblanc", lado="der", r=38),
    an(.608, .606, "Viper", None, "BLG", c + .6, "Ashe", lado="der", r=38),
    an(.245, .695, "Creme", None, "TES", c + .8, "Locke", lado="izq", r=38),
])
FX += [tar(b + .1, NX(g + "1"), "Barón: 4 663", "36:18", "oro", x=.5, y=.17, tam=44)]
b = T0(g + "2")
c = W(g + "2", "Bin")
FX += [J(n, b, c, 26, (31 - 26) / (c - b)),
       tar(W(g + "2", "suelta"), c, "Lo suelta en 3 565", "36:23 · ya no baja", R, logo="TES", x=.5, y=.17, tam=46)]
FX += MESA2("blte2", c, NX(g + "2"), H(n, 31))
b = T0(g + "3")
FX += SYNC(n, [(b, 31), (W(g + "3", "Viper"), 33), (W(g + "3", "ON"), 36), (W(g + "3", "Bin"), 50), (W(g + "3", "Knight"), 59.6), (W(g + "3", "Cuatro"), 62), (W(g + "3", "nexo"), 101.5), (e1, None)])
FX += [gris(W(g + "3", "Viper"), "Viper", "BLG", "36:25", .08, W(g + "3", "nexo")), gris(W(g + "3", "ON"), "ON", "BLG", "36:28", .21, W(g + "3", "nexo")),
       gris(W(g + "3", "Bin"), "Bin", "BLG", "36:42", .34, W(g + "3", "nexo")), gris(W(g + "3", "Knight"), "Knight", "BLG", "36:52", .47, W(g + "3", "nexo")),
       dict(tipo="destello", en=W(g + "3", "Viper"), fuerza=.45),
       tar(W(g + "3", "Cuatro"), W(g + "3", "nexo"), "4 muertes de Bilibili", "Ninguna de TES", R, logo="TES", dato="4-0", x=.74, y=.84, tam=46),
       dict(tipo="destello", en=W(g + "3", "nexo"), fuerza=.5)]

AZUL = {"TES"}
g = "blte_fin_"
n = "blte_g3"
e0, e1 = ESC("blte_fin")
u, v = W(g + "0", "369"), W(g + "0", "Viper")
w = W(g + "0", "TES")
FX += [CLIP(n, e0, w, 0, 23), J(n, w, e1, 23, .55),
       tar(e0 + .3, u, "Partida 3 · 17 a 3", "Para Top Esports", A, logo="TES", dato="17-3", x=.5, y=.17, tam=56),
       mg(L.premio("Lo mejor de TES", JUG("369"), "369", EQ("TES"), ["0 muertes en las dos últimas partidas", "6/0/12 en esas dos"], color="oro", sub="Top · Top Esports"),
          u, v, [u + .5, u + 1.1, u + 1.6], y=.5, nombre="premio 369"),
       peor(v, w, "Lo peor de Bilibili", "Viper", "BLG", ["0 asesinatos en las dos últimas: 0/8/6"], [v + .3, v + 1.0], "Tirador"),
       vs(w, e1, "BLG", "TES", "TES gana 2 a 1", "TES a cuartos · Bilibili 2-2", ganador=1, y=.42)]

# ================================================================== VIERNES · LOS vs TEAM LIQUID
AZUL = {"LOS"}
g = "lotl_res_"
e0, e1 = ESC("lotl_res")
b, c = T0(g + "1"), T0(g + "2")
d = W(g + "2", "Liquid")
f_ = W(g + "2", "Todo")
FX += [J("lotl_j3", e0, b, 22), CLIP("lotl_g2", b, c, 0, 8),
       CLIP("lotl_g1", c, d, 2, 14), CLIP("lotl_g2", d, e1, 8, 21.5),
       tar(e0 + .15, W(g + "0", "Team"), "Viernes", "30 de octubre", "oro", x=.5, y=.17, tam=66),
       vs(W(g + "0", "Team"), T1(g + "0") + .2, "TLAW", "LOS", "A muerte", "Team Liquid eliminó al campeón de China", y=.42),
       com(W(g + "1", "Felo"), "UgypvpvJ9AMDXNvkc-t4AaABAg", W(g + "1", "Pues") - W(g + "1", "Felo") + .1, x=.5, y=.32, tam=960),
       sil(W(g + "1", "Pues"), "Josedeodo", "Josedeodo", None, dur=c - W(g + "1", "Pues"), lado="izq", alto=520),
       tar(W(g + "1", "Pues"), c, "Josedeodo", "Jungla · Team Liquid", R, logo="TLAW", x=.76, y=.17, tam=40),
       tar(W(g + "2", "Curse"), d, "Curse · Trundle", "7/0/6 · partida 1", A, logo="LOS", icono=None, x=.72, y=.84, tam=46),
       cam(W(g + "2", "Curse"), "Curse", "Curse", dur=d - W(g + "2", "Curse"), x=.1, y=.3),
       tar(d, f_, "Liquid empata", "Alma, Barón y Anciano", R, logo="TLAW", x=.72, y=.84, tam=46),
       tar(f_, e1, "Partida 3 · 47 minutos", None, "oro", x=.5, y=.17, tam=56)]

g = "lotl_j_"
n = "lotl_j1"
AZUL = {"TLAW"}
e0, e1 = ESC("lotl_j")
FX += VIVO("lotl_j", n, 19, "Transmisión oficial · LOS vs Liquid · partida 3", "LOS", "Minuto 34")
a = T0(g + "0")
FX += REBX(n, a, 19 + (a - e0), NX(g + "0"), 14)
FX += [tar(W(g + "0", "siete"), W(g + "0", "tiene"), "LOS: de +7,2K a +3,3K", "Del minuto 27 al 34:42", R, logo="LOS", x=.76, y=.17, tam=40),
       tar(W(g + "0", "tiene"), NX(g + "0"), "Liquid, con el Barón", None, A, logo="TLAW", x=.24, y=.17, tam=40)]
b = T0(g + "1")
c = W(g + "1", "Feisty")
FX += PZ(n, b, c, 14, [
    zona(x=.595, y=.683, rx=.06, ry=.05, color=R, en=W(g + "1", "Curse"), alfa=.2),
    an(.387, .292, "Morgan", None, "TLAW", W(g + "1", "dragon"), "Gnar", lado="der", r=38),
    an(.20, .472, "CoreJJ", None, "TLAW", W(g + "1", "dragon") + .2, "Lulu", lado="izq", r=38),
    an(.265, .546, "Quid", None, "TLAW", W(g + "1", "dragon") + .4, "Viktor", lado="der", r=38),
    an(.209, .614, "Yeon", None, "TLAW", W(g + "1", "dragon") + .6, "Yunara", lado="izq", r=38),
    an(.634, .387, "Feisty", "CHANNELING", "LOS", W(g + "1", "Curse"), "Taliyah", lado="der", r=38),
], d3="lotl1a")
FX += [cam(W(g + "1", "Curse"), "Curse", "Curse · cae con su equipo", dur=c - W(g + "1", "Curse"), x=.91, y=.72, tam=190)]
d = NX(g + "1")
FX += LEN(n, c, d, 14, 17.6)
FX += [cam(c, "Feisty", "Feisty · Taliyah", dur=d - c + 3.0, x=.91, y=.3)]
b = T0(g + "2")
c = W(g + "2", "CoreJJ")
MURO1 = [(u, round(v + .012, 3)) for u, v in ((.206, .337), (.288, .320), (.369, .314), (.438, .303), (.531, .292), (.638, .253), (.744, .237))]  # cresta + .012 = centro de la roca
FX += PZ(n, b, c, 17.6, [
    muro_2d(MURO1, W(g + "2", "muro")),
    texto("EL MURO DE TALIYAH", None, .5, .13, W(g + "2", "muro") + .3, color=Y),
])
FX += MESA2("lotl", c, NX(g + "2"), H(n, 17.6))
FX += [tar(W(g + "2", "Yeon"), NX(g + "2"), "Josedeodo y Yeon", "Al sur, con todo LOS encima", R, logo="TLAW", x=.5, y=.84, tam=44)]
b = T0(g + "3")
FX += SYNC(n, [(b, 17.6), (W(g + "3", "dos"), 19), (W(g + "3", "Yeon"), 21.3), (W(g + "3", "Josedeodo"), 23.5), (W(g + "3", "doble"), 27.5), (W(g + "3", "triple"), 29), (NX(g + "3"), 30)])
FX += [tar(b, W(g + "3", "Ackerman"), "Dragón para Liquid", "34:41", A, logo="TLAW", x=.5, y=.84, tam=46),
       gris(W(g + "3", "Yeon"), "Yeon", "TLAW", "34:44", .08, NX(g + "3") + 2), gris(W(g + "3", "Josedeodo"), "Josedeodo", "TLAW", "34:46", .21, NX(g + "3") + 2),
       cam(W(g + "3", "Zest"), "Zest", "Zest · Tristana", dur=NX(g + "3") - W(g + "3", "Zest"), x=.91, y=.3),
       dict(tipo="destello", en=W(g + "3", "Yeon"), fuerza=.4), dict(tipo="destello", en=W(g + "3", "triple"), fuerza=.5),
       tar(W(g + "3", "doble"), W(g + "3", "triple"), "Doble", "34:50", R, logo="LOS", x=.74, y=.84, tam=46),
       tar(W(g + "3", "triple"), NX(g + "3"), "Triple", "34:52", R, logo="LOS", x=.74, y=.84, tam=46)]
b = T0(g + "4")
FX += TRAMO(n, b, e1, 30, 78)
FX += [tar(b + .05, W(g + "4", "LOS"), "4 por 0", None, R, logo="LOS", dato="4-0", x=.74, y=.84, tam=46),
       tar(W(g + "4", "LOS"), e1, "LOS, casi +7K", "Torre e inhibidor", R, logo="LOS", x=.74, y=.84, tam=46)]

g = "lotl_rep_"
e0, e1 = ESC("lotl_rep")
f0 = T0(g + "0")
FX += [J(n, e0, f0, 99.0), tar(e0 + .3, e0 + 5.5, "Repetición", "Con la narración original", R, x=.3, y=.13, tam=34)]
AUD_VIVOS.append(("lotl_rep", fuente(n), 99.0, round(e0, 3), round(f0, 3)))
FX += LENTA(n, f0, e1, 96, .55, zoom=(1.25, .45, .45), sub="Mírala otra vez")
FX += [tar(W(g + "0", "Divide"), e1, "«Divide completamente al equipo»", "Los narradores", "oro", x=.5, y=.84, tam=48)]

g = "lotl_peor_"
n = "lotl_j3"
e0, e1 = ESC("lotl_peor")
c = W(g + "0", "Duduhh")
d = W(g + "0", "solo")
u = W(g + "0", "cae")
v = W(g + "0", "Un")
b = T0(g + "1")
FX += [CLIP(n, e0, d, 2, 15),
       peor(e0 + .1, W(g + "0", "no"), "Casi lo regalan", "Duduhh", "LOS", ["Minuto 38 · no había muerto"], [e0 + .5, W(g + "0", "Minuto")], "Tirador · Kalista")]
FX += PZ(n, d, u, 15, [
    an(.305, .453, "Duduhh", "SOLO", "LOS", d, "Kalista", lado="izq"),
    an(.42, .416, "Josedeodo", None, "TLAW", d + .2, "Sejuani", lado="der", r=38),
    an(.603, .395, "Ackerman", None, "LOS", d + .4, "Renata", lado="der", r=36),
    an(.713, .424, "Curse", None, "LOS", d + .6, "Pantheon", lado="der", r=36),
])
FX += LEN(n, u, v, 15, 20)
FX += [J(n, v, b, 20, .9),
       gris(u + .1, "Duduhh", "LOS", "38:28 · su única muerte", .08, b),
       dict(tipo="destello", en=v - .3, fuerza=.45),
       tar(W(g + "0", "dijo"), b, "«Se sintió el dios»", "Un narrador", "oro", x=.5, y=.17, tam=52)]
n = "lotl_j2"
FX += [CLIP(n, b, e1, 4.6, 12),
       tar(b + .05, e1, "64 segundos después", "Barón para Liquid · 39:32", A, logo="TLAW", x=.5, y=.84, tam=48)]

g = "lotl_j2_"
e0, e1 = ESC("lotl_j2")
FX += VIVO("lotl_j2", n, 19, "Transmisión oficial · partida 3", "LOS", "Minuto 39")
a = T0(g + "0")
u, v, w = W(g + "0", "rio"), W(g + "0", "aparece"), W(g + "0", "Ocho")
c = W(g + "0", "otro")
d = W(g + "0", "Alma")
e_ = W(g + "0", "LOS", 1, fin=True) + .1        # la pausa dura hasta «es de LOS»: ahí sigue el VOD, y el alma cae cuando la voz la dice
_t = 13 - (u - a - 1.2)
FX += REB(n, a, 19 + (a - e0), _t)
FX += SYNC(n, [(a + 1.2, _t), (u, 13), (v, 17), (c, 21)])
FX += [tar(W(g + "0", "Liquid"), u, "Barón para Liquid", "39:32", A, logo="TLAW", x=.24, y=.17, tam=40),
       tar(u, v, "LOS, ya en el río", "39:37", R, logo="LOS", x=.24, y=.17, tam=40),
       tar(v, c, "Aparece el dragón", "39:41", "oro", x=.24, y=.17, tam=40)]
MURO2 = [(.323, .752), (.363, .680), (.414, .544), (.475, .373), (.516, .237), (.556, .147)]
FX += PZ(n, c, e_, 21, [
    muro_2d(MURO2, c + .05),
    texto("OTRO MURO DE FEISTY", None, .74, .3, c + .4, color=Y),
])
FX += SYNC(n, [(e_, 21), (d, 29), (T0(g + "1"), None)])
FX += [tar(d - .1, T0(g + "1"), "Alma para LOS", "8 segundos después · 39:49", R, logo="LOS", x=.5, y=.84, tam=48), dict(tipo="destello", en=d, fuerza=.5)]
b = T0(g + "1")
FX += [J(n, b, e1, 29 + b - d, .9),
       tar(b + .05, e1, "Liquid: 2 Barones", "Y perdió la partida", A, logo="TLAW", x=.5, y=.84, tam=48)]

g = "lotl_fin_"
n = "lotl_zest"
e0, e1 = ESC("lotl_fin")
u = W(g + "0", "Team")
v = W(g + "0", "Josedeodo")
FX += [CLIP(n, e0, u, 3, 28), J(n, u, e1, 28, .6),
       sil(e0 + .1, "Zest", "Zest", None, dur=u - e0 - .1, lado="izq", alto=560),
       tar(e0 + .1, u, "Zest · Tristana top", "10/1/3", R, logo="LOS", x=.76, y=.17, tam=40),
       tar(W(g + "0", "LOS"), u, "LOS gana 2 a 1", "LOS 2-2", R, logo="LOS", x=.7, y=.84, tam=48),
       elim(u, v - .2, "TLAW", "Team Liquid", "1-3 · fuera del Mundial", [W(g + "0", "Mundial")]),
       peg(v - .2, "Josedeodo", "Josedeodo", A, "TLAW", "Lo sentimos, Felo", dur=e1 - v + .2, x=.5, y=.48, tam=430, gris=True, sello=("9/7/17", 0))]

# ================================================================== VIERNES · G2 vs HANWHA
AZUL = {"G2"}
g = "g2hl_res_"
n = "g2hl_j3"
e0, e1 = ESC("g2hl_res")
FX += [CLIP(n, e0, e1, 2, 18),
       vs(e0 + .15, W(g + "0", "G2", 1), "G2", "HLE", "A muerte", "El que pierde se va", y=.42),
       tar(W(g + "0", "G2", 1), e1, "G2 mandó 14 minutos", "Hasta +1,2K", A, logo="G2", x=.5, y=.84, tam=52)]

g = "g2hl_peor_"
e0, e1 = ESC("g2hl_peor")
FX += VIVO("g2hl_peor", n, 31, "Transmisión oficial · G2 vs Hanwha · partida 1", "G2", "Minuto 14")
a = T0(g + "0")
FX += REBX(n, a, 31 + (a - e0), NX(g + "0"), 30)
FX += [tar(W(g + "0", "G2"), NX(g + "0"), "G2, 6 a 4", "Acaba de ganar una pelea", A, logo="G2", x=.76, y=.17, tam=40),
       cam(W(g + "0", "BrokenBlade"), "BrokenBlade", "BrokenBlade · Olaf", dur=NX(g + "0") - W(g + "0", "BrokenBlade"), x=.09, y=.42)]
b = T0(g + "1")
c, d = W(g + "1", "barras"), W(g + "1", "cuando")
FX += PZ(n, b, c, 30, [
    an(.37, .37, "BrokenBlade", "~85 % DE VIDA", "G2", b + .1, "Olaf", lado="izq"),
    an(.50, .525, "Zeus", "~55 % DE VIDA", "HLE", b + .3, "KSante", lado="der"),
])
FX += LEN(n, c, d, 30, 38)
FX += [tar(c, d, "12 segundos", "Persiguiéndolo", R, logo="G2", x=.76, y=.17, tam=40)]
FX += PZ(n, d, NX(g + "1"), 38, [
    an(.305, .42, "BrokenBlade", "~15 %", "G2", d + .1, "Olaf", lado="izq"),
    an(.465, .68, "Zeus", "~25 %", "HLE", d + .3, "KSante", lado="der"),
    ruta(n, 38, [(30.0, .50, .525), (34.0, .53, .545), (38.0, .465, .68)], R, d + .5),
    ruta(n, 38, [(30.0, .37, .37), (38.0, .305, .42)], A, d + .7),
], d3="g2hl3")
b = T0(g + "2")
u = W(g + "2", "Esa")
FX += SYNC(n, [(b, 38), (W(g + "2", "solo"), 41), (u, 44)])
FX += [J(n, u, e1, 44, .5),
       gris(W(g + "2", "solo"), "BrokenBlade", "G2", "14:23", .08, u),
       dict(tipo="destello", en=W(g + "2", "solo"), fuerza=.45),
       peor(u, e1, "Lo peor de G2", "BrokenBlade", "G2", ["Última vez arriba en oro: 14:24", "Partida 1: 22 a 11"], [W(g + "2", "ultima"), W(g + "2", "veintidos")], "Top · Olaf", sello=None)]

g = "g2hl_j2_"
n = "g2hl_j2"
AZUL = {"HLE"}
e0, e1 = ESC("g2hl_j2")
FX += VIVO("g2hl_j2", n, 24, "Transmisión oficial · G2 vs Hanwha · partida 2", "HLE", "Minuto 15")
a = T0(g + "0")
c = W(g + "0", "Labrov")
FX += REBX(n, a, 24 + (a - e0), c, 22)
FX += [cam(W(g + "0", "Zeka"), "Zeka", "Zeka · Swain", dur=NX(g + "0") - W(g + "0", "Zeka"), x=.91, y=.3)]
FX += PZ(n, c, NX(g + "0"), 22, [
    an(.43, .665, "Zeka", "1 CONTRA 3", "HLE", c + .1, "Swain", lado="der", r=50),
    an(.375, .435, "Caps", None, "G2", W(g + "0", "Caps"), "Galio", lado="izq"),
    an(.785, .445, "Hans Sama", None, "G2", W(g + "0", "Hans"), "Xayah", lado="der"),
    texto("LABROV LO ENCANTA", None, .6, .25, c + .3, color=R),
], d3="g2hl2")
b = T0(g + "1")
c = W(g + "1", "Y")
FX += [J(n, b, c, 22, (28 - 22) / (c - b)),
       tar(b + .1, c, "737 / 2 184 de vida", "15:34", R, x=.76, y=.17, tam=40)]
d = W(g + "1", "Zeka")
FX += PZ(n, c, d, 28, [
    an(.485, .585, "Zeka", "737 DE VIDA", "HLE", c + .05, "Swain", lado="der", r=50),
    an(.69, .50, "Hans Sama", None, "G2", c + .2, "Xayah", lado="der", r=38),
    ruta(n, 28, [(22.0, .43, .665), (25.0, .455, .625), (28.0, .485, .585)], A, c + .3),
])
FX += [J(n, d, e1, 28, 1.0),
       tar(d, e1, "Zeka · 2/0/7", "No murió en toda la partida", A, logo="HLE", x=.72, y=.84, tam=46)]

g = "g2hl_j_"
n = "g2hl_j1"
e0, e1 = ESC("g2hl_j")
FX += VIVO("g2hl_j", n, 26, "Transmisión oficial · G2 vs Hanwha · partida 2", "HLE", "Minuto 21")
a = T0(g + "0")
c = W(g + "0", "BrokenBlade")
FX += REBX(n, a, 26 + (a - e0), c, 17)
FX += [tar(W(g + "0", "G2"), c, "G2 +0,9K", "21:36", R, logo="G2", x=.76, y=.17, tam=40)]
FX += PZ(n, c, NX(g + "0"), 17, [
    an(.505, .305, "Labrov", None, "G2", c, "Rakan", lado="der"),
    an(.33, .31, "Delight", None, "HLE", c + .2, "Milio", lado="izq", r=36),
    texto("BROKENBLADE: 4/0/1", "Y ZEUS, ABAJO", .68, .70, c + .3, color=R),
])
b = T0(g + "1")
c = W(g + "1", "adelantado")
FX += LEN(n, b, c, 17, 23.7)
FX += MESA2("g2hl", c, NX(g + "1"), H(n, 23.7))
FX += [tar(W(g + "1", "Swain"), NX(g + "1"), "Swain: definitiva", "Zeka · 21:43", A, icono="Swain", x=.76, y=.17, tam=40)]
b = T0(g + "2")
c = W(g + "2", "Zeus")
d = W(g + "2", "Es")
FX += SYNC(n, [(b, 23.7), (W(g + "2", "provoca"), 27.5), (c, 29)])
FX += PZ(n, c, NX(g + "2"), 29, [
    an(.49, .385, "Caps", "EN MEDIO DE TODOS", "G2", c, "Galio", lado="der"),
    an(.47, .635, "Kanavi", None, "HLE", c + .15, "JarvanIV", lado="der", r=38),
    an(.395, .60, "Zeka", None, "HLE", c + .3, "Swain", lado="izq", r=38),
    an(.345, .43, "Gumayusi", None, "HLE", c + .45, "Lucian", lado="izq", r=38),
    an(.33, .39, "Delight", None, "HLE", c + .6, "Milio", lado="arriba", r=34),
], d3="g2hl1b")
FX += [gris(c, "Zeus", "HLE", "21:48 · la única baja", .08, NX(g + "2")),
       dict(tipo="destello", en=c, fuerza=.45)]
b = T0(g + "3")
u, v = W(g + "3", "Kanavi"), W(g + "3", "ace")
w = W(g + "3", "Hanwha")
FX += SYNC(n, [(b, 29), (u, 42.3), (v, 50), (w, 54), (e1, 58)])
FX += [tar(b + .1, u, "Gumayusi: triple", "22:02", A, icono="Lucian", x=.72, y=.84, tam=46),
       tar(u, v, "Kanavi remata a Hans Sama", "22:10", A, icono="JarvanIV", x=.72, y=.84, tam=46),
       dict(tipo="destello", en=v, fuerza=.55),
       tar(v, w, "Ace · 5 por 1", None, A, logo="HLE", dato="5-1", x=.72, y=.84, tam=46),
       elim(w, e1, "G2", "G2 Esports", "1-3 · fuera del Mundial", [W(g + "3", "G2")])]

# ================================================================== LA MESA TRAS CUATRO RONDAS
g = "tabla4_"
e0, e1 = ESC("tabla4")
d = W(g + "2", "muerte") + .2
FX += [CLIP("lyig_j1", e0, e1, 37, 62),
       mg(L.tablero_suizo("Así quedó la mesa tras cuatro rondas", COLS, LOG, [R3, R4a, R4b, R4c]), e0 + .05, d,
          [W(g + "0", "T1"), W(g + "1", "CFO"), W(g + "2", "seis")], y=.5, nombre="tablero R4"),
       mg(L.resultados("Sábado · tres cruces a muerte", [(EQ("KC"), "Karmine Corp", EQ("MKOI"), "Movistar KOI", None, "VS"),
                                                          (EQ("LOS"), "Los Grandes", EQ("LYON"), "LYON", None, "VS"),
                                                          (EQ("HLE"), "Hanwha Life", EQ("BLG"), "Bilibili", None, "VS")]),
          d, e1, [W(g + "2", "Karmine"), W(g + "2", "Los"), W(g + "2", "Hanwha")], y=.5, nombre="cruces R5")]
# ── ACTO B: aquí siguen las 3 series del sábado, premios, llave y cierre ───────────────────────────────────────────────────────



def matadores(k, lista, x=.92, y=.3):
    """quien remata, cuando la voz lo nombra: medallón chico en el borde derecho. lista = [(palabra, aparición, jugador)]"""
    ts = [W(k, p, m) for p, m, _ in lista]
    fin = T1(k) + .2
    return [cam(t, j, j, dur=min((ts[i + 1] if i + 1 < len(ts) else fin) - t, 2.6), x=x, y=y, tam=190) for i, (t, (_, _, j)) in enumerate(zip(ts, lista))]


FX += matadores("t1ko_j_3", [("Oner", 0, "Oner"), ("Doran", 0, "Doran"), ("Keria", 0, "Keria"), ("Peyz", 0, "Peyz"), ("Faker", 0, "Faker")])
FX += matadores("t1ko_peor_1", [("Doran", 0, "Doran"), ("Keria", 0, "Keria"), ("Doran", 1, "Doran")])
FX += matadores("lyig_j1_3", [("Inspired", 0, "Inspired"), ("Berserker", 0, "Berserker"), ("Dhokla", 0, "Dhokla")])
FX += matadores("lyig_j2_3", [("Inspired", 0, "Inspired"), ("JiaQi", 0, "JiaQi"), ("Isles", 0, "Isles")])
FX += matadores("kccf_j_2", [("Yike", 0, "Yike"), ("Canna", 0, "Canna"), ("Yike", 1, "Yike")])
FX += matadores("kccf_peor_1", [("Yike", 0, "Yike")])
FX += matadores("blte_peor_2", [("Tian", 0, "Tian"), ("369", 0, "369"), ("JackeyLove", 0, "JackeyLove")])
FX += matadores("blte_j_3", [("369", 0, "369"), ("Creme", 0, "Creme"), ("JackeyLove", 0, "JackeyLove"), ("369", 1, "369")])
FX += matadores("lotl_j_3", [("Ackerman", 0, "Ackerman")])
FX += matadores("g2hl_j_3", [("Gumayusi", 0, "Gumayusi"), ("Kanavi", 0, "Kanavi")])

# ================================================================== SÁBADO · KARMINE vs MOVISTAR KOI (datos_kcmk.md)
K.update({"kcmk_j1": 2201, "kcmk_j2": 210, "kcmk_j3": 1744, "kcmk_fb": 890, "kcmk_alma": 1376, "kcmk_baron": 1698, "kcmk_cierre1": 2380,
          "kcmk_ely2": 380, "kcmk_fin": 1548})
AZUL = {"KC"}
TV1, TV2 = "Transmisión oficial · KC vs KOI · partida 1", "Transmisión oficial · KC vs KOI · partida 2"
g = "kcmk_res_"
e0, e1 = ESC("kcmk_res")
b = T0(g + "1")
u, v, w = W(g + "1", "Luego"), W(g + "1", "Baron"), W(g + "1", "minuto")
FX += [J("kcmk_j1", e0, b, 0), J("kcmk_fb", b, u, 4.5 - (u - b)), J("kcmk_alma", u, v, 7.5 - (v - u)), J("kcmk_baron", v, w, 8.6 - (w - v)),
       J("kcmk_j3", w, e1, 1.0),
       tar(e0 + .15, W(g + "0", "Karmine"), "Sábado", "31 de octubre", "oro", x=.5, y=.17, tam=66),
       vs(W(g + "0", "Karmine"), T1(g + "0") + .2, "KC", "MKOI", "A muerte", "Los dos con 2-2 · el que pierde se va", y=.42),
       tar(b + .1, u, "14 minutos · 0 a 0", "Ni una sola muerte", "oro", x=.72, y=.84, tam=46),
       tar(u, v, "Alma infernal", "Karmine · 23:03", A, logo="KC", x=.72, y=.84, tam=46),
       tar(v, w, "Barón", "Karmine · 28:26", A, logo="KC", x=.72, y=.84, tam=46),
       tar(w, e1, "KC +1,6K", "Minuto 29", A, logo="KC", x=.72, y=.84, tam=46)]

g = "kcmk_j3_"
n = "kcmk_j3"
e0, e1 = ESC("kcmk_j3")
FX += VIVO("kcmk_j3", n, 12, TV1, "KC", "Minuto 29")
a = T0(g + "0")
FX += REBX(n, a, 12 + (a - e0), NX(g + "0"), 12)
FX += [tar(W(g + "0", "mejora"), NX(g + "0"), "Mejora del Barón: +1 417", "29:16", A, logo="KC", x=.76, y=.17, tam=40),
       tar(W(g + "0", "kyeahoo"), NX(g + "0"), "kyeahoo, tirando una torre", "Aparte de su equipo", "oro", x=.24, y=.17, tam=40),
       cam(W(g + "0", "kyeahoo"), "kyeahoo", "kyeahoo · Syndra", dur=NX(g + "0") - W(g + "0", "kyeahoo"), x=.09, y=.42)]
b = T0(g + "1")
c = W(g + "1", "Un")
d = W(g + "2", "Jojopyun")
FX += MESA2("kcmk3", b, c, H(n, 12))
FX += [cam(W(g + "1", "Myrwn"), "Myrwn", "Myrwn · Camille", dur=c - W(g + "1", "Myrwn"), x=.91, y=.3)]
FX += LEN(n, c, d, 12, 16.5)
FX += [tar(c + .1, d, "«Se regaló»", "Un narrador", "oro", x=.5, y=.17, tam=48)]
b, u, v, w, x_ = d, W(g + "2", "Supa"), W(g + "2", "Myrwn"), W(g + "2", "Elyoya"), W(g + "2", "Jojopyun", 1)
y_ = W(g + "2", "ace")
c = T0(g + "3")
FX += SYNC(n, [(b, 16.5), (u, 21), (v, 23), (w, 32), (x_, 56 - (y_ - x_)), (y_, 56), (W(g + "3", "Anciano"), 60), (e1, 60 + e1 - W(g + "3", "Anciano"))])
d = W(g + "3", "En")
FX += [gris(b, "Caliste", "KC", "29:20", .08, d), gris(u, "kyeahoo", "KC", "29:25", .21, d), gris(v, "Busio", "KC", "29:27", .34, d),
       gris(w, "Yike", "KC", "29:36", .47, d), gris(y_, "Canna", "KC", "30:00", .60, d),
       dict(tipo="destello", en=b, fuerza=.45), dict(tipo="destello", en=y_, fuerza=.55),
       tar(c, d, "5 por 0 y el Anciano", "30:04", R, logo="MKOI", dato="5-0", x=.72, y=.84, tam=46),
       peor(d, e1, "Lo peor de Karmine", "Caliste", "KC", ["Aturdido 29:16, muerto 29:20", "De +1,6K a -3,0K en 48 segundos"],
            [W(g + "3", "cuarenta"), W(g + "3", "tres")], "Tirador · Ashe")]
FX += matadores(g + "2", [("Jojopyun", 0, "Jojopyun"), ("Supa", 0, "Supa"), ("Myrwn", 0, "Myrwn"), ("Elyoya", 0, "Elyoya"), ("Jojopyun", 1, "Jojopyun")])

g = "kcmk_j1_"
n = "kcmk_j1"
e0, e1 = ESC("kcmk_j1")
FX += VIVO("kcmk_j1", n, 28, TV1, "KC", "Minuto 37")
a = T0(g + "0")
FX += REBX(n, a, 28 + (a - e0), NX(g + "0"), 27 - (T0(g + "2") - T0(g + "1")))
FX += [tar(W(g + "0", "tres"), NX(g + "0"), "KC -3,0K", None, R, logo="MKOI", x=.76, y=.17, tam=40),
       tar(W(g + "0", "Anciano"), NX(g + "0"), "Otro Anciano en juego", None, "oro", x=.24, y=.17, tam=40)]
b = T0(g + "1")
c = T0(g + "2")
FX += [J(n, b, c, 27 - (c - b), 1.0),
       cam(b, "kyeahoo", "kyeahoo · Syndra", dur=c - b, x=.09, y=.42),
       tar(W(g + "1", "narradores"), W(g + "1", "cinco"), "Volvió a base", "Según los narradores", "oro", x=.76, y=.17, tam=40),
       tar(W(g + "1", "cinco"), c, "5 contra 4", "KC sin kyeahoo", R, logo="MKOI", x=.72, y=.84, tam=46)]
b = c
c = W(g + "2", "Replegarse")
FX += LEN(n, b, c, 27, 30)
FX += [cam(W(g + "2", "Myrwn"), "Myrwn", "Myrwn · Camille", dur=c - W(g + "2", "Myrwn"), x=.91, y=.3)]
FX += PZ(n, c, NX(g + "2"), 30, [
    zona(.43, .53, .12, .17, R, c + .1, alfa=.2),
    texto("EL HEXÁGONO DE MYRWN", "SOBRE CALISTE", .73, .62, c + .1, color=R),
    an(.54, .38, "Busio", None, "KC", c + .3, "Seraphine", lado="der", r=38),
    texto("REPLEGARSE = PERDER", "LOS NARRADORES", .25, .25, c + .5, color=Y),
], d3="kcmk1a")
b = T0(g + "3")
c = W(g + "3", "Canna", 1)
FX += TRAMO(n, b, c, 30, 35)
FX += [cam(W(g + "3", "Canna"), "Canna", "Canna · Renekton", dur=c - W(g + "3", "Canna"), x=.91, y=.3)]
FX += MESA2("kcmk1", c, NX(g + "3"), H(n, 35))
b = T0(g + "4")
u, v = W(g + "4", "Myrwn"), W(g + "4", "Canna")
c = T0(g + "5")
w = W(g + "5", "Veinticinco")
x_ = W(g + "5", "Baron")
d = T0(g + "6")
FX += SYNC(n, [(b, 35), (u, 38), (v, 40), (c, 40 + c - v), (w, 49), (x_, 74), (d, 74 + d - x_)])
FX += [gris(b, "Elyoya", "MKOI", "37:16", .08, c), gris(u, "Myrwn", "MKOI", "37:19 · doble", .21, c), gris(v, "Canna", "KC", "37:21", .34, c),
       dict(tipo="destello", en=b, fuerza=.45), dict(tipo="destello", en=u, fuerza=.5),
       tar(c + .1, w, "De 15 327 a 0", "Anciano · 9 segundos · 37:30", A, logo="KC", x=.72, y=.84, tam=46),
       dict(tipo="destello", en=w, fuerza=.45),
       tar(x_, d, "Barón", "37:55", A, logo="KC", x=.72, y=.84, tam=46)]
FX += matadores(g + "4", [("Caliste", 0, "Caliste")])
FX += [J("kcmk_cierre1", d, e1, 17 - (e1 - d)),
       tar(W(g + "6", "dos"), W(g + "6", "Karmine"), "KC +2,5K", "Minuto 40", A, logo="KC", x=.76, y=.17, tam=40),
       tar(W(g + "6", "Karmine"), e1, "13 a 14", "Y Karmine gana la partida", A, logo="KC", dato="1-0", x=.72, y=.84, tam=46)]

g = "kcmk_j2_"
n = "kcmk_j2"
e0, e1 = ESC("kcmk_j2")
FX += VIVO("kcmk_j2", n, 33, TV2, "KC", "Minuto 4")
a = T0(g + "0")
c = W(g + "0", "Myrwn")
FX += REBX(n, a, 33 + (a - e0), c, 31)
FX += PZ(n, c, NX(g + "0"), 31, [
    an(.40, .48, "Canna", "RUMBLE", "KC", c, "Rumble", lado="izq", r=46),
    an(.405, .34, "Myrwn", None, "MKOI", c + .1, "Ornn", lado="izq", r=40),
    an(.56, .275, "Elyoya", None, "MKOI", W(g + "0", "Elyoya"), "LeeSin", lado="der", r=40),
    texto("2 CONTRA 1", None, .72, .55, W(g + "0", "Dos"), color=R),
], d3="kcmk2a")
b = T0(g + "1")
c = T0(g + "2")
FX += LEN(n, b, c, 31, 36)
FX += [tar(b + .1, W(g + "1", "Canna"), "Canna: 40 % de vida", "04:04", R, logo="KC", x=.76, y=.17, tam=40),
       tar(W(g + "1", "Canna"), c, "No gasta el Destello", "Los narradores: «muy confiados»", A, logo="KC", x=.72, y=.84, tam=46)]
b = c
c = W(g + "2", "Canna")
FX += LEN(n, b, c, 36, 37)
FX += [cam(W(g + "2", "Yike"), "Yike", "Yike · Pantheon", dur=T1(g + "2") - W(g + "2", "Yike"), x=.91, y=.3)]
FX += PZ(n, c, NX(g + "2"), 37, [
    an(.31, .60, "Canna", "SACA EL FUEGO", "KC", c, "Rumble", lado="izq", r=46),
    an(.405, .535, "Myrwn", "ATURDIDO", "MKOI", c + .15, "Ornn", lado="der", r=40),
    an(.505, .35, "Elyoya", None, "MKOI", c + .3, "LeeSin", lado="der", r=38),
], d3="kcmk2b")
b = T0(g + "3")
c = W(g + "3", "Canna")
d = W(g + "3", "lo")
u = W(g + "3", "Dos")
FX += SYNC(n, [(b, 37), (W(g + "3", "primera"), 39), (c, 43)])
FX += PZ(n, c, d, 43, [
    an(.33, .30, "Elyoya", "CASI MUERTO", "MKOI", c, "LeeSin", lado="izq", r=40),
    an(.335, .555, "Canna", "A UN HILO", "KC", c + .1, "Rumble", lado="izq", r=40),
    an(.43, .50, "Yike", None, "KC", c + .2, "Pantheon", lado="der", r=38),
    ruta(n, 43, [(37.0, .31, .60), (41.0, .49, .69), (43.0, .335, .555)], A, c + .1),
    ruta(n, 43, [(37.0, .505, .35), (41.0, .375, .33), (43.0, .33, .30)], R, c + .2),
])
FX += SYNC(n, [(d, 43), (NX(g + "3"), 43 + NX(g + "3") - d)])
FX += [gris(W(g + "3", "primera"), "Myrwn", "MKOI", "04:09 · primera sangre", .08, NX(g + "3")),
       gris(W(g + "3", "remata"), "Elyoya", "MKOI", "04:14", .21, NX(g + "3")),
       dict(tipo="destello", en=W(g + "3", "primera"), fuerza=.45), dict(tipo="destello", en=W(g + "3", "remata"), fuerza=.5),
       tar(u, NX(g + "3"), "2 por 0", "Con Canna a un hilo", A, logo="KC", dato="2-0", x=.72, y=.84, tam=46)]
b = T0(g + "4")
c = W(g + "4", "Veintiseis")
FX += [J("kcmk_fin", b, e1, 2),
       tar(b + .1, c, "Karmine, siempre arriba", "Desde el minuto 5", A, logo="KC", x=.72, y=.84, tam=46),
       tar(c, e1, "18 a 4 · +15,3K", "Partida 2 · 26:07", A, logo="KC", dato="2-0", x=.72, y=.84, tam=46)]
_t_fin = 2 + e1 - b

g = "kcmk_peor_"
e0, e1 = ESC("kcmk_peor")
FX += [J("kcmk_ely2", e0, e1, 1.5),
       peor(W(g + "0", "Elyoya"), e1, "Lo peor de KOI", "Elyoya", "MKOI", ["Partida 2: 1/5/2", "Dos muertes antes del minuto 7", "9,8 % del daño · su soporte, 15,4 %"],
            [W(g + "0", "asesinato"), W(g + "0", "dos"), W(g + "0", "daño")], "Jungla · Lee Sin")]

g = "kcmk_mvp_"
e0, e1 = ESC("kcmk_mvp")
b = T0(g + "1")
c = W(g + "1", "Movistar")
FX += [J("kcmk_fin", e0, b, _t_fin), J("kcmk_fin", b, e1, _t_fin + b - e0),
       mg(L.premio("Mejor de la serie", JUG("Yike"), "Yike", EQ("KC"), ["11/2/14 · 11 de 31 asesinatos", "Partida 2: 9/0/5 con Pantheon", "23,8 % del daño"], color="oro", sub="Jungla · Karmine Corp"),
          W(g + "0", "Yike"), b, [W(g + "0", "once"), W(g + "0", "segunda")], y=.5, nombre="premio Yike"),
       tar(b + .1, c, "Karmine, a cuartos", "3-2", A, logo="KC", x=.72, y=.84, tam=46),
       elim(c, e1, "MKOI", "Movistar KOI", "2-3 · fuera del Mundial", [W(g + "1", "Mundial")])]

# ================================================================== SÁBADO · LOS GRANDES vs LYON (datos_loly.md)
K.update({"loly_j1": 2374.5, "loly_j2": 1729, "loly_j3": 1994, "loly_fin2": 2729.5, "loly_b1": 2032, "loly_fin3": 2181})
AZUL = {"LOS"}
TV2, TV3 = "Transmisión oficial · LOS vs LYON · partida 2", "Transmisión oficial · LOS vs LYON · partida 3"
g = "loly_res_"
e0, e1 = ESC("loly_res")
b = T0(g + "1")
FX += [J("loly_b1", e0, b, 0), J("loly_j1", b, e1, 0),
       vs(e0 + .15, W(g + "0", "pierde") + .6, "LOS", "LYON", "A muerte", "Los dos con 2-2 · el que pierde se va", y=.42),
       tar(W(g + "0", "primera"), b, "Partida 1: Los Grandes", "2 Barones · nunca abajo en oro", A, logo="LOS", x=.72, y=.84, tam=46),
       tar(W(g + "1", "ocho"), W(g + "1", "narradores"), "LOS +8,4K", "Partida 2 · minuto 38", A, logo="LOS", x=.72, y=.84, tam=46),
       tar(W(g + "1", "narradores"), e1, "«Tienen que cerrar»", "Los narradores", "oro", x=.72, y=.84, tam=46)]

g = "loly_j1_"
n = "loly_j1"
e0, e1 = ESC("loly_j1")
FX += VIVO("loly_j1", n, 37, TV2, "LYON", "Minuto 40")
a = T0(g + "0")
FX += REBX(n, a, 37 + (a - e0), T0(g + "1"), 36)
FX += [tar(W(g + "0", "Siete"), T0(g + "1"), "LOS +7,8K", "40:11", A, logo="LOS", x=.76, y=.17, tam=40),
       tar(W(g + "0", "dragon"), T0(g + "1"), "El dragón del alma", None, "oro", x=.24, y=.17, tam=40)]
b = T0(g + "1")
c = W(g + "1", "Lo")
FX += LEN(n, b, c, 36, 39)
FX += [cam(b, "Curse", "Curse · Qiyana", dur=c - b, x=.91, y=.3)]
FX += MESA2("loly1", c, NX(g + "1"), H(n, 39))
b = T0(g + "2")
u, v = W(g + "2", "Inspired"), W(g + "2", "doble")
c = T0(g + "3")
d = W(g + "3", "alma")
FX += SYNC(n, [(b, 39), (u, 42.6), (v, 48.5), (d, 59), (e1, 59 + e1 - d)])
FX += [gris(b + .5, "Curse", "LOS", "40:15", .08, c), gris(u, "Zest", "LOS", "40:17", .21, c), gris(v, "Duduhh", "LOS", "40:23", .34, c),
       dict(tipo="destello", en=b + .5, fuerza=.45), dict(tipo="destello", en=u, fuerza=.45), dict(tipo="destello", en=v, fuerza=.55),
       tar(c, W(g + "3", "Diez"), "3 por 0", "Sin una baja de LYON", R, logo="LYON", dato="3-0", x=.72, y=.84, tam=46),
       tar(d - .5, e1, "Alma de la montaña", "LYON · 40:33", R, logo="LYON", x=.72, y=.84, tam=46)]
FX += matadores(g + "2", [("Berserker", 0, "Berserker"), ("Inspired", 0, "Inspired"), ("Berserker", 1, "Berserker")])

g = "loly_base_"
n = "loly_fin2"
e0, e1 = ESC("loly_base")
c = W(g + "0", "Berserker")
b = T0(g + "1")
FX += [J(n, e0, e1, 72 - (c - e0), 1.0),
       tar(W(g + "0", "inhibidor"), W(g + "0", "Anciano"), "Inhibidor de Berserker", "46:46", R, logo="LYON", x=.72, y=.14, tam=44),
       tar(W(g + "0", "Anciano"), W(g + "0", "pierden"), "Anciano: Los Grandes", "46:47", A, logo="LOS", x=.28, y=.14, tam=44),
       dict(tipo="destello", en=W(g + "0", "nexo"), fuerza=.55),
       tar(W(g + "0", "nexo"), b, "Nexo · 47:02", "Base race", R, logo="LYON", dato="1-1", x=.72, y=.84, tam=46),
       tar(W(g + "1", "tres"), e1, "LYON gana con 3,1K menos", "Partida 2 · 47 minutos", R, logo="LYON", x=.72, y=.84, tam=46)]

g = "loly_j2_"
n = "loly_j2"
AZUL = {"LYON"}
e0, e1 = ESC("loly_j2")
FX += VIVO("loly_j2", n, 35, TV3, "LYON", "Minuto 29")
a = T0(g + "0")
FX += REBX(n, a, 35 + (a - e0), T0(g + "1"), 27)
FX += [tar(W(g + "0", "Baron"), T0(g + "1"), "LOS +1,4K con Barón", "29:16", R, logo="LOS", x=.76, y=.17, tam=40)]
b = T0(g + "1")
c = W(g + "1", "y")
FX += LEN(n, b, c, 27, 29)
FX += [cam(b, "Berserker", "Berserker · Lucian", dur=c - b, x=.09, y=.42)]
FX += PZ(n, c, NX(g + "1"), 29, [
    texto("BERSERKER, ADELANTADO", "«UN ERROR GRAVÍSIMO»", .62, .25, c + .1, color=A),
    an(.345, .39, "Feisty", None, "LOS", c + .3, "Ryze", lado="izq", r=38),
    an(.29, .56, "Ackerman", None, "LOS", c + .45, "Renata", lado="izq", r=38),
    an(.21, .60, "Curse", None, "LOS", c + .6, "Chogath", lado="izq", r=42),
    an(.46, .59, "Dhokla", None, "LYON", c + .75, "KSante", lado="der", r=40),
    an(.55, .60, "Isles", None, "LYON", c + .9, "Milio", lado="der", r=36),
], d3="loly2a")
b = T0(g + "2")
c = T0(g + "4")
d = W(g + "4", "Inspired")
FX += [J(n, b, d, 29, 1.0)]
_t = 29 + d - b
FX += REBX(n, d, _t, e1, 42.5)
FX += [gris(W(g + "2", "Berserker"), "Berserker", "LYON", "29:22", .08, c), gris(W(g + "2", "mata", 1), "Duduhh", "LOS", "29:26", .21, c),
       gris(W(g + "3", "Ackerman"), "Ackerman", "LOS", "29:30", .34, c), gris(W(g + "3", "doble"), "Feisty", "LOS", "29:36", .47, c),
       dict(tipo="destello", en=W(g + "2", "mata", 1), fuerza=.45), dict(tipo="destello", en=W(g + "3", "doble"), fuerza=.55),
       tar(c, d, "3 por 1", "Con el Barón en contra", A, logo="LYON", dato="3-1", x=.72, y=.84, tam=46),
       cam(d, "Inspired", "Inspired · Nocturne", dur=e1 - d, x=.91, y=.3)]
FX += matadores(g + "3", [("Saint", 0, "Saint")])

g = "loly_j3_"
n = "loly_j3"
e0, e1 = ESC("loly_j3")
FX += VIVO("loly_j3", n, 31, TV3, "LYON", "Minuto 33")
a = T0(g + "0")
FX += REBX(n, a, 31 + (a - e0), T0(g + "1"), 31.5)
FX += [tar(W(g + "0", "Zest"), T0(g + "1"), "Zest, casi sin vida", "33:47", R, logo="LOS", x=.76, y=.17, tam=40)]
b = T0(g + "1")
FX += MESA2("loly3", b, NX(g + "1"), H(n, 31.5))
b = T0(g + "2")
u, v = W(g + "2", "Ackerman"), W(g + "2", "doble")
w = W(g + "2", "LYON")
d = W(g + "2", "inhibidor")
c = T0(g + "3")
FX += SYNC(n, [(b, 31.5), (u, 38), (v, 41), (w, 65 - (d - w)), (d, 65), (e1, 65 + e1 - d)])
FX += [gris(u, "Ackerman", "LOS", "33:52", .08, w), gris(v, "Duduhh", "LOS", "33:55", .21, w),
       dict(tipo="destello", en=u, fuerza=.45), dict(tipo="destello", en=v, fuerza=.55),
       tar(d - .4, c, "Inhibidor · 34:19", None, A, logo="LYON", x=.72, y=.84, tam=46),
       peor(c, e1, "Lo peor de Los Grandes", "Ackerman", "LOS", ["Partida 3: 0/5/3", "Serie: 1/7/14"], [W(g + "3", "sin"), W(g + "3", "cinco")], "Soporte · Renata")]
FX += matadores(g + "2", [("Berserker", 0, "Berserker")])

g = "loly_fin_"
e0, e1 = ESC("loly_fin")
b = T0(g + "1")
c = W(g + "1", "Los")
FX += [J("loly_fin3", e0, e1, 0),
       mg(L.premio("Mejor de la serie", JUG("Berserker"), "Berserker", EQ("LYON"), ["16/8/8 · 16 de 34 asesinatos", "39,2 % del daño en la partida 3", "Doble en las jugadas clave"], color="oro", sub="Tirador · LYON"),
          W(g + "0", "Berserker"), W(g + "0", "Inspired") - .1, [W(g + "0", "dieciseis")], y=.5, nombre="premio Berserker"),
       cam(W(g + "0", "Inspired"), "Inspired", "Inspired · 6/1/17", dur=b - W(g + "0", "Inspired"), x=.09, y=.42),
       tar(b + .1, W(g + "1", "Rodolfo"), "LYON, a cuartos", "3-2", A, logo="LYON", x=.72, y=.84, tam=46),
       com(W(g + "1", "Rodolfo"), "UgyZTKk5Cq0R2nYl7zN4AaABAg", c - W(g + "1", "Rodolfo"), y=.42),
       elim(c, e1, "LOS", "Los Grandes", "2-3 · fuera del Mundial", [W(g + "1", "Mundial")])]

# ================================================================== SÁBADO · HANWHA vs BILIBILI (datos_hlbl.md)
K.update({"hlbl_j1": 2402.5, "hlbl_g2": 1722.0, "hlbl_g2f": 1942.0})    # P2: VOD KH4HTOTtrGI (HUD = VOD − 463), tramos 2185 y 2405 +40 s
AZUL = {"BLG"}
TVH1 = "Transmisión oficial · HLE vs BLG · partida 1"
HG2, HG2_T, HG2F, HG2F_T = "hlbl_g2", (18.4, 30.4), "hlbl_g2f", (5.5, 17.6)    # P2: pelea 29:00-29:12 (doble, triple, ace) · nexo 32:38 y festejo
g = "hlbl_res_"
e0, e1 = ESC("hlbl_res")
b = T0(g + "1")
FX += [CLIP("hlbl_j1", e0, e1, 22, 41.6),
       vs(e0 + .15, W(g + "0", "pierde") + .6, "HLE", "BLG", "A muerte", "Los dos con 2-2 · el que pierde se va", y=.42),
       tar(W(g + "1", "Baron"), W(g + "1", "minuto", 1), "Partida 1: Hanwha manda", "Barón 36:12 · torres 7-3 · inhibidor", R, logo="HLE", x=.72, y=.84, tam=46),
       tar(W(g + "1", "minuto", 1), e1, "HLE +5,6K", "Minuto 39", R, logo="HLE", x=.72, y=.84, tam=46)]

g = "hlbl_j1_"
n = "hlbl_j1"
e0, e1 = ESC("hlbl_j1")
FX += VIVO("hlbl_j1", n, 33.3, TVH1, "BLG", "Minuto 40")
a = T0(g + "0")
c = W(g + "1", "cae")
FX += SYNC(n, [(a, 45.5), (c, 62.4)])
FX += [tar(W(g + "0", "alma"), T0(g + "1") + 2.5, "Alma de la montaña · BLG", "40:47 · y aún HLE +4,2K", A, logo="BLG", x=.72, y=.84, tam=46),
       gris(c, "Bin", "BLG", "41:05", .08, c + 9.0)]
# x1 en vivo: el cuádruple y el ace se ven enteros antes de explicarlos
b = T0(g + "2") + 8.6
FX += SYNC(n, [(c, 62.4), (b, 62.4 + b - c)])
FX += [dict(tipo="destello", en=c + 1.2, fuerza=.45), dict(tipo="destello", en=c + 8.0, fuerza=.55),
       tar(c + 1.4, c + 8.0, "Knight · Orianna", "41:06-41:10", A, icono="Orianna", logo="BLG", x=.72, y=.84, tam=46),
       tar(c + 8.0, b, "Ace · 5 por 1", "41:13", A, logo="BLG", dato="5-1", x=.72, y=.84, tam=46)]
# rebobina y lo repasa lento: cada nombre cuando cae
t_fin = 62.4 + b - c
u = {p: W(g + "2", p) for p in ("Knight", "Kanavi", "Gumayusi", "Zeka", "Zeus", "Cuatro")}
v = T0(g + "3")
w = W(g + "3", "cae")
FX += REB(n, b, t_fin, 62.0)
FX += SYNC(n, [(b + 1.2, 62.0), (u["Kanavi"], 63.5), (u["Gumayusi"], 64.1), (u["Zeka"], 64.6), (u["Zeus"], 67.5), (v, 70.4),
               (W(g + "3", "cinco"), 71.3), (w, 113.5), (e1, 113.5 + e1 - w)])
FX += [x2(b + 1.2, u["Cuatro"], "CÁMARA LENTA"),
       cam(u["Knight"], "Knight", "Knight · Orianna", dur=u["Kanavi"] - u["Knight"], x=.09, y=.42),
       gris(u["Kanavi"], "Kanavi", "HLE", "41:06", .22, v), gris(u["Gumayusi"], "Gumayusi", "HLE", "41:07", .36, v),
       gris(u["Zeka"], "Zeka", "HLE", "41:07", .50, v), gris(u["Zeus"], "Zeus", "HLE", "41:10", .64, v),
       dict(tipo="destello", en=u["Kanavi"], fuerza=.4), dict(tipo="destello", en=u["Zeus"], fuerza=.5),
       tar(u["Cuatro"], v, "Cuádruple de Knight", "4 asesinatos en 4 segundos", A, logo="BLG", dato="4", x=.72, y=.84, tam=46),
       gris(v, "Delight", "HLE", "41:13", .78, W(g + "3", "Cuarenta")),
       tar(W(g + "3", "cinco"), w, "5 por 1 · de -4,2K a ganar", "Partida 1 · 41:56", A, logo="BLG", dato="1-0", x=.72, y=.84, tam=46),
       dict(tipo="destello", en=w, fuerza=.55)]
FX += matadores(g + "3", [("Viper", 0, "Viper")])

g = "hlbl_g2_"
e0, e1 = ESC("hlbl_g2")
b = T0(g + "1")
FX += [CLIP(HG2, e0, b, *HG2_T),
       CLIP(HG2F, b, e1, *HG2F_T),
       tar(W(g + "0", "cuatro"), W(g + "0", "minuto"), "Alma de la montaña · BLG", "Partida 2 · 4 dragones a 1", A, logo="BLG", x=.72, y=.84, tam=46),
       tar(W(g + "0", "minuto"), b, "5 por 1 · 29:05-29:12", "Knight: 3 asesinatos", A, logo="BLG", dato="5-1", x=.72, y=.84, tam=46),
       tar(b, W(g + "1", "peor"), "BLG 14-3 · torres 10-0", "Partida 2 · 32:49", A, logo="BLG", dato="2-0", x=.72, y=.84, tam=46),
       peor(W(g + "1", "peor"), e1, "Lo peor de Hanwha", "Zeus", "HLE", ["Partida 2: 0/4/1", "Serie: 3/8/11"], [W(g + "1", "cero", 1)], "Top · K'Sante")]

g = "hlbl_fin_"
e0, e1 = ESC("hlbl_fin")
b = T0(g + "1")
c = W(g + "1", "Hanwha")
FX += [CLIP("hlbl_j1", e0, e1, 98, 118.5),
       mg(L.premio("Mejor de la serie", JUG("Knight"), "Knight", EQ("BLG"), ["15/1/12 en dos partidas", "Partida 1: cuádruple · 8/1/10", "Partida 2: 7/0/2"], color="oro", sub="Medio · Bilibili Gaming"),
          W(g + "0", "Knight"), b, [W(g + "0", "quince")], y=.5, nombre="premio Knight"),
       tar(b + .1, c, "Bilibili, a cuartos", "3-2", A, logo="BLG", x=.72, y=.84, tam=46),
       elim(c, e1, "HLE", "Hanwha Life", "2-3 · fuera del Mundial", [W(g + "1", "Mundial")])]

# ================================================================== CIERRE
R5 = [["DK", "GEN", "T1", "IG", "TES", "KC", "LYON", "BLG"], [], [], [], ["TSW", "AL", "CFO", "TLAW", "G2", "MKOI", "LOS", "HLE"]]
g = "tabla5_"
e0, e1 = ESC("tabla5")
FX += [CLIP("hlbl_j1", e0, e1, 100, 119),
       mg(L.tablero_suizo("Así termina la fase suiza", COLS, LOG, [R4c, R5]), e0 + .05, e1,
          [W(g + "0", "ultima")], y=.5, nombre="tablero R5")]

g = "sem_jug_"
e0, e1 = ESC("sem_jug")
b, c = T0(g + "1"), T0(g + "2")
FX += [J("t1_g2j2", e0, b, 60), J("kcmk_fin", b, c, 4), J("hlbl_j1", c, e1, 58),
       tar(e0 + .1, W(g + "0", "Tercero"), "Jugadores de la semana", "28 al 31 de octubre · 22 partidas", "oro", x=.5, y=.16, tam=50),
       mg(L.premio("N.º 3 de la semana", JUG("Doran"), "Doran", EQ("T1"), ["10/0/13 en 2 partidas", "Cero muertes contra KOI"], color="oro", sub="Top · T1"),
          W(g + "0", "Doran"), b, [W(g + "0", "diez")], y=.5, nombre="premio Doran"),
       mg(L.premio("N.º 2 de la semana", JUG("kyeahoo"), "kyeahoo", EQ("KC"), ["16/3/33 en 4 partidas a muerte", "KDA 16,3: el mejor de la semana"], color="oro", sub="Medio · Karmine Corp"),
          W(g + "1", "kyeahoo"), c, [W(g + "1", "dieciseis")], y=.5, nombre="premio kyeahoo"),
       mg(L.premio("N.º 1 de la semana", JUG("Knight"), "Knight", EQ("BLG"), ["30 asesinatos en 5 partidas: el que más", "Triple contra TES", "Cuádruple contra Hanwha"], color="oro", sub="Medio · Bilibili Gaming", sello="MVP"),
          W(g + "2", "Knight"), e1, [W(g + "2", "Treinta"), W(g + "2", "triple"), W(g + "2", "cuadruple")], y=.5, nombre="premio Knight semana")]

g = "sem_eq_"
e0, e1 = ESC("sem_eq")
FX += [CLIP("kcmk_fin", e0, e1, 6, 23),
       mg(L.premio("Equipo de la semana", EQ("KC"), "Karmine Corp", EQ("KC"), ["Desde la fase de entrada", "1-2 tras tres rondas", "Esta semana: 4 partidas, 4 victorias"], color="oro", sub="LEC · a cuartos con 3-2"),
          W(g + "0", "Karmine"), e1, [W(g + "0", "fase"), W(g + "0", "tres"), W(g + "1", "Cuatro", 1)], y=.5, nombre="premio KC")]

g = "sem_peor_"
e0, e1 = ESC("sem_peor")
FX += [CLIP("loly_fin2", e0, e1, 60, 92.5),
       mg(L.premio("Lo peor de la semana", EQ("LOS"), "Los Grandes", EQ("LOS"), ["Partida 2: +8,4K y 2 Barones", "20 minutos sin cerrar", "Perdió la serie y el Mundial"],
                   color="rojo", sub="2-3 · eliminado", sello="LO PEOR", gris=True),
          W(g + "0", "Los"), e1, [W(g + "0", "Ocho"), W(g + "0", "veinte"), W(g + "1", "Mundial")], y=.5, nombre="premio LOS")]

g = "llave_"
e0, e1 = ESC("llave")
FX += [CLIP("hlbl_j1", e0, e1, 97, 119),
       mg(L.resultados("Cuartos de final · sorteo", [(EQ("DK"), "Dplus KIA", EQ("BLG"), "Bilibili", None, "VS"),
                                                     (EQ("GEN"), "Gen.G", EQ("LYON"), "LYON", None, "VS"),
                                                     (EQ("KC"), "Karmine", EQ("T1"), "T1", None, "VS"),
                                                     (EQ("TES"), "Top Esports", EQ("IG"), "Invictus", None, "VS")]),
          W(g + "0", "sorteo"), W(g + "1", "mejor"), [W(g + "0", "Dplus"), W(g + "0", "Gen"), W(g + "0", "Karmine"), W(g + "1", "Top")],
          y=.45, nombre="llave sorteo"),
       tar(W(g + "1", "mejor"), e1, "Al mejor de 5 · eliminación directa", "Del 3 al 6 de noviembre · Allen, Texas", "oro", x=.68, y=.84, tam=46)]

g = "sem_com_"
e0, e1 = ESC("sem_com")
FX += [CLIP("blte_j1", e0, e1, 5, 64),
       com(W(g + "0", "Armando"), "UgxdOinvySjyp4YTe8F4AaABAg", T0(g + "1") - W(g + "0", "Armando"), y=.42),
       com(T0(g + "1"), "UgxTIEi9_E2no9q1M7l4AaABAg", T0(g + "2") - T0(g + "1"), y=.42),
       com(T0(g + "2"), "Ugy-sQZodyVx3gitmzB4AaABAg", W(g + "2", "Aunque") - T0(g + "2"), y=.42),
       tar(W(g + "2", "Aunque"), T0(g + "3"), "Pausa de CFO: 29 minutos", "Vista entera · jueves", "oro", x=.72, y=.84, tam=46),
       tar(T0(g + "3"), e1, "Todos los comentarios se leen", "Nos vemos en los cuartos", "oro", x=.5, y=.84, tam=50)]

# narración ORIGINAL donde la voz calla y el VOD corre a x1 (los ESPACIOS_VOZ y los `post`): vivos_audio.py la corta de aquí
_pal = sorted((w["s"], w["e"]) for f_ in _FR.values() for w in f_["words"])
_ya = [(x[3], x[4]) for x in AUD_VIVOS]
for p, q in [(u[1], v[0]) for u, v in zip(_pal, _pal[1:]) if v[0] - u[1] >= 1.2] + [(_pal[-1][1], _TL["total"])]:
    for f_ in FX:
        if f_.get("tipo") != "video" or not .97 <= f_.get("vel", 1) <= 1.03 or "_fuente" not in f_["ruta"] or "mesa_" in f_["ruta"]:
            continue
        u, v = max(p, f_["de"]), min(q, f_["a"])
        if v - u >= .8 and not any(u < y and x < v for x, y in _ya):
            AUD_VIVOS.append((next(e["id"] for e in _TL["escenas"] if e["t0"] <= u < e["t1"]), f_["ruta"], round(f_["desde"] + u - f_["de"], 3),
                              round(u, 3), round(v, 3)))
AUD_VIVOS.sort(key=lambda x: x[3])

ROTULOS = []
SFX = {}
_entra = sorted({e.get("de", e.get("en", 0)) for e in FX if e.get("tipo") == "mg" and not e.get("nombre", "").startswith(("pizarra", "rebobinar", "3D"))})
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

if __name__ != "__main__":
    # tiempos para los scripts auxiliares (mesas_3d.py, vivos_audio.py)
    _t = "# lo escribe efectos.py: (de, a) de cada mesa 3D en el video\nTIEMPOS = " + repr({k: v for k, v in TIEMPOS_MESAS.items()}) + "\n"
    _p = os.path.join(_D, "tiempos_mesas.py")
    if not os.path.exists(_p) or open(_p, encoding="utf-8").read() != _t:
        open(_p, "w", encoding="utf-8").write(_t)
    _p = os.path.join(_D, "investigacion", "vivos.json")
    _t = _json.dumps(AUD_VIVOS, ensure_ascii=False, indent=0)
    if not os.path.exists(_p) or open(_p, encoding="utf-8").read() != _t:
        open(_p, "w", encoding="utf-8").write(_t)
