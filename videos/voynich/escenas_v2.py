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
def TXT(palabras, cx, cy, px=120, fnt="pop_bi", lineas=None, color=BL, clave=None, sal=None, scan=False, mayus=True, escala0=1.65):
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


# ---------------------------------------------------------------- CONTENIDO (32.5 - 50)
C = "contenido"


def HERO(nombre, x=960, y=500, rot=0.0, alto=880, t_in=0.0, ry=(-12, -3), desde=(0, 0), dur=0.5):
    """Folio grande con cámara propia (para 'héroes' de página)."""
    def f(lz, t):
        sp = folio(nombre, alto)
        u = e_out(prog(t, t_in, t_in + dur))
        cam = D.Cam((1.0, W / 2, H / 2, 0.0), (1.10, W / 2, H / 2 + 12, 0.0), 2.4, mano=0.9)(t - t_in)
        D.pegar(lz, sp, cam @ D.poner(sp.w, sp.h, lerp(x + desde[0], x, u), lerp(y + desde[1], y, u), lerp(0.88, 1.0, u), lerp(rot + 6, rot, u), lerp(ry[0], ry[1], u)), smooth(prog(t, t_in, t_in + 0.15)))
    return f


shot(32.55, F_borroso("f004", 0.30), [], [HERO(4, 960, 500, -4, t_in=32.6, desde=(-900, 0))], ent=("tinta", 0.5))
shot(33.05, F_borroso("f007", 0.30), [], [HERO(7, 960, 500, 3, t_in=33.07, desde=(900, 0))], ent=("corte", 0.001))
shot(33.48, F_borroso("f024", 0.30), [TXT([("plantas", w_(C, 0, 2))], 960, 900, 170, fnt="impact", clave=[0])],
     [HERO(24, 960, 500, -2, t_in=33.5, desde=(0, 700))], ent=("corte", 0.001))
shot(34.00, F_clip("microscopio2", z0=1.05, z1=1.3, c0=(0.6, 0.5), c1=(0.7, 0.5), tono=(0.62, 0.52, 0.42), sat=0.35),
     [TXT([("ningún", w_(C, 0, 4)), ("botánico", w_(C, 0, 5))], 960, 850, 150, lineas=(1,), clave=[1])], ent=("aberracion", 0.28))
shot(35.05, F_borroso("f110", 0.30),
     [TXT([("identificar", w_(C, 0, 8))], 960, 930, 150, clave=[0])],
     [HERO(110, 960, 470, 2, t_in=35.07, desde=(0, -600)),
      lambda lz, t: D.estampa(lz, "SIN IDENTIFICAR", 1330, 620, t, w_(C, 0, 10) - 0.05, 90, rot=-8)], ent=("glitch", 0.25))
shot(37.85, F_borroso("f125", 0.30),
     [TXT([("estrellas", w_(C, 1, 2))], 960, 930, 160, fnt="impact", clave=[0])],
     [HERO(125, 960, 470, -6, t_in=37.87, alto=880), lambda lz, t: X.elipse_luz(lz, 960, 470, 300, 300, prog(t, 38.4, 39.1), grosor=6)], ent=("tinta", 0.45))
shot(39.15, F_borroso("f141", 0.30),
     [TXT([("mujeres", w_(C, 1, 3)), ("bañándose", w_(C, 1, 4))], 960, 930, 120, lineas=(), clave=[1])],
     [HERO(141, 960, 470, 4, t_in=39.17, ry=(12, 4), desde=(900, 0))], ent=("aberracion", 0.28))
shot(40.50, F_foto("f136", z0=1.6, z1=2.0, c0=(0.5, 0.75), c1=(0.5, 0.3), par=(0, 0), lado=2600, tono=(0.85, 0.85, 0.8)),
     [TXT([("tuberías", w_(C, 1, 6)), ("extrañas", w_(C, 1, 7))], 960, 930, 130, clave=[0, 1])], ent=("corte", 0.001))

PAGS = (187, 190, 176, 175, 161, 153, 148, 144)


def _montaje(lz, t):
    k = int((t - 41.45) / 0.21) % len(PAGS)
    sp = folio(PAGS[k], 900)
    Mm = D.poner(sp.w, sp.h, 960 + 40 * math.sin(k * 2.1), 480, 1.0 + 0.05 * ((t - 41.45) % 0.21) / 0.21, (k % 5 - 2) * 2.5, (k % 3 - 1) * 8)
    D.pegar(lz, sp, Mm, 1.0)


