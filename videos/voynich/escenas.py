# -*- coding: utf-8 -*-
"""El libro que nadie puede leer (manuscrito Voynich) — v3: calco del estilo de "Detrás del Enigma".

(ARCHIVO GENERADO por _armar.py a partir de partes3/p1..p4: edita las partes.)
Todo se dibuja en función del tiempo global (`Mundo`). Cada toma se declara con `shot(t0, fondo, textos, extras, ent, grado)`; el fin de una toma es
el inicio de la siguiente. Los tiempos salen de la voz (`w_(escena, frase, índice_de_palabra)`), así que nada queda desincronizado.

Lenguaje visual copiado del original (analizado cuadro a cuadro):
  * Texto principal: cursiva blanca en mayúsculas (Poppins SemiBold Italic), 2 líneas centradas, palabra a palabra con fundido, líneas de
    escaneo a través de las letras (`R`).   * Nombres y cifras: serif amarillo condensado, Título Con Mayúsculas (`S`), cifras rojas (`N`).
  * Preguntas: serif blanco + signo '?' rojo (`Q`).   * Trazos rojos rectos que se dibujan y se borran (`trazo_recto`), líneas de medida punteadas.
  * Filtro de película en TODO el cuadro (`X.cine`): tilt-shift, aberración cromática, bloom, viñeta, grano y escaneo.
  * Transiciones: fundido, mancha de tinta, fuga de luz de color, destello.
Poco texto y pequeño: solo donde el original lo pondría.
"""
import json
import math
import os
import types

import cv2
import numpy as np

from escena_base import *  # noqa: F401,F403
from motor import H, W, e_back, e_in, e_inout, e_out, lerp, prog, smooth, clamp01
import docu as D  # después del *: escena_base también exporta un `D` (dibujos)
import docu_fx as X

_ESC = {e["id"]: e for e in TL["escenas"]}
TOTAL = TL["total"]
AM, BL, RJ = D.AMARILLO, D.BLANCO, D.ROJO
I3 = np.eye(3)
AMAR = (0.95, 1.0, 0.10)


def w_(eid, fr, i):
    """Tiempo (s) en que empieza la palabra de índice i de la frase fr de la escena eid."""
    ws = _ESC[eid]["frases"][fr]["words"]
    return ws[min(i, len(ws) - 1)]["s"]


def INI(eid, i=0):
    return _ESC[eid]["frases"][i]["t0"]


def FIN(eid, i=-1):
    return _ESC[eid]["frases"][i]["t1"]


def pal_(eid, fr, i0, i1):
    """[(texto, t)] de las palabras [i0:i1] de la frase (sin puntuación)."""
    ws = _ESC[eid]["frases"][fr]["words"][i0:i1]
    return [(w["w"].strip(".,;:¿?¡!…\"()"), w["s"]) for w in ws]


# ------------------------------------------------------------------ caché de sprites (una copia por proceso)
_C = {}


def spr(clave, fn):
    if clave not in _C:
        _C[clave] = fn()
    return _C[clave]


def HD(nombre):
    return os.path.abspath(f"imagenes/folios_hd/{nombre}.jpg")


def folio(n, alto=1000):
    return spr(("f", n, alto), lambda: D.hoja_papel(D.cargar(D.ruta_img(f"f{n:03d}"), 2200), alto))


def pola(nombre, ancho=440, asp=1.05, foco=(0.5, 0.5), leyenda=None, lado=1600):
    return spr(("p", nombre, ancho, asp, foco, leyenda), lambda: D.polaroid(D.cargar(D.ruta_img(nombre), lado), ancho, asp, foco, leyenda=leyenda))


def corcho():
    return spr("corcho", lambda: D.Sprite(D.tablero(), None, sombra=False))


def recorte(nombre):
    return spr(("rec", nombre), lambda: X.recorte_borde(f"imagenes/recortes/{nombre}.png"))


def fondo_borroso(nombre, brillo=0.30, tinte=(1.0, 0.9, 0.78)):
    def mk():
        im = D.cargar(D.ruta_img(nombre), 700)
        h, w = im.shape[:2]
        k = max(480 / w, 270 / h)
        r = cv2.resize(im, (int(w * k) + 1, int(h * k) + 1), interpolation=cv2.INTER_AREA)
        y0, x0 = (r.shape[0] - 270) // 2, (r.shape[1] - 480) // 2
        r = cv2.GaussianBlur(r[y0:y0 + 270, x0:x0 + 480].astype(np.float32) / 255.0, (0, 0), 14)
        return np.clip(cv2.resize(r, (W, H), interpolation=cv2.INTER_CUBIC) * np.float32(tinte) * brillo, 0, 1).astype(np.float32)
    return spr(("fb", nombre, brillo), mk)


ZIPF = json.load(open("datos/zipf.json"))
PALABRAS_VOY = [w for w in open("datos/takahashi_clean.txt", encoding="utf-8", errors="ignore").read().replace("*", " ").split() if w.isalpha()][:6000]
C0 = (1700, 1000)


def carta(lz, sp, M, t, t_in, x, y, rot=0.0, s=1.0, desde=(0, -420), dur=0.5, flota=1.0, fase=0.0, op=1.0, ry0=50.0):
    if t < t_in:
        return
    u = e_out(prog(t, t_in, t_in + dur))
    e = t - t_in
    asent = math.exp(-(e - dur) * 3.2) * math.sin((e - dur) * 15.0) * 2.0 if e > dur else 0.0
    fl = flota * 4.0 * math.sin(0.9 * t + fase)
    Mm = M @ D.poner(sp.w, sp.h, lerp(x + desde[0], x, u), lerp(y + desde[1], y, u) + fl, lerp(1.3, 1.0, u) * s, rot + asent + (1 - u) * 12, (1 - u) * ry0)
    D.pegar(lz, sp, Mm, op * smooth(prog(t, t_in, t_in + 0.15)))


# ------------------------------------------------------------------ texto (estilos del original)
def R(palabras, cx=W / 2, cy=H * 0.56, px=88, lineas=None, sal=None):
    """Texto principal: cursiva blanca en mayúsculas con líneas de escaneo, palabra a palabra."""
    pal = X.rotulo(palabras, cx, cy, px, lineas)

    def f(lz, t):
        X.dibujar_rotulo(lz, pal, t, px, salida=sal)
    f.golpes = []
    return f


