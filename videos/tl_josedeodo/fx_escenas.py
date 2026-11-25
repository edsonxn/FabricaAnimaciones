# -*- coding: utf-8 -*-
"""Montaje de las escenas SIN jugada de tl_josedeodo (camino, gracias, acusacion, drafts, criticas, dragones, duelo, numeros, veredicto,
futuro, cierre; las jugadas gancho, blg, al1, cfo, mejor, los2, los3 están en fx_jugadas.py). Lo ejecuta efectos.py con exec (FX, AZUL, K y los helpers).
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


for _k, _v in {"lotl_j1": 2063, "lotl_j2": 2364.5, "lotl_j3": 2289, "lotl_g1": 723, "lotl_g2": 2158, "lotl_zest": 2767,
               "cfo_j1": 2000}.items():
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



def grande(de, a, titulo, sub=None, color="oro", y=.5, tam=96, **kw):
    """rótulo grande al centro (capítulo / dato)"""
    return tar(de, a, titulo, sub, color, x=.5, y=y, tam=tam, **kw)



def CAM(c):
    """nombre legible del campeón"""
    return {"LeeSin": "Lee Sin", "JarvanIV": "Jarvan IV", "XinZhao": "Xin Zhao"}.get(c, c)


# ================================================================== EL CAMINO (stats de las 7 partidas)
AZUL = {"TLAW"}
g = "camino_"
e0, e1 = ESC("camino")
k0, k1 = g + "0", g + "1"
b1 = T0(k1)
FX += [J("cfo_j1", e0, b1, 0.0, 1.0), J("lotl_g1", b1, e1, 0.0, 1.0), velo(e0, e1, .55),
       mg(L.resultados("El Mundial de Team Liquid", [(EQ("TLAW"), "Liquid 11", EQ("CFO"), "12 CTBC", 1),
                                                      (EQ("TLAW"), "Liquid 2", EQ("BLG"), "17 Bilibili", 1),
                                                      (EQ("TLAW"), "Liquid 2", EQ("AL"), "0 Anyone's Legend", 0),
                                                      (EQ("TLAW"), "Liquid 1", EQ("LOS"), "2 Los Grandes", 1)]),
          e0 + .1, W(k1, "Siete") - .1, [W(k0, "primera"), W(k0, "segunda"), W(k1, "elimina"), W(k1, "cae")], y=.5,
          nombre="resultados camino"),
       tar(W(k1, "campeon"), W(k1, "serie"), "Anyone's Legend", "Campeón de China · eliminado 2 a 0", "oro", logo="AL", x=.5, y=.9, tam=40),
       grande(W(k1, "Siete"), e1 + .2, "7 partidas · 3 - 4", "Tres victorias y cuatro derrotas", "oro", tam=96)]

# ================================================================== GRACIAS (comentarios reales ≤ 10 días) + la justa de gasYotube
g = "gracias_"
e0, e1 = ESC("gracias")
k0, k1 = g + "0", g + "1"
b1 = T0(k1)
FX += [fondo(e0, e1, ["TLAW"], "fondo gracias"),
       tar(e0 + .1, W(k0, "Daniel") - .1, "Gracias", "Lo que nos escribieron", "oro", x=.5, y=.15, tam=56),
       com(W(k0, "Daniel"), "UgyfsqiFpG-ocppdEmN4AaABAg", W(k0, "Argonauta") - W(k0, "Daniel"), y=.45),
       com(W(k0, "Argonauta"), "Ugxm0BexIA_d7ty1HF54AaABAg", W(k0, "Fede") - W(k0, "Argonauta"), x=.5, y=.3, tam=900),
       com(W(k0, "Rei"), "UgwKD0JApPpOgDfT78B4AaABAg", W(k0, "Fede") - W(k0, "Rei"), x=.5, y=.66, tam=900),
       com(W(k0, "Fede"), "UgzWl9poevS3JGJCtC94AaABAg", b1 - W(k0, "Fede"), y=.45),
       com(W(k1, "Gas"), "Ugw8yWeW4gGL5RV9cGd4AaABAg", W(k1, "razon") - W(k1, "Gas"), y=.42),
       tar(W(k1, "razon"), W(k1, "Por"), "El río es del jungla", "Gas tenía razón en algo", "oro", x=.5, y=.5, tam=70),
       pv(W(k1, "Por"), "Josedeodo", "Josedeodo · jungla de Team Liquid", dur=e1 - W(k1, "Por") + .2, x=.5, y=.5, tam=560)]

# ================================================================== LA ACUSACIÓN (Spawn · el draft contra BLG)
g = "acusacion_"
e0, e1 = ESC("acusacion")
k0, k1, k2 = (g + str(i) for i in range(3))
b1, b2 = T0(k1), T0(k2)
FX += [fondo(e0, b1, ["TLAW"], "fondo spawn"),
       tar(W(k0, "Spawn"), W(k0, "dijo"), "Spawn", "Entrenador de Team Liquid", A, logo="TLAW", x=.5, y=.3, tam=72),
       grande(W(k0, "dijo"), b1 + .2, "«Nada de lo que hacemos está funcionando»", "Spawn · tras quedar fuera del Mundial", "oro", y=.55,
              tam=64)]
FX += [fondo(b1, e1, ["TLAW", "BLG"], "fondo acusacion"),
       tar(b1 + .1, W(k1, "Lee"), "Partida 2 · contra Bilibili", "Liquid tiene la primera selección", A, logo="TLAW", x=.5, y=.15, tam=50),
       peg(W(k1, "Lee"), CARGA("LeeSin"), "Lee Sin", "oro", None, "Libre · el favorito de Josedeodo", dur=b2 - W(k1, "Lee") + .1,
           x=.5, y=.52, tam=480),
       peg(W(k2, "Ezreal"), CARGA("Ezreal"), "Ezreal", A, "TLAW", "1.ª selección de Liquid", dur=e1 - W(k2, "Ezreal") + .2, x=.3, y=.52,
           tam=420),
       peg(W(k2, "Lee"), CARGA("LeeSin"), "Lee Sin", R, "BLG", "1.ª selección de Bilibili · Xun", dur=e1 - W(k2, "Lee") + .2, x=.7, y=.52,
           tam=420, marcas=[W(k2, "Xun")]),
       dict(tipo="destello", en=W(k2, "Lee"), fuerza=.35)]

# ================================================================== LOS SIETE DRAFTS (Leaguepedia, comprobados con el feed)
g = "drafts_"
e0, e1 = ESC("drafts")
k0, k1, k2 = (g + str(i) for i in range(3))
b1, b2 = T0(k1), T0(k2)
FX += [J("lotl_g2", e0, b1, 0.0, 1.0), velo(e0, b1, .5),
       grande(e0 + .1, W(k0, "dato"), "LOS 7 DRAFTS", "Revisé los otros seis", "oro", tam=110),
       grande(W(k0, "dato"), b1 + .2, "Y el dato no cuadra", None, R, tam=96)]
FX += [fondo(b1, e1, ["TLAW"], "fondo drafts"),
       mg(L.ranking("Jungla con la PRIMERA selección", [(ICON("LeeSin"), "Lee Sin · contra CTBC", "DERROTA", "Josedeodo 3/4/7", R),
                                                         (ICON("LeeSin"), "Lee Sin · contra Anyone's Legend", "VICTORIA", "Josedeodo 3/0/8", A),
                                                         (ICON("Nocturne"), "Nocturne · contra Los Grandes", "DERROTA", "Josedeodo 3/3/2", R)]),
          b1 + .1, b2 + .2, [W(k1, "dos"), W(k1, "Nocturne"), W(k1, "Resultado")], y=.5, nombre="ranking draft 1"),
       tar(W(k1, "Resultado"), b2, "1 victoria · 2 derrotas", None, R, logo="TLAW", dato="1-2", x=.5, y=.88, tam=46),
       mg(L.ranking("Jungla en la SEGUNDA ronda del draft", [(ICON("Pantheon"), "Pantheon · contra Anyone's Legend", "VICTORIA", "Josedeodo 4/5/7", A),
                                                             (ICON("XinZhao"), "Xin Zhao · contra Los Grandes", "VICTORIA", "Josedeodo 5/1/10", A),
                                                             (ICON("Sejuani"), "Sejuani · contra Los Grandes", "DERROTA", "Josedeodo 1/3/5", R)]),
          b2 + .1, e1 + .2, [W(k2, "tres"), W(k2, "turnos"), W(k2, "Resultado")], y=.5, nombre="ranking draft 2"),
       tar(W(k2, "Resultado"), e1 + .2, "2 victorias · 1 derrota", None, A, logo="TLAW", dato="2-1", x=.5, y=.88, tam=46)]

# ================================================================== CRÍTICAS (con burla) Y JUSTAS
g = "criticas_"
e0, e1 = ESC("criticas")
k0, k1, k2 = (g + str(i) for i in range(3))
b1, b2 = T0(k1), T0(k2)
FX += [fondo(e0, e1, ["TLAW", "LOS"], "fondo criticas"),
       tar(e0 + .1, W(k0, "Shadow") - .1, "Pausa", "Los comentarios", "oro", x=.5, y=.5, tam=90),
       com(W(k0, "Shadow"), "UgyRkfTi4B-tmyRUv2x4AaABAg", W(k0, "tranquilo") - W(k0, "Shadow"), y=.42),
       tar(W(k0, "tranquilo"), b1 + .2, "Hoy no defiendo a nadie", "7 partidas · si sale culpable, sale culpable", "oro", x=.5, y=.5, tam=64),
       com(W(k1, "Luis"), "UgyjsR8HwH1-pqeCJDx4AaABAg", W(k1, "Luis", 1) - W(k1, "Luis"), y=.42),
       tar(W(k1, "Luis", 1), b2 + .2, "Este no llega tarde", "Las partidas ya se jugaron · los números no cambian", "oro", x=.5, y=.5, tam=64),
       com(W(k2, "Jorge"), "UgylfoAksU65kLRLMiZ4AaABAg", W(k2, "Hecho") - W(k2, "Jorge"), y=.42),
       tar(W(k2, "Hecho"), W(k2, "Mister"), "Hecho", "Hoy el acusado es el coach", "oro", x=.5, y=.5, tam=70),
       com(W(k2, "Mister"), "UgysFDPHvpklcAUidy54AaABAg", e1 - W(k2, "Mister") + .2, y=.42)]

# ================================================================== DRAGONES: 7 de 7 (stats)
g = "dragones_"
e0, e1 = ESC("dragones")
k0, k1, k2 = (g + str(i) for i in range(3))
b1, b2 = T0(k1), T0(k2)
FX += [J("lotl_j2", e0, b1, 17.0, 1.0), velo(e0, b1, .5),
       grande(W(k0, "Esto") - .1, b1 + .2, "Más dragones = ganó", "Las 7 partidas de Liquid", "oro", dato="7/7", tam=96)]
FX += [fondo(b1, b2, ["TLAW"], "fondo dragones"),
       mg(L.ranking("Dragones · Liquid contra sus rivales", [(EQ("TLAW"), "En las 3 victorias", "13 - 5", "Liquid se llevó más dragones", A),
                                                              (EQ("TLAW"), "En las 4 derrotas", "5 - 16", "El rival se llevó más dragones", R)]),
          b1 + .1, b2 + .2, [W(k1, "victorias"), W(k1, "derrotas")], y=.5, nombre="ranking dragones")]
FX += [J("lotl_j2", b2, e1, 21.0, 1.0), velo(b2, e1, .35),
       tar(W(k2, "rio"), e1 + .2, "El río es del jungla", "Y aquí viene el segundo 7 de 7", "oro", x=.5, y=.86, tam=50)]

# ================================================================== DUELO DE JUNGLAS · minuto 15 (oro15.py, feed)
g = "duelo_"
e0, e1 = ESC("duelo")
k0, k1, k2, k3 = (g + str(i) for i in range(4))
b1, b2, b3 = T0(k1), T0(k2), T0(k3)
FX += [fondo(e0, b3, ["TLAW"], "fondo duelo"),
       tar(e0 + .1, b1 + .2, "Josedeodo contra el jungla rival", "Oro al minuto 15 · las 7 partidas", "oro", logo="TLAW", x=.5, y=.5, tam=64),
       mg(L.ranking("En las 3 VICTORIAS · minuto 15", [(JUG("Tarzan"), "Contra Tarzan · partida 1", "+754", "Josedeodo arriba", A),
                                                       (JUG("Tarzan"), "Contra Tarzan · partida 2", "+958", "Josedeodo arriba", A),
                                                       (JUG("Curse"), "Contra Curse · partida 2", "+951", "Josedeodo arriba", A)]),
          b1 + .1, b2 + .2, [W(k1, "setecientos"), W(k1, "novecientos"), W(k1, "mil")], y=.5, nombre="ranking duelo v"),
       mg(L.ranking("En las 4 DERROTAS · minuto 15", [(JUG("Shad0w"), "Contra Shad0w · CTBC", "-1 119", "Josedeodo abajo", R),
                                                      (JUG("Xun"), "Contra Xun · Bilibili", "-174", "Josedeodo abajo", R),
                                                      (JUG("Curse"), "Contra Curse · partida 1", "-742", "Josedeodo abajo", R),
                                                      (JUG("Curse"), "Contra Curse · partida 3", "-952", "Josedeodo abajo", R)]),
          b2 + .1, b3 + .2, [W(k2, "mil"), W(k2, "ciento"), W(k2, "setecientos"), W(k2, "novecientos")], y=.52, nombre="ranking duelo d")]
FX += [J("lotl_j1", b3, e1, 0.0, 1.0), velo(b3, e1, .5),
       grande(b3 + .1, W(k3, "Siete"), "Ganó su duelo: Liquid ganó", "Lo perdió: Liquid perdió", "oro", tam=80),
       grande(W(k3, "Siete"), e1 + .2, "7 de 7", "La partida que lo decidió todo", "oro", dato="7/7", tam=110)]

# ================================================================== LOS NÚMEROS DE JOSEDEODO (stats)
g = "numeros_"
e0, e1 = ESC("numeros")
k0, k1 = g + "0", g + "1"
FX += [J("lotl_g2", e0, e1, 0.0, 1.0), velo(e0, e1, .55),
       mg(L.premio("Josedeodo en el Mundial", JUG("Josedeodo"), "Josedeodo", EQ("TLAW"),
                   ["19 asesinatos · 20 muertes · 41 asistencias", "Victorias: 12 asesinatos · 6 muertes",
                    "Derrotas: 7 asesinatos · 14 muertes"], color="azul", sub="Jungla · Team Liquid · 7 partidas"),
          e0 + .1, e1 + .2, [W(k0, "diecinueve"), W(k1, "victorias"), W(k1, "derrotas")], y=.5, nombre="premio Josedeodo")]

# ================================================================== VEREDICTO
g = "veredicto_"
e0, e1 = ESC("veredicto")
k0, k1, k2 = (g + str(i) for i in range(3))
b1, b2 = T0(k1), T0(k2)
FX += [J("lotl_j1", e0, b1, 60.0, 1.0), velo(e0, b1, .55),
       grande(e0 + .1, W(k0, "Del"), "EL VEREDICTO", "¿Culpa de quién?", "oro", tam=110),
       tar(W(k0, "Del"), b1 + .2, "¿Del coach? En un draft, sí", "Contra Bilibili: el Lee Sin para el rival", R, logo="TLAW", x=.5, y=.5,
           tam=64)]
FX += [J("lotl_g2", b1, b2, 4.0, 1.0), velo(b1, b2, .5),
       peg(W(k1, "mejor"), CARGA("XinZhao"), "Xin Zhao", A, "TLAW", "Su mejor partida · pick de 2.ª ronda · 5/1/10",
           dur=b2 - W(k1, "mejor") + .2, x=.5, y=.5, tam=480)]
FX += [J("lotl_j1", b2, e1, 30.0, 1.0), velo(b2, e1, .45),
       grande(b2 + .1, W(k2, "termometro"), "Ni culpable ni víctima", None, "oro", tam=96),
       peg(W(k2, "termometro"), "Josedeodo", "EL TERMÓMETRO", A, "TLAW", "Liquid llegó hasta donde llegó su jungla",
           dur=e1 - W(k2, "termometro") + .2, x=.5, y=.5, tam=520)]

# ================================================================== 2027
g = "futuro_"
e0, e1 = ESC("futuro")
k0 = g + "0"
FX += [fondo(e0, e1, ["TLAW", "C9"], "fondo futuro"),
       gris(W(k0, "CoreJJ"), "CoreJJ", "C9", "Se va a Cloud9", .14, a=e1 + .2),
       gris(W(k0, "Yeon"), "Yeon", "C9", "Se va a Cloud9", .32, a=e1 + .2),
       pv(W(k0, "Josedeodo"), "Josedeodo", "Se queda · contrato para 2027", dur=e1 - W(k0, "Josedeodo") + .2, x=.7, y=.47, tam=520),
       grande(W(k0, "proyecto"), e1 + .2, "El proyecto ahora es suyo", None, "oro", y=.86, tam=64)]

# ================================================================== CIERRE (la pregunta · suscripción)
g = "cierre_"
e0, e1 = ESC("cierre")
k0, k1 = g + "0", g + "1"
b1 = T0(k1)
FX += [J("lotl_zest", e0, e1, 0.0, .8), velo(e0, e1, .5),
       mg(L.menu([(JUG("Josedeodo"), "¿Josedeodo?", "azul"), (EQ("TLAW"), "¿El coach?", "rojo"), (CARGA("Taliyah"), "¿El río?", "oro")]),
          e0 + .1, b1 + .2, [W(k0, "coach"), W(k0, "Josedeodo"), W(k0, "rio")], y=.47, nombre="menu pregunta"),
       tar(W(k0, "comentarios"), b1 + .2, "Déjalo en los comentarios", "Todos se leen", "oro", x=.5, y=.88, tam=46),
       tar(W(k1, "suscribete"), e1 + .2, "Suscríbete", "Para el próximo análisis pausa por pausa", "oro", x=.5, y=.5, tam=80)]

# ================================================================== ¿QUIÉN ES JOSEDEODO? (Leaguepedia, Upcomer, Sheep Esports)
AZUL = {"TLAW"}
g = "quien_"
e0, e1 = ESC("quien")
k0, k1 = g + "0", g + "1"
b1 = T0(k1)
FX += [J("al_j2", e0, e1, 0.0, 1.0), velo(e0, e1, .55),
       sil(e0 + .1, "Josedeodo", "Josedeodo", "Brandon Villegas · Argentina", dur=W(k0, "Empezo") - e0, lado="izq"),
       mg(L.calendario("El camino de Josedeodo", [("2018", "Liga\nlatinoamericana", "oro"), ("Rainbow7", "México", "oro"),
                                                   ("2021", "FlyQuest\nEstados Unidos", "azul"), ("Estral", "Vuelve a\nLatinoamérica", "oro"),
                                                   ("2026", "Team Liquid\nMundial", "azul")]),
          W(k0, "Empezo") - .1, W(k1, "Ese") - .1, [W(k0, "liga"), W(k0, "Rainbow7"), W(k0, "FlyQuest"), W(k1, "Volvio"), W(k1, "Team")],
          y=.5, nombre="calendario Josedeodo"),
       tar(W(k1, "Ese"), W(k1, "Llego", 1), "Equipo ideal de la LCS", "Primavera 2026 · primer equipo", A, logo="TLAW", x=.5, y=.5, tam=70),
       grande(W(k1, "Llego", 1), e1 + .2, "Uno de los mejores junglas", "De su región · al Mundial 2026", "oro", y=.5, tam=80)]

# ================================================================== EL RIVAL: Curse (BR) y Ackerman (AR) en la serie a muerte (stats LOS G1-G3)
AZUL = {"TLAW"}
g = "rival_"
e0, e1 = ESC("rival")
k0, k1 = g + "0", g + "1"
b1 = T0(k1)
FX += [fondo(e0, e1, ["TLAW", "LOS"], "fondo rival"),
       vs(e0 + .1, W(k0, "Curse"), "TLAW", "LOS", "Liquid vs Los Grandes", "La serie a muerte · al mejor de 3"),
       pv(W(k0, "Curse"), "Curse", "Curse · jungla · Brasil", dur=b1 - W(k0, "Curse") + .1, x=.72, y=.5, tam=470),
       pv(W(k0, "Argentina"), "Josedeodo", "Josedeodo · jungla · Argentina", dur=b1 - W(k0, "Argentina") + .1, x=.28, y=.5, tam=470),
       tar(W(k0, "duelo"), W(k0, "Ackerman"), "Un duelo latino", "Argentina contra Brasil", "oro", x=.5, y=.88, tam=48),
       cam(W(k0, "Ackerman"), "Ackerman", "Ackerman · soporte · Argentina", dur=b1 - W(k0, "Ackerman") + .1, x=.5, y=.2, tam=200),
       mg(L.duelo((JUG("Josedeodo"), "Josedeodo", EQ("TLAW"), A, "Argentina"), (JUG("Curse"), "Curse", EQ("LOS"), R, "Brasil"),
                  "La serie a muerte · 3 partidas", [("Asesinatos", "9", "11", 9 / 11, 1.0, 1), ("Muertes", "7", "5", 1.0, 5 / 7, 1),
                                                     ("Asistencias", "17", "18", 17 / 18, 1.0, 1)]),
          b1 + .1, e1 + .2, [W(k1, "once"), W(k1, "cinco"), W(k1, "nueve")], y=.5, nombre="duelo Josedeodo-Curse")]

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
