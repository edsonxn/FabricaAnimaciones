# -*- coding: utf-8 -*-
"""Fotos REALES como pegatina dentro del kit de boceto + guache (historia_aguascalientes, 22-oct-2026).

Pedido del usuario: «cuando lo veas necesario mostrar 1 foto real de lo que estés hablando». `FotoPeg` tiene la MISMA interfaz que
`pegflow.Peg` (y que `boceto.Dib.dibujar`), así que entra en `ga`/`pa`/`R.act` igual que cualquier dibujo:
  - se ancla por los PIES (centro del borde inferior de la copia) en (x, y); s = 1 → `alto` px (400) de alto TOTAL (marco incluido);
  - aspecto de foto impresa pegada en la libreta: marco de papel blanco cálido (más ancho abajo, con el crédito en letra pequeña),
    dos tiras de cinta adhesiva semitransparente en las esquinas de arriba, inclinación ligera (de la semilla, o `incl` en grados),
    sombra suave como las pegatinas del kit, tono cálido leve (`calido`) para casar con el guache;
  - vida: temblor mínimo de toda la copia (3 variantes que se turnan con la fase del boceto, sin deformar la foto) + respiración;
  - `u` < 1 = entrada «pegar»: cae girando un poco desde más grande, la sombra se acerca al aterrizar y las cintas llegan al final;
    `sq` la aplasta (pop); `rot` se suma a la inclinación; `flip` se ignora (una foto real nunca se espeja).
Se compone en la capa `hoja.fotos` de pegflow: ENCIMA del mapa y de las pegatinas, DEBAJO del crayón y la tinta (rótulos, números).

Recortes: `fotos/recortes.json` → `python foto_peg.py recortar` rehace `fotos/<clave>_rec.jpg`.
"""
import json
import math
import os
import sys
from collections import OrderedDict
from functools import lru_cache

import cv2
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
FOTOS = os.path.join(AQUI, "fotos")


# ------------------------------------------------------------------ recortes (sin dependencias del kit)
def recortar(claves=None):
    rec = json.load(open(os.path.join(FOTOS, "recortes.json"), encoding="utf-8"))
    for k, v in rec.items():
        if k.startswith("_") or (claves and k not in claves):
            continue
        cx, cy, alto, asp = v
        im = cv2.imread(os.path.join(FOTOS, k + ".jpg"))
        if im is None:
            print("falta", k)
            continue
        h, w = im.shape[:2]
        ch = alto * h
        cw = ch * asp
        if cw > w:                                  # limitado por el ancho
            cw, ch = w, w / asp
        x0 = int(round(min(max(cx * w - cw / 2, 0), w - cw)))
        y0 = int(round(min(max(cy * h - ch / 2, 0), h - ch)))
        cv2.imwrite(os.path.join(FOTOS, k + "_rec.jpg"), im[y0:y0 + int(round(ch)), x0:x0 + int(round(cw))],
                    [cv2.IMWRITE_JPEG_QUALITY, 94])
        print(f"{k:14s} {int(round(cw))}x{int(round(ch))}")


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "recortar":
    recortar(sys.argv[2:] or None)
    sys.exit(0)


# ------------------------------------------------------------------ kit
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

import boceto as B  # noqa: E402
import pegflow  # noqa: E402,F401  (instala la capa hoja.fotos en Hoja.componer)
from motor import H, W  # noqa: E402

_CRED = None
_FUENTES = ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf"]
PAPEL = np.array([0.965, 0.945, 0.895], np.float32)        # blanco cálido de copia fotográfica vieja
TINTA_CRED = (68, 58, 50)
CINTA = np.array([0.975, 0.955, 0.865], np.float32)


def creditos():
    global _CRED
    if _CRED is None:
        _CRED = json.load(open(os.path.join(FOTOS, "creditos.json"), encoding="utf-8"))
    return _CRED


def _fuente(px):
    for f in _FUENTES:
        if os.path.exists(f):
            return ImageFont.truetype(f, int(px))
    return ImageFont.load_default()


def _ancho(txt, fnt):
    return fnt.getbbox(txt)[2]


def _lineas_credito(txt, ancho_max, fs):
    """Una línea si cabe; si no, dos partiendo por « / »; si aún no cabe, baja la letra (mín. 11 px)."""
    while True:
        fnt = _fuente(fs)
        if _ancho(txt, fnt) <= ancho_max:
            return [txt], fnt, fs
        partes = txt.split(" / ")
        if len(partes) > 1:
            mejor = None
            for i in range(1, len(partes)):
                a, b = " / ".join(partes[:i]), " / ".join(partes[i:])
                m = max(_ancho(a, fnt), _ancho(b, fnt))
                if mejor is None or m < mejor[0]:
                    mejor = (m, [a, b])
            if mejor[0] <= ancho_max:
                return mejor[1], fnt, fs
        if fs <= 11:
            return [txt], fnt, fs
        fs -= 1


