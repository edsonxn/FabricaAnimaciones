# -*- coding: utf-8 -*-
"""Kit del documental «Christa Pike: la ejecución que no terminó» (estilo documental v3, ver docs/estilo_documental.md).

Sobre el motor `docu` / `docu_fx`: anclas por PALABRA (no por índice), fondos para archivo 4:3 y para noticias con rótulo inferior,
crédito en pantalla de todo material de terceros, mapa de relieve con cámara y ruta, reloj de la noche, ventana con piedra,
diagrama vena/tejido y línea de años. Nada de aquí inventa documentos: son gráficos explicativos y se rotulan como tales.
"""
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
AMAR = (0.95, 1.0, 0.10)
CHART = (190, 235, 30)


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


def pola(nombre, ancho=440, asp=1.05, foco=(0.5, 0.5), leyenda=None, lado=1600):
    return spr(("p", nombre, ancho, asp, foco, leyenda), lambda: D.polaroid(D.cargar(D.ruta_img(nombre), lado), ancho, asp, foco, leyenda=leyenda))


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


def carta(lz, sp, M, t, t_in, x, y, rot=0.0, s=1.0, desde=(0, -420), dur=0.5, flota=1.0, fase=0.0, op=1.0, ry0=50.0, salida=None):
    if t < t_in:
        return
    u = e_out(prog(t, t_in, t_in + dur))
    e = t - t_in
    asent = math.exp(-(e - dur) * 3.2) * math.sin((e - dur) * 15.0) * 2.0 if e > dur else 0.0
    fl = flota * 4.0 * math.sin(0.9 * t + fase)
    Mm = M @ D.poner(sp.w, sp.h, lerp(x + desde[0], x, u), lerp(y + desde[1], y, u) + fl, lerp(1.3, 1.0, u) * s, rot + asent + (1 - u) * 12, (1 - u) * ry0)
    o = op * smooth(prog(t, t_in, t_in + 0.15)) * (1 - (smooth(prog(t, salida, salida + 0.3)) if salida is not None else 0))
    D.pegar(lz, sp, Mm, o)


# ------------------------------------------------------------------ texto (estilos del original)
def R(palabras, cx=W / 2, cy=H * 0.56, px=88, lineas=None, sal=None):
    """Texto principal: cursiva blanca en mayúsculas con líneas de escaneo, palabra a palabra."""
    pal = X.rotulo(palabras, cx, cy, px, lineas)

    def f(lz, t):
        X.dibujar_rotulo(lz, pal, t, px, salida=sal)
    return f


def S(palabras, cx=W / 2, cy=H * 0.55, px=98, lineas=None, sal=None):
    """Serif amarillo condensado, Título Con Mayúsculas (nombres, lugares, cifras)."""
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
def _frame_clip(nombre, ini, tl, vel, fin):
    """Cuadro RGB del clip en el instante ini + tl*vel, CONGELADO en `fin` (o en el final del archivo): nunca da la vuelta al inicio."""
    c = X.Clip.abrir(nombre)
    seg = c.n / c.fps
    lim = min(fin if fin is not None else seg, seg) - 2.0 / c.fps
    tt = min(max(ini + tl * vel, 0.0), lim)
    return c, c.frame(tt * c.fps)


def F_clip(nombre, ini=0.0, fin=None, z0=1.04, z1=1.14, c0=(0.5, 0.5), c1=(0.5, 0.5), tono=None, sat=1.0, banner=0.0, vel=1.0, op=1.0):
    """Clip 16:9 como fondo (cover) con cámara z0->z1. `banner` = fracción inferior que se recorta con zoom (rótulos de noticias).
    `fin` = segundo del archivo donde se congela (evita que el clip dé la vuelta)."""
    if banner:
        zb = 1.0 / (1.0 - banner)
        z0, z1 = z0 * zb, z1 * zb
        c0 = (c0[0], (1 - banner) / 2)
        c1 = (c1[0], (1 - banner) / 2)

    def f(lz, tl, t, dur, ext):
        c, fr = _frame_clip(nombre, ini, tl, vel, fin)
        u = e_inout(clamp01(tl / max(dur, 1e-3)))
        z = lerp(z0, z1, u) * ext
        cx, cy = lerp(c0[0], c1[0], u) * c.w, lerp(c0[1], c1[1], u) * c.h
        s = max(W / c.w, H / c.h) * z
        M = np.array([[s, 0, W / 2 - cx * s], [0, s, H / 2 - cy * s]], np.float32)
        out = cv2.warpAffine(fr, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT).astype(np.float32) / 255.0
        if sat != 1.0:
            lum = out @ np.array([0.299, 0.587, 0.114], np.float32)
            out = lum[..., None] + (out - lum[..., None]) * sat
        if tono is not None:
            out *= np.float32(tono)
        if op >= 0.999:
            lz[:] = np.clip(out, 0, 1)
        else:
            lz *= (1 - op)
            lz += np.clip(out, 0, 1) * op
    return f


