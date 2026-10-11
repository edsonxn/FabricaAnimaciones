# -*- coding: utf-8 -*-
"""Edición tipo TikTok de un video REAL (clips/crudo.mp4): gancho en frío, cortes sin silencios, cámara rápida,
zooms de golpe, rótulos de énfasis anclados a las palabras, checklist de la parada, SFX y música.

    python editar.py tiempos           tabla de segmentos (crudo -> salida)
    python editar.py hoja 0.5 3.2 ...  cuadros sueltos a previews/c_<t>.jpg (segundos de SALIDA)
    python editar.py audio             solo audio/mezcla.wav
    python editar.py                   audio + render -> salida/trailero_parada2_MASTER.mp4
Los sonidos se generan antes con `python sonidos.py`.
"""
import math
import os
import subprocess
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
FFMPEG = r"C:\ffmpeg\bin\ffmpeg.exe"
SRC = "clips/crudo.mp4"
W, H, FPS = 1080, 1920, 30
SW, SH = 576, 1024
ESC = W / SW
SALIDA = "salida/trailero_parada2_MASTER.mp4"

# ------------------------------------------------------------------ montaje: (id, a, b, velocidad); velocidad 0 = cuadro congelado (b = duración)
SEG = [
    ("gancho", 21.74, 23.50, 1),
    ("gancho_f", 23.47, 0.60, 0),
    ("parada", 0.00, 3.98, 1),
    ("antoj", 4.28, 7.02, 1),
    ("oye", 7.30, 9.46, 1),
    ("congela", 9.40, 0.85, 0),
    ("camino", 9.60, 12.85, 2.5),
    ("ahi", 12.85, 16.30, 1),
    ("susto", 16.30, 23.52, 1),
    ("asegurar", 23.55, 30.72, 1),
    ("barra", 31.05, 36.80, 3.5),
    ("puertas", 36.87, 42.50, 3.5),
    ("oficina", 42.52, 46.24, 1),
    ("cabina", 46.55, 53.05, 1),
]
TL, _o = {}, 0.0
for _id, _a, _b, _v in SEG:
    _d = _b if _v == 0 else (_b - _a) / _v
    TL[_id] = dict(id=_id, a=_a, b=_b, v=_v, o0=_o, d=_d)
    _o += _d
TOTAL = _o
ORDEN = [TL[s[0]] for s in SEG]


def T(seg, s):
    """Segundo de SALIDA del segundo `s` del crudo dentro del segmento `seg`."""
    g = TL[seg]
    return g["o0"] + (0 if g["v"] == 0 else (s - g["a"]) / g["v"])


def INI(seg):
    return TL[seg]["o0"]


def FIN(seg):
    return TL[seg]["o0"] + TL[seg]["d"]


def seg_en(t):
    for g in ORDEN:
        if t < g["o0"] + g["d"]:
            return g
    return ORDEN[-1]


# ------------------------------------------------------------------ rótulos
IMPACT = r"C:\Windows\Fonts\impact.ttf"
EMOJI = r"C:\Windows\Fonts\seguiemj.ttf"
ARIALBD = r"C:\Windows\Fonts\arialbd.ttf"
B, Y, G, R_ = (255, 255, 255), (255, 228, 0), (70, 255, 40), (255, 48, 48)


def _es_emoji(c):
    return ord(c) >= 0x2190


def _tramos(txt):
    out = []
    for c in txt:
        e = _es_emoji(c)
        if out and out[-1][0] == e:
            out[-1][1] += c
        else:
            out.append([e, c])
    return out