def S(palabras, cx=W / 2, cy=H * 0.55, px=98, lineas=None, sal=None):
    """Serif amarillo condensado, Título Con Mayúsculas (nombres, lugares, cifras)."""
    pal = X.serif_amarillo(palabras, cx, cy, px, lineas)

    def f(lz, t):
        X.dibujar_serif(lz, pal, t, px, salida=sal)
    f.golpes = []
    return f


def N(txt, cx, cy, px, t0, color=RJ, sal=None):
    """Cifra grande en serif condensado (roja como el '150' del original, o amarilla)."""
    def f(lz, t):
        D.numero(lz, txt, cx, cy, px, t, t0, color=color, fnt="abril_cond", salida=sal, pop=False)
    f.golpes = []
    return f


def Q(lineas, t0, cx=W / 2, cy=H * 0.60, px=88, sal=None):
    """Pregunta: serif blanco + signo '?' rojo."""
    def f(lz, t):
        X.pregunta_c(lz, lineas, t, t0, cx, cy, px, salida=sal)
    f.golpes = []
    return f


# ------------------------------------------------------------------ fondos
def F_clip(nombre, **kw):
    def f(lz, tl, t, dur, ext):
        X.clip_bg(lz, nombre, tl, dur, z_extra=ext, **kw)
    return f


def F_foto(nombre, **kw):
    def f(lz, tl, t, dur, ext):
        D.foto_parallax(lz, nombre, tl, dur, z_extra=ext, **kw)
    return f


def F_borroso(nombre, brillo=0.30):
    def f(lz, tl, t, dur, ext):
        lz[:] = fondo_borroso(nombre, brillo)
    return f


def F_pozo(cx=0.5, cy=0.45, r=0.8, color=(0.24, 0.18, 0.11)):
    def f(lz, tl, t, dur, ext):
        lz[:] = D.pozo_luz(cx, cy, r, color)
    return f


def F_negro():
    def f(lz, tl, t, dur, ext):
        lz[:] = 0
    return f


def HERO(nombre, x=960, y=500, rot=0.0, alto=880, t_in=0.0, ry=(-10, -3), desde=(0, 0), dur=0.55):
    """Folio grande con cámara propia."""
    def f(lz, t):
        sp = folio(nombre, alto)
        u = e_out(prog(t, t_in, t_in + dur))
        cam = D.Cam((1.0, W / 2, H / 2, 0.0), (1.08, W / 2, H / 2 + 10, 0.0), 3.0, mano=0.8)(t - t_in)
        D.pegar(lz, sp, cam @ D.poner(sp.w, sp.h, lerp(x + desde[0], x, u), lerp(y + desde[1], y, u), lerp(0.9, 1.0, u), lerp(rot + 5, rot, u), lerp(ry[0], ry[1], u)), smooth(prog(t, t_in, t_in + 0.2)))
    return f


# ================================================================== tomas
SHOTS = []
SND = []          # (t, nombre, vol, kw): efectos de sonido registrados por las tomas


def snd(t, nombre, vol=0.5, **kw):
    SND.append((t, nombre, vol, kw))


SFX_TRANS = {"tinta": ("whoosh", 0.5), "destello": ("brillo", 0.4), "fuga": ("zoom_whoosh", 0.45), "aberracion": ("whoosh", 0.4), "glitch": ("glitch", 0.4),
             "corte": ("tick", 0.35), "fundido": None, "desenfoque": None, "negro": ("impacto", 0.5), "zoom": ("zoom_whoosh", 0.45)}


def shot(t0, fondo, textos=(), extras=(), ent=("fundido", 0.5), grado=None, nombre=""):
    SHOTS.append(dict(t0=t0, fondo=fondo, textos=list(textos), extras=list(extras), ent=ent, grado=grado or {}, nombre=nombre))


def _construir():
    SHOTS.sort(key=lambda d: d["t0"])
    for k, d in enumerate(SHOTS):
        d["t1"] = SHOTS[k + 1]["t0"] if k + 1 < len(SHOTS) else TOTAL + 1.0
        d["golpes"] = []
        sfx = SFX_TRANS.get(d["ent"][0])
        if sfx and k > 0:
            snd(d["t0"] - 0.04, sfx[0], sfx[1], **({"dur": 0.6} if sfx[0] in ("whoosh", "zoom_whoosh") else {}))


def _dibujar(d, lz, t):
    tl = t - d["t0"]
    dur = d["t1"] - d["t0"] + 0.5
    d["fondo"](lz, tl, t, dur, 1.0)
    for e in d["extras"]:
        e(lz, t)
    for tx in d["textos"]:
        tx(lz, t)


# ---------------------------------------------------------------- GANCHO (0 - 17.5)
G = "gancho"
shot(0.0, F_clip("vela", inicio=4.0, z0=1.0, z1=1.22, tono=(1.0, 0.92, 0.82)), [], ent=("fundido", 0.01))
shot(1.10, F_clip("pluma", inicio=1.5, z0=1.05, z1=1.22, c0=(0.4, 0.55), c1=(0.6, 0.5), tono=(0.85, 0.75, 0.65)), [], ent=("fuga", 0.7))


def _cover(lz, t):
    sp = folio(1, 900)
    tl = t - 2.35
    ry = lerp(-24, -9, e_out(prog(t, 2.35, 3.9))) + 2 * math.sin(0.6 * t)
    cam = D.Cam((1.0, W / 2, H / 2, 0.0), (1.08, W / 2 + 30, H / 2 - 6, 0.0), 3.0, mano=0.5)(tl)
    Mlib = cam @ D.poner(sp.w, sp.h, 560, 540, 1.0, -3 + 1.2 * math.sin(0.4 * t), ry, 2)
    D.pegar(lz, sp, Mlib, smooth(prog(t, 2.35, 3.0)))
    c = [D.tf(Mlib, x, y) for x, y in ((28, 20), (sp.w - 28, 20), (sp.w - 28, sp.h - 20), (28, sp.h - 20), (28, 20))]
    D.linea_punteada(lz, c, e_inout(prog(t, 2.4, 3.8)), op=1.0 - smooth(prog(t, 3.6, 4.6)))


