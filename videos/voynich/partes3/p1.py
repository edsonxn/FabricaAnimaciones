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
