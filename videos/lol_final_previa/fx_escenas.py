# -*- coding: utf-8 -*-
"""Montaje de las escenas SIN jugada de la previa de la final (todas menos j1, j3_ctx, j3, j3_fin, j2, j4, j5, j6_ctx, j6, j6_fin,
que están en fx_jugadas.py). Lo ejecuta efectos.py con exec en su propio espacio (FX, AZUL, K y los helpers).
Fondo = VOD real del partido que nombra la voz (x1, pausa o congelado con zoom; nunca más rápido): medios/_fuente/r_*.mp4, j4b.mp4 y
tramos libres de j1/j2/j4/j5/j6/j6_baron (lo que no usan las jugadas); fase suiza de BLG = EXT lol_semana2 (blte_j3, hlbl_j1).
Sin VOD (no existe clip): fase suiza de Gen.G y de BLG contra KOI/Liquid/Karmine, la partida 1 contra LYON (AMPLIACION.md), la
fecha de la final y la historia 2023-2024 → `fondo()` animado con los escudos. Datos: investigacion/feed_*.txt, oro_*.json (cada
10 s del feed oficial), datos_relleno.md, datos_duelos.md, AMPLIACION.md; comentarios reales en pegatinas/com_<id>.png.
Personas reales: pegatina de transmisión (mg_lol), camafeo, banda, abanico o marco opaco de peg_anim (nunca silueta, 10-nov)."""
import math as _m

import cv2 as _cv
import numpy as _np

_i0 = len(FX)

# ---------------------------------------------------------------- recursos que faltan aquí (escudos de TES y TLAW)
_EQ0 = EQ


def EQ(cod):
    p = _EQ0(cod)
    return p if os.path.exists(p) else os.path.abspath(os.path.join(_D, "..", "lol_semana2", "iconos", "equipos", cod + ".png"))


for _k, _v in {"r_lyon2": 1541, "r_ig1": 1978, "r_ig2": 1350, "r_ig3fin": 2342, "r_dk2": 583, "r_dk3fin": 1933, "r_t1g1": 1758,
               "j4b": 1382, "hlbl_j1": 2402.5, "blte_j3": 1706, "j6": 1860, "j5": 1904, "j2": 910, "j1": 1490.7, "j4": 1802}.items():
    K.setdefault(_k, _v)


# ---------------------------------------------------------------- helpers de este archivo
def velo(de, a, k=.45):
    """capa oscura sobre el VOD para que los gráficos grandes se lean (el FX `oscurecer` va antes del video y no se ve)"""
    arr = _np.zeros((1080, 1920, 4), _np.uint8)
    arr[..., 3] = int(255 * k)
    return dict(tipo="mg", fn=lambda dt, dur, m: arr, de=de, a=a, x=.5, y=.5, entra=.3, sale=.3, nombre="pizarra velo")


_FONDO = {}


def fondo(de, a, logos, nombre="fondo"):
    """pantalla de transmisión SIN VOD (cuando no existe clip): azul noche, rejilla hextech, escudos que derivan y un barrido dorado"""
    key = tuple(logos)
    if key not in _FONDO:
        yy, xx = _np.mgrid[0:1080, 0:1920].astype(_np.float32)
        r = _np.clip(1 - _np.hypot((xx - 960) / 1920, (yy - 450) / 1080) * 1.7, 0, 1)[..., None]
        base = _np.float32((22, 12, 5)) * (1 - r) + _np.float32((80, 46, 18)) * r
        base[:, ::96] += 7
        base[::96, :] += 7
        ims = []
        for c in logos:
            im = _cv.imread(EQ(c), _cv.IMREAD_UNCHANGED)
            if im.shape[2] == 3:
                im = _np.dstack([im, _np.full(im.shape[:2], 255, _np.uint8)])
            ims.append(_cv.resize(im, (720, 720), interpolation=_cv.INTER_AREA).astype(_np.float32))
        _FONDO[key] = (base, ims, (xx + yy * .6))
    base, ims, diag = _FONDO[key]
    n = len(ims)

    def fn(dt, dur, m):
        f = base.copy()
        for i, lg in enumerate(ims):
            cx = 1920 * (.5 if n == 1 else .26 + .48 * i) + 28 * _m.sin(dt * .4 + 2 * i)
            cy = 540 + 20 * _m.cos(dt * .33 + i)
            x0, y0 = int(cx - 360), int(cy - 360)
            al = lg[..., 3:4] / 255 * .15
            f[y0:y0 + 720, x0:x0 + 720] = f[y0:y0 + 720, x0:x0 + 720] * (1 - al) + lg[..., :3] * al
        p = ((dt * .2) % 1.8 - .35) * 2600
        f += _np.exp(-((diag - p) / 170) ** 2)[..., None] * _np.float32((60, 120, 160)) * .35
        return _np.dstack([_np.clip(f, 0, 255).astype(_np.uint8), _np.full((1080, 1920), 255, _np.uint8)])

    return dict(tipo="pantalla", fn=fn, de=de, a=a, x=.5, y=.5, nombre=nombre)


def FZ(n, de, a, t, z=1.12, cx=.5, cy=.5, chip=None):
    """cuadro congelado con acercamiento lento (nunca quieto); chip = texto de la pizarra («PAUSA · 32:58», «PARTIDA 2 · …»)"""
    out = [J(n, de, a, t, 0, zoom=(z, cx, cy), zoom0=(1.0, .5, .5), zoom_dur=max(.6, a - de))]
    if chip:
        out.append(pizarra(de, a, [], H(n, t) if n in K else "", pausa=chip))
    return out


def SYNC2(n, pares):
    """como SYNC (nada pasa de x1; si no cabe, corte a mitad), pero si sobra tiempo PAUSA en el cuadro del momento que acaba de
    nombrar la voz (chip «PAUSA · reloj» + zoom lento) y luego sigue a x1 hasta llegar al siguiente justo a tiempo. Un salto de
    menos de 1 s se ve como tirón: en vez de cortar, sigue a x1 y llega un poco tarde (el retraso lo absorbe la pausa siguiente)."""
    out = []
    cur = pares[0][1]
    for (a, _t0), (b, t1) in zip(pares, pares[1:]):
        if b - a <= .03:
            continue
        dur = b - a
        if t1 is None:
            out.append(J(n, a, b, cur, 1.0))
            cur += dur
            continue
        need = t1 - cur
        if need > 1.05 * dur:
            if need - dur < 1.0:
                out.append(J(n, a, b, cur, 1.0))
                cur += dur
            else:
                out += TRAMO(n, a, b, cur, t1)
                cur = t1
            continue
        if need >= .8 * dur:
            out += TRAMO(n, a, b, cur, t1)
            cur = t1
            continue
        hold = dur - max(0.0, need)
        z = min(1.15, 1.03 + .02 * hold)
        out.append(J(n, a, a + hold, cur, 0, zoom=(z, .5, .5), zoom0=(1.0, .5, .5), zoom_dur=hold))
        if hold >= 1.2 and n in K:
            out.append(pizarra(a, a + hold, [], H(n, cur)))
        if b - (a + hold) > .03:
            out.append(J(n, a + hold, b, cur, 1.0, zoom=(1.0, .5, .5), zoom0=(z, .5, .5), zoom_dur=min(.5, b - a - hold)))
        cur = max(cur, t1)
    return out


import peg_anim as _PA  # noqa: E402

_MARCOS = ("polaroid", "museo", "carta", "clasico", "cristal")
_npv = [0]


def pv(en, img, titulo, dur=4.0, x=.75, y=.5, tam=600, **anim):
    """pegatina con marco OPACO (personas reales) y animación del rotador del video (peg_anim)"""
    ruta = img if (os.path.sep in img or "/" in img) else JUG(img)
    anim.setdefault("marco", _MARCOS[_npv[0] % len(_MARCOS)])
    _npv[0] += 1
    fn = _PA.variado(ruta, titulo, tam, tema="gaming", **anim)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.06, nombre="pegatina " + os.path.basename(ruta), ver=1.0)


def duelo(de, a, ja, jb, titulo, filas, marcas):
    """cara a cara por posición (mg_lol.duelo): ja/jb = (jugador, equipo, sub)"""
    (na, ea, sa), (nb, eb, sb) = ja, jb
    return mg(L.duelo((JUG(na), na, EQ(ea), COLOR(ea), sa), (JUG(nb), nb, EQ(eb), COLOR(eb), sb), titulo, filas), de, a, marcas,
              y=.5, nombre=f"duelo {na}-{nb}")


def cartas(campeones):
    return [(CARGA(c), c.replace("Leblanc", "LeBlanc").replace("Viktor", "Víktor").replace("LeeSin", "Lee Sin").replace("Kaisa", "Kai'Sa"))
            for c in campeones]


def R2(*xs):
    return [x for x in xs if x is not None]


T_ = lambda k, p, n=0: W(k, p, n)          # noqa: E731

# ================================================================== GANCHO (T1 cae · la final · el menú)
AZUL = {"T1"}
g = "gancho_"
e0, e1 = ESC("gancho")
a1, b2, b3 = T0(g + "1"), T0(g + "2"), T0(g + "3")
# j6 (T1-BLG partida 4, HUD = t + 1860): t 77,7 al empezar «En nueve segundos» → Oner cae en t 78, Doran en 83, Faker en 87
FX += [J("j6", e0, b2, 77.7 - a1, 1.0),
       mg(L.apertura("GEN.G vs BLG", "Todo antes de la gran final · Worlds 2026"), e0, T0(g + "0") + .3, x=.5, y=.5, nombre="apertura"),
       dict(tipo="destello", en=.15, fuerza=.7),
       tar(W(g + "0", "Domingo"), W(g + "0", "T1"), "Domingo · semifinal", "Partida 4 · Bilibili 2-1 T1", "oro", x=.26, y=.17, tam=46),
       tar(W(g + "0", "T1"), W(g + "0", "quinientos"), "T1 con el Barón", "Le quedan 2 segundos", A, logo="T1", x=.26, y=.17, tam=46),
       tar(W(g + "0", "quinientos"), T1(g + "0") + .3, "A menos de 500 de oro", "32:16 · BLG +0,4K", R, logo="BLG", x=.26, y=.17, tam=46),
       oro(W(g + "0", "partida"), T1(g + "0") + .4, "125", 14 * 60, 32 * 60 + 16, [24 * 60, 28 * 60, 32 * 60 + 16],
           [W(g + "0", "partida") + .8, W(g + "0", "perdiendo"), W(g + "0", "seis") + .5], "T1", "BLG", titulo="T1 - BLG · partida 4",
           desfase=5)]
FX += [marcador(a1, W(g + "1", "cuarto"), "T1", "BLG", [("izq", 1), ("izq", 0), ("izq", 2)], [a1 + .4, a1 + 5.4, a1 + 9.4],
                titulo="EN 9 SEGUNDOS"),
       cam(W(g + "1", "Oner"), "Oner", "Oner", dur=W(g + "1", "era") - W(g + "1", "Oner"), x=.07, y=.5, tam=190),
       cam(W(g + "1", "Doran"), "Doran", "Doran", dur=W(g + "1", "era") - W(g + "1", "Doran"), x=.2, y=.45, tam=190),
       cam(W(g + "1", "Faker"), "Faker", "Faker", dur=W(g + "1", "era") - W(g + "1", "Faker"), x=.32, y=.45, tam=190),
       tar(W(g + "1", "tres"), W(g + "1", "cuarto"), "3 Mundiales seguidos", "2023 · 2024 · 2025", A, logo="T1", x=.26, y=.17, tam=46),
       elim(W(g + "1", "cuarto"), b2 + .3, "T1", "T1", "El 4.º se queda en semifinales · 1-3", [W(g + "1", "semifinales")]),
       dict(tipo="destello", en=a1 + 9.4, fuerza=.4)]
