# -*- coding: utf-8 -*-
"""Pegatinas de Flow dentro del kit de boceto + guache (historia_jalisco, 22-oct-2026).

Los dibujos NO se escriben por código: son piezas PNG recortadas de las hojas de Flow (`piezas/<hoja>/NN.png`, `nucleo/pegaflow.py
recortar`). `Peg` tiene la misma interfaz que `boceto.Dib.dibujar`, así que entra en `ga`/`pa`/`R.act` como cualquier dibujo del kit:
  - se ancla por los PIES (centro de abajo) en (x, y); s = 1 → `alto` px (400 por defecto, la talla de un personaje en pantalla);
  - lleva la pegatina del kit (silueta en `hoja.peg` → borde de papel y sombra) y un temblor de línea suave (3 variantes que se turnan
    con la fase del boceto), más una respiración mínima, para que no se vea «foto pegada» junto a los rótulos que hierven;
  - `u` < 1 la destapa en diagonal (entrada «pluma»); `sq` la aplasta (entrada «pop»); `rot` y `flip` como el kit.
La imagen se compone en el fondo ANTES del crayón y la tinta: los rótulos y números del kit quedan siempre encima.
"""
import math
import os
from collections import OrderedDict

import cv2
import numpy as np

import boceto as B
from motor import H, W

AQUI = os.path.dirname(os.path.abspath(__file__))
PIEZAS = os.path.join(AQUI, "piezas")


# ------------------------------------------------------------------ capa de imágenes en la Hoja del boceto
def _limpiar(self, _orig=B.Hoja.limpiar):
    _orig(self)
    self.fotos = []


def _componer(self):
    fotos = getattr(self, "fotos", None)
    base = B.PAPEL_F if self.fondo is None else self.fondo
    if self.hay_peg:
        base = self._aplicar_pegatinas(base)
    if fotos:
        if base is B.PAPEL_F:
            base = base.copy()
        for rgb, a, x0, y0 in fotos:
            h, w = a.shape
            xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
            if xb <= xa or yb <= ya:
                continue
            aa = a[ya - y0:yb - y0, xa - x0:xb - x0, None]
            b = base[ya:yb, xa:xb]
            b *= 1 - aa
            b += rgb[ya - y0:yb - y0, xa - x0:xb - x0]          # premultiplicado
    if B._comp_numba is None:
        return self._componer_numpy(base)
    out = np.empty_like(B.PAPEL_F)
    B._comp_numba(np.ascontiguousarray(base, dtype=np.float32), self.cal, B.TEX, self.cray, self.tinta, B._INK, self.hay_cray, out)
    return out


B.Hoja.limpiar = _limpiar
B.Hoja.componer = _componer


# ------------------------------------------------------------------ piezas
_RAW = {}
_CACHE = OrderedDict()
_MAXC = 420


def _cargar(ruta):
    """Recorta al contenido, salvo los cuadros de ciclo (lienzo común alineado por los pies: recortar los haría bailar)."""
    if ruta not in _RAW:
        im = cv2.imread(ruta, cv2.IMREAD_UNCHANGED)
        if im is None:
            raise FileNotFoundError(ruta)
        rgb = im[..., 2::-1].astype(np.float32) / 255.0
        a = im[..., 3].astype(np.float32) / 255.0
        if os.path.basename(ruta).startswith("ciclo_"):
            y0, y1, x0, x1 = 0, a.shape[0], 0, a.shape[1]
        else:
            ys, xs = np.nonzero(a > 0.04)
            y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
        _RAW[ruta] = (np.ascontiguousarray(rgb[y0:y1, x0:x1]), np.ascontiguousarray(a[y0:y1, x0:x1]))
    return _RAW[ruta]


def _hervor(rgb, a, var, amp):
    """Desplazamiento suave y pequeño (temblor de línea a mano), distinto en cada variante."""
    if var == 0 or amp <= 0:
        return rgb, a
    h, w = a.shape
    r = np.random.default_rng(1000 + var)
    gh, gw = max(2, h // 38), max(2, w // 38)
    dx = cv2.resize(r.normal(0, 1, (gh, gw)).astype(np.float32), (w, h), interpolation=cv2.INTER_CUBIC) * amp
    dy = cv2.resize(r.normal(0, 1, (gh, gw)).astype(np.float32), (w, h), interpolation=cv2.INTER_CUBIC) * amp
    mx, my = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))
    mx += dx
    my += dy
    return (cv2.remap(rgb, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT),
            cv2.remap(a, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT))