def rotulo(lineas, tam=118, inclinar=0.16, giro=0, ancho_max=960):
    """Texto grueso estilo TikTok (Impact, borde negro, sombra) con emojis de color. lineas = [(texto, color)]."""
    f = ImageFont.truetype(IMPACT, tam)
    fe = ImageFont.truetype(EMOJI, int(tam * 0.86))
    sw = max(4, int(tam * 0.085))
    pad = sw + int(tam * 0.22)
    anchos = []
    for txt, _ in lineas:
        anchos.append(sum((fe if e else f).getlength(s) for e, s in _tramos(txt)))
    alto_l = int(tam * 1.12)
    cw, ch = int(max(anchos)) + 2 * pad, alto_l * len(lineas) + 2 * pad
    im = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    som = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    d, ds = ImageDraw.Draw(im), ImageDraw.Draw(som)
    for k, (txt, col) in enumerate(lineas):
        x = (cw - anchos[k]) / 2
        y = pad + alto_l * k + alto_l / 2
        for e, s in _tramos(txt):
            if e:
                d.text((x, y + tam * 0.02), s, font=fe, embedded_color=True, anchor="lm")
                x += fe.getlength(s)
            else:
                ds.text((x, y + tam * 0.09), s, font=f, fill=(0, 0, 0, 200), anchor="lm", stroke_width=sw, stroke_fill=(0, 0, 0, 200))
                d.text((x, y), s, font=f, fill=col + (255,), anchor="lm", stroke_width=sw, stroke_fill=(0, 0, 0, 255))
                x += f.getlength(s)
    som = som.filter(ImageFilter.GaussianBlur(tam * 0.035))
    im = Image.alpha_composite(som, im)
    if inclinar:
        extra = int(abs(inclinar) * ch) + 2
        lienzo = Image.new("RGBA", (cw + extra, ch), (0, 0, 0, 0))
        lienzo.paste(im, (extra // 2, 0))
        im = lienzo.transform(lienzo.size, Image.AFFINE, (1, inclinar, -inclinar * ch / 2, 0, 1, 0), Image.BICUBIC)
    if giro:
        im = im.rotate(giro, expand=True, resample=Image.BICUBIC)
    if im.width > ancho_max:
        k = ancho_max / im.width
        im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
    return _spr(im)


def _spr(im):
    a = np.asarray(im).astype(np.float32)
    return a[..., 2::-1].copy(), a[..., 3:4] / 255.0          # BGR, alfa


def etiqueta_tarima(ciudad="ASSONET, MA"):
    """Etiqueta de envío de tarima (la que lo asustó)."""
    w, h = 700, 300
    im = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((26, 30, w + 26, h + 30), 18, fill=(0, 0, 0, 150))
    d.rounded_rectangle((14, 14, w + 14, h + 14), 18, fill=(250, 248, 240, 255), outline=(20, 20, 20, 255), width=6)
    d.text((44, 34), "SHIP TO / ENTREGAR EN:", font=ImageFont.truetype(ARIALBD, 34), fill=(40, 40, 40, 255))
    d.text((w / 2 + 14, 138), ciudad, font=ImageFont.truetype(IMPACT, 112), fill=(10, 10, 10, 255), anchor="mm")
    rng = np.random.RandomState(7)
    x = 44
    while x < w - 30:
        g = int(rng.choice([3, 5, 8, 11]))
        d.rectangle((x, 216, x + g, 284), fill=(15, 15, 15, 255))
        x += g + int(rng.choice([4, 6, 9]))
    return _spr(im.rotate(-5, expand=True, resample=Image.BICUBIC))


def chip(txt, hecho, w=250, h=76):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if hecho:
        d.rounded_rectangle((2, 2, w - 3, h - 3), 22, fill=(70, 255, 40, 245), outline=(0, 0, 0, 255), width=4)
        col = (0, 0, 0, 255)
        d.line((20, 39, 31, 51, 50, 24), fill=col, width=8, joint="curve")
    else:
        d.rounded_rectangle((2, 2, w - 3, h - 3), 22, fill=(0, 0, 0, 150), outline=(255, 255, 255, 215), width=3)
        col = (255, 255, 255, 235)
        d.rounded_rectangle((20, 24, 48, 52), 5, outline=col, width=3)
    d.text((60, h / 2 + 1), txt, font=ImageFont.truetype(IMPACT, 41), fill=col, anchor="lm")
    return _spr(im)


def pastilla(txt, tam=50):
    f, fe = ImageFont.truetype(IMPACT, tam), ImageFont.truetype(EMOJI, int(tam * 0.84))
    an = sum((fe if e else f).getlength(s) for e, s in _tramos(txt))
    w, h = int(an) + 64, tam + 34
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((2, 2, w - 3, h - 3), h // 2, fill=(255, 228, 0, 250), outline=(0, 0, 0, 255), width=5)
    x = 32
    for e, s in _tramos(txt):
        if e:
            d.text((x, h / 2 + 1), s, font=fe, embedded_color=True, anchor="lm")
            x += fe.getlength(s)
        else:
            d.text((x, h / 2), s, font=f, fill=(0, 0, 0, 255), anchor="lm")
            x += f.getlength(s)
    return _spr(im)


def pegar(fr, spr, cx, cy, esc=1.0, alfa=1.0):
    bgr, a = spr
    if abs(esc - 1) > 0.004:
        nw, nh = max(2, int(bgr.shape[1] * esc)), max(2, int(bgr.shape[0] * esc))
        it = cv2.INTER_LINEAR if esc > 1 else cv2.INTER_AREA
        bgr = cv2.resize(bgr, (nw, nh), interpolation=it)
        a = cv2.resize(a, (nw, nh), interpolation=it)[..., None]
    h, w = bgr.shape[:2]
    x0, y0 = int(round(cx - w / 2)), int(round(cy - h / 2))
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    if xa >= xb or ya >= yb:
        return
    sb, sa = bgr[ya - y0:yb - y0, xa - x0:xb - x0], a[ya - y0:yb - y0, xa - x0:xb - x0] * alfa
    reg = fr[ya:yb, xa:xb].astype(np.float32)
    fr[ya:yb, xa:xb] = (reg * (1 - sa) + sb * sa).astype(np.uint8)


# ------------------------------------------------------------------ eventos
ROT, SON, PUNCH, TEMBLOR, FLASH = [], [], [], [], []


def son(nombre, t, vol=0.6):
    SON.append((nombre, max(0.0, t), vol))


def rot(seg, s, dur, lineas, y, tam=118, x=540, sfx="pop", vol=0.3, tiembla=0, giro=0, punch=0.0, spr=None, entrada="golpe"):
    t0 = T(seg, s)
    ROT.append(dict(t0=t0, dur=dur, spr=spr or rotulo(lineas, tam, giro=giro), x=x, y=y, tiembla=tiembla, entrada=entrada))
    if sfx:
        son(sfx, t0 - 0.03, vol)
    if punch:
        PUNCH.append((t0, punch, 0.16))


def temblor(t, amp=14, dur=0.4):
    TEMBLOR.append((t, amp, dur))


# --- gancho en frío
rot("gancho", 21.78, 0.82, [("¡A LA MADRE! 😱", Y)], 1340, 150, sfx="golpe", vol=0.9, punch=0.16)
rot("gancho", 22.66, 1.44, [("¿NO ME", B), ("DESCARGARON", B)], 1250, 128, sfx="pop", vol=0.4)
rot("gancho", 23.24, 0.86, [("NADA?", R_)], 1500, 210, sfx="boom", vol=0.9, tiembla=7, punch=0.22)
temblor(T("gancho", 23.24), 16, 0.45)
son("drama", INI("gancho_f") - 0.05, 0.55)
son("glitch", FIN("gancho_f") - 0.12, 0.6)
son("whoosh", FIN("gancho_f") - 0.2, 0.7)
FLASH.append((INI("parada"), 0.7))
# --- ya estamos descargados en esta parada
rot("parada", 0.02, 0.95, [("AHORA SÍ 😎", B)], 1330, 124, sfx=None)
rot("parada", 2.04, 1.25, [("DESCARGADOS ✅", G)], 1330, 136, sfx="ding", vol=0.5, punch=0.10)
rot("parada", 3.44, 0.56, [("...PARADA 😏", Y)], 1330, 130, sfx="pop", vol=0.45, punch=0.14)
# --- antojados, perros desgraciados
rot("antoj", 4.70, 1.05, [("ANTOJADOS 🤨", B)], 1330, 136, sfx="pop", vol=0.45, punch=0.10)
rot("antoj", 5.84, 1.16, [("PERROS", Y), ("DESGRACIADOS 🤣", Y)], 1320, 132, sfx="boom", vol=0.7, tiembla=5, punch=0.16)
temblor(T("antoj", 5.84), 13, 0.5)
# --- ¿por qué se me antoja a mí también?
rot("oye", 7.36, 0.80, [("OYE... 🤔", B)], 1360, 120, sfx=None)
rot("oye", 8.20, 1.22, [("¿POR QUÉ SE ME", B), ("ANTOJA A MÍ?", B)], 1340, 112, sfx="pop", vol=0.35)
rot("congela", 0, 0.83, [("¿¿A MÍ TAMBIÉN?? 💀", Y)], 1320, 138, sfx="boom", vol=1.0, tiembla=5, punch=0.22)
son("scratch", INI("congela") - 0.08, 0.6)
# --- camino a la caja (cámara rápida)
son("latigo", INI("camino") - 0.05, 0.7)
son("rapido", INI("camino"), 0.3)
rot("camino", 9.75, 1.15, [("A VER LA CAJA 👀", B)], 1380, 120, sfx=None, entrada="suave")
FLASH.append((INI("camino"), 0.45))
# --- ahí está, ya nos descargaron
son("whoosh", INI("ahi") - 0.1, 0.5)
rot("ahi", 14.02, 0.74, [("AHÍ ESTÁ 👉", B)], 1400, 128, sfx="pop", vol=0.4, punch=0.08)
rot("ahi", 15.34, 0.92, [("YA NOS", G), ("DESCARGARON ✅", G)], 1380, 124, sfx=None, punch=0.10)
# --- el susto
rot("susto", 16.94, 0.70, [("ME ASUSTÉ 😨", Y)], 1420, 136, sfx="pop", vol=0.45, punch=0.12)
rot("susto", 17.66, 0.54, [("LAS PALETAS DICEN...", B)], 1430, 96, sfx=None)
rot("susto", 18.20, 1.16, None, 1400, spr=etiqueta_tarima(), sfx="golpe", vol=0.7, punch=0.12)
rot("susto", 19.40, 1.80, [("¡LA PARADA", B), ("DE AYER! ⏪", Y)], 1410, 122, sfx="scratch", vol=0.4, punch=0.08)
son("subida", T("susto", 23.24) - 1.45, 0.45)
rot("susto", 21.78, 0.84, [("¡A LA MADRE! 😱", Y)], 1420, 146, sfx="pop", vol=0.5, punch=0.14)
rot("susto", 22.66, 0.84, [("¿NO ME", B), ("DESCARGARON", B)], 1340, 124, sfx=None)
rot("susto", 23.24, 0.42, [("NADA?", R_)], 1560, 190, sfx="boom", vol=0.9, tiembla=7, punch=0.2)
temblor(T("susto", 23.24), 15, 0.4)
# --- asegurar la carga
FLASH.append((INI("asegurar"), 0.35))
rot("asegurar", 23.62, 0.70, [("PERO BUENO... 😅", B)], 1420, 110, sfx=None)
rot("asegurar", 24.50, 1.30, [("ASEGURAR", B), ("LA CARGA 🔒", Y)], 1400, 126, sfx="pop", vol=0.45, punch=0.10)
rot("asegurar", 26.62, 0.66, [("QUE NO SE CAIGA...", B)], 1430, 104, sfx=None)
rot("asegurar", 27.28, 0.58, [("¡NI MADRES! 🤣", Y)], 1410, 144, sfx="boom", vol=0.6, tiembla=4, punch=0.16)
rot("asegurar", 28.52, 1.20, [("Y NOS VAMOS", B), ("A LA ÚLTIMA 🚛💨", G)], 1400, 120, sfx="whoosh", vol=0.5, punch=0.08)
rot("asegurar", 29.94, 0.78, [("¡VAMOS A DARLE! 🔥", Y)], 1410, 140, sfx="golpe", vol=0.9, tiembla=4, punch=0.22)
son("claxon", T("asegurar", 29.94), 0.4)
temblor(T("asegurar", 29.94), 12, 0.4)
# --- cámara rápida: barra y puertas
for _s, _txt, _sx, _ts in (("barra", [("ASEGURANDO", B), ("LA CARGA 🔒", Y)], "trinquete", 0.55),
                           ("puertas", [("CERRANDO", B), ("PUERTAS 🚪", Y)], "puerta", None)):
    FLASH.append((INI(_s), 0.5))
    son("latigo", INI(_s) - 0.06, 0.6)
    son("rapido", INI(_s), 0.35)
    ROT.append(dict(t0=INI(_s) + 0.05, dur=TL[_s]["d"] - 0.1, spr=rotulo(_txt, 112), x=540, y=1420, tiembla=0, entrada="suave"))
    if _ts:
        son(_sx, INI(_s) + _ts, 0.6)
son("puerta", T("puertas", 39.9), 0.75)
temblor(T("puertas", 40.3), 9, 0.3)
# --- por los papeles a la oficina
FLASH.append((INI("oficina"), 0.4))
son("whoosh", T("oficina", 43.03) - 0.12, 0.6)
FLASH.append((T("oficina", 43.03), 0.35))
rot("oficina", 43.46, 1.06, [("POR LOS PAPELES 📄", B)], 520, 118, sfx="pop", vol=0.4, punch=0.08)
rot("oficina", 44.56, 0.66, [("A LA OFICINA 🏢", Y)], 520, 124, sfx="pop", vol=0.35)
rot("oficina", 45.28, 0.92, [("¡VAMOS A DARLE! 🔥", Y)], 520, 134, sfx="golpe", vol=0.8, punch=0.18)
# --- papeles en mano, a la tercera tirada
son("whoosh", T("cabina", 46.9) - 0.12, 0.6)
FLASH.append((T("cabina", 46.9), 0.4))
rot("cabina", 47.30, 1.22, [("PAPELES EN MANO 📄", G)], 490, 122, sfx=None, punch=0.10)
rot("cabina", 48.56, 0.78, [("LISTO 😎", B)], 490, 140, sfx="pop", vol=0.4, punch=0.08)
rot("cabina", 49.72, 1.42, [("A LA 3RA TIRADA 🚛💨", Y)], 490, 128, sfx="golpe", vol=0.8, punch=0.16)
T_CIERRE = T("cabina", 51.34)
rot("cabina", 51.34, TOTAL - T_CIERRE, [("¿LLEGAMOS A LA 3RA?", B)], 480, 112, sfx="whoosh", vol=0.6, punch=0.14)
ROT.append(dict(t0=T_CIERRE + 0.28, dur=TOTAL - T_CIERRE - 0.28, spr=rotulo([("SÍGUEME 👉", G)], 170), x=540, y=1400, tiembla=0, entrada="golpe"))
son("golpe", T_CIERRE + 0.28, 0.8)
son("claxon", T("cabina", 51.9), 0.45)

# checklist de la parada: (texto, segundo de salida en que se palomea)
CHECK = [("DESCARGA", T("ahi", 15.36)), ("CARGA", FIN("barra") - 0.22), ("PUERTAS", FIN("puertas") - 0.22), ("PAPELES", T("cabina", 47.86))]
for _, _t in CHECK:
    son("ding", _t - 0.02, 0.55)
CHIPS = [(chip(n, False), chip(n, True)) for n, _ in CHECK]
PASTILLA = pastilla("🚛 PARADA 2 DE 3", 62)
RAPIDO = rotulo([("⏩ x3", B)], 84, inclinar=0)

# cámara: (segmento, segundo del crudo, zoom, cx, cy) -> se mantiene hasta el siguiente (zoom de corte)
CAM = [
    ("gancho", 21.74, 1.16, .54, .50), ("gancho", 22.66, 1.30, .56, .52), ("gancho_f", 0, 1.42, .56, .52),
    ("parada", 0.00, 1.05, .58, .42), ("parada", 2.04, 1.20, .60, .42), ("parada", 3.44, 1.32, .60, .42),
    ("antoj", 4.28, 1.06, .58, .43), ("antoj", 5.84, 1.30, .56, .40),
    ("oye", 7.30, 1.04, .50, .34), ("congela", 0, 1.22, .52, .33),
    ("camino", 9.60, 1.05, .50, .50),
    ("ahi", 12.85, 1.05, .50, .50), ("ahi", 14.84, 1.14, .50, .52),
    ("susto", 16.30, 1.05, .47, .52), ("susto", 16.94, 1.20, .47, .52), ("susto", 17.66, 1.05, .47, .52), ("susto", 18.20, 1.16, .47, .52),
    ("susto", 19.40, 1.05, .48, .50), ("susto", 21.78, 1.20, .52, .52), ("susto", 22.66, 1.34, .54, .53),
    ("asegurar", 23.55, 1.05, .48, .52), ("asegurar", 25.60, 1.16, .48, .52), ("asegurar", 27.28, 1.30, .48, .52),
    ("asegurar", 27.90, 1.05, .48, .52), ("asegurar", 29.58, 1.20, .48, .52),
    ("barra", 31.05, 1.05, .50, .50), ("puertas", 36.87, 1.05, .50, .50),
    ("oficina", 42.52, 1.05, .50, .50), ("oficina", 43.03, 1.08, .50, .58), ("oficina", 44.98, 1.24, .50, .60),
    ("cabina", 46.55, 1.08, .50, .58), ("cabina", 46.90, 1.05, .60, .58), ("cabina", 48.56, 1.18, .62, .60),
    ("cabina", 49.72, 1.30, .62, .60), ("cabina", 51.04, 1.08, .60, .58), ("cabina", 51.34, 1.22, .62, .60),
]
CAMT = sorted((T(s, a), z, cx, cy) for s, a, z, cx, cy in CAM)
DERIVA = {"barra": 0.10, "puertas": 0.10, "camino": 0.0, "oye": 0.14}       # empuje lento extra por segmento


def camara(t):
    k = 0
    for i, c in enumerate(CAMT):
        if c[0] <= t + 1e-6:
            k = i
    t0, z, cx, cy = CAMT[k]
    g = seg_en(t)
    z += min(0.05, 0.022 * (t - t0))                                          # nunca quieto: empuje continuo
    if g["id"] in DERIVA:
        z += DERIVA[g["id"]] * (t - g["o0"]) / g["d"]
    for tp, amp, tau in PUNCH:
        if t >= tp - 1e-6:
            z += amp * math.exp(-(t - tp) / tau)
    dx = dy = 0.0
    for tt, amp, dur in TEMBLOR:
        if tt <= t < tt + dur:
            k2 = (1 - (t - tt) / dur) ** 1.5 * amp
            n = int(round(t * FPS))
            dx += k2 * math.sin(n * 2.9 + 1.3)
            dy += k2 * math.cos(n * 3.7 + 0.4)
    return z, cx, cy, dx, dy


# ------------------------------------------------------------------ lectura del crudo
class Lector:
    def __init__(self):
        self.cap = cv2.VideoCapture(SRC)
        self.n = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.pos, self.idx, self.fr = 0, -1, None

    def leer(self, i):
        i = max(0, min(self.n - 2, int(i)))
        if i == self.idx:
            return self.fr
        if i < self.pos or i > self.pos + 90:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            self.pos = i
        while self.pos <= i:
            ok, f = self.cap.read()
            self.pos += 1
            if ok:
                self.fr = f
        self.idx = i
        return self.fr


_yy, _xx = np.mgrid[0:H, 0:W].astype(np.float32)
_r = np.sqrt(((_xx - W / 2) / (W * 0.72)) ** 2 + ((_yy - H / 2) / (H * 0.62)) ** 2)
VIN = np.clip((_r - 0.45) / 0.65, 0, 1)[..., None] ** 1.6
del _yy, _xx, _r


def anim(u, dur, entrada):
    """escala y alfa de un rótulo a los `u` s de aparecer."""
    if entrada == "suave":
        a = min(1, u / 0.15) * min(1, (dur - u) / 0.15)
        return 1 + 0.02 * math.sin(u * 9), max(0, a)
    e = min(1.0, u / 0.15)
    esc = 1 + 0.75 * (1 - e) ** 3 - 0.07 * math.sin(math.pi * min(1.0, u / 0.3)) * (u < 0.3)
    esc *= 1 + 0.018 * math.sin(u * 11)
    alfa = min(1.0, u / 0.06)
    cola = dur - u
    if cola < 0.10:
        alfa *= max(0, cola / 0.10)
        esc *= 0.86 + 0.14 * cola / 0.10
    return esc, alfa


def cuadro(n, lec):
    t = n / FPS
    g = seg_en(t)
    # --- fuente
    if g["v"] == 0:
        src = lec.leer(round(g["a"] * FPS)).astype(np.float32)
    elif g["v"] == 1:
        src = lec.leer(round((g["a"] + (t - g["o0"])) * FPS)).astype(np.float32)
    else:                                                                    # cámara rápida con estela de movimiento
        i1 = round((g["a"] + (t - g["o0"]) * g["v"]) * FPS)
        i0 = max(round(g["a"] * FPS), i1 - int(g["v"]))
        src = np.mean([lec.leer(i).astype(np.float32) for i in range(i0, i1 + 1)], axis=0)
    # --- cámara
    z, cx, cy, dx, dy = camara(t)
    s = ESC * z
    hw, hh = (W / 2 + abs(dx)) / s, (H / 2 + abs(dy)) / s
    px = min(max(cx * SW, hw), SW - hw) if hw * 2 <= SW else SW / 2
    py = min(max(cy * SH, hh), SH - hh) if hh * 2 <= SH else SH / 2
    M = np.float32([[s, 0, W / 2 + dx - s * px], [0, s, H / 2 + dy - s * py]])
    f = cv2.warpAffine(src, M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)
    f = cv2.addWeighted(f, 1.55, cv2.GaussianBlur(f, (0, 0), 2.0), -0.55, 0)                 # nitidez tras ampliar
    # --- color
    gris = (f[..., 0] * 0.114 + f[..., 1] * 0.587 + f[..., 2] * 0.299)[..., None]
    congelado = g["v"] == 0
    sat = 1.16
    if g["id"] == "congela":
        sat = 0.0
    f = gris + (f - gris) * sat
    f = (f - 128) * (1.22 if g["id"] == "congela" else 1.07) + 130
    vin = 0.55 if congelado else 0.16
    f *= 1 - vin * VIN
    if g["id"] in ("gancho_f",) or (g["id"] == "susto" and t >= T("susto", 23.24)) or (g["id"] == "gancho" and t >= T("gancho", 23.24)):
        f[..., 2] += 46 * VIN[..., 0] + 14                                                  # tinte rojo de alarma
        f[..., :2] *= 0.90
    for tf, fa in FLASH:
        if tf <= t < tf + 0.14:
            k = fa * (1 - (t - tf) / 0.14)
            f = f * (1 - k) + 255 * k
    fr = np.clip(f, 0, 255).astype(np.uint8)
    tg = FIN("gancho_f")
    if tg - 0.14 <= t < tg + 0.12:                                                           # glitch del corte de gancho
        rng = np.random.RandomState(n)
        d = int(rng.randint(10, 26))
        fr[..., 2] = np.roll(fr[..., 2], d, axis=1)
        fr[..., 0] = np.roll(fr[..., 0], -d, axis=1)
        for _ in range(6):
            y0, alto = int(rng.randint(0, H - 90)), int(rng.randint(20, 90))
            fr[y0:y0 + alto] = np.roll(fr[y0:y0 + alto], int(rng.randint(-90, 90)), axis=1)
    # --- checklist
    ah = min(1.0, t / 0.25)
    pegar(fr, PASTILLA, 540, 226, 1 + 0.5 * (1 - ah) ** 2, ah)
    for k, (_, tc) in enumerate(CHECK):
        x = 154 + k * 257
        ap = min(1.0, max(0.0, (t - 0.12 - 0.06 * k) / 0.2))
        if ap <= 0:
            continue
        if t >= tc:
            u = t - tc
            pegar(fr, CHIPS[k][1], x, 326, 1 + 0.55 * math.exp(-u / 0.12) * math.cos(u * 14), 1.0)
        else:
            pegar(fr, CHIPS[k][0], x, 326 + 30 * (1 - ap) ** 2, 1.0, ap)
    # --- rótulos
    for r in ROT:
        u = t - r["t0"]
        if 0 <= u < r["dur"]:
            esc, alfa = anim(u, r["dur"], r["entrada"])
            ox = oy = 0
            if r["tiembla"]:
                ox, oy = r["tiembla"] * math.sin(n * 2.3), r["tiembla"] * math.cos(n * 3.1)
            pegar(fr, r["spr"], r["x"] + ox, r["y"] + oy, esc, alfa)
    if g["v"] > 1 and int(t * 5) % 2 == 0:
        pegar(fr, RAPIDO, 880, 470, 1.0, 0.95)
    return fr


# ------------------------------------------------------------------ audio
def audio():
    import librosa
    import soundfile as sf
    SR = 48000
    os.makedirs("audio", exist_ok=True)
    subprocess.run([FFMPEG, "-v", "error", "-y", "-i", SRC, "-vn", "-ar", str(SR), "-ac", "2", "audio/crudo.wav"], check=True)
    x, _ = sf.read("audio/crudo.wav", always_2d=True, dtype="float32")
    N = int(round(TOTAL * SR))
    voz, hay = np.zeros((N, 2), np.float32), np.zeros(N, np.float32)
    f = int(0.008 * SR)
    for g in ORDEN:
        if g["v"] != 1:
            continue
        c = x[int(g["a"] * SR):int(g["b"] * SR)].copy()
        c[:f] *= np.linspace(0, 1, f)[:, None]
        c[-f:] *= np.linspace(1, 0, f)[:, None]
        i = int(g["o0"] * SR)
        c = c[:N - i]
        voz[i:i + len(c)] += c
        hay[i:i + len(c)] = 1
    hay[int(T_CIERRE * SR):] = 0.45                                           # cierre: sube la música bajo la última frase
    sf.write("audio/voz_cruda.wav", voz, SR)
    subprocess.run([FFMPEG, "-v", "error", "-y", "-i", "audio/voz_cruda.wav", "-af",
                    "highpass=f=85,afftdn=nf=-30,acompressor=threshold=-26dB:ratio=3.2:attack=6:release=140:makeup=1,"
                    "volume=11dB,alimiter=limit=0.84:attack=3:release=60", "-ar", str(SR), "audio/voz.wav"], check=True)
    voz, _ = sf.read("audio/voz.wav", always_2d=True, dtype="float32")
    voz = voz[:N]
    rms_v = float(np.sqrt(np.mean(voz[np.abs(voz).max(1) > 0.02] ** 2)))
    # efectos
    fx, cache = np.zeros((N, 2), np.float32), {}
    for nom, t, v in SON:
        if nom not in cache:
            y, _ = librosa.load(f"sfx/{nom}.mp3", sr=SR, mono=False)
            y = np.vstack([y, y]) if y.ndim == 1 else y[:2]
            ini = int(np.argmax(np.abs(y).max(0) > 0.03 * np.abs(y).max()))
            y = y[:, ini:] / (np.abs(y).max() + 1e-9) * 0.6
            q = min(int(0.08 * SR), y.shape[1])
            y[:, -q:] *= np.linspace(1, 0, q, dtype=np.float32)
            cache[nom] = y.T.astype(np.float32)
        y = cache[nom]
        i = int(t * SR)
        y = y[:max(0, N - i)] * v
        fx[i:i + len(y)] += y
    fx *= 0.56
    # música: baja bajo la voz, sube en los tramos sin voz
    mus = np.zeros((N, 2), np.float32)
    if os.path.exists("audio/lyria.mp3"):
        m, _ = librosa.load("audio/lyria.mp3", sr=SR, mono=False)
        m = (np.vstack([m, m]) if m.ndim == 1 else m[:2]).T
        ini = int(np.argmax(np.abs(m).max(1) > 0.05 * np.abs(m).max()))
        m = m[ini:ini + N]
        m = m / (np.sqrt(np.mean(m ** 2)) + 1e-9)
        k = int(0.18 * SR)
        env = np.convolve(hay, np.ones(k) / k, mode="same")
        gan_db = -8.5 - 11.5 * env                                             # -18 dB bajo la voz, -8.5 sin voz (respecto a la voz)
        gan = rms_v * 10 ** (gan_db / 20)
        mus[:len(m)] = m * gan[:len(m), None]
        q = int(0.5 * SR)
        mus[-q:] *= np.linspace(1, 0, q)[:, None]
    mez = voz + fx + mus
    sf.write("audio/mezcla_cruda.wav", mez, SR)
    subprocess.run([FFMPEG, "-v", "error", "-y", "-i", "audio/mezcla_cruda.wav", "-af", "volume=3.5dB,alimiter=limit=0.93:attack=3:release=50",
                    "-ar", str(SR), "audio/mezcla.wav"], check=True)
    act = np.abs(voz).max(1) > 0.02
    fondo = float(np.sqrt(np.mean((fx + mus)[act] ** 2)))
    print(f"audio/mezcla.wav  {TOTAL:.2f} s  voz/fondo = {20 * math.log10(rms_v / (fondo + 1e-9)):.1f} dB  pico {np.abs(mez).max():.2f}  "
          f"({len(SON)} efectos, música {'sí' if mus.any() else 'NO'})")


def render():
    os.makedirs("salida", exist_ok=True)
    nf = int(round(TOTAL * FPS))
    p = subprocess.Popen([FFMPEG, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", "audio/mezcla.wav", "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", SALIDA], stdin=subprocess.PIPE)
    lec = Lector()
    for n in range(nf):
        p.stdin.write(cuadro(n, lec).tobytes())
        if n % 150 == 0:
            print(f"  {n}/{nf}", flush=True)
    p.stdin.close()
    p.wait()
    print(SALIDA, f"{TOTAL:.2f} s")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "tiempos":
        for g in ORDEN:
            print(f"{g['o0']:6.2f}-{g['o0'] + g['d']:6.2f}  {g['id']:9s} crudo {g['a']:5.2f}-{(g['b'] if g['v'] else g['a']):5.2f}  x{g['v']}")
        print(f"total {TOTAL:.2f} s; {len(ROT)} rótulos, {len(SON)} efectos")
    elif a and a[0] == "hoja":
        lec = Lector()
        os.makedirs("previews", exist_ok=True)
        chicos = []
        for s in a[1:]:
            fr = cuadro(int(round(float(s) * FPS)), lec)
            cv2.imwrite(f"previews/c_{float(s):06.2f}.jpg", fr, [cv2.IMWRITE_JPEG_QUALITY, 90])
            ch = cv2.resize(fr, (324, 576), interpolation=cv2.INTER_AREA)
            cv2.putText(ch, s, (8, 566), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            chicos.append(ch)
        while len(chicos) % 6:
            chicos.append(np.zeros_like(chicos[0]))
        cv2.imwrite("previews/hoja.jpg", np.vstack([np.hstack(chicos[i:i + 6]) for i in range(0, len(chicos), 6)]))
        print("previews/hoja.jpg listo")
    elif a and a[0] == "audio":
        audio()
    else:
        audio()
        render()