shot(41.45, F_borroso("f190", 0.28), [TXT(pal_(C, 1, 9, 12), 960, 940, 120, clave=[0, 2])], [_montaje], ent=("zoom", 0.28))
shot(43.30, F_foto("folios_hd/f187", z0=1.7, z1=2.2, c0=(0.3, 0.3), c1=(0.6, 0.55), par=(0, 0), lado=3800, tono=(0.72, 0.7, 0.66)),
     [TXT([("alfabeto", w_(C, 1, 14)), ("desconocido", w_(C, 1, 15))], 960, 880, 140, lineas=(1,), clave=[1])],
     [lambda lz, t: X.resaltador(lz, 300, 300, 1000, 365, prog(t, 43.4, 44.1)), lambda lz, t: X.resaltador(lz, 700, 560, 1500, 625, prog(t, 43.9, 44.7), semilla=3)], ent=("destello", 0.3))
shot(45.40, F_foto("escriba", z0=1.02, z1=1.22, c0=(0.5, 0.5), c1=(0.56, 0.45), par=(60, 12), tono=(0.72, 0.66, 0.58)),
     [TXT([("Nadie", w_(C, 2, 0)), ("sabe", w_(C, 2, 1))], 700, 200, 96, sal=w_(C, 2, 2) - 0.05), NUM("¿Quién?", 1300, 320, 230, w_(C, 2, 2) - 0.05, color=AM, fnt="impact")], ent=("tinta", 0.5), grado=dict(fuerza_vineta=0.75))
shot(47.20, F_clip("escribir", inicio=2, z0=1.05, z1=1.3, c0=(0.55, 0.5), c1=(0.7, 0.5), tono=(0.9, 0.8, 0.7)),
     [NUM("¿Por qué?", 960, 300, 240, w_(C, 2, 6) - 0.05, color=BL, fnt="impact")], ent=("aberracion", 0.28))

# ---------------------------------------------------------------- FECHA (50 - 67.5)
Fh = "fecha"
shot(50.05, F_clip("reloj_oscuro", inicio=1, z0=1.05, z1=1.3, tono=(0.9, 0.8, 0.7)),
     [NUM("2009", 960, 480, 420, w_(Fh, 0, 1) - 0.05, color=BL, fnt="pop_bi")], ent=("tinta", 0.55))
shot(51.75, F_clip("microscopio", z0=1.05, z1=1.25, c0=(0.55, 0.5), c1=(0.6, 0.5), tono=(0.62, 0.52, 0.42), sat=0.35),
     [TXT([("Arizona", w_(Fh, 0, 7))], 960, 880, 170, fnt="impact", clave=[0])],
     [lambda lz, t: D.tag_nombre(lz, "Universidad de Arizona", 560, 250, t, w_(Fh, 0, 5), 56)], ent=("aberracion", 0.28))
shot(53.05, F_foto("folios_hd/f001", z0=1.5, z1=2.0, c0=(0.4, 0.3), c1=(0.55, 0.55), par=(0, 0), lado=3800, tono=(0.7, 0.65, 0.55)),
     [TXT([("pergamino", w_(Fh, 0, 10))], 960, 880, 150, fnt="impact", clave=[0])], ent=("corte", 0.001))


def _muestras(lz, t):
    for k, (nom, ley) in enumerate((("f017", "folio 8"), ("f051", "folio 26"), ("f093", "folio 47"), ("f123", "folio 68"))):
        carta(lz, pola(nom, 400, 1.25, (0.5, 0.45), ley), I3, t, 54.22 + 0.22 * k, 330 + k * 420, 470 + (k % 2) * 60, (-4, 3, -2, 5)[k], desde=(0, -700), dur=0.4, fase=k)
        snd(54.22 + 0.22 * k, "obturador", 0.4)


shot(54.20, F_pozo(0.5, 0.5, 0.9, (0.20, 0.16, 0.10)),
     [TXT([("carbono", w_(Fh, 0, 12)), ("14", w_(Fh, 0, 13))], 960, 930, 130, clave=[0, 1])], [_muestras], ent=("desenfoque", 0.3))
