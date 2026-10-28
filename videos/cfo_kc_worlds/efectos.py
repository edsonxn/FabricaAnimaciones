# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «CFO vs KC» (estilo análisis táctico, docs/estilo_analisis_tactico.md), copiada en su forma de
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
        _CAMS[n] = _json.load(open(os.path.join(_D, "investigacion", f"cam_j{n}.json")))
    return RV.ruta_en(_CAMS[n], t_ref, puntos)


def ruta(n, t_ref, puntos, color, en, etiqueta=None, off=(0, -50), dur=1.0):
    """flecha CONTINUA de la ruta hecha (de dónde vino) hasta su posición en el cuadro congelado"""
    pts = RUTA(n, t_ref, puntos)
    if len(pts) < 2:
        print(f"  AVISO ruta j{n}@{t_ref}: {puntos} cruza un corte de cámara → sin flecha")
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
    col = {"CFO": R, "KC": A}
    return mg(L.duelo((JUG(na), na, EQ(ea), col[ea], sa), (JUG(nb), nb, EQ(eb), col[eb], sb), titulo, filas), de, a, marcas,
              y=.5, nombre=f"duelo {na}-{nb}")


def repeticion(de, a, sub="Cámara lenta"):
    return [tar(de, a, "Repetición", sub, R, x=.12, y=.13, tam=34), dict(tipo="destello", en=de, fuerza=.35)]


# ================================================================== GANCHO
g = "gancho_"
FX = [
    mg(L.apertura("CFO vs KC", "Worlds 2026 · fase suiza · a muerte"), 0.0, W(g + "0", "dos"), x=.5, y=.5, nombre="apertura"),
    dict(tipo="destello", en=0.15, fuerza=.7),
    vs(W(g + "0", "dos"), T1(g + "0") + .2, "CFO", "KC", "Hoy · 2:00 p. m. · al mejor de 3", "29 de octubre · Allen, Texas", y=.42),
    tar(W(g + "0", "despide"), T1(g + "0") + .2, "El que pierda, se va a casa", None, R, x=.5, y=.84, tam=50),
    gran(T0(g + "1"), EQ("CFO"), "CTBC Flying Oyster", R, sub="Taiwán · LCP", dur=W(g + "1", "equipo") - T0(g + "1"), x=.22,
         tam=430),
    vs(W(g + "1", "equipo"), W(g + "1", "termino"), "CFO", "T1", "Worlds 2025: CFO 1 · T1 0", "Fase suiza", ganador=0, y=.42),
    peg(W(g + "1", "termino"), "Faker", "T1", "oro", "T1", "Campeón del mundo 2025", dur=T1(g + "1") - W(g + "1", "termino") + .2,
        x=.75, y=.47, tam=380),
    gran(T0(g + "2"), EQ("KC"), "Karmine Corp", A, sub="Francia · LEC", dur=W(g + "2", "llena") - T0(g + "2"), x=.78, tam=430),
    tar(W(g + "2", "streamers"), W(g + "2", "llena"), "Fundado por dos streamers", "2020 · Francia", A, logo="KC", x=.32, y=.78,
        tam=50),
    tar(W(g + "2", "llena"), W(g + "2", "juega"), "28.000 personas", "En sus eventos en París", "oro", dato="28K", x=.5, y=.8, tam=50),
    tar(W(g + "2", "juega"), T1(g + "2") + .2, "Su primer Mundial", None, A, logo="KC", x=.5, y=.8, tam=56),
    mg(L.resultados("First Stand 2025", [(EQ("CFO"), "CFO", EQ("KC"), "Karmine Corp", 0),
                                         (EQ("KC"), "Karmine Corp", EQ("CFO"), "CFO", 0)]),
       T0(g + "3"), W(g + "3", "desempate"), [T0(g + "3") + .2, W(g + "3", "cada")], y=.45, nombre="resultados FS25"),
    vs(W(g + "3", "desempate"), T1(g + "3") + .2, "CFO", "KC", "Hoy, el desempate", "El que pierda, a casa", y=.42),
    tar(T0(g + "4"), W(g + "4", "historia"), "¿Nunca los has visto?", "Te los presento en 15 minutos", "oro", x=.5, y=.2, tam=66),
    mg(L.menu([(EQ("CFO"), "La historia", "rojo"), (JUG("Caliste"), "Los jugadores", "azul"),
               (ART("Rumble"), "Las jugadas", "amarillo"), (EQ("KC"), "Los duelos", "oro")]),
       W(g + "4", "historia") - .3, T1(g + "4") + .3,
       [W(g + "4", "historia"), W(g + "4", "jugadores"), W(g + "4", "jugadas"), W(g + "4", "duelos")], y=.5, nombre="menu"),
]
# ================================================================== LO QUE ESTÁ EN JUEGO
g = "juego_"
FX += [
    tar(T0(g + "0"), W(g + "0", "fase"), "Lo que está en juego", None, "oro", x=.5, y=.2, tam=74),
    mg(L.suiza("Fase suiza · Allen, Texas"), W(g + "0", "fase"), T1(g + "0") + .3,
       [W(g + "0", "fase"), W(g + "0", "fase") + .6, W(g + "0", "tres"), W(g + "0", "victorias"), W(g + "0", "derrotas"),
        T1(g + "0")], y=.46, nombre="suiza"),
    mg(L.tabla("Antes de la ronda 4", [("1-2 · uno se va hoy", "rojo", [(EQ("CFO"), "CTBC Flying Oyster"), (EQ("KC"), "Karmine Corp")])]),
       T0(g + "1"), W(g + "1", "pierda"), [T0(g + "1") + .1, T0(g + "1") + .6], y=.5, nombre="tabla"),
    tar(W(g + "1", "pierda"), W(g + "1", "gane"), "El que pierda: 1-3", "Eliminado", R, x=.5, y=.5, tam=70),
    tar(W(g + "1", "gane"), T1(g + "1") + .2, "El que gane: 2-2", "Otra serie a muerte el sábado 31", A, x=.5, y=.5, tam=70),
    tar(T0(g + "2"), W(g + "2", "Fearless"), "Al mejor de 3", "Gana quien llegue a dos", "oro", x=.5, y=.2, tam=66),
    tar(W(g + "2", "Fearless"), W(g + "2", "CFO"), "Fearless Draft", "En la serie, ningún campeón se repite", "oro", x=.5, y=.17,
        tam=66),
    peg(W(g + "2", "campeon"), ICON("Rumble"), "Rumble", "oro", sub="Partida 1", dur=W(g + "2", "CFO") - W(g + "2", "campeon"), x=.24,
        y=.55, tam=240),
    peg(W(g + "2", "volver") - .4, ICON("Rumble"), "Rumble", R, sub="Partida 2", dur=W(g + "2", "CFO") - W(g + "2", "volver") + .4,
        x=.76, y=.55, tam=240, gris=True, sello=("YA USADO", 0), marcas=[W(g + "2", "elegir")]),
    tar(W(g + "2", "CFO"), T1(g + "2") + .2, "Primera selección: CFO", "En la partida 1 · mejor sembrado", R, logo="CFO", x=.5,
        y=.5, tam=60),
]
# ================================================================== CFO: HISTORIA
g = "cfo_historia_"
FX += [
    gran(T0(g + "0"), EQ("CFO"), "CTBC Flying Oyster", R, sub="Taipéi · fundado en 2022", dur=T1(g + "0") - T0(g + "0") + .2,
         x=.27, tam=520),
    tar(W(g + "0", "banco"), T1(g + "0") + .2, "CTBC", "Un banco de Taiwán", "oro", x=.72, y=.4, tam=80),
    tar(W(g + "0", "beisbol"), T1(g + "0") + .2, "También béisbol y básquetbol", None, "oro", x=.72, y=.62, tam=44),
    tar(T0(g + "1"), W(g + "1", "family"), "飛牡蠣", "«Ostra voladora»", "oro", x=.5, y=.35, tam=110),
    tar(W(g + "1", "family"), T1(g + "1") + .2, "≈ «family»", "Suena casi igual en chino", R, x=.5, y=.35, tam=96),
    tar(W(g + "1", "lema"), T1(g + "1") + .2, "«We are family»", "El lema del banco… y del equipo", "oro", x=.5, y=.7, tam=60),
    gran(W(g + "2", "Rest") - .3, "Rest", "Rest", R, "CFO", "Top · el único fundador", dur=T1(g + "2") - W(g + "2", "Rest") + .5,
         x=.27, tam=520),
    tar(T0(g + "2"), T1(g + "2") + .2, "2022", "Nace el equipo", "oro", x=.72, y=.4, tam=100),
    mg(L.calendario("CFO en 2025", [("LCP", "3 de 3\ntítulos", "oro"), ("MSI", "2-3 contra T1", "rojo"),
                                     ("Mundial", "1-0 a T1", "azul"), ("Cuartos", "1.º de APAC\nen 10 años", "amarillo")]),
       T0(g + "3"), T1(g + "3") + .3, [W(g + "3", "tres"), W(g + "3", "MSI"), W(g + "3", "Mundial"), W(g + "3", "cuartos")], y=.5,
       nombre="calendario CFO 2025"),
    peg(T0(g + "4"), "Faker", "T1", "oro", "T1", "Campeón del mundo 2025", dur=T1(g + "4") - T0(g + "4") + .3, x=.27, y=.47, tam=430),
    tar(T0(g + "4") + .3, T1(g + "4") + .3, "T1 · campeón 2025", "Y CFO le había ganado", "oro", logo="T1", x=.68, y=.6, tam=54),
]
# ================================================================== CFO: CAMINO
g = "cfo_camino_"
FX += [
    mg(L.calendario("CFO en 2026", [("Etapa 1", "Fuera en\n1.ª ronda", "rojo"), ("Etapa 2", "Fuera en\n1.ª ronda", "rojo"),
                                     ("Abril", "POUT y Kino", "oro"), ("Etapa 3", "Subcampeón", "azul"), ("Mundial", "LCP n.º 2", "amarillo")]),
       T0(g + "0"), T1(g + "1") + .3,
       [W(g + "0", "primeras"), W(g + "0", "primeras") + .5, W(g + "1", "abril"), W(g + "1", "Subcampeon"), W(g + "1", "boleto")],
       y=.5, nombre="calendario CFO 2026"),
    peg(W(g + "1", "POUT"), "POUT", "POUT", R, "CFO", "Medio · desde abril", dur=W(g + "1", "revivio") - W(g + "1", "POUT"), x=.18,
        y=.36, tam=260),
    peg(W(g + "1", "Kino"), "Kino", "Kino", R, "CFO", "Soporte · desde abril", dur=W(g + "1", "revivio") - W(g + "1", "Kino"), x=.82,
        y=.36, tam=260),
]
for i, (j, sub, pal) in enumerate((("Rest", "Top", "Rest"), ("Shad0w", "Jungla · Italia", "Shad0w"), ("POUT", "Medio · Corea", "POUT"),
                                    ("Kino", "Soporte", "Kino"), ("Doggo", "Tirador · capitán", "Doggo"))):
    e = W(g + "2", pal)
    FX.append(peg(e, j, j, R, "CFO", sub, dur=T1(g + "2") - e + .3, x=.1 + .2 * i, y=.5 if j != "Doggo" else .45,
                  tam=300 if j != "Doggo" else 380))