_SOMBRA = {}


def _sombra_rect(w, h):
    k = (w, h)
    if k not in _SOMBRA:
        pad = 90
        m = np.zeros((h + 2 * pad, w + 2 * pad), np.float32)
        m[pad:pad + h, pad:pad + w] = 1.0
        _SOMBRA[k] = (cv2.GaussianBlur(m, (0, 0), 26), pad)
    return _SOMBRA[k]


def F_arch(nombre, ini=0.0, fin=None, x_cont=(0.125, 0.875), z0=1.0, z1=1.07, alto=930, bg=0.30, tono=None, sat=1.0, vel=1.0, dx=0.0, op=1.0):
    """Archivo 4:3 (con barras negras en el original): el contenido va centrado, con sombra, sobre su propio fondo desenfocado y oscuro."""
    def f(lz, tl, t, dur, ext):
        c, fr = _frame_clip(nombre, ini, tl, vel, fin)
        h, w = fr.shape[:2]
        xa, xb = int(x_cont[0] * w), int(x_cont[1] * w)
        cont = fr[:, xa:xb]
        ch, cw = cont.shape[:2]
        # fondo: cover desenfocado a 1/6
        sw, sh = W // 6, H // 6
        k = max(sw / cw, sh / ch)
        r = cv2.resize(cont, (int(cw * k) + 1, int(ch * k) + 1), interpolation=cv2.INTER_AREA)
        y0, x0 = (r.shape[0] - sh) // 2, (r.shape[1] - sw) // 2
        r = cv2.GaussianBlur(r[y0:y0 + sh, x0:x0 + sw].astype(np.float32) / 255.0, (0, 0), 5)
        out = cv2.resize(r, (W, H), interpolation=cv2.INTER_CUBIC) * bg
        out = out * (np.float32(tono) if tono is not None else 1.0)
        u = e_inout(clamp01(tl / max(dur, 1e-3)))
        z = lerp(z0, z1, u) * ext
        fh = int(alto * z)
        fw = int(fh * cw / ch)
        fg = cv2.resize(cont, (fw, fh), interpolation=cv2.INTER_LINEAR).astype(np.float32) / 255.0
        if sat != 1.0:
            lum = fg @ np.array([0.299, 0.587, 0.114], np.float32)
            fg = lum[..., None] + (fg - lum[..., None]) * sat
        if tono is not None:
            fg = fg * np.float32(tono)
        cx, cy = W / 2 + dx, H / 2
        X0, Y0 = int(cx - fw / 2), int(cy - fh / 2)
        sm, pad = _sombra_rect(fw, fh)
        a0, b0 = X0 - pad, Y0 - pad
        ra0, rb0 = max(0, a0), max(0, b0)
        ra1, rb1 = min(W, a0 + sm.shape[1]), min(H, b0 + sm.shape[0])
        if ra1 > ra0 and rb1 > rb0:
            out[rb0:rb1, ra0:ra1] *= (1 - 0.65 * sm[rb0 - b0:rb1 - b0, ra0 - a0:ra1 - a0])[..., None]
        sx0, sy0 = max(0, -X0), max(0, -Y0)
        dx0, dy0 = max(0, X0), max(0, Y0)
        dx1, dy1 = min(W, X0 + fw), min(H, Y0 + fh)
        out[dy0:dy1, dx0:dx1] = fg[sy0:sy0 + (dy1 - dy0), sx0:sx0 + (dx1 - dx0)]
        if op >= 0.999:
            lz[:] = np.clip(out, 0, 1)
        else:
            lz *= (1 - op)
            lz += np.clip(out, 0, 1) * op
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