shot(2.35, F_borroso("f001", 0.34), [R(pal_(G, 0, 4, 11), 1310, 500, 88, lineas=(4,))], [_cover], ent=("fundido", 0.6))

shot(5.12, F_clip("paginas1", inicio=1.0, z0=1.05, z1=1.2, tono=(0.75, 0.68, 0.6)), [],
     [lambda lz, t: X.linea_medida(lz, (300, 640), (1640, 610), e_out(prog(t, w_(G, 1, 1), w_(G, 1, 3) + 0.5)), "240 páginas", t, w_(G, 1, 3), 84)], ent=("tinta", 0.7))


def _polaroids_plantas(lz, t):
    cam = D.Cam((1.0, C0[0], C0[1], 0.5), (1.12, C0[0] + 30, C0[1], -1.0), 3.0, mano=0.7)(t - 6.55)
    D.pegar(lz, corcho(), cam @ D.poner(3400, 2000, C0[0], C0[1]))
    cx, cy = C0
    cartas = (("f004", -420, -120, -7, w_(G, 1, 4) - 0.05), ("f024", 0, 60, 3, w_(G, 1, 4) + 0.35), ("f110", 420, -100, -4, w_(G, 1, 5) + 0.05))
    pts = []
    for k, (nom, dx, dy, r, ti) in enumerate(cartas):
        carta(lz, pola(nom, 400, 1.12, (0.5, 0.42)), cam, t, ti, cx + dx, cy + dy, r, desde=(-400 + 300 * k, -420), fase=k * 1.7)
        if t > ti + 0.25:
            pts.append((cx + dx, cy + dy - 240))
        snd(ti, "papel", 0.45)
    for a, b in zip(pts[:-1], pts[1:]):
        D.hilo(lz, cam, a, b, smooth(prog(t, w_(G, 1, 5), w_(G, 1, 5) + 0.5)))
    for p in pts:
        D.pin(lz, cam, *p)


shot(6.55, F_negro(), [], [_polaroids_plantas], ent=("fundido", 0.5))


def _trazos_glifos(lz, t):
    # dos trazos rojos rectos sobre líneas de texto (se dibujan y se borran) — las 'líneas rectas' del original
    tt = t - 8.55
    for k, (y, x0, x1) in enumerate(((452, 260, 1560), (596, 300, 1500))):
        u1 = e_out(prog(tt, 0.35 * k, 0.35 * k + 1.0))
        u0 = e_inout(prog(tt, 1.8 + 0.3 * k, 2.6 + 0.3 * k))
        X.trazo_recto(lz, (x0, y), (x1, y + 6), u0, u1, 24)


shot(8.20, F_foto("folios_hd/f187", z0=1.5, z1=1.85, c0=(0.30, 0.25), c1=(0.6, 0.55), par=(0, 0), lado=3800, tono=(0.85, 0.84, 0.8)),
     [R(pal_(G, 1, 7, 16), W / 2, 820, 84, lineas=(3,))], [_trazos_glifos], ent=("fuga", 0.7))
shot(11.35, F_pozo(0.5, 0.45, 0.85, (0.22, 0.17, 0.10)), [],
     [lambda lz, t: carta(lz, pola("alberti", 560, 1.0, (0.5, 0.5), "Disco de cifrado"), I3, t, 11.6, 620, 470, -4, desde=(-700, 0), dur=0.55),
      lambda lz, t: carta(lz, pola("purple", 560, 1.0, (0.5, 0.42), "Máquina militar"), I3, t, 12.9, 1300, 470, 3, desde=(700, 0), dur=0.55)], ent=("tinta", 0.6))
shot(13.68, F_clip("codigo2", z0=1.0, z1=1.15, tono=(1.0, 0.72, 0.32), sat=0.0), [],
     [lambda lz, t: D.panel_analisis(lz, PALABRAS_VOY, t, 13.85, 960, 800, 900, 260, dur=1.4)], ent=("fundido", 0.4))
shot(15.30, F_foto("folios_hd/f190", z0=1.5, z1=1.85, c0=(0.4, 0.3), c1=(0.6, 0.5), par=(0, 0), lado=3800, tono=(0.5, 0.48, 0.45)),
     [R(pal_(G, 2, 9, 13), W / 2, 330, 90, lineas=(2,))],
     [lambda lz, t: D.estampa(lz, "SIN DESCIFRAR", 960, 800, t, 16.55, 120, rot=-6)], ent=("fuga", 0.7))

# ---------------------------------------------------------------- ORIGEN (17.5 - 32.5)
O = "origen"
shot(17.50, F_clip("reloj_bolsillo", inicio=3, z0=1.05, z1=1.22, tono=(0.9, 0.78, 0.65)),
     [R(pal_(O, 0, 0, 4), W / 2, 820, 74, lineas=(2,))], ent=("tinta", 0.7))
shot(19.75, F_foto("mondragone_grabado", z0=1.1, z1=1.28, c0=(0.42, 0.5), c1=(0.55, 0.48), par=(60, 8), tono=(0.35, 0.29, 0.23)),
     [R([("Es", w_(O, 0, 3)), ("1912", w_(O, 0, 6))], W / 2, H * 0.5, 120)], ent=("fundido", 0.7))
shot(22.00, F_clip("biblioteca", inicio=1, z0=1.05, z1=1.2, tono=(0.9, 0.78, 0.62), sat=0.6), [], ent=("fundido", 0.7))


def _voynich(lz, t):
    sp = recorte("voynich_retrato")
    u = e_out(prog(t, 23.5, 24.2))
    cam = D.Cam((1.0, W / 2, H / 2, 0.0), (1.10, W / 2 - 20, H / 2, 0.0), 3.5, mano=0.5)(t - 23.5)
    D.pegar(lz, sp, cam @ D.poner(sp.w, sp.h, lerp(1900, 1380, u), 560, 1.0, lerp(10, -2, u)), smooth(prog(t, 23.5, 23.8)))
    D.tag_nombre(lz, "Wilfrid Voynich", 1330, 940, t, w_(O, 1, 5), 50)