# el sábado, la final: Gen.G (r_ig3fin, celebración de la semifinal) y Bilibili (r_dk3fin, cuartos)
AZUL = {"GEN"}
k = g + "2"
gb, gu, go = W(k, "Bilibili"), W(k, "Uno"), W(k, "otro")
FX += [J("r_ig3fin", b2, gb, 76.0, 1.0), J("r_dk3fin", gb, gu, 37.0, 1.0), J("r_ig3fin", gu, go, 76.0 + (gb - b2), 1.0),
       J("r_dk3fin", go, b3, 37.0 + (gu - gb), 1.0),
       tar(b2 + .1, W(k, "Gen"), "Sábado · Nueva York", "La gran final", "oro", x=.5, y=.17, tam=56),
       vs(W(k, "Gen"), gu, "GEN", "BLG", "La gran final", "Sábado 14 de noviembre · Nueva York", y=.42),
       tar(gu, go, "Gen.G: primera final en 9 años", "La última, en 2017, como Samsung Galaxy", A, logo="GEN", x=.5, y=.17, tam=52),
       tar(go, b3 + .2, "Bilibili perdió la última", "Final de 2024 · 2-3 contra T1", R, logo="BLG", dato="2-3", x=.5, y=.17, tam=52),
       dict(tipo="destello", en=gb, fuerza=.3)]
k = g + "3"
FX += [J("j3_3d", b3, e1, 0.0, 1.0), velo(b3, e1, .55),
       mg(L.menu([(ART("Yunara"), "A Nueva York", "oro"), (ART("Taliyah"), "Jugadas en 3D", "azul"),
                  (ART("Ahri"), "El cara a cara", "amarillo"), (ART("Viktor"), "Las claves", "rojo")]),
          b3 + .1, e1, [W(k, "camino"), W(k, "jugadas"), W(k, "cara"), W(k, "decidir")], y=.52, nombre="menu")]

# ================================================================== LA VOZ (Karen y Luis)
g = "voz_"
e0, e1 = ESC("voz")
b = T0(g + "1")
ka, lu = W(g + "0", "Karen"), W(g + "0", "Luis")
FX += [J("j6", e0, e1, 2.0, 1.0), velo(e0, e1, .45),
       tar(e0 + .1, ka, "Lo que nos pidieron", "Comentarios del último video", "oro", x=.5, y=.17, tam=52),
       com(ka, "UgzdTGS9S_FatHvDJeh4AaABAg", lu - ka - .1, y=.42, tam=1000),
       tar(W(g + "0", "Diez"), lu, "10 me gusta", "Le dieron la razón a Karen", "oro", x=.5, y=.78, tam=52),
       com(lu, "UgwZLRXew6Lq9FIaBBZ4AaABAg", b - lu + .2, y=.42, tam=1000),
       tar(b, W(g + "1", "Todos"), "Mensaje recibido", "La voz de siempre, de vuelta", "oro", x=.5, y=.5, tam=84),
       tar(W(g + "1", "Todos"), e1, "Todos los comentarios se leen", "Este video se hizo con ellos", "oro", x=.5, y=.5, tam=72)]

# ================================================================== LA FINAL (llave, sede, hora, qué está en juego)
g = "final_"
e0, e1 = ESC("final")
b1, b2 = T0(g + "1"), T0(g + "2")
k = g + "0"
FX += [fondo(e0, b2, ["GEN", "BLG"]),
       mg(L.llave("El camino a la final", [(EQ("GEN"), "Gen.G", EQ("LYON"), "LYON", "Cuartos · 3-0"),
                                            (EQ("GEN"), "Gen.G", EQ("IG"), "Invictus", "Semis · 3-0"),
                                            (EQ("BLG"), "Bilibili", EQ("DK"), "Dplus KIA", "Cuartos · 3-0"),
                                            (EQ("BLG"), "Bilibili", EQ("T1"), "T1", "Semis · 3-1")]),
          e0 + .1, W(k, "mejor"), [e0 + .4, e0 + 1.0, e0 + 1.6, e0 + 2.2, W(k, "Barclays")], y=.43, nombre="llave final"),
       tar(W(k, "Barclays"), W(k, "mejor"), "Barclays Center", "Brooklyn, Nueva York · sábado 14", "oro", x=.5, y=.93, tam=40),
       tar(W(k, "mejor"), b1 + .2, "Al mejor de 5", "El primero que gane 3 es campeón del mundo", "oro", x=.5, y=.5, tam=80),
       mg(L.calendario("Sábado 14 · la hora de la final", [("13:00", "Centro de México", "oro"), ("16:00", "Argentina", "azul"),
                                                           ("20:00", "España", "rojo")]),
          b1 + .1, b2 + .1, [W(g + "1", "una"), W(g + "1", "cuatro"), W(g + "1", "ocho")], y=.5, nombre="calendario hora final")]
k = g + "2"
s0, s1 = W(k, "Si"), W(k, "Si", 1)
FX += [*FZ("r_ig3fin", b2, s1, 96.0, 1.15, .5, .45), *FZ("r_dk3fin", s1, e1, 50.0, 1.15, .5, .45), velo(b2, e1, .25),
       tar(b2 + .1, s0, "Más que un trofeo", None, "oro", x=.5, y=.84, tam=60),
       tar(s0, s1, "Si gana Gen.G", "Corea: su 5.º Mundial seguido", A, logo="GEN", dato="5.º", x=.5, y=.84, tam=54),
       tar(s1, e1, "Si gana Bilibili", "China: su primer título desde 2021", R, logo="BLG", dato="2021", x=.5, y=.84, tam=54)]

# ================================================================== EL PÚBLICO (r_escenario: previa de la semifinal en Texas)
g = "final_publico_"
e0, e1 = ESC("final_publico")
k0, k1, k2 = g + "0", g + "1", g + "2"
cc, ny = W(k0, "carteles"), W(k0, "Nueva")
FX += [J("r_escenario", e0, cc, 10.0, 1.0), J("r_escenario", cc, cc + 1.6, 2.7, 1.0),
       *FZ("r_escenario", cc + 1.6, T0(k1), 4.3, 1.9, .2, .62),
       J("r_escenario", T0(k1), T0(k2), 4.3, 1.0)]
es = W(k2, "estadio")
dur = e1 - es
t_es = 26.0 if dur <= 7.0 else max(24.0, 33.0 - (dur - 1.8))
FX += [J("r_escenario", T0(k2), T0(k2) + 2.0, 0.0, 1.0), J("r_escenario", T0(k2) + 2.0, es, 19.0, 1.0)]
fin_x1 = min(e1, es + (32.95 - t_es))
FX += [J("r_escenario", es, fin_x1, t_es, 1.0)]
if e1 - fin_x1 > .05:
    FX += FZ("r_escenario", fin_x1, e1, 32.95, 1.08)
FX += [tar(e0 + .3, W(k0, "Texas"), "Semifinal · Texas", "Antes de Gen.G vs Invictus", "oro", x=.26, y=.17, tam=46),
       tar(ny, T0(k1) + .1, "«See you in NY»", "Nos vemos en Nueva York", "oro", x=.5, y=.84, tam=56),
       peg(W(k1, "Invictus"), EQ("IG"), "Invictus", R, None, None, dur=T1(k1) - W(k1, "Invictus") + .3, x=.12, y=.24, tam=200),
       peg(W(k1, "Gen"), EQ("GEN"), "Gen.G", A, None, None, dur=T1(k1) - W(k1, "Gen") + .3, x=.27, y=.24, tam=200),
       cam(W(k1, "Wei"), "Wei", "Wei · Invictus", dur=T1(k1) - W(k1, "Wei") + .4, x=.42, y=.22, tam=200),
       tar(W(k1, "Wei"), T1(k1) + .3, "«WEI WIN»", "Que gane Wei", R, logo="IG", x=.5, y=.84, tam=50),
       tar(T0(k2), es, "Las dos cabinas", "Y los campeones elegidos en las pantallas", "oro", x=.5, y=.84, tam=50),
       tar(W(k2, "hagan"), e1, "«MAKE NOISE»", "Hagan ruido", "oro", x=.5, y=.84, tam=60)]

# ================================================================== GEN.G: LA FASE SUIZA Y LAS ELIMINATORIAS
AZUL = {"GEN"}
g = "gen_suiza_"
e0, e1 = ESC("gen_suiza")
b1, b2 = T0(g + "1"), T0(g + "2")
k = g + "0"
FX += [fondo(e0, b1, ["GEN"]),
       tar(e0 + .15, W(k, "fase"), "Gen.G", "LCK #1 · Corea", A, logo="GEN", x=.5, y=.84, tam=60),
       mg(L.resultados("Gen.G en la fase suiza", [(EQ("GEN"), "Gen.G", EQ("IG"), "Invictus", 0), (EQ("GEN"), "Gen.G", EQ("HLE"), "Hanwha Life", 0),
                                                  (EQ("GEN"), "Gen.G", EQ("LYON"), "LYON", 0)]),
          W(k, "fase"), b1, [W(k, "Invictus"), W(k, "Hanwha"), W(k, "LYON")], y=.42, nombre="resultados suiza GEN"),
       tar(W(k, "Tres"), b1 + .1, "3 de 3", "Directo a cuartos", A, logo="GEN", dato="3-0", x=.5, y=.84, tam=60)]
# j1 (GEN-LYON partida 3, HUD = t + 1490,7) corre a x1 desde b1 hasta el inicio de la jugada j1 (t 47,1), con dos cuadros insertados
nv, ac = W(g + "2", "Nueve"), W(g + "2", "Acuerdate")
sg, l1 = W("gen_lyon_0", "segunda"), T0("gen_lyon_1")
for de, a in ((b1, nv), (ac, sg), (l1, ESC("gen_lyon")[1])):
    FX.append(J("j1", de, a, de - b1, 1.0))
FX += FZ("r_ig1", nv, ac, 22.6, 1.25, .45, .45, chip="PARTIDA 1 VS IG")
k = g + "1"
FX += [velo(b1, b2, .35),
       mg(L.resultados("Gen.G en eliminatorias", [(EQ("GEN"), "Gen.G", EQ("LYON"), "LYON", 0), (EQ("GEN"), "Gen.G", EQ("IG"), "Invictus", 0)]),
          b1 + .1, b2 + .1, [W(k, "eliminatorias"), W(k, "eliminatorias") + .5], y=.4, nombre="resultados elim GEN"),
       tar(W(k, "Seis"), W(k, "Seis", 1), "6 partidas", "Cuartos y semifinales", "oro", x=.5, y=.84, tam=56),
       tar(W(k, "Seis", 1), b2 + .2, "6 victorias", "Ninguna derrota", A, logo="GEN", dato="6-0", x=.5, y=.84, tam=56)]