shot(55.95, F_clip("humo", inicio=2, z0=1.05, z1=1.25, tono=(0.9, 0.85, 0.85)),
     [TXT([("el", w_(Fh, 1, 0)), ("resultado", w_(Fh, 1, 1))], 960, 540, 160, clave=[1])], ent=("tinta", 0.5))
shot(57.25, F_clip("pagina_cerca", inicio=5, z0=1.05, z1=1.2, tono=(0.30, 0.28, 0.26)),
     [NUM("1404", 640, 250, 210, w_(Fh, 1, 5) - 0.05, color=AM), NUM("1438", 1280, 250, 210, w_(Fh, 1, 11) - 0.05, color=AM)],
     [lambda lz, t: D.linea_tiempo(lz, t, 57.3, W / 2, 620, 1300, 1500, 1404, 1438, dur=max(0.8, w_(Fh, 1, 11) - 58.3), marcas=[(1455, "Biblia de Gutenberg")], etiqueta="Fecha del pergamino · carbono 14")], ent=("glitch", 0.25))
shot(61.45, F_foto("folios_hd/f001", z0=1.4, z1=1.8, c0=(0.6, 0.6), c1=(0.4, 0.3), par=(0, 0), lado=3800, tono=(0.7, 0.65, 0.55)),
     [TXT([("pergamino", w_(Fh, 2, 1)), ("medieval", w_(Fh, 2, 3))], 960, 480, 170, lineas=(1,), clave=[1])], ent=("destello", 0.3))
shot(63.75, F_foto("f008", z0=1.35, z1=1.6, c0=(0.5, 0.35), c1=(0.5, 0.5), par=(0, 0), lado=2600, tono=(0.45, 0.43, 0.4)),
     [TXT(pal_(Fh, 2, 4, 9), 960, 470, 130, lineas=(3,), clave=[3, 4])],
     [lambda lz, t: D.marcador_mano(lz, "tachado", 960, 530, 1080, 10, prog(t, w_(Fh, 2, 8) + 0.05, w_(Fh, 2, 8) + 0.4), grosor=14)], ent=("tinta", 0.45))


# ---------------------------------------------------------------- DUEÑOS (67.5 - 77.5)
Dn = "duenos"
shot(67.50, F_foto("escriba2", z0=1.02, z1=1.25, c0=(0.5, 0.5), c1=(0.45, 0.42), par=(50, 10), tono=(0.5, 0.45, 0.4)),
     [TXT(pal_(Dn, 0, 0, 4), 960, 470, 150, lineas=(2,), sal=w_(Dn, 0, 6) + 0.25)], ent=("tinta", 0.55), grado=dict(polvo=0.5))
shot(70.28, F_clip("carta", inicio=3, z0=1.05, z1=1.3, c0=(0.5, 0.5), c1=(0.6, 0.55), tono=(0.85, 0.78, 0.68)),
     [TXT(pal_(Dn, 1, 0, 5), 960, 250, 110, lineas=(2,), clave=[1])],
     [lambda lz, t: carta(lz, X.estampilla("kircher", "1665", 300), I3, t, 70.75, 1560, 700, 6, desde=(500, 300), dur=0.45),
      lambda lz, t: D.tag_nombre(lz, "Carta a Athanasius Kircher", 1470, 920, t, 71.2, 40)], ent=("aberracion", 0.28))
shot(72.85, F_foto("rodolfo_arcimboldo", z0=1.02, z1=1.25, c0=(0.5, 0.42), c1=(0.5, 0.36), par=(80, 10), tono=(0.9, 0.86, 0.8)),
     [TXT([("el", w_(Dn, 1, 7)), ("emperador", w_(Dn, 1, 8))], 560, 800, 140, lineas=(1,), clave=[1]),
      TXT([("Rodolfo", w_(Dn, 1, 9)), ("II", w_(Dn, 1, 10))], 560, 560, 170, lineas=(1,), clave=[0, 1], sal=74.6)],
     [lambda lz, t: D.tag_nombre(lz, "Rodolfo II", 1500, 260, t, w_(Dn, 1, 9), 56)], ent=("glitch", 0.25))