FX += [
    mg(L.resultados("CFO en el Mundial", [(EQ("TLAW"), "Team Liquid", EQ("CFO"), "CFO", 1),
                                           (EQ("MKOI"), "Movistar KOI", EQ("CFO"), "CFO", 0),
                                           (EQ("T1"), "T1", EQ("CFO"), "CFO", 0)]),
       T0(g + "3"), T1(g + "3") + .3, [T0(g + "3") + .2, W(g + "3", "KOI"), W(g + "3", "T1")], y=.45, nombre="resultados CFO"),
    tar(W(g + "4", "gana"), W(g + "4", "pelea"), "Cómo gana", None, A, x=.33, y=.5, tam=70),
    tar(W(g + "4", "pierde"), W(g + "4", "pelea"), "…y cómo pierde", None, R, x=.67, y=.5, tam=70),
    vs(W(g + "4", "pelea"), T1(g + "4") + .3, "TLAW", "CFO", "Su única victoria", "Ronda 1 · contra Team Liquid", ganador=1, y=.42),
]

# ================================================================== JUGADA 1 · TL vs CFO (j1: reloj = t + 2000; t=56 → 34:16)
f = "jugada1_"
e0, e1 = ESC("jugada1")
FX += [en_vivo(e0 + .3, "Transmisión oficial · Team Liquid vs CFO", "CFO"),
       tar(e0 + .3, e0 + 5.5, "Minuto 34", "Mira primero la pelea entera", "oro", x=.76, y=.17, tam=40)]