k = g + "2"
FX += [mg(L.ficha_jugador(JUG("Ruler"), "Ruler", EQ("GEN"), 1, [("Asesinatos en eliminatorias", "38", .95), ("En una partida contra IG", "9", .45)],
                          color="azul", sub="Tirador · el que más mata en Gen.G"),
          W(k, "Ruler"), ac, [W(k, "treinta"), nv], y=.47, nombre="ficha Ruler"),
       tar(nv, ac, "Partida 1 contra Invictus", "9 asesinatos de Ruler · Jhin", A, icono="Jhin", x=.26, y=.88, tam=40),
       pv(ac, "Ruler", "Ruler", dur=e1 - ac + .2, x=.74, y=.5, tam=600),
       tar(ac, e1 + .2, "Ruler", "Acuérdate de este nombre", A, logo="GEN", x=.3, y=.84, tam=60)]

# ================================================================== CUARTOS: GEN.G vs LYON
g = "gen_lyon_"
e0, e1 = ESC("gen_lyon")
k = g + "0"
FX += [vs(W(k, "cuartos"), W(k, "organizacion"), "GEN", "LYON", "Cuartos de final", "Miércoles 4 de noviembre", y=.42),
       tar(W(k, "organizacion"), W(k, "diecinueve"), "LYON", "Organización mexicana · ya cayó ante Gen.G en la suiza", R, logo="LYON", x=.5, y=.84, tam=50),
       tar(W(k, "diecinueve"), sg, "Partida 1", "Gen.G 19 - LYON 8", A, logo="GEN", dato="19-8", x=.28, y=.84, tam=46),
       tar(W(k, "veintidos"), sg, "Partida 2", "Gen.G 22 - LYON 6", A, logo="GEN", dato="22-6", x=.72, y=.84, tam=46),
       *FZ("r_lyon2", sg, l1, 36.3, 1.2, .5, .45, chip="PARTIDA 2"),
       cam(W(k, "Ruler"), "Ruler", "Ruler · Ashe", dur=l1 - W(k, "Ruler"), x=.09, y=.3, tam=210),
       tar(W(k, "Ruler"), l1 + .1, "Ruler: 8 asesinatos", "Partida 2 · Ashe", A, icono="Ashe", dato="8", x=.5, y=.84, tam=50)]
k = g + "1"
FX += [tar(W(k, "tercera"), W(k, "minuto"), "Partida 3", "La única en la que LYON le pegó", R, logo="LYON", x=.5, y=.84, tam=52),
       tar(W(k, "minuto"), e1 + .2, "Minuto 20: LYON 10 - Gen.G 8", "En asesinatos", R, logo="LYON", dato="10-8", x=.5, y=.84, tam=50)]

# ================================================================== LYON PARTIDA 1 (no hay clip: pantalla de transmisión)
g = "lyon_p1_"
e0, e1 = ESC("lyon_p1")
k = g + "0"
pr, sa, ca = W(k, "primera"), W(k, "sangre"), W(k, "Canyon")
FX += [fondo(e0, e1, ["GEN", "LYON"]),
       tar(e0 + .1, pr, "Gen.G vs LYON", "Las otras dos partidas de la serie", "oro", x=.5, y=.84, tam=56),
       vs(pr, sa, "GEN", "LYON", "Partida 1", "Cuartos de final", ganador=0, marca=W(k, "diecinueve"), y=.4),
       tar(W(k, "diecinueve"), sa, "19 a 8", "Gana Gen.G", A, logo="GEN", dato="19-8", x=.5, y=.84, tam=56),
       peg(sa, "Berserker", "Berserker", R, "LYON", "Primera sangre · sobre Duro", dur=ca - sa + .2, x=.3, y=.45, tam=420),
       peg(sa + .3, "Duro", "Duro", A, "GEN", "Minuto 1", dur=ca - sa - .1, x=.7, y=.45, tam=360, gris=True),
       pv(ca, "Canyon", "Canyon · 6 asesinatos", dur=e1 - ca + .2, x=.3, y=.48, tam=560),
       pv(W(k, "Kiin"), "Kiin", "Kiin · 6 asesinatos", dur=e1 - W(k, "Kiin") + .2, x=.7, y=.48, tam=560),
       tar(W(k, "seis"), e1 + .2, "6 asesinatos cada uno", "Partida 1 · Gen.G 19-8", A, logo="GEN", dato="6", x=.5, y=.9, tam=44),
       oro(pr + .2, e1, "116", 0, 32 * 60 + 12, [8 * 60, 20 * 60, 32 * 60 + 10], [W(k, "diecinueve"), sa, W(k, "seis")], "GEN", "LYON",
           titulo="Partida 1 · oro", x=.86, y=.2, escala=.45, desfase=3)]

# ================================================================== LYON PARTIDA 2 (r_lyon2, HUD = t + 1541; feed − HUD ≈ +3)
g = "lyon_p2_"
n = "r_lyon2"
e0, e1 = ESC("lyon_p2")
k0, k1, k2, k3 = (g + str(i) for i in range(4))
FX += VIVO("lyon_p2", n, 0.0, "Transmisión oficial · Gen.G vs LYON · partida 2", "GEN", "Minuto 25")
f0 = T0(k0)
FX += SYNC2(n, [(f0, f0 - e0), (W(k1, "Cae"), 14.6), (W(k1, "inhibidor"), 18.5), (W(k2, "Inspired"), 26.0), (W(k2, "Dhokla"), 27.6),
                (W(k2, "Isles"), 35.7), (W(k3, "Saint"), 38.6), (T1(k3) + .3, 39.6), (e1, None)])
FX += [tar(W(k0, "ocho"), W(k0, "Minuto"), "Ruler: 8 asesinatos", "En la partida 2 · Ashe", A, icono="Ashe", x=.27, y=.27, tam=44),
       tar(W(k0, "Minuto"), W(k0, "ocho", 1), "Barón de Gen.G", "25:41 · 17 a 6", A, logo="GEN", x=.27, y=.27, tam=44),
       tar(W(k0, "ocho", 1), T0(k1) + .3, "+8,4K de oro", "Gen.G, con el Barón", A, logo="GEN", dato="+8,4K", x=.27, y=.27, tam=44),
       oro(W(k0, "Minuto"), T1(k3) + 1.0, "117", 18 * 60, 26 * 60 + 24, [25 * 60 + 41, 25 * 60 + 57, 26 * 60 + 8, 26 * 60 + 20],
           [W(k0, "ocho", 1), W(k1, "Cae"), W(k2, "Dhokla"), W(k3, "Veintidos")], "GEN", "LYON", titulo="Gen.G - LYON · partida 2", desfase=3),
       tar(W(k1, "Cae"), W(k1, "inhibidor"), "Cae la torre", "Gen.G entra a la base de LYON", A, logo="GEN", x=.27, y=.27, tam=44),
       tar(W(k1, "inhibidor"), T0(k2), "Frente al inhibidor", "Ahí se arma la pelea", "oro", x=.27, y=.27, tam=44),
       marcador(T0(k2) - .2, e1 - .3, "GEN", "LYON", [("der", 1), ("der", 0), ("der", 4), ("der", 2), ("der", 3)],
                [W(k2, "Inspired"), W(k2, "Dhokla"), W(k2, "Isles"), W(k3, "Saint"), W(k3, "Veintidos")], titulo="LA PELEA"),
       cam(W(k2, "Ruler"), "Ruler", "Ruler · Ashe", dur=2.6, x=.07, y=.5, tam=190),
       cam(W(k2, "Chovy"), "Chovy", "Chovy", dur=2.2, x=.07, y=.7, tam=190),
       tar(W(k2, "doble"), T0(k3) + .2, "Doble de Ruler", "Inspired e Isles", A, icono="Ashe", x=.27, y=.27, tam=44),
       cam(W(k3, "Chovy"), "Chovy", "Chovy · Víktor", dur=3.0, x=.07, y=.5, tam=190),
       tar(W(k3, "doble"), W(k3, "Veintidos"), "Doble de Chovy", "Dhokla y Saint", A, icono="Viktor", x=.27, y=.27, tam=44),
       tar(W(k3, "Veintidos"), e1, "22 a 6", "5 por 0 en la pelea · ninguna baja", A, logo="GEN", dato="5-0", x=.27, y=.27, tam=44),
       dict(tipo="destello", en=W(k3, "Veintidos"), fuerza=.35)]

# ================================================================== SEMIFINAL: GEN.G vs INVICTUS
g = "gen_ig_"
e0, e1 = ESC("gen_ig")
b1 = T0(g + "1")
k = g + "0"
ts, la, v7 = W(k, "TheShy"), W(k, "Las"), W(k, "veintisiete")
FX += [J("r_escenario", e0, ts, 18.5, 1.0), *FZ("r_ig2", ts, la, 2.0, 1.15), *FZ("r_ig1", la, v7, 43.6, 1.12),
       *FZ("r_ig2", v7, b1, 41.5, 1.12), velo(ts, b1, .3),
       tar(e0 + .1, W(k, "Invictus"), "Semifinales", "Sábado 7 de noviembre · Texas", "oro", x=.5, y=.17, tam=56),
       vs(W(k, "Invictus"), la, "GEN", "IG", "Semifinal", "Gen.G vs Invictus Gaming", y=.36),
       peg(ts, "TheShy", "TheShy", R, "IG", "Top", dur=la - ts, x=.12, y=.55, tam=330),
       peg(W(k, "Rookie"), "Rookie", "Rookie", R, "IG", "Medio", dur=la - W(k, "Rookie"), x=.88, y=.55, tam=330),
       peg(W(k, "Top"), EQ("TES"), "Top Esports", R, None, "Eliminado por Invictus · 1-3", dur=la - W(k, "Top"), x=.5, y=.8, tam=230,
           gris=True, sello=("FUERA", 0), marcas=[W(k, "Top") + .6]),
       tar(W(k, "veintinueve"), W(k, "Cincuenta"), "Partida 1", "Gen.G 29 - Invictus 9", A, logo="GEN", dato="29-9", x=.28, y=.84, tam=46),
       tar(v7, W(k, "Cincuenta"), "Partida 2", "Gen.G 27 - Invictus 9", A, logo="GEN", dato="27-9", x=.72, y=.84, tam=46),
       tar(W(k, "Cincuenta"), b1 + .2, "56 a 18", "Asesinatos en las dos primeras", A, logo="GEN", dato="56-18", x=.5, y=.5, tam=72)]
k = g + "1"
FX += [*FZ("r_ig3fin", b1, e1, 0.3, 1.1, chip="PARTIDA 3"), velo(b1, e1, .4),
       oro(b1 + .1, e1, "130", 0, 39 * 60 + 1, [10 * 60, 18 * 60 + 22, 39 * 60 + 1], [b1 + 1.2, W(k, "perdiendo"), e1 - .2], "IG", "GEN",
           titulo="Invictus - Gen.G · partida 3", x=.5, y=.45, escala=1.0, desfase=4.5),
       tar(b1 + .1, W(k, "perdiendo"), "Partida 3", "La mejor de Gen.G en el Mundial", "oro", x=.5, y=.88, tam=48),
       tar(W(k, "perdiendo"), e1 + .1, "Y la iba perdiendo", "Invictus, arriba en oro", A, logo="IG", x=.5, y=.88, tam=48)]