shot(74.60, F_clip("monedas", inicio=2, z0=1.05, z1=1.3, c0=(0.5, 0.5), c1=(0.6, 0.5), tono=(0.75, 0.7, 0.65)),
     [NUM("600", 540, 360, 380, w_(Dn, 1, 14) - 0.05), TXT([("ducados", w_(Dn, 1, 15)), ("de", w_(Dn, 1, 16)), ("oro", w_(Dn, 1, 17))], 960, 880, 140, lineas=(1,), clave=[1, 2])],
     ent=("destello", 0.3))

# ---------------------------------------------------------------- INTENTOS (77.5 - 100)
It = "intentos"
shot(77.50, F_clip("maquina", inicio=1, z0=1.05, z1=1.3, tono=(0.75, 0.75, 0.7), sat=0.6),
     [TXT([("siglo", w_(It, 0, 3)), ("XX", w_(It, 0, 4))], 960, 540, 200, fnt="impact", clave=[1], mayus=False)], ent=("tinta", 0.5))


def _friedman_ext(lz, t):
    D.tag_nombre(lz, "William Friedman", 560, 860, t, w_(It, 0, 5), 52)


shot(79.05, F_foto("friedman", z0=1.05, z1=1.28, c0=(0.32, 0.42), c1=(0.34, 0.36), par=(80, 18), tono=(0.9, 0.9, 0.9)),
     [TXT([("William", w_(It, 0, 5)), ("Friedman", w_(It, 0, 6))], 1400, 330, 120, lineas=(1,), clave=[1])], [_friedman_ext], ent=("aberracion", 0.28), grado=dict(sat=0.7))
shot(80.45, F_clip("maquina2", inicio=3, z0=1.05, z1=1.3, tono=(0.7, 0.7, 0.68), sat=0.6),
     [TXT([("criptógrafo", w_(It, 0, 8))], 960, 540, 150, fnt="impact", clave=[0])], ent=("corte", 0.001))
shot(81.22, F_pozo(0.5, 0.45, 0.85, (0.26, 0.10, 0.28)),
     [TXT(pal_(It, 0, 12, 14), 960, 800, 110, clave=[]), TXT([("Púrpura", w_(It, 0, 14))], 960, 940, 170, fnt="impact", clave=[0])],
     [lambda lz, t: carta(lz, pola("purple", 640, 1.0, (0.5, 0.42), "Máquina Púrpura"), I3, t, 81.3, 960, 400, 3, desde=(0, -700), dur=0.45)], ent=("glitch", 0.25))
shot(82.90, F_clip("reloj_bolsillo", inicio=6, z0=1.05, z1=1.3, tono=(0.85, 0.75, 0.65)),
     [TXT([("le", w_(It, 0, 15)), ("dedicó", w_(It, 0, 16))], 960, 300, 110, lineas=(1,)), TXT([("años", w_(It, 0, 17))], 960, 640, 260, fnt="impact", clave=[0])], ent=("tinta", 0.45))
shot(84.98, F_borroso("f190", 0.28),
     [TXT(pal_(It, 1, 0, 3), 960, 900, 125, lineas=(1,), clave=[1, 2])],
     [HERO(190, 960, 470, -3, t_in=85.0, desde=(0, 700)),
      lambda lz, t: D.marcador_mano(lz, "tachado", 960, 470, 700, 800, prog(t, w_(It, 1, 2) + 0.1, w_(It, 1, 2) + 0.5), grosor=16),
      lambda lz, t: D.marcador_mano(lz, "tachado", 960, 470, -700, 800, prog(t, w_(It, 1, 2) + 0.25, w_(It, 1, 2) + 0.65), grosor=16)], ent=("corte", 0.001))
shot(86.22, F_clip("humo", inicio=8, z0=1.05, z1=1.25, tono=(0.85, 0.85, 0.9)),
     [NUM("1959", 700, 400, 300, 86.4, color=BL, fnt="pop_bi"), CAP(pal_(It, 1, 3, 6), 700, 620, 52)],
     [lambda lz, t: D.pegar(lz, X.sello_circular("Anagrama", "1959", "Philological Quarterly"), D.poner(420, 420, 1420, 500, 1.0, -10), 0.92 * smooth(prog(t, w_(It, 1, 7), w_(It, 1, 7) + 0.15)))], ent=("destello", 0.3))