a = T0(f + "0")
FX += [J(1, a, a + 1.2, 80, -(80 - 16) / 1.2), rebobinar(a, a + 1.2, "33:36"), dict(tipo="destello", en=a + 1.2, fuerza=.4)]
FX += P(1, a + 1.2, NX(f + "0"), 16, [
    anillo(.497, .034, 52, A, W(f + "0", "diez"), "10 A 5", "LIQUID, EN ASESINATOS", lado="abajo"),
    texto("CFO · 4 DRAGONES", "ALMA DE MONTAÑA", .74, .5, W(f + "0", "alma"), color=R),
    texto("DRAGÓN ANCESTRAL", "APARECE EN 19 SEGUNDOS", .5, .66, W(f + "0", "ancestral"), color=Y, tam=40),
], "33:36")
b = T0(f + "1")
FX += P2(1, b, NX(f + "1"), 16, [
    dict(tipo="foco", en=b + .2, k=.42),
    anillo(.355, .72, 60, R, W(f + "1", "Shad0w"), "SHAD0W", "QIYANA · EN LA OSCURIDAD", lado="der", icono="Qiyana"),
    anillo(.26, .22, 40, A, W(f + "1", "foso"), "LIQUID", "LOS CINCO, LISTOS", lado="izq"),
    anillo(.335, .245, 36, A, W(f + "1", "foso") + .15),
    anillo(.42, .255, 36, A, W(f + "1", "foso") + .3),
    intencion([(.355, .69), (.31, .52), (.30, .34)], R, W(f + "1", "espalda"), "POR LA ESPALDA", off=(-150, 0)),
    texto("SU EQUIPO, DE FRENTE", "CFO", .8, .55, W(f + "1", "frente"), color=R),
], "33:36")
a = T0(f + "2")
FX += [CLIP(1, a, NX(f + "2"), 16, 39), x2(a, NX(f + "2"), "▶▶ ACELERADO"),
       tar(a + .2, W(f + "2", "Shad0w"), "CoreJJ · Rakan", "Entra para abrir la pelea", A, icono="Rakan", x=.16, y=.14, tam=36),
       tar(W(f + "2", "Shad0w"), NX(f + "2"), "Shad0w lo caza", "Desde el flanco", R, icono="Qiyana", x=.16, y=.14, tam=36),
       peg(W(f + "2", "fuera"), "CoreJJ", "CoreJJ", A, "TLAW", "Fuera", dur=NX(f + "2") - W(f + "2", "fuera"), x=.1, y=.62, tam=200,
           gris=True),
       dict(tipo="destello", en=W(f + "2", "fuera"), fuerza=.5)]
b = T0(f + "3") + 2.4                     # de 39 a 56 (34:16) acelerado: sin saltos de tiempo
FX += [CLIP(1, T0(f + "3"), b, 39, 56), x2(T0(f + "3"), b, "▶▶ x7")]
FX += P2(1, b, NX(f + "3"), 56, [
    dict(tipo="zona", pts=[(.27, .55), (.47, .55), (.48, .76), (.25, .76)], color=Y, en=W(f + "3", "dragon"), alfa=.14),
    anillo(.45, .63, 50, R, W(f + "3", "Rest"), "REST", "DENTRO DEL FOSO", lado="izq", icono="Rumble"),
    anillo(.45, .72, 46, R, W(f + "3", "Shad0w"), "SHAD0W", "AL ANCESTRAL", lado="izq", icono="Qiyana"),
    anillo(.54, .60, 44, R, W(f + "3", "Doggo"), "DOGGO", None, lado="der", icono="Aphelios"),
    anillo(.47, .49, 44, R, W(f + "3", "Kino"), "KINO", None, lado="arriba", icono="Alistar"),
    anillo(.635, .34, 40, R, W(f + "3", "POUT"), "POUT", None, lado="der", icono="Viktor"),
    flecha([(.635, .35), (.48, .50), (.54, .60)], R, W(f + "3", "muro"), "EL MURO", off=(120, -10), dur=.8),
    anillo(.25, .50, 40, A, W(f + "3", "muro") + .4, "YEON", None, lado="izq"),
    anillo(.29, .42, 40, A, W(f + "3", "muro") + .6, "JOSEDEODO", None, lado="izq"),
], "34:16")
FX += [tar(b + .2, W(f + "3", "reparto"), "5 contra 4", "CFO empieza el ancestral", R, logo="CFO", x=.5, y=.86, tam=46)]
FX += MESA2("j1", T0(f + "4"), NX(f + "4"), "34:16")
a = T0(f + "5")
FX += [CLIP(1, a, NX(f + "5"), 56, 75), x2(a, NX(f + "5"), "▶▶ ACELERADO"),
       peg(W(f + "5", "acaba"), "Josedeodo", "Josedeodo", A, "TLAW", "Lo remata Rest", dur=NX(f + "5") - W(f + "5", "acaba"), x=.1,
           y=.62, tam=190, gris=True),
       peg(W(f + "5", "cobra"), "Shad0w", "Shad0w", R, "CFO", "Cae", dur=NX(f + "5") - W(f + "5", "cobra"), x=.9, y=.62, tam=190,
           gris=True),
       peg(W(f + "5", "borra"), "Quid", "Quid", A, "TLAW", "Lo borra POUT", dur=NX(f + "5") - W(f + "5", "borra"), x=.27, y=.62,
           tam=190, gris=True),
       dict(tipo="destello", en=W(f + "5", "levanta"), fuerza=.45)]
a = T0(f + "6")
FX += [CLIP(1, a, e1, 75, 82), dict(tipo="destello", en=a + .1, fuerza=.6),
       tar(a + .1, e1, "¡Dragón ancestral!", "Para CFO", R, logo="CFO", dato="34:39", x=.5, y=.84, tam=52),
       tar(W(f + "6", "Baron"), e1, "Y el Barón", "35:16", R, x=.5, y=.17, tam=46)]

# ── repetición de la jugada 1
f = "jugada1_rep_"
e0, e1 = ESC("jugada1_rep")
FX += [J(1, e0, T0(f + "0"), 34 - .55 * (T0(f + "0") - e0), .55, zoom=(1.35, .42, .6), zoom0=(1.0, .5, .5), zoom_dur=1.2),
       *repeticion(e0, e0 + 3.5)]
b = T0(f + "0")
FX += P2(1, b, NX(f + "0"), 34, [
    dict(tipo="foco", en=b + .2, k=.4),
    ruta(1, 34, [(26, .41, .57), (30.5, .235, .70), (34, .40, .67)], R, W(f + "0", "ruta"), "LA RUTA DE SHAD0W", off=(-170, 0)),
    ruta(1, 34, [(30.5, .42, .41), (34, .445, .52)], A, W(f + "0", "ruta") + .3, None),
    ruta(1, 34, [(30.5, .745, .50), (34, .72, .42)], R, W(f + "0", "ruta") + .6, None),
    ruta(1, 34, [(30.5, .80, .45), (34, .90, .59)], R, W(f + "0", "ruta") + .9, None),
    anillo(.40, .67, 46, R, W(f + "0", "objetivo"), "SHAD0W", "LLEGÓ PRIMERO", lado="izq", icono="Qiyana"),
    anillo(.445, .52, 46, A, W(f + "0", "cazo"), "COREJJ", "CAZADO", lado="der", icono="Rakan"),
    anillo(.72, .42, 40, R, W(f + "0", "posicion"), "KINO", "LLEGA A AYUDAR", lado="der", icono="Alistar"),
], "33:54")
a = T0(f + "1")
d = W(f + "1", "Dos")
FX += [J(1, a, d, 34, 1.0),
       tar(W(f + "1", "leccion"), d, "La lección de CFO", "No gana por matar más", "oro", x=.5, y=.18, tam=56),
       tar(W(f + "1", "objetivos"), d, "Objetivos y posición", "10-5 abajo… y gana", R, logo="CFO", x=.5, y=.84, tam=48),
       CLIP("2", d, e1, 72, 86), dict(tipo="destello", en=d, fuerza=.4),
       tar(d, d + 2.5, "2 minutos después", "37:17", "oro", x=.12, y=.13, tam=30),
       peg(W(f + "1", "Rest"), "Rest", "Rest", R, "CFO", "Rumble · el veterano", dur=e1 - W(f + "1", "Rest"), x=.15, y=.5, tam=300),
       tar(W(f + "1", "triple"), e1 + .2, "¡Triple!", "Rest · cierre de la partida", R, icono="Rumble", dato="3", x=.6, y=.84, tam=46)]