shot(23.50, F_borroso("f003", 0.32), [R(pal_(O, 1, 0, 5), 520, 500, 74, lineas=(3,))], [_voynich], ent=("fuga", 0.7))


def _mapa(lz, t):
    """Polaroid de mapa (como la de Cahuachi): cae desde arriba, se asienta con marcadores amarillo-verde y línea de distancia."""
    t0 = w_(O, 1, 14) - 0.1
    if t < t0:
        return
    sp = spr("mapa", lambda: D.polaroid(X.hoja_mapa(marcas=[("Roma", 1392, 1543), ("Frascati", 1601, 1679)]), 700, 0.76, (0.5, 0.5), sombra=True))
    u = e_out(prog(t, t0, t0 + 0.9))
    y = lerp(-500, 470, u)
    rot = lerp(-14, -3, u) + 1.2 * math.sin(1.2 * t)
    o = smooth(prog(t, t0, t0 + 0.2)) * (1 - smooth(prog(t, 28.35, 28.75)))
    D.pegar(lz, sp, D.poner(sp.w, sp.h, 1400, y, lerp(1.1, 1.0, u), rot), o)
    D.tag_nombre(lz, "≈ 20 km", 1400, 820, t, t0 + 0.9, 42)


shot(26.00, F_foto("mondragone_grabado", z0=1.02, z1=1.18, c0=(0.5, 0.52), c1=(0.6, 0.44), par=(70, 6), tono=(0.8, 0.76, 0.68)),
     [S([("Villa", 26.05), ("Mondragone", 26.3)], 620, 230, 100, lineas=(1,), sal=28.5)], [_mapa], ent=("tinta", 0.6))
shot(28.60, F_clip("vela2", inicio=2, z0=1.05, z1=1.25, tono=(1.0, 0.85, 0.7)),
     [S([("Manuscrito", w_(O, 2, 3) + 0.1), ("Voynich", w_(O, 2, 6))], 1150, 500, 128, lineas=(1,))],
     [lambda lz, t: carta(lz, folio(3, 820), I3, t, 28.7, 520, 520, -3, desde=(-800, 0), dur=0.6),
      lambda lz, t: D.pegar(lz, X.sello_circular("Beinecke MS 408", "MS 408", "Yale University"), D.poner(420, 420, 1560, 800, 0.5, -12), 0.9 * smooth(prog(t, 30.9, 31.2)))], ent=("fundido", 0.7))


# ---------------------------------------------------------------- CONTENIDO (32.5 - 50)
C = "contenido"
shot(32.55, F_borroso("f004", 0.30), [],
     [HERO(4, 620, 500, -4, t_in=32.6, desde=(-900, 0), alto=850), HERO(24, 1300, 500, 3, t_in=33.55, desde=(900, 0), alto=850)], ent=("tinta", 0.7))
shot(34.00, F_clip("microscopio2", z0=1.05, z1=1.25, c0=(0.6, 0.5), c1=(0.7, 0.5), tono=(0.62, 0.52, 0.42), sat=0.35),
     [R(pal_(C, 0, 4, 11), W / 2, 780, 84, lineas=(3,))], ent=("fundido", 0.5))
shot(35.45, F_borroso("f110", 0.30), [R(pal_(C, 0, 4, 11), W / 2, 780, 84, lineas=(3,), sal=37.6)],
     [HERO(110, 640, 470, 2, t_in=35.5, desde=(0, -600), alto=860),
      lambda lz, t: D.estampa(lz, "SIN IDENTIFICAR", 1330, 500, t, w_(C, 0, 10) - 0.05, 90, rot=-8)], ent=("fundido", 0.4))
shot(37.85, F_borroso("f125", 0.30), [R(pal_(C, 1, 0, 3), W / 2, 960, 84, sal=39.1)],
     [HERO(125, 960, 470, -5, t_in=37.9, alto=860), lambda lz, t: X.elipse_luz(lz, 960, 470, 300, 300, prog(t, 38.4, 39.1), grosor=5)], ent=("fuga", 0.7))
shot(39.15, F_borroso("f141", 0.30), [R(pal_(C, 1, 3, 8), W / 2, 930, 78, lineas=(3,))],
     [HERO(141, 960, 460, 4, t_in=39.2, ry=(12, 4), desde=(900, 0), alto=850)], ent=("fundido", 0.5))

PAGS = (187, 190, 176, 175, 161, 153, 148, 144)


def _montaje(lz, t):
    k = int((t - 41.45) / 0.30) % len(PAGS)
    sp = folio(PAGS[k], 900)
    Mm = D.poner(sp.w, sp.h, 960 + 30 * math.sin(k * 2.1), 480, 1.0 + 0.05 * ((t - 41.45) % 0.30) / 0.30, (k % 5 - 2) * 2.0, (k % 3 - 1) * 6)
    D.pegar(lz, sp, Mm, 1.0)


shot(41.45, F_borroso("f190", 0.28), [], [_montaje], ent=("zoom", 0.3))


def _trazos2(lz, t):
    tt = t - 43.7
    for k, (y, x0, x1) in enumerate(((330, 260, 1500), (610, 300, 1560))):
        u1 = e_out(prog(tt, 0.45 * k, 0.45 * k + 1.1))
        u0 = e_inout(prog(tt, 1.6 + 0.3 * k, 2.4 + 0.3 * k))
        X.trazo_recto(lz, (x0, y), (x1, y + 4), u0, u1, 22)


shot(43.30, F_foto("folios_hd/f187", z0=1.7, z1=2.1, c0=(0.3, 0.3), c1=(0.6, 0.55), par=(0, 0), lado=3800, tono=(0.72, 0.7, 0.66)),
     [R(pal_(C, 1, 13, 16), W / 2, 850, 88)], [_trazos2], ent=("fuga", 0.7))