shot(88.30, F_foto("folios_hd/f187", z0=1.6, z1=2.0, c0=(0.45, 0.4), c1=(0.6, 0.55), par=(0, 0), lado=3800, tono=(0.6, 0.58, 0.54)),
     [TXT([("lenguaje", w_(It, 1, 11)), ("artificial", w_(It, 1, 12))], 960, 540, 190, lineas=(1,), clave=[1])], ent=("aberracion", 0.28))
shot(90.20, F_clip("humo", inicio=1, z0=1.05, z1=1.3, tono=(0.75, 0.8, 0.9)),
     [TXT([("inquietante", w_(It, 2, 4))], 960, 540, 190, fnt="impact", clave=[0], scan=True)], ent=("glitch", 0.28), grado=dict(fuerza_vineta=0.8))
shot(91.72, F_foto("folios_hd/f190", z0=1.9, z1=2.4, c0=(0.25, 0.3), c1=(0.7, 0.6), par=(0, 0), lado=3800, tono=(0.55, 0.53, 0.5)),
     [TXT(pal_(It, 2, 7, 12), 960, 470, 150, lineas=(3,), clave=[2, 4])], ent=("corte", 0.001), grado=dict(fuerza_vineta=0.8))
shot(94.05, F_foto("folios_hd/f187", z0=1.6, z1=1.95, c0=(0.5, 0.4), c1=(0.5, 0.5), par=(0, 0), lado=3800, tono=(0.30, 0.29, 0.27)),
     [TXT([("patrones", w_(It, 3, 3)), ("estadísticos", w_(It, 3, 4))], 960, 130, 90, clave=[0, 1], lineas=()),
      TXT([("idioma", w_(It, 3, 10)), ("real", w_(It, 3, 11))], 960, 950, 150, lineas=(1,), clave=[1])],
     [lambda lz, t: D.grafica_zipf(lz, ZIPF, t, 94.15, W / 2, 500, 1240, 640, dur=3.4),
      lambda lz, t: X.elipse_luz(lz, 900, 560, 230, 150, prog(t, w_(It, 3, 10), w_(It, 3, 11) + 0.4), grosor=6)], ent=("desenfoque", 0.35))


# ---------------------------------------------------------------- TEORÍAS (100 - 112.5): tablero de evidencias con saltos de cámara
Te = "teorias"
KEYS = [(100.0, 1.0, C0[0], C0[1] - 40, 0.0), (101.45, 1.55, C0[0] - 520, C0[1] + 20, -1.5), (102.95, 1.5, C0[0], C0[1] + 90, 1.0),
        (105.0, 1.0, C0[0], C0[1] - 40, 0.0), (106.3, 1.55, C0[0] + 520, C0[1] + 10, 1.5), (108.0, 1.0, C0[0], C0[1] - 40, 0.0), (109.0, 1.12, C0[0] + 20, C0[1], -0.8)]


def _cam_keys(t):
    """Cámara por claves: mantiene, y salta con un movimiento rápido de 0,35 s (corte dinámico)."""
    for i in range(len(KEYS) - 1, -1, -1):
        if t >= KEYS[i][0]:
            k = KEYS[i]
            prev = KEYS[i - 1] if i > 0 else k
            u = e_inout(clamp01((t - k[0]) / 0.35))
            z, cx, cy, rot = [lerp(prev[j], k[j], u) for j in (1, 2, 3, 4)]
            z += 0.02 * (t - k[0]) / 2.0
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
        D.pegar(lz, q, M, smooth(prog(t, 100.1, 100.4)))
        pm, a_, m = D.palabra_img("¿Qué es?", "serif", 84, (0.72, 0.05, 0.05), stroke=0.02, glow=0.0)
        x, y = D.tf(M, q.w / 2, q.h / 2)
        D.mezclar_pm(lz, pm, a_, int(x - pm.shape[1] / 2), int(y - pm.shape[0] / 2), smooth(prog(t, 100.2, 100.5)))
    for k, p in enumerate(pins):
        D.hilo(lz, cam, (cx, cy - 350), p, smooth(prog(t, ti[k] + 0.2, ti[k] + 0.7)))
    if t > 100.1:
        D.pin(lz, cam, cx, cy - 350)
    for p in pins:
        D.pin(lz, cam, *p)
    for k, tt in enumerate((w_(Te, 2, 0), w_(Te, 2, 1), w_(Te, 2, 3))):
        dx, dy = tarjetas[k][1], tarjetas[k][2]
        x, y = D.tf(cam, cx + dx, cy + dy)
        z = float(np.sqrt(abs(np.linalg.det(cam[:2, :2]))))
        D.marcador_mano(lz, "tachado", x, y, ANC * 0.9 * z, ALT2 * 1.7 * z, prog(t, tt, tt + 0.3), grosor=16)
        D.marcador_mano(lz, "tachado", x, y, -ANC * 0.9 * z, ALT2 * 1.7 * z, prog(t, tt + 0.12, tt + 0.42), grosor=16)
    for k, (t_in, a, b) in enumerate((("a", 0, 0), )):
        pass
    D.estampa(lz, "SIN RESOLVER", W / 2, 640, t, w_(Te, 2, 6) + 0.1, 120, rot=-7)