# ================================================================== CFO: JUGADORES
g = "cfo_jugadores_"
FX += [
    mg(L.ficha_jugador(JUG("Doggo"), "Doggo", EQ("CFO"), 1, [("Daño a campeones", "58,2 K", .95), ("% del daño de CFO", "32 %", .64)],
                       R, sub="Tirador · el que más daño hace"),
       T0(g + "0"), W(g + "0", "Kino"), [W(g + "0", "dano"), W(g + "0", "mucho")], y=.5, nombre="ficha Doggo"),
    mg(L.ficha_jugador(JUG("Kino"), "Kino", EQ("CFO"), 2, [("Participación", "88 %", .88), ("Asistencias", "21", .7)], R,
                       sub="Soporte"),
       W(g + "0", "Kino"), W(g + "0", "Shad0w"), [W(g + "0", "nueve")], y=.5, nombre="ficha Kino"),
    mg(L.ficha_jugador(JUG("Shad0w"), "Shad0w", EQ("CFO"), 3, [("Participación", "80 %", .8), ("KDA", "2,5", .42)], R,
                       sub="Jungla"),
       W(g + "0", "Shad0w"), T1(g + "0") + .2, [W(g + "0", "ocho")], y=.5, nombre="ficha Shad0w"),
    mg(L.barras("CFO en 3 partidas", [(EQ("CFO"), "Muertes", 44), (EQ("CFO"), "Asesinatos", 25)], 44),
       T0(g + "1"), T1(g + "1") + .3, [W(g + "1", "cuarenta"), W(g + "1", "veinticinco")], y=.5, nombre="barras CFO"),
    vs(T0(g + "2"), T1(g + "2") + .3, "T1", "CFO", "Contra T1", "Ronda 3", ganador=0, y=.42),
]

# ================================================================== JUGADA 2 · T1 vs CFO (j3: reloj = t + 1412; j3b: + 477)
f = "jugada2_"
e0, e1 = ESC("jugada2")
FX += [en_vivo(e0 + .3, "Transmisión oficial · T1 vs CFO", "CFO"),
       tar(e0 + .3, e0 + 5.5, "Minuto 24", "CFO va ganando", "oro", x=.76, y=.17, tam=40)]
a = T0(f + "0")
u = W(f + "0", "Un")
FX += [J(3, a, a + 1.2, 70, -45), rebobinar(a, a + 1.2, "08:05"), dict(tipo="destello", en=a + 1.2, fuerza=.4),
       CLIP("3b", a + 1.2, u, 2, 16), CLIP("3b", u, NX(f + "0"), 57, 67),
       tar(a + 1.3, u, "Doggo · Kai'Sa", "Minuto 8", R, icono="Kaisa", x=.16, y=.14, tam=36),
       tar(W(f + "0", "Doran"), u, "Doran: sin Destello", "Y sin visión", A, icono="SummonerFlash", x=.8, y=.14, tam=34),
       peg(W(f + "0", "caza"), "Doran", "Doran", A, "T1", "Cazado", dur=u - W(f + "0", "caza"), x=.1, y=.62, tam=190, gris=True),
       tar(u, NX(f + "0"), "Otra vez", "Minuto 9", R, icono="Kaisa", x=.16, y=.14, tam=36),
       peg(u + 2.5, "Doran", "Doran", A, "T1", "Otra vez", dur=NX(f + "0") - u - 2.5, x=.1, y=.62, tam=190, gris=True)]
a = T0(f + "1")
FX += [CLIP(3, a, NX(f + "1"), 22, 48), x2(a, NX(f + "1"), "▶▶ ACELERADO"),
       tar(a, a + 2.5, "Minuto 24", "23:54", "oro", x=.12, y=.2, tam=30),
       tar(W(f + "1", "dos"), NX(f + "1"), "+2.000 de oro", "Y 4 torres", R, logo="CFO", dato="+2K", x=.5, y=.84, tam=48),
       tar(W(f + "1", "narradores"), NX(f + "1"), "«CFO juega increíblemente bien»", "Los narradores", "oro", x=.5, y=.18, tam=42),
       tar(W(f + "1", "limpiaba"), NX(f + "1"), "T1 limpia la visión", "Para forzar la pelea", A, logo="T1", x=.82, y=.62, tam=36)]
b = T0(f + "2")
FX += P2(3, b, NX(f + "2"), 48, [
    dict(tipo="foco", en=b + .2, k=.42),
    anillo(.44, .43, 60, R, W(f + "2", "Doggo"), "DOGGO", "EL QUE MÁS ORO TIENE", lado="izq", icono="Kaisa"),
    anillo(.365, .52, 38, R, W(f + "2", "proteger") + .3, "KINO", None, lado="izq", icono="Alistar"),
    anillo(.42, .71, 40, A, W(f + "2", "sabe"), "KERIA", None, lado="izq", icono="Rakan"),
    anillo(.67, .75, 40, A, W(f + "2", "sabe") + .3, "ONER", None, lado="der", icono="Vi"),
    intencion([(.42, .69), (.43, .56), (.44, .46)], A, W(f + "2", "atrapa"), None),
    intencion([(.66, .73), (.55, .58), (.46, .46)], A, W(f + "2", "atrapa") + .15, "OBJETIVO: DOGGO", off=(150, 0)),
], "24:20")
FX += MESA2("j2", T0(f + "3"), NX(f + "3"), "24:20")
FX += [tar(W(f + "3", "Doran"), NX(f + "3"), "Doran, por el flanco", "Sin que nadie lo vea", A, icono="Ambessa", x=.82, y=.14,
           tam=36)]
a = T0(f + "4")
FX += [CLIP(3, a, NX(f + "4"), 48, 58),
       tar(W(f + "4", "Keria"), NX(f + "4"), "Keria conecta", "El primer control", A, icono="Rakan", x=.16, y=.14, tam=36),
       peg(W(f + "4", "muere"), "Doggo", "Doggo", R, "CFO", "Cae primero", dur=NX(f + "4") - W(f + "4", "muere"), x=.1, y=.62,
           tam=200, gris=True),
       dict(tipo="destello", en=W(f + "4", "muere"), fuerza=.55)]
