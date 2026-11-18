# -*- coding: utf-8 -*-
"""Montaje de las escenas SIN jugada de t1_blg_caida (gancho, serie, doran, oro15, dragones, g4_ctx, faker, veredicto, cierre; las
jugadas g4a, g1, g2, g3, g4 y las nuevas están en fx_jugadas.py). Lo ejecuta efectos.py con exec (FX, AZUL, K y los helpers).
Fondo = VOD real del partido que se nombra (x1, pausa o congelado con zoom), fondo() animado bajo los gráficos de datos.
Datos: investigacion/stats_g*.json, oro_12x.json (feed oficial), feed_12x.txt. Helpers copiados de lol_final_previa/fx_escenas.py."""
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

K.update({"j6_fin": 2249.0, "j6_baron": 1719.0})
F_ORO = dict(desfase=5)          # reloj del feed − HUD (≈ 5 s en las cuatro partidas; previa)


def grande(de, a, titulo, sub=None, color="oro", y=.5, tam=96, **kw):
    """rótulo grande al centro (capítulo / dato)"""
    return tar(de, a, titulo, sub, color, x=.5, y=y, tam=tam, **kw)


# ================================================================== GANCHO (la caída · el acusado · el menú)
AZUL = {"T1"}
g = "gancho_"
e0, e1 = ESC("gancho")
k0, k1, k2, k3 = (g + str(i) for i in range(4))
b1, b2, b3 = T0(k1), T0(k2), T0(k3)
nx = W(k0, "cae")
ts = 16.0 - (nx - e0)                      # j6_fin: el nexo estalla (t ≈ 16,0) cuando la voz dice «cae»
FX += [J("j6_fin", e0, b1, max(0.0, ts), 1.0),
       mg(L.apertura("LA VERDADERA RAZÓN", "Por qué cayó T1 · semifinal Worlds 2026"), e0, W(k0, "Semifinal"), x=.5, y=.5, nombre="apertura"),
       dict(tipo="destello", en=.15, fuerza=.7),
       tar(W(k0, "Semifinal"), W(k0, "campeon"), "Domingo 8 de noviembre", "Semifinal del Mundial · partida 4", "oro", x=.26, y=.17, tam=46),
       tar(W(k0, "campeon"), nx, "T1", "Campeón de 2023, 2024 y 2025", A, logo="T1", dato="3", x=.26, y=.17, tam=46),
       vs(nx, b1 + .2, "BLG", "T1", "Bilibili 3 - 1 T1", "Semifinal · Worlds 2026", ganador=0, y=.42),
       dict(tipo="destello", en=nx, fuerza=.5)]
# «culpa a una sola persona: Doran» → j6 congelado en t 83 (32:23, Bin mata a Doran) con acercamiento
FX += [*FZ("j6", b1, b2, 83.2, 1.18, .45, .5), velo(b1, b2, .35),
       tar(b1 + .1, W(k1, "Doran"), "Desde ese día", "Casi todos culpan a uno", R, logo="T1", x=.5, y=.15, tam=48),
       peg(W(k1, "Doran"), "Doran", "Doran", R, "T1", "Top · T1", dur=b2 - W(k1, "Doran") + .2, x=.5, y=.5, tam=520, gris=True,
           sello=("¿CULPABLE?", 0), marcas=[W(k1, "Doran") + .9]),
       dict(tipo="destello", en=W(k1, "Doran"), fuerza=.35)]
# «Revisé las cuatro partidas, pausa por pausa» → rebobina y la G3 corre (j5 libre t 14-30)
FX += [*REB("j6", b2, 83.2, 77.0), J("j5", b2 + 1.2, b3, 14.0, 1.0),
       tar(W(k2, "cuatro"), W(k2, "Doran"), "4 partidas", "Pausa por pausa", "oro", x=.5, y=.84, tam=52),
       tar(W(k2, "Doran"), W(k2, "algo"), "Doran tiene parte de culpa", "Sí, la tiene", R, logo="T1", x=.5, y=.84, tam=52),
       tar(W(k2, "algo"), b3 + .2, "Algo que se repite en las 4", "Y casi nadie lo está mirando", "oro", x=.5, y=.84, tam=52)]
