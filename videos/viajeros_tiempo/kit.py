# -*- coding: utf-8 -*-
"""Kit del documental «¿Quién es Satoshi Nakamoto?»: anclas por PALABRA (resisten cambios de voz), textos del estilo documental v3
(R = cursiva blanca con escaneo, S = serif amarillo, N = cifra, Q = pregunta, TAG, SELLO, TRAZO), créditos y sonidos registrados.
Copiado de videos/christa_pike/kit_cp.py (partes genéricas). El tablero vivo está en tablero.py."""
import json
import math
import os
import re
import unicodedata

import cv2
import numpy as np
from PIL import Image, ImageDraw

from escena_base import *  # noqa: F401,F403   (TL, Escena...)
from motor import H, W, e_back, e_in, e_inout, e_out, lerp, prog, smooth, clamp01
import docu as D  # después del *: escena_base también exporta un `D`
import docu_fx as X

_ESC = {e["id"]: e for e in TL["escenas"]}
TOTAL = TL["total"]
AM, BL, RJ = D.AMARILLO, D.BLANCO, D.ROJO
I3 = np.eye(3)

# ------------------------------------------------------------------ anclas por palabra
def _n(s):
    s = unicodedata.normalize("NFD", s.lower())
    return re.sub(r"[^a-z0-9ñ]+", "", "".join(c for c in s if unicodedata.category(c) != "Mn"))


def _ws(eid, fr):
    return _ESC[eid]["frases"][fr]["words"]


def wi(eid, fr, clave, nth=0):
    """Índice de la palabra de la frase que empieza por `clave` (la nth-ésima coincidencia)."""
    k = _n(clave)
    c = 0
    for i, w in enumerate(_ws(eid, fr)):
        if _n(w["w"]).startswith(k):
            if c == nth:
                return i
            c += 1
    raise KeyError(f"{eid}[{fr}] sin palabra '{clave}' (#{nth}): " + " ".join(w["w"] for w in _ws(eid, fr)))


def ww(eid, fr, clave, nth=0, sep=0.0):
    """Tiempo (s) en que empieza la palabra `clave` de la frase fr de la escena eid."""
    return _ws(eid, fr)[wi(eid, fr, clave, nth)]["s"] + sep


def we(eid, fr, clave, nth=0):
    """Tiempo (s) en que termina la palabra."""
    return _ws(eid, fr)[wi(eid, fr, clave, nth)]["e"]


def w_(eid, fr, i):
    ws = _ws(eid, fr)
    return ws[min(i, len(ws) - 1)]["s"]


def INI(eid, i=0):
    return _ESC[eid]["frases"][i]["t0"]


def FIN(eid, i=-1):
    return _ESC[eid]["frases"][i]["t1"]


def pk(eid, fr, a, b=None, nth=0, nthb=0):
    """[(texto, t)] desde la palabra que empieza por `a` hasta la que empieza por `b` (inclusive); sin `b`, solo `a`."""
    i0 = wi(eid, fr, a, nth)
    i1 = wi(eid, fr, b, nthb) if b else i0
    return [(w["w"].strip(".,;:¿?¡!…\"()«»"), w["s"]) for w in _ws(eid, fr)[i0:i1 + 1]]


def pal_(eid, fr, i0, i1):
    ws = _ws(eid, fr)[i0:i1]
    return [(w["w"].strip(".,;:¿?¡!…\"()«»"), w["s"]) for w in ws]


# ------------------------------------------------------------------ caché de sprites
_C = {}


def spr(clave, fn):
    if clave not in _C:
        _C[clave] = fn()
    return _C[clave]


# ------------------------------------------------------------------ texto (estilos del original)
def _cortes(palabras, fnt, px, ancho_max, mayus=True, espacio=0.27):
    """Cortes de línea equilibrados para que el bloque no pase de `ancho_max` px (lineas para docu_fx.titular)."""
    ws = [D._ancho_palabra(w.upper() if mayus else w, fnt, px) for w, _ in palabras]
    sp = px * espacio
    tot = sum(ws) + sp * (len(ws) - 1)
    n = max(1, int(math.ceil(tot / ancho_max)))
    if n == 1:
        return None
    obj = tot / n
    cortes, acc = [], 0.0
    for i, w in enumerate(ws):
        if acc > 0 and acc + w / 2 > obj * (len(cortes) + 1) and len(cortes) < n - 1:
            cortes.append(i)
        acc += w + sp
    return tuple(cortes) or None