a = T0(f + "5")
FX += [CLIP(3, a, e1, 58, 72), x2(a, e1, "▶▶ ACELERADO"),
       mg(L.caida("CFO: 5 muertes en 11 segundos", [(JUG(j), j) for j in ("Doggo", "POUT", "Rest", "Kino", "Shad0w")], "0-5"),
          W(f + "5", "cinco"), e1 + .2, [W(f + "5", "cinco") + .4 * i for i in range(7)], y=.45, nombre="caida CFO"),
       tar(W(f + "5", "Baron"), e1 + .2, "T1 toma el Barón", "Y gana la partida", A, logo="T1", x=.5, y=.86, tam=46)]
# ── repetición de la jugada 2 (la repetición oficial de la transmisión)
f = "jugada2_rep_"
e0, e1 = ESC("jugada2_rep")
FX += [J(3, e0, T0(f + "0"), 97, .7), *repeticion(e0, e0 + 3.5, "La de la transmisión"),
       tar(e0 + 3.6, T0(f + "0"), "Keria encuentra a Doggo", "Doran, por el flanco", A, logo="T1", x=.5, y=.86, tam=44)]
a = T0(f + "0")
FX += [J(3, a, e1, 97 + (a - e0) * .7, .7),
       tar(a + .2, W(f + "0", "Contra"), "La grieta de CFO", "Gana… y pierde la pelea grande", "oro", x=.5, y=.18, tam=54),
       vs(W(f + "0", "Contra"), e1 + .2, "MKOI", "CFO", "Contra KOI, igual", "Barón… y 4-0 en la pelea siguiente", ganador=0, y=.42)]

# ================================================================== KC: HISTORIA
g = "kc_historia_"
FX += [
    gran(T0(g + "0"), EQ("KC"), "Karmine Corp", A, sub="Francia · fundado en 2020", dur=T1(g + "0") - T0(g + "0") + .2, x=.27, tam=520),
    tar(W(g + "0", "Twitch"), T1(g + "0") + .2, "Nació en Twitch", None, "oro", x=.72, y=.5, tam=70),
    tar(T0(g + "1"), W(g + "1", "Meses"), "Kameto y Kotei", "Dos streamers · 2020", A, logo="KC", x=.5, y=.2, tam=60),
    tar(W(g + "1", "Meses"), T1(g + "1") + .2, "Kameto Corp → Karmine Corp", "Noviembre de 2020", A, logo="KC", x=.5, y=.2, tam=54),
    tar(T0(g + "2"), W(g + "2", "presidente"), "4 títulos de EU Masters", "Récord de la segunda división europea", A, logo="KC",
        dato="4", x=.5, y=.5, tam=64),
    tar(W(g + "2", "presidente"), T1(g + "2") + .2, "Emmanuel Macron", "Los felicitó en 2021", "oro", x=.5, y=.5, tam=70),
    tar(T0(g + "3"), W(g + "3", "2023"), "El Blue Wall", "La afición de Karmine", A, logo="KC", x=.5, y=.2, tam=70),
    tar(W(g + "3", "2023"), T1(g + "3") + .2, "28.000 personas", "Paris La Défense Arena · 2023 y 2024", "oro", dato="28K", x=.5,
        y=.5, tam=70),
    tar(T0(g + "4"), W(g + "4", "este"), "LEC Winter 2025", "Primer club francés campeón", A, logo="KC", dato="3-0", x=.5, y=.5,
        tam=60),
    tar(W(g + "4", "este"), T1(g + "4") + .3, "2026: su primer Mundial", None, A, logo="KC", x=.5, y=.5, tam=70),
]
# ================================================================== KC: CAMINO
g = "kc_camino_"
FX += [
    mg(L.calendario("Karmine en 2026", [("Versus", "Final\n2-3 G2", "rojo"), ("Spring", "Final\n2-3 G2", "rojo"),
                                         ("EWC París", "Final\n(eliminó a T1)", "oro"), ("Summer", "9-0… y 3.º", "azul")]),
       T0(g + "0"), T1(g + "0") + .3, [W(g + "0", "finales"), W(g + "0", "contra"), W(g + "0", "Esports"), W(g + "0", "verano")],
       y=.5, nombre="calendario KC 2026"),
]
for i, (j, sub, pal) in enumerate((("Canna", "Top · ex-T1", "Canna"), ("Yike", "Jungla · Suecia", "Yike"), ("kyeahoo", "Medio · Corea", "kyeahoo"),
                                    ("Busio", "Soporte · EE. UU.", "Busio"), ("Caliste", "Tirador · 20 años · MVP", "Caliste"))):
    e = W(g + "1", pal)
    FX.append(peg(e, j, j, A, "KC", sub, dur=T1(g + "1") - e + .3, x=.1 + .2 * i, y=.5 if j != "Caliste" else .45,
                  tam=300 if j != "Caliste" else 380))
FX += [
    tar(T0(g + "2"), W(g + "2", "Perdio"), "Play-In · Los Ángeles", "Solo pasa uno", "oro", x=.5, y=.2, tam=60),
    tar(W(g + "2", "Perdio"), W(g + "2", "remonto"), "1 a 20", "Su primera partida, contra Cloud9", R, logo="C9", dato="1-20", x=.5,
        y=.5, tam=70),
    tar(W(g + "2", "remonto"), T1(g + "2") + .2, "3-2 a Cloud9", "Y 3-0, 3-0 a MVK", A, logo="KC", x=.5, y=.5, tam=70),
    mg(L.resultados("Karmine en el Mundial", [(EQ("KC"), "Karmine Corp", EQ("AL"), "Anyone's Legend", 0),
                                               (EQ("KC"), "Karmine Corp", EQ("LYON"), "LYON", 1),
                                               (EQ("KC"), "Karmine Corp", EQ("BLG"), "Bilibili Gaming", 1)]),
       T0(g + "3"), T1(g + "3") + .3, [W(g + "3", "aplasto"), W(g + "3", "LYON"), W(g + "3", "Bilibili")], y=.45, nombre="resultados KC"),
    vs(T0(g + "4"), T1(g + "4") + .3, "KC", "AL", "Contra el n.º 1 de China", "Ronda 1 · minuto 24", ganador=0, y=.42),
]

# ================================================================== JUGADA 3 · KC vs AL (j4: reloj = t + 1422; t=52 → 24:34)
f = "jugada3_"
e0, e1 = ESC("jugada3")
FX += [en_vivo(e0 + .3, "Transmisión oficial · Karmine vs Anyone's Legend", "KC"),
       tar(e0 + .3, e0 + 5.5, "Minuto 24", "Mira primero la pelea entera", "oro", x=.76, y=.17, tam=40)]