# ================================================================== GEN-IG PARTIDA 1 (r_ig1, HUD = t + 1978; feed − HUD ≈ +3)
g = "ig_p1_"
n = "r_ig1"
e0, e1 = ESC("ig_p1")
k0, k1, k2, k3 = (g + str(i) for i in range(4))
p = W(k0, "Primera")
q = W(k0, "Ruler") + .9
FX += [J(n, e0, p, 0.0, 1.0), *REB(n, p, p - e0, 0.4), *PZ(n, p + 1.2, q, 0.4, [])]
FX += SYNC2(n, [(q, 0.4), (W(k1, "Invictus"), 3.0), (W(k1, "JiaQi"), 10.5), (W(k1, "Canyon"), 20.0), (W(k1, "TheShy"), 22.6),
                (W(k1, "Meiko"), 25.6), (W(k2, "Duro"), 28.6), (W(k2, "Canyon"), 31.6), (W(k2, "cae"), 34.3), (W(k3, "Ruler"), 35.9),
                (e1, 43.95)])
FX += [tar(e0 + .1, p, "Las dos primeras", "Semifinal · Gen.G vs Invictus", "oro", x=.27, y=.27, tam=44),
       tar(p + 1.2, W(k0, "catorce"), "Partida 1 · minuto 33", "32:58 · 24 a 6", A, logo="GEN", x=.27, y=.27, tam=44),
       tar(W(k0, "catorce"), W(k0, "Ruler"), "+14,8K de oro", "Gen.G", A, logo="GEN", dato="+14,8K", x=.27, y=.27, tam=44),
       tar(W(k0, "Ruler"), T0(k1) + .4, "Ruler tira un inhibidor", "Jhin", A, icono="Jhin", x=.27, y=.27, tam=44),
       oro(W(k0, "minuto"), T0(k1) + 2.0, "128", 15 * 60, 32 * 60 + 58, [25 * 60, 32 * 60 + 58], [W(k0, "minuto") + 1.0, W(k0, "catorce")],
           "GEN", "IG", titulo="Gen.G - Invictus · partida 1", desfase=3),
       marcador(T0(k1), T1(k3) + .5, "GEN", "IG", [("izq", 0), ("der", 3), ("der", 0), ("der", 4), ("izq", 4), ("izq", 1), ("der", 1), ("der", 2)],
                [W(k1, "JiaQi"), W(k1, "Canyon"), W(k1, "TheShy"), W(k1, "Meiko"), W(k2, "Duro"), W(k2, "Canyon"), W(k2, "cae") + .2,
                 W(k2, "cae") + .6], titulo="LA ÚLTIMA PELEA"),
       tar(W(k1, "defiende"), W(k1, "JiaQi"), "Invictus defiende", "Frente a las torres del nexo", R, logo="IG", x=.27, y=.27, tam=44),
       cam(W(k1, "JiaQi"), "JiaQi", "JiaQi · Xayah", dur=2.4, x=.93, y=.5, tam=190),
       cam(W(k1, "Canyon"), "Canyon", "Canyon", dur=2.2, x=.07, y=.5, tam=190),
       cam(W(k1, "Ruler"), "Ruler", "Ruler · Jhin", dur=2.2, x=.07, y=.7, tam=190),
       cam(W(k1, "Chovy"), "Chovy", "Chovy", dur=2.2, x=.07, y=.5, tam=190),
       cam(W(k2, "Wei"), "Wei", "Wei · Vi", dur=3.0, x=.93, y=.5, tam=190),
       tar(W(k2, "alcanza"), T0(k3) + .2, "Cae todo Invictus", "Junto al nexo", A, logo="GEN", x=.27, y=.27, tam=44),
       tar(W(k3, "Cinco"), W(k3, "uno"), "5 por 3", "La última pelea", A, logo="GEN", dato="5-3", x=.27, y=.27, tam=44),
       tar(W(k3, "uno"), e1, "Gen.G 1-0", "Semifinal", A, logo="GEN", dato="1-0", x=.27, y=.27, tam=44),
       dict(tipo="destello", en=W(k2, "cae"), fuerza=.35)]

# ================================================================== GEN-IG PARTIDA 2 (r_ig2, HUD = t + 1350; feed − HUD ≈ +2,5)
g = "ig_p2_"
n = "r_ig2"
e0, e1 = ESC("ig_p2")
k0, k1, k2, k3, k4, k5 = (g + str(i) for i in range(6))
FX += VIVO("ig_p2", n, 0.0, "Transmisión oficial · Gen.G vs Invictus · partida 2", "GEN", "Minuto 22")
f0 = T0(k0)
lib = e0 + 5.6                       # las tarjetas del «En vivo» se van en e0 + 5,5
FX += REB(n, f0, f0 - e0, 0.5)
FX += SYNC2(n, [(f0 + 1.2, 0.5), (W(k1, "Meiko"), 8.8), (W(k1, "dragon"), 18.6), (W(k2, "Chovy"), 21.0), (W(k2, "Ruler"), 23.6),
                (W(k2, "JiaQi"), 26.0), (W(k3, "Wei"), 28.6), (W(k3, "Rookie"), 31.6), (W(k4, "TheShy"), 37.6), (T0(k5), 41.4), (e1, 41.4)])
FX += [tar(max(lib, W(k0, "Segunda")), W(k0, "Baron"), "Partida 2 · minuto 22", "22:30 · 12 a 5", A, logo="GEN", x=.27, y=.27, tam=44),
       tar(W(k0, "Baron"), W(k0, "pelea"), "Barón de Gen.G", "+6,4K de oro", A, logo="GEN", dato="+6,4K", x=.27, y=.27, tam=44),
       tar(W(k0, "pelea"), T0(k1) + .3, "Junto al foso", "Del dragón hextech", "oro", x=.27, y=.27, tam=44),
       oro(max(lib, W(k0, "Segunda")), T0(k2), "129", 14 * 60, 23 * 60 + 8, [20 * 60, 22 * 60 + 30, 22 * 60 + 49],
           [max(lib, W(k0, "Segunda")) + 1.0, W(k0, "seis"), W(k1, "dragon")], "GEN", "IG", titulo="Gen.G - Invictus · partida 2", desfase=2.5),
       marcador(T0(k1) - .2, T1(k4) + .5, "GEN", "IG", [("der", 4), ("izq", 2), ("izq", 3), ("der", 3), ("der", 1), ("der", 2), ("der", 0)],
                [W(k1, "Meiko"), W(k2, "Chovy"), W(k2, "Ruler"), W(k2, "JiaQi"), W(k3, "Wei"), W(k3, "Rookie"), W(k4, "TheShy")],
                titulo="LA PELEA DEL DRAGÓN"),
       cam(W(k1, "Chovy"), "Chovy", "Chovy · Ahri", dur=2.8, x=.07, y=.5, tam=190),
       tar(W(k1, "dragon"), T0(k2) + .3, "Dragón hextech", "Para Gen.G", A, logo="GEN", x=.27, y=.27, tam=44),
       cam(W(k2, "TheShy"), "TheShy", "TheShy · Rumble", dur=3.0, x=.93, y=.5, tam=190),
       cam(W(k3, "Kiin"), "Kiin", "Kiin · Gwen", dur=3.2, x=.07, y=.5, tam=190),
       tar(W(k3, "Doble"), T0(k4) + .2, "Doble de Kiin", "Wei y Rookie", A, icono="Gwen", x=.27, y=.27, tam=44),
       cam(W(k4, "Canyon"), "Canyon", "Canyon", dur=2.6, x=.07, y=.5, tam=190),
       tar(W(k4, "Diecisiete"), T0(k5) + .2, "17 a 7", "5 por 2 · cae todo Invictus", A, logo="GEN", dato="5-2", x=.27, y=.27, tam=44),
       velo(T0(k5), e1, .45),
       oro(T0(k5), e1, "129", 22 * 60 + 30, 29 * 60 + 10, [23 * 60 + 8, 29 * 60 + 5], [T0(k5) + .8, W(k5, "dos")], "GEN", "IG",
           titulo="Partida 2 · hasta el final", x=.5, y=.42, escala=.95, desfase=2.5),
       tar(W(k5, "dos"), W(k5, "llega"), "Gen.G 2-0", "Partida 2: 27 a 9", A, logo="GEN", dato="2-0", x=.5, y=.86, tam=50),
       tar(W(k5, "llega"), e1, "Y llega la tercera", None, "oro", x=.5, y=.86, tam=56)]

# ================================================================== GEN-IG PARTIDA 3: EL CIERRE (r_ig3fin, IG azul; HUD = t + 2342)
AZUL = {"IG"}
g = "ig3_cierre_"
n = "r_ig3fin"
e0, e1 = ESC("ig3_cierre")
k0, k1, k2, k3, k4 = (g + str(i) for i in range(5))
FX += SYNC2(n, [(e0, 0.3), (W(k1, "JiaQi"), 10.0), (W(k1, "TheShy"), 14.0), (W(k1, "Meiko"), 17.6), (T0(k2), 22.0), (W(k2, "tira"), 35.3),
                (W(k2, "Ruler"), 47.3), (W(k3, "Rookie"), 61.9), (W(k3, "camaras"), 62.4), (W(k4, "abraza"), 68.0), (W(k4, "cinco"), 92.0),
                (W(k4, "saludan"), 98.0), (e1, 102.9)])
FX += [tar(e0 + .1, W(k0, "Minuto"), "Así terminó la semifinal", "Partida 3", "oro", x=.27, y=.27, tam=44),
       tar(W(k0, "Minuto"), W(k0, "pero"), "Minuto 39", "Invictus 18 - Gen.G 12", A, logo="IG", dato="18-12", x=.27, y=.27, tam=44),
       tar(W(k0, "pero"), T0(k1) + .3, "Gen.G +1,9K", "Arriba en oro", R, logo="GEN", x=.27, y=.27, tam=44),
       oro(W(k0, "Minuto"), T0(k2), "130", 30 * 60, 39 * 60 + 20, [36 * 60, 39 * 60 + 1, 39 * 60 + 18], [W(k0, "Minuto") + 1, W(k0, "oro"), W(k1, "Meiko")],
           "IG", "GEN", titulo="Invictus - Gen.G · partida 3", desfase=4.5),
       marcador(T0(k1) - .2, T0(k4), "IG", "GEN", [("izq", 3), ("izq", 0), ("izq", 4), ("izq", 2)],
                [W(k1, "JiaQi"), W(k1, "TheShy"), W(k1, "Meiko"), W(k3, "Rookie")], titulo="LA ÚLTIMA PELEA"),
       cam(W(k1, "Ruler"), "Ruler", "Ruler · Yunara", dur=2.8, x=.07, y=.5, tam=190),
       cam(W(k1, "Kiin"), "Kiin", "Kiin · Camille", dur=3.2, x=.07, y=.7, tam=190),
       tar(W(k1, "doble"), T0(k2) + .2, "Doble de Kiin", "TheShy y Meiko", R, icono="Camille", x=.27, y=.27, tam=44),
       tar(W(k2, "rio"), W(k2, "Ruler"), "Gen.G cruza el río", "Y tira las torres", R, logo="GEN", x=.27, y=.27, tam=44),
       tar(W(k2, "Ruler"), T0(k3) + .3, "Ruler rompe un inhibidor", None, R, icono="Yunara", x=.27, y=.27, tam=44),
       tar(W(k3, "Rookie"), W(k3, "camaras"), "El último asesinato", "Ruler sobre Rookie, junto al nexo", R, icono="Yunara", x=.27, y=.27, tam=44),
       cam(W(k3, "camaras"), "Ruler", "Ruler", dur=3.0, x=.07, y=.5, tam=200),
       tar(W(k4, "Gen"), e1, "Gen.G 3-0 Invictus", "A la gran final", R, logo="GEN", dato="3-0", x=.5, y=.84, tam=54),
       dict(tipo="destello", en=W(k3, "Rookie"), fuerza=.35)]