shot(45.40, F_foto("escriba", z0=1.02, z1=1.2, c0=(0.5, 0.5), c1=(0.56, 0.45), par=(60, 12), tono=(0.72, 0.66, 0.58)),
     [Q([[("Nadie", w_(C, 2, 0)), ("sabe", w_(C, 2, 1))], [("quién", w_(C, 2, 2)), ("lo", w_(C, 2, 3)), ("escribió", w_(C, 2, 4))]], w_(C, 2, 2) - 0.1, 1350, 580, 84, sal=47.1)],
     ent=("tinta", 0.6))
shot(47.20, F_clip("escribir", inicio=2, z0=1.05, z1=1.25, c0=(0.55, 0.5), c1=(0.7, 0.5), tono=(0.9, 0.8, 0.7)),
     [Q([[("Ni", w_(C, 2, 5)), ("por", w_(C, 2, 6)), ("qué", w_(C, 2, 7))]], w_(C, 2, 5) - 0.1, 960, 560, 92)], ent=("fundido", 0.5))

# ---------------------------------------------------------------- FECHA (50 - 67.5)
Fh = "fecha"
shot(50.05, F_clip("reloj_oscuro", inicio=1, z0=1.05, z1=1.22, tono=(0.9, 0.8, 0.7)),
     [S([("2009", w_(Fh, 0, 3) - 0.1)], 960, 520, 230)], ent=("tinta", 0.7))
shot(51.75, F_clip("microscopio", z0=1.05, z1=1.2, c0=(0.55, 0.5), c1=(0.6, 0.5), tono=(0.62, 0.52, 0.42), sat=0.35),
     [S([("Universidad", w_(Fh, 0, 5)), ("De", w_(Fh, 0, 6)), ("Arizona", w_(Fh, 0, 7))], 960, 860, 96)], ent=("fundido", 0.6))


def _muestras(lz, t):
    for k, (nom, ley) in enumerate((("f017", "folio 8"), ("f051", "folio 26"), ("f093", "folio 47"), ("f123", "folio 68"))):
        carta(lz, pola(nom, 400, 1.25, (0.5, 0.45), ley), I3, t, 54.22 + 0.3 * k, 330 + k * 420, 450 + (k % 2) * 60, (-4, 3, -2, 5)[k], desde=(0, -700), dur=0.5, fase=k)
        snd(54.22 + 0.3 * k, "obturador", 0.35)


shot(54.20, F_pozo(0.5, 0.5, 0.9, (0.20, 0.16, 0.10)),
     [S([("Carbono", w_(Fh, 0, 12)), ("14", w_(Fh, 0, 13))], 960, 920, 104)], [_muestras], ent=("fundido", 0.6))
shot(55.95, F_clip("pagina_cerca", inicio=5, z0=1.05, z1=1.18, tono=(0.30, 0.28, 0.26)),
     [N("1404", 640, 250, 210, w_(Fh, 1, 5) - 0.05), N("1438", 1280, 250, 210, w_(Fh, 1, 11) - 0.05)],
     [lambda lz, t: D.linea_tiempo(lz, t, 57.3, W / 2, 620, 1300, 1500, 1404, 1438, dur=max(0.8, w_(Fh, 1, 11) - 58.3), marcas=[(1455, "Biblia de Gutenberg")], etiqueta="Fecha del pergamino · carbono 14")], ent=("fuga", 0.7))
shot(61.45, F_foto("folios_hd/f001", z0=1.4, z1=1.75, c0=(0.6, 0.6), c1=(0.4, 0.3), par=(0, 0), lado=3800, tono=(0.7, 0.65, 0.55)),
     [R([("pergamino", w_(Fh, 2, 1)), ("medieval", w_(Fh, 2, 3))], W / 2, 500, 100)], ent=("fundido", 0.6))
shot(63.75, F_foto("f008", z0=1.35, z1=1.55, c0=(0.5, 0.35), c1=(0.5, 0.5), par=(0, 0), lado=2600, tono=(0.45, 0.43, 0.4)),
     [R(pal_(Fh, 2, 4, 9), W / 2, 480, 88, lineas=(3,))],
     [lambda lz, t: X.trazo_recto(lz, (420, 560), (1500, 560), 0.0, e_out(prog(t, w_(Fh, 2, 8) + 0.05, w_(Fh, 2, 8) + 0.5)), 16)], ent=("fundido", 0.6))


# ---------------------------------------------------------------- DUEÑOS (67.5 - 77.5)
Dn = "duenos"
shot(67.50, F_foto("escriba2", z0=1.02, z1=1.22, c0=(0.5, 0.5), c1=(0.45, 0.42), par=(50, 10), tono=(0.5, 0.45, 0.4)),
     [R(pal_(Dn, 0, 0, 7), W / 2, 520, 92, lineas=(4,), sal=w_(Dn, 0, 6) + 0.4)], ent=("tinta", 0.7), grado=dict(polvo=0.4))
shot(70.28, F_clip("carta", inicio=3, z0=1.05, z1=1.25, c0=(0.5, 0.5), c1=(0.6, 0.55), tono=(0.85, 0.78, 0.68)),
     [R(pal_(Dn, 1, 0, 5), 900, 250, 88, lineas=(3,))],
     [lambda lz, t: carta(lz, X.estampilla("kircher", "1665", 300), I3, t, 70.9, 1560, 700, 6, desde=(500, 300), dur=0.55),
      lambda lz, t: D.tag_nombre(lz, "Carta a Athanasius Kircher", 1470, 920, t, 71.4, 40)], ent=("fuga", 0.7))
shot(72.85, F_foto("rodolfo_arcimboldo", z0=1.02, z1=1.2, c0=(0.5, 0.42), c1=(0.5, 0.36), par=(80, 10), tono=(0.9, 0.86, 0.8)),
     [S([("Rodolfo", w_(Dn, 1, 9)), ("II", w_(Dn, 1, 10))], 560, 700, 130, lineas=(1,))],
     [lambda lz, t: D.tag_nombre(lz, "El emperador", 500, 300, t, w_(Dn, 1, 8), 52)], ent=("fundido", 0.6))
shot(74.60, F_clip("monedas", inicio=2, z0=1.05, z1=1.25, c0=(0.5, 0.5), c1=(0.6, 0.5), tono=(0.75, 0.7, 0.65)),
     [N("600", 540, 380, 340, w_(Dn, 1, 14) - 0.05), S([("Ducados", w_(Dn, 1, 15)), ("De", w_(Dn, 1, 16)), ("Oro", w_(Dn, 1, 17))], 960, 900, 100)], ent=("fundido", 0.6))