FX += [J("j6", b3, e1, 2.0, 1.0), velo(b3, e1, .55),
       mg(L.menu([(CARGA("Vayne"), "El acusado", "rojo"), (CARGA("Orianna"), "Dato 1: el arranque", "amarillo"),
                  (CARGA("Skarner"), "Dato 2: el río", "azul"), (CARGA("Taliyah"), "La pelea en 3D", "oro")]),
          b3 + .1, e1, [W(k3, "acusacion"), W(k3, "dos"), W(k3, "decidieron"), W(k3, "pelea")], y=.52, nombre="menu")]

# ================================================================== LA SERIE (marcador de las 4 partidas, feed_122..125)
g = "serie_"
e0, e1 = ESC("serie")
k0, k1 = g + "0", g + "1"
p1, p2, p3, p4 = W(k0, "Partida"), W(k0, "Partida", 1), W(k1, "Partida"), W(k1, "cuarta")
FX += [*FZ("r_t1g1", e0, p2, 30.0, 1.1), *FZ("j4", p2, p3, 125.0, 1.1), *FZ("j5", p3, p4, 84.0, 1.1), J("j6_fin", p4, e1, 16.2, 1.0),
       velo(e0, e1, .5),
       mg(L.resultados("Semifinal · Bilibili vs T1", [(EQ("BLG"), "Bilibili 18", EQ("T1"), "6 T1", 0),
                                                       (EQ("BLG"), "Bilibili 10", EQ("T1"), "22 T1", 1),
                                                       (EQ("BLG"), "Bilibili 19", EQ("T1"), "10 T1", 0),
                                                       (EQ("BLG"), "Bilibili 21", EQ("T1"), "9 T1", 0)]),
          e0 + .1, W(k1, "final") - .1, [p1, p2, p3, p4], y=.5, nombre="resultados serie"),
       tar(W(k0, "empata"), p3, "Serie 1 - 1", "T1 empata", A, logo="T1", x=.5, y=.9, tam=40),
       elim(W(k1, "final"), e1 + .2, "T1", "T1", "Bilibili a la final · T1 a casa", [W(k1, "casa")])]

# ================================================================== EL ACUSADO: DORAN (muertes del feed; oro vs Bin al minuto 20)
g = "doran_"
e0, e1 = ESC("doran")
k0, k1, k2 = (g + str(i) for i in range(3))
b1, b2 = T0(k1), T0(k2)
FX += [*FZ("j6", e0, b1, 83.6, 1.12, .45, .5), velo(e0, b1, .5),
       pv(W(k0, "Doran"), "Doran", "Doran · top de T1", dur=W(k0, "veintidos") - W(k0, "Doran") + .2, x=.5, y=.48, tam=560),
       mg(L.ranking("Muertes en la serie", [(EQ("T1"), "Doran", "22", "Top · T1", R), (EQ("T1"), "Oner", "16", "Jungla · T1", R),
                                              (EQ("BLG"), "ON", "12", "Apoyo · Bilibili · el que más murió de BLG", A)]),
          W(k0, "veintidos") - .1, b1 + .2, [W(k0, "veintidos"), W(k0, "Oner"), W(k0, "ON")], y=.5, nombre="ranking muertes")]
FX += [fondo(b1, b2, ["T1", "BLG"], "fondo doran oro"),
       tar(b1 + .1, W(k1, "mil"), "Perdió su línea en las 4", "Oro de Doran contra Bin · minuto 20", R, logo="T1", x=.5, y=.15, tam=50),
       mg(L.ranking("Bin le saca oro a Doran · minuto 20", [(ICON("Rumble"), "Partida 1 · Rumble", "+1,2K", "Bin arriba en oro", R),
                                                             (ICON("Olaf"), "Partida 2 · Olaf", "+0,6K", "Bin arriba en oro", R),
                                                             (ICON("Ambessa"), "Partida 3 · Ambessa", "+1,8K", "Bin arriba en oro", R),
                                                             (ICON("Vayne"), "Partida 4 · Vayne", "+1,5K", "Bin arriba en oro", R)]),
          W(k1, "mil") - .2, b2 + .2, [W(k1, "mil"), W(k1, "seiscientos"), W(k1, "mil", 1), W(k1, "mil", 2)], y=.55, nombre="ranking oro doran"),
       cam(W(k1, "Bin"), "Bin", "Bin · top de Bilibili", dur=b2 - W(k1, "Bin"), x=.92, y=.2, tam=200)]
