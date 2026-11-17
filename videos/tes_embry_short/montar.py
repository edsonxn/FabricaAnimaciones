# -*- coding: utf-8 -*-
"""Montaje del Short vertical «Skyrim con IA»: 13 momentos de la serie de Embry, cámara que sigue la cara de quien habla
y golpe de zoom en el remate, barra «EGO DE EDSON» (barra de vida de Skyrim que se encoge al centro), bips, emojis,
SFX meme y la OST de taberna (The Bannered Mare, Jeremy Soule).

Uso:
  python montar.py --hoja t1 t2 ...      cuadros finales en previews/fx_NN.jpg (sin codificar)
  python montar.py --hoja-golpes          un cuadro por momento 0,35 s después del golpe + inicio → previews/fx_*.jpg
  python montar.py                        render completo → salida/tes_embry_short_MASTER.mp4 (+ .srt)
"""
import json, math, os, subprocess, sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))
import mg_tes as T  # noqa: E402

FPS, W, H, SR = 30, 1080, 1920, 48000
WIN_Y0, WIN_H = 300, 1350           # ventana del juego 4:5 (1080x1350)
CLIPS = os.path.join(AQUI, "segmentos", "clips")
HUESO, ORO, SANGRE = T.HUESO, T.ORO, T.SANGRE

ORDEN = ["hijas", "alcohol", "orca", "pan", "sombrero", "dormir", "yelmo", "dorthe", "diego", "trio", "fracaso",
         "autografo", "tiktok"]
EGO = {"hijas": -5, "alcohol": -3, "orca": -4, "pan": -3, "sombrero": -12, "dormir": -6, "yelmo": +15, "dorthe": -3,
       "diego": -4, "trio": -10, "fracaso": -5, "autografo": -18, "tiktok": -42}
EMO = {"hijas": "😭", "alcohol": "🍺", "orca": "🗿", "pan": "🍞", "sombrero": "💀", "dormir": "🤨", "yelmo": "🤡",
       "dorthe": "💀", "diego": "☀️", "trio": "😂", "fracaso": "🤢", "autografo": "✍️", "tiktok": "🤨"}
SFX_MEME = {"skull": "boom_1", "boom": "boom_2", "ding": "ding", "bruh": "bruh", "risas": "risas", "scratch": "scratch"}
SIN_CARA = {"trio": (49, 48, 18)}   # no se ve la cara de frente: encuadre fijo al grupo
# Cara de quien dice el remate, marcada a mano cada ~0,5 s sobre los cuadros reales (el Haar de caras.py fallaba
# con las caras del juego: Lemkil y Tulio salían cortados y en «pan» hacía zoom al plato). h = alto de la cara en %.
MANO = {
    "hijas": (11, [(27.64, 85, 28), (28.19, 53, 24), (28.69, 53, 24), (29.19, 60, 20), (29.69, 55, 16), (30.19, 53, 17),
                   (30.69, 71, 28), (31.01, 71, 28), (36.0, 51, 37), (37.05, 53, 37), (38.05, 52, 37), (38.55, 53, 35),
                   (39.05, 57, 46), (39.29, 59, 45), (39.55, 53, 39), (40.05, 52, 35), (40.55, 52, 36), (40.75, 52, 36)]),
    "alcohol": (24, [(12.6, 51, 24), (13.15, 52, 30), (13.65, 61, 33), (14.15, 52, 33), (14.49, 52, 33),
                     (24.16, 50, 35), (25.71, 52, 34), (26.21, 50, 37), (28.73, 50, 37)]),
    "orca": (10, [(19.32, 48, 20), (19.87, 49, 22), (20.37, 49, 24), (20.87, 49, 33), (21.37, 50, 37), (21.87, 53, 35),
                  (22.37, 50, 35), (23.14, 50, 35), (30.2, 42, 31), (30.75, 47, 43), (33.25, 47, 43), (33.75, 47, 35),
                  (33.89, 47, 35)]),
    "pan": (9, [(27.2, 49, 35), (28.75, 50, 35), (29.25, 62, 50), (29.75, 79, 68), (30.25, 78, 67), (30.75, 78, 59),
                (31.25, 80, 56), (32.75, 77, 55), (33.25, 56, 39), (33.75, 36, 26), (34.01, 36, 26)]),
    "sombrero": (9, [(26.76, 52, 35), (29.81, 53, 37), (30.02, 53, 37)]),
    "yelmo": (24, [(13.0, 53, 39), (14.55, 52, 40), (15.05, 51, 41), (17.33, 51, 41), (25.32, 53, 33), (25.87, 53, 33),
                   (26.37, 52, 39), (26.87, 53, 35), (27.37, 53, 33), (28.09, 54, 33)]),
    "dorthe": (7, [(28.12, 51, 44), (28.67, 51, 44), (29.17, 52, 55), (29.67, 50, 52), (30.17, 52, 43), (30.67, 48, 43),
                   (31.17, 48, 41), (31.67, 48, 41), (32.45, 48, 39)]),
    "dormir": (14, [(20.28, 52, 31), (21.33, 52, 31), (21.83, 54, 44), (22.77, 55, 43), (29.04, 65, 33), (29.59, 65, 33),
                    (30.09, 66, 35), (30.59, 66, 37), (32.26, 66, 37)]),
    "diego": (9, [(33.04, 51, 43), (33.59, 53, 44), (34.09, 48, 35), (34.59, 50, 31), (35.09, 49, 37), (36.46, 49, 37),
                  (43.56, 50, 30), (44.11, 51, 31), (44.61, 50, 31), (45.11, 48, 9), (45.61, 49, 28), (46.11, 53, 28),
                  (46.61, 49, 33), (47.11, 50, 35), (47.34, 50, 35)]),
    "fracaso": (6, [(47.68, 53, 28), (49.23, 52, 28), (51.29, 52, 28)]),
    "autografo": (10, [(37.6, 45, 35), (39.15, 45, 35), (39.65, 44, 30), (40.38, 45, 30)]),
    "tiktok": (11, [(42.44, 52, 35), (43.99, 52, 35), (44.49, 52, 37), (45.99, 52, 37), (46.49, 61, 43), (46.9, 61, 43),
                    (48.12, 48, 28), (48.67, 47, 33), (49.0, 45, 33, 16), (49.30, 45, 33, 20), (49.55, 58, 11, 20), (49.80, 64, 11, 20),
                    (50.05, 54, 28, 22), (50.30, 45, 26, 22), (50.55, 49, 26, 22), (50.80, 55, 37, 20), (51.05, 60, 30, 21),
                    (51.30, 64, 28, 22), (51.55, 67, 26, 22), (51.80, 64, 31, 22), (52.05, 57, 30, 20), (52.22, 57, 30, 20)]),
}
INTRO, OUTRO = 0.0, 3.0
HOOK = ("LE DI IA A LOS NPC", "DE SKYRIM…", "Y ME HUMILLARON")