a = T0(f + "0")
FX += [J(4, a, a + 1.2, 76, -20), rebobinar(a, a + 1.2, "24:34"), dict(tipo="destello", en=a + 1.2, fuerza=.4)]
FX += P(4, a + 1.2, NX(f + "0"), 52, [
    anillo(.497, .034, 52, A, W(f + "0", "dos"), "2 A 1", "EN ASESINATOS", lado="abajo"),
    texto("DRAGONES: 2 A 2", None, .26, .5, W(f + "0", "dragones"), color=Y),
    texto("ORO: 41,8 K CONTRA 42,1 K", "CASI EMPATADO", .74, .5, W(f + "0", "oro"), color=Y),
], "24:34")
b = T0(f + "1")
FX += P2(4, b, NX(f + "1"), 52, [
    dict(tipo="foco", en=b + .2, k=.42),
    anillo(.385, .33, 56, R, W(f + "1", "Kael"), "KAEL", "NEEKO · EL OBJETIVO", lado="izq", icono="Neeko"),
    anillo(.56, .43, 48, A, W(f + "1", "Busio"), "BUSIO", "RENATA", lado="der", icono="Renata"),
    flecha([(.555, .42), (.47, .37), (.40, .335)], A, W(f + "1", "Destello"), "DESTELLO", off=(0, -60)),
    texto("NO CONECTA", None, .47, .2, W(f + "1", "conecta"), color=R),
    anillo(.67, .35, 36, A, W(f + "1", "conecta") + .2, "YIKE", None, lado="der", icono="JarvanIV"),
    anillo(.27, .70, 44, A, W(f + "1", "conecta") + .5, "CANNA", "JAX · AÚN LEJOS", lado="der", icono="Jax"),
], "24:34")
a = T0(f + "2")
FX += [CLIP(4, a, NX(f + "2"), 52, 63.5),
       tar(a + .2, W(f + "2", "cae"), "Yike · Jarvan IV", "Se mete demasiado", A, icono="JarvanIV", x=.16, y=.14, tam=36),
       peg(W(f + "2", "cae"), "Yike", "Yike", A, "KC", "Cae primero", dur=NX(f + "2") - W(f + "2", "cae"), x=.1, y=.62, tam=200,
           gris=True),
       tar(W(f + "2", "pinta"), NX(f + "2"), "Pinta para Anyone's Legend", None, R, logo="AL", x=.5, y=.86, tam=44)]
b = T0(f + "3")
FX += P2(4, b, NX(f + "3"), 63.5, [
    dict(tipo="foco", en=b + .2, k=.4),
    texto("LA DEFINITIVA DE BUSIO", "RENATA · COMPRA TIEMPO", .5, .16, W(f + "3", "definitiva"), color=A, icono="Renata"),
    anillo(.42, .25, 48, R, W(f + "3", "combo"), "KAEL", "ATURDIDO · POCA VIDA", lado="izq", icono="Neeko"),
    texto("ANYONE'S LEGEND", "CON POCA VIDA", .76, .45, W(f + "3", "vida"), color=R, tam=40),
], "24:45")
a = T0(f + "4")
FX += [CLIP(4, a, NX(f + "4"), 63.5, 67),
       gran(a + .1, "Canna", "Canna", A, "KC", "Jax · a la retaguardia", dur=NX(f + "4") - a, x=.2, tam=420)]
a = T0(f + "5")
FX += [CLIP(4, a, e1, 67, 77), x2(a, e1, "▶▶ ACELERADO"), dict(tipo="destello", en=W(f + "5", "cuadruple"), fuerza=.6),
       peg(W(f + "5", "Tarzan"), "Tarzan", "Tarzan", R, "AL", None, dur=e1 - W(f + "5", "Tarzan"), x=.08, y=.25, tam=150, gris=True),
       peg(W(f + "5", "Kael"), "Kael", "Kael", R, "AL", None, dur=e1 - W(f + "5", "Kael"), x=.08, y=.47, tam=150, gris=True),
       peg(W(f + "5", "Shanks"), "Shanks", "Shanks", R, "AL", None, dur=e1 - W(f + "5", "Shanks"), x=.08, y=.69, tam=150, gris=True),
       peg(W(f + "5", "Breathe"), "Breathe", "Breathe", R, "AL", "kyeahoo", dur=e1 - W(f + "5", "Breathe"), x=.92, y=.3, tam=150,
           gris=True),
       tar(W(f + "5", "cuadruple"), e1 + .2, "¡Cuádruple!", "Canna · Jax", A, logo="KC", dato="4", x=.5, y=.86, tam=50)]
# ── repetición de la jugada 3
f = "jugada3_rep_"
e0, e1 = ESC("jugada3_rep")
FX += [J(4, e0, T0(f + "0"), 68 - .6 * (T0(f + "0") - e0), .6, zoom=(1.3, .5, .45), zoom0=(1.0, .5, .5), zoom_dur=1.0),
       *repeticion(e0, e0 + 3.5)]
b = T0(f + "0")
d = W(f + "0", "Dos")
FX += P2(4, b, d, 68, [
    ruta(4, 68, [(61.5, .495, .58), (68, .55, .34)], A, b + .3, "LA RUTA DE CANNA", off=(-160, 40)),
    anillo(.55, .34, 50, A, b + .9, "CANNA", "A LA RETAGUARDIA", lado="der", icono="Jax"),
    anillo(.575, .66, 44, A, W(f + "0", "jungla") + .5, "KYEAHOO", "ONDA DE CHOQUE", lado="der", icono="Orianna"),
    texto("CADA UNO, SU TRABAJO", None, .5, .15, W(f + "0", "trabajo"), color=A, tam=40),
], "24:50")
FX += [J(4, d, e1, 68, 1.0),
       tar(d, e1 + .2, "Barón para Karmine", "Y la victoria", A, logo="KC", x=.5, y=.86, tam=46)]

# ================================================================== KC: JUGADORES
g = "kc_jugadores_"
FX += [
    mg(L.ficha_jugador(JUG("Caliste"), "Caliste", EQ("KC"), 1, [("Asesinatos", "60", .95), ("KDA", "5,6", .93),
                                                                ("Partidas", "14", .5)], A, sub="Tirador · 20 años"),
       T0(g + "0"), T1(g + "0") + .2, [W(g + "0", "sesenta"), W(g + "0", "KDA"), W(g + "0", "catorce")], y=.5, nombre="ficha Caliste"),
    mg(L.ficha_jugador(JUG("Busio"), "Busio", EQ("KC"), 2, [("Participación", "70 %", .7), ("Asistencias", "124", .95)], A,
                       sub="Soporte"),
       T0(g + "1"), W(g + "1", "Yike"), [W(g + "1", "siete")], y=.5, nombre="ficha Busio"),
    peg(W(g + "1", "Yike"), "Yike", "Yike", A, "KC", "Jungla", dur=T1(g + "1") - W(g + "1", "Yike") + .2, x=.25, y=.47, tam=400),
    peg(W(g + "1", "Lee"), ICON("LeeSin"), "Lee Sin", "oro", sub="5 partidas", dur=W(g + "1", "Fearless") - W(g + "1", "Lee"),
        x=.7, y=.5, tam=260),
    peg(W(g + "1", "Fearless"), ICON("LeeSin"), "Lee Sin", A, sub="Fearless", dur=T1(g + "1") - W(g + "1", "Fearless") + .2, x=.7,
        y=.5, tam=260, gris=True, sello=("SOLO UNA VEZ", 0), marcas=[W(g + "1", "repetir")]),
    vs(T0(g + "2"), T1(g + "2") + .3, "C9", "KC", "Play-In · partida 4", "Cloud9 2 · Karmine 1", y=.42),
]