def HERO(nombre, x=960, y=500, rot=0.0, alto=880, t_in=0.0, ry=(-10, -3), desde=(0, 0), dur=0.55, lado=2200, sal=None):
    """Foto grande tipo lámina, con cámara propia."""
    def f(lz, t):
        sp = spr(("hero", nombre, alto), lambda: D.hoja_papel(D.cargar(D.ruta_img(nombre), lado), alto))
        u = e_out(prog(t, t_in, t_in + dur))
        cam = D.Cam((1.0, W / 2, H / 2, 0.0), (1.08, W / 2, H / 2 + 10, 0.0), 3.0, mano=0.8)(t - t_in)
        o = smooth(prog(t, t_in, t_in + 0.2)) * (1 - (smooth(prog(t, sal, sal + 0.3)) if sal is not None else 0))
        D.pegar(lz, sp, cam @ D.poner(sp.w, sp.h, lerp(x + desde[0], x, u), lerp(y + desde[1], y, u), lerp(0.9, 1.0, u), lerp(rot + 5, rot, u), lerp(ry[0], ry[1], u)), o)
    return f


def FRAME_CLIP(nombre, x, y, ancho, ini, t_in, rot=0.0, x_cont=None, t_out=None, op=1.0, z=1.0, fin=None):
    """Mini-pantalla con un clip (marco blanco fino, sombra) que entra como una lámina. `x_cont` recorta barras laterales."""
    def f(lz, t):
        if t < t_in:
            return
        c, fr = _frame_clip(nombre, ini, t - t_in, 1.0, fin)
        h, w = fr.shape[:2]
        if x_cont:
            fr = fr[:, int(x_cont[0] * w):int(x_cont[1] * w)]
            h, w = fr.shape[:2]
        alto = int(ancho * h / w)
        im = cv2.resize(fr, (ancho, alto), interpolation=cv2.INTER_AREA)
        b = 10
        marco = np.full((alto + 2 * b, ancho + 2 * b, 3), 245, np.uint8)
        marco[b:b + alto, b:b + ancho] = im
        sp = D.Sprite(marco, None, sombra=True, sr=16, off=(10, 14), sop=0.6)
        u = e_out(prog(t, t_in, t_in + 0.45))
        o = op * smooth(prog(t, t_in, t_in + 0.2)) * (1 - (smooth(prog(t, t_out, t_out + 0.3)) if t_out is not None else 0))
        D.pegar(lz, sp, D.poner(sp.w, sp.h, x, lerp(y + 60, y, u), lerp(1.12, 1.0, u) * z, rot + (1 - u) * 5), o)
    return f


# ------------------------------------------------------------------ reloj de la noche
def RELOJ(txt, cx, cy, px, t0, sal=None, etiqueta="hora local · Nashville"):
    """Hora grande en serif rojo con su etiqueta; entra con un tic."""
    snd(t0, "tick", 0.55)

    def f(lz, t):
        D.numero(lz, txt, cx, cy, px, t, t0, color=RJ, fnt="abril_cond", salida=sal, pop=False)
        if t >= t0 + 0.2:
            o = smooth(prog(t, t0 + 0.2, t0 + 0.6)) * (1 - (smooth(prog(t, sal, sal + 0.3)) if sal is not None else 0))
            sp = spr(("rl", etiqueta), lambda: _cred_sprite(etiqueta.upper()))
            D.pegar(lz, sp, D.poner(sp.w, sp.h, cx, cy + px * 0.62, 1.0, 0.0), 0.8 * o)
    return f


# ------------------------------------------------------------------ mapa de relieve con cámara y ruta
_MAPA = {}