# ================================================================== BILIBILI: LA FASE SUIZA
AZUL = {"BLG"}
g = "blg_suiza_"
e0, e1 = ESC("blg_suiza")
k0, k1, k2 = (g + str(i) for i in range(3))
c, h, ga = W(k1, "perdio"), W(k1, "tuvo"), W(k1, "Gano", 1)
FX += [fondo(e0, c, ["BLG"]),
       tar(e0 + .1, W(k0, "fase"), "Bilibili Gaming", "LPL #2 · China", A, logo="BLG", x=.5, y=.84, tam=60),
       mg(L.resultados("Bilibili en la fase suiza", [(EQ("BLG"), "Bilibili", EQ("MKOI"), "Movistar KOI", 1),
                                                     (EQ("BLG"), "Bilibili", EQ("TLAW"), "Team Liquid", 0), (EQ("BLG"), "Bilibili", EQ("KC"), "Karmine", 0)]),
          W(k0, "fase"), c, [W(k0, "Movistar"), W(k1, "Liquid"), W(k1, "Karmine")], y=.42, nombre="resultados suiza BLG"),
       # BLG-TES partida 2 (EXT lol_semana2, HUD = t + 1706): +5,2K a las 28:49 (t 23) antes de perder a 4 jugadores
       J("blte_j3", c, h, 19.0, 1.0),
       tar(c, h, "Perdió con Top Esports", "Iba +5,2K · 28:49", R, logo="TES", x=.5, y=.84, tam=54),
       # BLG-HLE partida 1 (EXT, HUD = t + 2402,5): el cuádruple de Knight, t 62-67,5 (41:05-41:10)
       J("hlbl_j1", h, e1, 62.0 - (ga - h), 1.0),
       tar(h, ga, "A todo o nada", "Contra Hanwha Life", R, logo="HLE", x=.5, y=.84, tam=54),
       tar(ga, W(k1, "cuadruple"), "Bilibili 2-0", "Contra Hanwha Life", A, logo="BLG", dato="2-0", x=.27, y=.27, tam=44),
       cam(W(k1, "Knight"), "Knight", "Knight · Orianna", dur=4.0, x=.07, y=.5, tam=200),
       tar(W(k1, "cuadruple"), T0(k2) + 1.5, "Cuádruple de Knight", "41:05 · partida 1", A, icono="Orianna", x=.27, y=.27, tam=44),
       tar(T0(k2), W(k2, "Entro"), "3 victorias, 2 derrotas", "Fase suiza", A, logo="BLG", dato="3-2", x=.5, y=.84, tam=54),
       tar(W(k2, "Entro"), e1 + .2, "A cuartos", "Por la puerta de atrás", A, logo="BLG", x=.5, y=.84, tam=54)]

# ================================================================== CUARTOS: BILIBILI vs DPLUS KIA (j2 = partida 1, HUD = t + 910)
g = "blg_dk_"
e0, e1 = ESC("blg_dk")
k0, k1 = g + "0", g + "1"
FX += [J("j2", e0, e1, 40.6 - (e1 - e0), 1.0),
       vs(W(k0, "Cuartos"), W(k0, "uno"), "BLG", "DK", "Cuartos de final", "Jueves 5 de noviembre", y=.4),
       tar(W(k0, "uno"), T0(k1) + .2, "Dplus KIA", "Pasó invicta la fase suiza · 3-0", R, logo="DK", dato="3-0", x=.5, y=.84, tam=54),
       tar(W(k1, "Bilibili"), W(k1, "pelea"), "Bilibili 3-0", "24-10 · 13-10 · 25-9", A, logo="BLG", dato="3-0", x=.5, y=.84, tam=54),
       tar(W(k1, "pelea"), e1 + .3, "Partida 1 · minuto 16", "La pelea que marcó la serie", "oro", x=.5, y=.84, tam=54)]

# ================================================================== BLG-DK PARTIDA 2 (r_dk2, DK azul; HUD = t + 583; desde t 38,9 = repetición)
AZUL = {"DK"}
g = "dk_p2_"
n = "r_dk2"
e0, e1 = ESC("dk_p2")
k0, k1, k2, k3, k4 = (g + str(i) for i in range(5))
FX += VIVO("dk_p2", n, 0.0, "Transmisión oficial · Bilibili vs Dplus KIA · partida 2", "BLG", "Minuto 9")
f0 = T0(k0)
lib = e0 + 5.6
FX += REB(n, f0, f0 - e0, 0.4)
FX += SYNC2(n, [(f0 + 1.2, 0.4), (W(k1, "Llegan"), 6.5), (W(k1, "Lucid"), 12.3), (W(k1, "ON"), 15.2), (W(k2, "Smash"), 18.3), (W(k2, "Xun"), 20.3),
                (W(k3, "ShowMaker"), 23.2), (e1, None)])
FX += [tar(max(lib, W(k0, "Minuto")), T0(k1), "Partida 2 · minuto 9", "Río de abajo, junto al dragón", "oro", x=.27, y=.27, tam=44),
       cam(W(k0, "ON"), "ON", "ON", dur=2.6, x=.07, y=.5, tam=180), cam(W(k0, "Xun"), "Xun", "Xun", dur=2.6, x=.07, y=.7, tam=180),
       cam(W(k0, "Lucid"), "Lucid", "Lucid", dur=2.6, x=.93, y=.5, tam=180), cam(W(k0, "Career"), "Career", "Career", dur=2.6, x=.93, y=.7, tam=180),
       cam(W(k1, "ShowMaker"), "ShowMaker", "ShowMaker", dur=2.4, x=.93, y=.5, tam=180),
       cam(W(k1, "Knight"), "Knight", "Knight", dur=2.4, x=.07, y=.5, tam=180), cam(W(k1, "Viper"), "Viper", "Viper", dur=2.4, x=.07, y=.7, tam=180),
       oro(max(lib, W(k0, "Minuto")), T0(k3), "099", 4 * 60, 10 * 60 + 12, [9 * 60 + 43, 10 * 60 + 5], [W(k0, "Minuto") + 1.0, W(k2, "Smash")],
           "DK", "BLG", titulo="Dplus KIA - Bilibili · partida 2", desfase=5.5),
       marcador(W(k1, "Llegan"), e1 - .3, "DK", "BLG", [("izq", 1), ("der", 4), ("izq", 3), ("der", 1), ("izq", 2)],
                [W(k1, "Lucid"), W(k1, "ON"), W(k2, "Smash"), W(k2, "Xun"), W(k3, "ShowMaker")], titulo="EL RÍO DE ABAJO"),
       tar(W(k2, "doble"), T0(k3), "Doble de ShowMaker", "ON y Xun", A, icono="Ryze", x=.27, y=.27, tam=44),
       tar(W(k3, "Doble"), W(k4, "Fue"), "Doble de Viper", "3 por 2 para Bilibili", R, icono="Ezreal", dato="3-2", x=.27, y=.27, tam=44),
       tar(W(k4, "Fue"), e1, "Bilibili 13 - 10", "La partida más apretada de la serie", R, logo="BLG", dato="13-10", x=.5, y=.84, tam=52),
       dict(tipo="destello", en=W(k3, "ShowMaker"), fuerza=.35)]

# ================================================================== BLG-DK PARTIDA 3 (r_dk3fin, DK azul; HUD = t + 1933)
g = "dk_p3_"
n = "r_dk3fin"
e0, e1 = ESC("dk_p3")
k0, k1, k2 = (g + str(i) for i in range(3))
FX += SYNC2(n, [(e0, 0.3), (W(k1, "Xun"), 4.0), (W(k1, "Bin"), 12.5), (W(k2, "Cae"), 21.8), (W(k2, "Tres"), 27.5), (W(k2, "choca"), 32.5),
                (e1, 56.8)])
FX += [tar(W(k0, "tercera"), W(k0, "Minuto"), "Partida 3", "Sin discusión", "oro", x=.27, y=.27, tam=44),
       tar(W(k0, "Minuto"), W(k0, "veintidos"), "Barón de Bilibili", "32:13", R, logo="BLG", x=.27, y=.27, tam=44),
       tar(W(k0, "veintidos"), W(k0, "dentro"), "22 a 9", "En asesinatos", R, logo="BLG", dato="22-9", x=.27, y=.27, tam=44),
       tar(W(k0, "dentro"), T0(k1) + .3, "Dentro de la base de DK", "+6,9K de oro", R, logo="BLG", x=.27, y=.27, tam=44),
       oro(W(k0, "Minuto"), T0(k1) + .5, "100", 20 * 60, 32 * 60 + 13, [28 * 60, 32 * 60 + 13], [W(k0, "Minuto") + .8, W(k0, "dentro")],
           "DK", "BLG", titulo="Dplus KIA - Bilibili · partida 3", desfase=4),
       tar(W(k1, "Xun"), W(k1, "Bin"), "Xun tira un inhibidor", None, R, logo="BLG", x=.27, y=.27, tam=44),
       tar(W(k1, "Bin"), W(k1, "Jax"), "Bin, otro", None, R, logo="BLG", x=.27, y=.27, tam=44),
       mg(L.premio("Partida 3 · el mejor", JUG("Bin"), "Bin", EQ("BLG"), ["12 asesinatos con Jax", "7 sobre Siwoo, el top de DK"], color="rojo",
                   sub="Top · Bilibili"), W(k1, "Jax"), T0(k2), [W(k1, "doce"), W(k1, "Siete")], y=.52, nombre="premio Bin"),
       cam(W(k1, "Siwoo"), "Siwoo", "Siwoo · DK", dur=T0(k2) - W(k1, "Siwoo"), x=.92, y=.13, tam=150),
       tar(W(k2, "Cae"), W(k2, "Tres"), "Cae el nexo", None, R, logo="BLG", x=.27, y=.27, tam=44),
       tar(W(k2, "Tres"), e1, "Bilibili 3-0 Dplus KIA", "A semifinales", R, logo="BLG", dato="3-0", x=.5, y=.84, tam=54),
       dict(tipo="destello", en=W(k2, "Cae"), fuerza=.4)]