# ================================================================== JUGADA 4 · C9 vs KC, Play-In J4 (j5: reloj = t + 2131; VOD en español)
f = "jugada4_"
e0, e1 = ESC("jugada4")
FX += [en_vivo(e0 + .3, "Transmisión oficial (español) · Cloud9 vs Karmine", "KC"),
       tar(e0 + .3, e0 + 5.5, "Play-In · partida 4", "El final, primero", "oro", x=.76, y=.17, tam=40)]
a = T0(f + "0")
FX += [CLIP(5, a, NX(f + "0"), 143, 152),
       vs(a + .2, NX(f + "0"), "C9", "KC", "Cloud9 iba 2-1", "Si Karmine pierde, se queda sin Mundial", y=.42)]
a = T0(f + "1")
p = W(f + "1", "Pero")
FX += [J(5, a, a + 1.2, 152, -88), rebobinar(a, a + 1.2, "36:17"), dict(tipo="destello", en=a + 1.2, fuerza=.4)]
FX += P(5, a + 1.2, p, 46, [
    texto("+7.800 DE ORO", "KARMINE", .26, .5, W(f + "1", "ocho"), color=A),
    texto("4 DRAGONES · 1 BARÓN", "KARMINE", .74, .5, W(f + "1", "dragones"), color=A),
], "36:17")
FX += [CLIP(5, p, NX(f + "1"), 46, 72),
       peg(W(f + "1", "kyeahoo"), "kyeahoo", "kyeahoo", A, "KC", "Cae", dur=NX(f + "1") - W(f + "1", "kyeahoo"), x=.1, y=.62, tam=180,
           gris=True),
       peg(W(f + "1", "Busio"), "Busio", "Busio", A, "KC", "Cae", dur=NX(f + "1") - W(f + "1", "Busio"), x=.25, y=.62, tam=180,
           gris=True)]
b = T0(f + "2")
FX += P2(5, b, NX(f + "2"), 72, [
    dict(tipo="foco", en=b + .2, k=.42),
    texto("3 CONTRA 5", "KARMINE, CON DOS MENOS", .5, .88, W(f + "2", "dos"), color=R, tam=40),
    anillo(.37, .21, 56, A, W(f + "2", "Caliste"), "CALISTE", "XAYAH · SE QUEDA", lado="der", icono="Xayah"),
    anillo(.53, .50, 44, A, W(f + "2", "huye"), "CANNA", None, lado="izq", icono="Renekton"),
    anillo(.40, .64, 44, A, W(f + "2", "huye") + .2, "YIKE", None, lado="izq", icono="Qiyana"),
    anillo(.64, .49, 40, R, W(f + "2", "pelea"), "CLOUD9", "LOS CINCO", lado="der"),
    intencion([(.38, .23), (.50, .34), (.61, .45)], A, W(f + "2", "pelea"), "DAÑO DESDE ATRÁS", off=(60, -60)),
], "36:43")
a = T0(f + "3")
FX += [CLIP(5, a, NX(f + "3"), 72, 92), x2(a, NX(f + "3"), "▶▶ ACELERADO"),
       peg(W(f + "3", "Tactical"), "Tactical", "Tactical", R, "C9", None, dur=NX(f + "3") - W(f + "3", "Tactical"), x=.08, y=.25,
           tam=150, gris=True),
       peg(W(f + "3", "Vulcan"), "Vulcan", "Vulcan", R, "C9", None, dur=NX(f + "3") - W(f + "3", "Vulcan"), x=.08, y=.47, tam=150,
           gris=True),
       peg(W(f + "3", "Loki"), "Loki ", "Loki", R, "C9", None, dur=NX(f + "3") - W(f + "3", "Loki"), x=.08, y=.69, tam=150, gris=True),
       peg(W(f + "3", "Blaber"), "Blaber", "Blaber", R, "C9", None, dur=NX(f + "3") - W(f + "3", "Blaber"), x=.92, y=.3, tam=150,
           gris=True),
       tar(W(f + "3", "gana"), NX(f + "3"), "Karmine gana la pelea", "Con dos menos", A, logo="KC", x=.5, y=.86, tam=46)]
a = T0(f + "4")
FX += [CLIP(5, a, NX(f + "4"), 92, 120), x2(a, NX(f + "4"), "▶▶ ACELERADO"), dict(tipo="destello", en=W(f + "4", "toma"), fuerza=.5),
       tar(W(f + "4", "ancestral"), NX(f + "4"), "Dragón ancestral", "Para Karmine", A, logo="KC", dato="37:29", x=.5, y=.86, tam=48)]
a = T0(f + "5")
FX += [CLIP(5, a, e1, 120, 158), x2(a, e1, "▶▶ ACELERADO"),
       tar(W(f + "5", "tres"), W(f + "5", "ace"), "¡Triple!", "Caliste · en 3 segundos", A, icono="Xayah", dato="3", x=.5, y=.86, tam=46),
       tar(W(f + "5", "ace"), e1 + .2, "¡Ace!", "Y nexo", A, logo="KC", x=.5, y=.86, tam=56),
       mg(L.resultados("Play-In · Karmine vs Cloud9", [(EQ("KC"), "Karmine Corp", EQ("C9"), "Cloud9", 0)]), W(f + "5", "fuerza"),
          e1 + .2, [W(f + "5", "gana")], y=.4, nombre="resultado C9")]
# ── repetición de la jugada 4
f = "jugada4_rep_"
e0, e1 = ESC("jugada4_rep")
FX += [J(5, e0, T0(f + "0"), 136, .5, zoom=(1.3, .58, .3), zoom0=(1.0, .5, .5), zoom_dur=1.0), *repeticion(e0, e0 + 3.5)]
a = T0(f + "0")
FX += [J(5, a, e1, 136 + (a - e0) * .5, .5, zoom=(1.3, .58, .3), zoom0=(1.3, .58, .3)),
       gran(a + .1, "Caliste", "Caliste", A, "KC", "Xayah · 11/1/3", dur=e1 - a, x=.2, tam=420),
       tar(W(f + "0", "seis"), W(f + "0", "amenaza"), "6 asesinatos", "En el último minuto y cuarto", A, dato="6", x=.65, y=.8, tam=48),
       tar(W(f + "0", "amenaza"), e1 + .2, "Si la pelea se alarga…", "…su tirador la termina", "oro", x=.62, y=.8, tam=48)]