def _version(ruta, alto_px, flip, var, sqk):
    k = (ruta, alto_px, flip, var, sqk)
    if k in _CACHE:
        _CACHE.move_to_end(k)
        return _CACHE[k]
    rgb, a = _cargar(ruta)
    sq = sqk / 40.0
    hh = max(2, int(round(alto_px * (1 - sq))))
    ww = max(2, int(round(rgb.shape[1] * alto_px / rgb.shape[0] * (1 + sq))))
    interp = cv2.INTER_AREA if hh < rgb.shape[0] else cv2.INTER_CUBIC
    r2 = np.clip(cv2.resize(rgb, (ww, hh), interpolation=interp), 0, 1)
    a2 = np.clip(cv2.resize(a, (ww, hh), interpolation=interp), 0, 1)
    if flip:
        r2, a2 = r2[:, ::-1].copy(), a2[:, ::-1].copy()
    r2, a2 = _hervor(r2, a2, var, amp=min(1.6, 0.5 + hh / 260.0))
    m = (a2 > 0.5).astype(np.uint8) * 255
    _CACHE[k] = (np.ascontiguousarray(r2 * a2[..., None]), a2, m)        # rgb premultiplicado
    if len(_CACHE) > _MAXC:
        _CACHE.popitem(last=False)
    return _CACHE[k]


class Peg:
    """Pegatina de Flow con la interfaz de `boceto.Dib`."""

    def __init__(self, ruta, alto=400.0, dy=0.0):
        self.ruta = ruta if os.path.isabs(ruta) else os.path.join(PIEZAS, ruta)
        self.alto = float(alto)
        self.dy = dy                 # pies más arriba (+) o abajo (-) que el borde inferior de la pieza, en fracción del alto
        self.total = 1.0

    def dibujar(self, hoja, x, y, s=1.0, rot=0.0, flip=False, u=1.0, fase_=0, semilla=0, ancho=1.0, sq=0.0, lapiz=0.0,
                tv=None, vida=1.0, peg=False):
        if u <= 0.001 or s <= 0.01:
            return
        resp = 1.0
        if tv is not None and vida > 0:
            resp = 1.0 + 0.012 * vida * math.sin(B.OMEGA * tv + semilla * 0.731)
        alto_px = int(round(self.alto * s * resp / 3.0)) * 3
        if alto_px < 6:
            return
        sqk = int(round(max(-0.3, min(0.3, sq)) * 40))
        var = (int(fase_) + semilla) % 3 if vida > 0 else 0
        rgb, a, m = _version(self.ruta, alto_px, bool(flip), var, sqk)
        if abs(rot) > 0.01:                     # giro alrededor de los pies
            h, w = a.shape
            pad = int(0.25 * max(h, w))
            M = cv2.getRotationMatrix2D((w / 2 + pad, h + pad), -math.degrees(rot), 1.0)
            sz = (w + 2 * pad, h + 2 * pad)
            rgb = cv2.warpAffine(cv2.copyMakeBorder(rgb, pad, pad, pad, pad, cv2.BORDER_CONSTANT), M, sz)
            a = cv2.warpAffine(cv2.copyMakeBorder(a, pad, pad, pad, pad, cv2.BORDER_CONSTANT), M, sz)
            m = (a > 0.5).astype(np.uint8) * 255
            x0, y0 = int(round(x - w / 2 - pad)), int(round(y - h - pad + self.dy * h))
        else:
            h, w = a.shape
            x0, y0 = int(round(x - w / 2)), int(round(y - h + self.dy * h))
        if u < 0.999:                           # destape en diagonal con borde suave
            hh, ww = a.shape
            yy, xx = np.mgrid[0:hh, 0:ww].astype(np.float32)
            frente = (xx / max(1, ww) * 0.55 + yy / max(1, hh) * 0.45)
            k = np.clip((u * 1.15 - frente) / 0.12, 0, 1)
            a = a * k
            rgb = rgb * k[..., None]
            m = (a > 0.5).astype(np.uint8) * 255
        if peg:
            hoja.peg_mascara(m, x0, y0)
        if not hasattr(hoja, "fotos"):
            hoja.fotos = []
        hoja.fotos.append((rgb, a, x0, y0))


_PEGS = {}


def P(hoja, n, alto=400.0, dy=0.0):
    """Pieza n de la hoja (número del `_indice.jpg`)."""
    k = (hoja, n, alto, dy)
    if k not in _PEGS:
        _PEGS[k] = Peg(os.path.join(hoja, f"{n:02d}.png"), alto, dy)
    return _PEGS[k]


def ciclo(hoja, alto=400.0):
    """Cuadros del ciclo alineados por los pies (`ciclo_NN.png`)."""
    d = os.path.join(PIEZAS, hoja)
    fs = sorted(f for f in os.listdir(d) if f.startswith("ciclo_"))
    return [Peg(os.path.join(d, f), alto) for f in fs]