R = {m["c"]: m for m in json.load(open(os.path.join(AQUI, "momentos.json"), encoding="utf-8"))}
CARAS = json.load(open(os.path.join(AQUI, "caras.json"), encoding="utf-8"))
MOM = [R[c] for c in ORDEN]

# ---------------------------------------------------------------- línea de tiempo
SEGS = []          # (i_mom, i_trozo, a_clip, b_clip, t_out0)
t = INTRO
for i, m in enumerate(MOM):
    m["t0"] = t
    for k, (a, b) in enumerate(m["trozos"]):
        SEGS.append((i, k, a, b, t))
        t += b - a
    m["t1"] = t
FIN_MOM = t
TOTAL = t + OUTRO


def clip_a_out(m, s):
    """Tiempo de clip → tiempo de salida dentro del momento m."""
    acc = m["t0"]
    for a, b in m["trozos"]:
        if a - 0.01 <= s <= b + 0.01:
            return acc + (s - a)
        acc += b - a
    return m["t1"] - 0.5


for m in MOM:
    m["tg"] = clip_a_out(m, m["t_golpe"])
    m["out_bips"] = [clip_a_out(m, s) for s in m["t_bips"]]

# ego acumulado
ego, EGO_T = 100, []
for m in MOM:
    EGO_T.append((m["tg"], ego, max(0, min(100, ego + EGO[m["c"]]))))
    ego = max(0, min(100, ego + EGO[m["c"]]))


def ego_en(t):
    v = 100
    for tg, a, b in EGO_T:
        if t >= tg:
            u = min(1, (t - tg) / 0.45)
            v = a + (b - a) * (1 - (1 - u) ** 3)
    return v


