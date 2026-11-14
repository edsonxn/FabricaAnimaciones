# -*- coding: utf-8 -*-
"""Anclas a la voz (ww), stickers de Flow limpios y lista de eventos de sonido (comunes a escenas.py y sonidos_navidad.py)."""
import json
import os
import re
import unicodedata

import cv2
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
TL = json.load(open(os.path.join(AQUI, "timeline.json"), encoding="utf-8"))
TOTAL = TL["total"]
ESC = {e["id"]: e for e in TL["escenas"]}
ORDEN = [e["id"] for e in TL["escenas"]]


def _n(s):
    s = unicodedata.normalize("NFD", s.lower())
    return re.sub(r"[^a-z0-9ñ]+", "", "".join(c for c in s if unicodedata.category(c) != "Mn"))


def ww(esc, frase, palabra, n=0, fin=False):
    """Segundo en que la voz dice `palabra` (varias palabras = secuencia) en la frase `frase` de la escena `esc`."""
    obj = [_n(x) for x in palabra.split()]
    ws = ESC[esc]["frases"][frase]["words"]
    nw = [_n(x["w"]) for x in ws]
    hits = [ws[i + len(obj) - 1]["e"] if fin else ws[i]["s"]
            for i in range(len(ws) - len(obj) + 1) if all(nw[i + j].startswith(obj[j]) for j in range(len(obj)))]
    if len(hits) <= n:
        raise KeyError(f"[{esc}/{frase}] palabra no encontrada: {palabra}")
    return hits[n]


def INI(esc, frase=0):
    return ESC[esc]["frases"][frase]["words"][0]["s"]


def FIN(esc, frase=-1):
    return ESC[esc]["frases"][frase]["words"][-1]["e"]


def T0(esc):
    return ESC[esc]["t0"]


def T1(esc):
    return ESC[esc]["t1"]


def NFRASES(esc):
    return len(ESC[esc]["frases"])


# ------------------------------------------------------------ stickers de Flow (limpios)
_RAW = {}


def stk(nombre, alto):
    """Sticker de stickers/<nombre>.png a `alto` px: quita los restos sueltos del recorte (islas chicas y halos tenues)."""
    import coquette as C
    ruta = os.path.join(AQUI, "stickers", nombre + ".png")
    dst = os.path.join(AQUI, "stickers", "_limpios", nombre + ".png")
    if ruta not in _RAW and os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(ruta):
        _RAW[ruta] = dst
    if ruta not in _RAW:
        from PIL import Image
        a = np.asarray(Image.open(ruta).convert("RGBA")).copy()
        m = (a[..., 3] > 140).astype(np.uint8)
        n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
        if n > 1:
            areas = st[1:, cv2.CC_STAT_AREA]
            keep = np.zeros(n, bool)
            keep[1:] = areas >= areas.max() * 0.06
            mk = keep[lab].astype(np.uint8)
            mk = cv2.dilate(mk, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
            a[..., 3] = (a[..., 3] * mk).astype(np.uint8)
        a[..., 3] = np.where(a[..., 3] < 60, 0, a[..., 3])
        ys, xs = np.nonzero(a[..., 3])
        a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        tmp = f"{dst}.{os.getpid()}.png"
        Image.fromarray(a).save(tmp)
        os.replace(tmp, dst)
        _RAW[ruta] = dst
    return C.sticker(_RAW[ruta], alto)