# ---------------------------------------------------------------- INTENTOS (77.5 - 100)
It = "intentos"
shot(77.50, F_clip("maquina", inicio=1, z0=1.05, z1=1.25, tono=(0.75, 0.75, 0.7), sat=0.6),
     [R(pal_(It, 0, 0, 5), W / 2, 820, 80, lineas=(3,))], ent=("tinta", 0.7))
shot(79.05, F_foto("friedman", z0=1.05, z1=1.25, c0=(0.32, 0.42), c1=(0.34, 0.36), par=(80, 18), tono=(0.9, 0.9, 0.9)),
     [S([("William", w_(It, 0, 5)), ("Friedman", w_(It, 0, 6))], 1420, 300, 104, lineas=(1,))],
     [lambda lz, t: D.tag_nombre(lz, "Criptógrafo", 560, 860, t, w_(It, 0, 8), 48)], ent=("fundido", 0.6), grado=dict(sat=0.7))
shot(81.22, F_pozo(0.5, 0.45, 0.85, (0.26, 0.10, 0.28)),
     [R(pal_(It, 0, 11, 15), W / 2, 880, 84, lineas=(2,))],
     [lambda lz, t: carta(lz, pola("purple", 640, 1.0, (0.5, 0.42), "Máquina Púrpura"), I3, t, 81.3, 960, 400, 3, desde=(0, -700), dur=0.55)], ent=("fuga", 0.7))
shot(82.90, F_clip("reloj_bolsillo", inicio=6, z0=1.05, z1=1.25, tono=(0.85, 0.75, 0.65)),
     [R(pal_(It, 0, 15, 18), W / 2, 500, 96, lineas=(1,))], ent=("fundido", 0.6))


def _equis(lz, t):
    t0 = w_(It, 1, 2) + 0.1
    for k, (a, b) in enumerate((((700, 250), (1220, 760)), ((1220, 250), (700, 760)))):
        X.trazo_recto(lz, a, b, 0.0, e_out(prog(t, t0 + 0.25 * k, t0 + 0.25 * k + 0.5)), 26)


shot(84.98, F_borroso("f190", 0.28), [R(pal_(It, 1, 0, 3), W / 2, 900, 88)], [HERO(190, 960, 470, -3, t_in=85.0, desde=(0, 700)), _equis], ent=("fundido", 0.5))
shot(86.22, F_clip("humo", inicio=8, z0=1.05, z1=1.22, tono=(0.85, 0.85, 0.9)),
     [S([("1959", 86.4)], 700, 470, 230)],
     [lambda lz, t: D.pegar(lz, X.sello_circular("Anagrama", "1959", "Philological Quarterly"), D.poner(420, 420, 1400, 500, 1.0, -10), 0.92 * smooth(prog(t, w_(It, 1, 7), w_(It, 1, 7) + 0.2)))], ent=("fuga", 0.7))
shot(88.30, F_foto("folios_hd/f187", z0=1.6, z1=1.95, c0=(0.45, 0.4), c1=(0.6, 0.55), par=(0, 0), lado=3800, tono=(0.6, 0.58, 0.54)),
     [R(pal_(It, 1, 10, 13), W / 2, 540, 96, lineas=(1,))], ent=("fundido", 0.6))
shot(90.20, F_clip("humo", inicio=1, z0=1.05, z1=1.25, tono=(0.75, 0.8, 0.9)),
     [R(pal_(It, 2, 2, 5), W / 2, 540, 96, lineas=(1,))], ent=("fundido", 0.6), grado=dict(vineta=0.85))


def _trazos3(lz, t):
    t0 = w_(It, 2, 9) - 0.2
    for k, y in enumerate((300, 430, 560, 690)):
        u1 = e_out(prog(t, t0 + 0.22 * k, t0 + 0.22 * k + 0.7))
        X.trazo_recto(lz, (250, y), (1670, y + 4), 0.0, u1, 16, op=0.85)


shot(91.72, F_foto("folios_hd/f190", z0=1.9, z1=2.3, c0=(0.25, 0.3), c1=(0.7, 0.6), par=(0, 0), lado=3800, tono=(0.55, 0.53, 0.5)),
     [R(pal_(It, 2, 5, 12), W / 2, 880, 84, lineas=(4,))], [_trazos3], ent=("fundido", 0.6), grado=dict(vineta=0.85))
shot(94.05, F_foto("folios_hd/f187", z0=1.6, z1=1.9, c0=(0.5, 0.4), c1=(0.5, 0.5), par=(0, 0), lado=3800, tono=(0.30, 0.29, 0.27)),
     [R(pal_(It, 3, 3, 12), W / 2, 950, 62, lineas=(5,))],
     [lambda lz, t: D.grafica_zipf(lz, ZIPF, t, 94.15, W / 2, 450, 1240, 640, dur=3.6),
      lambda lz, t: X.elipse_luz(lz, 900, 520, 230, 150, prog(t, w_(It, 3, 10), w_(It, 3, 11) + 0.5), grosor=5)], ent=("fuga", 0.7))


# ---------------------------------------------------------------- TEORÍAS (100 - 112.5): tablero de evidencias
Te = "teorias"
KEYS = [(100.0, 1.0, C0[0], C0[1] - 40, 0.0), (101.5, 1.35, C0[0] - 480, C0[1] + 20, -1.0), (103.2, 1.3, C0[0], C0[1] + 90, 0.8),
        (105.4, 1.0, C0[0], C0[1] - 40, 0.0), (106.4, 1.35, C0[0] + 480, C0[1] + 10, 1.0), (108.6, 1.0, C0[0], C0[1] - 40, 0.0)]


