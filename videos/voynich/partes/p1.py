# -*- coding: utf-8 -*-
"""El libro que nadie puede leer (manuscrito Voynich) — v2: estilo documental vistoso, cortes rápidos sobre video de apoyo real.

(ARCHIVO GENERADO por _armar.py a partir de partes/p1..p4: edita las partes.)
Todo se dibuja en función del tiempo global (`Mundo`). Cada toma se declara con `shot(t0, fondo, textos, extras, ent, grado)`; el fin de una toma es
el inicio de la siguiente. Los tiempos salen de la voz (`w_(escena, frase, índice_de_palabra)`), así que nada queda desincronizado.
Texto: Poppins Black Italic en mayúsculas con golpe (docu_fx.slam), Impact para golpes de una palabra, Abril Fatface para cifras.
La versión anterior (más lenta, con fotos y polaroids) queda en escenas_v1.py.
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


def w_(eid, fr, i):
    """Tiempo (s) en que empieza la palabra de índice i de la frase fr de la escena eid."""
    ws = _ESC[eid]["frases"][fr]["words"]
    return ws[min(i, len(ws) - 1)]["s"]


def we_(eid, fr, i):
    ws = _ESC[eid]["frases"][fr]["words"]
    return ws[min(i, len(ws) - 1)]["e"]


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


def carta(lz, sp, M, t, t_in, x, y, rot=0.0, s=1.0, desde=(0, -420), dur=0.42, flota=1.0, fase=0.0, op=1.0, ry0=62.0):
    if t < t_in:
        return
    u = e_out(prog(t, t_in, t_in + dur))
    e = t - t_in
    asent = math.exp(-(e - dur) * 3.2) * math.sin((e - dur) * 15.0) * 2.4 if e > dur else 0.0
    fl = flota * 5.0 * math.sin(0.9 * t + fase)
    Mm = M @ D.poner(sp.w, sp.h, lerp(x + desde[0], x, u), lerp(y + desde[1], y, u) + fl, lerp(1.4, 1.0, u) * s, rot + asent + (1 - u) * 16, (1 - u) * ry0)
    D.pegar(lz, sp, Mm, op * smooth(prog(t, t_in, t_in + 0.12)))


# ------------------------------------------------------------------ texto
def TXT(palabras, cx, cy, px=120, fnt="pop_bi", lineas=None, color=BL, clave=None, sal=None, scan=False, mayus=True, escala0=1.28):
    """Bloque de texto de golpe: `palabras` = [(texto, t)]. Devuelve f(lz, t) con .golpes (tiempos de cada palabra)."""
    pal = X.titular(palabras, cx, cy, px, fnt, lineas, color, clave, mayus=mayus)

    def f(lz, t):
        X.slam(lz, pal, t, fnt, px, salida=sal, scan=scan, escala0=escala0)
    f.golpes = [palabras[0][1]] if palabras else []
    return f


def CAP(palabras, cx, cy, px=40, lineas=None, sal=None):
    pal = X.titular(palabras, cx, cy, px, "pop_sbi", lineas, BL, None, mayus=True, espacio=0.2)

    def f(lz, t):
        X.caption(lz, pal, t, px, salida=sal)
    f.golpes = []
    return f


def NUM(txt, cx, cy, px, t0, color=RJ, fnt="abril", sal=None):
    def f(lz, t):
        D.numero(lz, txt, cx, cy, px, t, t0, color=color, fnt=fnt, salida=sal)
    f.golpes = [t0]
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


def franja(lz, fuerza=0.5, y0=0.62):
    Y = np.linspace(0, 1, H, dtype=np.float32)
    g = np.clip((Y - y0) / (1 - y0), 0, 1)
    lz *= (1 - fuerza * g ** 1.3)[:, None, None]


# ================================================================== tomas
SHOTS = []
SND = []          # (t, nombre, vol, kw): efectos de sonido registrados por las tomas


def snd(t, nombre, vol=0.5, **kw):
    SND.append((t, nombre, vol, kw))


SFX_TRANS = {"tinta": ("whoosh", 0.55), "destello": ("brillo", 0.5), "aberracion": ("zoom_whoosh", 0.5), "glitch": ("glitch", 0.45),
             "zoom": ("zoom_whoosh", 0.55), "corte": ("tick", 0.4), "desenfoque": ("whoosh", 0.3), "negro": ("impacto", 0.5), "fundido": None}


def shot(t0, fondo, textos=(), extras=(), ent=("corte", 0.001), grado=None, nombre=""):
    SHOTS.append(dict(t0=t0, fondo=fondo, textos=list(textos), extras=list(extras), ent=ent, grado=grado or {}, nombre=nombre))


def _construir():
    SHOTS.sort(key=lambda d: d["t0"])
    for k, d in enumerate(SHOTS):
        d["t1"] = SHOTS[k + 1]["t0"] if k + 1 < len(SHOTS) else TOTAL + 1.0
        d["golpes"] = sorted(g for tx in d["textos"] for g in getattr(tx, "golpes", []))
        sfx = SFX_TRANS.get(d["ent"][0])
        if sfx and k > 0:
            snd(d["t0"] - 0.04, sfx[0], sfx[1], **({"dur": 0.6} if sfx[0] in ("whoosh", "zoom_whoosh") else {}))
        for g in d["golpes"][:6]:
            snd(g, "pop", 0.30)


def _dibujar(d, lz, t):
    tl = t - d["t0"]
    dur = d["t1"] - d["t0"] + 0.5
    ext = X.pulso(t, d["golpes"])
    d["fondo"](lz, tl, t, dur, ext)
    for e in d["extras"]:
        e(lz, t)
    for tx in d["textos"]:
        tx(lz, t)


# ---------------------------------------------------------------- GANCHO (0 - 17.5)
G = "gancho"
shot(0.0, F_clip("vela", inicio=4.0, z0=1.0, z1=1.28, tono=(1.0, 0.92, 0.82)), [], ent=("fundido", 0.01))
shot(1.10, F_clip("pluma", inicio=1.5, z0=1.05, z1=1.25, c0=(0.4, 0.55), c1=(0.6, 0.5), tono=(0.85, 0.75, 0.65)),
     [TXT([("Un", w_(G, 0, 1)), ("libro", w_(G, 0, 2))], 960, 820, 160, clave=[1])], ent=("destello", 0.35))


def _cover(lz, t):
    sp = folio(1, 900)
    tl = t - 2.35
    ry = lerp(-26, -9, e_out(prog(t, 2.35, 3.9))) + 3 * math.sin(0.6 * t)
    cam = D.Cam((1.0, W / 2, H / 2, 0.0), (1.10, W / 2 + 30, H / 2 - 6, 0.0), 3.0, mano=0.6)(tl)
    Mlib = cam @ D.poner(sp.w, sp.h, 600, 540, 1.0, -3 + 1.5 * math.sin(0.4 * t), ry, 2)
    D.pegar(lz, sp, Mlib, smooth(prog(t, 2.35, 2.9)))
    c = [D.tf(Mlib, x, y) for x, y in ((28, 20), (sp.w - 28, 20), (sp.w - 28, sp.h - 20), (28, sp.h - 20), (28, 20))]
    D.linea_punteada(lz, c, e_inout(prog(t, 2.4, 3.6)), op=1.0 - smooth(prog(t, 3.5, 4.4)))


shot(2.35, F_borroso("f001", 0.34), [TXT(pal_(G, 0, 4, 8), 1440, 400, 118, lineas=(3,)),
                                      TXT(pal_(G, 0, 8, 11), 1440, 640, 118, clave=[2], lineas=(2,))], [_cover], ent=("aberracion", 0.30))

# 240 páginas
shot(5.12, F_clip("paginas1", inicio=1.0, z0=1.05, z1=1.22, tono=(0.8, 0.72, 0.62)),
     [NUM("240", 620, 400, 330, w_(G, 1, 1) - 0.05), TXT([("páginas", w_(G, 1, 3))], 1210, 560, 150, color=BL, mayus=True)],
     [lambda lz, t: X.linea_medida(lz, (260, 720), (1660, 690), e_out(prog(t, w_(G, 1, 1), w_(G, 1, 3) + 0.4)), "240 páginas", t, w_(G, 1, 3), 60)], ent=("tinta", 0.5))


def _polaroids_plantas(lz, t):
    cam = D.Cam((1.0, C0[0], C0[1], 0.5), (1.15, C0[0] + 30, C0[1], -1.0), 2.4, mano=0.8)(t - 6.55)
    D.pegar(lz, corcho(), cam @ D.poner(3400, 2000, C0[0], C0[1]))
    cx, cy = C0
    cartas = (("f004", -420, -120, -7, w_(G, 1, 4) - 0.05), ("f024", 0, 60, 3, w_(G, 1, 4) + 0.28), ("f110", 420, -100, -4, w_(G, 1, 5) - 0.02))
    pts = []
    for k, (nom, dx, dy, r, ti) in enumerate(cartas):
        carta(lz, pola(nom, 400, 1.12, (0.5, 0.42)), cam, t, ti, cx + dx, cy + dy, r, desde=(-400 + 300 * k, -420), fase=k * 1.7)
        if t > ti + 0.25:
            pts.append((cx + dx, cy + dy - 240))
    for a, b in zip(pts[:-1], pts[1:]):
        D.hilo(lz, cam, a, b, smooth(prog(t, w_(G, 1, 5), w_(G, 1, 5) + 0.4)))
    for p in pts:
        D.pin(lz, cam, *p)


shot(6.55, F_negro(), [TXT(pal_(G, 1, 4, 6), 960, 960, 105, clave=[1])], [_polaroids_plantas], ent=("corte", 0.001))

shot(8.20, F_foto("folios_hd/f187", z0=1.5, z1=1.95, c0=(0.30, 0.25), c1=(0.6, 0.55), par=(0, 0), lado=3800, tono=(0.85, 0.84, 0.8)),
     [TXT([("un", w_(G, 1, 7)), ("idioma", w_(G, 1, 8))], 960, 900, 150, clave=[1])],
     [lambda lz, t: X.resaltador(lz, 380, 430, 1240, 495, prog(t, 8.45, 9.4)),
      lambda lz, t: X.elipse_luz(lz, 1350, 700, 300, 120, prog(t, 9.0, 9.9), grosor=6)], ent=("destello", 0.35))
shot(9.70, F_foto("folios_hd/f187", z0=2.1, z1=2.5, c0=(0.62, 0.62), c1=(0.35, 0.3), par=(0, 0), lado=3800, tono=(0.62, 0.6, 0.55)),
     [TXT([("ningún", w_(G, 1, 13)), ("otro", w_(G, 1, 14)), ("lado", w_(G, 1, 15))], 960, 540, 190, clave=[0], lineas=(1,))], ent=("corte", 0.001))

# criptógrafos / militares / computadoras / nadie lo ha logrado
shot(11.35, F_pozo(0.5, 0.45, 0.85, (0.22, 0.17, 0.10)),
     [TXT([("criptógrafos", w_(G, 2, 3))], 960, 900, 130, clave=[0])],
     [lambda lz, t: carta(lz, pola("alberti", 620, 1.0, (0.5, 0.5), "Disco de cifrado"), I3, t, 11.6, 960, 430, -4, desde=(-700, 0), dur=0.45)], ent=("tinta", 0.4))
shot(12.85, F_pozo(0.5, 0.45, 0.85, (0.22, 0.17, 0.10)),
     [TXT([("militares", w_(G, 2, 4))], 960, 900, 150, clave=[0])],
     [lambda lz, t: carta(lz, pola("purple", 620, 1.0, (0.5, 0.42), "Máquina militar"), I3, t, 12.9, 960, 430, 3, desde=(700, 0), dur=0.45)], ent=("corte", 0.001))
shot(13.68, F_clip("codigo2", z0=1.0, z1=1.2, tono=(1.0, 0.72, 0.32), sat=0.0),
     [TXT([("computadoras", w_(G, 2, 6))], 960, 540, 150, clave=[0], scan=True)],
     [lambda lz, t: D.panel_analisis(lz, PALABRAS_VOY, t, 13.85, 960, 800, 900, 260, dur=1.4)], ent=("glitch", 0.25))
shot(15.30, F_foto("folios_hd/f190", z0=1.5, z1=1.9, c0=(0.4, 0.3), c1=(0.6, 0.5), par=(0, 0), lado=3800, tono=(0.5, 0.48, 0.45)),
     [TXT(pal_(G, 2, 9, 13), 960, 400, 140, lineas=(2,), clave=[3])],
     [lambda lz, t: D.estampa(lz, "SIN DESCIFRAR", 960, 800, t, 16.55, 120, rot=-6)], ent=("aberracion", 0.3))

# ---------------------------------------------------------------- ORIGEN (17.5 - 32.5)
O = "origen"
shot(17.50, F_clip("reloj_bolsillo", inicio=3, z0=1.05, z1=1.25, tono=(0.9, 0.78, 0.65)),
     [CAP(pal_(O, 0, 0, 4), 960, 900, 46, lineas=(2,))], ent=("tinta", 0.55))
shot(19.75, F_foto("mondragone_grabado", z0=1.1, z1=1.3, c0=(0.42, 0.5), c1=(0.55, 0.48), par=(60, 8), tono=(0.35, 0.29, 0.23)),
     [NUM("1912", 960, 470, 380, w_(O, 0, 6) - 0.1, color=BL, fnt="pop_bi"), CAP([("Es", 19.9)], 560, 240, 70)], ent=("negro", 0.4))
shot(22.00, F_clip("biblioteca", inicio=1, z0=1.05, z1=1.25, tono=(0.9, 0.78, 0.62), sat=0.6),
     [TXT(pal_(O, 1, 3, 5), 960, 800, 140, lineas=(1,), clave=[0, 1])], ent=("aberracion", 0.3))


def _voynich(lz, t):
    sp = recorte("voynich_retrato")
    u = e_out(prog(t, 23.5, 24.1))
    cam = D.Cam((1.0, W / 2, H / 2, 0.0), (1.12, W / 2 - 20, H / 2, 0.0), 2.6, mano=0.6)(t - 23.5)
    D.pegar(lz, sp, cam @ D.poner(sp.w, sp.h, lerp(1900, 1350, u), 560, 1.0, lerp(12, -2, u)), smooth(prog(t, 23.5, 23.75)))
    D.tag_nombre(lz, "Anticuario · 1912", 1290, 940, t, w_(O, 1, 6) + 0.2, 46)


shot(23.50, F_borroso("f003", 0.32), [TXT(pal_(O, 1, 5, 7), 520, 480, 150, lineas=(1,), clave=[1])], [_voynich], ent=("destello", 0.3))
shot(25.05, F_clip("paginas3", inicio=2, z0=1.05, z1=1.25, tono=(0.75, 0.66, 0.55), sat=0.8),
     [TXT(pal_(O, 1, 7, 10), 960, 540, 140, lineas=(1,), clave=[2])], ent=("corte", 0.001))


def _villa(lz, t):
    D.marca_chartreuse(lz, 1130, 560, 92, t, 26.2)
    D.tag_nombre(lz, "Villa Mondragone · Frascati", 1130, 700, t, 26.3, 46)
    X.linea_medida(lz, (300, 880), (1650, 880), e_out(prog(t, w_(O, 1, 14), w_(O, 1, 16))), "a unos 20 km de Roma", t, w_(O, 1, 16), 60)


shot(26.00, F_foto("mondragone_grabado", z0=1.02, z1=1.2, c0=(0.5, 0.52), c1=(0.6, 0.44), par=(70, 6), tono=(0.9, 0.86, 0.78)),
     [TXT(pal_(O, 1, 12, 14), 960, 250, 120, clave=[1])], [_villa], ent=("tinta", 0.4))
shot(28.60, F_borroso("f003", 0.34),
     [], [lambda lz, t: carta(lz, folio(3, 900), I3, t, 28.65, 620, 540, -3, desde=(-800, 0), dur=0.5)], ent=("aberracion", 0.3))
shot(29.90, F_clip("vela2", inicio=2, z0=1.05, z1=1.3, tono=(1.0, 0.85, 0.7)),
     [TXT([("manuscrito", 30.0), ("Voynich", w_(O, 2, 6))], 960, 470, 165, lineas=(1,), clave=[1])],
     [lambda lz, t: D.pegar(lz, X.sello_circular("Beinecke MS 408", "MS 408", "Yale University"), D.poner(420, 420, 1560, 760, 0.55, -12), 0.9 * smooth(prog(t, 30.9, 31.1)))], ent=("destello", 0.35))