shot(100.0, F_negro(), [TXT([("código", w_(Te, 0, 5))], 960, 940, 170, fnt="impact", clave=[0], sal=w_(Te, 0, 8) - 0.1),
                        TXT([("idioma", w_(Te, 0, 8)), ("inventado", w_(Te, 0, 9))], 960, 940, 130, lineas=(1,), clave=[1], sal=w_(Te, 1, 6) - 0.1),
                        TXT([("fraude", w_(Te, 1, 6)), ("medieval", w_(Te, 1, 7))], 960, 940, 130, lineas=(1,), clave=[0], sal=w_(Te, 1, 9) - 0.1),
                        TXT([("muy", w_(Te, 1, 8)), ("ingenioso", w_(Te, 1, 9))], 960, 940, 130, lineas=(1,), clave=[1], sal=w_(Te, 2, 0) - 0.1),
                        TXT(pal_(Te, 2, 0, 4), 960, 1000, 92, clave=[3])], [_tablero], ent=("tinta", 0.5))

# ---------------------------------------------------------------- CIERRE (112.5 - 131.25)
K = "cierre"
shot(112.50, F_clip("biblioteca", inicio=0.5, z0=1.0, z1=1.28, c0=(0.5, 0.5), c1=(0.5, 0.55), tono=(1.0, 0.9, 0.8)),
     [TXT([("descansa", w_(K, 0, 3))], 960, 900, 160, fnt="impact", clave=[0])], ent=("tinta", 0.55))
shot(114.85, F_foto("beinecke_interior", z0=1.05, z1=1.26, c0=(0.5, 0.55), c1=(0.5, 0.42), par=(70, 14), tono=(0.95, 0.9, 0.85)),
     [TXT([("libros", w_(K, 0, 8)), ("raros", w_(K, 0, 9))], 960, 250, 150, lineas=(1,), clave=[1])],
     [lambda lz, t: D.tag_nombre(lz, "Biblioteca Beinecke", 470, 860, t, w_(K, 0, 6), 54)], ent=("aberracion", 0.28))
shot(116.92, F_clip("paginas2", inicio=0.5, z0=1.05, z1=1.25, tono=(0.7, 0.62, 0.52)),
     [TXT(pal_(K, 0, 12, 15), 960, 880, 120, lineas=(1,), clave=[2])],
     [lambda lz, t: D.pegar(lz, X.sello_circular("Universidad", "YALE", "New Haven"), D.poner(420, 420, 1500, 450, 0.85, -10), 0.95 * smooth(prog(t, w_(K, 0, 14), w_(K, 0, 14) + 0.15))),
      lambda lz, t: carta(lz, X.estampilla("f003", "MS 408", 320), I3, t, 117.0, 380, 470, -6, desde=(-500, 0), dur=0.45)], ent=("glitch", 0.25))