def _cam_keys(t):
    """Cámara por claves: mantiene y se mueve con suavidad (0,9 s) entre encuadres."""
    for i in range(len(KEYS) - 1, -1, -1):
        if t >= KEYS[i][0]:
            k = KEYS[i]
            prev = KEYS[i - 1] if i > 0 else k
            u = e_inout(clamp01((t - k[0]) / 0.9))
            z, cx, cy, rot = [lerp(prev[j], k[j], u) for j in (1, 2, 3, 4)]
            z += 0.015 * (t - k[0]) / 2.0
            return D.camara(z, cx, cy, rot)
    return D.camara(1.0, KEYS[0][2], KEYS[0][3], 0.0)


def _tablero(lz, t):
    cam = _cam_keys(t)
    D.pegar(lz, corcho(), cam @ D.poner(3400, 2000, C0[0], C0[1]))
    cx, cy = C0
    ANC = 360
    ALT2 = 0.5 * ANC * (0.055 + 0.89 * 1.15 + 0.17)
    ti = (w_(Te, 0, 5) - 0.15, w_(Te, 0, 8) - 0.15, w_(Te, 1, 6) - 0.15)
    tarjetas = (("alberti", -520, 20, -5, ti[0], "Disco de cifrado"), ("f190", 0, 90, 3, ti[1], None), ("f110", 520, 10, -3, ti[2], "¿Fraude medieval?"))
    pins = []
    for k, (nom, dx, dy, r, t_in, ley) in enumerate(tarjetas):
        sp = pola(nom, ANC, 1.15, (0.5, 0.5) if nom != "f190" else (0.5, 0.35), ley)
        carta(lz, sp, cam, t, t_in, cx + dx, cy + dy, r, desde=(0, -420), fase=k * 1.3)
        if t > t_in + 0.25:
            pins.append((cx + dx, cy + dy - ALT2 + 22))
    if t > 100.1:
        q = spr("pregunta", lambda: D.Sprite(np.full((220, 360, 3), (240, 235, 220), np.uint8), None, sombra=True, sr=12))
        M = cam @ D.poner(q.w, q.h, cx, cy - 250, 1.0, 1.5)
        D.pegar(lz, q, M, smooth(prog(t, 100.1, 100.5)))
        pm, a_, m = D.palabra_img("¿Qué es?", "serif", 84, (0.72, 0.05, 0.05), stroke=0.02, glow=0.0)
        x, y = D.tf(M, q.w / 2, q.h / 2)
        D.mezclar_pm(lz, pm, a_, int(x - pm.shape[1] / 2), int(y - pm.shape[0] / 2), smooth(prog(t, 100.2, 100.6)))
    for k, p in enumerate(pins):
        D.hilo(lz, cam, (cx, cy - 350), p, smooth(prog(t, ti[k] + 0.2, ti[k] + 0.8)))
    if t > 100.1:
        D.pin(lz, cam, cx, cy - 350)
    for p in pins:
        D.pin(lz, cam, *p)
    for k, tt in enumerate((w_(Te, 2, 0), w_(Te, 2, 1), w_(Te, 2, 3))):
        dx, dy = tarjetas[k][1], tarjetas[k][2]
        x, y = D.tf(cam, cx + dx, cy + dy)
        z = float(np.sqrt(abs(np.linalg.det(cam[:2, :2]))))
        X.trazo_recto(lz, (x - ANC * 0.42 * z, y - ALT2 * 0.8 * z), (x + ANC * 0.42 * z, y + ALT2 * 0.8 * z), 0.0, e_out(prog(t, tt, tt + 0.4)), 22)
        X.trazo_recto(lz, (x + ANC * 0.42 * z, y - ALT2 * 0.8 * z), (x - ANC * 0.42 * z, y + ALT2 * 0.8 * z), 0.0, e_out(prog(t, tt + 0.15, tt + 0.55)), 22)
    D.estampa(lz, "SIN RESOLVER", W / 2, 640, t, w_(Te, 2, 6) + 0.1, 120, rot=-7)


shot(100.0, F_negro(),
     [R(pal_(Te, 0, 4, 6), W / 2, 1000, 66, sal=w_(Te, 0, 7) - 0.05), R(pal_(Te, 0, 7, 10), W / 2, 1000, 66, sal=w_(Te, 1, 5) - 0.05),
      R(pal_(Te, 1, 5, 10), W / 2, 1000, 66, sal=w_(Te, 2, 0) - 0.05), R(pal_(Te, 2, 0, 7), W / 2, 1000, 62, lineas=None)],
     [_tablero], ent=("tinta", 0.7))

# ---------------------------------------------------------------- CIERRE (112.5 - 131.25)
K = "cierre"
shot(112.50, F_clip("biblioteca", inicio=0.5, z0=1.0, z1=1.25, c0=(0.5, 0.5), c1=(0.5, 0.55), tono=(1.0, 0.9, 0.8), sat=0.7), [], ent=("tinta", 0.7))
shot(114.85, F_foto("beinecke_interior", z0=1.05, z1=1.24, c0=(0.5, 0.55), c1=(0.5, 0.42), par=(70, 14), tono=(0.95, 0.9, 0.85)), [],
     [lambda lz, t: D.tag_nombre(lz, "Biblioteca Beinecke", 470, 860, t, w_(K, 0, 6), 54)], ent=("fuga", 0.7))
shot(116.92, F_clip("paginas2", inicio=0.5, z0=1.05, z1=1.22, tono=(0.7, 0.62, 0.52)),
     [S(pal_(K, 0, 12, 15), 960, 880, 100, lineas=(1,))],
     [lambda lz, t: D.pegar(lz, X.sello_circular("Universidad", "YALE", "New Haven"), D.poner(420, 420, 1500, 430, 0.85, -10), 0.95 * smooth(prog(t, w_(K, 0, 14), w_(K, 0, 14) + 0.2))),
      lambda lz, t: carta(lz, X.estampilla("f003", "MS 408", 320), I3, t, 117.0, 380, 470, -6, desde=(-500, 0), dur=0.55)], ent=("fundido", 0.6))