# en pantalla los nombres van con su ortografía REAL (la narración los escribe fonéticos para la voz española)
REAL = {"dórian": "Dorian", "bak": "Back", "jal": "Hal", "fíni": "Finney", "sábo": "Szabo", "nik": "Nick", "ádam": "Adam", "kreig": "Craig",
        "rait": "Wright", "sásaman": "Sassaman", "píter": "Peter", "tod": "Todd", "yon": "John", "carrerú": "Carreyrou", "niu": "New",
        "taims": "Times", "jáshcash": "Hashcash", "gávin": "Gavin", "ándresen": "Andresen", "témpel": "Temple", "siti": "City",
        "niusuik": "Newsweek", "uei": "Wei", "líman": "Lehman", "bróders": "Brothers", "yeims": "James", "mélor": "Mellor",
        "uikiliks": "WikiLeaks", "góld": "gold", "forbs": "Forbes", "teranos": "Theranos", "pol": "Paul", "ru": "Roux", "solochi": "Solotshi"}


def _real(palabras):
    out = []
    for w, t in palabras:
        nucleo = w.strip(".,;:¿?¡!…\"()«»")
        r = REAL.get(nucleo.lower())
        out.append((w.replace(nucleo, r) if (r and nucleo) else w, t))
    return out


def R(palabras, cx=W / 2, cy=H * 0.56, px=88, lineas=None, sal=None, ancho_max=1560):
    """Texto principal: cursiva blanca en mayúsculas con líneas de escaneo, palabra a palabra (corta líneas solo si no cabe)."""
    palabras = _real(palabras)
    if lineas is None:
        lineas = _cortes(palabras, "pop_sbi", px, ancho_max)
    pal = X.rotulo(palabras, cx, cy, px, lineas)

    def f(lz, t):
        X.dibujar_rotulo(lz, pal, t, px, salida=sal)
    return f


def S(palabras, cx=W / 2, cy=H * 0.55, px=98, lineas=None, sal=None):
    """Serif amarillo condensado, Título Con Mayúsculas (nombres, lugares, cifras)."""
    palabras = _real(palabras)
    if lineas is None:
        lineas = _cortes(palabras, "serif_cond", px, 1600, False, 0.24)
    pal = X.serif_amarillo(palabras, cx, cy, px, lineas)

    def f(lz, t):
        X.dibujar_serif(lz, pal, t, px, salida=sal)
    return f


def N(txt, cx, cy, px, t0, color=RJ, sal=None):
    """Cifra grande en serif condensado (roja o amarilla)."""
    def f(lz, t):
        D.numero(lz, txt, cx, cy, px, t, t0, color=color, fnt="abril_cond", salida=sal, pop=False)
    return f


def Q(lineas, t0, cx=W / 2, cy=H * 0.60, px=88, sal=None):
    """Pregunta: serif blanco + signo '?' rojo."""
    def f(lz, t):
        X.pregunta_c(lz, lineas, t, t0, cx, cy, px, salida=sal)
    return f


def TAG(txt, x, y, t0, px=40, rot=-3.0, sal=None):
    def f(lz, t):
        D.tag_nombre(lz, txt, x, y, t, t0, px, rot, salida=sal)
    return f


def SELLO(txt, x, y, t0, px=90, rot=-8.0, color=(0.78, 0.08, 0.08), sal=None):
    snd(t0, "sello", 0.65)

    def f(lz, t):
        D.estampa(lz, txt, x, y, t, t0, px, color, rot, salida=sal)
    return f


def TRAZO(p0, p1, t0, dur=0.6, w=24, sal=None, borra=0.5):
    """Trazo rojo recto: se dibuja desde t0 y (si hay `sal`) se borra desde ahí."""
    def f(lz, t):
        u1 = e_out(prog(t, t0, t0 + dur))
        u0 = e_inout(prog(t, sal, sal + borra)) if sal is not None else 0.0
        X.trazo_recto(lz, p0, p1, u0, u1, w)
    return f


# ------------------------------------------------------------------ crédito en pantalla (material de terceros)
def _cred_sprite(txt):
    from PIL import ImageFont
    f = D.fuente("sans_l", 25)
    bb = f.getbbox(txt)
    w, h = bb[2] - bb[0] + 24, bb[3] - bb[1] + 16
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text((12 - bb[0], 8 - bb[1]), txt, font=f, fill=(240, 238, 232, 255), stroke_width=2, stroke_fill=(0, 0, 0, 255))
    a = np.asarray(im, np.float32)[..., 3] / 255.0
    return D.Sprite(np.asarray(im)[..., :3].copy(), a, sombra=False)