FX += [J("j6", b2, e1, 2.0 + (b2 - b1), 1.0), velo(b2, e1, .5),
       abanico(W(k2, "Rumble") - .1, e1 + .2, [(CARGA("Rumble"), "Rumble"), (CARGA("Olaf"), "Olaf"), (CARGA("Ambessa"), "Ambessa"),
                                               (CARGA("Vayne"), "Vayne")],
               [W(k2, "Rumble"), W(k2, "Olaf"), W(k2, "Ambessa"), W(k2, "Vayne")], y=.47, tam=330, nombre="abanico Doran"),
       tar(W(k2, "ninguno"), e1 + .2, "Con ninguno pudo con Bin", "4 campeones · 4 líneas perdidas", R, logo="T1", x=.5, y=.88, tam=46)]

# ================================================================== PRIMER DATO: oro de T1 al minuto 15 (oro_12x.json)
g = "oro15_"
e0, e1 = ESC("oro15")
k0, k1, k2 = (g + str(i) for i in range(3))
b1, b2 = T0(k1), T0(k2)
FX += [J("j5", e0, b1, 14.0 + (ESC("gancho")[1] - T0("gancho_2")), 1.0), velo(e0, b1, .5),
       grande(W(k0, "primer") - .1, b1 + .2, "PRIMER DATO", "Lo que casi nadie menciona", "oro", tam=110)]
FX += [fondo(b1, b2, ["BLG", "T1"], "fondo oro15"),
       mg(L.ranking("Oro al minuto 15", [(EQ("BLG"), "Partida 1", "+0,4K", "Bilibili arriba", A), (EQ("BLG"), "Partida 2", "+2,1K", "Bilibili arriba · y la ganó T1", A),
                                         (EQ("BLG"), "Partida 3", "+0,7K", "Bilibili arriba", A), (EQ("BLG"), "Partida 4", "+2,8K", "Bilibili arriba", A)]),
          b1 + .1, b2 + .2, [W(k1, "Cuatrocientos"), W(k1, "dos"), W(k1, "Setecientos"), W(k1, "ochocientos")], y=.53, nombre="ranking oro15"),
       tar(b1 + .1, W(k1, "Cuatrocientos"), "Minuto 15", "En las 4 partidas", "oro", x=.5, y=.12, tam=48)]
FX += [J("j4", b2, e1, 16.0, 1.0), velo(b2, e1, .3),
       oro(b2 + .1, e1, "123", 0, 1900, [600, 1033, 1900], [W(k2, "tambien"), W(k2, "ganó"), W(k2, "remontando")], "T1", "BLG",
           notas=[(1033, "Bilibili +2,7K")], titulo="Partida 2 · la que ganó T1", x=.5, y=.45, escala=.95, **F_ORO),
       tar(W(k2, "ni"), e1, "0 de 4 arranques", "La única que ganó, la ganó remontando", R, logo="T1", dato="0/4", x=.5, y=.88, tam=44)]

# ================================================================== SEGUNDO DATO: más dragones = ganó las 4 (stats_g*.json)
g = "dragones_"
e0, e1 = ESC("dragones")
k0, k1, k2 = (g + str(i) for i in range(3))
b1, b2 = T0(k1), T0(k2)
FX += [J("j5", e0, b1, 60.0, 1.0), velo(e0, b1, .5),
       grande(e0 + .1, W(k0, "equipo") - .1, "SEGUNDO DATO", "El que decide la serie", "oro", tam=110),
       grande(W(k0, "equipo"), b1 + .2, "Más dragones = ganó", "Las 4 partidas", "oro", tam=96)]
