# -*- coding: utf-8 -*-
"""Capa de EFECTOS de la previa de la final de la Worlds 2026 (Gen.G vs BLG, ~25 min; docs/estilo_analisis_tactico.md), gramática
de videos/lol_semana2/efectos.py (helpers copiados: J, CLIP, TRAMO, P/PZ, REB/REBX, LENTA, MESA, V3, VIVO, SYNC, com, sil, peg, tar).
Fuentes: medios/_fuente/<n>.mp4 (j1..j6 = jugadas, r_* = relleno; datos en investigacion/datos_jN.md y datos_relleno.md) y, para
la fase suiza de BLG, las de lol_semana2 (EXT). Colores = lado del mapa en cada partida (AZUL). Anclas a la voz: T0/T1/W/NX.
FORMAS NUEVAS de presentar las jugadas (el usuario, 10-nov: «me gustan todas menos de la 7 a la 10, bueno la 8 si me gusta»; SE SUMAN):
  1 VOD → Grieta 3D sin corte (la mesa sube a vista cenital y funde con la Grieta) · 2 bullet time (la mesa da media vuelta)
  3 pantalla dividida (VOD + ventanas con zoom a cada protagonista) · 4 marcador de pelea tipo NFL (mg_lol_pelea.marcador_pelea)
  5 oro en vivo del feed (mg_lol_pelea.oro_vivo) · 6 «LO QUE PODÍA HACER» (ruta fantasma rotulada) · 8 visión y niebla (Grieta 3D).
  «para que las apliques TODAS»: 4 y 5 en las seis · j1 3 · j2 2+6 · j3 1+8+2 · j4 3+6 · j5 2+3 · j6 1+6+8 (ESTADO § Presentación ELEGIDA).
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


EXT = {"hlbl_j1": ("lol_semana2", "hlbl_j1"), "blte_j1": ("lol_semana2", "blte_j1"), "blte_j2": ("lol_semana2", "blte_j2"),
       "blte_j3": ("lol_semana2", "blte_j3"), "blte_g3": ("lol_semana2", "blte_g3"), "hlbl_g2": ("lol_semana2", "hlbl_g2")}


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


K = {}          # HUD = t_fuente + K[n] (lo llenan las secciones con los datos medidos: datos_jN.md / datos_relleno.md)


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




# ───────────────────────────────────────── formas nuevas (nucleo/mg_lol_pelea.py) ─────────────────────────────────────────
import mg_lol_pelea as MP  # noqa: E402

ROSTER = {"GEN": "Kiin Canyon Chovy Ruler Duro", "BLG": "Bin Xun Knight Viper ON", "T1": "Doran Oner Faker Peyz Keria",
          "IG": "TheShy Wei Rookie JiaQi Meiko", "LYON": "Dhokla Inspired Saint Berserker Isles",
          "DK": "Siwoo Lucid ShowMaker Smash Career"}


def _eq(cod, color):
    return dict(logo=EQ(cod), cod=cod, color=color, jugadores=[(j, JUG(j)) for j in ROSTER[cod].split()])


def marcador(de, a, izq, der, muertes, marcas, titulo="LA PELEA", y=.885, escala=.78):
    """FORMA 4 · barra NFL al pie: izq/der = códigos (color = lado del mapa); muertes = [(«izq»|«der», índice en ROSTER)] en el
    orden de las marcas (instantes ABSOLUTOS del video, uno por muerte)"""
    fn = MP.marcador_pelea(_eq(izq, COLOR(izq)), _eq(der, COLOR(der)), muertes, titulo)
    import cv2 as _cv
    f2 = (lambda dt, dur, m: _cv.resize(fn(dt, dur, m), None, fx=escala, fy=escala, interpolation=_cv.INTER_AREA)) if escala != 1 else fn
    return mg(f2, de, a, marcas, x=.5, y=y, nombre="marcador " + titulo)


def oro(de, a, gid, g0, g1, claves, marcas, azul, rojo, notas=(), titulo="Diferencia de oro", x=.74, y=.27, escala=.62, desfase=0.0):
    """FORMA 5 · la curva de oro del feed (investigacion/oro_<gid>.json, cada 10 s) se dibuja en vivo: claves = segundo de juego que
    alcanza la línea en cada marca (absoluta). desfase = reloj del feed − HUD (para pasar las claves de HUD al feed)."""
    d = _json.load(open(os.path.join(_D, "investigacion", f"oro_{gid}.json")))
    serie = [(s - desfase, v) for s, v, *_ in d if g0 <= s - desfase <= g1]
    fn = MP.oro_vivo(titulo, serie, claves, (EQ(azul), azul), (EQ(rojo), rojo), notas)
    import cv2 as _cv
    f2 = lambda dt, dur, m: _cv.resize(fn(dt, dur, m), None, fx=escala, fy=escala, interpolation=_cv.INTER_AREA)
    return mg(f2, de, a, marcas, x=x, y=y, nombre="oro " + gid)


# ───────────────────────────────────────── secciones (dos archivos para trabajar en paralelo) ─────────────────────────────
TIEMPOS_3D = {}          # {"j3": dict(de, a, reloj=[[t_video, seg_juego]])} → tiempos_3d.py (lo leen j3_3d.py / j6_3d.py)
for _sec in ("fx_escenas.py", "fx_jugadas.py"):
    _p = os.path.join(_D, _sec)
    if os.path.exists(_p):
        exec(compile(open(_p, encoding="utf-8").read(), _p, "exec"))

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
    # tiempos para los scripts auxiliares (mesas_3d.py, j3_3d.py/j6_3d.py, vivos_audio.py)
    for _nom, _var, _val in (("tiempos_mesas.py", "TIEMPOS", {k: v for k, v in TIEMPOS_MESAS.items()}), ("tiempos_3d.py", "TIEMPOS", TIEMPOS_3D)):
        _t = f"# lo escribe efectos.py\n{_var} = " + repr(_val) + "\n"
        _p = os.path.join(_D, _nom)
        if not os.path.exists(_p) or open(_p, encoding="utf-8").read() != _t:
            open(_p, "w", encoding="utf-8").write(_t)
    _p = os.path.join(_D, "investigacion", "vivos.json")
    _t = _json.dumps(AUD_VIVOS, ensure_ascii=False, indent=0)
    if not os.path.exists(_p) or open(_p, encoding="utf-8").read() != _t:
        open(_p, "w", encoding="utf-8").write(_t)