# ================================================================== SEMIFINAL: BILIBILI vs T1 (j5 libre t 14-30; r_t1g1 = partida 1)
AZUL = {"BLG"}
g = "t1_ctx_"
e0, e1 = ESC("t1_ctx")
k0, k1 = g + "0", g + "1"
b1 = T0(k1)
FX += [J("j5", e0, b1, 14.0, 1.0),
       tar(e0 + .1, W(k0, "Bilibili"), "La semifinal", "Domingo 8 de noviembre", "oro", x=.5, y=.84, tam=56),
       vs(W(k0, "Bilibili"), W(k0, "revancha"), "BLG", "T1", "Semifinal", "Bilibili vs T1", y=.4),
       tar(W(k0, "campeon"), W(k0, "revancha"), "T1", "Campeón de 2023, 2024 y 2025", R, logo="T1", dato="3", x=.5, y=.84, tam=54),
       tar(W(k0, "revancha"), b1 + .2, "La revancha", "Final de 2024 · T1 3-2 Bilibili", "oro", logo="BLG", dato="2-3", x=.5, y=.84, tam=54),
       *FZ("r_t1g1", b1, e1, 0.0, 1.12, chip="PARTIDA 1"), velo(b1, e1, .35),
       tar(b1 + .1, W(k1, "dieciocho"), "Partida 1", "Bilibili vs T1", "oro", x=.5, y=.84, tam=54),
       mg(L.premio("Partida 1 · el mejor", JUG("Knight"), "Knight", EQ("BLG"), ["Bilibili gana 18 a 6", "9 asesinatos de Knight"], color="azul",
                   sub="Medio · Bilibili"), W(k1, "dieciocho") - .2, W(k1, "Faker"), [W(k1, "dieciocho"), W(k1, "nueve")], y=.5,
          nombre="premio Knight p1"),
       peg(W(k1, "Faker"), "Faker", "Faker", R, "T1", "Locke · 4 asesinatos", dur=e1 - W(k1, "Faker") + .2, x=.5, y=.47, tam=440),
       tar(W(k1, "alcanzo"), e1 + .2, "No alcanzó", "T1 pierde la partida 1", R, logo="T1", x=.5, y=.88, tam=48)]

# ================================================================== BLG-T1 PARTIDA 1 (r_t1g1, BLG azul; HUD = t + 1758; feed − HUD ≈ +4)
g = "t1_p1_"
n = "r_t1g1"
e0, e1 = ESC("t1_p1")
k0, k1, k2 = (g + str(i) for i in range(3))
FX += VIVO("t1_p1", n, 0.0, "Transmisión oficial · Bilibili vs T1 · partida 1", "BLG", "Minuto 29")
f0 = T0(k0)
lib = e0 + 5.6
FX += SYNC2(n, [(f0, f0 - e0), (W(k0, "encuentran"), 12.0), (W(k1, "Oner"), 18.6), (W(k1, "Keria"), 21.0), (W(k1, "Doran"), 24.6),
                (W(k2, "Peyz"), 31.0), (W(k2, "Faker"), 34.0), (e1, None)])
FX += [tar(max(lib, W(k0, "Minuto")), W(k0, "catorce"), "Partida 1 · minuto 29", "29:18", A, logo="BLG", x=.27, y=.27, tam=44),
       tar(W(k0, "catorce"), T0(k1) + .2, "14 a 6 · +5,1K", "Bilibili", A, logo="BLG", dato="+5,1K", x=.27, y=.27, tam=44),
       oro(max(lib, W(k0, "Minuto")), T1(k2) + .5, "122", 20 * 60, 29 * 60 + 55, [29 * 60 + 18, 29 * 60 + 38, 29 * 60 + 51],
           [W(k0, "cinco"), W(k1, "Oner"), W(k2, "Cuatro")], "BLG", "T1", titulo="Bilibili - T1 · partida 1", desfase=4),
       marcador(T0(k1) - .2, e1 - .3, "BLG", "T1", [("der", 1), ("der", 4), ("der", 0), ("der", 3)],
                [W(k1, "Oner"), W(k1, "Keria"), W(k1, "Doran"), W(k2, "Peyz")], titulo="LA PELEA DE LA JUNGLA"),
       cam(W(k1, "Viper"), "Viper", "Viper · Corki", dur=2.4, x=.07, y=.5, tam=190),
       cam(W(k1, "Knight"), "Knight", "Knight", dur=2.6, x=.07, y=.7, tam=190),
       tar(W(k1, "doble"), T0(k2) + .2, "Doble de Knight", "Keria y Doran", A, logo="BLG", x=.27, y=.27, tam=44),
       cam(W(k2, "Xun"), "Xun", "Xun · Naafiri", dur=2.4, x=.07, y=.5, tam=190),
       tar(W(k2, "Cuatro"), e1, "4 por 0", "Faker se escapa con lo justo", A, logo="BLG", dato="4-0", x=.27, y=.27, tam=44),
       cam(W(k2, "Faker"), "Faker", "Faker · se escapa", dur=4.0, x=.93, y=.5, tam=190),
       dict(tipo="destello", en=W(k1, "Doran"), fuerza=.3)]

# ================================================================== LA JUGADA DE FAKER EN LA PARTIDA 2 (j4b, T1 azul; HUD = t + 1382)
AZUL = {"T1"}
g = "faker_p2_"
n = "j4b"
e0, e1 = ESC("faker_p2")
k0, k1, k2, k3, k4, k5, k6 = (g + str(i) for i in range(7))
FX += SYNC2(n, [(e0, 0.0), (W(k0, "alma"), 12.3), (W(k1, "roba"), 13.3), (W(k2, "ON"), 16.3), (W(k2, "barra"), 19.1), (W(k3, "Xun"), 19.6),
                (W(k3, "Oner"), 21.8), (W(k3, "Keria"), 35.5), (W(k4, "Faker"), 36.6), (W(k5, "Peyz"), 40.7), (W(k5, "Knight"), 43.5),
                (W(k5, "alcanza"), 46.2), (T0(k6), 46.7)])
p6 = T1(k6) + .2
FX += [J(n, T0(k6), p6, 46.7, 0, zoom=(1.14, .5, .5), zoom0=(1.0, .5, .5), zoom_dur=p6 - T0(k6)), pizarra(T0(k6), p6, [], H(n, 46.7)),
       J(n, p6, e1, 46.7, 1.0), en_vivo(p6 + .1, "Transmisión oficial · así lo cantaron", "T1")]
FX += [tar(e0 + .1, W(k0, "Minuto"), "Partida 2", "Otra jugada · 7 minutos antes", "oro", x=.27, y=.27, tam=44),
       tar(W(k0, "Minuto"), W(k0, "cuarto"), "Minuto 23 · T1", "Barón y 3 dragones", A, logo="T1", x=.27, y=.27, tam=44),
       tar(W(k0, "cuarto"), W(k1, "roba"), "El 4.º dragón", "El del océano: le da el alma", "oro", x=.27, y=.27, tam=44),
       oro(W(k0, "Minuto"), T0(k2), "123", 15 * 60, 23 * 60 + 15, [23 * 60 + 2, 23 * 60 + 15], [W(k0, "Minuto") + 1.0, W(k1, "roba")],
           "T1", "BLG", titulo="T1 - Bilibili · partida 2", desfase=6),
       tar(W(k1, "roba"), T0(k2) + .3, "¡Robado!", "El dragón del océano y el alma", A, logo="T1", x=.27, y=.27, tam=44),
       marcador(T0(k2) - .2, T1(k5) + .6, "T1", "BLG", [("der", 4), ("der", 1), ("izq", 1), ("izq", 4), ("der", 3), ("der", 2)],
                [W(k2, "ON"), W(k3, "Xun"), W(k3, "Oner"), W(k3, "Keria"), W(k5, "Viper"), W(k5, "alcanza")], titulo="LA PELEA DEL ALMA"),
       cam(W(k2, "Doran"), "Doran", "Doran · Olaf", dur=2.6, x=.07, y=.5, tam=190),
       cam(W(k2, "Faker"), "Faker", "Faker · Syndra", dur=T1(k2) - W(k2, "Faker"), x=.07, y=.7, tam=200),
       tar(W(k2, "Zhonya"), T1(k2) + .3, "Reloj de arena de Zhonya", "No le pueden hacer daño", Y, icono="Syndra", x=.27, y=.27, tam=44),
       tar(W(k3, "doble"), W(k3, "Viper"), "Doble de Doran", "ON y Xun", A, icono="Olaf", x=.27, y=.27, tam=44),
       cam(W(k3, "Viper"), "Viper", "Viper · Kai'Sa", dur=3.0, x=.93, y=.5, tam=190),
       tar(W(k4, "Faker"), T0(k5) + .3, "Llega Faker", "Con la teleportación", A, icono="SummonerTeleport", x=.27, y=.27, tam=44),
       cam(W(k5, "Peyz"), "Peyz", "Peyz · Jhin", dur=2.4, x=.07, y=.5, tam=190),
       cam(W(k5, "Knight"), "Knight", "Knight · LeBlanc", dur=3.0, x=.93, y=.5, tam=190),
       tar(W(k5, "alcanza"), T0(k6) + .3, "Syndra lo alcanza", "23:48", A, icono="Syndra", x=.27, y=.27, tam=44),
       tar(W(k6, "Cuatro"), W(k6, "ventaja"), "4 por 2 para T1", "Con el alma del océano", A, logo="T1", dato="4-2", x=.27, y=.27, tam=44),
       oro(W(k6, "ventaja") - .2, W(k6, "Faker"), "123", 20 * 60, 24 * 60 + 2, [23 * 60 + 48, 24 * 60 + 2], [W(k6, "ventaja"), W(k6, "dos")],
           "T1", "BLG", titulo="T1 - Bilibili · después del alma", x=.5, y=.45, escala=.85, desfase=6),
       pv(W(k6, "Faker"), "Faker", "Faker · no murió en toda la partida", dur=W(k6, "Asi") - W(k6, "Faker") + .3, x=.5, y=.48, tam=600),
       tar(W(k6, "Asi"), p6 + .1, "Así lo cantó la transmisión", None, "oro", x=.5, y=.84, tam=56),
       dict(tipo="destello", en=W(k1, "roba"), fuerza=.35)]

# ================================================================== LOS COMENTARIOS DE T1 (j4: T1 celebra la partida 2; j6_baron: el público)
g = "t1_com_"
e0, e1 = ESC("t1_com")
k0, k1 = g + "0", g + "1"
m4 = min(e1, e0 + 15.0)
FX += [J("j4", e0, m4, 133.0, 1.0), J("j6_baron", m4, e1, 28.6, 1.0, zoom=(1.15, .56, .56), zoom0=(1.15, .56, .56)), velo(e0, e1, .35),
       com(W(k0, "Rolnesc"), "UgwIctSzVxir3xTjeOV4AaABAg", T1(k0) - W(k0, "Rolnesc") + .4, y=.42, tam=980),
       cam(W(k0, "Faker"), "Faker", "Faker", dur=T1(k0) - W(k0, "Faker") + .4, x=.1, y=.8, tam=180),
       cam(W(k0, "Keria"), "Keria", "Keria", dur=T1(k0) - W(k0, "Keria") + .4, x=.9, y=.8, tam=180),
       tar(W(k0, "Asi", 1), T1(k0) + .4, "Así se sintió medio planeta", None, "oro", x=.5, y=.84, tam=50),
       com(W(k1, "igcid"), "UgzQ2CTfmw1tnwSfATV4AaABAg", W(k1, "Aqui") - W(k1, "igcid"), y=.42, tam=980),
       tar(W(k1, "Aqui"), e1, "Aquí seguimos", "Nos vemos en 2027", "oro", logo="T1", x=.5, y=.5, tam=72)]