FX += [fondo(b1, b2, ["T1", "BLG"], "fondo dragones"),
       mg(L.duelo((EQ("T1"), "T1", EQ("T1"), "rojo", "Dragones"), (EQ("BLG"), "Bilibili", EQ("BLG"), "azul", "Dragones"),
                  "Dragones por partida", [("Partida 1", "1", "3", .25, .75, 1), ("Partida 2 · alma + ancestral", "4", "0", 1.0, .02, 0),
                                           ("Partida 3 · alma infernal", "2", "4", .5, 1.0, 1), ("Partida 4 · alma de montaña", "2", "4", .5, 1.0, 1)]),
          b1 + .1, b2 + .2, [W(k1, "Partida"), W(k1, "Partida", 1), W(k1, "Partida", 2), W(k1, "Partida", 3)], y=.5, nombre="duelo dragones")]
FX += [J("j4b", b2, e1, 2.0, 1.0), velo(b2, e1, .35),
       grande(W(k2, "Cuatro"), W(k2, "unica"), "4 de 4", "El que gana el río, gana la partida", "oro", dato="4/4", tam=90),
       tar(W(k2, "unica"), e1 + .2, "Partida 2: el río fue de T1", "Y la ganó 22 a 10", A, logo="T1", x=.5, y=.86, tam=46)]

# ================================================================== G4: EL CONTEXTO (feed_125; j6_baron = repetición de la pelea del 28 y el Barón)
AZUL = {"T1"}
g = "g4_ctx_"
e0, e1 = ESC("g4_ctx")
k0, k1, k2 = (g + str(i) for i in range(3))
b1, b2 = T0(k1), T0(k2)
FX += [*FZ("j6", e0, b1, 2.0, 1.1), velo(e0, b1, .5),
       oro(e0 + .3, b1, "125", 0, 1100, [600, 1065], [W(k0, "dieciocho"), W(k0, "cinco")], "T1", "BLG", notas=[(1065, "Bilibili +4,7K")],
           titulo="Partida 4 · diferencia de oro", x=.5, y=.5, escala=.95, **F_ORO),
       tar(W(k0, "diez"), b1 + .2, "Bilibili 10 - 3", "Minuto 18 · partida de la eliminación", R, logo="BLG", x=.5, y=.12, tam=46)]
_bx = min(W(k2, "Baron") - .3, b1 + 41.0)
FX += [J("j6_baron", b1, _bx, 0.0, 1.0), J("j6_baron", _bx, e1, 41.0, 1.0),
       tar(b1 + .1, W(k1, "Faker"), "Repetición · minuto 28", "La pelea que lo cambió todo", A, logo="T1", x=.5, y=.84, tam=44),
       cam(W(k1, "Faker"), "Faker", "Faker · 2 asesinatos", dur=b2 - W(k1, "Faker"), x=.08, y=.3, tam=200),
       cam(W(k1, "Doran"), "Doran", "Doran · 2 asesinatos", dur=b2 - W(k1, "Doran"), x=.08, y=.58, tam=200),
       tar(W(k1, "cinco"), b2 + .2, "5 por 2 para T1", "28:02 - 28:27", A, logo="T1", dato="5-2", x=.5, y=.84, tam=44),
       tar(W(k2, "Baron"), W(k2, "cuatrocientos"), "Barón para T1", "29:20", A, logo="T1", x=.76, y=.17, tam=40),
       oro(W(k2, "diferencia"), e1, "125", 1600, 1940, [1680, 1936], [W(k2, "diferencia"), W(k2, "cuatrocientos")], "T1", "BLG",
           notas=[(1936, "Bilibili +0,4K")], titulo="Partida 4 · se acerca", x=.24, y=.3, escala=.6, **F_ORO)]

# ================================================================== ¿Y FAKER? (stats finales: 14/5/21; Viper 23, Knight 18)
AZUL = {"T1"}
g = "faker_"
e0, e1 = ESC("faker")
k0 = g + "0"
FX += [*FZ("j4b", e0, e1, 46.7, 1.14), velo(e0, e1, .55),
       mg(L.premio("La serie de Faker", JUG("Faker"), "Faker", EQ("T1"), ["14 asesinatos · 5 muertes · 21 asistencias", "0 muertes en la partida 2",
                                                                         "El que más mató de T1"], color="azul", sub="Medio · T1",
                   sello="NO FUE ÉL"),
          e0 + .2, e1 + .2, [W(k0, "Catorce"), W(k0, "Ninguna"), W(k0, "problema") - .4, W(k0, "problema")], y=.5, nombre="premio Faker")]