def _internet(lz, t):
    tl = t - 119.15
    vent = spr("ventana", lambda: _ventana())
    cam = D.Cam((1.0, W / 2, H / 2, 0.0), (1.06, W / 2, H / 2 - 8, 0.0), 2.0, mano=0.6)(tl)
    D.pegar(lz, vent, cam @ D.poner(vent.w, vent.h, W / 2, 470, 1.0, 0.0), smooth(prog(t, 119.15, 119.4)))
    nomb = (4, 7, 10, 24, 32, 110, 111, 136, 141, 147, 175, 176)
    for k, n in enumerate(nomb):
        col, fila = k % 6, k // 6
        x = 405 + col * 222
        y = 385 + fila * 335 - 6 * math.sin(0.7 * t + k)
        sp = pola(f"f{n:03d}", 205, 1.36, (0.5, 0.45))
        D.pegar(lz, sp, cam @ D.poner(sp.w, sp.h, x, y, 1.0, (k % 3 - 1) * 1.5), smooth(prog(t, 119.3 + 0.05 * k, 119.6 + 0.05 * k)))


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


shot(119.15, F_pozo(0.5, 0.5, 0.85, (0.17, 0.15, 0.13)),
     [TXT([("internet", w_(K, 1, 4))], 960, 960, 130, fnt="impact", clave=[0])], [_internet], ent=("tinta", 0.45))
shot(120.90, F_clip("proyector", inicio=4, z0=1.05, z1=1.3, c0=(0.5, 0.5), c1=(0.6, 0.5), tono=(0.7, 0.62, 0.55)),
     [NUM("600", 640, 380, 380, w_(K, 1, 6) - 0.05, color=AM), TXT([("años", w_(K, 1, 7))], 1330, 520, 200, fnt="impact", clave=[0])], ent=("aberracion", 0.28))
shot(122.85, F_foto("folios_hd/f003", z0=1.7, z1=2.3, c0=(0.4, 0.3), c1=(0.52, 0.5), par=(0, 0), lado=3800, tono=(0.72, 0.66, 0.56)),
     [TXT([("guardando", w_(K, 1, 10)), ("su", w_(K, 1, 11)), ("secreto", w_(K, 1, 12))], 960, 880, 150, lineas=(1,), clave=[2])], ent=("destello", 0.3))
shot(125.38, F_foto("folios_hd/f190", z0=1.9, z1=2.4, c0=(0.25, 0.3), c1=(0.7, 0.6), par=(0, 0), lado=3800, tono=(0.5, 0.48, 0.45)),
     [TXT(pal_(K, 2, 0, 8), 960, 480, 120, lineas=(4,), clave=[7], sal=w_(K, 2, 8) - 0.08)], ent=("tinta", 0.45), grado=dict(fuerza_vineta=0.8))
shot(127.12, F_clip("vela", inicio=6, z0=1.05, z1=1.35, tono=(1.0, 0.9, 0.8)),
     [TXT(pal_(K, 2, 8, 15), 960, 470, 130, lineas=(4,), clave=[3, 4, 5, 6], sal=129.6)], ent=("destello", 0.35))
FIN_VOZ = FIN("cierre")
shot(129.85, F_negro(),
     [TXT([("El", 130.1), ("libro", 130.3), ("que", 130.5), ("nadie", 130.7), ("puede", 130.9), ("leer", 131.1)], 960, 470, 100, lineas=(3,), clave=[3, 5], escala0=1.3),
      CAP([("Escaneos", 130.9), ("del", 130.9), ("manuscrito:", 130.9), ("Beinecke", 130.9), ("Library,", 130.9), ("Yale", 130.9), ("(MS", 130.9), ("408)", 130.9)], 960, 720, 26),
      CAP([("Video:", 131.0), ("Pexels", 131.0), ("·", 131.0), ("Fotos:", 131.0), ("Wikimedia", 131.0), ("Commons", 131.0)], 960, 765, 26)], ent=("negro", 0.5))
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
        e(w_("origen", 0, 6) - 0.05, "impacto", 0.6)
        e(w_("fecha", 0, 13), "ding", 0.35)
        e(w_("fecha", 2, 8) + 0.1, "garabato", 0.5, dur=0.4)
        for tt in (w_("teorias", 2, 0), w_("teorias", 2, 1), w_("teorias", 2, 3)):
            e(tt, "garabato", 0.5, dur=0.35)
        e(w_("teorias", 2, 6) + 0.1, "sello", 0.8)
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
        img = D.acabado(img, t, **d["grado"])
        img *= smooth(prog(t, 0.0, 0.9))
        return np.clip(img, 0, 1).astype(np.float32)


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