# ================================================================== LOS NÚMEROS DEL CAMINO (feed: marcadores de las 13 partidas)
AZUL = {"GEN"}
g = "numeros_"
e0, e1 = ESC("numeros")
k0, k1, k2, k3 = (g + str(i) for i in range(4))
b1, b2, b3 = T0(k1), T0(k2), T0(k3)
u = W(k2, "unica")
FX += [*FZ("r_lyon2", e0, b1, 39.5, 1.12), J("j2", b1, b2, 2.0, 1.0), *FZ("r_ig1", b2, u, 43.6, 1.12), *FZ("r_ig3fin", u, b3, 72.5, 1.12),
       J("j2", b3, e1, 2.0 + (b2 - b1), 1.0), velo(e0, b2, .5), velo(b3, e1, .5),
       mg(L.duelo((EQ("GEN"), "Gen.G", EQ("GEN"), "azul", "6 partidas"), (EQ("BLG"), "Bilibili", EQ("BLG"), "rojo", "7 partidas"),
                  "Los números del camino", [("Asesinatos", "129", "130", 129 / 130, 1.0, 1), ("Asesinatos en contra", "60", "76", 60 / 76, 1.0, 0)]),
          e0 + .1, b2, [W(k0, "ciento"), W(k0, "sesenta")], y=.5, nombre="duelo numeros"),
       tar(W(k1, "Bilibili"), b2, "Una partida más", "7 contra 6", R, logo="BLG", x=.5, y=.93, tam=40),
       tar(W(k2, "veintinueve"), u, "La paliza más grande", "Gen.G 29 - Invictus 9 · partida 1", A, logo="GEN", dato="29-9", x=.5, y=.17, tam=54),
       tar(u, b3 + .2, "La única vez que mató menos", "Partida 3 contra Invictus · y la ganó", A, logo="GEN", dato="16-18", x=.5, y=.17, tam=54),
       mg(L.duelo((EQ("GEN"), "Gen.G", EQ("GEN"), "azul", "6 partidas"), (EQ("BLG"), "Bilibili", EQ("BLG"), "rojo", "7 partidas"),
                  "La primera sangre", [("Primera sangre", "3 de 6", "3 de 7", .5, 3 / 7, None), ("Partidas perdidas", "0", "1", .02, .14, 0)]),
          b3 + .1, e1, [W(k3, "tres"), W(k3, "una")], y=.5, nombre="duelo primera sangre")]

# ================================================================== EL CARA A CARA (investigacion/datos_duelos.md)
g = "duelos_intro_"
e0, e1 = ESC("duelos_intro")
k = g + "0"
se, si = W(k, "seis"), W(k, "siete")
FX += [*FZ("r_ig3fin", e0, si, 99.5, 1.1), *FZ("r_dk3fin", si, e1, 53.0, 1.1), velo(e0, e1, .4),
       tar(e0 + .1, e1, "El cara a cara", "Posición por posición · eliminatorias", "oro", x=.5, y=.15, tam=64),
       abanico(se, e1 + .2, [(JUG(j), j) for j in ROSTER["GEN"].split()], [se + .15 * i for i in range(5)], x=.27, y=.58, tam=200, nombre="abanico GEN"),
       abanico(si, e1 + .2, [(JUG(j), j) for j in ROSTER["BLG"].split()], [si + .15 * i for i in range(5)], x=.73, y=.58, tam=200, nombre="abanico BLG")]

for sid, (fa, ta), (fb, tb), ja, jb, tit, filas, palabras in [
        ("duelo_top", ("r_ig2", 31.6), ("r_dk3fin", 13.0), ("Kiin", "GEN", "Top · 6 partidas"), ("Bin", "BLG", "Top · 7 partidas"), "Top",
         [("Muertes", "9", "17", 9 / 17, 1.0, 0), ("Asesinatos", "25", "30", 25 / 30, 1.0, 1), ("KDA", "8,0", "3,9", .8, .39, 0)],
         [("0", "nueve"), ("0", "treinta"), ("0", "seguro")]),
        ("duelo_jungla", ("r_ig1", 20.0), ("r_dk2", 12.3), ("Canyon", "GEN", "Jungla · 6 partidas"), ("Xun", "BLG", "Jungla · 7 partidas"), "Jungla",
         [("KDA", "9,1", "7,8", .91, .78, 0), ("Asesinatos", "27", "29", 27 / 29, 1.0, 1), ("Asistencias", "64", "65", 64 / 65, 1.0, 1),
          ("Muertes", "10", "12", 10 / 12, 1.0, 0)],
         [("0", "mejor"), ("0", "veintisiete"), ("0", "sesenta"), ("0", "diez")]),
        ("duelo_adc", ("r_ig3fin", 10.0), ("r_dk2", 23.0), ("Ruler", "GEN", "Tirador · 6 partidas"), ("Viper", "BLG", "Tirador · 7 partidas"),
         "Tirador", [("Asesinatos", "38", "37", 1.0, 37 / 38, 0), ("Súbditos por partida", "322", "322", 1.0, 1.0, None),
                     ("Muertes", "11", "17", 11 / 17, 1.0, 0)],
         [("0", "treinta"), ("0", "trescientos"), ("1", "once")]),
        ("duelo_sup", ("r_ig1", 28.6), ("r_dk2", 15.2), ("Duro", "GEN", "Soporte · 6 partidas"), ("ON", "BLG", "Soporte · 7 partidas"), "Soporte",
         [("Asistencias", "77", "87", 77 / 87, 1.0, 1), ("Muertes", "19", "21", 19 / 21, 1.0, 0)],
         [("0", "Setenta"), ("0", "mueren")])]:
    e0, e1 = ESC(sid)
    mitad = W(sid + "_0", jb[0])
    FX += [*FZ(fa, e0, mitad, ta, 1.12), *FZ(fb, mitad, e1, tb, 1.12), velo(e0, e1, .5),
           duelo(e0 + .05, e1, ja, jb, tit, filas, [W(sid + "_" + i, p) for i, p in palabras])]

# medio: el duelo de la final + la primera final de Chovy
g = "duelo_mid_"
e0, e1 = ESC("duelo_mid")
k0, k1 = g + "0", g + "1"
b1 = T0(k1)
FX += [*FZ("r_lyon2", e0, W(k0, "Knight"), 38.6, 1.12), *FZ("r_t1g1", W(k0, "Knight"), b1, 24.6, 1.12), *FZ("r_ig2", b1, e1, 8.8, 1.12),
       velo(e0, e1, .5),
       duelo(e0 + .05, b1, ("Chovy", "GEN", "Medio · 6 partidas"), ("Knight", "BLG", "Medio · 7 partidas"), "Medio · el duelo de la final",
             [("KDA", "7,6", "10,2", .76, 1.0, 1), ("Asesinatos", "28", "29", 28 / 29, 1.0, 1), ("Asistencias", "56", "63", 56 / 63, 1.0, 1),
              ("Muertes", "11", "9", 1.0, 9 / 11, 1)],
             [W(k0, "mejor"), W(k0, "veintinueve"), W(k0, "sesenta"), W(k0, "nueve")]),
       mg(L.calendario("Chovy en el Mundial", [("2022", "Semifinal", "gris"), ("2024", "Semifinal", "gris"), ("2025", "Semifinal", "gris"),
                                               ("2026", "Su primera final", "oro")]),
          b1 + .1, e1, [W(k1, "veintidos"), W(k1, "veinticuatro"), W(k1, "veinticinco"), W(k1, "primera")], y=.62, nombre="calendario Chovy"),
       pv(b1 + .1, "Chovy", "Chovy · su primera final", dur=e1 - b1, x=.5, y=.27, tam=420)]

# ================================================================== LOS CAMPEONES (Fearless; datos_duelos.md § Campeones)
g = "campeones_"
e0, e1 = ESC("campeones")
k0, k1, k2, k3 = (g + str(i) for i in range(4))
b1, b2, b3 = T0(k1), T0(k2), T0(k3)
kn = W(k0, "Knight")
vi, as2 = W(k1, "Viper"), W(k1, "Ashe", 1)
ar, so = W(k2, "Arriba"), W(k2, "soporte")
FX += [*FZ("r_lyon2", e0, kn, 38.6, 1.1), *FZ("j4b", kn, b1, 34.6, 1.1), *FZ("r_ig1", b1, vi, 22.6, 1.1), *FZ("r_dk2", vi, b2, 22.5, 1.1),
       *FZ("r_ig1", b2, ar, 20.0, 1.1), *FZ("r_ig3fin", ar, so, 14.0, 1.1), *FZ("r_ig1", so, b3, 28.6, 1.1),
       *FZ("r_dk3fin", b3, W(k3, "Gen"), 25.0, 1.1), *FZ("r_ig3fin", W(k3, "Gen"), e1, 65.0, 1.1), velo(e0, e1, .5),
       tar(e0 + .1, W(k0, "Chovy"), "Un detalle de la selección", "Campeones distintos en eliminatorias", "oro", x=.5, y=.15, tam=56),
       cam(W(k0, "Chovy"), "Chovy", "Chovy · 5", dur=b1 - W(k0, "Chovy"), x=.27, y=.2, tam=200),
       abanico(W(k0, "cinco"), b1, cartas(["Ahri", "Cassiopeia", "Galio", "Taliyah", "Viktor"]), [W(k0, "cinco") + .12 * i for i in range(5)],
               x=.24, y=.58, tam=145, nombre="abanico Chovy"),
       cam(kn, "Knight", "Knight · 6", dur=b1 - kn, x=.73, y=.2, tam=200),
       abanico(W(k0, "seis"), b1, cartas(["Ahri", "Galio", "Leblanc", "Orianna", "Taliyah", "Viktor"]), [W(k0, "seis") + .12 * i for i in range(6)],
               x=.76, y=.58, tam=135, nombre="abanico Knight"),
       cam(W(k1, "Ruler"), "Ruler", "Ruler · 4", dur=as2 - W(k1, "Ruler"), x=.27, y=.2, tam=200),
       abanico(W(k1, "Ashe"), as2, cartas(["Ashe", "Jhin", "Xayah", "Yunara"]), [W(k1, "Ashe"), W(k1, "Ashe") + .35, W(k1, "Ashe") + .7, W(k1, "Yunara")],
               x=.24, y=.58, tam=145, nombre="abanico Ruler"),
       cam(vi, "Viper", "Viper · 6", dur=as2 - vi, x=.73, y=.2, tam=200),
       abanico(W(k1, "seis"), as2, cartas(["Ashe", "Cassiopeia", "Corki", "Ezreal", "Kaisa", "Lucian"]),
               [W(k1, "seis") + .12 * i for i in range(6)], x=.76, y=.58, tam=135, nombre="abanico Viper"),
       peg(as2, CARGA("Ashe"), "Ashe", "oro", None, "La única que comparten", dur=b2 - as2 + .1, x=.5, y=.48, tam=480),
       cam(W(k2, "Canyon"), "Canyon", "Canyon", dur=ar - W(k2, "Canyon"), x=.15, y=.3, tam=200),
       cam(W(k2, "Xun"), "Xun", "Xun", dur=ar - W(k2, "Xun"), x=.85, y=.3, tam=200),
       abanico(W(k2, "Lee"), ar, cartas(["LeeSin", "Pantheon", "Qiyana"]), [W(k2, "Lee"), W(k2, "Pantheon"), W(k2, "Qiyana")], x=.5, y=.58, tam=220,
               nombre="abanico jungla"),
       cam(W(k2, "Kiin"), "Kiin", "Kiin", dur=so - W(k2, "Kiin"), x=.15, y=.3, tam=200),
       cam(W(k2, "Bin"), "Bin", "Bin", dur=so - W(k2, "Bin"), x=.85, y=.3, tam=200),
       peg(W(k2, "Camille"), CARGA("Camille"), "Camille", "oro", None, "Arriba: la única que comparten", dur=so - W(k2, "Camille"), x=.5, y=.5,
           tam=440),
       cam(W(k2, "Duro"), "Duro", "Duro", dur=b3 - W(k2, "Duro"), x=.15, y=.3, tam=200),
       cam(W(k2, "ON"), "ON", "ON", dur=b3 - W(k2, "ON"), x=.85, y=.3, tam=200),
       abanico(W(k2, "Leona"), b3, cartas(["Leona", "Nautilus", "Seraphine"]), [W(k2, "Leona"), W(k2, "Nautilus"), W(k2, "Seraphine")], x=.5, y=.58,
               tam=220, nombre="abanico soporte"),
       tar(W(k3, "Bilibili"), e1 + .2, "Bilibili: 30 campeones", "En 7 partidas", R, logo="BLG", dato="30", x=.3, y=.5, tam=60),
       tar(W(k3, "Gen"), e1 + .2, "Gen.G: 23", "En 6 partidas", A, logo="GEN", dato="23", x=.72, y=.5, tam=60)]

