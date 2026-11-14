# -*- coding: utf-8 -*-
"""Kit gráfico propio del reel jch_carrera_moyahua (vertical 1080x1920). Cada función devuelve fn(dt, dur, marcas) -> BGRA
para los FX `mg`/`pantalla` de nucleo/secuencia_fx.py.
  mapa_ruta()            mapa REAL (OpenTopoMap, © OpenStreetMap) con la carretera 23 (trazo OSRM) que se dibuja de Jesús María
                          (km 78) a Moyahua (km 105) + contador de curvas; Juchipila y Apozol de referencia.
  postura(lado)          cintillo «POSTURA · EN CONTRA» (rojo) / «POSTURA · A FAVOR» (verde) arriba, con la barra que late.
  ficha(titulo, items)   tarjeta de datos (items con ✓/✗ que aparecen con las marcas de la voz).
  cifra(num, texto)      número gigante que cuenta hasta su valor + leyenda.
  balanza()              balanza que oscila sin decidirse (el narrador NO toma postura): RIESGO | DERRAMA.
  credito(texto)         etiqueta chica «Video: canal» abajo a la izquierda.
"""
import json, math, os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

AQ = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1920
F = "C:/Windows/Fonts/"
ROJO, VERDE, AMAR, BLANCO, NEGRO = (232, 52, 46), (40, 190, 110), (255, 204, 0), (250, 248, 240), (12, 12, 14)
_fc = {}


def fuente(tam, nombre="bahnschrift.ttf", var="Bold Condensed"):
    k = (tam, nombre, var)
    if k not in _fc:
        f = ImageFont.truetype(F + nombre, tam)
        if var:
            try:
                f.set_variation_by_name(var)
            except Exception:
                pass
        _fc[k] = f
    return _fc[k]


def ease(x):
    x = min(1.0, max(0.0, x))
    return 1 - (1 - x) ** 3


def pop(x, d=.35):
    x = min(1.0, max(0.0, x / d))
    return 1 + 0.18 * math.sin(x * math.pi) * (1 - x) if x < 1 else 1.0


def a_bgra(im):
    a = np.array(im.convert("RGBA"))
    return np.ascontiguousarray(a[:, :, [2, 1, 0, 3]])