# ---------------------------------------------------------------- seguimiento de cara
def pista(m):
    """Por trozo: (tiempos, x%, y%) suavizados + alto de cara % (mediana)."""
    pts = [p for p in CARAS.get(m["c"], [])]
    if m["c"] in SIN_CARA:
        x, y, h = SIN_CARA[m["c"]]
        return [(np.array([a, b]), np.array([x, x]), np.array([y, y])) for a, b in m["trozos"]], h
    if m["c"] in MANO:
        h, ks = MANO[m["c"]]
        ks = np.array([list(q) + [h] * (4 - len(q)) for q in ks], float)
        out = []
        k = np.exp(-0.5 * (np.arange(-8, 9) * 0.05 / 0.09) ** 2)
        k /= k.sum()
        suave = lambda v: np.convolve(np.pad(v, 8, mode="edge"), k, "valid")
        for a, b in m["trozos"]:
            ts = np.arange(a, b + 0.05, 0.05)
            out.append((ts, suave(np.interp(ts, ks[:, 0], ks[:, 1])), suave(np.interp(ts, ks[:, 0], ks[:, 2])),
                        suave(np.interp(ts, ks[:, 0], ks[:, 3]))))
        return out, float(h)
    hs = []
    out = []
    for a, b in m["trozos"]:
        q = np.array([p for p in pts if a - 0.05 <= p[0] <= b + 0.05]) if pts else np.zeros((0, 4))
        if len(q):
            mx, my = np.median(q[:, 1]), np.median(q[:, 2])
            ok = np.hypot(q[:, 1] - mx, q[:, 2] - my) < 9
            q = q[ok] if ok.sum() else q
        if not len(q):
            gx, gy = (np.median(np.array(pts)[:, 1]), np.median(np.array(pts)[:, 2])) if pts else (50, 40)
            q = np.array([[a, gx, gy, 14]])
        hs += list(q[:, 3])
        ts = np.arange(a, b + 0.05, 0.05)
        x = np.interp(ts, q[:, 0], q[:, 1])
        y = np.interp(ts, q[:, 0], q[:, 2])
        k = np.exp(-0.5 * (np.arange(-12, 13) * 0.05 / 0.30) ** 2)
        k /= k.sum()
        xp, yp = np.pad(x, 12, mode="edge"), np.pad(y, 12, mode="edge")
        out.append((ts, np.convolve(xp, k, "valid"), np.convolve(yp, k, "valid")))
    return out, float(np.clip(np.median(hs), 6, 24))


for m in MOM:
    m["pista"], m["cara_h"] = pista(m)


def cara(m, k, s):
    ts, xs, ys = m["pista"][k][:3]
    return float(np.interp(s, ts, xs)) * 19.2, float(np.interp(s, ts, ys)) * 10.8


def alto_cara(m, k, s):
    p = m["pista"][k]
    return float(np.interp(s, p[0], p[3])) if len(p) > 3 else m["cara_h"]


def ease_back(u):
    u = min(1, max(0, u))
    c = 1.9
    return 1 + (c + 1) * (u - 1) ** 3 + c * (u - 1) ** 2


def camara(m, k, s, t):
    """Ventana de recorte (x0, y0, wc, hc) en el cuadro 1920x1080 del clip."""
    fx, fy = cara(m, k, s)
    z_pre = 1.0 + 0.14 * min(1, max(0, (t - m["t0"]) / max(0.5, m["tg"] - m["t0"]))) + (0.07 if k > 0 else 0)
    hc_g = float(np.clip(alto_cara(m, k, s) * 10.8 * 3.6, 330, 640))
    z_g = 1080 / hc_g
    if t < m["tg"]:
        z = z_pre
    else:
        u = (t - m["tg"]) / 0.13
        z_pre_g = 1.0 + 0.14 + (0.07 if len(m["trozos"]) > 1 else 0)
        z = z_pre_g + (z_g - z_pre_g) * ease_back(u) + 0.04 * max(0, t - m["tg"] - 0.13)
    hc = 1080 / z
    wc = hc * 0.8
    cx, cy = fx, fy + 0.12 * hc
    if t >= m["tg"] and m["meme"] in ("skull", "boom", "scratch"):
        u = (t - m["tg"]) / 0.35
        if u < 1:
            amp = 10 / z * (1 - u)
            cx += amp * math.sin(2 * math.pi * 21 * t)
            cy += amp * math.cos(2 * math.pi * 17 * t)
    x0 = float(np.clip(cx - wc / 2, 0, 1920 - wc))
    y0 = float(np.clip(cy - hc / 2, 0, 1080 - hc))
    return x0, y0, wc, hc


# ---------------------------------------------------------------- lectura de cuadros
class Lector:
    def __init__(self):
        self.cap, self.clave, self.ult = None, None, None

    def leer(self, clave, s):
        if clave != self.clave or self.ult is None or s < self.ult[0] - 1e-3 or s > self.ult[0] + 1.0:
            if self.cap:
                self.cap.release()
            self.cap = cv2.VideoCapture(os.path.join(CLIPS, clave + ".mp4"))
            self.cap.set(cv2.CAP_PROP_POS_MSEC, max(0, s - 0.05) * 1000)
            self.clave, self.ult = clave, None
            ok, f = self.cap.read()
            self.ult = (self.cap.get(cv2.CAP_PROP_POS_MSEC) / 1000, f)
        while self.ult[0] + 1 / 120 < s:
            ok, f = self.cap.read()
            if not ok:
                break
            self.ult = (self.cap.get(cv2.CAP_PROP_POS_MSEC) / 1000, f)
        return self.ult[1]


