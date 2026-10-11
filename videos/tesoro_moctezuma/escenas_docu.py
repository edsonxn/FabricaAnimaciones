# -*- coding: utf-8 -*-
"""El tesoro perdido de Moctezuma — mini documental de misterio (estilo `documental`, ~6 min, 16:9).

Todo se dibuja en función del tiempo global (`Mundo`). Cada toma se declara con `shot(t0, fondo, textos, extras, ent, grado)`; el fin de una toma es
el inicio de la siguiente. Los tiempos salen de la voz (`w_(escena, frase, índice_de_palabra)`), así que nada queda desincronizado.
Lenguaje visual (copiado de voynich / "Detrás del Enigma"): texto principal en cursiva blanca con escaneo (`R`), nombres y cifras en serif amarillo (`S`, `N`),
preguntas serif + '?' rojo (`Q`), estampas rojas, trazos rectos rojos, polaroids sobre fondo borroso, corcho con hilo rojo, filtro de película (`X.cine`).
Piezas propias: barra de oro, sol de oro y luna de plata (sprites procedurales), reparto en quintos, barra que se hunde, infografía de bajas.
"""
import itertools
import math
import os

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
ORO = (0.95, 0.78, 0.25)


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


def _lin(n, maxw=4):
    """Reparte n palabras en líneas equilibradas de a lo sumo maxw."""
    k = max(1, -(-n // maxw))
    base, extra = divmod(n, k)
    return tuple(base + (1 if i < extra else 0) for i in range(k))


# ------------------------------------------------------------------ caché de sprites (una copia por proceso)
_C = {}


def spr(clave, fn):
    if clave not in _C:
        _C[clave] = fn()
    return _C[clave]


def pola(nombre, ancho=440, asp=1.05, foco=(0.5, 0.5), leyenda=None, lado=1600):
    return spr(("p", nombre, ancho, asp, foco, leyenda), lambda: D.polaroid(D.cargar(D.ruta_img(nombre), lado), ancho, asp, foco, leyenda=leyenda))


def lamina(nombre, alto=880, lado=2400):
    """Imagen como lámina de papel con sombra (para pinturas y grabados sobre fondo borroso)."""
    return spr(("l", nombre, alto), lambda: D.hoja_papel(D.cargar(D.ruta_img(nombre), lado), alto))


def corcho():
    return spr("corcho", lambda: D.Sprite(D.tablero(), None, sombra=False))


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


C0 = (1700, 1000)


def carta(lz, sp, M, t, t_in, x, y, rot=0.0, s=1.0, desde=(0, -420), dur=0.5, flota=1.0, fase=0.0, op=1.0, ry0=50.0, t_out=None):
    if t < t_in:
        return
    u = e_out(prog(t, t_in, t_in + dur))
    e = t - t_in
    asent = math.exp(-(e - dur) * 3.2) * math.sin((e - dur) * 15.0) * 2.0 if e > dur else 0.0
    fl = flota * 4.0 * math.sin(0.9 * t + fase)
    Mm = M @ D.poner(sp.w, sp.h, lerp(x + desde[0], x, u), lerp(y + desde[1], y, u) + fl, lerp(1.3, 1.0, u) * s, rot + asent + (1 - u) * 12, (1 - u) * ry0)
    o = op * smooth(prog(t, t_in, t_in + 0.15))
    if t_out is not None:
        o *= 1 - smooth(prog(t, t_out, t_out + 0.3))
    D.pegar(lz, sp, Mm, o)


# ------------------------------------------------------------------ texto (estilos del original)
def R(palabras, cx=W / 2, cy=H * 0.56, px=88, lineas=None, sal=None):
    """Texto principal: cursiva blanca en mayúsculas con líneas de escaneo, palabra a palabra."""
    if lineas is None and len(palabras) > 4:
        lineas = _lin(len(palabras))
    pal = X.rotulo(palabras, cx, cy, px, tuple(itertools.accumulate(lineas)) if lineas else None)

    def f(lz, t):
        X.dibujar_rotulo(lz, pal, t, px, salida=sal)
    return f


def S(palabras, cx=W / 2, cy=H * 0.55, px=98, lineas=None, sal=None):
    """Serif amarillo condensado, Título Con Mayúsculas (nombres, lugares, cifras)."""
    pal = X.serif_amarillo(palabras, cx, cy, px, tuple(itertools.accumulate(lineas)) if lineas else None)

    def f(lz, t):
        X.dibujar_serif(lz, pal, t, px, salida=sal)
    return f


def N(txt, cx, cy, px, t0, color=RJ, sal=None):
    def f(lz, t):
        D.numero(lz, txt, cx, cy, px, t, t0, color=color, fnt="abril_cond", salida=sal, pop=False)
    return f


def Q(lineas, t0, cx=W / 2, cy=H * 0.60, px=88, sal=None):
    def f(lz, t):
        X.pregunta_c(lz, lineas, t, t0, cx, cy, px, salida=sal)
    return f


def Qf(eid, fr, i0, i1, cx=W / 2, cy=H * 0.60, px=84, sal=None):
    """Pregunta con las palabras [i0:i1] de la frase, partidas en líneas."""
    p = pal_(eid, fr, i0, i1)
    ln, k = [], 0
    for n in _lin(len(p), 3):
        ln.append(p[k:k + n])
        k += n
    return Q(ln, p[0][1] - 0.1, cx, cy, px, sal)


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


def F_agua(t_ini=0.0):
    """Agua oscura vista desde arriba del fondo: degradado verde-azulado, rayos de luz y burbujas."""
    def f(lz, tl, t, dur, ext):
        lz[:] = _agua(t)
    return f


def HERO(nombre, x=960, y=500, rot=0.0, alto=880, t_in=0.0, ry=(-10, -3), desde=(0, 0), dur=0.55, t_out=None):
    """Pintura/grabado grande como lámina con cámara propia."""
    def f(lz, t):
        sp = lamina(nombre, alto)
        u = e_out(prog(t, t_in, t_in + dur))
        cam = D.Cam((1.0, W / 2, H / 2, 0.0), (1.08, W / 2, H / 2 + 10, 0.0), 3.0, mano=0.8)(t - t_in)
        o = smooth(prog(t, t_in, t_in + 0.2))
        if t_out is not None:
            o *= 1 - smooth(prog(t, t_out, t_out + 0.3))
        D.pegar(lz, sp, cam @ D.poner(sp.w, sp.h, lerp(x + desde[0], x, u), lerp(y + desde[1], y, u), lerp(0.9, 1.0, u), lerp(rot + 5, rot, u), lerp(ry[0], ry[1], u)), o)
    return f


# ------------------------------------------------------------------ sprites procedurales (oro, plata, agua)
def _poly(img, alfa, pts, c0, c1, y0, y1):
    m = np.zeros(img.shape[:2], np.uint8)
    cv2.fillPoly(m, [np.int32(pts)], 255, cv2.LINE_AA)
    ys = np.clip((np.arange(img.shape[0], dtype=np.float32)[:, None] - y0) / max(y1 - y0, 1), 0, 1)[..., None]
    col = np.float32(c0)[None, None, :] * (1 - ys) + np.float32(c1)[None, None, :] * ys
    mm = m > 0
    img[mm] = np.broadcast_to(col, img.shape)[mm]
    alfa[mm] = 1.0


def _barra_sp(w=560):
    """Lingote de oro (cara superior, frontal con brillo diagonal y bordes oscuros)."""
    S_ = 2
    w0, h0 = w * S_, int(w * 0.44) * S_
    img = np.zeros((h0, w0, 3), np.float32)
    al = np.zeros((h0, w0), np.float32)
    a, b = w0 * 0.14, h0 * 0.06
    top = [(a + w0 * 0.05, b), (w0 - a - w0 * 0.05, b), (w0 - a * 0.30, h0 * 0.44), (a * 0.30, h0 * 0.44)]
    fr = [(a * 0.30, h0 * 0.44), (w0 - a * 0.30, h0 * 0.44), (w0 - a * 0.05, h0 * 0.94), (a * 0.05, h0 * 0.94)]
    _poly(img, al, top, (255, 232, 140), (240, 196, 84), b, h0 * 0.44)
    _poly(img, al, fr, (226, 172, 44), (150, 96, 14), h0 * 0.44, h0 * 0.94)
    sh = np.zeros((h0, w0), np.float32)
    cv2.fillPoly(sh, [np.int32([(w0 * 0.20, h0 * 0.44), (w0 * 0.36, h0 * 0.44), (w0 * 0.30, h0 * 0.94), (w0 * 0.16, h0 * 0.94)])], 1.0, cv2.LINE_AA)
    sh = cv2.GaussianBlur(sh, (0, 0), 6) * al
    img = img * (1 - 0.35 * sh[..., None]) + 255 * 0.35 * sh[..., None]
    ed = np.zeros((h0, w0), np.uint8)
    cv2.polylines(ed, [np.int32(top), np.int32(fr)], True, 255, 5, cv2.LINE_AA)
    e = cv2.GaussianBlur(ed.astype(np.float32) / 255.0, (0, 0), 1.2)
    img = img * (1 - 0.55 * e[..., None]) + np.float32((90, 52, 6)) * 0.55 * e[..., None]
    img = cv2.resize(np.clip(img, 0, 255).astype(np.uint8), (w, h0 // S_), interpolation=cv2.INTER_AREA)
    al = cv2.resize(al, (w, h0 // S_), interpolation=cv2.INTER_AREA)
    return D.Sprite(img, al, sombra=True, sr=14, off=(8, 14), sop=0.6)


def barra_sp():
    return spr("barra", _barra_sp)


def _disco_sp(kind, d=520):
    S_ = 2
    n = d * S_
    c = n / 2
    img = np.zeros((n, n, 3), np.float32)
    al = np.zeros((n, n), np.float32)
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
    r = np.hypot(xx - c, yy - c)
    if kind == "oro":
        pts = []
        for k in range(48):
            ang = math.pi * 2 * k / 48
            rr = n * (0.49 if k % 2 == 0 else 0.385)
            pts.append((c + rr * math.cos(ang), c + rr * math.sin(ang)))
        m = np.zeros((n, n), np.uint8)
        cv2.fillPoly(m, [np.int32(pts)], 255, cv2.LINE_AA)
        c_in, c_out, R_ = np.float32((255, 236, 150)), np.float32((196, 130, 22)), n * 0.49
    else:
        m = np.zeros((n, n), np.uint8)
        cv2.circle(m, (int(c), int(c)), int(n * 0.47), 255, -1, cv2.LINE_AA)
        c_in, c_out, R_ = np.float32((240, 244, 250)), np.float32((120, 130, 146)), n * 0.47
    u = np.clip(r / R_, 0, 1)[..., None]
    lux = np.clip(1 - np.hypot(xx - c * 0.78, yy - c * 0.72) / (n * 0.7), 0, 1)[..., None]
    img[:] = c_in * (1 - u) + c_out * u
    img = img * (0.72 + 0.4 * lux)
    ring = np.zeros((n, n), np.float32)
    for rr in ((0.30, 0.20, 0.10) if kind == "oro" else (0.36,)):
        cv2.circle(ring, (int(c), int(c)), int(n * rr), 1.0, 5, cv2.LINE_AA)
    if kind == "oro":
        for k in range(24):
            ang = math.pi * 2 * k / 24
            cv2.line(ring, (int(c + n * 0.12 * math.cos(ang)), int(c + n * 0.12 * math.sin(ang))),
                     (int(c + n * 0.30 * math.cos(ang)), int(c + n * 0.30 * math.sin(ang))), 1.0, 4, cv2.LINE_AA)
    else:
        for (dx, dy, rr) in ((-0.13, -0.10, 0.07), (0.12, 0.05, 0.10), (-0.02, 0.20, 0.055), (0.16, -0.17, 0.045)):
            cv2.circle(ring, (int(c + n * dx), int(c + n * dy)), int(n * rr), 1.0, 5, cv2.LINE_AA)
    ring = cv2.GaussianBlur(ring, (0, 0), 1.6)
    img = img * (1 - 0.32 * ring[..., None])
    al = cv2.GaussianBlur(m.astype(np.float32) / 255.0, (0, 0), 1.0)
    img = cv2.resize(np.clip(img, 0, 255).astype(np.uint8), (d, d), interpolation=cv2.INTER_AREA)
    al = cv2.resize(al, (d, d), interpolation=cv2.INTER_AREA)
    return D.Sprite(img, al, sombra=True, sr=16, off=(8, 14), sop=0.6)


def disco_sp(kind):
    return spr(("disco", kind), lambda: _disco_sp(kind))


def _agua(t):
    """Fondo submarino oscuro: degradado, rayos que ondulan y burbujas que suben."""
    g = spr("agua_g", lambda: _agua_base())
    img = g.copy()
    xs = np.linspace(0, 1, W, dtype=np.float32)[None, :]
    ys = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    ray = (np.sin(xs * 23.0 + t * 0.7 + np.sin(xs * 7.0 + t * 0.4) * 2.0) * 0.5 + 0.5) ** 3
    ray = ray * (1 - ys) ** 1.6 * (np.sin(xs * 5.3 - t * 0.35) * 0.5 + 0.5)
    img += ray[..., None] * np.float32((0.05, 0.16, 0.16))
    for k in range(26):
        ph = (t * (0.11 + 0.05 * (k % 5)) + k * 0.137) % 1.0
        x = (0.06 + 0.88 * ((k * 0.6180339) % 1.0)) * W + 22 * math.sin(t * 1.3 + k)
        y = H * (1.05 - ph * 1.15)
        cv2.circle(img, (int(x), int(y)), 3 + (k % 4) * 2, (0.35, 0.65, 0.68), 1, cv2.LINE_AA)
    return np.clip(img, 0, 1)


def _agua_base():
    ys = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    a, b = np.float32((0.06, 0.30, 0.34)), np.float32((0.005, 0.03, 0.05))
    return np.repeat(a * (1 - ys) + b * ys, W, axis=1).astype(np.float32)


def _brillo_oro(lz, t, cx, cy, r, k):
    g = spr("glow", lambda: _glow_map())
    s = max(int(2 * r), 16)
    m = cv2.resize(g, (s, s), interpolation=cv2.INTER_LINEAR)
    x0, y0 = int(cx - s / 2), int(cy - s / 2)
    xa, ya, xb, yb = max(x0, 0), max(y0, 0), min(x0 + s, W), min(y0 + s, H)
    if xb <= xa or yb <= ya:
        return
    lz[ya:yb, xa:xb] += m[ya - y0:yb - y0, xa - x0:xb - x0, None] * np.float32(ORO) * k


def _glow_map(n=256):
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
    r = np.hypot(xx - n / 2, yy - n / 2) / (n / 2)
    return np.clip(1 - r, 0, 1) ** 2.2


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


def CARTA(sp_fn, t_in, x, y, rot=0.0, desde=(0, -420), dur=0.55, s=1.0, t_out=None):
    """Extra: lámina/polaroid que cae y se asienta (con sonido de papel)."""
    snd(t_in, "papel", 0.4)
    return lambda lz, t: carta(lz, sp_fn(), I3, t, t_in, x, y, rot, s, desde=desde, dur=dur, t_out=t_out)


def TAG(txt, x, y, t0, px=44, rot=-3.0, sal=None):
    return lambda lz, t: D.tag_nombre(lz, txt, x, y, t, t0, px, rot, salida=sal)


def EST(txt, x, y, t0, px=100, rot=-7.0, snd_=True):
    if snd_:
        snd(t0, "sello", 0.7)
    return lambda lz, t: D.estampa(lz, txt, x, y, t, t0, px, rot=rot)


def TRAZO(p0, p1, t0, w=24, dur=0.6):
    snd(t0, "garabato", 0.4, dur=0.5)
    return lambda lz, t: X.trazo_recto(lz, p0, p1, 0.0, e_out(prog(t, t0, t0 + dur)), w)


# ---------------------------------------------------------------- GANCHO
G = "gancho"
shot(0.0, F_clip("lluvia_noche", inicio=2.0, z0=1.0, z1=1.2, tono=(0.75, 0.82, 0.95)),
     [S([("Junio", w_(G, 0, 3)), ("1520", w_(G, 0, 7))], W / 2, 500, 200, lineas=(1,), sal=w_(G, 0, 8) + 0.4)], ent=("fundido", 0.01))
shot(w_(G, 0, 8) - 0.05, F_foto("noche_triste", z0=1.05, z1=1.25, c0=(0.42, 0.5), c1=(0.6, 0.45), par=(60, 8), tono=(0.85, 0.85, 0.9)),
     [R(pal_(G, 0, 12, 20), W / 2, 850, 78)], ent=("tinta", 0.7), grado=dict(vineta=0.8))
shot(INI(G, 1) - 0.05, F_clip("joyas", inicio=2.0, z0=1.05, z1=1.25, tono=(1.0, 0.85, 0.65)),
     [S([("Oro", w_(G, 1, 5)), ("Joyas", w_(G, 1, 6)), ("Plumas", w_(G, 1, 8))], W / 2, 850, 130, lineas=(3,))], ent=("fundido", 0.5))
shot(w_(G, 2, 0) - 0.1, F_clip("lago", inicio=1.0, z0=1.02, z1=1.2, tono=(0.7, 0.75, 0.85)),
     [R(pal_(G, 2, 1, 6), W / 2, 850, 84)], ent=("fuga", 0.7), grado=dict(vineta=0.85))
shot(w_(G, 2, 6) - 0.1, F_clip("humo", inicio=3.0, z0=1.05, z1=1.3, tono=(0.7, 0.72, 0.8)),
     [Qf(G, 2, 6, 14, W / 2, 560, 88)], ent=("tinta", 0.7), grado=dict(vineta=0.9))
snd(0.2, "latido", 0.7, dur=1.6)
snd(0.4, "lluvia", 0.5, dur=3.0)
snd(3.4, "lluvia", 0.45, dur=3.0)
snd(w_(G, 2, 6), "impacto", 0.6)

# ---------------------------------------------------------------- LLEGADA
L = "llegada"
shot(INI(L, 0) - 0.05, F_foto("mapa_1524", z0=1.05, z1=1.35, c0=(0.72, 0.5), c1=(0.72, 0.52), par=(0, 0), lado=3800, tono=(0.85, 0.8, 0.7)),
     [S([("Noviembre", w_(L, 0, 1)), ("1519", w_(L, 0, 3))], 460, 250, 130, lineas=(2,))], ent=("tinta", 0.7))
shot(w_(L, 0, 5) + 0.05, F_borroso("cortes", 0.32), [], [CARTA(lambda: pola("cortes", 560, 1.18, (0.5, 0.35)), w_(L, 0, 6) - 0.1, 620, 470, -3, desde=(-700, 0)),
                                                       TAG("Hernán Cortés", 640, 900, w_(L, 0, 6), 50)], ent=("fuga", 0.7))
shot(w_(L, 0, 9) - 0.1, F_foto("rivera_mercado", z0=1.05, z1=1.3, c0=(0.5, 0.55), c1=(0.55, 0.5), par=(70, 10), tono=(0.95, 0.92, 0.85)),
     [S([("Tenochtitlan", w_(L, 0, 10))], 500, 220, 130, lineas=(1,)), R(pal_(L, 0, 11, 16), W / 2, 880, 70)], ent=("fundido", 0.6))
shot(INI(L, 1) - 0.05, F_foto("encuentro", z0=1.05, z1=1.3, c0=(0.4, 0.5), c1=(0.55, 0.55), par=(60, 8), tono=(0.9, 0.88, 0.85)),
     [R(pal_(L, 1, 0, 5), W / 2, 880, 74)], ent=("tinta", 0.7))
shot(w_(L, 1, 6) - 0.1, F_borroso("moctezuma_valle", 0.32), [S([("Palacio", w_(L, 1, 8)), ("Del", w_(L, 1, 9)), ("Padre", w_(L, 1, 11))], 1260, 180, 96, lineas=(1,))],
     [CARTA(lambda: pola("moctezuma_valle", 640, 0.72, (0.55, 0.5), "Moctezuma II"), w_(L, 1, 6) - 0.05, 700, 470, 3, desde=(0, -500))], ent=("fundido", 0.5))

shot(INI(L, 2) - 0.05, F_clip("joyas2", inicio=4.0, z0=1.05, z1=1.3, tono=(1.0, 0.85, 0.7)),
     [R(pal_(L, 2, 0, 4), W / 2, 850, 84)], ent=("fuga", 0.7))
shot(w_(L, 2, 11) - 0.05, F_clip("monedas2", inicio=2.0, z0=1.05, z1=1.3, tono=(0.85, 0.7, 0.55)),
     [R(pal_(L, 2, 11, 18), W / 2, 830, 76)], ent=("fundido", 0.5), grado=dict(vineta=0.85))

# ---------------------------------------------------------------- PUERTA
P = "puerta"
shot(INI(P, 0) - 0.05, F_foto("templo_mayor", z0=1.7, z1=1.35, c0=(0.3, 0.8), c1=(0.45, 0.7), par=(0, 0), tono=(0.42, 0.36, 0.32)),
     [R(pal_(P, 0, 6, 14), W / 2, 830, 84)], ent=("tinta", 0.7), grado=dict(vineta=0.85))
shot(INI(P, 1) - 0.05, F_borroso("bernal_portada", 0.30), [S([("Bernal", w_(P, 1, 3)), ("Díaz", w_(P, 1, 4)), ("Del", w_(P, 1, 5)), ("Castillo", w_(P, 1, 6))], 1290, 560, 100, lineas=(2, 2))],
     [CARTA(lambda: pola("bernal_portada", 520, 1.36, (0.5, 0.32), "Historia verdadera, 1632"), INI(P, 1) + 0.05, 600, 480, -4, desde=(-700, 0))], ent=("fuga", 0.7))
snd(w_(P, 1, 7), "impacto", 0.7)
shot(w_(P, 1, 7) - 0.05, F_foto("templo_mayor", z0=1.9, z1=1.5, c0=(0.62, 0.78), c1=(0.6, 0.72), par=(0, 0), tono=(0.6, 0.52, 0.45)),
     [R(pal_(P, 1, 7, 11), W / 2, 830, 90)], ent=("zoom", 0.3), grado=dict(polvo=0.5))
shot(w_(P, 1, 12) - 0.05, F_clip("joyas", inicio=6.0, z0=1.05, z1=1.3, tono=(1.0, 0.85, 0.65)),
     [S([("Oro", w_(P, 1, 16)), ("Jade", w_(P, 1, 17)), ("Piedras Preciosas", w_(P, 1, 19))], W / 2, 860, 104, lineas=(3,))], ent=("destello", 0.5))
snd(w_(P, 1, 16), "bling", 0.5)
shot(INI(P, 2) - 0.05, F_foto("moctezuma_duran", z0=1.02, z1=1.25, c0=(0.5, 0.5), c1=(0.6, 0.45), par=(0, 0), tono=(0.75, 0.68, 0.6)),
     [R(pal_(P, 2, 5, 10), W / 2, 850, 80)], [TAG("Códice Durán · Moctezuma II", 1480, 300, INI(P, 2) + 0.3, 40)], ent=("fundido", 0.6))

# ---------------------------------------------------------------- VALOR (jade y plumas valían más que el oro)
Va = "valor"
shot(INI(Va, 0) - 0.05, F_clip("joyas", inicio=10.0, z0=1.05, z1=1.25, tono=(1.0, 0.85, 0.65)),
     [R(pal_(Va, 0, 4, 11), W / 2, 850, 78)], ent=("tinta", 0.7))
shot(INI(Va, 1) - 0.05, F_foto("moctezuma_valle", z0=1.05, z1=1.3, c0=(0.45, 0.5), c1=(0.55, 0.45), par=(60, 8), tono=(0.95, 0.92, 0.88)),
     [S([("Jade", w_(Va, 1, 3)), ("Plumas", w_(Va, 1, 6)), ("De", w_(Va, 1, 7)), ("Quetzal", w_(Va, 1, 8))], 540, 220, 110, lineas=(1, 3))], [TAG("Materiales reservados a la élite", 560, 950, w_(Va, 1, 9), 42)], ent=("fuga", 0.7))
shot(INI(Va, 2) - 0.05, F_pozo(0.5, 0.5, 0.9, (0.28, 0.20, 0.08)),
     [R(pal_(Va, 2, 3, 8), W / 2, 780, 88)], [CARTA(lambda: spr("disco_oro_v", lambda: disco_sp("oro")), INI(Va, 2) + 0.05, W / 2, 400, 0, desde=(0, -500), s=0.8),
                                            TAG("Náhuatl: teocuitlatl", 960, 900, w_(Va, 2, 3) + 0.2, 42)], ent=("fundido", 0.5))
shot(INI(Va, 3) - 0.05, F_clip("monedas2", inicio=6.0, z0=1.05, z1=1.3, tono=(0.8, 0.65, 0.5)),
     [R(pal_(Va, 3, 4, 9), W / 2, 830, 86)], ent=("tinta", 0.7), grado=dict(vineta=0.85))
snd(INI(Va, 3) + 0.4, "fuego", 0.35, dur=2.5)

# ---------------------------------------------------------------- DURERO
Dr = "durero"
shot(INI(Dr, 0) - 0.05, F_borroso("carlos_v", 0.30), [R(pal_(Dr, 0, 8, 12), 1290, 470, 72, lineas=(2, 2))],
     [CARTA(lambda: pola("carlos_v", 520, 1.34, (0.5, 0.3), "Carlos V"), INI(Dr, 0) + 0.05, 560, 480, 3, desde=(-700, 0)),
      TAG("El rey", 590, 940, w_(Dr, 0, 6), 46)], ent=("tinta", 0.7))
shot(INI(Dr, 1) - 0.05, F_clip("vela2", inicio=1.0, z0=1.05, z1=1.25, tono=(1.0, 0.85, 0.7)),
     [S([("Bruselas", w_(Dr, 1, 12)), ("1520", w_(Dr, 1, 12) + 0.25)], 1300, 250, 130, lineas=(1,))],
     [CARTA(lambda: pola("durero", 520, 1.34, (0.5, 0.3)), w_(Dr, 1, 4) - 0.1, 560, 480, -3, desde=(-700, 0)),
      TAG("Alberto Durero", 560, 940, w_(Dr, 1, 7), 48)], ent=("fuga", 0.7))


def _sol_luna(lz, t):
    ts, tl_ = w_(Dr, 2, 2) - 0.15, w_(Dr, 2, 7) - 0.15
    for tt, kind, x, ley in ((ts, "oro", 600, "Sol de oro"), (tl_, "plata", 1320, "Luna de plata")):
        if t < tt:
            continue
        u = e_back(prog(t, tt, tt + 0.6))
        rot = (t - tt) * (8 if kind == "oro" else -5)
        sp = disco_sp(kind)
        _brillo_oro(lz, t, x, 470, 420, 0.28 * smooth(prog(t, tt, tt + 0.5)) if kind == "oro" else 0.0)
        D.pegar(lz, sp, D.poner(sp.w, sp.h, x, 470 + 5 * math.sin(t * 1.1 + x), max(u, 0.01) * 0.95, rot), smooth(prog(t, tt, tt + 0.2)))
        D.tag_nombre(lz, ley, x, 850, t, tt + 0.5, 46)


shot(w_(Dr, 2, 0) - 0.05, F_pozo(0.5, 0.5, 0.95, (0.26, 0.18, 0.08)), [], [_sol_luna], ent=("fundido", 0.5))
snd(w_(Dr, 2, 2), "brillo", 0.5)
snd(w_(Dr, 2, 7), "brillo", 0.4)
shot(w_(Dr, 2, 14) - 0.1, F_clip("biblioteca", inicio=4.0, z0=1.05, z1=1.25, tono=(0.9, 0.78, 0.62), sat=0.6),
     [R(pal_(Dr, 2, 15, 26), W / 2, 780, 66, lineas=(3, 3, 3, 2))], [TAG("Diario de Durero, 1520", 1480, 250, w_(Dr, 2, 14) + 0.2, 40)], ent=("tinta", 0.7))

# ---------------------------------------------------------------- FUNDICIÓN
Fu = "fundicion"
shot(INI(Fu, 0) - 0.05, F_clip("joyas2", inicio=1.0, z0=1.05, z1=1.25, tono=(1.0, 0.85, 0.7)),
     [R(pal_(Fu, 0, 3, 8), W / 2, 850, 82)], ent=("fuga", 0.7))
shot(INI(Fu, 1) - 0.05, F_clip("antorcha", inicio=4.0, z0=1.2, z1=1.6, c0=(0.5, 0.6), c1=(0.5, 0.55), tono=(1.0, 0.8, 0.6)),
     [R(pal_(Fu, 1, 0, 3), W / 2, 500, 96, lineas=(1, 2))], ent=("tinta", 0.7), grado=dict(vineta=0.85))
snd(INI(Fu, 1) + 0.2, "fuego", 0.4, dur=3.0)


def _reparto(lz, t):
    ti = [w_(Fu, 1, 3), w_(Fu, 1, 3) + 0.22, w_(Fu, 1, 3) + 0.44, w_(Fu, 1, 3) + 0.66, w_(Fu, 1, 3) + 0.88]
    sp = barra_sp()
    x0 = 960 - 2 * 320
    lev = [w_(Fu, 1, 5), w_(Fu, 1, 10), w_(Fu, 1, 14), w_(Fu, 1, 14), w_(Fu, 1, 14)]
    for k in range(5):
        if t < ti[k]:
            continue
        u = e_back(prog(t, ti[k], ti[k] + 0.4))
        dy = -34 * smooth(prog(t, lev[k], lev[k] + 0.3))
        D.pegar(lz, sp, D.poner(sp.w, sp.h, x0 + 320 * k, 470 + dy - (1 - u) * 300, 0.52 * max(u, 0.01) ** 0.2, -2 + 4 * (k % 2)), smooth(prog(t, ti[k], ti[k] + 0.15)))
    for txt, x, t0 in (("Rey · 1/5", x0, w_(Fu, 1, 6)), ("Cortés · 1/5", x0 + 320, w_(Fu, 1, 10)), ("Soldados · el resto", x0 + 640 + 320, w_(Fu, 1, 15))):
        D.tag_nombre(lz, txt, x, 720, t, t0, 40)


for k in range(5):
    snd(w_(Fu, 1, 3) + 0.22 * k, "clink", 0.5, tono=0.9 + 0.08 * k)
shot(w_(Fu, 1, 3) - 0.1, F_pozo(0.5, 0.5, 0.9, (0.22, 0.15, 0.08)), [], [_reparto], ent=("fundido", 0.5))
shot(INI(Fu, 2) - 0.05, F_clip("monedas2", inicio=3.0, z0=1.05, z1=1.25, tono=(0.7, 0.62, 0.55)),
     [R(pal_(Fu, 2, 0, 9), W / 2, 830, 74)], [EST("Todo fundido", 1280, 400, w_(Fu, 2, 7), 120)], ent=("tinta", 0.7))

# ---------------------------------------------------------------- MATANZA (Toxcatl)
Mz = "matanza"
shot(INI(Mz, 0) - 0.05, F_foto("mapa_1524", z0=1.05, z1=1.5, c0=(0.25, 0.5), c1=(0.2, 0.5), par=(0, 0), lado=3800, tono=(0.8, 0.75, 0.68)),
     [R(pal_(Mz, 0, 1, 6), W / 2, 850, 84)], ent=("tinta", 0.7))
shot(w_(Mz, 0, 11) - 0.05, F_clip("mapa_vela", inicio=1.0, z0=1.05, z1=1.3, tono=(1.0, 0.85, 0.7)),
     [S([("Pedro", w_(Mz, 0, 16)), ("De", w_(Mz, 0, 17)), ("Alvarado", w_(Mz, 0, 18))], 560, 250, 110, lineas=(3,))], [TAG("Queda al mando", 620, 940, w_(Mz, 0, 12), 42)], ent=("fundido", 0.5))
shot(INI(Mz, 1) - 0.05, F_foto("templo_mayor", z0=1.05, z1=1.25, c0=(0.5, 0.6), c1=(0.6, 0.55), par=(60, 8), tono=(0.7, 0.66, 0.66)),
     [S([("Mayo", w_(Mz, 1, 1)), ("1520", w_(Mz, 1, 4))], 480, 220, 130, lineas=(2,), sal=w_(Mz, 1, 9) + 0.3)], [TAG("Fiesta de Tóxcatl · Templo Mayor", 500, 940, w_(Mz, 1, 6), 40)], ent=("tinta", 0.7), grado=dict(vineta=0.85))
shot(w_(Mz, 1, 10) - 0.05, F_foto("orozco_noche", z0=1.05, z1=1.3, c0=(0.55, 0.5), c1=(0.4, 0.5), par=(50, 6), tono=(0.95, 0.6, 0.55)),
     [R(pal_(Mz, 1, 10, 15), W / 2, 830, 84)], ent=("zoom", 0.3), grado=dict(vineta=0.85))
snd(w_(Mz, 1, 10), "impacto", 0.6)
shot(w_(Mz, 1, 15) - 0.05, F_foto("moctezuma_valle", z0=1.05, z1=1.3, c0=(0.5, 0.55), c1=(0.45, 0.5), par=(60, 8), tono=(0.6, 0.55, 0.55)),
     [R(pal_(Mz, 1, 15, 22), W / 2, 850, 70)], ent=("fundido", 0.5), grado=dict(vineta=0.85))
shot(INI(Mz, 2) - 0.05, F_foto("noche_triste", z0=1.05, z1=1.3, c0=(0.6, 0.5), c1=(0.45, 0.5), par=(60, 8), tono=(1.0, 0.7, 0.6)),
     [R(pal_(Mz, 2, 0, 5), W / 2, 830, 90)], ent=("aberracion", 0.5), grado=dict(vineta=0.85))
shot(w_(Mz, 2, 5) - 0.05, F_foto("rivera_mercado", z0=1.05, z1=1.3, c0=(0.5, 0.55), c1=(0.45, 0.5), par=(60, 8), tono=(0.55, 0.5, 0.5)),
     [R(pal_(Mz, 2, 8, 16), W / 2, 850, 68)], ent=("tinta", 0.7), grado=dict(vineta=0.85))
snd(INI(Mz, 2), "latido", 0.5, dur=1.2)

# ---------------------------------------------------------------- MUERTE
Mu = "muerte"
shot(INI(Mu, 0) - 0.05, F_foto("moctezuma_valle", z0=1.05, z1=1.25, c0=(0.55, 0.5), c1=(0.5, 0.55), par=(60, 8), tono=(0.9, 0.86, 0.8)),
     [S([("Moctezuma", w_(Mu, 0, 0)), ("II", w_(Mu, 0, 0) + 0.3)], 520, 220, 110, lineas=(2,)), R(pal_(Mu, 0, 6, 11), W / 2, 880, 74)], ent=("tinta", 0.7))
shot(INI(Mu, 1) - 0.05, F_borroso("moctezuma_duran", 0.30), [Qf(Mu, 1, 4, 10, W / 2, 900, 62)],
     [CARTA(lambda: pola("moctezuma_duran", 640, 0.66, (0.5, 0.5), "Moctezuma II"), INI(Mu, 1) + 0.05, W / 2, 400, 0, desde=(0, -600))], ent=("fundido", 0.5))
shot(w_(Mu, 1, 10) - 0.1, F_borroso("cortes", 0.28), [],
     [CARTA(lambda: pola("cortes", 460, 1.25, (0.5, 0.3), "Versión española"), w_(Mu, 1, 10) - 0.05, 560, 470, -3, desde=(-700, 0)),
      TAG("«Lo apedrearon los mexicas»", 570, 920, w_(Mu, 1, 12), 40),
      CARTA(lambda: pola("moctezuma_duran", 560, 0.85, (0.5, 0.5), "Fuentes indígenas"), w_(Mu, 1, 17) - 0.05, 1360, 470, 3, desde=(700, 0)),
      TAG("«Lo mataron los españoles»", 1350, 920, w_(Mu, 1, 20), 40)], ent=("tinta", 0.6))
shot(INI(Mu, 2) - 0.05, F_foto("tenochtitlan_1521", z0=1.05, z1=1.3, c0=(0.5, 0.5), c1=(0.45, 0.42), par=(0, 0), tono=(0.75, 0.68, 0.6)),
     [R(pal_(Mu, 2, 0, 6), W / 2, 820, 82)], ent=("fuga", 0.7))
shot(w_(Mu, 2, 6) - 0.1, F_foto("orozco_noche", z0=1.05, z1=1.25, c0=(0.4, 0.5), c1=(0.6, 0.5), par=(40, 6), tono=(0.75, 0.7, 0.7)),
     [R(pal_(Mu, 2, 6, 10), W / 2, 850, 92)], ent=("aberracion", 0.5), grado=dict(vineta=0.85))
snd(INI(Mu, 1), "latido", 0.5, dur=1.2)

# ---------------------------------------------------------------- ANTES DE LA HUIDA
Ah = "antes_huida"
shot(INI(Ah, 0) - 0.05, F_foto("encuentro", z0=1.1, z1=1.35, c0=(0.6, 0.55), c1=(0.45, 0.55), par=(50, 6), tono=(0.8, 0.72, 0.65)),
     [R(pal_(Ah, 0, 3, 12), W / 2, 850, 76)], ent=("tinta", 0.7), grado=dict(vineta=0.85))
shot(w_(Ah, 0, 12) - 0.05, F_clip("joyas", inicio=3.0, z0=1.05, z1=1.3, tono=(0.85, 0.72, 0.6)),
     [R(pal_(Ah, 0, 12, 17), W / 2, 830, 84)], ent=("fundido", 0.5), grado=dict(vineta=0.85))
shot(INI(Ah, 1) - 0.05, F_clip("joyas2", inicio=0.5, z0=1.1, z1=1.35, c0=(0.4, 0.5), c1=(0.6, 0.5), tono=(0.95, 0.8, 0.62)),
     [S(pal_(Ah, 1, 7, 11), W / 2, 430, 100, lineas=(2, 2)), R(pal_(Ah, 1, 5, 7), W / 2, 850, 70)], ent=("fuga", 0.7), grado=dict(vineta=0.8))
snd(INI(Ah, 1) + 0.5, "clink", 0.45)
shot(INI(Ah, 2) - 0.05, F_clip("lluvia_noche", inicio=1.0, z0=1.0, z1=1.25, tono=(0.65, 0.72, 0.9)),
     [R(pal_(Ah, 2, 4, 11), W / 2, 850, 80)], ent=("fundido", 0.5), grado=dict(vineta=0.9))
snd(INI(Ah, 2), "lluvia", 0.4, dur=3.0)

# ---------------------------------------------------------------- NOCHE TRISTE
Nn = "noche"
shot(INI(Nn, 0) - 0.05, F_clip("lluvia_noche", inicio=5.0, z0=1.0, z1=1.25, tono=(0.7, 0.78, 0.95)),
     [S([("30", w_(Nn, 0, 3)), ("De", w_(Nn, 0, 4)), ("Junio", w_(Nn, 0, 5)), ("1520", w_(Nn, 0, 5) + 0.3)], W / 2, 330, 150, lineas=(4,), sal=w_(Nn, 0, 9))],
     ent=("negro", 0.5), grado=dict(vineta=0.9))
shot(w_(Nn, 0, 9) - 0.05, F_foto("mapa_1524", z0=1.0, z1=1.5, c0=(0.72, 0.5), c1=(0.6, 0.5), par=(0, 0), lado=3800, tono=(0.55, 0.55, 0.6)),
     [R(pal_(Nn, 0, 12, 17), W / 2, 880, 78)], [TAG("Tenochtitlan, 1524", 480, 250, w_(Nn, 0, 9) + 0.3, 42)], ent=("tinta", 0.7), grado=dict(vineta=0.85))
shot(INI(Nn, 1) - 0.05, F_foto("noche_triste", z0=1.05, z1=1.3, c0=(0.5, 0.5), c1=(0.35, 0.55), par=(80, 10), tono=(0.9, 0.9, 0.95)),
     [R(pal_(Nn, 1, 0, 3), W / 2, 850, 96)], ent=("aberracion", 0.5), grado=dict(vineta=0.75))
shot(w_(Nn, 1, 3) - 0.05, F_foto("orozco_noche", z0=1.05, z1=1.3, c0=(0.6, 0.5), c1=(0.4, 0.5), par=(50, 6), tono=(0.85, 0.8, 0.8)),
     [R(pal_(Nn, 1, 3, 10), W / 2, 850, 78)], ent=("glitch", 0.35), grado=dict(vineta=0.8))
shot(INI(Nn, 2) - 0.05, F_clip("joyas", inicio=9.0, z0=1.05, z1=1.3, tono=(0.85, 0.7, 0.58)),
     [R(pal_(Nn, 2, 0, 5), W / 2, 830, 84)], ent=("fuga", 0.7), grado=dict(vineta=0.85))
shot(w_(Nn, 2, 5) - 0.05, F_clip("gotas", inicio=1.0, z0=1.05, z1=1.3, tono=(0.6, 0.7, 0.85)),
     [R(pal_(Nn, 2, 5, 11), W / 2, 830, 84)], ent=("fundido", 0.4), grado=dict(vineta=0.9))


def _hundir(lz, t):
    t0 = INI(Nn, 3) - 0.1
    if t < t0:
        return
    sp = barra_sp()
    e = t - t0
    y = lerp(-140, 760, e_out(prog(e, 0, 5.0))) + 8 * math.sin(e * 2.0)
    rot = 20 * math.sin(e * 0.9) - 10 + e * 5
    o = 1 - 0.55 * smooth(prog(e, 2.0, 5.0))
    D.pegar(lz, sp, D.poner(sp.w, sp.h, 860 + 60 * math.sin(e * 0.7), y, 0.9 - 0.25 * smooth(prog(e, 0, 5.0)), rot, 35 * math.sin(e * 0.8)), o)
    y2 = lerp(-360, 820, e_out(prog(e - 0.5, 0, 5.2)))
    D.pegar(lz, sp, D.poner(sp.w, sp.h, 1220 + 40 * math.sin(e * 0.5 + 1), y2, 0.6, -25 + e * 7, 30 * math.cos(e * 0.6)), 0.7 * o)


snd(w_(Nn, 3, 1), "chapuzon", 0.7)
snd(w_(Nn, 3, 3), "burbujas", 0.5)
snd(w_(Nn, 3, 5), "clink", 0.35, tono=0.7)
shot(INI(Nn, 3) - 0.1, F_agua(), [R(pal_(Nn, 3, 4, 9), W / 2, 880, 84)], [_hundir], ent=("fundido", 0.4), grado=dict(vineta=0.85))
for tt in (0.4, INI(Nn, 0) + 0.2, INI(Nn, 0) + 3.2, INI(Nn, 1) + 0.2, INI(Nn, 1) + 3.2, INI(Nn, 2) + 0.2):
    snd(tt, "lluvia", 0.4, dur=3.0)
snd(INI(Nn, 1) + 0.6, "impacto", 0.7)
snd(w_(Nn, 1, 3), "pasos", 0.4, dur=1.4)

# ---------------------------------------------------------------- BAJAS
B = "bajas"


def _cifras(lz, t):
    t0 = w_(B, 0, 0)
    for txt, x, ta, ley, sub in (("154", 380, w_(B, 0, 2), "Según Cortés", "españoles"), ("450+", 960, w_(B, 0, 12), "Según otros cronistas", "españoles"),
                                 ("1 000 – 4 000", 1540, w_(B, 0, 19), "Según los cronistas", "aliados indígenas")):
        D.numero(lz, txt, x, 470, 190 if len(txt) < 6 else 108, t, ta - 0.05, color=RJ if "154" in txt else AM, fnt="abril_cond", pop=False)
        D.tag_nombre(lz, ley, x, 620, t, ta + 0.2, 36)
        D.tag_nombre(lz, sub, x, 700, t, ta + 0.35, 36)


shot(INI(B, 0) - 0.05, F_foto("orozco_noche", z0=1.15, z1=1.35, c0=(0.5, 0.45), c1=(0.55, 0.55), par=(30, 4), tono=(0.32, 0.30, 0.30)),
     [R(pal_(B, 0, 6, 8), W / 2, 900, 80)], [_cifras], ent=("tinta", 0.7), grado=dict(vineta=0.9))
for i in (2, 12, 19):
    snd(w_(B, 0, i), "ding", 0.3)
shot(INI(B, 1) - 0.05, F_foto("noche_triste", z0=1.05, z1=1.3, c0=(0.6, 0.5), c1=(0.4, 0.55), par=(60, 8), tono=(0.75, 0.75, 0.8)),
     [R(pal_(B, 1, 3, 9), W / 2, 850, 76)], [EST("Perdido", 1340, 330, w_(B, 1, 12), 130)], ent=("fuga", 0.7), grado=dict(vineta=0.85))

shot(INI(B, 2) - 0.05, F_clip("lago", inicio=6.0, z0=1.05, z1=1.3, tono=(0.75, 0.68, 0.7)),
     [R(pal_(B, 2, 6, 16), W / 2, 830, 72)],
     [TAG("Según la tradición", 480, 250, INI(B, 2) + 0.2, 42)], ent=("fundido", 0.6), grado=dict(vineta=0.9))

# ---------------------------------------------------------------- REGRESO (Tlaxcala, viruela, bergantines)
Rg = "regreso"
shot(INI(Rg, 0) - 0.05, F_borroso("tlaxcala", 0.34), [R(pal_(Rg, 0, 3, 12), W / 2, 880, 68)],
     [CARTA(lambda: lamina("tlaxcala", 520), INI(Rg, 0) + 0.05, W / 2, 400, -2, desde=(0, -600)), TAG("Lienzo de Tlaxcala", 960, 720, w_(Rg, 0, 5), 42)], ent=("tinta", 0.7))
shot(INI(Rg, 1) - 0.05, F_clip("humo", inicio=6.0, z0=1.05, z1=1.3, tono=(1.6, 1.6, 1.5)),
     [S([("Viruela", w_(Rg, 1, 3))], 560, 250, 140, lineas=(1,)), R(pal_(Rg, 1, 4, 11), W / 2, 850, 76)], ent=("fuga", 0.7), grado=dict(vineta=0.9))
shot(INI(Rg, 2) - 0.05, F_foto("mapa_1524", z0=1.0, z1=1.35, c0=(0.6, 0.5), c1=(0.75, 0.5), par=(0, 0), lado=3800, tono=(0.8, 0.78, 0.72)),
     [S([("Mayo", w_(Rg, 2, 1)), ("1521", w_(Rg, 2, 5))], 460, 220, 120, lineas=(2,)), N("13", 1500, 300, 280, w_(Rg, 2, 13) - 0.05, color=AM), R(pal_(Rg, 2, 15, 19), W / 2, 880, 72)],
     [TAG("bergantines", 1500, 470, w_(Rg, 2, 14), 44)], ent=("tinta", 0.7))
snd(w_(Rg, 2, 13), "ding", 0.35)
shot(INI(Rg, 3) - 0.05, F_foto("tenochtitlan_1521", z0=1.05, z1=1.3, c0=(0.5, 0.5), c1=(0.45, 0.45), par=(0, 0), tono=(0.9, 0.82, 0.76)),
     [R(pal_(Rg, 3, 6, 14), W / 2, 850, 72)], ent=("fundido", 0.6), grado=dict(vineta=0.9))

# ---------------------------------------------------------------- CUAUHTÉMOC
K = "cuauhtemoc"
shot(INI(K, 0) - 0.05, F_foto("rivera_mercado", z0=1.05, z1=1.3, c0=(0.5, 0.5), c1=(0.6, 0.55), par=(50, 6), tono=(0.75, 0.5, 0.42)),
     [S([("13", w_(K, 0, 5)), ("De", w_(K, 0, 6)), ("Agosto", w_(K, 0, 7)), ("1521", w_(K, 0, 11))], 520, 230, 130, lineas=(4,))],
     ent=("tinta", 0.7), grado=dict(vineta=0.85))
shot(w_(K, 0, 12) - 0.05, F_clip("humo", inicio=5.0, z0=1.05, z1=1.3, tono=(1.5, 1.5, 1.6)),
     [R(pal_(K, 0, 12, 17), W / 2, 830, 84)], ent=("fundido", 0.5), grado=dict(vineta=0.9))
shot(INI(K, 1) - 0.05, F_foto("suplicio", z0=1.02, z1=1.18, c0=(0.5, 0.5), c1=(0.42, 0.52), par=(50, 8), tono=(0.85, 0.82, 0.8)),
     [S([("Cuauhtémoc", w_(K, 1, 3))], 470, 200, 110, lineas=(1,))], [TAG("Último emperador mexica", 560, 950, w_(K, 1, 4), 42)], ent=("fuga", 0.7))
shot(INI(K, 2) - 0.05, F_foto("suplicio", z0=1.45, z1=1.7, c0=(0.55, 0.78), c1=(0.5, 0.85), par=(50, 8), tono=(0.85, 0.8, 0.75)),
     [R(pal_(K, 2, 4, 7), W / 2, 330, 84)], ent=("zoom", 0.4), grado=dict(vineta=0.85))
snd(INI(K, 2), "fuego", 0.35, dur=3.0)
shot(INI(K, 3) - 0.05, F_clip("lago", inicio=3.0, z0=1.05, z1=1.3, tono=(0.5, 0.58, 0.7)),
     [R(pal_(K, 3, 9, 15), W / 2, 850, 80), N("4 días", 1440, 300, 150, w_(K, 3, 5) - 0.05, color=AM, sal=w_(K, 3, 9))], [TAG("Según las crónicas", 470, 300, INI(K, 3) + 0.2, 42)],
     ent=("tinta", 0.7), grado=dict(vineta=0.9))

shot(INI(K, 4) - 0.05, F_clip("monedas2", inicio=1.0, z0=1.05, z1=1.3, tono=(0.75, 0.65, 0.55)),
     [R(pal_(K, 4, 2, 7), W / 2, 830, 80)], ent=("fundido", 0.5), grado=dict(vineta=0.85))
shot(w_(K, 4, 8) - 0.05, F_borroso("cortes", 0.28), [R(pal_(K, 4, 9, 16), 1290, 470, 60, lineas=(3, 3, 1))],
     [CARTA(lambda: pola("cortes", 520, 1.34, (0.5, 0.3), "Endeudado"), w_(K, 4, 8) - 0.05, 560, 480, -3, desde=(-700, 0))], ent=("tinta", 0.6))
shot(INI(K, 5) - 0.05, F_clip("joyas", inicio=12.0, z0=1.1, z1=1.35, c0=(0.6, 0.5), c1=(0.4, 0.5), tono=(0.55, 0.45, 0.38)),
     [Qf(K, 5, 2, 10, W / 2, 560, 84)], ent=("fuga", 0.7), grado=dict(vineta=0.9))
snd(INI(K, 5) + 0.3, "latido", 0.45, dur=1.2)

# ---------------------------------------------------------------- LAGO
La = "lago"
shot(INI(La, 0) - 0.05, F_foto("mapa_1524", z0=1.0, z1=1.4, c0=(0.72, 0.5), c1=(0.8, 0.5), par=(0, 0), lado=3800, tono=(0.85, 0.8, 0.72)),
     [R(pal_(La, 0, 0, 4), W / 2, 880, 84)], ent=("tinta", 0.7))
shot(w_(La, 0, 11) - 0.05, F_foto("zocalo", z0=1.05, z1=1.3, c0=(0.5, 0.55), c1=(0.5, 0.45), par=(60, 8), tono=(0.9, 0.88, 0.85)),
     [S([("Ciudad", w_(La, 0, 17)), ("De", w_(La, 0, 18)), ("México", w_(La, 0, 19))], 500, 220, 120, lineas=(1,))], ent=("desenfoque", 0.9))
shot(INI(La, 1) - 0.05, F_clip("cdmx2", inicio=1.0, z0=1.05, z1=1.35, tono=(0.85, 0.85, 0.9)),
     [R(pal_(La, 1, 2, 10), W / 2, 830, 80)], ent=("fuga", 0.7), grado=dict(vineta=0.8))

# ---------------------------------------------------------------- SUBSUELO
Su = "subsuelo"
shot(INI(Su, 0) - 0.05, F_clip("cdmx", inicio=18.0, z0=1.05, z1=1.3, tono=(0.85, 0.85, 0.9)),
     [R(pal_(Su, 0, 3, 10), W / 2, 850, 78)], ent=("fundido", 0.5), grado=dict(vineta=0.8))
shot(INI(Su, 1) - 0.05, F_clip("excavadora", inicio=5.0, z0=1.05, z1=1.3, tono=(1.35, 1.28, 1.15)),
     [S([("1978", w_(Su, 1, 1))], 500, 230, 210, lineas=(1,), sal=w_(Su, 1, 9)), R(pal_(Su, 1, 6, 13), W / 2, 850, 70)], ent=("tinta", 0.7), grado=dict(polvo=0.5))
shot(w_(Su, 1, 13) - 0.05, F_foto("templo_mayor", z0=1.25, z1=1.05, c0=(0.55, 0.62), c1=(0.5, 0.55), par=(50, 6), tono=(0.75, 0.7, 0.68)),
     [R(pal_(Su, 1, 13, 19), W / 2, 850, 78)], ent=("zoom", 0.3), grado=dict(vineta=0.85))
snd(w_(Su, 1, 13), "impacto", 0.5)
shot(INI(Su, 2) - 0.05, F_foto("templo_mayor", z0=1.05, z1=1.3, c0=(0.5, 0.6), c1=(0.55, 0.5), par=(60, 8), tono=(0.95, 0.9, 0.85)),
     [S([("Templo", w_(Su, 2, 3)), ("Mayor", w_(Su, 2, 4))], 500, 230, 130, lineas=(1,))], [TAG("Enterrado durante siglos", 520, 940, w_(Su, 2, 5), 42)], ent=("fuga", 0.7))

# ---------------------------------------------------------------- BARRA


def _bar_hero(t0, t1, escala=1.55, scan=False):
    def f(lz, t):
        sp = barra_sp()
        u = e_back(prog(t, t0, t0 + 0.7))
        rot = -6 + 4 * math.sin(0.8 * (t - t0))
        cam = D.Cam((1.0, W / 2, H / 2, 0.0), (1.06, W / 2, H / 2 - 8, 0.0), max(t1 - t0, 1.0), mano=0.5)(t - t0)
        _brillo_oro(lz, t, 960, 480, 600, 0.22 * smooth(prog(t, t0, t0 + 0.6)))
        M = cam @ D.poner(sp.w, sp.h, 960, 480 + 6 * math.sin(t * 1.2), escala * max(u, 0.01), rot, 8 * math.sin(0.6 * (t - t0)))
        D.pegar(lz, sp, M, smooth(prog(t, t0, t0 + 0.25)))
        if scan:
            p = (((t - t0) * 0.55) % 1.0)
            x = lerp(300, 1620, p)
            a = (0.6 * math.sin(math.pi * p))
            X.trazo_recto(lz, (x, 200), (x + 40, 760), 0.0, 1.0, 10, color=(0.35, 0.95, 0.85), op=a)
    return f


Br = "barra"
shot(INI(Br, 0) - 0.05, F_clip("excavadora", inicio=0.5, z0=1.05, z1=1.25, tono=(1.35, 1.28, 1.15)),
     [S([("1981", w_(Br, 0, 1))], W / 2, 250, 230, lineas=(1,), sal=w_(Br, 0, 8) + 0.5)], ent=("tinta", 0.7))
shot(w_(Br, 0, 10) - 0.05, F_foto("alameda_aire", z0=1.05, z1=1.3, c0=(0.4, 0.45), c1=(0.55, 0.5), par=(70, 10), tono=(0.9, 0.9, 0.9)),
     [S([("Alameda", w_(Br, 0, 13)), ("Central", w_(Br, 0, 14))], 520, 220, 110, lineas=(1,))], ent=("fundido", 0.6))
shot(w_(Br, 0, 15) - 0.05, F_pozo(0.5, 0.5, 0.9, (0.30, 0.20, 0.08)),
     [N("1,93 kg", W / 2, 860, 130, w_(Br, 0, 21) - 0.05, color=AM)], [_bar_hero(w_(Br, 0, 15), INI(Br, 1)), TAG("Barra de oro · 1981", 500, 250, w_(Br, 0, 17), 46)], ent=("destello", 0.5))
snd(w_(Br, 0, 15) + 0.05, "bling", 0.6)
snd(w_(Br, 0, 15) + 0.3, "clink", 0.5)
shot(INI(Br, 1) - 0.05, F_pozo(0.5, 0.5, 0.9, (0.08, 0.16, 0.16)),
     [R(pal_(Br, 1, 5, 9), W / 2, 880, 62)],
     [_bar_hero(INI(Br, 1), INI(Br, 2), 1.3, scan=True), TAG("Instituto Nacional de Antropología e Historia", 960, 190, w_(Br, 1, 4), 40, rot=-1.5),
      TAG("Fluorescencia de rayos X", 520, 700, w_(Br, 1, 6), 40, rot=2.0), EST("Oro mexica", 1400, 800, w_(Br, 1, 10), 110)], ent=("fuga", 0.7))
snd(w_(Br, 1, 7), "obturador", 0.3)
shot(INI(Br, 2) - 0.05, F_foto("alameda_hidalgo", z0=1.05, z1=1.25, c0=(0.4, 0.5), c1=(0.6, 0.5), par=(50, 6), tono=(0.9, 0.9, 0.9)),
     [R(pal_(Br, 2, 0, 8), W / 2, 850, 72)], [EST("Única pieza identificada", 1240, 360, w_(Br, 2, 11), 78)], ent=("tinta", 0.7))

shot(INI(Br, 3) - 0.05, F_clip("cdmx", inicio=30.0, z0=1.05, z1=1.3, tono=(0.7, 0.7, 0.75)),
     [Qf(Br, 3, 9, 15, W / 2, 540, 84)], ent=("fuga", 0.7), grado=dict(vineta=0.9))
snd(INI(Br, 3) + 0.3, "latido", 0.45, dur=1.2)

# ---------------------------------------------------------------- PALACIO
Pa = "palacio"
shot(INI(Pa, 0) - 0.05, F_foto("monte_piedad", z0=1.05, z1=1.3, c0=(0.4, 0.5), c1=(0.6, 0.5), par=(60, 8), tono=(0.92, 0.9, 0.85)),
     [S([("2017", w_(Pa, 0, 6))], 480, 220, 170, lineas=(1,), sal=w_(Pa, 0, 22)), S([("Nacional", w_(Pa, 0, 12)), ("Monte", w_(Pa, 0, 13)), ("De", w_(Pa, 0, 14)), ("Piedad", w_(Pa, 0, 15))], 1300, 900, 88, lineas=(2, 2))], ent=("tinta", 0.7))
shot(w_(Pa, 0, 22) - 0.05, F_foto("monte_piedad_placa", z0=1.05, z1=1.25, c0=(0.5, 0.5), c1=(0.5, 0.5), par=(0, 0), tono=(0.9, 0.88, 0.85)),
     [R(pal_(Pa, 0, 24, 31), W / 2, 900, 62)], [TAG("Placa en el Monte de Piedad", 480, 240, w_(Pa, 0, 22) + 0.3, 42)], ent=("fuga", 0.7))
shot(INI(Pa, 1) - 0.05, F_clip("joyas", inicio=8.0, z0=1.05, z1=1.3, tono=(1.0, 0.85, 0.7)),
     [R(pal_(Pa, 1, 5, 9), W / 2, 850, 84)], ent=("fundido", 0.5))
snd(w_(Pa, 1, 6), "clink", 0.4)
snd(w_(Pa, 1, 7), "bling", 0.35)

# ---------------------------------------------------------------- TEORÍAS: tablero de evidencias
Te = "teorias"
T0 = INI(Te, 0) - 0.05
KEYS = [(T0, 1.0, C0[0], C0[1] - 40, 0.0), (w_(Te, 1, 0) - 0.3, 1.35, C0[0] - 480, C0[1] + 20, -1.0), (w_(Te, 2, 0) - 0.3, 1.3, C0[0], C0[1] + 90, 0.8),
        (w_(Te, 3, 0) - 0.3, 1.35, C0[0] + 480, C0[1] + 10, 1.0), (w_(Te, 3, 12) + 0.2, 1.0, C0[0], C0[1] - 40, 0.0)]


def _cam_keys(t):
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
    ti = (w_(Te, 1, 0) - 0.1, w_(Te, 2, 0) - 0.1, w_(Te, 3, 0) - 0.1)
    tarjetas = (("mapa_1524", -520, 20, -5, ti[0], "Bajo la ciudad", (0.72, 0.5)), ("templo_mayor", 0, 90, 3, ti[1], "Escondido", (0.5, 0.55)),
                ("bernal_portada", 520, 10, -3, ti[2], "¿Una leyenda?", (0.5, 0.3)))
    pins = []
    for k, (nom, dx, dy, r, t_in, ley, foco) in enumerate(tarjetas):
        carta(lz, pola(nom, ANC, 1.15, foco, ley), cam, t, t_in, cx + dx, cy + dy, r, desde=(0, -420), fase=k * 1.3)
        if t > t_in + 0.25:
            pins.append((cx + dx, cy + dy - ALT2 + 22))
    if t > T0 + 0.1:
        q = spr("pregunta", lambda: D.Sprite(np.full((220, 460, 3), (240, 235, 220), np.uint8), None, sombra=True, sr=12))
        M = cam @ D.poner(q.w, q.h, cx, cy - 250, 1.0, 1.5)
        D.pegar(lz, q, M, smooth(prog(t, T0 + 0.1, T0 + 0.5)))
        pm, a_, m = D.palabra_img("¿Dónde está?", "serif", 84, (0.72, 0.05, 0.05), stroke=0.02, glow=0.0)
        x, y = D.tf(M, q.w / 2, q.h / 2)
        D.mezclar_pm(lz, pm, a_, int(x - pm.shape[1] / 2), int(y - pm.shape[0] / 2), smooth(prog(t, T0 + 0.2, T0 + 0.6)))
    for k, p in enumerate(pins):
        D.hilo(lz, cam, (cx, cy - 350), p, smooth(prog(t, ti[k] + 0.2, ti[k] + 0.8)))
    if t > T0 + 0.1:
        D.pin(lz, cam, cx, cy - 350)
    for p in pins:
        D.pin(lz, cam, *p)
    D.estampa(lz, "Sin resolver", W / 2, 640, t, w_(Te, 3, 10) + 0.1, 120, rot=-7)


snd(w_(Te, 3, 10) + 0.1, "sello", 0.8)
for k in range(3):
    snd(w_(Te, k + 1, 0) - 0.1, "papel", 0.45)
shot(T0, F_negro(),
     [R(pal_(Te, 1, 4, 13), W / 2, 1000, 60, sal=w_(Te, 2, 0) - 0.05, lineas=(9,)), R(pal_(Te, 2, 1, 9), W / 2, 1000, 60, sal=w_(Te, 3, 0) - 0.05, lineas=(8,)),
      R(pal_(Te, 3, 0, 15), W / 2, 985, 54, lineas=(8, 7))],
     [_tablero], ent=("tinta", 0.7))

# ---------------------------------------------------------------- CIERRE
Ci = "cierre"
shot(INI(Ci, 0) - 0.05, F_clip("lluvia_noche", inicio=9.0, z0=1.0, z1=1.25, tono=(0.65, 0.72, 0.9)),
     [R(pal_(Ci, 0, 7, 14), W / 2, 850, 78)], ent=("negro", 0.5), grado=dict(vineta=0.9))
shot(w_(Ci, 0, 14) - 0.05, F_clip("lago", inicio=2.0, z0=1.05, z1=1.3, tono=(0.5, 0.55, 0.7)),
     [S(pal_(Ci, 0, 16, 24), W / 2, 500, 84, lineas=(4, 4))], ent=("fundido", 0.6), grado=dict(vineta=0.9))
snd(INI(Ci, 0) + 0.3, "lluvia", 0.4, dur=3.0)
snd(w_(Ci, 0, 15), "impacto", 0.5)


def _duerme(lz, t):
    tt = INI(Ci, 1) + 0.5
    k = 0.10 + 0.20 * smooth(prog(t, tt, w_(Ci, 1, 10) + 0.5)) + 0.03 * math.sin(t * 2.0)
    _brillo_oro(lz, t, 960, 1150, 1300, k)


shot(INI(Ci, 1) - 0.05, F_foto("zocalo", z0=1.05, z1=1.3, c0=(0.5, 0.45), c1=(0.5, 0.55), par=(60, 8), tono=(0.55, 0.55, 0.6)),
     [R(pal_(Ci, 1, 0, 13), W / 2, 400, 74, lineas=(4, 3, 3, 3))], [_duerme], ent=("tinta", 0.7), grado=dict(vineta=0.85))
snd(w_(Ci, 1, 8), "brillo", 0.5)
shot(INI(Ci, 2) - 0.05, F_clip("excavadora", inicio=3.0, z0=1.05, z1=1.3, tono=(1.2, 1.15, 1.05)),
     [Qf(Ci, 2, 0, 15, W / 2, 540, 70, sal=FIN(Ci) + 0.6)], ent=("fuga", 0.7), grado=dict(vineta=0.85))
snd(w_(Ci, 2, 0), "latido", 0.5, dur=1.2)
FIN_VOZ = FIN(Ci)
shot(FIN_VOZ + 1.2, F_negro(),
     [S([("El", FIN_VOZ + 1.5), ("Tesoro", FIN_VOZ + 1.7), ("Perdido", FIN_VOZ + 1.9), ("De", FIN_VOZ + 2.1), ("Moctezuma", FIN_VOZ + 2.3)], 960, 470, 110, lineas=(5,)),
      R([("Imágenes:", FIN_VOZ + 2.6), ("Wikimedia", FIN_VOZ + 2.6), ("Commons", FIN_VOZ + 2.6), ("(dominio", FIN_VOZ + 2.6), ("público", FIN_VOZ + 2.6), ("y", FIN_VOZ + 2.6),
         ("CC", FIN_VOZ + 2.6), ("BY-SA:", FIN_VOZ + 2.6), ("José", FIN_VOZ + 2.6), ("Luiz,", FIN_VOZ + 2.6), ("ProtoplasmaKid,", FIN_VOZ + 2.6), ("J.", FIN_VOZ + 2.6), ("C.", FIN_VOZ + 2.6), ("Fonseca", FIN_VOZ + 2.6), ("Mata)", FIN_VOZ + 2.6)],
        960, 700, 28, lineas=(15,)),
      R([("Video:", FIN_VOZ + 2.7), ("Pexels", FIN_VOZ + 2.7), ("·", FIN_VOZ + 2.7), ("Fuentes:", FIN_VOZ + 2.7), ("Bernal", FIN_VOZ + 2.7), ("Díaz,", FIN_VOZ + 2.7), ("Arqueología", FIN_VOZ + 2.7),
         ("Mexicana,", FIN_VOZ + 2.7), ("INAH", FIN_VOZ + 2.7)], 960, 750, 28, lineas=(9,))], ent=("negro", 0.6))
snd(FIN_VOZ + 1.5, "impacto", 0.6)
_construir()


# ================================================================== Mundo
class Mundo(Escena):
    def preparar(self):
        if self.idx == 0:
            self.sonidos()

    def sonidos(self):
        e = self.ev
        for t, n, v, kw in SND:
            e(t, n, v, **kw)

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