def CRED(txt, t0, t1, x=64, y=1024):
    """Rótulo pequeño abajo a la izquierda: «Imagen: WBIR», «Foto: Wikimedia Commons / autor»..."""
    def f(lz, t):
        if t < t0 or t > t1 + 0.4:
            return
        o = 0.82 * smooth(prog(t, t0, t0 + 0.4)) * (1 - smooth(prog(t, t1 - 0.2, t1 + 0.35)))
        sp = spr(("cred", txt), lambda: _cred_sprite(txt))
        D.pegar(lz, sp, D.poner(sp.w, sp.h, x + sp.w / 2, y, 1.0, 0.0), o)
    return f


# ------------------------------------------------------------------ fondos
# ------------------------------------------------------------------ tomas (SHOTS) y sonidos registrados por ellas
SHOTS = []
SND = []          # (t, nombre, vol, kw): efectos de sonido registrados por las tomas


def snd(t, nombre, vol=0.5, **kw):
    SND.append((t, nombre, vol, kw))


SFX_TRANS = {"tinta": ("whoosh", 0.4), "destello": ("brillo", 0.35), "fuga": ("zoom_whoosh", 0.4), "aberracion": ("whoosh", 0.35),
             "glitch": ("glitch", 0.35), "corte": ("tick", 0.3), "fundido": None, "desenfoque": None, "negro": ("impacto", 0.45), "zoom": ("zoom_whoosh", 0.4)}


def shot(t0, fondo, textos=(), extras=(), ent=("fundido", 0.5), grado=None, nombre=""):
    SHOTS.append(dict(t0=t0, fondo=fondo, textos=list(textos), extras=list(extras), ent=ent, grado=grado or {}, nombre=nombre))


def construir():
    SHOTS.sort(key=lambda d: d["t0"])
    for k, d in enumerate(SHOTS):
        d["t1"] = SHOTS[k + 1]["t0"] if k + 1 < len(SHOTS) else TOTAL + 1.0
        d["golpes"] = []
        sfx = SFX_TRANS.get(d["ent"][0])
        if sfx and k > 0:
            snd(d["t0"] - 0.04, sfx[0], sfx[1], **({"dur": 0.6} if sfx[0] in ("whoosh", "zoom_whoosh") else {}))


_SH = {}


def _sombra_inf():
    if "s" not in _SH:
        y = (np.arange(H, dtype=np.float32) / H - 0.56) / 0.44
        _SH["s"] = (1.0 - 0.52 * np.clip(y, 0, 1) ** 1.25)[:, None, None].astype(np.float32)
    return _SH["s"]


def dibujar(d, lz, t):
    tl = t - d["t0"]
    dur = d["t1"] - d["t0"] + 0.5
    d["fondo"](lz, tl, t, dur, 1.0)
    if d["textos"]:
        lz *= _sombra_inf()                      # sombra suave abajo: el texto principal se lee sobre cualquier imagen
    for e in d["extras"]:
        e(lz, t)
    for tx in d["textos"]:
        tx(lz, t)


# ------------------------------------------------------------------ tarjeta de créditos (final)
def CREDITOS(titulo, lineas, t0, t_fin=None):
    """Título serif amarillo + líneas pequeñas que aparecen escalonadas desde t0; se desvanecen en t_fin."""
    def f(lz, t):
        if t < t0:
            return
        o = 1 - (smooth(prog(t, t_fin, t_fin + 0.8)) if t_fin is not None else 0)
        pil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(pil)
        y = 230
        a0 = smooth(prog(t, t0, t0 + 0.7))
        d.text((W / 2, y), titulo, font=D.fuente("serif", 84), fill=(240, 245, 40, int(255 * a0 * o)), anchor="mm", stroke_width=2, stroke_fill=(10, 8, 6, 255))
        y += 150
        for k, ln in enumerate(lineas):
            a = smooth(prog(t, t0 + 0.9 + 0.35 * k, t0 + 1.5 + 0.35 * k)) * o
            d.text((W / 2, y), ln, font=D.fuente("sans_l", 31), fill=(236, 234, 228, int(255 * a)), anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0, int(255 * a)))
            y += 62
        a = np.asarray(pil, np.float32) / 255.0
        lz *= (1 - a[..., 3:4] * 0.0)
        lz[:] = lz * (1 - a[..., 3:4]) + a[..., :3] * a[..., 3:4]
    return f