# ---------------------------------------------------------------- capas de texto
EMOJI_F = {}


def emoji(ch, tam):
    k = (ch, tam)
    if k not in EMOJI_F:
        from PIL import ImageFont
        f = ImageFont.truetype("C:/Windows/Fonts/seguiemj.ttf", 109)
        im = Image.new("RGBA", (220, 220), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((110, 110), ch, font=f, embedded_color=True, anchor="mm")
        bb = im.getbbox()
        im = im.crop(bb) if bb else im
        s = tam / max(im.size)
        EMOJI_F[k] = im.resize((max(1, int(im.size[0] * s)), max(1, int(im.size[1] * s))), Image.LANCZOS)
    return EMOJI_F[k]


def texto_grande(s, ancho_max=960, tam=118, color=(255, 255, 255), stroke=10, giro=-2.5):
    f = T.fuente("Bold Condensed", tam)
    d0 = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    while d0.textlength(s, font=f) > ancho_max and tam > 56:
        tam -= 4
        f = T.fuente("Bold Condensed", tam)
    w = int(d0.textlength(s, font=f)) + 2 * stroke + 20
    im = Image.new("RGBA", (w, tam + 2 * stroke + 30), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text((w / 2 + 5, im.size[1] / 2 + 7), s, font=f, fill=(0, 0, 0, 170), anchor="mm", stroke_width=stroke,
           stroke_fill=(0, 0, 0, 170))
    d.text((w / 2, im.size[1] / 2), s, font=f, fill=color + (255,), anchor="mm", stroke_width=stroke,
           stroke_fill=(0, 0, 0, 255))
    return im.rotate(giro, resample=Image.BICUBIC, expand=True)


CACHE = {}


def capa_cache(k, fn):
    if k not in CACHE:
        CACHE[k] = fn()
    return CACHE[k]


def pegar(base, im, cx, cy, escala=1.0, alfa=1.0):
    if escala <= 0.02 or alfa <= 0.01:
        return
    if abs(escala - 1) > 1e-3:
        im = im.resize((max(1, int(im.size[0] * escala)), max(1, int(im.size[1] * escala))), Image.BICUBIC)
    if alfa < 0.999:
        a = im.getchannel("A").point(lambda v: int(v * alfa))
        im = im.copy()
        im.putalpha(a)
    base.alpha_composite(im, (int(cx - im.size[0] / 2), int(cy - im.size[1] / 2)))


def pop(dt, dur=0.28):
    if dt <= 0:
        return 0.0
    u = dt / dur
    return 1.0 if u >= 1.8 else 1 - math.exp(-5 * u) * math.cos(8 * u)


def encabezado():
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    T._texto(d, (W / 2, 128), "SKYRIM CON IA", T.fuente("Bold Condensed", 84), HUESO, ancla="mm", track=8)
    T.separador(d, W / 2, 176, 300)
    T._texto(d, (W / 2, 210), "EGO DE EDSON", T.fuente("SemiBold Condensed", 30), (200, 196, 186), ancla="mm", track=6)
    # marco de la ventana del juego
    d.rectangle([0, WIN_Y0 - 3, W, WIN_Y0 - 1], fill=HUESO + (200,))
    d.rectangle([0, WIN_Y0 + WIN_H + 1, W, WIN_Y0 + WIN_H + 3], fill=HUESO + (200,))
    return im


def barra_ego(d, v, t, delta=None, t_delta=None):
    """Barra de vida de Skyrim: marco con puntas, relleno rojo que se encoge hacia el centro."""
    cx, cy, mw, hh = W / 2, 252, 300, 9
    d.polygon([(cx - mw - 26, cy), (cx - mw - 6, cy - hh - 6), (cx + mw + 6, cy - hh - 6), (cx + mw + 26, cy),
               (cx + mw + 6, cy + hh + 6), (cx - mw - 6, cy + hh + 6)], fill=(10, 10, 10, 200), outline=HUESO + (220,))
    fw = mw * v / 100
    rojo = (205, 40, 32) if v > 25 or int(t * 6) % 2 == 0 else (255, 90, 70)
    if fw > 1:
        d.rectangle([cx - fw, cy - hh, cx + fw, cy + hh], fill=rojo + (255,))
        d.rectangle([cx - fw, cy - hh, cx + fw, cy - hh + 4], fill=(255, 140, 120, 160))
    if delta is not None and t_delta is not None and 0 <= t - t_delta < 1.3:
        u = (t - t_delta) / 1.3
        s = ("+%d" % delta) if delta > 0 else ("%d" % delta)
        col = (120, 230, 120) if delta > 0 else (255, 70, 60)
        f = T.fuente("Bold Condensed", 54)
        a = int(255 * (1 - u ** 3))
        y = cy - 10 - 40 * u
        d.text((cx + mw + 70, y), s, font=f, fill=col + (a,), anchor="lm", stroke_width=4, stroke_fill=(0, 0, 0, a))


def placa_nombre(nombre):
    def f():
        im = Image.new("RGBA", (W, 120), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        T._texto(d, (W / 2, 40), nombre, T.fuente("Bold Condensed", 58), HUESO, ancla="mm", track=5)
        T.separador(d, W / 2, 86, 220)
        return im
    return capa_cache(("placa", nombre), f)


def burbuja(yo):
    def f():
        ctx = yo.startswith("(")
        s = yo.strip("()") if ctx else "YO: " + yo
        fnt = T.fuente("SemiBold Condensed" if ctx else "Bold Condensed", 44)
        d0 = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
        tw = int(d0.textlength(s, font=fnt))
        w, h = min(tw + 64, 1000), 82
        im = Image.new("RGBA", (w + 20, h + 30), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        if ctx:
            d.rounded_rectangle([10, 10, w + 10, h + 10], 20, fill=(12, 12, 12, 205), outline=HUESO + (160,), width=2)
            d.text((w / 2 + 10, h / 2 + 10), s, font=fnt, fill=HUESO + (255,), anchor="mm")
        else:
            d.rounded_rectangle([10, 10, w + 10, h + 10], 30, fill=(255, 255, 255, 240))
            d.polygon([(60, h + 8), (100, h + 8), (52, h + 28)], fill=(255, 255, 255, 240))
            d.text((w / 2 + 10, h / 2 + 10), s, font=fnt, fill=(20, 20, 20, 255), anchor="mm")
        return im
    return capa_cache(("burb", yo), f)


def chip(n, tot):
    def f():
        im = Image.new("RGBA", (190, 80), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([4, 4, 186, 76], 16, fill=(10, 10, 10, 190), outline=ORO + (230,), width=3)
        d.text((95, 40), "#%d/%d" % (n, tot), font=T.fuente("Bold Condensed", 46), fill=ORO + (255,), anchor="mm")
        return im
    return capa_cache(("chip", n), f)


ENC = encabezado()


# ---------------------------------------------------------------- cuadro
def fondo_y_ventana(fr, x0, y0, wc, hc):
    small = cv2.resize(fr, (192, 108), interpolation=cv2.INTER_AREA)
    bg = cv2.GaussianBlur(small, (0, 0), 6)
    bg = cv2.resize(bg[:, 48:144], (W, H), interpolation=cv2.INTER_LINEAR)
    bg = (bg.astype(np.float32) * 0.42).astype(np.uint8)
    xi, yi = int(x0), int(y0)
    wi, hi = int(round(wc)), int(round(hc))
    crop = fr[yi:yi + hi, xi:xi + wi]
    win = cv2.resize(crop, (W, WIN_H), interpolation=cv2.INTER_CUBIC if wi < W else cv2.INTER_AREA)
    if wi < 800:   # un poco de nitidez al acercar
        bl = cv2.GaussianBlur(win, (0, 0), 1.6)
        win = cv2.addWeighted(win, 1.45, bl, -0.45, 0)
    bg[WIN_Y0:WIN_Y0 + WIN_H] = win
    return bg


BANDA = (1100, WIN_Y0 + WIN_H, 50)   # franja esmerilada detrás de nombre y remate: tapa el «E Hablar <NPC>» del juego


def _rampa():
    y0, y1, f = BANDA
    n = y1 - y0
    a = np.ones(n, np.float32)
    a[:f] = np.linspace(0, 1, f)
    return a[:, None, None]


RAMPA = _rampa()


def franja(img):
    y0, y1, _ = BANDA
    reg = img[y0:y1].astype(np.float32)
    bl = cv2.GaussianBlur(img[y0:y1], (0, 0), 11).astype(np.float32) * 0.42
    img[y0:y1] = (reg * (1 - RAMPA) + bl * RAMPA).astype(np.uint8)
    return img


def cuadro(t, lector):
    # momento y trozo
    if t >= FIN_MOM:
        m = MOM[-1]
        i, k = len(MOM) - 1, len(m["trozos"]) - 1
        s = m["trozos"][-1][1] - 0.04
        t_cam = FIN_MOM - 1e-3
    else:
        i, k, a, b, t0 = [sg for sg in SEGS if sg[4] <= t + 1e-6][-1]
        m = MOM[i]
        s = a + (t - t0)
        t_cam = t
    fr = lector.leer(m["c"], s)
    x0, y0, wc, hc = camara(m, k, s, t_cam)
    if t >= FIN_MOM:   # cierre: congelado que se acerca un poco, desaturado
        u = min(1, (t - FIN_MOM) / OUTRO)
        z = 1 + 0.1 * u
        cx, cy = x0 + wc / 2, y0 + hc / 2
        wc, hc = wc / z, hc / z
        x0, y0 = cx - wc / 2, cy - hc / 2
    img = fondo_y_ventana(fr, x0, y0, wc, hc)
    if t >= FIN_MOM:
        g = cv2.cvtColor(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
        u = min(1, (t - FIN_MOM) / 0.4)
        img = cv2.addWeighted(img, 1 - 0.8 * u, g, 0.8 * u, 0)
        img = (img.astype(np.float32) * (1 - 0.45 * u)).astype(np.uint8)
    else:
        img = franja(img)

    base = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)).convert("RGBA")
    base.alpha_composite(ENC)
    d = ImageDraw.Draw(base)
    j_ego = max([n for n, (tg, _, _) in enumerate(EGO_T) if tg <= t] or [None]) if any(tg <= t for tg, _, _ in EGO_T) else None
    delta = EGO[MOM[j_ego]["c"]] if j_ego is not None else None
    barra_ego(d, ego_en(t), t, delta, EGO_T[j_ego][0] if j_ego is not None else None)

    if t < FIN_MOM:
        dt0, dtg = t - m["t0"], t - m["tg"]
        # número del momento
        pegar(base, chip(i + 1, len(MOM)), 120, WIN_Y0 + 60, escala=pop(dt0 - 0.05, 0.22) if dt0 < 0.6 else 1)
        # burbuja YO / contexto
        if m["yo"] and dtg < -0.15:
            fade = min(1, (m["tg"] - 0.15 - t) / 0.15)
            pegar(base, burbuja(m["yo"]), W / 2, WIN_Y0 + 165, escala=pop(dt0 - 0.08, 0.25), alfa=fade)
        # nombre de quien habla
        if i == 0 and t < 2.6:
            pass
        else:
            a_n = min(1, max(0, (dt0 - 0.1) / 0.2))
            pegar(base, placa_nombre(m["quien"]), W / 2, 1150 + 20 * (1 - a_n), alfa=a_n)
        # remate
        if dtg >= -0.05:
            im = capa_cache(("rem", m["c"]), lambda: texto_grande(m["remate"], color=(255, 230, 90) if m["c"] in ("tiktok", "autografo", "sombrero") else (255, 255, 255)))
            pegar(base, im, W / 2, 1290, escala=pop(dtg + 0.05, 0.3))
            # emoji cerca de la cara
            fx, fy = cara(m, k, s)
            ex = (fx - x0) * (W / wc)
            semi = 0.5 * 0.8 * alto_cara(m, k, s) * 10.8 * (W / wc)     # medio ancho de la cara en la ventana
            lado = -1 if ex > W / 2 + 60 else 1
            ex += lado * (semi + 165)
            ey = WIN_Y0 + (fy - y0) * (WIN_H / hc) - 0.9 * semi - 30
            ex, ey = float(np.clip(ex, 130, W - 130)), float(np.clip(ey, WIN_Y0 + 200, 1000))
            esc = pop(dtg - 0.12, 0.3)
            if esc > 0:
                em = emoji(EMO[m["c"]], 210).rotate(12 * math.sin(t * 7), resample=Image.BICUBIC, expand=True)
                pegar(base, em, ex, ey, escala=esc)
        # bips
        for tb in m["out_bips"]:
            if 0 <= t - tb < 0.55:
                pegar(base, emoji("🤬", 130), 150, 1000, escala=pop(t - tb, 0.15))
        # gancho de entrada
        if i == 0 and t < 2.6:
            a1 = min(1, t / 0.12) * (1 if t < 2.3 else max(0, (2.6 - t) / 0.3))
            l1 = capa_cache("h1", lambda: texto_grande(HOOK[0], tam=110, giro=0))
            l2 = capa_cache("h2", lambda: texto_grande(HOOK[1], tam=110, giro=0))
            l3 = capa_cache("h3", lambda: texto_grande(HOOK[2] + "", tam=124, color=(255, 230, 90), giro=-3))
            pegar(base, l1, W / 2, 1080, escala=pop(t, 0.25), alfa=a1)
            pegar(base, l2, W / 2, 1190, escala=pop(t - 0.15, 0.25), alfa=a1)
            if t > 1.0:
                pegar(base, l3, W / 2 - 40, 1320, escala=pop(t - 1.0, 0.28), alfa=a1)
                pegar(base, emoji("💀", 150), W / 2 + 380, 1320, escala=pop(t - 1.15, 0.28), alfa=a1)
    else:
        u = t - FIN_MOM
        im1 = capa_cache("o1", lambda: texto_grande("EGO DE EDSON: 0", tam=120, color=(255, 80, 64), giro=-2))
        im2 = capa_cache("o2", lambda: texto_grande("¿PARTE 2?", tam=150, color=(255, 230, 90), giro=2))
        im3 = capa_cache("o3", lambda: texto_grande("COMENTA TU NPC FAVORITO", tam=70, giro=0, stroke=7))
        pegar(base, im1, W / 2, 760, escala=pop(u - 0.1, 0.3))
        pegar(base, emoji("💀", 240), W / 2, 980, escala=pop(u - 0.35, 0.3))
        pegar(base, im2, W / 2, 1200, escala=pop(u - 0.8, 0.3))
        pegar(base, im3, W / 2, 1330, escala=pop(u - 1.1, 0.3))
        pegar(base, emoji("👇", 110), W / 2, 1450, escala=pop(u - 1.3, 0.3))

    out = cv2.cvtColor(np.asarray(base.convert("RGB")), cv2.COLOR_RGB2BGR)
    # destellos: corte entre momentos y golpes fuertes
    fl = 0.0
    for n, mm in enumerate(MOM):
        if n and 0 <= t - mm["t0"] < 0.1:
            fl = max(fl, 0.65 * (1 - (t - mm["t0"]) / 0.1))
        if mm["meme"] in ("skull", "boom") and 0 <= t - mm["tg"] < 0.08:
            fl = max(fl, 0.35 * (1 - (t - mm["tg"]) / 0.08))
    if 0 <= t - FIN_MOM < 0.12:
        fl = max(fl, 0.6 * (1 - (t - FIN_MOM) / 0.12))
    if fl > 0:
        out = cv2.addWeighted(out, 1 - fl, np.full_like(out, 255), fl, 0)
    return out


# ---------------------------------------------------------------- audio
def decodificar(ruta):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", ruta, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.float32).reshape(-1, 2).copy()


def poner(buf, x, t, g=1.0):
    i = int(t * SR)
    if i >= len(buf):
        return
    n = min(len(x), len(buf) - i)
    buf[i:i + n] += x[:n] * g


def audio():
    n = int(TOTAL * SR) + SR
    voz = np.zeros((n, 2), np.float32)
    cache = {}
    for m in MOM:
        if m["c"] not in cache:
            cache[m["c"]] = decodificar(os.path.join(CLIPS, m["c"] + ".mp4"))
        x = cache[m["c"]]
        trozo_mom = []
        for a, b in m["trozos"]:
            y = x[int(a * SR):int(b * SR)].copy()
            f = int(0.012 * SR)
            y[:f] *= np.linspace(0, 1, f)[:, None]
            y[-f:] *= np.linspace(1, 0, f)[:, None]
            trozo_mom.append(y)
        y = np.concatenate(trozo_mom)
        # bips: de la palabra marcada hasta la siguiente
        todas = [p[0] for p in m["palabras"]]
        for tb in m["t_bips"]:
            sig = [w for w in todas if w > tb + 0.05]
            te = min(sig[0] - 0.02 if sig else tb + 0.5, tb + 0.7)
            o0, o1 = clip_a_out(m, tb - 0.03) - m["t0"], clip_a_out(m, te) - m["t0"]
            i0, i1 = int(o0 * SR), int(o1 * SR)
            if i1 > i0:
                tt = np.arange(i1 - i0) / SR
                bip = 0.22 * np.sin(2 * np.pi * 1000 * tt)
                f = min(int(0.005 * SR), (i1 - i0) // 2)
                env = np.ones(i1 - i0)
                env[:f] = np.linspace(0, 1, f)
                env[-f:] = np.linspace(1, 0, f)
                y[i0:i1] = (bip * env)[:, None]
        rms = np.sqrt(np.mean(y ** 2)) + 1e-6
        g = float(np.clip(10 ** (-19 / 20) / rms, 0.3, 4.0))
        poner(voz, y, m["t0"], g)
    voz = np.clip(voz, -0.98, 0.98)

    fx = np.zeros_like(voz)
    sfx = lambda nom: decodificar(os.path.join(AQUI, "sfx", nom + ".mp3"))
    sx = {k: sfx(k) for k in ["boom_1", "boom_2", "ding", "bruh", "risas", "scratch", "whoosh_1", "whoosh_2", "whoosh_3"]}
    for k, s in sx.items():
        sx[k] = s / (np.abs(s).max() + 1e-6)
    for j, m in enumerate(MOM):
        if j:
            poner(fx, sx["whoosh_%d" % (j % 3 + 1)], m["t0"] - 0.12, 0.30)
        nom = SFX_MEME.get(m["meme"])
        if nom:
            g = {"boom_1": 0.55, "boom_2": 0.55, "ding": 0.35, "bruh": 0.32, "risas": 0.30, "scratch": 0.45}[nom]
            poner(fx, sx[nom], m["tg"] + (0.0 if nom in ("boom_1", "boom_2", "scratch") else 0.15), g)
    poner(fx, sx["boom_2"], FIN_MOM, 0.5)
    poner(fx, sx["risas"], FIN_MOM + 0.5, 0.35)

    mus = decodificar(next(os.path.join(AQUI, "audio", "ost", f) for f in os.listdir(os.path.join(AQUI, "audio", "ost"))
                           if "Bannered" in f))
    mus = mus / (np.sqrt(np.mean(mus ** 2)) + 1e-6) * 10 ** (-19 / 20)
    mus = np.tile(mus, (int(np.ceil(n / len(mus))), 1))[:n]
    env = np.full(n, 0.16, np.float32)
    i_fin = int(FIN_MOM * SR)
    env[i_fin:] = np.linspace(0.16, 0.55, n - i_fin)
    env[-int(0.6 * SR):] *= np.linspace(1, 0, int(0.6 * SR))
    env[:int(0.3 * SR)] *= np.linspace(0, 1, int(0.3 * SR))
    mezcla = voz + fx + mus * env[:, None]
    mezcla = mezcla[:int(TOTAL * SR)]
    ruta = os.path.join(AQUI, "audio", "mezcla_short.wav")
    import soundfile as sf
    sf.write(ruta, mezcla, SR, subtype="FLOAT")
    return ruta


def srt():
    def ts(x):
        h, r = divmod(x, 3600)
        mi, se = divmod(r, 60)
        return "%02d:%02d:%06.3f" % (h, mi, se)
    lin, n = [], 1
    for m in MOM:
        for a, b in m["trozos"]:
            ws = [p for t, p in m["palabras"] if a - 0.01 <= t <= b + 0.01]
            s = " ".join("[…]" if p == "[bip]" else p for p in ws)
            t0, t1 = clip_a_out(m, a), clip_a_out(m, b)
            lin.append("%d\n%s --> %s\n%s\n" % (n, ts(t0).replace(".", ","), ts(t1).replace(".", ","), s))
            n += 1
    return "\n".join(lin)


# ---------------------------------------------------------------- principal
def hoja(tiempos):
    lec = Lector()
    for n, t in enumerate(tiempos):
        img = cuadro(t, lec)
        ruta = os.path.join(AQUI, "previews", "fx_%02d.jpg" % n)
        cv2.imwrite(ruta, cv2.resize(img, (540, 960), interpolation=cv2.INTER_AREA), [cv2.IMWRITE_JPEG_QUALITY, 85])
    print("hoja: %d cuadros, total %.1f s" % (len(tiempos), TOTAL))


def render():
    a = audio()
    os.makedirs(os.path.join(AQUI, "salida"), exist_ok=True)
    tmp = os.path.join(AQUI, "segmentos", "video_short.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "%dx%d" % (W, H),
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                          "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    lec = Lector()
    nf = int(TOTAL * FPS)
    for f in range(nf):
        p.stdin.write(cuadro(f / FPS, lec).tobytes())
        if f % 300 == 0:
            print("cuadro %d/%d" % (f, nf), flush=True)
    p.stdin.close()
    p.wait()
    master = os.path.join(AQUI, "salida", "tes_embry_short_MASTER.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", tmp, "-i", a, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest",
                    "-movflags", "+faststart", master], check=True)
    open(master.replace(".mp4", ".srt"), "w", encoding="utf-8").write(srt())
    print("MASTER:", master, "%.1f s" % TOTAL)


if __name__ == "__main__":
    if "--hoja" in sys.argv:
        hoja([float(x) for x in sys.argv[sys.argv.index("--hoja") + 1:]])
    elif "--hoja-golpes" in sys.argv:
        ts = []
        for m in MOM:
            ts += [m["t0"] + 0.4, m["tg"] + 0.45]
        ts += [FIN_MOM + 2.5]
        hoja(ts)
        print(" ".join("%s:%.1f/%.1f" % (m["c"], m["t0"], m["tg"]) for m in MOM))
    else:
        render()