def _tono(rgb, k):
    """Tono cálido leve: un poco menos de saturación, negros levantados hacia el papel, sesgo ámbar. Conserva el realismo."""
    if k <= 0:
        return rgb
    g = rgb.mean(axis=2, keepdims=True)
    out = rgb * (1 - 0.18 * k) + g * (0.18 * k)
    out = out * (1 - 0.06 * k) + 0.06 * k * PAPEL * 0.9
    out = out * np.array([1 + 0.035 * k, 1 + 0.005 * k, 1 - 0.07 * k], np.float32)
    return np.clip(out, 0, 1)


def _cinta(L, T, semilla):
    """Tira de cinta adhesiva L x T con los extremos rasgados (dientes). Devuelve (rgb, alfa)."""
    r = np.random.default_rng(semilla)
    a = np.zeros((T, L), np.float32)
    a[:] = 0.66
    # extremos en zigzag
    dien = max(3, T // 6)
    ys = np.arange(T)
    for lado in (0, 1):
        perfil = np.abs(((ys / max(1.0, T / 7.0)) + r.uniform(0, 1)) % 2 - 1) * dien + r.uniform(0, dien * 0.6, T)
        for y in range(T):
            n = int(perfil[y])
            if lado == 0:
                a[y, :n] = 0
            else:
                a[y, L - n:] = 0
    # fibras / brillo
    fib = cv2.GaussianBlur(r.normal(0, 1, (T, L)).astype(np.float32), (0, 0), sigmaX=6, sigmaY=0.8)
    a *= np.clip(1 + 0.10 * fib, 0.75, 1.25)
    brillo = np.linspace(-1, 1, T, dtype=np.float32)[:, None]
    rgb = np.empty((T, L, 3), np.float32)
    rgb[:] = CINTA
    rgb += (0.05 * np.exp(-((brillo - 0.35) ** 2) / 0.05))[..., None]
    a = cv2.GaussianBlur(a, (0, 0), 0.7)
    return np.clip(rgb, 0, 1), np.clip(a, 0, 1)


_IMG = {}
_CACHE = OrderedDict()
_MAXC = 160


def _foto(clave):
    if clave not in _IMG:
        ruta = os.path.join(FOTOS, clave + "_rec.jpg")
        if not os.path.exists(ruta):
            ruta = os.path.join(FOTOS, clave + ".jpg")
        im = cv2.imread(ruta)
        if im is None:
            raise FileNotFoundError(ruta)
        _IMG[clave] = im[..., ::-1].astype(np.float32) / 255.0
    return _IMG[clave]


@lru_cache(maxsize=48)
def _tarjeta(clave, alto_px, calido, cinta, semilla, credito, kc=1.0):
    """Copia sin girar: (rgb premultiplicado, alfa, ancla_x, ancla_y) en un lienzo con margen para cintas, giro y sombra."""
    foto = _foto(clave)
    asp = foto.shape[1] / foto.shape[0]
    Hc = alto_px
    m = max(6, int(round(0.045 * Hc)))
    fs = max(13, int(round(0.031 * Hc)))
    # primero con una línea de crédito; si hay que partirla, se recalcula
    for _ in range(2):
        nl = 1 if _ == 0 else len(lineas)
        mb = m + int(round(nl * fs * 1.32)) + max(3, int(0.012 * Hc))
        ph = Hc - m - mb
        pw = int(round(ph * asp))
        cw = pw + 2 * m
        lineas, fnt, fs2 = _lineas_credito(credito, pw, fs) if credito else ([], None, fs)
        if len(lineas) <= nl:
            break
    fs = fs2
    P = int(round(0.16 * max(cw, Hc))) + 24
    Wl, Hl = cw + 2 * P, Hc + 2 * P
    rgb = np.zeros((Hl, Wl, 3), np.float32)
    a = np.zeros((Hl, Wl), np.float32)
    r = np.random.default_rng(7 + semilla)
    # papel con grano y bordes un poco más amarillos
    x0, y0 = P, P
    papel = np.empty((Hc, cw, 3), np.float32)
    papel[:] = PAPEL
    grano = cv2.GaussianBlur(r.normal(0, 1, (Hc, cw)).astype(np.float32), (0, 0), 1.2) * 0.012
    papel += grano[..., None]
    yy, xx = np.mgrid[0:Hc, 0:cw].astype(np.float32)
    borde = np.minimum(np.minimum(xx, cw - 1 - xx), np.minimum(yy, Hc - 1 - yy))
    papel *= (1 - 0.035 * np.exp(-borde / max(2.0, 0.02 * Hc)))[..., None] * np.array([1, 0.995, 0.975], np.float32)
    rgb[y0:y0 + Hc, x0:x0 + cw] = papel
    a[y0:y0 + Hc, x0:x0 + cw] = 1.0
    # foto
    im = cv2.resize(foto, (pw, ph), interpolation=cv2.INTER_AREA if ph < foto.shape[0] else cv2.INTER_CUBIC)
    im = _tono(np.clip(im, 0, 1), calido)
    # leve sombra interior en el canto de la foto (se lee como copia pegada sobre la cartulina)
    rgb[y0 + m - 1:y0 + m + ph + 1, x0 + m - 1:x0 + m + pw + 1] *= 0.80
    rgb[y0 + m:y0 + m + ph, x0 + m:x0 + m + pw] = im
    # crédito
    if lineas:
        L = Image.new("L", (cw, mb), 0)
        d = ImageDraw.Draw(L)
        lh = int(round(fs * 1.32))
        ytxt = int(round((mb - m * 0.25 - lh * len(lineas)) / 2 + m * 0.10))
        for i, t in enumerate(lineas):
            tw = _ancho(t, fnt)
            d.text(((cw - tw) / 2, ytxt + i * lh), t, font=fnt, fill=255)
        tm = np.asarray(L, np.float32)[..., None] / 255.0
        zona = rgb[y0 + Hc - mb:y0 + Hc, x0:x0 + cw]
        zona[:] = zona * (1 - tm) + (np.array(TINTA_CRED, np.float32) / 255.0) * tm
    # cintas en las dos esquinas de arriba
    if cinta and kc > 0:
        Lt = int(round(0.30 * min(cw, Hc) + 0.06 * max(cw, Hc)))
        Tt = max(10, int(round(0.085 * min(cw, Hc) + 0.02 * max(cw, Hc))))
        for j, (cx, cy, ang) in enumerate(((x0 + 0.055 * cw, y0 + 0.045 * Hc, -38 + r.uniform(-6, 6)),
                                           (x0 + 0.945 * cw, y0 + 0.045 * Hc, 40 + r.uniform(-6, 6)))):
            trgb, ta = _cinta(Lt, Tt, semilla * 13 + j)
            ta = ta * kc
            Mr = cv2.getRotationMatrix2D((Lt / 2, Tt / 2), ang, 1.0)
            Mr[0, 2] += cx - Lt / 2
            Mr[1, 2] += cy - Tt / 2
            ta = cv2.warpAffine(ta, Mr, (Wl, Hl))
            trgb = cv2.warpAffine(trgb, Mr, (Wl, Hl))
            rgb = rgb * (1 - ta[..., None]) + trgb * ta[..., None]
            a = a + ta * (1 - a)
    rgb *= a[..., None]
    return np.ascontiguousarray(rgb), np.ascontiguousarray(a), P + cw / 2.0, P + Hc


_TEMBLOR = ((0.0, 0.0, 0.0), (0.55, -0.35, 0.10), (-0.45, 0.30, -0.08))   # (dx, dy, grados) por variante


def _version(clave, alto_px, calido, cinta, semilla, credito, var, uq, sqk, rotq):
    k = (clave, alto_px, calido, cinta, semilla, credito, var, uq, sqk, rotq)
    if k in _CACHE:
        _CACHE.move_to_end(k)
        return _CACHE[k]
    u = uq / 20.0
    kc = round(min(1.0, max(0.0, (u - 0.55) / 0.35)), 2)  # las cintas llegan al final de la entrada
    rgb, a, ax, ay = _tarjeta(clave, alto_px, calido, cinta, semilla, credito, kc)
    e = 1 - (1 - u) ** 3                       # sale rápido y aterriza suave
    dx, dy, dg = _TEMBLOR[var]
    ang = rotq * 0.25 + dg + 6.0 * (1 - e)
    esc = 1.0 + 0.10 * (1 - e)
    sq = sqk / 40.0
    Hl, Wl = a.shape
    M = cv2.getRotationMatrix2D((ax, ay), -ang, esc)
    if abs(sq) > 1e-3:                         # aplastar alrededor de los pies
        S = np.array([[1 + sq, 0, ax * -sq], [0, 1 - sq, ay * sq], [0, 0, 1]], np.float64)
        M = (S @ np.vstack([M, [0, 0, 1]]))[:2]
    M[0, 2] += dx
    M[1, 2] += dy
    rgb = cv2.warpAffine(rgb, M, (Wl, Hl), flags=cv2.INTER_LINEAR)
    a = cv2.warpAffine(a, M, (Wl, Hl), flags=cv2.INTER_LINEAR)
    # sombra: como las pegatinas del kit (7, 10 px, blur 6, 0,30), más lejana y difusa mientras «cae»
    lift = 1 - e
    ox, oy = 7 + 14 * lift, 10 + 20 * lift
    sh = cv2.warpAffine(a, np.float32([[1, 0, ox], [0, 1, oy]]), (Wl, Hl))
    sh = cv2.GaussianBlur(sh, (0, 0), 6.0 + 8 * lift) * (0.32 - 0.12 * lift)
    sh += cv2.GaussianBlur(cv2.warpAffine(a, np.float32([[1, 0, 1.5], [0, 1, 2.5]]), (Wl, Hl)), (0, 0), 1.6) * 0.18 * e
    sh = np.clip(sh, 0, 1)
    fade = min(1.0, u / 0.25) if u < 0.999 else 1.0
    a_out = (a + sh * (1 - a)) * fade
    rgb = rgb * fade
    ys, xs = np.nonzero(a_out > 0.003)
    if len(ys) == 0:
        _CACHE[k] = None
        return None
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    res = (np.ascontiguousarray(rgb[y0:y1, x0:x1]), np.ascontiguousarray(a_out[y0:y1, x0:x1]), ax - x0, ay - y0)
    _CACHE[k] = res
    if len(_CACHE) > _MAXC:
        _CACHE.popitem(last=False)
    return res


class FotoPeg:
    """Foto real impresa y pegada con cinta, con la interfaz de `boceto.Dib` / `pegflow.Peg`."""

    def __init__(self, clave, alto=400.0, dy=0.0, incl=None, calido=0.35, cinta=True, credito=None):
        self.clave = clave
        self.alto = float(alto)
        self.dy = dy
        self.semilla = sum(map(ord, clave))
        self.incl = (((self.semilla * 37) % 100) / 100.0 * 2 - 1) * 3.2 if incl is None else float(incl)
        if abs(self.incl) < 1.2 and incl is None:
            self.incl = 1.6 if self.incl >= 0 else -1.6
        self.calido = round(float(calido), 2)
        self.cinta = bool(cinta)
        self.credito = creditos().get(clave, {}).get("credito_corto", "") if credito is None else credito
        self.total = 1.0
        _foto(clave)                              # falla pronto si no existe

    def dibujar(self, hoja, x, y, s=1.0, rot=0.0, flip=False, u=1.0, fase_=0, semilla=0, ancho=1.0, sq=0.0, lapiz=0.0,
                tv=None, vida=1.0, peg=False):
        if u <= 0.001 or s <= 0.01:
            return
        resp = 1.0
        if tv is not None and vida > 0:
            resp = 1.0 + 0.007 * vida * math.sin(B.OMEGA * tv + semilla * 0.731)
        alto_px = int(round(self.alto * s * resp / 3.0)) * 3
        if alto_px < 60:
            return
        var = (int(fase_) + semilla) % 3 if vida > 0 else 0
        uq = int(round(min(1.0, u) * 20))
        sqk = int(round(max(-0.3, min(0.3, sq)) * 40))
        rotq = int(round((self.incl + math.degrees(rot)) * 4))
        v = _version(self.clave, alto_px, self.calido, self.cinta, self.semilla, self.credito, var, uq, sqk, rotq)
        if v is None:
            return
        rgb, a, ax, ay = v
        x0 = int(round(x - ax))
        y0 = int(round(y - ay + self.dy * alto_px))
        if not hasattr(hoja, "fotos"):
            hoja.fotos = []
        hoja.fotos.append((rgb, a, x0, y0))

    def caja(self, x, y, s=1.0):
        """Caja aproximada (x0, y0, x1, y1) en pantalla de la copia sin girar, para planear que no choque con rótulos."""
        foto = _foto(self.clave)
        Hc = self.alto * s
        m = 0.045 * Hc
        ph = Hc - m - (m + 0.031 * Hc * 1.32 * 1.5)
        cw = ph * foto.shape[1] / foto.shape[0] + 2 * m
        y1 = y + self.dy * Hc
        return (x - cw / 2, y1 - Hc, x + cw / 2, y1)


_FP = {}


def F(clave, alto=400.0, **kw):
    """FotoPeg compartida por clave (como `pegflow.P`)."""
    k = (clave, alto, tuple(sorted(kw.items())))
    if k not in _FP:
        _FP[k] = FotoPeg(clave, alto, **kw)
    return _FP[k]


def s_para(frac_alto=0.48, alto=400.0):
    """s para que la copia (marco incluido) ocupe `frac_alto` del alto de pantalla."""
    return frac_alto * H / alto