# ================================================================== LA HISTORIA (2023-2024 sin clip: pantalla; los campeones del mundo)
g = "historia_"
e0, e1 = ESC("historia")
k0, k1, k2 = (g + str(i) for i in range(3))
b2 = T0(k2)
cy_, vp = W(k2, "Canyon"), W(k2, "Viper")
FX += [fondo(e0, b2, ["GEN", "BLG"]),
       tar(e0 + .1, W(k0, "dos"), "No es la primera vez", "Gen.G vs Bilibili", "oro", x=.5, y=.15, tam=56),
       mg(L.calendario("Gen.G vs Bilibili", [("2023 · MSI", "Gana Bilibili", "rojo"), ("2023 · Mundial", "Cuartos: BLG 3-2", "rojo"),
                                             ("2024 · MSI", "Gana Gen.G", "azul"), ("2024 · final MSI", "Gen.G 3-1", "azul"),
                                             ("2026 · final", "Sábado 14", "oro")]),
          e0 + .2, b2 + .2, [W(k0, "dos") + .2, W(k0, "cuartos"), W(k1, "MSI"), W(k1, "final"), T1(k1) - .3], y=.52, nombre="calendario historia"),
       *FZ("r_ig3fin", b2, cy_, 65.0, 1.12), *FZ("r_ig1", cy_, vp, 20.0, 1.12), *FZ("r_dk2", vp, e1, 23.0, 1.12),
       tar(b2, W(k2, "Ruler"), "En una final, la experiencia pesa", None, "oro", x=.5, y=.84, tam=52),
       banda(W(k2, "Ruler"), "Ruler", "Ruler", "Campeón del mundo 2017 · Samsung Galaxy", dur=cy_ - W(k2, "Ruler"), y=.45),
       banda(cy_, "Canyon", "Canyon", "Campeón del mundo 2020 · DAMWON", dur=vp - cy_, y=.45, lado="izq"),
       banda(vp, "Viper", "Viper", "Campeón del mundo 2021 · EDG", dur=e1 - vp + .2, y=.45),
       tar(W(k2, "ultimo"), e1 + .2, "El último campeón chino", "Viper · 2021", R, logo="BLG", x=.5, y=.84, tam=52)]

# ================================================================== TRES CLAVES (Fearless, el centro, la paciencia, los cierres)
g = "claves_"
e0, e1 = ESC("claves")
k0, k1, k2, k3, k4 = (g + str(i) for i in range(5))
b1, b2, b3, b4 = T0(k1), T0(k2), T0(k3), T0(k4)
FX += [J("j6", e0, b1, 24.0, 1.0), J("j5", b1, b2, 0.0, 1.0), J("j5", b2, b3, min(28.5, 37.0 - (b3 - b2)), 1.0),
       J("r_ig3fin", b3, b4, 4.0, 1.0), J("r_lyon2", b4, e1, min(3.0, 45.5 - (e1 - b4)), 1.0),
       velo(e0, b2, .4), velo(b3, b4, .35),
       tar(e0 + .1, W(k0, "Pero"), "3 claves para el sábado", None, "oro", x=.5, y=.5, tam=90),
       tar(W(k0, "Fearless"), W(k0, "cinco"), "Fearless", "El campeón que ya se usó en la serie, no se repite", "oro", x=.5, y=.84, tam=54),
       peg(W(k0, "campeon"), CARGA("Ashe"), "Ashe", "oro", None, "Ya usada en la serie", dur=T1(k0) - W(k0, "campeon") + .3, x=.5, y=.42, tam=440,
           gris=True, sello=("NO SE REPITE", 0), marcas=[W(k0, "elegir")]),
       tar(W(k0, "cinco"), b1 + .2, "En 5 partidas", "Gana el que tenga más fondo", "oro", x=.5, y=.84, tam=54),
       cam(W(k1, "Chovy"), "Chovy", "Chovy", dur=T1(k1) - W(k1, "Chovy") + .3, x=.12, y=.3, tam=210),
       cam(W(k1, "Knight"), "Knight", "Knight", dur=T1(k1) - W(k1, "Knight") + .3, x=.88, y=.3, tam=210),
       abanico(W(k1, "Ahri"), b2, cartas(["Ahri", "Galio", "Taliyah", "Viktor"]), [W(k1, "Ahri"), W(k1, "Galio"), W(k1, "Taliyah"), W(k1, "Viktor")],
               x=.5, y=.55, tam=230, nombre="abanico medio"),
       tar(W(k1, "elija"), b2 + .2, "El que elija primero", "Se los quita al otro", "oro", x=.5, y=.9, tam=48),
       tar(b2, W(k2, "Si", 1), "Clave 1: el centro", None, "oro", x=.5, y=.84, tam=60),
       tar(W(k2, "Si", 1), b3 + .2, "Si Knight juega como en la semifinal", "Ventaja para Bilibili en el centro", R, logo="BLG", x=.5, y=.84, tam=50),
       pv(W(k2, "Knight"), "Knight", "Knight · medio de Bilibili", dur=b3 - W(k2, "Knight") + .2, x=.76, y=.45, tam=560),
       oro(b3 + .1, b4, "130", 0, 18 * 60 + 22, [10 * 60, 18 * 60 + 22], [b3 + 1.2, W(k3, "cuatro")], "IG", "GEN",
           titulo="Invictus - Gen.G · partida 3", x=.5, y=.42, escala=.9, desfase=4.5),
       tar(b3, W(k3, "cuatro"), "Clave 2: la paciencia", "Gen.G: 6 de 6 en eliminatorias", A, logo="GEN", x=.5, y=.86, tam=50),
       tar(W(k3, "cuatro"), b4 + .2, "4 600 abajo contra Invictus", "Y aun así ganó · sabe esperar", A, logo="GEN", dato="-4,6K", x=.5, y=.86, tam=50),
       tar(b4, W(k4, "Las"), "Clave 3: los cierres", None, "oro", x=.5, y=.84, tam=60),
       tar(W(k4, "Las"), W(k4, "Las", 1), "Gen.G: unos 32 minutos", "Por partida, en eliminatorias", A, logo="GEN", dato="32'", x=.5, y=.84, tam=52),
       tar(W(k4, "Las", 1), e1 + .2, "Bilibili: un poco más", "El que imponga su ritmo, se lleva la copa", R, logo="BLG", x=.5, y=.84, tam=52)]

# ================================================================== PRONÓSTICO (Leonardo · Historias de un Mundo Nuevo)
AZUL = {"BLG"}
g = "pronostico_"
e0, e1 = ESC("pronostico")
k0, k1 = g + "0", g + "1"
FX += [J("hlbl_j1", e0, e1, 75.0, 1.0), velo(e0, e1, .45),
       com(W(k0, "Leonardo"), "UgyWEuykwUukrpEuYdF4AaABAg", T1(k0) - W(k0, "Leonardo") + .3, y=.4, tam=1000),
       tar(W(k0, "Tres"), T1(k0) + .3, "Pronóstico de Leonardo", "3 a 2 para Bilibili", A, logo="BLG", dato="3-2", x=.5, y=.86, tam=52),
       com(W(k1, "Historias"), "Ugxqy7pCRCgtLjewPOZ4AaABAg", e1 - W(k1, "Historias"), y=.42, tam=1000),
       tar(W(k1, "Ahi"), e1, "¡Ahí estás!", None, "oro", x=.5, y=.82, tam=64)]

# ================================================================== CIERRE (agradecimientos · suscripción · la pregunta)
AZUL = {"GEN"}
g = "cierre_"
e0, e1 = ESC("cierre")
k0, k1, k2 = (g + str(i) for i in range(3))
b2 = T0(k2)
gq = W(k2, "Bilibili")
FX += [J("hlbl_j1", e0, b2, 75.0 + (ESC("pronostico")[1] - ESC("pronostico")[0]), 1.0), velo(e0, b2, .45),
       *FZ("r_ig3fin", b2, gq, 101.0, 1.1), *FZ("r_dk3fin", gq, e1, 55.0, 1.1), velo(b2, e1, .3),
       tar(e0 + .1, W(k0, "tierrarara"), "Gracias a todos los que comentan", "Todos se leen", "oro", x=.5, y=.15, tam=56),
       com(W(k0, "tierrarara"), "UgxAagc7tHDylIeRH2h4AaABAg", T1(k0) - W(k0, "tierrarara") + .5, x=.3, y=.3, tam=760),
       com(W(k0, "Mike"), "Ugx35zdqW7ygvSQPfR54AaABAg", T1(k0) - W(k0, "Mike") + .5, x=.7, y=.5, tam=760),
       com(W(k0, "Paco"), "UgwVGfaBbE-In9afzcR4AaABAg", T1(k0) - W(k0, "Paco") + .5, x=.3, y=.72, tam=760),
       tar(T0(k1), T1(k1) + .3, "Suscríbete y activa la campanita", "El resumen de la final, con las jugadas analizadas", "oro", x=.5, y=.5, tam=70),
       vs(b2, e1, "GEN", "BLG", "¿Quién gana el sábado?", "Y con qué marcador: déjalo en los comentarios", y=.42),
       tar(W(k2, "Nos"), e1, "Nos vemos después de la final", None, "oro", x=.5, y=.88, tam=56)]

# ---------------------------------------------------------------- control: nada al revés ni de duración nula
_mal = []
for _f in FX[_i0:]:
    if "de" in _f and _f["a"] - _f["de"] < .05:
        _mal.append(_f)
    elif "en" in _f and "dur" in _f and _f["dur"] < .05:
        _mal.append(_f)
for _f in _mal:
    print(f"  AVISO fx_escenas: «{_f.get('nombre', _f.get('tipo'))}» sin duración ({_f.get('de', _f.get('en')):.2f}): se quita")
    FX.remove(_f)