# ================================================================== LOS CINCO DUELOS (Mundial 2026; KC con el Play-In)
g = "duelos_"
FX += [tar(T0(g + "0"), T1(g + "0") + .3, "Los 5 duelos de hoy", "Posición por posición", "oro", x=.5, y=.45, tam=84)]
FX += [
    duelo(T0(g + "1"), T1(g + "1") + .2, ("Rest", "CFO", "Top · Rumble"), ("Canna", "KC", "Top · MVP vs AL"), "Top",
          [("KDA", "1,0", "3,0", .2, .6, 1), ("Participación", "44 %", "53 %", .44, .53, 1), ("Asesinatos por partida", "2,3", "2,5", .46, .5, 1)],
          [W(g + "1", "Rumble"), W(g + "1", "Canna"), W(g + "1", "MVP")]),
    duelo(T0(g + "2"), T1(g + "2") + .2, ("Shad0w", "CFO", "Jungla · Qiyana"), ("Yike", "KC", "Jungla · Lee Sin"), "Jungla",
          [("Participación", "80 %", "66 %", .8, .66, 0), ("KDA", "2,5", "4,1", .42, .69, 1), ("Asesinatos por partida", "2,3", "3,3", .46, .66, 1)],
          [W(g + "2", "flanco"), W(g + "2", "ocho"), W(g + "2", "Yike", 1)]),
    duelo(T0(g + "3"), T1(g + "3") + .2, ("POUT", "CFO", "Medio · desde abril"), ("kyeahoo", "KC", "Medio · desde enero"), "Medio",
          [("KDA", "1,7", "3,4", .28, .56, 1), ("Participación", "48 %", "59 %", .48, .59, 1), ("Muertes por partida", "2,3", "2,4", .46, .48, None)],
          [W(g + "3", "coreanos"), W(g + "3", "llegados"), W(g + "3", "enero")]),
    duelo(T0(g + "4"), T1(g + "4") + .2, ("Doggo", "CFO", "Tirador · capitán"), ("Caliste", "KC", "Tirador · 20 años"), "Tirador · el duelo de estrellas",
          [("% del daño de su equipo", "32 %", "25 %", .64, .5, 0), ("Asesinatos por partida", "2,3", "4,3", .46, .86, 1), ("KDA", "2,1", "5,6", .35, .93, 1)],
          [W(g + "4", "capitan"), W(g + "4", "frances"), W(g + "4", "sesenta")]),
    duelo(T0(g + "5"), T1(g + "5") + .2, ("Kino", "CFO", "Soporte · Alistar"), ("Busio", "KC", "Soporte · Renata, Rakan"), "Soporte",
          [("Participación", "88 %", "70 %", .88, .7, 0), ("KDA", "2,2", "4,9", .37, .82, 1), ("Asistencias por partida", "7", "8,9", .7, .89, 1)],
          [W(g + "5", "Kino", 1), W(g + "5", "Busio", 1), W(g + "5", "engancha")]),
]

# ================================================================== CLAVES
g = "claves_"
FX += [
    tar(T0(g + "0"), T1(g + "0") + .3, "3 claves para hoy", "Para verlo como un experto", "oro", x=.5, y=.45, tam=80),
    tar(T0(g + "1"), W(g + "1", "CFO"), "1 · La pelea de mitad de partida", "Los dos han tirado ventajas ahí", "oro", x=.5, y=.17, tam=54),
    vs(W(g + "1", "CFO"), W(g + "1", "Karmine"), "T1", "CFO", "CFO: contra T1 y KOI", "Iba ganando… y perdió la pelea", ganador=0, y=.45),
    vs(W(g + "1", "Karmine"), W(g + "1", "tropiece"), "LYON", "KC", "Karmine: contra LYON", "+4.700 de oro en el minuto 22… y perdió",
       ganador=0, y=.45),
    tar(W(g + "1", "tropiece"), T1(g + "1") + .2, "El que no se tropiece, gana", None, "oro", x=.5, y=.5, tam=64),
    tar(T0(g + "2"), T1(g + "2") + .2, "2 · Los objetivos", "Mira quién llega primero al dragón", "oro", x=.5, y=.17, tam=58),
    peg(W(g + "2", "CFO"), EQ("CFO"), "Alma + ancestral", R, sub="Su única victoria", dur=W(g + "2", "Karmine") - W(g + "2", "CFO") + 2,
        x=.27, y=.52, tam=340),
    peg(W(g + "2", "Karmine"), EQ("KC"), "Ancestral", A, sub="Su serie a muerte", dur=T1(g + "2") - W(g + "2", "Karmine") + .2, x=.73,
        y=.52, tam=340),
    tar(T0(g + "3"), T1(g + "3") + .2, "3 · Fearless", "Un campeón, una sola vez", "oro", x=.5, y=.17, tam=58),
    peg(W(g + "3", "Rest"), ICON("Rumble"), "Rest · Rumble", R, sub="CFO", dur=T1(g + "3") - W(g + "3", "Rest") + .2, x=.27, y=.52,
        tam=280, marcas=[W(g + "3", "vez")]),
    peg(W(g + "3", "Yike"), ICON("LeeSin"), "Yike · Lee Sin", A, sub="KC", dur=T1(g + "3") - W(g + "3", "Yike") + .2, x=.73, y=.52,
        tam=280),
    tar(W(g + "3", "gaste"), T1(g + "3") + .2, "¿Su mejor carta en la partida 1?", "Puede faltarle en la 3", "oro", x=.5, y=.86, tam=44),
    mg(L.resultados("First Stand 2025", [(EQ("CFO"), "CFO", EQ("KC"), "Karmine Corp", 0),
                                         (EQ("KC"), "Karmine Corp", EQ("CFO"), "CFO", 0)]),
       T0(g + "4"), W(g + "4", "Hoy"), [W(g + "4", "grupos"), W(g + "4", "semifinal")], y=.45, nombre="resultados FS25 b"),
    vs(W(g + "4", "Hoy"), T1(g + "4") + .3, "CFO", "KC", "Hoy, el desempate", "Jueves 29 de octubre", y=.42),
]
# ================================================================== CIERRE
g = "cierre_"
FX += [
    mg(L.calendario("Jueves 29 de octubre · hora del centro de México", [("14:00", "CFO vs\nKarmine Corp", "amarillo"),
                                                                         ("17:00", "TES vs BLG", "oro")]),
       T0(g + "0"), T1(g + "0") + .3, [W(g + "0", "dos"), W(g + "0", "cinco")], y=.45, nombre="horarios"),
    peg(T0(g + "1"), EQ("CFO"), "¿La ostra voladora?", R, dur=W(g + "1", "comentarios") - T0(g + "1"), x=.27, y=.47, tam=380),
    peg(W(g + "1", "muro") - .3, EQ("KC"), "¿El Blue Wall?", A, dur=W(g + "1", "comentarios") - W(g + "1", "muro") + .3, x=.73, y=.47,
        tam=380),
    tar(W(g + "1", "comentarios"), W(g + "1", "Nos"), "¿Con quién vas?", "Déjalo en los comentarios", "oro", x=.5, y=.45, tam=76),
    mg(L.apertura("¡NOS VEMOS!", "CFO vs KC · jueves 29 de octubre · 2:00 p. m."), W(g + "1", "Nos"), _TL["total"], x=.5, y=.5,
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