def _mapa():
    if "m" not in _MAPA:
        im = cv2.cvtColor(cv2.imread(os.path.join(os.getcwd(), "mapas", "mapa_sureste.png")), cv2.COLOR_BGR2RGB)
        im = np.clip((im.astype(np.float32) / 255.0 - 0.42) * 1.55 + 0.46, 0, 1)
        _MAPA["meta"] = json.load(open(os.path.join(os.getcwd(), "mapas", "meta.json")))
        pil = Image.fromarray((im * 255).astype(np.uint8)).convert("RGBA")
        ov = Image.new("RGBA", pil.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for txt, lon, lat, px in (("TENNESSEE", -86.3, 35.78, 74), ("KENTUCKY", -85.9, 37.4, 54), ("VIRGINIA", -78.9, 37.35, 54),
                                  ("VIRGINIA OCCIDENTAL", -80.9, 38.7, 44), ("CAROLINA DEL NORTE", -79.7, 35.55, 50),
                                  ("GEORGIA", -83.4, 33.2, 54), ("ALABAMA", -86.8, 33.0, 54), ("MISISIPI", -89.6, 33.6, 50)):
            x, y = _proy_meta(lon, lat)
            f = D.fuente("sans_l", px)
            sep = int(px * 0.28)
            w = sum(d.textlength(c, font=f) + sep for c in txt)
            xx = x - w / 2
            for c in txt:
                d.text((xx, y), c, font=f, fill=(255, 255, 255, 120), anchor="lm", stroke_width=2, stroke_fill=(0, 0, 0, 90))
                xx += d.textlength(c, font=f) + sep
        pil = Image.alpha_composite(pil, ov).convert("RGB")
        _MAPA["m"] = np.asarray(pil)
    return _MAPA["m"], _MAPA["meta"]


def _proy_meta(lon, lat):
    m = _MAPA["meta"]
    n = 2 ** m["z"]
    x = (lon + 180) / 360 * n
    y = (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n
    return (x - m["tx0"]) * 256 - m["x_off"], (y - m["ty0"]) * 256 - m["y_off"]


def proy(lon, lat):
    _, m = _mapa()
    n = 2 ** m["z"]
    x = (lon + 180) / 360 * n
    y = (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n
    return (x - m["tx0"]) * 256 - m["x_off"], (y - m["ty0"]) * 256 - m["y_off"]


CIUDADES = {"Beckley": (-81.188, 37.778), "Swannanoa": (-82.400, 35.598), "Knoxville": (-83.921, 35.961), "Nashville": (-86.781, 36.163)}


def MAPA(claves, marcas=(), rutas=(), tono=(0.80, 0.80, 0.78), titulo=None):
    """Fondo de mapa. `claves` = [(t, zoom, lon, lat)] (tiempo ABSOLUTO; la cámara interpola con easing); `marcas` = [(ciudad, t_aparece)];
    `rutas` = [(ciudad_a, ciudad_b, t0, t1)] líneas punteadas que se dibujan. Escala: zoom 1 = 0.62 px de pantalla por px del mapa."""
    def cam(t):
        ks = sorted(claves)
        if t <= ks[0][0]:
            return ks[0][1:]
        for (ta, za, xa, ya), (tb, zb, xb, yb) in zip(ks[:-1], ks[1:]):
            if t <= tb:
                u = e_inout(clamp01((t - ta) / max(tb - ta, 1e-3)))
                return lerp(za, zb, u), lerp(xa, xb, u), lerp(ya, yb, u)
        return ks[-1][1:]

    def f(lz, tl, t, dur, ext):
        im, _ = _mapa()
        z, lon, lat = cam(t)
        s = 0.62 * z * ext
        cx, cy = proy(lon, lat)
        M = np.array([[s, 0, W / 2 - cx * s], [0, s, H / 2 - cy * s]], np.float32)
        out = cv2.warpAffine(im, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT).astype(np.float32) / 255.0
        out *= np.float32(tono)
        # rutas
        for (a, b, t0, t1) in rutas:
            if t < t0:
                continue
            pa = np.array(proy(*CIUDADES[a]))
            pb = np.array(proy(*CIUDADES[b]))
            u = e_inout(prog(t, t0, t1))
            qa = pa * s + M[:, 2]
            qb = (pa + (pb - pa) * u) * s + M[:, 2]
            n = max(2, int(np.hypot(*(qb - qa)) / 34))
            for i in range(n):
                a0 = qa + (qb - qa) * (i / n)
                a1 = qa + (qb - qa) * ((i + 0.55) / n)
                cv2.line(out, (int(a0[0]), int(a0[1])), (int(a1[0]), int(a1[1])), (1.0, 0.98, 0.94), 5, cv2.LINE_AA)
        # marcas: primero los puntos, luego los nombres
        vis = []
        for (c, t0) in marcas:
            if t < t0:
                continue
            px_, py_ = np.array(proy(*CIUDADES[c])) * s + M[:, 2]
            if not (-80 < px_ < W + 80 and -80 < py_ < H + 80):
                continue
            u = e_back(prog(t, t0, t0 + 0.4))
            rad = int(20 * u * min(1.4, max(0.8, z ** 0.35)))
            cv2.circle(out, (int(px_), int(py_)), rad + 7, (0.02, 0.02, 0.02), -1, cv2.LINE_AA)
            cv2.circle(out, (int(px_), int(py_)), rad, tuple(v / 255.0 for v in CHART), -1, cv2.LINE_AA)
            vis.append((c, px_, py_, rad))
        if vis:
            pil = Image.fromarray((out * 255).clip(0, 255).astype(np.uint8))
            d = ImageDraw.Draw(pil)
            for c, px_, py_, rad in vis:
                d.text((px_, py_ - rad - 18), c, font=D.fuente("sans_l", 38), fill=(255, 255, 255), anchor="mb", stroke_width=4, stroke_fill=(0, 0, 0))
            out = np.asarray(pil).astype(np.float32) / 255.0
        lz[:] = np.clip(out, 0, 1)
    return f


# ------------------------------------------------------------------ gráficos explicativos
def F_ventana_piedra(t_piedra, base=(0.075, 0.08, 0.095)):
    """Muro de bloques con una ventana en la pared (luz fría detrás del vidrio); una piedra blanca aparece en ella: el detalle de las 7:41 p. m.
    que contaron los testigos. Gráfico de recreación (se rotula como tal)."""
    def f(lz, tl, t, dur, ext):
        if "muro" not in _C:
            rng = np.random.default_rng(3)
            ruido = cv2.GaussianBlur(rng.random((H // 6, W // 6)).astype(np.float32), (0, 0), 1.0)
            _C["muro"] = cv2.resize(ruido, (W, H), interpolation=cv2.INTER_CUBIC)
            bl = np.ones((H, W), np.float32)
            for yy in range(0, H, 72):
                bl[yy:yy + 3] *= 0.45
                for xx in range((yy // 72 % 2) * 120, W, 240):
                    bl[yy:yy + 72, xx:xx + 3] *= 0.5
            _C["bloques"] = bl
        muro, bloques = _C["muro"], _C["bloques"]
        cam = 1.0 + 0.05 * (tl / max(dur, 1))
        cx, cy = 1180, 520
        ww_, hh_ = int(640 * cam), int(460 * cam)
        x0, y0 = int(cx - ww_ / 2), int(cy - hh_ / 2)
        # muro iluminado desde la ventana (halo frío)
        Y, X = np.mgrid[0:H, 0:W].astype(np.float32)
        d = np.sqrt(((X - cx) / 1100.0) ** 2 + ((Y - cy) / 760.0) ** 2)
        luz = np.clip(1.0 - d, 0, 1) ** 1.6
        lz[:] = (np.array(base, np.float32) * (0.75 + 0.5 * muro[..., None]) * bloques[..., None]) + luz[..., None] * np.array([0.10, 0.13, 0.17], np.float32)
        # marco y vidrio
        cv2.rectangle(lz, (x0 - 22, y0 - 22), (x0 + ww_ + 22, y0 + hh_ + 22), (0.20, 0.21, 0.23), -1)
        cv2.rectangle(lz, (x0 - 22, y0 - 22), (x0 + ww_ + 22, y0 + hh_ + 22), (0.34, 0.35, 0.38), 4)
        vid = np.linspace(0.55, 0.22, hh_)[:, None, None] * np.array([0.72, 0.86, 1.0], np.float32)
        lz[y0:y0 + hh_, x0:x0 + ww_] = vid
        refl = np.zeros((hh_, ww_), np.float32)
        cv2.fillConvexPoly(refl, np.array([[0, hh_ * 0.05], [ww_ * 0.42, 0], [ww_ * 0.62, 0], [0, hh_ * 0.75]], np.int32), 0.13)
        lz[y0:y0 + hh_, x0:x0 + ww_] += refl[..., None]
        cv2.line(lz, (x0 + ww_ // 2, y0), (x0 + ww_ // 2, y0 + hh_), (0.20, 0.21, 0.23), 8)          # travesaño
        # alféizar con su sombra
        cv2.rectangle(lz, (x0 - 40, y0 + hh_ + 22), (x0 + ww_ + 40, y0 + hh_ + 52), (0.30, 0.31, 0.33), -1)
        cv2.rectangle(lz, (x0 - 40, y0 + hh_ + 52), (x0 + ww_ + 40, y0 + hh_ + 80), (0.05, 0.05, 0.06), -1)
        # polvo en suspensión frente a la luz
        for i in range(36):
            px_ = (X[0, int((i * 197 + t * (8 + i % 5) * 4) % W)])
            py_ = (i * 83 + t * (6 + i % 4) * 5) % (H * 0.9)
            cv2.circle(lz, (int(px_), int(py_)), 2 + i % 2, (0.5, 0.55, 0.62), -1, cv2.LINE_AA)
        # piedra: cae dentro del vidrio y rebota una vez
        if t >= t_piedra:
            u = clamp01((t - t_piedra) / 0.6)
            yb = y0 + hh_ - 34
            ya = y0 + 34
            yy_ = lerp(ya, yb, u * u) - (math.sin(clamp01((t - t_piedra - 0.6) / 0.35) * math.pi) * 22 if t > t_piedra + 0.6 else 0)
            xx_ = x0 + ww_ * 0.62
            gl = np.zeros((H, W), np.float32)
            cv2.ellipse(gl, (int(xx_), int(yy_)), (38, 28), 14, 0, 360, 1.0, -1, cv2.LINE_AA)
            halo = cv2.GaussianBlur(gl, (0, 0), 44) * 0.7
            lz += halo[..., None] * np.array([1.0, 0.98, 0.92], np.float32)
            lz *= (1 - gl[..., None] * 0.97)
            lz += gl[..., None] * np.array([0.95, 0.94, 0.90], np.float32) * 0.97
    return f


def F_vena(t0):
    """Diagrama explicativo (no es una imagen real): línea intravenosa que debería ir a la vena y el líquido se desvía al tejido."""
    def f(lz, tl, t, dur, ext):
        lz[:] = D.pozo_luz(0.5, 0.5, 0.9, (0.10, 0.09, 0.10), (0.012, 0.010, 0.012))
        base = np.zeros((H, W, 3), np.float32)
        yv = 560
        # tejido (franja punteada gris) arriba y abajo
        for yy, sg in ((yv - 230, -1), (yv + 160, 1)):
            cv2.rectangle(base, (210, yy), (1710, yy + 70), (0.17, 0.16, 0.16), -1)
        # vena (tubo rojo)
        cv2.line(base, (260, yv), (1660, yv), (0.55, 0.06, 0.07), 70, cv2.LINE_AA)
        cv2.line(base, (260, yv - 14), (1660, yv - 14), (0.80, 0.12, 0.12), 26, cv2.LINE_AA)
        lz += base
        # línea IV (diagonal fina) entrando desde arriba a la izquierda y pinchando la pared de la vena
        u = e_out(prog(t, t0, t0 + 0.9))
        a = np.array([330, 160.0])
        b = np.array([760, yv - 36.0])
        c = a + (b - a) * u
        cv2.line(lz, (int(a[0]), int(a[1])), (int(c[0]), int(c[1])), (0.82, 0.82, 0.80), 9, cv2.LINE_AA)
        # fluido: del catéter al tejido en vez de a la vena
        if t > t0 + 0.9:
            v = e_inout(prog(t, t0 + 1.0, t0 + 3.2))
            for k in range(40):
                ang = -math.pi / 2 + (k - 20) * 0.075
                r = (60 + 380 * v) * (0.5 + 0.5 * ((k * 37) % 10) / 10)
                px_, py_ = 760 + math.cos(ang) * r * 1.1, yv - 36 + math.sin(ang) * r * 0.9
                if py_ < yv - 60:
                    cv2.circle(lz, (int(px_), int(py_)), 7, (0.95, 0.90, 0.25), -1, cv2.LINE_AA)
            glow = np.zeros((H, W), np.float32)
            cv2.circle(glow, (760, yv - 150), int(40 + 220 * v), 1.0, -1, cv2.LINE_AA)
            glow = cv2.GaussianBlur(glow, (0, 0), 60)
            lz += glow[..., None] * np.array([0.30, 0.26, 0.04], np.float32) * 0.9
        # rótulos
        pil = Image.fromarray((np.clip(lz, 0, 1) * 255).astype(np.uint8))
        d = ImageDraw.Draw(pil)
        ft = D.fuente("sans_l", 40)
        if t > t0 + 0.4:
            d.text((1700, yv + 120), "VENA", font=ft, fill=(255, 150, 140), anchor="rm", stroke_width=3, stroke_fill=(0, 0, 0))
        if t > t0 + 1.4:
            d.text((960, yv - 330), "TEJIDO", font=ft, fill=(210, 205, 200), anchor="mm", stroke_width=3, stroke_fill=(0, 0, 0))
        d.text((960, 1010), "ESQUEMA EXPLICATIVO · NO ES UNA IMAGEN REAL", font=D.fuente("sans_l", 26), fill=(190, 188, 182), anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0))
        lz[:] = np.asarray(pil).astype(np.float32) / 255.0
    return f


# ------------------------------------------------------------------ línea de años (1995-2026) con marcas que aparecen
def LINEA_ANOS(a_ini, a_fin, y, marcas, t_ini, t_fin_barra, r0, r1, x0=170, x1=1750, etiqueta="", sal=None, paso=5, paso_lab=10):
    """Eje de años con una barra que crece de r0 a r1 y marcas [(año, texto, t_aparece[, (arriba, alto)])]. `y` = y del eje en pantalla."""
    def f(lz, t):
        if t < t_ini:
            return
        o = smooth(prog(t, t_ini, t_ini + 0.4)) * (1 - (smooth(prog(t, sal, sal + 0.4)) if sal is not None else 0))
        wpx, hpx, yy = 1920, 720, 420
        im = Image.new("RGBA", (wpx, hpx), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        px = lambda yr: x0 + (yr - a_ini) / (a_fin - a_ini) * (x1 - x0)
        d.line([x0, yy, x1, yy], fill=(235, 235, 230, 255), width=6)
        for yr in range(int(math.ceil(a_ini / paso) * paso), int(a_fin) + 1, paso):
            big = yr % paso_lab == 0
            d.line([px(yr), yy - (20 if big else 10), px(yr), yy + (20 if big else 10)], fill=(235, 235, 230, 255), width=4 if big else 2)
            if big:
                d.text((px(yr), yy + 34), str(yr), font=D.fuente("sans", 36), fill=(235, 235, 230, 255), anchor="mt", stroke_width=2, stroke_fill=(0, 0, 0, 255))
        u = e_inout(clamp01((t - t_ini - 0.2) / max(t_fin_barra - t_ini, 0.5)))
        xa, xb = px(r0), lerp(px(r0), px(r1), u)
        d.rectangle([xa, yy - 24, max(xb, xa + 2), yy + 24], fill=(232, 240, 40, 235))
        for k_, m in enumerate(marcas):
            yr, txt, ta = m[:3]
            if t < ta:
                continue
            up, hh = m[3] if len(m) > 3 else (k_ % 2 == 0, 110)
            lab = m[4] if len(m) > 4 else str(int(yr))
            q = e_out(prog(t, ta, ta + 0.35))
            y1 = yy - hh * q if up else yy + 44 + hh * q
            d.line([px(yr), yy - 16 if up else yy + 16, px(yr), y1], fill=(200, 200, 195, int(255 * q)), width=4)
            d.ellipse([px(yr) - 13, yy - 13, px(yr) + 13, yy + 13], fill=(190, 235, 30, 255))
            d.text((px(yr), y1 - 10 if up else y1 + 10), lab, font=D.fuente("serif", 58), fill=(232, 240, 40, int(255 * q)), anchor="mb" if up else "mt",
                   stroke_width=2, stroke_fill=(0, 0, 0, int(255 * q)))
            d.text((px(yr), y1 - 78 if up else y1 + 80), txt, font=D.fuente("sans_l", 35), fill=(238, 238, 232, int(255 * q)), anchor="mb" if up else "mt",
                   stroke_width=3, stroke_fill=(0, 0, 0, int(255 * q)))
        if etiqueta:
            d.text((wpx / 2, 24), etiqueta, font=D.fuente("sans_l", 38), fill=(228, 228, 222, 255), anchor="mt", stroke_width=3, stroke_fill=(0, 0, 0, 255))
        a = np.asarray(im, np.float32) / 255.0
        D.mezclar_pm(lz, a[..., :3] * a[..., 3:4], a[..., 3], 0, int(y - yy), o)
    return f


def CRONO(t0, t1, cx, cy, r=180, color=(0.86, 0.10, 0.10)):
    """Reloj circular que se llena (de 0 a una vuelta) entre t0 y t1; marcas cada cinco minutos de una hora."""
    def f(lz, t):
        if t < t0:
            return
        o = smooth(prog(t, t0, t0 + 0.5))
        u = e_inout(prog(t, t0 + 0.3, t1))
        buf = lz.copy()
        cv2.circle(buf, (cx, cy), r + 6, (0.03, 0.03, 0.03), 26, cv2.LINE_AA)
        cv2.circle(buf, (cx, cy), r, (0.35, 0.35, 0.35), 8, cv2.LINE_AA)
        for k_ in range(12):
            a = math.radians(k_ * 30 - 90)
            cv2.line(buf, (int(cx + math.cos(a) * (r - 22)), int(cy + math.sin(a) * (r - 22))), (int(cx + math.cos(a) * (r + 2)), int(cy + math.sin(a) * (r + 2))),
                     (0.9, 0.9, 0.88), 4, cv2.LINE_AA)
        if u > 0.003:
            cv2.ellipse(buf, (cx, cy), (r, r), 0, -90, -90 + 360 * u, color, 16, cv2.LINE_AA)
            a = math.radians(-90 + 360 * u)
            cv2.circle(buf, (int(cx + math.cos(a) * r), int(cy + math.sin(a) * r)), 15, (1.0, 0.95, 0.9), -1, cv2.LINE_AA)
        lz[:] = lz * (1 - o) + buf * o
    return f


# ------------------------------------------------------------------ persianas que se cierran y se abren (sobre lo que haya debajo)
def PERSIANAS(t_cierra, t_abre, dur=0.9, n=14):
    """Láminas horizontales negras que cierran de arriba abajo en `dur` s desde t_cierra y se abren desde t_abre."""
    def f(lz, t):
        u1 = e_inout(prog(t, t_cierra, t_cierra + dur))
        u2 = e_inout(prog(t, t_abre, t_abre + dur))
        c = u1 * (1 - u2)
        if c <= 0.003:
            return
        hh = H / n
        for k in range(n):
            y0 = int(k * hh)
            alto = int(hh * c * 1.02)
            if alto > 0:
                lz[y0:y0 + alto] *= 0.04
    return f


# ------------------------------------------------------------------ temporizador de cuenta atrás (5:00 -> 0:00)
def TEMPORIZADOR(t0, t1, cx, cy, px, desde=300):
    def f(lz, t):
        if t < t0:
            return
        u = clamp01((t - t0) / max(t1 - t0, 1e-3))
        rest = int(round(desde * (1 - u)))
        txt = f"{rest // 60}:{rest % 60:02d}"
        D.numero(lz, txt, cx, cy, px, t, t0, color=BL, fnt="abril_cond", pop=False)
    return f


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