def _internet(lz, t):
    tl = t - 119.15
    vent = spr("ventana", lambda: _ventana())
    cam = D.Cam((1.0, W / 2, H / 2, 0.0), (1.05, W / 2, H / 2 - 8, 0.0), 2.4, mano=0.5)(tl)
    D.pegar(lz, vent, cam @ D.poner(vent.w, vent.h, W / 2, 470, 1.0, 0.0), smooth(prog(t, 119.15, 119.5)))
    nomb = (4, 7, 10, 24, 32, 110, 111, 136, 141, 147, 175, 176)
    for k, n in enumerate(nomb):
        col, fila = k % 6, k // 6
        x = 405 + col * 222
        y = 385 + fila * 335 - 6 * math.sin(0.7 * t + k)
        sp = pola(f"f{n:03d}", 205, 1.36, (0.5, 0.45))
        D.pegar(lz, sp, cam @ D.poner(sp.w, sp.h, x, y, 1.0, (k % 3 - 1) * 1.5), smooth(prog(t, 119.4 + 0.07 * k, 119.8 + 0.07 * k)))


def _ventana():
    w, h = 1500, 760
    im = np.zeros((h, w, 3), np.uint8)
    im[:] = (26, 26, 28)
    cv2.rectangle(im, (0, 0), (w, 66), (44, 44, 48), -1)
    for k, c in enumerate(((70, 70, 220), (60, 190, 240), (80, 200, 90))):
        cv2.circle(im, (34 + k * 34, 33), 10, c[::-1], -1, cv2.LINE_AA)
    cv2.rectangle(im, (150, 14), (w - 60, 52), (20, 20, 22), -1)
    from PIL import Image, ImageDraw
    pil = Image.fromarray(im)
    ImageDraw.Draw(pil).text((176, 33), "collections.library.yale.edu", font=D.fuente("sans_l", 24), fill=(200, 200, 195), anchor="lm")
    return D.Sprite(np.asarray(pil), None, sombra=True, sr=26, off=(18, 26), sop=0.7)


shot(119.15, F_pozo(0.5, 0.5, 0.85, (0.17, 0.15, 0.13)), [], [_internet], ent=("tinta", 0.7))
shot(120.90, F_clip("proyector", inicio=4, z0=1.05, z1=1.25, c0=(0.5, 0.5), c1=(0.6, 0.5), tono=(0.7, 0.62, 0.55)),
     [R(pal_(K, 1, 5, 9), W / 2, 540, 92, lineas=(2,))], ent=("fundido", 0.6))
shot(122.85, F_foto("folios_hd/f003", z0=1.7, z1=2.1, c0=(0.4, 0.3), c1=(0.52, 0.5), par=(0, 0), lado=3800, tono=(0.72, 0.66, 0.56)),
     [R(pal_(K, 1, 9, 13), W / 2, 820, 92, lineas=(2,))], ent=("fuga", 0.7))
shot(125.38, F_foto("folios_hd/f190", z0=1.9, z1=2.3, c0=(0.25, 0.3), c1=(0.7, 0.6), par=(0, 0), lado=3800, tono=(0.5, 0.48, 0.45)),
     [Q([[(w, t) for w, t in pal_(K, 2, 0, 4)], [(w, t) for w, t in pal_(K, 2, 4, 8)]], w_(K, 2, 0) - 0.1, W / 2, 560, 84, sal=w_(K, 2, 8) - 0.1)], ent=("tinta", 0.7), grado=dict(vineta=0.85))
shot(127.12, F_clip("vela", inicio=6, z0=1.05, z1=1.3, tono=(1.0, 0.9, 0.8)),
     [Q([[(w, t) for w, t in pal_(K, 2, 8, 12)], [(w, t) for w, t in pal_(K, 2, 12, 15)]], w_(K, 2, 8) - 0.1, W / 2, 560, 84, sal=129.6)], ent=("fuga", 0.7))
FIN_VOZ = FIN("cierre")
shot(129.85, F_negro(),
     [S([("El", 130.1), ("Libro", 130.3), ("Que", 130.5), ("Nadie", 130.7), ("Puede", 130.9), ("Leer", 131.1)], 960, 470, 110, lineas=(3,)),
      R([("Escaneos", 130.9), ("del", 130.9), ("manuscrito:", 130.9), ("Beinecke", 130.9), ("Library,", 130.9), ("Yale", 130.9), ("(MS", 130.9), ("408)", 130.9)], 960, 700, 30, lineas=None),
      R([("Video:", 131.0), ("Pexels", 131.0), ("·", 131.0), ("Fotos:", 131.0), ("Wikimedia", 131.0), ("Commons", 131.0)], 960, 750, 30)], ent=("negro", 0.6))
_construir()


# ================================================================== Mundo
class Mundo(Escena):
    def preparar(self):
        if self.idx == 0:
            self.sonidos()

    def sonidos(self):
        e = self.ev
        e(0.2, "latido", 0.7, dur=1.6)
        for t, n, v, kw in SND:
            e(t, n, v, **kw)
        e(w_("gancho", 2, 12) + 0.35, "sello", 0.8)
        e(w_("fecha", 0, 13), "ding", 0.35)
        e(w_("fecha", 2, 8) + 0.1, "garabato", 0.5, dur=0.4)
        for tt in (w_("teorias", 2, 0), w_("teorias", 2, 1), w_("teorias", 2, 3)):
            e(tt, "garabato", 0.5, dur=0.35)
        e(w_("teorias", 2, 6) + 0.1, "sello", 0.8)
        for tt in (8.7, 9.0, 43.9, 44.3, 92.4, 92.7):
            e(tt, "garabato", 0.4, dur=0.5)
        e(w_("cierre", 2, 8) - 0.05, "latido", 0.55, dur=1.2)
        e(130.1, "impacto", 0.6)

    def render(self, lz, t):
        i = 0
        for k, d in enumerate(SHOTS):
            if d["t0"] <= t:
                i = k
        d = SHOTS[i]
        img = np.zeros((H, W, 3), np.float32)
        _dibujar(d, img, t)
        tipo, dur = d["ent"]
        if i > 0 and t < d["t0"] + dur:
            A = np.zeros((H, W, 3), np.float32)
            _dibujar(SHOTS[i - 1], A, t)
            img = X.mezcla2(A, img, (t - d["t0"]) / dur, tipo, i)
        img = X.cine(img, t, **d["grado"])
        img *= smooth(prog(t, 0.0, 0.9))
        return np.clip(img, 0, 1).astype(np.float32)


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