def texto_img(txt, tam, color=BLANCO, borde=NEGRO, b=6, nombre="bahnschrift.ttf", var="Bold Condensed"):
    f = fuente(tam, nombre, var)
    x0, y0, x1, y1 = f.getbbox(txt)
    im = Image.new("RGBA", (x1 - x0 + 2 * b + 8, y1 - y0 + 2 * b + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text((b + 4 - x0, b + 4 - y0), txt, font=f, fill=color + (255,), stroke_width=b, stroke_fill=borde + (255,))
    return im


# ------------------------------------------------------------------ mapa
def _merc(lat, lon, z, tx0, ty0):
    n = 2 ** z
    x = (lon + 180) / 360 * n
    y = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
    return (x - tx0) * 256, (y - ty0) * 256


PUEBLOS = {"Juchipila": (21.4088, -103.1163), "Apozol": (21.4699, -103.0899), "Moyahua": (21.2656, -103.1657),
           "Jesús María": (21.0972, -103.1565)}


def mapa_ruta():
    cache = {}

    def prep():
        meta = json.load(open(os.path.join(AQ, "mapas", "canon_meta.json")))
        base = cv2.imread(os.path.join(AQ, "mapas", "canon_base.png"))
        # un poco más oscuro y frío para que el trazo rojo mande
        base = cv2.addWeighted(base, .78, np.full_like(base, (40, 30, 20)), .22, 0)
        r = json.load(open(os.path.join(AQ, "_ruta.json")))["routes"][0]
        co = r["geometry"]["coordinates"]
        pts = np.array([_merc(la, lo, meta["z"], meta["tx0"], meta["ty0"]) for lo, la in co])
        jm, my = np.array(_merc(*PUEBLOS["Jesús María"], meta["z"], meta["tx0"], meta["ty0"])), \
            np.array(_merc(*PUEBLOS["Moyahua"], meta["z"], meta["tx0"], meta["ty0"]))
        k = int(np.argmin(((pts - my) ** 2).sum(1)))          # fin del tramo de carrera
        carrera, resto = pts[:k + 1], pts[k:]
        seg = np.r_[0, np.cumsum(np.hypot(*np.diff(carrera, axis=0).T))]
        cache.update(base=base, meta=meta, carrera=carrera, resto=resto, acum=seg / seg[-1],
                     pueblos={n: np.array(_merc(la, lo, meta["z"], meta["tx0"], meta["ty0"])) for n, (la, lo) in PUEBLOS.items()},
                     etiquetas={n: texto_img(n.upper(), 46) for n in PUEBLOS},
                     km78=texto_img("KM 78", 40, AMAR), km105=texto_img("KM 105", 40, AMAR),
                     tit=texto_img("CARRETERA FEDERAL 23", 64), sub=texto_img("27.5 KM DE CARRERA", 50, AMAR),
                     cred=texto_img("Mapa: © OpenStreetMap · OpenTopoMap (CC-BY-SA) · ruta OSRM", 24, b=3,
                                    nombre="segoeui.ttf", var=None))

    def fn(dt, dur, marcas):
        if not cache:
            prep()
        c = cache
        bw, bh = c["base"].shape[1], c["base"].shape[0]
        # cámara: de la región entera a encuadrar el tramo de carrera
        x0, y0 = c["carrera"].min(0) - (260, 330)
        x1, y1 = c["carrera"].max(0) + (260, 260)
        s_lejos = max(W / bw, H / bh) * 1.02
        s_cerca = min(W / (x1 - x0), H / (y1 - y0))
        cx_l, cy_l = bw / 2, bh / 2
        cx_c, cy_c = (x0 + x1) / 2, (y0 + y1) / 2
        e = ease(dt / max(1.0, dur * .32))
        s = s_lejos + (s_cerca - s_lejos) * e
        s *= 1 + 0.025 * dt / max(dur, 1)
        cx, cy = cx_l + (cx_c - cx_l) * e, cy_l + (cy_c - cy_l) * e
        M = np.float32([[s, 0, W / 2 - s * cx], [0, s, H / 2 - s * cy]])
        f = cv2.warpAffine(c["base"], M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        tp = lambda p: (p * s + (W / 2 - s * cx, H / 2 - s * cy))
        # Moyahua -> Juchipila (contexto, blanco a rayas)
        r = tp(c["resto"]).astype(np.int32)
        for i in range(0, len(r) - 1, 2):
            cv2.line(f, tuple(r[i]), tuple(r[i + 1]), (235, 235, 235), 4, cv2.LINE_AA)
        # tramo de carrera que se dibuja
        t0 = (marcas[0] if marcas else dur * .25)
        t1 = (marcas[1] if len(marcas) > 1 else dur * .8)
        prog = ease((dt - t0) / max(.5, t1 - t0))
        n = int(np.searchsorted(c["acum"], prog))
        if n > 1:
            p = tp(c["carrera"][:n]).astype(np.int32)
            glow = np.zeros_like(f)
            cv2.polylines(glow, [p], False, (40, 40, 255), 30, cv2.LINE_AA)
            glow = cv2.GaussianBlur(glow, (0, 0), 9)
            f = cv2.add(f, glow)
            cv2.polylines(f, [p], False, (20, 20, 20), 15, cv2.LINE_AA)
            cv2.polylines(f, [p], False, (46, 52, 232), 9, cv2.LINE_AA)
            hx, hy = p[-1]
            rr = int(12 + 5 * math.sin(dt * 9))
            cv2.circle(f, (int(hx), int(hy)), rr + 6, (255, 255, 255), -1, cv2.LINE_AA)
            cv2.circle(f, (int(hx), int(hy)), rr, (46, 52, 232), -1, cv2.LINE_AA)
        im = Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)).convert("RGBA")
        # pueblos
        for nmb, p in c["pueblos"].items():
            q = tp(p)
            vis = 1.0 if nmb in ("Juchipila", "Apozol") else (prog > 0.001 if nmb == "Jesús María" else prog > .97)
            if not vis or not (-50 < q[0] < W + 50 and -50 < q[1] < H + 50):
                continue
            d = ImageDraw.Draw(im)
            d.ellipse([q[0] - 13, q[1] - 13, q[0] + 13, q[1] + 13], fill=BLANCO + (255,), outline=NEGRO + (255,), width=5)
            et = c["etiquetas"][nmb]
            lx = q[0] + 26 if q[0] < W * .62 else q[0] - 26 - et.width
            im.alpha_composite(et, (int(lx), int(q[1] - et.height / 2)))
            if nmb == "Jesús María":
                im.alpha_composite(c["km78"], (int(lx), int(q[1] + et.height / 2 - 4)))
            if nmb == "Moyahua":
                im.alpha_composite(c["km105"], (int(lx), int(q[1] + et.height / 2 - 4)))
        # título y contador
        a = ease(dt / .5)
        banda = Image.new("RGBA", (W, 300), (0, 0, 0, 0))
        bd = ImageDraw.Draw(banda)
        for i in range(300):
            bd.line([(0, i), (W, i)], fill=(8, 8, 12, int(210 * (1 - i / 300) * a)))
        im.alpha_composite(banda, (0, 0))
        im.alpha_composite(c["tit"], ((W - c["tit"].width) // 2, 120))
        im.alpha_composite(c["sub"], ((W - c["sub"].width) // 2, 205))
        curvas = int(round(97 * prog))
        if dt > t0 - .2:
            num = texto_img(f"{curvas}", 150, AMAR if curvas < 97 else BLANCO, b=8)
            lab = texto_img("CURVAS", 60, b=6)
            sc = pop(dt - t1, .4) if dt > t1 else 1.0
            if sc != 1.0:
                num = num.resize((int(num.width * sc), int(num.height * sc)), Image.LANCZOS)
            im.alpha_composite(num, (W - num.width - 50, H - 720))
            im.alpha_composite(lab, (W - lab.width - 56, H - 720 + num.height - 10))
        im.alpha_composite(c["cred"], (24, H - c["cred"].height - 16))
        return a_bgra(im)
    return fn


# ------------------------------------------------------------------ postura
def postura(lado):
    rojo = lado == "contra"
    col = ROJO if rojo else VERDE
    t1 = texto_img("POSTURA", 56, BLANCO, b=0)
    t2 = texto_img("EN CONTRA" if rojo else "A FAVOR", 130, BLANCO, b=0)
    nota = texto_img("voz que representa a quienes piensan así", 34, (235, 235, 235), b=0, nombre="segoeui.ttf", var=None)

    def fn(dt, dur, marcas):
        ww = max(t2.width, t1.width, nota.width) + 90
        hh = t1.height + t2.height + nota.height + 70
        im = Image.new("RGBA", (ww + 30, hh + 30), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        e = ease(dt / .35) * (1 - ease((dt - dur + .3) / .3))
        d.rounded_rectangle([10, 14, ww + 10, hh + 14], 26, fill=(0, 0, 0, 120))
        d.rounded_rectangle([4, 4, ww, hh], 26, fill=col + (235,))
        lat = int(10 + 4 * math.sin(dt * 6))
        d.rounded_rectangle([4, 4, 4 + lat, hh], 6, fill=(255, 255, 255, 230))
        im.alpha_composite(t1, (44, 22))
        im.alpha_composite(t2, (40, 22 + t1.height))
        im.alpha_composite(nota, (44, 30 + t1.height + t2.height))
        dx = int((1 - e) * -(ww + 60))
        out = Image.new("RGBA", (im.width + abs(dx) + 4, im.height), (0, 0, 0, 0))
        out.alpha_composite(im, (max(0, dx + abs(dx)), 0))
        a = np.array(out)
        a[:, :, 3] = (a[:, :, 3] * min(1, e * 1.5)).astype(np.uint8)
        return a_bgra(Image.fromarray(a))
    return fn


# ------------------------------------------------------------------ ficha de datos
def ficha(titulo, items, color=AMAR, ancho=940):
    """items = [(texto, "x"|"v"|"·")], aparecen con las marcas (o repartidas)."""
    tt = texto_img(titulo, 70, NEGRO, b=0)
    filas = [(texto_img(tx, 54, BLANCO, b=0), m) for tx, m in items]

    def fn(dt, dur, marcas):
        hh = 60 + tt.height + 30 + sum(f.height + 26 for f, _ in filas) + 30
        im = Image.new("RGBA", (ancho + 20, hh + 20), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        # la caja crece con cada dato que aparece (nada de caja vacía): el tamaño de la imagen no cambia, el título no se mueve
        ts0 = list(marcas) + [None] * len(filas)
        vis = sum(1 for i in range(len(filas))
                  if dt >= (ts0[i] if ts0[i] is not None else .4 + i * (dur * .6 / max(1, len(filas)))))
        hv = 60 + tt.height + (30 + sum(f.height + 26 for f, _ in filas[:vis]) + 30 if vis else 24)
        d.rounded_rectangle([12, 16, ancho + 12, hv + 16], 30, fill=(0, 0, 0, 110))
        d.rounded_rectangle([0, 0, ancho, hv], 30, fill=(14, 14, 18, 225), outline=color + (255,), width=5)
        d.rounded_rectangle([0, 0, ancho, 60 + tt.height], 30, fill=color + (255,))
        d.rectangle([0, 40 + tt.height - 10, ancho, 60 + tt.height], fill=color + (255,))
        im.alpha_composite(tt, ((ancho - tt.width) // 2, 30))
        y = 60 + tt.height + 30
        ts = list(marcas) + [None] * len(filas)
        for i, (fi, m) in enumerate(filas):
            ti = ts[i] if ts[i] is not None else .4 + i * (dur * .6 / max(1, len(filas)))
            if dt >= ti:
                k = ease((dt - ti) / .3)
                cx, cy = 70, y + fi.height // 2
                if m == "x":
                    d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=ROJO + (255,))
                    d.line([cx - 14, cy - 14, cx + 14, cy + 14], fill=BLANCO, width=8)
                    d.line([cx - 14, cy + 14, cx + 14, cy - 14], fill=BLANCO, width=8)
                elif m == "v":
                    d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=VERDE + (255,))
                    d.line([cx - 15, cy, cx - 4, cy + 12, cx + 16, cy - 13], fill=BLANCO, width=8)
                else:
                    d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=color + (255,))
                fa = fi.copy()
                fa.putalpha(fa.getchannel("A").point(lambda v: int(v * k)))
                im.alpha_composite(fa, (120 + int((1 - k) * 40), y))
            y += fi.height + 26
        e = ease(dt / .3) * (1 - ease((dt - dur + .3) / .3))
        sc = .85 + .15 * e
        im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS)
        a = np.array(im)
        a[:, :, 3] = (a[:, :, 3] * e).astype(np.uint8)
        return a_bgra(Image.fromarray(a))
    return fn


# ------------------------------------------------------------------ cifra gigante
def cifra(num, texto, color=AMAR, sub=None, desde=0):
    lab = texto_img(texto, 72)
    sb = texto_img(sub, 44, (235, 235, 235), b=5) if sub else None

    def fn(dt, dur, marcas):
        k = ease(dt / max(.6, min(1.4, dur * .4)))
        v = int(round(desde + (num - desde) * k))
        n = texto_img(f"{v:,}".replace(",", " "), 230, color if k < 1 else BLANCO, b=10)
        sc = pop(dt - 1.4, .4) if dt > 1.4 else 1.0
        n = n.resize((int(n.width * sc), int(n.height * sc)), Image.LANCZOS)
        ww = max(n.width, lab.width, sb.width if sb else 0)
        hh = n.height + lab.height + (sb.height if sb else 0)
        im = Image.new("RGBA", (ww, hh), (0, 0, 0, 0))
        im.alpha_composite(n, ((ww - n.width) // 2, 0))
        im.alpha_composite(lab, ((ww - lab.width) // 2, n.height - 20))
        if sb:
            im.alpha_composite(sb, ((ww - sb.width) // 2, n.height + lab.height - 30))
        e = ease(dt / .25) * (1 - ease((dt - dur + .25) / .25))
        a = np.array(im)
        a[:, :, 3] = (a[:, :, 3] * e).astype(np.uint8)
        return a_bgra(Image.fromarray(a))
    return fn


# ------------------------------------------------------------------ balanza neutral
def balanza():
    L1, L2 = texto_img("RIESGO", 70, BLANCO), texto_img("DERRAMA", 70, BLANCO)
    s1 = texto_img("cierre · accidentes", 32, (240, 240, 240), b=4, nombre="segoeuib.ttf", var=None)
    s2 = texto_img("turismo · comercio", 32, (240, 240, 240), b=4, nombre="segoeuib.ttf", var=None)
    q = texto_img("¿?", 160, AMAR, b=8)

    def fn(dt, dur, marcas):
        im = Image.new("RGBA", (W, 1000), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        ang = math.radians(9 * math.sin(dt * 1.7))           # oscila, nunca se queda de un lado
        cx, cy, L = W // 2, 260, 320
        e = ease(dt / .4) * (1 - ease((dt - dur + .3) / .3))
        d.polygon([(cx, cy - 10), (cx - 70, cy + 560), (cx + 70, cy + 560)], fill=(30, 30, 36, 235))
        d.rectangle([cx - 160, cy + 560, cx + 160, cy + 590], fill=(30, 30, 36, 235))
        p1 = (cx - L * math.cos(ang), cy - L * math.sin(ang))
        p2 = (cx + L * math.cos(ang), cy + L * math.sin(ang))
        d.line([p1, p2], fill=(250, 250, 250, 255), width=14)
        d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=AMAR + (255,))
        for p, col, lab, sb in ((p1, ROJO, L1, s1), (p2, VERDE, L2, s2)):
            d.line([p, (p[0], p[1] + 170)], fill=(220, 220, 220, 255), width=5)
            px, py = p[0], p[1] + 170
            d.chord([px - 150, py - 80, px + 150, py + 80], 0, 180, fill=col + (240,))
            im.alpha_composite(lab, (int(px - lab.width / 2), int(py + 70)))
            im.alpha_composite(sb, (int(min(max(10, px - sb.width / 2), W - sb.width - 10)), int(py + 70 + lab.height)))
        im.alpha_composite(q, ((W - q.width) // 2, 20 + int(8 * math.sin(dt * 3))))
        a = np.array(im)
        a[:, :, 3] = (a[:, :, 3] * e).astype(np.uint8)
        return a_bgra(Image.fromarray(a))
    return fn


# ------------------------------------------------------------------ crédito
def credito(texto):
    t = texto_img(texto, 26, BLANCO, b=0, nombre="segoeuib.ttf", var=None)
    im = Image.new("RGBA", (t.width + 28, t.height + 14), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle([0, 0, im.width - 1, im.height - 1], 12, fill=(0, 0, 0, 150))
    im.alpha_composite(t, (14, 7))
    arr = a_bgra(im)

    def fn(dt, dur, marcas):
        return arr
    return fn


def hoja(fn, dur, marcas, salida, n=6):
    """Prueba: n cuadros del MG sobre gris, en fila."""
    cuadros = []
    for i in range(n):
        dt = dur * (i + .5) / n
        a = fn(dt, dur, marcas)
        fondo = np.full((H, W, 3), 90, np.uint8)
        h, w = a.shape[:2]
        x, y = (W - w) // 2, (H - h) // 2
        x0, y0 = max(0, x), max(0, y)
        sub = a[y0 - y:y0 - y + min(h, H - y0), x0 - x:x0 - x + min(w, W - x0)]
        al = sub[:, :, 3:4] / 255.0
        roi = fondo[y0:y0 + sub.shape[0], x0:x0 + sub.shape[1]]
        fondo[y0:y0 + sub.shape[0], x0:x0 + sub.shape[1]] = (roi * (1 - al) + sub[:, :, :3] * al).astype(np.uint8)
        cuadros.append(cv2.resize(fondo, (360, 640)))
    cv2.imwrite(salida, np.hstack(cuadros))