# ================================================================== LOS RIVALES (Knight 18 · 8/0 en la G1; Viper 23)
AZUL = {"BLG"}
g = "rivales_"
e0, e1 = ESC("rivales")
k1 = g + "0"
FX += [J("r_t1g1", e0, e1, 0.0, 1.0), velo(e0, e1, .5),
       mg(L.ranking("Asesinatos en la serie", [(EQ("BLG"), "Viper", "23", "Tirador · Bilibili", A), (EQ("BLG"), "Knight", "18", "Medio · Bilibili", A),
                                                (EQ("T1"), "Faker", "14", "Medio · T1", R)]),
          e0 + .1, e1 + .2, [W(k1, "Knight"), W(k1, "Viper"), W(k1, "Viper") + .8], y=.5, nombre="ranking asesinatos"),
       cam(W(k1, "Knight"), "Knight", "Knight · medio", dur=2.8, x=.1, y=.25, tam=200)]

# ================================================================== VEREDICTO
g = "veredicto_"
e0, e1 = ESC("veredicto")
k0, k1, k2 = (g + str(i) for i in range(3))
b1, b2 = T0(k1), T0(k2)
FX += [J("j6", e0, b1, 30.0, 1.0), velo(e0, b1, .55),
       grande(e0 + .1, W(k0, "Doran"), "EL VEREDICTO", "¿Cuál es la verdadera razón?", "oro", tam=110),
       mg(L.ranking("Lo que perdió T1", [(EQ("T1"), "La línea de Doran", "4 de 4", "Bin arriba al minuto 20", R),
                                         (EQ("T1"), "El arranque", "4 de 4", "Bilibili arriba al minuto 15", R),
                                         (EQ("T1"), "El río", "3 de 4", "Más dragones = ganó la partida", R)]),
          W(k0, "Doran") - .1, b1 + .2, [W(k0, "Doran"), W(k0, "arranques"), W(k0, "rio")], y=.5, nombre="ranking veredicto")]
FX += [*FZ("j6", b1, b2, 83.2, 1.15, .5, .45), velo(b1, b2, .45),
       tar(W(k1, "Cuando"), W(k1, "no"), "Dueño de los dragones", "Ganó 22 a 10", A, logo="T1", x=.5, y=.15, tam=48),
       tar(W(k1, "no"), W(k1, "ultima"), "Sin el río", "Bilibili le ganó las otras 3", R, logo="BLG", x=.5, y=.15, tam=48),
       tar(W(k1, "ultima"), b2 + .2, "Partida 4", "Pelea por una torre con el Barón a 2 segundos", R, logo="T1", x=.5, y=.15, tam=48)]
FX += [J("j6_fin", b2, e1, 16.2, 1.0), velo(b2, e1, .45),
       grande(W(k2, "jugador") - .2, W(k2, "nunca"), "No cayó por un jugador", None, "oro", tam=96),
       grande(W(k2, "nunca"), e1 + .2, "Cayó por el arranque y el río", "Bilibili fue mejor en los dos", "oro", tam=84)]

# ================================================================== CIERRE (fichajes · la pregunta · suscripción)
g = "cierre_"
e0, e1 = ESC("cierre")
k0, k1 = g + "0", g + "1"
b1 = T0(k1)
FX += [J("j6_fin", e0, e1, 25.0, .72), velo(e0, e1, .5),   # festejo de BLG 25-42 s a x0,72 (el VOD dura 42 s; r_escenario es de GEN-IG), 17-nov
       tar(e0 + .1, b1 + .2, "Mercado de fichajes", "El video con todos los movimientos, en el canal", "oro", logo="T1", x=.5, y=.5, tam=70),
       mg(L.versus((JUG("Doran"), "Doran"), (EQ("BLG"), "El río"), "¿Culpa de quién?", "Déjalo en los comentarios: todos se leen"),
          b1, W(k1, "suscribete"), [], y=.45, nombre="versus pregunta"),
       tar(W(k1, "suscribete"), e1 + .2, "Suscríbete", "Para el próximo análisis pausa por pausa", "oro", x=.5, y=.5, tam=80)]

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
